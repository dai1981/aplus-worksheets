# -*- coding: utf-8 -*-
"""
AU Year 3 Maths: Data and graphs (Australian Curriculum v9.0: AC9M3ST01, AC9M3ST02)
  python3 tools/gen_au_maths_y3_data.py
Tally marks and frequency tables (categorical and discrete numerical data), pictographs (one-to-one, then a key
of 2 or 5; half symbols only for a key of 2), column graphs with scales of 1, 2 and 5 (columns that end between
gridlines), comparing two representations of the same data (A to D in one picture) and interpreting data in context.
Wrong answers come from real student mistakes: counting a tally group of 5 as 4, counting symbols instead of using
the key, half a symbol = 1, reading a column between gridlines as the lower line, counting grid spaces,
adding instead of subtracting (sum vs difference), reading the height of a column as the category.
HTML attributes use single quotes (no backslashes in the JSON). Australian English.
"""
import json, re, math, os, random

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "au", "maths", "year-3")
UPDATED = "2026-11-02"
GREEN = "#006633"
BAR = "#2e8b57"
BAR2 = "#3a6ea5"
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
        lead = c.split(" ")[0].lstrip("$")
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
    w, h = int(math.ceil(w)), int(math.ceil(h))
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def part_svg(part, label):
    W, H, body = part
    return svg_wrap(W, H, body, label)


def side_by_side(parts, label, gap=24):
    """Several (W, H, body) parts in one picture, next to each other."""
    x = 0
    H = max(p[1] for p in parts)
    s = []
    for k, (w, h, b) in enumerate(parts):
        if k:
            s.append("<line x1='%.1f' y1='6' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1'/>"
                     % (x - gap / 2, x - gap / 2, H - 6, GRID))
        s.append("<g transform='translate(%.1f 0)'>%s</g>" % (x, b))
        x += w + gap
    return svg_wrap(x - gap, H, "".join(s), label)


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


# ------------------------------------------------------------ pictograph symbols
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
                 ordered=False, maxv=None):
        self.title, self.axis, self.cats, self.unit = title, axis, cats, unit
        self.ask_f, self.more_f, self.fewer_f, self.both_f, self.total = ask, more, fewer, both, total
        self.scales, self.pkeys, self.ph, self.ordered, self.maxv = scales, pkeys, ph or {}, ordered, maxv

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


VOTE = ("vote", "votes")
STU = ("student", "students")
FAM = ("family", "families")
LOWER = lambda cs: {c: c.lower() for c in cs}

