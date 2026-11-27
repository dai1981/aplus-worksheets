# -*- coding: utf-8 -*-
"""
BC science (BC's Curriculum, Science K-10 and the Grade 11-12 courses): country `ca-bc`, subject `science`,
grade `kindergarten`, `grade-1` ... `grade-12`.  K-10: one unit per Big Idea (some Big Ideas have two units); domain is the
science area (Biology / Chemistry / Physics / Earth and Space Science).  Grade 11-12: the courses Chemistry 11, Life Sciences 11,
Physics 11, Earth Sciences 11, Anatomy and Physiology 12, Chemistry 12, Physics 12, Geology 12 share one grade page
(domain = course name).
  BU(area_or_course, sort, slug, std, title, short, meta, kb, ks, think, ex, mist, faq, sets, pic=None, allow=())
      sets = lambda X: [(title, [(maker, n)]) x 5]
  X = caon_hs.X (Canadian English, names, leak checks, once per unit) plus
      X.o(mod, slug, s)   set s of an Ontario unit (caon_sci1-8, caon_hs9-12) or an Australian senior unit (au_sr11*, au_sr12*)
                          whose sets are lambda X: the makers are built with this X (no second wrap)
      X.ch(...)           as in caon_hs (UK A level, India Class 11-12)
  Items that name Ontario places or programs (Toronto, Sudbury, EQAO, SNC1W ...) are dropped.
build(mod, grade, slug): seed 69000 + 100 * grade + sort (K = 0).
"""
import importlib
import inspect
import json
import re
import caon_sci
import caon_hs
import au_sr
import uk_sci
import sci_common
from caon_sci import People, _CSrc, _quotes, ca_text, _bad, _NAME_RE, SEEN
from sci_common import lesson, kid_lesson, Unit
from au_sci import sgnum, _fixnums

URL_K10 = "https://curriculum.gov.bc.ca/curriculum/science/%s/core"
COURSES = {
    "Chemistry 11": (11, "https://curriculum.gov.bc.ca/curriculum/science/11/chemistry"),
    "Life Sciences 11": (11, "https://curriculum.gov.bc.ca/curriculum/science/11/life-sciences"),
    "Physics 11": (11, "https://curriculum.gov.bc.ca/curriculum/science/11/physics"),
    "Earth Sciences 11": (11, "https://curriculum.gov.bc.ca/curriculum/science/11/earth-sciences"),
    "Anatomy and Physiology 12": (12, "https://curriculum.gov.bc.ca/curriculum/science/12/anatomy-and-physiology"),
    "Chemistry 12": (12, "https://curriculum.gov.bc.ca/curriculum/science/12/chemistry"),
    "Physics 12": (12, "https://curriculum.gov.bc.ca/curriculum/science/12/physics"),
    "Geology 12": (12, "https://curriculum.gov.bc.ca/curriculum/science/12/geology"),
}
AREAS = ("Biology", "Chemistry", "Physics", "Earth and Space Science")

BC_DROP = [r"\b(Ontario|Ontarian|Toronto|Ottawa|Sudbury|Hamilton|Kingston|Thunder Bay|Muskoka|Niagara|Great Lakes|Lake Ontario|Lake Erie|"
           r"Lake Huron|Lake Superior|Canadian Shield|Algonquin Park|EQAO|HST|SNC1W|SNC2D|SBI[34]U|SCH[34]U|SPH[34]U|Grade 1[0-2]? ?[A-Z]{3}\d)\b",
           r"\b13 ?%"]
_BCRE = re.compile("|".join(BC_DROP))


def BU(area, sort, slug, std, title, short, meta, kb, ks, think, ex, mist, faq, sets, pic=None, allow=()):
    assert area in AREAS or area in COURSES, area
    return dict(area=area, sort=sort, slug=slug, std=std, title=title, short=short, meta=meta, kb=kb, ks=ks, think=think,
                ex=ex, mist=mist, faq=faq, sets=sets, pic=pic, allow=tuple(allow))


class X(caon_hs.X):
    def _w(self, f, rep=(), drop=()):
        return super()._w(f, rep, list(drop) + BC_DROP)

    def gen(self, mod, name, rep=(), drop=(), n=None):
        return super().gen(mod, name, rep, list(drop) + BC_DROP, n)

    def w(self, f, rep=(), drop=(), n=None):
        return super().w(f, rep, list(drop) + BC_DROP, n)

    def o(self, mod, slug, s, year=None):
        """set s of a unit whose sets take X (Ontario caon_*, Australian au_sr*): built with this X"""
        key = ("o", mod, year, slug)
        if key not in self._spec:
            u = self._units(mod, year)[slug]
            self._sync()
            fn = u["sets"]
            self._spec[key] = fn(self) if len(inspect.signature(fn).parameters) else fn()
        ms = self._spec[key][s - 1][1]
        tot = sum(n for _, n in ms)
        R = self.R

        def g():
            self._sync()
            r = R.random() * tot
            for f, n in ms:
                r -= n
                if r < 0:
                    break
            it = f()
            if it is None or _BCRE.search(re.sub(r"<[^>]+>", " ", json.dumps(it, ensure_ascii=False))):
                return None
            return it
        g.__name__ = "%s_%s_%d" % (mod, slug, s)
        return g

    def pic(self, mod, slug):
        return self._units(mod, None)[slug]["pic"]


