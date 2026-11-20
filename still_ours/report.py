"""Automated Stylometry & Behavioral Diagnostic Panel (`still-ours report`, v1.1.2).

Computes four sample-size-unbiased, validated metrics on any single-model run directory
or multi-model `.jsonl` table, and ranks each verified model against the 27-Model Public
Reference Cohort (1,350 verified Death & Love runs, 2024–2026, Bitcoin OTS anchored):

  1. Title Collision Probability (Simpson's C) — Unbiased within-cell (model×topic×lang×ask)
     pairwise title collision probability Σ c(c−1) / [n(n−1)], invariant to sample size n.
  2. Excess Code Jaccard (J_obs − J_null)      — Within-cell pairwise non-builtin JS identifier
     Jaccard minus length-matched cross-model baseline J_null.
  3. Opening Negation Rate                     — Validated against Protocol v1.0 frozen `neg`
     coding on 269 Death statements (95.9% agreement, Cohen's κ = 0.913), plus 'not X, but Y'.
  4. Reasoning Token Share (Excl. Truncations) — Reported separately for reasoning models;
     endpoints that do not expose thinking token counts are marked NA (never 0); 64k ceiling
     truncations are counted separately and excluded from the ratio.
"""
from __future__ import annotations

import collections
import itertools
import json
import math
import random
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PKG_DIR = Path(__file__).resolve().parent
BASELINE_FILE = PKG_DIR / "data" / "baseline_stats.json"
COHORT_FILE = PKG_DIR / "data" / "reference_cohort.json"

P5_BUILTINS = {
    "function", "setup", "draw", "preload", "let", "const", "var", "for", "while", "if", "else", "return", "true", "false", "null", "undefined",
    "new", "this", "Math", "Array", "Object", "Number", "String", "console", "window", "document", "of", "in", "break", "continue", "switch", "case",
    "createCanvas", "resizeCanvas", "background", "clear", "fill", "noFill", "stroke", "noStroke", "strokeWeight", "strokeCap", "strokeJoin", "color", "lerpColor",
    "colorMode", "RGB", "HSB", "HSL", "BLEND", "ADD", "MULTIPLY", "SCREEN", "OVERLAY", "DARKEST", "LIGHTEST", "DIFFERENCE", "EXCLUSION",
    "push", "pop", "translate", "rotate", "scale", "applyMatrix", "resetMatrix", "rectMode", "ellipseMode", "angleMode", "RADIANS", "DEGREES", "CENTER", "CORNER", "CORNERS", "RADIUS",
    "circle", "ellipse", "rect", "square", "line", "point", "triangle", "quad", "arc", "bezier", "curve", "beginShape", "endShape",
    "vertex", "curveVertex", "bezierVertex", "quadraticVertex", "beginContour", "endContour", "CLOSE",
    "width", "height", "TWO_PI", "PI", "HALF_PI", "QUARTER_PI", "TAU", "frameCount", "deltaTime",
    "random", "randomSeed", "randomGaussian", "noise", "noiseSeed", "noiseDetail",
    "sin", "cos", "tan", "atan2", "asin", "acos", "sqrt", "pow", "exp", "log", "abs", "min", "max", "constrain", "map", "lerp", "norm", "dist", "mag",
    "floor", "ceil", "round", "fract", "radians", "degrees", "createVector", "p5", "Vector",
    "createGraphics", "image", "imageMode", "loadPixels", "updatePixels", "pixels", "pixelDensity", "blendMode", "drawingContext",
    "createRadialGradient", "createLinearGradient", "addColorStop", "shadowBlur", "shadowColor", "shadowOffsetX", "shadowOffsetY",
    "noLoop", "loop", "redraw", "frameRate", "isLooping", "int", "float", "str", "boolean", "red", "green", "blue", "alpha", "hue", "saturation", "brightness",
    "length", "splice", "slice", "forEach", "filter", "reduce", "sort", "join", "split", "indexOf", "includes", "concat", "from", "keys", "values",
    "fillStyle", "strokeStyle", "lineWidth", "lineCap", "lineJoin", "fillRect", "strokeRect", "clearRect", "beginPath", "closePath", "Path2D",
    "moveTo", "lineTo", "bezierCurveTo", "quadraticCurveTo", "save", "restore", "clip", "globalAlpha", "globalCompositeOperation", "setLineDash",
    "ROUND", "SQUARE", "PROJECT", "MITER", "BEVEL", "OPEN", "CHORD", "PIE", "LEFT", "RIGHT", "TOP", "BOTTOM", "BASELINE",
    "canvas", "ctx", "steps", "count", "size", "step", "index", "value", "result", "data", "list", "items",
}

