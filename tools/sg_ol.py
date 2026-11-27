# -*- coding: utf-8 -*-
"""
Singapore Upper Secondary science (Singapore-Cambridge GCE O-Level Physics 6091, Chemistry 6092, Biology 6093, MOE 2023
syllabuses, first examined 2025): grade `secondary-3` / `secondary-4`, domain Physics / Chemistry / Biology
(one grade page lists the three subjects, as for UK A level).
  OL(seed) -> (U, R, P, src)
    src("gen_uk_science_y10_electricity", "g_q", rep=[(regex, new)], drop=[regex]) adopts any science maker (UK, US or SG
    generator) with Singapore names, British spelling and O-Level wording; src.B("module", "B1") gives a bank list.
    Every imported generator module (and the modules it imported) is pointed at this unit (U, R, P), so the seed is ours.
  make_ol(level, subj, slug, sort, topic, std, title, short, meta, kb, ks, think, ex, mist, faq, sets)
    standard_code "O-Level Physics (6091): Kinematics", standard_url = the syllabus PDF, seo_title from the subject.
O-Level physics uses g = 10 N/kg (10 m/s²): items with 9.8 or 9.81 from other countries are dropped.
Seeds: 65000 + 100 * level + 20 * subject index + sort (Physics 0, Chemistry 1, Biology 2 -> P 0..19, C 20..39, B 40..59).
"""
import json
import re
import sys
import importlib
import sci_common
import uk_sci
import sg_sci
from sg_sci import (Unit, item, bank, lesson, table, People, once, upto, sgm, _bad, UK_NAMES, fig)
from sg_lss import sgnum

SUBJ = {"Physics": ("6091", "https://www.seab.gov.sg/files/O%20Lvl%20Syllabus%20Sch%20Cddts/2026/6091_y26_sy.pdf"),
        "Chemistry": ("6092", "https://www.moe.gov.sg/api/media/3d7b6e4b-4b12-444e-ab9f-57f5d4d2365f/2023-OLevel-Chemistry-Syllabus-Updated-2024.pdf"),
        "Biology": ("6093", "https://moe.gov.sg/-/media/files/secondary/syllabuses/science/updated-2024/2023-olevel-biology-syllabus-updated-2024.pdf")}
SIDX = {"Physics": 0, "Chemistry": 1, "Biology": 2}

OL_REP = [(r"\bpupils\b", "students"), (r"\bPupils\b", "Students"), (r"\bpupil\b", "student"), (r"\bPupil\b", "Student"),
          (r"\bGCSE\b", "O-Level"), (r"\bin a UK plug\b", "in a Singapore plug"), (r"\bUK mains\b", "Singapore mains"),
          (r"\bmobile phone", "handphone"), (r"\bsnooker\b", "billiard"), (r"\bmarathon runner", "runner"),
          (r"\bmol L⁻¹", "mol/dm³"), (r"\bdm⁻³", "/dm³")]
OL_DROP = [r"\bUK\b", r"\bBritain\b", r"\bAmerica\b", r"\bUS\b", r"\bKS[1-4]\b", r"\bYear \d", r"\bA level\b", r"(?<![\d.])9\.81?(?!\d)", r"Ofsted", r"National Grid", r"\bNHS\b", "£", r"\bGrade \d", r"\bNGSS\b",
           r"\bfeet\b", r"\bmiles?\b", r"°F", r"\bCommon Core\b", r"\bmph\b"]

_mods = {}
import random as _random  # noqa: E402
import ws_common as _ws  # noqa: E402
from sg_sec import GIRLS as _SG_G, BOYS as _SG_B  # noqa: E402
_US_NAMES = [n for n in _ws.GIRLS + _ws.BOYS if n not in _SG_G + _SG_B + uk_sci.GIRLS + uk_sci.BOYS]
_US_RE = re.compile(r"\b(%s)\b" % "|".join(sorted(_US_NAMES, key=len, reverse=True)))
_NR2 = _random.Random(2025)


def _us_names(it):
    sub = {}

    def nm(m):
        k = m.group(1)
        if k not in sub:
            pool = [n for n in (_SG_G if k in _ws.GIRLS else _SG_B) if n not in sub.values()]
            sub[k] = _NR2.choice(pool)
        return sub[k]
    it["q"], it["e"] = _US_RE.sub(nm, it["q"]), _US_RE.sub(nm, it["e"])
    it["c"] = [_US_RE.sub(nm, c) for c in it["c"]]
    return it


