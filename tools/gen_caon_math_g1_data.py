# -*- coding: utf-8 -*-
"""
CA Grade 1 Math: Sorting and graphs (Ontario Curriculum 2020, Data: D1.1 to D1.5)
  python3 tools/gen_caon_math_g1_data.py
Sort shapes by one attribute (colour, shape or size) and name the rule, tally marks in bundles of 5,
pictographs with one-to-one correspondence (with a title, labels and a source), ordering categories from
greatest to least, and comparing data in Canadian classroom contexts (favourite fruit, how we get to school).
Counts up to 14, totals up to 20. Wrong answers come from real mistakes: sorting by the wrong attribute,
reading the other group, counting a tally bundle as 4, reading the row above or below, adding when the
question asks how many more, giving the order backwards or in the order the rows are listed.
HTML attributes use single quotes (no backslashes in the JSON). Canadian English.
"""
import json, re, math, os, random

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-1")
UPDATED = "2026-11-02"
GREEN = "#006633"
RED = "#c0392b"
INK = "#2b2b2b"
GRID = "#c9d3cc"
MUTE = "#555555"
FONT = "Arial, Helvetica, sans-serif"
MINUS = "−"


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e):
    """4 choices: correct + the first 3 unique distractors (no zero or negative numbers)."""
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        if c is None:
            continue
        c = str(c)
        lead = c.split(" ")[0]
        if c in seen or not c or lead.startswith("-") or lead == "0":
            continue
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    return {"q": q, "c": [correct] + pick, "a": 0, "e": e}


def balance(sets, rnd):
    """Spread the correct answers evenly (5/5/5/5) over the 4 positions in every set.
    Items marked 'fixed' (A-D pictures) already have their position; the rest fill the gaps."""
    for s in sets:
        left = {0: 5, 1: 5, 2: 5, 3: 5}
        for it in s["items"]:
            if it.get("fixed"):
                left[it["a"]] -= 1
        assert min(left.values()) >= 0
        targets = [p for p in range(4) for _ in range(left[p])]
        rnd.shuffle(targets)
        free = [it for it in s["items"] if not it.get("fixed")]
        assert len(free) == len(targets)
        for it, t in zip(free, targets):
            c = it["c"]
            wrong = [x for i, x in enumerate(c) if i != it["a"]]
            rnd.shuffle(wrong)
            right = c[it["a"]]
            it["c"] = wrong[:t] + [right] + wrong[t:]
            it["a"] = t
        for it in s["items"]:
            it.pop("fixed", None)


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


def cap(s):
    return s[0].upper() + s[1:]


def plus(vals):
    return " + ".join(str(v) for v in vals)


def minus(a, b):
    return "%d %s %d = %d" % (a, MINUS, b, a - b)


def letters(ks):
    ks = sorted(ks)
    return ", ".join("ABCD"[k] for k in ks[:-1]) + " and " + "ABCD"[ks[-1]]


# ------------------------------------------------------------ symbols / shapes
def star_pts(cx, cy, R=9.5, r=4.0):
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rad = R if i % 2 == 0 else r
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    return pts


def symbol(kind, cx, cy, col=GREEN, k=1.0, stroke=False):
    """Small shape centred on (cx, cy). k scales it. stroke adds a dark outline (for sorting pictures)."""
    st = " stroke='%s' stroke-width='1.2' stroke-linejoin='round'" % INK if stroke else ""
    if kind == "circle":
        return "<circle cx='%.1f' cy='%.1f' r='%.1f' fill='%s'%s/>" % (cx, cy, 8.5 * k, col, st)
    if kind == "square":
        h = 7.5 * k
        return "<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' rx='1.5' fill='%s'%s/>" % (cx - h, cy - h, 2 * h, 2 * h, col, st)
    if kind == "triangle":
        h = 9.5 * k
        return "<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='%s'%s/>" % (
            cx, cy - h, cx + h, cy + h * 0.8, cx - h, cy + h * 0.8, col, st)
    if kind == "heart":
        return ("<path d='M%.1f %.1f C%.1f %.1f %.1f %.1f %.1f %.1f C%.1f %.1f %.1f %.1f %.1f %.1f Z' fill='%s'%s/>"
                % (cx, cy + 8 * k, cx - 12 * k, cy - 1 * k, cx - 6 * k, cy - 11 * k, cx, cy - 4 * k,
                   cx + 6 * k, cy - 11 * k, cx + 12 * k, cy - 1 * k, cx, cy + 8 * k, col, st))
    return "<polygon points='%s' fill='%s'%s/>" % (" ".join("%.1f,%.1f" % p for p in star_pts(cx, cy, 10.5 * k, 4.4 * k)), col, st)


SYMS = ["circle", "star", "square", "heart"]

# Things to sort: (shape, colour, size)
SHAPES = ["circle", "square", "triangle", "star"]
COLOURS = ["red", "blue", "yellow", "green"]
SIZES = ["big", "small"]
COL = {"red": "#d64234", "blue": "#2e6fb0", "yellow": "#f2c418", "green": "#2e9b57"}
SIZE_K = {"big": 1.35, "small": 0.72}
ATTR_VALS = {0: SHAPES, 1: COLOURS, 2: SIZES}
ATTR_NAME = {0: "shape", 1: "colour", 2: "size"}
PL = {"circle": "circles", "square": "squares", "triangle": "triangles", "star": "stars"}


def draw_item(it, cx, cy):
    return symbol(it[0], cx, cy, COL[it[1]], SIZE_K[it[2]], stroke=True)


def val_word(attr, v):
    """'circles', 'red', 'big' - as in 'They are all ___'."""
    return PL[v] if attr == 0 else v


def rule_txt(attr, v):
    return "All " + val_word(attr, v)


def item_name(it):
    return "%s %s %s" % (it[2], it[1], it[0])


CELL = 34


def box(x, y, w, h, title, dashed=False):
    s = ["<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' rx='8' fill='#f6faf7' stroke='%s' stroke-width='1.5'%s/>"
         % (x, y, w, h, GREEN, " stroke-dasharray='5 4'" if dashed else "")]
    if title:
        s.append(text(x + w / 2, y - 6, title, 15, bold=True))
    return "".join(s)


def groups_svg(groups, label, per_row=3):
    """Boxes side by side, each with a title above and its things inside."""
    rows = max(int(math.ceil(len(g[1]) / float(per_row))) for g in groups)
    bw, bh = per_row * CELL + 12, rows * CELL + 10
    gap = 16
    W = len(groups) * bw + (len(groups) - 1) * gap + 8
    H = 22 + bh + 4
    s = []
    for gi, (title, items) in enumerate(groups):
        x = 4 + gi * (bw + gap)
        s.append(box(x, 22, bw, bh, title))
        for k, it in enumerate(items):
            r, c = divmod(k, per_row)
            s.append(draw_item(it, x + 6 + c * CELL + CELL / 2, 22 + 5 + r * CELL + CELL / 2))
    return svg_wrap(W, H, "".join(s), label)


