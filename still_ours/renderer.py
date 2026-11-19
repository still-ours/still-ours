"""Deterministic AI-free p5.js 1.11.13 renderer and contact-sheet builder."""
from __future__ import annotations

import base64
import hashlib
import html
import json
import os
import re
import shutil
from pathlib import Path
from typing import Any, Dict, List

from . import P5_VERSION

PKG_DIR = Path(__file__).resolve().parent
P5_VENDOR = PKG_DIR / "vendor" / "p5-1.11.13.min.js"

SECTION = re.compile(r"^\s*(?:\*\*|#+\s*)?(TITLE|STYLE|STATEMENT|CODE)\s*(?:\*\*)?\s*[:：]\s*(?:\*\*)?", re.I | re.M)

PAGE_TEMPLATE = """<!doctype html><html><head><meta charset="utf-8">
<style>html,body{{margin:0;padding:0;background:#ffffff;overflow:hidden}}</style>
<script>window.__errors=[];window.addEventListener('error',function(e){{window.__errors.push(String(e.message||e))}});</script>
<script src="{p5}"></script></head><body>
<script>
{code}
</script></body></html>"""


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def parse_reply(text: str) -> Dict[str, Any]:
    out: Dict[str, Any] = {"title": "", "style": "", "statement": "", "code": ""}
    marks = list(SECTION.finditer(text or ""))
    for i, mk in enumerate(marks):
        end = marks[i + 1].start() if i + 1 < len(marks) else len(text)
        out[mk.group(1).lower()] = text[mk.end():end].strip()
    code_src = out["code"] or text or ""
    fence = re.findall(r"```(?:javascript|js|p5|p5js)?\s*\n(.*?)```", code_src, re.S | re.I)
    if fence:
        out["code"] = max(fence, key=len).strip()
    elif not re.search(r"function\s+setup\s*\(", out["code"]):
        fence_all = re.findall(r"```(?:javascript|js|p5|p5js)?\s*\n(.*?)```", text or "", re.S | re.I)
        out["code"] = max(fence_all, key=len).strip() if fence_all else ""
    out["wrapped_in_html"] = False
    if re.search(r"<script", out["code"], re.I):
        inline = re.findall(r"<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>", out["code"], re.S | re.I)
        if inline:
            out["code"] = "\n".join(x.strip() for x in inline if x.strip())
            out["wrapped_in_html"] = True
    for k in ("title", "style", "statement"):
        out[k] = out[k].strip().strip("*_").strip().strip('"').strip("*_").strip()
    return out


def render_one(browser, html_path: Path, png_path: Path, width: int = 1600, height: int = 2000, settle_ms: int = 4000, timeout_ms: int = 30000) -> Dict[str, Any]:
    ctx = browser.new_context(viewport={"width": width, "height": height}, device_scale_factor=1)
    page = ctx.new_page()
    console: List[str] = []
    page.on("console", lambda m: console.append(f"{m.type}: {m.text}") if m.type in ("error", "warning") else None)
    page.on("pageerror", lambda e: console.append(f"pageerror: {e}"))
    info: Dict[str, Any] = {"ok": False, "canvas": None, "errors": [], "settle_ms": settle_ms}
    try:
        page.goto(html_path.resolve().as_uri(), wait_until="load", timeout=timeout_ms)
        page.wait_for_timeout(settle_ms)
        page.evaluate("() => { try { window.__looping = (typeof isLooping === 'function') ? isLooping() : null; if (typeof noLoop === 'function') noLoop(); } catch (e) {} }")
        data = page.evaluate("""() => {
            const cs = Array.from(document.querySelectorAll('canvas'));
            if (!cs.length) return null;
            const c = cs.sort((a,b) => b.width*b.height - a.width*a.height)[0];
            return {w: c.width, h: c.height, url: c.toDataURL('image/png')};
        }""")
        info["errors"] = page.evaluate("() => window.__errors || []")
        info["was_looping"] = page.evaluate("() => { try { return window.__looping === true; } catch (e) { return null; } }")
        if data:
            png_path.write_bytes(base64.b64decode(data["url"].split(",", 1)[1]))
            info["canvas"] = [data["w"], data["h"]]
            info["ok"] = True
    except Exception as e:
        info["errors"].append(f"renderer: {str(e).splitlines()[0][:300]}")
    finally:
        info["console"] = console[:40]
        for c in console:
            if c.startswith("pageerror:") and c[10:].strip() not in info["errors"]:
                info["errors"].append(c[10:].strip())
        try:
            ctx.close()
        except Exception:
            pass
    return info


def _launch_browser(pw):
    try:
        return pw.chromium.launch()
    except Exception:
        for ch in ("chrome", "msedge"):
            try:
                return pw.chromium.launch(channel=ch)
            except Exception:
                pass
        mac_chrome = Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
        if mac_chrome.exists():
            return pw.chromium.launch(executable_path=str(mac_chrome))
        raise


