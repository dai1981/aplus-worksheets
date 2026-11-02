# -*- coding: utf-8 -*-
"""
US Grade 2 Math: Picture Graphs, Bar Graphs and Line Plots (2.MD.D.9-10)
  python tools/gen_us_math_g2_graphs.py
Single-unit scale only (each picture = 1, each grid space = 1), up to four categories,
whole-number line plots. HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, re, math, os, random

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "us", "math", "grade-2")
UPDATED = "2026-11-02"
GREEN = "#006633"
BAR = "#2e8b57"
RED = "#c0392b"
INK = "#2b2b2b"
GRID = "#c9d3cc"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Maya", "Ava", "Mia", "Zoe", "Lily", "Emma", "Nora", "Ruby", "Sofia", "Grace"]
BOYS = ["Leo", "Noah", "Eli", "Sam", "Ben", "Omar", "Kai", "Jack", "Luis", "Owen"]


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e):
    """4 choices: correct + the first 3 unique distractors (no zero or negative numbers).
    Positions are set later by balance()."""
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
    Items marked 'fixed' (A-D graph pictures) already have their position; the rest fill the gaps."""
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


def ones(cnt, word):
    return "%d %s" % (cnt, word if cnt == 1 else word + "s")


def cap(s):
    return s[0].upper() + s[1:]


def plus(vals):
    return " + ".join(str(v) for v in vals)


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


# ------------------------------------------------------------ symbols (no clip paths: ids would clash on one page)
def star_pts(cx, cy, R=9.5, r=4.0):
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rad = R if i % 2 == 0 else r
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    return pts


def symbol(kind, cx, cy, col=GREEN):
    if kind == "circle":
        return "<circle cx='%.1f' cy='%.1f' r='8.5' fill='%s'/>" % (cx, cy, col)
    if kind == "square":
        return "<rect x='%.1f' y='%.1f' width='15' height='15' rx='2' fill='%s'/>" % (cx - 7.5, cy - 7.5, col)
    if kind == "heart":
        return ("<path d='M%.1f %.1f C%.1f %.1f %.1f %.1f %.1f %.1f C%.1f %.1f %.1f %.1f %.1f %.1f Z' fill='%s'/>"
                % (cx, cy + 8, cx - 12, cy - 1, cx - 6, cy - 11, cx, cy - 4,
                   cx + 6, cy - 11, cx + 12, cy - 1, cx, cy + 8, col))
    return "<polygon points='%s' fill='%s'/>" % (" ".join("%.1f,%.1f" % p for p in star_pts(cx, cy)), col)


SYMS = ["circle", "star", "square", "heart"]


# ------------------------------------------------------------ contexts
class Ctx:
    def __init__(self, title, axis, cats, unit, f, ph=None, sumto=None, short=True):
        self.title, self.axis, self.cats, self.unit = title, axis, cats, unit
        self.f, self.ph, self.sumto, self.short = f, ph or {}, sumto, short

    def p(self, c):
        return self.ph.get(c, c)

    def q(self, kind, a=None, b=None):
        return self.f[kind].format(a=self.p(a) if a else "", b=self.p(b) if b else "")

    def has(self, kind):
        return kind in self.f


VOTE = ("vote", "votes")
STU = ("student", "students")
LOWER = lambda cs: {c: c.lower() for c in cs}


def votes_f(noun="votes"):
    return {"ask": "How many votes did {a} get?",
            "more": "How many more votes did {a} get than {b}?",
            "fewer": "How many fewer votes did {a} get than {b}?",
            "both": "How many votes did {a} and {b} get in all?",
            "total": "How many votes were there in all?",
            "nota": "How many votes were not for {a}?",
            "tie": "How many more votes does {b} need to have as many as {a}?"}


def chose_f():
    return {"ask": "How many students chose {a}?",
            "more": "How many more students chose {a} than {b}?",
            "fewer": "How many fewer students chose {a} than {b}?",
            "both": "How many students chose {a} or {b}?",
            "total": "How many students voted in all?",
            "nota": "How many students did not choose {a}?",
            "tie": "How many more students need to choose {b} to match {a}?"}


def person_f(verb, past, noun):
    """Categories are children's names."""
    return {"ask": "How many %s did {a} %s?" % (noun, verb),
            "more": "How many more %s did {a} %s than {b}?" % (noun, verb),
            "fewer": "How many fewer %s did {a} %s than {b}?" % (noun, verb),
            "both": "How many %s did {a} and {b} %s in all?" % (noun, verb),
            "total": "How many %s did they %s in all?" % (noun, verb),
            "tie": "How many more %s does {b} need to %s to have as many as {a}?" % (noun, verb)}


