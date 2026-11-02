# -*- coding: utf-8 -*-
"""
CA-BC Grade 4 Math (BC Mathematics Curriculum, Data and probability):
one-to-one and many-to-one correspondence, using bar graphs and pictographs.
  python3 tools/gen_cabc_math_g4_graphs.py
Pictographs with a key (1 symbol = 2, 5 or 10, and half symbols), bar graphs with scales of 2, 5 and 10,
comparing and totalling data, choosing a key or scale, drawing conclusions, and word problems in BC contexts
(favourite sports, salmon counts, rainy days in Vancouver).
Wrong answers come from real student mistakes: reading a symbol as 1, reading half a symbol as 1 for every key,
ignoring a half symbol, misreading the scale (line below, line above, counting grid spaces).
Every value is checked in code. HTML attributes use single quotes (no backslashes in the JSON). Canadian English.
"""
import json, re, math, os, random

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-4")
UPDATED = "2026-11-02"
GREEN = "#006633"
BAR = "#2e8b57"
FILL = "#cfe6d6"
RED = "#c0392b"
INK = "#2b2b2b"
GRID = "#c9d3cc"
MUTE = "#555555"
FONT = "Arial, Helvetica, sans-serif"


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e):
    """4 choices: correct + 3 unique distractors from real mistakes (no zero, negative or fractional numbers).
    Positions are balanced later for the whole set."""
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        c = str(c)
        lead = c.split(" ")[0].lstrip("$")
        if c in seen or not c or lead.startswith("-") or lead.startswith("−") or lead == "0" or re.match(r"^[0-9]+[.][0-9]", lead):
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


