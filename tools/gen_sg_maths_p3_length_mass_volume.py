# -*- coding: utf-8 -*-
"""
Singapore Primary 3 Maths: Length, Mass and Volume (MOE 2021 Primary Mathematics Syllabus, Standard:
Primary 3 Measurement - measuring length in km, volume in ml; compound units; converting between km and m,
m and cm, kg and g, ℓ and ml)
  python3 tools/gen_sg_maths_p3_length_mass_volume.py
Primary 3: numbers to 10 000, short sentences for 8-9 year olds, pictures in many questions, bar models in
word problems. Singapore style: metre, litre (ℓ), ml, compound units ("2 m 35 cm"), 4-digit numbers without
a separator. Scale, beaker, ruler and tape figures are adapted from gen_cabc_math_g3_measuring.py; bar models
from gen_sg_maths_p4_add_sub_decimals.py. HTML attributes use single quotes (no backslashes in the JSON).
Every needle, liquid level and length is drawn exactly at its value, and every answer is parsed back and checked
against a value worked out separately in whole numbers of the smallest unit (cm, g, ml).
Wrong answers come from real mistakes: 3 kg 40 g = 340 g, 1 km = 100 m, adding m and cm as one number,
forgetting to rename 1 kg as 1000 g, taking the smaller digit from the bigger one, counting every mark as 10.
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "sg", "maths", "primary-3")
UPDATED = "2026-11-03"
GREEN = "#006633"
RED = "#c0392b"
INK = "#2b2b2b"
WOOD = "#f6e7b8"
TAPE = "#fff3a6"
WATER = "#9fd3f2"
WATER_LINE = "#2a7fb8"
JUICE = "#e8b23a"
JUICE_LINE = "#a8741a"
HEADFILL = "#cfe6d6"
PARTFILL = "#fde3c8"
ORANGE = "#b35900"
FONT = "Arial, Helvetica, sans-serif"
NB = " "
GIRLS = ["Siti", "Nurul", "Farah", "Mei Ling", "Hui Min", "Xin Yi", "Priya", "Devi", "Kavya", "Chloe", "Sarah"]
BOYS = ["Ali", "Ahmad", "Hafiz", "Wei Ming", "Jun Jie", "Zhi Hao", "Raju", "Kumar", "Arjun", "Ethan", "Ryan"]


# ------------------------------------------------------------ units and checking
# base units: length in cm, mass in g, volume in ml
UNIT = {"cm": ("L", 1), "m": ("L", 100), "km": ("L", 100000),
        "g": ("M", 1), "kg": ("M", 1000), "ml": ("V", 1), "ℓ": ("V", 1000)}
TOK = re.compile(r"([\d" + NB + r"]+)\s*(" + "|".join(sorted(UNIT, key=len, reverse=True)) + r")(?![a-zA-Z])")
PAIR = {"L": ("m", "cm", 100), "K": ("km", "m", 1000), "M": ("kg", "g", 1000), "V": ("ℓ", "ml", 1000)}


def parse(s):
    """'2 m 35 cm' -> ('L', 235). None if the string is not a plain measurement."""
    s = s.strip()
    pos, fam, tot = 0, None, 0
    for mt in TOK.finditer(s):
        if s[pos:mt.start()].strip():
            return None
        fu, sz = UNIT[mt.group(2)]
        if fam and fu != fam:
            return None
        fam = fu
        tot += int(mt.group(1).replace(NB, "")) * sz
        pos = mt.end()
    if fam is None or s[pos:].strip():
        return None
    return fam, tot


def c(n):
    """MOE style: 4 digits plain (4536), 5 or more digits grouped with a no-break space."""
    if n < 10000:
        return str(n)
    return "{:,}".format(n).replace(",", NB)


def cu(v, kind):
    """Compound form. kind L: cm -> 'm cm'; K: m -> 'km m'; M: g -> 'kg g'; V: ml -> 'ℓ ml'."""
    big, small, f = PAIR[kind]
    a, b = divmod(v, f)
    if a and b:
        return "%s %s %s %s" % (c(a), big, c(b), small)
    if a:
        return "%s %s" % (c(a), big)
    return "%s %s" % (c(b), small)


def sm(v, kind):
    """In the smaller unit only: '235 cm'."""
    return "%s %s" % (c(v), PAIR[kind][1])


def fam_of(kind):
    return "L" if kind in "LK" else kind


def base(v, kind):
    """Value in the base unit of the family (km m values are in m; base is cm)."""
    return v * 100 if kind == "K" else v


def mcq(q, correct, cands, e, want=None):
    """4 choices: correct + the first 3 unique distractors. Measurement choices must differ in value.
    want = (family, value in cm / g / ml) checks the correct answer."""
    correct = str(correct)
    if want is not None:
        assert parse(correct) == want, (q, correct, want, parse(correct))
    seen = {correct}
    pc = parse(correct)
    vals = {pc} if pc else set()
    pick = []
    for x in cands:
        x = str(x)
        lead = x.split(" ")[0]
        if x in seen or not x or lead.startswith("−") or lead == "0":
            continue
        pv = parse(x)
        if pv:
            if pv in vals or pv[1] <= 0:
                continue
            vals.add(pv)
        seen.add(x)
        pick.append(x)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    return {"q": q, "c": [correct] + pick, "a": 0, "e": e}


class People:
    def __init__(self, rnd):
        self.pool = [(x, "she", "her") for x in GIRLS] + [(x, "he", "his") for x in BOYS]
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


def tw(s, fs):
    """Rough text width of bold Arial."""
    w = 0
    for ch in s:
        if ch in ".,: " + NB:
            w += 0.3
        elif ch in "ℓl1i":
            w += 0.45
        elif ch in "m×÷?$":
            w += 0.85
        else:
            w += 0.6
    return w * fs


def marks(k, w="mark"):
    return "%d %s%s" % (k, w, "" if k == 1 else "s")


# ------------------------------------------------------------ figure: centimetre ruler
def ruler_svg(s_cm, e_cm, ncm=12):
    """Centimetre ruler from 0 to ncm with an eraser lying exactly from s_cm to e_cm."""
    PX = 34.0
    X0, YR, RH = 18, 40, 50
    W = int(X0 * 2 + PX * ncm + 26)
    H = YR + RH + 4
    X = lambda v: X0 + PX * v
    a, b = X(s_cm), X(e_cm)
    o = ["<rect x='%.1f' y='12' width='%.1f' height='20' rx='4' fill='#f7b7c5' stroke='%s' stroke-width='1.5'/>"
         % (a, b - a, INK),
         "<rect x='%.1f' y='12' width='%.1f' height='20' fill='#5dade2' stroke='%s' stroke-width='1.5'/>"
         % (a + (b - a) * 0.45, (b - a) * 0.4, INK)]
    for x in (a, b):
        o.append("<line x1='%.1f' y1='32' x2='%.1f' y2='%d' stroke='%s' stroke-width='1.2' stroke-dasharray='3 2'/>"
                 % (x, x, YR, RED))
    o.append("<rect x='4' y='%d' width='%d' height='%d' rx='3' fill='%s' stroke='%s' stroke-width='2'/>"
             % (YR, W - 8, RH, WOOD, INK))
    small, big = [], []
    for i in range(ncm * 2 + 1):
        x = X(i / 2.0)
        (big if i % 2 == 0 else small).append("M%.1f %dL%.1f %d" % (x, YR, x, YR + (18 if i % 2 == 0 else 10)))
    o.append("<path d='%s' stroke='%s' stroke-width='1.2'/>" % ("".join(small), INK))
    o.append("<path d='%s' stroke='%s' stroke-width='2'/>" % ("".join(big), INK))
    for cc in range(ncm + 1):
        o.append(text(X(cc), YR + 38, str(cc), 15))
    o.append(text(X(ncm) + 12, YR + 38, "cm", 15, anchor="start", bold=False))
    return svg_wrap(W, H, "".join(o), "ruler with an eraser from %d cm to %d cm" % (s_cm, e_cm))


# ------------------------------------------------------------ figure: measuring tape in m and cm
TAPE_OBJ = {"rope": "#8e5b2a", "ribbon": RED, "plank": "#c79a5b"}


def tape_svg(v_cm, max_m, obj):
    """Tape from 0 to max_m metres, a mark every 10 cm (longer at 50 cm). The object lies from 0 to v_cm."""
    PX = {2: 22.0, 3: 15.0, 4: 11.5}[max_m]          # px per 10 cm
    X0, YT, TH = 20, 44, 46
    X = lambda cm: X0 + PX * cm / 10.0
    W = int(X(max_m * 100) + 44)
    H = YT + TH + 4
    o = []
    col = TAPE_OBJ[obj]
    if obj == "rope":
        o.append("<line x1='%.1f' y1='24' x2='%.1f' y2='24' stroke='%s' stroke-width='7' stroke-linecap='butt'/>"
                 % (X(0), X(v_cm), col))
    elif obj == "ribbon":
        o.append("<rect x='%.1f' y='17' width='%.1f' height='14' fill='%s' stroke='%s' stroke-width='1.5'/>"
                 % (X(0), X(v_cm) - X(0), col, INK))
    else:
        o.append("<rect x='%.1f' y='12' width='%.1f' height='24' fill='%s' stroke='%s' stroke-width='1.5'/>"
                 % (X(0), X(v_cm) - X(0), col, INK))
    for x in (X(0), X(v_cm)):
        o.append("<line x1='%.1f' y1='34' x2='%.1f' y2='%d' stroke='%s' stroke-width='1.4' stroke-dasharray='3 2'/>"
                 % (x, x, YT, RED))
    o.append("<rect x='%d' y='%d' width='%.1f' height='%d' rx='3' fill='%s' stroke='%s' stroke-width='2'/>"
             % (X0 - 12, YT, X(max_m * 100) - X0 + 34, TH, TAPE, INK))
    small, mid, big = [], [], []
    for i in range(max_m * 10 + 1):
        x = X(i * 10)
        if i % 10 == 0:
            big.append("M%.1f %dL%.1f %d" % (x, YT, x, YT + 20))
        elif i % 5 == 0:
            mid.append("M%.1f %dL%.1f %d" % (x, YT, x, YT + 14))
        else:
            small.append("M%.1f %dL%.1f %d" % (x, YT, x, YT + 9))
    o.append("<path d='%s' stroke='%s' stroke-width='1.3'/>" % ("".join(small), INK))
    o.append("<path d='%s' stroke='%s' stroke-width='1.8'/>" % ("".join(mid), INK))
    o.append("<path d='%s' stroke='%s' stroke-width='2.4'/>" % ("".join(big), INK))
    for m in range(max_m + 1):
        o.append(text(X(m * 100), YT + 38, "0" if m == 0 else "%d m" % m, 15))
    return svg_wrap(W, H, "".join(o), "measuring tape with a %s from 0 to %d cm" % (obj, v_cm))


# ------------------------------------------------------------ figures: scale and beaker
def dial_svg(v, mx, lab, tick, size=200):
    """Round scale in g: 0 at the lower left, mx at the lower right (270 degrees). Needle exactly at v.
    Numbers in kg when lab is a whole number of kg, else in g."""
    in_kg = lab % 1000 == 0
    cx = cy = size / 2.0
    R = cx - 6

    def pt(val, r):
        a = math.radians(-135 + 270.0 * val / mx)
        return cx + r * math.sin(a), cy - r * math.cos(a)
    s = ["<circle cx='%.1f' cy='%.1f' r='%.1f' fill='#fff' stroke='%s' stroke-width='6'/>" % (cx, cy, R, GREEN)]
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
             % (cx, cy, nx, ny, RED))
    s.append("<g font-size='%d' font-weight='700' fill='%s' text-anchor='middle' stroke='#fff' stroke-width='4' "
             "paint-order='stroke'>" % (17 if in_kg or mx < 1000 else 15, INK))
    for val in range(0, mx + 1, lab):
        x, y = pt(val, R - 36)
        s.append("<text x='%.1f' y='%.1f'>%s</text>" % (x, y + 6, str(val // 1000 if in_kg else val)))
    s.append("</g>")
    s.append("<circle cx='%.1f' cy='%.1f' r='7' fill='%s'/>" % (cx, cy, RED))
    s.append(text(cx, cy + 62, "kg" if in_kg else "g", 22, col=GREEN))
    return svg_wrap(size, size, "".join(s), "scale with the needle at %d g" % v)


def beaker_svg(v, mx, lab, step, liquid="water"):
    """Measuring beaker in ml: a line every `step`, a number every `lab` (in ℓ when lab is whole litres).
    Liquid exactly at v."""
    in_l = lab % 1000 == 0
    x0, x1 = 78, 156
    yb, yt = 196, 30
    fill, line = (JUICE, JUICE_LINE) if liquid == "orange juice" else (WATER, WATER_LINE)

    def Y(val):
        return yb - (yb - yt) * float(val) / mx
    s = []
    if v > 0:
        s.append("<rect x='%d' y='%.1f' width='%d' height='%.1f' fill='%s'/>" % (x0, Y(v), x1 - x0, yb - Y(v), fill))
        s.append("<line x1='%d' y1='%.1f' x2='%d' y2='%.1f' stroke='%s' stroke-width='2.5'/>" % (x0, Y(v), x1, Y(v), line))
    s.append("<path d='M%d %d L%d %d L%d %d Q%d %d %d %d L%d %d Q%d %d %d %d L%d %d L%d %d' fill='none' stroke='%s' "
             "stroke-width='4' stroke-linejoin='round'/>"
             % (x0 - 9, 12, x0, 20, x0, yb - 4, x0, yb, x0 + 6, yb, x1 - 6, yb, x1, yb, x1, yb - 4, x1, 20,
                x1 + 2, 16, INK))
    s.append("<g font-size='15' font-weight='700' fill='%s' text-anchor='end'>" % INK)
    for val in range(step, mx + 1, step):
        major = val % lab == 0
        s.append("<line x1='%d' y1='%.1f' x2='%d' y2='%.1f' stroke='%s' stroke-width='%s'/>"
                 % (x0, Y(val), x0 + (24 if major else 13), Y(val), INK, "2.6" if major else "1.6"))
        if major:
            s.append("<text x='%d' y='%.1f'>%s</text>" % (x0 - 7, Y(val) + 5,
                                                          ("%d ℓ" % (val // 1000)) if in_l else str(val)))
    s.append("</g>")
    if not in_l:
        s.append(text(x0 - 7, 214, "ml", 15, anchor="end", col=GREEN))
    return svg_wrap(176, 220, "".join(s), "measuring beaker with %s at %d ml" % (liquid, v))


# ------------------------------------------------------------ figures: bar models
def brace(x1, x2, y, up, lab, col=INK):
    d = 7 if up else -7
    o = ["<path d='M%.1f %.1f L%.1f %.1f L%.1f %.1f L%.1f %.1f' fill='none' stroke='%s' stroke-width='2'/>"
         % (x1, y + d, x1, y, x2, y, x2, y + d, col)]
    o.append(text((x1 + x2) / 2.0, y - 7 if up else y + 20, lab, 16, col=col))
    return "".join(o)


def bar_parts(parts, total_lab, BW=440):
    """One bar split into parts drawn to scale. parts = [(value, label inside)]. Bracket below with total_lab."""
    X0, TOP, BH = 10, 8, 40
    tot = float(sum(v for v, _ in parts))
    W = X0 * 2 + BW
    H = TOP + BH + 36
    o, x = [], float(X0)
    fills = [HEADFILL, PARTFILL, "#fff"]
    for i, (v, lab) in enumerate(parts):
        w = v / tot * BW
        assert tw(lab, 16) <= w - 6, (lab, w)
        o.append("<rect x='%.1f' y='%d' width='%.1f' height='%d' fill='%s' stroke='%s' stroke-width='2'/>"
                 % (x, TOP, w, BH, fills[i % 3] if len(set(p[0] for p in parts)) > 1 else HEADFILL, GREEN))
        o.append(text(x + w / 2.0, TOP + BH / 2.0 + 6, lab, 16, col=RED if lab == "?" else INK))
        x += w
    o.append(brace(X0, X0 + BW, TOP + BH + 10, False, total_lab, col=RED if total_lab == "?" else INK))
    if len(set(v for v, _ in parts)) == 1:
        lab = "bar model: %d equal parts, whole %s" % (len(parts), total_lab)
    else:
        lab = "bar model: parts %s, whole %s" % (", ".join(l for _, l in parts), total_lab)
    return svg_wrap(W, H, "".join(o), lab)


def bar_compare(rows, diff_lab, BW=380):
    """Comparison model. rows = [(name, value, label inside)], the first bar is the longer one.
    The shorter bar has a dashed part up to the longer one, with diff_lab inside it."""
    (n1, v1, l1), (n2, v2, l2) = rows
    assert v1 > v2
    LW = int(max(tw(n1, 16), tw(n2, 16))) + 16
    X0, TOP, BH, GAP = 6, 8, 38, 16
    x0 = X0 + LW
    W = x0 + BW + 10
    H = TOP + 2 * BH + GAP + 8
    w2 = float(v2) / v1 * BW
    o = []
    for i, (nm, w, lab, fl) in enumerate([(n1, BW, l1, HEADFILL), (n2, w2, l2, PARTFILL)]):
        y = TOP + i * (BH + GAP)
        assert tw(lab, 16) <= w - 6, (lab, w)
        o.append(text(x0 - 10, y + BH / 2.0 + 6, nm, 16, anchor="end"))
        o.append("<rect x='%d' y='%d' width='%.1f' height='%d' fill='%s' stroke='%s' stroke-width='2'/>"
                 % (x0, y, w, BH, fl, GREEN))
        o.append(text(x0 + w / 2.0, y + BH / 2.0 + 6, lab, 16, col=RED if lab == "?" else INK))
    y = TOP + BH + GAP
    dw = BW - w2
    assert tw(diff_lab, 16) <= dw - 6, (diff_lab, dw)
    o.append("<rect x='%.1f' y='%d' width='%.1f' height='%d' fill='none' stroke='%s' stroke-width='2' "
             "stroke-dasharray='6 4'/>" % (x0 + w2, y, dw, BH, ORANGE))
    o.append(text(x0 + w2 + dw / 2.0, y + BH / 2.0 + 6, diff_lab, 16, col=RED if diff_lab == "?" else ORANGE))
    lab = "bar model comparing %s (%s) and %s (%s), difference %s" % (n1, l1, n2, l2, diff_lab)
    return svg_wrap(int(W), H, "".join(o), lab)


# ------------------------------------------------------------ set 1: choose the unit
def set_units(P):
    its = []
    for obj, ans, wr, e in [
        ("the length of an eraser", "cm", ["m", "km", "kg"],
         "An eraser is short. It fits on a 30 cm ruler, so use centimetres. Kilograms measure mass."),
        ("the height of an HDB block of flats", "m", ["cm", "km", "ℓ"],
         "An HDB block is very tall, but you can see the top. Use metres. Litres measure volume."),
        ("the distance from Changi Airport to the Singapore Zoo", "km", ["m", "cm", "kg"],
         "That is a long trip by car or MRT, so use kilometres."),
        ("the length of a swimming pool", "m", ["km", "cm", "g"],
         "You can swim from one end of a pool to the other, so use metres."),
        ("the mass of a mandarin orange", "g", ["kg", "ml", "cm"],
         "A mandarin orange is light. It fits in your hand, so use grams."),
        ("the mass of a bag of rice", "kg", ["g", "ℓ", "km"],
         "A bag of rice is heavy to carry, so use kilograms."),
        ("the mass of a pencil", "g", ["kg", "cm", "ml"],
         "A pencil is very light, so use grams. Centimetres measure length."),
        ("the volume of medicine in a teaspoon", "ml", ["ℓ", "g", "cm"],
         "A teaspoon holds only a little, so use millilitres. Grams measure mass."),
        ("the volume of water in a bucket", "ℓ", ["ml", "kg", "m"],
         "A bucket holds a lot of water, so use litres."),
        ("the volume of juice in a packet drink", "ml", ["ℓ", "kg", "m"],
         "A packet drink from the canteen holds a small amount, so use millilitres."),
    ]:
        its.append(mcq("Which unit is best to measure %s?" % obj, ans, wr, e))
    its.append(mcq("1 km = ? m", "1000 m", ["100 m", "10 m", "10" + NB + "000 m"],
                   "Kilo means 1000. So 1 km = 1000 m. 1 km is not 100 m.", ("L", 100000)))
    its.append(mcq("1 m = ? cm", "100 cm", ["1000 cm", "10 cm", "50 cm"],
                   "A metre rule has 100 centimetres marked on it. So 1 m = 100 cm.", ("L", 100)))
    its.append(mcq("1 kg = ? g", "1000 g", ["100 g", "10 g", "500 g"],
                   "Kilo means 1000. So 1 kg = 1000 g.", ("M", 1000)))
    its.append(mcq("1 ℓ = ? ml", "1000 ml", ["100 ml", "10 ml", "500 ml"],
                   "1000 millilitres fill 1 litre: 1 ℓ = 1000 ml.", ("V", 1000)))
    for q, ans, wr, e, want in [
        ("A ruler is about ? long.", "30 cm", ["30 m", "3 cm", "30 km"],
         "A ruler fits in your school bag. It is about 30 cm long. 30 m is longer than a classroom.", ("L", 30)),
        ("A bottle of water holds about ?", "500 ml", ["500 ℓ", "5 ml", "50 ℓ"],
         "A water bottle is small, so it holds about 500 ml. 500 ℓ would fill a big tank.", ("V", 500)),
        ("A Primary 3 pupil has a mass of about ?", "28 kg", ["28 g", "280 kg", "2 kg"],
         "Most P3 pupils have a mass between 20 kg and 35 kg. 28 g is the mass of a few coins.", ("M", 28000)),
        ("You can walk about ? in 15 minutes.", "1 km", ["1 m", "10 m", "100 km"],
         "A 15-minute walk covers about 1 km. You walk 1 m in one big step.", ("L", 100000)),
    ]:
        its.append(mcq("Choose the best estimate. " + q, ans, wr, e, want))
    its.append(mcq("Which is longer: 1 km or 900 m?", "1 km", ["900 m", "They are the same.", "You cannot tell."],
                   "1 km = 1000 m. 1000 m is longer than 900 m, so 1 km is longer, even though 1 looks small."))
    its.append(mcq("Which holds more: a 1 ℓ carton of milk or a 950 ml bottle of juice?", "the 1 ℓ carton",
                   ["the 950 ml bottle", "They hold the same.", "You cannot tell."],
                   "1 ℓ = 1000 ml. 1000 ml is more than 950 ml, so the carton holds more. "
                   "Change to the same unit before you compare."))
    assert len(its) == 20, len(its)
    return {"title": "Choose the unit: km, m, cm, kg, g, ℓ and ml", "items": its}


# ------------------------------------------------------------ set 2: read scales, beakers and tapes
def read_e(v, lab, tick, kind, what):
    """Explanation for a scale or beaker reading. v, lab, tick in g or ml."""
    sp = lab // tick
    b = v - v % lab
    k = (v - b) // tick
    w = "mark" if what == "needle" else "line"
    s = ("The numbers go up by %s. There are %d spaces between two numbers, so each %s is %s ÷ %d = %s. "
         % (cu(lab, kind), sp, w, sm(lab, kind), sp, sm(tick, kind)))
    if what == "needle":
        if b == 0:
            return s + "The needle is %s past 0: %s." % (marks(k), cu(v, kind))
        return s + "The needle is %s past %s: %s + %s = %s." % (marks(k), cu(b, kind), cu(b, kind),
                                                                  sm(k * tick, kind), cu(v, kind))
    if b == 0:
        return s + "The top of the %s is %s up from the bottom: %s." % (what, marks(k, "line"), cu(v, kind))
    return s + "The top of the %s is %s above %s: %s + %s = %s." % (
        what, marks(k, "line"), cu(b, kind), cu(b, kind), sm(k * tick, kind), cu(v, kind))


def read_wrongs(v, lab, tick, kind, i):
    """Real mistakes: every mark counted as 10, one mark off, the next number, a digit slip in compound units."""
    b = v - v % lab
    k = (v - b) // tick
    f = PAIR[kind][2]
    w = [cu(b + 10 * k, kind), cu(v + tick, kind), cu(v - tick, kind), cu(b + lab, kind)]
    if v >= f and v % f:
        big, small, _ = PAIR[kind]
        slip = "%d %s %d %s" % (v // f, big, (v % f) // 100, small)    # 1 kg 400 g written as 1 kg 4 g
        w.insert(0 if i % 2 == 0 else 2, slip)
    else:
        w.insert(1 if i % 2 == 0 else 3, "%d %s" % (v, PAIR[kind][0]))   # 350 g written as 350 kg
    return w


DIALS = [  # (value g, max, label step, tick, object)
    (350, 500, 100, 50, "a packet of biscuits"),
    (850, 1000, 200, 50, "a bag of onions"),
    (1400, 3000, 1000, 100, "a durian"),
    (2700, 3000, 1000, 100, "a bag of potatoes"),
    (600, 2000, 1000, 100, "a papaya"),
    (1900, 2000, 1000, 100, "a bag of mangoes"),
    (3600, 5000, 1000, 200, "a watermelon"),
    (4200, 5000, 1000, 200, "a box of storybooks"),
]
BEAKERS = [  # (value ml, max, label step, line step, liquid)
    (300, 1000, 200, 100, "water"),
    (450, 500, 100, 50, "orange juice"),
    (900, 1000, 500, 100, "water"),
    (1400, 2000, 1000, 200, "water"),
    (600, 2000, 1000, 200, "orange juice"),
    (1800, 2000, 1000, 200, "water"),
    (1250, 3000, 1000, 250, "water"),
    (2750, 3000, 1000, 250, "orange juice"),
]


def set_read(P):
    its = []
    for i, (v, mx, lab, tick, obj) in enumerate(DIALS):
        q = fig(dial_svg(v, mx, lab, tick)) + "The scale shows the mass of %s. What is the mass?" % obj
        its.append(mcq(q, cu(v, "M"), read_wrongs(v, lab, tick, "M", i), read_e(v, lab, tick, "M", "needle"),
                       ("M", v)))
    for i, (v, mx, lab, step, liq) in enumerate(BEAKERS):
        q = fig(beaker_svg(v, mx, lab, step, liq)) + "How much %s is in the beaker?" % liq
        its.append(mcq(q, cu(v, "V"), read_wrongs(v, lab, step, "V", i + 1), read_e(v, lab, step, "V", liq),
                       ("V", v)))
    s_cm, e_cm = 3, 10
    its.append(mcq(fig(ruler_svg(s_cm, e_cm)) + "How long is the eraser?", "7 cm", ["10 cm", "8 cm", "13 cm"],
                   "The eraser starts at 3, not at 0. It ends at 10. 10 − 3 = 7, so it is 7 cm long.", ("L", 7)))
    for v, mx, obj in [(170, 2, "ribbon"), (240, 3, "rope"), (320, 4, "plank")]:
        m, r = divmod(v, 100)
        e = ("From 0 to 1 m there are 10 spaces, so each mark is 100 cm ÷ 10 = 10 cm. The %s ends %s after %d m: "
             "%d m + %d cm = %s." % (obj, marks(r // 10), m, m, r, cu(v, "L")))
        its.append(mcq(fig(tape_svg(v, mx, obj)) + "How long is the %s?" % obj, cu(v, "L"),
                       ["%d m %d cm" % (m, r // 10), "%d m %d cm" % (m, r + 10), "%d m" % v, "%d m" % (m + 1)], e,
                       ("L", v)))
    assert len(its) == 20, len(its)
    return {"title": "Read scales, beakers and tapes", "items": its}


# ------------------------------------------------------------ set 3: compound units to the smaller unit
def to_small_e(a, b, kind):
    big, small, f = PAIR[kind]
    if a == 1:
        return "1 %s = %d %s. Then %s + %s = %s." % (big, f, small, sm(f, kind), sm(b, kind), sm(f + b, kind))
    return "1 %s = %d %s, so %d %s = %s. Then %s + %s = %s." % (
        big, f, small, a, big, sm(a * f, kind), sm(a * f, kind), sm(b, kind), sm(a * f + b, kind))


def set_to_small(P):
    its = []
    plan = [  # (a, b, kind, wrong values in the small unit)
        (3, 0, "L", [30, 3000, 3]),
        (2, 35, "L", [37, 2035, 2350]),
        (6, 70, "L", [76, 607, 6070]),
        (1, 600, "M", [160, 700, 601]),
        (2, 750, "M", [752, 950, 2075]),
        (1, 250, "V", [125, 350, 251]),
        (3, 500, "V", [350, 3005, 503]),
        (1, 200, "K", [300, 1020, 120]),
        (3, 450, "K", [453, 345, 750]),
        (4, 8, "L", [48, 480, 4008]),
        (3, 40, "M", [340, 3400, 43]),
        (2, 80, "V", [280, 2800, 82]),
        (5, 60, "K", [560, 5600, 65]),
        (4, 5, "M", [45, 405, 4500]),
        (2, 5, "K", [25, 205, 2500]),
        (5, 5, "V", [55, 505, 5500]),
    ]
    for a, b, kind, wr in plan:
        big, small, f = PAIR[kind]
        q = ("%d %s = ? %s" % (a, big, small)) if b == 0 else ("%d %s %d %s = ? %s" % (a, big, b, small, small))
        if b == 0:
            e = "1 %s = %d %s, so %d %s = %d × %d = %s." % (big, f, small, a, big, a, f, sm(a * f, kind))
        else:
            e = to_small_e(a, b, kind)
            if b < 100 and f == 1000:
                e += " Keep the zeros: %d %s %d %s is %s, not %s." % (a, big, b, small, sm(a * f + b, kind),
                                                                     sm(int("%d%d" % (a, b)), kind))
            elif b < 10:
                e += " Keep the zero: %d %s %d %s is %s, not %s." % (a, big, b, small, sm(a * f + b, kind),
                                                                    sm(int("%d%d" % (a, b)), kind))
            elif kind == "K" and a == 1:
                e += " 1 km is 1000 m, not 100 m."
        its.append(mcq(q, sm(a * f + b, kind), [sm(x, kind) for x in wr], e, (fam_of(kind), base(a * f + b, kind))))
    # mistakes and comparisons
    n, he, his = P.next()
    its.insert(12, mcq("%s says 2 kg 60 g = 260 g. Is %s right? What is 2 kg 60 g in grams?" % (n, he),
                       "2060 g", ["260 g", "2600 g", "62 g"],
                       "%s is not right. 2 kg = 2000 g, not 200 g. 2000 g + 60 g = 2060 g." % n, ("M", 2060)))
    its.insert(13, mcq("Which is the same as 2 m 5 cm?", "205 cm", ["25 cm", "250 cm", "2005 cm"],
                       "2 m = 200 cm. 200 cm + 5 cm = 205 cm. 250 cm is 2 m 50 cm.", ("L", 205)))
    its.insert(3, mcq("6 km = ? m", "6000 m", ["600 m", "60 m", "6100 m"],
                      "1 km = 1000 m, so 6 km = 6 × 1000 = 6000 m.", ("L", 600000)))
    its.append(mcq("Which is heavier: 2 kg 90 g or 2900 g?", "2900 g",
                   ["2 kg 90 g", "They are the same.", "You cannot tell."],
                   "Change to grams: 2 kg 90 g = 2000 g + 90 g = 2090 g. 2900 g is more than 2090 g, so 2900 g is heavier."))
    assert len(its) == 20, len(its)
    return {"title": "Change compound units to cm, m, g or ml", "items": its}


# ------------------------------------------------------------ set 4: back to compound units, add and subtract
def set_back(P):
    its = []
    plan = [  # (value in the small unit, kind, wrong answers as text)
        (1250, "V", ["12 ℓ 50 ml", "1 ℓ 25 ml", "125 ℓ"]),
        (305, "L", ["30 m 5 cm", "3 m 50 cm", "305 m"]),
        (450, "L", ["45 m", "4 m 5 cm", "40 m 50 cm"]),
        (1500, "M", ["15 kg", "1 kg 50 g", "150 kg"]),
        (2700, "K", ["27 km", "2 km 70 m", "270 km"]),
        (4060, "M", ["40 kg 60 g", "4 kg 600 g", "4 kg 6 g"]),
        (508, "L", ["50 m 8 cm", "5 m 80 cm", "58 m"]),
        (3009, "V", ["30 ℓ 9 ml", "3 ℓ 90 ml", "3 ℓ 900 ml"]),
        (6040, "K", ["60 km 40 m", "6 km 400 m", "6 km 4 m"]),
        (7300, "M", ["73 kg", "7 kg 30 g", "730 kg"]),
    ]
    for v, kind, wr in plan:
        big, small, f = PAIR[kind]
        a, b = divmod(v, f)
        q = "%s = ? %s ? %s" % (sm(v, kind), big, small)
        e = "%s = %s + %s. %s = %d %s, so %s = %s." % (sm(v, kind), sm(a * f, kind), sm(b, kind), sm(a * f, kind),
                                                      a, big, sm(v, kind), cu(v, kind))
        its.append(mcq(q, cu(v, kind), wr, e, (fam_of(kind), base(v, kind))))
    # compare
    its.append(mcq("Which is longer: 3 m 5 cm or 350 cm?", "350 cm",
                   ["3 m 5 cm", "They are the same.", "You cannot tell."],
                   "Change to centimetres: 3 m 5 cm = 300 cm + 5 cm = 305 cm. 350 cm is longer than 305 cm."))
    its.append(mcq("Which is the most?", "2500 ml", ["2 ℓ 50 ml", "2 ℓ 5 ml", "2 ℓ 250 ml"],
                   "Change all to ml: 2 ℓ 50 ml = 2050 ml, 2 ℓ 5 ml = 2005 ml, 2 ℓ 250 ml = 2250 ml. "
                   "2500 ml is the most."))
    its.append(mcq("Which is the shortest?", "4 km 8 m", ["4 km 80 m", "4800 m", "4 km 200 m"],
                   "Change all to m: 4 km 80 m = 4080 m, 4800 m, 4 km 200 m = 4200 m, 4 km 8 m = 4008 m. "
                   "4008 m is the shortest."))
    # add and subtract
    for q, ans, wr, e, want in [
        ("2 m 45 cm + 1 m 30 cm = ?", "3 m 75 cm", ["78 cm", "1 m 15 cm", "375 m"],
         "Add the metres: 2 m + 1 m = 3 m. Add the centimetres: 45 cm + 30 cm = 75 cm. So the answer is 3 m 75 cm. "
         "Do not add 2 + 45 + 1 + 30 as one number.", ("L", 375)),
        ("4 m − 35 cm = ?", "3 m 65 cm", ["3 m 75 cm", "65 cm", "4 m 65 cm"],
         "Rename 4 m as 3 m 100 cm. 100 cm − 35 cm = 65 cm. So the answer is 3 m 65 cm.", ("L", 365)),
        ("1 kg 650 g + 500 g = ?", "2 kg 150 g", ["1 kg 150 g", "6 kg 650 g", "2 kg 650 g"],
         "650 g + 500 g = 1150 g = 1 kg 150 g. Then 1 kg + 1 kg 150 g = 2 kg 150 g.", ("M", 2150)),
        ("2 kg 800 g + 1 kg 400 g = ?", "4 kg 200 g", ["3 kg 200 g", "1 kg 400 g", "42 kg"],
         "800 g + 400 g = 1200 g = 1 kg 200 g. 2 kg + 1 kg + 1 kg 200 g = 4 kg 200 g. "
         "Do not forget the 1 kg from renaming.", ("M", 4200)),
        ("5 ℓ − 1 ℓ 300 ml = ?", "3 ℓ 700 ml", ["4 ℓ 300 ml", "4 ℓ 700 ml", "3 ℓ 300 ml"],
         "Rename 5 ℓ as 4 ℓ 1000 ml. 1000 ml − 300 ml = 700 ml and 4 ℓ − 1 ℓ = 3 ℓ. So the answer is 3 ℓ 700 ml.",
         ("V", 3700)),
        ("3 km 200 m − 1 km 500 m = ?", "1 km 700 m", ["2 km 300 m", "2 km 700 m", "1 km 300 m"],
         "200 m is less than 500 m, so rename 1 km: 3 km 200 m = 2 km 1200 m. 1200 m − 500 m = 700 m and "
         "2 km − 1 km = 1 km. So the answer is 1 km 700 m.", ("L", 170000)),
        ("2 ℓ 600 ml + 1 ℓ 750 ml = ?", "4 ℓ 350 ml", ["3 ℓ 350 ml", "1 ℓ 150 ml", "43 ℓ 50 ml"],
         "600 ml + 750 ml = 1350 ml = 1 ℓ 350 ml. 2 ℓ + 1 ℓ + 1 ℓ 350 ml = 4 ℓ 350 ml.", ("V", 4350)),
    ]:
        its.append(mcq(q, ans, wr, e, want))
    assert len(its) == 20, len(its)
    return {"title": "Change to compound units, add and subtract", "items": its}


# ------------------------------------------------------------ set 5: word problems with bar models
def set_words(P):
    its = []

    def add(q, ans, wr, e, want=None, svg=None):
        its.append(mcq((fig(svg) if svg else "") + q, ans, wr, e, want))

    n, he, his = P.next()
    add("%s has a ribbon 2 m 40 cm long. %s cuts off 85 cm to wrap a present. How much ribbon is left?"
        % (n, cap(he)), "1 m 55 cm", ["3 m 25 cm", "55 cm", "155 m"],
        "2 m 40 cm = 240 cm. Cutting off takes away: 240 cm − 85 cm = 155 cm = 1 m 55 cm.", ("L", 155),
        bar_parts([(85, "85 cm"), (155, "?")], "2 m 40 cm"))
    n, he, his = P.next()
    add("%s walks 1 km 300 m to the MRT station. Then %s walks 450 m to the library. How far does %s walk in all?"
        % (n, he, he), "1 km 750 m", ["850 m", "1 km 150 m", "1 km 75 m"],
        "Add the metres: 300 m + 450 m = 750 m. So %s walks 1 km 750 m. 1 km is 1000 m, not 100 m." % he,
        ("L", 175000))
    add("Mrs Lim has 3 kg 200 g of rice. She cooks 1 kg 500 g of it. How much rice is left?",
        "1 kg 700 g", ["2 kg 300 g", "2 kg 700 g", "4 kg 700 g"],
        "3 kg 200 g = 2 kg 1200 g. 1200 g − 500 g = 700 g and 2 kg − 1 kg = 1 kg. 1 kg 700 g of rice is left.",
        ("M", 1700), bar_parts([(1500, "1 kg 500 g"), (1700, "?")], "3 kg 200 g"))
    add("A durian has a mass of 1 kg 800 g. A pineapple has a mass of 1 kg 350 g. How much heavier is the durian?",
        "450 g", ["3 kg 150 g", "1 kg 450 g", "350 g"],
        "Both have 1 kg, so compare the grams: 800 g − 350 g = 450 g. The durian is 450 g heavier.",
        ("M", 450), bar_compare([("durian", 1800, "1 kg 800 g"), ("pineapple", 1350, "1 kg 350 g")], "?"))
    n, he, his = P.next()
    add("A jug has 2 ℓ of water. %s pours 3 cups of 250 ml from it. How much water is left in the jug?" % n,
        "1 ℓ 250 ml", ["750 ml", "1 ℓ 750 ml", "2 ℓ 750 ml"],
        "3 cups: 3 × 250 ml = 750 ml. 2 ℓ = 2000 ml. 2000 ml − 750 ml = 1250 ml = 1 ℓ 250 ml.", ("V", 1250))
    n, he, his = P.next()
    add("%s cuts a rope 3 m 60 cm long into 4 equal pieces. How long is each piece?" % n,
        "90 cm", ["15 cm", "9 cm", "90 m"],
        "3 m 60 cm = 360 cm. 4 units = 360 cm, so 1 unit = 360 ÷ 4 = 90 cm. Do not divide only the 60 cm.",
        ("L", 90), bar_parts([(90, "?"), (90, ""), (90, ""), (90, "")], "3 m 60 cm"))
    n, he, his = P.next()
    add("%s buys 5 packets of soya bean milk. Each packet holds 250 ml. How much soya bean milk is there in all?" % n,
        "1 ℓ 250 ml", ["255 ml", "12 ℓ 50 ml", "1 ℓ 25 ml"],
        "5 × 250 ml = 1250 ml. 1250 ml = 1000 ml + 250 ml = 1 ℓ 250 ml.", ("V", 1250))
    n, he, his = P.next()
    add("%s’s bus ride to school is 4 km 600 m. %s friend’s MRT ride is 2 km 800 m. How much longer is the bus ride?"
        % (n, cap(his)), "1 km 800 m", ["2 km 200 m", "7 km 400 m", "180 m"],
        "4 km 600 m = 3 km 1600 m. 1600 m − 800 m = 800 m and 3 km − 2 km = 1 km. The bus ride is 1 km 800 m longer.",
        ("L", 180000), bar_compare([("bus", 4600, "4 km 600 m"), ("MRT", 2800, "2 km 800 m")], "?"))
    add("Mr Tan’s pail can hold 8 ℓ of water. It has 5 ℓ 750 ml of water now. How much more water is needed to "
        "fill it?", "2 ℓ 250 ml", ["3 ℓ 250 ml", "13 ℓ 750 ml", "3 ℓ 750 ml"],
        "8 ℓ = 7 ℓ 1000 ml. 1000 ml − 750 ml = 250 ml and 7 ℓ − 5 ℓ = 2 ℓ. 2 ℓ 250 ml more is needed.", ("V", 2250))
    n, he, his = P.next()
    add("%s’s school bag has a mass of 3 kg 400 g. %s takes out a book of 650 g. What is the mass of the bag now?"
        % (n, cap(he)), "2 kg 750 g", ["4 kg 50 g", "3 kg 250 g", "750 g"],
        "3 kg 400 g = 2 kg 1400 g. 1400 g − 650 g = 750 g. The bag is now 2 kg 750 g.", ("M", 2750))
    add("On Sports Day, 4 pupils run a relay. Each pupil runs 400 m. How far do they run in all?",
        "1 km 600 m", ["404 m", "1 km 60 m", "160 m"],
        "4 units of 400 m: 4 × 400 m = 1600 m = 1 km 600 m.", ("L", 160000),
        bar_parts([(400, "400 m"), (400, "400 m"), (400, "400 m"), (400, "400 m")], "?"))
    add("A chicken rice stall uses 2 kg 500 g of rice each day. How much rice does it use in 3 days?",
        "7 kg 500 g", ["6 kg 500 g", "7 kg 50 g", "5 kg 500 g"],
        "3 × 2500 g = 7500 g = 7 kg 500 g. Remember that 3 × 500 g = 1500 g = 1 kg 500 g.", ("M", 7500))
    n1, he1, his1 = P.next()
    n2, he2, his2 = P.next()
    add("%s is 1 m 32 cm tall. %s is 1 m 28 cm tall. How much taller is %s?" % (n1, n2, n1),
        "4 cm", ["2 m 60 cm", "1 m 4 cm", "4 m"],
        "Both are 1 m and more, so compare the centimetres: 32 cm − 28 cm = 4 cm.", ("L", 4))
    add("Mdm Wong has 2 kg of flour. She uses 750 g to make kueh and 500 g to make bread. How much flour is left?",
        "750 g", ["1 kg 250 g", "3 kg 250 g", "250 g"],
        "She uses 750 g + 500 g = 1250 g. 2 kg = 2000 g. 2000 g − 1250 g = 750 g of flour is left.", ("M", 750),
        bar_parts([(750, "750 g"), (500, "500 g"), (750, "?")], "2 kg"))
    n, he, his = P.next()
    add("%s travels 6 km 200 m from home to Gardens by the Bay. Then %s travels home the same way. How far does %s "
        "travel in all?" % (n, he, he), "12 km 400 m", ["6 km 400 m", "12 km 200 m", "3 km 100 m"],
        "Two equal trips: 6 km 200 m + 6 km 200 m = 12 km 400 m.", ("L", 1240000))
    add("A bottle has 2 ℓ 400 ml of juice. The juice is shared equally among 4 children. How much juice does each "
        "child get?", "600 ml", ["100 ml", "2 ℓ 100 ml", "60 ml"],
        "2 ℓ 400 ml = 2400 ml. 4 units = 2400 ml, so 1 unit = 2400 ÷ 4 = 600 ml.", ("V", 600))
    add("A box of mandarin oranges for Chinese New Year has a mass of 4 kg 250 g. The empty box has a mass of 750 g. "
        "What is the mass of the oranges?", "3 kg 500 g", ["4 kg 500 g", "5 kg", "500 g"],
        "4 kg 250 g = 3 kg 1250 g. 1250 g − 750 g = 500 g. The oranges have a mass of 3 kg 500 g.", ("M", 3500),
        bar_parts([(750, "750 g"), (3500, "?")], "4 kg 250 g"))
    n, he, his = P.next()
    add("%s cycles 2 km 750 m at East Coast Park in the morning and 1 km 500 m in the evening. How far does %s cycle "
        "in all?" % (n, he), "4 km 250 m", ["3 km 250 m", "1 km 250 m", "4 km 25 m"],
        "750 m + 500 m = 1250 m = 1 km 250 m. 2 km + 1 km + 1 km 250 m = 4 km 250 m.", ("L", 425000))
    add("How many 250 ml cups can be filled from 2 ℓ of water?", "8 cups", ["4 cups", "80 cups", "2 cups"],
        "2 ℓ = 2000 ml. 4 cups of 250 ml make 1000 ml, so 2000 ml fills 2 × 4 = 8 cups.")
    n, he, his = P.next()
    add("%s is 1 m 25 cm tall. %s father is 50 cm taller than %s. %s brother is 30 cm shorter than %s father. "
        "How tall is %s brother?" % (n, cap(his), "her" if he == "she" else "him", cap(his), his, his),
        "1 m 45 cm", ["1 m 75 cm", "2 m 5 cm", "95 cm"],
        "Father: 1 m 25 cm + 50 cm = 1 m 75 cm. Brother: 1 m 75 cm − 30 cm = 1 m 45 cm.", ("L", 145))
    assert len(its) == 20, len(its)
    return {"title": "Word problems with bar models", "items": its}


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
        "<h2>Units for length, mass and volume</h2>"
        "<p><b>Length</b> is how long something is: kilometres (km), metres (m) and centimetres (cm). "
        "<b>Mass</b> is how heavy something is: kilograms (kg) and grams (g). "
        "<b>Volume</b> is how much liquid there is: litres (ℓ) and millilitres (ml).</p>" +
        table(["Fact", "About the same as"], [
            ["1 km = 1000 m", "a 15-minute walk"],
            ["1 m = 100 cm", "a metre rule, or one big step"],
            ["1 kg = 1000 g", "a 1 kg bag of sugar"],
            ["1 ℓ = 1000 ml", "a carton of milk"],
        ]) +
        "<p>Use the small unit for small things (an eraser in cm, a pencil in g, medicine in ml) "
        "and the big unit for big things (a trip in km, a bag of rice in kg, a bucket of water in ℓ).</p>"
        "<h2>Read a scale or a beaker</h2>"
        "<p>Not every mark has a number. First find <b>what one mark is worth</b>: "
        "the jump between two numbers ÷ the number of spaces. Then count on from the number before.</p>"
        "<figure class='sn-fig'>" + dial_svg(1400, 3000, 1000, 100) +
        "<figcaption>From 1 kg to 2 kg there are 10 spaces, so each mark is 100 g. "
        "The needle is 4 marks past 1 kg: 1 kg 400 g.</figcaption></figure>"
        "<figure class='sn-fig'>" + beaker_svg(1400, 2000, 1000, 200) +
        "<figcaption>From 1 ℓ to 2 ℓ there are 5 spaces, so each line is 200 ml. "
        "The water is 2 lines above 1 ℓ: 1 ℓ 400 ml.</figcaption></figure>"
        "<h2>Compound units</h2>"
        "<p>A measurement like <b>2 m 35 cm</b> uses two units. To change it to the smaller unit, "
        "change the big unit first, then add.</p>" +
        ex("Example 1", "2 m 35 cm = ? cm", "2 m = 200 cm. 200 cm + 35 cm = 235 cm.", "235 cm") +
        ex("Example 2", "3 kg 40 g = ? g", "3 kg = 3000 g. 3000 g + 40 g = 3040 g. Keep the zero in 3040.", "3040 g") +
        "<p>To change back, take out the thousands (or hundreds for cm).</p>" +
        ex("Example 3", "1250 ml = ? ℓ ? ml", "1250 ml = 1000 ml + 250 ml. 1000 ml = 1 ℓ.", "1 ℓ 250 ml") +
        "<h2>Use a bar model</h2>"
        "<figure class='sn-fig'>" + bar_parts([(85, "85 cm"), (155, "?")], "2 m 40 cm") +
        "<figcaption>A ribbon is 2 m 40 cm long. 85 cm is cut off. 240 cm − 85 cm = 155 cm = 1 m 55 cm is left."
        "</figcaption></figure>"
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["3 kg 40 g = 340 g", "3 kg = 3000 g, so 3 kg 40 g = 3040 g"],
            ["1 km = 100 m", "1 km = 1000 m (1 m = 100 cm)"],
            ["2 m + 35 cm = 37", "Add metres to metres and cm to cm: 2 m 35 cm"],
            ["1250 ml = 12 ℓ 50 ml", "1000 ml make 1 ℓ: 1250 ml = 1 ℓ 250 ml"],
            ["Counting every mark as 10", "Find what one mark is worth: jump ÷ spaces"],
            ["Forgetting to rename", "4 m − 35 cm: rename 4 m as 3 m 100 cm"],
        ])
    )


FAQ = [
    {"q": "What is taught in P3 length, mass and volume?",
     "a": "In Primary 3, students measure length in km, m and cm, mass in kg and g, and volume in ℓ and ml. "
          "They use compound units such as 2 m 35 cm and change them to the smaller unit and back."},
    {"q": "How do I explain 3 kg 40 g = 3040 g to my child?",
     "a": "Change the kilograms first: 3 kg = 3000 g. Then add the grams: 3000 g + 40 g = 3040 g, so the zero stays in the hundreds place."},
    {"q": "What is the most common mistake with compound units?",
     "a": "The most common mistake is writing the two numbers side by side, so 3 kg 40 g becomes 340 g. "
          "Another is thinking that 1 km = 100 m; it is 1000 m."},
    {"q": "Is this in the MOE syllabus?",
     "a": "Yes. Measuring length in km, volume in ml, and converting compound units (km and m, m and cm, kg and g, "
          "ℓ and ml) are part of Primary 3 Measurement in the MOE 2021 Primary Mathematics Syllabus."},
]


def balance(sets, rnd):
    """Spread the correct answers evenly (5/5/5/5) over the 4 positions in every set."""
    for s in sets:
        targets = [0, 1, 2, 3] * 5
        rnd.shuffle(targets)
        for it, t in zip(s["items"], targets):
            ch = it["c"]
            right = ch[it["a"]]
            wrong = [x for i, x in enumerate(ch) if i != it["a"]]
            rnd.shuffle(wrong)
            wrong.insert(t, right)
            it["c"] = wrong
            it["a"] = t


def verify(sets):
    """Every picture's answer is the value drawn."""
    n = 0
    for s in sets:
        for it in s["items"]:
            right = it["c"][it["a"]]
            m = re.search(r"aria-label='scale with the needle at (\d+) g'", it["q"])
            if m and "What is the mass?" in it["q"]:
                assert parse(right) == ("M", int(m.group(1))), it["q"][-80:]
                n += 1
            m = re.search(r"aria-label='measuring beaker with [a-z ]+ at (\d+) ml'", it["q"])
            if m:
                assert parse(right) == ("V", int(m.group(1))), it["q"][-80:]
                n += 1
            m = re.search(r"aria-label='measuring tape with a [a-z]+ from 0 to (\d+) cm'", it["q"])
            if m:
                assert parse(right) == ("L", int(m.group(1))), it["q"][-80:]
                n += 1
            m = re.search(r"aria-label='ruler with an eraser from (\d+) cm to (\d+) cm'", it["q"])
            if m:
                assert parse(right) == ("L", int(m.group(2)) - int(m.group(1))), it["q"][-80:]
                n += 1
            vals = [parse(x) for x in it["c"]]
            if all(vals):
                assert len(set(vals)) == 4, it["c"]
    assert n == 20, n
    return n