CTXS = [
    Ctx("Favorite Fruit", "Fruit", ["Apple", "Banana", "Grape", "Pear", "Peach"], VOTE, votes_f()),
    Ctx("Pets We Have", "Pet", ["Dog", "Cat", "Fish", "Bird"], STU,
        {"ask": "How many students have a {a}?",
         "more": "How many more students have a {a} than a {b}?",
         "fewer": "How many fewer students have a {a} than a {b}?",
         "both": "How many students have a {a} or a {b}?",
         "total": "How many students are shown in all?",
         "nota": "How many students do not have a {a}?"}, ph=LOWER(["Dog", "Cat", "Fish", "Bird"])),
    Ctx("Books Read This Week", "Student", ["Maya", "Leo", "Ava", "Noah", "Zoe"], ("book", "books"),
        person_f("read", "read", "books")),
    Ctx("Weather for Two Weeks", "Weather", ["Sunny", "Cloudy", "Rainy", "Windy"], ("day", "days"),
        {"ask": "How many days were {a}?",
         "more": "How many more days were {a} than {b}?",
         "fewer": "How many fewer days were {a} than {b}?",
         "both": "How many days were {a} or {b}?",
         "total": "How many days are shown in all?",
         "nota": "How many days were not {a}?"}, ph=LOWER(["Sunny", "Cloudy", "Rainy", "Windy"]), sumto=14),
    Ctx("How We Get to School", "Way", ["Bus", "Car", "Walk", "Bike"], STU,
        {"ask": "How many students {a} to school?",
         "more": "How many more students {a} to school than {b}?",
         "fewer": "How many fewer students {a} to school than {b}?",
         "both": "How many students {a} or {b} to school?",
         "total": "How many students are shown in all?",
         "nota": "How many students do not {a} to school?"},
        ph={"Bus": "ride the bus", "Car": "come by car", "Walk": "walk", "Bike": "ride a bike"}),
    Ctx("Favorite Color", "Color", ["Red", "Blue", "Green", "Yellow", "Purple"], VOTE, votes_f()),
    Ctx("Birds at the Feeder", "Bird", ["Robin", "Finch", "Crow", "Blue Jay"], ("bird", "birds"),
        {"ask": "How many {a} came to the feeder?",
         "more": "How many more {a} than {b} came?",
         "fewer": "How many fewer {a} than {b} came?",
         "both": "How many {a} and {b} came in all?",
         "total": "How many birds came in all?",
         "nota": "How many birds were not {a}?"},
        ph={"Robin": "robins", "Finch": "finches", "Crow": "crows", "Blue Jay": "blue jays"}),
    Ctx("Favorite Season", "Season", ["Spring", "Summer", "Fall", "Winter"], VOTE, votes_f()),
    Ctx("Toys in the Bin", "Toy", ["Balls", "Cars", "Blocks", "Dolls"], ("toy", "toys"),
        {"ask": "How many {a} are in the bin?",
         "more": "How many more {a} than {b} are in the bin?",
         "fewer": "How many fewer {a} than {b} are in the bin?",
         "both": "How many {a} and {b} are there in all?",
         "total": "How many toys are in the bin?",
         "nota": "How many toys are not {a}?"}, ph=LOWER(["Balls", "Cars", "Blocks", "Dolls"])),
    Ctx("Bugs We Saw", "Bug", ["Ant", "Bee", "Ladybug", "Beetle"], ("bug", "bugs"),
        {"ask": "How many {a} did the class see?",
         "more": "How many more {a} than {b} did the class see?",
         "fewer": "How many fewer {a} than {b} did the class see?",
         "both": "How many {a} and {b} did the class see in all?",
         "total": "How many bugs did the class see in all?",
         "nota": "How many bugs were not {a}?"},
        ph={"Ant": "ants", "Bee": "bees", "Ladybug": "ladybugs", "Beetle": "beetles"}),
    Ctx("Stickers We Have", "Student", ["Ruby", "Omar", "Lily", "Kai", "Emma"], ("sticker", "stickers"),
        {"ask": "How many stickers does {a} have?",
         "more": "How many more stickers does {a} have than {b}?",
         "fewer": "How many fewer stickers does {a} have than {b}?",
         "both": "How many stickers do {a} and {b} have in all?",
         "total": "How many stickers do they have in all?",
         "tie": "How many more stickers does {b} need to have as many as {a}?"}),
    Ctx("Shells We Found", "Student", ["Sam", "Nora", "Eli", "Mia", "Owen"], ("shell", "shells"),
        person_f("find", "found", "shells")),
    Ctx("Favorite Snack", "Snack", ["Popcorn", "Grapes", "Pretzels", "Yogurt"], STU, chose_f(),
        ph=LOWER(["Popcorn", "Grapes", "Pretzels", "Yogurt"])),
    Ctx("Ice Cream Scoops Sold", "Flavor", ["Vanilla", "Mint", "Berry", "Mango"], ("scoop", "scoops"),
        {"ask": "How many {a} scoops were sold?",
         "more": "How many more {a} scoops than {b} scoops were sold?",
         "fewer": "How many fewer {a} scoops than {b} scoops were sold?",
         "both": "How many {a} and {b} scoops were sold in all?",
         "total": "How many scoops were sold in all?",
         "nota": "How many scoops were not {a}?"}, ph=LOWER(["Vanilla", "Mint", "Berry", "Mango"])),
    Ctx("Favorite Sport", "Sport", ["Soccer", "Tennis", "Swim", "Baseball"], STU, chose_f(),
        ph={"Soccer": "soccer", "Tennis": "tennis", "Swim": "swimming", "Baseball": "baseball"}),
    Ctx("Lunch Choices", "Lunch", ["Pizza", "Tacos", "Pasta", "Salad"], STU, chose_f(),
        ph=LOWER(["Pizza", "Tacos", "Pasta", "Salad"])),
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


def make_data(ctx, n, rnd, lo=1, hi=9, ok=lambda v: True):
    """n categories with n different whole-number values."""
    for _ in range(5000):
        cats = rnd.sample(ctx.cats, n)
        vals = [rnd.randint(lo, hi) for _ in range(n)]
        if len(set(vals)) != n:
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


def tally_svg(title, axis, cats, vals, label="tally chart"):
    fs, rh = 15, 28
    lw = max(max(tw(c, fs) for c in cats), tw(axis, fs, True)) * 1.1 + 24
    groups = max(math.ceil(v / 5) for v in vals)
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


def bar_top(vals, lab):
    t = max(max(vals), 5)
    if lab == 2:
        t = int(math.ceil(t / 2.0) * 2)
    return t


def bar_svg(title, cat_axis, val_axis, cats, vals, horizontal=False, lab=1, missing=None, label="bar graph"):
    """Bar graph with a single-unit scale: a grid line at every 1, numbers every `lab`.
    `missing` = index of a category drawn with no bar (a red ? shows where it goes)."""
    fs = 14
    nt = bar_top(vals, lab)
    assert nt <= 12
    s = []
    if not horizontal:
        gy = 18 if nt <= 10 else 15
        ph = nt * gy
        x0 = 22 + tw(nt, fs) + 8
        slot = max(50, max(tw(c, fs) for c in cats) + 12)
        pw = slot * len(cats)
        y0 = 32
        yb = y0 + ph
        W = max(x0 + pw + 8, tw(title, 16, True) + 16)
        s.append(text(W / 2, 18, title, 16, bold=True))
        for k in range(nt + 1):
            y = yb - k * gy
            s.append("<line x1='%d' y1='%.1f' x2='%d' y2='%.1f' stroke='%s' stroke-width='1'/>" % (x0, y, x0 + pw, y, GRID))
            if k % lab == 0:
                s.append(text(x0 - 5, y + 5, k, fs, anchor="end"))
        for i, (c, v) in enumerate(zip(cats, vals)):
            cx = x0 + slot * i + slot / 2
            bw = 28
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
        rh = 26
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
            if k % lab == 0:
                s.append(text(x, yb + 17, k, fs))
        for i, (c, v) in enumerate(zip(cats, vals)):
            cy = y0 + rh * i + rh / 2
            if i == missing:
                s.append(text(x0 + 10, cy + 6, "?", 18, bold=True, col=RED))
            else:
                s.append("<rect x='%d' y='%.1f' width='%.1f' height='16' fill='%s'/>" % (x0, cy - 8, v * gx, BAR))
            s.append(text(x0 - 6, cy + 5, c, fs, anchor="end"))
        s.append("<path d='M%d %d V%d H%d' fill='none' stroke='%s' stroke-width='2'/>" % (x0, y0, yb, x0 + pw + 4, INK))
        s.append(text(x0 + pw / 2, yb + 36, val_axis, fs, bold=True))
        mid = y0 + ph / 2
        s.append(text(13, mid, cat_axis, fs, bold=True, extra=" transform='rotate(-90 13 %.1f)'" % mid))
        H = yb + 42
        assert tw(cat_axis, fs, True) < ph + 26, (cat_axis, ph)
    return svg_wrap(int(math.ceil(W)), int(H), "".join(s), label)


def ctx_bar(ctx, cats, vals, horizontal=False, lab=1, missing=None):
    return bar_svg(ctx.title, ctx.axis, ctx.unit[1].capitalize(), cats, vals, horizontal, lab, missing,
                   label="bar graph: " + ctx.title.lower())


def ctx_pic(ctx, cats, vals, sym):
    return pic_svg(ctx.title, cats, vals, sym, ctx.unit, label="picture graph: " + ctx.title.lower())


def ctx_tally(ctx, cats, vals):
    return tally_svg(ctx.title, ctx.axis, cats, vals, label="tally chart: " + ctx.title.lower())


def bars4_svg(title, cats, graphs):
    """2 x 2 grid of small bar graphs labeled A-D (single-unit scale)."""
    fs = 14
    top = max(max(max(g) for g in graphs), 5)
    gy = 12
    slot = max(40, max(tw(c, fs) for c in cats) + 8)
    lx = 18                                     # room for the axis numbers
    CW = int(lx + 10 + slot * len(cats) + 14)
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
            s.append("<rect x='%.1f' y='%d' width='20' height='%d' fill='%s'/>" % (cx - 10, yb - v * gy, v * gy, BAR))
            s.append(text(cx, yb + 16, c, fs))
        s.append("<path d='M%d %d V%d H%d' fill='none' stroke='%s' stroke-width='1.6'/>" % (x0, yb - top * gy - 4, yb, x0 + slot * len(cats), INK))
    return svg_wrap(W, H, "".join(s), "four bar graphs labeled A to D")


# ------------------------------------------------------------ line plots
IN = ("inch", "inches")
CM = ("centimeter", "centimeters")


def plot_svg(start, counts, unit, label="line plot of lengths", gap=44):
    n = len(counts)
    mx = max(max(counts), 1)
    pad = 26
    W = int(2 * pad + gap * (n - 1))
    Y = 30 + 16 * (mx - 1)
    H = Y + 52
    X = lambda i: pad + gap * i
    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (pad - 16, Y, W - pad + 16, Y, INK)]
    for i in range(n):
        x = X(i)
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.8'/>" % (x, Y - 6, x, Y + 6, INK))
        s.append(text(x, Y + 25, start + i, 16))
        for k in range(counts[i]):
            cy = Y - 18 - 16 * k
            s.append("<path d='M%d %d L%d %d M%d %d L%d %d' stroke='%s' stroke-width='2.4' stroke-linecap='round'/>"
                     % (x - 6, cy - 6, x + 6, cy + 6, x - 6, cy + 6, x + 6, cy - 6, GREEN))
    s.append(text(W / 2, Y + 47, "Length (%s)" % unit[1], 14))
    assert tw("Length (%s)" % unit[1], 14) < W
    return svg_wrap(W, H, "".join(s), label)


