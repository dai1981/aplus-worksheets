# -*- coding: utf-8 -*-
"""
CA Grade 3 Math: Data and graphs (Ontario Curriculum 2020, Data: D1.1 to D1.5)
  python3 tools/gen_ca_math_g3_data.py
Sorting data in Venn and Carroll diagrams, tally marks and frequency tables, pictographs with many-to-one
correspondence (1 symbol = 2, 5 or 10), bar graphs with scales of 2 and 5 (with sources, titles and labels),
the mode, and drawing conclusions from data in Canadian contexts.
Wrong answers come from real student mistakes: reading a symbol as 1, misreading the scale (line below, line
above, counting grid spaces), giving the biggest number (the frequency) as the mode, counting a tally group of 5
as 4, counting the overlap of a Venn diagram twice or forgetting the items outside the circles.
HTML attributes use single quotes (no backslashes in the JSON). Canadian English.
"""
import json, re, math, os, random

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-3")
UPDATED = "2026-11-02"
GREEN = "#006633"
BAR = "#2e8b57"
BAR2 = "#3a6ea5"
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


def dollars(v):
    return "$%d" % v


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

    def both(self, a, b):
        return self.both_f.format(a=self.p(a), b=self.p(b))


VOTE = ("vote", "votes")
STU = ("student", "students")
LOWER = lambda cs: {c: c.lower() for c in cs}
TEACH = ["Ms. Lee", "Mr. Khan", "Mme Roy", "Mr. Chen"]
POSS = {t: t + "’s class" for t in TEACH}

