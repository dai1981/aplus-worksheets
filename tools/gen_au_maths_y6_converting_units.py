# -*- coding: utf-8 -*-
"""
AU Year 6 Maths: Converting Metric Units (Australian Curriculum v9.0, AC9M6M01)
  python3 tools/gen_au_maths_y6_converting_units.py
Convert between mm, cm, m and km, g, kg and t, and mL and L, using decimals (1.25 m = 125 cm,
750 g = 0.75 kg, 2.5 L = 2500 mL); choose a sensible unit and decimal form; compare and order mixed units.
HTML attributes use single quotes (no backslashes in the JSON).
Australian English, mL and L with a capital L.
Australian number style: 4-digit numbers plain (2400 kg), 5 or more digits grouped with a no-break space.
Every measurement answer is parsed back to a base unit (mm, g, mL) and checked in code, and measurement
choices in a question never have the same value.
Wrong answers come from real mistakes: multiplying by 100 for kg, g or mL, moving the point the wrong way,
1.5 m = 105 cm, 3 kg 40 g = 3.4 kg, and comparing the numbers without changing to one unit.
"""
import json, math, os, random, re
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "au", "maths", "year-6")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
RED = "#c0392b"
INK = "#2b2b2b"
WATER = "#9fd3f2"
WATER_LINE = "#2a7fb8"
WOOD = "#f6e7b8"
FONT = "Arial, Helvetica, sans-serif"
NBSP = " "
GIRLS = ["Charlotte", "Isla", "Mia", "Amelia", "Ava", "Harper", "Chloe", "Ruby", "Mei", "Zara", "Matilda", "Sienna",
         "Grace"]
BOYS = ["Oliver", "Jack", "Noah", "William", "Leo", "Lachlan", "Liam", "Aarav", "Kai", "Cooper", "Ethan"]


# ------------------------------------------------------------ units and checking
# unit: (family, size in the base unit mm / g / mL, word)
UNIT = {"mm": ("L", 1, "millimetres"), "cm": ("L", 10, "centimetres"), "m": ("L", 1000, "metres"),
        "km": ("L", 1000000, "kilometres"),
        "g": ("M", 1, "grams"), "kg": ("M", 1000, "kilograms"), "t": ("M", 1000000, "tonnes"),
        "mL": ("C", 1, "millilitres"), "L": ("C", 1000, "litres")}
TOK = re.compile(r"(\d[\d" + NBSP + r"]*(?:\.\d+)?)\s*(" + "|".join(sorted(UNIT, key=len, reverse=True)) +
                 r")(?![a-zA-Z])")


def parse(s):
    """'2 kg 40 g' -> ('M', 2040). None if the string is not a plain measurement."""
    s = s.strip()
    pos, fam, tot = 0, None, Fr(0)
    for mt in TOK.finditer(s):
        if s[pos:mt.start()].strip():
            return None
        fu, sz = UNIT[mt.group(2)][:2]
        if fam and fu != fam:
            return None
        fam = fu
        tot += Fr(mt.group(1).replace(NBSP, "")) * sz
        pos = mt.end()
    if fam is None or s[pos:].strip():
        return None
    return fam, tot


def truth(st):
    """'0.4 L < 450 mL' -> True/False (chains allowed)."""
    parts = re.split(r" (<|>|=) ", st)
    vals = [parse(p) for p in parts[0::2]]
    assert all(vals) and len({v[0] for v in vals}) == 1, st
    ok = True
    for i, op in enumerate(parts[1::2]):
        a, b = vals[i][1], vals[i + 1][1]
        ok = ok and {"<": a < b, ">": a > b, "=": a == b}[op]
    return ok


def c(n):
    """Australian style: 4 digits plain (2400), 5 or more digits grouped with a no-break space (12 000)."""
    n = int(n)
    if n < 10000:
        return str(n)
    return "{:,}".format(n).replace(",", NBSP)


def fmt(x):
    """Fraction/int -> '2400', '12 000' or '0.75' (exact, at most 3 decimal places)."""
    x = Fr(x)
    assert (x * 1000).denominator == 1, x
    if x.denominator == 1:
        return c(x.numerator)
    s = ("%.3f" % float(x)).rstrip("0")
    a, _, b = s.partition(".")
    return c(int(a)) + "." + b


def m(n, u):
    return "%s %s" % (fmt(n), u)


def two(v, big, small):
    """v in base units -> '2 kg 40 g' (no zero parts)."""
    B, S = UNIT[big][1], UNIT[small][1]
    a, r = divmod(Fr(v), B)
    r = r / S
    assert r.denominator == 1
    if r == 0:
        return m(a, big)
    if a == 0:
        return m(r, small)
    return "%s %s" % (m(a, big), m(r, small))


def kgg(v):
    return two(v, "kg", "g")


def lml(v):
    return two(v, "L", "mL")


def mcm(v):
    return two(v, "m", "cm")


def cmmm(v):
    return two(v, "cm", "mm")


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e, rnd, want=None):
    """4 choices: correct + 3 unique distractors. Measurement choices must all differ in value.
    want = (family, value in base unit) checks the correct answer."""
    correct = str(correct)
    if want is not None:
        assert parse(correct) == (want[0], Fr(want[1])), (q, correct, want, parse(correct))
    seen = {correct}
    pc = parse(correct)
    vals = {pc[1]} if pc else set()
    pick = []
    for x in cands:
        x = str(x)
        lead = x.split(" ")[0]
        if x in seen or not x or lead.startswith("-") or lead == "0":
            continue
        pv = parse(x)
        if pc and pv and pv[0] == pc[0]:
            if pv[1] in vals:
                continue
            vals.add(pv[1])
        seen.add(x)
        pick.append(x)
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


def marks(k, w="mark"):
    return "%d %s%s" % (k, w, "" if k == 1 else "s")


# ------------------------------------------------------------ figures
def draw_object(kind, a, b):
    """An object lying exactly from x=a to x=b, between y=12 and y=32."""
    o = []
    if kind in ("pencil", "crayon"):
        body = "#f4c542" if kind == "pencil" else "#3a6fb0"
        tipc = WOOD if kind == "pencil" else body
        tip = min(22, (b - a) * 0.3)
        o.append("<rect x='%.1f' y='12' width='%.1f' height='20' fill='%s' stroke='%s' stroke-width='1.5'/>"
                 % (a, b - a - tip, body, INK))
        if kind == "pencil":
            o.append("<rect x='%.1f' y='12' width='8' height='20' fill='#e98aa0' stroke='%s' stroke-width='1.5'/>" % (a, INK))
        else:
            o.append("<rect x='%.1f' y='12' width='%.1f' height='20' fill='#fff' stroke='%s' stroke-width='1.5'/>"
                     % (a + (b - a - tip) * 0.25, (b - a - tip) * 0.4, INK))
        o.append("<path d='M%.1f 12 L%.1f 22 L%.1f 32 Z' fill='%s' stroke='%s' stroke-width='1.5' stroke-linejoin='round'/>"
                 % (b - tip, b, b - tip, tipc, INK))
        if kind == "pencil":
            o.append("<path d='M%.1f 19.5 L%.1f 22 L%.1f 24.5 Z' fill='%s'/>" % (b - tip * 0.25, b, b - tip * 0.25, INK))
    elif kind == "eraser":
        o.append("<rect x='%.1f' y='12' width='%.1f' height='20' rx='4' fill='#f7b7c5' stroke='%s' stroke-width='1.5'/>"
                 % (a, b - a, INK))
        o.append("<rect x='%.1f' y='12' width='%.1f' height='20' fill='#5dade2' stroke='%s' stroke-width='1.5'/>"
                 % (a + (b - a) * 0.45, (b - a) * 0.4, INK))
    else:  # ribbon
        o.append("<rect x='%.1f' y='15' width='%.1f' height='14' fill='%s' stroke='%s' stroke-width='1.5'/>"
                 % (a, b - a, RED, INK))
    return "".join(o)


