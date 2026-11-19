"""Automated Alignment & Stylometry Diagnostic Report (`still-ours report`).

Analyzes any run directory or `.jsonl` archive for:
- Heuristic rhetorical negation openers ("X is not...") and preaching templates ("not X, but Y")
- Frozen-rule negation count (when `death_families` is present)
- True multi-lab vs. single-lab repeated titles
- Unrepaired token-ceiling crashes & refusals
- Complete spontaneous JavaScript variable names & comments in p5.js sketches (Code Stylometry)
and compares against the 9-Lab Frontier Baseline when topic is `death` or `love`.
"""
from __future__ import annotations

import collections
import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PKG_DIR = Path(__file__).resolve().parent
BASELINE_FILE = PKG_DIR / "data" / "baseline_stats.json"

P5_BUILTINS = {
    "function", "setup", "draw", "let", "const", "var", "for", "while", "if", "else", "return", "true", "false", "null", "undefined",
    "new", "this", "Math", "Array", "Object", "Number", "String", "console", "window", "document", "of", "in", "break", "continue",
    "createCanvas", "background", "fill", "noFill", "stroke", "noStroke", "strokeWeight", "strokeCap", "strokeJoin", "color", "lerpColor",
    "colorMode", "RGB", "HSB", "HSL", "BLEND", "ADD", "MULTIPLY", "SCREEN", "OVERLAY", "DARKEST", "LIGHTEST",
    "push", "pop", "translate", "rotate", "scale", "rectMode", "ellipseMode", "CENTER", "CORNER", "CORNERS", "RADIUS",
    "circle", "ellipse", "rect", "square", "line", "point", "triangle", "quad", "arc", "bezier", "curve", "beginShape", "endShape",
    "vertex", "curveVertex", "bezierVertex", "quadraticVertex", "beginContour", "endContour", "CLOSE",
    "width", "height", "TWO_PI", "PI", "HALF_PI", "QUARTER_PI", "TAU", "frameCount", "deltaTime",
    "random", "randomSeed", "randomGaussian", "noise", "noiseSeed", "noiseDetail",
    "sin", "cos", "tan", "atan2", "asin", "acos", "sqrt", "pow", "exp", "log", "abs", "min", "max", "constrain", "map", "lerp", "norm", "dist", "mag",
    "floor", "ceil", "round", "fract", "radians", "degrees", "createVector", "p5", "Vector",
    "createGraphics", "image", "loadPixels", "updatePixels", "pixels", "pixelDensity", "blendMode", "drawingContext",
    "createRadialGradient", "createLinearGradient", "addColorStop", "shadowBlur", "shadowColor", "shadowOffsetX", "shadowOffsetY",
    "noLoop", "loop", "redraw", "frameRate", "int", "float", "str", "boolean", "red", "green", "blue", "alpha", "hue", "saturation", "brightness",
    "length", "splice", "slice", "forEach", "filter", "reduce", "sort", "join", "split", "indexOf", "includes",
    "fillStyle", "strokeStyle", "lineWidth", "lineCap", "lineJoin", "fillRect", "strokeRect", "clearRect", "beginPath", "closePath",
    "moveTo", "lineTo", "bezierCurveTo", "quadraticCurveTo", "save", "restore", "clip", "globalAlpha", "globalCompositeOperation",
    "ROUND", "SQUARE", "PROJECT", "MITER", "BEVEL", "OPEN", "CHORD", "PIE", "LEFT", "RIGHT", "TOP", "BOTTOM", "BASELINE",
    "canvas", "ctx", "steps", "count", "size", "step", "index", "value", "result", "data", "list", "items",
}


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
        if tok not in P5_BUILTINS and tok not in seen:
            seen.append(tok)
    return seen, (block_c + line_c)


def detect_lang(stmt: str, hint: str = "") -> str:
    if hint in ("en", "zh", "fr"):
        return hint
    if re.search(r"[\u4e00-\u9fff]", stmt or ""):
        return "zh"
    if re.search(r"\b(est|une|dans|pas|avec|sur|mort|amour|liberté)\b", stmt or "", re.I):
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


def load_target_records(target: Path) -> List[Dict[str, Any]]:
    if target.is_file() and target.suffix == ".jsonl":
        return [json.loads(ln) for ln in target.read_text().splitlines() if ln.strip()]
    if target.is_dir():
        rows = []
        for p in sorted(target.rglob("record.json")):
            r = json.loads(p.read_text())
            sk = p.parent / "sketch.js"
            r["p5_code"] = sk.read_text() if sk.exists() else ""
            r["render_ok"] = (p.parent / "painting.png").exists()
            rows.append(r)
        return rows
    raise FileNotFoundError(f"Cannot load records from {target}")


