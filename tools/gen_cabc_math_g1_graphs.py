# -*- coding: utf-8 -*-
"""
BC Grade 1 Math: Concrete graphs (BC Mathematics Curriculum, Data and probability:
"concrete graphs, using one-to-one correspondence")
  python3 tools/gen_cabc_math_g1_graphs.py
Sort real things and count each group, read graphs made of real objects or connecting cubes
(1 object = 1), find the most and the fewest (also when a row is spread out), compare two rows
(how many more / fewer) and answer questions about class data (favourite fruit, how we get to school,
rain boots, BC animals, recess). Numbers to 20.
Wrong answers come from real mistakes: counting every thing instead of one group, counting the other
group, miscounting by one, reading the row above or below, adding when the question asks how many more,
picking the longest-looking row instead of counting, forgetting to add the new votes.
HTML attributes use single quotes (no backslashes in the JSON). Canadian English.
"""
import json, re, math, os, random

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-1")
UPDATED = "2026-11-02"
GREEN = "#006633"
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
    """Spread the correct answers evenly (5/5/5/5) over the 4 positions in every set."""
    for s in sets:
        targets = [p for p in range(4) for _ in range(5)]
        rnd.shuffle(targets)
        for it, t in zip(s["items"], targets):
            c = it["c"]
            wrong = [x for i, x in enumerate(c) if i != it["a"]]
            rnd.shuffle(wrong)
            right = c[it["a"]]
            it["c"] = wrong[:t] + [right] + wrong[t:]
            it["a"] = t


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


def count_list(v):
    return ", ".join(str(k) for k in range(1, v + 1))


def minus(a, b):
    return "%d %s %d = %d" % (a, MINUS, b, a - b)


# ------------------------------------------------------------ pictures of real things
def apple(cx, cy):
    return ("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='#6b4423' stroke-width='2' stroke-linecap='round'/>"
            "<ellipse cx='%.1f' cy='%.1f' rx='3.6' ry='1.8' fill='#2e9b57' transform='rotate(-30 %.1f %.1f)'/>"
            "<circle cx='%.1f' cy='%.1f' r='7.8' fill='#d64234' stroke='#8e2219' stroke-width='1'/>"
            % (cx, cy - 5, cx + 1.5, cy - 10.5, cx + 4.5, cy - 9, cx + 4.5, cy - 9, cx, cy + 1.5))


def banana(cx, cy):
    return ("<path d='M%.1f %.1f Q%.1f %.1f %.1f %.1f Q%.1f %.1f %.1f %.1f Z' fill='#f2c418' stroke='#a07800' stroke-width='1' "
            "stroke-linejoin='round'/>"
            % (cx - 9.5, cy - 6, cx, cy + 14, cx + 9.5, cy - 6, cx, cy - 1, cx - 9.5, cy - 6))


def pear(cx, cy):
    return ("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='#6b4423' stroke-width='2' stroke-linecap='round'/>"
            "<circle cx='%.1f' cy='%.1f' r='4.6' fill='#8cbf3f'/>"
            "<circle cx='%.1f' cy='%.1f' r='7' fill='#8cbf3f'/>"
            % (cx, cy - 7, cx + 1, cy - 11, cx, cy - 3.5, cx, cy + 3.5))


def orange(cx, cy):
    return ("<circle cx='%.1f' cy='%.1f' r='7.8' fill='#f39c12' stroke='#b36b00' stroke-width='1'/>"
            "<ellipse cx='%.1f' cy='%.1f' rx='3.4' ry='1.7' fill='#2e9b57' transform='rotate(-20 %.1f %.1f)'/>"
            % (cx, cy + 1, cx + 2.5, cy - 7.4, cx + 2.5, cy - 7.4))


FRUIT = {"Apple": apple, "Banana": banana, "Pear": pear, "Orange": orange}
FRUIT_PL = {"Apple": "apples", "Banana": "bananas", "Pear": "pears", "Orange": "oranges"}


def cube(x, y, s, col):
    """A connecting cube: square with a lighter inner face."""
    return ("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' rx='2' fill='%s' stroke='%s' stroke-width='1.2'/>"
            "<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' rx='1' fill='none' stroke='#ffffff' stroke-opacity='0.55' stroke-width='1'/>"
            % (x, y, s, s, col, INK, x + 4, y + 4, s - 8, s - 8))


# Sorting shapes (shape, colour)
SHAPES = ["circle", "square", "triangle", "star"]
COLOURS = ["red", "blue", "yellow", "green"]
COL = {"red": "#d64234", "blue": "#2e6fb0", "yellow": "#f2c418", "green": "#2e9b57"}
PL = {"circle": "circles", "square": "squares", "triangle": "triangles", "star": "stars"}


def star_pts(cx, cy, R, r):
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rad = R if i % 2 == 0 else r
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    return pts


