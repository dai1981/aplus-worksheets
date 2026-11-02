# -*- coding: utf-8 -*-
"""
CA Grade 6 Math: Metric Units and Time (Ontario Curriculum 2020, Spatial Sense E2)
  python3 tools/gen_ca_math_g6_metric_time.py
Convert between mm, cm, m and km, g and kg, and mL and L with decimals; choose the unit (including square
units for area); elapsed time across hours on the 12-hour clock (a.m./p.m.); Canadian word problems
(Terry Fox Run, maple syrup, hockey, canoe trips, a Toronto to Vancouver flight).
Every measurement answer is parsed back to a base unit (mm, g, mL) and checked in code; every time is worked
out in minutes since midnight.
Wrong answers come from real mistakes: multiplying by 100 for kg, g, mL or L, moving the point the wrong way,
3 kg 40 g = 3.4 kg, reading a ruler from 0 when the object starts at 1 cm, an hour counted as 100 minutes,
forgetting to carry an hour, and mixing up a.m. and p.m.
Canadian English and Ontario number style (4 digits plain, 5 or more digits with a no-break space).
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, math, os, random, re
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-6")
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



# ------------------------------------------------------------ time
DAY = 24 * 60


def T(h, mi, half):
    """T(7, 25, 'pm') -> minutes since midnight."""
    assert 1 <= h <= 12 and 0 <= mi < 60
    return (h % 12) * 60 + mi + (720 if half == "pm" else 0)


def f12(t):
    t %= DAY
    if t == 720:
        return "12:00 noon"
    assert t != 0, "no midnight times"
    h = t // 60
    return "%d:%02d %s" % ((h - 1) % 12 + 1, t % 60, "a.m." if h < 12 else "p.m.")


def mins(n):
    return "%d minute%s" % (n, "" if n == 1 else "s")


def dur(n):
    assert n > 0
    hh, mm = divmod(n, 60)
    parts = []
    if hh:
        parts.append("%d hour%s" % (hh, "" if hh == 1 else "s"))
    if mm:
        parts.append(mins(mm))
    return " ".join(parts)


def raw_dur(hh, mm):
    """'1 hour 75 minutes' style (for the 100-minutes-in-an-hour mistake)."""
    if hh <= 0 and mm <= 0:
        return None
    if hh <= 0:
        return mins(mm)
    return "%d hour%s" % (hh, "" if hh == 1 else "s") + (" " + mins(mm) if mm else "")


def dur_value(s):
    v = 0
    for n_, unit in re.findall(r"(\d+) (hour|minute)", s):
        v += int(n_) * (60 if unit == "hour" else 1)
    return v


def clock_num(t):
    """12-hour clock reading as a number: 2:05 p.m. -> 205."""
    t %= DAY
    h = (t // 60 - 1) % 12 + 1
    return h * 100 + t % 60


def naive100(t1, t2):
    """Subtracting the clock numbers as if an hour had 100 minutes: 9:40 to 11:15 -> 1115 - 940 = 175."""
    k = clock_num(t2) - clock_num(t1)
    if k <= 0:
        return None
    return raw_dur(k // 100, k % 100)


def mm_wrong_way(t1, t2):
    """Hours subtracted, then the smaller minutes taken from the bigger: 2:50 to 4:05 -> 2 hours 45 minutes."""
    hh = t2 // 60 - t1 // 60
    mm = abs(t2 % 60 - t1 % 60)
    return raw_dur(hh, mm)


def jumps(t1, t2):
    pts = [t1]
    a = -(-t1 // 60) * 60
    if t1 < a <= t2:
        pts.append(a)
    b = (t2 // 60) * 60
    if b > pts[-1]:
        pts.append(b)
    if t2 > pts[-1]:
        pts.append(t2)
    return pts


def jump_label(n_):
    hh, mm = divmod(n_, 60)
    if not hh:
        return "+%d min" % mm
    if not mm:
        return "+%d h" % hh
    return "+%d h %d min" % (hh, mm)


def timeline_svg(t1, t2, W=470):
    """Open number line (not to scale): equal spaces, each jump labelled."""
    pts = jumps(t1, t2)
    L, R, Y = 50, W - 50, 72
    n_ = len(pts) - 1

    def X(i):
        return L + (R - L) * i / float(n_)
    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2.5'/>" % (L, Y, R, Y, INK)]
    for i, t in enumerate(pts):
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='2.5'/>"
                 % (X(i), Y - 10, X(i), Y + 10, INK))
        s.append(text(X(i), Y + 32, f12(t), 15))
    for i in range(n_):
        x1, x2 = X(i), X(i + 1)
        s.append("<path d='M%.1f %d Q%.1f %d %.1f %d' fill='none' stroke='%s' stroke-width='2.5'/>"
                 % (x1 + 4, Y - 12, (x1 + x2) / 2, Y - 54, x2 - 4, Y - 12, RED))
        s.append(text((x1 + x2) / 2, Y - 40, jump_label(pts[i + 1] - pts[i]), 15, col=RED))
    return svg_wrap(W, 114, "".join(s), "time line from %s to %s" % (f12(t1), f12(t2)))


def count_on(t1, t2):
    pts = jumps(t1, t2)
    parts = ["%s to %s is %s" % (f12(a), f12(b), dur(b - a)) for a, b in zip(pts, pts[1:])]
    d = t2 - t1
    if len(parts) == 1:
        return "Count on: %s. So it is <b>%s</b>." % (parts[0], dur(d))
    terms = [dur(b - a) for a, b in zip(pts, pts[1:])]
    hrs = [x for x in terms if "minute" not in x]
    mns = [x for x in terms if "minute" in x]
    return "Count on: %s. %s = <b>%s</b>." % ("; ".join(parts), " + ".join(hrs + mns), dur(d))


def tidy(s):
    return s.replace("a.m..", "a.m.").replace("p.m..", "p.m.")


def tmcq(q, correct, cands, e, rnd):
    """Choices are strings; values must all differ (durations by minutes, times by text)."""
    key = dur_value if ("hour" in correct or "minute" in correct) else (lambda x: x)
    seen = {key(correct)}
    pick = []
    for x in cands:
        if not x or key(x) in seen:
            continue
        seen.add(key(x))
        pick.append(x)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    ch = pick + [correct]
    rnd.shuffle(ch)
    return {"q": q, "c": ch, "a": ch.index(correct), "e": tidy(e)}


def dur_q(q, t1, t2, rnd, extra=(), note="", hundred=True):
    d = t2 - t1
    assert d > 0
    cands = list(extra)
    nv = naive100(t1, t2) if t2 < DAY and (t1 < 720) == (t2 < 720) else None
    if hundred and nv:
        cands.append(nv)
    if t2 < DAY:
        cands.append(mm_wrong_way(t1, t2))
    for k in (60, -60, 10, -10, 20, -20):
        if d + k > 0:
            cands.append(dur(d + k))
    e = note + count_on(t1, t2)
    if nv and dur_value(nv) != d:
        e += " (An hour has 60 minutes, not 100, so you cannot just subtract the clock numbers.)"
    return tmcq(q, dur(d), cands, e, rnd)


def add_e(t, d):
    """Explanation for t + d: add the hours, then count on the minutes through the next o'clock."""
    hh, mm = divmod(d, 60)
    s, cur = [], t
    if hh:
        s.append("Add %s: %s + %s = %s." % ("%d hour%s" % (hh, "" if hh == 1 else "s"), f12(cur),
                                            "%d h" % hh, f12(cur + hh * 60)))
        cur += hh * 60
    if mm:
        to_next = 60 - cur % 60
        if mm > to_next:
            s.append(("Then add" if s else "Add") + " %s: %s takes you to %s, and %s more is %s." % (
                mins(mm), mins(to_next), f12(cur + to_next), mins(mm - to_next), f12(cur + mm)))
        else:
            s.append(("Then add" if s else "Add") + " %s: %s." % (mins(mm), f12(cur + mm)))
    return tidy(" ".join(s))


