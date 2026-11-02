# -*- coding: utf-8 -*-
"""
UK Year 5 Maths: Converting Units (National Curriculum in England, Year 5: Measurement)
  python3 tools/gen_uk_maths_y5_converting_units.py
HTML attributes use single quotes (no backslashes in the JSON).
British English, metric units, plus the Year 5 imperial approximations
(1 inch ≈ 2.5 cm, 1 foot ≈ 30 cm, 1 kg ≈ 2.2 lb, 1 pint ≈ 570 ml).
Every correct answer is checked in code: each measurement string is parsed back to a base unit.
Imperial units are stored as exactly the "about" value, so "about" answers can be checked too.
"""
import json, math, os, random, re
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "uk", "maths", "year-5")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
FILL2 = "#eef6f0"
RED = "#c0392b"
INK = "#2b2b2b"
GRID = "#c9ddd0"
WATER = "#9fd3f2"
WATER_LINE = "#2a7fb8"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Amelia", "Isla", "Freya", "Poppy", "Ava", "Aisha", "Lily", "Zara", "Grace", "Ruby", "Maya", "Evie"]
BOYS = ["Oliver", "Harry", "Mohammed", "Jack", "Arjun", "Noah", "George", "Leo", "Alfie", "Kai", "Ethan", "Charlie"]


# ------------------------------------------------------------ units and checking
# unit: (family, size in the base unit, singular word, plural word)
UNIT = {
    "mm": ("L", 1, "millimetre", "millimetres"), "cm": ("L", 10, "centimetre", "centimetres"),
    "m": ("L", 1000, "metre", "metres"), "km": ("L", 1000000, "kilometre", "kilometres"),
    "inch": ("L", 25, "inch", "inches"), "foot": ("L", 300, "foot", "feet"),   # 1 inch ≈ 2.5 cm, 1 foot ≈ 30 cm
    "g": ("M", 1, "gram", "grams"), "kg": ("M", 1000, "kilogram", "kilograms"),
    "lb": ("M", Fr(5000, 11), "pound", "pounds"),                              # 1 kg ≈ 2.2 lb
    "ml": ("C", 1, "millilitre", "millilitres"), "l": ("C", 1000, "litre", "litres"),
    "pint": ("C", 570, "pint", "pints"),                                       # 1 pint ≈ 570 ml
    "second": ("T", 1, "second", "seconds"), "minute": ("T", 60, "minute", "minutes"),
    "hour": ("T", 3600, "hour", "hours"), "day": ("T", 86400, "day", "days"),
    "week": ("T", 604800, "week", "weeks"),
    "month": ("Y", 1, "month", "months"), "year": ("Y", 12, "year", "years"),
}
WORDU = {"second", "minute", "hour", "day", "week", "month", "year", "inch", "foot", "pint"}
ALIAS = {}
for _k, (_fam, _sz, _s, _p) in UNIT.items():
    ALIAS[_k] = _k
    if _k in WORDU:
        ALIAS[_s] = _k
        ALIAS[_p] = _k
TOK = re.compile(r"([\d,]+(?:\.\d+)?)\s*(" + "|".join(sorted(ALIAS, key=len, reverse=True)) + r")(?![a-z])")


def parse(s):
    """'2 kg 30 g' -> ('M', 2030). Returns None if the string is not a plain measurement."""
    s = re.sub(r"^about ", "", s.strip())
    pos, fam, tot = 0, None, Fr(0)
    for mt in TOK.finditer(s):
        if s[pos:mt.start()].strip():
            return None
        u = ALIAS[mt.group(2)]
        fu, sz = UNIT[u][0], UNIT[u][1]
        if fam and fu != fam:
            return None
        fam = fu
        tot += Fr(mt.group(1).replace(",", "")) * sz
        pos = mt.end()
    if fam is None or s[pos:].strip():
        return None
    return fam, tot


def truth(st):
    """'3 km > 2,900 m' -> True/False (chains like a < b < c allowed)."""
    parts = re.split(r" (<|>|=) ", st)
    vals = [parse(p) for p in parts[0::2]]
    assert all(vals) and len({v[0] for v in vals}) == 1, st
    ok = True
    for i, op in enumerate(parts[1::2]):
        a, b = vals[i][1], vals[i + 1][1]
        ok = ok and {"<": a < b, ">": a > b, "=": a == b}[op]
    return ok


def fmt(x):
    """Fraction/int -> '4,536' or '2.375' (exact, at most 3 decimal places)."""
    x = Fr(x)
    assert (x * 1000).denominator == 1, x
    if x.denominator == 1:
        return "{:,}".format(x.numerator)
    s = "%.3f" % float(x)
    s = s.rstrip("0").rstrip(".")
    a, _, b = s.partition(".")
    return "{:,}".format(int(a)) + "." + b


def m(n, u):
    """'4,000 m', '3 hours', '1 minute', '40 miles'."""
    if u in WORDU:
        return "%s %s" % (fmt(n), UNIT[u][2] if Fr(n) == 1 else UNIT[u][3])
    return "%s %s" % (fmt(n), u)


def mix(a, ua, b, ub):
    return m(a, ua) + " " + m(b, ub)


def word(u, n=2):
    return UNIT[u][2] if n == 1 else UNIT[u][3]


def D(s):
    return Fr(s)


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e, rnd, want=None):
    """4 choices: correct + 3 unique distractors. If the choices are measurements, their values must differ.
    want = (family, value in base unit) checks the correct answer."""
    correct = str(correct)
    if want is not None:
        assert parse(correct) == (want[0], Fr(want[1])), (q, correct, want, parse(correct))
    seen = {correct}
    vals = set()
    pc = parse(correct)
    if pc:
        vals.add(pc[1])
    pick = []
    for c in cands:
        c = str(c)
        lead = c.split(" ")[0].lstrip("£")
        if c in seen or not c or lead.startswith("-") or lead in ("0", "0p"):
            continue
        pv = parse(c)
        if pc and pv and pv[0] == pc[0]:
            if pv[1] in vals:
                continue
            vals.add(pv[1])
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    ch = pick + [correct]
    rnd.shuffle(ch)
    return {"q": q, "c": ch, "a": ch.index(correct), "e": e}


class People:
    def __init__(self, rnd):
        self.pool = [(n, "she", "her") for n in GIRLS] + [(n, "he", "his") for n in BOYS]
        rnd.shuffle(self.pool)
        self.i = 0

    def next(self):
        p = self.pool[self.i % len(self.pool)]
        self.i += 1
        return p


