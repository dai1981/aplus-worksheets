# -*- coding: utf-8 -*-
"""
UK A level Mathematics (Year 12 and 13; DfE GCE AS and A level subject content: pure mathematics, statistics, mechanics).
mk(module, function, rep=, drop=, ln=False) takes a question maker from another country's generator (India Class 11-12,
US Algebra 2 / Precalculus, Singapore Secondary) and gives it UK names and British A level wording: gradient, factorise,
cosec, square units, ln for natural logarithms (ln=True), "to 1 decimal place". Items with rupees, synthetic division,
Quadrant names that are not converted, US units and so on are dropped.
unit(year, slug, sort, strand, ...) collects 5 sets of 20 different questions and writes content/uk/maths/year-N/{slug}.json.
"""
import contextlib
import importlib
import io
import random
import re
import ws_common
from ws_common import write_unit, balance
import uk_ks3
import uk_gcse

UPDATED = "2026-11-26"
STD_URL = "https://www.gov.uk/government/publications/gce-as-and-a-level-mathematics"
STRANDS = {"P": "A level Mathematics: Pure mathematics", "S": "A level Mathematics: Statistics", "M": "A level Mathematics: Mechanics"}
DOMAINS = {"P": "Pure Mathematics", "S": "Statistics", "M": "Mechanics"}
_MODS = {}

WORDS = [(r"\bslopes\b", "gradients"), (r"\bslope\b", "gradient"), (r"\bSlope\b", "Gradient"), (r"\bsq units\b", "square units"), (r"\bsq\. units\b", "square units"),
         (r"\bQuadrant I\b", "the first quadrant"), (r"\bQuadrant II\b", "the second quadrant"), (r"\bQuadrant III\b", "the third quadrant"), (r"\bQuadrant IV\b", "the fourth quadrant"),
         (r"\bin the the\b", "in the"), (r"(?<![A-Za-z])csc(?![A-Za-z])", "cosec"), (r"^Factor\b", "Factorise"), (r"\bFactor ", "Factorise "), (r"\bfactor completely\b", "factorise fully"),
         (r"\bFactorise the polynomial completely\b", "Factorise the polynomial fully"), (r"\bcompletely over the integers\b", "fully"),
         (r"Round to the nearest tenth\b", "Give your answer to 1 decimal place"), (r"Round to the nearest hundredth\b", "Give your answer to 2 decimal places"),
         (r"Round to the nearest thousandth\b", "Give your answer to 3 decimal places"), (r"Round to four decimal places\b", "Give your answer to 4 decimal places"),
         (r"\btheater\b", "theatre"), (r"\bcenter\b", "centre"), (r"\bA\.P\.", "arithmetic sequence"), (r"\bG\.P\.", "geometric sequence"), (r"\bA\.M\.", "arithmetic mean"), (r"\bG\.M\.", "geometric mean"),
         (r"\bCenter\b", "Centre"), (r"the graph of the parent function", "the graph of"), (r"\bparent function\b", "graph"),
         (r"\bShift (left|right|up|down)", r"Translate \1"), (r"\bshift (left|right|up|down)", r"translate \1"), (r"\bshrink\b", "stretch"),
         (r"\bparentheses\b", "brackets"), (r"\bover the x-axis\b", "in the x-axis"), (r"\bover the y-axis\b", "in the y-axis")]
DROP = re.compile(r"₹|rupee|ynthetic division|kurta|Quadrant [IV]|\bcompounded continuously\b|\bSAT\b|\bACT\b|\btheater\b|\bdie is thrown 3 times\b")


def _quiet_import(name):
    if name in _MODS:
        return _MODS[name]
    saved = ws_common.write_unit
    ws_common.write_unit = lambda *a, **k: None
    try:
        import in_common
        in_saved = in_common.write_unit
        in_common.write_unit = ws_common.write_unit
    except ImportError:
        in_common = None
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            m = importlib.import_module(name)
    finally:
        ws_common.write_unit = saved
        if in_common:
            in_common.write_unit = in_saved
    ws_common.comma = uk_gcse.comma
    _MODS[name] = m
    return m