def back_e(t, d):
    """Explanation for t - d: count back the hours, then the minutes through the o'clock."""
    hh, mm = divmod(d, 60)
    s, cur = [], t
    if hh:
        s.append("Count back %s: %s." % ("%d hour%s" % (hh, "" if hh == 1 else "s"), f12(cur - hh * 60)))
        cur -= hh * 60
    if mm:
        back = cur % 60
        if mm > back:
            s.append(("Then count back" if s else "Count back") + " %s: %s takes you to %s, and %s more is %s." % (
                mins(mm), mins(back), f12(cur - back), mins(mm - back), f12(cur - mm)))
        else:
            s.append(("Then count back" if s else "Count back") + " %s: %s." % (mins(mm), f12(cur - mm)))
    return tidy(" ".join(s))


def flip(t):
    return (t + 720) % DAY


# ------------------------------------------------------------ set 1: length
def set_length(rnd):
    its = []
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
    q = fig(ruler_svg(0, 83, "pencil", 9)) + "How long is the pencil in centimetres?"
    its.append(mcq(q, "8.3 cm", ["83 cm", "0.83 cm", "8.03 cm"],
                   "The pencil ends 3 small marks after 8 cm. Each small mark is 1 mm, so it is 83 mm. "
                   "1 cm = 10 mm, so 83 ÷ 10 = 8.3 cm.", rnd, want=("L", 83)))
    q = fig(ruler_svg(10, 76, "crayon", 8)) + "How long is the crayon in centimetres?"
    its.append(mcq(q, "6.6 cm", ["7.6 cm", "66 cm", "6.06 cm"],
                   "The crayon starts at 1 cm, not at 0. It ends 6 small marks after 7 cm, at 7.6 cm. "
                   "7.6 − 1 = 6.6 cm (66 mm). 7.6 cm is where it ends, not how long it is.", rnd, want=("L", 66)))
    its.append(conv(D("3.125"), "km", "m", [D("312.5"), 31250, D("3.125")], rnd))
    its.append(conv(75, "m", "km", [D("0.75"), D("7.5"), 75000], rnd,
                    extra=" Check: 0.75 km would be 750 m."))
    its.append(conv(D("1.75"), "m", "mm", [175, 17500, D("1.75")], rnd,
                    extra=" (1.75 × 100 = 175 gives centimetres, not millimetres.)"))
    its.append(conv(38, "mm", "m", [D("3.8"), D("0.38"), 38000], rnd,
                    extra=" You need a 0 in the tenths place."))
    its.append(conv(4050, "m", "km", [D("4.5"), D("40.5"), D("4.005")], rnd,
                    extra=" The 0 in 4050 keeps its place: 4.05, not 4.5."))
    its.append(conv(D("1.08"), "m", "cm", [180, D("10.8"), 1080], rnd))
    its.append(mcq("The CN Tower in Toronto is <b>553 m</b> tall. How tall is it in kilometres?", "0.553 km",
                   ["5.53 km", "55.3 km", "553" + NBSP + "000 km"],
                   "1 km = 1000 m, so divide by 1000: 553 ÷ 1000 = 0.553 km. The digits move 3 places to the right. "
                   "(5.53 km divides by 100, and 553" + NBSP + "000 km multiplies.)", rnd, want=("L", 553000)))
    its.append(mcq("Convert. <b>2 km 75 m = ☐ km</b>", "2.075 km", ["2.75 km", "20.75 km", "2.705 km"],
                   "75 m = 75 ÷ 1000 = 0.075 km, because 1 km = 1000 m. So 2 km 75 m = 2 + 0.075 = 2.075 km. "
                   "2.75 km would be 2 km 750 m.", rnd, want=("L", 2075000)))
    its.append(mcq("Which is the same as <b>6.04 m</b>?", "6 m 4 cm", ["6 m 40 cm", "6 m 4 mm", "64 cm"],
                   "6.04 m = 6 m and 0.04 m. 0.04 m = 0.04 × 100 = 4 cm. So 6.04 m = 6 m 4 cm. "
                   "6 m 40 cm would be 6.4 m.", rnd, want=("L", 6040)))
    its.append(mcq("Find the missing number. <b>1 km − 375 m = ☐ km</b>", "0.625 km",
                   ["0.725 km", "0.375 km", "625 km"],
                   "1 km = 1000 m. 1000 − 375 = 625 m. 625 ÷ 1000 = 0.625 km. "
                   "Take care when you regroup: 1000 − 375 is 625, not 725.", rnd, want=("L", 625000)))
    assert len(its) == 20, len(its)
    return {"title": "Length: mm, cm, m and km with decimals", "items": its}


