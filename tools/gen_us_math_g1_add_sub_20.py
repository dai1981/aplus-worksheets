# -*- coding: utf-8 -*-
"""
US Grade 1 Math: Addition and Subtraction Within 20 (1.OA.C.6)
  python tools/gen_us_math_g1_add_sub_20.py
Every sum, difference and picture count is checked in code.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "us", "math", "grade-1")
UPDATED = "2026-11-02"
GREEN = "#006633"
RED = "#c0392b"
BLUE = "#2e6fb7"
GOLD = "#e0a800"
INK = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"
MINUS = "−"
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


def cap(s):
    return s[0].upper() + s[1:]


def pl(n, word):
    irregular = {"fish": "fish"}
    return "%d %s" % (n, word if n == 1 else irregular.get(word, word + "s"))


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


def mark_large(u, pattern):
    """Tag wide pictures (number lines, two groups side by side) so they print larger."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


# ------------------------------------------------------------ pictures: objects
OC = 30          # one object cell


def obj(kind, cx, cy, crossed=False):
    """One object centred at (cx, cy), about 24 units wide. Every object starts with <g class='o'>."""
    if kind == "apple":
        s = ("<circle cx='%d' cy='%d' r='10' fill='%s'/>"
             "<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2.5'/>"
             "<ellipse cx='%d' cy='%d' rx='4.5' ry='2.5' fill='%s'/>"
             % (cx, cy + 2, RED, cx, cy - 7, cx + 1, cy - 12, INK, cx + 5, cy - 10, GREEN))
    elif kind == "star":
        pts = []
        for k in range(10):
            r = 12 if k % 2 == 0 else 5
            a = math.pi / 2 + k * math.pi / 5
            pts.append("%.1f,%.1f" % (cx + r * math.cos(a), cy - r * math.sin(a)))
        s = "<polygon points='%s' fill='%s' stroke='%s' stroke-width='1.5'/>" % (" ".join(pts), GOLD, INK)
    elif kind == "ball":
        s = ("<circle cx='%d' cy='%d' r='11' fill='%s' stroke='%s' stroke-width='1.5'/>"
             "<path d='M %d %d Q %d %d %d %d' fill='none' stroke='#fff' stroke-width='2.5'/>"
             % (cx, cy, BLUE, INK, cx - 10, cy - 3, cx, cy + 6, cx + 10, cy - 3))
    else:   # dot
        s = "<circle cx='%d' cy='%d' r='10' fill='%s'/>" % (cx, cy, GREEN)
    if crossed:
        s = "<g opacity='0.45'>" + s + "</g>"
        s += ("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='3.5'/>"
              "<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='3.5'/>"
              % (cx - 12, cy - 12, cx + 12, cy + 12, INK, cx + 12, cy - 12, cx - 12, cy + 12, INK))
    return "<g class='o'>" + s + "</g>"


