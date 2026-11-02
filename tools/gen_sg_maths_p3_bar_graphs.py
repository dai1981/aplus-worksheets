# -*- coding: utf-8 -*-
"""
Singapore Primary 3 Maths: Bar Graphs (MOE 2021 Primary Mathematics Syllabus, Standard – Statistics)
  python3 tools/gen_sg_maths_p3_bar_graphs.py
Reading and interpreting bar graphs with a scale of 1, then scales of 2, 5 and 10 (bars on a line and bars
halfway between two lines), comparing and totalling, horizontal bar graphs, and word problems with
Singapore contexts (favourite fruit at recess, books borrowed from the library, Sports Day points,
bubble tea, rainy days) and bar models (the model method, “units”).
Wrong answers come from real student mistakes: counting grid lines as 1 each when the scale counts by
2s, 5s or 10s, reading the bar next door, reading a bar between two lines as the line below or above,
adding instead of subtracting, stopping after the first step of a two-step problem.
Every value is checked in code. Singapore style: British spelling, Singapore names. HTML attributes use
single quotes (no backslashes in the JSON).
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "sg", "maths", "primary-3")
UPDATED = "2026-11-03"
LINE = "#1f4e79"
BAR = "#2f6fb5"
FILL = "#cfe0f1"
PFILL = "#eef4fa"
RED = "#c0392b"
INK = "#2b2b2b"
GRID = "#c4d0dc"
FONT = "Arial, Helvetica, sans-serif"
NB = "\u00a0"


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e):
    """4 choices: correct + 3 unique distractors from real mistakes (no zero or negative numbers).
    Positions are balanced later for the whole set."""
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        if c is None:
            continue
        c = str(c)
        lead = c.split(" ")[0]
        if c in seen or not c or lead.startswith("-") or lead.startswith("−") or lead == "0":
            continue
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q[-90:], correct, cands)
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


def tw(t, fs, bold=False):
    """Approximate text width in px (Arial)."""
    return len(str(t)) * fs * (0.62 if bold else 0.58)


def text(x, y, t, fs=14, anchor="middle", bold=False, col=INK, extra=""):
    return ("<text x='%.1f' y='%.1f' font-size='%d'%s fill='%s' text-anchor='%s'%s>%s</text>"
            % (x, y, fs, " font-weight='700'" if bold else "", col, anchor, extra, t))


def fmt(v, unit):
    """unit = (singular, plural)."""
    if v is None:
        return None
    return "%d %s" % (v, unit[0] if v == 1 else unit[1])


# ------------------------------------------------------------ contexts
class Ctx:
    def __init__(self, title, axis, vaxis, cats, unit, ask, more, fewer, both, total, notq, scales,
                 ph=None, ordered=False, tie=None, vert=True):
        self.title, self.axis, self.vaxis, self.cats, self.unit = title, axis, vaxis, cats, unit
        self.ask_f, self.more_f, self.fewer_f, self.both_f = ask, more, fewer, both
        self.total, self.not_f, self.tie_f = total, notq, tie
        self.scales, self.ph, self.ordered, self.vert = scales, ph or {}, ordered, vert

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

    def notq(self, a):
        return self.not_f.format(a=self.p(a))

    def tie(self, a, b):
        return self.tie_f.format(a=self.p(a), b=self.p(b))


STU = ("student", "students")
BOOK = ("book", "books")
CUP = ("cup", "cups")
PT = ("point", "points")
STK = ("sticker", "stickers")
DAY = ("day", "days")
BOX = ("box", "boxes")
DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
DAYPH = {"Mon": "Monday", "Tue": "Tuesday", "Wed": "Wednesday", "Thu": "Thursday", "Fri": "Friday",
         "Sat": "Saturday"}
LOW = lambda cs: {c: c.lower() for c in cs}

FRUIT = Ctx("Favourite fruit at recess", "Fruit", "Students", ["Apple", "Banana", "Papaya", "Grapes", "Orange"], STU,
            "How many students chose {a}?", "How many more students chose {a} than {b}?",
            "How many fewer students chose {a} than {b}?", "How many students chose {a} or {b}?",
            "How many students chose a fruit altogether?",
            "Each student chose one fruit. How many students did <b>not</b> choose {a}?",
            {1: (1, 10), 2: (2, 20), 5: (5, 50)},
            ph={"Apple": "apples", "Banana": "bananas", "Papaya": "papaya", "Grapes": "grapes", "Orange": "oranges"})
BOOKS = Ctx("Books borrowed from the library", "Day", "Books", DAYS[:5], BOOK,
            "How many books were borrowed on {a}?", "How many more books were borrowed on {a} than on {b}?",
            "How many fewer books were borrowed on {a} than on {b}?",
            "How many books were borrowed on {a} and {b} altogether?",
            "How many books were borrowed altogether?",
            "How many books were borrowed on the other days, not counting {a}?",
            {2: (4, 20), 5: (10, 50), 10: (20, 100)}, ph=DAYPH, ordered=True)
SCHOOL = Ctx("How we go to school", "Way", "Students", ["Walk", "Bus", "MRT", "Car", "Bicycle"], STU,
             "How many students {a} to school?", "How many more students {a} than {b}?",
             "How many fewer students {a} than {b}?", "How many students {a} or {b}?",
             "How many students are in the survey altogether?",
             "Each student chose one way. How many students do <b>not</b> {a}?",
             {1: (1, 10), 2: (2, 20), 5: (5, 50)},
             ph={"Walk": "walk", "Bus": "take the bus", "MRT": "take the MRT", "Car": "come by car", "Bicycle": "cycle"})
HAWKER = Ctx("Favourite hawker food", "Food", "Students", ["Chicken rice", "Prata", "Laksa", "Satay", "Nasi lemak"], STU,
             "How many students chose {a}?", "How many more students chose {a} than {b}?",
             "How many fewer students chose {a} than {b}?", "How many students chose {a} or {b}?",
             "How many students voted altogether?",
             "Each student voted once. How many students did <b>not</b> choose {a}?",
             {1: (1, 10), 2: (2, 20), 5: (5, 50), 10: (20, 100)}, ph=LOW(["Chicken rice", "Prata", "Laksa", "Satay", "Nasi lemak"]),
             vert=False)
BUBBLE = Ctx("Cups of bubble tea sold", "Flavour", "Cups", ["Milk tea", "Taro", "Mango", "Lychee", "Peach"], CUP,
             "How many cups of {a} were sold?", "How many more cups of {a} than {b} were sold?",
             "How many fewer cups of {a} than {b} were sold?", "How many cups of {a} and {b} were sold altogether?",
             "How many cups were sold altogether?", "How many cups sold were <b>not</b> {a}?",
             {5: (10, 50), 10: (20, 100)},
             ph={"Milk tea": "milk tea", "Taro": "taro tea", "Mango": "mango tea", "Lychee": "lychee tea", "Peach": "peach tea"})
HOUSE = Ctx("Sports Day points", "House", "Points", ["Red", "Blue", "Green", "Yellow"], PT,
            "How many points did {a} get?", "How many more points did {a} get than {b}?",
            "How many fewer points did {a} get than {b}?", "How many points did {a} and {b} get altogether?",
            "How many points did the four houses get altogether?",
            "How many points did the other houses get, not counting {a}?",
            {10: (20, 100)}, ph={c: c + " House" for c in ["Red", "Blue", "Green", "Yellow"]},
            tie="How many more points does {b} need to catch up with {a}?")
STICK = Ctx("Stickers collected", "Child", "Stickers", ["Ali", "Mei Ling", "Raju", "Siti", "Ethan"], STK,
            "How many stickers did {a} collect?", "How many more stickers did {a} collect than {b}?",
            "How many fewer stickers did {a} collect than {b}?",
            "How many stickers did {a} and {b} collect altogether?",
            "How many stickers did the children collect altogether?",
            "How many stickers did the others collect, not counting {a}?",
            {1: (1, 10), 2: (2, 20), 5: (5, 50)},
            tie="How many more stickers must {b} collect to have as many as {a}?")
RAINY = Ctx("Rainy days last year", "Month", "Rainy days", ["Mar", "Apr", "May", "Jun", "Jul", "Aug"], DAY,
            "How many rainy days were there in {a}?", "How many more rainy days were there in {a} than in {b}?",
            "How many fewer rainy days were there in {a} than in {b}?",
            "How many rainy days were there in {a} and {b} altogether?",
            "How many rainy days were there in these months altogether?",
            "How many rainy days were there in the other months, not counting {a}?",
            {2: (8, 18)}, ordered=True,
            ph={"Mar": "March", "Apr": "April", "May": "May", "Jun": "June", "Jul": "July", "Aug": "August"})
ORANGE = Ctx("Boxes of mandarin oranges sold", "Day", "Boxes", DAYS, BOX,
             "How many boxes were sold on {a}?", "How many more boxes were sold on {a} than on {b}?",
             "How many fewer boxes were sold on {a} than on {b}?",
             "How many boxes were sold on {a} and {b} altogether?",
             "How many boxes were sold altogether?",
             "How many boxes were sold on the other days, not counting {a}?",
             {5: (10, 50), 10: (20, 100)}, ph=DAYPH, ordered=True)
CCA = Ctx("Students in each CCA", "CCA", "Students", ["Choir", "Football", "Art", "Robotics", "Dance"], STU,
          "How many students joined {a}?", "How many more students joined {a} than {b}?",
          "How many fewer students joined {a} than {b}?", "How many students joined {a} or {b}?",
          "How many students are in these CCAs altogether?",
          "Each student joined one of these CCAs. How many students did <b>not</b> join {a}?",
          {2: (4, 20), 5: (10, 50)},
          ph={"Choir": "the choir", "Football": "football", "Art": "the art club", "Robotics": "robotics",
              "Dance": "dance"})
CTXS = [FRUIT, BOOKS, SCHOOL, HAWKER, BUBBLE, HOUSE, STICK, RAINY, ORANGE, CCA]


class Picker:
    """Hands out contexts in a shuffled cycle so neighbouring questions use different stories."""
    def __init__(self, rnd):
        self.rnd = rnd
        self.q = []
        self.last = None

    def next(self, ok=lambda c: True):
        for _ in range(4):
            for i, c in enumerate(self.q):
                if ok(c) and c is not self.last:
                    self.last = c
                    return self.q.pop(i)
            fresh = CTXS[:]
            self.rnd.shuffle(fresh)
            self.q += fresh
        raise ValueError("no context")


def fresh_data(ctx, n, sc, rnd, half, halves):
    """Data with at least one bar of the wanted kind (on a line / between lines) not asked about yet."""
    for _ in range(200):
        cats, vals = make_data(ctx, n, sc, rnd, halves=halves)
        if any((v % sc != 0) == half and (ctx.title, c) not in ASKED for c, v in zip(cats, vals)):
            return cats, vals
    return cats, vals


def make_data(ctx, n, sc, rnd, ok=lambda v: True, halves=(0, 1)):
    """n different values for scale sc. Scale 1 and 5: every value on a line. Scale 2 and 10: a value may be
    halfway between two lines (odd numbers for 2s, 5s for 10s); `halves` = allowed count of such values."""
    n = min(n, len(ctx.cats))
    if ctx.ordered:
        start = rnd.randint(0, len(ctx.cats) - n)
        cats = ctx.cats[start:start + n]
    else:
        cats = rnd.sample(ctx.cats, n)
    lo, hi = ctx.scales[sc]
    step = {1: 1, 2: 1, 5: 5, 10: 5}[sc]
    pool = list(range(lo, hi + 1, step))
    for _ in range(20000):
        vals = [rnd.choice(pool) for _ in range(n)]
        if len(set(vals)) != n:
            continue
        nh = sum(1 for v in vals if v % sc)
        if not halves[0] <= nh <= halves[1]:
            continue
        if max(vals) - min(vals) < 3 * step + (sc if sc > 2 else 0):
            continue
        if not ok(vals):
            continue
        return cats, vals
    raise ValueError("no data for " + ctx.title)


# ------------------------------------------------------------ bar graphs
def bar_svg(title, cat_axis, val_axis, cats, vals, scale, horizontal=False, missing=None, label="bar graph"):
    """Bar graph with a grid line and a number at every step of the scale.
    `missing` = index of a category drawn with no bar (a red ? shows where it goes)."""
    fs = 14
    top_v = int(math.ceil(max(vals) / float(scale)) * scale)
    if top_v // scale < 4:
        top_v = 4 * scale
    nt = top_v // scale
    assert 4 <= nt <= 10, (title, vals, scale)
    for v in vals:
        assert v % scale == 0 or (scale in (2, 10) and 2 * (v % scale) == scale), (title, v, scale)
    s = []
    if not horizontal:
        gy = 16 if nt > 6 else 19
        ph = nt * gy
        lw = tw(top_v, fs)
        x0 = 22 + lw + 6
        slot = max(48, max(tw(c, fs) for c in cats) + 12)
        pw = slot * len(cats)
        y0 = 32
        yb = y0 + ph
        W = x0 + pw + 8
        W = max(W, tw(title, 16, True) + 16)
        s.append(text(W / 2, 18, title, 16, bold=True))
        for k in range(nt + 1):
            y = yb - k * gy
            s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1'/>" % (x0, y, x0 + pw, y, GRID))
            s.append(text(x0 - 5, y + 5, k * scale, fs, anchor="end"))
        for i, (c, v) in enumerate(zip(cats, vals)):
            cx = x0 + slot * i + slot / 2
            bw = min(30, slot * 0.62)
            if i == missing:
                s.append(text(cx, yb - 6, "?", 18, bold=True, col=RED))
            else:
                h = v / float(scale) * gy
                s.append("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' fill='%s'/>" % (cx - bw / 2, yb - h, bw, h, BAR))
            s.append(text(cx, yb + 17, c, fs))
        s.append("<path d='M%.1f %d V%.1f H%.1f' fill='none' stroke='%s' stroke-width='2'/>" % (x0, y0 - 6, yb, x0 + pw, INK))
        s.append(text(x0 + pw / 2, yb + 36, cat_axis, fs, bold=True))
        mid = y0 + ph / 2
        s.append(text(13, mid, val_axis, fs, bold=True, extra=" transform='rotate(-90 13 %.1f)'" % mid))
        H = yb + 42
        assert tw(val_axis, fs, True) < ph + 26, (val_axis, ph)
    else:
        rh = 26
        gx = 26 if nt > 6 else 32
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
                w = v / float(scale) * gx
                s.append("<rect x='%.1f' y='%.1f' width='%.1f' height='16' fill='%s'/>" % (x0, cy - 8, w, BAR))
            s.append(text(x0 - 6, cy + 5, c, fs, anchor="end"))
        s.append("<path d='M%.1f %d V%d H%.1f' fill='none' stroke='%s' stroke-width='2'/>" % (x0, y0, yb, x0 + pw + 4, INK))
        s.append(text(x0 + pw / 2, yb + 36, val_axis, fs, bold=True))
        mid = y0 + ph / 2
        s.append(text(13, mid, cat_axis, fs, bold=True, extra=" transform='rotate(-90 13 %.1f)'" % mid))
        H = yb + 42
        assert tw(cat_axis, fs, True) < ph + 26, (cat_axis, ph)
    return svg_wrap(W, H, "".join(s), label)


def ctx_bar(ctx, cats, vals, scale, horizontal=False, missing=None):
    return bar_svg(ctx.title, ctx.axis, ctx.vaxis, cats, vals, scale, horizontal, missing,
                   label="bar graph: " + ctx.title.lower())


# ------------------------------------------------------------ A-D panels (one picture)
PW, PH = 218, 172


def mini_bar(x0, y0, cats, vals, scale, top_v):
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
        h = v / float(scale) * gy
        s.append("<rect x='%.1f' y='%.1f' width='24' height='%.1f' fill='%s'/>" % (cx - 12, yb - h, h, BAR))
        s.append(text(cx, yb + 17, c, fs))
        assert tw(c, fs) <= slot - 4, c
    s.append("<path d='M%.1f %.1f V%.1f H%.1f' fill='none' stroke='%s' stroke-width='2'/>" % (ax, yb - 112 - 4, yb, ax + slot * len(cats), INK))
    assert ax + slot * len(cats) <= x0 + PW - 2
    return "".join(s)


def panel_svg(draws, label):
    W, H = 2 * PW, 2 * PH
    s = ["<line x1='%d' y1='4' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (PW, PW, H - 4, GRID),
         "<line x1='4' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (PH, W - 4, PH, GRID)]
    for k, d in enumerate(draws):
        x0, y0 = (k % 2) * PW, (k // 2) * PH
        s.append(d(x0, y0))
        s.append(text(x0 + 8, y0 + 20, "ABCD"[k], 18, anchor="start", bold=True))
    return svg_wrap(W, H, "".join(s), label)


# ------------------------------------------------------------ bar models
SEGFILL = {"u": FILL, "o": "#e3e3e3", "w": "#ffffff"}


def model_svg(rows, top=None, under=(), right=None, BW=300, label="bar model"):
    """Bar model drawn to scale.
    rows: [(name, [(value, text, style)])], style u (unit, blue), o (other, grey), w (white, dashed).
    top: (v0, v1, text) bracket over row 0; under: [(row, v0, v1, text)] brackets under a row;
    right: text for a bracket on the right joining all rows. Text '?' is drawn in red."""
    names = [n for n, _ in rows]
    nw = max([tw(n, 15) for n in names] + [0])
    x0 = 8 + (nw + 10 if nw else 0)
    maxv = max(sum(v for v, _, _ in segs) for _, segs in rows)
    sc = BW / float(maxv)
    bh = 32
    out = []
    y = 38 if top else 8
    ys = []
    for i, (n, segs) in enumerate(rows):
        ys.append(y)
        y += bh + (40 if any(u[0] == i for u in under) else 14)
    last_under = any(u[0] == len(rows) - 1 for u in under)
    Hh = (y - 40 + 46) if last_under else (y - 14 + 8)

    def col(t):
        return RED if t == "?" else INK

    for i, (n, segs) in enumerate(rows):
        ry = ys[i]
        if n:
            out.append(text(8, ry + 22, n, 15, anchor="start"))
        x = x0
        for v, t, st in segs:
            w = v * sc
            dash = " stroke-dasharray='5 4'" if st == "w" else ""
            out.append("<rect x='%.1f' y='%d' width='%.1f' height='%d' fill='%s' stroke='%s' stroke-width='2'%s/>"
                       % (x, ry, w, bh, SEGFILL[st], LINE, dash))
            if t:
                assert tw(t, 15) + 4 <= w, (t, w)
                out.append(text(x + w / 2, ry + 22, t, 15, col=col(t)))
            x += w
    if top:
        v0, v1, t = top
        a, b = x0 + v0 * sc, x0 + v1 * sc
        ry = ys[0]
        out.append("<path d='M%.1f %d V%d H%.1f V%d' fill='none' stroke='%s' stroke-width='2'/>" % (a, ry - 4, ry - 11, b, ry - 4, INK))
        out.append(text((a + b) / 2, ry - 16, t, 16, col=col(t)))
    for r, v0, v1, t in under:
        a, b = x0 + v0 * sc, x0 + v1 * sc
        yb = ys[r] + bh
        out.append("<path d='M%.1f %d V%d H%.1f V%d' fill='none' stroke='%s' stroke-width='2'/>"
                   % (a, yb + 4, yb + 11, b, yb + 4, RED if t == "?" else INK))
        out.append(text((a + b) / 2, yb + 30, t, 16, col=col(t)))
    W = x0 + BW + 8
    if right:
        xr = x0 + BW + 8
        y0, y1 = ys[0], ys[-1] + bh
        out.append("<path d='M%.1f %d H%.1f V%d H%.1f' fill='none' stroke='%s' stroke-width='2'/>" % (xr, y0, xr + 8, y1, xr, INK))
        out.append(text(xr + 14, (y0 + y1) / 2 + 6, right, 16, col=col(right), anchor="start"))
        W = xr + 14 + tw(right, 16) + 8
    return svg_wrap(W, Hh, "".join(out), label)


# ------------------------------------------------------------ reading text and mistakes
def read_bar(c, v, scale):
    if v % scale:
        lo = v - v % scale
        return "The bar for %s ends halfway between %d and %d, so it shows %d." % (c, lo, lo + scale, v)
    return "The bar for %s ends on the line for %d." % (c, v)


def bn(ctx, c):
    """Bar name in a question: full day or month name for Mon, Jul …"""
    return ctx.p(c) if ctx.ordered else c


def neighbour(n, j):
    return j + 1 if j + 1 < n else j - 1


ASKED = set()


def pick_row(rnd, ctx, cats, js):
    """A bar that has not been asked about before in this context (so no two questions read the same)."""
    fresh = [j for j in js if (ctx.title, cats[j]) not in ASKED]
    j = rnd.choice(fresh or js)
    ASKED.add((ctx.title, cats[j]))
    return j


def scl(sc):
    return "The scale counts by %ds. " % sc


def read_q(rnd, ctx, cats, vals, sc, f, half, horiz=False):
    """How many … ? for one bar. Wrong answers: grid lines counted as 1 each, the bar next door,
    the line below or above."""
    n = len(cats)
    js = [k for k, v in enumerate(vals) if (v % sc != 0) == half]
    j = pick_row(rnd, ctx, cats, js)
    c, v = cats[j], vals[j]
    nb = neighbour(n, j)
    U = ctx.unit
    if half:
        lo, hi = v - v % sc, v - v % sc + sc
        cand = [lo, hi, vals[nb], lo // sc, v + sc]
        why = "(%d and %d are the lines on each side of it.)" % (lo, hi)
    elif sc > 1:
        cand = [v // sc, vals[nb], v + sc, v - sc]
        why = ("(%d counts the grid lines as 1 each. Read the number on the scale instead.)" % (v // sc)
               if v // sc != vals[nb] else "")
    else:
        cand = [vals[nb], v + 1, v - 1] + [vals[k] for k in range(n) if k != j]
        why = ("(%d is the bar next to it, %s. Keep your finger on the right bar.)" % (vals[nb], cats[nb]))
    look = "Look straight across" if not horiz else "Look straight down"
    e = "%s%s %s" % (scl(sc), read_bar(c, v, sc), why)
    if sc == 1 and not half:
        e = "%s from the end of the %s bar to the scale. %s" % (look, c, e)
    return mcq(f + ctx.ask(c), fmt(v, U), [fmt(x, U) for x in cand], e.strip())


def which_q(rnd, ctx, cats, vals, sc, f, half):
    n = len(cats)
    js = [k for k, v in enumerate(vals) if (v % sc != 0) == half]
    j = rnd.choice(js)
    v = vals[j]
    near = sorted([k for k in range(n) if k != j], key=lambda k: abs(vals[k] - v))
    return mcq(f + "Which bar shows %s?" % fmt(v, ctx.unit), cats[j], [cats[k] for k in near],
               "%sFind %d on the scale. %s" % (scl(sc), v, read_bar(cats[j], v, sc)))


def step_q(f, sc):
    return mcq(f + "What does the scale on this bar graph count by?", "%ds" % sc,
               ["%ds" % x for x in (1, 2, 5, 10) if x != sc],
               "Read the numbers on the scale: 0, %d, %d, %d … Each line is %d more than the one before it, "
               "so the scale counts by %ds." % (sc, 2 * sc, 3 * sc, sc, sc)
               + (" Do not count the lines as 1 each." if sc > 1 else ""))


def list_q(ctx, cats, vals, sc, f, horiz=False):
    lst = lambda vs: ", ".join(str(v) for v in vs)
    sw = vals[:]
    sw[0], sw[1] = sw[1], sw[0]
    hs = [k for k, v in enumerate(vals) if v % sc]
    if hs:
        wrong = [lst([v - v % sc for v in vals]), lst([v + (sc - v % sc if v % sc else 0) for v in vals]), lst(sw)]
        why = " (%s reads the bars between two lines as the line below.)" % wrong[0]
    elif sc > 1:
        wrong = [lst([v // sc for v in vals]), lst(sw), lst([v + sc for v in vals])]
        why = " (%s counts the grid lines as 1 each.)" % wrong[0]
    else:
        wrong = [lst(sw), lst([v + 1 for v in vals]), lst(vals[::-1])]
        why = " (%s swaps the first two bars.)" % wrong[0]
    order = "from top to bottom" if horiz else "from left to right"
    return mcq(f + "Which list matches this bar graph? The numbers are in order %s: %s."
               % (order, ", ".join(cats)), lst(vals), wrong,
               scl(sc) + " ".join(read_bar(c, v, sc) for c, v in zip(cats, vals)) + why)


def ends(word_hi, horiz):
    return ("longest" if horiz else "tallest") if word_hi else "shortest"


def most_q(ctx, cats, vals, sc, f, most, horiz=False):
    j = vals.index(max(vals) if most else min(vals))
    U = ctx.unit
    if ctx.ordered:
        q = "Which %s has the %s %s?" % (ctx.axis.lower(), "most" if most else "fewest", U[1])
        if ctx is RAINY:
            q = "Which month had the %s rainy days?" % ("most" if most else "fewest")
    else:
        q = "Which bar shows the %s %s?" % ("most" if most else "fewest", U[1])
    ans = ctx.p(cats[j]) if ctx.ordered else cats[j]
    others = [ctx.p(cats[k]) if ctx.ordered else cats[k] for k in range(len(cats)) if k != j]
    return mcq(f + q, ans, others, "The %s bar is %s. %s" % (ends(most, horiz), cats[j], read_bar(cats[j], vals[j], sc)))


# ------------------------------------------------------------ set 1: scale of 1
def match_q(rnd, pos, title, cats, vals, step):
    """Which bar graph (A to D) shows the data? Wrong graphs come from real drawing mistakes."""
    wrong = []
    i, j = rnd.sample(range(len(vals)), 2)
    while vals[i] == vals[j]:
        i, j = rnd.sample(range(len(vals)), 2)
    sw = vals[:]
    sw[i], sw[j] = sw[j], sw[i]
    wrong.append(("two bars are the wrong way round", sw))
    k = rnd.choice(range(len(vals)))
    w = vals[:]
    w[k] = vals[k] + step
    wrong.append(("the %s bar is one line too high" % cats[k], w))
    k2 = rnd.choice([x for x in range(len(vals)) if x != k and vals[x] > step])
    w = vals[:]
    w[k2] = vals[k2] - step
    wrong.append(("the %s bar is one line too low" % cats[k2], w))
    order = wrong[:]
    order.insert(pos, ("ok", vals))
    assert len({tuple(v) for _, v in order}) == 4
    top_v = int(math.ceil(max(max(v) for _, v in order) / float(step)) * step)
    draws = [(lambda x0, y0, v=v: mini_bar(x0, y0, cats, v, step, top_v)) for _, v in order]
    svg = panel_svg(draws, "bar graphs: " + title.lower())
    why = ["in %s, %s" % ("ABCD"[k], t) for k, (t, v) in enumerate(order) if t != "ok"]
    e = "%s matches every number. %s." % ("ABCD"[pos], "; ".join(why))
    e = e.replace(". in ", ". In ")
    tb = "<b>%s</b>: %s. " % (title, ", ".join("%s %d" % (c, v) for c, v in zip(cats, vals)))
    return mcq_fixed(fig(svg) + tb + "Which bar graph shows this data?", ["A", "B", "C", "D"], pos, e)


def set_scale1(rnd, PK):
    its = []
    plan = ["title", "step", "read", "which", "read", "most", "read", "fewest", "which", "over",
            "read", "list", "read", "match", "which", "order", "read", "most", "read", "under"]
    for i, kind in enumerate(plan):
        if kind == "match":
            its.append(match_q(rnd, 2, "Stickers collected", ["Ali", "Siti", "Raju", "Devi"], [6, 9, 4, 7], 1))
            continue
        ctx = PK.next(lambda c: 1 in c.scales and c.vert)
        n = 5 if i % 3 == 0 else 4
        if kind == "read":
            cats, vals = fresh_data(ctx, n, 1, rnd, False, (0, 0))
        else:
            cats, vals = make_data(ctx, n, 1, rnd)
        n = len(cats)
        f = fig(ctx_bar(ctx, cats, vals, 1))
        U = ctx.unit
        if kind == "title":
            others = [c.title for c in CTXS if c is not ctx]
            rnd.shuffle(others)
            its.append(mcq(f + "What is the title of this bar graph?", ctx.title, [ctx.axis, ctx.vaxis] + others,
                           "The title is at the top of the graph. It tells us what the graph is about: “%s”. "
                           "“%s” and “%s” are the labels on the two axes." % (ctx.title, ctx.axis, ctx.vaxis)))
        elif kind == "step":
            its.append(step_q(f, 1))
        elif kind == "read":
            its.append(read_q(rnd, ctx, cats, vals, 1, f, False))
        elif kind == "which":
            its.append(which_q(rnd, ctx, cats, vals, 1, f, False))
        elif kind in ("most", "fewest"):
            its.append(most_q(ctx, cats, vals, 1, f, kind == "most"))
        elif kind == "list":
            its.append(list_q(ctx, cats, vals, 1, f))
        elif kind in ("over", "under"):
            lim = sorted(vals)[n // 2]
            if kind == "over":
                ans = sum(1 for v in vals if v > lim)
                ge = sum(1 for v in vals if v >= lim)
                q = "How many bars show more than %s?" % fmt(lim, U)
                pick = [c for c, v in zip(cats, vals) if v > lim]
            else:
                ans = sum(1 for v in vals if v < lim)
                ge = sum(1 for v in vals if v <= lim)
                q = "How many bars show fewer than %s?" % fmt(lim, U)
                pick = [c for c, v in zip(cats, vals) if v < lim]
            word = "More" if kind == "over" else "Fewer"
            bars = lambda x: "%d bar%s" % (x, "" if x == 1 else "s")
            its.append(mcq(f + q, bars(ans), [bars(x) for x in [ge, ans + 1, ans - 1, n - ans, n]],
                           "Read every bar: %s. %s than %d means %d itself does not count. %s: %s. That is %s."
                           % (", ".join("%s %d" % (c, v) for c, v in zip(cats, vals)), word, lim, lim,
                              word + " than %d" % lim, " and ".join(pick), bars(ans))))
        elif kind == "order":
            idx = sorted(range(n), key=lambda k: -vals[k])
            right = ", ".join(cats[k] for k in idx)
            rev = ", ".join(cats[k] for k in idx[::-1])
            sw = idx[:]
            sw[1], sw[2] = sw[2], sw[1]
            sw2 = idx[:]
            sw2[0], sw2[1] = sw2[1], sw2[0]
            its.append(mcq(f + "Which list orders the bars from the most %s to the fewest?" % U[1], right,
                           [rev, ", ".join(cats[k] for k in sw), ", ".join(cats[k] for k in sw2)],
                           "Read every bar: %s. Start with the tallest bar and end with the shortest: %s. "
                           "(%s goes from the fewest to the most.)"
                           % (", ".join("%s %d" % (c, v) for c, v in zip(cats, vals)), right, rev)))
    assert len(its) == 20, len(its)
    return {"title": "Reading bar graphs: scale of 1", "items": its}


# ------------------------------------------------------------ set 2: scales of 2, 5 and 10
def lines_q(sc, k, item, unit):
    v = sc * k
    return mcq("A bar graph has a scale that counts by %ds. The bar for %s ends on the %s line above 0. "
               "What number does the bar show?" % (sc, item, ["", "1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th", "9th"][k]),
               fmt(v, unit), [fmt(x, unit) for x in [k, v + sc, k + sc, v - sc]],
               "Count up the lines by %ds: %s. So the bar shows %d. "
               "(%d counts the grid lines as 1 each.)" % (sc, ", ".join(str(sc * t) for t in range(1, k + 1)), v, k))


def set_scales(rnd, PK):
    its = []
    plan = [(2, "step"), (2, "read"), (2, "readh"), (2, "which"), (2, "list"),
            (5, "step"), (5, "read"), (5, "read"), (5, "which"), (5, "lines"),
            (10, "step"), (10, "read"), (10, "readh"), (10, "which"), (10, "readh"),
            (10, "lines"), (2, "readh"), (5, "list"), (10, "list"), (2, "whichh")]
    for i, (sc, kind) in enumerate(plan):
        if kind == "lines":
            if sc == 5:
                its.append(lines_q(5, 7, "mango tea", CUP))
            else:
                its.append(lines_q(10, 6, "Blue House", PT))
            continue
        ctx = PK.next(lambda c: sc in c.scales and c.vert)
        n = 5 if i % 3 == 0 else 4
        if sc in (2, 10):
            hv = (1, 2) if kind in ("readh", "whichh", "list") else (0, 1)
        else:
            hv = (0, 0)
        if kind in ("read", "readh"):
            cats, vals = fresh_data(ctx, n, sc, rnd, kind.endswith("h"), hv)
        else:
            cats, vals = make_data(ctx, n, sc, rnd, halves=hv)
        f = fig(ctx_bar(ctx, cats, vals, sc))
        if kind == "step":
            its.append(step_q(f, sc))
        elif kind == "read":
            its.append(read_q(rnd, ctx, cats, vals, sc, f, False))
        elif kind == "readh":
            its.append(read_q(rnd, ctx, cats, vals, sc, f, True))
        elif kind == "which":
            its.append(which_q(rnd, ctx, cats, vals, sc, f, False))
        elif kind == "whichh":
            its.append(which_q(rnd, ctx, cats, vals, sc, f, True))
        elif kind == "list":
            its.append(list_q(ctx, cats, vals, sc, f))
    assert len(its) == 20, len(its)
    return {"title": "Scales of 2, 5 and 10", "items": its}


# ------------------------------------------------------------ set 3 and 4: compare and total
def rd(cats, vals, k):
    return "%s: %d" % (cats[k], vals[k])


def compare_q(rnd, ctx, cats, vals, sc, f, kind, horiz=False):
    n = len(cats)
    U = ctx.unit
    hint = scl(sc) if any(v % sc for v in vals) else ""
    if kind in ("more", "fewer"):
        pairs = [(a, b) for a in range(n) for b in range(n) if vals[a] - vals[b] >= 2 * (sc if sc > 1 else 1)]
        new = [pr for pr in pairs if (ctx.title, cats[pr[0]], cats[pr[1]]) not in ASKED]
        a, b = rnd.choice(new or pairs)
        ASKED.add((ctx.title, cats[a], cats[b]))
        d = vals[a] - vals[b]
        q = ctx.more(cats[a], cats[b]) if kind == "more" else ctx.fewer(cats[b], cats[a])
        w = "more" if kind == "more" else "fewer"
        cand = [vals[a] + vals[b], vals[a] if kind == "more" else vals[b], d + sc, d - sc, d + 1]
        if sc > 1:
            cand.insert(1, d // sc if d % sc == 0 and d // sc != d else None)
        return mcq(f + q, fmt(d, U), [fmt(x, U) for x in cand if x],
                   "%s%s. %s. How many %s means find the difference: %d − %d = %d. (%d adds instead of subtracting.)"
                   % (hint, rd(cats, vals, a), rd(cats, vals, b), w, vals[a], vals[b], d, vals[a] + vals[b]))
    if kind == "both":
        a, b = rnd.sample(range(n), 2)
        t = vals[a] + vals[b]
        cand = [abs(vals[a] - vals[b]), t + sc, t - sc, max(vals[a], vals[b]), t + 1]
        return mcq(f + ctx.both(cats[a], cats[b]), fmt(t, U), [fmt(x, U) for x in cand],
                   "%s%s. %s. Altogether means add: %d + %d = %d. (%d subtracts instead of adding.)"
                   % (hint, rd(cats, vals, a), rd(cats, vals, b), vals[a], vals[b], t, abs(vals[a] - vals[b])))
    if kind == "total":
        t = sum(vals)
        lows = sum(v - v % sc for v in vals)
        cand = [lows if lows != t else None, t - vals[-1], t - vals[0], t + sc, t - sc]
        e = ("%sRead every bar: %s. Add them all: %s = %d. Make sure you add every bar once."
             % (hint, ", ".join(rd(cats, vals, k) for k in range(n)), " + ".join(str(v) for v in vals), t))
        if lows != t:
            e += " (%d reads the bars between two lines as the line below.)" % lows
        return mcq(f + ctx.total, fmt(t, U), [fmt(x, U) for x in cand], e)
    if kind == "range":
        hi, lo = max(vals), min(vals)
        jh, jl = vals.index(hi), vals.index(lo)
        second = sorted(vals)[-2]
        cand = [hi + lo, hi, hi - second, hi - lo + sc]
        long_w = "longest" if horiz else "tallest"
        return mcq(f + "How many more %s does the %s bar show than the shortest bar?" % (U[1], long_w),
                   fmt(hi - lo, U), [fmt(x, U) for x in cand],
                   "%sThe %s bar is %s (%d). The shortest bar is %s (%d). %d − %d = %d."
                   % (hint, long_w, cats[jh], hi, cats[jl], lo, hi, lo, hi - lo))
    if kind == "notx":
        j = pick_row(rnd, ctx, cats, list(range(n)))
        t = sum(vals)
        nb = neighbour(n, j)
        cand = [vals[j], t, t - vals[nb], t - vals[j] + sc]
        return mcq(f + ctx.notq(cats[j]), fmt(t - vals[j], U), [fmt(x, U) for x in cand],
                   "%sAdd the other bars: %s = %d. Or find the total, %d, and take away %s (%d): %d − %d = %d."
                   % (hint, " + ".join(str(vals[k]) for k in range(n) if k != j), t - vals[j], t, cats[j], vals[j],
                      t, vals[j], t - vals[j]))
    if kind == "tie":
        pairs = [(a, b) for a in range(n) for b in range(n) if vals[a] - vals[b] >= 2 * (sc if sc > 1 else 1)]
        a, b = rnd.choice(pairs)
        d = vals[a] - vals[b]
        cand = [vals[a], vals[a] + vals[b], d + sc, d - sc]
        return mcq(f + ctx.tie(cats[a], cats[b]), fmt(d, U), [fmt(x, U) for x in cand],
                   "%s%s. %s. Find the difference: %d − %d = %d. (%d is %s’s number, not how many more.)"
                   % (hint, rd(cats, vals, a), rd(cats, vals, b), vals[a], vals[b], d, vals[a], ctx.p(cats[a])))
    if kind == "vsboth":
        srt = sorted(range(n), key=lambda k: vals[k])
        a, b, c = srt[-1], srt[0], srt[1]
        t2 = vals[b] + vals[c]
        d = vals[a] - t2
        q = ("How many more %s does the %s bar show than the %s and %s bars together?"
             % (U[1], bn(ctx, cats[a]), bn(ctx, cats[b]), bn(ctx, cats[c])))
        cand = [vals[a] + t2, t2, vals[a] - vals[b], d + sc]
        return mcq(f + q, fmt(d, U), [fmt(x, U) for x in cand],
                   "%sStep 1: %s and %s together: %d + %d = %d. Step 2: %s: %d. %d − %d = %d. "
                   "(%d stops after step 1.)"
                   % (hint, cats[b], cats[c], vals[b], vals[c], t2, cats[a], vals[a], vals[a], t2, d, t2))
    if kind == "twice":
        pairs = [(a, b) for a in range(n) for b in range(n) if vals[a] == 2 * vals[b]]
        a, b = pairs[0]
        near = [k for k in range(n) if vals[k] == vals[b] + 2 * sc] + \
            sorted([k for k in range(n) if k not in (a, b)], key=lambda k: abs(vals[k] - vals[a]))
        return mcq(f + "Which bar shows twice as many %s as the %s bar?" % (U[1], cats[b]), cats[a],
                   [cats[k] for k in near if k != a],
                   "%s%s: %d. Twice as many is 2 × %d = %d. The %s bar shows %d."
                   % (hint, cats[b], vals[b], vals[b], vals[a], cats[a], vals[a]))
    if kind == "missing":
        return None
    raise ValueError(kind)


def missing_q(rnd, ctx, cats, vals, sc, horiz=False):
    n = len(cats)
    m = pick_row(rnd, ctx, cats, list(range(n)))
    f = fig(ctx_bar(ctx, cats, vals, sc, horizontal=horiz, missing=m))
    U = ctx.unit
    t = sum(vals)
    v = vals[m]
    rest = t - v
    cand = [rest, t, v + sc, v - sc, v // sc if sc > 1 else None]
    return mcq(f + "The bar for %s is not drawn yet. The total is %s. What number should the %s bar show?"
               % (bn(ctx, cats[m]), fmt(t, U), bn(ctx, cats[m])), fmt(v, U), [fmt(x, U) for x in cand if x],
               "Add the bars you can see: %s = %d. Then %d − %d = %d. So the %s bar should end at %d."
               % (" + ".join(str(vals[k]) for k in range(n) if k != m), rest, t, rest, v, cats[m], v))


def set_compare(rnd, PK):
    its = []
    plan = [(1, "more"), (1, "both"), (2, "fewer"), (2, "total"), (5, "more"), (1, "range"), (5, "both"),
            (10, "more"), (2, "notx"), (5, "fewer"), (10, "total"), (1, "tie"), (5, "range"), (10, "both"),
            (1, "total"), (2, "missing"), (10, "fewer"), (5, "notx"), (10, "vsboth"), (5, "twice")]
    for i, (sc, kind) in enumerate(plan):
        need = (lambda c: c.tie_f is not None) if kind == "tie" else (lambda c: True)
        ctx = PK.next(lambda c: sc in c.scales and c.vert and need(c))
        n = 5 if (i % 2 == 0 or kind == "twice") else 4
        ok = lambda vs: True
        if kind == "vsboth":
            ok = lambda vs: max(vs) - sum(sorted(vs)[:2]) >= 2 * sc
        if kind == "twice":
            ok = lambda vs: any(a == 2 * b for a in vs for b in vs)
        cats, vals = make_data(ctx, n, sc, rnd, ok=ok, halves=(0, 1) if sc in (2, 10) else (0, 0))
        if kind == "missing":
            its.append(missing_q(rnd, ctx, cats, vals, sc))
            continue
        f = fig(ctx_bar(ctx, cats, vals, sc))
        its.append(compare_q(rnd, ctx, cats, vals, sc, f, kind))
    assert len(its) == 20, len(its)
    return {"title": "Compare and total", "items": its}


# ------------------------------------------------------------ set 4: horizontal bar graphs
def set_horizontal(rnd, PK):
    its = []
    plan = [(1, "read"), (1, "longest"), (2, "read"), (2, "readh"), (1, "more"), (5, "step"), (5, "read"),
            (5, "which"), (2, "both"), (10, "read"), (10, "readh"), (5, "fewer"), (10, "shortest"), (2, "total"),
            (10, "more"), (5, "range"), (2, "whichh"), (10, "notx"), (5, "missing"), (10, "list")]
    for i, (sc, kind) in enumerate(plan):
        ctx = PK.next(lambda c: sc in c.scales)
        n = 5 if i % 2 == 0 else 4
        if sc in (2, 10):
            hv = (1, 2) if kind in ("readh", "whichh", "list") else (0, 1)
        else:
            hv = (0, 0)
        if kind in ("read", "readh"):
            cats, vals = fresh_data(ctx, n, sc, rnd, kind.endswith("h"), hv)
        else:
            cats, vals = make_data(ctx, n, sc, rnd, halves=hv)
        if kind == "missing":
            its.append(missing_q(rnd, ctx, cats, vals, sc, horiz=True))
            continue
        f = fig(ctx_bar(ctx, cats, vals, sc, horizontal=True))
        if kind == "read":
            its.append(read_q(rnd, ctx, cats, vals, sc, f, False, horiz=True))
        elif kind == "readh":
            its.append(read_q(rnd, ctx, cats, vals, sc, f, True, horiz=True))
        elif kind == "which":
            its.append(which_q(rnd, ctx, cats, vals, sc, f, False))
        elif kind == "whichh":
            its.append(which_q(rnd, ctx, cats, vals, sc, f, True))
        elif kind == "step":
            its.append(step_q(f, sc))
        elif kind in ("longest", "shortest"):
            its.append(most_q(ctx, cats, vals, sc, f, kind == "longest", horiz=True))
        elif kind == "list":
            its.append(list_q(ctx, cats, vals, sc, f, horiz=True))
        else:
            its.append(compare_q(rnd, ctx, cats, vals, sc, f, kind, horiz=True))
    assert len(its) == 20, len(its)
    return {"title": "Horizontal bar graphs", "items": its}


# ------------------------------------------------------------ set 5: word problems
def set_words():
    its = []
    # favourite fruit at recess (all P3 students), vertical, scale 10
    fc = ["Apple", "Banana", "Papaya", "Melon", "Grapes"]
    fv = [45, 30, 15, 50, 25]
    ff = fig(bar_svg("Favourite fruit at recess (all P3 students)", "Fruit", "Students", fc, fv, 10,
                     label="bar graph: favourite fruit at recess"))
    its.append(mcq(ff + "How many more P3 students chose melon than papaya?", fmt(35, STU),
                   [fmt(x, STU) for x in [65, 40, 30, 3]],
                   "The scale counts by 10s. Melon ends on 50. Papaya ends halfway between 10 and 20, so 15. "
                   "50 − 15 = 35. (40 reads papaya as 10, and 30 reads it as 20.)"))
    its.append(mcq(ff + "How many P3 students chose a fruit altogether?", fmt(165, STU),
                   [fmt(x, STU) for x in [150, 180, 140]],
                   "Apple 45, banana 30, papaya 15, melon 50, grapes 25. 45 + 30 + 15 + 50 + 25 = 165. "
                   "(150 reads every bar between two lines as the line below; 140 leaves out grapes.)"))
    its.append(mcq(ff + "The canteen vendor gives 1 fruit to each student who chose apple or grapes. "
                   "How many fruits does she need?", "70 fruits", ["20 fruits", "60 fruits", "80 fruits"],
                   "Apple 45 (halfway between 40 and 50). Grapes 25 (halfway between 20 and 30). 45 + 25 = 70. "
                   "(20 subtracts instead of adding. 60 reads both bars as the line below.)"))
    its.append(mcq(ff + "The bananas come in bunches of 5. How many bunches are needed so that each student "
                   "who chose banana gets 1 banana?", "6 bunches", ["25 bunches", "35 bunches", "150 bunches"],
                   "Banana ends on the line for 30, so 30 students need 30 bananas. 30 ÷ 5 = 6 bunches. "
                   "(25 subtracts 5, and 150 multiplies by 5.)"))
    its.append(mcq(ff + "Which sentence is true?", "Twice as many chose banana as papaya.",
                   ["Apple is the most popular fruit.", "Grapes and papaya are the same.",
                    "Fewer chose melon than apple."],
                   "Banana 30 and papaya 15: 2 × 15 = 30, so twice as many chose banana. "
                   "Melon (50) is the most popular, not apple (45). Grapes (25) and papaya (15) are different."))
    # books borrowed from the library, horizontal, scale 10
    bc = DAYS[:5]
    bv = [40, 65, 50, 85, 30]
    bf = fig(bar_svg("Books borrowed from the library", "Day", "Books", bc, bv, 10, horizontal=True,
                     label="bar graph: books borrowed from the library"))
    its.append(mcq(bf + "On which day were the most books borrowed?", "Thursday", ["Tuesday", "Wednesday", "Monday"],
                   "The longest bar is Thursday. It ends halfway between 80 and 90, so 85 books."))
    its.append(mcq(bf + "How many fewer books were borrowed on Friday than on Thursday?", fmt(55, BOOK),
                   [fmt(x, BOOK) for x in [115, 50, 60]],
                   "Thursday 85 (halfway between 80 and 90). Friday 30. 85 − 30 = 55. "
                   "(Reading Thursday as 80 gives 50, as 90 gives 60. 115 adds them.)"))
    its.append(mcq(bf + "How many books were borrowed from Monday to Friday?", fmt(270, BOOK),
                   [fmt(x, BOOK) for x in [260, 280, 240]],
                   "40 + 65 + 50 + 85 + 30 = 270. (260 reads Tuesday as 60 and Thursday as 80. "
                   "240 leaves out Friday.)"))
    its.append(mcq(bf + "Mrs Lim hoped for 300 books to be borrowed this week. How many more books were needed "
                   "to reach 300?", fmt(30, BOOK), [fmt(x, BOOK) for x in [570, 40, 20]],
                   "Step 1: total borrowed: 40 + 65 + 50 + 85 + 30 = 270. Step 2: 300 − 270 = 30 more books. "
                   "(40 and 20 come from reading the bars between two lines wrongly: 300 − 260 and 300 − 280.)"))
    its.append(mcq(bf + "On which two days were 90 books borrowed altogether?", "Monday and Wednesday",
                   ["Tuesday and Friday", "Monday and Friday", "Wednesday and Friday"],
                   "Monday 40 + Wednesday 50 = 90. (Tuesday and Friday: 65 + 30 = 95. Monday and Friday: 70. "
                   "Wednesday and Friday: 80.)"))
    # how we go to school, horizontal, scale 5
    gc = ["Walk", "Bus", "MRT", "Car"]
    gv = [25, 40, 15, 30]
    gf = fig(bar_svg("How P3 students go to school", "Way", "Students", gc, gv, 5, horizontal=True,
                     label="bar graph: how p3 students go to school"))
    its.append(mcq(gf + "Next term, 10 of the students who come by car will take the bus instead. "
                   "How many students will take the bus then?", fmt(50, STU), [fmt(x, STU) for x in [20, 30, 40]],
                   "Bus now: 40. 10 more will take the bus: 40 + 10 = 50. "
                   "(20 is the new number of car students: 30 − 10.)"))
    its.append(mcq(gf + "Which two ways together have the same number of students as the bus?", "Walk and MRT",
                   ["MRT and Car", "Walk and Car", "Car and Bus"],
                   "Bus: 40. Walk 25 + MRT 15 = 40. (MRT and Car: 45. Walk and Car: 55.)"))
    its.append(mcq(gf + "Mr Tan says, “More than half of these students take the bus.” Is he right?",
                   "No. 40 is less than half of 110.",
                   ["Yes. The bus bar is the longest.", "Yes. 40 students take the bus.", "No. Nobody takes the bus."],
                   "Total: 25 + 40 + 15 + 30 = 110. Half of 110 is 55. Only 40 take the bus. "
                   "The longest bar shows the most popular way, not more than half."))
    # bar-model word problems (data from bar graphs and surveys)
    m = model_svg([("Mei Ling", [(24, "24", "u")]), ("Raju", [(24, "", "u"), (9, "9", "o")])], right="?",
                  label="bar model: stickers of mei ling and raju")
    its.append(mcq(fig(m) + "Mei Ling collected 24 stickers. Raju collected 9 more stickers than Mei Ling. "
                   "How many stickers did they collect altogether?", fmt(57, STK),
                   [fmt(x, STK) for x in [33, 15, 48]],
                   "Step 1: Raju: 24 + 9 = 33. Step 2: altogether: 24 + 33 = 57. "
                   "(33 is only Raju’s stickers. Stop only when you have answered the question.)"))
    m = model_svg([("Week 1", [(150, "150", "u")]), ("Week 2", [(150, "", "u")] * 3)], under=[(1, 0, 450, "?")],
                  label="bar model: books borrowed in week 1 and week 2")
    its.append(mcq(fig(m) + "In a bar graph of books borrowed, the bar for Week 1 shows 150 books. The bar for "
                   "Week 2 is 3 times as long. How many books were borrowed in Week 2?", fmt(450, BOOK),
                   [fmt(x, BOOK) for x in [153, 600, 50]],
                   "1 unit = 150. Week 2 is 3 units: 3 × 150 = 450 books. "
                   "(153 adds 3. 600 is both weeks together.)"))
    m = model_svg([("Apple", [(1, "", "u")] * 2), ("Banana", [(1, "", "u")])], right="36",
                  under=[(0, 0, 2, "?")], label="bar model: apple and banana votes")
    its.append(mcq(fig(m) + "In a class survey, twice as many students chose apple as banana. "
                   "36 students chose apple or banana. How many students chose apple?", fmt(24, STU),
                   [fmt(x, STU) for x in [12, 18, 72]],
                   "Apple is 2 units and banana is 1 unit. 3 units = 36, so 1 unit = 36 ÷ 3 = 12. "
                   "Apple: 2 units = 2 × 12 = 24. (12 is banana. 18 halves 36, but there are 3 units, not 2.)"))
    m = model_svg([("Milk tea", [(85, "85", "u")]), ("Taro", [(48, "?", "u"), (37, "37", "w")])],
                  label="bar model: cups of milk tea and taro tea")
    its.append(mcq(fig(m) + "A bubble tea shop sold 85 cups of milk tea. It sold 37 fewer cups of taro tea. "
                   "How many cups of taro tea did it sell?", fmt(48, CUP), [fmt(x, CUP) for x in [122, 52, 58]],
                   "Taro is shorter by 37. 85 − 37 = 48. Rename 1 ten as 10 ones: 15 − 7 = 8, 7 − 3 = 4. "
                   "(52 takes 5 − 7 as 7 − 5. 122 adds instead of subtracting.)"))
    m = model_svg([("Red", [(240, "240", "u")]), ("Blue", [(240, "", "u"), (75, "75", "o")]),
                   ("Green", [(265, "?", "u"), (50, "50", "w")])], label="bar model: sports day points")
    its.append(mcq(fig(m) + "On Sports Day, Red House got 240 points. Blue House got 75 more points than Red House. "
                   "Green House got 50 fewer points than Blue House. How many points did Green House get?",
                   fmt(265, PT), [fmt(x, PT) for x in [315, 190, 365]],
                   "Step 1: Blue: 240 + 75 = 315. Step 2: Green: 315 − 50 = 265. "
                   "(315 is Blue House. 190 takes 50 from Red House instead of Blue House. 365 adds the 50 instead of subtracting.)"))
    m = model_svg([("Apple", [(48, "", "u"), (16, "16", "o")]), ("Papaya", [(48, "", "u")])],
                  top=(0, 64, "64"), right="?", label="bar model: apple and papaya votes")
    its.append(mcq(fig(m) + "In a survey, 64 students chose apple. This is 16 more than the number who chose "
                   "papaya. How many students chose apple or papaya?", fmt(112, STU),
                   [fmt(x, STU) for x in [48, 144, 80]],
                   "Papaya is 16 fewer than apple: 64 − 16 = 48. Altogether: 64 + 48 = 112. "
                   "(144 adds 16 to get papaya, but papaya is the smaller bar. 48 is only papaya.)"))
    m = model_svg([("June", [(18, "18", "u")]), ("July", [(12, "", "u"), (6, "6", "w")]),
                   ("August", [(12, "", "u"), (12, "", "u")])], under=[(2, 0, 24, "?")],
                  label="bar model: books hui min read")
    its.append(mcq(fig(m) + "Hui Min drew a bar graph of the books she read. She read 18 books in June. "
                   "In July she read 6 fewer books than in June. In August she read twice as many books as in July. "
                   "How many books did she read in August?", fmt(24, BOOK), [fmt(x, BOOK) for x in [12, 36, 30]],
                   "Step 1: July: 18 − 6 = 12. Step 2: August is 2 units of 12: 2 × 12 = 24. "
                   "(36 doubles June instead of July. 12 is July.)"))
    assert len(its) == 20, len(its)
    return {"title": "Word problems: fruit, books and more", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


def body_html():
    fc = ["Apple", "Banana", "Papaya", "Grapes"]
    fv = [12, 7, 4, 10]
    bc = DAYS[:5]
    bv = [30, 55, 70, 45, 20]
    m = model_svg([("Wed", [(70, "70", "u")]), ("Fri", [(20, "20", "u"), (50, "?", "w")])],
                  label="bar model: books borrowed on wednesday and friday")
    return (
        "<h2>How to read a bar graph</h2>"
        "<p>A bar graph uses bars to show numbers. Read it in three steps. "
        "1. Read the <b>title</b> and the labels. "
        "2. Find what the <b>scale</b> counts by: 1s, 2s, 5s or 10s. "
        "3. Go from the end of the bar straight across to the scale, and read the number.</p>"
        "<figure class='sn-fig'>" + bar_svg("Favourite fruit at recess", "Fruit", "Students", fc, fv, 2,
                                            label="bar graph: favourite fruit at recess") +
        "<figcaption>The scale counts by 2s. Apple ends on the line for 12. Banana ends halfway between 6 and 8, "
        "so 7 students chose bananas.</figcaption></figure>" +
        ex("Example 1", "How many more students chose apples than bananas?",
           "Apple: 12. Banana: 7. How many more means subtract: 12 − 7 = 5.", "5 more students") +
        "<h2>Different scales</h2>"
        "<p>Each line on the scale is not always 1. If the scale counts by 10s, the 3rd line is 30, not 3. "
        "A bar that ends halfway between 50 and 60 shows 55.</p>"
        "<p>Some bar graphs are <b>horizontal</b>. The bars go across, and the scale is at the bottom. "
        "Read them in the same way.</p>"
        "<figure class='sn-fig'>" + bar_svg("Books borrowed from the library", "Day", "Books", bc, bv, 10,
                                            horizontal=True, label="bar graph: books borrowed from the library") +
        "<figcaption>The scale counts by 10s. Tuesday ends halfway between 50 and 60, so 55 books were borrowed "
        "on Tuesday.</figcaption></figure>" +
        "<figure class='sn-fig'>" + m +
        "<figcaption>Bar model: the Friday bar is shorter. The missing part is the difference.</figcaption></figure>" +
        ex("Example 2", "How many more books were borrowed on Wednesday than on Friday?",
           "Wednesday: 70. Friday: 20. The model shows the difference: 70 − 20 = 50.", "50 more books") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Counting the grid lines as 1 each", "Read the numbers on the scale: 10, 20, 30 …"],
            ["Reading the bar next door", "Put your finger on the right bar, then go across"],
            ["Reading a bar between two lines as the line below or above", "Halfway between 30 and 40 is 35"],
            ["Adding when the question asks how many more", "How many more or fewer means subtract"],
            ["Stopping after step 1", "Read the question again: what does it ask for?"],
        ])
    )


FAQ = [
    {"q": "What do P3 students learn about bar graphs?",
     "a": "In Primary 3, students read and interpret bar graphs, including graphs whose scale counts by 2s, 5s or 10s and horizontal bar graphs. They use the data to compare, find totals and solve word problems."},
    {"q": "How do I help my child read a bar graph with a scale?",
     "a": "Ask your child to read the numbers on the scale first and say what it counts by. Then put a finger on the end of the bar and go straight across to the scale."},
    {"q": "What is the most common mistake with bar graphs?",
     "a": "The most common mistake is counting each grid line as 1 when the scale counts by 2s, 5s or 10s. Reading the bar next door and misreading bars that end between two lines are also common."},
    {"q": "Are bar graphs in the MOE Primary 3 syllabus?",
     "a": "Yes. Reading and interpreting data from bar graphs, using different scales on the axis, is part of Statistics in the MOE 2021 Primary 3 Mathematics syllabus. Data analysis skills like these are used all the way to the PSLE in Primary 6."},
]


# ------------------------------------------------------------ assemble
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


SVG = re.compile(r"(<svg.*?</svg>)", re.S)
GAP = re.compile(r"(?<=\d) (?=\d{3}(?!\d))")


def nbsp(s):
    """Use a no-break space between digit groups (10 000) everywhere outside SVG markup."""
    return "".join(p if p.startswith("<svg") else GAP.sub(NB, p) for p in SVG.split(s))


def fix_spaces(u):
    for k in ("title", "seo_title", "short_title", "meta_desc", "key_big", "key_sub", "body_html", "standard_text"):
        u[k] = nbsp(u[k])
    for f in u["faq"]:
        f["q"], f["a"] = nbsp(f["q"]), nbsp(f["a"])
    for s in u["sets"]:
        s["title"] = nbsp(s["title"])
        for it in s["items"]:
            it["q"], it["e"] = nbsp(it["q"]), nbsp(it["e"])
            it["c"] = [nbsp(c) for c in it["c"]]
    return u


def mark_large(u, pattern):
    """Tag pictures that must print larger (bar graphs, A to D panels, bar models)."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen_unit():
    ASKED.clear()
    rnd = random.Random(63813)
    PK = Picker(rnd)
    sets = [set_scale1(rnd, PK), set_scales(rnd, PK), set_compare(rnd, PK), set_horizontal(rnd, PK), set_words()]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["e"], it
            assert it["q"].count("<svg") <= 1, it["q"]
            assert "<svg" not in it["e"]
            k = it["q"] + "|" + "|".join(sorted(it["c"]))
            assert k not in seen, it["q"]
            seen.add(k)
    u = {
        "country": "sg", "subject": "maths", "grade": "primary-3", "slug": "bar-graphs", "sort": 13,
        "updated": UPDATED, "pdf_url": "",
        "title": "Primary 3 Bar Graphs",
        "seo_title": "P3 Bar Graphs Worksheets: Free Primary 3 Maths with Answers (MOE Syllabus)",
        "short_title": "Bar graphs",
        "domain": "Statistics",
        "standard_code": "Primary 3: Statistics",
        "standard_url": "https://www.moe.gov.sg/primary/curriculum/syllabus",
        "standard_text": "Reading and interpreting data from bar graphs; using different scales on the axis",
        "meta_desc": "Free P3 maths: read bar graphs with scales of 1, 2, 5 and 10, horizontal bar graphs, compare "
                     "and total data, word problems. 100 questions with answers.",
        "key_big": "Check what the scale counts by, then read across from the end of the bar.",
        "key_sub": "If the scale counts by 10s and a bar ends halfway between 30 and 40, it shows 35.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    assert len(u["meta_desc"]) <= 160, len(u["meta_desc"])
    return fix_spaces(mark_large(u, "(bar graph|bar model)"))


if __name__ == "__main__":
    u = gen_unit()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