# ------------------------------------------------------------ set 2: mass and capacity
def set_mass_cap(rnd):
    its = []
    its.append(conv(750, "g", "kg", [D("7.5"), D("0.075"), 750000], rnd))
    its.append(conv(D("2.5"), "kg", "g", [250, 25000, 205], rnd,
                    extra=" (250 g multiplies by 100, but 1 kg is 1000 g, not 100 g.)"))
    its.append(conv(D("3.2"), "kg", "g", [320, 32, 32000], rnd,
                    extra=" (320 g uses × 100. A kilogram has 1000 grams.)"))
    its.append(conv(D("1.25"), "L", "mL", [125, 12500, 1025], rnd,
                    extra=" (125 mL would be 0.125 L.)"))
    its.append(conv(330, "mL", "L", [D("3.3"), D("0.033"), 330000], rnd))
    its.append(conv(D("0.5"), "L", "mL", [50, 5, 5000], rnd,
                    extra=" (50 mL uses × 100. A litre has 1000 millilitres.)"))
    its.append(conv(45, "g", "kg", [D("0.45"), D("4.5"), 45000], rnd))
    its.append(conv(D("4.08"), "kg", "g", [4800, 408, 40800], rnd))
    its.append(conv(2600, "mL", "L", [26, D("0.26"), D("2.06")], rnd))
    its.append(conv(D("0.08"), "L", "mL", [800, 8, D("0.8")], rnd))
    its.append(mcq("Convert. <b>3 kg 50 g = ☐ kg</b>", "3.05 kg", ["3.5 kg", "3.005 kg", "30.5 kg"],
                   "50 g = 50 ÷ 1000 = 0.05 kg. So 3 kg 50 g = 3.05 kg. 3.5 kg would be 3 kg 500 g.",
                   rnd, want=("M", 3050)))
    its.append(mcq("Convert. <b>1 L 200 mL = ☐ L</b>", "1.2 L", ["1.02 L", "12 L", "1.002 L"],
                   "200 mL = 200 ÷ 1000 = 0.2 L. So 1 L 200 mL = 1.2 L. 1.02 L would be 1 L 20 mL.",
                   rnd, want=("C", 1200)))
    q = fig(dial_svg(1400, 3000, 1000, 200, 1000)) + \
        "The scale shows the mass of a bag of flour. What is the mass in kilograms?"
    its.append(mcq(q, "1.4 kg", ["1.2 kg", "1.04 kg", "14 kg"],
                   "Each kilogram is split into 5 equal spaces, so each mark is 1 ÷ 5 = 0.2 kg (200 g). "
                   "The needle is 2 marks past 1 kg: 1 + 0.4 = 1.4 kg. (1.2 kg counts each mark as 0.1 kg.)",
                   rnd, want=("M", 1400)))
    q = fig(dial_svg(2750, 4000, 1000, 250, 1000)) + \
        "The scale shows the mass of a box of books. What is the mass in kilograms?"
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
    its.append(mcq("Work out <b>1.5 kg + 700 g</b>. Give your answer in kilograms.", "2.2 kg",
                   ["701.5 kg", "8.5 kg", "1.57 kg"],
                   "Use one unit first: 700 g = 0.7 kg. Then 1.5 + 0.7 = 2.2 kg. "
                   "701.5 kg adds the numbers without converting, and 8.5 kg treats 700 g as 7 kg.",
                   rnd, want=("M", 2200)))
    its.append(mcq("Work out <b>4 L − 1750 mL</b>. Give your answer in millilitres.", "2250 mL",
                   ["1746 mL", "3250 mL", "5750 mL"],
                   "Use one unit first: 4 L = 4000 mL. 4000 − 1750 = 2250 mL. "
                   "(1746 mL takes away 4 without converting, and 5750 mL adds instead of subtracting.)",
                   rnd, want=("C", 2250)))
    assert len(its) == 20, len(its)
    return {"title": "Mass and capacity: g, kg, mL and L", "items": its}


