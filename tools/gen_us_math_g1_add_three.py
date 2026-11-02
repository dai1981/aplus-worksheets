# -*- coding: utf-8 -*-
"""
US Grade 1 Math: Add Three Numbers (1.OA.A.2)
  python tools/gen_us_math_g1_add_three.py
Every sum, missing number and picture count is checked in code.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "us", "math", "grade-1")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
RED = "#c0392b"
BLUE = "#2e6da4"
GOLD = "#e8b400"
PURPLE = "#8e5bb5"
INK = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"
BOX = "☐"
GIRLS = ["Maya", "Ava", "Mia", "Zoe", "Lily", "Emma", "Nora", "Ruby", "Sofia", "Grace"]
BOYS = ["Leo", "Noah", "Eli", "Sam", "Ben", "Omar", "Kai", "Jack", "Luis", "Owen"]


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e):
    """4 choices: correct + the first 3 unique distractors (no 0 or negatives). Positions are set by balance()."""
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        c = str(c)
        if c in seen or not c or c.startswith("-") or re.match(r"^0\b", c):
            continue
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    return {"q": q, "c": [correct] + pick, "a": 0, "e": e}


def balance(sets, rnd):
    """Spread the correct answers evenly over the 4 positions in every set."""
    for s in sets:
        targets = [0, 1, 2, 3] * 5
        rnd.shuffle(targets)
        for it, t in zip(s["items"], targets):
            c = it["c"]
            right = c[it["a"]]
            wrong = [x for i, x in enumerate(c) if i != it["a"]]
            rnd.shuffle(wrong)
            it["c"] = wrong[:t] + [right] + wrong[t:]
            it["a"] = t


class People:
    def __init__(self, rnd):
        self.pool = [(n, "she", "her") for n in GIRLS] + [(n, "he", "his") for n in BOYS]
        rnd.shuffle(self.pool)
        self.i = 0

    def next(self):
        p = self.pool[self.i % len(self.pool)]
        self.i += 1
        return p

    def ctx(self):
        """Names N, A, B, C (all different) and pronouns that match N."""
        ps = [self.next() for _ in range(3)]
        n, he, his = ps[0]
        return dict(N=n, he=he, He=cap(he), his=his, His=cap(his),
                    A=ps[0][0], B=ps[1][0], C=ps[2][0])


def cap(s):
    return s[0].upper() + s[1:]


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def text(x, y, t, fs=16, anchor="middle", col=INK):
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, col, anchor, t))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def plus(t):
    return " + ".join(str(x) for x in t)


def val(expr):
    """Value of '4 + 6 + 7' (only + is used in expressions that are compared)."""
    left = expr.split("=")[0].replace(BOX, "").strip()
    tot = 0
    for part in left.split("+"):
        part = part.strip()
        if "−" in part:
            x, y = part.split("−")
            tot += int(x) - int(y)
        else:
            tot += int(part)
    return tot


def strat_e(a, b, c):
    """Short explanation for a + b + c: make a ten first, else a double first, else left to right."""
    s = a + b + c
    t = (a, b, c)
    for i, j in [(0, 1), (0, 2), (1, 2)]:
        if t[i] + t[j] == 10:
            r = t[3 - i - j]
            return "Make a ten first: %d + %d = 10. Then 10 + %d = <b>%d</b>." % (t[i], t[j], r, s)
    for i, j in [(0, 1), (0, 2), (1, 2)]:
        if t[i] == t[j]:
            r = t[3 - i - j]
            return "Use a double: %d + %d = %d. Then %d + %d = <b>%d</b>." % (t[i], t[j], 2 * t[i], 2 * t[i], r, s)
    return "%d + %d = %d. Then %d + %d = <b>%d</b>." % (a, b, a + b, a + b, c, s)


# ------------------------------------------------------------ figures
def apple(cx, cy):
    return ("<circle cx='%d' cy='%d' r='9' fill='%s'/>"
            "<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>"
            "<ellipse cx='%d' cy='%d' rx='4' ry='2' fill='%s'/>"
            % (cx, cy + 1, RED, cx, cy - 7, cx + 1, cy - 11, INK, cx + 5, cy - 10, GREEN))


def star(cx, cy):
    import math
    pts = []
    for k in range(10):
        r = 10 if k % 2 == 0 else 4.2
        a = math.pi / 2 + k * math.pi / 5
        pts.append("%.1f,%.1f" % (cx + r * math.cos(a), cy - r * math.sin(a)))
    return "<polygon points='%s' fill='%s' stroke='%s' stroke-width='1'/>" % (" ".join(pts), GOLD, INK)


def ball(cx, cy):
    return ("<circle cx='%d' cy='%d' r='9' fill='%s'/>"
            "<path d='M %d %d Q %d %d %d %d' fill='none' stroke='#fff' stroke-width='2'/>"
            % (cx, cy, BLUE, cx - 9, cy, cx, cy - 6, cx + 9, cy))


def button(cx, cy):
    s = "<circle cx='%d' cy='%d' r='9' fill='%s'/>" % (cx, cy, PURPLE)
    for dx, dy in [(-3, -3), (3, -3), (-3, 3), (3, 3)]:
        s += "<circle cx='%d' cy='%d' r='1.6' fill='#fff'/>" % (cx + dx, cy + dy)
    return s


OBJ = {"apple": apple, "star": star, "ball": ball, "button": button}
GW, GH, ST = 88, 62, 26     # one group box and the step between objects (3 columns x 2 rows)


def groups_svg(groups, kind):
    """Three boxes of objects with + signs between them. Each box holds up to 6 objects."""
    o, gap = 6, 28
    draw = OBJ[kind]
    s = []
    count = 0
    for g, n in enumerate(groups):
        assert 1 <= n <= 6
        x0 = o + g * (GW + gap)
        s.append("<rect x='%d' y='%d' width='%d' height='%d' rx='8' fill='#fff' stroke='%s' stroke-width='2'/>"
                 % (x0, o, GW, GH, INK))
        rows = [min(n, 3), n - min(n, 3)] if n > 3 else [n]
        y_top = o + GH / 2 - (len(rows) - 1) * ST / 2
        for r, k in enumerate(rows):
            for i in range(k):
                cx = x0 + GW / 2 + (i - (k - 1) / 2) * ST
                cy = y_top + r * ST
                s.append(draw(int(cx), int(cy)))
                count += 1
        if g < len(groups) - 1:
            s.append(text(x0 + GW + gap / 2, o + GH / 2 + 8, "+", 22))
    assert count == sum(groups)
    W = 2 * o + 3 * GW + 2 * gap
    return svg_wrap(W, GH + 2 * o, "".join(s), "three groups of %ss: %s" % (kind, " and ".join(map(str, groups))))


CELL = 30
FW, FH = 5 * CELL, 2 * CELL     # one ten frame: 150 x 60


def frame(x0, y0, colors):
    """One ten frame at (x0, y0). colors: list of up to 10 fill colors, top row first, left to right."""
    assert len(colors) <= 10
    s = ["<rect x='%d' y='%d' width='%d' height='%d' fill='#fff' stroke='%s' stroke-width='3'/>"
         % (x0, y0, FW, FH, INK)]
    for i in range(1, 5):
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>"
                 % (x0 + i * CELL, y0, x0 + i * CELL, y0 + FH, INK))
    s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>"
             % (x0, y0 + CELL, x0 + FW, y0 + CELL, INK))
    for k, col in enumerate(colors):
        r, c = divmod(k, 5)
        s.append("<circle cx='%d' cy='%d' r='10' fill='%s'/>"
                 % (x0 + c * CELL + CELL // 2, y0 + r * CELL + CELL // 2, col))
    return "".join(s)


def frame3_svg(a, b, c):
    """One ten frame: a red, b green and c blue counters."""
    assert a + b + c <= 10
    o = 6
    return svg_wrap(FW + 2 * o, FH + 2 * o, frame(o, o, [RED] * a + [GREEN] * b + [BLUE] * c),
                    "ten frame with %d red, %d green and %d blue counters" % (a, b, c))


def frames_svg(p, q, r, horizontal=False):
    """Two ten frames: p red + q green fill the top frame (p + q = 10), r blue in the bottom frame."""
    assert p + q == 10 and r <= 10
    o, gap = 6, 12
    top, bottom = [RED] * p + [GREEN] * q, [BLUE] * r
    if horizontal:
        W, H = 2 * FW + gap + 2 * o, FH + 2 * o
        body = frame(o, o, top) + frame(o + FW + gap, o, bottom)
    else:
        W, H = FW + 2 * o, 2 * FH + gap + 2 * o
        body = frame(o, o, top) + frame(o, o + FH + gap, bottom)
    return svg_wrap(W, H, body, "two ten frames: %d red and %d green counters fill one, %d blue counters in the other" % (p, q, r))


def numline_svg(hops, end=20):
    """Number line 0 to end with one hop for each number, starting at 0."""
    L, step, Y = 16, 20, 66
    W = 2 * L + end * step
    X = lambda v: L + v * step
    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (L - 8, Y, W - L + 8, Y, INK)]
    for v in range(end + 1):
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (X(v), Y - 6, X(v), Y + 6, INK))
        s.append(text(X(v), Y + 24, str(v), 14))
    at = 0
    for h in hops:
        a, b = at, at + h
        mid = (X(a) + X(b)) / 2
        s.append("<path d='M %d %d Q %.1f %d %d %d' fill='none' stroke='%s' stroke-width='2.5'/>"
                 % (X(a), Y - 8, mid, Y - 52, X(b), Y - 8, GREEN))
        s.append(text(mid, Y - 36, "+%d" % h, 14, col=GREEN))
        at = b
    assert at <= end
    return svg_wrap(W, Y + 32, "".join(s), "number line from 0 to %d with hops of %s" % (end, ", ".join(map(str, hops))))


# ============================================================ set 1: three groups with pictures
def set_pictures(P):
    its = []
    unit = {"apple": "apples", "star": "stars", "ball": "balls", "button": "buttons"}
    counts = [((2, 3, 4), "apple"), ((1, 4, 2), "star"), ((3, 3, 2), "ball"), ((5, 1, 3), "button"),
              ((2, 2, 2), "apple"), ((4, 2, 4), "star"), ((1, 5, 3), "ball"), ((3, 1, 2), "button"),
              ((6, 1, 2), "apple"), ((2, 4, 1), "star")]
    for k, (t, kind) in enumerate(counts):
        a, b, c = t
        s = a + b + c
        assert s <= 10
        q = fig(groups_svg(t, kind)) + "How many %s are there in all?" % unit[kind]
        e = "Count each group: %d, %d and %d. %d + %d = %d. Then %d + %d = <b>%d</b>." % (a, b, c, a, b, a + b, a + b, c, s)
        cands = [a + b, s + 1, s - 1, b + c] if k % 2 == 0 else [b + c, s - 1, s + 1, a + b]
        its.append(mcq(q, s, cands, e))

    for t, kind in [((3, 2, 5), "ball"), ((4, 1, 3), "apple"), ((2, 5, 2), "button"), ((1, 3, 6), "star"), ((5, 2, 1), "apple")]:
        a, b, c = t
        s = a + b + c
        right = "%d + %d + %d" % t
        cands = ["%d + %d" % (a, b), "%d + %d + %d" % (a, b, c + 1), "%d + %d" % (b, c), "%d + %d + %d" % (a + 1, b, c),
                 "%d + %d + %d" % (a, b - 1, c)]
        vals = {s}
        wrong = []
        for w in cands:
            if val(w) not in vals:
                vals.add(val(w))
                wrong.append(w)
        e = "The groups have %d, %d and %d %s. So the number sentence is <b>%s</b> = %d. Use all three groups." % (
            a, b, c, unit[kind], right, s)
        its.append(mcq(fig(groups_svg(t, kind)) + "Which number sentence matches the picture?", right, wrong, e))

    for t in [(5, 3, 2), (1, 6, 2), (4, 2, 1), (2, 2, 5), (3, 4, 3)]:
        a, b, c = t
        s = a + b + c
        q = fig(frame3_svg(a, b, c)) + "Use the ten frame. %d + %d + %d = <b>?</b>" % t
        e = "Count each color: %d red, %d green and %d blue. %s" % (a, b, c, strat_e(a, b, c))
        if s == 10:
            e += " The ten frame is full."
        its.append(mcq(q, s, [a + b, s - 1, b + c, s + 1], e))
    assert len(its) == 20, len(its)
    return {"title": "Add three groups with pictures", "items": its}


# ============================================================ set 2: add three numbers within 20
def set_within_20(P):
    its = []
    plain = [(2, 5, 3), (6, 2, 1), (3, 4, 5), (8, 1, 2), (5, 3, 6), (7, 2, 4),
             (9, 3, 2), (4, 8, 5), (9, 2, 5), (5, 6, 8), (2, 9, 7), (6, 5, 4)]
    for k, (a, b, c) in enumerate(plain):
        s = a + b + c
        assert s <= 20
        e = "Add two numbers first: %d + %d = %d. Then add the last number: %d + %d = <b>%d</b>." % (a, b, a + b, a + b, c, s)
        cands = [a + b, s + 1, s - 1, s + c] if k % 2 == 0 else [b + c, s - 1, s + 1, a + c]
        its.append(mcq("%d + %d + %d = <b>?</b>" % (a, b, c), s, cands, e))

    for a, b, c in [(4, 3, 6), (5, 2, 7), (2, 6, 3), (6, 3, 5)]:
        s = a + b + c
        right = "%d + %d + %d = %d" % (a, b, c, s)
        wrong = ["%d + %d = %d" % (a, b, a + b), "%d + %d + %d = %d" % (a, b, c, s + 1), "%d + %d + %d = %d" % (a, b, c, s - 1)]
        e = ("The hops are +%d, +%d and +%d. They start at 0 and end at %d. So <b>%s</b>."
             % (a, b, c, s, right))
        its.append(mcq(fig(numline_svg([a, b, c])) + "Which number sentence does the number line show?", right, wrong, e))

    for t, miss in [((4, 5, 3), 1), ((2, 7, 6), 1), ((2, 3, 5), 0), ((6, 2, 6), 2)]:
        s = sum(t)
        k = t[miss]
        shown = [str(x) if i != miss else BOX for i, x in enumerate(t)]
        known = [x for i, x in enumerate(t) if i != miss]
        q = "%s = %d<br>What number goes in the %s?" % (" + ".join(shown), s, BOX)
        e = "%d + %d = %d. Now %d + <b>%d</b> = %d. So the %s is %d." % (
            known[0], known[1], sum(known), sum(known), k, s, BOX, k)
        its.append(mcq(q, k, [s, sum(known), k + 1, k - 1, s - known[0]], e))
    assert len(its) == 20, len(its)
    return {"title": "Add three numbers within 20", "items": its}


# ============================================================ set 3: make a ten first
def set_make_ten(P):
    its = []
    # which two numbers make 10? (p, q make 10, r is the other number, in the order shown)
    for t, (p, q), r in [((4, 7, 6), (4, 6), 7), ((3, 5, 7), (3, 7), 5), ((8, 6, 2), (8, 2), 6), ((9, 4, 1), (9, 1), 4)]:
        right = "%d and %d" % (p, q)
        wrong = ["%d and %d" % (p, r), "%d and %d" % (r, q), "%d and %d" % (10 - r, r)]
        assert 10 - r != r or True
        e = "%d + %d = <b>10</b>. %d + %d = %d and %d + %d = %d. " % (p, q, p, r, p + r, r, q, r + q)
        if 10 - r == r:
            e += "%d and %d make 10, but there is only one %d." % (r, r, r)
        else:
            e += "%d and %d make 10, but there is no %d here." % (10 - r, r, 10 - r)
        its.append(mcq("%s<br>Which two numbers make 10?" % plus(t), right, wrong, e))

    for k, t in enumerate([(4, 7, 6), (3, 8, 7), (6, 5, 4), (9, 6, 1), (2, 3, 8)]):
        a, b, c = t
        s = sum(t)
        r = [x for x in t if 10 - x not in t or (10 - x == x and t.count(x) < 2)]
        assert len(r) == 1, t
        r = r[0]
        bad = "10%d" % r
        if k in (0, 2):
            cands = [bad, a + b, s - 1, s + 1]
            e = strat_e(a, b, c) + " Not %s: 10 and %d more is %d." % (bad, r, s)
        else:
            cands = [a + b, s + 1, s - 1, b + c]
            e = strat_e(a, b, c)
        its.append(mcq("Make a ten first. %s = <b>?</b>" % plus(t), s, cands, e))

    for a, b, c in [(8, 5, 2), (7, 4, 3), (1, 6, 9), (6, 8, 4)]:
        s = a + b + c
        p, q, r = (a, c, b)
        assert p + q == 10
        right = "%d + %d = 10, then 10 + %d = %d" % (p, q, r, s)
        wrong = ["%d + %d = 10, then 10 + %d = 10%d" % (p, q, r, r),
                 "%d + %d = 10, then 10 + %d = %d" % (p, r, q, 10 + q),
                 "%d + %d = 10, then 10 + %d = %d" % (p, q, r, s + 1)]
        e = "%d and %d make 10. %d + %d is not 10, it is %d. Then 10 + %d = <b>%d</b>." % (p, q, p, r, p + r, r, s)
        its.append(mcq("Which way makes a ten first for %d + %d + %d?" % (a, b, c), right, wrong, e))

    for a, b, c in [(3, 6, 7), (2, 5, 8), (1, 7, 9)]:
        s = a + b + c
        q = fig(frames_svg(a, c, b)) + "Use the ten frames. %d + %d + %d = <b>?</b>" % (a, b, c)
        e = ("%d red and %d green counters fill the top frame: %d + %d = 10. The bottom frame has %d. 10 + %d = <b>%d</b>."
             % (a, c, a, c, b, b, s))
        its.append(mcq(q, s, ["10%d" % b, s + 1, a + b, s - 1], e))

    for t in [(7, 8, 3), (6, 2, 4), (1, 5, 9), (8, 9, 2)]:
        s = sum(t)
        k = s - 10
        pair = [x for x in t if x != k]
        q = "%s = 10 + <b>?</b>" % plus(t)
        e = "%d + %d = 10. The number left is %d. So %s = 10 + <b>%d</b> = %d." % (pair[0], pair[1], k, plus(t), k, s)
        its.append(mcq(q, k, [s, pair[1], k + 1, k - 1], e))
    assert len(its) == 20, len(its)
    return {"title": "Make a ten first", "items": its}


# ============================================================ set 4: doubles first, any order
def set_doubles_order(P):
    its = []
    for t in [(5, 2, 5), (6, 3, 6), (4, 4, 7), (7, 2, 7), (3, 8, 3), (8, 1, 8)]:
        s = sum(t)
        n = [x for x in t if t.count(x) == 2][0]
        r = [x for x in t if x != n][0]
        e = "Find the double: %d + %d = %d. Then %d + %d = <b>%d</b>." % (n, n, 2 * n, 2 * n, r, s)
        its.append(mcq("Use a double. %s = <b>?</b>" % plus(t), s, [2 * n, s + 1, s - 1, s + r, n + r], e))

    for t in [(2, 7, 2), (6, 1, 6), (9, 9, 2), (3, 4, 4)]:
        n = [x for x in t if t.count(x) == 2][0]
        r = [x for x in t if x != n][0]
        right = "%d + %d = %d" % (n, n, 2 * n)
        wrong = ["%d + %d = %d" % (n, n, 2 * n + 1), "%d + %d = %d" % (r, r, 2 * r), "%d + %d = %d" % (n, n, 2 * n - 1)]
        e = ("There are two %ds, so start with <b>%d + %d = %d</b>. There is only one %d, so %d + %d does not fit. Then %d + %d = %d."
             % (n, n, n, 2 * n, r, r, r, 2 * n, r, sum(t)))
        its.append(mcq("Use a double first. What is the first step for %s?" % plus(t), right, wrong, e))

    for t, perm in [((4, 9, 1), (1, 4, 9)), ((2, 6, 3), (3, 2, 6)), ((7, 5, 2), (2, 7, 5)),
                    ((3, 8, 6), (6, 8, 3)), ((6, 1, 4), (4, 6, 1))]:
        a, b, c = t
        s = sum(t)
        right = plus(perm)
        cands = ["%d + %d" % (a, b), "%d + %d + %d" % (a, b, c + 1), "%d + %d + %d" % (a, a, b), "%d + %d + %d" % (a, b - 1, c)]
        vals = {s}
        wrong = []
        for w in cands:
            if val(w) not in vals:
                vals.add(val(w))
                wrong.append(w)
        assert val(right) == s and sorted(perm) == sorted(t)
        e = "You can add in any order. <b>%s</b> has the same three numbers, so it is also %d." % (right, s)
        its.append(mcq("Which has the same sum as %s?" % plus(t), right, wrong, e))

    for t, perm in [((3, 5, 2), (2, 3, 5)), ((6, 4, 7), (7, 6, 4)), ((8, 3, 1), (1, 8, 3)),
                    ((2, 7, 9), (9, 2, 7)), ((5, 4, 6), (4, 6, 5))]:
        s = sum(t)
        q = "%s = %d<br>What is %s?" % (plus(t), s, plus(perm))
        e = "The numbers are the same. Only the order changed. So the sum is still <b>%d</b>." % s
        its.append(mcq(q, s, [perm[0] + perm[1], s + 1, s - 1], e))
    assert len(its) == 20, len(its)
    return {"title": "Doubles first and any order", "items": its}


# ============================================================ set 5: word problems
STORIES = [
    ("{A} has 3 stickers. {B} has 5 stickers. {C} has 4 stickers. How many stickers do they have in all?", (3, 5, 4), "stickers"),
    ("A red bowl has 4 apples. A blue bowl has 2 apples. A green bowl has 6 apples. How many apples are there in all?", (4, 2, 6), "apples"),
    ("{N} sees 5 ducks in a pond. Then 3 more ducks come. Then 5 more ducks come. How many ducks are in the pond now?", (5, 3, 5), "ducks"),
    ("{N} reads 6 pages on Monday. {He} reads 4 pages on Tuesday. {He} reads 3 pages on Wednesday. How many pages does {he} read in all?", (6, 4, 3), "pages"),
    ("A box has 7 red crayons, 2 blue crayons and 3 green crayons. How many crayons are in the box?", (7, 2, 3), "crayons"),
    ("{N} has 2 toy cars, 8 toy trucks and 5 toy buses. How many toys does {he} have?", (2, 8, 5), "toys"),
    ("There are 6 birds in a tree. 6 more birds come. Then 1 more bird comes. How many birds are in the tree now?", (6, 6, 1), "birds"),
    ("{A} picks 9 flowers. {B} picks 1 flower. {C} picks 7 flowers. How many flowers do they pick in all?", (9, 1, 7), "flowers"),
    ("One tank has 5 fish. Another tank has 4 fish. A third tank has 5 fish. How many fish are there in all?", (5, 4, 5), "fish"),
    ("3 kids are on the slide. 8 kids are on the swings. 2 kids are in the sandbox. How many kids are there in all?", (3, 8, 2), "kids"),
    ("{N} eats 2 grapes. Then {he} eats 5 grapes. Then {he} eats 8 grapes. How many grapes does {he} eat in all?", (2, 5, 8), "grapes"),
    ("The class has 4 goldfish, 2 turtles and 4 frogs as pets. How many pets does the class have?", (4, 2, 4), "pets"),
    ("{N} builds a tower with 6 red blocks, 5 blue blocks and 4 yellow blocks. How many blocks are in the tower?", (6, 5, 4), "blocks"),
    ("Mom bakes 7 muffins. Dad bakes 7 muffins. {N} bakes 3 muffins. How many muffins do they bake in all?", (7, 7, 3), "muffins"),
]

EQ_STORIES = [
    ("{N} has 5 red balloons, 3 blue balloons and 2 green balloons. How many balloons does {he} have?", (5, 3, 2)),
    ("A pet shop has 4 cats, 6 dogs and 2 rabbits. How many animals are there?", (4, 6, 2)),
    ("{N} finds 3 shells. Then {he} finds 7 more. Then {he} finds 1 more. How many shells does {he} find in all?", (3, 7, 1)),
    ("{A} has 8 marbles. {B} has 2 marbles. {C} has 6 marbles. How many marbles do they have in all?", (8, 2, 6)),
    ("A bus has 9 kids. 4 kids get on. Then 5 more kids get on. How many kids are on the bus now?", (9, 4, 5)),
    ("{N} has 2 pencils in {his} box, 4 in {his} bag and 9 on {his} desk. How many pencils does {he} have?", (2, 4, 9)),
]


def set_word_problems(P):
    its = []
    for k, (tpl, t, unit) in enumerate(STORIES):
        a, b, c = t
        s = sum(t)
        assert s <= 20
        q = tpl.format(**P.ctx())
        u = lambda x: "%d %s" % (x, unit)
        cands = [u(a + b), u(s + 1), u(s - 1), u(b + c)] if k % 2 == 0 else [u(b + c), u(s - 1), u(s + 1), u(a + b)]
        e = "Add all three numbers: %d + %d + %d. %s" % (a, b, c, strat_e(a, b, c))
        its.append(mcq(q, u(s), cands, e))

    for tpl, t in EQ_STORIES:
        a, b, c = t
        s = sum(t)
        q = tpl.format(**P.ctx()) + "<br>Which number sentence matches the story?"
        right = "%d + %d + %d = %s" % (a, b, c, BOX)
        cands = ["%d + %d = %s" % (a, b, BOX), "%d + %d − %d = %s" % (a, b, c, BOX),
                 "%d + %d + %d = %s" % (a, b, b, BOX), "%d + %d = %s" % (b, c, BOX)]
        vals = {s}
        wrong = []
        for w in cands:
            if val(w) not in vals and val(w) > 0:
                vals.add(val(w))
                wrong.append(w)
        e = "The story puts three groups together: %d, %d and %d. So add all three: <b>%s</b>. %s" % (
            a, b, c, right, strat_e(a, b, c).replace("<b>", "").replace("</b>", ""))
        e = e.rstrip(".") + ", so the %s is %d." % (BOX, s)
        its.append(mcq(q, right, wrong, e))
    assert len(its) == 20, len(its)
    return {"title": "Word problems with three numbers", "items": its}


# ============================================================ lesson
def body_html():
    return (
        "<h2>Add three numbers, two at a time</h2>"
        "<p>You can add three numbers. Add two of them first. Then add the third number to that sum. "
        "The numbers can go in <b>any order</b>. The sum stays the same.</p>"
        "<figure class='sn-fig'>" + groups_svg((2, 3, 4), "apple") +
        "<figcaption>2 + 3 + 4: 2 + 3 = 5. Then 5 + 4 = 9 apples.</figcaption></figure>"
        + ex("Example", "5 + 1 + 3 = ?", "5 + 1 = 6. Then 6 + 3 = 9.", "9")
        + "<h2>Look for a ten</h2>"
        "<p>Do two of the numbers make 10? Add them first. Adding to 10 is easy: 10 + 7 = 17.</p>"
        + "<p>Pairs that make 10: <b>1 + 9, 2 + 8, 3 + 7, 4 + 6, 5 + 5</b>.</p>"
        "<figure class='sn-fig'>" + frames_svg(4, 6, 7, horizontal=True) +
        "<figcaption>4 + 7 + 6: 4 red and 6 green fill one ten frame. 10 + 7 = 17.</figcaption></figure>"
        + ex("Example", "4 + 7 + 6 = ?", "4 + 6 = 10. Then 10 + 7 = 17.", "17")
        + "<h2>Look for a double</h2>"
        "<p>If two numbers are the same, add the double first.</p>"
        + ex("Example", "5 + 2 + 5 = ?", "5 + 5 = 10. Then 10 + 2 = 12.", "12")
        + "<h2>Use a number line</h2>"
        "<p>Start at 0. Make one hop for each number. Where you stop is the sum.</p>"
        "<figure class='sn-fig'>" + numline_svg([3, 4, 5]) +
        "<figcaption>3 + 4 + 5: hop 3, then 4, then 5. You stop at 12.</figcaption></figure>"
        + "<h2>Word problems</h2>"
        "<p>Read the story. Find all three numbers. Write a number sentence with a " + BOX + " for the answer.</p>"
        + ex("Example", "Mia has 3 stickers. Leo has 5 stickers. Ava has 4 stickers. How many stickers do they have in all?",
             "3 + 5 + 4 = " + BOX + ". 3 + 5 = 8. Then 8 + 4 = 12.", "12 stickers")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Adding only two numbers: 2 + 5 + 3 → 7", "Touch each number as you add it. Use all three."],
            ["Adding one number twice: 2 + 5 + 3 → 15", "Cross out each number when you use it."],
            ["Writing 10 + 7 as 107", "10 and 7 more is 17. It is 1 ten and 7 ones."],
            ["Counting the start: 9 + 3 → “9, 10, 11”", "Start at 9 and count on: 10, 11, 12."],
            ["Thinking the order changes the sum", "2 + 3 + 5 and 5 + 3 + 2 are both 10."],
        ])
    )


FAQ = [
    {"q": "How do 1st graders add three numbers?",
     "a": "They add two numbers first, then add the third number to that sum. For 2 + 5 + 3, think 2 + 5 = 7, then 7 + 3 = 10 (Common Core 1.OA.A.2)."},
    {"q": "Does the order matter when adding three numbers?",
     "a": "No. You can add the numbers in any order and the sum is the same. So pick the easiest pair first, like two numbers that make 10."},
    {"q": "What is the make a ten strategy for adding three numbers?",
     "a": "Look for two numbers that add to 10 and add them first. For 4 + 7 + 6, 4 + 6 = 10, and then 10 + 7 = 17."},
    {"q": "How can I help my child with three-number word problems?",
     "a": "Have your child find all three numbers in the story, then draw or use small objects for each group. Writing a number sentence like 3 + 5 + 4 = ☐ helps them use every number once."},
]


def mark_large(u, pattern):
    """Tag pictures that must print larger so they stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='[^']*(?:" + pattern + "))")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(103)
    P = People(rnd)
    sets = [set_pictures(P), set_within_20(P), set_make_ten(P), set_doubles_order(P), set_word_problems(P)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5)
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"] not in seen, it["q"]
            seen.add(it["q"])
            # sums in plain "a + b + c" choices are all different
            exprs = [c for c in it["c"] if re.match(r"^[\d +−]+$", c)]
            if len(exprs) == 4:
                assert len({val(c) for c in exprs}) == 4, it
    # pictures: the counters drawn match the label
    for s in sets:
        for it in s["items"]:
            m = re.search(r"aria-label='ten frame with (\d+) red, (\d+) green and (\d+) blue counters'", it["q"])
            if m:
                assert it["q"].count("<circle") == sum(int(x) for x in m.groups())
    u = {
        "country": "us", "subject": "math", "grade": "grade-1", "slug": "add-three-numbers", "sort": 3,
        "updated": UPDATED, "pdf_url": "",
        "title": "Add Three Numbers (Sums to 20)",
        "seo_title": "Grade 1 Adding Three Numbers Worksheets: Make a Ten, Doubles and Word Problems",
        "short_title": "Add three numbers",
        "domain": "Operations and Algebraic Thinking",
        "standard_code": "1.OA.A.2",
        "standard_url": "https://www.thecorestandards.org/Math/Content/1/OA/A/2/",
        "standard_text": "Solve word problems that call for addition of three whole numbers whose sum is less than or equal to 20, e.g., by using objects, drawings, and equations with a symbol for the unknown number to represent the problem.",
        "meta_desc": "Free Grade 1 worksheets for adding three numbers with sums to 20: count three groups of pictures, make a ten first, use doubles, add in any order, and solve 1st grade word problems. 100 questions with an answer key.",
        "key_big": "Add two numbers first. Then add the third.",
        "key_sub": "Look for two numbers that make 10, or a double. 4 + 7 + 6: 4 + 6 = 10, then 10 + 7 = 17. You can add in any order and the sum stays the same.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "three groups|number line")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
