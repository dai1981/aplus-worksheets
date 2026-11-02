# -*- coding: utf-8 -*-
"""
AU Year 4 Maths: Data and graphs (Australian Curriculum v9.0: AC9M4ST01, AC9M4ST02, AC9M4ST03)
  python3 tools/gen_au_maths_y4_data.py
Tally marks and frequency tables (categorical and discrete numerical data), many-to-one pictographs (1 symbol = 2, 5
or 10; half symbols for keys of 2 and 10), column graphs with scales of 2, 5 and 10 (columns that end between
gridlines), choosing a key or a scale, comparing displays of the same data (A to D in one picture), dot plots,
planning a survey and checking whether a conclusion is supported by the data.
Wrong answers come from real student mistakes: reading each symbol as 1, half a symbol = 1, counting grid spaces,
reading a column between gridlines as the line below, counting the stacks on a dot plot, adding the numbers on the
axis instead of the frequencies, and conclusions about people who were not asked.
HTML attributes use single quotes (no backslashes in the JSON). Australian English.
"""
import json, re, math, os, random

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "au", "maths", "year-4")
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
LOWER = lambda cs: {c: c.lower() for c in cs}

CTXS = [
    Ctx("Favourite sport", "Sport", ["AFL", "Cricket", "Netball", "Soccer", "Swimming"], STU,
        "How many students chose {a}?", "How many more students chose {a} than {b}?",
        "How many fewer students chose {a} than {b}?", "How many students chose {a} or {b}?",
        "How many students voted altogether?", [2, 5, 10], [2, 5, 10],
        ph={"AFL": "AFL", "Cricket": "cricket", "Netball": "netball", "Soccer": "soccer", "Swimming": "swimming"}),
    Ctx("Favourite fruit", "Fruit", ["Apple", "Banana", "Mango", "Orange", "Watermelon"], VOTE,
        "How many votes did {a} get?", "How many more votes did {a} get than {b}?",
        "How many fewer votes did {a} get than {b}?", "How many votes did {a} and {b} get altogether?",
        "How many votes were there altogether?", [2, 5], [2, 5]),
    Ctx("Favourite Australian animal", "Animal", ["Koala", "Kangaroo", "Wombat", "Echidna", "Platypus"], VOTE,
        "How many votes did the {a} get?", "How many more votes did the {a} get than the {b}?",
        "How many fewer votes did the {a} get than the {b}?", "How many votes did the {a} and the {b} get altogether?",
        "How many votes were there altogether?", [2, 5, 10], [2, 5, 10],
        ph=LOWER(["Koala", "Kangaroo", "Wombat", "Echidna", "Platypus"])),
    Ctx("How we travel to school", "Way", ["Walk", "Car", "Bus", "Bike", "Scooter"], STU,
        "How many students {a} to school?", "How many more students {a} to school than {b}?",
        "How many fewer students {a} to school than {b}?", "How many students {a} or {b} to school?",
        "How many students are in the survey altogether?", [5, 10], [5, 10],
        ph={"Walk": "walk", "Car": "come by car", "Bus": "come by bus", "Bike": "ride a bike", "Scooter": "ride a scooter"}),
    Ctx("Birds seen in the schoolyard", "Bird", ["Magpie", "Kookaburra", "Galah", "Lorikeet", "Ibis"], ("bird", "birds"),
        "How many {a} were seen?", "How many more {a} than {b} were seen?",
        "How many fewer {a} than {b} were seen?", "How many {a} and {b} were seen altogether?",
        "How many birds were seen altogether?", [2], [2], maxv=18,
        ph={"Magpie": "magpies", "Kookaburra": "kookaburras", "Galah": "galahs", "Lorikeet": "lorikeets", "Ibis": "ibises"}),
    Ctx("Ice blocks sold at the canteen", "Day", ["Mon", "Tue", "Wed", "Thu", "Fri"], ("ice block", "ice blocks"),
        "How many ice blocks were sold on {a}?", "How many more ice blocks were sold on {a} than on {b}?",
        "How many fewer ice blocks were sold on {a} than on {b}?", "How many ice blocks were sold on {a} and {b} altogether?",
        "How many ice blocks were sold altogether?", [5, 10], [5, 10], ordered=True,
        ph={"Mon": "Monday", "Tue": "Tuesday", "Wed": "Wednesday", "Thu": "Thursday", "Fri": "Friday"}),
    Ctx("Books read this term", "Student", ["Charlotte", "Oliver", "Isla", "Jack", "Mia", "Noah"], ("book", "books"),
        "How many books did {a} read?", "How many more books did {a} read than {b}?",
        "How many fewer books did {a} read than {b}?", "How many books did {a} and {b} read altogether?",
        "How many books did the students read altogether?", [2], [2], maxv=20),
    Ctx("House points", "House", ["Banksia", "Wattle", "Waratah", "Jacaranda"], ("point", "points"),
        "How many points did {a} House get?", "How many more points did {a} House get than {b} House?",
        "How many fewer points did {a} House get than {b} House?", "How many points did {a} and {b} get altogether?",
        "How many points did the houses get altogether?", [10], [10]),
    Ctx("Cans collected for recycling", "Class", ["4A", "4B", "4C", "4D"], ("can", "cans"),
        "How many cans did class {a} collect?", "How many more cans did class {a} collect than {b}?",
        "How many fewer cans did class {a} collect than {b}?", "How many cans did classes {a} and {b} collect altogether?",
        "How many cans did the classes collect altogether?", [5, 10], [5, 10], ordered=True),
    Ctx("Shells found at the beach", "Student", ["Ruby", "Kai", "Zara", "Leo", "Grace"], ("shell", "shells"),
        "How many shells did {a} find?", "How many more shells did {a} find than {b}?",
        "How many fewer shells did {a} find than {b}?", "How many shells did {a} and {b} find altogether?",
        "How many shells did they find altogether?", [2, 5], [2, 5]),
    Ctx("Raffle tickets sold", "Class", ["4A", "4B", "4C", "4D"], ("ticket", "tickets"),
        "How many tickets did class {a} sell?", "How many more tickets did class {a} sell than {b}?",
        "How many fewer tickets did class {a} sell than {b}?", "How many tickets did classes {a} and {b} sell altogether?",
        "How many tickets did the classes sell altogether?", [10], [10], ordered=True),
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
        if "Car" in cats and vals[cats.index("Car")] < sorted(vals)[-2]:
            continue                                # realistic: car is one of the two most common ways
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
        tb = "<b>%s</b> (frequency table): %s. " % (title, ", ".join("%s %d" % (c, v) for c, v in zip(cats, vals)))
    return mcq_fixed(fig(svg) + tb + q, ["A", "B", "C", "D"], pos, e)


def tally_word(v):
    g, r = v // 5, v % 5
    parts = []
    if g:
        parts.append(ones(g, "group") + " of 5")
    if r:
        parts.append(ones(r, "mark"))
    return " and ".join(parts)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


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



def mark_large(u, pattern):
    """Tag pictures that must print larger (graphs, tables, A to D panels) so their labels stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u



# ------------------------------------------------------------ Year 4 versions of the misreading helpers
def pic_wrong(v, key):
    """Real misreadings of one pictograph row."""
    full, hf = v // key, v % key
    out = [full + (1 if hf else 0)]                 # read every symbol as 1
    if hf:
        out += [full * key, (full + 1) * key, full * key + 1]   # ignored the half / half as whole / half as 1
    return out


def bar_wrong(v, scale):
    if v % scale:
        lo = v - v % scale
        return [lo, lo + scale, lo // scale]        # line below / line above / counted grid spaces
    return [v // scale]                             # counted grid spaces


# ------------------------------------------------------------ dot plot
def dot_svg(title, axis, lo, hi, counts):
    """Dot plot: one dot for each answer, stacked above a number line."""
    fs = 14
    gap, r, dy = 34, 6.5, 15
    mx = max(counts.values())
    pw = gap * (hi - lo)
    W = max(26 * 2 + pw, tw(title, 16, True) + 16, tw(axis, fs, True) + 16)
    x0 = (W - pw) / 2
    top = 34
    yb = top + mx * dy + 6
    s = [text(W / 2, 18, title, 16, bold=True)]
    for v in range(lo, hi + 1):
        x = x0 + (v - lo) * gap
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1.5'/>" % (x, yb, x, yb + 6, INK))
        s.append(text(x, yb + 22, v, fs))
        for k in range(counts.get(v, 0)):
            s.append("<circle cx='%.1f' cy='%.1f' r='%.1f' fill='%s'/>" % (x, yb - 9 - k * dy, r, GREEN))
    s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2'/>" % (x0 - 12, yb, x0 + pw + 12, yb, INK))
    s.append(text(W / 2, yb + 44, axis, fs, bold=True))
    assert all(lo <= k <= hi for k in counts)
    return svg_wrap(W, yb + 52, "".join(s), "dot plot: " + title.lower())


# ------------------------------------------------------------ set 1: tally marks and frequency tables
def set_tally(rnd):
    its = []
    # 1-4 count tally marks
    for v in (18, 27, 34, 41):
        its.append(mcq(fig(tally_only_svg(v)) + "What number do these tally marks show?", v, tally_cands(v),
                       "Each group of 5 is four lines with one line across. Count the groups in 5s, then count on the "
                       "single marks: %s" % tally_text(v)))
    # 5 which tally shows 23 (A to D in one picture)
    pos = 2
    order = [28, 22]
    order.insert(pos, 23)
    order.append(24)
    PWT = 236
    s = []
    for k, v in enumerate(order):
        x0, y0 = (k % 2) * PWT, (k // 2) * 44
        s.append(text(x0 + 8, y0 + 27, "ABCD"[k], 17, anchor="start", bold=True))
        s.append(tally_marks(x0 + 34, y0 + 21, v))
        assert x0 + 34 + tally_width(v) < x0 + PWT - 4
    svg = svg_wrap(2 * PWT, 88, "".join(s), "four sets of tally marks")
    wrong = {28: "one group of 5 too many", 22: "one single mark is missing", 24: "one single mark too many"}
    its.append(mcq_fixed(fig(svg) + "Which tally marks show 23?", ["A", "B", "C", "D"], pos,
                         "23 = 5 + 5 + 5 + 5 + 3, so look for 4 groups of 5 and 3 single marks. That is %s. "
                         % "ABCD"[pos] + "; ".join("%s shows %d (%s)" % ("ABCD"[k], v, wrong[v])
                                                    for k, v in enumerate(order) if v != 23) + "."))
    # 6-9 frequency table with tallies: favourite fruit
    cats = ["Apple", "Banana", "Mango", "Orange", "Watermelon"]
    vals = [8, 13, 16, 6, 11]
    f = fig(freq_svg("Favourite fruit in 4B", "Fruit", cats, vals, "frequency table: favourite fruit in 4b", missing=2))
    its.append(mcq(f + "What number should go in the Frequency column for Mango?", 16, tally_cands(16, [13, 11]),
                   "The frequency is the number the tally marks show. Mango has %s" % tally_text(16)))
    its.append(mcq(f + "Which fruit got the fewest votes?", "Orange", ["Apple", "Watermelon", "Banana"],
                   "Orange has the shortest tally: 1 group of 5 and 1 more, so 6 votes. Apple has 8, the next fewest."))
    its.append(mcq(f + "How many more votes did Mango get than Watermelon?", fmt(5, VOTE),
                   [fmt(x, VOTE) for x in [27, 2, 16, 11]],
                   "Mango 16 (3 groups of 5 and 1 more). Watermelon 11. How many more means subtract: 16 − 11 = 5. "
                   "(Counting each tally group as 4 makes Mango 13, and 13 − 11 = 2.)"))
    tot = sum(vals)
    its.append(mcq(f + "Every student in 4B voted once. How many students are in 4B?", fmt(tot, STU),
                   [fmt(x, STU) for x in [tot - 16, sum((v // 5) * 4 + v % 5 for v in vals), tot - 1, tot + 1]],
                   "Find the Mango frequency first: 16. Then add all the rows: 8 + 13 + 16 + 6 + 11 = %d." % tot))
    # 10-13 discrete numerical data: pets at home
    cats = ["0", "1", "2", "3", "4"]
    vals = [5, 9, 7, 3, 2]
    f = fig(freq_svg("Number of pets at home: 4C", "Pets", cats, vals, "frequency table: number of pets at home",
                     tally=False))
    its.append(mcq(f + "How many students have 2 pets?", fmt(7, STU), [fmt(x, STU) for x in [2, 9, 3, 5]],
                   "Find the row for 2 pets. The frequency is 7, so 7 students have 2 pets. "
                   "The 2 is the number of pets, not the number of students."))
    its.append(mcq(f + "What is the most common number of pets?", "1 pet", ["9 pets", "4 pets", "2 pets"],
                   "The biggest frequency is 9, in the row for 1 pet. So 1 pet is the most common answer. "
                   "9 is how many students, not how many pets."))
    its.append(mcq(f + "How many students answered the survey?", fmt(26, STU), [fmt(x, STU) for x in [10, 5, 21, 9]],
                   "Add the frequencies: 5 + 9 + 7 + 3 + 2 = 26 students. "
                   "(10 adds the numbers of pets, 0 + 1 + 2 + 3 + 4. 21 leaves out the students with no pets.)"))
    its.append(mcq(f + "How many students have more than 2 pets?", fmt(5, STU), [fmt(x, STU) for x in [12, 3, 21]],
                   "More than 2 means 3 or 4 pets: 3 + 2 = 5 students. Do not include the students with exactly 2 pets "
                   "(that gives 12)."))
    # 14-16 table with a total and a missing value
    cats = ["4A", "4B", "4C", "4D"]
    vals = [34, 38, 27, 41]
    f = fig(freq_svg("Cans collected for recycling", "Class", cats, vals, "frequency table: cans collected for recycling",
                     tally=False, missing=1, total=True))
    its.append(mcq(f + "How many cans did 4B collect?", fmt(38, ("can", "cans")),
                   [fmt(x, ("can", "cans")) for x in [102, 242, 42]],
                   "Add the classes you know: 34 + 27 + 41 = 102. The total is 140, so 4B collected 140 − 102 = 38. "
                   "(242 adds instead of subtracting. 42 comes from taking 0 from 2 in the ones.)"))
    its.append(mcq(f + "Which class collected 7 more cans than 4C?", "4A", ["4B", "4D", "4C"],
                   "4C collected 27. 7 more is 27 + 7 = 34. 4A collected 34."))
    its.append(mcq(f + "How many more cans did 4D collect than 4C?", fmt(14, ("can", "cans")),
                   [fmt(x, ("can", "cans")) for x in [68, 26, 41]],
                   "4D 41, 4C 27. How many more means subtract: 41 − 27 = 14. "
                   "(26 comes from taking 1 from 7 in the ones instead of regrouping. 68 is the sum.)"))
    # 17-18 categorical and numerical data
    its.append(mcq("Which survey question gives numerical data (answers that are numbers)?",
                   "How many books did you read last week?",
                   ["What is your favourite sport?", "How do you get to school?", "Which house are you in?"],
                   "“How many books did you read last week?” has number answers, such as 0, 2 or 5. The other questions "
                   "have answers that are categories (words), such as netball, bus or Wattle."))
    its.append(mcq("Which survey question gives categorical data (answers that are words, not numbers)?",
                   "What is your favourite season?",
                   ["How many pets do you have?", "How many people live in your house?",
                    "How many minutes do you read each night?"],
                   "Favourite season gives answers like summer or winter. These are categories. "
                   "The other questions ask “how many”, so the answers are numbers."))
    # 19-20 word problems about tallies
    its.append(mcq("Cooper makes a tally of the cars that pass the school gate. He draws 6 groups of five and 4 single marks. "
                   "How many cars has he counted?", fmt(34, ("car", "cars")),
                   [fmt(x, ("car", "cars")) for x in [28, 10, 35, 64]],
                   "6 groups of five: 6 × 5 = 30. Then 4 more: 30 + 4 = 34 cars. "
                   "(Counting each group as 4 gives 24 + 4 = 28.)"))
    its.append(mcq("Ruby counted 23 votes for netball. How should she draw the tally?", "4 groups of five and 3 marks",
                   ["3 groups of five and 8 marks", "2 groups of five and 3 marks", "5 groups of five and 3 marks"],
                   "23 = 5 + 5 + 5 + 5 + 3. Draw 4 groups of five (four lines and one across) and 3 single marks. "
                   "Never leave 5 or more single marks: make another group of five. (2 groups and 3 marks is only 13.)"))
    assert len(its) == 20
    return {"title": "Tally marks and frequency tables", "items": its}


# ------------------------------------------------------------ set 2: many-to-one pictographs
def set_pictograph(rnd, PK):
    its = []
    plan = [(2, "read"), (2, "readh"), (2, "half"), (2, "most"), (2, "more"), (2, "which"),
            (5, "read"), (5, "draw"), (5, "read"), (5, "fewest"), (5, "more"), (5, "total"),
            (10, "read"), (10, "readh"), (10, "half"), (10, "draw"), (10, "which"), (10, "readh"), (10, "more"),
            (10, "total")]
    draws = iter([("Each star stands for 5 votes. Netball got 40 votes. How many stars should be in the Netball row?",
                   40, 5, "star"),
                  ("Each circle stands for 10 students. 45 students ride a bike to school. "
                   "What should the Bike row show?", 45, 10, "circle")])
    for i, (key, kind) in enumerate(plan):
        sym = SYMS[i % 3]
        if kind == "draw":
            q, v, k, sym = next(draws)
            assert k == key
            full, hf = v // key, v % key
            ans = halfs(v, key, sym)
            if hf:
                cand = [ones(v, sym), ones(full + 1, sym), ones(full, sym), ones(v // 5, sym)]
                e = ("%d = %d + %d. %d is %s (%d × %d = %d). %d is half of %d, so add half a %s. Draw %s. "
                     "(Drawing %s would mean each %s stands for 1.)"
                     % (v, full * key, hf, full * key, ones(full, sym), full, key, full * key, hf, key, sym, ans,
                        ones(v, sym), sym))
            else:
                cand = [ones(v, sym), ones(full + 1, sym), ones(full - 1, sym), ones(v // 10, sym)]
                e = ("Count in %ds until you reach %d: %s. That is %s, so draw %s. Check: %d × %d = %d. "
                     "(Drawing %s would mean each %s stands for 1.)"
                     % (key, v, ", ".join(str(key * t) for t in range(1, full + 1)), ones(full, "step"), ans, full, key,
                        v, ones(v, sym), sym))
            its.append(mcq(q, ans, cand, e))
            continue
        ctx = PK.next(lambda c: key in c.pkeys)
        half = (key == 10) or (key == 2 and kind in ("readh", "half", "which"))
        n = 5 if i % 4 == 3 and len(ctx.cats) >= 5 else 4
        okh = (lambda vs: any(v % key and v > key for v in vs)) if half else (lambda vs: max(vs) - min(vs) >= 2 * key)
        cats, vals = make_data(ctx, n, key, half, rnd, max_units={2: 9, 5: 8, 10: 7}[key], min_units=1, ok=okh)
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
            cand = pic_wrong(v, key) + [v + key, v - key] + others + [v * 2]
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
                           [fmt(x, U) for x in [1, key, key * 2, 3]],
                           "The key says one whole %s = %s. Half a %s is half of %d, which is %s. "
                           "(Half a symbol is not always 1: it is half of the key.)"
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
            pairs = [(a, b) for a in range(n) for b in range(n) if vals[a] - vals[b] >= 2 * key]
            a, b = rnd.choice(pairs)
            d = vals[a] - vals[b]
            nd = math.ceil(vals[a] / key) - math.ceil(vals[b] / key)
            cand = [vals[a] + vals[b], nd, d + key, d - key, vals[a], d + 1]
            its.append(mcq(f + ctx.more(cats[a], cats[b]), fmt(d, U), [fmt(x, U) for x in cand],
                           "%s%s and %s. How many more means find the difference: %d − %d = %s."
                           % (keytxt, "%s: %s" % (cats[a], short_pic(vals[a], key)),
                              "%s: %s" % (cats[b], short_pic(vals[b], key)), vals[a], vals[b], fmt(d, U))))
        else:
            t = sum(vals)
            nsym = sum(math.ceil(v / key) for v in vals)
            nohalf = sum(v - v % key for v in vals)
            cand = [nsym, nohalf, t - min(vals), t + key, t - key]
            its.append(mcq(f + ctx.total, fmt(t, U), [fmt(x, U) for x in cand],
                           "%sRead every row: %s. Add them: %s = %s."
                           % (keytxt, ", ".join("%s %d" % (c, v) for c, v in zip(cats, vals)),
                              " + ".join(str(v) for v in vals), fmt(t, U))))
    assert len(its) == 20
    return {"title": "Pictographs: 1 symbol = 2, 5 or 10", "items": its}


# ------------------------------------------------------------ set 3: column graphs
def set_column(rnd, PK):
    its = []
    plan = [(2, "step"), (2, "read"), (2, "readh"), (2, "which"), (2, "most"), (2, "more"),
            (5, "step"), (5, "read"), (5, "read"), (5, "fewest"), (5, "more"), (5, "both"),
            (10, "step"), (10, "read"), (10, "readh"), (10, "readh"), (10, "which"), (10, "more"), (10, "both"),
            (10, "most")]
    for i, (sc, kind) in enumerate(plan):
        ctx = PK.next(lambda c: sc in c.scales)
        half = (sc == 10 and kind != "step") or (sc == 2 and kind in ("readh", "which", "more"))
        n = 5 if (i % 3 == 0 and len(ctx.cats) >= 5) else 4
        okh = (lambda vs: any(v % sc and v > sc for v in vs)) if half else (lambda vs: True)
        cats, vals = make_data(ctx, n, sc, half, rnd, max_units={2: 9, 5: 8, 10: 8}[sc], min_units=1, ok=okh)
        f = fig(ctx_bar(ctx, cats, vals, sc))
        U = ctx.unit
        scl = "The scale goes up in %ds. " % sc
        if kind in ("read", "readh"):
            if kind == "readh":
                j = rnd.choice([k for k, v in enumerate(vals) if v % sc])
            else:
                j = rnd.randrange(n)
            c, v = cats[j], vals[j]
            others = [vals[k] for k in range(n) if k != j]
            cand = bar_wrong(v, sc) + [v + sc, v - sc] + others + [v + 1]
            its.append(mcq(f + ctx.ask(c), fmt(v, U), [fmt(x, U) for x in cand],
                           "%s%s So the answer is %s." % (scl, read_bar(c, v, sc), fmt(v, U))))
        elif kind == "step":
            its.append(mcq(f + "What does the scale on this column graph go up in?", "%ds" % sc,
                           ["%ds" % x for x in (1, 2, 5, 10) if x != sc],
                           "Read the numbers on the scale: 0, %d, %d, %d … Each line is %d more than the one before, "
                           "so the scale goes up in %ds. Each gridline is worth %d, not 1." % (sc, 2 * sc, 3 * sc, sc, sc, sc)))
        elif kind == "which":
            j = rnd.choice([k for k, v in enumerate(vals) if v % sc]) if half else rnd.randrange(n)
            v = vals[j]
            near = sorted([k for k in range(n) if k != j], key=lambda k: abs(vals[k] - v))
            its.append(mcq(f + "Which column shows %s?" % fmt(v, U), cats[j], [cats[k] for k in near],
                           "%sFind %d on the scale. %s" % (scl, v, read_bar(cats[j], v, sc))))
        elif kind in ("most", "fewest"):
            j = vals.index(max(vals) if kind == "most" else min(vals))
            word = "tallest" if kind == "most" else "shortest"
            q = "Which column shows the %s %s?" % ("most" if kind == "most" else "fewest", U[1])
            its.append(mcq(f + q, cats[j], [cats[k] for k in range(n) if k != j],
                           "The column for %s is the %s one. %s" % (cats[j], word, read_bar(cats[j], vals[j], sc))))
        elif kind == "more":
            pairs = [(a, b) for a in range(n) for b in range(n) if vals[a] - vals[b] >= 2 * sc
                     and (not half or vals[a] % sc or vals[b] % sc)]
            a, b = rnd.choice(pairs)
            d = vals[a] - vals[b]
            mis = []
            if vals[b] % sc:
                mis.append(vals[a] - (vals[b] - vals[b] % sc))
            if vals[a] % sc:
                mis.append(vals[a] - vals[a] % sc - vals[b])
            spaces = [d // sc] if d % sc == 0 else []
            cand = [vals[a] + vals[b]] + mis + spaces + [d + sc, d - sc, vals[a], d + 1]
            its.append(mcq(f + ctx.more(cats[a], cats[b]), fmt(d, U), [fmt(x, U) for x in cand],
                           "%s%s: %d. %s: %d. How many more means find the difference: %d − %d = %s."
                           % (scl, cats[a], vals[a], cats[b], vals[b], vals[a], vals[b], fmt(d, U))))
        else:
            a, b = rnd.sample(range(n), 2)
            t = vals[a] + vals[b]
            lowsum = vals[a] - vals[a] % sc + vals[b] - vals[b] % sc
            cand = [abs(vals[a] - vals[b]), lowsum, t // sc, t + sc, t - sc, t + 10]
            its.append(mcq(f + ctx.both(cats[a], cats[b]), fmt(t, U), [fmt(x, U) for x in cand],
                           "%s%s: %d. %s: %d. Altogether means add: %d + %d = %s."
                           % (scl, cats[a], vals[a], cats[b], vals[b], vals[a], vals[b], fmt(t, U))))
    assert len(its) == 20
    return {"title": "Column graphs with scales of 2, 5 and 10", "items": its}


# ------------------------------------------------------------ set 4: compare displays and dot plots
BOOKS = {0: 2, 1: 4, 2: 6, 3: 5, 4: 3, 5: 2, 7: 1}
SIBS = {0: 4, 1: 9, 2: 6, 3: 3, 5: 2}


def books_dot():
    return dot_svg("Books read last week: 4C", "Number of books", 0, 7, BOOKS)


def sibs_dot():
    return dot_svg("Brothers and sisters: 4A", "Number of brothers and sisters", 0, 5, SIBS)


def set_compare(rnd):
    its = []
    # 1-4 choose a key or a scale
    its.append(mcq("Mia will draw a pictograph of these votes: 40, 25, 35 and 50. She wants whole symbols only, "
                   "and as few symbols as she can. Which key should she use?", "1 symbol = 5 votes",
                   ["1 symbol = 1 vote", "1 symbol = 2 votes", "1 symbol = 10 votes"],
                   "Every number is in the 5 times table, so a key of 5 gives whole symbols: 8, 5, 7 and 10. "
                   "A key of 10 or 2 would need half symbols for 25 and 35. A key of 1 needs 150 symbols."))
    its.append(mcq("Jack will draw a pictograph of 60, 90, 40 and 70 students. He wants whole symbols only, "
                   "and as few symbols as he can. Which key should he use?", "1 symbol = 10 students",
                   ["1 symbol = 1 student", "1 symbol = 2 students", "1 symbol = 5 students"],
                   "Every number is a multiple of 10, so a key of 10 gives whole symbols: 6, 9, 4 and 7 (26 symbols). "
                   "A key of 5 also works, but it needs twice as many symbols (52)."))
    its.append(mcq("Kai will draw a column graph of 12, 18, 6 and 14 votes. Every column must end exactly on a gridline, "
                   "and he wants no more than 10 gridlines above 0. What should the scale go up in?", "2s",
                   ["1s", "5s", "10s"],
                   "Counting in 1s needs 18 gridlines, which is too many. Counting in 2s needs 9 gridlines (2 to 18), "
                   "and every number is even, so every column ends on a line. In 5s or 10s, 12, 18, 6 and 14 would end "
                   "between lines."))
    its.append(mcq("Isla will draw a column graph of 35, 50, 20 and 45 tickets. Every column must end exactly on a gridline, "
                   "and she wants no more than 10 gridlines above 0. What should the scale go up in?", "5s",
                   ["1s", "2s", "10s"],
                   "Counting in 5s needs 10 gridlines (5 to 50), and every number is in the 5 times table. "
                   "1s or 2s need far too many lines (50 or 25). In 10s, 35 and 45 would end halfway between lines."))
    # 5-7 which display shows the same data (A to D)
    its.append(match_q(rnd, 2, "Raffle tickets sold", ["4A", "4B", "4C", "4D"], [45, 70, 30, 55], 10,
                       ("ticket", "tickets")))
    its.append(match_q(rnd, 0, "Ice blocks sold", ["Mon", "Tue", "Wed", "Thu"], [20, 30, 15, 25], 5,
                       ("ice block", "ice blocks"), pic=True, sym="square"))
    its.append(match_q(rnd, 3, "Favourite animal", ["Koala", "Emu", "Wombat", "Echidna"], [35, 50, 20, 40], 10,
                       VOTE, pic=True, sym="star"))
    # 8-9 pictograph and column graph of the same data, one column missing
    P = [(BYTITLE["Raffle tickets sold"], ["4A", "4B", "4C", "4D"], [45, 60, 35, 50], 10, 2, "circle", 10),
         (BYTITLE["Books read this term"], ["Isla", "Jack", "Mia", "Noah"], [9, 14, 7, 12], 2, 0, "star", 2)]
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
    # 10-14 dot plot: books read
    f = fig(books_dot())
    n_b = sum(BOOKS.values())
    its.append(mcq(f + "How many students read 3 books?", fmt(5, STU), [fmt(x, STU) for x in [3, 6, 4]],
                   "Each dot is one student. Count the dots above 3: there are 5. "
                   "(3 is the number of books, not the number of students.)"))
    its.append(mcq(f + "How many students are shown on the dot plot?", fmt(n_b, STU),
                   [fmt(x, STU) for x in [7, 28, n_b - 1]],
                   "Each dot is one student, so count every dot: 2 + 4 + 6 + 5 + 3 + 2 + 1 = %d. "
                   "(7 counts the stacks, and 28 adds the numbers on the line.)" % n_b))
    its.append(mcq(f + "What is the most common number of books read?", "2 books", ["6 books", "7 books", "3 books"],
                   "The tallest stack of dots is above 2 (6 dots). So 2 books is the most common answer. "
                   "6 is how many students, not how many books."))
    its.append(mcq(f + "How many students read more than 4 books?", fmt(3, STU), [fmt(x, STU) for x in [6, 2, 1]],
                   "More than 4 means 5, 6 or 7 books. There are 2 dots above 5, none above 6 and 1 above 7: "
                   "2 + 1 = 3. (6 also counts the students who read exactly 4.)"))
    its.append(mcq(f + "Which statement is true?", "More students read 1 book than 5 books.",
                   ["Most students read 7 books.", "Every student read at least 1 book.",
                    "The same number of students read 2 books and 3 books."],
                   "1 book has 4 dots and 5 books has 2 dots, so this is true. Only 1 student read 7 books. "
                   "2 students read 0 books. 2 books has 6 dots and 3 books has 5."))
    # 15-17 dot plot: brothers and sisters
    f = fig(sibs_dot())
    its.append(mcq(f + "How many students have no brothers or sisters?", fmt(4, STU), [fmt(x, STU) for x in [9, 6, 24]],
                   "No brothers or sisters means the answer 0. There are 4 dots above 0."))
    its.append(mcq(f + "How many students have 2 or more brothers and sisters?", fmt(11, STU),
                   [fmt(x, STU) for x in [5, 20, 3]],
                   "2 or more means 2, 3, 4 or 5: 6 + 3 + 0 + 2 = 11. "
                   "(5 leaves out the students with exactly 2.)"))
    its.append(mcq(f + "How many more students have 1 brother or sister than have 3?", fmt(6, STU),
                   [fmt(x, STU) for x in [12, 2, 3]],
                   "Above 1 there are 9 dots. Above 3 there are 3 dots. 9 − 3 = 6. "
                   "(2 is 3 − 1, the numbers on the line, not the dots.)"))
    # 18 choose the display
    its.append(mcq("Grace asked 4A, “How many brothers and sisters do you have?” She wants to show each answer as one dot "
                   "above a number line. Which display should she use?", "A dot plot",
                   ["A pictograph", "A column graph", "A tally"],
                   "A dot plot has a number line, and each answer is one dot above its number. It suits numerical "
                   "data such as 0, 1, 2 or 3 brothers and sisters."))
    # 19-20 two column graphs with different scales
    cats = ["4A", "4B", "4C", "4D"]
    vals = [20, 35, 40, 25]
    pa = bar_part("Graph A", "Class", "Cans", cats, vals, 5)
    pb = bar_part("Graph B", "Class", "Cans", cats, vals, 10, col=BAR2)
    f = fig(side_by_side([pa, pb], "two column graphs: cans collected, two scales"))
    its.append(mcq(f + "Kai says Graph B shows fewer cans than Graph A because its columns are shorter. Is he right?",
                   "No. Both graphs show the same numbers.",
                   ["Yes. The columns in Graph B are shorter.", "Yes. Graph B has fewer gridlines.",
                    "No. Graph B shows more cans."],
                   "Graph A goes up in 5s and Graph B goes up in 10s. Read both: 4A 20, 4B 35, 4C 40, 4D 25. "
                   "The numbers are the same; only the scale is different. Always read the scale, not the height."))
    its.append(mcq(f + "Read Graph B. How many cans did 4B collect?", fmt(35, ("can", "cans")),
                   [fmt(x, ("can", "cans")) for x in [3, 30, 40]],
                   "Graph B goes up in 10s. The 4B column ends halfway between 30 and 40, so it shows 35. "
                   "(3 counts the grid spaces. Graph A shows 35 too.)"))
    assert len(its) == 20, len(its)
    return {"title": "Compare displays and read dot plots", "items": its}


# ------------------------------------------------------------ set 5: surveys, conclusions and word problems
SP_C = ["AFL", "Cricket", "Netball", "Soccer", "Swimming"]
SP_V = [25, 15, 30, 20, 10]
TR_C = ["Walk", "Car", "Bus", "Bike", "Scooter"]
TR_V = [45, 80, 35, 20, 15]
BK_C = ["0", "1", "2", "3", "4", "5"]
BK_V = [2, 5, 8, 6, 3, 1]


def set_words(rnd):
    its = []
    S = STU
    sport = fig(bar_svg("Favourite sport in Year 4", "Sport", "Students", SP_C, SP_V, 5,
                        label="column graph: favourite sport in year 4"))
    its.append(mcq(sport + "How many more students chose netball than cricket?", fmt(15, S),
                   [fmt(x, S) for x in [45, 3, 5]],
                   "The scale goes up in 5s. Netball 30, cricket 15. How many more means subtract: 30 − 15 = 15. "
                   "(3 counts the grid spaces between the tops of the columns.)"))
    its.append(mcq(sport + "Every Year 4 student voted once. How many students are in Year 4?", fmt(100, S),
                   [fmt(x, S) for x in [20, 90, 95]],
                   "Read every column: 25 + 15 + 30 + 20 + 10 = 100. "
                   "(20 counts grid spaces: 5 + 3 + 6 + 4 + 2.)"))
    its.append(mcq(sport + "Which conclusion is supported by the graph?",
                   "More Year 4 students chose netball than any other sport.",
                   ["Every Year 4 student plays netball.", "No Year 4 students like swimming.",
                    "Most children in Australia like AFL best."],
                   "Netball has the tallest column (30), so this is supported. The survey asked about favourites, "
                   "not who plays. 10 students chose swimming. The survey only asked Year 4, not all of Australia."))
    its.append(mcq(sport + "Cooper says, “Twice as many students chose AFL as chose swimming.” Is he right?",
                   "No. Twice 10 is 20, but AFL got 25.",
                   ["Yes. AFL got 25 and swimming got 10.", "No. AFL got 5 and swimming got 2.",
                    "Yes. AFL is the most popular sport."],
                   "Swimming 10, AFL 25. Twice 10 is 20, and 25 is more than 20, so he is not right. "
                   "(5 and 2 are grid spaces, not students.)"))
    its.append(mcq(sport + "The school will buy new equipment for the two most popular sports. Which two?",
                   "Netball and AFL", ["Netball and soccer", "AFL and soccer", "Cricket and swimming"],
                   "The two tallest columns are netball (30) and AFL (25). Soccer is 20."))
    travel = fig(part_svg(pic_part("How students travel to school", TR_C, TR_V, 10, "circle", S),
                          "pictograph: how students travel to school"))
    its.append(mcq(travel + "How many students come to school by car?", fmt(80, S), [fmt(x, S) for x in [8, 70, 85]],
                   "Each circle stands for 10 students. The Car row has 8 circles: 8 × 10 = 80. "
                   "(8 reads each circle as 1 student.)"))
    its.append(mcq(travel + "How many more students come by car than walk?", fmt(35, S),
                   [fmt(x, S) for x in [125, 40, 45]],
                   "Car: 8 circles = 80. Walk: 4 circles and half a circle = 40 + 5 = 45. 80 − 45 = 35. "
                   "(Leaving out the half circle gives 80 − 40 = 40.)"))
    its.append(mcq(travel + "How many students walk, ride a bike or ride a scooter?", fmt(80, S),
                   [fmt(x, S) for x in [70, 195, 8]],
                   "Walk 45, Bike 20, Scooter 15 (1 circle and half a circle). 45 + 20 + 15 = 80. "
                   "(Leaving out the half circles gives 40 + 20 + 10 = 70. 8 counts the circles.)"))
    its.append(mcq(travel + "Next term, 20 students who come by car will walk instead. What should the Walk row show then?",
                   "6 and a half circles", ["65 circles", "6 circles", "2 circles"],
                   "Walk now: 45. 45 + 20 = 65 students. 65 = 60 + 5: 6 circles for 60 and half a circle for 5."))
    its.append(mcq(travel + "Which conclusion is supported by the pictograph?",
                   "More students come by car than walk and ride a scooter together.",
                   ["Most students walk to school.", "No students come to school by train.",
                    "The bus is the least common way to travel."],
                   "Car 80. Walk and scooter: 45 + 15 = 60. 80 is more, so this is supported. Walking (45) is not most of "
                   "the 195 students. Train was not in the survey, so we cannot tell. Scooter (15) is the least common."))
    books = fig(freq_svg("Books read in the holidays: 4D", "Books read", BK_C, BK_V,
                         "frequency table: books read in the holidays"))
    its.append(mcq(books + "How many students read at least 3 books?", fmt(10, S), [fmt(x, S) for x in [4, 21, 6]],
                   "At least 3 means 3, 4 or 5 books: 6 + 3 + 1 = 10 students. "
                   "(4 leaves out the students who read exactly 3. 21 is the students who read 3 or fewer.)"))
    tb = sum(int(c) * v for c, v in zip(BK_C, BK_V))
    its.append(mcq(books + "How many books did these students read altogether?", fmt(tb, ("book", "books")),
                   [fmt(x, ("book", "books")) for x in [25, 15, tb - 5]],
                   "Multiply each number of books by its frequency: 0 × 2 + 1 × 5 + 2 × 8 + 3 × 6 + 4 × 3 + 5 × 1 "
                   "= 0 + 5 + 16 + 18 + 12 + 5 = %d. (25 is the number of students, and 15 adds 0 + 1 + 2 + 3 + 4 + 5.)" % tb))
    its.append(mcq(books + "Which conclusion is supported by the table?", "Most students in 4D read 2 or 3 books.",
                   ["Every student in 4D read at least one book.", "4D read more books than every other class.",
                    "Nobody read 6 books because the books were too long."],
                   "2 or 3 books: 8 + 6 = 14 of the 25 students, which is more than half. 2 students read 0 books. "
                   "The table has no data about other classes, and it does not tell us why."))
    its.append(mcq(books + "The teacher says, “More than half the class read 2 or more books.” Is she right?",
                   "Yes. 18 of the 25 students did.",
                   ["No. Only 8 students read 2 books.", "No. 7 students read fewer than 2 books.",
                    "Yes. 25 students answered."],
                   "2 or more books: 8 + 6 + 3 + 1 = 18 students. Half of 25 is 12 and a half, and 18 is more, "
                   "so she is right."))
    # planning a survey and using a spreadsheet
    its.append(mcq("Zara wants to know which ice block flavour the canteen should sell. Which survey question is best?",
                   "Which flavour would you choose: lemon, raspberry, mango or cola?",
                   ["Do you like ice blocks?", "How many ice blocks are in the freezer?",
                    "Raspberry is the best flavour, isn’t it?"],
                   "The best question matches the purpose and gives clear answers to count. "
                   "“Do you like ice blocks?” does not tell her the flavour, and the last question pushes people to "
                   "say raspberry."))
    its.append(mcq("Ethan wants to find out how Year 4 students travel to school. Who should he ask?",
                   "All the Year 4 students", ["Only his three best friends", "Only the students on the bus",
                                               "Students at another school"],
                   "To answer a question about Year 4, collect data from Year 4. Asking only friends or only bus "
                   "students would give answers that do not show the whole of Year 4."))
    its.append(mcq("Mia types the house points into a spreadsheet: Banksia 40, Wattle 65, Waratah 50, Jacaranda 55. "
                   "Her column graph goes up in 10s. Where is the top of the Wattle column?", "Halfway between 60 and 70",
                   ["On the line for 60", "On the line for 70", "On the 65th gridline"],
                   "The gridlines go 0, 10, 20 … There is no line for 65. 65 is halfway between 60 and 70."))
    its.append(mcq("Mia also wants a pictograph of the house points (40, 65, 50 and 55). She can use whole and half "
                   "symbols, and she wants as few symbols as she can. Which key should she use?", "1 symbol = 10 points",
                   ["1 symbol = 1 point", "1 symbol = 2 points", "1 symbol = 5 points"],
                   "With a key of 10: 4, 6 and a half, 5 and 5 and a half symbols (21 symbols). A key of 5 needs 42 "
                   "symbols, and a key of 1 or 2 needs even more."))
    its.append(mcq(sport + "How many more students chose netball or soccer than chose AFL or cricket?", fmt(10, S),
                   [fmt(x, S) for x in [90, 50, 2]],
                   "Step 1: netball or soccer: 30 + 20 = 50. Step 2: AFL or cricket: 25 + 15 = 40. "
                   "Step 3: 50 − 40 = 10. (2 counts grid spaces.)"))
    its.append(mcq(travel + "The school bike racks hold 30 bikes. All the students who ride a bike park there. "
                   "How many spaces are left?", fmt(10, ("space", "spaces")),
                   [fmt(x, ("space", "spaces")) for x in [28, 50, 20]],
                   "The Bike row has 2 circles: 2 × 10 = 20 bikes. 30 − 20 = 10 spaces. "
                   "(28 reads each circle as 1 bike.)"))
    assert len(its) == 20
    return {"title": "Surveys and conclusions: word problems", "items": its}


# ------------------------------------------------------------ lesson
LS_C = ["AFL", "Cricket", "Netball", "Soccer"]
LS_V = [35, 20, 45, 30]


def body_html():
    return (
        "<h2>Ask a question, then collect data</h2>"
        "<p>Start with a question, such as “How do Year 4 students travel to school?”. "
        "Then ask the right people and record every answer. "
        "Some data is in <b>categories</b> (words, such as bus or netball). "
        "Some data is <b>numerical</b> (numbers, such as how many books you read).</p>"
        "<p>Record the answers with <b>tally marks</b> or in a spreadsheet, and write the totals in a "
        "<b>frequency table</b>. Then show the data in a <b>pictograph</b>, a <b>column graph</b> or a <b>dot plot</b>.</p>"
        "<h2>Tally marks and frequency tables</h2>"
        "<p>Draw one mark for each answer. The fifth mark goes across the other four. "
        "Count the groups in 5s, then add the single marks. The <b>frequency</b> is how many.</p>"
        "<figure class='sn-fig'>" + tally_only_svg(17) +
        "<figcaption>3 groups of 5 and 2 marks: 15 + 2 = 17.</figcaption></figure>"
        "<h2>Many-to-one pictographs</h2>"
        "<p>In Year 4, one symbol stands for <b>many</b>: 2, 5 or 10. Read the <b>key</b> first. "
        "Count the symbols in 2s, 5s or 10s. Half a symbol is half of the key: if one symbol = 10, half = 5.</p>"
        "<figure class='sn-fig'>" + part_svg(pic_part("Favourite sport in Year 4", LS_C, LS_V, 10, "circle", STU),
                                             "pictograph: favourite sport in year 4") +
        "<figcaption>Each circle = 10 students. AFL: 3 circles = 30, and half a circle = 5, so 35.</figcaption></figure>" +
        ex("Example", "How many more students chose netball than soccer?",
           "Netball: 4 circles and a half = 45. Soccer: 3 circles = 30. 45 − 30 = 15.", "15 students") +
        "<h2>Column graphs</h2>"
        "<p>Find what the <b>scale</b> goes up in: 2s, 5s or 10s. Go across from the top of the column to the scale. "
        "If a column ends halfway between two gridlines, the number is halfway between them.</p>"
        "<figure class='sn-fig'>" + bar_svg("Favourite sport in Year 4", "Sport", "Students", LS_C, LS_V, 10,
                                            label="column graph: favourite sport in year 4") +
        "<figcaption>The scale goes up in 10s. Netball ends halfway between 40 and 50, so 45.</figcaption></figure>"
        "<p>The pictograph and the column graph show the same data. To check two displays, read every category in both.</p>"
        "<h2>Dot plots</h2>"
        "<p>A dot plot shows numerical data. Each answer is one dot above a number line. "
        "The tallest stack is the most common answer.</p>"
        "<figure class='sn-fig'>" + books_dot() +
        "<figcaption>6 students read 2 books. Count every dot to find how many students: 23.</figcaption></figure>"
        "<h2>Make conclusions the data supports</h2>"
        "<p>A conclusion must match the numbers and the people you asked.</p>" +
        table(["Conclusion", "Supported?"], [
            ["Netball got the most votes in Year 4.", "Yes: it has the tallest column."],
            ["Netball got 15 more votes than soccer.", "Yes: 45 − 30 = 15."],
            ["Every Australian child likes netball best.", "No: only Year 4 was asked."],
            ["Nobody likes cricket.", "No: 20 students chose it."],
        ]) +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Reading each symbol as 1", "Use the key: 4 circles of 10 = 40"],
            ["Saying half a symbol = 1", "Half a symbol is half of the key"],
            ["Counting grid spaces instead of reading the scale", "Read the number on the scale"],
            ["Reading a column between gridlines as the lower line", "Halfway between 30 and 40 is 35"],
            ["Counting the stacks on a dot plot", "Count every dot: one dot is one answer"],
            ["Making a conclusion about people who were not asked", "Only talk about the data you collected"],
        ])
    )


FAQ = [
    {"q": "What do Year 4 students learn about data in the Australian Curriculum?",
     "a": "They collect categorical and numerical data, record it in tables or spreadsheets, and show it in many-to-one pictographs, column graphs and dot plots. They then interpret the displays and discuss what the data shows."},
    {"q": "What is a many-to-one pictograph?",
     "a": "It is a pictograph where one symbol stands for more than one, such as 2, 5 or 10. You use the key to work out each row, so 3 symbols with a key of 10 means 30."},
    {"q": "How do you choose a scale for a column graph?",
     "a": "Look at the biggest number and choose a scale (such as 2s, 5s or 10s) that fits it in about 10 gridlines. If the numbers are all multiples of the scale, every column ends exactly on a line."},
    {"q": "What is the difference between categorical and numerical data?",
     "a": "Categorical data is words or groups, such as favourite sport or how you travel to school. Numerical data is numbers, such as how many books you read or how many pets you have."},
]


def gen_unit():
    rnd = random.Random(4819)
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
        "country": "au", "subject": "maths", "grade": "year-4", "slug": "data-and-graphs", "sort": 19,
        "updated": UPDATED, "pdf_url": "",
        "title": "Data and Graphs: Pictographs, Column Graphs and Dot Plots",
        "seo_title": "Year 4 Data and Graphs Worksheets: Pictographs, Column Graphs and Dot Plots (Free, with Answer Key)",
        "short_title": "Data and graphs",
        "domain": "Statistics",
        "standard_code": "AC9M4ST01",
        "standard_url": "https://v9.australiancurriculum.edu.au/f-10-curriculum/learning-areas/mathematics",
        "standard_text": "Acquire data for categorical and discrete numerical variables to address a question of interest or purpose, using digital tools; represent data using many-to-one pictographs, column graphs and other displays or visualisations; interpret and discuss the information that has been created",
        "meta_desc": "Free Year 4 maths worksheets on data and graphs for the Australian Curriculum: tally marks and frequency tables, many-to-one pictographs (1 symbol = 2, 5 or 10), column graphs with scales of 2, 5 and 10, dot plots and survey conclusions. 100 questions with an answer key.",
        "key_big": "Read the key or the scale first. One symbol or one gridline is often worth more than 1.",
        "key_sub": "If one symbol = 10, half a symbol = 5. A column halfway between 30 and 40 shows 35. A conclusion must match the data and the people you asked.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen_unit()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        mark_large(u, "(pictograph|column graph|frequency table|two column|four sets|dot plot)")
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
