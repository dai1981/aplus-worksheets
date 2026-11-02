# -*- coding: utf-8 -*-
"""
UK Year 2 Maths: Measuring (National Curriculum in England, Year 2: Measurement)
  python tools/gen_uk_maths_y2_measuring.py
HTML attributes use single quotes (no backslashes in the JSON).
British English, metric units only, whole units only (no 1 m 20 cm).
Every measurement answer is parsed back to a base unit (cm, g, ml, °C) and checked in code.
Wrong answers come from real mistakes: starting a ruler at 1 or reading the end of an object that does not
start at 0, counting the numbers instead of the spaces, reading the next or the last number on a scale,
counting every mark as 1, choosing m for a pencil or g for a person, and comparing numbers without units.
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "uk", "maths", "year-2")
UPDATED = "2026-11-02"
GREEN = "#006633"
RED = "#c0392b"
INK = "#2b2b2b"
WATER = "#9fd3f2"
WATER_LINE = "#2a7fb8"
WOOD = "#f6e7b8"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Amelia", "Isla", "Freya", "Poppy", "Ava", "Aisha", "Lily", "Zara", "Grace", "Ruby", "Maya", "Evie"]
BOYS = ["Oliver", "Harry", "Mohammed", "Jack", "Arjun", "Noah", "George", "Leo", "Alfie", "Kai", "Ethan", "Charlie"]


# ------------------------------------------------------------ units and checking
UNIT = {"cm": ("L", 1), "m": ("L", 100), "g": ("M", 1), "kg": ("M", 1000),
        "ml": ("C", 1), "litre": ("C", 1000), "litres": ("C", 1000), "°C": ("T", 1)}
MEAS = re.compile(r"^([\d,]+) (cm|m|g|kg|ml|litres|litre|°C)$")


def parse(s):
    """'5 kg' -> ('M', 5000). None if the string is not a plain measurement."""
    mt = MEAS.match(s.strip())
    if not mt:
        return None
    fam, sz = UNIT[mt.group(2)]
    return fam, int(mt.group(1).replace(",", "")) * sz


def truth(st):
    """'2 m &gt; 90 cm' -> True/False."""
    st = st.replace("&lt;", "<").replace("&gt;", ">")
    a, op, b = re.split(r" (<|>|=) ", st)
    pa, pb = parse(a), parse(b)
    assert pa and pb and pa[0] == pb[0], st
    return {"<": pa[1] < pb[1], ">": pa[1] > pb[1], "=": pa[1] == pb[1]}[op]


def c(n):
    return "{:,}".format(n)


def fm(v, unit):
    """7, 'kg' -> '7 kg'; 1, 'litres' -> '1 litre'."""
    if unit == "litres":
        return "%s litre%s" % (c(v), "" if v == 1 else "s")
    return "%s %s" % (c(v), unit)


def want_of(v, unit):
    return UNIT[unit][0], v * UNIT[unit][1]


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e, rnd, want=None):
    """4 choices: correct + 3 unique distractors. Measurement choices of one kind must all differ in value.
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


NAMES = {"pencil": "pencil", "crayon": "crayon", "rubber": "rubber", "ribbon": "ribbon"}


def ruler_svg(s_cm, e_cm, kind="pencil", ncm=None):
    """Centimetre ruler from 0 to ncm with an object exactly from s_cm to e_cm."""
    if ncm is None:
        ncm = max(8, e_cm + 1)
    PX = 32.0
    X0, YR, RH = 18, 40, 42
    W = int(X0 * 2 + PX * ncm + 32)
    H = YR + RH + 4
    X = lambda cm: X0 + PX * cm
    a, b = X(s_cm), X(e_cm)
    o = [draw_object(kind, a, b)]
    for x in (a, b):
        o.append("<line x1='%.1f' y1='32' x2='%.1f' y2='%d' stroke='%s' stroke-width='1.2' stroke-dasharray='3 2'/>"
                 % (x, x, YR, RED))
    o.append("<rect x='4' y='%d' width='%d' height='%d' rx='3' fill='%s' stroke='%s' stroke-width='2'/>"
             % (YR, W - 8, RH, WOOD, INK))
    o.append("<path d='%s' stroke='%s' stroke-width='2'/>"
             % ("".join("M%.1f %dL%.1f %d" % (X(i), YR, X(i), YR + 14) for i in range(ncm + 1)), INK))
    for i in range(ncm + 1):
        o.append(text(X(i), YR + 32, str(i), 15))
    o.append(text(X(ncm) + 18, YR + 32, "cm", 15, anchor="start", bold=False))
    return svg_wrap(W, H, "".join(o), "ruler with a %s from %d cm to %d cm" % (NAMES[kind], s_cm, e_cm))


