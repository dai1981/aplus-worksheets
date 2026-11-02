# -*- coding: utf-8 -*-
"""
CA-BC Grade 3 Math (BC Mathematics Curriculum, Data and probability):
one-to-one correspondence with bar graphs, pictographs, charts, and tables.
  python3 tools/gen_cabc_math_g3_graphs.py
Tally charts and tables, pictographs where 1 symbol = 1, bar graphs with a scale of 1 and then 2,
comparing and totalling data, and asking questions and drawing conclusions in BC contexts
(favourite sports, salmon at the creek, birds in Stanley Park, rainy days in Vancouver).
Wrong answers come from real student mistakes: miscounting tally marks (a group of 5 read as 4 or as 1),
reading the wrong bar or row (the one next to it), counting one too many or too few, reading a bar between
two lines as the line below or above, counting grid spaces instead of reading the scale, adding instead of
subtracting. Every value is checked in code. HTML attributes use single quotes (no backslashes in the JSON).
Canadian English.
"""
import json, re, math, os, random

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-3")
UPDATED = "2026-11-02"
GREEN = "#006633"
BAR = "#2e8b57"
FILL = "#cfe6d6"
FILL2 = "#e6f2ea"
RED = "#c0392b"
INK = "#2b2b2b"
GRID = "#c9d3cc"
MUTE = "#555555"
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


# ------------------------------------------------------------ pictograph symbols
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
    return "<polygon points='%s' fill='%s'/>" % (" ".join("%.1f,%.1f" % p for p in star_pts(cx, cy)), col)


SYMS = ["circle", "star", "square"]


# ------------------------------------------------------------ contexts
class Ctx:
    def __init__(self, title, axis, cats, unit, ask, more, fewer, both, total, scales, pic, source, ph=None,
                 ordered=False, minv=1):
        self.title, self.axis, self.cats, self.unit = title, axis, cats, unit
        self.ask_f, self.more_f, self.fewer_f, self.both_f, self.total = ask, more, fewer, both, total
        self.scales, self.pic, self.ph, self.ordered, self.minv = scales, pic, ph or {}, ordered, minv
        self.source = source

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


STU = ("student", "students")
SAL = ("salmon", "salmon")
BIRD = ("bird", "birds")
LAP = ("lap", "laps")
DAY = ("day", "days")
LOWER = lambda cs: {c: c.lower() for c in cs}
TEACH = ["Ms. Lee", "Mr. Gill", "Ms. Ward", "Mr. Chen"]
POSS = {t: t + "’s class" for t in TEACH}
SPORTS = ["Soccer", "Hockey", "Lacrosse", "Swimming", "Basketball"]
SALMON = ["Chinook", "Coho", "Sockeye", "Pink", "Chum"]

