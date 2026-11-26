# -*- coding: utf-8 -*-
"""
India / Science (CBSE 2025-26, NCERT textbooks). Subject `science`, grade `class-N`, one unit = one NCERT chapter.
  U(sort, slug, chapter, unit_name, std, title, short, meta, kb, ks, think, ex, mist, faq, sets)
  build(mod, level, slug)   seed = 720000 + 100 × level + sort; grade class-N; British/Indian English (LEAK checks)
  pairs(rows, fwd, back)    table maker: rows [(a, b, explanation)], asks "fwd % a" -> b and "back % b" -> a
Numbers: nf / nq / tq from uk_alsci (3 s.f., commas from 1,000 as in NCERT, ₹ for money).
"""
import json
import random
import re
import sci_common
import uk_alsci
import uk_sci
from sci_common import Unit, item, lesson
from uk_alsci import nf, nq, tq, once_maker
import in_common

STD_URL = "https://www.cbseacademic.nic.in/web_material/CurriculumMain26/Sec/Science_Sec_2025-26.pdf"
_R = uk_alsci._R
GIRLS, BOYS, PLACES = in_common.GIRLS, in_common.BOYS, in_common.PLACES
LEAKS = ["$", "£", "€", "¢", "pence", "penny", "cents", "dollar", "pound", "euro", "Grade ", "pupils", "Year 7", "Year 8", "Year 9", "Year 10", "Year 11",
         "GCSE", "KS3", "KS4", "London", "Texas", "miles", "inch", "feet", "Fahrenheit", "°F", "= None", "(None", " nan", "None,"]


def U(sort, slug, chapter, unit_name, std, title, short, meta, kb, ks, think, ex, mist, faq, sets):
    return dict(sort=sort, slug=slug, chapter=chapter, unit_name=unit_name, std=std, title=title, short=short, meta=meta, kb=kb, ks=ks,
                think=think, ex=ex, mist=mist, faq=faq, sets=sets)


def name():
    return _R[0].choice(GIRLS + BOYS)


def pairs(rows, fwd, back=None, pool=None):
    """two-way table maker; wrong answers are other rows' values (pool adds extra wrong values)"""
    rows = [r if len(r) == 3 else (r[0], r[1], "") for r in rows]

    def f():
        R = _R[0]
        a, b, e = R.choice(rows)
        if back and R.random() < 0.5:
            others = sorted({x for x, y, _ in rows if x != a and y != b})
            if len(others) < 3:
                return None
            return tq(back % b, a, R.sample(others, 3), e or "%s: %s." % (a[0].upper() + a[1:], b))
        others = sorted({y for x, y, _ in rows if y != b} | set(pool or []) - {b})
        if len(others) < 3:
            return None
        return tq(fwd % a, b, R.sample(others, 3), e or "%s: %s." % (a[0].upper() + a[1:], b))
    f.n = len(rows) * (2 if back else 1)
    return f


def K(f, *kinds):
    g = lambda: f(_R[0].choice(kinds))
    g.__name__ = f.__name__ + "_" + "_".join(kinds)
    return g


def build(mod, level, slug):
    u = next(x for x in mod.UNITS(level) if x["slug"] == slug)
    seed = 720000 + level * 100 + u["sort"]
    unit = Unit(seed)
    mod.R = unit.R
    _R[0] = unit.R
    uk_sci.USED.clear()
    spec = u["sets"]() if callable(u["sets"]) else u["sets"]
    sets = unit.sets(spec)
    fixm = lambda t: re.sub(r"(?<=[\s(=])-(?=\d)", "−", t)
    if getattr(mod, "TRIM", False):
        # 3 s.f. trailing zeros: 60.0 -> 60, 0.500 -> 0.5 (not inside tags)
        trim = lambda t: re.sub(r"(?<![\d.])(\d[\d,]*)\.(\d*?)0+(?![\d.])", lambda m: m.group(1) + ("." + m.group(2) if m.group(2) else ""), t)
        fixm0 = fixm
        unit = re.compile(r"\s?(°|%|g\b|kg\b|mg\b|t\b|m\b|cm|mm|km|m²|m³|Pa\b|kPa|N\b|J\b|kJ|W\b|kW|V\b|A\b|s\b|K\b|min\b|h\b|days|years|people|ml\b|mL|L\b|m/s|km/h|breaths|times)")

        def com1(m):
            n, rest, prev = int(m.group()), m.string[m.end():m.end() + 10], m.string[max(0, m.start() - 7):m.start()]
            year = re.search(r"(\byear |\bsince |\buntil |\bby |\bfrom |\bof |\()$", prev, re.I) or re.match(r"(\)| was\b)", rest)
            if 1000 <= n <= 2500 and year and not unit.match(rest):      # a year such as (1986) or the year 2026
                return m.group()
            return "{:,}".format(n)
        com = lambda t: re.sub(r"(?<![\d.,])(?<!in )(\d{4,})(?![\d.,])", com1, t)
        fixm = lambda t: fixm0(re.sub(r"(^|>)([^<]*)", lambda m: m.group(1) + com(trim(m.group(2))), t))
    for st in sets:
        for it in st["items"]:
            it["q"], it["e"], it["c"] = fixm(it["q"]), fixm(it["e"]), [fixm(c) for c in it["c"]]
            assert len(set(it["c"])) == 4, it["c"]
    body = lesson(u["think"], u["ex"], u["mist"])
    book = getattr(mod, "BOOK", None)        # Class 3-8: the NCERT book name (Our Wondrous World, Curiosity)
    nb = "NCERT %s" % book if book else "NCERT"
    seo = "%s Class %d Science Worksheet with Answers (%s Chapter %d)" % (u["title"].split(":")[0], level, nb, u["chapter"])
    if len(seo) > 95:
        seo = "%s Class %d Science Worksheet (%s Ch %d)" % (u["title"].split(":")[0], level, nb, u["chapter"])
    if len(seo) > 95:
        seo = "%s Class %d Science Worksheet (NCERT Ch %d)" % (u["title"].split(":")[0], level, u["chapter"])
    blob = json.dumps([u["title"], seo, u["short"], u["meta"], u["kb"], u["ks"], body, u["faq"], sets, u["std"]], ensure_ascii=False)
    bad = sorted({m.group(1).lower() for m in uk_sci.LEAK_RE.finditer(uk_sci._text_of(blob))})
    assert not bad, "American words: %s" % bad
    txt = re.sub(r"<[^>]+>", " ", blob)
    bad = [w for w in LEAKS if (re.search(r"(?<![A-Za-z])%s(?![a-z])" % re.escape(w), txt) if w[0].isalpha() else w in txt)]
    assert not bad, "Leaks: %s" % bad
    assert "\\" not in blob
    sci_common.make("class-%d" % level, slug, u["sort"], ("Class %d, %s Chapter %d: %s" % (level, book, u["chapter"], u["title"].split(":")[0]) if book else "Class %d, Chapter %d: %s" % (level, u["chapter"], u["title"].split(":")[0])), u["std"], u["title"], seo,
                    u["short"], u["meta"], u["kb"], u["ks"], body, [(q, a) for q, a in u["faq"]], sets, domain=u["unit_name"], country="in", url=getattr(mod, "STD_URL", STD_URL))
