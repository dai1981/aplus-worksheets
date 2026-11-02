# -*- coding: utf-8 -*-
"""
US Grade 1 Math: The Equal Sign, True or False and Missing Numbers (1.OA.D.7, 1.OA.D.8)
  python tools/gen_us_math_g1_equal_sign.py
Every equation, missing number and dot count is checked in code.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "us", "math", "grade-1")
UPDATED = "2026-11-02"
GREEN = "#006633"
RED = "#c0392b"
BLUE = "#2e6da4"
INK = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"
MINUS = "−"
Q = "<b>?</b>"
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
        self.pool = [(n, "she", "her", "her") for n in GIRLS] + [(n, "he", "his", "him") for n in BOYS]
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
    """Tag wide pictures (number lines) so they print larger."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def ev(expr):
    """Value of '8 − 1', '4 + 1', '6', '4 + ? + 2' (with ? given)."""
    toks = expr.split()
    v = int(toks[0])
    for op, n in zip(toks[1::2], toks[2::2]):
        assert op in ("+", MINUS), expr
        v = v + int(n) if op == "+" else v - int(n)
    return v


def eq_true(eq):
    lhs, rhs = eq.split(" = ")
    return ev(lhs) == ev(rhs)


def show(eq):
    """Equation text with the unknown drawn as a bold ?."""
    return eq.replace("?", Q)


def solve(eq):
    """The one whole number 0-20 that makes eq true (and check it is the only one)."""
    ok = [n for n in range(0, 21) if eq_true(eq.replace("?", str(n)))]
    assert len(ok) == 1, (eq, ok)
    return ok[0]


def count_list(a, b):
    return ", ".join(str(x) for x in range(a + 1, b + 1))


# ------------------------------------------------------------ figures
def balance_svg(left, right, unknown=False, label=None):
    """Pan balance. left/right: lists of (count, color). unknown: draw a ? in the right pan.
    The beam is level when both sides are equal (or the right side is unknown); the heavier side goes down."""
    L = sum(n for n, _ in left)
    R = sum(n for n, _ in right)
    assert L <= 15 and R <= 15
    t = 0 if (unknown or L == R) else (10 if L > R else -10)   # + : left side down
    rows = lambda groups, q: max(1, sum(math.ceil(n / 5) for n, _ in groups)) + (1 if q else 0)
    RM = max(rows(left, False), rows(right, unknown))
    by = 43 + 18 * (RM - 1) + 10
    W, H = 300, by + 46
    s = []
    # stand
    s.append("<polygon points='150,%d 128,%d 172,%d' fill='%s'/>" % (by, by + 34, by + 34, INK))
    s.append("<rect x='105' y='%d' width='90' height='7' rx='2' fill='%s'/>" % (by + 34, INK))
    # beam
    s.append("<line x1='66' y1='%.1f' x2='234' y2='%.1f' stroke='%s' stroke-width='5' stroke-linecap='round'/>"
             % (by + t * 0.8 * 84 / 78, by - t * 0.8 * 84 / 78, INK))
    for cx, ey, groups, q in [(72, by + t * 0.8, left, False), (228, by - t * 0.8, right, unknown)]:
        py = ey - 10
        s.append("<line x1='%d' y1='%.1f' x2='%d' y2='%.1f' stroke='%s' stroke-width='3'/>" % (cx, ey, cx, py, INK))
        s.append("<path d='M %d %.1f L %d %.1f L %d %.1f L %d %.1f Z' fill='#e9eef2' stroke='%s' stroke-width='2.5'/>"
                 % (cx - 52, py - 3, cx + 52, py - 3, cx + 44, py + 3, cx - 44, py + 3, INK))
        r0 = 0                       # each group starts on a new row, so the groups are easy to see
        for n, col in groups:
            for k in range(n):
                r, c = divmod(k, 5)
                s.append("<circle cx='%d' cy='%.1f' r='7' fill='%s'/>" % (cx - 36 + c * 18, py - 13 - 18 * (r0 + r), col))
            r0 += math.ceil(n / 5)
        if q:
            s.append(text(cx, py - 13 - 18 * r0 + 9, "?", 26, col=INK))
    if label is None:
        label = "balance scale with %s on the left and %s on the right" % (
            " and ".join("%d dot%s" % (n, "" if n == 1 else "s") for n, _ in left),
            (" and ".join("%d dot%s" % (n, "" if n == 1 else "s") for n, _ in right) + (" and a question mark" if unknown else "")) if right else "a question mark")
    return svg_wrap(W, H, "".join(s), label)


CELL = 30
FW, FH = 5 * CELL, 2 * CELL     # one ten frame: 150 x 60


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


def ten_frame_svg(n):
    o = 6
    return svg_wrap(FW + 2 * o, FH + 2 * o, frame(o, o, [RED] * n), "ten frame with %d counters" % n)