def shape(kind, colour, cx, cy, k=1.05):
    col = COL[colour]
    st = " stroke='%s' stroke-width='1.2' stroke-linejoin='round'" % INK
    if kind == "circle":
        return "<circle cx='%.1f' cy='%.1f' r='%.1f' fill='%s'%s/>" % (cx, cy, 8.5 * k, col, st)
    if kind == "square":
        h = 7.5 * k
        return "<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' rx='1.5' fill='%s'%s/>" % (cx - h, cy - h, 2 * h, 2 * h, col, st)
    if kind == "triangle":
        h = 9.5 * k
        return "<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='%s'%s/>" % (
            cx, cy - h, cx + h, cy + h * 0.8, cx - h, cy + h * 0.8, col, st)
    return "<polygon points='%s' fill='%s'%s/>" % (" ".join("%.1f,%.1f" % p for p in star_pts(cx, cy, 10.5 * k, 4.4 * k)), col, st)


CELL = 30


def pile_svg(things, draw, rnd, label, cols=5):
    """Things mixed up on a mat (one per cell, small jitter) so they must be sorted before counting."""
    n = len(things)
    rows = int(math.ceil(n / float(cols)))
    if rows * cols - n < 2:
        rows += 1
    cells = sorted(rnd.sample(range(rows * cols), n))
    things = things[:]
    rnd.shuffle(things)
    W, H = cols * CELL + 10, rows * CELL + 10
    s = ["<rect x='1' y='1' width='%d' height='%d' rx='8' fill='#f6faf7' stroke='%s' stroke-width='1.5'/>" % (W - 2, H - 2, GRID)]
    for t, c in zip(things, cells):
        r, cc = divmod(c, cols)
        cx = 5 + cc * CELL + CELL / 2 + rnd.choice([-2, -1, 0, 1, 2])
        cy = 5 + r * CELL + CELL / 2 + rnd.choice([-2, -1, 0, 1, 2])
        s.append(draw(t, cx, cy))
    return svg_wrap(W, H, "".join(s), label)


def fruit_draw(t, cx, cy):
    return FRUIT[t](cx, cy)


def shape_draw(t, cx, cy):
    return shape(t[0], t[1], cx, cy)


# ------------------------------------------------------------ contexts
class Ctx:
    def __init__(self, key, title, axis, cats, unit, f, intro, cols=None, ph=None):
        self.key, self.title, self.axis, self.cats, self.unit = key, title, axis, cats, unit
        self.f, self.intro, self.cols, self.ph = f, intro, cols or {}, ph or {}

    def p(self, c):
        return self.ph.get(c, c)

    def q(self, kind, a=None, b=None, w=None, v=None, add=None):
        return self.f[kind].format(a=self.p(a) if a else "", b=self.p(b) if b else "", w=w or "",
                                   n=fmt(v, self.unit) if v is not None else "", add=add or "")

    def has(self, kind):
        return kind in self.f

    @property
    def fruit(self):
        return self.key == "fruit"


VOTE = ("vote", "votes")
KID = ("student", "students")


def votes_f(word):
    return {"ask": "How many votes did {a} get?",
            "more": "How many more votes did {a} get than {b}?",
            "fewer": "How many fewer votes did {a} get than {b}?",
            "both": "How many votes did {a} and {b} get altogether?",
            "total": "How many votes were there altogether?",
            "tie": "How many more votes does {b} need to tie with {a}?",
            "now": "Then {add} more students voted for {a}. How many votes does {a} have now?",
            "most": "Which %s got the {w} votes?" % word,
            "which": "Which %s got {n}?" % word,
            "same": "Which two got the same number of votes?"}


CTXS = [
    Ctx("fruit", "Our favourite fruit", "Fruit", ["Apple", "Banana", "Pear", "Orange"], VOTE, votes_f("fruit"),
        "Ms. Kaur’s class voted for a favourite fruit."),
    Ctx("school", "How we get to school", "Way", ["Bus", "Car", "Walk", "Bike"], KID,
        {"ask": "How many students {a} to school?",
         "more": "How many more students {a} than {b}?",
         "fewer": "How many fewer students {a} than {b}?",
         "both": "How many students {a} or {b}?",
         "total": "How many students are in the graph?",
         "most": "Which way do the {w} students get to school?",
         "which": "Which way do {n} get to school?",
         "same": "Which two ways have the same number of students?"},
        "Mr. Singh’s class graphed how they get to school.",
        cols={"Bus": "#f2c418", "Car": "#d64234", "Walk": "#2e9b57", "Bike": "#2e6fb0"},
        ph={"Bus": "take the bus", "Car": "come by car", "Walk": "walk", "Bike": "ride a bike"}),
    Ctx("boots", "Our rain boots", "Colour", ["Red", "Blue", "Yellow", "Green"], KID,
        {"ask": "How many students have {a} boots?",
         "more": "How many more students have {a} boots than {b} boots?",
         "fewer": "How many fewer students have {a} boots than {b} boots?",
         "both": "How many students have {a} or {b} boots?",
         "total": "How many students are in the graph?",
         "most": "Which colour of boots do the {w} students have?",
         "which": "Which colour of boots do {n} have?",
         "same": "Which two colours have the same number of students?"},
        "Room 4 in Vancouver graphed their rain boots.",
        cols={"Red": "#d64234", "Blue": "#2e6fb0", "Yellow": "#f2c418", "Green": "#2e9b57"},
        ph={"Red": "red", "Blue": "blue", "Yellow": "yellow", "Green": "green"}),
    Ctx("animal", "Favourite BC animal", "Animal", ["Orca", "Eagle", "Bear", "Salmon"], VOTE, votes_f("animal"),
        "Mrs. Chan’s class voted for a favourite BC animal.",
        cols={"Orca": "#3b3f46", "Eagle": "#8a5a2b", "Bear": "#b07a4f", "Salmon": "#e8746a"}),
    Ctx("recess", "What we play at recess", "Game", ["Soccer", "Tag", "Swings", "Slide"], KID,
        {"ask": "How many students picked {a}?",
         "more": "How many more students picked {a} than {b}?",
         "fewer": "How many fewer students picked {a} than {b}?",
         "both": "How many students picked {a} or {b}?",
         "total": "How many students are in the graph?",
         "most": "Which one did the {w} students pick?",
         "which": "Which one did {n} pick?",
         "same": "Which two got the same number of students?"},
        "Room 2 graphed what they play at recess.",
        cols={"Soccer": "#2e6fb0", "Tag": "#d64234", "Swings": "#7d4fa8", "Slide": "#2e9b57"},
        ph={"Soccer": "soccer", "Tag": "tag", "Swings": "the swings", "Slide": "the slide"}),
]
BYKEY = {c.key: c for c in CTXS}


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