class _Src:
    def __init__(self, U, P):
        self.U, self.P = U, P

    def _mod(self, name):
        if name not in _mods:
            m = importlib.import_module(name)
            _mods[name] = m
        self.sync()
        return _mods[name]

    def sync(self):
        """point every loaded generator / helper module with module-level U, R or P at this unit"""
        for k, m in list(sys.modules.items()):
            if m is None or not (k.startswith("gen_") or k.startswith("al_") or k in ("sci_foodweb",)):
                continue
            if hasattr(m, "R"):
                m.R = self.U.R
            if hasattr(m, "U") and isinstance(getattr(m, "U"), sci_common.Unit):
                m.U = self.U
            if hasattr(m, "P") and isinstance(getattr(m, "P"), (uk_sci.People, People)):
                m.P = self.P if isinstance(m.P, People) else uk_sci.People(self.U.R)

    def wrap(self, f, rep=(), drop=()):
        g0 = sgm(f, list(OL_REP) + list(rep))
        dr = re.compile("|".join(list(OL_DROP) + list(drop)), re.I)

        def g():
            it = g0()
            if it is None:
                return None
            it = _us_names(it)
            if dr.search(re.sub(r"<[^>]+>", " ", json.dumps(it, ensure_ascii=False))):
                return None
            return it
        g.__name__ = getattr(f, "__name__", "g")
        return g

    def __call__(self, mod, name, rep=(), drop=()):
        m = self._mod(mod)
        f = getattr(m, name)
        return self.wrap(f, rep, drop)

    def B(self, mod, name, rep=(), drop=()):
        m = self._mod(mod)
        return [self.wrap(f, rep, drop) for f in getattr(m, name)]


def OL(seed):
    U = Unit(seed)
    R = U.R
    P = People(R)
    uk_sci.USED.clear()
    return U, R, P, _Src(U, P)


def seed_of(level, subj, sort):
    return 65000 + 100 * level + 20 * SIDX[subj] + sort


_AN = re.compile(r"\b([Aa]) (?=8|(?:11|18)(?![\d.]))")


_AN2 = re.compile(r"\b([Aa]) (?=a|i|o(?!ne\b|ne-|nce\b)|e(?!u)|u(?!ni|se|su|ra|ro|ti|tub|-))")
_BIG = re.compile(r"(?<![\d.,\u00a0])(\d{5,})(?![\d.,]\d)")


def _big(m):
    d = m.group(1)
    out = ""
    while len(d) > 3:
        out = "\u00a0" + d[-3:] + out
        d = d[:-3]
    return d + out


def _art(t):
    """a 8 kg -> an 8 kg, a 800 N -> an 800 N, a oil -> an oil; 13600 -> 13 600 (also in text between tags)"""
    def f(x):
        x = _AN.sub(lambda k: k.group(1) + "n ", x)
        x = _AN2.sub(lambda k: k.group(1) + "n ", x)
        return _BIG.sub(_big, x)
    return re.sub(r"(<[^>]*>)|([^<]+)", lambda m: m.group(1) or f(m.group(2)), t)


def _fixnums(sets):
    for st in sets:
        for it in st["items"]:
            it["q"], it["e"] = _art(sgnum(it["q"])), _art(sgnum(it["e"]))
            it["c"] = [_art(sgnum(c)) for c in it["c"]]
    return sets


def make_ol(level, subj, slug, sort, topic, std_text, title, short, meta, key_big, key_sub, think, ex, mist, faq, sets, allow=(), seo=None):
    assert level in (3, 4) and subj in SUBJ, (level, subj)
    code, url = SUBJ[subj]
    sets = _fixnums(sets)
    body = sgnum(lesson(think, ex, mist))
    seo = seo or "Secondary %d %s: %s Worksheets (O-Level %s with Answers)" % (level, subj, title, code)
    if len(seo) > 95:
        seo = "Secondary %d %s: %s Worksheets (O-Level)" % (level, subj, title)
    blob = json.dumps([title, seo, short, meta, key_big, key_sub, body, faq, sets, std_text], ensure_ascii=False)
    bad = sorted(_bad(blob) - set(allow))
    assert not bad, "Words that do not fit Singapore: %s" % bad
    t = re.sub(r"<[^>]+>", " ", blob)
    m = re.compile(r"\b(%s)\b" % "|".join(re.escape(n) for n in UK_NAMES)).search(t)
    assert not m, "UK name left: %s" % m.group(1)
    m = re.search(r".{25}\bpupils?\b.{25}", re.sub(r"\b(?:the|The|and|bigger|larger|smaller) pupils?\b|\bpupils? (?:widen|dilate|reflex|become|becomes|get)", "", t))
    assert not m, "pupil (a student?): %s" % (m.group(0) if m else "")
    for w in ("Year 1", "Year 9", "PSLE", "GCSE"):
        assert w not in t, w
    assert subj != "Physics" or not re.search(r"(?<![\d.])9\.81?(?!\d)", t), "g = 9.8 left"
    sci_common.make("secondary-%d" % level, slug, sort, "O-Level %s (%s): %s" % (subj, code, topic), std_text, title, seo, short, meta,
                    key_big, key_sub, body, faq, sets, domain=subj, country="sg", url=url)


# ---- small makers ----
from uk_alsci import nf, tq   # noqa: E402  (nf: 3 s.f.; sgnum turns 1,500 into 1500 on the page)
import uk_alsci  # noqa: E402

_TZ = re.compile(r"(\d\.\d*?[1-9])0+(?!\d)|(\d)\.0+(?!\d)")


