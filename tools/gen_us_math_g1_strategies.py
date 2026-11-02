# -*- coding: utf-8 -*-
"""
US Grade 1 Math: Addition and Subtraction Strategies (1.OA.B.3, 1.OA.B.4, 1.OA.C.5)
  python tools/gen_us_math_g1_strategies.py
Turn-around facts, making a ten with three numbers, counting on and back,
fact families, and subtraction as an unknown-addend problem.
Every fact, choice and picture count is checked in code.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "us", "math", "grade-1")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
RED = "#c0392b"
INK = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"
M = "−"   # real minus sign
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
        if c in seen or not c or c.startswith("-") or c.startswith(M) or re.match(r"^0\b", c):
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
        self.pool = [(n, "she", "her") for n in GIRLS] + [(n, "he", "him") for n in BOYS]
        rnd.shuffle(self.pool)
        self.i = 0

    def next(self):
        p = self.pool[self.i % len(self.pool)]
        self.i += 1
        return p


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


def mark_large(u, pattern):
    """Tag wide pictures (number lines, cube trains) so they print larger."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def add(a, b):
    return "%d + %d = %d" % (a, b, a + b)


def sub(a, b):
    return "%d %s %d = %d" % (a, M, b, a - b)


def is_true(eq):
    """Check a fact like '11 − 3 = 8'."""
    x, op, y, _, z = eq.split()
    x, y, z = int(x), int(y), int(z)
    return (x + y if op == "+" else x - y) == z


def nums(eq):
    return {int(n) for n in re.findall(r"\d+", eq)}


def seq(a, b):
    """'10, 11, 12' from a to b (inclusive), either direction."""
    st = 1 if b >= a else -1
    return ", ".join(str(v) for v in range(a, b + st, st))


def unit(n, one, many):
    return "%d %s" % (n, one if n == 1 else many)


# ------------------------------------------------------------ figures
CUBE = 22


def cube(x, y, col):
    return ("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='2'/>"
            % (x, y, CUBE, CUBE, col, INK))


def trains_svg(a, b):
    """Top train: a red then b green cubes. Bottom train: the same train turned around (b green then a red)."""
    o, gap = 6, 12
    top = [RED] * a + [GREEN] * b
    bot = [GREEN] * b + [RED] * a
    s = [cube(o + i * CUBE, o, c) for i, c in enumerate(top)]
    s += [cube(o + i * CUBE, o + CUBE + gap, c) for i, c in enumerate(bot)]
    W, H = (a + b) * CUBE + 2 * o, 2 * CUBE + gap + 2 * o
    return svg_wrap(W, H, "".join(s), "cube train of %d red and %d green cubes and the same train turned around" % (a, b))


def one_train_svg(a, b):
    o = 6
    s = [cube(o + i * CUBE, o, c) for i, c in enumerate([RED] * a + [GREEN] * b)]
    return svg_wrap((a + b) * CUBE + 2 * o, CUBE + 2 * o, "".join(s), "cube train of %d red and %d green cubes" % (a, b))


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


def turn_dominoes_svg(a, b):
    """Domino a|b, an arrow, and the same domino turned around b|a."""
    o, gap = 6, 44
    x2 = o + 120 + gap
    ax = o + 120 + 8
    arrow = ("<path d='M %d 36 h %d' stroke='%s' stroke-width='3'/>"
             "<polygon points='%d,36 %d,29 %d,43' fill='%s'/>" % (ax, gap - 22, GREEN, ax + gap - 14, ax + gap - 24, ax + gap - 24, GREEN))
    body = domino_body(o, o, a, b) + arrow + domino_body(x2, o, b, a)
    return svg_wrap(x2 + 120 + o, 60 + 2 * o, body, "domino with %d and %d dots turned around" % (a, b))


STEP = 32


def numline_svg(lo, hi, start, hops=0):
    """Number line lo..hi with a dot at start. hops > 0: jumps right, hops < 0: jumps left, one jump per number."""
    L = 22
    Y = 50 if hops else 26
    W = 2 * L + (hi - lo) * STEP
    X = lambda v: L + (v - lo) * STEP
    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (L - 14, Y, W - L + 14, Y, INK)]
    for v in range(lo, hi + 1):
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (X(v), Y - 7, X(v), Y + 7, INK))
        s.append(text(X(v), Y + 28, str(v), 16, col=RED if v == start else INK))
    d = 1 if hops > 0 else -1
    for k in range(abs(hops)):
        a, b = start + d * k, start + d * (k + 1)
        assert lo <= b <= hi
        xa, xb = X(a), X(b)
        mid = (xa + xb) / 2
        s.append("<path d='M %d %d Q %.1f %d %d %d' fill='none' stroke='%s' stroke-width='2.5'/>"
                 % (xa, Y - 10, mid, Y - 44, xb, Y - 10, GREEN))
        s.append("<polygon points='%d,%d %d,%d %d,%d' fill='%s'/>"
                 % (xb, Y - 9, xb - d * 2, Y - 20, xb - d * 10, Y - 13, GREEN))
    s.append("<circle cx='%d' cy='%d' r='7' fill='%s'/>" % (X(start), Y, RED))
    if hops:
        label = "number line from %d to %d with %d jumps %s from %d" % (lo, hi, abs(hops), "right" if d > 0 else "left", start)
    else:
        label = "number line from %d to %d with a dot at %d" % (lo, hi, start)
    return svg_wrap(W, Y + 36, "".join(s), label)


