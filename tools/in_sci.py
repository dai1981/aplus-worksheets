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
    for st in sets:
        for it in st["items"]:
            it["q"], it["e"], it["c"] = fixm(it["q"]), fixm(it["e"]), [fixm(c) for c in it["c"]]
    body = lesson(u["think"], u["ex"], u["mist"])
    seo = "%s Class %d Science Worksheet with Answers (NCERT Chapter %d)" % (u["title"].split(":")[0], level, u["chapter"])
    if len(seo) > 95:
        seo = "%s Class %d Science Worksheet (NCERT Ch %d)" % (u["title"].split(":")[0], level, u["chapter"])
    blob = json.dumps([u["title"], seo, u["short"], u["meta"], u["kb"], u["ks"], body, u["faq"], sets, u["std"]], ensure_ascii=False)
    bad = sorted({m.group(1).lower() for m in uk_sci.LEAK_RE.finditer(uk_sci._text_of(blob))})
    assert not bad, "American words: %s" % bad
    txt = re.sub(r"<[^>]+>", " ", blob)
    bad = [w for w in LEAKS if (re.search(r"(?<![A-Za-z])%s(?![a-z])" % re.escape(w), txt) if w[0].isalpha() else w in txt)]
    assert not bad, "Leaks: %s" % bad
    assert "\\" not in blob
    sci_common.make("class-%d" % level, slug, u["sort"], "Class %d, Chapter %d: %s" % (level, u["chapter"], u["title"].split(":")[0]), u["std"], u["title"], seo,
                    u["short"], u["meta"], u["kb"], u["ks"], body, [(q, a) for q, a in u["faq"]], sets, domain=u["unit_name"], country="in", url=STD_URL)
