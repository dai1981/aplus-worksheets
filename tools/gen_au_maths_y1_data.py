# -*- coding: utf-8 -*-
"""
AU Year 1 Maths: Data and tally marks (Australian Curriculum v9.0, AC9M1ST01 and AC9M1ST02)
  python3 tools/gen_au_maths_y1_data.py
Three or four categories, counts up to 14, totals up to 20. Sort and count, tally marks
(bundles of 5), picture graphs (one picture for each), most and fewest, how many more.
Every answer is checked in code. HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, re, math, os, random

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "au", "maths", "year-1")
UPDATED = "2026-11-02"
GREEN = "#006633"
RED = "#c0392b"
INK = "#2b2b2b"
GRID = "#c9d3cc"
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


# ------------------------------------------------------------ symbols / shapes
def star_pts(cx, cy, R=9.5, r=4.0):
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rad = R if i % 2 == 0 else r
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    return pts


def symbol(kind, cx, cy, col=GREEN, k=1.0):
    """Small shape centred on (cx, cy). k scales it."""
    if kind == "circle":
        return "<circle cx='%.1f' cy='%.1f' r='%.1f' fill='%s'/>" % (cx, cy, 8.5 * k, col)
    if kind == "square":
        h = 7.5 * k
        return "<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' rx='2' fill='%s'/>" % (cx - h, cy - h, 2 * h, 2 * h, col)
    if kind == "triangle":
        h = 9.5 * k
        return "<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='%s'/>" % (
            cx, cy - h, cx + h, cy + h * 0.8, cx - h, cy + h * 0.8, col)
    if kind == "heart":
        return ("<path d='M%.1f %.1f C%.1f %.1f %.1f %.1f %.1f %.1f C%.1f %.1f %.1f %.1f %.1f %.1f Z' fill='%s'/>"
                % (cx, cy + 8 * k, cx - 12 * k, cy - 1 * k, cx - 6 * k, cy - 11 * k, cx, cy - 4 * k,
                   cx + 6 * k, cy - 11 * k, cx + 12 * k, cy - 1 * k, cx, cy + 8 * k, col))
    return "<polygon points='%s' fill='%s'/>" % (" ".join("%.1f,%.1f" % p for p in star_pts(cx, cy, 9.5 * k, 4.0 * k)), col)


SYMS = ["circle", "star", "square", "heart"]
SHAPES = ["circle", "square", "triangle", "star", "heart"]
SHAPE_COL = {"circle": "#2e8b57", "square": "#2e6fb0", "triangle": "#d9822b", "star": "#c9a227", "heart": "#c0392b"}
SHAPE_PL = {s: s + "s" for s in SHAPES}


def mixed_svg(kinds, vals, rnd, label="mixed shapes to sort", cols=6):
    """Shapes scattered (one per cell, small jitter) so they must be sorted before counting."""
    n = sum(vals)
    rows = int(math.ceil(n / float(cols)))
    if rows * cols - n < 2:
        rows += 1
    cells = rnd.sample(range(rows * cols), n)
    items = []
    for kd, v in zip(kinds, vals):
        items += [kd] * v
    rnd.shuffle(items)
    cw = 36
    W, H = cols * cw + 8, rows * cw + 8
    s = ["<rect x='1' y='1' width='%d' height='%d' rx='8' fill='#f6faf7' stroke='%s' stroke-width='1.5'/>" % (W - 2, H - 2, GRID)]
    for kd, c in zip(items, cells):
        r, cc = divmod(c, cols)
        cx = 4 + cc * cw + cw / 2 + rnd.choice([-3, -1, 0, 1, 3])
        cy = 4 + r * cw + cw / 2 + rnd.choice([-3, -1, 0, 1, 3])
        s.append(symbol(kd, cx, cy, SHAPE_COL[kd], 1.15))
    return svg_wrap(W, H, "".join(s), label)


# ------------------------------------------------------------ contexts
class Ctx:
    def __init__(self, title, axis, cats, unit, f, ph=None, sumto=None, names=False):
        self.title, self.axis, self.cats, self.unit = title, axis, cats, unit
        self.f, self.ph, self.sumto, self.names = f, ph or {}, sumto, names

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
            "tie": "How many more votes does {b} need to have as many as {a}?",
            "most": "Which %s got the {w} votes?" % word,
            "which": "Which %s got {n}?" % word}


def person_f(verb, past, noun):
    return {"ask": "How many %s did {a} %s?" % (noun, verb),
            "more": "How many more %s did {a} %s than {b}?" % (noun, verb),
            "fewer": "How many fewer %s did {a} %s than {b}?" % (noun, verb),
            "both": "How many %s did {a} and {b} %s altogether?" % (noun, verb),
            "total": "How many %s did they %s altogether?" % (noun, verb),
            "tie": "How many more %s does {b} need to %s to have as many as {a}?" % (noun, verb),
            "most": "Who %s the {w} %s?" % (past, noun),
            "which": "Who %s {n}?" % past}


CTXS = [
    Ctx("Favourite Fruit", "Fruit", ["Apple", "Banana", "Mango", "Orange"], VOTE, votes_f("fruit")),
    Ctx("Favourite Colour", "Colour", ["Red", "Blue", "Green", "Yellow"], VOTE, votes_f("colour")),
    Ctx("Favourite Ice-Cream", "Flavour", ["Vanilla", "Mint", "Berry", "Lemon"], VOTE, votes_f("flavour")),
    Ctx("Our Pets", "Pet", ["Dog", "Cat", "Fish", "Bird"], KID,
        {"ask": "How many students have a {a}?",
         "more": "How many more students have a {a} than a {b}?",
         "fewer": "How many fewer students have a {a} than a {b}?",
         "both": "How many students have a {a} or a {b}?",
         "total": "How many students are shown altogether?",
         "most": "Which pet do the {w} students have?",
         "which": "Which pet do {n} have?"}, ph=LOWER(["Dog", "Cat", "Fish", "Bird"])),
    Ctx("How We Get to School", "Way", ["Bus", "Car", "Walk", "Bike"], KID,
        {"ask": "How many students {a} to school?",
         "more": "How many more students {a} than {b}?",
         "fewer": "How many fewer students {a} than {b}?",
         "both": "How many students {a} or {b}?",
         "total": "How many students are shown altogether?",
         "most": "Which way do the {w} students get to school?",
         "which": "Which way do {n} get to school?"},
        ph={"Bus": "catch the bus", "Car": "come by car", "Walk": "walk", "Bike": "ride a bike"}),
    Ctx("Favourite Snack", "Snack", ["Popcorn", "Grapes", "Crackers", "Yoghurt"], KID,
        {"ask": "How many students chose {a}?",
         "more": "How many more students chose {a} than {b}?",
         "fewer": "How many fewer students chose {a} than {b}?",
         "both": "How many students chose {a} or {b}?",
         "total": "How many students voted altogether?",
         "tie": "How many more students need to choose {b} to match {a}?",
         "most": "Which snack did the {w} students choose?",
         "which": "Which snack did {n} choose?"}, ph=LOWER(["Popcorn", "Grapes", "Crackers", "Yoghurt"])),
    Ctx("What We Play at Recess", "Game", ["Swings", "Slide", "Tag", "Skipping"], KID,
        {"ask": "How many students picked {a}?",
         "more": "How many more students picked {a} than {b}?",
         "fewer": "How many fewer students picked {a} than {b}?",
         "both": "How many students picked {a} or {b}?",
         "total": "How many students are shown altogether?",
         "most": "Which one did the {w} students pick?",
         "which": "Which one did {n} pick?"},
        ph={"Swings": "the swings", "Slide": "the slide", "Tag": "tag", "Skipping": "skipping"}),
    Ctx("Weather for 2 Weeks", "Weather", ["Sunny", "Cloudy", "Rainy", "Windy"], ("day", "days"),
        {"ask": "How many days were {a}?",
         "more": "How many more days were {a} than {b}?",
         "fewer": "How many fewer days were {a} than {b}?",
         "both": "How many days were {a} or {b}?",
         "total": "How many days are shown altogether?",
         "most": "Which weather had the {w} days?",
         "which": "Which weather had {n}?"}, ph=LOWER(["Sunny", "Cloudy", "Rainy", "Windy"]), sumto=14),
    Ctx("Toys in the Box", "Toy", ["Balls", "Cars", "Blocks", "Dolls"], ("toy", "toys"),
        {"ask": "How many {a} are in the box?",
         "more": "How many more {a} than {b} are in the box?",
         "fewer": "How many fewer {a} than {b} are in the box?",
         "both": "How many {a} and {b} are there altogether?",
         "total": "How many toys are in the box?",
         "most": "Which toy is there the {w} of?",
         "which": "Which toy has {v} in the box?"}, ph=LOWER(["Balls", "Cars", "Blocks", "Dolls"])),
    Ctx("Minibeasts We Saw", "Minibeast", ["Ants", "Bees", "Snails", "Beetles"], ("minibeast", "minibeasts"),
        {"ask": "How many {a} did we see?",
         "more": "How many more {a} than {b} did we see?",
         "fewer": "How many fewer {a} than {b} did we see?",
         "both": "How many {a} and {b} did we see altogether?",
         "total": "How many minibeasts did we see altogether?",
         "most": "Which minibeast did we see the {w} of?",
         "which": "Which minibeast did we see {v} of?"}, ph=LOWER(["Ants", "Bees", "Snails", "Beetles"])),
    Ctx("Birds in the Park", "Bird", ["Magpie", "Galah", "Kookaburra", "Lorikeet"], ("bird", "birds"),
        {"ask": "How many {a} did we see?",
         "more": "How many more {a} than {b} did we see?",
         "fewer": "How many fewer {a} than {b} did we see?",
         "both": "How many {a} and {b} did we see altogether?",
         "total": "How many birds did we see altogether?",
         "most": "Which bird did we see the {w} of?",
         "which": "Which bird did we see {v} of?"},
        ph={"Magpie": "magpies", "Galah": "galahs", "Kookaburra": "kookaburras", "Lorikeet": "lorikeets"}),
    Ctx("Shells We Found", "Name", ["Mia", "Leo", "Isla", "Jack"], ("shell", "shells"),
        person_f("find", "found", "shells"), names=True),
    Ctx("Books We Read", "Name", ["Ruby", "Noah", "Zara", "Kai"], ("book", "books"),
        person_f("read", "read", "books"), names=True),
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


def make_data(ctx, rnd, lo=1, hi=9, ok=lambda v: True, n=3, tmax=20):
    """n categories with n different whole-number values, total at most tmax."""
    for _ in range(20000):
        cats = rnd.sample(ctx.cats, n)
        vals = [rnd.randint(lo, hi) for _ in range(n)]
        if len(set(vals)) != n or sum(vals) > tmax:
            continue
        if ctx.sumto and sum(vals) != ctx.sumto:
            continue
        if ok(vals):
            return cats, vals
    raise ValueError("no data for " + ctx.title)

# ------------------------------------------------------------ graphs
def pic_svg(title, cats, vals, sym, unit, label="picture graph"):
    """Picture graph: one row per category, each picture = 1, key line at the bottom."""
    fs, rh, gap = 15, 26, 23
    lw = max(tw(c, fs) for c in cats) * 1.1 + 24
    m = max(max(vals), 5)
    W = lw + 12 + m * gap + 6
    keytxt = "= " + fmt(1, unit)
    kw = tw("Key:", fs, True) + 32 + tw(keytxt, fs)
    W = int(math.ceil(max(W, tw(title, 16, True) + 16, kw + 16)))
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
        for j in range(v):
            s.append(symbol(sym, lw + 12 + j * gap + 9, y + rh / 2))
    ky = top + H_tab + 22
    x = (W - kw) / 2
    s.append(text(x, ky, "Key:", fs, anchor="start", bold=True))
    x += tw("Key:", fs, True) + 16
    s.append(symbol(sym, x, ky - 5))
    s.append(text(x + 14, ky, keytxt, fs, anchor="start"))
    H = ky + 8
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


def tally_svg(title, axis, cats, vals, label="tally chart"):
    fs, rh = 15, 28
    lw = max(max(tw(c, fs) for c in cats), tw(axis, fs, True)) * 1.1 + 24
    groups = max(math.ceil(v / 5.0) for v in vals)
    tw_ = max(groups * 36 + 4, tw("Tally", fs, True) + 20)
    W = int(math.ceil(max(lw + tw_ + 16, tw(title, 16, True) + 16)))
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
    H = top + rows * rh + 6
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
    return pic_svg(ctx.title, cats, vals, sym, ctx.unit, label="picture graph: " + ctx.title.lower())


def ctx_tally(ctx, cats, vals):
    return tally_svg(ctx.title, ctx.axis, cats, vals, label="tally chart: " + ctx.title.lower())


# ------------------------------------------------------------ reading text (explanations)
def count_list(v):
    return ", ".join(str(k) for k in range(1, v + 1))


def count_row(c, v, sym):
    if v <= 6:
        return "Count the %ss in the %s row: %s." % (sym, c, count_list(v))
    return "Count the %ss in the %s row. There are %d." % (sym, c, v)


def more_fmt(d, unit, word):
    return "%d %s %s" % (d, word, unit[0] if d == 1 else unit[1])


def word_list(names):
    return ", ".join(names[:-1]) + " and " + names[-1]


INTRO = {
    "Favourite Fruit": "Class 1B voted for a favourite fruit.",
    "Favourite Colour": "Class 1G voted for a favourite colour.",
    "Favourite Ice-Cream": "Year 1 voted for an ice-cream flavour.",
    "Our Pets": "Some students told us about their pets.",
    "How We Get to School": "We asked how students get to school.",
    "Favourite Snack": "Students chose a snack for the class party.",
    "What We Play at Recess": "Students picked a game for recess.",
    "Weather for 2 Weeks": "We kept a weather chart for 2 weeks.",
    "Toys in the Box": "We sorted the toys in the box.",
    "Minibeasts We Saw": "We went on a minibeast hunt.",
    "Birds in the Park": "We counted birds in the park.",
    "Shells We Found": "Some friends found shells at the beach.",
    "Books We Read": "Some friends counted the books they read.",
}


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


# ------------------------------------------------------------ set 1: sort and count
def set_sort(rnd):
    its = []
    plan = ["count"] * 10 + ["which"] * 4 + ["most"] * 2 + ["fewest"] * 1 + ["all"] * 3
    seen_data = set()
    last_ans = []
    used_v = set()
    for i, kind in enumerate(plan):
        for _ in range(1000):
            kinds = rnd.sample(SHAPES, 3)
            lo, hi = (1, 6) if i < 5 else (2, 7)
            vals = [rnd.randint(lo, hi) for _ in range(3)]
            key = tuple(sorted(zip(kinds, vals)))
            if kind == "all" and sum(vals) != [11, 13, 15][i - 17]:
                continue
            if kind != "all":
                j_ = vals.index(max(vals)) if kind == "most" else vals.index(min(vals)) if kind == "fewest" else i % 3
                if kinds[j_] in last_ans or (kind == "which" and vals[j_] in used_v):
                    continue
            if len(set(vals)) == 3 and sum(vals) <= 15 and key not in seen_data:
                seen_data.add(key)
                break
        f = fig(mixed_svg(kinds, vals, rnd))
        pl = [SHAPE_PL[k] for k in kinds]
        t = sum(vals)
        tip = "Sort the shapes into groups. Touch each one as you count it."
        if kind == "count":
            j = i % 3
            v = vals[j]
            last_ans = [kinds[j]]
            others = [vals[k] for k in range(3) if k != j]
            its.append(mcq(f + "How many %s are there?" % pl[j], fmt(v, (kinds[j], pl[j])),
                           [fmt(x, (kinds[j], pl[j])) for x in [v + 1, v - 1] + others + [t, v + 2]],
                           "%s Count the %s: %s. There %s %s." % (tip, pl[j], count_list(v),
                                                                  "is" if v == 1 else "are", fmt(v, (kinds[j], pl[j])))))
        elif kind == "which":
            j = i % 3
            v = vals[j]
            used_v.add(v)
            order = sorted([k for k in range(3) if k != j], key=lambda k: abs(vals[k] - v))
            other = [s for s in SHAPES if s not in kinds][0]
            last_ans = [kinds[j]]
            its.append(mcq(f + "Sort the shapes. Which group has %d?" % v, cap(pl[j]),
                           [cap(pl[k]) for k in order] + [cap(SHAPE_PL[other])],
                           "%s %s." % (tip, ". ".join("%s: %d" % (cap(pl[k]), vals[k]) for k in range(3)))
                           + " The %s group has %d." % (kinds[j], v)))
        elif kind in ("most", "fewest"):
            j = vals.index(max(vals) if kind == "most" else min(vals))
            last_ans = [kinds[j]]
            other = [s for s in SHAPES if s not in kinds][0]
            order = sorted([k for k in range(3) if k != j], key=lambda k: abs(vals[k] - vals[j]))
            its.append(mcq(f + "Which shape is there the %s of?" % kind, cap(pl[j]),
                           [cap(pl[k]) for k in order] + [cap(SHAPE_PL[other])],
                           "%s %s. %d is the %s number, so there are the %s %s."
                           % (tip, ". ".join("%s: %d" % (cap(pl[k]), vals[k]) for k in range(3)),
                              vals[j], "biggest" if kind == "most" else "smallest", kind, pl[j])))
        else:
            cand = [3, t + 1, t - 1, t - min(vals), max(vals)]          # counted the groups / missed a group
            its.append(mcq(f + "How many shapes are there altogether?", "%d shapes" % t, ["%d shapes" % x for x in cand],
                           "Count each group: %s. Then add: %s = %d. (There are 3 groups, but the question asks for shapes.)"
                           % (", ".join("%d %s" % (vals[k], pl[k] if vals[k] > 1 else kinds[k]) for k in range(3)),
                              plus(vals), t)))
    return {"title": "Sort and count", "items": its}


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
            unit_ = [("car", "cars"), ("dog", "dogs"), ("leaf", "leaves")][i - 7]
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
            cand = [v - b, v + b] + nb + [b + r, v + 1, v - 1]               # missed the line / counted it twice / bundle as 1
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


# ------------------------------------------------------------ set 3: picture graphs
def set_picture(rnd, PK):
    its = []
    plan = ["read"] * 8 + ["which"] * 4 + ["read4"] * 5 + ["which4"] * 3
    asked = set()
    for i, kind in enumerate(plan):
        n = 4 if kind.endswith("4") else 3
        ctx = PK.next()
        U = ctx.unit
        sym = SYMS[i % 4]
        hi = 6 if i < 4 else 9
        j = [0, 2, 1, 2, 1, 0, 2, 1][i] if n == 3 and i < 8 else [1, 2, 3, 0, 2][i - 12] if kind == "read4" else None
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
        else:
            j = rnd.choice([k for k in range(n) if vals[k] >= 2])
            v = vals[j]
            close = sorted([k for k in range(n) if k != j], key=lambda k: abs(vals[k] - v))
            its.append(mcq(f + ctx.q("which", v=v), cats[j], [cats[k] for k in close] + spare,
                           "Look for the row with %d %ss. %s" % (v, sym, count_row(cats[j], v, sym))))
    return {"title": "Picture graphs: one picture for each", "items": its}


# ------------------------------------------------------------ set 4: most and fewest
def set_most(rnd, PK):
    its = []
    plan = [("shapes", "most"), ("shapes", "fewest"),
            ("pic", "most"), ("tally", "fewest"), ("pic", "fewest"), ("tally", "most"),
            ("pic", "most"), ("tally", "fewest"),
            ("pic4", "fewest"), ("tally4", "most"), ("pic4", "most"), ("tally4", "fewest"),
            ("pic4", "most"), ("tally4", "fewest"), ("pic4", "fewest"), ("tally4", "most"),
            ("pic", "order_down"), ("tally", "order_up"), ("pic", "order_up"), ("tally", "order_down")]
    for i, (style, kind) in enumerate(plan):
        sym = SYMS[i % 4]
        if style == "shapes":
            for _ in range(1000):
                kinds = rnd.sample(SHAPES, 3)
                vals = [rnd.randint(3, 7) for _ in range(3)]
                if len(set(vals)) == 3 and sum(vals) <= 15:
                    break
            pl = [SHAPE_PL[k] for k in kinds]
            j = vals.index(max(vals) if kind == "most" else min(vals))
            other = [s for s in SHAPES if s not in kinds][0]
            order = sorted([k for k in range(3) if k != j], key=lambda k: abs(vals[k] - vals[j]))
            its.append(mcq(fig(mixed_svg(kinds, vals, rnd)) + "Sort the shapes. Which shape is there the %s of?" % kind,
                           cap(pl[j]), [cap(pl[k]) for k in order] + [cap(SHAPE_PL[other])],
                           "Sort and count. %s. %d is the %s number, so there are the %s %s."
                           % (rd_list([cap(p) for p in pl], vals), vals[j],
                              "biggest" if kind == "most" else "smallest", kind, pl[j])))
            continue
        n = 4 if style.endswith("4") else 3
        ctx = PK.next(lambda c: c.has("most"))
        hi = 9 if style.startswith("pic") else 12
        lo = 1 if n == 4 else 2
        if kind.startswith("order"):
            cats, vals = make_data(ctx, rnd, 2, hi, ok=lambda v: sorted(v)[2] - sorted(v)[0] >= 3)
        else:
            cats, vals = make_data(ctx, rnd, lo, hi, n=n,
                                   ok=lambda v: sorted(v)[-1] - sorted(v)[-2] <= 2 and sorted(v)[1] - sorted(v)[0] <= 2)
        if style.startswith("pic"):
            f, how = fig(ctx_pic(ctx, cats, vals, sym)), "Count the %ss in each row." % sym
        else:
            f, how = fig(ctx_tally(ctx, cats, vals)), "Count the tally marks in each row. A bundle is 5."
        if kind.startswith("order"):
            o = sorted(range(3), key=lambda k: -vals[k])
            want = o if kind == "order_down" else o[::-1]
            nm = lambda ks: ", ".join(cats[k] for k in ks)
            cand = [nm(want[::-1]), nm([want[1], want[0], want[2]]), nm([want[0], want[2], want[1]]), nm([want[2], want[0], want[1]])]
            words = ("most to fewest", "Most", "Fewest") if kind == "order_down" else ("fewest to most", "Fewest", "Most")
            its.append(mcq(f + "Put them in order from %s." % words[0], nm(want), cand,
                           "%s %s. %s: %s (%d). Next: %s (%d). %s: %s (%d)."
                           % (how, rd_list(cats, vals), words[1], cats[want[0]], vals[want[0]],
                              cats[want[1]], vals[want[1]], words[2], cats[want[2]], vals[want[2]])))
        else:
            j = vals.index(max(vals) if kind == "most" else min(vals))
            order = sorted([k for k in range(n) if k != j], key=lambda k: abs(vals[k] - vals[j]))
            spare = [x for x in ctx.cats if x not in cats]
            its.append(mcq(f + ctx.q("most", w=kind), cats[j], [cats[k] for k in order] + spare,
                           "%s %s. %d is the %s number. The answer is %s."
                           % (how, rd_list(cats, vals), vals[j], "biggest" if kind == "most" else "smallest",
                              cats[j])))
    return {"title": "Which has the most? Which has the fewest?", "items": its}


# ------------------------------------------------------------ set 5: how many more
def set_word(rnd, PK):
    its = []
    plan = ["more", "both", "more", "fewer", "total", "more", "both", "fewer", "more", "tie",
            "total", "more", "fewer", "both", "tie", "more", "fewer", "total", "tie", "more"]
    seen = set()
    for i, kind in enumerate(plan):
        ctx = PK.next(lambda c: c.has(kind))
        U = ctx.unit
        style = i % 2                       # 0 picture, 1 tally
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
                if vals[a] - vals[b] >= 2:
                    break
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
                e = ("%s %s %s %s needs to get from %d up to %d. Count on from %d to %d, or %s. So %s needs %s."
                     % (how, rd(a), rd(b), cats[b], vb, va, vb, va, minus(va, vb), cats[b], more_fmt(d, U, "more")))
            else:
                e = ("%s %s %s Match them up one to one. %d are left over: %s. The answer is %s."
                     % (how, rd(a), rd(b), d, minus(va, vb), more_fmt(d, U, word)))
            its.append(mcq(f + intro + q, fmt(d, U), [fmt(x, U) for x in cand], e))
        elif kind == "both":
            a, b = sorted(rnd.sample(range(3), 2))
            va, vb = vals[a], vals[b]
            t = va + vb
            cand = [abs(va - vb), t + 1, t - 1, max(va, vb), sum(vals)]
            its.append(mcq(f + intro + ctx.q("both", cats[a], cats[b]), fmt(t, U), [fmt(x, U) for x in cand],
                           "%s %s %s Altogether means add: %d + %d = %s." % (how, rd(a), rd(b), va, vb, fmt(t, U))))
        else:
            t = sum(vals)
            cand = [3, t - min(vals), t + 1, t - 1, max(vals)]
            its.append(mcq(f + intro + ctx.q("total"), fmt(t, U), [fmt(x, U) for x in cand],
                           "%s %s Add all three: %s = %s. (There are 3 rows, but the answer is the number of %s.)"
                           % (how, " ".join(rd(k) for k in range(3)), plus(vals), fmt(t, U), U[1])))
    return {"title": "How many more? Word problems", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


L_KINDS, L_SVALS = ["circle", "star", "triangle"], [5, 3, 4]
L_CATS = ["Apple", "Banana", "Mango"]
L_VALS = [7, 3, 12]


def body_html():
    fr = BYTITLE["Favourite Fruit"]
    lr = random.Random(1813)
    return (
        "<h2>The big idea</h2>"
        "<p><b>Data</b> is information we collect, like votes or things we count. "
        "First we <b>sort</b> things into groups. Then we <b>count</b> each group. "
        "Then we show the numbers with <b>tally marks</b> or a <b>picture graph</b>.</p>"
        "<h2>Sort and count</h2>"
        "<p>Put the same shapes together. Touch each one as you count it.</p>"
        "<figure class='sn-fig'>" + mixed_svg(L_KINDS, L_SVALS, lr, label="12 mixed shapes") +
        "<figcaption>Circles: 5. Stars: 3. Triangles: 4. That is 5 + 3 + 4 = 12 shapes altogether.</figcaption></figure>"
        "<h2>Tally marks: bundles of 5</h2>"
        "<p>Make one mark for each thing. The 5th mark goes <b>across</b> the first 4. "
        "That makes a <b>bundle of 5</b>. To read a tally, count the bundles by 5s, then count on the single marks.</p>"
        "<figure class='sn-fig'>" + ctx_tally(fr, L_CATS, L_VALS) +
        "<figcaption>Apple: 1 bundle and 2 marks. Count 5, then 6, 7. That is 7 votes. "
        "Mango: 2 bundles and 2 marks. Count 5, 10, then 11, 12. That is 12 votes.</figcaption></figure>"
        "<h2>Picture graph</h2>"
        "<p>In a picture graph, <b>one picture stands for one</b> thing. Put your finger on the name. "
        "Then count the pictures in that row only.</p>"
        "<figure class='sn-fig'>" + ctx_pic(fr, ["Apple", "Banana", "Mango"], [7, 3, 5], "star") +
        "<figcaption>The Mango row has 5 stars, so Mango got 5 votes.</figcaption></figure>"
        "<h2>Most and fewest</h2>"
        "<p>The <b>most</b> is the biggest number. In a picture graph it is the longest row. "
        "The <b>fewest</b> (also called the least) is the smallest number.</p>" +
        ex("Most and fewest", "Apple 7, Banana 3, Mango 5. Which fruit got the most votes? Which got the fewest?",
           "7 is the biggest number. 3 is the smallest number.", "Most: Apple. Fewest: Banana") +
        "<h2>How many more?</h2>"
        "<p><b>How many more</b> or <b>how many fewer</b> means compare. Match the pictures one to one, "
        "or take the smaller number away from the bigger one. <b>Altogether</b> means add.</p>" +
        ex("How many more?", "How many more votes did Apple get than Mango?",
           "Apple 7, Mango 5. 2 stars are left over. 7 %s 5 = 2." % MINUS, "2 more votes") +
        ex("How many altogether?", "How many votes were there altogether?",
           "Apple 7, Banana 3, Mango 5. 7 + 3 + 5 = 15.", "15 votes") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Counting a bundle of tally marks as 4, or as 6", "4 marks and 1 line across is 5"],
            ["Reading the row above or below", "Put your finger on the name first, then read that row"],
            ["Counting a shape twice or skipping one", "Touch or cross out each one as you count"],
            ["Adding when it asks how many more", "How many more or fewer means compare, so subtract"],
            ["Answering a name when it asks how many", "How many wants a number, like 4 votes"],
            ["Counting the rows instead of the things", "Altogether means add the numbers in each row"],
        ])
    )


FAQ = [
    {"q": "What do Year 1 students learn about data in the Australian Curriculum?",
     "a": "They collect data by asking questions and record it with objects, drawings, lists and tally marks (AC9M1ST01). They show it in one-to-one displays such as picture graphs and talk about what it shows, like which group has the most (AC9M1ST02)."},
    {"q": "How do you teach tally marks in Year 1?",
     "a": "Make one mark for each thing, and draw the 5th mark across the first 4 to make a bundle of 5. To read a tally, count the bundles by 5s and then count on the single marks, so 1 bundle and 2 marks is 7."},
    {"q": "What is a one-to-one display?",
     "a": "It is a graph where one picture, object or square stands for one thing. A picture graph with one picture for each vote is a one-to-one display, so you can just count the pictures."},
    {"q": "How can I practise data with my Year 1 child at home?",
     "a": "Ask the family a question, such as their favourite fruit, and keep a tally. Then ask “Which got the most?” and “How many more votes did apples get than bananas?”"},
]


def gen_data():
    rnd = random.Random(1812)
    PK = Picker(rnd)
    sets = [set_sort(rnd), set_tally(rnd, PK), set_picture(rnd, PK), set_most(rnd, PK), set_word(rnd, PK)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        pos = [it["a"] for it in s["items"]]
        assert all(pos.count(p) == 5 for p in range(4)), (s["title"], pos)
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"].count("<svg") == 1, it["q"][:80]
            k = it["q"] + "|" + "|".join(sorted(it["c"]))
            assert k not in seen, it["q"]
            seen.add(k)
    return {
        "country": "au", "subject": "maths", "grade": "year-1", "slug": "data-and-tally-marks", "sort": 12,
        "updated": UPDATED, "pdf_url": "",
        "title": "Data and Tally Marks: Sort, Count and Picture Graphs",
        "seo_title": "Year 1 Data and Tally Marks Worksheets: Sorting, Tally Marks and Picture Graphs (Free, with Answer Key)",
        "short_title": "Data and tally marks",
        "domain": "Statistics",
        "standard_code": "AC9M1ST01",
        "standard_url": "https://v9.australiancurriculum.edu.au/f-10-curriculum/learning-areas/mathematics",
        "standard_text": "Acquire and record data for categorical variables in various ways including using digital tools, objects, images, drawings, lists, tally marks and symbols",
        "meta_desc": "Free Year 1 maths worksheets on data for the Australian Curriculum (AC9M1ST01, AC9M1ST02): sort and count, read tally marks in bundles of 5, read picture graphs with one picture for each, find the most and fewest, and answer “how many more?”. 100 questions with an answer key.",
        "key_big": "Sort it, count it, show it.",
        "key_sub": "A tally bundle is 5: count 5, 10, then count on the single marks. In a picture graph each picture is 1. How many more means compare; altogether means add.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


def mark_large(u, pattern):
    """Tag pictures that must print larger (graphs, tally charts, A-D choices) so their labels stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


if __name__ == "__main__":
    u = gen_data()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as f:
        mark_large(u, "(picture graph|tally chart|four tally rows)")
        json.dump(u, f, ensure_ascii=False, indent=1)
    print("wrote", path)