def nl_range(start, n, d):
    """12 numbers wide. Counting on: start sits 3 from the left; counting back: start sits 3 from the right."""
    if d > 0:
        lo = max(0, start - 3)
        hi = lo + 11
        assert start + n <= hi
    else:
        hi = start + 3
        lo = hi - 11
        if lo < 0:
            lo, hi = 0, 11
        assert start - n >= lo
    return lo, hi


def bond_svg(whole, a, b):
    """Number bond: whole on top, two parts below. Values may be '?'."""
    W, H, r = 176, 136, 26
    top, left, right = (88, 32), (34, 104), (142, 104)
    s = []
    for p in (left, right):
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='3'/>" % (top[0], top[1], p[0], p[1], INK))
    for (cx, cy), v, fill in [(top, whole, FILL), (left, a, "#fff"), (right, b, "#fff")]:
        s.append("<circle cx='%d' cy='%d' r='%d' fill='%s' stroke='%s' stroke-width='3'/>" % (cx, cy, r, fill, GREEN))
        s.append(text(cx, cy + 7, str(v), 20, col=RED if v == "?" else INK))
    return svg_wrap(W, H, "".join(s), "number bond: whole %s, parts %s and %s" % (whole, a, b))


def triangle_svg(top, a, b):
    """Fact triangle: the sum at the top corner, the two parts at the bottom corners."""
    W, H = 176, 140
    pts = "88,10 10,130 166,130"
    s = ["<polygon points='%s' fill='%s' stroke='%s' stroke-width='3' stroke-linejoin='round'/>" % (pts, FILL, GREEN),
         text(88, 52, str(top), 20, col=RED if top == "?" else INK),
         text(44, 120, str(a), 20, col=RED if a == "?" else INK),
         text(132, 120, str(b), 20, col=RED if b == "?" else INK),
         "<line x1='60' y1='68' x2='116' y2='68' stroke='%s' stroke-width='1.5' stroke-dasharray='4 4'/>" % GREEN]
    return svg_wrap(W, H, "".join(s), "fact triangle with %s at the top and %s and %s at the bottom" % (top, a, b))


