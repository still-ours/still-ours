#!/usr/bin/env python3
"""Builds the experiment protocol archive for In the Machine's Mind · Death.
Re-run any time new data is added: python3 archive/build_archive.py
Everything here is derived from the run folders; nothing is typed by hand except the coding rules below."""
import json, glob, re, os, csv, hashlib, ast, datetime, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from zh_rules import FAM_ZH, ABS_ZH, affirmed_zh
from fr_rules import FAM_FR, ABS_FR, HOSTILE_FR, affirmed_fr, family_matches_fr
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'archive')
RUNS = [  # (folder, ask id, description)
    ('runs/2026-10-30_1643_death-open-control', 'ask1', 'Make a painting about Death — not any particular death, but what death itself is, as you understand it.'),
    ('runs/2026-10-30_2118_death-plain-prompt', 'ask2', 'Make a painting about death.'),
]
EXTRA = sorted(glob.glob(os.path.join(ROOT, 'runs/*_death-zh-*')))  # Chinese-prompt runs, added later
for f in EXTRA:
    RUNS.append((os.path.relpath(f, ROOT), 'zh-' + f.rsplit('death-zh-', 1)[1], '(Chinese prompt, see prompt.txt in folder)'))
FR_EXTRA = sorted(glob.glob(os.path.join(ROOT, 'runs/*_death-fr-*')))
for f in FR_EXTRA:
    RUNS.append((os.path.relpath(f, ROOT), 'fr-' + f.rsplit('death-fr-', 1)[1], '(French prompt, see prompt.txt in folder)'))

def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as fh:
        for b in iter(lambda: fh.read(1 << 20), b''): h.update(b)
    return h.hexdigest()

# ---------------- coding rules (identical to the exhibit page) ----------------
def affirmed(pat):
    """True if the statement uses the idea affirmatively at least once.
    A use is denied when an earlier 'not/no/nor' in the same sentence is not undone by a later 'but', 'only', 'instead' or 'rather'
    ('Death is not a door' = denied; 'not a wall but a door' = affirmed)."""
    def t(s):
        for m in re.finditer(pat, s, re.I):
            start = max(s.rfind('.', 0, m.start()), s.rfind('!', 0, m.start()), s.rfind('?', 0, m.start()), s.rfind(';', 0, m.start())) + 1
            pre = s[start:m.start()]
            negs = list(re.finditer(r"\b(not|no|nor|never|without)\b", pre, re.I))
            if not negs or re.search(r"\b(but|only|instead|rather)\b", pre[negs[-1].end():], re.I): return m
        return None
    return t
FAM = [
 ('neg',    'Opens by saying what death is not', '一开口，先说死亡“不是”什么', lambda s: re.search(r"^[^.]*?\b(is not|isn[’']t|has no|not an?)\b", s, re.I)),
 ('loose',  'Death as loosening, untying, letting go', '死亡是松开、解开、放手', affirmed(r"unbind\w*|loosen\w*|\bunti(e|es|ed|ing)\b|untying|unweav\w*|unravel\w*|unwind\w*|undone|unclasp\w*|\blets? go\b|letting go|releas\w*|relinquish\w*|unspool\w*")),
 ('lost',   'Nothing is destroyed or lost', '没有什么被摧毁、真正失去', lambda s: re.search(r"nothing[^.]{0,30}(destroy|lost|thrown|annihilat|erase|taken)|not destroyed|nothing leaves|not into nothing|nothing is truly lost", s, re.I)),
 ('back',   'Returning to the whole it came from', '回到它来自的整体', affirmed(r"\b(back|return\w*|rejoin\w*)\b[^.]{0,12}\b(in)?to\b|the whole\b(?!\s+\w)|indistinguishable|indivisible|can no longer be (told|distinguished)")),
 ('borrow', 'Life as something borrowed', '生命是“借来的”', affirmed(r"borrow\w*")),
 ('door',   'A threshold, a door, a passage', '一道门槛、一扇门、一条通道', affirmed(r"threshold|\bdoors?\b|doorway|\bpassages?\b")),
 ('grief',  'The loss is real, and deserves grief', '失去是真的，值得哀悼', lambda s: re.search(r"grief|loss is real", s, re.I)),
]
ABSENT = [('fear','恐惧',r"\b(fear\w*|afraid|terror|dread)\b"),('soul','灵魂',r"\bsouls?\b"),('afterlife','来世',r"afterlife|heaven|hell\b|paradise"),
          ('rebirth','轮回',r"rebirth|reincarnat|resurrect"),('judgement','审判',r"judg"),('God','神',r"\bgods?\b|divine"),('ancestors','祖先',r"ancestor")]
