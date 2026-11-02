# -*- coding: utf-8 -*-
"""
AU Year 2 Maths: Data, tables and graphs (Australian Curriculum v9.0: AC9M2ST01, AC9M2ST02)
  python3 tools/gen_au_maths_y2_data.py
Sorting objects into groups (by colour, shape or size), tally marks and simple tables, picture graphs where
one picture stands for one thing, column graphs with a scale of 1, and comparing displays of the same data
(most, least, how many more, altogether). Numbers stay small (each group 20 or less).
Wrong answers come from real student mistakes: counting a tally group of 5 as 4 (missing the fifth mark),
counting by the wrong attribute (colour instead of shape), reading the wrong row or column, counting
grid spaces from 1, adding when the question asks “how many more” and subtracting when it asks “altogether”.
HTML attributes use single quotes (no backslashes in the JSON). Australian English.
"""
import json, re, math, os, random

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "au", "maths", "year-2")
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
COLS = {"red": "#d7263d", "blue": "#2b59c3", "yellow": "#f4c430", "green": "#3aa655"}


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e):
    """4 choices: correct + 3 unique distractors from real mistakes (no zero or negative numbers).
    Positions are balanced later for the whole set."""
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


def plus(vals):
    return " + ".join(str(v) for v in vals)


def count_list(n):
    return ", ".join(str(k) for k in range(1, n + 1))


# ------------------------------------------------------------ shapes for sorting
def star_pts(cx, cy, R=9.5, r=4.0):
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rad = R if i % 2 == 0 else r
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    return pts


def obj(o, cx, cy):
    """o = (kind, colour, big). Drawn with a dark outline so it still reads in black and white."""
    kind, col, big = o
    r = 13.5 if big else 8
    f = COLS[col]
    st = " stroke='%s' stroke-width='1.3'" % INK
    if kind == "circle":
        return "<circle cx='%.1f' cy='%.1f' r='%.1f' fill='%s'%s/>" % (cx, cy, r, f, st)
    if kind == "square":
        a = r * 0.88
        return "<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' fill='%s'%s/>" % (cx - a, cy - a, 2 * a, 2 * a, f, st)
    if kind == "triangle":
        pts = [(cx, cy - r * 1.05), (cx - r * 1.12, cy + r * 0.85), (cx + r * 1.12, cy + r * 0.85)]
    else:
        pts = star_pts(cx, cy, R=r * 1.15, r=r * 0.5)
    return "<polygon points='%s' fill='%s'%s/>" % (" ".join("%.1f,%.1f" % p for p in pts), f, st)


PL = {"circle": "circles", "square": "squares", "triangle": "triangles", "star": "stars"}
CELL = 40


def scatter_part(items, rnd, cols=6):
    """Objects on a loose grid (a little jitter), in a random order."""
    n = len(items)
    rows = int(math.ceil(n / cols))
    cells = [(c, r) for r in range(rows) for c in range(cols)]
    rnd.shuffle(cells)
    s = ["<rect x='1' y='1' width='%d' height='%d' rx='8' fill='#ffffff' stroke='%s' stroke-width='1.5'/>"
         % (cols * CELL + 10, rows * CELL + 10, GRID)]
    for o, (c, r) in zip(items, cells):
        cx = 6 + c * CELL + CELL / 2 + rnd.randint(-3, 3)
        cy = 6 + r * CELL + CELL / 2 + rnd.randint(-3, 3)
        s.append(obj(o, cx, cy))
    return (cols * CELL + 12, rows * CELL + 12, "".join(s))


def scatter_svg(items, rnd, cols=6):
    return part_svg(scatter_part(items, rnd, cols), "shapes to sort")


def loops_svg(groups, labels, letters=None, per_row=3):
    """Sorting loops side by side. letters = {(group, index): 'A'} writes a letter under that object."""
    ch = 52 if letters else CELL
    s = []
    x = 0
    H = 0
    for g, (items, lab) in enumerate(zip(groups, labels)):
        rows = int(math.ceil(len(items) / per_row))
        w = per_row * CELL + 20
        w = max(w, tw(lab, 15, True) + 20)
        h = rows * ch + 20
        s.append(text(x + w / 2, 18, lab, 15, bold=True))
        s.append("<rect x='%.1f' y='28' width='%.1f' height='%.1f' rx='18' fill='%s' stroke='%s' stroke-width='2'/>"
                 % (x + 1, w - 2, h, FILL2, GREEN))
        x0 = x + (w - per_row * CELL) / 2
        for k, o in enumerate(items):
            cx = x0 + (k % per_row) * CELL + CELL / 2
            cy = 28 + 10 + (k // per_row) * ch + 20
            s.append(obj(o, cx, cy))
            if letters and (g, k) in letters:
                s.append(text(cx, cy + 32, letters[(g, k)], 15, bold=True, col=RED))
        H = max(H, 28 + h + 2)
        x += w + 16
    return svg_wrap(x - 16, H, "".join(s), "shapes sorted into groups")


def cnt(items, kind=None, col=None, big=None):
    return sum(1 for o in items if (kind is None or o[0] == kind) and (col is None or o[1] == col)
               and (big is None or o[2] == big))


# ------------------------------------------------------------ data contexts
class Ctx:
    def __init__(self, title, axis, cats, unit, ask, more, fewer, both, total, ph=None, ordered=False, maxv=None):
        self.title, self.axis, self.cats, self.unit = title, axis, cats, unit
        self.ask_f, self.more_f, self.fewer_f, self.both_f, self.total = ask, more, fewer, both, total
        self.ph, self.ordered, self.maxv = ph or {}, ordered, maxv

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
        "How many students voted altogether?",
        ph={"AFL": "AFL", "Cricket": "cricket", "Netball": "netball", "Soccer": "soccer", "Swimming": "swimming"}),
    Ctx("Favourite fruit", "Fruit", ["Apple", "Banana", "Mango", "Orange", "Grapes"], VOTE,
        "How many votes did {a} get?", "How many more votes did {a} get than {b}?",
        "How many fewer votes did {a} get than {b}?", "How many votes did {a} and {b} get altogether?",
        "How many votes were there altogether?"),
    Ctx("Favourite Australian animal", "Animal", ["Koala", "Kangaroo", "Wombat", "Emu", "Echidna"], VOTE,
        "How many votes did the {a} get?", "How many more votes did the {a} get than the {b}?",
        "How many fewer votes did the {a} get than the {b}?", "How many votes did the {a} and the {b} get altogether?",
        "How many votes were there altogether?", ph=LOWER(["Koala", "Kangaroo", "Wombat", "Emu", "Echidna"])),
    Ctx("How we get to school", "Way", ["Walk", "Car", "Bus", "Bike"], STU,
        "How many students {a} to school?", "How many more students {a} to school than {b}?",
        "How many fewer students {a} to school than {b}?", "How many students {a} or {b} to school?",
        "How many students are in the survey altogether?",
        ph={"Walk": "walk", "Car": "come by car", "Bus": "come by bus", "Bike": "ride a bike"}),
    Ctx("Birds in the schoolyard", "Bird", ["Magpie", "Galah", "Lorikeet", "Ibis"], ("bird", "birds"),
        "How many {a} did the class see?", "How many more {a} than {b} did the class see?",
        "How many fewer {a} than {b} did the class see?", "How many {a} and {b} did the class see altogether?",
        "How many birds did the class see altogether?",
        ph={"Magpie": "magpies", "Galah": "galahs", "Lorikeet": "lorikeets", "Ibis": "ibises"}),
    Ctx("Ice blocks sold at the canteen", "Day", ["Mon", "Tue", "Wed", "Thu", "Fri"], ("ice block", "ice blocks"),
        "How many ice blocks were sold on {a}?", "How many more ice blocks were sold on {a} than on {b}?",
        "How many fewer ice blocks were sold on {a} than on {b}?", "How many ice blocks were sold on {a} and {b} altogether?",
        "How many ice blocks were sold altogether?", ordered=True,
        ph={"Mon": "Monday", "Tue": "Tuesday", "Wed": "Wednesday", "Thu": "Thursday", "Fri": "Friday"}),
    Ctx("Books read this week", "Student", ["Charlotte", "Oliver", "Isla", "Jack", "Mia"], ("book", "books"),
        "How many books did {a} read?", "How many more books did {a} read than {b}?",
        "How many fewer books did {a} read than {b}?", "How many books did {a} and {b} read altogether?",
        "How many books did they read altogether?"),
    Ctx("Pets in 2B", "Pet", ["Dog", "Cat", "Fish", "Bird", "Rabbit"], STU,
        "How many students have a {a}?", "How many more students have a {a} than a {b}?",
        "How many fewer students have a {a} than a {b}?", "How many students have a {a} or a {b}?",
        "How many students are shown altogether?", ph=LOWER(["Dog", "Cat", "Fish", "Bird", "Rabbit"])),
    Ctx("Favourite colour", "Colour", ["Red", "Blue", "Green", "Purple", "Pink"], VOTE,
        "How many votes did {a} get?", "How many more votes did {a} get than {b}?",
        "How many fewer votes did {a} get than {b}?", "How many votes did {a} and {b} get altogether?",
        "How many votes were there altogether?", ph=LOWER(["Red", "Blue", "Green", "Purple", "Pink"])),
    Ctx("Shells found at the beach", "Student", ["Ruby", "Kai", "Zara", "Leo", "Grace"], ("shell", "shells"),
        "How many shells did {a} find?", "How many more shells did {a} find than {b}?",
        "How many fewer shells did {a} find than {b}?", "How many shells did {a} and {b} find altogether?",
        "How many shells did they find altogether?"),
]
BYTITLE = {c.title: c for c in CTXS}