def mixed_svg(items, rnd, label="mixed shapes to sort", cols=5):
    """Things scattered (one per cell, small jitter) so they must be sorted before counting."""
    n = len(items)
    rows = int(math.ceil(n / float(cols)))
    if rows * cols - n < 2:
        rows += 1
    cells = sorted(rnd.sample(range(rows * cols), n))
    items = items[:]
    rnd.shuffle(items)
    W, H = cols * CELL + 8, rows * CELL + 8
    s = ["<rect x='1' y='1' width='%d' height='%d' rx='8' fill='#f6faf7' stroke='%s' stroke-width='1.5'/>" % (W - 2, H - 2, GRID)]
    for it, c in zip(items, cells):
        r, cc = divmod(c, cols)
        cx = 4 + cc * CELL + CELL / 2 + rnd.choice([-2, -1, 0, 1, 2])
        cy = 4 + r * CELL + CELL / 2 + rnd.choice([-2, -1, 0, 1, 2])
        s.append(draw_item(it, cx, cy))
    return svg_wrap(W, H, "".join(s), label)


def where_svg(new, groups, label):
    """A dashed 'New' box on the left, then 4 sorted boxes in a 2 x 2 grid (2 things in each)."""
    bw, bh, gap = 2 * CELL + 12, CELL + 10, 10
    nx = 4
    nw = CELL + 22
    gx = nx + nw + 18
    H = 2 * (22 + bh) + gap + 4
    s = [box(nx, H / 2 - bh / 2 + 4, nw, bh, "New", dashed=True),
         draw_item(new, nx + nw / 2, H / 2 + 4)]
    for gi, (title, items) in enumerate(groups):
        r, c = divmod(gi, 2)
        x = gx + c * (bw + gap)
        y = 22 + r * (22 + bh + gap)
        s.append(box(x, y, bw, bh, title))
        for k, it in enumerate(items):
            s.append(draw_item(it, x + 6 + k * CELL + CELL / 2, y + 5 + CELL / 2))
    W = gx + 2 * bw + gap + 4
    return svg_wrap(W, int(H), "".join(s), label)


def belong_svg(rule, items, label):
    """Rule at the top, 4 things labelled A-D underneath."""
    cw = 52
    W = 4 * cw + 8
    W = int(max(W, tw(rule, 16, True) + 16))
    x0 = (W - 4 * cw) / 2
    s = [text(W / 2, 18, rule, 16, bold=True),
         "<rect x='%.1f' y='28' width='%d' height='%d' rx='8' fill='#f6faf7' stroke='%s' stroke-width='1.5'/>"
         % (x0, 4 * cw, CELL + 12, GREEN)]
    for k, it in enumerate(items):
        cx = x0 + k * cw + cw / 2
        s.append(draw_item(it, cx, 28 + 6 + CELL / 2))
        s.append(text(cx, 28 + CELL + 12 + 20, "ABCD"[k], 16, bold=True))
    H = 28 + CELL + 12 + 26
    return svg_wrap(W, H, "".join(s), label)


# ------------------------------------------------------------ contexts
class Ctx:
    def __init__(self, title, axis, cats, unit, f, source, ph=None, sumto=None):
        self.title, self.axis, self.cats, self.unit = title, axis, cats, unit
        self.f, self.source, self.ph, self.sumto = f, source, ph or {}, sumto

    def p(self, c):
        return self.ph.get(c, c)

    def q(self, kind, a=None, b=None, w=None, v=None):
        return self.f[kind].format(a=self.p(a) if a else "", b=self.p(b) if b else "",
                                   w=w or "", v=v if v is not None else "",
                                   n=fmt(v, self.unit) if v is not None else "")

    def has(self, kind):
        return kind in self.f


VOTE = ("vote", "votes")
KID = ("student", "students")
LOWER = lambda cs: {c: c.lower() for c in cs}


def votes_f(word):
    return {"ask": "How many votes did {a} get?",
            "more": "How many more votes did {a} get than {b}?",
            "fewer": "How many fewer votes did {a} get than {b}?",
            "both": "How many votes did {a} and {b} get altogether?",
            "total": "How many votes were there altogether?",
            "tie": "How many more votes does {b} need to tie with {a}?",
            "most": "Which %s got the {w} votes?" % word,
            "which": "Which %s got {n}?" % word}


def person_f(verb, past, noun):
    return {"ask": "How many %s did {a} %s?" % (noun, verb),
            "more": "How many more %s did {a} %s than {b}?" % (noun, verb),
            "fewer": "How many fewer %s did {a} %s than {b}?" % (noun, verb),
            "both": "How many %s did {a} and {b} %s altogether?" % (noun, verb),
            "total": "How many %s did they %s altogether?" % (noun, verb),
            "tie": "How many more %s does {b} need to %s to tie with {a}?" % (noun, verb),
            "most": "Who %s the {w} %s?" % (past, noun),
            "which": "Who %s {n}?" % past}


