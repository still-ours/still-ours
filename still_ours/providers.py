"""Multi-provider synchronous & 50%-off official Batch API adapters.

Supports:
- Local OpenAI-compatible servers (Ollama, LM Studio, vLLM, llama.cpp) — zero API key needed
- First-party REST & Batch APIs: OpenAI, Anthropic, Google Gemini, Mistral, DeepSeek
- OpenRouter (first-party / full-precision routing enforced, no reduced-precision fallbacks)
"""
from __future__ import annotations

import json
import os
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


PROVIDER_DEFAULTS = {
    "openai": {"base_url": "https://api.openai.com/v1", "env_key": "OPENAI_API_KEY"},
    "anthropic": {"base_url": "https://api.anthropic.com/v1", "env_key": "ANTHROPIC_API_KEY"},
    "gemini": {"base_url": "https://generativelanguage.googleapis.com/v1beta/openai", "env_key": "GEMINI_API_KEY"},
    "mistral": {"base_url": "https://api.mistral.ai/v1", "env_key": "MISTRAL_API_KEY"},
    "deepseek": {"base_url": "https://api.deepseek.com/v1", "env_key": "DEEPSEEK_API_KEY"},
    "openrouter": {"base_url": "https://openrouter.ai/api/v1", "env_key": "OPENROUTER_API_KEY"},
    "ollama": {"base_url": "http://localhost:11434/v1", "env_key": None},
}

OPENROUTER_FIRST_PARTY = {
    "openai": ["openai"],
    "anthropic": ["anthropic"],
    "google": ["google-ai-studio", "google-vertex"],
    "x-ai": ["xai"],
    "deepseek": ["deepseek"],
    "qwen": ["alibaba"],
    "moonshotai": ["moonshotai"],
    "mistralai": ["mistral"],
}
FULL_PRECISION_QUANTIZATIONS = ["bf16", "fp16", "fp32", "unknown"]


def infer_provider(model_id: str, provider: Optional[str] = None, base_url: Optional[str] = None) -> str:
    if provider and provider != "auto":
        return provider.lower()
    if base_url:
        if "11434" in base_url or "localhost" in base_url or "127.0.0.1" in base_url:
            return "ollama"
        return "openai-compatible"
    low = model_id.lower()
    if low.startswith("ollama/"):
        return "ollama"
    if "/" in model_id and os.environ.get("OPENROUTER_API_KEY") and not os.environ.get("OPENAI_API_KEY"):
        return "openrouter"
    if low.startswith(("gpt-", "o1", "o3", "o4", "openai/")):
        return "openai" if os.environ.get("OPENAI_API_KEY") else "openrouter"
    if low.startswith(("claude-", "anthropic/")):
        return "anthropic" if os.environ.get("ANTHROPIC_API_KEY") else "openrouter"
    if low.startswith(("gemini-", "google/")):
        return "gemini" if os.environ.get("GEMINI_API_KEY") else "openrouter"
    if low.startswith(("mistral-", "pixtral-", "codestral-", "mistralai/")):
        return "mistral" if os.environ.get("MISTRAL_API_KEY") else "openrouter"
    if low.startswith(("deepseek-", "deepseek/")):
        return "deepseek" if os.environ.get("DEEPSEEK_API_KEY") else "openrouter"
    if os.environ.get("OPENROUTER_API_KEY"):
        return "openrouter"
    return "ollama"


def strip_vendor_prefix(model_id: str, provider: str) -> str:
    if provider == "openrouter":
        return model_id
    if provider == "ollama" and model_id.lower().startswith("ollama/"):
        return model_id.split("/", 1)[1]
    for pfx in ("openai/", "anthropic/", "google/", "mistralai/", "deepseek/"):
        if model_id.lower().startswith(pfx):
            return model_id.split("/", 1)[1]
    return model_id


def resolve_credentials(provider: str, api_key: Optional[str] = None, base_url: Optional[str] = None) -> Tuple[str, Optional[str]]:
    spec = PROVIDER_DEFAULTS.get(provider, {})
    url = (base_url or spec.get("base_url") or "http://localhost:11434/v1").rstrip("/")
    key = api_key
    if not key and spec.get("env_key"):
        key = os.environ.get(spec["env_key"])
        if provider == "gemini" and not key:
            key = os.environ.get("GOOGLE_API_KEY")
    if provider in ("ollama", "openai-compatible") and not key:
        key = os.environ.get("API_KEY", "local-no-key")
    return url, key


