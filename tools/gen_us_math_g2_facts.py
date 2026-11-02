# -*- coding: utf-8 -*-
"""
US Grade 2 Math: Addition and Subtraction Facts Within 20 (2.OA.B.2)
  python tools/gen_us_math_g2_facts.py
Every sum, difference and counter count is checked in code.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "us", "math", "grade-2")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
RED = "#c0392b"
INK = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"
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


# ------------------------------------------------------------ figures
CELL = 30
FW, FH = 5 * CELL, 2 * CELL     # one ten frame: 150 x 60


def frame(x0, y0, colors):
    """One ten frame at (x0, y0). colors: list of up to 10 fill colors, filled top row first, left to right."""
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


def ten_frame_svg(n):
    o = 6
    return svg_wrap(FW + 2 * o, FH + 2 * o, frame(o, o, [RED] * n), "ten frame with %d counters" % n)


def two_frames_svg(top, bottom, label, horizontal=False):
    """Two ten frames. top/bottom are lists of colors. Stacked (compact for print) or side by side."""
    o, gap = 6, 12
    if horizontal:
        W, H = 2 * FW + gap + 2 * o, FH + 2 * o
        body = frame(o, o, top) + frame(o + FW + gap, o, bottom)
    else:
        W, H = FW + 2 * o, 2 * FH + gap + 2 * o
        body = frame(o, o, top) + frame(o, o + FH + gap, bottom)
    return svg_wrap(W, H, body, label)


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


def count_up_svg(start, end):
    """Number line from start to end with a hop to 10 and a hop to end."""
    L, step, Y = 24, 52, 78
    W = 2 * L + (end - start) * step
    X = lambda v: L + (v - start) * step
    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (L - 10, Y, W - L + 10, Y, INK)]
    for v in range(start, end + 1):
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (X(v), Y - 7, X(v), Y + 7, INK))
        s.append(text(X(v), Y + 28, str(v), 16))
    for a, b in [(start, 10), (10, end)]:
        mid = (X(a) + X(b)) / 2
        s.append("<path d='M %d %d Q %.1f %d %d %d' fill='none' stroke='%s' stroke-width='2.5'/>"
                 % (X(a), Y - 9, mid, Y - 56, X(b), Y - 9, GREEN))
        s.append(text(mid, Y - 38, "+%d" % (b - a), 16, col=GREEN))
    return svg_wrap(W, Y + 36, "".join(s), "number line counting up from %d to %d" % (start, end))


# ------------------------------------------------------------ math words
def add_e(a, b):
    """Short make-10 explanation for a + b > 10."""
    big, small = max(a, b), min(a, b)
    need = 10 - big
    left = small - need
    assert need > 0 and left > 0
    first = "Start with %d. " % big if big != a else ""
    return ("%sTake %d from the %d to make 10: %d + %d = 10. Then add the %d left: 10 + %d = <b>%d</b>."
            % (first, need, small, big, need, left, left, a + b))


def sub_by_add(a, b):
    d = a - b
    return "Think addition: %d + <b>%d</b> = %d. So %d − %d = %d." % (b, d, a, a, b, d)


# ============================================================ set 1: make 10 with ten frames
def set_ten_frames(P):
    its = []
    for n in [6, 9, 7]:
        q = fig(ten_frame_svg(n)) + "How many counters are in the ten frame?"
        e = "The top row is full: that is 5. The bottom row has %d. 5 + %d = <b>%d</b>." % (n - 5, n - 5, n)
        its.append(mcq(q, n, [n - 1, n + 1, 10 - n], e))

    for n in [8, 4, 3, 5, 2, 6]:
        k = 10 - n
        q = fig(ten_frame_svg(n)) + "How many more counters make 10?"
        e = ("A ten frame has 10 boxes. %d boxes have counters, so <b>%d</b> boxes are empty. %d + %d = 10."
             % (n, k, n, k))
        its.append(mcq(q, k, [k + 1, k - 1, n, 10], e))

    for k in [3, 6, 8, 5]:
        q = (fig(two_frames_svg([RED] * 10, [RED] * k, "a full ten frame and a ten frame with %d counters" % k))
             + "How many counters are there in all?")
        e = "A full ten frame is 10. 10 + %d = <b>%d</b>. That is 1 ten and %d ones." % (k, 10 + k, k)
        its.append(mcq(q, 10 + k, [k, 10 + k - 1, 10 + k + 1], e))

    for a in [7, 4, 9, 2]:
        k = 10 - a
        e = "%d and %d make 10. Count up from %d: %s. That is <b>%d</b>." % (
            a, k, a, ", ".join(str(a + i) for i in range(1, k + 1)), k)
        its.append(mcq("%d + <b>?</b> = 10" % a, k, [k + 1, k - 1, a, 10 + a], e))

    for (a, b), qt in zip([(6, 4), (7, 3), (8, 2)],
                          ["Which two numbers make 10?", "Which pair adds up to 10?", "Which pair of numbers makes 10?"]):
        wrong = [(a, b + 1), (a - 1, b), (a + 1, b + 1)]
        assert a + b == 10 and all(x + y != 10 for x, y in wrong)
        e = ("%d + %d = <b>10</b>. The others make %s." %
             (a, b, ", ".join(str(x + y) for x, y in wrong[:2]) + " and " + str(sum(wrong[2]))))
        its.append(mcq(qt, "%d and %d" % (a, b), ["%d and %d" % w for w in wrong], e))
    assert len(its) == 20, len(its)
    return {"title": "Make 10 with ten frames", "items": its}


# ============================================================ set 2: doubles and near doubles
HOOK = {4: "A spider has 8 legs: 4 on each side.",
        5: "Two hands have 10 fingers: 5 and 5.",
        6: "An egg carton has 2 rows of 6 eggs: 12 eggs.",
        7: "Two weeks have 14 days: 7 and 7.",
        8: "8 + 2 = 10, and 6 more is 16.",
        9: "10 + 10 = 20. Take away 2, and you get 18."}


def set_doubles(P):
    its = []
    for n in [4, 5, 6, 7, 8, 9]:
        q = (fig(domino_svg(n, n)) if n <= 6 else "") + "%d + %d = <b>?</b>" % (n, n)
        e = "%d + %d is a double. %d + %d = <b>%d</b>. %s" % (n, n, n, n, 2 * n, HOOK[n])
        its.append(mcq(q, 2 * n, [2 * n - 2, 2 * n + 2, 2 * n + 1], e))

    for a, b in [(6, 7), (5, 6), (9, 8), (4, 5), (7, 8)]:
        lo = min(a, b)
        q = (fig(domino_svg(a, b)) if max(a, b) <= 6 else "") + "Use a double. %d + %d = <b>?</b>" % (a, b)
        e = "%d + %d = %d. %d is 1 more than %d, so add 1 more: %d + 1 = <b>%d</b>." % (
            lo, lo, 2 * lo, max(a, b), lo, 2 * lo, a + b)
        its.append(mcq(q, a + b, [2 * lo, 2 * lo + 2, 2 * lo - 1], e))

    for a, b in [(8, 9), (7, 6), (3, 4), (6, 5)]:
        lo, hi = min(a, b), max(a, b)
        right = "%d + %d + 1" % (lo, lo)
        wrong = ["%d + %d + 2" % (lo, lo), "%d + %d + 1" % (hi, hi), "%d + %d + 1" % (a, b)]
        e = "%d is 1 more than %d. So %d + %d is %d + %d and 1 more: %d + 1 = <b>%d</b>." % (
            hi, lo, a, b, lo, lo, 2 * lo, a + b)
        its.append(mcq("Which way uses a double to find %d + %d?" % (a, b), right, wrong, e))
    nm, he, his = P.next()
    its.append(mcq("%s knows 8 + 8 = 16. How can %s find 8 + 7?" % (nm, he), "16 − 1 = 15",
                   ["16 + 1 = 17", "16 − 2 = 14", "16 + 2 = 18"],
                   "7 is 1 less than 8. So 8 + 7 is 1 less than 8 + 8: 16 − 1 = <b>15</b>."))

    for a in [6, 5, 7, 4]:
        b = a + 2
        e = "%d + %d = %d. %d is 2 more than %d, so add 2: %d + 2 = <b>%d</b>. Or use the middle number: %d + %d = %d." % (
            a, a, 2 * a, b, a, 2 * a, a + b, a + 1, a + 1, a + b)
        its.append(mcq("%d + %d = <b>?</b>" % (a, b), a + b, [2 * a + 1, 2 * a, 2 * b], e))
    assert len(its) == 20, len(its)
    return {"title": "Doubles and near doubles", "items": its}


# ============================================================ set 3: add by making 10
def set_make_ten(P):
    its = []
    for a, b in [(9, 4), (8, 5), (9, 7), (8, 6)]:
        s, need = a + b, 10 - a
        q = (fig(two_frames_svg([RED] * a, [GREEN] * b, "ten frames with %d and %d counters" % (a, b)))
             + "Move counters to fill the top ten frame. What is %d + %d?" % (a, b))
        e = ("Move %d counter%s up. Now the top frame has 10, and %d %s left. 10 + %d = <b>%d</b>."
             % (need, "" if need == 1 else "s", b - need, "is" if b - need == 1 else "are", b - need, s))
        its.append(mcq(q, s, [10 + b, s - 1, s + 1, a], e))

    for a, b in [(7, 5), (9, 6), (8, 4), (7, 6), (6, 5)]:
        need = 10 - a
        k = b - need
        q = "%d + %d = %d + %d + <b>?</b>" % (a, b, a, need)
        e = "Break %d into %d and %d. %d + %d = 10, then add %d: 10 + %d = %d. The missing number is <b>%d</b>." % (
            b, need, k, a, need, k, k, a + b, k)
        its.append(mcq(q, k, [b, need, k + 1, k - 1], e))

    for a, b in [(9, 8), (8, 7), (7, 4), (5, 8)]:
        k = a + b - 10
        q = "%d + %d = 10 + <b>?</b>" % (a, b)
        its.append(mcq(q, k, [min(a, b), k + 1, k - 1, 10 - max(a, b)],
                       add_e(a, b) + " So the missing number is %d." % k))

    for a, b in [(9, 2), (4, 9), (8, 3), (5, 9), (2, 9), (6, 9), (4, 7)]:
        s = a + b
        its.append(mcq("%d + %d = <b>?</b>" % (a, b), s, [10 + min(a, b), s - 1, s + 1, s + 2], add_e(a, b)))
    assert len(its) == 20, len(its)
    return {"title": "Add by making 10", "items": its}


# ============================================================ set 4: subtract within 20
def set_subtract(P):
    its = []
    for a, b in [(13, 8), (15, 9), (12, 7), (16, 8), (14, 6)]:
        d = a - b
        cands = [a + b, d + 1]
        if a % 10 < b:
            cands.append(10 + b - a % 10)   # did 8 − 3 instead of 13 − 8
        cands.append(d - 1)
        q = "%d − %d = <b>?</b><br>Think: %d + ? = %d" % (a, b, b, a)
        its.append(mcq(q, d, cands, sub_by_add(a, b)))

    for a, b in [(12, 3), (11, 2), (15, 3), (17, 2)]:
        d = a - b
        steps = ", ".join(str(a - i) for i in range(1, b + 1))
        e = "Start at %d and count back %d: %s. Do not count %d itself. %d − %d = <b>%d</b>." % (a, b, steps, a, a, b, d)
        its.append(mcq("Count back to find %d − %d." % (a, b), d, [d + 1, a + b, d - 1], e))

    for a, b in [(16, 9), (13, 5), (11, 4)]:
        part = a - 10
        k = b - part
        q = "%d − %d = %d − %d − <b>?</b>" % (a, b, a, part)
        e = ("%d − %d = 10. You must take away %d in all, and %d is done. So take away <b>%d</b> more: 10 − %d = %d."
             % (a, part, b, part, k, k, a - b))
        its.append(mcq(q, k, [b, part, k + 1, k - 1], e))

    fam = [(6, 9, "%d − %d = %d" % (15, 9, 6), ["9 − 6 = 3", "15 + 9 = 24", "16 − 9 = 7"]),
           (7, 5, "%d − %d = %d" % (12, 7, 5), ["7 − 5 = 2", "12 + 5 = 17", "12 − 2 = 10"]),
           (8, 9, "%d + %d = %d" % (9, 8, 17), ["9 − 8 = 1", "17 + 8 = 25", "18 − 9 = 9"])]
    for a, b, right, wrong in fam:
        s = a + b
        for w in wrong + [right]:     # every choice is a true fact
            x, op, y, _, z = w.split()
            assert (int(x) + int(y) if op == "+" else int(x) - int(y)) == int(z), w
        e = ("The family of %d, %d and %d: %d + %d = %d, %d + %d = %d, %d − %d = %d, %d − %d = %d. "
             "Only <b>%s</b> uses all three numbers." % (a, b, s, a, b, s, b, a, s, s, a, b, s, b, a, right))
        its.append(mcq("Which fact is in the same family as %d + %d = %d?" % (a, b, s), right, wrong, e))

    for a, s in [(9, 15), (7, 13), (8, 12), (6, 14)]:
        k = s - a
        e = "Count up from %d to 10, then to %d: %d + %d = 10, 10 + %d = %d. %d + %d = %d, so the missing number is <b>%d</b>." % (
            a, s, a, 10 - a, s - 10, s, 10 - a, s - 10, k, k)
        its.append(mcq("%d + <b>?</b> = %d" % (a, s), k, [a + s, k + 1, k - 1], e))
    its.append(mcq("<b>?</b> − 7 = 8", 15, [1, 14, 16],
                   "Think addition: 7 + 8 = <b>15</b>. Check: 15 − 7 = 8. 1 is wrong because 8 − 7 = 1 goes the other way."))
    assert len(its) == 20, len(its)
    return {"title": "Subtract within 20", "items": its}


# ============================================================ set 5: mixed facts and stories
def set_stories(P):
    its = []
    for op, a, b in [("+", 3, 9), ("-", 17, 9), ("-", 11, 3), ("+", 4, 8), ("-", 14, 7), ("-", 12, 5)]:
        if op == "+":
            s = a + b
            its.append(mcq("%d + %d = <b>?</b>" % (a, b), s, [s - 1, s + 1, 10 + min(a, b), abs(a - b)], add_e(a, b)))
        else:
            d = a - b
            e = sub_by_add(a, b) + (" 7 + 7 = 14 is a double." if (a, b) == (14, 7) else "")
            its.append(mcq("%d − %d = <b>?</b>" % (a, b), d, [a + b, d + 1, d - 1], e))

    # (template, op, a, b, unit) — op: add, sub (take away), more (how many more needed / compare), start
    stories = [
        ("{N} has 8 red beads and 5 blue beads. How many beads does {he} have?", "add", 8, 5, "beads"),
        ("There are 15 birds on a fence. 7 birds fly away. How many birds are left?", "sub", 15, 7, "birds"),
        ("{N} has 9 toy cars. {He} gets 3 more. How many toy cars does {he} have now?", "add", 9, 3, "cars"),
        ("There are 12 apples in a bag. {N} uses 4 for a pie. How many apples are left?", "sub", 12, 4, "apples"),
        ("A tank has 6 fish. The class puts in 7 more fish. How many fish are in the tank now?", "add", 6, 7, "fish"),
        ("{N} has 16 stickers. {He} gives 9 to a friend. How many stickers does {he} have left?", "sub", 16, 9, "stickers"),
        ("{N} read 7 pages on Monday. {He} read 7 pages on Tuesday. How many pages did {he} read in all?", "add", 7, 7, "pages"),
        ("There are 11 kids at the park. 5 kids go home. How many kids are still at the park?", "sub", 11, 5, "kids"),
        ("{N} has 9 crayons. {He} wants 15 crayons. How many more crayons does {he} need?", "more", 15, 9, "crayons"),
        ("{N} has 13 shells. {M} has 6 shells. How many more shells does {N} have than {M}?", "more", 13, 6, "shells"),
        ("There are 14 cookies on a plate. The kids eat some. Now 8 cookies are left. How many cookies did they eat?",
         "sub", 14, 8, "cookies"),
        ("Some ducks are in a pond. 4 more ducks come. Now there are 11 ducks. How many ducks were there at first?",
         "start", 11, 4, "ducks"),
        ("There are 17 children on a bus. 8 children get off. How many children are on the bus now?", "sub", 17, 8, "children"),
        ("{N} picks 6 flowers. {M} picks 8 flowers. How many flowers do they pick in all?", "add", 6, 8, "flowers"),
    ]
    for tpl, op, a, b, unit in stories:
        nm, he, his = P.next()
        m = P.next()[0] if "{M}" in tpl else ""
        q = tpl.format(N=nm, M=m, he=he, He=cap(he))
        u = lambda x: "%d %s" % (x, unit)
        if op == "add":
            s = a + b
            if a == b:
                e = "Put the pages together, so add: %d + %d = <b>%d</b>. It is a double." % (a, b, s)
            else:
                e = "Put the two groups together, so add. " + add_e(a, b)
            its.append(mcq(q, u(s), [u(s - 2), u(s + 1), u(s - 1)] if a == b else [u(s - 1), u(s + 1), u(abs(a - b))], e))
            continue
        d = a - b
        if op == "start":
            e = "Take away the %d %s that came: %d − %d = <b>%d</b>. Check: %d + %d = %d." % (b, unit, a, b, d, d, b, a)
        elif op == "more" and "than" in q:
            e = "Find the difference: %d − %d = <b>%d</b>. Think: %d + %d = %d." % (a, b, d, b, d, a)
        elif op == "more":
            e = "Count up from %d to %d: %d + <b>%d</b> = %d. So %d − %d = %d." % (b, a, b, d, a, a, b, d)
        else:
            e = "Some are gone, so subtract: %d − %d = <b>%d</b>. Think: %d + %d = %d." % (a, b, d, b, d, a)
        its.append(mcq(q, u(d), [u(a + b), u(d + 1), u(d - 1)], e))
    assert len(its) == 20, len(its)
    return {"title": "Mixed facts and word problems", "items": its}


# ============================================================ lesson
def body_html():
    return (
        "<h2>Facts you know by heart</h2>"
        "<p>A fact is a sum of two one-digit numbers, like 8 + 5 = 13, and the subtraction that goes with it. "
        "By the end of Grade 2, you should know them fast, without counting on your fingers. "
        "Three strategies get you there: <b>make 10</b>, <b>doubles</b> and <b>think addition</b>.</p>"
        "<h2>Make 10</h2>"
        "<p>First learn the pairs that make 10: 1 + 9, 2 + 8, 3 + 7, 4 + 6 and 5 + 5. "
        "Then fill up a 10 to add a bigger fact.</p>"
        "<figure class='sn-fig'>" + two_frames_svg([RED] * 8 + [GREEN] * 2, [GREEN] * 3,
                                                   "8 + 5 shown as 10 + 3 on two ten frames", horizontal=True) +
        "<figcaption>8 + 5: move 2 of the 5 to fill the ten frame. Now you have 10 and 3, so 8 + 5 = 13.</figcaption></figure>"
        + ex("Example", "9 + 6 = ?", "9 needs 1 to make 10. Take 1 from the 6, and 5 is left. 10 + 5 = 15.", "15")
        + "<h2>Doubles and near doubles</h2>"
        "<p>A <b>double</b> adds a number to itself: 6 + 6 = 12. A <b>near double</b> is 1 more: "
        "6 + 7 is 6 + 6 and 1 more, so 6 + 7 = 13.</p>"
        "<figure class='sn-fig'>" + dominoes_svg([(5, 5), (5, 6)]) +
        "<figcaption>5 + 5 = 10. The second domino has 1 more dot, so 5 + 6 = 11.</figcaption></figure>"
        + table(["Double", "Near double"], [
            ["5 + 5 = 10", "5 + 6 = 11"],
            ["6 + 6 = 12", "6 + 7 = 13"],
            ["7 + 7 = 14", "7 + 8 = 15"],
            ["8 + 8 = 16", "8 + 9 = 17"],
            ["9 + 9 = 18", "9 + 10 = 19"],
        ]) +
        "<h2>Subtract: think addition</h2>"
        "<p>To find 13 − 8, ask: 8 + what = 13? Count up from 8. Jump to 10, then to 13.</p>"
        "<figure class='sn-fig'>" + count_up_svg(8, 13) +
        "<figcaption>From 8 to 10 is 2. From 10 to 13 is 3. 2 + 3 = 5, so 13 − 8 = 5.</figcaption></figure>"
        + ex("Fact family", "6, 9 and 15", "6 + 9 = 15, 9 + 6 = 15, 15 − 9 = 6, 15 − 6 = 9. If you know one fact, you know all four.",
             "4 facts from 1 family")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Counting the start number: 12 − 3 → “12, 11, 10”, so 10", "Start at 12 and say the next number: 11, 10, 9. 12 − 3 = 9"],
            ["Forgetting to take away when making 10: 9 + 4 → 14", "If 1 goes to the 9, only 3 is left: 10 + 3 = 13"],
            ["Adding when the story says take away", "Words like “fly away”, “are left” and “give” mean subtract"],
            ["Getting a double wrong by 2: 7 + 7 = 12", "Remember a picture: two weeks have 14 days, so 7 + 7 = 14"],
            ["Using the wrong double: 6 + 7 → 7 + 7 + 1", "Double the smaller number and add 1: 6 + 6 + 1 = 13"],
        ])
    )


FAQ = [
    {"q": "What math facts should a 2nd grader know by heart?",
     "a": "By the end of Grade 2, children should know all sums of two one-digit numbers from memory, like 8 + 7 = 15 (Common Core 2.OA.B.2). They should also add and subtract within 20 quickly, using strategies such as making 10."},
    {"q": "What is the make a 10 strategy?",
     "a": "Break one number apart to fill a 10 first. For 8 + 5, take 2 from the 5 so 8 + 2 = 10, then add the 3 that is left: 10 + 3 = 13."},
    {"q": "What are doubles and near doubles in math?",
     "a": "Doubles are facts that add a number to itself, like 6 + 6 = 12. Near doubles are one more, like 6 + 7: use the double and add 1, so 6 + 7 = 13."},
    {"q": "How can my child learn math facts without counting on fingers?",
     "a": "Teach one strategy at a time (make 10, doubles, think addition) and practice a few facts for about 5 minutes every day. Saying the whole fact out loud, like “9 + 6 = 15”, helps it move into memory."},
]


def gen():
    rnd = random.Random(201)
    P = People(rnd)
    sets = [set_ten_frames(P), set_doubles(P), set_make_ten(P), set_subtract(P), set_stories(P)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5)
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            k = it["q"]
            assert k not in seen, it["q"]
            seen.add(k)
            # every number in a choice stays within 0-30 and positive
            for c in it["c"]:
                for n in re.findall(r"\d+", c):
                    assert 0 < int(n) <= 30, (it["q"], c)
    # counters drawn in each ten-frame question match the numbers in the text
    for s in sets:
        for it in s["items"]:
            m = re.search(r"aria-label='ten frame with (\d+) counters'", it["q"])
            if m:
                assert it["q"].count("<circle") == int(m.group(1))
    return {
        "country": "us", "subject": "math", "grade": "grade-2", "slug": "addition-subtraction-facts", "sort": 1,
        "updated": UPDATED, "pdf_url": "",
        "title": "Addition and Subtraction Facts Within 20",
        "seo_title": "Grade 2 Addition and Subtraction Facts Worksheets: Make 10, Doubles and Facts Within 20",
        "short_title": "Addition and subtraction facts",
        "domain": "Operations and Algebraic Thinking",
        "standard_code": "2.OA.B.2",
        "standard_url": "https://www.thecorestandards.org/Math/Content/2/OA/B/2/",
        "standard_text": "Fluently add and subtract within 20 using mental strategies. By end of Grade 2, know from memory all sums of two one-digit numbers.",
        "meta_desc": "Free Grade 2 math facts worksheets: make 10 with ten frames, doubles and near doubles, add by making 10, subtract by thinking addition, and simple word problems. 100 practice questions with step-by-step answers.",
        "key_big": "Make 10, use doubles, and think addition to subtract.",
        "key_sub": "8 + 5 = 8 + 2 + 3 = 13. 6 + 7 is 6 + 6 + 1 = 13. 13 − 8 = 5 because 8 + 5 = 13. Learn the strategy first, then practice until the facts come from memory.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