def make_data(ctx, rnd, lo=1, hi=9, ok=lambda v: True, n=3, tmax=20, distinct=True):
    for _ in range(20000):
        cats = rnd.sample(ctx.cats, n)
        vals = [rnd.randint(lo, hi) for _ in range(n)]
        if distinct and len(set(vals)) != n:
            continue
        if sum(vals) > tmax:
            continue
        if ok(vals):
            return cats, vals
    raise ValueError("no data for " + ctx.title)


# ------------------------------------------------------------ concrete graphs
def row_graph(ctx, cats, vals, label=None):
    """Object graph: one row per category on a mat of squares. 1 object (or 1 cube) = 1. Everything starts at the line."""
    fs, rh, cw = 15, 28, 24
    lw = max(max(tw(c, fs) for c in cats), tw(ctx.axis, fs, True)) + 16
    m = max(max(vals), 6)
    W = int(math.ceil(max(lw + m * cw + 8, tw(ctx.title, 16, True) + 16)))
    top = 26
    s = [text(W / 2, 18, ctx.title, 16, bold=True)]
    for i, (c, v) in enumerate(zip(cats, vals)):
        y = top + i * rh
        s.append(text(lw - 8, y + 19, c, fs, anchor="end"))
        for j in range(m):
            s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='#f6faf7' stroke='%s' stroke-width='1'/>"
                     % (lw + j * cw, y + 1, cw, rh - 2, GRID))
        for j in range(v):
            cx = lw + j * cw + cw / 2
            if ctx.fruit:
                s.append(FRUIT[c](cx, y + rh / 2))
            else:
                s.append(cube(cx - 9, y + rh / 2 - 9, 18, ctx.cols[c]))
    H = top + len(cats) * rh
    s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2.5'/>" % (lw, top - 2, lw, H + 2, GREEN))
    H += 6
    return svg_wrap(W, H, "".join(s), label or "concrete graph: " + ctx.title.lower())


def tower_graph(ctx, cats, vals, label=None):
    """Cube towers standing on one line, a label under each tower. 1 cube = 1."""
    fs, cs = 15, 18
    colw = int(max(max(tw(c, fs) for c in cats) + 12, 46))
    m = max(max(vals), 5)
    W = int(math.ceil(max(len(cats) * colw + 8, tw(ctx.title, 16, True) + 16)))
    x0 = (W - len(cats) * colw) / 2
    top = 28
    base = top + m * cs
    s = [text(W / 2, 18, ctx.title, 16, bold=True)]
    for i, (c, v) in enumerate(zip(cats, vals)):
        cx = x0 + i * colw + colw / 2
        for j in range(v):
            if ctx.fruit:
                s.append(FRUIT[c](cx, base - (j + 0.5) * cs - 1))
            else:
                s.append(cube(cx - cs / 2, base - (j + 1) * cs, cs, ctx.cols[c]))
        s.append(text(cx, base + 20, c, fs))
    s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='2.5'/>" % (x0, base + 1, x0 + len(cats) * colw, base + 1, GREEN))
    H = base + 28
    return svg_wrap(W, H, "".join(s), label or "cube tower graph: " + ctx.title.lower())


def spread_svg(cats, vals, gaps, label="fruit in rows that are not lined up"):
    """Rows of fruit with no mat: some rows are spread out, some are close together."""
    fs, rh = 15, 30
    lw = max(tw(c, fs) for c in cats) + 16
    starts = [lw + 12 for i in range(len(cats))]
    ends = [st + (v - 1) * g for st, v, g in zip(starts, vals, gaps)]
    W = int(math.ceil(max(ends) + 16))
    s = []
    for i, (c, v, g) in enumerate(zip(cats, vals, gaps)):
        y = 4 + i * rh + rh / 2
        s.append(text(lw - 8, y + 5, c, fs, anchor="end"))
        for j in range(v):
            s.append(FRUIT[c](starts[i] + j * g, y))
    H = 4 + len(cats) * rh + 4
    return svg_wrap(W, int(H), "".join(s), label)


def graph(ctx, cats, vals, style):
    return fig(row_graph(ctx, cats, vals) if style == "row" else tower_graph(ctx, cats, vals))


