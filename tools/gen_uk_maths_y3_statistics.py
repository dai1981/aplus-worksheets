# -*- coding: utf-8 -*-
"""
UK Year 3 Maths: Bar charts, pictograms and tables (National Curriculum in England: Year 3 Statistics)
  python3 tools/gen_uk_maths_y3_statistics.py
Pictograms with keys of 2, 5 and 10 (half symbols only for 2 and 10), bar charts with scales of 2, 5 and 10,
tally charts and simple tables, one-step and two-step "how many more / fewer / altogether" questions,
matching a table to a chart (A to D in one picture) and word problems. No time graphs (that is Year 4).
Wrong answers come from real pupil mistakes: counting symbols instead of using the key, half a symbol = 1,
reading a bar between two lines as the lower line, counting grid spaces, adding instead of subtracting.
HTML attributes use single quotes (no backslashes in the JSON). British English.
"""
import json, re, math, os, random

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "uk", "maths", "year-3")
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
    pts = star_pts(cx, cy)
    if half:
        pts = [pts[0], pts[9], pts[8], pts[7], pts[6], pts[5]]
    return "<polygon points='%s' fill='%s'/>" % (" ".join("%.1f,%.1f" % p for p in pts), col)


SYMS = ["circle", "star", "square"]


# ------------------------------------------------------------ contexts
class Ctx:
    def __init__(self, title, axis, cats, unit, ask, more, fewer, both, total, scales, pkeys, ph=None,
                 ordered=False, two=False, target=None):
        self.title, self.axis, self.cats, self.unit = title, axis, cats, unit
        self.ask_f, self.more_f, self.fewer_f, self.both_f, self.total = ask, more, fewer, both, total
        self.scales, self.pkeys, self.ph, self.ordered, self.two, self.target = scales, pkeys, ph or {}, ordered, two, target

    def p(self, c):
        return self.ph.get(c, c)

    def ask(self, c):
        return self.ask_f.format(a=self.p(c))

    def more(self, a, b):
        return self.more_f.format(a=self.p(a), b=self.p(b))

    def fewer(self, a, b):
        return self.fewer_f.format(a=self.p(a), b=self.p(b))

    def more2(self, a, b, c):
        """How many more A than B and C together?"""
        return self.more_f.format(a=self.p(a), b="%s and %s together" % (self.p(b), self.p(c)))

    def fewer2(self, a, b, c):
        return self.fewer_f.format(a=self.p(a), b="%s and %s together" % (self.p(b), self.p(c)))

    def both(self, a, b):
        return self.both_f.format(a=self.p(a), b=self.p(b))


VOTE = ("vote", "votes")
PUP = ("pupil", "pupils")
LOWER = lambda cs: {c: c.lower() for c in cs}