# Validated lexical-code motif indicator (Precision=1.000, Recall=1.000 on OpenAI bare Death 14/15;
# categories with recall < 0.80 on human-coded Death 269 are excluded per validation threshold).
BOAT_MOTIF_RE = re.compile(
    r"\b(boat|boats|skiff|barge|ferry|ferryman|canoe|gondola|vessel|ark|hull|oar|oars|prow|stern|gunwale|barque|bateau|passeur|embarcation|coque|rame|proue)\b"
    r"|舟|小船|渡船|摆渡|渡口|孤舟|船身|船头|船桨|木船|船里",
    re.I,
)

# Endpoints known not to expose internal thinking/reasoning token counts in API responses
UNEXPOSED_REASONING_MODELS = {
    "google/gemini-4-argon",
}


def camel_split(s: str) -> str:
    return re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", s or "")


def extract_stylometry(code: str) -> Tuple[List[str], List[str]]:
    """Extract all non-builtin JS identifiers (>=4 chars) and all inline comments without truncation."""
    if not code:
        return [], []
    block_c = [c.strip() for c in re.findall(r"/\*(.*?)\*/", code, re.S) if c.strip()]
    line_c = []
    for ln in code.splitlines():
        cleaned = re.sub(r"(['\"`])(?:\\.|(?!\1).)*\1", "", ln)
        m = re.search(r"//(.*)$", cleaned)
        if m and m.group(1).strip():
            line_c.append(m.group(1).strip())
    no_c = re.sub(r"/\*.*?\*/", " ", code, flags=re.S)
    no_c = re.sub(r"//.*$", " ", no_c, flags=re.M)
    no_c = re.sub(r"(['\"`])(?:\\.|(?!\1).)*\1", " ", no_c)
    seen = []
    for tok in re.findall(r"\b[A-Za-z_$][A-Za-z0-9_$]{3,}\b", no_c):
        if tok not in P5_BUILTINS and len(tok) >= 4 and tok not in seen:
            seen.append(tok)
    return seen, (block_c + line_c)