def count_txt(ctx, c, v, style):
    where = "row" if style == "row" else "tower"
    if ctx.fruit:
        what = FRUIT_PL[c] if v != 1 else c.lower()
    else:
        what = "cubes" if v != 1 else "cube"
    frm = "from the start line" if style == "row" else "from the bottom"
    if v <= 8:
        return "Find the %s %s. Touch each one as you count %s: %s." % (c, where, frm, count_list(v))
    return "Find the %s %s. Count the %s %s. There are %d." % (c, where, what, frm, v)


def rd(cats, vals):
    return ". ".join("%s: %d" % (c, v) for c, v in zip(cats, vals)) + "."


# ------------------------------------------------------------ set 1: sort and count
def set_sort(rnd):
    its = []
    seen = set()
    fr = list(FRUIT)

    # fruit pile: how many apples? (6)
    for i, (f, want_k) in enumerate([("Apple", 3), ("Pear", 5), ("Banana", 4), ("Orange", 6), ("Apple", 7), ("Pear", 5)]):
        for _ in range(5000):
            kinds = [f] + rnd.sample([x for x in fr if x != f], 2 if i < 3 else 3)
            n = want_k + (rnd.randint(4, 6) if i < 3 else rnd.randint(6, 8))
            pile = [f] * want_k + [rnd.choice(kinds[1:]) for _ in range(n - want_k)]
            cnt = {k: pile.count(k) for k in kinds}
            k = cnt[f]
            other = max([x for x in kinds if x != f], key=lambda x: cnt[x])
            if k != want_k or min(cnt.values()) < 2 or cnt[other] == k:
                continue
            if len(set(cnt.values())) < len(kinds) - 1:
                continue
            key = tuple(sorted(pile))
            if key not in seen:
                seen.add(key)
                break
        else:
            raise ValueError("no pile")
        pl = FRUIT_PL[f]
        unit = (f.lower(), pl)
        q = fig(pile_svg(pile, fruit_draw, rnd, "mixed fruit to sort")) + "Sort the fruit. How many %s are there?" % pl
        e = ("Look only at the %s. Touch each one as you count: %s. There are %s. "
             "Do not count the other fruit." % (pl, count_list(k), fmt(k, unit)))
        its.append(mcq(q, fmt(k, unit), [fmt(x, unit) for x in [cnt[other], n, k + 1, k - 1]], e))

    # shapes: sort by colour (4) and by shape (4)
    plan = [("colour", "red"), ("shape", "circle"), ("colour", "blue"), ("shape", "triangle"),
            ("colour", "yellow"), ("shape", "square"), ("colour", "green"), ("shape", "star")]
    for (attr, v), want_k in zip(plan, [5, 4, 6, 3, 4, 5, 3, 6]):
        a = 1 if attr == "colour" else 0
        for _ in range(5000):
            n = rnd.randint(9, 12)
            items = [(rnd.choice(SHAPES), rnd.choice(COLOURS)) for _ in range(n)]
            want = [it for it in items if it[a] == v]
            k = len(want)
            if k != want_k:
                continue
            # a child who also looks at the other attribute counts only the most common kind
            ob = 1 - a
            top_o = max(set(it[ob] for it in want), key=lambda x: sum(1 for it in want if it[ob] == x))
            only = sum(1 for it in want if it[ob] == top_o)
            if only >= k or len(set(it[ob] for it in want)) < 2:
                continue
            key = tuple(sorted(items))
            if key not in seen:
                seen.add(key)
                break
        else:
            raise ValueError("no shapes")
        if attr == "colour":
            word, unit = "%s shapes" % v, ("%s shape" % v, "%s shapes" % v)
            e = ("Sort by colour. Shape does not matter. Count only the %s ones: %s. There are %s."
                 % (v, count_list(k), fmt(k, unit)))
        else:
            word, unit = PL[v], (v, PL[v])
            e = ("Sort by shape. Colour does not matter. Count every %s: %s. There are %s."
                 % (v, count_list(k), fmt(k, unit)))
        q = fig(pile_svg(items, shape_draw, rnd, "mixed shapes to sort")) + "Sort by %s. How many %s are there?" % (attr, word)
        its.append(mcq(q, fmt(k, unit), [fmt(x, unit) for x in [only, n, k + 1, k - 1]], e))

    # which group has the most / fewest after sorting (6)
    for i, kind in enumerate(["most", "fewest", "most", "fewest", "most", "fewest"]):
        for _ in range(5000):
            n = rnd.randint(11, 15)
            pile = [rnd.choice(fr) for _ in range(n)]
            cnt = [pile.count(x) for x in fr]
            if min(cnt) < 1 or len(set(cnt)) < 4:
                continue
            srt = sorted(cnt)
            if kind == "most" and srt[3] - srt[2] != 1:
                continue
            if kind == "fewest" and srt[1] - srt[0] != 1:
                continue
            key = tuple(sorted(pile))
            if key not in seen:
                seen.add(key)
                break
        else:
            raise ValueError("no pile")
        j = cnt.index(max(cnt) if kind == "most" else min(cnt))
        order = sorted([k for k in range(4) if k != j], key=lambda k: abs(cnt[k] - cnt[j]))
        q = fig(pile_svg(pile, fruit_draw, rnd, "mixed fruit to sort")) + "Sort the fruit. Which fruit has the %s?" % kind
        e = ("Sort them into 4 groups and count each group. %s %d is the %s number. The answer is %s."
             % (rd([FRUIT_PL[x].capitalize() for x in fr], cnt), cnt[j], "greatest" if kind == "most" else "least",
                FRUIT_PL[fr[j]].capitalize()))
        its.append(mcq(q, FRUIT_PL[fr[j]].capitalize(), [FRUIT_PL[fr[k]].capitalize() for k in order], e))
    return {"title": "Sort and count", "items": its}