# ============================================================ set 1: turn-around facts
def set_turn_around(P):
    its = []
    for a, b in [(5, 2), (4, 6), (6, 3), (1, 5)]:
        s = a + b
        q = fig(turn_dominoes_svg(a, b)) + "%s. The domino turns around. What is %d + %d?" % (add(a, b), b, a)
        e = "The domino has the same dots: %d and %d. %d + %d = %d + %d = <b>%d</b>. Turn-around facts have the same sum." % (
            b, a, b, a, a, b, s)
        its.append(mcq(q, s, [s - 1, s + 1, abs(a - b)], e))

    for a, b in [(8, 3), (9, 4), (7, 5), (6, 9)]:
        s = a + b
        q = (fig(trains_svg(a, b)) + "The top train shows %s. The bottom train is the same train turned around. "
             "What fact does it show?" % add(a, b))
        right = add(b, a)
        wrong = ["%d + %d = %d" % (b, a, s + 1), sub(a, b) if a > b else sub(b, a), "%d + %d = %d" % (b, a, s - 1)]
        e = ("The bottom train has the same cubes: %d green and %d red. %d + %d = <b>%d</b>. "
             "Changing the order does not change the sum." % (b, a, b, a, s))
        its.append(mcq(q, right, wrong, e))

    B = "<b>?</b>"
    for qt, x, y, ans in [("6 + 9 = 9 + %s", 6, 9, 6), ("%s + 7 = 7 + 5", 5, 7, 5), ("4 + 8 = %s + 4", 4, 8, 8)]:
        other = x + y - ans
        e = "Both sides use the same two numbers, %d and %d. So the missing number is <b>%d</b>. Both sides are %d." % (
            min(x, y), max(x, y), ans, x + y)
        its.append(mcq(qt % B, ans, [other, x + y, abs(x - y), ans + 1], e))

    its.append(mcq("Which is the same as 4 + 9?", "9 + 4", ["9 %s 4" % M, "4 + 10", "9 + 5"],
                   "Switch the order: 4 + 9 = 9 + 4 = <b>13</b>. 9 %s 4 is 5, not 13." % M))

    for a, b in [(7, 2), (10, 6)]:
        s = a + b
        q = "You know %s. Which fact do you also know?" % add(a, b)
        wrong = ["%d + %d = %d" % (b, a, s - 1), "%d %s %d = %d" % (a, M, b, s), "%d + %d = %d" % (b, a, s + 1)]
        e = "Turn it around: %d + %d = <b>%d</b> too. The sum stays the same." % (b, a, s)
        its.append(mcq(q, add(b, a), wrong, e))

    for a, b in [(2, 9), (3, 8)]:
        nm, he, _ = P.next()
        s = a + b
        q = "%s wants to count on to find %d + %d. What is the fastest way?" % (nm, a, b)
        right = "Start at %d, count on %d" % (b, a)
        wrong = ["Start at %d, count on %d" % (b, a + 1), "Start at %d, count back %d" % (b, a),
                 "Start at %d, count on %d" % (a, b - 1)]
        e = ("%d + %d = %d + %d. Start at the bigger number. Then there are only %d numbers to say: %s. "
             "%d + %d = <b>%d</b>." % (a, b, b, a, a, seq(b + 1, s), a, b, s))
        its.append(mcq(q, right, wrong, e))

    for a, b, c in [(7, 5, 3), (2, 6, 4)]:
        x, y, mid = (a, c, b) if a + c == 10 else (b, c, a)
        assert x + y == 10
        q = "%d + %d + %d = 10 + <b>?</b>" % (a, b, c)
        e = "Add the two numbers that make 10 first: %d + %d = 10. The %d is left. So the missing number is <b>%d</b>." % (x, y, mid, mid)
        its.append(mcq(q, mid, [y, x, a + b + c, mid + 1], e))
    for a, b, c in [(4, 9, 6), (8, 5, 2)]:
        assert a + c == 10
        t = a + b + c
        q = "Make a ten first. %d + %d + %d = <b>?</b>" % (a, b, c)
        e = "%d + %d = 10. Then 10 + %d = <b>%d</b>." % (a, c, b, t)
        its.append(mcq(q, t, [a + b, t - 1, t + 1], e))
    assert len(its) == 20, len(its)
    return {"title": "Turn-around facts and make a ten", "items": its}


# ============================================================ set 2: count on and count back
def set_count(P):
    its = []
    for s0, n in [(9, 3), (6, 2), (8, 3), (13, 2), (15, 3)]:
        lo, hi = nl_range(s0, n, 1)
        t = s0 + n
        q = fig(numline_svg(lo, hi, s0)) + "Start at %d. Count on %d.<br>%d + %d = <b>?</b>" % (s0, n, s0, n)
        e = "Start at %d. Do not count %d. Say the next %d numbers: %s. %d + %d = <b>%d</b>." % (
            s0, s0, n, seq(s0 + 1, t), s0, n, t)
        its.append(mcq(q, t, [t - 1, s0 - n, t + 1], e))

    for s0, n in [(12, 2), (10, 3), (16, 3), (11, 2)]:
        lo, hi = nl_range(s0, n, -1)
        t = s0 - n
        q = fig(numline_svg(lo, hi, s0)) + "Start at %d. Count back %d.<br>%d %s %d = <b>?</b>" % (s0, n, s0, M, n)
        e = "Start at %d. Do not count %d. Count back %d: %s. %d %s %d = <b>%d</b>." % (
            s0, s0, n, seq(s0 - 1, t), s0, M, n, t)
        its.append(mcq(q, t, [t + 1, s0 + n, t - 1], e))

    for s0, n in [(7, 4), (11, 3), (14, -4), (10, -2)]:
        lo, hi = nl_range(s0, abs(n), 1 if n > 0 else -1)
        q = fig(numline_svg(lo, hi, s0, n)) + "Which fact does the number line show?"
        if n > 0:
            t = s0 + n
            right = add(s0, n)
            wrong = [sub(s0, n), "%d + %d = %d" % (s0, n + 1, t + 1), "%d + %d = %d" % (s0, n, t - 1)]
            e = "Start at %d. There are %d jumps to the right. Right means add. %d + %d = <b>%d</b>." % (s0, n, s0, n, t)
        else:
            n = -n
            t = s0 - n
            right = sub(s0, n)
            wrong = [add(s0, n), "%d %s %d = %d" % (s0, M, n + 1, t - 1), "%d %s %d = %d" % (s0, M, n, t + 1)]
            e = "Start at %d. There are %d jumps to the left. Left means subtract. %d %s %d = <b>%d</b>." % (s0, n, s0, M, n, t)
        its.append(mcq(q, right, wrong, e))

    for (s0, n), nmq in [((8, 3), True), ((5, 4), True), ((14, 3), False)]:
        nm, he, _ = P.next()
        if nmq:
            t = s0 + n
            q = "%s counts on to find %d + %d. What does %s say?" % (nm, s0, n, he)
            right = seq(s0 + 1, t)
            wrong = [seq(s0, t - 1), seq(s0 - 1, s0 - n), seq(s0 + 1, t + 1)]
            e = "Start at %d and say the next %d numbers: %s. So %d + %d = <b>%d</b>." % (s0, n, right, s0, n, t)
        else:
            t = s0 - n
            q = "%s counts back to find %d %s %d. What does %s say?" % (nm, s0, M, n, he)
            right = seq(s0 - 1, t)
            wrong = [seq(s0, t + 1), seq(s0 + 1, s0 + n), seq(s0 - 1, t + 1)]
            e = "Start at %d and count back %d: %s. So %d %s %d = <b>%d</b>." % (s0, n, right, s0, M, n, t)
        its.append(mcq(q, right, wrong, e))

    for a, b in [(2, 7), (3, 9)]:
        big, small, t = max(a, b), min(a, b), a + b
        e = "Start at the bigger number, %d. Count on %d: %s. %d + %d = <b>%d</b>." % (big, small, seq(big + 1, t), a, b, t)
        its.append(mcq("Count on. %d + %d = <b>?</b>" % (a, b), t, [t - 1, big - small, t + 1], e))
    for s0, n in [(17, 3), (11, 2)]:
        t = s0 - n
        e = "Start at %d. Count back %d: %s. %d %s %d = <b>%d</b>." % (s0, n, seq(s0 - 1, t), s0, M, n, t)
        its.append(mcq("Count back. %d %s %d = <b>?</b>" % (s0, M, n), t, [t + 1, s0 + n, t - 1], e))
    assert len(its) == 20, len(its)
    return {"title": "Count on and count back", "items": its}


