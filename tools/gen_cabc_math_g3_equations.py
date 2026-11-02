# -*- coding: utf-8 -*-
"""
British Columbia Grade 3 Math: One-Step Equations
(BC Mathematics Curriculum, Grade 3 — Patterning: one-step addition and subtraction equations with an unknown number)
  python3 tools/gen_cabc_math_g3_equations.py
The equal sign as “the same as” (pan balances), missing numbers in addition (□ + 25 = 60), missing numbers in
subtraction (80 − □ = 35, □ − 15 = 40), writing an equation for a story, and word problems in BC contexts.
Numbers to 1000, money to $100.
Wrong choices come from real mistakes: reading = as “the answer is” (9 + 6 = 15 + 5 = 20), adding instead of using
the inverse (□ + 25 = 60 -> 85), subtracting when adding is needed (□ − 15 = 40 -> 25), taking the smaller digit
from the larger in each column (80 − 35 -> 55), forgetting to carry, and off-by-ten slips.
Every answer is checked in code. HTML attributes use single quotes. Canadian English.
"""
import json, os, random, re
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-3")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
GREY = "#e4e4e4"
INK = "#2b2b2b"
RED = "#c0392b"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Olivia", "Ava", "Chloe", "Simran", "Jasleen", "Mei", "Hana", "Sofia", "Emma", "Leah", "Zara", "Nadia"]
BOYS = ["Liam", "Ethan", "Noah", "Arjun", "Harjot", "Wei", "Mateo", "Lucas", "Kai", "Owen", "Ryan"]
BOX = "□"
NB = " "
LETTERS = "abcdefghijklmnopqrstuvwxyz"


# ------------------------------------------------------------ numbers and equations
def n(x):
    """BC style: 4 digits no separator, 5 or more digits grouped with a no-break space."""
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
    """Plain text equation (for choices and SVG): '?' becomes □."""
    return " ".join(tok(p) for p in parts)


def html(*parts):
    """Equation for question text: □ in bold."""
    out = []
    for p in parts:
        t = tok(p)
        if t == BOX:
            t = "<b>" + BOX + "</b>"
        out.append(t)
    return " ".join(out)


def val(expr):
    s = expr.replace("−", "-").replace(NB, "").replace("$", "")
    s = re.sub(r"(\d+)", r"F(\1)", s)
    return eval(s, {"__builtins__": {}, "F": Fraction})


def holds(eq, ans=None):
    """'□ + 25 = 60' is true with □ = ans."""
    s = re.sub(r"<[^>]+>", "", eq)
    if ans is not None:
        s = s.replace(BOX, str(ans))
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
        if c in seen or not c or c.startswith("-") or c.startswith("−") or c in ("$0",):
            continue
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    return {"q": q, "c": [correct] + pick, "a": 0, "e": e}


def mcq_r(q, ans, cands, e, fmt=None):
    """Numeric answer. cands = [(value, reason or None)]. The explanation gets a “Not X: reason.”
    for every wrong choice that is shown and has a reason."""
    fmt = fmt or n
    seen = {ans}
    pick = []
    for v, why in cands:
        if v <= 0 or v in seen:
            continue
        seen.add(v)
        pick.append((v, why))
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, ans, cands)
    for v, why in pick:
        if why:
            e += " Not %s: %s." % (fmt(v), why)
    return {"q": q, "c": [fmt(ans)] + [fmt(v) for v, _ in pick], "a": 0, "e": e}


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
    """Draw 'a + □' centred at cx: □ drawn as a red box."""
    ts = s.split(" ")
    x = cx - expr_w(s) / 2
    out = []
    for t in ts:
        w = tok_w(t)
        if t == BOX:
            out.append("<rect x='%.1f' y='%.1f' width='%d' height='%d' fill='#fff' stroke='%s' stroke-width='2.5'/>"
                       % (x, base - 16, BOXW, BOXW, RED))
        else:
            out.append("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                       % (x + w / 2, base, FS, INK, t))
        x += w + GAP
    return "".join(out)


def lab(t):
    return t.replace(BOX, "box")


def pan_svg(left, right):
    """A level pan balance with an expression on each pan."""
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
                    "pan balance: %s on the left and %s on the right" % (lab(left), lab(right)))


def bar_svg(whole, p1, p2):
    """Part-part-whole bar model, drawn to scale. Values are numbers or '?' (box)."""
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
    lb = "bar model: whole %s, parts %s and %s" % tuple(lab(tok(v)) for v in vals)
    return svg_wrap(W + 16, 8 + 2 * h + 10 + 8, "".join(s), lb)


def mark_large(u, pattern):
    rx = re.compile(r"<svg (?=[^>]*aria-label='(?:" + pattern + "))")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


# ------------------------------------------------------------ distractor lists (value, reason)
ADDS = "that adds instead of subtracting"
SUBS = "that subtracts instead of adding"
SFL = "that takes the smaller digit from the larger in each column instead of regrouping"
CARRY = "that forgets to carry"


def sub_cands(big, small, ans):
    """Answer is big − small."""
    c = [(big + small, ADDS)]
    if sfl(big, small) != ans:
        c.append((sfl(big, small), SFL))
    return c + [(ans + 10, None), (ans - 10, None), (ans + 1, None), (ans - 1, None), (ans + 100, None)]


