# -*- coding: utf-8 -*-
"""
US Grade 3 Math: Mass and Liquid Volume (3.MD.A.2)
  python tools/gen_us_math_g3_mass_volume.py
HTML attributes use single quotes (no backslashes in the JSON).
Grade 3 uses grams (g), kilograms (kg) and liters (L) only, and no conversions between units.
"""
import json, math, os, random

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "us", "math", "grade-3")
UPDATED = "2026-11-01"
GREEN = "#006633"
FILL = "#cfe6d6"
RED = "#c0392b"
INK = "#2b2b2b"
WATER = "#9fd3f2"
WATER_LINE = "#2a7fb8"
GIRLS = ["Maya", "Ava", "Mia", "Zoe", "Lily", "Emma", "Nora", "Ruby", "Sofia", "Grace"]
BOYS = ["Leo", "Noah", "Eli", "Sam", "Ben", "Omar", "Kai", "Jack", "Luis", "Owen"]


# ------------------------------------------------------------ helpers
def n(v):
    return "{:,}".format(v)


def mcq(q, correct, cands, e, rnd):
    """4 choices: correct + 3 unique distractors (no zero or negative numbers)."""
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        c = str(c)
        lead = c.split(" ")[0]
        if c in seen or not c or lead.startswith("-") or lead == "0":
            continue
        seen.add(c)
        pick.append(c)
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
            "role='img' aria-label='%s'>%s</svg>" % (w, h, w, h, label, body))


def other_unit(u):
    return {"g": "kg", "kg": "g", "L": "kg"}[u]


def marks(k):
    return "%d mark%s" % (k, "" if k == 1 else "s")


class People:
    def __init__(self, rnd):
        self.pool = [(x, "she", "her") for x in GIRLS] + [(x, "he", "his") for x in BOYS]
        rnd.shuffle(self.pool)
        self.i = 0

    def next(self):
        p = self.pool[self.i % len(self.pool)]
        self.i += 1
        return p


def an(w):
    return ("an " if w[0] in "aeiou" else "a ") + w


def cap(s):
    return s[0].upper() + s[1:]


def no_carry_add(a, b):
    """Adding each column but forgetting to regroup."""
    out, place = 0, 1
    while a or b:
        out += ((a % 10 + b % 10) % 10) * place
        a, b, place = a // 10, b // 10, place * 10
    return out


def small_from_big(a, b):
    """Subtracting the smaller digit from the bigger digit in every column."""
    out, place = 0, 1
    while a or b:
        out += abs(a % 10 - b % 10) * place
        a, b, place = a // 10, b // 10, place * 10
    return out


# ------------------------------------------------------------ pictures
def dial_svg(v, mx, lab, tick, unit, size=200):
    """Round scale: 0 at the lower left, the top value at the lower right (270 degrees). Needle exactly at v."""
    c = size / 2.0
    R = c - 6
    def pt(val, r):
        a = math.radians(-135 + 270.0 * val / mx)
        return c + r * math.sin(a), c - r * math.cos(a)
    s = ["<circle cx='%.1f' cy='%.1f' r='%.1f' fill='#fff' stroke='%s' stroke-width='6'/>" % (c, c, R, GREEN)]
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
             % (c, c, nx, ny, RED))
    s.append("<g font-size='%d' font-weight='700' fill='%s' text-anchor='middle' stroke='#fff' stroke-width='4' "
             "paint-order='stroke'>" % (15 if mx >= 1000 else 17, INK))
    for val in range(0, mx + 1, lab):
        x, y = pt(val, R - 36)
        s.append("<text x='%.1f' y='%.1f'>%d</text>" % (x, y + 6, val))
    s.append("</g>")
    s.append("<circle cx='%.1f' cy='%.1f' r='7' fill='%s'/>" % (c, c, RED))
    s.append("<text x='%.1f' y='%.1f' font-size='22' font-weight='800' fill='%s' text-anchor='middle'>%s</text>"
             % (c, c + 62, GREEN, unit))
    return svg_wrap(size, size, "".join(s), "scale with the needle at %d %s" % (v, unit))


def container_svg(v, mx, lab, step, handle="", size=200):
    """Container with a line every `step` liters and a label every `lab` liters. Water exactly at v."""
    x0, x1 = 78, 168                          # inside walls
    yb, yt = 186, 34                          # 0 L and the top line (mx L)
    def Y(val):
        return yb - (yb - yt) * float(val) / mx
    s = []
    if handle == "top":
        s.append("<path d='M%d %d Q%d %d %d %d' fill='none' stroke='%s' stroke-width='4'/>"
                 % (x0 + 4, 20, (x0 + x1) / 2, -14, x1 - 4, 20, INK))
    elif handle == "side":
        s.append("<path d='M%d %d C%d %d %d %d %d %d' fill='none' stroke='%s' stroke-width='6'/>"
                 % (x1, 48, x1 + 34, 48, x1 + 34, 124, x1, 124, INK))
    if v:
        s.append("<rect x='%d' y='%.1f' width='%d' height='%.1f' fill='%s'/>" % (x0, Y(v), x1 - x0, yb - Y(v), WATER))
        s.append("<line x1='%d' y1='%.1f' x2='%d' y2='%.1f' stroke='%s' stroke-width='2.5'/>" % (x0, Y(v), x1, Y(v), WATER_LINE))
    s.append("<path d='M%d %d L%d %d Q%d %d %d %d L%d %d Q%d %d %d %d L%d %d' fill='none' stroke='%s' stroke-width='4' "
             "stroke-linejoin='round'/>" % (x0, 20, x0, yb - 4, x0, yb, x0 + 6, yb, x1 - 6, yb, x1, yb, x1, yb - 4, x1, 20, INK))
    s.append("<g font-size='16' font-weight='700' fill='%s' text-anchor='end'>" % INK)
    for val in range(step, mx + 1, step):
        major = val % lab == 0
        s.append("<line x1='%d' y1='%.1f' x2='%d' y2='%.1f' stroke='%s' stroke-width='%s'/>"
                 % (x0, Y(val), x0 + (22 if major else 12), Y(val), INK, "2.6" if major else "1.6"))
        if major:
            s.append("<text x='%d' y='%.1f'>%d L</text>" % (x0 - 7, Y(val) + 6, val))
    s.append("</g>")
    return svg_wrap(size, size, "".join(s), "container with marks every %d L, water at %d L" % (step, v))