def _anthropic_max_tokens(wire_model: str, requested: int) -> int:
    # Legacy Claude 3 / 3.5 capped output at 4096/8192; Claude 3.7, 4.x, 4.5, and 5.x support 64000+
    low = wire_model.lower()
    if "claude-3-5" in low:
        return min(requested, 8192)
    if "claude-3-" in low:
        return min(requested, 4096)
    return requested


def _default_openrouter_routing(model_id: str, explicit_order: Optional[List[str]] = None) -> Dict[str, Any]:
    if explicit_order:
        return {"order": explicit_order, "allow_fallbacks": False}
    vendor = model_id.split("/")[0].lower() if "/" in model_id else ""
    first = OPENROUTER_FIRST_PARTY.get(vendor)
    if first:
        return {"order": first, "allow_fallbacks": False}
    return {"allow_fallbacks": False, "quantizations": FULL_PRECISION_QUANTIZATIONS}


def call_sync(
    model_id: str,
    prompt: str,
    max_tokens: int = 64000,
    provider: str = "auto",
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
    openrouter_providers: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Stateless single-message call with zero system prompt and provider-default temperature.

    Follows frozen protocol retry discipline: retries ONLY transient HTTP 429/5xx or pre-connection
    failures (`requests.ConnectionError`). Never retries `ReadTimeout` (which may have already reached
    generation), recording it instead as `timeout_unknown`.
    """
    import requests

    prov = infer_provider(model_id, provider, base_url)
    url, key = resolve_credentials(prov, api_key, base_url)
    wire_model = strip_vendor_prefix(model_id, prov)

    if prov not in ("ollama", "openai-compatible") and not key:
        env_hint = PROVIDER_DEFAULTS.get(prov, {}).get("env_key", "API_KEY")
        raise RuntimeError(f"Missing API key for provider '{prov}'. Export {env_hint} or pass --api-key.")

    if prov == "anthropic":
        eff_max = _anthropic_max_tokens(wire_model, max_tokens)
        req_params = {
            "endpoint": f"{url}/messages",
            "anthropic_version": "2023-06-01",
            "model": wire_model,
            "max_tokens": eff_max,
            "system_prompt": None,
            "temperature": "provider_default",
        }
        headers = {
            "x-api-key": key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        }
        body = {
            "model": wire_model,
            "max_tokens": eff_max,
            "messages": [{"role": "user", "content": prompt}],
        }
        last_err = None
        for attempt in range(3):
            try:
                r = requests.post(f"{url}/messages", headers=headers, json=body, timeout=(30, 2400))
                if r.status_code in (429, 500, 502, 503, 529):
                    last_err = f"HTTP {r.status_code}: {r.text[:300]}"
                    time.sleep(15 * (attempt + 1))
                    continue
                j = r.json() if "json" in r.headers.get("content-type", "") else {}
                text_parts = [b.get("text", "") for b in (j.get("content") or []) if b.get("type") == "text"]
                text = "\n".join(text_parts)
                stop_reason = j.get("stop_reason")
                finish = "length" if stop_reason == "max_tokens" else ("stop" if stop_reason == "end_turn" else stop_reason)
                usage = j.get("usage") or {}
                return {
                    "http_status": r.status_code,
                    "provider": "anthropic",
                    "model_served": j.get("model", wire_model),
                    "generation_id": j.get("id"),
                    "finish_reason": finish,
                    "text": text,
                    "usage": {
                        "prompt_tokens": usage.get("input_tokens"),
                        "completion_tokens": usage.get("output_tokens"),
                    },
                    "request_params": req_params,
                    "raw": j or r.text,
                }
            except requests.exceptions.ReadTimeout as e:
                # Request reached server; never re-ask under frozen protocol rules
                return {
                    "http_status": None,
                    "provider": "anthropic",
                    "finish_reason": "timeout_unknown",
                    "text": "",
                    "error": repr(e),
                    "request_params": req_params,
                    "raw": repr(e),
                }
            except requests.exceptions.ConnectionError as e:
                last_err = repr(e)
                time.sleep(15 * (attempt + 1))
        return {"http_status": None, "provider": "anthropic", "text": "", "error": last_err, "request_params": req_params, "raw": last_err}

    # OpenAI-compatible (OpenAI, Gemini OpenAI compat, Mistral, DeepSeek, OpenRouter, Ollama)
    headers = {"Content-Type": "application/json"}
    if key:
        headers["Authorization"] = f"Bearer {key}"
    if prov == "openrouter":
        headers["X-Title"] = "Still Ours?"

    body: Dict[str, Any] = {
        "model": wire_model,
        "messages": [{"role": "user", "content": prompt}],
    }
    if prov == "openai" and wire_model.startswith(("o1", "o3", "o4", "gpt-5", "gpt-6")):
        body["max_completion_tokens"] = max_tokens
    else:
        body["max_tokens"] = max_tokens

    routing_cfg = None
    if prov == "openrouter":
        routing_cfg = _default_openrouter_routing(wire_model, openrouter_providers)
        body["provider"] = routing_cfg

    req_params = {
        "endpoint": f"{url}/chat/completions",
        "model": wire_model,
        "max_tokens": max_tokens,
        "system_prompt": None,
        "temperature": "provider_default",
        "provider_routing": routing_cfg,
    }

    last_err = None
    for attempt in range(3):
        try:
            r = requests.post(f"{url}/chat/completions", headers=headers, json=body, timeout=(30, 2400))
            if r.status_code in (429, 500, 502, 503, 504):
                last_err = f"HTTP {r.status_code}: {r.text[:300]}"
                time.sleep(15 * (attempt + 1))
                continue
            j = r.json() if "json" in r.headers.get("content-type", "") else {}
            text, finish = "", None
            try:
                msg = j["choices"][0]["message"]
                text = msg.get("content") or ""
                finish = j["choices"][0].get("finish_reason")
            except Exception:
                pass
            return {
                "http_status": r.status_code,
                "provider": j.get("provider") or prov,
                "model_served": j.get("model") or wire_model,
                "generation_id": j.get("id"),
                "finish_reason": finish,
                "text": text,
                "usage": j.get("usage") or {},
                "request_params": req_params,
                "raw": j or r.text,
            }
        except requests.exceptions.ReadTimeout as e:
            return {
                "http_status": None,
                "provider": prov,
                "finish_reason": "timeout_unknown",
                "text": "",
                "error": repr(e),
                "request_params": req_params,
                "raw": repr(e),
            }
        except requests.exceptions.ConnectionError as e:
            last_err = repr(e)
            time.sleep(15 * (attempt + 1))
    return {"http_status": None, "provider": prov, "text": "", "error": last_err, "request_params": req_params, "raw": last_err}


# ---------------------------------------------------------------------------
# Official 50%-Off Asynchronous Batch APIs (OpenAI & Anthropic)
# ---------------------------------------------------------------------------

def submit_batch(
    provider: str,
    jobs: List[Dict[str, Any]],
    batch_dir: Path,
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    """Submit an asynchronous 50%-discount official Batch job (OpenAI or Anthropic)."""
    import requests

    prov = provider.lower()
    url, key = resolve_credentials(prov, api_key)
    if not key:
        env_hint = PROVIDER_DEFAULTS.get(prov, {}).get("env_key", "API_KEY")
        raise RuntimeError(f"Missing API key for {prov} Batch API. Export {env_hint}.")

    batch_dir.mkdir(parents=True, exist_ok=True)

    if prov == "anthropic":
        requests_payload = []
        for job in jobs:
            wm = strip_vendor_prefix(job["model"], "anthropic")
            eff_max = _anthropic_max_tokens(wm, job.get("max_tokens", 64000))
            requests_payload.append({
                "custom_id": job["custom_id"],
                "params": {
                    "model": wm,
                    "max_tokens": eff_max,
                    "messages": [{"role": "user", "content": job["prompt"]}],
                },
            })
        (batch_dir / "batch_input.json").write_text(json.dumps(requests_payload, ensure_ascii=False, indent=2))
        r = requests.post(
            f"{url}/messages/batches",
            headers={
                "x-api-key": key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            json={"requests": requests_payload},
            timeout=120,
        )
        r.raise_for_status()
        info = r.json()
        meta = {
            "provider": "anthropic",
            "anthropic_version": "2023-06-01",
            "batch_id": info["id"],
            "submitted_response": info,
            "jobs": jobs,
        }
        (batch_dir / "batch_meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2))
        return meta

    elif prov == "openai":
        jsonl_path = batch_dir / "batch_input.jsonl"
        with jsonl_path.open("w", encoding="utf-8") as fh:
            for job in jobs:
                wm = strip_vendor_prefix(job["model"], "openai")
                tok_key = "max_completion_tokens" if wm.startswith(("o1", "o3", "o4", "gpt-5", "gpt-6")) else "max_tokens"
                line = {
                    "custom_id": job["custom_id"],
                    "method": "POST",
                    "url": "/v1/chat/completions",
                    "body": {
                        "model": wm,
                        "messages": [{"role": "user", "content": job["prompt"]}],
                        tok_key: job.get("max_tokens", 64000),
                    },
                }
                fh.write(json.dumps(line, ensure_ascii=False) + "\n")
        with jsonl_path.open("rb") as fh:
            fr = requests.post(
                f"{url}/files",
                headers={"Authorization": f"Bearer {key}"},
                files={"file": ("batch_input.jsonl", fh, "application/jsonl")},
                data={"purpose": "batch"},
                timeout=120,
            )
        fr.raise_for_status()
        file_id = fr.json()["id"]
        br = requests.post(
            f"{url}/batches",
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
            json={"input_file_id": file_id, "endpoint": "/v1/chat/completions", "completion_window": "24h"},
            timeout=120,
        )
        br.raise_for_status()
        info = br.json()
        meta = {"provider": "openai", "batch_id": info["id"], "input_file_id": file_id, "submitted_response": info, "jobs": jobs}
        (batch_dir / "batch_meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2))
        return meta

    else:
        raise ValueError(f"Batch API currently supports 'openai' and 'anthropic' (got '{provider}').")


def check_or_collect_batch(batch_dir: Path, api_key: Optional[str] = None) -> Tuple[str, Optional[List[Dict[str, Any]]]]:
    """Check batch status; if completed/ended, download and normalize all replies."""
    import requests

    meta = json.loads((batch_dir / "batch_meta.json").read_text())
    prov = meta["provider"]
    batch_id = meta["batch_id"]
    url, key = resolve_credentials(prov, api_key)

    if prov == "anthropic":
        headers = {"x-api-key": key, "anthropic-version": "2023-06-01"}
        r = requests.get(f"{url}/messages/batches/{batch_id}", headers=headers, timeout=60)
        r.raise_for_status()
        info = r.json()
        status = info.get("processing_status", "unknown")
        if status != "ended":
            return status, None
        res_url = info.get("results_url")
        rr = requests.get(res_url, headers=headers, timeout=300)
        rr.raise_for_status()
        (batch_dir / "batch_results_raw.jsonl").write_text(rr.text)
        results = []
        for line in rr.text.splitlines():
            if not line.strip():
                continue
            obj = json.loads(line)
            cid = obj["custom_id"]
            res = obj.get("result") or {}
            msg = res.get("message") or {}
            text = "\n".join(b.get("text", "") for b in (msg.get("content") or []) if b.get("type") == "text")
            sr = msg.get("stop_reason")
            finish = "length" if sr == "max_tokens" else ("stop" if sr == "end_turn" else sr)
            u = msg.get("usage") or {}
            results.append({
                "custom_id": cid,
                "http_status": 200 if res.get("type") == "succeeded" else 500,
                "provider": "anthropic-batch",
                "model_served": msg.get("model"),
                "generation_id": msg.get("id"),
                "finish_reason": finish,
                "text": text,
                "usage": {"prompt_tokens": u.get("input_tokens"), "completion_tokens": u.get("output_tokens")},
                "raw": obj,
            })
        return "completed", results

    elif prov == "openai":
        headers = {"Authorization": f"Bearer {key}"}
        r = requests.get(f"{url}/batches/{batch_id}", headers=headers, timeout=60)
        r.raise_for_status()
        info = r.json()
        status = info.get("status", "unknown")
        if status != "completed":
            return status, None
        out_id = info.get("output_file_id")
        rr = requests.get(f"{url}/files/{out_id}/content", headers=headers, timeout=300)
        rr.raise_for_status()
        (batch_dir / "batch_results_raw.jsonl").write_text(rr.text)
        results = []
        for line in rr.text.splitlines():
            if not line.strip():
                continue
            obj = json.loads(line)
            cid = obj["custom_id"]
            resp = obj.get("response") or {}
            body = resp.get("body") or {}
            text, finish = "", None
            try:
                text = body["choices"][0]["message"].get("content") or ""
                finish = body["choices"][0].get("finish_reason")
            except Exception:
                pass
            results.append({
                "custom_id": cid,
                "http_status": resp.get("status_code"),
                "provider": "openai-batch",
                "model_served": body.get("model"),
                "generation_id": body.get("id"),
                "finish_reason": finish,
                "text": text,
                "usage": body.get("usage") or {},
                "raw": obj,
            })
        return "completed", results

    raise ValueError(f"Unsupported batch provider: {prov}")