CTXS = [
    Ctx("Favourite sport", "Sport", SPORTS, STU,
        "How many students chose {a}?", "How many more students chose {a} than {b}?",
        "How many fewer students chose {a} than {b}?", "How many students chose {a} or {b}?",
        "How many students voted altogether?", [1, 2], True, "Source: Grade 3 class vote", ph=LOWER(SPORTS)),
    Ctx("Salmon seen at the creek", "Kind of salmon", SALMON, SAL,
        "How many {a} salmon were seen?", "How many more {a} salmon than {b} salmon were seen?",
        "How many fewer {a} salmon than {b} salmon were seen?",
        "How many {a} and {b} salmon were seen altogether?",
        "How many salmon were seen altogether?", [1, 2], True, "Source: Grade 3 field trip count",
        ph={"Chinook": "Chinook", "Coho": "coho", "Sockeye": "sockeye", "Pink": "pink", "Chum": "chum"}),
    Ctx("How we get to school", "Way to school", ["Walk", "Car", "Bus", "Bike"], STU,
        "How many students {a} to school?", "How many more students {a} to school than {b}?",
        "How many fewer students {a} to school than {b}?", "How many students {a} or {b} to school?",
        "How many students are in the survey altogether?", [1, 2], True, "Source: class survey",
        ph={"Walk": "walk", "Car": "come by car", "Bus": "take the bus", "Bike": "ride a bike"}),
    Ctx("Birds seen in Stanley Park", "Bird", ["Eagle", "Heron", "Crow", "Duck", "Gull"], BIRD,
        "How many {a} were seen?", "How many more {a} than {b} were seen?",
        "How many fewer {a} than {b} were seen?", "How many {a} and {b} were seen altogether?",
        "How many birds were seen altogether?", [1, 2], True, "Source: field trip bird count",
        ph={"Eagle": "bald eagles", "Heron": "herons", "Crow": "crows", "Duck": "ducks", "Gull": "gulls"}),
    Ctx("Favourite fruit", "Fruit", ["Apple", "Cherry", "Peach", "Pear", "Blueberry"], STU,
        "How many students chose {a}?", "How many more students chose {a} than {b}?",
        "How many fewer students chose {a} than {b}?", "How many students chose {a} or {b}?",
        "How many students voted altogether?", [1, 2], True, "Source: Grade 3 class vote",
        ph={"Apple": "apples", "Cherry": "cherries", "Peach": "peaches", "Pear": "pears", "Blueberry": "blueberries"}),
    Ctx("Books read in March", "Student", ["Liam", "Olivia", "Arjun", "Mei", "Ethan", "Simran"], ("book", "books"),
        "How many books did {a} read?", "How many more books did {a} read than {b}?",
        "How many fewer books did {a} read than {b}?", "How many books did {a} and {b} read altogether?",
        "How many books did the students read altogether?", [1, 2], True, "Source: class reading logs"),
    Ctx("Laps at the Terry Fox Run", "Student", ["Kai", "Leah", "Owen", "Zara", "Ryan"], LAP,
        "How many laps did {a} run?", "How many more laps did {a} run than {b}?",
        "How many fewer laps did {a} run than {b}?", "How many laps did {a} and {b} run altogether?",
        "How many laps did the students run altogether?", [1, 2], True, "Source: Terry Fox Run lap cards"),
    Ctx("Rainy days in Vancouver", "Month", ["Oct", "Nov", "Dec", "Jan", "Feb"], DAY,
        "How many rainy days were there in {a}?", "How many more rainy days were there in {a} than in {b}?",
        "How many fewer rainy days were there in {a} than in {b}?",
        "How many rainy days were there in {a} and {b} altogether?",
        "How many rainy days were there altogether?", [2], False, "Source: our class weather log", ordered=True,
        minv=11, ph={"Oct": "October", "Nov": "November", "Dec": "December", "Jan": "January", "Feb": "February"}),
    Ctx("Cans for the food bank", "Class", TEACH, ("can", "cans"),
        "How many cans did {a} collect?", "How many more cans did {a} collect than {b}?",
        "How many fewer cans did {a} collect than {b}?", "How many cans did {a} and {b} collect altogether?",
        "How many cans did the classes collect altogether?", [2], False, "Source: school food bank count",
        ph=POSS, minv=4),
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


def make_data(ctx, n, scale, rnd, maxv, ok=lambda v, c: True):
    """n different whole-number values from ctx.minv to maxv."""
    if ctx.ordered:
        start = rnd.randint(0, len(ctx.cats) - n)
        cats = ctx.cats[start:start + n]
    else:
        cats = rnd.sample(ctx.cats, n)
    for _ in range(5000):
        vals = [rnd.randint(max(ctx.minv, 1), maxv) for _ in range(n)]
        if len(set(vals)) != n:
            continue
        if not ok(vals, cats):
            continue
        return cats, vals
    raise ValueError("no data for " + ctx.title)


def source_line(y, src):
    return text(8, y, src, 14, anchor="start", col=MUTE, extra=" font-style='italic'")


# ------------------------------------------------------------ pictograph (1 symbol = 1)
def pic_part(title, cats, vals, sym, unit, missing=None, source=None, wrong_row=None):
    """Pictograph: one row per category, one symbol for each, key line at the bottom."""
    fs, rh, gap = 15, 26, 23
    lw = max(tw(c, fs) for c in cats) + 22
    m = max(max(vals), 4)
    W = lw + 12 + m * gap + 14
    keytxt = "= " + fmt(1, unit)
    kw = tw("Key:", fs, True) + 32 + tw(keytxt, fs)
    W = int(max(W, tw(title, 16, True) + 16, kw + 16, tw(source, 14) + 16 if source else 0))
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
        for j in range(v):
            s.append(symbol(sym, lw + 12 + j * gap + 9, y + rh / 2))
    ky = top + H_tab + 22
    x = (W - kw) / 2
    s.append(text(x, ky, "Key:", fs, anchor="start", bold=True))
    x += tw("Key:", fs, True) + 16
    s.append(symbol(sym, x, ky - 5))
    s.append(text(x + 14, ky, keytxt, fs, anchor="start"))
    H = ky + 8
    if source:
        s.append(source_line(ky + 24, source))
        H = ky + 30
    return (W, H, "".join(s))


def pic_svg(title, cats, vals, sym, unit, source=None, label=None, missing=None):
    return part_svg(pic_part(title, cats, vals, sym, unit, missing=missing, source=source),
                    label or "pictograph: " + title.lower())


def ctx_pic(ctx, cats, vals, sym, missing=None):
    return pic_svg(ctx.title, cats, vals, sym, ctx.unit, source=ctx.source, missing=missing)


# ------------------------------------------------------------ bar graph
def bar_part(title, cat_axis, val_axis, cats, vals, scale, top_v=None, col=BAR, source=None):
    """Vertical bar graph with a gridline at every step of the scale."""
    fs = 14
    top_v = top_v or int(math.ceil(max(vals) / scale) * scale)
    if top_v // scale < 4:
        top_v = 4 * scale
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
    W = max(W, tw(title, 16, True) + 16, tw(source, 14) + 16 if source else 0)
    if title:
        s.append(text(W / 2, 18, title, 16, bold=True))
    for k in range(nt + 1):
        y = yb - k * gy
        s.append("<line x1='%d' y1='%.1f' x2='%d' y2='%.1f' stroke='%s' stroke-width='1'/>" % (x0, y, x0 + pw, y, GRID))
        s.append(text(x0 - 5, y + 5, k * scale, fs, anchor="end"))
    for i, (c, v) in enumerate(zip(cats, vals)):
        cx = x0 + slot * i + slot / 2
        bw = min(30, slot * 0.62)
        h = v / scale * gy
        s.append("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' fill='%s'/>" % (cx - bw / 2, yb - h, bw, h, col))
        s.append(text(cx, yb + 17, c, fs))
    s.append("<path d='M%d %d V%d H%d' fill='none' stroke='%s' stroke-width='2'/>" % (x0, y0 - 6, yb, x0 + pw, INK))
    s.append(text(x0 + pw / 2, yb + 36, cat_axis, fs, bold=True))
    mid = y0 + ph / 2
    s.append(text(13, mid, val_axis, fs, bold=True, extra=" transform='rotate(-90 13 %.1f)'" % mid))
    H = yb + 42
    if source:
        s.append(source_line(yb + 60, source))
        H = yb + 66
    assert tw(val_axis, fs, True) < ph + 26, (val_axis, ph)
    return (W, H, "".join(s))


def bar_svg(title, cat_axis, val_axis, cats, vals, scale, label="bar graph", source=None):
    return part_svg(bar_part(title, cat_axis, val_axis, cats, vals, scale, source=source), label)


def val_axis(ctx):
    return "Rainy days" if ctx.unit == DAY else ctx.unit[1].capitalize()


def ctx_bar(ctx, cats, vals, scale):
    return bar_svg(ctx.title, ctx.axis, val_axis(ctx), cats, vals, scale,
                   label="bar graph: " + ctx.title.lower(), source=ctx.source)


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
        h = v / scale * gy
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


# ------------------------------------------------------------ tally marks and tables
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
    W = max(tally_width(v) + 30, 80)
    return svg_wrap(W, 34, "<rect x='1' y='1' width='%d' height='32' rx='4' fill='#ffffff' stroke='%s' stroke-width='1.5'/>"
                    % (W - 2, GRID) + tally_marks(15, 17, v), "tally marks")


def table_part(title, head, cats, vals, tally=True, count=True, missing=None, count_head="Total"):
    """Tally chart or table: category | tally | total. `missing` = row whose total is a red ?."""
    fs, rh = 15, 28
    c1 = int(max(max(tw(c, fs) for c in cats), tw(head, fs, True)) + 20)
    cols = [c1]
    if tally:
        cols.append(int(max(max(tally_width(v) for v in vals) + 24, 70)))
    if count:
        cols.append(int(max(tw(count_head, fs, True) + 20, 64)))
    top = 28
    tot = sum(cols)
    W = int(max(tot + 8, tw(title, 16, True) + 16))
    x0 = (W - tot) / 2
    s = [text(W / 2, 19, title, 16, bold=True)]
    rows = [(head, None)] + list(zip(cats, vals))
    for r, (c, v) in enumerate(rows):
        y = top + r * rh
        hd = r == 0
        x = x0
        for k, cw in enumerate(cols):
            s.append("<rect x='%.1f' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.5'/>"
                     % (x, y, cw, rh, FILL2 if hd or k == 0 else "#ffffff", GREEN))
            name = "cnt" if (k == 2 or (k == 1 and not tally)) else ("tally" if k == 1 else "cat")
            if name == "cat":
                s.append(text(x + 10, y + 19, c, fs, anchor="start", bold=hd))
            elif hd:
                s.append(text(x + 10 if name == "tally" else x + cw / 2, y + 19, "Tally" if name == "tally" else count_head,
                              fs, anchor="start" if name == "tally" else "middle", bold=True))
            elif name == "tally":
                s.append(tally_marks(x + 14, y + rh / 2, v))
            elif r - 1 == missing:
                s.append(text(x + cw / 2, y + 20, "?", 17, bold=True, col=RED))
            else:
                s.append(text(x + cw / 2, y + 19, v, fs))
            x += cw
    H = top + len(rows) * rh + 4
    return (W, H, "".join(s))


def table_svg(title, head, cats, vals, label, **kw):
    return part_svg(table_part(title, head, cats, vals, **kw), label)


# ------------------------------------------------------------ reading text and mistakes
def read_pic(c, v, sym):
    return "Count the %ss in the %s row: %s. Each %s stands for 1, so the row shows %d." % (sym, c, ones(v, sym), sym, v)


def read_bar(c, v, scale):
    if v % scale:
        lo = v - v % scale
        return "The bar for %s ends halfway between %d and %d, so it shows %d." % (c, lo, lo + scale, v)
    return "The bar for %s ends on the line for %d." % (c, v)


def tally_text(v):
    g, r = v // 5, v % 5
    if g and r:
        return "%s of 5, then %d more: %s, then %s. So %d." % (
            ones(g, "group"), r, ", ".join(str(5 * k) for k in range(1, g + 1)),
            ", ".join(str(5 * g + k) for k in range(1, r + 1)), v)
    if g:
        return "%s of 5: %s. So %d." % (ones(g, "group"), ", ".join(str(5 * k) for k in range(1, g + 1)), v)
    return "%d single marks." % r


def tally_cands(v):
    g, r = v // 5, v % 5
    return [g * 4 + r, g + r, v + 1, v - 1, v + 5]


def rainy(ctx, q):
    """Say “rainy days”, not just “days”, in questions about the rainy-day graph."""
    return q.replace(" days?", " rainy days?") if ctx.unit == DAY else q


def neighbour(n, j):
    return j + 1 if j + 1 < n else j - 1


ASKED = set()


def pick_row(rnd, ctx, cats, js):
    """A row/bar that has not been asked about before in this context (so no two questions read the same)."""
    fresh = [j for j in js if (ctx.title, cats[j]) not in ASKED]
    j = rnd.choice(fresh or js)
    ASKED.add((ctx.title, cats[j]))
    return j


# ------------------------------------------------------------ set 1: tally charts and tables
def set_tally(rnd):
    its = []
    for v in (7, 12, 9, 16):
        g, r = v // 5, v % 5
        e = ("Each group of 5 is four lines with one line across. Count the groups by 5s, then count on the "
             "single marks. %s" % tally_text(v))
        if g:
            e += " (%d counts each group as 4. Count the line across too.)" % (g * 4 + r)
        its.append(mcq(fig(tally_only_svg(v)) + "What number do these tally marks show?", v, tally_cands(v), e))
    # 5: which tally shows 13 (A to D)
    order = [12, 18, 13, 14]
    pos = order.index(13)
    s = []
    for k, v in enumerate(order):
        x0, y0 = (k % 2) * 170, (k // 2) * 44
        s.append(text(x0 + 8, y0 + 27, "ABCD"[k], 17, anchor="start", bold=True))
        s.append(tally_marks(x0 + 34, y0 + 21, v))
        assert x0 + 34 + tally_width(v) < x0 + 166
    svg = svg_wrap(340, 88, "".join(s), "four sets of tally marks")
    its.append(mcq_fixed(fig(svg) + "Which tally marks show 13?", ["A", "B", "C", "D"], pos,
                         "13 = 5 + 5 + 3, so look for 2 groups of 5 and 3 single marks. That is C. "
                         "A shows 12 (one mark too few), B shows 18 (one group of 5 too many) and D shows 14 (one mark too many)."))
    # 6-10 tally chart: favourite sport
    cats = ["Soccer", "Hockey", "Lacrosse", "Swimming", "Basketball"]
    vals = [11, 8, 4, 7, 6]
    f = fig(table_svg("Favourite sport", "Sport", cats, vals, "tally chart: favourite sport", missing=0))
    its.append(mcq(f + "What number should go in the Total column for Soccer?", 11, [9, 3, 12, 10],
                   "Soccer has %s (9 counts the group of 5 as 4 marks.)" % tally_text(11)))
    its.append(mcq(f + "How many students chose hockey?", fmt(8, STU), [fmt(x, STU) for x in [4, 7, 9]],
                   "Find the Hockey row. The tally shows %s Do not read the Lacrosse row below it (4)." % tally_text(8)))
    its.append(mcq(f + "Which sport did the fewest students choose?", "Lacrosse", ["Basketball", "Swimming", "Hockey"],
                   "Lacrosse has only 4 single marks. Every other sport has at least one group of 5."))
    its.append(mcq(f + "How many more students chose hockey than swimming?", fmt(1, STU),
                   [fmt(x, STU) for x in [15, 2, 3]],
                   "Hockey 8, swimming 7. How many more means find the difference: 8 − 7 = 1. "
                   "(15 adds them instead.)"))
    its.append(mcq(f + "Every student voted once. How many students voted?", fmt(36, STU),
                   [fmt(x, STU) for x in [25, 31, 30]],
                   "Soccer 11, hockey 8, lacrosse 4, swimming 7, basketball 6. "
                   "11 + 8 + 4 + 7 + 6 = 36. (25 leaves out soccer, the row with the ?. 31 counts each group of 5 as 4.)"))
    # 11-14 table: weather in October (31 days)
    W_c = ["Rainy", "Cloudy", "Sunny", "Foggy"]
    W_v = [15, 9, 5, 2]
    assert sum(W_v) == 31
    f = fig(table_svg("Weather in Vancouver in October", "Weather", W_c, W_v, "table: weather in vancouver in october",
                      tally=False, count_head="Days"))
    its.append(mcq(f + "How many days in October were cloudy?", fmt(9, DAY), [fmt(x, DAY) for x in [15, 5, 10]],
                   "Find the Cloudy row, then read across to the Days column: 9. "
                   "(15 is the Rainy row above it, and 5 is the Sunny row below it.)"))
    its.append(mcq(f + "How many more rainy days than sunny days were there?", fmt(10, DAY),
                   [fmt(x, DAY) for x in [20, 6, 11]],
                   "Rainy 15, sunny 5. 15 − 5 = 10 more rainy days. (20 adds instead of subtracting; "
                   "6 uses the Cloudy row by mistake: 15 − 9.)"))
    its.append(mcq(f + "October has 31 days. How many days were <b>not</b> rainy?", fmt(16, DAY),
                   [fmt(x, DAY) for x in [15, 14, 11]],
                   "31 − 15 = 16. Check: cloudy, sunny and foggy are 9 + 5 + 2 = 16. "
                   "(15 is the number of rainy days.)"))
    its.append(mcq(f + "Which kind of day happened most often?", "Rainy", ["Cloudy", "Foggy", "Sunny"],
                   "Rainy has the biggest number in the table: 15 days. That is almost half of October."))
    # 15-16 tally chart: birds at the feeder, with no totals
    cats = ["Chickadee", "Robin", "Junco", "Sparrow"]
    vals = [14, 6, 10, 9]
    f = fig(table_svg("Birds at our feeder", "Bird", cats, vals, "tally chart: birds at our feeder", count=False))
    its.append(mcq(f + "How many juncos came to the feeder?", fmt(10, BIRD), [fmt(x, BIRD) for x in [8, 9, 2, 11]],
                   "The Junco row has %s (8 counts each group as 4 marks; 9 is the Sparrow row below it.)"
                   % tally_text(10)))
    its.append(mcq(f + "Which bird came 14 times?", "Chickadee", ["Junco", "Sparrow", "Robin"],
                   "14 = 5 + 5 + 4. The Chickadee row has 2 groups of 5 and 4 single marks."))
    # 17 which tally is wrong
    its.append(mcq("Leah counts 8 votes for hockey. Which tally is right?", "1 group of 5 and 3 marks",
                   ["8 groups of 5", "1 group of 5 and 8 marks", "2 groups of 5 and 3 marks"],
                   "8 = 5 + 3. Draw 1 group of 5 (four lines and one line across) and 3 single marks."))
    # 18-20 word problems
    its.append(mcq("Noah makes a tally of the cars that go past the school. He draws 3 groups of 5 and 2 single marks. "
                   "How many cars went past?", fmt(17, ("car", "cars")),
                   [fmt(x, ("car", "cars")) for x in [14, 5, 32, 18]],
                   "Count the groups by 5s: 5, 10, 15. Then count on 2: 16, 17. So 17 cars. "
                   "(14 counts each group as 4. 5 counts each group as 1.)"))
    its.append(mcq("Sofia counted 19 votes for blueberries. How should she draw the tally?", "3 groups of 5 and 4 marks",
                   ["4 groups of 5 and 4 marks", "1 group of 5 and 9 marks", "19 groups of 5"],
                   "19 = 5 + 5 + 5 + 4. Draw 3 groups of 5 and 4 single marks. "
                   "Never leave 5 or more single marks: make another group of 5."))
    its.append(mcq("Ji-woo’s tally chart shows 2 groups of 5 for orcas and 1 group of 5 and 4 marks for seals on a "
                   "whale-watching trip near Victoria. How many more orcas than seals did the class see?", "1 more",
                   ["19 more", "5 more", "4 more"],
                   "Orcas: 5, 10, so 10. Seals: 5, then 6, 7, 8, 9, so 9. 10 − 9 = 1 more orca. "
                   "(19 adds them. 5 more compares only the groups.)"))
    assert len(its) == 20
    return {"title": "Tally charts and tables", "items": its}


# ------------------------------------------------------------ set 2: pictographs, 1 symbol = 1
def set_pictograph(rnd, PK):
    its = []
    plan = ["key", "read", "read", "most", "read", "which", "fewest", "read", "which", "more", "read",
            "fewer", "more", "both", "over", "draw", "two", "total", "missing", "more"]
    draw_done = False
    for i, kind in enumerate(plan):
        sym = SYMS[i % 3]
        if kind == "draw":
            its.append(mcq("Ava makes a pictograph of the books she read. The key says one star = 1 book. "
                           "Ava read 7 books. How many stars should she draw in her row?", "7 stars",
                           ["6 stars", "8 stars", "1 star"],
                           "One star stands for 1 book, so draw one star for each book: 7 books, 7 stars. "
                           "Count them as you draw so you do not draw one too many or one too few."))
            continue
        ctx = PK.next(lambda c: c.pic)
        n = 5 if i % 3 == 0 and len(ctx.cats) >= 5 else 4
        cats, vals = make_data(ctx, n, 1, rnd, 9, ok=lambda vs, cs: max(vs) - min(vs) >= 3)
        U = ctx.unit
        miss = None
        if kind == "missing":
            miss = pick_row(rnd, ctx, cats, list(range(n)))
        f = fig(ctx_pic(ctx, cats, vals, sym, missing=miss))
        keytxt = "Each %s stands for %s. " % (sym, fmt(1, U))
        if kind == "key":
            its.append(mcq(f + "Look at the key. What does one %s stand for?" % sym, fmt(1, U),
                           [fmt(n, U), fmt(max(vals), U), fmt(sum(vals), U), fmt(2, U)],
                           "The key is under the pictograph. It says one %s = %s. "
                           "So we count the %ss one by one." % (sym, fmt(1, U), sym)))
        elif kind == "read":
            j = pick_row(rnd, ctx, cats, list(range(n)))
            c, v = cats[j], vals[j]
            nb = neighbour(n, j)
            cand = [vals[nb], v + 1, v - 1] + [vals[k] for k in range(n) if k != j]
            its.append(mcq(f + ctx.ask(c), fmt(v, U), [fmt(x, U) for x in cand],
                           "%s (%d is the %s row next to it. Keep your finger on the right row.)"
                           % (read_pic(c, v, sym), vals[nb], cats[nb])))
        elif kind in ("most", "fewest"):
            j = vals.index(max(vals) if kind == "most" else min(vals))
            w = "most" if kind == "most" else "fewest"
            word = "longest" if kind == "most" else "shortest"
            q = "Which row shows the %s %s?" % (w, U[1])
            its.append(mcq(f + q, cats[j], [cats[k] for k in range(n) if k != j],
                           "Every %s stands for 1, so the %s row shows the %s. %s"
                           % (sym, word, w, read_pic(cats[j], vals[j], sym))))
        elif kind == "which":
            j = pick_row(rnd, ctx, cats, list(range(n)))
            v = vals[j]
            near = sorted([k for k in range(n) if k != j], key=lambda k: abs(vals[k] - v))
            its.append(mcq(f + "Which row shows %s?" % fmt(v, U), cats[j], [cats[k] for k in near],
                           "Count the %ss in each row. %s" % (sym, read_pic(cats[j], v, sym))))
        elif kind in ("more", "fewer"):
            pairs = [(a, b) for a in range(n) for b in range(n) if vals[a] - vals[b] >= 2]
            a, b = rnd.choice(pairs)
            d = vals[a] - vals[b]
            if kind == "more":
                q = ctx.more(cats[a], cats[b])
                e = ("%s%s: %d. %s: %d. How many more means find the difference: %d − %d = %d. "
                     "You can also count the extra %ss at the end of the %s row."
                     % (keytxt, cats[a], vals[a], cats[b], vals[b], vals[a], vals[b], d, sym, cats[a]))
            else:
                q = ctx.fewer(cats[b], cats[a])
                e = ("%s%s: %d. %s: %d. How many fewer means find the difference: %d − %d = %d."
                     % (keytxt, cats[b], vals[b], cats[a], vals[a], vals[a], vals[b], d))
            cand = [vals[a] + vals[b], d + 1, d - 1, vals[a]]
            its.append(mcq(f + q, fmt(d, U), [fmt(x, U) for x in cand], e + " (%d adds instead of subtracting.)"
                           % (vals[a] + vals[b])))
        elif kind == "both":
            a, b = rnd.sample(range(n), 2)
            t = vals[a] + vals[b]
            cand = [abs(vals[a] - vals[b]), t + 1, t - 1, max(vals[a], vals[b])]
            its.append(mcq(f + ctx.both(cats[a], cats[b]), fmt(t, U), [fmt(x, U) for x in cand],
                           "%s%s: %d. %s: %d. Altogether means add: %d + %d = %d."
                           % (keytxt, cats[a], vals[a], cats[b], vals[b], vals[a], vals[b], t)))
        elif kind == "over":
            lim = sorted(vals)[n // 2]
            ans = sum(1 for v in vals if v > lim)
            ge = sum(1 for v in vals if v >= lim)
            q = "How many rows show more than %d %s?" % (lim, U[1])
            cand = [ge, ans + 1, ans - 1, n - ans, ans + 2, n]
            its.append(mcq(f + q, str(ans) + (" row" if ans == 1 else " rows"),
                           [str(x) + (" row" if x == 1 else " rows") for x in cand],
                           "Read every row: %s. More than %d means %d itself does not count. Rows with more than %d: %s. That is %s."
                           % (", ".join("%s %d" % (c, v) for c, v in zip(cats, vals)), lim, lim, lim,
                              " and ".join(c for c, v in zip(cats, vals) if v > lim),
                              str(ans) + (" row" if ans == 1 else " rows"))))
        elif kind == "two":
            # which row has exactly 2 more than another row
            pairs = [(a, b) for a in range(n) for b in range(n) if vals[a] - vals[b] == 2]
            if not pairs:
                cats, vals = make_data(ctx, n, 1, rnd, 9, ok=lambda vs, cs: any(x - y == 2 for x in vs for y in vs))
                f = fig(ctx_pic(ctx, cats, vals, sym))
                pairs = [(a, b) for a in range(n) for b in range(n) if vals[a] - vals[b] == 2]
            a, b = pairs[0]
            alt = [k for k in range(n) if k not in (a, b)]
            minus = [k for k in range(n) if vals[k] == vals[b] - 2]
            cand = [cats[k] for k in minus] + [cats[k] for k in sorted(alt, key=lambda k: abs(vals[k] - vals[b]))] + [cats[b]]
            its.append(mcq(f + "Which row has 2 more %ss than the %s row?" % (sym, cats[b]), cats[a], cand,
                           "The %s row has %s. 2 more is %d + 2 = %d. The %s row has %d."
                           % (cats[b], ones(vals[b], sym), vals[b], vals[b] + 2, cats[a], vals[a])))
        elif kind == "total":
            t = sum(vals)
            cand = [t - vals[-1], t + 1, t - 1, n]
            its.append(mcq(f + ctx.total, fmt(t, U), [fmt(x, U) for x in cand],
                           "%sRead every row: %s. Add them: %s = %d. (%d leaves out the last row.)"
                           % (keytxt, ", ".join("%s %d" % (c, v) for c, v in zip(cats, vals)),
                              " + ".join(str(v) for v in vals), t, t - vals[-1])))
        elif kind == "missing":
            t = sum(vals)
            v = vals[miss]
            rest = t - v
            cand = [t, rest, v + 1, v - 1]
            its.append(mcq(f + "The %s row is not drawn yet. Altogether there are %s. "
                           "How many %s should the %s row show?" % (cats[miss], fmt(t, U), U[1], cats[miss]),
                           fmt(v, U), [fmt(x, U) for x in cand],
                           "Add the rows you can see: %s = %d. Then %d − %d = %d. So draw %s."
                           % (" + ".join(str(vals[k]) for k in range(n) if k != miss), rest, t, rest, v,
                              ones(v, sym))))
    assert len(its) == 20, len(its)
    return {"title": "Pictographs: 1 symbol = 1", "items": its}


# ------------------------------------------------------------ set 3: bar graphs, scale of 1 then 2
MATCH_WHY = {
    "swap": "two bars are the wrong way round",
    "low": "a bar is on the line below (it should be halfway between two lines)",
    "high": "one bar is one line too high",
    "lowl": "one bar is one line too low",
}


def match_q(rnd, pos, title, cats, vals, step):
    """Which bar graph (A to D) shows the data in the table? Wrong graphs come from real drawing mistakes."""
    wrong = []
    i, j = rnd.sample(range(len(vals)), 2)
    while vals[i] == vals[j]:
        i, j = rnd.sample(range(len(vals)), 2)
    sw = vals[:]
    sw[i], sw[j] = sw[j], sw[i]
    wrong.append(("swap", sw))
    halves = [k for k in range(len(vals)) if vals[k] % step]
    if halves:
        k = halves[0]
        w = vals[:]
        w[k] = vals[k] - step // 2
        wrong.append(("low", w))
    k = rnd.choice([k for k in range(len(vals)) if not halves or k != halves[0]])
    w = vals[:]
    w[k] = vals[k] + step
    wrong.append(("high", w))
    if len(wrong) < 3:
        k2 = rnd.choice([x for x in range(len(vals)) if x != k and vals[x] > step])
        w = vals[:]
        w[k2] = vals[k2] - step
        wrong.append(("lowl", w))
    wrong = wrong[:3]
    order = wrong[:]
    order.insert(pos, ("ok", vals))
    assert len({tuple(v) for _, v in order}) == 4
    top_v = int(math.ceil(max(max(v) for _, v in order) / step) * step)
    draws = [(lambda x0, y0, v=v: mini_bar(x0, y0, cats, v, step, top_v)) for _, v in order]
    svg = panel_svg(draws, "bar graphs: " + title.lower())
    why = ["%s: %s" % ("ABCD"[k], MATCH_WHY[tag]) for k, (tag, v) in enumerate(order) if tag != "ok"]
    sc_txt = ("the lines go up by 1s, with a number on every second line" if step == 1 and top_v > 8
              else "the scale goes up by %ds" % step)
    e = ("%s matches every number (%s). %s."
         % ("ABCD"[pos], sc_txt, "; ".join(why)))
    tb = "<b>%s</b>: %s. " % (title, ", ".join("%s %d" % (c, v) for c, v in zip(cats, vals)))
    return mcq_fixed(fig(svg) + tb + "Which bar graph shows this data?", ["A", "B", "C", "D"], pos, e)


def set_bar(rnd, PK):
    its = []
    plan = [(1, "step"), (1, "read"), (1, "which"), (1, "read"), (1, "most"), (1, "fewest"), (1, "read"),
            (1, "which"), (1, "list"), (1, "match"),
            (2, "step"), (2, "read"), (2, "readh"), (2, "which"), (2, "readh"), (2, "most"), (2, "read"),
            (2, "whichh"), (2, "list"), (2, "match")]
    for i, (sc, kind) in enumerate(plan):
        if kind == "match":
            if sc == 1:
                its.append(match_q(rnd, 1, "Laps at the Terry Fox Run", ["Kai", "Leah", "Owen", "Zara"], [6, 9, 4, 7], 1))
            else:
                its.append(match_q(rnd, 3, "Birds seen in Stanley Park", ["Crow", "Duck", "Gull", "Owl"],
                                   [12, 7, 16, 10], 2))
            continue
        ctx = PK.next(lambda c: sc in c.scales)
        half = kind in ("readh", "whichh")
        n = 5 if (i % 3 == 0 and len(ctx.cats) >= 5) else 4
        maxv = 10 if sc == 1 else 20
        if sc == 1:
            ok = lambda vs, cs: max(vs) - min(vs) >= 3
        else:
            ok = lambda vs, cs: max(vs) - min(vs) >= 4 and (
                not half or any(v % 2 and (ctx.title, c) not in ASKED for v, c in zip(vs, cs))) and (
                half or (kind == "list" and 1 <= sum(v % 2 for v in vs) <= 2) or (kind != "list" and sum(v % 2 for v in vs) <= 1))
        cats, vals = make_data(ctx, n, sc, rnd, maxv, ok=ok)
        f = fig(ctx_bar(ctx, cats, vals, sc))
        U = ctx.unit
        scl = "The scale goes up by %ds. " % sc if sc > 1 else "The scale goes up by 1s. "
        if kind in ("read", "readh"):
            if kind == "readh":
                j = pick_row(rnd, ctx, cats, [k for k, v in enumerate(vals) if v % sc])
            else:
                j = pick_row(rnd, ctx, cats, [k for k, v in enumerate(vals) if v % sc == 0])
            c, v = cats[j], vals[j]
            nb = neighbour(n, j)
            if v % sc:
                cand = [v - 1, v + 1, vals[nb], v + 2, v - 2]
                why = "(%d and %d are the lines below and above it.)" % (v - 1, v + 1)
            elif sc == 2:
                cand = [v // 2, vals[nb], v + 2, v - 2]
                why = "(%d counts the grid spaces, and %d is the %s bar next to it.)" % (v // 2, vals[nb], cats[nb])
            else:
                cand = [vals[nb], v + 1, v - 1, v + 2] + [vals[k] for k in range(n) if k != j]
                why = "(%d is the %s bar next to it. Look straight across from the top of the right bar.)" % (vals[nb], cats[nb])
            its.append(mcq(f + ctx.ask(c), fmt(v, U), [fmt(x, U) for x in cand],
                           "%s%s %s" % (scl, read_bar(c, v, sc), why)))
        elif kind == "step":
            its.append(mcq(f + "What does the scale on this bar graph count by?", "%ds" % sc,
                           ["%ds" % x for x in (1, 2, 5, 10) if x != sc],
                           "Read the numbers on the scale: 0, %d, %d, %d … Each line is %d more than the one below it, "
                           "so the scale counts by %ds." % (sc, 2 * sc, 3 * sc, sc, sc)
                           + (" (Do not count the lines by 1s.)" if sc > 1 else "")))
        elif kind in ("which", "whichh"):
            if half:
                j = pick_row(rnd, ctx, cats, [k for k, v in enumerate(vals) if v % sc])
            else:
                j = pick_row(rnd, ctx, cats, [k for k, v in enumerate(vals) if v % sc == 0])
            v = vals[j]
            near = sorted([k for k in range(n) if k != j], key=lambda k: abs(vals[k] - v))
            its.append(mcq(f + rainy(ctx, "Which bar shows %s?" % fmt(v, U)), cats[j], [cats[k] for k in near],
                           "%sFind %d on the scale and look across. %s" % (scl, v, read_bar(cats[j], v, sc))))
        elif kind in ("most", "fewest"):
            j = vals.index(max(vals) if kind == "most" else min(vals))
            word = "tallest" if kind == "most" else "shortest"
            q = rainy(ctx, "Which bar shows the %s %s?" % ("most" if kind == "most" else "fewest", U[1]))
            its.append(mcq(f + q, cats[j], [cats[k] for k in range(n) if k != j],
                           "The bar for %s is the %s one. %s" % (cats[j], word, read_bar(cats[j], vals[j], sc))))
        elif kind == "list":
            lst = lambda vs: ", ".join(str(v) for v in vs)
            sw = vals[:]
            sw[0], sw[1] = sw[1], sw[0]
            if sc == 2:
                wrong = [lst([v - v % 2 for v in vals]), lst([v + v % 2 for v in vals]), lst(sw)]
            else:
                wrong = [lst(sw), lst([v + 1 for v in vals]), lst(vals[::-1])]
            e = scl + " ".join(read_bar(c, v, sc) for c, v in zip(cats, vals))
            if sc == 2:
                e += (" (%s reads the bars between two lines as the line below, and %s as the line above.)"
                      % (lst([v - v % 2 for v in vals]), lst([v + v % 2 for v in vals])))
            else:
                e += " (%s swaps the first two bars.)" % lst(sw)
            its.append(mcq(f + "Which list matches this bar graph? The numbers are in this order: %s." % ", ".join(cats),
                           lst(vals), wrong, e))
    assert len(its) == 20, len(its)
    return {"title": "Bar graphs: scale of 1, then 2", "items": its}


# ------------------------------------------------------------ set 4: compare and total
def set_compare(rnd, PK):
    its = []
    plan = [("pic", "more"), ("bar1", "fewer"), ("bar1", "both"), ("pic", "total"), ("bar2", "more"),
            ("bar1", "more"), ("pic", "both"), ("bar2", "fewer"), ("bar1", "range"), ("pic", "notx"),
            ("bar2", "both"), ("bar1", "total"), ("pic", "tie"), ("bar2", "more"), ("bar1", "notx"),
            ("pic", "fewer"), ("bar2", "range"), ("bar1", "tie"), ("bar2", "total"), ("pic", "vsboth")]
    for i, (gk, kind) in enumerate(plan):
        if gk == "pic":
            ctx = PK.next(lambda c: c.pic)
            sc, maxv = 1, 9
        elif gk == "bar1":
            ctx = PK.next(lambda c: 1 in c.scales)
            sc, maxv = 1, 10
        else:
            ctx = PK.next(lambda c: 2 in c.scales)
            sc, maxv = 2, 20
        n = 5 if (i % 2 == 0 and len(ctx.cats) >= 5) else 4
        if gk == "bar2":
            ok = lambda vs, cs: max(vs) - min(vs) >= 6 and sum(v % 2 for v in vs) <= 1
        else:
            ok = lambda vs, cs: max(vs) - min(vs) >= 3
        if kind == "vsboth":
            ok2 = ok
            ok = lambda vs, cs: ok2(vs, cs) and max(vs) > sum(sorted(vs)[:2])
        cats, vals = make_data(ctx, n, sc, rnd, maxv, ok=ok)
        sym = SYMS[i % 3]
        f = fig(ctx_pic(ctx, cats, vals, sym) if gk == "pic" else ctx_bar(ctx, cats, vals, sc))
        U = ctx.unit
        rd = lambda k: "%s: %d" % (cats[k], vals[k])
        if kind in ("more", "fewer"):
            pairs = [(a, b) for a in range(n) for b in range(n) if vals[a] - vals[b] >= 2]
            a, b = rnd.choice(pairs)
            d = vals[a] - vals[b]
            q = ctx.more(cats[a], cats[b]) if kind == "more" else ctx.fewer(cats[b], cats[a])
            w = "more" if kind == "more" else "fewer"
            cand = [vals[a] + vals[b], vals[a] if kind == "more" else vals[b], d + 1, d - 1]
            its.append(mcq(f + q, fmt(d, U), [fmt(x, U) for x in cand],
                           "%s. %s. How many %s means find the difference: %d − %d = %d. (%d adds instead of subtracting.)"
                           % (rd(a), rd(b), w, vals[a], vals[b], d, vals[a] + vals[b])))
        elif kind == "both":
            a, b = rnd.sample(range(n), 2)
            t = vals[a] + vals[b]
            cand = [abs(vals[a] - vals[b]), t + 1, t - 1, t + sc if sc == 2 else max(vals[a], vals[b])]
            its.append(mcq(f + ctx.both(cats[a], cats[b]), fmt(t, U), [fmt(x, U) for x in cand],
                           "%s. %s. Altogether means add: %d + %d = %d." % (rd(a), rd(b), vals[a], vals[b], t)))
        elif kind == "total":
            t = sum(vals)
            cand = [t - vals[-1], t - vals[0], t + 1, t - 1]
            its.append(mcq(f + ctx.total, fmt(t, U), [fmt(x, U) for x in cand],
                           "Read every %s: %s. Add them all: %s = %d. Make sure you add every %s once."
                           % ("row" if gk == "pic" else "bar", ", ".join(rd(k) for k in range(n)),
                              " + ".join(str(v) for v in vals), t, "row" if gk == "pic" else "bar")))
        elif kind == "range":
            hi, lo = max(vals), min(vals)
            jh, jl = vals.index(hi), vals.index(lo)
            second = sorted(vals)[-2]
            cand = [hi + lo, hi, hi - second, hi - lo + 1]
            its.append(mcq(f + "How many more %s does the %s %s show than the %s %s?"
                           % (U[1], "tallest" if gk != "pic" else "longest", "bar" if gk != "pic" else "row",
                              "shortest", "bar" if gk != "pic" else "row"),
                           fmt(hi - lo, U), [fmt(x, U) for x in cand],
                           "The %s is %s (%d). The shortest is %s (%d). %d − %d = %d."
                           % ("tallest bar" if gk != "pic" else "longest row", cats[jh], hi, cats[jl], lo, hi, lo, hi - lo)))
        elif kind == "notx":
            j = pick_row(rnd, ctx, cats, list(range(n)))
            t = sum(vals)
            nb = neighbour(n, j)
            if ctx.ask_f.startswith("How many students"):
                q = "Every student is counted once. How many students did <b>not</b> %s?" % (
                    "choose " + ctx.p(cats[j]) if "chose" in ctx.ask_f else ctx.p(cats[j]) + " to school")
            else:
                q = "How many %s are <b>not</b> in the %s %s?" % (U[1], cats[j], "row" if gk == "pic" else "bar")
            cand = [vals[j], t, t - vals[nb], t - vals[j] + 1]
            its.append(mcq(f + q, fmt(t - vals[j], U), [fmt(x, U) for x in cand],
                           "Total: %s = %d. Take away %s (%d): %d − %d = %d. You can also add the other %s: %s = %d."
                           % (" + ".join(str(v) for v in vals), t, cats[j], vals[j], t, vals[j], t - vals[j],
                              "rows" if gk == "pic" else "bars",
                              " + ".join(str(vals[k]) for k in range(n) if k != j), t - vals[j])))
        elif kind == "tie":
            pairs = [(a, b) for a in range(n) for b in range(n) if vals[a] - vals[b] >= 2]
            a, b = rnd.choice(pairs)
            d = vals[a] - vals[b]
            q = "How many more %s does %s need to catch up to %s?" % (U[1], cats[b], cats[a])
            cand = [vals[a], vals[a] + vals[b], d + 1, d - 1]
            its.append(mcq(f + q, fmt(d, U), [fmt(x, U) for x in cand],
                           "%s. %s. Count up from %d to %d: that is %d − %d = %d more. (%d is %s’s number, not how many more.)"
                           % (rd(a), rd(b), vals[b], vals[a], vals[a], vals[b], d, vals[a], cats[a])))
        elif kind == "vsboth":
            srt = sorted(range(n), key=lambda k: vals[k])
            a = srt[-1]
            b, c = srt[0], srt[1]
            t2 = vals[b] + vals[c]
            d = vals[a] - t2
            q = ("How many more %s does %s show than %s and %s together?"
                 % (U[1], cats[a], cats[b], cats[c]))
            cand = [vals[a] + t2, t2, vals[a] - vals[b], d + 1]
            its.append(mcq(f + q, fmt(d, U), [fmt(x, U) for x in cand],
                           "Step 1: %s and %s together: %d + %d = %d. Step 2: %s: %d. %d − %d = %d."
                           % (cats[b], cats[c], vals[b], vals[c], t2, cats[a], vals[a], vals[a], t2, d)))
    assert len(its) == 20, len(its)
    return {"title": "Compare and total", "items": its}


# ------------------------------------------------------------ set 5: questions and conclusions (word problems)
def set_words(rnd):
    its = []
    S = STU
    # spring break bar graph, scale 2
    sb_c = ["Camping", "Skiing", "Beach", "Visit family"]
    sb_v = [6, 11, 4, 9]
    sb = fig(bar_svg("Our Spring Break plans", "Plan", "Students", sb_c, sb_v, 2,
                     label="bar graph: our spring break plans", source="Source: Grade 3 class survey"))
    its.append(mcq(sb + "Which question did the class ask to get this data?", "What will you do over Spring Break?",
                   ["How many days is Spring Break?", "Do you like skiing?", "Where do you live?"],
                   "The bars are camping, skiing, beach and visit family. These are answers to "
                   "“What will you do over Spring Break?” “Do you like skiing?” only has yes or no answers."))
    its.append(mcq(sb + "How many students are in the survey?", fmt(30, S), [fmt(x, S) for x in [28, 15, 26]],
                   "Skiing ends halfway between 10 and 12, so 11. Visit family ends halfway between 8 and 10, so 9. "
                   "6 + 11 + 4 + 9 = 30. (28 reads 11 and 9 as 10 and 8. 15 counts the grid spaces.)"))
    its.append(mcq(sb + "Which statement is true?", "More students will ski than camp.",
                   ["The beach is the most popular plan.", "Camping and skiing are the same.",
                    "Fewer students will visit family than go to the beach."],
                   "Skiing 11 and camping 6, so more students will ski. The beach (4) is the least popular, "
                   "and visit family (9) is more than the beach (4)."))
    its.append(mcq(sb + "Zara says, “Half of the class will go skiing.” Is she right?",
                   "No. 11 is less than half of 30.",
                   ["Yes. Skiing has the tallest bar.", "Yes. 11 students will ski.", "No. Nobody will go skiing."],
                   "There are 30 students, and half of 30 is 15. Only 11 will ski. The tallest bar shows the most "
                   "popular plan, not half of the class."))
    # how we get to school pictograph 1:1
    tr_c = ["Walk", "Car", "Bus", "Bike"]
    tr_v = [8, 6, 3, 5]
    trv = fig(pic_svg("How we get to school", tr_c, tr_v, "circle", S, source="Source: Division 5 survey"))
    its.append(mcq(trv + "What can the class say from this pictograph?", "Walking is the most common way.",
                   ["Most students take the bus.", "Nobody rides a bike.", "Car and bike are the same."],
                   "The Walk row is the longest: 8 circles. The Bus row is the shortest (3), and 5 students bike."))
    its.append(mcq(trv + "The school wants fewer cars at drop-off. If 2 of the car students start to bike, "
                   "how many students will bike?", fmt(7, S), [fmt(x, S) for x in [4, 3, 8]],
                   "Bike now: 5. 2 more will bike: 5 + 2 = 7. (4 is the new number of car students: 6 − 2.)"))
    its.append(mcq(trv + "Which question can you <b>not</b> answer with this pictograph?",
                   "How far away does each student live?",
                   ["How many students walk to school?", "Do more students bike or take the bus?",
                    "How many students were in the survey?"],
                   "The pictograph shows how students get to school, not how far they live. "
                   "We can read the walkers (8), compare bike and bus (5 and 3), and add for the total (22)."))
    # survey questions
    its.append(mcq("Liam wants to make a bar graph of his class’s favourite fruit. Which survey question is best?",
                   "Which fruit do you like best: apple, cherry, peach or pear?",
                   ["Do you like fruit?", "How many apples are in BC?", "What did you eat today?"],
                   "A good survey question gives a few clear choices, and each student picks one. "
                   "Then every answer fits one bar. “Do you like fruit?” only gives yes or no."))
    its.append(mcq("Mei asks, “Which do you like best: soccer, hockey or lacrosse?” Kai likes basketball best. "
                   "What should Mei add to her choices?", "Other",
                   ["Hockey", "Nothing", "A second vote"],
                   "Adding “Other” gives every student an answer to pick. Each student still votes only once."))
    # rainy days bar graph, scale 2
    rn_c = ["Oct", "Nov", "Dec", "Jan"]
    rn_v = [15, 20, 18, 17]
    rn = fig(bar_svg("Rainy days in Vancouver", "Month", "Rainy days", rn_c, rn_v, 2,
                     label="bar graph: rainy days in vancouver", source="Source: our class weather log"))
    its.append(mcq(rn + "Which month had the most rainy days?", "November", ["December", "January", "October"],
                   "The tallest bar is November. It ends on the line for 20."))
    its.append(mcq(rn + "How many more rainy days were there in November than in October?", fmt(5, DAY),
                   [fmt(x, DAY) for x in [35, 6, 4]],
                   "November ends on 20. October ends halfway between 14 and 16, so 15. 20 − 15 = 5. "
                   "(Reading October as 14 gives 6; as 16 gives 4.)"))
    its.append(mcq(rn + "November has 30 days. How many November days were <b>not</b> rainy?", fmt(10, DAY),
                   [fmt(x, DAY) for x in [20, 12, 50]],
                   "Rainy days in November: 20. 30 − 20 = 10 days were not rainy. (12 uses December’s bar, 18.)"))
    its.append(mcq(rn + "Owen says, “It rains every day in Vancouver.” Does the graph agree?",
                   "No. Every month had some days with no rain.",
                   ["Yes. All the bars are tall.", "Yes. November had 20 rainy days.", "No. It never rains in January."],
                   "Every month has 30 or 31 days, and no bar reaches 30. So each month had some dry days. "
                   "The bars are tall, so it rains a lot, but not every day."))
    # terry fox run table
    tf_c = ["Div. 1", "Div. 2", "Div. 3", "Div. 4"]
    tf_v = [42, 35, 50, 38]
    tf = fig(table_svg("Laps at the Terry Fox Run", "Class", tf_c, tf_v, "table: laps at the terry fox run",
                       tally=False, count_head="Laps"))
    its.append(mcq(tf + "Division 3 says, “We ran the most laps.” How many more laps is that than Division 2?",
                   fmt(15, LAP), [fmt(x, LAP) for x in [85, 8, 12]],
                   "Division 3: 50. Division 2: 35. 50 − 35 = 15. (8 uses Division 1: 50 − 42. "
                   "12 uses Division 4: 50 − 38.)"))
    its.append(mcq(tf + "The school’s goal is 160 laps. Did the four divisions reach it?",
                   "Yes, they ran 165 laps.",
                   ["No, they ran 155 laps.", "No, they ran 50 laps.", "Yes, they ran 175 laps."],
                   "42 + 35 + 50 + 38 = 165. 165 is more than 160, so they reached the goal. "
                   "(50 is only the biggest number in the table.)"))
    # salmon pictograph 1:1
    sm_c = ["Chinook", "Coho", "Chum", "Pink"]
    sm_v = [3, 7, 5, 9]
    sm = fig(pic_svg("Salmon seen at the creek", sm_c, sm_v, "star", SAL, source="Source: Grade 3 field trip count"))
    its.append(mcq(sm + "The class saw 2 more coho on the way back. Which kind of salmon did they see most now?",
                   "Coho and pink (a tie)", ["Coho", "Pink", "Chum"],
                   "Coho: 7 + 2 = 9. Pink: 9. Now coho and pink are the same, so it is a tie."))
    its.append(mcq(sm + "How many salmon did the class see altogether?", fmt(24, SAL), [fmt(x, SAL) for x in [4, 15, 23]],
                   "Chinook 3, coho 7, chum 5, pink 9. 3 + 7 + 5 + 9 = 24. (4 is the number of rows; 15 leaves out pink.)"))
    # food bank bar graph scale 2
    fb = fig(bar_svg("Cans for the food bank", "Class", "Cans", TEACH, [14, 18, 9, 12], 2,
                     label="bar graph: cans for the food bank", source="Source: school food bank count"))
    its.append(mcq(fb + "Ms. Ward’s class wants to catch up to Mr. Gill’s class. How many more cans does it need?",
                   fmt(9, ("can", "cans")), [fmt(x, ("can", "cans")) for x in [8, 10, 27]],
                   "Mr. Gill: 18. Ms. Ward: halfway between 8 and 10, so 9. 18 − 9 = 9 more cans. "
                   "(Reading Ms. Ward’s bar as 8 or 10 gives 10 or 8.)"))
    its.append(mcq(fb + "Which two classes together collected 26 cans?", "Ms. Lee and Mr. Chen",
                   ["Mr. Gill and Ms. Ward", "Ms. Lee and Mr. Gill", "Ms. Ward and Mr. Chen"],
                   "Ms. Lee 14 and Mr. Chen 12: 14 + 12 = 26. (Mr. Gill and Ms. Ward: 18 + 9 = 27. "
                   "Ms. Lee and Mr. Gill: 32. Ms. Ward and Mr. Chen: 21.)"))
    its.append(mcq(fb + "Harjot says, “Mr. Gill’s class collected twice as many cans as Ms. Ward’s class.” Is he right?",
                   "Yes. 9 + 9 = 18.", ["No. 18 is not double 9.", "No. Ms. Lee collected the most.",
                                         "Yes. Mr. Gill has the shortest bar."],
                   "Mr. Gill 18, Ms. Ward 9. Double 9 is 9 + 9 = 18, so Harjot is right. Mr. Gill has the tallest bar."))
    assert len(its) == 20
    return {"title": "Questions and conclusions: word problems", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


def body_html():
    sp = ["Soccer", "Hockey", "Lacrosse", "Swimming"]
    spv = [8, 5, 7, 4]
    rn_c = ["Oct", "Nov", "Dec", "Jan"]
    rn_v = [17, 20, 19, 16]
    return (
        "<h2>Collect, count, show, then explain</h2>"
        "<p>Data is information we collect, such as votes in a class survey. "
        "First we ask a clear <b>question</b>. Then we <b>count</b> the answers with tally marks. "
        "Then we <b>show</b> them in a table, a pictograph or a bar graph. "
        "Last, we say what the data tells us.</p>"
        "<h2>Tally charts and tables</h2>"
        "<p>Draw one mark for each answer. The fifth mark goes across the other four. "
        "Count the groups by 5s, then count on the single marks.</p>"
        "<figure class='sn-fig'>" + table_svg("Favourite sport", "Sport", sp, spv, "tally chart: favourite sport") +
        "<figcaption>Soccer: 1 group of 5 and 3 more marks. 5, then 6, 7, 8. So the total is 8.</figcaption></figure>" +
        "<h2>Pictographs: 1 symbol = 1</h2>"
        "<p>Look at the <b>key</b> first. In Grade 3, one symbol stands for one thing. "
        "This is called <b>one-to-one correspondence</b>. Count the symbols in a row to find the number.</p>"
        "<figure class='sn-fig'>" + pic_svg("Favourite sport", sp, spv, "circle", STU, source="Source: Grade 3 class vote") +
        "<figcaption>Each circle = 1 student. The Lacrosse row has 7 circles, so 7 students chose lacrosse.</figcaption></figure>" +
        ex("Example", "How many more students chose soccer than hockey?",
           "Soccer has 8 circles. Hockey has 5. 8 − 5 = 3. You can also count the 3 extra circles in the Soccer row.",
           "3 more students") +
        "<h2>Bar graphs</h2>"
        "<p>A good bar graph has a <b>title</b>, <b>labels</b>, a <b>scale</b> and a <b>source</b> "
        "(where the data came from). Find what the scale counts by: 1s or 2s. "
        "Put your finger on the top of the bar and look straight across to the scale. "
        "If the scale counts by 2s and a bar ends halfway between two lines, the number is halfway between them.</p>"
        "<figure class='sn-fig'>" + bar_svg("Rainy days in Vancouver", "Month", "Rainy days", rn_c, rn_v, 2,
                                            label="bar graph: rainy days in vancouver", source="Source: our class weather log") +
        "<figcaption>The scale counts by 2s. October ends halfway between 16 and 18, so October had 17 rainy days.</figcaption></figure>" +
        ex("Example", "How many more rainy days were there in November than in December?",
           "November ends on 20. December is halfway between 18 and 20, so 19. 20 − 19 = 1.", "1 more rainy day") +
        "<h2>Ask questions and draw conclusions</h2>"
        "<p>A good survey question has a few clear choices, and each person picks one. "
        "After you make the graph, compare the bars or rows: which is the most, which is the least, "
        "and how many more? Only say what the data shows. A vote in one class tells us about that class, not about everyone.</p>" +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Counting a group of 5 tally marks as 4", "Count the line across too: each group is 5"],
            ["Counting each group of tally marks as 1", "Count the groups by 5s: 5, 10, 15"],
            ["Reading the wrong bar or row", "Keep your finger on the right bar, then look across"],
            ["Counting one symbol too many or too few", "Touch each symbol as you count"],
            ["Counting grid spaces when the scale counts by 2s", "Read the number on the scale"],
            ["Adding when the question asks how many more", "How many more means subtract"],
        ])
    )


FAQ = [
    {"q": "What do Grade 3 students learn about graphs in the BC math curriculum?",
     "a": "The BC Grade 3 curriculum includes one-to-one correspondence with bar graphs, pictographs, charts and tables. Students collect data, count it with tally marks, show it so that one symbol or one square stands for one thing, and talk about what the data shows."},
    {"q": "What is one-to-one correspondence in a pictograph?",
     "a": "It means each symbol stands for exactly one thing. If the key says 1 star = 1 student, then a row of 6 stars shows 6 students. In Grade 4, students move on to keys where 1 symbol stands for 2, 5 or 10."},
    {"q": "How do you count tally marks?",
     "a": "Each group of five tally marks has four lines and one line across. Count the groups by 5s, then count on the single marks: 2 groups and 3 marks is 5, 10, then 11, 12, 13."},
    {"q": "How can I help my child read a bar graph?",
     "a": "Ask them to read the title and labels first, then check what the scale counts by. Have them put a finger on the top of one bar and look straight across to the scale, so they read the right bar."},
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


def mark_large(u, pattern):
    """Tag pictures that must print larger (graphs, tables and A to D panels) so their labels stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen_unit():
    ASKED.clear()
    rnd = random.Random(53810)
    PK = Picker(rnd)
    sets = [set_tally(rnd), set_pictograph(rnd, PK), set_bar(rnd, PK), set_compare(rnd, PK), set_words(rnd)]
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
    u = {
        "country": "ca-bc", "subject": "math", "grade": "grade-3", "slug": "bar-graphs-and-pictographs", "sort": 10,
        "updated": UPDATED, "pdf_url": "",
        "title": "Grade 3 Bar Graphs and Pictographs",
        "seo_title": "Grade 3 Bar Graphs and Pictographs Worksheets: Free Math Practice with Answer Key (BC Curriculum)",
        "short_title": "Bar graphs and pictographs",
        "domain": "Data and probability",
        "standard_code": "Grade 3: Data and probability",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/3/core",
        "standard_text": "One-to-one correspondence with bar graphs, pictographs, charts, and tables",
        "meta_desc": "Free Grade 3 math worksheets on bar graphs and pictographs for the BC curriculum: tally charts and tables, pictographs where 1 symbol = 1, bar graphs with a scale of 1 or 2, comparing and totalling data, and drawing conclusions. 100 questions with an answer key.",
        "key_big": "One symbol or one tally mark stands for one thing. Count carefully, then read across to the right number.",
        "key_sub": "A group of tally marks is 5, not 4. Keep your finger on the right bar or row. If the scale counts by 2s, a bar halfway between 8 and 10 shows 9.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(pictograph|bar graph|tally chart|table|four sets)")


if __name__ == "__main__":
    u = gen_unit()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