def two_frames_svg(top, bottom, label, horizontal=False):
    o, gap = 6, 12
    if horizontal:
        W, H = 2 * FW + gap + 2 * o, FH + 2 * o
        body = frame(o, o, top) + frame(o + FW + gap, o, bottom)
    else:
        W, H = FW + 2 * o, 2 * FH + gap + 2 * o
        body = frame(o, o, top) + frame(o, o + FH + gap, bottom)
    return svg_wrap(W, H, body, label)


def number_line_svg(lo, hi, start=None):
    """Plain number line from lo to hi (a tool to count on or back). start: circle one number."""
    L, step, Y = 18, 30, 22
    W = 2 * L + (hi - lo) * step
    X = lambda v: L + (v - lo) * step
    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (L - 10, Y, W - L + 10, Y, INK)]
    for v in range(lo, hi + 1):
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (X(v), Y - 7, X(v), Y + 7, INK))
        s.append(text(X(v), Y + 28, str(v), 15))
    if start is not None:
        s.append("<circle cx='%d' cy='%d' r='6' fill='%s'/>" % (X(start), Y, GREEN))
    return svg_wrap(W, Y + 36, "".join(s), "number line from %d to %d" % (lo, hi))


# ============================================================ set 1: = means "the same as"
def set_same_as(P):
    its = []
    # A. balanced scale: which number sentence matches?
    for a, b in [(3, 2), (4, 4), (6, 1)]:
        s = a + b
        q = (fig(balance_svg([(a, RED), (b, GREEN)], [(s, BLUE)]))
             + "The scale is balanced. Which number sentence matches it?")
        e = ("The left side has %d and %d. That is %d. The right side has %d. Both sides are the same, so "
             "<b>%d + %d = %d</b>." % (a, b, s, s, a, b, s))
        its.append(mcq(q, "%d + %d = %d" % (a, b, s),
                       ["%d + %d = %d" % (a, b, s + 1), "%d + %d = %d" % (a, b, s - 1), "%d = %d" % (a, s)], e))
    for s, a, b in [(7, 5, 2), (9, 6, 3)]:
        q = (fig(balance_svg([(s, BLUE)], [(a, RED), (b, GREEN)]))
             + "The scale is balanced. Which number sentence matches it?")
        e = ("The left side has %d. The right side has %d and %d. %d + %d = %d. "
             "The total can come first: <b>%d = %d + %d</b>." % (s, a, b, a, b, s, s, a, b))
        its.append(mcq(q, "%d = %d + %d" % (s, a, b),
                       ["%d = %d + %d" % (s, a, b + 1), "%d = %d + %d" % (s, a - 1, b), "%d = %d" % (s, a)], e))
    # B. balanced scale with an unknown side
    for a, b in [(5, 4), (6, 6), (3, 8)]:
        s = a + b
        q = (fig(balance_svg([(a, RED), (b, GREEN)], [], unknown=True))
             + "The scale is balanced. How many dots are on the right side?")
        e = "Balanced means both sides are the same. The left side has %d + %d = %d dots. So the right side has <b>%d</b>." % (
            a, b, s, s)
        its.append(mcq(q, s, [s + 1, s - 1, max(a, b)], e))
    # C. scale that is not balanced: how many more on the right?
    for a, b, k in [(4, 3, 5), (6, 2, 3), (5, 5, 6), (7, 4, 8)]:
        s = a + b
        need = s - k
        q = (fig(balance_svg([(a, RED), (b, GREEN)], [(k, BLUE)]))
             + "The scale is not balanced. How many more dots must go on the right side to balance it?")
        e = ("The left side has %d + %d = %d dots. The right side has %d. Count up from %d to %d: %s. "
             "That is <b>%d</b> more. %d + %d = %d." % (a, b, s, k, k, s, count_list(k, s), need, k, need, s))
        its.append(mcq(q, need, [s, need + 1, need - 1], e))
    # D. what does = mean?
    its.append(mcq("What does the = sign mean?", "is the same as",
                   ["the answer is next", "add the numbers", "is more than"],
                   "The = sign means <b>is the same as</b>. 3 + 2 = 5 means 3 + 2 is the same as 5. "
                   "The answer does not always come next."))
    # E. which is the same as n?
    for n, right, wrong in [(8, "5 + 3", ["5 + 4", "8 + 1", "4 + 3"]),
                            (6, "9 − 3", ["9 − 2", "6 − 1", "6 + 3"]),
                            (10, "6 + 4", ["6 + 5", "10 + 4", "5 + 4"]),
                            (7, "10 − 3", ["10 − 2", "7 + 3", "10 − 4"])]:
        assert ev(right) == n and all(ev(w) != n for w in wrong)
        e = "<b>%s</b> = %d. The others are %s." % (right, n, ", ".join(
            "%s = %d" % (w, ev(w)) for w in wrong))
        its.append(mcq("Which is the same as %d?" % n, right, wrong, e))
    # F. which makes it true? (an expression on the right)
    for left, right, wrong in [("4 + 3", "5 + 2", ["4 + 4", "3 + 3", "7 + 2"]),
                               ("6 + 2", "4 + 4", ["4 + 5", "6 + 3", "8 + 2"]),
                               ("5 + 5", "7 + 3", ["7 + 4", "5 + 4", "10 + 5"])]:
        v = ev(left)
        assert ev(right) == v and all(ev(w) != v for w in wrong)
        e = ("%s = %d. The other side must be %d too. <b>%s</b> = %d. "
             "Watch out: %s is not %d. The = sign does not mean “the answer comes next.”"
             % (left, v, v, right, v, wrong[2], v))
        its.append(mcq("Which one makes it true?<br>%s = ___" % left, right, wrong, e))
    assert len(its) == 20, len(its)
    return {"title": "“=” means “the same as”", "items": its}


