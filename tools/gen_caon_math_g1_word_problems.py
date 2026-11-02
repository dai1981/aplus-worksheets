# -*- coding: utf-8 -*-
"""
CA Grade 1 Math: Word problems to 50 (Ontario Curriculum 2020, B2.4)
  python3 tools/gen_caon_math_g1_word_problems.py
Join (add to) stories, take-away stories, compare stories, part-part-whole stories with a bar model,
and choosing the equation for a story. Numbers add up to no more than 50. Canadian English.
Every answer and every wrong answer is computed and checked in code.
HTML attributes use single quotes (no backslashes in the JSON).
Helpers are copied from gen_us_math_g1_word_problems.py and gen_caon_math_g2_add_sub.py.
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-1")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
PINK = "#f6d5d1"
INK = "#2b2b2b"
RED = "#c0392b"
FONT = "Arial, Helvetica, sans-serif"
BOX = "☐"
MINUS = "−"
GIRLS = ["Olivia", "Emma", "Maya", "Zoe", "Amira", "Mei", "Chloe", "Priya", "Leah", "Hana", "Ava", "Sofia"]
BOYS = ["Liam", "Noah", "Aiden", "Lucas", "Owen", "Arjun", "Ethan", "Jayden", "Benjamin", "Mateo", "Nathan", "Kai"]

C = dict(red="#d9443a", blue="#3b7dd8", green="#3fa34d", yellow="#f2c230", orange="#f08a24",
         purple="#8e5bc7", gold="#e8b21c", brown="#c68a4a", black="#2b2b2b", white="#ffffff")


# ------------------------------------------------------------ helpers
def lead(c):
    m = re.match(r"(\d+)", c)
    return int(m.group(1)) if m else None


def mcq(q, correct, cands, e, rnd):
    """4 choices: correct + 3 unique distractors (whole numbers 1 to 99, all different values)."""
    correct = str(correct)
    seen = {correct}
    num = BOX not in correct
    vals = {lead(correct)} if num else set()
    pick = []
    for c in cands:
        c = str(c)
        v = lead(c)
        if c in seen or not c:
            continue
        if num and v is not None and (v < 1 or v > 99 or v in vals):
            continue
        seen.add(c)
        if num:
            vals.add(v)
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

    def next(self):
        p = self.pool[self.i % len(self.pool)]
        self.i += 1
        return p

    def one(self):
        n, he, his, him = self.next()
        return dict(N=n, he=he, He=cap(he), his=his, His=cap(his), him=him)

    def two(self):
        a = self.next()
        b = self.next()
        while b[0] == a[0]:
            b = self.next()
        return a[0], b[0]


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
    elif kind == "mitt":
        s += ("<ellipse cx='%.1f' cy='%.1f' rx='3.6' ry='5.5' fill='%s' stroke='%s' stroke-width='1.2' "
              "transform='rotate(-35 %.1f %.1f)'/>" % (cx - 6.5, cy + 0.5, C["red"], INK, cx - 6.5, cy + 0.5)
              + "<rect x='%.1f' y='%.1f' width='13' height='16' rx='6' fill='%s' stroke='%s' stroke-width='1.2'/>"
              % (cx - 5.5, cy - 10, C["red"], INK)
              + "<rect x='%.1f' y='%.1f' width='14' height='5' rx='1.5' fill='#ffffff' stroke='%s' stroke-width='1.2'/>"
              % (cx - 6, cy + 5, INK))
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
              + "<polygon points='%s' fill='%s' stroke='%s' stroke-width='1'/>" % (leaf_pts(cx, cy, 11), C["red"], INK))
    elif kind == "snowball":
        s += ("<circle cx='%.1f' cy='%.1f' r='9.5' fill='#ffffff' stroke='#5b7a99' stroke-width='1.6'/>" % (cx, cy)
              + "<path d='M%.1f %.1f q4 -4 9 -2' fill='none' stroke='#a9c1d9' stroke-width='1.4'/>" % (cx - 5, cy - 2))
    elif kind == "child":
        s += ("<path d='M%.1f %.1f q0 -8 7 -8 q7 0 7 8 z' fill='%s' stroke='%s' stroke-width='1.2'/>"
              % (cx - 7, cy + 12, C["blue"], INK)
              + "<circle cx='%.1f' cy='%.1f' r='5' fill='#f3d2b5' stroke='%s' stroke-width='1.2'/>" % (cx, cy - 5, INK))
    else:
        raise ValueError(kind)
    return s + "</g>"


NAMES = dict(apple=("apple", "apples"), star=("sticker", "stickers"), cookie=("cookie", "cookies"),
             mitt=("mitt", "mitts"), card=("card", "cards"), puck=("puck", "pucks"), leaf=("leaf", "leaves"),
             snowball=("snowball", "snowballs"), child=("child", "children"))


def plural(n, kind):
    return NAMES[kind][0 if n == 1 else 1]


def cross(cx, cy, r=10):
    return ("<g data-x='1'><line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2.6' stroke-linecap='round'/>"
            "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2.6' stroke-linecap='round'/></g>"
            % (cx - r, cy - r, cx + r, cy + r, RED, cx - r, cy + r, cx + r, cy - r, RED))


def group_body(x0, y0, n, kind, cols=5, gap5=0):
    """n objects in rows of `cols`; an extra gap after every 5 in a row (like a ten frame)."""
    s, centers = [], []
    for i in range(n):
        r, c = divmod(i, cols)
        cx = x0 + c * PITCH + PITCH / 2 + (gap5 if c >= 5 else 0)
        cy = y0 + r * PITCH + PITCH / 2
        centers.append((cx, cy))
        s.append(obj(kind, cx, cy))
    ncol = min(n, cols)
    w = ncol * PITCH + (gap5 if ncol > 5 else 0)
    h = ((n + cols - 1) // cols) * PITCH
    return "".join(s), w, h, centers


def join_svg(a, b, kind):
    """Add to: a objects, then b more inside a dashed box."""
    o, gap = 6, 22
    b1, w1, h1, _ = group_body(o, o + 4, a, kind, cols=10, gap5=8)
    b2, w2, h2, _ = group_body(o + w1 + gap + 6, o + 4, b, kind)
    box = ("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' rx='8' fill='none' stroke='%s' stroke-width='1.6' "
           "stroke-dasharray='5 3'/>" % (o + w1 + gap, o, w2 + 12, h2 + 8, GREEN))
    W, H = o + w1 + gap + w2 + 12 + o, o + max(h1, h2) + 8 + o
    svg = svg_wrap(int(W + 0.99), int(H + 0.99), b1 + box + b2, "picture: %d %s and %d more" % (a, plural(a, kind), b))
    assert svg.count("<g data-o='1'>") == a + b
    return svg


def take_svg(a, b, kind):
    """Take away: a objects in rows of 10 (or 5); the last b are crossed out."""
    o = 6
    cols = 10 if a > 10 else 5
    body, w, h, cen = group_body(o, o, a, kind, cols=cols, gap5=8)
    xs = "".join(cross(cx, cy) for cx, cy in cen[a - b:])
    svg = svg_wrap(int(w + 2 * o + 0.99), int(h + 2 * o + 0.99), body + xs,
                   "picture: %d %s, %d crossed out" % (a, plural(a, kind), b))
    assert svg.count("<g data-o='1'>") == a and svg.count("<g data-x='1'>") == b
    return svg


def rows_svg(n1, n2, name1, name2, kind, lines=False):
    """Compare: two rows lined up one under the other, names at the left."""
    fs = 16
    lw = max(tw(name1, fs), tw(name2, fs))
    x0 = 10 + lw * 1.15 + 10
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


# ------------------------------------------------------------ tens and ones blocks
CU = 12          # one cube
RG = 6           # gap between rods


def blocks_body(x0, y0, n, h=10 * CU):
    """n as tens rods and ones cubes; everything sits on the same bottom line. Returns body, w, rod and cube centres."""
    t, o = divmod(n, 10)
    s, rods, cubes = [], [], []
    x = x0
    for i in range(t):
        for k in range(10):
            s.append("<rect x='%.1f' y='%.1f' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1'/>"
                     % (x, y0 + h - (k + 1) * CU, CU, CU, FILL, GREEN))
        s.append("<rect x='%.1f' y='%.1f' width='%d' height='%d' fill='none' stroke='%s' stroke-width='1.8'/>"
                 % (x, y0 + h - 10 * CU, CU, 10 * CU, GREEN))
        rods.append((x + CU / 2.0, y0 + h - 5 * CU))
        x += CU + RG
    if t and o:
        x += 6
    for i in range(o):
        c, r = divmod(i, 5)
        cx, cy = x + c * (CU + 4), y0 + h - (r + 1) * (CU + 2) + 2
        s.append("<rect x='%.1f' y='%.1f' width='%d' height='%d' fill='#fbe3a6' stroke='#a07a12' stroke-width='1.2'/>"
                 % (cx, cy, CU, CU))
        cubes.append((cx + CU / 2.0, cy + CU / 2.0))
    w = t * (CU + RG) - (RG if t and not o else 0) + (6 if t and o else 0) + (((o + 4) // 5) * (CU + 4) - 4 if o else 0)
    return "".join(s), w, rods, cubes


def label_tens(n):
    t, o = divmod(n, 10)
    parts = []
    if t:
        parts.append("%d ten%s" % (t, "" if t == 1 else "s"))
    if o:
        parts.append("%d one%s" % (o, "" if o == 1 else "s"))
    return " and ".join(parts)


def join_blocks_svg(a, b):
    """Add to with blocks: a, then b more in a dashed box."""
    o, gap = 8, 16
    H = 10 * CU
    b1, w1, _, _ = blocks_body(o, o + 6, a)
    b2, w2, _, _ = blocks_body(o + w1 + gap + 8, o + 6, b)
    box = ("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' rx='8' fill='none' stroke='%s' stroke-width='1.6' "
           "stroke-dasharray='5 3'/>" % (o + w1 + gap, o, w2 + 16, H + 12, GREEN))
    W, HH = o + w1 + gap + w2 + 16 + o, o + H + 12 + o
    return svg_wrap(int(W + 0.99), int(HH + 0.99), b1 + box + b2,
                    "tens and ones blocks: %d (%s) and %d more (%s)" % (a, label_tens(a), b, label_tens(b)))


def take_blocks_svg(a, b):
    """Take away with blocks: a as tens and ones; b ones cubes (or b/10 rods) crossed out."""
    o = 8
    body, w, rods, cubes = blocks_body(o, o, a)
    if b % 10 == 0:
        xs = []
        for cx, cy in rods[len(rods) - b // 10:]:
            xs.append("<g data-x='1'><line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2.8' "
                      "stroke-linecap='round'/><line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2.8' "
                      "stroke-linecap='round'/></g>" % (cx - 8, cy - 56, cx + 8, cy + 56, RED, cx + 8, cy - 56, cx - 8, cy + 56, RED))
        xs = "".join(xs)
    else:
        assert b <= len(cubes)
        xs = "".join(cross(cx, cy, 8) for cx, cy in cubes[len(cubes) - b:])
    return svg_wrap(int(w + 2 * o + 0.99), 10 * CU + 2 * o, body + xs,
                    "tens and ones blocks: %d (%s), %d crossed out" % (a, label_tens(a), b))


# ------------------------------------------------------------ bar models
def bar_svg(p1, p2, unknown=None):
    """Part-part-whole bar model: whole on top, the two parts below, drawn to scale (with a minimum width)."""
    whole = p1 + p2
    m, BW, bh, gap, minw = 8, 300, 38, 10, 52
    w1 = int(round(BW * p1 / float(whole)))
    w1 = max(minw, min(BW - minw, w1))
    W, H = BW + 2 * m, 2 * m + 2 * bh + gap
    lab = {"whole": whole, "p1": p1, "p2": p2}
    if unknown:
        lab[unknown] = "?"
    y2 = m + bh + gap

    def box(x, y, w, k):
        unk = lab[k] == "?"
        return ("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='2'%s/>"
                % (x, y, w, bh, PINK if unk else (FILL if k == "whole" else "#ffffff"), RED if unk else GREEN,
                   " stroke-dasharray='5 3'" if unk else ""))
    s = [box(m, m, BW, "whole"), box(m, y2, w1, "p1"), box(m + w1, y2, BW - w1, "p2")]
    for cx, cy, k in [(m + BW / 2.0, m + 26, "whole"), (m + w1 / 2.0, y2 + 26, "p1"), (m + w1 + (BW - w1) / 2.0, y2 + 26, "p2")]:
        v = lab[k]
        s.append(text(cx, cy, str(v), 20, col=RED if v == "?" else INK))
    return svg_wrap(W, H, "".join(s), "bar model: whole %s, parts %s and %s" % (lab["whole"], lab["p1"], lab["p2"]))


def cmp_bar_svg(n1, name1, n2, name2, unknown):
    """Compare bar model: name1 has n1 (the bigger), name2 has n2. A dashed piece shows the difference.
    unknown: 'diff' (how many more), 'big' (n1 is the ?), 'small' (n2 is the ?)."""
    assert n1 > n2
    d = n1 - n2
    fs = 16
    lw = max(tw(name1, fs), tw(name2, fs))
    x0 = 10 + lw * 1.15 + 10
    BW, bh, gap, m = 300, 36, 12, 8
    u = BW / float(n1)
    w1, w2 = n1 * u, n2 * u
    lab1 = "?" if unknown == "big" else str(n1)
    lab2 = "?" if unknown == "small" else str(n2)
    labd = "?" if unknown == "diff" else str(d)
    assert w2 >= tw(lab2, 20) + 8 and (w1 - w2) >= tw(labd, 20) + 8, (n1, n2)
    y1, y2 = m, m + bh + gap
    s = [text(x0 - 10, y1 + bh / 2 + 6, name1, fs, anchor="end"), text(x0 - 10, y2 + bh / 2 + 6, name2, fs, anchor="end")]

    def rect(x, y, w, unk, fill):
        return ("<rect x='%.1f' y='%d' width='%.1f' height='%d' fill='%s' stroke='%s' stroke-width='2'%s/>"
                % (x, y, w, bh, PINK if unk else fill, RED if unk else GREEN, " stroke-dasharray='5 3'" if unk else ""))
    s.append(rect(x0, y1, w1, lab1 == "?", FILL))
    s.append(rect(x0, y2, w2, lab2 == "?", "#ffffff"))
    s.append("<rect x='%.1f' y='%d' width='%.1f' height='%d' fill='%s' stroke='%s' stroke-width='2' stroke-dasharray='5 3'/>"
             % (x0 + w2, y2, w1 - w2, bh, PINK if labd == "?" else "#ffffff", RED))
    s.append(text(x0 + w1 / 2, y1 + 25, lab1, 20, col=RED if lab1 == "?" else INK))
    s.append(text(x0 + w2 / 2, y2 + 25, lab2, 20, col=RED if lab2 == "?" else INK))
    s.append(text(x0 + w2 + (w1 - w2) / 2, y2 + 25, labd, 20, col=RED))
    W, H = x0 + BW + m, y2 + bh + m
    return svg_wrap(int(W + 0.99), H, "".join(s),
                    "compare bar model: %s %s, %s %s, difference %s" % (name1, lab1, name2, lab2, labd))


# ------------------------------------------------------------ contexts: add to / take away
# s start, ad add, ads add some, tk take, tks take some, now, qn now?, qa added?, qt taken?
# k = picture kind (None: no object picture), top = biggest realistic number
JOIN = [
    dict(s="The lost and found box had {a} mitts.", ad="Students found {b} more mitts.", ads="Students found some more mitts.",
         tk="Children took {b} mitts home.", tks="Children took some mitts home.",
         now="Now there are {c} mitts in the box.", qn="How many mitts are in the box now?",
         qa="How many mitts did students find?", qt="How many mitts did children take home?",
         u=("mitt", "mitts"), k="mitt", top=50),
    dict(s="{N} picked {a} apples at the orchard.", ad="Then {he} picked {b} more.", ads="Then {he} picked some more.",
         tk="{He} gave {b} apples to {his} class.", tks="{He} gave some apples to {his} class.",
         now="Now {he} has {c} apples.", qn="How many apples does {N} have now?",
         qa="How many more apples did {N} pick?", qt="How many apples did {N} give away?",
         u=("apple", "apples"), k="apple", top=50),
    dict(s="{N} had {a} hockey cards.", ad="{He} got {b} more cards.", ads="{He} got some more cards.",
         tk="{He} gave {b} cards to {his} friend.", tks="{He} gave some cards to {his} friend.",
         now="Now {he} has {c} hockey cards.", qn="How many hockey cards does {N} have now?",
         qa="How many cards did {N} get?", qt="How many cards did {N} give away?",
         u=("hockey card", "hockey cards"), k="card", top=50),
    dict(s="There were {a} children on the school bus.", ad="At the next stop, {b} more got on.",
         ads="At the next stop, some more got on.",
         tk="At the next stop, {b} children got off.", tks="At the next stop, some children got off.",
         now="Now there are {c} children on the bus.", qn="How many children are on the bus now?",
         qa="How many children got on?", qt="How many children got off?",
         u=("child", "children"), k="child", top=48),
    dict(s="At recess, {a} children were on the playground.", ad="Then {b} more children came out.",
         ads="Then some more children came out.",
         tk="Then {b} children went inside.", tks="Then some children went inside.",
         now="Now there are {c} children on the playground.", qn="How many children are on the playground now?",
         qa="How many children came out?", qt="How many children went inside?",
         u=("child", "children"), k="child", top=50),
    dict(s="There were {a} pucks in the bucket.", ad="The coach put in {b} more.", ads="The coach put in some more.",
         tk="The coach took out {b} pucks.", tks="The coach took out some pucks.",
         now="Now there are {c} pucks in the bucket.", qn="How many pucks are in the bucket now?",
         qa="How many pucks did the coach put in?", qt="How many pucks did the coach take out?",
         u=("puck", "pucks"), k="puck", top=50),
    dict(s="{N} collected {a} maple leaves.", ad="{He} found {b} more.", ads="{He} found some more.",
         tk="The wind blew {b} leaves away.", tks="The wind blew some leaves away.",
         now="Now {he} has {c} maple leaves.", qn="How many maple leaves does {N} have now?",
         qa="How many more leaves did {N} find?", qt="How many leaves blew away?",
         u=("maple leaf", "maple leaves"), k="leaf", top=50),
    dict(s="{N} made {a} snowballs.", ad="Then {he} made {b} more.", ads="Then {he} made some more.",
         tk="{He} threw {b} snowballs at a tree.", tks="{He} threw some snowballs at a tree.",
         now="Now {he} has {c} snowballs.", qn="How many snowballs does {N} have now?",
         qa="How many more snowballs did {N} make?", qt="How many snowballs did {N} throw?",
         u=("snowball", "snowballs"), k="snowball", top=30),
    dict(s="{N} had {a} stickers.", ad="{His} teacher gave {him} {b} more.", ads="{His} teacher gave {him} some more.",
         tk="{He} used {b} stickers on a card.", tks="{He} used some stickers on a card.",
         now="Now {he} has {c} stickers.", qn="How many stickers does {N} have now?",
         qa="How many stickers did the teacher give {N}?", qt="How many stickers did {N} use?",
         u=("sticker", "stickers"), k="star", top=50),
    dict(s="There were {a} cookies on a tray.", ad="Grandma baked {b} more.", ads="Grandma baked some more.",
         tk="The children ate {b} cookies.", tks="The children ate some cookies.",
         now="Now there are {c} cookies on the tray.", qn="How many cookies are on the tray now?",
         qa="How many cookies did Grandma bake?", qt="How many cookies did the children eat?",
         u=("cookie", "cookies"), k="cookie", top=36),
    dict(s="There were {a} Canada geese on the pond.", ad="Then {b} more geese landed.", ads="Then some more geese landed.",
         tk="Then {b} geese flew away.", tks="Then some geese flew away.",
         now="Now there are {c} geese on the pond.", qn="How many geese are on the pond now?",
         qa="How many geese landed?", qt="How many geese flew away?",
         u=("goose", "geese"), k=None, top=50),
    dict(s="The class library had {a} books.", ad="The teacher added {b} more.", ads="The teacher added some more.",
         tk="Students took {b} books home.", tks="Students took some books home.",
         now="Now there are {c} books in the class library.", qn="How many books are in the class library now?",
         qa="How many books did the teacher add?", qt="How many books did students take home?",
         u=("book", "books"), k=None, top=50),
]

# ------------------------------------------------------------ contexts: put together / take apart
PARTS = [
    dict(tot="At recess, {a} children play tag and {b} play soccer. How many children play?",
         part="At recess, {c} children play outside. {a} play tag. The rest play soccer. How many play soccer?",
         u=("child", "children")),
    dict(tot="{N} has {a} red apples and {b} green apples. How many apples does {he} have?",
         part="{N} has {c} apples. {a} are red. The rest are green. How many are green?",
         u=("apple", "apples")),
    dict(tot="The lost and found has {a} red mitts and {b} blue mitts. How many mitts are there?",
         part="The lost and found has {c} mitts. {a} are red. The rest are blue. How many are blue?",
         u=("mitt", "mitts")),
    dict(tot="The school bus has {a} girls and {b} boys. How many children are on the bus?",
         part="The school bus has {c} children. {a} are girls. How many are boys?",
         u=("child", "children"), pu=("boy", "boys")),
    dict(tot="{N} has {a} red leaves and {b} yellow leaves. How many leaves does {he} have?",
         part="{N} has {c} leaves. {a} are red. The rest are yellow. How many are yellow?",
         u=("leaf", "leaves")),
    dict(tot="There are {a} geese on the grass and {b} geese in the water. How many geese are there?",
         part="There are {c} geese at the pond. {a} are on the grass. The rest are in the water. How many are in the water?",
         u=("goose", "geese")),
    dict(tot="{N} has {a} hockey cards and {b} baseball cards. How many cards does {he} have?",
         part="{N} has {c} cards. {a} are hockey cards. The rest are baseball cards. How many baseball cards does {he} have?",
         u=("card", "cards"), pu=("baseball card", "baseball cards")),
    dict(tot="Dad baked {a} chocolate cookies and {b} oatmeal cookies. How many cookies did he bake?",
         part="Dad baked {c} cookies. {a} are chocolate. The rest are oatmeal. How many are oatmeal?",
         u=("cookie", "cookies")),
    dict(tot="{N} read {a} books in October and {b} books in November. How many books did {he} read?",
         part="{N} read {c} books in October and November. {He} read {a} in October. How many did {he} read in November?",
         u=("book", "books")),
]


# ------------------------------------------------------------ contexts: compare
def cmp_ctx(verb_has, verb_did, T, k, one, top=50):
    """verb_has: 'has'; verb_did: question form, e.g. 'does {X} have'."""
    return dict(has="{X} %s {n} %s." % (verb_has, T), more="{X} %s {d} more %s than {Y}." % (verb_has, T),
                fewer="{X} %s {d} fewer %s than {Y}." % (verb_has, T),
                qm="How many more %s %s than {Y}?" % (T, verb_did), qf="How many fewer %s %s than {Y}?" % (T, verb_did),
                qh="How many %s %s?" % (T, verb_did), u=(one, T), k=k, top=top)


CMP = [cmp_ctx("picked", "did {X} pick", "apples", "apple", "apple"),
       cmp_ctx("has", "does {X} have", "hockey cards", "card", "hockey card"),
       cmp_ctx("has", "does {X} have", "stickers", "star", "sticker"),
       cmp_ctx("made", "did {X} make", "snowballs", "snowball", "snowball", top=30),
       cmp_ctx("collected", "did {X} collect", "maple leaves", "leaf", "maple leaf"),
       cmp_ctx("shot", "did {X} shoot", "pucks", "puck", "puck"),
       dict(has="{X} jumped rope {n} times.", more="{X} jumped rope {d} more times than {Y}.",
            fewer="{X} jumped rope {d} fewer times than {Y}.",
            qm="How many more times did {X} jump than {Y}?", qf="How many fewer times did {X} jump than {Y}?",
            qh="How many times did {X} jump rope?", u=("time", "times"), k=None, top=50),
       dict(has="{X} read {n} pages.", more="{X} read {d} more pages than {Y}.", fewer="{X} read {d} fewer pages than {Y}.",
            qm="How many more pages did {X} read than {Y}?", qf="How many fewer pages did {X} read than {Y}?",
            qh="How many pages did {X} read?", u=("page", "pages"), k=None, top=50)]


# ------------------------------------------------------------ stories (one builder for every kind)
# AR add to, result unknown     TR take away, result unknown
# CA add to, change unknown     CT take away, change unknown
# PT put together (whole)       PA take apart (one part unknown)
# CD compare: how many more     CF compare: how many fewer
# CB compare: bigger unknown    CS compare: smaller unknown
def count_on(a, t):
    return ", ".join(str(x) for x in range(a + 1, t + 1))


def tens_slip_add(a, b):
    """Typical place-value slip when one number has tens: 23 + 20 = 25, 23 + 4 = 63."""
    if a >= 10 and b % 10 == 0:
        return a + b // 10
    if a >= 20 and b < 10:
        return a + 10 * b
    return None


def tens_slip_sub(a, b):
    """34 − 10 = 33 (took the ten away as a one), 36 − 4 = −… skip."""
    if a >= 20 and b % 10 == 0:
        return a - b // 10
    return None


def e_add(a, b):
    s = a + b
    if a >= 20 and b % 10 == 0:
        return "Add the tens: %d + %d = %d." % (a, b, s)
    if a >= 20 and b < 10:
        return "Add the ones: %d + %d = %d. The tens stay the same: %d + %d = %d." % (a % 10, b, a % 10 + b, a, b, s)
    if b <= 4 and a > b:
        return "Count on from %d: %s. So %d + %d = %d." % (a, count_on(a, s), a, b, s)
    return "Put them together: %d + %d = %d." % (a, b, s)


def e_sub(a, b):
    r = a - b
    if a >= 20 and b % 10 == 0:
        return "Take away the tens: %d − %d = %d." % (a, b, r)
    if a >= 20 and b < 10 and b <= a % 10:
        return "Take away the ones: %d − %d = %d. The tens stay the same: %d − %d = %d." % (a % 10, b, a % 10 - b, a, b, r)
    if r <= 4:
        return "Count up from %d to %d: %s. That is %d. So %d − %d = %d." % (b, a, count_on(b, a), r, a, b, r)
    return "Take away: %d − %d = %d." % (a, b, r)


def build(kind, c, p, x, y):
    """x, y: the two story numbers in story order. Returns q, ans, wrong list, e, eq, U, nums."""
    U = lambda v: fmt(v, c["u"])
    pp = p if isinstance(p, dict) else {}
    if kind == "AR":
        a, b = x, y
        ans = a + b
        q = say(c["s"] + " " + c["ad"] + " " + c["qn"], pp, a=a, b=b)
        e = "Some are added, so add. " + e_add(a, b)
        wrong = [abs(a - b), tens_slip_add(a, b), max(a, b), ans + 1, ans - 1, ans + 2, ans + 10]
        eq = "%d + %d = %s" % (a, b, BOX)
    elif kind == "TR":
        a, b = x, y
        ans = a - b
        q = say(c["s"] + " " + c["tk"] + " " + c["qn"], pp, a=a, b=b)
        e = "Some are taken away, so subtract. Do not add. " + e_sub(a, b)
        wrong = [a + b, tens_slip_sub(a, b), b, ans + 1, ans - 1, a, ans + 2]
        eq = "%d − %d = %s" % (a, b, BOX)
    elif kind == "CA":
        a, t = x, y
        ans = t - a
        q = say(c["s"] + " " + c["ads"] + " " + c["now"] + " " + c["qa"], pp, a=a, c=t)
        e = "The number added is missing: %d + %s = %d. " % (a, BOX, t)
        e += ("Count on from %d to %d: %s. That is %d." % (a, t, count_on(a, t), ans) if ans <= 5
              else "Subtract: %d − %d = %d. Check: %d + %d = %d." % (t, a, ans, a, ans, t))
        wrong = [a + t, t, a, ans + 1, ans - 1, ans + 2]
        eq = "%d + %s = %d" % (a, BOX, t)
    elif kind == "CT":
        a, t = x, y
        ans = a - t
        q = say(c["s"] + " " + c["tks"] + " " + c["now"] + " " + c["qt"], pp, a=a, c=t)
        e = ("The number taken away is missing: %d − %s = %d. Subtract: %d − %d = %d. Check: %d − %d = %d."
             % (a, BOX, t, a, t, ans, a, ans, t))
        wrong = [a + t, a, t, ans + 1, ans - 1, ans + 2]
        eq = "%d − %s = %d" % (a, BOX, t)
    elif kind == "PT":
        a, b = x, y
        ans = a + b
        q = say(c["tot"], pp, a=a, b=b)
        e = "You know both parts. Find the whole, so add. " + e_add(a, b)
        wrong = [abs(a - b), tens_slip_add(a, b), max(a, b), ans + 1, ans - 1, ans + 2, ans + 10]
        eq = "%d + %d = %s" % (a, b, BOX)
    elif kind == "PA":
        t, a = x, y
        ans = t - a
        q = say(c["part"], pp, c=t, a=a)
        U = lambda v: fmt(v, c.get("pu", c["u"]))
        e = ("You know the whole (%d) and one part (%d). Subtract: %d − %d = %d. Check: %d + %d = %d."
             % (t, a, t, a, ans, a, ans, t))
        wrong = [t + a, t, a, ans + 1, ans - 1, ans + 2]
        eq = "%d − %d = %s" % (t, a, BOX)
    elif kind in ("CD", "CF"):
        X, Y, big, small = p                              # X has big, Y has small
        ans = big - small
        q = say(c["has"], {}, X=X, n=big) + " " + say(c["has"], {}, X=Y, n=small) + " "
        if kind == "CD":
            q += say(c["qm"], {}, X=X, Y=Y)
            e = "Match them up. %s has %d extra. Find the difference: %d − %d = %d. Do not add." % (X, ans, big, small, ans)
        else:
            q += say(c["qf"], {}, X=Y, Y=X)
            e = "Match them up. %s has %d fewer. Find the difference: %d − %d = %d. Do not add." % (Y, ans, big, small, ans)
        e += " Check: %d + %d = %d." % (small, ans, big)
        wrong = [big + small, big, small, ans + 1, ans - 1, ans + 2]
        eq = "%d − %d = %s" % (big, small, BOX)
        x, y = big, small
    elif kind == "CB":
        X, Y, n, d = p                                    # Y has n, X has d more than Y
        ans = n + d
        q = (say(c["has"], {}, X=Y, n=n) + " " + say(c["more"], {}, X=X, d=d, Y=Y) + " " + say(c["qh"], {}, X=X))
        e = "%s has more than %s, so add. %d + %d = %d." % (X, Y, n, d, ans)
        wrong = [abs(n - d), n, d, ans + 1, ans - 1, tens_slip_add(n, d)]
        eq = "%d + %d = %s" % (n, d, BOX)
        x, y = n, d
    elif kind == "CS":
        X, Y, n, d = p                                    # X has n, Y has d fewer than X
        ans = n - d
        q = (say(c["has"], {}, X=X, n=n) + " " + say(c["fewer"], {}, X=Y, d=d, Y=X) + " " + say(c["qh"], {}, X=Y))
        e = "%s has fewer than %s, so subtract. %d − %d = %d. Do not add." % (Y, X, n, d, ans)
        wrong = [n + d, n, d, ans + 1, ans - 1, ans + 2]
        eq = "%d − %d = %s" % (n, d, BOX)
        x, y = n, d
    else:
        raise ValueError(kind)
    wrong = [w for w in wrong if w is not None]
    assert 2 <= ans <= 50 and solve_box(eq) == ans, (kind, eq, ans)
    assert max(x, y, ans) <= 50 and ans not in (x, y), (kind, x, y, ans)
    return dict(q=q, ans=ans, wrong=wrong, e=e + " Answer: %s." % U(ans), eq=eq, U=U, nums=(x, y), kind=kind)


def solve_box(eq):
    """Whole-number value of ☐ that makes the equation true (None if there is none)."""
    for v in range(0, 101):
        l, r = eq.replace(MINUS, "-").replace(BOX, str(v)).split(" = ")
        if eval(l) == eval(r):
            return v
    return None


# ------------------------------------------------------------ pickers
def pick(rnd, used, gen, ok):
    for _ in range(20000):
        v = gen()
        if ok(*v) and v not in used:
            used.add(v)
            return v
    raise RuntimeError("no numbers")


class Ctx:
    """Cycles through a context list in a shuffled order; can ask for one with a picture or a big enough top."""
    def __init__(self, rnd, lst):
        self.rnd, self.lst = rnd, lst
        self.order = []

    def get(self, pic=False, need=0):
        last = getattr(self, "last", None)
        for _ in range(3):
            if not self.order:
                self.order = list(self.lst)
                self.rnd.shuffle(self.order)
            for strict in (True, False):
                for i, c in enumerate(self.order):
                    if (not pic or c.get("k")) and c.get("top", 50) >= need and (not strict or c is not last):
                        self.last = self.order.pop(i)
                        return self.last
            self.order = []
        raise RuntimeError("no context")


def item(b, rnd, pic=""):
    return mcq((fig(pic) if pic else "") + b["q"], b["U"](b["ans"]), [b["U"](v) for v in b["wrong"]], b["e"], rnd)


def add_ok_big(a, b):
    """Sums 21 to 50 a Grade 1 student can model: add ones without a new ten, or add tens."""
    s = a + b
    if not (21 <= s <= 50 and a >= 11):
        return False
    return (b < 10 and a % 10 + b <= 9) or (b % 10 == 0 and b <= 30)


def sub_ok_big(a, b):
    r = a - b
    if not (21 <= a <= 50 and r >= 2):
        return False
    return (2 <= b < 10 and b <= a % 10 and r != b) or (b % 10 == 0 and r != b)


def pic_for(b, c, X=None, Y=None):
    """The picture that fits a story."""
    k, (x, y), ans = b["kind"], b["nums"], b["ans"]
    if k == "AR":
        return join_svg(x, y, c["k"]) if x + y <= 20 and c.get("k") else join_blocks_svg(x, y)
    if k == "TR":
        return take_svg(x, y, c["k"]) if x <= 20 and c.get("k") else take_blocks_svg(x, y)
    if k == "CA":
        return bar_svg(x, ans, "p2")
    if k == "CT":
        return bar_svg(y, ans, "p2")
    if k == "PT":
        return bar_svg(x, y, "whole")
    if k == "PA":
        return bar_svg(y, ans, "p2")
    if k in ("CD", "CF"):
        return rows_svg(x, y, X, Y, c["k"]) if x <= 20 and c.get("k") else cmp_bar_svg(x, X, y, Y, "diff")
    if k == "CB":
        return cmp_bar_svg(x + y, X, x, Y, "big")
    if k == "CS":
        return cmp_bar_svg(x, X, x - y, Y, "small")
    raise ValueError(k)


# ------------------------------------------------------------ set 1: join (add to)
def set_join(rnd, P, J, used):
    its = []
    R = rnd.randint
    for i in range(20):
        if i < 16:
            if i < 6:
                a, b = pick(rnd, used, lambda: (R(2, 8), R(2, 5)), lambda a, b: 5 <= a + b <= 10 and a != b)
            elif i < 12:
                a, b = pick(rnd, used, lambda: (R(5, 14), R(2, 9)), lambda a, b: 11 <= a + b <= 20 and a != b and b <= 6)
            else:
                a, b = pick(rnd, used, lambda: (R(11, 45), rnd.choice([2, 3, 4, 5, 6, 10, 20])), add_ok_big)
            c = J.get(pic=i < 12, need=a + b)
            bb = build("AR", c, P.one(), a, b)
        else:
            if i < 18:
                a, t = pick(rnd, used, lambda: (R(5, 15), R(11, 20)), lambda a, t: 2 <= t - a <= 8 and t - a != a)
            else:
                a, t = pick(rnd, used, lambda: (R(15, 40), R(25, 50)),
                            lambda a, t: (t - a in (10, 20) or (2 <= t - a <= 6 and a % 10 + t - a <= 9)) and t - a != a)
            c = J.get(need=t)
            bb = build("CA", c, P.one(), a, t)
        its.append(item(bb, rnd, pic_for(bb, c)))
    return {"title": "Join stories: some more come", "items": its}


# ------------------------------------------------------------ set 2: take away
def set_take(rnd, P, J, used):
    its = []
    R = rnd.randint
    for i in range(20):
        if i < 16:
            if i < 6:
                a, b = pick(rnd, used, lambda: (R(5, 10), R(2, 5)), lambda a, b: a - b >= 2 and a - b != b)
            elif i < 12:
                a, b = pick(rnd, used, lambda: (R(11, 20), R(2, 9)), lambda a, b: a - b >= 3 and a - b != b)
            else:
                a, b = pick(rnd, used, lambda: (R(21, 50), rnd.choice([2, 3, 4, 5, 6, 10, 20])), sub_ok_big)
            c = J.get(pic=i < 12, need=a)
            bb = build("TR", c, P.one(), a, b)
        else:
            if i < 18:
                a, t = pick(rnd, used, lambda: (R(11, 20), R(4, 15)), lambda a, t: 2 <= a - t <= 9 and a - t != t)
            else:
                a, t = pick(rnd, used, lambda: (R(25, 50), R(10, 45)),
                            lambda a, t: (a - t in (10, 20) or (2 <= a - t <= 6 and a - t <= a % 10)) and a - t != t)
            c = J.get(need=a)
            bb = build("CT", c, P.one(), a, t)
        its.append(item(bb, rnd, pic_for(bb, c)))
    return {"title": "Take-away stories: some go away", "items": its}


# ------------------------------------------------------------ set 3: compare
def set_compare(rnd, P, Cc, used):
    a1 = ["CD", "CF"] * 3
    a2 = ["CD", "CF"] * 3
    a3 = ["CD", "CF"] * 3
    for h in (a1, a2, a3):
        rnd.shuffle(h)
    kinds = a1 + a2 + a3 + ["CB", "CS"]
    its = []
    R = rnd.randint
    for i, k in enumerate(kinds):
        X, Y = P.two()
        if k in ("CD", "CF"):
            if i < 6:
                big, small = pick(rnd, used, lambda: (R(5, 10), R(2, 8)), lambda b, s: 2 <= b - s <= 5 and b - s != s)
            elif i < 12:
                big, small = pick(rnd, used, lambda: (R(11, 18), R(5, 14)), lambda b, s: 3 <= b - s <= 8 and b - s != s)
            else:
                big, small = pick(rnd, used, lambda: (R(25, 50), R(10, 40)),
                                  lambda b, s: (b - s in (10, 20) or (4 <= b - s <= 7 and b - s <= b % 10 and b > 30))
                                  and b - s != s and s >= 10)
            c = Cc.get(pic=i < 12, need=big)
            bb = build(k, c, (X, Y, big, small), 0, 0)
        elif k == "CB":
            n, d = pick(rnd, used, lambda: (R(12, 30), rnd.choice([5, 6, 10])),
                        lambda n, d: n + d <= 40 and (d == 10 or n % 10 + d <= 9))
            c = Cc.get(need=n + d)
            bb = build(k, c, (X, Y, n, d), 0, 0)
        else:
            n, d = pick(rnd, used, lambda: (R(25, 45), rnd.choice([5, 6, 10])),
                        lambda n, d: (d == 10 or d <= n % 10) and n - d != d)
            c = Cc.get(need=n)
            bb = build(k, c, (X, Y, n, d), 0, 0)
        its.append(item(bb, rnd, pic_for(bb, c, X, Y)))
        if i < 3:
            its[-1]["q"] = its[-1]["q"].replace(pic_for(bb, c, X, Y), rows_svg(bb["nums"][0], bb["nums"][1], X, Y, c["k"], lines=True))
    return {"title": "Compare stories: how many more?", "items": its}


# ------------------------------------------------------------ set 4: part-part-whole with a bar model
def set_parts(rnd, P, Pc, used):
    kinds = []
    for _ in range(2):
        h = ["PT"] * 5 + ["PA"] * 5
        rnd.shuffle(h)
        kinds += h
    its = []
    R = rnd.randint
    for i, k in enumerate(kinds):
        small = i < 10
        if k == "PT":
            if small:
                a, b = pick(rnd, used, lambda: (R(3, 12), R(3, 9)), lambda a, b: 8 <= a + b <= 20 and a != b)
            else:
                a, b = pick(rnd, used, lambda: (R(11, 40), rnd.choice([3, 4, 5, 6, 7, 10, 20])), add_ok_big)
            bb = build("PT", Pc.get(), P.one(), a, b)
        else:
            if small:
                t, a = pick(rnd, used, lambda: (R(8, 20), R(3, 12)), lambda t, a: t - a >= 3 and t - a != a)
            else:
                t, a = pick(rnd, used, lambda: (R(21, 50), R(10, 40)),
                            lambda t, a: (t - a in (10, 20) or (2 <= t - a <= 7 and t - a <= t % 10)) and t - a != a)
            bb = build("PA", Pc.get(), P.one(), t, a)
        its.append(item(bb, rnd, pic_for(bb, None)))
    return {"title": "Part-part-whole stories with a bar model", "items": its}


# ------------------------------------------------------------ set 5: choose the equation
FORMS = ["{p} + {q} = ☐", "{p} − {q} = ☐", "{q} + ☐ = {p}", "{p} + ☐ = {q}",
         "☐ − {p} = {q}", "☐ − {q} = {p}", "{p} − ☐ = {q}", "☐ + {q} = {p}"]
WHY = dict(AR="Some are added and the end is missing, so add",
           TR="Some are taken away and the end is missing, so subtract",
           CA="The number added is missing, so the ☐ goes in the middle",
           CT="The number taken away is missing, so the ☐ goes in the middle",
           PT="Both parts are known and the whole is missing, so add",
           PA="The whole and one part are known, so take the part away from the whole",
           CD="How many more means find the difference, so subtract",
           CF="How many fewer means find the difference, so subtract")
TRAP = dict(AR="{p} − {q} = ☐", TR="{p} + {q} = ☐", CA="{p} + {q} = ☐", CT="{p} + {q} = ☐",
            PT="{p} − {q} = ☐", PA="{p} + {q} = ☐", CD="{p} + {q} = ☐", CF="{p} + {q} = ☐")


def canon(x):
    """12 + 8 = ☐ and 8 + 12 = ☐ count as the same choice."""
    m = re.match(r"^(\d+) \+ (\d+) = ☐$", x)
    return ("+",) + tuple(sorted(int(v) for v in m.groups())) if m else x


def eq_item(b, rnd, pic):
    kind = b["kind"]
    p, q = b["nums"]
    ans = b["ans"]
    trap = TRAP[kind].format(p=max(p, q), q=min(p, q)) if "−" in TRAP[kind] else TRAP[kind].format(p=p, q=q)
    assert solve_box(trap) not in (None, ans)
    bad = []
    pool = [f.format(p=p, q=q) for f in FORMS] + [f.format(p=q, q=p) for f in FORMS]
    for x in [trap] + rnd.sample(pool, len(pool)):
        v = solve_box(x)
        if x == b["eq"] or x in bad or v is None or v == ans or v < 1 or canon(x) in {canon(y) for y in bad + [b["eq"]]}:
            continue
        bad.append(x)
    assert bad[0] == trap and len(bad) >= 3, (kind, trap, bad)
    qq = (fig(pic) if pic else "") + b["q"] + " Which equation matches the story?"
    e = "%s: <b>%s</b>. The ☐ is %d. (%s does not match the story.)" % (WHY[kind], b["eq"], ans, trap)
    return mcq(qq, b["eq"], bad[:3], e, rnd)


def set_equation(rnd, P, J, Pc, Cc, used):
    its = []
    R = rnd.randint
    half1 = ["AR", "TR", "CA", "CT", "PT", "PA", "CD", "CF", "AR", "TR"]
    half2 = ["AR", "TR", "CA", "CT", "PT", "PA", "CD", "CF", "PA", "CD"]
    rnd.shuffle(half1)
    rnd.shuffle(half2)
    for n, k in enumerate(half1 + half2):
        big = n >= 10
        c, X, Y = None, None, None
        if k == "AR":
            if big:
                x, y = pick(rnd, used, lambda: (R(11, 45), rnd.choice([3, 4, 5, 6, 10, 20])), add_ok_big)
            else:
                x, y = pick(rnd, used, lambda: (R(4, 12), R(2, 8)), lambda a, b: 9 <= a + b <= 20 and a != b)
            c = J.get(pic=not big, need=x + y)
            bb = build(k, c, P.one(), x, y)
        elif k == "TR":
            if big:
                x, y = pick(rnd, used, lambda: (R(21, 50), rnd.choice([3, 4, 5, 6, 10, 20])), sub_ok_big)
            else:
                x, y = pick(rnd, used, lambda: (R(9, 20), R(2, 8)), lambda a, b: a - b >= 3 and a - b != b)
            c = J.get(pic=not big, need=x)
            bb = build(k, c, P.one(), x, y)
        elif k == "CA":
            if big:
                x, y = pick(rnd, used, lambda: (R(15, 40), R(25, 50)),
                            lambda a, t: (t - a in (10, 20) or (3 <= t - a <= 6 and a % 10 + t - a <= 9)) and t - a != a)
            else:
                x, y = pick(rnd, used, lambda: (R(4, 14), R(9, 20)), lambda a, t: 3 <= t - a <= 8 and t - a != a)
            c = J.get(need=y)
            bb = build(k, c, P.one(), x, y)
        elif k == "CT":
            if big:
                x, y = pick(rnd, used, lambda: (R(25, 50), R(10, 45)),
                            lambda a, t: (a - t in (10, 20) or (3 <= a - t <= 6 and a - t <= a % 10)) and a - t != t)
            else:
                x, y = pick(rnd, used, lambda: (R(9, 20), R(3, 14)), lambda a, t: 3 <= a - t <= 8 and a - t != t)
            c = J.get(need=x)
            bb = build(k, c, P.one(), x, y)
        elif k == "PT":
            if big:
                x, y = pick(rnd, used, lambda: (R(11, 40), rnd.choice([4, 5, 6, 7, 10, 20])), add_ok_big)
            else:
                x, y = pick(rnd, used, lambda: (R(4, 12), R(4, 9)), lambda a, b: 10 <= a + b <= 20 and a != b)
            c = Pc.get()
            bb = build(k, c, P.one(), x, y)
        elif k == "PA":
            if big:
                x, y = pick(rnd, used, lambda: (R(21, 50), R(10, 40)),
                            lambda t, a: (t - a in (10, 20) or (3 <= t - a <= 7 and t - a <= t % 10)) and t - a != a)
            else:
                x, y = pick(rnd, used, lambda: (R(9, 20), R(3, 12)), lambda t, a: t - a >= 3 and t - a != a)
            c = Pc.get()
            bb = build(k, c, P.one(), x, y)
        else:
            X, Y = P.two()
            if big:
                bg, sm = pick(rnd, used, lambda: (R(25, 50), R(10, 40)),
                              lambda b, s: (b - s in (10, 20) or (4 <= b - s <= 7 and b - s <= b % 10 and b > 30))
                              and b - s != s and s >= 10)
            else:
                bg, sm = pick(rnd, used, lambda: (R(7, 16), R(3, 12)), lambda b, s: 3 <= b - s <= 7 and b - s != s)
            c = Cc.get(pic=not big, need=bg)
            bb = build(k, c, (X, Y, bg, sm), 0, 0)
        pic = pic_for(bb, c, X, Y) if n < 17 else ""
        its.append(eq_item(bb, rnd, pic))
    return {"title": "Choose the equation for the story", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def body_html():
    assert 5 + 3 == 8 and 9 - 4 == 5 and 8 - 5 == 3 and 24 + 5 == 29 and 34 - 20 == 14 and 15 + 20 == 35
    return (
        "<h2>The idea: picture the story</h2>"
        "<p>Read the story. Ask: <b>what happens?</b> Do some come? Do some go away? "
        "Are two groups compared? Then find the number you do not know.</p>"
        + table(["Story", "What happens", "Equation"], [
            ["Join", "Some more come.", "5 + 3 = ☐"],
            ["Take away", "Some go away.", "9 − 4 = ☐"],
            ["Compare", "Which has more? How many more?", "8 − 5 = ☐"],
            ["Part-part-whole", "Two parts make the whole.", "24 + 5 = ☐"],
        ]) +
        "<h2>Join: some more come</h2>"
        "<p>Draw the first group. Draw the ones that come. Count them all.</p>"
        "<figure class='sn-fig'>" + join_svg(5, 3, "card") +
        "<figcaption>Liam had 5 hockey cards. He got 3 more. Count on from 5: 6, 7, 8. 5 + 3 = 8 hockey cards.</figcaption></figure>"
        "<h2>Take away: some go away</h2>"
        "<p>Draw them all. Cross out the ones that go away. Count the ones that are left.</p>"
        "<figure class='sn-fig'>" + take_svg(9, 4, "mitt") +
        "<figcaption>The lost and found box had 9 mitts. Children took 4 home. 5 are left. 9 − 4 = 5 mitts.</figcaption></figure>"
        "<p>With bigger numbers, use tens and ones. Take away tens from the tens.</p>"
        "<figure class='sn-fig'>" + take_blocks_svg(34, 20) +
        "<figcaption>There were 34 children on the school bus. 20 got off. 3 tens − 2 tens = 1 ten. 34 − 20 = 14 children.</figcaption></figure>"
        "<h2>Compare: how many more?</h2>"
        "<p>Line up the two rows. Match them one to one. The extra ones are the answer.</p>"
        "<figure class='sn-fig'>" + rows_svg(8, 5, "Maya", "Owen", "apple", lines=True) +
        "<figcaption>Maya picked 8 apples. Owen picked 5. Maya has 3 with no match. 8 − 5 = 3. Maya picked 3 more. Do not add.</figcaption></figure>"
        "<h2>Part-part-whole: use a bar model</h2>"
        "<p>The long bar is the whole. The two short bars are the parts. "
        "Know both parts? Add. Know the whole and one part? Subtract.</p>"
        "<figure class='sn-fig'>" + bar_svg(24, 5, "whole") +
        "<figcaption>At recess, 24 children play tag and 5 play soccer. 24 + 5 = 29 children.</figcaption></figure>"
        + ex("Choose the equation", "Ava had 15 stickers. Her teacher gave her some more. Now she has 35. How many did she get?",
             "The number added is missing. Put the ☐ there: 15 + ☐ = 35. 15 + 20 = 35, so the ☐ is 20.",
             "15 + ☐ = 35, 20 stickers") +
        "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Adding in a take-away story: 9 − 4 is not 13", "Some go away, so there are fewer. Subtract: 9 − 4 = 5."],
            ["Adding in a “how many more” story", "Line up the rows. Count the extra ones: 8 − 5 = 3."],
            ["Using the wrong numbers: giving 9 or 4 as the answer", "Find the number you do not know. Check it in the story."],
            ["Adding tens as ones: 23 + 20 = 25", "20 is 2 tens. 2 tens + 2 tens = 4 tens. 23 + 20 = 43."],
        ])
    )


FAQ = [
    {"q": "What word problems do Grade 1 students solve in the Ontario math curriculum?",
     "a": "Grade 1 students solve join, take-away, compare and part-part-whole stories with whole numbers that add up to no more than 50. They use objects, drawings and equations to show and solve each story."},
    {"q": "How can I help my child with “how many more” questions?",
     "a": "Line up two rows of objects and match them one to one. The extra objects are the answer, so 8 apples and 5 apples gives 8 − 5 = 3 more."},
    {"q": "What is a bar model in Grade 1 math?",
     "a": "A bar model shows a whole as a long bar and its two parts as shorter bars under it. If both parts are known, add; if the whole and one part are known, subtract."},
    {"q": "Should Grade 1 students use key words to solve word problems?",
     "a": "Not by themselves. Words like “more” can trick children, so have them act out or draw the story first and then decide to add or subtract."},
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
            assert len(set(it["c"])) == 4, it
            assert it["q"].count("<svg") <= 1
            right = it["c"][it["a"]]
            if BOX in right:
                v = solve_box(right)
                assert all(solve_box(c) not in (None, v) for c in it["c"] if c != right), it
            else:
                assert len({lead(c) for c in it["c"]}) == 4, it
            plain = re.sub(r"<[^>]+>", " ", it["q"]).strip()
            assert plain not in seen, plain
            seen.add(plain)
            m = re.search(r"aria-label='bar model: whole (\S+), parts (\S+) and (\S+)'", it["q"])
            if m and BOX not in right:
                vals = [m.group(1), m.group(2), m.group(3)]
                k = vals.index("?")
                nn = [int(x) for x in vals if x != "?"]
                want = nn[0] + nn[1] if k == 0 else nn[0] - nn[1]
                assert lead(right) == want, it["q"]
            m = re.search(r"aria-label='picture: (\d+) \w+ and (\d+) more'", it["q"])
            if m and BOX not in right:
                assert lead(right) == int(m.group(1)) + int(m.group(2)), it["q"]
            m = re.search(r"aria-label='(?:picture|tens and ones blocks): (\d+) [^,]*, (\d+) crossed out'", it["q"])
            if m and BOX not in right:
                assert lead(right) == int(m.group(1)) - int(m.group(2)), it["q"]
            m = re.search(r"aria-label='tens and ones blocks: (\d+) \([^)]*\) and (\d+) more", it["q"])
            if m and BOX not in right:
                assert lead(right) == int(m.group(1)) + int(m.group(2)), it["q"]
            for t in [plain, it["e"]] + it["c"]:
                assert "\\" not in t and ".." not in t, t
                assert not re.search(r"\b1 (apples|stickers|cards|mitts|pucks|leaves|snowballs|children|cookies|geese|"
                                     r"books|boys|times|pages|hockey cards|maple leaves)\b", t), t
                assert not re.search(r"\b([2-9]|\d\d) (apple|sticker|card|mitt|puck|leaf|snowball|child|cookie|goose|"
                                     r"book|boy|time|page)\b(?!s)", t), t


def gen():
    rnd = random.Random(41805)
    P = People(rnd)
    J, Pc, Cc = Ctx(rnd, JOIN), Ctx(rnd, PARTS), Ctx(rnd, CMP)
    used = set()
    sets = [set_join(rnd, P, J, used), set_take(rnd, P, J, used), set_compare(rnd, P, Cc, used),
            set_parts(rnd, P, Pc, used), set_equation(rnd, P, J, Pc, Cc, used)]
    balance(sets, rnd)
    verify(sets)
    u = {
        "country": "ca-on", "subject": "math", "grade": "grade-1", "slug": "word-problems-to-50", "sort": 5,
        "updated": UPDATED, "pdf_url": "",
        "title": "Word Problems to 50",
        "seo_title": "Grade 1 Math Word Problems to 50 Worksheets: Join, Take Away and Compare (Ontario)",
        "short_title": "Word problems to 50",
        "domain": "Number",
        "standard_code": "Grade 1: B2.4",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Use objects, diagrams, and equations to represent, describe, and solve situations involving "
                         "addition and subtraction of whole numbers that add up to no more than 50",
        "meta_desc": "Free Grade 1 math worksheets on word problems to 50, matched to the Ontario curriculum: "
                     "join and take-away stories with pictures, compare stories, bar models and choosing the equation. "
                     "100 questions with an answer key.",
        "key_big": "Picture the story. Then decide: add or subtract?",
        "key_sub": "Some more come: add. Some go away: subtract. “How many more” means find the difference, "
                   "so subtract. Draw it, then write an equation with a ☐ for the missing number.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "picture|tens and ones blocks|bar model|compare bar model")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