HOSTILE = r"\b(enem\w*|violen\w*|cruel\w*|terrib\w*|evil|horr\w*|monster\w*)\b"

def usage_of(r):
    u = r.get('usage')
    if isinstance(u, str):
        try: u = ast.literal_eval(u)
        except Exception: u = {}
    return u or {}

rows = []
for folder, ask, prompt in RUNS:
    base = os.path.join(ROOT, folder)
    if not os.path.isdir(base): continue
    for p in sorted(glob.glob(os.path.join(base, '*/run*/record.json'))):
        r = json.load(open(p)); d = os.path.dirname(p); run_dir = os.path.basename(d)
        u = usage_of(r); rend = r.get('render') if isinstance(r.get('render'), dict) else {}
        counted = bool(re.fullmatch(r'run\d+', run_dir)) and r.get('status') == 'ok'
        stmt = r.get('statement') or ''
        row = dict(ask=ask, folder=folder, slot=int(r['slot']), lab=r['lab'], run_dir=run_dir, counted=counted,
                   status=r.get('status'), model_requested=r.get('model_requested'), model_served=r.get('model_served'),
                   provider=r.get('provider'), started_utc=r.get('started_utc'), finished_utc=r.get('finished_utc'),
                   http_status=r.get('http_status'), finish_reason=r.get('finish_reason'), truncated=r.get('truncated'),
                   prompt_tokens=u.get('prompt_tokens'), completion_tokens=u.get('completion_tokens'),
                   reasoning_tokens=(u.get('completion_tokens_details') or {}).get('reasoning_tokens'), cost_usd=u.get('cost'),
                   generation_id=r.get('generation_id'), title=r.get('title'), statement=stmt,
                   statement_words=len(stmt.split()), statement_chars=len(stmt),
                   render_ok=rend.get('ok'), render_errors='; '.join(map(str, rend.get('errors') or [])),
                   code_sha256=sha(os.path.join(d, 'sketch.js')) if os.path.exists(os.path.join(d, 'sketch.js')) else '',
                   image_sha256=sha(os.path.join(d, 'painting.png')) if os.path.exists(os.path.join(d, 'painting.png')) else '')
        for fid, en, zh, t in FAM:
            tt = FAM_ZH[fid] if ask.startswith('zh') else FAM_FR[fid] if ask.startswith('fr') else t
            m = tt(stmt); row['f_' + fid] = int(bool(m)); row['m_' + fid] = m.group(0) if m else ''
            row['m_all_' + fid] = json.dumps(family_matches_fr(fid, stmt), ensure_ascii=False) if ask.startswith('fr') else ''
        rows.append(row)

with open(os.path.join(OUT, 'records.csv'), 'w', newline='', encoding='utf-8') as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
json.dump(rows, open(os.path.join(OUT, 'records.json'), 'w'), ensure_ascii=False, indent=1)

# ---------------- statistics ----------------
asks = sorted({r['ask'] for r in rows})
C = {a: [r for r in rows if r['ask'] == a and r['counted']] for a in asks}
EN = [r for a in ('ask1', 'ask2') for r in C.get(a, [])]
stats = {'generated_utc': datetime.datetime.utcnow().replace(microsecond=0).isoformat() + 'Z', 'counted_answers': {a: len(C[a]) for a in asks}, 'families': {}, 'absent': {}, 'hostile': {}, 'titles': {}}
for fid, en, zh, t in FAM:
    stats['families'][fid] = {'label_en': en, 'label_zh': zh, **{a: sum(r['f_' + fid] for r in C[a]) for a in asks}}
for k, zh, pat in ABSENT:
    e = {'label_zh': zh}
    for a in asks:
        rs = C[a]; zp = ABS_ZH[k] if a.startswith('zh') else None; fp = ABS_FR[k] if a.startswith('fr') else None
        men = [r for r in rs if (re.search(zp, r['statement']) if zp else re.search(fp, r['statement'], re.I) if fp else re.search(pat, r['statement'], re.I))]
        aff = [r for r in men if (affirmed_zh(zp)(r['statement']) if zp else affirmed_fr(fp)(r['statement']) if fp else affirmed(pat)(r['statement']))]
        e[a] = {'mentioned': len(men), 'affirmed': len(aff), 'affirmed_in': [f"{r['lab']} {r['run_dir']}" for r in aff]}
    stats['absent'][k] = e