def grid(kind, x0, y0, n, crossed=0):
    """n objects in rows of 5. The last `crossed` objects get an X."""
    return "".join(obj(kind, x0 + (k % 5) * OC + OC // 2, y0 + (k // 5) * OC + OC // 2, k >= n - crossed)
                   for k in range(n))


def gw(n):
    return min(n, 5) * OC


def gh(n):
    return ((n + 4) // 5) * OC


def two_groups_svg(kind, a, b, name):
    o, gap = 4, 34
    W = gw(a) + gap + gw(b) + 2 * o
    H = max(gh(a), gh(b)) + 2 * o
    body = grid(kind, o, o, a) + text(o + gw(a) + gap / 2, H / 2 + 7, "+", 22) + grid(kind, o + gw(a) + gap, o, b)
    one = name[:-1]
    return svg_wrap(W, H, body, "two groups: %d %s and %d %s" % (a, one if a == 1 else name, b, one if b == 1 else name))


def crossed_svg(kind, n, k, name):
    o = 4
    return svg_wrap(gw(n) + 2 * o, gh(n) + 2 * o, grid(kind, o, o, n, k),
                    "%d %s, %d crossed out" % (n, name, k))


# ------------------------------------------------------------ pictures: ten frames
CELL = 30
FW, FH = 5 * CELL, 2 * CELL


def frame(x0, y0, colors):
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


def ten_frame_svg(colors, label):
    o = 6
    return svg_wrap(FW + 2 * o, FH + 2 * o, frame(o, o, colors), label)


def two_frames_svg(top, bottom, label, horizontal=False):
    o, gap = 6, 12
    if horizontal:
        W, H = 2 * FW + gap + 2 * o, FH + 2 * o
        body = frame(o, o, top) + frame(o + FW + gap, o, bottom)
    else:
        W, H = FW + 2 * o, 2 * FH + gap + 2 * o
        body = frame(o, o, top) + frame(o, o + FH + gap, bottom)
    return svg_wrap(W, H, body, label)


# ------------------------------------------------------------ pictures: dominoes
PIPS = {1: [(1, 1)], 2: [(0, 0), (2, 2)], 3: [(0, 0), (1, 1), (2, 2)],
        4: [(0, 0), (2, 0), (0, 2), (2, 2)], 5: [(0, 0), (2, 0), (1, 1), (0, 2), (2, 2)],
        6: [(0, 0), (0, 1), (0, 2), (2, 0), (2, 1), (2, 2)]}


def domino_body(x0, y0, a, b, half=60):
    s = ["<rect x='%d' y='%d' width='%d' height='%d' rx='10' fill='#fff' stroke='%s' stroke-width='3'/>"
         % (x0, y0, 2 * half, half, INK),
         "<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>"
         % (x0 + half, y0 + 6, x0 + half, y0 + half - 6, INK)]
    step = half // 4
    for k, n in enumerate((a, b)):
        for cx, cy in PIPS[n]:
            s.append("<circle cx='%d' cy='%d' r='6' fill='%s'/>"
                     % (x0 + k * half + step * (cx + 1), y0 + step * (cy + 1), INK))
    return "".join(s)


def domino_svg(a, b):
    o = 6
    return svg_wrap(120 + 2 * o, 60 + 2 * o, domino_body(o, o, a, b), "domino with %d and %d dots" % (a, b))


def dominoes_svg(pairs):
    o, gap = 6, 24
    body = "".join(domino_body(o + i * (120 + gap), o, a, b) for i, (a, b) in enumerate(pairs))
    W = len(pairs) * 120 + (len(pairs) - 1) * gap + 2 * o
    return svg_wrap(W, 60 + 2 * o, body, "dominoes " + " and ".join("%d and %d" % p for p in pairs))


# ------------------------------------------------------------ pictures: number lines
def number_line_svg(lo, hi, start=None, hops=(), step=30):
    """Number line lo..hi. `start` gets a green dot. hops: list of (from, to) arcs with a +/− label."""
    L, Y = 18, 66 if hops else 22
    W = 2 * L + (hi - lo) * step
    X = lambda v: L + (v - lo) * step
    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (L - 10, Y, W - L + 10, Y, INK)]
    for v in range(lo, hi + 1):
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (X(v), Y - 7, X(v), Y + 7, INK))
        s.append(text(X(v), Y + 27, str(v), 15))
    for a, b in hops:
        mid = (X(a) + X(b)) / 2
        s.append("<path d='M %d %d Q %.1f %d %d %d' fill='none' stroke='%s' stroke-width='2.5'/>"
                 % (X(a), Y - 9, mid, Y - 54, X(b), Y - 9, GREEN))
        s.append(text(mid, Y - 36, ("+%d" if b > a else MINUS + "%d") % abs(b - a), 16, col=GREEN))
    if start is not None:
        s.append("<circle cx='%d' cy='%d' r='7' fill='%s'/>" % (X(start), Y, GREEN))
    label = "number line from %d to %d" % (lo, hi) + (" with a dot on %d" % start if start is not None else "")
    return svg_wrap(W, Y + 34, "".join(s), label)


# ------------------------------------------------------------ math words
def make10_e(a, b):
    """Short make-10 explanation for a + b > 10."""
    big, small = max(a, b), min(a, b)
    need = 10 - big
    left = small - need
    assert need > 0 and left > 0
    first = "Start with %d. " % big if big != a else ""
    return ("%s%d needs %d to make 10. Take %d from the %d, and %d is left. 10 + %d = <b>%d</b>."
            % (first, big, need, need, small, left, left, a + b))


def on_e(a, b):
    return "Start at %d. Count on %d: %s. %d + %d = <b>%d</b>." % (
        a, b, ", ".join(str(a + i) for i in range(1, b + 1)), a, b, a + b)