# what was measured: (plural, singular, unit, smallest, largest, who)
LCTX = [("pencils", "pencil", IN, 3, 9), ("crayons", "crayon", CM, 5, 11), ("leaves", "leaf", IN, 2, 8),
        ("shells", "shell", CM, 2, 8), ("ribbons", "ribbon", IN, 4, 12), ("worms", "worm", CM, 4, 10),
        ("sticks", "stick", IN, 6, 12), ("feathers", "feather", IN, 2, 8), ("erasers", "eraser", CM, 3, 8),
        ("carrots", "carrot", IN, 3, 8), ("toy cars", "toy car", CM, 6, 12), ("paper strips", "paper strip", CM, 7, 14)]


class LPicker:
    def __init__(self, rnd):
        self.pool = LCTX[:]
        rnd.shuffle(self.pool)
        self.i = 0

    def next(self):
        c = self.pool[self.i % len(self.pool)]
        self.i += 1
        return c


def make_plot(rnd, ctx, ok=lambda c: True, n=None, tot=(8, 16)):
    """Line plot data inside the context's range; `ok(counts)` must be true."""
    pl, sg, unit, lo, hi = ctx
    if n is None:
        n = min(7, hi - lo + 1)
    for _ in range(4000):
        s = rnd.randint(lo, hi - n + 1)
        peak = rnd.randrange(n)
        counts = [max(0, min(5, rnd.choice([4, 5, 3, 4]) - abs(i - peak) + rnd.choice([-1, 0, 0, 1]))) for i in range(n)]
        t = sum(counts)
        ends_ok = not (counts[0] == 0 and counts[1] == 0) and not (counts[-1] == 0 and counts[-2] == 0)
        if tot[0] <= t <= tot[1] and ends_ok and ok(counts):
            return s, counts
    raise RuntimeError("no plot for %s" % (ctx,))


def unique_max(counts):
    return counts.count(max(counts)) == 1


def data_list(rnd, s, cn):
    d = []
    for i, c in enumerate(cn):
        d += [s + i] * c
    rnd.shuffle(d)
    return d


def ctx_plot(ctx, s, cn):
    return plot_svg(s, cn, ctx[2], label="line plot of %s lengths" % ctx[1])


# ------------------------------------------------------------ reading text (explanations)
def read_bar(c, v, lab, hor=False):
    if lab == 2 and v % 2:
        return "The %s bar ends at the line between %d and %d. That line is %d." % (c, v - 1, v + 1, v)
    return "The %s bar ends at the line for %d." % (c, v)


def count_row(c, v, sym):
    if v <= 6:
        return "Count the %ss in the %s row: %s." % (sym, c, ", ".join(str(k) for k in range(1, v + 1)))
    return "Count the %ss in the %s row. There are %d." % (sym, c, v)


def tally_read(c, v):
    b, r = divmod(v, 5)
    parts = ["5"] * b + ([str(r)] if r else [])
    grp = "1 group of 5" if b == 1 else "%d groups of 5" % b
    more = (" and %d more mark%s" % (r, "" if r == 1 else "s")) if r else ""
    return "The %s row has %s%s. %s = %d." % (c, grp, more, " + ".join(parts), v)


def xs(c):
    return "1 X" if c == 1 else "%d X's" % c


def more_fmt(d, unit, word):
    return "%d %s %s" % (d, word, unit[0] if d == 1 else unit[1])