def cap(s):
    return s[0].upper() + s[1:]


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def text(x, y, t, fs=17, anchor="middle", bold=True, col=INK):
    return ("<text x='%.1f' y='%.1f' font-size='%d'%s fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, " font-weight='700'" if bold else "", col, anchor, t))


def frac(a, b):
    return "<span class='fr'><span class='fn'>%d</span><span class='fd'>%d</span></span>" % (a, b)


def tw(s, fs):
    return sum(0.33 if ch in ",." else 0.6 for ch in s) * fs


# ------------------------------------------------------------ conversion explanations
def k_between(uf, ut):
    return Fr(UNIT[uf][1], UNIT[ut][1])


def places(k):
    return {10: "1 place", 100: "2 places", 1000: "3 places"}.get(k)


def conv_e(n, uf, ut):
    """Explanation for n uf -> ut (one step, metric or time)."""
    k = k_between(uf, ut)
    r = Fr(n) * k
    if k > 1:
        k = int(k)
        s = "%s. %s are bigger than %s, so multiply by %s: %s × %s = %s." % (
            "%s = %s" % (m(1, uf), m(k, ut)), cap(word(uf)), word(ut), fmt(k), fmt(n), fmt(k), fmt(r))
        if places(k):
            s += " The digits move %s to the left." % places(k)
    else:
        k = int(1 / k)
        s = "%s. %s are smaller than %s, so divide by %s: %s ÷ %s = %s." % (
            "%s = %s" % (m(1, ut), m(k, uf)), cap(word(uf)), word(ut), fmt(k), fmt(n), fmt(k), fmt(r))
        if places(k):
            s += " The digits move %s to the right." % places(k)
    return s + " So %s = %s." % (m(n, uf), m(r, ut))


def conv(n, uf, ut, wrong, rnd, q=None, e=None, extra=""):
    """Convert n uf into ut. wrong = numbers in ut from real mistakes."""
    n = Fr(n)
    fam = UNIT[uf][0]
    r = n * k_between(uf, ut)
    if q is None:
        q = "Convert. <b>%s = ☐ %s</b>" % (m(n, uf), ut if ut not in WORDU else word(ut))
    return mcq(q, m(r, ut), [m(Fr(w), ut) for w in wrong], (e or conv_e(n, uf, ut)) + extra, rnd,
               want=(fam, n * UNIT[uf][1]))


# ------------------------------------------------------------ figures
def ruler_svg(s_mm, e_mm, ncm=9):
    """Ruler from 0 to ncm cm with mm marks and a pencil from s_mm to e_mm (exact)."""
    PX = 38.0
    X0, YR, RH = 18, 40, 50
    W = int(X0 * 2 + PX * ncm + 26)
    H = YR + RH + 4
    X = lambda mm: X0 + PX * mm / 10.0
    o = []
    a, b = X(s_mm), X(e_mm)
    tip = min(22, (b - a) * 0.3)
    o.append("<rect x='%.1f' y='12' width='%.1f' height='20' fill='#f4c542' stroke='%s' stroke-width='1.5'/>"
             % (a, b - a - tip, INK))
    o.append("<rect x='%.1f' y='12' width='8' height='20' fill='#e98aa0' stroke='%s' stroke-width='1.5'/>" % (a, INK))
    o.append("<path d='M%.1f 12 L%.1f 22 L%.1f 32 Z' fill='#f6e7b8' stroke='%s' stroke-width='1.5' stroke-linejoin='round'/>"
             % (b - tip, b, b - tip, INK))
    o.append("<path d='M%.1f 19.5 L%.1f 22 L%.1f 24.5 Z' fill='%s'/>" % (b - tip * 0.25, b, b - tip * 0.25, INK))
    for x in (a, b):
        o.append("<line x1='%.1f' y1='32' x2='%.1f' y2='%d' stroke='%s' stroke-width='1.2' stroke-dasharray='3 2'/>"
                 % (x, x, YR, RED))
    o.append("<rect x='4' y='%d' width='%d' height='%d' rx='3' fill='#f6e7b8' stroke='%s' stroke-width='2'/>"
             % (YR, W - 8, RH, INK))
    small, big = [], []
    for i in range(ncm * 10 + 1):
        x = X(i)
        ln = 18 if i % 10 == 0 else (12 if i % 5 == 0 else 7)
        (big if i % 10 == 0 else small).append("M%.1f %dL%.1f %d" % (x, YR, x, YR + ln))
    o.append("<path d='%s' stroke='%s' stroke-width='1'/>" % ("".join(small), INK))
    o.append("<path d='%s' stroke='%s' stroke-width='2'/>" % ("".join(big), INK))
    for c in range(ncm + 1):
        o.append(text(X(c * 10), YR + 38, str(c), 15))
    o.append(text(X(ncm * 10) + 12, YR + 38, "cm", 15, anchor="start", bold=False))
    return svg_wrap(W, H, "".join(o), "ruler with a pencil from %d mm to %d mm" % (s_mm, e_mm))


def dial_svg(v, mx, lab, tick, unit, div=1, size=200):
    """Round scale, values in grams. Labels every `lab` g shown as val/div. Needle exactly at v."""
    c = size / 2.0
    R = c - 6

    def pt(val, r):
        a = math.radians(-135 + 270.0 * val / mx)
        return c + r * math.sin(a), c - r * math.cos(a)
    s = ["<circle cx='%.1f' cy='%.1f' r='%.1f' fill='#fff' stroke='%s' stroke-width='6'/>" % (c, c, R, GREEN)]
    small, big = [], []
    for i in range(mx // tick + 1):
        val = i * tick
        major = val % lab == 0
        x1, y1 = pt(val, R - (17 if major else 10))
        x2, y2 = pt(val, R - 4)
        (big if major else small).append("M%.1f %.1fL%.1f %.1f" % (x1, y1, x2, y2))
    s.append("<path d='%s' stroke='%s' stroke-width='1.6'/>" % ("".join(small), INK))
    s.append("<path d='%s' stroke='%s' stroke-width='3'/>" % ("".join(big), INK))
    nx, ny = pt(v, R - 9)
    s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='3.5' stroke-linecap='round'/>"
             % (c, c, nx, ny, RED))
    s.append("<g font-size='%d' font-weight='700' fill='%s' text-anchor='middle' stroke='#fff' stroke-width='4' "
             "paint-order='stroke'>" % (15 if mx // div >= 1000 else 17, INK))
    for val in range(0, mx + 1, lab):
        x, y = pt(val, R - 36)
        s.append("<text x='%.1f' y='%.1f'>%s</text>" % (x, y + 6, fmt(Fr(val, div))))
    s.append("</g>")
    s.append("<circle cx='%.1f' cy='%.1f' r='7' fill='%s'/>" % (c, c, RED))
    s.append("<text x='%.1f' y='%.1f' font-size='22' font-weight='800' fill='%s' text-anchor='middle'>%s</text>"
             % (c, c + 62, GREEN, unit))
    return svg_wrap(size, size, "".join(s), "weighing scale with the needle at %s g" % fmt(v))


def jug_svg(v, mx, lab, step, size=200):
    """Measuring jug in ml: a line every `step` ml, a label every `lab` ml. Water exactly at v."""
    x0, x1 = 92, 168
    yb, yt = 186, 34

    def Y(val):
        return yb - (yb - yt) * float(val) / mx
    s = []
    s.append("<path d='M%d %d C%d %d %d %d %d %d' fill='none' stroke='%s' stroke-width='6'/>"
             % (x1, 50, x1 + 28, 50, x1 + 28, 124, x1, 124, INK))
    s.append("<rect x='%d' y='%.1f' width='%d' height='%.1f' fill='%s'/>" % (x0, Y(v), x1 - x0, yb - Y(v), WATER))
    s.append("<line x1='%d' y1='%.1f' x2='%d' y2='%.1f' stroke='%s' stroke-width='2.5'/>" % (x0, Y(v), x1, Y(v), WATER_LINE))
    s.append("<path d='M%d %d L%d %d L%d %d Q%d %d %d %d L%d %d Q%d %d %d %d L%d %d' fill='none' stroke='%s' "
             "stroke-width='4' stroke-linejoin='round'/>"
             % (x0 - 8, 14, x0, 22, x0, yb - 4, x0, yb, x0 + 6, yb, x1 - 6, yb, x1, yb, x1, yb - 4, x1, 16, INK))
    s.append("<g font-size='15' font-weight='700' fill='%s' text-anchor='end'>" % INK)
    for val in range(step, mx + 1, step):
        major = val % lab == 0
        s.append("<line x1='%d' y1='%.1f' x2='%d' y2='%.1f' stroke='%s' stroke-width='%s'/>"
                 % (x0, Y(val), x0 + (22 if major else 12), Y(val), INK, "2.6" if major else "1.6"))
        if major:
            s.append("<text x='%d' y='%.1f'>%s</text>" % (x0 - 7, Y(val) + 5, fmt(val)))
    s.append("</g>")
    s.append(text(x0 - 7, 198, "ml", 15, anchor="end", col=GREEN))
    return svg_wrap(size, size + 6, "".join(s), "measuring jug with water at %s ml" % fmt(v))


def ladder_svg(units, factors, label):
    """Boxes big -> small with × above and ÷ below the arrows."""
    BW, GAP, BH = 64, 86, 44
    W = 8 + len(units) * BW + (len(units) - 1) * GAP + 8
    H = 120
    o = []
    for i, u in enumerate(units):
        x = 8 + i * (BW + GAP)
        o.append("<rect x='%d' y='38' width='%d' height='%d' rx='8' fill='%s' stroke='%s' stroke-width='2.5'/>"
                 % (x, BW, BH, FILL, GREEN))
        o.append(text(x + BW / 2, 38 + BH / 2 + 7, u, 20))
        if i < len(units) - 1:
            a, b = x + BW + 6, x + BW + GAP - 6
            o.append("<path d='M%d 48 L%d 48 M%d 42 L%d 48 L%d 54' fill='none' stroke='%s' stroke-width='2.5'/>"
                     % (a, b, b - 7, b, b - 7, GREEN))
            o.append(text((a + b) / 2, 34, "× " + factors[i], 16, col=GREEN))
            o.append("<path d='M%d 72 L%d 72 M%d 66 L%d 72 L%d 78' fill='none' stroke='%s' stroke-width='2.5'/>"
                     % (b, a, a + 7, a, a + 7, RED))
            o.append(text((a + b) / 2, 100, "÷ " + factors[i], 16, col=RED))
    return svg_wrap(W, H, "".join(o), label)


def inch_ruler_svg(mark_in=None, n_in=5, ncm=13):
    """Ruler drawn to true scale (1 inch = 2.54 cm): inches along the top, centimetres along the bottom.
    A red line marks mark_in inches. Labels have a halo so the red line never hides them."""
    PX = 30.0                      # pixels per cm
    X0, YT, YB = 18, 34, 124
    XC = lambda cm: X0 + PX * cm
    XI = lambda inch: X0 + PX * 2.54 * inch
    XU = XC(ncm) + 16              # unit words start here
    W = int(XU + tw("inches", 14) + 14)
    H = YB + 8
    o = ["<rect x='4' y='%d' width='%d' height='%d' rx='3' fill='#f6e7b8' stroke='%s' stroke-width='2'/>"
         % (YT, W - 8, YB - YT, INK)]
    small, big = [], []
    for i in range(n_in * 4 + 1):
        x = XI(i / 4.0)
        ln = 20 if i % 4 == 0 else (13 if i % 2 == 0 else 8)
        (big if i % 4 == 0 else small).append("M%.1f %dL%.1f %d" % (x, YT, x, YT + ln))
    for i in range(ncm * 10 + 1):
        x = XC(i / 10.0)
        ln = 18 if i % 10 == 0 else (11 if i % 5 == 0 else 6)
        (big if i % 10 == 0 else small).append("M%.1f %dL%.1f %d" % (x, YB, x, YB - ln))
    o.append("<path d='%s' stroke='%s' stroke-width='1'/>" % ("".join(small), INK))
    o.append("<path d='%s' stroke='%s' stroke-width='2'/>" % ("".join(big), INK))
    if mark_in is not None:
        x = XI(mark_in)
        o.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='2.5'/>" % (x, YT - 12, x, YB + 6, RED))
        o.append("<path d='M%.1f %d l-6 -10 h12 z' fill='%s'/>" % (x, YT - 2, RED))
    o.append("<g fill='%s' text-anchor='middle' stroke='#f6e7b8' stroke-width='5' paint-order='stroke'>" % INK)
    for i in range(n_in + 1):
        o.append("<text x='%.1f' y='%d' font-size='15' font-weight='700'>%d</text>" % (XI(i), YT + 37, i))
    for c in range(ncm + 1):
        o.append("<text x='%.1f' y='%d' font-size='14'>%d</text>" % (XC(c), YB - 24, c))
    o.append("</g>")
    o.append(text(XU, YT + 37, "inches", 14, anchor="start", col=GREEN))
    o.append(text(XU, YB - 24, "cm", 14, anchor="start", col=GREEN))
    lab = "ruler with inches and centimetres" + ("" if mark_in is None else ", marked at %s inches" % mark_in)
    return svg_wrap(W, H, "".join(o), lab)


def ab(n, u):
    return "about " + m(n, u)


# ------------------------------------------------------------ set 1: length
def set_length(rnd):
    its = []
    L = lambda v: ("L", v)
    its.append(conv(3, "km", "m", [300, 30, D("0.003")], rnd,
                    extra=" (300 m would mean 1 km = 100 m.)"))
    its.append(conv(5000, "m", "km", [50, 500, 5000000], rnd))
    its.append(conv(4, "m", "cm", [40, 4000, D("0.04")], rnd))
    its.append(conv(600, "cm", "m", [60, D("0.6"), 60000], rnd))
    its.append(conv(8, "cm", "mm", [800, D("0.8"), 8], rnd))
    its.append(conv(D("2.4"), "km", "m", [240, 24, 2004], rnd,
                    extra=" (240 m multiplies by 100, not 1,000.)"))
    its.append(conv(350, "m", "km", [D("3.5"), 35, 350000], rnd))
    its.append(conv(D("1.5"), "m", "cm", [15, 1500, 105], rnd))
    its.append(conv(D("3.7"), "cm", "mm", [370, D("0.37"), 307], rnd))
    its.append(conv(85, "mm", "cm", [850, D("0.85"), D("0.085")], rnd))
    its.append(conv(D("0.75"), "km", "m", [75, D("7.5"), 7500], rnd))
    its.append(conv(125, "cm", "m", [D("12.5"), D("0.125"), 12500], rnd))
    its.append(conv(2050, "m", "km", [D("2.5"), D("20.5"), D("2.005")], rnd,
                    extra=" The 0 in 2,050 keeps its place: 2.05, not 2.5."))
    its.append(conv(D("4.06"), "m", "cm", [460, D("40.6"), 4060], rnd,
                    extra=" (460 cm would be 4.6 m.)"))
    q = fig(ruler_svg(20, 94)) + "How long is the pencil in centimetres?"
    its.append(mcq(q, "7.4 cm", ["9.4 cm", "74 cm", "7.04 cm"],
                   "The pencil starts at 2 cm, not 0. It ends 4 small marks after 9 cm, at 9.4 cm. "
                   "9.4 − 2 = 7.4 cm (74 mm). 9.4 cm forgets that the pencil does not start at 0.", rnd, want=L(74)))
    its.append(mcq("Convert. <b>3 km 400 m = ☐ km</b>", "3.4 km", ["3.04 km", "34 km", "3.004 km"],
                   "400 m = 400 ÷ 1,000 = 0.4 km. So 3 km 400 m = 3 + 0.4 = 3.4 km. 3.04 km would be 3 km 40 m.",
                   rnd, want=L(3400000)))
    its.append(mcq("Which is the same as <b>1.08 m</b>?", "1 m 8 cm", ["1 m 80 cm", "1 m 8 mm", "108 mm"],
                   "1.08 m = 1 m and 0.08 m. 0.08 m = 0.08 × 100 = 8 cm. So 1.08 m = 1 m 8 cm. "
                   "1 m 80 cm would be 1.8 m.", rnd, want=L(1080)))
    ch = ["0.65 km", "0.6 km", "580 m", "6,500 cm"]
    assert [parse(c)[1] / 1000 for c in ch] == [650, 600, 580, 65]
    its.append(mcq("Which is the longest?", ch[0], ch[1:],
                   "Change them all to metres: 0.65 km = 650 m, 0.6 km = 600 m and 6,500 cm = 65 m. "
                   "650 m is the longest. 6,500 has the biggest number, but centimetres are small.", rnd))
    sts = ["250 cm = 2.5 m", "3.5 km = 350 m", "60 mm = 0.6 cm", "0.4 m = 4 cm"]
    assert [truth(s) for s in sts] == [True, False, False, False]
    its.append(mcq("Which is true?", sts[0], sts[1:],
                   "250 ÷ 100 = 2.5, so 250 cm = 2.5 m. The others are wrong: 3.5 km = 3,500 m, "
                   "60 mm = 6 cm and 0.4 m = 40 cm.", rnd))
    its.append(mcq("Find the missing number. <b>1 m − 35 cm = ☐ m</b>", "0.65 m", ["0.75 m", "0.35 m", "65 m"],
                   "1 m = 100 cm. 100 − 35 = 65 cm. 65 ÷ 100 = 0.65 m. "
                   "Take care when you exchange: 100 − 35 is 65, not 75.", rnd, want=L(650)))
    assert len(its) == 20, len(its)
    return {"title": "Length: mm, cm, m and km with decimals", "items": its}


# ------------------------------------------------------------ set 2: mass and capacity
def set_mass_cap(rnd):
    its = []
    its.append(conv(4, "kg", "g", [400, 40, D("0.004")], rnd))
    its.append(conv(6000, "ml", "l", [60, 600, 6000000], rnd))
    its.append(conv(D("2.5"), "kg", "g", [250, 25, 2005], rnd))
    its.append(conv(D("1.5"), "l", "ml", [150, 15, 1005], rnd))
    its.append(conv(350, "g", "kg", [D("3.5"), 35, 350000], rnd,
                    extra=" Check: 0.35 kg is a bit more than a quarter of a kilogram."))
    its.append(conv(750, "ml", "l", [D("7.5"), 75, D("0.075")], rnd))
    its.append(conv(D("0.25"), "kg", "g", [25, D("2.5"), 2500], rnd))
    its.append(conv(D("3.2"), "l", "ml", [320, 32, 3002], rnd))
    its.append(conv(80, "g", "kg", [D("0.8"), 8, 80000], rnd,
                    extra=" You need a 0 in the tenths place."))
    its.append(conv(1250, "ml", "l", [D("12.5"), D("0.125"), D("1.025")], rnd))
    its.append(mcq("Convert. <b>2 kg 50 g = ☐ kg</b>", "2.05 kg", ["2.5 kg", "2.005 kg", "20.5 kg"],
                   "50 g = 50 ÷ 1,000 = 0.05 kg. So 2 kg 50 g = 2.05 kg. 2.5 kg would be 2 kg 500 g.",
                   rnd, want=("M", 2050)))
    its.append(mcq("Work out <b>1.2 l + 600 ml</b>. Give your answer in litres.", "1.8 l",
                   ["601.2 l", "7.2 l", "1.26 l"],
                   "Use one unit first: 600 ml = 0.6 l. Then 1.2 + 0.6 = 1.8 l. "
                   "601.2 l adds the numbers without converting.", rnd, want=("C", 1800)))
    ch = ["1 kg 600 g", "1.5 kg", "1,450 g", "0.95 kg"]
    assert [parse(c)[1] for c in ch] == [1600, 1500, 1450, 950]
    its.append(mcq("Which is the heaviest?", ch[0], ch[1:],
                   "Change them all to grams: 1 kg 600 g = 1,600 g, 1.5 kg = 1,500 g and 0.95 kg = 950 g. "
                   "1,600 g is the heaviest.", rnd))
    sts = ["0.3 l < 450 ml < 0.5 l", "0.5 l < 450 ml < 0.3 l", "450 ml < 0.3 l < 0.5 l", "0.3 l < 0.5 l < 450 ml"]
    assert [truth(s) for s in sts] == [True, False, False, False]
    its.append(mcq("Which list goes from the smallest to the largest capacity?", sts[0], sts[1:],
                   "Change them all to millilitres: 0.3 l = 300 ml and 0.5 l = 500 ml. 300 &lt; 450 &lt; 500.", rnd))
    # scales
    q = fig(dial_svg(750, 1000, 200, 50, "g")) + "The scale shows the mass of some carrots. What is the mass in kilograms?"
    its.append(mcq(q, "0.75 kg", ["0.63 kg", "7.5 kg", "0.075 kg"],
                   "The numbers go up by 200 g and there are 4 spaces, so each mark is 50 g. "
                   "The needle is 3 marks past 600 g: 600 + 150 = 750 g. 750 ÷ 1,000 = 0.75 kg. "
                   "(0.63 kg counts each mark as 10 g.)", rnd, want=("M", 750)))
    q = fig(dial_svg(2600, 4000, 1000, 200, "kg", 1000)) + "The scale shows the mass of a bag of potatoes. What is the mass in kilograms?"
    its.append(mcq(q, "2.6 kg", ["2.3 kg", "2.06 kg", "26 kg"],
                   "Each kilogram is split into 5 equal spaces, so each mark is 1 ÷ 5 = 0.2 kg (200 g). "
                   "The needle is 3 marks past 2 kg: 2 + 0.6 = 2.6 kg. (2.3 kg counts each mark as 0.1 kg.)",
                   rnd, want=("M", 2600)))
    q = fig(dial_svg(1750, 3000, 1000, 250, "kg", 1000)) + "The scale shows the mass of a parcel. What is the mass in kilograms?"
    its.append(mcq(q, "1.75 kg", ["1.3 kg", "1.075 kg", "17.5 kg"],
                   "Each kilogram is split into 4 equal spaces, so each mark is 1 ÷ 4 = 0.25 kg (250 g). "
                   "The needle is 3 marks past 1 kg: 1 + 0.75 = 1.75 kg. (1.3 kg counts each mark as 0.1 kg.)",
                   rnd, want=("M", 1750)))
    q = fig(jug_svg(850, 1000, 250, 50)) + "How much water is in the jug? Give your answer in litres."
    its.append(mcq(q, "0.85 l", ["0.77 l", "8.5 l", "0.085 l"],
                   "The numbers go up by 250 ml and there are 5 spaces, so each line is 50 ml. "
                   "The water is 2 lines above 750 ml: 750 + 100 = 850 ml. 850 ÷ 1,000 = 0.85 l. "
                   "(0.77 l counts each line as 10 ml.)", rnd, want=("C", 850)))
    q = fig(jug_svg(1300, 2000, 500, 100)) + "How much water is in the jug? Give your answer in litres."
    its.append(mcq(q, "1.3 l", ["1.15 l", "13 l", "1.03 l"],
                   "The numbers go up by 500 ml and there are 5 spaces, so each line is 100 ml. "
                   "The water is 3 lines above 1,000 ml: 1,300 ml. 1,300 ÷ 1,000 = 1.3 l. "
                   "(1.15 l counts each line as 50 ml.)", rnd, want=("C", 1300)))
    q = fig(jug_svg(1200, 2000, 500, 100)) + "How much more water is needed to fill the jug to 2 litres?"
    its.append(mcq(q, "800 ml", ["1,200 ml", "80 ml", "8 l"],
                   "Each line is 100 ml. The water is at 1,200 ml. 2 litres = 2,000 ml. "
                   "2,000 − 1,200 = 800 ml more. (1,200 ml is the water already in the jug.)", rnd, want=("C", 800)))
    assert len(its) == 20, len(its)
    return {"title": "Mass and capacity: g, kg, ml and l", "items": its}


# ------------------------------------------------------------ set 3: imperial units
def set_imperial(rnd):
    its = []
    L = lambda v: ("L", v)
    IN = "1 inch is about 2.5 cm. "
    FT = "1 foot is about 30 cm. "
    LB = "1 kg is about 2.2 pounds (lb). "
    PT = "1 pint is about 570 ml. "
    its.append(mcq("About how many centimetres are the same as <b>1 inch</b>?", ab(D("2.5"), "cm"),
                   [ab(25, "cm"), ab(12, "cm"), ab(10, "cm")],
                   "This is the fact to learn: 1 inch ≈ 2.5 cm. An inch is about the width of an adult’s thumb. "
                   "(12 is the number of inches in 1 foot.)", rnd, want=L(25)))
    its.append(mcq("About how many centimetres are the same as <b>1 foot</b>?", ab(30, "cm"),
                   [ab(12, "cm"), ab(100, "cm"), ab(3, "cm")],
                   "This is the fact to learn: 1 foot ≈ 30 cm, about the length of a school ruler. "
                   "1 foot = 12 inches, and 12 × 2.5 = 30. (100 cm is 1 metre.)", rnd, want=L(300)))
    its.append(mcq("About how many pounds (lb) are the same as <b>1 kg</b>?", ab(D("2.2"), "lb"),
                   [ab(1000, "lb"), ab(22, "lb"), ab(D("0.45"), "lb")],
                   "This is the fact to learn: 1 kg ≈ 2.2 lb. A pound is a bit less than half a kilogram, "
                   "so there are more pounds than kilograms. (1 kg = 1,000 g, not 1,000 lb.)", rnd, want=("M", 1000)))
    its.append(mcq("About how many millilitres are the same as <b>1 pint</b>?", ab(570, "ml"),
                   [ab(1000, "ml"), ab(57, "ml"), ab(5700, "ml")],
                   "This is the fact to learn: 1 pint ≈ 570 ml, which is just over half a litre. "
                   "(1,000 ml is 1 litre, not 1 pint.)", rnd, want=("C", 570)))
    its.append(mcq("A bottle holds 1 pint of milk. Which is closest to its capacity?", "just over half a litre",
                   ["about 1 litre", "about 2 litres", "about a quarter of a litre"],
                   PT + "Half a litre is 500 ml, so 570 ml is just over half a litre.", rnd))
    q = fig(inch_ruler_svg(4)) + "The ruler shows inches and centimetres. About how many centimetres are the same as 4 inches?"
    its.append(mcq(q, ab(10, "cm"), [ab(4, "cm"), ab(D("6.5"), "cm"), ab(40, "cm")],
                   "Follow the red line from 4 inches down to the centimetres: it is just past 10 cm. "
                   "Or work it out: " + IN + "4 × 2.5 = 10, so 4 inches ≈ 10 cm. (6.5 cm adds 4 + 2.5.)",
                   rnd, want=L(100)))
    its.append(mcq("About how many centimetres are the same as <b>12 inches</b>?", ab(30, "cm"),
                   [ab(D("4.8"), "cm"), ab(D("14.5"), "cm"), ab(120, "cm")],
                   IN + "Inches are bigger than centimetres, so multiply: 12 × 2.5 = 30 cm. "
                   "12 inches is 1 foot, which is about 30 cm. (4.8 cm divides instead.)", rnd, want=L(300)))
    its.append(mcq("About how many inches are the same as <b>20 cm</b>?", ab(8, "inch"),
                   [ab(50, "inch"), ab(D("17.5"), "inch"), ab(2, "inch")],
                   IN + "Centimetres are smaller, so divide: 20 ÷ 2.5 = 8 inches. Check: 8 × 2.5 = 20. "
                   "(50 inches multiplies instead.)", rnd, want=L(200)))
    its.append(mcq("About how many centimetres are the same as <b>3 feet</b>?", ab(90, "cm"),
                   [ab(10, "cm"), ab(33, "cm"), ab(36, "cm")],
                   FT + "3 × 30 = 90 cm. (36 is the number of inches in 3 feet, not centimetres.)", rnd, want=L(900)))
    its.append(mcq("About how many pounds (lb) are the same as <b>5 kg</b>?", ab(11, "lb"),
                   [ab(D("2.3"), "lb"), ab(D("7.2"), "lb"), ab(110, "lb")],
                   LB + "5 × 2.2 = 11 lb. There are more pounds than kilograms. (7.2 lb adds 5 + 2.2.)",
                   rnd, want=("M", 5000)))
    its.append(mcq("A suitcase can weigh up to <b>20 kg</b>. About how many pounds (lb) is that?", ab(44, "lb"),
                   [ab(9, "lb"), ab(D("22.2"), "lb"), ab(440, "lb")],
                   LB + "20 × 2.2 = 44 lb (2 × 22). (440 lb puts the decimal point in the wrong place.)",
                   rnd, want=("M", 20000)))
    its.append(mcq("About how many kilograms are the same as <b>22 lb</b>?", ab(10, "kg"),
                   [ab(D("48.4"), "kg"), ab(D("19.8"), "kg"), ab(D("24.2"), "kg")],
                   LB + "Pounds to kilograms: divide. 22 ÷ 2.2 = 10 kg. Check: 10 × 2.2 = 22. "
                   "(48.4 kg multiplies by 2.2 instead.)", rnd, want=("M", 10000)))
    its.append(mcq("About how many millilitres are the same as <b>2 pints</b>?", ab(1140, "ml"),
                   [ab(572, "ml"), ab(285, "ml"), ab(11400, "ml")],
                   PT + "2 × 570 = 1,140 ml. (285 ml halves 570 instead of doubling it.)", rnd, want=("C", 1140)))
    its.append(mcq("About how many litres are the same as <b>4 pints</b>?", "about 2.3 l",
                   ["about 23 l", "about 4 l", "about 0.14 l"],
                   PT + "4 × 570 = 2,280 ml. 2,280 ml = 2.28 l, which is about 2.3 litres. "
                   "(4 l treats a pint as a litre.)", rnd))
    ch = ["1 foot", "11 inches", "25 cm", "0.2 m"]
    assert [parse(c)[1] for c in ch] == [300, 275, 250, 200]
    its.append(mcq("Which is the longest?", ch[0], ch[1:],
                   "Change them all to centimetres. 1 foot ≈ 30 cm, 11 inches ≈ 11 × 2.5 = 27.5 cm, "
                   "and 0.2 m = 20 cm. 1 foot is the longest.", rnd))
    its.append(mcq("Which is heavier: a 2 kg bag of flour or a 4 lb bag of flour?", "The 2 kg bag",
                   ["The 4 lb bag", "They weigh exactly the same", "You cannot compare kg and lb"],
                   LB + "2 kg ≈ 2 × 2.2 = 4.4 lb, which is more than 4 lb. So the 2 kg bag is heavier. "
                   "4 is the bigger number, but a pound is lighter than a kilogram.", rnd))
    its.append(mcq("Which is true?", "1 foot ≈ 30 cm", ["1 inch ≈ 25 cm", "1 kg ≈ 22 lb", "1 pint ≈ 2 l"],
                   "1 foot is about 30 cm. The others are wrong: 1 inch ≈ 2.5 cm, 1 kg ≈ 2.2 lb "
                   "and 1 pint ≈ 570 ml, just over half a litre.", rnd))
    P = People(rnd)
    n, he, his = P.next()
    its.append(mcq("%s is <b>4 feet 6 inches</b> tall. About how tall is %s in centimetres?" % (n, he),
                   ab(135, "cm"), [ab(126, "cm"), ab(120, "cm"), ab(1350, "cm")],
                   "4 feet ≈ 4 × 30 = 120 cm. 6 inches ≈ 6 × 2.5 = 15 cm. 120 + 15 = 135 cm. "
                   "(126 cm adds 6 cm instead of 6 inches.)", rnd, want=L(1350)))
    n = "Freya"
    its.append(mcq("Freya’s baby brother weighed <b>6.6 lb</b> when he was born. About how much is that in kilograms?",
                   ab(3, "kg"), [ab(D("14.52"), "kg"), ab(D("4.4"), "kg"), ab(30, "kg")],
                   LB + "Pounds to kilograms: divide. 6.6 ÷ 2.2 = 3 kg. Check: 3 × 2.2 = 6.6. "
                   "(14.52 kg multiplies instead. A newborn baby is not that heavy.)", rnd, want=("M", 3000)))
    n, he, his = P.next()
    its.append(mcq("A recipe needs <b>1 pint</b> of milk. %s has a 1 litre carton. Is there enough?" % n,
                   "Yes, with about 430 ml left over",
                   ["No, %s needs about 430 ml more" % he, "Yes, with about 530 ml left over",
                    "Yes, with exactly 430 ml left over"],
                   PT + "1 litre = 1,000 ml, which is more than 570 ml. 1,000 − 570 = 430 ml left over. "
                   "It is about 430 ml, not exactly, because 1 pint ≈ 570 ml is an approximation.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Imperial units: inches, feet, pounds and pints", "items": its}


# ------------------------------------------------------------ set 4: time
def set_time(rnd):
    its = []
    T = lambda v: ("T", v)
    its.append(conv(4, "hour", "minute", [400, 64, 40], rnd,
                    e="1 hour = 60 minutes (not 100). Multiply: 4 × 60 = 240, so 4 hours = 240 minutes."))
    its.append(conv(5, "minute", "second", [500, 65, 50], rnd,
                    e="1 minute = 60 seconds. Multiply: 5 × 60 = 300, so 5 minutes = 300 seconds."))
    its.append(conv(180, "second", "minute", [D("1.8"), 18, 10800], rnd,
                    e="1 minute = 60 seconds. Seconds to minutes: divide by 60, not 100. 180 ÷ 60 = 3, because 3 × 60 = 180."))
    its.append(conv(300, "minute", "hour", [3, 30, 18000], rnd,
                    e="1 hour = 60 minutes. Minutes to hours: divide by 60. 300 ÷ 60 = 5. "
                      "(3 hours divides by 100, as if 1 hour were 100 minutes.)"))
    its.append(conv(3, "day", "hour", [27, 36, 30], rnd,
                    e="1 day = 24 hours. Multiply: 3 × 24 = 72, so 3 days = 72 hours. (36 hours uses 12 hours, which is only half a day.)"))
    its.append(conv(6, "week", "day", [60, 13, 36], rnd,
                    e="1 week = 7 days. Multiply: 6 × 7 = 42, so 6 weeks = 42 days."))
    its.append(conv(56, "day", "week", [392, D("5.6"), 49], rnd,
                    e="1 week = 7 days. Days to weeks: divide. 56 ÷ 7 = 8, so 56 days = 8 weeks."))
    its.append(conv(4, "year", "month", [40, 16, 52], rnd,
                    e="1 year = 12 months. Multiply: 4 × 12 = 48, so 4 years = 48 months. (52 is the number of weeks in a year.)"))
    its.append(conv(2, "hour", "second", [120, 12000, 200], rnd,
                    e="1 hour = 60 minutes and 1 minute = 60 seconds, so 1 hour = 60 × 60 = 3,600 seconds. "
                      "2 × 3,600 = 7,200 seconds. (120 is the number of minutes.)"))
    its.append(mcq("How many days are in a <b>leap year</b>?", "366 days", ["365 days", "364 days", "360 days"],
                   "A normal year has 365 days. A leap year has one extra day, 29 February, so it has 366 days.",
                   rnd, want=T(366 * 86400)))
    its.append(mcq("Which of these years is a leap year?", "2028", ["2025", "2026", "2030"],
                   "A leap year comes every 4 years. Leap years divide exactly by 4: 2028 ÷ 4 = 507. "
                   "2025, 2026 and 2030 do not divide exactly by 4, so they are not leap years.", rnd))
    its.append(mcq("How many days are in February in a leap year?", "29 days", ["28 days", "30 days", "31 days"],
                   "February usually has 28 days. In a leap year it has one extra day, 29 February, so it has 29 days.",
                   rnd, want=T(29 * 86400)))
    its.append(mcq("How many days are in 2 years? Neither year is a leap year.", "730 days",
                   ["720 days", "104 days", "732 days"],
                   "1 year = 365 days. 2 × 365 = 730 days. (104 is the number of weeks in 2 years, and "
                   "732 days would be 2 leap years.)", rnd, want=T(730 * 86400)))
    its.append(mcq("Convert. <b>2 hours 15 minutes = ☐ minutes</b>", "135 minutes",
                   ["215 minutes", "17 minutes", "120 minutes"],
                   "2 hours = 2 × 60 = 120 minutes. Add the 15 minutes: 120 + 15 = 135 minutes. "
                   "(215 minutes would mean 1 hour = 100 minutes.)", rnd, want=T(8100)))
    its.append(mcq("Which is the same as <b>200 seconds</b>?", "3 minutes 20 seconds",
                   ["2 minutes", "3 minutes 33 seconds", "20 minutes"],
                   "3 minutes = 180 seconds. 200 − 180 = 20, so 200 seconds = 3 minutes 20 seconds. "
                   "(2 minutes would mean 1 minute = 100 seconds.)", rnd, want=T(200)))
    its.append(mcq("Which is the same as <b>1.5 hours</b>?", "1 hour 30 minutes",
                   ["1 hour 50 minutes", "1 hour 5 minutes", "150 minutes"],
                   "0.5 hours is half an hour, and half of 60 minutes is 30 minutes. "
                   "So 1.5 hours = 1 hour 30 minutes = 90 minutes, not 1 hour 50 minutes.", rnd, want=T(5400)))
    its.append(mcq("Which is the same as <b>130 minutes</b>?", "2 hours 10 minutes",
                   ["1 hour 30 minutes", "13 hours", "1.3 hours"],
                   "120 minutes = 2 hours. 130 − 120 = 10, so 130 minutes = 2 hours 10 minutes. "
                   "1 hour 30 minutes and 1.3 hours both treat an hour as 100 minutes.", rnd, want=T(7800)))
    ch = ["110 minutes", "1.5 hours", "1 hour 45 minutes", "6,000 seconds"]
    assert [parse(c)[1] / 60 for c in ch] == [110, 90, 105, 100]
    its.append(mcq("Which is the longest time?", ch[0], ch[1:],
                   "Change them all to minutes: 1.5 hours = 90 minutes, 1 hour 45 minutes = 105 minutes and "
                   "6,000 seconds = 6,000 ÷ 60 = 100 minutes. 110 minutes is the longest.", rnd))
    sts = ["1 day = 1,440 minutes", "1 day = 2,400 minutes", "1 hour = 100 minutes", "2 days = 36 hours"]
    assert [truth(s) for s in sts] == [True, False, False, False]
    its.append(mcq("Which is true?", sts[0], sts[1:],
                   "1 day = 24 hours, and each hour is 60 minutes. 24 × 60 = 1,440, so 1 day = 1,440 minutes. "
                   "2,400 minutes uses 100 minutes in an hour.", rnd))
    its.append(mcq("Find the missing number. <b>3 minutes − 45 seconds = ☐ seconds</b>", "135 seconds",
                   ["255 seconds", "225 seconds", "145 seconds"],
                   "3 minutes = 3 × 60 = 180 seconds. 180 − 45 = 135 seconds. "
                   "(255 seconds uses 300 seconds for 3 minutes. 225 adds instead of subtracting.)", rnd, want=T(135)))
    assert len(its) == 20, len(its)
    return {"title": "Time: seconds to years and leap years", "items": its}


# ------------------------------------------------------------ set 5: word problems
def set_story(rnd):
    P = People(rnd)
    its = []

    def add(q, r, w, e, want=None):
        its.append(mcq(q, r, w, e, rnd, want=want))

    add("A recipe for 4 people uses 200 g of flour. How much flour is needed for 6 people?",
        "300 g", ["1,200 g", "202 g", "400 g"],
        "200 ÷ 4 = 50 g for each person. 6 × 50 = 300 g. (202 g adds 2 instead of scaling, "
        "and 1,200 g is 6 × 200.)", ("M", 300))
    add("A pancake recipe for 4 people uses 300 ml of milk. How many litres of milk are needed for 10 people?",
        "0.75 l", ["7.5 l", "3 l", "1.2 l"],
        "300 ÷ 4 = 75 ml for each person. 10 × 75 = 750 ml. 750 ÷ 1,000 = 0.75 l. "
        "(3 l uses 300 ml for each person.)", ("C", 750))
    n, he, his = P.next()
    add("%s’s family drinks 2 pints of milk every day. About how many litres is that in 1 week?" % n,
        "about 8 l", ["about 14 l", "about 1.1 l", "about 80 l"],
        "1 week = 7 days, so 7 × 2 = 14 pints. 1 pint ≈ 570 ml, so 14 × 570 = 7,980 ml, which is about 8 litres. "
        "(14 l treats a pint as a litre. 1.1 l is only 1 day.)")
    assert 14 * 570 == 7980
    add("A 1.5 litre bottle of water is shared equally between 6 cups. How much water goes in each cup?",
        "250 ml", ["25 ml", "9,000 ml", "0.25 ml"],
        "1.5 l = 1,500 ml. 1,500 ÷ 6 = 250 ml. Check: 6 × 250 = 1,500. (0.25 is the answer in litres, not ml.)",
        ("C", 250))
    add("Apples cost £1.20 for 1 kg. How much do 2.5 kg of apples cost?",
        "£3", ["£3.70", "£2.40", "£30"],
        "2 kg cost 2 × £1.20 = £2.40. Half a kilogram costs half of £1.20, which is 60p. £2.40 + 60p = £3. "
        "(£2.40 forgets the 0.5 kg. £3.70 adds 2.5 instead of multiplying.)")
    add("Cheese costs 90p for 100 g. How much does 0.5 kg of cheese cost?",
        "£4.50", ["45p", "£45", "£9"],
        "0.5 kg = 500 g. 500 g is 5 lots of 100 g. 5 × 90p = 450p = £4.50. "
        "(45p works out 0.5 × 90p without converting. £9 is the price of 1 kg.)")
    n, he, his = P.next()
    add("%s has 3 m of ribbon. %s cuts it into pieces 25 cm long. How many pieces does %s get?" % (n, cap(he), he),
        "12 pieces", ["75 pieces", "120 pieces", "4 pieces"],
        "3 m = 300 cm. 300 ÷ 25 = 12 pieces. (4 pieces is only 1 m. 75 pieces multiplies 3 × 25.)")
    n, he, his = P.next()
    add("One lap of the school track is 400 m. %s runs 6 laps. How far does %s run in kilometres?" % (n, he),
        "2.4 km", ["24 km", "0.24 km", "2,400 km"],
        "6 × 400 = 2,400 m. 1 km = 1,000 m, so 2,400 ÷ 1,000 = 2.4 km.", ("L", 2400000))
    n, he, his = P.next()
    add("%s walks 850 m to school. %s walks there and back every day for 5 school days. "
        "How far does %s walk in the week, in kilometres?" % (n, cap(he), he),
        "8.5 km", ["4.25 km", "85 km", "1.7 km"],
        "There and back is 2 × 850 = 1,700 m a day. 5 × 1,700 = 8,500 m. 8,500 ÷ 1,000 = 8.5 km. "
        "(4.25 km forgets the walk home. 1.7 km is only 1 day.)", ("L", 8500000))
    n, he, his = P.next()
    add("%s posts three parcels. They weigh 1.4 kg, 650 g and 2 kg. What is their total mass in kilograms?" % n,
        "4.05 kg", ["653.4 kg", "9.9 kg", "3.465 kg"],
        "Change 650 g to kilograms first: 650 ÷ 1,000 = 0.65 kg. 1.4 + 0.65 + 2 = 4.05 kg. "
        "(9.9 kg treats 650 g as 6.5 kg.)", ("M", 4050))
    add("A film lasts 135 minutes. It starts at 6:30 pm. What time does it finish?",
        "8:45 pm", ["8:05 pm", "8:15 pm", "9:05 pm"],
        "135 minutes = 120 + 15 = 2 hours 15 minutes. 6:30 pm + 2 hours = 8:30 pm, then 15 more minutes is 8:45 pm. "
        "(8:05 pm reads 135 minutes as 1 hour 35 minutes.)")
    n, he, his = P.next()
    add("%s practises the piano for 20 minutes every day for 2 weeks. How long is that altogether?" % n,
        "4 hours 40 minutes", ["2 hours 80 minutes", "28 hours", "2 hours 20 minutes"],
        "2 weeks = 14 days. 14 × 20 = 280 minutes. 4 × 60 = 240, and 280 − 240 = 40, "
        "so it is 4 hours 40 minutes. (2 hours 80 minutes uses 100 minutes in an hour. 2 hours 20 minutes is only 1 week.)",
        ("T", 280 * 60))
    n, he, his = P.next()
    add("%s’s summer holiday is 3 weeks and 4 days long. How many days is that?" % n,
        "25 days", ["34 days", "7 days", "19 days"],
        "1 week = 7 days, so 3 weeks = 21 days. 21 + 4 = 25 days. (19 days counts only 5 days in a week.)",
        ("T", 25 * 86400))
    add("A real car is 10 times as long as a model of it. The model is 42 cm long. "
        "How long is the real car in metres?",
        "4.2 m", ["42 m", "0.42 m", "420 m"],
        "The real car is 10 times as long: 42 × 10 = 420 cm. 420 ÷ 100 = 4.2 m. "
        "(420 m forgets to change centimetres to metres.)", ("L", 4200))
    add("A cake recipe for 8 people uses 1.2 kg of flour. How many grams of flour are needed for 2 people?",
        "300 g", ["600 g", "4,800 g", "30 g"],
        "2 people is a quarter of 8 people. 1.2 kg = 1,200 g. 1,200 ÷ 4 = 300 g. "
        "(600 g is enough for 4 people. 4,800 g multiplies by 4 instead of dividing.)", ("M", 300))
    n, he, his = P.next()
    add("%s’s dad is 6 feet tall. About how tall is he in metres?" % n,
        ab(D("1.8"), "m"), [ab(D("0.72"), "m"), ab(18, "m"), ab(D("0.18"), "m")],
        "1 foot ≈ 30 cm, so 6 feet ≈ 6 × 30 = 180 cm. 180 ÷ 100 = 1.8 m. "
        "(0.72 m changes 6 feet into 72 inches, then reads them as centimetres.)", ("L", 1800))
    n, he, his = P.next()
    add("%s buys 4 pints of milk. Each pint costs 65p. How much does %s pay?" % (n, he),
        "£2.60", ["£26", "69p", "£1.30"],
        "4 × 65p = 260p. 100p = £1, so 260p = £2.60. (69p adds 4 + 65. £1.30 is only 2 pints.)")
    add("A 5 kg bag of rice is shared equally into 8 smaller bags. How many grams of rice are in each bag?",
        "625 g", ["62.5 g", "1,600 g", "0.625 g"],
        "5 kg = 5,000 g. 5,000 ÷ 8 = 625 g. Check: 8 × 625 = 5,000. "
        "(0.625 is the answer in kilograms, not grams.)", ("M", 625))
    jumps = [("Oliver", "1.45 m"), ("Ava", "138 cm"), ("Leo", "1,520 mm"), ("Isla", "1.5 m")]
    vals = [parse(j)[1] for _, j in jumps]
    assert vals == [1450, 1380, 1520, 1500]
    add("Four pupils do a standing long jump. Oliver jumps 1.45 m, Ava jumps 138 cm, Leo jumps 1,520 mm "
        "and Isla jumps 1.5 m. Who jumps the furthest?",
        "Leo", ["Oliver", "Ava", "Isla"],
        "Change them all to centimetres: 1.45 m = 145 cm, 1,520 mm = 152 cm and 1.5 m = 150 cm. "
        "152 cm is the furthest, so Leo jumps the furthest.")
    n, he, his = P.next()
    add("%s’s family goes on holiday on 25 July. The holiday lasts exactly 3 weeks. On what date do they come home?" % n,
        "15 August", ["28 July", "16 August", "25 August"],
        "3 weeks = 21 days. July has 31 days, so 25 July + 6 days = 31 July. 21 − 6 = 15 days more: 15 August. "
        "(16 August counts July as 30 days. 28 July adds 3 days, not 3 weeks.)")
    assert 25 + 21 - 31 == 15
    assert len(its) == 20, len(its)
    return {"title": "Word problems: recipes, money and journeys", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


def body_html():
    return (
        "<h2>Multiply or divide?</h2>"
        "<p>To change a bigger unit into a smaller unit, <b>multiply</b>: you need more of the small units. "
        "To change a smaller unit into a bigger unit, <b>divide</b>. "
        "Multiplying by 1,000 moves every digit 3 places to the left. Dividing by 1,000 moves every digit 3 places to the right.</p>"
        "<figure class='sn-fig'>" + ladder_svg(["km", "m", "cm", "mm"], ["1,000", "100", "10"],
                                                "length units: km to m to cm to mm") +
        "<figcaption>Going to a smaller unit: multiply. Going to a bigger unit: divide.</figcaption></figure>" +
        ex("Kilometres to metres", "2.4 km = ☐ m", "1 km = 1,000 m. Multiply: 2.4 × 1,000 = 2,400.",
           "2,400 m (not 240 m)") +
        ex("Grams to kilograms", "350 g = ☐ kg", "1 kg = 1,000 g. Divide: 350 ÷ 1,000 = 0.35.", "0.35 kg") +
        "<h2>Metric facts to know</h2>" +
        table(["Measure", "Facts"], [
            ["Length", "1 cm = 10 mm &nbsp; 1 m = 100 cm &nbsp; 1 km = 1,000 m"],
            ["Mass", "1 kg = 1,000 g"],
            ["Capacity", "1 l = 1,000 ml"],
        ]) +
        "<h2>Read the scale, then convert</h2>"
        "<p>Work out what each mark is worth before you read the scale.</p>"
        "<figure class='sn-fig'>" + jug_svg(1300, 2000, 500, 100) +
        "<figcaption>500 ml is split into 5 spaces, so each line is 100 ml. The water is at 1,300 ml, which is 1.3 l.</figcaption></figure>"
        "<h2>Imperial units</h2>"
        "<p>Imperial units are older units that are still used in the UK. Milk is sold in pints, "
        "people often give their height in feet and inches, and babies are weighed in pounds (lb). "
        "We only need rough facts, so we say <b>about</b> (≈).</p>" +
        table(["Imperial", "About the same as"], [
            ["1 inch", "2.5 cm"],
            ["1 foot (12 inches)", "30 cm"],
            ["2.2 pounds (lb)", "1 kg"],
            ["1 pint", "570 ml (just over half a litre)"],
        ]) +
        "<figure class='sn-fig'>" + inch_ruler_svg(4) +
        "<figcaption>4 inches is just over 10 cm, so 4 inches ≈ 10 cm.</figcaption></figure>" +
        ex("Inches to centimetres", "12 inches ≈ ☐ cm", "1 inch ≈ 2.5 cm. 12 × 2.5 = 30.", "about 30 cm") +
        ex("Pints to litres", "4 pints ≈ ☐ litres", "1 pint ≈ 570 ml. 4 × 570 = 2,280 ml = 2.28 l.", "about 2.3 litres") +
        "<h2>Time is not decimal</h2>"
        "<p>An hour has 60 minutes, not 100, and a minute has 60 seconds.</p>" +
        table(["Time", "Facts"], [
            ["Seconds and minutes", "1 minute = 60 seconds &nbsp; 1 hour = 60 minutes"],
            ["Days and weeks", "1 day = 24 hours &nbsp; 1 week = 7 days"],
            ["Years", "1 year = 12 months = 52 weeks and 1 day = 365 days"],
            ["Leap years", "every 4 years, 366 days, with 29 February (2024, 2028)"],
        ]) +
        ex("Hours to minutes", "2 hours 15 minutes = ☐ minutes", "2 × 60 = 120. 120 + 15 = 135.", "135 minutes") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["2.4 km = 240 m", "1 km = 1,000 m, so multiply by 1,000: 2.4 km = 2,400 m"],
            ["1 km = 100 m", "Kilo means 1,000: 1 km = 1,000 m and 1 kg = 1,000 g"],
            ["Multiplying to get a bigger unit (350 g = 350,000 kg)", "Smaller unit to bigger unit: divide (350 g = 0.35 kg)"],
            ["1 hour = 100 minutes", "1 hour = 60 minutes, so 130 minutes = 2 hours 10 minutes"],
            ["4 pints = exactly 2,280 ml", "Imperial facts are approximate: 4 pints is about 2.3 litres"],
        ])
    )


FAQ = [
    {"q": "What unit conversions do Year 5 children need to know?",
     "a": "Year 5 children convert between km and m, m and cm, cm and mm, kg and g, and l and ml, often with decimals. "
          "They also convert units of time and learn rough imperial equivalents such as inches, pounds and pints."},
    {"q": "Do Year 5 pupils learn imperial units?",
     "a": "Yes. They learn approximate equivalences, such as 1 inch ≈ 2.5 cm, 1 foot ≈ 30 cm, 1 kg ≈ 2.2 lb "
          "and 1 pint ≈ 570 ml, because these units are still used in everyday life in the UK."},
    {"q": "How do you convert kilometres to metres?",
     "a": "Multiply by 1,000, because 1 km = 1,000 m. So 2.4 km = 2,400 m. To go back from metres to kilometres, divide by 1,000."},
    {"q": "How many days are in a leap year?",
     "a": "A leap year has 366 days instead of 365, because February has 29 days. Leap years come every 4 years, such as 2024 and 2028."},
]


def balance(sets, rnd):
    """Spread the correct answers evenly over the 4 positions in every set."""
    for s in sets:
        targets = [0, 1, 2, 3] * 5
        rnd.shuffle(targets)
        for it, t in zip(s["items"], targets):
            c = it["c"]
            c[it["a"]], c[t] = c[t], c[it["a"]]
            it["a"] = t


def gen_unit():
    rnd = random.Random(5513)
    sets = [set_length(rnd), set_mass_cap(rnd), set_imperial(rnd), set_time(rnd), set_story(rnd)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        pos = [0, 0, 0, 0]
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            pos[it["a"]] += 1
            k = it["q"] + "|" + "|".join(sorted(it["c"]))
            assert k not in seen, it["q"]
            seen.add(k)
            assert it["q"].count("<svg") <= 1
        assert pos == [5, 5, 5, 5], (s["title"], pos)
    return {
        "country": "uk", "subject": "maths", "grade": "year-5", "slug": "converting-units", "sort": 13,
        "updated": UPDATED, "pdf_url": "",
        "title": "Converting Units",
        "seo_title": "Year 5 Converting Units Worksheets: Metric, Imperial and Time (Free, with Answers)",
        "short_title": "Converting units",
        "domain": "Measurement",
        "standard_code": "Year 5: Measurement",
        "standard_url": "https://www.gov.uk/government/publications/national-curriculum-in-england-mathematics-programmes-of-study",
        "standard_text": "Convert between different units of metric measure [for example, kilometre and metre; centimetre and metre; centimetre and millimetre; gram and kilogram; litre and millilitre]; understand and use approximate equivalences between metric units and common imperial units such as inches, pounds and pints; solve problems involving converting between units of time; use all four operations to solve problems involving measure [for example, length, mass, volume, money] using decimal notation, including scaling.",
        "meta_desc": "Free Year 5 maths worksheets on converting units: km, m, cm and mm, kg and g, l and ml with decimals, imperial units (inches, feet, pounds and pints), and time including leap years. Scales and word problems with recipes and money. 100 questions with an answer key, matched to the National Curriculum.",
        "key_big": "Bigger unit to smaller unit: multiply. Smaller unit to bigger unit: divide.",
        "key_sub": "2.4 km = 2,400 m and 350 g = 0.35 kg. Time uses 60, so 1 hour = 60 minutes, not 100. Imperial units are only about: 1 inch ≈ 2.5 cm, 1 kg ≈ 2.2 lb, 1 pint ≈ 570 ml.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


def mark_large(u, pattern):
    """Tag pictures that must print larger so their labels stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


if __name__ == "__main__":
    u = gen_unit()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        mark_large(u, "(ruler)")
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