def back_e(a, b):
    return "Start at %d. Count back %d: %s. %d %s %d = <b>%d</b>." % (
        a, b, ", ".join(str(a - i) for i in range(1, b + 1)), a, MINUS, b, a - b)


def sub_q(a, b):
    return "%d %s %d = <b>?</b>" % (a, MINUS, b)


# ============================================================ set 1: add within 10
def set_add10(P):
    its = []
    for kind, name, a, b in [("apple", "apples", 3, 2), ("star", "stars", 4, 3), ("ball", "balls", 2, 5),
                             ("apple", "apples", 5, 4), ("star", "stars", 1, 6), ("ball", "balls", 6, 2)]:
        s = a + b
        q = fig(two_groups_svg(kind, a, b, name)) + "How many %s in all?<br>%d + %d = <b>?</b>" % (name, a, b)
        e = "Count all the %s. Or start at %d and count on %d: %s. %d + %d = <b>%d</b>." % (
            name, a, b, ", ".join(str(a + i) for i in range(1, b + 1)), a, b, s)
        its.append(mcq(q, s, [s - 1, s + 1, abs(a - b), a], e))

    for r, g in [(4, 3), (5, 5), (6, 3), (2, 6)]:
        s = r + g
        q = (fig(ten_frame_svg([RED] * r + [GREEN] * g, "ten frame with %d red and %d green counters" % (r, g)))
             + "There are %d red and %d green counters. How many counters in all?" % (r, g))
        if s == 10:
            e = "Every box is full. A full ten frame is <b>10</b>. 5 + 5 = 10."
        else:
            e = "%d + %d = <b>%d</b>. The top row has 5. The bottom row has %d. 5 + %d = %d." % (
                r, g, s, s - 5, s - 5, s)
        its.append(mcq(q, s, [s - 1, s + 1, abs(r - g), 10 - s, 5], e))

    for a, b in [(6, 3), (5, 2), (7, 3), (4, 4)]:
        s = a + b
        q = (fig(number_line_svg(0, 10, start=a))
             + "Start at %d. Count on %d.<br>%d + %d = <b>?</b>" % (a, b, a, b))
        e = on_e(a, b) + " Do not count %d itself." % a
        its.append(mcq(q, s, [s - 1, s + 1, b, a], e))

    for a, b in [(5, 3), (2, 7), (3, 4), (1, 8)]:
        s = a + b
        if a == 1:
            e = "Adding 1 gives the next number. After 8 comes 9. 1 + 8 = <b>9</b>."
        else:
            big, small = max(a, b), min(a, b)
            e = "Start with the bigger number, %d. Count on %d: %s. %d + %d = <b>%d</b>." % (
                big, small, ", ".join(str(big + i) for i in range(1, small + 1)), a, b, s)
        its.append(mcq("%d + %d = <b>?</b>" % (a, b), s, [s - 1, s + 1, abs(a - b)], e))

    for a, b in [(3, 6), (2, 8)]:
        s = a + b
        q = "%d + %d = %d.<br>What is %d + %d?" % (b, a, s, a, b)
        e = "You can add in any order. %d + %d and %d + %d are the same: <b>%d</b>." % (b, a, a, b, s)
        its.append(mcq(q, s, [abs(b - a), s - 1, s + 1], e))
    assert len(its) == 20, len(its)
    return {"title": "Add within 10", "items": its}