# objects for the balance: (kind, width, height, color)
def draw_obj(kind, cx, yb, w, h, col):
    x, y = cx - w / 2.0, yb - h
    if kind == "weight":
        return ("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' rx='4' fill='%s'/>"
                "<text x='%.1f' y='%.1f' font-size='14' font-weight='700' fill='#fff' text-anchor='middle'>%s</text>"
                % (x, y, w, h, GREEN, cx, yb - 7, col))
    if kind in ("round", "fruit", "pine", "egg"):
        out = "<ellipse cx='%.1f' cy='%.1f' rx='%.1f' ry='%.1f' fill='%s' stroke='%s' stroke-width='1.5'/>" % (cx, yb - h / 2.0, w / 2.0, h / 2.0, col, INK)
        if kind == "fruit":
            out += "<path d='M%.1f %.1f q2 -6 5 -8' stroke='%s' stroke-width='2' fill='none'/>" % (cx, y + 2, INK)
        if kind == "pine":
            out += ("<path d='M%.1f %.1f l-8 -14 l8 6 l0 -12 l6 12 l7 -8 l-5 16 z' fill='%s'/>" % (cx - 3, y + 3, GREEN))
        return out
    if kind == "ball2":                      # beach ball with stripes
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
        return ("<path d='M%.1f %.1f Q%.1f %.1f %.1f %.1f Q%.1f %.1f %.1f %.1f Q%.1f %.1f %.1f %.1f Z' fill='%s' stroke='%s' stroke-width='1.5'/>"
                "<path d='M%.1f %.1f l-5 -7 M%.1f %.1f l5 -7' stroke='%s' stroke-width='2'/>"
                % (x + 6, y + 8, x, yb, x + w / 2.0, yb, x + w, yb, x + w - 6, y + 8, x + w / 2.0, y + 2, x + 6, y + 8, col, INK,
                   cx, y + 7, cx, y + 7, INK))
    if kind == "truck":
        return ("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' rx='3' fill='%s' stroke='%s' stroke-width='1.5'/>"
                "<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' rx='3' fill='%s' stroke='%s' stroke-width='1.5'/>"
                "<circle cx='%.1f' cy='%.1f' r='6' fill='%s'/><circle cx='%.1f' cy='%.1f' r='6' fill='%s'/>"
                % (x, y, w * 0.62, h - 6, col, INK, x + w * 0.62, y + 8, w * 0.38, h - 14, col, INK,
                   x + 12, yb - 6, INK, x + w - 12, yb - 6, INK))
    if kind == "book":
        return ("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' rx='2' fill='%s' stroke='%s' stroke-width='1.5'/>"
                "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='#fff' stroke-width='2'/>"
                % (x, y, w, h, col, INK, x + 6, y + 2, x + 6, yb - 2))
    return ("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' rx='3' fill='%s' stroke='%s' stroke-width='1.5'/>"
            % (x, y, w, h, col, INK))