def trim(s):
    """3 s.f. without trailing zeros after the point: 0.0250 -> 0.025, 20.0 -> 20 (only for calculated answers)"""
    return _TZ.sub(lambda m: m.group(1) or m.group(2), s)


def nq(q, val, wrongs, unit, e, sf=3, keep=False):
    """numeric item (3 s.f.; trailing zeros dropped unless keep=True); None if fewer than 3 different wrong values"""
    it = uk_alsci.nq(q, val, wrongs, unit, e, sf)
    if it is None or keep:
        return it
    c = [trim(x) for x in it["c"]]
    if len({x.lower() for x in c}) < 4:
        return None
    it["c"] = c
    it["e"] = trim(it["e"])
    return it


def fx(v, d=2):
    return "%.*f" % (d, v)


def rows(R, rs, fwd, back=None, extra=()):
    """two-way fact table maker: rs = [(a, b) or (a, b, why)]; wrong answers are the other rows' values (+ extra)"""
    rs = [r if len(r) == 3 else (r[0], r[1], "") for r in rs]

    def f():
        a, b, e = R.choice(rs)
        if back and R.random() < 0.5:
            others = sorted({x for x, y, _ in rs if y != b})
            if len(others) < 3:
                return None
            return tq(back % b, a, R.sample(others, 3), e or "%s: %s." % (a[0].upper() + a[1:], b.rstrip(".")))
        others = sorted(({y for x, y, _ in rs if y != b} | set(extra)) - {b})
        if len(others) < 3:
            return None
        return tq(fwd % a, b, R.sample(others, 3), e or "%s: %s." % (a[0].upper() + a[1:], b.rstrip(".")))
    return f


def pool(R, rs):
    """a maker that returns a random hand-written row (q, a, [w, w, w], e); the unit drops repeats"""
    its = [item(*r) for r in rs]

    def f():
        import copy
        return copy.deepcopy(R.choice(its))
    f.n = len(its)
    return f


from sci_common import svg_wrap, text, line, GRAY, INK, BLUE, RED, GREEN  # noqa: E402


def graph(pts, xmax, ymax, xstep, ystep, xlab, ylab, label="graph", W=420, H=260, marks=()):
    """line graph through pts [(x, y)] on a grid; marks: [(x, 'A')] letters above the line at x."""
    L, B, Tp, Rt = 58, 44, 16, 16
    gw, gh = W - L - Rt, H - B - Tp
    X = lambda x: L + gw * x / xmax
    Y = lambda y: Tp + gh - gh * y / ymax
    s = []
    k = 0
    while k * xstep <= xmax + 1e-9:
        x = k * xstep
        s.append(line(X(x), Tp, X(x), Tp + gh, col="#ddd", w=1))
        s.append(text(X(x), Tp + gh + 17, trim_num(x), fs=12, weight=400))
        k += 1
    k = 0
    while k * ystep <= ymax + 1e-9:
        y = k * ystep
        s.append(line(L, Y(y), L + gw, Y(y), col="#ddd", w=1))
        s.append(text(L - 6, Y(y) + 4, trim_num(y), fs=12, anchor="end", weight=400))
        k += 1
    s.append(line(L, Tp + gh, L + gw, Tp + gh, w=2) + line(L, Tp, L, Tp + gh, w=2))
    s.append(text(L + gw / 2, H - 6, xlab, fs=13, weight=400))
    s.append("<text x='14' y='%.1f' font-size='13' text-anchor='middle' fill='%s' transform='rotate(-90 14 %.1f)'>%s</text>" % (Tp + gh / 2, INK, Tp + gh / 2, ylab))
    s.append("<polyline points='%s' fill='none' stroke='%s' stroke-width='3'/>" % (" ".join("%.1f,%.1f" % (X(x), Y(y)) for x, y in pts), BLUE))
    for x, lab in marks:
        for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
            if x1 <= x <= x2:
                y = y1 + (y2 - y1) * (x - x1) / (x2 - x1) if x2 != x1 else max(y1, y2)
                s.append(text(X(x), Y(y) - 9, lab, fs=14, col=RED))
                break
    return svg_wrap(W, H, "".join(s), label).replace("<svg ", "<svg data-pf='lg' ", 1)


def trim_num(x):
    return ("%d" % x) if float(x).is_integer() else trim("%.2f" % x)


def keep(f, pred):
    """wrap maker f: drop items for which pred(item) is false"""
    def g():
        it = f()
        return it if it and pred(it) else None
    g.__name__ = getattr(f, "__name__", "g")
    return g


def ans_num(it):
    """the number at the start of the correct answer (or None)"""
    m = re.match(r"\s*[−-]?[\d.]+", it["c"][0].replace(" ", "").replace(",", ""))
    return float(m.group(0).replace("−", "-")) if m else None


def ex(x):
    """exact number for question data: 15750 -> 15750 (page shows 15 750), 0.25 -> 0.25, 2.0 -> 2"""
    if isinstance(x, float) and x.is_integer():
        x = int(x)
    if isinstance(x, int):
        return str(x)
    return trim("%.6f" % x)
