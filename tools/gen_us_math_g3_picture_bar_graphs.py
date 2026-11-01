# -*- coding: utf-8 -*-
"""
US Grade 3 Math: Picture Graphs and Bar Graphs (3.MD.B.3)
  python tools/gen_us_math_g3_picture_bar_graphs.py
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, re, math, os, random

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "us", "math", "grade-3")
UPDATED = "2026-11-01"
GREEN = "#006633"
BAR = "#2e8b57"
FILL = "#cfe6d6"
RED = "#c0392b"
INK = "#2b2b2b"
GRID = "#c9d3cc"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Maya", "Ava", "Mia", "Zoe", "Lily", "Emma", "Nora", "Ruby", "Sofia", "Grace"]
BOYS = ["Leo", "Noah", "Eli", "Sam", "Ben", "Omar", "Kai", "Jack", "Luis", "Owen"]


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e, rnd):
    """4 choices: correct + 3 unique distractors (no zero or negative numbers)."""
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        c = str(c)
        lead = c.split(" ")[0].lstrip("$")
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
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def tw(t, fs, bold=False):
    """Approximate text width in px (Arial)."""
    return len(str(t)) * fs * (0.62 if bold else 0.58)


def text(x, y, t, fs=14, anchor="middle", bold=False, col=INK, extra=""):
    return ("<text x='%.1f' y='%.1f' font-size='%d'%s fill='%s' text-anchor='%s'%s>%s</text>"
            % (x, y, fs, " font-weight='700'" if bold else "", col, anchor, extra, t))


def fmt(v, unit):
    """unit = (singular, plural)."""
    if unit[0] == "$":
        return "$%d" % v
    return "%d %s" % (v, unit[0] if v == 1 else unit[1])


def ones(cnt, word):
    return "%d %s" % (cnt, word if cnt == 1 else word + "s")


# ------------------------------------------------------------ symbols (no clip paths: ids would clash on one page)
def star_pts(cx, cy, R=9.5, r=4.0):
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rad = R if i % 2 == 0 else r
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    return pts


def symbol(kind, cx, cy, half=False, col=GREEN):
    """A whole symbol, or its left half."""
    if kind == "circle":
        if half:
            return "<path d='M%.1f %.1f A8.5 8.5 0 0 0 %.1f %.1f Z' fill='%s'/>" % (cx, cy - 8.5, cx, cy + 8.5, col)
        return "<circle cx='%.1f' cy='%.1f' r='8.5' fill='%s'/>" % (cx, cy, col)
    if kind == "square":
        return "<rect x='%.1f' y='%.1f' width='%.1f' height='15' rx='2' fill='%s'/>" % (cx - 7.5, cy - 7.5, 7.5 if half else 15, col)
    pts = star_pts(cx, cy)
    if half:
        pts = [pts[0], pts[9], pts[8], pts[7], pts[6], pts[5]]     # top point, left side, bottom inner point
    return "<polygon points='%s' fill='%s'/>" % (" ".join("%.1f,%.1f" % p for p in pts), col)


SYMS = ["circle", "star", "square"]


# ------------------------------------------------------------ contexts
class Ctx:
    def __init__(self, title, axis, cats, unit, ask, more, fewer, total, keys, ph=None, ordered=False,
                 sumto=None, nota=None):
        self.title, self.axis, self.cats, self.unit = title, axis, cats, unit
        self.ask_f, self.more_f, self.fewer_f, self.total = ask, more, fewer, total
        self.keys, self.ph, self.ordered, self.sumto, self.nota_f = keys, ph or {}, ordered, sumto, nota

    def p(self, c):
        return self.ph.get(c, c)

    def ask(self, c):
        return self.ask_f.format(a=self.p(c))

    def more(self, a, b):
        return self.more_f.format(a=self.p(a), b=self.p(b))

    def fewer(self, a, b):
        return self.fewer_f.format(a=self.p(a), b=self.p(b))

    def nota(self, c):
        return self.nota_f.format(a=self.p(c))


VOTE = ("vote", "votes")
STU = ("student", "students")
LOWER = lambda cs: {c: c.lower() for c in cs}

CTXS = [
    Ctx("Favorite Fruit", "Fruit", ["Apple", "Banana", "Grape", "Orange", "Pear"], VOTE,
        "How many votes did {a} get?", "How many more votes did {a} get than {b}?",
        "How many fewer votes did {a} get than {b}?", "How many votes were there in all?", [2, 5],
        nota="How many votes were not for {a}?"),
    Ctx("Pets We Have", "Pet", ["Dog", "Cat", "Fish", "Bird", "Hamster"], STU,
        "How many students have a {a}?", "How many more students have a {a} than a {b}?",
        "How many fewer students have a {a} than a {b}?", "How many students are shown in all?", [2],
        ph=LOWER(["Dog", "Cat", "Fish", "Bird", "Hamster"])),
    Ctx("Books Read in March", "Student", ["Maya", "Leo", "Ava", "Noah", "Zoe", "Ben"], ("book", "books"),
        "How many books did {a} read?", "How many more books did {a} read than {b}?",
        "How many fewer books did {a} read than {b}?", "How many books did the students read in all?", [2]),
    Ctx("Weather in April", "Weather", ["Sunny", "Cloudy", "Rainy", "Windy"], ("day", "days"),
        "How many days were {a}?", "How many more days were {a} than {b}?",
        "How many fewer days were {a} than {b}?", "How many days are shown in all?", [2],
        ph=LOWER(["Sunny", "Cloudy", "Rainy", "Windy"]), ordered=True, sumto=30,
        nota="How many days were not {a}?"),
    Ctx("How We Get to School", "Way", ["Bus", "Car", "Walk", "Bike"], STU,
        "How many students {a} to school?", "How many more students {a} to school than {b}?",
        "How many fewer students {a} to school than {b}?", "How many students are in the survey in all?", [5, 10],
        ph={"Bus": "ride the bus", "Car": "come by car", "Walk": "walk", "Bike": "ride a bike"}, ordered=True),
    Ctx("Favorite Sport", "Sport", ["Soccer", "Baseball", "Swimming", "Tennis", "Hockey"], STU,
        "How many students chose {a}?", "How many more students chose {a} than {b}?",
        "How many fewer students chose {a} than {b}?", "How many students voted in all?", [2, 5, 10],
        ph=LOWER(["Soccer", "Baseball", "Swimming", "Tennis", "Hockey"]),
        nota="How many students did not choose {a}?"),
    Ctx("Cans Collected", "Class", ["Room 1", "Room 2", "Room 3", "Room 4"], ("can", "cans"),
        "How many cans did {a} collect?", "How many more cans did {a} collect than {b}?",
        "How many fewer cans did {a} collect than {b}?", "How many cans did the classes collect in all?", [5, 10],
        ordered=True),
    Ctx("Lemonade Sold", "Day", ["Mon", "Tue", "Wed", "Thu", "Fri"], ("cup", "cups"),
        "How many cups of lemonade were sold on {a}?", "How many more cups were sold on {a} than on {b}?",
        "How many fewer cups were sold on {a} than on {b}?", "How many cups were sold in all?", [2, 5, 10],
        ph={"Mon": "Monday", "Tue": "Tuesday", "Wed": "Wednesday", "Thu": "Thursday", "Fri": "Friday"}, ordered=True),
    Ctx("Birds at the Feeder", "Bird", ["Robin", "Sparrow", "Blue Jay", "Finch"], ("bird", "birds"),
        "How many {a} were seen?", "How many more {a} than {b} were seen?",
        "How many fewer {a} than {b} were seen?", "How many birds were seen in all?", [2, 5],
        ph={"Robin": "robins", "Sparrow": "sparrows", "Blue Jay": "blue jays", "Finch": "finches"}),
    Ctx("Favorite Color", "Color", ["Red", "Blue", "Green", "Purple", "Yellow"], VOTE,
        "How many votes did {a} get?", "How many more votes did {a} get than {b}?",
        "How many fewer votes did {a} get than {b}?", "How many votes were there in all?", [2, 5, 10],
        nota="How many votes were not for {a}?"),
    Ctx("Trees in the Park", "Tree", ["Oak", "Maple", "Pine", "Birch"], ("tree", "trees"),
        "How many {a} trees are in the park?", "How many more {a} trees than {b} trees are in the park?",
        "How many fewer {a} trees than {b} trees are in the park?", "How many trees are in the park in all?", [5, 10],
        ph=LOWER(["Oak", "Maple", "Pine", "Birch"])),
    Ctx("Ice Cream Cones Sold", "Flavor", ["Vanilla", "Chocolate", "Mint", "Mango"], ("cone", "cones"),
        "How many {a} cones were sold?", "How many more {a} cones than {b} cones were sold?",
        "How many fewer {a} cones than {b} cones were sold?", "How many cones were sold in all?", [5, 10],
        ph=LOWER(["Vanilla", "Chocolate", "Mint", "Mango"])),
    Ctx("Points Scored", "Team", ["Lions", "Tigers", "Bears", "Hawks"], ("point", "points"),
        "How many points did the {a} score?", "How many more points did the {a} score than the {b}?",
        "How many fewer points did the {a} score than the {b}?", "How many points did the teams score in all?", [2, 5, 10]),
    Ctx("Stickers Collected", "Student", ["Ruby", "Omar", "Lily", "Kai", "Grace"], ("sticker", "stickers"),
        "How many stickers does {a} have?", "How many more stickers does {a} have than {b}?",
        "How many fewer stickers does {a} have than {b}?", "How many stickers do they have in all?", [2, 5, 10]),
    Ctx("Favorite Season", "Season", ["Spring", "Summer", "Fall", "Winter"], VOTE,
        "How many votes did {a} get?", "How many more votes did {a} get than {b}?",
        "How many fewer votes did {a} get than {b}?", "How many votes were there in all?", [2, 5, 10], ordered=True,
        nota="How many votes were not for {a}?"),
    Ctx("Library Books Checked Out", "Topic", ["Animals", "Sports", "Space", "Mystery"], ("book", "books"),
        "How many {a} books were checked out?", "How many more {a} books than {b} books were checked out?",
        "How many fewer {a} books than {b} books were checked out?", "How many books were checked out in all?", [5, 10]),
    Ctx("Seashells Found", "Student", ["Sam", "Nora", "Eli", "Mia", "Owen"], ("shell", "shells"),
        "How many shells did {a} find?", "How many more shells did {a} find than {b}?",
        "How many fewer shells did {a} find than {b}?", "How many shells did they find in all?", [2, 5]),
    Ctx("Favorite Lunch", "Lunch", ["Pizza", "Tacos", "Pasta", "Salad"], STU,
        "How many students chose {a}?", "How many more students chose {a} than {b}?",
        "How many fewer students chose {a} than {b}?", "How many students voted in all?", [2, 5, 10],
        ph=LOWER(["Pizza", "Tacos", "Pasta", "Salad"]),
        nota="How many students did not choose {a}?"),
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


def make_data(ctx, n, step, half, rnd, max_units=8, min_units=1):
    """n unique values. Each value is a whole number of steps, or (half=True) may end on a half step."""
    if ctx.ordered:
        start = rnd.randint(0, len(ctx.cats) - n)
        cats = ctx.cats[start:start + n]
    else:
        cats = rnd.sample(ctx.cats, n)
    for _ in range(2000):
        units = []
        for i in range(n):
            u = rnd.randint(min_units, max_units)
            hs = half and rnd.random() < 0.45 and u < max_units
            units.append(u + (0.5 if hs else 0))
        vals = [int(u * step) for u in units]
        if len(set(vals)) != n:
            continue
        if ctx.sumto and sum(vals) != ctx.sumto:
            continue
        if half and not any(u % 1 for u in units):
            continue
        return cats, vals
    raise ValueError("no data for " + ctx.title)


# ------------------------------------------------------------ graphs
def pic_svg(title, cats, vals, key, sym, unit, key_q=False, label="picture graph"):
    """Picture graph: one row per category, symbols worth `key` each, key line at the bottom."""
    fs, rh, gap = 15, 26, 23
    lw = max(tw(c, fs, True) for c in cats) + 22

    nsym = [math.ceil(v / key) for v in vals]
    m = max(max(nsym), 4)
    W = lw + 12 + m * gap + 14
    keytxt = "= ?" if key_q else "= " + fmt(key, unit)
    kw = tw("Key:", fs, True) + 32 + tw(keytxt, fs)
    W = int(max(W, tw(title, 16, True) + 16, kw + 16))
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
        full, hf = v // key, v % key
        for j in range(full + (1 if hf else 0)):
            if j == full:                           # pale outline of the whole symbol behind a half symbol
                s.append(symbol(sym, lw + 12 + j * gap + 9, y + rh / 2, col=FILL))
            s.append(symbol(sym, lw + 12 + j * gap + 9, y + rh / 2, half=(j == full)))
    ky = top + H_tab + 22
    x = (W - kw) / 2
    s.append(text(x, ky, "Key:", fs, anchor="start", bold=True))
    x += tw("Key:", fs, True) + 16
    s.append(symbol(sym, x, ky - 5))
    s.append(text(x + 14, ky, keytxt, fs, anchor="start", col=RED if key_q else INK))
    H = ky + 8
    return svg_wrap(W, H, "".join(s), label)


def bar_svg(title, cat_axis, val_axis, cats, vals, scale, horizontal=False, missing=None, label="bar graph"):
    """Scaled bar graph with a grid line at every step of the scale.
    `missing` = index of a category drawn with no bar (a red ? shows where it goes)."""
    fs = 14
    top_v = int(math.ceil(max(vals) / scale) * scale)
    nt = top_v // scale
    assert 2 <= nt <= 8, (title, vals, scale)
    s = []
    if not horizontal:
        gy = 16 if nt > 6 else 19
        ph = nt * gy
        lw = tw(top_v, fs)
        x0 = 22 + lw + 6
        slot = max(46, max(tw(c, fs) for c in cats) + 10)
        pw = slot * len(cats)
        y0 = 32
        yb = y0 + ph
        W = x0 + pw + 8
        W = max(W, tw(title, 16, True) + 16)
        s.append(text(W / 2, 18, title, 16, bold=True))
        for k in range(nt + 1):
            y = yb - k * gy
            s.append("<line x1='%d' y1='%.1f' x2='%d' y2='%.1f' stroke='%s' stroke-width='1'/>" % (x0, y, x0 + pw, y, GRID))
            s.append(text(x0 - 5, y + 5, k * scale, fs, anchor="end"))
        for i, (c, v) in enumerate(zip(cats, vals)):
            cx = x0 + slot * i + slot / 2
            bw = min(30, slot * 0.62)
            if i == missing:
                s.append(text(cx, yb - 6, "?", 18, bold=True, col=RED))
            else:
                h = v / scale * gy
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
        gx = 26 if nt > 6 else 30
        pw = nt * gx
        lw = max(tw(c, fs) for c in cats)
        x0 = 24 + lw + 8
        y0 = 30
        ph = rh * len(cats)
        yb = y0 + ph
        W = x0 + pw + tw(top_v, fs) / 2 + 6
        W = max(W, tw(title, 16, True) + 16)
        s.append(text(W / 2, 18, title, 16, bold=True))
        for k in range(nt + 1):
            x = x0 + k * gx
            s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='1'/>" % (x, y0, x, yb, GRID))
            s.append(text(x, yb + 17, k * scale, fs))
        for i, (c, v) in enumerate(zip(cats, vals)):
            cy = y0 + rh * i + rh / 2
            if i == missing:
                s.append(text(x0 + 10, cy + 6, "?", 18, bold=True, col=RED))
            else:
                w = v / scale * gx
                s.append("<rect x='%d' y='%.1f' width='%.1f' height='16' fill='%s'/>" % (x0, cy - 8, w, BAR))
            s.append(text(x0 - 6, cy + 5, c, fs, anchor="end"))
        s.append("<path d='M%d %d V%d H%d' fill='none' stroke='%s' stroke-width='2'/>" % (x0, y0, yb, x0 + pw + 4, INK))
        s.append(text(x0 + pw / 2, yb + 36, val_axis, fs, bold=True))
        mid = y0 + ph / 2
        s.append(text(13, mid, cat_axis, fs, bold=True, extra=" transform='rotate(-90 13 %.1f)'" % mid))
        H = yb + 42
        assert tw(cat_axis, fs, True) < ph + 26, (cat_axis, ph)
    return svg_wrap(int(math.ceil(W)), int(H), "".join(s), label)


def ctx_bar(ctx, cats, vals, scale, horizontal, missing=None):
    return bar_svg(ctx.title, ctx.axis, ctx.unit[1].capitalize() if ctx.unit[0] != "$" else "Dollars", cats, vals,
                   scale, horizontal, missing, label="bar graph: " + ctx.title.lower())


def ctx_pic(ctx, cats, vals, key, sym, key_q=False):
    return pic_svg(ctx.title, cats, vals, key, sym, ctx.unit, key_q, label="picture graph: " + ctx.title.lower())


# ------------------------------------------------------------ reading text (used in explanations)
def read_pic(c, v, key, sym, unit):
    full, hf = v // key, v % key
    if hf:
        if full == 0:
            return "The %s row has half a %s: half of %d is %s." % (c, sym, key, fmt(v, unit))
        return ("The %s row has %s and half a %s: %d × %d = %d, and half of %d is %d, so %d + %d = %s."
                % (c, ones(full, sym), sym, full, key, full * key, key, hf, full * key, hf, fmt(v, unit)))
    return "The %s row has %s: %d × %d = %s." % (c, ones(full, sym), full, key, fmt(v, unit))


def more_fmt(d, unit, word):
    return "%d %s %s" % (d, word, unit[0] if d == 1 else unit[1])


def read_bar(c, v, scale):
    if v % scale:
        lo = v - v % scale
        return "The %s bar ends halfway between %d and %d, so it shows %d." % (c, lo, lo + scale, v)
    return "The %s bar ends at the line for %d." % (c, v)


def pic_read_cands(v, key, others, unit):
    full, hf = v // key, v % key
    drawn = full + (1 if hf else 0)
    c = [drawn]                                     # counted the symbols
    if hf:
        c += [full * key, (full + 1) * key]         # ignored the half / counted it as whole
    c += [v + key, v - key] + others + [v * 2]
    return [fmt(x, unit) for x in c]


def bar_read_cands(v, scale, others, unit):
    c = []
    if v % scale:
        lo = v - v % scale
        c += [lo, lo + scale]                       # read the line below / above
    elif v // scale != v:
        c += [v // scale]                           # counted grid spaces
    c += [v + scale, v - scale] + others + [v + 1]
    return [fmt(x, unit) for x in c]


# ------------------------------------------------------------ set 1: picture graphs
def set_picture(rnd, PK):
    its = []
    plan = (["read"] * 13 + ["most", "fewest", "most"] + ["half", "half"] + ["which", "which"])
    keys = [2, 5, 10, 2, 10, 5, 2, 10, 5, 2, 5, 10, 2, 5, 10, 2, 10, 2, 5, 10]
    for i, kind in enumerate(plan):
        key = keys[i]
        if kind == "half":
            key = [2, 10][plan[:i].count("half")]
        ctx = PK.next(lambda c: key in c.keys)
        sym = SYMS[i % 3]
        half = key % 2 == 0 and (kind == "half" or (kind == "read" and i % 2 == 0))
        n = 5 if i % 4 == 3 and len(ctx.cats) >= 5 else 4
        cats, vals = make_data(ctx, n, key, half, rnd, max_units=7)
        f = fig(ctx_pic(ctx, cats, vals, key, sym))
        U = ctx.unit
        if kind == "read":
            if half:
                j = rnd.choice([k for k, v in enumerate(vals) if v % key])
            else:
                j = rnd.randrange(n)
            c, v = cats[j], vals[j]
            others = [vals[k] for k in range(n) if k != j]
            its.append(mcq(f + ctx.ask(c), fmt(v, U), pic_read_cands(v, key, others, U),
                           "Each %s stands for %s. %s" % (sym, fmt(key, U), read_pic(c, v, key, sym, U)), rnd))
        elif kind in ("most", "fewest"):
            j = vals.index(max(vals) if kind == "most" else min(vals))
            word = "the most" if kind == "most" else "the fewest"
            q = "Which row shows %s %s?" % (word, U[1])
            its.append(mcq(f + q, cats[j], [cats[k] for k in range(n) if k != j],
                           "Every %s has the same value, so the row with %s %ss wins. %s"
                           % (sym, "the most" if kind == "most" else "the fewest", sym,
                              read_pic(cats[j], vals[j], key, sym, U)), rnd))
        elif kind == "half":
            its.append(mcq(f + "In this graph, what does half a %s stand for?" % sym, fmt(key // 2, U),
                           [fmt(key, U), "half a " + U[0], fmt(key * 2, U), fmt(1, U)],
                           "The key says one whole %s = %s. Half a %s is half of %d, which is %s."
                           % (sym, fmt(key, U), sym, key, fmt(key // 2, U)), rnd))
        else:
            j = rnd.randrange(n)
            v = vals[j]
            cand = [cats[k] for k in range(n) if k != j and math.ceil(vals[k] / key) == v] + \
                   [cats[k] for k in range(n) if k != j]
            its.append(mcq(f + "Which row shows %s?" % fmt(v, U), cats[j], cand,
                           "%s ÷ %d = %d, so look for a row with %s. %s"
                           % (fmt(v, U), key, v // key, ones(v // key, sym), read_pic(cats[j], v, key, sym, U)), rnd))
    return {"title": "Read a picture graph with a key", "items": its}


# ------------------------------------------------------------ set 2: bar graphs
def set_bar(rnd, PK):
    its = []
    plan = ["read"] * 15 + ["which"] * 3 + ["most", "fewest"]
    scales = [2, 5, 10, 2, 10, 5, 10, 2, 5, 10, 2, 5, 10, 2, 10, 5, 2, 10, 5, 2]
    for i, kind in enumerate(plan):
        sc = scales[i]
        ctx = PK.next(lambda c: sc in c.keys)
        half = sc != 5 and i % 3 != 1
        hor = i % 2 == 1
        n = 4
        cats, vals = make_data(ctx, n, sc, half, rnd, max_units=7)
        f = fig(ctx_bar(ctx, cats, vals, sc, hor))
        U = ctx.unit
        scl = "The scale counts by %d." % sc
        if kind == "read":
            if half and i % 2 == 0:
                j = rnd.choice([k for k, v in enumerate(vals) if v % sc])
            else:
                j = rnd.randrange(n)
            c, v = cats[j], vals[j]
            others = [vals[k] for k in range(n) if k != j]
            its.append(mcq(f + ctx.ask(c), fmt(v, U), bar_read_cands(v, sc, others, U),
                           "%s %s So the answer is %s." % (scl, read_bar(c, v, sc), fmt(v, U)), rnd))
        elif kind == "which":
            j = rnd.randrange(n)
            v = vals[j]
            its.append(mcq(f + "Which bar shows %s?" % fmt(v, U), cats[j], [cats[k] for k in range(n) if k != j],
                           "%s Find %d on the scale. %s" % (scl, v, read_bar(cats[j], v, sc)), rnd))
        else:
            j = vals.index(max(vals) if kind == "most" else min(vals))
            word = "longest" if kind == "most" else "shortest"
            if not hor:
                word = "tallest" if kind == "most" else "shortest"
            q = "Which bar shows %s %s?" % ("the most" if kind == "most" else "the fewest", U[1])
            its.append(mcq(f + q, cats[j], [cats[k] for k in range(n) if k != j],
                           "The %s bar is the %s one. %s It shows %s." % (cats[j], word, read_bar(cats[j], vals[j], sc),
                                                                          fmt(vals[j], U)), rnd))
    return {"title": "Read a scaled bar graph", "items": its}


# ------------------------------------------------------------ set 3: how many more / fewer
def compare_item(rnd, PK, kind, pic, sc, hor, i):
    ctx = PK.next(lambda c: sc in c.keys)
    half = sc % 2 == 0 and i % 3 == 0
    cats, vals = make_data(ctx, 4, sc, half, rnd, max_units=7)
    U = ctx.unit
    order = sorted(range(4), key=lambda k: -vals[k])
    while True:
        a, b = sorted(rnd.sample(range(4), 2), key=lambda k: -vals[k])
        if vals[a] - vals[b] >= 2 and not (half and vals[a] % sc == 0 and vals[b] % sc == 0 and i % 2 == 0):
            break
    va, vb = vals[a], vals[b]
    d = va - vb
    sym = SYMS[i % 3]
    if pic:
        f = fig(ctx_pic(ctx, cats, vals, sc, sym))
        r1, r2 = read_pic(cats[a], va, sc, sym, U), read_pic(cats[b], vb, sc, sym, U)
        steps = math.ceil(va / sc) - math.ceil(vb / sc)
    else:
        f = fig(ctx_bar(ctx, cats, vals, sc, hor))
        r1, r2 = read_bar(cats[a], va, sc), read_bar(cats[b], vb, sc)
        steps = d // sc if d // sc else d + 1
    q = ctx.more(cats[a], cats[b]) if kind == "more" else ctx.fewer(cats[b], cats[a])
    other = [k for k in range(4) if k not in (a, b)][0]
    cand = [va + vb, steps, d + sc, d - sc, abs(vals[other] - vb) or d + 2, va, d + 1]
    word = "more" if kind == "more" else "fewer"
    e = "%s %s %d − %d = %d, so the answer is %s." % (r1, r2, va, vb, d, more_fmt(d, U, word))
    if not pic:
        e = "The scale counts by %d. " % sc + e
    return mcq(f + q, fmt(d, U), [fmt(x, U) for x in cand], e, rnd)


def set_compare(rnd, PK):
    its = []
    scales = [2, 5, 10, 2, 5, 10, 10, 2, 5, 10, 2, 5, 10, 2, 5, 10, 2, 10, 5, 2]
    for i in range(20):
        pic = i % 10 in (2, 5, 8)
        kind = "more" if i % 2 == 0 else "fewer"
        its.append(compare_item(rnd, PK, kind, pic, scales[i], i % 4 in (1, 2), i))
    return {"title": "How many more? How many fewer?", "items": its}


# ------------------------------------------------------------ set 4: two-step questions
def set_two_step(rnd, PK):
    its = []
    plan = ["total"] * 4 + ["pair_vs_one"] * 4 + ["not"] * 3 + ["range"] * 3 + ["pairs"] * 3 + ["pic_two"] * 3
    scales = [2, 5, 10, 5, 10, 2, 5, 10, 5, 10, 2, 10, 5, 2, 10, 2, 5, 2, 10, 2]
    for i, kind in enumerate(plan):
        sc = scales[i]
        ok = (lambda c: sc in c.keys and c.nota_f) if kind == "not" else (lambda c: sc in c.keys)
        ctx = PK.next(ok)
        U = ctx.unit
        pic = kind == "pic_two"
        half = sc % 2 == 0 and i % 2 == 0
        hor = i % 2 == 1
        for _ in range(500):
            cats, vals = make_data(ctx, 4, sc, half, rnd, max_units=7)
            srt = sorted(range(4), key=lambda k: -vals[k])
            if kind == "pair_vs_one":
                c_ = srt[0]
                a, b = [k for k in range(4) if k != c_][:2] if False else rnd.sample([k for k in range(4) if k != c_], 2)
                if vals[a] + vals[b] - vals[c_] >= 2:
                    break
            elif kind == "pairs":
                a, b, c_, d_ = srt[0], srt[3], srt[1], srt[2]
                if rnd.random() < 0.5:
                    a, b, c_, d_ = srt[0], srt[2], srt[1], srt[3]
                if vals[a] + vals[b] - vals[c_] - vals[d_] >= 2:
                    break
            else:
                break
        sym = SYMS[i % 3]
        f = fig(ctx_pic(ctx, cats, vals, sc, sym) if pic else ctx_bar(ctx, cats, vals, sc, hor))
        rd = (lambda k: read_pic(cats[k], vals[k], sc, sym, U)) if pic else (lambda k: read_bar(cats[k], vals[k], sc))
        lst = ", ".join("%s %d" % (cats[k], vals[k]) for k in range(4))
        if kind == "total":
            t = sum(vals)
            miss = t - min(vals)
            its.append(mcq(f + ctx.total, fmt(t, U),
                           [fmt(x, U) for x in [miss, t - max(vals), sum(math.ceil(v / sc) for v in vals), t + sc, t - sc, t + 10]],
                           "Step 1: read every bar: %s. Step 2: add them: %s = %s."
                           % (lst, " + ".join(str(v) for v in vals), fmt(t, U)), rnd))
        elif kind == "pair_vs_one":
            s2 = vals[a] + vals[b]
            ans = s2 - vals[c_]
            q = "How many more %s do the %s and %s bars show together than the %s bar?" % (U[1], cats[a], cats[b], cats[c_])
            its.append(mcq(f + q, fmt(ans, U),
                           [fmt(x, U) for x in [s2, s2 + vals[c_], abs(vals[a] - vals[b]), ans + sc, ans - sc, ans + 2]],
                           "Step 1: %s + %s = %d + %d = %d. Step 2: compare with %s (%d): %d − %d = %d, so %s."
                           % (cats[a], cats[b], vals[a], vals[b], s2, cats[c_], vals[c_], s2, vals[c_], ans, more_fmt(ans, U, "more")), rnd))
        elif kind == "not":
            t = sum(vals)
            j = rnd.randrange(4)
            ans = t - vals[j]
            its.append(mcq(f + ctx.nota(cats[j]), fmt(ans, U),
                           [fmt(x, U) for x in [t, vals[j], ans - vals[(j + 1) % 4], ans + sc, ans - sc]],
                           "Step 1: add all the bars: %s = %d. Step 2: take away %s (%d): %d − %d = %s. "
                           "Or add the other three bars: %s = %d."
                           % (" + ".join(str(v) for v in vals), t, cats[j], vals[j], t, vals[j], fmt(ans, U),
                              " + ".join(str(vals[k]) for k in range(4) if k != j), ans), rnd))
        elif kind == "range":
            hi, lo = srt[0], srt[3]
            ans = vals[hi] - vals[lo]
            q = "What is the difference between the greatest number and the least number of %s?" % U[1]
            its.append(mcq(f + q, fmt(ans, U),
                           [fmt(x, U) for x in [vals[hi], vals[hi] + vals[lo], vals[hi] - vals[srt[2]],
                                                vals[srt[1]] - vals[lo], ans + sc, ans - sc]],
                           "Step 1: find the greatest and the least. The %s bar is the greatest (%d). The %s bar is the least (%d). "
                           "Step 2: %d − %d = %s." % (cats[hi], vals[hi], cats[lo], vals[lo], vals[hi], vals[lo], fmt(ans, U)), rnd))
        elif kind == "pairs":
            s1, s2 = vals[a] + vals[b], vals[c_] + vals[d_]
            ans = s1 - s2
            q = ("How many more %s do the %s and %s bars show together than the %s and %s bars?"
                 % (U[1], cats[a], cats[b], cats[c_], cats[d_]))
            its.append(mcq(f + q, fmt(ans, U),
                           [fmt(x, U) for x in [s1, s1 + s2, s2, ans + sc, ans - sc, ans + 1]],
                           "Step 1: %s + %s = %d + %d = %d, and %s + %s = %d + %d = %d. Step 2: %d − %d = %d, so %s."
                           % (cats[a], cats[b], vals[a], vals[b], s1, cats[c_], cats[d_], vals[c_], vals[d_], s2,
                              s1, s2, ans, more_fmt(ans, U, "more")), rnd))
        else:                                       # picture graph: two rows together
            hs = [k for k in range(4) if vals[k] % sc] or [0]
            a = hs[0]
            b = rnd.choice([k for k in range(4) if k != a])
            ans = vals[a] + vals[b]
            drawn = math.ceil(vals[a] / sc) + math.ceil(vals[b] / sc)
            q = "How many %s do the %s and %s rows show in all?" % (U[1], cats[a], cats[b])
            its.append(mcq(f + q, fmt(ans, U),
                           [fmt(x, U) for x in [drawn, (vals[a] // sc + vals[b] // sc) * sc, drawn * sc,
                                                abs(vals[a] - vals[b]), ans + sc]],
                           "Step 1: %s %s Step 2: %d + %d = %s."
                           % (read_pic(cats[a], vals[a], sc, sym, U), read_pic(cats[b], vals[b], sc, sym, U),
                              vals[a], vals[b], fmt(ans, U)), rnd))
    return {"title": "Two-step questions", "items": its}


# ------------------------------------------------------------ set 5: make graphs and solve word problems
def set_make(rnd, PK):
    its = []
    # 5: missing bar
    for i, sc in enumerate([5, 2, 10, 10, 2]):
        ctx = PK.next(lambda c: sc in c.keys)
        U = ctx.unit
        halfq = i in (3, 4)
        for _ in range(500):
            cats, vals = make_data(ctx, 4, sc, False, rnd, max_units=7, min_units=2)
            j = rnd.randrange(4)
            if halfq:
                vals[j] += sc // 2
            if len(set(vals)) == 4 and vals[j] // sc >= 2 and math.ceil(max(vals) / sc) <= 8:
                break
        f = fig(ctx_bar(ctx, cats, vals, sc, False, missing=j))
        v = vals[j]
        if not halfq:
            sp = v // sc
            its.append(mcq(f + "The bar for %s is missing. It should show %s. How many grid spaces tall should the bar be?"
                           % (cats[j], fmt(v, U)), ones(sp, "space"),
                           [ones(x, "space") for x in [v, sp + 1, sp - 1, sc, sp + 2]],
                           "Each grid space stands for %d. %d ÷ %d = %d, so the bar is %s tall and ends at the line for %d. "
                           "Drawing %s would forget the scale." % (sc, v, sc, sp, ones(sp, "space"), v, ones(v, "space")), rnd))
        else:
            lo = v - v % sc
            ans = "halfway between %d and %d" % (lo, lo + sc)
            its.append(mcq(f + "The bar for %s is missing. It should show %s. Where should the top of the bar be?"
                           % (cats[j], fmt(v, U)), ans,
                           ["at the line for %d" % lo, "at the line for %d" % (lo + sc),
                            "halfway between %d and %d" % (lo - sc, lo),
                            "halfway between %d and %d" % (lo + sc, lo + 2 * sc)],
                           "The scale counts by %d. %d is between %d and %d, exactly in the middle (%d + %d = %d). "
                           "So the bar ends halfway between the two lines." % (sc, v, lo, lo + sc, lo, sc // 2, v), rnd))
    # 4: how many symbols to draw
    draw = [("Ava", "books", "star", 5, 35), ("The Tigers", "points", "circle", 2, 9),
            ("Room 3", "cans", "square", 10, 60), ("Fall", "votes", "star", 10, 45)]
    stories = ["On a picture graph, each star stands for 5 books. Ava read 35 books. How many stars should be in Ava's row?",
               "On a picture graph, each circle stands for 2 points. The Tigers scored 9 points. How many circles should be in the Tigers' row?",
               "On a picture graph, each square stands for 10 cans. Room 3 collected 60 cans. How many squares should be in the Room 3 row?",
               "On a picture graph, each star stands for 10 votes. Fall got 45 votes. How many stars should be in the Fall row?"]
    for (who, noun, sym, key, v), q in zip(draw, stories):
        full, hf = v // key, v % key
        if hf:
            ans = "%d and a half %ss" % (full, sym)
            cand = [ones(v, sym), ones(full, sym), ones(full + 1, sym), "%d and a half %ss" % (full - 1, sym)]
            e = ("%d ÷ %d = %d with %d left over. %d is half of %d, so draw %s and half a %s. Check: %d × %d + %d = %d."
                 % (v, key, full, hf, hf, key, ones(full, sym), sym, full, key, hf, v))
        else:
            ans = ones(full, sym)
            cand = [ones(v, sym), ones(key, sym), ones(full + 1, sym), ones(full - 1, sym)]
            e = "%d ÷ %d = %d, so draw %s. Check: %d × %d = %d. Drawing %d would forget the key." % (v, key, full, ans, full, key, v, v)
        its.append(mcq(q, ans, cand, e, rnd))
    # 3: what should the key say?
    for i, key in enumerate([5, 2, 10]):
        ctx = PK.next(lambda c: key in c.keys)
        U = ctx.unit
        sym = SYMS[(i + 1) % 3]
        for _ in range(500):
            cats, vals = make_data(ctx, 4, key, False, rnd, max_units=7, min_units=2)
            j = rnd.randrange(4)
            cnt = vals[j] // key
            if cnt >= 3 and cnt != key:
                break
        f = fig(ctx_pic(ctx, cats, vals, key, sym, key_q=True))
        v = vals[j]
        q = "The %s row stands for %s. The key is missing. Each %s should stand for how many %s?" % (cats[j], fmt(v, U), sym, U[1])
        its.append(mcq(f + q, fmt(key, U),
                       [fmt(x, U) for x in [cnt, v] + [k for k in (2, 5, 10) if k != key]],
                       "The %s row has %s and stands for %s. %d ÷ %d = %d, so each %s = %s. Check: %d × %d = %d."
                       % (cats[j], ones(cnt, sym), fmt(v, U), v, cnt, key, sym, fmt(key, U), cnt, key, v), rnd))
    # 3: which bar is drawn wrong?
    for i, sc in enumerate([2, 5, 10]):
        ctx = PK.next(lambda c: sc in c.keys)
        U = ctx.unit
        for _ in range(500):
            cats, vals = make_data(ctx, 4, sc, False, rnd, max_units=7, min_units=2)
            j = rnd.randrange(4)
            wrong = [vals[j] // sc, vals[j] + sc, vals[j] - sc][i]  # forgot the scale / one line too high / too low
            drawn = vals[:]
            drawn[j] = wrong
            if wrong % sc == 0 and wrong != vals[j] and wrong not in vals and 0 < wrong and math.ceil(max(drawn) / sc) <= 8 \
                    and max(drawn) >= max(vals):
                break
        else:
            raise ValueError("wrong bar")
        who = [n for n in (GIRLS + BOYS)[i * 3:] if n not in cats][0]
        f = fig(ctx_bar(ctx, cats, drawn, sc, i == 1))
        data = ", ".join("%s %d" % (c, v) for c, v in zip(cats, vals))
        q = "%s made this bar graph from the data: %s. Which bar is drawn wrong?" % (who, data)
        why = ["", "It is one line too high.", "It is one line too low."][i]
        if i == 0:
            why = "The scale counts by %d, so %d should be %s tall, not %s." % (sc, vals[j], ones(vals[j] // sc, "space"),
                                                                          ones(wrong // sc, "space"))
        its.append(mcq(f + q, cats[j], [cats[k] for k in range(4) if k != j],
                       "Check each bar against the data. The %s bar ends at %d, but the data says %d. %s"
                       % (cats[j], wrong, vals[j], why), rnd))
    # 5: word problems with a graph
    its += stories_items(rnd)
    return {"title": "Make graphs and solve word problems", "items": its}


def stories_items(rnd):
    its = []
    # cans goal
    ctx = BYTITLE["Cans Collected"]
    cats, vals = ["Room 1", "Room 2", "Room 3", "Room 4"], [40, 25, 55, 30]
    t = sum(vals)
    goal = 200
    its.append(mcq(fig(ctx_bar(ctx, cats, vals, 10, False)) +
                   "The four classes want to collect %d cans in all. How many more cans do they need?" % goal,
                   fmt(goal - t, ctx.unit), [fmt(x, ctx.unit) for x in [t, goal - t + 10, goal - (t - 25), goal - t - 10]],
                   "Step 1: cans so far: 40 + 25 + 55 + 30 = %d. Step 2: %d − %d = %d, so they need %s." % (t, goal, t, goal - t, more_fmt(goal - t, ctx.unit, "more")),
                   rnd))
    # lemonade money
    ctx = BYTITLE["Lemonade Sold"]
    cats, vals = ["Mon", "Tue", "Wed", "Thu", "Fri"], [15, 10, 20, 25, 35]
    price = 2
    s = vals[3] + vals[4]
    its.append(mcq(fig(ctx_bar(ctx, cats, vals, 5, True)) +
                   "Each cup of lemonade costs $%d. How much money did the stand make on Thursday and Friday together?" % price,
                   "$%d" % (s * price), ["$%d" % x for x in [s, vals[4] * price, vals[3] * price, (s + 5) * price]],
                   "Step 1: cups on Thursday and Friday: %d + %d = %d. Step 2: each cup is $%d, so %d × %d = $%d."
                   % (vals[3], vals[4], s, price, s, price, s * price), rnd))
    # books goal (picture graph with halves)
    ctx = BYTITLE["Books Read in March"]
    cats, vals = ["Maya", "Leo", "Ava", "Noah"], [9, 12, 7, 14]
    its.append(mcq(fig(ctx_pic(ctx, cats, vals, 2, "star")) +
                   "Ava wants to read 20 books in March. How many more books does she need to read?",
                   fmt(20 - 7, ctx.unit), [fmt(x, ctx.unit) for x in [20 - 4, 20 - 6, 20 - 8, 7]],
                   "Step 1: %s Step 2: 20 − 7 = 13 more books. (Counting 4 stars as 4 books gives 16, which is wrong.)"
                   % read_pic("Ava", 7, 2, "star", ctx.unit), rnd))
    # weather: recess outside
    ctx = BYTITLE["Weather in April"]
    cats, vals = ["Sunny", "Cloudy", "Rainy", "Windy"], [12, 7, 8, 3]
    its.append(mcq(fig(ctx_bar(ctx, cats, vals, 2, False)) +
                   "The graph shows all 30 days of April. The class had recess outside on every day that was not rainy. "
                   "On how many days did the class have recess outside?",
                   fmt(22, ctx.unit), [fmt(x, ctx.unit) for x in [8, 19, 18, 12]],
                   "Step 1: the Rainy bar ends at the line for 8, so 8 days were rainy. Step 2: 30 − 8 = 22 days. Check: 12 + 7 + 3 = 22.", rnd))
    # trees: plant more
    ctx = BYTITLE["Trees in the Park"]
    cats, vals = ["Oak", "Maple", "Pine", "Birch"], [35, 50, 20, 15]
    its.append(mcq(fig(ctx_bar(ctx, cats, vals, 10, True)) +
                   "The park plants 25 more pine trees. Then how many more pine trees than oak trees will the park have?",
                   fmt(10, ctx.unit), [fmt(x, ctx.unit) for x in [15, 45, 80, 5]],
                   "Step 1: pine trees after planting: 20 + 25 = 45. Step 2: compare with oak: 45 − 35 = 10 more pine trees.",
                   rnd))
    return its


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


L_FRUIT = (["Apple", "Banana", "Grape", "Orange"], [8, 5, 10, 3])
L_PETS = (["Dog", "Cat", "Fish", "Bird"], [35, 20, 15, 25])


def body_html():
    fr = BYTITLE["Favorite Fruit"]
    sp = BYTITLE["Pets We Have"]
    return (
        "<h2>What a scaled graph is</h2>"
        "<p>A graph shows data so you can compare it at a glance. In a <b>scaled</b> graph, one picture or one grid space "
        "can stand for <b>more than 1</b>. The key or the scale tells you how much.</p>"
        "<h2>Read a picture graph</h2>"
        "<p>Look at the <b>key</b> first. Then count the pictures in a row and multiply by the key. "
        "Half a picture stands for half of the key.</p>"
        "<figure class='sn-fig'>" + ctx_pic(fr, L_FRUIT[0], L_FRUIT[1], 2, "circle") +
        "<figcaption>Each circle = 2 votes. Banana has 2 circles and half a circle: 2 × 2 = 4, plus 1 = 5 votes.</figcaption></figure>" +
        ex("Example", "How many votes did Grape get?", "Grape has 5 circles. 5 × 2 = 10.", "10 votes") +
        "<h2>Read a bar graph</h2>"
        "<p>Find what the <b>scale</b> counts by: 2, 5, 10 or another number. Follow the top of the bar across to the scale. "
        "If a bar ends halfway between two lines, the value is halfway between the two numbers.</p>"
        "<figure class='sn-fig'>" + bar_svg("Pets We Have", "Pet", "Students", L_PETS[0], [12, 7, 4, 9], 2, False,
                                            label="bar graph: pets we have") +
        "<figcaption>The scale counts by 2. The Cat bar ends halfway between 6 and 8, so it shows 7 students.</figcaption></figure>"
        "<h2>How many more? How many fewer?</h2>"
        "<p>Read both bars, then <b>subtract</b> the smaller number from the bigger number.</p>" +
        ex("Example", "Using the pet graph: how many more students have a dog than a bird?",
           "Dog: 12. Bird: 9. 12 − 9 = 3.", "3 more students") +
        "<h2>Two-step questions</h2>"
        "<p>Some questions need two steps. Do the first step (often adding two bars), then answer the real question.</p>" +
        ex("Example", "How many more students have a dog or a cat than a bird?",
           "Step 1: 12 + 7 = 19. Step 2: 19 − 9 = 10.", "10 more students") +
        "<h2>Draw your own scaled graph</h2>"
        "<p>Pick a scale that fits your biggest number. Then divide each number by the scale.</p>" +
        table(["Data", "Picture graph (each star = 5)", "Bar graph (scale of 5)"], [
            ["Dog 35", "7 stars", "bar ends at 35 (7 spaces)"],
            ["Cat 20", "4 stars", "bar ends at 20 (4 spaces)"],
            ["Fish 15", "3 stars", "bar ends at 15 (3 spaces)"],
            ["Bird 25", "5 stars", "bar ends at 25 (5 spaces)"],
        ]) +
        "<p>Always give your graph a title, label both axes, and write the key or the scale.</p>"
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Counting pictures instead of using the key (5 circles = 5)", "Multiply by the key: 5 × 2 = 10"],
            ["Skipping a half picture", "Half a picture is half of the key"],
            ["Counting grid spaces as 1 each", "Check what the scale counts by"],
            ["Adding when the question says how many more", "How many more or fewer means subtract"],
            ["Answering after one step", "Read the question again: is there a second step?"],
        ])
    )


FAQ = [
    {"q": "What is a scaled picture graph?",
     "a": "It is a picture graph where each picture stands for more than one thing, such as each star = 5 votes. The key tells the value, so 4 stars mean 4 × 5 = 20 votes."},
    {"q": "How do you read a scaled bar graph in 3rd grade?",
     "a": "First find what the scale counts by, such as 2, 5 or 10. Then follow the top of the bar across to the number on the scale. A bar that ends halfway between 10 and 20 shows 15."},
    {"q": "How do you solve how many more and how many fewer questions with a bar graph?",
     "a": "Read the two bars, then subtract the smaller number from the bigger number. If Soccer has 25 votes and Tennis has 10, Soccer has 25 − 10 = 15 more votes."},
    {"q": "What does half a picture mean on a picture graph?",
     "a": "Half a picture stands for half of the key. If each circle = 10 students, half a circle = 5 students, so 3 and a half circles = 35 students."},
]


def gen_graphs():
    rnd = random.Random(40)
    PK = Picker(rnd)
    sets = [set_picture(rnd, PK), set_bar(rnd, PK), set_compare(rnd, PK), set_two_step(rnd, PK), set_make(rnd, PK)]
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            k = it["q"] + "|" + "|".join(sorted(it["c"]))
            assert k not in seen, it["q"]
            seen.add(k)
    return {
        "country": "us", "subject": "math", "grade": "grade-3", "slug": "picture-and-bar-graphs", "sort": 10,
        "updated": UPDATED, "pdf_url": "",
        "title": "Picture Graphs and Bar Graphs",
        "seo_title": "Grade 3 Picture Graphs and Bar Graphs Worksheets: Scaled Graphs, How Many More and Two-Step Questions",
        "short_title": "Picture and bar graphs",
        "domain": "Measurement and Data",
        "standard_code": "3.MD.B.3",
        "standard_url": "https://www.thecorestandards.org/Math/Content/3/MD/B/3/",
        "standard_text": "Draw a scaled picture graph and a scaled bar graph to represent a data set with several categories. Solve one- and two-step “how many more” and “how many less” problems using information presented in scaled bar graphs.",
        "meta_desc": "Free Grade 3 picture graph and bar graph worksheets: read scaled graphs with a key, half pictures and bars between grid lines, solve how many more and how many fewer questions, two-step problems, and draw your own graphs. 100 practice questions with answers.",
        "key_big": "Check the key or the scale first. Then read the graph.",
        "key_sub": "Each picture or grid space can stand for 2, 5, 10 or more. Multiply the pictures by the key, and read bars against the scale. How many more or fewer means subtract.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


def mark_large(u, pattern):
    """Tag pictures that must print larger (graphs, rulers, A-D choices) so their labels stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


if __name__ == "__main__":
    u = gen_graphs()
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as f:
        mark_large(u, "(picture graph|bar graph)")
        json.dump(u, f, ensure_ascii=False, indent=1)
    print("wrote", path)