# ------------------------------------------------------------ set 2: read a concrete graph
def set_read(rnd, PK):
    its = []
    plan = (["row-ask"] * 5 + ["tower-ask"] * 4 + ["row-ask"] * 4 + ["tower-ask"] * 2 +
            ["row-which", "tower-which", "row-which", "row-which4", "tower-which4"])
    asked = set()
    for i, kind in enumerate(plan):
        style = "row" if kind.startswith("row") else "tower"
        n = 4 if kind.endswith("4") or i in (11, 12, 14) else 3
        ctx = PK.next()
        U = ctx.unit
        hi = 7 if style == "tower" else (6 if i < 5 else 10)
        for _ in range(500):
            cats, vals = make_data(ctx, rnd, 1, hi, n=n, ok=lambda v: max(v) >= 3)
            j = rnd.choice([k for k in range(n) if vals[k] >= 2])
            if (ctx.key, cats[j], vals[j]) not in asked:
                break
        else:
            raise ValueError("no data")
        asked.add((ctx.key, cats[j], vals[j]))
        f = graph(ctx, cats, vals, style)
        c, v = cats[j], vals[j]
        nb = [vals[k] for k in (j - 1, j + 1) if 0 <= k < n]          # read the row above or below
        if "ask" in kind:
            cand = nb + [v + 1, v - 1] + [vals[k] for k in range(n) if k != j] + [sum(vals)]
            its.append(mcq(f + ctx.q("ask", c), fmt(v, U), [fmt(x, U) for x in cand],
                           "%s So the answer is %s." % (count_txt(ctx, c, v, style), fmt(v, U))))
        else:
            close = sorted([k for k in range(n) if k != j], key=lambda k: abs(vals[k] - v))
            spare = [x for x in ctx.cats if x not in cats]
            its.append(mcq(f + ctx.q("which", v=v), c, [cats[k] for k in close] + spare,
                           "Count each %s. %s The %s %s has %d." % ("row" if style == "row" else "tower",
                                                                   rd(cats, vals), c, "row" if style == "row" else "tower", v)))
    return {"title": "Read a concrete graph: 1 object = 1", "items": its}


# ------------------------------------------------------------ set 3: most and fewest
def set_most(rnd, PK):
    its = []
    plan = [("row", "most", 3), ("tower", "fewest", 3), ("row", "fewest", 3), ("tower", "most", 3),
            ("row", "most", 4), ("tower", "fewest", 4), ("row", "fewest", 4), ("tower", "most", 4),
            ("spread", "most", 3), ("spread", "fewest", 3),
            ("row", "same", 4), ("tower", "same", 4),
            ("row", "most", 4), ("tower", "fewest", 4),
            ("spread", "most", 3), ("row", "same", 4),
            ("row", "fewest", 4), ("spread", "fewest", 3), ("tower", "same", 4), ("tower", "most", 4)]
    seen = set()
    for i, (style, kind, n) in enumerate(plan):
        if style == "spread":
            fruit = BYKEY["fruit"]
            for _ in range(5000):
                cats = rnd.sample(fruit.cats, 3)
                vals = rnd.sample(range(4, 9), 3)
                if sorted(vals)[2] - sorted(vals)[0] > 3 or sorted(vals)[1] - sorted(vals)[0] < 1:
                    continue
                if (tuple(cats), tuple(vals)) not in seen:
                    break
            else:
                raise ValueError("no spread data")
            seen.add((tuple(cats), tuple(vals)))
            j = vals.index(max(vals) if kind == "most" else min(vals))
            # the rows look backwards: the row with the most is the shortest, the row with the fewest is the longest
            trap = vals.index(min(vals) if kind == "most" else max(vals))
            o = sorted(range(3), key=lambda k: -vals[k])
            lens = {}
            lens[o[0]] = (vals[o[0]] - 1) * 24
            lens[o[1]] = lens[o[0]] + 34
            lens[o[2]] = lens[o[1]] + 34
            gaps = [lens[k] / (vals[k] - 1.0) for k in range(3)]
            assert min(gaps) >= 24 and lens[o[2]] > lens[o[1]] > lens[o[0]]
            q = fig(spread_svg(cats, vals, gaps)) + "Which fruit has the %s? Count, do not just look." % kind
            cand = [cats[trap]] + [cats[k] for k in range(3) if k not in (j, trap)] + ["They are the same"]
            e = ("The %s are spread out, so that row looks long. The %s are close together. "
                 "Count each row: %s %s has the %s." % (FRUIT_PL[cats[o[2]]], FRUIT_PL[cats[o[0]]], rd(cats, vals), cats[j], kind))
            its.append(mcq(q, cats[j], cand, e))
            continue
        ctx = PK.next(lambda c: c.has("same") if kind == "same" else True)
        hi = 7 if style == "tower" else 9
        for _ in range(500):
            if kind == "same":
                cats, vals = make_data(ctx, rnd, 1, hi, n=4, distinct=False,
                                       ok=lambda v: len(set(v)) == 3 and min(v) >= 2)
            else:
                cats, vals = make_data(ctx, rnd, 1, hi, n=n,
                                       ok=lambda v: sorted(v)[-1] - sorted(v)[-2] <= 2 and sorted(v)[1] - sorted(v)[0] <= 2)
            if (ctx.key, tuple(vals)) not in seen:
                break
        else:
            raise ValueError("no data")
        seen.add((ctx.key, tuple(vals)))
        f = graph(ctx, cats, vals, style)
        part = "row" if style == "row" else "tower"
        if kind == "same":
            pair = [k for k in range(4) if vals.count(vals[k]) == 2]
            nm = lambda a, b: "%s and %s" % (cats[a], cats[b])
            others = [(a, b) for a in range(4) for b in range(a + 1, 4) if (a, b) != tuple(pair)]
            others.sort(key=lambda p: abs(vals[p[0]] - vals[p[1]]))
            e = "Count each %s. %s %s and %s both have %d." % (part, rd(cats, vals), cats[pair[0]], cats[pair[1]], vals[pair[0]])
            its.append(mcq(f + ctx.q("same"), nm(*pair), [nm(*p) for p in others], e))
        else:
            j = vals.index(max(vals) if kind == "most" else min(vals))
            order = sorted([k for k in range(n) if k != j], key=lambda k: abs(vals[k] - vals[j]))
            opp = vals.index(min(vals) if kind == "most" else max(vals))
            order = [opp] + [k for k in order if k != opp] if n == 3 else order
            spare = [x for x in ctx.cats if x not in cats]
            look = "longest" if kind == "most" else "shortest"
            if style == "tower":
                look = "tallest" if kind == "most" else "shortest"
            e = ("Everything starts at the line, so the %s %s has the %s. %s %d is the %s number. The answer is %s."
                 % (look, part, kind, rd(cats, vals), vals[j], "greatest" if kind == "most" else "least", cats[j]))
            its.append(mcq(f + ctx.q("most", w=kind), cats[j], [cats[k] for k in order] + spare, e))
    return {"title": "Which has the most? Which has the fewest?", "items": its}