# ============================================================ set 2: true or false
def tf_item(eq, wrong):
    lhs, rhs = eq.split(" = ")
    a, b = ev(lhs), ev(rhs)
    parts = " ".join("%s is %d." % (x, ev(x)) for x in (lhs, rhs) if x != str(ev(x)))
    if a == b:
        right = "True. Both sides are %d." % a
        e = (parts + " " if parts else "") + "Both sides are %d, so it is <b>true</b>." % a
    else:
        right = "False. %d is not %d." % (a, b)
        e = (parts + " " if parts else "") + "%d and %d are not the same, so it is <b>false</b>." % (a, b)
    return mcq("Is it true or false?<br>%s" % eq, right, wrong, e)


def set_true_false(P):
    its = []
    its.append(tf_item("6 = 6", ["False. There is no + or −.", "False. 6 is not 12.", "True. Both sides are 12."]))
    its.append(tf_item("5 = 4", ["True. Both sides are 5.", "True. 5 is next to 4.", "False. 5 is not 6."]))
    its.append(tf_item("7 = 8 − 1", ["False. The answer goes last.", "False. 8 − 1 is 9.", "True. Both sides are 8."]))
    its.append(tf_item("9 = 5 + 4", ["False. The answer goes last.", "False. 5 + 4 is 10.", "True. Both sides are 10."]))
    its.append(tf_item("3 + 3 = 7", ["True. Both sides are 7.", "True. 3 + 3 is 7.", "False. 6 is not 8."]))
    its.append(tf_item("5 + 2 = 2 + 5", ["False. The order is not the same.", "False. 7 is not 8.", "True. Both sides are 8."]))
    # which is true?
    for right, wrong in [("8 = 10 − 2", ["8 = 10 − 3", "4 + 4 = 9", "10 = 8 − 2"]),
                         ("6 + 1 = 7", ["6 + 1 = 8", "7 = 6 − 1", "1 + 6 = 6"]),
                         ("3 + 6 = 6 + 3", ["3 + 6 = 6 + 4", "3 + 6 = 6", "9 = 3 + 5"]),
                         ("4 + 5 = 9 + 0", ["4 + 5 = 9 + 1", "4 + 5 = 8", "5 = 4 + 5"]),
                         ("10 − 4 = 3 + 3", ["10 − 4 = 3 + 4", "10 − 4 = 4", "6 = 10 − 3"])]:
        assert eq_true(right) and not any(eq_true(w) for w in wrong), right
        e = "Find each side. %s: both sides are %d, so it is <b>true</b>. The other three have sides that are not the same." % (
            right, ev(right.split(" = ")[0]))
        its.append(mcq("Which number sentence is true?", right, wrong, e))
    # which is false?
    for right, wrong in [("5 + 3 = 9", ["5 + 3 = 8", "8 = 5 + 3", "3 + 5 = 8"]),
                         ("4 + 1 = 5 + 2", ["4 + 1 = 2 + 3", "4 + 1 = 5", "4 + 1 = 1 + 4"]),
                         ("7 − 2 = 4", ["7 − 2 = 5", "5 = 7 − 2", "7 − 2 = 2 + 3"]),
                         ("2 + 8 = 8 + 1", ["2 + 8 = 8 + 2", "10 = 2 + 8", "2 + 8 = 5 + 5"])]:
        assert not eq_true(right) and all(eq_true(w) for w in wrong), right
        lhs, rhs = right.split(" = ")
        parts = " ".join("%s is %d." % (x, ev(x)) for x in (lhs, rhs) if x != str(ev(x)))
        e = "%s %d is not %d, so <b>%s</b> is false. The other three are true." % (parts, ev(lhs), ev(rhs), right)
        its.append(mcq("Which number sentence is false?", right, wrong, e))
    # harder true or false
    its.append(tf_item("4 + 1 = 5 + 2", ["True. 4 + 1 is 5.", "True. Both sides are 7.", "False. 5 is not 6."]))
    its.append(tf_item("10 − 3 = 6", ["True. Both sides are 6.", "False. 10 − 3 is 8.", "True. 10 − 3 is 6."]))
    its.append(tf_item("6 + 4 = 5 + 5", ["False. 6 is not 5.", "False. 10 is not 11.", "True. Both sides are 11."]))
    its.append(tf_item("9 − 2 = 3 + 4", ["False. One is − and one is +.", "False. 7 is not 8.", "True. Both sides are 6."]))
    its.append(tf_item("7 + 1 = 7 + 2", ["True. Both have a 7.", "True. Both sides are 8.", "False. 8 is not 10."]))
    assert len(its) == 20, len(its)
    return {"title": "True or false?", "items": its}