def add_cands(a, b, ans):
    """Answer is a + b."""
    c = [(abs(a - b), SUBS)]
    if nocarry(a, b) != ans:
        c.append((nocarry(a, b), CARRY))
    return c + [(ans - 10, None), (ans + 10, None), (ans + 1, None), (ans - 1, None)]


WHAT = "<br>What number goes in the box?"


# ============================================================ set 1: balances
def set_balances(P):
    its = []
    # A. which equation matches the balance
    for l, r, right, wrongs in [
        ("6 + 8", "14", "6 + 8 = 14", ["6 + 8 = 15", "6 = 8 + 14", "14 + 8 = 6"]),
        ("12", "20 − 8", "12 = 20 − 8", ["12 = 20 + 8", "12 + 20 = 8", "20 = 12 − 8"]),
        ("9 + 7", "10 + 6", "9 + 7 = 10 + 6", ["9 + 7 = 16 + 6", "9 + 7 = 10 + 7", "9 + 6 = 10 + 7"]),
        ("30 − 10", "15 + 5", "30 − 10 = 15 + 5", ["30 − 10 = 15 − 5", "30 + 10 = 15 + 5", "30 − 10 = 20 + 5"]),
    ]:
        assert holds(right) and not any(holds(w) for w in wrongs)
        if " " in l and " " in r:
            e = ("The pans balance. %s = %s and %s = %s, so <b>%s</b>. The = sign means “is the same as”."
                 % (l, val(l), r, val(r), right))
        else:
            e = ("The pans balance, so both sides have the same value. The left pan has %s and the right pan has %s, "
                 "so <b>%s</b>. The = sign can sit between any two things that are the same." % (l, r, right))
        its.append(mcq("The pans balance. Which equation matches?" + fig(pan_svg(l, r)), right, wrongs, e))
    # B. balance with a box (one step)
    for l, r, ans, wr, e in [
        ("9 + 6", BOX, 15, [3, 14, 16], "The pans balance, so the box has the same value as 9 + 6. 9 + 6 = <b>15</b>. "
         "Not 3: that subtracts."),
        (BOX + " + 6", "14", 8, [20, 9, 7], "Something plus 6 balances 14. Use the inverse: 14 − 6 = <b>8</b>. "
         "Check: 8 + 6 = 14. Not 20: that adds 14 and 6."),
        (BOX + " − 8", "12", 20, [4, 19, 21], "Something take away 8 leaves 12. Undo − 8 by adding: 12 + 8 = <b>20</b>. "
         "Check: 20 − 8 = 12. Not 4: that subtracts instead of adding."),
        ("70", "30 + " + BOX, 40, [100, 4, 50], "30 plus something balances 70. 70 − 30 = <b>40</b>. "
         "Check: 30 + 40 = 70. Not 100: that adds. Not 4: 4 tens is 40."),
        (BOX, "50 − 15", 35, [65, 45, 25], "The box must be the same as 50 − 15. 50 − 15 = <b>35</b>. "
         "Not 65: that adds. Not 45: that takes 0 from 5 instead of regrouping."),
        ("25 + " + BOX, "60", 35, [85, 45, 25], "25 plus something balances 60. Use the inverse: 60 − 25 = <b>35</b>. "
         "Check: 25 + 35 = 60. Not 85: that adds. Not 45: that takes 0 from 5 instead of regrouping."),
    ]:
        eq = (l + " = " + r)
        assert holds(eq, ans) and not any(holds(eq, w) for w in wr), eq
        its.append(mcq("The pans balance." + WHAT + fig(pan_svg(l, r)), ans, wr, e))
    # C. which equation is true
    prompts = iter(["Which equation is true?", "Which equation is true? The total can come first.",
                    "Work out both sides. Which equation is true?", "Which equation is true? Check both sides."])
    for right, wrongs, e in [
        ("8 + 4 = 7 + 5", ["8 + 4 = 12 + 5", "8 + 4 = 7 + 4", "8 + 4 = 9 + 4"],
         "Work out both sides. 8 + 4 = 12 and 7 + 5 = 12, so <b>8 + 4 = 7 + 5</b> is true. "
         "8 + 4 = 12 + 5 is false: 12 + 5 is 17."),
        ("16 = 8 + 8", ["16 = 8 + 9", "8 = 16 + 8", "16 = 7 + 8"],
         "8 + 8 = 16, so <b>16 = 8 + 8</b> is true. The total can come first, before the = sign."),
        ("15 − 5 = 6 + 4", ["15 − 5 = 10 + 4", "15 − 5 = 20", "15 + 5 = 6 + 4"],
         "15 − 5 = 10 and 6 + 4 = 10, so <b>15 − 5 = 6 + 4</b> is true. Both sides are 10."),
        ("45 + 10 = 50 + 5", ["45 + 10 = 55 + 5", "45 + 10 = 50 + 10", "45 + 10 = 40 + 5"],
         "45 + 10 = 55 and 50 + 5 = 55, so <b>45 + 10 = 50 + 5</b> is true. "
         "45 + 10 = 55 + 5 is false: 55 + 5 is 60, not 55."),
    ]:
        assert holds(right) and not any(holds(w) for w in wrongs)
        its.append(mcq(next(prompts), right, wrongs, e))
    # D. which expression has the same value
    for ex_, right, wrongs in [
        ("6 + 9", "10 + 5", ["10 + 9", "6 + 10", "15 + 9"]),
        ("30 − 8", "20 + 2", ["30 + 8", "20 + 8", "38 − 8"]),
    ]:
        v = val(ex_)
        assert val(right) == v and all(val(w) != v for w in wrongs)
        e = "%s = %s and %s = %s. They have the same value, so <b>%s = %s</b>." % (ex_, v, right, v, ex_, right)
        its.append(mcq("Which has the same value as %s?" % ex_, right, wrongs, e))
    # E. = sign first
    its.append(mcq(html("?", "=", 9, "+", 7) + WHAT, 16, [2, 15, 17],
                   "The = sign can come first. The box is the same as 9 + 7, so it is <b>16</b>. Not 2: that subtracts."))
    assert sfl(40, 16) == 36
    its.append(mcq(html("?", "=", 40, "−", 16) + WHAT, 24, [56, 36, 34],
                   "The box is the same as 40 − 16. 40 − 16 = <b>24</b>. Not 56: that adds. "
                   "Not 36: that takes 0 from 6 instead of regrouping."))
    # F. meaning and a mistake
    its.append(mcq("What does the = sign mean in 6 + 4 = 7 + 3?", "Both sides are the same",
                   ["The answer comes next", "Add all the numbers", "The left side is bigger"],
                   "= means “is the same as”. 6 + 4 = 10 and 7 + 3 = 10, so <b>both sides are the same</b>. "
                   "It does not just mean “the answer comes next”."))
    nm, he, his = P.next()
    its.append(mcq("%s adds 8 and 7, then adds 5. %s writes 8 + 7 = 15 + 5 = 20. What is wrong?" % (nm, cap(he)),
                   "8 + 7 is not the same as 15 + 5",
                   ["8 + 7 is not 15", "15 + 5 is not 20", "Nothing is wrong"],
                   "= means both sides are the same. 8 + 7 = 15, but 15 + 5 = 20, so “8 + 7 = 15 + 5” is <b>not true</b>. "
                   "%s should write two equations: 8 + 7 = 15 and 15 + 5 = 20." % nm))
    assert len(its) == 20
    return {"title": "Balances: the equal sign means “the same as”", "items": its}