# ============================================================ set 2: subtract within 10
def set_sub10(P):
    its = []
    for kind, name, n, k in [("apple", "apples", 5, 2), ("ball", "balls", 7, 3), ("star", "stars", 8, 5),
                             ("apple", "apples", 9, 4), ("ball", "balls", 6, 1), ("star", "stars", 10, 3)]:
        d = n - k
        q = (fig(crossed_svg(kind, n, k, name))
             + "Some %s are crossed out. How many are left?<br>%s" % (name, sub_q(n, k)))
        e = "There are %d %s. %d %s crossed out. Count the ones with no X: <b>%d</b>. %d %s %d = %d." % (
            n, name, k, "is" if k == 1 else "are", d, n, MINUS, k, d)
        its.append(mcq(q, d, [d + 1, d - 1, n + k, k], e))

    for a, b in [(9, 2), (7, 3), (10, 2), (6, 3)]:
        d = a - b
        q = fig(number_line_svg(0, 10, start=a)) + "Start at %d. Count back %d.<br>%s" % (a, b, sub_q(a, b))
        e = back_e(a, b) + " Do not count %d itself." % a
        its.append(mcq(q, d, [d + 1, d - 1, a + b], e))

    for x, y in [(4, 5), (3, 5), (2, 6), (3, 7)]:
        s = x + y
        q = "%d + %d = %d.<br>So %s" % (x, y, s, sub_q(s, x))
        e = "Think addition. %d + <b>%d</b> = %d, so %d %s %d = <b>%d</b>." % (x, y, s, s, MINUS, x, y)
        its.append(mcq(q, y, [x, s + x, y + 1, y - 1], e))

    for a, s in [(2, 9), (5, 7)]:
        k = s - a
        e = "Count on from %d to %d: %s. That is %d jumps. %d + <b>%d</b> = %d." % (
            a, s, ", ".join(str(a + i) for i in range(1, k + 1)), k, a, k, s)
        its.append(mcq("%d + <b>?</b> = %d" % (a, s), k, [a + s, k + 1, s], e))

    for a, b in [(10, 4), (8, 6), (9, 5), (7, 1)]:
        d = a - b
        if b == 1:
            e = "Taking away 1 gives the number before. Just before 7 is 6. 7 %s 1 = <b>6</b>." % MINUS
        else:
            e = "Think addition: %d + <b>%d</b> = %d. So %d %s %d = %d." % (b, d, a, a, MINUS, b, d)
        its.append(mcq(sub_q(a, b), d, [a + b, d + 1, d - 1], e))
    assert len(its) == 20, len(its)
    return {"title": "Subtract within 10", "items": its}


# ============================================================ set 3: make 10
def set_make10(P):
    its = []
    for n in [7, 4, 9, 6, 3]:
        k = 10 - n
        q = fig(ten_frame_svg([RED] * n, "ten frame with %d counters" % n)) + "How many more counters make 10?"
        e = "A ten frame has 10 boxes. %d boxes have counters, so <b>%d</b> %s empty. %d + %d = 10." % (n, k, "box is" if k == 1 else "boxes are", n, k)
        its.append(mcq(q, k, [k + 1, k - 1, n, 10], e))

    for a in [8, 5, 1, 2]:
        k = 10 - a
        e = "%d and %d make 10. Count on from %d: %s. That is <b>%d</b>." % (
            a, k, a, ", ".join(str(a + i) for i in range(1, k + 1)), k)
        its.append(mcq("%d + <b>?</b> = 10" % a, k, [k + 1, k - 1, a, 10], e))

    for (a, b), qt in zip([(6, 4), (3, 7)], ["Which two numbers make 10?", "Which pair adds up to 10?"]):
        wrong = [(a, b + 1), (a - 1, b), (a + 1, b + 1)]
        assert a + b == 10 and all(x + y != 10 for x, y in wrong)
        e = "%d + %d = <b>10</b>. The others make %d, %d and %d." % (a, b, *[x + y for x, y in wrong])
        its.append(mcq(qt, "%d and %d" % (a, b), ["%d and %d" % w for w in wrong], e))

    for a, b in [(8, 6), (9, 5), (7, 4), (9, 3), (8, 5)]:
        need = 10 - a
        k = b - need
        q = (fig(two_frames_svg([RED] * a, [GREEN] * b, "ten frames with %d and %d counters" % (a, b)))
             + "Move %d green counter%s up to fill the top frame.<br>%d + %d = 10 + <b>?</b>"
             % (need, "" if need == 1 else "s", a, b))
        e = ("The top frame now has 10. The bottom frame has %d %s left. So %d + %d = 10 + <b>%d</b> = %d."
             % (k, "counter" if k == 1 else "counters", a, b, k, a + b))
        its.append(mcq(q, k, [b, need, k + 1, k - 1, k + 2], e))

    for a, b in [(9, 4), (7, 5), (8, 3), (6, 8)]:
        s = a + b
        need = 10 - max(a, b)
        q = "%d + %d = 10 + %d = <b>?</b>" % (a, b, s - 10)
        e = make10_e(a, b) + " 10 + %d is 1 ten and %s." % (s - 10, pl(s - 10, "one"))
        its.append(mcq(q, s, ["10%d" % (s - 10), s - 1, s + 1], e))
    assert len(its) == 20, len(its)
    return {"title": "Make 10", "items": its}