def dial_svg(v, mx, lab, tick, unit, size=200):
    """Round scale in display units (g or kg). Labels every `lab`, a mark every `tick`. Needle exactly at v."""
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
    if small:
        s.append("<path d='%s' stroke='%s' stroke-width='1.6'/>" % ("".join(small), INK))
    s.append("<path d='%s' stroke='%s' stroke-width='3'/>" % ("".join(big), INK))
    nx, ny = pt(v, R - 9)
    s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='3.5' stroke-linecap='round'/>"
             % (cx, cx, nx, ny, RED))
    s.append("<g font-size='%d' font-weight='700' fill='%s' text-anchor='middle' stroke='#fff' stroke-width='4' "
             "paint-order='stroke'>" % (15 if mx >= 1000 else 17, INK))
    for val in range(0, mx + 1, lab):
        x, y = pt(val, R - 36)
        s.append("<text x='%.1f' y='%.1f'>%s</text>" % (x, y + 6, c(val)))
    s.append("</g>")
    s.append("<circle cx='%.1f' cy='%.1f' r='7' fill='%s'/>" % (cx, cx, RED))
    s.append("<text x='%.1f' y='%.1f' font-size='22' font-weight='800' fill='%s' text-anchor='middle'>%s</text>"
             % (cx, cx + 62, GREEN, unit))
    return svg_wrap(size, size, "".join(s), "weighing scale with the needle at %s" % fm(v, unit))


def jug_svg(v, mx, lab, step, unit, size=200):
    """Measuring jug in display units (ml or litres): a line every `step`, a label every `lab`. Water exactly at v."""
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
            s.append("<text x='%d' y='%.1f'>%s</text>" % (x0 - 7, Y(val) + 5, c(val)))
    s.append("</g>")
    s.append(text(x0 - 7, 198, unit, 15, anchor="end", col=GREEN))
    return svg_wrap(size, size + 6, "".join(s), "measuring jug with water at %s" % fm(v, unit))