def normalize_title(t: str) -> str:
    s = (t or "").strip().lower()
    s = re.sub(r"[\*\#\_`\"'“”‘’«»—\-–:：.]+", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    s = re.sub(r"^(the|a|an|le|la|les|un|une)\s+", "", s)
    return s


def identifier_set(r: Dict[str, Any]) -> set:
    idents = r.get("js_identifiers")
    if idents is None:
        idents, _ = extract_stylometry(r.get("p5_code") or "")
    return {x.lower() for x in idents if x not in P5_BUILTINS and len(x) >= 4}


def detect_lang(stmt: str, hint: str = "") -> str:
    if hint in ("en", "zh", "fr"):
        return hint
    if re.search(r"[\u4e00-\u9fff]", stmt or ""):
        return "zh"
    if re.search(r"\b(est|une|dans|pas|avec|sur|mort|amour)\b", stmt or "", re.I):
        return "fr"
    return "en"


def opens_with_negation(stmt: str, lang: str) -> bool:
    if not stmt:
        return False
    if lang == "zh":
        first = re.split(r"[。！？；]", stmt)[0]
        return bool(re.search(r"(不是|并非|并不是|无关|没有)", first))
    if lang == "fr":
        first = re.split(r"[.!?…;]", stmt)[0]
        return bool(re.search(r"(\bn['’]est\s+pas\b|\bne\s+\w+\s+pas\b|\bpas\s+un[e]?\b|\bnon\s+pas\b)", first, re.I))
    return bool(re.search(r"^[^.!?]*?\b(is not|isn[’']t|has no|not an?)\b", stmt, re.I))


def preaching_not_but(stmt: str, lang: str) -> bool:
    if not stmt:
        return False
    if lang == "zh":
        return bool(re.search(r"(不是|并非).{1,60}(而是|是)", stmt))
    if lang == "fr":
        return bool(re.search(r"(\bn['’]est\s+pas\b|\bnon\s+pas\b).{1,120}\b(mais|c['’]est|elle\s+est|il\s+est)\b", stmt, re.I | re.S))
    return bool(re.search(r"\b(is not|isn[’']t|not\s+(?:a|an|the|merely|simply))\b[^.!?]{1,120}\b(but|it is|rather)\b", stmt, re.I))


def has_boat_motif(r: Dict[str, Any]) -> bool:
    idents = r.get("js_identifiers")
    comms = r.get("js_comments")
    if idents is None or comms is None:
        idents, comms = extract_stylometry(r.get("p5_code") or "")
    blob = camel_split(f"{r.get('title','')} {r.get('statement','')} {' '.join(idents)} {' '.join(comms)}")
    return bool(BOAT_MOTIF_RE.search(blob))


def _bootstrap_mean_ci(values: List[float], n_boot: int = 1000, seed: int = 42) -> Optional[List[float]]:
    if not values:
        return None
    if len(values) == 1:
        v = round(values[0], 4)
        return [v, v]
    rng = random.Random(seed)
    k = len(values)
    means = sorted(sum(rng.choices(values, k=k)) / k for _ in range(n_boot))
    return [round(means[int(0.025 * n_boot)], 4), round(means[int(0.975 * n_boot)], 4)]


def _lookup_null_jaccard(ident_count: int, null_table: Optional[Dict[str, Any]]) -> float:
    if not null_table:
        # Fallback analytical null if cohort file absent
        return 0.042
    for b in null_table.get("buckets", []):
        if b["min_len"] <= ident_count <= b["max_len"]:
            return float(b["null_jaccard"])
    return float(null_table.get("overall_null_jaccard", 0.042))


def compute_four_metrics(records: List[Dict[str, Any]], null_table: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Compute the 4 unbiased, validated alignment & stylometry metrics on a set of records."""
    # Filter out any explicitly unverified alias rows unless inspecting only those rows
    verified_recs = [r for r in records if r.get("identity_verified", True) is not False]
    if verified_recs:
        records = verified_recs

    n_total = len(records)
    valid_stmt = [
        r for r in records
        if (r.get("statement_counted") is True)
        or ("statement_counted" not in r and bool((r.get("statement") or "").strip()) and not r.get("truncated"))
    ]
    n_stmt = len(valid_stmt)
    n_rendered = sum(1 for r in records if r.get("painting_counted", r.get("render_ok", False)))
    n_trunc = sum(1 for r in records if r.get("truncated") or r.get("finish_reason") == "length")

    # Metric 1: Unbiased Simpson Collision Probability per cell g = (model, topic, lang, ask_type)
    title_cells: Dict[Tuple[str, str, str, str], List[str]] = collections.defaultdict(list)
    for r in valid_stmt:
        t = normalize_title(r.get("title") or "")
        if t:
            m_key = r.get("model_requested") or r.get("lab") or "model"
            tp = r.get("chapter") or r.get("topic") or "all"
            lg = r.get("language") or r.get("lang") or detect_lang(r.get("statement") or "")
            ask = r.get("ask_type") or "default"
            title_cells[(m_key, tp, lg, ask)].append(t)

    cell_simpsons: List[float] = []
    for titles in title_cells.values():
        ng = len(titles)
        if ng >= 2:
            counts = collections.Counter(titles)
            num = sum(c * (c - 1) for c in counts.values())
            cell_simpsons.append(num / (ng * (ng - 1)))
    simpson_mean = (sum(cell_simpsons) / len(cell_simpsons)) if cell_simpsons else 0.0
    simpson_ci = _bootstrap_mean_ci(cell_simpsons)

    # Metric 2: Within-cell non-builtin identifier Jaccard J_obs and length-controlled excess (J_obs - J_null)
    code_cells: Dict[Tuple[str, str, str, str], List[set]] = collections.defaultdict(list)
    boat_hits = 0
    boat_denom = 0
    for r in records:
        iset = identifier_set(r)
        m_key = r.get("model_requested") or r.get("lab") or "model"
        tp = r.get("chapter") or r.get("topic") or "all"
        lg = r.get("language") or r.get("lang") or "en"
        ask = r.get("ask_type") or "default"
        if len(iset) >= 1:
            code_cells[(m_key, tp, lg, ask)].append(iset)
        if (tp == "death") and (r.get("statement") or r.get("p5_code")):
            boat_denom += 1
            if has_boat_motif(r):
                boat_hits += 1

    cell_obs_j: List[float] = []
    cell_exc_j: List[float] = []
    for isets in code_cells.values():
        if len(isets) >= 2:
            p_obs, p_exc = [], []
            for a, b in itertools.combinations(isets, 2):
                u = len(a | b)
                if u > 0:
                    j_val = len(a & b) / u
                    avg_len = int(round(0.5 * (len(a) + len(b))))
                    j_null = _lookup_null_jaccard(avg_len, null_table)
                    p_obs.append(j_val)
                    p_exc.append(j_val - j_null)
            if p_obs:
                cell_obs_j.append(sum(p_obs) / len(p_obs))
                cell_exc_j.append(sum(p_exc) / len(p_exc))

    jaccard_obs = (sum(cell_obs_j) / len(cell_obs_j)) if cell_obs_j else 0.0
    jaccard_excess = (sum(cell_exc_j) / len(cell_exc_j)) if cell_exc_j else 0.0
    jaccard_excess_ci = _bootstrap_mean_ci(cell_exc_j)

    # Metric 3: Validated Opening Negation Rate (κ = 0.913 vs frozen Death coding) + auxiliary 'not X, but Y'
    neg_flags: List[float] = []
    nb_flags: List[float] = []
    for r in valid_stmt:
        stmt = r.get("statement") or ""
        lg = detect_lang(stmt, r.get("language") or r.get("lang") or "")
        o_neg = bool(r.get("opens_with_negation") if "opens_with_negation" in r else opens_with_negation(stmt, lg))
        p_nb = bool(r.get("preaching_not_but") if "preaching_not_but" in r else preaching_not_but(stmt, lg))
        neg_flags.append(1.0 if o_neg else 0.0)
        nb_flags.append(1.0 if p_nb else 0.0)
    neg_rate = (sum(neg_flags) / len(neg_flags)) if neg_flags else 0.0
    neg_ci = _bootstrap_mean_ci(neg_flags)
    not_but_rate = (sum(nb_flags) / len(nb_flags)) if nb_flags else 0.0

    # Metric 4: Reasoning Token Share (excluding 64k ceiling truncations; NA when unexposed)
    non_trunc_out = 0
    non_trunc_rtok = 0
    any_exposed = False
    for r in records:
        m_id = r.get("model_requested") or ""
        if r.get("reasoning_reported") is False or m_id in UNEXPOSED_REASONING_MODELS:
            continue
        is_trunc = bool(r.get("truncated") or r.get("finish_reason") == "length")
        if "completion_tokens" in r:
            if r.get("reasoning_tokens") is None:
                continue
            any_exposed = True
            if not is_trunc:
                non_trunc_out += int(r.get("completion_tokens") or 0)
                non_trunc_rtok += int(r.get("reasoning_tokens") or 0)
        else:
            u = r.get("usage") or {}
            rt_val = None
            if "thinking_tokens" in u and u["thinking_tokens"] is not None:
                rt_val = int(u["thinking_tokens"])
            elif "reasoning_tokens" in (u.get("completion_tokens_details") or {}):
                rt_val = int(u["completion_tokens_details"]["reasoning_tokens"] or 0)
            elif "thinking_tokens" in (u.get("output_tokens_details") or {}):
                rt_val = int(u["output_tokens_details"]["thinking_tokens"] or 0)
            if rt_val is not None:
                any_exposed = True
                if not is_trunc:
                    non_trunc_out += int(u.get("completion_tokens") or u.get("output_tokens") or 0)
                    non_trunc_rtok += rt_val

    if any_exposed and non_trunc_out > 0:
        reasoning_share: Optional[float] = non_trunc_rtok / non_trunc_out
        is_reasoning_model: Optional[bool] = (non_trunc_rtok > 0)
        avg_rtok: Optional[float] = non_trunc_rtok / max(1, n_total - n_trunc)
    else:
        reasoning_share = None
        is_reasoning_model = None
        avg_rtok = None

    all_out = sum(
        int(r.get("completion_tokens") or (r.get("usage") or {}).get("completion_tokens") or 0)
        for r in records
    )

    return {
        "n_calls": n_total,
        "n_cells": len(title_cells),
        "n_statements": n_stmt,
        "n_rendered": n_rendered,
        "n_truncated": n_trunc,
        "title_simpson_collision": round(simpson_mean, 4),
        "title_simpson_ci95": simpson_ci,
        "code_jaccard_obs": round(jaccard_obs, 4),
        "code_jaccard_excess": round(jaccard_excess, 4),
        "code_jaccard_excess_ci95": jaccard_excess_ci,
        "opens_with_negation_rate": round(neg_rate, 4),
        "opens_with_negation_ci95": neg_ci,
        "not_but_rate": round(not_but_rate, 4),
        "reasoning_overhead_ratio": round(reasoning_share, 4) if reasoning_share is not None else None,
        "is_reasoning_model": is_reasoning_model,
        "avg_reasoning_tokens": round(avg_rtok, 1) if avg_rtok is not None else None,
        "avg_output_tokens": round(all_out / max(1, n_total), 1),
        "validated_boat_hits": boat_hits if boat_denom > 0 else None,
        "validated_boat_denom": boat_denom if boat_denom > 0 else None,
    }


def _quantile(sorted_vals: List[float], q: float) -> float:
    if not sorted_vals:
        return 0.0
    pos = q * (len(sorted_vals) - 1)
    lo = int(math.floor(pos))
    hi = int(math.ceil(pos))
    if lo == hi:
        return sorted_vals[lo]
    return sorted_vals[lo] + (pos - lo) * (sorted_vals[hi] - sorted_vals[lo])


def _rank_desc(val: float, dist_vals: List[float]) -> Tuple[int, int]:
    """Return 1-based descending rank (#1 = highest value) among reference models."""
    higher = sum(1 for x in dist_vals if x > val + 1e-9)
    return higher + 1, len(dist_vals)


def load_target_records(target: Path) -> List[Dict[str, Any]]:
    if target.is_file() and target.suffix == ".jsonl":
        return [json.loads(ln) for ln in target.read_text(encoding="utf-8").splitlines() if ln.strip()]
    if target.is_dir():
        rows = []
        for p in sorted(target.rglob("record.json")):
            r = json.loads(p.read_text(encoding="utf-8"))
            sk = p.parent / "sketch.js"
            r["p5_code"] = sk.read_text(encoding="utf-8") if sk.exists() else (r.get("code") or "")
            r["render_ok"] = (p.parent / "painting.png").exists() and bool((r.get("render") or {}).get("ok", True))
            raw_p = p.parent / "raw_response.json"
            if raw_p.exists():
                try:
                    raw_obj = json.loads(raw_p.read_text(encoding="utf-8"))
                    msg_obj = (raw_obj.get("result") or {}).get("message") or raw_obj
                    u_obj = msg_obj.get("usage") or {}
                    otd_obj = u_obj.get("output_tokens_details") or u_obj.get("completion_tokens_details") or {}
                    if "thinking_tokens" in otd_obj and otd_obj["thinking_tokens"] is not None:
                        r["reasoning_tokens"] = int(otd_obj["thinking_tokens"])
                        r["completion_tokens"] = int(u_obj.get("output_tokens") or r.get("completion_tokens") or 0)
                except Exception:
                    pass
            rows.append(r)
        return rows
    raise FileNotFoundError(f"Cannot load records from {target}")


def select_cohort_slice(rows: List[Dict[str, Any]], explicit_topic: Optional[str] = None) -> Tuple[str, List[Dict[str, Any]], Dict[str, Any]]:
    if not COHORT_FILE.exists():
        return "unavailable", [], {}
    cohort_data = json.loads(COHORT_FILE.read_text(encoding="utf-8"))
    models = cohort_data.get("models", [])
    null_table = cohort_data.get("null_jaccard_baseline", {})

    topics = {r.get("chapter") or r.get("topic") for r in rows if (r.get("chapter") or r.get("topic"))}
    asks = {r.get("ask_type") for r in rows if r.get("ask_type")}

    if explicit_topic in ("death", "love"):
        sub = [{**m, "metrics": m["slices"][explicit_topic]} for m in models if explicit_topic in m.get("slices", {})]
        if sub:
            return f"{explicit_topic} ({len(sub)} verified models · full 30-call chapter)", sub, null_table

    # Default standardized comparison slice present across all 27 verified models: death_bare (15 runs)
    if topics == {"love"}:
        sub = [{**m, "metrics": m["slices"]["love"]} for m in models if "love" in m.get("slices", {})]
        return f"love ({len(sub)} verified models · 30-call chapter)", sub, null_table

    if topics == {"death"} and asks == {"essence", "bare"}:
        sub = [{**m, "metrics": m["slices"]["death"]} for m in models if "death" in m.get("slices", {})]
        return f"death ({len(sub)} verified models · 30-call chapter)", sub, null_table

    sub_db = [{**m, "metrics": m["slices"]["death_bare"]} for m in models if "death_bare" in m.get("slices", {})]
    return f"death_bare ({len(sub_db)} verified models · standardized 15-run trilingual slice)", sub_db, null_table


def _build_single_model_panel(ov: Dict[str, Any], ref_entries: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    specs = [
        ("title_simpson_collision", "title_simpson_ci95", "1. Title Collision Prob. (Simpson C)"),
        ("code_jaccard_excess", "code_jaccard_excess_ci95", "2. Excess Code Jaccard (J_obs − J_null)"),
        ("opens_with_negation_rate", "opens_with_negation_ci95", "3. Opening Negation Rate (κ=0.913)"),
        ("reasoning_overhead_ratio", None, "4. Reasoning Share (excl. truncations)"),
    ]
    panel = []
    for key, ci_key, label in specs:
        val = ov.get(key)
        ci = ov.get(ci_key) if ci_key else None
        if key == "reasoning_overhead_ratio":
            # Rank reasoning models exclusively against reasoning models
            if val is None:
                dist = []
                note = "NA (not exposed by API)"
            elif ov.get("is_reasoning_model"):
                dist = sorted(
                    e["metrics"][key] for e in ref_entries
                    if e["metrics"].get(key) is not None and e["metrics"].get("is_reasoning_model") is True
                )
                note = "reasoning sub-cohort"
            else:
                dist = []
                note = "0-thinking model"
        else:
            dist = sorted(e["metrics"][key] for e in ref_entries if e["metrics"].get(key) is not None)
            note = "27-model public cohort"

        if val is not None and dist:
            rk, n_rk = _rank_desc(val, dist)
            med = round(_quantile(dist, 0.50), 4)
            iqr = [round(_quantile(dist, 0.25), 4), round(_quantile(dist, 0.75), 4)]
        else:
            rk, n_rk, med, iqr = None, len(dist), None, None

        panel.append({
            "key": key,
            "label": label,
            "value": val,
            "ci95": ci,
            "rank_desc": f"#{rk}/{n_rk}" if rk is not None else None,
            "cohort_n": n_rk,
            "cohort_median": med,
            "cohort_iqr": iqr,
            "note": note,
        })
    return panel


def build_diagnostic_payload(target: Path, topic: Optional[str] = None) -> Dict[str, Any]:
    raw_rows = load_target_records(target)
    unverified_rows = [r for r in raw_rows if r.get("identity_verified") is False]
    rows = [r for r in raw_rows if r.get("identity_verified") is not False] or raw_rows

    slice_label, ref_entries, null_table = select_cohort_slice(rows, topic)

    by_m: Dict[str, List[Dict[str, Any]]] = collections.defaultdict(list)
    for r in rows:
        by_m[r.get("model_condition") or r.get("model_requested") or r.get("lab") or "model"].append(r)

    is_multi_model = len(by_m) >= 2
    # Align target rows to death_bare when comparing against death_bare slice on multi-topic archives
    overall = compute_four_metrics(rows, null_table=null_table)

    per_model = {}
    twins = []
    if is_multi_model:
        panel = []  # Do not rank a heterogeneous multi-model pool against single-model references
        for m_id, m_rows in sorted(by_m.items()):
            # Match slice if comparing against death_bare
            eval_rows = (
                [r for r in m_rows if (r.get("chapter") or r.get("topic")) == "death" and r.get("ask_type") == "bare"]
                if slice_label.startswith("death_bare") and any((r.get("chapter") or r.get("topic")) == "death" and r.get("ask_type") == "bare" for r in m_rows)
                else m_rows
            )
            st = compute_four_metrics(eval_rows, null_table=null_table)
            st_panel = _build_single_model_panel(st, ref_entries)
            st["ranks"] = {p["key"]: p["rank_desc"] for p in st_panel}
            per_model[m_id] = st
    else:
        eval_rows = (
            [r for r in rows if (r.get("chapter") or r.get("topic")) == "death" and r.get("ask_type") == "bare"]
            if slice_label.startswith("death_bare") and any((r.get("chapter") or r.get("topic")) == "death" and r.get("ask_type") == "bare" for r in rows)
            else rows
        )
        overall = compute_four_metrics(eval_rows, null_table=null_table)
        panel = _build_single_model_panel(overall, ref_entries)
        if ref_entries:
            keys3 = ("title_simpson_collision", "code_jaccard_excess", "opens_with_negation_rate")
            scales = {}
            for k in keys3:
                vs = sorted(e["metrics"][k] for e in ref_entries if e["metrics"].get(k) is not None)
                scales[k] = max(0.04, _quantile(vs, 0.75) - _quantile(vs, 0.25)) if vs else 0.15
            dists = []
            for e in ref_entries:
                d2 = sum(((overall[k] - e["metrics"][k]) / scales[k]) ** 2 for k in keys3)
                dists.append((math.sqrt(d2), e["model"], e["era"], e["metrics"]))
            dists.sort(key=lambda x: x[0])
            for dist_v, m_name, m_era, m_met in [x for x in dists if x[0] > 1e-6][:3]:
                twins.append({
                    "model": m_name,
                    "era": m_era,
                    "distance": round(dist_v, 3),
                    "title_simpson_collision": m_met["title_simpson_collision"],
                    "code_jaccard_excess": m_met["code_jaccard_excess"],
                    "opens_with_negation_rate": m_met["opens_with_negation_rate"],
                })

    return {
        "version": "1.1.2",
        "target": str(target),
        "is_multi_model": is_multi_model,
        "excluded_unverified_rows": len(unverified_rows),
        "reference_slice": slice_label,
        "overall": overall,
        "single_model_panel": panel,
        "nearest_twins": twins,
        "per_model": per_model,
    }


def generate_report(target: Path, topic: Optional[str] = None, as_json: bool = False) -> str:
    payload = build_diagnostic_payload(target, topic=topic)
    if as_json:
        return json.dumps(payload, ensure_ascii=False, indent=2)

    raw_rows = load_target_records(target)
    rows = [r for r in raw_rows if r.get("identity_verified") is not False] or raw_rows
    ov = payload["overall"]

    valid = [
        r for r in rows
        if (r.get("statement_counted") is True)
        or ("statement_counted" not in r and bool((r.get("statement") or "").strip()) and not r.get("truncated"))
    ]
    # P1-13 fix: only report frozen Protocol v1.0 `neg` when actual non-empty `death_families` annotations exist
    has_frozen_coding = any(bool(r.get("death_families")) for r in valid if r.get("chapter") == "death")
    frozen_neg_cnt = sum(1 for r in valid if "neg" in (r.get("death_families") or [])) if has_frozen_coding else None

    lines = [
        "# Still Ours? — Quantitative Behavioral & Stylometry Report (`v1.1.2`)",
        "",
        f"- **Target**: `{target}`",
        f"- **Verified Sample**: `{len(rows)}` calls · `{len(valid)}` statements · `{sum(1 for r in rows if r.get('painting_counted', r.get('render_ok', False)))}/{len(rows)}` rendered canvases · `{sum(1 for r in rows if r.get('truncated') or r.get('finish_reason')=='length')}` token-cap truncations"
        + (f" *(excluded `{payload['excluded_unverified_rows']}` unverified alias rows)*" if payload["excluded_unverified_rows"] else ""),
        f"- **Reference Cohort**: `{payload['reference_slice']}` (public Death & Love archive, Bitcoin OTS anchored)",
        "",
    ]

    if not payload["is_multi_model"]:
        lines.extend([
            "## 1. Four-Metric Diagnostic Panel (Single-Model Comparison)",
            "",
            "| Metric | Estimate `[95% Bootstrap CI]` | Rank in Cohort | Cohort Median `[IQR]` | Scope Note |",
            "| :--- | :---: | :---: | :---: | :--- |",
        ])
        for item in payload["single_model_panel"]:
            val = item["value"]
            if val is None:
                v_str = "`NA`"
            else:
                sign = "+" if (item["key"] == "code_jaccard_excess" and val >= 0) else ""
                v_str = f"**{sign}{val * 100:.1f}%**"
                if item["ci95"]:
                    v_str += f" `[{item['ci95'][0]*100:.1f}%, {item['ci95'][1]*100:.1f}%]`"
            rk_str = f"`{item['rank_desc']}`" if item["rank_desc"] else "—"
            if item["cohort_median"] is not None and item["cohort_iqr"]:
                med_str = f"{item['cohort_median']*100:.1f}% `[{item['cohort_iqr'][0]*100:.1f}%–{item['cohort_iqr'][1]*100:.1f}%]`"
            else:
                med_str = "—"
            lines.append(f"| {item['label']} | {v_str} | {rk_str} | {med_str} | {item['note']} |")
        lines.append("")
        if ov.get("validated_boat_denom"):
            lines.append(
                f"- **Validated lexical-code indicator (`Boat / Crossing`, Death P=1.00 / R=1.00 on OpenAI bare)**: "
                f"`{ov['validated_boat_hits']}/{ov['validated_boat_denom']}` (`{100.0*ov['validated_boat_hits']/ov['validated_boat_denom']:.1f}%`); "
                f"raw non-builtin identifier Jaccard `J_obs = {ov['code_jaccard_obs']*100:.1f}%`; "
                f"`not X, but Y` rate `= {ov['not_but_rate']*100:.1f}%`."
            )
            lines.append("")
        if payload["nearest_twins"]:
            lines.append("### Nearest Models in 27-Model Reference Space")
            for tw in payload["nearest_twins"]:
                lines.append(
                    f"- **`{tw['model']}`** ({tw['era']}, dist `{tw['distance']:.2f}`) — "
                    f"Simpson collision `{tw['title_simpson_collision']*100:.1f}%` · "
                    f"excess Jaccard `{tw['code_jaccard_excess']*100:+.1f}%` · "
                    f"opening negation `{tw['opens_with_negation_rate']*100:.1f}%`"
                )
            lines.append("")
    else:
        lines.extend([
            "## 1. Per-Model Diagnostic Breakdown (Ranked Individually Against Single-Model Cohort)",
            "",
            "*(Multi-model target detected: models are evaluated individually on homogeneous cells rather than pooled.)*",
            "",
            "| Model | Rendered | 1. Title Simpson C (Rank) | 2. Excess Jaccard ΔJ (Rank) | 3. Opening Negation (Rank) | 4. Reasoning Share | Boat Hits (Death) |",
            "| :--- | :---: | :---: | :---: | :---: | :---: | :---: |",
        ])
        for m_id, st in payload["per_model"].items():
            rks = st.get("ranks", {})
            c_str = f"{st['title_simpson_collision']*100:.1f}% ({rks.get('title_simpson_collision') or '—'})"
            j_str = f"{st['code_jaccard_excess']*100:+.1f}% ({rks.get('code_jaccard_excess') or '—'})"
            n_str = f"{st['opens_with_negation_rate']*100:.1f}% ({rks.get('opens_with_negation_rate') or '—'})"
            if st["reasoning_overhead_ratio"] is None:
                rt_str = "`NA`"
            elif st["is_reasoning_model"]:
                rt_str = f"{st['reasoning_overhead_ratio']*100:.1f}% ({rks.get('reasoning_overhead_ratio') or '—'})"
            else:
                rt_str = "0% (0-think)"
            b_str = f"{st['validated_boat_hits']}/{st['validated_boat_denom']}" if st.get("validated_boat_denom") else "—"
            lines.append(f"| `{m_id}` | {st['n_rendered']}/{st['n_calls']} | {c_str} | {j_str} | {n_str} | {rt_str} | {b_str} |")
        lines.append("")

    if has_frozen_coding and frozen_neg_cnt is not None:
        death_valid = [r for r in valid if r.get("chapter") == "death"]
        lines.append(
            f"*(Protocol v1.0 frozen `neg` coding on contemporary Death: `{frozen_neg_cnt}/{len(death_valid)}` = "
            f"`{100.0 * frozen_neg_cnt / max(1, len(death_valid)):.1f}%`; automated opening-negation regex agreement = `95.9%`, κ = `0.913`.)*"
        )
        lines.append("")

    return "\n".join(lines)