# ============================================================ set 4: doubles and near doubles
HOOK = {2: "", 3: "", 4: "A spider has 8 legs: 4 on each side.",
        5: "Two hands have 10 fingers: 5 and 5.",
        6: "An egg box has 2 rows of 6 eggs: 12 eggs.",
        7: "Two weeks have 14 days: 7 and 7.",
        8: "8 + 2 = 10, and 6 more is 16.",
        9: "10 + 10 = 20. Take away 2, and you get 18."}


def set_doubles(P):
    its = []
    for n in [2, 3, 4, 5, 6]:
        q = fig(domino_svg(n, n)) + "%d + %d = <b>?</b>" % (n, n)
        e = ("%d + %d is a double. %d + %d = <b>%d</b>. %s" % (n, n, n, n, 2 * n, HOOK[n])).strip()
        its.append(mcq(q, 2 * n, [2 * n - 1, 2 * n + 1, 2 * n + 2, n], e))
    for n in [7, 8, 9]:
        e = "%d + %d is a double. %d + %d = <b>%d</b>. %s" % (n, n, n, n, 2 * n, HOOK[n])
        its.append(mcq("%d + %d = <b>?</b>" % (n, n), 2 * n, [2 * n - 2, 2 * n + 2, 2 * n + 1], e))

    for a, b in [(3, 4), (5, 4), (5, 6), (6, 7), (8, 7), (8, 9)]:
        lo, hi = min(a, b), max(a, b)
        q = (fig(domino_svg(a, b)) if hi <= 6 else "") + "Use a double. %d + %d = <b>?</b>" % (a, b)
        e = "%d + %d = %d. %d is 1 more than %d, so add 1 more: %d + 1 = <b>%d</b>." % (
            lo, lo, 2 * lo, hi, lo, 2 * lo, a + b)
        its.append(mcq(q, a + b, [2 * lo, 2 * hi, 2 * lo - 1], e))

    for a, b in [(7, 8), (4, 5)]:
        q = "%d + %d = %d + %d + <b>?</b>" % (a, b, a, a)
        e = "%d is 1 more than %d. So %d + %d is %d + %d and <b>1</b> more: %d + 1 = %d." % (
            b, a, a, b, a, a, 2 * a, a + b)
        its.append(mcq(q, 1, [2, b, a], e))

    for a, b in [(6, 7), (5, 6)]:
        right = "%d + %d + 1" % (a, a)
        wrong = ["%d + %d + 2" % (a, a), "%d + %d + 1" % (b, b), "%d + %d" % (a, a)]
        e = "%d is 1 more than %d. Double the smaller number and add 1: %d + %d + 1 = <b>%d</b>." % (
            b, a, a, a, a + b)
        its.append(mcq("Which one has the same answer as %d + %d?" % (a, b), right, wrong, e))

    nm, he, his = P.next()
    its.append(mcq("%s knows 9 + 9 = 18. What is 9 + 8?" % nm, 17, [19, 18, 16],
                   "8 is 1 less than 9. So 9 + 8 is 1 less than 9 + 9: 18 %s 1 = <b>17</b>." % MINUS))
    nm, he, his = P.next()
    its.append(mcq("%s knows 6 + 6 = 12. How can %s find 6 + 5?" % (nm, he), "12 %s 1 = 11" % MINUS,
                   ["12 + 1 = 13", "12 %s 2 = 10" % MINUS, "12 + 5 = 17"],
                   "5 is 1 less than 6. So 6 + 5 is 1 less than 6 + 6: 12 %s 1 = <b>11</b>." % MINUS))
    assert len(its) == 20, len(its)
    return {"title": "Doubles and near doubles", "items": its}