# ------------------------------------------------------------ set 3: choose the unit
def set_choose(rnd):
    its = []
    for obj, ans, wr, e in [
        ("the mass of a bag of potatoes", "kilograms (kg)", ["litres (L)", "kilometres (km)", "millimetres (mm)"],
         "Mass is measured in grams or kilograms. A bag of potatoes is heavy, so kilograms fit. "
         "Litres measure capacity, and kilometres and millimetres measure length."),
        ("the length of a skating rink", "metres (m)", ["kilometres (km)", "millimetres (mm)", "grams (g)"],
         "A skating rink is about 60 m long, so metres fit. A kilometre is far too long, a millimetre far too small, "
         "and grams measure mass."),
        ("the area of a classroom floor", "square metres (m²)", ["metres (m)", "square centimetres (cm²)",
                                                                 "square kilometres (km²)"],
         "Area needs square units. A classroom floor is about 8 m by 9 m, so square metres fit. "
         "Metres measure length, not area."),
        ("the area of a postage stamp", "square centimetres (cm²)", ["centimetres (cm)", "square metres (m²)",
                                                                     "square kilometres (km²)"],
         "A stamp is small and flat, about 3 cm by 4 cm, so square centimetres fit. "
         "Centimetres alone measure length, not area."),
        ("the area of Lake Ontario", "square kilometres (km²)", ["kilometres (km)", "square metres (m²)",
                                                                 "square centimetres (cm²)"],
         "Lake Ontario is huge, so square kilometres fit. Kilometres alone measure length, not area."),
    ]:
        its.append(mcq("Which unit is best for measuring <b>%s</b>?" % obj, ans, wr, e, rnd))
    for obj, ans, wr, e in [
        ("the mass of an adult moose", "450 kg", ["450 g", "4.5 kg", "45 g"],
         "An adult moose is much heavier than a person, so hundreds of kilograms fit. 4.5 kg is about the "
         "mass of a cat."),
        ("how much a juice box holds", "200 mL", ["200 L", "2 L", "20 L"],
         "A juice box holds much less than a litre. 200 mL = 0.2 L. 2 L is a big carton."),
        ("the length of a hockey stick", "1.5 m", ["1.5 km", "1.5 cm", "15 m"],
         "A hockey stick comes up to about a student’s chin, so 1.5 m fits. 1.5 cm is shorter than a fingernail, "
         "and 15 m is longer than a school bus."),
        ("the driving distance from Toronto to Ottawa", "450 km", ["450 m", "45 m", "4.5 km"],
         "Toronto to Ottawa is a drive of about 4 or 5 hours, so it is a few hundred kilometres. "
         "4.5 km is only about an hour’s walk."),
        ("the thickness of a loonie", "2 mm", ["2 cm", "2 m", "0.2 m"],
         "A loonie is very thin, less than 1 cm, so millimetres fit. 2 cm is as thick as a stack of about 10 loonies."),
        ("how much water a bathtub holds", "150 L", ["150 mL", "15 mL", "1.5 L"],
         "A bathtub holds a lot of water, so litres fit. 1.5 L is only a large water bottle."),
        ("the mass of a Grade 6 student", "40 kg", ["40 g", "4 kg", "400 kg"],
         "Most Grade 6 students have a mass of about 30 kg to 50 kg. 4 kg is about the mass of a new baby."),
        ("the mass of a slice of bread", "30 g", ["30 kg", "3 kg", "0.3 kg"],
         "A slice of bread is light, so grams fit. 0.3 kg = 300 g, which is about a whole small loaf."),
        ("how much a teaspoon holds", "5 mL", ["5 L", "50 L", "0.5 L"],
         "A teaspoon holds only a tiny amount, so millilitres fit. 0.5 L = 500 mL, which is a whole bottle of water."),
    ]:
        its.append(mcq("Which is the most sensible measurement for <b>%s</b>?" % obj, ans, wr, e, rnd))
    its.append(mcq("Owen jumps <b>312 cm</b> in the long jump. Which shows this in metres?", "3.12 m",
                   ["31.2 m", "0.312 m", "3.012 m"],
                   "1 m = 100 cm, so divide by 100: 312 ÷ 100 = 3.12 m. The digits move 2 places to the right.",
                   rnd, want=("L", 3120)))
    its.append(mcq("A bag of rice has a mass of <b>1650 g</b>. Which shows this in kilograms?", "1.65 kg",
                   ["16.5 kg", "165 kg", "1.065 kg"],
                   "1 kg = 1000 g, so divide by 1000: 1650 ÷ 1000 = 1.65 kg. "
                   "(16.5 kg divides by 100, as if 1 kg were 100 g.)", rnd, want=("M", 1650)))
    its.append(mcq("An ant is <b>0.006 m</b> long. Which shows the same length in a more sensible unit?", "6 mm",
                   ["6 cm", "0.6 mm", "0.06 mm"],
                   "1 m = 1000 mm, so 0.006 × 1000 = 6 mm. A small number of millimetres is easier to read than "
                   "a decimal with zeros.", rnd, want=("L", 6)))
    its.append(mcq("A newborn baby has a mass of <b>3 kg 40 g</b>. Which shows this in kilograms?", "3.04 kg",
                   ["3.4 kg", "3.004 kg", "30.4 kg"],
                   "40 g = 40 ÷ 1000 = 0.04 kg. So 3 kg 40 g = 3.04 kg. 3.4 kg would be 3 kg 400 g.",
                   rnd, want=("M", 3040)))
    its.append(mcq("A cross-country ski trail is <b>1 km 60 m</b> long. Which shows this in kilometres?", "1.06 km",
                   ["1.6 km", "1.006 km", "10.6 km"],
                   "60 m = 60 ÷ 1000 = 0.06 km. So 1 km 60 m = 1.06 km. 1.6 km would be 1 km 600 m.",
                   rnd, want=("L", 1060000)))
    its.append(mcq("A pot holds <b>2 L 50 mL</b> of soup. Which shows this in litres?", "2.05 L",
                   ["2.5 L", "2.005 L", "20.5 L"],
                   "50 mL = 50 ÷ 1000 = 0.05 L. So 2 L 50 mL = 2.05 L. 2.5 L would be 2 L 500 mL.",
                   rnd, want=("C", 2050)))
    assert len(its) == 20, len(its)
    return {"title": "Choose the unit", "items": its}