def thermo_svg(v, mx, lab, tick, size=200):
    """Thermometer in °C from 0 to mx: a label every `lab`, a mark every `tick`. Liquid exactly at v."""
    tx, tw = 92, 16           # tube left edge and width
    yb, yt = 168, 22          # y of 0 and of mx
    def Y(val):
        return yb - (yb - yt) * float(val) / mx
    s = []
    s.append("<rect x='%d' y='%d' width='%d' height='%d' rx='8' fill='#fff' stroke='%s' stroke-width='3'/>"
             % (tx, yt - 12, tw, yb - yt + 22, INK))
    s.append("<circle cx='%d' cy='%d' r='16' fill='%s' stroke='%s' stroke-width='3'/>" % (tx + tw // 2, yb + 18, RED, INK))
    s.append("<rect x='%d' y='%.1f' width='%d' height='%.1f' fill='%s'/>"
             % (tx + 4, Y(v), tw - 8, yb + 8 - Y(v), RED))
    s.append("<circle cx='%d' cy='%d' r='12.5' fill='%s'/>" % (tx + tw // 2, yb + 18, RED))
    s.append("<g font-size='15' font-weight='700' fill='%s' text-anchor='end'>" % INK)
    for i in range(mx // tick + 1):
        val = i * tick
        major = val % lab == 0
        s.append("<line x1='%d' y1='%.1f' x2='%d' y2='%.1f' stroke='%s' stroke-width='%s'/>"
                 % (tx + tw, Y(val), tx + tw + (18 if major else 10), Y(val), INK, "2.4" if major else "1.4"))
        if major:
            s.append("<text x='%d' y='%.1f'>%d</text>" % (tx - 8, Y(val) + 5, val))
    s.append("</g>")
    s.append(text(162, 102, "°C", 26, col=GREEN))
    return svg_wrap(size, size + 8, "".join(s), "thermometer showing %d °C" % v)


def count_on_e(v, lab, tick, unit, what):
    """Short Year 2 explanation for reading a scale."""
    sp = lab // tick
    base = v - v % lab
    k = (v - base) // tick
    if sp == 1:
        s = "Every mark has a number. "
    else:
        s = ("The numbers go up in %ss. There are %d spaces between two numbers, so each mark is %s. "
             % (c(lab), sp, fm(tick, unit)))
    if k == 0:
        return s + "The %s is right on %s. So it is %s." % (what, c(v), fm(v, unit))
    steps = ", ".join(c(base + i * tick) for i in range(1, k + 1))
    return s + "Count on from %s: %s. So it is %s." % (c(base), steps, fm(v, unit))


def scale_wrong(v, lab, tick, unit, other=None):
    """Wrong answers from real mistakes, most likely first."""
    base = v - v % lab
    k = (v - base) // tick
    w = []
    if k and tick != 1:
        w.append(fm(base + k, unit))           # counts every mark as 1
    if k:
        w.append(fm(base + lab, unit))         # reads the next number
        w.append(fm(base, unit))               # reads the last number
    if other:
        w.append(fm(v, other))                 # wrong unit
    w += [fm(v + tick, unit), fm(v - tick, unit), fm(v + lab, unit), fm(v - lab, unit)]
    return w


# ------------------------------------------------------------ set 1: length with a ruler
def set_length(rnd):
    its = []
    units = ["centimetres (cm)", "metres (m)", "kilograms (kg)", "litres"]
    for obj, ans, e in [
        ("a pencil", "centimetres (cm)", "A pencil is short. It fits on a ruler, so use centimetres."),
        ("the school hall", "metres (m)", "The hall is long. Use metres for long things."),
        ("how tall a tree is", "metres (m)", "A tree is tall. Use metres. Kilograms and litres do not measure length."),
    ]:
        q = ("Which unit would you use to measure %s?" % obj if obj.startswith("how")
             else "Which unit would you use to measure the length of %s?" % obj)
        its.append(mcq(q, ans, [u for u in units if u != ans], e, rnd))
    for e_cm, kind in [(6, "pencil"), (4, "rubber"), (9, "ribbon"), (5, "crayon"), (3, "rubber"),
                       (8, "crayon"), (7, "ribbon"), (11, "pencil"), (10, "crayon"), (12, "ribbon")]:
        nm = NAMES[kind]
        q = fig(ruler_svg(0, e_cm, kind)) + "How long is the %s?" % nm
        e = ("The %s starts at 0 and ends at %d. So it is %d cm long. Count the spaces, not the numbers."
             % (nm, e_cm, e_cm))
        its.append(mcq(q, "%d cm" % e_cm, ["%d cm" % (e_cm + 1), "%d cm" % (e_cm - 1), "%d m" % e_cm], e, rnd,
                       want=("L", e_cm)))
    for s_cm, e_cm, kind in [(2, 8, "pencil"), (1, 5, "rubber"), (3, 10, "crayon"), (2, 11, "ribbon"),
                             (4, 9, "crayon"), (1, 9, "pencil")]:
        nm = NAMES[kind]
        ln = e_cm - s_cm
        q = fig(ruler_svg(s_cm, e_cm, kind)) + "How long is the %s?" % nm
        e = ("The %s starts at %d, not at 0. Count the spaces from %d to %d: there are %d. "
             "Or work it out: %d − %d = %d. So it is %d cm long." % (nm, s_cm, s_cm, e_cm, ln, e_cm, s_cm, ln, ln))
        its.append(mcq(q, "%d cm" % ln, ["%d cm" % e_cm, "%d cm" % (ln + 1), "%d cm" % (ln - 1), "%d m" % ln], e, rnd,
                       want=("L", ln)))
    its.append(mcq("Harry puts one end of his pencil on 1, not on 0. The other end is on 8. How long is the pencil?",
                   "7 cm", ["8 cm", "9 cm", "7 m"],
                   "The pencil starts at 1, so 8 is not the answer. 8 − 1 = 7. The pencil is 7 cm long.", rnd,
                   want=("L", 7)))
    assert len(its) == 20, len(its)
    return {"title": "Measure length with a ruler in cm", "items": its}


# ------------------------------------------------------------ set 2: mass on scales
DIALS = [  # (value, max, label step, mark step, unit, object)
    (3, 5, 1, 1, "kg", "a bag of potatoes"),
    (200, 500, 100, 100, "g", "a bag of pasta"),
    (4, 5, 1, 1, "kg", "a pumpkin"),
    (400, 500, 100, 100, "g", "a box of eggs"),
    (5, 10, 2, 1, "kg", "a bag of dog food"),
    (7, 10, 2, 1, "kg", "a watermelon"),
    (9, 10, 2, 1, "kg", "a box of books"),
    (50, 100, 20, 10, "g", "a bar of chocolate"),
    (90, 100, 20, 10, "g", "a bag of sweets"),
    (300, 1000, 200, 100, "g", "a block of cheese"),
    (500, 1000, 200, 100, "g", "a bag of rice"),
    (700, 1000, 200, 100, "g", "a bunch of bananas"),
    (12, 20, 5, 1, "kg", "a suitcase"),
    (18, 20, 5, 1, "kg", "a big bag of sand"),
]


def set_mass(rnd):
    its = []
    its.append(mcq("Which unit would you use to find the mass of a bag of potatoes?", "kilograms (kg)",
                   ["metres (m)", "litres", "centimetres (cm)"],
                   "Mass is how heavy something is. We measure mass in kilograms (kg) or grams (g).", rnd))
    for obj, ans, wr, e in [
        ("an apple", "100 g", ["100 kg", "10 kg", "1 g"],
         "An apple is light. It is about 100 grams. 100 kg is heavier than a grown-up."),
        ("a bag of sugar", "1 kg", ["1 g", "100 kg", "10 g"],
         "A bag of sugar is about 1 kilogram. 1 g is about as heavy as a paper clip."),
        ("a Year 2 child", "20 kg", ["20 g", "200 kg", "2 kg"],
         "A Year 2 child is about 20 kilograms. 20 g is lighter than a bar of chocolate."),
    ]:
        its.append(mcq("What is the best estimate for the mass of %s?" % obj, ans, wr, e, rnd))
    for v, mx, lab, tick, unit, obj in DIALS:
        q = fig(dial_svg(v, mx, lab, tick, unit)) + "The scale shows %s. What is the mass?" % obj
        other = "g" if unit == "kg" else "kg"
        its.append(mcq(q, fm(v, unit), scale_wrong(v, lab, tick, unit, other),
                       count_on_e(v, lab, tick, unit, "needle"), rnd, want=want_of(v, unit)))
    its.append(mcq(fig(dial_svg(6, 10, 2, 1, "kg")) +
                   "The scale shows a parcel. Mum puts a 2 kg bag on the scale too. What will the scale show now?",
                   "8 kg", ["6 kg", "4 kg", "7 kg"],
                   "The needle is at 6 kg. Mum adds 2 kg, so add: 6 + 2 = 8 kg.", rnd, want=("M", 8000)))
    its.append(mcq(fig(dial_svg(300, 500, 100, 100, "g")) +
                   "The scale shows some flour. How much more flour is needed to make 500 g?",
                   "200 g", ["800 g", "300 g", "100 g"],
                   "The needle is at 300 g. Count on from 300 to 500: 400, 500. That is 200 g more.",
                   rnd, want=("M", 200)))
    assert len(its) == 20, len(its)
    return {"title": "Read scales: mass in kg and g", "items": its}


# ------------------------------------------------------------ set 3: capacity in jugs
JUGS = [  # (value, max, label step, line step, unit)
    (300, 500, 100, 100, "ml"),
    (2, 5, 1, 1, "litres"),
    (400, 500, 100, 100, "ml"),
    (4, 5, 1, 1, "litres"),
    (3, 10, 2, 1, "litres"),
    (7, 10, 2, 1, "litres"),
    (40, 100, 20, 10, "ml"),
    (70, 100, 20, 10, "ml"),
    (300, 1000, 200, 100, "ml"),
    (500, 1000, 200, 100, "ml"),
    (900, 1000, 200, 100, "ml"),
    (25, 50, 10, 5, "ml"),
    (35, 50, 10, 5, "ml"),
]


def set_capacity(rnd):
    its = []
    for q, ans, wr, e in [
        ("Which unit would you use to measure the water in a bath?", "litres",
         ["kilograms (kg)", "centimetres (cm)", "metres (m)"],
         "A bath holds a lot of water. We measure lots of water in litres."),
        ("Which unit would you use to measure medicine on a spoon?", "millilitres (ml)",
         ["litres", "kilograms (kg)", "metres (m)"],
         "A spoon holds only a little. We measure a little water in millilitres (ml)."),
    ]:
        its.append(mcq(q, ans, wr, e, rnd))
    for obj, ans, wr, e in [
        ("a cup", "200 ml", ["200 litres", "2 ml", "20 litres"],
         "A cup holds about 200 millilitres. 200 litres would fill a bath."),
        ("a bucket", "10 litres", ["10 ml", "100 litres", "1 ml"],
         "A bucket holds about 10 litres. 10 ml is only two teaspoons."),
        ("a teaspoon", "5 ml", ["5 litres", "500 ml", "50 litres"],
         "A teaspoon holds only a little, about 5 millilitres."),
    ]:
        its.append(mcq("What is the best estimate for how much %s holds?" % obj, ans, wr, e, rnd))
    for v, mx, lab, step, unit in JUGS:
        q = fig(jug_svg(v, mx, lab, step, unit)) + "How much water is in the jug?"
        other = "litres" if unit == "ml" else "ml"
        its.append(mcq(q, fm(v, unit), scale_wrong(v, lab, step, unit, other),
                       count_on_e(v, lab, step, unit, "water"), rnd, want=want_of(v, unit)))
    its.append(mcq(fig(jug_svg(200, 500, 100, 100, "ml")) + "How much more water is needed to fill the jug to 500 ml?",
                   "300 ml", ["700 ml", "200 ml", "400 ml"],
                   "The water is at 200 ml. Count on from 200 to 500: 300, 400, 500. That is 300 ml more.", rnd,
                   want=("C", 300)))
    its.append(mcq(fig(jug_svg(800, 1000, 200, 100, "ml")) + "Jack pours 200 ml out of the jug. How much water is left?",
                   "600 ml", ["1,000 ml", "800 ml", "700 ml"],
                   "Each line is 100 ml, so the water is at 800 ml. Pouring out means take away: 800 − 200 = 600 ml.",
                   rnd, want=("C", 600)))
    assert len(its) == 20, len(its)
    return {"title": "Read jugs: capacity in ml and litres", "items": its}


# ------------------------------------------------------------ set 4: temperature
THERMOS = [  # (value, max, label step, mark step, place)
    (7, 20, 5, 1, "outside on a cold morning"),
    (13, 20, 5, 1, "in the garden"),
    (18, 20, 5, 1, "in the school hall"),
    (15, 50, 10, 5, "in the playground"),
    (25, 50, 10, 5, "outside on a sunny day"),
    (35, 50, 10, 5, "in a greenhouse in summer"),
    (14, 40, 10, 2, "in the park in spring"),
    (26, 40, 10, 2, "on the beach"),
    (32, 40, 10, 2, "in a hot car"),
    (70, 100, 20, 10, "in a cup of tea"),
    (90, 100, 20, 10, "in water from the kettle"),
]


def set_temperature(rnd):
    its = []
    its.append(mcq("What do we use to measure temperature?", "a thermometer",
                   ["a ruler", "a weighing scale", "a measuring jug"],
                   "A thermometer measures how hot or cold something is. Temperature is measured in degrees Celsius (°C).",
                   rnd))
    for obj, ans, wr, e in [
        ("in a classroom", "20 °C", ["2 °C", "50 °C", "100 °C"],
         "A classroom is warm, but not hot. It is about 20 °C."),
        ("outside on a hot summer day in the UK", "25 °C", ["5 °C", "100 °C", "60 °C"],
         "A hot day in the UK is about 25 °C. 5 °C is cold, and 100 °C is as hot as boiling water."),
        ("outside on a snowy day", "2 °C", ["20 °C", "30 °C", "50 °C"],
         "Snow needs it to be very cold. Water freezes at 0 °C, so a snowy day is about 2 °C."),
    ]:
        its.append(mcq("What is the best estimate for the temperature %s?" % obj, ans, wr, e, rnd))
    for v, mx, lab, tick, place in THERMOS:
        q = fig(thermo_svg(v, mx, lab, tick)) + "This thermometer is %s. What temperature does it show?" % place
        its.append(mcq(q, fm(v, "°C"), scale_wrong(v, lab, tick, "°C"),
                       count_on_e(v, lab, tick, "°C", "red line"), rnd, want=("T", v)))
    sts = ["14 °C &gt; 9 °C", "14 °C &lt; 9 °C", "14 °C = 9 °C", "9 °C &gt; 14 °C"]
    assert [truth(s) for s in sts] == [True, False, False, False]
    its.append(mcq("On Monday it was 14 °C. On Tuesday it was 9 °C. Which is true?", sts[0], sts[1:],
                   "14 is more than 9, so Monday was warmer. 14 °C &gt; 9 °C. The open side of &gt; faces the bigger number.",
                   rnd))
    ch = ["12 °C", "21 °C", "2 °C", "20 °C"]
    assert min(ch, key=lambda x: parse(x)[1]) == "2 °C"
    its.append(mcq("Which temperature is the coldest?", "2 °C", ["12 °C", "21 °C", "20 °C"],
                   "The coldest temperature is the smallest number. 2 is smaller than 12, 20 and 21.", rnd))
    its.append(mcq(fig(thermo_svg(12, 20, 5, 1)) + "It gets 5 degrees warmer. What will the temperature be?",
                   "17 °C", ["7 °C", "12 °C", "16 °C"],
                   "The thermometer shows 12 °C. Warmer means add: 12 + 5 = 17 °C.", rnd, want=("T", 17)))
    its.append(mcq(fig(thermo_svg(30, 50, 10, 5)) + "It gets 10 degrees warmer. What will the temperature be?",
                   "40 °C", ["20 °C", "35 °C", "31 °C"],
                   "Each mark is 5 °C, so it shows 30 °C. Warmer means add: 30 + 10 = 40 °C.", rnd, want=("T", 40)))
    its.append(mcq(fig(thermo_svg(20, 40, 10, 2)) + "At night it gets 6 degrees colder. What will the temperature be?",
                   "14 °C", ["26 °C", "17 °C", "20 °C"],
                   "The thermometer shows 20 °C. Colder means take away: 20 − 6 = 14 °C.", rnd, want=("T", 14)))
    assert len(its) == 20, len(its)
    return {"title": "Read a thermometer in °C", "items": its}


# ------------------------------------------------------------ set 5: compare, choose units, word problems
def set_story(rnd):
    P = People(rnd)
    its = []

    def add(q, r, w, e, want=None):
        its.append(mcq(q, r, w, e, rnd, want=want))

    for sts, e in [
        (["45 cm &lt; 54 cm", "45 cm &gt; 54 cm", "45 cm = 54 cm", "54 cm &lt; 45 cm"],
         "Look at the tens. 4 tens is less than 5 tens, so 45 cm &lt; 54 cm."),
        (["1 m = 100 cm", "1 m = 10 cm", "1 m = 1 cm", "1 m = 1,000 cm"],
         "A metre stick has 100 centimetres on it. So 1 m = 100 cm."),
        (["2 m &gt; 90 cm", "2 m &lt; 90 cm", "2 m = 90 cm", "90 cm &gt; 2 m"],
         "1 m = 100 cm, so 2 m = 200 cm. 200 cm is more than 90 cm. Do not just compare 2 and 90."),
        (["5 kg &gt; 50 g", "5 kg &lt; 50 g", "5 kg = 50 g", "50 g &gt; 5 kg"],
         "A kilogram is much heavier than a gram: 1 kg = 1,000 g. So 5 kg is more than 50 g, "
         "even though 5 is less than 50."),
    ]:
        assert [truth(s) for s in sts] == [True, False, False, False], sts
        add("Which is true?", sts[0], sts[1:], e)
    ch = ["1 litre", "500 ml", "100 ml", "10 ml"]
    assert max(ch, key=lambda x: parse(x)[1]) == "1 litre"
    add("Which holds the most?", "1 litre", ch[1:],
        "1 litre = 1,000 ml. That is more than 500 ml. Look at the units, not just the numbers.")
    for q, lists, e in [
        ("Which list goes from the shortest to the longest?",
         [["9 cm", "12 cm", "21 cm"], ["21 cm", "12 cm", "9 cm"], ["12 cm", "21 cm", "9 cm"], ["9 cm", "21 cm", "12 cm"]],
         "9 is the smallest number and 21 is the biggest. So the order is 9 cm, 12 cm, 21 cm."),
        ("Which list goes from the lightest to the heaviest?",
         [["5 kg", "15 kg", "50 kg"], ["50 kg", "15 kg", "5 kg"], ["15 kg", "5 kg", "50 kg"], ["5 kg", "50 kg", "15 kg"]],
         "5 is the smallest number and 50 is the biggest. So the order is 5 kg, 15 kg, 50 kg."),
    ]:
        vs = [[parse(x)[1] for x in l] for l in lists]
        assert vs[0] == sorted(vs[0]) and all(v != sorted(v) for v in vs[1:]), q
        add(q, ", ".join(lists[0]), [", ".join(l) for l in lists[1:]], e)
    add("About how long is a pencil?", "15 cm", ["15 m", "1 cm", "50 m"],
        "A pencil fits on a ruler, so it is about 15 cm. 15 m is longer than a classroom!")
    add("About how tall is a door?", "2 m", ["2 cm", "20 m", "20 cm"],
        "A door is taller than a grown-up, so it is about 2 m. 2 cm is shorter than your finger.")

    n, he, his = P.next()
    add("%s has 45 cm of ribbon. %s cuts off 20 cm. How much ribbon is left?" % (n, cap(he)),
        "25 cm", ["65 cm", "35 cm", "25 m"], "Cutting off means take away: 45 − 20 = 25 cm.", ("L", 25))
    n, he, his = P.next()
    add("%s has two pieces of string. One is 23 cm long. The other is 34 cm long. "
        "How much string is there altogether?" % n,
        "57 cm", ["11 cm", "47 cm", "67 cm"], "Altogether means add: 23 + 34 = 57 cm.", ("L", 57))
    add("A sunflower is 60 cm tall. It grows 25 cm more. How tall is it now?",
        "85 cm", ["35 cm", "75 cm", "95 cm"], "It grows, so add: 60 + 25 = 85 cm.", ("L", 85))
    n, he, his = P.next()
    n2, he2, his2 = P.next()
    add("%s builds a tower 48 cm tall. %s builds a tower 30 cm tall. How much taller is %s’s tower?" % (n, n2, n),
        "18 cm", ["78 cm", "28 cm", "12 cm"], "How much taller means find the difference: 48 − 30 = 18 cm.", ("L", 18))
    add("A cat weighs 4 kg. A dog weighs 12 kg. How much heavier is the dog?",
        "8 kg", ["16 kg", "12 kg", "9 kg"], "Find the difference: 12 − 4 = 8 kg.", ("M", 8000))
    n, he, his = P.next()
    add("%s makes biscuits. %s uses 50 g of butter and 40 g of sugar. How much is that altogether?" % (n, cap(he)),
        "90 g", ["10 g", "80 g", "90 kg"], "Altogether means add: 50 + 40 = 90 g.", ("M", 90))
    n, he, his = P.next()
    add("%s has a 500 ml bottle of water. %s drinks 200 ml at lunchtime. How much water is left?" % (n, cap(he)),
        "300 ml", ["700 ml", "200 ml", "400 ml"], "Drinks means take away: 500 − 200 = 300 ml.", ("C", 300))
    add("A bucket holds 5 litres. How much water do 4 buckets hold?",
        "20 litres", ["9 litres", "1 litre", "25 litres"],
        "4 lots of 5 litres: 5, 10, 15, 20. So 4 × 5 = 20 litres.", ("C", 20000))
    n, he, his = P.next()
    add("%s fills a 10 litre paddling pool with a 2 litre jug. How many jugs of water does %s need?" % (n, he),
        "5 jugs", ["8 jugs", "12 jugs", "20 jugs"],
        "How many 2s make 10? Count in 2s: 2, 4, 6, 8, 10. That is 5 jugs. 10 ÷ 2 = 5.")
    add("In the morning it was 8 °C. At lunchtime it was 15 °C. How many degrees warmer was it at lunchtime?",
        "7 °C", ["23 °C", "8 °C", "6 °C"],
        "Find the difference. Count on from 8 to 15: 8 to 10 is 2, 10 to 15 is 5. 2 + 5 = 7 °C.", ("T", 7))
    add("In the afternoon it was 21 °C. In the evening it was 6 degrees colder. What was the temperature in the evening?",
        "15 °C", ["27 °C", "16 °C", "6 °C"], "Colder means take away: 21 − 6 = 15 °C.", ("T", 15))
    assert len(its) == 20, len(its)
    return {"title": "Compare measures and solve word problems", "items": its}


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
        "<p>We measure with <b>units</b>. Each kind of measure has its own units and its own tool.</p>" +
        table(["Measure", "Units", "Tool"], [
            ["Length and height (how long or tall)", "centimetres (cm), metres (m)", "ruler, metre stick"],
            ["Mass (how heavy)", "grams (g), kilograms (kg)", "weighing scale"],
            ["Capacity (how much it holds)", "millilitres (ml), litres", "measuring jug"],
            ["Temperature (how hot or cold)", "degrees Celsius (°C)", "thermometer"],
        ]) +
        "<p>Use small units for small things and big units for big things. "
        "A pencil is about 15 cm long. A door is about 2 m tall.</p>"
        "<h2>Measure with a ruler</h2>"
        "<p>Put one end of the object on <b>0</b>, not on 1 and not on the edge of the ruler. "
        "Read the number at the other end.</p>"
        "<figure class='sn-fig'>" + ruler_svg(0, 6, "pencil") +
        "<figcaption>The pencil starts at 0 and ends at 6. It is 6 cm long.</figcaption></figure>"
        "<p>If the object does not start at 0, count the spaces from the start to the end.</p>"
        "<figure class='sn-fig'>" + ruler_svg(2, 7, "crayon") +
        "<figcaption>The crayon starts at 2 and ends at 7. There are 5 spaces, so it is 5 cm long, not 7 cm.</figcaption></figure>"
        "<h2>Read a scale, a jug or a thermometer</h2>"
        "<p>Not every mark has a number. First find <b>what each mark is worth</b>. "
        "Look at how the numbers go up, and count the spaces between them. Then count on from the number before.</p>"
        "<figure class='sn-fig'>" + dial_svg(7, 10, 2, 1, "kg") +
        "<figcaption>The numbers go up in 2s. There are 2 spaces between them, so each mark is 1 kg. "
        "Count on from 6: 7. The mass is 7 kg.</figcaption></figure>"
        "<figure class='sn-fig'>" + jug_svg(300, 1000, 200, 100, "ml") +
        "<figcaption>The numbers go up in 200s. There are 2 spaces, so each line is 100 ml. "
        "Count on from 200: 300. There is 300 ml of water.</figcaption></figure>"
        "<figure class='sn-fig'>" + thermo_svg(15, 50, 10, 5) +
        "<figcaption>The numbers go up in 10s. There are 2 spaces, so each mark is 5 °C. "
        "Count on from 10: 15. It is 15 °C.</figcaption></figure>"
        "<h2>Compare and order</h2>"
        "<p>Use &lt; (less than), &gt; (more than) and = (equal to). The open side faces the bigger amount. "
        "Check the <b>units</b> as well as the numbers.</p>" +
        ex("Which is longer?", "2 m or 90 cm?",
           "1 m = 100 cm, so 2 m = 200 cm. 200 cm is more than 90 cm.", "2 m &gt; 90 cm") +
        ex("Which is heavier?", "5 kg or 50 g?",
           "A kilogram is much heavier than a gram. 5 kg is more, even though 5 is less than 50.", "5 kg &gt; 50 g") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Starting the ruler at 1 or at the edge", "Start at 0, or count the spaces from the start"],
            ["Counting every mark on a scale as 1", "Work out what each mark is worth first"],
            ["Reading the next number on the scale", "Count on from the number before the needle"],
            ["Saying a pencil is 15 m long", "Small things are measured in cm, big things in m"],
            ["Saying 50 g is more than 5 kg", "Look at the units: 1 kg = 1,000 g"],
        ])
    )


FAQ = [
    {"q": "What measuring do Year 2 children learn?",
     "a": "Year 2 pupils measure length and height in cm and m, mass in kg and g, capacity in litres and ml, "
          "and temperature in °C. They use rulers, scales, jugs and thermometers, and compare with <, > and =."},
    {"q": "How do you teach a Year 2 child to use a ruler?",
     "a": "Show them how to put one end of the object on 0, not on 1 or the edge of the ruler. "
          "Then read the number at the other end and say the unit, such as 6 cm."},
    {"q": "How do you read a scale when not every mark has a number?",
     "a": "Look at how the numbers go up and count the spaces between two numbers to find what each mark is worth. "
          "Then count on from the number before the needle or the water line."},
    {"q": "Do Year 2 children need to know that 1 m = 100 cm?",
     "a": "Year 2 pupils choose the right unit and compare measures. Knowing that 1 m = 100 cm and "
          "1 kg = 1,000 g helps them see that 2 m is longer than 90 cm."},
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
    rnd = random.Random(2210)
    sets = [set_length(rnd), set_mass(rnd), set_capacity(rnd), set_temperature(rnd), set_story(rnd)]
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
        "country": "uk", "subject": "maths", "grade": "year-2", "slug": "measuring", "sort": 10,
        "updated": UPDATED, "pdf_url": "",
        "title": "Measuring: Length, Mass, Capacity and Temperature",
        "seo_title": "Year 2 Measuring Worksheets: Rulers, Scales, Jugs and Thermometers (Free, with Answers)",
        "short_title": "Measuring",
        "domain": "Measurement",
        "standard_code": "Year 2: Measurement",
        "standard_url": "https://www.gov.uk/government/publications/national-curriculum-in-england-mathematics-programmes-of-study",
        "standard_text": "Choose and use appropriate standard units to estimate and measure length/height in any direction "
                         "(m/cm); mass (kg/g); temperature (°C); capacity (litres/ml) to the nearest appropriate unit, "
                         "using rulers, scales, thermometers and measuring vessels; compare and order lengths, mass, "
                         "volume/capacity and record the results using >, < and =.",
        "meta_desc": "Free Year 2 maths worksheets on measuring: lengths in cm with a ruler, mass in kg and g on scales, "
                     "capacity in ml and litres in jugs, temperature in °C on a thermometer, choosing sensible units "
                     "and comparing with <, > and =. 100 questions with an answer key, matched to the National Curriculum.",
        "key_big": "Start at 0, find what each mark is worth, and always check the unit.",
        "key_sub": "A pencil is about 15 cm, not 15 m. 5 kg is heavier than 50 g, because a kilogram is much "
                   "heavier than a gram.",
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
