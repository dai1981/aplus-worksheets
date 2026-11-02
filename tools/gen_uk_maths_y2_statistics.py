# -*- coding: utf-8 -*-
"""
UK Year 2 Maths: Pictograms, tally charts, block diagrams and tables (National Curriculum in England: Year 2 Statistics)
  python3 tools/gen_uk_maths_y2_statistics.py
Tally charts (groups of five with the line across), pictograms where 1 symbol = 1, then 2, 5 or 10
(half symbols only when 1 symbol = 2), block diagrams (one block for each item), simple tables,
sorting categories by quantity, and "how many more / fewer / altogether" questions. Numbers up to 100.
Wrong answers come from real pupil mistakes: counting a group of 5 as 4 or 6, counting symbols instead of
using the key, half a symbol = 2 or left out, reading the wrong row or column, adding instead of subtracting.
HTML attributes use single quotes (no backslashes in the JSON). British English.
"""
import json, re, math, os, random

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "uk", "maths", "year-2")
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
    """4 choices: correct + 3 unique distractors from real mistakes (no zero or negative numbers)."""
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        c = str(c)
        lead = c.split(" ")[0]
        if c in seen or not c or lead.startswith("-") or lead.startswith("−") or lead == "0":
            continue
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    return {"q": q, "c": pick + [correct], "a": 3, "e": e}


def mcq_fixed(q, choices, ai, e):
    """Choices keep their order (A, B, C, D). The answer position is not moved later."""
    assert len(set(choices)) == 4 and 0 <= ai < 4
    return {"q": q, "c": list(choices), "a": ai, "e": e, "_fix": True}


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


def count_in(step, n):
    return ", ".join(str(step * t) for t in range(1, n + 1))


def plus(vals):
    return " + ".join(str(v) for v in vals)


# ------------------------------------------------------------ pictogram symbols
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
    if kind == "heart":
        assert not half
        return ("<path d='M%.1f %.1f C%.1f %.1f %.1f %.1f %.1f %.1f C%.1f %.1f %.1f %.1f %.1f %.1f Z' fill='%s'/>"
                % (cx, cy + 8, cx - 12, cy - 1, cx - 6, cy - 11, cx, cy - 4,
                   cx + 6, cy - 11, cx + 12, cy - 1, cx, cy + 8, RED))
    pts = star_pts(cx, cy)
    if half:
        pts = [pts[0], pts[9], pts[8], pts[7], pts[6], pts[5]]
    return "<polygon points='%s' fill='%s'/>" % (" ".join("%.1f,%.1f" % p for p in pts), col)


SYMS = ["circle", "star", "square", "heart"]
HALF_SYMS = ["circle", "star", "square"]


# ------------------------------------------------------------ contexts
class Ctx:
    def __init__(self, title, axis, cats, unit, ask, more, fewer, both, total, most, least, ph=None,
                 keys=(1, 2), big_title=None, sumto=None, hi=None, cunits=False):
        self.title, self.axis, self.cats, self.unit = title, axis, cats, unit
        self.ask_f, self.more_f, self.fewer_f, self.both_f, self.total = ask, more, fewer, both, total
        self.most, self.least = most, least
        self.ph, self.keys, self.big_title, self.sumto, self.hi = ph or {}, keys, big_title, sumto, hi
        self.cunits = {}
        if cunits:
            self.cunits = {c: (c.lower(), self.ph[c]) for c in cats}

    def p(self, c):
        return self.ph.get(c, c)

    def ask(self, c):
        return self.ask_f.format(a=self.p(c))

    def more(self, a, b):
        return self.more_f.format(a=self.p(a), b=self.p(b))

    def fewer(self, a, b):
        return self.fewer_f.format(a=self.p(a), b=self.p(b))

    def both(self, a, b):
        return self.both_f.format(a=self.p(a), b=self.p(b))

    def cu(self, c):
        """Unit for one category (woodlice, robins), or the general unit."""
        return self.cunits.get(c, self.unit)

    def ttl(self, key):
        return self.big_title if key >= 5 and self.big_title else self.title


CHILD = ("child", "children")
LOWER = lambda cs: {c: c.lower() for c in cs}
FRUIT_PL = {"Apple": "apples", "Banana": "bananas", "Grapes": "grapes", "Orange": "oranges", "Pear": "pears"}

