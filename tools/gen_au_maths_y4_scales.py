# -*- coding: utf-8 -*-
"""
AU Year 4 Maths: Reading Scales and Temperature (Australian Curriculum v9.0, AC9M4M01)
  python tools/gen_au_maths_y4_scales.py
HTML attributes use single quotes (no backslashes in the JSON).
Australian English, metric units, mL and L with a capital L, temperatures in °C, minus sign U+2212.
Every instrument is drawn exactly to its value, and every measurement answer is parsed back to a base unit
(mm, g, mL, s, °C) and checked in code.
Wrong answers come from real mistakes: counting marks instead of spaces, assuming each mark is 1,
not starting from 0, reading the labelled number before or after, reading below zero as above zero,
and reading a stopwatch like a clock (1:25 as 1 h 25 min or 125 s).
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "au", "maths", "year-4")
UPDATED = "2026-11-02"
GREEN = "#006633"
RED = "#c0392b"
INK = "#2b2b2b"
WATER = "#9fd3f2"
WATER_LINE = "#2a7fb8"
WOOD = "#f6e7b8"
TAPE = "#ffe27a"
GREY = "#eef1f4"
FONT = "Arial, Helvetica, sans-serif"
NBSP = " "
MINUS = "−"


# ------------------------------------------------------------ units and checking
UNIT = {"mm": ("L", 1), "cm": ("L", 10), "m": ("L", 1000), "km": ("L", 1000000),
        "g": ("M", 1), "kg": ("M", 1000), "mL": ("C", 1), "L": ("C", 1000),
        "s": ("T", 1), "min": ("T", 60), "h": ("T", 3600)}
TOK = re.compile(r"([\d" + NBSP + r"]+)\s*(" + "|".join(sorted(UNIT, key=len, reverse=True)) + r")(?![a-zA-Z])")
TEMP = re.compile("^(" + MINUS + r"?)(\d+) °C$")


def parse(s):
    """'2 kg 750 g' -> ('M', 2750); '−2 °C' -> ('D', -2). None if not a plain measurement."""
    s = s.strip()
    mt = TEMP.match(s)
    if mt:
        return "D", (-1 if mt.group(1) else 1) * int(mt.group(2))
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


def c(n):
    n = int(n)
    if n < 10000:
        return str(n)
    return "{:,}".format(n).replace(",", NBSP)


def num(n):
    """Signed number with a real minus sign."""
    return (MINUS + str(-n)) if n < 0 else str(n)


def deg(n):
    return "%s °C" % num(n)


def two(v, big, small, B):
    a, r = divmod(v, B)
    if r == 0:
        return "%s %s" % (c(a), big)
    if a == 0:
        return "%s %s" % (c(r), small)
    return "%s %s %s %s" % (c(a), big, c(r), small)


def kgg(v):
    return two(v, "kg", "g", 1000)


def lml(v):
    return two(v, "L", "mL", 1000)


def mcm(cm):
    return two(cm, "m", "cm", 100)


def cmmm(mm):
    return two(mm, "cm", "mm", 10)


def minsec(s):
    a, b = divmod(s, 60)
    if a == 0:
        return "%d s" % b
    if b == 0:
        return "%d min" % a
    return "%d min %d s" % (a, b)


def marks(k, w="mark"):
    return "%d %s%s" % (k, w, "" if k == 1 else "s")


def cap(s):
    return s[0].upper() + s[1:]


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
        if x in seen or not x or x.startswith("-"):
            continue
        pv = parse(x)
        if pc and pv and pv[0] == pc[0]:
            if pv[1] in vals:
                continue
            if pc[0] != "D" and pv[1] <= 0:
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


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def text(x, y, t, fs=17, anchor="middle", bold=True, col=INK):
    return ("<text x='%.1f' y='%.1f' font-size='%d'%s fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, " font-weight='700'" if bold else "", col, anchor, t))


# ------------------------------------------------------------ figures: ruler (mm marks)
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
    elif kind == "leaf":
        m = (a + b) / 2.0
        o.append("<path d='M%.1f 22 Q%.1f 4 %.1f 22 Q%.1f 40 %.1f 22 Z' fill='#7cc576' stroke='%s' stroke-width='1.5'/>"
                 % (a, m, b, m, a, INK))
        o.append("<line x1='%.1f' y1='22' x2='%.1f' y2='22' stroke='%s' stroke-width='1.2'/>" % (a, b, INK))
    else:  # ribbon
        o.append("<rect x='%.1f' y='15' width='%.1f' height='14' fill='%s' stroke='%s' stroke-width='1.5'/>"
                 % (a, b - a, RED, INK))
    return "".join(o)


NAMES = {"pencil": "pencil", "crayon": "crayon", "eraser": "eraser", "ribbon": "piece of ribbon", "leaf": "leaf"}


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


# ------------------------------------------------------------ figures: straight scales
def strip_svg(lo, hi, tick, lab, v, unit, kind="tape", div=1, span=400):
    """Straight scale from lo to hi (base units), a mark every `tick`, a number every `lab` (shown as val/div).
    kind: 'tape' (tape measure), 'bath' (bathroom scales window) or 'thermo' (thermometer, liquid to v).
    The pointer (or the top of the liquid) is exactly at v."""
    assert (hi - lo) % tick == 0 and lab % tick == 0 and lo % lab == 0 and hi % lab == 0 and lab % div == 0
    assert lo <= v <= hi
    n = (hi - lo) // tick
    px = float(span) / n
    X0 = 56 if kind == "thermo" else 26
    X = lambda val: X0 + px * (val - lo) / tick
    W = int(X(hi) + 46)
    o = []
    half = lab // 2 if (lab // 2) % tick == 0 and lab // tick >= 4 else None
    if kind == "thermo":
        ty, th = 24, 14                         # tube top and height
        bx, by = 26, ty + th / 2.0
        o.append("<rect x='%d' y='%d' width='%.1f' height='%d' rx='7' fill='#fff' stroke='%s' stroke-width='2'/>"
                 % (bx, ty, X(hi) + 12 - bx, th, INK))
        o.append("<circle cx='%d' cy='%.1f' r='15' fill='%s' stroke='%s' stroke-width='2'/>" % (bx, by, RED, INK))
        o.append("<rect x='%d' y='%d' width='%.1f' height='%d' fill='%s'/>" % (bx, ty + 4, X(v) - bx, th - 8, RED))
        o.append("<circle cx='%d' cy='%.1f' r='12.5' fill='%s'/>" % (bx, by, RED))
        y0 = ty + th + 3
        small, big = [], []
        for i in range(n + 1):
            val = lo + i * tick
            ln = 14 if val % lab == 0 else (10 if half and val % half == 0 else 6)
            (big if val % lab == 0 else small).append("M%.1f %dL%.1f %d" % (X(val), y0, X(val), y0 + ln))
        o.append("<path d='%s' stroke='%s' stroke-width='1.3'/>" % ("".join(small), INK))
        o.append("<path d='%s' stroke='%s' stroke-width='2.4'/>" % ("".join(big), INK))
        for val in range(lo, hi + 1, lab):
            o.append(text(X(val), y0 + 32, num(val // div), 16))
        o.append(text(X(hi) + 18, y0 + 32, "°C", 16, anchor="start", col=GREEN))
        H = y0 + 40
        label = "thermometer showing %s" % deg(v)
    else:
        top = 26
        bh = 50
        fill = TAPE if kind == "tape" else GREY
        o.append("<rect x='%.1f' y='%d' width='%.1f' height='%d' rx='4' fill='%s' stroke='%s' stroke-width='2'/>"
                 % (X(lo) - 16, top, X(hi) - X(lo) + 32, bh, fill, INK))
        small, big = [], []
        for i in range(n + 1):
            val = lo + i * tick
            ln = 20 if val % lab == 0 else (14 if half and val % half == 0 else 9)
            (big if val % lab == 0 else small).append("M%.1f %dL%.1f %d" % (X(val), top, X(val), top + ln))
        o.append("<path d='%s' stroke='%s' stroke-width='1.3'/>" % ("".join(small), INK))
        o.append("<path d='%s' stroke='%s' stroke-width='2.4'/>" % ("".join(big), INK))
        for val in range(lo, hi + 1, lab):
            o.append(text(X(val), top + 41, c(val // div), 16))
        o.append(text(X(hi) + 20, top + 41, unit, 15, anchor="start", col=GREEN))
        xv = X(v)
        o.append("<path d='M%.1f 4 L%.1f 4 L%.1f 18 Z' fill='%s'/>" % (xv - 8, xv + 8, xv, RED))
        o.append("<line x1='%.1f' y1='16' x2='%.1f' y2='%d' stroke='%s' stroke-width='2.5'/>" % (xv, xv, top + 22, RED))
        H = top + bh + 4
        what = "tape measure" if kind == "tape" else "bathroom scales"
        label = "%s with the pointer at %s" % (what, fmt_unit(v, unit, div))
    return svg_wrap(W + (14 if kind != "thermo" else 0), H, "".join(o), label)


def fmt_unit(v, unit, div):
    if unit == "cm":
        return "%s cm" % c(v)
    if unit == "m":
        return mcm(v)
    if unit == "kg":
        return kgg(v) if div == 1000 else "%s kg" % c(v)
    return "%s %s" % (c(v), unit)


# ------------------------------------------------------------ figures: dials, jugs, stopwatches
def dial_body(v, mx, lab, tick, div, size, ox=0, oy=0):
    """Round kitchen scale, values in grams. Labels every `lab` g shown as val/div. Needle exactly at v."""
    assert lab % div == 0 and lab % tick == 0 and mx % lab == 0
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


def dial_svg(v, mx, lab, tick, div=1, size=200):
    return svg_wrap(size, size, dial_body(v, mx, lab, tick, div, size),
                    "kitchen scales with the needle at %s" % kgg(v))


def dial_pair_svg(va, vb, mx, lab, tick, div=1):
    size = 180
    body = (dial_body(va, mx, lab, tick, div, size, 0, 0) + dial_body(vb, mx, lab, tick, div, size, size + 30, 0) +
            text(size / 2.0, size + 26, "A", 20) + text(size * 1.5 + 30, size + 26, "B", 20))
    return svg_wrap(size * 2 + 30, size + 34, body, "two kitchen scales: A at %s and B at %s" % (kgg(va), kgg(vb)))


def jug_svg(v, mx, lab, step, div=1, size=200):
    """Measuring jug, values in mL: a line every `step` mL, a number every `lab` mL shown as val/div (mL or L).
    Water exactly at v."""
    assert lab % div == 0 and lab % step == 0 and mx % lab == 0
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
            s.append("<text x='%d' y='%.1f'>%s</text>" % (x0 - 7, Y(val) + 5, c(val // div)))
    s.append("</g>")
    s.append(text(x0 - 7, 202, unit, 15, anchor="end", col=GREEN))
    return svg_wrap(size, size + 8, "".join(s), "measuring jug in %s with water at %s" % (unit, lml(v)))


def stopwatch_svg(sec, size=200):
    """Analog stopwatch: 60 seconds once around, a mark every second, numbers every 5 s (60 at the top)."""
    assert 0 < sec < 60
    cx = cy = size / 2.0
    R = size / 2.0 - 6

    def pt(val, r):
        ang = math.radians(6.0 * val)
        return cx + r * math.sin(ang), cy - r * math.cos(ang)
    s = ["<circle cx='%.1f' cy='%.1f' r='%.1f' fill='#fff' stroke='%s' stroke-width='6'/>" % (cx, cy, R, INK)]
    small, big = [], []
    for i in range(60):
        major = i % 5 == 0
        x1, y1 = pt(i, R - (15 if major else 9))
        x2, y2 = pt(i, R - 4)
        (big if major else small).append("M%.1f %.1fL%.1f %.1f" % (x1, y1, x2, y2))
    s.append("<path d='%s' stroke='%s' stroke-width='1.5'/>" % ("".join(small), INK))
    s.append("<path d='%s' stroke='%s' stroke-width='3'/>" % ("".join(big), INK))
    s.append("<g font-size='16' font-weight='700' fill='%s' text-anchor='middle'>" % INK)
    for k in range(1, 13):
        x, y = pt(k * 5, R - 30)
        s.append("<text x='%.1f' y='%.1f'>%d</text>" % (x, y + 6, k * 5))
    s.append("</g>")
    s.append(text(cx, cy - 32, "seconds", 14, bold=False, col=GREEN))
    nx, ny = pt(sec, R - 8)
    s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='3' stroke-linecap='round'/>"
             % (cx, cy, nx, ny, RED))
    s.append("<circle cx='%.1f' cy='%.1f' r='6' fill='%s'/>" % (cx, cy, RED))
    return svg_wrap(size, size, "".join(s), "stopwatch with the hand at %d seconds" % sec)


def digital_svg(sec):
    """Digital stopwatch showing minutes:seconds."""
    mm, ss = divmod(sec, 60)
    s = ["<rect x='3' y='3' width='214' height='104' rx='18' fill='%s' stroke='%s' stroke-width='3'/>" % (GREY, INK),
         "<rect x='22' y='16' width='176' height='62' rx='6' fill='#dfe9d6' stroke='%s' stroke-width='2'/>" % INK,
         "<text x='110' y='66' font-size='44' font-weight='700' fill='%s' text-anchor='middle' "
         "font-family='Courier New, monospace'>%02d:%02d</text>" % (INK, mm, ss),
         text(70, 98, "min", 14, bold=False, col=GREEN), text(150, 98, "s", 14, bold=False, col=GREEN)]
    return svg_wrap(220, 110, "".join(s), "digital stopwatch showing %02d:%02d" % (mm, ss))


# ------------------------------------------------------------ explanations
def read_e(v, base_lab, lab, tick, show, what="pointer", lab_show=None, tick_show=None):
    """'The numbers go up by …, there are S spaces, so each mark is …; the pointer is k marks past …'."""
    sp = lab // tick
    base = v - (v - base_lab) % lab if v >= 0 else None
    k = (v - base) // tick
    ls = lab_show or show(lab)
    ts = tick_show or show(tick)
    s = ("The numbers go up by %s. There are %d spaces between two numbers, so each mark is %s ÷ %d = %s. "
         % (ls, sp, ls, sp, ts))
    if k == 0:
        return s + "The %s is right at %s." % (what, show(v))
    return s + "Count the spaces after %s: %s. So it is %s." % (
        show(base), ", ".join(show(base + tick * i) for i in range(1, k + 1)), show(v))


# ------------------------------------------------------------ set 1: rulers and tape measures
def set_length(rnd):
    its = []
    its.append(mcq("On a ruler, how many small <b>spaces</b> are there from 3 cm to 4 cm?", "10",
                   ["9", "11", "1"],
                   "There are 9 small marks between 3 and 4, but 10 spaces. Count the spaces, not the marks. "
                   "Each space is 1 mm, and 10 mm = 1 cm.", rnd))
    # from 0
    for e_mm, kind, ansfmt, wrong in [
        (47, "crayon", cmmm, ["47 cm", "4 cm 6 mm", "5 cm", "4 cm 3 mm"]),
        (62, "pencil", cmmm, ["62 cm", "6 cm 1 mm", "7 cm", "6 cm 8 mm"]),
        (85, "ribbon", lambda x: "%d mm" % x, ["85 cm", "13 mm", "95 mm"]),
    ]:
        a, b = divmod(e_mm, 10)
        nm = NAMES[kind]
        q = fig(ruler_svg(0, e_mm, kind)) + "How long is the %s?" % nm
        e = ("It starts at 0. It ends %s past %d cm. Each small space is 1 mm, so it is %d cm %d mm = %d mm."
             % (marks(b, "small space"), a, a, b, e_mm))
        its.append(mcq(q, ansfmt(e_mm), wrong, e, rnd, want=("L", e_mm)))
    # not from 0
    for s_mm, e_mm, kind, ansfmt, wrong in [
        (20, 58, "eraser", lambda x: "%d mm" % x, ["58 mm", "48 mm", "39 mm"]),
        (30, 74, "pencil", cmmm, ["7 cm 4 mm", "4 cm 5 mm", "5 cm 4 mm"]),
        (15, 52, "crayon", lambda x: "%d mm" % x, ["52 mm", "42 mm", "38 mm"]),
        (40, 96, "ribbon", lambda x: "%d mm" % x, ["96 mm", "57 mm", "66 mm"]),
        (25, 70, "pencil", cmmm, ["7 cm", "5 cm 5 mm", "4 cm 6 mm"]),
    ]:
        ln = e_mm - s_mm
        nm = NAMES[kind]
        q = fig(ruler_svg(s_mm, e_mm, kind)) + "How long is the %s?" % nm
        e = ("It does not start at 0. It starts at %d mm and ends at %d mm. %d − %d = %d mm"
             % (s_mm, e_mm, e_mm, s_mm, ln))
        e += ", which is %s." % cmmm(ln)
        its.append(mcq(q, ansfmt(ln), wrong, e, rnd, want=("L", ln)))
    # tape measures (values in cm)
    cmf = lambda x: "%s cm" % c(x)
    for lo, hi, tick, lab, v, wrong in [
        (130, 150, 1, 10, 143, ["140 cm", "144 cm", "150 cm"]),
        (100, 160, 2, 10, 126, ["123 cm", "130 cm", "124 cm"]),
        (60, 100, 2, 10, 84, ["82 cm", "90 cm", "86 cm"]),
        (200, 300, 5, 50, 235, ["207 cm", "250 cm", "240 cm"]),
        (100, 200, 5, 50, 165, ["153 cm", "150 cm", "170 cm"]),
        (20, 60, 1, 10, 37, ["30 cm", "38 cm", "40 cm"]),
    ]:
        q = fig(strip_svg(lo, hi, tick, lab, v, "cm")) + "What does the tape measure show at the red pointer?"
        its.append(mcq(q, cmf(v), wrong, read_e(v, lo, lab, tick, cmf), rnd, want=("L", v * 10)))
    for v, wrong in [(230, ["2 m 3 cm", "3 m", "2 m 40 cm"]), (170, ["1 m 7 cm", "2 m", "1 m 60 cm"])]:
        q = (fig(strip_svg(0, 400, 10, 100, v, "m", div=100)) +
             "A long tape measure is used at the athletics carnival. What does it show at the red pointer?")
        e = ("The numbers go up by 1 m = 100 cm. There are 10 spaces between two numbers, so each mark is "
             "100 ÷ 10 = 10 cm, not 1 cm. The pointer is %s past %d m: %d m %d cm."
             % (marks((v % 100) // 10), v // 100, v // 100, v % 100))
        its.append(mcq(q, mcm(v), wrong, e, rnd, want=("L", v * 10)))
    its.append(mcq("A ruler is broken, so it starts at 4 cm. A feather goes from the 4 cm mark to the 13 cm mark. "
                   "How long is the feather?", "9 cm", ["13 cm", "17 cm", "10 cm"],
                   "It does not start at 0, so take the start away from the end: 13 − 4 = 9 cm.", rnd,
                   want=("L", 90)))
    its.append(mcq("A tape measure has the numbers 10, 20, 30, … and 5 spaces between each pair of numbers. "
                   "What is each mark worth?", "2 cm", ["1 cm", "5 cm", "10 cm"],
                   "From one number to the next is 10 cm. 10 cm shared into 5 spaces: 10 ÷ 5 = 2 cm.", rnd,
                   want=("L", 20)))
    its.append(mcq("Each small mark on a tape measure is worth 5 cm. A line ends 3 marks past 40 cm. "
                   "Where does it end?", "55 cm", ["43 cm", "45 cm", "50 cm"],
                   "Count on 3 marks of 5 cm from 40: 45, 50, 55. It ends at 55 cm.", rnd, want=("L", 550)))
    assert len(its) == 20, len(its)
    return {"title": "Rulers and tape measures with unlabelled marks", "items": its}


# ------------------------------------------------------------ set 2: kitchen and bathroom scales
def set_mass(rnd):
    its = []
    gf = lambda x: "%s g" % c(x)
    its.append(mcq("How many grams are in half a kilogram?", "500 g", ["50 g", "5 g", "100 g"],
                   "1 kg = 1000 g. Half of 1000 is 500, so half a kilogram is 500 g.", rnd, want=("M", 500)))
    for v, mx, lab, tick, obj in [
        (250, 1000, 200, 50, "a bunch of grapes"),
        (650, 1000, 200, 50, "a bag of potatoes"),
        (850, 1000, 200, 50, "a tub of yoghurt"),
        (350, 1000, 250, 50, "a block of cheese"),
        (600, 1000, 250, 50, "a bag of rice"),
        (900, 1000, 250, 50, "a bag of oranges"),
        (1300, 2000, 500, 100, "a pineapple"),
    ]:
        base = v - v % lab
        k = (v - base) // tick
        wrong = [gf(base + k), gf(base), gf(base + lab), gf(v + tick), gf(v - tick)]
        q = fig(dial_svg(v, mx, lab, tick)) + "The kitchen scales show the mass of %s. What is the mass?" % obj
        its.append(mcq(q, gf(v), wrong, read_e(v, 0, lab, tick, gf), rnd, want=("M", v)))
    its.append(mcq(fig(dial_svg(450, 1000, 200, 100)) +
                   "The needle is halfway between two marks. What is the mass of the bag of flour?",
                   "450 g", ["400 g", "500 g", "405 g"],
                   "Each mark is 200 ÷ 2 = 100 g. The needle is halfway between 400 g and 500 g. "
                   "Halfway between them is 450 g.", rnd, want=("M", 450)))
    for v, mx, tick, obj in [(2750, 5000, 250, "a bag of potting mix"), (3500, 5000, 500, "a watermelon"),
                             (1800, 3000, 100, "a bag of apples"), (4250, 5000, 250, "a bag of dog food"),
                             (2600, 3000, 100, "a pumpkin")]:
        base = v - v % 1000
        k = (v - base) // tick
        wrong = [kgg(base + k * (100 if tick != 100 else 10)), kgg(base + 1000), kgg(v - tick), kgg(base + k),
                 kgg(v + tick)]
        e = ("Each kilogram is split into %d spaces, so each mark is 1000 ÷ %d = %d g. The needle is %s past "
             "%d kg: %d × %d = %d g. So it is %s." % (1000 // tick, 1000 // tick, tick, marks(k), base // 1000,
                                                     k, tick, k * tick, kgg(v)))
        q = fig(dial_svg(v, mx, 1000, tick, 1000)) + "The scales show the mass of %s. What is the mass?" % obj
        its.append(mcq(q, kgg(v), wrong, e, rnd, want=("M", v)))
    kf = lambda x: "%s kg" % c(x)
    for lo, hi, tick, lab, v, who, wrong in [
        (20, 50, 1, 5, 33, "Jack", ["30 kg", "34 kg", "35 kg"]),
        (20, 60, 2, 10, 36, "Mia", ["33 kg", "40 kg", "38 kg"]),
        (40, 80, 5, 20, 55, "Mum", ["43 kg", "60 kg", "50 kg"]),
        (20, 40, 1, 10, 27, "Leo", ["20 kg", "28 kg", "30 kg"]),
    ]:
        q = fig(strip_svg(lo, hi, tick, lab, v, "kg", kind="bath")) + \
            "%s stands on the bathroom scales. What is %s mass?" % (who, "her" if who in ("Mia", "Mum") else "his")
        its.append(mcq(q, kf(v), wrong, read_e(v, lo, lab, tick, kf), rnd, want=("M", v * 1000)))
    q = fig(strip_svg(30000, 40000, 500, 5000, 32500, "kg", kind="bath", div=1000)) + \
        "Sienna stands on the bathroom scales. What is her mass?"
    its.append(mcq(q, "32 kg 500 g", ["35 kg", "32 kg", "33 kg", "32 kg 5 g"],
                   "From 30 kg to 35 kg there are 10 spaces, so each mark is 5000 g ÷ 10 = 500 g, not 1 kg. "
                   "The pointer is 5 marks past 30 kg: 5 × 500 g = 2500 g = 2 kg 500 g. "
                   "30 kg + 2 kg 500 g = 32 kg 500 g.", rnd, want=("M", 32500)))
    its.append(mcq("Kitchen scales have a mark every 250 g. The needle is 3 marks past 1 kg. What is the mass?",
                   "1 kg 750 g", ["1 kg 3 g", "1 kg 300 g", "1 kg 500 g"],
                   "Each mark is 250 g, not 1 g. 3 marks: 250, 500, 750. So it is 1 kg 750 g.", rnd,
                   want=("M", 1750)))
    assert len(its) == 20, len(its)
    return {"title": "Kitchen and bathroom scales: g and kg", "items": its}


# ------------------------------------------------------------ set 3: jugs
def set_capacity(rnd):
    its = []
    mf = lambda x: "%s mL" % c(x)
    its.append(mcq("A jug has a line every 250 mL. How many <b>spaces</b> are there from 0 up to 1 L?", "4",
                   ["5", "3", "250"],
                   "1 L = 1000 mL. Count by 250: 250, 500, 750, 1000. That is 4 spaces. "
                   "Do not count the 0 line as a space.", rnd))
    for v, mx, lab, step in [(350, 1000, 200, 50), (650, 1000, 200, 50), (400, 1000, 250, 50),
                             (850, 1000, 250, 50), (175, 500, 100, 25), (325, 500, 100, 25)]:
        base = v - v % lab
        k = (v - base) // step
        wrong = [mf(base + k), mf(base), mf(base + lab), mf(v + step), mf(v - step)]
        q = fig(jug_svg(v, mx, lab, step)) + "How much water is in the jug?"
        its.append(mcq(q, mf(v), wrong, read_e(v, 0, lab, step, mf, what="water"), rnd, want=("C", v)))
    for v, lo in [(550, 500), (250, 200)]:
        q = fig(jug_svg(v, 1000, 200, 100)) + "The water is halfway between two lines. How much water is in the jug?"
        its.append(mcq(q, mf(v), [mf(lo), mf(lo + 100), mf(lo + 5), mf(lo + 10)],
                       "The numbers go up by 200 mL with 2 spaces, so each line is 100 mL. The water is halfway "
                       "between %d mL and %d mL. Halfway is %d mL." % (lo, lo + 100, v), rnd, want=("C", v)))
    for v, mx, step in [(1250, 2000, 250), (1750, 2000, 250), (1400, 2000, 100), (2500, 3000, 500),
                        (2750, 3000, 250), (600, 2000, 200)]:
        base = v - v % 1000
        k = (v - base) // step
        wrong = [lml(base + k * (100 if step != 100 else 10)), lml(base + 1000), lml(v - step), lml(base + k),
                 lml(v + step)]
        if base:
            e = ("Each litre is split into %d spaces, so each line is 1000 ÷ %d = %d mL. The water is %s above "
                 "%d L: %d × %d = %d mL. So it is %s." % (1000 // step, 1000 // step, step, marks(k, "line"),
                                                         base // 1000, k, step, k * step, lml(v)))
        else:
            e = ("Each litre is split into %d spaces, so each line is 1000 ÷ %d = %d mL. The water is %s up from "
                 "the bottom: %d × %d = %d mL. It has not reached 1 L." % (1000 // step, 1000 // step, step,
                                                                         marks(k, "line"), k, step, v))
        q = fig(jug_svg(v, mx, 1000, step, 1000)) + "How much water is in the jug?"
        its.append(mcq(q, lml(v), wrong, e, rnd, want=("C", v)))
    its.append(mcq(fig(jug_svg(1750, 2000, 1000, 250, 1000)) + "How much more water is needed to fill the jug to 2 L?",
                   "250 mL", ["750 mL", "1 L 250 mL", "350 mL"],
                   "Each line is 250 mL, so the water is at 1 L 750 mL. One more line reaches 2 L. "
                   "So 250 mL more is needed.", rnd, want=("C", 250)))
    its.append(mcq(fig(jug_svg(350, 1000, 200, 50)) + "Cooper pours in 150 mL more water. "
                   "How much water will be in the jug?", "500 mL", ["200 mL", "450 mL", "550 mL"],
                   "Each line is 50 mL, so the water is at 350 mL now. Pouring in means add: 350 + 150 = 500 mL.",
                   rnd, want=("C", 500)))
    its.append(mcq("Which amount is the same as 1500 mL?", "1 L 500 mL", ["15 L", "1 L 50 mL", "150 L"],
                   "1000 mL = 1 L. 1500 mL = 1000 mL + 500 mL = 1 L 500 mL.", rnd, want=("C", 1500)))
    its.append(mcq("A jug has lines every 250 mL. The water is halfway between the 500 mL line and the 1 L line. "
                   "How much water is in the jug?", "750 mL", ["550 mL", "600 mL", "1 L 500 mL"],
                   "From 500 mL to 1000 mL is 500 mL. Half of 500 is 250. 500 + 250 = 750 mL.", rnd,
                   want=("C", 750)))
    its.append(mcq("A jug has a line every 100 mL. The water is 4 lines above 1 L. How much water is in the jug?",
                   "1 L 400 mL", ["1 L 4 mL", "1 L 40 mL", "5 L"],
                   "Each line is 100 mL, not 1 mL. 4 × 100 = 400 mL. So it is 1 L 400 mL.", rnd, want=("C", 1400)))
    assert len(its) == 20, len(its)
    return {"title": "Jugs with partial marks: mL and L", "items": its}


# ------------------------------------------------------------ set 4: thermometers and stopwatches
def set_temp_time(rnd):
    its = []
    for lo, hi, tick, lab, v, where in [
        (10, 40, 1, 10, 23, "in the classroom"),
        (10, 40, 1, 5, 17, "on an autumn afternoon"),
        (0, 50, 2, 10, 34, "on a hot day in Sydney"),
        (0, 50, 2, 10, 26, "at the beach"),
        (20, 45, 1, 5, 38, "on a summer afternoon in Perth"),
        (-10, 20, 1, 5, 8, "on a winter morning in Melbourne"),
    ]:
        base = v - (v - lo) % lab
        k = (v - base) // tick
        wrong = [deg(base + k * (2 if tick == 1 else 1)), deg(base), deg(base + lab), deg(v + tick), deg(v - tick)]
        q = fig(strip_svg(lo, hi, tick, lab, v, "°C", kind="thermo")) + "What temperature does the thermometer show %s?" % where
        e = read_e(v, lo, lab, tick, deg, what="red line", lab_show="%d degrees" % lab,
                   tick_show="%d degree%s" % (tick, "" if tick == 1 else "s"))
        its.append(mcq(q, deg(v), wrong, e, rnd, want=("D", v)))
    q = fig(strip_svg(-10, 10, 1, 5, -2, "°C", kind="thermo")) + "What temperature does the thermometer show on a frosty morning?"
    its.append(mcq(q, deg(-2), [deg(2), deg(-3), deg(-5), deg(-1)],
                   "The red line ends before 0, so the temperature is below zero. Count back from 0: 2 marks "
                   "of 1 degree. It is " + deg(-2) + ", not 2 °C.", rnd, want=("D", -2)))
    q = fig(strip_svg(-10, 10, 2, 10, -4, "°C", kind="thermo")) + "What temperature does the thermometer show?"
    its.append(mcq(q, deg(-4), [deg(4), deg(-2), deg(-6)],
                   "Each mark is 10 ÷ 5 = 2 degrees. The red line ends 2 marks before 0: 2 × 2 = 4. "
                   "It is below zero, so it is " + deg(-4) + ".", rnd, want=("D", -4)))
    its.append(mcq("Which temperature is the coldest?", deg(-2), [deg(0), deg(2), deg(5)],
                   "Temperatures below zero are colder than 0 °C. " + deg(-2) + " is 2 degrees below zero, "
                   "so it is the coldest.", rnd, want=("D", -2)))
    its.append(mcq("Which temperature is 2 degrees <b>below</b> zero?", deg(-2), [deg(2), deg(-20), deg(20)],
                   "Below zero temperatures have a minus sign. 2 degrees below zero is written " + deg(-2) + ". "
                   "2 °C is 2 degrees above zero.", rnd, want=("D", -2)))
    its.append(mcq("It is 3 °C in the evening. Overnight the temperature drops by 5 degrees. What is it now?",
                   deg(-2), [deg(2), deg(8), deg(-8)],
                   "Count down 5 degrees from 3: 2, 1, 0, " + deg(-1) + ", " + deg(-2) + ". "
                   "It goes below zero, so it is " + deg(-2) + ", not 2 °C.", rnd, want=("D", -2)))
    sf = lambda x: "%d s" % x
    for v in [17, 43, 28, 52, 36, 9]:
        base = v - v % 5
        q = fig(stopwatch_svg(v)) + "The stopwatch measures how long a race takes. How many seconds does it show?"
        e = ("The numbers go up by 5 seconds, and each small mark is 1 second. The hand is %s past %d: "
             "%d + %d = %d seconds." % (marks(v - base), base, base, v - base, v)) if base else \
            ("Each small mark is 1 second. The hand is %s past the top, so it shows %d seconds." % (marks(v), v))
        wrong = [sf(base + 5), sf(v + 1), sf(v - 1), sf(base)] if base else [sf(v + 1), sf(v - 1), sf(v + 5)]
        its.append(mcq(q, sf(v), wrong, e, rnd, want=("T", v)))
    its.append(mcq(fig(digital_svg(85)) + "The digital stopwatch shows minutes and seconds. How long does it show?",
                   "1 min 25 s", ["1 h 25 min", "125 s", "12 min 5 s"],
                   "On a stopwatch the number before the colon is minutes and the number after it is seconds. "
                   "01:25 is 1 min 25 s, not 1 hour.", rnd, want=("T", 85)))
    its.append(mcq(fig(digital_svg(125)) + "How long does the digital stopwatch show?",
                   "2 min 5 s", ["2 h 5 min", "205 s", "2 min 50 s"],
                   "Minutes come before the colon and seconds after it. 02:05 is 2 min 5 s. "
                   "05 is 5 seconds, not 50.", rnd, want=("T", 125)))
    its.append(mcq(fig(digital_svg(90)) + "How many seconds altogether does the stopwatch show?",
                   "90 s", ["130 s", "30 s", "60 s"],
                   "01:30 is 1 min 30 s. 1 min = 60 s, so 60 + 30 = 90 s. It is not 130 s, because "
                   "1 minute is 60 seconds, not 100.", rnd, want=("T", 90)))
    assert len(its) == 20, len(its)
    return {"title": "Thermometers (°C) and stopwatches", "items": its}


# ------------------------------------------------------------ set 5: compare measures and word problems
def set_story(rnd):
    its = []

    def add(q, r, w, e, want=None):
        its.append(mcq(q, r, w, e, rnd, want=want))

    for q, ch, ans, e in [
        ("Which is the heaviest?", ["1 kg 500 g", "1300 g", "1 kg 50 g", "1450 g"], "1 kg 500 g",
         "Change them all to grams: 1 kg 500 g = 1500 g and 1 kg 50 g = 1050 g. 1500 g is the most. "
         "Do not compare only the numbers 1 and 1450."),
        ("Which is the longest?", ["1 m 20 cm", "150 cm", "1 m 5 cm", "115 cm"], "150 cm",
         "Change them all to centimetres: 1 m 20 cm = 120 cm and 1 m 5 cm = 105 cm. 150 cm is the longest."),
        ("Which holds the most?", ["1 L 250 mL", "1500 mL", "1 L 50 mL", "1400 mL"], "1500 mL",
         "Change them all to millilitres: 1 L 250 mL = 1250 mL and 1 L 50 mL = 1050 mL. 1500 mL is the most."),
    ]:
        vals = [parse(x)[1] for x in ch]
        assert len(set(vals)) == 4 and parse(ans)[1] == max(vals)
        add(q, ans, [x for x in ch if x != ans], e)
    add(fig(dial_pair_svg(2750, 3250, 5000, 1000, 250, 1000)) +
        "Two bags of potatoes are on the scales. Which bag is heavier, and by how much?",
        "B, by 500 g", ["A, by 500 g", "B, by 1 kg", "B, by 250 g"],
        "Each mark is 1000 ÷ 4 = 250 g. A shows 2 kg 750 g and B shows 3 kg 250 g. B is heavier. "
        "From 2 kg 750 g to 3 kg is 250 g, and to 3 kg 250 g is 250 g more: 500 g.")
    order = [-2, 0, 3]
    add("Which list goes from the coldest to the warmest?", ", ".join(deg(t) for t in order),
        [", ".join(deg(t) for t in o) for o in ([0, -2, 3], [3, 0, -2], [-2, 3, 0])],
        "Below zero is colder than 0 °C. " + deg(-2) + " is the coldest, then 0 °C, then 3 °C.")
    add("At the swimming carnival, Ruby’s stopwatch shows 00:58. Kai’s stopwatch shows 01:02. "
        "Who is faster, and by how much?", "Ruby, by 4 s", ["Kai, by 4 s", "Ruby, by 44 s", "Kai, by 44 s"],
        "00:58 is 58 s. 01:02 is 1 min 2 s = 62 s. The smaller time is faster, so Ruby wins. 62 − 58 = 4 s.")
    add("On a winter morning in Canberra it is " + deg(-2) + " at 7 am. By 2 pm it is 12 °C. "
        "How many degrees warmer is it at 2 pm?", "14 degrees", ["10 degrees", "12 degrees", "2 degrees"],
        "Count up from " + deg(-2) + " to 0: 2 degrees. Then 0 to 12: 12 degrees. 2 + 12 = 14 degrees.")
    add("On a summer day in Perth it is 38 °C at 3 pm. At midnight it is 21 °C. How many degrees cooler is it "
        "at midnight?", "17 degrees", ["59 degrees", "21 degrees", "18 degrees"],
        "Cooler means find the difference: 38 − 21 = 17 degrees. Check: 21 + 17 = 38.")
    add("Mum stands on the bathroom scales: 62 kg. Then she picks up the dog and the scales show 71 kg. "
        "What is the mass of the dog?", "9 kg", ["133 kg", "11 kg", "19 kg"],
        "The dog’s mass is the difference: 71 − 62 = 9 kg.", ("M", 9000))
    add("The school canteen buys 2 kg 500 g of onions for the sausage sizzle. They use 1 kg 750 g. "
        "How much is left?", "750 g", ["1 kg 250 g", "4 kg 250 g", "850 g"],
        "Change to grams: 2500 − 1750 = 750 g. Do not take 500 from 750: the grams part needs regrouping.",
        ("M", 750))
    add("A jug holds 1 L 500 mL of cordial. Six cups of 200 mL are poured for a picnic. How much cordial is "
        "left in the jug?", "300 mL", ["1 L 200 mL", "1 L 300 mL", "2 L 700 mL"],
        "6 × 200 = 1200 mL poured. 1 L 500 mL = 1500 mL. 1500 − 1200 = 300 mL left.", ("C", 300))
    add("At the athletics carnival, Lachlan jumps 2 m 45 cm and Isla jumps 2 m 70 cm. How much further does "
        "Isla jump?", "25 cm", ["35 cm", "5 m 15 cm", "75 cm"],
        "The metres are the same, so compare the centimetres: 70 − 45 = 25 cm.", ("L", 250))
    add("Kai’s pencil is 14 cm 5 mm long. Zara’s pencil is 12 cm 8 mm long. How much longer is Kai’s pencil?",
        "1 cm 7 mm", ["2 cm 3 mm", "1 cm 3 mm", "27 cm 3 mm"],
        "Change to millimetres: 145 − 128 = 17 mm = 1 cm 7 mm. Do not take 5 from 8 the wrong way round: regroup 1 cm as 10 mm.",
        ("L", 17))
    add("Leo runs 3 laps of the oval. Each lap takes 40 s. How long does he run altogether?", "2 min",
        ["1 min 20 s", "120 min", "43 s"],
        "3 × 40 = 120 s. 60 s = 1 min, so 120 s = 2 min. 1 min 20 s is wrong: 1 minute is 60 s, not 100 s.",
        ("T", 120))
    add("The kitchen scales show 450 g of flour. The Anzac biscuit recipe needs 1 kg. How much more flour is "
        "needed?", "550 g", ["650 g", "1 kg 450 g", "450 g"],
        "1 kg = 1000 g. 1000 − 450 = 550 g. Check: 450 + 550 = 1000.", ("M", 550))
    add(fig(strip_svg(15, 35, 1, 5, 23, "°C", kind="thermo")) +
        "The pool must be at least 26 °C for the swimming carnival. How many degrees warmer does the water "
        "need to be?", "3 degrees", ["2 degrees", "4 degrees", "49 degrees"],
        "The thermometer shows 23 °C: each mark is 1 degree and the red line is 3 marks past 20. "
        "26 − 23 = 3 degrees.")
    add(fig(strip_svg(150, 200, 2, 10, 176, "cm")) +
        "A sunflower in the school garden is measured with a tape measure. How much more must it grow to "
        "be 2 m tall?", "24 cm", ["27 cm", "34 cm", "176 cm"],
        "Each mark is 10 ÷ 5 = 2 cm. The pointer is 3 marks past 170: 176 cm. 2 m = 200 cm. "
        "200 − 176 = 24 cm.", ("L", 240))
    add("A watering can holds 9 L. A jug holds 1 L 500 mL. How many full jugs fill the watering can?", "6",
        ["9", "5", "8"],
        "Count by 1 L 500 mL: 1 L 500 mL, 3 L, 4 L 500 mL, 6 L, 7 L 500 mL, 9 L. That is 6 jugs.")
    add("A bunch of bananas has a mass of 1 kg 200 g. Another bunch has a mass of 950 g. What is their total "
        "mass?", "2 kg 150 g", ["2 kg 50 g", "1 kg 150 g", "2 kg 250 g"],
        "Change to grams: 1200 + 950 = 2150 g = 2 kg 150 g.", ("M", 2150))
    add("Charlotte has 1 m of ribbon. She cuts off a 35 cm piece and a 40 cm piece. How much ribbon is left?",
        "25 cm", ["75 cm", "35 cm", "65 cm"],
        "1 m = 100 cm. She cuts 35 + 40 = 75 cm. 100 − 75 = 25 cm left.", ("L", 250))
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
        "<h2>Find what one mark is worth</h2>"
        "<p>Most marks on a scale have no number. Before you read it, work out <b>what one mark is worth</b>.</p>"
        "<p>1. Find two numbers next to each other. 2. Count the <b>spaces</b> between them (not the marks). "
        "3. Divide: the jump ÷ the number of spaces.</p>" +
        table(["Numbers go up by", "Spaces between", "Each mark is worth"], [
            ["10 cm", "5", "10 ÷ 5 = 2 cm"],
            ["200 g", "4", "200 ÷ 4 = 50 g"],
            ["1 kg (1000 g)", "4", "1000 ÷ 4 = 250 g"],
            ["1 L (1000 mL)", "10", "1000 ÷ 10 = 100 mL"],
            ["10 °C", "10", "10 ÷ 10 = 1 degree"],
        ]) +
        "<h2>Rulers: start at 0</h2>"
        "<p>If an object does not start at 0, take the start away from the end.</p>"
        "<figure class='sn-fig'>" + ruler_svg(20, 58, "eraser") +
        "<figcaption>The eraser goes from 20 mm to 58 mm. 58 − 20 = 38 mm, which is 3 cm 8 mm.</figcaption></figure>"
        "<h2>Scales and jugs</h2>"
        "<figure class='sn-fig'>" + dial_svg(650, 1000, 200, 50) +
        "<figcaption>The numbers go up by 200 g with 4 spaces, so each mark is 50 g. "
        "The needle is 1 mark past 600: 650 g.</figcaption></figure>"
        "<figure class='sn-fig'>" + jug_svg(1750, 2000, 1000, 250, 1000) +
        "<figcaption>Each litre has 4 spaces, so each line is 250 mL. The water is 3 lines above 1 L: "
        "1 L 750 mL (1750 mL).</figcaption></figure>"
        "<p>If the needle or water is <b>halfway</b> between two marks, the answer is halfway between their values. "
        "Halfway between 500 mL and 600 mL is 550 mL.</p>"
        "<h2>Thermometers and temperatures below zero</h2>"
        "<p>We measure temperature in degrees Celsius (°C). Water freezes at 0 °C. A temperature below zero "
        "has a minus sign: " + deg(-2) + " is 2 degrees colder than 0 °C.</p>"
        "<figure class='sn-fig'>" + strip_svg(-10, 10, 1, 5, -2, "°C", kind="thermo") +
        "<figcaption>The red line ends 2 marks before 0, so it shows " + deg(-2) + ".</figcaption></figure>"
        "<h2>Stopwatches</h2>"
        "<p>An analog stopwatch goes once around in 60 seconds. A digital stopwatch shows minutes, then a colon, "
        "then seconds: 01:25 is 1 min 25 s. Remember 1 min = 60 s.</p>"
        "<figure class='sn-fig'>" + stopwatch_svg(43) +
        "<figcaption>The hand is 3 marks past 40, so it shows 43 seconds.</figcaption></figure>" +
        ex("Compare", "Which is heavier: 1 kg 500 g or 1300 g?",
           "Change to the same unit: 1 kg 500 g = 1500 g. 1500 g is more than 1300 g.", "1 kg 500 g") +
        ex("How much warmer?", "It is " + deg(-2) + " in the morning and 12 °C in the afternoon.",
           "From " + deg(-2) + " up to 0 is 2 degrees. From 0 up to 12 is 12 degrees. 2 + 12 = 14.", "14 degrees") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Counting the marks instead of the spaces", "Count the spaces (jumps) between two numbers"],
            ["Thinking every mark is worth 1", "Work out what one mark is worth first: jump ÷ spaces"],
            ["Reading the end of an object that does not start at 0", "Take the start away from the end"],
            ["Reading " + deg(-2) + " as 2 °C", "Below 0, count back from 0 and write the minus sign"],
            ["Reading 01:25 on a stopwatch as 1 hour 25 minutes or 125 seconds",
             "It is 1 min 25 s, and 1 min = 60 s, so 85 s"],
        ])
    )


FAQ = [
    {"q": "What does Year 4 measurement cover in the Australian Curriculum?",
     "a": "Year 4 students read scaled and digital instruments where not every mark is labelled, including rulers, "
          "tape measures, kitchen and bathroom scales, jugs, thermometers in °C and stopwatches, and they compare "
          "length, mass, capacity, duration and temperature."},
    {"q": "How do you read a scale with unlabelled marks?",
     "a": "Find two numbers next to each other, count the spaces between them and divide the jump by the number of "
          "spaces. That tells you what each mark is worth, so you can count on from the number before."},
    {"q": "Do Year 4 students learn negative temperatures?",
     "a": "Yes, in a simple way. They read thermometers in °C, including temperatures just below zero such as "
          + deg(-2) + ", which is 2 degrees colder than 0 °C."},
    {"q": "Is reading scales tested in NAPLAN?",
     "a": "Year 4 does not sit NAPLAN, but reading scales and instruments is part of the Year 5 NAPLAN numeracy "
          "test, so Year 4 is a good time to practise it."},
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
    rnd = random.Random(4812)
    sets = [set_length(rnd), set_mass(rnd), set_capacity(rnd), set_temp_time(rnd), set_story(rnd)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        pos = [0, 0, 0, 0]
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            vals = [parse(x) for x in it["c"]]
            if all(vals):
                assert len(set(vals)) == 4, it["c"]
            pos[it["a"]] += 1
            k = it["q"] + "|" + "|".join(sorted(it["c"]))
            assert k not in seen, it["q"]
            seen.add(k)
            assert it["q"].count("<svg") <= 1
        assert pos == [5, 5, 5, 5], (s["title"], pos)
    return {
        "country": "au", "subject": "maths", "grade": "year-4", "slug": "reading-scales-and-temperature", "sort": 12,
        "updated": UPDATED, "pdf_url": "",
        "title": "Reading Scales and Temperature",
        "seo_title": "Year 4 Reading Scales and Temperature Worksheets (Free, with Answer Key)",
        "short_title": "Reading scales and temperature",
        "domain": "Measurement",
        "standard_code": "AC9M4M01",
        "standard_url": "https://v9.australiancurriculum.edu.au/f-10-curriculum/learning-areas/mathematics",
        "standard_text": "Interpret unmarked and partial units when measuring and comparing attributes of length, "
                         "mass, capacity, duration and temperature, using scaled and digital instruments",
        "meta_desc": "Free Year 4 maths worksheets on reading scales: rulers and tape measures, kitchen and bathroom "
                     "scales, measuring jugs, thermometers in °C (including below zero) and stopwatches, with "
                     "unlabelled marks. 100 questions with an answer key, matched to the Australian Curriculum.",
        "key_big": "Count the spaces between two numbers to find what one mark is worth.",
        "key_sub": "Jump ÷ spaces = one mark. Start at 0, count on from the number before, and write a minus sign "
                   "for temperatures below zero.",
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
    for p in ("ruler", "tape measure", "bathroom scales", "thermometer", "two kitchen scales"):
        mark_large(u, p)
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