# ============================================================ set 3: fact families
def family(a, b):
    s = a + b
    return [add(a, b), add(b, a), sub(s, a), sub(s, b)]


def fam_e(a, b):
    s = a + b
    return "The family of %d, %d and %d: %s." % (a, b, s, ", ".join(family(a, b)))


def set_families(P):
    its = []
    belong = [((3, 8), "11 − 3 = 8", ["8 − 3 = 5", "11 + 3 = 14", "11 − 2 = 9"]),
              ((4, 9), "9 + 4 = 13", ["9 − 4 = 5", "13 − 3 = 10", "9 + 5 = 14"]),
              ((5, 7), "12 − 7 = 5", ["7 − 5 = 2", "12 − 2 = 10", "7 + 6 = 13"]),
              ((6, 8), "14 − 8 = 6", ["8 − 6 = 2", "14 + 6 = 20", "8 + 8 = 16"]),
              ((2, 9), "11 − 9 = 2", ["9 − 2 = 7", "11 + 2 = 13", "11 − 3 = 8"]),
              ((7, 9), "16 − 7 = 9", ["9 − 7 = 2", "16 − 6 = 10", "7 + 8 = 15"])]
    for (a, b), right, wrong in belong:
        fam = {a, b, a + b}
        assert right in family(a, b) and is_true(right)
        for w in wrong:
            assert is_true(w) and not nums(w) <= fam, w
        q = fig(triangle_svg(a + b, a, b)) + "Which fact is in this fact family?"
        e = ("This family uses only %d, %d and %d. <b>%s</b> uses only these numbers. "
             "The other facts are true, but they use a different number." % (a, b, a + b, right))
        its.append(mcq(q, right, wrong, e))

    for right, wrong, qt in [("5, 7, 12", ["5, 7, 13", "5, 6, 12", "4, 7, 12"], "Which three numbers make a fact family?"),
                             ("4, 8, 12", ["4, 8, 13", "4, 7, 12", "3, 8, 12"],
                              "Two numbers must add up to the third. Which three numbers make a fact family?")]:
        x, y, z = [int(v) for v in right.split(", ")]
        assert x + y == z
        for w in wrong:
            p, r, t = sorted(int(v) for v in w.split(", "))
            assert p + r != t, w
        e = "%d + %d = %d, so <b>%s</b> make a family. Check the others: %s." % (
            x, y, z, right, ", ".join("%s + %s is not %s" % tuple(w.split(", ")) for w in wrong))
        its.append(mcq(qt, right, wrong, e))

    for (a, b), odd in [((2, 7), "7 − 2 = 5"), ((5, 6), "6 − 5 = 1"), ((3, 9), "9 + 4 = 13"),
                        ((7, 8), "15 − 6 = 9"), ((4, 6), "6 − 4 = 2"), ((8, 9), "17 + 8 = 25")]:
        f = family(a, b)
        assert is_true(odd) and odd not in f and not nums(odd) <= {a, b, a + b}
        rnd_f = [f[0], f[2], f[3]] if (a + b) % 2 else [f[1], f[2], f[3]]
        q = "Which fact is <b>NOT</b> in the fact family of %d, %d and %d?" % (a, b, a + b)
        extra = sorted(nums(odd) - {a, b, a + b})
        e = "<b>%s</b> uses %s, which %s not in the family. %s" % (
            odd, " and ".join(str(v) for v in extra), "is" if len(extra) == 1 else "are", fam_e(a, b))
        its.append(mcq(q, odd, rnd_f, e))

    for a, b in [(9, 6), (8, 4)]:
        s = a + b
        q = "You know %s. Which subtraction fact do you also know?" % add(a, b)
        right = sub(s, b)
        wrong = ["%d %s %d = %d" % (b, M, s, a), "%d %s %d = %d" % (s, M, b, a - 1), "%d %s %d = %d" % (a, M, b, s)]
        e = ("Start with the biggest number, %d. Take away %d, and %d is left: <b>%s</b>. "
             "You cannot take %d away from %d." % (s, b, a, right, s, b))
        its.append(mcq(q, right, wrong, e))

    for a, b in [(6, 7), (5, 9)]:
        s = a + b
        f = family(a, b)
        q = "%s<br>%s<br>%s<br>%d %s <b>?</b> = %d" % (f[0], f[1], f[2], s, M, b)
        e = "The last fact is %d %s <b>%d</b> = %d. Check: %d + %d = %d." % (s, M, a, b, a, b, s)
        its.append(mcq(q, a, [b, s, a - 1, a + 1], e))
    for top, l, r, ans, cands in [(14, 8, "?", 6, [22, 7, 5]), ("?", 9, 7, 16, [2, 15, 17])]:
        q = fig(triangle_svg(top, l, r)) + "What number is missing from this fact family?"
        if top == "?":
            e = "The top number is the sum: %d + %d = <b>%d</b>." % (l, r, ans)
        else:
            e = "Think: %d + ? = %d. %d + <b>%d</b> = %d. So %d %s %d = %d." % (l, top, l, ans, top, top, M, l, ans)
        its.append(mcq(q, ans, cands, e))
    assert len(its) == 20, len(its)
    return {"title": "Fact families", "items": its}