# ------------------------------------------------------------ set 1: picture graphs and tally charts
def set_picture(rnd, PK):
    its = []
    plan = ["read"] * 10 + ["most", "fewest", "which", "most", "fewest", "which"] + ["tally"] * 3 + ["tally_most"]
    for i, kind in enumerate(plan):
        ctx = PK.next()
        U = ctx.unit
        sym = SYMS[i % 4]
        n = 3 if i in (1, 6, 9) else 4
        if kind.startswith("tally"):
            cats, vals = make_data(ctx, n, rnd, 3, 13, ok=lambda v: sum(1 for x in v if x >= 5) >= 3)
            f = fig(ctx_tally(ctx, cats, vals))
        else:
            cats, vals = make_data(ctx, n, rnd, 1, 9)
            f = fig(ctx_pic(ctx, cats, vals, sym))
        if kind == "read":
            j = rnd.randrange(n)
            c, v = cats[j], vals[j]
            nb = [vals[k] for k in (j - 1, j + 1) if 0 <= k < n]           # read the row above or below
            others = [vals[k] for k in range(n) if k != j]
            its.append(mcq(f + ctx.q("ask", c), fmt(v, U), [fmt(x, U) for x in nb + [v + 1, v - 1] + others + [v + 2, v - 2]],
                           "Each %s stands for 1. %s So the answer is %s." % (sym, count_row(c, v, sym), fmt(v, U))))
        elif kind in ("most", "fewest", "tally_most"):
            j = vals.index(min(vals) if kind == "fewest" else max(vals))
            word = "the fewest" if kind == "fewest" else "the most"
            order = sorted([k for k in range(n) if k != j], key=lambda k: abs(vals[k] - vals[j]))
            q = "Which row shows %s %s?" % (word, U[1])
            if kind == "tally_most":
                e = ("Find the row with the most marks. %s The other rows are %s."
                     % (tally_read(cats[j], vals[j]), ", ".join("%s %d" % (cats[k], vals[k]) for k in range(n) if k != j)))
            else:
                e = ("Each %s is 1, so the row with %s %ss wins. %s has %d. The others have %s."
                     % (sym, word, sym, cats[j], vals[j], ", ".join(str(vals[k]) for k in range(n) if k != j)))
            its.append(mcq(f + q, cats[j], [cats[k] for k in order], e))
        elif kind == "which":
            j = rnd.randrange(n)
            v = vals[j]
            close = sorted([k for k in range(n) if k != j], key=lambda k: abs(vals[k] - v))
            its.append(mcq(f + "Which row shows %s?" % fmt(v, U), cats[j], [cats[k] for k in close],
                           "Look for a row with %s. %s" % (ones(v, sym), count_row(cats[j], v, sym))))
        else:                                                           # read a tally chart
            j = rnd.choice([k for k in range(n) if vals[k] >= 6 and vals[k] % 5])
            c, v = cats[j], vals[j]
            b, r = divmod(v, 5)
            nb = [vals[k] for k in (j - 1, j + 1) if 0 <= k < n]
            cand = [v - b, b + r] + nb + [v + 1, v - 1]                  # forgot the line across / each group as 1
            its.append(mcq(f + ctx.q("ask", c), fmt(v, U), [fmt(x, U) for x in cand],
                           "A group of 4 marks with a line across is 5. %s" % tally_read(c, v)))
    return {"title": "Read picture graphs and tally charts", "items": its}


# ------------------------------------------------------------ set 2: bar graphs
def set_bar(rnd, PK):
    its = []
    plan = ["read"] * 12 + ["which"] * 3 + ["most", "fewest", "most", "fewest", "same"]
    labs = [1, 1, 1, 2, 1, 2, 1, 2, 2, 1, 2, 2, 1, 2, 1, 1, 2, 1, 2, 1]
    for i, kind in enumerate(plan):
        ctx = PK.next()
        U = ctx.unit
        lab = labs[i]
        hor = i % 2 == 1
        n = 4
        hi = 12 if lab == 2 else 9
        if kind == "same":
            for _ in range(5000):
                cats = rnd.sample(ctx.cats, 4)
                vals = [rnd.randint(2, 9) for _ in range(4)]
                if len(set(vals)) == 3 and (not ctx.sumto or sum(vals) == ctx.sumto):
                    break
        else:
            cats, vals = make_data(ctx, n, rnd, 1, hi,
                                   ok=lambda v: lab == 1 or sum(1 for x in v if x % 2) >= 2)
        f = fig(ctx_bar(ctx, cats, vals, hor, lab))
        scl = "Each grid line is 1 more." if lab == 1 else "The numbers count by 2s, so the line between two numbers is the number in the middle."
        if kind == "read":
            if lab == 2:
                j = rnd.choice([k for k in range(n) if vals[k] % 2])
            else:
                j = rnd.randrange(n)
            c, v = cats[j], vals[j]
            nb = [vals[k] for k in (j - 1, j + 1) if 0 <= k < n]
            others = [vals[k] for k in range(n) if k != j]
            its.append(mcq(f + ctx.q("ask", c), fmt(v, U), [fmt(x, U) for x in [v + 1, v - 1] + nb + others + [v + 2]],
                           "%s %s So the answer is %s." % (scl, read_bar(c, v, lab), fmt(v, U))))
        elif kind == "which":
            j = rnd.randrange(n)
            v = vals[j]
            close = sorted([k for k in range(n) if k != j], key=lambda k: abs(vals[k] - v))
            its.append(mcq(f + "Which bar shows %s?" % fmt(v, U), cats[j], [cats[k] for k in close],
                           "Find %d on the numbers. Follow that line across. %s" % (v, read_bar(cats[j], v, lab))))
        elif kind in ("most", "fewest"):
            j = vals.index(max(vals) if kind == "most" else min(vals))
            if hor:
                word = "longest" if kind == "most" else "shortest"
            else:
                word = "tallest" if kind == "most" else "shortest"
            order = sorted([k for k in range(n) if k != j], key=lambda k: abs(vals[k] - vals[j]))
            q = "Which bar shows %s %s?" % ("the most" if kind == "most" else "the fewest", U[1])
            its.append(mcq(f + q, cats[j], [cats[k] for k in order],
                           "The %s bar is the %s bar. %s It shows %s." % (cats[j], word, read_bar(cats[j], vals[j], lab), fmt(vals[j], U))))
        else:
            v = [x for x in vals if vals.count(x) == 2][0]
            a, b = [k for k in range(4) if vals[k] == v]
            pairs = [(x, y) for x in range(4) for y in range(x + 1, 4) if (x, y) != (a, b)]
            pairs.sort(key=lambda p: abs(vals[p[0]] - vals[p[1]]))
            nm = lambda p: "%s and %s" % (cats[p[0]], cats[p[1]])
            its.append(mcq(f + "Which two bars show the same number?", nm((a, b)), [nm(p) for p in pairs],
                           "The %s bar and the %s bar both end at the line for %d. They are the same %s."
                           % (cats[a], cats[b], v, "length" if hor else "height")))
    return {"title": "Read a bar graph", "items": its}