def mark_large(u, pattern):
    """Tag wide pictures so they print larger."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='(?:" + pattern + "))")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(63808)
    P = People(rnd)
    sets = [set_units(P), set_read(P), set_to_small(P), set_back(P), set_words(P)]
    balance(sets, rnd)
    verify(sets)
    keys = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5), (s["title"], [it["a"] for it in s["items"]])
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"].count("<svg") <= 1, it["q"]
            assert it["q"] not in keys, it["q"]
            keys.add(it["q"])
            for x in [it["q"], it["e"]] + it["c"]:
                assert "\\" not in x and '"' not in x, x
    return {
        "country": "sg", "subject": "maths", "grade": "primary-3", "slug": "length-mass-and-volume", "sort": 8,
        "updated": UPDATED, "pdf_url": "",
        "title": "Primary 3 Length, Mass and Volume",
        "seo_title": "P3 Length, Mass and Volume Worksheets: Free Primary 3 Maths with Answers (MOE Syllabus)",
        "short_title": "Length, Mass and Volume",
        "domain": "Measurement and Geometry",
        "standard_code": "Primary 3: Measurement",
        "standard_url": "https://www.moe.gov.sg/primary/curriculum/syllabus",
        "standard_text": "Measuring length in km, volume in ml; compound units; converting between km and m, "
                         "m and cm, kg and g, ℓ and ml",
        "meta_desc": "Free P3 maths practice: km, m, cm, kg, g, ℓ and ml, reading scales and beakers, "
                     "compound units like 3 kg 40 g = 3040 g. 100 questions with answers.",
        "key_big": "Change the big unit first, then add: 1 km = 1000 m, 1 m = 100 cm, 1 kg = 1000 g, 1 ℓ = 1000 ml.",
        "key_sub": "3 kg 40 g = 3000 g + 40 g = 3040 g, not 340 g.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen()
    mark_large(u, "ruler|measuring tape|bar model")
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