# ------------------------------------------------------------ set 4: elapsed time
def set_time(rnd):
    its = []
    its.append(tmcq("How long is <b>135 minutes</b> in hours and minutes?", "2 hours 15 minutes",
                    ["1 hour 35 minutes", "2 hours 35 minutes", "3 hours 15 minutes"],
                    "1 hour = 60 minutes. 135 − 60 − 60 = 15, so 135 minutes = 2 hours 15 minutes. "
                    "(1 hour 35 minutes treats an hour as 100 minutes.)", rnd))
    q = "How many minutes are in <b>2.5 hours</b>?"
    its.append(mcq(q, "150 minutes", ["250 minutes", "170 minutes", "25 minutes"],
                   "2.5 hours = 2 hours and half an hour. 2 × 60 + 30 = 150 minutes. "
                   "(250 uses 100 minutes per hour, and 170 reads 2.5 hours as 2 hours 50 minutes.)", rnd))
    ch = ["1.5 hours", "100 minutes", "1 hour 20 minutes", "95 minutes"]
    assert sorted(ch, key=lambda x: {"1.5 hours": 90}.get(x, dur_value(x)))[-1] == "100 minutes"
    its.append(mcq("Which is the <b>longest</b> time?", "100 minutes", ["1.5 hours", "1 hour 20 minutes", "95 minutes"],
                   "Change them all to minutes: 1.5 hours = 90 minutes and 1 hour 20 minutes = 80 minutes. "
                   "100 minutes is the longest. (1.5 hours is 1 hour 30 minutes, not 1 hour 50 minutes.)", rnd))
    its.append(dur_q("A class trip to the museum leaves at <b>9:40 a.m.</b> and arrives at <b>11:15 a.m.</b> "
                     "How long is the trip?", T(9, 40, "am"), T(11, 15, "am"), rnd))
    its.append(dur_q("A soccer game starts at <b>2:50 p.m.</b> and ends at <b>4:05 p.m.</b> How long is the game?",
                     T(2, 50, "pm"), T(4, 5, "pm"), rnd))
    its.append(dur_q("Hockey practice runs from <b>6:45 a.m.</b> to <b>8:10 a.m.</b> How long is practice?",
                     T(6, 45, "am"), T(8, 10, "am"), rnd))
    for a, b, what in [(T(10, 45, "am"), T(1, 20, "pm"), "a school concert rehearsal"),
                       (T(9, 35, "am"), T(12, 20, "pm"), "a math and science fair"),
                       (T(2, 35, "pm"), T(5, 15, "pm"), "a skating party")]:
        q = fig(timeline_svg(a, b)) + "The time line shows %s. How long is it from <b>%s</b> to <b>%s</b>?" % (
            what, f12(a), f12(b))
        its.append(dur_q(tidy(q), a, b, rnd))
    its.append(dur_q("Leah’s family drives to the cottage. They leave at <b>11:30 a.m.</b> and arrive at "
                     "<b>2:10 p.m.</b> How long is the drive?", T(11, 30, "am"), T(2, 10, "pm"), rnd))
    its.append(tmcq("Work out <b>1 hour 45 minutes + 50 minutes</b>.", "2 hours 35 minutes",
                    ["1 hour 35 minutes", "2 hours 45 minutes", "3 hours 35 minutes"],
                    "45 + 50 = 95 minutes. 95 minutes = 1 hour 35 minutes, so the total is 1 hour + 1 hour 35 minutes "
                    "= 2 hours 35 minutes. (1 hour 35 minutes forgets to carry the extra hour.)", rnd))

    def end_q(q, t, d, wrong_extra=()):
        r = t + d
        cands = list(wrong_extra) + [f12(r - 60), f12(flip(r)), f12(r + 60), f12(r + 10), f12(r - 10)]
        return tmcq(q, f12(r), cands, add_e(t, d), rnd)

    def start_q(q, t, d, wrong_extra=()):
        r = t - d
        cands = list(wrong_extra) + [f12(t + d), f12(r + 60), f12(flip(r)), f12(r + 10), f12(r - 10)]
        return tmcq(q, f12(r), cands, back_e(t, d), rnd)

    its.append(end_q("A movie starts at <b>7:25 p.m.</b> and lasts <b>1 hour 50 minutes</b>. What time does it end?",
                     T(7, 25, "pm"), 110))
    its.append(end_q("Mateo’s canoe trip starts at <b>10:35 a.m.</b> He paddles for <b>2 hours 50 minutes</b>. "
                     "What time does he finish?", T(10, 35, "am"), 170))
    its.append(start_q("The school bus must arrive by <b>8:40 a.m.</b> The ride takes <b>55 minutes</b>. "
                       "What is the latest time the bus can leave?", T(8, 40, "am"), 55))
    its.append(start_q("Arjun’s swimming lesson ends at <b>5:05 p.m.</b> It lasted <b>1 hour 20 minutes</b>. "
                       "What time did it start?", T(5, 5, "pm"), 80, wrong_extra=[f12(T(4, 45, "pm"))]))
    its.append(end_q("A train leaves Toronto at <b>9:40 a.m.</b> The trip to Ottawa takes <b>4 hours 25 minutes</b>. "
                     "What time does the train arrive?", T(9, 40, "am"), 265))
    its.append(end_q("A flight from Toronto to Vancouver takes off at <b>8:15 a.m.</b> Toronto time. It is in the air "
                     "for <b>5 hours 10 minutes</b>. What time is it in Toronto when the plane lands?",
                     T(8, 15, "am"), 310))
    its.append(tmcq("Clocks in Vancouver are <b>3 hours behind</b> clocks in Toronto. A plane lands in Vancouver at "
                    "<b>1:25 p.m.</b> Toronto time. What time do the clocks in Vancouver show?", f12(T(10, 25, "am")),
                    [f12(T(4, 25, "pm")), f12(T(10, 25, "pm")), f12(T(11, 25, "am"))],
                    "Vancouver is behind, so count back 3 hours: 1:25 p.m. → 12:25 p.m. → 11:25 a.m. → 10:25 a.m. "
                    "Going back past 12 o’clock changes p.m. to a.m. (4:25 p.m. adds the 3 hours instead.)", rnd))
    its.append(dur_q("A flight from Toronto to Vancouver takes off at <b>5:50 p.m.</b> and lands at <b>10:55 p.m.</b>, "
                     "both in Toronto time. How long is the flight?", T(5, 50, "pm"), T(10, 55, "pm"), rnd))
    its.append(dur_q("Hana goes to bed at <b>9:15 p.m.</b> and wakes up at <b>6:45 a.m.</b> How long does she sleep?",
                     T(9, 15, "pm"), T(6, 45, "am") + DAY, rnd, extra=["2 hours 30 minutes"],
                     note="Do not just subtract 6:45 from 9:15: the time goes past midnight. "))
    assert len(its) == 20, len(its)
    return {"title": "Elapsed time across hours", "items": its}


