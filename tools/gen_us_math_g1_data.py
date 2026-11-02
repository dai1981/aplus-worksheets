# -*- coding: utf-8 -*-
"""
US Grade 1 Math: Organize, Represent and Interpret Data (1.MD.C.4)
  python tools/gen_us_math_g1_data.py
Up to three categories, counts up to 15, totals up to 20. Sort and count, tally charts,
picture graphs (each picture = 1), bar graphs (count by 1s) and short word problems.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, re, math, os, random

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "us", "math", "grade-1")
UPDATED = "2026-11-02"
GREEN = "#006633"
BAR = "#2e8b57"
RED = "#c0392b"
INK = "#2b2b2b"
GRID = "#c9d3cc"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Maya", "Ava", "Mia", "Zoe", "Lily", "Emma", "Nora", "Ruby"]
BOYS = ["Leo", "Noah", "Eli", "Sam", "Ben", "Omar", "Kai", "Jack"]
MINUS = "−"


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e):
    """4 choices: correct + the first 3 unique distractors (no zero or negative numbers)."""
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        if c is None:
            continue
        c = str(c)
        lead = c.split(" ")[0]
        if c in seen or not c or lead.startswith("-") or lead == "0":
            continue
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    return {"q": q, "c": [correct] + pick, "a": 0, "e": e}


def balance(sets, rnd):
    """Spread the correct answers evenly (5/5/5/5) over the 4 positions in every set.
    Items marked 'fixed' (A-D pictures) already have their position; the rest fill the gaps."""
    for s in sets:
        left = {0: 5, 1: 5, 2: 5, 3: 5}
        for it in s["items"]:
            if it.get("fixed"):
                left[it["a"]] -= 1
        assert min(left.values()) >= 0
        targets = [p for p in range(4) for _ in range(left[p])]
        rnd.shuffle(targets)
        free = [it for it in s["items"] if not it.get("fixed")]
        assert len(free) == len(targets)
        for it, t in zip(free, targets):
            c = it["c"]
            wrong = [x for i, x in enumerate(c) if i != it["a"]]
            rnd.shuffle(wrong)
            right = c[it["a"]]
            it["c"] = wrong[:t] + [right] + wrong[t:]
            it["a"] = t
        for it in s["items"]:
            it.pop("fixed", None)


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def tw(t, fs, bold=False):
    """Approximate text width in px (Arial)."""
    return len(str(t)) * fs * (0.62 if bold else 0.58)


def text(x, y, t, fs=14, anchor="middle", bold=False, col=INK, extra=""):
    return ("<text x='%.1f' y='%.1f' font-size='%d'%s fill='%s' text-anchor='%s'%s>%s</text>"
            % (x, y, fs, " font-weight='700'" if bold else "", col, anchor, extra, t))


def fmt(v, unit):
    """unit = (singular, plural)."""
    return "%d %s" % (v, unit[0] if v == 1 else unit[1])


def cap(s):
    return s[0].upper() + s[1:]


def plus(vals):
    return " + ".join(str(v) for v in vals)


def minus(a, b):
    return "%d %s %d = %d" % (a, MINUS, b, a - b)


class People:
    def __init__(self, rnd):
        self.pool = [(n, "she", "her") for n in GIRLS] + [(n, "he", "his") for n in BOYS]
        rnd.shuffle(self.pool)
        self.i = 0

    def next(self, avoid=()):
        while True:
            p = self.pool[self.i % len(self.pool)]
            self.i += 1
            if p[0] not in avoid:
                return dict(N=p[0], he=p[1], He=cap(p[1]), his=p[2], His=cap(p[2]))


# ------------------------------------------------------------ symbols / shapes
def star_pts(cx, cy, R=9.5, r=4.0):
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rad = R if i % 2 == 0 else r
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    return pts


def symbol(kind, cx, cy, col=GREEN, k=1.0):
    """Small shape centred on (cx, cy). k scales it."""
    if kind == "circle":
        return "<circle cx='%.1f' cy='%.1f' r='%.1f' fill='%s'/>" % (cx, cy, 8.5 * k, col)
    if kind == "square":
        h = 7.5 * k
        return "<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' rx='2' fill='%s'/>" % (cx - h, cy - h, 2 * h, 2 * h, col)
    if kind == "triangle":
        h = 9.5 * k
        return "<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='%s'/>" % (
            cx, cy - h, cx + h, cy + h * 0.8, cx - h, cy + h * 0.8, col)
    if kind == "heart":
        return ("<path d='M%.1f %.1f C%.1f %.1f %.1f %.1f %.1f %.1f C%.1f %.1f %.1f %.1f %.1f %.1f Z' fill='%s'/>"
                % (cx, cy + 8 * k, cx - 12 * k, cy - 1 * k, cx - 6 * k, cy - 11 * k, cx, cy - 4 * k,
                   cx + 6 * k, cy - 11 * k, cx + 12 * k, cy - 1 * k, cx, cy + 8 * k, col))
    return "<polygon points='%s' fill='%s'/>" % (" ".join("%.1f,%.1f" % p for p in star_pts(cx, cy, 9.5 * k, 4.0 * k)), col)


SYMS = ["circle", "star", "square", "heart"]
SHAPES = ["circle", "square", "triangle", "star", "heart"]
SHAPE_COL = {"circle": "#2e8b57", "square": "#2e6fb0", "triangle": "#d9822b", "star": "#c9a227", "heart": "#c0392b"}
SHAPE_PL = {s: s + "s" for s in SHAPES}


def mixed_svg(kinds, vals, rnd, label="mixed shapes to sort", cols=6):
    """Shapes scattered (one per cell, small jitter) so they must be sorted before counting."""
    n = sum(vals)
    rows = int(math.ceil(n / float(cols)))
    if rows * cols - n < 2:
        rows += 1
    cells = rnd.sample(range(rows * cols), n)
    items = []
    for kd, v in zip(kinds, vals):
        items += [kd] * v
    rnd.shuffle(items)
    cw = 36
    W, H = cols * cw + 8, rows * cw + 8
    s = ["<rect x='1' y='1' width='%d' height='%d' rx='8' fill='#f6faf7' stroke='%s' stroke-width='1.5'/>" % (W - 2, H - 2, GRID)]
    for kd, c in zip(items, cells):
        r, cc = divmod(c, cols)
        cx = 4 + cc * cw + cw / 2 + rnd.choice([-3, -1, 0, 1, 3])
        cy = 4 + r * cw + cw / 2 + rnd.choice([-3, -1, 0, 1, 3])
        s.append(symbol(kd, cx, cy, SHAPE_COL[kd], 1.15))
    return svg_wrap(W, H, "".join(s), label)


# ------------------------------------------------------------ contexts
class Ctx:
    def __init__(self, title, axis, cats, unit, f, ph=None, sumto=None, names=False):
        self.title, self.axis, self.cats, self.unit = title, axis, cats, unit
        self.f, self.ph, self.sumto, self.names = f, ph or {}, sumto, names

    def p(self, c):
        return self.ph.get(c, c)

    def q(self, kind, a=None, b=None, w=None, v=None):
        return self.f[kind].format(a=self.p(a) if a else "", b=self.p(b) if b else "",
                                   w=w or "", v=v if v is not None else "",
                                   n=fmt(v, self.unit) if v is not None else "")

    def has(self, kind):
        return kind in self.f


VOTE = ("vote", "votes")
KID = ("kid", "kids")
LOWER = lambda cs: {c: c.lower() for c in cs}


def votes_f(word):
    return {"ask": "How many votes did {a} get?",
            "more": "How many more votes did {a} get than {b}?",
            "fewer": "How many fewer votes did {a} get than {b}?",
            "both": "How many votes did {a} and {b} get in all?",
            "total": "How many votes were there in all?",
            "tie": "How many more votes does {b} need to have as many as {a}?",
            "most": "Which %s got the {w} votes?" % word,
            "which": "Which %s got {n}?" % word}


def person_f(verb, noun):
    return {"ask": "How many %s did {a} %s?" % (noun, verb),
            "more": "How many more %s did {a} %s than {b}?" % (noun, verb),
            "fewer": "How many fewer %s did {a} %s than {b}?" % (noun, verb),
            "both": "How many %s did {a} and {b} %s in all?" % (noun, verb),
            "total": "How many %s did they %s in all?" % (noun, verb),
            "tie": "How many more %s does {b} need to %s to have as many as {a}?" % (noun, verb),
            "most": "Who %s the {w} %s?" % ({"find": "found", "read": "read"}[verb], noun),
            "which": "Who %s {n}?" % {"find": "found", "read": "read"}[verb]}


CTXS = [
    Ctx("Favorite Fruit", "Fruit", ["Apple", "Banana", "Grape", "Pear"], VOTE, votes_f("fruit")),
    Ctx("Favorite Color", "Color", ["Red", "Blue", "Green", "Yellow"], VOTE, votes_f("color")),
    Ctx("Favorite Ice Cream", "Flavor", ["Vanilla", "Mint", "Berry", "Lemon"], VOTE, votes_f("flavor")),
    Ctx("Our Pets", "Pet", ["Dog", "Cat", "Fish", "Bird"], KID,
        {"ask": "How many kids have a {a}?",
         "more": "How many more kids have a {a} than a {b}?",
         "fewer": "How many fewer kids have a {a} than a {b}?",
         "both": "How many kids have a {a} or a {b}?",
         "total": "How many kids are shown in all?",
         "most": "Which pet do the {w} kids have?",
         "which": "Which pet do {n} have?"}, ph=LOWER(["Dog", "Cat", "Fish", "Bird"])),
    Ctx("How We Get to School", "Way", ["Bus", "Car", "Walk", "Bike"], KID,
        {"ask": "How many kids {a} to school?",
         "more": "How many more kids {a} than {b}?",
         "fewer": "How many fewer kids {a} than {b}?",
         "both": "How many kids {a} or {b}?",
         "total": "How many kids are shown in all?",
         "most": "Which way do the {w} kids get to school?",
         "which": "Which way do {n} get to school?"},
        ph={"Bus": "ride the bus", "Car": "come by car", "Walk": "walk", "Bike": "ride a bike"}),
    Ctx("Favorite Snack", "Snack", ["Popcorn", "Grapes", "Crackers", "Yogurt"], KID,
        {"ask": "How many kids chose {a}?",
         "more": "How many more kids chose {a} than {b}?",
         "fewer": "How many fewer kids chose {a} than {b}?",
         "both": "How many kids chose {a} or {b}?",
         "total": "How many kids voted in all?",
         "tie": "How many more kids need to choose {b} to match {a}?",
         "most": "Which snack did the {w} kids choose?",
         "which": "Which snack did {n} choose?"}, ph=LOWER(["Popcorn", "Grapes", "Crackers", "Yogurt"])),
    Ctx("What We Like at Recess", "Play", ["Swings", "Slide", "Tag", "Jump Rope"], KID,
        {"ask": "How many kids picked {a}?",
         "more": "How many more kids picked {a} than {b}?",
         "fewer": "How many fewer kids picked {a} than {b}?",
         "both": "How many kids picked {a} or {b}?",
         "total": "How many kids are shown in all?",
         "most": "Which one did the {w} kids pick?",
         "which": "Which one did {n} pick?"},
        ph={"Swings": "the swings", "Slide": "the slide", "Tag": "tag", "Jump Rope": "jump rope"}),
    Ctx("Weather for 2 Weeks", "Weather", ["Sunny", "Cloudy", "Rainy", "Windy"], ("day", "days"),
        {"ask": "How many days were {a}?",
         "more": "How many more days were {a} than {b}?",
         "fewer": "How many fewer days were {a} than {b}?",
         "both": "How many days were {a} or {b}?",
         "total": "How many days are shown in all?",
         "most": "Which weather had the {w} days?",
         "which": "Which weather had {n}?"}, ph=LOWER(["Sunny", "Cloudy", "Rainy", "Windy"]), sumto=14),
    Ctx("Toys in the Box", "Toy", ["Balls", "Cars", "Blocks", "Dolls"], ("toy", "toys"),
        {"ask": "How many {a} are in the box?",
         "more": "How many more {a} than {b} are in the box?",
         "fewer": "How many fewer {a} than {b} are in the box?",
         "both": "How many {a} and {b} are there in all?",
         "total": "How many toys are in the box?",
         "most": "Which toy is there the {w} of?",
         "which": "Which toy has {v} in the box?"}, ph=LOWER(["Balls", "Cars", "Blocks", "Dolls"])),
    Ctx("Bugs We Saw", "Bug", ["Ants", "Bees", "Ladybugs", "Beetles"], ("bug", "bugs"),
        {"ask": "How many {a} did we see?",
         "more": "How many more {a} than {b} did we see?",
         "fewer": "How many fewer {a} than {b} did we see?",
         "both": "How many {a} and {b} did we see in all?",
         "total": "How many bugs did we see in all?",
         "most": "Which bug did we see the {w} of?",
         "which": "Which bug did we see {v} of?"}, ph=LOWER(["Ants", "Bees", "Ladybugs", "Beetles"])),
    Ctx("Birds at the Feeder", "Bird", ["Robin", "Crow", "Finch", "Blue Jay"], ("bird", "birds"),
        {"ask": "How many {a} came?",
         "more": "How many more {a} than {b} came?",
         "fewer": "How many fewer {a} than {b} came?",
         "both": "How many {a} and {b} came in all?",
         "total": "How many birds came in all?",
         "most": "Which bird did we see the {w} of?",
         "which": "Which bird did we see {v} of?"},
        ph={"Robin": "robins", "Crow": "crows", "Finch": "finches", "Blue Jay": "blue jays"}),
    Ctx("Shells We Found", "Name", ["Mia", "Leo", "Ava", "Sam"], ("shell", "shells"), person_f("find", "shells"), names=True),
    Ctx("Books We Read", "Name", ["Zoe", "Ben", "Lily", "Omar"], ("book", "books"), person_f("read", "books"), names=True),
]
BYTITLE = {c.title: c for c in CTXS}


class Picker:
    """Hands out contexts in a shuffled cycle so neighbouring questions use different stories."""
    def __init__(self, rnd):
        self.rnd = rnd
        self.q = []
        self.last = None

    def next(self, ok=lambda c: True):
        for _ in range(3):
            for i, c in enumerate(self.q):
                if ok(c) and c is not self.last:
                    self.last = c
                    return self.q.pop(i)
            fresh = CTXS[:]
            self.rnd.shuffle(fresh)
            self.q += fresh
        raise ValueError("no context")


def make_data(ctx, rnd, lo=1, hi=9, ok=lambda v: True, n=3, tmax=20):
    """n categories with n different whole-number values, total at most tmax."""
    for _ in range(20000):
        cats = rnd.sample(ctx.cats, n)
        vals = [rnd.randint(lo, hi) for _ in range(n)]
        if len(set(vals)) != n or sum(vals) > tmax:
            continue
        if ctx.sumto and sum(vals) != ctx.sumto:
            continue
        if ok(vals):
            return cats, vals
    raise ValueError("no data for " + ctx.title)


# ------------------------------------------------------------ graphs
def pic_svg(title, cats, vals, sym, unit, label="picture graph"):
    """Picture graph: one row per category, each picture = 1, key line at the bottom."""
    fs, rh, gap = 15, 26, 23
    lw = max(tw(c, fs) for c in cats) * 1.1 + 24
    m = max(max(vals), 5)
    W = lw + 12 + m * gap + 6
    keytxt = "= " + fmt(1, unit)
    kw = tw("Key:", fs, True) + 32 + tw(keytxt, fs)
    W = int(math.ceil(max(W, tw(title, 16, True) + 16, kw + 16)))
    top = 28
    s = [text(W / 2, 19, title, 16, bold=True)]
    H_tab = len(cats) * rh
    s.append("<rect x='4' y='%d' width='%d' height='%d' fill='none' stroke='%s' stroke-width='1.5'/>" % (top, W - 8, H_tab, GREEN))
    s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.5'/>" % (lw, top, lw, top + H_tab, GREEN))
    for i, (c, v) in enumerate(zip(cats, vals)):
        y = top + i * rh
        if i:
            s.append("<line x1='4' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (y, W - 4, y, GRID))
        s.append(text(lw - 8, y + 18, c, fs, anchor="end"))
        for j in range(v):
            s.append(symbol(sym, lw + 12 + j * gap + 9, y + rh / 2))
    ky = top + H_tab + 22
    x = (W - kw) / 2
    s.append(text(x, ky, "Key:", fs, anchor="start", bold=True))
    x += tw("Key:", fs, True) + 16
    s.append(symbol(sym, x, ky - 5))
    s.append(text(x + 14, ky, keytxt, fs, anchor="start"))
    H = ky + 8
    return svg_wrap(W, H, "".join(s), label)


def tally_marks(x, cy, v):
    """Tally marks: groups of 5 (four lines and one line across)."""
    s = []
    b, r = divmod(v, 5)
    for g in range(b + (1 if r else 0)):
        k = 4 if g < b else r
        gx = x + g * 36
        for i in range(k):
            s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2.2' stroke-linecap='round'/>"
                     % (gx + i * 6, cy - 9, gx + i * 6, cy + 9, INK))
        if g < b:
            s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2.2' stroke-linecap='round'/>"
                     % (gx - 4, cy + 6, gx + 22, cy - 6, INK))
    return "".join(s)


def plain_marks(x, cy, v, per=4):
    """Wrong tally: groups of `per` straight marks with no line across (a common mistake)."""
    s = []
    for i in range(v):
        g, k = divmod(i, per)
        mx = x + g * 36 + k * 6
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2.2' stroke-linecap='round'/>"
                 % (mx, cy - 9, mx, cy + 9, INK))
    return "".join(s)


def tally_svg(title, axis, cats, vals, label="tally chart"):
    fs, rh = 15, 28
    lw = max(max(tw(c, fs) for c in cats), tw(axis, fs, True)) * 1.1 + 24
    groups = max(math.ceil(v / 5.0) for v in vals)
    tw_ = max(groups * 36 + 4, tw("Tally", fs, True) + 20)
    W = int(math.ceil(max(lw + tw_ + 16, tw(title, 16, True) + 16)))
    top = 28
    s = [text(W / 2, 19, title, 16, bold=True)]
    rows = len(cats) + 1
    s.append("<rect x='4' y='%d' width='%d' height='%d' fill='none' stroke='%s' stroke-width='1.5'/>" % (top, W - 8, rows * rh, GREEN))
    s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.5'/>" % (lw, top, lw, top + rows * rh, GREEN))
    s.append("<rect x='5' y='%d' width='%d' height='%d' fill='#e8f2ec'/>" % (top + 1, W - 10, rh - 1))
    s.append(text(lw - 8, top + 19, axis, fs, anchor="end", bold=True))
    s.append(text(lw + 12, top + 19, "Tally", fs, anchor="start", bold=True))
    for i, (c, v) in enumerate(zip(cats, vals)):
        y = top + (i + 1) * rh
        s.append("<line x1='4' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (y, W - 4, y, GRID))
        s.append(text(lw - 8, y + 19, c, fs, anchor="end"))
        s.append(tally_marks(lw + 14, y + rh / 2, v))
    H = top + rows * rh + 6
    return svg_wrap(W, H, "".join(s), label)


def tally4_svg(rows):
    """Four tally rows labeled A-D. rows = list of (kind, v): kind 'ok' or 'plain'."""
    rh = 34
    groups = max(int(math.ceil(v / 4.0)) for _, v in rows)
    W = 40 + groups * 36 + 10
    H = rh * 4 + 6
    s = []
    for i, (kind, v) in enumerate(rows):
        y = 3 + i * rh
        if i:
            s.append("<line x1='4' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (y, W - 4, y, GRID))
        s.append(text(10, y + rh / 2 + 6, "ABCD"[i], 18, anchor="start", bold=True))
        if kind == "ok":
            s.append(tally_marks(44, y + rh / 2, v))
        else:
            s.append(plain_marks(44, y + rh / 2, v))
    return svg_wrap(W, H, "".join(s), "four tally rows labeled A to D")


def bar_svg(title, cat_axis, val_axis, cats, vals, horizontal=False, missing=None, label="bar graph"):
    """Bar graph with a single-unit scale: a grid line and a number at every 1."""
    fs = 14
    nt = max(max(vals), 5)
    assert nt <= 12
    s = []
    if not horizontal:
        gy = 18 if nt <= 10 else 15
        ph = nt * gy
        x0 = 22 + tw(nt, fs) + 8
        slot = max(54, max(tw(c, fs) for c in cats) + 14)
        pw = slot * len(cats)
        y0 = 32
        yb = y0 + ph
        W = max(x0 + pw + 8, tw(title, 16, True) + 16)
        s.append(text(W / 2, 18, title, 16, bold=True))
        for k in range(nt + 1):
            y = yb - k * gy
            s.append("<line x1='%d' y1='%.1f' x2='%d' y2='%.1f' stroke='%s' stroke-width='1'/>" % (x0, y, x0 + pw, y, GRID))
            s.append(text(x0 - 5, y + 5, k, fs, anchor="end"))
        for i, (c, v) in enumerate(zip(cats, vals)):
            cx = x0 + slot * i + slot / 2
            bw = 30
            if i == missing:
                s.append(text(cx, yb - 6, "?", 18, bold=True, col=RED))
            else:
                h = v * gy
                s.append("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' fill='%s'/>" % (cx - bw / 2, yb - h, bw, h, BAR))
            s.append(text(cx, yb + 17, c, fs))
        s.append("<path d='M%d %d V%d H%d' fill='none' stroke='%s' stroke-width='2'/>" % (x0, y0 - 6, yb, x0 + pw, INK))
        s.append(text(x0 + pw / 2, yb + 36, cat_axis, fs, bold=True))
        mid = y0 + ph / 2
        s.append(text(13, mid, val_axis, fs, bold=True, extra=" transform='rotate(-90 13 %.1f)'" % mid))
        H = yb + 42
        assert tw(val_axis, fs, True) < ph + 26, (val_axis, ph)
    else:
        rh = 28
        gx = 24 if nt <= 10 else 21
        pw = nt * gx
        lw = max(tw(c, fs) for c in cats)
        x0 = 24 + lw + 8
        y0 = 30
        ph = rh * len(cats)
        yb = y0 + ph
        W = max(x0 + pw + tw(nt, fs) / 2 + 6, tw(title, 16, True) + 16)
        s.append(text(W / 2, 18, title, 16, bold=True))
        for k in range(nt + 1):
            x = x0 + k * gx
            s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='1'/>" % (x, y0, x, yb, GRID))
            s.append(text(x, yb + 17, k, fs))
        for i, (c, v) in enumerate(zip(cats, vals)):
            cy = y0 + rh * i + rh / 2
            if i == missing:
                s.append(text(x0 + 10, cy + 6, "?", 18, bold=True, col=RED))
            else:
                s.append("<rect x='%d' y='%.1f' width='%.1f' height='18' fill='%s'/>" % (x0, cy - 9, v * gx, BAR))
            s.append(text(x0 - 6, cy + 5, c, fs, anchor="end"))
        s.append("<path d='M%d %d V%d H%d' fill='none' stroke='%s' stroke-width='2'/>" % (x0, y0, yb, x0 + pw + 4, INK))
        s.append(text(x0 + pw / 2, yb + 36, val_axis, fs, bold=True))
        mid = y0 + ph / 2
        s.append(text(13, mid, cat_axis, fs, bold=True, extra=" transform='rotate(-90 13 %.1f)'" % mid))
        H = yb + 42
        assert tw(cat_axis, fs, True) < ph + 26, (cat_axis, ph)
    return svg_wrap(int(math.ceil(W)), int(H), "".join(s), label)


def ctx_bar(ctx, cats, vals, horizontal=False, missing=None):
    return bar_svg(ctx.title, ctx.axis, ctx.unit[1].capitalize(), cats, vals, horizontal, missing,
                   label="bar graph: " + ctx.title.lower())


def ctx_pic(ctx, cats, vals, sym):
    return pic_svg(ctx.title, cats, vals, sym, ctx.unit, label="picture graph: " + ctx.title.lower())


def ctx_tally(ctx, cats, vals):
    return tally_svg(ctx.title, ctx.axis, cats, vals, label="tally chart: " + ctx.title.lower())


def bars4_svg(title, cats, graphs):
    """2 x 2 grid of small bar graphs labeled A-D (single-unit scale, numbers every 2)."""
    fs = 14
    top = max(max(max(g) for g in graphs), 6)
    top += top % 2
    gy = 11
    slot = max(44, max(tw(c, fs) for c in cats) + 8)
    lx = 20
    CW = int(lx + 10 + slot * len(cats) + 12)
    CH = int(30 + top * gy + 26)
    W, H = 2 * CW, 2 * CH + 26
    s = [text(W / 2, 18, title, 16, bold=True),
         "<line x1='%d' y1='26' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (CW, CW, H - 2, GRID),
         "<line x1='2' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (26 + CH, W - 2, 26 + CH, GRID)]
    for k, vals in enumerate(graphs):
        ox, oy = (k % 2) * CW, 26 + (k // 2) * CH
        x0 = ox + lx + 10
        yb = oy + 30 + top * gy
        s.append(text(ox + 8, oy + 20, "ABCD"[k], 18, anchor="start", bold=True))
        for t in range(top + 1):
            y = yb - t * gy
            s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>"
                     % (x0, y, x0 + slot * len(cats), y, GRID))
            if t % 2 == 0:
                s.append(text(x0 - 4, y + 5, t, fs, anchor="end"))
        for i, (c, v) in enumerate(zip(cats, vals)):
            cx = x0 + slot * i + slot / 2
            s.append("<rect x='%.1f' y='%d' width='22' height='%d' fill='%s'/>" % (cx - 11, yb - v * gy, v * gy, BAR))
            s.append(text(cx, yb + 16, c, fs))
        s.append("<path d='M%d %d V%d H%d' fill='none' stroke='%s' stroke-width='1.6'/>" % (x0, yb - top * gy - 4, yb, x0 + slot * len(cats), INK))
    return svg_wrap(W, H, "".join(s), "four bar graphs labeled A to D")


def side_by_side(left, right, label, gap=16):
    """One picture: the data (left) next to the A-D graphs (right), so the page sees a single figure."""
    def size(svg):
        m = re.search(r"viewBox='0 0 (\d+) (\d+)'", svg)
        return int(m.group(1)), int(m.group(2))
    lw, lh = size(left)
    rw, rh = size(right)
    W, H = lw + gap + rw, max(lh, rh)

    def nest(svg, x, y):
        w, h = size(svg)
        return re.sub(r"^<svg [^>]*>", "<svg x='%d' y='%d' width='%d' height='%d' viewBox='0 0 %d %d'>" % (x, y, w, h, w, h), svg)
    body = nest(left, 0, (H - lh) // 2) + nest(right, lw + gap, (H - rh) // 2)
    return svg_wrap(W, H, body, label)


# ------------------------------------------------------------ reading text (explanations)
def count_list(v):
    return ", ".join(str(k) for k in range(1, v + 1))


def count_row(c, v, sym):
    if v <= 6:
        return "Count the %ss in the %s row: %s." % (sym, c, count_list(v))
    return "Count the %ss in the %s row. There are %d." % (sym, c, v)


def tally_read(c, v):
    b, r = divmod(v, 5)
    if b == 0:
        return "The %s row has %d mark%s, so it shows %d." % (c, v, "" if v == 1 else "s", v)
    parts = ["5"] * b + ([str(r)] if r else [])
    grp = "1 group of 5" if b == 1 else "%d groups of 5" % b
    more = (" and %d more mark%s" % (r, "" if r == 1 else "s")) if r else ""
    if len(parts) == 1:
        return "The %s row has %s. That is 5." % (c, grp)
    return "The %s row has %s%s. %s = %d." % (c, grp, more, " + ".join(parts), v)


def read_bar(c, v):
    return "The %s bar stops at the line for %d." % (c, v)


def more_fmt(d, unit, word):
    return "%d %s %s" % (d, word, unit[0] if d == 1 else unit[1])


def word_list(names):
    return ", ".join(names[:-1]) + " and " + names[-1]


# ------------------------------------------------------------ set 1: sort and count
def set_sort(rnd):
    its = []
    plan = ["count"] * 10 + ["which"] * 3 + ["most"] * 2 + ["fewest"] * 2 + ["all"] * 3
    seen_data = set()
    last_ans = []
    used_v = set()
    for i, kind in enumerate(plan):
        for _ in range(1000):
            kinds = rnd.sample(SHAPES, 3)
            lo, hi = (1, 6) if i < 5 else (2, 7)
            vals = [rnd.randint(lo, hi) for _ in range(3)]
            key = tuple(sorted(zip(kinds, vals)))
            if kind == "all" and sum(vals) != [11, 13, 15][i - 17]:
                continue
            if kind != "all":
                j_ = vals.index(max(vals)) if kind == "most" else vals.index(min(vals)) if kind == "fewest" else i % 3
                if kinds[j_] in last_ans or (kind == "which" and vals[j_] in used_v):
                    continue
            if len(set(vals)) == 3 and sum(vals) <= 15 and key not in seen_data:
                seen_data.add(key)
                break
        f = fig(mixed_svg(kinds, vals, rnd))
        pl = [SHAPE_PL[k] for k in kinds]
        t = sum(vals)
        tip = "Sort the shapes into groups. Touch each one as you count it."
        if kind == "count":
            j = i % 3
            v = vals[j]
            last_ans = [kinds[j]]
            others = [vals[k] for k in range(3) if k != j]
            its.append(mcq(f + "How many %s are there?" % pl[j], fmt(v, (kinds[j], pl[j])),
                           [fmt(x, (kinds[j], pl[j])) for x in [v + 1, v - 1] + others + [t, v + 2]],
                           "%s Count the %s: %s. There %s %s." % (tip, pl[j], count_list(v),
                                                                  "is" if v == 1 else "are", fmt(v, (kinds[j], pl[j])))))
        elif kind == "which":
            j = i % 3
            v = vals[j]
            used_v.add(v)
            order = sorted([k for k in range(3) if k != j], key=lambda k: abs(vals[k] - v))
            other = [s for s in SHAPES if s not in kinds][0]
            last_ans = [kinds[j]]
            its.append(mcq(f + "Sort the shapes. Which group has %d?" % v, cap(pl[j]),
                           [cap(pl[k]) for k in order] + [cap(SHAPE_PL[other])],
                           "%s %s." % (tip, ". ".join("%s: %d" % (cap(pl[k]), vals[k]) for k in range(3)))
                           + " The %s group has %d." % (kinds[j], v)))
        elif kind in ("most", "fewest"):
            j = vals.index(max(vals) if kind == "most" else min(vals))
            last_ans = [kinds[j]]
            other = [s for s in SHAPES if s not in kinds][0]
            order = sorted([k for k in range(3) if k != j], key=lambda k: abs(vals[k] - vals[j]))
            its.append(mcq(f + "Which shape is there the %s of?" % kind, cap(pl[j]),
                           [cap(pl[k]) for k in order] + [cap(SHAPE_PL[other])],
                           "%s %s. %d is the %s number, so there are the %s %s."
                           % (tip, ". ".join("%s: %d" % (cap(pl[k]), vals[k]) for k in range(3)),
                              vals[j], "biggest" if kind == "most" else "smallest", kind, pl[j])))
        else:
            cand = [3, t + 1, t - 1, t - min(vals), max(vals)]          # counted the groups / missed a group
            its.append(mcq(f + "How many shapes are there in all?", "%d shapes" % t, ["%d shapes" % x for x in cand],
                           "Count each group: %s. Then add: %s = %d. (There are 3 groups, but the question asks for shapes.)"
                           % (", ".join("%d %s" % (vals[k], pl[k] if vals[k] > 1 else kinds[k]) for k in range(3)),
                              plus(vals), t)))
    return {"title": "Sort and count", "items": its}


# ------------------------------------------------------------ set 2: tally charts
def set_tally(rnd, PK):
    its = []
    plan = ["read"] * 6 + ["which"] * 3 + ["read"] * 5 + ["most", "fewest", "most", "fewest"] + ["all"] * 2
    which_pos = iter([1, 3, 0])
    for i, kind in enumerate(plan):
        if kind == "which":
            v = rnd.choice([6, 7, 8, 9, 11, 12, 13, 14][i % 3::3])
            b, r = divmod(v, 5)
            rows = [("ok", v), ("ok", v - 1), ("ok", v + 1), ("plain", v - b)]       # plain: groups of 4, no line across
            names = ["right", "one mark short", "one mark extra", "no line across"]
            pos = next(which_pos)
            order = [1, 2, 3]
            rnd.shuffle(order)
            order.insert(pos, 0)
            rows = [rows[k] for k in order]
            p = PK.next()
            unit_ = rnd.choice([("car", "cars"), ("bird", "birds"), ("dog", "dogs"), ("leaf", "leaves")])
            parts = ["5"] * b + ([str(r)] if r else [])
            plain_k = order.index(3)
            q = fig(tally4_svg(rows)) + "Which tally shows %s?" % fmt(v, unit_)
            e = ("4 marks with a line across make a group of 5. %d = %s, so you need %s%s. "
                 "Row %s has no line across, so it shows only %d marks."
                 % (v, " + ".join(parts), "1 group of 5" if b == 1 else "%d groups of 5" % b,
                    (" and %d more mark%s" % (r, "" if r == 1 else "s")) if r else "", "ABCD"[plain_k], v - b))
            its.append({"q": q, "c": ["A", "B", "C", "D"], "a": pos, "fixed": True, "e": e})
            continue
        ctx = PK.next(lambda c: not (c.sumto and kind == "read" and i >= 9))
        U = ctx.unit
        if kind == "read":
            hard = i >= 9
            cats, vals = make_data(ctx, rnd, 2, 14 if hard else 9,
                                   ok=lambda v: any(x >= 6 and x % 5 for x in v) and (not hard or max(v) >= 10))
            good = [k for k in range(3) if vals[k] >= 6 and vals[k] % 5]
            if hard:
                good = [k for k in good if vals[k] >= 10] or good
            j = rnd.choice(good)
            c, v = cats[j], vals[j]
            b, r = divmod(v, 5)
            others = [vals[k] for k in range(3) if k != j]
            cand = [v - b, v + b, b + r, v + 1, v - 1] + others              # missed the line / counted it twice / group as 1
            e = "4 marks with a line across is 5. %s" % tally_read(c, v)
        elif kind in ("most", "fewest"):
            cats, vals = make_data(ctx, rnd, 2, 13, ok=lambda v: max(v) >= 6)
            j = vals.index(max(vals) if kind == "most" else min(vals))
        else:
            want = [14, 17][i - 18]
            ctx = ctx if not ctx.sumto else PK.next(lambda c: not c.sumto)
            U = ctx.unit
            cats, vals = make_data(ctx, rnd, 2, 12, ok=lambda v: max(v) >= 6 and sum(v) == want)
        f = fig(ctx_tally(ctx, cats, vals))
        if kind == "read":
            its.append(mcq(f + ctx.q("ask", c), fmt(v, U), [fmt(x, U) for x in cand], e))
        elif kind in ("most", "fewest"):
            order = sorted([k for k in range(3) if k != j], key=lambda k: abs(vals[k] - vals[j]))
            spare = [x for x in ctx.cats if x not in cats]
            its.append(mcq(f + ctx.q("most", w="most" if kind == "most" else "fewest"), cats[j],
                           [cats[k] for k in order] + spare,
                           "Count each row. %s. %s has the %s." % (". ".join("%s: %d" % (cats[k], vals[k]) for k in range(3)),
                                                                   cats[j], "most" if kind == "most" else "fewest")))
        else:
            t = sum(vals)
            cand = [3, t + 1, t - 1, t - min(vals), max(vals)]
            its.append(mcq(f + ctx.q("total"), fmt(t, U), [fmt(x, U) for x in cand],
                           "Count each row: %s. Add: %s = %s." % (", ".join("%s %d" % (cats[k], vals[k]) for k in range(3)),
                                                                   plus(vals), fmt(t, U))))
    return {"title": "Read tally charts", "items": its}


# ------------------------------------------------------------ set 3: picture graphs
def set_picture(rnd, PK):
    its = []
    plan = ["read"] * 4 + ["which", "most", "read", "fewest", "read", "which", "read", "most",
                           "read", "fewest", "which", "read", "most", "read", "fewest", "which"]
    for i, kind in enumerate(plan):
        ctx = PK.next()
        U = ctx.unit
        sym = SYMS[i % 4]
        cats, vals = make_data(ctx, rnd, 1, 9 if i >= 4 else 6, ok=lambda v: kind != "which" or max(v) >= 2)
        f = fig(ctx_pic(ctx, cats, vals, sym))
        spare = [x for x in ctx.cats if x not in cats]
        if kind == "read":
            j = rnd.randrange(3)
            c, v = cats[j], vals[j]
            nb = [vals[k] for k in (j - 1, j + 1) if 0 <= k < 3]          # read the row above or below
            others = [vals[k] for k in range(3) if k != j]
            its.append(mcq(f + ctx.q("ask", c), fmt(v, U), [fmt(x, U) for x in nb + [v + 1, v - 1] + others + [sum(vals), v + 2]],
                           "Each %s stands for 1. %s So the answer is %s." % (sym, count_row(c, v, sym), fmt(v, U))))
        elif kind == "which":
            j = rnd.choice([k for k in range(3) if vals[k] >= 2])
            v = vals[j]
            close = sorted([k for k in range(3) if k != j], key=lambda k: abs(vals[k] - v))
            its.append(mcq(f + ctx.q("which", v=v), cats[j], [cats[k] for k in close] + spare,
                           "Look for the row with %d %ss. %s" % (v, sym, count_row(cats[j], v, sym))))
        else:
            j = vals.index(max(vals) if kind == "most" else min(vals))
            order = sorted([k for k in range(3) if k != j], key=lambda k: abs(vals[k] - vals[j]))
            its.append(mcq(f + ctx.q("most", w=kind), cats[j], [cats[k] for k in order] + spare,
                           "Each %s is 1. %s. The %s row has the %s %ss." % (
                               sym, ". ".join("%s: %d" % (cats[k], vals[k]) for k in range(3)),
                               cats[j], kind, sym)))
    return {"title": "Read picture graphs", "items": its}


# ------------------------------------------------------------ set 4: bar graphs
def set_bar(rnd, PK):
    its = []
    plan = ["read"] * 4 + ["which", "most", "read", "fewest", "read", "order", "which", "most",
                           "read", "fewest", "read", "which", "most", "read", "fewest", "order"]
    for i, kind in enumerate(plan):
        ctx = PK.next()
        U = ctx.unit
        hor = i % 4 == 3
        cats, vals = make_data(ctx, rnd, 1, 10, ok=lambda v: (kind != "which" or max(v) >= 2) and (kind != "order" or
                                                                                              sorted(v)[2] - sorted(v)[0] >= 3))
        f = fig(ctx_bar(ctx, cats, vals, hor))
        spare = [x for x in ctx.cats if x not in cats]
        if kind == "read":
            j = rnd.randrange(3)
            c, v = cats[j], vals[j]
            nb = [vals[k] for k in (j - 1, j + 1) if 0 <= k < 3]
            others = [vals[k] for k in range(3) if k != j]
            its.append(mcq(f + ctx.q("ask", c), fmt(v, U), [fmt(x, U) for x in [v + 1, v - 1] + nb + others + [v + 2, sum(vals)]],
                           "Find the %s bar. Look at the end of the bar and go %s to the number. %s So the answer is %s."
                           % (c, "down" if hor else "across", read_bar(c, v), fmt(v, U))))
        elif kind == "which":
            j = rnd.choice([k for k in range(3) if vals[k] >= 2])
            v = vals[j]
            close = sorted([k for k in range(3) if k != j], key=lambda k: abs(vals[k] - v))
            its.append(mcq(f + ctx.q("which", v=v), cats[j], [cats[k] for k in close] + spare,
                           "Find %d on the numbers. Follow that line. %s" % (v, read_bar(cats[j], v))))
        elif kind in ("most", "fewest"):
            j = vals.index(max(vals) if kind == "most" else min(vals))
            word = ("longest" if kind == "most" else "shortest") if hor else ("tallest" if kind == "most" else "shortest")
            order = sorted([k for k in range(3) if k != j], key=lambda k: abs(vals[k] - vals[j]))
            its.append(mcq(f + ctx.q("most", w=kind), cats[j], [cats[k] for k in order] + spare,
                           "The %s bar is the %s bar. It shows %s." % (cats[j], word, fmt(vals[j], U))))
        else:
            o = sorted(range(3), key=lambda k: -vals[k])
            nm = lambda ks: ", ".join(cats[k] for k in ks)
            cand = [nm(o[::-1]), nm([o[1], o[0], o[2]]), nm([o[0], o[2], o[1]]), nm([o[2], o[0], o[1]])]
            its.append(mcq(f + "Put the bars in order from most to fewest.", nm(o), cand,
                           "Most: %s (%d). Next: %s (%d). Fewest: %s (%d)."
                           % (cats[o[0]], vals[o[0]], cats[o[1]], vals[o[1]], cats[o[2]], vals[o[2]])))
    return {"title": "Read bar graphs", "items": its}


# ------------------------------------------------------------ set 5: word problems
def set_word(rnd, PK):
    its = []
    plan = ["both", "more", "total", "fewer", "match_shapes", "both", "more", "fewer", "total", "tie",
            "both", "more", "fewer", "match_tally", "both", "total", "more", "fewer", "tie", "both"]
    match_pos = iter([2, 0])
    for i, kind in enumerate(plan):
        if kind.startswith("match"):
            pos = next(match_pos)
            if kind == "match_shapes":
                for _ in range(1000):
                    kinds = rnd.sample(SHAPES, 3)
                    vals = [rnd.randint(2, 7) for _ in range(3)]
                    if len(set(vals)) == 3 and sum(vals) <= 15:
                        break
                cats = [cap(SHAPE_PL[k]) for k in kinds]
                left = mixed_svg(kinds, vals, rnd, cols=3)
                head = "Sort and count the shapes. "
                title = "Our Shapes"
            else:
                ctx = PK.next(lambda c: max(len(x) for x in c.cats) <= 6)
                cats, vals = make_data(ctx, rnd, 2, 7, ok=lambda v: max(v) >= 6)
                left = ctx_tally(ctx, cats, vals)
                head = ""
                title = ctx.title
            for _ in range(500):
                a, b = rnd.sample(range(3), 2)
                hi_ = list(vals); k1 = rnd.randrange(3); hi_[k1] += 1          # one bar one too high
                sw = list(vals); sw[a], sw[b] = sw[b], sw[a]                   # two bars switched
                lo_ = list(vals); k2 = rnd.choice([k for k in range(3) if k != k1]); lo_[k2] -= 1
                g = [hi_, sw, lo_]
                if min(lo_) >= 1 and len({tuple(x) for x in g + [vals]}) == 4:
                    break
            why = ["%s %d" % (cats[k1], hi_[k1]), "%s and %s switched" % (cats[a], cats[b]), "%s %d" % (cats[k2], lo_[k2])]
            order = [0, 1, 2]
            rnd.shuffle(order)
            graphs = [g[o] for o in order]
            graphs.insert(pos, vals)
            notes = [why[o] for o in order]
            notes.insert(pos, None)
            data = ", ".join("%s %d" % (c, v) for c, v in zip(cats, vals))
            others = "; ".join("%s has %s" % ("ABCD"[k], notes[k]) for k in range(4) if k != pos)
            what = "the shapes" if kind == "match_shapes" else "the tally chart"
            its.append({"q": fig(side_by_side(left, bars4_svg(title, cats, graphs), "four bar graphs labeled A to D, with the data"))
                             + head + "Which bar graph matches %s?" % what,
                        "c": ["A", "B", "C", "D"], "a": pos, "fixed": True,
                        "e": "First count: %s. Only graph <b>%s</b> has bars at %s. Graph %s."
                             % (data, "ABCD"[pos], word_list([str(v) for v in vals]), others)})
            continue
        ctx = PK.next(lambda c: c.has(kind))
        U = ctx.unit
        style = i % 3                       # 0 bar, 1 picture, 2 tally
        if kind in ("more", "fewer", "tie"):
            cats, vals = make_data(ctx, rnd, 1, 10, ok=lambda v: sorted(v)[2] - sorted(v)[0] >= 3)
        else:
            cats, vals = make_data(ctx, rnd, 2, 10 if kind == "both" else 9)
        sym = SYMS[i % 4]
        if style == 1 and max(vals) <= 9:
            f, how = fig(ctx_pic(ctx, cats, vals, sym)), "Count the pictures."
        elif style == 2:
            f, how = fig(ctx_tally(ctx, cats, vals)), "Count the tally marks."
        else:
            f, how = fig(ctx_bar(ctx, cats, vals, i % 2 == 1)), "Read the bars."
        rd = lambda k: "%s: %d." % (cats[k], vals[k])
        if kind in ("more", "fewer", "tie"):
            for _ in range(200):
                a, b = sorted(rnd.sample(range(3), 2), key=lambda k: -vals[k])
                if vals[a] - vals[b] >= 2:
                    break
            va, vb = vals[a], vals[b]
            d = va - vb
            if kind == "more":
                q = ctx.q("more", cats[a], cats[b])
            elif kind == "fewer":
                q = ctx.q("fewer", cats[b], cats[a])
            else:
                q = ctx.q("tie", cats[a], cats[b])
            cand = [va + vb, va, vb, d + 1, d - 1]                       # added / read one bar / off by one
            word = "fewer" if kind == "fewer" else "more"
            if kind == "tie":
                e = ("%s %s %s %s needs to get from %d up to %d. %s, so %s needs %s."
                     % (how, rd(a), rd(b), cats[b], vb, va, minus(va, vb), cats[b], more_fmt(d, U, "more")))
            else:
                e = "%s %s %s Take the smaller number away from the bigger one: %s. The answer is %s." % (
                    how, rd(a), rd(b), minus(va, vb), more_fmt(d, U, word))
            its.append(mcq(f + q, fmt(d, U), [fmt(x, U) for x in cand], e))
        elif kind == "both":
            a, b = sorted(rnd.sample(range(3), 2))
            va, vb = vals[a], vals[b]
            t = va + vb
            cand = [abs(va - vb), t + 1, t - 1, max(va, vb), sum(vals)]
            its.append(mcq(f + ctx.q("both", cats[a], cats[b]), fmt(t, U), [fmt(x, U) for x in cand],
                           "%s %s %s In all means add: %d + %d = %s." % (how, rd(a), rd(b), va, vb, fmt(t, U))))
        else:
            t = sum(vals)
            cand = [3, t - min(vals), t + 1, t - 1, max(vals)]
            its.append(mcq(f + ctx.q("total"), fmt(t, U), [fmt(x, U) for x in cand],
                           "%s %s Add all three: %s = %s. (There are 3 groups, but the answer is the number of %s.)"
                           % (how, " ".join(rd(k) for k in range(3)), plus(vals), fmt(t, U), U[1])))
    return {"title": "How many in all, how many more, how many fewer", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


L_KINDS, L_SVALS = ["circle", "star", "triangle"], [5, 3, 4]
L_CATS = ["Apple", "Banana", "Grape"]
L_VALS = [7, 3, 5]


def body_html():
    fr = BYTITLE["Favorite Fruit"]
    lr = random.Random(1140)
    return (
        "<h2>The big idea</h2>"
        "<p><b>Data</b> is information we collect, like votes or things we count. "
        "First we <b>sort</b> things into groups. Then we <b>count</b> each group. "
        "Then we show the numbers in a chart or graph. In Grade 1, a graph has up to <b>3 groups</b>.</p>"
        "<h2>Sort and count</h2>"
        "<p>Put the same shapes together. Touch each one as you count it.</p>"
        "<figure class='sn-fig'>" + mixed_svg(L_KINDS, L_SVALS, lr, label="12 mixed shapes") +
        "<figcaption>Circles: 5. Stars: 3. Triangles: 4. That is 5 + 3 + 4 = 12 shapes in all.</figcaption></figure>"
        "<h2>Tally chart</h2>"
        "<p>Make one mark for each thing. The 5th mark goes <b>across</b> the first 4. "
        "So a group with a line across is <b>5</b>.</p>"
        "<figure class='sn-fig'>" + ctx_tally(fr, L_CATS, L_VALS) +
        "<figcaption>Apple has 1 group of 5 and 2 more marks: 5 + 2 = 7 votes.</figcaption></figure>"
        "<h2>Picture graph</h2>"
        "<p>Each picture stands for <b>1</b>. Count the pictures in a row.</p>"
        "<figure class='sn-fig'>" + ctx_pic(fr, L_CATS, L_VALS, "star") +
        "<figcaption>The Grape row has 5 stars, so Grape got 5 votes.</figcaption></figure>"
        "<h2>Bar graph</h2>"
        "<p>Find the top of the bar. Look straight across to the number. Each line is 1 more.</p>"
        "<figure class='sn-fig'>" + ctx_bar(fr, L_CATS, L_VALS) +
        "<figcaption>The Banana bar stops at 3, so Banana got 3 votes. Apple has the tallest bar, so it got the most votes.</figcaption></figure>"
        "<h2>Ask and answer questions</h2>"
        "<p><b>In all</b> means put together, so add. <b>How many more</b> or <b>how many fewer</b> means compare, so subtract.</p>" +
        ex("How many in all?", "How many votes were there in all?", "Apple 7, Banana 3, Grape 5. 7 + 3 + 5 = 15.", "15 votes") +
        ex("How many more?", "How many more votes did Apple get than Banana?", "Apple 7, Banana 3. 7 %s 3 = 4." % MINUS, "4 more votes") +
        ex("How many fewer?", "How many fewer votes did Grape get than Apple?", "Grape 5, Apple 7. 7 %s 5 = 2." % MINUS, "2 fewer votes") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Counting a tally group as 4, or as 6", "4 marks and 1 line across is 5"],
            ["Counting a shape twice or skipping one", "Touch or cross out each one as you count"],
            ["Reading the bar next to the one you want", "Put your finger on the name first"],
            ["Adding when it asks how many more", "How many more or fewer means subtract"],
            ["Answering a name when it asks how many", "How many wants a number, like 4 votes"],
            ["Counting the groups instead of the things", "In all means add the numbers in each group"],
        ])
    )


FAQ = [
    {"q": "What does organize data mean in 1st grade?",
     "a": "It means sorting things into up to 3 groups, counting each group, and showing the counts in a tally chart, picture graph or bar graph. Then students answer questions like how many in all and how many more."},
    {"q": "How do you teach tally marks to first graders?",
     "a": "Make one mark for each thing, and draw the 5th mark across the first 4. Then count the groups by 5s and add the extra marks, so one group and 2 marks is 7."},
    {"q": "How do you read a bar graph in Grade 1?",
     "a": "Put your finger on the name under the bar, go to the top of the bar, and look straight across to the number. In Grade 1 each line on the graph is 1."},
    {"q": "How do you find how many more on a graph?",
     "a": "Read the two numbers, then take the smaller one away from the bigger one. If Dog has 8 and Cat has 5, there are 8 − 5 = 3 more."},
]


def gen_data():
    rnd = random.Random(114)
    PK = Picker(rnd)
    sets = [set_sort(rnd), set_tally(rnd, PK), set_picture(rnd, PK), set_bar(rnd, PK), set_word(rnd, PK)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        pos = [it["a"] for it in s["items"]]
        assert all(pos.count(p) == 5 for p in range(4)), (s["title"], pos)
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            k = it["q"] + "|" + "|".join(sorted(it["c"]))
            assert k not in seen, it["q"]
            seen.add(k)
    return {
        "country": "us", "subject": "math", "grade": "grade-1", "slug": "organize-data", "sort": 14,
        "updated": UPDATED, "pdf_url": "",
        "title": "Organize Data: Sort, Count, Tally Charts and Graphs",
        "seo_title": "Grade 1 Organize Data Worksheets: Sorting, Tally Charts, Picture and Bar Graphs with 3 Categories",
        "short_title": "Organize data",
        "domain": "Measurement and Data",
        "standard_code": "1.MD.C.4",
        "standard_url": "https://www.thecorestandards.org/Math/Content/1/MD/C/4/",
        "standard_text": "Organize, represent, and interpret data with up to three categories; ask and answer questions about the total number of data points, how many in each category, and how many more or less are in one category than in another.",
        "meta_desc": "Free Grade 1 data worksheets: sort and count shapes, read tally charts, picture graphs and bar graphs with up to 3 groups, and answer how many in all, how many more and how many fewer. 100 first grade practice questions with an answer key.",
        "key_big": "Sort it, count it, show it.",
        "key_sub": "Sort things into groups and count each group. A tally group with a line across is 5. Each picture or grid line is 1. In all means add; how many more or fewer means subtract.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


def mark_large(u, pattern):
    """Tag pictures that must print larger (graphs, tally charts, A-D choices) so their labels stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


if __name__ == "__main__":
    u = gen_data()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as f:
        mark_large(u, "(picture graph|bar graph|tally chart|four bar graphs|four tally rows)")
        json.dump(u, f, ensure_ascii=False, indent=1)
    print("wrote", path)