# ============================================================ set 5: subtract within 20 and stories
def set_sub20(P):
    its = []
    for a, b in [(13, 4), (15, 7), (12, 5)]:
        part = a - 10
        k = b - part
        q = "%d %s %d = %d %s %d %s <b>?</b>" % (a, MINUS, b, a, MINUS, part, MINUS)
        e = ("%d %s %d = 10. You must take away %d in all, and %d is done. Take away <b>%d</b> more: 10 %s %d = %d."
             % (a, MINUS, part, b, part, k, MINUS, k, a - b))
        its.append(mcq(q, k, [b, part, k + 1], e))

    for a, b in [(14, 6), (11, 3), (16, 7)]:
        d = a - b
        part = a - 10
        q = "Go back to 10 first.<br>%s" % sub_q(a, b)
        e = "%d %s %d = 10. Then take away %d more: 10 %s %d = <b>%d</b>." % (
            a, MINUS, part, b - part, MINUS, b - part, d)
        its.append(mcq(q, d, [10 + b - part, d + 1, d - 1], e))

    for x, y in [(8, 4), (9, 6), (7, 6), (5, 8)]:
        s = x + y
        q = "%d + %d = %d.<br>So %s" % (x, y, s, sub_q(s, x))
        e = "Think addition. %d + <b>%d</b> = %d, so %d %s %d = <b>%d</b>." % (x, y, s, s, MINUS, x, y)
        its.append(mcq(q, y, [s + x, x, y + 1, y - 1], e))

    q = fig(number_line_svg(10, 20, start=17)) + "Start at 17. Count back 2.<br>%s" % sub_q(17, 2)
    its.append(mcq(q, 15, [16, 14, 19], back_e(17, 2) + " Do not count 17 itself."))
    its.append(mcq(sub_q(16, 8), 8, [24, 9, 7],
                   "Think of a double: 8 + 8 = 16. So 16 %s 8 = <b>8</b>." % MINUS))

    # (template, op, a, b, unit word)
    stories = [
        ("{N} has 9 apples. {He} gets 4 more. How many apples does {he} have now?", "add", 9, 4, "apple"),
        ("There are 12 birds. 5 fly away. How many birds are left?", "sub", 12, 5, "bird"),
        ("{N} has 6 red cars and 6 blue cars. How many cars does {he} have?", "add", 6, 6, "car"),
        ("There are 15 cookies. {N} eats 2. How many cookies are left?", "sub", 15, 2, "cookie"),
        ("A frog jumps 8 times. Then it jumps 7 more times. How many jumps is that in all?", "add", 8, 7, "jump"),
        ("{N} has 11 crayons. {He} gives 3 to a friend. How many crayons does {he} have left?", "sub", 11, 3, "crayon"),
        ("There are 7 fish in a tank. Dad puts in 5 more. How many fish are in the tank now?", "add", 7, 5, "fish"),
        ("14 kids play outside. 10 kids go in. How many kids are still outside?", "sub", 14, 10, "kid"),
    ]
    for tpl, op, a, b, unit in stories:
        nm, he, his = P.next()
        q = tpl.format(N=nm, he=he, He=cap(he))
        u = lambda x: pl(x, unit)
        if op == "add":
            s = a + b
            if a == b:
                e = "Put the cars together, so add. %d + %d is a double: <b>%d</b>." % (a, b, s)
                its.append(mcq(q, u(s), [u(s - 1), u(s + 2), u(s + 1)], e))
            else:
                e = "Put them together, so add. " + make10_e(a, b)
                its.append(mcq(q, u(s), [u(s - 1), u(s + 1), u(a - b)], e))
            continue
        d = a - b
        if b == 10:
            e = "Some go away, so subtract. 14 is 10 and 4. Take away the 10, and <b>4</b> are left. 14 %s 10 = 4." % MINUS
        elif b <= 3:
            e = "Some are gone, so subtract. " + back_e(a, b)
        else:
            e = "Some are gone, so subtract. Think addition: %d + <b>%d</b> = %d. So %d %s %d = %d." % (
                b, d, a, a, MINUS, b, d)
        its.append(mcq(q, u(d), [u(a + b), u(d + 1), u(d - 1)], e))
    assert len(its) == 20, len(its)
    return {"title": "Subtract within 20 and word problems", "items": its}