# ------------------------------------------------------------ set 5: word problems
def set_story(rnd):
    its = []

    def add(q, r, w, e, want=None):
        its.append(mcq(q, r, w, e, rnd, want=want))

    def addt(q, r, w, e):
        its.append(tmcq(q, r, w, e, rnd))

    add("Our school’s Terry Fox Run is 5 km. Students run laps of a 400 m track. How many laps is 5 km?",
        "12.5 laps", ["125 laps", "1.25 laps", "12 laps"],
        "5 km = 5000 m. 5000 ÷ 400 = 12.5 laps. Check: 12 × 400 = 4800 m, and half a lap is 200 m more.")
    add("Maya has run 3.2 km of the 5 km Terry Fox Run. How many metres does she have left?",
        "1800 m", ["2800 m", "1.8 m", "180 m"],
        "5 − 3.2 = 1.8 km left. 1.8 × 1000 = 1800 m. (2800 m is a regrouping slip: 5000 − 3200 is 1800.)",
        ("L", 1800000))
    addt("The Terry Fox Run starts at <b>1:40 p.m.</b> Chloe runs the 5 km in <b>38 minutes</b>. "
         "What time does she finish?", f12(T(2, 18, "pm")),
         [f12(T(1, 18, "pm")), f12(T(2, 18, "am")), f12(T(2, 28, "pm"))],
         add_e(T(1, 40, "pm"), 38) + " (1:18 p.m. forgets to move on to the next hour.)")
    add("A sugar shack has <b>15 L</b> of maple syrup. It fills bottles that hold <b>250 mL</b> each. "
        "How many bottles can it fill?",
        "60 bottles", ["6 bottles", "600 bottles", "3750 bottles"],
        "15 L = 15" + NBSP + "000 mL. 15" + NBSP + "000 ÷ 250 = 60 bottles. Check: 4 bottles make 1 L, and "
        "15 × 4 = 60. (6 bottles uses 15 L = 1500 mL, and 3750 multiplies 15 × 250.)")
    add("A family buys 6 bottles of maple syrup. Each bottle holds 250 mL. How many litres of syrup is that?",
        "1.5 L", ["15 L", "0.15 L", "1500 L"],
        "6 × 250 = 1500 mL. 1 L = 1000 mL, so 1500 ÷ 1000 = 1.5 L. (15 L divides by 100.)", ("C", 1500))
    add("It takes about 40 L of maple sap to make 1 L of maple syrup. About how much sap is needed for "
        "<b>750 mL</b> of syrup?",
        "30 L", ["30" + NBSP + "000 L", "300 L", "3 L"],
        "750 mL = 0.75 L. 40 × 0.75 = 30 L of sap. (30" + NBSP + "000 L multiplies 40 × 750 without changing "
        "750 mL into litres.)", ("C", 30000))
    add("Liam packs his hockey bag: skates 1.6 kg, helmet 650 g and pads 2.35 kg. What is the total mass in kilograms?",
        "4.6 kg", ["653.95 kg", "10.45 kg", "4.015 kg"],
        "Change 650 g to kilograms first: 650 ÷ 1000 = 0.65 kg. 1.6 + 0.65 + 2.35 = 4.6 kg. "
        "(653.95 kg adds without converting, and 10.45 kg treats 650 g as 6.5 kg.)", ("M", 4600))
    add("Ethan makes pancakes. Each batch needs 0.3 kg of flour. He makes 3 batches from a 1.5 kg bag. "
        "How many grams of flour are left?",
        "600 g", ["1200 g", "60 g", "1410 g"],
        "3 × 0.3 = 0.9 kg used. 1.5 − 0.9 = 0.6 kg left. 0.6 × 1000 = 600 g. "
        "(1200 g only takes away one batch.)", ("M", 600))
    add("A bird feeder holds 125 g of seed. How many times can Sofia fill it from a 2 kg bag?",
        "16 times", ["1.6 times", "160 times", "250 times"],
        "2 kg = 2000 g. 2000 ÷ 125 = 16. Check: 16 × 125 = 2000. (250 multiplies 2 × 125.)")
    add("A recipe for 4 people uses 250 mL of milk. How many litres of milk are needed for 10 people?",
        "0.625 L", ["6.25 L", "2.5 L", "1 L"],
        "250 ÷ 4 = 62.5 mL for each person. 10 × 62.5 = 625 mL. 625 ÷ 1000 = 0.625 L. "
        "(2.5 L uses 250 mL for each person.)", ("C", 625))
    add("25 students each bring a 750 mL water bottle on a field trip. How many litres of water is that altogether?",
        "18.75 L", ["187.5 L", "1.875 L", "18" + NBSP + "750 L"],
        "25 × 750 = 18" + NBSP + "750 mL. 18" + NBSP + "750 ÷ 1000 = 18.75 L. (187.5 L divides by 100, and "
        "18" + NBSP + "750 L forgets to change millilitres into litres.)", ("C", 18750))
    add("A 2 L carton of juice is poured into 8 cups of 180 mL each. How many millilitres are left in the carton?",
        "560 mL", ["1440 mL", "1820 mL", "56 mL"],
        "8 × 180 = 1440 mL poured. 2 L = 2000 mL. 2000 − 1440 = 560 mL left. "
        "(1820 mL takes away only one cup.)", ("C", 560))
    add("Kai swims 1.2 km at practice in a 25 m pool. How many lengths does he swim?",
        "48 lengths", ["4.8 lengths", "480 lengths", "24 lengths"],
        "1.2 km = 1200 m. 1200 ÷ 25 = 48 lengths. Check: 48 × 25 = 1200. "
        "(24 lengths counts there and back, 50 m, as one length.)")
    add("Zoe has 4.5 m of ribbon. She cuts it into pieces 15 cm long. How many pieces does she get?",
        "30 pieces", ["3 pieces", "300 pieces", "60 pieces"],
        "4.5 m = 450 cm. 450 ÷ 15 = 30 pieces. (3 pieces divides 45 by 15 without converting.)")
    add("A canoe route is 12 km. The group paddles 2.75 km before lunch and 3600 m after lunch. "
        "How much farther do they still have to paddle?",
        "5.65 km", ["8.89 km", "6.35 km", "6.65 km"],
        "3600 m = 3.6 km. 2.75 + 3.6 = 6.35 km paddled. 12 − 6.35 = 5.65 km to go. "
        "(8.89 km treats 3600 m as 0.36 km, and 6.35 km is the distance already paddled.)", ("L", 5650000))
    add("A box of 24 apples has a mass of 3.6 kg. Each apple has the same mass. What is the mass of one apple in grams?",
        "150 g", ["15 g", "1.5 g", "86.4 g"],
        "3.6 kg = 3600 g. 3600 ÷ 24 = 150 g. (15 g changes 3.6 kg into 360 g, and 86.4 g multiplies 3.6 × 24.)",
        ("M", 150))
    add("Ava was 1.38 m tall last year. Since then she has grown 6 cm. How tall is she now, in metres?",
        "1.44 m", ["1.98 m", "7.38 m", "1.386 m"],
        "6 cm = 6 ÷ 100 = 0.06 m. 1.38 + 0.06 = 1.44 m. (1.98 m adds 0.6 m, and 7.38 m adds 6 m.)", ("L", 1440))
    its.append(dur_q("The field trip bus leaves school at <b>8:50 a.m.</b> and arrives at the science centre at "
                     "<b>10:35 a.m.</b> How long is the bus ride?", T(8, 50, "am"), T(10, 35, "am"), rnd))
    t0, d1, d2 = T(6, 20, "am"), 75, 150
    addt("Nathan’s family leaves home at <b>6:20 a.m.</b> The drive to the airport takes <b>1 hour 15 minutes</b>. "
         "Their flight to Vancouver leaves <b>2 hours 30 minutes</b> after they arrive. What time does the flight leave?",
         f12(t0 + d1 + d2), [f12(t0 + d1), f12(t0 + d1 + d2 - 60), f12(flip(t0 + d1 + d2)), f12(t0 + d2)],
         "Arrive at the airport: 6:20 a.m. + 1 hour 15 minutes = 7:35 a.m. Then 7:35 a.m. + 2 hours = 9:35 a.m., "
         "and 30 minutes more is 10:05 a.m. (7:35 a.m. is when they reach the airport, not when the flight leaves.)")
    addt("Priya walks 1.5 km to the rink. She walks 1 km in about 12 minutes. She leaves home at <b>3:52 p.m.</b> "
         "About what time does she reach the rink?", f12(T(4, 10, "pm")),
         [f12(T(4, 4, "pm")), f12(T(4, 7, "pm")), f12(T(4, 10, "am"))],
         "1.5 km takes 12 + 6 = 18 minutes (half a kilometre takes half of 12 minutes). 3:52 p.m. + 8 minutes = "
         "4:00 p.m., and 10 more minutes is 4:10 p.m. (4:04 p.m. adds only the 12 minutes for 1 km, and 4:07 p.m. uses 15 minutes instead of 18.)")
    assert len(its) == 20, len(its)
    return {"title": "Word problems: Terry Fox Run, maple syrup and trips", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % x for x in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


def body_html():
    a, b = T(10, 45, "am"), T(1, 20, "pm")
    return tidy(
        "<h2>Multiply or divide?</h2>"
        "<p>To change a bigger unit into a smaller unit, <b>multiply</b>: you need more of the small units. "
        "To change a smaller unit into a bigger unit, <b>divide</b>. "
        "Multiplying by 1000 moves every digit 3 places to the left. Dividing by 1000 moves every digit "
        "3 places to the right.</p>"
        "<figure class='sn-fig'>" + ladder_svg(["km", "m", "cm", "mm"], ["1000", "100", "10"],
                                                "length units: km to m to cm to mm") +
        "<figcaption>Going to a smaller unit: multiply. Going to a bigger unit: divide.</figcaption></figure>" +
        table(["Measure", "Facts to know"], [
            ["Length", "1 cm = 10 mm &nbsp; 1 m = 100 cm = 1000 mm &nbsp; 1 km = 1000 m"],
            ["Mass", "1 kg = 1000 g"],
            ["Capacity", "1 L = 1000 mL"],
            ["Time", "1 hour = 60 minutes &nbsp; 1 day = 24 hours"],
        ]) +
        ex("Example 1: metres to centimetres", "1.25 m = ☐ cm", "1 m = 100 cm. Multiply: 1.25 × 100 = 125.", "125 cm") +
        ex("Example 2: grams to kilograms", "750 g = ☐ kg", "1 kg = 1000 g. Divide: 750 ÷ 1000 = 0.75.", "0.75 kg") +
        ex("Example 3: two units as one decimal", "3 kg 40 g = ☐ kg",
           "40 g = 40 ÷ 1000 = 0.04 kg. Keep the 0 in the tenths place.", "3.04 kg (not 3.4 kg)") +
        "<h2>Read the scale, then convert</h2>"
        "<p>First find what one line on the scale is worth. Then read it and change the unit if you need to.</p>"
        "<figure class='sn-fig'>" + jug_svg(1300, 2000, 500, 100) +
        "<figcaption>Each line is 100 mL. The water is at 1300 mL, which is 1.3 L.</figcaption></figure>"
        "<h2>Choose the unit</h2>"
        "<p>Pick the unit that gives an easy number. A hockey stick is about 1.5 m, not 0.0015 km. "
        "An ant is 6 mm, not 0.006 m. Area always needs square units: cm², m² or km².</p>"
        "<h2>Elapsed time across hours</h2>"
        "<p>An hour has <b>60</b> minutes, so you cannot subtract clock times like ordinary numbers. "
        "Count on in jumps: to the next o’clock, then whole hours, then the minutes left. "
        "Remember that times change from a.m. to p.m. after 12 noon.</p>"
        "<figure class='sn-fig'>" + timeline_svg(a, b) +
        "<figcaption>From 10:45 a.m. to 1:20 p.m.: 15 minutes + 2 hours + 20 minutes = 2 hours 35 minutes."
        "</figcaption></figure>" +
        ex("Example 4: finding the end time", "A movie starts at 7:25 p.m. and lasts 1 hour 50 minutes. When does it end?",
           add_e(T(7, 25, "pm"), 110), "9:15 p.m.") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["2.5 kg = 250 g (multiplying by 100)", "1 kg = 1000 g, so 2.5 kg = 2500 g"],
            ["750 g = 750" + NBSP + "000 kg (moving the point the wrong way)",
             "Smaller unit to bigger unit: divide. 750 g = 0.75 kg"],
            ["3 kg 40 g = 3.4 kg", "40 g = 0.04 kg, so 3 kg 40 g = 3.04 kg"],
            ["9:40 to 11:15 is 1115 − 940 = 1 hour 75 minutes (100 minutes per hour)",
             "Count on: 20 minutes + 1 hour + 15 minutes = 1 hour 35 minutes"],
            ["1.5 hours = 1 hour 50 minutes", "Half an hour is 30 minutes: 1.5 hours = 90 minutes"],
        ])
    )