def weight(v, u):
    t = "%d %s" % (v, u)
    return ("weight", 14 + 8.6 * len(t), 22, t)


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
    """tilt > 0: left side down. Items are (kind, w, h, color_or_text)."""
    W = 360
    LX, RX, PX = 85, 275, 180
    d = 14 * tilt
    pl, pr = pack(left), pack(right)
    hs = max(sum(r[2] for r in pl) + 2 * (len(pl) - 1), sum(r[2] for r in pr) + 2 * (len(pr) - 1))
    piv = 8 + hs + abs(d) + 24
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
                s.append("<text x='%d' y='%d' font-size='16' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                         % (cx, piv + 60, INK, t))
    return svg_wrap(W, H, "".join(s), label)


# ------------------------------------------------------------ set 1: units and estimates
UNIT_CH = {"g": "grams (g)", "kg": "kilograms (kg)", "L": "liters (L)"}


def set_units(rnd):
    its = []
    small = ["cm", "centimeters (cm)"]
    unit_q = [
        ("mass", "a strawberry", "g", "A strawberry is very light, about as heavy as a few paper clips. Light things are measured in grams."),
        ("mass", "a pencil", "g", "A pencil is light. You could hold many in one hand, so grams are the best unit."),
        ("mass", "a key", "g", "A key is small and light, so measure it in grams."),
        ("mass", "a slice of bread", "g", "A slice of bread is light, so grams are the best unit."),
        ("mass", "a bicycle", "kg", "A bicycle is heavy. Heavy things are measured in kilograms."),
        ("mass", "a bag of potatoes", "kg", "A bag of potatoes is heavy, so kilograms are the best unit."),
        ("mass", "a dog", "kg", "A dog is heavy, so measure its mass in kilograms."),
        ("vol", "a bathtub", "L", "How much water a bathtub holds is a liquid volume. Liquid volume is measured in liters."),
        ("vol", "a fish tank", "L", "The water in a fish tank is a liquid volume, so use liters."),
        ("vol", "a kitchen sink", "L", "The water in a sink is a liquid volume, so use liters."),
    ]
    for kind, obj, u, why in unit_q:
        if kind == "mass":
            q = "Which unit is best for measuring the mass of %s?" % obj
            fourth = "centimeters (cm)" if u == "g" else "meters (m)"
            wrongs = [UNIT_CH[x] for x in ("g", "kg", "L") if x != u] + [fourth]
            e = why + " Liters measure liquid, and %s measure length." % fourth.split(" ")[0]
            if u == "g":
                e = why + " Kilograms are for heavy things, and %s measure length." % fourth.split(" ")[0]
        else:
            q = "Which unit is best for measuring how much water %s holds?" % obj
            wrongs = ["grams (g)", "kilograms (kg)", "meters (m)"]
            e = why + " Grams and kilograms measure mass, and meters measure length."
        its.append(mcq(q, UNIT_CH[u], wrongs, e, rnd))
    rnd.shuffle(its)
    est = [
        ("mass of a paper clip", "1 g", ["1 kg", "100 g", "10 kg"], "A paper clip is the benchmark for 1 gram. 1 kg is as heavy as a dictionary."),
        ("mass of a nickel", "5 g", ["5 kg", "50 g", "500 g"], "A nickel has a mass of about 5 grams, about as much as 5 paper clips."),
        ("mass of an apple", "150 g", ["150 kg", "15 kg", "1 g"], "An apple is light but heavier than a paper clip. It is about 150 grams. 150 kg is heavier than a grown-up."),
        ("mass of a dictionary", "1 kg", ["1 g", "10 kg", "100 kg"], "A big dictionary is the benchmark for 1 kilogram. 1 g is only a paper clip."),
        ("mass of a bicycle", "15 kg", ["15 g", "150 kg", "1 kg"], "A bicycle is about as heavy as 15 dictionaries, so about 15 kg. 15 g is as light as a few coins."),
        ("mass of a watermelon", "5 kg", ["5 g", "50 kg", "500 g"], "A watermelon is about as heavy as 5 dictionaries, so about 5 kg."),
        ("mass of a pet cat", "4 kg", ["4 g", "40 kg", "400 kg"], "A cat is about as heavy as 4 dictionaries, so about 4 kg. 40 kg is as heavy as a big dog."),
        ("liquid volume of a large milk jug", "4 L", ["40 L", "400 L", "4 g"], "A large milk jug holds about as much as 4 one-liter bottles, so about 4 L. Grams measure mass, not liquid."),
        ("liquid volume of a bucket", "10 L", ["1 L", "100 L", "10 g"], "A bucket holds about 10 one-liter bottles of water, so about 10 L."),
        ("liquid volume of a full bathtub", "150 L", ["15 L", "1,500 L", "1 L"], "A bathtub holds a lot of water, about 150 L. 15 L is only a bucket and a half."),
    ]
    its2 = []
    for what, ans, wr, e in est:
        its2.append(mcq("What is the best estimate for the %s?" % what, ans, wr, e, rnd))
    rnd.shuffle(its2)
    return {"title": "Choose the unit and estimate", "items": its + its2}


# ------------------------------------------------------------ set 2: read a scale
DIALS = [  # (max, label step, tick step, unit, [(object, lo, hi)], how many)
    (10, 2, 1, "kg", [("a pumpkin", 3, 9), ("a bag of potatoes", 3, 9), ("a watermelon", 5, 9)], 3),
    (20, 5, 1, "kg", [("a bag of dog food", 8, 19), ("a box of books", 11, 19), ("a car tire", 9, 13)], 3),
    (50, 10, 2, "kg", [("a big dog", 22, 38), ("a sack of rice", 22, 28)], 2),
    (100, 20, 5, "kg", [("a third grader", 25, 35), ("a grown-up", 55, 85)], 2),
    (500, 100, 20, "g", [("a bunch of grapes", 220, 480), ("a bag of carrots", 240, 480)], 2),
    (1000, 200, 50, "g", [("a loaf of bread", 450, 700), ("a bag of apples", 650, 950)], 2),
    (200, 50, 10, "g", [("a tennis ball", 60, 60), ("an orange", 130, 190)], 2),
]


def tick_e(v, lab, tick, unit):
    base = v - v % lab
    k = (v - base) // tick
    sp = lab // tick
    s = "The numbers go up by %d %s. There are %d spaces between numbers, so each small mark is %d %s. " % (lab, unit, sp, tick, unit)
    if k == 0:
        return s + "The needle points right at %d %s." % (v, unit)
    if base == 0:
        return s + "The needle is %s past 0: %d × %d = %d %s." % (marks(k), k, tick, v, unit)
    return s + "The needle is %s past %d: %d + %d = %d %s." % (marks(k), base, base, k * tick, v, unit)


def read_cands(v, mx, lab, tick, unit, i):
    base = v - v % lab
    k = (v - base) // tick
    c = []
    if tick != 1:
        c.append(base + k)                          # every mark counted as 1
    else:
        c.append(base + 2 * k)                      # every mark counted as 2
    c += [v + tick, v - tick]                       # one mark off
    c = ["%s %s" % (n(x), unit) for x in c if 0 < x <= mx]
    swap = "%s %s" % (n(v), other_unit(unit))
    c.insert(1 if i % 3 == 0 else 3, swap)
    c.append("%s %s" % (n(base + lab), unit))
    return c


def set_scale(rnd):
    its = []
    i = 0
    for mx, lab, tick, unit, objs, cnt in DIALS:
        used = set()
        while len(used) < cnt:
            obj, lo, hi = rnd.choice(objs)
            vals = [x for x in range(lo, hi + 1) if x % tick == 0 and (x % lab or lo == hi) and x not in used]
            if not vals:
                continue
            v = rnd.choice(vals)
            used.add(v)
            its.append(mcq(fig(dial_svg(v, mx, lab, tick, unit)) + "The scale shows the mass of %s. What is the mass?" % obj,
                           "%s %s" % (n(v), unit), read_cands(v, mx, lab, tick, unit, i), tick_e(v, lab, tick, unit), rnd))
            i += 1
    rnd.shuffle(its)
    # read the scale, then subtract the container
    extra = [
        (500, 100, 20, "g", "a bowl of cherries", "the empty bowl", 120, "the cherries", 260, 480),
        (1000, 200, 50, "g", "a basket of apples", "the empty basket", 150, "the apples", 650, 950),
        (20, 5, 1, "kg", "a box of books", "the empty box", 2, "the books", 11, 19),
        (50, 10, 2, "kg", "a suitcase full of clothes", "the empty suitcase", 4, "the clothes", 16, 28),
    ]
    its2 = []
    for mx, lab, tick, unit, whole, empty, cm, part, lo, hi in extra:
        v = rnd.choice([x for x in range(lo, hi + 1) if x % tick == 0 and x % lab])
        a = v - cm
        base = v - v % lab
        k = (v - base) // tick
        mis = (base + k if tick != 1 else base + 2 * k) - cm
        its2.append(mcq(fig(dial_svg(v, mx, lab, tick, unit)) +
                        "The scale shows %s. The mass of %s is %d %s. What is the mass of %s?" % (whole, empty, cm, unit, part),
                        "%s %s" % (n(a), unit),
                        ["%s %s" % (n(x), unit) for x in [v, v + cm, mis, a + tick]],
                        "Read the scale: each small mark is %d %s, so the needle is at %s %s. "
                        "Take away %s: %s − %d = %s %s." % (tick, unit, n(v), unit, empty, n(v), cm, n(a), unit), rnd))
    return {"title": "Read a scale", "items": its + its2}


# ------------------------------------------------------------ set 3: read a container
CONT = [  # (max, label step, line step, name, handle, how many to read, how many "to fill")
    (5, 1, 1, "jug", "side", 2, 1),
    (10, 2, 1, "bucket", "top", 3, 2),
    (20, 10, 2, "water cooler", "", 3, 1),
    (50, 10, 5, "fish tank", "", 3, 1),
    (100, 20, 10, "rain barrel", "", 3, 1),
]


def lines_e(v, lab, step):
    base = v - v % lab
    k = (v - base) // step
    sp = lab // step
    if step == lab:
        return "Every line has a number. The water is at the %d L line." % v
    s = "The numbers go up by %d L. There are %d spaces between numbers, so each line is %d L. " % (lab, sp, step)
    if k == 0:
        return s + "The water is right at the %d L line." % v
    if base == 0:
        return s + "The water is %d line%s up from the bottom: %d × %d = %d L." % (k, "" if k == 1 else "s", k, step, v)
    return s + "The water is %d line%s above %d L: %d + %d = %d L." % (k, "" if k == 1 else "s", base, base, k * step, v)


def set_container(rnd):
    its, its2 = [], []
    for mx, lab, step, name, handle, nr, nf in CONT:
        vals = [x for x in range(step, mx, step)]
        off = [x for x in vals if x % lab] or vals
        on = [x for x in vals if x % lab == 0 and x != mx]
        pick = rnd.sample(off, min(nr, len(off)))
        if len(pick) < nr:
            pick += rnd.sample([x for x in vals if x not in pick], nr - len(pick))
        if on and nr >= 3:
            pick[-1] = rnd.choice(on)              # one on a numbered line
        rest = [x for x in vals if x not in pick]
        fill = rnd.sample(rest, nf)
        for v in pick:
            base = v - v % lab
            k = (v - base) // step
            c = [base + k if step != 1 else base + 2 * k, v + step, v - step, mx - v]
            c = ["%d L" % x for x in c if 0 < x <= mx]
            c.insert(2, "%d kg" % v)
            its.append(mcq(fig(container_svg(v, mx, lab, step, handle)) + "How much water is in the %s?" % name,
                           "%d L" % v, c, lines_e(v, lab, step), rnd))
        for v in fill:
            a = mx - v
            its2.append(mcq(fig(container_svg(v, mx, lab, step, handle)) +
                            "The %s is full when the water reaches the top line, %d L. How many more liters are needed to fill it?" % (name, mx),
                            "%d L" % a, ["%d L" % x for x in [v, a + step, a - step, mx + v, mx]],
                            "The water is at %d L. The top line is %d L. %d − %d = %d L more." % (v, mx, mx, v, a), rnd))
    rnd.shuffle(its)
    rnd.shuffle(its2)
    return {"title": "Read liquid volume", "items": its + its2}


# ------------------------------------------------------------ set 4: balance
OBJ = {  # name: (kind, w, h, color)
    "apple": ("fruit", 30, 28, "#d9483b"), "orange": ("round", 30, 30, "#f39c12"),
    "book": ("book", 66, 18, "#3a6fb0"), "pencil case": ("box", 62, 18, "#8e5bb5"),
    "can of soup": ("jar", 30, 38, "#c8ccd0"), "watermelon": ("round", 72, 46, "#3f9a4a"),
    "pumpkin": ("round", 58, 40, "#e67e22"), "bag of rice": ("bag", 46, 44, "#efe2c0"),
    "bowling ball": ("round", 38, 38, "#34495e"), "egg": ("egg", 18, 24, "#f3e3c3"),
    "lemon": ("round", 26, 20, "#f1d23a"), "potato": ("round", 32, 22, "#b5835a"),
    "tennis ball": ("round", 22, 22, "#c7e04a"), "melon": ("round", 48, 40, "#bcd96b"),
    "brick": ("box", 54, 24, "#b5523b"), "sack of potatoes": ("bag", 52, 50, "#c9a46b"),
    "pineapple": ("pine", 32, 44, "#e2b13c"), "jar of jam": ("jar", 30, 36, "#a3324a"),
    "box of crayons": ("box", 50, 26, "#f4c542"), "toy truck": ("truck", 62, 32, "#c0392b"),
    "beach ball": ("ball2", 60, 60, ""), "sponge": ("box", 54, 24, "#f7dc6f"),
    "dictionary": ("book", 66, 26, "#7b3f2a"), "notebook": ("book", 60, 8, "#5dade2"),
}


def o(name):
    return OBJ[name]


def set_balance(rnd):
    its = []
    # A: object balances weights
    bal = [("apple", 150, "g", [100, 50]), ("orange", 200, "g", [100, 50, 50]), ("book", 600, "g", [500, 100]),
           ("pencil case", 250, "g", [200, 50]), ("can of soup", 400, "g", [200, 200]),
           ("watermelon", 6, "kg", [5, 1]), ("pumpkin", 4, "kg", [2, 2]), ("bag of rice", 3, "kg", [2, 1]),
           ("bowling ball", 7, "kg", [5, 2])]
    for name, m, u, ws in rnd.sample(bal, 7):
        assert sum(ws) == m
        its.append(mcq(fig(balance_svg([o(name)], [weight(x, u) for x in ws], 0, name, "",
                                        "balance with %s and weights" % an(name))) +
                       "The pan balance is level. What is the mass of the %s?" % name,
                       "%d %s" % (m, u), ["%d %s" % (ws[0], u), "%d %s" % (m, other_unit(u)),
                                          "%d %s" % (m + ws[-1], u), "%d %s" % (len(ws), u), "%d %s" % (m - ws[-1], u)],
                       "The pans are level, so the %s has the same mass as the weights: %s = %d %s."
                       % (name, " + ".join(str(x) for x in ws), m, u), rnd))
    # B: identical objects balance weights -> divide
    same = [("egg", "eggs", 3, 50, "g", [100, 50]), ("apple", "apples", 4, 150, "g", [500, 100]),
            ("lemon", "lemons", 5, 100, "g", [500]), ("tennis ball", "tennis balls", 4, 60, "g", [200, 20, 20]),
            ("melon", "melons", 2, 2, "kg", [2, 2]), ("brick", "bricks", 3, 2, "kg", [5, 1]),
            ("potato", "potatoes", 3, 200, "g", [500, 100])]
    for one, many, k, m, u, ws in rnd.sample(same, 5):
        t = k * m
        assert sum(ws) == t
        its.append(mcq(fig(balance_svg([o(one)] * k, [weight(x, u) for x in ws], 0, "%d %s" % (k, many), "",
                                        "balance with %d %s and weights" % (k, many))) +
                       "The pan balance is level. The %s all have the same mass. What is the mass of 1 %s?" % (many, one),
                       "%d %s" % (m, u), ["%s %s" % (n(x), u) for x in [t, t - k, t * k, t + k]],
                       "The weights show %s = %d %s for %s %s. Share it equally: %d ÷ %d = %d %s."
                       % (" + ".join(str(x) for x in ws), t, u, "both" if k == 2 else "all %d" % k, many, t, k, m, u) if len(ws) > 1 else
                       "The weight shows %d %s for all %d %s. Share it equally: %d ÷ %d = %d %s." % (t, u, k, many, t, k, m, u), rnd))
    # C: object + weight on one side
    plus = [("sack of potatoes", 4, "kg", 1, [5]), ("pineapple", 2, "kg", 1, [2, 1]), ("jar of jam", 350, "g", 50, [200, 200]),
            ("box of crayons", 150, "g", 50, [200]), ("toy truck", 700, "g", 100, [500, 200, 100])]
    for name, m, u, lw, ws in rnd.sample(plus, 4):
        R = sum(ws)
        assert m + lw == R
        its.append(mcq(fig(balance_svg([o(name), weight(lw, u)], [weight(x, u) for x in ws], 0, name, "",
                                        "balance with %s and a weight" % an(name))) +
                       "The pan balance is level. What is the mass of the %s?" % name,
                       "%d %s" % (m, u), ["%d %s" % (x, u) for x in [R, R + lw, lw]] + ["%d %s" % (m, other_unit(u))],
                       "The right pan has %d %s. The left pan has the %s and %d %s. %d − %d = %d %s for the %s."
                       % (R, u, name, lw, u, R, lw, m, u, name), rnd))
    # D: which is heavier / lighter (the lower pan is heavier)
    pairs = [("watermelon", "orange"), ("bowling ball", "beach ball"), ("brick", "sponge"), ("dictionary", "notebook")]
    plan = [("heavier", 1), ("lighter", -1), ("heavier", -1), ("lighter", 1)]
    for (hv, lt), (word, side) in zip(pairs, plan):
        L, Rn = (hv, lt) if side == 1 else (lt, hv)
        ans = hv if word == "heavier" else lt
        wrong = lt if word == "heavier" else hv
        down = "left" if side == 1 else "right"
        e = ("The %s side is lower. The lower pan holds the heavier object, so the %s is heavier and the %s is lighter."
             % (down, hv, lt))
        if (hv, lt) == ("bowling ball", "beach ball"):
            e += " A bigger object is not always heavier."
        its.append(mcq(fig(balance_svg([o(L)], [o(Rn)], side, L, Rn, "balance with %s and %s, %s side down" % (an(L), an(Rn), down))) +
                       "Look at the pan balance. Which object is %s?" % word,
                       "the %s" % ans, ["the %s" % wrong, "They are the same", "You cannot tell"], e, rnd))
    a, b, c, d = its[:7], its[7:12], its[12:16], its[16:]
    rnd.shuffle(a)
    return {"title": "Pan balances", "items": d[:2] + a + d[2:] + b + c}


# ------------------------------------------------------------ set 5: word problems
def set_story(rnd):
    P = People(rnd)
    its = []

    def add(q, ans, u, wrong, e):
        its.append(mcq(q, "%s %s" % (n(ans), u), ["%s %s" % (n(x), uu) for x, uu in wrong], e, rnd))

    nm, he, his = P.next()
    a, b = rnd.randint(31, 48) * 10 + rnd.randint(4, 9), rnd.randint(12, 26) * 10 + rnd.randint(5, 9)
    add("%s puts a book with a mass of %d g and a pencil case with a mass of %d g in %s backpack. "
        "What is the total mass of the two things?" % (nm, a, b, his), a + b, "g",
        [(a - b, "g"), (no_carry_add(a, b), "g"), (a + b, "kg"), (a + b + 100, "g")],
        "Put the masses together: %d + %d = %d g." % (a, b, a + b))
    a = rnd.randint(4, 8); b = a + rnd.randint(3, 9)
    add("A puppy had a mass of %d kg in the spring. Now it has a mass of %d kg. How many kilograms did it gain?" % (a, b),
        b - a, "kg", [(a + b, "kg"), (b, "kg"), (a, "kg")],
        "Find the difference: %d − %d = %d kg." % (b, a, b - a))
    k, m = rnd.randint(4, 9), rnd.randint(2, 5)
    add("A store has %d bags of rice. Each bag has a mass of %d kg. What is the total mass of the rice?" % (k, m),
        k * m, "kg", [(k + m, "kg"), (k * m, "g"), (k * (m + 1), "kg")],
        "%d equal bags of %d kg: %d × %d = %d kg." % (k, m, k, m, k * m))
    s, g = rnd.randint(4, 9), rnd.randint(3, 6)
    t = s * g
    nm, he, his = P.next()
    add("%s has %d kg of potatoes. %s puts them into %d sacks with the same mass. What is the mass of each sack?" % (nm, t, cap(he), g),
        s, "kg", [(t - g, "kg"), (t + g, "kg"), (t * g, "kg")],
        "Share %d kg equally into %d sacks: %d ÷ %d = %d kg." % (t, g, t, g, s))
    a, b = rnd.randint(21, 38), rnd.randint(16, 19)
    nm, he, his = P.next()
    add("A fish tank has %d L of water. %s adds %d L more. How much water is in the tank now?" % (a, nm, b),
        a + b, "L", [(a - b, "L"), (no_carry_add(a, b), "L"), (a + b, "kg"), (a + b + 1, "L")],
        "Adding more means add: %d + %d = %d L." % (a, b, a + b))
    a, b = rnd.randint(131, 175), rnd.randint(46, 89)
    while (a % 10) >= (b % 10) or a - b == b:
        b = rnd.randint(46, 89)
    add("A bathtub had %d L of water. Then %d L drained out. How much water is left in the bathtub?" % (a, b),
        a - b, "L", [(a + b, "L"), (small_from_big(a, b), "L"), (b, "L"), (a - b - 10, "L")],
        "Water went out, so subtract: %d − %d = %d L." % (a, b, a - b))
    c, k = rnd.randint(4, 9), rnd.randint(3, 8)
    nm, he, his = P.next()
    add("%s's watering can holds %d L. %s fills it %d times to water the garden. How many liters of water does %s use?"
        % (nm, c, cap(he), k, he), c * k, "L", [(c + k, "L"), (c * k - c, "L"), (c * k + c, "L")],
        "%d times %d L: %d × %d = %d L." % (k, c, k, c, c * k))
    s, g = rnd.randint(5, 9), rnd.randint(3, 4)
    t = s * g
    add("A coach mixes %d L of sports drink. The coach pours the same amount into %d coolers. How many liters go into each cooler?" % (t, g),
        s, "L", [(t - g, "L"), (t + g, "L"), (t * g, "L")],
        "Share equally: %d ÷ %d = %d L in each cooler." % (t, g, s))
    e, w = rnd.randint(2, 4), rnd.randint(5, 9)
    t = e * w
    nm, he, his = P.next()
    add("A bag of dog food has %d kg of food. %s's dog eats %d kg each week. How many weeks will the bag last?" % (t, nm, e),
        w, "weeks", [(t - e, "weeks"), (t + e, "weeks"), (t * e, "weeks")],
        "How many groups of %d kg are in %d kg? %d ÷ %d = %d weeks." % (e, t, t, e, w))
    b, k = rnd.choice([5, 10]), rnd.randint(4, 8)
    T = b * k
    add("A bucket holds %d L. How many full buckets of water are needed to fill a tank that holds %d L?" % (b, T),
        k, "buckets", [(T - b, "buckets"), (T + b, "buckets"), (k + 1, "buckets")],
        "How many %d L buckets make %d L? %d ÷ %d = %d buckets." % (b, T, T, b, k))
    a, b = rnd.randint(12, 16), rnd.randint(3, 6)
    nm, he, his = P.next()
    add("%s's bicycle has a mass of %d kg. %s scooter has a mass of %d kg. How much heavier is the bicycle?" % (nm, a, cap(his), b),
        a - b, "kg", [(a + b, "kg"), (a, "kg"), (b, "kg")],
        "“How much heavier” compares two masses, so subtract: %d − %d = %d kg." % (a, b, a - b))
    k = rnd.randint(4, 9)
    add("One egg has a mass of about 50 g. What is the mass of %d eggs?" % k,
        50 * k, "g", [(50 + k, "g"), (50 * k, "kg"), (50 * (k - 1), "g")],
        "%d equal groups of 50 g: %d × 50 = %d g." % (k, k, 50 * k))
    a = rnd.randint(16, 34) * 10 + rnd.randint(1, 9)
    while (a % 10) == 0:
        a += 1
    add("A small wading pool holds 400 L when it is full. It has %d L of water in it now. How many more liters are needed to fill it?" % a,
        400 - a, "L", [(400 + a, "L"), (a, "L"), (400 - a + 10, "L")],
        "Find the missing part: 400 − %d = %d L." % (a, 400 - a))
    f, d = rnd.randint(4, 8), rnd.randint(5, 7)
    add("A baker uses %d kg of flour each day. How many kilograms of flour does the baker use in %d days?" % (f, d),
        f * d, "kg", [(f + d, "kg"), (f * d, "g"), ((d - 1) * f, "kg")],
        "%d days of %d kg: %d × %d = %d kg." % (d, f, d, f, f * d))
    s, g = rnd.randint(4, 8), rnd.randint(6, 8)
    t = s * g
    nm, he, his = P.next()
    add("%s picks %d kg of apples. %s packs them into %d bags with the same mass. What is the mass of each bag?" % (nm, t, cap(he), g),
        s, "kg", [(t - g, "kg"), (t + g, "kg"), (s, "g")],
        "Share equally: %d ÷ %d = %d kg in each bag." % (t, g, s))
    f, e2 = rnd.randint(6, 9), rnd.randint(1, 2)
    nm, he, his = P.next()
    add("%s's backpack full of books has a mass of %d kg. The empty backpack has a mass of %d kg. What is the mass of the books?"
        % (nm, f, e2), f - e2, "kg", [(f + e2, "kg"), (f, "kg"), (e2, "kg")],
        "Take away the backpack: %d − %d = %d kg." % (f, e2, f - e2))
    a, b = rnd.randint(25, 58), rnd.randint(15, 39)
    while (a % 10) + (b % 10) < 10:
        b = rnd.randint(15, 39)
    add("A rain barrel had %d L of water. A storm added %d L. How much water is in the barrel now?" % (a, b),
        a + b, "L", [(a - b if a > b else b - a, "L"), (no_carry_add(a, b), "L"), (a + b, "kg")],
        "Add the water that came in: %d + %d = %d L." % (a, b, a + b))
    k = rnd.randint(6, 9)
    nm, he, his = P.next()
    add("%s buys %d bottles of water for a picnic. Each bottle holds 2 L. How many liters of water does %s buy?" % (nm, k, he),
        2 * k, "L", [(k + 2, "L"), (k, "L"), (2 * (k + 1), "L")],
        "%d bottles of 2 L: %d × 2 = %d L." % (k, k, 2 * k))
    c, g = rnd.choice([20, 30, 40]), rnd.randint(4, 8)
    t = c * g
    add("A box holds %d toy cars that all have the same mass. Together the cars have a mass of %d g. What is the mass of 1 toy car?" % (g, t),
        c, "g", [(t - g, "g"), (t + g, "g"), (c, "kg")],
        "Share the mass equally: %d ÷ %d = %d g." % (t, g, c))
    a, b = rnd.randint(82, 95) * 10, rnd.randint(21, 44) * 10 + rnd.randint(1, 9)
    nm, he, his = P.next()
    add("A bag had %d g of flour. %s used %d g to bake bread. How much flour is left in the bag?" % (a, nm, b),
        a - b, "g", [(a + b, "g"), (small_from_big(a, b), "g"), (b, "g"), (a - b + 10, "g")],
        "Flour was used up, so subtract: %d − %d = %d g." % (a, b, a - b))
    rnd.shuffle(its)
    return {"title": "Word problems with mass and volume", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


def body_html():
    return (
        "<h2>Mass and liquid volume</h2>"
        "<p><b>Mass</b> tells how heavy something is. We measure it in <b>grams (g)</b> for light things and "
        "<b>kilograms (kg)</b> for heavy things. <b>Liquid volume</b> tells how much liquid a container holds. "
        "We measure it in <b>liters</b>. You may see liters written as <b>l</b> or <b>L</b>. Both mean liter. "
        "This page uses L.</p>"
        "<h2>Benchmarks: know what 1 unit feels like</h2>"
        "<p>Compare a new object with something you know. Then choose the unit and a sensible number.</p>" +
        table(["Unit", "About the same as", "More examples"], [
            ["1 gram (g)", "a paper clip", "a nickel is about 5 g, an apple about 150 g"],
            ["1 kilogram (kg)", "a big dictionary", "a watermelon is about 5 kg, a bicycle about 15 kg"],
            ["1 liter (L)", "a large water bottle", "a milk jug holds about 4 L, a bucket about 10 L"],
        ]) +
        "<h2>Read a scale</h2>"
        "<p>Not every mark has a number. First find <b>what each small mark is worth</b>, then count from the "
        "number just before the needle.</p>"
        "<figure class='sn-fig'>" + dial_svg(340, 500, 100, 20, "g") +
        "<figcaption>The numbers go up by 100 g and there are 5 spaces between them, so each mark is 20 g. "
        "The needle is 2 marks past 300: 340 g.</figcaption></figure>" +
        ex("Example", "A scale has a number every 10 kg and 5 spaces between numbers. The needle is 3 marks past 20. What is the mass?",
           "Each mark is 10 ÷ 5 = 2 kg. 3 marks are 6 kg. 20 + 6 = 26.", "26 kg") +
        "<h2>Read a container</h2>"
        "<p>Read the line at the <b>top of the water</b>. Use the same rule: find what each line is worth.</p>"
        "<figure class='sn-fig'>" + container_svg(7, 10, 2, 1, "top") +
        "<figcaption>There is a line every 1 L. The water is at 7 L.</figcaption></figure>"
        "<h2>Solve word problems</h2>"
        "<p>All the amounts in a Grade 3 problem use the <b>same unit</b>. Decide what is happening, then add, "
        "subtract, multiply or divide. Write the unit in the answer.</p>" +
        table(["Story", "Operation", "Answer"], [
            ["A 345 g book and a 278 g lunch box. Total mass?", "345 + 278", "623 g"],
            ["A tub had 150 L. 60 L drained out. How much is left?", "150 − 60", "90 L"],
            ["6 bags of flour, 2 kg each. Total mass?", "6 × 2", "12 kg"],
            ["24 L of juice shared equally into 4 jugs. Each jug?", "24 ÷ 4", "6 L"],
        ]) +
        "<p>On a pan balance, the <b>lower pan is heavier</b>. When the pans are level, both sides have the same mass.</p>"
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Counting every mark as 1", "Check what one mark is worth: numbers ÷ spaces"],
            ["Choosing grams for a heavy object", "Grams for light things, kilograms for heavy things"],
            ["Using grams or kilograms for water in a tub", "Liquid in a container is measured in liters"],
            ["Thinking the higher pan is heavier", "The heavier side goes down"],
            ["Leaving out the unit", "Write g, kg or L after the number"],
        ])
    )


