# -*- coding: utf-8 -*-
"""
BC Grade 3 Math: Measuring Length, Mass and Capacity (BC Mathematics Curriculum, Grade 3, Geometry and measurement:
"measurement, using standard units (linear, mass, and capacity)")
  python3 tools/gen_cabc_math_g3_measuring.py
HTML attributes use single quotes (no backslashes in the JSON).
Grade 3: numbers to 1000, short sentences for 8-9 year olds, a picture in many questions. Canadian English, metric.
Sets: cm, m, km and benchmarks; read a ruler; g and kg on scales; mL and L in jugs; choose the unit and word problems.
Every ruler object, needle and liquid level is drawn exactly at its value, and every answer is parsed back and checked.
Wrong answers come from real mistakes: starting at 1 or reading the end number when the object does not start at 0,
counting the marks instead of the spaces, counting every mark as 1 when the marks go up by 2, 5, 10, 20, 50 or 100,
thinking the bigger object (or the bigger number) is heavier, mixing up units, and adding instead of subtracting.
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-3")
UPDATED = "2026-11-02"
GREEN = "#006633"
RED = "#c0392b"
INK = "#2b2b2b"
WOOD = "#f6e7b8"
WATER = "#9fd3f2"
WATER_LINE = "#2a7fb8"
JUICE = "#e8b23a"
JUICE_LINE = "#a8741a"
FONT = "Arial, Helvetica, sans-serif"
NBSP = " "
GIRLS = ["Olivia", "Ava", "Chloe", "Simran", "Jasleen", "Mei", "Hana", "Sofia", "Emma", "Leah", "Zara", "Nadia"]
BOYS = ["Liam", "Ethan", "Noah", "Arjun", "Harjot", "Wei", "Lucas", "Mateo", "Kai", "Owen", "Ryan"]


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


def c(n):
    """BC style: 4 digits plain (1000), 5 or more digits grouped with a no-break space."""
    if n < 10000:
        return str(n)
    return "{:,}".format(n).replace(",", NBSP)


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


def marks(k, w="mark"):
    return "%d %s%s" % (k, w, "" if k == 1 else "s")


# ------------------------------------------------------------ figure: ruler (cm and half cm)
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
    elif kind == "feather":
        p0, w = a + (b - a) * 0.12, b - a
        o.append("<path d='M%.1f 22 C%.1f 9 %.1f 9 %.1f 22 C%.1f 35 %.1f 35 %.1f 22 Z' fill='#d9e8f5' stroke='%s' "
                 "stroke-width='1.5'/>" % (p0, p0 + 0.15 * w, b - 0.25 * w, b, b - 0.25 * w, p0 + 0.15 * w, p0, INK))
        o.append("<line x1='%.1f' y1='22' x2='%.1f' y2='22' stroke='%s' stroke-width='2'/>" % (a, b, INK))
    else:  # ribbon
        o.append("<rect x='%.1f' y='15' width='%.1f' height='14' fill='%s' stroke='%s' stroke-width='1.5'/>"
                 % (a, b - a, RED, INK))
    return "".join(o)


NAMES = {"pencil": "pencil", "crayon": "crayon", "eraser": "eraser", "ribbon": "piece of ribbon",
         "feather": "feather"}


def ruler_svg(s_cm, e_cm, kind="pencil", ncm=None):
    """Centimetre ruler from 0 to ncm with half-centimetre marks and an object from s_cm to e_cm (exact)."""
    if ncm is None:
        ncm = max(8, e_cm + 1)
    PX = 38.0
    X0, YR, RH = 18, 40, 50
    W = int(X0 * 2 + PX * ncm + 26)
    H = YR + RH + 4
    X = lambda v: X0 + PX * v
    a, b = X(s_cm), X(e_cm)
    o = [draw_object(kind, a, b)]
    for x in (a, b):
        o.append("<line x1='%.1f' y1='32' x2='%.1f' y2='%d' stroke='%s' stroke-width='1.2' stroke-dasharray='3 2'/>"
                 % (x, x, YR, RED))
    o.append("<rect x='4' y='%d' width='%d' height='%d' rx='3' fill='%s' stroke='%s' stroke-width='2'/>"
             % (YR, W - 8, RH, WOOD, INK))
    small, big = [], []
    for i in range(ncm * 2 + 1):
        x = X(i / 2.0)
        if i % 2 == 0:
            big.append("M%.1f %dL%.1f %d" % (x, YR, x, YR + 18))
        else:
            small.append("M%.1f %dL%.1f %d" % (x, YR, x, YR + 10))
    o.append("<path d='%s' stroke='%s' stroke-width='1.2'/>" % ("".join(small), INK))
    o.append("<path d='%s' stroke='%s' stroke-width='2'/>" % ("".join(big), INK))
    for cc in range(ncm + 1):
        o.append(text(X(cc), YR + 38, str(cc), 15))
    o.append(text(X(ncm) + 12, YR + 38, "cm", 15, anchor="start", bold=False))
    art = "an" if kind == "eraser" else "a"
    nm = NAMES[kind]
    return svg_wrap(W, H, "".join(o), "ruler with %s %s from %d cm to %d cm" % (art, nm, s_cm, e_cm))


# ------------------------------------------------------------ figures: scale and jug
def dial_svg(v, mx, lab, tick, unit, size=200):
    """Round scale: 0 at the lower left, mx at the lower right (270 degrees). Needle exactly at v."""
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


def jug_svg(v, mx, lab, step, unit, liquid="water", size=200):
    """Measuring jug: a line every `step`, a number every `lab`. Liquid exactly at v."""
    x0, x1 = 92, 168
    yb, yt = 186, 34
    fill, line = (JUICE, JUICE_LINE) if liquid == "apple juice" else (WATER, WATER_LINE)

    def Y(val):
        return yb - (yb - yt) * float(val) / mx
    s = []
    s.append("<path d='M%d %d C%d %d %d %d %d %d' fill='none' stroke='%s' stroke-width='6'/>"
             % (x1, 50, x1 + 28, 50, x1 + 28, 124, x1, 124, INK))
    if v > 0:
        s.append("<rect x='%d' y='%.1f' width='%d' height='%.1f' fill='%s'/>" % (x0, Y(v), x1 - x0, yb - Y(v), fill))
        s.append("<line x1='%d' y1='%.1f' x2='%d' y2='%.1f' stroke='%s' stroke-width='2.5'/>" % (x0, Y(v), x1, Y(v), line))
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
    s.append(text(x0 - 7, 202, unit, 15, anchor="end", col=GREEN))
    return svg_wrap(size, size + 6, "".join(s), "measuring jug with %s at %s %s" % (liquid, c(v), unit))


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
    if kind == "puck":
        return ("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' rx='6' fill='#222'/>"
                "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='#666' stroke-width='1.5'/>"
                % (x, y, w, h, x + 3, y + 4, x + w - 3, y + 4))
    if kind == "ball2":
        r = w / 2.0
        return ("<circle cx='%.1f' cy='%.1f' r='%.1f' fill='#fff' stroke='%s' stroke-width='1.5'/>"
                "<path d='M%.1f %.1f Q%.1f %.1f %.1f %.1f' stroke='%s' stroke-width='6' fill='none'/>"
                "<path d='M%.1f %.1f Q%.1f %.1f %.1f %.1f' stroke='#e6b800' stroke-width='6' fill='none'/>"
                % (cx, yb - r, r, INK, cx, yb - 2 * r + 2, cx - r * 0.9, yb - r, cx, yb - 2, RED,
                   cx, yb - 2 * r + 2, cx + r * 0.9, yb - r, cx, yb - 2))
    if kind == "jar":
        return ("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' rx='4' fill='%s' stroke='%s' stroke-width='1.5'/>"
                "<rect x='%.1f' y='%.1f' width='%.1f' height='7' rx='2' fill='%s'/>"
                % (x, y + 6, w, h - 6, col, INK, x + 2, y, w - 4, INK))
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
    W = 360
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
    return svg_wrap(W, H, "".join(s), label)


OBJ = {  # name: (kind, w, h, colour)
    "bowling ball": ("round", 38, 38, "#34495e"), "beach ball": ("ball2", 62, 62, ""),
    "brick": ("box", 54, 24, "#b5523b"), "pillow": ("pillow", 96, 34, "#f3e3f7"),
    "hockey puck": ("puck", 40, 14, ""), "sponge": ("box", 58, 26, "#f7dc6f"),
    "jar of jam": ("jar", 30, 36, "#a3324a"), "rock": ("round", 34, 26, "#8d8d8d"),
    "bag of chips": ("pillow", 70, 40, "#f39c12"),
}


def an(w):
    return ("an " if w[0] in "aeiou" else "a ") + w


# ------------------------------------------------------------ explanations for scales and jugs
def read_e(v, lab, tick, unit, what):
    """what: 'needle', 'water' or 'apple juice'."""
    sp = lab // tick
    base = v - v % lab
    k = (v - base) // tick
    w = "mark" if what == "needle" else "line"
    if sp == 1:
        s = "Every %s has a number. " % w
    else:
        s = ("The numbers go up by %s %s. There are %d spaces between two numbers, so each %s is %s ÷ %d = %s %s. "
             % (c(lab), unit, sp, w, c(lab), sp, c(tick), unit))
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
    """Real mistakes: every mark counted as 1 (or as 2 when marks are 1), one mark off, the next number, wrong unit."""
    base = v - v % lab
    k = (v - base) // tick
    mis = base + k if tick != 1 else base + 2 * k
    w = ["%s %s" % (c(mis), unit), "%s %s" % (c(v + tick), unit), "%s %s" % (c(base + lab), unit),
         "%s %s" % (c(v - tick), unit)]
    w.insert(1 if i % 3 == 0 else 4, "%s %s" % (c(v), alt))
    return w


# ------------------------------------------------------------ set 1: cm, m, km and benchmarks
CHL = ["centimetres (cm)", "metres (m)", "kilometres (km)", "kilograms (kg)"]


def set_length_units(rnd):
    its = []
    for obj, u, why in [
        ("the length of a crayon", 0, "A crayon is short. It fits on a 30 cm ruler, so use centimetres."),
        ("the width of a math notebook", 0, "A notebook fits on your desk and on a ruler, so use centimetres."),
        ("the length of a caterpillar", 0, "A caterpillar is small enough to sit on your hand, so use centimetres."),
        ("the length of a canoe", 1, "A canoe is longer than a grown-up is tall, so use metres."),
        ("the height of a cedar tree", 1, "A cedar tree is very tall, but you can see the top. Use metres."),
        ("the length of a soccer field", 1, "You can run from one end of a soccer field to the other in less than a "
                                            "minute, so use metres."),
        ("the distance from Vancouver to Whistler", 2, "Vancouver to Whistler is a long drive on the Sea-to-Sky "
                                                         "Highway, so use kilometres."),
        ("the distance from Kamloops to Kelowna", 2, "Kamloops to Kelowna is a drive of a few hours, so use "
                                                      "kilometres."),
    ]:
        e = why + " Kilograms measure mass, not length."
        its.append(mcq("Which unit is best to measure %s?" % obj, CHL[u], CHL, e, rnd))
    rnd.shuffle(its)
    its.append(mcq("How many centimetres are in 1 metre?", "100 cm", ["10 cm", "1000 cm", "50 cm"],
                   "A metre stick has 100 centimetres marked on it. So 1 m = 100 cm.", rnd, want=("L", 1000)))
    its.append(mcq("How many metres are in 1 kilometre?", "1000 m", ["100 m", "10 m", "1 m"],
                   "Kilo means 1000. So 1 km = 1000 m.", rnd, want=("L", 1000000)))
    its.append(mcq("Which list goes from the <b>shortest</b> unit to the <b>longest</b> unit?", "cm, m, km",
                   ["km, m, cm", "m, cm, km", "cm, km, m"],
                   "A centimetre is the smallest. 100 cm make 1 m, and 1000 m make 1 km.", rnd))
    for q, ans, wr, e in [
        ("Your fingertip is about ☐ wide.", "1 cm", ["1 m", "10 cm", "1 km"],
         "The width of a fingertip is a good benchmark for 1 cm."),
        ("One big step is about ☐ long.", "1 m", ["1 cm", "10 m", "1 km"],
         "A big step for a grown-up is about 1 m, the same as a metre stick."),
        ("A classroom door is about ☐ tall.", "2 m", ["2 cm", "2 km", "20 m"],
         "A door is a bit taller than a grown-up. That is about 2 m. 2 cm is shorter than your finger."),
        ("A new pencil is about ☐ long.", "19 cm", ["19 m", "190 cm", "1 cm"],
         "A new pencil fits on a 30 cm ruler, so it is about 19 cm. 190 cm is almost as tall as a door."),
        ("A Grade 3 student is about ☐ tall.", "130 cm", ["130 m", "13 cm", "13 m"],
         "Most Grade 3 students are a little more than 1 m tall. 130 cm fits. 13 cm is the size of a hand."),
        ("A school bus is about ☐ long.", "12 m", ["12 cm", "12 km", "120 m"],
         "A school bus is about as long as 6 classroom doors lying end to end, so about 12 m."),
        ("You can walk about ☐ in 15 minutes.", "1 km", ["1 m", "100 m", "100 km"],
         "A 15-minute walk is a good benchmark for 1 km. You can walk 1 m in one big step."),
    ]:
        its.append(mcq("Choose the best estimate. " + q, ans, wr, e, rnd))
    its.append(mcq("Which is longer: 1 m or 90 cm?", "1 m", ["90 cm", "They are the same.", "You cannot tell."],
                   "1 m = 100 cm. 100 cm is longer than 90 cm, so 1 m is longer. "
                   "Do not just compare the numbers 1 and 90.", rnd))
    its.append(mcq("Which is longer: 1 km or 900 m?", "1 km", ["900 m", "They are the same.", "You cannot tell."],
                   "1 km = 1000 m. 1000 m is longer than 900 m, so 1 km is longer, even though 1 looks small.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Centimetres, metres and kilometres", "items": its}


# ------------------------------------------------------------ set 2: read a ruler
def set_ruler(rnd):
    its = []
    for e_cm, kind in [(6, "pencil"), (4, "eraser"), (9, "ribbon"), (7, "crayon")]:
        nm = NAMES[kind]
        q = fig(ruler_svg(0, e_cm, kind)) + "How long is the %s?" % nm
        e = ("The %s starts at 0 and ends at %d, so it is %d cm long. Count the spaces, not the marks: "
             "there are %d numbers from 0 to %d but only %d spaces." % (nm, e_cm, e_cm, e_cm + 1, e_cm, e_cm))
        its.append(mcq(q, "%d cm" % e_cm, ["%d cm" % (e_cm + 1), "%d m" % e_cm, "%d cm" % (e_cm - 1)], e, rnd,
                       want=("L", e_cm * 10)))
    for s_cm, e_cm, kind in [(1, 6, "crayon"), (1, 9, "pencil"), (1, 5, "eraser")]:
        nm = NAMES[kind]
        ln = e_cm - s_cm
        q = fig(ruler_svg(s_cm, e_cm, kind)) + "How long is the %s?" % nm
        e = ("The %s starts at 1, not at 0. So the end number is 1 too big: %d − 1 = %d cm. "
             "You can also count the spaces from 1 to %d: there are %d." % (nm, e_cm, ln, e_cm, ln))
        its.append(mcq(q, "%d cm" % ln, ["%d cm" % e_cm, "%d cm" % (e_cm + 1), "%d cm" % (ln - 1)], e, rnd,
                       want=("L", ln * 10)))
    for s_cm, e_cm, kind in [(2, 9, "pencil"), (3, 7, "eraser"), (2, 8, "ribbon"), (3, 11, "feather"),
                             (4, 10, "crayon"), (5, 12, "pencil"), (3, 12, "ribbon")]:
        nm = NAMES[kind]
        ln = e_cm - s_cm
        q = fig(ruler_svg(s_cm, e_cm, kind)) + "How long is the %s?" % nm
        e = ("The %s starts at %d, not at 0. It ends at %d. %d − %d = %d, so it is %d cm long. "
             "You can also count the spaces from %d to %d: there are %d." % (nm, s_cm, e_cm, e_cm, s_cm, ln, ln,
                                                                            s_cm, e_cm, ln))
        its.append(mcq(q, "%d cm" % ln, ["%d cm" % e_cm, "%d cm" % (ln + 1), "%d cm" % (e_cm + s_cm),
                                         "%d cm" % (ln - 1)], e, rnd, want=("L", ln * 10)))
    its.append(mcq("Leah measures a ribbon. It goes from 0 to 6 on the ruler. She counts the numbers "
                   "0, 1, 2, 3, 4, 5, 6 and says the ribbon is 7 cm. How long is it really?", "6 cm",
                   ["7 cm", "5 cm", "6 m"],
                   "Leah counted 7 numbers, but length is the number of spaces between them. From 0 to 6 there are "
                   "6 spaces, so the ribbon is 6 cm.", rnd, want=("L", 60)))
    its.append(mcq("Noah puts one end of his crayon at 1 on the ruler, not at 0. The other end is at 10. "
                   "How long is the crayon?", "9 cm", ["10 cm", "11 cm", "8 cm"],
                   "He started at 1, so the end number is 1 too big. 10 − 1 = 9 cm.", rnd, want=("L", 90)))
    its.append(mcq("Sofia’s marker lies on a ruler. One end is at 4 cm and the other end is at 13 cm. "
                   "How long is the marker?", "9 cm", ["13 cm", "17 cm", "10 cm"],
                   "It does not start at 0, so subtract: 13 − 4 = 9 cm. 17 cm adds the numbers instead.", rnd,
                   want=("L", 90)))
    its.append(mcq("Kai measures the classroom whiteboard with a metre stick. The stick fits along it exactly "
                   "3 times. How long is the whiteboard?", "3 m", ["3 cm", "4 m", "100 m"],
                   "Each time the metre stick fits, that is 1 m. 3 times is 3 m.", rnd, want=("L", 3000)))
    its.append(mcq("A pencil is 15 cm long. A crayon is 9 cm long. How much longer is the pencil?", "6 cm",
                   ["24 cm", "9 cm", "15 cm"],
                   "“How much longer” compares two lengths, so subtract: 15 − 9 = 6 cm.", rnd, want=("L", 60)))
    its.append(mcq("Arjun lays 3 crayons end to end. Each crayon is 8 cm long. How long is the row?", "24 cm",
                   ["11 cm", "16 cm", "24 m"],
                   "3 crayons of 8 cm: 8 + 8 + 8 = 3 × 8 = 24 cm.", rnd, want=("L", 240)))
    assert len(its) == 20, len(its)
    return {"title": "Read a ruler (not always from 0)", "items": its}


# ------------------------------------------------------------ set 3: g and kg on scales
DIALS = [  # (value, max, label step, tick, unit, object)
    (3, 10, 2, 1, "kg", "a bag of potatoes"),
    (7, 10, 2, 1, "kg", "a pumpkin"),
    (5, 10, 2, 1, "kg", "a box of apples"),
    (13, 20, 5, 1, "kg", "a bag of dog food"),
    (18, 20, 5, 1, "kg", "a box of library books"),
    (32, 50, 10, 2, "kg", "a Grade 3 student"),
    (150, 500, 100, 50, "g", "an apple"),
    (350, 500, 100, 50, "g", "a box of crackers"),
    (240, 500, 100, 20, "g", "a block of cheese"),
    (460, 500, 100, 20, "g", "a bunch of grapes"),
    (850, 1000, 200, 50, "g", "a bag of onions"),
    (170, 200, 50, 10, "g", "a hockey puck"),
]


def set_scale(rnd):
    its = []
    its.append(mcq("How many grams are in 1 kilogram?", "1000 g", ["100 g", "10 g", "1 g"],
                   "Kilo means 1000. So 1 kg = 1000 g.", rnd, want=("M", 1000)))
    reads = []
    for i, (v, mx, lab, tick, unit, obj) in enumerate(DIALS):
        alt = "g" if unit == "kg" else "kg"
        q = fig(dial_svg(v, mx, lab, tick, unit)) + "The scale shows the mass of %s. What is the mass?" % obj
        reads.append(mcq(q, "%s %s" % (c(v), unit), read_wrongs(v, lab, tick, unit, alt, i),
                         read_e(v, lab, tick, unit, "needle"), rnd, want=("M", v * UNIT[unit][1])))
    its += reads
    # bigger is not always heavier
    for hv, lt, word, side in [("bowling ball", "beach ball", "heavier", 1), ("brick", "pillow", "heavier", -1),
                               ("rock", "bag of chips", "lighter", 1)]:
        L, Rn = (hv, lt) if side == 1 else (lt, hv)
        ans = hv if word == "heavier" else lt
        wrong = lt if word == "heavier" else hv
        down = "left" if side == 1 else "right"
        e = ("The %s pan is lower. The lower pan holds the heavier object, so the %s is heavier and the %s is lighter. "
             "The bigger object is not always heavier." % (down, hv, lt))
        its.append(mcq(fig(balance_svg([OBJ[L]], [OBJ[Rn]], side, L, Rn,
                                       "pan balance with %s and %s, %s side down" % (an(L), an(Rn), down))) +
                       "Look at the pan balance. Which object is %s?" % word,
                       "the %s" % ans, ["the %s" % wrong, "They are the same.", "You cannot tell."], e, rnd))
    ws = [200, 100, 50]
    its.append(mcq(fig(balance_svg([OBJ["jar of jam"]], [weight(x, "g") for x in ws], 0, "jar of jam", "",
                                   "level pan balance with a jar of jam and weights")) +
                   "The pan balance is level. What is the mass of the jar of jam?",
                   "350 g", ["200 g", "350 kg", "3 g", "400 g"],
                   "The pans are level, so the jar has the same mass as the weights: 200 + 100 + 50 = 350 g.",
                   rnd, want=("M", 350)))
    its.append(mcq("Which is heavier: 900 g or 1 kg?", "1 kg", ["900 g", "They are the same.", "You cannot tell."],
                   "1 kg = 1000 g. 1000 g is more than 900 g, so 1 kg is heavier, even though 1 looks small.", rnd))
    its.append(mcq(fig(dial_svg(450, 500, 100, 50, "g")) +
                   "The scale shows a bowl of blueberries. The empty bowl has a mass of 100 g. "
                   "What is the mass of the blueberries?",
                   "350 g", ["550 g", "450 g", "100 g"],
                   "Each mark is 50 g, so the needle is at 450 g. Take away the bowl: 450 − 100 = 350 g.",
                   rnd, want=("M", 350)))
    its.append(mcq(fig(dial_svg(600, 1000, 200, 100, "g")) +
                   "The scale shows some flour. How much more flour is needed to make 1000 g?",
                   "400 g", ["1600 g", "500 g", "600 g"],
                   "Each mark is 100 g, so the needle is at 600 g. 1000 − 600 = 400 g more.",
                   rnd, want=("M", 400)))
    assert len(its) == 20, len(its)
    return {"title": "Read a scale in g and kg", "items": its}


# ------------------------------------------------------------ set 4: mL and L in jugs
JUGS = [  # (value, max, label step, line step, unit, liquid)
    (300, 1000, 200, 100, "mL", "water"),
    (700, 1000, 200, 100, "mL", "water"),
    (250, 1000, 500, 250, "mL", "water"),
    (750, 1000, 500, 250, "mL", "apple juice"),
    (450, 1000, 250, 50, "mL", "water"),
    (850, 1000, 250, 50, "mL", "water"),
    (150, 500, 100, 50, "mL", "apple juice"),
    (350, 500, 100, 50, "mL", "water"),
    (650, 1000, 200, 50, "mL", "water"),
    (7, 10, 2, 1, "L", "water"),
    (3, 10, 2, 1, "L", "water"),
    (13, 20, 5, 1, "L", "water"),
    (35, 50, 10, 5, "L", "water"),
]


def set_jug(rnd):
    its = []
    its.append(mcq("How many millilitres are in 1 litre?", "1000 mL", ["100 mL", "10 mL", "1 mL"],
                   "1000 millilitres fill 1 litre: 1 L = 1000 mL.", rnd, want=("C", 1000)))
    for i, (v, mx, lab, step, unit, liq) in enumerate(JUGS):
        alt = "L" if unit == "mL" else "mL"
        q = fig(jug_svg(v, mx, lab, step, unit, liq)) + "How much %s is in the measuring jug?" % liq
        its.append(mcq(q, "%s %s" % (c(v), unit), read_wrongs(v, lab, step, unit, alt, i),
                       read_e(v, lab, step, unit, liq), rnd, want=("C", v * UNIT[unit][1])))
    its.append(mcq("Which holds more: a 1 L carton of milk or a 750 mL bottle of water?", "the 1 L carton",
                   ["the 750 mL bottle", "They hold the same.", "You cannot tell."],
                   "1 L = 1000 mL. 1000 mL is more than 750 mL, so the carton holds more. "
                   "Do not compare just the numbers 1 and 750.", rnd))
    its.append(mcq("Mei pours 500 mL of water into a tall, thin glass. Hana pours 500 mL into a short, wide bowl. "
                   "Which has more water?", "They have the same.",
                   ["the tall glass", "the wide bowl", "You cannot tell."],
                   "Both have 500 mL. The water in the tall glass looks higher, but the amount is the same.", rnd))
    its.append(mcq("Which tool is best for measuring 250 mL of milk for a recipe?", "a measuring cup",
                   ["a kitchen scale", "a ruler", "a metre stick"],
                   "Capacity is measured with a measuring cup or a measuring jug. A scale measures mass.", rnd))
    its.append(mcq(fig(jug_svg(400, 1000, 200, 100, "mL")) + "How much more water is needed to fill the jug to 1000 mL?",
                   "600 mL", ["1400 mL", "400 mL", "700 mL"],
                   "Each line is 100 mL, so the water is at 400 mL. 1000 − 400 = 600 mL more.",
                   rnd, want=("C", 600)))
    its.append(mcq(fig(jug_svg(800, 1000, 200, 100, "mL")) +
                   "Zara pours 250 mL of water out of the jug. How much water is left?",
                   "550 mL", ["1050 mL", "650 mL", "250 mL"],
                   "The water is at 800 mL. Water is poured out, so subtract: 800 − 250 = 550 mL.",
                   rnd, want=("C", 550)))
    its.append(mcq(fig(jug_svg(6, 10, 2, 1, "L")) +
                   "The jug is filled to the top line, 10 L. How many more litres are needed?",
                   "4 L", ["16 L", "6 L", "3 L"],
                   "Each line is 1 L, so the water is at 6 L. 10 − 6 = 4 L more.", rnd, want=("C", 4000)))
    assert len(its) == 20, len(its)
    return {"title": "Read a measuring jug in mL and L", "items": its}


# ------------------------------------------------------------ set 5: choose the unit and word problems
CH6 = ["grams (g)", "kilograms (kg)", "millilitres (mL)", "litres (L)", "centimetres (cm)", "kilometres (km)"]


def no_carry_add(a, b):
    out, place = 0, 1
    while a or b:
        out += ((a % 10 + b % 10) % 10) * place
        a, b, place = a // 10, b // 10, place * 10
    return out


def small_from_big(a, b):
    out, place = 0, 1
    while a or b:
        out += abs(a % 10 - b % 10) * place
        a, b, place = a // 10, b // 10, place * 10
    return out


def set_story(rnd):
    P = People(rnd)
    its = []
    for q, ans, wr, e in [
        ("the mass of a salmon", "kilograms (kg)", ["grams (g)", "litres (L)", "kilometres (km)"],
         "A salmon is heavy to hold up, so use kilograms. Litres measure capacity, and kilometres measure length."),
        ("the mass of a strawberry", "grams (g)", ["kilograms (kg)", "millilitres (mL)", "centimetres (cm)"],
         "A strawberry is very light, so use grams. Millilitres measure capacity."),
        ("how much a water bottle holds", "millilitres (mL)", ["litres (L)", "grams (g)", "centimetres (cm)"],
         "A water bottle holds a small amount, so use millilitres. Grams measure mass."),
        ("how much a bathtub holds", "litres (L)", ["millilitres (mL)", "kilograms (kg)", "kilometres (km)"],
         "A bathtub holds a lot of water, so use litres. Kilograms measure mass."),
        ("the length of the Fraser River", "kilometres (km)", ["centimetres (cm)", "litres (L)", "kilograms (kg)"],
         "The Fraser River is very long. It flows across much of BC, so use kilometres."),
    ]:
        its.append(mcq("Which unit is best for %s?" % q, ans, wr, e, rnd))
    rnd.shuffle(its)

    def add(q, ans, u, wrong, e, fam=None, mult=1):
        want = (fam, ans * mult) if fam else None
        its.append(mcq(q, "%s %s" % (c(ans), u), ["%s %s" % (c(x), uu) for x, uu in wrong if x > 0], e, rnd,
                       want=want))

    nm, he, his = P.next()
    a, b = 48, 36
    add(
        "%s’s family drives %d km to the BC Ferries terminal. After the ferry, they drive %d km more. "
        "How far do they drive in all?" % (nm, a, b), a + b, "km",
        [(a - b, "km"), (no_carry_add(a, b), "km"), (a + b, "m"), (a + b + 10, "km")],
        "Put the two drives together: %d + %d = %d km." % (a, b, a + b), "L", 1000000)
    nm, he, his = P.next()
    add(
        "At the Terry Fox Run, %s runs 5 km. %s little brother walks 2 km. How much farther does %s run?"
        % (nm, cap(his), nm), 3, "km", [(7, "km"), (5, "km"), (2, "km")],
        "“How much farther” compares two distances, so subtract: 5 − 2 = 3 km.", "L", 1000000)
    nm, he, his = P.next()
    add(
        "%s has a ribbon that is 1 m long. %s cuts off 35 cm for a craft. How much ribbon is left?" % (nm, cap(he)),
        65, "cm", [(135, "cm"), (75, "cm"), (65, "m")],
        "1 m = 100 cm. Cutting takes ribbon away: 100 − 35 = 65 cm.", "L", 10)
    add(
        "A class plants 4 rows of beans in the school garden. Each row is 3 m long. "
        "How long are all the rows together?", 12, "m", [(7, "m"), (3, "m"), (12, "cm")],
        "4 rows of 3 m: 3 + 3 + 3 + 3 = 4 × 3 = 12 m.", "L", 1000)
    nm, he, his = P.next()
    add(
        "%s rides %s bike around a 400 m loop in the park. %s rides 2 loops. How far does %s ride?"
        % (nm, his, cap(he), he), 800, "m", [(402, "m"), (200, "m"), (800, "km")],
        "2 loops of 400 m: 2 × 400 = 800 m.", "L", 1000)
    add(
        "A fisher catches 3 salmon. Each salmon has a mass of 4 kg. What is their total mass?",
        12, "kg", [(7, "kg"), (8, "kg"), (12, "g")],
        "3 salmon of 4 kg: 4 + 4 + 4 = 3 × 4 = 12 kg.", "M", 1000)
    nm, he, his = P.next()
    add(
        "%s’s hockey bag has a mass of 11 kg. %s takes out %s skates, which have a mass of 2 kg. "
        "What is the mass of the bag now?" % (nm, cap(he), his), 9, "kg", [(13, "kg"), (11, "kg"), (2, "kg")],
        "Taking out the skates makes the bag lighter: 11 − 2 = 9 kg.", "M", 1000)
    nm, he, his = P.next()
    a, b = 250, 375
    add(
        "%s picks %d g of blueberries. %s sister picks %d g. How many grams do they pick in all?"
        % (nm, a, cap(his), b), a + b, "g", [(b - a, "g"), (no_carry_add(a, b), "g"), (a + b, "kg"), (a + b + 100, "g")],
        "Put the masses together: %d + %d = %d g." % (a, b, a + b), "M")
    add(
        "A bag holds 1 kg of flour. A baker uses 350 g for bannock. How much flour is left?",
        650, "g", [(1350, "g"), (750, "g"), (350, "g"), (650, "kg")],
        "1 kg = 1000 g. Flour is used, so subtract: 1000 − 350 = 650 g.", "M")
    add(
        "It rains a lot in Vancouver. A rain barrel had 65 L of water. A storm added 28 L. "
        "How much water is in the barrel now?", 93, "L", [(37, "L"), (83, "L"), (93, "mL")],
        "Water came in, so add: 65 + 28 = 93 L.", "C", 1000)
    nm, he, his = P.next()
    a, b = 600, 175
    add(
        "%s’s water bottle holds %d mL. %s drinks %d mL at recess. How much water is left?" % (nm, a, cap(he), b),
        a - b, "mL", [(a + b, "mL"), (small_from_big(a, b), "mL"), (b, "mL"), (a - b + 100, "mL")],
        "Drinking takes water away, so subtract: %d − %d = %d mL." % (a, b, a - b), "C")
    nm, he, his = P.next()
    add(
        "%s packs 4 juice boxes for a field trip. Each juice box holds 200 mL. How much juice is that in all?" % nm,
        800, "mL", [(204, "mL"), (600, "mL"), (800, "L")],
        "4 equal groups of 200 mL: 4 × 200 = 800 mL.", "C")
    add(
        "On a camping trip on Vancouver Island, each camper drinks 2 L of water a day. "
        "How much water do 4 campers drink in a day?", 8, "L", [(6, "L"), (2, "L"), (8, "mL")],
        "4 equal groups of 2 L: 4 × 2 = 8 L.", "C", 1000)
    add(
        "A watering can holds 5 L. How many full cans are needed to give the school garden 20 L of water?",
        4, "cans", [(15, "cans"), (25, "cans"), (100, "cans")],
        "How many 5 L cans make 20 L? 20 ÷ 5 = 4 cans.")
    add(
        "A pancake recipe needs 500 mL of milk. Wei has 350 mL. How much more milk does he need?",
        150, "mL", [(850, "mL"), (250, "mL"), (350, "mL")],
        "Find the missing part: 500 − 350 = 150 mL.", "C")
    assert len(its) == 20, len(its)
    return {"title": "Choose the unit and solve word problems", "items": its}


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
        "<p><b>Length</b> tells how long something is: centimetres (cm), metres (m) and kilometres (km). "
        "<b>Mass</b> tells how heavy something is: grams (g) and kilograms (kg). "
        "<b>Capacity</b> tells how much a container holds: millilitres (mL) and litres (L).</p>"
        "<p>Key facts: 1 m = 100 cm, 1 km = 1000 m, 1 kg = 1000 g and 1 L = 1000 mL.</p>"
        "<h2>Benchmarks: know what 1 unit looks like</h2>"
        "<p>Compare with something you know. Then choose the unit and a sensible number.</p>" +
        table(["Unit", "About the same as"], [
            ["1 centimetre (cm)", "the width of your fingertip"],
            ["1 metre (m)", "a metre stick, or one big step"],
            ["1 kilometre (km)", "a 15-minute walk"],
            ["1 gram (g)", "a paper clip"],
            ["1 kilogram (kg)", "a 1 L carton of milk"],
            ["1 millilitre (mL)", "a few drops of water"],
            ["1 litre (L)", "what a carton of milk holds"],
        ]) +
        "<h2>Measure with a ruler</h2>"
        "<p>Line up one end with <b>0</b>. Read the number at the other end. "
        "If the object does not start at 0, subtract: <b>end − start</b>.</p>"
        "<figure class='sn-fig'>" + ruler_svg(0, 7, "pencil") +
        "<figcaption>The pencil starts at 0 and ends at 7. It is 7 cm long.</figcaption></figure>"
        "<figure class='sn-fig'>" + ruler_svg(2, 9, "crayon") +
        "<figcaption>The crayon starts at 2 and ends at 9. 9 − 2 = 7, so it is 7 cm long.</figcaption></figure>"
        "<h2>Read a scale or a measuring jug</h2>"
        "<p>Not every mark has a number. First find <b>what one mark is worth</b>: "
        "the jump between two numbers ÷ the number of spaces. Then count on from the number before.</p>"
        "<figure class='sn-fig'>" + dial_svg(650, 1000, 200, 50, "g") +
        "<figcaption>The numbers go up by 200 g. There are 4 spaces, so each mark is 50 g. "
        "The needle is 1 mark past 600: 650 g.</figcaption></figure>"
        "<figure class='sn-fig'>" + jug_svg(750, 1000, 500, 250, "mL", "apple juice") +
        "<figcaption>The numbers go up by 500 mL. There are 2 spaces, so each line is 250 mL. "
        "The apple juice is 1 line above 500: 750 mL.</figcaption></figure>"
        "<h2>Bigger is not always heavier</h2>"
        "<p>On a pan balance, the <b>lower pan is heavier</b>. A big object can be light.</p>"
        "<figure class='sn-fig'>" + balance_svg([OBJ["bowling ball"]], [OBJ["beach ball"]], 1, "bowling ball",
                                               "beach ball",
                                               "pan balance with a bowling ball and a beach ball, left side down") +
        "<figcaption>The bowling ball is smaller, but its pan is lower. The bowling ball is heavier.</figcaption></figure>" +
        ex("Example", "A ribbon is 1 m long. Liam cuts off 35 cm. How much is left?",
           "Change to the same unit: 1 m = 100 cm. Then subtract: 100 − 35 = 65.", "65 cm") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Starting at 1 on the ruler", "Start at 0, or subtract: end − start"],
            ["Counting the numbers, not the spaces", "From 0 to 6 there are 6 spaces: 6 cm"],
            ["Counting every mark as 1 on a scale or jug", "Find what one mark is worth: jump ÷ spaces"],
            ["Thinking a bigger object is heavier", "Check with a balance: the lower pan is heavier"],
            ["Thinking 1 kg is less than 900 g", "Change to the same unit: 1 kg = 1000 g"],
            ["Leaving out the unit", "Write cm, m, km, g, kg, mL or L after the number"],
        ])
    )


FAQ = [
    {"q": "What do Grade 3 students learn about measurement in BC?",
     "a": "In the Geometry and measurement area of the BC Grade 3 math curriculum, students measure with standard units: "
          "centimetres, metres and kilometres for length, grams and kilograms for mass, and millilitres and litres for capacity."},
    {"q": "What are good benchmarks for 1 cm, 1 m, 1 kg and 1 L?",
     "a": "A fingertip is about 1 cm wide and one big step is about 1 m. "
          "A 1 L carton of milk holds 1 litre and has a mass of about 1 kg."},
    {"q": "Why does my child get the wrong length on a ruler?",
     "a": "The most common mistakes are starting at 1, counting the numbers instead of the spaces, and reading the end "
          "number when the object does not start at 0. Ask your child to subtract: end − start."},
    {"q": "How can I practise measuring at home?",
     "a": "Measure toys with a ruler, read the kitchen scale when you bake, and fill a measuring cup with water. "
          "Guess first, then check, and always say the unit."},
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
    rnd = random.Random(53807)
    sets = [set_length_units(rnd), set_ruler(rnd), set_scale(rnd), set_jug(rnd), set_story(rnd)]
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
            # pictures: the correct answer is the value drawn
            m = re.search(r"aria-label='ruler with an? [a-z ]+ from (\d+) cm to (\d+) cm'", it["q"])
            if m:
                assert it["c"][it["a"]] == "%d cm" % (int(m.group(2)) - int(m.group(1))), it["q"][-60:]
                n += 1
            m = re.search(r"aria-label='(?:scale with the needle|measuring jug with [a-z ]+) at (\d+) (g|kg|mL|L)'",
                          it["q"])
            if m and "What is the mass?" in it["q"] or m and "is in the measuring jug?" in it["q"]:
                assert it["c"][it["a"]] == "%s %s" % (m.group(1), m.group(2)), it["q"][-60:]
                n += 1
        assert pos == [5, 5, 5, 5], (s["title"], pos)
    assert n == 14 + 12 + 13, n
    return {
        "country": "ca-bc", "subject": "math", "grade": "grade-3", "slug": "measuring-length-mass-and-capacity",
        "sort": 7, "updated": UPDATED, "pdf_url": "",
        "title": "Grade 3 Measuring Length, Mass and Capacity",
        "seo_title": "Grade 3 Measuring Length, Mass and Capacity Worksheets: Free Math Practice with Answer Key "
                     "(BC Curriculum)",
        "short_title": "Length, mass and capacity",
        "domain": "Geometry and measurement",
        "standard_code": "Grade 3: Geometry and measurement",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/3/core",
        "standard_text": "Measurement, using standard units (linear, mass, and capacity)",
        "meta_desc": "Free Grade 3 math worksheets on measuring for the BC curriculum: centimetres, metres and kilometres, "
                     "reading a ruler, grams and kilograms on a scale, millilitres and litres in a jug, and word "
                     "problems. 100 questions with an answer key.",
        "key_big": "Choose the right unit, then read the marks carefully.",
        "key_sub": "On a ruler, start at 0 or subtract end − start. On a scale or jug, find what one mark is worth "
                   "before you count. 1 m = 100 cm, 1 kg = 1000 g, 1 L = 1000 mL.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


def mark_large(u, pattern):
    """Tag wide pictures so they print larger."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='(?:" + pattern + "))")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


if __name__ == "__main__":
    u = gen_unit()
    mark_large(u, "ruler|pan balance|level pan balance")
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