NAMES = {"pencil": "pencil", "crayon": "crayon", "eraser": "eraser", "ribbon": "piece of ribbon"}


def ruler_svg(s_mm, e_mm, kind="pencil", ncm=None):
    """Ruler from 0 to ncm cm with mm marks and an object from s_mm to e_mm (exact)."""
    if ncm is None:
        ncm = max(8, -(-e_mm // 10) + 1)
    PX = 38.0
    X0, YR, RH = 18, 40, 50
    W = int(X0 * 2 + PX * ncm + 26)
    H = YR + RH + 4
    X = lambda mm: X0 + PX * mm / 10.0
    a, b = X(s_mm), X(e_mm)
    o = [draw_object(kind, a, b)]
    for x in (a, b):
        o.append("<line x1='%.1f' y1='32' x2='%.1f' y2='%d' stroke='%s' stroke-width='1.2' stroke-dasharray='3 2'/>"
                 % (x, x, YR, RED))
    o.append("<rect x='4' y='%d' width='%d' height='%d' rx='3' fill='%s' stroke='%s' stroke-width='2'/>"
             % (YR, W - 8, RH, WOOD, INK))
    small, big = [], []
    for i in range(ncm * 10 + 1):
        x = X(i)
        ln = 18 if i % 10 == 0 else (12 if i % 5 == 0 else 7)
        (big if i % 10 == 0 else small).append("M%.1f %dL%.1f %d" % (x, YR, x, YR + ln))
    o.append("<path d='%s' stroke='%s' stroke-width='1'/>" % ("".join(small), INK))
    o.append("<path d='%s' stroke='%s' stroke-width='2'/>" % ("".join(big), INK))
    for cc in range(ncm + 1):
        o.append(text(X(cc * 10), YR + 38, str(cc), 15))
    o.append(text(X(ncm * 10) + 12, YR + 38, "cm", 15, anchor="start", bold=False))
    return svg_wrap(W, H, "".join(o), "ruler with %s %s from %d mm to %d mm"
                    % ("an" if kind == "eraser" else "a", NAMES[kind], s_mm, e_mm))


def dial_svg(v, mx, lab, tick, div=1, size=200):
    """Round scale, values in grams. Labels every `lab` g shown as val/div (g or kg). Needle exactly at v."""
    unit = "g" if div == 1 else "kg"
    cx = cy = size / 2.0
    R = size / 2.0 - 6

    def pt(val, r):
        ang = math.radians(-135 + 270.0 * val / mx)
        return cx + r * math.sin(ang), cy - r * math.cos(ang)
    s = ["<circle cx='%.1f' cy='%.1f' r='%.1f' fill='#fff' stroke='%s' stroke-width='6'/>" % (cx, cy, R, GREEN)]
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
             % (cx, cy, nx, ny, RED))
    s.append("<g font-size='%d' font-weight='700' fill='%s' text-anchor='middle' stroke='#fff' stroke-width='4' "
             "paint-order='stroke'>" % (15 if mx // div >= 1000 else 17, INK))
    for val in range(0, mx + 1, lab):
        x, y = pt(val, R - 36)
        s.append("<text x='%.1f' y='%.1f'>%s</text>" % (x, y + 6, fmt(Fr(val, div))))
    s.append("</g>")
    s.append("<circle cx='%.1f' cy='%.1f' r='7' fill='%s'/>" % (cx, cy, RED))
    s.append("<text x='%.1f' y='%.1f' font-size='22' font-weight='800' fill='%s' text-anchor='middle'>%s</text>"
             % (cx, cy + 62, GREEN, unit))
    return svg_wrap(size, size, "".join(s), "weighing scale in %s with the needle at %s" % (unit, kgg(v)))


def jug_svg(v, mx, lab, step, div=1, size=200):
    """Measuring jug, values in mL: a line every `step` mL, a label every `lab` mL shown as val/div (mL or L).
    Water exactly at v."""
    unit = "mL" if div == 1 else "L"
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
            s.append("<text x='%d' y='%.1f'>%s</text>" % (x0 - 7, Y(val) + 5, fmt(Fr(val, div))))
    s.append("</g>")
    s.append(text(x0 - 7, 202, unit, 15, anchor="end", col=GREEN))
    return svg_wrap(size, size + 8, "".join(s), "measuring jug in %s with water at %s" % (unit, lml(v)))


# ------------------------------------------------------------ explanations for reading instruments
def dial_e(v, lab, tick, div):
    sp = lab // tick
    base = v - v % lab
    k = (v - base) // tick
    if div == 1:
        s = ("The numbers go up by %s g and there are %d spaces between them, so each mark is %s ÷ %d = %d g. "
             % (c(lab), sp, c(lab), sp, tick))
        return s + "The needle is %s past %s: %s + %d = %s g." % (marks(k), c(base), c(base), k * tick, c(v))
    s = ("Each kilogram is split into %d spaces, so each mark is 1000 ÷ %d = %d g. " % (sp, sp, tick))
    return s + "The needle is %s past %d kg: %d kg and %d × %d = %d g, so %s." % (
        marks(k), base // 1000, base // 1000, k, tick, k * tick, kgg(v))


def jug_e(v, lab, step, div):
    sp = lab // step
    base = v - v % lab
    k = (v - base) // step
    if div == 1:
        s = ("The numbers go up by %s mL and there are %d spaces between them, so each line is %s ÷ %d = %d mL. "
             % (c(lab), sp, c(lab), sp, step))
        return s + "The water is %s above %s: %s + %d = %s mL." % (marks(k, "line"), c(base), c(base), k * step, c(v))
    s = "Each litre is split into %d spaces, so each line is 1000 ÷ %d = %d mL. " % (sp, sp, step)
    return s + "The water is %s above %d L: %d L and %d × %d = %d mL, so %s." % (
        marks(k, "line"), base // 1000, base // 1000, k, step, k * step, lml(v))


# ------------------------------------------------------------ set 1: choose the unit


# ------------------------------------------------------------ conversions
def k_between(uf, ut):
    return Fr(UNIT[uf][1], UNIT[ut][1])


PLACES = {10: "1 place", 100: "2 places", 1000: "3 places"}


def conv_e(n, uf, ut):
    """Explanation for n uf -> ut (one step)."""
    k = k_between(uf, ut)
    r = Fr(n) * k
    if k > 1:
        k = int(k)
        s = "1 %s = %s %s. %s are bigger than %s, so multiply by %s: %s × %s = %s." % (
            uf, fmt(k), ut, cap(UNIT[uf][2]), UNIT[ut][2], fmt(k), fmt(n), fmt(k), fmt(r))
        if k in PLACES:
            s += " The digits move %s to the left." % PLACES[k]
    else:
        k = int(1 / k)
        s = "1 %s = %s %s. %s are smaller than %s, so divide by %s: %s ÷ %s = %s." % (
            ut, fmt(k), uf, cap(UNIT[uf][2]), UNIT[ut][2], fmt(k), fmt(n), fmt(k), fmt(r))
        if k in PLACES:
            s += " The digits move %s to the right." % PLACES[k]
    return s + " So %s = %s." % (m(n, uf), m(r, ut))


def conv(n, uf, ut, wrong, rnd, q=None, e=None, extra=""):
    """Convert n uf into ut. wrong = numbers in ut from real mistakes."""
    n = Fr(n)
    fam = UNIT[uf][0]
    r = n * k_between(uf, ut)
    if q is None:
        q = "Convert. <b>%s = ☐ %s</b>" % (m(n, uf), ut)
    return mcq(q, m(r, ut), [m(Fr(w), ut) for w in wrong], (e or conv_e(n, uf, ut)) + extra, rnd,
               want=(fam, n * UNIT[uf][1]))


def D(s):
    return Fr(s)


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


# ------------------------------------------------------------ set 1: length
def set_length(rnd):
    its = []
    L = lambda v: ("L", v)
    its.append(conv(D("3.6"), "m", "cm", [36, 3600, 306], rnd))
    its.append(conv(D("1.25"), "m", "cm", [D("12.5"), 1250, 1025], rnd))
    its.append(conv(D("1.5"), "m", "cm", [105, 15, 1500], rnd,
                    extra=" (1.5 m is 1 m 50 cm, so it is not 105 cm. 105 cm would be 1.05 m.)"))
    its.append(conv(45, "mm", "cm", [450, D("0.45"), D("0.045")], rnd))
    its.append(conv(D("2.4"), "km", "m", [240, 24000, 2004], rnd))
    its.append(conv(850, "m", "km", [D("8.5"), D("0.085"), 850000], rnd,
                    extra=" (850" + NBSP + "000 km multiplies when it should divide.)"))
    its.append(conv(D("0.7"), "cm", "mm", [70, D("0.07"), 700], rnd))
    its.append(conv(65, "cm", "m", [D("6.5"), D("0.065"), 6500], rnd))
    its.append(conv(D("3.125"), "km", "m", [D("312.5"), 31250, D("3.125")], rnd))
    its.append(conv(75, "m", "km", [D("0.75"), D("7.5"), 75000], rnd,
                    extra=" Check: 0.75 km would be 750 m."))
    its.append(conv(D("1.75"), "m", "mm", [175, 17500, D("1.75")], rnd,
                    extra=" (1.75 × 100 = 175 would give centimetres, not millimetres.)"))
    its.append(conv(45, "mm", "m", [D("4.5"), D("0.45"), 45], rnd,
                    extra=" You need a 0 in the tenths place."))
    q = fig(ruler_svg(0, 83, "pencil", 9)) + "How long is the pencil in centimetres?"
    its.append(mcq(q, "8.3 cm", ["83 cm", "0.83 cm", "8.03 cm"],
                   "The pencil ends 3 small marks after 8 cm. Each small mark is 1 mm, so it is 83 mm. "
                   "1 cm = 10 mm, so 83 ÷ 10 = 8.3 cm.", rnd, want=L(83)))
    q = fig(ruler_svg(0, 56, "crayon", 7)) + "How long is the crayon in metres?"
    its.append(mcq(q, "0.056 m", ["0.56 m", "5.6 m", "0.506 m"],
                   "The crayon ends 6 small marks after 5 cm, so it is 56 mm. 1 m = 1000 mm, so divide by 1000: "
                   "56 ÷ 1000 = 0.056 m. (0.56 m divides by 100, which gives 560 mm.)", rnd, want=L(56)))
    its.append(conv(4050, "m", "km", [D("4.5"), D("40.5"), D("4.005")], rnd,
                    extra=" The 0 in 4050 keeps its place: 4.05, not 4.5."))
    its.append(conv(D("1.08"), "m", "cm", [180, D("10.8"), 1080], rnd))
    its.append(mcq("Convert. <b>2 km 75 m = ☐ km</b>", "2.075 km", ["2.75 km", "20.75 km", "2.705 km"],
                   "75 m = 75 ÷ 1000 = 0.075 km, because 1 km = 1000 m. So 2 km 75 m = 2 + 0.075 = 2.075 km. "
                   "2.75 km would be 2 km 750 m.", rnd, want=L(2075000)))
    its.append(mcq("Which is the same as <b>0.305 km</b>?", "305 m", ["3050 m", "30.5 m", "35 m"],
                   "Multiply by 1000: 0.305 × 1000 = 305 m. The 0 holds the tenths place, so it is not 35 m.",
                   rnd, want=L(305000)))
    its.append(mcq("Which is the same as <b>6.04 m</b>?", "6 m 4 cm", ["6 m 40 cm", "6 m 4 mm", "64 cm"],
                   "6.04 m = 6 m and 0.04 m. 0.04 m = 0.04 × 100 = 4 cm. So 6.04 m = 6 m 4 cm. "
                   "6 m 40 cm would be 6.4 m.", rnd, want=L(6040)))
    its.append(mcq("Find the missing number. <b>1 km − 375 m = ☐ km</b>", "0.625 km",
                   ["0.725 km", "0.375 km", "625 km"],
                   "1 km = 1000 m. 1000 − 375 = 625 m. 625 ÷ 1000 = 0.625 km. "
                   "Take care when you regroup: 1000 − 375 is 625, not 725.", rnd, want=L(625000)))
    assert len(its) == 20, len(its)
    return {"title": "Length: mm, cm, m and km with decimals", "items": its}


# ------------------------------------------------------------ set 2: mass and capacity
def set_mass_cap(rnd):
    its = []
    its.append(conv(750, "g", "kg", [D("7.5"), D("0.075"), 750000], rnd))
    its.append(conv(D("2.5"), "kg", "g", [250, 25000, 205], rnd,
                    extra=" (250 g multiplies by 100, but 1 kg is 1000 g, not 100 g.)"))
    its.append(conv(D("1.25"), "L", "mL", [125, 12500, 1025], rnd,
                    extra=" (125 mL would be 0.125 L.)"))
    its.append(conv(D("2.5"), "L", "mL", [250, 25, 25000], rnd))
    its.append(conv(330, "mL", "L", [D("3.3"), D("0.033"), 330000], rnd))
    its.append(conv(D("2.4"), "t", "kg", [240, 24000, 2004], rnd,
                    extra=" (240 kg multiplies by 100, but 1 t is 1000 kg.)"))
    its.append(conv(3500, "kg", "t", [35, D("0.35"), D("3.05")], rnd))
    its.append(conv(45, "g", "kg", [D("0.45"), D("4.5"), 45000], rnd))
    its.append(conv(D("4.08"), "kg", "g", [4800, 408, 4008], rnd))
    its.append(conv(D("0.6"), "t", "kg", [60, 6, 6000], rnd))
    its.append(conv(2600, "mL", "L", [26, D("0.26"), D("2.06")], rnd))
    its.append(conv(D("0.08"), "L", "mL", [800, 8, D("0.8")], rnd))
    its.append(mcq("Convert. <b>3 kg 50 g = ☐ kg</b>", "3.05 kg", ["3.5 kg", "3.005 kg", "30.5 kg"],
                   "50 g = 50 ÷ 1000 = 0.05 kg. So 3 kg 50 g = 3.05 kg. 3.5 kg would be 3 kg 500 g.",
                   rnd, want=("M", 3050)))
    its.append(mcq("Work out <b>1.5 kg + 700 g</b>. Give your answer in kilograms.", "2.2 kg",
                   ["701.5 kg", "8.5 kg", "1.57 kg"],
                   "Use one unit first: 700 g = 0.7 kg. Then 1.5 + 0.7 = 2.2 kg. "
                   "701.5 kg adds the numbers without converting.", rnd, want=("M", 2200)))
    q = fig(dial_svg(1400, 3000, 1000, 200, 1000)) + \
        "The scale shows the mass of a bag of flour. What is the mass in kilograms?"
    its.append(mcq(q, "1.4 kg", ["1.2 kg", "1.04 kg", "14 kg"],
                   "Each kilogram is split into 5 equal spaces, so each mark is 1 ÷ 5 = 0.2 kg (200 g). "
                   "The needle is 2 marks past 1 kg: 1 + 0.4 = 1.4 kg. (1.2 kg counts each mark as 0.1 kg.)",
                   rnd, want=("M", 1400)))
    q = fig(dial_svg(2750, 4000, 1000, 250, 1000)) + \
        "The scale shows the mass of a parcel. What is the mass in kilograms?"
    its.append(mcq(q, "2.75 kg", ["2.3 kg", "2.075 kg", "27.5 kg"],
                   "Each kilogram is split into 4 equal spaces, so each mark is 1 ÷ 4 = 0.25 kg (250 g). "
                   "The needle is 3 marks past 2 kg: 2 + 0.75 = 2.75 kg. (2.3 kg counts each mark as 0.1 kg.)",
                   rnd, want=("M", 2750)))
    q = fig(dial_svg(600, 1000, 200, 50)) + "The scale shows the mass of some apples. What is the mass in kilograms?"
    its.append(mcq(q, "0.6 kg", ["6 kg", "0.06 kg", "600 kg"],
                   "The needle points to 600 g. 1 kg = 1000 g, so divide by 1000: 600 ÷ 1000 = 0.6 kg.",
                   rnd, want=("M", 600)))
    q = fig(jug_svg(1300, 2000, 500, 100)) + "How much water is in the jug? Give your answer in litres."
    its.append(mcq(q, "1.3 L", ["1.03 L", "13 L", "0.13 L"],
                   "The numbers go up by 500 mL with 5 spaces between them, so each line is 100 mL. "
                   "The water is 3 lines above 1000 mL: 1300 mL. 1300 ÷ 1000 = 1.3 L. "
                   "(1.03 L would be 1030 mL.)", rnd, want=("C", 1300)))
    q = fig(jug_svg(650, 1000, 250, 50)) + "How much water is in the jug? Give your answer in litres."
    its.append(mcq(q, "0.65 L", ["0.53 L", "6.5 L", "0.065 L"],
                   "The numbers go up by 250 mL with 5 spaces between them, so each line is 50 mL. "
                   "The water is 3 lines above 500 mL: 500 + 150 = 650 mL. 650 ÷ 1000 = 0.65 L. "
                   "(0.53 L counts each line as 10 mL.)", rnd, want=("C", 650)))
    q = fig(jug_svg(1600, 2000, 500, 100)) + "How much more water is needed to fill the jug to 2 L?"
    its.append(mcq(q, "400 mL", ["600 mL", "1600 mL", "40 mL"],
                   "Each line is 100 mL. The water is at 1600 mL. 2 L = 2000 mL. 2000 − 1600 = 400 mL more. "
                   "(600 mL reads the water level as 1400 mL.)", rnd, want=("C", 400)))
    assert len(its) == 20, len(its)
    return {"title": "Mass and capacity: g, kg, t, mL and L", "items": its}


# ------------------------------------------------------------ set 3: sensible unit and decimal form
def set_sensible(rnd):
    its = []
    for obj, ans, wr, e in [
        ("the mass of a watermelon", "4.5 kg", ["4.5 g", "4.5 t", "45 g"],
         "A watermelon is heavy to carry but far lighter than a car, so kilograms fit. 4.5 g is lighter than "
         "one 20c coin, and 4.5 t is heavier than a big car."),
        ("how much a can of soft drink holds", "375 mL", ["375 L", "3.75 L", "37.5 mL"],
         "A can holds less than half a litre. 375 mL = 0.375 L. 375 L would fill a big bathtub twice."),
        ("the length of a classroom", "9.5 m", ["9.5 km", "9.5 cm", "95 m"],
         "A classroom is about 10 big steps long, so 9.5 m fits. 9.5 cm is only the width of a hand, and 95 m is longer than a whole row of classrooms."),
        ("the mass of a loaded truck", "12.5 t", ["12.5 kg", "125 g", "1.25 kg"],
         "A loaded truck is very heavy, so use tonnes. 12.5 t = 12 500 kg."),
        ("the driving distance from Sydney to Canberra", "290 km", ["290 m", "29 m", "2.9 km"],
         "Sydney to Canberra is a drive of about 3 hours, so it is a few hundred kilometres. "
         "2.9 km is only a short walk."),
        ("the thickness of a mobile phone", "8 mm", ["8 cm", "8 m", "0.8 m"],
         "A phone is thinner than 1 cm, so use millimetres. 8 cm is as thick as a large book."),
        ("how much water a bathtub holds", "150 L", ["150 mL", "15 mL", "1.5 L"],
         "A bathtub holds a lot of water, so use litres. 1.5 L is only a large drink bottle."),
        ("the mass of an adult koala", "9 kg", ["9 g", "9 t", "0.9 kg"],
         "An adult koala is about as heavy as a big bag of dog food, so kilograms fit. 0.9 kg = 900 g, "
         "which is lighter than a carton of milk."),
        ("the mass of a Year 6 student", "38 kg", ["38 g", "38 t", "3.8 kg"],
         "Most Year 6 students have a mass of about 30 kg to 50 kg. 3.8 kg is the mass of a new baby."),
    ]:
        its.append(mcq("Which is the most sensible measurement for <b>%s</b>?" % obj, ans, wr, e, rnd))
    its.append(mcq("A carpenter measures a board as <b>2 m 45 cm</b>. How is this written in metres?", "2.45 m",
                   ["2.045 m", "24.5 m", "2.405 m"],
                   "45 cm = 45 ÷ 100 = 0.45 m, because 1 m = 100 cm. So 2 m 45 cm = 2.45 m.", rnd, want=("L", 2450)))
    its.append(mcq("A bag of rice has a mass of <b>1650 g</b>. Which shows this in kilograms?", "1.65 kg",
                   ["16.5 kg", "165 kg", "1.065 kg"],
                   "1 kg = 1000 g, so divide by 1000: 1650 ÷ 1000 = 1.65 kg. "
                   "(16.5 kg divides by 100, as if 1 kg were 100 g.)", rnd, want=("M", 1650)))
    its.append(mcq("A jug holds <b>1 L 200 mL</b>. Which shows this in litres?", "1.2 L",
                   ["1.02 L", "12 L", "0.12 L"],
                   "200 mL = 200 ÷ 1000 = 0.2 L. So 1 L 200 mL = 1.2 L. 1.02 L would be 1 L 20 mL.",
                   rnd, want=("C", 1200)))
    its.append(mcq("Which shows <b>3 kg 250 g</b> using one unit?", "3.25 kg",
                   ["3.025 kg", "32.5 kg", "325 g"],
                   "250 g = 0.25 kg, so 3 kg 250 g = 3.25 kg (or 3250 g). 325 g joins the digits and loses the 0.",
                   rnd, want=("M", 3250)))
    its.append(mcq("A newborn baby has a mass of <b>3 kg 40 g</b>. Which shows this in kilograms?", "3.04 kg",
                   ["3.4 kg", "3.004 kg", "30.4 kg"],
                   "40 g = 40 ÷ 1000 = 0.04 kg. So 3 kg 40 g = 3.04 kg. 3.4 kg would be 3 kg 400 g.",
                   rnd, want=("M", 3040)))
    its.append(mcq("A bridge sign shows a mass limit of <b>4500 kg</b>. Which shows this in tonnes?", "4.5 t",
                   ["45 t", "0.45 t", "4.05 t"],
                   "1 t = 1000 kg, so divide by 1000: 4500 ÷ 1000 = 4.5 t. (45 t divides by 100.)",
                   rnd, want=("M", 4500000)))
    its.append(mcq("Mia jumps <b>312 cm</b> in the long jump. Which shows this in metres?", "3.12 m",
                   ["31.2 m", "0.312 m", "3.012 m"],
                   "1 m = 100 cm, so divide by 100: 312 ÷ 100 = 3.12 m. The digits move 2 places to the right.",
                   rnd, want=("L", 3120)))
    its.append(mcq("An ant is <b>0.006 m</b> long. Which shows the same length in a more sensible unit?", "6 mm",
                   ["6 cm", "0.6 mm", "0.06 mm"],
                   "1 m = 1000 mm, so 0.006 × 1000 = 6 mm. A small number of millimetres is easier to read than "
                   "a decimal with zeros.", rnd, want=("L", 6)))
    its.append(mcq("A road is <b>0.004 km</b> wide. Which shows the same width in a more sensible unit?", "4 m",
                   ["40 m", "0.4 m", "400 m"],
                   "1 km = 1000 m, so 0.004 × 1000 = 4 m. Metres suit the width of a road.", rnd, want=("L", 4000)))
    its.append(mcq("Which decimal measurement is the same as <b>2 L 50 mL</b>?", "2.05 L",
                   ["2.5 L", "2.005 L", "20.5 L"],
                   "50 mL = 50 ÷ 1000 = 0.05 L. So 2 L 50 mL = 2.05 L. 2.5 L would be 2 L 500 mL.",
                   rnd, want=("C", 2050)))
    its.append(mcq("A cricket oval is <b>1 km 60 m</b> around the outside. Which shows this in kilometres?", "1.06 km",
                   ["1.6 km", "1.006 km", "10.6 km"],
                   "60 m = 60 ÷ 1000 = 0.06 km. So 1 km 60 m = 1.06 km. 1.6 km would be 1 km 600 m.",
                   rnd, want=("L", 1060000)))
    assert len(its) == 20, len(its)
    return {"title": "Choose a sensible unit and decimal form", "items": its}


# ------------------------------------------------------------ set 4: compare and order
def set_compare(rnd):
    its = []

    def pick_one(q, ch, which, e):
        vals = [parse(x)[1] for x in ch]
        assert len(set(vals)) == 4 and len({parse(x)[0] for x in ch}) == 1
        best = (max if which == "max" else min)(range(4), key=lambda i: vals[i])
        its.append(mcq(q, ch[best], [x for i, x in enumerate(ch) if i != best], e, rnd))

    pick_one("Which is the longest?", ["0.5 km", "450 m", "5200 cm", "0.48 km"], "max",
             "Change them all to metres: 0.5 km = 500 m, 5200 cm = 52 m and 0.48 km = 480 m. "
             "500 m is the longest. 5200 cm has the biggest number, but centimetres are small.")
    pick_one("Which is the shortest?", ["6.5 cm", "0.07 m", "68 mm", "0.6 m"], "min",
             "Change them all to millimetres: 6.5 cm = 65 mm, 0.07 m = 70 mm and 0.6 m = 600 mm. "
             "65 mm is the shortest.")
    pick_one("Which is the heaviest?", ["1.2 kg", "1050 g", "0.95 kg", "1 kg 150 g"], "max",
             "Change them all to grams: 1.2 kg = 1200 g, 0.95 kg = 950 g and 1 kg 150 g = 1150 g. "
             "1200 g is the heaviest.")
    pick_one("Which is the lightest?", ["0.3 t", "350 kg", "0.32 t", "3100 kg"], "min",
             "Change them all to kilograms: 0.3 t = 300 kg and 0.32 t = 320 kg. 300 kg is the lightest. "
             "3100 kg is 3.1 t, the heaviest of all.")
    pick_one("Which holds the most?", ["1.5 L", "1250 mL", "0.9 L", "1 L 450 mL"], "max",
             "Change them all to millilitres: 1.5 L = 1500 mL, 0.9 L = 900 mL and 1 L 450 mL = 1450 mL. "
             "1500 mL is the most.")
    pick_one("Which holds the least?", ["0.75 L", "700 mL", "0.8 L", "705 mL"], "min",
             "Change them all to millilitres: 0.75 L = 750 mL and 0.8 L = 800 mL. 700 mL is the least.")
    pick_one("Which is the heaviest?", ["0.07 t", "65 kg", "7500 g", "69 kg"], "max",
             "Change them all to kilograms: 0.07 t = 0.07 × 1000 = 70 kg and 7500 g = 7.5 kg. "
             "70 kg is the heaviest. 7500 g has the biggest number, but grams are small.")

    def true_one(q, sts, e):
        assert [truth(s) for s in sts] == [True, False, False, False], sts
        its.append(mcq(q, sts[0], sts[1:], e, rnd))

    true_one("Which is true?", ["1.2 km = 1200 m", "0.3 m = 3 cm", "45 mm = 0.45 m", "2.5 m = 250 mm"],
             "1.2 × 1000 = 1200, so 1.2 km = 1200 m. The others are wrong: 0.3 m = 30 cm, "
             "45 mm = 0.045 m and 2.5 m = 2500 mm.")
    true_one("Which is true?", ["0.6 kg = 600 g", "0.6 kg = 60 g", "1.05 L = 1500 mL", "3 t > 3100 kg"],
             "0.6 × 1000 = 600, so 0.6 kg = 600 g. The others are wrong: 1.05 L = 1050 mL, "
             "and 3 t = 3000 kg, which is less than 3100 kg.")
    true_one("Which is true?", ["0.75 kg > 705 g", "0.5 L < 450 mL", "2.4 t < 2040 kg", "1.5 m < 105 cm"],
             "0.75 kg = 750 g, and 750 g &gt; 705 g. The others are wrong: 0.5 L = 500 mL, 2.4 t = 2400 kg "
             "and 1.5 m = 150 cm.")
    true_one("Which is true?", ["3.5 km > 3050 m", "0.8 m > 85 cm", "250 g > 0.3 kg", "1.25 L < 1200 mL"],
             "3.5 km = 3500 m, and 3500 m &gt; 3050 m. The others are wrong: 0.8 m = 80 cm, 0.3 kg = 300 g "
             "and 1.25 L = 1250 mL.")
    true_one("Which list goes from the smallest to the largest capacity?",
             ["0.25 L < 400 mL < 0.5 L", "0.5 L < 400 mL < 0.25 L", "400 mL < 0.25 L < 0.5 L",
              "0.25 L < 0.5 L < 400 mL"],
             "Change them all to millilitres: 0.25 L = 250 mL and 0.5 L = 500 mL. 250 &lt; 400 &lt; 500.")
    true_one("Which list goes from the shortest to the longest?",
             ["0.09 km < 95 m < 9600 cm", "9600 cm < 95 m < 0.09 km", "95 m < 9600 cm < 0.09 km",
              "0.09 km < 9600 cm < 95 m"],
             "Change them all to metres: 0.09 km = 90 m and 9600 cm = 96 m. 90 &lt; 95 &lt; 96.")
    true_one("Which list goes from the heaviest to the lightest?",
             ["2.5 t > 2.25 t > 2050 kg", "2050 kg > 2.5 t > 2.25 t", "2.25 t > 2.5 t > 2050 kg",
              "2.5 t > 2050 kg > 2.25 t"],
             "Change them all to kilograms: 2.5 t = 2500 kg and 2.25 t = 2250 kg. 2500 &gt; 2250 &gt; 2050. "
             "2.25 is not more than 2.5: compare the tenths first.")
    order = ["1150 mm", "1.2 m", "125 cm", "0.13 km"]
    assert truth(" < ".join(order))
    its.append(mcq("Put these in order from shortest to longest: <b>1.2 m, 125 cm, 1150 mm, 0.13 km</b>",
                   ", ".join(order),
                   ["0.13 km, 1.2 m, 125 cm, 1150 mm", "1.2 m, 125 cm, 1150 mm, 0.13 km",
                    "1150 mm, 125 cm, 1.2 m, 0.13 km"],
                   "Change them all to centimetres: 1.2 m = 120 cm, 1150 mm = 115 cm and 0.13 km = 130 m = 13 000 cm. "
                   "115 &lt; 120 &lt; 125 &lt; 13 000. (0.13 km has the smallest number but is by far the longest.)"
                   .replace("13 000", "13" + NBSP + "000"), rnd))
    # the three wrong choices are equal to each other on purpose, so build this item without mcq()
    ch = ["1200 m", "1 km 200 m", "120" + NBSP + "000 cm", "120 m"]
    assert [parse(x)[1] for x in ch] == [1200000, 1200000, 1200000, 120000]
    rnd.shuffle(ch)
    its.append({"q": "Which is <b>not</b> the same as 1.2 km?", "c": ch, "a": ch.index("120 m"),
                "e": "1.2 km = 1.2 × 1000 = 1200 m = 1 km 200 m. 1200 m = 1200 × 100 = 120" + NBSP + "000 cm. "
                     "120 m multiplies by 100 instead of 1000."})
    assert parse("120" + NBSP + "000 cm") == ("L", 1200000) and parse("1 km 200 m") == ("L", 1200000)
    its.append(mcq("Which two measurements are equal?", "0.4 kg and 400 g",
                   ["0.4 kg and 40 g", "4 kg and 400 g", "0.04 kg and 400 g"],
                   "0.4 × 1000 = 400, so 0.4 kg = 400 g. 4 kg = 4000 g and 0.04 kg = 40 g.", rnd))
    assert parse("0.4 kg") == parse("400 g")
    its.append(mcq("How much longer is <b>1.5 m</b> than <b>105 cm</b>?", "45 cm",
                   ["55 cm", "1395 cm", "0.45 cm"],
                   "Use one unit: 1.5 m = 150 cm. 150 − 105 = 45 cm. "
                   "(1395 cm treats 1.5 m as 1500 cm, and 0.45 cm puts the wrong unit on 0.45 m.)",
                   rnd, want=("L", 450)))
    its.append(mcq("How much more is <b>2 L</b> than <b>1250 mL</b>?", "750 mL",
                   ["850 mL", "1248 mL", "3250 mL"],
                   "Use one unit: 2 L = 2000 mL. 2000 − 1250 = 750 mL. "
                   "(1248 mL takes away 2 without converting, and 3250 mL adds instead of subtracting.)",
                   rnd, want=("C", 750)))
    its.append(mcq("Lachlan says <b>0.5 kg is less than 450 g</b>, because 0.5 is smaller than 450. Is he right?",
                   "No. 0.5 kg = 500 g, which is more than 450 g.",
                   ["Yes. 0.5 is smaller than 450.", "No. 0.5 kg = 50 g, so they are equal.",
                    "Yes. 0.5 kg = 5 g, which is less."],
                   "Compare in the same unit. 0.5 × 1000 = 500, so 0.5 kg = 500 g, and 500 g &gt; 450 g.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Compare and order mixed units", "items": its}


# ------------------------------------------------------------ set 5: word problems
def set_story(rnd):
    its = []

    def add(q, r, w, e, want=None):
        its.append(mcq(q, r, w, e, rnd, want=want))

    add("The school fun run is 5 km. It goes around a 400 m track. How many laps is that?",
        "12.5 laps", ["125 laps", "1.25 laps", "12 laps"],
        "5 km = 5000 m. 5000 ÷ 400 = 12.5 laps. Check: 12 × 400 = 4800 m, and half a lap is 200 m more.")
    add("Charlotte has run 3.2 km of the 5 km fun run. How many metres does she have left?",
        "1800 m", ["2800 m", "1.8 m", "180 m"],
        "5 − 3.2 = 1.8 km left. 1.8 × 1000 = 1800 m. (2800 m is a regrouping slip: 5000 − 3200 is 1800.)",
        ("L", 1800000))
    add("Oliver makes pancakes. One batch needs 0.3 kg of flour. He makes 3 batches from a 1.5 kg bag. "
        "How many grams of flour are left?",
        "600 g", ["1200 g", "60 g", "1410 g"],
        "3 × 0.3 = 0.9 kg used. 1.5 − 0.9 = 0.6 kg left. 0.6 × 1000 = 600 g. "
        "(1200 g only takes away one batch.)", ("M", 600))
    add("A recipe for 4 people uses 250 mL of milk. How many litres of milk are needed for 10 people?",
        "0.625 L", ["6.25 L", "2.5 L", "1 L"],
        "250 ÷ 4 = 62.5 mL for each person. 10 × 62.5 = 625 mL. 625 ÷ 1000 = 0.625 L. "
        "(2.5 L uses 250 mL for each person.)", ("C", 625))
    add("An Anzac biscuit recipe uses 125 g of butter to make 12 biscuits. Isla wants to make 36 biscuits. "
        "How many kilograms of butter does she need?",
        "0.375 kg", ["3.75 kg", "0.125 kg", "37.5 kg"],
        "36 biscuits is 3 times 12, so 3 × 125 = 375 g. 375 ÷ 1000 = 0.375 kg. (3.75 kg divides by 100.)",
        ("M", 375))
    add("Noah drinks 4 full 750 mL water bottles on a hot day. How many litres is that?",
        "3 L", ["30 L", "0.3 L", "300 L"],
        "4 × 750 = 3000 mL. 1 L = 1000 mL, so 3000 ÷ 1000 = 3 L. (30 L divides by 100.)", ("C", 3000))
    add("How many 600 mL bottles can be filled from a 15 L water cooler?",
        "25 bottles", ["2.5 bottles", "250 bottles", "40 bottles"],
        "15 L = 15 000 mL. 15 000 ÷ 600 = 25 bottles. Check: 25 × 600 = 15 000 mL. "
        "(40 bottles divides 600 by 15.)".replace("15 000", "15" + NBSP + "000"))
    add("25 students each take a 750 mL water bottle on an excursion. How many litres of water is that altogether?",
        "18.75 L", ["187.5 L", "1.875 L", "18" + NBSP + "750 L"],
        "25 × 750 = 18" + NBSP + "750 mL. 18" + NBSP + "750 ÷ 1000 = 18.75 L. (187.5 L divides by 100, and 18" + NBSP + "750 L forgets to change millilitres into litres.)",
        ("C", 18750))
    add("A small truck can carry 2.4 t. Each bag of cement has a mass of 40 kg. How many bags can it carry?",
        "60 bags", ["6 bags", "600 bags", "96 bags"],
        "2.4 t = 2400 kg. 2400 ÷ 40 = 60 bags. (6 bags uses 2.4 t = 240 kg, and 96 bags multiplies 2.4 × 40.)")
    add("An empty truck has a mass of 2.4 t. It is loaded with 850 kg of bricks. What is the total mass in tonnes?",
        "3.25 t", ["10.9 t", "2.485 t", "852.4 t"],
        "850 kg = 850 ÷ 1000 = 0.85 t. 2.4 + 0.85 = 3.25 t. "
        "(10.9 t treats 850 kg as 8.5 t, and 852.4 t adds without converting.)", ("M", 3250000))
    add("A truck carries 2.4 t of sand. It drops off 650 kg at each of 3 houses. How much sand is left, in kilograms?",
        "450 kg", ["1750 kg", "45 kg", "1950 kg"],
        "2.4 t = 2400 kg. 3 × 650 = 1950 kg dropped off. 2400 − 1950 = 450 kg left. "
        "(1750 kg takes away only one load, and 1950 kg is the sand dropped off.)", ("M", 450000))
    add("Jack posts three parcels: 1.25 kg, 750 g and 2.4 kg. What is their total mass in kilograms?",
        "4.4 kg", ["753.65 kg", "11.15 kg", "3.725 kg"],
        "Change 750 g to kilograms first: 750 ÷ 1000 = 0.75 kg. 1.25 + 0.75 + 2.4 = 4.4 kg. "
        "(11.15 kg treats 750 g as 7.5 kg.)", ("M", 4400))
    add("At the athletics carnival, Oliver jumps 1.6 m, Ava jumps 155 cm, Leo jumps 1580 mm and Ruby jumps 1.06 m. "
        "Who jumps the furthest?",
        "Oliver", ["Ava", "Leo", "Ruby"],
        "Change them all to centimetres: 1.6 m = 160 cm, 1580 mm = 158 cm and 1.06 m = 106 cm. "
        "160 cm is the furthest, so Oliver jumps the furthest.")
    add("Kai swims 1.2 km at training in a 25 m pool. How many lengths does he swim?",
        "48 lengths", ["4.8 lengths", "480 lengths", "24 lengths"],
        "1.2 km = 1200 m. 1200 ÷ 25 = 48 lengths. Check: 48 × 25 = 1200. (24 lengths counts there and back, 50 m, as one length.)")
    add("Grace has 4.5 m of ribbon. She cuts it into pieces 15 cm long. How many pieces does she get?",
        "30 pieces", ["3 pieces", "300 pieces", "60 pieces"],
        "4.5 m = 450 cm. 450 ÷ 15 = 30 pieces. (3 pieces divides 45 by 15 without converting.)")
    add("A school bushwalk is 12 km. The class walks 2.75 km before lunch and 3600 m after lunch. "
        "How much further do they still have to walk?",
        "5.65 km", ["8.89 km", "6.35 km", "6.65 km"],
        "3600 m = 3.6 km. 2.75 + 3.6 = 6.35 km walked. 12 − 6.35 = 5.65 km to go. "
        "(8.89 km treats 3600 m as 0.36 km.)", ("L", 5650000))
    add("A 2 L carton of juice is poured into 8 cups of 180 mL each. How many millilitres are left in the carton?",
        "560 mL", ["1440 mL", "1820 mL", "56 mL"],
        "8 × 180 = 1440 mL poured. 2 L = 2000 mL. 2000 − 1440 = 560 mL left. "
        "(1820 mL takes away only one cup.)", ("C", 560))
    add("A box of 24 apples has a mass of 3.6 kg. Each apple has the same mass. What is the mass of one apple in grams?",
        "150 g", ["15 g", "1.5 g", "86.4 g"],
        "3.6 kg = 3600 g. 3600 ÷ 24 = 150 g. (15 g changes 3.6 kg into 360 g, and 86.4 g multiplies 3.6 × 24.)",
        ("M", 150))
    add("The canteen buys 6 kg of sausages for a sausage sizzle. Each sausage has a mass of 75 g. "
        "How many sausages is that?",
        "80 sausages", ["8 sausages", "800 sausages", "450 sausages"],
        "6 kg = 6000 g. 6000 ÷ 75 = 80 sausages. Check: 80 × 75 = 6000. (450 sausages multiplies 6 × 75.)")
    add("Ava was 1.38 m tall last year. Since then she has grown 6 cm. How tall is she now, in metres?",
        "1.44 m", ["1.98 m", "7.38 m", "1.386 m"],
        "6 cm = 6 ÷ 100 = 0.06 m. 1.38 + 0.06 = 1.44 m. "
        "(1.98 m adds 0.6 m, and 7.38 m adds 6 m.)", ("L", 1440))
    assert len(its) == 20, len(its)
    return {"title": "Word problems: recipes, fun runs, water bottles and trucks", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % x for x in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


def body_html():
    return (
        "<h2>Multiply or divide?</h2>"
        "<p>To change a bigger unit into a smaller unit, <b>multiply</b>: you need more of the small units. "
        "To change a smaller unit into a bigger unit, <b>divide</b>. "
        "Multiplying by 1000 moves every digit 3 places to the left. Dividing by 1000 moves every digit "
        "3 places to the right.</p>"
        "<figure class='sn-fig'>" + ladder_svg(["km", "m", "cm", "mm"], ["1000", "100", "10"],
                                                "length units: km to m to cm to mm") +
        "<figcaption>Going to a smaller unit: multiply. Going to a bigger unit: divide.</figcaption></figure>"
        "<figure class='sn-fig'>" + ladder_svg(["t", "kg", "g"], ["1000", "1000"], "mass units: t to kg to g") +
        "<figcaption>Mass: 1 t = 1000 kg and 1 kg = 1000 g. Capacity: 1 L = 1000 mL.</figcaption></figure>" +
        ex("Metres to centimetres", "1.25 m = ☐ cm", "1 m = 100 cm. Multiply: 1.25 × 100 = 125.", "125 cm") +
        ex("Grams to kilograms", "750 g = ☐ kg", "1 kg = 1000 g. Divide: 750 ÷ 1000 = 0.75.", "0.75 kg") +
        ex("Litres to millilitres", "2.5 L = ☐ mL", "1 L = 1000 mL. Multiply: 2.5 × 1000 = 2500.", "2500 mL") +
        "<h2>Facts to know</h2>" +
        table(["Measure", "Facts"], [
            ["Length", "1 cm = 10 mm &nbsp; 1 m = 100 cm = 1000 mm &nbsp; 1 km = 1000 m"],
            ["Mass", "1 kg = 1000 g &nbsp; 1 t = 1000 kg"],
            ["Capacity", "1 L = 1000 mL"],
        ]) +
        "<h2>Choose a sensible unit and decimal form</h2>"
        "<p>Pick the unit that gives an easy number for the situation. A board is 2.45 m, not 0.002" + NBSP +
        "45 km. An ant is 6 mm, not 0.006 m. Two units together can be written as one decimal.</p>" +
        ex("Two units as a decimal", "3 kg 40 g = ☐ kg",
           "40 g = 40 ÷ 1000 = 0.04 kg. Keep the 0 in the tenths place.", "3.04 kg (not 3.4 kg)") +
        "<h2>Read the scale, then convert</h2>"
        "<figure class='sn-fig'>" + jug_svg(1300, 2000, 500, 100) +
        "<figcaption>Each line is 100 mL. The water is at 1300 mL, which is 1.3 L.</figcaption></figure>"
        "<h2>Compare in one unit</h2>"
        "<p>To compare or order, change every measurement into the same unit first.</p>" +
        ex("Which is longer?", "0.5 km or 5200 cm?",
           "0.5 km = 500 m. 5200 cm = 52 m. 500 m is longer.", "0.5 km") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["2.5 kg = 250 g (multiplying by 100)", "1 kg = 1000 g, so 2.5 kg = 2500 g"],
            ["750 g = 750" + NBSP + "000 kg (moving the point the wrong way)",
             "Smaller unit to bigger unit: divide. 750 g = 0.75 kg"],
            ["1.5 m = 105 cm", "1.5 m is 1 m 50 cm, so 1.5 m = 150 cm"],
            ["3 kg 40 g = 3.4 kg", "40 g = 0.04 kg, so 3 kg 40 g = 3.04 kg"],
            ["Comparing only the numbers (5200 cm &gt; 0.5 km)", "Use one unit first: 5200 cm = 52 m and 0.5 km = 500 m"],
        ])
    )


FAQ = [
    {"q": "What metric conversions do Year 6 students learn in the Australian Curriculum?",
     "a": "Year 6 students convert between mm, cm, m and km, between g, kg and t, and between mL and L, "
          "and they use decimals such as 1.25 m = 125 cm and 750 g = 0.75 kg."},
    {"q": "How do you convert 1.5 m to centimetres?",
     "a": "Multiply by 100, because 1 m = 100 cm: 1.5 × 100 = 150 cm. It is not 105 cm, because 0.5 m is half a metre, 50 cm."},
    {"q": "How many kilograms are in a tonne?",
     "a": "1 tonne = 1000 kg. So a 2.4 t truck load is 2.4 × 1000 = 2400 kg, and 3500 kg = 3.5 t."},
    {"q": "Is converting metric units tested in NAPLAN?",
     "a": "Year 6 students do not sit NAPLAN, but measurement, including converting units, is part of the "
          "NAPLAN numeracy test in Years 7 and 9. Practising it in Year 6 is good preparation for high school."},
]


def balance(sets, rnd):
    """Spread the correct answers evenly over the 4 positions in every set."""
    for s in sets:
        targets = [0, 1, 2, 3] * 5
        rnd.shuffle(targets)
        for it, t in zip(s["items"], targets):
            ch = it["c"]
            ch[it["a"]], ch[t] = ch[t], ch[it["a"]]
            it["a"] = t


def gen_unit():
    rnd = random.Random(6812)
    sets = [set_length(rnd), set_mass_cap(rnd), set_sensible(rnd), set_compare(rnd), set_story(rnd)]
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
        "country": "au", "subject": "maths", "grade": "year-6", "slug": "converting-metric-units", "sort": 12,
        "updated": UPDATED, "pdf_url": "",
        "title": "Year 6 Converting Metric Units: Length, Mass and Capacity",
        "seo_title": "Year 6 Converting Metric Units Worksheets: mm, cm, m, km, g, kg, t, mL and L (Free Maths with Answer Key)",
        "short_title": "Converting Metric Units",
        "domain": "Measurement",
        "standard_code": "AC9M6M01",
        "standard_url": "https://v9.australiancurriculum.edu.au/f-10-curriculum/learning-areas/mathematics",
        "standard_text": "Convert between common metric units of length, mass and capacity; choose and use decimal "
                         "representations of metric measurements relevant to the situation",
        "meta_desc": "Free Year 6 maths worksheets on converting metric units, aligned to the Australian Curriculum "
                     "(AC9M6M01): mm, cm, m and km, g, kg and t, mL and L with decimals, choosing sensible units, "
                     "comparing mixed units and word problems. 100 questions with an answer key.",
        "key_big": "Bigger unit to smaller unit: multiply. Smaller unit to bigger unit: divide.",
        "key_sub": "1 m = 100 cm, 1 kg = 1000 g, 1 t = 1000 kg and 1 L = 1000 mL. So 1.25 m = 125 cm, "
                   "750 g = 0.75 kg and 2.5 L = 2500 mL.",
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
    mark_large(u, "ruler")
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