# ============================================================ set 3: missing number on the right or in the middle
def add_e(a, b):
    s = a + b
    if a == b:
        return "%d + %d is a double. %d + %d = <b>%d</b>." % (a, b, a, b, s)
    if s > 10 and max(a, b) >= 7:
        big, small = max(a, b), min(a, b)
        need = 10 - big
        return ("Make 10. %d + %d = 10. %d is left from the %d. 10 + %d = <b>%d</b>."
                % (big, need, small - need, small, small - need, s))
    return "Count on from %d: %s. %d + %d = <b>%d</b>." % (max(a, b), count_list(max(a, b), s), a, b, s)


def missing_add_e(a, c):
    """a + ? = c"""
    k = c - a
    if k <= 5:
        return "Count up from %d to %d: %s. That is %d. %d + <b>%d</b> = %d." % (a, c, count_list(a, c), k, a, k, c)
    if a < 10 < c:
        return "From %d to 10 is %d. From 10 to %d is %d. %d + %d = %d. So %d + <b>%d</b> = %d." % (
            a, 10 - a, c, c - 10, 10 - a, c - 10, k, a, k, c)
    return "%d − %d = %d. So %d + <b>%d</b> = %d." % (c, a, k, a, k, c)


def set_right_middle(P):
    its = []
    # A. answer on the right
    for a, b in [(6, 6), (3, 5), (9, 4), (8, 7)]:
        s = a + b
        cands = [s - 1, s + 1, 10 + min(a, b) if s > 10 else s + 2, s - 2]
        its.append(mcq("%d + %d = %s" % (a, b, Q), s, cands, add_e(a, b)))
    for a, b in [(9, 4), (14, 5), (12, 6)]:
        d = a - b
        e = "Think addition: %d + ? = %d. %d + %d = %d, so %d − %d = <b>%d</b>." % (b, a, b, d, a, a, b, d)
        its.append(mcq("%d − %d = %s" % (a, b, Q), d, [a + b, d + 1, d - 1], e))
    # B. a + ? = c with ten frames
    for a, c in [(8, 11), (6, 10), (9, 13)]:
        k = c - a
        eq = "%d + ? = %d" % (a, c)
        assert solve(eq) == k
        if c <= 10:
            pic = ten_frame_svg(a)
        else:
            pic = two_frames_svg([RED] * a, [], "a ten frame with %d counters and an empty ten frame" % a)
        q = fig(pic) + "Count on. What number makes it true?<br>%s" % show(eq)
        its.append(mcq(q, k, [a + c, k + 1, k - 1], missing_add_e(a, c)))
    # C. a + ? = c with a number line, then plain
    for a, c in [(7, 15), (5, 12)]:
        k = c - a
        eq = "%d + ? = %d" % (a, c)
        assert solve(eq) == k
        q = fig(number_line_svg(a - 1, c + 1, start=a)) + "What number makes it true?<br>%s" % show(eq)
        its.append(mcq(q, k, [a + c, k + 1, k - 1], missing_add_e(a, c)))
    for a, c in [(4, 9), (10, 17)]:
        k = c - a
        eq = "%d + ? = %d" % (a, c)
        assert solve(eq) == k
        e = missing_add_e(a, c) if a != 10 else "10 and 7 make 17. So 10 + <b>7</b> = 17."
        its.append(mcq("What number makes it true?<br>%s" % show(eq), k, [a + c, k + 1, k - 1, c], e))
    # D. a − ? = c
    for a, c in [(15, 9), (10, 4), (13, 8), (11, 7), (18, 10)]:
        k = a - c
        eq = "%d − ? = %d" % (a, c)
        assert solve(eq) == k
        if a == 18:
            e = "18 is 10 and 8. Take away the 8 and 10 is left. So 18 − <b>8</b> = 10."
        else:
            e = "Think addition: %d + ? = %d. %d + %d = %d. So %d − <b>%d</b> = %d." % (c, a, c, k, a, a, k, c)
        its.append(mcq("What number makes it true?<br>%s" % show(eq), k, [a + c, k + 1, k - 1, c], e))
    # E. three numbers
    eq = "4 + ? + 2 = 10"
    assert solve(eq) == 4
    its.append(mcq("What number makes it true?<br>%s" % show(eq), 4, [16, 6, 5],
                   "4 + 2 = 6. Now 6 + ? = 10. Count up from 6: 7, 8, 9, 10. That is 4. Check: 4 + <b>4</b> + 2 = 10."))
    assert len(its) == 20, len(its)
    return {"title": "Find the missing number", "items": its}