# ============================================================ set 2: □ + 25 = 60
def set_add_unknown(P):
    its = []

    def add(parts, ans, cands, e, bar=None):
        eq = plain(*parts)
        assert holds(eq, ans), eq
        q = html(*parts) + WHAT + (fig(bar_svg(*bar)) if bar else "")
        its.append(mcq_r(q, ans, cands, e))

    # easy facts first
    add(["?", "+", 7, "=", 15], 8, sub_cands(15, 7, 8),
        "Use the inverse. Subtraction undoes addition: □ = 15 − 7 = <b>8</b>. Check: 8 + 7 = 15.")
    for a, s, first, bar in [(9, 17, False, False), (300, 700, True, False), (25, 60, True, True), (40, 90, False, False),
                             (18, 50, True, False), (37, 80, False, False), (46, 90, True, False), (28, 65, False, True),
                             (19, 47, False, False), (38, 72, True, False), (63, 81, False, False), (150, 400, True, True), (240, 500, False, False),
                             (275, 600, True, False), (365, 800, False, True), (125, 310, False, False)]:
        ans = s - a
        if first:
            parts = ["?", "+", a, "=", s]
            b = (s, "?", a)
            lead = "Use the inverse. Subtraction undoes addition: □ = %s = <b>%s</b>." % (plain(s, "−", a), n(ans))
            chk = plain(ans, "+", a, "=", s)
        else:
            parts = [a, "+", "?", "=", s]
            b = (s, a, "?")
            lead = ("Think: %s plus what makes %s? Use the inverse: □ = %s = <b>%s</b>."
                    % (n(a), n(s), plain(s, "−", a), n(ans)))
            chk = plain(a, "+", ans, "=", s)
        cands = sub_cands(s, a, ans)
        if a % 100 == 0 and s % 100 == 0:
            lead += " That is %d hundreds − %d hundreds = %d hundreds." % (s // 100, a // 100, ans // 100)
            cands = [(s + a, ADDS), (ans // 100, "%d hundreds is %s" % (ans // 100, n(ans))), (ans // 10, None)]
        add(parts, ans, cands, lead + " Check: %s." % chk, b if bar else None)
    # = sign first
    add([70, "=", "?", "+", 45], 25, sub_cands(70, 45, 25),
        "The = sign can come first. □ + 45 = 70, so □ = 70 − 45 = <b>25</b>. Check: 25 + 45 = 70.")
    add([100, "=", 64, "+", "?"], 36, sub_cands(100, 64, 36) + [(46, None)],
        "64 + □ = 100, so □ = 100 − 64 = <b>36</b>. Count on: 64 to 70 is 6, and 70 to 100 is 30. Check: 64 + 36 = 100.",
        (100, 64, "?"))
    # a mistake
    nm, he, his = P.next()
    assert sfl(92, 38) == 66
    its.append(mcq("%s says that in %s, the box is 130. Is %s right?" % (nm, html("?", "+", 38, "=", 92), he),
                   "No, the box is 54", ["Yes, the box is 130", "No, the box is 66", "No, the box is 64"],
                   "Check: 130 + 38 = 168, not 92. %s added instead of subtracting. Use the inverse: "
                   "92 − 38 = <b>54</b>. Check: 54 + 38 = 92. 66 takes the smaller digit from the larger in each column."
                   % nm))
    assert len(its) == 20, len(its)
    return {"title": "Missing numbers in addition: □ + 25 = 60", "items": its}


# ============================================================ set 3: 80 − □ = 35
def set_sub_unknown(P):
    its = []

    def add(parts, ans, cands, e, bar=None):
        eq = plain(*parts)
        assert holds(eq, ans), eq
        q = html(*parts) + WHAT + (fig(bar_svg(*bar)) if bar else "")
        its.append(mcq_r(q, ans, cands, e))

    rows = [("take", 15, 9, False), ("start", 8, 7, False), ("take", 80, 35, True), ("start", 15, 40, False),
            ("take", 64, 28, False), ("take", 52, 17, False), ("start", 26, 57, True), ("take", 90, 46, False),
            ("start", 36, 45, False), ("take", 300, 120, True), ("start", 120, 380, False), ("take", 430, 160, False),
            ("take", 705, 480, False), ("start", 250, 475, True), ("take", 600, 245, False), ("take", 500, 275, False)]
    for kind, a, r, bar in rows:
        if kind == "take":
            ans = a - r
            e = ("%s take away what leaves %s? □ = %s = <b>%s</b>. Check: %s."
                 % (n(a), n(r), plain(a, "−", r), n(ans), plain(a, "−", ans, "=", r)))
            add([a, "−", "?", "=", r], ans, sub_cands(a, r, ans), e, (a, r, "?") if bar else None)
        else:
            ans = r + a
            e = ("The box is the number you start with. Undo − %s by adding: □ = %s = <b>%s</b>. Check: %s."
                 % (n(a), plain(r, "+", a), n(ans), plain(ans, "−", a, "=", r)))
            add(["?", "−", a, "=", r], ans, add_cands(r, a, ans), e, ("?", r, a) if bar else None)
    # = sign first
    add([50, "=", 92, "−", "?"], 42, sub_cands(92, 50, 42),
        "The = sign can come first. 92 − □ = 50, so □ = 92 − 50 = <b>42</b>. Check: 92 − 42 = 50.")
    add([25, "=", "?", "−", 18], 43, add_cands(25, 18, 43),
        "□ − 18 = 25. □ is the number you start with, so add: □ = 25 + 18 = <b>43</b>. Check: 43 − 18 = 25.")
    # mistakes and checking
    nm, he, his = P.next()
    its.append(mcq("%s solves %s and gets 23. What did %s do wrong?" % (nm, html("?", "−", 17, "=", 40), he),
                   cap(he) + " subtracted instead of adding",
                   [cap(he) + " added instead of subtracting", cap(he) + " forgot to regroup", "Nothing, 23 is right"],
                   "Check: 23 − 17 = 6, not 40. %s <b>subtracted instead of adding</b>. The box is the number you start "
                   "with, so undo − 17 by adding: 40 + 17 = 57. Check: 57 − 17 = 40." % cap(he)))
    nm, he, his = P.next()
    its.append(mcq("%s solves %s and gets 34. Which equation checks %s answer?" % (nm, html(72, "−", "?", "=", 38), his),
                   "34 + 38 = 72", ["72 + 38 = 110", "72 + 34 = 106", "38 − 34 = 4"],
                   "Check a subtraction with addition, the inverse: <b>34 + 38 = 72</b> is true, so 34 is right. "
                   "72 + 38 = 110 is true too, but it does not check the answer."))
    assert len(its) == 20, len(its)
    return {"title": "Missing numbers in subtraction: 80 − □ = 35", "items": its}


# ============================================================ set 4: write an equation for a story
def set_write(P):
    its = []

    def match(q, right, wrongs, e, ans):
        assert holds(right, ans), right
        for w in wrongs:
            assert not holds(w, ans), w
        assert len(set(wrongs + [right])) == 4
        its.append(mcq(q, right, wrongs, e))

    W = "Which equation matches?"
    nm, he, his = P.next()
    match("%s has 25 hockey cards. %s gets some more. Now %s has 60. %s" % (nm, cap(he), he, W),
          plain(25, "+", "?", "=", 60), [plain(25, "+", 60, "=", "?"), plain(60, "+", "?", "=", 25), plain("?", "−", 25, "=", 60)],
          "%s starts with 25, gets an unknown number more and ends with 60: <b>25 + □ = 60</b>. "
          "25 + 60 = □ is wrong: 60 is the total, not a part. Then □ = 60 − 25 = 35." % nm, 35)
    nm, he, his = P.next()
    match("%s picks 36 blueberries. Then %s picks 27 more. How many does %s have in all? %s" % (nm, he, he, W),
          plain(36, "+", 27, "=", "?"), [plain(36, "−", 27, "=", "?"), plain(36, "+", "?", "=", 27), plain("?", "+", 27, "=", 36)],
          "Joining 36 and 27 gives the total: <b>36 + 27 = □</b>. So □ = 63.", 63)
    match("There are 45 bald eagles in the trees near Squamish. Some fly away. Now 18 are left. " + W,
          plain(45, "−", "?", "=", 18), [plain(45, "+", 18, "=", "?"), plain("?", "−", 45, "=", 18), plain(18, "−", "?", "=", 45)],
          "Start with 45, take away an unknown number and 18 are left: <b>45 − □ = 18</b>. Then □ = 45 − 18 = 27.", 27)
    match("A SkyTrain car has 64 people on it. At the next station, 28 people get off. How many are on now? " + W,
          plain(64, "−", 28, "=", "?"), [plain(64, "+", 28, "=", "?"), plain("?", "−", 28, "=", 64), plain(28, "+", 64, "=", "?")],
          "Start with 64 and take away 28: <b>64 − 28 = □</b>. So □ = 36 people. Getting off means take away, not add.", 36)
    match("Some children are playing at Stanley Park. 15 more children come. Now there are 42. " + W,
          plain("?", "+", 15, "=", 42), [plain(15, "+", 42, "=", "?"), plain("?", "−", 15, "=", 42), plain(15, "−", "?", "=", 42)],
          "The unknown is how many children were there at the start. Add 15 and you get 42: <b>□ + 15 = 42</b>. "
          "Then □ = 42 − 15 = 27.", 27)
    match("There are 28 students in a class. 13 are on the red team. The rest are on the blue team. " + W,
          plain(13, "+", "?", "=", 28), [plain(13, "+", 28, "=", "?"), plain("?", "−", 13, "=", 28), plain(28, "+", "?", "=", 13)],
          "The red team and the blue team make the whole class: <b>13 + □ = 28</b>. Then □ = 28 − 13 = 15.", 15)
    nm, he, his = P.next()
    match("%s has some money. %s spends $12 at the Richmond Night Market and has $25 left. %s" % (nm, cap(he), W),
          plain("?", "−", 12, "=", 25), [plain(12, "−", "?", "=", 25), plain(25, "−", 12, "=", "?"), plain("?", "+", 25, "=", 12)],
          "The unknown is the money at the start. Take away $12 and $25 is left: <b>□ − 12 = 25</b>. "
          "Then □ = 25 + 12 = $37. 25 − 12 = □ uses the wrong operation.", 37)
    match("Which equation means “a number plus 12 is 30”?",
          plain("?", "+", 12, "=", 30), [plain("?", "=", 12, "+", 30), plain("?", "−", 12, "=", 30), plain(12, "−", "?", "=", 30)],
          "Use □ for the number. “Plus 12” is + 12 and “is 30” is = 30: <b>□ + 12 = 30</b>. Then □ = 18.", 18)
    match("Which equation means “a number take away 8 is 25”?",
          plain("?", "−", 8, "=", 25), [plain(8, "−", "?", "=", 25), plain("?", "+", 8, "=", 25), plain(25, "−", 8, "=", "?")],
          "Start with the number □, take away 8, and get 25: <b>□ − 8 = 25</b>. Then □ = 25 + 8 = 33. "
          "8 − □ starts with 8, not with the number.", 33)
    match("Which equation matches the bar model?" + fig(bar_svg(90, 54, "?")),
          plain(54, "+", "?", "=", 90), [plain(54, "+", 90, "=", "?"), plain("?", "−", 54, "=", 90), plain(90, "+", "?", "=", 54)],
          "The two parts, 54 and □, make the whole, 90: <b>54 + □ = 90</b>. Then □ = 90 − 54 = 36.", 36)
    match("Which equation matches the bar model?" + fig(bar_svg("?", 36, 48)),
          plain(36, "+", 48, "=", "?"), [plain(48, "−", 36, "=", "?"), plain(36, "+", "?", "=", 48), plain(36, "−", "?", "=", 48)],
          "The box is the whole. The parts 36 and 48 join to make it: <b>36 + 48 = □</b>. So □ = 84.", 84)
    match("A BC Ferries boat has some cars on it. Then 140 more cars drive on. Now there are 400 cars. " + W,
          plain("?", "+", 140, "=", 400), [plain("?", "=", 140, "+", 400), plain("?", "−", 140, "=", 400), plain(140, "−", "?", "=", 400)],
          "Some cars and 140 more make 400: <b>□ + 140 = 400</b>. Then □ = 400 − 140 = 260.", 260)
    match("A Grade 3 class has raised $320 for the Terry Fox Run. The goal is $500. Which equation shows how much "
          "more they need?",
          plain(320, "+", "?", "=", 500), [plain(320, "+", 500, "=", "?"), plain("?", "−", 320, "=", 500), plain(500, "+", "?", "=", 320)],
          "What they have plus what they still need makes the goal: <b>320 + □ = 500</b>. Then □ = 500 − 320 = $180.", 180)
    match("The school library has 600 books. Some are checked out. 450 books are still on the shelves. " + W,
          plain(600, "−", "?", "=", 450), [plain(600, "+", 450, "=", "?"), plain("?", "−", 600, "=", 450), plain(450, "−", "?", "=", 600)],
          "Start with 600, take away the books checked out, and 450 are left: <b>600 − □ = 450</b>. Then □ = 150.", 150)
    match("Which equation matches the bar model?" + fig(bar_svg(500, "?", 275)),
          plain("?", "+", 275, "=", 500), [plain(500, "+", 275, "=", "?"), plain("?", "−", 275, "=", 500), plain(275, "−", "?", "=", 500)],
          "The parts □ and 275 make the whole, 500: <b>□ + 275 = 500</b>. Then □ = 500 − 275 = 225.", 225)
    nm, he, his = P.next()
    match("%s’s family drives 350 km from Vancouver to Kamloops. They stop in Hope after 150 km. Which equation shows "
          "how far they still have to drive?" % nm,
          plain(150, "+", "?", "=", 350), [plain(350, "+", 150, "=", "?"), plain("?", "−", 150, "=", 350), plain(150, "−", "?", "=", 350)],
          "They drove 150 km, they still have □ km, and the whole trip is 350 km: <b>150 + □ = 350</b>. "
          "Then □ = 350 − 150 = 200 km.", 200)
    # equation -> story
    its.append(mcq("Which story matches " + html(60, "−", "?", "=", 35) + "?",
                   "60 geese are on a pond. Some fly away. 35 are left. How many flew away?",
                   ["60 geese are on a pond. 35 more land. How many are there now?",
                    "Some geese are on a pond. 35 fly away. 60 are left. How many were there?",
                    "60 geese and 35 ducks are on a pond. How many birds are there?"],
                   "60 − □ = 35 starts with 60, takes away an unknown number and leaves 35. "
                   "That is the story where <b>some geese fly away and 35 are left</b>. Then □ = 60 − 35 = 25."))
    nm, he, his = P.next()
    its.append(mcq("Which story matches " + html("?", "+", 18, "=", 50) + "?",
                   "%s has some stickers. %s gets 18 more. Now %s has 50. How many did %s have at first?" % (nm, cap(he), he, he),
                   ["%s has 50 stickers. %s gets 18 more. How many does %s have now?" % (nm, cap(he), he),
                    "%s has some stickers. %s gives away 18. Now %s has 50. How many did %s have at first?" % (nm, cap(he), he, he),
                    "%s has 18 stickers. %s gets 50 more. How many does %s have now?" % (nm, cap(he), he)],
                   "□ + 18 = 50: an unknown start, plus 18, makes 50. That is the story where %s <b>has some stickers, "
                   "gets 18 more and then has 50</b>. Then □ = 50 − 18 = 32." % nm))
    # fix a mistake
    nm, he, his = P.next()
    match("“48 people are on a SkyTrain. Some get off. Now 30 are on.” %s writes 48 + 30 = □. Which equation should "
          "%s write?" % (nm, he),
          plain(48, "−", "?", "=", 30), [plain(48, "+", "?", "=", 30), plain("?", "−", 48, "=", 30), plain(30, "−", "?", "=", 48)],
          "People get off, so it is take away. Start with 48, take away □, and 30 are left: <b>48 − □ = 30</b>. "
          "Then □ = 18. 48 + 30 adds instead.", 18)
    # comparison (hard)
    nm1, he1, his1 = P.next()
    nm2, he2, his2 = P.next()
    match("%s has 42 hockey cards. %s has 15 more cards than %s. Which equation shows how many cards %s has?"
          % (nm1, nm2, nm1, nm2),
          plain(42, "+", 15, "=", "?"), [plain(42, "−", 15, "=", "?"), plain(15, "+", "?", "=", 42), plain(42, "+", "?", "=", 15)],
          "“15 more than 42” means add 15 to 42: <b>42 + 15 = □</b>. So %s has 57 cards. "
          "42 − 15 would give fewer cards, not more." % nm2, 57)
    assert len(its) == 20, len(its)
    return {"title": "Write an equation for a story", "items": its}


# ============================================================ set 5: word problems
def set_words(P):
    its = []

    def solve(q, parts, ans, cands, e, unit="", money=False, bar=None):
        eq = plain(*parts)
        assert holds(eq, ans), eq
        if money:
            f = lambda v: "$" + n(v)
        else:
            f = lambda v: n(v) + unit
        its.append(mcq_r(q + (fig(bar_svg(*bar)) if bar else ""), ans, cands,
                         "Equation: %s. %s" % (html(*parts), e), f))

    nm, he, his = P.next()
    solve("%s has 25 hockey cards. %s gets some more. Now %s has 60 cards. How many cards did %s get?"
          % (nm, cap(he), he, he),
          [25, "+", "?", "=", 60], 35, sub_cands(60, 25, 35),
          "Use the inverse: □ = 60 − 25 = <b>35</b> cards. Check: 25 + 35 = 60.")
    nm, he, his = P.next()
    solve("%s picks 37 apples at an orchard in the Okanagan. %s wants 80 apples. How many more does %s need to pick?"
          % (nm, cap(he), he),
          [37, "+", "?", "=", 80], 43, sub_cands(80, 37, 43),
          "Use the inverse: □ = 80 − 37 = <b>43</b> apples. Check: 37 + 43 = 80.")
    solve("There were 80 Canada geese on a pond. Some flew away. Now 35 are left. How many flew away?",
          [80, "−", "?", "=", 35], 45, sub_cands(80, 35, 45),
          "□ = 80 − 35 = <b>45</b> geese. Check: 80 − 45 = 35.", bar=(80, 35, "?"))
    solve("There are 28 students in gym class. 13 are on the red team and the rest are on the blue team. "
          "How many are on the blue team?",
          [13, "+", "?", "=", 28], 15, sub_cands(28, 13, 15),
          "□ = 28 − 13 = <b>15</b> students. Check: 13 + 15 = 28.")
    solve("A Grade 3 class has raised $64 for the Terry Fox Run. The goal is $100. How much more do they need to raise?",
          [64, "+", "?", "=", 100], 36, sub_cands(100, 64, 36) + [(46, None)],
          "□ = 100 − 64 = <b>$36</b>. Count on: $64 to $70 is $6, and $70 to $100 is $30. Check: $64 + $36 = $100.",
          money=True)
    solve("A bus takes students to Grouse Mountain. At the first stop, 18 students get off. Now 24 are on the bus. "
          "How many students were on the bus at the start?",
          ["?", "−", 18, "=", 24], 42, add_cands(24, 18, 42),
          "Undo − 18 by adding: □ = 24 + 18 = <b>42</b> students. Check: 42 − 18 = 24.")
    nm, he, his = P.next()
    solve("%s reads some pages on Saturday and 35 pages on Sunday. %s reads 90 pages in all. "
          "How many pages did %s read on Saturday?" % (nm, cap(he), he),
          ["?", "+", 35, "=", 90], 55, sub_cands(90, 35, 55),
          "□ = 90 − 35 = <b>55</b> pages. Check: 55 + 35 = 90.")
    nm, he, his = P.next()
    solve("%s has some money. %s spends $15 at the PNE and has $28 left. How much money did %s have at the start?"
          % (nm, cap(he), he),
          ["?", "−", 15, "=", 28], 43, add_cands(28, 15, 43),
          "Undo − 15 by adding: □ = 28 + 15 = <b>$43</b>. Check: $43 − $15 = $28.", money=True)
    nm, he, his = P.next()
    solve("%s has $50. %s buys a book and has $18 left. How much did the book cost?" % (nm, cap(he)),
          [50, "−", "?", "=", 18], 32, sub_cands(50, 18, 32),
          "□ = 50 − 18 = <b>$32</b>. Check: $50 − $32 = $18.", money=True)
    solve("Two classes go on a field trip to the Royal BC Museum in Victoria. There are 52 students in all. "
          "One class has 27 students. How many students are in the other class?",
          [27, "+", "?", "=", 52], 25, sub_cands(52, 27, 25),
          "□ = 52 − 27 = <b>25</b> students. Check: 27 + 25 = 52.")
    solve("A class counts bald eagles near Brackendale. They count 26 eagles on Saturday and some more on Sunday. "
          "They count 61 eagles in all. How many did they count on Sunday?",
          [26, "+", "?", "=", 61], 35, sub_cands(61, 26, 35),
          "□ = 61 − 26 = <b>35</b> eagles. Check: 26 + 35 = 61.")
    solve("A class counts 150 salmon in a creek on Monday. On Friday they count 320 salmon. "
          "How many more salmon do they count on Friday?",
          [150, "+", "?", "=", 320], 170, sub_cands(320, 150, 170),
          "□ = 320 − 150 = <b>170</b> salmon. Check: 150 + 170 = 320.", bar=(320, 150, "?"))
    solve("A school has 400 students. 165 students walk to school. The rest come by bus or car. "
          "How many students come by bus or car?",
          [165, "+", "?", "=", 400], 235, sub_cands(400, 165, 235),
          "□ = 400 − 165 = <b>235</b> students. Check: 165 + 235 = 400.")
    solve("The school library has 500 books in the reading corner. 275 are in English and the rest are in French. "
          "How many books are in French?",
          [275, "+", "?", "=", 500], 225, sub_cands(500, 275, 225),
          "□ = 500 − 275 = <b>225</b> books. Check: 275 + 225 = 500.", bar=(500, 275, "?"))
    solve("A hiking trail is 850 m long. A class has walked 475 m. How many metres do they still have to walk?",
          [475, "+", "?", "=", 850], 375, sub_cands(850, 475, 375),
          "□ = 850 − 475 = <b>375</b> m. Check: 475 + 375 = 850.", unit=" m")
    solve("A ski hill has 600 pairs of rental skis. 385 pairs are rented out. How many pairs are left?",
          [600, "−", 385, "=", "?"], 215, sub_cands(600, 385, 215),
          "Work out 600 − 385 = <b>215</b> pairs. Check: 215 + 385 = 600.")
    solve("A ferry to Vancouver Island has room for 400 cars. 265 cars are on it. How many more cars can drive on?",
          [265, "+", "?", "=", 400], 135, sub_cands(400, 265, 135),
          "□ = 400 − 265 = <b>135</b> cars. Check: 265 + 135 = 400.")
    nm, he, his = P.next()
    solve("%s gives away 45 stickers. Now %s has 128 stickers. How many stickers did %s have at the start?"
          % (nm, he, he),
          ["?", "−", 45, "=", 128], 173, add_cands(128, 45, 173),
          "Undo − 45 by adding: □ = 128 + 45 = <b>173</b> stickers. Check: 173 − 45 = 128.")
    nm, he, his = P.next()
    solve("%s’s family drives from Vancouver to Kelowna, about 390 km. They stop in Merritt after 270 km. "
          "How many kilometres do they still have to drive?" % nm,
          [270, "+", "?", "=", 390], 120, sub_cands(390, 270, 120),
          "□ = 390 − 270 = <b>120</b> km. Check: 270 + 120 = 390.", unit=" km", bar=(390, 270, "?"))
    solve("A school wants to collect 1000 cans for the food bank. So far it has 640 cans. How many more cans does it need?",
          [640, "+", "?", "=", 1000], 360, [(1640, ADDS), (460, "count on from 640 to 700 (60), then from 700 to 1000 (300)"),
                                           (260, None)],
          "□ = 1000 − 640 = <b>360</b> cans. Check: 640 + 360 = 1000.")
    assert len(its) == 20, len(its)
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
        "<h2>Find the unknown: use the inverse</h2>"
        "<p>A box □ stands for an <b>unknown</b> number. To find it, use the <b>inverse</b>, the operation that undoes it. "
        "Subtraction undoes addition, and addition undoes subtraction. Then put your answer back in to check.</p>"
        "<figure class='sn-fig'>" + bar_svg(60, "?", 25) +
        "<figcaption>The two parts make 60. One part is 25, so the other part is 60 − 25 = 35.</figcaption></figure>" +
        table(["Equation", "Do this", "Answer"], [
            [html("?", "+", 25, "=", 60), "60 − 25", "35"],
            [html(80, "−", "?", "=", 35), "80 − 35", "45"],
            [html("?", "−", 15, "=", 40), "40 + 15", "55"],
        ]) +
        ex("Example", html(80, "−", "?", "=", 35),
           "80 take away what leaves 35? Work out 80 − 35 = 45. Check: 80 − 45 = 35.", "45") +
        ex("Example", html("?", "−", 15, "=", 40),
           "The box is the number you start with. Undo − 15 by adding: 40 + 15 = 55. Check: 55 − 15 = 40.", "55") +
        "<h2>Write an equation for a story</h2>"
        "<p>Use a box for the number you do not know. Joining or getting more is +. Taking away or getting off is −.</p>"
        "<figure class='sn-fig'>" + bar_svg(400, 165, "?") +
        "<figcaption>400 students, 165 walk: 165 + □ = 400, so □ = 400 − 165 = 235.</figcaption></figure>" +
        ex("Example", "45 bald eagles sit in the trees. Some fly away. Now 18 are left. How many flew away?",
           "Equation: 45 − □ = 18. Work out 45 − 18 = 27. Check: 45 − 27 = 18.", "27 eagles") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["□ + 25 = 60, so □ = 85 (60 + 25)", "Use the inverse: 60 − 25 = 35"],
            ["□ − 15 = 40, so □ = 25 (40 − 15)", "Undo − 15 by adding: 40 + 15 = 55"],
            ["80 − □ = 35, so □ = 55 (smaller digit from larger)", "Regroup: 80 − 35 = 45"],
            ["8 + 7 = 15 + 5 = 20", "= means “the same as”. Write two equations: 8 + 7 = 15, then 15 + 5 = 20"],
        ])
    )


