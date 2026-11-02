# -*- coding: utf-8 -*-
"""
AU Year 5 Maths: Metric Units (Australian Curriculum v9.0, AC9M5M01)
  python3 tools/gen_au_maths_y5_metric_units.py
Choose appropriate metric units for length, mass and capacity; use smaller units or a combination of
units (1 m 35 cm, 2 kg 400 g, 1 L 250 mL) for a more accurate measure; convert with simple decimals.
HTML attributes use single quotes (no backslashes in the JSON).
Australian English, metric units only, mL and L with a capital L.
Australian number style: 4-digit numbers plain (2400 g), 5 or more digits grouped with a no-break space.
Every measurement answer is parsed back to a base unit (mm, g, mL) and checked in code, and measurement
choices in a question never have the same value.
Wrong answers come from real mistakes: 1 m = 10 cm or 1000 cm, 2 kg 40 g = 240 g, reading the wrong
interval on a scale, forgetting that an object does not start at 0, and multiplying instead of dividing.
"""
import json, math, os, random, re
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "au", "maths", "year-5")
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
def set_units(rnd):
    its = []
    for obj, ans, wr, e in [
        ("the length of an ant", "mm", ["cm", "m", "g"],
         "Most ants are shorter than 1 cm, so use millimetres. A centimetre is too big to show its length well."),
        ("the length of a netball court", "m", ["cm", "km", "mm"],
         "A netball court is about 30 m long. You can walk along it in under a minute, so use metres."),
        ("the distance from Sydney to Canberra", "km", ["m", "cm", "kg"],
         "Sydney to Canberra is a long drive of a few hours, so use kilometres."),
        ("the mass of a watermelon", "kg", ["g", "t", "L"],
         "A watermelon is heavy to carry but much lighter than a car, so use kilograms. Tonnes are for very heavy "
         "things like trucks."),
        ("the mass of a 20c coin", "g", ["kg", "t", "mL"],
         "A coin is very light, so use grams. A 20c coin has a mass of about 11 g."),
        ("the mass of a loaded truck", "t", ["kg", "g", "km"],
         "A loaded truck is very heavy, so use tonnes. 1 t = 1000 kg."),
        ("how much medicine fits on a teaspoon", "mL", ["L", "g", "mm"],
         "A teaspoon holds only a little, about 5 mL, so use millilitres."),
        ("how much water a bathtub holds", "L", ["mL", "kg", "m"],
         "A bathtub holds a lot of water, so use litres. Kilograms measure mass, not capacity."),
        ("the height of a tall gum tree", "m", ["cm", "km", "mm"],
         "A tall gum tree is many metres high. Centimetres would give a huge number, and kilometres are far too big."),
        ("the thickness of a $1 coin", "mm", ["cm", "m", "g"],
         "A coin is only a few millimetres thick. That is much less than 1 cm, so use millimetres."),
        ("the length of a pencil case", "cm", ["km", "m", "mL"],
         "A pencil case fits on a 30 cm ruler, so use centimetres."),
        ("the mass of a kangaroo", "kg", ["g", "t", "L"],
         "A grown kangaroo is about as heavy as an adult person, so use kilograms."),
        ("how much a can of soft drink holds", "mL", ["L", "g", "kg"],
         "A can holds less than 1 litre (375 mL), so use millilitres. Grams and kilograms measure mass."),
        ("the length of a marathon race", "km", ["m", "cm", "kg"],
         "A marathon is about 42 km. It takes runners hours, so use kilometres."),
    ]:
        its.append(mcq("Which unit is best to measure <b>%s</b>?" % obj, ans, wr, e, rnd))
    for q, ans, wr, e in [
        ("the mass of a family car", "about 1500 kg", ["about 1500 g", "about 15 kg", "about 150 t"],
         "A family car is about 1500 kg, which is 1.5 t. 1500 g is only as heavy as one and a half bags of sugar."),
        ("the capacity of a school water bottle", "about 750 mL", ["about 750 L", "about 75 L", "about 7 mL"],
         "Most drink bottles hold 500 mL to 1 L, so 750 mL fits. 75 L would fill a big rubbish bin."),
        ("the height of a Year 5 student", "about 140 cm", ["about 140 m", "about 140 mm", "about 14 cm"],
         "Most Year 5 students are between 1 m 30 cm and 1 m 50 cm tall, so 140 cm fits. "
         "140 mm is only 14 cm, the size of a hand."),
    ]:
        its.append(mcq("Choose the best estimate for <b>%s</b>." % q, ans, wr, e, rnd))
    its.append(mcq("Jack measures his book. It is between 24 cm and 25 cm long. Which unit should he use to give a "
                   "<b>more accurate</b> measure?", "millimetres", ["metres", "kilometres", "grams"],
                   "A smaller unit gives a more accurate measure. 1 cm = 10 mm, so he can measure to the nearest "
                   "millimetre, for example 247 mm.", rnd))
    its.append(mcq("Mia’s bag of apples is between 1 kg and 2 kg. Which is the <b>most accurate</b> way to record "
                   "its mass?", "1 kg 350 g", ["about 1 kg", "about 2 kg", "less than 2 kg"],
                   "Using kilograms and grams together gives a more accurate measure than whole kilograms. "
                   "1 kg 350 g tells exactly where the mass is between 1 kg and 2 kg.", rnd))
    its.append(mcq("Which measure of a pencil is the <b>most accurate</b>?", "164 mm",
                   ["16 cm", "about 20 cm", "less than 1 m"],
                   "Millimetres are the smallest unit here. 164 mm (16 cm 4 mm) is more accurate than 16 cm, "
                   "which leaves out the extra 4 mm.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Choose the best metric unit", "items": its}


# ------------------------------------------------------------ set 2: read instruments
def set_read(rnd):
    its = []
    q = fig(ruler_svg(0, 74, "pencil")) + "How long is the pencil? Give your answer in millimetres."
    its.append(mcq(q, "74 mm", ["74 cm", "70 mm", "80 mm"],
                   "The pencil starts at 0. It ends 4 small marks past 7 cm. 7 cm = 70 mm, and 70 + 4 = 74 mm. "
                   "(80 mm reads the next number, 8, instead of counting the small marks.)", rnd, want=("L", 74)))
    q = fig(ruler_svg(20, 83, "crayon")) + "How long is the crayon? Give your answer in cm and mm."
    its.append(mcq(q, "6 cm 3 mm", ["8 cm 3 mm", "7 cm 3 mm", "6 cm 7 mm"],
                   "The crayon starts at 2 cm, not 0. It ends at 8 cm 3 mm. 83 mm − 20 mm = 63 mm = 6 cm 3 mm. "
                   "(8 cm 3 mm forgets that the crayon does not start at 0.)", rnd, want=("L", 63)))
    q = fig(ruler_svg(10, 48, "eraser")) + "How long is the eraser in millimetres?"
    its.append(mcq(q, "38 mm", ["48 mm", "38 cm", "30 mm"],
                   "The eraser starts at 1 cm (10 mm) and ends at 48 mm. 48 − 10 = 38 mm. "
                   "(48 mm forgets that it starts at 1 cm. 30 mm counts only the whole centimetres.)",
                   rnd, want=("L", 38)))
    q = fig(ruler_svg(0, 105, "ribbon", 12)) + "How long is the ribbon in millimetres?"
    its.append(mcq(q, "105 mm", ["10.5 mm", "150 mm", "100 mm"],
                   "The ribbon ends 5 small marks past 10 cm. 10 cm = 100 mm, and 100 + 5 = 105 mm. "
                   "(150 mm reads 10 cm 5 mm as 1 and 50.)", rnd, want=("L", 105)))
    q = fig(ruler_svg(0, 97, "pencil", 11)) + "Which is the <b>most accurate</b> measure of the pencil?"
    its.append(mcq(q, "9 cm 7 mm", ["9 cm", "10 cm", "97 cm"],
                   "The pencil ends 7 small marks past 9 cm, so it is 9 cm 7 mm (97 mm). 9 cm and 10 cm are "
                   "only to the nearest centimetre. 97 cm uses the wrong unit.", rnd, want=("L", 97)))
    q = fig(ruler_svg(0, 58, "crayon")) + "Lachlan says the crayon is about 6 cm long. What is a more accurate measure?"
    its.append(mcq(q, "5 cm 8 mm", ["6 cm 8 mm", "5 cm", "58 cm"],
                   "The crayon ends 8 small marks past 5 cm, so it is 5 cm 8 mm (58 mm). "
                   "6 cm is the nearest whole centimetre, but 5 cm 8 mm is more accurate.", rnd, want=("L", 58)))
    # scales
    for v, mx, lab, tick, div, obj, wrong, note in [
        (1400, 3000, 1000, 100, 1000, "a pumpkin", ["1 kg 40 g", "1 kg 4 g", "1 kg 800 g"],
         " (1 kg 40 g counts each mark as 10 g.)"),
        (2750, 4000, 1000, 250, 1000, "a bag of potatoes", ["2 kg 300 g", "2 kg 3 g", "3 kg 750 g"],
         " (2 kg 300 g counts each mark as 100 g.)"),
        (3600, 5000, 1000, 200, 1000, "a pile of library books", ["3 kg 300 g", "3 kg 3 g", "3 kg 60 g"],
         " (3 kg 300 g counts each mark as 100 g.)"),
        (650, 1000, 200, 50, 1, "a bunch of bananas", ["610 g", "700 g", "625 g"],
         " (610 g counts each mark as 10 g, and 700 g counts each mark as 100 g.)"),
        (360, 500, 100, 20, 1, "a block of cheese", ["330 g", "400 g", "36 g"],
         " (330 g counts each mark as 10 g. 400 g reads the next number.)"),
        (1800, 2000, 500, 100, 1, "a bag of flour", ["1530 g", "2000 g", "1300 g"],
         " (1530 g counts each mark as 10 g.)"),
    ]:
        q = fig(dial_svg(v, mx, lab, tick, div)) + "The scale shows the mass of %s. What is the mass?" % obj
        ans = kgg(v) if div == 1000 else m(v, "g")
        its.append(mcq(q, ans, wrong, dial_e(v, lab, tick, div) + note, rnd, want=("M", v)))
    q = fig(dial_svg(1300, 3000, 1000, 100, 1000)) + ("The scale shows a bag of rice. How much more rice is needed "
                                                      "to make 2 kg?")
    its.append(mcq(q, "700 g", ["1300 g", "1700 g", "7 g"],
                   "Each mark is 100 g, so the needle is at 1 kg 300 g = 1300 g. 2 kg = 2000 g. "
                   "2000 − 1300 = 700 g more.", rnd, want=("M", 700)))
    # jugs
    for v, mx, lab, step, div, ask, ansf, wrong, note in [
        (1250, 2000, 500, 250, 1, "Give your answer in L and mL.", lml, ["1 L 25 mL", "1 L 100 mL", "1 L 500 mL"],
         " (1 L 100 mL counts each line as 100 mL.)"),
        (750, 1000, 200, 50, 1, "", None, ["630 mL", "900 mL", "800 mL"],
         " (630 mL counts each line as 10 mL, and 900 mL counts each line as 100 mL.)"),
        (2500, 3000, 1000, 250, 1000, "Give your answer in L and mL.", lml, ["2 L 200 mL", "2 L 2 mL", "3 L"],
         " (2 L 200 mL counts each line as 100 mL.)"),
        (1750, 3000, 1000, 250, 1000, "Give your answer in millilitres.", None, ["1300 mL", "175 mL", "2000 mL"],
         " (1300 mL counts each line as 100 mL.)"),
        (440, 500, 100, 20, 1, "", None, ["420 mL", "402 mL", "500 mL"],
         " (420 mL counts each line as 10 mL.)"),
        (850, 1000, 250, 50, 1, "", None, ["770 mL", "950 mL", "1000 mL"],
         " (770 mL counts each line as 10 mL.)"),
    ]:
        q = fig(jug_svg(v, mx, lab, step, div)) + ("How much water is in the jug? " + ask).strip()
        ans = ansf(v) if ansf else m(v, "mL")
        its.append(mcq(q, ans, wrong, jug_e(v, lab, step, div) + note, rnd, want=("C", v)))
    q = fig(jug_svg(1400, 2000, 500, 100)) + "How much more water is needed to fill the jug to 2 L?"
    its.append(mcq(q, "600 mL", ["1400 mL", "1600 mL", "700 mL"],
                   "Each line is 100 mL, so the water is at 1400 mL. 2 L = 2000 mL. 2000 − 1400 = 600 mL more. "
                   "(1400 mL is the water already in the jug.)", rnd, want=("C", 600)))
    assert len(its) == 20, len(its)
    return {"title": "Read rulers, scales and jugs accurately", "items": its}


# ------------------------------------------------------------ set 3: combine units
def set_combine(rnd):
    its = []

    def add(q, ans, wr, e, want=None):
        its.append(mcq(q, ans, wr, e, rnd, want=want))
    add("<b>1 m 35 cm = ☐ cm</b>", "135 cm", ["1035 cm", "45 cm", "36 cm"],
        "1 m = 100 cm. 100 + 35 = 135 cm. (45 cm uses 1 m = 10 cm. 1035 cm uses 1 m = 1000 cm.)", ("L", 1350))
    add("<b>2 kg 400 g = ☐ g</b>", "2400 g", ["600 g", "2004 g", "240 g"],
        "1 kg = 1000 g, so 2 kg = 2000 g. 2000 + 400 = 2400 g. (600 g uses 1 kg = 100 g.)", ("M", 2400))
    add("<b>1 L 250 mL = ☐ mL</b>", "1250 mL", ["350 mL", "251 mL", "1025 mL"],
        "1 L = 1000 mL. 1000 + 250 = 1250 mL. (350 mL uses 1 L = 100 mL. 251 mL adds 1 + 250.)", ("C", 1250))
    add("<b>2 kg 40 g = ☐ g</b>", "2040 g", ["240 g", "2400 g", "2004 g"],
        "2 kg = 2000 g. 2000 + 40 = 2040 g. The 40 g is 4 tens, so the hundreds digit is 0. "
        "(240 g just joins 2 and 40. 2400 g puts the 4 in the hundreds place.)", ("M", 2040))
    add("<b>3 m 5 cm = ☐ cm</b>", "305 cm", ["35 cm", "350 cm", "3005 cm"],
        "3 m = 300 cm. 300 + 5 = 305 cm. (35 cm just joins 3 and 5. 350 cm would be 3 m 50 cm.)", ("L", 3050))
    add("<b>4 cm 7 mm = ☐ mm</b>", "47 mm", ["407 mm", "11 mm", "470 mm"],
        "1 cm = 10 mm, so 4 cm = 40 mm. 40 + 7 = 47 mm. (407 mm uses 1 cm = 100 mm. 11 mm adds 4 + 7.)", ("L", 47))
    add("<b>1 km 200 m = ☐ m</b>", "1200 m", ["300 m", "1020 m", "12" + NBSP + "000 m"],
        "1 km = 1000 m. 1000 + 200 = 1200 m. (300 m uses 1 km = 100 m.)", ("L", 1200000))
    add("<b>3 L 75 mL = ☐ mL</b>", "3075 mL", ["375 mL", "3750 mL", "78 mL"],
        "3 L = 3000 mL. 3000 + 75 = 3075 mL. (3750 mL would be 3 L 750 mL.)", ("C", 3075))
    add("<b>2 t 300 kg = ☐ kg</b>", "2300 kg", ["230 kg", "2030 kg", "500 kg"],
        "1 t = 1000 kg, so 2 t = 2000 kg. 2000 + 300 = 2300 kg. (500 kg uses 1 t = 100 kg.)", ("M", 2300000))
    add("<b>165 cm = ☐ m ☐ cm</b>", "1 m 65 cm", ["16 m 5 cm", "165 m", "1 m 56 cm"],
        "100 cm = 1 m. 165 − 100 = 65, so 165 cm = 1 m 65 cm. (16 m 5 cm uses 1 m = 10 cm.)", ("L", 1650))
    add("<b>2075 g = ☐ kg ☐ g</b>", "2 kg 75 g", ["2 kg 750 g", "20 kg 75 g", "207 kg 5 g"],
        "2000 g = 2 kg. 2075 − 2000 = 75, so 2075 g = 2 kg 75 g. (2 kg 750 g would be 2750 g.)", ("M", 2075))
    add("<b>1650 mL = ☐ L ☐ mL</b>", "1 L 650 mL", ["16 L 50 mL", "1 L 65 mL", "165 L"],
        "1000 mL = 1 L. 1650 − 1000 = 650, so 1650 mL = 1 L 650 mL. (16 L 50 mL uses 1 L = 100 mL.)", ("C", 1650))
    add("<b>3040 m = ☐ km ☐ m</b>", "3 km 40 m", ["3 km 400 m", "30 km 40 m", "3 km 4 m"],
        "3000 m = 3 km. 3040 − 3000 = 40, so 3040 m = 3 km 40 m. (3 km 400 m would be 3400 m.)", ("L", 3040000))
    add("<b>58 mm = ☐ cm ☐ mm</b>", "5 cm 8 mm", ["58 cm", "50 cm 8 mm", "5 cm 80 mm"],
        "10 mm = 1 cm, so 50 mm = 5 cm. 58 − 50 = 8, so 58 mm = 5 cm 8 mm.", ("L", 58))
    ch = ["1 m 80 cm", "1 m 8 cm", "118 cm", "170 cm"]
    assert [parse(x)[1] for x in ch] == [1800, 1080, 1180, 1700]
    add("Which is the <b>longest</b>?", ch[0], ch[1:],
        "Change them all to centimetres: 1 m 80 cm = 180 cm and 1 m 8 cm = 108 cm. "
        "180 cm is more than 170 cm and 118 cm, so 1 m 80 cm is the longest.")
    ch = ["2500 g", "2 kg 50 g", "2 kg 5 g", "2 kg 400 g"]
    assert [parse(x)[1] for x in ch] == [2500, 2050, 2005, 2400]
    add("Which is the <b>heaviest</b>?", ch[0], ch[1:],
        "Change them all to grams: 2 kg 50 g = 2050 g, 2 kg 5 g = 2005 g and 2 kg 400 g = 2400 g. "
        "2500 g is the heaviest.")
    add("Which is the same as <b>1 L 500 mL</b>?", "1500 mL", ["150 mL", "1050 mL", "1 L 5 mL"],
        "1 L = 1000 mL. 1000 + 500 = 1500 mL. (1050 mL would be 1 L 50 mL.)", ("C", 1500))
    add("<b>1 m 60 cm + 70 cm = ?</b>", "2 m 30 cm", ["1 m 30 cm", "2 m 130 cm", "2 m 3 cm"],
        "60 cm + 70 cm = 130 cm. 130 cm = 1 m 30 cm, so trade 100 cm for 1 m: 1 m + 1 m 30 cm = 2 m 30 cm. "
        "(1 m 30 cm forgets to add the traded metre. 2 m 3 cm reads 130 cm as 1 m 3 cm.)", ("L", 2300))
    add("<b>2 kg − 350 g = ?</b>", "1 kg 650 g", ["1 kg 750 g", "2 kg 350 g", "1 kg 65 g"],
        "2 kg = 2000 g. 2000 − 350 = 1650 g = 1 kg 650 g. "
        "(1 kg 750 g is a regrouping slip: 1000 − 350 is 650, not 750.)", ("M", 1650))
    add("<b>3 L 200 mL − 1 L 500 mL = ?</b>", "1 L 700 mL", ["2 L 300 mL", "1 L 300 mL", "2 L 700 mL"],
        "You cannot take 500 mL from 200 mL, so trade 1 L for 1000 mL: 3 L 200 mL = 2 L 1200 mL. "
        "1200 − 500 = 700 mL and 2 − 1 = 1 L, so 1 L 700 mL. "
        "(2 L 300 mL takes 200 from 500 instead.)", ("C", 1700))
    assert len(its) == 20, len(its)
    return {"title": "Combine units: m and cm, kg and g, L and mL", "items": its}


# ------------------------------------------------------------ set 4: convert, including decimals
def k_between(uf, ut):
    return Fr(UNIT[uf][1], UNIT[ut][1])


def conv_e(n, uf, ut):
    k = k_between(uf, ut)
    r = Fr(n) * k
    if k > 1:
        s = "1 %s = %s %s. %s are bigger than %s, so multiply by %s: %s × %s = %s." % (
            uf, fmt(k), ut, cap(UNIT[uf][2]), UNIT[ut][2], fmt(k), fmt(n), fmt(k), fmt(r))
    else:
        k = 1 / k
        s = "1 %s = %s %s. %s are smaller than %s, so divide by %s: %s ÷ %s = %s." % (
            ut, fmt(k), uf, cap(UNIT[uf][2]), UNIT[ut][2], fmt(k), fmt(n), fmt(k), fmt(r))
    return s + " So %s = %s." % (m(n, uf), m(r, ut))


def conv(n, uf, ut, wrong, rnd, extra=""):
    n = Fr(n)
    fam = UNIT[uf][0]
    r = n * k_between(uf, ut)
    q = "<b>%s = ☐ %s</b>" % (m(n, uf), ut)
    return mcq(q, m(r, ut), [m(Fr(w), ut) for w in wrong], conv_e(n, uf, ut) + extra, rnd,
               want=(fam, n * UNIT[uf][1]))


def set_convert(rnd):
    its = []
    D = Fr
    its.append(mcq("<b>1 m = ☐ cm</b>", "100 cm", ["10 cm", "1000 cm", "1 cm"],
                   "1 m = 100 cm. A metre ruler has 100 centimetres on it. (10 is the number of mm in 1 cm, "
                   "and 1000 is the number of mm in 1 m.)", rnd, want=("L", 1000)))
    its.append(mcq("<b>1 km = ☐ m</b>", "1000 m", ["100 m", "10 m", "10" + NBSP + "000 m"],
                   "Kilo means 1000, so 1 km = 1000 m.", rnd, want=("L", 1000000)))
    its.append(mcq("<b>1 t = ☐ kg</b>", "1000 kg", ["100 kg", "10 kg", "1 kg"],
                   "1 tonne = 1000 kg. A small car is about 1 t.", rnd, want=("M", 1000000)))
    its.append(conv(6, "m", "cm", [60, 6000, D(6, 100)], rnd, extra=" (60 cm uses 1 m = 10 cm.)"))
    its.append(conv(4000, "g", "kg", [40, 400, 4000000], rnd))
    its.append(conv(D("3.5"), "kg", "g", [350, 35, 3005], rnd, extra=" (350 g multiplies by 100, not 1000.)"))
    its.append(conv(750, "mL", "L", [D("7.5"), 75, D("0.075")], rnd,
                    extra=" Check: 0.75 L is three quarters of a litre."))
    its.append(conv(D("2.5"), "m", "cm", [25, 2500, 205], rnd))
    its.append(conv(D("1.2"), "km", "m", [120, 12, 1002], rnd, extra=" (120 m multiplies by 100, not 1000.)"))
    its.append(conv(D("0.5"), "L", "mL", [50, 5000, 5], rnd, extra=" Half a litre is 500 mL."))
    its.append(conv(D("4.5"), "cm", "mm", [450, 405, D("0.45")], rnd))
    its.append(conv(250, "g", "kg", [D("2.5"), 25, D("0.025")], rnd,
                    extra=" Check: 0.25 kg is a quarter of a kilogram."))
    its.append(conv(D("1.75"), "L", "mL", [175, 17500, 1075], rnd))
    its.append(conv(D("2.5"), "t", "kg", [250, 25, 2005], rnd))
    its.append(conv(60, "cm", "m", [6, D("0.06"), 6000], rnd, extra=" (6 m divides by 10, not 100.)"))
    its.append(conv(D("1.4"), "m", "cm", [14, 1400, 104], rnd))
    its.append(conv(D("0.25"), "L", "mL", [25, D("2.5"), 2500], rnd))
    its.append(mcq("Which is the same as <b>1.5 kg</b>?", "1 kg 500 g", ["1 kg 5 g", "1 kg 50 g", "15 kg"],
                   "0.5 kg is half a kilogram, which is 500 g. So 1.5 kg = 1 kg 500 g = 1500 g. "
                   "(1 kg 5 g would be 1.005 kg.)", rnd, want=("M", 1500)))
    its.append(mcq("Which is the same as <b>2.3 m</b>?", "2 m 30 cm", ["2 m 3 cm", "23 cm", "23 m"],
                   "0.3 m = 0.3 × 100 = 30 cm. So 2.3 m = 2 m 30 cm = 230 cm. (2 m 3 cm would be 2.03 m.)",
                   rnd, want=("L", 2300)))
    sts = ["0.4 L < 450 mL < 0.5 L", "0.5 L < 450 mL < 0.4 L", "450 mL < 0.4 L < 0.5 L", "0.4 L < 0.5 L < 450 mL"]
    assert [truth(s) for s in sts] == [True, False, False, False]
    its.append(mcq("Which list goes from the <b>smallest</b> to the <b>largest</b> capacity?", sts[0], sts[1:],
                   "Change them all to millilitres: 0.4 L = 400 mL and 0.5 L = 500 mL. 400 &lt; 450 &lt; 500. "
                   "450 is the biggest number, but 450 mL is less than half a litre.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Convert between units, including decimals", "items": its}


# ------------------------------------------------------------ set 5: word problems
def set_story(rnd):
    P = People(rnd)
    its = []

    def add(q, ans, wr, e, want=None):
        its.append(mcq(q, ans, wr, e, rnd, want=want))

    n, he, his = P.next()
    add("A pancake recipe for 4 people uses 300 mL of milk. %s makes pancakes for 8 people. "
        "How much milk does %s need?" % (n, he), "600 mL", ["304 mL", "2400 mL", "150 mL"],
        "8 people is double 4 people, so double the milk: 2 × 300 = 600 mL. "
        "(2400 mL multiplies by 8. 150 mL halves instead of doubling.)", ("C", 600))
    n, he, his = P.next()
    add("A recipe for Anzac biscuits uses 150 g of flour. %s makes 3 batches. How much flour does %s use?" % (n, he),
        "450 g", ["153 g", "4500 g", "45 g"],
        "3 batches: 3 × 150 = 450 g. (153 g adds 3 instead of multiplying.)", ("M", 450))
    n, he, his = P.next()
    add("A recipe needs 1.5 kg of potatoes. %s has 900 g. How many more grams does %s need?" % (n, he),
        "600 g", ["150 g", "2400 g", "600 kg"],
        "1.5 kg = 1500 g. 1500 − 900 = 600 g more. "
        "(150 g treats 1.5 kg as 1050 g. 2400 g adds instead of finding the difference.)", ("M", 600))
    add("To make a jug of cordial, you mix 250 mL of cordial with 1.75 L of water. How much drink does that make?",
        "2 L", ["251.75 mL", "4.25 L", "1.775 L"],
        "Use one unit: 1.75 L = 1750 mL. 250 + 1750 = 2000 mL = 2 L. "
        "(251.75 mL adds the numbers without converting.)", ("C", 2000))
    n, he, his = P.next()
    add("At the athletics carnival, %s jumps 3 m 45 cm in the long jump. How far is that in centimetres?" % n,
        "345 cm", ["3045 cm", "48 cm", "3450 cm"],
        "3 m = 300 cm. 300 + 45 = 345 cm. (48 cm adds 3 + 45. 3045 cm uses 1 m = 1000 cm.)", ("L", 3450))
    a, b = P.next(), P.next()
    add("In the long jump, %s jumps 3 m 20 cm and %s jumps 2 m 95 cm. How much further does %s jump?"
        % (a[0], b[0], a[0]), "25 cm", ["1 m 75 cm", "35 cm", "75 cm"],
        "Use centimetres: 320 − 295 = 25 cm. "
        "(1 m 75 cm takes 20 from 95 instead of regrouping 1 m as 100 cm.)", ("L", 250))
    jumps = [("Oliver", "2.9 m"), ("Ava", "285 cm"), ("Leo", "3 m 5 cm"), ("Isla", "3.1 m")]
    assert [parse(j)[1] for _, j in jumps] == [2900, 2850, 3050, 3100]
    add("Four students do the long jump at the athletics carnival. Oliver jumps 2.9 m, Ava jumps 285 cm, "
        "Leo jumps 3 m 5 cm and Isla jumps 3.1 m. Who jumps the furthest?",
        "Isla", ["Oliver", "Ava", "Leo"],
        "Change them all to centimetres: 2.9 m = 290 cm, 3 m 5 cm = 305 cm and 3.1 m = 310 cm. "
        "310 cm is the furthest, so Isla wins. 3.1 m is 3 m 10 cm, which is more than 3 m 5 cm.")
    add("In the 4 × 100 m relay, each runner runs 100 m. How far does the whole team run in kilometres?",
        "0.4 km", ["4 km", "400 km", "0.04 km"],
        "4 × 100 = 400 m. 1 km = 1000 m, so 400 ÷ 1000 = 0.4 km. (4 km would be 4000 m.)", ("L", 400000))
    n, he, his = P.next()
    add("The school cross-country course is 2.5 km long. %s has run 1800 m. How far does %s still have to run?"
        % (n, he), "700 m", ["4300 m", "1300 m", "70 m"],
        "2.5 km = 2500 m. 2500 − 1800 = 700 m. (4300 m adds instead. 1300 m takes 5 from 8 instead of regrouping.)",
        ("L", 700000))
    n, he, his = P.next()
    add("%s’s water bottle holds 750 mL. On a hot day %s fills it and drinks it all 4 times. "
        "How many litres does %s drink?" % (n, he, he), "3 L", ["30 L", "0.3 L", "3000 L"],
        "4 × 750 = 3000 mL. 1 L = 1000 mL, so 3000 mL = 3 L. (3000 L forgets to change mL into L.)", ("C", 3000))
    add("A 1.5 L bottle of water is shared equally between 6 cups. How much water goes in each cup?",
        "250 mL", ["25 mL", "0.25 mL", "9000 mL"],
        "1.5 L = 1500 mL. 1500 ÷ 6 = 250 mL. Check: 6 × 250 = 1500. (0.25 is the answer in litres, not mL.)",
        ("C", 250))
    n, he, his = P.next()
    add("%s’s 1 L water bottle is full. %s drinks 350 mL at recess and 400 mL at lunch. How much water is left?"
        % (n, cap(he)), "250 mL", ["750 mL", "350 mL", "1750 mL"],
        "350 + 400 = 750 mL drunk. 1 L = 1000 mL. 1000 − 750 = 250 mL left. (750 mL is what was drunk.)",
        ("C", 250))
    add("The school canteen sells water in 600 mL bottles. How many bottles hold 3 L altogether?",
        "5 bottles", ["2 bottles", "50 bottles", "18 bottles"],
        "3 L = 3000 mL. 3000 ÷ 600 = 5 bottles. Check: 5 × 600 = 3000. (18 multiplies 3 × 6.)")
    n, he, his = P.next()
    add("%s’s school bag has a mass of 4 kg 200 g. %s takes out a 650 g lunchbox. What is the mass of the bag now?"
        % (n, cap(he)), "3 kg 550 g", ["4 kg 450 g", "4 kg 550 g", "3 kg 450 g"],
        "4 kg 200 g = 4200 g. 4200 − 650 = 3550 g = 3 kg 550 g. "
        "(4 kg 450 g takes 200 from 650 instead of regrouping.)", ("M", 3550))
    add("A truck carries 3 t of sand to a building site. It tips out 1200 kg. How much sand is left on the truck?",
        "1800 kg", ["4200 kg", "1800 t", "18 kg"],
        "3 t = 3000 kg. 3000 − 1200 = 1800 kg. (4200 kg adds instead of subtracting. 1800 t has the wrong unit.)",
        ("M", 1800000))
    n, he, his = P.next()
    add("%s buys 3 bags of mandarins. Each bag has a mass of 750 g. What is the total mass?" % n,
        "2 kg 250 g", ["2 kg 25 g", "22 kg 50 g", "2 kg 750 g"],
        "3 × 750 = 2250 g. 2000 g = 2 kg, so 2250 g = 2 kg 250 g. (2 kg 25 g would be 2025 g.)", ("M", 2250))
    n, he, his = P.next()
    add("%s has 2 m of ribbon for a school project. %s cuts it into pieces 25 cm long. How many pieces does %s get?"
        % (n, cap(he), he), "8 pieces", ["80 pieces", "4 pieces", "50 pieces"],
        "2 m = 200 cm. 200 ÷ 25 = 8 pieces. (4 pieces is only 1 m. 50 multiplies 2 × 25.)")
    n, he, his = P.next()
    add("%s walks 650 m to school and 650 m home every day. How far does %s walk in 5 school days, in kilometres?"
        % (n, he), "6.5 km", ["3.25 km", "65 km", "6500 km"],
        "There and back is 2 × 650 = 1300 m a day. 5 × 1300 = 6500 m. 6500 ÷ 1000 = 6.5 km. "
        "(3.25 km forgets the walk home.)", ("L", 6500000))
    n, he, his = P.next()
    add("A recipe needs 1 kg 200 g of flour. Flour is sold in 500 g bags. How many bags does %s need to buy?" % n,
        "3 bags", ["2 bags", "4 bags", "24 bags"],
        "1 kg 200 g = 1200 g. 2 bags = 1000 g, which is not enough. 3 bags = 1500 g, which is enough. "
        "(2 bags leaves 200 g short.)")
    add("Which holds more: one 1.25 L bottle or two 600 mL bottles?", "the 1.25 L bottle, by 50 mL",
        ["the two 600 mL bottles, by 50 mL", "they hold the same", "the 1.25 L bottle, by 650 mL"],
        "1.25 L = 1250 mL. Two 600 mL bottles hold 2 × 600 = 1200 mL. 1250 − 1200 = 50 mL, "
        "so the 1.25 L bottle holds 50 mL more. (650 mL compares it with only one 600 mL bottle.)")
    assert len(its) == 20, len(its)
    return {"title": "Word problems: recipes, sport and water bottles", "items": its}


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
        "<h2>Choose a unit that fits</h2>"
        "<p>Small things use small units. Big things use big units. Think of something you know of about that size.</p>" +
        table(["Measure", "Units (small to big)", "About the size of"], [
            ["Length", "mm, cm, m, km", "1 mm: the thickness of a 5c coin. 1 cm: the width of a fingertip. "
                                        "1 m: a big step. 1 km: about 10 minutes’ walk"],
            ["Mass", "g, kg, t", "1 g: a paper clip. 1 kg: a bag of sugar. 1 t: a small car"],
            ["Capacity", "mL, L", "5 mL: a teaspoon. 375 mL: a can of soft drink. 1 L: a carton of milk"],
        ]) +
        table(["Facts to know"], [
            ["1 cm = 10 mm &nbsp; 1 m = 100 cm &nbsp; 1 km = 1000 m"],
            ["1 kg = 1000 g &nbsp; 1 t = 1000 kg"],
            ["1 L = 1000 mL"],
        ]) +
        "<h2>Smaller units give a more accurate measure</h2>"
        "<p>“About 7 cm” is not exact. Count the small marks too and use millimetres, "
        "or use two units together.</p>"
        "<figure class='sn-fig'>" + ruler_svg(0, 74, "pencil") +
        "<figcaption>The pencil ends 4 small marks past 7 cm. It is 7 cm 4 mm, which is 74 mm.</figcaption></figure>"
        "<p>On a scale or a jug, first work out <b>what one mark is worth</b>: the jump between two numbers ÷ the "
        "number of spaces.</p>"
        "<figure class='sn-fig'>" + dial_svg(2750, 4000, 1000, 250, 1000) +
        "<figcaption>Each kilogram has 4 spaces, so each mark is 1000 ÷ 4 = 250 g. "
        "The needle is 3 marks past 2 kg: 2 kg 750 g.</figcaption></figure>"
        "<figure class='sn-fig'>" + jug_svg(1250, 2000, 500, 250) +
        "<figcaption>The numbers go up by 500 mL with 2 spaces, so each line is 250 mL. "
        "The water is at 1250 mL, which is 1 L 250 mL.</figcaption></figure>"
        "<h2>Combine units</h2>"
        "<p>Change the big unit into the small unit, then add the rest.</p>" +
        ex("Metres and centimetres", "1 m 35 cm = ☐ cm", "1 m = 100 cm. 100 + 35 = 135.", "135 cm") +
        ex("Kilograms and grams", "2 kg 40 g = ☐ g", "2 kg = 2000 g. 2000 + 40 = 2040.", "2040 g (not 240 g)") +
        ex("Litres and millilitres", "1650 mL = ☐ L ☐ mL", "1000 mL = 1 L. 1650 − 1000 = 650.", "1 L 650 mL") +
        "<h2>Convert between units</h2>"
        "<p>Big unit to small unit: <b>multiply</b> (you need more of the small units). "
        "Small unit to big unit: <b>divide</b>.</p>" +
        ex("Kilograms to grams", "3.5 kg = ☐ g", "1 kg = 1000 g. 3.5 × 1000 = 3500.", "3500 g") +
        ex("Millilitres to litres", "750 mL = ☐ L", "1 L = 1000 mL. 750 ÷ 1000 = 0.75.", "0.75 L") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["1 m = 10 cm or 1 m = 1000 cm", "1 m = 100 cm. It is 1 cm = 10 mm and 1 km = 1000 m"],
            ["2 kg 40 g = 240 g", "2 kg = 2000 g, so 2 kg 40 g = 2040 g"],
            ["Counting every mark on a scale as 1, 10 or 100", "Work out what one mark is worth first"],
            ["Forgetting that an object does not start at 0", "Take the start away from the end"],
            ["Comparing numbers without units (450 mL &gt; 0.5 L)", "Change to the same unit: 0.5 L = 500 mL"],
            ["Choosing a unit from the wrong measure (kg for a bottle of water’s capacity)",
             "Length: mm, cm, m, km. Mass: g, kg, t. Capacity: mL, L"],
        ])
    )