CTXS = [
    Ctx("Favourite fruit", "Fruit", ["Apple", "Banana", "Grapes", "Orange", "Pear"], CHILD,
        "How many children chose {a}?", "How many more children chose {a} than {b}?",
        "How many fewer children chose {a} than {b}?", "How many children chose {a} or {b}?",
        "How many children voted altogether?", "Which fruit is the most popular?", "Which fruit is the least popular?",
        ph=FRUIT_PL, keys=(1, 2, 5, 10), big_title="Favourite fruit in our school"),
    Ctx("Our pets", "Pet", ["Dog", "Cat", "Fish", "Rabbit", "Hamster"], CHILD,
        "How many children have a {a}?", "How many more children have a {a} than a {b}?",
        "How many fewer children have a {a} than a {b}?", "How many children have a {a} or a {b}?",
        "How many children are shown altogether?", "Which pet do the most children have?",
        "Which pet do the fewest children have?", ph=LOWER(["Dog", "Cat", "Fish", "Rabbit", "Hamster"]), keys=(1, 2)),
    Ctx("Minibeasts we found", "Minibeast", ["Ladybird", "Worm", "Snail", "Spider", "Woodlouse"], ("minibeast", "minibeasts"),
        "How many {a} were found?", "How many more {a} than {b} were found?",
        "How many fewer {a} than {b} were found?", "How many {a} and {b} were found altogether?",
        "How many minibeasts were found altogether?", "Which minibeast did they find the most of?",
        "Which minibeast did they find the fewest of?",
        ph={"Ladybird": "ladybirds", "Worm": "worms", "Snail": "snails", "Spider": "spiders", "Woodlouse": "woodlice"},
        keys=(1, 2), cunits=True),
    Ctx("Favourite colour", "Colour", ["Red", "Blue", "Green", "Yellow", "Purple"], CHILD,
        "How many children chose {a}?", "How many more children chose {a} than {b}?",
        "How many fewer children chose {a} than {b}?", "How many children chose {a} or {b}?",
        "How many children voted altogether?", "Which colour is the most popular?", "Which colour is the least popular?",
        ph=LOWER(["Red", "Blue", "Green", "Yellow", "Purple"]), keys=(1, 2, 5, 10), big_title="Favourite colour in our school"),
    Ctx("How we come to school", "Way", ["Walk", "Car", "Bus", "Bike", "Scooter"], CHILD,
        "How many children {a}?", "How many more children {a} than {b}?",
        "How many fewer children {a} than {b}?", "How many children {a} or {b}?",
        "How many children are shown altogether?", "Which way do the most children come to school?",
        "Which way do the fewest children come to school?",
        ph={"Walk": "walk to school", "Car": "come by car", "Bus": "come by bus", "Bike": "come by bike",
            "Scooter": "come by scooter"}, keys=(1, 2, 5, 10), big_title="How children come to our school"),
    Ctx("Favourite playtime game", "Game", ["Tag", "Skipping", "Football", "Hopscotch"], CHILD,
        "How many children chose {a}?", "How many more children chose {a} than {b}?",
        "How many fewer children chose {a} than {b}?", "How many children chose {a} or {b}?",
        "How many children voted altogether?", "Which game is the most popular?", "Which game is the least popular?",
        ph=LOWER(["Tag", "Skipping", "Football", "Hopscotch"]), keys=(1, 2, 5, 10), big_title="Favourite game in our school"),
    Ctx("Birds in the garden", "Bird", ["Robin", "Sparrow", "Blackbird", "Pigeon", "Blue tit"], ("bird", "birds"),
        "How many {a} were seen?", "How many more {a} than {b} were seen?",
        "How many fewer {a} than {b} were seen?", "How many {a} and {b} were seen altogether?",
        "How many birds were seen altogether?", "Which bird was seen the most?", "Which bird was seen the least?",
        ph={"Robin": "robins", "Sparrow": "sparrows", "Blackbird": "blackbirds", "Pigeon": "pigeons", "Blue tit": "blue tits"},
        keys=(1, 2), cunits=True),
    Ctx("Favourite ice cream", "Flavour", ["Vanilla", "Strawberry", "Chocolate", "Mint"], CHILD,
        "How many children chose {a}?", "How many more children chose {a} than {b}?",
        "How many fewer children chose {a} than {b}?", "How many children chose {a} or {b}?",
        "How many children voted altogether?", "Which flavour is the most popular?", "Which flavour is the least popular?",
        ph=LOWER(["Vanilla", "Strawberry", "Chocolate", "Mint"]), keys=(1, 2, 5, 10),
        big_title="Favourite ice cream in our school"),
    Ctx("Cars going past the school", "Colour", ["Red", "Blue", "Black", "White", "Silver"], ("car", "cars"),
        "How many {a} cars went past?", "How many more {a} cars than {b} cars went past?",
        "How many fewer {a} cars than {b} cars went past?", "How many {a} and {b} cars went past altogether?",
        "How many cars went past altogether?", "Which colour of car went past the most?",
        "Which colour of car went past the least?",
        ph=LOWER(["Red", "Blue", "Black", "White", "Silver"]), keys=(1, 2)),
    Ctx("Weather in March", "Weather", ["Sunny", "Rainy", "Cloudy", "Windy"], ("day", "days"),
        "How many days were {a}?", "How many more {a} days than {b} days were there?",
        "How many fewer {a} days than {b} days were there?", "How many days were {a} or {b}?",
        "How many days are shown altogether?", "Which weather did March have on the most days?",
        "Which weather did March have on the fewest days?",
        ph=LOWER(["Sunny", "Rainy", "Cloudy", "Windy"]), keys=(1,), sumto=31, hi=12),
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


def make_data(ctx, n, step, half, rnd, max_units=8, min_units=1, ok=lambda v: True):
    """n unique values (whole numbers of steps, or with half=True some ending on a half step)."""
    assert not half or step == 2
    n = min(n, len(ctx.cats))
    if ctx.sumto:                                         # all the weather must add up to the days in the month
        n = len(ctx.cats)
    for _ in range(20000):
        cats = rnd.sample(ctx.cats, n) if not ctx.sumto else ctx.cats[:]
        units = []
        for i in range(n):
            u = rnd.randint(min_units, ctx.hi or max_units)
            hs = half and rnd.random() < 0.5 and u < max_units
            units.append(u + (0.5 if hs else 0))
        vals = [int(u * step) for u in units]
        if len(set(vals)) != n:
            continue
        if half and not any(u % 1 for u in units):
            continue
        if ctx.sumto and sum(vals) != ctx.sumto:
            continue
        if not ok(vals):
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
        assert hf == 0 or (key == 2 and hf == 1), (title, v, key)
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


def ctx_pic(ctx, cats, vals, key, sym):
    return pic_svg(ctx.ttl(key), cats, vals, key, sym, ctx.unit, label="pictogram: " + ctx.ttl(key).lower())


# ------------------------------------------------------------ block diagram
def block_svg(title, cats, vals, val_axis, label="block diagram", hl=None):
    """Block diagram: one square block for each item, stacked in columns. Scale on the left counts in 2s."""
    fs, b = 14, 12
    top_v = max(vals)
    top_v += top_v % 2
    slot = max(46, max(tw(c, fs) for c in cats) + 10)
    x0 = 24 + tw(top_v, fs) + 6
    y0 = 34
    ph = top_v * b
    yb = y0 + ph
    pw = slot * len(cats)
    W = max(x0 + pw + 8, tw(title, 16, True) + 16)
    s = [text(W / 2, 18, title, 16, bold=True)]
    for k in range(top_v + 1):
        y = yb - k * b
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='%s'/>"
                 % (x0, y, x0 + pw, y, GRID, "1" if k % 2 == 0 else "0.6"))
        if k % 2 == 0:
            s.append(text(x0 - 5, y + 5, k, fs, anchor="end"))
    for i, (c, v) in enumerate(zip(cats, vals)):
        cx = x0 + slot * i + slot / 2
        for k in range(v):
            s.append("<rect x='%.1f' y='%.1f' width='%d' height='%d' fill='%s' stroke='#ffffff' stroke-width='1.5'/>"
                     % (cx - b / 2 - 3, yb - (k + 1) * b, b + 6, b, BAR))
        s.append(text(cx, yb + 17, c, fs))
    s.append("<path d='M%.1f %d V%.1f H%.1f' fill='none' stroke='%s' stroke-width='2'/>" % (x0, y0 - 6, yb, x0 + pw, INK))
    mid = y0 + ph / 2
    assert tw(val_axis, fs, True) < ph + 30, (val_axis, ph)
    s.append(text(13, mid, val_axis, fs, bold=True, extra=" transform='rotate(-90 13 %.1f)'" % mid))
    H = yb + 24
    return svg_wrap(int(math.ceil(W)), int(H), "".join(s), label)


def ctx_block(ctx, cats, vals):
    return block_svg(ctx.title, cats, vals, ctx.unit[1].capitalize(), label="block diagram: " + ctx.title.lower())


# ------------------------------------------------------------ tally charts and tables
def tally_group(x, cy, ups, cross):
    s = []
    for k in range(ups):
        xx = x + k * 6
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2.2' stroke-linecap='round'/>"
                 % (xx, cy - 9, xx, cy + 9, INK))
    if cross:
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2.2' stroke-linecap='round'/>"
                 % (x - 4, cy + 7, x + (ups - 1) * 6 + 4, cy - 7, INK))
    return "".join(s)