# ============================================================ set 4: missing number on the left, = first, both sides
def set_left_both(P):
    its = []
    for a, b in [(9, 4), (6, 2), (7, 8)]:
        s = a + b
        eq = "? = %d + %d" % (a, b)
        assert solve(eq) == s
        e = "The = sign can come first. ? is the same as %d + %d. " % (a, b) + add_e(a, b)
        its.append(mcq(show(eq), s, [s - 1, s + 1, abs(a - b)], e))
    for a, b in [(12, 5), (10, 6)]:
        d = a - b
        eq = "? = %d − %d" % (a, b)
        assert solve(eq) == d
        e = "? is the same as %d − %d. Think: %d + %d = %d. So ? = <b>%d</b>." % (a, b, b, d, a, d)
        its.append(mcq(show(eq), d, [a + b, d + 1, d - 1], e))
    for c, a in [(12, 7), (10, 4), (16, 8)]:
        k = c - a
        eq = "%d = %d + ?" % (c, a)
        assert solve(eq) == k
        e = "Read it as %d + ? = %d. " % (a, c) + missing_add_e(a, c)
        if a == 8 and c == 16:
            e = "Read it as 8 + ? = 16. 8 + 8 is a double: 16. So ? = <b>8</b>."
        its.append(mcq("What number makes it true?<br>%s" % show(eq), k, [a + c, k + 1, k - 1], e))
    for c, b in [(5, 3), (6, 4)]:
        k = c + b
        eq = "%d = ? − %d" % (c, b)
        assert solve(eq) == k
        e = ("Start with ?, take away %d, and %d is left. So ? is %d + %d = <b>%d</b>. Check: %d − %d = %d."
             % (b, c, c, b, k, k, b, c))
        its.append(mcq("What number makes it true?<br>%s" % show(eq), k, [c - b, k - 1, k + 1], e))
    eq = "? + 6 = 10"
    assert solve(eq) == 4
    its.append(mcq("What number makes it true?<br>%s" % show(eq), 4, [16, 5, 3],
                   "Count up from 6 to 10: 7, 8, 9, 10. That is 4. <b>4</b> + 6 = 10."))
    eq = "? − 4 = 7"
    assert solve(eq) == 11
    its.append(mcq("What number makes it true?<br>%s" % show(eq), 11, [3, 10, 12],
                   "Start with ?, take away 4, and 7 is left. So ? is 7 + 4 = <b>11</b>. Check: 11 − 4 = 7. "
                   "3 is wrong because 7 − 4 = 3 goes the other way."))
    # both sides
    both = [("3 + 4 = ? + 5", True), ("8 + 2 = ? + 6", False), ("4 + 4 = 2 + ?", False), ("7 + 3 = 2 + ?", True),
            ("9 − 3 = ? + 1", False), ("6 + 3 = 10 − ?", False), ("13 − 3 = 7 + ?", False), ("5 + 5 = ? + 3", False)]
    for eq, pic in both:
        k = solve(eq)
        lhs, rhs = eq.split(" = ")
        v = ev(lhs)
        other = int([t for t in rhs.split() if t not in ("+", MINUS, "?")][0])
        op = "+" if "+" in rhs else MINUS
        q = "What number makes it true?<br>%s" % show(eq)
        if pic:
            la, lb = [int(t) for t in lhs.split(" + ")]
            q = fig(balance_svg([(la, RED), (lb, GREEN)], [(other, BLUE)], unknown=True)) + q
        if op == "+":
            how = "%d + ? = %d. Count up from %d to %d: %s. So ? = <b>%d</b>." % (other, v, other, v, count_list(other, v), k)
            wrong_all = v + other
        else:
            how = "%d − ? = %d. Think: %d + %d = %d. So ? = <b>%d</b>." % (other, v, v, k, other, k)
            wrong_all = v + other
        e = ("First find the left side: %s = %d. The right side must be %d too. %s "
             "It is not %d. The answer does not come right after the = sign." % (lhs, v, v, how, v))
        its.append(mcq(q, k, [v, wrong_all, k + 1, k - 1], e))
    assert len(its) == 20, len(its)
    return {"title": "Missing number on either side", "items": its}