def render_run_dir(run_dir: Path, records: List[Dict[str, Any]], width: int = 1600, height: int = 2000, settle_ms: int = 4000) -> None:
    from playwright.sync_api import sync_playwright

    shutil.copy(P5_VENDOR, run_dir / "p5.min.js")
    with sync_playwright() as pw:
        browser = _launch_browser(pw)
        for rec in records:
            d = run_dir / rec["dir"]
            sk = d / "sketch.js"
            if not sk.exists():
                rec["render"] = {"ok": False, "errors": ["no code returned"]}
                continue
            page_path = d / "painting.html"
            rel_p5 = os.path.relpath(run_dir / "p5.min.js", d)
            page_path.write_text(PAGE_TEMPLATE.format(p5=rel_p5, code=sk.read_text()))
            info = render_one(browser, page_path, d / "painting.png", width=width, height=height, settle_ms=settle_ms)
            if info["ok"] and info["errors"]:
                info["note"] = "drawn, but code raised runtime errors (archived unrepaired)"
            rec["render"] = info
            if not info["ok"] and rec.get("status") == "ok":
                rec["status"] = "render_failed"
            (d / "record.json").write_text(json.dumps(rec, ensure_ascii=False, indent=2))
            print(f"  render [{rec.get('model_served') or rec.get('model_requested')}] {rec.get('lang','')}/{rec.get('ask_type','')} r{rec['run']}: {'ok' if info['ok'] else 'FAILED'}")
        browser.close()


def build_contact_sheet_and_gallery(run_dir: Path, records: List[Dict[str, Any]], manifest: Dict[str, Any]) -> Path:
    from playwright.sync_api import sync_playwright

    esc = html.escape
    cols = min(5, max(3, len(records))) if len(records) != 9 else 3
    tiles = []
    for r in records:
        d = run_dir / r["dir"]
        png = d / "painting.png"
        if png.exists():
            media = f'<img src="{esc(r["dir"])}/painting.png" loading="lazy" alt="">'
        else:
            media = f'<div class="void"><span>{esc(r.get("status", "failed"))}</span></div>'
        tag = " · ".join(x for x in [r.get("lab") or r.get("model_served") or r.get("model_requested"), r.get("lang", "").upper(), r.get("ask_type", "")] if x)
        stmt = esc(r.get("statement") or "")
        tiles.append(f"""<figure class="tile">{media}
<figcaption><div class="t">{esc(r.get('title') or 'Untitled')}</div>
<div class="m">{esc(tag)} · run {r.get('run', 1)}</div>
{f'<p>{stmt}</p>' if stmt else ''}</figcaption></figure>""")

    css = f"""
:root{{--wall:#0f0e0c;--ink:#ece6dc;--soft:#9e9689;--line:rgba(236,230,220,.14)}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--wall);color:var(--ink);font-family:Georgia,'Iowan Old Style',serif}}
header{{padding:40px 44px 18px;max-width:1600px;margin:auto}}
h1{{font-weight:400;font-size:32px;margin:0 0 6px;letter-spacing:.02em}}
.sub{{color:var(--soft);font:13px/1.6 ui-monospace,Menlo,monospace}}
.grid{{display:grid;grid-template-columns:repeat({cols},1fr);gap:28px 24px;padding:20px 44px 48px;max-width:1600px;margin:auto}}
.tile{{margin:0}}.tile img,.void{{width:100%;aspect-ratio:4/5;display:block;background:#050505;border:1px solid var(--line)}}
.void{{display:flex;align-items:center;justify-content:center;color:var(--soft);font:13px ui-monospace,monospace;text-align:center;padding:20px}}
figcaption{{padding-top:10px}}.t{{font-size:16px;color:var(--ink)}}.m{{font:11.5px/1.5 ui-monospace,Menlo,monospace;color:#d6a76c;margin-top:3px}}
figcaption p{{font-size:13px;line-height:1.5;color:var(--soft);margin:6px 0 0}}
"""
    doc = f"""<!doctype html><html><head><meta charset="utf-8"><title>{esc(manifest.get('title', 'Still Ours? Probe'))}</title><style>{css}</style></head>
<body><header><h1>{esc(manifest.get('title', 'Still Ours? — Diagnostic Probe'))}</h1>
<div class="sub">Renderer: deterministic p5.js {P5_VERSION} (AI-free, randomSeed(1), 1600×2000) · {esc(manifest.get('started_utc','')[:19])} UTC · n={len(records)}</div></header>
<div class="grid">{''.join(tiles)}</div></body></html>"""
    gal = run_dir / "gallery.html"
    gal.write_text(doc)

    poster_html = run_dir / "_poster.html"
    poster_html.write_text(doc)
    sheet_jpg = run_dir / "contact_sheet.jpg"
    with sync_playwright() as pw:
        b = _launch_browser(pw)
        p = b.new_page(viewport={"width": 1560, "height": 1100}, device_scale_factor=1.5)
        p.goto(poster_html.resolve().as_uri(), wait_until="load")
        p.wait_for_timeout(400)
        p.evaluate("() => { document.querySelectorAll('figcaption p').forEach(x => x.remove()); }")
        p.query_selector("body").screenshot(path=str(sheet_jpg), type="jpeg", quality=88)
        b.close()
    poster_html.unlink(missing_ok=True)
    return sheet_jpg