def tally_marks(x, cy, v, ups=4, cross=True):
    """Groups of five: four upright lines and one line across (the gate).
    ups/cross let us draw real wrong tallies (five upright lines with a line across, or no line across)."""
    s = []
    per = ups + (1 if cross else 0)
    gw = ups * 6 + 16
    for g in range(v // per):
        s.append(tally_group(x, cy, ups, cross))
        x += gw
    s.append(tally_group(x, cy, v % per, False))
    return "".join(s)


def tally_width(v, ups=4, cross=True):
    per = ups + (1 if cross else 0)
    return (v // per) * (ups * 6 + 16) + (v % per) * 6


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


def ctx_tally(ctx, cats, vals):
    return tally_svg(ctx.title, ctx.axis, cats, vals, label="tally chart: " + ctx.title.lower())


def one_tally_svg(v):
    W = int(tally_width(v) + 24)
    return svg_wrap(max(W, 40), 30, tally_marks(12, 15, v), "tally marks")


TALLY_WHY = {
    "six": "the groups have five upright lines and a line across, so each group is 6",
    "plain": "the groups have no line across, so they are hard to count in 5s",
    "plus": "it has one mark too many",
    "minus": "it has one mark too few",
}


def tally_abcd_svg(rows):
    """Four tallies labelled A to D in one picture. rows = list of (kind, v)."""
    rh = 34
    ws = []
    for kind, v in rows:
        if kind == "six":
            ws.append(tally_width(v, 5, True))
        elif kind == "plain":
            ws.append(tally_width(v, 4, False))
        else:
            ws.append(tally_width(v))
    W = int(40 + max(ws) + 16)
    H = rh * 4 + 4
    s = []
    for k, (kind, v) in enumerate(rows):
        cy = 4 + rh * k + rh / 2
        s.append(text(14, cy + 6, "ABCD"[k], 17, bold=True))
        if kind == "six":
            s.append(tally_marks(40, cy, v, 5, True))
        elif kind == "plain":
            s.append(tally_marks(40, cy, v, 4, False))
        else:
            s.append(tally_marks(40, cy, v))
        if k:
            s.append("<line x1='4' y1='%.1f' x2='%d' y2='%.1f' stroke='%s' stroke-width='1'/>" % (cy - rh / 2, W - 4, cy - rh / 2, GRID))
    return svg_wrap(W, H, "".join(s), "tally marks A to D")


def table_svg(title, head, rows, label="table"):
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
            s.append(text(x + cw[k] / 2, y + 19, cell, fs, bold=hd))
            x += cw[k]
    H = top + (len(rows) + 1) * rh + 4
    return svg_wrap(W, H, "".join(s), label)


def ctx_table(ctx, cats, vals):
    head = "Children" if ctx.unit == CHILD else ctx.unit[1].capitalize()
    return table_svg(ctx.title, [ctx.axis, "Number of " + head.lower()], [[c, v] for c, v in zip(cats, vals)],
                     label="table: " + ctx.title.lower())


# ------------------------------------------------------------ reading text
def tally_text(v):
    g, r = v // 5, v % 5
    if g and r:
        return "%s of 5 and %d more. Count in 5s: %s, then %s. So it is %d." % (
            ones(g, "group"), r, count_in(5, g), ", ".join(str(g * 5 + t) for t in range(1, r + 1)), v)
    if g:
        return "%s of 5. Count in 5s: %s. So it is %d." % (ones(g, "group"), count_in(5, g), v)
    return "%d single marks, so it is %d." % (r, v)


def tally_cands(v):
    g, r = v // 5, v % 5
    return [g * 4 + r, g * 6 + r, g + r, v + 1, v - 1, v + 5]


def read_pic(c, v, key, sym, unit):
    full, hf = v // key, v % key
    if key == 1:
        return "Count the %ss in the %s row: %s." % (sym, c, fmt(v, unit))
    if hf:
        if full == 0:
            return "The %s row has half a %s: half of 2 is 1." % (c, sym)
        return ("The %s row has %s and half a %s. Count in 2s: %s, then 1 more for the half. So it is %s."
                % (c, ones(full, sym), sym, count_in(2, full), fmt(v, unit)))
    return "The %s row has %s. Count in %ds: %s. So it is %s." % (c, ones(full, sym), key, count_in(key, full), fmt(v, unit))


# ------------------------------------------------------------ set 1: tally charts
def set_tally(rnd, PK):
    its = []
    # 1-5 one tally on its own
    for v in [5, 7, 10, 13, 18]:
        its.append(mcq(fig(one_tally_svg(v)) + "What number does this tally show?", str(v), tally_cands(v),
                       "Four lines with one line across make a group of 5. " + tally_text(v)))
    def ok_tally(vs):
        return sum(1 for v in vs if v % 5 and v > 5) >= 2
    charts = []
    for t in range(6):
        ctx = PK.next(lambda c: not c.sumto)
        cats, vals = make_data(ctx, 3 if t in (0, 2) else 4, 1, False, rnd, max_units=19, min_units=2, ok=ok_tally)
        charts.append((ctx, cats, vals))
    # 6-9 read a row
    for t in range(4):
        ctx, cats, vals = charts[t]
        j = rnd.choice([k for k in range(len(vals)) if vals[k] % 5 and vals[k] > 5])
        v = vals[j]
        U = ctx.cu(cats[j])
        cands = [fmt(x, U) for x in tally_cands(v)[:3] + [vals[k] for k in range(len(vals)) if k != j] + [v + 1, v - 1]]
        its.append(mcq(fig(ctx_tally(ctx, cats, vals)) + ctx.ask(cats[j]), fmt(v, U), cands,
                       "Find the %s row. It has %s" % (cats[j], tally_text(v))))
    # 10-11 which row shows N
    for t in (4, 5):
        ctx, cats, vals = charts[t]
        j = rnd.choice([k for k in range(len(vals)) if vals[k] > 5])
        v = vals[j]
        near = sorted([k for k in range(len(vals)) if k != j], key=lambda k: abs(vals[k] - v))
        while len(near) < 3:
            near.append(None)
        cand = [cats[k] for k in near if k is not None]
        extra = [c for c in ctx.cats if c not in cats]
        its.append(mcq(fig(ctx_tally(ctx, cats, vals)) + "Which row shows %s?" % fmt(v, ctx.unit), cats[j], cand + extra,
                       "%d is %s. The %s row has %s" % (v, " + ".join(["5"] * (v // 5) + ([str(v % 5)] if v % 5 else [])),
                                                        cats[j], tally_text(v))))
    # 12-13 most / least
    for t, kind in ((1, "most"), (3, "least")):
        ctx, cats, vals = charts[t]
        j = vals.index(max(vals) if kind == "most" else min(vals))
        q = ctx.most if kind == "most" else ctx.least
        its.append(mcq(fig(ctx_tally(ctx, cats, vals)) + q, cats[j], [cats[k] for k in range(4) if k != j],
                       "Count every row: %s. The %s number is %d, for %s."
                       % (", ".join("%s %d" % (c, v) for c, v in zip(cats, vals)),
                          "biggest" if kind == "most" else "smallest", vals[j], cats[j])))
    # 14-16 which tally shows N (A to D in one picture)
    for v, pos, wrongs in [(8, 2, ["plus", "six", "minus"]), (13, 0, ["plain", "minus", "six"]),
                           (17, 3, ["six", "plus", "plain"])]:
        rows = [(w, v + 1 if w == "plus" else v - 1 if w == "minus" else v) for w in wrongs]
        rows.insert(pos, ("ok", v))
        why = ["%s: %s" % ("ABCD"[k], TALLY_WHY[w]) for k, (w, _) in enumerate(rows) if w != "ok"]
        its.append(mcq_fixed(fig(tally_abcd_svg(rows)) + "Which tally shows %d?" % v, ["A", "B", "C", "D"], pos,
                             "%s is right: %s %s." % ("ABCD"[pos], tally_text(v), "; ".join(why))))
    # 17-18 how many more / fewer
    for t, kind in ((0, "more"), (2, "fewer")):
        ctx, cats, vals = charts[t]
        order = sorted(range(len(vals)), key=lambda k: vals[k])
        hi, lo = order[-1], order[0]
        d = vals[hi] - vals[lo]
        U = ctx.cu(cats[hi] if kind == "more" else cats[lo])
        q = ctx.more(cats[hi], cats[lo]) if kind == "more" else ctx.fewer(cats[lo], cats[hi])
        its.append(mcq(fig(ctx_tally(ctx, cats, vals)) + q, fmt(d, U),
                       [fmt(x, U) for x in [vals[hi] + vals[lo], vals[hi], d + 1, d - 1, d + 5]],
                       "%s: %d. %s: %d. How many %s means find the difference: %d − %d = %d."
                       % (cats[hi], vals[hi], cats[lo], vals[lo], kind, vals[hi], vals[lo], d)))
    # 19-20 altogether
    for t in (4, 5):
        ctx, cats, vals = charts[t]
        U = ctx.unit
        tot = sum(vals)
        wrong = sum((v // 5) * 4 + v % 5 for v in vals)
        its.append(mcq(fig(ctx_tally(ctx, cats, vals)) + ctx.total, fmt(tot, U),
                       [fmt(x, U) for x in [wrong, tot - vals[-1], tot + 1, tot - 1, tot + 10]],
                       "Count every row: %s. Then add: %s = %d."
                       % (", ".join("%s %d" % (c, v) for c, v in zip(cats, vals)), plus(vals), tot)))
    assert len(its) == 20
    return {"title": "Tally charts", "items": its}


# ------------------------------------------------------------ set 2: pictograms where 1 symbol = 1
def set_pic1(rnd, PK):
    its = []
    plan = ["read", "read", "read", "read", "read", "read", "which", "which", "most", "most", "least", "least",
            "more", "fewer", "more", "both", "both", "both", "total", "total"]
    for i, kind in enumerate(plan):
        ctx = PK.next(lambda c: 1 in c.keys and not c.sumto)
        sym = SYMS[i % 4]
        n = 3 if i < 4 else 4
        cats, vals = make_data(ctx, n, 1, False, rnd, max_units=9, ok=lambda vs: max(vs) - min(vs) >= 2)
        f = fig(ctx_pic(ctx, cats, vals, 1, sym))
        U = ctx.unit
        n = len(cats)
        how = "Each %s = %s. " % (sym, fmt(1, U))
        if kind == "read":
            j = rnd.randrange(n)
            v = vals[j]
            CU = ctx.cu(cats[j])
            its.append(mcq(f + ctx.ask(cats[j]), fmt(v, CU),
                           [fmt(x, CU) for x in [vals[k] for k in range(n) if k != j] + [v + 1, v - 1, v + 2]],
                           how + read_pic(cats[j], v, 1, sym, CU)))
        elif kind == "which":
            j = rnd.randrange(n)
            v = vals[j]
            near = sorted([k for k in range(n) if k != j], key=lambda k: abs(vals[k] - v))
            its.append(mcq(f + "Which row shows %s?" % fmt(v, U), cats[j], [cats[k] for k in near],
                           how + "Look for the row with %s. That is %s." % (ones(v, sym), cats[j])))
        elif kind in ("most", "least"):
            j = vals.index(max(vals) if kind == "most" else min(vals))
            its.append(mcq(f + (ctx.most if kind == "most" else ctx.least), cats[j], [cats[k] for k in range(n) if k != j],
                           how + "The %s row has the %s %ss: %d." % (cats[j], "most" if kind == "most" else "fewest", sym, vals[j])))
        elif kind in ("more", "fewer"):
            pairs = [(a, b) for a in range(n) for b in range(n) if vals[a] - vals[b] >= 2]
            hi, lo = rnd.choice(pairs)
            d = vals[hi] - vals[lo]
            q = ctx.more(cats[hi], cats[lo]) if kind == "more" else ctx.fewer(cats[lo], cats[hi])
            CU = ctx.cu(cats[hi] if kind == "more" else cats[lo])
            its.append(mcq(f + q, fmt(d, CU), [fmt(x, CU) for x in [vals[hi] + vals[lo], vals[hi], d + 1, d - 1]],
                           how + "%s: %d. %s: %d. How many %s means find the difference: %d − %d = %d."
                           % (cats[hi], vals[hi], cats[lo], vals[lo], kind, vals[hi], vals[lo], d)))
        elif kind == "both":
            a, b = rnd.sample(range(n), 2)
            t = vals[a] + vals[b]
            its.append(mcq(f + ctx.both(cats[a], cats[b]), fmt(t, U),
                           [fmt(x, U) for x in [abs(vals[a] - vals[b]), t + 1, t - 1, max(vals[a], vals[b])]],
                           how + "%s: %d. %s: %d. Add them: %d + %d = %d."
                           % (cats[a], vals[a], cats[b], vals[b], vals[a], vals[b], t)))
        else:
            t = sum(vals)
            its.append(mcq(f + ctx.total, fmt(t, U), [fmt(x, U) for x in [t - vals[-1], t + 1, t - 1, t + 10]],
                           how + "Count every row: %s. Add them: %s = %d."
                           % (", ".join("%s %d" % (c, v) for c, v in zip(cats, vals)), plus(vals), t)))
    return {"title": "Pictograms: 1 symbol = 1", "items": its}


# ------------------------------------------------------------ set 3: pictograms where 1 symbol = 2, 5 or 10
def set_pic_key(rnd, PK):
    its = []
    plan = [("read", 2), ("read", 5), ("read", 10), ("read", 2), ("rhalf", 2), ("read", 5), ("read", 10),
            ("rhalf", 2), ("draw", 5), ("draw", 10), ("read", 10), ("rhalf", 2), ("most", 5), ("draw", 2),
            ("least", 10), ("more", 5), ("more", 10), ("both", 2), ("both", 10), ("fewer", 5)]
    draws = iter([("Each square stands for 5 children. 20 children chose tag. How many squares go in the Tag row?",
                   20, 5, "square"),
                  ("Each circle stands for 10 children. 60 children walk to school. How many circles go in the Walk row?",
                   60, 10, "circle"),
                  ("Each star stands for 2 children. 7 children chose mint. What goes in the Mint row?", 7, 2, "star")])
    for i, (kind, key) in enumerate(plan):
        if kind == "draw":
            q, v, k, sym = next(draws)
            assert k == key
            full, hf = v // key, v % key
            ans = halfs(v, key, sym)
            if hf:
                cand = [ones(v, sym), ones(full + 1, sym), ones(full, sym), ones(v * 2, sym)]
                e = ("Count in 2s: %s. That is %s, which makes %d. 1 more is half of 2, so add half a %s. "
                     "Draw %s." % (count_in(2, full), ones(full, sym), full * 2, sym, ans))
            else:
                cand = [ones(v, sym), ones(key, sym), ones(full + 1, sym), ones(full - 1, sym)]
                e = ("Count in %ds until you reach %d: %s. That is %s, so draw %s, not %d."
                     % (key, v, count_in(key, full), ones(full, "step"), ans, v))
            its.append(mcq(q, ans, cand, e))
            continue
        ctx = PK.next(lambda c: key in c.keys)
        sym = HALF_SYMS[i % 3] if key == 2 else SYMS[i % 4]
        half = kind in ("rhalf", "both") and key == 2
        n = 4
        mu = 8 if key == 2 else (7 if key == 5 else 9)
        cats, vals = make_data(ctx, n, key, half, rnd, max_units=mu,
                               ok=lambda vs: max(vs) - min(vs) >= 2 * key and min(vs) >= 2)
        f = fig(ctx_pic(ctx, cats, vals, key, sym))
        U = ctx.unit
        how = "Look at the key: each %s = %s%s. " % (sym, fmt(key, U), ", so half a %s = 1" % sym if key == 2 else "")
        if kind in ("read", "rhalf"):
            js = [k for k in range(n) if (vals[k] % key) == (1 if kind == "rhalf" else 0) and vals[k] > key]
            j = rnd.choice(js)
            v = vals[j]
            full = v // key
            if kind == "rhalf":
                cand = [full + 1, full * 2, full * 2 + 2, v + 2]        # counted symbols / left out the half / half as whole
            else:
                cand = [full, v + key, v - key, full + 1]               # counted the symbols instead of using the key
            cand += [vals[k] for k in range(n) if k != j]
            CU = ctx.cu(cats[j])
            its.append(mcq(f + ctx.ask(cats[j]), fmt(v, CU), [fmt(x, CU) for x in cand], how + read_pic(cats[j], v, key, sym, CU)))
        elif kind in ("most", "least"):
            j = vals.index(max(vals) if kind == "most" else min(vals))
            its.append(mcq(f + (ctx.most if kind == "most" else ctx.least), cats[j], [cats[k] for k in range(n) if k != j],
                           how + "The %s row has the %s %ss: %s. Count in %ds: %s. So it is %s."
                           % (cats[j], "most" if kind == "most" else "fewest", sym, ones(vals[j] // key, sym), key,
                              count_in(key, vals[j] // key), fmt(vals[j], U))))
        elif kind in ("more", "fewer"):
            pairs = [(a, b) for a in range(n) for b in range(n) if vals[a] - vals[b] >= 2 * key]
            hi, lo = rnd.choice(pairs)
            d = vals[hi] - vals[lo]
            q = ctx.more(cats[hi], cats[lo]) if kind == "more" else ctx.fewer(cats[lo], cats[hi])
            CU = ctx.cu(cats[hi] if kind == "more" else cats[lo])
            its.append(mcq(f + q, fmt(d, CU),
                           [fmt(x, CU) for x in [d // key, vals[hi] + vals[lo], d + key, d - key, vals[hi]]],
                           how + "%s: %s = %d. %s: %s = %d. How many %s means subtract: %d − %d = %d."
                           % (cats[hi], ones(vals[hi] // key, sym), vals[hi], cats[lo], ones(vals[lo] // key, sym), vals[lo],
                              kind, vals[hi], vals[lo], d)))
        else:
            if half:
                hs = [k for k in range(n) if vals[k] % 2]
                a = hs[0]
                b = rnd.choice([k for k in range(n) if k != a])
            else:
                a, b = rnd.sample(range(n), 2)
            t = vals[a] + vals[b]
            nsym = [vals[a] / key, vals[b] / key]
            cand = [math.ceil(nsym[0]) + math.ceil(nsym[1]), abs(vals[a] - vals[b]), t + key, t - key]
            if half:
                cand = [t - 1, t + 1] + cand                         # left out the half / counted half as 2
            its.append(mcq(f + ctx.both(cats[a], cats[b]), fmt(t, U), [fmt(x, U) for x in cand],
                           how + "%s: %d. %s: %d. Altogether means add: %d + %d = %d."
                           % (cats[a], vals[a], cats[b], vals[b], vals[a], vals[b], t)))
    return {"title": "Pictograms: 1 symbol = 2, 5 or 10", "items": its}


# ------------------------------------------------------------ set 4: block diagrams, tables and ordering
def order_q(f, cats, vals, most_first, unit, rnd):
    """Put the categories in order. Wrong answers: the wrong way round, the order they are drawn, one pair swapped."""
    idx = sorted(range(len(vals)), key=lambda k: -vals[k] if most_first else vals[k])
    right = [cats[k] for k in idx]
    rev = right[::-1]
    drawn = cats[:]
    sw = right[:]
    sw[1], sw[2] = sw[2], sw[1]
    sw2 = right[:]
    sw2[0], sw2[1] = sw2[1], sw2[0]
    J = lambda l: ", ".join(l)
    q = "Put them in order from %s." % ("most to fewest" if most_first else "fewest to most")
    return mcq(f + q, J(right), [J(rev), J(drawn), J(sw), J(sw2)],
               "Read each one: %s. %s: %s."
               % (", ".join("%s %d" % (c, v) for c, v in zip(cats, vals)),
                  "Biggest first" if most_first else "Smallest first", ", ".join("%s (%d)" % (cats[k], vals[k]) for k in idx)))


def set_block_table(rnd):
    its = []
    PK = Picker(rnd)
    used_weather = []
    plan = ["read", "read", "read", "which", "most", "least", "more", "fewer", "order_most", "order_least",
            "tread", "tread", "tmost", "torder", "ttotal", "tmore", "two_cell", "two_row", "tleast", "torder2"]
    for i, kind in enumerate(plan):
        tab = kind.startswith("t")
        if kind.startswith("two"):
            continue
        ctx = PK.next(lambda c: 1 in c.keys and not (c.sumto and used_weather))
        if ctx.sumto:
            used_weather.append(i)
        hi_u = 12 if not tab else 19
        def ok(vs):
            if max(vs) - min(vs) < 3:
                return False
            if "order" in kind:
                s_ = sorted(vs)
                return all(s_[k + 1] - s_[k] >= 1 for k in range(len(s_) - 1)) and vs != sorted(vs) and vs != sorted(vs, reverse=True)
            return True
        cats, vals = make_data(ctx, 4, 1, False, rnd, max_units=hi_u, min_units=2, ok=ok)
        n = len(cats)
        U = ctx.unit
        if tab:
            f = fig(ctx_table(ctx, cats, vals))
            look = "Read the table. "
        else:
            f = fig(ctx_block(ctx, cats, vals))
            look = "Each block = %s. " % fmt(1, U)
        if kind in ("read", "tread"):
            j = rnd.randrange(n)
            v = vals[j]
            row = [vals[k] for k in range(n) if k != j]
            cand = [v + 1, v - 1] + row if not tab else row + [v + 1, sum(vals)]
            if tab:
                e = "Find the %s row, then read the number next to it: %s." % (cats[j], fmt(v, U))
            else:
                e = look + "Count the blocks in the %s column: %d. The top of the column is at %d on the scale." % (cats[j], v, v)
            CU = ctx.cu(cats[j])
            its.append(mcq(f + ctx.ask(cats[j]), fmt(v, CU), [fmt(x, CU) for x in cand], e.replace(fmt(v, U), fmt(v, CU))))
        elif kind == "which":
            j = rnd.randrange(n)
            v = vals[j]
            near = sorted([k for k in range(n) if k != j], key=lambda k: abs(vals[k] - v))
            its.append(mcq(f + "Which column shows %s?" % fmt(v, U), cats[j], [cats[k] for k in near],
                           look + "The %s column has %d blocks." % (cats[j], v)))
        elif kind in ("most", "least", "tmost", "tleast"):
            m = kind.endswith("most")
            j = vals.index(max(vals) if m else min(vals))
            what = "column" if not tab else "number"
            its.append(mcq(f + (ctx.most if m else ctx.least), cats[j], [cats[k] for k in range(n) if k != j],
                           look + "The %s %s is %s: %d." % ("tallest" if (m and not tab) else "shortest" if not tab else
                                                            "biggest" if m else "smallest", what, cats[j], vals[j])))
        elif kind in ("more", "fewer", "tmore"):
            pairs = [(a, b) for a in range(n) for b in range(n) if vals[a] - vals[b] >= 3]
            hi, lo = rnd.choice(pairs)
            d = vals[hi] - vals[lo]
            kd = "fewer" if kind == "fewer" else "more"
            q = ctx.more(cats[hi], cats[lo]) if kd == "more" else ctx.fewer(cats[lo], cats[hi])
            CU = ctx.cu(cats[hi] if kd == "more" else cats[lo])
            its.append(mcq(f + q, fmt(d, CU), [fmt(x, CU) for x in [vals[hi] + vals[lo], vals[hi], d + 1, d - 1]],
                           look + "%s: %d. %s: %d. How many %s means find the difference: %d − %d = %d."
                           % (cats[hi], vals[hi], cats[lo], vals[lo], kd, vals[hi], vals[lo], d)))
        elif kind == "ttotal":
            t = sum(vals)
            its.append(mcq(f + ctx.total, fmt(t, U), [fmt(x, U) for x in [t - vals[-1], t + 10, t - 10, t + 1]],
                           look + "Add all the numbers: %s = %d." % (plus(vals), t)))
        else:
            most_first = kind in ("order_most", "torder")
            it = order_q(f, cats, vals, most_first, U, rnd)
            word = {"Way": "ways of coming to school", "Weather": "types of weather"}.get(ctx.axis, ctx.axis.lower() + "s")
            it["q"] = it["q"].replace("Put them", "Put the " + word)
            its.append(it)
    # two-way table (Year 2 classes)
    a = [9, 14, 6, 11]
    b = [12, 8, 13, 7]
    rows = ["Football", "Art", "Choir", "Gardening"]
    tf = fig(table_svg("After-school clubs", ["Club", "Class 2A", "Class 2B"], [[r, x, y] for r, x, y in zip(rows, a, b)],
                       label="table: after-school clubs"))
    U = CHILD
    two_cell = mcq(tf + "How many children from Class 2B go to Choir?", fmt(13, U), [fmt(x, U) for x in [6, 7, 19, 8]],
                   "Find the Choir row, then go across to the Class 2B column: 13. (6 is the Class 2A column.)")
    two_row = mcq(tf + "How many children go to Football altogether?", fmt(21, U), [fmt(x, U) for x in [3, 23, 12, 20]],
                  "Football row: Class 2A 9, Class 2B 12. Altogether means add: 9 + 12 = 21.")
    out = []
    k = 0
    for kind in plan:
        if kind == "two_cell":
            out.append(two_cell)
        elif kind == "two_row":
            out.append(two_row)
        else:
            out.append(its[k])
            k += 1
    assert len(out) == 20
    return {"title": "Block diagrams, tables and putting in order", "items": out}


# ------------------------------------------------------------ set 5: word problems
def set_words(rnd):
    its = []
    W = BYTITLE["Weather in March"]
    wv = [12, 8, 7, 4]
    assert sum(wv) == 31
    wf = fig(ctx_block(W, W.cats, wv))
    D = ("day", "days")
    its.append(mcq(wf + "How many more sunny days than rainy days were there in March?", fmt(4, D),
                   [fmt(x, D) for x in [20, 5, 12]],
                   "Sunny: 12 blocks. Rainy: 8 blocks. How many more means subtract: 12 − 8 = 4."))
    its.append(mcq(wf + "How many days were rainy or windy?", fmt(12, D), [fmt(x, D) for x in [4, 11, 13]],
                   "Rainy: 8. Windy: 4. Or means put them together: 8 + 4 = 12."))
    its.append(mcq(wf + "March has 31 days. How many days were not sunny?", fmt(19, D), [fmt(x, D) for x in [12, 43, 21]],
                   "Sunny: 12. 31 − 12 = 19 days were not sunny. Check: 8 + 7 + 4 = 19."))
    # pets tally
    P = BYTITLE["Our pets"]
    pv = [9, 7, 4, 6]
    pf = fig(ctx_tally(P, ["Dog", "Cat", "Fish", "Rabbit"], pv))
    its.append(mcq(pf + "Each child in Class 2 has one pet. How many children are in the tally chart?", fmt(26, CHILD),
                   [fmt(x, CHILD) for x in [23, 25, 16]],
                   "Dog: 5 and 4 more = 9. Cat: 5 and 2 more = 7. Fish: 4. Rabbit: 5 and 1 more = 6. "
                   "9 + 7 + 4 + 6 = 26. (Counting each group of 5 as 4 gives 23.)"))
    its.append(mcq(pf + "How many fewer children have a fish than a cat?", fmt(3, CHILD), [fmt(x, CHILD) for x in [11, 2, 4]],
                   "Cat: 7. Fish: 4. How many fewer means subtract: 7 − 4 = 3."))
    # minibeasts pictogram key 2
    M = BYTITLE["Minibeasts we found"]
    mv = [6, 9, 4, 3]
    MB = ("minibeast", "minibeasts")
    mf = fig(ctx_pic(M, ["Ladybird", "Worm", "Snail", "Spider"], mv, 2, "circle"))
    its.append(mcq(mf + "How many worms and snails were found altogether?", fmt(13, MB), [fmt(x, MB) for x in [7, 12, 5]],
                   "Each circle = 2, so half a circle = 1. Worms: 4 and a half circles = 9. Snails: 2 circles = 4. "
                   "9 + 4 = 13. (Counting the circles gives 7.)"))
    its.append(mcq(mf + "How many more worms than spiders were found?", "6 worms", ["3 worms", "12 worms", "5 worms"],
                   "Worms: 9. Spiders: 1 and a half circles = 3. 9 − 3 = 6. (3 is the difference in circles, not minibeasts.)"))
    # fruit pictogram key 5
    F = BYTITLE["Favourite fruit"]
    fv = [20, 15, 30, 10]
    ff = fig(ctx_pic(F, ["Apple", "Banana", "Grapes", "Orange"], fv, 5, "star"))
    its.append(mcq(ff + "How many children voted altogether?", fmt(75, CHILD), [fmt(x, CHILD) for x in [15, 70, 65]],
                   "Each star = 5. Apple 4 stars = 20, banana 3 stars = 15, grapes 6 stars = 30, orange 2 stars = 10. "
                   "20 + 15 + 30 + 10 = 75. (15 is the number of stars.)"))
    its.append(mcq(ff + "How many more children chose grapes than oranges?", fmt(20, CHILD), [fmt(x, CHILD) for x in [4, 40, 15]],
                   "Grapes: 6 stars = 30. Oranges: 2 stars = 10. 30 − 10 = 20. (4 is the difference in stars.)"))
    its.append(mcq(ff + "Which two fruits together got the same number of votes as grapes?", "Apple and orange",
                   ["Apple and banana", "Banana and orange", "Apple and grapes"],
                   "Grapes got 30. Apple 20 + orange 10 = 30. Apple and banana make 35, banana and orange make 25."))
    its.append(mcq(ff + "5 more children vote for banana. How many votes has banana got now?", fmt(20, ("vote", "votes")),
                   [fmt(x, ("vote", "votes")) for x in [8, 10, 40]],
                   "Banana had 3 stars = 15. 15 + 5 = 20 votes. That is one more star. "
                   "(8 comes from adding 5 to the 3 stars.)"))
    # stickers key 10
    S = ("sticker", "stickers")
    sf = fig(pic_svg("Stickers we have", ["Oliver", "Amelia", "Harry"], [40, 60, 30], 10, "heart", S,
                     label="pictogram: stickers we have"))
    its.append(mcq(sf + "Amelia wants 100 stickers. How many more stickers does she need?", fmt(40, S),
                   [fmt(x, S) for x in [94, 60, 50]],
                   "Each heart = 10. Amelia has 6 hearts = 60. 60 + 40 = 100, so she needs 40 more. "
                   "(94 comes from 100 − 6, counting the hearts.)"))
    its.append(mcq(sf + "How many stickers do Oliver and Harry have altogether?", fmt(70, S), [fmt(x, S) for x in [7, 10, 60]],
                   "Oliver: 4 hearts = 40. Harry: 3 hearts = 30. 40 + 30 = 70. (7 is the number of hearts.)"))
    # tuck shop table
    T = ("piece", "pieces")
    tf = fig(table_svg("Fruit sold at the tuck shop", ["Fruit", "Number sold"],
                       [["Apples", 14], ["Bananas", 9], ["Pears", 6], ["Satsumas", 11]], label="table: fruit sold at the tuck shop"))
    its.append(mcq(tf + "How many pieces of fruit were sold altogether?", "40 pieces", ["29 pieces", "39 pieces", "50 pieces"],
                   "Add all the numbers: 14 + 9 + 6 + 11 = 40. (29 leaves out the satsumas.)"))
    its.append(mcq(tf + "Put the fruit in order from most sold to fewest sold.", "Apples, Satsumas, Bananas, Pears",
                   ["Pears, Bananas, Satsumas, Apples", "Apples, Bananas, Pears, Satsumas", "Apples, Bananas, Satsumas, Pears"],
                   "Apples 14, satsumas 11, bananas 9, pears 6. Biggest first: apples, satsumas, bananas, pears."))
    # birds tally
    B = BYTITLE["Birds in the garden"]
    bv = [8, 13, 6, 11]
    BD = ("bird", "birds")
    bf = fig(ctx_tally(B, ["Robin", "Sparrow", "Blackbird", "Pigeon"], bv))
    its.append(mcq(bf + "Class 2 counted birds in the garden. How many birds did they see altogether?", fmt(38, BD),
                   [fmt(x, BD) for x in [33, 27, 43]],
                   "Robin 8, sparrow 13, blackbird 6, pigeon 11. 8 + 13 + 6 + 11 = 38. "
                   "(Counting each group of 5 as 4 gives 33.)"))
    its.append(mcq(bf + "How many fewer blackbirds than pigeons did they see?", "5 blackbirds",
                   ["17 blackbirds", "4 blackbirds", "6 blackbirds"],
                   "Pigeons: 2 groups of 5 and 1 more = 11. Blackbirds: 5 and 1 more = 6. 11 − 6 = 5."))
    # travel block diagram with a missing number
    tr = BYTITLE["How we come to school"]
    its.append(mcq(fig(ctx_block(tr, ["Walk", "Car", "Bus", "Bike"], [11, 7, 4, 3])) +
                   "There are 28 children in Class 2. The rest came by scooter. How many children came by scooter?",
                   fmt(3, CHILD), [fmt(x, CHILD) for x in [25, 53, 4]],
                   "Step 1: add the columns: 11 + 7 + 4 + 3 = 25. Step 2: 28 − 25 = 3 children came by scooter. "
                   "(25 is the number shown, not the answer.)"))
    # books key 2
    BK = ("book", "books")
    kf = fig(pic_svg("Books we read this week", ["Leo", "Zara", "Kai"], [6, 3, 8], 2, "square", BK,
                     label="pictogram: books we read this week"))
    its.append(mcq(kf + "Zara reads 4 more books. How many books has she read now?", fmt(7, BK), [fmt(x, BK) for x in [6, 8, 11]],
                   "Each square = 2, so half a square = 1. Zara: 1 and a half squares = 3. 3 + 4 = 7. "
                   "(Counting half a square as 2 gives 8.)"))
    its.append(mcq(kf + "How many more books did Kai read than Zara?", fmt(5, BK), [fmt(x, BK) for x in [11, 6, 3]],
                   "Kai: 4 squares = 8. Zara: 3. 8 − 3 = 5. (Adding gives 11.)"))
    assert len(its) == 20
    return {"title": "Word problems: totals and comparisons", "items": its}


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
    pets = BYTITLE["Our pets"]
    W = BYTITLE["Weather in March"]
    return (
        "<h2>What is data?</h2>"
        "<p>Data is information we collect. We can count votes, pets or minibeasts. "
        "Then we show the numbers in a <b>tally chart</b>, a <b>pictogram</b>, a <b>block diagram</b> or a <b>table</b>.</p>"
        "<h2>Tally charts</h2>"
        "<p>Make one mark for each thing you count. The fifth mark goes <b>across</b> the other four. "
        "This makes a group of 5. Count the groups in 5s, then count on the single marks.</p>"
        "<figure class='sn-fig'>" + ctx_tally(pets, ["Dog", "Cat", "Fish"], [12, 7, 4]) +
        "<figcaption>Dog: 2 groups of 5 and 2 more. Count 5, 10, then 11, 12. So 12 children have a dog.</figcaption></figure>" +
        ex("Example", "How many children have a cat?", "1 group of 5 and 2 more: 5, then 6, 7.", "7 children") +
        "<h2>Pictograms</h2>"
        "<p>A pictogram uses pictures. Always look at the <b>key</b> first. "
        "If 1 symbol = 1, just count the symbols. If 1 symbol = 2, 5 or 10, count in 2s, 5s or 10s.</p>"
        "<figure class='sn-fig'>" + ctx_pic(fr, ["Apple", "Banana", "Grapes"], [6, 7, 4], 2, "circle") +
        "<figcaption>Each circle = 2 children, so half a circle = 1. Banana: 2, 4, 6, and 1 more = 7.</figcaption></figure>" +
        ex("Example", "Each star = 10 children. The Walk row has 4 stars. How many children walk?",
           "Count in 10s: 10, 20, 30, 40.", "40 children") +
        "<h2>Block diagrams</h2>"
        "<p>In a block diagram, each block stands for 1. The blocks sit in columns. "
        "Count the blocks, or read the number on the scale at the top of the column.</p>"
        "<figure class='sn-fig'>" + ctx_block(W, W.cats, [10, 9, 7, 5]) +
        "<figcaption>Sunny has 10 blocks, so March had 10 sunny days. The tallest column is the most.</figcaption></figure>" +
        "<h2>Tables and putting in order</h2>"
        "<p>In a table, find the right row, then read across. To put things in order, find the biggest number first, "
        "then the next biggest, and so on.</p>" +
        table(["Fruit", "Number sold"], [["Apples", "14"], ["Bananas", "9"], ["Pears", "6"]]) +
        ex("Example", "Put the fruit in order from most to fewest.", "14 is the biggest, then 9, then 6.",
           "apples, bananas, pears") +
        "<h2>Add or subtract?</h2>" +
        table(["The question says", "Do this"], [
            ["altogether, in total, both, A or B", "Add"],
            ["how many more, how many fewer, difference", "Subtract"],
        ]) +
        ex("Example", "Dog 12, cat 7. How many more children have a dog than a cat?", "12 − 7 = 5.", "5 more children") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Counting a tally group of 5 as 4 (forgetting the line across)", "The line across is the fifth mark"],
            ["Drawing five lines and then a line across (a group of 6)", "Draw four lines, then the fifth goes across"],
            ["Counting symbols and forgetting the key", "If 1 symbol = 5, count 5, 10, 15 …"],
            ["Saying half a symbol is 2 when 1 symbol = 2", "Half of 2 is 1"],
            ["Reading the wrong row or column", "Put your finger on the label, then go across or up"],
            ["Adding when the question says how many more", "How many more means subtract"],
        ])
    )


FAQ = [
    {"q": "What statistics do children learn in Year 2?",
     "a": "In Year 2 children read and make tally charts, pictograms, block diagrams and simple tables. They answer questions about totals and compare groups, such as “How many more?”."},
    {"q": "How do you teach tally charts in Year 2?",
     "a": "Make one mark for each thing, and draw the fifth mark across the other four. Children then count the groups in 5s and count on the single marks."},
    {"q": "What is a block diagram in Year 2?",
     "a": "A block diagram is like a bar chart made of blocks. Each block stands for 1 thing, so children can count the blocks or read the scale."},
    {"q": "What does the key on a pictogram mean?",
     "a": "The key tells you what one symbol stands for, such as 1, 2, 5 or 10. If one symbol stands for 2, half a symbol stands for 1."},
]


def balance(sets, rnd):
    """Move the answers of the free questions so every position is right 5 times in each set."""
    for s in sets:
        cnt, free = [0] * 4, []
        for it in s["items"]:
            if it.pop("_fix", False):
                cnt[it["a"]] += 1
            else:
                free.append(it)
        targets = []
        for p in range(4):
            assert cnt[p] <= 5, (s["title"], cnt)
            targets += [p] * (5 - cnt[p])
        rnd.shuffle(targets)
        for it, t in zip(free, targets):
            corr = it["c"][it["a"]]
            wrong = [c for k, c in enumerate(it["c"]) if k != it["a"]]
            rnd.shuffle(wrong)
            wrong.insert(t, corr)
            it["c"] = wrong
            it["a"] = t
        final = [sum(1 for it in s["items"] if it["a"] == i) for i in range(4)]
        assert final == [5, 5, 5, 5], (s["title"], final)


def gen_unit():
    rnd = random.Random(2213)
    PK = Picker(rnd)
    sets = [set_tally(rnd, PK), set_pic1(rnd, PK), set_pic_key(rnd, PK), set_block_table(rnd), set_words(rnd)]
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
        "country": "uk", "subject": "maths", "grade": "year-2", "slug": "pictograms-and-tally-charts", "sort": 13,
        "updated": UPDATED, "pdf_url": "",
        "title": "Pictograms, Tally Charts and Block Diagrams",
        "seo_title": "Year 2 Pictograms and Tally Charts Worksheets: Block Diagrams and Tables (Free, with Answers)",
        "short_title": "Pictograms and tally charts",
        "domain": "Statistics",
        "standard_code": "Year 2: Statistics",
        "standard_url": "https://www.gov.uk/government/publications/national-curriculum-in-england-mathematics-programmes-of-study",
        "standard_text": "Interpret and construct simple pictograms, tally charts, block diagrams and simple tables; ask and answer simple questions by counting the number of objects in each category and sorting the categories by quantity; ask and answer questions about totalling and comparing categorical data.",
        "meta_desc": "Free Year 2 maths worksheets on statistics: tally charts in groups of five, pictograms where one symbol stands for 1, 2, 5 or 10, block diagrams, simple tables, putting groups in order, and “how many more?” and “how many altogether?” questions. 100 questions with an answer key, following the National Curriculum.",
        "key_big": "Count carefully, and look at the key first.",
        "key_sub": "In a tally, the fifth mark goes across, so each group is 5. If 1 symbol = 2, half a symbol = 1. Altogether means add; how many more or how many fewer means subtract.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


def mark_large(u, pattern):
    """Tag pictures that must print larger (charts, tables, A to D tallies) so their labels stay readable."""
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
        mark_large(u, "(pictogram|block diagram|tally chart|table|tally marks A)")
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
