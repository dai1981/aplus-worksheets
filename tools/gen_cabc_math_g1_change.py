# -*- coding: utf-8 -*-
"""
CA-BC Grade 1 Math: Change in quantity to 20 (BC Mathematics Curriculum, Patterning)
  python3 tools/gen_cabc_math_g1_change.py
Some more come (join), some go away (separate), what changed (start and now known),
same or changed, and BC word problems to 20. Canadian English, very short sentences.
Every answer and every wrong answer is computed and checked in code.
HTML attributes use single quotes (no backslashes in the JSON).
Helpers are copied from gen_caon_math_g1_word_problems.py (rewritten for BC).
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-1")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
INK = "#2b2b2b"
RED = "#c0392b"
FONT = "Arial, Helvetica, sans-serif"
MINUS = "−"
GIRLS = ["Olivia", "Ava", "Chloe", "Simran", "Jasleen", "Mei", "Hana", "Sofia", "Emma", "Leah", "Zara", "Nadia"]
BOYS = ["Liam", "Ethan", "Noah", "Arjun", "Harjot", "Wei", "Mateo", "Lucas", "Kai", "Owen", "Ryan"]

C = dict(red="#d9443a", blue="#3b7dd8", green="#3fa34d", yellow="#f2c230", orange="#f08a24",
         gold="#e8b21c", brown="#c68a4a", black="#2b2b2b", white="#ffffff")


# ------------------------------------------------------------ helpers
def lead(c):
    m = re.match(r"^(\d+) (?!more$|fewer$)", c)
    return int(m.group(1)) if m else None


def key(c):
    """Numeric choices ("12 salmon") are compared by value; word choices ("3 more") by text."""
    v = lead(c)
    return v if v is not None else c


def mcq(q, correct, cands, e, rnd):
    """4 choices: correct + the first 3 usable distractors (all different)."""
    correct = str(correct)
    keys = {key(correct)}
    pick = []
    for c in cands:
        if c is None:
            continue
        c = str(c)
        v = lead(c)
        if v is not None and not (1 <= v <= 99):
            continue
        if re.match(r"^(More|Fewer): (\d+)$", c) and int(c.split(": ")[1]) < 1:
            continue
        if key(c) in keys:
            continue
        keys.add(key(c))
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
        self.pool = [(n, "she", "her", "her") for n in GIRLS] + [(n, "he", "his", "him") for n in BOYS]
        rnd.shuffle(self.pool)
        self.i = 0

    def one(self):
        n, he, his, him = self.pool[self.i % len(self.pool)]
        self.i += 1
        return dict(N=n, he=he, He=cap(he), his=his, His=cap(his), him=him)


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    assert "'" not in label
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


def leaf_pts(cx, cy, s):
    half = [(0, -1.0), (0.16, -0.62), (0.42, -0.74), (0.34, -0.28), (0.86, -0.46), (0.74, -0.16),
            (0.98, 0.0), (0.46, 0.2), (0.52, 0.42), (0.08, 0.32)]
    pts = half + [(-x, y) for x, y in reversed(half[1:])]
    return " ".join("%.1f,%.1f" % (cx + x * s, cy + y * s) for x, y in pts)


def obj(kind, cx, cy):
    s = "<g data-o='1'>"
    if kind == "apple":
        s += ("<path d='M%.1f %.1f q1 -4 3 -5' fill='none' stroke='#7a4a1e' stroke-width='2'/>" % (cx, cy - 7)
              + "<ellipse cx='%.1f' cy='%.1f' rx='4' ry='2' fill='%s' transform='rotate(-30 %.1f %.1f)'/>"
              % (cx + 5, cy - 10, C["green"], cx + 5, cy - 10)
              + "<circle cx='%.1f' cy='%.1f' r='9' fill='%s' stroke='%s' stroke-width='1.2'/>" % (cx, cy + 1, C["red"], INK))
    elif kind == "star":
        pts = []
        for k in range(10):
            r = 11 if k % 2 == 0 else 4.6
            a = math.pi / 2 + k * math.pi / 5
            pts.append("%.1f,%.1f" % (cx + r * math.cos(a), cy - r * math.sin(a) + 1))
        s += "<polygon points='%s' fill='%s' stroke='%s' stroke-width='1.2'/>" % (" ".join(pts), C["gold"], INK)
    elif kind == "cookie":
        s += "<circle cx='%.1f' cy='%.1f' r='9.5' fill='%s' stroke='%s' stroke-width='1.2'/>" % (cx, cy, C["brown"], INK)
        for dx, dy in [(-4, -3), (3, -4), (0, 3), (5, 3), (-4, 4)]:
            s += "<circle cx='%.1f' cy='%.1f' r='1.5' fill='#5a3a1a'/>" % (cx + dx, cy + dy)
    elif kind == "card":
        s += ("<rect x='%.1f' y='%.1f' width='17' height='23' rx='2' fill='#ffffff' stroke='%s' stroke-width='1.3'/>"
              % (cx - 8.5, cy - 11.5, INK)
              + "<rect x='%.1f' y='%.1f' width='13' height='12' fill='%s'/>" % (cx - 6.5, cy - 9.5, C["blue"])
              + "<circle cx='%.1f' cy='%.1f' r='3' fill='#f3d2b5' stroke='%s' stroke-width='0.8'/>" % (cx, cy - 4.5, INK)
              + "<rect x='%.1f' y='%.1f' width='11' height='2.4' fill='%s'/>" % (cx - 5.5, cy + 5, C["red"]))
    elif kind == "puck":
        s += ("<rect x='%.1f' y='%.1f' width='20' height='7' fill='%s'/>" % (cx - 10, cy - 3, C["black"])
              + "<ellipse cx='%.1f' cy='%.1f' rx='10' ry='4' fill='%s'/>" % (cx, cy + 4, C["black"])
              + "<ellipse cx='%.1f' cy='%.1f' rx='10' ry='4' fill='#555555' stroke='%s' stroke-width='1'/>" % (cx, cy - 3, C["black"]))
    elif kind == "leaf":
        s += ("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='#8a3b12' stroke-width='1.8'/>" % (cx, cy + 2, cx, cy + 12)
              + "<polygon points='%s' fill='%s' stroke='%s' stroke-width='1'/>" % (leaf_pts(cx, cy, 11), C["orange"], INK))
    elif kind == "snowball":
        s += ("<circle cx='%.1f' cy='%.1f' r='9.5' fill='#ffffff' stroke='#5b7a99' stroke-width='1.6'/>" % (cx, cy)
              + "<path d='M%.1f %.1f q4 -4 9 -2' fill='none' stroke='#a9c1d9' stroke-width='1.4'/>" % (cx - 5, cy - 2))
    elif kind == "child":
        s += ("<path d='M%.1f %.1f q0 -8 7 -8 q7 0 7 8 z' fill='%s' stroke='%s' stroke-width='1.2'/>"
              % (cx - 7, cy + 12, C["blue"], INK)
              + "<circle cx='%.1f' cy='%.1f' r='5' fill='#f3d2b5' stroke='%s' stroke-width='1.2'/>" % (cx, cy - 5, INK))
    elif kind == "fish":
        # a spawning sockeye salmon: red body, green head, facing left
        s += ("<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='%s' stroke='%s' stroke-width='1.1' "
              "stroke-linejoin='round'/>" % (cx + 5, cy, cx + 10.5, cy - 6, cx + 10.5, cy + 6, C["red"], INK)
              + "<ellipse cx='%.1f' cy='%.1f' rx='8.5' ry='6' fill='%s' stroke='%s' stroke-width='1.1'/>"
              % (cx - 2, cy, C["red"], INK)
              + "<path d='M%.1f %.1f a8.5 6 0 0 0 0 12 q3 -6 0 -12 z' fill='%s' stroke='%s' stroke-width='1.1'/>"
              % (cx - 5, cy - 5.85, C["green"], INK)
              + "<circle cx='%.1f' cy='%.1f' r='1.3' fill='%s'/>" % (cx - 7.5, cy - 1.5, INK))
    elif kind == "eagle":
        # a bald eagle sitting: dark body, white head, yellow beak and feet
        s += ("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2'/>" % (cx - 3, cy + 9, cx - 3, cy + 13, C["yellow"])
              + "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2'/>" % (cx + 3, cy + 9, cx + 3, cy + 13, C["yellow"])
              + "<ellipse cx='%.1f' cy='%.1f' rx='7.5' ry='8' fill='#5a3a1a' stroke='%s' stroke-width='1.1'/>" % (cx, cy + 3, INK)
              + "<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='%s' stroke='%s' stroke-width='0.8'/>"
              % (cx + 3.5, cy - 9, cx + 10, cy - 6.5, cx + 3.5, cy - 4.5, C["yellow"], INK)
              + "<circle cx='%.1f' cy='%.1f' r='5.5' fill='#ffffff' stroke='%s' stroke-width='1.1'/>" % (cx, cy - 7, INK)
              + "<circle cx='%.1f' cy='%.1f' r='1.2' fill='%s'/>" % (cx + 2, cy - 8, INK))
    elif kind == "shell":
        s += ("<path d='M%.1f %.1f Q%.1f %.1f %.1f %.1f Q%.1f %.1f %.1f %.1f Z' fill='#f5b98a' stroke='%s' stroke-width='1.2'/>"
              % (cx - 4, cy + 8, cx - 16, cy - 6, cx, cy - 11, cx + 16, cy - 6, cx + 4, cy + 8, INK))
        for dx in (-7, -3.5, 0, 3.5, 7):
            s += ("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='0.9'/>"
                  % (cx, cy + 7, cx + dx * 1.2, cy - 7 + abs(dx) * 0.3, INK))
        s += "<rect x='%.1f' y='%.1f' width='8' height='4' rx='1' fill='#e59a66' stroke='%s' stroke-width='1'/>" % (cx - 4, cy + 7, INK)
    elif kind == "ball":
        s += "<circle cx='%.1f' cy='%.1f' r='10' fill='#ffffff' stroke='%s' stroke-width='1.3'/>" % (cx, cy, INK)
        pts, outs = [], []
        for k in range(5):
            a = -math.pi / 2 + k * 2 * math.pi / 5
            pts.append("%.1f,%.1f" % (cx + 4.2 * math.cos(a), cy + 4.2 * math.sin(a)))
            outs.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1.1'/>"
                        % (cx + 4.2 * math.cos(a), cy + 4.2 * math.sin(a), cx + 9.6 * math.cos(a), cy + 9.6 * math.sin(a), INK))
        s += "".join(outs) + "<polygon points='%s' fill='%s'/>" % (" ".join(pts), INK)
    else:
        raise ValueError(kind)
    return s + "</g>"


def cross(cx, cy, r=10):
    return ("<g data-x='1'><line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2.6' stroke-linecap='round'/>"
            "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2.6' stroke-linecap='round'/></g>"
            % (cx - r, cy - r, cx + r, cy + r, RED, cx - r, cy + r, cx + r, cy - r, RED))


def group_body(x0, y0, n, kind, cols=10, gap5=8):
    """n objects in rows of `cols`; an extra gap after every 5 in a row (like a ten frame)."""
    s, centers = [], []
    for i in range(n):
        r, c = divmod(i, cols)
        cx = x0 + c * PITCH + PITCH / 2 + (c // 5) * gap5
        cy = y0 + r * PITCH + PITCH / 2
        centers.append((cx, cy))
        s.append(obj(kind, cx, cy))
    ncol = min(n, cols)
    w = ncol * PITCH + ((ncol - 1) // 5) * gap5
    h = ((n + cols - 1) // cols) * PITCH
    return "".join(s), w, h, centers


def word(n, kind):
    return WORDS[kind][0 if n == 1 else 1]


WORDS = dict(apple=("apple", "apples"), star=("sticker", "stickers"), cookie=("cookie", "cookies"),
             card=("card", "cards"), puck=("puck", "pucks"), leaf=("leaf", "leaves"), snowball=("snowball", "snowballs"),
             child=("person", "people"), fish=("salmon", "salmon"), eagle=("eagle", "eagles"),
             shell=("shell", "shells"), ball=("ball", "balls"))


def join_svg(a, b, kind, c=0):
    """a objects, then b more inside a dashed box. c > 0: the last c objects are crossed out (they went away)."""
    o, gap = 6, 22
    b1, w1, h1, c1 = group_body(o, o + 4, a, kind)
    b2, w2, h2, c2 = group_body(o + w1 + gap + 6, o + 4, b, kind, cols=5)
    box = ("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' rx='8' fill='none' stroke='%s' stroke-width='1.6' "
           "stroke-dasharray='5 3'/>" % (o + w1 + gap, o, w2 + 12, h2 + 8, GREEN))
    xs = "".join(cross(x, y) for x, y in (c1 + c2)[a + b - c:]) if c else ""
    W, H = o + w1 + gap + w2 + 12 + o, o + max(h1 + 4, h2 + 8) + o
    if c:
        label = "picture: %d %s, %d more, %d crossed out" % (a, word(a, kind), b, c)
    else:
        label = "picture: %d %s and %d more" % (a, word(a, kind), b)
    svg = svg_wrap(int(W + 0.99), int(H + 0.99), b1 + box + b2 + xs, label)
    assert svg.count("<g data-o='1'>") == a + b and svg.count("<g data-x='1'>") == c
    return svg


def take_svg(a, b, kind):
    """a objects in rows of 10; the last b are crossed out."""
    o = 6
    body, w, h, cen = group_body(o, o, a, kind)
    xs = "".join(cross(cx, cy) for cx, cy in cen[a - b:])
    svg = svg_wrap(int(w + 2 * o + 0.99), int(h + 2 * o + 0.99), body + xs,
                   "picture: %d %s, %d crossed out" % (a, word(a, kind), b))
    assert svg.count("<g data-o='1'>") == a and svg.count("<g data-x='1'>") == b
    return svg


def before_now_svg(s, t, kind):
    """Before group on top, Now group below (rows of 10, lined up so they can be matched)."""
    fs = 16
    x0 = 10 + tw("Before", fs) + 12
    y1 = 6
    b1, w1, h1, _ = group_body(x0, y1, s, kind)
    y2 = y1 + h1 + 12
    b2, w2, h2, _ = group_body(x0, y2, t, kind)
    line = ("<line x1='6' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1.2' stroke-dasharray='4 3'/>"
            % (y1 + h1 + 6, x0 + max(w1, w2) + 2, y1 + h1 + 6, GREEN))
    lab = (text(x0 - 10, y1 + PITCH / 2 + 6, "Before", fs, anchor="end")
           + text(x0 - 10, y2 + PITCH / 2 + 6, "Now", fs, anchor="end", col=GREEN))
    W, H = x0 + max(w1, w2) + 8, y2 + h2 + 6
    svg = svg_wrap(int(W + 0.99), int(H + 0.99), lab + line + b1 + b2,
                   "before and now: %d %s before, %d %s now" % (s, word(s, kind), t, word(t, kind)))
    assert svg.count("<g data-o='1'>") == s + t
    return svg


# ------------------------------------------------------------ contexts
# s start, ad add, ads add some, tk take, tks take some, now, qn now?, qa added?, qt taken?
# k = picture kind, top = biggest realistic number
def ctx(s, ad, ads, tk, tks, now, qn, qa, qt, u, k, top=20):
    return dict(s=s, ad=ad, ads=ads, tk=tk, tks=tks, now=now, qn=qn, qa=qa, qt=qt, u=u, k=k, top=top)


APPLE = ctx("{N} had {a} apples.", "{He} picked {b} more.", "{He} picked some more.",
            "{He} gave {b} to friends.", "{He} gave some to friends.", "Now {he} has {c} apples.",
            "How many apples does {N} have now?", "How many apples did {he} pick?",
            "How many apples did {he} give away?", ("apple", "apples"), "apple")
STICKER = ctx("{N} had {a} stickers.", "{His} teacher gave {him} {b} more.", "{His} teacher gave {him} some more.",
              "{He} used {b} on a card.", "{He} used some on a card.", "Now {he} has {c} stickers.",
              "How many stickers does {N} have now?", "How many stickers did {he} get?",
              "How many stickers did {he} use?", ("sticker", "stickers"), "star")
COOKIE = ctx("There were {a} cookies on a plate.", "Dad baked {b} more.", "Dad baked some more.",
             "The children ate {b}.", "The children ate some.", "Now there are {c} cookies.",
             "How many cookies are on the plate now?", "How many cookies did Dad bake?",
             "How many cookies did the children eat?", ("cookie", "cookies"), "cookie")
CARD = ctx("{N} had {a} hockey cards.", "{He} got {b} more.", "{He} got some more.",
           "{He} gave {b} to {his} friend.", "{He} gave some to {his} friend.", "Now {he} has {c} cards.",
           "How many cards does {N} have now?", "How many cards did {he} get?",
           "How many cards did {he} give away?", ("card", "cards"), "card")
PUCK = ctx("There were {a} pucks on the ice.", "The coach dropped {b} more.", "The coach dropped some more.",
           "The coach picked up {b}.", "The coach picked up some.", "Now there are {c} pucks on the ice.",
           "How many pucks are on the ice now?", "How many pucks did the coach drop?",
           "How many pucks did the coach pick up?", ("puck", "pucks"), "puck")
LEAF = ctx("{N} had {a} leaves.", "{He} found {b} more.", "{He} found some more.",
           "The wind blew {b} away.", "The wind blew some away.", "Now {he} has {c} leaves.",
           "How many leaves does {N} have now?", "How many leaves did {he} find?",
           "How many leaves blew away?", ("leaf", "leaves"), "leaf")
SNOW = ctx("{N} made {a} snowballs.", "Then {he} made {b} more.", "Then {he} made some more.",
           "{He} threw {b} at a tree.", "{He} threw some at a tree.", "Now {he} has {c} snowballs.",
           "How many snowballs does {N} have now?", "How many more did {he} make?",
           "How many snowballs did {he} throw?", ("snowball", "snowballs"), "snowball")
BUS = ctx("There were {a} children on the bus.", "At the next stop, {b} more got on.", "At the next stop, some more got on.",
          "At the next stop, {b} got off.", "At the next stop, some got off.", "Now there are {c} children on the bus.",
          "How many children are on the bus now?", "How many children got on?",
          "How many children got off?", ("child", "children"), "child")
# BC word-problem contexts (set 5 and some of set 4)
SALMON = ctx("There were {a} salmon in the creek.", "Then {b} more swam in.", "Then some more swam in.",
             "Then {b} swam away.", "Then some swam away.", "Now there are {c} salmon in the creek.",
             "How many salmon are in the creek now?", "How many salmon swam in?",
             "How many salmon swam away?", ("salmon", "salmon"), "fish")
SLIDE = ctx("There were {a} kids at the slide.", "Then {b} more kids came.", "Then some more kids came.",
            "Then {b} kids went to the swings.", "Then some kids went to the swings.", "Now there are {c} kids at the slide.",
            "How many kids are at the slide now?", "How many kids came?",
            "How many kids went to the swings?", ("kid", "kids"), "child", top=16)
EAGLE = ctx("There were {a} eagles in a cedar tree.", "Then {b} more landed.", "Then some more landed.",
            "Then {b} flew away.", "Then some flew away.", "Now there are {c} eagles in the tree.",
            "How many eagles are in the tree now?", "How many eagles landed?",
            "How many eagles flew away?", ("eagle", "eagles"), "eagle")
SHELL = ctx("{N} had {a} shells.", "{He} found {b} more on the beach.", "{He} found some more on the beach.",
            "{He} gave {b} to {his} sister.", "{He} gave some to {his} sister.", "Now {he} has {c} shells.",
            "How many shells does {N} have now?", "How many shells did {he} find?",
            "How many shells did {he} give away?", ("shell", "shells"), "shell")
SKYTRAIN = ctx("There were {a} people on the SkyTrain.", "At the next station, {b} more got on.",
               "At the next station, some more got on.", "At the next station, {b} got off.",
               "At the next station, some got off.", "Now there are {c} people on the SkyTrain.",
               "How many people are on the SkyTrain now?", "How many people got on?",
               "How many people got off?", ("person", "people"), "child")
BALL = ctx("There were {a} soccer balls in the bag.", "The coach put in {b} more.", "The coach put in some more.",
           "The players took out {b}.", "The players took out some.", "Now there are {c} balls in the bag.",
           "How many balls are in the bag now?", "How many balls did the coach put in?",
           "How many balls did the players take out?", ("ball", "balls"), "ball")

GEN = [APPLE, STICKER, COOKIE, CARD, PUCK, LEAF, SNOW, BUS, SHELL, BALL]
BC = [SALMON, SLIDE, EAGLE, SALMON, SLIDE, SHELL, SKYTRAIN]


class Ctx:
    """Cycles through a context list in a shuffled order; never the same one twice in a row."""
    def __init__(self, rnd, lst):
        self.rnd, self.lst, self.order, self.last = rnd, lst, [], None

    def get(self, need=0):
        for _ in range(3):
            if not self.order:
                self.order = list(self.lst)
                self.rnd.shuffle(self.order)
            for strict in (True, False):
                for i, c in enumerate(self.order):
                    if c["top"] >= need and (not strict or c is not self.last):
                        self.last = self.order.pop(i)
                        return self.last
            self.order = []
        raise RuntimeError("no context")


def pick(used, tag, gen, ok):
    for _ in range(20000):
        v = gen()
        if ok(*v) and (tag,) + v not in used:
            used.add((tag,) + v)
            return v
    raise RuntimeError("no numbers")


# ------------------------------------------------------------ explanations
def seq(a, t):
    return ", ".join(str(x) for x in range(a + 1, t + 1))


def back(a, t):
    return ", ".join(str(x) for x in range(a - 1, t - 1, -1))


def e_add(a, b):
    s = a + b
    if b <= 3:
        return "Count on from %d: %s. So %d + %d = %d." % (a, seq(a, s), a, b, s)
    if a < 10 < s:
        k = 10 - a
        return "Make 10: %d + %d = 10. Then %d more is %d. So %d + %d = %d." % (a, k, b - k, s, a, b, s)
    return "Put them together: %d + %d = %d." % (a, b, s)


def e_sub(a, b):
    r = a - b
    if b <= 3:
        return "Count back from %d: %s. So %d %s %d = %d." % (a, back(a, r), a, MINUS, b, r)
    if r < 10 < a:
        k = a - 10
        return "Take away %d to get 10. Take away %d more to get %d. So %d %s %d = %d." % (k, b - k, r, a, MINUS, b, r)
    return "Take away: %d %s %d = %d." % (a, MINUS, b, r)


def e_change_up(s, t):
    d = t - s
    if d <= 5:
        return "Start at %d. Count on to %d: %s. That is %d more. %d + %d = %d." % (s, t, seq(s, t), d, s, d, t)
    return "Find the difference: %d %s %d = %d. Check: %d + %d = %d." % (t, MINUS, s, d, s, d, t)


def e_change_down(s, t):
    d = s - t
    if d <= 5:
        return ("There are fewer now, so some went away. Count up from %d to %d: %s. That is %d. %d %s %d = %d."
                % (t, s, seq(t, s), d, s, MINUS, d, t))
    return ("There are fewer now, so some went away. %d %s %d = %d. Check: %d %s %d = %d."
            % (s, MINUS, t, d, s, MINUS, d, t))


# ------------------------------------------------------------ the four story kinds
def story(kind, c, p, x, y, rnd, pic=True):
    """AR: some more come; TR: some go away; CA: how many came?; CT: how many went away?"""
    U = lambda v: fmt(v, c["u"])
    if kind == "AR":
        a, b = x, y
        ans = a + b
        q = say(c["s"] + " " + c["ad"] + " " + c["qn"], p, a=a, b=b)
        e = "Some more came, so there are more now. " + e_add(a, b)
        third = abs(a - b) if abs(a - b) >= 2 else ans + 1
        wrong = [a, third, ans - 1, ans + 1, b]
        svg = join_svg(a, b, c["k"]) if pic else ""
    elif kind == "TR":
        a, b = x, y
        ans = a - b
        q = say(c["s"] + " " + c["tk"] + " " + c["qn"], p, a=a, b=b)
        e = "Some went away, so there are fewer now. Do not add. " + e_sub(a, b)
        wrong = [a + b, a, rnd.choice([ans + 1, ans - 1, b]), ans + 1, ans - 1]
        svg = take_svg(a, b, c["k"]) if pic else ""
    elif kind == "CA":
        a, t = x, y
        ans = t - a
        q = say(c["s"] + " " + c["ads"] + " " + c["now"] + " " + c["qa"], p, a=a, c=t)
        e = e_change_up(a, t) + " %d is how many there are now, not how many came." % t
        wrong = [t, a, rnd.choice([a + t, ans + 1]), ans + 1, ans - 1]
        svg = before_now_svg(a, t, c["k"]) if pic else ""
    elif kind == "CT":
        a, t = x, y
        ans = a - t
        q = say(c["s"] + " " + c["tks"] + " " + c["now"] + " " + c["qt"], p, a=a, c=t)
        e = e_change_down(a, t) + " %d is how many there were at the start." % a
        wrong = [t, a, rnd.choice([a + t, ans + 1]), ans + 1, ans - 1]
        svg = before_now_svg(a, t, c["k"]) if pic else ""
    else:
        raise ValueError(kind)
    assert 2 <= ans <= 20 and max(x, y) <= 20 and ans not in (x, y), (kind, x, y)
    it = mcq((fig(svg) if svg else "") + q, U(ans), [U(v) for v in wrong], e + " Answer: %s." % U(ans), rnd)
    it["_chk"] = (kind, x, y, ans)
    return it


# ------------------------------------------------------------ set 1: some more come
def set_join(rnd, P, J, used):
    its = []
    R = rnd.randint
    for i in range(20):
        if i < 7:
            a, b = pick(used, "AR", lambda: (R(2, 8), R(2, 5)), lambda a, b: 5 <= a + b <= 10)
        elif i < 14:
            a, b = pick(used, "AR", lambda: (R(4, 12), R(2, 8)), lambda a, b: 11 <= a + b <= 15)
        else:
            a, b = pick(used, "AR", lambda: (R(8, 16), R(2, 8)), lambda a, b: 16 <= a + b <= 20)
        its.append(story("AR", J.get(a + b), P.one(), a, b, rnd))
    return {"title": "Some more come", "items": its}


# ------------------------------------------------------------ set 2: some go away
def set_take(rnd, P, J, used):
    its = []
    R = rnd.randint
    for i in range(20):
        lo, hi = [(5, 10), (11, 15), (16, 20)][0 if i < 7 else 1 if i < 14 else 2]
        a, b = pick(used, "TR", lambda: (R(lo, hi), R(2, 9)), lambda a, b: a - b >= 2 and a - b != b)
        its.append(story("TR", J.get(a), P.one(), a, b, rnd))
    return {"title": "Some go away", "items": its}


# ------------------------------------------------------------ set 3: what changed?
def set_changed(rnd, P, J, used):
    its = []
    R = rnd.randint
    kinds = []
    for _ in range(2):
        h = ["CA"] * 5 + ["CT"] * 5
        rnd.shuffle(h)
        kinds += h
    for i, k in enumerate(kinds):
        top = 12 if i < 10 else 20
        lo = 3 if i < 10 else 8
        if k == "CA":
            a, t = pick(used, "CA", lambda: (R(lo, top - 2), R(lo + 2, top)),
                        lambda a, t: 2 <= t - a <= 8 and t - a != a and (i < 10 or t >= 13))
            c = J.get(t)
        else:
            a, t = pick(used, "CT", lambda: (R(lo + 2, top), R(lo, top - 2)),
                        lambda a, t: 2 <= a - t <= 8 and a - t != t and (i < 10 or a >= 13))
            c = J.get(a)
        its.append(story(k, c, P.one(), a, t, rnd))
    return {"title": "What changed? How many came or went?", "items": its}


# ------------------------------------------------------------ set 4: same or changed?
def look_item(rnd, s, t, kind, noun):
    """Before and now pictures: choose the change (3 more / 3 fewer / The same)."""
    U = lambda v: fmt(v, noun)
    q = fig(before_now_svg(s, t, kind)) + "Before: %s. Now: %s. How did the number change?" % (U(s), U(t))
    if t > s:
        d = t - s
        right = "%d more" % d
        wrong = ["%d fewer" % d, "%d more" % t, rnd.choice(["%d more" % s, "The same"])]
        e = ("Match each one before with one now. %d are left over in the Now row. "
             "There are %d more now: %d + %d = %d." % (d, d, s, d, t))
    elif t < s:
        d = s - t
        right = "%d fewer" % d
        wrong = ["%d more" % d, "%d fewer" % t, rnd.choice(["%d fewer" % s, "The same"])]
        e = ("Match each one now with one before. %d in the Before row have no match. "
             "There are %d fewer now: %d %s %d = %d." % (d, d, s, MINUS, d, t))
    else:
        right = "The same"
        wrong = ["%d more" % s, "%d fewer" % s, "%d more" % (2 * s)]
        e = "Every one before matches one now. Nothing is left over. The number stayed the same: %d." % s
    it = mcq(q, right, wrong, e + " Answer: %s." % right, rnd)
    it["_chk"] = ("LOOK", s, t, right)
    return it


def say_item(rnd, c, p, a, b, up):
    """No picture: more or fewer now, and how many?"""
    if up:
        ans = a + b
        q = say(c["s"] + " " + c["ad"], p, a=a, b=b) + " Are there more or fewer now?"
        right = "More: %d" % ans
        wrong = ["Fewer: %d" % (a - b), "The same: %d" % a, "More: %d" % b]
        e = "Some more came, so there are more now. %d + %d = %d." % (a, b, ans)
    else:
        ans = a - b
        q = say(c["s"] + " " + c["tk"], p, a=a, b=b) + " Are there more or fewer now?"
        right = "Fewer: %d" % ans
        wrong = ["More: %d" % (a + b), "The same: %d" % a, "Fewer: %d" % b]
        e = "Some went away, so there are fewer now. Do not add. %d %s %d = %d." % (a, MINUS, b, ans)
    it = mcq(q, right, wrong, e + " Answer: %s." % right, rnd)
    it["_chk"] = ("SAY", a, b if up else -b, right)
    return it


def two_item(rnd, c, p, a, b, d):
    """Some come, then some go. Same or changed?"""
    U = lambda v: fmt(v, c["u"])
    ans = a + b - d
    q = (fig(join_svg(a, b, c["k"], d)) + say(c["s"] + " " + c["ad"], p, a=a, b=b) + " "
         + say(c["tk"], p, b=d) + " " + say(c["qn"], p))
    if b == d:
        e = "%d came and %d went away. That is no change. There are still %d." % (b, d, a)
        wrong = [a + b + d, a + b, a - d, ans + 1]
    else:
        e = "First %d + %d = %d. Then %d %s %d = %d." % (a, b, a + b, a + b, MINUS, d, ans)
        e += " There are %s than at the start." % ("more" if ans > a else "fewer")
        wrong = [a + b + d, a + b, a, abs(a - d)]
    it = mcq(q, U(ans), [U(v) for v in wrong], e + " Answer: %s." % U(ans), rnd)
    it["_chk"] = ("TWO", a, b, d, ans)
    return it


def set_same(rnd, P, used):
    its = []
    R = rnd.randint
    look_ctx = [("fish", ("salmon", "salmon")), ("eagle", ("eagle", "eagles")), ("shell", ("shell", "shells")),
                ("apple", ("apple", "apples")), ("ball", ("ball", "balls")), ("star", ("sticker", "stickers")),
                ("cookie", ("cookie", "cookies")), ("leaf", ("leaf", "leaves"))]
    rnd.shuffle(look_ctx)
    looks = ["up", "up", "up", "down", "down", "down", "same", "same"]
    rnd.shuffle(looks)
    for i, L in enumerate(looks):
        kind, noun = look_ctx[i]
        if L == "same":
            s = t = pick(used, "LS", lambda: (R(5, 12),), lambda s: True)[0]
        elif L == "up":
            s, t = pick(used, "LU", lambda: (R(4, 12), R(7, 15)), lambda s, t: 2 <= t - s <= 6 and t - s != s)
        else:
            s, t = pick(used, "LD", lambda: (R(7, 15), R(4, 12)), lambda s, t: 2 <= s - t <= 6 and s - t != t)
        its.append(look_item(rnd, s, t, kind, noun))
    S = Ctx(rnd, [SALMON, EAGLE, SLIDE, SKYTRAIN, BALL, COOKIE])
    ups = [True, True, True, False, False, False]
    rnd.shuffle(ups)
    for up in ups:
        if up:
            a, b = pick(used, "SU", lambda: (R(6, 14), R(2, 6)), lambda a, b: a + b <= 20 and a - b >= 2 and a - b != b)
        else:
            a, b = pick(used, "SD", lambda: (R(8, 18), R(2, 7)), lambda a, b: a - b >= 2 and a - b != b)
        its.append(say_item(rnd, S.get(a + b if up else a), P.one(), a, b, up))
    T = Ctx(rnd, [SALMON, EAGLE, SLIDE, STICKER, COOKIE, BALL])
    same = [True, True, True, False, False, False]
    rnd.shuffle(same)
    for sm in same:
        if sm:
            a, b, d = pick(used, "TW", lambda: (R(4, 9), R(2, 4), 0), lambda a, b, d: True)
            d = b
        else:
            a, b, d = pick(used, "TW", lambda: (R(4, 9), R(2, 5), R(2, 5)),
                           lambda a, b, d: b != d and a - d >= 2 and a + b - d not in (a, b, d) and abs(a - d) != a + b - d)
        its.append(two_item(rnd, T.get(a + b), P.one(), a, b, d))
    return {"title": "Same or changed?", "items": its}


# ------------------------------------------------------------ set 5: BC word problems to 20
def set_words(rnd, P, W, used):
    its = []
    R = rnd.randint
    first = ["AR"] * 5 + ["TR"] * 5
    rnd.shuffle(first)
    mid = ["CA"] * 3 + ["CT"] * 3
    rnd.shuffle(mid)
    last = ["CA", "CT", "CA", "CT"]
    rnd.shuffle(last)
    starts = set()
    for i, k in enumerate(first + mid + last):
        pic = i < 16
        c = W.get()
        top = c["top"]
        fresh = lambda a: (c["s"], a) not in starts
        if k == "AR":
            a, b = pick(used, "AR", lambda: (R(6, 14), R(3, 8)),
                        lambda a, b: 11 <= a + b <= min(20, top) and a != b and fresh(a))
        elif k == "TR":
            a, b = pick(used, "TR", lambda: (R(11, top), R(3, 9)), lambda a, b: a - b >= 3 and a - b != b and fresh(a))
        elif k == "CA":
            a, b = pick(used, "CA", lambda: (R(5, 15), R(11, top)), lambda a, t: 3 <= t - a <= 9 and t - a != a and fresh(a))
        else:
            a, b = pick(used, "CT", lambda: (R(11, top), R(4, 15)), lambda a, t: 3 <= a - t <= 9 and a - t != t and fresh(a))
        starts.add((c["s"], a))
        its.append(story(k, c, P.one(), a, b, rnd, pic=pic))
    return {"title": "Word problems to 20", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def body_html():
    assert 8 + 4 == 12 and 13 - 5 == 8 and 12 - 8 == 4 and 6 + 2 - 2 == 6 and 15 - 9 == 6
    return (
        "<h2>The idea: a number can change</h2>"
        "<p>Start with a group. Then something happens. <b>Some more come</b>: the number goes up. "
        "<b>Some go away</b>: the number goes down. If nothing comes or goes, it <b>stays the same</b>.</p>"
        "<p>Say it in words: “I had 8. 4 more came. Now I have 12.”</p>"
        + table(["What happens", "The number", "Example"], [
            ["Some more come", "goes up", "8 + 4 = 12"],
            ["Some go away", "goes down", "13 − 5 = 8"],
            ["Some come, the same number go", "stays the same", "6 + 2 − 2 = 6"],
        ]) +
        "<h2>Some more come</h2>"
        "<p>Show the first group. Show the ones that come. Count them all.</p>"
        "<figure class='sn-fig'>" + join_svg(8, 4, "fish") +
        "<figcaption>There were 8 salmon in the creek. 4 more swam in. Count on from 8: 9, 10, 11, 12. "
        "Now there are 12 salmon.</figcaption></figure>"
        "<h2>Some go away</h2>"
        "<p>Show them all. Cross out the ones that go away. Count the ones that are left.</p>"
        "<figure class='sn-fig'>" + take_svg(13, 5, "child") +
        "<figcaption>There were 13 kids at the slide. 5 went to the swings. 8 are left. 13 − 5 = 8 kids.</figcaption></figure>"
        "<h2>What changed?</h2>"
        "<p>Put the “before” group over the “now” group. Match them one to one. "
        "The extra ones show the change.</p>"
        "<figure class='sn-fig'>" + before_now_svg(8, 12, "apple") +
        "<figcaption>Before: 8 apples. Now: 12 apples. 4 apples have no match. 4 more came. 8 + 4 = 12.</figcaption></figure>"
        + ex("How many went away?", "There were 15 eagles in a cedar tree. Some flew away. Now there are 9. How many flew away?",
             "There are fewer now, so some went away. Count up from 9 to 15: 10, 11, 12, 13, 14, 15. That is 6.",
             "6 eagles") +
        "<h2>Same or changed?</h2>"
        "<p>Sometimes some come and then the same number go away. Then there is no change.</p>"
        "<figure class='sn-fig'>" + join_svg(6, 2, "cookie", 2) +
        "<figcaption>There were 6 cookies. Dad baked 2 more. The children ate 2. 2 came and 2 went. "
        "There are still 6 cookies.</figcaption></figure>"
        "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Adding when some went away: 13 − 5 is not 18", "Some went away, so there are fewer. Subtract: 13 − 5 = 8."],
            ["Giving the start number: “8” for 8 + 4", "The number changed. Count the new group: 12."],
            ["Giving the “now” number when asked how many came", "Count on from the start to the now number: 8 to 12 is 4."],
            ["Mixing up more and fewer", "Is the new group bigger or smaller? Bigger means some came."],
        ])
    )


FAQ = [
    {"q": "What does “change in quantity to 20” mean in BC Grade 1 math?",
     "a": "It means seeing how a group of up to 20 things changes when some come or some go away. "
          "Children show the change with objects and say it in words, like “I had 8, 4 more came, now I have 12.”"},
    {"q": "Why is change in quantity part of patterning in the BC curriculum?",
     "a": "It is an early step toward algebra. Children look at a start number, a change and a new number, "
          "and learn that adding makes a group bigger and taking away makes it smaller."},
    {"q": "How can I help my child with “how many came?” questions?",
     "a": "Start at the first number and count on to the new number, holding up a finger for each count. "
          "From 8 to 12 is 9, 10, 11, 12, so 4 came."},
    {"q": "How can my child practise change in quantity at home?",
     "a": "Use real things like crackers, toys or coins. Put out a group, add or take away a few, "
          "and ask “Are there more or fewer now? How many changed?”"},
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
    rx = re.compile(r"<svg (?=[^>]*aria-label='(?:" + pattern + "))")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def verify(sets):
    """Check every answer again from the question text and picture labels."""
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5), s["title"]
        for it in s["items"]:
            chk = it.pop("_chk")
            right = it["c"][it["a"]]
            assert len({key(c) for c in it["c"]}) == 4, it["c"]
            assert it["q"].count("<svg") <= 1
            plain = re.sub(r"<[^>]+>", " ", it["q"]).strip()
            assert plain not in seen, plain
            seen.add(plain)
            nums = [int(x) for x in re.findall(r"\d+", plain)]
            k = chk[0]
            if k in ("AR", "TR", "CA", "CT"):
                _, x, y, ans = chk
                assert lead(right) == ans and nums[:2] == [x, y], (chk, plain)
                assert ans == {"AR": x + y, "TR": x - y, "CA": y - x, "CT": x - y}[k]
            elif k == "LOOK":
                _, x, y, r = chk
                assert r == ("The same" if x == y else "%d %s" % (abs(y - x), "more" if y > x else "fewer"))
            elif k == "SAY":
                _, a, b, r = chk
                assert r == ("More: %d" % (a + b) if b > 0 else "Fewer: %d" % (a + b)) and nums[:2] == [a, abs(b)]
            elif k == "TWO":
                _, a, b, d, ans = chk
                assert lead(right) == a + b - d and nums[:3] == [a, b, d]
            m = re.search(r"aria-label='picture: (\d+) [a-z]+ and (\d+) more'", it["q"])
            if m:
                assert lead(right) == int(m.group(1)) + int(m.group(2))
            m = re.search(r"aria-label='picture: (\d+) [a-z]+, (\d+) crossed out'", it["q"])
            if m:
                assert lead(right) == int(m.group(1)) - int(m.group(2))
            m = re.search(r"aria-label='picture: (\d+) [a-z]+, (\d+) more, (\d+) crossed out'", it["q"])
            if m:
                assert lead(right) == int(m.group(1)) + int(m.group(2)) - int(m.group(3))
            m = re.search(r"aria-label='before and now: (\d+) [a-z]+ before, (\d+) [a-z]+ now'", it["q"])
            if m and lead(right) is not None:
                assert lead(right) == abs(int(m.group(1)) - int(m.group(2)))
            for t in [plain, it["e"]] + it["c"]:
                assert "\\" not in t and ".." not in t, t
                assert not re.search(r"\b1 (apples|stickers|cards|pucks|leaves|snowballs|children|cookies|eagles|"
                                     r"shells|balls|kids|people)\b", t), t
                assert not re.search(r"\b([2-9]|\d\d) (apple|sticker|card|puck|leaf|snowball|child|cookie|eagle|"
                                     r"shell|ball|kid|person)\b(?!s)", t), t


def gen():
    rnd = random.Random(51804)
    P = People(rnd)
    J, W = Ctx(rnd, GEN), Ctx(rnd, BC)
    used = set()
    sets = [set_join(rnd, P, J, used), set_take(rnd, P, J, used), set_changed(rnd, P, J, used),
            set_same(rnd, P, used), set_words(rnd, P, W, used)]
    balance(sets, rnd)
    verify(sets)
    u = {
        "country": "ca-bc", "subject": "math", "grade": "grade-1", "slug": "change-in-quantity", "sort": 4,
        "updated": UPDATED, "pdf_url": "",
        "title": "Change in Quantity to 20: Some Come, Some Go",
        "seo_title": "Grade 1 Math Change in Quantity to 20 Worksheets: Free, with Answer Key (BC Curriculum)",
        "short_title": "Change in quantity to 20",
        "domain": "Patterning",
        "standard_code": "Grade 1: Patterning",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/1/core",
        "standard_text": "Change in quantity to 20, concretely and verbally",
        "meta_desc": "Free Grade 1 math worksheets on change in quantity to 20, following the BC curriculum: "
                     "some more come, some go away, what changed, and same or changed, with pictures and word problems. "
                     "100 questions with an answer key.",
        "key_big": "Some more come: the number goes up. Some go away: it goes down.",
        "key_sub": "8 salmon and 4 more swim in: 8 + 4 = 12. 13 kids and 5 go to the swings: 13 − 5 = 8. "
                   "Before 8, now 12? 4 came.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "picture|before and now")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