CTXS = [
    Ctx("Favourite sport", "Sport", ["AFL", "Cricket", "Netball", "Soccer", "Swimming"], STU,
        "How many students chose {a}?", "How many more students chose {a} than {b}?",
        "How many fewer students chose {a} than {b}?", "How many students chose {a} or {b}?",
        "How many students voted altogether?", [1, 2, 5], [1, 2, 5],
        ph={"AFL": "AFL", "Cricket": "cricket", "Netball": "netball", "Soccer": "soccer", "Swimming": "swimming"}),
    Ctx("Favourite fruit", "Fruit", ["Apple", "Banana", "Mango", "Orange", "Watermelon"], VOTE,
        "How many votes did {a} get?", "How many more votes did {a} get than {b}?",
        "How many fewer votes did {a} get than {b}?", "How many votes did {a} and {b} get altogether?",
        "How many votes were there altogether?", [1, 2, 5], [1, 2, 5]),
    Ctx("Favourite Australian animal", "Animal", ["Koala", "Kangaroo", "Wombat", "Echidna", "Platypus"], VOTE,
        "How many votes did the {a} get?", "How many more votes did the {a} get than the {b}?",
        "How many fewer votes did the {a} get than the {b}?", "How many votes did the {a} and the {b} get altogether?",
        "How many votes were there altogether?", [1, 2, 5], [1, 2, 5],
        ph=LOWER(["Koala", "Kangaroo", "Wombat", "Echidna", "Platypus"])),
    Ctx("How we travel to school", "Way", ["Walk", "Car", "Bus", "Bike", "Scooter"], STU,
        "How many students {a} to school?", "How many more students {a} to school than {b}?",
        "How many fewer students {a} to school than {b}?", "How many students {a} or {b} to school?",
        "How many students are in the survey altogether?", [2, 5], [2, 5],
        ph={"Walk": "walk", "Car": "come by car", "Bus": "come by bus", "Bike": "ride a bike", "Scooter": "ride a scooter"}),
    Ctx("Birds seen in the schoolyard", "Bird", ["Magpie", "Kookaburra", "Galah", "Lorikeet", "Ibis"], ("bird", "birds"),
        "How many {a} were seen?", "How many more {a} than {b} were seen?",
        "How many fewer {a} than {b} were seen?", "How many {a} and {b} were seen altogether?",
        "How many birds were seen altogether?", [1, 2], [1, 2], maxv=16,
        ph={"Magpie": "magpies", "Kookaburra": "kookaburras", "Galah": "galahs", "Lorikeet": "lorikeets", "Ibis": "ibises"}),
    Ctx("Ice blocks sold at the canteen", "Day", ["Mon", "Tue", "Wed", "Thu", "Fri"], ("ice block", "ice blocks"),
        "How many ice blocks were sold on {a}?", "How many more ice blocks were sold on {a} than on {b}?",
        "How many fewer ice blocks were sold on {a} than on {b}?", "How many ice blocks were sold on {a} and {b} altogether?",
        "How many ice blocks were sold altogether?", [2, 5], [2, 5], ordered=True,
        ph={"Mon": "Monday", "Tue": "Tuesday", "Wed": "Wednesday", "Thu": "Thursday", "Fri": "Friday"}),
    Ctx("Books read this term", "Student", ["Charlotte", "Oliver", "Isla", "Jack", "Mia", "Noah"], ("book", "books"),
        "How many books did {a} read?", "How many more books did {a} read than {b}?",
        "How many fewer books did {a} read than {b}?", "How many books did {a} and {b} read altogether?",
        "How many books did the students read altogether?", [1, 2], [1, 2]),
    Ctx("Pets in Year 3", "Pet", ["Dog", "Cat", "Fish", "Bird", "Guinea pig"], STU,
        "How many students have a {a}?", "How many more students have a {a} than a {b}?",
        "How many fewer students have a {a} than a {b}?", "How many students have a {a} or a {b}?",
        "How many students are shown altogether?", [1, 2], [1, 2], maxv=14,
        ph=LOWER(["Dog", "Cat", "Fish", "Bird", "Guinea pig"])),
    Ctx("House points", "House", ["Banksia", "Wattle", "Waratah", "Jacaranda"], ("point", "points"),
        "How many points did {a} House get?", "How many more points did {a} House get than {b} House?",
        "How many fewer points did {a} House get than {b} House?", "How many points did {a} and {b} get altogether?",
        "How many points did the houses get altogether?", [5], [5]),
    Ctx("Cans collected for recycling", "Class", ["3A", "3B", "3C", "3D"], ("can", "cans"),
        "How many cans did class {a} collect?", "How many more cans did class {a} collect than {b}?",
        "How many fewer cans did class {a} collect than {b}?", "How many cans did classes {a} and {b} collect altogether?",
        "How many cans did the classes collect altogether?", [5], [5], ordered=True),
    Ctx("Shells found at the beach", "Student", ["Ruby", "Kai", "Zara", "Leo", "Grace"], ("shell", "shells"),
        "How many shells did {a} find?", "How many more shells did {a} find than {b}?",
        "How many fewer shells did {a} find than {b}?", "How many shells did {a} and {b} find altogether?",
        "How many shells did they find altogether?", [1, 2, 5], [1, 2, 5]),
    Ctx("People in our families", "Number of people", ["2", "3", "4", "5", "6"], FAM,
        "How many families have {a} people?", "How many more families have {a} people than {b} people?",
        "How many fewer families have {a} people than {b} people?", "How many families have {a} or {b} people?",
        "How many families are in the survey?", [1, 2], [], ordered=True, maxv=12),
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
    if ctx.maxv:
        max_units = min(max_units, ctx.maxv // step)
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


# ------------------------------------------------------------ pictograph
def pic_part(title, cats, vals, key, sym, unit, missing=None):
    """Pictograph: one row per category, symbols worth `key` each, key line at the bottom."""
    fs, rh, gap = 15, 26, 23
    lw = max(tw(c, fs) for c in cats) + 22
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
        if i == missing:
            s.append(text(lw + 20, y + 19, "?", 18, bold=True, col=RED))
            continue
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
    return (W, H, "".join(s))


def ctx_pic(ctx, cats, vals, key, sym):
    return part_svg(pic_part(ctx.title, cats, vals, key, sym, ctx.unit), "pictograph: " + ctx.title.lower())


# ------------------------------------------------------------ column graph
def bar_part(title, cat_axis, val_axis, cats, vals, scale, missing=None, top_v=None, col=BAR):
    """Column graph with a gridline at every step of the scale.
    `missing` = index of a category drawn with no column (a red ? shows where it goes)."""
    fs = 14
    top_v = top_v or int(math.ceil(max(vals) / scale) * scale)
    nt = top_v // scale
    assert 2 <= nt <= 10, (title, vals, scale)
    s = []
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
            s.append("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' fill='%s'/>" % (cx - bw / 2, yb - h, bw, h, col))
        s.append(text(cx, yb + 17, c, fs))
    s.append("<path d='M%d %d V%d H%d' fill='none' stroke='%s' stroke-width='2'/>" % (x0, y0 - 6, yb, x0 + pw, INK))
    s.append(text(x0 + pw / 2, yb + 36, cat_axis, fs, bold=True))
    mid = y0 + ph / 2
    s.append(text(13, mid, val_axis, fs, bold=True, extra=" transform='rotate(-90 13 %.1f)'" % mid))
    H = yb + 42
    assert tw(val_axis, fs, True) < ph + 26, (val_axis, ph)
    return (W, H, "".join(s))


def bar_svg(title, cat_axis, val_axis, cats, vals, scale, missing=None, label="column graph"):
    return part_svg(bar_part(title, cat_axis, val_axis, cats, vals, scale, missing), label)


def ctx_bar(ctx, cats, vals, scale, missing=None):
    return bar_svg(ctx.title, ctx.axis, ctx.unit[1].capitalize(), cats, vals,
                   scale, missing, label="column graph: " + ctx.title.lower())


# ------------------------------------------------------------ A-D panels (one picture)
PW, PH = 218, 172


def mini_bar(x0, y0, cats, vals, scale, top_v):
    """A small column graph inside a panel (no title): scale on the left, short labels below."""
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
        if nt <= 8 or k % 2 == 0:
            s.append(text(ax - 4, y + 5, k * scale, fs, anchor="end"))
    for i, (c, v) in enumerate(zip(cats, vals)):
        cx = ax + slot * i + slot / 2
        h = v / scale * gy
        s.append("<rect x='%.1f' y='%.1f' width='24' height='%.1f' fill='%s'/>" % (cx - 12, yb - h, h, BAR))
        s.append(text(cx, yb + 17, c, fs))
        assert tw(c, fs) <= slot - 4, c
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


def mini_tally(x0, y0, cats, vals):
    fs, rh = 14, 25
    lw = x0 + max(tw(c, fs) for c in cats) + 14
    s = []
    for i, (c, v) in enumerate(zip(cats, vals)):
        y = y0 + 28 + i * rh
        s.append(text(lw - 7, y + 17, c, fs, anchor="end"))
        s.append(tally_marks(lw + 10, y + rh / 2 + 1, v))
        assert lw + 10 + tally_width(v) <= x0 + PW - 4
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


# ------------------------------------------------------------ tally marks and frequency tables
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


def tally_only_svg(v):
    W = tally_width(v) + 30
    W = max(W, 80)
    return svg_wrap(W, 34, "<rect x='1' y='1' width='%d' height='32' rx='4' fill='#ffffff' stroke='%s' stroke-width='1.5'/>"
                    % (W - 2, GRID) + tally_marks(15, 17, v), "tally marks")


def freq_part(title, head, cats, vals, tally=True, freq=True, missing=None, total=False):
    """Frequency table: category | tally | frequency. `missing` = row whose frequency is a red ?."""
    fs, rh = 15, 28
    c1 = int(max(max(tw(c, fs) for c in cats), tw(head, fs, True)) + 20)
    cols = [c1]
    if tally:
        cols.append(int(max(max(tally_width(v) for v in vals) + 24, 70)))
    if freq:
        cols.append(int(tw("Frequency", fs, True) + 20))
    top = 28
    tot = sum(cols)
    W = int(max(tot + 8, tw(title, 16, True) + 16))
    x0 = (W - tot) / 2
    s = [text(W / 2, 19, title, 16, bold=True)]
    rows = [(head, None)] + list(zip(cats, vals))
    if total:
        rows.append(("Total", sum(vals)))
    for r, (c, v) in enumerate(rows):
        y = top + r * rh
        hd = r == 0
        x = x0
        for k, cw in enumerate(cols):
            s.append("<rect x='%.1f' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.5'/>"
                     % (x, y, cw, rh, FILL2 if hd or k == 0 else "#ffffff", GREEN))
            name = "freq" if (k == 2 or (k == 1 and not tally)) else ("tally" if k == 1 else "cat")
            if name == "cat":
                s.append(text(x + 10, y + 19, c, fs, anchor="start", bold=hd or c == "Total"))
            elif hd:
                s.append(text(x + 10 if name == "tally" else x + cw / 2, y + 19, "Tally" if name == "tally" else "Frequency",
                              fs, anchor="start" if name == "tally" else "middle", bold=True))
            elif name == "tally":
                if c != "Total":
                    s.append(tally_marks(x + 14, y + rh / 2, v))
            else:
                if r - 1 == missing:
                    s.append(text(x + cw / 2, y + 20, "?", 17, bold=True, col=RED))
                else:
                    s.append(text(x + cw / 2, y + 19, v, fs, bold=c == "Total"))
            x += cw
    H = top + len(rows) * rh + 4
    return (W, H, "".join(s))


def freq_svg(title, head, cats, vals, label, **kw):
    return part_svg(freq_part(title, head, cats, vals, **kw), label)


# ------------------------------------------------------------ reading text (used in explanations)
def read_pic(c, v, key, sym, unit):
    full, hf = v // key, v % key
    if key == 1:
        return "The %s row has %s, so it shows %s." % (c, ones(full, sym), fmt(v, unit))
    if hf:
        if full == 0:
            return "The %s row has half a %s: half of %d is %s." % (c, sym, key, fmt(v, unit))
        return ("The %s row has %s and half a %s: %d × %d = %d, and half of %d is %d, so %d + %d = %s."
                % (c, ones(full, sym), sym, full, key, full * key, key, hf, full * key, hf, fmt(v, unit)))
    return "The %s row has %s: %d × %d = %s." % (c, ones(full, sym), full, key, fmt(v, unit))


def short_pic(v, key):
    full, hf = v // key, v % key
    if key == 1:
        return "%d" % v
    if hf:
        return "%d × %d + %d = %d" % (full, key, hf, v) if full else "half of %d = %d" % (key, v)
    return "%d × %d = %d" % (full, key, v)


def read_bar(c, v, scale):
    if v % scale:
        lo = v - v % scale
        return "The column for %s ends halfway between %d and %d, so it shows %d." % (c, lo, lo + scale, v)
    return "The column for %s ends on the line for %d." % (c, v)


def pic_wrong(v, key):
    """Real misreadings of one pictograph row."""
    full, hf = v // key, v % key
    out = [full + (1 if hf else 0)]                 # counted the symbols
    if hf:
        out += [full * key, (full + 1) * key]       # ignored the half / half counted as whole
    return out


def bar_wrong(v, scale):
    if v % scale:
        lo = v - v % scale
        return [lo, lo + scale]                     # read the line below / above
    return [v // scale]                             # counted grid spaces


def tally_text(v):
    g, r = v // 5, v % 5
    if g and r:
        return "%s of 5 and %d more: %d × 5 = %d, and %d + %d = %d." % (ones(g, "group"), r, g, g * 5, g * 5, r, v)
    if g:
        return "%s of 5: %d × 5 = %d." % (ones(g, "group"), g, v)
    return "%d single marks." % r


def tally_cands(v, others=()):
    g, r = v // 5, v % 5
    return [g * 4 + r, g + r, v + 1, v - 1, v + 5] + list(others)


# ------------------------------------------------------------ set 1: tally marks and frequency tables
def set_tally(rnd):
    its = []
    # 1-4 count tally marks
    for v in (8, 13, 19, 22):
        its.append(mcq(fig(tally_only_svg(v)) + "What number do these tally marks show?", v, tally_cands(v),
                       "Each group of 5 is four lines with one line across. Count the groups in 5s, then count on the "
                       "single marks: %s" % tally_text(v)))
    # 5 which tally shows 16 (A to D in one picture)
    vs = [16, 21, 15, 17]
    pos = 1
    order = vs[1:]
    order.insert(pos, vs[0])
    W = 2 * 190
    s = []
    for k, v in enumerate(order):
        x0, y0 = (k % 2) * 190, (k // 2) * 44
        s.append(text(x0 + 8, y0 + 27, "ABCD"[k], 17, anchor="start", bold=True))
        s.append(tally_marks(x0 + 34, y0 + 21, v))
        assert x0 + 34 + tally_width(v) < x0 + 186
    svg = svg_wrap(W, 88, "".join(s), "four sets of tally marks")
    wrong = {21: "one group of 5 too many", 15: "one single mark is missing", 17: "one single mark too many"}
    its.append(mcq_fixed(fig(svg) + "Which tally marks show 16?", ["A", "B", "C", "D"], pos,
                         "16 = 5 + 5 + 5 + 1, so look for 3 groups of 5 and 1 single mark. That is %s. "
                         % "ABCD"[pos] + "; ".join("%s shows %d (%s)" % ("ABCD"[k], v, wrong[v])
                                                    for k, v in enumerate(order) if v != 16) + "."))
    # 6-9 frequency table with tallies: favourite fruit
    cats = ["Apple", "Banana", "Mango", "Orange", "Watermelon"]
    vals = [9, 6, 14, 4, 11]
    f = fig(freq_svg("Favourite fruit", "Fruit", cats, vals, "frequency table: favourite fruit", missing=2))
    its.append(mcq(f + "What number should go in the Frequency column for Mango?", 14, tally_cands(14, [9, 11]),
                   "The frequency is the number the tally marks show. Mango has %s" % tally_text(14)))
    its.append(mcq(f + "Which fruit got the most votes?", "Mango", ["Watermelon", "Apple", "Banana"],
                   "Mango has 14 votes (2 groups of 5 and 4 more). That is more than Watermelon (11) and Apple (9)."))
    its.append(mcq(f + "How many more votes did Watermelon get than Orange?", fmt(7, VOTE),
                   [fmt(x, VOTE) for x in [15, 6, 8, 11]],
                   "Watermelon 11, Orange 4. How many more means find the difference: 11 − 4 = 7."))
    tot = sum(vals)
    its.append(mcq(f + "How many students voted altogether? (Each student voted once.)", fmt(tot, STU),
                   [fmt(x, STU) for x in [tot - 14, sum((v // 5) * 4 + v % 5 for v in vals), tot - 4, tot + 1]],
                   "Find the Mango frequency first: 14. Then add all the rows: 9 + 6 + 14 + 4 + 11 = %d." % tot))
    # 10-13 discrete numerical data: people in families
    cats = ["2", "3", "4", "5", "6"]
    vals = [3, 7, 11, 5, 2]
    f = fig(freq_svg("People in our families", "People", cats, vals, "frequency table: people in our families"))
    its.append(mcq(f + "How many families have 4 people?", fmt(11, FAM), [fmt(x, FAM) for x in [4, 9, 3, 12, 7]],
                   "Find the row for 4 people. The frequency is 11 (2 groups of 5 and 1 more). "
                   "The 4 is the number of people, not the number of families."))
    its.append(mcq(f + "Which number of people is the most common family size?", "4 people",
                   ["11 people", "6 people", "3 people"],
                   "The biggest frequency is 11, in the row for 4 people. So 4 people is the most common family size. "
                   "11 is how many families, not how many people."))
    its.append(mcq(f + "How many families are in the survey?", fmt(28, FAM), [fmt(x, FAM) for x in [20, 5, 11, 27]],
                   "Add the frequencies: 3 + 7 + 11 + 5 + 2 = 28 families. (20 is 2 + 3 + 4 + 5 + 6, the family sizes.)"))
    its.append(mcq(f + "How many families have more than 4 people?", fmt(7, FAM), [fmt(x, FAM) for x in [5, 18, 11, 2]],
                   "More than 4 means 5 or 6 people: 5 + 2 = 7 families. Do not include the families with exactly 4 people."))
    # 14-16 frequency table without tallies: birds
    cats = ["Magpie", "Kookaburra", "Galah", "Lorikeet", "Ibis"]
    vals = [12, 3, 8, 15, 6]
    f = fig(freq_svg("Birds seen in the schoolyard", "Bird", cats, vals, "frequency table: birds seen in the schoolyard",
                     tally=False))
    its.append(mcq(f + "How many more magpies than galahs were seen?", fmt(4, ("bird", "birds")),
                   [fmt(x, ("bird", "birds")) for x in [20, 12, 5, 3]],
                   "Magpie 12, Galah 8. How many more means subtract: 12 − 8 = 4."))
    its.append(mcq(f + "Which bird was seen half as many times as the magpie?", "Ibis", ["Galah", "Kookaburra", "Lorikeet"],
                   "The magpie was seen 12 times. Half of 12 is 6. The ibis has a frequency of 6."))
    its.append(mcq(f + "Mia sees 4 more lorikeets. What is the new frequency for Lorikeet?", 19, [11, 15, 4, 20],
                   "The lorikeet frequency was 15. 4 more means add: 15 + 4 = 19."))
    # 17-18 categorical and numerical data
    its.append(mcq("Which survey question has answers that are numbers?", "How many pets do you have?",
                   ["What is your favourite colour?", "How do you get to school?", "What is your favourite sport?"],
                   "“How many pets do you have?” has number answers, such as 0, 1, 2 or 3. The other questions have "
                   "answers that are words (categories), such as red, bus or cricket."))
    its.append(mcq("Which survey question has answers that are categories (words), not numbers?",
                   "What is your favourite fruit?",
                   ["How many brothers and sisters do you have?", "How many books did you read this week?",
                    "How many people are in your family?"],
                   "Favourite fruit gives answers like apple or mango. These are categories. "
                   "The other questions ask “how many”, so the answers are numbers."))
    # 19-20 word problems about tallies
    its.append(mcq("Jack makes a tally of the cars that pass the school gate. He draws 4 groups of five and 3 single marks. "
                   "How many cars has he counted?", fmt(23, ("car", "cars")),
                   [fmt(x, ("car", "cars")) for x in [19, 7, 43, 24]],
                   "Each group of five shows 5: 5, 10, 15, 20. Then 3 more: 21, 22, 23. So 23 cars. "
                   "(Counting each group as 4 gives 19.)"))
    its.append(mcq("Ruby counted 17 votes for netball. How should she draw the tally?", "3 groups of five and 2 marks",
                   ["2 groups of five and 7 marks", "4 groups of five and 1 mark", "17 groups of five"],
                   "17 = 5 + 5 + 5 + 2. Draw 3 groups of five (four lines and one across) and 2 single marks. "
                   "Never leave 5 or more single marks: make another group of five."))
    assert len(its) == 20
    return {"title": "Tally marks and frequency tables", "items": its}


# ------------------------------------------------------------ set 2: pictographs
def set_pictograph(rnd, PK):
    its = []
    plan = [(1, "read"), (1, "most"), (1, "more"), (1, "read"), (1, "total"),
            (2, "read"), (2, "readh"), (2, "half"), (2, "draw"), (2, "which"), (2, "readh"), (2, "fewest"), (2, "more"),
            (5, "read"), (5, "draw"), (5, "which"), (5, "read"), (5, "most"), (5, "more"), (5, "total")]
    draws = iter([("Each star stands for 2 books. Noah read 12 books. How many stars should be in his row?", 12, 2, "star"),
                  ("Each square stands for 5 students. 35 students walk to school. How many squares should be in the Walk row?",
                   35, 5, "square")])
    for i, (key, kind) in enumerate(plan):
        sym = SYMS[i % 3]
        if kind == "draw":
            q, v, k, sym = next(draws)
            assert k == key and v % key == 0
            full = v // key
            ans = ones(full, sym)
            cand = [ones(v, sym), ones(full + 1, sym), ones(full - 1, sym), ones(key, sym)]
            e = ("Count in %ds until you reach %d: %s. That is %s, so draw %s. Check: %d × %d = %d. "
                 "(Drawing %s would show %d × %d.)"
                 % (key, v, ", ".join(str(key * t) for t in range(1, full + 1)), ones(full, "step"), ans, full, key, v,
                    ones(v, sym), v, key))
            its.append(mcq(q, ans, cand, e))
            continue
        ctx = PK.next(lambda c: key in c.pkeys)
        half = key == 2 and kind in ("readh", "half", "which")
        n = 5 if i % 4 == 3 and len(ctx.cats) >= 5 else 4
        okh = (lambda vs: any(v % key and v > key for v in vs)) if half else (lambda vs: max(vs) - min(vs) >= 2)
        cats, vals = make_data(ctx, n, key, half, rnd, max_units=6 if key > 1 else 8, min_units=1 if key > 1 else 2, ok=okh)
        f = fig(ctx_pic(ctx, cats, vals, key, sym))
        U = ctx.unit
        keytxt = ("Look at the key: each %s stands for %s. " % (sym, fmt(key, U)))
        if kind in ("read", "readh"):
            if kind == "readh":
                j = rnd.choice([k for k, v in enumerate(vals) if v % key and v > key])
            else:
                j = rnd.randrange(n)
            c, v = cats[j], vals[j]
            others = [vals[k] for k in range(n) if k != j]
            cand = pic_wrong(v, key) + [v + key, v - key] + others + [v * 2] if key > 1 else others + [v + 1, v - 1]
            its.append(mcq(f + ctx.ask(c), fmt(v, U), [fmt(x, U) for x in cand], keytxt + read_pic(c, v, key, sym, U)))
        elif kind in ("most", "fewest"):
            j = vals.index(max(vals) if kind == "most" else min(vals))
            w = "most" if kind == "most" else "fewest"
            q = "Which row shows the %s %s?" % (w, U[1])
            its.append(mcq(f + q, cats[j], [cats[k] for k in range(n) if k != j],
                           "Every %s stands for the same number, so the row with the %s %ss shows the %s. %s"
                           % (sym, w, sym, w, read_pic(cats[j], vals[j], key, sym, U))))
        elif kind == "half":
            its.append(mcq(f + "In this pictograph, what does half a %s stand for?" % sym, fmt(key // 2, U),
                           [fmt(key, U), fmt(key * 2, U), fmt(3, U), fmt(5, U)],
                           "The key says one whole %s = %s. Half a %s is half of %d, which is %s."
                           % (sym, fmt(key, U), sym, key, fmt(key // 2, U))))
        elif kind == "which":
            hs = [k for k in range(n) if vals[k] % key and vals[k] > key] if half else list(range(n))
            j = rnd.choice(hs)
            v = vals[j]
            near = sorted([k for k in range(n) if k != j], key=lambda k: abs(vals[k] - v))
            cand = [cats[k] for k in range(n) if k != j and math.ceil(vals[k] / key) == v] + [cats[k] for k in near]
            if half:
                e = "Half a %s is %d, so %s is %s. %s" % (sym, key // 2, fmt(v, U), halfs(v, key, sym),
                                                        read_pic(cats[j], v, key, sym, U))
            else:
                e = "Each %s = %d. %d ÷ %d = %d, so look for %s. %s" % (sym, key, v, key, v // key, ones(v // key, sym),
                                                                       read_pic(cats[j], v, key, sym, U))
            its.append(mcq(f + "Which row shows %s?" % fmt(v, U), cats[j], cand, e))
        elif kind == "more":
            pairs = [(a, b) for a in range(n) for b in range(n) if vals[a] - vals[b] >= max(2, key)]
            a, b = rnd.choice(pairs)
            d = vals[a] - vals[b]
            cand = [vals[a] + vals[b]] + ([d // key] if key > 1 else []) + [d + key, d - key, vals[a], d + 1]
            its.append(mcq(f + ctx.more(cats[a], cats[b]), fmt(d, U), [fmt(x, U) for x in cand],
                           "%s%s and %s. How many more means find the difference: %d − %d = %s."
                           % (keytxt, "%s: %s" % (cats[a], short_pic(vals[a], key)),
                              "%s: %s" % (cats[b], short_pic(vals[b], key)), vals[a], vals[b], fmt(d, U))))
        else:
            t = sum(vals)
            nsym = sum(math.ceil(v / key) for v in vals)
            cand = ([nsym] if key > 1 else []) + [t - min(vals), t + key, t - key, t + 10]
            its.append(mcq(f + ctx.total, fmt(t, U), [fmt(x, U) for x in cand],
                           "%sRead every row: %s. Add them: %s = %s."
                           % (keytxt, ", ".join("%s %d" % (c, v) for c, v in zip(cats, vals)),
                              " + ".join(str(v) for v in vals), fmt(t, U))))
    return {"title": "Pictographs: 1 symbol = 1, 2 or 5", "items": its}


# ------------------------------------------------------------ set 3: column graphs
def set_column(rnd, PK):
    its = []
    plan = [(1, "read"), (1, "step"), (1, "most"), (1, "read"), (1, "which"), (1, "more"),
            (2, "step"), (2, "read"), (2, "readh"), (2, "readh"), (2, "which"), (2, "fewest"), (2, "readh"), (2, "more"),
            (5, "read"), (5, "step"), (5, "read"), (5, "which"), (5, "more"), (5, "both")]
    for i, (sc, kind) in enumerate(plan):
        ctx = PK.next(lambda c: sc in c.scales)
        half = sc == 2 and kind in ("readh", "which", "more")
        n = 5 if (i % 3 == 0 and len(ctx.cats) >= 5) else 4
        cats, vals = make_data(ctx, n, sc, half, rnd, max_units=8 if sc == 1 else 7, min_units=1 if sc > 1 else 2)
        f = fig(ctx_bar(ctx, cats, vals, sc))
        U = ctx.unit
        lab = (lambda c: c + " people") if ctx.unit == FAM else (lambda c: c)
        scl = "The scale goes up in %ds. " % sc
        if kind in ("read", "readh"):
            if kind == "readh":
                j = rnd.choice([k for k, v in enumerate(vals) if v % sc])
            else:
                j = rnd.randrange(n)
            c, v = cats[j], vals[j]
            others = [vals[k] for k in range(n) if k != j]
            cand = bar_wrong(v, sc) + [v + sc, v - sc] + others + [v + 1] if sc > 1 else [v + 1, v - 1] + others
            its.append(mcq(f + ctx.ask(c), fmt(v, U), [fmt(x, U) for x in cand],
                           "%s%s So the answer is %s." % (scl, read_bar(lab(c), v, sc), fmt(v, U))))
        elif kind == "step":
            its.append(mcq(f + "What does the scale on this column graph go up in?", "%ds" % sc,
                           ["%ds" % x for x in (1, 2, 5, 10) if x != sc],
                           "Read the numbers on the scale: 0, %d, %d, %d … Each line is %d more than the one before, "
                           "so the scale goes up in %ds." % (sc, 2 * sc, 3 * sc, sc, sc)))
        elif kind == "which":
            if half:
                j = rnd.choice([k for k, v in enumerate(vals) if v % sc])
            else:
                j = rnd.randrange(n)
            v = vals[j]
            near = sorted([k for k in range(n) if k != j], key=lambda k: abs(vals[k] - v))
            its.append(mcq(f + "Which column shows %s?" % fmt(v, U), lab(cats[j]), [lab(cats[k]) for k in near],
                           "%sFind %d on the scale. %s" % (scl, v, read_bar(lab(cats[j]), v, sc))))
        elif kind in ("most", "fewest"):
            j = vals.index(max(vals) if kind == "most" else min(vals))
            word = "tallest" if kind == "most" else "shortest"
            q = "Which column shows the %s %s?" % ("most" if kind == "most" else "fewest", U[1])
            its.append(mcq(f + q, lab(cats[j]), [lab(cats[k]) for k in range(n) if k != j],
                           "The column for %s is the %s one. %s It shows %s." % (lab(cats[j]), word, read_bar(lab(cats[j]), vals[j], sc),
                                                                             fmt(vals[j], U))))
        elif kind == "more":
            pairs = [(a, b) for a in range(n) for b in range(n) if vals[a] - vals[b] >= max(2, sc)
                     and (not half or vals[a] % sc or vals[b] % sc)]
            a, b = rnd.choice(pairs)
            d = vals[a] - vals[b]
            mis = []
            if vals[b] % sc:
                mis.append(vals[a] - (vals[b] - vals[b] % sc))
            if vals[a] % sc:
                mis.append(vals[a] - vals[a] % sc - vals[b])
            spaces = [d // sc] if d % sc == 0 and sc > 1 else []
            cand = [vals[a] + vals[b]] + mis + spaces + [d + sc, d - sc, vals[a], d + 1]
            its.append(mcq(f + ctx.more(cats[a], cats[b]), fmt(d, U), [fmt(x, U) for x in cand],
                           "%s%s: %d. %s: %d. How many more means find the difference: %d − %d = %s."
                           % (scl, lab(cats[a]), vals[a], lab(cats[b]), vals[b], vals[a], vals[b], fmt(d, U))))
        else:
            a, b = rnd.sample(range(n), 2)
            t = vals[a] + vals[b]
            cand = [abs(vals[a] - vals[b]), t // sc, t + sc, t - sc, t + 10]
            its.append(mcq(f + ctx.both(cats[a], cats[b]), fmt(t, U), [fmt(x, U) for x in cand],
                           "%s%s: %d. %s: %d. Altogether means add: %d + %d = %s."
                           % (scl, lab(cats[a]), vals[a], lab(cats[b]), vals[b], vals[a], vals[b], fmt(t, U))))
    return {"title": "Column graphs with scales of 1, 2 and 5", "items": its}


# ------------------------------------------------------------ set 4: compare representations
MATCH_WHY = {
    "swap": "two columns are the wrong way round",
    "low": "a column is on the line below (it should be halfway between two lines)",
    "high": "one column is one line too high",
    "lowl": "one column is one line too low",
    "pswap": "two rows are the wrong way round",
    "phalf": "a half symbol is drawn as a whole symbol",
    "pone": "one row has a symbol too many",
    "pless": "one row is missing a symbol",
    "pcount": "it draws one symbol for every student and ignores the key",
}


def match_q(rnd, pos, title, cats, vals, step, unit, pic=False, sym="circle", show="list", extra=None):
    """Which picture (A to D) shows this data? Wrong pictures come from real drawing mistakes."""
    wrong = []
    i, j = rnd.sample([k for k in range(len(vals)) if True], 2)
    while vals[i] == vals[j]:
        i, j = rnd.sample(range(len(vals)), 2)
    sw = vals[:]
    sw[i], sw[j] = sw[j], sw[i]
    wrong.append(("pswap" if pic else "swap", sw))
    halves = [k for k in range(len(vals)) if vals[k] % step]
    if halves:
        k = halves[0]
        w = vals[:]
        w[k] = vals[k] + step // 2 if pic else vals[k] - step // 2
        wrong.append(("phalf" if pic else "low", w))
    k = rnd.choice([k for k in range(len(vals)) if not halves or k != halves[0]])
    w = vals[:]
    w[k] = vals[k] + step
    wrong.append(("pone" if pic else "high", w))
    if len(wrong) < 3:
        k2 = rnd.choice([x for x in range(len(vals)) if x != k and vals[x] > step])
        w = vals[:]
        w[k2] = vals[k2] - step
        wrong.append(("pless" if pic else "lowl", w))
    wrong = wrong[:3]
    order = wrong[:]
    order.insert(pos, ("ok", vals))
    assert len({tuple(v) for _, v in order}) == 4
    top_v = int(math.ceil(max(max(v) for _, v in order) / step) * step)
    if pic:
        draws = [(lambda x0, y0, v=v: mini_pic(x0, y0, cats, v, step, sym)) for _, v in order]
        svg = panel_svg(draws, "pictographs: " + title.lower(), key_line=(sym, "= " + fmt(step, unit)))
        q = "Which pictograph shows the same data?"
    else:
        draws = [(lambda x0, y0, v=v: mini_bar(x0, y0, cats, v, step, top_v)) for _, v in order]
        svg = panel_svg(draws, "column graphs: " + title.lower())
        q = "Which column graph shows the same data?"
    why = ["%s: %s" % ("ABCD"[k], MATCH_WHY[tag]) for k, (tag, v) in enumerate(order) if tag != "ok"]
    e = ("%s matches every number%s. %s."
         % ("ABCD"[pos], " (each symbol = %d)" % step if pic else " (the scale goes up in %ds)" % step, "; ".join(why)))
    if show == "tally":
        tb = "<b>%s</b> (tally): %s. " % (title, ", ".join("%s %s" % (c, tally_word(v)) for c, v in zip(cats, vals)))
        e = "First count the tallies: %s. " % ", ".join("%s %d" % (c, v) for c, v in zip(cats, vals)) + e
    else:
        tb = "<b>%s</b> (frequency table): %s. " % (title, ", ".join(("%s people: %d" if unit == FAM else "%s %d") % (c, v) for c, v in zip(cats, vals)))
    return mcq_fixed(fig(svg) + tb + q, ["A", "B", "C", "D"], pos, e)


def tally_word(v):
    g, r = v // 5, v % 5
    parts = []
    if g:
        parts.append(ones(g, "group") + " of 5")
    if r:
        parts.append(ones(r, "mark"))
    return " and ".join(parts)


def set_compare(rnd):
    its = []
    # 1-4 table -> column graph (A to D)
    its.append(match_q(rnd, 2, "Favourite colour", ["Red", "Blue", "Pink", "Grey"], [5, 8, 3, 6], 1, VOTE))
    its.append(match_q(rnd, 0, "People in families", ["2", "3", "4", "5"], [4, 9, 12, 7], 2, FAM))
    its.append(match_q(rnd, 3, "Cans collected", ["3A", "3B", "3C", "3D"], [25, 40, 15, 30], 5, ("can", "cans")))
    its.append(match_q(rnd, 1, "Ice blocks sold", ["Mon", "Tue", "Wed", "Thu"], [11, 6, 14, 9], 2, ("ice block", "ice blocks")))
    # 5-8 tally / table -> pictograph (A to D)
    its.append(match_q(rnd, 1, "Pets", ["Dog", "Cat", "Fish", "Bird"], [6, 4, 3, 5], 1, STU, pic=True, sym="circle",
                       show="tally"))
    its.append(match_q(rnd, 3, "Shells found", ["Ruby", "Kai", "Zara", "Leo"], [8, 5, 10, 3], 2, ("shell", "shells"),
                       pic=True, sym="star"))
    its.append(match_q(rnd, 0, "Cans collected", ["3A", "3B", "3C", "3D"], [20, 35, 15, 30], 5, ("can", "cans"),
                       pic=True, sym="square"))
    its.append(match_q(rnd, 2, "Fruit eaten", ["Apple", "Kiwi", "Plum", "Pear"], [10, 7, 12, 5], 2, ("piece", "pieces"),
                       pic=True, sym="circle", show="tally"))
    # 9-11 column graph -> list of numbers
    G = [(BYTITLE["Favourite sport"], ["AFL", "Cricket", "Netball", "Soccer"], [12, 7, 10, 5], 2),
         (BYTITLE["Favourite Australian animal"], ["Koala", "Kangaroo", "Wombat", "Echidna"], [30, 15, 25, 10], 5),
         (BYTITLE["Birds seen in the schoolyard"], ["Magpie", "Galah", "Lorikeet", "Ibis"], [6, 9, 4, 7], 1)]
    for ctx, cats, vals, sc in G:
        f = fig(ctx_bar(ctx, cats, vals, sc))
        lst = lambda vs: ", ".join(str(v) for v in vs)
        sw = vals[:]
        sw[1], sw[2] = sw[2], sw[1]
        if sc == 2:
            cand = [[v - v % 2 for v in vals], sw, [v // 2 for v in vals]]
            why = "Reading the columns that end between lines as the line below gives %s." % lst(cand[0])
        elif sc == 5:
            cand = [[v // 5 for v in vals], sw, [v + 5 for v in vals]]
            why = "Counting grid spaces instead of reading the scale gives %s." % lst(cand[0])
        else:
            cand = [[v + 1 for v in vals], sw, [v - 1 for v in vals]]
            why = "Read the line at the top of each column, not the space above it."
        q = ("Which list of numbers matches this column graph? The numbers are in this order: %s."
             % ", ".join(ctx.p(c) for c in cats))
        its.append(mcq(f + q, lst(vals), [lst(c) for c in cand],
                       "The scale goes up in %ds. %s %s" % (sc, " ".join(read_bar(c, v, sc) for c, v in zip(cats, vals)), why)))
    # 12-15 pictograph and column graph of the same data, one column missing
    P = [(BYTITLE["Favourite fruit"], ["Apple", "Banana", "Mango", "Orange"], [6, 9, 4, 7], 2, 1, "circle", 2),
         (BYTITLE["Shells found at the beach"], ["Ruby", "Kai", "Zara", "Leo"], [15, 10, 25, 20], 5, 2, "star", 5),
         (BYTITLE["Books read this term"], ["Isla", "Jack", "Mia", "Noah"], [8, 5, 3, 6], 1, 3, "square", 1),
         (BYTITLE["How we travel to school"], ["Walk", "Car", "Bus", "Bike"], [12, 16, 7, 4], 2, 2, "circle", 2)]
    for ctx, cats, vals, key, miss, sym, sc in P:
        U = ctx.unit
        pp = pic_part(ctx.title, cats, vals, key, sym, U)
        bp = bar_part("Column graph", ctx.axis, U[1].capitalize(), cats, vals, sc, missing=miss)
        svg = side_by_side([pp, bp], "pictograph and column graph: " + ctx.title.lower())
        v = vals[miss]
        cand = pic_wrong(v, key) + [vals[miss - 1], v + key, v - 1]
        its.append(mcq(fig(svg) + "The pictograph and the column graph show the same data. "
                       "How many %s should the missing %s column show?" % (U[1], cats[miss]), fmt(v, U),
                       [fmt(x, U) for x in cand],
                       "Read the %s row of the pictograph. Each %s = %s. %s Draw the %s column up to %d."
                       % (cats[miss], sym, fmt(key, U), read_pic(cats[miss], v, key, sym, U), cats[miss], v)))
    # 16-20 two classes, two column graphs
    cats = ["Dog", "Cat", "Fish", "Bird"]
    a = [7, 5, 2, 4]
    b = [4, 8, 3, 6]
    pa = bar_part("Class 3A", "Pet", "Students", cats, a, 1, top_v=8)
    pb = bar_part("Class 3B", "Pet", "Students", cats, b, 1, top_v=8, col=BAR2)
    f = fig(side_by_side([pa, pb], "two column graphs: pets in class 3a and class 3b"))
    its.append(mcq(f + "How many more students in Class 3B than in Class 3A have a cat?", fmt(3, STU),
                   [fmt(x, STU) for x in [13, 8, 1, 4]],
                   "Class 3B cat: 8. Class 3A cat: 5. How many more means subtract: 8 − 5 = 3."))
    its.append(mcq(f + "Which pet is the most common in Class 3A but not in Class 3B?", "Dog", ["Cat", "Bird", "Fish"],
                   "In Class 3A the tallest column is Dog (7). In Class 3B the tallest column is Cat (8)."))
    its.append(mcq(f + "How many students in the two classes have a bird?", fmt(10, STU), [fmt(x, STU) for x in [2, 6, 4, 11]],
                   "Class 3A bird: 4. Class 3B bird: 6. Both classes means add: 4 + 6 = 10."))
    its.append(mcq(f + "How many students are shown in Class 3B’s graph?", fmt(21, STU), [fmt(x, STU) for x in [18, 8, 39, 20]],
                   "Add the Class 3B columns: 4 + 8 + 3 + 6 = 21. (18 is Class 3A: 7 + 5 + 2 + 4.)"))
    its.append(mcq(f + "Which statement is true?", "Class 3B has 1 more fish than Class 3A.",
                   ["Class 3A has more cats than Class 3B.", "Both classes have the same number of dogs.",
                    "Class 3A has 6 birds."],
                   "Fish: Class 3B 3, Class 3A 2, so 3B has 1 more. Class 3A has 5 cats and 3B has 8. "
                   "Dogs: 7 and 4. Class 3A has 4 birds; 6 birds is Class 3B."))
    assert len(its) == 20, len(its)
    return {"title": "Compare different graphs of the same data", "items": its}


# ------------------------------------------------------------ set 5: interpret data in context
def set_words(rnd):
    its = []
    S = STU
    sp_c = ["AFL", "Cricket", "Netball", "Soccer", "Swimming"]
    sp_v = [12, 7, 10, 9, 4]
    sport = fig(bar_svg("Favourite sport in Year 3", "Sport", "Students", sp_c, sp_v, 2,
                        label="column graph: favourite sport in year 3"))
    its.append(mcq(sport + "How many students chose AFL or soccer?", fmt(21, S), [fmt(x, S) for x in [3, 20, 22, 12]],
                   "The scale goes up in 2s. AFL ends on 12. Soccer ends halfway between 8 and 10, so 9. "
                   "AFL or soccer means add: 12 + 9 = 21. (Reading soccer as 8 gives 20.)"))
    its.append(mcq(sport + "How many more students chose netball than swimming?", fmt(6, S), [fmt(x, S) for x in [14, 3, 10]],
                   "Netball 10, swimming 4. How many more means subtract: 10 − 4 = 6. "
                   "(14 is the sum, and 3 counts the grid spaces between the columns.)"))
    tot = sum(sp_v)
    its.append(mcq(sport + "Every student in Year 3 voted once. How many students voted?", fmt(tot, S),
                   [fmt(x, S) for x in [40, 21, 41]],
                   "Read every column: 12, 7, 10, 9 and 4. Cricket and soccer end between gridlines, so they are 7 and 9. "
                   "12 + 7 + 10 + 9 + 4 = %d. (Reading 7 and 9 as 6 and 8 gives 40.)" % tot))
    its.append(mcq(sport + "Which statement is true?", "Cricket got 3 more votes than swimming.",
                   ["Soccer got more votes than netball.", "Swimming was the most popular sport.",
                    "AFL got twice as many votes as netball."],
                   "Cricket 7 and swimming 4: 7 − 4 = 3, so this is true. Soccer (9) is less than netball (10). "
                   "Swimming (4) is the least popular. Twice netball would be 20, not 12."))
    its.append(mcq(sport + "The teacher will choose the two most popular sports for the next sport lesson. Which two?",
                   "AFL and netball", ["AFL and soccer", "Netball and soccer", "Cricket and swimming"],
                   "The two tallest columns are AFL (12) and netball (10). Soccer is 9, just below netball."))
    # fruit pictograph, key 2
    PF = ("piece of fruit", "pieces of fruit")
    fr_c = ["Apple", "Banana", "Mango", "Orange"]
    fr_v = [8, 11, 6, 5]
    fruit = fig(part_svg(pic_part("Fruit eaten at recess", fr_c, fr_v, 2, "circle", PF), "pictograph: fruit eaten at recess"))
    its.append(mcq(fruit + "How many pieces of fruit were eaten at recess altogether?", fmt(30, PF),
                   [fmt(x, PF) for x in [16, 28, 32]],
                   "Each circle = 2, so half a circle = 1. Apple 8, banana 5 × 2 + 1 = 11, mango 6, orange 2 × 2 + 1 = 5. "
                   "8 + 11 + 6 + 5 = 30. (Counting the circles gives 16. Leaving out the halves gives 28.)"))
    its.append(mcq(fruit + "How many more bananas than oranges were eaten?", fmt(6, ("banana", "bananas")),
                   [fmt(x, ("banana", "bananas")) for x in [16, 3, 5]],
                   "Banana 11, orange 5. How many more means subtract: 11 − 5 = 6. "
                   "(3 is the difference in the number of circles, not in pieces of fruit.)"))
    # ice blocks column graph, scale 5
    IB = ("ice block", "ice blocks")
    ib_c = ["Mon", "Tue", "Wed", "Thu", "Fri"]
    ib_v = [15, 25, 10, 35, 40]
    ice = fig(bar_svg("Ice blocks sold at the canteen", "Day", "Ice blocks", ib_c, ib_v, 5,
                      label="column graph: ice blocks sold at the canteen"))
    its.append(mcq(ice + "Ice blocks cost $2 each. How much money did the canteen make from ice blocks on Thursday?", "$70",
                   ["$35", "$37", "$60"],
                   "Thursday: 35 ice blocks. Each costs $2, so 35 × 2 = 70. The canteen made $70. "
                   "(35 is the number of ice blocks, not dollars.)"))
    its.append(mcq(ice + "On which day were 15 more ice blocks sold than on Wednesday?", "Tuesday",
                   ["Monday", "Thursday", "Friday"],
                   "Wednesday: 10. 15 more than 10 is 10 + 15 = 25. Tuesday shows 25. "
                   "(Monday shows 15, but the question asks for 15 more than Wednesday.)"))
    its.append(mcq(ice + "On two days the weather was very hot. Which two days were most likely the hot days?",
                   "Thursday and Friday", ["Monday and Wednesday", "Monday and Tuesday", "Tuesday and Wednesday"],
                   "People buy more ice blocks on hot days. The two tallest columns are Thursday (35) and Friday (40)."))
    # travel frequency table
    tr_c = ["Walk", "Car", "Bus", "Bike"]
    tr_v = [9, 14, 6, 3]
    trv = fig(freq_svg("How we travel to school", "Way", tr_c, tr_v, "frequency table: how we travel to school"))
    its.append(mcq(trv + "How many students do not come to school by car?", fmt(18, S), [fmt(x, S) for x in [32, 14, 15]],
                   "Not by car means walk, bus or bike: 9 + 6 + 3 = 18. (32 is everyone, and 14 is only the car students.)"))
    its.append(mcq(trv + "Next week 5 of the car students will walk instead. How many students will walk?", fmt(14, S),
                   [fmt(x, S) for x in [4, 9, 19]],
                   "5 more students will walk: 9 + 5 = 14. (19 adds the 5 to the car row instead.)"))
    # family size column graph, scale 1
    fm_c = ["2", "3", "4", "5", "6"]
    fm_v = [3, 6, 8, 4, 2]
    fam = fig(bar_svg("People in our families", "Number of people", "Families", fm_c, fm_v, 1,
                      label="column graph: people in our families"))
    its.append(mcq(fam + "What is the most common number of people in a family?", "4 people",
                   ["8 people", "6 people", "3 people"],
                   "The tallest column is above 4, so 4 people is the most common. The column is 8 high, "
                   "which means 8 families, not 8 people."))
    its.append(mcq(fam + "How many families have 5 or more people?", fmt(6, FAM), [fmt(x, FAM) for x in [4, 2, 11]],
                   "5 or more means the columns for 5 and 6 people: 4 + 2 = 6 families. "
                   "(11 adds the family sizes 5 + 6, not the families.)"))
    its.append(mcq(fam + "How many families were in the survey?", fmt(23, FAM), [fmt(x, FAM) for x in [20, 8, 5]],
                   "Add the heights of all the columns: 3 + 6 + 8 + 4 + 2 = 23 families. "
                   "(20 adds the numbers under the columns, 2 + 3 + 4 + 5 + 6.)"))
    # cans pictograph, key 5
    CN = ("can", "cans")
    cn_c = ["3A", "3B", "3C", "3D"]
    cn_v = [30, 45, 20, 35]
    cans = fig(part_svg(pic_part("Cans collected for recycling", cn_c, cn_v, 5, "square", CN),
                        "pictograph: cans collected for recycling"))
    its.append(mcq(cans + "Year 3 wants to collect 150 cans. How many more cans do they need?", fmt(20, CN),
                   [fmt(x, CN) for x in [130, 124, 30]],
                   "Each square = 5 cans. 3A 30, 3B 45, 3C 20, 3D 35. Step 1: 30 + 45 + 20 + 35 = 130. "
                   "Step 2: 150 − 130 = 20. (Counting squares gives 26, and 150 − 26 = 124.)"))
    its.append(mcq(cans + "Class 3B says, “We collected more cans than 3A and 3C together.” Are they right?",
                   "No. 3A and 3C collected 50, which is 5 more.",
                   ["Yes. 3B has the most squares.", "Yes. 3B collected 45 and 3A collected 30.",
                    "No. 3B collected 9 cans."],
                   "3B: 9 squares × 5 = 45 cans. 3A and 3C together: 30 + 20 = 50 cans. 50 is more than 45, so 3B is wrong."))
    # drawing and choosing
    its.append(mcq("Mia is drawing a column graph. The scale goes up in 2s. Netball got 7 votes. Where should the top of the "
                   "netball column be?", "Halfway between 6 and 8",
                   ["On the line for 6", "On the line for 8", "On the 7th line up"],
                   "There is no line for 7, because the lines go 0, 2, 4, 6, 8. 7 is halfway between 6 and 8. "
                   "(The 7th line up is 14.)"))
    its.append(mcq("Leo will draw a pictograph of 10, 15, 20 and 5 votes. He wants whole symbols only and as few symbols "
                   "as he can. Which key should he use?", "1 symbol = 5 votes",
                   ["1 symbol = 1 vote", "1 symbol = 2 votes", "1 symbol = 10 votes"],
                   "Every number is in the 5 times table, so a key of 5 gives whole symbols: 2, 3, 4 and 1. "
                   "A key of 10 would need half symbols for 15 and 5. Keys of 1 or 2 need many more symbols."))
    its.append(mcq(sport + "How many more students chose netball or soccer than chose AFL?", fmt(7, S),
                   [fmt(x, S) for x in [31, 3, 2]],
                   "Step 1: netball or soccer: 10 + 9 = 19. Step 2: AFL is 12. 19 − 12 = 7 more. "
                   "(31 adds all three. 3 is 12 − 9.)"))
    assert len(its) == 20
    return {"title": "Interpret data: word problems", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


def body_html():
    sp = ["AFL", "Cricket", "Netball", "Soccer"]
    spv = [8, 5, 7, 4]
    return (
        "<h2>Collect, then show the data</h2>"
        "<p>Data is information we collect, such as votes in a class survey. "
        "Some data is in <b>categories</b> (words, such as cricket or netball). "
        "Some data is <b>numbers</b> (such as how many people are in each family).</p>"
        "<p>We record the data with <b>tally marks</b>, write it in a <b>frequency table</b>, "
        "then show it as a <b>pictograph</b> or a <b>column graph</b>. "
        "All four can show the same data.</p>"
        "<h2>Tally marks and frequency tables</h2>"
        "<p>Draw one mark for each answer. The fifth mark goes across the other four. "
        "Count the groups in 5s, then add the single marks. The <b>frequency</b> is how many.</p>"
        "<figure class='sn-fig'>" + freq_svg("Favourite sport", "Sport", sp, spv, "frequency table: favourite sport") +
        "<figcaption>AFL: 1 group of 5 and 3 more, so the frequency is 8.</figcaption></figure>" +
        ex("Example", "How many students chose netball?", "1 group of 5 is 5. Then 2 more: 6, 7.", "7 students") +
        "<h2>Pictographs</h2>"
        "<p>Look at the <b>key</b> first. One symbol can stand for 1, 2 or 5. "
        "Count the symbols in 1s, 2s or 5s. If one symbol stands for 2, half a symbol stands for 1.</p>"
        "<figure class='sn-fig'>" + part_svg(pic_part("Favourite sport", sp, spv, 2, "circle", STU),
                                             "pictograph: favourite sport") +
        "<figcaption>Each circle = 2 students. Netball: 2, 4, 6, and half a circle is 1 more, so 7.</figcaption></figure>" +
        ex("Example", "How many students chose soccer?", "2 circles. Count in 2s: 2, 4.", "4 students") +
        "<h2>Column graphs</h2>"
        "<p>Find what the <b>scale</b> goes up in: 1s, 2s or 5s. Go across from the top of the column to the scale. "
        "If a column ends halfway between two gridlines, the number is halfway between them.</p>"
        "<figure class='sn-fig'>" + bar_svg("Favourite sport", "Sport", "Students", sp, spv, 2,
                                            label="column graph: favourite sport") +
        "<figcaption>The scale goes up in 2s. Cricket ends halfway between 4 and 6, so 5 students chose cricket.</figcaption></figure>" +
        ex("Example", "How many more students chose AFL than cricket?", "AFL 8, cricket 5. 8 − 5 = 3.", "3 more students") +
        "<p>The table, the pictograph and the column graph above all show the same data. "
        "To check that two graphs match, read every category in both.</p>"
        "<h2>Add or subtract?</h2>" +
        table(["The question says", "Do this"], [
            ["altogether, in total, both, A or B", "Add"],
            ["how many more, how many fewer, difference", "Subtract"],
        ]) +
        ex("Two-step example", "Netball got 7 votes and soccer got 4. How many more votes did netball and soccer get "
           "together than AFL (8)?", "Step 1: 7 + 4 = 11. Step 2: 11 − 8 = 3.", "3 more votes") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Counting a tally group of 5 as 4", "The line across is the fifth mark"],
            ["Counting symbols and ignoring the key (4 circles = 4)", "Use the key: 4 circles of 2 = 8"],
            ["Saying half a symbol = 1 for every key", "Half a symbol is half of the key"],
            ["Reading a column between gridlines as the lower line", "Halfway between 6 and 8 is 7"],
            ["Counting grid spaces instead of reading the scale", "Read the number on the scale"],
            ["Adding when the question says how many more", "How many more means subtract"],
        ])
    )


FAQ = [
    {"q": "What do Year 3 students learn about data in the Australian Curriculum?",
     "a": "They collect data with tally marks, record it in frequency tables, and show it in pictographs and column graphs. They compare the graphs and explain what the data tells them."},
    {"q": "What is the difference between a pictograph and a column graph?",
     "a": "A pictograph uses symbols, and a key tells you how many each symbol stands for. A column graph uses columns, and you read the height against the scale."},
    {"q": "How do you read tally marks?",
     "a": "Each group of four lines with one line across is 5. Count the groups in 5s, then add the single marks: 3 groups and 2 marks is 17."},
    {"q": "Are graphs and tables in the Year 3 NAPLAN numeracy test?",
     "a": "Yes. NAPLAN numeracy includes statistics, so students may need to read tables, pictographs and column graphs and answer questions such as “How many more?”."},
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
    rnd = random.Random(3813)
    PK = Picker(rnd)
    sets = [set_tally(rnd), set_pictograph(rnd, PK), set_column(rnd, PK), set_compare(rnd), set_words(rnd)]
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
        "country": "au", "subject": "maths", "grade": "year-3", "slug": "data-and-graphs", "sort": 13,
        "updated": UPDATED, "pdf_url": "",
        "title": "Data and Graphs: Tally Marks, Pictographs and Column Graphs",
        "seo_title": "Year 3 Data and Graphs Worksheets: Tally Marks, Pictographs and Column Graphs (Free, with Answer Key)",
        "short_title": "Data and graphs",
        "domain": "Statistics",
        "standard_code": "AC9M3ST02",
        "standard_url": "https://v9.australiancurriculum.edu.au/f-10-curriculum/learning-areas/mathematics",
        "standard_text": "Create and compare different graphical representations of data sets including using software where appropriate; interpret the data in terms of the context",
        "meta_desc": "Free Year 3 maths worksheets on data and graphs for the Australian Curriculum: tally marks and frequency tables, pictographs with a key, column graphs with scales of 1, 2 and 5, comparing graphs and NAPLAN-style “how many more?” questions. 100 questions with an answer key.",
        "key_big": "Read the key or the scale first. Then read every row or column.",
        "key_sub": "A tally group is 5. If one symbol = 2, half a symbol = 1. A column halfway between 6 and 8 shows 7. Altogether means add; how many more means subtract.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


def mark_large(u, pattern):
    """Tag pictures that must print larger (graphs, tables, A to D panels) so their labels stay readable."""
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
        mark_large(u, "(pictograph|column graph|frequency table|two column|four sets)")
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