FAQ = [
    {"q": "What are one-step equations in Grade 3 math in BC?",
     "a": "They are addition and subtraction equations with one unknown number, like □ + 25 = 60 or 80 − □ = 35. The BC Grade 3 Patterning standard asks students to solve them and write them for stories."},
    {"q": "How do you find the missing number in □ + 25 = 60?",
     "a": "Use the inverse operation. Subtraction undoes addition, so □ = 60 − 25 = 35. Check by putting 35 back in: 35 + 25 = 60."},
    {"q": "What does the equal sign mean in Grade 3 math?",
     "a": "The equal sign means “is the same as”, not “the answer is”. Both sides must have the same value, like a level pan balance: 8 + 6 = 10 + 4."},
    {"q": "How can I help my child turn a word problem into an equation?",
     "a": "Ask what number is unknown and put a box there. Joining or getting more is +, taking away is −: “25 cards, gets some more, now 60” is 25 + □ = 60."},
]


def gen_unit():
    rnd = random.Random(53805)
    P = People(rnd)
    sets = [set_balances(P), set_add_unknown(P), set_sub_unknown(P), set_write(P), set_words(P)]
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
        "country": "ca-bc", "subject": "math", "grade": "grade-3", "slug": "one-step-equations", "sort": 5,
        "updated": UPDATED, "pdf_url": "",
        "title": "Grade 3 One-Step Equations",
        "seo_title": "Grade 3 One-Step Equations Worksheets: Free Math with Answer Key (BC Curriculum)",
        "short_title": "One-Step Equations",
        "domain": "Patterning",
        "standard_code": "Grade 3: Patterning",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/3/core",
        "standard_text": "One-step addition and subtraction equations with an unknown number",
        "meta_desc": "Free Grade 3 math worksheets on one-step equations for the BC curriculum: the equal sign as a balance, missing numbers like □ + 25 = 60 and 80 − □ = 35, writing equations for stories and word problems. 100 questions with an answer key.",
        "key_big": "The equal sign means “is the same as”. To find the unknown, use the inverse: subtraction undoes addition.",
        "key_sub": "□ + 25 = 60, so □ = 60 − 25 = 35. □ − 15 = 40, so □ = 40 + 15 = 55. Put the number back in to check.",
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