# ------------------------------------------------------------ set 4: how many more, how many fewer
def set_compare(rnd, PK):
    its = []
    plan = ["more", "more", "fewer", "more", "fewer", "more", "more", "fewer", "more", "fewer",
            "more", "fewer", "more", "more", "fewer", "more", "fewer", "more", "fewer", "more"]
    asked = set()
    for i, kind in enumerate(plan):
        style = "row" if i % 3 != 1 else "tower"
        ctx = PK.next()
        U = ctx.unit
        hi = 7 if style == "tower" else (6 if i < 6 else 10)
        for _ in range(500):
            cats, vals = make_data(ctx, rnd, 1, hi, ok=lambda v: sorted(v)[2] - sorted(v)[0] >= 2)
            a, b = sorted(rnd.sample(range(3), 2), key=lambda k: -vals[k])
            d = vals[a] - vals[b]
            if d >= (1 if i < 6 else 2) and d <= 6 and (ctx.key, cats[a], cats[b], vals[a], vals[b]) not in asked:
                break
        else:
            raise ValueError("no data")
        asked.add((ctx.key, cats[a], cats[b], vals[a], vals[b]))
        va, vb = vals[a], vals[b]
        third = [k for k in range(3) if k not in (a, b)][0]
        q = ctx.q("more", cats[a], cats[b]) if kind == "more" else ctx.q("fewer", cats[b], cats[a])
        cand = [va + vb, va, vb, d + 1, d - 1, abs(vals[third] - vb), abs(va - vals[third])]
        word = kind
        if style == "row":
            how = "Match them one to one. %d %s left over." % (d, "is" if d == 1 else "are")
        else:
            what = (cats[a].lower() if d == 1 else FRUIT_PL[cats[a]]) if ctx.fruit else ("cube" if d == 1 else "cubes")
            how = "Compare the towers. The %s tower has %d extra %s on top." % (cats[a], d, what)
        e = ("%s: %d. %s: %d. %s %s. The answer is %d %s."
             % (cats[a], va, cats[b], vb, how, minus(va, vb), d, word))
        its.append(mcq(graph(ctx, cats, vals, style) + q, "%d %s" % (d, word), ["%d %s" % (x, word) for x in cand], e))
    return {"title": "How many more? How many fewer?", "items": its}