FAQ = [
    {"q": "What metric units do Year 5 students use in the Australian Curriculum?",
     "a": "Year 5 students choose and use millimetres, centimetres, metres and kilometres for length, grams, "
          "kilograms and tonnes for mass, and millilitres and litres for capacity."},
    {"q": "Why do Year 5 students use smaller units or a combination of units?",
     "a": "Smaller units give a more accurate measure. A pencil that is “about 16 cm” can be measured more "
          "accurately as 164 mm or 16 cm 4 mm."},
    {"q": "How do you change 2 kg 40 g into grams?",
     "a": "Change the kilograms into grams first: 2 kg = 2000 g. Then add the grams: 2000 + 40 = 2040 g, not 240 g."},
    {"q": "Is measurement part of the Year 5 NAPLAN numeracy test?",
     "a": "Yes. NAPLAN numeracy includes measurement, so Year 5 students may be asked to choose units, read scales "
          "and convert between units such as metres and centimetres."},
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
    rnd = random.Random(5810)
    sets = [set_units(rnd), set_read(rnd), set_combine(rnd), set_convert(rnd), set_story(rnd)]
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
        "country": "au", "subject": "maths", "grade": "year-5", "slug": "metric-units", "sort": 10,
        "updated": UPDATED, "pdf_url": "",
        "title": "Year 5 Metric Units: Length, Mass and Capacity",
        "seo_title": "Year 5 Metric Units Worksheets: Length, Mass and Capacity (Free Maths with Answer Key)",
        "short_title": "Metric Units",
        "domain": "Measurement",
        "standard_code": "AC9M5M01",
        "standard_url": "https://v9.australiancurriculum.edu.au/f-10-curriculum/learning-areas/mathematics",
        "standard_text": "Choose appropriate metric units when measuring the length, mass and capacity of objects; "
                         "use smaller units or a combination of units to obtain a more accurate measure",
        "meta_desc": "Free Year 5 maths worksheets on metric units, aligned to the Australian Curriculum (AC9M5M01): "
                     "choose mm, cm, m, km, g, kg, t, mL or L, read rulers, scales and jugs accurately, combine "
                     "units like 1 m 35 cm, convert units and solve word problems. 100 questions with an answer key, "
                     "great for NAPLAN practice.",
        "key_big": "Choose a unit that fits the size, and use smaller units for a more accurate measure.",
        "key_sub": "1 m = 100 cm, 1 kg = 1000 g and 1 L = 1000 mL. So 1 m 35 cm = 135 cm and 2 kg 40 g = 2040 g, "
                   "not 240 g.",
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