CTXS = [
    Ctx("Favourite fruit", "Fruit", ["Apple", "Banana", "Grapes", "Orange"], VOTE, votes_f("fruit"),
        "Source: Ms. Lee’s class vote"),
    Ctx("How we get to school", "Way", ["Bus", "Car", "Walk", "Bike"], KID,
        {"ask": "How many students {a} to school?",
         "more": "How many more students {a} than {b}?",
         "fewer": "How many fewer students {a} than {b}?",
         "both": "How many students {a} or {b}?",
         "total": "How many students are in the survey?",
         "most": "Which way do the {w} students get to school?",
         "which": "Which way do {n} get to school?"},
        "Source: Room 5 survey",
        ph={"Bus": "take the bus", "Car": "come by car", "Walk": "walk", "Bike": "ride a bike"}),
    Ctx("Favourite colour", "Colour", ["Red", "Blue", "Green", "Purple"], VOTE, votes_f("colour"),
        "Source: Mr. Khan’s class vote"),
    Ctx("Our pets", "Pet", ["Dog", "Cat", "Fish", "Bird"], KID,
        {"ask": "How many students have a {a}?",
         "more": "How many more students have a {a} than a {b}?",
         "fewer": "How many fewer students have a {a} than a {b}?",
         "both": "How many students have a {a} or a {b}?",
         "total": "How many students are in the survey?",
         "most": "Which pet do the {w} students have?",
         "which": "Which pet do {n} have?"},
        "Source: Room 2 survey", ph=LOWER(["Dog", "Cat", "Fish", "Bird"])),
    Ctx("Favourite snack", "Snack", ["Popcorn", "Crackers", "Yogurt", "Cheese"], KID,
        {"ask": "How many students chose {a}?",
         "more": "How many more students chose {a} than {b}?",
         "fewer": "How many fewer students chose {a} than {b}?",
         "both": "How many students chose {a} or {b}?",
         "total": "How many students voted altogether?",
         "tie": "How many more students need to choose {b} to tie with {a}?",
         "most": "Which snack did the {w} students choose?",
         "which": "Which snack did {n} choose?"},
        "Source: Mme Roy’s class vote", ph=LOWER(["Popcorn", "Crackers", "Yogurt", "Cheese"])),
    Ctx("What we play at recess", "Game", ["Tag", "Swings", "Slide", "Soccer"], KID,
        {"ask": "How many students picked {a}?",
         "more": "How many more students picked {a} than {b}?",
         "fewer": "How many fewer students picked {a} than {b}?",
         "both": "How many students picked {a} or {b}?",
         "total": "How many students are in the survey?",
         "most": "Which one did the {w} students pick?",
         "which": "Which one did {n} pick?"},
        "Source: Room 3 survey",
        ph={"Tag": "tag", "Swings": "the swings", "Slide": "the slide", "Soccer": "soccer"}),
    Ctx("Weather for 2 weeks", "Weather", ["Sunny", "Cloudy", "Rainy", "Snowy"], ("day", "days"),
        {"ask": "How many days were {a}?",
         "more": "How many more days were {a} than {b}?",
         "fewer": "How many fewer days were {a} than {b}?",
         "both": "How many days were {a} or {b}?",
         "total": "How many days are shown altogether?",
         "most": "Which weather had the {w} days?",
         "which": "Which weather had {n}?"},
        "Source: our class weather chart", ph=LOWER(["Sunny", "Cloudy", "Rainy", "Snowy"]), sumto=14),
    Ctx("Favourite winter fun", "Fun", ["Skating", "Sledding", "Hockey", "Skiing"], VOTE, votes_f("one"),
        "Source: Mr. Chen’s class vote"),
    Ctx("Birds at the feeder", "Bird", ["Chickadee", "Blue jay", "Cardinal", "Sparrow"], ("bird", "birds"),
        {"ask": "How many {a} did we see?",
         "more": "How many more {a} than {b} did we see?",
         "fewer": "How many fewer {a} than {b} did we see?",
         "both": "How many {a} and {b} did we see altogether?",
         "total": "How many birds did we see altogether?",
         "most": "Which bird did we see the {w} of?",
         "which": "Which bird did we see {v} of?"},
        "Source: our bird count",
        ph={"Chickadee": "chickadees", "Blue jay": "blue jays", "Cardinal": "cardinals", "Sparrow": "sparrows"}),
    Ctx("Books we read", "Name", ["Liam", "Maya", "Owen", "Zoe"], ("book", "books"),
        person_f("read", "read", "books"), "Source: our reading log"),
    Ctx("Apples we picked", "Name", ["Noah", "Emma", "Arjun", "Mei"], ("apple", "apples"),
        person_f("pick", "picked", "apples"), "Source: field trip tally"),
]
BYTITLE = {c.title: c for c in CTXS}

INTRO = {
    "Favourite fruit": "Ms. Lee’s class voted for a favourite fruit.",
    "How we get to school": "Room 5 asked how students get to school.",
    "Favourite colour": "Mr. Khan’s class voted for a favourite colour.",
    "Our pets": "Room 2 asked students about their pets.",
    "Favourite snack": "Mme Roy’s class voted for a party snack.",
    "What we play at recess": "Room 3 asked what students play at recess.",
    "Weather for 2 weeks": "Our class kept a weather chart for 2 weeks.",
    "Favourite winter fun": "Mr. Chen’s class voted for winter fun.",
    "Birds at the feeder": "We counted birds at the school feeder.",
    "Books we read": "Some friends kept a reading log.",
    "Apples we picked": "Some friends picked apples on a field trip.",
}


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


def make_data(ctx, rnd, lo=1, hi=9, ok=lambda v: True, n=3, tmax=20):
    """n categories with n different whole-number values, total at most tmax."""
    for _ in range(20000):
        cats = rnd.sample(ctx.cats, n)
        vals = [rnd.randint(lo, hi) for _ in range(n)]
        if len(set(vals)) != n or sum(vals) > tmax:
            continue
        if ctx.sumto and n == 3 and sum(vals) != ctx.sumto:
            continue
        if ctx.sumto and n != 3:
            continue
        if ok(vals):
            return cats, vals
    raise ValueError("no data for " + ctx.title)


# ------------------------------------------------------------ graphs
def source_line(y, src):
    return text(8, y, src, 14, anchor="start", col=MUTE, extra=" font-style='italic'")


def pic_svg(title, axis, cats, vals, sym, unit, source, label="pictograph"):
    """Pictograph: title, a label row, one row per category (each picture = 1), key and source."""
    fs, rh, gap = 15, 26, 23
    head = cap(unit[1])
    lw = max(max(tw(c, fs) for c in cats), tw(axis, fs, True)) + 22
    m = max(max(vals), 5)
    W = lw + 12 + m * gap + 12
    keytxt = "= " + fmt(1, unit)
    kw = tw("Key:", fs, True) + 32 + tw(keytxt, fs)
    W = int(math.ceil(max(W, tw(title, 16, True) + 16, kw + 16, tw(source, 14) + 16)))
    top = 28
    s = [text(W / 2, 19, title, 16, bold=True)]
    rows = len(cats) + 1
    H_tab = rows * rh
    s.append("<rect x='4' y='%d' width='%d' height='%d' fill='none' stroke='%s' stroke-width='1.5'/>" % (top, W - 8, H_tab, GREEN))
    s.append("<rect x='5' y='%d' width='%d' height='%d' fill='#e8f2ec'/>" % (top + 1, W - 10, rh - 1))
    s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.5'/>" % (lw, top, lw, top + H_tab, GREEN))
    s.append(text(lw - 8, top + 18, axis, fs, anchor="end", bold=True))
    s.append(text(lw + 12, top + 18, head, fs, anchor="start", bold=True))
    for i, (c, v) in enumerate(zip(cats, vals)):
        y = top + (i + 1) * rh
        s.append("<line x1='4' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (y, W - 4, y, GRID))
        s.append(text(lw - 8, y + 18, c, fs, anchor="end"))
        for j in range(v):
            s.append(symbol(sym, lw + 12 + j * gap + 9, y + rh / 2))
    ky = top + H_tab + 22
    x = (W - kw) / 2
    s.append(text(x, ky, "Key:", fs, anchor="start", bold=True))
    x += tw("Key:", fs, True) + 16
    s.append(symbol(sym, x, ky - 5))
    s.append(text(x + 14, ky, keytxt, fs, anchor="start"))
    s.append(source_line(ky + 24, source))
    H = ky + 30
    return svg_wrap(W, H, "".join(s), label)


def tally_marks(x, cy, v):
    """Tally marks: groups of 5 (four lines and one line across)."""
    s = []
    b, r = divmod(v, 5)
    for g in range(b + (1 if r else 0)):
        k = 4 if g < b else r
        gx = x + g * 36
        for i in range(k):
            s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2.2' stroke-linecap='round'/>"
                     % (gx + i * 6, cy - 9, gx + i * 6, cy + 9, INK))
        if g < b:
            s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2.2' stroke-linecap='round'/>"
                     % (gx - 4, cy + 6, gx + 22, cy - 6, INK))
    return "".join(s)