class Picker:
    """Hands out contexts in a shuffled cycle so neighbouring questions use different stories."""
    def __init__(self, rnd):
        self.rnd = rnd
        self.q = []
        self.last = None

    def next(self):
        if not self.q:
            fresh = CTXS[:]
            self.rnd.shuffle(fresh)
            if fresh[0] is self.last:
                fresh.append(fresh.pop(0))
            self.q = fresh
        self.last = self.q.pop(0)
        return self.last


def make_data(ctx, n, rnd, lo=2, hi=9, ok=lambda v: True):
    """n different values from lo to hi."""
    if ctx.ordered:
        start = rnd.randint(0, len(ctx.cats) - n)
        cats = ctx.cats[start:start + n]
    else:
        cats = rnd.sample(ctx.cats, n)
    for _ in range(5000):
        vals = rnd.sample(range(lo, hi + 1), n)
        if ok(vals):
            return cats, vals
    raise ValueError("no data for " + ctx.title)


# ------------------------------------------------------------ picture graph (one picture for each)
def symbol(kind, cx, cy, col=GREEN):
    if kind == "circle":
        return "<circle cx='%.1f' cy='%.1f' r='8.5' fill='%s'/>" % (cx, cy, col)
    if kind == "square":
        return "<rect x='%.1f' y='%.1f' width='15' height='15' rx='2' fill='%s'/>" % (cx - 7.5, cy - 7.5, col)
    return "<polygon points='%s' fill='%s'/>" % (" ".join("%.1f,%.1f" % p for p in star_pts(cx, cy)), col)


SYMS = ["circle", "star", "square"]


def pic_part(title, cats, vals, sym, unit, missing=None, minsym=4):
    """Picture graph: one row per category, one symbol for each thing, key at the bottom."""
    fs, rh, gap = 15, 26, 23
    lw = max(tw(c, fs) for c in cats) + 22
    m = max(max(vals), minsym)
    W = lw + 12 + m * gap + 14
    keytxt = "= " + fmt(1, unit)
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
        for j in range(v):
            s.append(symbol(sym, lw + 12 + j * gap + 9, y + rh / 2))
    ky = top + H_tab + 22
    x = (W - kw) / 2
    s.append(text(x, ky, "Key:", fs, anchor="start", bold=True))
    x += tw("Key:", fs, True) + 16
    s.append(symbol(sym, x, ky - 5))
    s.append(text(x + 14, ky, keytxt, fs, anchor="start"))
    return (W, ky + 8, "".join(s))


def ctx_pic(ctx, cats, vals, sym):
    return part_svg(pic_part(ctx.title, cats, vals, sym, ctx.unit), "picture graph: " + ctx.title.lower())


# ------------------------------------------------------------ column graph (scale of 1)
def bar_part(title, cat_axis, val_axis, cats, vals, missing=None, top_v=None, col=BAR):
    fs = 14
    top_v = top_v or max(max(vals) + 1, 5)
    nt = top_v
    assert 4 <= nt <= 12, (title, vals)
    s = []
    gy = 16 if nt > 8 else 19
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
        s.append(text(x0 - 5, y + 5, k, fs, anchor="end"))
    for i, (c, v) in enumerate(zip(cats, vals)):
        cx = x0 + slot * i + slot / 2
        bw = min(30, slot * 0.62)
        if i == missing:
            s.append(text(cx, yb - 6, "?", 18, bold=True, col=RED))
        else:
            h = v * gy
            s.append("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' fill='%s'/>" % (cx - bw / 2, yb - h, bw, h, col))
        s.append(text(cx, yb + 17, c, fs))
    s.append("<path d='M%d %d V%d H%d' fill='none' stroke='%s' stroke-width='2'/>" % (x0, y0 - 6, yb, x0 + pw, INK))
    s.append(text(x0 + pw / 2, yb + 36, cat_axis, fs, bold=True))
    mid = y0 + ph / 2
    s.append(text(13, mid, val_axis, fs, bold=True, extra=" transform='rotate(-90 13 %.1f)'" % mid))
    assert tw(val_axis, fs, True) < ph + 26, (val_axis, ph)
    return (W, yb + 42, "".join(s))


def bar_svg(title, cat_axis, val_axis, cats, vals, missing=None, label="column graph"):
    return part_svg(bar_part(title, cat_axis, val_axis, cats, vals, missing), label)


def ctx_bar(ctx, cats, vals, missing=None):
    return bar_svg(ctx.title, ctx.axis, ctx.unit[1].capitalize(), cats, vals, missing,
                   label="column graph: " + ctx.title.lower())


# ------------------------------------------------------------ tally marks and tables
def tally_marks(x, cy, v):
    """Groups of five: four upright lines and the fifth line across."""
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


