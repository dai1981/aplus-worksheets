# -*- coding: utf-8 -*-
"""
UK Year 4 Maths: Bar charts, pictograms, tables and time graphs (National Curriculum: Year 4 Statistics)
  python3 tools/gen_uk_maths_y4_statistics.py
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, re, math, os, random

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "uk", "maths", "year-4")
UPDATED = "2026-11-02"
GREEN = "#006633"
BAR = "#2e8b57"
FILL = "#cfe6d6"
FILL2 = "#e6f2ea"
RED = "#c0392b"
INK = "#2b2b2b"
GRID = "#c9d3cc"
FONT = "Arial, Helvetica, sans-serif"


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e):
    """4 choices: correct + 3 unique distractors from real mistakes (no zero or negative numbers).
    Positions are balanced later for the whole set."""
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        c = str(c)
        lead = c.split(" ")[0].lstrip("£")
        if c in seen or not c or lead.startswith("-") or lead.startswith("−") or lead == "0":
            continue
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    return {"q": q, "c": pick + [correct], "a": 3, "e": e}


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


def halfs(v, key, sym):
    """'3 and a half stars' / 'half a star' / '4 stars'."""
    full, hf = v // key, v % key
    if not hf:
        return ones(full, sym)
    if full == 0:
        return "half a " + sym
    return "%d and a half %ss" % (full, sym)


# ------------------------------------------------------------ pictogram symbols (no clip paths: ids would clash on one page)
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
        pts = [pts[0], pts[9], pts[8], pts[7], pts[6], pts[5]]
    return "<polygon points='%s' fill='%s'/>" % (" ".join("%.1f,%.1f" % p for p in pts), col)


SYMS = ["circle", "star", "square"]


# ------------------------------------------------------------ contexts
class Ctx:
    def __init__(self, title, axis, cats, unit, ask, more, fewer, total, scales, pkeys, ph=None, ordered=False,
                 sumto=None, nota=None):
        self.title, self.axis, self.cats, self.unit = title, axis, cats, unit
        self.ask_f, self.more_f, self.fewer_f, self.total = ask, more, fewer, total
        self.scales, self.pkeys, self.ph, self.ordered, self.sumto, self.nota_f = scales, pkeys, ph or {}, ordered, sumto, nota

    def p(self, c):
        return self.ph.get(c, c)

    def ask(self, c):
        return self.ask_f.format(a=self.p(c))

    def more(self, a, b):
        return self.more_f.format(a=self.p(a), b=self.p(b))

    def fewer(self, a, b):
        return self.fewer_f.format(a=self.p(a), b=self.p(b))


VOTE = ("vote", "votes")
PUP = ("pupil", "pupils")
LOWER = lambda cs: {c: c.lower() for c in cs}

CTXS = [
    Ctx("Favourite fruit", "Fruit", ["Apple", "Banana", "Grapes", "Orange", "Pear"], VOTE,
        "How many votes did {a} get?", "How many more votes did {a} get than {b}?",
        "How many fewer votes did {a} get than {b}?", "How many votes were there altogether?", [2, 5], [2, 4]),
    Ctx("Pets in Year 4", "Pet", ["Dog", "Cat", "Fish", "Rabbit", "Hamster"], PUP,
        "How many pupils have a {a}?", "How many more pupils have a {a} than a {b}?",
        "How many fewer pupils have a {a} than a {b}?", "How many pupils are shown altogether?", [2], [2],
        ph=LOWER(["Dog", "Cat", "Fish", "Rabbit", "Hamster"])),
    Ctx("Books read this term", "Pupil", ["Amelia", "Harry", "Isla", "Arjun", "Freya", "Leo"], ("book", "books"),
        "How many books did {a} read?", "How many more books did {a} read than {b}?",
        "How many fewer books did {a} read than {b}?", "How many books did the pupils read altogether?", [2], [2, 4]),
    Ctx("How we travel to school", "Way", ["Walk", "Car", "Bus", "Bike", "Scooter"], PUP,
        "How many pupils {a} to school?", "How many more pupils {a} to school than {b}?",
        "How many fewer pupils {a} to school than {b}?", "How many pupils are in the survey altogether?", [5, 10], [4, 10],
        ph={"Walk": "walk", "Car": "come by car", "Bus": "come by bus", "Bike": "cycle", "Scooter": "come by scooter"}),
    Ctx("Favourite sport", "Sport", ["Football", "Netball", "Swimming", "Cricket", "Rugby"], PUP,
        "How many pupils chose {a}?", "How many more pupils chose {a} than {b}?",
        "How many fewer pupils chose {a} than {b}?", "How many pupils voted altogether?", [2, 5, 10], [2, 4, 10],
        ph=LOWER(["Football", "Netball", "Swimming", "Cricket", "Rugby"])),
    Ctx("Cans collected", "Class", ["4A", "4B", "4C", "4D"], ("can", "cans"),
        "How many cans did class {a} collect?", "How many more cans did class {a} collect than class {b}?",
        "How many fewer cans did class {a} collect than class {b}?", "How many cans did the classes collect altogether?",
        [5, 10], [10], ordered=True),
    Ctx("Cakes sold at the cake sale", "Day", ["Mon", "Tue", "Wed", "Thu", "Fri"], ("cake", "cakes"),
        "How many cakes were sold on {a}?", "How many more cakes were sold on {a} than on {b}?",
        "How many fewer cakes were sold on {a} than on {b}?", "How many cakes were sold altogether?", [2, 5, 10], [4, 10],
        ph={"Mon": "Monday", "Tue": "Tuesday", "Wed": "Wednesday", "Thu": "Thursday", "Fri": "Friday"}, ordered=True),
    Ctx("Birds in the garden", "Bird", ["Robin", "Blackbird", "Sparrow", "Blue tit"], ("bird", "birds"),
        "How many {a} were seen?", "How many more {a} than {b} were seen?",
        "How many fewer {a} than {b} were seen?", "How many birds were seen altogether?", [2, 5], [2, 4],
        ph={"Robin": "robins", "Blackbird": "blackbirds", "Sparrow": "sparrows", "Blue tit": "blue tits"}),
    Ctx("Favourite colour", "Colour", ["Red", "Blue", "Green", "Purple", "Yellow"], VOTE,
        "How many votes did {a} get?", "How many more votes did {a} get than {b}?",
        "How many fewer votes did {a} get than {b}?", "How many votes were there altogether?", [2, 5, 10], [2, 4, 10]),
    Ctx("Trees in the park", "Tree", ["Oak", "Ash", "Beech", "Birch"], ("tree", "trees"),
        "How many {a} trees are in the park?", "How many more {a} trees than {b} trees are in the park?",
        "How many fewer {a} trees than {b} trees are in the park?", "How many trees are in the park altogether?",
        [5, 10], [10], ph=LOWER(["Oak", "Ash", "Beech", "Birch"])),
    Ctx("Ice lollies sold", "Flavour", ["Lemon", "Orange", "Cola", "Cherry"], ("lolly", "lollies"),
        "How many {a} lollies were sold?", "How many more {a} lollies than {b} lollies were sold?",
        "How many fewer {a} lollies than {b} lollies were sold?", "How many lollies were sold altogether?", [5, 10], [4, 10],
        ph=LOWER(["Lemon", "Orange", "Cola", "Cherry"])),
    Ctx("House points", "House", ["Kestrel", "Falcon", "Hawk", "Owl"], ("point", "points"),
        "How many points did {a} House get?", "How many more points did {a} House get than {b} House?",
        "How many fewer points did {a} House get than {b} House?", "How many points did the houses get altogether?",
        [2, 5, 10], [10]),
    Ctx("Stickers collected", "Pupil", ["Ruby", "Mohammed", "Lily", "Kai", "Grace"], ("sticker", "stickers"),
        "How many stickers has {a} got?", "How many more stickers has {a} got than {b}?",
        "How many fewer stickers has {a} got than {b}?", "How many stickers have they got altogether?", [2, 5, 10], [2, 4]),
    Ctx("Favourite season", "Season", ["Spring", "Summer", "Autumn", "Winter"], VOTE,
        "How many votes did {a} get?", "How many more votes did {a} get than {b}?",
        "How many fewer votes did {a} get than {b}?", "How many votes were there altogether?", [2, 5, 10], [2, 4, 10],
        ordered=True),
    Ctx("Library books borrowed", "Topic", ["Animals", "Sport", "Space", "Mystery"], ("book", "books"),
        "How many {a} books were borrowed?", "How many more {a} books than {b} books were borrowed?",
        "How many fewer {a} books than {b} books were borrowed?", "How many books were borrowed altogether?", [5, 10], [4, 10]),
    Ctx("Shells found on the beach", "Pupil", ["Noah", "Ava", "Ethan", "Maya", "Alfie"], ("shell", "shells"),
        "How many shells did {a} find?", "How many more shells did {a} find than {b}?",
        "How many fewer shells did {a} find than {b}?", "How many shells did they find altogether?", [2, 5], [2, 4]),
    Ctx("School dinner choices", "Dinner", ["Pasta", "Curry", "Pizza", "Roast"], PUP,
        "How many pupils chose {a}?", "How many more pupils chose {a} than {b}?",
        "How many fewer pupils chose {a} than {b}?", "How many pupils chose a dinner altogether?", [2, 5, 10], [2, 4, 10],
        ph=LOWER(["Pasta", "Curry", "Pizza", "Roast"])),
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
    assert not half or step % 2 == 0
    if ctx.ordered:
        start = rnd.randint(0, len(ctx.cats) - n)
        cats = ctx.cats[start:start + n]
    else:
        cats = rnd.sample(ctx.cats, n)
    for _ in range(2000):
        units = []
        for i in range(n):
            u = rnd.randint(min_units, max_units)
            hs = half and rnd.random() < 0.5 and u < max_units
            units.append(u + (0.5 if hs else 0))
        vals = [int(u * step) for u in units]
        if len(set(vals)) != n:
            continue
        if half and not any(u % 1 for u in units):
            continue
        return cats, vals
    raise ValueError("no data for " + ctx.title)


# ------------------------------------------------------------ pictogram
def pic_svg(title, cats, vals, key, sym, unit, label="pictogram"):
    """Pictogram: one row per category, symbols worth `key` each, key line at the bottom."""
    fs, rh, gap = 15, 26, 23
    lw = max(tw(c, fs, True) for c in cats) + 22
    nsym = [math.ceil(v / key) for v in vals]
    m = max(max(nsym), 4)
    W = lw + 12 + m * gap + 14
    keytxt = "= " + fmt(key, unit)
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
        assert hf in (0, key // 2), (title, v, key)
        for j in range(full + (1 if hf else 0)):
            if j == full:                           # pale outline of the whole symbol behind a half symbol
                s.append(symbol(sym, lw + 12 + j * gap + 9, y + rh / 2, col=FILL))
            s.append(symbol(sym, lw + 12 + j * gap + 9, y + rh / 2, half=(j == full)))
    ky = top + H_tab + 22
    x = (W - kw) / 2
    s.append(text(x, ky, "Key:", fs, anchor="start", bold=True))
    x += tw("Key:", fs, True) + 16
    s.append(symbol(sym, x, ky - 5))
    s.append(text(x + 14, ky, keytxt, fs, anchor="start"))
    H = ky + 8
    return svg_wrap(W, H, "".join(s), label)


# ------------------------------------------------------------ bar chart
def bar_svg(title, cat_axis, val_axis, cats, vals, scale, horizontal=False, missing=None, label="bar chart"):
    """Bar chart with a grid line at every step of the scale.
    `missing` = index of a category drawn with no bar (a red ? shows where it goes)."""
    fs = 14
    top_v = int(math.ceil(max(vals) / scale) * scale)
    nt = top_v // scale
    assert 2 <= nt <= 9, (title, vals, scale)
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
    return bar_svg(ctx.title, ctx.axis, ctx.unit[1].capitalize(), cats, vals,
                   scale, horizontal, missing, label="bar chart: " + ctx.title.lower())


def ctx_pic(ctx, cats, vals, key, sym):
    return pic_svg(ctx.title, cats, vals, key, sym, ctx.unit, label="pictogram: " + ctx.title.lower())


# ------------------------------------------------------------ tally chart and tables
def tally_marks(x, cy, v):
    """Groups of five: four upright lines and one line across."""
    s = []
    for g in range(v // 5):
        for k in range(4):
            xx = x + k * 6
            s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2'/>" % (xx, cy - 8, xx, cy + 8, INK))
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2'/>" % (x - 3, cy + 6, x + 21, cy - 6, INK))
        x += 34
    for k in range(v % 5):
        xx = x + k * 6
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2'/>" % (xx, cy - 8, xx, cy + 8, INK))
    return "".join(s)


def tally_width(v):
    return (v // 5) * 34 + (v % 5) * 6


def tally_svg(title, head, cats, vals, label="tally chart"):
    fs, rh = 15, 28
    c1 = int(max(max(tw(c, fs) for c in cats), tw(head, fs, True)) + 20)
    c2 = int(max(max(tally_width(v) for v in vals) + 24, 90))
    top = 28
    W = int(max(4 + c1 + c2 + 4, tw(title, 16, True) + 16))
    x0 = (W - c1 - c2) / 2
    s = [text(W / 2, 19, title, 16, bold=True)]
    rows = [(head, None)] + list(zip(cats, vals))
    for r, (c, v) in enumerate(rows):
        y = top + r * rh
        hd = r == 0
        s.append("<rect x='%.1f' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.5'/>"
                 % (x0, y, c1, rh, FILL2 if hd else "#ffffff", GREEN))
        s.append("<rect x='%.1f' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.5'/>"
                 % (x0 + c1, y, c2, rh, FILL2 if hd else "#ffffff", GREEN))
        s.append(text(x0 + 10, y + 19, c, fs, anchor="start", bold=hd))
        if hd:
            s.append(text(x0 + c1 + 10, y + 19, "Tally", fs, anchor="start", bold=True))
        else:
            s.append(tally_marks(x0 + c1 + 14, y + rh / 2, v))
    H = top + len(rows) * rh + 4
    return svg_wrap(W, H, "".join(s), label)


def table_svg(title, head, rows, label="table", red="?"):
    """head = column headings; rows = lists of cells (first cell = row name)."""
    fs, rh = 15, 28
    ncol = len(head)
    cw = []
    for k in range(ncol):
        cells = [head[k]] + [str(r[k]) for r in rows]
        cw.append(int(max(tw(x, fs, True) for x in cells) + 20))
    tot = sum(cw)
    W = int(max(tot + 8, tw(title, 16, True) + 16))
    x0 = (W - tot) / 2
    top = 28
    s = [text(W / 2, 19, title, 16, bold=True)]
    for r, row in enumerate([head] + rows):
        y = top + r * rh
        x = x0
        for k, cell in enumerate(row):
            hd = r == 0 or k == 0
            s.append("<rect x='%.1f' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.5'/>"
                     % (x, y, cw[k], rh, FILL2 if hd else "#ffffff", GREEN))
            s.append(text(x + cw[k] / 2, y + 19, cell, fs, bold=hd or cell == red, col=RED if cell == red else INK))
            x += cw[k]
    H = top + (len(rows) + 1) * rh + 4
    return svg_wrap(W, H, "".join(s), label)


# ------------------------------------------------------------ time graph
def time_svg(title, xlabels, xt, yt, vals, scale, label="time graph"):
    """Points joined by straight lines. y axis starts at 0, a grid line at every step of the scale."""
    fs = 14
    top_v = int(math.ceil(max(vals) / scale) * scale)
    nt = top_v // scale
    assert 3 <= nt <= 10, (title, vals, scale)
    gy = 18 if nt <= 7 else 15
    ph = nt * gy
    slot = max(46, max(tw(c, fs) for c in xlabels) + 8)
    x0 = 22 + tw(top_v, fs) + 8
    n = len(xlabels)
    assert len(vals) == n
    pw = slot * (n - 1)
    y0 = 34
    yb = y0 + ph
    W = x0 + pw + tw(xlabels[-1], fs) / 2 + 6
    W = max(W, tw(title, 16, True) + 16)
    s = [text(W / 2, 18, title, 16, bold=True)]
    for k in range(nt + 1):
        y = yb - k * gy
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1'/>" % (x0, y, x0 + pw, y, GRID))
        s.append(text(x0 - 5, y + 5, k * scale, fs, anchor="end"))
    for i, c in enumerate(xlabels):
        x = x0 + slot * i
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1'/>" % (x, y0, x, yb, GRID))
        s.append(text(x, yb + 18, c, fs))
    s.append("<path d='M%.1f %d V%.1f H%.1f' fill='none' stroke='%s' stroke-width='2'/>" % (x0, y0 - 6, yb, x0 + pw + 4, INK))
    pts = [(x0 + slot * i, yb - v / scale * gy) for i, v in enumerate(vals)]
    s.append("<polyline points='%s' fill='none' stroke='%s' stroke-width='2.5'/>" % (" ".join("%.1f,%.1f" % p for p in pts), BAR))
    for p in pts:
        s.append("<circle cx='%.1f' cy='%.1f' r='4' fill='%s'/>" % (p[0], p[1], GREEN))
    s.append(text(x0 + pw / 2, yb + 38, xt, fs, bold=True))
    mid = y0 + ph / 2
    s.append(text(13, mid, yt, fs, bold=True, extra=" transform='rotate(-90 13 %.1f)'" % mid))
    assert tw(yt, fs, True) < ph + 30, (yt, ph)
    H = yb + 44
    return svg_wrap(int(math.ceil(W)), int(H), "".join(s), label)


class TG:
    """One time graph: labels on the x axis, values, scale and how to talk about it."""
    def __init__(self, kind, xl, vals, scale):
        self.kind, self.xl, self.vals, self.scale = kind, xl, vals, scale
        m = {
            "temp": ("Temperature in the playground", "Time", "Temperature (°C)", ("°C", "°C"), "the temperature"),
            "plant": ("Height of a sunflower", "Weeks after planting", "Height (cm)", ("cm", "cm"), "the height of the sunflower"),
            "car": ("Car journey to the seaside", "Time", "Distance (km)", ("km", "km"), "the distance travelled"),
            "tea": ("Temperature of a cup of tea", "Minutes after making it", "Temperature (°C)", ("°C", "°C"),
                    "the temperature of the tea"),
        }[kind]
        self.title, self.xt, self.yt, self.unit, self.what = m

    def svg(self):
        return time_svg(self.title, self.xl, self.xt, self.yt, self.vals, self.scale,
                        label="time graph: " + self.title.lower())

    def at(self, i):
        """How the x label is said in a sentence."""
        if self.kind == "plant":
            return "week %s" % self.xl[i]
        if self.kind == "tea":
            return "%s minutes" % self.xl[i]
        return self.xl[i]

    def v(self, x):
        return "%d %s" % (x, self.unit[0])

    def read(self, i):
        v, sc = self.vals[i], self.scale
        if v % sc:
            lo = v - v % sc
            return "At %s the point is halfway between the lines for %d and %d, so it shows %s." % (self.at(i), lo, lo + sc, self.v(v))
        return "At %s the point is on the line for %d, so it shows %s." % (self.at(i), v, self.v(v))


def clock(h, m):
    return "%02d:%02d" % (h, m)


def gen_temp(rnd):
    for _ in range(5000):
        v = [rnd.randint(5, 9)]
        for d in [rnd.randint(1, 3), rnd.randint(1, 3), rnd.randint(1, 4), rnd.randint(0, 2),
                  rnd.randint(-2, 1), rnd.randint(-3, -1)]:
            v.append(v[-1] + d)
        if max(v) <= 20 and v.count(max(v)) == 1 and any(x % 2 for x in v):
            ups = [v[i + 1] - v[i] for i in range(6)]
            if ups.count(max(ups)) == 1:
                return TG("temp", [clock(h, 0) for h in range(9, 16)], v, 2)
    raise ValueError("temp")


def gen_plant(rnd):
    for _ in range(5000):
        v = [rnd.randint(1, 3)]
        for _k in range(6):
            v.append(v[-1] + rnd.randint(1, 4))
        ups = [v[i + 1] - v[i] for i in range(6)]
        if v[-1] <= 20 and ups.count(max(ups)) == 1 and any(x % 2 for x in v):
            return TG("plant", [str(w) for w in range(7)], v, 2)
    raise ValueError("plant")


def gen_car(rnd):
    for _ in range(5000):
        ups = [rnd.choice([5, 10, 15, 20]) for _k in range(6)]
        stop = rnd.randint(1, 4)
        ups[stop] = 0
        v = [0]
        for u in ups:
            v.append(v[-1] + u)
        if 55 <= v[-1] <= 80 and any(x % 10 for x in v) and ups.count(max(ups)) == 1:
            return TG("car", [clock(10, m) if m < 60 else clock(11, 0) for m in range(0, 70, 10)], v, 10)
    raise ValueError("car")


def gen_tea(rnd):
    for _ in range(5000):
        downs = sorted([rnd.choice([5, 10, 15, 20]) for _k in range(6)], reverse=True)
        v = [rnd.choice([80, 85, 90])]
        for d in downs:
            v.append(v[-1] - d)
        if v[-1] >= 20 and len(set(v)) == 7 and any(x % 10 for x in v):
            return TG("tea", [str(m) for m in range(0, 70, 10)], v, 10)
    raise ValueError("tea")


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
    return "The %s bar ends on the line for %d." % (c, v)


def pic_read_cands(v, key, others, unit):
    full, hf = v // key, v % key
    drawn = full + (1 if hf else 0)
    c = [drawn]                                     # counted the symbols
    if hf:
        c += [full * key + 1, full * key, (full + 1) * key]   # half = 1 / ignored the half / counted it as whole
    c += [v + key, v - key] + others + [v * 2]
    return [fmt(x, unit) for x in c]


def bar_read_cands(v, scale, others, unit):
    c = []
    if v % scale:
        lo = v - v % scale
        c += [lo, lo + scale]                       # read the line below / above
    else:
        c += [v // scale]                           # counted grid spaces
    c += [v + scale, v - scale] + others + [v + 1]
    return [fmt(x, unit) for x in c]


def tally_text(v):
    g, r = v // 5, v % 5
    if g and r:
        return "%s of 5 and %d more: %d × 5 = %d, and %d + %d = %d." % (ones(g, "group"), r, g, g * 5, g * 5, r, v)
    if g:
        return "%s of 5: %d × 5 = %d." % (ones(g, "group"), g, v)
    return "%d single marks." % r


# ------------------------------------------------------------ set 1: bar charts
def set_bar(rnd, PK):
    its = []
    plan = ["step", "read", "read", "read", "read", "which", "read", "read", "most", "read",
            "read", "step", "fewest", "read", "read", "which", "read", "most", "read", "which"]
    scales = [2, 5, 10, 2, 10, 5, 2, 10, 5, 2, 10, 10, 2, 5, 2, 10, 10, 5, 2, 2]
    for i, kind in enumerate(plan):
        sc = scales[i]
        ctx = PK.next(lambda c: sc in c.scales)
        half = sc != 5 and kind in ("read", "which") and i % 3 != 1
        hor = i % 3 == 2
        n = 5 if (i % 4 == 0 and len(ctx.cats) >= 5) else 4
        cats, vals = make_data(ctx, n, sc, half, rnd, max_units=7)
        f = fig(ctx_bar(ctx, cats, vals, sc, hor))
        U = ctx.unit
        scl = "The scale goes up in %ds." % sc
        if kind == "read":
            if half:
                j = rnd.choice([k for k, v in enumerate(vals) if v % sc])
            else:
                j = rnd.randrange(n)
            c, v = cats[j], vals[j]
            others = [vals[k] for k in range(n) if k != j]
            its.append(mcq(f + ctx.ask(c), fmt(v, U), bar_read_cands(v, sc, others, U),
                           "%s %s So the answer is %s." % (scl, read_bar(c, v, sc), fmt(v, U))))
        elif kind == "step":
            its.append(mcq(f + "What does the scale on this bar chart go up in?", "%ds" % sc,
                           ["1s"] + ["%ds" % x for x in (2, 5, 10, 20) if x != sc],
                           "Read the numbers on the scale: 0, %d, %d, %d … Each line is %d more than the one before, "
                           "so the scale goes up in %ds." % (sc, 2 * sc, 3 * sc, sc, sc)))
        elif kind == "which":
            if half:
                j = rnd.choice([k for k, v in enumerate(vals) if v % sc])
            else:
                j = rnd.randrange(n)
            v = vals[j]
            near = sorted([k for k in range(n) if k != j], key=lambda k: abs(vals[k] - v))
            its.append(mcq(f + "Which bar shows %s?" % fmt(v, U), cats[j], [cats[k] for k in near],
                           "%s Find %d on the scale. %s" % (scl, v, read_bar(cats[j], v, sc))))
        else:
            j = vals.index(max(vals) if kind == "most" else min(vals))
            word = ("longest" if hor else "tallest") if kind == "most" else "shortest"
            q = "Which bar shows the %s %s?" % ("most" if kind == "most" else "fewest", U[1])
            its.append(mcq(f + q, cats[j], [cats[k] for k in range(n) if k != j],
                           "The %s bar is the %s one. %s It shows %s." % (cats[j], word, read_bar(cats[j], vals[j], sc),
                                                                          fmt(vals[j], U))))
    return {"title": "Read bar charts with scales of 2, 5 and 10", "items": its}


# ------------------------------------------------------------ set 2: pictograms
def set_pictogram(rnd, PK):
    its = []
    plan = ["read", "read", "half", "read", "most", "read", "draw", "read", "half", "which",
            "read", "draw", "read", "fewest", "read", "half", "read", "which", "draw", "read"]
    keys = [2, 4, 4, 10, 4, 2, 4, 10, 10, 4, 4, 10, 2, 10, 10, 4, 4, 2, 2, 10]
    draws = iter([("Each star stands for 4 books. Freya read 18 books. How many stars should be in her row?",
                   18, 4, "star"),
                  ("Each circle stands for 10 pupils. 45 pupils walk to school. How many circles should be in the Walk row?",
                   45, 10, "circle"),
                  ("Each square stands for 2 votes. Summer got 13 votes. How many squares should be in the Summer row?",
                   13, 2, "square")])
    for i, kind in enumerate(plan):
        key = keys[i]
        if kind == "draw":
            q, v, k, sym = next(draws)
            assert k == key
            full, hf = v // key, v % key
            ans = halfs(v, key, sym)
            cand = [ones(v, sym), ones(full, sym), ones(full + 1, sym), halfs(v - key, key, sym), ones(full + 2, sym)]
            e = ("%d ÷ %d = %d remainder %d. %d is half of %d, so draw %s and half a %s. Check: %d × %d + %d = %d."
                 % (v, key, full, hf, hf, key, ones(full, sym), sym, full, key, hf, v))
            its.append(mcq(q, ans, cand, e))
            continue
        ctx = PK.next(lambda c: key in c.pkeys)
        sym = SYMS[i % 3]
        half = kind in ("read", "half", "which") and not (kind == "read" and i % 5 == 0)
        n = 5 if i % 4 == 3 and len(ctx.cats) >= 5 else 4
        cats, vals = make_data(ctx, n, key, half, rnd, max_units=6)
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
                           "Look at the key: each %s stands for %s. %s" % (sym, fmt(key, U), read_pic(c, v, key, sym, U))))
        elif kind in ("most", "fewest"):
            j = vals.index(max(vals) if kind == "most" else min(vals))
            q = "Which row shows the %s %s?" % ("most" if kind == "most" else "fewest", U[1])
            its.append(mcq(f + q, cats[j], [cats[k] for k in range(n) if k != j],
                           "Every %s stands for the same number, so the row with the %s %ss shows the %s. %s"
                           % (sym, "most" if kind == "most" else "fewest", sym, "most" if kind == "most" else "fewest",
                              read_pic(cats[j], vals[j], key, sym, U))))
        elif kind == "half":
            its.append(mcq(f + "In this pictogram, what does half a %s stand for?" % sym, fmt(key // 2, U),
                           [fmt(1, U), fmt(key, U), fmt(key * 2, U), fmt(key // 2 + 1, U)],
                           "The key says one whole %s = %s. Half a %s is half of %d, which is %s, not 1."
                           % (sym, fmt(key, U), sym, key, fmt(key // 2, U))))
        else:
            hs = [k for k in range(n) if vals[k] % key]
            j = rnd.choice(hs)
            v = vals[j]
            cand = [cats[k] for k in range(n) if k != j and math.ceil(vals[k] / key) == v] + \
                   [cats[k] for k in range(n) if k != j]
            its.append(mcq(f + "Which row shows %s?" % fmt(v, U), cats[j], cand,
                           "%s ÷ %d = %d remainder %d, so look for %s. %s"
                           % (fmt(v, U), key, v // key, v % key, halfs(v, key, sym), read_pic(cats[j], v, key, sym, U))))
    return {"title": "Pictograms: use the key", "items": its}


# ------------------------------------------------------------ set 3: tally charts and tables
TALLY_CTX = [
    ("Favourite fruit", "Fruit", ["Apple", "Banana", "Grapes", "Pear"], VOTE, "How many votes did {a} get?"),
    ("Vehicles past the school", "Vehicle", ["Car", "Van", "Lorry", "Bus"], ("vehicle", "vehicles"),
     "How many {a} went past the school?"),
    ("Favourite sport", "Sport", ["Football", "Netball", "Swimming", "Cricket"], PUP, "How many pupils chose {a}?"),
    ("Birds in the garden", "Bird", ["Robin", "Blackbird", "Sparrow", "Magpie"], ("bird", "birds"),
     "How many {a} were seen?"),
    ("Colours of cars", "Colour", ["Black", "White", "Silver", "Red"], ("car", "cars"), "How many {a} cars were there?"),
]
PLURAL = {"Car": "cars", "Van": "vans", "Lorry": "lorries", "Bus": "buses", "Robin": "robins", "Blackbird": "blackbirds",
          "Sparrow": "sparrows", "Magpie": "magpies"}


def tally_data(rnd, cats, lo=4, hi=24):
    for _ in range(2000):
        vals = [rnd.randint(lo, hi) for _ in cats]
        if len(set(vals)) == len(vals) and sum(1 for v in vals if v % 5) >= 3:
            return vals
    raise ValueError("tally")


def tally_cands(v, others):
    g, r = v // 5, v % 5
    return [g * 4 + r, g + r, v + 1, v - 1, v + 5] + others


def two_way(rnd):
    days = ["Monday", "Tuesday", "Wednesday", "Thursday"]
    for _ in range(2000):
        a = [rnd.randint(8, 35) for _ in days]
        b = [rnd.randint(8, 35) for _ in days]
        tot = [x + y for x, y in zip(a, b)]
        if len(set(a + b)) == 8 and len(set(tot)) == 4 and all(abs(x - y) >= 3 for x, y in zip(a, b)) \
                and sum(1 for x, y in zip(a, b) if (x % 10) + (y % 10) >= 10) >= 2:
            return days, a, b
    raise ValueError("two way")


def set_tally_table(rnd):
    its = []
    # tally charts: 10 questions on 5 charts
    order = list(range(len(TALLY_CTX)))
    rnd.shuffle(order)
    tally_kinds = [("read", "read"), ("read", "which"), ("read", "total"), ("read", "diff"), ("which", "total")]
    for t, (k1, k2) in zip(order, tally_kinds):
        title, head, cats, U, ask = TALLY_CTX[t]
        vals = tally_data(rnd, cats)
        f = fig(tally_svg(title, head, cats, vals, label="tally chart: " + title.lower()))
        used = set()
        for kind in (k1, k2):
            if kind == "read":
                j = rnd.choice([k for k in range(4) if vals[k] % 5 and vals[k] >= 5 and k not in used])
                used.add(j)
                v = vals[j]
                a = PLURAL.get(cats[j], cats[j].lower() if title != "Favourite fruit" else cats[j])
                if title == "Colours of cars":
                    a = cats[j].lower()
                UU = (cats[j].lower(), PLURAL[cats[j]]) if title == "Vehicles past the school" else U
                its.append(mcq(f + ask.format(a=a), fmt(v, UU), [fmt(x, UU) for x in tally_cands(v, [vals[k] for k in range(4) if k != j])],
                               "Each group of 5 is four lines with one line across. The %s row has %s" % (cats[j], tally_text(v))))
            elif kind == "which":
                j = rnd.choice([k for k in range(4) if k not in used and vals[k] >= 5 and vals[k] % 5])
                used.add(j)
                v = vals[j]
                g, r = v // 5, v % 5
                near = sorted([k for k in range(4) if k != j], key=lambda k: abs(vals[k] - v))
                its.append(mcq(f + "Which row shows %s?" % fmt(v, U), cats[j], [cats[k] for k in near],
                               "%d = %s. Look for %s and %s. That is the %s row."
                               % (v, " + ".join(["5"] * g + ([str(r)] if r else [])), ones(g, "group") + " of 5",
                                  ones(r, "single mark") if r else "no single marks", cats[j])))
            elif kind == "total":
                tot = sum(vals)
                wrong = sum((v // 5) * 4 + v % 5 for v in vals)
                q = "How many %s are shown in the tally chart altogether?" % U[1]
                its.append(mcq(f + q, fmt(tot, U), [fmt(x, U) for x in [wrong, tot - min(vals), tot + 10, tot - 10, tot + 1]],
                               "Count each row: %s. Then add: %s = %s."
                               % (", ".join("%s %d" % (c, v) for c, v in zip(cats, vals)),
                                  " + ".join(str(v) for v in vals), fmt(tot, U))))
            else:
                hi, lo = vals.index(max(vals)), vals.index(min(vals))
                d = vals[hi] - vals[lo]
                q = "What is the difference between the biggest and the smallest number of %s?" % U[1]
                its.append(mcq(f + q, fmt(d, U), [fmt(x, U) for x in [vals[hi] + vals[lo], vals[hi], d + 1, d - 1, d + 5]],
                               "The biggest is %s (%d). The smallest is %s (%d). Difference means subtract: %d − %d = %d."
                               % (cats[hi], vals[hi], cats[lo], vals[lo], vals[hi], vals[lo], d)))
    # two-way tables: 10 questions on 3 tables
    plans = [["cell", "row", "diff", "most"], ["cell", "col", "diff"], ["cell", "row", "col"]]
    for p in plans:
        days, a, b = two_way(rnd)
        f = fig(table_svg("Library books borrowed", ["Day", "Year 3", "Year 4"],
                          [[d, x, y] for d, x, y in zip(days, a, b)], label="table: library books borrowed"))
        idx = rnd.sample(range(4), 4)
        for n_, kind in enumerate(p):
            j = idx[n_]
            d, x, y = days[j], a[j], b[j]
            if kind == "cell":
                yr, val, oth = ("Year 4", y, x) if n_ % 2 == 0 and rnd.random() < 0.5 else ("Year 3", x, y)
                col_wrong = [a[k] if yr == "Year 3" else b[k] for k in range(4) if k != j]
                its.append(mcq(f + "How many books did %s borrow on %s?" % (yr, d), fmt(val, ("book", "books")),
                               [fmt(z, ("book", "books")) for z in [oth] + col_wrong + [x + y]],
                               "Find the %s row, then go across to the %s column. The cell says %d." % (d, yr, val)))
            elif kind == "row":
                tot = x + y
                nox = (x % 10 + y % 10) % 10 + (x // 10 + y // 10) * 10     # forgot to exchange
                its.append(mcq(f + "How many books were borrowed on %s altogether?" % d, fmt(tot, ("book", "books")),
                               [fmt(z, ("book", "books")) for z in [nox, abs(x - y), tot + 10, tot - 1, tot + 1]],
                               "Add the two cells in the %s row: %d + %d = %d." % (d, x, y, tot)))
            elif kind == "diff":
                big, small = max(x, y), min(x, y)
                more_yr = "Year 3" if x > y else "Year 4"
                less_yr = "Year 4" if x > y else "Year 3"
                dd = big - small
                its.append(mcq(f + "On %s, how many more books did %s borrow than %s?" % (d, more_yr, less_yr),
                               fmt(dd, ("book", "books")),
                               [fmt(z, ("book", "books")) for z in [x + y, big, dd + 10, dd + 1, dd - 1]],
                               "How many more means find the difference: %d − %d = %d." % (big, small, dd)))
            elif kind == "col":
                yr, col = ("Year 4", b) if rnd.random() < 0.5 else ("Year 3", a)
                tot = sum(col)
                its.append(mcq(f + "How many books did %s borrow from Monday to Thursday?" % yr, fmt(tot, ("book", "books")),
                               [fmt(z, ("book", "books")) for z in [tot - col[3], sum(a) + sum(b), tot + 10, tot - 10]],
                               "Add the whole %s column: %s = %d." % (yr, " + ".join(str(z) for z in col), tot)))
            else:
                tots = [p_ + q_ for p_, q_ in zip(a, b)]
                jm = tots.index(max(tots))
                jy = b.index(max(b))
                cand = ([days[jy]] if jy != jm else []) + [days[k] for k in range(4) if k != jm]
                its.append(mcq(f + "On which day were the most books borrowed altogether?", days[jm], cand,
                               "Add each row: %s. The biggest total is %d on %s."
                               % (", ".join("%s %d" % (dd_[:3], t_) for dd_, t_ in zip(days, tots)), tots[jm], days[jm])))
    assert len(its) == 20, len(its)
    return {"title": "Tally charts and tables", "items": its}


# ------------------------------------------------------------ set 4: time graphs
def set_time(rnd):
    its = []
    graphs = {"temp": [gen_temp(rnd) for _ in range(3)], "plant": [gen_plant(rnd) for _ in range(2)],
              "car": [gen_car(rnd) for _ in range(2)], "tea": [gen_tea(rnd) for _ in range(2)]}
    plan = [("temp", 0, "read"), ("plant", 0, "read"), ("car", 0, "read"), ("tea", 0, "read"), ("temp", 1, "read"),
            ("temp", 0, "highest"), ("plant", 1, "reach"), ("temp", 2, "increase"), ("tea", 1, "decrease"),
            ("car", 1, "stop"), ("plant", 0, "increase"), ("temp", 1, "highest"), ("car", 0, "increase"),
            ("plant", 1, "most"), ("tea", 0, "decrease"), ("temp", 2, "reach"), ("temp", 1, "estimate"),
            ("plant", 0, "increase"), ("car", 1, "estimate"), ("temp", 0, "most")]
    used = {}
    for kind, gi, q in plan:
        G = graphs[kind][gi]
        f = fig(G.svg())
        V, n, sc = G.vals, len(G.vals), G.scale
        tag = (kind, gi)
        u = used.setdefault(tag, set())

        def pick(ok):
            c = [i for i in range(n) if ok(i) and i not in u]
            i = rnd.choice(c)
            u.add(i)
            return i

        if q == "read":
            i = pick(lambda i: 0 < i < n - 1 and V[i] % sc != 0 and V[i] not in (V[i - 1], V[i + 1]))
            v = V[i]
            lo = v - v % sc
            cand = [lo, lo + sc, V[i - 1], V[i + 1], v // sc if v // sc else v + 1, v + sc]
            ask = {"temp": "What was the temperature at %s?", "plant": "How tall was the sunflower in week %s?",
                   "car": "How far had the car travelled at %s?", "tea": "What was the temperature of the tea after %s minutes?"}[kind]
            its.append(mcq(f + ask % G.xl[i], G.v(v), [G.v(x) for x in cand],
                           "Go up from %s to the point, then across to the scale. The scale goes up in %ds. %s"
                           % (G.at(i), sc, G.read(i))))
        elif q == "highest":
            i = V.index(max(V))
            near = [i - 1, i + 1, V.index(min(V)), n - 1, 0]
            its.append(mcq(f + "At what time was it warmest?", G.xl[i], [G.xl[k] for k in near if 0 <= k < n],
                           "Find the highest point on the line. It is at %s, when it was %s." % (G.xl[i], G.v(V[i]))))
        elif q == "reach":
            i = pick(lambda i: i >= 2 and all(V[k] < V[i] for k in range(i)))
            if kind == "plant":
                qq = "In which week did the sunflower first reach %s?" % G.v(V[i])
                ans, cand = "Week %s" % G.xl[i], ["Week %s" % G.xl[k] for k in (i + 1, i - 1, V[i] // sc, i + 2, i - 2) if 0 <= k < n]
                cand = [c for c in cand if c != ans]
            else:
                qq = "At what time did the temperature first reach %s?" % G.v(V[i])
                ans, cand = G.xl[i], [G.xl[k] for k in (i + 1, i - 1, i + 2, i - 2) if 0 <= k < n]
            its.append(mcq(f + qq, ans, cand,
                           "Find %d on the scale and go across until you meet the line. Then go down: it is %s." % (V[i], G.at(i))))
        elif q in ("increase", "decrease"):
            for _ in range(200):
                i, j = sorted(rnd.sample(range(n), 2))
                ok_dir = (V[i] - V[j] if kind == "tea" else V[j] - V[i]) >= 2 * sc
                if j - i >= 2 and ok_dir and (i, j) not in u and i not in {p[0] for p in u if isinstance(p, tuple)}:
                    break
            u.add((i, j))
            d = abs(V[j] - V[i])
            wrong_t = V[j - 1] - V[i] if V[j - 1] != V[i] else V[j] - V[i + 1]
            cand = [V[j], V[i] + V[j], abs(wrong_t), d + sc, d - sc, d + 1]
            if kind == "temp":
                qq = "How much warmer was it at %s than at %s?" % (G.xl[j], G.xl[i])
            elif kind == "plant":
                qq = "How much did the sunflower grow from week %s to week %s?" % (G.xl[i], G.xl[j])
            elif kind == "car":
                qq = "How far did the car travel between %s and %s?" % (G.xl[i], G.xl[j])
            else:
                qq = "By how much did the tea cool down between %s and %s minutes?" % (G.xl[i], G.xl[j])
                cand = [V[i], V[i] + V[j], abs(wrong_t), d + sc, d - sc, d + 1]
            big, small = max(V[i], V[j]), min(V[i], V[j])
            its.append(mcq(f + qq, G.v(d), [G.v(x) for x in cand],
                           "Read both points: %s at %s and %s at %s. Find the difference: %d − %d = %s."
                           % (G.v(V[i]), G.at(i), G.v(V[j]), G.at(j), big, small, G.v(d))))
        elif q == "most":
            ups = [V[k + 1] - V[k] for k in range(n - 1)]
            k = ups.index(max(ups))
            hi = V.index(max(V))
            if kind == "plant":
                lab = lambda a: "Week %s to week %s" % (G.xl[a], G.xl[a + 1])
                qq = "Between which two weeks did the sunflower grow the most?"
            else:
                lab = lambda a: "%s to %s" % (G.xl[a], G.xl[a + 1])
                qq = "Between which two times did the temperature rise the most?"
            cand_k = [hi - 1 if hi - 1 != k else hi, k - 1, k + 1, n - 2, 0] + \
                sorted(range(n - 1), key=lambda a: -ups[a])
            cand = [lab(a) for a in cand_k if 0 <= a < n - 1 and a != k]
            its.append(mcq(f + qq, lab(k), cand,
                           "Look for the steepest part of the line. From %s to %s it goes up %d − %d = %s. No other part goes up as much."
                           % (G.at(k), G.at(k + 1), V[k + 1], V[k], G.v(ups[k]))))
        elif q == "stop":
            ups = [V[k + 1] - V[k] for k in range(n - 1)]
            k = ups.index(0)
            lab = lambda a: "%s to %s" % (G.xl[a], G.xl[a + 1])
            low = sorted([a for a in range(n - 1) if a != k], key=lambda a: ups[a])
            cand = [lab(a) for a in [low[0], k - 1, k + 1] + low[1:] if 0 <= a < n - 1 and a != k]
            its.append(mcq(f + "The car stopped for a break. Between which two times was it not moving?", lab(k), cand,
                           "When the car stops, the distance does not change, so the line is flat. "
                           "From %s to %s the distance stays at %s." % (G.xl[k], G.xl[k + 1], G.v(V[k]))))
        else:                                       # estimate halfway between two points
            ks = [k for k in range(n - 1) if (V[k + 1] - V[k]) % 2 == 0 and V[k + 1] != V[k]
                  and ((V[k] + V[k + 1]) // 2) % sc != 0]
            if not ks:
                ks = [k for k in range(n - 1) if (V[k + 1] - V[k]) % 2 == 0 and V[k + 1] != V[k]]
            k = rnd.choice(ks)
            mid = (V[k] + V[k + 1]) // 2
            h, m = map(int, G.xl[k].split(":"))
            step = 60 if kind == "temp" else 10
            t = clock(h + (m + step // 2) // 60, (m + step // 2) % 60)
            noun = "temperature" if kind == "temp" else "distance the car had travelled"
            its.append(mcq(f + "Estimate the %s at %s." % (noun, t), G.v(mid),
                           [G.v(x) for x in [V[k], V[k + 1], V[k] + V[k + 1], mid + sc, mid + 1]],
                           "%s is halfway between %s and %s. The line goes from %s to %s, so halfway is about %s. "
                           "A time graph lets you read values between the points." % (t, G.xl[k], G.xl[k + 1], G.v(V[k]),
                                                                                       G.v(V[k + 1]), G.v(mid))))
    return {"title": "Time graphs", "items": its}


# ------------------------------------------------------------ set 5: word problems
def set_words():
    its = []
    B, CK, P, K, KM, D = ("book", "books"), ("cake", "cakes"), PUP, ("can", "cans"), ("km", "km"), ("day", "days")
    # 1 cans target (bar chart, scale 10)
    ctx = BYTITLE["Cans collected"]
    cats, vals = ["4A", "4B", "4C", "4D"], [40, 25, 55, 30]
    t = sum(vals)
    its.append(mcq(fig(ctx_bar(ctx, cats, vals, 10, False)) +
                   "Year 4 want to collect 200 cans for the food bank. How many more cans do they need?",
                   fmt(200 - t, K), [fmt(x, K) for x in [t, 55, 45]],
                   "Step 1: cans so far: 40 + 25 + 55 + 30 = %d. Step 2: 200 − %d = %d. (Reading the 4B bar as 20 or 30 gives a wrong total.)"
                   % (t, t, 200 - t)))
    # 2 pictogram sum with halves (key 4)
    ctx = BYTITLE["Books read this term"]
    cats, vals = ["Amelia", "Harry", "Isla", "Arjun"], [14, 20, 10, 16]
    its.append(mcq(fig(ctx_pic(ctx, cats, vals, 4, "star")) +
                   "How many books did Amelia and Isla read altogether?",
                   fmt(24, B), [fmt(x, B) for x in [6, 22, 4]],
                   "Each star = 4 books, so half a star = 2. Amelia: 3 × 4 + 2 = 14. Isla: 2 × 4 + 2 = 10. "
                   "Altogether means add: 14 + 10 = 24."))
    # 3 pictogram difference (key 10)
    ctx = BYTITLE["Cakes sold at the cake sale"]
    cats, vals = ["Mon", "Tue", "Wed", "Thu", "Fri"], [25, 40, 15, 35, 50]
    pf = fig(ctx_pic(ctx, cats, vals, 10, "circle"))
    its.append(mcq(pf + "How many more cakes were sold on Friday than on Monday?",
                   fmt(25, CK), [fmt(x, CK) for x in [75, 29, 30]],
                   "Each circle = 10 cakes, so half a circle = 5. Friday: 5 × 10 = 50. Monday: 2 × 10 + 5 = 25. "
                   "How many more means subtract: 50 − 25 = 25."))
    # 4 money from pictogram
    its.append(mcq(pf + "Each cake costs 50p. How much money did the cake sale make on Tuesday?",
                   "£20", ["£2", "£40", "£200"],
                   "Tuesday: 4 circles × 10 = 40 cakes. 2 cakes cost 50p + 50p = £1, so 40 cakes cost 40 ÷ 2 = £20."))
    # 5 table total
    tk = [["Thursday", 46, 38], ["Friday", 62, 54]]
    tf = fig(table_svg("Tickets sold for the school play", ["Day", "Adult", "Child"], tk,
                       label="table: tickets sold for the school play"))
    its.append(mcq(tf + "How many tickets were sold altogether?",
                   fmt(200, ("ticket", "tickets")), [fmt(x, ("ticket", "tickets")) for x in [108, 116, 84]],
                   "Add all four cells: 46 + 38 = 84 on Thursday and 62 + 54 = 116 on Friday. 84 + 116 = 200."))
    # 6 table money
    its.append(mcq(tf + "Adult tickets cost £5 each. How much money did the adult tickets make on Friday?",
                   "£310", ["£270", "£230", "£67"],
                   "Friday adult tickets: 62. 62 × 5 = 300 + 10 = £310. (54 is the child tickets, not the adult tickets.)"))
    # 7 tally: more than two together
    vt = [23, 7, 9, 12]
    its.append(mcq(fig(tally_svg("Vehicles past the school", "Vehicle", ["Car", "Bus", "Lorry", "Bike"], vt,
                                 label="tally chart: vehicles past the school")) +
                   "How many more cars went past than buses and lorries together?",
                   fmt(7, ("vehicle", "vehicles")), [fmt(x, ("vehicle", "vehicles")) for x in [16, 39, 14]],
                   "Cars: 4 groups of 5 and 3 more = 23. Buses and lorries together: 7 + 9 = 16. Difference: 23 − 16 = 7."))
    # 8 weather: not rainy
    ctx = Ctx("Weather in April", "Weather", ["Sunny", "Cloudy", "Rainy", "Windy"], D, "", "", "", "", [2], [])
    its.append(mcq(fig(ctx_bar(ctx, ["Sunny", "Cloudy", "Rainy", "Windy"], [12, 7, 8, 3], 2, False)) +
                   "The chart shows all 30 days of April. The class played outside at lunchtime on every day that was not rainy. "
                   "On how many days did they play outside?",
                   fmt(22, D), [fmt(x, D) for x in [8, 20, 38]],
                   "Step 1: the Rainy bar ends on the line for 8, so 8 days were rainy. Step 2: 30 − 8 = 22 days. "
                   "Check: 12 + 7 + 3 = 22."))
    # 9 car journey still to go
    car = TG("car", [clock(10, m) if m < 60 else clock(11, 0) for m in range(0, 70, 10)], [0, 15, 30, 30, 45, 65, 80], 10)
    its.append(mcq(fig(car.svg()) + "The journey to the seaside is 80 km. How much further did the car still have to go at 10:30?",
                   "50 km", ["30 km", "35 km", "110 km"],
                   "At 10:30 the point is on the line for 30, so the car had travelled 30 km. Still to go: 80 − 30 = 50 km."))
    # 10 temperature: warmest vs 09:00
    temp = TG("temp", [clock(h, 0) for h in range(9, 16)], [7, 9, 12, 15, 16, 14, 11], 2)
    its.append(mcq(fig(temp.svg()) + "How much warmer was the warmest time of the day than 09:00?",
                   "9 °C", ["16 °C", "23 °C", "7 °C"],
                   "The warmest point is 16 °C at 13:00. At 09:00 it was 7 °C. Difference: 16 − 7 = 9 °C."))
    # 11 plant: growth over 6 weeks
    plant = TG("plant", [str(w) for w in range(7)], [3, 5, 8, 11, 13, 16, 18], 2)
    its.append(mcq(fig(plant.svg()) + "Poppy planted the sunflower in week 0. How much did it grow in the 6 weeks?",
                   "15 cm", ["18 cm", "21 cm", "13 cm"],
                   "Week 0: 3 cm. Week 6: 18 cm. It grew 18 − 3 = 15 cm. 18 cm is how tall it is, not how much it grew."))
    # 12-14 which graph for continuous data
    its.append(mcq("Which data would be best shown on a time graph?",
                   "Temperature every hour", ["Favourite fruits", "Pets in Year 4", "Ways to get to school"],
                   "A time graph shows something that changes over time, like temperature. Fruits, pets and ways to school "
                   "are groups you count, so a bar chart or pictogram is better."))
    its.append(mcq("Oliver measures his bean plant every week. Which graph should he use to show how it grows?",
                   "Time graph", ["Pictogram", "Tally chart", "Venn diagram"],
                   "Height keeps changing over time, even between his measurements. A time graph joins the points so you can see it grow."))
    its.append(mcq("Which data is best shown in a bar chart, not a time graph?",
                   "Favourite sports", ["Temperature in a day", "Height of a plant", "Mass of a puppy"],
                   "Favourite sports are separate groups that you count. Temperature, height and mass change over time, "
                   "so they suit a time graph."))
    # 15 missing bar from total
    ctx = BYTITLE["Favourite sport"]
    its.append(mcq(fig(ctx_bar(ctx, ["Football", "Netball", "Swimming", "Cricket"], [9, 6, 8, 7], 2, False, missing=3)) +
                   "30 pupils voted altogether. The bar for cricket is missing. How many pupils chose cricket?",
                   fmt(7, P), [fmt(x, P) for x in [23, 8, 53]],
                   "Step 1: add the other bars: 9 + 6 + 8 = 23. Step 2: 30 − 23 = 7 pupils chose cricket. "
                   "(Football ends halfway between 8 and 10, so it is 9, not 8.)"))
    # 16 house points catch up
    ctx = BYTITLE["House points"]
    its.append(mcq(fig(ctx_bar(ctx, ["Kestrel", "Falcon", "Hawk", "Owl"], [65, 80, 45, 70], 10, True)) +
                   "How many more points does Hawk House need to catch up with Falcon House?",
                   fmt(35, ("point", "points")), [fmt(x, ("point", "points")) for x in [125, 40, 30]],
                   "Falcon: 80. Hawk: 45 (halfway between 40 and 50). 80 − 45 = 35 points."))
    # 17 tally: fruit left over
    vf = [14, 9, 6, 11]
    its.append(mcq(fig(tally_svg("Fruit at snack time", "Fruit", ["Apple", "Banana", "Pear", "Orange"], vf,
                                 label="tally chart: fruit at snack time")) +
                   "The school bought 50 pieces of fruit. The tally chart shows the fruit that pupils took. How many pieces were left?",
                   "10 pieces", ["40 pieces", "16 pieces", "90 pieces"],
                   "Pupils took 14 + 9 + 6 + 11 = 40 pieces. Left: 50 − 40 = 10 pieces. "
                   "(Counting each group of 5 as 4 gives 34 and a wrong answer of 16.)"))
    # 18 tea below 60
    tea = TG("tea", [str(m) for m in range(0, 70, 10)], [85, 70, 60, 50, 45, 40, 35], 10)
    its.append(mcq(fig(tea.svg()) + "Lily waits until her tea is below 60 °C. After how many minutes is the tea first below 60 °C?",
                   "30 minutes", ["20 minutes", "10 minutes", "60 minutes"],
                   "At 20 minutes the tea is exactly 60 °C, which is not below 60 °C. At 30 minutes it is 50 °C, so the answer is 30 minutes."))
    # 19 bar chart sum (walk or cycle)
    ctx = BYTITLE["How we travel to school"]
    its.append(mcq(fig(ctx_bar(ctx, ["Walk", "Car", "Bus", "Bike", "Scooter"], [35, 20, 15, 25, 10], 5, False)) +
                   "How many pupils walk or cycle to school?",
                   fmt(60, P), [fmt(x, P) for x in [10, 105, 12]],
                   "Walk: 35. Bike: 25. “Walk or cycle” means put them together: 35 + 25 = 60 pupils."))
    # 20 pictogram total with halves (key 2)
    ctx = BYTITLE["Birds in the garden"]
    its.append(mcq(fig(ctx_pic(ctx, ["Robin", "Blackbird", "Sparrow", "Blue tit"], [5, 8, 11, 6], 2, "square")) +
                   "How many birds were seen altogether?",
                   fmt(30, ("bird", "birds")), [fmt(x, ("bird", "birds")) for x in [15, 28, 32]],
                   "Each square = 2 birds, so half a square = 1. Robin 5, blackbird 8, sparrow 11, blue tit 6. "
                   "5 + 8 + 11 + 6 = 30 birds."))
    assert len(its) == 20
    return {"title": "Word problems: sum, difference and comparison", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


def body_html():
    fr = BYTITLE["Favourite fruit"]
    temp = TG("temp", [clock(h, 0) for h in range(9, 16)], [6, 8, 11, 14, 15, 13, 10], 2)
    return (
        "<h2>Four ways to show data</h2>"
        "<p>Data is information we collect, such as votes or temperatures. A <b>tally chart</b> helps you count. "
        "A <b>table</b> shows the numbers. A <b>bar chart</b> or <b>pictogram</b> lets you compare groups at a glance. "
        "A <b>time graph</b> shows how something changes over time.</p>"
        "<h2>Read a bar chart</h2>"
        "<p>First find what the <b>scale</b> goes up in: 2s, 5s or 10s. Then follow the top of the bar across to the scale. "
        "If a bar ends halfway between two lines, the value is halfway between the two numbers.</p>"
        "<figure class='sn-fig'>" + bar_svg("Pets in Year 4", "Pet", "Pupils", ["Dog", "Cat", "Fish", "Rabbit"],
                                            [12, 7, 4, 9], 2, False, label="bar chart: pets in year 4") +
        "<figcaption>The scale goes up in 2s. The Cat bar ends halfway between 6 and 8, so 7 pupils have a cat.</figcaption></figure>" +
        ex("Example", "How many more pupils have a dog than a rabbit?", "Dog: 12. Rabbit: 9. 12 − 9 = 3.", "3 more pupils") +
        "<h2>Read a pictogram</h2>"
        "<p>Look at the <b>key</b> first. Count the symbols in a row and multiply by the key. "
        "Half a symbol stands for <b>half of the key</b>, not 1.</p>"
        "<figure class='sn-fig'>" + ctx_pic(fr, ["Apple", "Banana", "Grapes", "Orange"], [16, 10, 20, 6], 4, "circle") +
        "<figcaption>Each circle = 4 votes, so half a circle = 2 votes. Banana: 2 × 4 + 2 = 10 votes.</figcaption></figure>" +
        ex("Example", "How many votes did Orange get?", "1 whole circle and half a circle: 4 + 2 = 6.", "6 votes") +
        "<h2>Tally charts and tables</h2>"
        "<p>In a tally chart, every fifth mark goes across the other four. Count the groups in 5s, then add the single marks.</p>"
        "<figure class='sn-fig'>" + tally_svg("Vehicles past the school", "Vehicle", ["Car", "Van", "Bus"], [17, 8, 3],
                                              label="tally chart: vehicles past the school") +
        "<figcaption>Car: 3 groups of 5 and 2 more: 15 + 2 = 17 cars.</figcaption></figure>"
        "<p>In a table, find the right row, then go across to the right column.</p>" +
        table(["Day", "Year 3", "Year 4"], [["Monday", "18", "25"], ["Tuesday", "22", "16"]]) +
        ex("Example", "How many books did Year 4 borrow on Monday?", "Monday row, Year 4 column: 25.", "25 books") +
        "<h2>Read a time graph</h2>"
        "<p>A time graph shows <b>continuous</b> data, like temperature or height, that keeps changing. "
        "The points are joined with lines because the value changes between the times too. "
        "Go up from the time to the line, then across to the scale.</p>"
        "<figure class='sn-fig'>" + temp.svg() +
        "<figcaption>At 11:00 it was 11 °C. At 13:00 it was 15 °C, the warmest time. From 09:00 to 13:00 it got 15 − 6 = 9 °C warmer.</figcaption></figure>" +
        ex("Example", "How much warmer was it at 12:00 than at 10:00?", "12:00: 14 °C. 10:00: 8 °C. 14 − 8 = 6.", "6 °C") +
        "<h2>Sum or difference?</h2>" +
        table(["The question says", "Do this"], [
            ["altogether, in total, both together, A or B", "Add (sum)"],
            ["how many more, how many fewer, difference, how much warmer", "Subtract (difference)"],
        ]) +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Reading a bar between two lines as the lower line", "Halfway between 10 and 20 is 15"],
            ["Counting symbols instead of using the key (5 circles = 5)", "Multiply by the key: 5 × 4 = 20"],
            ["Saying half a symbol = 1", "Half a symbol is half of the key"],
            ["Counting a tally group of 5 as 4", "The line across is the fifth mark"],
            ["Reading a time graph at the wrong time", "Go straight up from the time on the bottom axis"],
            ["Adding when the question asks how many more", "How many more means subtract"],
        ])
    )


FAQ = [
    {"q": "What statistics do children learn in Year 4?",
     "a": "In Year 4 pupils read and draw bar charts, pictograms, tables and time graphs. They use them to answer comparison, sum and difference questions, such as how many more or how many altogether."},
    {"q": "What is a time graph?",
     "a": "A time graph is a line graph that shows how something changes over time, such as the temperature during a day or the height of a plant each week. Time goes along the bottom and the points are joined with straight lines."},
    {"q": "What is the difference between discrete and continuous data?",
     "a": "Discrete data is counted in whole groups, such as votes or pets, and suits a bar chart or pictogram. Continuous data, such as temperature, height or distance, keeps changing and suits a time graph."},
    {"q": "How do you read half a symbol on a pictogram?",
     "a": "Half a symbol stands for half of the key. If each circle = 10 pupils, half a circle = 5 pupils, so 3 and a half circles = 35 pupils."},
]


def balance(sets, rnd):
    """Spread the correct answers evenly: 5 at each of the 4 positions in every set."""
    for s in sets:
        items = s["items"]
        targets = [i for i in range(4) for _ in range(5)]
        rnd.shuffle(targets)
        for it, t in zip(items, targets):
            corr = it["c"][it["a"]]
            wrong = [c for k, c in enumerate(it["c"]) if k != it["a"]]
            rnd.shuffle(wrong)
            wrong.insert(t, corr)
            it["c"] = wrong
            it["a"] = t
        final = [sum(1 for it in items if it["a"] == i) for i in range(4)]
        assert final == [5, 5, 5, 5], (s["title"], final)


def gen_unit():
    rnd = random.Random(4417)
    PK = Picker(rnd)
    sets = [set_bar(rnd, PK), set_pictogram(rnd, PK), set_tally_table(rnd), set_time(rnd), set_words()]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["e"], it
            assert it["q"].count("<svg") <= 1, it["q"]
            k = it["q"] + "|" + "|".join(sorted(it["c"]))
            assert k not in seen, it["q"]
            seen.add(k)
    return {
        "country": "uk", "subject": "maths", "grade": "year-4", "slug": "bar-charts-and-time-graphs", "sort": 17,
        "updated": UPDATED, "pdf_url": "",
        "title": "Bar Charts, Pictograms, Tables and Time Graphs",
        "seo_title": "Year 4 Bar Charts and Time Graphs Worksheets: Pictograms, Tally Charts and Tables (Free, with Answers)",
        "short_title": "Bar charts and time graphs",
        "domain": "Statistics",
        "standard_code": "Year 4: Statistics",
        "standard_url": "https://www.gov.uk/government/publications/national-curriculum-in-england-mathematics-programmes-of-study",
        "standard_text": "Interpret and present discrete and continuous data using appropriate graphical methods, including bar charts and time graphs; solve comparison, sum and difference problems using information presented in bar charts, pictograms, tables and other graphs.",
        "meta_desc": "Free Year 4 maths worksheets on statistics: read bar charts with scales of 2, 5 and 10, pictograms with half symbols, tally charts, tables and time graphs, then solve sum and difference problems. 100 questions with an answer key, following the National Curriculum.",
        "key_big": "Check the scale or the key first. Then read the graph.",
        "key_sub": "A bar halfway between 10 and 20 shows 15. Half a symbol is half of the key. On a time graph, go up from the time and across to the scale. Altogether means add; how many more means subtract.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


def mark_large(u, pattern):
    """Tag pictures that must print larger (charts, tables, graphs) so their labels stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


if __name__ == "__main__":
    u = gen_unit()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        mark_large(u, "(pictogram|bar chart|tally chart|table|time graph)")
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
