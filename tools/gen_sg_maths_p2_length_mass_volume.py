# -*- coding: utf-8 -*-
"""
Singapore Primary 2 Maths: Length, Mass and Volume (MOE 2021 Primary Mathematics Syllabus, Standard,
Measurement and Geometry: measuring length in metres, mass in kilograms/grams, volume of liquid in litres;
comparing and ordering)
  python3 tools/gen_sg_maths_p2_length_mass_volume.py
Ruler, scale, jug and pan balance helpers adapted from gen_cabc_math_g3_measuring.py and gen_uk_maths_y2_measuring.py;
bar models adapted from gen_sg_maths_p3_add_sub.py (all wording rewritten for Singapore).
Primary 2: numbers to 1000, short sentences for 7-8 year olds, a picture in many questions, no unit conversions
(1 m = 100 cm and 1 kg = 1000 g come in Primary 3). Volume of liquid in litres only (ℓ, as MOE writes it).
Sets: m or cm; weighing scales in kg and g; containers in ℓ; compare and order; word problems with bar models.
Every ruler object, needle and water level is drawn exactly at its value, and every answer is parsed back and checked.
Wrong answers come from real mistakes: reading the scale from the wrong mark (every mark counted as 1, one mark off,
the next number), counting the marks instead of the spaces on a ruler, the wrong unit, thinking a bigger object is
always heavier, comparing only the first digit, adding instead of subtracting, and forgetting to rename.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "sg", "maths", "primary-2")
UPDATED = "2026-11-03"
GREEN = "#006633"
FILL = "#cfe6d6"
PARTFILL = "#fde3c8"
RED = "#c0392b"
ORANGE = "#b35900"
INK = "#2b2b2b"
WOOD = "#f6e7b8"
WATER = "#9fd3f2"
WATER_LINE = "#2a7fb8"
JUICE = "#f5a623"
JUICE_LINE = "#b86e00"
FONT = "Arial, Helvetica, sans-serif"
NB = "\u00a0"
L = "ℓ"


# ------------------------------------------------------------ units and checking
UNIT = {"cm": ("L", 1), "m": ("L", 100), "g": ("M", 1), "kg": ("M", 1000), L: ("V", 1)}
TOK = re.compile(r"(\d+)\s*(" + "|".join(sorted(UNIT, key=len, reverse=True)) + r")(?![a-zA-Z])")


def parse(s):
    """'5 kg' -> ('M', 5000). None if the string is not a plain measurement."""
    s = s.strip()
    pos, fam, tot = 0, None, 0
    for mt in TOK.finditer(s):
        if s[pos:mt.start()].strip():
            return None
        fu, sz = UNIT[mt.group(2)]
        if fam and fu != fam:
            return None
        fam = fu
        tot += int(mt.group(1)) * sz
        pos = mt.end()
    if fam is None or s[pos:].strip():
        return None
    return fam, tot


def c(n):
    return str(n)


def W(v, u):
    """(family, value in base unit) for the want= check."""
    fu, sz = UNIT[u]
    return fu, v * sz


def mcq(q, correct, cands, e, rnd, want=None):
    """4 choices: correct + 3 unique distractors. Measurement choices must differ in value.
    want = (family, value in the base unit) checks the correct answer."""
    correct = str(correct)
    if want is not None:
        assert parse(correct) == want, (q, correct, want, parse(correct))
    seen = {correct}
    pc = parse(correct)
    vals = {pc} if pc else set()
    pick = []
    for x in cands:
        if x is None:
            continue
        x = str(x)
        lead = x.split(" ")[0]
        if x in seen or not x or lead.startswith("-") or lead.startswith("−") or lead == "0":
            continue
        pv = parse(x)
        if pv:
            if pv in vals:
                continue
            vals.add(pv)
        seen.add(x)
        pick.append(x)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    ch = pick + [correct]
    rnd.shuffle(ch)
    return {"q": q, "c": ch, "a": ch.index(correct), "e": e}


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


def no_carry_add(a, b):
    """Adding each column but forgetting to rename (carry)."""
    out, place = 0, 1
    while a or b:
        out += ((a % 10 + b % 10) % 10) * place
        a, b, place = a // 10, b // 10, place * 10
    return out


def small_from_big(a, b):
    """Taking the smaller digit from the bigger one in every column (no renaming)."""
    out, place = 0, 1
    while a or b:
        out += abs(a % 10 - b % 10) * place
        a, b, place = a // 10, b // 10, place * 10
    return out


# ------------------------------------------------------------ figure: ruler (cm)
def draw_object(kind, a, b, y0=12):
    """An object lying exactly from x=a to x=b, between y0 and y0+20."""
    o = []
    y1, ym = y0 + 20, y0 + 10
    if kind in ("pencil", "crayon"):
        body = "#f4c542" if kind == "pencil" else "#3a6fb0"
        tipc = WOOD if kind == "pencil" else body
        tip = min(22, (b - a) * 0.3)
        o.append("<rect x='%.1f' y='%d' width='%.1f' height='20' fill='%s' stroke='%s' stroke-width='1.5'/>"
                 % (a, y0, b - a - tip, body, INK))
        if kind == "pencil":
            o.append("<rect x='%.1f' y='%d' width='8' height='20' fill='#e98aa0' stroke='%s' stroke-width='1.5'/>"
                     % (a, y0, INK))
        else:
            o.append("<rect x='%.1f' y='%d' width='%.1f' height='20' fill='#fff' stroke='%s' stroke-width='1.5'/>"
                     % (a + (b - a - tip) * 0.25, y0, (b - a - tip) * 0.4, INK))
        o.append("<path d='M%.1f %d L%.1f %d L%.1f %d Z' fill='%s' stroke='%s' stroke-width='1.5' "
                 "stroke-linejoin='round'/>" % (b - tip, y0, b, ym, b - tip, y1, tipc, INK))
        if kind == "pencil":
            o.append("<path d='M%.1f %.1f L%.1f %d L%.1f %.1f Z' fill='%s'/>"
                     % (b - tip * 0.25, ym - 2.5, b, ym, b - tip * 0.25, ym + 2.5, INK))
    elif kind == "eraser":
        o.append("<rect x='%.1f' y='%d' width='%.1f' height='20' rx='4' fill='#f7b7c5' stroke='%s' stroke-width='1.5'/>"
                 % (a, y0, b - a, INK))
        o.append("<rect x='%.1f' y='%d' width='%.1f' height='20' fill='#5dade2' stroke='%s' stroke-width='1.5'/>"
                 % (a + (b - a) * 0.45, y0, (b - a) * 0.4, INK))
    else:  # ribbon
        col = RED if kind == "ribbon" else "#2e86c1"
        o.append("<rect x='%.1f' y='%d' width='%.1f' height='14' fill='%s' stroke='%s' stroke-width='1.5'/>"
                 % (a, y0 + 3, b - a, col, INK))
    return "".join(o)


NAMES = {"pencil": "pencil", "crayon": "crayon", "eraser": "eraser", "ribbon": "ribbon"}


def ruler_part(X0, YR, ncm, PX):
    X = lambda v: X0 + PX * v
    o = ["<rect x='%d' y='%d' width='%d' height='50' rx='3' fill='%s' stroke='%s' stroke-width='2'/>"
         % (X0 - 14, YR, int(PX * ncm + 40), WOOD, INK)]
    small, big = [], []
    for i in range(ncm * 2 + 1):
        x = X(i / 2.0)
        (big if i % 2 == 0 else small).append("M%.1f %dL%.1f %d" % (x, YR, x, YR + (18 if i % 2 == 0 else 10)))
    o.append("<path d='%s' stroke='%s' stroke-width='1.2'/>" % ("".join(small), INK))
    o.append("<path d='%s' stroke='%s' stroke-width='2'/>" % ("".join(big), INK))
    for cc in range(ncm + 1):
        o.append(text(X(cc), YR + 38, str(cc), 15))
    o.append(text(X(ncm) + 12, YR + 38, "cm", 15, anchor="start", bold=False))
    return "".join(o)


def ruler_svg(s_cm, e_cm, kind="pencil", ncm=None):
    """Centimetre ruler from 0 to ncm with half-centimetre marks and an object from s_cm to e_cm (exact)."""
    if ncm is None:
        ncm = max(8, e_cm + 1)
    PX = 38.0
    X0, YR = 18, 40
    Wd = int(X0 * 2 + PX * ncm + 26)
    X = lambda v: X0 + PX * v
    a, b = X(s_cm), X(e_cm)
    o = [draw_object(kind, a, b)]
    for x in (a, b):
        o.append("<line x1='%.1f' y1='32' x2='%.1f' y2='%d' stroke='%s' stroke-width='1.2' stroke-dasharray='3 2'/>"
                 % (x, x, YR, RED))
    o.append(ruler_part(X0, YR, ncm, PX))
    art = "an" if kind == "eraser" else "a"
    return svg_wrap(Wd, YR + 54, "".join(o), "ruler with %s %s from %d cm to %d cm" % (art, NAMES[kind], s_cm, e_cm))


def ribbons_svg(a_cm, b_cm):
    """Two ribbons A and B, both starting at 0, above one centimetre ruler (exact)."""
    ncm = max(a_cm, b_cm) + 1
    PX = 38.0
    X0, YR = 40, 70
    Wd = int(X0 + PX * ncm + 44)
    X = lambda v: X0 + PX * v
    o, top = [], []
    for i, (nm, v, kind) in enumerate((("A", a_cm, "ribbon"), ("B", b_cm, "ribbon2"))):
        y0 = 6 + 30 * i
        top.append(text(14, y0 + 16, nm, 16))
        top.append(draw_object(kind, X(0), X(v), y0))
        o.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='1.2' stroke-dasharray='3 2'/>"
                 % (X(v), y0 + 17, X(v), YR, RED))
    o += top
    o.append("<line x1='%.1f' y1='9' x2='%.1f' y2='%d' stroke='%s' stroke-width='1.2' stroke-dasharray='3 2'/>"
             % (X(0), X(0), YR, RED))
    o.append(ruler_part(X0, YR, ncm, PX))
    return svg_wrap(Wd, YR + 54, "".join(o), "two ribbons on a ruler: A is %d cm, B is %d cm" % (a_cm, b_cm))


# ------------------------------------------------------------ figure: metre sticks
def metre_svg(k, kind="rope"):
    """A rope (or banner) exactly as long as k metre sticks laid end to end."""
    PX, X0 = 100, 10
    Wd = X0 * 2 + PX * k
    o = []
    a, b = X0, X0 + PX * k
    if kind == "rope":
        o.append("<path d='M%d 22 L%d 22' stroke='#8e5a2b' stroke-width='7' stroke-linecap='butt'/>" % (a, b))
        o.append("<path d='M%d 22 L%d 22' stroke='#c79a5b' stroke-width='2.5' stroke-dasharray='6 5'/>" % (a, b))
    else:
        o.append("<rect x='%d' y='8' width='%d' height='28' fill='#f9e79f' stroke='%s' stroke-width='1.5'/>"
                 % (a, b - a, RED))
        o.append(text((a + b) / 2.0, 28, "HAPPY CHILDREN’S DAY", 15, col=RED))
    for x in (a, b):
        o.append("<line x1='%d' y1='24' x2='%d' y2='44' stroke='%s' stroke-width='1.2' stroke-dasharray='3 2'/>"
                 % (x, x, RED))
    for i in range(k):
        x = X0 + PX * i
        o.append("<rect x='%d' y='44' width='%d' height='26' fill='%s' stroke='%s' stroke-width='1.5'/>"
                 % (x, PX, "#f4d03f" if i % 2 == 0 else "#fff", INK))
        o.append(text(x + PX / 2.0, 63, "1 m", 16))
    nm = "rope" if kind == "rope" else "banner"
    return svg_wrap(Wd, 76, "".join(o), "metre sticks: a %s as long as %d metre sticks" % (nm, k))


# ------------------------------------------------------------ figures: scale and container
def dial_svg(v, mx, lab, tick, unit, size=200):
    """Round weighing scale: 0 at the lower left, mx at the lower right (270 degrees). Needle exactly at v."""
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
             "paint-order='stroke'>" % (15 if mx >= 1000 else 17, INK))
    for val in range(0, mx + 1, lab):
        x, y = pt(val, R - 36)
        s.append("<text x='%.1f' y='%.1f'>%s</text>" % (x, y + 6, c(val)))
    s.append("</g>")
    s.append("<circle cx='%.1f' cy='%.1f' r='7' fill='%s'/>" % (cx, cy, RED))
    s.append(text(cx, cy + 62, unit, 22, col=GREEN))
    return svg_wrap(size, size, "".join(s), "scale with the needle at %s %s" % (c(v), unit))


def container_part(ox, v, mx, lab, step, liquid="water"):
    """A measuring container with a line every `step` and a number every `lab` litres. Liquid exactly at v."""
    x0, x1 = 92 + ox, 168 + ox
    yb, yt = 186, 34
    fill, line = (JUICE, JUICE_LINE) if liquid == "orange juice" else (WATER, WATER_LINE)

    def Y(val):
        return yb - (yb - yt) * float(val) / mx
    s = ["<path d='M%d %d C%d %d %d %d %d %d' fill='none' stroke='%s' stroke-width='6'/>"
         % (x1, 50, x1 + 28, 50, x1 + 28, 124, x1, 124, INK)]
    if v > 0:
        s.append("<rect x='%d' y='%.1f' width='%d' height='%.1f' fill='%s'/>" % (x0, Y(v), x1 - x0, yb - Y(v), fill))
        s.append("<line x1='%d' y1='%.1f' x2='%d' y2='%.1f' stroke='%s' stroke-width='2.5'/>"
                 % (x0, Y(v), x1, Y(v), line))
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
    s.append(text(x0 - 7, 202, L, 16, anchor="end", col=GREEN))
    return "".join(s)


def jug_svg(v, mx, lab, step, liquid="water"):
    return svg_wrap(152, 206, container_part(-50, v, mx, lab, step, liquid),
                    "container with %s at %s %s" % (liquid, c(v), L))


def two_jugs_svg(va, vb, mx, lab, step):
    o = [container_part(-50, va, mx, lab, step), container_part(110, vb, mx, lab, step)]
    o.append(text(80, 226, "A", 18))
    o.append(text(240, 226, "B", 18))
    return svg_wrap(312, 232, "".join(o), "two containers: A has %d %s, B has %d %s" % (va, L, vb, L))


def bottles_svg(k, each=1):
    """k bottles in a row, each labelled with what it holds."""
    BW, GAP, X0 = 34, 8, 6
    Wd = X0 * 2 + k * BW + (k - 1) * GAP
    o = []
    for i in range(k):
        x = X0 + i * (BW + GAP)
        o.append("<rect x='%.1f' y='4' width='12' height='8' rx='2' fill='%s'/>" % (x + BW / 2.0 - 6, GREEN))
        o.append("<path d='M%.1f 12 L%.1f 12 L%.1f 26 Q%.1f 30 %.1f 34 L%.1f 82 Q%.1f 86 %.1f 86 L%.1f 86 "
                 "Q%.1f 86 %.1f 82 L%.1f 34 Q%.1f 30 %.1f 26 Z' fill='%s' stroke='%s' stroke-width='1.8'/>"
                 % (x + BW / 2.0 - 7, x + BW / 2.0 + 7, x + BW / 2.0 + 7, x + BW, x + BW, x + BW, x + BW,
                    x + BW - 4, x + 4, x, x, x, x, x + BW / 2.0 - 7, WATER, INK))
        o.append("<rect x='%.1f' y='46' width='%d' height='24' fill='#fff' stroke='%s' stroke-width='1'/>"
                 % (x + 2, BW - 4, INK))
        o.append(text(x + BW / 2.0, 64, "%d %s" % (each, L), 14))
    return svg_wrap(Wd, 92, "".join(o), "bottles: %d bottles of %d %s each" % (k, each, L))


# ------------------------------------------------------------ figure: pan balance
def draw_obj(kind, cx, yb, w, h, col):
    x, y = cx - w / 2.0, yb - h
    if kind == "weight":
        return ("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' rx='4' fill='%s'/>"
                "<text x='%.1f' y='%.1f' font-size='14' font-weight='700' fill='#fff' text-anchor='middle'>%s</text>"
                % (x, y, w, h, GREEN, cx, yb - 6, col))
    if kind == "round":
        return ("<ellipse cx='%.1f' cy='%.1f' rx='%.1f' ry='%.1f' fill='%s' stroke='%s' stroke-width='1.5'/>"
                % (cx, yb - h / 2.0, w / 2.0, h / 2.0, col, INK))
    if kind == "ball2":
        r = w / 2.0
        return ("<circle cx='%.1f' cy='%.1f' r='%.1f' fill='#fff' stroke='%s' stroke-width='1.5'/>"
                "<path d='M%.1f %.1f Q%.1f %.1f %.1f %.1f' stroke='%s' stroke-width='6' fill='none'/>"
                "<path d='M%.1f %.1f Q%.1f %.1f %.1f %.1f' stroke='#e6b800' stroke-width='6' fill='none'/>"
                % (cx, yb - r, r, INK, cx, yb - 2 * r + 2, cx - r * 0.9, yb - r, cx, yb - 2, RED,
                   cx, yb - 2 * r + 2, cx + r * 0.9, yb - r, cx, yb - 2))
    if kind == "melon":
        return ("<ellipse cx='%.1f' cy='%.1f' rx='%.1f' ry='%.1f' fill='#3c8d40' stroke='%s' stroke-width='1.5'/>"
                "<path d='M%.1f %.1f Q%.1f %.1f %.1f %.1f M%.1f %.1f Q%.1f %.1f %.1f %.1f' stroke='#1e5b22' "
                "stroke-width='2' fill='none'/>"
                % (cx, yb - h / 2.0, w / 2.0, h / 2.0, INK, cx - w * 0.2, y + 3, cx - w * 0.32, yb - h / 2.0,
                   cx - w * 0.2, yb - 3, cx + w * 0.2, y + 3, cx + w * 0.32, yb - h / 2.0, cx + w * 0.2, yb - 3))
    if kind == "pineapple":
        return ("<path d='M%.1f %.1f L%.1f %.1f L%.1f %.1f L%.1f %.1f L%.1f %.1f Z' fill='#2e8b57'/>"
                "<ellipse cx='%.1f' cy='%.1f' rx='%.1f' ry='%.1f' fill='#e5a50a' stroke='%s' stroke-width='1.5'/>"
                % (cx - 9, y + 14, cx - 4, y, cx, y + 8, cx + 5, y, cx + 9, y + 14,
                   cx, yb - (h - 12) / 2.0, w / 2.0, (h - 12) / 2.0, INK))
    if kind == "pillow":
        return ("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' rx='12' fill='%s' stroke='%s' stroke-width='1.5'/>"
                % (x, y, w, h, col, INK))
    return ("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' rx='3' fill='%s' stroke='%s' stroke-width='1.5'/>"
            % (x, y, w, h, col, INK))


def weight(v, u):
    t = "%d %s" % (v, u)
    return ("weight", 14 + 8.6 * len(t), 22, t)


def pack(items, maxw=124, gap=4):
    rows, cur, cw = [], [], 0
    for it in items:
        w = it[1]
        if cur and cw + gap + w > maxw:
            rows.append(cur)
            cur, cw = [], 0
        cw = cw + (gap if cur else 0) + w
        cur.append(it)
    if cur:
        rows.append(cur)
    return [(r, sum(i[1] for i in r) + gap * (len(r) - 1), max(i[2] for i in r)) for r in rows]


def balance_svg(left, right, tilt=0, lname="", rname="", label="pan balance"):
    """tilt > 0: left side down. Items are (kind, w, h, colour_or_text)."""
    Wd = 360
    LX, RX, PX = 85, 275, 180
    d = 14 * tilt
    pl, pr = pack(left), pack(right)
    hs = max(sum(r[2] for r in pl) + 2 * (len(pl) - 1), sum(r[2] for r in pr) + 2 * (len(pr) - 1))
    piv = 12 + hs + abs(d) + 24
    s = []
    s.append("<rect x='%d' y='%d' width='10' height='34' fill='%s'/>" % (PX - 5, piv, INK))
    s.append("<rect x='%d' y='%d' width='90' height='9' rx='3' fill='%s'/>" % (PX - 45, piv + 34, INK))
    s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='6' stroke-linecap='round'/>"
             % (LX, piv + d, RX, piv - d, INK))
    s.append("<circle cx='%d' cy='%d' r='6' fill='%s'/>" % (PX, piv, RED))
    for cx, ey, rows in ((LX, piv + d, pl), (RX, piv - d, pr)):
        top = ey - 24
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='4'/>" % (cx, top + 6, cx, ey, INK))
        s.append("<rect x='%d' y='%d' width='124' height='7' rx='3' fill='%s'/>" % (cx - 62, top, GREEN))
        yb = top
        for row, rw, rh in rows:
            x = cx - rw / 2.0
            for it in row:
                s.append(draw_obj(it[0], x + it[1] / 2.0, yb, it[1], it[2], it[3]))
                x += it[1] + 4
            yb -= rh + 2
    H = piv + 44
    if lname or rname:
        H = piv + 66
        for cx, t in ((LX, lname), (RX, rname)):
            if t:
                s.append(text(cx, piv + 62, t, 16))
    return svg_wrap(Wd, H, "".join(s), label)


OBJ = {  # name: (kind, w, h, colour)
    "bowling ball": ("round", 38, 38, "#34495e"), "beach ball": ("ball2", 62, 62, ""),
    "brick": ("box", 54, 24, "#b5523b"), "pillow": ("pillow", 96, 34, "#f3e3f7"),
    "stone": ("round", 34, 26, "#8d8d8d"), "packet of chips": ("pillow", 70, 40, "#f39c12"),
    "watermelon": ("melon", 70, 48, ""), "pineapple": ("pineapple", 36, 52, ""),
}


def an(w):
    return ("an " if w[0] in "aeiou" else "a ") + w


# ------------------------------------------------------------ bar models
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


def brace(x1, x2, y, up, lab, col=INK):
    d = 7 if up else -7
    o = ["<path d='M%.1f %.1f L%.1f %.1f L%.1f %.1f L%.1f %.1f' fill='none' stroke='%s' stroke-width='2'/>"
         % (x1, y + d, x1, y, x2, y, x2, y + d, col)]
    o.append(text((x1 + x2) / 2.0, y - 7 if up else y + 20, lab, 16, col=col))
    return "".join(o)


def bar_parts(parts_, total_lab, BW=420):
    """One bar split into parts drawn to scale. parts_ = [(value, label inside)]. Bracket below with total_lab."""
    X0, TOP, BH = 10, 8, 40
    tot = sum(v for v, _ in parts_)
    Wd = X0 * 2 + BW
    H = TOP + BH + 36
    o, x = [], float(X0)
    fills = [FILL, PARTFILL, "#fff"]
    for i, (v, lab) in enumerate(parts_):
        w = float(v) / tot * BW
        assert tw(lab, 16) <= w - 6, (lab, w)
        o.append("<rect x='%.1f' y='%d' width='%.1f' height='%d' fill='%s' stroke='%s' stroke-width='2'/>"
                 % (x, TOP, w, BH, fills[i % 3], GREEN))
        o.append(text(x + w / 2.0, TOP + BH / 2.0 + 6, lab, 16, col=RED if lab == "?" else INK))
        x += w
    o.append(brace(X0, X0 + BW, TOP + BH + 10, False, total_lab, col=RED if total_lab == "?" else INK))
    return svg_wrap(Wd, H, "".join(o), "bar model: parts %s, whole %s" % (", ".join(l for _, l in parts_), total_lab))


def bar_compare(rows, diff_lab, BW=360):
    """Comparison model. rows = [(name, value, label inside)], the first bar is the longer one.
    The shorter bar has a dashed part up to the longer one, with diff_lab inside it."""
    (n1, v1, l1), (n2, v2, l2) = rows
    assert v1 > v2
    LW = int(max(tw(n1, 16), tw(n2, 16))) + 16
    X0, TOP, BH, GAP = 6, 8, 38, 16
    x0 = X0 + LW
    Wd = x0 + BW + 10
    H = TOP + 2 * BH + GAP + 8
    w2 = float(v2) / v1 * BW
    o = []
    for i, (nm, w, lab, fill) in enumerate([(n1, BW, l1, FILL), (n2, w2, l2, PARTFILL)]):
        y = TOP + i * (BH + GAP)
        assert tw(lab, 16) <= w - 6, (lab, w)
        o.append(text(x0 - 10, y + BH / 2.0 + 6, nm, 16, anchor="end"))
        o.append("<rect x='%d' y='%d' width='%.1f' height='%d' fill='%s' stroke='%s' stroke-width='2'/>"
                 % (x0, y, w, BH, fill, GREEN))
        o.append(text(x0 + w / 2.0, y + BH / 2.0 + 6, lab, 16, col=RED if lab == "?" else INK))
    y = TOP + BH + GAP
    dw = BW - w2
    assert tw(diff_lab, 16) <= dw - 6, (diff_lab, dw)
    o.append("<rect x='%.1f' y='%d' width='%.1f' height='%d' fill='none' stroke='%s' stroke-width='2' "
             "stroke-dasharray='6 4'/>" % (x0 + w2, y, dw, BH, ORANGE))
    o.append(text(x0 + w2 + dw / 2.0, y + BH / 2.0 + 6, diff_lab, 16, col=RED if diff_lab == "?" else ORANGE))
    lab = "bar model comparing %s (%s) and %s (%s), difference %s" % (n1, l1, n2, l2, diff_lab)
    return svg_wrap(int(Wd), H, "".join(o), lab)


def bar_units(n, each_lab, total_lab, BW=400):
    """n equal units in one bar, each labelled each_lab, bracket below with total_lab."""
    X0, TOP, BH = 10, 8, 40
    w = float(BW) / n
    assert tw(each_lab, 16) <= w - 6, (each_lab, w)
    o = []
    for i in range(n):
        x = X0 + i * w
        o.append("<rect x='%.1f' y='%d' width='%.1f' height='%d' fill='%s' stroke='%s' stroke-width='2'/>"
                 % (x, TOP, w, BH, FILL, GREEN))
        o.append(text(x + w / 2.0, TOP + BH / 2.0 + 6, each_lab, 16, col=RED if each_lab == "?" else INK))
    o.append(brace(X0, X0 + BW, TOP + BH + 10, False, total_lab, col=RED if total_lab == "?" else INK))
    return svg_wrap(X0 * 2 + BW, TOP + BH + 36, "".join(o),
                    "bar model: %d equal units of %s, whole %s" % (n, each_lab, total_lab))


# ------------------------------------------------------------ explanations for scales and containers
def read_e(v, lab, tick, unit, what):
    """what: 'needle', 'water' or 'orange juice'."""
    sp = lab // tick
    base = v - v % lab
    k = (v - base) // tick
    w = "mark" if what == "needle" else "line"
    if sp == 1:
        s = "Every %s has a number. " % w
    else:
        s = ("The numbers go up by %s %s. There are %d spaces between two numbers, so each %s is %s %s. "
             % (c(lab), unit, sp, w, c(tick), unit))
    if what == "needle":
        if k == 0:
            return s + "The needle points right at %s: %s %s." % (c(base), c(v), unit)
        if base == 0:
            return s + "The needle is %s past 0: %s %s." % (marks(k), c(v), unit)
        return s + "The needle is %s past %s: %s + %s = %s %s." % (marks(k), c(base), c(base), c(k * tick), c(v), unit)
    if k == 0:
        return s + "The top of the %s is right at the %s line: %s %s." % (what, c(base), c(v), unit)
    if base == 0:
        return s + "The top of the %s is %s up from the bottom: %s %s." % (what, marks(k, "line"), c(v), unit)
    return s + "The top of the %s is %s above %s: %s + %s = %s %s." % (
        what, marks(k, "line"), c(base), c(base), c(k * tick), c(v), unit)


def read_wrongs(v, lab, tick, unit, alt, i):
    """Real mistakes: every mark counted as 1 (or as 2 when marks are 1), one mark off, the next number,
    the number before, the wrong unit."""
    base = v - v % lab
    k = (v - base) // tick
    mis = base + k if tick != 1 else base + 2 * k
    w = ["%s %s" % (c(mis), unit), "%s %s" % (c(v + tick), unit), "%s %s" % (c(base + lab), unit),
         "%s %s" % (c(v - tick), unit), "%s %s" % (c(base), unit), "%s %s" % (c(v + 2 * tick), unit)]
    if alt:
        w.insert(1 if i % 3 == 0 else 4, "%s %s" % (c(v), alt))
    return w


# ------------------------------------------------------------ set 1: m or cm
CHL = ["centimetres (cm)", "metres (m)", "kilograms (kg)", "litres (%s)" % L]


def set_length(rnd):
    its = []
    for obj, u, why in [
        ("the length of an eraser", 0, "An eraser is short. It fits on a ruler, so use centimetres."),
        ("the length of a storybook", 0, "A storybook fits on your desk and on a ruler, so use centimetres."),
        ("the length of a leaf", 0, "A leaf is small enough to hold in your hand, so use centimetres."),
        ("the height of a water bottle", 0, "A water bottle fits in your school bag, so use centimetres."),
        ("the length of the school field", 1, "The school field is very long. Use metres."),
        ("the height of an HDB block", 1, "An HDB block is very tall. Use metres."),
        ("the length of a swimming pool", 1, "A swimming pool is much longer than a ruler, so use metres."),
        ("the length of the school corridor", 1, "A corridor is long. You walk many steps along it, so use metres."),
    ]:
        e = why + " Kilograms measure mass and litres measure volume, not length."
        its.append(mcq("Which unit would you use to measure %s?" % obj, CHL[u], CHL, e, rnd))
    for q, ans, wr, e, wv in [
        ("A new pencil is about ☐ long.", "18 cm", ["18 m", "180 cm", "1 cm"],
         "A new pencil fits on a 30 cm ruler, so it is about 18 cm. 18 m is longer than a bus.", W(18, "cm")),
        ("A classroom door is about ☐ tall.", "2 m", ["2 cm", "20 m", "20 cm"],
         "A door is a bit taller than an adult. That is about 2 m. 2 cm is shorter than your finger.", W(2, "m")),
        ("A Primary 2 pupil is about ☐ tall.", "120 cm", ["120 m", "12 cm", "12 m"],
         "Most Primary 2 pupils are a little taller than a metre stick: about 120 cm. 12 cm is the size of a hand.",
         W(120, "cm")),
        ("A bus is about ☐ long.", "12 m", ["12 cm", "120 m", "1 m"],
         "A bus is about as long as 6 doors lying end to end, so about 12 m.", W(12, "m")),
        ("An exercise book is about ☐ long.", "25 cm", ["25 m", "2 cm", "250 cm"],
         "An exercise book is a little shorter than a 30 cm ruler: about 25 cm.", W(25, "cm")),
        ("The tip of your finger is about ☐ wide.", "1 cm", ["1 m", "10 cm", "10 m"],
         "Your fingertip is a good way to remember 1 cm.", W(1, "cm")),
        ("A classroom is about ☐ long.", "9 m", ["9 cm", "90 m", "1 m"],
         "A classroom is much longer than a door is tall, but you can walk across it in a few steps: about 9 m.",
         W(9, "m")),
    ]:
        its.append(mcq("Choose the best answer. " + q, ans, wr, e, rnd, want=wv))
    for e_cm, kind in [(7, "crayon"), (12, "pencil")]:
        nm = NAMES[kind]
        q = fig(ruler_svg(0, e_cm, kind)) + "How long is the %s?" % nm
        e = ("The %s starts at 0 and ends at %d, so it is %d cm long. Count the spaces, not the marks: "
             "there are %d numbers from 0 to %d but only %d spaces." % (nm, e_cm, e_cm, e_cm + 1, e_cm, e_cm))
        its.append(mcq(q, "%d cm" % e_cm, ["%d cm" % (e_cm + 1), "%d m" % e_cm, "%d cm" % (e_cm - 1)], e, rnd,
                       want=W(e_cm, "cm")))
    s_cm, e_cm = 3, 9
    ln = e_cm - s_cm
    q = fig(ruler_svg(s_cm, e_cm, "ribbon")) + "How long is the ribbon?"
    e = ("The ribbon starts at %d, not at 0. It ends at %d. %d − %d = %d, so it is %d cm long. "
         "You can also count the spaces from %d to %d: there are %d." % (s_cm, e_cm, e_cm, s_cm, ln, ln, s_cm, e_cm, ln))
    its.append(mcq(q, "%d cm" % ln, ["%d cm" % e_cm, "%d cm" % (ln + 1), "%d m" % ln], e, rnd, want=W(ln, "cm")))
    for k, kind in [(3, "rope"), (4, "banner")]:
        nm = "rope" if kind == "rope" else "banner"
        q = fig(metre_svg(k, kind)) + "The %s is as long as these metre sticks. How long is the %s?" % (nm, nm)
        e = ("Each metre stick is 1 m long. The %s is as long as %d metre sticks, so it is %d m long. "
             "Count the sticks, not the lines between them." % (nm, k, k))
        its.append(mcq(q, "%d m" % k, ["%d cm" % k, "%d m" % (k + 1), "%d m" % (k - 1)], e, rnd, want=W(k, "m")))
    assert len(its) == 20, len(its)
    return {"title": "Metres or centimetres?", "items": its}


# ------------------------------------------------------------ set 2: weighing scales
DIALS = [  # (value, max, label step, tick, unit, object)
    (2, 5, 1, 1, "kg", "a durian"),
    (3, 10, 2, 1, "kg", "a bag of potatoes"),
    (5, 10, 2, 1, "kg", "a bag of rice"),
    (7, 10, 2, 1, "kg", "a watermelon"),
    (9, 20, 5, 1, "kg", "a box of mandarin oranges"),
    (16, 20, 5, 1, "kg", "a suitcase"),
    (24, 50, 10, 2, "kg", "a Primary 2 pupil"),
    (25, 50, 10, 5, "kg", "a sack of rice"),
    (150, 500, 100, 50, "g", "an apple"),
    (450, 500, 100, 50, "g", "a loaf of bread"),
    (240, 500, 100, 20, "g", "a mango"),
    (180, 200, 50, 10, "g", "a bunch of rambutans"),
    (300, 1000, 200, 100, "g", "a packet of noodles"),
    (700, 1000, 200, 100, "g", "a papaya"),
    (900, 1000, 200, 100, "g", "a bag of onions"),
    (650, 1000, 200, 50, "g", "a pack of chicken"),
]


def set_scale(rnd):
    its = []
    for i, (v, mx, lab, tick, unit, obj) in enumerate(DIALS):
        alt = "g" if unit == "kg" else "kg"
        q = fig(dial_svg(v, mx, lab, tick, unit)) + "The scale shows the mass of %s. What is the mass?" % obj
        its.append(mcq(q, "%s %s" % (c(v), unit), read_wrongs(v, lab, tick, unit, alt, i),
                       read_e(v, lab, tick, unit, "needle"), rnd, want=W(v, unit)))
    its.append(mcq(fig(balance_svg([OBJ["pineapple"]], [weight(x, "g") for x in (500, 200, 100)], 0, "pineapple", "",
                                   "level pan balance with a pineapple and weights")) +
                   "The pan balance is level. What is the mass of the pineapple?",
                   "800 g", ["500 g", "700 g", "800 kg", "3 g"],
                   "The pans are level, so the pineapple has the same mass as the weights: 500 + 200 + 100 = 800 g.",
                   rnd, want=W(800, "g")))
    its.append(mcq(fig(balance_svg([OBJ["watermelon"]], [weight(x, "kg") for x in (2, 2, 1)], 0, "watermelon", "",
                                   "level pan balance with a watermelon and weights")) +
                   "The pan balance is level. What is the mass of the watermelon?",
                   "5 kg", ["3 kg", "4 kg", "5 g", "6 kg"],
                   "The pans are level, so the watermelon has the same mass as the weights: 2 + 2 + 1 = 5 kg.",
                   rnd, want=W(5, "kg")))
    its.append(mcq(fig(dial_svg(750, 1000, 200, 50, "g")) +
                   "The scale shows a basket of eggs. The empty basket has a mass of 150 g. "
                   "What is the mass of the eggs?",
                   "600 g", ["900 g", "750 g", "150 g", "650 g"],
                   "Each mark is 50 g, so the needle is at 750 g. Take away the basket: 750 − 150 = 600 g.",
                   rnd, want=W(600, "g")))
    its.append(mcq(fig(dial_svg(8, 10, 2, 1, "kg")) +
                   "This is a bag of potatoes on the scale. Ahmad puts in 2 kg more. What will the scale show then?",
                   "10 kg", ["6 kg", "8 kg", "10 g", "9 kg"],
                   "Each mark is 1 kg, so the needle is at 8 kg now. Adding makes it heavier: 8 + 2 = 10 kg.",
                   rnd, want=W(10, "kg")))
    assert len(its) == 20, len(its)
    return {"title": "Read weighing scales in kg and g", "items": its}


# ------------------------------------------------------------ set 3: containers in litres
JUGS = [  # (value, max, label step, line step, liquid)
    (3, 5, 1, 1, "water"),
    (4, 10, 2, 1, "water"),
    (7, 10, 2, 1, "orange juice"),
    (9, 10, 2, 1, "water"),
    (6, 10, 2, 1, "water"),
    (12, 20, 5, 1, "water"),
    (17, 20, 5, 1, "water"),
    (8, 20, 5, 1, "orange juice"),
    (14, 20, 10, 2, "water"),
    (16, 40, 10, 2, "water"),
    (25, 50, 10, 5, "water"),
    (45, 50, 10, 5, "water"),
]


def set_jug(rnd):
    its = []
    for i, (v, mx, lab, step, liq) in enumerate(JUGS):
        q = fig(jug_svg(v, mx, lab, step, liq)) + "How much %s is in the container?" % liq
        its.append(mcq(q, "%s %s" % (c(v), L), read_wrongs(v, lab, step, L, None, i),
                       read_e(v, lab, step, L, liq), rnd, want=W(v, L)))
    its.append(mcq(fig(jug_svg(6, 10, 2, 1)) +
                   "How many more litres of water are needed to fill the container to 10 %s?" % L,
                   "4 %s" % L, ["16 %s" % L, "6 %s" % L, "5 %s" % L],
                   "Each line is 1 %s, so the water is at 6 %s. 10 − 6 = 4 %s more." % (L, L, L),
                   rnd, want=W(4, L)))
    its.append(mcq(fig(jug_svg(13, 20, 5, 1)) +
                   "How many more litres of water are needed to fill the container to 20 %s?" % L,
                   "7 %s" % L, ["33 %s" % L, "13 %s" % L, "8 %s" % L],
                   "Each line is 1 %s, so the water is at 13 %s. 20 − 13 = 7 %s more." % (L, L, L),
                   rnd, want=W(7, L)))
    its.append(mcq(fig(jug_svg(18, 20, 5, 1)) +
                   "Nurul pours 6 %s of water out of the container. How much water is left?" % L,
                   "12 %s" % L, ["24 %s" % L, "6 %s" % L, "11 %s" % L],
                   "Each line is 1 %s, so the water is at 18 %s. Water is poured out, so subtract: "
                   "18 − 6 = 12 %s." % (L, L, L), rnd, want=W(12, L)))
    its.append(mcq(fig(bottles_svg(6)) + "Wei Ming fills these bottles with water from a pail. "
                   "How much water did the pail have?", "6 %s" % L, ["7 %s" % L, "5 %s" % L, "1 %s" % L],
                   "Each bottle holds 1 %s. There are 6 bottles, so the pail had 6 %s." % (L, L), rnd, want=W(6, L)))
    its.append(mcq(fig(bottles_svg(8)) + "A pail holds as much water as these bottles. How much does the pail hold?",
                   "8 %s" % L, ["9 %s" % L, "7 %s" % L, "1 %s" % L],
                   "Each bottle holds 1 %s. Count the bottles: 8 bottles hold 8 %s." % (L, L), rnd, want=W(8, L)))
    its.append(mcq(fig(bottles_svg(5, 2)) + "Each bottle holds 2 %s of water. How much water is there in all?" % L,
                   "10 %s" % L, ["5 %s" % L, "7 %s" % L, "2 %s" % L],
                   "Count in twos: 2, 4, 6, 8, 10. 5 bottles of 2 %s is 5 × 2 = 10 %s. "
                   "5 %s counts the bottles, not the litres." % (L, L, L), rnd, want=W(10, L)))
    its.append(mcq("Which of these holds about 1 %s?" % L, "a carton of milk",
                   ["a teaspoon", "a bathtub", "a small cup"],
                   "A big carton of milk from the supermarket holds about 1 %s. A teaspoon and a small cup hold much "
                   "less. A bathtub holds much more." % L, rnd))
    its.append(mcq("Which of these holds much more than 1 %s?" % L, "a bathtub",
                   ["a teaspoon", "a juice box", "a small cup"],
                   "A bathtub holds a lot of water, many litres. A teaspoon, a juice box and a small cup "
                   "each hold less than 1 %s." % L, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Read containers in litres (%s)" % L, "items": its}


# ------------------------------------------------------------ set 4: compare and order
def set_compare(rnd):
    its = []
    for hv, lt, word, side in [("bowling ball", "beach ball", "heavier", 1), ("brick", "pillow", "heavier", -1),
                               ("stone", "packet of chips", "lighter", 1)]:
        Ln, Rn = (hv, lt) if side == 1 else (lt, hv)
        ans = hv if word == "heavier" else lt
        wrong = lt if word == "heavier" else hv
        down = "left" if side == 1 else "right"
        e = ("The %s pan is lower. The lower pan holds the heavier object, so the %s is heavier and the %s is lighter. "
             "A bigger object is not always heavier." % (down, hv, lt))
        its.append(mcq(fig(balance_svg([OBJ[Ln]], [OBJ[Rn]], side, Ln, Rn,
                                       "pan balance with %s and %s, %s side down" % (an(Ln), an(Rn), down))) +
                       "Look at the pan balance. Which is %s?" % word,
                       "the %s" % ans, ["the %s" % wrong, "They are the same.", "You cannot tell."], e, rnd))
    its.append(mcq("A box is heavier than a bag. The bag is heavier than a basket. Which is the lightest?",
                   "the basket", ["the box", "the bag", "You cannot tell."],
                   "The box is heavier than the bag, and the bag is heavier than the basket. "
                   "So the basket is the lightest.", rnd))
    its.append(mcq("Which is the heaviest?", "351 g", ["315 g", "153 g", "135 g"],
                   "Compare the hundreds first: 315 and 351 have 3 hundreds, 153 and 135 have only 1. "
                   "Then compare the tens of 315 and 351: 5 tens is more than 1 ten. So 351 g is the heaviest.", rnd, want=W(351, "g")))
    its.append(mcq("Which is the shortest?", "607 cm", ["670 cm", "760 cm", "706 cm"],
                   "607 and 670 have 6 hundreds, the others have 7. Then compare the tens: 0 tens is less than "
                   "7 tens. So 607 cm is the shortest.", rnd, want=W(607, "cm")))
    its.append(mcq("Which is the greatest volume?", "42 %s" % L, ["24 %s" % L, "40 %s" % L, "4 %s" % L],
                   "Compare the tens first: 42 and 40 have 4 tens. Then the ones: 2 is more than 0. "
                   "So 42 %s is the greatest." % L, rnd, want=W(42, L)))
    its.append(mcq("Arrange the lengths from the shortest to the longest: 45 m, 54 m, 40 m.",
                   "40 m, 45 m, 54 m", ["54 m, 45 m, 40 m", "45 m, 54 m, 40 m", "40 m, 54 m, 45 m"],
                   "Compare the tens: 40 and 45 have 4 tens, 54 has 5 tens, so 54 m is the longest. "
                   "40 is less than 45. Shortest to longest: 40 m, 45 m, 54 m.", rnd))
    its.append(mcq("Arrange the masses from the heaviest to the lightest: 308 g, 380 g, 83 g.",
                   "380 g, 308 g, 83 g", ["83 g, 308 g, 380 g", "308 g, 380 g, 83 g", "83 g, 380 g, 308 g"],
                   "83 has no hundreds, so 83 g is the lightest, even though 8 looks big. 380 has more tens than 308. "
                   "Heaviest to lightest: 380 g, 308 g, 83 g.", rnd))
    its.append(mcq("Arrange the volumes from the least to the most: 15 %s, 51 %s, 5 %s." % (L, L, L),
                   "5 %s, 15 %s, 51 %s" % (L, L, L),
                   ["51 %s, 15 %s, 5 %s" % (L, L, L), "15 %s, 5 %s, 51 %s" % (L, L, L),
                    "15 %s, 51 %s, 5 %s" % (L, L, L)],
                   "5 has no tens, so 5 %s is the least. 51 has 5 tens and 15 has 1 ten. "
                   "Least to most: 5 %s, 15 %s, 51 %s." % (L, L, L, L), rnd))
    its.append(mcq(fig(ribbons_svg(9, 5)) + "How much longer is ribbon A than ribbon B?", "4 cm",
                   ["14 cm", "9 cm", "5 cm"],
                   "Ribbon A ends at 9 cm and ribbon B ends at 5 cm. “How much longer” means subtract: 9 − 5 = 4 cm.",
                   rnd, want=W(4, "cm")))
    its.append(mcq(fig(ribbons_svg(6, 11)) + "Which ribbon is longer, and by how much?", "B, by 5 cm",
                   ["A, by 5 cm", "B, by 17 cm", "B, by 11 cm"],
                   "Ribbon B ends at 11 cm and ribbon A ends at 6 cm, so B is longer. 11 − 6 = 5 cm.", rnd))
    its.append(mcq(fig(two_jugs_svg(8, 5, 10, 2, 1)) + "How much more water is in container A than in container B?",
                   "3 %s" % L, ["13 %s" % L, "8 %s" % L, "5 %s" % L],
                   "Each line is 1 %s. A has 8 %s and B has 5 %s. 8 − 5 = 3 %s more." % (L, L, L, L),
                   rnd, want=W(3, L)))
    its.append(mcq(fig(two_jugs_svg(12, 18, 20, 5, 1)) + "Which container has more water, and how much more?",
                   "B, 6 %s more" % L, ["A, 6 %s more" % L, "B, 30 %s more" % L, "B, 18 %s more" % L],
                   "Each line is 1 %s. A has 12 %s and B has 18 %s, so B has more. 18 − 12 = 6 %s more."
                   % (L, L, L, L), rnd))
    its.append(mcq("Xin Yi pours 2 %s of water into a tall, thin container. Zhi Hao pours 2 %s of water into a short, "
                   "wide container. Which has more water?" % (L, L), "They have the same.",
                   ["the tall container", "the wide container", "You cannot tell."],
                   "Both have 2 %s. The water in the tall container looks higher, but the amount is the same." % L, rnd))
    its.append(mcq("Which is lighter: 409 g or 490 g?", "409 g", ["490 g", "They are the same.", "You cannot tell."],
                   "Both have 4 hundreds. Compare the tens: 0 tens is less than 9 tens. So 409 g is lighter.",
                   rnd, want=W(409, "g")))
    its.append(mcq("A bag of rice has a mass of 8 kg. Another bag of rice has a mass of 5 kg. "
                   "How much heavier is the first bag?", "3 kg", ["13 kg", "8 kg", "3 g"],
                   "“How much heavier” means subtract: 8 − 5 = 3 kg.", rnd, want=W(3, "kg")))
    its.append(mcq("Mei Ling is 125 cm tall. Jun Jie is 118 cm tall. Who is taller, and by how much?",
                   "Mei Ling, by 7 cm", ["Jun Jie, by 7 cm", "Mei Ling, by 13 cm", "Mei Ling, by 243 cm"],
                   "125 is more than 118, so Mei Ling is taller. 125 − 118 = 7 cm. Rename 1 ten as 10 ones: "
                   "15 − 8 = 7. Do not take 5 from 8.", rnd))
    its.append(mcq("Raju is 132 cm tall. Priya is 123 cm tall. Kumar is 128 cm tall. Who is the tallest?",
                   "Raju", ["Priya", "Kumar", "You cannot tell."],
                   "All have 1 hundred. Compare the tens: 132 has 3 tens, 123 and 128 have 2 tens. "
                   "So Raju is the tallest.", rnd))
    its.append(mcq("Ryan says, “The bigger box is always the heavier one.” Is he right?",
                   "No. A big box can be light.", ["Yes, always.", "Yes, if it is taller.", "Yes, if it is wider."],
                   "Size does not tell you the mass. A big box of cotton wool can be lighter than a small box of "
                   "stones. Use a pan balance or a scale to check.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Compare and order length, mass and volume", "items": its}


# ------------------------------------------------------------ set 5: word problems
def set_story(rnd):
    its = []

    def add(q, ans, u, wrong, e, model=None):
        f = fig(model) if model else ""
        its.append(mcq(f + q, "%s %s" % (c(ans), u), ["%s %s" % (c(x), uu) for x, uu in wrong if x > 0], e, rnd,
                       want=W(ans, u)))

    add("Mr Tan buys some durians with a mass of 4 kg. He also buys some mangoes with a mass of 3 kg. "
        "What is the total mass of the fruit?", 7, "kg", [(1, "kg"), (12, "kg"), (7, "g")],
        "Put the two masses together: 4 + 3 = 7 kg.")
    add("Siti’s ribbon is 85 cm long. Farah’s ribbon is 47 cm long. How much longer is Siti’s ribbon?",
        38, "cm", [(132, "cm"), (small_from_big(85, 47), "cm"), (38, "m")],
        "The model compares the two ribbons. Find the difference: 85 − 47 = 38 cm. "
        "Rename 1 ten as 10 ones: 15 − 7 = 8.",
        bar_compare([("Siti", 85, "85 cm"), ("Farah", 47, "47 cm")], "?"))
    add("A shop has 356 kg of rice. It sells 128 kg. How much rice is left?", 228, "kg",
        [(484, "kg"), (small_from_big(356, 128), "kg"), (228, "g")],
        "The whole is 356 kg. One part is 128 kg. The other part is 356 − 128 = 228 kg.",
        bar_parts([(128, "128 kg"), (228, "?")], "356 kg"))
    add("The school field is 95 m long. Ali runs from one end to the other end and back. How far does he run?",
        190, "m", [(95, "m"), (no_carry_add(95, 95), "m"), (190, "cm")],
        "He runs 95 m there and 95 m back: 95 + 95 = 190 m.")
    add("Each bottle holds 2 %s of water. How much water do 5 bottles hold?" % L, 10, L,
        [(7, L), (3, L), (5, L)],
        "5 units of 2 %s: 5 × 2 = 10 %s." % (L, L), bar_units(5, "2 %s" % L, "?"))
    add("Kumar pours 20 %s of water equally into 4 pails. How much water is in each pail?" % L, 5, L,
        [(16, L), (24, L), (80, L)],
        "4 units = 20 %s. 1 unit = 20 ÷ 4 = 5 %s." % (L, L), bar_units(4, "?", "20 %s" % L))
    add("A bag of flour has a mass of 500 g. Mrs Ng uses 275 g to bake a cake. How much flour is left?", 225, "g",
        [(775, "g"), (small_from_big(500, 275), "g"), (225, "kg")],
        "Flour is used, so subtract: 500 − 275 = 225 g. Rename 1 hundred as 9 tens and 10 ones.")
    add("A pail has 14 %s of water. Hafiz adds 9 %s more. How much water is in the pail now?" % (L, L), 23, L,
        [(5, L), (no_carry_add(14, 9), L), (22, L)],
        "Water is added, so add: 14 + 9 = 23 %s." % L)
    add("A blue rope is 36 m long. A red rope is 18 m longer than the blue rope. How long is the red rope?", 54, "m",
        [(18, "m"), (no_carry_add(36, 18), "m"), (54, "cm")],
        "The red rope is the longer bar: 36 + 18 = 54 m. “Longer than” means add here.",
        bar_compare([("Red", 54, "?"), ("Blue", 36, "36 m")], "18 m"))
    add("Hui Min has a mass of 26 kg. Her father is 45 kg heavier than her. What is her father’s mass?", 71, "kg",
        [(19, "kg"), (no_carry_add(26, 45), "kg"), (71, "g")],
        "Her father is the longer bar. He is heavier, so add: 26 + 45 = 71 kg.",
        bar_compare([("Father", 71, "?"), ("Hui Min", 26, "26 kg")], "45 kg"))
    add("A box of mandarin oranges has a mass of 5 kg. What is the mass of 4 such boxes?", 20, "kg",
        [(9, "kg"), (25, "kg"), (20, "g")],
        "4 units of 5 kg: 4 × 5 = 20 kg.", bar_units(4, "5 kg", "?"))
    add("Mrs Kumar puts 40 kg of rice equally into 10 bags. What is the mass of each bag?", 4, "kg",
        [(30, "kg"), (50, "kg"), (400, "kg")],
        "10 units = 40 kg. 1 unit = 40 ÷ 10 = 4 kg.")
    add("Jun Jie is 128 cm tall. Zhi Hao is 9 cm shorter than Jun Jie. How tall is Zhi Hao?", 119, "cm",
        [(137, "cm"), (small_from_big(128, 9), "cm"), (119, "m")],
        "Zhi Hao is shorter, so subtract: 128 − 9 = 119 cm. Rename 1 ten as 10 ones: 18 − 9 = 9.")
    add("A tank has 250 %s of water. 175 %s is used to water the plants. How much water is left?" % (L, L), 75, L,
        [(425, L), (small_from_big(250, 175), L), (85, L)],
        "Water is used, so subtract: 250 − 175 = 75 %s." % L)
    add("At the void deck, a table is 2 m long. Mr Rahman puts 6 tables end to end. How long is the row of tables?",
        12, "m", [(8, "m"), (4, "m"), (12, "cm")],
        "6 tables of 2 m: 6 × 2 = 12 m.")
    add("Priya buys 400 g of grapes and 350 g of cherries. What is the total mass of the fruit?", 750, "g",
        [(50, "g"), (750, "kg"), (700, "g")],
        "Put the two masses together: 400 + 350 = 750 g.")
    add("On Sports Day, each team gets 3 %s of water. How much water do 5 teams get?" % L, 15, L,
        [(8, L), (2, L), (12, L)],
        "5 teams of 3 %s: 5 × 3 = 15 %s." % (L, L))
    add("A ribbon is 15 m long. Mdm Wong cuts it into 3 equal pieces. How long is each piece?", 5, "m",
        [(12, "m"), (18, "m"), (45, "m")],
        "3 units = 15 m. 1 unit = 15 ÷ 3 = 5 m.", bar_units(3, "?", "15 m"))
    add("Xin Yi walks 450 m from her HDB block to the MRT station. Then she walks 280 m to the library. "
        "How far does she walk in all?", 730, "m", [(170, "m"), (no_carry_add(450, 280), "m"), (730, "cm")],
        "Put the two parts together: 450 + 280 = 730 m. 5 tens + 8 tens = 13 tens, so rename 10 tens as 1 hundred.",
        bar_parts([(450, "450 m"), (280, "280 m")], "?"))
    its.append(mcq("Ahmad has a rope 30 m long. He cuts it into pieces. Each piece is 5 m long. "
                   "How many pieces does he get?", "6 pieces", ["25 pieces", "35 pieces", "150 pieces"],
                   "How many 5 m are in 30 m? 30 ÷ 5 = 6 pieces.", rnd))
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
        "<h2>Three things we measure</h2>"
        "<p><b>Length</b> tells how long or tall something is: centimetres (cm) and metres (m). "
        "<b>Mass</b> tells how heavy something is: grams (g) and kilograms (kg). "
        "<b>Volume of liquid</b> tells how much water or juice there is: litres (%s).</p>" % L +
        table(["Unit", "Use it for", "About the same as"], [
            ["1 centimetre (cm)", "short things", "the width of your fingertip"],
            ["1 metre (m)", "long or tall things", "a metre stick"],
            ["1 gram (g)", "light things", "a paper clip"],
            ["1 kilogram (kg)", "heavy things", "a big bag of sugar"],
            ["1 litre (%s)" % L, "liquids", "a big carton of milk"],
        ]) +
        "<h2>Length: cm or m?</h2>"
        "<p>Use <b>cm</b> for things that fit on a ruler. Use <b>m</b> for long things like a field or a corridor. "
        "On a ruler, start at <b>0</b> and count the <b>spaces</b>.</p>"
        "<figure class='sn-fig'>" + ruler_svg(0, 7, "pencil") +
        "<figcaption>The pencil starts at 0 and ends at 7. It is 7 cm long.</figcaption></figure>"
        "<figure class='sn-fig'>" + metre_svg(3) +
        "<figcaption>The rope is as long as 3 metre sticks. It is 3 m long.</figcaption></figure>"
        "<h2>Read a scale or a container</h2>"
        "<p>Not every mark has a number. First find <b>what one mark is worth</b>. "
        "Then count on from the number before the needle.</p>"
        "<figure class='sn-fig'>" + dial_svg(650, 1000, 200, 50, "g") +
        "<figcaption>The numbers go up by 200 g. There are 4 spaces, so each mark is 50 g. "
        "The needle is 1 mark past 600: 650 g.</figcaption></figure>"
        "<figure class='sn-fig'>" + jug_svg(14, 20, 10, 2) +
        "<figcaption>The numbers go up by 10 %s. There are 5 spaces, so each line is 2 %s. "
        "The water is 2 lines above 10: 14 %s.</figcaption></figure>" % (L, L, L) +
        "<h2>Compare and order</h2>"
        "<p>Use the same unit. Compare the hundreds first, then the tens, then the ones. "
        "On a pan balance, the <b>lower pan is heavier</b>. A big object can be light.</p>"
        "<figure class='sn-fig'>" + balance_svg([OBJ["bowling ball"]], [OBJ["beach ball"]], 1, "bowling ball",
                                               "beach ball",
                                               "pan balance with a bowling ball and a beach ball, left side down") +
        "<figcaption>The bowling ball is smaller, but its pan is lower. The bowling ball is heavier.</figcaption>"
        "</figure>"
        "<h2>Word problems: draw a model</h2>"
        "<figure class='sn-fig'>" + bar_compare([("Siti", 85, "85 cm"), ("Farah", 47, "47 cm")], "?") +
        "<figcaption>Siti’s ribbon is 85 cm. Farah’s ribbon is 47 cm. The dashed part is the difference.</figcaption>"
        "</figure>" +
        ex("Example", "Siti’s ribbon is 85 cm long. Farah’s ribbon is 47 cm long. How much longer is Siti’s ribbon?",
           "“How much longer” means find the difference: 85 − 47 = 38.", "38 cm") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Counting every mark as 1 on a scale", "Find what one mark is worth first"],
            ["Reading the number after the needle", "Count on from the number before it"],
            ["Counting the numbers on a ruler, not the spaces", "From 0 to 6 there are 6 spaces: 6 cm"],
            ["Thinking a bigger object is always heavier", "Check with a balance: the lower pan is heavier"],
            ["Thinking taller water means more water", "Read the number of litres"],
            ["Leaving out the unit", "Write cm, m, g, kg or %s after the number" % L],
        ])
    )


FAQ = [
    {"q": "What is taught in P2 length, mass and volume?",
     "a": "Primary 2 students measure length in metres and centimetres, mass in kilograms and grams, and volume of "
          "liquid in litres. They read scales and containers, and compare and order the measurements."},
    {"q": "How do I teach my child to read a weighing scale?",
     "a": "First find what one mark is worth: look at the jump between two numbers and count the spaces. "
          "Then count on from the number just before the needle."},
    {"q": "What is the most common mistake?",
     "a": "Reading the scale from the wrong mark, such as counting every small mark as 1. "
          "Another is thinking that a bigger object is always heavier."},
    {"q": "Is length, mass and volume in the MOE Primary 2 syllabus?",
     "a": "Yes. It is in Measurement and Geometry of the MOE 2021 Primary Mathematics Syllabus. "
          "In Primary 3, students go on to change metres to centimetres, kilograms to grams and litres to millilitres."},
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


def mark_large(u, pattern):
    """Tag wide pictures so they print larger."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='(?:" + pattern + "))")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen_unit():
    rnd = random.Random(62809)
    sets = [set_length(rnd), set_scale(rnd), set_jug(rnd), set_compare(rnd), set_story(rnd)]
    for s in sets:
        rnd.shuffle(s["items"])
    balance(sets, rnd)
    seen = set()
    n = 0
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        pos = [0, 0, 0, 0]
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            pos[it["a"]] += 1
            assert it["q"] not in seen, it["q"]
            seen.add(it["q"])
            assert it["q"].count("<svg") <= 1
            ans = it["c"][it["a"]]
            m = re.search(r"aria-label='ruler with an? [a-z ]+ from (\d+) cm to (\d+) cm'", it["q"])
            if m:
                assert ans == "%d cm" % (int(m.group(2)) - int(m.group(1))), it["q"][-60:]
                n += 1
            m = re.search(r"aria-label='metre sticks: a [a-z]+ as long as (\d+) metre sticks'", it["q"])
            if m:
                assert ans == "%s m" % m.group(1)
                n += 1
            m = re.search(r"aria-label='(?:scale with the needle|container with [a-z ]+) at (\d+) (g|kg|ℓ)'", it["q"])
            if m and ("What is the mass?" in it["q"] or "is in the container?" in it["q"]):
                assert ans == "%s %s" % (m.group(1), m.group(2)), it["q"][-60:]
                n += 1
            m = re.search(r"aria-label='bottles: (\d+) bottles of (\d+) ℓ each'", it["q"])
            if m:
                assert ans == "%d ℓ" % (int(m.group(1)) * int(m.group(2)))
                n += 1
        assert pos == [5, 5, 5, 5], (s["title"], pos)
    assert n == 5 + 16 + 12 + 3, n
    u = {
        "country": "sg", "subject": "maths", "grade": "primary-2", "slug": "length-mass-and-volume",
        "sort": 9, "updated": UPDATED, "pdf_url": "",
        "title": "Primary 2 Length, Mass and Volume",
        "seo_title": "P2 Length, Mass and Volume Worksheets: Free Primary 2 Maths with Answers (MOE Syllabus)",
        "short_title": "Length, mass and volume",
        "domain": "Measurement and Geometry",
        "standard_code": "Primary 2: Measurement",
        "standard_url": "https://www.moe.gov.sg/primary/curriculum/syllabus",
        "standard_text": "Measuring length in metres, mass in kilograms/grams, volume of liquid in litres; "
                         "comparing and ordering",
        "meta_desc": "Free P2 maths practice: m or cm, read scales in kg and g, read containers in litres, compare "
                     "and order, word problems. 100 questions with answers.",
        "key_big": "Choose the right unit, then find what one mark is worth before you read.",
        "key_sub": "Numbers go up by 200 g with 4 spaces, so each mark is 50 g: 1 mark past 600 g is 650 g.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    assert len(u["meta_desc"]) <= 160, len(u["meta_desc"])
    return u


if __name__ == "__main__":
    u = gen_unit()
    mark_large(u, "ruler|two ribbons|metre sticks|pan balance|level pan balance|bar model|bottles|two containers")
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