FAQ = [
    {"q": "What is the difference between grams and kilograms?",
     "a": "Both measure mass. A gram is very light, about the mass of a paper clip. A kilogram is 1,000 grams, about the mass of a big dictionary, so it is used for heavier things."},
    {"q": "What are good benchmarks for 1 gram, 1 kilogram and 1 liter?",
     "a": "A paper clip is about 1 gram, a big dictionary is about 1 kilogram, and a large water bottle holds about 1 liter. Children compare new objects with these to make estimates."},
    {"q": "How do you read a scale in 3rd grade math?",
     "a": "Find two numbers next to each other and count the spaces between them. Divide to find what each mark is worth, then count the marks from the number just before the needle."},
    {"q": "Do 3rd graders convert between grams and kilograms?",
     "a": "No. In standard 3.MD.A.2, word problems use the same unit throughout. Converting units, such as kilograms to grams, starts in Grade 4."},
]


def gen_mass_volume():
    rnd = random.Random(43)
    sets = [set_units(rnd), set_scale(rnd), set_container(rnd), set_balance(rnd), set_story(rnd)]
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
    return {
        "country": "us", "subject": "math", "grade": "grade-3", "slug": "mass-and-volume", "sort": 13,
        "updated": UPDATED, "pdf_url": "",
        "title": "Mass and Liquid Volume",
        "seo_title": "Grade 3 Mass and Liquid Volume Worksheets: Grams, Kilograms, Liters, Scales and Word Problems",
        "short_title": "Mass and volume",
        "domain": "Measurement and Data",
        "standard_code": "3.MD.A.2",
        "standard_url": "https://www.thecorestandards.org/Math/Content/3/MD/A/2/",
        "standard_text": "Measure and estimate liquid volumes and masses of objects using standard units of grams (g), kilograms (kg), and liters (l). Add, subtract, multiply, or divide to solve one-step word problems involving masses or volumes that are given in the same units.",
        "meta_desc": "Free Grade 3 mass and liquid volume worksheets: choose grams, kilograms or liters, estimate with benchmarks, read scales and containers, use a pan balance, and solve one-step word problems. 100 practice questions with answers.",
        "key_big": "Grams and kilograms tell how heavy. Liters tell how much liquid.",
        "key_sub": "A paper clip is about 1 g, a dictionary about 1 kg, and a large water bottle about 1 L. On a scale, find what one mark is worth before you count.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen_mass_volume()
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(u, f, ensure_ascii=False, indent=1)
    print("wrote", path)
