# -*- coding: utf-8 -*-
"""
Canada (Ontario) Grade 3 Math: Equations and Equivalence
(Ontario Curriculum, Grades 1–8: Mathematics, 2020 — Algebra C2.1, C2.2, C2.3)
  python3 tools/gen_ca_math_g3_equations.py
The equal sign as “the same as” (pan balances), missing numbers (□ + 25 = 60, 80 − □ = 35),
making both sides equal (40 + 15 = 50 + □), letters for unknowns (n + 6 = 14) and word problems
written as equations. Numbers to 1000.
Wrong choices come from real mistakes: reading = as “the answer is” (40 + 15 = 50 + □ -> 55),
adding when the inverse is needed (□ + 25 = 60 -> 85), subtracting the smaller digit from the
larger in each column (80 − 35 -> 55), forgetting to carry, changing the other number the wrong way
on a balance (40 + 15 = 50 + □ -> 25) and adding every number in the equation.
Every answer is checked in code. HTML attributes use single quotes. Canadian English.
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-3")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
GREY = "#e4e4e4"
INK = "#2b2b2b"
RED = "#c0392b"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Olivia", "Emma", "Maya", "Zoe", "Amira", "Mei", "Chloe", "Priya", "Leah", "Hana", "Ava", "Sofia"]
BOYS = ["Liam", "Noah", "Aiden", "Lucas", "Owen", "Arjun", "Ethan", "Jayden", "Benjamin", "Mateo", "Nathan", "Kai"]
BOX = "□"
NB = " "
LETTERS = "abcdefghijklmnopqrstuvwxyz"


# ------------------------------------------------------------ numbers and equations
def n(x):
    """Ontario style: 4 digits no separator, 5 or more digits grouped with a no-break space."""
    s = str(x)
    if abs(x) < 10000:
        return s
    out = ""
    while len(s) > 3:
        out = NB + s[-3:] + out
        s = s[:-3]
    return s + out


def tok(p):
    if isinstance(p, int):
        return n(p)
    if p == "?":
        return BOX
    return p


def plain(*parts):
    """Plain text equation (for choices and SVG): '?' becomes □, letters stay plain."""
    return " ".join(tok(p) for p in parts)


def html(*parts):
    """Equation for question text: □ in bold, a single letter in italics."""
    out = []
    for p in parts:
        t = tok(p)
        if t == BOX:
            t = "<b>" + BOX + "</b>"
        elif len(t) == 1 and t in LETTERS:
            t = "<i>" + t + "</i>"
        out.append(t)
    return " ".join(out)


def val(expr):
    return eval(expr.replace("−", "-").replace(NB, ""), {"__builtins__": {}})


def holds(eq, ans=None):
    """'□ + 25 = 60' or 'n + 6 = 14' is true with the unknown = ans."""
    s = re.sub(r"<[^>]+>", "", eq)
    if ans is not None:
        s = s.replace(BOX, str(ans))
        s = re.sub(r"\b[a-z]\b", str(ans), s)
    vals = [val(p.strip()) for p in s.split("=")]
    return all(v == vals[0] for v in vals)


def sfl(a, b):
    """Smaller digit from larger digit in each column: 80 − 35 -> 55 (a typical mistake)."""
    da, db = str(a), str(b).rjust(len(str(a)), "0")
    return int("".join(str(abs(int(x) - int(y))) for x, y in zip(da, db)))


def nocarry(a, b):
    """Add column by column and drop every carried ten: 28 + 15 -> 33."""
    out, p = 0, 1
    while a or b:
        out += ((a % 10 + b % 10) % 10) * p
        a, b, p = a // 10, b // 10, p * 10
    return out


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e):
    """4 choices: correct + the first 3 unique distractors. Positions are set later by balance()."""
    correct = n(correct) if isinstance(correct, int) else str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        if isinstance(c, int):
            if c <= 0:
                continue
            c = n(c)
        c = str(c)
        if c in seen or not c or c.startswith("-") or c.startswith("−") or c.startswith("0") or c in ("$0",):
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
        self.pool = [(x, "she", "her") for x in GIRLS] + [(x, "he", "his") for x in BOYS]
        rnd.shuffle(self.pool)
        self.i = 0

    def next(self):
        p = self.pool[self.i % len(self.pool)]
        self.i += 1
        return p


def cap(s):
    return s[0].upper() + s[1:]


# ------------------------------------------------------------ pictures
def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    w, h = int(round(w)), int(round(h))
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


FS = 18
GAP = 7
BOXW = 22


def tok_w(t):
    return BOXW if t == BOX else len(t) * FS * 0.6


def expr_w(s):
    ts = s.split(" ")
    return sum(tok_w(t) for t in ts) + GAP * (len(ts) - 1)


def draw_expr(cx, base, s):
    """Draw 'a + □' centred at cx: each token placed on its own, □ drawn as a red box,
    a single letter in red italics."""
    ts = s.split(" ")
    x = cx - expr_w(s) / 2
    out = []
    for t in ts:
        w = tok_w(t)
        if t == BOX:
            out.append("<rect x='%.1f' y='%.1f' width='%d' height='%d' fill='#fff' stroke='%s' stroke-width='2.5'/>"
                       % (x, base - 16, BOXW, BOXW, RED))
        elif len(t) == 1 and t in LETTERS:
            out.append("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' font-style='italic' fill='%s' "
                       "text-anchor='middle'>%s</text>" % (x + w / 2, base, FS, RED, t))
        else:
            out.append("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                       % (x + w / 2, base, FS, INK, t))
        x += w + GAP
    return "".join(out)


def pan_svg(left, right):
    """A level pan balance with an expression on each pan (plain text, □ or a letter allowed)."""
    def box_w(t):
        return max(90, int(expr_w(t) + 24))
    wl, wr = box_w(left), box_w(right)
    cl = 8 + wl / 2
    cr = cl + wl / 2 + 40 + wr / 2
    mid = (cl + cr) / 2
    top, ih = 8, 36
    py = top + ih
    s = []
    for t, c, w in ((left, cl, wl), (right, cr, wr)):
        s.append("<rect x='%.1f' y='%d' width='%d' height='%d' rx='6' fill='%s' stroke='%s' stroke-width='2'/>"
                 % (c - w / 2, top, w, ih, GREY, INK))
        s.append(draw_expr(c, top + 25, t))
        s.append("<rect x='%.1f' y='%d' width='%d' height='6' fill='%s'/>" % (c - w / 2, py, w, INK))
        s.append("<rect x='%.1f' y='%d' width='4' height='18' fill='%s'/>" % (c - 2, py + 6, INK))
    by = py + 24
    s.append("<rect x='%.1f' y='%d' width='%.1f' height='6' fill='%s'/>" % (cl - 2, by, cr - cl + 4, INK))
    s.append("<path d='M%.1f %d L%.1f %d L%.1f %d Z' fill='%s'/>" % (mid, by + 6, mid - 22, by + 40, mid + 22, by + 40, GREEN))
    s.append("<rect x='%.1f' y='%d' width='80' height='5' fill='%s'/>" % (mid - 40, by + 40, INK))
    return svg_wrap(cr + wr / 2 + 8, by + 47, "".join(s),
                    "pan balance: %s on the left and %s on the right" % (left.replace(BOX, "box"), right.replace(BOX, "box")))


def bar_svg(whole, p1, p2):
    """Part-part-whole bar model, drawn to scale. Values are numbers, '?' (box) or a letter."""
    vals = [whole, p1, p2]
    nums = [v if isinstance(v, int) else None for v in vals]
    miss = [i for i, v in enumerate(nums) if v is None]
    assert len(miss) == 1
    full = list(nums)
    m = miss[0]
    full[m] = (nums[1] + nums[2]) if m == 0 else (nums[0] - (nums[2] if m == 1 else nums[1]))
    assert full[1] + full[2] == full[0] and min(full) > 0
    W, x0, h = 280, 8, 36
    w1 = round(W * full[1] / full[0])
    w1 = min(max(w1, 70), W - 70)
    s = []
    rows = [(8, [(x0, W, whole, FILL)]), (8 + h + 10, [(x0, w1, p1, "#fff"), (x0 + w1, W - w1, p2, "#fff")])]
    for y, cells in rows:
        for x, w, v, f in cells:
            s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='2.5'/>"
                     % (x, y, w, h, f, GREEN))
            s.append(draw_expr(x + w / 2, y + 25, tok(v)))
    lab = "bar model: whole %s, parts %s and %s" % tuple("box" if v == "?" else tok(v) for v in vals)
    return svg_wrap(W + 16, 8 + 2 * h + 10 + 8, "".join(s), lab)


def mark_large(u, pattern):
    rx = re.compile(r"<svg (?=[^>]*aria-label='(?:" + pattern + "))")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


# ------------------------------------------------------------ distractor lists
def sub_cands(big, small, ans):
    """Answer is big − small. Mistakes: adding instead, smaller-from-larger, regrouping slips."""
    return [big + small, sfl(big, small), ans + 10, ans - 10, ans + 1, ans - 1, ans + 100]


def add_cands(a, b, ans):
    """Answer is a + b. Mistakes: subtracting instead, forgetting to carry, carry slips."""
    return [abs(a - b), nocarry(a, b), ans - 10, ans + 10, ans + 1, ans - 1]


WHAT = "<br>What number goes in the box?"


# ============================================================ set 1: = means "the same as"
def set_same_as(P):
    its = []
    # A. which equation matches the balance
    for l, r, right, wrongs in [
        ("7 + 5", "12", "7 + 5 = 12", ["7 + 5 = 13", "7 = 5 + 12", "12 + 5 = 7"]),
        ("15", "9 + 6", "15 = 9 + 6", ["15 = 9 + 7", "15 + 9 = 6", "9 = 15 + 6"]),
        ("8 + 6", "10 + 4", "8 + 6 = 10 + 4", ["8 + 6 = 14 + 4", "8 + 6 = 10 + 6", "8 + 4 = 10 + 6"]),
        ("20 − 5", "10 + 5", "20 − 5 = 10 + 5", ["20 − 5 = 10 − 5", "20 + 5 = 10 + 5", "20 − 5 = 15 + 5"]),
    ]:
        assert holds(right) and not any(holds(w) for w in wrongs)
        e = ("The pans balance, so both sides have the same value. The left pan has %s and the right pan has %s, "
             "so <b>%s</b>. The = sign can sit between any two things that are the same." % (l, r, right))
        if " " in l and " " in r:
            e = ("The pans balance. %s = %d and %s = %d, so <b>%s</b>. The = sign means “is the same as”."
                 % (l, val(l), r, val(r), right))
        its.append(mcq("The pans balance. Which equation matches?" + fig(pan_svg(l, r)), right, wrongs, e))
    # B. balance with a box
    for l, r, ans, wr, e in [
        ("9 + 6", BOX, 15, [3, 14, 16], "The pans balance, so the box has the same value as 9 + 6. 9 + 6 = <b>15</b>. "
         "Not 3: that subtracts."),
        (BOX, "20 − 8", 12, [28, 13, 11], "The box must be the same as 20 − 8. 20 − 8 = <b>12</b>. "
         "Not 28: that adds instead of subtracting."),
        ("30 + 40", BOX, 70, [10, 7, 80], "30 + 40 is 3 tens + 4 tens = 7 tens = <b>70</b>. Not 7: 7 tens is 70. "
         "Not 10: that subtracts."),
        (BOX, "50 − 15", 35, [65, 45, 25], "50 − 15 = <b>35</b>. Not 45: that takes 0 from 5 instead of regrouping. "
         "Not 65: that adds."),
    ]:
        assert val((l if l != BOX else r)) == ans
        its.append(mcq("The pans balance." + WHAT + fig(pan_svg(l, r)), ans, wr, e))
    # C. which equation is true
    prompts = iter(["Which equation is true?", "Which equation is true? The total can come first.",
                    "Work out both sides. Which equation is true?", "Which equation is true? Check both sides."])
    for right, wrongs, e in [
        ("9 + 3 = 8 + 4", ["9 + 3 = 12 + 4", "9 + 3 = 8 + 3", "9 + 3 = 10 + 3"],
         "Work out both sides. 9 + 3 = 12 and 8 + 4 = 12, so <b>9 + 3 = 8 + 4</b> is true. "
         "9 + 3 = 12 + 4 is false: 12 + 4 is 16."),
        ("14 = 7 + 7", ["14 = 7 + 8", "7 = 14 + 7", "14 = 6 + 7"],
         "7 + 7 = 14, so <b>14 = 7 + 7</b> is true. The total can come first, before the = sign."),
        ("16 − 6 = 5 + 5", ["16 − 6 = 10 + 5", "16 − 6 = 22", "16 + 6 = 5 + 5"],
         "16 − 6 = 10 and 5 + 5 = 10, so <b>16 − 6 = 5 + 5</b> is true. Both sides are 10."),
        ("25 + 10 = 30 + 5", ["25 + 10 = 35 + 5", "25 + 10 = 30 + 10", "25 + 10 = 20 + 5"],
         "25 + 10 = 35 and 30 + 5 = 35, so <b>25 + 10 = 30 + 5</b> is true. "
         "25 + 10 = 35 + 5 is false: 35 + 5 is 40, not 35."),
    ]:
        assert holds(right) and not any(holds(w) for w in wrongs)
        its.append(mcq(next(prompts), right, wrongs, e))
    # D. which expression has the same value
    for ex_, right, wrongs in [
        ("7 + 8", "10 + 5", ["10 + 8", "7 + 9", "15 + 8"]),
        ("12 + 9", "11 + 10", ["12 + 10", "13 + 10", "21 + 9"]),
        ("20 − 6", "10 + 4", ["20 + 6", "10 + 6", "26 − 6"]),
        ("40 + 25", "50 + 15", ["50 + 25", "65 + 25", "40 + 15"]),
    ]:
        v = val(ex_)
        assert val(right) == v and all(val(w) != v for w in wrongs)
        e = "%s = %d and %s = %d. They have the same value, so <b>%s = %s</b>." % (ex_, v, right, v, ex_, right)
        its.append(mcq("Which has the same value as %s?" % ex_, right, wrongs, e))
    # E. = sign first
    its.append(mcq(html("?", "=", 8, "+", 7) + WHAT, 15, [1, 14, 16],
                   "The = sign can come first. The box is the same as 8 + 7, so it is <b>15</b>. Not 1: that subtracts."))
    its.append(mcq(html("?", "=", 30, "−", 12) + WHAT, 18, [42, 22, 28],
                   "The box is the same as 30 − 12. 30 − 12 = <b>18</b>. Not 42: that adds. "
                   "Not 22: that takes 0 from 2 instead of regrouping."))
    # F. meaning and a mistake
    its.append(mcq("What does the = sign mean in 6 + 4 = 7 + 3?", "Both sides are the same",
                   ["The answer comes next", "Add all the numbers", "The left side is bigger"],
                   "= means “is the same as”. 6 + 4 = 10 and 7 + 3 = 10, so <b>both sides are the same</b>. "
                   "It does not just mean “the answer comes next”."))
    nm, he, his = P.next()
    its.append(mcq("%s adds 9 and 6, then adds 5. %s writes 9 + 6 = 15 + 5 = 20. What is wrong?" % (nm, cap(he)),
                   "9 + 6 is not the same as 15 + 5",
                   ["9 + 6 is not 15", "15 + 5 is not 20", "Nothing is wrong"],
                   "= means both sides are the same. 9 + 6 = 15, but 15 + 5 = 20, so “9 + 6 = 15 + 5” is <b>not true</b>. "
                   "%s should write two equations: 9 + 6 = 15 and 15 + 5 = 20." % nm))
    assert len(its) == 20
    return {"title": "The equal sign means “the same as”", "items": its}


# ============================================================ set 2: missing numbers
def set_missing():
    its = []

    def add(parts, ans, cands, e, bar=None):
        eq = plain(*parts)
        assert holds(eq, ans), eq
        q = html(*parts) + WHAT + (fig(bar_svg(*bar)) if bar else "")
        its.append(mcq(q, ans, cands, e))

    # □ + a = s
    for a, s, bar in [(25, 60, False), (18, 50, False), (46, 90, True), (150, 400, False), (275, 600, False)]:
        ans = s - a
        e = ("Use the inverse. Subtraction undoes addition: □ = %s = <b>%s</b>. Check: %s. "
             "Not %s: that adds instead of subtracting." % (plain(s, "−", a), n(ans), plain(ans, "+", a, "=", s), n(s + a)))
        add(["?", "+", a, "=", s], ans, sub_cands(s, a, ans), e, (s, "?", a) if bar else None)
    # a + □ = s
    for a, s, bar in [(37, 80, False), (28, 65, True), (19, 47, False), (240, 500, False), (365, 800, False)]:
        ans = s - a
        e = ("Think: %s plus what makes %s? Use the inverse: □ = %s = <b>%s</b>. Check: %s. "
             "Not %s: that adds instead of subtracting." % (n(a), n(s), plain(s, "−", a), n(ans),
                                                           plain(a, "+", ans, "=", s), n(s + a)))
        add([a, "+", "?", "=", s], ans, sub_cands(s, a, ans), e, (s, a, "?") if bar else None)
    # a − □ = r
    for a, r, bar in [(80, 35, True), (64, 28, False), (52, 17, False), (300, 120, False), (705, 480, False)]:
        ans = a - r
        e = ("%s take away what leaves %s? □ = %s = <b>%s</b>. Check: %s. Not %s: that adds the two numbers."
             % (n(a), n(r), plain(a, "−", r), n(ans), plain(a, "−", ans, "=", r), n(a + r)))
        if sfl(a, r) != ans:
            e += " Not %s: that takes the smaller digit from the larger in each column." % n(sfl(a, r))
        add([a, "−", "?", "=", r], ans, sub_cands(a, r, ans), e, (a, r, "?") if bar else None)
    # □ − a = r
    for a, r, bar in [(15, 40, False), (26, 57, True), (120, 380, False)]:
        ans = r + a
        e = ("The box is the number you start with. Undo − %s by adding: □ = %s = <b>%s</b>. Check: %s. "
             "Not %s: that subtracts instead of adding." % (n(a), plain(r, "+", a), n(ans), plain(ans, "−", a, "=", r), n(r - a)))
        add(["?", "−", a, "=", r], ans, add_cands(r, a, ans), e, ("?", r, a) if bar else None)
    # = sign first
    add([70, "=", "?", "+", 45], 25, sub_cands(70, 45, 25),
        "The = sign can come first. □ + 45 = 70, so □ = 70 − 45 = <b>25</b>. Check: 25 + 45 = 70. "
        "Not 115: that adds. Not 35: that takes the smaller digit from the larger.")
    add([50, "=", 92, "−", "?"], 42, sub_cands(92, 50, 42),
        "92 − □ = 50, so □ = 92 − 50 = <b>42</b>. Check: 92 − 42 = 50. Not 142: that adds the two numbers.")
    assert sfl(70, 45) == 35
    assert len(its) == 20
    return {"title": "Find the missing number", "items": its}


# ============================================================ set 3: make both sides equal
def set_equal_sides():
    its = []

    def add(parts, ans, cands, e, pic=None):
        eq = plain(*parts)
        assert holds(eq, ans), eq
        if pic:
            l, r = eq.split(" = ")
            q = "The pans balance: " + html(*parts) + "." + WHAT + fig(pan_svg(l, r))
        else:
            q = html(*parts) + WHAT
        its.append(mcq(q, ans, cands, e))

    # a + b = c + □
    for a, b, c, pic in [(40, 15, 50, True), (26, 8, 30, True), (35, 27, 40, False), (48, 16, 50, True),
                         (120, 60, 100, False), (64, 19, 60, False), (200, 150, 250, True), (300, 125, 400, False)]:
        S = a + b
        ans = S - c
        d = a - c
        wrong_way = b - d
        how = ("%s is %d %s than %s, so □ must be %d %s than %s" %
               (n(c), abs(d), "less" if d > 0 else "more", n(a), abs(d), "more" if d > 0 else "less", n(b)))
        e = ("Both sides must have the same value. The left side is %s. So %s and □ = <b>%s</b>. Or: %s. "
             "Not %s: that is the value of the left side, not the missing number." % (
                 plain(a, "+", b, "=", S), plain(c, "+", "?", "=", S), n(ans), how, n(S)))
        if wrong_way > 0:
            e += " Not %s: that changes %s the wrong way." % (n(wrong_way), n(b))
        add([a, "+", b, "=", c, "+", "?"], ans, [S, wrong_way, S + c], e, pic)
    # □ + c = a + b
    for a, b, c in [(18, 25, 20), (34, 25, 29)]:
        S = a + b
        ans = S - c
        e = ("Work out the side you know: %s. So %s, and □ = %s = <b>%s</b>. "
             "Not %s: that is the value of the right side." % (plain(a, "+", b, "=", S), plain("?", "+", c, "=", S),
                                                                plain(S, "−", c), n(ans), n(S)))
        wrong = b + (c - a)
        e += " Not %s: %s is %s than %s, so □ must be %s than %s, not %s." % (
            n(wrong), n(c), "more" if c > a else "less", n(a), "less" if c > a else "more", n(b), "more" if c > a else "less")
        add(["?", "+", c, "=", a, "+", b], ans, [S, wrong, S + c], e)
    # a − b = c − □
    for a, b, c, pic in [(45, 15, 50, True), (70, 25, 72, False), (90, 38, 100, False), (500, 100, 450, False)]:
        D = a - b
        ans = c - D
        wrong_way = b - (c - a)
        e = ("Work out the side you know: %s. So %s, and □ = %s = <b>%s</b>. Not %s: that is the value of the left side."
             % (plain(a, "−", b, "=", D), plain(c, "−", "?", "=", D), plain(c, "−", D), n(ans), n(D)))
        add([a, "−", b, "=", c, "−", "?"], ans, [D, wrong_way, c + D, ans + 10], e, pic)
    # mixed
    add([30, "+", 20, "=", 60, "−", "?"], 10, [50, 110, 40],
        "30 + 20 = 50. So 60 − □ = 50, and □ = 60 − 50 = <b>10</b>. Not 50: that is the value of the left side.")
    add([80, "−", 30, "=", 20, "+", "?"], 30, [50, 70, 10],
        "80 − 30 = 50. So 20 + □ = 50, and □ = 50 − 20 = <b>30</b>. Not 50: that is the value of the left side.")
    # what must be added / subtracted (C2.2)
    for parts, ans, wr, e in [
        ([45, "+", 20, "+", "?", "=", 50, "+", 30], 15, [5, 80, 10],
         "The right side is 50 + 30 = 80. The left side has 45 + 20 = 65. 80 − 65 = <b>15</b>, so add 15. "
         "Not 80: that is the right side. Not 5: that only compares 45 and 50."),
        ([36, "+", 14, "+", "?", "=", 40, "+", 25], 15, [65, 4, 11],
         "The right side is 40 + 25 = 65. The left side has 36 + 14 = 50. 65 − 50 = <b>15</b>, so add 15. "
         "Not 65: that is the right side. Not 4: that only compares 36 and 40."),
        ([60, "+", 25, "−", "?", "=", 70], 15, [85, 10, 155],
         "60 + 25 = 85. To get from 85 down to 70, subtract 85 − 70 = <b>15</b>. "
         "Not 85: that is the left side. Not 10: that only compares 60 and 70."),
        ([90, "−", 30, "−", "?", "=", 50], 10, [60, 40, 20],
         "90 − 30 = 60. To get from 60 down to 50, subtract 60 − 50 = <b>10</b>. "
         "Not 60: that is 90 − 30. Not 40: that is 90 − 50 and forgets the − 30."),
    ]:
        eq = plain(*parts)
        assert holds(eq, ans), eq
        what = "added to" if "+ " + BOX in eq else "subtracted from"
        left = eq.split(" = ")[0].rsplit(" ", 2)[0]
        q = ("What number must be %s %s to make both sides equal?<br>%s" % (what, left, html(*parts)))
        its.append(mcq(q, ans, wr, e))
    assert len(its) == 20
    return {"title": "Make both sides equal", "items": its}


# ============================================================ set 4: letters for unknowns
def set_letters(P):
    its = []

    def solve(parts, ans, cands, e, pic=False):
        eq = plain(*parts)
        assert holds(eq, ans), eq
        L = [p for p in parts if isinstance(p, str) and len(p) == 1 and p in LETTERS][0]
        q = html(*parts) + ". What is <i>%s</i>?" % L
        if pic:
            l, r = eq.split(" = ")
            q = "The pans balance: " + q + fig(pan_svg(l, r))
        its.append(mcq(q, ans, cands, e))

    for parts, ans, kind in [
        (["n", "+", 6, "=", 14], 8, "add"), (["k", "+", 9, "=", 21], 12, "add"), ([25, "+", "m", "=", 60], 35, "add"),
        (["y", "+", 38, "=", 75], 37, "add"), (["p", "+", 250, "=", 600], 350, "add"),
        ([20, "−", "t", "=", 13], 7, "subfrom"), ([42, "−", "y", "=", 18], 24, "subfrom"), ([900, "−", "w", "=", 350], 550, "subfrom"),
        (["a", "−", 12, "=", 30], 42, "start"), (["b", "−", 45, "=", 27], 72, "start"),
    ]:
        L = [p for p in parts if isinstance(p, str) and p in LETTERS][0]
        nums = [p for p in parts if isinstance(p, int)]
        chk = plain(*[ans if p == L else p for p in parts])
        if kind == "add":
            a, s = nums
            e = ("The letter <i>%s</i> stands for the unknown number. Use the inverse: <i>%s</i> = %s = <b>%s</b>. "
                 "Check: %s. Not %s: that adds instead of subtracting." % (L, L, plain(s, "−", a), n(ans), chk, n(s + a)))
            cands = sub_cands(s, a, ans)
        elif kind == "subfrom":
            a, r = nums
            e = ("%s take away what leaves %s? <i>%s</i> = %s = <b>%s</b>. Check: %s. Not %s: that adds."
                 % (n(a), n(r), L, plain(a, "−", r), n(ans), plain(a, "−", ans, "=", r), n(a + r)))
            cands = sub_cands(a, r, ans)
        else:
            a, r = nums
            e = ("<i>%s</i> is the number you start with. Undo − %s by adding: <i>%s</i> = %s = <b>%s</b>. Check: %s. "
                 "Not %s: that subtracts instead of adding." % (L, n(a), L, plain(r, "+", a), n(ans), plain(ans, "−", a, "=", r), n(abs(r - a))))
            cands = add_cands(r, a, ans)
        solve(parts, ans, cands, e)
    solve(["x", "+", 15, "=", 15, "+", 20], 20, [35, 50, 15],
          "You can add in any order: 20 + 15 = 15 + 20. So <i>x</i> = <b>20</b>. Not 35: that is the value of the right side.",
          pic=True)
    solve(["h", "+", 30, "=", 40, "+", 25], 35, [65, 15, 95],
          "The right side is 40 + 25 = 65. So <i>h</i> + 30 = 65 and <i>h</i> = 65 − 30 = <b>35</b>. "
          "Not 65: that is the right side. Not 15: 30 is less than 40, so <i>h</i> must be more than 25, not less.", pic=True)
    # □ -> letter
    its.append(mcq("Which equation means the same as " + html("?", "+", 9, "=", 21) + "?", "k + 9 = 21",
                   ["k = 9 + 21", "k + 21 = 9", "9 − k = 21"],
                   "A letter can take the place of the box. Both stand for the same unknown number: <b>k + 9 = 21</b>. "
                   "In both, the unknown is 12."))
    # true for a value
    for v, right, wrongs in [
        (7, "a + 8 = 15", ["a + 8 = 16", "a − 7 = 7", "15 − a = 9"]),
        (25, "n + 25 = 50", ["n + 25 = 52", "50 − n = 20", "n − 5 = 30"]),
    ]:
        L = right[0]
        assert holds(right, v) and not any(holds(w, v) for w in wrongs)
        lhs = right.split(" = ")[0]
        e = ("Put %d in place of <i>%s</i>. %s = %d, so <b>%s</b> is true." % (v, L, lhs.replace(L, str(v)), val(lhs.replace(L, str(v))), right))
        its.append(mcq("Which equation is true when <i>%s</i> = %d?" % (L, v), right, wrongs, e))
    # words -> equation
    its.append(mcq("Which equation means “a number plus 12 is 30”?", "n + 12 = 30",
                   ["n = 12 + 30", "n − 12 = 30", "12 − n = 30"],
                   "Let <i>n</i> be the number. “Plus 12” is + 12 and “is 30” is = 30: <b>n + 12 = 30</b>. Then <i>n</i> = 18."))
    its.append(mcq("Which equation means “a number take away 8 is 25”?", "n − 8 = 25",
                   ["8 − n = 25", "n + 8 = 25", "n = 8 − 25"],
                   "Start with the number <i>n</i>, take away 8, and get 25: <b>n − 8 = 25</b>. Then <i>n</i> = 25 + 8 = 33. "
                   "8 − <i>n</i> starts with 8, not with the number."))
    # bar models with a letter
    its.append(mcq("What is <i>n</i> in the bar model?" + fig(bar_svg(70, 45, "n")), 25, [115, 35, 15],
                   "The two parts make the whole: 45 + <i>n</i> = 70. So <i>n</i> = 70 − 45 = <b>25</b>. "
                   "Not 115: that adds. Not 35: that takes the smaller digit from the larger."))
    assert sfl(70, 45) == 35
    its.append(mcq("What is <i>m</i> in the bar model?" + fig(bar_svg("m", 36, 48)), 84, [12, 74, 94],
                   "<i>m</i> is the whole, so add the parts: 36 + 48 = <b>84</b>. Not 12: that subtracts. "
                   "Not 74: that forgets to carry the ten from 6 + 8 = 14."))
    assert nocarry(36, 48) == 74
    # mistake
    nm, he, his = P.next()
    its.append(mcq("%s solves <i>y</i> + 17 = 40 and gets <i>y</i> = 57. What did %s do wrong?" % (nm, he),
                   cap(he) + " added instead of subtracting",
                   [cap(he) + " subtracted instead of adding", cap(he) + " forgot to carry", "Nothing, 57 is right"],
                   "57 + 17 is 74, not 40. %s <b>added instead of subtracting</b>. Use the inverse: "
                   "<i>y</i> = 40 − 17 = 23. Check: 23 + 17 = 40." % (cap(he))))
    assert len(its) == 20
    return {"title": "Letters for unknown numbers", "items": its}


# ============================================================ set 5: word problems
def set_words(P):
    its = []

    def match(q, right, wrongs, e, ans):
        assert holds(right, ans), right
        for w in wrongs:
            assert ans is None or not holds(w, ans), w
        its.append(mcq(q, right, wrongs, e))

    def solve(q, parts, ans, cands, e, money=False, bar=None):
        sentence = plain(*parts)
        assert holds(sentence, ans), sentence
        f = (lambda v: "$" + n(v)) if money else (lambda v: n(v))
        cs = [f(c) for c in cands if c > 0]
        q = q + (fig(bar_svg(*bar)) if bar else "")
        its.append(mcq(q, f(ans), cs, "Equation: %s. %s" % (html(*parts), e)))

    # 1
    nm, he, his = P.next()
    match("%s has 25 hockey cards. %s gets some more. Now %s has 60. Which equation shows this?" % (nm, cap(he), he),
          plain(25, "+", "?", "=", 60), [plain(25, "+", 60, "=", "?"), plain(60, "+", "?", "=", 25), plain("?", "−", 25, "=", 60)],
          "%s starts with 25, gets an unknown number more and ends with 60: <b>25 + □ = 60</b>. Then □ = 60 − 25 = 35." % nm, 35)
    # 2
    nm, he, his = P.next()
    solve("%s picks 37 apples at the orchard. %s wants 80 apples. How many more does %s need to pick?" % (nm, cap(he), he),
          [37, "+", "?", "=", 80], 43, sub_cands(80, 37, 43),
          "Use the inverse: □ = 80 − 37 = <b>43</b> apples. Check: 37 + 43 = 80. Not 117: that adds.")
    # 3
    solve("A Grade 3 class has raised $85 for the Terry Fox Run. The goal is $150. How much more do they need to raise?",
          [85, "+", "?", "=", 150], 65, sub_cands(150, 85, 65),
          "□ = 150 − 85 = <b>$65</b>. Check: $85 + $65 = $150. Not $235: that adds instead of subtracting.", money=True)
    # 4
    solve("There were 80 Canada geese on a pond. Some flew away. Now 35 are left. How many flew away?",
          [80, "−", "?", "=", 35], 45, sub_cands(80, 35, 45),
          "□ = 80 − 35 = <b>45</b> geese. Check: 80 − 45 = 35. Not 115: that adds. "
          "Not 55: that takes 0 from 5 instead of regrouping.", bar=(80, 35, "?"))
    # 5
    match("A bus takes students to the skating rink. At the first stop, 18 students get off. Now 24 are on the bus. "
          "Let <i>s</i> be the number of students at the start. Which equation matches?",
          "s − 18 = 24", ["s + 18 = 24", "24 − 18 = s", "18 − s = 24"],
          "Start with <i>s</i>, 18 get off, and 24 are left: <b>s − 18 = 24</b>. Then <i>s</i> = 24 + 18 = 42.", 42)
    # 6
    solve("A bus takes students to the skating rink. At the first stop, 18 students get off. Now 24 are on the bus. "
          "How many students were on the bus at the start?",
          ["s", "−", 18, "=", 24], 42, add_cands(24, 18, 42),
          "Undo − 18 by adding: <i>s</i> = 24 + 18 = <b>42</b> students. Check: 42 − 18 = 24. "
          "Not 6: that subtracts instead of adding. Not 32: that forgets to carry the ten.")
    # 7
    solve("The school library has 500 books in the reading corner. 275 are in English and the rest are in French. "
          "How many books are in French?",
          [275, "+", "?", "=", 500], 225, sub_cands(500, 275, 225),
          "□ = 500 − 275 = <b>225</b> books. Check: 275 + 225 = 500. Not 775: that adds.", bar=(500, 275, "?"))
    # 8
    solve("A sugar shack makes 400 L of maple syrup in March. It makes 150 L in the first week. "
          "How many litres does it make in the rest of March?",
          [150, "+", "?", "=", 400], 250, sub_cands(400, 150, 250),
          "□ = 400 − 150 = <b>250</b> L. Check: 150 + 250 = 400. Not 550: that adds.")
    # 9
    nm1, he1, his1 = P.next()
    nm2, he2, his2 = P.next()
    match("%s has 30 red blocks and 20 blue blocks. %s has 40 red blocks. %s wants the same number of blocks as %s. "
          "Which equation shows how many blue blocks %s needs?" % (nm1, nm2, nm2, nm1, nm2),
          plain(30, "+", 20, "=", 40, "+", "?"),
          [plain(30, "+", 20, "=", "?"), plain(30, "+", 40, "=", 20, "+", "?"), plain(40, "+", 20, "=", 30, "+", "?")],
          "The two totals must be the same, so the two sides are equal: <b>30 + 20 = 40 + □</b>. "
          "30 + 20 = 50, so □ = 10 blue blocks.", 10)
    # 10
    nm1, he1, his1 = P.next()
    nm2, he2, his2 = P.next()
    solve("%s has 26 stickers and gets 8 more. %s has 30 stickers. How many more does %s need to have the same number as %s?"
          % (nm1, nm2, nm2, nm1),
          [26, "+", 8, "=", 30, "+", "?"], 4, [34, 12, 64],
          "26 + 8 = 34. So 30 + □ = 34 and □ = <b>4</b>. Not 34: that is %s’s total. "
          "Not 12: 30 is more than 26, so %s needs fewer than 8, not more." % (nm1, nm2))
    # 11
    nm, he, his = P.next()
    solve("%s’s family goes on a 120 km canoe trip. They paddle 45 km on day 1 and 40 km on day 3. "
          "How far do they paddle on day 2?" % nm,
          [45, "+", "?", "+", 40, "=", 120], 35, [205, 75, 80],
          "45 + 40 = 85. So 85 + □ = 120 and □ = 120 − 85 = <b>35</b> km. "
          "Not 75: that forgets the 40 km on day 3. Not 205: that adds all the numbers.")
    # 12
    nm, he, his = P.next()
    match("%s reads <i>p</i> pages on Saturday and 35 pages on Sunday. %s reads 90 pages in all. Which equation matches?"
          % (nm, cap(he)),
          "p + 35 = 90", ["p = 90 + 35", "p − 35 = 90", "35 − p = 90"],
          "Saturday’s pages plus Sunday’s pages make 90: <b>p + 35 = 90</b>. Then <i>p</i> = 90 − 35 = 55.", 55)
    # 13
    solve("%s reads <i>p</i> pages on Saturday and 35 pages on Sunday. %s reads 90 pages in all. How many pages did %s read on Saturday?"
          % (nm, cap(he), he),
          ["p", "+", 35, "=", 90], 55, sub_cands(90, 35, 55),
          "<i>p</i> = 90 − 35 = <b>55</b> pages. Check: 55 + 35 = 90. Not 125: that adds.")
    # 14
    solve("A school has 600 students. On a snow day, only 245 students come to school. How many students stay home?",
          [245, "+", "?", "=", 600], 355, sub_cands(600, 245, 355),
          "□ = 600 − 245 = <b>355</b> students. Check: 245 + 355 = 600. Not 845: that adds. "
          "Not 445: that takes the smaller digit from the larger instead of regrouping.", bar=(600, 245, "?"))
    assert sfl(600, 245) == 445
    # 15
    nm, he, his = P.next()
    match("%s works out 72 − 38 = 34. Which equation can %s use to check %s answer?" % (nm, he, his),
          "34 + 38 = 72", ["72 + 38 = 110", "72 + 34 = 106", "38 − 34 = 72"],
          "Check a subtraction with addition, the inverse: <b>34 + 38 = 72</b> is true, so the answer is right. "
          "72 + 38 = 110 is true too, but it does not check the subtraction.", None)
    # 16
    nm, he, his = P.next()
    solve("%s has some money. %s spends $15 at the fall fair and has $28 left. How much money did %s have at the start?"
          % (nm, cap(he), he),
          ["?", "−", 15, "=", 28], 43, add_cands(28, 15, 43),
          "Undo − 15 by adding: □ = 28 + 15 = <b>$43</b>. Check: $43 − $15 = $28. "
          "Not $13: that subtracts. Not $33: that forgets to carry the ten.", money=True)
    # 17
    solve("There are 28 students in gym class. 13 are on the red team and the rest are on the blue team. "
          "How many are on the blue team?",
          [13, "+", "?", "=", 28], 15, [41, 25, 14],
          "□ = 28 − 13 = <b>15</b> students. Check: 13 + 15 = 28. Not 41: that adds.")
    # 18
    nm, he, his = P.next()
    match("%s’s family needs 64 buns for Thanksgiving dinner. They have 38 buns. Let <i>b</i> be the number of buns "
          "they still need. Which equation matches?" % nm,
          "38 + b = 64", ["38 + 64 = b", "b − 38 = 64", "64 + b = 38"],
          "They have 38, they need <i>b</i> more, and that makes 64: <b>38 + b = 64</b>. Then <i>b</i> = 64 − 38 = 26.", 26)
    # 19
    solve("The school wants to collect 1000 cans for the food bank. So far it has 640 cans. How many more cans does it need?",
          [640, "+", "?", "=", 1000], 360, [1640, 460, 260],
          "□ = 1000 − 640 = <b>360</b> cans. Check: 640 + 360 = 1000. Not 1640: that adds. "
          "Not 460: count on from 640 to 700 (60), then from 700 to 1000 (300). 60 + 300 = 360.")
    # 20
    nm, he, his = P.next()
    match("%s’s family drives 450 km to the cottage. They stop for lunch after 280 km. "
          "Which equation shows how far they still have to drive?" % nm,
          plain(280, "+", "?", "=", 450),
          [plain(450, "+", 280, "=", "?"), plain("?", "−", 280, "=", 450), plain(280, "−", "?", "=", 450)],
          "They drove 280 km, they still have □ km, and the whole trip is 450 km: <b>280 + □ = 450</b>. "
          "Then □ = 450 − 280 = 170 km.", 170)
    its[-1]["q"] += fig(bar_svg(450, 280, "?"))
    assert len(its) == 20
    return {"title": "Word problems with equations", "items": its}


# ============================================================ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def body_html():
    return (
        "<h2>The equal sign means “the same as”</h2>"
        "<p>An <b>equation</b> has an = sign. The = sign does not mean “the answer comes next”. "
        "It means both sides have the <b>same value</b>, like a pan balance that is level.</p>"
        "<figure class='sn-fig'>" + pan_svg("8 + 6", "10 + 4") +
        "<figcaption>8 + 6 = 14 and 10 + 4 = 14. The pans balance, so 8 + 6 = 10 + 4.</figcaption></figure>"
        "<h2>Find the missing number</h2>"
        "<p>A box □ or a letter like <i>n</i> stands for an <b>unknown</b> number. "
        "Use the inverse: subtraction undoes addition, and addition undoes subtraction. "
        "Then put your answer back in to check.</p>"
        "<figure class='sn-fig'>" + bar_svg(60, "?", 25) +
        "<figcaption>The two parts make 60. One part is 25, so the other part is 60 − 25 = 35.</figcaption></figure>" +
        table(["Equation", "Do this", "Answer"], [
            [html("?", "+", 25, "=", 60), "60 − 25", "35"],
            [html(80, "−", "?", "=", 35), "80 − 35", "45"],
            [html("?", "−", 15, "=", 40), "40 + 15", "55"],
            [html("n", "+", 6, "=", 14), "14 − 6", "<i>n</i> = 8"],
        ]) +
        ex("Example", html("?", "−", 15, "=", 40),
           "The box is the number you start with. Undo − 15 by adding: 40 + 15 = 55. Check: 55 − 15 = 40.", "55") +
        "<h2>Make both sides equal</h2>"
        "<p>When both sides have numbers, work out the side you know first. Then find what the other side needs.</p>"
        "<figure class='sn-fig'>" + pan_svg("40 + 15", "50 + " + BOX) +
        "<figcaption>40 + 15 = 55, so 50 + □ must also be 55. The box is 5.</figcaption></figure>" +
        ex("Example", html(40, "+", 15, "=", 50, "+", "?"),
           "The left side is 40 + 15 = 55. So 50 + □ = 55, and □ = 55 − 50 = 5. "
           "Or: 50 is 10 more than 40, so the box is 10 less than 15.", "5") +
        ex("Example", "What must be added to 45 + 20 to make it equal to 50 + 30?",
           "45 + 20 = 65 and 50 + 30 = 80. 80 − 65 = 15.", "15") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["40 + 15 = 50 + □, so □ = 55", "55 is the left side. 50 + □ = 55, so □ = 5"],
            ["40 + 15 = 50 + □, so □ = 25", "50 is more than 40, so □ is less than 15: □ = 5"],
            ["□ + 25 = 60, so □ = 85 (60 + 25)", "Use the inverse: 60 − 25 = 35"],
            ["□ − 15 = 40, so □ = 25 (40 − 15)", "Undo − 15 by adding: 40 + 15 = 55"],
            ["80 − 35 = 55 (smaller digit from larger)", "Regroup: 80 − 35 = 45"],
            ["9 + 6 = 15 + 5 = 20", "Write two equations: 9 + 6 = 15, then 15 + 5 = 20"],
        ])
    )


FAQ = [
    {"q": "What does the equal sign mean in Grade 3 math?",
     "a": "The equal sign means “is the same as”, not “the answer is”. In 40 + 15 = 50 + □, both sides must have the same value, so the box is 5, not 55."},
    {"q": "How do you find the missing number in an equation like □ + 25 = 60?",
     "a": "Use the inverse operation: subtraction undoes addition, so □ = 60 − 25 = 35. For □ − 15 = 40, add: 40 + 15 = 55. Then put the number back in to check."},
    {"q": "Why do Grade 3 students use letters like n in equations?",
     "a": "The Ontario curriculum (Algebra C2.1) has Grade 3 students use symbols and letters for unknown numbers. A letter works just like a box: in n + 6 = 14, n = 8."},
    {"q": "Are equations and equivalence part of the Grade 3 EQAO math assessment?",
     "a": "The Grade 3 EQAO math assessment is based on the Ontario curriculum, which includes the Algebra strand. Practising missing numbers, balances and word problems like these builds the skills students need."},
]


def gen_unit():
    rnd = random.Random(33808)
    P = People(rnd)
    sets = [set_same_as(P), set_missing(), set_equal_sides(), set_letters(P), set_words(P)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5), s["title"]
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"].count("<svg") <= 1
            assert it["q"] not in seen, it["q"]
            seen.add(it["q"])
    return {
        "country": "ca-on", "subject": "math", "grade": "grade-3", "slug": "equations-and-equivalence", "sort": 8,
        "updated": UPDATED, "pdf_url": "",
        "title": "Grade 3 Equations and Equivalence",
        "seo_title": "Grade 3 Equations and Equivalence Worksheets: Free Math with Answer Key (Ontario Curriculum)",
        "short_title": "Equations and Equivalence",
        "domain": "Algebra",
        "standard_code": "Grade 3: C2.2",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Determine what needs to be added to or subtracted from addition and subtraction expressions to make them equivalent",
        "meta_desc": "Free Grade 3 math worksheets on equations and equivalence for the Ontario curriculum: the equal sign as a balance, missing numbers like □ + 25 = 60, making both sides equal, letters for unknowns and word problems. 100 questions with an answer key, great EQAO practice.",
        "key_big": "The equal sign means “is the same as”. Both sides of an equation must have the same value.",
        "key_sub": "□ + 25 = 60, so □ = 60 − 25 = 35. In 40 + 15 = 50 + □, the left side is 55, so □ = 5, not 55.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen_unit()
    mark_large(u, "bar model|pan balance")
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(u, f, ensure_ascii=False, indent=1)
    print("wrote", path)