# ------------------------------------------------------------ set 5: class data word problems
def set_word(rnd, PK):
    its = []
    plan = ["total", "both", "more", "total", "now", "now", "both", "more", "tie", "fewer",
            "fewer", "total", "both", "tie", "total", "both", "fewer", "more", "both", "total"]
    fruit, school = BYKEY["fruit"], BYKEY["school"]
    asked, seen = set(), set()
    for i, kind in enumerate(plan):
        if i % 2 == 0:
            ctx = fruit if i % 4 == 0 else school
        else:
            ctx = BYKEY["animal"] if kind in ("tie", "now") else PK.next(lambda c: c not in (fruit, school))
        if not ctx.has(kind):
            kind = {"tie": "more", "now": "both"}[kind]
        U = ctx.unit
        style = "row" if i % 3 != 2 else "tower"
        hi = 7 if style == "tower" else 9
        for _ in range(500):
            if kind in ("more", "fewer", "tie"):
                cats, vals = make_data(ctx, rnd, 1, hi, ok=lambda v: sorted(v)[2] - sorted(v)[0] >= 3)
            elif kind == "now":
                cats, vals = make_data(ctx, rnd, 2, hi, tmax=16)
            else:
                cats, vals = make_data(ctx, rnd, 2, hi, n=3 if i % 2 == 0 else 4 if kind == "total" else 3)
            if (ctx.key, tuple(vals)) not in seen:
                break
        else:
            raise ValueError("no data")
        seen.add((ctx.key, tuple(vals)))
        n = len(cats)
        f = graph(ctx, cats, vals, style)
        intro = ctx.intro + " "
        r = lambda k: "%s: %d." % (cats[k], vals[k])
        if kind in ("more", "fewer", "tie"):
            for _ in range(200):
                a, b = sorted(rnd.sample(range(3), 2), key=lambda k: -vals[k])
                if vals[a] - vals[b] >= 2 and (ctx.key, kind, cats[a], cats[b]) not in asked:
                    break
            asked.add((ctx.key, kind, cats[a], cats[b]))
            va, vb = vals[a], vals[b]
            d = va - vb
            if kind == "more":
                q = ctx.q("more", cats[a], cats[b])
            elif kind == "fewer":
                q = ctx.q("fewer", cats[b], cats[a])
            else:
                q = ctx.q("tie", cats[a], cats[b])
            cand = [va + vb, va, vb, d + 1, d - 1]
            word = "fewer" if kind == "fewer" else "more"
            if kind == "tie":
                e = ("%s %s %s needs to go from %d up to %d. Count on: %s. That is %d more. %s. So %s needs %s."
                     % (r(a), r(b), cats[b], vb, va, ", ".join(str(x) for x in range(vb + 1, va + 1)), d,
                        minus(va, vb), cats[b], "%d more %s" % (d, U[0] if d == 1 else U[1])))
            else:
                e = ("%s %s Match them one to one. %d %s left over. %s. The answer is %d %s %s."
                     % (r(a), r(b), d, "is" if d == 1 else "are", minus(va, vb), d, word, U[0] if d == 1 else U[1]))
            its.append(mcq(f + intro + q, fmt(d, U), [fmt(x, U) for x in cand], e))
        elif kind == "both":
            for _ in range(200):
                a, b = sorted(rnd.sample(range(n), 2))
                if (ctx.key, kind, cats[a], cats[b]) not in asked:
                    break
            asked.add((ctx.key, kind, cats[a], cats[b]))
            va, vb = vals[a], vals[b]
            t = va + vb
            cand = [abs(va - vb), t + 1, t - 1, max(va, vb), sum(vals)]
            its.append(mcq(f + intro + ctx.q("both", cats[a], cats[b]), fmt(t, U), [fmt(x, U) for x in cand],
                           "%s %s Add the two: %d + %d = %d. The answer is %s." % (r(a), r(b), va, vb, t, fmt(t, U))))
        elif kind == "now":
            add = 2 if i < 10 else 3
            j = rnd.choice([k for k in range(n) if (ctx.key, "now", cats[k]) not in asked])
            asked.add((ctx.key, "now", cats[j]))
            v = vals[j]
            nb = [vals[k] + add for k in (j - 1, j + 1) if 0 <= k < n]       # added to the wrong row
            cand = [v, v + add + 1, v + add - 1] + nb + [sum(vals) + add]
            q = ctx.q("now", cats[j], add="%d" % add)
            e = ("The graph shows %s: %d. Add the %d new votes: %d + %d = %d. Now %s has %s."
                 % (cats[j], v, add, v, add, v + add, cats[j], fmt(v + add, U)))
            its.append(mcq(f + intro + q, fmt(v + add, U), [fmt(x, U) for x in cand], e))
        else:
            t = sum(vals)
            cand = [n, t + 1, t - 1, max(vals), t - min(vals)]
            plus = " + ".join(str(v) for v in vals)
            e = ("%s Add them all: %s = %d. (There are %d %ss, but the question asks for the number of %s.)"
                 % (" ".join(r(k) for k in range(n)), plus, t, n, "row" if style == "row" else "tower", U[1]))
            its.append(mcq(f + intro + ctx.q("total"), fmt(t, U), [fmt(x, U) for x in cand], e))
    return {"title": "Word problems: class data", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


L_PILE = ["Apple"] * 6 + ["Banana"] * 3 + ["Pear"] * 4
L_CATS = ["Apple", "Banana", "Pear"]
L_VALS = [6, 3, 4]
L_SCH = ["Bus", "Walk", "Car", "Bike"]
L_SCV = [5, 7, 3, 2]


def body_html():
    fr, sc = BYKEY["fruit"], BYKEY["school"]
    return (
        "<h2>The big idea</h2>"
        "<p>A <b>concrete graph</b> is a graph made of real things. "
        "It can use fruit, toys, shoes or connecting cubes. "
        "<b>One thing stands for one.</b> This is called <b>one-to-one correspondence</b>.</p>"
        "<h2>Sort, then count</h2>"
        "<p>First, <b>sort</b> the things into groups. Then <b>count</b> each group. "
        "Touch each thing once as you count.</p>"
        "<figure class='sn-fig'>" + pile_svg(L_PILE, fruit_draw, random.Random(7), "mixed fruit to sort") +
        "<figcaption>Sort the fruit. There are 6 apples, 3 bananas and 4 pears.</figcaption></figure>"
        "<h2>Make and read the graph</h2>"
        "<p>Put each group in its own row. Every row <b>starts at the same line</b>. "
        "Put one thing in each square. Then the longest row has the most.</p>"
        "<figure class='sn-fig'>" + row_graph(fr, L_CATS, L_VALS) +
        "<figcaption>Apple got 6 votes. Banana got 3. Pear got 4. Apple has the most. Banana has the fewest.</figcaption></figure>"
        "<p>We can also use <b>cube towers</b>. Each student puts one cube on a tower. "
        "The tallest tower has the most.</p>"
        "<figure class='sn-fig'>" + tower_graph(sc, L_SCH, L_SCV) +
        "<figcaption>7 students walk. That is the tallest tower. 2 students ride a bike. That is the shortest tower.</figcaption></figure>"
        "<h2>Count, do not just look</h2>"
        "<p>If things are spread out, a row can look long. Match the things one to one, or count them.</p>"
        "<figure class='sn-fig'>" + spread_svg(["Apple", "Banana"], [6, 4], [23, 46], "apples close together and bananas spread out") +
        "<figcaption>The banana row looks longer, but there are only 4 bananas. There are 6 apples.</figcaption></figure>"
        "<h2>How many more?</h2>"
        "<p><b>How many more</b> and <b>how many fewer</b> mean compare. Match the rows one to one. "
        "Count the ones left over. <b>Altogether</b> means add.</p>" +
        ex("How many more?", "Apple 6, Pear 4. How many more votes did Apple get than Pear?",
           "Match 4 apples with 4 pears. 2 apples are left over. 6 %s 4 = 2." % MINUS, "2 more votes") +
        ex("How many altogether?", "Apple 6, Banana 3, Pear 4. How many votes were there altogether?",
           "6 + 3 + 4 = 13.", "13 votes") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Counting all the things, not one group", "Sort first, then count only that group"],
            ["Counting a thing twice or skipping one", "Touch each thing once as you count"],
            ["Reading the row above or below", "Put your finger on the label, then read that row"],
            ["Picking the row that looks longest", "Count, or match one to one"],
            ["Adding when it asks how many more", "How many more means compare: find what is left over"],
        ])
    )