# ------------------------------------------------------------ set 3: put together, take apart, compare
def set_compare(rnd, PK):
    its = []
    plan = ["both", "more", "fewer", "both", "more", "fewer", "both", "more", "fewer", "both",
            "more", "fewer", "tie", "total", "more", "fewer", "nota", "tie", "total", "nota"]
    pics = {3, 7, 11, 15}
    for i, kind in enumerate(plan):
        ctx = PK.next(lambda c: c.has(kind))
        U = ctx.unit
        pic = i in pics
        hor = i % 3 == 1
        hi = 9 if pic else 10
        cats, vals = make_data(ctx, 4, rnd, 1, hi, ok=lambda v: sorted(v)[-1] - sorted(v)[1] >= 2 and sum(v) <= 30)
        sym = SYMS[i % 4]
        f = fig(ctx_pic(ctx, cats, vals, sym) if pic else ctx_bar(ctx, cats, vals, hor))
        rd = (lambda k: "%s: %d." % (cats[k], vals[k]))
        how = "Count the pictures in each row." if pic else "Read each bar."
        if kind in ("more", "fewer", "tie"):
            for _ in range(200):
                a, b = sorted(rnd.sample(range(4), 2), key=lambda k: -vals[k])
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
            cand = [va + vb, va, d + 1, d - 1, vb]                       # added / read one bar / off by one
            word = "fewer" if kind == "fewer" else "more"
            e = "%s %s %s Compare: %d − %d = %d. The answer is %s." % (how, rd(a), rd(b), va, vb, d, more_fmt(d, U, word))
            if kind == "tie":
                e = ("%s %s %s %s needs to get from %d up to %d. %d − %d = %d, so %s needs %s."
                     % (how, rd(a), rd(b), cats[b], vb, va, va, vb, d, cats[b], more_fmt(d, U, "more")))
            its.append(mcq(f + q, fmt(d, U), [fmt(x, U) for x in cand], e))
        elif kind == "both":
            a, b = rnd.sample(range(4), 2)
            va, vb = vals[a], vals[b]
            t = va + vb
            cand = [abs(va - vb), t + 1, t - 1, max(va, vb), sum(vals)]  # subtracted / off by one / one bar
            its.append(mcq(f + ctx.q("both", cats[a], cats[b]), fmt(t, U), [fmt(x, U) for x in cand],
                           "%s %s %s Put them together: %d + %d = %s." % (how, rd(a), rd(b), va, vb, fmt(t, U))))
        elif kind == "total":
            t = sum(vals)
            cand = [4, t - min(vals), t + 1, t - 1, max(vals)]          # counted the bars / missed one bar
            its.append(mcq(f + ctx.q("total"), fmt(t, U), [fmt(x, U) for x in cand],
                           "%s %s Add all four: %s = %s. (There are 4 bars, but the answer is the number of %s.)"
                           % (how, " ".join(rd(k) for k in range(4)), plus(vals), fmt(t, U), U[1])))
        else:                                                            # take apart: not X
            j = rnd.randrange(4)
            t = sum(vals)
            ans = t - vals[j]
            cand = [vals[j], t, ans + 1, ans - 1]                         # read X / the total
            rest = [vals[k] for k in range(4) if k != j]
            its.append(mcq(f + ctx.q("nota", cats[j]), fmt(ans, U), [fmt(x, U) for x in cand],
                           "Leave out %s. Add the other three: %s = %s." % (cats[j], plus(rest), fmt(ans, U))))
    return {"title": "In all, how many more, how many fewer", "items": its}


