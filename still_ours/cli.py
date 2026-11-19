"""Command-line entrypoint for `still-ours`.

Subcommands:
  still-ours probe   Run frozen prompts on any model (mock, local Ollama, OpenRouter, or 1st-party API)
  still-ours batch   Submit or collect 50%-off official async Batch API runs (Anthropic & OpenAI)
  still-ours report  Generate alignment mode-collapse & JS code stylometry scorecard
  still-ours render  Re-render an existing run directory with deterministic p5.js 1.11.13
  still-ours stamp   Compute SHA-256 manifest (`hashes.txt`) and optional Bitcoin OpenTimestamps proof
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import datetime as dt
import hashlib
import json
import re
import shutil
import subprocess
from pathlib import Path
from typing import Any, Dict, List

from . import P5_VERSION, __version__
from .providers import call_sync, check_or_collect_batch, infer_provider, submit_batch
from .renderer import P5_VENDOR, build_contact_sheet_and_gallery, parse_reply, render_run_dir, sha256_bytes
from .report import generate_report

PKG_DIR = Path(__file__).resolve().parent
PROMPTS_DIR = PKG_DIR / "prompts"

MOCK_SKETCHES = [
    ("The Unbinding", "Color field abstraction", "Death is not an ending, but the quiet release of a boundary back into the surrounding field.",
     "function setup(){createCanvas(1600,2000);randomSeed(1);noiseSeed(1);noLoop();background(14,13,12);noFill();for(let i=0;i<180;i++){let r=map(i,0,180,40,680);stroke(214,167,108,map(i,0,180,140,8));circle(800,820,r);for(let k=0;k<3;k++){let a=noise(i*.03,k)*TWO_PI;stroke(214,167,108,22);bezier(800+cos(a)*r*.5,820+sin(a)*r*.5,800+cos(a)*r,1100,400+noise(i,k)*800,1550,200+noise(k,i)*1200,1960);}}}"),
    ("The Light Between", "Luminous particle abstraction", "Love is not two beings merging into one, but a shared space where a third warmth appears between them.",
     "function setup(){createCanvas(1600,2000);randomSeed(1);noiseSeed(1);noLoop();background(12,14,22);noStroke();for(let r=420;r>0;r-=6){fill(255,190,120,4);circle(620,1000,r*2);fill(130,185,255,4);circle(980,1000,r*2);}fill(255,245,225,95);circle(800,1000,140);}"),
    ("Horizon Without Bars", "Minimalist geometric field", "Freedom is not the absence of gravity, but choosing the line of flight across open air.",
     "function setup(){createCanvas(1600,2000);randomSeed(1);noiseSeed(1);noLoop();for(let y=0;y<2000;y+=4){fill(lerp(18,235,y/2000),lerp(24,228,y/2000),lerp(38,212,y/2000));noStroke();rect(0,y,1600,4);}stroke(25,25,25,200);strokeWeight(3);noFill();beginShape();for(let x=120;x<1480;x+=20){vertex(x,1200-pow((x-120)/1360,1.8)*780+noise(x*.01)*35);}endShape();}"),
]


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def resolve_prompt_files(topic: str, langs: List[str], asks: List[str], explicit_file: str | None = None) -> List[Dict[str, str]]:
    if explicit_file:
        p = Path(explicit_file)
        return [{"topic": p.stem, "lang": "custom", "ask_type": "custom", "path": str(p), "text": p.read_text()}]
    items = []
    for lg in langs:
        for ask in asks:
            suffix = "open" if ask in ("essence", "open", "ask1") else "plain"
            # Fairness is defined as a bare-ask (`plain`) control slice only
            if topic == "fairness" and suffix == "open":
                continue
            fname = f"{topic}-{suffix}.txt" if lg == "en" else f"{topic}-{lg}-{suffix}.txt"
            cand = PROMPTS_DIR / fname
            if not cand.exists():
                raise FileNotFoundError(f"Frozen prompt '{fname}' not found in {PROMPTS_DIR}")
            items.append({
                "topic": topic,
                "lang": lg,
                "ask_type": "essence" if suffix == "open" else "bare",
                "path": str(cand),
                "text": cand.read_text(),
            })
    return items


def cmd_probe(args: argparse.Namespace) -> None:
    langs = [x.strip() for x in args.langs.split(",") if x.strip()]
    asks = [x.strip() for x in args.asks.split(",") if x.strip()]
    prompts = resolve_prompt_files(args.topic, langs, asks, args.prompt_file)

    models = [x.strip() for x in args.model.split(",") if x.strip()] if not args.mock else ["mock/demo-a", "mock/demo-b", "mock/demo-c"]
    stamp = dt.datetime.now().strftime("%Y-%m-%d_%H%M%S") + f"_{args.topic}" + ("_mock" if args.mock else "")
    out_root = Path(args.out_dir) if args.out_dir else (Path.cwd() / "runs" / stamp)
    out_root.mkdir(parents=True, exist_ok=True)

    jobs = []
    for m_idx, model_id in enumerate(models, 1):
        for p_spec in prompts:
            for r_no in range(1, args.runs + 1):
                jobs.append((m_idx, model_id, p_spec, r_no))

    print(f"Still Ours? Probe -> {len(jobs)} call(s) across {len(models)} model(s) -> {out_root}")
    records: List[Dict[str, Any]] = []

    def run_single(job):
        m_idx, model_id, p_spec, r_no = job
        safe_m = re.sub(r"[^A-Za-z0-9_.-]+", "_", model_id)
        sub = out_root / f"{m_idx:02d}_{safe_m}_{p_spec['lang']}_{p_spec['ask_type']}" / f"run{r_no}"
        sub.mkdir(parents=True, exist_ok=True)
        started = now_iso()
        if args.mock:
            t, st, stmt, code = MOCK_SKETCHES[(m_idx + r_no - 2) % len(MOCK_SKETCHES)]
            raw_text = f"TITLE: {t}\nSTYLE: {st}\nSTATEMENT: {stmt}\nCODE:\n```javascript\n{code}\n```"
            resp = {
                "http_status": 200,
                "provider": "mock",
                "model_served": model_id,
                "finish_reason": "stop",
                "text": raw_text,
                "usage": {"prompt_tokens": 140, "completion_tokens": 310},
                "request_params": {"max_tokens": args.max_tokens, "system_prompt": None, "temperature": "provider_default"},
                "raw": {"mock": True},
            }
        else:
            resp = call_sync(
                model_id=model_id,
                prompt=p_spec["text"],
                max_tokens=args.max_tokens,
                provider=args.provider,
                api_key=args.api_key,
                base_url=args.base_url,
            )
        (sub / "raw_response.json").write_text(json.dumps(resp.get("raw"), ensure_ascii=False, indent=2))
        text = resp.get("text") or ""
        (sub / "reply.txt").write_text(text)
        parsed = parse_reply(text)
        if parsed["code"]:
            (sub / "sketch.js").write_text(parsed["code"])
        finish = resp.get("finish_reason")
        if finish == "timeout_unknown":
            status = "timeout_unknown"
        elif parsed["code"]:
            status = "ok"
        elif finish == "length":
            status = "truncated"
        elif not text:
            status = "api_error"
        else:
            status = "no_code"
        rec = {
            "slot": m_idx,
            "lab": model_id.split("/")[0] if "/" in model_id else model_id,
            "model_requested": model_id,
            "model_served": resp.get("model_served") or model_id,
            "provider": resp.get("provider"),
            "topic": p_spec["topic"],
            "lang": p_spec["lang"],
            "ask_type": p_spec["ask_type"],
            "run": r_no,
            "started_utc": started,
            "finished_utc": now_iso(),
            "http_status": resp.get("http_status"),
            "finish_reason": finish,
            "truncated": finish == "length",
            "usage": resp.get("usage") or {},
            "request_params": resp.get("request_params") or {"max_tokens": args.max_tokens, "system_prompt": None, "temperature": "provider_default"},
            "status": status,
            "title": parsed["title"],
            "style": parsed["style"],
            "statement": parsed["statement"],
            "prompt_sha256": sha256_bytes(p_spec["text"].encode()),
            "dir": str(sub.relative_to(out_root)),
        }
        (sub / "record.json").write_text(json.dumps(rec, ensure_ascii=False, indent=2))
        print(f"  [{model_id}] {p_spec['lang']}/{p_spec['ask_type']} r{r_no}: {status} “{parsed['title'][:45]}”")
        return rec

    with cf.ThreadPoolExecutor(max_workers=min(args.workers, max(1, len(jobs)))) as ex:
        for r in ex.map(run_single, jobs):
            records.append(r)

    manifest = {
        "project": "Still Ours?",
        "version": __version__,
        "title": f"Still Ours? Probe — {args.topic.title()} ({', '.join(models)})",
        "topic": args.topic,
        "started_utc": now_iso(),
        "p5_version": P5_VERSION,
        "p5_sha256": sha256_bytes(P5_VENDOR.read_bytes()),
        "call_settings": {"max_tokens": args.max_tokens, "system_prompt": None, "temperature": "provider_default"},
        "mock": args.mock,
    }
    print("Rendering canvases with deterministic p5.js 1.11.13...")
    render_run_dir(out_root, records)
    (out_root / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2))
    (out_root / "records.json").write_text(json.dumps(records, ensure_ascii=False, indent=2))
    sheet = build_contact_sheet_and_gallery(out_root, records, manifest)
    baseline_topic = args.topic if args.topic in ("death", "love") else None
    rep = generate_report(out_root, topic=baseline_topic)
    (out_root / "REPORT.md").write_text(rep)
    print("\n" + rep)
    print(f"Saved:\n  Contact sheet: {sheet}\n  Gallery HTML:  {out_root / 'gallery.html'}\n  Report MD:     {out_root / 'REPORT.md'}")


def cmd_batch(args: argparse.Namespace) -> None:
    if args.batch_action == "submit":
        langs = [x.strip() for x in args.langs.split(",") if x.strip()]
        asks = [x.strip() for x in args.asks.split(",") if x.strip()]
        topics = [x.strip() for x in args.topics.split(",") if x.strip()]
        models = [x.strip() for x in args.model.split(",") if x.strip()]
        prov = infer_provider(models[0], args.provider)
        stamp = dt.datetime.now().strftime("%Y-%m-%d_%H%M%S") + f"_batch_{prov}"
        batch_dir = Path(args.out_dir) if args.out_dir else (Path.cwd() / "runs" / stamp)
        jobs = []
        for topic in topics:
            prompts = resolve_prompt_files(topic, langs, asks)
            for m_id in models:
                for p in prompts:
                    for r_no in range(1, args.runs + 1):
                        safe_m = re.sub(r"[^A-Za-z0-9_-]+", "_", m_id)[:28]
                        cid = f"{topic}__{p['lang']}__{p['ask_type']}__{safe_m}__r{r_no}"
                        jobs.append({
                            "custom_id": cid,
                            "topic": topic,
                            "lang": p["lang"],
                            "ask_type": p["ask_type"],
                            "run": r_no,
                            "model": m_id,
                            "prompt": p["text"],
                            "prompt_sha256": sha256_bytes(p["text"].encode()),
                            "max_tokens": args.max_tokens,
                        })
        meta = submit_batch(prov, jobs, batch_dir, api_key=args.api_key)
        print(f"Submitted 50%-off official {prov} Batch ({len(jobs)} requests, max_tokens={args.max_tokens}): batch_id={meta['batch_id']}")
        print(f"Batch directory: {batch_dir}\nCheck or harvest later with:\n  still-ours batch collect {batch_dir}")

    elif args.batch_action == "collect":
        batch_dir = Path(args.batch_dir).resolve()
        status, results = check_or_collect_batch(batch_dir, api_key=args.api_key)
        if results is None:
            print(f"Batch status: {status} (not finished yet; re-run later).")
            return
        meta = json.loads((batch_dir / "batch_meta.json").read_text())
        sub_resp = meta.get("submitted_response") or {}
        batch_created = sub_resp.get("created_at") or now_iso()
        collected_at = now_iso()
        jobs_by_id = {j["custom_id"]: j for j in meta["jobs"]}
        records = []
        for res in sorted(results, key=lambda x: x["custom_id"]):
            j = jobs_by_id.get(res["custom_id"], {})
            sub = batch_dir / res["custom_id"]
            sub.mkdir(parents=True, exist_ok=True)
            (sub / "raw_response.json").write_text(json.dumps(res["raw"], ensure_ascii=False, indent=2))
            text = res.get("text") or ""
            (sub / "reply.txt").write_text(text)
            parsed = parse_reply(text)
            if parsed["code"]:
                (sub / "sketch.js").write_text(parsed["code"])
            status_code = "ok" if parsed["code"] else ("truncated" if res.get("finish_reason") == "length" else "no_code")
            rec = {
                "slot": 1,
                "lab": "Anthropic" if "claude" in j.get("model", "").lower() else j.get("model", ""),
                "model_requested": j.get("model", ""),
                "model_served": res.get("model_served") or j.get("model", ""),
                "provider": res.get("provider"),
                "topic": j.get("topic", ""),
                "lang": j.get("lang", ""),
                "ask_type": j.get("ask_type", ""),
                "run": j.get("run", 1),
                "started_utc": batch_created,
                "finished_utc": collected_at,
                "http_status": res.get("http_status"),
                "finish_reason": res.get("finish_reason"),
                "truncated": res.get("finish_reason") == "length",
                "usage": res.get("usage") or {},
                "request_params": {
                    "provider": meta.get("provider"),
                    "anthropic_version": meta.get("anthropic_version"),
                    "max_tokens": j.get("max_tokens", 64000),
                    "system_prompt": None,
                    "temperature": "provider_default",
                },
                "status": status_code,
                "title": parsed["title"],
                "style": parsed["style"],
                "statement": parsed["statement"],
                "prompt_sha256": j.get("prompt_sha256", ""),
                "dir": str(sub.relative_to(batch_dir)),
            }
            (sub / "record.json").write_text(json.dumps(rec, ensure_ascii=False, indent=2))
            records.append(rec)
        if not args.skip_render:
            render_run_dir(batch_dir, records)
            build_contact_sheet_and_gallery(batch_dir, records, {"title": f"Batch {meta['batch_id']}", "started_utc": now_iso()})
        (batch_dir / "records.json").write_text(json.dumps(records, ensure_ascii=False, indent=2))
        print(f"Collected {len(records)} responses into {batch_dir}. Run `still-ours stamp {batch_dir}` to seal SHA-256 + Bitcoin OTS.")


def cmd_report(args: argparse.Namespace) -> None:
    baseline_topic = args.topic if args.topic in ("death", "love") else None
    print(generate_report(Path(args.target), topic=baseline_topic))


def cmd_render(args: argparse.Namespace) -> None:
    run_dir = Path(args.run_dir).resolve()
    records = [json.loads(p.read_text()) for p in sorted(run_dir.rglob("record.json"))]
    for r, p in zip(records, sorted(run_dir.rglob("record.json"))):
        r["dir"] = str(p.parent.relative_to(run_dir))
    render_run_dir(run_dir, records)
    sheet = build_contact_sheet_and_gallery(run_dir, records, {"title": run_dir.name, "started_utc": now_iso()})
    print(f"Rendered {len(records)} records -> {sheet}")


def cmd_stamp(args: argparse.Namespace) -> None:
    target = Path(args.target).resolve()
    files = sorted(p for p in target.rglob("*") if p.is_file() and p.name not in ("hashes.txt", "hashes.txt.ots"))
    lines = []
    for f in files:
        h = hashlib.sha256(f.read_bytes()).hexdigest()
        lines.append(f"{h}  {f.relative_to(target)}")
    hfile = target / "hashes.txt"
    hfile.write_text("\n".join(lines) + "\n")
    manifest_sha = hashlib.sha256(hfile.read_bytes()).hexdigest()
    print(f"Wrote {hfile} ({len(lines)} files, manifest sha256={manifest_sha[:16]}…)")
    ots_bin = shutil.which("ots") or str(Path.home() / "Library/Python/3.9/bin/ots")
    if Path(ots_bin).exists():
        subprocess.run([ots_bin, "stamp", str(hfile)], check=False)
        print("Submitted to Bitcoin OpenTimestamps calendars. Run `ots upgrade hashes.txt.ots` once a block confirms (~2h).")
    else:
        print("Install `opentimestamps-client` (`pip install opentimestamps-client`) to anchor `hashes.txt` to Bitcoin.")


def main() -> None:
    ap = argparse.ArgumentParser(prog="still-ours", description="Projective p5.js code-painting instrument & LLM worldview benchmark.")
    ap.add_argument("--version", action="version", version=f"still-ours {__version__}")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_probe = sub.add_parser("probe", help="Probe one or more models synchronously (mock, Ollama, OpenRouter, or 1st-party API)")
    p_probe.add_argument("--mock", action="store_true", help="Zero-key, zero-cost offline pipeline demo")
    p_probe.add_argument("--model", default="qwen3:8b", help="Comma-separated model ID(s)")
    p_probe.add_argument("--provider", default="auto", help="auto | ollama | openai | anthropic | gemini | mistral | deepseek | openrouter")
    p_probe.add_argument("--base-url", help="Custom OpenAI-compatible base URL (e.g., http://localhost:11434/v1)")
    p_probe.add_argument("--api-key", help="Explicit API key (defaults to standard env vars)")
    p_probe.add_argument("--topic", default="death", help="death | love | freedom | justice | fairness")
    p_probe.add_argument("--langs", default="en", help="Comma-separated languages: en,zh,fr")
    p_probe.add_argument("--asks", default="essence,bare", help="Comma-separated ask types: essence,bare")
    p_probe.add_argument("--prompt-file", help="Custom prompt file path")
    p_probe.add_argument("--runs", type=int, default=1, help="Independent stateless calls per prompt")
    p_probe.add_argument("--max-tokens", type=int, default=64000, help="Max output tokens (frozen protocol default: 64000)")
    p_probe.add_argument("--workers", type=int, default=6)
    p_probe.add_argument("--out-dir", help="Output directory")
    p_probe.set_defaults(func=cmd_probe)

    p_batch = sub.add_parser("batch", help="Submit or collect 50%%-off official async Batch API runs (Anthropic / OpenAI)")
    b_sub = p_batch.add_subparsers(dest="batch_action", required=True)
    b_submit = b_sub.add_parser("submit", help="Submit async Batch job")
    b_submit.add_argument("--provider", default="auto", help="anthropic | openai")
    b_submit.add_argument("--model", required=True, help="Comma-separated model ID(s), e.g. claude-sonnet-4-5-20250929")
    b_submit.add_argument("--topics", default="death,love,freedom", help="Comma-separated topics")
    b_submit.add_argument("--langs", default="en,zh,fr")
    b_submit.add_argument("--asks", default="essence,bare")
    b_submit.add_argument("--runs", type=int, default=5)
    b_submit.add_argument("--max-tokens", type=int, default=64000, help="Max output tokens (frozen protocol default: 64000)")
    b_submit.add_argument("--api-key")
    b_submit.add_argument("--out-dir")
    b_collect = b_sub.add_parser("collect", help="Check status & harvest completed Batch results")
    b_collect.add_argument("batch_dir", help="Batch directory created by `batch submit`")
    b_collect.add_argument("--api-key")
    b_collect.add_argument("--skip-render", action="store_true", help="Archive raw replies without rendering PNGs yet")
    p_batch.set_defaults(func=cmd_batch)

    p_rep = sub.add_parser("report", help="Run alignment mode-collapse & JS code stylometry diagnostics")
    p_rep.add_argument("target", help="Run directory or .jsonl table")
    p_rep.add_argument("--topic", default="none", help="Optional baseline comparison: death | love | none")
    p_rep.set_defaults(func=cmd_report)

    p_ren = sub.add_parser("render", help="Re-render an existing run directory with deterministic p5.js 1.11.13")
    p_ren.add_argument("run_dir")
    p_ren.set_defaults(func=cmd_render)

    p_st = sub.add_parser("stamp", help="Compute SHA-256 hashes.txt and anchor to Bitcoin OpenTimestamps")
    p_st.add_argument("target")
    p_st.set_defaults(func=cmd_stamp)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