CTXS = [
    Ctx("Favourite winter sport", "Sport", ["Hockey", "Skating", "Skiing", "Sledding", "Ringette"], STU,
        "How many students chose {a}?", "How many more students chose {a} than {b}?",
        "How many fewer students chose {a} than {b}?", "How many students chose {a} or {b}?",
        "How many students voted altogether?", [2, 5], [2, 5], "Source: school vote",
        ph=LOWER(["Hockey", "Skating", "Skiing", "Sledding", "Ringette"])),
    Ctx("Favourite Canadian animal", "Animal", ["Beaver", "Moose", "Loon", "Polar bear", "Orca"], VOTE,
        "How many votes did the {a} get?", "How many more votes did the {a} get than the {b}?",
        "How many fewer votes did the {a} get than the {b}?", "How many votes did the {a} and the {b} get altogether?",
        "How many votes were there altogether?", [2, 5], [2, 5], "Source: school vote",
        ph=LOWER(["Beaver", "Moose", "Loon", "Polar bear", "Orca"])),
    Ctx("How we get to school", "Way to school", ["Walk", "Car", "Bus", "Bike"], STU,
        "How many students {a} to school?", "How many more students {a} to school than {b}?",
        "How many fewer students {a} to school than {b}?", "How many students {a} or {b} to school?",
        "How many students are in the survey altogether?", [2, 5], [2, 5], "Source: school survey",
        ph={"Walk": "walk", "Car": "come by car", "Bus": "take the bus", "Bike": "ride a bike"}),
    Ctx("Birds at the school feeder", "Bird", ["Chickadee", "Blue jay", "Cardinal", "Sparrow", "Junco"], ("bird", "birds"),
        "How many {a} were seen?", "How many more {a} than {b} were seen?",
        "How many fewer {a} than {b} were seen?", "How many {a} and {b} were seen altogether?",
        "How many birds were seen altogether?", [2], [2], "Source: our class bird count", maxv=20,
        ph={"Chickadee": "chickadees", "Blue jay": "blue jays", "Cardinal": "cardinals", "Sparrow": "sparrows",
            "Junco": "juncos"}),
    Ctx("Hot chocolates sold at the rink", "Day", ["Mon", "Tue", "Wed", "Thu", "Fri"], ("hot chocolate", "hot chocolates"),
        "How many hot chocolates were sold on {a}?", "How many more hot chocolates were sold on {a} than on {b}?",
        "How many fewer hot chocolates were sold on {a} than on {b}?",
        "How many hot chocolates were sold on {a} and {b} altogether?",
        "How many hot chocolates were sold altogether?", [5], [5, 10], "Source: rink snack bar records", ordered=True,
        ph={"Mon": "Monday", "Tue": "Tuesday", "Wed": "Wednesday", "Thu": "Thursday", "Fri": "Friday"}),
    Ctx("Cans for the food drive", "Class", TEACH, ("can", "cans"),
        "How many cans did {a} collect?", "How many more cans did {a} collect than {b}?",
        "How many fewer cans did {a} collect than {b}?", "How many cans did {a} and {b} collect altogether?",
        "How many cans did the classes collect altogether?", [5], [5, 10], "Source: school food drive count",
        ph=POSS),
    Ctx("Books read in March", "Student", ["Liam", "Olivia", "Arjun", "Mei", "Ethan", "Priya"], ("book", "books"),
        "How many books did {a} read?", "How many more books did {a} read than {b}?",
        "How many fewer books did {a} read than {b}?", "How many books did {a} and {b} read altogether?",
        "How many books did the students read altogether?", [2], [2], "Source: class reading logs", maxv=20),
    Ctx("Apples picked on the field trip", "Student", ["Noah", "Emma", "Aiden", "Zoe", "Mateo"], ("apple", "apples"),
        "How many apples did {a} pick?", "How many more apples did {a} pick than {b}?",
        "How many fewer apples did {a} pick than {b}?", "How many apples did {a} and {b} pick altogether?",
        "How many apples did they pick altogether?", [2, 5], [2, 5, 10], "Source: field trip tally sheet"),
    Ctx("Laps at the Terry Fox Run", "Grade", ["Gr. 1", "Gr. 2", "Gr. 3", "Gr. 4", "Gr. 5"], ("lap", "laps"),
        "How many laps did {a} run?", "How many more laps did {a} run than {b}?",
        "How many fewer laps did {a} run than {b}?", "How many laps did {a} and {b} run altogether?",
        "How many laps did the five grades run altogether?", [5], [5, 10], "Source: Terry Fox Run lap cards",
        ordered=True, ph={"Gr. %d" % g: "the Grade %d students" % g for g in range(1, 6)}),
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


def source_line(W, y, src):
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
        s.append(source_line(W, ky + 24, source))
        H = ky + 30
    return (W, H, "".join(s))


def ctx_pic(ctx, cats, vals, key, sym):
    return part_svg(pic_part(ctx.title, cats, vals, key, sym, ctx.unit, source=ctx.source),
                    "pictograph: " + ctx.title.lower())


# ------------------------------------------------------------ bar graph
def bar_part(title, cat_axis, val_axis, cats, vals, scale, missing=None, top_v=None, col=BAR, source=None):
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
    if source:
        s.append(source_line(W, yb + 60, source))
        H = yb + 66
    assert tw(val_axis, fs, True) < ph + 26, (val_axis, ph)
    return (W, H, "".join(s))


def bar_svg(title, cat_axis, val_axis, cats, vals, scale, missing=None, label="bar graph", source=None):
    return part_svg(bar_part(title, cat_axis, val_axis, cats, vals, scale, missing, source=source), label)


def ctx_bar(ctx, cats, vals, scale, missing=None, title=True):
    return bar_svg(ctx.title if title else "", ctx.axis, ctx.unit[1].capitalize(), cats, vals,
                   scale, missing, label="bar graph: " + ctx.title.lower(), source=ctx.source)


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


def freq_part(title, head, cats, vals, tally=True, freq=True, missing=None):
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
    for r, (c, v) in enumerate(rows):
        y = top + r * rh
        hd = r == 0
        x = x0
        for k, cw in enumerate(cols):
            s.append("<rect x='%.1f' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.5'/>"
                     % (x, y, cw, rh, FILL2 if hd or k == 0 else "#ffffff", GREEN))
            name = "freq" if (k == 2 or (k == 1 and not tally)) else ("tally" if k == 1 else "cat")
            if name == "cat":
                s.append(text(x + 10, y + 19, c, fs, anchor="start", bold=hd))
            elif hd:
                s.append(text(x + 10 if name == "tally" else x + cw / 2, y + 19, "Tally" if name == "tally" else "Frequency",
                              fs, anchor="start" if name == "tally" else "middle", bold=True))
            elif name == "tally":
                s.append(tally_marks(x + 14, y + rh / 2, v))
            else:
                if r - 1 == missing:
                    s.append(text(x + cw / 2, y + 20, "?", 17, bold=True, col=RED))
                else:
                    s.append(text(x + cw / 2, y + 19, v, fs))
            x += cw
    H = top + len(rows) * rh + 4
    return (W, H, "".join(s))


def freq_svg(title, head, cats, vals, label, **kw):
    return part_svg(freq_part(title, head, cats, vals, **kw), label)


# ------------------------------------------------------------ Venn and Carroll diagrams
VW, VCX1, VCX2, VCY, VR = 410, 165, 245, 132, 90


def venn_svg(la, lb, a_only, both, b_only, outside, label, fs=15):
    """Two overlapping circles in a box. Items are text; each item is checked to sit inside its region."""
    H = VCY + VR + 40
    s = ["<rect x='3' y='3' width='%d' height='%d' rx='6' fill='#ffffff' stroke='%s' stroke-width='1.5'/>" % (VW - 6, H - 6, GREEN),
         "<circle cx='%d' cy='%d' r='%d' fill='%s' fill-opacity='0.45' stroke='%s' stroke-width='2'/>" % (VCX1, VCY, VR, FILL, GREEN),
         "<circle cx='%d' cy='%d' r='%d' fill='%s' fill-opacity='0.35' stroke='%s' stroke-width='2'/>" % (VCX2, VCY, VR, "#d6e2f0", BAR2),
         text(VCX1 - 40, 30, la, 15, bold=True, col=GREEN),
         text(VCX2 + 40, 30, lb, 15, bold=True, col=BAR2)]
    assert VCX1 - 40 - tw(la, 15, True) / 2 > 6 and VCX2 + 40 + tw(lb, 15, True) / 2 < VW - 6, (la, lb)
    assert abs((VCX1 - 40 + tw(la, 15, True) / 2) - (VCX2 + 40 - tw(lb, 15, True) / 2)) > 0 and \
        VCX1 - 40 + tw(la, 15, True) / 2 < VCX2 + 40 - tw(lb, 15, True) / 2 - 8, (la, lb)

    def inside(px, py, cx):
        return (px - cx) ** 2 + (py - VCY) ** 2 < (VR - 3) ** 2

    def outside_c(px, py, cx):
        return (px - cx) ** 2 + (py - VCY) ** 2 > (VR + 3) ** 2

    def place(items, x, region):
        n = len(items)
        for k, t in enumerate(items):
            yc = VCY + (k - (n - 1) / 2.0) * 25
            w = tw(t, fs) / 2
            for px in (x - w, x + w):
                for py in (yc - 7, yc + 7):
                    a, b = inside(px, py, VCX1), inside(px, py, VCX2)
                    oa, ob = outside_c(px, py, VCX1), outside_c(px, py, VCX2)
                    ok = {"a": a and ob, "b": b and oa, "ab": a and b}[region]
                    assert ok, (t, region, px, py)
            s.append(text(x, yc + 5, t, fs))
    place(a_only, 116, "a")
    place(both, (VCX1 + VCX2) / 2.0, "ab")
    place(b_only, 294, "b")
    # outside: one row under the circles
    if outside:
        widths = [tw(t, fs) for t in outside]
        gap = 22
        tot = sum(widths) + gap * (len(outside) - 1)
        x = (VW - tot) / 2
        yb = VCY + VR + 24
        for t, w in zip(outside, widths):
            s.append(text(x + w / 2, yb, t, fs))
            x += w + gap
        assert tot < VW - 20
    return svg_wrap(VW, H, "".join(s), label)


def carroll_svg(cols, rows, cells, label, letters=False, fs=15):
    """2 x 2 Carroll diagram. cells[r][c] = list of lines of text."""
    hw = int(max(tw(r, fs, True) for r in rows) + 20)
    cw = int(max(max(tw(c, fs, True) for c in cols) + 20,
                 max(tw(line, fs) for row in cells for cell in row for line in cell) + (44 if letters else 24)))
    hh = 30
    nl = max(len(cell) for row in cells for cell in row)
    rh = max(40, 16 + 22 * nl)
    W = hw + 2 * cw + 8
    H = hh + 2 * rh + 8
    x0, y0 = 4, 4
    s = []
    for c in range(2):
        x = x0 + hw + c * cw
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.5'/>" % (x, y0, cw, hh, FILL2, GREEN))
        s.append(text(x + cw / 2, y0 + 20, cols[c], fs, bold=True))
    for r in range(2):
        y = y0 + hh + r * rh
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.5'/>" % (x0, y, hw, rh, FILL2, GREEN))
        s.append(text(x0 + hw / 2, y + rh / 2 + 5, rows[r], fs, bold=True))
        for c in range(2):
            x = x0 + hw + c * cw
            s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='#ffffff' stroke='%s' stroke-width='1.5'/>" % (x, y, cw, rh, GREEN))
            if letters:
                s.append(text(x + 8, y + 19, "ABCD"[r * 2 + c], 16, anchor="start", bold=True, col=BAR2))
            lines = cells[r][c]
            for k, line in enumerate(lines):
                ly = y + rh / 2 + 5 + (k - (len(lines) - 1) / 2.0) * 22
                s.append(text(x + cw / 2 + (8 if letters else 0), ly, line, fs))
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


def pic_wrong(v, key):
    """Real misreadings of one pictograph row."""
    full, hf = v // key, v % key
    out = [full + (1 if hf else 0)]                 # read each symbol as 1
    if hf:
        out += [full * key + 1, full * key, (full + 1) * key]   # half = 1 / ignored the half / half as whole
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


# ------------------------------------------------------------ set 1: sorting in Venn and Carroll diagrams
def set_sort(rnd):
    its = []
    WHERE = ["In the overlap", "Only in Even", "Only in More than 50", "Outside the circles"]
    A1, AB, B1, O = ["12", "36", "8", "44"], ["64", "90", "58"], ["71", "85", "53"], ["27", "9", "45"]
    v1 = fig(venn_svg("Even", "More than 50", A1, AB, B1, O, "venn diagram: even numbers and numbers more than 50"))
    # 1
    its.append(mcq(v1 + "How many numbers are even <b>and</b> more than 50?", 3, [7, 6, 4],
                   "Numbers that are in both circles go in the overlap, where the circles cross: 64, 90 and 58. "
                   "That is 3 numbers. (7 counts the whole Even circle, and 6 counts the whole More than 50 circle.)"))
    # 2-4 where does it go?
    its.append(mcq(v1 + "Where should 72 go?", WHERE[0], WHERE[1:],
                   "72 is even (it ends in 2) and 72 is more than 50. It belongs in both circles, so it goes in the overlap."))
    its.append(mcq(v1 + "Where should 49 go?", WHERE[3], WHERE[:3],
                   "49 is odd (it ends in 9), so it is not in Even. 49 is less than 50, so it is not in More than 50. "
                   "It goes outside both circles."))
    its.append(mcq(v1 + "Where should 50 go?", WHERE[1], [WHERE[0], WHERE[2], WHERE[3]],
                   "50 is even. But 50 is not <b>more than</b> 50, because it is equal to 50. "
                   "So 50 goes only in the Even circle, not in the overlap."))
    # 5 wrong place
    v2 = fig(venn_svg("Even", "More than 50", ["12", "36", "8"], ["64", "46", "90"], ["71", "85", "53"], ["27", "9", "45"],
                      "venn diagram with one number in the wrong place"))
    its.append(mcq(v2 + "One number is in the wrong place. Which number is it?", 46, [64, 53, 27],
                   "46 is even, but 46 is less than 50. It should be only in the Even circle, not in the overlap. "
                   "64 is even and more than 50, so it is in the right place."))
    # 6 not even
    its.append(mcq(v1 + "How many numbers are <b>not</b> even?", 6, [3, 7, 13],
                   "The numbers that are not even are outside the Even circle: 71, 85 and 53 in the other circle, "
                   "and 27, 9 and 45 outside both circles. 3 + 3 = 6. Do not forget the numbers outside the circles."))
    # 7-10 students
    vs = fig(venn_svg("Plays hockey", "Plays soccer", ["Liam", "Ava", "Mateo", "Chloe"], ["Emma", "Kai", "Owen"],
                      ["Priya", "Ethan"], ["Mei", "Arjun", "Zoe", "Nathan"], "venn diagram: students who play hockey and soccer"))
    its.append(mcq(vs + "How many students play <b>both</b> hockey and soccer?", fmt(3, STU), [fmt(x, STU) for x in [6, 12, 7]],
                   "Students who play both sports are in the overlap: Emma, Kai and Owen. That is 3 students."))
    its.append(mcq(vs + "How many students play hockey?", fmt(7, STU), [fmt(x, STU) for x in [4, 3, 12]],
                   "Count the whole hockey circle, including the overlap: Liam, Ava, Mateo, Chloe (4) and Emma, Kai, Owen (3). "
                   "4 + 3 = 7. (4 forgets the students in the overlap.)"))
    its.append(mcq(vs + "How many students play neither hockey nor soccer?", fmt(4, STU), [fmt(x, STU) for x in [10, 2, 13]],
                   "Neither means outside both circles: Mei, Arjun, Zoe and Nathan. That is 4 students."))
    its.append(mcq(vs + "How many students were sorted altogether?", fmt(13, STU), [fmt(x, STU) for x in [9, 16, 12]],
                   "Count each student once: 4 + 3 + 2 + 4 = 13. Count the overlap only once, and remember the 4 students "
                   "outside the circles. (9 forgets the students outside; 16 counts the overlap twice.)"))
    # 11-13 Carroll diagram with boxes A to D
    cols, rows = ["Less than 500", "500 or more"], ["Even", "Odd"]
    cl = fig(carroll_svg(cols, rows, [[["128, 346, 90"], ["712, 584"]], [["237, 451, 69"], ["905, 663"]]],
                         "carroll diagram: even and odd numbers, less than 500 and 500 or more", letters=True))
    its.append(mcq_fixed(cl + "Which box should 734 go in?", ["A", "B", "C", "D"], 1,
                         "734 ends in 4, so it is even: top row. 734 is 500 or more: right column. That is box B."))
    its.append(mcq_fixed(cl + "Which box should 815 go in?", ["A", "B", "C", "D"], 3,
                         "815 ends in 5, so it is odd: bottom row. 815 is 500 or more: right column. That is box D."))
    its.append(mcq_fixed(cl + "Which box should 500 go in?", ["A", "B", "C", "D"], 1,
                         "500 ends in 0, so it is even: top row. 500 is not less than 500, so it goes in the "
                         "“500 or more” column. That is box B."))
    # 14 wrong box
    cw_ = fig(carroll_svg(cols, rows, [[["128, 346, 90"], ["712, 584"]], [["237, 557, 69"], ["905, 663"]]],
                          "carroll diagram with one number in the wrong box"))
    its.append(mcq(cw_ + "One number is in the wrong box. Which number is it?", 557, [237, 663, 346],
                   "557 is odd, so the bottom row is right. But 557 is more than 500, so it belongs in the "
                   "“500 or more” column, not “Less than 500”."))
    # 15-17 Carroll diagram with counts
    cc = fig(carroll_svg(["Walks to school", "Does not walk"], ["Has a pet", "No pet"], [[["6"], ["9"]], [["4"], ["7"]]],
                         "carroll diagram: students who walk to school and students who have a pet"))
    its.append(mcq(cc + "How many students have a pet <b>and</b> walk to school?", fmt(6, STU), [fmt(x, STU) for x in [10, 15, 9]],
                   "Find the box in the “Has a pet” row and the “Walks to school” column. It says 6."))
    its.append(mcq(cc + "How many students walk to school?", fmt(10, STU), [fmt(x, STU) for x in [6, 15, 4]],
                   "Add both boxes in the “Walks to school” column: 6 + 4 = 10. (6 is only the walkers with a pet.)"))
    its.append(mcq(cc + "How many students do <b>not</b> have a pet?", fmt(11, STU), [fmt(x, STU) for x in [7, 15, 4]],
                   "Add both boxes in the “No pet” row: 4 + 7 = 11."))
    # 18 find the label
    vl = fig(venn_svg("Even", "?", ["4", "8", "12", "16"], ["10", "20", "30"], ["15", "25", "35"], ["3", "7", "11"],
                      "venn diagram with a missing label"))
    its.append(mcq(vl + "What is the best label for the second circle?", "Multiples of 5",
                   ["Odd numbers", "Multiples of 10", "More than 10"],
                   "Every number in the second circle is in the 5 times table: 10, 20, 30, 15, 25, 35. "
                   "It cannot be Odd numbers (10 is even) or Multiples of 10 (15 is not). "
                   "More than 10 does not work, because 12 and 16 are outside it."))
    # 19 counts in a Venn diagram
    vc = fig(venn_svg("Plays hockey", "Plays soccer", ["10"], ["5"], ["6"], ["?"], "venn diagram with the number of students"))
    its.append(mcq(vc + "There are 28 students in the class. The numbers show how many students are in each part. "
                   "How many students play neither sport?", fmt(7, STU), [fmt(x, STU) for x in [2, 12, 21]],
                   "Students in the circles: 10 + 5 + 6 = 21. 28 − 21 = 7 students are outside both circles. "
                   "(2 comes from 28 − 15 − 11, which counts the 5 students in the overlap twice.)"))
    # 20 word problem
    its.append(mcq("Hana sorts the numbers 14, 30, 7 and 25 into a Venn diagram. The circles are “Even” and "
                   "“Multiples of 5”. Which number goes in the overlap?", 30, [25, 14, 7],
                   "30 is even and 30 is in the 5 times table, so it goes in the overlap. 25 is a multiple of 5 but odd. "
                   "14 is even but not a multiple of 5. 7 goes outside both circles."))
    assert len(its) == 20
    return {"title": "Sort data in Venn and Carroll diagrams", "items": its}


# ------------------------------------------------------------ set 2: tally marks and frequency tables
def set_tally(rnd):
    its = []
    for v in (8, 13, 19, 22):
        its.append(mcq(fig(tally_only_svg(v)) + "What number do these tally marks show?", v, tally_cands(v),
                       "Each group of 5 is four lines with one line across. Count the groups in 5s, then count on the "
                       "single marks: %s" % tally_text(v)))
    vs = [16, 21, 15, 17]
    pos = 2
    order = vs[1:]
    order.insert(pos, vs[0])
    s = []
    for k, v in enumerate(order):
        x0, y0 = (k % 2) * 190, (k // 2) * 44
        s.append(text(x0 + 8, y0 + 27, "ABCD"[k], 17, anchor="start", bold=True))
        s.append(tally_marks(x0 + 34, y0 + 21, v))
        assert x0 + 34 + tally_width(v) < x0 + 186
    svg = svg_wrap(380, 88, "".join(s), "four sets of tally marks")
    wrong = {21: "one group of 5 too many", 15: "one single mark is missing", 17: "one single mark too many"}
    its.append(mcq_fixed(fig(svg) + "Which tally marks show 16?", ["A", "B", "C", "D"], pos,
                         "16 = 5 + 5 + 5 + 1, so look for 3 groups of 5 and 1 single mark. That is %s. "
                         % "ABCD"[pos] + "; ".join("%s shows %d (%s)" % ("ABCD"[k], v, wrong[v])
                                                    for k, v in enumerate(order) if v != 16) + "."))
    # 6-9 favourite winter sport with tallies
    cats = ["Hockey", "Skating", "Skiing", "Sledding", "Ringette"]
    vals = [9, 14, 6, 11, 4]
    f = fig(freq_svg("Favourite winter sport", "Sport", cats, vals, "frequency table: favourite winter sport", missing=1))
    its.append(mcq(f + "What number should go in the Frequency column for Skating?", 14, tally_cands(14, [9, 11]),
                   "The frequency is the number the tally marks show. Skating has %s" % tally_text(14)))
    its.append(mcq(f + "Which sport got the most votes?", "Skating", ["Sledding", "Hockey", "Ringette"],
                   "Skating has 14 votes (2 groups of 5 and 4 more). That is more than Sledding (11) and Hockey (9)."))
    its.append(mcq(f + "How many more students chose sledding than ringette?", fmt(7, STU),
                   [fmt(x, STU) for x in [15, 6, 8, 11]],
                   "Sledding 11, ringette 4. How many more means find the difference: 11 − 4 = 7."))
    tot = sum(vals)
    its.append(mcq(f + "How many students voted altogether? (Each student voted once.)", fmt(tot, STU),
                   [fmt(x, STU) for x in [tot - 14, sum((v // 5) * 4 + v % 5 for v in vals), tot - 4, tot + 1]],
                   "Find the Skating frequency first: 14. Then add all the rows: 9 + 14 + 6 + 11 + 4 = %d." % tot))
    # 10-13 quantitative data: people in families
    FAM = ("family", "families")
    cats = ["2", "3", "4", "5", "6"]
    vals = [3, 8, 10, 5, 2]
    f = fig(freq_svg("People in our families", "People", cats, vals, "frequency table: people in our families"))
    its.append(mcq(f + "How many families have 4 people?", fmt(10, FAM), [fmt(x, FAM) for x in [4, 8, 2, 12, 7]],
                   "Find the row for 4 people. The frequency is 10 (2 groups of 5). "
                   "The 4 is the number of people, not the number of families."))
    its.append(mcq(f + "What is the most common family size?", "4 people",
                   ["10 people", "6 people", "3 people"],
                   "The biggest frequency is 10, in the row for 4 people. So 4 people is the most common family size. "
                   "10 is how many families, not how many people."))
    its.append(mcq(f + "How many families are in the survey?", fmt(28, FAM), [fmt(x, FAM) for x in [20, 5, 10, 27]],
                   "Add the frequencies: 3 + 8 + 10 + 5 + 2 = 28 families. (20 is 2 + 3 + 4 + 5 + 6, the family sizes.)"))
    its.append(mcq(f + "How many families have more than 4 people?", fmt(7, FAM), [fmt(x, FAM) for x in [17, 11, 2]],
                   "More than 4 means 5 or 6 people: 5 + 2 = 7 families. Do not include the families with exactly 4 people. "
                   "(17 adds the 4-people row too.)"))
    # 14-16 frequency table without tallies: birds
    B = ("bird", "birds")
    cats = ["Chickadee", "Blue jay", "Cardinal", "Sparrow", "Junco"]
    vals = [12, 6, 8, 15, 3]
    f = fig(freq_svg("Birds at the school feeder", "Bird", cats, vals, "frequency table: birds at the school feeder",
                     tally=False))
    its.append(mcq(f + "How many more chickadees than cardinals were seen?", fmt(4, B), [fmt(x, B) for x in [20, 12, 5, 3]],
                   "Chickadee 12, cardinal 8. How many more means subtract: 12 − 8 = 4."))
    its.append(mcq(f + "Which bird was seen half as many times as the chickadee?", "Blue jay", ["Cardinal", "Junco", "Sparrow"],
                   "The chickadee was seen 12 times. Half of 12 is 6. The blue jay has a frequency of 6."))
    its.append(mcq(f + "Owen sees 4 more sparrows. What is the new frequency for Sparrow?", 19, [11, 15, 4, 20],
                   "The sparrow frequency was 15. 4 more means add: 15 + 4 = 19."))
    # 17-18 qualitative and quantitative
    its.append(mcq("Which survey question has answers that are numbers?", "How many pets do you have?",
                   ["What is your favourite colour?", "How do you get to school?", "What is your favourite winter sport?"],
                   "“How many pets do you have?” has number answers, such as 0, 1, 2 or 3 (quantitative data). "
                   "The other questions have answers that are words, such as red, bus or hockey (qualitative data)."))
    its.append(mcq("Which survey question has answers that are words, not numbers?",
                   "What is your favourite fruit?",
                   ["How many brothers and sisters do you have?", "How many books did you read this week?",
                    "How many people are in your family?"],
                   "Favourite fruit gives answers like apple or banana. These are words (qualitative data). "
                   "The other questions ask “how many”, so the answers are numbers."))
    # 19-20 word problems
    its.append(mcq("Noah makes a tally of the Canada geese that fly over the schoolyard. He draws 4 groups of five and "
                   "3 single marks. How many geese has he counted?", fmt(23, ("goose", "geese")),
                   [fmt(x, ("goose", "geese")) for x in [19, 7, 43, 24]],
                   "Each group of five shows 5: 5, 10, 15, 20. Then 3 more: 21, 22, 23. So 23 geese. "
                   "(Counting each group as 4 gives 19.)"))
    its.append(mcq("Sofia counted 17 votes for ringette. How should she draw the tally?", "3 groups of five and 2 marks",
                   ["2 groups of five and 7 marks", "4 groups of five and 1 mark", "17 groups of five"],
                   "17 = 5 + 5 + 5 + 2. Draw 3 groups of five (four lines and one across) and 2 single marks. "
                   "Never leave 5 or more single marks: make another group of five."))
    assert len(its) == 20
    return {"title": "Tally marks and frequency tables", "items": its}


# ------------------------------------------------------------ set 3: pictographs, 1 symbol = 2, 5 or 10
ASKED = set()


def pick_row(rnd, ctx, cats, js):
    """A row/bar that has not been asked about before in this context (so no two questions read the same)."""
    fresh = [j for j in js if (ctx.title, cats[j]) not in ASKED]
    j = rnd.choice(fresh or js)
    ASKED.add((ctx.title, cats[j]))
    return j


def set_pictograph(rnd, PK):
    its = []
    plan = [(2, "read"), (2, "most"), (2, "readh"), (2, "which"), (2, "draw"), (2, "more"), (2, "fewest"),
            (5, "read"), (5, "which"), (5, "draw"), (5, "read"), (5, "more"), (5, "total"),
            (10, "read"), (10, "readh"), (10, "half"), (10, "which"), (10, "draw"), (10, "more"), (10, "total")]
    draws = iter([("Each star stands for 2 books. Priya read 14 books. How many stars should be in her row?", 14, 2, "star"),
                  ("Each square stands for 5 students. 30 students walk to school. How many squares should be in the Walk row?",
                   30, 5, "square"),
                  ("Each circle stands for 10 cans. Mr. Khan’s class collected 70 cans. How many circles should be in "
                   "the class’s row?", 70, 10, "circle")])
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
        half = (key == 2 and kind in ("readh", "which")) or (key == 10 and kind in ("readh", "half"))
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
                           [fmt(1, U), fmt(key, U), fmt(key * 2, U)],
                           "The key says one whole %s = %s. Half a %s is half of %d, which is %s. "
                           "(Half a symbol is not always 1. It is half of the key.)"
                           % (sym, fmt(key, U), sym, key, fmt(key // 2, U))))
        elif kind == "which":
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
        elif kind == "more":
            pairs = [(a, b) for a in range(n) for b in range(n) if vals[a] - vals[b] >= 2 * key]
            a, b = rnd.choice(pairs)
            d = vals[a] - vals[b]
            cand = [d // key, vals[a] + vals[b], d + key, d - key, vals[a]]
            its.append(mcq(f + ctx.more(cats[a], cats[b]), fmt(d, U), [fmt(x, U) for x in cand],
                           "%s%s: %s. %s: %s. How many more means find the difference: %d − %d = %s. "
                           "(%d is the difference in symbols, not in %s.)"
                           % (keytxt, cats[a], short_pic(vals[a], key), cats[b], short_pic(vals[b], key),
                              vals[a], vals[b], fmt(d, U), d // key, U[1])))
        else:
            t = sum(vals)
            nsym = sum(math.ceil(v / key) for v in vals)
            cand = [nsym, t - min(vals), t + key, t - key]
            its.append(mcq(f + ctx.total, fmt(t, U), [fmt(x, U) for x in cand],
                           "%sRead every row: %s. Add them: %s = %s. (%d is the number of symbols.)"
                           % (keytxt, ", ".join("%s %d" % (c, v) for c, v in zip(cats, vals)),
                              " + ".join(str(v) for v in vals), fmt(t, U), nsym)))
    return {"title": "Pictographs: 1 symbol = 2, 5 or 10", "items": its}


# ------------------------------------------------------------ set 4: bar graphs with scales of 2 and 5
MATCH_WHY = {
    "swap": "two bars are the wrong way round",
    "low": "a bar is on the line below (it should be halfway between two lines)",
    "high": "one bar is one line too high",
    "lowl": "one bar is one line too low",
}


def match_q(rnd, pos, title, cats, vals, step, unit):
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
    tb = "<b>%s</b> (frequency table): %s. " % (title, ", ".join("%s %d" % (c, v) for c, v in zip(cats, vals)))
    return mcq_fixed(fig(svg) + tb + "Which bar graph shows the same data?", ["A", "B", "C", "D"], pos, e)


def set_bar(rnd, PK):
    its = []
    plan = [(2, "step"), (2, "read"), (2, "readh"), (2, "which"), (2, "readh"), (2, "fewest"), (2, "more"),
            (5, "step"), (5, "read"), (5, "which"), (5, "read"), (5, "most"), (5, "more"), (5, "both")]
    for i, (sc, kind) in enumerate(plan):
        ctx = PK.next(lambda c: sc in c.scales)
        half = sc == 2 and kind in ("readh", "which", "more")
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
        elif kind in ("most", "fewest"):
            j = vals.index(max(vals) if kind == "most" else min(vals))
            word = "tallest" if kind == "most" else "shortest"
            q = "Which bar shows the %s %s?" % ("most" if kind == "most" else "fewest", U[1])
            its.append(mcq(f + q, cats[j], [cats[k] for k in range(n) if k != j],
                           "The bar for %s is the %s one. %s It shows %s." % (cats[j], word, read_bar(cats[j], vals[j], sc),
                                                                          fmt(vals[j], U))))
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
            cand = [vals[a] + vals[b]] + mis + spaces + [d + sc, d - sc, vals[a]]
            its.append(mcq(f + ctx.more(cats[a], cats[b]), fmt(d, U), [fmt(x, U) for x in cand],
                           "%s%s: %d. %s: %d. How many more means find the difference: %d − %d = %s."
                           % (scl, cats[a], vals[a], cats[b], vals[b], vals[a], vals[b], fmt(d, U))))
        else:
            pairs = [(x, y) for x in range(n) for y in range(n) if x < y and (vals[x] + vals[y]) // sc not in vals]
            a, b = rnd.choice(pairs)
            t = vals[a] + vals[b]
            gs = t // sc
            assert gs not in vals, (vals, gs)
            cand = [gs, abs(vals[a] - vals[b]), t + sc, t - sc]
            its.append(mcq(f + ctx.both(cats[a], cats[b]), fmt(t, U), [fmt(x, U) for x in cand],
                           "%s%s: %d. %s: %d. Altogether means add: %d + %d = %s. (%d counts grid spaces, not %s.)"
                           % (scl, cats[a], vals[a], cats[b], vals[b], vals[a], vals[b], fmt(t, U), gs, U[1])))
    # 15-16 table -> bar graph (A to D)
    its.append(match_q(rnd, 2, "Favourite Canadian animal", ["Loon", "Orca", "Lynx", "Bear"], [8, 13, 6, 10], 2, VOTE))
    its.append(match_q(rnd, 0, "Hot chocolates sold at the rink", ["Mon", "Tue", "Wed", "Thu"], [25, 35, 15, 30], 5,
                       ("hot chocolate", "hot chocolates")))
    # 17 missing title
    an = BYTITLE["Favourite Canadian animal"]
    f = fig(ctx_bar(an, ["Beaver", "Moose", "Loon", "Polar bear"], [8, 5, 11, 6], 2, title=False)
            .replace("aria-label='bar graph: favourite canadian animal'", "aria-label='bar graph with no title'"))
    its.append(mcq(f + "Every bar graph needs a title, labels, a scale and a source. What is missing from this bar graph?",
                   "A title", ["A scale", "Labels", "A source"],
                   "The graph has a scale (0, 2, 4 …), labels (Animal and Votes), and a source under the graph. "
                   "It has no title at the top. A good title is “Favourite Canadian animal”."))
    # 18 source
    hc = BYTITLE["Hot chocolates sold at the rink"]
    f = fig(ctx_bar(hc, ["Mon", "Tue", "Wed", "Thu", "Fri"], [15, 25, 10, 30, 45], 5))
    its.append(mcq(f + "Where did the data in this bar graph come from?", "The rink snack bar records",
                   ["A vote in a Grade 3 class", "The scale on the left", "A weather report"],
                   "The source is written under the graph: “Source: rink snack bar records”. "
                   "The source tells where the data came from."))
    # 19 choose a scale
    its.append(mcq("Owen will make a bar graph of this data: 15, 40, 25 and 35. Which scale is best?", "Count by 5s",
                   ["Count by 1s", "Count by 2s", "Count by 100s"],
                   "All the numbers are in the 5 times table, so every bar ends on a line when the scale counts by 5s: "
                   "0, 5, 10 … 40. Counting by 1s or 2s needs too many lines (and 15, 25, 35 fall between lines of 2). "
                   "Counting by 100s makes every bar too short to read."))
    # 20 list that matches
    cn = BYTITLE["Cans for the food drive"]
    cats, vals = TEACH, [30, 45, 20, 35]
    f = fig(ctx_bar(cn, cats, vals, 5))
    lst = lambda vs: ", ".join(str(v) for v in vs)
    sw = vals[:]
    sw[1], sw[2] = sw[2], sw[1]
    its.append(mcq(f + "Which list matches this bar graph? The numbers are in this order: %s."
                   % ", ".join(cats), lst(vals), [lst([v // 5 for v in vals]), lst(sw), lst([v + 5 for v in vals])],
                   "The scale counts by 5s. " + " ".join(read_bar(c, v, 5) for c, v in zip(cats, vals)) +
                   " Counting grid spaces instead of reading the scale gives %s." % lst([v // 5 for v in vals])))
    assert len(its) == 20, len(its)
    return {"title": "Bar graphs with scales of 2 and 5", "items": its}


# ------------------------------------------------------------ set 5: mode and conclusions
def set_words(rnd):
    its = []
    S = STU
    sp_c = ["Hockey", "Skating", "Skiing", "Sledding", "Ringette"]
    sp_v = [12, 9, 6, 10, 5]
    sport = fig(bar_svg("Favourite winter sport", "Sport", "Students", sp_c, sp_v, 2,
                        label="bar graph: favourite winter sport of the grade 3 classes",
                        source="Source: vote of the Grade 3 classes"))
    its.append(mcq(sport + "What is the mode of this data?", "Hockey", ["12", "Ringette", "Sledding"],
                   "The mode is the answer that was chosen most often. The tallest bar is Hockey, so the mode is hockey. "
                   "12 is how many students chose hockey. It is not the mode."))
    its.append(mcq(sport + "How many students chose hockey or skating?", fmt(21, S), [fmt(x, S) for x in [3, 20, 22]],
                   "The scale counts by 2s. Hockey ends on 12. Skating ends halfway between 8 and 10, so 9. "
                   "Hockey or skating means add: 12 + 9 = 21. (Reading skating as 8 gives 20.)"))
    its.append(mcq(sport + "How many more students chose sledding than skiing?", fmt(4, S), [fmt(x, S) for x in [16, 2, 6]],
                   "Sledding 10, skiing 6. How many more means subtract: 10 − 6 = 4. "
                   "(16 is the sum, and 2 counts the grid spaces between the bars.)"))
    tot = sum(sp_v)
    its.append(mcq(sport + "Every Grade 3 student voted once. How many students voted?", fmt(tot, S),
                   [fmt(x, S) for x in [40, 44, 5]],
                   "Read every bar: 12, 9, 6, 10 and 5. Skating and ringette end between gridlines, so they are 9 and 5. "
                   "12 + 9 + 6 + 10 + 5 = %d. (Reading 9 and 5 as 8 and 4 gives 40.)" % tot))
    its.append(mcq(sport + "Which statement is true?", "Sledding got 1 more vote than skating.",
                   ["Skiing got more votes than skating.", "Ringette was the most popular sport.",
                    "Hockey got twice as many votes as sledding."],
                   "Sledding 10 and skating 9: 10 − 9 = 1, so this is true. Skiing (6) is less than skating (9). "
                   "Ringette (5) is the least popular. Twice sledding would be 20, not 12."))
    its.append(mcq(sport + "The gym teacher will plan activities for the two most popular sports. Which two?",
                   "Hockey and sledding", ["Hockey and skating", "Skating and sledding", "Skiing and ringette"],
                   "The two tallest bars are hockey (12) and sledding (10). Skating is 9, just below sledding."))
    # travel pictograph, key 5
    tr_c = ["Walk", "Car", "Bus", "Bike"]
    tr_v = [35, 25, 40, 10]
    trv = fig(part_svg(pic_part("How we get to school", tr_c, tr_v, 5, "square", S, source="Source: school survey"),
                       "pictograph: how we get to school"))
    its.append(mcq(trv + "Which way to get to school is the mode?", "Bus", ["40", "8", "Walk"],
                   "The mode is the most common answer. The Bus row has the most squares (8 squares × 5 = 40 students), "
                   "so the mode is bus. 40 and 8 are numbers of students and squares, not the mode."))
    its.append(mcq(trv + "How many students take the bus or come by car?", fmt(65, S), [fmt(x, S) for x in [13, 15, 70]],
                   "Each square = 5 students. Bus: 8 × 5 = 40. Car: 5 × 5 = 25. 40 + 25 = 65. "
                   "(13 counts the squares, as if each square were 1.)"))
    its.append(mcq(trv + "How many more students take the bus than walk?", fmt(5, S), [fmt(x, S) for x in [1, 75, 10]],
                   "Bus: 8 squares = 40. Walk: 7 squares = 35. 40 − 35 = 5. (1 is the difference in squares.)"))
    its.append(mcq(trv + "The school wants fewer cars at drop-off. If 10 of the car students start to walk, "
                   "how many students will walk?", fmt(45, S), [fmt(x, S) for x in [15, 35, 17]],
                   "Walk now: 7 squares × 5 = 35. 10 more students will walk: 35 + 10 = 45. "
                   "(17 is 7 squares + 10, which reads each square as 1.)"))
    # mode from lists
    its.append(mcq("Kai wrote down how many goals he scored in his last 7 hockey games: 2, 3, 1, 3, 5, 3, 2. "
                   "What is the mode?", 3, [5, 7, 2],
                   "The mode is the number that appears most often. 3 appears three times, 2 appears twice, "
                   "and 1 and 5 appear once. The mode is 3. (5 is the biggest number, not the mode.)"))
    its.append(mcq("At drop-off, Zoe counted the people in each car: 2, 4, 1, 2, 3, 2, 5, 2. What is the mode?", 2,
                   [5, 4, 8],
                   "2 appears four times, more than any other number, so the mode is 2. "
                   "(5 is the biggest number, and 4 is how many times 2 appears.)"))
    its.append(mcq("Which set of data has a mode of 4?", "4, 6, 4, 2, 4",
                   ["2, 4, 6, 6, 3", "1, 4, 3, 1, 5", "9, 8, 4, 8, 7"],
                   "In 4, 6, 4, 2, 4 the number 4 appears three times, so the mode is 4. "
                   "The other modes are 6 (in 2, 4, 6, 6, 3), 1 (in 1, 4, 3, 1, 5) and 8 (in 9, 8, 4, 8, 7)."))
    # Thanksgiving dessert table
    ds_c = ["Pumpkin pie", "Apple pie", "Butter tarts", "Ice cream"]
    ds_v = [11, 8, 6, 4]
    ds = fig(freq_svg("Favourite Thanksgiving dessert", "Dessert", ds_c, ds_v, "frequency table: favourite thanksgiving dessert",
                      tally=False))
    its.append(mcq(ds + "What is the mode of this data?", "Pumpkin pie", ["11", "Ice cream", "Apple pie"],
                   "The mode is the dessert with the biggest frequency. Pumpkin pie has 11 votes, the most. "
                   "11 is the frequency, not the mode."))
    its.append(mcq(ds + "4 more students vote for apple pie. What is the mode now?", "Apple pie",
                   ["Pumpkin pie", "12", "Butter tarts"],
                   "Apple pie now has 8 + 4 = 12 votes. 12 is more than 11 (pumpkin pie), so apple pie is the new mode."))
    # Terry Fox Run money, scale 5
    tf = fig(bar_svg("Money raised for the Terry Fox Run", "Class", "Dollars", TEACH, [35, 50, 45, 20], 5,
                     label="bar graph: money raised for the terry fox run", source="Source: school office records"))
    its.append(mcq(tf + "How much money did the four classes raise altogether?", "$150", ["$30", "$145", "$50"],
                   "The scale counts by 5s. Ms. Lee $35, Mr. Khan $50, Mme Roy $45, Mr. Chen $20. "
                   "35 + 50 + 45 + 20 = 150. (30 counts the grid spaces: 7 + 10 + 9 + 4.)"))
    its.append(mcq(tf + "Next year, Mme Roy’s class wants to raise $60. How much more is that than this year?", "$15",
                   ["$20", "$105", "$25"],
                   "Mme Roy’s bar ends on 45. 60 − 45 = 15, so $15 more. (Reading the bar as 40 gives $20; "
                   "$105 adds instead of subtracting; $25 uses Ms. Lee’s bar, 35, by mistake.)"))
    # bird pictograph, key 2
    BD = ("bird", "birds")
    bd_c = ["Chickadee", "Blue jay", "Cardinal", "Sparrow", "Junco"]
    bd_v = [14, 5, 6, 9, 8]
    bd = fig(part_svg(pic_part("Birds at the school feeder", bd_c, bd_v, 2, "circle", BD, source="Source: our class bird count"),
                      "pictograph: birds at the school feeder"))
    its.append(mcq(bd + "How many more chickadees were seen than blue jays and cardinals together?", fmt(3, BD),
                   [fmt(x, BD) for x in [25, 9, 8]],
                   "Each circle = 2 birds, so half a circle = 1. Blue jay 2 × 2 + 1 = 5. Cardinal 3 × 2 = 6. "
                   "Step 1: 5 + 6 = 11. Step 2: chickadee 7 × 2 = 14, and 14 − 11 = 3."))
    t = sum(bd_v)
    its.append(mcq(bd + "How many birds were seen altogether?", fmt(t, BD), [fmt(x, BD) for x in [22, 40, 44]],
                   "Chickadee 14, blue jay 5, cardinal 6, sparrow 9, junco 8. 14 + 5 + 6 + 9 + 8 = %d. "
                   "(22 counts the circles. Leaving out the half circles gives 40.)" % t))
    its.append(mcq(sport + "Arjun says, “Hockey is the favourite winter sport of every Grade 3 student in Canada.” "
                   "Is he right?", "No. The data is from one school only.",
                   ["Yes. Hockey has the tallest bar.", "Yes. 12 students chose hockey.",
                    "No. Skating has the tallest bar."],
                   "The source says the data is from a vote of the Grade 3 classes at one school. It tells us about these "
                   "students, not every Grade 3 student in Canada. Even at this school, most students did not choose hockey: "
                   "12 out of 42."))
    assert len(its) == 20
    return {"title": "Mode and conclusions: word problems", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


def body_html():
    sp = ["Hockey", "Skating", "Skiing", "Sledding"]
    spv = [8, 5, 7, 4]
    return (
        "<h2>Sort, count, show, then explain</h2>"
        "<p>Data is information we collect, such as votes in a class survey. "
        "First we <b>sort</b> it. Then we <b>count</b> it with tally marks. "
        "Then we <b>show</b> it in a pictograph or a bar graph. "
        "Last, we say what the data tells us.</p>"
        "<h2>Venn and Carroll diagrams</h2>"
        "<p>A <b>Venn diagram</b> sorts things with circles. Things that fit both labels go in the <b>overlap</b>. "
        "Things that fit neither label go outside the circles. "
        "A <b>Carroll diagram</b> sorts things into boxes: each thing goes in the box for its row and its column.</p>"
        "<figure class='sn-fig'>" + venn_svg("Even", "More than 50", ["12", "36", "8"], ["64", "90"], ["71", "85"],
                                            ["27", "9"], "venn diagram: even numbers and numbers more than 50") +
        "<figcaption>64 and 90 are even and more than 50, so they go in the overlap.</figcaption></figure>" +
        ex("Example", "Where does 50 go?", "50 is even. 50 is not more than 50.", "Only in the Even circle") +
        "<h2>Tally marks and frequency tables</h2>"
        "<p>Draw one mark for each answer. The fifth mark goes across the other four. "
        "Count the groups by 5s, then add the single marks. The <b>frequency</b> is how many.</p>"
        "<figure class='sn-fig'>" + freq_svg("Favourite winter sport", "Sport", sp, spv,
                                            "frequency table: favourite winter sport") +
        "<figcaption>Hockey: 1 group of 5 and 3 more, so the frequency is 8.</figcaption></figure>" +
        "<h2>Pictographs</h2>"
        "<p>Look at the <b>key</b> first. In Grade 3, one symbol can stand for 2, 5 or 10. "
        "Count the symbols by 2s, 5s or 10s. Half a symbol stands for half of the key.</p>"
        "<figure class='sn-fig'>" + part_svg(pic_part("Favourite winter sport", sp, spv, 2, "circle", STU,
                                                      source="Source: Grade 3 class vote"),
                                             "pictograph: favourite winter sport") +
        "<figcaption>Each circle = 2 students. Skiing: 2, 4, 6, and half a circle is 1 more, so 7.</figcaption></figure>" +
        ex("Example", "How many students chose sledding?", "2 circles. Count by 2s: 2, 4.", "4 students") +
        "<h2>Bar graphs</h2>"
        "<p>A good bar graph has a <b>title</b>, <b>labels</b>, a <b>scale</b> and a <b>source</b> "
        "(where the data came from). Find what the scale counts by: 2s or 5s. "
        "If a bar ends halfway between two lines, the number is halfway between them.</p>"
        "<figure class='sn-fig'>" + bar_svg("Favourite winter sport", "Sport", "Students", sp, spv, 2,
                                            label="bar graph: favourite winter sport", source="Source: Grade 3 class vote") +
        "<figcaption>The scale counts by 2s. Skating ends halfway between 4 and 6, so 5 students chose skating.</figcaption></figure>" +
        ex("Example", "How many more students chose hockey than skating?", "Hockey 8, skating 5. 8 − 5 = 3.", "3 more students") +
        "<h2>The mode</h2>"
        "<p>The <b>mode</b> is the answer that appears most often. In a graph, it is the tallest bar or the longest row. "
        "In the graphs above, the mode is hockey.</p>" +
        ex("Example", "Goals in 6 games: 1, 3, 2, 3, 4, 3. What is the mode?", "3 appears three times. No other number appears that often.",
           "3") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Reading each symbol as 1 (4 circles = 4)", "Use the key: 4 circles of 2 = 8"],
            ["Saying half a symbol = 1 for every key", "Half a symbol is half of the key: half of 10 is 5"],
            ["Reading a bar between lines as the lower line", "Halfway between 6 and 8 is 7"],
            ["Counting grid spaces instead of reading the scale", "Read the number on the scale"],
            ["Giving the biggest number as the mode", "The mode is the answer that appears most often"],
            ["Counting the overlap of a Venn diagram twice", "Count each thing once"],
        ])
    )


FAQ = [
    {"q": "What do Grade 3 students learn about data in the Ontario math curriculum?",
     "a": "They sort data in Venn and Carroll diagrams, organize it in frequency tables, show it in pictographs and bar graphs with a scale, find the mode, and explain what the data tells them."},
    {"q": "What is the mode in Grade 3 math?",
     "a": "The mode is the value or answer that appears most often in a set of data. In 2, 3, 3, 5 the mode is 3; in a bar graph it is the category with the tallest bar."},
    {"q": "What is the difference between a Venn diagram and a Carroll diagram?",
     "a": "A Venn diagram sorts things with overlapping circles, and things that fit both rules go in the overlap. A Carroll diagram sorts things into a grid of boxes, with one rule for the rows and one for the columns."},
    {"q": "Is data on the Grade 3 EQAO math assessment?",
     "a": "Yes. The Grade 3 EQAO math assessment covers the strands of the Ontario curriculum, including Data, so students may read tables, pictographs and bar graphs and answer questions about them."},
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
    rnd = random.Random(33816)
    PK = Picker(rnd)
    sets = [set_sort(rnd), set_tally(rnd), set_pictograph(rnd, PK), set_bar(rnd, PK), set_words(rnd)]
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
        "country": "ca-on", "subject": "math", "grade": "grade-3", "slug": "data-and-graphs", "sort": 16,
        "updated": UPDATED, "pdf_url": "",
        "title": "Data and Graphs: Venn Diagrams, Pictographs, Bar Graphs and the Mode",
        "seo_title": "Grade 3 Data and Graphs Worksheets: Pictographs, Bar Graphs and Mode (Free, Answer Key, Ontario)",
        "short_title": "Data and graphs",
        "domain": "Data",
        "standard_code": "Grade 3: D1.3",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Display sets of data, using many-to-one correspondence, in pictographs and bar graphs with proper sources, titles, and labels, and appropriate scales",
        "meta_desc": "Free Grade 3 math worksheets on data and graphs for the Ontario curriculum: Venn and Carroll diagrams, tally marks and frequency tables, pictographs with a key of 2, 5 or 10, bar graphs with scales of 2 and 5, and the mode. 100 EQAO-style questions with an answer key.",
        "key_big": "Read the key or the scale first. Then read every row or bar.",
        "key_sub": "If one symbol = 10, half a symbol = 5. A bar halfway between 6 and 8 shows 7. The mode is the answer that appears most often, not the biggest number. In a Venn diagram, count the overlap once.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


def mark_large(u, pattern):
    """Tag pictures that must print larger (graphs, tables, diagrams, A to D panels) so their labels stay readable."""
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
        mark_large(u, "(pictograph|bar graph|frequency table|four sets|venn|carroll)")
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