def plain_marks(x, cy, v, per=4):
    """Wrong tally: groups of `per` straight marks with no line across (a common mistake)."""
    s = []
    for i in range(v):
        g, k = divmod(i, per)
        mx = x + g * 36 + k * 6
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2.2' stroke-linecap='round'/>"
                 % (mx, cy - 9, mx, cy + 9, INK))
    return "".join(s)


def tally_svg(title, axis, cats, vals, source, label="tally chart"):
    fs, rh = 15, 28
    lw = max(max(tw(c, fs) for c in cats), tw(axis, fs, True)) + 22
    groups = max(math.ceil(v / 5.0) for v in vals)
    tw_ = max(groups * 36 + 4, tw("Tally", fs, True) + 20)
    W = int(math.ceil(max(lw + tw_ + 16, tw(title, 16, True) + 16, tw(source, 14) + 16)))
    top = 28
    s = [text(W / 2, 19, title, 16, bold=True)]
    rows = len(cats) + 1
    s.append("<rect x='4' y='%d' width='%d' height='%d' fill='none' stroke='%s' stroke-width='1.5'/>" % (top, W - 8, rows * rh, GREEN))
    s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.5'/>" % (lw, top, lw, top + rows * rh, GREEN))
    s.append("<rect x='5' y='%d' width='%d' height='%d' fill='#e8f2ec'/>" % (top + 1, W - 10, rh - 1))
    s.append(text(lw - 8, top + 19, axis, fs, anchor="end", bold=True))
    s.append(text(lw + 12, top + 19, "Tally", fs, anchor="start", bold=True))
    for i, (c, v) in enumerate(zip(cats, vals)):
        y = top + (i + 1) * rh
        s.append("<line x1='4' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (y, W - 4, y, GRID))
        s.append(text(lw - 8, y + 19, c, fs, anchor="end"))
        s.append(tally_marks(lw + 14, y + rh / 2, v))
    H = top + rows * rh + 22
    s.append(source_line(H - 6, source))
    return svg_wrap(W, H, "".join(s), label)


def tally4_svg(rows):
    """Four tally rows labelled A-D. rows = list of (kind, v): kind 'ok' or 'plain'."""
    rh = 34
    groups = max(int(math.ceil(v / 4.0)) for _, v in rows)
    W = 40 + groups * 36 + 10
    H = rh * 4 + 6
    s = []
    for i, (kind, v) in enumerate(rows):
        y = 3 + i * rh
        if i:
            s.append("<line x1='4' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (y, W - 4, y, GRID))
        s.append(text(10, y + rh / 2 + 6, "ABCD"[i], 18, anchor="start", bold=True))
        if kind == "ok":
            s.append(tally_marks(44, y + rh / 2, v))
        else:
            s.append(plain_marks(44, y + rh / 2, v))
    return svg_wrap(W, H, "".join(s), "four tally rows labelled A to D")


def ctx_pic(ctx, cats, vals, sym):
    return pic_svg(ctx.title, ctx.axis, cats, vals, sym, ctx.unit, ctx.source, label="pictograph: " + ctx.title.lower())


def ctx_tally(ctx, cats, vals):
    return tally_svg(ctx.title, ctx.axis, cats, vals, ctx.source, label="tally chart: " + ctx.title.lower())


# ------------------------------------------------------------ reading text (explanations)
def count_list(v):
    return ", ".join(str(k) for k in range(1, v + 1))


def count_row(c, v, sym):
    if v <= 6:
        return "Count the %ss in the %s row: %s." % (sym, c, count_list(v))
    return "Count the %ss in the %s row. There are %d." % (sym, c, v)


def more_fmt(d, unit, word):
    return "%d %s %s" % (d, word, unit[0] if d == 1 else unit[1])


def bundles(b):
    return "1 bundle of 5" if b == 1 else "%d bundles of 5" % b


def count_on(v):
    """Count the bundles by 5s, then count on the single marks: 5, 10, then 11, 12."""
    b, r = divmod(v, 5)
    fives = ", ".join(str(5 * k) for k in range(1, b + 1))
    if not r:
        return "Count by 5s: %s." % fives
    return "Count %s, then %s." % (fives, ", ".join(str(5 * b + k) for k in range(1, r + 1)))


def tally_read(c, v):
    b, r = divmod(v, 5)
    if b == 0:
        return "The %s row has %d mark%s, so it shows %d." % (c, v, "" if v == 1 else "s", v)
    more = (" and %d more mark%s" % (r, "" if r == 1 else "s")) if r else ""
    return "The %s row has %s%s. %s That is %d." % (c, bundles(b), more, count_on(v), v)


def rd_list(cats, vals):
    return ". ".join("%s: %d" % (c, v) for c, v in zip(cats, vals))


# ------------------------------------------------------------ set 1: sort and find the rule
NAMES1 = ["Maya", "Liam", "Zoe", "Owen", "Amira", "Lucas", "Mei", "Ethan", "Priya", "Kai"]


def rand_item(rnd, fixed=None):
    it = [rnd.choice(SHAPES), rnd.choice(COLOURS), rnd.choice(SIZES)]
    for a, v in (fixed or {}).items():
        it[a] = v
    return tuple(it)


def set_sort(rnd):
    its = []
    names = iter(NAMES1 * 3)
    seen = set()

    # --- count after sorting by colour or size (4)
    for i, (attr, v) in enumerate([(1, "red"), (2, "big"), (1, "blue"), (2, "small")]):
        for _ in range(5000):
            n = rnd.randint(8, 11)
            items = [rand_item(rnd) for _ in range(n)]
            want = [it for it in items if it[attr] == v]
            k = len(want)
            if not (3 <= k <= 6) or len(set(items)) < n - 2:
                continue
            # most common shape among the wanted ones (a child who sorts by shape too counts only these)
            shp = max(SHAPES, key=lambda s: sum(1 for it in want if it[0] == s))
            only = sum(1 for it in want if it[0] == shp)
            other_v = [x for x in ATTR_VALS[attr] if x != v]
            rest = n - k if attr == 2 else sum(1 for it in items if it[1] == other_v[0])
            if only >= k or only < 1 or len({k, only, rest, n}) < 4:
                continue
            key = tuple(sorted(items))
            if key not in seen:
                seen.add(key)
                break
        word = "%s shapes" % v
        unit = ("%s shape" % v, word)
        cand = [only, rest, k + 1, k - 1, n]
        q = fig(mixed_svg(items, rnd, label="mixed shapes to sort")) + \
            "Sort by %s. How many %s are there?" % (ATTR_NAME[attr], word)
        e = ("Look only at the %s. Shape does not matter. Touch each %s shape as you count: %s. "
             "There are %s." % (ATTR_NAME[attr], v, count_list(k), fmt(k, unit)))
        its.append(mcq(q, fmt(k, unit), [fmt(x, unit) for x in cand], e))

    # --- where does the new one go? (5)
    used_new = set()
    for i, attr in enumerate([1, 0, 1, 0, 1]):
        other = 1 - attr                      # colour <-> shape
        vals = ATTR_VALS[attr]
        for _ in range(5000):
            new = rand_item(rnd)
            wrong_box = rnd.choice([x for x in vals if x != new[attr]])
            groups = []
            for gv in vals:
                g = []
                for k in range(2):
                    fx = {attr: gv}
                    if gv == wrong_box and k == 0:
                        fx[other] = new[other]          # looks like the new one in the other attribute
                    g.append(rand_item(rnd, fx))
                groups.append(g)
            # only the wrong box shares the other attribute with the new one
            share = [gi for gi, g in enumerate(groups) if any(it[other] == new[other] for it in g)]
            if share != [vals.index(wrong_box)]:
                continue
            if any(new in g for g in groups) or any(g[0] == g[1] for g in groups):
                continue
            if new[0] in used_new or new[1] in used_new:
                continue
            key = ("w", new, tuple(map(tuple, groups)))
            if key not in seen:
                seen.add(key)
                used_new.add(new[attr])
                break
        lab = [cap(val_word(attr, x)) for x in vals]
        nm = next(names)
        q = fig(where_svg(new, list(zip(lab, groups)), "four sorted groups and a new shape")) + \
            "%s sorts by %s. Where does the new shape go?" % (nm, ATTR_NAME[attr])
        right = cap(val_word(attr, new[attr]))
        wb = cap(val_word(attr, wrong_box))
        if attr == 1:
            e = ("The rule is colour. The new shape is %s, so it goes in the %s group. "
                 "It is a %s like one in the %s group, but shape is not the rule." % (new[1], right, new[0], wb))
        else:
            e = ("The rule is shape. The new shape is a %s, so it goes with the %s. "
                 "It is %s like one in the %s group, but colour is not the rule." % (new[0], PL[new[0]], new[1], PL[wrong_box]))
        its.append(mcq(q, right, [wb] + [x for x in lab if x not in (right, wb)], e))

    # --- which one does not belong? (5, A-D fixed)
    for i, (attr, pos) in enumerate([(1, 2), (0, 0), (2, 3), (1, 1), (0, 2)]):
        vals = ATTR_VALS[attr]
        for _ in range(5000):
            v = rnd.choice(vals)
            good = [rand_item(rnd, {attr: v}) for _ in range(3)]
            if len(set(good)) < 3:
                continue
            # the others must differ in the other two attributes, so only the rule is shared
            oth = [a for a in range(3) if a != attr]
            if any(len(set(it[a] for it in good)) < 2 for a in oth):
                continue
            bad_v = rnd.choice([x for x in vals if x != v])
            twin = rnd.choice(good)
            bad = list(twin)
            bad[attr] = bad_v                    # same as one of the good ones except the rule
            bad = tuple(bad)
            items = good[:pos] + [bad] + good[pos:]
            key = ("b", tuple(items))
            if key not in seen:
                seen.add(key)
                break
        rule = "Rule: all " + val_word(attr, v)
        q = fig(belong_svg(rule, items, "four shapes labelled A to D")) + "Which one does not follow the rule?"
        ok = [k for k in range(4) if k != pos]
        e = ("%s are all %s. %s is %s, so it does not belong." %
             (letters(ok), val_word(attr, v), "ABCD"[pos],
              ("a " + bad_v) if attr == 0 else bad_v))
        its.append({"q": q, "c": ["A", "B", "C", "D"], "a": pos, "fixed": True, "e": e})

    # --- what is the rule for the group? (6)
    for i, (attr, gi) in enumerate([(1, 0), (0, 1), (2, 0), (1, 1), (0, 0), (2, 1)]):
        vals = ATTR_VALS[attr]
        oth = [a for a in range(3) if a != attr]
        for _ in range(20000):
            v1, v2 = rnd.sample(vals, 2)
            n1, n2 = rnd.randint(4, 6), rnd.randint(4, 6)
            g1 = [rand_item(rnd, {attr: v1}) for _ in range(n1)]
            g2 = [rand_item(rnd, {attr: v2}) for _ in range(n2)]
            g = [g1, g2][gi]
            # the asked group must be mixed in both other attributes, so only one rule fits
            if any(len(set(it[a] for it in g)) < 2 for a in oth):
                continue
            if any(len(set(it[a] for it in gg)) < 2 for a in oth for gg in (g1, g2)):
                continue
            key = ("r", tuple(g1), tuple(g2))
            if key not in seen:
                seen.add(key)
                break
        mine = [v1, v2][gi]
        theirs = [v2, v1][gi]
        cand = [rule_txt(attr, theirs)]
        for a in oth:
            present = sorted(sorted(set(it[a] for it in g)), key=lambda x: -sum(1 for it in g if it[a] == x))
            cand.append(rule_txt(a, present[0]))
        nm = next(names)
        q = fig(groups_svg([("Group 1", g1), ("Group 2", g2)], "shapes sorted into two groups")) + \
            "%s sorted the shapes. What is the rule for Group %d?" % (nm, gi + 1)
        a1, a2 = oth
        e = ("Look at every shape in Group %d. They are all %s. They are not all the same %s or %s. "
             "Group %d is all %s." % (gi + 1, val_word(attr, mine), ATTR_NAME[a1], ATTR_NAME[a2], 2 - gi,
                                  val_word(attr, theirs)))
        its.append(mcq(q, rule_txt(attr, mine), cand, e))
    return {"title": "Sort and find the rule", "items": its}


# ------------------------------------------------------------ set 2: tally marks
def set_tally(rnd, PK):
    its = []
    plan = ["read"] * 7 + ["pick"] * 3 + ["read"] * 6 + ["which"] * 4
    pick_pos = iter([1, 3, 0])
    used_pick = set()
    for i, kind in enumerate(plan):
        if kind == "pick":
            v = [7, 9, 12][i - 7]
            b, r = divmod(v, 5)
            rows = [("ok", v), ("ok", v - 1), ("ok", v + 1), ("plain", v - b)]       # plain: groups of 4, no line across
            pos = next(pick_pos)
            order = [1, 2, 3]
            rnd.shuffle(order)
            order.insert(pos, 0)
            rows = [rows[k] for k in order]
            unit_ = [("loon", "loons"), ("mitten", "mittens"), ("leaf", "leaves")][i - 7]
            plain_k = order.index(3)
            q = fig(tally4_svg(rows)) + "Which tally shows %s?" % fmt(v, unit_)
            e = ("4 marks with a line across make a bundle of 5. %d is %s%s. "
                 "Row %s has no line across, so it shows only %d marks."
                 % (v, bundles(b), (" and %d more mark%s" % (r, "" if r == 1 else "s")) if r else "",
                    "ABCD"[plain_k], v - b))
            its.append({"q": q, "c": ["A", "B", "C", "D"], "a": pos, "fixed": True, "e": e})
            continue
        hard = i >= 10
        ctx = PK.next(lambda c: not (c.sumto and hard))
        U = ctx.unit
        if kind == "read":
            for _ in range(200):
                cats, vals = make_data(ctx, rnd, 2, 14 if hard else 9,
                                       ok=lambda v: any(x >= 6 and x % 5 for x in v) and (not hard or max(v) >= 10))
                good = [k for k in range(3) if vals[k] >= 6 and vals[k] % 5]
                if hard:
                    good = [k for k in good if vals[k] >= 10] or good
                j = rnd.choice(good)
                if vals[j] not in used_pick or len(used_pick) > 9:
                    break
            c, v = cats[j], vals[j]
            used_pick.add(v)
            b, r = divmod(v, 5)
            nb = [vals[k] for k in (j - 1, j + 1) if 0 <= k < 3]          # read the row above or below
            cand = [v - b, v + b] + nb + [b + r, v + 1, v - 1]               # bundle as 4 / as 6 / bundle as 1
            e = "4 marks with a line across is 5. %s" % tally_read(c, v)
            its.append(mcq(fig(ctx_tally(ctx, cats, vals)) + ctx.q("ask", c), fmt(v, U), [fmt(x, U) for x in cand], e))
        else:
            cats, vals = make_data(ctx, rnd, 3, 14, ok=lambda v: max(v) >= 10 and min(v) >= 4)
            j = rnd.choice([k for k in range(3) if vals[k] >= 6])
            v = vals[j]
            close = sorted([k for k in range(3) if k != j], key=lambda k: abs(vals[k] - v))
            spare = [x for x in ctx.cats if x not in cats]
            its.append(mcq(fig(ctx_tally(ctx, cats, vals)) + ctx.q("which", v=v), cats[j], [cats[k] for k in close] + spare,
                           "Read every row. %s. %s" % (rd_list(cats, vals), tally_read(cats[j], v))))
    return {"title": "Tally marks: bundles of 5", "items": its}


# ------------------------------------------------------------ set 3: pictographs
def set_picture(rnd, PK):
    its = []
    plan = ["read"] * 7 + ["title", "source"] + ["which"] * 4 + ["read4"] * 4 + ["source4"] + ["which4"] * 2
    asked = set()
    pos3 = iter([0, 2, 1, 2, 1, 0, 2])
    pos4 = iter([1, 3, 0, 2])
    for i, kind in enumerate(plan):
        n = 4 if kind.endswith("4") else 3
        ctx = PK.next(lambda c: not (n == 4 and c.sumto))
        U = ctx.unit
        sym = SYMS[i % 4]
        hi = 6 if i < 4 else 9
        j = next(pos3) if kind == "read" else next(pos4) if kind == "read4" else None
        for _ in range(500):
            cats, vals = make_data(ctx, rnd, 1, hi, n=n, ok=lambda v: max(v) >= 3)
            if j is None or (ctx.title, cats[j]) not in asked:
                break
        if j is not None:
            asked.add((ctx.title, cats[j]))
        f = fig(ctx_pic(ctx, cats, vals, sym))
        spare = [x for x in ctx.cats if x not in cats]
        if kind.startswith("read"):
            c, v = cats[j], vals[j]
            nb = [vals[k] for k in (j - 1, j + 1) if 0 <= k < n]          # read the row above or below
            others = [vals[k] for k in range(n) if k != j]
            its.append(mcq(f + ctx.q("ask", c), fmt(v, U), [fmt(x, U) for x in nb + [v + 1, v - 1] + others + [sum(vals), v + 2]],
                           "Each %s stands for 1. %s So the answer is %s." % (sym, count_row(c, v, sym), fmt(v, U))))
        elif kind == "title":
            src = cap(ctx.source.replace("Source: ", ""))
            its.append(mcq(f + "What is the title of this pictograph?", ctx.title, [ctx.axis, src, cats[0]],
                           "The title is at the top. It tells what the graph is about: %s." % ctx.title.lower()))
        elif kind.startswith("source"):
            src = cap(ctx.source.replace("Source: ", ""))
            its.append(mcq(f + "Where did the data come from?", src, [ctx.title, ctx.axis, cats[1]],
                           "The source is under the graph. It tells where the data came from: %s." % ctx.source.replace("Source: ", "")))
        else:
            j = rnd.choice([k for k in range(n) if vals[k] >= 2])
            v = vals[j]
            close = sorted([k for k in range(n) if k != j], key=lambda k: abs(vals[k] - v))
            its.append(mcq(f + ctx.q("which", v=v), cats[j], [cats[k] for k in close] + spare,
                           "Look for the row with %d %ss. %s" % (v, sym, count_row(cats[j], v, sym))))
    return {"title": "Pictographs: 1 picture = 1", "items": its}


# ------------------------------------------------------------ set 4: order from greatest to least
def set_order(rnd, PK):
    its = []
    plan = [("pic", "most"), ("tally", "fewest"), ("pic", "fewest"), ("tally", "most"),
            ("pic", "down"), ("tally", "down"), ("pic", "down"), ("tally", "up"),
            ("pic", "down"), ("tally", "down"), ("pic", "up"), ("tally", "down"),
            ("pic", "up"), ("tally", "down"), ("pic", "down"), ("tally", "up"),
            ("pic4", "down"), ("tally4", "down"), ("pic4", "up"), ("tally4", "down")]
    seen = set()
    for i, (style, kind) in enumerate(plan):
        sym = SYMS[i % 4]
        n = 4 if style.endswith("4") else 3
        ctx = PK.next(lambda c: c.has("most") and not (n == 4 and c.sumto))
        hi = 9 if style.startswith("pic") else 12
        for _ in range(500):
            if kind in ("most", "fewest"):
                cats, vals = make_data(ctx, rnd, 2, hi, n=n,
                                       ok=lambda v: sorted(v)[-1] - sorted(v)[-2] <= 2 and sorted(v)[1] - sorted(v)[0] <= 2)
            else:
                # the rows must not already be in the asked order, so reading top to bottom is a real mistake
                cats, vals = make_data(ctx, rnd, 1 if n == 4 else 2, hi, n=n,
                                       ok=lambda v: v != sorted(v) and v != sorted(v, reverse=True)
                                       and sorted(v)[-1] - sorted(v)[0] >= 3)
            if (ctx.title, tuple(vals)) not in seen:
                break
        seen.add((ctx.title, tuple(vals)))
        if style.startswith("pic"):
            f, how = fig(ctx_pic(ctx, cats, vals, sym)), "Count the %ss in each row." % sym
        else:
            f, how = fig(ctx_tally(ctx, cats, vals)), "Count the tally marks in each row. A bundle is 5."
        if kind in ("down", "up"):
            o = sorted(range(n), key=lambda k: -vals[k])
            want = o if kind == "down" else o[::-1]
            nm = lambda ks: ", ".join(cats[k] for k in ks)
            swaps = []
            for a in range(n - 1):
                w2 = want[:]
                w2[a], w2[a + 1] = w2[a + 1], w2[a]
                swaps.append(w2)
            swaps.sort(key=lambda w2: abs(vals[w2[0]] - vals[w2[1]]) if w2 != want else 99)
            cand = [nm(want[::-1]), nm(list(range(n)))] + [nm(w2) for w2 in swaps]   # backwards / as listed / two swapped
            words = ("greatest to least", "Greatest", "Least") if kind == "down" else ("least to greatest", "Least", "Greatest")
            mid = " ".join("Next: %s (%d)." % (cats[k], vals[k]) for k in want[1:-1])
            its.append(mcq(f + "Put them in order from %s." % words[0], nm(want), cand,
                           "%s %s. %s: %s (%d). %s %s: %s (%d)."
                           % (how, rd_list(cats, vals), words[1], cats[want[0]], vals[want[0]],
                              mid, words[2], cats[want[-1]], vals[want[-1]])))
        else:
            j = vals.index(max(vals) if kind == "most" else min(vals))
            order = sorted([k for k in range(n) if k != j], key=lambda k: abs(vals[k] - vals[j]))
            spare = [x for x in ctx.cats if x not in cats]
            its.append(mcq(f + ctx.q("most", w=kind), cats[j], [cats[k] for k in order] + spare,
                           "%s %s. %d is the %s number. The answer is %s."
                           % (how, rd_list(cats, vals), vals[j], "greatest" if kind == "most" else "least",
                              cats[j])))
    return {"title": "Order from greatest to least", "items": its}


# ------------------------------------------------------------ set 5: compare and answer questions
def set_word(rnd, PK):
    its = []
    plan = ["more", "both", "more", "fewer", "total", "more", "both", "fewer", "more", "tie",
            "fewer", "more", "total", "both", "tie", "more", "fewer", "total", "tie", "more"]
    asked = set()
    fruit, school = BYTITLE["Favourite fruit"], BYTITLE["How we get to school"]
    seen = set()
    for i, kind in enumerate(plan):
        if i % 3 == 0:
            ctx = fruit
        elif i % 3 == 1:
            ctx = school
        else:
            ctx = PK.next(lambda c: c.has(kind) and c not in (fruit, school))
        if not ctx.has(kind):
            kind = "more"
        U = ctx.unit
        style = i % 2                       # 0 pictograph, 1 tally
        hi = 9 if style == 0 else 12
        for _ in range(500):
            if kind in ("more", "fewer", "tie"):
                cats, vals = make_data(ctx, rnd, 1, hi, ok=lambda v: sorted(v)[2] - sorted(v)[0] >= 3)
            else:
                cats, vals = make_data(ctx, rnd, 2, hi)
            if (ctx.title, tuple(vals)) not in seen:
                break
        seen.add((ctx.title, tuple(vals)))
        sym = SYMS[i % 4]
        if style == 0:
            f, how = fig(ctx_pic(ctx, cats, vals, sym)), "Count the %ss. Each one is 1." % sym
        else:
            f, how = fig(ctx_tally(ctx, cats, vals)), "Count the tally marks. A bundle is 5."
        intro = INTRO[ctx.title] + " "
        rd = lambda k: "%s: %d." % (cats[k], vals[k])
        if kind in ("more", "fewer", "tie"):
            for _ in range(200):
                a, b = sorted(rnd.sample(range(3), 2), key=lambda k: -vals[k])
                if vals[a] - vals[b] >= 2 and (ctx.title, kind, cats[a], cats[b]) not in asked:
                    break
            asked.add((ctx.title, kind, cats[a], cats[b]))
            va, vb = vals[a], vals[b]
            d = va - vb
            if kind == "more":
                q = ctx.q("more", cats[a], cats[b])
            elif kind == "fewer":
                q = ctx.q("fewer", cats[b], cats[a])
            else:
                q = ctx.q("tie", cats[a], cats[b])
            cand = [va + vb, va, vb, d + 1, d - 1]                       # added / read one row / off by one
            word = "fewer" if kind == "fewer" else "more"
            if kind == "tie":
                e = ("%s %s %s %s needs to go from %d up to %d. Count on from %d to %d, or %s. So %s needs %s."
                     % (how, rd(a), rd(b), cats[b], vb, va, vb, va, minus(va, vb), cats[b], more_fmt(d, U, "more")))
            else:
                e = ("%s %s %s Match them up one to one. %d are left over: %s. The answer is %s."
                     % (how, rd(a), rd(b), d, minus(va, vb), more_fmt(d, U, word)))
            its.append(mcq(f + intro + q, fmt(d, U), [fmt(x, U) for x in cand], e))
        elif kind == "both":
            for _ in range(200):
                a, b = sorted(rnd.sample(range(3), 2))
                if (ctx.title, kind, frozenset((cats[a], cats[b]))) not in asked:
                    break
            asked.add((ctx.title, kind, frozenset((cats[a], cats[b]))))
            va, vb = vals[a], vals[b]
            t = va + vb
            cand = [abs(va - vb), t + 1, t - 1, max(va, vb), sum(vals)]
            its.append(mcq(f + intro + ctx.q("both", cats[a], cats[b]), fmt(t, U), [fmt(x, U) for x in cand],
                           "%s %s %s Add the two rows: %d + %d = %s." % (how, rd(a), rd(b), va, vb, fmt(t, U))))
        else:
            t = sum(vals)
            cand = [3, t - min(vals), t + 1, t - 1, max(vals)]
            its.append(mcq(f + intro + ctx.q("total"), fmt(t, U), [fmt(x, U) for x in cand],
                           "%s %s Add all three rows: %s = %s. (There are 3 rows, but the answer is the number of %s.)"
                           % (how, " ".join(rd(k) for k in range(3)), plus(vals), fmt(t, U), U[1])))
    return {"title": "Compare and answer questions: word problems", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


L_G1 = [("circle", "red", "big"), ("star", "red", "small"), ("square", "red", "big"), ("triangle", "red", "small")]
L_G2 = [("triangle", "blue", "big"), ("circle", "blue", "small"), ("star", "blue", "big"), ("square", "blue", "small")]
L_CATS = ["Apple", "Banana", "Grapes"]
L_VALS = [7, 3, 5]
L_TV = [7, 3, 12]


def body_html():
    fr = BYTITLE["Favourite fruit"]
    return (
        "<h2>The big idea</h2>"
        "<p><b>Data</b> is information we collect, like votes in a class survey. "
        "First we <b>sort</b> things into groups. Then we <b>count</b> each group with <b>tally marks</b>. "
        "Then we <b>show</b> the data in a <b>pictograph</b>. Last, we ask what the graph tells us.</p>"
        "<h2>Sort and name the rule</h2>"
        "<p>A <b>sorting rule</b> tells how things go together. We can sort by <b>colour</b>, by <b>shape</b> "
        "or by <b>size</b>. To find the rule, look at every thing in one group. What is the same for all of them?</p>"
        "<figure class='sn-fig'>" + groups_svg([("Group 1", L_G1), ("Group 2", L_G2)], "shapes sorted by colour") +
        "<figcaption>Group 1 is all red. Group 2 is all blue. The shapes and sizes are mixed, so the rule is colour.</figcaption></figure>"
        "<h2>Tally marks: bundles of 5</h2>"
        "<p>Make one mark for each thing. The 5th mark goes <b>across</b> the first 4. "
        "That makes a <b>bundle of 5</b>. To read a tally, count the bundles by 5s, then count on the single marks.</p>"
        "<figure class='sn-fig'>" + ctx_tally(fr, L_CATS, L_TV) +
        "<figcaption>Apple: 1 bundle and 2 marks. Count 5, then 6, 7. That is 7 votes. "
        "Grapes: 2 bundles and 2 marks. Count 5, 10, then 11, 12. That is 12 votes.</figcaption></figure>"
        "<h2>Pictographs: 1 picture = 1</h2>"
        "<p>In a Grade 1 pictograph, <b>one picture stands for one</b> thing. "
        "A good graph has a <b>title</b> at the top, <b>labels</b> for the rows, a <b>key</b>, "
        "and a <b>source</b> that tells where the data came from. "
        "Put your finger on the label. Then count the pictures in that row only.</p>"
        "<figure class='sn-fig'>" + ctx_pic(fr, L_CATS, L_VALS, "star") +
        "<figcaption>The Grapes row has 5 stars, so Grapes got 5 votes. The data came from Ms. Lee’s class vote.</figcaption></figure>"
        "<h2>Order from greatest to least</h2>"
        "<p>The <b>greatest</b> number is the longest row. The <b>least</b> number is the shortest row. "
        "Find the greatest first, then the next, then the least.</p>" +
        ex("Greatest to least", "Apple 7, Banana 3, Grapes 5. Put them in order from greatest to least.",
           "7 is the greatest. 5 is next. 3 is the least.", "Apple, Grapes, Banana") +
        "<h2>Compare and answer questions</h2>"
        "<p><b>How many more</b> or <b>how many fewer</b> means compare. Match the pictures one to one, "
        "or take the smaller number away from the bigger one. <b>Altogether</b> means add.</p>" +
        ex("How many more?", "How many more votes did Apple get than Grapes?",
           "Apple 7, Grapes 5. 2 stars are left over. 7 %s 5 = 2." % MINUS, "2 more votes") +
        ex("How many altogether?", "How many votes were there altogether?",
           "Apple 7, Banana 3, Grapes 5. 7 + 3 + 5 = 15.", "15 votes") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Naming a rule that fits only some things", "Check every thing in the group"],
            ["Counting a bundle of tally marks as 4", "4 marks and 1 line across is 5"],
            ["Reading the row above or below", "Put your finger on the label first, then read that row"],
            ["Writing the order backwards", "Greatest to least starts with the longest row"],
            ["Adding when it asks how many more", "How many more or fewer means compare, so subtract"],
            ["Mixing up the title and the source", "The title is at the top; the source is at the bottom"],
        ])
    )


FAQ = [
    {"q": "What do Grade 1 students learn about data in the Ontario math curriculum?",
     "a": "They sort things by one attribute and name the sorting rule, collect data with tally marks, and show it in concrete graphs and pictographs where one picture stands for one. They also order the categories from greatest to least and answer questions about the data."},
    {"q": "How do you teach tally marks in Grade 1?",
     "a": "Make one mark for each thing, and draw the 5th mark across the first 4 to make a bundle of 5. To read a tally, count the bundles by 5s and then count on the single marks, so 1 bundle and 2 marks is 7."},
    {"q": "What is a pictograph in Grade 1 math?",
     "a": "It is a graph that uses pictures, with one picture for each thing (one-to-one correspondence). A complete pictograph has a title, labels, a key and a source that says where the data came from."},
    {"q": "How can I practise sorting and graphing with my Grade 1 child at home?",
     "a": "Sort laundry, toys or snacks and ask “What is your rule?” Then ask the family a question, such as their favourite fruit, keep a tally, and ask which got the most and how many more."},
]


def gen_unit():
    rnd = random.Random(41809)
    PK = Picker(rnd)
    sets = [set_sort(rnd), set_tally(rnd, PK), set_picture(rnd, PK), set_order(rnd, PK), set_word(rnd, PK)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        pos = [it["a"] for it in s["items"]]
        assert all(pos.count(p) == 5 for p in range(4)), (s["title"], pos)
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["e"], it
            assert it["q"].count("<svg") == 1, it["q"][:80]
            k = it["q"] + "|" + "|".join(sorted(it["c"]))
            assert k not in seen, it["q"]
            seen.add(k)
    return {
        "country": "ca-on", "subject": "math", "grade": "grade-1", "slug": "sorting-and-graphs", "sort": 9,
        "updated": UPDATED, "pdf_url": "",
        "title": "Sorting and Graphs: Sorting Rules, Tally Marks and Pictographs",
        "seo_title": "Grade 1 Sorting and Graphs Worksheets: Tally Marks and Pictographs (Free, Answer Key, Ontario)",
        "short_title": "Sorting and graphs",
        "domain": "Data",
        "standard_code": "Grade 1: D1.3",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Display sets of data, using one-to-one correspondence, in concrete graphs and pictographs with proper sources, titles, and labels",
        "meta_desc": "Free Grade 1 math worksheets on sorting and graphs for the Ontario curriculum: sort by colour, shape or size and name the rule, read tally marks in bundles of 5, read pictographs where 1 picture = 1, order from greatest to least, and compare. 100 questions with an answer key.",
        "key_big": "Sort it, count it, show it, then ask what it tells you.",
        "key_sub": "A sorting rule must fit every thing in the group. A tally bundle is 5. In a Grade 1 pictograph, 1 picture = 1. How many more means compare; altogether means add.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


def mark_large(u, pattern):
    """Tag pictures that must print larger (graphs, tally charts, sorted groups, A-D choices) so their labels stay readable."""
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
        mark_large(u, "(pictograph|tally chart|four tally rows|four sorted groups|shapes sorted into|four shapes labelled|mixed shapes)")
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