FAQ = [
    {"q": "What metric conversions do Grade 6 students learn in the Ontario math curriculum?",
     "a": "Grade 6 students convert between mm, cm, m and km, between g and kg, and between mL and L, using decimals "
          "such as 1.25 m = 125 cm and 750 g = 0.75 kg. They also solve problems with elapsed time."},
    {"q": "How do you convert grams to kilograms?",
     "a": "Divide by 1000, because 1 kg = 1000 g. So 750 g = 0.75 kg and 2600 g = 2.6 kg. To go from kilograms to grams, multiply by 1000."},
    {"q": "What is the easiest way to find elapsed time?",
     "a": "Count on in jumps on a time line: to the next o’clock, then whole hours, then the minutes left. "
          "Do not subtract the clock numbers, because an hour has 60 minutes, not 100."},
    {"q": "Are unit conversions and elapsed time on the Grade 6 EQAO math test?",
     "a": "The Grade 6 EQAO math assessment is based on the Ontario curriculum, and measurement is part of the "
          "Spatial Sense strand. Practising conversions and elapsed time is good preparation."},
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
    rnd = random.Random(36816)
    sets = [set_length(rnd), set_mass_cap(rnd), set_choose(rnd), set_time(rnd), set_story(rnd)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        pos = [0, 0, 0, 0]
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["e"], it
            for f in [it["q"], it["e"]] + it["c"]:
                assert "m.." not in re.sub("<[^>]+>", "", f), f
            pos[it["a"]] += 1
            k = it["q"] + "|" + "|".join(sorted(it["c"]))
            assert k not in seen, it["q"]
            seen.add(k)
            assert it["q"].count("<svg") <= 1
        assert pos == [5, 5, 5, 5], (s["title"], pos)
    return {
        "country": "ca-on", "subject": "math", "grade": "grade-6", "slug": "metric-units-and-time", "sort": 16,
        "updated": UPDATED, "pdf_url": "",
        "title": "Metric Units and Time: Converting Length, Mass and Capacity, and Elapsed Time",
        "seo_title": "Grade 6 Metric Units and Elapsed Time Worksheets: mm, cm, m, km, g, kg, mL, L (Free Math, Answer Key)",
        "short_title": "Metric Units and Time",
        "domain": "Spatial Sense",
        "standard_code": "Grade 6: Spatial Sense, E2",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Measure length, area, mass, and capacity using appropriate metric units, and solve problems "
                         "that require converting smaller units to larger ones and vice versa; solve problems "
                         "involving elapsed time",
        "meta_desc": "Free Grade 6 math worksheets on metric units and elapsed time for the Ontario curriculum: "
                     "converting mm, cm, m and km, g and kg, mL and L with decimals, choosing the unit, and elapsed "
                     "time across hours, with a Terry Fox Run and maple syrup word problems. 100 questions with an "
                     "answer key, good EQAO practice.",
        "key_big": "Bigger unit to smaller unit: multiply. Smaller unit to bigger unit: divide.",
        "key_sub": "1 m = 100 cm, 1 km = 1000 m, 1 kg = 1000 g and 1 L = 1000 mL. For time, an hour has 60 minutes, "
                   "not 100, so count on in jumps.",
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
    mark_large(u, "(ruler|time line)")
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