def syms(v, key, sym):
    """How a value is drawn: '4 circles', '4 and a half circles', 'half a circle'."""
    full, hf = v // key, v % key
    assert hf in (0, key // 2)
    if not hf:
        return ones(full, sym)
    if full == 0:
        return "half a %s" % sym
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
    def __init__(self, title, axis, cats, unit, ask, more, fewer, both, total, scales, pkeys, source, ph=None,
                 ordered=False, maxv=None):
        self.title, self.axis, self.cats, self.unit = title, axis, cats, unit
        self.ask_f, self.more_f, self.fewer_f, self.both_f, self.total = ask, more, fewer, both, total
        self.scales, self.pkeys, self.ph, self.ordered, self.maxv = scales, pkeys, ph or {}, ordered, maxv
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
LOWER = lambda cs: {c: c.lower() for c in cs}
TEACH = ["Ms. Lee", "Mr. Gill", "Ms. Ward", "Mr. Chen"]
POSS = {t: t + "’s class" for t in TEACH}
SPORTS = ["Soccer", "Hockey", "Lacrosse", "Basketball", "Swimming"]
SALMON = ["Chinook", "Coho", "Sockeye", "Pink", "Chum"]
SAL_PH = {"Chinook": "Chinook", "Coho": "coho", "Sockeye": "sockeye", "Pink": "pink", "Chum": "chum"}

CTXS = [
    Ctx("Favourite sport", "Sport", SPORTS, STU,
        "How many students chose {a}?", "How many more students chose {a} than {b}?",
        "How many fewer students chose {a} than {b}?", "How many students chose {a} or {b}?",
        "How many students voted altogether?", [2, 5], [2, 5], "Source: Grade 4 class vote", ph=LOWER(SPORTS)),
    Ctx("Salmon counted at the creek", "Kind of salmon", SALMON, SAL,
        "How many {a} salmon were counted?", "How many more {a} salmon than {b} salmon were counted?",
        "How many fewer {a} salmon than {b} salmon were counted?",
        "How many {a} and {b} salmon were counted altogether?",
        "How many salmon were counted altogether?", [5, 10], [5, 10], "Source: Grade 4 salmon count", ph=SAL_PH),
    Ctx("How we get to school", "Way to school", ["Walk", "Car", "Bus", "Bike"], STU,
        "How many students {a} to school?", "How many more students {a} to school than {b}?",
        "How many fewer students {a} to school than {b}?", "How many students {a} or {b} to school?",
        "How many students are in the survey altogether?", [5, 10], [5, 10], "Source: school survey",
        ph={"Walk": "walk", "Car": "come by car", "Bus": "take the bus", "Bike": "ride a bike"}),
    Ctx("Birds seen in Stanley Park", "Bird", ["Eagle", "Heron", "Crow", "Duck", "Gull"], ("bird", "birds"),
        "How many {a} were seen?", "How many more {a} than {b} were seen?",
        "How many fewer {a} than {b} were seen?", "How many {a} and {b} were seen altogether?",
        "How many birds were seen altogether?", [2], [2], "Source: field trip bird count", maxv=20,
        ph={"Eagle": "bald eagles", "Heron": "herons", "Crow": "crows", "Duck": "ducks", "Gull": "gulls"}),
    Ctx("Cans for the food bank", "Class", TEACH, ("can", "cans"),
        "How many cans did {a} collect?", "How many more cans did {a} collect than {b}?",
        "How many fewer cans did {a} collect than {b}?", "How many cans did {a} and {b} collect altogether?",
        "How many cans did the classes collect altogether?", [5, 10], [5, 10], "Source: school food drive count",
        ph=POSS),
    Ctx("Books read in the reading challenge", "Student", ["Liam", "Olivia", "Arjun", "Mei", "Ethan", "Simran"],
        ("book", "books"),
        "How many books did {a} read?", "How many more books did {a} read than {b}?",
        "How many fewer books did {a} read than {b}?", "How many books did {a} and {b} read altogether?",
        "How many books did the students read altogether?", [2], [2], "Source: class reading logs", maxv=20),
    Ctx("Laps at the Terry Fox Run", "Grade", ["Gr. 3", "Gr. 4", "Gr. 5", "Gr. 6", "Gr. 7"], ("lap", "laps"),
        "How many laps did {a} run?", "How many more laps did {a} run than {b}?",
        "How many fewer laps did {a} run than {b}?", "How many laps did {a} and {b} run altogether?",
        "How many laps did the five grades run altogether?", [5, 10], [5, 10], "Source: Terry Fox Run lap cards",
        ordered=True, ph={"Gr. %d" % g: "the Grade %d students" % g for g in range(3, 8)}),
    Ctx("Visitors to the book fair", "Day", ["Mon", "Tue", "Wed", "Thu", "Fri"], ("visitor", "visitors"),
        "How many visitors came on {a}?", "How many more visitors came on {a} than on {b}?",
        "How many fewer visitors came on {a} than on {b}?", "How many visitors came on {a} and {b} altogether?",
        "How many visitors came altogether?", [5, 10], [5, 10], "Source: book fair sign-in sheet", ordered=True,
        ph={"Mon": "Monday", "Tue": "Tuesday", "Wed": "Wednesday", "Thu": "Thursday", "Fri": "Friday"}),
]


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


def make_data(ctx, n, step, half, rnd, max_units=7, min_units=1, ok=lambda v, c: True):
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
        if not ok(vals, cats):
            continue
        return cats, vals
    raise ValueError("no data for " + ctx.title)


def source_line(y, src):
    return text(8, y, src, 14, anchor="start", col=MUTE, extra=" font-style='italic'")


# ------------------------------------------------------------ pictograph
def pic_part(title, cats, vals, key, sym, unit, missing=None, source=None):
    """Pictograph: one row per category, symbols worth `key` each, key line at the bottom."""
    fs, rh, gap = 15, 26, 23
    lw = max(tw(c, fs) for c in cats) + 22
    nsym = [math.ceil(v / key) for v in vals]
    m = max(max(nsym), 4)
    W = lw + 12 + m * gap + 14
    keytxt = "= " + fmt(key, unit)
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
    if source:
        s.append(source_line(ky + 24, source))
        H = ky + 30
    return (W, H, "".join(s))


def pic_svg(title, cats, vals, key, sym, unit, source=None, label=None):
    return part_svg(pic_part(title, cats, vals, key, sym, unit, source=source), label or "pictograph: " + title.lower())


def ctx_pic(ctx, cats, vals, key, sym):
    return pic_svg(ctx.title, cats, vals, key, sym, ctx.unit, source=ctx.source)


# ------------------------------------------------------------ bar graph
def bar_part(title, cat_axis, val_axis, cats, vals, scale, top_v=None, col=BAR, source=None):
    """Vertical bar graph with a gridline at every step of the scale. title may be empty (missing title)."""
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


def ctx_bar(ctx, cats, vals, scale, title=True):
    return bar_svg(ctx.title if title else "", ctx.axis, ctx.unit[1].capitalize(), cats, vals,
                   scale, label="bar graph: " + ctx.title.lower(), source=ctx.source)


# ------------------------------------------------------------ A-D panels (one picture)
PW, PH = 218, 172


def mini_bar(x0, y0, cats, vals, scale, top_v):
    """A small bar graph inside a panel (no title): scale on the left, short labels below."""
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
    """2 x 2 panels labelled A to D. draws: list of functions (x0, y0) -> svg string."""
    W, H = 2 * PW, 2 * PH
    s = ["<line x1='%d' y1='4' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (PW, PW, H - 4, GRID),
         "<line x1='4' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (PH, W - 4, PH, GRID)]
    for k, d in enumerate(draws):
        x0, y0 = (k % 2) * PW, (k // 2) * PH
        s.append(d(x0, y0))
        s.append(text(x0 + 8, y0 + 20, "ABCD"[k], 18, anchor="start", bold=True))
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
        return "The bar for %s ends halfway between %d and %d, so it shows %d." % (c, lo, lo + scale, v)
    return "The bar for %s ends on the line for %d." % (c, v)


def pic_mis(v, key):
    """Real misreadings of a half symbol: ignore it, read it as 1, read it as a whole symbol."""
    full, hf = v // key, v % key
    if not hf:
        return []
    return [full * key, full * key + 1, (full + 1) * key]


def pic_wrong(v, key):
    """Real misreadings of one pictograph row (the first is: each symbol read as 1)."""
    return [math.ceil(v / key)] + pic_mis(v, key)


def bar_mis(v, scale):
    if v % scale:
        lo = v - v % scale
        return [lo, lo + scale]                     # read the line below / above
    return []


def bar_wrong(v, scale):
    if v % scale:
        lo = v - v % scale
        return [lo, lo + scale, lo + 1]             # line below / line above / halfway read as 1 more
    return [v // scale]                             # counted grid spaces


ASKED = set()


def pick_row(rnd, ctx, cats, js):
    """A row/bar that has not been asked about before in this context (so no two questions read the same)."""
    fresh = [j for j in js if (ctx.title, cats[j]) not in ASKED]
    j = rnd.choice(fresh or js)
    ASKED.add((ctx.title, cats[j]))
    return j


# ------------------------------------------------------------ set 1: pictographs with a key
def set_pictograph(rnd, PK):
    its = []
    plan = [(2, "read"), (2, "most"), (2, "readh"), (2, "half"), (2, "which"), (2, "draw"),
            (5, "read"), (5, "which"), (5, "fewest"), (5, "draw"), (5, "read"), (5, "count"),
            (10, "read"), (10, "readh"), (10, "half"), (10, "which"), (10, "readh"), (10, "draw"), (10, "most"),
            (10, "count")]
    draws = iter([
        ("Each circle stands for 2 students. 16 students chose soccer. How many circles should be in the Soccer row?",
         16, 2, "circle"),
        ("Each square stands for 5 salmon. The class counted 35 coho salmon. How many squares should be in the Coho row?",
         35, 5, "square"),
        ("Each star stands for 10 cans. Ms. Ward’s class collected 80 cans for the food bank. How many stars should be "
         "in the class’s row?", 80, 10, "star")])
    for i, (key, kind) in enumerate(plan):
        sym = SYMS[i % 3]
        if kind == "draw":
            q, v, k, sym = next(draws)
            assert k == key and v % key == 0
            full = v // key
            ans = ones(full, sym)
            cand = [ones(v, sym), ones(full + 1, sym), ones(full - 1, sym), ones(key, sym)]
            e = ("Count by %ds until you reach %d: %s. That is %s, so draw %s. Check: %d × %d = %d. "
                 "(Drawing %s would mean each %s stands for 1.)"
                 % (key, v, ", ".join(str(key * t) for t in range(1, full + 1)), ones(full, "step"), ans, full, key, v,
                    ones(v, sym), sym))
            its.append(mcq(q, ans, cand, e))
            continue
        ctx = PK.next(lambda c: key in c.pkeys)
        half = (key == 2 and kind in ("readh", "which", "half")) or (key == 10 and kind in ("readh", "half", "count"))
        n = 5 if i % 3 == 0 and len(ctx.cats) >= 5 else 4
        fresh = lambda c: (ctx.title, c) not in ASKED
        okh = ((lambda vs, cs: any(v % key and v > key and fresh(c) for v, c in zip(vs, cs))) if half
               else (lambda vs, cs: max(vs) - min(vs) >= 2 * key))
        cats, vals = make_data(ctx, n, key, half, rnd, max_units=7 if key < 10 else 6, min_units=1, ok=okh)
        f = fig(ctx_pic(ctx, cats, vals, key, sym))
        U = ctx.unit
        keytxt = "Look at the key: each %s stands for %s. " % (sym, fmt(key, U))
        if kind in ("read", "readh"):
            if kind == "readh":
                j = pick_row(rnd, ctx, cats, [k for k, v in enumerate(vals) if v % key and v > key])
            else:
                j = pick_row(rnd, ctx, cats, list(range(n)))
            c, v = cats[j], vals[j]
            others = [vals[k] for k in range(n) if k != j]
            cand = pic_wrong(v, key) + [v + key, v - key] + others + [v * 2]
            its.append(mcq(f + ctx.ask(c), fmt(v, U), [fmt(x, U) for x in cand],
                           keytxt + read_pic(c, v, key, sym, U) + " (%s would mean each %s is 1.)"
                           % (fmt(math.ceil(v / key), U), sym)))
        elif kind in ("most", "fewest"):
            j = vals.index(max(vals) if kind == "most" else min(vals))
            w = "most" if kind == "most" else "fewest"
            q = "Which row shows the %s %s?" % (w, U[1])
            its.append(mcq(f + q, cats[j], [cats[k] for k in range(n) if k != j],
                           "Every %s stands for the same number, so the row with the %s %ss shows the %s. %s"
                           % (sym, w, sym, w, read_pic(cats[j], vals[j], key, sym, U))))
        elif kind == "half":
            its.append(mcq(f + "In this pictograph, what does half a %s stand for?" % sym, fmt(key // 2, U),
                           [fmt(x, U) for x in (1, key, key * 2, key + 1)],
                           "The key says one whole %s = %s. Half a %s is half of %d, which is %s. "
                           "(Half a symbol is not always 1. It is half of the key.)"
                           % (sym, fmt(key, U), sym, key, fmt(key // 2, U))))
        elif kind == "count":
            j = pick_row(rnd, ctx, cats, [k for k, v in enumerate(vals) if v % key and v > key] if half else list(range(n)))
            v = vals[j]
            ans = syms(v, key, sym)
            full = v // key
            cand = [ones(v, sym)] + ([ones(full + 1, sym), ones(full, sym)] if v % key
                                     else [ones(full + 1, sym), ones(full - 1, sym)]) + [ones(v // 2, sym)]
            its.append(mcq(f + "How many %ss are in the %s row?" % (sym, cats[j]), ans, cand,
                           "Count the symbols in the row: %s. Check with the key: %s. "
                           "(The row does not have %s. That would be the number of %s.)"
                           % (ans, short_pic(v, key), ones(v, sym), U[1])))
        else:  # which
            hs = [k for k in range(n) if vals[k] % key and vals[k] > key] if half else list(range(n))
            j = pick_row(rnd, ctx, cats, hs)
            v = vals[j]
            near = sorted([k for k in range(n) if k != j], key=lambda k: abs(vals[k] - v))
            cand = [cats[k] for k in range(n) if k != j and math.ceil(vals[k] / key) == v] + [cats[k] for k in near]
            if half:
                e = "Half a %s is %d. %s" % (sym, key // 2, read_pic(cats[j], v, key, sym, U))
            else:
                e = "Each %s = %d. %d ÷ %d = %d, so look for %s. %s" % (sym, key, v, key, v // key, ones(v // key, sym),
                                                                       read_pic(cats[j], v, key, sym, U))
            its.append(mcq(f + "Which row shows %s?" % fmt(v, U), cats[j], cand, e))
    assert len(its) == 20
    return {"title": "Pictographs: 1 symbol = 2, 5 or 10", "items": its}


# ------------------------------------------------------------ set 2: bar graphs with scales of 2, 5 and 10
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
    e = ("%s matches every number (the scale goes up by %ds). %s."
         % ("ABCD"[pos], step, "; ".join(why)))
    tb = "<b>%s</b>: %s. " % (title, ", ".join("%s %d" % (c, v) for c, v in zip(cats, vals)))
    return mcq_fixed(fig(svg) + tb + "Which bar graph shows this data?", ["A", "B", "C", "D"], pos, e)


def set_bar(rnd, PK):
    its = []
    plan = [(2, "step"), (2, "read"), (2, "readh"), (2, "which"), (2, "fewest"),
            (5, "step"), (5, "read"), (5, "which"), (5, "read"), (5, "most"),
            (10, "step"), (10, "read"), (10, "readh"), (10, "which"), (10, "readh"), (10, "read")]
    for i, (sc, kind) in enumerate(plan):
        ctx = PK.next(lambda c: sc in c.scales)
        half = sc in (2, 10) and kind in ("readh", "which")
        n = 5 if (i % 3 == 0 and len(ctx.cats) >= 5) else 4
        cats, vals = make_data(ctx, n, sc, half, rnd, max_units=8 if sc == 2 else 9, min_units=1,
                               ok=lambda vs, cs: max(vs) - min(vs) >= 2 * sc and
                               (not half or any(v % sc and (ctx.title, c) not in ASKED for v, c in zip(vs, cs))))
        f = fig(ctx_bar(ctx, cats, vals, sc))
        U = ctx.unit
        scl = "The scale goes up by %ds. " % sc
        if kind in ("read", "readh"):
            if kind == "readh":
                j = pick_row(rnd, ctx, cats, [k for k, v in enumerate(vals) if v % sc])
            else:
                j = pick_row(rnd, ctx, cats, list(range(n)))
            c, v = cats[j], vals[j]
            others = [vals[k] for k in range(n) if k != j]
            cand = bar_wrong(v, sc) + [v + sc, v - sc] + others + [v + 1]
            its.append(mcq(f + ctx.ask(c), fmt(v, U), [fmt(x, U) for x in cand],
                           "%s%s So the answer is %s." % (scl, read_bar(c, v, sc), fmt(v, U))))
        elif kind == "step":
            its.append(mcq(f + "What does the scale on this bar graph count by?", "%ds" % sc,
                           ["%ds" % x for x in (1, 2, 5, 10) if x != sc],
                           "Read the numbers on the scale: 0, %d, %d, %d … Each line is %d more than the one before, "
                           "so the scale counts by %ds. (Do not count the lines by 1s.)" % (sc, 2 * sc, 3 * sc, sc, sc)))
        elif kind == "which":
            if half:
                j = pick_row(rnd, ctx, cats, [k for k, v in enumerate(vals) if v % sc])
            else:
                j = pick_row(rnd, ctx, cats, list(range(n)))
            v = vals[j]
            near = sorted([k for k in range(n) if k != j], key=lambda k: abs(vals[k] - v))
            its.append(mcq(f + "Which bar shows %s?" % fmt(v, U), cats[j], [cats[k] for k in near],
                           "%sFind %d on the scale. %s" % (scl, v, read_bar(cats[j], v, sc))))
        else:
            j = vals.index(max(vals) if kind == "most" else min(vals))
            word = "tallest" if kind == "most" else "shortest"
            q = "Which bar shows the %s %s?" % ("most" if kind == "most" else "fewest", U[1])
            its.append(mcq(f + q, cats[j], [cats[k] for k in range(n) if k != j],
                           "The bar for %s is the %s one. %s" % (cats[j], word, read_bar(cats[j], vals[j], sc))))
    # 17-18 table -> bar graph (A to D)
    its.append(match_q(rnd, 2, "Birds seen in Stanley Park", ["Crow", "Duck", "Gull", "Jay"], [8, 13, 6, 10], 2))
    its.append(match_q(rnd, 0, "Visitors to the book fair", ["Mon", "Tue", "Wed", "Thu"], [40, 65, 30, 50], 10))
    # 19 list that matches
    cn = CTXS[4]
    vals = [40, 70, 50, 60]
    f = fig(ctx_bar(cn, TEACH, vals, 10))
    lst = lambda vs: ", ".join(str(v) for v in vs)
    sw = vals[:]
    sw[1], sw[2] = sw[2], sw[1]
    its.append(mcq(f + "Which list matches this bar graph? The numbers are in this order: %s." % ", ".join(TEACH),
                   lst(vals), [lst([v // 10 for v in vals]), lst(sw), lst([v + 10 for v in vals])],
                   "The scale counts by 10s. " + " ".join(read_bar(c, v, 10) for c, v in zip(TEACH, vals)) +
                   " Counting grid spaces instead of reading the scale gives %s." % lst([v // 10 for v in vals])))
    # 20 halfway without a picture
    its.append(mcq("On a bar graph with a scale of 10s, a bar ends halfway between the lines for 40 and 50. "
                   "What number does the bar show?", 45, [41, 40, 50, 5],
                   "Halfway between 40 and 50 is 45, because 45 is 5 more than 40 and 5 less than 50. "
                   "(41 would mean halfway is 1 more. Halfway is half of the scale: half of 10 is 5.)"))
    assert len(its) == 20, len(its)
    return {"title": "Bar graphs: scales of 2, 5 and 10", "items": its}


# ------------------------------------------------------------ set 3: compare and total from graphs
def set_compare(rnd, PK):
    its = []
    plan = [("pic", 2, "more"), ("bar", 2, "more"), ("pic", 5, "more"), ("bar", 5, "more"), ("pic", 10, "more"),
            ("bar", 10, "more"), ("pic", 2, "fewer"), ("bar", 5, "fewer"), ("pic", 10, "fewer"), ("bar", 10, "fewer"),
            ("pic", 5, "both"), ("bar", 2, "both"), ("pic", 10, "both"), ("bar", 10, "both"),
            ("pic", 2, "total"), ("bar", 5, "total"), ("pic", 5, "total"), ("bar", 10, "total"), ("pic", 10, "total"),
            ("bar", 2, "total")]
    for i, (g, k, kind) in enumerate(plan):
        pic = g == "pic"
        ctx = PK.next(lambda c: k in (c.pkeys if pic else c.scales))
        half = k in (2, 10) and i % 2 == 0 if pic else k in (2, 10)
        n = 4 if kind == "total" else (5 if len(ctx.cats) >= 5 and i % 3 == 0 else 4)
        mu = (7 if k < 10 else 6) if pic else (8 if k == 2 else 9)
        cats, vals = make_data(ctx, n, k, half, rnd, max_units=mu, min_units=1,
                               ok=lambda vs, cs: max(vs) - min(vs) >= 2 * k)
        sym = SYMS[i % 3]
        f = fig(ctx_pic(ctx, cats, vals, k, sym) if pic else ctx_bar(ctx, cats, vals, k))
        U = ctx.unit
        intro = ("Each %s stands for %s. " % (sym, fmt(k, U))) if pic else ("The scale goes up by %ds. " % k)
        mis = (lambda v: pic_mis(v, k)) if pic else (lambda v: bar_mis(v, k))
        rd = (lambda c, v: "%s: %s" % (c, short_pic(v, k))) if pic else (lambda c, v: "%s: %d" % (c, v))
        unitw = "symbols" if pic else "grid spaces"
        if kind in ("more", "fewer"):
            pairs = [(a, b) for a in range(n) for b in range(n) if vals[a] - vals[b] >= 2 * k
                     and (not half or vals[a] % k or vals[b] % k)]
            a, b = rnd.choice(pairs)
            d = vals[a] - vals[b]
            cand = [vals[a] - x for x in mis(vals[b])] + [x - vals[b] for x in mis(vals[a])]
            spaces = [d // k] if d % k == 0 else []
            cand += spaces + [vals[a] + vals[b], d + k, d - k, vals[a]]
            q = ctx.more(cats[a], cats[b]) if kind == "more" else ctx.fewer(cats[b], cats[a])
            word = "more" if kind == "more" else "fewer"
            extra = (" (%d is the difference in %s, not in %s.)" % (d // k, unitw, U[1])) if spaces else ""
            its.append(mcq(f + q, fmt(d, U), [fmt(x, U) for x in cand],
                           "%s%s. %s. How many %s means find the difference: %d − %d = %s.%s"
                           % (intro, rd(cats[a], vals[a]), rd(cats[b], vals[b]), word, vals[a], vals[b], fmt(d, U), extra)))
        elif kind == "both":
            pairs = [(x, y) for x in range(n) for y in range(n) if x < y and (not half or vals[x] % k or vals[y] % k)]
            a, b = rnd.choice(pairs)
            t = vals[a] + vals[b]
            cand = [x + vals[b] for x in mis(vals[a])] + [vals[a] + x for x in mis(vals[b])]
            ns = math.ceil(vals[a] / k) + math.ceil(vals[b] / k)
            cand += [ns, abs(vals[a] - vals[b]), t + k, t - k]
            its.append(mcq(f + ctx.both(cats[a], cats[b]), fmt(t, U), [fmt(x, U) for x in cand],
                           "%s%s. %s. Altogether means add: %d + %d = %s."
                           % (intro, rd(cats[a], vals[a]), rd(cats[b], vals[b]), vals[a], vals[b], fmt(t, U))))
        else:
            t = sum(vals)
            low = sum(v - v % k for v in vals)
            ns = sum(math.ceil(v / k) for v in vals)
            cand = ([low] if low != t else []) + ([ns] if pic or low == t else []) + [t - min(vals), t + k, t - k]
            note = ""
            if low != t:
                note = " (%d leaves out the %s.)" % (low, "half symbols" if pic else "halves between the lines")
            elif pic:
                note = " (%d is the number of symbols.)" % ns
            else:
                note = " (%d counts grid spaces, not %s.)" % (ns, U[1])
            its.append(mcq(f + ctx.total, fmt(t, U), [fmt(x, U) for x in cand],
                           "%sRead every %s: %s. Add them: %s = %s.%s"
                           % (intro, "row" if pic else "bar", ", ".join("%s %d" % (c, v) for c, v in zip(cats, vals)),
                              " + ".join(str(v) for v in vals), fmt(t, U), note)))
    assert len(its) == 20
    return {"title": "Compare and total from graphs", "items": its}


# ------------------------------------------------------------ set 4: choose the key or scale, draw conclusions
SP_C = SPORTS
SP_V = [9, 5, 2, 3, 6]


def set_choose(rnd):
    its = []
    S = STU
    # 1 one-to-one
    its.append(mcq("Which key shows <b>one-to-one</b> correspondence?", "1 symbol = 1 student",
                   ["1 symbol = 2 students", "1 symbol = 5 students", "1 symbol = 10 students"],
                   "One-to-one means one symbol for each one thing: 1 symbol = 1 student. "
                   "The other keys are many-to-one: one symbol stands for many students."))
    # 2 why many-to-one
    its.append(mcq("Mei counted 80 salmon. Why is a key of 1 symbol = 10 salmon better than 1 symbol = 1 salmon?",
                   "She draws 8 symbols, not 80.",
                   ["The graph shows more salmon.", "Each salmon is bigger.", "She does not need a key."],
                   "With 1 symbol = 10 salmon, 80 salmon is 80 ÷ 10 = 8 symbols. With 1 symbol = 1 salmon she would "
                   "draw 80 symbols. The number of salmon stays 80 either way, and the key is still needed."))
    # 3-5 choose a scale
    for data, ans, wrong, why in [
            ([20, 45, 30, 35], 5, [1, 2, 10],
             "All the numbers are in the 5 times table, so with a scale of 5s every bar ends on a line, up to 45 (9 lines). "
             "A scale of 1s needs 45 lines. With 2s or 10s, 45 and 35 do not end on a line."),
            ([60, 90, 40, 80], 10, [2, 5, 100],
             "All the numbers are in the 10 times table, so a scale of 10s works with only 9 lines up to 90. "
             "5s also works but needs 18 lines, and 2s needs 45 lines. With 100s, no bar ends on a line."),
            ([8, 14, 6, 12], 2, [1, 5, 10],
             "All the numbers are even, so with a scale of 2s every bar ends on a line, up to 14 (7 lines). "
             "1s needs 14 lines. With 5s or 10s, 8, 14, 6 and 12 do not end on a line.")]:
        its.append(mcq("Owen will make a bar graph of this data: %s. He wants every bar to end <b>on</b> a line, "
                       "with as few lines as possible. Which scale should he use?" % ", ".join(map(str, data)),
                       "Count by %ds" % ans, ["Count by %ds" % w for w in wrong], why))
        assert all(v % ans == 0 for v in data)
    # 6-8 choose a key
    for data, unit, ans, wrong in [([30, 50, 25, 40], ("lap", "laps"), 5, [1, 2, 10]),
                                   ([12, 8, 16, 10], ("book", "books"), 2, [1, 5, 10]),
                                   ([70, 40, 90, 60], ("can", "cans"), 10, [2, 5, 20])]:
        assert all(v % ans == 0 for v in data)
        bad = [w for w in wrong if any(v % w for v in data)]
        okw = [w for w in wrong if w not in bad]
        assert all(w < ans for w in okw)
        why = ("Every number is in the %d times table, so 1 symbol = %d %s gives whole symbols: %s. "
               % (ans, ans, unit[1], ", ".join("%d ÷ %d = %d" % (v, ans, v // ans) for v in data)))
        if okw:
            why += "A key of %s also gives whole symbols, but more of them. " % " or ".join(str(w) for w in okw)
        if bad:
            v = [v for v in data if v % bad[0]][0]
            why += "A key of %d does not work for %d." % (bad[0], v)
        its.append(mcq("Hana will make a pictograph of this data: %s %s. She wants only whole symbols, and as few "
                       "symbols as possible. Which key should she use?" % (", ".join(map(str, data)), unit[1]),
                       "1 symbol = %s" % fmt(ans, unit), ["1 symbol = %s" % fmt(w, unit) for w in wrong], why.strip()))
    # 9-10 half symbols
    its.append(mcq("In a pictograph, each star stands for 10 laps. The Grade 4 students ran 45 laps at the Terry Fox Run. "
                   "How should their row look?", "4 and a half stars", ["45 stars", "5 stars", "4 stars"],
                   "45 = 40 + 5. 40 laps is 4 stars (4 × 10). 5 is half of 10, so add half a star: 4 and a half stars."))
    its.append(mcq("In a pictograph, each circle stands for 2 bald eagles. Kai saw 7 eagles. How should his row look?",
                   "3 and a half circles", ["7 circles", "4 circles", "3 circles"],
                   "7 = 6 + 1. 6 eagles is 3 circles (3 × 2). 1 is half of 2, so add half a circle: 3 and a half circles."))
    # 11-12 change the key
    its.append(mcq("In Liam’s pictograph, each circle = 5 students, and the Soccer row has 6 circles. He makes a new "
                   "pictograph where each circle = 10 students. How many circles go in the Soccer row now?",
                   "3 circles", ["6 circles", "12 circles", "30 circles"],
                   "First find the number of students: 6 × 5 = 30. Then use the new key: 30 ÷ 10 = 3 circles. "
                   "A bigger key means fewer symbols. (12 circles doubles the symbols instead of halving them.)"))
    its.append(mcq("In Ava’s pictograph, each star = 2 books, and her row has 10 stars. She makes a new pictograph "
                   "where each star = 5 books. How many stars go in her row now?",
                   "4 stars", ["10 stars", "2 stars", "25 stars"],
                   "First find the number of books: 10 × 2 = 20. Then use the new key: 20 ÷ 5 = 4 stars. "
                   "(2 stars comes from 10 ÷ 5, which forgets that each old star was 2 books.)"))
    # 13 missing title
    cn = CTXS[4]
    f = fig(ctx_bar(cn, TEACH, [50, 30, 70, 40], 10, title=False)
            .replace("aria-label='bar graph: cans for the food bank'", "aria-label='bar graph with no title'"))
    its.append(mcq(f + "Every bar graph needs a title, labels, a scale and a source. What is missing from this bar graph?",
                   "A title", ["A scale", "Labels", "A source"],
                   "The graph has a scale (0, 10, 20 …), labels (Class and Cans) and a source under the graph. "
                   "It has no title at the top. A good title is “Cans for the food bank”."))
    # 14 list matches a pictograph
    sal = [20, 35, 15, 30]
    f = fig(pic_svg("Salmon counted at the creek", SALMON[:4], sal, 5, "square", SAL, source="Source: Grade 4 salmon count"))
    lst = lambda vs: ", ".join(str(v) for v in vs)
    its.append(mcq(f + "Which list matches this pictograph? The numbers are in this order: Chinook, Coho, Sockeye, Pink.",
                   lst(sal), [lst([v // 5 for v in sal]), lst([v * 2 for v in sal]), lst([v + 5 for v in sal])],
                   "Each square = 5 salmon. Chinook 4 × 5 = 20, Coho 7 × 5 = 35, Sockeye 3 × 5 = 15, Pink 6 × 5 = 30. "
                   "(%s counts the squares as 1 each, and %s uses a key of 10 by mistake.)"
                   % (lst([v // 5 for v in sal]), lst([v * 2 for v in sal]))))
    # 15-17 sport bar graph, scale 2
    sport = fig(bar_svg("Favourite sport", "Sport", "Students", SP_C, SP_V, 2,
                        label="bar graph: favourite sport", source="Source: Grade 4 class vote"))
    its.append(mcq(sport + "Which statement is true?", "Swimming got 1 more vote than hockey.",
                   ["Hockey got more votes than swimming.", "Lacrosse got the most votes.",
                    "Soccer got twice as many votes as hockey."],
                   "The scale counts by 2s. Swimming 6, hockey 5 (halfway between 4 and 6): 6 − 5 = 1, so this is true. "
                   "Lacrosse (2) got the fewest votes. Twice hockey would be 10, but soccer got 9."))
    its.append(mcq(sport + "Which sports did fewer than 5 students choose?", "Lacrosse and basketball",
                   ["Lacrosse only", "Lacrosse, basketball and hockey", "Basketball and hockey"],
                   "Lacrosse ends on 2. Basketball ends halfway between 2 and 4, so 3. Both are less than 5. "
                   "Hockey ends halfway between 4 and 6, so it is 5, and 5 is not fewer than 5. "
                   "(Reading hockey as 4 adds hockey by mistake.)"))
    its.append(mcq(sport + "Ava says, “Soccer is the favourite sport of every Grade 4 student in BC.” Is she right?",
                   "No. The data is from one class only.",
                   ["Yes. Soccer has the tallest bar.", "Yes. 9 students chose soccer.", "No. Swimming has the tallest bar."],
                   "The source says the data is from one Grade 4 class vote. It tells us about this class, not every "
                   "student in BC. Even in this class, most students did not choose soccer: 9 out of %d." % sum(SP_V)))
    # 18 two scales
    its.append(mcq("Two bar graphs show the same salmon count. Graph A has a scale of 10s, and its Coho bar ends halfway "
                   "between 30 and 40. Graph B has a scale of 5s. Where does the Coho bar end on Graph B?",
                   "On the line for 35", ["Halfway between 30 and 35", "On the line for 30", "On the line for 40"],
                   "Halfway between 30 and 40 is 35. Graph B counts by 5s, so it has a line for 35. "
                   "The bar ends right on that line."))
    # 19 Terry Fox laps, scale 10
    tf_c = ["Gr. 3", "Gr. 4", "Gr. 5", "Gr. 6", "Gr. 7"]
    tf_v = [35, 50, 40, 70, 85]
    tf = fig(bar_svg("Laps at the Terry Fox Run", "Grade", "Laps", tf_c, tf_v, 10,
                     label="bar graph: laps at the terry fox run", source="Source: Terry Fox Run lap cards"))
    assert tf_v[3] == 2 * tf_v[0] and tf_v[2] < tf_v[1]
    its.append(mcq(tf + "Which statement is true?", "Grade 6 ran twice as many laps as Grade 3.",
                   ["Grade 5 ran more laps than Grade 4.", "Grade 7 ran 80 laps.",
                    "Grade 4 and Grade 5 ran the same number of laps."],
                   "The scale counts by 10s. Grade 3 ends halfway between 30 and 40, so 35. Grade 6 ends on 70. "
                   "35 × 2 = 70, so Grade 6 ran twice as many. Grade 7 is 85, not 80, and Grade 5 (40) ran fewer than Grade 4 (50)."))
    # 20 pattern
    dy_c, dy_v = ["Mon", "Tue", "Wed", "Thu"], [20, 30, 40, 50]
    dy = fig(bar_svg("Salmon counted each day", "Day", "Salmon", dy_c, dy_v, 10,
                     label="bar graph: salmon counted each day", source="Source: Grade 4 salmon count"))
    its.append(mcq(dy + "The number of salmon goes up the same way each day. If it keeps going, how many salmon will "
                   "the class count on Friday?", fmt(60, SAL), [fmt(x, SAL) for x in [50, 70, 6]],
                   "20, 30, 40, 50: each bar is 10 more than the day before. 50 + 10 = 60 salmon on Friday. "
                   "(6 counts grid spaces, not salmon.)"))
    assert len(its) == 20
    order = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
    return {"title": "Choose the key or scale and draw conclusions", "items": [its[k] for k in order]}


# ------------------------------------------------------------ set 5: word problems
def set_words(rnd):
    S = STU
    # sports bar graph, scale 5
    sp_c = SPORTS
    sp_v = [35, 25, 15, 30, 20]
    sport = fig(bar_svg("Favourite sport of the Grade 4 students", "Sport", "Students", sp_c, sp_v, 5,
                        label="bar graph: favourite sport of the grade 4 students",
                        source="Source: school survey of Grade 4 students"))
    # rainy days bar graph, scale 2
    rn_c = ["Nov", "Dec", "Jan", "Feb", "Mar"]
    rn_v = [20, 19, 17, 13, 16]
    RD = ("rainy day", "rainy days")
    rain = fig(bar_svg("Rainy days in Vancouver", "Month", "Rainy days", rn_c, rn_v, 2,
                       label="bar graph: rainy days in vancouver", source="Source: our class weather log"))
    # salmon pictograph, key 10
    sa_v = [25, 45, 70, 60, 35]
    salmon = fig(pic_svg("Salmon counted at the creek", SALMON, sa_v, 10, "circle", SAL,
                         source="Source: Grade 4 salmon count"))
    W = {}
    W["S1"] = mcq(sport + "How many students chose lacrosse?", fmt(15, S), [fmt(x, S) for x in [3, 10, 20]],
                  "The scale counts by 5s. The lacrosse bar ends on the line for 15. (3 counts the grid spaces as 1 each.)")
    W["S2"] = mcq(sport + "How many more students chose soccer than lacrosse?", fmt(20, S), [fmt(x, S) for x in [4, 50, 15]],
                  "Soccer 35, lacrosse 15. How many more means subtract: 35 − 15 = 20. "
                  "(4 is the difference in grid spaces, and 50 adds the two bars.)")
    W["S3"] = mcq(sport + "Every student chose one sport. How many students took part in the survey?", fmt(125, S),
                  [fmt(x, S) for x in [25, 120, 130]],
                  "Read every bar: 35, 25, 15, 30 and 20. 35 + 25 + 15 + 30 + 20 = 125. "
                  "(25 counts grid spaces: 7 + 5 + 3 + 6 + 4.)")
    W["S4"] = mcq(sport + "The students who chose basketball make teams of 5 for a lunch tournament. How many teams "
                  "do they make?", "6 teams", ["30 teams", "150 teams", "7 teams"],
                  "Basketball ends on 30. 30 ÷ 5 = 6 teams. (7 teams comes from using the soccer bar, 35. "
                  "150 multiplies instead of dividing.)")
    W["S5"] = mcq(sport + "The school will start clubs for the two most popular sports. Which two?",
                  "Soccer and basketball", ["Soccer and hockey", "Basketball and swimming", "Hockey and lacrosse"],
                  "The two tallest bars are soccer (35) and basketball (30). Hockey is 25, the third tallest.")
    W["R1"] = mcq(rain + "Which month had the most rainy days?", "November", ["December", "January", "March"],
                  "The tallest bar is November. It ends on the line for 20. December is 19, just below it.")
    W["R2"] = mcq(rain + "How many rainy days were there in January?", fmt(17, RD), [fmt(x, RD) for x in [16, 18, 19]],
                  "The scale counts by 2s. The January bar ends halfway between 16 and 18, so it shows 17. "
                  "(16 and 18 read the line below or above. 19 is December.)")
    W["R3"] = mcq(rain + "How many more rainy days were there in November than in February?", fmt(7, RD),
                  [fmt(x, RD) for x in [8, 6, 33]],
                  "November 20. February ends halfway between 12 and 14, so 13. 20 − 13 = 7. "
                  "(Reading February as 12 gives 8; as 14 gives 6.)")
    W["R4"] = mcq(rain + "That February had 28 days. How many days in February were <b>not</b> rainy?", "15 days",
                  ["13 days", "16 days", "41 days"],
                  "February had 13 rainy days. 28 − 13 = 15 days without rain. "
                  "(13 is the rainy days, 16 reads February as 12, and 41 adds.)")
    W["R5"] = mcq(rain + "How many rainy days were there altogether from November to March?", fmt(85, RD),
                  [fmt(x, RD) for x in [82, 69, 88]],
                  "Read every bar: 20, 19, 17, 13 and 16. 20 + 19 + 17 + 13 + 16 = 85. "
                  "(82 reads the three bars between lines on the line below; 69 forgets March.)")
    W["R6"] = mcq(rain + "Which statement is true?", "December had 3 more rainy days than March.",
                  ["January had more rainy days than December.", "March had the fewest rainy days.",
                   "Every month had more than 15 rainy days."],
                  "December 19 and March 16: 19 − 16 = 3, so this is true. January (17) had fewer than December (19). "
                  "February (13) had the fewest, so not every month had more than 15.")
    W["F1"] = mcq(salmon + "How many coho salmon were counted?", fmt(45, SAL), [fmt(x, SAL) for x in [5, 40, 41, 50]],
                  "Each circle = 10 salmon, so half a circle = 5. " + read_pic("Coho", 45, 10, "circle", SAL) +
                  " (5 reads each circle as 1. 41 reads the half circle as 1.)")
    W["F2"] = mcq(salmon + "How many circles are in the Coho row?", "4 and a half circles",
                  ["45 circles", "5 circles", "4 circles"],
                  "The Coho row has 4 whole circles and half a circle. That shows 45 salmon, but it is only "
                  "4 and a half circles.")
    W["F3"] = mcq(salmon + "How many more sockeye than Chinook salmon were counted?", fmt(45, SAL),
                  [fmt(x, SAL) for x in [50, 40, 95]],
                  "Sockeye: 7 × 10 = 70. Chinook: 2 × 10 + 5 = 25. 70 − 25 = 45. "
                  "(50 leaves out the half circle; 40 reads it as a whole circle; 95 adds.)")
    W["F4"] = mcq(salmon + "The pink salmon were counted over 3 days, with the same number each day. How many pink "
                  "salmon were counted each day?", fmt(20, SAL), [fmt(x, SAL) for x in [2, 180, 6]],
                  "Pink: 6 circles × 10 = 60 salmon. 60 ÷ 3 = 20 each day. (2 divides the 6 circles, not the salmon; "
                  "180 multiplies.)")
    t = sum(sa_v)
    W["F5"] = mcq(salmon + "How many salmon were counted altogether?", fmt(t, SAL), [fmt(x, SAL) for x in [25, 220, 223]],
                  "Chinook 25, Coho 45, Sockeye 70, Pink 60, Chum 35. 25 + 45 + 70 + 60 + 35 = %d. "
                  "(25 counts the circles; 220 leaves out the three half circles.)" % t)
    assert t == 235
    W["W1"] = mcq("Simran keeps a log of rainy days in Vancouver. She counted 60 rainy days. In her pictograph, each "
                  "cloud stands for 5 days. How many clouds does she draw?", "12 clouds", ["60 clouds", "6 clouds", "300 clouds"],
                  "60 ÷ 5 = 12, so 12 clouds. Check by counting by 5s twelve times: 5, 10, … 60. "
                  "(6 clouds would be right for a key of 10.)")
    W["W2"] = mcq("Mei went whale watching near Victoria. In her pictograph, each symbol stands for 2 orcas. "
                  "Her Saturday row has 4 and a half symbols. How many orcas did she see on Saturday?",
                  "9 orcas", ["5 orcas", "8 orcas", "10 orcas"],
                  "4 symbols × 2 = 8 orcas. Half a symbol is half of 2, which is 1. 8 + 1 = 9 orcas. "
                  "(8 leaves out the half symbol, and 10 reads it as a whole one.)")
    W["W3"] = mcq("On a bar graph with a scale of 10s, the Grade 4 bar for the Terry Fox Run ends halfway between 60 and 70. "
                  "The Grade 5 bar ends on 80. How many more laps did Grade 5 run than Grade 4?",
                  "15 laps", ["20 laps", "10 laps", "145 laps"],
                  "Grade 4: halfway between 60 and 70 is 65. 80 − 65 = 15 laps. "
                  "(Reading Grade 4 as 60 gives 20; as 70 gives 10.)")
    W["W4"] = mcq("Owen’s class voted: 18 students chose soccer and 14 chose hockey. In his pictograph, each ball stands "
                  "for 2 votes. How many more balls are in the Soccer row than in the Hockey row?",
                  "2 balls", ["4 balls", "9 balls", "16 balls"],
                  "Soccer: 18 ÷ 2 = 9 balls. Hockey: 14 ÷ 2 = 7 balls. 9 − 7 = 2 balls. "
                  "(4 is the difference in votes, not in balls.)")
    order = ["S1", "R1", "F2", "S2", "R2", "F1", "S5", "R3", "W1", "W2", "S4", "R4", "F3", "F4", "R6", "S3",
             "W4", "F5", "R5", "W3"]
    assert sorted(order) == sorted(W)
    return {"title": "Word problems: sports, salmon and rainy days", "items": [W[k] for k in order]}


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
    sal_c = ["Chinook", "Coho", "Sockeye", "Pink"]
    sal_v = [30, 45, 60, 25]
    rn_c = ["Nov", "Dec", "Jan", "Feb"]
    rn_v = [20, 19, 17, 13]
    return (
        "<h2>One-to-one and many-to-one</h2>"
        "<p>In a pictograph, each symbol stands for a number. If 1 symbol = 1 student, that is "
        "<b>one-to-one</b> correspondence. If 1 symbol = 2, 5 or 10 students, that is <b>many-to-one</b>. "
        "Many-to-one makes big numbers quick to draw: 80 salmon is only 8 symbols when 1 symbol = 10.</p>"
        "<h2>Read a pictograph</h2>"
        "<p>Look at the <b>key</b> first. Count the symbols by 2s, 5s or 10s. "
        "Half a symbol stands for half of the key.</p>"
        "<figure class='sn-fig'>" + pic_svg("Favourite sport", sp, spv, 2, "circle", STU, source="Source: Grade 4 class vote") +
        "<figcaption>Each circle = 2 students. Lacrosse: 2, 4, 6, and half a circle is 1 more, so 7.</figcaption></figure>" +
        ex("Example", "How many students chose soccer?", "4 circles. Count by 2s: 2, 4, 6, 8.", "8 students") +
        "<figure class='sn-fig'>" + pic_svg("Salmon counted at the creek", sal_c, sal_v, 10, "star", SAL,
                                            source="Source: Grade 4 salmon count") +
        "<figcaption>Each star = 10 salmon, so half a star = 5. Coho: 4 stars and half a star = 40 + 5 = 45.</figcaption></figure>" +
        ex("Example", "How many more sockeye than Chinook?", "Sockeye 6 × 10 = 60. Chinook 3 × 10 = 30. 60 − 30 = 30.",
           "30 more salmon") +
        "<h2>Read a bar graph</h2>"
        "<p>A good bar graph has a <b>title</b>, <b>labels</b>, a <b>scale</b> and a <b>source</b>. "
        "Find what the scale counts by: 2s, 5s or 10s. "
        "If a bar ends halfway between two lines, the number is halfway between them.</p>"
        "<figure class='sn-fig'>" + bar_svg("Rainy days in Vancouver", "Month", "Rainy days", rn_c, rn_v, 2,
                                            label="bar graph: rainy days in vancouver", source="Source: our class weather log") +
        "<figcaption>The scale counts by 2s. January ends halfway between 16 and 18, so it had 17 rainy days.</figcaption></figure>" +
        ex("Example", "How many more rainy days were there in November than in February?",
           "November 20. February is halfway between 12 and 14, so 13. 20 − 13 = 7.", "7 more rainy days") +
        "<h2>Choose a key or a scale</h2>"
        "<p>Look at the data. If every number is in the 5 times table, a key or scale of 5 works. "
        "If every number is in the 10 times table, use 10: it needs the fewest symbols or lines. "
        "Numbers that end in 5 can use half symbols when the key is 10.</p>" +
        ex("Example", "Data: 30, 50, 25, 40 laps. Which key?", "25 is not in the 10 times table, but every number is in the 5 times table.",
           "1 symbol = 5 laps") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Reading each symbol as 1 (4 circles = 4)", "Use the key: 4 circles of 10 = 40"],
            ["Saying half a symbol = 1 for every key", "Half a symbol is half of the key: half of 10 is 5"],
            ["Leaving out a half symbol", "Add it on: 4 and a half stars of 10 = 45"],
            ["Reading a bar between lines as the lower line", "Halfway between 40 and 50 is 45"],
            ["Counting grid spaces instead of reading the scale", "Read the number on the scale"],
        ])
    )


FAQ = [
    {"q": "What do Grade 4 students learn about graphs in the BC math curriculum?",
     "a": "The BC Grade 4 curriculum includes one-to-one and many-to-one correspondence, using bar graphs and pictographs. Students read and make graphs where one symbol or one grid line stands for 2, 5, 10 or more, then compare the data and draw conclusions."},
    {"q": "What is many-to-one correspondence in a pictograph?",
     "a": "It means one symbol stands for more than one thing. If the key says 1 star = 5 students, then 3 stars show 15 students. One-to-one correspondence means 1 symbol = 1 thing."},
    {"q": "How do you read half a symbol in a pictograph?",
     "a": "Half a symbol stands for half of the key. If 1 circle = 10 salmon, half a circle = 5 salmon; if 1 circle = 2 students, half a circle = 1 student."},
    {"q": "Are bar graphs and pictographs on the Grade 4 FSA?",
     "a": "The Grade 4 FSA numeracy section is based on the BC curriculum and can include reading information from graphs and tables to solve problems. Practising with keys and scales, as in these worksheets, is good preparation."},
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
    """Tag pictures that must print larger (graphs and A to D panels) so their labels stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen_unit():
    ASKED.clear()
    rnd = random.Random(34814)
    PK = Picker(rnd)
    sets = [set_pictograph(rnd, PK), set_bar(rnd, PK), set_compare(rnd, PK), set_choose(rnd), set_words(rnd)]
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
        "country": "ca-bc", "subject": "math", "grade": "grade-4", "slug": "bar-graphs-and-pictographs", "sort": 14,
        "updated": UPDATED, "pdf_url": "",
        "title": "Grade 4 Bar Graphs and Pictographs",
        "seo_title": "Grade 4 Bar Graphs and Pictographs Worksheets: Free Math Practice with Answer Key (BC Curriculum)",
        "short_title": "Bar graphs and pictographs",
        "domain": "Data and probability",
        "standard_code": "Grade 4: Data and probability",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/4/core",
        "standard_text": "One-to-one correspondence and many-to-one correspondence, using bar graphs and pictographs",
        "meta_desc": "Free Grade 4 math worksheets on bar graphs and pictographs for the BC curriculum: keys where 1 symbol = 2, 5 or 10, half symbols, scales of 2, 5 and 10, comparing and totalling data, and choosing a key or scale. 100 questions with an answer key, good FSA numeracy practice.",
        "key_big": "Read the key or the scale first. If 1 symbol = 10, then 4 symbols = 40 and half a symbol = 5.",
        "key_sub": "On a bar graph, check what the scale counts by. A bar halfway between 40 and 50 shows 45, not 41. Multiply by the key: never read a symbol or a grid space as 1.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(pictograph|bar graph)")


if __name__ == "__main__":
    u = gen_unit()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