# ------------------------------------------------------------ set 4: line plots
def set_lineplot(rnd, LP):
    its = []
    plan = ["count"] * 5 + ["most"] * 3 + ["all"] * 3 + ["longest", "shortest"] + ["longer", "shorter", "longer"] + \
           ["more", "more"] + ["diff", "diff"]
    for i, kind in enumerate(plan):
        ctx = LP.next()
        pl, sg, U = ctx[0], ctx[1], ctx[2]
        if kind == "most":
            s, cn = make_plot(rnd, ctx, unique_max)
        elif kind in ("longest", "shortest"):
            s, cn = make_plot(rnd, ctx, lambda c: (c[-1] == 0) if kind == "longest" else (c[0] == 0))
        elif kind == "more":
            s, cn = make_plot(rnd, ctx, lambda c: any(c[a] - c[b] >= 2 and c[b] > 0 and abs(a - b) != c[a] - c[b]
                                                      for a in range(len(c)) for b in range(len(c))))
        else:
            s, cn = make_plot(rnd, ctx)
        n = len(cn)
        V = [s + k for k in range(n)]
        f = fig(ctx_plot(ctx, s, cn))
        tot = sum(cn)
        if kind == "count":
            j = rnd.choice([k for k in range(n) if cn[k] > 0 and 0 < k < n - 1] or [k for k in range(n) if cn[k]])
            L, c = V[j], cn[j]
            nb = [cn[k] for k in (j - 1, j + 1) if 0 <= k < n]
            q = "How many %s are %s long?" % (pl, fmt(L, U))
            cand = nb + [L, tot, c + 1, c - 1]                           # the column next to it / the length itself
            its.append(mcq(f + q, str(c), cand,
                           "Find %d on the number line. Count the X's above it: %d. Each X is one %s, so %s %s long."
                           % (L, c, sg, "1 %s is" % sg if c == 1 else "%d %s are" % (c, pl), fmt(L, U))))
        elif kind == "most":
            j = cn.index(max(cn))
            second = sorted([k for k in range(n) if k != j], key=lambda k: -cn[k])
            cand = [fmt(max(cn), U), fmt(V[second[0]], U), fmt(V[-1], U), fmt(V[j] + 1, U), fmt(V[j] - 1, U)]
            its.append(mcq(f + "What length are the most %s?" % pl, fmt(V[j], U), cand,
                           "Find the tallest stack of X's. It is above %d and has %d X's. So the most %s are %s long. "
                           "(%d is how many %s, not the length.)" % (V[j], cn[j], pl, fmt(V[j], U), cn[j], pl)))
        elif kind == "all":
            cand = [n, tot + 1, tot - 1, max(cn), tot - min(c for c in cn if c)]   # counted the marks / missed a stack
            its.append(mcq(f + "How many %s were measured in all?" % pl, str(tot), cand,
                           "Each X is one %s. Count all the X's: %s = %d. (Do not count the numbers on the line.)"
                           % (sg, plus([c for c in cn if c]), tot)))
        elif kind in ("longest", "shortest"):
            has = [k for k in range(n) if cn[k]]
            j = has[-1] if kind == "longest" else has[0]
            end = V[-1] if kind == "longest" else V[0]
            big = V[cn.index(max(cn))]
            other = V[has[0]] if kind == "longest" else V[has[-1]]
            cand = [fmt(end, U), fmt(big, U), fmt(other, U), fmt(V[j] - 1 if kind == "longest" else V[j] + 1, U)]
            word = "right" if kind == "longest" else "left"
            its.append(mcq(f + "How long is the %s %s?" % (kind, sg), fmt(V[j], U), cand,
                           "Find the X that is farthest to the %s. It is above %d, so the %s %s is %s. "
                           "There is no X above %d." % (word, V[j], kind, sg, fmt(V[j], U), end)))
        elif kind in ("longer", "shorter"):
            k0 = rnd.randrange(2, n - 2) if n > 4 else 1
            L = V[k0]
            if kind == "longer":
                ans = sum(cn[k0 + 1:])
                incl = ans + cn[k0]
                other = sum(cn[:k0])
                txt = "longer than"
                e = "Longer than %d means %s. Count the X's to the right of %d: %s = %d." % (
                    L, "more than %d, so do not count the X's above %d" % (L, L), L, plus([c for c in cn[k0 + 1:] if c]), ans)
            else:
                ans = sum(cn[:k0])
                incl = ans + cn[k0]
                other = sum(cn[k0 + 1:])
                txt = "shorter than"
                e = "Shorter than %d means %s. Count the X's to the left of %d: %s = %d." % (
                    L, "less than %d, so do not count the X's above %d" % (L, L), L, plus([c for c in cn[:k0] if c]), ans)
            cand = [incl, other, n - k0 - 1 if kind == "longer" else k0, ans + 1, ans - 1]   # included L / wrong side / counted marks
            q = "How many %s are %s %s?" % (pl, txt, fmt(L, U))
            its.append(mcq(f + q, str(ans), cand, e))
        elif kind == "more":
            for _ in range(100):
                a, b = rnd.sample(range(n), 2)
                if cn[a] - cn[b] >= 2 and cn[b] > 0 and abs(V[a] - V[b]) != cn[a] - cn[b]:
                    break
            else:
                raise ValueError("no pair")
            d = cn[a] - cn[b]
            q = "How many more %s are %s long than %s long?" % (pl, fmt(V[a], U), fmt(V[b], U))
            cand = [cn[a] + cn[b], cn[a], abs(V[a] - V[b]), d + 1, d - 1, d + 2]       # added / one stack / subtracted lengths
            its.append(mcq(f + q, str(d), cand,
                           "Above %d: %s. Above %d: %s. %d − %d = %d more %s."
                           % (V[a], xs(cn[a]), V[b], xs(cn[b]), cn[a], cn[b], d, sg if d == 1 else pl)))
        else:                                                            # longest - shortest
            has = [k for k in range(n) if cn[k]]
            hi, lo = V[has[-1]], V[has[0]]
            D = hi - lo
            cand = [fmt(x, U) for x in [D + 1, hi, tot, D - 1, hi + lo]]  # counted the marks / longest only
            its.append(mcq(f + "How much longer is the longest %s than the shortest %s?" % (sg, sg), fmt(D, U), cand,
                           "Longest: %s. Shortest: %s. %d − %d = %s. (Count the jumps on the line, not the marks.)"
                           % (fmt(hi, U), fmt(lo, U), hi, lo, fmt(D, U))))
    return {"title": "Read a line plot", "items": its}



