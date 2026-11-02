# -*- coding: utf-8 -*-
"""
UK Year 3 Maths: Measuring Length, Mass and Capacity (National Curriculum in England, Year 3: Measurement)
  python tools/gen_uk_maths_y3_measuring.py
HTML attributes use single quotes (no backslashes in the JSON).
British English, metric units only. No decimals: mixed units such as 1 m 20 cm, 1 kg 300 g, 1 l 500 ml.
Every measurement answer is parsed back to a base unit (mm, g, ml) and checked in code.
Wrong answers come from real mistakes: reading the end of an object that does not start at 0, counting
the numbers on a ruler instead of the spaces, starting at 1, counting every mark on a scale as 1 or 10,
reading the next number, mixing up units (g/kg, ml/l, cm/mm), 1 m 5 cm = 15 cm or 150 cm, and adding or
subtracting mixed units without exchanging.
"""
import json, math, os, random, re
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "uk", "maths", "year-3")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
RED = "#c0392b"
INK = "#2b2b2b"
WATER = "#9fd3f2"
WATER_LINE = "#2a7fb8"
WOOD = "#f6e7b8"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Amelia", "Isla", "Freya", "Poppy", "Ava", "Aisha", "Lily", "Zara", "Grace", "Ruby", "Maya", "Evie"]
BOYS = ["Oliver", "Harry", "Mohammed", "Jack", "Arjun", "Noah", "George", "Leo", "Alfie", "Kai", "Ethan", "Charlie"]


# ------------------------------------------------------------ units and checking
UNIT = {"mm": ("L", 1), "cm": ("L", 10), "m": ("L", 1000),
        "g": ("M", 1), "kg": ("M", 1000), "ml": ("C", 1), "l": ("C", 1000)}
TOK = re.compile(r"([\d,]+)\s*(" + "|".join(sorted(UNIT, key=len, reverse=True)) + r")(?![a-z])")


def parse(s):
    """'1 kg 300 g' -> ('M', 1300). None if the string is not a plain measurement."""
    s = s.strip()
    pos, fam, tot = 0, None, 0
    for mt in TOK.finditer(s):
        if s[pos:mt.start()].strip():
            return None
        fu, sz = UNIT[mt.group(2)]
        if fam and fu != fam:
            return None
        fam = fu
        tot += int(mt.group(1).replace(",", "")) * sz
        pos = mt.end()
    if fam is None or s[pos:].strip():
        return None
    return fam, tot


def truth(st):
    """'1 m 5 cm < 150 cm' -> True/False (chains allowed)."""
    parts = re.split(r" (<|>|=) ", st)
    vals = [parse(p) for p in parts[0::2]]
    assert all(vals) and len({v[0] for v in vals}) == 1, st
    ok = True
    for i, op in enumerate(parts[1::2]):
        a, b = vals[i][1], vals[i + 1][1]
        ok = ok and {"<": a < b, ">": a > b, "=": a == b}[op]
    return ok


def c(n):
    return "{:,}".format(n)