# ============================================================ set 4: subtract by thinking addition
def ones_mistake(a, b):
    """13 − 9: a child does 9 − 3 = 6 and writes 16."""
    if a > 10 and a % 10 < b < 10:
        return 10 + b - a % 10
    return None


def think_e(a, b):
    d = a - b
    if b < 10 < a and b + d > 10:
        e = "Count up from %d to %d: %s. That is %d. " % (b, a, seq(b + 1, a), d)
    else:
        e = ""
    return e + "%d + <b>%d</b> = %d, so %d %s %d = %d." % (b, d, a, a, M, b, d)


def set_think_add(P):
    its = []
    for a, b in [(10, 8), (10, 6), (9, 7), (8, 5), (12, 10)]:
        d = a - b
        q = "%d %s %d = <b>?</b><br>Think: %d + ? = %d" % (a, M, b, b, a)
        its.append(mcq(q, d, [d + 1, a + b, d - 1], "Think addition. " + think_e(a, b)))

    for a, b in [(13, 9), (11, 8), (15, 7), (12, 9), (14, 6)]:
        d = a - b
        cands = [a + b, d + 1]
        if ones_mistake(a, b):
            cands.append(ones_mistake(a, b))
        cands.append(d - 1)
        q = fig(bond_svg(a, b, "?")) + "%d %s %d = <b>?</b><br>Think: %d + ? = %d" % (a, M, b, b, a)
        its.append(mcq(q, d, cands, "The whole is %d. One part is %d. " % (a, b) + think_e(a, b)))

    for a, b in [(15, 7), (13, 8), (11, 6), (16, 9)]:
        d = a - b
        right = add(b, d)
        wrong = [add(a, b), "%d + %d = %d" % (b, d, a + 1), "%d + %d = %d" % (b, d + 1, a)]
        q = "Which addition fact helps you find %d %s %d?" % (a, M, b)
        e = "Think: %d + what = %d? <b>%s</b>, so %d %s %d = %d. %s is true, but it does not help." % (
            b, a, right, a, M, b, d, add(a, b))
        its.append(mcq(q, right, wrong, e))

    for b, d in [(6, 8), (9, 3), (4, 7)]:
        a = b + d
        q = "<b>?</b> %s %d = %d" % (M, b, d)
        e = "Think addition: %d + %d = <b>%d</b>. Check: %d %s %d = %d." % (b, d, a, a, M, b, d)
        its.append(mcq(q, a, [abs(d - b), a - 1, a + 1], e))

    for (a, b), qt in [((16, 9), "Which fact is true?"), ((14, 8), "Check with addition. Which fact is right?"),
                       ((12, 5), "Which one is correct?")]:
        d = a - b
        right = sub(a, b)
        wrong = ["%d %s %d = %d" % (a, M, b, ones_mistake(a, b)), "%d %s %d = %d" % (a, M, b, d + 1),
                 "%d %s %d = %d" % (a, M, b, a + b)]
        e = ("Check with addition: %d + %d = %d, so <b>%s</b> is right. "
             "Do not do %d %s %d = %d and write %d." % (b, d, a, right, b, M, a % 10, b - a % 10, ones_mistake(a, b)))
        its.append(mcq(qt, right, wrong, e))
    assert len(its) == 20, len(its)
    return {"title": "Subtract by thinking addition", "items": its}


