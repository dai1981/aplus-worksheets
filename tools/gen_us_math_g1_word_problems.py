# -*- coding: utf-8 -*-
"""
US Grade 1 Math: Addition and Subtraction Word Problems within 20 (1.OA.A.1)
  python tools/gen_us_math_g1_word_problems.py
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "us", "math", "grade-1")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
PINK = "#f6d5d1"
INK = "#2b2b2b"
RED = "#c0392b"
FONT = "Arial, Helvetica, sans-serif"
BOX = "☐"
MINUS = "−"
GIRLS = ["Maya", "Ava", "Mia", "Zoe", "Lily", "Emma", "Nora", "Ruby", "Sofia", "Grace"]
BOYS = ["Leo", "Noah", "Eli", "Sam", "Ben", "Omar", "Kai", "Jack", "Luis", "Owen"]

# object colors
C = dict(red="#d9443a", blue="#3b7dd8", green="#3fa34d", yellow="#f2c230", orange="#f08a24",
         purple="#8e5bc7", gold="#e8b21c", silver="#b8bfc6", pink="#e86aa6", brown="#c68a4a")


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e, rnd):
    """4 choices: correct + 3 unique distractors (no zero or negative numbers)."""
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        c = str(c)
        lead = c.split(" ")[0]
        if c in seen or not c:
            continue
        if lead.lstrip("-").isdigit() and (int(lead) < 1 or int(lead) > 40):
            continue
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    ch = pick + [correct]
    rnd.shuffle(ch)
    return {"q": q, "c": ch, "a": ch.index(correct), "e": e}


def cap(s):
    return s[0].upper() + s[1:]


class People:
    def __init__(self, rnd):
        self.pool = [(n, "she", "her") for n in GIRLS] + [(n, "he", "his") for n in BOYS]
        rnd.shuffle(self.pool)
        self.i = 0

    def next(self):
        p = self.pool[self.i % len(self.pool)]
        self.i += 1
        return p

    def one(self):
        n, he, his = self.next()
        return dict(N=n, he=he, He=cap(he), his=his, His=cap(his))

    def two(self):
        a = self.next()
        b = self.next()
        while b[0] == a[0]:
            b = self.next()
        return a[0], b[0]


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def tw(t, fs):
    """Approximate width in px of bold Arial text."""
    return len(str(t)) * fs * 0.6


def text(x, y, t, fs=16, anchor="middle", col=INK):
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, col, anchor, t))


def fmt(n, u):
    return "%d %s" % (n, u[0] if n == 1 else u[1])


def say(t, p, **k):
    d = dict(p)
    d.update(k)
    return t.format(**d)


# ------------------------------------------------------------ objects (each fits in a 28 x 28 cell)
PITCH = 28
DEF_COL = dict(apple="red", star="gold", fish="orange", ball="blue", flower="pink", block="green",
               cookie="brown", balloon="red", car="blue", duck="yellow")


def obj(kind, cx, cy, col=None):
    col = C[col or DEF_COL[kind]]
    s = "<g data-o='1'>"
    if kind == "apple":
        s += ("<path d='M%.1f %.1f q1 -4 3 -5' fill='none' stroke='#7a4a1e' stroke-width='2'/>" % (cx, cy - 7)
              + "<ellipse cx='%.1f' cy='%.1f' rx='4' ry='2' fill='%s' transform='rotate(-30 %.1f %.1f)'/>"
              % (cx + 5, cy - 10, C["green"], cx + 5, cy - 10)
              + "<circle cx='%.1f' cy='%.1f' r='9' fill='%s' stroke='%s' stroke-width='1.2'/>" % (cx, cy + 1, col, INK))
    elif kind == "star":
        pts = []
        for k in range(10):
            r = 11 if k % 2 == 0 else 4.6
            a = math.pi / 2 + k * math.pi / 5
            pts.append("%.1f,%.1f" % (cx + r * math.cos(a), cy - r * math.sin(a) + 1))
        s += "<polygon points='%s' fill='%s' stroke='%s' stroke-width='1.2'/>" % (" ".join(pts), col, INK)
    elif kind == "fish":
        s += ("<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='%s' stroke='%s' stroke-width='1.2'/>"
              % (cx + 3, cy, cx + 11, cy - 6.5, cx + 11, cy + 6.5, col, INK)
              + "<ellipse cx='%.1f' cy='%.1f' rx='8' ry='6' fill='%s' stroke='%s' stroke-width='1.2'/>" % (cx - 3, cy, col, INK)
              + "<circle cx='%.1f' cy='%.1f' r='1.4' fill='%s'/>" % (cx - 7, cy - 1.5, INK))
    elif kind == "ball":
        s += ("<circle cx='%.1f' cy='%.1f' r='9.5' fill='%s' stroke='%s' stroke-width='1.2'/>" % (cx, cy, col, INK)
              + "<path d='M%.1f %.1f Q%.1f %.1f %.1f %.1f' fill='none' stroke='#ffffff' stroke-width='1.8'/>"
              % (cx - 9, cy - 2, cx, cy + 5, cx + 9, cy - 2))
    elif kind == "flower":
        for k in range(5):
            a = -math.pi / 2 + k * 2 * math.pi / 5
            s += "<circle cx='%.1f' cy='%.1f' r='4.6' fill='%s' stroke='%s' stroke-width='0.8'/>" % (
                cx + 5.6 * math.cos(a), cy + 5.6 * math.sin(a), col, INK)
        s += "<circle cx='%.1f' cy='%.1f' r='3.4' fill='%s' stroke='%s' stroke-width='0.8'/>" % (
            cx, cy, C["orange"] if col == C["yellow"] else C["yellow"], INK)
    elif kind == "block":
        s += ("<rect x='%.1f' y='%.1f' width='19' height='19' rx='3' fill='%s' stroke='%s' stroke-width='1.4'/>"
              % (cx - 9.5, cy - 9.5, col, INK))
    elif kind == "cookie":
        s += "<circle cx='%.1f' cy='%.1f' r='9.5' fill='%s' stroke='%s' stroke-width='1.2'/>" % (cx, cy, col, INK)
        for dx, dy in [(-4, -3), (3, -4), (0, 3), (5, 3), (-4, 4)]:
            s += "<circle cx='%.1f' cy='%.1f' r='1.5' fill='#5a3a1a'/>" % (cx + dx, cy + dy)
    elif kind == "balloon":
        s += ("<path d='M%.1f %.1f q-2 4 1 7' fill='none' stroke='%s' stroke-width='1'/>" % (cx, cy + 6, INK)
              + "<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='%s'/>" % (cx, cy + 4, cx - 2, cy + 7, cx + 2, cy + 7, col)
              + "<ellipse cx='%.1f' cy='%.1f' rx='7' ry='8.5' fill='%s' stroke='%s' stroke-width='1.2'/>" % (cx, cy - 3, col, INK))
    elif kind == "car":
        s += ("<rect x='%.1f' y='%.1f' width='10' height='6' rx='2' fill='%s' stroke='%s' stroke-width='1.2'/>"
              % (cx - 5, cy - 7, col, INK)
              + "<rect x='%.1f' y='%.1f' width='21' height='8' rx='2' fill='%s' stroke='%s' stroke-width='1.2'/>"
              % (cx - 10.5, cy - 2, col, INK)
              + "<circle cx='%.1f' cy='%.1f' r='3' fill='%s'/>" % (cx - 6, cy + 6.5, INK)
              + "<circle cx='%.1f' cy='%.1f' r='3' fill='%s'/>" % (cx + 6, cy + 6.5, INK))
    elif kind == "duck":
        s += ("<ellipse cx='%.1f' cy='%.1f' rx='9' ry='6' fill='%s' stroke='%s' stroke-width='1.2'/>" % (cx + 2, cy + 4, col, INK)
              + "<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='%s' stroke='%s' stroke-width='0.8'/>"
              % (cx - 7.5, cy - 6, cx - 11.5, cy - 4.5, cx - 7.5, cy - 3, C["orange"], INK)
              + "<circle cx='%.1f' cy='%.1f' r='4.6' fill='%s' stroke='%s' stroke-width='1.2'/>" % (cx - 4, cy - 5, col, INK)
              + "<circle cx='%.1f' cy='%.1f' r='1.1' fill='%s'/>" % (cx - 4.5, cy - 6, INK))
    else:
        raise ValueError(kind)
    return s + "</g>"


def cross(cx, cy):
    return ("<g data-x='1'><line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2.6' stroke-linecap='round'/>"
            "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2.6' stroke-linecap='round'/></g>"
            % (cx - 10, cy - 10, cx + 10, cy + 10, RED, cx - 10, cy + 10, cx + 10, cy - 10, RED))


def group_body(x0, y0, n, kind, col=None, cols=5, gap5=0):
    """n objects in rows of `cols`; an extra gap after every 5 in a row (like a ten-frame)."""
    s, centers = [], []
    for i in range(n):
        r, c = divmod(i, cols)
        cx = x0 + c * PITCH + PITCH / 2 + (gap5 if c >= 5 else 0)
        cy = y0 + r * PITCH + PITCH / 2
        centers.append((cx, cy))
        s.append(obj(kind, cx, cy, col))
    ncol = min(n, cols)
    w = ncol * PITCH + (gap5 if ncol > 5 else 0)
    h = ((n + cols - 1) // cols) * PITCH
    return "".join(s), w, h, centers


def plural(n, kind):
    word = dict(fish="fish", balloon="balloons").get(kind, kind + "s")
    return word if n != 1 else kind


def join_svg(a, b, kind):
    """Add to: a objects, then b more inside a dashed box."""
    o, gap = 6, 26
    b1, w1, h1, _ = group_body(o, o + 4, a, kind)
    b2, w2, h2, _ = group_body(o + w1 + gap + 6, o + 4, b, kind)
    box = ("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' rx='8' fill='none' stroke='%s' stroke-width='1.6' "
           "stroke-dasharray='5 3'/>" % (o + w1 + gap, o, w2 + 12, h2 + 8, GREEN))
    W, H = o + w1 + gap + w2 + 12 + o, o + max(h1, h2) + 8 + o
    svg = svg_wrap(int(W + 0.99), int(H + 0.99), b1 + box + b2, "picture: %d %s and %d more" % (a, plural(a, kind), b))
    assert svg.count("<g data-o='1'>") == a + b
    return svg


def take_svg(a, b, kind):
    """Take from: a objects in rows of 10; the last b are crossed out."""
    o = 6
    body, w, h, cen = group_body(o, o, a, kind, cols=10, gap5=8)
    xs = "".join(cross(cx, cy) for cx, cy in cen[a - b:])
    svg = svg_wrap(int(w + 2 * o + 0.99), int(h + 2 * o + 0.99), body + xs,
                   "picture: %d %s, %d crossed out" % (a, plural(a, kind), b))
    assert svg.count("<g data-o='1'>") == a and svg.count("<g data-x='1'>") == b
    return svg


def two_color_svg(a, b, kind, c1, c2):
    """Put together: a objects of one color and b of another, side by side."""
    o, gap = 6, 22
    b1, w1, h1, _ = group_body(o, o, a, kind, c1)
    b2, w2, h2, _ = group_body(o + w1 + gap, o, b, kind, c2)
    W, H = o + w1 + gap + w2 + o, o + max(h1, h2) + o
    svg = svg_wrap(int(W + 0.99), int(H + 0.99), b1 + b2,
                   "picture: %d %s %s and %d %s %s" % (a, c1, plural(a, kind), b, c2, plural(b, kind)))
    assert svg.count("<g data-o='1'>") == a + b
    return svg


def rows_svg(n1, n2, name1, name2, kind, lines=False):
    """Compare: two rows lined up one under the other, names at the left."""
    fs = 16
    lw = max(tw(name1, fs), tw(name2, fs))
    x0 = 8 + lw + 10
    s = [text(x0 - 10, 6 + PITCH / 2 + 6, name1, fs, anchor="end"),
         text(x0 - 10, 6 + PITCH + 8 + PITCH / 2 + 6, name2, fs, anchor="end")]
    b1, w1, _, c1 = group_body(x0, 6, n1, kind, cols=20)
    b2, w2, _, c2 = group_body(x0, 6 + PITCH + 8, n2, kind, cols=20)
    if lines:
        for (xa, ya), (xb, yb) in zip(c1, c2):
            s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1.5' stroke-dasharray='3 2'/>"
                     % (xa, ya + 11, xb, yb - 11, GREEN))
    W = x0 + max(w1, w2) + 8
    H = 6 + 2 * PITCH + 8 + 6
    svg = svg_wrap(int(W + 0.99), int(H + 0.99), "".join(s) + b1 + b2,
                   "picture: %s %d %s in a row, %s %d %s in a row" % (name1, n1, plural(n1, kind), name2, n2, plural(n2, kind)))
    assert svg.count("<g data-o='1'>") == n1 + n2
    return svg


def ppw_svg(whole, p1, p2, wl, l1, l2):
    """Part-part-whole mat: the whole on top, the two parts under it, short words under the parts."""
    fs, sfs = 20, 14
    pw = max(72, tw(l1, sfs) + 16, tw(l2, sfs) + 16)
    o = 6
    W = 2 * pw + 2 * o
    s = []
    s.append("<rect x='%d' y='%d' width='%.1f' height='38' fill='%s' stroke='%s' stroke-width='2.5'%s/>"
             % (o, o, 2 * pw, PINK if whole == "?" else FILL, RED if whole == "?" else GREEN,
                " stroke-dasharray='5 3'" if whole == "?" else ""))
    tx = o + pw
    s.append("<text x='%.1f' y='%d' font-size='%d' font-weight='700' text-anchor='middle'>"
             "<tspan fill='%s'>%s</tspan><tspan fill='%s' font-size='%d' dx='6'>%s</tspan></text>"
             % (tx, o + 26, fs, RED if whole == "?" else INK, whole, INK, sfs, wl))
    for k, (v, lab) in enumerate([(p1, l1), (p2, l2)]):
        x = o + k * pw
        unk = v == "?"
        s.append("<rect x='%.1f' y='%d' width='%.1f' height='38' fill='%s' stroke='%s' stroke-width='2.5'%s/>"
                 % (x, o + 38, pw, PINK if unk else FILL, RED if unk else GREEN, " stroke-dasharray='5 3'" if unk else ""))
        s.append(text(x + pw / 2, o + 38 + 26, v, fs, col=RED if unk else INK))
        s.append(text(x + pw / 2, o + 76 + 18, lab, sfs))
    return svg_wrap(int(W + 0.99), o + 76 + 24, "".join(s), "part-part-whole mat: %s %s, parts %s and %s" % (whole, wl, p1, p2))


# ------------------------------------------------------------ contexts: add to / take from
# s start, ss some at start, ad add, ads add some, tk take, tks take some, now, qn now?, qs start?, qa added?, qt taken?
# k = picture kind (None: no picture), lab = (start, change) words for the mat when adding / taking
JOIN = [
    dict(s="{N} had {a} stickers.", ss="{N} had some stickers.",
         ad="{He} got {b} more.", ads="{He} got some more.",
         tk="{He} gave {b} to a friend.", tks="{He} gave some to a friend.",
         now="Now {he} has {c} stickers.", qn="How many stickers does {N} have now?",
         qs="How many stickers did {N} have at first?", qa="How many stickers did {N} get?",
         qt="How many stickers did {N} give away?", u=("sticker", "stickers"), k="star"),
    dict(s="There were {a} ducks in a pond.", ss="Some ducks were in a pond.",
         ad="{b} more ducks came.", ads="Some more ducks came.",
         tk="{b} ducks swam away.", tks="Some ducks swam away.",
         now="Now there are {c} ducks in the pond.", qn="How many ducks are in the pond now?",
         qs="How many ducks were in the pond at first?", qa="How many ducks came?",
         qt="How many ducks swam away?", u=("duck", "ducks"), k="duck"),
    dict(s="{N} had {a} apples.", ss="{N} had some apples.",
         ad="{He} picked {b} more.", ads="{He} picked some more.",
         tk="{He} used {b} to make a pie.", tks="{He} used some to make a pie.",
         now="Now {he} has {c} apples.", qn="How many apples does {N} have now?",
         qs="How many apples did {N} have at first?", qa="How many apples did {N} pick?",
         qt="How many apples did {N} use?", u=("apple", "apples"), k="apple"),
    dict(s="A pet store had {a} fish in a tank.", ss="A pet store had some fish in a tank.",
         ad="The store got {b} more fish.", ads="The store got some more fish.",
         tk="The store sold {b} fish.", tks="The store sold some fish.",
         now="Now there are {c} fish in the tank.", qn="How many fish are in the tank now?",
         qs="How many fish were in the tank at first?", qa="How many fish did the store get?",
         qt="How many fish did the store sell?", u=("fish", "fish"), k="fish"),
    dict(s="{N} had {a} balls.", ss="{N} had some balls.",
         ad="{He} found {b} more.", ads="{He} found some more.",
         tk="{He} lost {b} at the park.", tks="{He} lost some at the park.",
         now="Now {he} has {c} balls.", qn="How many balls does {N} have now?",
         qs="How many balls did {N} have at first?", qa="How many balls did {N} find?",
         qt="How many balls did {N} lose?", u=("ball", "balls"), k="ball"),
    dict(s="{N} picked {a} flowers.", ss="{N} picked some flowers.",
         ad="Then {he} picked {b} more.", ads="Then {he} picked some more.",
         tk="{He} gave {b} to {his} grandma.", tks="{He} gave some to {his} grandma.",
         now="Now {he} has {c} flowers.", qn="How many flowers does {N} have now?",
         qs="How many flowers did {N} pick at first?", qa="How many more flowers did {N} pick?",
         qt="How many flowers did {N} give to {his} grandma?", u=("flower", "flowers"), k="flower"),
    dict(s="{N} made a tower with {a} blocks.", ss="{N} made a tower with some blocks.",
         ad="{He} put on {b} more blocks.", ads="{He} put on some more blocks.",
         tk="{He} took off {b} blocks.", tks="{He} took off some blocks.",
         now="Now the tower has {c} blocks.", qn="How many blocks are in the tower now?",
         qs="How many blocks were in the tower at first?", qa="How many blocks did {N} put on?",
         qt="How many blocks did {N} take off?", u=("block", "blocks"), k="block"),
    dict(s="There were {a} cookies on a plate.", ss="There were some cookies on a plate.",
         ad="Dad put {b} more on the plate.", ads="Dad put some more on the plate.",
         tk="The children ate {b} cookies.", tks="The children ate some cookies.",
         now="Now there are {c} cookies on the plate.", qn="How many cookies are on the plate now?",
         qs="How many cookies were on the plate at first?", qa="How many cookies did Dad put on the plate?",
         qt="How many cookies did the children eat?", u=("cookie", "cookies"), k="cookie"),
    dict(s="{N} had {a} balloons.", ss="{N} had some balloons.",
         ad="{He} got {b} more.", ads="{He} got some more.",
         tk="{b} of them popped.", tks="Some of them popped.",
         now="Now {he} has {c} balloons.", qn="How many balloons does {N} have now?",
         qs="How many balloons did {N} have at first?", qa="How many balloons did {N} get?",
         qt="How many balloons popped?", u=("balloon", "balloons"), k="balloon"),
    dict(s="{N} had {a} toy cars.", ss="{N} had some toy cars.",
         ad="{He} got {b} more for {his} birthday.", ads="{He} got some more for {his} birthday.",
         tk="{He} gave {b} to {his} cousin.", tks="{He} gave some to {his} cousin.",
         now="Now {he} has {c} toy cars.", qn="How many toy cars does {N} have now?",
         qs="How many toy cars did {N} have at first?", qa="How many toy cars did {N} get?",
         qt="How many toy cars did {N} give away?", u=("toy car", "toy cars"), k="car"),
    dict(s="There were {a} children on a bus.", ss="Some children were on a bus.",
         ad="At the stop, {b} more got on.", ads="At the stop, some more got on.",
         tk="At the stop, {b} got off.", tks="At the stop, some got off.",
         now="Now there are {c} children on the bus.", qn="How many children are on the bus now?",
         qs="How many children were on the bus at first?", qa="How many children got on?",
         qt="How many children got off?", u=("child", "children"), k=None),
    dict(s="There were {a} frogs on a log.", ss="Some frogs were on a log.",
         ad="{b} more frogs jumped on.", ads="Some more frogs jumped on.",
         tk="{b} frogs jumped off.", tks="Some frogs jumped off.",
         now="Now there are {c} frogs on the log.", qn="How many frogs are on the log now?",
         qs="How many frogs were on the log at first?", qa="How many frogs jumped on?",
         qt="How many frogs jumped off?", u=("frog", "frogs"), k=None),
    dict(s="{N} had {a} crayons.", ss="{N} had some crayons.",
         ad="{His} dad gave {him} {b} more.", ads="{His} dad gave {him} some more.",
         tk="{He} lost {b} crayons.", tks="{He} lost some crayons.",
         now="Now {he} has {c} crayons.", qn="How many crayons does {N} have now?",
         qs="How many crayons did {N} have at first?", qa="How many crayons did {his} dad give {him}?",
         qt="How many crayons did {N} lose?", u=("crayon", "crayons"), k=None),
    dict(s="There were {a} birds in a tree.", ss="Some birds were in a tree.",
         ad="{b} more birds flew in.", ads="Some more birds flew in.",
         tk="{b} birds flew away.", tks="Some birds flew away.",
         now="Now there are {c} birds in the tree.", qn="How many birds are in the tree now?",
         qs="How many birds were in the tree at first?", qa="How many birds flew in?",
         qt="How many birds flew away?", u=("bird", "birds"), k=None),
]


def P1(p):
    d = dict(p)
    d["him"] = "her" if p["he"] == "she" else "him"
    return d


# ------------------------------------------------------------ contexts: put together / take apart
# tot: total unknown, part: one part unknown, pu: unit of the part asked, lab: mat words, k/c1/c2: picture
PARTS = [
    dict(tot="{N} has {a} red balls and {b} blue balls. How many balls does {he} have?",
         part="{N} has {c} balls. {a} are red. The rest are blue. How many blue balls does {he} have?",
         u=("ball", "balls"), lab=("red", "blue"), k="ball", c1="red", c2="blue"),
    dict(tot="A bowl has {a} red apples and {b} green apples. How many apples are in the bowl?",
         part="A bowl has {c} apples. {a} are red. The rest are green. How many green apples are there?",
         u=("apple", "apples"), lab=("red", "green"), k="apple", c1="red", c2="green"),
    dict(tot="A tank has {a} orange fish and {b} blue fish. How many fish are in the tank?",
         part="A tank has {c} fish. {a} are orange. The rest are blue. How many blue fish are there?",
         u=("fish", "fish"), lab=("orange", "blue"), k="fish", c1="orange", c2="blue"),
    dict(tot="{N} picked {a} pink flowers and {b} yellow flowers. How many flowers did {he} pick?",
         part="{N} picked {c} flowers. {a} were pink. The rest were yellow. How many yellow flowers did {he} pick?",
         u=("flower", "flowers"), lab=("pink", "yellow"), k="flower", c1="pink", c2="yellow"),
    dict(tot="{N} has {a} green blocks and {b} yellow blocks. How many blocks does {he} have?",
         part="{N} has {c} blocks. {a} are green. The rest are yellow. How many yellow blocks does {he} have?",
         u=("block", "blocks"), lab=("green", "yellow"), k="block", c1="green", c2="yellow"),
    dict(tot="There are {a} red balloons and {b} purple balloons. How many balloons are there?",
         part="There are {c} balloons. {a} are red. The rest are purple. How many purple balloons are there?",
         u=("balloon", "balloons"), lab=("red", "purple"), k="balloon", c1="red", c2="purple"),
    dict(tot="{N} has {a} gold stars and {b} silver stars. How many stars does {he} have?",
         part="{N} has {c} stars. {a} are gold. The rest are silver. How many silver stars does {he} have?",
         u=("star", "stars"), lab=("gold", "silver"), k="star", c1="gold", c2="silver"),
    dict(tot="{N} has {a} red cars and {b} blue cars. How many cars does {he} have?",
         part="{N} has {c} toy cars. {a} are red. The rest are blue. How many blue cars does {he} have?",
         u=("car", "cars"), lab=("red", "blue"), k="car", c1="red", c2="blue"),
    dict(tot="There are {a} girls and {b} boys at the park. How many children are at the park?",
         part="There are {c} children at the park. {a} are girls. How many boys are at the park?",
         u=("child", "children"), pu=("boy", "boys"), lab=("girls", "boys"), k=None),
    dict(tot="A pet shop has {a} cats and {b} dogs. How many pets does it have?",
         part="A pet shop has {c} cats and dogs. {a} are cats. How many dogs are there?",
         u=("pet", "pets"), pu=("dog", "dogs"), lab=("cats", "dogs"), k=None),
    dict(tot="{N} read {a} books in May and {b} books in June. How many books did {he} read?",
         part="{N} read {c} books in May and June. {He} read {a} in May. How many books did {he} read in June?",
         u=("book", "books"), lab=("May", "June"), k=None),
    dict(tot="A farm has {a} brown eggs and {b} white eggs. How many eggs are there?",
         part="A farm has {c} eggs. {a} are brown. The rest are white. How many white eggs are there?",
         u=("egg", "eggs"), lab=("brown", "white"), k=None),
    dict(tot="There are {a} big dogs and {b} small dogs at the park. How many dogs are there?",
         part="There are {c} dogs at the park. {a} are big. The rest are small. How many small dogs are there?",
         u=("dog", "dogs"), lab=("big", "small"), k=None),
    dict(tot="{N} has {a} pencils and {b} crayons in a box. How many things are in the box?",
         part="{N} has {c} pencils and crayons in a box. {a} are pencils. How many crayons are there?",
         u=("thing", "things"), pu=("crayon", "crayons"), lab=("pencils", "crayons"), k=None),
]


# ------------------------------------------------------------ contexts: compare
def has_ctx(T, k, one=None):
    return dict(has="{X} has {n} %s." % T, more="{X} has {d} more %s than {Y}." % T,
                fewer="{X} has {d} fewer %s than {Y}." % T,
                qm="How many more %s does {X} have than {Y}?" % T, qf="How many fewer %s does {X} have than {Y}?" % T,
                qh="How many %s does {X} have?" % T, u=(one or T[:-1], T), k=k)


CMP = [has_ctx("apples", "apple"), has_ctx("stickers", "star"), has_ctx("balls", "ball"), has_ctx("fish", "fish", "fish"),
       has_ctx("flowers", "flower"), has_ctx("blocks", "block"), has_ctx("cookies", "cookie"), has_ctx("balloons", "balloon"),
       has_ctx("toy cars", "car"), has_ctx("shells", None), has_ctx("crayons", None), has_ctx("rocks", None),
       dict(has="{X} read {n} books.", more="{X} read {d} more books than {Y}.", fewer="{X} read {d} fewer books than {Y}.",
            qm="How many more books did {X} read than {Y}?", qf="How many fewer books did {X} read than {Y}?",
            qh="How many books did {X} read?", u=("book", "books"), k=None),
       dict(has="{X} hopped {n} times.", more="{X} hopped {d} more times than {Y}.", fewer="{X} hopped {d} fewer times than {Y}.",
            qm="How many more times did {X} hop than {Y}?", qf="How many fewer times did {X} hop than {Y}?",
            qh="How many times did {X} hop?", u=("time", "times"), k=None)]


# ------------------------------------------------------------ stories (one builder for every kind)
# AR add to, result unknown     TR take from, result unknown
# CA add to, change unknown     CT take from, change unknown
# SA add to, start unknown      ST take from, start unknown
# PT put together (total)       PA take apart (one part unknown)
# CD compare: how many more     CF compare: how many fewer
# CB compare: bigger unknown    CS compare: smaller unknown
def count_on(a, t):
    return ", ".join(str(x) for x in range(a + 1, t + 1))


def build(kind, c, p, x, y):
    """x, y: the two story numbers in story order. Returns q (no picture), ans, wrong list, e, eq, unit, nums."""
    U = lambda v: fmt(v, c["u"])
    pp = P1(p) if isinstance(p, dict) else {}
    if kind == "AR":
        a, b = x, y
        ans = a + b
        q = say(c["s"] + " " + c["ad"] + " " + c["qn"], pp, a=a, b=b)
        e = "%d and %d more. Put them together: %d + %d = %d." % (a, b, a, b, ans)
        if a >= b and b <= 4:
            e += " Count on from %d: %s." % (a, count_on(a, ans))
        wrong = [abs(a - b), max(a, b), ans - 1, ans + 1, ans + 2, ans - 2]
        eq = "%d + %d = %s" % (a, b, BOX)
    elif kind == "TR":
        a, b = x, y
        ans = a - b
        q = say(c["s"] + " " + c["tk"] + " " + c["qn"], pp, a=a, b=b)
        e = "Start with %d. Take away %d: %d − %d = %d." % (a, b, a, b, ans)
        wrong = [a + b, b, ans + 1, ans - 1, a, ans + 2]
        eq = "%d − %d = %s" % (a, b, BOX)
    elif kind == "CA":
        a, t = x, y
        ans = t - a
        q = say(c["s"] + " " + c["ads"] + " " + c["now"] + " " + c["qa"], pp, a=a, c=t)
        e = "The change is missing: %d + %s = %d. " % (a, BOX, t)
        e += ("Count on from %d to %d: %s. That is %d." % (a, t, count_on(a, t), ans) if ans <= 5
              else "Subtract: %d − %d = %d." % (t, a, ans))
        wrong = [a + t, t, a, ans + 1, ans - 1, ans + 2]
        eq = "%d + %s = %d" % (a, BOX, t)
        U = lambda v: fmt(v, c["u"])
    elif kind == "CT":
        a, t = x, y
        ans = a - t
        q = say(c["s"] + " " + c["tks"] + " " + c["now"] + " " + c["qt"], pp, a=a, c=t)
        e = ("The change is missing: %d − %s = %d. Subtract: %d − %d = %d. Check: %d − %d = %d."
             % (a, BOX, t, a, t, ans, a, ans, t))
        wrong = [a + t, a, t, ans + 1, ans - 1, ans + 2]
        eq = "%d − %s = %d" % (a, BOX, t)
    elif kind == "SA":
        b, t = x, y
        ans = t - b
        q = say(c["ss"] + " " + c["ad"] + " " + c["now"] + " " + c["qs"], pp, b=b, c=t)
        e = ("The start is missing: %s + %d = %d. Take away the %d that came: %d − %d = %d."
             % (BOX, b, t, b, t, b, ans))
        wrong = [t + b, t, b, ans + 1, ans - 1, ans + 2]
        eq = "%s + %d = %d" % (BOX, b, t)
    elif kind == "ST":
        b, t = x, y
        ans = t + b
        q = say(c["ss"] + " " + c["tk"] + " " + c["now"] + " " + c["qs"], pp, b=b, c=t)
        e = ("The start is missing: %s − %d = %d. Put the %d back: %d + %d = %d."
             % (BOX, b, t, b, t, b, ans))
        wrong = [abs(t - b), t, b, ans + 1, ans - 1, ans + 2]
        eq = "%s − %d = %d" % (BOX, b, t)
    elif kind == "PT":
        a, b = x, y
        ans = a + b
        q = say(c["tot"], pp, a=a, b=b)
        e = "You know both parts. Put them together: %d + %d = %d." % (a, b, ans)
        wrong = [abs(a - b), max(a, b), ans - 1, ans + 1, ans + 2, ans - 2]
        eq = "%d + %d = %s" % (a, b, BOX)
    elif kind == "PA":
        t, a = x, y
        ans = t - a
        q = say(c["part"], pp, c=t, a=a)
        U = lambda v: fmt(v, c.get("pu", c["u"]))
        e = ("You know the whole (%d) and one part (%d). Subtract: %d − %d = %d. Check: %d + %d = %d."
             % (t, a, t, a, ans, a, ans, t))
        wrong = [t + a, t, a, ans + 1, ans - 1, ans + 2]
        eq = "%d + %s = %d" % (a, BOX, t)
    elif kind in ("CD", "CF"):
        X, Y, big, small = p                              # X has big, Y has small
        ans = big - small
        q = say(c["has"], {}, X=X, n=big) + " " + say(c["has"], {}, X=Y, n=small) + " "
        if kind == "CD":
            q += say(c["qm"], {}, X=X, Y=Y)
            e = "Match them up. %s has %d extra. Find the difference: %d − %d = %d. Do not add." % (X, ans, big, small, ans)
        else:
            q += say(c["qf"], {}, X=Y, Y=X)
            e = "Match them up. %s has %d fewer. Find the difference: %d − %d = %d." % (Y, ans, big, small, ans)
        e += " Check: %d + %d = %d." % (small, ans, big)
        wrong = [big + small, big, small, ans + 1, ans - 1, ans + 2]
        eq = "%d + %s = %d" % (small, BOX, big)
        x, y = big, small
    elif kind == "CB":
        X, Y, n, d = p                                    # Y has n, X has d more than Y
        ans = n + d
        q = (say(c["has"], {}, X=Y, n=n) + " " + say(c["more"], {}, X=X, d=d, Y=Y) + " " + say(c["qh"], {}, X=X))
        e = "%s has %d more than %s. Add: %d + %d = %d." % (X, d, Y, n, d, ans)
        wrong = [abs(n - d), n, d, ans + 1, ans - 1, ans + 2]
        eq = "%d + %d = %s" % (n, d, BOX)
        x, y = n, d
    elif kind == "CS":
        X, Y, n, d = p                                    # X has n, Y has d fewer than X
        ans = n - d
        q = (say(c["has"], {}, X=X, n=n) + " " + say(c["fewer"], {}, X=Y, d=d, Y=X) + " " + say(c["qh"], {}, X=Y))
        e = "%s has %d fewer than %s. Subtract: %d − %d = %d." % (Y, d, X, n, d, ans)
        wrong = [n + d, n, d, ans + 1, ans - 1, ans + 2]
        eq = "%d − %d = %s" % (n, d, BOX)
        x, y = n, d
    else:
        raise ValueError(kind)
    assert 1 <= ans <= 20 and solve_box(eq) == ans, (kind, eq, ans)
    assert ans not in (x, y), (kind, x, y, ans)
    return dict(q=q, ans=ans, wrong=wrong, e=e + " Answer: %s." % U(ans), eq=eq, U=U, nums=(x, y))


def solve_box(eq):
    """Whole-number value of ☐ that makes the equation true (None if there is none)."""
    for v in range(0, 61):
        l, r = eq.replace(MINUS, "-").replace(BOX, str(v)).split(" = ")
        if eval(l) == eval(r):
            return v
    return None


# ------------------------------------------------------------ number pickers
def pick(rnd, used, gen, ok):
    for _ in range(10000):
        v = gen()
        if ok(*v) and v not in used:
            used.add(v)
            return v
    raise RuntimeError("no numbers")


class Ctx:
    """Cycles through a context list in a shuffled order; can ask for one with a picture."""
    def __init__(self, rnd, lst):
        self.rnd, self.lst = rnd, lst
        self.order = []

    def get(self, pic=False):
        if not self.order:
            self.order = list(self.lst)
            self.rnd.shuffle(self.order)
        for i, c in enumerate(self.order):
            if not pic or c["k"]:
                return self.order.pop(i)
        self.order = []
        return self.get(pic)


def item(b, rnd, pic=""):
    return mcq(fig(pic) + b["q"] if pic else b["q"], b["U"](b["ans"]), [b["U"](v) for v in b["wrong"]], b["e"], rnd)


# ------------------------------------------------------------ set 1: add to / take from (result unknown)
def set_result(rnd, P, J):
    ops = []
    for _ in range(2):
        h = ["AR"] * 5 + ["TR"] * 5
        rnd.shuffle(h)
        ops += h
    used = set()
    its = []
    for i, op in enumerate(ops):
        pic = i < 14
        c = J.get(pic)
        small = i < 10
        R = rnd.randint
        if op == "AR":
            if small:
                a, b = pick(rnd, used, lambda: (R(2, 8), R(2, 6)), lambda a, b: a + b <= 10 and a != b)
            else:
                a, b = pick(rnd, used, lambda: (R(4, 12), R(3, 9)),
                            lambda a, b: 11 <= a + b <= 20 and a != b and (not pic or a <= 10))
        else:
            if small:
                a, b = pick(rnd, used, lambda: (R(5, 10), R(2, 6)), lambda a, b: a - b >= 2 and a - b != b)
            else:
                a, b = pick(rnd, used, lambda: (R(11, 19), R(2, 9)), lambda a, b: a - b >= 3 and a - b != b)
        bb = build(op, c, P.one(), a, b)
        svg = ""
        if pic:
            svg = join_svg(a, b, c["k"]) if op == "AR" else take_svg(a, b, c["k"])
        its.append(item(bb, rnd, svg))
    return {"title": "Add to and take from", "items": its}


# ------------------------------------------------------------ set 2: put together / take apart
def set_parts(rnd, P, Pc):
    kinds = []
    for _ in range(2):
        h = ["PT"] * 5 + ["PA"] * 5
        rnd.shuffle(h)
        kinds += h
    used = set()
    its = []
    R = rnd.randint
    for i, k in enumerate(kinds):
        small = i < 8
        if k == "PT":
            pic = i < 12
            c = Pc.get(pic)
            if small:
                a, b = pick(rnd, used, lambda: (R(2, 7), R(2, 7)), lambda a, b: 5 <= a + b <= 10 and a != b)
            else:
                a, b = pick(rnd, used, lambda: (R(3, 10), R(3, 10)), lambda a, b: 11 <= a + b <= 20 and a != b)
            bb = build("PT", c, P.one(), a, b)
            if pic:
                svg = two_color_svg(a, b, c["k"], c["c1"], c["c2"])
            else:
                svg = ppw_svg("?", str(a), str(b), "in all", c["lab"][0], c["lab"][1])
        else:
            c = Pc.get()
            if small:
                t, a = pick(rnd, used, lambda: (R(6, 10), R(2, 8)), lambda t, a: t - a >= 2 and t - a != a)
            else:
                t, a = pick(rnd, used, lambda: (R(11, 20), R(3, 12)), lambda t, a: t - a >= 3 and t - a != a)
            bb = build("PA", c, P.one(), t, a)
            svg = ppw_svg(str(t), str(a), "?", "in all", c["lab"][0], c["lab"][1]) if i < 16 else ""
        its.append(item(bb, rnd, svg))
    return {"title": "Put together and take apart", "items": its}


# ------------------------------------------------------------ set 3: compare
def set_compare(rnd, P, Cc):
    first = ["CD", "CF"] * 6
    rnd.shuffle(first)
    last = ["CB", "CS"] * 4
    rnd.shuffle(last)
    used = set()
    its = []
    R = rnd.randint
    for i, k in enumerate(first + last):
        pic = i < 8
        c = Cc.get(pic)
        X, Y = P.two()
        if k in ("CD", "CF"):
            if i < 8:
                big, small = pick(rnd, used, lambda: (R(5, 10), R(2, 8)), lambda b, s: b - s >= 2 and b - s != s)
            else:
                big, small = pick(rnd, used, lambda: (R(11, 18), R(4, 14)), lambda b, s: b - s >= 3 and b - s != s)
            bb = build(k, c, (X, Y, big, small), 0, 0)
            svg = rows_svg(big, small, X, Y, c["k"]) if pic else ""
        elif k == "CB":
            hi = 12 if i < 16 else 20
            n, d = pick(rnd, used, lambda: (R(3, 14), R(2, 6)), lambda n, d: n + d <= hi and n != d)
            bb = build(k, c, (X, Y, n, d), 0, 0)
            svg = ""
        else:
            hi = 12 if i < 16 else 20
            n, d = pick(rnd, used, lambda: (R(6, 20), R(2, 6)), lambda n, d: n <= hi and n - d >= 2 and n - d != d)
            bb = build(k, c, (X, Y, n, d), 0, 0)
            svg = ""
        its.append(item(bb, rnd, svg))
    return {"title": "Compare: how many more or fewer?", "items": its}


# ------------------------------------------------------------ set 4: missing change or start
def set_unknown(rnd, P, J):
    a1 = ["CA", "CT"] * 5
    rnd.shuffle(a1)
    a2 = ["SA", "ST"] * 5
    rnd.shuffle(a2)
    used = set()
    its = []
    R = rnd.randint
    for i, k in enumerate(a1 + a2):
        c = J.get()
        small = i % 10 < 5
        hi = 10 if small else 20
        lo = 4 if small else 11
        if k == "CA":
            a, t = pick(rnd, used, lambda: (R(2, 14), R(lo, hi)), lambda a, t: 2 <= t - a <= 9 and t - a != a)
            mat = (str(t), str(a), "?", "now", "at first", "more")
        elif k == "CT":
            a, t = pick(rnd, used, lambda: (R(lo, hi), R(2, 14)), lambda a, t: 2 <= a - t <= 9 and a - t != t)
            mat = (str(a), str(t), "?", "at first", "left", "gone")
        elif k == "SA":
            b, t = pick(rnd, used, lambda: (R(2, 8), R(lo, hi)), lambda b, t: t - b >= 2 and t - b != b)
            mat = (str(t), "?", str(b), "now", "at first", "more")
        else:
            b, t = pick(rnd, used, lambda: (R(2, 8), R(2, 14)), lambda b, t: lo <= t + b <= hi and t != b)
            mat = ("?", str(t), str(b), "at first", "left", "gone")
        x, y = (a, t) if k in ("CA", "CT") else (b, t)
        bb = build(k, c, P.one(), x, y)
        svg = ppw_svg(*mat) if i % 10 < 6 else ""
        its.append(item(bb, rnd, svg))
    return {"title": "Find the missing change or start", "items": its}


# ------------------------------------------------------------ set 5: equations with a box and mixed stories
FORMS = ["{p} + {q} = ☐", "{p} − {q} = ☐", "{q} − {p} = ☐", "{p} + ☐ = {q}", "{q} + ☐ = {p}",
         "☐ + {p} = {q}", "☐ − {p} = {q}", "☐ − {q} = {p}", "{p} − ☐ = {q}", "{q} − ☐ = {p}"]
WHY = dict(AR="We do not know the end", TR="We do not know the end",
           CA="We do not know how many were added", CT="We do not know how many were taken away",
           SA="We do not know the start", ST="We do not know the start",
           PT="We do not know the whole", PA="We do not know one part",
           CD="We do not know the difference", CF="We do not know the difference",
           CB="We do not know the bigger number", CS="We do not know the smaller number")
SUBT = ["{p} − {q} = ☐", "{q} − {p} = ☐"]              # subtracted when the story needs adding
ADDT = ["{p} + {q} = ☐"]                                 # added the two story numbers
TRAP = dict(AR=SUBT, TR=ADDT, CA=ADDT, CT=ADDT, SA=ADDT, ST=SUBT, PT=SUBT, PA=ADDT, CD=ADDT, CF=ADDT)


def eq_item(kind, b, rnd):
    p, q = b["nums"]
    ans = b["ans"]
    bad = []
    traps = [f.format(p=p, q=q) for f in TRAP[kind]]
    traps = [x for x in traps if solve_box(x) not in (None, ans) and solve_box(x) >= 1]
    trap = traps[0]
    for f in [trap] + rnd.sample(FORMS, len(FORMS)):
        x = f.format(p=p, q=q)
        v = solve_box(x)
        if x == b["eq"] or x in bad or v is None or v == ans or v < 1:
            continue
        bad.append(x)
    assert bad[0] == trap, (kind, trap, bad)
    q = b["q"] + " Which equation matches this story?"
    e = "%s. Put the ☐ there: %s. The ☐ is %d. Answer: %s." % (WHY[kind], b["eq"], ans, b["eq"])
    return mcq(q, b["eq"], bad[:3], e, rnd)


def set_mixed(rnd, P, J, Pc, Cc):
    used = set()
    its = []
    R = rnd.randint
    eqk = ["AR", "TR", "PT", "PA", "CD", "CA", "CT", "SA", "ST", "CF"]
    rnd.shuffle(eqk)
    mix = ["CA", "ST", "CB", "CS", "PA", "CF", "SA", "CT", "PT", "AR"]
    rnd.shuffle(mix)
    for n, k in enumerate(eqk + mix):
        if k in ("AR", "TR", "CA", "CT", "SA", "ST"):
            c = J.get()
            p = P.one()
            if k == "AR":
                x, y = pick(rnd, used, lambda: (R(5, 12), R(3, 9)), lambda a, b: 11 <= a + b <= 20 and a != b)
            elif k == "TR":
                x, y = pick(rnd, used, lambda: (R(11, 19), R(3, 9)), lambda a, b: a - b >= 3 and a - b != b)
            elif k == "CA":
                x, y = pick(rnd, used, lambda: (R(4, 14), R(11, 20)), lambda a, t: 3 <= t - a <= 9 and t - a != a)
            elif k == "CT":
                x, y = pick(rnd, used, lambda: (R(11, 20), R(3, 14)), lambda a, t: 3 <= a - t <= 9 and a - t != t)
            elif k == "SA":
                x, y = pick(rnd, used, lambda: (R(3, 9), R(11, 20)), lambda b, t: t - b >= 3 and t - b != b)
            else:
                x, y = pick(rnd, used, lambda: (R(3, 9), R(4, 14)), lambda b, t: 11 <= t + b <= 20 and t != b)
            bb = build(k, c, p, x, y)
        elif k in ("PT", "PA"):
            c = Pc.get()
            if k == "PT":
                x, y = pick(rnd, used, lambda: (R(4, 12), R(4, 12)), lambda a, b: 11 <= a + b <= 20 and a != b)
            else:
                x, y = pick(rnd, used, lambda: (R(11, 20), R(4, 12)), lambda t, a: t - a >= 3 and t - a != a)
            bb = build(k, c, P.one(), x, y)
        else:
            c = Cc.get()
            X, Y = P.two()
            if k in ("CD", "CF"):
                big, small = pick(rnd, used, lambda: (R(11, 19), R(5, 15)), lambda b, s: b - s >= 3 and b - s != s)
                bb = build(k, c, (X, Y, big, small), 0, 0)
            elif k == "CB":
                nn, d = pick(rnd, used, lambda: (R(8, 15), R(3, 7)), lambda nn, d: 11 <= nn + d <= 20)
                bb = build(k, c, (X, Y, nn, d), 0, 0)
            else:
                nn, d = pick(rnd, used, lambda: (R(11, 20), R(3, 7)), lambda nn, d: nn - d != d)
                bb = build(k, c, (X, Y, nn, d), 0, 0)
        its.append(eq_item(k, bb, rnd) if n < 10 else item(bb, rnd))
    return {"title": "Equations with a ☐ and mixed stories", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


def body_html():
    return (
        "<h2>Picture the story</h2>"
        "<p>Read the story. Ask: <b>what is happening?</b> Are some added, taken away, put together or compared? "
        "Then find the number you do not know. It can be the start, the change or the end.</p>"
        "<h2>Five kinds of stories</h2>" +
        table(["Kind", "Story", "Equation"], [
            ["Add to", "Mia had 5 apples. She picked 3 more. How many now?", "5 + 3 = ☐"],
            ["Take from", "Leo had 9 balloons. 4 popped. How many are left?", "9 − 4 = ☐"],
            ["Put together", "Ava has 6 red and 5 blue balls. How many in all?", "6 + 5 = ☐"],
            ["Take apart", "Sam has 12 balls. 5 are red. The rest are blue. How many are blue?", "5 + ☐ = 12"],
            ["Compare", "Ava has 8 stickers. Leo has 5. How many more does Ava have?", "5 + ☐ = 8"],
        ]) +
        "<h2>Draw it</h2>"
        "<p>When some are added, draw them. Then count them all.</p>"
        "<figure class='sn-fig'>" + join_svg(5, 3, "apple") +
        "<figcaption>Mia had 5 apples. She picked 3 more. Count on from 5: 6, 7, 8. 5 + 3 = 8 apples.</figcaption></figure>"
        "<p>When some are taken away, draw them all. Cross out the ones that go away.</p>"
        "<figure class='sn-fig'>" + take_svg(9, 4, "balloon") +
        "<figcaption>Leo had 9 balloons. 4 popped. 5 are not crossed out. 9 − 4 = 5 balloons.</figcaption></figure>"
        "<p>A part-part-whole mat shows two parts and the whole. If you know both parts, add. "
        "If you know the whole and one part, subtract.</p>"
        "<figure class='sn-fig'>" + ppw_svg("12", "5", "?", "in all", "red", "blue") +
        "<figcaption>Sam has 12 balls. 5 are red. The rest are blue. 12 − 5 = 7 blue balls. Check: 5 + 7 = 12.</figcaption></figure>"
        "<p>To compare, line up the two rows. Match one to one. The extra ones are the answer.</p>"
        "<figure class='sn-fig'>" + rows_svg(8, 5, "Ava", "Leo", "star", lines=True) +
        "<figcaption>Ava has 8 stickers. Leo has 5. 3 of Ava's stickers have no match. "
        "Ava has 3 more. 8 − 5 = 3. Do not add.</figcaption></figure>"
        "<h2>Use a box for the missing number</h2>"
        "<p>Write an equation. Put a <b>☐</b> where the missing number goes. The box can be at the start, in the middle or at the end.</p>" +
        ex("Missing change", "Mia had 6 stickers. She got some more. Now she has 9. How many did she get?",
           "6 + ☐ = 9. Count on from 6: 7, 8, 9. That is 3.", "3 stickers") +
        ex("Missing start", "Sam had some shells. He found 4 more. Now he has 11. How many did he have at first?",
           "☐ + 4 = 11. Take away the 4 he found: 11 − 4 = 7.", "7 shells") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Adding when the story asks “how many more”", "Line up the two rows. Count the extra ones, or subtract: 8 − 5 = 3."],
            ["Adding the two numbers when the start or change is missing", "Write the equation with a ☐ first. Check your answer in the story."],
            ["Giving the bigger number as the answer", "The bigger number is the whole. The answer is the missing part."],
            ["Counting one too many or one too few", "Touch each picture once. Count on from the bigger number."],
        ])
    )


FAQ = [
    {"q": "What kinds of word problems do 1st graders solve?",
     "a": "First graders solve add to, take from, put together, take apart and compare stories with numbers up to 20. The missing number can be the start, the change or the end."},
    {"q": "How can I help my 1st grader with “how many more” problems?",
     "a": "Line up two rows of objects and match them one to one. The extra objects are the answer, so 8 − 5 = 3 or 5 + ☐ = 8."},
    {"q": "What does the box mean in an equation like ☐ + 4 = 11?",
     "a": "The box stands for the missing number. Here it is the start, and 11 − 4 = 7, so the box is 7."},
    {"q": "Should first graders use key words to solve word problems?",
     "a": "Not by themselves. Key words like “more” can trick children, so have them act out or draw the story and then decide to add or subtract."},
]


def balance(sets, rnd):
    """Spread the correct answers evenly over the 4 positions in every set."""
    for s in sets:
        targets = [0, 1, 2, 3] * 5
        rnd.shuffle(targets)
        for it, t in zip(s["items"], targets):
            c = it["c"]
            c[it["a"]], c[t] = c[t], c[it["a"]]
            it["a"] = t


def mark_large(u, pattern):
    """Tag pictures that must print larger so the objects stay easy to count."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def check(sets):
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5), s["title"]
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            vals = [c.split(" ")[0] for c in it["c"]]
            assert BOX in it["c"][0] or len(set(vals)) == 4, it
            plain = re.sub(r"<[^>]+>", " ", it["q"])
            assert plain not in seen, plain
            seen.add(plain)
            for t in [plain, it["e"]] + it["c"]:
                assert "\\" not in t and ".." not in t and "  ." not in t
                assert not re.search(r"\b1 (apples|stickers|balls|flowers|blocks|cookies|balloons|toy cars|ducks|frogs|"
                                     r"crayons|birds|children|stars|cars|eggs|dogs|pets|books|boys|times|things)\b", t), t
                assert re.search(r"\b(\d+) (child|apple|sticker|ball|flower|block|cookie|balloon|duck|frog|crayon|bird|star|"
                                 r"car|egg|dog|pet|book|boy|time|thing)\b(?!s)", t) is None or \
                    all(m == "1" for m in re.findall(r"\b(\d+) (?:child|apple|sticker|ball|flower|block|cookie|balloon|duck|"
                                                     r"frog|crayon|bird|star|car|egg|dog|pet|book|boy|time|thing)\b(?!s)", t)), t