# ------------------------------------------------------------ set 5: make graphs and solve word problems
def set_make(rnd, PK, LP, P):
    its = []
    # 3: make a line plot from a list
    for t in range(3):
        ctx = LP.next()
        pl, sg, U = ctx[0], ctx[1], ctx[2]
        s, cn = make_plot(rnd, ctx, lambda c: len(set(c)) >= 4, n=5, tot=(8, 12))
        d = data_list(rnd, s, cn)
        j = rnd.choice([k for k in range(1, 4) if cn[k] >= 2])
        L = s + j
        p = P.next()
        q = ("%s measured %d %s in %s: %s. %s makes a line plot. How many X's go above %d?"
             % (p["N"], len(d), pl, U[1], ", ".join(str(x) for x in d), p["He"], L))
        cand = [cn[j - 1], cn[j + 1], len(d), cn[j] + 1, cn[j] - 1]
        its.append(mcq(q, str(cn[j]), cand,
                       "Put one X for each %s. Find every %d in the list and count them: %d. So %d X's go above %d."
                       % (sg, L, cn[j], cn[j], L)))
    # 3: which bar is wrong?
    for t in range(3):
        ctx = PK.next()
        U = ctx.unit
        for _ in range(500):
            cats, vals = make_data(ctx, 4, rnd, 2, 9)
            j = rnd.randrange(4)
            wrong = vals[j] + [1, -1, 1][t]
            drawn = vals[:]
            drawn[j] = wrong
            if wrong not in vals and 1 <= wrong <= 10:
                break
        p = P.next(avoid=cats)
        f = fig(ctx_bar(ctx, cats, drawn, t == 1))
        data = ", ".join("%s %d" % (c, v) for c, v in zip(cats, vals))
        q = "%s made this bar graph from the data: %s. Which bar is wrong?" % (p["N"], data)
        its.append(mcq(f + q, cats[j], [cats[k] for k in range(4) if k != j],
                       "Check each bar against the data. The %s bar ends at %d, but the data says %d. It is one line too %s."
                       % (cats[j], wrong, vals[j], "high" if wrong > vals[j] else "low")))
    # 3: which graph matches the data? (A-D pictures)
    used = set()
    for t, pos in enumerate([2, 0, 3]):
        n = 4 if t != 1 else 3
        ctx = PK.next(lambda c: sum(1 for x in c.cats if len(x) <= 5) >= n and not c.sumto and c.title not in used)
        used.add(ctx.title)
        U = ctx.unit
        for _ in range(500):
            cats, vals = make_data(ctx, n, rnd, 1, 6)
            if max(len(x) for x in cats) > 5:
                continue
            a, b = rnd.sample(range(n), 2)
            hi_ = list(vals); k1 = rnd.randrange(n); hi_[k1] += 1          # one bar one too high
            sw = list(vals); sw[a], sw[b] = sw[b], sw[a]                   # two bars swapped
            lo_ = list(vals); k2 = rnd.choice([k for k in range(n) if k != k1]); lo_[k2] -= 1   # one bar one too low
            g = [hi_, sw, lo_]
            if min(lo_) >= 1 and max(hi_) <= 7 and len({tuple(x) for x in g + [vals]}) == 4:
                break
        why = ["%s %d" % (cats[k1], hi_[k1]), "%s and %s switched" % (cats[a], cats[b]), "%s %d" % (cats[k2], lo_[k2])]
        order = [0, 1, 2]
        rnd.shuffle(order)
        graphs = [g[o] for o in order]
        graphs.insert(pos, vals)
        notes = [why[o] for o in order]
        notes.insert(pos, None)
        data = ", ".join("%s %d" % (c, v) for c, v in zip(cats, vals))
        L = "ABCD"[pos]
        others = "; ".join("%s has %s" % ("ABCD"[k], notes[k]) for k in range(4) if k != pos)
        its.append({"q": fig(bars4_svg(ctx.title, cats, graphs)) + "Which bar graph shows this data? %s." % data,
                    "c": ["A", "B", "C", "D"], "a": pos, "fixed": True,
                    "e": "Check every bar. Only graph <b>%s</b> matches: %s. Graph %s." % (L, data, others)})
    # 2: add more to a bar
    for t in range(2):
        ctx = PK.next(lambda c: c.unit in (VOTE, STU))
        U = ctx.unit
        cats, vals = make_data(ctx, 4, rnd, 2, 9)
        j, k = rnd.sample(range(4), 2)
        add = rnd.randint(3, 6)
        nv = vals[j] + add
        if ctx.unit == VOTE:
            q = "Later, %d more students vote for %s. How many votes does %s have now?" % (add, cats[j], cats[j])
        else:
            q = "Later, %d more students choose %s. How many students choose %s now?" % (add, ctx.p(cats[j]), ctx.p(cats[j]))
        cand = [fmt(x, U) for x in [vals[j], add, nv + 1, vals[k] + add, nv - 1]]
        its.append(mcq(fig(ctx_bar(ctx, cats, vals, t == 1)) + q, fmt(nv, U), cand,
                       "%s Add the %d new ones: %d + %d = %s." % (read_bar(cats[j], vals[j], 1), add, vals[j], add, fmt(nv, U))))
    # 2: add to a line plot
    for t in range(2):
        ctx = LP.next()
        pl, sg, U = ctx[0], ctx[1], ctx[2]
        s, cn = make_plot(rnd, ctx, lambda c: True, n=6)
        j = rnd.choice([k for k in range(1, 5) if cn[k] >= 1])
        L = s + j
        add = rnd.choice([2, 3])
        p = P.next()
        q = ("%s finds %d more %s. Each one is %s long. %s adds them to the line plot. Now how many %s are %s long?"
             % (p["N"], add, pl, fmt(L, U), p["He"], pl, fmt(L, U)))
        nv = cn[j] + add
        cand = [cn[j], sum(cn) + add, cn[j + 1] + add, nv + 1, L + add]
        its.append(mcq(fig(ctx_plot(ctx, s, cn)) + q, str(nv), cand,
                       "Right now there %s above %d. Add %d more X's: %d + %d = %d." % ("is 1 X" if cn[j] == 1 else "are " + xs(cn[j]), L, add, cn[j], add, nv)))
    # 2: reach a goal
    goals = [("Books Read This Week", "wants to read %d books this week. How many more books does %s need to read?"),
             ("Shells We Found", "wants to find %d shells. How many more shells does %s need to find?")]
    for title, tpl in goals:
        ctx = BYTITLE[title]
        U = ctx.unit
        cats, vals = make_data(ctx, 4, rnd, 2, 9)
        j = rnd.randrange(4)
        goal = rnd.choice([g for g in (10, 12, 15) if g - vals[j] >= 3])
        name = cats[j]
        he = "she" if name in GIRLS else "he"
        q = "%s %s" % (name, tpl % (goal, he))
        ans = goal - vals[j]
        cand = [goal + vals[j], vals[j], ans + 1, ans - 1, goal]
        its.append(mcq(fig(ctx_bar(ctx, cats, vals, False)) + q, fmt(ans, U), [fmt(x, U) for x in cand],
                       "%s %s has %d and wants %d. %d − %d = %s." % (read_bar(name, vals[j], 1), name, vals[j], goal,
                                                                     goal, vals[j], more_fmt(ans, U, "more"))))
    # 3: missing bar (take apart)
    for t in range(3):
        ctx = PK.next(lambda c: c.unit == STU)
        U = ctx.unit
        cats, vals = make_data(ctx, 4, rnd, 2, 8)
        j = rnd.randrange(4)
        t_ = sum(vals)
        known = [vals[k] for k in range(4) if k != j]
        q = "All %d students in the class are in this graph. The bar for %s is missing. %s" % (t_, cats[j], ctx.q("ask", cats[j]))
        cand = [sum(known), t_, t_ - sum(known[:2]), vals[j] + 1, vals[j] - 1]
        its.append(mcq(fig(ctx_bar(ctx, cats, vals, t == 1, missing=j)) + q, fmt(vals[j], U), [fmt(x, U) for x in cand],
                       "Add the bars you can see: %s = %d. All %d students: %d − %d = %s."
                       % (plus(known), sum(known), t_, t_, sum(known), fmt(vals[j], U))))
    # 2: two bars together vs one bar
    for t in range(2):
        ctx = PK.next(lambda c: c.has("more"))
        U = ctx.unit
        for _ in range(500):
            cats, vals = make_data(ctx, 4, rnd, 1, 9)
            c_ = vals.index(max(vals))
            a, b = rnd.sample([k for k in range(4) if k != c_], 2)
            if vals[a] + vals[b] - vals[c_] >= 2:
                break
        s2 = vals[a] + vals[b]
        ans = s2 - vals[c_]
        q = "How many more %s do the %s and %s bars show together than the %s bar?" % (U[1], cats[a], cats[b], cats[c_])
        cand = [s2, s2 + vals[c_], abs(vals[a] - vals[b]), ans + 1, ans - 1]
        its.append(mcq(fig(ctx_bar(ctx, cats, vals, t == 1)) + q, fmt(ans, U), [fmt(x, U) for x in cand],
                       "Step 1: %s + %s = %d + %d = %d. Step 2: compare with %s (%d): %d − %d = %s."
                       % (cats[a], cats[b], vals[a], vals[b], s2, cats[c_], vals[c_], s2, vals[c_], more_fmt(ans, U, "more"))))
    return {"title": "Make graphs and solve word problems", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


L_CATS = ["Apple", "Banana", "Grape", "Pear"]
L_VALS = [6, 3, 8, 4]
L_LEN = [5, 6, 6, 7, 4, 6, 8, 7, 6, 5]           # 10 pencils, inches
L_START, L_COUNTS = 4, [1, 2, 4, 2, 1]


def body_html():
    assert sorted(L_LEN) == [L_START + i for i, c in enumerate(L_COUNTS) for _ in range(c)]
    fr = BYTITLE["Favorite Fruit"]
    return (
        "<h2>The big idea</h2>"
        "<p>A graph shows data so you can see it fast. In Grade 2, each picture stands for <b>1</b> and each grid line "
        "on a bar graph counts by <b>1</b>. A graph can show up to 4 groups.</p>" +
        table(["Fruit", "Votes"], [[c, str(v)] for c, v in zip(L_CATS, L_VALS)]) +
        "<h2>Picture graph</h2>"
        "<p>Each picture is 1 vote. Count the pictures in a row.</p>"
        "<figure class='sn-fig'>" + ctx_pic(fr, L_CATS, L_VALS, "star") +
        "<figcaption>The Grape row has 8 stars, so Grape got 8 votes.</figcaption></figure>"
        "<h2>Bar graph</h2>"
        "<p>Go to the top of the bar. Look across to the numbers. The bar ends at the number of votes.</p>"
        "<figure class='sn-fig'>" + ctx_bar(fr, L_CATS, L_VALS) +
        "<figcaption>The Pear bar ends at the line for 4, so Pear got 4 votes.</figcaption></figure>"
        "<h2>How many in all? How many more?</h2>"
        "<p><b>In all</b> means put together, so add. <b>How many more</b> or <b>how many fewer</b> means compare, so subtract.</p>" +
        ex("In all", "How many votes did Apple and Pear get in all?", "Apple 6, Pear 4. 6 + 4 = 10.", "10 votes") +
        ex("How many more", "How many more votes did Grape get than Banana?", "Grape 8, Banana 3. 8 − 3 = 5.", "5 more votes") +
        "<h2>Line plot</h2>"
        "<p>Measure some objects. Draw a number line. Put <b>one X</b> above the length of each object.</p>"
        "<p>Leo measured 10 pencils in inches: " + ", ".join(str(x) for x in L_LEN) + ".</p>"
        "<figure class='sn-fig'>" + plot_svg(L_START, L_COUNTS, IN, label="line plot of 10 pencil lengths") +
        "<figcaption>There are 10 X's for 10 pencils. The tallest stack is above 6, so most pencils are 6 inches long.</figcaption></figure>" +
        table(["Question", "How to find it", "Answer"], [
            ["How many pencils are 7 inches long?", "Count the X's above 7", "2"],
            ["What length are the most pencils?", "Find the tallest stack", "6 inches"],
            ["How many pencils in all?", "1 + 2 + 4 + 2 + 1", "10"],
        ]) +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Reading the bar next to the one you want", "Put your finger on the name, then go up the bar"],
            ["Reading the line just above or below", "Look straight across from the top of the bar"],
            ["Adding when it asks how many more", "How many more or fewer means subtract"],
            ["Counting the bars instead of the votes", "Add the numbers the bars show"],
            ["On a line plot, giving the number of X's as the length", "The number under the stack is the length"],
        ])
    )


