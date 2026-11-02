# -*- coding: utf-8 -*-
"""
AU Year 3 Maths: Measuring Length, Mass and Capacity (Australian Curriculum v9.0, AC9M3M01 and AC9M3M02)
  python tools/gen_au_maths_y3_measuring.py
HTML attributes use single quotes (no backslashes in the JSON).
Australian English, metric units only, mL and L with a capital L. 4-digit numbers have no separator (1000 g).
Every measurement answer is parsed back to a base unit (mm, g, mL) and checked in code.
Wrong answers come from real mistakes: choosing km for a pencil or a mass unit for a length, starting at 1
on the ruler, reading the end of an object that does not start at 0, counting every mark as 1 or 10,
reading the next labelled number, writing the wrong unit, and comparing numbers without their units.
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "au", "maths", "year-3")
UPDATED = "2026-11-02"
GREEN = "#006633"
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
UNIT = {"mm": ("L", 1), "cm": ("L", 10), "m": ("L", 1000), "km": ("L", 1000000),
        "g": ("M", 1), "kg": ("M", 1000), "mL": ("C", 1), "L": ("C", 1000)}
TOK = re.compile(r"([\d" + NBSP + r"]+)\s*(" + "|".join(sorted(UNIT, key=len, reverse=True)) + r")(?![a-zA-Z])")


def parse(s):
    """'1 kg' -> ('M', 1000). None if the string is not a plain measurement."""
    s = s.strip()
    pos, fam, tot = 0, None, 0
    for mt in TOK.finditer(s):
        if s[pos:mt.start()].strip():
            return None
        fu, sz = UNIT[mt.group(2)]
        if fam and fu != fam:
            return None
        fam = fu
        tot += int(mt.group(1).replace(NBSP, "")) * sz
        pos = mt.end()
    if fam is None or s[pos:].strip():
        return None
    return fam, tot


def truth(st):
    """'1 kg > 900 g' -> True/False (chains allowed)."""
    parts = re.split(r" (<|>|=) ", st)
    vals = [parse(p) for p in parts[0::2]]
    assert all(vals) and len({v[0] for v in vals}) == 1, st
    ok = True
    for i, op in enumerate(parts[1::2]):
        a, b = vals[i][1], vals[i + 1][1]
        ok = ok and {"<": a < b, ">": a > b, "=": a == b}[op]
    return ok


def c(n):
    """Australian style: 4 digits plain (1000), 5 or more digits grouped with a no-break space."""
    if n < 10000:
        return str(n)
    return "{:,}".format(n).replace(",", NBSP)


def gs(v):
    return "%s g" % c(v)


def kgs(v):
    assert v % 1000 == 0
    return "%d kg" % (v // 1000)


def mls(v):
    return "%s mL" % c(v)


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
    return svg_wrap(W, H, "".join(o), "ruler with %s %s from %d mm to %d mm" % ("an" if kind == "eraser" else "a", NAMES[kind], s_mm, e_mm))


def dial_body(v, mx, lab, tick, div, size, ox=0, oy=0):
    """Round scale body, values in grams. Labels every `lab` g shown as val/div. Needle exactly at v."""
    unit = "g" if div == 1 else "kg"
    cx, cy = ox + size / 2.0, oy + size / 2.0
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
        s.append("<text x='%.1f' y='%.1f'>%s</text>" % (x, y + 6, c(val // div)))
    s.append("</g>")
    s.append("<circle cx='%.1f' cy='%.1f' r='7' fill='%s'/>" % (cx, cy, RED))
    s.append("<text x='%.1f' y='%.1f' font-size='22' font-weight='800' fill='%s' text-anchor='middle'>%s</text>"
             % (cx, cy + 62, GREEN, unit))
    return "".join(s)


def wlabel(v, div):
    return gs(v) if div == 1 else kgs(v)


def dial_svg(v, mx, lab, tick, div=1, size=200):
    return svg_wrap(size, size, dial_body(v, mx, lab, tick, div, size),
                    "weighing scale with the needle at %s" % wlabel(v, div))


def dial_pair_svg(va, vb, mx, lab, tick, div=1):
    """Two scales side by side, labelled A and B (one SVG)."""
    size = 180
    body = (dial_body(va, mx, lab, tick, div, size, 0, 0) + dial_body(vb, mx, lab, tick, div, size, size + 30, 0) +
            text(size / 2.0, size + 26, "A", 20) + text(size * 1.5 + 30, size + 26, "B", 20))
    return svg_wrap(size * 2 + 30, size + 34, body, "two weighing scales: A at %s and B at %s"
                    % (wlabel(va, div), wlabel(vb, div)))


def jug_svg(v, mx, lab, step, size=200):
    """Measuring jug, values in mL: a line every `step` mL, a label every `lab` mL. Water exactly at v."""
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
    s.append(text(x0 - 7, 198, "mL", 15, anchor="end", col=GREEN))
    return svg_wrap(size, size + 6, "".join(s), "measuring jug with water at %s" % mls(v))


# ------------------------------------------------------------ set 1: choose the unit and estimate
def set_units(rnd):
    its = []
    for obj, ans, wr, e in [
        ("the length of a pencil", "cm", ["km", "m", "kg"],
         "A pencil is short and fits on a ruler, so use centimetres. Kilometres are for long trips, like a drive "
         "to the next town."),
        ("the length of the school swimming pool", "m", ["cm", "km", "L"],
         "A pool is long, but you can walk along it in a minute, so use metres. Litres measure capacity, not length."),
        ("the distance from Sydney to Melbourne", "km", ["m", "cm", "kg"],
         "Sydney to Melbourne is a long trip by car or plane, so use kilometres."),
        ("the mass of a watermelon", "kg", ["g", "L", "m"],
         "A watermelon is heavy, so use kilograms. Litres measure how much a container holds."),
        ("the mass of a strawberry", "g", ["kg", "mL", "cm"],
         "A strawberry is very light, so use grams."),
        ("how much water a bathtub holds", "L", ["mL", "kg", "m"],
         "A bathtub holds a lot of water, so use litres."),
        ("how much medicine fits on a spoon", "mL", ["L", "g", "cm"],
         "A spoon holds only a little, so use millilitres."),
        ("the mass of a school backpack", "kg", ["g", "km", "L"],
         "A full backpack is quite heavy, so use kilograms."),
        ("the length of a cricket pitch", "m", ["km", "kg", "mL"],
         "A cricket pitch is about 20 m long. You can walk along it in a short time, so use metres."),
    ]:
        its.append(mcq("Which unit is best to measure %s?" % obj, ans, wr, e, rnd))
    its.append(mcq("Which unit measures <b>mass</b>?", "kilograms (kg)",
                   ["kilometres (km)", "litres (L)", "metres (m)"],
                   "Mass is how heavy something is. We measure mass in grams and kilograms. "
                   "Kilometres sound like kilograms, but they measure length.", rnd))
    its.append(mcq("Which unit measures <b>capacity</b>?", "litres (L)",
                   ["metres (m)", "kilograms (kg)", "centimetres (cm)"],
                   "Capacity is how much a container holds. We measure it in millilitres and litres.", rnd))
    for q, ans, wr, e in [
        ("A classroom door is about ☐ tall.", "2 m", ["2 cm", "2 km", "20 m"],
         "You are about 1 m 30 cm tall, and a door is a bit taller than an adult. That is about 2 m. "
         "2 cm is shorter than your finger."),
        ("A new pencil is about ☐ long.", "18 cm", ["18 m", "18 km", "18 mm"],
         "A pencil fits on a 30 cm ruler, so it is about 18 cm long. 18 m is longer than a classroom."),
        ("A Year 3 student is about ☐ tall.", "130 cm", ["130 m", "13 cm", "130 km"],
         "Most Year 3 students are between 1 m and 1 m 50 cm tall. 130 cm fits. 13 cm is the size of a hand."),
        ("A large carton of milk holds about ☐.", "2 L", ["2 mL", "200 L", "20 L"],
         "Big milk cartons from the supermarket hold 2 L. 2 mL is less than half a teaspoon."),
        ("A can of soft drink holds about ☐.", "375 mL", ["375 L", "37 mL", "3 L"],
         "Australian drink cans hold 375 mL. 375 L would fill about two bathtubs."),
        ("A whole watermelon has a mass of about ☐.", "6 kg", ["6 g", "60 kg", "600 g"],
         "A whole watermelon is heavy to carry, about 6 kg. 6 g is as light as six paper clips, "
         "and 60 kg is as heavy as a grown-up."),
        ("A paper clip has a mass of about ☐.", "1 g", ["1 kg", "100 g", "10 kg"],
         "A paper clip is very light. 1 g is about the mass of one paper clip."),
        ("A teaspoon holds about ☐.", "5 mL", ["5 L", "500 mL", "50 L"],
         "A teaspoon holds only a little, about 5 mL. 5 L would half fill a bucket."),
        ("A bag of sugar from the supermarket has a mass of about ☐.", "1 kg", ["1 g", "100 kg", "10 g"],
         "Sugar is often sold in 1 kg bags. 100 kg is heavier than a grown-up."),
    ]:
        its.append(mcq("Choose the best estimate. " + q, ans, wr, e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Choose the unit and estimate", "items": its}


# ------------------------------------------------------------ set 2: length with a ruler
def set_length(rnd):
    its = []
    its.append(mcq("How many centimetres are in 1 metre?", "100 cm", ["10 cm", "1000 cm", "50 cm"],
                   "A metre ruler has 100 centimetres marked on it. So 1 m = 100 cm.", rnd, want=("L", 1000)))
    its.append(mcq("How many millimetres are in 1 centimetre?", "10 mm", ["100 mm", "1 mm", "5 mm"],
                   "Look at a ruler. There are 10 small spaces in each centimetre. So 1 cm = 10 mm.", rnd,
                   want=("L", 10)))
    # whole cm, starting at 0
    for e_cm, kind in [(7, "pencil"), (5, "crayon"), (4, "eraser"), (8, "ribbon"), (6, "crayon")]:
        nm = NAMES[kind]
        q = fig(ruler_svg(0, e_cm * 10, kind)) + "How long is the %s?" % nm
        e = ("The %s starts at 0 and ends at %d. So it is %d cm long. Count the spaces, not the marks."
             % (nm, e_cm, e_cm))
        its.append(mcq(q, "%d cm" % e_cm, ["%d cm" % (e_cm + 1), "%d cm" % (e_cm - 1), "%d m" % e_cm], e, rnd,
                       want=("L", e_cm * 10)))
    # whole cm, not starting at 0
    for s_cm, e_cm, kind in [(2, 9, "pencil"), (1, 6, "crayon"), (3, 7, "eraser"), (2, 8, "ribbon"),
                             (1, 9, "pencil"), (4, 9, "crayon")]:
        nm = NAMES[kind]
        ln = e_cm - s_cm
        q = fig(ruler_svg(s_cm * 10, e_cm * 10, kind)) + "How long is the %s?" % nm
        e = ("The %s starts at %d, not at 0. It ends at %d. %d − %d = %d, so it is %d cm long. "
             "You can also count the spaces: there are %d." % (nm, s_cm, e_cm, e_cm, s_cm, ln, ln, ln))
        its.append(mcq(q, "%d cm" % ln, ["%d cm" % e_cm, "%d cm" % (ln + 1), "%d cm" % (e_cm + s_cm),
                                         "%d cm" % (ln - 1)], e, rnd, want=("L", ln * 10)))
    for n, s_cm, e_cm in [("Lachlan", 1, 8), ("Harper", 1, 12)]:
        he = "he" if n == "Lachlan" else "she"
        thing = "his pencil" if n == "Lachlan" else "her book"
        ln = e_cm - s_cm
        its.append(mcq("%s puts the end of %s at 1 on the ruler, not at 0. The other end is at %d. "
                       "How long is it?" % (n, thing, e_cm), "%d cm" % ln,
                       ["%d cm" % e_cm, "%d cm" % (e_cm + 1), "%d cm" % (ln - 1)],
                       "%s started at 1, so the number at the end is 1 too big. %d − 1 = %d cm."
                       % (cap(he), e_cm, ln), rnd, want=("L", ln * 10)))
    # cm and mm, starting at 0 (lightly)
    for e_mm, kind in [(46, "crayon"), (63, "pencil"), (35, "eraser")]:
        nm = NAMES[kind]
        a, b = divmod(e_mm, 10)
        q = fig(ruler_svg(0, e_mm, kind)) + "How long is the %s in millimetres?" % nm
        e = ("The %s goes past %d cm and then %s more. %d cm = %d mm, and %d + %d = %d. So it is %d mm long."
             % (nm, a, marks(b, "small mark"), a, a * 10, a * 10, b, e_mm, e_mm))
        its.append(mcq(q, "%d mm" % e_mm, ["%d mm" % (a + b), "%d mm" % (a * 100 + b), "%d cm" % e_mm,
                                           "%d mm" % (e_mm + 10)], e, rnd, want=("L", e_mm)))
    its.append(mcq(fig(ruler_svg(20, 74, "pencil")) + "How long is the pencil in millimetres?", "54 mm",
                   ["74 mm", "64 mm", "54 cm"],
                   "The pencil starts at 2 cm, not at 0. It ends at 7 cm and 4 small marks, which is 74 mm. "
                   "2 cm = 20 mm. 74 − 20 = 54 mm.", rnd, want=("L", 54)))
    its.append(mcq("Which tool is best to measure the length of your desk?", "a ruler or tape measure",
                   ["a measuring jug", "kitchen scales", "a clock"],
                   "Length is measured with a ruler or a tape measure. A jug measures capacity, scales measure mass "
                   "and a clock measures time.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Measure length with a ruler", "items": its}


# ------------------------------------------------------------ set 3: mass on scales
def dial_e(v, lab, tick, div):
    sp = lab // tick
    base = v - v % lab
    k = (v - base) // tick
    if div == 1:
        s = ("The numbers go up by %d g. There are %d spaces between numbers, so each mark is %d ÷ %d = %d g. "
             % (lab, sp, lab, sp, tick))
        if k == 0:
            return s + "The needle points right at %d: %d g." % (base, v)
        if base == 0:
            return s + "The needle is %s past 0: %d g." % (marks(k), v)
        return s + "The needle is %s past %d: %d + %d = %d g." % (marks(k), base, base, k * tick, v)
    L, T = lab // 1000, tick // 1000
    s = ("The numbers go up by %d kg. There are %d spaces between numbers, so each mark is %d kg. "
         % (L, sp, T))
    if k == 0:
        return s + "The needle points right at %d: %d kg." % (base // 1000, v // 1000)
    return s + "The needle is %s past %d: %d + %d = %d kg." % (marks(k), base // 1000, base // 1000, k * T, v // 1000)


DIALS = [  # (value g, max, label step, tick, div, object, wrong answers)
    (300, 1000, 200, 100, 1, "a block of cheese", ["210 g", "400 g", "200 g", "300 kg"]),
    (700, 1000, 200, 100, 1, "a bunch of bananas", ["610 g", "800 g", "600 g"]),
    (900, 1000, 200, 100, 1, "a bag of apples", ["810 g", "1000 g", "800 g"]),
    (500, 1000, 200, 100, 1, "a tub of yoghurt", ["410 g", "600 g", "400 g", "500 kg"]),
    (800, 1000, 500, 100, 1, "a loaf of bread", ["503 g", "530 g", "700 g", "900 g"]),
    (400, 1000, 500, 100, 1, "a box of cereal", ["40 g", "4 g", "200 g", "500 g"]),
    (900, 1000, 500, 100, 1, "a bag of mandarins", ["504 g", "540 g", "1000 g", "800 g"]),
    (300, 1000, 500, 100, 1, "a bag of carrots", ["30 g", "3 g", "150 g", "500 g"]),
    (350, 500, 100, 50, 1, "an avocado and a mango", ["310 g", "400 g", "300 g"]),
    (150, 500, 100, 50, 1, "an orange", ["110 g", "200 g", "100 g", "150 kg"]),
    (7000, 10000, 2000, 1000, 1000, "a bag of dog food", ["6 kg", "8 kg", "7 g"]),
    (3000, 10000, 2000, 1000, 1000, "a pile of library books", ["2 kg", "4 kg", "3 g"]),
    (5000, 10000, 2000, 1000, 1000, "a pumpkin", ["4 kg", "6 kg", "5 g"]),
    (12000, 20000, 5000, 1000, 1000, "a suitcase", ["11 kg", "15 kg", "12 g"]),
    (17000, 20000, 5000, 1000, 1000, "a bag of potting mix", ["16 kg", "20 kg", "17 g"]),
]


def set_mass(rnd):
    its = []
    its.append(mcq("How many grams are in 1 kilogram?", "1000 g", ["100 g", "10 g", "1 g"],
                   "Kilo means 1000. So 1 kg = 1000 g.", rnd, want=("M", 1000)))
    for v, mx, lab, tick, div, obj, wrong in DIALS:
        q = fig(dial_svg(v, mx, lab, tick, div)) + "The scale shows the mass of %s. What is the mass?" % obj
        its.append(mcq(q, wlabel(v, div), wrong, dial_e(v, lab, tick, div), rnd, want=("M", v)))
    its.append(mcq(fig(dial_svg(600, 1000, 200, 100)) +
                   "The scale shows a bag of flour. How much more flour is needed to make 1 kg?",
                   "400 g", ["1600 g", "500 g", "600 g"],
                   "The needle is at 600 g. 1 kg = 1000 g. 1000 − 600 = 400 g more.", rnd, want=("M", 400)))
    its.append(mcq(fig(dial_svg(450, 500, 100, 50)) +
                   "The scale shows a bowl of cherries. The empty bowl has a mass of 100 g. "
                   "What is the mass of the cherries?",
                   "350 g", ["550 g", "450 g", "410 g"],
                   "Each mark is 50 g, so the needle is at 450 g. Take away the bowl: 450 − 100 = 350 g.",
                   rnd, want=("M", 350)))
    for va, vb, ans, wr, e in [
        (600, 900, "B, by 300 g", ["A, by 300 g", "B, by 3 g", "B, by 200 g"],
         "Each mark is 100 g. A shows 600 g and B shows 900 g. B is heavier. 900 − 600 = 300 g."),
        (800, 300, "A, by 500 g", ["B, by 500 g", "A, by 5 g", "A, by 1100 g"],
         "Each mark is 100 g. A shows 800 g and B shows 300 g. A is heavier. 800 − 300 = 500 g."),
    ]:
        its.append(mcq(fig(dial_pair_svg(va, vb, 1000, 200, 100)) +
                       "Which bag of fruit is heavier, and by how much?", ans, wr, e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Read scales: mass in g and kg", "items": its}


# ------------------------------------------------------------ set 4: capacity in jugs
def jug_e(v, lab, step, mx=0):
    sp = lab // step
    base = v - v % lab
    k = (v - base) // step
    if lab == mx:
        s = ("The jug goes from 0 at the bottom to %s mL. There are %d spaces, so each line is %s ÷ %d = %d mL. "
             % (c(lab), sp, c(lab), sp, step))
    else:
        s = ("The numbers go up by %s mL. There are %d spaces between numbers, so each line is %s ÷ %d = %d mL. "
             % (c(lab), sp, c(lab), sp, step))
    if k == 0:
        return s + "The water is right at the %s line: %s." % (c(base), mls(v))
    if base == 0:
        return s + "The water is %s up from the bottom: %s." % (marks(k, "line"), mls(v))
    return s + "The water is %s above %s: %s + %d = %s mL." % (marks(k, "line"), c(base), c(base), k * step, c(v))


JUGS = [  # (value mL, max, label step, line step, wrong answers)
    (300, 1000, 200, 100, ["210 mL", "400 mL", "200 mL", "300 L"]),
    (700, 1000, 200, 100, ["610 mL", "800 mL", "600 mL"]),
    (900, 1000, 200, 100, ["810 mL", "1000 mL", "800 mL"]),
    (250, 1000, 500, 250, ["100 mL", "500 mL", "750 mL"]),
    (750, 1000, 500, 250, ["501 mL", "600 mL", "1000 mL"]),
    (500, 1000, 1000, 250, ["2 mL", "250 mL", "750 mL"]),
    (400, 1000, 250, 50, ["280 mL", "253 mL", "450 mL", "550 mL"]),
    (650, 1000, 250, 50, ["530 mL", "503 mL", "600 mL", "800 mL"]),
    (550, 1000, 250, 50, ["510 mL", "501 mL", "600 mL", "750 mL"]),
    (850, 1000, 250, 50, ["770 mL", "752 mL", "900 mL"]),
    (250, 500, 100, 50, ["210 mL", "300 mL", "200 mL", "250 L"]),
    (350, 500, 100, 50, ["310 mL", "400 mL", "300 mL"]),
    (1300, 2000, 500, 100, ["1030 mL", "13 mL", "1150 mL", "1400 mL"]),
    (1700, 2000, 500, 100, ["1520 mL", "17 mL", "1600 mL", "1800 mL"]),
    (1250, 2000, 500, 250, ["1001 mL", "1500 mL", "1100 mL"]),
]


def set_capacity(rnd):
    its = []
    its.append(mcq("How many millilitres are in 1 litre?", "1000 mL", ["100 mL", "10 mL", "1 mL"],
                   "Milli means one thousandth. So 1 L = 1000 mL.", rnd, want=("C", 1000)))
    for v, mx, lab, step, wrong in JUGS:
        q = fig(jug_svg(v, mx, lab, step)) + "How much water is in the jug?"
        its.append(mcq(q, mls(v), wrong, jug_e(v, lab, step, mx), rnd, want=("C", v)))
    its.append(mcq(fig(jug_svg(400, 1000, 200, 100)) + "How much more water is needed to fill the jug to 1 L?",
                   "600 mL", ["1400 mL", "400 mL", "700 mL"],
                   "Each line is 100 mL, so the water is at 400 mL. 1 L = 1000 mL. 1000 − 400 = 600 mL more.",
                   rnd, want=("C", 600)))
    its.append(mcq(fig(jug_svg(800, 1000, 200, 100)) + "Noah pours 250 mL of water out of the jug. How much is left?",
                   "550 mL", ["650 mL", "1050 mL", "250 mL"],
                   "The water is at 800 mL. Water is poured out, so subtract: 800 − 250 = 550 mL.", rnd,
                   want=("C", 550)))
    its.append(mcq("How many 250 mL cups of water fill a 1 L jug?", "4", ["250", "3", "1000"],
                   "1 L = 1000 mL. Count by 250: 250, 500, 750, 1000. That is 4 cups.", rnd))
    its.append(mcq("Which tool is best to measure 200 mL of milk for a recipe?", "a measuring jug",
                   ["a ruler", "kitchen scales", "a tape measure"],
                   "Capacity is measured with a measuring jug or a measuring cup. Scales measure mass.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Read jugs: capacity in mL and L", "items": its}


# ------------------------------------------------------------ set 5: compare and word problems
def set_story(rnd):
    P = People(rnd)
    its = []

    def add(q, r, w, e, want=None):
        its.append(mcq(q, r, w, e, rnd, want=want))

    # compare (do not compare numbers without their units)
    for q, ch, ans, e in [
        ("Which is the heaviest?", ["900 g", "1 kg", "990 g", "99 g"], "1 kg",
         "Change them all to grams: 1 kg = 1000 g. 1000 g is more than 990 g and 900 g. "
         "Do not just compare the numbers 1 and 990."),
        ("Which is the longest?", ["190 cm", "2 m", "150 cm", "99 cm"], "2 m",
         "Change them all to centimetres: 2 m = 200 cm. 200 cm is more than 190 cm. "
         "Do not just compare the numbers 2 and 190."),
        ("Which holds the most?", ["950 mL", "800 mL", "1 L", "600 mL"], "1 L",
         "Change them all to millilitres: 1 L = 1000 mL. 1000 mL is more than 950 mL. "
         "Do not just compare the numbers 1 and 950."),
    ]:
        vals = [parse(x)[1] for x in ch]
        assert len(set(vals)) == 4 and parse(ans)[1] == max(vals)
        add(q, ans, [x for x in ch if x != ans], e)
    sts = ["1 kg > 900 g", "1 kg < 900 g", "1 kg = 100 g", "900 g > 1 kg"]
    assert [truth(s) for s in sts] == [True, False, False, False]
    add("Which is true?", sts[0], sts[1:],
        "1 kg = 1000 g. 1000 g is more than 900 g. Do not compare only the numbers 1 and 900.")
    sts = ["80 cm < 1 m < 120 cm", "1 m < 80 cm < 120 cm", "120 cm < 80 cm < 1 m", "80 cm < 120 cm < 1 m"]
    assert [truth(s) for s in sts] == [True, False, False, False]
    add("Which list goes from the shortest to the longest?", sts[0], sts[1:],
        "Change them to centimetres: 1 m = 100 cm. 80 < 100 < 120.")
    # word problems
    n, he, his = P.next()
    add("%s has a 600 mL water bottle. %s drinks 250 mL at recess. How much water is left?" % (n, cap(he)),
        "350 mL", ["850 mL", "450 mL", "250 mL"], "Drinking takes water away, so subtract: 600 − 250 = 350 mL.",
        ("C", 350))
    n, he, his = P.next()
    add("At the market, %s's watermelon has a mass of 6 kg. A rockmelon has a mass of 2 kg. "
        "How much heavier is the watermelon?" % n,
        "4 kg", ["8 kg", "4 g", "3 kg"], "How much heavier means find the difference: 6 − 2 = 4 kg.", ("M", 4000))
    n, he, his = P.next()
    add("%s's lunchbox has a mass of 400 g. %s drink bottle has a mass of 600 g. "
        "What is their total mass?" % (n, cap(his)),
        "1 kg", ["10 g", "200 g", "10 kg"],
        "Add: 400 + 600 = 1000 g. 1000 g = 1 kg. It is not 10 g: 4 hundreds + 6 hundreds = 10 hundreds.",
        ("M", 1000))
    n, he, his = P.next()
    add("%s's backpack has a mass of 5 kg. %s takes out 2 kg of library books. What is the mass of the backpack now?"
        % (n, cap(he)), "3 kg", ["7 kg", "3 g", "2 kg"],
        "Taking out means subtract: 5 − 2 = 3 kg.", ("M", 3000))
    add("The school canteen has 8 kg of sausages for the sausage sizzle. They cook 5 kg. How many kilograms are left?",
        "3 kg", ["13 kg", "3 g", "4 kg"], "Subtract what was cooked: 8 − 5 = 3 kg.", ("M", 3000))
    n, he, his = P.next()
    add("%s has 85 cm of ribbon. %s cuts off 30 cm for a card. How much ribbon is left?" % (n, cap(he)),
        "55 cm", ["115 cm", "65 cm", "55 m"], "Cutting off means subtract: 85 − 30 = 55 cm.", ("L", 550))
    add("A sunflower in the school garden was 35 cm tall. It grew 18 cm more. How tall is it now?",
        "53 cm", ["43 cm", "17 cm", "513 cm"],
        "Add: 35 + 18. 5 + 8 = 13, so regroup 10 ones as 1 ten. 35 + 18 = 53 cm.", ("L", 530))
    n, he, his = P.next()
    n2, he2, his2 = P.next()
    add("At the athletics carnival, %s jumps 185 cm. %s jumps 210 cm. How much further does %s jump?" % (n, n2, n2),
        "25 cm", ["35 cm", "395 cm", "125 cm"],
        "Count on from 185: 185 → 200 is 15 cm, 200 → 210 is 10 cm. 15 + 10 = 25 cm.", ("L", 250))
    n, he, his = P.next()
    add("%s is 128 cm tall. %s dad is 180 cm tall. How much taller is %s dad?" % (n, cap(his), his),
        "52 cm", ["62 cm", "308 cm", "48 cm"],
        "Find the difference: 180 − 128 = 52 cm. Check: 128 + 52 = 180.", ("L", 520))
    n, he, his = P.next()
    add("%s rides %s bike 3 km to the beach and 3 km back home. How far does %s ride altogether?" % (n, his, he),
        "6 km", ["6 m", "3 km", "9 km"], "There and back is 3 km + 3 km = 6 km.", ("L", 6000000))
    add("A jug holds 1 L of cordial. Four cups of 200 mL are poured for a picnic. How much cordial is left in the jug?",
        "200 mL", ["800 mL", "600 mL", "1200 mL"],
        "4 cups of 200 mL: 200 + 200 + 200 + 200 = 800 mL. 1 L = 1000 mL. 1000 − 800 = 200 mL left.", ("C", 200))
    n, he, his = P.next()
    add("%s has a 1 kg bag of flour. %s uses 350 g to bake Anzac biscuits. How much flour is left?" % (n, cap(he)),
        "650 g", ["750 g", "1350 g", "350 g"],
        "1 kg = 1000 g. Subtract: 1000 − 350 = 650 g. Check: 650 + 350 = 1000.", ("M", 650))
    n, he, his = P.next()
    add("%s has a 2 L bottle of orange juice. %s pours 500 mL into glasses for the family. "
        "How much juice is left in the bottle?" % (n, cap(he)),
        "1500 mL", ["2500 mL", "1500 L", "498 mL"],
        "2 L = 2000 mL. Subtract: 2000 − 500 = 1500 mL. Do not take 2 from 500: change to the same unit first.",
        ("C", 1500))
    add("A paddling pool holds 60 L of water. A bucket holds 10 L. How many full buckets fill the pool?",
        "6", ["50", "70", "600"], "Count by 10 L: 10, 20, 30, 40, 50, 60. That is 6 buckets. 60 ÷ 10 = 6.")
    add("A brown worm is 45 mm long. A pink worm is 6 cm long. Which worm is longer, and by how much?",
        "the pink worm, by 15 mm", ["the brown worm, by 39 mm", "the pink worm, by 39 mm",
                                    "the brown worm, by 15 mm"],
        "6 cm = 60 mm. 60 mm is more than 45 mm, so the pink worm is longer. 60 − 45 = 15 mm. "
        "Do not take 6 from 45: change to the same unit first.")
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
        "<p><b>Length</b> is how long something is. <b>Mass</b> is how heavy it is. "
        "<b>Capacity</b> is how much a container holds. Each one has its own units and its own tool.</p>" +
        table(["Measure", "Units", "Tool"], [
            ["Length", "millimetres (mm), centimetres (cm), metres (m), kilometres (km)", "ruler, tape measure"],
            ["Mass", "grams (g), kilograms (kg)", "scales"],
            ["Capacity", "millilitres (mL), litres (L)", "measuring jug, measuring cup"],
        ]) +
        "<p>Key facts: 1 m = 100 cm, 1 cm = 10 mm, 1 kg = 1000 g, 1 L = 1000 mL.</p>"
        "<h2>Choose a unit and estimate</h2>"
        "<p>Small things use small units. Big things use big units. Compare with something you know.</p>" +
        table(["Familiar item", "About"], [
            ["The width of your little finger", "1 cm"],
            ["A classroom door (height)", "2 m"],
            ["A paper clip", "1 g"],
            ["A bag of sugar", "1 kg"],
            ["A teaspoon", "5 mL"],
            ["A can of soft drink", "375 mL"],
            ["A carton of milk", "1 L or 2 L"],
        ]) +
        "<h2>Measure with a ruler</h2>"
        "<p>Line up one end of the object with <b>0</b>, not with 1 and not with the edge of the ruler. "
        "Read the number at the other end.</p>"
        "<figure class='sn-fig'>" + ruler_svg(0, 70, "pencil") +
        "<figcaption>The pencil starts at 0 and ends at 7. It is 7 cm long.</figcaption></figure>"
        "<p>If the object does not start at 0, take away the start from the end, or count the spaces.</p>"
        "<figure class='sn-fig'>" + ruler_svg(20, 90, "crayon") +
        "<figcaption>The crayon starts at 2 and ends at 9. 9 − 2 = 7, so it is 7 cm long, not 9 cm.</figcaption></figure>"
        "<h2>Read a scale or a jug</h2>"
        "<p>Not every mark has a number. First work out <b>what one mark is worth</b>: "
        "the jump between two numbers ÷ the number of spaces. Then count on from the number before.</p>"
        "<figure class='sn-fig'>" + dial_svg(700, 1000, 200, 100) +
        "<figcaption>The numbers go up by 200 g. There are 2 spaces, so each mark is 100 g. "
        "The needle is 1 mark past 600: 700 g.</figcaption></figure>"
        "<figure class='sn-fig'>" + jug_svg(750, 1000, 500, 250) +
        "<figcaption>The numbers go up by 500 mL. There are 2 spaces, so each line is 250 mL. "
        "The water is 1 line above 500: 750 mL.</figcaption></figure>"
        "<h2>Compare with the same unit</h2>"
        "<p>To compare, change both measures to the <b>same unit</b> first. Never compare just the numbers.</p>" +
        ex("Which is heavier?", "1 kg or 900 g?",
           "1 kg = 1000 g. 1000 g is more than 900 g.", "1 kg is heavier") +
        ex("How much is left?", "Ava has a 600 mL water bottle and drinks 250 mL.",
           "Drinking takes water away, so subtract: 600 − 250 = 350.", "350 mL") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Choosing km for a pencil, or kg for a length", "Pick a length unit that fits the size: mm, cm, m or km"],
            ["Starting at 1 or at the edge of the ruler", "Start at 0, or take away the start from the end"],
            ["Counting every mark on a scale as 1 or 10", "Work out what one mark is worth first"],
            ["Thinking 900 g is more than 1 kg", "Change to the same unit: 1 kg = 1000 g"],
            ["Writing the answer without a unit", "Always write the unit: 7 cm, 350 mL, 3 kg"],
        ])
    )


FAQ = [
    {"q": "What measurement do Year 3 students learn in the Australian Curriculum?",
     "a": "Year 3 students choose suitable metric units, estimate, and measure and compare length (mm, cm, m, km), "
          "mass (g, kg) and capacity (mL, L) using rulers, scales and jugs with labelled markings."},
    {"q": "How do you read a scale when not every mark has a number?",
     "a": "Count the spaces between two labelled numbers and divide the jump by the spaces to find what one mark is "
          "worth. Then count on from the number before the needle or water line."},
    {"q": "Is measurement part of the Year 3 NAPLAN numeracy test?",
     "a": "Yes. NAPLAN numeracy includes measurement, so Year 3 students may be asked to read rulers, scales and "
          "jugs, choose units and compare measures."},
    {"q": "What are good benchmarks for estimating mass and capacity?",
     "a": "A paper clip is about 1 g and a bag of sugar is about 1 kg. A teaspoon holds about 5 mL and a carton of "
          "milk holds 1 L or 2 L."},
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
    rnd = random.Random(3808)
    sets = [set_units(rnd), set_length(rnd), set_mass(rnd), set_capacity(rnd), set_story(rnd)]
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
        "country": "au", "subject": "maths", "grade": "year-3", "slug": "measuring-length-mass-and-capacity", "sort": 8,
        "updated": UPDATED, "pdf_url": "",
        "title": "Measuring Length, Mass and Capacity",
        "seo_title": "Year 3 Measuring Worksheets: Length, Mass and Capacity (Free, with Answer Key)",
        "short_title": "Measuring length, mass and capacity",
        "domain": "Measurement",
        "standard_code": "AC9M3M02",
        "standard_url": "https://v9.australiancurriculum.edu.au/f-10-curriculum/learning-areas/mathematics",
        "standard_text": "Measure and compare objects using familiar metric units of length, mass and capacity, "
                         "and instruments with labelled markings",
        "meta_desc": "Free Year 3 maths worksheets on measuring: choose metric units and estimate, measure length "
                     "with a ruler, read scales in g and kg and jugs in mL and L, and compare measures in word "
                     "problems. 100 questions with an answer key, matched to the Australian Curriculum and "
                     "useful for NAPLAN.",
        "key_big": "Choose a unit that fits, start at 0, and find what one mark is worth.",
        "key_sub": "1 m = 100 cm, 1 kg = 1000 g and 1 L = 1000 mL. Compare measures in the same unit: "
                   "1 kg is heavier than 900 g.",
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
    mark_large(u, "two weighing scales")
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
