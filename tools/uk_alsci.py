# -*- coding: utf-8 -*-
"""
UK A level sciences (Year 12 and 13): Biology, Chemistry and Physics, subject `science`, grade `year-12` / `year-13`.
DfE: GCE AS and A level subject content for biology, chemistry, physics and psychology.
  nf(x, sf)           number to sf significant figures (commas from 1,000; × 10ⁿ for very large or small numbers)
  nq(q, v, wrongs, unit, e, sf)  numeric item; wrong values from real mistakes, None if fewer than 3 differ
  build(mod, slug)    builds one unit from mod.UNITS (dicts made with U()) with a fresh Unit and mod.R
Makers in al_bio / al_chem / al_phys use their module's R, which build() points at the unit's random generator.
"""
import json
import math
import re
import sci_common
import uk_sci
from sci_common import Unit, item, bank, lesson, table
from uk_ks3 import People

STD_URL = "https://www.gov.uk/government/publications/gce-as-and-a-level-biology-chemistry-physics-and-psychology"
MINUS = "−"
SUP = str.maketrans("-0123456789", "⁻⁰¹²³⁴⁵⁶⁷⁸⁹")


def nf(x, sf=3, sci_lo=1e-3, sci_hi=1e6):
    """3 s.f. by default; 0.000123 -> 1.23 × 10⁻⁴; 1234.5 -> 1,230"""
    if x == 0:
        return "0"
    if isinstance(x, int) and abs(x) < 10 ** 7:
        return (MINUS if x < 0 else "") + "{:,}".format(abs(x))
    neg = x < 0
    x = abs(float(x))
    e = int(math.floor(math.log10(x)))
    m = round(x / 10 ** e, sf - 1)
    if m >= 10:
        m /= 10
        e += 1
    if x < sci_lo or x >= sci_hi:
        s = ("%." + str(sf - 1) + "f") % m + " × 10<sup>%s</sup>" % (str(e).replace("-", MINUS))
    else:
        v = round(x, sf - 1 - e)
        p = max(0, sf - 1 - e)
        s = "{:,.{p}f}".format(v, p=p)
    return (MINUS if neg else "") + s


def nq(q, val, wrongs, unit, e, sf=3):
    wrongs = [w for w in wrongs if w is not None]
    if not (isinstance(val, int) and all(isinstance(w, int) for w in wrongs)):
        val, wrongs = float(val), [float(w) for w in wrongs]
        if abs(val) < 1e7 and val.is_integer() and all(abs(w) < 1e7 and w.is_integer() for w in wrongs):
            val, wrongs = int(val), [int(w) for w in wrongs]
    a = nf(val, sf) + unit
    ws = []
    for w in wrongs:
        if w is None:
            continue
        try:
            s = nf(w, sf) + unit
        except (ValueError, OverflowError, ZeroDivisionError):
            continue
        if s != a and s not in ws:
            ws.append(s)
    if len(ws) < 3:
        return None
    return item(q, a, ws[:3], e)


def tq(q, a, wrongs, e):
    """text item; None if the wrong answers do not give 3 different choices"""
    ws = []
    for w in wrongs:
        if w and w != a and w not in ws:
            ws.append(w)
    if len(ws) < 3:
        return None
    return item(q, a, ws[:3], e)


def once_maker(rows):
    """bank-like maker from rows [(q, a, [w,w,w], e)]: returns a random row each call (Unit removes repeats)."""
    its = [item(*r) for r in rows]

    def f():
        import copy
        return copy.deepcopy(_R[0].choice(its))
    f.n = len(its)
    return f


_R = [None]


def U(subject, sort, slug, topic, std, title, short, meta, kb, ks, think, ex, mist, faq, sets):
    return dict(subject=subject, sort=sort, slug=slug, topic=topic, std=std, title=title, short=short, meta=meta, kb=kb, ks=ks,
                think=think, ex=ex, mist=mist, faq=faq, sets=sets)


def build(mod, year, slug):
    u = next(x for x in mod.UNITS(year) if x["slug"] == slug)
    seed = 700000 + year * 100 + u["sort"]
    unit = Unit(seed)
    mod.R = unit.R
    _R[0] = unit.R
    if hasattr(mod, "P"):
        mod.P = People(unit.R)
    uk_sci.USED.clear()
    spec = u["sets"]() if callable(u["sets"]) else u["sets"]
    sets = unit.sets(spec)
    fixm = lambda t: re.sub(r"(?<=[\s(=])-(?=\d)", MINUS, t)
    for st in sets:
        for it in st["items"]:
            it["q"], it["e"], it["c"] = fixm(it["q"]), fixm(it["e"]), [fixm(c) for c in it["c"]]
    body = lesson(u["think"], u["ex"], u["mist"])
    short = u["short"]
    small = {"and", "of", "in", "the", "a", "to", "or", "for"}
    ts = " ".join(w if (i and w in small) else w[0].upper() + w[1:] for i, w in enumerate(short.split()))
    seo = "Year %d A Level %s: %s Worksheets" % (year, u["subject"], ts)
    grade = "year-%d" % year
    blob = json.dumps([u["title"], seo, short, u["meta"], u["kb"], u["ks"], body, u["faq"], sets, u["std"]], ensure_ascii=False)
    bad = sorted({m.group(1).lower() for m in uk_sci.LEAK_RE.finditer(uk_sci._text_of(blob))})
    assert not bad, "American words: %s" % bad
    assert "\\" not in blob
    sci_common.make(grade, slug, u["sort"], "A level %s: %s" % (u["subject"], u["topic"]), u["std"], u["title"], seo, short, u["meta"],
                    u["kb"], u["ks"], body, [(q, a) for q, a in u["faq"]], sets, domain=u["subject"], country="uk", url=STD_URL)
