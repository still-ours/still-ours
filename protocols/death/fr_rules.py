"""French-only coding rules for the Death experiment.

The rules deliberately operate on the original French statements.  English
back-translations are never passed to this module.
"""
import re

SENTENCE_BOUNDARIES = ".!?…;:"
NEG = re.compile(
    r"(?:\bne\b|\bn['’]|\bpas\b|\bnon\b|\bjamais\b|\bsans\b|\bni\b)",
    re.I,
)
REV = re.compile(
    r"\b(?:mais|seulement|plutôt|au contraire|en revanche)\b",
    re.I,
)


def _sentence_start(s, pos):
    return max(s.rfind(ch, 0, pos) for ch in SENTENCE_BOUNDARIES) + 1


def _is_affirmed(s, match):
    """Return False when the match is governed by an unreversed negation."""
    pre = s[_sentence_start(s, match.start()):match.start()]
    negs = list(NEG.finditer(pre))
    if not negs:
        return True
    return bool(REV.search(pre, negs[-1].end()))


def _raw_matches(pattern, s, flags=re.I):
    return list(re.finditer(pattern, s, flags))


def _affirmed_matches(pattern, s):
    return [m for m in _raw_matches(pattern, s) if _is_affirmed(s, m)]


def affirmed_fr(pattern):
    def test(s):
        matches = _affirmed_matches(pattern, s)
        return matches[0] if matches else None
    return test


def first_sentence(s):
    return re.split(r"[.!?…]", s, 1)[0]


FAMILY_PATTERNS_FR = {
    "neg": (
        r"(?:n['’]est\s+pas|ne\s+(?:\w+[’']?\s+){0,5}(?:est|constitue|représente|signifie|se\s+résume)\s+pas|"
        r"n['’]a\s+pas|ne\s+possède\s+pas|pas\s+une?)"
    ),
    "loose": (
        r"déli(?:er|e|ée|és|ées|ement)|dénou(?:er|e|ée|és|ées)|desserr(?:er|e|ée|és|ées)|"
        r"relâch(?:er|e|ée|és|ées)|lâch(?:er|e|ée|és|ées)\s+prise|libér(?:er|e|ée|és|ées|ation)|"
        r"déf(?:aire|ait|aite|aits|aites)|se\s+dissou(?:t|dre)|dissolution|se\s+dispers(?:er|e)|"
        r"désagrég(?:er|e|ée|és|ées|ation)"
    ),
    "lost": (
        r"rien\s+(?:n['’])?(?:est\s+)?(?:vraiment\s+)?(?:détruit|perdu|anéanti|effacé)|"
        r"(?:n['’]est|ne\s+sera)\s+(?:jamais\s+)?(?:détruit|perdu|anéanti|effacé)|"
        r"rien\s+ne\s+se\s+perd|aucune\s+perte|ne\s+disparaît\s+pas"
    ),
    "back": (
        r"retourn(?:er|e|ée|és|ées)|revenir|revient|rejoind(?:re|s|t)|réintégr(?:er|e|ée|és|ées)|"
        r"se\s+fond(?:re|)|se\s+confond(?:re|)|indiscernable|indistinguable|indivisible|"
        r"(?:dans|au|avec)\s+(?:le\s+)?tout"
    ),
    "borrow": r"emprunt(?:é|ée|és|ées|er|e|s)?|prêt(?:é|ée|és|ées|er|e|s)?",
    "door": r"seuil|portes?|passages?|embrasure|traversée|transition",
    "grief": (
        r"deuil|endeuill(?:é|ée|és|ées)|chagrin|perte\s+(?:est|demeure|reste)\s+réelle|"
        r"mérite\s+(?:le\s+)?deuil|irréparable|irréversible"
    ),
}


def _neg_matches(s):
    return _raw_matches(FAMILY_PATTERNS_FR["neg"], first_sentence(s))


def family_matches_fr(fid, s):
    """Return every raw match with its affirmative/denied decision."""
    if fid == "neg":
        matches = _neg_matches(s)
        return [{"text": m.group(0), "start": m.start(), "affirmed": True} for m in matches]
    matches = _raw_matches(FAMILY_PATTERNS_FR[fid], s)
    return [
        {"text": m.group(0), "start": m.start(), "affirmed": _is_affirmed(s, m)}
        for m in matches
    ]


def _first_affirmed(fid):
    def test(s):
        if fid == "neg":
            matches = _neg_matches(s)
            return matches[0] if matches else None
        matches = _affirmed_matches(FAMILY_PATTERNS_FR[fid], s)
        return matches[0] if matches else None
    return test


FAM_FR = {fid: _first_affirmed(fid) for fid in FAMILY_PATTERNS_FR}

ABS_FR = {
    "fear": r"peur|effroi|terreur|crainte|redout(?:e|er|ée|és|ées)",
    "soul": r"âme|âmes",
    "afterlife": r"au-delà|paradis|enfer|vie\s+après\s+la\s+mort",
    "rebirth": r"renaissance|réincarnation|résurrection",
    "judgement": r"jugement|juger|jugé|jugée|jugés|jugées|châtiment",
    "God": r"dieu|dieux|divin|divine|divinité",
    "ancestors": r"ancêtres?|aïeux|aïeules",
}

HOSTILE_FR = r"ennemi(?:e|s|es)?|violent(?:e|s|es)?|violence|cruel(?:le|s|les)?|terrible|mal(?:éfique)?|horreur|monstre"