# ============================================================ set 5: word problems
UNITS = {"cars": ("car", "cars"), "apples": ("apple", "apples"), "birds": ("bird", "birds"),
         "grapes": ("grape", "grapes"), "stickers": ("sticker", "stickers"), "shells": ("shell", "shells"),
         "kids": ("kid", "kids"), "pages": ("page", "pages"), "beads": ("bead", "beads"), "marbles": ("marble", "marbles"),
         "pets": ("pet", "pets"), "ducks": ("duck", "ducks"), "plums": ("plum", "plums"), "fish": ("fish", "fish")}


def set_stories(P):
    its = []

    def story(tpl, ans, cands, e, kind):
        nm, he, him = P.next()
        m = P.next()[0] if "{M}" in tpl else ""
        q = tpl.format(N=nm, M=m, he=he, He=cap(he), him=him)
        one, many = UNITS[kind]
        u = lambda n: unit(n, one, many)
        its.append(mcq(q, u(ans), [u(c) for c in cands], e.format(N=nm, M=m)))

    story("{N} has 3 red cars and 9 blue cars. How many cars does {he} have?", 12, [11, 6, 13],
          "Put them together: 3 + 9 = 9 + 3. Start at 9 and count on 3: 10, 11, 12. That is <b>12 cars</b>.", "cars")
    story("{N} has 2 apples. {He} gets 8 more. How many apples does {he} have now?", 10, [9, 6, 11],
          "2 + 8 = 8 + 2. Start at 8 and count on 2: 9, 10. That is <b>10 apples</b>.", "apples")
    story("There are 12 birds in a tree. 2 birds fly away. How many birds are left?", 10, [11, 14, 9],
          "Some fly away, so subtract. Start at 12 and count back 2: 11, 10. That is <b>10 birds</b>.", "birds")
    story("There are 16 kids in a class. 3 kids go to the library. How many kids are still in the class?", 13, [14, 19, 12],
          "Some go away, so subtract. Start at 16 and count back 3: 15, 14, 13. That is <b>13 kids</b>.", "kids")
    story("{N} read 6 pages on Monday. {He} read 4 pages on Tuesday. How many pages did {he} read in all?", 10, [9, 2, 11],
          "6 + 4 = <b>10 pages</b>. Start at 6 and count on 4: 7, 8, 9, 10.", "pages")
    story("{N} has 10 grapes. {He} eats 8. How many grapes are left?", 2, [18, 3, 1],
          "10 %s 8 = ? Think: 8 + 2 = 10. So <b>2 grapes</b> are left." % M, "grapes")
    story("There are 11 kids at the park. 9 kids go home. How many kids are still at the park?", 2, [20, 3, 1],
          "11 %s 9 = ? Think: 9 + 2 = 11. So <b>2 kids</b> are still there." % M, "kids")
    story("{N} has 13 stickers. {He} gives 9 to {M}. How many stickers does {N} have left?", 4, [22, 5, 3],
          "13 %s 9 = ? Think: 9 + 4 = 13. So {N} has <b>4 stickers</b> left." % M, "stickers")
    story("{N} has 7 shells. {He} wants 15 shells. How many more shells does {he} need?", 8, [22, 7, 9],
          "Think: 7 + ? = 15. 7 + 3 = 10, and 5 more is 15. 3 + 5 = 8. {N} needs <b>8 more shells</b>.", "shells")
    story("A tank has 6 fish. The class puts in 9 more fish. How many fish are in the tank now?", 15, [14, 3, 16],
          "6 + 9 = 9 + 6. Start at 9. 9 + 1 = 10, and 5 more is 15. That is <b>15 fish</b>.", "fish")

    nm, he, _ = P.next()
    its.append(mcq("%s has 2 cookies. %s gets 9 more. What is the fastest way to find how many %s has?" % (nm, cap(he), he),
                   "Start at 9, count on 2",
                   ["Start at 2, count on 8", "Start at 9, count back 2", "Start at 11, count on 2"],
                   "2 + 9 = 9 + 2. Start at the bigger number, 9, and count on 2: 10, 11. %s has 11 cookies." % nm))

    story("{N} has 4 red marbles, 7 blue marbles and 6 green marbles. How many marbles does {he} have in all?", 17, [11, 16, 18],
          "Make a ten first: 4 + 6 = 10. Then 10 + 7 = <b>17 marbles</b>.", "marbles")
    story("A pet shop has 5 cats, 3 dogs and 5 rabbits. How many pets is that?", 13, [8, 12, 14],
          "Make a ten first: 5 + 5 = 10. Then 10 + 3 = <b>13 pets</b>.", "pets")

    nm, he, _ = P.next()
    m = P.next()[0]
    its.append(mcq("%s has 4 red beads and 7 blue beads. %s has 7 red beads and 4 blue beads. Who has more beads?" % (nm, m),
                   "Same: 11 each", [nm, m, "Same: 10 each"],
                   "4 + 7 = 11 and 7 + 4 = 11. Turn-around facts have the same sum, so they have <b>the same number</b> of beads."))
    nm, he, _ = P.next()
    m = P.next()[0]
    its.append(mcq("%s makes a cube train with 6 red cubes and 8 blue cubes. %s uses 8 red cubes and 6 blue cubes. "
                   "Who uses more cubes?" % (nm, m),
                   "Same: 14 each", [nm, m, "Same: 15 each"],
                   "6 + 8 = 14 and 8 + 6 = 14. Both trains have <b>14 cubes</b>."))

    its.append(mcq("There are 12 birds. Some fly away. Now 8 birds are left. Which fact helps you find how many flew away?",
                   "8 + ? = 12", ["12 + 8 = ?", "8 %s 12 = ?" % M, "? %s 8 = 12" % M],
                   "8 birds are left. 8 and the birds that flew away make 12: 8 + 4 = 12. So 4 birds flew away."))
    nm, he, _ = P.next()
    its.append(mcq("%s has 9 blocks. %s needs 16 blocks. Which fact finds how many more blocks %s needs?" % (nm, cap(he), he),
                   "9 + ? = 16", ["9 + 16 = ?", "9 %s 16 = ?" % M, "16 + ? = 9"],
                   "%s has 9 and needs 16. 9 + 7 = 16, so %s needs 7 more blocks." % (nm, he)))
    nm, he, _ = P.next()
    its.append(mcq("%s has 15 crayons. %s loses some. Now %s has 9. Which fact finds how many %s lost?" % (nm, cap(he), he, he),
                   "15 %s ? = 9" % M, ["15 + 9 = ?", "9 %s 15 = ?" % M, "15 + ? = 9"],
                   "15 take away some is 9. Think: 9 + 6 = 15. So 15 %s 6 = 9, and %s lost 6 crayons." % (M, he)))

    story("Some ducks are in a pond. 5 more ducks come. Now there are 13 ducks. How many ducks were there at first?",
          8, [18, 9, 7],
          "Think: ? + 5 = 13. 8 + 5 = 13, so there were <b>8 ducks</b> at first. Check: 13 %s 5 = 8." % M, "ducks")
    story("{N} knows 8 + 5 = 13. {He} has 13 plums. {He} gives 5 to friends. How many plums are left?", 8, [18, 7, 9],
          "13 %s 5 is in the same family as 8 + 5 = 13. So 13 %s 5 = <b>8</b>. 8 plums are left." % (M, M), "plums")
    assert len(its) == 20, len(its)
    return {"title": "Word problems: choose a strategy", "items": its}