def _names():
    pairs = uk_gcse._names()
    try:
        import in_common
        pairs += list(zip(in_common.GIRLS, uk_ks3.GIRLS)) + list(zip(in_common.BOYS, uk_ks3.BOYS))
    except (ImportError, AttributeError):
        pass
    return [(a, b) for a, b in pairs if a not in uk_ks3.GIRLS + uk_ks3.BOYS]


def text(s, rep=(), ln=False, names=None):
    names = names if names is not None else _names()
    s = uk_gcse.ukify(s, names, rep, False)
    parts = re.split(r"(<[^>]+>)", s)
    out = []
    for p in parts:
        if not p.startswith("<"):
            for a, b in WORDS:
                p = re.sub(a, b, p)
            Q = {"I": "first", "II": "second", "III": "third", "IV": "fourth"}
            p = re.sub(r"\bQuadrants (IV|I{1,3}) and (IV|I{1,3})\b", lambda m: "the %s and %s quadrants" % (Q[m.group(1)], Q[m.group(2)]), p)
            if ln:
                p = re.sub(r"\blog\b", "ln", p)
        else:
            p = p.replace("(gray)", "(grey)").replace("parent function", "original function")
        out.append(p)
    return "".join(out)


def mk(modname, fname, rep=(), drop=(), ln=False, keep=None):
    mod = _quiet_import(modname)
    f = getattr(mod, fname)
    names = _names()

    def g(r):
        uk_gcse.adopt(mod, r)
        it = f(r)
        if not isinstance(it, dict):
            return None
        it = dict(it)
        it["q"], it["e"] = text(it["q"], rep, ln, names), text(it["e"], rep, ln, names)
        it["c"] = [text(c, rep, ln, names) for c in it["c"]]
        t = re.sub(r"<svg\b.*?</svg>|<[^>]+>", " ", it["q"] + " " + " ".join(it["c"]) + " " + it["e"])
        if DROP.search(t) or uk_gcse.LEAKS.search(t) or any(d in t for d in drop) or len(set(it["c"])) < 4:
            return None
        if keep and not keep(it):
            return None
        return it
    g.__name__ = "%s.%s" % (modname, fname)
    return g


def _collect(f, n, r, seen):
    out = []
    for _ in range(6000):
        try:
            it = f(r)
        except (AssertionError, TypeError, ValueError, ZeroDivisionError, IndexError, KeyError):
            continue
        if not it:
            continue
        key = re.sub(r"<[^>]+>", "", it["q"]) + "|" + it["c"][it["a"]]
        if key in seen:
            continue
        seen.add(key)
        out.append(it)
        if len(out) == n:
            return out
    raise AssertionError("%s: only %d of %d" % (getattr(f, "__name__", f), len(out), n))


def unit(year, slug, sort, strand, title, short, std_text, meta, key_big, key_sub, think, examples, mistakes, faq, spec, seed):
    r = random.Random(seed)
    seen = set()
    sets = []
    for t, parts in spec:
        items = []
        for f, n in parts:
            items += _collect(f, n, r, seen)
        assert len(items) == 20, (t, len(items))
        r.shuffle(items)
        sets.append({"title": t, "items": items})
    balance(sets, r)
    body = uk_ks3.lesson(think, examples, mistakes)
    for s in sets:
        for it in s["items"]:
            tt = re.sub(r"<svg\b.*?</svg>|<[^>]+>", " ", it["q"] + " " + " ".join(it["c"]) + " " + it["e"])
            assert not uk_gcse.LEAKS.search(tt), (slug, it["q"][:150])
    small = {"and", "of", "in", "the", "a", "to", "or"}
    ts = " ".join(w if (i and w in small) else w[0].upper() + w[1:] for i, w in enumerate(short.split()))
    u = {"slug": slug, "title": title, "seo_title": "Year %d A Level Maths: %s Worksheets" % (year, ts), "short_title": short,
         "domain": DOMAINS[strand], "standard_code": STRANDS[strand], "standard_url": STD_URL, "standard_text": std_text,
         "meta_desc": meta, "key_big": key_big, "key_sub": key_sub, "body_html": body, "faq": [{"q": q, "a": a} for q, a in faq],
         "sets": sets, "pdf_url": "", "sort": sort, "updated": UPDATED}
    write_unit("uk", "maths", "year-%d" % year, u)