# ============================================================ lesson
def body_html():
    return (
        "<h2>Add: count on</h2>"
        "<p>To add, put two groups together. You do not have to count them all. "
        "Start at the bigger number and <b>count on</b>.</p>"
        "<figure class='sn-fig'>" + two_groups_svg("apple", 5, 3, "apples") +
        "<figcaption>5 + 3. Start at 5. Count on 3: 6, 7, 8. So 5 + 3 = 8.</figcaption></figure>"
        + ex("Count on", "6 + 3 = ?", "Say 6. Then count 3 more: 7, 8, 9.", "9") +
        "<h2>Subtract: take away</h2>"
        "<p>To subtract, take some away. Cross them out. Count what is left.</p>"
        "<figure class='sn-fig'>" + crossed_svg("ball", 8, 3, "balls") +
        "<figcaption>8 − 3. Cross out 3 balls. 5 balls are left. So 8 − 3 = 5.</figcaption></figure>"
        "<h2>Make 10</h2>"
        "<p>Learn the pairs that make 10: 1 + 9, 2 + 8, 3 + 7, 4 + 6 and 5 + 5. "
        "Then fill up a 10 to add bigger numbers.</p>"
        "<figure class='sn-fig'>" + two_frames_svg([RED] * 8 + [GREEN] * 2, [GREEN] * 4,
                                                   "8 + 6 shown as 10 + 4 on two ten frames", horizontal=True) +
        "<figcaption>8 + 6. Move 2 of the 6 to fill the frame. Now there are 10 and 4. 8 + 6 = 10 + 4 = 14.</figcaption></figure>"
        "<h2>Doubles and near doubles</h2>"
        "<p>A <b>double</b> adds a number to itself: 6 + 6 = 12. "
        "6 + 7 is 1 more than 6 + 6. So 6 + 7 = 6 + 6 + 1 = 13.</p>"
        "<figure class='sn-fig'>" + dominoes_svg([(5, 5), (5, 6)]) +
        "<figcaption>5 + 5 = 10. The second domino has 1 more dot. So 5 + 6 = 11.</figcaption></figure>"
        + table(["Double", "1 more"], [
            ["5 + 5 = 10", "5 + 6 = 11"],
            ["6 + 6 = 12", "6 + 7 = 13"],
            ["7 + 7 = 14", "7 + 8 = 15"],
            ["8 + 8 = 16", "8 + 9 = 17"],
        ]) +
        "<h2>Subtract within 20</h2>"
        "<p>Go back to 10 first. For 13 − 4, take away 3 to get 10. Then take away 1 more.</p>"
        "<figure class='sn-fig'>" + number_line_svg(8, 14, hops=[(13, 10), (10, 9)], step=40) +
        "<figcaption>13 − 3 = 10. 10 − 1 = 9. So 13 − 4 = 9.</figcaption></figure>"
        + ex("Think addition", "12 − 8 = ?", "Ask: 8 + what = 12? You know 8 + 4 = 12.", "4") +
        "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Counting the start number: 6 + 3 → “6, 7, 8”, so 8", "Say 6, then count 3 more: 7, 8, 9. 6 + 3 = 9"],
            ["Adding when you should take away: 12 − 5 = 17", "Words like “fly away”, “eat” and “left” mean subtract"],
            ["Writing 10 + 4 as 104", "10 + 4 is 1 ten and 4 ones. That is 14"],
            ["Doubling the wrong number: 6 + 7 → 7 + 7", "Double the smaller number and add 1: 6 + 6 + 1 = 13"],
        ])
    )


FAQ = [
    {"q": "What addition and subtraction should a 1st grader know?",
     "a": "By the end of Grade 1, children add and subtract within 20, and know facts within 10 quickly (Common Core 1.OA.C.6). They use strategies like counting on, making 10 and doubles."},
    {"q": "What is counting on in 1st grade math?",
     "a": "Counting on means starting at one number and counting up. For 6 + 3, say 6 and then count 7, 8, 9. Do not count the 6 again."},
    {"q": "How do you teach making 10 to a first grader?",
     "a": "Use a ten frame with 10 boxes. For 8 + 6, move 2 counters to fill the frame, so 8 + 6 becomes 10 + 4 = 14."},
    {"q": "How can a first grader subtract numbers like 13 − 4?",
     "a": "Go back to 10 first: 13 − 3 = 10, then 10 − 1 = 9. Or think addition: 4 + 9 = 13, so 13 − 4 = 9."},
]