# ============================================================ set 5: word problems with an unknown
def set_stories(P):
    its = []

    def u(n, unit):
        sing = {"children": "child", "kids": "kid", "fish": "fish"}.get(unit, unit[:-1])
        return "%d %s" % (n, sing if n == 1 else unit)

    # (template, kind, numbers, unit)
    # kinds: more (has a, needs c), got (a, gets ?, now c), start (? then + b = c), gave (a, gives ?, c left),
    #        startsub (?, b leave, c left), part (total c, b of one kind), compare (a vs b)
    stories = [
        ("{N} has 7 shells. {He} needs 12 shells. How many more shells does {he} need?", "more", (7, 12), "shells"),
        ("{N} has 9 stickers. {He} gets some more. Now {he} has 13 stickers. How many stickers did {he} get?",
         "more", (9, 13), "stickers"),
        ("Some birds are in a tree. 6 more birds come. Now there are 15 birds. How many birds were in the tree at first?",
         "start", (6, 15), "birds"),
        ("{N} had 16 grapes. {He} ate some. Now {he} has 10 grapes. How many grapes did {he} eat?",
         "gave", (16, 10), "grapes"),
        ("Some kids are at the park. 4 kids go home. Now 8 kids are at the park. How many kids were at the park at first?",
         "startsub", (4, 8), "kids"),
        ("A box holds 10 crayons. There are 7 crayons in it now. How many more crayons fit in the box?",
         "more", (7, 10), "crayons"),
        ("{N} wants to read 17 pages. {He} has read 8 pages. How many more pages does {he} need to read?",
         "more", (8, 17), "pages"),
        ("{N} has 13 toy cars. {He} gives some to {M}. Now {N} has 5 toy cars. How many toy cars did {he} give?",
         "gave", (13, 5), "toy cars"),
        ("There are 10 ducks. Some ducks are in the water. 6 ducks are on the grass. How many ducks are in the water?",
         "part", (10, 6), "ducks"),
        ("{N} has 8 marbles. {M} has 3 marbles. How many more marbles does {N} have than {M}?",
         "compare", (8, 3), "marbles"),
        ("A plate has 6 cookies. Dad puts some more on it. Now there are 14 cookies. How many cookies did Dad put on?",
         "more", (6, 14), "cookies"),
        ("There are 18 children in a class. 9 are boys. The rest are girls. How many girls are there?",
         "part", (18, 9), "girls"),
        ("{N} has some stamps. {M} gives {him} 7 more. Now {N} has 17 stamps. How many stamps did {N} have at first?",
         "start", (7, 17), "stamps"),
        ("{N} needs 20 points to win a game. {He} has 12 points. How many more points does {he} need?",
         "more", (12, 20), "points"),
    ]
    for tpl, kind, (x, y), unit in stories:
        nm, he, his, him = P.next()
        m = P.next()[0] if "{M}" in tpl else ""
        q = tpl.format(N=nm, M=m, he=he, He=cap(he), him=him)
        pic = ""
        if kind == "more":       # x + ? = y
            k = y - x
            e = "%s %d + ? = %d. %s" % ("Think:", x, y, missing_add_e(x, y))
            cands = [x + y, k + 1, k - 1]
            if unit == "crayons":
                pic = fig(ten_frame_svg(7))
                e = "The box holds 10. 7 are in it. Count up from 7 to 10: 8, 9, 10. That is 3. 7 + <b>3</b> = 10."
        elif kind == "start":    # ? + x = y
            k = y - x
            e = "Think: ? + %d = %d. Take away the %d that came: %d − %d = <b>%d</b>. Check: %d + %d = %d." % (
                x, y, x, y, x, k, k, x, y)
            cands = [x + y, k + 1, k - 1]
        elif kind == "gave":     # x − ? = y
            k = x - y
            e = "Think: %d − ? = %d. Count up from %d to %d: %d + %d = %d. So the answer is <b>%d</b>. Check: %d − %d = %d." % (
                x, y, y, x, y, k, x, k, x, k, y)
            cands = [x + y, y, k + 1, k - 1]
        elif kind == "startsub":  # ? − x = y
            k = x + y
            e = "Think: ? − %d = %d. Put back the %d %s who left: %d + %d = <b>%d</b>. Check: %d − %d = %d." % (
                x, y, x, unit, y, x, k, k, x, y)
            cands = [y - x, k + 1, k - 1]
        elif kind == "part":     # x = y + ?
            k = x - y
            e = "Think: %d = %d + ?. %d − %d = <b>%d</b>. Check: %d + %d = %d." % (x, y, x, y, k, y, k, x)
            cands = [x + y, k + 1, k - 1]
        else:                    # compare: y + ? = x
            k = x - y
            e = "Think: %d + ? = %d. Count up from %d: %s. That is <b>%d</b> more." % (y, x, y, count_list(y, x), k)
            cands = [x + y, k + 1, k - 1]
        its.append(mcq(pic + q, u(k, unit), [u(c, unit) for c in cands if c > 0], e))

    # same number on both sides
    nm, he, his, him = P.next()
    m, mhe, mhis, mhim = P.next()
    q = ("%s has 5 red blocks and 3 blue blocks. %s has 6 blocks. How many more blocks does %s need "
         "to have as many as %s?" % (nm, m, m, nm))
    assert solve("5 + 3 = 6 + ?") == 2
    its.append(mcq(q, "2 blocks", ["8 blocks", "14 blocks", "3 blocks"],
                   "%s has 5 + 3 = 8 blocks. Think: 6 + ? = 8. Count up from 6: 7, 8. That is <b>2</b>. "
                   "5 + 3 = 6 + 2." % nm))
    nm, he, his, him = P.next()
    m, mhe, mhis, mhim = P.next()
    q = ("%s has 4 red apples and 4 green apples. %s has 2 red apples and some green apples. "
         "They have the same number of apples. How many green apples does %s have?" % (nm, m, m))
    assert solve("4 + 4 = 2 + ?") == 6
    its.append(mcq(q, "6 green apples", ["8 green apples", "10 green apples", "5 green apples"],
                   "%s has 4 + 4 = 8 apples. %s must have 8 too. Think: 2 + ? = 8. 2 + 6 = 8, so <b>6</b>. "
                   "4 + 4 = 2 + 6." % (nm, m)))

    # which number sentence fits the story?
    fits = [
        ("{N} has 7 shells. {He} needs 12. Which number sentence fits?", "7 + ? = 12",
         ["7 + 12 = ?", "12 + ? = 7", "? − 7 = 12"],
         "{He} has 7 and needs 12 in all. 7 and some more make 12: <b>7 + ? = 12</b>."),
        ("There are 15 frogs. Some hop away. 9 frogs are left. Which number sentence fits?", "15 − ? = 9",
         ["15 + 9 = ?", "9 − ? = 15", "15 + ? = 9"],
         "Start with 15. Some hop away, so take away. 9 are left: <b>15 − ? = 9</b>."),
        ("{N} has some pens. {He} gets 4 more. Now {he} has 11. Which number sentence fits?", "? + 4 = 11",
         ["4 + 11 = ?", "? − 4 = 11", "11 + 4 = ?"],
         "{He} starts with some pens. That is ?. Then 4 more come, and the total is 11: <b>? + 4 = 11</b>."),
        ("{N} has 6 big bears and 2 small bears. {M} has 8 bears. Which number sentence shows they have the same?",
         "6 + 2 = 8", ["6 + 2 = 9", "6 + 8 = 2", "6 = 2 + 8"],
         "{N} has 6 + 2 bears. {M} has 8. The same number goes on each side: <b>6 + 2 = 8</b>."),
    ]
    for tpl, right, wrong, e in fits:
        nm, he, his, him = P.next()
        m = P.next()[0] if "{M}" in tpl else ""
        f = lambda s: s.format(N=nm, M=m, he=he, He=cap(he))
        its.append(mcq(f(tpl), right, wrong, f(e)))
    assert len(its) == 20, len(its)
    return {"title": "Word problems with a missing number", "items": its}


