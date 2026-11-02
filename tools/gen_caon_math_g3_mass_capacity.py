# -*- coding: utf-8 -*-
"""
Canada (Ontario) Grade 3 Math: Mass and Capacity (Grade 3: E2.4)
  python3 tools/gen_ca_math_g3_mass_capacity.py
Canadian English, Ontario number style (4 digits plain, 5+ digits grouped with a no-break space).
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-3")
UPDATED = "2026-11-02"
GREEN = "#006633"
RED = "#c0392b"
INK = "#2b2b2b"
WATER = "#9fd3f2"
WATER_LINE = "#2a7fb8"
SYRUP = "#c9822b"
SYRUP_LINE = "#8a5414"
CUBE = "#5dade2"
FONT = "Arial, Helvetica, sans-serif"
NBSP = " "
GIRLS = ["Olivia", "Emma", "Maya", "Zoe", "Amira", "Mei", "Chloe", "Priya", "Leah", "Hana", "Ava", "Sofia"]
BOYS = ["Liam", "Noah", "Aiden", "Lucas", "Owen", "Arjun", "Ethan", "Jayden", "Benjamin", "Mateo", "Nathan", "Kai"]


# ------------------------------------------------------------ units and checking
UNIT = {"g": ("M", 1), "kg": ("M", 1000), "mL": ("C", 1), "L": ("C", 1000)}
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
    """Ontario style: 4 digits plain (1000), 5 or more digits grouped with a no-break space."""
    if n < 10000:
        return str(n)
    return "{:,}".format(n).replace(",", NBSP)


def mcq(q, correct, cands, e, rnd, want=None):
    """4 choices: correct + 3 unique distractors. Measurement choices of the same kind must differ in value.
    want = (family, value in base unit) checks the correct answer."""
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


# ------------------------------------------------------------ explanations for scales and jugs
def read_e(v, lab, tick, unit, what):
    """what: 'needle' or 'water' (or 'syrup')."""
    sp = lab // tick
    base = v - v % lab
    k = (v - base) // tick
    w = "mark" if what == "needle" else "line"
    if sp == 1:
        s = "Every %s has a number. " % w
    else:
        s = ("The numbers go up by %s %s. There are %d spaces between numbers, so each %s is %s ÷ %d = %s %s. "
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
    """Real mistakes: every mark counted as 1 (or as 2), one mark off, the next number, the wrong unit."""
    base = v - v % lab
    k = (v - base) // tick
    mis = base + k if tick != 1 else base + 2 * k
    w = ["%s %s" % (c(mis), unit), "%s %s" % (c(v + tick), unit), "%s %s" % (c(base + lab), unit),
         "%s %s" % (c(v - tick), unit)]
    w.insert(1 if i % 3 == 0 else 4, "%s %s" % (c(v), alt))
    return w


# ------------------------------------------------------------ set 1: choose the unit and estimate
CH4 = ["grams (g)", "kilograms (kg)", "millilitres (mL)", "litres (L)"]


def set_units(rnd):
    its = []
    mass = [
        ("a pencil", "g", "A pencil is light. You could hold many pencils in one hand, so use grams."),
        ("a hockey puck", "g", "A hockey puck fits in your hand. It is light enough for grams."),
        ("a mitten", "g", "A mitten is very light, so use grams."),
        ("a bag of potatoes", "kg", "A bag of potatoes is heavy to carry. Heavy things are measured in kilograms."),
        ("a Grade 3 student", "kg", "A student is heavy compared with a paper clip, so use kilograms."),
        ("a canoe", "kg", "A canoe is very heavy. It takes two people to carry it, so use kilograms."),
    ]
    for obj, u, why in mass:
        e = why + " Millilitres and litres measure capacity, not mass."
        its.append(mcq("Which unit is best for measuring the mass of %s?" % obj, CH4[0 if u == "g" else 1],
                       CH4, e, rnd))
    cap_q = [
        ("a teaspoon", "mL", "A teaspoon holds only a tiny amount, so use millilitres."),
        ("a juice box", "mL", "A juice box holds a small amount of juice, so use millilitres."),
        ("a small bottle of vanilla", "mL", "A small bottle of vanilla holds only a little, so use millilitres."),
        ("a bathtub", "L", "A bathtub holds a lot of water. Big amounts are measured in litres."),
        ("a kitchen sink", "L", "A sink holds a lot of water, so use litres."),
        ("a rain barrel", "L", "A rain barrel holds a lot of water, so use litres."),
    ]
    for obj, u, why in cap_q:
        e = why + " Grams and kilograms measure mass, not capacity."
        its.append(mcq("Which unit is best for measuring how much %s holds?" % obj, CH4[2 if u == "mL" else 3],
                       CH4, e, rnd))
    rnd.shuffle(its)
    est = [
        ("the mass of a paper clip", "1 g", ["1 kg", "100 g", "10 kg"],
         "A paper clip is the benchmark for 1 gram. 1 kg is as heavy as a 1 L carton of milk."),
        ("the mass of an apple", "150 g", ["150 kg", "15 kg", "1 g"],
         "An apple is light, but it is heavier than a paper clip. It is about 150 g. 150 kg is heavier than a grown-up."),
        ("the mass of a 1 L carton of milk", "1 kg", ["1 g", "10 kg", "100 g"],
         "A 1 L carton of milk is a good benchmark for 1 kilogram. 1 g is only a paper clip."),
        ("the mass of a pet cat", "4 kg", ["4 g", "40 kg", "400 g"],
         "A cat is about as heavy as 4 cartons of milk, so about 4 kg. 40 kg is as heavy as a big dog."),
        ("how much a can of pop holds", "355 mL", ["355 L", "35 L", "3 mL"],
         "A can of pop holds less than a 1 L carton of milk. It holds about 355 mL. 355 L would fill more than a bathtub."),
        ("how much a teaspoon holds", "5 mL", ["5 L", "50 mL", "500 mL"],
         "A teaspoon holds about 5 mL. 500 mL is half of a 1 L carton of milk."),
        ("how much a bucket holds", "10 L", ["10 mL", "100 L", "1 L"],
         "A bucket holds about 10 cartons of milk, so about 10 L. 10 mL is only two teaspoons."),
        ("how much a full bathtub holds", "150 L", ["150 mL", "15 L", "1500 L"],
         "A bathtub holds about 150 L of water. 15 L is only a bucket and a half."),
    ]
    its2 = [mcq("What is the best estimate for %s?" % what, ans, wr, e, rnd) for what, ans, wr, e in est]
    return {"title": "Choose g or kg, mL or L", "items": its + its2}


# ------------------------------------------------------------ set 2: read a scale
DIALS = [  # (value, max, label step, tick, unit, object)
    (3, 10, 2, 1, "kg", "a bag of potatoes"),
    (7, 10, 2, 1, "kg", "a pumpkin"),
    (9, 10, 2, 1, "kg", "a hockey bag"),
    (13, 20, 5, 1, "kg", "a bag of dog food"),
    (18, 20, 5, 1, "kg", "a box of library books"),
    (6, 20, 5, 1, "kg", "a watermelon"),
    (32, 50, 10, 2, "kg", "a Grade 3 student"),
    (26, 50, 10, 2, "kg", "a big dog"),
    (150, 500, 100, 50, "g", "an orange"),
    (350, 500, 100, 50, "g", "a jar of jam"),
    (240, 500, 100, 20, "g", "a block of cheese"),
    (460, 500, 100, 20, "g", "a bunch of grapes"),
    (700, 1000, 200, 100, "g", "a loaf of bread"),
    (650, 1000, 200, 50, "g", "a bag of carrots"),
    (850, 1000, 200, 50, "g", "a bag of apples"),
    (170, 200, 50, 10, "g", "a hockey puck"),
]


def set_scale(rnd):
    its = []
    for i, (v, mx, lab, tick, unit, obj) in enumerate(DIALS):
        alt = "g" if unit == "kg" else "kg"
        q = fig(dial_svg(v, mx, lab, tick, unit)) + "The scale shows the mass of %s. What is the mass?" % obj
        its.append(mcq(q, "%s %s" % (c(v), unit), read_wrongs(v, lab, tick, unit, alt, i),
                       read_e(v, lab, tick, unit, "needle"), rnd, want=("M", v * UNIT[unit][1])))
    rnd.shuffle(its)
    its.append(mcq(fig(dial_svg(450, 500, 100, 50, "g")) +
                   "The scale shows a bowl of blueberries. The empty bowl has a mass of 100 g. "
                   "What is the mass of the blueberries?",
                   "350 g", ["550 g", "450 g", "405 g", "100 g"],
                   "Each mark is 50 g, so the needle is at 450 g. Take away the bowl: 450 − 100 = 350 g.",
                   rnd, want=("M", 350)))
    its.append(mcq(fig(dial_svg(14, 20, 5, 1, "kg")) +
                   "The scale shows a suitcase. The empty suitcase has a mass of 3 kg. "
                   "What is the mass of the clothes inside?",
                   "11 kg", ["17 kg", "14 kg", "12 kg"],
                   "Each mark is 1 kg, so the needle is at 14 kg. Take away the suitcase: 14 − 3 = 11 kg.",
                   rnd, want=("M", 11000)))
    its.append(mcq(fig(dial_svg(600, 1000, 200, 100, "g")) +
                   "The scale shows some flour. How much more flour is needed to make 1000 g?",
                   "400 g", ["1600 g", "500 g", "600 g"],
                   "Each mark is 100 g, so the needle is at 600 g. 1000 − 600 = 400 g more.",
                   rnd, want=("M", 400)))
    its.append(mcq(fig(dial_svg(8, 10, 2, 1, "kg")) +
                   "Arjun puts his backpack on the scale. Then he takes out a 2 kg book. What will the scale show now?",
                   "6 kg", ["10 kg", "8 kg", "7 kg"],
                   "The needle is at 8 kg. Taking out the book makes it lighter: 8 − 2 = 6 kg.",
                   rnd, want=("M", 6000)))
    assert len(its) == 20
    return {"title": "Read a scale in g and kg", "items": its}


# ------------------------------------------------------------ set 3: read a measuring jug
JUGS = [  # (value, max, label step, line step, unit, liquid)
    (300, 1000, 200, 100, "mL", "water"),
    (700, 1000, 200, 100, "mL", "water"),
    (250, 1000, 500, 250, "mL", "water"),
    (750, 1000, 500, 250, "mL", "syrup"),
    (450, 1000, 250, 50, "mL", "water"),
    (850, 1000, 250, 50, "mL", "water"),
    (150, 500, 100, 50, "mL", "water"),
    (350, 500, 100, 50, "mL", "syrup"),
    (650, 1000, 200, 50, "mL", "water"),
    (550, 1000, 200, 50, "mL", "water"),
    (7, 10, 2, 1, "L", "water"),
    (3, 10, 2, 1, "L", "water"),
    (13, 20, 5, 1, "L", "water"),
    (16, 20, 5, 1, "L", "water"),
    (35, 50, 10, 5, "L", "water"),
]


def set_jug(rnd):
    its = []
    for i, (v, mx, lab, step, unit, liq) in enumerate(JUGS):
        alt = "L" if unit == "mL" else "mL"
        thing = "maple syrup" if liq == "syrup" else "water"
        q = fig(jug_svg(v, mx, lab, step, unit, liq)) + "How much %s is in the measuring jug?" % thing
        its.append(mcq(q, "%s %s" % (c(v), unit), read_wrongs(v, lab, step, unit, alt, i),
                       read_e(v, lab, step, unit, liq), rnd, want=("C", v * UNIT[unit][1])))
    rnd.shuffle(its)
    its.insert(0, mcq("How many millilitres are in 1 litre?", "1000 mL", ["100 mL", "10 mL", "1 mL"],
                      "Milli means one thousandth. 1000 millilitres fill 1 litre: 1 L = 1000 mL.",
                      rnd, want=("C", 1000)))
    its.append(mcq(fig(jug_svg(400, 1000, 200, 100, "mL")) + "How much more water is needed to fill the jug to 1000 mL?",
                   "600 mL", ["1400 mL", "400 mL", "700 mL"],
                   "Each line is 100 mL, so the water is at 400 mL. 1000 − 400 = 600 mL more.",
                   rnd, want=("C", 600)))
    its.append(mcq(fig(jug_svg(800, 1000, 200, 100, "mL")) +
                   "Zoe pours 250 mL of water out of the jug. How much water is left?",
                   "550 mL", ["1050 mL", "650 mL", "250 mL"],
                   "The water is at 800 mL. Water is poured out, so subtract: 800 − 250 = 550 mL.",
                   rnd, want=("C", 550)))
    its.append(mcq("Which tool is best for measuring 250 mL of milk for a recipe?", "a measuring cup",
                   ["a kitchen scale", "a ruler", "a thermometer"],
                   "Capacity is measured with a measuring cup or a measuring jug. A scale measures mass.", rnd))
    assert len(its) == 19, len(its)
    its.append(mcq(fig(jug_svg(6, 10, 2, 1, "L")) +
                   "The jug is filled to the top line, 10 L. How many more litres are needed?",
                   "4 L", ["16 L", "6 L", "3 L"],
                   "Each line is 1 L, so the water is at 6 L. 10 − 6 = 4 L more.", rnd, want=("C", 4000)))
    assert len(its) == 20, len(its)
    return {"title": "Read a measuring jug in mL and L", "items": its}


# ------------------------------------------------------------ set 4: compare and order
def set_compare(rnd):
    its = []
    # A: heavier / lighter on a balance (the lower pan is heavier)
    pairs = [("pumpkin", "apple", "heavier", 1), ("bowling ball", "beach ball", "heavier", -1),
             ("brick", "pillow", "lighter", 1), ("hockey puck", "sponge", "lighter", -1)]
    for hv, lt, word, side in pairs:
        L, Rn = (hv, lt) if side == 1 else (lt, hv)
        ans = hv if word == "heavier" else lt
        wrong = lt if word == "heavier" else hv
        down = "left" if side == 1 else "right"
        e = "The %s pan is lower. The lower pan holds the heavier object, so the %s is heavier and the %s is lighter." % (
            down, hv, lt)
        if (hv, lt) in (("bowling ball", "beach ball"), ("brick", "pillow"), ("hockey puck", "sponge")):
            e += " A bigger object is not always heavier."
        its.append(mcq(fig(balance_svg([o(L)], [o(Rn)], side, L, Rn,
                                       "pan balance with %s and %s, %s side down" % (an(L), an(Rn), down))) +
                       "Look at the pan balance. Which object is %s?" % word,
                       "the %s" % ans, ["the %s" % wrong, "They are the same.", "You cannot tell."], e, rnd))
    # B: non-standard units (cubes)
    for name, k in [("apple", 7), ("potato", 9), ("orange", 8)]:
        its.append(mcq(fig(balance_svg([o(name)], cubes(k), 0, name, "%d cubes" % k,
                                       "level pan balance with %s and %d cubes" % (an(name), k))) +
                       "The pan balance is level. What is the mass of the %s in cubes?" % name,
                       "%d cubes" % k, ["%d cubes" % (k - 1), "%d cubes" % (k + 1), "1 cube"],
                       "The pans are level, so the %s has the same mass as the cubes. Count them: %d cubes." % (name, k),
                       rnd))
    # C: object balances standard weights
    for name, m, u, ws in [("jar of jam", 350, "g", [200, 100, 50]), ("bag of rice", 3, "kg", [2, 1]),
                           ("can of soup", 400, "g", [200, 200]), ("pumpkin", 6, "kg", [5, 1])]:
        assert sum(ws) == m
        alt = "kg" if u == "g" else "g"
        its.append(mcq(fig(balance_svg([o(name)], [weight(x, u) for x in ws], 0, name, "",
                                       "level pan balance with %s and weights" % an(name))) +
                       "The pan balance is level. What is the mass of the %s?" % name,
                       "%d %s" % (m, u), ["%d %s" % (ws[0], u), "%d %s" % (m, alt), "%d %s" % (len(ws), u),
                                          "%d %s" % (m + ws[-1], u)],
                       "The pans are level, so the %s has the same mass as the weights: %s = %d %s."
                       % (name, " + ".join(str(x) for x in ws), m, u), rnd))
    # D: order (lightest to heaviest)
    its.append(mcq("Order from lightest to heaviest: 450 g, 1 kg, 90 g",
                   "90 g, 450 g, 1 kg", ["1 kg, 90 g, 450 g", "450 g, 90 g, 1 kg", "1 kg, 450 g, 90 g"],
                   "1 kg = 1000 g, so 1 kg is the heaviest even though the number 1 looks small. "
                   "90 g &lt; 450 g &lt; 1000 g.", rnd))
    its.append(mcq("Order from least to most: 2 L, 600 mL, 900 mL",
                   "600 mL, 900 mL, 2 L", ["2 L, 600 mL, 900 mL", "900 mL, 600 mL, 2 L", "2 L, 900 mL, 600 mL"],
                   "1 L = 1000 mL, so 2 L = 2000 mL. 600 mL &lt; 900 mL &lt; 2000 mL.", rnd))
    its.append(mcq("A book is heavier than an apple. The apple is heavier than an eraser. "
                   "Which is the lightest?", "the eraser", ["the book", "the apple", "They are the same."],
                   "Book &gt; apple and apple &gt; eraser. So the order from heaviest is book, apple, eraser. "
                   "The eraser is the lightest.", rnd))
    its.append(mcq("Which is heavier: 1 kg of feathers or 1 kg of rocks?", "They are the same.",
                   ["the rocks", "the feathers", "You cannot tell."],
                   "Both have a mass of 1 kg, so they are equally heavy. The feathers just take up more space.", rnd))
    # E: unit size (non-standard units)
    its.append(mcq("Mei fills a pot using a small cup. It takes 12 small cups. "
                   "Then she uses a big cup to fill the same pot. How many big cups will she need?",
                   "fewer than 12", ["more than 12", "exactly 12", "24 big cups"],
                   "A big cup holds more, so it takes fewer big cups to fill the same pot. "
                   "The bigger the unit, the fewer units you need.", rnd))
    its.append(mcq("A book balances 40 paper clips. Erasers are heavier than paper clips. "
                   "How many erasers will balance the same book?",
                   "fewer than 40", ["more than 40", "exactly 40", "80 erasers"],
                   "Each eraser is heavier, so fewer erasers are needed. "
                   "A bigger unit gives a smaller number.", rnd))
    its.append(mcq("Owen fills a jug with 6 of his glasses. Hana fills the same jug with 9 of her glasses. "
                   "Whose glass is bigger?", "Owen’s glass",
                   ["Hana’s glass", "They are the same.", "You cannot tell."],
                   "It is the same jug. Owen needed fewer glasses, so each of his glasses holds more. "
                   "A bigger unit gives a smaller number.", rnd))
    # F: capacity of containers
    its.append(mcq("Container A fills 8 cups of water. Container B fills 5 of the same cups. "
                   "Which holds more?", "Container A", ["Container B", "They hold the same.", "You cannot tell."],
                   "The cups are the same size. 8 cups is more than 5 cups, so Container A holds more.", rnd))
    its.append(mcq("Which holds more: a 1 L carton of milk or a 750 mL bottle of water?", "the 1 L carton",
                   ["the 750 mL bottle", "They hold the same.", "You cannot tell."],
                   "1 L = 1000 mL. 1000 mL is more than 750 mL, so the carton holds more. "
                   "Do not compare just the numbers 1 and 750.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Compare and order on a balance", "items": its}


# ------------------------------------------------------------ set 5: word problems
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

    def add(q, ans, u, wrong, e, fam=None, mult=1):
        want = (fam, ans * mult) if fam else None
        its.append(mcq(q, "%s %s" % (c(ans), u), ["%s %s" % (c(x), uu) for x, uu in wrong if x > 0], e, rnd, want=want))

    # maple syrup in a 1 L jug (with a picture)
    nm, he, his = P.next()
    its.append(mcq(fig(jug_svg(1000, 1000, 200, 100, "mL", "syrup")) +
                   "%s has a full 1 L jug of maple syrup. %s pours 250 mL on the pancakes. "
                   "How much maple syrup is left?" % (nm, cap(he)),
                   "750 mL", ["1250 mL", "250 mL", "850 mL"],
                   "1 L = 1000 mL. Syrup is poured out, so subtract: 1000 − 250 = 750 mL.", rnd, want=("C", 750)))
    # bag of apples (with a scale)
    nm, he, his = P.next()
    its.append(mcq(fig(dial_svg(4, 10, 2, 1, "kg")) +
                   "%s buys a bag of apples at the orchard. The scale shows its mass. %s buys 2 more bags just like it. "
                   "What is the mass of all 3 bags?" % (nm, cap(he)),
                   "12 kg", ["6 kg", "7 kg", "8 kg"],
                   "The scale shows 4 kg. 3 bags of 4 kg: 3 × 4 = 12 kg.", rnd, want=("M", 12000)))
    a, b = 386, 248
    add("A backpack has a lunch with a mass of %d g and a water bottle with a mass of %d g. "
        "What is the total mass?" % (a, b), a + b, "g",
        [(a - b, "g"), (no_carry_add(a, b), "g"), (a + b, "kg"), (a + b + 100, "g")],
        "Put the masses together: %d + %d = %d g." % (a, b, a + b), "M")
    a, b = 9, 4
    add("A pumpkin for Thanksgiving has a mass of %d kg. A small pumpkin has a mass of %d kg. "
        "How much heavier is the big pumpkin?" % (a, b), a - b, "kg", [(a + b, "kg"), (a, "kg"), (b, "kg")],
        "“How much heavier” compares two masses, so subtract: %d − %d = %d kg." % (a, b, a - b), "M", 1000)
    nm, he, his = P.next()
    add("%s’s hockey bag has a mass of 11 kg. %s takes out %s skates, which have a mass of 2 kg. "
        "What is the mass of the bag now?" % (nm, cap(he), his), 9, "kg", [(13, "kg"), (11, "kg"), (2, "kg")],
        "Taking out the skates makes the bag lighter: 11 − 2 = 9 kg.", "M", 1000)
    nm, he, his = P.next()
    add("%s packs 6 juice boxes for a field trip. Each juice box holds 200 mL. How much juice is that in all?" % nm,
        1200, "mL", [(206, "mL"), (1000, "mL"), (1400, "mL"), (1200, "L")],
        "6 equal groups of 200 mL: 6 × 200 = 1200 mL.", "C")
    add("On a canoe trip, each camper drinks 2 L of water a day. How much water do 4 campers drink in a day?",
        8, "L", [(6, "L"), (2, "L"), (10, "L"), (8, "mL")],
        "4 equal groups of 2 L: 4 × 2 = 8 L.", "C", 1000)
    add("A bag of milk holds 4 L. A family drinks 1 bag each week. How much milk do they drink in 5 weeks?",
        20, "L", [(9, "L"), (16, "L"), (24, "L")],
        "5 weeks of 4 L: 5 × 4 = 20 L.", "C", 1000)
    add("The water cooler at the Terry Fox Run holds 18 L. Runners drink 9 L. How much water is left?",
        9, "L", [(27, "L"), (18, "L"), (8, "L")],
        "Water was used, so subtract: 18 − 9 = 9 L.", "C", 1000)
    a, b = 600, 175
    nm, he, his = P.next()
    add("%s’s water bottle holds %d mL. %s drinks %d mL at recess. How much water is left?" % (nm, a, cap(he), b),
        a - b, "mL", [(a + b, "mL"), (small_from_big(a, b), "mL"), (b, "mL"), (a - b + 100, "mL")],
        "Drinking takes water away, so subtract: %d − %d = %d mL." % (a, b, a - b), "C")
    add("A rain barrel had 65 L of water. A storm added 28 L. How much water is in the barrel now?",
        93, "L", [(37, "L"), (83, "L"), (93, "mL")],
        "Water came in, so add: 65 + 28 = 93 L.", "C", 1000)
    add("A box holds 5 bags of flour. Each bag has a mass of 2 kg. What is the mass of the flour?",
        10, "kg", [(7, "kg"), (2, "kg"), (12, "kg"), (10, "g")],
        "5 bags of 2 kg: 5 × 2 = 10 kg.", "M", 1000)
    nm, he, his = P.next()
    add("%s picks 24 kg of apples. %s puts them into 4 bags with the same mass. What is the mass of each bag?"
        % (nm, cap(he)), 6, "kg", [(20, "kg"), (28, "kg"), (96, "kg")],
        "Share equally: 24 ÷ 4 = 6 kg in each bag.", "M", 1000)
    add("A pot of soup holds 3 L. How many millilitres is that?",
        3000, "mL", [(300, "mL"), (30, "mL"), (1003, "mL")],
        "1 L = 1000 mL, so 3 L = 3 × 1000 = 3000 mL.", "C")
    add("A dog eats 200 g of food in the morning and 200 g at night. How many grams does it eat in a day?",
        400, "g", [(200, "g"), (4, "g"), (402, "g")],
        "Morning and night together: 200 + 200 = 400 g.", "M")
    nm, he, his = P.next()
    add("%s fills a fish tank with a 5 L pail. %s pours in 7 full pails. How much water is in the tank?" % (nm, cap(he)),
        35, "L", [(12, "L"), (30, "L"), (40, "L")],
        "7 pails of 5 L: 7 × 5 = 35 L.", "C", 1000)
    a, b = 840, 365
    add("A bag of sugar had %d g. A baker uses %d g for butter tarts. How much sugar is left?" % (a, b),
        a - b, "g", [(a + b, "g"), (small_from_big(a, b), "g"), (b, "g"), (a - b + 10, "g")],
        "Sugar was used, so subtract: %d − %d = %d g." % (a, b, a - b), "M")
    add("A watering can holds 4 L. How many full cans are needed to give a garden 20 L of water?",
        5, "cans", [(16, "cans"), (24, "cans"), (80, "cans")],
        "How many 4 L cans make 20 L? 20 ÷ 4 = 5 cans.")
    nm, he, his = P.next()
    add("%s’s backpack has a mass of 7 kg. %s friend’s backpack has a mass of 5 kg. "
        "What is their total mass?" % (nm, cap(his)), 12, "kg", [(2, "kg"), (11, "kg"), (12, "g")],
        "Put the masses together: 7 + 5 = 12 kg.", "M", 1000)
    add("A recipe needs 500 mL of milk. Priya has 350 mL. How much more milk does she need?",
        150, "mL", [(850, "mL"), (250, "mL"), (350, "mL")],
        "Find the missing part: 500 − 350 = 150 mL.", "C")
    assert len(its) == 20, len(its)
    # easier one-step problems first, keep the two picture problems at the start
    first, rest = its[:2], its[2:]
    rnd.shuffle(rest)
    return {"title": "Word problems with mass and capacity", "items": first + rest}


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
        "<h2>Mass and capacity</h2>"
        "<p><b>Mass</b> tells how heavy something is. We measure it in <b>grams (g)</b> for light things and "
        "<b>kilograms (kg)</b> for heavy things. <b>Capacity</b> tells how much a container holds. We measure it in "
        "<b>millilitres (mL)</b> for small amounts and <b>litres (L)</b> for big amounts.</p>"
        "<p>Key facts: 1 kg = 1000 g and 1 L = 1000 mL.</p>"
        "<h2>Benchmarks: know what 1 unit feels like</h2>"
        "<p>Compare a new object with something you know. Then choose the unit and a sensible number.</p>" +
        table(["Unit", "About the same as", "More examples"], [
            ["1 gram (g)", "a paper clip", "an apple is about 150 g"],
            ["1 kilogram (kg)", "a 1 L carton of milk", "a pet cat is about 4 kg"],
            ["1 millilitre (mL)", "a few drops of water", "a teaspoon holds about 5 mL"],
            ["1 litre (L)", "a carton of milk", "a bag of milk holds 4 L, a bucket about 10 L"],
        ]) +
        "<h2>Compare on a pan balance</h2>"
        "<p>The <b>lower pan is heavier</b>. When the pans are level, both sides have the same mass. "
        "A bigger object is not always heavier.</p>"
        "<figure class='sn-fig'>" + balance_svg([o("bowling ball")], [o("beach ball")], 1, "bowling ball", "beach ball",
                                               "pan balance with a bowling ball and a beach ball, left side down") +
        "<figcaption>The bowling ball is smaller, but its pan is lower. The bowling ball is heavier.</figcaption></figure>"
        "<h2>The size of the unit</h2>"
        "<p>You can measure with cubes, cups or paper clips. A <b>bigger unit</b> gives a <b>smaller number</b>. "
        "A smaller unit gives a bigger number.</p>" +
        ex("Example", "A pot holds 12 small cups of water. Will it hold more or fewer big cups?",
           "A big cup holds more water, so fewer big cups fill the pot.", "fewer than 12 big cups") +
        "<h2>Read a scale or a measuring jug</h2>"
        "<p>Not every mark has a number. First find <b>what one mark is worth</b>: "
        "the jump between two numbers ÷ the number of spaces. Then count on from the number before.</p>"
        "<figure class='sn-fig'>" + dial_svg(650, 1000, 200, 50, "g") +
        "<figcaption>The numbers go up by 200 g. There are 4 spaces, so each mark is 50 g. "
        "The needle is 1 mark past 600: 650 g.</figcaption></figure>"
        "<figure class='sn-fig'>" + jug_svg(750, 1000, 500, 250, "mL", "syrup") +
        "<figcaption>The numbers go up by 500 mL. There are 2 spaces, so each line is 250 mL. "
        "The maple syrup is 1 line above 500: 750 mL.</figcaption></figure>"
        "<h2>Solve word problems</h2>"
        "<p>Decide what is happening, then add, subtract, multiply or divide. Write the unit in the answer.</p>" +
        table(["Story", "Operation", "Answer"], [
            ["A 386 g lunch and a 248 g water bottle. Total mass?", "386 + 248", "634 g"],
            ["A 1 L jug of maple syrup. Pour out 250 mL. How much is left?", "1000 − 250", "750 mL"],
            ["6 juice boxes of 200 mL. How much juice?", "6 × 200", "1200 mL"],
            ["24 kg of apples in 4 equal bags. Each bag?", "24 ÷ 4", "6 kg"],
        ]) +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Thinking a bigger object is always heavier", "Check with a balance: the lower pan is heavier"],
            ["Counting every mark on a scale as 1", "Find what one mark is worth: jump ÷ spaces"],
            ["Choosing grams for a heavy object", "Grams for light things, kilograms for heavy things"],
            ["Thinking 1 kg is less than 450 g", "Change to the same unit: 1 kg = 1000 g"],
            ["Thinking more cups means a bigger container", "Check the cup size: small cups give a bigger number"],
            ["Leaving out the unit", "Write g, kg, mL or L after the number"],
        ])
    )


FAQ = [
    {"q": "What do Grade 3 students learn about mass and capacity in Ontario?",
     "a": "In the Ontario math curriculum, Grade 3 students estimate, measure and compare mass in grams and "
          "kilograms and capacity in millilitres and litres. They also explain why a bigger unit gives a smaller number."},
    {"q": "What are good benchmarks for 1 gram, 1 kilogram, 1 millilitre and 1 litre?",
     "a": "A paper clip has a mass of about 1 g, and a 1 L carton of milk has a mass of about 1 kg. "
          "A teaspoon holds about 5 mL, and the carton itself holds 1 L."},
    {"q": "Why do you need more units when the unit is smaller?",
     "a": "Each small unit holds or weighs less, so you need more of them to fill or balance the same object. "
          "A pot might hold 12 small cups but only 6 big cups."},
    {"q": "Is mass and capacity on the Grade 3 EQAO math assessment?",
     "a": "The Grade 3 EQAO math assessment covers all strands of the Ontario curriculum, including Spatial Sense. "
          "Students may be asked to choose units, read scales and jugs, and compare masses and capacities."},
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
    rnd = random.Random(33812)
    sets = [set_units(rnd), set_scale(rnd), set_jug(rnd), set_compare(rnd), set_story(rnd)]
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
        "country": "ca-on", "subject": "math", "grade": "grade-3", "slug": "mass-and-capacity", "sort": 12,
        "updated": UPDATED, "pdf_url": "",
        "title": "Mass and Capacity",
        "seo_title": "Grade 3 Mass and Capacity Worksheets: Grams, Kilograms, Millilitres and Litres (Free, with Answer Key)",
        "short_title": "Mass and capacity",
        "domain": "Spatial Sense",
        "standard_code": "Grade 3: E2.4",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Use various units of mass and capacity to estimate, measure, and compare the masses and "
                         "capacities of objects, and explain how the size of the unit affects the measurement",
        "meta_desc": "Free Grade 3 math worksheets on mass and capacity: choose grams or kilograms, millilitres or "
                     "litres, read scales and measuring jugs, compare on a pan balance and solve word problems. "
                     "100 questions with an answer key, matched to the Ontario curriculum and useful for EQAO.",
        "key_big": "Grams and kilograms tell how heavy. Millilitres and litres tell how much a container holds.",
        "key_sub": "A paper clip is about 1 g and a 1 L carton of milk is about 1 kg. On a scale or a jug, "
                   "find what one mark is worth before you count.",
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
    mark_large(u, "pan balance|level pan balance")
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