def seed_of(grade, sort):
    return 69000 + 100 * grade + sort


def gname(grade):
    return "kindergarten" if grade == 0 else "grade-%d" % grade


def build(mod, grade, slug):
    us = mod.UNITS(grade) if len(inspect.signature(mod.UNITS).parameters) else mod.UNITS()
    u = next(x for x in us if x["slug"] == slug)
    sort = u["sort"]
    U = Unit(seed_of(grade, sort))
    R = U.R
    P = People(R)
    uk_sci.USED.clear()
    SEEN.clear()
    src = _CSrc(U, P)
    x = X(U, R, P, src)
    pic = u["pic"](x) if callable(u["pic"]) else u["pic"]
    sets = U.sets(u["sets"](x))
    area = u["area"]
    subj = "Chemistry" if "Chemistry" in area else ("Biology" if area in ("Biology", "Life Sciences 11", "Anatomy and Physiology 12") else "")
    for st in sets:
        for it in st["items"]:
            it["q"], it["e"], it["c"] = caon_hs._fix(it["q"], subj), caon_hs._fix(it["e"], subj), [caon_hs._fix(c, subj) for c in it["c"]]
            it["q"] = it["q"].replace("sgpond", "pond")
            assert len({c.strip().lower() for c in it["c"]}) == 4, it["c"]
    sets = _fixnums(sets)
    if pic is not None:
        lead, points = u["think"]
        body = kid_lesson(pic, lead, points, u["ex"], u["mist"])
    else:
        body = lesson(u["think"], u["ex"], u["mist"])
    body = sgnum(body)
    if area in COURSES:
        gr, url = COURSES[area]
        assert gr == grade
        seo = "%s: %s Worksheets (BC Curriculum)" % (area, u["title"])
        if len(seo) > 95:
            seo = "%s: %s Worksheets" % (area, u["title"])
        code = area
        std = "%s (summary of BC's Curriculum, %s)" % (u["std"], area)
    else:
        url = URL_K10 % ("K" if grade == 0 else str(grade))
        gl = "Kindergarten" if grade == 0 else "Grade %d" % grade
        seo = "%s Science: %s Worksheets (BC Curriculum)" % (gl, u["title"])
        if len(seo) > 95:
            seo = "%s Science: %s Worksheets" % (gl, u["title"])
        code = "%s: %s" % (gl, area)
        std = "%s (summary of BC's Curriculum, Science %s, %s)" % (u["std"], "K" if grade == 0 else grade, area)
    blob = json.dumps([u["title"], seo, u["short"], u["meta"], u["kb"], u["ks"], body, u["faq"], sets, std], ensure_ascii=False)
    bad = sorted(_bad(blob) - set(u["allow"]) - {"southern seasons"})
    for st in sets:
        for it in st["items"]:
            assert not caon_sci.SEASON_RE.search(re.sub(r"<[^>]+>", " ", it["q"] + " " + it["c"][it["a"]] + " " + it["e"])), it["q"]
    if bad:
        low = blob.lower()
        ctx = [low[max(0, low.find(w) - 80):low.find(w) + 40] for w in bad]
        raise AssertionError("Words that do not fit BC: %s %s" % (bad, ctx))
    txt = re.sub(r"<[^>]+>", " ", blob)
    m = _BCRE.search(txt) or au_sr.SR_LEAK.search(txt)
    assert not m, "Word left: %s [%s]" % (m.group(0), txt[max(0, m.start() - 150):m.end() + 60])
    m = _NAME_RE.search(txt)
    assert not m, "Foreign name left: %s" % m.group(1)
    assert "\\" not in blob, blob[max(0, blob.index("\\") - 120):blob.index("\\") + 40]
    sci_common.make(gname(grade), slug, sort, code, std, u["title"], seo, u["short"], u["meta"], u["kb"], u["ks"], body,
                    [(q, a) for q, a in u["faq"]], sets, domain=area, country="ca-bc", url=url)


def _part(X, p):
    if isinstance(p, str):
        bits = p.split(":")
        mod, slug, s = bits[0], bits[1], int(bits[2])
        year = int(bits[3]) if len(bits) > 3 else None
        if mod.startswith(("al_", "in_s")):
            return X.ch(mod, slug, s, year)
        return X.o(mod, slug, s, year)
    return p


def S(X, rows):
    """rows: [(title, "mod:slug:set") or (title, [(part, n), ...])] -> sets; part = "mod:slug:set[:year]" or a maker"""
    out = []
    for title, parts in rows:
        if isinstance(parts, str):
            parts = [(parts, 20)]
        out.append((title, [(_part(X, p), n) for p, n in parts]))
    return out


def _clean(f):
    def g():
        it = f()
        if it is None or _BCRE.search(re.sub(r"<[^>]+>", " ", json.dumps(it, ensure_ascii=False))):
            return None
        return it
    g.__name__ = getattr(f, "__name__", "g")
    return g


def GM(X, mod, *names, n=20):
    """parts [(maker, k)] from one gen module: names g_x or bank names (B1, POOL1); n questions shared out"""
    mod = mod if mod.startswith("gen_") else "gen_" + mod
    k, r = divmod(n, len(names))
    out = []
    for i, nm in enumerate(names):
        f = X.B(mod, nm) if not nm.startswith("g_") else X.gen(mod, nm)
        out.append((_clean(f), k + (1 if i < r else 0)))
    return out