CTXS = [
    Ctx("Favourite fruit", "Fruit", ["Apple", "Banana", "Grapes", "Orange", "Pear"], VOTE,
        "How many votes did {a} get?", "How many more votes did {a} get than {b}?",
        "How many fewer votes did {a} get than {b}?", "How many votes did {a} and {b} get altogether?",
        "How many votes were there altogether?", [2, 5, 10], [2, 5, 10], two=True),
    Ctx("Minibeasts in the garden", "Minibeast", ["Ladybird", "Worm", "Snail", "Spider", "Woodlouse"],
        ("minibeast", "minibeasts"),
        "How many {a} were found?", "How many more {a} were found than {b}?",
        "How many fewer {a} were found than {b}?", "How many {a} and {b} were found altogether?",
        "How many minibeasts were found altogether?", [2, 5], [2, 5], two=True,
        ph={"Ladybird": "ladybirds", "Worm": "worms", "Snail": "snails", "Spider": "spiders", "Woodlouse": "woodlice"}),
    Ctx("Books read this term", "Pupil", ["Amelia", "Harry", "Isla", "Arjun", "Freya", "Leo"], ("book", "books"),
        "How many books did {a} read?", "How many more books did {a} read than {b}?",
        "How many fewer books did {a} read than {b}?", "How many books did {a} and {b} read altogether?",
        "How many books did the pupils read altogether?", [2, 5], [2, 5], two=True,
        target="The pupils want to read {n} books altogether this term. How many more books must they read?"),
    Ctx("Pets in Year 3", "Pet", ["Dog", "Cat", "Fish", "Rabbit", "Hamster"], PUP,
        "How many pupils have a {a}?", "How many more pupils have a {a} than a {b}?",
        "How many fewer pupils have a {a} than a {b}?", "How many pupils have a {a} or a {b}?",
        "How many pupils are shown altogether?", [2], [2], ph=LOWER(["Dog", "Cat", "Fish", "Rabbit", "Hamster"])),
    Ctx("How we travel to school", "Way", ["Walk", "Car", "Bus", "Bike", "Scooter"], PUP,
        "How many pupils {a} to school?", "How many more pupils {a} to school than {b}?",
        "How many fewer pupils {a} to school than {b}?", "How many pupils {a} or {b} to school?",
        "How many pupils are in the survey altogether?", [5, 10], [5, 10],
        ph={"Walk": "walk", "Car": "come by car", "Bus": "come by bus", "Bike": "cycle", "Scooter": "come by scooter"}),
    Ctx("Favourite sport", "Sport", ["Football", "Netball", "Swimming", "Cricket", "Rugby"], PUP,
        "How many pupils chose {a}?", "How many more pupils chose {a} than {b}?",
        "How many fewer pupils chose {a} than {b}?", "How many pupils chose {a} or {b}?",
        "How many pupils voted altogether?", [2, 5, 10], [2, 5, 10], two=True,
        ph=LOWER(["Football", "Netball", "Swimming", "Cricket", "Rugby"])),
    Ctx("Cakes sold at the cake sale", "Day", ["Mon", "Tue", "Wed", "Thu", "Fri"], ("cake", "cakes"),
        "How many cakes were sold on {a}?", "How many more cakes were sold on {a} than on {b}?",
        "How many fewer cakes were sold on {a} than on {b}?", "How many cakes were sold on {a} and {b} altogether?",
        "How many cakes were sold altogether?", [2, 5, 10], [5, 10],
        ph={"Mon": "Monday", "Tue": "Tuesday", "Wed": "Wednesday", "Thu": "Thursday", "Fri": "Friday"}, ordered=True,
        two=True, target="The school wants to sell {n} cakes altogether. How many more cakes must it sell?"),
    Ctx("Birds in the garden", "Bird", ["Robin", "Blackbird", "Sparrow", "Blue tit"], ("bird", "birds"),
        "How many {a} were seen?", "How many more {a} were seen than {b}?",
        "How many fewer {a} were seen than {b}?", "How many {a} and {b} were seen altogether?",
        "How many birds were seen altogether?", [2, 5], [2, 5], two=True,
        ph={"Robin": "robins", "Blackbird": "blackbirds", "Sparrow": "sparrows", "Blue tit": "blue tits"}),
    Ctx("Favourite colour", "Colour", ["Red", "Blue", "Green", "Purple", "Yellow"], VOTE,
        "How many votes did {a} get?", "How many more votes did {a} get than {b}?",
        "How many fewer votes did {a} get than {b}?", "How many votes did {a} and {b} get altogether?",
        "How many votes were there altogether?", [2, 5, 10], [2, 5, 10], two=True),
    Ctx("House points", "House", ["Kestrel", "Falcon", "Hawk", "Owl"], ("point", "points"),
        "How many points did {a} House get?", "How many more points did {a} House get than {b} House?",
        "How many fewer points did {a} House get than {b} House?", "How many points did {a} and {b} get altogether?",
        "How many points did the houses get altogether?", [5, 10], [10]),
    Ctx("Stickers collected", "Pupil", ["Ruby", "Mohammed", "Lily", "Kai", "Grace"], ("sticker", "stickers"),
        "How many stickers has {a} got?", "How many more stickers has {a} got than {b}?",
        "How many fewer stickers has {a} got than {b}?", "How many stickers have {a} and {b} got altogether?",
        "How many stickers have they got altogether?", [2, 5], [2, 5], two=True),
    Ctx("Shells found on the beach", "Pupil", ["Noah", "Ava", "Ethan", "Maya", "Alfie"], ("shell", "shells"),
        "How many shells did {a} find?", "How many more shells did {a} find than {b}?",
        "How many fewer shells did {a} find than {b}?", "How many shells did {a} and {b} find altogether?",
        "How many shells did they find altogether?", [2, 5], [2, 5], two=True),
    Ctx("Ice lollies sold", "Flavour", ["Lemon", "Orange", "Cola", "Cherry"], ("lolly", "lollies"),
        "How many {a} lollies were sold?", "How many more {a} lollies than {b} lollies were sold?",
        "How many fewer {a} lollies than {b} lollies were sold?", "How many {a} and {b} lollies were sold altogether?",
        "How many lollies were sold altogether?", [5, 10], [5, 10], ph=LOWER(["Lemon", "Orange", "Cola", "Cherry"])),
    Ctx("Library books borrowed", "Topic", ["Animals", "Sport", "Space", "Mystery"], ("book", "books"),
        "How many {a} books were borrowed?", "How many more {a} books than {b} books were borrowed?",
        "How many fewer {a} books than {b} books were borrowed?", "How many {a} and {b} books were borrowed altogether?",
        "How many books were borrowed altogether?", [5, 10], [5, 10],
        ph={"Animals": "animal", "Sport": "sport", "Space": "space", "Mystery": "mystery"}),
    Ctx("Cans collected", "Class", ["3A", "3B", "3C", "3D"], ("can", "cans"),
        "How many cans did class {a} collect?", "How many more cans did class {a} collect than {b}?",
        "How many fewer cans did class {a} collect than {b}?", "How many cans did classes {a} and {b} collect altogether?",
        "How many cans did the classes collect altogether?", [5, 10], [10], ordered=True, two=True,
        ph={"3A": "3A", "3B": "3B", "3C": "3C", "3D": "3D"},
        target="Year 3 want to collect {n} cans altogether. How many more cans do they need?"),
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


def make_data(ctx, n, step, half, rnd, max_units=7, min_units=1, ok=lambda v: True):
    """n unique values. Each value is a whole number of steps, or (half=True) may end on a half step."""
    assert not half or step % 2 == 0
    if ctx.ordered:
        start = rnd.randint(0, len(ctx.cats) - n)
        cats = ctx.cats[start:start + n]
    else:
        cats = rnd.sample(ctx.cats, n)
    for _ in range(5000):
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
        assert hf in (0, key // 2) and (hf == 0 or key % 2 == 0), (title, v, key)
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


def ctx_bar(ctx, cats, vals, scale, horizontal=False, missing=None):
    return bar_svg(ctx.title, ctx.axis, ctx.unit[1].capitalize(), cats, vals,
                   scale, horizontal, missing, label="bar chart: " + ctx.title.lower())


def ctx_pic(ctx, cats, vals, key, sym):
    return pic_svg(ctx.title, cats, vals, key, sym, ctx.unit, label="pictogram: " + ctx.title.lower())


# ------------------------------------------------------------ A-D panels (one picture)
PW, PH = 218, 172


def mini_bar(x0, y0, cats, vals, scale, top_v):
    """A small bar chart inside a panel (no title): scale on the left, short labels below."""
    fs = 14
    nt = top_v // scale
    gy = 112.0 / nt
    ax = x0 + 38
    yb = y0 + 142
    slot = 44
    s = []
    for k in range(nt + 1):
        y = yb - k * gy
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1'/>" % (ax, y, ax + slot * len(cats), y, GRID))
        s.append(text(ax - 4, y + 5, k * scale, fs, anchor="end"))
    for i, (c, v) in enumerate(zip(cats, vals)):
        cx = ax + slot * i + slot / 2
        h = v / scale * gy
        s.append("<rect x='%.1f' y='%.1f' width='24' height='%.1f' fill='%s'/>" % (cx - 12, yb - h, h, BAR))
        s.append(text(cx, yb + 17, c, fs))
    s.append("<path d='M%.1f %.1f V%.1f H%.1f' fill='none' stroke='%s' stroke-width='2'/>" % (ax, yb - 112 - 4, yb, ax + slot * len(cats), INK))
    assert ax + slot * len(cats) <= x0 + PW - 2
    return "".join(s)


def mini_pic(x0, y0, cats, vals, key, sym):
    fs, rh, gap = 14, 25, 22
    lw = x0 + max(tw(c, fs) for c in cats) + 14
    s = []
    for i, (c, v) in enumerate(zip(cats, vals)):
        y = y0 + 28 + i * rh
        s.append(text(lw - 7, y + 17, c, fs, anchor="end"))
        full, hf = v // key, v % key
        assert hf in (0, key // 2) and (hf == 0 or key % 2 == 0)
        for j in range(full + (1 if hf else 0)):
            cx = lw + 4 + j * gap + 9
            if j == full:
                s.append(symbol(sym, cx, y + rh / 2, col=FILL))
            s.append(symbol(sym, cx, y + rh / 2, half=(j == full)))
            assert cx + 10 <= x0 + PW - 2, (cats, vals, key)
    s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1.5'/>"
             % (lw, y0 + 28, lw, y0 + 28 + rh * len(cats), GREEN))
    return "".join(s)


def panel_svg(draws, label, key_line=None):
    """2 x 2 panels labelled A to D. draws: list of functions (x0, y0) -> svg string."""
    W, H = 2 * PW, 2 * PH
    s = ["<line x1='%d' y1='4' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (PW, PW, H - 4, GRID),
         "<line x1='4' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (PH, W - 4, PH, GRID)]
    for k, d in enumerate(draws):
        x0, y0 = (k % 2) * PW, (k // 2) * PH
        s.append(d(x0, y0))
        s.append(text(x0 + 8, y0 + 20, "ABCD"[k], 18, anchor="start", bold=True))
    if key_line:
        sym, txt = key_line
        kw = tw("Key:", 15, True) + 32 + tw(txt, 15)
        x = (W - kw) / 2
        ky = H + 22
        s.append(text(x, ky, "Key:", 15, anchor="start", bold=True))
        x += tw("Key:", 15, True) + 16
        s.append(symbol(sym, x, ky - 5))
        s.append(text(x + 14, ky, txt, 15, anchor="start"))
        H += 32
    return svg_wrap(W, H, "".join(s), label)


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


# ------------------------------------------------------------ reading text (used in explanations)
def read_pic(c, v, key, sym, unit):
    full, hf = v // key, v % key
    if hf:
        if full == 0:
            return "The %s row has half a %s: half of %d is %s." % (c, sym, key, fmt(v, unit))
        return ("The %s row has %s and half a %s: %d × %d = %d, and half of %d is %d, so %d + %d = %s."
                % (c, ones(full, sym), sym, full, key, full * key, key, hf, full * key, hf, fmt(v, unit)))
    return "The %s row has %s: %d × %d = %s." % (c, ones(full, sym), full, key, fmt(v, unit))


def short_pic(v, key):
    full, hf = v // key, v % key
    if hf:
        return "%d × %d + %d = %d" % (full, key, hf, v) if full else "half of %d = %d" % (key, v)
    return "%d × %d = %d" % (full, key, v)


def read_bar(c, v, scale):
    if v % scale:
        lo = v - v % scale
        return "The %s bar ends halfway between %d and %d, so it shows %d." % (c, lo, lo + scale, v)
    return "The %s bar ends on the line for %d." % (c, v)


def pic_wrong(v, key):
    """Real misreadings of one pictogram row."""
    full, hf = v // key, v % key
    out = [full + (1 if hf else 0)]                 # counted the symbols
    if hf:
        out += [full * key + 1, full * key, (full + 1) * key]   # half = 1 / ignored the half / half counted as whole
    return out


def bar_wrong(v, scale):
    if v % scale:
        lo = v - v % scale
        return [lo, lo + scale]                     # read the line below / above
    return [v // scale]                             # counted grid spaces


def pic_read_cands(v, key, others, unit):
    c = pic_wrong(v, key) + [v + key, v - key] + others + [v * 2]
    return [fmt(x, unit) for x in c]


def bar_read_cands(v, scale, others, unit):
    c = bar_wrong(v, scale) + [v + scale, v - scale] + others + [v + 1]
    return [fmt(x, unit) for x in c]


def tally_text(v):
    g, r = v // 5, v % 5
    if g and r:
        return "%s of 5 and %d more: %d × 5 = %d, and %d + %d = %d." % (ones(g, "group"), r, g, g * 5, g * 5, r, v)
    if g:
        return "%s of 5: %d × 5 = %d." % (ones(g, "group"), g, v)
    return "%d single marks." % r


# ------------------------------------------------------------ set 1: pictograms
def set_pictogram(rnd, PK):
    its = []
    plan = ["read", "read", "read", "half", "read", "most", "draw", "read", "half", "which",
            "read", "fewest", "draw", "read", "read", "half", "which", "read", "draw", "read"]
    keys = [2, 5, 10, 10, 5, 2, 2, 2, 10, 2,
            10, 5, 10, 5, 2, 10, 10, 5, 5, 10]
    draws = iter([("Each star stands for 2 books. Freya read 9 books. How many stars should be in her row?", 9, 2, "star"),
                  ("Each circle stands for 10 pupils. 45 pupils walk to school. How many circles should be in the Walk row?",
                   45, 10, "circle"),
                  ("Each square stands for 5 votes. Red got 30 votes. How many squares should be in the Red row?",
                   30, 5, "square")])
    for i, kind in enumerate(plan):
        key = keys[i]
        if kind == "draw":
            q, v, k, sym = next(draws)
            assert k == key
            full, hf = v // key, v % key
            ans = halfs(v, key, sym)
            if hf:
                cand = [ones(v, sym), ones(full, sym), ones(full + 1, sym), halfs(v - key, key, sym), ones(full + 2, sym)]
                e = ("Count in %ds: %s. %d whole %ss make %d. %d more is half of %d, so add half a %s. "
                     "Draw %s."
                     % (key, ", ".join(str(key * t) for t in range(1, full + 1)), full, sym, full * key, hf, key, sym, ans))
            else:
                cand = [ones(v, sym), ones(full + 1, sym), ones(full - 1, sym), ones(key, sym)]
                e = ("Count in %ds until you reach %d: %s. That is %s, so draw %s. Check: %d × %d = %d."
                     % (key, v, ", ".join(str(key * t) for t in range(1, full + 1)), ones(full, "step"), ans, full, key, v))
            its.append(mcq(q, ans, cand, e))
            continue
        ctx = PK.next(lambda c: key in c.pkeys)
        sym = SYMS[i % 3]
        half = key != 5 and kind in ("read", "half", "which") and not (kind == "read" and i % 4 == 0)
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
            w = "most" if kind == "most" else "fewest"
            q = "Which row shows the %s %s?" % (w, U[1])
            its.append(mcq(f + q, cats[j], [cats[k] for k in range(n) if k != j],
                           "Every %s stands for the same number, so the row with the %s %ss shows the %s. %s"
                           % (sym, w, sym, w, read_pic(cats[j], vals[j], key, sym, U))))
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
                           "Half a %s is %d, so %s is %s. %s"
                           % (sym, key // 2, fmt(v, U), halfs(v, key, sym), read_pic(cats[j], v, key, sym, U))))
    return {"title": "Pictograms: 1 symbol = 2, 5 or 10", "items": its}


# ------------------------------------------------------------ set 2: bar charts
def set_bar(rnd, PK):
    its = []
    plan = ["step", "read", "read", "read", "read", "which", "read", "step", "most", "read",
            "read", "read", "fewest", "read", "read", "which", "read", "most", "read", "which"]
    scales = [2, 2, 5, 10, 2, 5, 10, 5, 2, 10, 5, 2, 10, 5, 2, 10, 10, 5, 2, 2]
    for i, kind in enumerate(plan):
        sc = scales[i]
        ctx = PK.next(lambda c: sc in c.scales)
        half = sc != 5 and kind in ("read", "which") and i % 3 != 1
        hor = i % 4 == 2
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
    return {"title": "Bar charts with scales of 2, 5 and 10", "items": its}


# ------------------------------------------------------------ set 3: tally charts and tables
TALLY_CTX = [
    ("Favourite fruit", "Fruit", ["Apple", "Banana", "Grapes", "Pear"], VOTE, "How many votes did {a} get?", {}),
    ("Vehicles past the school", "Vehicle", ["Car", "Van", "Lorry", "Bus"], ("vehicle", "vehicles"),
     "How many {a} went past the school?", {"Car": ("car", "cars"), "Van": ("van", "vans"), "Lorry": ("lorry", "lorries"),
                                             "Bus": ("bus", "buses")}),
    ("Favourite sport", "Sport", ["Football", "Netball", "Swimming", "Cricket"], PUP, "How many pupils chose {a}?", {}),
    ("Minibeasts in the garden", "Minibeast", ["Ladybird", "Worm", "Snail", "Spider"], ("minibeast", "minibeasts"),
     "How many {a} were found?", {"Ladybird": ("ladybird", "ladybirds"), "Worm": ("worm", "worms"),
                                  "Snail": ("snail", "snails"), "Spider": ("spider", "spiders")}),
    ("Colours of cars", "Colour", ["Black", "White", "Silver", "Red"], ("car", "cars"), "How many {a} cars were there?", {}),
]


def tally_data(rnd, cats, lo=3, hi=19):
    for _ in range(2000):
        vals = [rnd.randint(lo, hi) for _ in cats]
        if len(set(vals)) == len(vals) and sum(1 for v in vals if v % 5 and v > 5) >= 3:
            return vals
    raise ValueError("tally")


def tally_cands(v, others):
    g, r = v // 5, v % 5
    return [g * 4 + r, g + r, v + 1, v - 1, v + 5] + others


TABLES = [
    dict(title="Minibeasts found by Year 3", head=["Minibeast", "Class 3A", "Class 3B"],
         rows=["Ladybirds", "Worms", "Snails", "Spiders"], lo=3, hi=19, unit=("minibeast", "minibeasts"),
         cell="How many {r} did class {c} find?", row="How many {r} did the two classes find altogether?",
         diff="How many more {r} did class {big} find than class {small}?",
         col="How many minibeasts did class {c} find altogether?",
         most="Which minibeast did the two classes find the most of altogether?",
         rname=lambda r: r.lower(), cname=lambda c: c.replace("Class ", ""),
         runit=lambda r: (r.lower()[:-1], r.lower())),
    dict(title="Books read in two weeks", head=["Pupil", "Week 1", "Week 2"],
         rows=["Oliver", "Poppy", "Kai", "Evie"], lo=2, hi=14, unit=("book", "books"),
         cell="How many books did {r} read in {c}?", row="How many books did {r} read in the two weeks altogether?",
         diff="How many more books did {r} read in {big} than in {small}?",
         col="How many books did the four pupils read in {c}?",
         most="Who read the most books in the two weeks altogether?",
         rname=lambda r: r, cname=lambda c: c.lower(), runit=lambda r: ("book", "books")),
    dict(title="Lunches in Year 3", head=["Day", "Hot dinner", "Packed lunch"],
         rows=["Monday", "Tuesday", "Wednesday", "Thursday"], lo=8, hi=24, unit=PUP,
         cell="How many pupils had a {c} on {r}?", row="How many pupils had lunch on {r} altogether?",
         diff="On {r}, how many more pupils had a {big} than a {small}?",
         col="How many pupils had a {c} from Monday to Thursday?",
         most="On which day did the most pupils have lunch altogether?",
         rname=lambda r: r, cname=lambda c: c.lower(), runit=lambda r: PUP),
]


def two_way(rnd, lo, hi):
    for _ in range(5000):
        a = [rnd.randint(lo, hi) for _ in range(4)]
        b = [rnd.randint(lo, hi) for _ in range(4)]
        tot = [x + y for x, y in zip(a, b)]
        if len(set(a + b)) == 8 and len(set(tot)) == 4 and all(abs(x - y) >= 3 for x, y in zip(a, b)) \
                and tot.count(max(tot)) == 1 and b.index(max(b)) != tot.index(max(tot)):
            return a, b
    raise ValueError("two way")


def set_tally_table(rnd):
    its = []
    order = list(range(len(TALLY_CTX)))
    rnd.shuffle(order)
    tally_kinds = [("read", "read"), ("read", "which"), ("read", "total"), ("read", "diff"), ("which", "total")]
    for t, (k1, k2) in zip(order, tally_kinds):
        title, head, cats, U, ask, runits = TALLY_CTX[t]
        vals = tally_data(rnd, cats)
        f = fig(tally_svg(title, head, cats, vals, label="tally chart: " + title.lower()))
        used = set()
        for kind in (k1, k2):
            if kind == "read":
                j = rnd.choice([k for k in range(4) if vals[k] % 5 and vals[k] > 5 and k not in used])
                used.add(j)
                v = vals[j]
                UU = runits.get(cats[j], U)
                a = runits[cats[j]][1] if cats[j] in runits else (cats[j].lower() if title in ("Colours of cars", "Favourite sport") else cats[j])
                its.append(mcq(f + ask.format(a=a), fmt(v, UU),
                               [fmt(x, UU) for x in tally_cands(v, [vals[k] for k in range(4) if k != j])],
                               "Each group of 5 is four lines with one line across. The %s row has %s" % (cats[j], tally_text(v))))
            elif kind == "which":
                j = rnd.choice([k for k in range(4) if k not in used and vals[k] > 5 and vals[k] % 5])
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
    # simple tables: 10 questions on 3 tables
    plans = [["cell", "row", "diff", "most"], ["cell", "col", "diff"], ["cell", "row", "col"]]
    for T, p in zip(TABLES, plans):
        a, b = two_way(rnd, T["lo"], T["hi"])
        rows = T["rows"]
        h1, h2 = T["head"][1], T["head"][2]
        f = fig(table_svg(T["title"], T["head"], [[r, x, y] for r, x, y in zip(rows, a, b)],
                          label="table: " + T["title"].lower()))
        idx = rnd.sample(range(4), 4)
        U = T["unit"]
        for n_, kind in enumerate(p):
            j = idx[n_]
            r, x, y = rows[j], a[j], b[j]
            RU = T["runit"](r)
            if kind == "cell":
                ch, val, oth = (h2, y, x) if n_ == 0 and T is TABLES[1] else (h1, x, y)
                col_wrong = [(a if ch == h1 else b)[k] for k in range(4) if k != j]
                its.append(mcq(f + T["cell"].format(r=T["rname"](r), c=T["cname"](ch)), fmt(val, RU),
                               [fmt(z, RU) for z in [oth] + col_wrong + [x + y]],
                               "Find the %s row, then go across to the %s column. The cell says %d." % (r, ch, val)))
            elif kind == "row":
                tot = x + y
                its.append(mcq(f + T["row"].format(r=T["rname"](r)), fmt(tot, RU),
                               [fmt(z, RU) for z in [abs(x - y), tot + 10, tot - 1, tot + 1, max(x, y)]],
                               "Altogether means add. Add the two cells in the %s row: %d + %d = %d." % (r, x, y, tot)))
            elif kind == "diff":
                big, small = (h1, h2) if x > y else (h2, h1)
                dd = abs(x - y)
                its.append(mcq(f + T["diff"].format(r=T["rname"](r), big=T["cname"](big), small=T["cname"](small)),
                               fmt(dd, RU), [fmt(z, RU) for z in [x + y, max(x, y), dd + 1, dd - 1, dd + 10]],
                               "How many more means find the difference: %d − %d = %d." % (max(x, y), min(x, y), dd)))
            elif kind == "col":
                ch, col = (h2, b) if T is TABLES[1] else (h1, a)
                tot = sum(col)
                its.append(mcq(f + T["col"].format(c=T["cname"](ch)), fmt(tot, U),
                               [fmt(z, U) for z in [tot - col[3], sum(a) + sum(b), tot + 10, tot - 10]],
                               "Add the whole %s column: %s = %d." % (ch, " + ".join(str(z) for z in col), tot)))
            else:
                tots = [p_ + q_ for p_, q_ in zip(a, b)]
                jm = tots.index(max(tots))
                jy = b.index(max(b))
                cand = [rows[jy]] + [rows[k] for k in range(4) if k != jm]
                its.append(mcq(f + T["most"], rows[jm], cand,
                               "Add each row: %s. The biggest total is %d, for %s."
                               % (", ".join("%s %d + %d = %d" % (r_, p_, q_, p_ + q_) for r_, p_, q_ in zip(rows, a, b)),
                                  tots[jm], rows[jm].lower() if T is TABLES[0] else rows[jm])))
    assert len(its) == 20, len(its)
    return {"title": "Tally charts and tables", "items": its}


# ------------------------------------------------------------ set 4: how many more, fewer, altogether
def misread_total(vals, sc, chart):
    """Total after one typical misreading: half a symbol = 1 / a bar between lines read as the lower line;
    with no halves, counting symbols or grid spaces instead of using the key or scale."""
    if any(v % sc for v in vals):
        if chart == "pic":
            return sum(v - v % sc + (1 if v % sc else 0) for v in vals)
        return sum(v - v % sc for v in vals)
    return sum(v // sc for v in vals)


def set_compare(rnd, PK):
    its = []
    plan = [("more", "bar", 2), ("alt2", "pic", 5), ("fewer", "bar", 10), ("more", "pic", 2), ("alt2", "bar", 5),
            ("fewer", "pic", 10), ("total", "bar", 2), ("more", "bar", 5), ("alt2", "pic", 10), ("fewer", "bar", 2),
            ("two_more", "bar", 5), ("total", "pic", 5), ("more", "pic", 10), ("two_fewer", "pic", 2), ("target", "bar", 10),
            ("two_more", "pic", 10), ("fewer", "pic", 5), ("two_fewer", "bar", 10), ("target", "pic", 5), ("two_more", "bar", 2)]
    for i, (kind, chart, sc) in enumerate(plan):
        def ok_ctx(c):
            if sc not in (c.pkeys if chart == "pic" else c.scales):
                return False
            if kind.startswith("two") and not c.two:
                return False
            if kind == "target" and not c.target:
                return False
            if kind == "alt2" and c.title == "How we travel to school":
                return False
            return True
        ctx = PK.next(ok_ctx)
        half = sc != 5 and i % 3 != 2
        n = 4

        def ok_vals(vs):
            s_ = sorted(vs)
            if kind == "two_more":
                return s_[3] > s_[0] + s_[1] and s_[3] - s_[0] - s_[1] >= 2
            if kind == "two_fewer":
                return s_[0] + s_[1] > s_[2] + 1 and s_[3] < s_[0] + s_[1] + s_[2] and s_[0] + s_[1] - s_[2] >= 2
            return max(vs) - min(vs) >= 2
        cats, vals = make_data(ctx, n, sc, half, rnd, max_units=6, ok=ok_vals)
        sym = SYMS[i % 3]
        if chart == "bar":
            f = fig(ctx_bar(ctx, cats, vals, sc, i % 5 == 3))
            rd = lambda k: "%s %d" % (cats[k], vals[k])
            wrongs = lambda v: bar_wrong(v, sc)
            how = "The scale goes up in %ds. " % sc
        else:
            f = fig(ctx_pic(ctx, cats, vals, sc, sym))
            rd = lambda k: "%s %s" % (cats[k], short_pic(vals[k], sc))
            wrongs = lambda v: pic_wrong(v, sc)
            how = "Each %s = %d%s. " % (sym, sc, ", so half a %s = %d" % (sym, sc // 2) if sc % 2 == 0 else "")
        U = ctx.unit
        # a misread of a value that ends between lines / on a half symbol (if there is one)
        def mis(k):
            w = wrongs(vals[k])
            return w[0] if chart == "bar" and vals[k] % sc else (w[1] if chart == "pic" and vals[k] % sc else w[0])
        if kind in ("more", "fewer"):
            pairs = [(a_, b_) for a_ in range(n) for b_ in range(n) if vals[a_] - vals[b_] >= max(2, sc)]
            hi, lo = rnd.choice(pairs)
            d = vals[hi] - vals[lo]
            mis_d = [vals[hi] - mis(lo) if vals[lo] % sc else None, mis(hi) - vals[lo] if vals[hi] % sc else None]
            mis_d = [z for z in mis_d if z]
            spaces = [d // sc] if d % sc == 0 and sc > 1 else []      # counted grid spaces / symbols
            q = ctx.more(cats[hi], cats[lo]) if kind == "more" else ctx.fewer(cats[lo], cats[hi])
            word = "How many more" if kind == "more" else "How many fewer"
            its.append(mcq(f + q, fmt(d, U), [fmt(z, U) for z in [vals[hi] + vals[lo]] + mis_d + spaces + [d + sc, d - sc, vals[hi]]],
                           "%s%s and %s. %s means find the difference: %d − %d = %s."
                           % (how, rd(hi), rd(lo), word, vals[hi], vals[lo], fmt(d, U))))
        elif kind == "alt2":
            k1, k2 = rnd.sample(range(n), 2)
            t = vals[k1] + vals[k2]
            its.append(mcq(f + ctx.both(cats[k1], cats[k2]), fmt(t, U),
                           [fmt(z, U) for z in [abs(vals[k1] - vals[k2])] +
                            [mis(k) + vals[k1 + k2 - k] for k in (k1, k2) if vals[k] % sc] +
                            ([t // sc] if t % sc == 0 else []) + [t + sc, t - sc]],
                           "%s%s and %s. Altogether means add: %d + %d = %s."
                           % (how, rd(k1), rd(k2), vals[k1], vals[k2], fmt(t, U))))
        elif kind == "total":
            t = sum(vals)
            mt = misread_total(vals, sc, chart)
            its.append(mcq(f + ctx.total, fmt(t, U), [fmt(z, U) for z in [mt, t - min(vals), t + sc, t - sc, t + 10]],
                           "%sRead every %s: %s. Add them: %s = %s."
                           % (how, "bar" if chart == "bar" else "row", ", ".join(rd(k) for k in range(n)),
                              " + ".join(str(v) for v in vals), fmt(t, U))))
        elif kind in ("two_more", "two_fewer"):
            order = sorted(range(n), key=lambda k: vals[k])
            if kind == "two_more":
                a, b, c = order[3], order[0], order[1]
                both = vals[b] + vals[c]
                d = vals[a] - both
                q = ctx.more2(cats[a], cats[b], cats[c])
                e2 = "Step 2: %d − %d = %s." % (vals[a], both, fmt(d, U))
                wrong = [vals[a] - vals[b], vals[a] - vals[c], vals[a] + both, d + sc]
            else:
                a, b, c = order[2], order[0], order[1]
                both = vals[b] + vals[c]
                d = both - vals[a]
                q = ctx.fewer2(cats[a], cats[b], cats[c])
                e2 = "Step 2: %d − %d = %s fewer." % (both, vals[a], fmt(d, U))
                wrong = [both, vals[a] - vals[b], vals[a] - vals[c], vals[a] + both, d + sc]
            its.append(mcq(f + q, fmt(d, U), [fmt(z, U) for z in wrong],
                           "%s%s, %s and %s. Step 1: %s and %s together: %d + %d = %d. %s"
                           % (how, rd(a), rd(b), rd(c), ctx.p(cats[b]), ctx.p(cats[c]), vals[b], vals[c], both, e2)))
        else:
            t = sum(vals)
            goal = (t // 50 + 1) * 50 if t >= 40 else (t // 10 + 2) * 10
            need = goal - t
            mt = misread_total(vals, sc, chart)
            its.append(mcq(f + ctx.target.format(n=goal), fmt(need, U),
                           [fmt(z, U) for z in [t, goal - mt, goal + t if goal + t < 1000 else need + 10, need + sc, need - sc]],
                           "%sStep 1: read every %s and add: %s = %d. Step 2: %d − %d = %s."
                           % (how, "bar" if chart == "bar" else "row", " + ".join(str(v) for v in vals), t, goal, t, fmt(need, U))))
    return {"title": "How many more, how many fewer, how many altogether?", "items": its}


# ------------------------------------------------------------ set 5: match the chart, and word problems
MATCH_WHY = {
    "swap": "two bars are the wrong way round",
    "low": "a bar is on the line below (it should be halfway between two lines)",
    "high": "one bar is one line too high",
    "pswap": "two rows are the wrong way round",
    "phalf": "a half symbol is drawn as a whole symbol",
    "pone": "one row has a symbol too many",
    "lowl": "one bar is one line too low",
    "pless": "one row is missing a symbol",
}


def match_variants(vals, step, rnd, pic=False):
    """The data, plus three wrong versions made from real drawing mistakes."""
    out = []
    i, j = rnd.sample([k for k in range(len(vals))], 2)
    sw = vals[:]
    sw[i], sw[j] = sw[j], sw[i]
    out.append(("pswap" if pic else "swap", sw))
    halves = [k for k in range(len(vals)) if vals[k] % step]
    if halves:
        k = halves[0]
        w = vals[:]
        if pic:
            w[k] = vals[k] + step // 2
            out.append(("phalf", w))
        else:
            w[k] = vals[k] - step // 2
            out.append(("low", w))
    k = rnd.choice([k for k in range(len(vals)) if not halves or k != halves[0]])
    w = vals[:]
    w[k] = vals[k] + step
    out.append(("pone" if pic else "high", w))
    return out


def match_q(rnd, pos, title, cats, vals, step, unit, pic=False, sym="circle"):
    wrong = match_variants(vals, step, rnd, pic)
    if len(wrong) < 3:
        hk = [k for k in range(len(vals)) if wrong[-1][1][k] != vals[k]][0]
        k = rnd.choice([k for k in range(len(vals)) if k != hk and vals[k] > step])
        w = vals[:]
        w[k] = vals[k] - step
        wrong.append(("pless" if pic else "lowl", w))
    wrong = wrong[:3]
    for _, w in wrong:
        assert w != vals
    order = wrong[:]
    order.insert(pos, ("ok", vals))
    assert len({tuple(v) for _, v in order}) == 4
    top_v = int(math.ceil(max(max(v) for _, v in order) / step) * step)
    if pic:
        draws = [(lambda x0, y0, v=v: mini_pic(x0, y0, cats, v, step, sym)) for _, v in order]
        svg = panel_svg(draws, "pictograms: " + title.lower(), key_line=(sym, "= " + fmt(step, unit)))
        q = "Which pictogram shows these numbers?"
    else:
        draws = [(lambda x0, y0, v=v: mini_bar(x0, y0, cats, v, step, top_v)) for _, v in order]
        svg = panel_svg(draws, "bar charts: " + title.lower())
        q = "Which bar chart shows these numbers?"
    why = []
    for k, (tag, v) in enumerate(order):
        if tag != "ok":
            why.append("%s: %s" % ("ABCD"[k], MATCH_WHY[tag]))
    e = ("%s matches every number%s. %s."
         % ("ABCD"[pos], " (each symbol = %d)" % step if pic else " (the scale goes up in %ds)" % step, "; ".join(why)))
    tb = "<b>%s:</b> %s. " % (title, ", ".join("%s %d" % (c, v) for c, v in zip(cats, vals)))
    return mcq_fixed(fig(svg) + tb + q, ["A", "B", "C", "D"], pos, e)


def set_words(rnd):
    its = []
    # 1-6 match a table to a chart (A to D in one picture)
    its.append(match_q(rnd, 2, "Favourite fruit", ["Apple", "Pear", "Plum", "Kiwi"], [8, 5, 10, 3], 2, VOTE))
    its.append(match_q(rnd, 0, "Minibeasts found", ["Ant", "Worm", "Snail", "Slug"], [15, 25, 10, 35], 5,
                       ("minibeast", "minibeasts")))
    its.append(match_q(rnd, 3, "Favourite colour", ["Red", "Blue", "Pink", "Green"], [40, 25, 60, 30], 10, VOTE))
    its.append(match_q(rnd, 1, "Books read", ["Ava", "Kai", "Leo", "Zara"], [6, 3, 8, 5], 2, ("book", "books"),
                       pic=True, sym="star"))
    its.append(match_q(rnd, 2, "Cakes sold", ["Mon", "Tue", "Wed", "Thu"], [20, 35, 15, 40], 10, ("cake", "cakes"),
                       pic=True, sym="circle"))
    its.append(match_q(rnd, 0, "Pets", ["Dog", "Cat", "Fish", "Bird"], [15, 10, 20, 5], 5, PUP, pic=True, sym="square"))
    B, P = ("book", "books"), PUP
    # 7 favourite fruit pictogram (key 2): how many more
    ctx = BYTITLE["Favourite fruit"]
    vals = [8, 5, 10, 3]
    pf = fig(ctx_pic(ctx, ["Apple", "Banana", "Grapes", "Pear"], vals, 2, "circle"))
    its.append(mcq(pf + "Year 3 voted for their favourite fruit. How many more pupils chose grapes than pears?",
                   fmt(7, P), [fmt(x, P) for x in [13, 8, 3]],
                   "Each circle = 2 votes, so half a circle = 1. Grapes: 5 × 2 = 10. Pear: 1 × 2 + 1 = 3. "
                   "How many more means subtract: 10 − 3 = 7. (Half a circle is 1 here, because half of 2 is 1.)"))
    # 8-9 minibeasts bar chart (scale 2)
    ctx = BYTITLE["Minibeasts in the garden"]
    mb = [9, 14, 6, 11, 16]
    bf = fig(ctx_bar(ctx, ["Ladybird", "Worm", "Snail", "Spider", "Woodlouse"], mb, 2))
    assert sum(mb) == 56
    its.append(mcq(bf + "Class 3B looked for minibeasts in the school garden. How many minibeasts did they find altogether?",
                   fmt(56, ("minibeast", "minibeasts")), [fmt(x, ("minibeast", "minibeasts")) for x in [54, 45, 28]],
                   "Read each bar: ladybirds 9, worms 14, snails 6, spiders 11, woodlice 16. "
                   "9 + 14 + 6 + 11 + 16 = 56. (Reading 9 and 11 as 8 and 10 gives 54.)"))
    its.append(mcq(bf + "How many more woodlice than snails did the class find?",
                   fmt(10, ("woodlouse", "woodlice")), [fmt(x, ("woodlouse", "woodlice")) for x in [22, 5, 16]],
                   "Woodlice: 16. Snails: 6. How many more means subtract: 16 − 6 = 10. "
                   "(5 is the number of grid spaces between the bars, not the number of minibeasts.)"))
    # 10-11 books read pictogram (key 5)
    ctx = BYTITLE["Books read this term"]
    bk = [15, 25, 10, 20]
    kf = fig(ctx_pic(ctx, ["Amelia", "Harry", "Isla", "Arjun"], bk, 5, "star"))
    its.append(mcq(kf + "Harry wants to read 40 books this term. How many more books does he need to read?",
                   fmt(15, B), [fmt(x, B) for x in [35, 65, 5]],
                   "Each star = 5 books. Harry has 5 stars: 5 × 5 = 25 books. 40 − 25 = 15 more books. "
                   "(35 comes from counting the stars as 5 books.)"))
    its.append(mcq(kf + "How many books did Amelia and Isla read altogether?",
                   fmt(25, B), [fmt(x, B) for x in [5, 50, 30]],
                   "Amelia: 3 stars, 3 × 5 = 15. Isla: 2 stars, 2 × 5 = 10. Altogether: 15 + 10 = 25 books. "
                   "(5 is the difference, or the number of stars.)"))
    # 12-13 after-school clubs tally
    clubs = [16, 8, 7, 5]
    tf = fig(tally_svg("After-school clubs", "Club", ["Football", "Art", "Choir", "Chess"], clubs,
                       label="tally chart: after-school clubs"))
    its.append(mcq(tf + "Art club has space for 15 children. How many more children can join Art club?",
                   fmt(7, ("child", "children")), [fmt(x, ("child", "children")) for x in [23, 8, 9]],
                   "Art: 1 group of 5 and 3 more = 8. 15 − 8 = 7 more children. "
                   "(Counting the group of 5 as 4 gives 7 children in Art, and a wrong answer of 8.)"))
    its.append(mcq(tf + "How many more children go to Football club than to Choir and Chess together?",
                   fmt(4, ("child", "children")), [fmt(x, ("child", "children")) for x in [28, 9, 11]],
                   "Football: 3 groups of 5 and 1 more = 16. Step 1: Choir and Chess together: 7 + 5 = 12. "
                   "Step 2: 16 − 12 = 4."))
    # 14 house points (scale 10, horizontal)
    ctx = BYTITLE["House points"]
    its.append(mcq(fig(ctx_bar(ctx, ["Kestrel", "Falcon", "Hawk", "Owl"], [35, 50, 25, 45], 10, True)) +
                   "How many fewer points has Hawk House got than Falcon House?",
                   fmt(25, ("point", "points")), [fmt(x, ("point", "points")) for x in [75, 30, 20]],
                   "Falcon: 50. Hawk: halfway between 20 and 30, so 25. 50 − 25 = 25 points. "
                   "(Reading Hawk as 20 gives 30.)"))
    # 15 cake sale money (key 10)
    ctx = BYTITLE["Cakes sold at the cake sale"]
    its.append(mcq(fig(ctx_pic(ctx, ["Mon", "Tue", "Wed", "Thu"], [20, 35, 15, 40], 10, "circle")) +
                   "Each cake costs £1. How much money did the cake sale make on Tuesday and Wednesday together?",
                   "£50", ["£20", "£42", "£5"],
                   "Each circle = 10 cakes, so half a circle = 5. Tuesday: 3 × 10 + 5 = 35. Wednesday: 1 × 10 + 5 = 15. "
                   "35 + 15 = 50 cakes, so £50. (Counting half a circle as 1 gives £42.)"))
    # 16 missing bar from total
    ctx = BYTITLE["Favourite sport"]
    sp = [10, 7, 6, 5]
    assert 28 - sum(sp[:3]) == sp[3]
    its.append(mcq(fig(ctx_bar(ctx, ["Football", "Netball", "Swimming", "Cricket"], sp, 2, False, missing=3)) +
                   "There are 28 pupils in the class. Each pupil chose one sport. The bar for cricket is missing. "
                   "How many pupils chose cricket?",
                   fmt(5, P), [fmt(x, P) for x in [23, 6, 51]],
                   "Step 1: add the other bars: 10 + 7 + 6 = 23. Step 2: 28 − 23 = 5 pupils chose cricket. "
                   "(Netball ends halfway between 6 and 8, so it is 7, not 6.)"))
    # 17 table: minibeasts two classes
    tb = fig(table_svg("Minibeasts found", ["Minibeast", "Class 3A", "Class 3B"], [["Worms", 12, 9], ["Snails", 7, 15]],
                       label="table: minibeasts found"))
    its.append(mcq(tb + "How many snails did the two classes find altogether?",
                   "22 snails", ["8 snails", "19 snails", "24 snails"],
                   "Find the Snails row: 7 and 15. Altogether means add: 7 + 15 = 22. "
                   "(19 is 12 + 7, which adds down the Class 3A column instead.)"))
    # 18 pets pictogram total with halves (key 2)
    ctx = BYTITLE["Pets in Year 3"]
    pv = [9, 6, 3, 4]
    its.append(mcq(fig(ctx_pic(ctx, ["Dog", "Cat", "Fish", "Rabbit"], pv, 2, "square")) +
                   "Each pupil has one pet. How many pupils are shown altogether?",
                   fmt(22, P), [fmt(x, P) for x in [20, 11, 24]],
                   "Each square = 2 pupils, so half a square = 1. Dog 9, cat 6, fish 3, rabbit 4. "
                   "9 + 6 + 3 + 4 = 22. (Counting the squares gives 11. Leaving out the half squares gives 20.)"))
    # 19 choose a key
    its.append(mcq("Leo wants to draw a pictogram of 40, 30, 50 and 20 votes. Which key needs the fewest symbols?",
                   "1 symbol = 10 votes", ["1 symbol = 1 vote", "1 symbol = 2 votes", "1 symbol = 5 votes"],
                   "The bigger the key, the fewer symbols you draw. With 1 symbol = 10 votes, 40 votes is just 4 symbols. "
                   "With 1 symbol = 2 votes it would be 20 symbols."))
    # 20 ice creams two-step (scale 5)
    ic = Ctx("Ice creams sold", "Flavour", ["Vanilla", "Strawberry", "Chocolate", "Mint"], ("ice cream", "ice creams"),
             "", "", "", "", "", [5], [])
    its.append(mcq(fig(ctx_bar(ic, ["Vanilla", "Strawberry", "Chocolate", "Mint"], [35, 20, 45, 15], 5)) +
                   "How many fewer chocolate ice creams were sold than vanilla and mint ice creams together?",
                   "5 ice creams", ["95 ice creams", "10 ice creams", "30 ice creams"],
                   "Step 1: vanilla and mint together: 35 + 15 = 50. Step 2: chocolate is 45. 50 − 45 = 5 fewer."))
    assert len(its) == 20
    return {"title": "Match the chart, and word problems", "items": its}


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
    return (
        "<h2>Three ways to show data</h2>"
        "<p>Data is information we collect, such as votes or minibeasts we find. "
        "A <b>tally chart</b> or a <b>table</b> shows the numbers. "
        "A <b>pictogram</b> or a <b>bar chart</b> lets you compare them at a glance.</p>"
        "<h2>Read a pictogram</h2>"
        "<p>Look at the <b>key</b> first. One symbol can stand for 2, 5 or 10. "
        "Count the symbols in a row in 2s, 5s or 10s. "
        "Half a symbol stands for <b>half of the key</b>, not 1.</p>"
        "<figure class='sn-fig'>" + ctx_pic(fr, ["Apple", "Banana", "Grapes", "Pear"], [6, 7, 4, 9], 2, "circle") +
        "<figcaption>Each circle = 2 votes, so half a circle = 1 vote. Banana: 2, 4, 6, and 1 more = 7 votes.</figcaption></figure>" +
        ex("Example", "How many votes did Pear get?", "4 circles and half a circle. Count in 2s: 2, 4, 6, 8, then 1 more for the half.", "9 votes") +
        "<p>If each symbol = 10, half a symbol = 5. Three and a half symbols = 10, 20, 30 and 5 more = 35.</p>"
        "<h2>Read a bar chart</h2>"
        "<p>First find what the <b>scale</b> goes up in: 2s, 5s or 10s. Then go across from the top of the bar to the scale. "
        "If a bar ends halfway between two lines, the number is halfway between them.</p>"
        "<figure class='sn-fig'>" + bar_svg("Pets in Year 3", "Pet", "Pupils", ["Dog", "Cat", "Fish", "Rabbit"],
                                            [12, 7, 4, 9], 2, False, label="bar chart: pets in year 3") +
        "<figcaption>The scale goes up in 2s. The Cat bar ends halfway between 6 and 8, so 7 pupils have a cat.</figcaption></figure>" +
        ex("Example", "How many more pupils have a dog than a rabbit?", "Dog: 12. Rabbit: 9. 12 − 9 = 3.", "3 more pupils") +
        "<h2>Tally charts and tables</h2>"
        "<p>In a tally chart, every fifth mark goes across the other four. Count the groups in 5s, then add the single marks.</p>"
        "<figure class='sn-fig'>" + tally_svg("Vehicles past the school", "Vehicle", ["Car", "Van", "Bus"], [17, 8, 3],
                                              label="tally chart: vehicles past the school") +
        "<figcaption>Car: 3 groups of 5 and 2 more: 5, 10, 15, then 16, 17. So 17 cars.</figcaption></figure>"
        "<p>In a table, find the right row, then go across to the right column.</p>" +
        table(["Minibeast", "Class 3A", "Class 3B"], [["Worms", "11", "8"], ["Snails", "6", "13"]]) +
        ex("Example", "How many snails did Class 3B find?", "Snails row, Class 3B column: 13.", "13 snails") +
        "<h2>Add or subtract?</h2>" +
        table(["The question says", "Do this"], [
            ["altogether, in total, both, A or B", "Add"],
            ["how many more, how many fewer, difference", "Subtract"],
        ]) +
        "<p>A <b>two-step</b> question needs two sums. Do one step, then use the answer in the next step.</p>" +
        ex("Two-step example", "Football got 16 votes. Choir got 7 and Chess got 5. How many more votes did Football get than Choir and Chess together?",
           "Step 1: 7 + 5 = 12. Step 2: 16 − 12 = 4.", "4 more votes") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Counting symbols, not using the key (4 circles = 4)", "Use the key: 4 circles of 5 = 20"],
            ["Saying half a symbol = 1", "Half a symbol is half of the key: half of 10 is 5"],
            ["Reading a bar between two lines as the lower line", "Halfway between 10 and 20 is 15"],
            ["Counting grid spaces instead of reading the scale", "Read the number on the scale"],
            ["Counting a tally group of 5 as 4", "The line across is the fifth mark"],
            ["Adding when the question says how many more", "How many more means subtract"],
        ])
    )


FAQ = [
    {"q": "What statistics do children learn in Year 3?",
     "a": "In Year 3 children read and draw bar charts, pictograms and tables. They answer one-step and two-step questions such as “How many more?” and “How many fewer?”."},
    {"q": "How do you read a pictogram with a key?",
     "a": "Look at the key first, then count the symbols in 2s, 5s or 10s. Half a symbol is half of the key, so if one circle = 10, half a circle = 5."},
    {"q": "How do you read a bar chart with a scale of 2, 5 or 10?",
     "a": "Find what the scale goes up in, then go across from the top of the bar to the scale. If the bar ends halfway between two lines, the number is halfway between them."},
    {"q": "What is a two-step problem with a bar chart?",
     "a": "It is a question that needs two sums. For example, add two bars together first, then find the difference between that total and a third bar."},
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
    rnd = random.Random(3314)
    PK = Picker(rnd)
    sets = [set_pictogram(rnd, PK), set_bar(rnd, PK), set_tally_table(rnd), set_compare(rnd, PK), set_words(rnd)]
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
        "country": "uk", "subject": "maths", "grade": "year-3", "slug": "bar-charts-and-pictograms", "sort": 14,
        "updated": UPDATED, "pdf_url": "",
        "title": "Bar Charts, Pictograms and Tables",
        "seo_title": "Year 3 Bar Charts and Pictograms Worksheets: Tally Charts, Tables and How Many More (Free, with Answers)",
        "short_title": "Bar charts and pictograms",
        "domain": "Statistics",
        "standard_code": "Year 3: Statistics",
        "standard_url": "https://www.gov.uk/government/publications/national-curriculum-in-england-mathematics-programmes-of-study",
        "standard_text": "Interpret and present data using bar charts, pictograms and tables; solve one-step and two-step questions [for example, ‘How many more?’ and ‘How many fewer?’] using information presented in scaled bar charts and pictograms and tables.",
        "meta_desc": "Free Year 3 maths worksheets on statistics: pictograms where one symbol stands for 2, 5 or 10, bar charts with scales of 2, 5 and 10, tally charts and tables, and one-step and two-step “how many more?” and “how many fewer?” questions. 100 questions with an answer key, following the National Curriculum.",
        "key_big": "Look at the key or the scale first. Then read the chart.",
        "key_sub": "If one symbol = 10, half a symbol = 5. A bar halfway between 10 and 20 shows 15. Altogether means add; how many more or how many fewer means subtract.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


def mark_large(u, pattern):
    """Tag pictures that must print larger (charts, tables, A to D panels) so their labels stay readable."""
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
        mark_large(u, "(pictogram|bar chart|tally chart|table)")
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