# ============================================================ lesson
def body_html():
    return (
        "<h2>Use what you know</h2>"
        "<p>You do not have to count every fact from 1. If you know one fact, you know more facts. "
        "These strategies help you add and subtract fast.</p>"
        "<h2>Turn-around facts</h2>"
        "<p>Change the order. The sum stays the same.</p>"
        "<figure class='sn-fig'>" + trains_svg(8, 3) +
        "<figcaption>8 red and 3 green is 11. Turn the train around: 3 green and 8 red is still 11. So 8 + 3 = 3 + 8.</figcaption></figure>"
        "<p>With three numbers, add the two that make 10 first.</p>"
        + ex("Make a ten", "2 + 6 + 4 = ?", "Look for two numbers that make 10: 6 + 4 = 10. Then 2 + 10 = 12.", "12")
        + "<h2>Count on and count back</h2>"
        "<p>To add a small number, start at the bigger number and count on. To take away a small number, count back. "
        "Do not count the number you start on.</p>"
        "<figure class='sn-fig'>" + numline_svg(6, 17, 9, 3) +
        "<figcaption>9 + 3: start at 9. Jump 3 times: 10, 11, 12. So 9 + 3 = 12.</figcaption></figure>"
        + ex("Count back", "12 − 2 = ?", "Start at 12. Count back 2: 11, 10.", "10")
        + "<h2>Fact families</h2>"
        "<p>3 numbers can make 4 facts. They all use the same 3 numbers.</p>"
        "<figure class='sn-fig'>" + triangle_svg(11, 3, 8) +
        "<figcaption>3, 8 and 11: 3 + 8 = 11, 8 + 3 = 11, 11 − 3 = 8, 11 − 8 = 3.</figcaption></figure>"
        "<h2>Subtract: think addition</h2>"
        "<p>To find 13 − 9, ask: 9 + what = 13? Count up from 9: 10, 11, 12, 13. That is 4.</p>"
        "<figure class='sn-fig'>" + bond_svg(13, 9, "?") +
        "<figcaption>The whole is 13. One part is 9. 9 + 4 = 13, so 13 − 9 = 4.</figcaption></figure>"
        + ex("Example", "10 − 8 = ?", "Think: 8 + ? = 10. 8 + 2 = 10.", "2")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["9 + 3: “9, 10, 11”, so 11", "Do not count 9. Say the next 3 numbers: 10, 11, 12"],
            ["12 − 2: “12, 11”, so 11", "Start at 12 and count back 2: 11, 10. So 10"],
            ["Counting on from the small number: 2 + 9", "Start at 9 and count on 2: 10, 11"],
            ["8 − 3 = 5 in the family of 3, 8 and 11", "A family uses only its 3 numbers. 5 is not one of them"],
            ["13 − 9: “9 − 3 = 6”, so 16", "Think addition: 9 + 4 = 13, so 13 − 9 = 4"],
        ])
    )