def gs(v):
    """grams -> '650 g', '2 kg', '1 kg 300 g'."""
    if v < 1000:
        return "%d g" % v
    return "%d kg" % (v // 1000) + ("" if v % 1000 == 0 else " %d g" % (v % 1000))


def mls(v):
    """millilitres -> '650 ml', '2 l', '1 l 300 ml'."""
    if v < 1000:
        return "%d ml" % v
    return "%d l" % (v // 1000) + ("" if v % 1000 == 0 else " %d ml" % (v % 1000))


def cms(v):
    """centimetres -> '85 cm', '2 m', '1 m 25 cm'."""
    if v < 100:
        return "%d cm" % v
    return "%d m" % (v // 100) + ("" if v % 100 == 0 else " %d cm" % (v % 100))


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e, rnd, want=None):
    """4 choices: correct + 3 unique distractors. Measurement choices must all differ in value.
    want = (family, value in base unit) checks the correct answer."""
    correct = str(correct)
    if want is not None:
        assert parse(correct) == want, (q, correct, want, parse(correct))
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
    elif kind == "rubber":
        o.append("<rect x='%.1f' y='12' width='%.1f' height='20' rx='4' fill='#f7b7c5' stroke='%s' stroke-width='1.5'/>"
                 % (a, b - a, INK))
        o.append("<rect x='%.1f' y='12' width='%.1f' height='20' fill='#5dade2' stroke='%s' stroke-width='1.5'/>"
                 % (a + (b - a) * 0.45, (b - a) * 0.4, INK))
    else:  # ribbon
        o.append("<rect x='%.1f' y='15' width='%.1f' height='14' fill='%s' stroke='%s' stroke-width='1.5'/>"
                 % (a, b - a, RED, INK))
    return "".join(o)


NAMES = {"pencil": "pencil", "crayon": "crayon", "rubber": "rubber", "ribbon": "piece of ribbon"}


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
    return svg_wrap(W, H, "".join(o), "ruler with a %s from %d mm to %d mm" % (NAMES[kind], s_mm, e_mm))


def dial_svg(v, mx, lab, tick, div=1, size=200):
    """Round scale, values in grams. Labels every `lab` g shown as val/div. Needle exactly at v."""
    unit = "g" if div == 1 else "kg"
    cx = size / 2.0
    R = cx - 6
    def pt(val, r):
        ang = math.radians(-135 + 270.0 * val / mx)
        return cx + r * math.sin(ang), cx - r * math.cos(ang)
    s = ["<circle cx='%.1f' cy='%.1f' r='%.1f' fill='#fff' stroke='%s' stroke-width='6'/>" % (cx, cx, R, GREEN)]
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
             % (cx, cx, nx, ny, RED))
    s.append("<g font-size='%d' font-weight='700' fill='%s' text-anchor='middle' stroke='#fff' stroke-width='4' "
             "paint-order='stroke'>" % (15 if mx // div >= 1000 else 17, INK))
    for val in range(0, mx + 1, lab):
        x, y = pt(val, R - 36)
        s.append("<text x='%.1f' y='%.1f'>%s</text>" % (x, y + 6, c(val // div)))
    s.append("</g>")
    s.append("<circle cx='%.1f' cy='%.1f' r='7' fill='%s'/>" % (cx, cx, RED))
    s.append("<text x='%.1f' y='%.1f' font-size='22' font-weight='800' fill='%s' text-anchor='middle'>%s</text>"
             % (cx, cx + 62, GREEN, unit))
    return svg_wrap(size, size, "".join(s), "weighing scale with the needle at %s" % gs(v))


def jug_svg(v, mx, lab, step, div=1, size=200):
    """Measuring jug, values in ml: a line every `step` ml, a label every `lab` ml (shown as val/div).
    Water exactly at v."""
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
            s.append("<text x='%d' y='%.1f'>%s</text>" % (x0 - 7, Y(val) + 5, c(val // div)))
    s.append("</g>")
    s.append(text(x0 - 7, 198, "ml" if div == 1 else "litres", 15, anchor="end", col=GREEN))
    return svg_wrap(size, size + 6, "".join(s), "measuring jug with water at %s" % mls(v))


# ------------------------------------------------------------ set 1: length with a ruler
def set_length(rnd):
    its = []
    its.append(mcq("How many millimetres are in 1 centimetre?", "10 mm", ["100 mm", "1 mm", "5 mm"],
                   "Look at a ruler. There are 10 small spaces in each centimetre. So 1 cm = 10 mm.", rnd,
                   want=("L", 10)))
    its.append(mcq("How many centimetres are in 1 metre?", "100 cm", ["10 cm", "1,000 cm", "50 cm"],
                   "A metre stick has 100 centimetres marked on it. So 1 m = 100 cm.", rnd, want=("L", 1000)))
    units = ["millimetres (mm)", "centimetres (cm)", "metres (m)", "kilograms (kg)"]
    for obj, ans, e in [
        ("an ant", "millimetres (mm)", "An ant is tiny, shorter than 1 cm. Use millimetres for very short things."),
        ("a pencil", "centimetres (cm)", "A pencil fits on a ruler. Use centimetres. Metres are for long things like a room."),
        ("the playground", "metres (m)", "The playground is long. Use metres. Kilograms measure mass, not length."),
    ]:
        its.append(mcq("Which unit is best to measure the length of %s?" % obj, ans,
                       [u for u in units if u != ans], e, rnd))
    # whole cm, starting at 0
    for e_cm, kind in [(7, "pencil"), (5, "crayon"), (4, "rubber"), (8, "ribbon")]:
        nm = NAMES[kind]
        q = fig(ruler_svg(0, e_cm * 10, kind)) + "How long is the %s?" % nm
        e = ("The %s starts at 0 and ends at %d. So it is %d cm long. Count the big spaces, not the numbers."
             % (nm, e_cm, e_cm))
        its.append(mcq(q, "%d cm" % e_cm, ["%d cm" % (e_cm + 1), "%d cm" % (e_cm - 1), "%d mm" % e_cm], e, rnd,
                       want=("L", e_cm * 10)))
    # whole cm, not starting at 0
    for s_cm, e_cm, kind in [(2, 9, "pencil"), (1, 6, "crayon"), (3, 7, "rubber"), (2, 8, "ribbon")]:
        nm = NAMES[kind]
        ln = e_cm - s_cm
        q = fig(ruler_svg(s_cm * 10, e_cm * 10, kind)) + "How long is the %s?" % nm
        e = ("The %s starts at %d, not at 0. It ends at %d. %d − %d = %d, so it is %d cm long. "
             "You can also count the big spaces: there are %d." % (nm, s_cm, e_cm, e_cm, s_cm, ln, ln, ln))
        its.append(mcq(q, "%d cm" % ln, ["%d cm" % e_cm, "%d cm" % (ln + 1), "%d cm" % (e_cm + s_cm), "%d cm" % (ln - 1)], e, rnd,
                       want=("L", ln * 10)))
    # cm and mm, starting at 0
    for e_mm, kind in [(46, "crayon"), (63, "pencil"), (38, "rubber")]:
        nm = NAMES[kind]
        a, b = divmod(e_mm, 10)
        q = fig(ruler_svg(0, e_mm, kind)) + "How long is the %s?" % nm
        e = ("The %s goes past %d cm and then %s more. Each small mark is 1 mm. So it is %d cm %d mm long."
             % (nm, a, marks(b, "small mark"), a, b))
        its.append(mcq(q, "%d cm %d mm" % (a, b),
                       ["%d cm %d mm" % (b, a), "%d cm %d mm" % (a + 1, b), "%d cm" % e_mm, "%d cm" % a], e, rnd,
                       want=("L", e_mm)))
    its.append(mcq(fig(ruler_svg(0, 35, "rubber")) + "How long is the rubber in millimetres?", "35 mm",
                   ["5 mm", "305 mm", "35 cm"],
                   "The rubber is 3 cm and 5 mm long. 3 cm = 30 mm, and 30 + 5 = 35. So it is 35 mm long.", rnd,
                   want=("L", 35)))
    # cm and mm, not starting at 0
    for s_mm, e_mm, kind in [(20, 74, "pencil"), (30, 78, "crayon")]:
        nm = NAMES[kind]
        ln = e_mm - s_mm
        a, b = divmod(ln, 10)
        q = fig(ruler_svg(s_mm, e_mm, kind)) + "How long is the %s?" % nm
        e = ("The %s starts at %d cm, not at 0. It ends at %d cm %d mm. Take away %d cm: %d cm %d mm − %d cm = %d cm %d mm."
             % (nm, s_mm // 10, e_mm // 10, e_mm % 10, s_mm // 10, e_mm // 10, e_mm % 10, s_mm // 10, a, b))
        its.append(mcq(q, "%d cm %d mm" % (a, b),
                       ["%d cm %d mm" % (e_mm // 10, e_mm % 10), "%d cm %d mm" % (a + 1, b), "%d cm" % ln], e, rnd,
                       want=("L", ln)))
    its.append(mcq("A worm is 6 cm 4 mm long. How long is it in millimetres?", "64 mm", ["10 mm", "604 mm", "640 mm"],
                   "1 cm = 10 mm, so 6 cm = 60 mm. 60 + 4 = 64. The worm is 64 mm long.", rnd, want=("L", 64)))
    assert len(its) == 20, len(its)
    return {"title": "Measure length with a ruler: cm and mm", "items": its}


# ------------------------------------------------------------ set 2: mass on scales
def dial_e(v, lab, tick, div):
    sp = lab // tick
    base = v - v % lab
    k = (v - base) // tick
    if div == 1:
        s = ("The numbers go up by %d g. There are %d spaces between numbers, so each mark is %d ÷ %d = %d g. "
             % (lab, sp, lab, sp, tick))
    elif lab == 1000:
        s = ("Each kilogram is split into %d equal spaces. 1 kg = 1,000 g, so each mark is 1,000 ÷ %d = %d g. "
             % (sp, sp, tick))
    else:
        s = "The numbers go up by %d kg. There are %d spaces between numbers, so each mark is %d kg. " % (
            lab // 1000, sp, tick // 1000)
    if base == 0:
        return s + "The needle is %s past 0: %s." % (marks(k), gs(v))
    if div == 1:
        return s + "The needle is %s past %d: %d + %d = %d g." % (marks(k), base, base, k * tick, v)
    return s + "The needle is %s past %s: %s + %s = %s." % (marks(k), gs(base), gs(base), gs(k * tick), gs(v))


DIALS = [  # (value g, max, label step, tick, div, object, wrong answers)
    (350, 500, 100, 50, 1, "a bag of carrots", ["310 g", "400 g", "300 g", "350 kg"]),
    (150, 500, 100, 50, 1, "an apple", ["110 g", "200 g", "100 g", "150 kg"]),
    (450, 500, 100, 50, 1, "a jar of honey", ["410 g", "500 g", "400 g"]),
    (300, 1000, 200, 100, 1, "a block of cheese", ["210 g", "250 g", "400 g", "300 kg"]),
    (700, 1000, 200, 100, 1, "a bunch of bananas", ["610 g", "650 g", "800 g"]),
    (900, 1000, 200, 100, 1, "a bag of apples", ["810 g", "850 g", "1 kg"]),
    (800, 1000, 500, 100, 1, "a loaf of bread", ["503 g", "530 g", "700 g", "900 g"]),
    (400, 1000, 500, 100, 1, "a box of cereal", ["40 g", "200 g", "500 g"]),
    (2500, 5000, 1000, 500, 1000, "a bag of potatoes", ["2 kg 5 g", "25 kg", "3 kg 500 g"]),
    (1500, 5000, 1000, 500, 1000, "a pumpkin", ["1 kg 5 g", "15 kg", "2 kg 500 g"]),
    (1300, 3000, 1000, 100, 1000, "a melon", ["1 kg 3 g", "13 kg", "1 kg 30 g", "1 kg 400 g"]),
    (2700, 3000, 1000, 100, 1000, "a parcel", ["2 kg 7 g", "27 kg", "2 kg 70 g", "2 kg 600 g"]),
    (7000, 10000, 2000, 1000, 1000, "a bag of dog food", ["6 kg", "8 kg", "7 g", "6 kg 500 g"]),
    (3000, 10000, 2000, 1000, 1000, "a pile of books", ["2 kg", "4 kg", "3 g", "2 kg 500 g"]),
]


def set_mass(rnd):
    its = []
    its.append(mcq("How many grams are in 1 kilogram?", "1,000 g", ["100 g", "10 g", "1 g"],
                   "Kilo means 1,000. So 1 kg = 1,000 g.", rnd, want=("M", 1000)))
    for obj, ans, wr, e in [
        ("a bag of sugar", "1 kg", ["1 g", "100 kg", "10 g"],
         "A bag of sugar is about 1 kilogram. 1 g is about the mass of a paper clip."),
        ("an apple", "100 g", ["100 kg", "1 g", "10 kg"],
         "An apple is light, about 100 grams. 100 kg is heavier than a grown-up."),
        ("a Year 3 child", "25 kg", ["25 g", "250 kg", "2 kg"],
         "A Year 3 child is about 25 kilograms. 25 g is lighter than a bar of chocolate."),
    ]:
        its.append(mcq("What is the best estimate for the mass of %s?" % obj, ans, wr, e, rnd))
    for v, mx, lab, tick, div, obj, wrong in DIALS:
        q = fig(dial_svg(v, mx, lab, tick, div)) + "The scale shows the mass of %s. What is the mass?" % obj
        its.append(mcq(q, gs(v), wrong, dial_e(v, lab, tick, div), rnd, want=("M", v)))
    its.append(mcq(fig(dial_svg(600, 1000, 200, 100)) +
                   "The scale shows a bag of flour. How much more flour is needed to make 1 kg?",
                   "400 g", ["1 kg 600 g", "500 g", "600 g"],
                   "The needle is at 600 g. 1 kg = 1,000 g. 1,000 − 600 = 400 g more.", rnd, want=("M", 400)))
    its.append(mcq(fig(dial_svg(250, 500, 100, 50)) +
                   "The scale shows a bowl of cherries. The empty bowl weighs 100 g. What is the mass of the cherries?",
                   "150 g", ["350 g", "250 g", "110 g"],
                   "Each mark is 50 g, so the needle is at 250 g. Take away the bowl: 250 − 100 = 150 g.",
                   rnd, want=("M", 150)))
    assert len(its) == 20, len(its)
    return {"title": "Read scales: mass in g and kg", "items": its}


# ------------------------------------------------------------ set 3: capacity in jugs
def jug_e(v, lab, step, div):
    sp = lab // step
    base = v - v % lab
    k = (v - base) // step
    if div == 1:
        s = ("The numbers go up by %d ml. There are %d spaces between numbers, so each line is %d ÷ %d = %d ml. "
             % (lab, sp, lab, sp, step))
    else:
        s = ("Each litre is split into %d equal spaces. 1 l = 1,000 ml, so each line is 1,000 ÷ %d = %d ml. "
             % (sp, sp, step))
    if base == 0:
        return s + "The water is %s up from the bottom: %s." % (marks(k, "line"), mls(v))
    if v < 1000:
        return s + "The water is %s above %d: %d + %d = %d ml." % (marks(k, "line"), base, base, k * step, v)
    return s + "The water is %s above %s: %s + %d ml = %s." % (marks(k, "line"), mls(base), mls(base), k * step, mls(v))


JUGS = [  # (value ml, max, label step, line step, div, wrong answers)
    (250, 500, 100, 50, 1, ["210 ml", "300 ml", "200 ml", "250 l"]),
    (350, 500, 100, 50, 1, ["310 ml", "400 ml", "300 ml"]),
    (450, 500, 100, 50, 1, ["410 ml", "500 ml", "400 ml"]),
    (300, 1000, 200, 100, 1, ["210 ml", "250 ml", "400 ml", "300 l"]),
    (700, 1000, 200, 100, 1, ["610 ml", "650 ml", "800 ml"]),
    (900, 1000, 200, 100, 1, ["810 ml", "850 ml", "1 l"]),
    (400, 1000, 250, 50, 1, ["280 ml", "253 ml", "450 ml", "550 ml"]),
    (650, 1000, 250, 50, 1, ["530 ml", "503 ml", "600 ml", "800 ml"]),
    (550, 1000, 250, 50, 1, ["510 ml", "501 ml", "600 ml", "750 ml"]),
    (850, 1000, 250, 50, 1, ["770 ml", "752 ml", "900 ml"]),
    (1300, 2000, 500, 100, 1, ["1 l 30 ml", "13 l", "1 l 150 ml", "1 l 400 ml"]),
    (1700, 2000, 500, 100, 1, ["1 l 520 ml", "17 l", "1 l 600 ml", "1 l 800 ml"]),
    (3500, 5000, 1000, 500, 1000, ["3 l 5 ml", "35 l", "4 l 500 ml", "3 l 50 ml"]),
    (1500, 5000, 1000, 500, 1000, ["1 l 5 ml", "15 l", "2 l 500 ml", "1 l 50 ml"]),
]


def set_capacity(rnd):
    its = []
    its.append(mcq("How many millilitres are in 1 litre?", "1,000 ml", ["100 ml", "10 ml", "1 ml"],
                   "Milli means one thousandth. So 1 l = 1,000 ml.", rnd, want=("C", 1000)))
    for obj, ans, wr, e in [
        ("a teaspoon", "5 ml", ["5 l", "500 ml", "50 l"],
         "A teaspoon holds only a little, about 5 millilitres. 5 l would fill a big bucket halfway."),
        ("a mug", "300 ml", ["300 l", "3 ml", "30 l"],
         "A mug of tea is about 300 millilitres. 300 l would fill a bath."),
        ("a bucket", "10 l", ["10 ml", "100 l", "1 ml"],
         "A bucket holds about 10 litres. 10 ml is only two teaspoons."),
    ]:
        its.append(mcq("What is the best estimate for how much %s holds?" % obj, ans, wr, e, rnd))
    for v, mx, lab, step, div, wrong in JUGS:
        q = fig(jug_svg(v, mx, lab, step, div)) + "How much water is in the jug?"
        its.append(mcq(q, mls(v), wrong, jug_e(v, lab, step, div), rnd, want=("C", v)))
    its.append(mcq(fig(jug_svg(150, 500, 100, 50)) + "How much more water is needed to fill the jug to 500 ml?",
                   "350 ml", ["650 ml", "150 ml", "450 ml"],
                   "Each line is 50 ml, so the water is at 150 ml. 500 − 150 = 350 ml more.", rnd, want=("C", 350)))
    its.append(mcq(fig(jug_svg(800, 1000, 200, 100)) + "Jack pours 250 ml of water out of the jug. How much is left?",
                   "550 ml", ["650 ml", "1 l 50 ml", "250 ml"],
                   "The water is at 800 ml. Water is poured out, so subtract: 800 − 250 = 550 ml.", rnd,
                   want=("C", 550)))
    assert len(its) == 20, len(its)
    return {"title": "Read jugs: capacity in ml and l", "items": its}


# ------------------------------------------------------------ set 4: compare and order
def set_compare(rnd):
    its = []
    for q, ans, wr, e, want in [
        ("1 m 5 cm = ☐ cm", "105 cm", ["15 cm", "150 cm", "1,005 cm"],
         "1 m = 100 cm. Add the 5 cm: 100 + 5 = 105 cm. It is not 15 cm, and it is not 150 cm.", 1050),
        ("1 m 50 cm = ☐ cm", "150 cm", ["15 cm", "105 cm", "1,050 cm"],
         "1 m = 100 cm. Add the 50 cm: 100 + 50 = 150 cm.", 1500),
        ("2 m 30 cm = ☐ cm", "230 cm", ["23 cm", "203 cm", "2,030 cm"],
         "2 m = 200 cm. Add the 30 cm: 200 + 30 = 230 cm.", 2300),
        ("4 cm 5 mm = ☐ mm", "45 mm", ["9 mm", "405 mm", "450 mm"],
         "1 cm = 10 mm, so 4 cm = 40 mm. Add the 5 mm: 40 + 5 = 45 mm.", 45),
    ]:
        its.append(mcq("Find the missing number. <b>%s</b>" % q, ans, wr, e, rnd, want=("L", want)))
    its.append(mcq("Find the missing number. <b>1 kg 200 g = ☐ g</b>", "1,200 g", ["120 g", "1,020 g", "300 g"],
                   "1 kg = 1,000 g. Add the 200 g: 1,000 + 200 = 1,200 g. 300 g would mean 1 kg = 100 g.", rnd, want=("M", 1200)))
    its.append(mcq("Find the missing number. <b>1 kg 50 g = ☐ g</b>", "1,050 g", ["150 g", "1,500 g", "1,005 g"],
                   "1 kg = 1,000 g. Add the 50 g: 1,000 + 50 = 1,050 g. The 5 is in the tens place.", rnd,
                   want=("M", 1050)))
    its.append(mcq("Find the missing number. <b>1 l 500 ml = ☐ ml</b>", "1,500 ml", ["150 ml", "1,050 ml", "600 ml"],
                   "1 l = 1,000 ml. Add the 500 ml: 1,000 + 500 = 1,500 ml. 600 ml would mean 1 l = 100 ml.",
                   rnd, want=("C", 1500)))
    its.append(mcq("Which is the same as <b>320 cm</b>?", "3 m 20 cm", ["32 m", "3 m 2 cm", "320 m"],
                   "100 cm = 1 m, so 300 cm = 3 m. 320 cm = 3 m and 20 cm left over.", rnd, want=("L", 3200)))
    base = {"cm": "centimetres", "g": "grams", "ml": "millilitres"}
    for q, ch, fn, u in [
        ("Which is the longest?", ["150 cm", "1 m 5 cm", "1 m 40 cm", "99 cm"], max, "cm"),
        ("Which is the shortest?", ["2 m", "190 cm", "2 m 5 cm", "1 m 95 cm"], min, "cm"),
        ("Which is the heaviest?", ["1 kg", "900 g", "1 kg 50 g", "950 g"], max, "g"),
        ("Which is the lightest?", ["600 g", "1 kg", "1 kg 20 g", "800 g"], min, "g"),
        ("Which holds the most?", ["1 l", "800 ml", "1 l 200 ml", "1,100 ml"], max, "ml"),
        ("Which holds the least?", ["2 l", "1 l 900 ml", "1,950 ml", "2 l 50 ml"], min, "ml"),
    ]:
        vals = [parse(x)[1] // UNIT[u][1] for x in ch]
        assert len(set(vals)) == 4
        i = vals.index(fn(vals))
        conv = ["%s = %s %s" % (ch[j], c(vals[j]), u) for j in range(4) if ch[j] != "%s %s" % (c(vals[j]), u)]
        e = "Change them all to %s: %s. So the answer is %s." % (base[u], ", ".join(conv), ch[i])
        its.append(mcq(q, ch[i], [x for j, x in enumerate(ch) if j != i], e, rnd))
    for sts, e in [
        (["1 m 5 cm < 150 cm", "1 m 5 cm = 15 cm", "1 m 5 cm = 150 cm", "1 m 5 cm > 150 cm"],
         "1 m 5 cm = 100 cm + 5 cm = 105 cm. 105 cm is less than 150 cm."),
        (["1 kg > 900 g", "1 kg = 100 g", "800 g > 1 kg", "1 kg < 950 g"],
         "1 kg = 1,000 g. 1,000 g is more than 900 g. Do not compare only the numbers 1 and 900."),
        (["3 l > 2 l 900 ml", "3 l = 300 ml", "2 l 900 ml > 3 l", "3 l < 2,500 ml"],
         "3 l = 3,000 ml and 2 l 900 ml = 2,900 ml. 3,000 is more than 2,900."),
        (["40 mm = 4 cm", "40 mm = 40 cm", "4 cm < 30 mm", "40 mm = 400 cm"],
         "1 cm = 10 mm, so 4 cm = 40 mm. 4 cm is more than 30 mm."),
    ]:
        assert [truth(s) for s in sts] == [True, False, False, False], sts
        its.append(mcq("Which is true?", sts[0], sts[1:], e, rnd))
    for q, sts, e in [
        ("Which list goes from the shortest to the longest?",
         ["95 cm < 1 m 5 cm < 150 cm", "1 m 5 cm < 95 cm < 150 cm", "150 cm < 1 m 5 cm < 95 cm",
          "95 cm < 150 cm < 1 m 5 cm"],
         "Change them to centimetres: 1 m 5 cm = 105 cm. 95 < 105 < 150."),
        ("Which list goes from the lightest to the heaviest?",
         ["800 g < 1 kg < 1 kg 200 g", "1 kg < 800 g < 1 kg 200 g", "1 kg 200 g < 1 kg < 800 g",
          "800 g < 1 kg 200 g < 1 kg"],
         "Change them to grams: 1 kg = 1,000 g and 1 kg 200 g = 1,200 g. 800 < 1,000 < 1,200."),
    ]:
        assert [truth(s) for s in sts] == [True, False, False, False], sts
        its.append(mcq(q, sts[0], sts[1:], e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Compare and order measures", "items": its}


# ------------------------------------------------------------ set 5: word problems
def set_story(rnd):
    P = People(rnd)
    its = []

    def add(q, r, w, e, want=None):
        its.append(mcq(q, r, w, e, rnd, want=want))

    n, he, his = P.next()
    add("%s has 85 cm of ribbon. %s cuts off 30 cm. How much ribbon is left?" % (n, cap(he)),
        "55 cm", ["115 cm", "65 cm", "50 cm"], "Cutting off means subtract: 85 − 30 = 55 cm.", ("L", 550))
    n, he, his = P.next()
    add("%s has two pieces of ribbon. One is 45 cm long. The other is 38 cm long. "
        "How much ribbon is there altogether?" % n,
        "83 cm", ["73 cm", "7 cm", "713 cm"],
        "Add: 45 + 38. 5 + 8 = 13, so exchange 10 ones for 1 ten. 45 + 38 = 83 cm.", ("L", 830))
    add("A sunflower was 35 cm tall. It grew 18 cm more. How tall is it now?",
        "53 cm", ["43 cm", "17 cm", "513 cm"],
        "Add: 35 + 18 = 53 cm. Remember to exchange: 5 + 8 = 13.", ("L", 530))
    n, he, his = P.next()
    add("%s builds a train track 3 m long. %s adds 1 m 50 cm more track. How long is the track now?" % (n, cap(he)),
        "4 m 50 cm", ["4 m 5 cm", "1 m 50 cm", "3 m 50 cm"],
        "Add the metres: 3 m + 1 m = 4 m. Then add the 50 cm. The track is 4 m 50 cm long.", ("L", 4500))
    n, he, his = P.next()
    n2, he2, his2 = P.next()
    add("%s is 1 m 25 cm tall. %s is 1 m 10 cm tall. How much taller is %s?" % (n, n2, n),
        "15 cm", ["35 cm", "2 m 35 cm", "1 m 15 cm"],
        "Both are 1 m and some more. Compare the centimetres: 25 − 10 = 15 cm.", ("L", 150))
    n, he, his = P.next()
    add("%s has 1 m 40 cm of string. %s ties on 80 cm more. How long is the string now?" % (n, cap(he)),
        "2 m 20 cm", ["60 cm", "1 m 20 cm", "2 m 40 cm"],
        "40 cm + 80 cm = 120 cm = 1 m 20 cm. Add this to 1 m: 1 m + 1 m 20 cm = 2 m 20 cm.", ("L", 2200))
    n, he, his = P.next()
    add("%s needs 250 g of flour for a cake and 175 g of flour for biscuits. How much flour does %s need altogether?"
        % (n, he), "425 g", ["325 g", "75 g", "415 g"],
        "Add: 250 + 175. 5 tens + 7 tens = 12 tens, so exchange 10 tens for 1 hundred. 250 + 175 = 425 g.",
        ("M", 425))
    n, he, his = P.next()
    add("%s has a 1 kg bag of flour. %s uses 350 g to bake bread. How much flour is left?" % (n, cap(he)),
        "650 g", ["750 g", "1 kg 350 g", "350 g"],
        "1 kg = 1,000 g. Subtract: 1,000 − 350 = 650 g.", ("M", 650))
    add("A bag of apples weighs 600 g. A bag of oranges weighs 450 g. How much do they weigh altogether?",
        "1 kg 50 g", ["1 kg 5 g", "150 g", "1 kg 500 g"],
        "600 + 450 = 1,050 g. 1,000 g = 1 kg, so 1,050 g = 1 kg 50 g.", ("M", 1050))
    add("A parcel can weigh up to 2 kg. Mum's parcel weighs 1 kg 300 g. How much more can she put in it?",
        "700 g", ["800 g", "1 kg 700 g", "3 kg 300 g"],
        "1 kg 300 g = 1,300 g and 2 kg = 2,000 g. 2,000 − 1,300 = 700 g more.", ("M", 700))
    n, he, his = P.next()
    add("%s's school bag weighs 2 kg. %s puts in a lunchbox that weighs 500 g. How much does the bag weigh now?"
        % (n, cap(he)), "2 kg 500 g", ["2 kg 5 g", "502 g", "7 kg"],
        "Add the grams to the kilograms: 2 kg + 500 g = 2 kg 500 g.", ("M", 2500))
    n, he, his = P.next()
    add("%s has a 500 ml bottle of water. %s drinks 175 ml. How much water is left?" % (n, cap(he)),
        "325 ml", ["475 ml", "375 ml", "675 ml"],
        "Subtract: 500 − 175. Exchange across the zeros: 500 − 175 = 325 ml. Check: 325 + 175 = 500.",
        ("C", 325))
    n, he, his = P.next()
    add("A recipe needs 300 ml of milk. %s has 1 l of milk. How much milk is left after making the recipe?" % n,
        "700 ml", ["1 l 300 ml", "300 ml", "800 ml"],
        "1 l = 1,000 ml. Subtract: 1,000 − 300 = 700 ml.", ("C", 700))
    add("For a party, Dad buys a 1 l carton of juice and a 500 ml carton of juice. How much juice is there altogether?",
        "1 l 500 ml", ["501 ml", "6 l", "1 l 50 ml"],
        "Add the millilitres to the litres: 1 l + 500 ml = 1 l 500 ml (1,500 ml).", ("C", 1500))
    add("For a party, a jug holds 1 l of squash. Four cups of 200 ml are poured. How much squash is left in the jug?",
        "200 ml", ["800 ml", "600 ml", "1 l 200 ml"],
        "4 cups of 200 ml: 200 + 200 + 200 + 200 = 800 ml. 1 l = 1,000 ml. 1,000 − 800 = 200 ml left.", ("C", 200))
    add("At a party there are 2 l of orange juice. The children drink 1 l 400 ml. How much juice is left?",
        "600 ml", ["1 l 600 ml", "700 ml", "3 l 400 ml"],
        "2 l = 2,000 ml and 1 l 400 ml = 1,400 ml. 2,000 − 1,400 = 600 ml.", ("C", 600))
    add("A fish tank has 5 l of water. 2 l 500 ml more is added. How much water is in the tank now?",
        "7 l 500 ml", ["7 l 5 ml", "2 l 500 ml", "7 l 50 ml"],
        "Add the litres: 5 l + 2 l = 7 l. Then add the 500 ml: 7 l 500 ml.", ("C", 7500))
    n, he, his = P.next()
    add("%s needs ribbon to wrap presents. %s has 2 m of ribbon and uses 75 cm. How much ribbon is left?"
        % (n, cap(he)), "1 m 25 cm", ["1 m 35 cm", "2 m 75 cm", "125 m"],
        "2 m = 200 cm. Subtract: 200 − 75 = 125 cm. 125 cm = 1 m 25 cm.", ("L", 1250))
    n, he, his = P.next()
    n2, he2, his2 = P.next()
    add("On sports day, %s jumps 1 m 85 cm. %s jumps 2 m 10 cm. How much further does %s jump?" % (n, n2, n2),
        "25 cm", ["75 cm", "35 cm", "3 m 95 cm"],
        "1 m 85 cm = 185 cm and 2 m 10 cm = 210 cm. Count on: 185 → 200 is 15 cm, 200 → 210 is 10 cm. "
        "15 + 10 = 25 cm.", ("L", 250))
    add("A brown worm is 45 mm long. A pink worm is 6 cm long. Which worm is longer, and by how much?",
        "the pink worm, by 15 mm", ["the brown worm, by 39 mm", "the pink worm, by 39 mm",
                                    "the brown worm, by 15 mm"],
        "6 cm = 60 mm. 60 mm is more than 45 mm, so the pink worm is longer. 60 − 45 = 15 mm. "
        "Do not take 6 from 45: change to the same unit first.")
    assert len(its) == 20, len(its)
    return {"title": "Add and subtract measures: word problems", "items": its}


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
        "<h2>What we measure</h2>"
        "<p><b>Length</b> is how long something is. <b>Mass</b> is how heavy it is. "
        "<b>Capacity</b> is how much a container holds. Each one has its own units.</p>" +
        table(["Measure", "Units", "Facts"], [
            ["Length", "millimetres (mm), centimetres (cm), metres (m)", "1 cm = 10 mm &nbsp; 1 m = 100 cm"],
            ["Mass", "grams (g), kilograms (kg)", "1 kg = 1,000 g"],
            ["Capacity", "millilitres (ml), litres (l)", "1 l = 1,000 ml"],
        ]) +
        "<h2>Measure with a ruler</h2>"
        "<p>Line up the end of the object with <b>0</b>, not with the edge of the ruler and not with 1. "
        "Read the number at the other end.</p>"
        "<figure class='sn-fig'>" + ruler_svg(0, 46, "crayon") +
        "<figcaption>The crayon goes past 4 cm and then 6 small marks: 4 cm 6 mm, or 46 mm.</figcaption></figure>"
        "<p>If the object does not start at 0, take away the start from the end.</p>"
        "<figure class='sn-fig'>" + ruler_svg(20, 90, "pencil") +
        "<figcaption>The pencil starts at 2 and ends at 9. 9 − 2 = 7, so it is 7 cm long, not 9 cm.</figcaption></figure>"
        "<h2>Read a scale or a jug</h2>"
        "<p>Not every mark has a number. First work out <b>what one mark is worth</b>: "
        "the jump between two numbers ÷ the number of spaces. Then count on from the number before.</p>"
        "<figure class='sn-fig'>" + dial_svg(350, 500, 100, 50) +
        "<figcaption>The numbers go up by 100 g. There are 2 spaces, so each mark is 50 g. "
        "The needle is 1 mark past 300: 350 g.</figcaption></figure>"
        "<figure class='sn-fig'>" + jug_svg(1300, 2000, 500, 100) +
        "<figcaption>The numbers go up by 500 ml. There are 5 spaces, so each line is 100 ml. "
        "The water is 3 lines above 1,000 ml: 1,300 ml = 1 l 300 ml.</figcaption></figure>"
        "<h2>Compare and order</h2>"
        "<p>To compare, change both measures to the <b>same unit</b> first.</p>" +
        ex("Which is longer?", "1 m 5 cm or 150 cm?",
           "1 m = 100 cm, so 1 m 5 cm = 100 + 5 = 105 cm. 105 cm is less than 150 cm.", "150 cm is longer") +
        "<h2>Add and subtract</h2>"
        "<p>Add or subtract like units: metres with metres, centimetres with centimetres. "
        "If you make 100 cm, exchange it for 1 m. If you make 1,000 g, exchange it for 1 kg.</p>" +
        ex("Adding mixed units", "1 m 40 cm + 80 cm",
           "40 cm + 80 cm = 120 cm = 1 m 20 cm. 1 m + 1 m 20 cm = 2 m 20 cm.", "2 m 20 cm") +
        ex("Subtracting from 1 kg", "1 kg − 350 g",
           "1 kg = 1,000 g. 1,000 − 350 = 650.", "650 g") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Starting at 1 or at the edge of the ruler", "Start at 0, or take away the start from the end"],
            ["Counting every mark on a scale as 1 or 10", "Work out what one mark is worth first"],
            ["1 m 5 cm = 15 cm or 150 cm", "1 m = 100 cm, so 1 m 5 cm = 105 cm"],
            ["Thinking 1 kg is less than 900 g", "1 kg = 1,000 g, which is more than 900 g"],
            ["1 m 40 cm + 80 cm = 1 m 120 cm", "Exchange 100 cm for 1 m: 1 m 120 cm = 2 m 20 cm"],
        ])
    )


FAQ = [
    {"q": "What measurement do Year 3 children learn?",
     "a": "Year 3 pupils measure, compare, add and subtract lengths in m, cm and mm, mass in kg and g, and "
          "capacity in l and ml. They use rulers, weighing scales and measuring jugs."},
    {"q": "How do you measure with a ruler in Year 3?",
     "a": "Line up one end of the object with 0 on the ruler, not with 1 or the edge. Read the number at the other end. "
          "Each small mark is 1 mm, and 10 mm make 1 cm."},
    {"q": "How do you read a scale when not every mark has a number?",
     "a": "Find two numbers next to each other and count the spaces between them. Divide the jump by the spaces to find "
          "what one mark is worth, then count on from the number before the needle."},
    {"q": "Is 1 m 5 cm the same as 150 cm?",
     "a": "No. 1 m = 100 cm, so 1 m 5 cm = 105 cm. 150 cm is the same as 1 m 50 cm."},
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
    rnd = random.Random(3308)
    sets = [set_length(rnd), set_mass(rnd), set_capacity(rnd), set_compare(rnd), set_story(rnd)]
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
        "country": "uk", "subject": "maths", "grade": "year-3", "slug": "measuring-length-mass-and-capacity", "sort": 8,
        "updated": UPDATED, "pdf_url": "",
        "title": "Measuring Length, Mass and Capacity",
        "seo_title": "Year 3 Measuring Worksheets: Length, Mass and Capacity with Rulers, Scales and Jugs (Free, with Answers)",
        "short_title": "Measuring length, mass and capacity",
        "domain": "Measurement",
        "standard_code": "Year 3: Measurement",
        "standard_url": "https://www.gov.uk/government/publications/national-curriculum-in-england-mathematics-programmes-of-study",
        "standard_text": "Measure, compare, add and subtract: lengths (m/cm/mm); mass (kg/g); volume/capacity (l/ml).",
        "meta_desc": "Free Year 3 maths worksheets on measuring: lengths in m, cm and mm with a ruler, mass in kg and g on "
                     "scales, capacity in l and ml in jugs, comparing mixed units such as 1 m 5 cm and 150 cm, and "
                     "adding and subtracting measures in word problems. 100 questions with an answer key, matched to "
                     "the National Curriculum.",
        "key_big": "Start at 0, find what one mark is worth, and use the same unit to compare.",
        "key_sub": "1 cm = 10 mm, 1 m = 100 cm, 1 kg = 1,000 g and 1 l = 1,000 ml. So 1 m 5 cm = 105 cm, "
                   "which is shorter than 150 cm.",
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
