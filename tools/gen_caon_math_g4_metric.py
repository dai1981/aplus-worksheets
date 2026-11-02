# -*- coding: utf-8 -*-
"""
Canada (Ontario) Grade 4 Math: Mass, Capacity and Metric Units (Grade 4: E2.2, with E2.1)
  python3 tools/gen_caon_math_g4_metric.py
Metric prefixes (kilo, centi, milli), choosing units and tools for length, mass and capacity,
grams and kilograms, millilitres and litres, reading scales and jugs, and Canadian word problems.
Every measurement answer is parsed back to a base unit (mm, g, mL) and checked in code.
Wrong answers come from real mistakes: 1 kg = 100 g (or 1 L = 100 mL), 3 kg 50 g = 350 g or 3500 g,
mixing up kilo / centi / milli, a bigger number means a bigger amount (900 g > 1 kg),
a bigger object is heavier, a taller container holds more, counting every mark on a scale as 100 g.
Canadian English and Ontario number style (4 digits plain, 5 or more digits with a no-break space).
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, math, os, random, re
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-4")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
RED = "#c0392b"
INK = "#2b2b2b"
WATER = "#9fd3f2"
WATER_LINE = "#2a7fb8"
SYRUP = "#c9822b"
SYRUP_LINE = "#8a5414"
WOOD = "#f6e7b8"
CUBE = "#5dade2"
FONT = "Arial, Helvetica, sans-serif"
NBSP = " "
GIRLS = ["Olivia", "Emma", "Maya", "Zoe", "Amira", "Mei", "Chloe", "Priya", "Leah", "Hana", "Ava", "Sofia"]
BOYS = ["Liam", "Noah", "Aiden", "Lucas", "Owen", "Arjun", "Ethan", "Jayden", "Benjamin", "Mateo", "Nathan", "Kai"]


# ------------------------------------------------------------ units and checking
# unit: (family, size in the base unit mm / g / mL)
UNIT = {"mm": ("L", 1), "cm": ("L", 10), "m": ("L", 1000), "km": ("L", 1000000),
        "g": ("M", 1), "kg": ("M", 1000), "mL": ("C", 1), "L": ("C", 1000)}
TOK = re.compile(r"(\d[\d" + NBSP + r"]*(?:\.\d+)?)\s*(" + "|".join(sorted(UNIT, key=len, reverse=True)) +
                 r")(?![a-zA-Z])")


def parse(s):
    """'2 kg 40 g' -> ('M', 2040). None if the string is not a plain measurement."""
    s = s.strip()
    pos, fam, tot = 0, None, Fr(0)
    for mt in TOK.finditer(s):
        if s[pos:mt.start()].strip():
            return None
        fu, sz = UNIT[mt.group(2)]
        if fam and fu != fam:
            return None
        fam = fu
        tot += Fr(mt.group(1).replace(NBSP, "")) * sz
        pos = mt.end()
    if fam is None or s[pos:].strip():
        return None
    return fam, tot


def c(n):
    """Ontario style: 4 digits plain (1000), 5 or more digits grouped with a no-break space (10 000)."""
    n = int(n)
    if n < 10000:
        return str(n)
    return "{:,}".format(n).replace(",", NBSP)


def m(n, u):
    return "%s %s" % (c(n), u)


def two(v, big, small):
    """v in base units -> '2 kg 40 g' (no zero parts)."""
    B, S = UNIT[big][1], UNIT[small][1]
    a, r = divmod(int(v), B)
    assert r % S == 0
    r //= S
    if r == 0:
        return m(a, big)
    if a == 0:
        return m(r, small)
    return "%s %s" % (m(a, big), m(r, small))


def kgg(v):
    return two(v, "kg", "g")


def lml(v):
    return two(v, "L", "mL")


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
        if x in seen or not x or lead.startswith("-") or lead.startswith("−") or lead == "0":
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


# ------------------------------------------------------------ figures: scale and jug
def dial_svg(v, mx, lab, tick, unit, labdiv=1, size=200):
    """Round scale in base units (g). 0 at the lower left, mx at the lower right (270 degrees).
    A number every `lab` (shown as lab / labdiv in `unit`), a mark every `tick`. Needle exactly at v."""
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
             "paint-order='stroke'>" % (15 if mx // labdiv >= 1000 else 18, INK))
    for val in range(0, mx + 1, lab):
        x, y = pt(val, R - 36)
        s.append("<text x='%.1f' y='%.1f'>%s</text>" % (x, y + 6, c(val // labdiv)))
    s.append("</g>")
    s.append("<circle cx='%.1f' cy='%.1f' r='7' fill='%s'/>" % (cx, cy, RED))
    s.append(text(cx, cy + 62, unit, 22, col=GREEN))
    return svg_wrap(size, size, "".join(s), "scale with the needle at %s" % (kgg(v) if unit == "kg" else m(v, unit)))


def jug_svg(v, mx, lab, step, unit, liquid="water", labdiv=1, size=200):
    """Measuring jug in mL: a line every `step`, a number every `lab` (shown as lab / labdiv). Liquid at v."""
    x0, x1 = 92, 168
    yb, yt = 186, 34
    fill, line = (SYRUP, SYRUP_LINE) if liquid == "syrup" else (WATER, WATER_LINE)

    def Y(val):
        return yb - (yb - yt) * float(val) / mx
    s = []
    s.append("<path d='M%d %d C%d %d %d %d %d %d' fill='none' stroke='%s' stroke-width='6'/>"
             % (x1, 50, x1 + 28, 50, x1 + 28, 124, x1, 124, INK))
    s.append("<rect x='%d' y='%.1f' width='%d' height='%.1f' fill='%s'/>" % (x0, Y(v), x1 - x0, yb - Y(v), fill))
    s.append("<line x1='%d' y1='%.1f' x2='%d' y2='%.1f' stroke='%s' stroke-width='2.5'/>" % (x0, Y(v), x1, Y(v), line))
    s.append("<path d='M%d %d L%d %d L%d %d Q%d %d %d %d L%d %d Q%d %d %d %d L%d %d' fill='none' stroke='%s' "
             "stroke-width='4' stroke-linejoin='round'/>"
             % (x0 - 8, 14, x0, 22, x0, yb - 4, x0, yb, x0 + 6, yb, x1 - 6, yb, x1, yb, x1, yb - 4, x1, 16, INK))
    s.append("<g font-size='%d' font-weight='700' fill='%s' text-anchor='end'>" % (15 if labdiv == 1 else 18, INK))
    for val in range(step, mx + 1, step):
        major = val % lab == 0
        s.append("<line x1='%d' y1='%.1f' x2='%d' y2='%.1f' stroke='%s' stroke-width='%s'/>"
                 % (x0, Y(val), x0 + (22 if major else 12), Y(val), INK, "2.6" if major else "1.6"))
        if major:
            s.append("<text x='%d' y='%.1f'>%s</text>" % (x0 - 7, Y(val) + 5, c(val // labdiv)))
    s.append("</g>")
    s.append(text(x0 - 7, 202, unit, 15 if labdiv == 1 else 18, anchor="end", col=GREEN))
    what = lml(v) if unit == "L" else m(v, unit)
    return svg_wrap(size, size + 6, "".join(s), "measuring jug with %s at %s" % (liquid, what))


def dial_e(v, lab, tick, unit, labdiv):
    """Explanation for a scale in g (labels in kg when labdiv = 1000)."""
    sp = lab // tick
    base = v - v % lab
    k = (v - base) // tick
    if labdiv == 1000:
        s = ("The numbers are kilograms, and 1 kg = 1000 g. There are %d spaces between two numbers, "
             "so each mark is 1000 ÷ %d = %d g. " % (sp, sp, tick))
        if k == 0:
            return s + "The needle points right at %s." % kgg(v)
        return s + "The needle is %s past %s: %s + %d g = %s." % (marks(k), kgg(base) if base else "0",
                                                                   kgg(base) if base else "0", k * tick, kgg(v))
    s = ("The numbers go up by %s %s. There are %d spaces between numbers, so each mark is %s ÷ %d = %s %s. "
         % (c(lab), unit, sp, c(lab), sp, c(tick), unit))
    return s + "The needle is %s past %s: %s + %s = %s %s." % (marks(k), c(base), c(base), c(k * tick), c(v), unit)


def jug_e(v, lab, step, labdiv, liquid="water"):
    sp = lab // step
    base = v - v % lab
    k = (v - base) // step
    if labdiv == 1000:
        s = ("The numbers are litres, and 1 L = 1000 mL. There are %d spaces between two numbers, "
             "so each line is 1000 ÷ %d = %d mL. " % (sp, sp, step))
        if k == 0:
            return s + "The top of the %s is right at %s." % (liquid, lml(v))
        return s + "The top of the %s is %s above %s: %s." % (liquid, marks(k, "line"), lml(base), lml(v))
    s = ("The numbers go up by %s mL. There are %d spaces between numbers, so each line is %s ÷ %d = %s mL. "
         % (c(lab), sp, c(lab), sp, c(step)))
    return s + "The top of the %s is %s above %s: %s + %s = %s mL." % (
        liquid, marks(k, "line"), c(base), c(base), c(k * step), c(v))


# ------------------------------------------------------------ figures: pan balance
def draw_obj(kind, cx, yb, w, h, col):
    x, y = cx - w / 2.0, yb - h
    if kind == "weight":
        return ("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' rx='4' fill='%s'/>"
                "<text x='%.1f' y='%.1f' font-size='14' font-weight='700' fill='#fff' text-anchor='middle'>%s</text>"
                % (x, y, w, h, GREEN, cx, yb - 6, col))
    if kind == "cube":
        return ("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' fill='%s' stroke='%s' stroke-width='1.3'/>"
                % (x, y, w, h, col, INK))
    if kind in ("round", "fruit", "pump"):
        out = ("<ellipse cx='%.1f' cy='%.1f' rx='%.1f' ry='%.1f' fill='%s' stroke='%s' stroke-width='1.5'/>"
               % (cx, yb - h / 2.0, w / 2.0, h / 2.0, col, INK))
        if kind == "fruit":
            out += "<path d='M%.1f %.1f q2 -6 5 -8' stroke='%s' stroke-width='2' fill='none'/>" % (cx, y + 2, INK)
        if kind == "pump":
            out += ("<path d='M%.1f %.1f Q%.1f %.1f %.1f %.1f M%.1f %.1f Q%.1f %.1f %.1f %.1f' stroke='%s' "
                    "stroke-width='1.3' fill='none'/>"
                    % (cx - w / 6.0, y + 2, cx - w / 3.0, yb - h / 2.0, cx - w / 6.0, yb - 1,
                       cx + w / 6.0, y + 2, cx + w / 3.0, yb - h / 2.0, cx + w / 6.0, yb - 1, INK))
            out += "<rect x='%.1f' y='%.1f' width='6' height='9' rx='2' fill='%s'/>" % (cx - 3, y - 7, GREEN)
        return out
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
    if kind == "bag":
        return ("<path d='M%.1f %.1f Q%.1f %.1f %.1f %.1f Q%.1f %.1f %.1f %.1f Q%.1f %.1f %.1f %.1f Z' fill='%s' "
                "stroke='%s' stroke-width='1.5'/>"
                "<path d='M%.1f %.1f l-5 -7 M%.1f %.1f l5 -7' stroke='%s' stroke-width='2'/>"
                % (x + 6, y + 8, x, yb, x + w / 2.0, yb, x + w, yb, x + w - 6, y + 8, x + w / 2.0, y + 2, x + 6, y + 8,
                   col, INK, cx, y + 7, cx, y + 7, INK))
    if kind == "pillow":
        return ("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' rx='12' fill='%s' stroke='%s' stroke-width='1.5'/>"
                % (x, y, w, h, col, INK))
    if kind == "book":
        return ("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' rx='2' fill='%s' stroke='%s' stroke-width='1.5'/>"
                "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='#fff' stroke-width='2'/>"
                % (x, y, w, h, col, INK, x + 6, y + 2, x + 6, yb - 2))
    return ("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' rx='3' fill='%s' stroke='%s' stroke-width='1.5'/>"
            % (x, y, w, h, col, INK))


def weight(v, u):
    t = "%d %s" % (v, u)
    return ("weight", 14 + 8.6 * len(t), 22, t)


def cubes(k):
    return [("cube", 18, 18, CUBE)] * k


def pack(items, maxw=124, gap=4):
    """Rows of items (bottom row first). Returns [(row_items, row_width, row_height)]."""
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
    "apple": ("fruit", 30, 28, "#d9483b"), "orange": ("round", 30, 30, "#f39c12"),
    "pumpkin": ("pump", 64, 44, "#e67e22"), "hockey puck": ("puck", 40, 14, ""),
    "bowling ball": ("round", 38, 38, "#34495e"), "beach ball": ("ball2", 62, 62, ""),
    "brick": ("box", 54, 24, "#b5523b"), "pillow": ("pillow", 96, 34, "#f3e3f7"),
    "book": ("book", 66, 18, "#3a6fb0"), "jar of jam": ("jar", 30, 36, "#a3324a"),
    "bag of rice": ("bag", 46, 44, "#efe2c0"), "can of soup": ("jar", 30, 38, "#c8ccd0"),
    "potato": ("round", 34, 24, "#b5835a"), "mitten": ("box", 34, 30, "#d64b6a"),
    "eraser": ("box", 32, 14, "#f7b7c5"), "lemon": ("round", 28, 22, "#f1d23a"),
    "box of crayons": ("box", 50, 26, "#f4c542"), "sponge": ("box", 58, 26, "#f7dc6f"),
}


def o(name):
    return OBJ[name]


def an(w):
    return ("an " if w[0] in "aeiou" else "a ") + w



# ------------------------------------------------------------ figures: ruler and unit ladder
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


def ruler_svg(s_mm, e_mm, kind="pencil", ncm=None, PX=38.0):
    """Ruler from 0 to ncm cm with mm marks and an object from s_mm to e_mm (exact)."""
    if ncm is None:
        ncm = max(8, -(-e_mm // 10) + 1)
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


def containers_svg():
    """A tall thin vase (A) and a short wide bowl (B)."""
    o = []
    # vase A
    o.append("<path d='M52 20 L52 128 Q52 136 60 136 L84 136 Q92 136 92 128 L92 20' fill='#eaf6fd' stroke='%s' "
             "stroke-width='3.5' stroke-linejoin='round'/>" % INK)
    o.append("<ellipse cx='72' cy='20' rx='20' ry='5' fill='none' stroke='%s' stroke-width='3'/>" % INK)
    o.append(text(72, 160, "A", 18))
    # bowl B
    o.append("<path d='M140 84 Q144 136 205 136 Q266 136 270 84 Z' fill='#eaf6fd' stroke='%s' stroke-width='3.5' "
             "stroke-linejoin='round'/>" % INK)
    o.append("<ellipse cx='205' cy='84' rx='65' ry='9' fill='none' stroke='%s' stroke-width='3'/>" % INK)
    o.append(text(205, 160, "B", 18))
    return svg_wrap(290, 168, "".join(o), "a tall thin vase A and a short wide bowl B")


# ------------------------------------------------------------ set 1: kilo, centi, milli
def set_prefix(rnd):
    its = []
    its.append(mcq("In <b>kilo</b>metre and <b>kilo</b>gram, what does <b>kilo</b> mean?", "1000",
                   ["100", "10", "one thousandth"],
                   "Kilo means 1000. 1 kilometre = 1000 metres and 1 kilogram = 1000 grams.", rnd))
    its.append(mcq("In <b>centi</b>metre, what does <b>centi</b> mean?", "one hundredth",
                   ["100", "one thousandth", "one tenth"],
                   "Centi means one hundredth. A centimetre is one hundredth of a metre, so 100 cm = 1 m. "
                   "(Think of a cent: 100 cents make 1 dollar.)", rnd))
    its.append(mcq("In <b>milli</b>litre and <b>milli</b>metre, what does <b>milli</b> mean?", "one thousandth",
                   ["1000", "one hundredth", "one million"],
                   "Milli means one thousandth. A millilitre is one thousandth of a litre, so 1000 mL = 1 L.", rnd))
    its.append(mcq(fig(ruler_svg(0, 10, "ribbon", 2, 110.0)) +
                   "The ribbon is 1 cm long. How many millimetres is that?", "10 mm",
                   ["100 mm", "1 mm", "5 mm", "1000 mm"],
                   "Count the small spaces from 0 to 1: there are 10. Each small space is 1 mm, so 1 cm = 10 mm.",
                   rnd, want=("L", 10)))
    its.append(mcq("How many centimetres are in 1 metre?", "100 cm", ["1000 cm", "10 cm", "1 cm"],
                   "Centi means one hundredth, so it takes 100 centimetres to make 1 metre: 1 m = 100 cm. "
                   "A metre stick shows 100 cm.", rnd, want=("L", 1000)))
    its.append(mcq("How many metres are in 1 kilometre?", "1000 m", ["100 m", "10 m", "10" + NBSP + "000 m"],
                   "Kilo means 1000, so 1 km = 1000 m. That is about the length of 10 soccer fields.", rnd, want=("L", 1000000)))
    its.append(mcq("How many grams are in 1 kilogram?", "1000 g", ["100 g", "10 g", "10" + NBSP + "000 g"],
                   "Kilo means 1000, so 1 kg = 1000 g. Watch out: 1 kg is not 100 g.", rnd, want=("M", 1000)))
    its.append(mcq("How many millilitres are in 1 litre?", "1000 mL", ["100 mL", "10 mL", "1 mL"],
                   "Milli means one thousandth, so 1000 millilitres make 1 litre: 1 L = 1000 mL.",
                   rnd, want=("C", 1000)))
    its.append(mcq("How many millimetres are in 1 metre?", "1000 mm", ["100 mm", "10 mm", "10" + NBSP + "000 mm"],
                   "Milli means one thousandth, so 1 m = 1000 mm. (Check: 1 m = 100 cm and each cm is 10 mm: "
                   "100 × 10 = 1000.)", rnd, want=("L", 1000)))
    its.append(mcq("Which unit is 1000 times as long as a metre?", "kilometre",
                   ["centimetre", "millimetre", "kilogram"],
                   "Kilo means 1000, so a kilometre is 1000 metres. A kilogram is 1000 grams: it measures mass, "
                   "not length.", rnd))
    its.append(mcq("Which unit is one hundredth of a metre?", "centimetre",
                   ["millimetre", "kilometre", "millilitre"],
                   "Centi means one hundredth, so a centimetre is one hundredth of a metre. "
                   "A millimetre is one thousandth of a metre.", rnd))
    its.append(mcq("Which unit is one thousandth of a litre?", "millilitre",
                   ["kilolitre", "centimetre", "millimetre"],
                   "Milli means one thousandth, and litres measure capacity. So a millilitre is one thousandth "
                   "of a litre.", rnd))
    rnd.shuffle(its)
    hard = []
    hard.append(mcq("Order the units from shortest to longest.", "mm, cm, m, km",
                    ["km, m, cm, mm", "cm, mm, m, km", "mm, cm, km, m"],
                    "A millimetre is the tiniest. 10 mm make 1 cm, 100 cm make 1 m, and 1000 m make 1 km.", rnd))
    hard.append(mcq("Which length is the greatest?", "1 km", ["900 m", "999 cm", "5000 mm"],
                    "Change to metres: 1 km = 1000 m, 999 cm is less than 10 m, and 5000 mm = 5 m. "
                    "1 km is the greatest even though 1 is the smallest number.", rnd))
    hard.append(mcq("Which is the heaviest?", "2 kg", ["1900 g", "850 g", "999 g"],
                    "2 kg = 2000 g. 2000 g is more than 1900 g, 999 g and 850 g. "
                    "Compare the masses in the same unit, not just the numbers.", rnd))
    hard.append(mcq("Which capacity is the least?", "950 mL", ["1 L", "1200 mL", "2 L"],
                    "1 L = 1000 mL and 2 L = 2000 mL. 950 mL is less than 1000 mL, 1200 mL and 2000 mL.", rnd))
    hard.append(mcq("3 km = ☐ m", "3000 m", ["300 m", "30 m", "30" + NBSP + "000 m"],
                    "1 km = 1000 m, so 3 km = 3 × 1000 = 3000 m.", rnd, want=("L", 3000000)))
    hard.append(mcq("5 m = ☐ cm", "500 cm", ["5000 cm", "50 cm", "15 cm"],
                    "1 m = 100 cm, so 5 m = 5 × 100 = 500 cm.", rnd, want=("L", 5000)))
    hard.append(mcq("7 cm = ☐ mm", "70 mm", ["700 mm", "7000 mm", "17 mm"],
                    "1 cm = 10 mm, so 7 cm = 7 × 10 = 70 mm.", rnd, want=("L", 70)))
    hard.append(mcq("A bigger unit gives a smaller number. Which is true?", "4 m = 400 cm",
                    ["4 m = 40 cm", "4 cm = 400 m", "4 m = 4000 cm"],
                    "Metres are bigger than centimetres, so you need more centimetres: 4 × 100 = 400. "
                    "4 m = 400 cm.", rnd))
    its += hard
    assert len(its) == 20, len(its)
    return {"title": "Kilo, centi and milli", "items": its}


# ------------------------------------------------------------ set 2: choose the unit and the tool
CHL = ["millimetres (mm)", "centimetres (cm)", "metres (m)", "kilometres (km)"]
CH4 = ["grams (g)", "kilograms (kg)", "millilitres (mL)", "litres (L)"]


def set_choose(rnd):
    its = []
    length = [
        ("the length of an ant", 0, "An ant is tiny, only a few millimetres long. Use the smallest unit, millimetres."),
        ("the thickness of a loonie", 0, "A loonie is only about 2 mm thick. Tiny lengths are measured in millimetres."),
        ("the length of a crayon", 1, "A crayon fits in your hand and is about 9 cm long. Use centimetres."),
        ("the width of a math book", 1, "A book is about 21 cm wide. Use centimetres."),
        ("the length of a hockey rink", 2, "A hockey rink is about 60 m long. Long lengths you can walk are measured "
                                           "in metres."),
        ("the distance from Toronto to Ottawa", 3, "Toronto and Ottawa are about 400 km apart. Long distances between "
                                                    "towns are measured in kilometres."),
    ]
    for what, k, e in length:
        its.append(mcq("Which unit is best for measuring %s?" % what, CHL[k], CHL, e, rnd))
    mass = [
        ("the mass of a loonie", 0, "A loonie is very light, only about 6 g. Use grams."),
        ("the mass of a bag of potatoes", 1, "A bag of potatoes is heavy to carry. Heavy things are measured in "
                                             "kilograms."),
        ("the mass of a moose", 1, "A moose is very heavy, hundreds of kilograms. Use kilograms."),
    ]
    for what, k, e in mass:
        its.append(mcq("Which unit is best for measuring %s?" % what, CH4[k], CH4,
                       e + " Millilitres and litres measure capacity, not mass.", rnd))
    capq = [
        ("how much a juice box holds", 2, "A juice box holds only about 200 mL. Small amounts are measured in "
                                           "millilitres."),
        ("how much medicine fits on a spoon", 2, "A spoon holds only about 5 mL. Use millilitres."),
        ("how much water a bathtub holds", 3, "A bathtub holds a lot of water, about 150 L. Use litres."),
    ]
    for what, k, e in capq:
        its.append(mcq("Which unit is best for measuring %s?" % what, CH4[k], CH4,
                       e + " Grams and kilograms measure mass, not capacity.", rnd))
    tools = [
        ("the length of the school hallway", "a trundle wheel", ["a 30 cm ruler", "a kitchen scale", "a measuring cup"],
         "A trundle wheel clicks every metre as you roll it, so it is good for long lengths. "
         "A 30 cm ruler is much too short."),
        ("the distance around your head", "a measuring tape", ["a ruler", "a trundle wheel", "a pan balance"],
         "A measuring tape bends, so it can go around a curved shape. A ruler is stiff and cannot bend."),
        ("the mass of an apple", "a kitchen scale", ["a ruler", "a measuring cup", "a thermometer"],
         "Mass is measured with a scale or a pan balance. A measuring cup measures capacity."),
        ("250 mL of milk for a recipe", "a measuring cup", ["a kitchen scale", "a ruler", "a trundle wheel"],
         "Capacity is measured with a measuring cup or a measuring jug. A scale measures mass."),
        ("the length of a pencil", "a ruler", ["a trundle wheel", "a measuring cup", "a bathroom scale"],
         "A pencil is short, so a ruler marked in centimetres and millimetres is best."),
    ]
    for what, ans, wr, e in tools:
        its.append(mcq("Which tool is best for measuring %s?" % what, ans, wr, e, rnd))
    rnd.shuffle(its)
    est = [
        ("the height of a classroom door", "2 m", ["2 cm", "20 m", "2 km"],
         "A door is a bit taller than a grown-up, about 2 m. 20 m is as tall as a 6-storey building."),
        ("the mass of a Grade 4 student", "30 kg", ["30 g", "300 kg", "3 kg"],
         "A Grade 4 student has a mass of about 30 kg. 30 g is only the mass of about 5 loonies."),
        ("how much a mug of hot chocolate holds", "250 mL", ["250 L", "25 mL", "2500 mL"],
         "A mug holds about a quarter of a 1 L carton, which is 250 mL. 250 L would fill more than a bathtub."),
    ]
    its += [mcq("What is the best estimate for %s?" % w, a, wr, e, rnd) for w, a, wr, e in est]
    assert len(its) == 20, len(its)
    return {"title": "Choose the unit and the tool", "items": its}


# ------------------------------------------------------------ set 3: grams and kilograms
def set_grams(rnd):
    its = []

    def to_g(n):
        its.append(mcq("%d kg = ☐ g" % n, m(n * 1000, "g"),
                       [m(n * 100, "g"), m(n * 10, "g"), m(n * 10000, "g")],
                       "1 kg = 1000 g, so %d kg = %d × 1000 = %s g." % (n, n, c(n * 1000)),
                       rnd, want=("M", n * 1000)))

    def to_kg(n):
        its.append(mcq("%s g = ☐ kg" % c(n * 1000), m(n, "kg"),
                       [m(n * 10, "kg"), m(n * 100, "kg"), m(n * 1000, "kg")],
                       "1000 g = 1 kg. How many groups of 1000 are in %s? %s ÷ 1000 = %d, so it is %d kg."
                       % (c(n * 1000), c(n * 1000), n, n), rnd, want=("M", n * 1000)))

    its.append(mcq("Which fact about mass is true?", "1 kg = 1000 g", ["1 kg = 100 g", "1 kg = 10 g", "1 g = 1000 kg"],
                   "Kilo means 1000. One kilogram is 1000 grams.", rnd))
    to_g(2)
    to_g(5)
    to_kg(3)
    to_kg(7)
    its.append(mcq("5000 g = 5 ☐", "kg", ["g", "mL", "cm"],
                   "1000 g = 1 kg, so 5000 g is 5 groups of 1000 g: 5 kg.", rnd))
    its.append(mcq("Half of a kilogram is how many grams?", "500 g", ["50 g", "250 g", "5 g"],
                   "1 kg = 1000 g. Half of 1000 is 500, so half a kilogram is 500 g. "
                   "(50 g would be half of 100 g.)", rnd, want=("M", 500)))
    its.append(mcq("Which is heavier: 1 kg or 900 g?", "1 kg", ["900 g", "They are the same.", "You cannot tell."],
                   "Change to the same unit: 1 kg = 1000 g. 1000 g is more than 900 g, so 1 kg is heavier. "
                   "A bigger number is not always more.", rnd))
    its.append(mcq("Which is heavier: 3 kg or 2500 g?", "3 kg", ["2500 g", "They are the same.", "You cannot tell."],
                   "3 kg = 3000 g. 3000 g is more than 2500 g, so 3 kg is heavier.", rnd))
    # balance: bigger is not always heavier
    its.append(mcq(fig(balance_svg([o("brick")], [o("pillow")], 1, "brick", "pillow",
                                   "pan balance with a brick and a pillow, left side down")) +
                   "Look at the pan balance. Which object is heavier?", "the brick",
                   ["the pillow", "They are the same.", "You cannot tell."],
                   "The pan with the brick is lower, so the brick is heavier. The pillow is bigger, "
                   "but a bigger object is not always heavier.", rnd))
    its.append(mcq(fig(balance_svg([o("beach ball")], [o("jar of jam")], -1, "beach ball", "jar of jam",
                                   "pan balance with a beach ball and a jar of jam, right side down")) +
                   "Look at the pan balance. Which object is lighter?", "the beach ball",
                   ["the jar of jam", "They are the same.", "You cannot tell."],
                   "The pan with the jar of jam is lower, so the jar is heavier and the beach ball is lighter. "
                   "The beach ball is big, but it is full of air.", rnd))
    rnd.shuffle(its)
    hard = []
    hard.append(mcq("10 kg = ☐ g", "10" + NBSP + "000 g", ["1000 g", "100 g", "10" + NBSP + "100 g"],
                    "1 kg = 1000 g, so 10 kg = 10 × 1000 = 10" + NBSP + "000 g.", rnd, want=("M", 10000)))
    hard.append(mcq("2 kg 400 g = ☐ g", "2400 g", ["240 g", "2040 g", "2004 g"],
                    "2 kg = 2000 g. Add the 400 g: 2000 + 400 = 2400 g.", rnd, want=("M", 2400)))
    hard.append(mcq("3 kg 50 g = ☐ g", "3050 g", ["350 g", "3500 g", "3005 g"],
                    "3 kg = 3000 g. Add the 50 g: 3000 + 50 = 3050 g. Writing 3500 g would add 500 g, not 50 g.",
                    rnd, want=("M", 3050)))
    hard.append(mcq("4500 g = ☐", "4 kg 500 g", ["45 kg", "4 kg 50 g", "40 kg 500 g"],
                    "4500 g = 4000 g + 500 g. 4000 g = 4 kg, so 4500 g = 4 kg 500 g.", rnd, want=("M", 4500)))
    hard.append(mcq("1.5 kg = ☐ g", "1500 g", ["150 g", "1050 g", "15 g"],
                    "1.5 kg is 1 kg and half a kilogram (5 tenths). 1000 g + 500 g = 1500 g.", rnd, want=("M", 1500)))
    hard.append(mcq("Which mass is the greatest?", "1 kg 300 g", ["1030 g", "1003 g", "130 g"],
                    "Change all to grams: 1 kg 300 g = 1300 g. 1300 g is more than 1030 g, 1003 g and 130 g.", rnd))
    hard.append(mcq("Order from lightest to heaviest: 2 kg, 1800 g, 700 g", "700 g, 1800 g, 2 kg",
                    ["2 kg, 700 g, 1800 g", "1800 g, 700 g, 2 kg", "2 kg, 1800 g, 700 g"],
                    "2 kg = 2000 g. So 700 g &lt; 1800 g &lt; 2000 g. The 2 kg is the heaviest even though 2 is "
                    "the smallest number.", rnd))
    hard.append(mcq(fig(balance_svg([o("pumpkin")], [weight(2, "kg"), weight(500, "g"), weight(500, "g")], 0,
                                    "pumpkin", "", "level pan balance with a pumpkin and weights")) +
                    "The pan balance is level. What is the mass of the pumpkin?", "3 kg",
                    ["1002 g", "2 kg 500 g", "2 kg"],
                    "500 g + 500 g = 1000 g = 1 kg. Then 2 kg + 1 kg = 3 kg. Do not just add the numbers "
                    "2 + 500 + 500: they are in different units.", rnd, want=("M", 3000)))
    hard.append(mcq("How many 250 g packs of butter make 1 kg?", "4 packs", ["2 packs", "10 packs", "25 packs"],
                    "1 kg = 1000 g. Count by 250: 250, 500, 750, 1000. That is 4 packs.", rnd))
    assert len(its) + len(hard) == 20
    return {"title": "Grams and kilograms", "items": its + hard}


# ------------------------------------------------------------ set 4: millilitres and litres
def set_litres(rnd):
    its = []

    def to_ml(n):
        its.append(mcq("%d L = ☐ mL" % n, m(n * 1000, "mL"),
                       [m(n * 100, "mL"), m(n * 10, "mL"), m(n * 10000, "mL")],
                       "1 L = 1000 mL, so %d L = %d × 1000 = %s mL." % (n, n, c(n * 1000)),
                       rnd, want=("C", n * 1000)))

    def to_l(n):
        its.append(mcq("%s mL = ☐ L" % c(n * 1000), m(n, "L"),
                       [m(n * 10, "L"), m(n * 100, "L"), m(n * 1000, "L")],
                       "1000 mL = 1 L. %s ÷ 1000 = %d, so it is %d L." % (c(n * 1000), n, n),
                       rnd, want=("C", n * 1000)))

    its.append(mcq("Which fact about capacity is true?", "1 L = 1000 mL", ["1 L = 100 mL", "1 L = 10 mL", "1 mL = 1000 L"],
                   "Milli means one thousandth, so 1000 millilitres make 1 litre.", rnd))
    to_ml(3)
    to_ml(6)
    to_l(2)
    to_l(8)
    its.append(mcq("4000 mL = 4 ☐", "L", ["mL", "kg", "m"],
                   "1000 mL = 1 L, so 4000 mL is 4 groups of 1000 mL: 4 L.", rnd))
    its.append(mcq("Half of a litre is how many millilitres?", "500 mL", ["50 mL", "250 mL", "5 mL"],
                   "1 L = 1000 mL. Half of 1000 is 500, so half a litre is 500 mL.", rnd, want=("C", 500)))
    its.append(mcq("A teaspoon holds about how much?", "5 mL", ["5 L", "50 mL", "500 mL"],
                   "A teaspoon is a good benchmark for 5 mL. 500 mL is half of a 1 L carton of milk.", rnd))
    its.append(mcq("A 1 L carton of milk has a mass of about how much?", "1 kg", ["1 g", "100 g", "10 kg"],
                   "1 L of milk or water has a mass of about 1 kg. So a 1 L carton is a benchmark for 1 kg.", rnd))
    its.append(mcq("Which holds more: 2 L or 1900 mL?", "2 L", ["1900 mL", "They hold the same.", "You cannot tell."],
                   "2 L = 2000 mL. 2000 mL is more than 1900 mL, so 2 L is more. Compare in the same unit.", rnd))
    its.append(mcq("Which holds more: 4 L or 4500 mL?", "4500 mL", ["4 L", "They hold the same.", "You cannot tell."],
                   "4 L = 4000 mL. 4500 mL is more than 4000 mL.", rnd))
    rnd.shuffle(its)
    hard = []
    hard.append(mcq("10 L = ☐ mL", "10" + NBSP + "000 mL", ["1000 mL", "100 mL", "10" + NBSP + "010 mL"],
                    "1 L = 1000 mL, so 10 L = 10 × 1000 = 10" + NBSP + "000 mL.", rnd, want=("C", 10000)))
    hard.append(mcq("1 L 250 mL = ☐ mL", "1250 mL", ["125 mL", "1025 mL", "350 mL"],
                    "1 L = 1000 mL. Add the 250 mL: 1000 + 250 = 1250 mL.", rnd, want=("C", 1250)))
    hard.append(mcq("4 L 80 mL = ☐ mL", "4080 mL", ["480 mL", "4800 mL", "4008 mL"],
                    "4 L = 4000 mL. Add the 80 mL: 4000 + 80 = 4080 mL. Keep the 0 in the hundreds place.",
                    rnd, want=("C", 4080)))
    hard.append(mcq("3500 mL = ☐", "3 L 500 mL", ["35 L", "3 L 50 mL", "30 L 500 mL"],
                    "3500 mL = 3000 mL + 500 mL, and 3000 mL = 3 L. So 3500 mL = 3 L 500 mL.", rnd, want=("C", 3500)))
    hard.append(mcq("2.5 L = ☐ mL", "2500 mL", ["250 mL", "2050 mL", "25 mL"],
                    "2.5 L is 2 L and half a litre (5 tenths). 2000 mL + 500 mL = 2500 mL.", rnd, want=("C", 2500)))
    hard.append(mcq("Which capacity is the greatest?", "2500 mL", ["2 L 50 mL", "2 L 5 mL", "250 mL"],
                    "Change all to millilitres: 2 L 50 mL = 2050 mL and 2 L 5 mL = 2005 mL. "
                    "2500 mL is the greatest.", rnd))
    hard.append(mcq("Order from least to most: 1 L, 300 mL, 1100 mL", "300 mL, 1 L, 1100 mL",
                    ["1 L, 300 mL, 1100 mL", "300 mL, 1100 mL, 1 L", "1100 mL, 1 L, 300 mL"],
                    "1 L = 1000 mL. So 300 mL &lt; 1000 mL &lt; 1100 mL.", rnd))
    hard.append(mcq("How many 250 mL glasses can you fill from a full 1 L jug?", "4 glasses",
                    ["2 glasses", "10 glasses", "25 glasses"],
                    "1 L = 1000 mL. Count by 250: 250, 500, 750, 1000. That is 4 glasses.", rnd))
    hard.append(mcq(fig(containers_svg()) +
                    "Leah empties a full 1 L jug into the tall vase A. It fills up, and 400 mL is left in the jug. "
                    "Then she empties another full 1 L jug into the short bowl B. It fills up, and 100 mL is left. "
                    "Which container holds more?", "bowl B", ["vase A", "They hold the same.", "You cannot tell."],
                    "Vase A holds 1000 − 400 = 600 mL. Bowl B holds 1000 − 100 = 900 mL. The bowl holds more. "
                    "A taller container does not always hold more.", rnd))
    assert len(its) + len(hard) == 20
    return {"title": "Millilitres and litres", "items": its + hard}


# ------------------------------------------------------------ set 5: read scales and solve word problems
def dial_wrongs(v, lab, tick):
    base = v - v % lab
    k = (v - base) // tick
    r = v - base
    w = []
    if tick != 100:
        w.append(base + 100 * k)            # every mark counted as 100 g
    else:
        w.append(base + 50 * k)
    if r and r % 10 == 0 and r >= 100:
        w.append(base + r // 10)           # 2 kg 750 g written as 2 kg 75 g
    w += [v + tick, v - tick, base + lab]
    return w


def set_story(rnd):
    P = People(rnd)
    its = []
    # A: read a scale (labels in kg, marks in g)
    for v, mx, tick in [(2750, 4000, 250), (1400, 5000, 200), (3500, 5000, 500)]:
        q = fig(dial_svg(v, mx, 1000, tick, "kg", 1000)) + "What mass does the scale show?"
        its.append(mcq(q, kgg(v), [kgg(x) for x in dial_wrongs(v, 1000, tick)],
                       dial_e(v, 1000, tick, "kg", 1000), rnd, want=("M", v)))
    q = fig(dial_svg(550, 1000, 200, 50, "g")) + "What mass does the scale show?"
    its.append(mcq(q, "550 g", ["700 g", "430 g", "600 g", "550 kg"], dial_e(550, 200, 50, "g", 1), rnd,
                   want=("M", 550)))
    # B: read a jug
    q = fig(jug_svg(1250, 2000, 1000, 250, "L", "water", 1000)) + "How much water is in the jug?"
    its.append(mcq(q, "1 L 250 mL", ["1 L 100 mL", "1 L 25 mL", "1 L 500 mL", "2 L"],
                   jug_e(1250, 1000, 250, 1000), rnd, want=("C", 1250)))
    q = fig(jug_svg(2500, 3000, 1000, 500, "L", "water", 1000)) + "How much water is in the jug?"
    its.append(mcq(q, "2 L 500 mL", ["2 L 100 mL", "2 L 50 mL", "3 L"],
                   jug_e(2500, 1000, 500, 1000), rnd, want=("C", 2500)))
    q = fig(jug_svg(650, 1000, 200, 50, "mL", "syrup")) + "How much maple syrup is in the jug?"
    its.append(mcq(q, "650 mL", ["610 mL", "700 mL", "800 mL", "650 L"],
                   jug_e(650, 200, 50, 1, "maple syrup"), rnd, want=("C", 650)))
    rnd.shuffle(its)
    # C: problems with a picture
    nm, he, his = P.next()
    its.append(mcq(fig(dial_svg(3500, 5000, 1000, 500, "kg", 1000)) +
                   "The scale shows %s’s backpack. %s takes out a 600 g lunch. What is the mass of the backpack now?"
                   % (nm, cap(he)), "2900 g", ["4100 g", "3440 g", "2500 g"],
                   "Each mark is 500 g, so the scale shows 3 kg 500 g = 3500 g. "
                   "Taking out the lunch makes it lighter: 3500 − 600 = 2900 g.", rnd, want=("M", 2900)))
    nm, he, his = P.next()
    its.append(mcq(fig(jug_svg(1250, 2000, 1000, 250, "L", "water", 1000)) +
                   "%s wants 2 L of water in the jug for the plants. How much more water does %s need?" % (nm, he),
                   "750 mL", ["850 mL", "1250 mL", "3250 mL"],
                   "Each line is 250 mL, so the jug has 1 L 250 mL = 1250 mL. 2 L = 2000 mL. "
                   "2000 − 1250 = 750 mL more.", rnd, want=("C", 750)))
    # D: word problems
    its.append(mcq("A bag of milk holds 4 L. How many millilitres is that?", "4000 mL", ["400 mL", "40 mL", "4004 mL"],
                   "1 L = 1000 mL, so 4 L = 4 × 1000 = 4000 mL.", rnd, want=("C", 4000)))
    its.append(mcq("A sugar shack fills 4 bottles with maple syrup. Each bottle holds 250 mL. "
                   "How much maple syrup is that?", "1 L", ["1000 L", "10 L", "254 mL"],
                   "4 × 250 = 1000 mL, and 1000 mL = 1 L.", rnd, want=("C", 1000)))
    nm, he, his = P.next()
    its.append(mcq("%s’s hockey bag has a mass of 9 kg. %s adds %s skates, which have a mass of 1 kg 500 g. "
                   "What is the mass of the bag now?" % (nm, cap(he), his), "10 kg 500 g",
                   ["9 kg 500 g", "10 kg 50 g", "7 kg 500 g"],
                   "Add the kilograms: 9 + 1 = 10 kg. Then add the 500 g: 10 kg 500 g.", rnd, want=("M", 10500)))
    its.append(mcq("On a canoe trip, 4 campers each carry a 750 mL water bottle. How much water do they carry "
                   "in all?", "3000 mL", ["754 mL", "300 mL", "2800 mL"],
                   "4 equal groups of 750 mL: 4 × 750 = 3000 mL. That is 3 L.", rnd, want=("C", 3000)))
    its.append(mcq("A baker has a 2 kg bag of flour. Each batch of muffins uses 250 g. How many batches can "
                   "the baker make?", "8 batches", ["4 batches", "10 batches", "80 batches"],
                   "2 kg = 2000 g. 2000 ÷ 250 = 8, so the baker can make 8 batches.", rnd))
    its.append(mcq("Two pumpkins for Thanksgiving have masses of 3 kg 600 g and 2 kg 700 g. "
                   "What is their total mass?", "6 kg 300 g", ["5 kg 300 g", "900 g", "6 kg 130 g"],
                   "Add the grams: 600 + 700 = 1300 g = 1 kg 300 g. Add the kilograms: 3 + 2 + 1 = 6 kg. "
                   "The total is 6 kg 300 g.", rnd, want=("M", 6300)))
    its.append(mcq("The water cooler at the Terry Fox Run holds 10 L. Each paper cup holds 250 mL. "
                   "How many cups can be filled?", "40 cups", ["4 cups", "400 cups", "25 cups"],
                   "10 L = 10" + NBSP + "000 mL. There are 4 cups in each litre (4 × 250 = 1000), "
                   "so 10 × 4 = 40 cups.", rnd))
    nm, he, his = P.next()
    its.append(mcq("%s has 2 L of apple juice. %s pours 6 glasses of 300 mL for %s friends. How much juice is left?"
                   % (nm, cap(he), his), "200 mL", ["1800 mL", "1700 mL", "3800 mL"],
                   "The glasses use 6 × 300 = 1800 mL. 2 L = 2000 mL. 2000 − 1800 = 200 mL left.",
                   rnd, want=("C", 200)))
    its.append(mcq("Box A has a mass of 1 kg 800 g. Box B has a mass of 2 kg 200 g. How much heavier is Box B?",
                   "400 g", ["600 g", "1 kg 600 g", "4 kg"],
                   "Change to grams: 2200 g − 1800 g = 400 g. (Subtracting 800 − 200 = 600 is the wrong way "
                   "around.)", rnd, want=("M", 400)))
    nm, he, his = P.next()
    its.append(mcq("%s has a big bag of popcorn with a mass of 200 g and a small can of beans with a mass of "
                   "400 g. Which is heavier?" % nm, "the can of beans",
                   ["the bag of popcorn", "They are the same.", "You cannot tell."],
                   "400 g is more than 200 g, so the can is heavier. The bag is bigger, but bigger does not "
                   "mean heavier.", rnd))
    nm, he, his = P.next()
    its.append(mcq("The water jug at the cottage holds 5 L. %s uses 1 L 500 mL for cooking and 750 mL for tea. "
                   "How much water is left?" % nm, "2 L 750 mL",
                   ["2 L 250 mL", "7 L 250 mL", "3 L 500 mL"],
                   "Water used: 1500 + 750 = 2250 mL. 5 L = 5000 mL. 5000 − 2250 = 2750 mL = 2 L 750 mL.",
                   rnd, want=("C", 2750)))
    assert len(its) == 20, len(its)
    return {"title": "Read scales and solve word problems", "items": its}


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
        "<h2>Kilo, centi and milli</h2>"
        "<p>Metric units are built from a few base units: the <b>metre</b> for length, the <b>gram</b> for mass "
        "and the <b>litre</b> for capacity. A <b>prefix</b> at the front tells you the size.</p>" +
        table(["Prefix", "Meaning", "Examples"], [
            ["kilo", "1000", "1 km = 1000 m, 1 kg = 1000 g"],
            ["centi", "one hundredth", "100 cm = 1 m"],
            ["milli", "one thousandth", "1000 mm = 1 m, 1000 mL = 1 L"],
        ]) +
        "<figure class='sn-fig'>" + ladder_svg(["km", "m", "cm", "mm"], ["1000", "100", "10"],
                                                "length units: km to m to cm to mm") +
        "<figcaption>From a bigger unit to a smaller unit, multiply: you need more of the small units.</figcaption>"
        "</figure>"
        "<h2>Choose the unit and the tool</h2>"
        "<p>Use a <b>benchmark</b>: something you know well. Then pick the unit that gives an easy number.</p>" +
        table(["Unit", "About the same as", "Tool"], [
            ["1 mm", "the thickness of a dime", "ruler"],
            ["1 cm", "the width of your little finger", "ruler"],
            ["1 m", "a big step, or a metre stick", "metre stick, measuring tape"],
            ["1 km", "about 10 soccer fields end to end", "trundle wheel, map"],
            ["1 g", "a paper clip", "kitchen scale, pan balance"],
            ["1 kg", "a 1 L carton of milk", "kitchen scale, bathroom scale"],
            ["1 mL", "a few drops of water", "measuring spoon"],
            ["1 L", "a carton of milk", "measuring cup, measuring jug"],
        ]) +
        "<h2>Grams and kilograms, millilitres and litres</h2>"
        "<p><b>1 kg = 1000 g</b> and <b>1 L = 1000 mL</b>. To change kilograms to grams, multiply by 1000. "
        "To change litres to millilitres, multiply by 1000.</p>" +
        ex("Example 1", "3 kg 50 g = ☐ g", "3 kg = 3000 g. Then add 50 g: 3000 + 50 = 3050.", "3050 g") +
        ex("Example 2", "Which holds more: 1 L or 900 mL?",
           "Use the same unit. 1 L = 1000 mL, and 1000 mL is more than 900 mL.", "1 L") +
        "<h2>Read a scale</h2>"
        "<p>First find <b>what one mark is worth</b>: the jump between two numbers ÷ the number of spaces. "
        "Then count on from the number before the needle.</p>"
        "<figure class='sn-fig'>" + dial_svg(2750, 4000, 1000, 250, "kg", 1000) +
        "<figcaption>The numbers are kilograms. There are 4 spaces between 2 and 3, so each mark is "
        "1000 ÷ 4 = 250 g. The needle is 3 marks past 2 kg: 2 kg 750 g, or 2750 g.</figcaption></figure>"
        "<h2>Bigger is not always heavier</h2>"
        "<p>A big beach ball is full of air. A small brick is heavy. Only a scale or a pan balance tells you which "
        "is heavier: the <b>lower pan</b> is heavier.</p>"
        "<figure class='sn-fig'>" + balance_svg([o("brick")], [o("pillow")], 1, "brick", "pillow",
                                                "pan balance with a brick and a pillow, left side down") +
        "<figcaption>The pillow is bigger, but the brick’s pan is lower. The brick is heavier.</figcaption></figure>"
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["1 kg = 100 g or 1 L = 100 mL", "Kilo means 1000: 1 kg = 1000 g. Milli means one thousandth: 1 L = 1000 mL"],
            ["Thinking 900 g is more than 1 kg because 900 is a bigger number",
             "Change to the same unit first: 1 kg = 1000 g"],
            ["3 kg 50 g = 350 g or 3500 g", "3 kg = 3000 g, so 3 kg 50 g = 3050 g"],
            ["Thinking a bigger object is always heavier", "Check with a scale or a pan balance"],
            ["Thinking a taller container always holds more", "Fill it and measure: a short, wide bowl can hold more"],
            ["Counting every mark on a scale as 100 g", "Find what one mark is worth: jump ÷ spaces"],
        ])
    )


FAQ = [
    {"q": "What metric units do Grade 4 students learn in Ontario?",
     "a": "In the Ontario math curriculum, Grade 4 students use millimetres, centimetres, metres and kilometres for "
          "length, grams and kilograms for mass, and millilitres and litres for capacity. They learn what the "
          "prefixes kilo, centi and milli mean and choose the best unit and tool."},
    {"q": "What do kilo, centi and milli mean?",
     "a": "Kilo means 1000, centi means one hundredth and milli means one thousandth. So 1 km = 1000 m, "
          "100 cm = 1 m and 1000 mL = 1 L."},
    {"q": "How many grams are in a kilogram, and how many millilitres are in a litre?",
     "a": "There are 1000 grams in 1 kilogram and 1000 millilitres in 1 litre. A common mistake is to say 100."},
    {"q": "What are good benchmarks for 1 gram, 1 kilogram, 1 millilitre and 1 litre?",
     "a": "A paper clip has a mass of about 1 g, and a 1 L carton of milk has a mass of about 1 kg. "
          "A few drops of water make about 1 mL, and the milk carton holds 1 L."},
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
    rnd = random.Random(44815)
    sets = [set_prefix(rnd), set_choose(rnd), set_grams(rnd), set_litres(rnd), set_story(rnd)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        pos = [0, 0, 0, 0]
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            pos[it["a"]] += 1
            k = it["q"]
            assert k not in seen, it["q"]
            seen.add(k)
            assert it["q"].count("<svg") <= 1
        assert pos == [5, 5, 5, 5], (s["title"], pos)
    return {
        "country": "ca-on", "subject": "math", "grade": "grade-4", "slug": "mass-capacity-and-metric-units",
        "sort": 15, "updated": UPDATED, "pdf_url": "",
        "title": "Mass, Capacity and Metric Units",
        "seo_title": "Grade 4 Metric Units Worksheets: Kilo, Centi, Milli, Grams, Kilograms, Millilitres and "
                     "Litres (Free, with Answer Key)",
        "short_title": "Mass, capacity and metric units",
        "domain": "Spatial Sense",
        "standard_code": "Grade 4: E2.2",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Use metric prefixes to describe the relative size of different metric units, and choose "
                         "appropriate units and tools to measure length, mass, and capacity",
        "meta_desc": "Free Grade 4 math worksheets on metric units: what kilo, centi and milli mean, choosing the "
                     "unit and tool, grams and kilograms, millilitres and litres, reading scales and word problems. "
                     "100 questions with an answer key, matched to the Ontario curriculum.",
        "key_big": "Kilo means 1000: 1 kg = 1000 g. Milli means one thousandth: 1 L = 1000 mL.",
        "key_sub": "Compare measurements in the same unit, not just the numbers: 1 kg is more than 900 g. "
                   "A bigger object is not always heavier.",
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
    mark_large(u, "pan balance|level pan balance|a tall thin vase|ruler")
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