FAQ = [
    {"q": "What is a concrete graph in Grade 1 math?",
     "a": "A concrete graph is made of real things, such as fruit, shoes or connecting cubes, lined up in rows or towers. Each thing stands for one, so students can count and compare the rows."},
    {"q": "What does one-to-one correspondence mean on a graph?",
     "a": "It means one object stands for one piece of data, such as one cube for each student’s vote. Matching two rows one to one shows which row has more and how many more."},
    {"q": "What do Grade 1 students learn about data in the BC math curriculum?",
     "a": "In the BC Grade 1 Data and probability area, students make and read concrete graphs using one-to-one correspondence. They sort, count, compare which has more or fewer, and talk about what the graph shows."},
    {"q": "How can I practise concrete graphs with my Grade 1 child at home?",
     "a": "Sort snacks, socks or toy cars into rows that start at the same line. Ask which row has the most, which has the fewest and how many more one row has than another."},
]


def gen_unit():
    rnd = random.Random(51809)
    PK = Picker(rnd)
    sets = [set_sort(rnd), set_read(rnd, PK), set_most(rnd, PK), set_compare(rnd, PK), set_word(rnd, PK)]
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
        "country": "ca-bc", "subject": "math", "grade": "grade-1", "slug": "concrete-graphs", "sort": 9,
        "updated": UPDATED, "pdf_url": "",
        "title": "Grade 1 Concrete Graphs: Sort, Count and Compare",
        "seo_title": "Grade 1 Concrete Graphs Worksheets: Free Math Practice with Answer Key (BC Curriculum)",
        "short_title": "Concrete graphs",
        "domain": "Data and probability",
        "standard_code": "Grade 1: Data and probability",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/1/core",
        "standard_text": "Concrete graphs, using one-to-one correspondence",
        "meta_desc": "Free Grade 1 math worksheets on concrete graphs for the BC curriculum: sort and count real things, read graphs of fruit and cube towers where 1 object = 1, find the most and the fewest, and answer how many more questions about class data. 100 questions with an answer key.",
        "key_big": "In a concrete graph, 1 thing = 1. Start every row at the same line, then count.",
        "key_sub": "Sort first, then count one group. Touch each thing once. The longest row or tallest tower has the most. How many more means match one to one and count what is left over.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


def mark_large(u, pattern):
    """Tag pictures that must print larger (graphs, rows, piles) so they stay readable."""
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
        mark_large(u, "(concrete graph|cube tower graph|fruit in rows|mixed)")
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