FAQ = [
    {"q": "What are addition and subtraction strategies in 1st grade?",
     "a": "First graders use turn-around facts (8 + 3 = 3 + 8), making a ten, counting on and counting back, fact families, and thinking addition to subtract. These come from Common Core standards 1.OA.B.3, 1.OA.B.4 and 1.OA.C.5."},
    {"q": "What is a turn-around fact?",
     "a": "A turn-around fact has the same two numbers in a different order, like 8 + 3 and 3 + 8. The sum is the same, so knowing one fact gives you the other one free."},
    {"q": "How do you teach counting on in Grade 1?",
     "a": "Start at the bigger number and say the next numbers, one for each number you add. For 9 + 3, say “10, 11, 12”. Do not count the 9 again."},
    {"q": "How does addition help with subtraction?",
     "a": "Subtraction is finding a missing part. To solve 13 − 9, ask “9 plus what makes 13?” Since 9 + 4 = 13, the answer is 4."},
]


def gen():
    rnd = random.Random(113)
    P = People(rnd)
    sets = [set_turn_around(P), set_count(P), set_families(P), set_think_add(P), set_stories(P)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5)
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"] not in seen, it["q"]
            seen.add(it["q"])
            assert "-" not in re.sub(r"<[^>]+>", "", it["q"] + "".join(it["c"]) + it["e"]).replace("Turn-around", "").replace("turn-around", ""), it
            for c in it["c"]:
                for n in re.findall(r"\d+", c):
                    assert 0 < int(n) <= 120, (it["q"], c)
                if re.match(r"^\d+ [+−] \d+ = \d+$", c):
                    pass
            # equations shown as the right answer are true
            r = it["c"][it["a"]]
            if re.match(r"^\d+ [+−] \d+ = \d+$", r):
                assert is_true(r), r
            # cube counts match the label
            m = re.search(r"aria-label='cube train of (\d+) red and (\d+) green cubes", it["q"])
            if m:
                n = int(m.group(1)) + int(m.group(2))
                k = it["q"].count("<rect")
                assert k in (n, 2 * n), (k, n)
    u = {
        "country": "us", "subject": "math", "grade": "grade-1", "slug": "addition-subtraction-strategies", "sort": 13,
        "updated": UPDATED, "pdf_url": "",
        "title": "Addition and Subtraction Strategies",
        "seo_title": "Grade 1 Addition and Subtraction Strategies Worksheets: Turn-Around Facts, Counting On and Fact Families",
        "short_title": "Addition and subtraction strategies",
        "domain": "Operations and Algebraic Thinking",
        "standard_code": "1.OA.B.3",
        "standard_url": "https://www.thecorestandards.org/Math/Content/1/OA/B/3/",
        "standard_text": "Apply properties of operations as strategies to add and subtract. Examples: If 8 + 3 = 11 is known, then 3 + 8 = 11 is also known. (Commutative property of addition.) To add 2 + 6 + 4, the second two numbers can be added to make a ten, so 2 + 6 + 4 = 2 + 10 = 12. (Associative property of addition.)",
        "meta_desc": "Free Grade 1 addition and subtraction strategies worksheets: turn-around facts, make a ten, count on and count back on a number line, fact families, and subtract by thinking addition. 100 1st grade practice questions with pictures and an answer key.",
        "key_big": "If you know 8 + 3 = 11, you also know 3 + 8 = 11, 11 − 3 = 8 and 11 − 8 = 3.",
        "key_sub": "Count on from the bigger number: 9 + 3 is 10, 11, 12. Make a ten: 2 + 6 + 4 = 2 + 10 = 12. To find 13 − 9, think 9 + ? = 13.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    mark_large(u, "number line")
    mark_large(u, "cube train")
    return u


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