# ============================================================ lesson
def body_html():
    return (
        "<h2>The = sign means “the same as”</h2>"
        "<p>The = sign does not mean “the answer comes next.” It means <b>the same as</b>. "
        "The two sides of = must have the same value. Think of a balance scale. "
        "When both sides are the same, the scale is level.</p>"
        "<figure class='sn-fig'>" + balance_svg([(4, RED), (2, GREEN)], [(6, BLUE)]) +
        "<figcaption>4 + 2 is the same as 6. The scale is balanced, so 4 + 2 = 6. You can also write 6 = 4 + 2.</figcaption></figure>"
        "<h2>True or false?</h2>"
        "<p>Find the value of each side. If both sides are the same, the number sentence is <b>true</b>. "
        "If they are not, it is <b>false</b>.</p>"
        + table(["Number sentence", "Left side", "Right side", "True or false?"], [
            ["6 = 6", "6", "6", "True"],
            ["7 = 8 − 1", "7", "7", "True"],
            ["5 + 2 = 2 + 5", "7", "7", "True"],
            ["4 + 1 = 5 + 2", "5", "7", "False"],
        ]) +
        "<h2>Find the missing number</h2>"
        "<p>A <b>?</b> stands for a number you do not know. Find the number that makes both sides the same.</p>"
        "<figure class='sn-fig'>" + two_frames_svg([RED] * 8 + [GREEN] * 2, [GREEN],
                                                   "8 + 3 = 11 shown on two ten frames", horizontal=True) +
        "<figcaption>8 + ? = 11. Start with 8. Add counters until there are 11. You add 3, so ? = 3.</figcaption></figure>"
        + ex("Example", "15 − ? = 9", "Think addition: 9 + ? = 15. 9 + 6 = 15.", "6")
        + ex("Example", "5 = ? − 3", "Start with ?, take away 3, and 5 is left. So ? is 5 + 3 = 8. Check: 8 − 3 = 5.", "8")
        + "<h2>Numbers on both sides</h2>"
        "<p>Sometimes both sides have a + or a −. Find the side you know first.</p>"
        "<figure class='sn-fig'>" + balance_svg([(3, RED), (4, GREEN)], [(5, BLUE)], unknown=True) +
        "<figcaption>3 + 4 = ? + 5. The left side is 7. The right side has 5, so it needs 2 more. ? = 2.</figcaption></figure>"
        + ex("Example", "3 + 4 = ? + 5", "The left side is 3 + 4 = 7. Now 5 + ? = 7. Count up from 5: 6, 7.", "2")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Writing the answer right after =: 3 + 4 = ? + 5 → 7", "Make both sides the same: 7 = 2 + 5, so ? = 2"],
            ["Adding all the numbers: 8 + ? = 11 → 19", "Ask: 8 and what make 11? Count up from 8: 9, 10, 11. ? = 3"],
            ["Saying 4 + 1 = 5 + 2 is true because 4 + 1 = 5", "Look at the whole right side: 5 + 2 is 7, not 5. It is false"],
            ["Saying 7 = 8 − 1 is false because the answer is first", "The = sign can come first. 7 and 8 − 1 are both 7. It is true"],
            ["Counting the start number: 8 + ? = 11 → 4", "Start at 8 and count the next numbers: 9, 10, 11. That is 3"],
        ])
    )