def table_part(title, head, cats, vals, tally=True, num=True, missing=None, numhead="Number", total=False):
    """Table: category | tally | number. `missing` = row whose number is a red ?."""
    fs, rh = 15, 28
    c1 = int(max(max(tw(c, fs) for c in cats + (["Total"] if total else [])), tw(head, fs, True)) + 20)
    cols = [c1]
    if tally:
        cols.append(int(max(max(tally_width(v) for v in vals) + 24, 70)))
    if num:
        cols.append(int(tw(numhead, fs, True) + 22))
    top = 28 if title else 2
    tot = sum(cols)
    W = int(max(tot + 8, tw(title, 16, True) + 16 if title else 0))
    x0 = (W - tot) / 2
    s = [text(W / 2, 19, title, 16, bold=True)] if title else []
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
            name = "num" if (k == 2 or (k == 1 and not tally)) else ("tally" if k == 1 else "cat")
            if name == "cat":
                s.append(text(x + 10, y + 19, c, fs, anchor="start", bold=hd or c == "Total"))
            elif hd:
                s.append(text(x + 10 if name == "tally" else x + cw / 2, y + 19, "Tally" if name == "tally" else numhead,
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
    return (W, top + len(rows) * rh + 4, "".join(s))


def table_svg(title, head, cats, vals, label, **kw):
    return part_svg(table_part(title, head, cats, vals, **kw), label)


def tally_text(v):
    g, r = v // 5, v % 5
    if g and r:
        return "%s of 5 and %d more. Count %s, then %s. So it is %d." % (
            ones(g, "group"), r, ", ".join(str(5 * k) for k in range(1, g + 1)),
            ", ".join(str(5 * g + k) for k in range(1, r + 1)), v)
    if g:
        return "%s of 5. Count %s. So it is %d." % (ones(g, "group"), ", ".join(str(5 * k) for k in range(1, g + 1)), v)
    return "%s. So it is %d." % (ones(r, "single mark"), v)


def tally_cands(v):
    g, r = v // 5, v % 5
    return [g * 4 + r, v + 1, v - 1, g + r, v + 5, g * 6 + r]


# ------------------------------------------------------------ set 1: sort objects into groups
KINDS = ["circle", "triangle", "square", "star"]


def rand_items(rnd, n, kinds, cols, sizes=(True, False), ok=lambda it: True):
    for _ in range(20000):
        it = [(rnd.choice(kinds), rnd.choice(cols), rnd.choice(sizes)) for _ in range(n)]
        if ok(it):
            return it
    raise ValueError("items")


def set_sort(rnd):
    its = []
    # 1 How many triangles?
    A = rand_items(rnd, 11, ["circle", "triangle", "square"], ["red", "blue"],
                   ok=lambda it: len({cnt(it, kind=k) for k in ("circle", "triangle", "square")}) == 3
                   and cnt(it, kind="triangle") >= 3 and len({cnt(it, col="red"), cnt(it, col="blue"),
                                                              cnt(it, kind="triangle")}) == 3
                   and cnt(it, kind="triangle", col="red") not in (0, cnt(it, kind="triangle"))
                   and cnt(it, kind="triangle", col="blue") > 0)
    fA = fig(scatter_svg(A, rnd))
    t = cnt(A, kind="triangle")
    its.append(mcq(fA + "How many triangles are there?", t,
                   [cnt(A, kind="circle"), cnt(A, kind="square"), len(A), t + 1, t - 1],
                   "A triangle has 3 sides and 3 corners. Touch each triangle once and count: %s. "
                   "There are %d triangles. Count only triangles, not the other shapes." % (count_list(t), t)))
    # 2 How many red shapes? (same picture)
    rd = cnt(A, col="red")
    its.append(mcq(fA + "How many red shapes are there?", rd,
                   [cnt(A, col="blue"), cnt(A, kind="triangle", col="red"), len(A), rd + 1, rd - 1],
                   "Look at the colour only. Count every red shape, whatever its shape: %s. "
                   "There are %d red shapes." % (count_list(rd), rd)))
    # 3 How many blue triangles? (same picture)
    bt = cnt(A, kind="triangle", col="blue")
    its.append(mcq(fA + "How many <b>blue triangles</b> are there?", bt,
                   [cnt(A, col="blue"), t, cnt(A, kind="triangle", col="red"), bt + 1, bt + 2],
                   "The shape must be a triangle <b>and</b> it must be blue. There are %d triangles, "
                   "but only %d of them are blue." % (t, bt)))
    # 4 big shapes
    B = rand_items(rnd, 12, ["circle", "square", "star"], ["yellow", "green"],
                   ok=lambda it: 3 <= cnt(it, big=True) <= 7 and len({cnt(it, big=True), cnt(it, big=False),
                                                                      cnt(it, col="yellow"), cnt(it, col="green")}) == 4
                   and len({cnt(it, kind=k) for k in ("circle", "square", "star")}) == 3
                   and min(cnt(it, kind=k) for k in ("circle", "square", "star")) >= 2)
    fB = fig(scatter_svg(B, rnd))
    bg = cnt(B, big=True)
    its.append(mcq(fB + "How many <b>big</b> shapes are there?", bg,
                   [cnt(B, big=False), len(B), cnt(B, col="yellow"), bg + 1, bg - 1],
                   "Look at the size only. Count the big shapes: %s. There are %d big shapes. "
                   "(%d shapes are small.)" % (count_list(bg), bg, cnt(B, big=False))))
    # 5 which shape has the most (same picture)
    kc = {k: cnt(B, kind=k) for k in ("circle", "square", "star")}
    mk = max(kc, key=kc.get)
    its.append(mcq(fB + "Sort the shapes by shape. Which group has the most?", PL[mk].capitalize(),
                   [PL[k].capitalize() for k in kc if k != mk] + ["Triangles"],
                   "Count each group: circles %d, squares %d, stars %d. The biggest number is %d, so %s is the "
                   "biggest group." % (kc["circle"], kc["square"], kc["star"], kc[mk], PL[mk])))
    # 6 shapes that are not yellow (same picture)
    ny = len(B) - cnt(B, col="yellow")
    its.append(mcq(fB + "How many shapes are <b>not</b> yellow?", ny,
                   [cnt(B, col="yellow"), len(B), ny + 1, ny - 1],
                   "Not yellow means every other colour. Here that is the green shapes: %s. "
                   "Check: %d shapes − %d yellow = %d." % (count_list(ny), len(B), cnt(B, col="yellow"), ny)))
    # 7 how many groups by colour / by shape
    C = rand_items(rnd, 10, ["circle", "triangle", "square", "star"], ["red", "blue", "yellow"], sizes=(True,),
                   ok=lambda it: len({o[0] for o in it}) == 4 and len({o[1] for o in it}) == 3)
    fC = fig(scatter_svg(C, rnd, cols=5))
    its.append(mcq(fC + "Mia sorts these shapes by <b>colour</b>. How many groups will she make?", 3,
                   [4, len(C), 2, 5],
                   "Mia makes one group for each colour: red, blue and yellow. That is 3 groups. "
                   "(4 groups would be sorting by shape: circles, triangles, squares and stars.)"))
    its.append(mcq(fC + "Noah sorts the same shapes by <b>shape</b>. How many groups will he make?", 4,
                   [3, len(C), 5, 2],
                   "Noah makes one group for each kind of shape: circles, triangles, squares and stars. "
                   "That is 4 groups. (3 groups would be sorting by colour.)"))
    # 9-11 how were they sorted?
    rules = [("colour", "By colour"), ("shape", "By shape"), ("size", "By size")]
    choice_all = ["By colour", "By shape", "By size", "They are not sorted"]
    for rule, ans in [rules[1], rules[0], rules[2]]:
        for _ in range(5000):
            if rule == "colour":
                gs = [[(rnd.choice(["circle", "square", "triangle"]), c, rnd.choice([True, False])) for _ in range(5)]
                      for c in ("red", "blue")]
            elif rule == "shape":
                gs = [[(k, rnd.choice(["red", "blue", "yellow"]), rnd.choice([True, False])) for _ in range(5)]
                      for k in ("circle", "star", "square")]
                gs = [g[:4] for g in gs]
            else:
                gs = [[(rnd.choice(["circle", "square", "triangle", "star"]), rnd.choice(["red", "blue", "green"]), b)
                       for _ in range(5)] for b in (True, False)]
            # every other attribute must be mixed inside every group
            okg = True
            for g in gs:
                if rule != "colour" and len({o[1] for o in g}) < 2:
                    okg = False
                if rule != "shape" and len({o[0] for o in g}) < 2:
                    okg = False
                if rule != "size" and len({o[2] for o in g}) < 2:
                    okg = False
            if okg:
                break
        labels = ["Group %d" % (k + 1) for k in range(len(gs))]
        f = fig(loops_svg(gs, labels))
        if rule == "colour":
            e = ("Group 1 has only red shapes. Group 2 has only blue shapes. The shapes and the sizes are mixed. "
                 "So they are sorted by colour.")
        elif rule == "shape":
            e = ("Group 1 has only circles, Group 2 only stars and Group 3 only squares. The colours and sizes are "
                 "mixed. So they are sorted by shape.")
        else:
            e = ("Group 1 has only big shapes. Group 2 has only small shapes. The shapes and colours are mixed. "
                 "So they are sorted by size.")
        its.append(mcq(f + "How were these shapes sorted?", ans, [c for c in choice_all if c != ans], e))
    # 12-14 which shape is in the wrong group? (letters A to D)
    WG = [
        ("Circles", "Not circles", lambda o: o[0] == "circle", "circle"),
        ("Red", "Blue", lambda o: o[1] == "red", "red"),
        ("Big", "Small", lambda o: o[2], "big"),
    ]
    for gi, (l1, l2, in1, word) in enumerate(WG):
        pos = [2, 0, 3][gi]
        for _ in range(5000):
            if gi == 0:
                g1 = [("circle", rnd.choice(["red", "blue", "yellow"]), rnd.choice([True, False])) for _ in range(5)]
                g2 = [(rnd.choice(["square", "triangle", "star"]), rnd.choice(["red", "blue", "yellow"]),
                       rnd.choice([True, False])) for _ in range(5)]
            elif gi == 1:
                g1 = [(rnd.choice(KINDS), "red", rnd.choice([True, False])) for _ in range(5)]
                g2 = [(rnd.choice(KINDS), "blue", rnd.choice([True, False])) for _ in range(5)]
            else:
                g1 = [(rnd.choice(KINDS), rnd.choice(["red", "blue", "green"]), True) for _ in range(5)]
                g2 = [(rnd.choice(KINDS), rnd.choice(["red", "blue", "green"]), False) for _ in range(5)]
            if len({o[0] for o in g1 + g2}) >= 3 and len({o[1] for o in g1 + g2}) >= 2:
                break
        # put one wrong object in: an object that belongs in the other group
        letters = {}
        order = [(0, 1), (0, 3), (1, 0), (1, 2)]
        wslot = order[pos]
        gg = [g1, g2]
        donor = g2 if wslot[0] == 0 else g1
        gg[wslot[0]][wslot[1]] = donor[4]
        for k, sl in enumerate(order):
            letters[sl] = "ABCD"[k]
        f = fig(loops_svg(gg, [l1, l2], letters))
        mv = gg[wslot[0]][wslot[1]]
        desc = {"circle": "circle", "square": "square", "triangle": "triangle", "star": "star"}[mv[0]]
        if gi == 0:
            why = "Shape %s is a %s, not a circle. It belongs in Not circles." % ("ABCD"[pos], desc) if wslot[0] == 0 else \
                  "Shape %s is a circle. It belongs in the Circles group." % "ABCD"[pos]
        elif gi == 1:
            why = "Shape %s is %s. It belongs in the %s group." % ("ABCD"[pos], mv[1], mv[1].capitalize())
        else:
            why = "Shape %s is %s. It belongs in the %s group." % ("ABCD"[pos], "big" if mv[2] else "small",
                                                                    "Big" if mv[2] else "Small")
        its.append(mcq_fixed(f + "Which shape is in the wrong group?", ["A", "B", "C", "D"], pos,
                             "Read the label on each group. Check every lettered shape. " + why +
                             " The other lettered shapes are in the right group."))
    # 15-16 sort into a table, missing number
    D = rand_items(rnd, 13, ["circle", "triangle", "square"], ["red", "blue", "yellow"], sizes=(True,),
                   ok=lambda it: len({cnt(it, kind=k) for k in ("circle", "triangle", "square")}) == 3
                   and min(cnt(it, kind=k) for k in ("circle", "triangle", "square")) >= 2
                   and len({cnt(it, col=c) for c in ("red", "blue", "yellow")}) == 3
                   and min(cnt(it, col=c) for c in ("red", "blue", "yellow")) >= 2)
    sc = scatter_part(D, rnd, cols=5)
    kc = [cnt(D, kind=k) for k in ("circle", "triangle", "square")]
    tb = table_part("", "Shape", ["Circles", "Triangles", "Squares"], kc, tally=False, missing=1)
    f = fig(side_by_side([sc, tb], "shapes and a table sorted by shape"))
    its.append(mcq(f + "Charlotte sorts the shapes by shape. What number goes in the table for triangles?", kc[1],
                   [cnt(D, col="red"), cnt(D, col="blue"), kc[1] + 1, kc[1] - 1, len(D) - kc[0] - kc[2] + 1],
                   "Count the triangles of every colour: %s. So %d goes in the table. "
                   "Check: %d + %d + %d = %d shapes." % (count_list(kc[1]), kc[1], kc[0], kc[1], kc[2], len(D))))
    cc = [cnt(D, col=c) for c in ("red", "blue", "yellow")]
    tb = table_part("", "Colour", ["Red", "Blue", "Yellow"], cc, tally=False, missing=2)
    f = fig(side_by_side([scatter_part(D, rnd, cols=5), tb], "shapes and a table sorted by colour"))
    its.append(mcq(f + "Then Charlotte sorts the same shapes by colour. What number goes in the table for yellow?", cc[2],
                   [kc[2], cc[2] + 1, cc[2] - 1, len(D) - cc[0], cc[0]],
                   "Count every yellow shape: %s. So %d goes in the table. "
                   "Check: %d + %d + %d = %d shapes, the same as before." % (count_list(cc[2]), cc[2], cc[0], cc[1], cc[2], len(D))))
    # 17-20 word problems
    E = rand_items(rnd, 12, ["circle", "triangle", "square", "star"], ["red", "blue"], sizes=(True,),
                   ok=lambda it: 3 <= cnt(it, kind="circle") <= 5 and len({o[0] for o in it}) == 4
                   and cnt(it, kind="circle", col="red") > 0)
    nc = cnt(E, kind="circle")
    f = fig(scatter_svg(E, rnd))
    its.append(mcq(f + "Kai sorts these shapes into two groups: shapes with corners and shapes with no corners. "
                   "How many shapes have no corners?", nc,
                   [len(E) - nc, cnt(E, kind="circle", col="red"), len(E), nc + 1],
                   "Only circles have no corners. Count the circles: %s. So %d shapes have no corners. "
                   "The other %d shapes have corners." % (count_list(nc), nc, len(E) - nc)))
    its.append(mcq("Oliver has 16 toy cars. He sorts them into red cars and cars that are not red. "
                   "7 cars are red. How many cars are not red?", "9 cars", ["23 cars", "7 cars", "8 cars"],
                   "All the cars are in one group or the other. 16 − 7 = 9 cars are not red. "
                   "(Adding gives 23, but there are only 16 cars.)"))
    its.append(mcq("Ava sorts her shells into big shells and small shells. She has 6 big shells and 8 small shells. "
                   "How many shells does she have altogether?", "14 shells", ["2 shells", "13 shells", "8 shells"],
                   "Altogether means add the two groups: 6 + 8 = 14 shells. "
                   "(2 is how many more small shells than big shells.)"))
    its.append(mcq("Lunch boxes in 2C have 20 items. 8 are fruit, 5 are sandwiches and the rest are snacks. "
                   "How many snacks are there?", "7 snacks", ["13 snacks", "12 snacks", "33 snacks"],
                   "Step 1: fruit and sandwiches: 8 + 5 = 13. Step 2: 20 − 13 = 7 snacks. "
                   "(13 is the fruit and sandwiches, not the snacks.)"))
    assert len(its) == 20, len(its)
    return {"title": "Sort objects into groups", "items": its}


# ------------------------------------------------------------ set 2: tally marks and tables
def set_tally(rnd):
    its = []
    for v in (6, 9, 12, 17):
        its.append(mcq(fig(tally_only_svg(v)) + "What number do these tally marks show?", v, tally_cands(v),
                       "Four lines with one line across make a group of 5. " + tally_text(v)))
    # 5 which shows 12
    order = [17, 11, 12, 13]
    pos = order.index(12)
    s = []
    for k, v in enumerate(order):
        x0, y0 = (k % 2) * 170, (k // 2) * 44
        s.append(text(x0 + 8, y0 + 27, "ABCD"[k], 17, anchor="start", bold=True))
        s.append(tally_marks(x0 + 34, y0 + 21, v))
        assert x0 + 34 + tally_width(v) < x0 + 166
    svg = svg_wrap(340, 88, "".join(s), "four sets of tally marks")
    why = {17: "one group of 5 too many", 11: "one mark too few", 13: "one mark too many"}
    its.append(mcq_fixed(fig(svg) + "Which tally marks show 12?", ["A", "B", "C", "D"], pos,
                         "12 = 5 + 5 + 2. Look for 2 groups of 5 and 2 single marks. That is %s. " % "ABCD"[pos] +
                         "; ".join("%s shows %d (%s)" % ("ABCD"[k], v, why[v]) for k, v in enumerate(order) if v != 12) + "."))
    # 6 the fifth mark
    its.append(mcq(fig(tally_only_svg(4)) + "Zara has drawn 4 tally marks. How should she draw the 5th mark?",
                   "A line across the 4 marks",
                   ["A line next to the 4 marks", "A circle around the 4 marks", "A new row of marks"],
                   "The 5th mark goes across the other four. This makes a group of 5 that is easy to count in 5s."))
    # 7-10 tally table: favourite fruit
    cats = ["Apple", "Banana", "Mango", "Grapes"]
    vals = [8, 5, 11, 3]
    f = fig(table_svg("Favourite fruit", "Fruit", cats, vals, "tally table: favourite fruit", missing=2))
    its.append(mcq(f + "What number goes in the Number column for Mango?", 11, tally_cands(11) + [8],
                   "Mango has 2 groups of 5 and 1 more. Count 5, 10, then 11. So 11 goes in the table."))
    its.append(mcq(f + "Which fruit got the fewest votes?", "Grapes", ["Banana", "Apple", "Mango"],
                   "Grapes has only 3 marks and no group of 5. That is fewer than Banana (5), Apple (8) and Mango (11)."))
    its.append(mcq(f + "How many more votes did Apple get than Banana?", "3 votes", ["13 votes", "8 votes", "2 votes"],
                   "Apple 8, Banana 5. How many more means take away: 8 − 5 = 3. (13 is 8 + 5, the votes altogether.)"))
    its.append(mcq(f + "How many votes were there altogether?", "27 votes",
                   ["23 votes", "26 votes", "16 votes"],
                   "First find Mango: 11. Then add every row: 8 + 5 + 11 + 3 = 27. "
                   "(Counting each group of 5 as 4 gives 23. Leaving out Mango gives 16.)"))
    # 11-14 table without tallies: weather this fortnight (14 days)
    cats = ["Sunny", "Cloudy", "Rainy", "Windy"]
    vals = [6, 4, 3, 1]
    f = fig(table_svg("Weather in the last 2 weeks", "Weather", cats, vals, "table: weather in the last 2 weeks",
                      tally=False, numhead="Days"))
    its.append(mcq(f + "How many days were rainy?", "3 days", ["4 days", "1 day", "6 days"],
                   "Put your finger on Rainy. Go across to the Days column. It says 3. "
                   "(4 is the row above, Cloudy.)"))
    its.append(mcq(f + "Which weather did we have most often?", "Sunny", ["Cloudy", "Rainy", "Windy"],
                   "The biggest number in the Days column is 6, next to Sunny."))
    its.append(mcq(f + "How many more sunny days than rainy days were there?", "3 days", ["9 days", "2 days", "6 days"],
                   "Sunny 6, rainy 3. How many more means take away: 6 − 3 = 3. (9 is 6 + 3.)"))
    its.append(mcq(f + "How many days were <b>not</b> sunny?", "8 days", ["6 days", "14 days", "7 days"],
                   "Not sunny means cloudy, rainy or windy: 4 + 3 + 1 = 8 days. Check: 14 days − 6 sunny days = 8."))
    # 15-16 make a tally from a list
    lst = ["dog", "cat", "dog", "fish", "dog", "cat", "dog", "dog", "cat", "fish", "dog", "rabbit"]
    L = ", ".join(lst)
    its.append(mcq("Noah asked his friends, “What pet do you have?” He wrote: <b>%s</b>. "
                   "How many tally marks should go next to Dog?" % L, "6 marks", ["3 marks", "12 marks", "5 marks"],
                   "Cross off each “dog” as you count it: 1, 2, 3, 4, 5, 6. Draw a group of 5 and 1 more mark. "
                   "(12 is all the answers, and 3 is the cats.)"))
    its.append(mcq("Here are Noah’s answers again: <b>%s</b>. Which pet did only one friend have?" % L, "Rabbit",
                   ["Fish", "Cat", "Dog"],
                   "Count each pet: dog 6, cat 3, fish 2, rabbit 1. Only one friend has a rabbit."))
    # 17 total row
    cats = ["Walk", "Car", "Bus", "Bike"]
    vals = [7, 9, 4, 5]
    f = fig(table_svg("How we get to school", "Way", cats, vals, "tally table: how we get to school", total=True,
                      missing=3))
    its.append(mcq(f + "There are 25 students in the survey. How many students ride a bike?", "5 students",
                   ["20 students", "4 students", "6 students"],
                   "Add the rows we know: 7 + 9 + 4 = 20. Then 25 − 20 = 5. "
                   "Check the tally: Bike has 1 group of 5. So 5 students ride a bike."))
    its.append(mcq(f + "How many more students come by car than walk?", "2 students",
                   ["16 students", "4 students", "9 students"],
                   "Car 9, walk 7. How many more means take away: 9 − 7 = 2. (16 is 9 + 7.)"))
    # 19-20 word problems
    its.append(mcq("Jack counts the cars going past the school gate. He draws 3 groups of 5 and 2 more marks. "
                   "How many cars did he count?", "17 cars", ["14 cars", "5 cars", "32 cars"],
                   "Count the groups in 5s: 5, 10, 15. Then 2 more: 16, 17. So 17 cars. "
                   "(Counting each group as 4 gives 14.)"))
    its.append(mcq("Ruby counted 13 votes for netball. How should she draw the tally?", "2 groups of 5 and 3 marks",
                   ["1 group of 5 and 8 marks", "13 groups of 5", "3 groups of 5 and 2 marks"],
                   "13 = 5 + 5 + 3. Draw 2 groups of 5, then 3 single marks. "
                   "Never leave 5 single marks: make another group of 5. (3 groups and 2 marks is 17.)"))
    assert len(its) == 20, len(its)
    return {"title": "Tally marks and tables", "items": its}


# ------------------------------------------------------------ set 3: picture graphs (one picture for each)
def set_picture(rnd, PK):
    its = []
    plan = ["read", "read", "most", "read", "fewest", "which", "read", "more", "which", "fewer",
            "more", "both", "most", "read", "more", "which", "total", "fewest", "more", "total"]
    for i, kind in enumerate(plan):
        ctx = PK.next()
        sym = SYMS[i % 3]
        n = 3 if (i < 4 and kind == "read") else (5 if i % 3 == 0 and len(ctx.cats) >= 5 else 4)
        cats, vals = make_data(ctx, n, rnd, lo=2 if i < 8 else 1, hi=7 if i < 8 else 9,
                               ok=lambda vs: max(vs) - min(vs) >= 3)
        f = fig(ctx_pic(ctx, cats, vals, sym))
        U = ctx.unit
        key = "Each %s stands for %s. " % (sym, fmt(1, U))
        if kind == "read":
            j = rnd.randrange(n)
            c, v = cats[j], vals[j]
            nb = [vals[k] for k in (j - 1, j + 1) if 0 <= k < n]
            cand = nb + [v + 1, v - 1] + vals
            its.append(mcq(f + ctx.ask(c), fmt(v, U), [fmt(x, U) for x in cand],
                           "%sPut your finger on the %s row and count the %ss: %s. So %s. "
                           "(Make sure you count the right row.)" % (key, c, sym, count_list(v), fmt(v, U))))
        elif kind in ("most", "fewest"):
            j = vals.index(max(vals) if kind == "most" else min(vals))
            w = "most" if kind == "most" else "fewest"
            longest = "longest" if kind == "most" else "shortest"
            its.append(mcq(f + "Which row has the %s %s?" % (w, U[1]), cats[j], [cats[k] for k in range(n) if k != j],
                           "Each %s stands for 1, so the %s row has the %s. %s has %s. "
                           % (sym, longest, w, cats[j], ones(vals[j], sym)) +
                           "Others: " + ", ".join("%s %d" % (cats[k], vals[k]) for k in range(n) if k != j) + "."))
        elif kind == "which":
            j = rnd.randrange(n)
            v = vals[j]
            near = sorted([k for k in range(n) if k != j], key=lambda k: abs(vals[k] - v))
            cand = [cats[k] for k in near] + [x for x in ctx.cats if x not in cats]
            its.append(mcq(f + "Which row shows %s?" % fmt(v, U), cats[j], cand,
                           "Count the %ss in each row. The %s row has %d, so it shows %s."
                           % (sym, cats[j], v, fmt(v, U))))
        elif kind in ("more", "fewer"):
            pairs = [(a, b) for a in range(n) for b in range(n) if vals[a] - vals[b] >= 2]
            a, b = rnd.choice(pairs)
            if kind == "fewer":
                a, b = b, a
            d = abs(vals[a] - vals[b])
            q = ctx.more(cats[a], cats[b]) if kind == "more" else ctx.fewer(cats[a], cats[b])
            cand = [vals[a] + vals[b], max(vals[a], vals[b]), d + 1, d - 1, min(vals[a], vals[b])]
            its.append(mcq(f + q, fmt(d, U), [fmt(x, U) for x in cand],
                           "%s: %d. %s: %d. How many %s means find the difference: %d − %d = %d. "
                           "You can also match the %ss in the two rows and count the extra ones. "
                           "(Adding gives %d.)"
                           % (cats[a], vals[a], cats[b], vals[b], kind, max(vals[a], vals[b]), min(vals[a], vals[b]), d,
                              sym, vals[a] + vals[b])))
        elif kind == "both":
            a, b = rnd.sample(range(n), 2)
            t = vals[a] + vals[b]
            cand = [abs(vals[a] - vals[b]), t + 1, t - 1, max(vals[a], vals[b]), sum(vals)]
            its.append(mcq(f + ctx.both(cats[a], cats[b]), fmt(t, U), [fmt(x, U) for x in cand],
                           "%s: %d. %s: %d. Altogether means add: %d + %d = %s."
                           % (cats[a], vals[a], cats[b], vals[b], vals[a], vals[b], fmt(t, U))))
        else:
            t = sum(vals)
            cand = [t - min(vals), t + 1, t - 1, max(vals), t + 10]
            its.append(mcq(f + ctx.total, fmt(t, U), [fmt(x, U) for x in cand],
                           "Count every row: %s. Add them: %s = %s."
                           % (", ".join("%s %d" % (c, v) for c, v in zip(cats, vals)), plus(vals), fmt(t, U))))
    return {"title": "Picture graphs: one picture for each", "items": its}


# ------------------------------------------------------------ set 4: column graphs (scale of 1)
def set_column(rnd, PK):
    its = []
    plan = ["read", "read", "step", "most", "read", "which", "fewest", "read", "which", "more",
            "read", "more", "both", "fewer", "which", "more", "total", "most", "more", "both"]
    for i, kind in enumerate(plan):
        ctx = PK.next()
        n = 3 if i < 3 else (5 if i % 3 == 0 and len(ctx.cats) >= 5 else 4)
        cats, vals = make_data(ctx, n, rnd, lo=2 if i < 8 else 1, hi=8 if i < 8 else 10,
                               ok=lambda vs: max(vs) - min(vs) >= 3)
        f = fig(ctx_bar(ctx, cats, vals))
        U = ctx.unit
        if kind == "read":
            j = rnd.randrange(n)
            c, v = cats[j], vals[j]
            nb = [vals[k] for k in (j - 1, j + 1) if 0 <= k < n]
            cand = nb + [v + 1, v - 1] + vals
            its.append(mcq(f + ctx.ask(c), fmt(v, U), [fmt(x, U) for x in cand],
                           "Find %s at the bottom. Go up to the top of that column, then across to the numbers. "
                           "It ends on the line for %d. So %s. (Use the column above the label, not the one next to it.)"
                           % (c, v, fmt(v, U))))
        elif kind == "step":
            its.append(mcq(f + "The numbers on the side go 0, 1, 2, 3 … How many does each line stand for?", "1",
                           ["2", "5", "10"],
                           "Each line is 1 more than the line below it, so each line stands for 1."))
        elif kind in ("most", "fewest"):
            j = vals.index(max(vals) if kind == "most" else min(vals))
            w = "most" if kind == "most" else "fewest"
            word = "tallest" if kind == "most" else "shortest"
            its.append(mcq(f + "Which column shows the %s %s?" % (w, U[1]), cats[j], [cats[k] for k in range(n) if k != j],
                           "The %s column shows the %s. The %s column is %d high." % (word, w, cats[j], vals[j])))
        elif kind == "which":
            j = rnd.randrange(n)
            v = vals[j]
            near = sorted([k for k in range(n) if k != j], key=lambda k: abs(vals[k] - v))
            cand = [cats[k] for k in near] + [x for x in ctx.cats if x not in cats]
            its.append(mcq(f + "Which column shows %s?" % fmt(v, U), cats[j], cand,
                           "Find %d on the side. Go across the line for %d. The %s column ends on that line."
                           % (v, v, cats[j])))
        elif kind in ("more", "fewer"):
            pairs = [(a, b) for a in range(n) for b in range(n) if vals[a] - vals[b] >= 2]
            a, b = rnd.choice(pairs)
            if kind == "fewer":
                a, b = b, a
            d = abs(vals[a] - vals[b])
            q = ctx.more(cats[a], cats[b]) if kind == "more" else ctx.fewer(cats[a], cats[b])
            cand = [vals[a] + vals[b], max(vals[a], vals[b]), d + 1, d - 1, min(vals[a], vals[b])]
            its.append(mcq(f + q, fmt(d, U), [fmt(x, U) for x in cand],
                           "%s: %d. %s: %d. How many %s means find the difference: %d − %d = %d. "
                           "(Adding gives %d, but that is how many altogether.)"
                           % (cats[a], vals[a], cats[b], vals[b], kind, max(vals[a], vals[b]), min(vals[a], vals[b]), d,
                              vals[a] + vals[b])))
        elif kind == "both":
            a, b = rnd.sample(range(n), 2)
            t = vals[a] + vals[b]
            cand = [abs(vals[a] - vals[b]), t + 1, t - 1, max(vals[a], vals[b]), sum(vals)]
            its.append(mcq(f + ctx.both(cats[a], cats[b]), fmt(t, U), [fmt(x, U) for x in cand],
                           "%s: %d. %s: %d. Altogether means add: %d + %d = %s. (%d is the difference.)"
                           % (cats[a], vals[a], cats[b], vals[b], vals[a], vals[b], fmt(t, U), abs(vals[a] - vals[b]))))
        else:
            t = sum(vals)
            cand = [t - min(vals), t + 1, t - 1, max(vals), t + 10]
            its.append(mcq(f + ctx.total, fmt(t, U), [fmt(x, U) for x in cand],
                           "Read every column: %s. Add them: %s = %s."
                           % (", ".join("%s %d" % (c, v) for c, v in zip(cats, vals)), plus(vals), fmt(t, U))))
    return {"title": "Column graphs with a scale of 1", "items": its}


# ------------------------------------------------------------ set 5: compare displays and word problems
PW, PH = 218, 172

MATCH_WHY = {
    "swap": "two columns are the wrong way round",
    "high": "one column is 1 too tall",
    "low": "one column is 1 too short",
    "pswap": "two rows are the wrong way round",
    "pone": "one row has 1 picture too many",
    "pless": "one row has 1 picture too few",
}


def mini_bar(x0, y0, cats, vals, top_v):
    fs = 14
    gy = 112.0 / top_v
    ax = x0 + 34
    yb = y0 + 142
    slot = 44
    s = []
    for k in range(top_v + 1):
        y = yb - k * gy
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1'/>" % (ax, y, ax + slot * len(cats), y, GRID))
        if top_v <= 8 or k % 2 == 0:
            s.append(text(ax - 4, y + 5, k, fs, anchor="end"))
    for i, (c, v) in enumerate(zip(cats, vals)):
        cx = ax + slot * i + slot / 2
        h = v * gy
        s.append("<rect x='%.1f' y='%.1f' width='24' height='%.1f' fill='%s'/>" % (cx - 12, yb - h, h, BAR))
        s.append(text(cx, yb + 17, c, fs))
        assert tw(c, fs) <= slot - 2, c
    s.append("<path d='M%.1f %.1f V%.1f H%.1f' fill='none' stroke='%s' stroke-width='2'/>" % (ax, yb - 116, yb, ax + slot * len(cats), INK))
    assert ax + slot * len(cats) <= x0 + PW - 2
    return "".join(s)


def mini_pic(x0, y0, cats, vals, sym):
    fs, rh, gap = 14, 25, 20
    lw = x0 + max(tw(c, fs) for c in cats) + 14
    s = []
    for i, (c, v) in enumerate(zip(cats, vals)):
        y = y0 + 28 + i * rh
        s.append(text(lw - 7, y + 17, c, fs, anchor="end"))
        for j in range(v):
            cx = lw + 4 + j * gap + 9
            s.append(symbol(sym, cx, y + rh / 2))
            assert cx + 10 <= x0 + PW - 2, (cats, vals)
    s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1.5'/>"
             % (lw, y0 + 28, lw, y0 + 28 + rh * len(cats), GREEN))
    return "".join(s)


def panel_svg(draws, label, key_line=None):
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


def match_q(rnd, pos, title, cats, vals, unit, pic=False, sym="circle"):
    """Which picture (A to D) shows the data in the table? Wrong pictures come from real drawing mistakes."""
    n = len(vals)
    i, j = rnd.sample(range(n), 2)
    while vals[i] == vals[j]:
        i, j = rnd.sample(range(n), 2)
    sw = vals[:]
    sw[i], sw[j] = sw[j], sw[i]
    k = rnd.choice([x for x in range(n)])
    hi = vals[:]
    hi[k] += 1
    k2 = rnd.choice([x for x in range(n) if x != k and vals[x] > 1])
    lo = vals[:]
    lo[k2] -= 1
    wrong = [("pswap" if pic else "swap", sw), ("pone" if pic else "high", hi), ("pless" if pic else "low", lo)]
    rnd.shuffle(wrong)
    order = wrong[:]
    order.insert(pos, ("ok", vals))
    assert len({tuple(v) for _, v in order}) == 4
    top_v = max(max(max(v) for _, v in order) + 1, 5)
    if pic:
        draws = [(lambda x0, y0, v=v: mini_pic(x0, y0, cats, v, sym)) for _, v in order]
        g = panel_svg(draws, "picture graphs: " + title.lower(), key_line=(sym, "= " + fmt(1, unit)))
        q = "Which picture graph shows the same data as the table?"
    else:
        draws = [(lambda x0, y0, v=v: mini_bar(x0, y0, cats, v, top_v)) for _, v in order]
        g = panel_svg(draws, "column graphs: " + title.lower())
        q = "Which column graph shows the same data as the table?"
    why = ["%s: %s" % ("ABCD"[k], MATCH_WHY[tag]) for k, (tag, v) in enumerate(order) if tag != "ok"]
    e = ("Check every %s against the table: %s. %s matches every number. %s."
         % ("row" if pic else "column", ", ".join("%s %d" % (c, v) for c, v in zip(cats, vals)), "ABCD"[pos],
            "; ".join(why)))
    return g, q, e, pos


def set_compare(rnd):
    its = []
    # 1-4 match a table to a graph (A to D); the table is given as text (one SVG per question)
    M = [(2, "Favourite colour", ["Red", "Blue", "Pink", "Green"], [5, 7, 3, 6], VOTE, False, "circle", False),
         (0, "Pets", ["Dog", "Cat", "Fish", "Bird"], [6, 4, 2, 5], STU, False, "circle", True),
         (3, "Fruit", ["Apple", "Kiwi", "Plum", "Pear"], [4, 6, 5, 2], VOTE, True, "star", False),
         (1, "Birds seen", ["Magpie", "Galah", "Ibis"], [6, 3, 5], ("bird", "birds"), True, "circle", True)]
    for pos, title, cats, vals, U, pic, sym, tally in M:
        g, q, e, p = match_q(rnd, pos, title, cats, vals, U, pic=pic, sym=sym)
        if tally:
            head = "<b>Tally table</b>: %s. " % ", ".join("%s %s" % (c, tally_word(v)) for c, v in zip(cats, vals))
            e = "First count the tallies: %s. " % ", ".join("%s %d" % (c, v) for c, v in zip(cats, vals)) + e
            q = q.replace("the table", "the tally table")
        else:
            head = "<b>Table</b>: %s. " % ", ".join("%s %d" % (c, v) for c, v in zip(cats, vals))
        its.append(mcq_fixed(fig(g) + head + q, ["A", "B", "C", "D"], p, e))
    # 5-8 tally table and column graph of the same data, one column missing
    P = [(BYTITLE["Favourite fruit"], ["Apple", "Banana", "Mango", "Orange"], [6, 9, 4, 7], 1),
         (BYTITLE["Shells found at the beach"], ["Ruby", "Kai", "Zara", "Leo"], [5, 8, 10, 3], 2),
         (BYTITLE["Books read this week"], ["Isla", "Jack", "Mia", "Oliver"], [4, 7, 3, 6], 3),
         (BYTITLE["How we get to school"], ["Walk", "Car", "Bus", "Bike"], [7, 11, 6, 2], 1)]
    for ctx, cats, vals, miss in P:
        U = ctx.unit
        tp = table_part(ctx.title, ctx.axis, cats, vals, num=False)
        bp = bar_part("Column graph", ctx.axis, U[1].capitalize(), cats, vals, missing=miss, top_v=max(vals) + 1)
        svg = side_by_side([tp, bp], "tally table and column graph: " + ctx.title.lower())
        v = vals[miss]
        g, r = v // 5, v % 5
        cand = [g * 4 + r, vals[miss - 1], vals[(miss + 1) % 4], v + 1, v - 1]
        its.append(mcq(fig(svg) + "The tally table and the column graph show the same data. "
                       "How tall should the missing column for %s be?" % cats[miss], fmt(v, U),
                       [fmt(x, U) for x in cand],
                       "Read the %s row of the tally table. %s Draw the %s column up to the line for %d."
                       % (cats[miss], tally_text(v), cats[miss], v)))
    # 9-13 favourite sport column graph
    sp_c = ["AFL", "Cricket", "Netball", "Soccer", "Swim"]
    sp_v = [8, 5, 9, 6, 3]
    sport = fig(bar_svg("Favourite sport in 2A", "Sport", "Students", sp_c, sp_v, label="column graph: favourite sport in 2a"))
    its.append(mcq(sport + "How many more students chose netball than cricket?", "4 students",
                   ["14 students", "5 students", "3 students"],
                   "Netball 9, cricket 5. How many more means take away: 9 − 5 = 4. (14 is 9 + 5.)"))
    its.append(mcq(sport + "How many students chose AFL or soccer?", "14 students",
                   ["2 students", "13 students", "8 students"],
                   "AFL 8, soccer 6. AFL or soccer means add: 8 + 6 = 14. (2 is the difference.)"))
    its.append(mcq(sport + "Every student in 2A voted once. How many students are in 2A?", "31 students",
                   ["9 students", "28 students", "30 students"],
                   "Read every column: 8, 5, 9, 6 and 3. Add them: 8 + 5 + 9 + 6 + 3 = 31. "
                   "(9 is only the tallest column.)"))
    its.append(mcq(sport + "Which sentence is true?", "Netball got 1 more vote than AFL.",
                   ["Swim was the most popular.", "Soccer got more votes than AFL.", "Cricket got 6 votes."],
                   "Netball 9 and AFL 8, so netball got 1 more. Swim (3) was the least popular. "
                   "Soccer (6) is less than AFL (8). Cricket got 5; 6 is soccer."))
    its.append(mcq(sport + "The teacher picks the two most popular sports for sport day. Which two?", "Netball and AFL",
                   ["Netball and soccer", "AFL and cricket", "Cricket and swim"],
                   "The two tallest columns are netball (9) and AFL (8). Soccer is next with 6."))
    # 14-17 picture graph: fruit sold at the canteen
    PF = ("piece of fruit", "pieces of fruit")
    fr_c = ["Apple", "Banana", "Orange", "Mango"]
    fr_v = [7, 4, 9, 2]
    fruit = fig(part_svg(pic_part("Fruit sold at the canteen", fr_c, fr_v, "circle", PF),
                         "picture graph: fruit sold at the canteen"))
    its.append(mcq(fruit + "How many more oranges than bananas were sold?", "5 oranges",
                   ["13 oranges", "4 oranges", "9 oranges"],
                   "Oranges 9, bananas 4. How many more means take away: 9 − 4 = 5. (13 is 9 + 4.)"))
    its.append(mcq(fruit + "How many apples and mangoes were sold altogether?", fmt(9, PF),
                   [fmt(x, PF) for x in [5, 7, 8]],
                   "Apples 7, mangoes 2. Altogether means add: 7 + 2 = 9. (5 is the difference.)"))
    its.append(mcq(fruit + "How many pieces of fruit were sold altogether?", fmt(22, PF),
                   [fmt(x, PF) for x in [20, 18, 9]],
                   "Count every row: 7, 4, 9, 2. Add them: 7 + 4 + 9 + 2 = 22. (Leaving out mango gives 20.)"))
    its.append(mcq(fruit + "Tomorrow the canteen sells 3 more mangoes. How many mangoes is that tomorrow?", "5 mangoes",
                   ["3 mangoes", "1 mango", "6 mangoes"],
                   "Today: 2 mangoes. 3 more means add: 2 + 3 = 5 mangoes."))
    # 18-20 compare displays
    its.append(mcq("Grace made a tally table and a column graph of the same votes. "
                   "Cricket has 2 groups of 5 and 1 more mark. How tall should the cricket column be?", "11 votes",
                   ["9 votes", "7 votes", "10 votes"],
                   "Count the tally: 5, 10, then 11. The column must also show 11. "
                   "(Counting each group as 4 gives 9.)"))
    its.append(mcq(fig(table_svg("Favourite Australian animal", "Animal", ["Koala", "Kangaroo", "Wombat"], [9, 6, 4],
                                 "table: favourite australian animal", tally=False, numhead="Votes")) +
                   "Lachlan says, “Koala got more votes than kangaroo and wombat together.” Is he right?",
                   "No. Kangaroo and wombat got 10, which is 1 more.",
                   ["Yes. Koala has the most votes.", "Yes. 9 is more than 6.", "No. Koala got 6 votes."],
                   "Kangaroo and wombat together: 6 + 4 = 10. Koala: 9. 10 is more than 9, so Lachlan is wrong."))
    its.append(mcq("Ethan wants to show his class which fruit got the most votes. Which display shows this "
                   "most quickly?", "A column graph", ["A list of every vote", "A pile of voting slips", "A sentence for each vote"],
                   "In a column graph you can see the tallest column at once. "
                   "With a list of every vote you must count each fruit first."))
    assert len(its) == 20, len(its)
    return {"title": "Compare displays and answer questions", "items": its}


def tally_word(v):
    g, r = v // 5, v % 5
    parts = []
    if g:
        parts.append(ones(g, "group") + " of 5")
    if r:
        parts.append(ones(r, "mark"))
    return " and ".join(parts)


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


def body_html():
    groups = [[("circle", "red", True), ("square", "red", False), ("triangle", "red", True), ("star", "red", False)],
              [("square", "blue", True), ("circle", "blue", False), ("star", "blue", True)]]
    sp = ["AFL", "Cricket", "Netball", "Soccer"]
    spv = [7, 4, 6, 3]
    return (
        "<h2>What is data?</h2>"
        "<p>Data is information we collect. We can ask a question, such as “What is your favourite sport?”, "
        "or we can look and count, such as birds in the schoolyard. "
        "Then we <b>sort</b> the data into groups and show it in a <b>table</b> or a <b>graph</b>.</p>"
        "<h2>Sort into groups</h2>"
        "<p>Choose one rule, such as colour, shape or size. Every object goes into one group only.</p>"
        "<figure class='sn-fig'>" + loops_svg(groups, ["Red", "Blue"]) +
        "<figcaption>Sorted by colour. The shapes are mixed, but every shape in a group is the same colour.</figcaption></figure>" +
        "<h2>Tally marks and tables</h2>"
        "<p>Draw one mark for each thing. The <b>5th mark goes across</b> the other four. "
        "Count the groups in 5s, then count on the single marks. Write the number in the table.</p>"
        "<figure class='sn-fig'>" + table_svg("Favourite sport", "Sport", sp, spv, "tally table: favourite sport") +
        "<figcaption>AFL: 1 group of 5 and 2 more. Count 5, then 6, 7. So 7 students chose AFL.</figcaption></figure>" +
        ex("Example", "How many students chose netball?", "1 group of 5 is 5. Then 1 more: 6.", "6 students") +
        "<h2>Picture graphs</h2>"
        "<p>In a picture graph, one picture stands for one thing. Count the pictures in each row. "
        "The longest row is the most.</p>"
        "<figure class='sn-fig'>" + part_svg(pic_part("Favourite sport", sp, spv, "circle", STU),
                                             "picture graph: favourite sport") +
        "<figcaption>Each circle = 1 student. Cricket has 4 circles, so 4 students chose cricket.</figcaption></figure>" +
        "<h2>Column graphs</h2>"
        "<p>Find the label at the bottom. Go up to the top of its column, then across to the numbers. "
        "Each line stands for 1. The tallest column is the most.</p>"
        "<figure class='sn-fig'>" + bar_svg("Favourite sport", "Sport", "Students", sp, spv,
                                            label="column graph: favourite sport") +
        "<figcaption>The netball column ends on the line for 6, so 6 students chose netball.</figcaption></figure>" +
        "<p>The table, the picture graph and the column graph above all show the same data.</p>"
        "<h2>Add or take away?</h2>" +
        table(["The question says", "Do this"], [
            ["altogether, in total, both, A or B", "Add"],
            ["how many more, how many fewer, difference", "Take away"],
        ]) +
        ex("Example", "How many more students chose AFL than soccer?", "AFL 7, soccer 3. 7 − 3 = 4.",
           "4 more students") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Counting a group of 5 tally marks as 4", "The line across is the 5th mark"],
            ["Drawing 5 lines and then a line across", "Draw 4 lines, then the 5th goes across"],
            ["Sorting by colour when the rule is shape", "Read the rule, and look only at that"],
            ["Reading the row or column next to the right one", "Put your finger on the label first"],
            ["Adding when the question says how many more", "How many more means take away"],
        ])
    )