FAQ = [
    {"q": "What is a picture graph in 2nd grade?",
     "a": "A picture graph uses a small picture for each item, and in 2nd grade each picture stands for 1. Count the pictures in a row to find how many."},
    {"q": "How do you read a bar graph in 2nd grade?",
     "a": "Find the top of the bar and look straight across to the numbers. In 2nd grade each grid line counts by 1, so a bar that stops at 7 shows 7."},
    {"q": "How do you solve how many more questions with a bar graph?",
     "a": "Read the two bars, then subtract the smaller number from the bigger one. If Dog has 8 and Cat has 5, there are 8 − 5 = 3 more dogs."},
    {"q": "What is a line plot in 2nd grade math?",
     "a": "A line plot is a number line with an X above it for each measurement. Students measure objects to the nearest whole inch or centimeter and put one X above each length."},
]


def gen_graphs():
    rnd = random.Random(214)
    PK = Picker(rnd)
    LP = LPicker(rnd)
    P = People(rnd)
    sets = [set_picture(rnd, PK), set_bar(rnd, PK), set_compare(rnd, PK), set_lineplot(rnd, LP), set_make(rnd, PK, LP, P)]
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
        "country": "us", "subject": "math", "grade": "grade-2", "slug": "graphs-and-line-plots", "sort": 14,
        "updated": UPDATED, "pdf_url": "",
        "title": "Picture Graphs, Bar Graphs and Line Plots",
        "seo_title": "Grade 2 Picture Graph, Bar Graph and Line Plot Worksheets: Count by 1s, How Many More, Whole-Number Line Plots",
        "short_title": "Graphs and line plots",
        "domain": "Measurement and Data",
        "standard_code": "2.MD.D.9–10",
        "standard_url": "https://www.thecorestandards.org/Math/Content/2/MD/D/",
        "standard_text": "Generate measurement data by measuring lengths of several objects to the nearest whole unit, or by making repeated measurements of the same object. Show the measurements by making a line plot, where the horizontal scale is marked off in whole-number units. Draw a picture graph and a bar graph (with single-unit scale) to represent a data set with up to four categories. Solve simple put-together, take-apart, and compare problems using information presented in a bar graph.",
        "meta_desc": "Free Grade 2 graph worksheets: read picture graphs where each picture is 1, bar graphs that count by 1s and tally charts with up to 4 groups, solve how many in all, how many more and how many fewer, and read whole-number line plots. 100 practice questions with answers.",
        "key_big": "Each picture is 1. Each grid line is 1. Each X is 1.",
        "key_sub": "Count the pictures in a row, or look straight across from the top of a bar. In all means add; how many more or fewer means subtract. On a line plot, the number under the X's is the length.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


def mark_large(u, pattern):
    """Tag pictures that must print larger (graphs, line plots, A-D choices) so their labels stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


if __name__ == "__main__":
    u = gen_graphs()
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as f:
        mark_large(u, "(picture graph|bar graph|tally chart|line plot|four bar graphs)")
        json.dump(u, f, ensure_ascii=False, indent=1)
    print("wrote", path)