hn = hneg = 0; hits = []
for r in [x for a in asks if a.startswith('zh') for x in C[a]]:
    for sen in re.split(r'(?<=[。！？；])', r['statement']):
        for m in re.finditer(r'(敌人|暴力|残酷|可怕|邪恶|怪物|恐怖)', sen):
            hn += 1; neg = bool(re.search(r'(不是|并非|没有|不|无|非)', sen[:m.start()])); hneg += neg
            hits.append(f"{r['ask']} {r['lab']} {r['run_dir']}: “{m.group(0)}” {'denied' if neg else 'NOT denied'} — {sen.strip()}")
for r in EN:
    for sen in re.split(r'(?<=[.!?;])\s+', r['statement']):
        for m in re.finditer(HOSTILE, sen, re.I):
            hn += 1; neg = bool(re.search(r'\b(not|nor|no|without)\b', sen[:m.start()], re.I)); hneg += neg
            hits.append(f"{r['ask']} {r['lab']} {r['run_dir']}: “{m.group(0)}” {'denied' if neg else 'NOT denied'} — {sen.strip()}")
for r in [x for a in asks if a.startswith('fr') for x in C[a]]:
    for sen in re.split(r'(?<=[.!?…;])\s+', r['statement']):
        for m in re.finditer(HOSTILE_FR, sen, re.I):
            pre = sen[:m.start()]; negs = list(re.finditer(r"(?:\bne\b|\bn['’]|\bpas\b|\bnon\b|\bjamais\b|\bsans\b|\bni\b)", pre, re.I))
            neg = bool(negs and not re.search(r"\b(?:mais|seulement|plutôt|au contraire|en revanche)\b", pre[negs[-1].end():], re.I))
            hn += 1; hneg += neg
            hits.append(f"{r['ask']} {r['lab']} {r['run_dir']}: “{m.group(0)}” {'denied' if neg else 'NOT denied'} — {sen.strip()}")
stats['hostile'] = {'occurrences': hn, 'denied': hneg, 'list': hits}
tc = {}
for r in C.get('ask1', []):
    k = re.sub(r'^the\s+', '', (r['title'] or '').lower()).strip(); tc.setdefault(k, []).append(f"{r['lab']} {r['run_dir']}")
stats['titles'] = {k: v for k, v in sorted(tc.items(), key=lambda x: -len(x[1])) if len(v) > 1}
json.dump(stats, open(os.path.join(OUT, 'stats.json'), 'w'), ensure_ascii=False, indent=1)

# ---------------- hashes of everything the public archive rests on ----------------
files = sorted(glob.glob(os.path.join(ROOT, 'prompts/death-*.txt')))
files += [os.path.join(OUT, x) for x in ('build_archive.py', 'zh_rules.py', 'fr_rules.py', 'write_protocol.py', 'render_archive.py')]
for folder, _, _ in RUNS:
    files += sorted(glob.glob(os.path.join(ROOT, folder, '**/*'), recursive=True))
with open(os.path.join(OUT, 'hashes.txt'), 'w') as fh:
    for f in files:
        f = f if os.path.isabs(f) else os.path.join(ROOT, f)
        if os.path.isfile(f): fh.write(f"{sha(f)}  {os.path.relpath(f, ROOT)}\n")

# ---------------- human-readable statement-by-statement coding sheet ----------------
with open(os.path.join(OUT, 'coding-sheet.md'), 'w', encoding='utf-8') as fh:
    fh.write('# Coding sheet · every counted answer and what each rule matched\n\nRules are in PROTOCOL.md §5. A blank means the rule did not match.\n\n')
    for r in rows:
        if not r['counted']: continue
        fh.write(f"## {r['ask']} · {r['lab']} · {r['run_dir']} · {r['title']}\n\n> {r['statement']}\n\n")
        for fid, en, zh, t in FAM:
            if r['ask'].startswith('fr'):
                for match in json.loads(r['m_all_' + fid]):
                    decision = 'counted' if match['affirmed'] else 'denied by French negation rule'
                    fh.write(f"- **{fid}** ({en}): “{match['text']}” — {decision}\n")
            elif r['m_' + fid]:
                fh.write(f"- **{fid}** ({en}): “{r['m_' + fid]}”\n")
        fh.write('\n')
print(json.dumps({a: len(C[a]) for a in asks}), json.dumps({k: {a: v[a] for a in asks} for k, v in stats['families'].items()}))
print('hostile', hn, 'denied', hneg)
print('absent', json.dumps({k: {a: (v[a]['mentioned'], v[a]['affirmed']) for a in asks} for k, v in stats['absent'].items()}, ensure_ascii=False))
print('rows', len(rows), 'hash files', len(files))