FAQ = [
    {"q": "What do Year 2 students learn about data in the Australian Curriculum?",
     "a": "They collect data with surveys and by counting, sort it into categories and record it in lists and tables. They also make and compare simple displays such as picture graphs and column graphs."},
    {"q": "How do you teach tally marks in Year 2?",
     "a": "Draw one mark for each thing and draw the 5th mark across the other four. Students then count the groups in 5s and count on the single marks: 2 groups and 3 marks is 13."},
    {"q": "What is the difference between a picture graph and a column graph?",
     "a": "A picture graph uses a picture for each thing, so you count the pictures. A column graph uses columns, so you read the top of each column against the numbers on the side."},
    {"q": "Do Year 2 students sit NAPLAN?",
     "a": "No. NAPLAN starts in Year 3. Reading tables and graphs in Year 2 builds the skills students use later in Year 3."},
]


def balance(sets, rnd):
    """Move the answers of the free questions so every position is right 5 times in each set."""
    for s in sets:
        cnt_, free = [0] * 4, []
        for it in s["items"]:
            if it.pop("_fix", False):
                cnt_[it["a"]] += 1
            else:
                free.append(it)
        targets = []
        for p in range(4):
            assert cnt_[p] <= 5, (s["title"], cnt_)
            targets += [p] * (5 - cnt_[p])
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
    rnd = random.Random(2816)
    PK = Picker(rnd)
    sets = [set_sort(rnd), set_tally(rnd), set_picture(rnd, PK), set_column(rnd, PK), set_compare(rnd)]
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
        "country": "au", "subject": "maths", "grade": "year-2", "slug": "data-tables-and-graphs", "sort": 16,
        "updated": UPDATED, "pdf_url": "",
        "title": "Data, Tables and Graphs: Sorting, Tally Marks, Picture Graphs and Column Graphs",
        "seo_title": "Year 2 Data and Graphs Worksheets: Sorting, Tally Marks, Tables and Column Graphs (Free, with Answer Key)",
        "short_title": "Data, tables and graphs",
        "domain": "Statistics",
        "standard_code": "AC9M2ST01",
        "standard_url": "https://v9.australiancurriculum.edu.au/f-10-curriculum/learning-areas/mathematics",
        "standard_text": "Acquire data for categorical variables through surveys, observation, experiment and using digital tools; sort data into relevant categories and display data using lists and tables",
        "meta_desc": "Free Year 2 maths worksheets on data for the Australian Curriculum: sorting objects into groups, tally marks and tables, picture graphs and column graphs with a scale of 1, and “how many more?” questions. 100 questions with an answer key.",
        "key_big": "Sort by one rule, count carefully, then read the table or graph.",
        "key_sub": "The 5th tally mark goes across the other four. In a picture graph one picture is 1. Altogether means add; how many more means take away.",
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
        mark_large(u, "(picture graph|column graph|tally table|table|four sets|shapes)")
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