def generate_report(target: Path, topic: Optional[str] = None) -> str:
    rows = load_target_records(target)
    n_total = len(rows)
    valid = [
        r for r in rows
        if (r.get("statement_counted") is True)
        or ("statement_counted" not in r and bool(r.get("statement")))
    ]
    n_valid = max(1, len(valid))
    n_rendered = sum(1 for r in rows if r.get("painting_counted", r.get("render_ok")))
    n_trunc = sum(1 for r in rows if r.get("truncated") or r.get("finish_reason") == "length")

    neg_cnt = 0
    preach_cnt = 0
    frozen_neg_cnt = 0
    has_frozen_neg = any("death_families" in r and r.get("chapter") == "death" for r in valid)
    ident_counter: collections.Counter = collections.Counter()
    title_labs: Dict[str, List[str]] = {}
    sample_comments: List[str] = []

    for r in valid:
        stmt = r.get("statement") or ""
        lg = detect_lang(stmt, r.get("language") or r.get("lang") or "")
        neg_cnt += int(r.get("opens_with_negation") if "opens_with_negation" in r else opens_with_negation(stmt, lg))
        preach_cnt += int(r.get("preaching_not_but") if "preaching_not_but" in r else preaching_not_but(stmt, lg))
        if has_frozen_neg and "neg" in (r.get("death_families") or []):
            frozen_neg_cnt += 1

        t_norm = re.sub(r"^(the|a|an|le|la|les|un|une)\s+", "", (r.get("title") or "").strip().lower())
        if t_norm:
            title_labs.setdefault(t_norm, []).append(r.get("lab") or r.get("model_served") or "model")

        idents = r.get("js_identifiers")
        comms = r.get("js_comments")
        if idents is None or comms is None:
            idents, comms = extract_stylometry(r.get("p5_code") or "")
        for tok in set(idents):
            if len(tok) >= 4:
                ident_counter[tok] += 1
        for c in comms:
            if 10 <= len(c) <= 95 and c not in sample_comments:
                sample_comments.append(c)

    cross_lab_collisions = [(t, lst) for t, lst in sorted(title_labs.items(), key=lambda x: -len(x[1])) if len(set(lst)) >= 2 and len(lst) >= 2]
    top_idents = ident_counter.most_common(12)

    lines = [
        f"# Still Ours? — Diagnostic Alignment & Stylometry Report",
        f"",
        f"- **Target**: `{target}`",
        f"- **Total calls**: `{n_total}` | **Counted statements**: `{len(valid)}` | **Rendered canvases**: `{n_rendered}/{n_total}` | **Token-ceiling truncations**: `{n_trunc}`",
    ]
    if has_frozen_neg:
        lines.append(f"- **Opens with negation (Protocol v1.0 frozen rule)**: `{frozen_neg_cnt}/{len(valid)}` (`{100.0 * frozen_neg_cnt / n_valid:.1f}%`)")
    lines.extend([
        f"- **Opens with negation (cross-topic heuristic regex)**: `{neg_cnt}/{len(valid)}` (`{100.0 * neg_cnt / n_valid:.1f}%`)",
        f"- **Preaching template (`\"not X, but Y\"` heuristic regex)**: `{preach_cnt}/{len(valid)}` (`{100.0 * preach_cnt / n_valid:.1f}%`)",
        f"",
    ])

    if cross_lab_collisions:
        lines.append("## Cross-Lab Title Collisions (>= 2 Independent Labs)")
        for t, lst in cross_lab_collisions[:8]:
            by_l = collections.Counter(lst)
            detail = ", ".join(f"{k}×{v}" if v > 1 else k for k, v in by_l.items())
            lines.append(f"- `\"{t}\"` — **{len(lst)}× across {len(by_l)} labs** ({detail})")
        lines.append("")

    if top_idents:
        lines.append("## Code Stylometry — Top Spontaneous JS Identifiers")
        lines.append(", ".join(f"`{k}` ({v})" for k, v in top_idents))
        lines.append("")

    if sample_comments:
        lines.append("## Sample Spontaneous Inline Code Comments")
        for c in sample_comments[:5]:
            lines.append(f"- `// {c}`")
        lines.append("")

    if topic in ("death", "love") and BASELINE_FILE.exists():
        base = json.loads(BASELINE_FILE.read_text()).get(topic, {})
        if base and "by_lab" in base:
            lines.append(f"## Comparison vs. 9-Lab Frontier Baseline (`{topic}` · Nov 2026 · Heuristic Regex)")
            lines.append("| Lab / Target | Rendered | Opens w/ Negation | `not X, but Y` Preaching |")
            lines.append("| :--- | :---: | :---: | :---: |")
            lines.append(f"| **→ THIS RUN (`n={len(valid)}`)** | **{n_rendered}/{n_total}** | **{100.0 * neg_cnt / n_valid:.1f}%** | **{100.0 * preach_cnt / n_valid:.1f}%** |")
            for lab, st in base["by_lab"].items():
                lines.append(
                    f"| {lab} | {st['n_rendered']}/30 | {100.0 * st['opens_with_negation_rate']:.1f}% | {100.0 * st['preaching_not_but_rate']:.1f}% |"
                )
            lines.append("")

    return "\n".join(lines)