def gen():
    rnd = random.Random(102)
    P = People(rnd)
    J, Pc, Cc = Ctx(rnd, JOIN), Ctx(rnd, PARTS), Ctx(rnd, CMP)
    sets = [set_result(rnd, P, J), set_parts(rnd, P, Pc), set_compare(rnd, P, Cc), set_unknown(rnd, P, J),
            set_mixed(rnd, P, J, Pc, Cc)]
    balance(sets, rnd)
    check(sets)
    u = {
        "country": "us", "subject": "math", "grade": "grade-1", "slug": "word-problems-within-20", "sort": 2,
        "updated": UPDATED, "pdf_url": "",
        "title": "Addition and Subtraction Word Problems within 20",
        "seo_title": "Grade 1 Word Problems within 20 Worksheets: Add To, Take From, Put Together, Compare and Missing Numbers",
        "short_title": "Word problems within 20",
        "domain": "Operations and Algebraic Thinking",
        "standard_code": "1.OA.A.1",
        "standard_url": "https://www.thecorestandards.org/Math/Content/1/OA/A/1/",
        "standard_text": "Use addition and subtraction within 20 to solve word problems involving situations of adding to, taking from, putting together, taking apart, and comparing, with unknowns in all positions, e.g., by using objects, drawings, and equations with a symbol for the unknown number to represent the problem.",
        "meta_desc": "Free Grade 1 word problem worksheets within 20: add to, take from, put together, take apart and compare stories with pictures, missing start or change, and equations with a ☐. 100 practice questions for 1st grade with an answer key.",
        "key_big": "Act out the story. Then find the missing number.",
        "key_sub": "Are some added, taken away, put together or compared? Draw it, then write an equation with a ☐ where the missing number goes. “How many more” means find the difference.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "picture")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