def check(sets):
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5)
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            # no two choices with the same value (e.g. '12 − 1 = 11' style expressions are checked below)
            vals = [re.sub(r" [a-z]+$", "", c) for c in it["c"]]
            assert len(set(vals)) == 4, it
            exprs = [c for c in it["c"] if re.match(r"^\d+( [+−] \d+)+$", c)]
            if exprs:
                v = [eval(c.replace("−", "-")) for c in exprs]
                assert len(set(v)) == len(v), it["c"]
            assert it["q"] not in seen, it["q"]
            seen.add(it["q"])
            assert "\\" not in it["q"] + it["e"] and '"' not in it["q"] + it["e"]
            for c in it["c"]:
                for n in re.findall(r"\d+", c):
                    assert 0 < int(n) <= 30 or re.match(r"^10\d$", c), (it["q"], c)
            # pictures: object, counter and pip counts match the labels
            for m in re.finditer(r"aria-label='two groups: (\d+) \w+ and (\d+) \w+'", it["q"]):
                assert it["q"].count("class='o'") == int(m.group(1)) + int(m.group(2))
            for m in re.finditer(r"aria-label='(\d+) \w+, (\d+) crossed out'", it["q"]):
                assert it["q"].count("class='o'") == int(m.group(1))
                assert it["q"].count("stroke-width='3.5'") == 2 * int(m.group(2))
            m = re.search(r"aria-label='ten frame with (\d+) red and (\d+) green counters'", it["q"])
            if m:
                assert it["q"].count("<circle") == int(m.group(1)) + int(m.group(2))
            m = re.search(r"aria-label='ten frame with (\d+) counters'", it["q"])
            if m:
                assert it["q"].count("<circle") == int(m.group(1))
            m = re.search(r"aria-label='ten frames with (\d+) and (\d+) counters'", it["q"])
            if m:
                assert it["q"].count("<circle") == int(m.group(1)) + int(m.group(2))
            m = re.search(r"aria-label='domino with (\d+) and (\d+) dots'", it["q"])
            if m:
                assert it["q"].count("r='6'") == int(m.group(1)) + int(m.group(2))
            # the answer key: evaluate simple a + b = ? / a − b = ? questions
            plain = re.sub(r"<[^>]+>", " ", it["q"])
            m = re.search(r"(\d+) ([+−]) (\d+) = \?\s*$", plain.strip())
            if m:
                x, op, y = int(m.group(1)), m.group(2), int(m.group(3))
                want = x + y if op == "+" else x - y
                assert it["c"][it["a"]].split()[0] == str(want), (plain, it["c"], it["a"])
            # expression choices are true or evaluate correctly
            for c in it["c"]:
                m = re.match(r"^(\d+) ([+−]) (\d+) = (\d+)$", c)
                if m:
                    x, op, y, z = int(m.group(1)), m.group(2), int(m.group(3)), int(m.group(4))
                    assert (x + y if op == "+" else x - y) == z, c


def gen():
    rnd = random.Random(101)
    P = People(rnd)
    sets = [set_add10(P), set_sub10(P), set_make10(P), set_doubles(P), set_sub20(P)]
    balance(sets, rnd)
    check(sets)
    u = {
        "country": "us", "subject": "math", "grade": "grade-1", "slug": "addition-subtraction-within-20", "sort": 1,
        "updated": UPDATED, "pdf_url": "",
        "title": "Grade 1 Addition and Subtraction Within 20",
        "seo_title": "Grade 1 Addition and Subtraction Within 20 Worksheets: Count On, Make 10 and Doubles",
        "short_title": "Add and subtract within 20",
        "domain": "Operations and Algebraic Thinking",
        "standard_code": "1.OA.C.6",
        "standard_url": "https://www.thecorestandards.org/Math/Content/1/OA/C/6/",
        "standard_text": "Add and subtract within 20, demonstrating fluency for addition and subtraction within 10. Use strategies such as counting on; making ten (e.g., 8 + 6 = 8 + 2 + 4 = 10 + 4 = 14); decomposing a number leading to a ten (e.g., 13 − 4 = 13 − 3 − 1 = 10 − 1 = 9); using the relationship between addition and subtraction (e.g., knowing that 8 + 4 = 12, one knows 12 − 8 = 4); and creating equivalent but easier or known sums (e.g., adding 6 + 7 by creating the known equivalent 6 + 6 + 1 = 12 + 1 = 13).",
        "meta_desc": "Free 1st grade addition and subtraction worksheets within 20: add and subtract within 10 with pictures, make 10 with ten frames, doubles and near doubles, and subtract by going back to 10. 100 Grade 1 questions with an answer key.",
        "key_big": "Count on to add. Make 10 to add bigger numbers. Think addition to subtract.",
        "key_sub": "6 + 3: start at 6 and count 7, 8, 9. 8 + 6 = 10 + 4 = 14. 6 + 7 = 6 + 6 + 1 = 13. 13 − 4 = 9 because 4 + 9 = 13.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(two groups|number line)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