FAQ = [
    {"q": "What does the equal sign mean in 1st grade math?",
     "a": "The equal sign means “the same as.” Both sides must have the same value, so 7 = 8 − 1 and 5 + 2 = 2 + 5 are true (Common Core 1.OA.D.7)."},
    {"q": "How do you know if a number sentence is true or false?",
     "a": "Find the value of each side. If both sides are the same, it is true; if not, it is false. 4 + 1 = 5 + 2 is false because 5 is not 7."},
    {"q": "How do first graders find a missing number like 8 + ? = 11?",
     "a": "Start at 8 and count up to 11: 9, 10, 11. That is 3 counts, so the missing number is 3. For 15 − ? = 9, think addition: 9 + 6 = 15, so it is 6."},
    {"q": "Why does my child write 7 for 3 + 4 = ? + 5?",
     "a": "Many children think the answer always comes right after the = sign. Show a balance scale: 3 + 4 is 7, so the right side must also be 7, and 2 + 5 = 7, so the missing number is 2."},
]


def gen():
    rnd = random.Random(112)
    P = People(rnd)
    sets = [set_same_as(P), set_true_false(P), set_right_middle(P), set_left_both(P), set_stories(P)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5)
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            k = it["q"] + "|" + "|".join(sorted(it["c"]))
            assert k not in seen, it["q"]
            seen.add(k)
            for c in it["c"]:
                for n in re.findall(r"\d+", c):
                    assert 0 <= int(n) <= 40, (it["q"], c)
            # numeric choices never equal in value
            nums = [c for c in it["c"] if re.fullmatch(r"\d+", c)]
            assert len(set(map(int, nums))) == len(nums)
    # dots drawn on each balance scale match its label
    for s in sets:
        for it in s["items"]:
            m = re.search(r"aria-label='balance scale with ([^']*)'", it["q"])
            if m:
                want = sum(int(n) for n in re.findall(r"(\d+) dots?", m.group(1)))
                assert it["q"].count("<circle") == want, it["q"]
            m = re.search(r"aria-label='(?:a )?ten frame with (\d+) counters", it["q"])
            if m:
                assert it["q"].count("<circle") == int(m.group(1)), it["q"]
    u = {
        "country": "us", "subject": "math", "grade": "grade-1", "slug": "equal-sign-missing-numbers", "sort": 12,
        "updated": UPDATED, "pdf_url": "",
        "title": "The Equal Sign: True or False and Missing Numbers",
        "seo_title": "Grade 1 Equal Sign Worksheets: True or False Equations and Missing Numbers",
        "short_title": "Equal sign and missing numbers",
        "domain": "Operations and Algebraic Thinking",
        "standard_code": "1.OA.D.7",
        "standard_url": "https://www.thecorestandards.org/Math/Content/1/OA/D/7/",
        "standard_text": "Understand the meaning of the equal sign, and determine if equations involving addition and subtraction are true or false. For example, which of the following equations are true and which are false? 6 = 6, 7 = 8 − 1, 5 + 2 = 2 + 5, 4 + 1 = 5 + 2.",
        "meta_desc": "Free Grade 1 equal sign worksheets: learn that = means “the same as” with balance scales, decide if equations are true or false, and find missing numbers like 8 + ? = 11 and 5 = ? − 3. 100 practice questions with an answer key.",
        "key_big": "The = sign means “the same as.” Both sides must have the same value.",
        "key_sub": "7 = 8 − 1 is true because both sides are 7. 4 + 1 = 5 + 2 is false because 5 is not 7. To find a missing number, make both sides the same: 3 + 4 = 2 + 5.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "number line")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
