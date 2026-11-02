# -*- coding: utf-8 -*-
"""
British Columbia Grade 4 Math: One-Step Equations
(BC Mathematics Curriculum, Grade 4 — Patterning: one-step equations with an unknown number, using all operations)
  python3 tools/gen_cabc_math_g4_equations.py
The equal sign as “the same as” (pan balances), unknowns as boxes and letters with + and − (numbers to 10 000),
unknowns with × and ÷ (4 × □ = 28, n ÷ 3 = 6), writing an equation for a story, and word problems solved
with an equation in BC contexts.
Wrong choices come from real mistakes: reading = as “the answer is” (6 + 4 = □ + 5 -> 10), using the same
operation instead of the inverse (□ + 36 = 90 -> 126, 4 × □ = 28 -> 112, n ÷ 3 = 6 -> 2), subtracting when
dividing is needed (4 × □ = 28 -> 24), smaller-digit-from-larger, forgetting to carry and neighbouring facts.
Every answer is checked in code. HTML attributes use single quotes. Canadian English, BC numbers (10 000).
"""
import json, os, random, re
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-4")
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
    s = expr.replace("−", "-").replace("×", "*").replace(NB, "").replace("$", "")
    s = re.sub(r"(\d+)", r"F(\1)", s).replace("÷", "/")
    return eval(s, {"__builtins__": {}, "F": Fraction})


def holds(eq, ans=None):
    """'□ + 25 = 60' or '4 × n = 28' is true with the unknown = ans."""
    s = re.sub(r"<[^>]+>", "", eq)
    if ans is not None:
        s = s.replace(BOX, str(ans))
        s = re.sub(r"\b[a-z]\b", str(ans), s)
    vals = [val(p.strip()) for p in s.split("=")]
    return all(v == vals[0] for v in vals)


def sfl(a, b):
    """Smaller digit from larger digit in each column: 400 − 150 -> 350 (a typical mistake)."""
    da, db = str(a), str(b).rjust(len(str(a)), "0")
    return int("".join(str(abs(int(x) - int(y))) for x, y in zip(da, db)))


def nocarry(a, b):
    """Add column by column and drop every carried ten: 48 + 35 -> 73."""
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
    """Draw 'a + □' centred at cx: □ drawn as a red box, a single letter in red italics."""
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


def lab(t):
    return t.replace(BOX, "box")


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
                    "pan balance: %s on the left and %s on the right" % (lab(left), lab(right)))


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
    lb = "bar model: whole %s, parts %s and %s" % tuple(lab(tok(v)) for v in vals)
    return svg_wrap(W + 16, 8 + 2 * h + 10 + 8, "".join(s), lb)


def parts_svg(k, part, total):
    """Equal-parts bar: k equal parts, each labelled part, with the total above a bracket.
    part / total are numbers, '?' (box) or a letter."""
    cw = 46 if k <= 5 else 40
    x0, y = 8, 40
    s = []
    for i in range(k):
        s.append("<rect x='%d' y='%d' width='%d' height='36' fill='%s' stroke='%s' stroke-width='2.5'/>"
                 % (x0 + i * cw, y, cw, FILL, GREEN))
        s.append(draw_expr(x0 + i * cw + cw / 2, y + 25, tok(part)))
    x1 = x0 + k * cw
    s.append("<path d='M%d %d v-8 H%d v8' fill='none' stroke='%s' stroke-width='2'/>" % (x0, y - 4, x1, INK))
    s.append(draw_expr((x0 + x1) / 2, y - 16, tok(total)))
    return svg_wrap(x1 + 8, y + 44, "".join(s),
                    "equal parts bar: %d equal parts of %s make %s" % (k, lab(tok(part)), lab(tok(total))))


def mark_large(u, pattern):
    rx = re.compile(r"<svg (?=[^>]*aria-label='(?:" + pattern + "))")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


# ------------------------------------------------------------ distractor lists
def sub_cands(big, small, ans):
    """Answer is big − small. Mistakes: adding instead (same operation), smaller-from-larger, regrouping slips."""
    c = [big + small]
    if sfl(big, small) != ans:
        c.append(sfl(big, small))
    step = 100 if ans >= 1000 else 10
    return c + [ans + step, ans - step, ans + 10, ans - 10, ans + 1, ans - 1]


def add_cands(a, b, ans):
    """Answer is a + b. Mistakes: subtracting instead, forgetting to carry, carry slips."""
    c = [abs(a - b)]
    if nocarry(a, b) != ans:
        c.append(nocarry(a, b))
    step = 100 if ans >= 1000 else 10
    return c + [ans - step, ans + step, ans - 10, ans + 10, ans + 1, ans - 1]


WHAT = "<br>What number goes in the box?"


# ============================================================ set 1: = means "the same as"
def set_same_as(P):
    its = []
    # A. which equation matches the balance
    for l, r, right, wrongs in [
        ("6 + 7", "13", "6 + 7 = 13", ["6 + 7 = 14", "6 = 7 + 13", "13 + 7 = 6"]),
        ("24", "4 × 6", "24 = 4 × 6", ["24 = 4 + 6", "24 × 4 = 6", "4 = 24 × 6"]),
        ("3 × 4", "6 + 6", "3 × 4 = 6 + 6", ["3 × 4 = 12 + 6", "3 + 4 = 6 + 6", "3 × 4 = 6 × 6"]),
        ("20 ÷ 4", "10 − 5", "20 ÷ 4 = 10 − 5", ["20 ÷ 4 = 10 + 5", "20 − 4 = 10 − 5", "20 ÷ 4 = 10 ÷ 5"]),
    ]:
        assert holds(right) and not any(holds(w) for w in wrongs)
        if " " in l and " " in r:
            e = ("The pans balance. %s = %s and %s = %s, so <b>%s</b>. The = sign means “is the same as”."
                 % (l, val(l), r, val(r), right))
        else:
            e = ("The pans balance, so both sides have the same value. The left pan has %s and the right pan has %s, "
                 "so <b>%s</b>. The = sign can sit between any two things that are the same." % (l, r, right))
        its.append(mcq("The pans balance. Which equation matches?" + fig(pan_svg(l, r)), right, wrongs, e))
    # B. balance with a box
    for l, r, ans, wr, e in [
        ("8 × 3", BOX, 24, [11, 5, 27], "The pans balance, so the box has the same value as 8 × 3. 8 × 3 = <b>24</b>. "
         "Not 11: that adds 8 and 3."),
        (BOX, "45 ÷ 5", 9, [40, 50, 225], "The box must be the same as 45 ÷ 5. 45 ÷ 5 = <b>9</b>. "
         "Not 40: that subtracts. Not 225: that multiplies."),
        ("400 − 150", BOX, 250, [550, 350, 240], "400 − 150 = <b>250</b>. Not 550: that adds. "
         "Not 350: that takes the smaller digit from the larger instead of regrouping."),
        (BOX, "6 × 7", 42, [13, 36, 48], "The box is the same as 6 × 7 = <b>42</b>. Not 13: that adds. "
         "Not 36 or 48: those are 6 × 6 and 6 × 8."),
    ]:
        assert val(l if l != BOX else r) == ans
        its.append(mcq("The pans balance." + WHAT + fig(pan_svg(l, r)), ans, wr, e))
    assert sfl(400, 150) == 350
    # C. which equation is true
    prompts = iter(["Which equation is true?", "Which equation is true? The total can come first.",
                    "Work out both sides. Which equation is true?", "Which equation is true? Check both sides."])
    for right, wrongs, e in [
        ("5 × 4 = 10 + 10", ["5 × 4 = 20 + 10", "5 + 4 = 10 + 10", "5 × 4 = 10 × 10"],
         "Work out both sides. 5 × 4 = 20 and 10 + 10 = 20, so <b>5 × 4 = 10 + 10</b> is true. "
         "5 × 4 = 20 + 10 is false: 20 + 10 is 30."),
        ("36 = 9 × 4", ["36 = 9 + 4", "36 = 6 × 7", "9 = 36 × 4"],
         "9 × 4 = 36, so <b>36 = 9 × 4</b> is true. The total can come first, before the = sign. "
         "6 × 7 is 42, not 36."),
        ("18 ÷ 3 = 2 × 3", ["18 ÷ 3 = 15", "18 − 3 = 2 × 3", "18 ÷ 3 = 3 × 3"],
         "18 ÷ 3 = 6 and 2 × 3 = 6, so <b>18 ÷ 3 = 2 × 3</b> is true. Both sides are 6. "
         "18 ÷ 3 = 15 is false: 15 is 18 − 3."),
        ("1000 − 200 = 500 + 300", ["1000 − 200 = 800 + 300", "1000 − 200 = 500 + 200", "1000 + 200 = 500 + 300"],
         "1000 − 200 = 800 and 500 + 300 = 800, so <b>1000 − 200 = 500 + 300</b> is true. "
         "1000 − 200 = 800 + 300 is false: 800 + 300 is 1100, not 800."),
    ]:
        assert holds(right) and not any(holds(w) for w in wrongs)
        its.append(mcq(next(prompts), right, wrongs, e))
    # D. which expression has the same value
    for ex_, right, wrongs in [
        ("2 × 6", "3 × 4", ["2 + 6", "3 × 6", "12 × 6"]),
        ("40 ÷ 5", "4 + 4", ["40 − 5", "4 × 5", "45 ÷ 5"]),
        ("25 + 37", "30 + 32", ["30 + 37", "20 + 32", "62 + 37"]),
        ("9 × 5", "50 − 5", ["9 + 5", "50 − 9", "10 × 4"]),
    ]:
        v = val(ex_)
        assert val(right) == v and all(val(w) != v for w in wrongs)
        e = "%s = %s and %s = %s. They have the same value, so <b>%s = %s</b>." % (ex_, v, right, v, ex_, right)
        its.append(mcq("Which has the same value as %s?" % ex_, right, wrongs, e))
    # E. meaning, = first, and the “answer is” mistake
    its.append(mcq("What does the = sign mean in 3 × 5 = 10 + 5?", "Both sides are the same",
                   ["The answer comes next", "Add all the numbers", "The left side is bigger"],
                   "= means “is the same as”. 3 × 5 = 15 and 10 + 5 = 15, so <b>both sides are the same</b>. "
                   "It does not just mean “the answer comes next”."))
    its.append(mcq(html("?", "=", 7, "×", 8) + WHAT, 56, [15, 54, 64],
                   "The = sign can come first. The box is the same as 7 × 8, so it is <b>56</b>. Not 15: that adds. "
                   "Not 54 or 64: those are 6 × 9 and 8 × 8."))
    assert holds(plain(6, "+", 4, "=", "?", "+", 5), 5)
    its.append(mcq(html(6, "+", 4, "=", "?", "+", 5) + WHAT, 5, [10, 15, 1],
                   "The left side is 6 + 4 = 10. So □ + 5 must also be 10, and □ = <b>5</b>. "
                   "Not 10: that reads = as “the answer is”. Not 15: that adds all the numbers."))
    nm, he, his = P.next()
    its.append(mcq("%s multiplies 4 by 5, then adds 6. %s writes 4 × 5 = 20 + 6 = 26. What is wrong?" % (nm, cap(he)),
                   "4 × 5 is not the same as 20 + 6",
                   ["4 × 5 is not 20", "20 + 6 is not 26", "Nothing is wrong"],
                   "= means both sides are the same. 4 × 5 = 20, but 20 + 6 = 26, so “4 × 5 = 20 + 6” is <b>not true</b>. "
                   "%s should write two equations: 4 × 5 = 20 and 20 + 6 = 26." % nm))
    assert len(its) == 20
    return {"title": "The equal sign means “the same as”", "items": its}


# ============================================================ set 2: unknowns with + and −
def set_add_sub(P):
    its = []

    def add(parts, ans, cands, e, bar=None):
        eq = plain(*parts)
        assert holds(eq, ans), eq
        L = [p for p in parts if isinstance(p, str) and len(p) == 1 and p in LETTERS]
        ask = ". What is <i>%s</i>?" % L[0] if L else WHAT
        q = html(*parts) + ask + (fig(bar_svg(*bar)) if bar else "")
        its.append(mcq(q, ans, cands, e))

    def U(u):
        return "<i>%s</i>" % u if u != "?" else BOX

    def unknown_plus(parts, a, s, u, bar=None):
        ans = s - a
        chk = plain(*[ans if p == u else p for p in parts])
        e = ("Use the inverse. Subtraction undoes addition: %s = %s = <b>%s</b>. Check: %s. "
             "Not %s: that adds, the same operation, instead of subtracting." % (U(u), plain(s, "−", a), n(ans), chk, n(s + a)))
        if sfl(s, a) not in (ans, s + a):
            e += " Not %s: that takes the smaller digit from the larger in each column." % n(sfl(s, a))
        add(parts, ans, sub_cands(s, a, ans), e, bar)

    def unknown_taken(parts, a, r, u, bar=None):
        ans = a - r
        e = ("%s take away what leaves %s? %s = %s = <b>%s</b>. Check: %s. Not %s: that adds the two numbers."
             % (n(a), n(r), U(u), plain(a, "−", r), n(ans), plain(a, "−", ans, "=", r), n(a + r)))
        if sfl(a, r) != ans:
            e += " Not %s: that takes the smaller digit from the larger in each column." % n(sfl(a, r))
        add(parts, ans, sub_cands(a, r, ans), e, bar)

    def unknown_start(parts, a, r, u, bar=None):
        ans = r + a
        e = ("%s is the number you start with. Undo − %s by adding: %s = %s = <b>%s</b>. Check: %s. "
             "Not %s: that subtracts, the same operation, instead of adding."
             % (cap(U(u)) if u != "?" else "The box", n(a), U(u), plain(r, "+", a), n(ans),
                plain(ans, "−", a, "=", r), n(abs(r - a))))
        if nocarry(r, a) != ans:
            e += " Not %s: that forgets to carry." % n(nocarry(r, a))
        add(parts, ans, add_cands(r, a, ans), e, bar)

    unknown_plus(["?", "+", 36, "=", 90], 36, 90, "?")
    unknown_plus(["?", "+", 125, "=", 400], 125, 400, "?", (400, "?", 125))
    unknown_plus(["?", "+", 1250, "=", 3000], 1250, 3000, "?")
    unknown_plus([48, "+", "?", "=", 100], 48, 100, "?")
    unknown_plus([275, "+", "?", "=", 650], 275, 650, "?", (650, 275, "?"))
    unknown_plus([2400, "+", "?", "=", 5000], 2400, 5000, "?")
    unknown_plus(["n", "+", 17, "=", 50], 17, 50, "n")
    unknown_plus([4500, "+", "k", "=", 6000], 4500, 6000, "k")
    unknown_taken([90, "−", "?", "=", 35], 90, 35, "?")
    unknown_taken([500, "−", "?", "=", 260], 500, 260, "?", (500, 260, "?"))
    unknown_taken([3000, "−", "?", "=", 1750], 3000, 1750, "?")
    unknown_taken([64, "−", "y", "=", 29], 64, 29, "y")
    unknown_start(["?", "−", 28, "=", 46], 28, 46, "?")
    unknown_start(["?", "−", 350, "=", 425], 350, 425, "?", ("?", 425, 350))
    unknown_start(["?", "−", 1600, "=", 2400], 1600, 2400, "?")
    unknown_start(["m", "−", 140, "=", 360], 140, 360, "m")
    unknown_start(["p", "−", 1200, "=", 2800], 1200, 2800, "p")
    # = sign first
    add([80, "=", "?", "+", 35], 45, sub_cands(80, 35, 45),
        "The = sign can come first. □ + 35 = 80, so □ = 80 − 35 = <b>45</b>. Check: 45 + 35 = 80. "
        "Not 115: that adds. Not 55: that takes the smaller digit from the larger.")
    assert sfl(80, 35) == 55
    add([600, "=", 900, "−", "n"], 300, [1500, 400, 200],
        "The = sign can come first. 900 − <i>n</i> = 600, so <i>n</i> = 900 − 600 = <b>300</b>. "
        "Check: 900 − 300 = 600. Not 1500: that adds the two numbers.")
    # mistake: same operation instead of the inverse
    nm, he, his = P.next()
    its.append(mcq("%s solves <i>n</i> − 25 = 40 and gets <i>n</i> = 15. What did %s do wrong?" % (nm, he),
                   cap(he) + " subtracted instead of adding",
                   [cap(he) + " added instead of subtracting", cap(he) + " forgot to carry", "Nothing, 15 is right"],
                   "15 − 25 does not give 40. %s used the same operation, <b>subtraction, instead of the inverse</b>. "
                   "Undo − 25 by adding: <i>n</i> = 40 + 25 = 65. Check: 65 − 25 = 40." % cap(he)))
    assert len(its) == 20
    return {"title": "Unknowns with + and −", "items": its}


# ============================================================ set 3: unknowns with × and ÷
def set_mul_div(P):
    its = []

    def Q(parts):
        L = [p for p in parts if isinstance(p, str) and len(p) == 1 and p in LETTERS]
        return html(*parts) + (". What is <i>%s</i>?" % L[0] if L else WHAT)

    def U(parts):
        L = [p for p in parts if isinstance(p, str) and len(p) == 1 and p in LETTERS]
        return "<i>%s</i>" % L[0] if L else BOX

    # a × □ = p  and □ × a = p
    for parts, a, p in [
        ([4, "×", "?", "=", 28], 4, 28), ([6, "×", "?", "=", 54], 6, 54), ([8, "×", "n", "=", 72], 8, 72),
        (["?", "×", 7, "=", 42], 7, 42), (["?", "×", 5, "=", 45], 5, 45), (["k", "×", 3, "=", 24], 3, 24),
        ([9, "×", "?", "=", 63], 9, 63),
    ]:
        ans = p // a
        assert holds(plain(*parts), ans) and ans != a
        chk = plain(*[ans if (p_ == "?" or (isinstance(p_, str) and p_ in LETTERS and len(p_) == 1)) else p_ for p_ in parts])
        e = ("Division undoes multiplication: %s = %s = <b>%d</b>. Check: %s. Not %s: that subtracts. "
             "Not %s: that multiplies, the same operation, instead of dividing." % (U(parts), plain(p, "÷", a), ans, chk, n(p - a), n(p * a)))
        its.append(mcq(Q(parts), ans, [p - a, p * a, ans + 1], e))
    # □ ÷ a = q  (the unknown is the number you start with)
    for parts, a, q in [(["n", "÷", 3, "=", 6], 3, 6), (["?", "÷", 4, "=", 7], 4, 7), (["?", "÷", 9, "=", 6], 9, 6),
                        (["t", "÷", 2, "=", 8], 2, 8)]:
        ans = a * q
        assert holds(plain(*parts), ans)
        wr = []
        why = ""
        if q % a == 0:
            wr.append(q // a)
            why = " Not %d: that divides again, the same operation, instead of multiplying." % (q // a)
        wr += [q + a, q - a, a * (q + 1), a * (q - 1)]
        e = ("%s is the number you start with. Multiplication undoes division: %s = %s = <b>%d</b>. Check: %s.%s"
             % ("The box" if U(parts) == BOX else cap(U(parts)), U(parts), plain(q, "×", a), ans,
                plain(ans, "÷", a, "=", q), why))
        if not why:
            e += " Not %d: that adds the two numbers." % (q + a)
        its.append(mcq(Q(parts), ans, wr, e))
    # p ÷ □ = q
    for parts, p, q in [([56, "÷", "?", "=", 7], 56, 7), ([36, "÷", "n", "=", 4], 36, 4), ([30, "÷", "?", "=", 6], 30, 6)]:
        ans = p // q
        assert holds(plain(*parts), ans)
        e = ("Ask: %d shared into how many groups gives %d in each? %s = %s = <b>%d</b>. Check: %s. "
             "Not %s: that multiplies. Not %s: that subtracts." % (p, q, U(parts), plain(p, "÷", q), ans,
                                                                  plain(p, "÷", ans, "=", q), n(p * q), n(p - q)))
        its.append(mcq(Q(parts), ans, [p * q, p - q, p + q], e))
    # = sign first
    parts = [48, "=", 6, "×", "?"]
    assert holds(plain(*parts), 8)
    its.append(mcq(Q(parts), 8, [42, 288, 9],
                   "The = sign can come first. 6 × □ = 48, so □ = 48 ÷ 6 = <b>8</b>. Check: 6 × 8 = 48. "
                   "Not 42: that subtracts. Not 288: that multiplies."))
    parts = [9, "=", "n", "÷", 7]
    assert holds(plain(*parts), 63)
    its.append(mcq(Q(parts), 63, [16, 2, 56],
                   "The = sign can come first. <i>n</i> ÷ 7 = 9, so <i>n</i> = 9 × 7 = <b>63</b>. Check: 63 ÷ 7 = 9. "
                   "Not 16: that adds. Not 56: that is 8 × 7."))
    # equal-parts bars
    its.append(mcq("The bar shows 4 equal parts that make 32. " + html(4, "×", "?", "=", 32) + WHAT
                   + fig(parts_svg(4, "?", 32)), 8, [28, 128, 36],
                   "4 equal parts make 32, so □ = 32 ÷ 4 = <b>8</b>. Check: 4 × 8 = 32. "
                   "Not 28: that subtracts. Not 128: that multiplies."))
    its.append(mcq("The bar shows 5 equal parts of 9. " + html("n", "÷", 5, "=", 9) + ". What is <i>n</i>?"
                   + fig(parts_svg(5, 9, "n")), 45, [14, 4, 54],
                   "<i>n</i> is the whole. Put the 5 parts together: <i>n</i> = 9 × 5 = <b>45</b>. Check: 45 ÷ 5 = 9. "
                   "Not 14: that adds. Not 4: that subtracts."))
    # tens
    its.append(mcq(Q([7, "×", "?", "=", 70]), 10, [63, 490, 1],
                   "7 × 10 = 70, so □ = 70 ÷ 7 = <b>10</b>. Not 63: that subtracts. Not 490: that multiplies. "
                   "Not 1: 7 × 1 is 7, not 70."))
    assert 7 * 10 == 70
    # mistake
    nm, he, his = P.next()
    its.append(mcq("%s solves <i>n</i> ÷ 6 = 3 and gets <i>n</i> = 2. What did %s do wrong?" % (nm, he),
                   cap(he) + " divided instead of multiplying",
                   [cap(he) + " multiplied instead of dividing", cap(he) + " subtracted instead of adding",
                    "Nothing, 2 is right"],
                   "2 ÷ 6 is not 3. %s used the same operation, <b>division, instead of the inverse</b>. "
                   "Undo ÷ 6 by multiplying: <i>n</i> = 3 × 6 = 18. Check: 18 ÷ 6 = 3." % cap(he)))
    assert len(its) == 20, len(its)
    return {"title": "Unknowns with × and ÷", "items": its}


# ============================================================ set 4: write an equation for a story
def set_write(P):
    its = []

    def match(q, right, wrongs, e, ans):
        assert holds(right, ans), right
        for w in wrongs:
            assert not holds(w, ans), w
        its.append(mcq(q, right, wrongs, e))

    W = "Which equation matches?"
    nm, he, his = P.next()
    match("%s has 28 hockey cards. %s gets some more. Now %s has 64. %s" % (nm, cap(he), he, W),
          plain(28, "+", "?", "=", 64), [plain(28, "+", 64, "=", "?"), plain(64, "+", "?", "=", 28), plain("?", "−", 28, "=", 64)],
          "%s starts with 28, gets an unknown number more and ends with 64: <b>28 + □ = 64</b>. "
          "28 + 64 = □ is wrong: 64 is the total, not a part. Then □ = 64 − 28 = 36." % nm, 36)
    match("There are 45 bald eagles in the trees near Squamish. Some fly away. Now 18 are left. " + W,
          plain(45, "−", "?", "=", 18), [plain(45, "+", 18, "=", "?"), plain("?", "−", 45, "=", 18), plain(18, "−", "?", "=", 45)],
          "Start with 45, take away an unknown number and 18 are left: <b>45 − □ = 18</b>. Then □ = 45 − 18 = 27.", 27)
    match("A box has 6 bags of granola bars. Each bag has the same number of bars, <i>n</i>. There are 48 bars in all. " + W,
          "6 × n = 48", ["6 + n = 48", "n ÷ 6 = 48", "48 × 6 = n"],
          "6 equal groups of <i>n</i> make 48: <b>6 × n = 48</b>. Equal groups mean ×, not +. Then <i>n</i> = 48 ÷ 6 = 8.", 8)
    match("32 students make 4 equal soccer teams. Let <i>t</i> be the number on each team. " + W,
          "32 ÷ 4 = t", ["32 × 4 = t", "t ÷ 4 = 32", "32 − 4 = t"],
          "Sharing 32 into 4 equal teams is division: <b>32 ÷ 4 = t</b>. So <i>t</i> = 8. "
          "32 × 4 = <i>t</i> would make the teams bigger than the class.", 8)
    nm, he, his = P.next()
    match("%s has some money. %s spends $12 at the PNE and has $25 left. %s" % (nm, cap(he), W),
          plain("?", "−", 12, "=", 25), [plain(12, "−", "?", "=", 25), plain(25, "−", 12, "=", "?"), plain("?", "+", 25, "=", 12)],
          "The unknown is the money at the start. Take away $12 and $25 is left: <b>□ − 12 = 25</b>. "
          "Then □ = 25 + 12 = $37. 25 − 12 = □ uses the wrong operation.", 37)
    match("A BC Ferries boat has <i>c</i> cars on it. Then 140 more cars drive on. Now there are 400 cars. " + W,
          "c + 140 = 400", ["c = 140 + 400", "c − 140 = 400", "140 − c = 400"],
          "<i>c</i> cars and 140 more make 400: <b>c + 140 = 400</b>. Then <i>c</i> = 400 − 140 = 260.", 260)
    match("The class puts 56 chairs in 7 equal rows. Let <i>r</i> be the number of chairs in each row. " + W,
          "7 × r = 56", ["7 + r = 56", "r ÷ 7 = 56", "56 × 7 = r"],
          "7 rows of <i>r</i> chairs make 56: <b>7 × r = 56</b>. Then <i>r</i> = 56 ÷ 7 = 8.", 8)
    nm, he, his = P.next()
    match("%s shares some Okanagan cherries equally into 5 bags. Each bag has 9 cherries. Let <i>c</i> be the number "
          "of cherries at the start. %s" % (nm, W),
          "c ÷ 5 = 9", ["c × 5 = 9", "9 ÷ 5 = c", "c − 5 = 9"],
          "Start with <i>c</i>, share into 5 bags and get 9 in each: <b>c ÷ 5 = 9</b>. Then <i>c</i> = 9 × 5 = 45.", 45)
    match("Which equation means “a number times 8 is 64”?",
          "n × 8 = 64", ["n + 8 = 64", "n ÷ 8 = 64", "8 ÷ n = 64"],
          "Let <i>n</i> be the number. “Times 8” is × 8 and “is 64” is = 64: <b>n × 8 = 64</b>. Then <i>n</i> = 8.", 8)
    match("Which equation means “a number divided by 4 is 7”?",
          "n ÷ 4 = 7", ["4 ÷ n = 7", "n × 4 = 7", "n − 4 = 7"],
          "Start with the number <i>n</i> and divide it by 4: <b>n ÷ 4 = 7</b>. Then <i>n</i> = 7 × 4 = 28. "
          "4 ÷ <i>n</i> starts with 4, not with the number.", 28)
    match("Which equation means “a number plus 250 is 900”?",
          "n + 250 = 900", ["n = 250 + 900", "n − 250 = 900", "250 − n = 900"],
          "“Plus 250” is + 250 and “is 900” is = 900: <b>n + 250 = 900</b>. Then <i>n</i> = 900 − 250 = 650.", 650)
    match("A Grade 4 class has raised $320 for the Terry Fox Run. The goal is $500. Let <i>m</i> be the money they still "
          "need. " + W,
          "320 + m = 500", ["320 + 500 = m", "m − 320 = 500", "500 + m = 320"],
          "What they have plus what they still need makes the goal: <b>320 + m = 500</b>. Then <i>m</i> = 500 − 320 = $180.", 180)
    match("Each chair on a ski lift at Whistler holds 4 people. 36 people ride up on <i>c</i> full chairs. " + W,
          "4 × c = 36", ["36 × 4 = c", "c ÷ 4 = 36", "4 + c = 36"],
          "<i>c</i> chairs with 4 people on each make 36: <b>4 × c = 36</b>. Then <i>c</i> = 36 ÷ 4 = 9.", 9)
    match("The library has 1500 books. Some are checked out. 1200 books are still on the shelves. Let <i>b</i> be the "
          "number checked out. " + W,
          "1500 − b = 1200", ["1500 + 1200 = b", "b − 1500 = 1200", "1200 − b = 1500"],
          "Start with 1500, take away <i>b</i>, and 1200 are left: <b>1500 − b = 1200</b>. Then <i>b</i> = 300.", 300)
    nm, he, his = P.next()
    match("%s bakes 3 trays of muffins with 12 muffins on each tray. Let <i>m</i> be the number of muffins in all. %s"
          % (nm, W),
          "3 × 12 = m", ["3 + 12 = m", "12 ÷ 3 = m", "m × 3 = 12"],
          "3 equal trays of 12 is <b>3 × 12 = m</b>. So <i>m</i> = 36. 3 + 12 adds the trays to the muffins.", 36)
    # equation -> story
    its.append(mcq("Which story matches " + html(24, "÷", 6, "=", "?") + "?",
                   "24 apples are shared into 6 bags. How many in each bag?",
                   ["There are 24 apples and 6 more. How many in all?",
                    "There are 6 bags with 24 apples in each. How many in all?",
                    "There are 24 apples and 6 are eaten. How many are left?"],
                   "÷ means sharing into equal groups. Sharing 24 apples into 6 bags is <b>24 ÷ 6 = □</b>, so □ = 4. "
                   "6 bags of 24 would be 6 × 24."))
    its.append(mcq("Which story matches " + html(5, "×", "?", "=", 40) + "?",
                   "5 friends get the same number of stickers. They get 40 in all. How many each?",
                   ["5 friends have 40 stickers each. How many in all?",
                    "Kai has 5 stickers and gets 40 more. How many now?",
                    "Kai has 40 stickers and gives away 5. How many are left?"],
                   "5 equal groups of an unknown number make 40: <b>5 × □ = 40</b>. Then □ = 40 ÷ 5 = 8."))
    match("Which equation means the same as " + html(9, "×", "?", "=", 54) + "?",
          "9 × k = 54", ["k = 9 × 54", "54 × k = 9", "9 + k = 54"],
          "A letter can take the place of the box. Both stand for the same unknown number: <b>9 × k = 54</b>. "
          "In both, the unknown is 6.", 6)
    nm, he, his = P.next()
    match("“48 crayons are shared equally into 6 boxes.” %s writes 48 + 6 = □. Which equation should %s write?" % (nm, he),
          plain(48, "÷", 6, "=", "?"), [plain(48, "×", 6, "=", "?"), plain(48, "−", 6, "=", "?"), plain(6, "÷", 48, "=", "?")],
          "Shared equally means divide, with the total first: <b>48 ÷ 6 = □</b>. So □ = 8 crayons in each box.", 8)
    nm1, he1, his1 = P.next()
    nm2, he2, his2 = P.next()
    match("%s has 3 bags of 8 marbles. %s has 4 bags with the same number in each bag. They have the same number of "
          "marbles. %s" % (nm1, nm2, W),
          plain(3, "×", 8, "=", 4, "×", "?"), [plain(3, "×", 8, "=", "?"), plain(3, "×", 4, "=", 8, "×", "?"),
                                              plain(3, "+", 8, "=", 4, "+", "?")],
          "Both totals are the same, so both sides are equal: <b>3 × 8 = 4 × □</b>. 3 × 8 = 24, so □ = 24 ÷ 4 = 6 marbles.", 6)
    assert len(its) == 20, len(its)
    return {"title": "Write an equation for a story", "items": its}


# ============================================================ set 5: word problems
def set_words(P):
    its = []

    def solve(q, parts, ans, cands, e, unit="", money=False, pic=None):
        eq = plain(*parts)
        assert holds(eq, ans), eq
        if money:
            f = lambda v: "$" + n(v)
        else:
            f = lambda v: n(v) + unit
        cs = [f(c) for c in cands if c > 0]
        its.append(mcq(q + (fig(pic) if pic else ""), f(ans), cs, "Equation: %s. %s" % (html(*parts), e)))

    def mul_e(a, p, ans, what):
        return ("Use the inverse: %s ÷ %d = <b>%d</b> %s. Check: %d × %d = %d. Not %d: that subtracts. "
                "Not %d: that multiplies instead of dividing." % (n(p), a, ans, what, a, ans, p, p - a, p * a))

    # 1
    solve("A fish counter on a creek on Vancouver Island counts 245 salmon by Monday. By Tuesday the total is 610. "
          "How many salmon swam by on Tuesday?",
          [245, "+", "?", "=", 610], 365, sub_cands(610, 245, 365),
          "□ = 610 − 245 = <b>365</b> salmon. Check: 245 + 365 = 610. Not 855: that adds. "
          "Not 435: that takes the smaller digit from the larger in each column.")
    assert sfl(610, 245) == 435
    # 2
    solve("A Grade 4 class has raised $185 for the Terry Fox Run. The goal is $400. How much more do they need to raise?",
          [185, "+", "?", "=", 400], 215, sub_cands(400, 185, 215),
          "□ = 400 − 185 = <b>$215</b>. Check: $185 + $215 = $400. Not $585: that adds. "
          "Not $385: that takes the smaller digit from the larger in each column.", money=True,
          pic=bar_svg(400, 185, "?"))
    # 3
    nm, he, his = P.next()
    solve("%s’s soccer team shares 54 orange slices equally. There are 9 players. How many slices does each player get?" % nm,
          [9, "×", "?", "=", 54], 6, [45, 486, 7], mul_e(9, 54, 6, "slices"))
    # 4
    solve("42 students go on a field trip to Stanley Park. Each van holds 7 students. All the vans are full. "
          "How many vans do they need?",
          [7, "×", "v", "=", 42], 6, [35, 294, 7], mul_e(7, 42, 6, "vans"))
    # 5
    solve("A class visits the Vancouver Aquarium. The teacher splits the students into 4 equal groups. "
          "There are 8 students in each group. How many students are in the class?",
          ["n", "÷", 4, "=", 8], 32, [2, 12, 4],
          "Undo ÷ 4 by multiplying: <i>n</i> = 8 × 4 = <b>32</b> students. Check: 32 ÷ 4 = 8. "
          "Not 2: that divides again instead of multiplying. Not 12: that adds.")
    # 6
    solve("A ferry can carry 310 cars. 185 cars are already on the ferry. How many more cars can fit?",
          [185, "+", "?", "=", 310], 125, sub_cands(310, 185, 125),
          "□ = 310 − 185 = <b>125</b> cars. Check: 185 + 125 = 310. Not 495: that adds. "
          "Not 275: that takes the smaller digit from the larger in each column.")
    assert sfl(310, 185) == 275
    # 7
    solve("A ski hill sells 1250 lift tickets in the morning. By the end of the day it has sold 2000. "
          "How many tickets did it sell in the afternoon?",
          [1250, "+", "?", "=", 2000], 750, sub_cands(2000, 1250, 750),
          "□ = 2000 − 1250 = <b>750</b> tickets. Check: 1250 + 750 = 2000. Not 3250: that adds. "
          "Not 1250: that takes the smaller digit from the larger in each column.")
    assert sfl(2000, 1250) == 1250 and sfl(400, 185) == 385
    # 8
    nm, he, his = P.next()
    solve("%s has some stickers. %s gives 35 to friends and has 48 left. How many stickers did %s have at the start?"
          % (nm, cap(he), he),
          ["?", "−", 35, "=", 48], 83, add_cands(48, 35, 83),
          "Undo − 35 by adding: □ = 48 + 35 = <b>83</b>. Check: 83 − 35 = 48. "
          "Not 13: that subtracts. Not 73: that forgets to carry the ten.")
    assert nocarry(48, 35) == 73
    # 9
    nm, he, his = P.next()
    solve("%s reads 8 pages each day. How many days will it take %s to read 72 pages?" % (nm, "her" if he == "she" else "him"),
          [8, "×", "d", "=", 72], 9, [64, 576, 8], mul_e(8, 72, 9, "days"))
    # 10
    nm, he, his = P.next()
    solve("%s plants 56 cedar seedlings in 8 equal rows. How many seedlings are in each row?" % nm,
          [8, "×", "r", "=", 56], 7, [48, 448, 8], mul_e(8, 56, 7, "seedlings"))
    # 11
    nm, he, his = P.next()
    solve("The Grouse Grind trail on Grouse Mountain is about 2900 m long. %s has hiked 1700 m. "
          "About how many more metres does %s have to hike?" % (nm, he),
          [1700, "+", "?", "=", 2900], 1200, [4600, 1300, 1100],
          "□ = 2900 − 1700 = <b>1200</b> m. Check: 1700 + 1200 = 2900. Not 4600: that adds. "
          "Not 1300 or 1100: count on from 1700 to 2000 (300), then to 2900 (900). 300 + 900 = 1200.", unit=" m")
    # 12
    solve("A whale-watching boat in Victoria has 48 seats. 29 people are on the boat. How many seats are empty?",
          [29, "+", "?", "=", 48], 19, [77, 21, 29],
          "□ = 48 − 29 = <b>19</b> seats. Check: 29 + 19 = 48. Not 77: that adds. "
          "Not 21: that takes the smaller digit from the larger.")
    assert sfl(48, 29) == 21
    # 13
    nm, he, his = P.next()
    solve("%s buys 4 rolls of hockey tape. Each roll costs the same. %s pays $12. How much does each roll cost?"
          % (nm, cap(he)),
          [4, "×", "?", "=", 12], 3, [8, 48, 16],
          "Use the inverse: □ = 12 ÷ 4 = <b>$3</b>. Check: 4 × $3 = $12. Not $8: that subtracts. "
          "Not $48: that multiplies.", money=True)
    # 14
    solve("A toonie is worth $2. How many toonies make $16?",
          [2, "×", "t", "=", 16], 8, [14, 32, 18],
          "Use the inverse: <i>t</i> = 16 ÷ 2 = <b>8</b> toonies. Check: 8 × $2 = $16. Not 14: that subtracts. "
          "Not 32: that multiplies.")
    # 15
    solve("6 friends share some granola bars equally. Each friend gets 3 bars. How many granola bars were there?",
          ["b", "÷", 6, "=", 3], 18, [2, 9, 24],
          "Undo ÷ 6 by multiplying: <i>b</i> = 3 × 6 = <b>18</b> bars. Check: 18 ÷ 6 = 3. "
          "Not 2: that divides 6 by 3. Not 9: that adds.")
    # 16
    nm, he, his = P.next()
    solve("%s’s family drives about 390 km from Vancouver to Kelowna. They have driven 240 km. "
          "How far do they still have to drive?" % nm,
          [240, "+", "?", "=", 390], 150, [630, 160, 140],
          "□ = 390 − 240 = <b>150</b> km. Check: 240 + 150 = 390. Not 630: that adds instead of subtracting.",
          unit=" km", pic=bar_svg(390, 240, "?"))
    # 17
    nm, he, his = P.next()
    solve("%s cuts a 45 cm ribbon into 5 equal pieces. How long is each piece?" % nm,
          [5, "×", "?", "=", 45], 9, [40, 225, 8],
          "Use the inverse: □ = 45 ÷ 5 = <b>9</b> cm. Check: 5 × 9 = 45. Not 40: that subtracts. "
          "Not 225: that multiplies.", unit=" cm", pic=parts_svg(5, "?", 45))
    # 18
    nm, he, his = P.next()
    solve("%s needs 80 juice boxes for Sports Day. They come in packs of 10. How many packs does %s need?" % (nm, he),
          [10, "×", "p", "=", 80], 8, [70, 800, 90],
          "Use the inverse: <i>p</i> = 80 ÷ 10 = <b>8</b> packs. Check: 10 × 8 = 80. Not 70: that subtracts. "
          "Not 800: that multiplies.")
    # 19
    nm, he, his = P.next()
    solve("%s scores some points in the first half of a basketball game and 18 points in the second half. "
          "%s scores 45 points in all. How many points did %s score in the first half?" % (nm, cap(he), he),
          ["n", "+", 18, "=", 45], 27, sub_cands(45, 18, 27),
          "<i>n</i> = 45 − 18 = <b>27</b> points. Check: 27 + 18 = 45. Not 63: that adds. "
          "Not 33: that takes the smaller digit from the larger.")
    assert sfl(45, 18) == 33
    # 20
    solve("A school wants to collect 2500 cans for the food bank. So far it has 1750 cans. How many more cans does it need?",
          [1750, "+", "?", "=", 2500], 750, sub_cands(2500, 1750, 750),
          "□ = 2500 − 1750 = <b>750</b> cans. Check: 1750 + 750 = 2500. Not 4250: that adds. "
          "Not 1250: that takes the smaller digit from the larger.")
    assert sfl(2500, 1750) == 1250
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
        "<figure class='sn-fig'>" + pan_svg("2 × 6", "8 + 4") +
        "<figcaption>2 × 6 = 12 and 8 + 4 = 12. The pans balance, so 2 × 6 = 8 + 4.</figcaption></figure>"
        "<h2>Find the unknown: use the inverse</h2>"
        "<p>A box □ or a letter like <i>n</i> stands for an <b>unknown</b> number. "
        "To find it, use the <b>inverse</b> operation, the one that undoes it. "
        "Then put your answer back in to check.</p>" +
        table(["Equation", "Undo it with", "Do this", "Answer"], [
            [html("?", "+", 36, "=", 90), "−", "90 − 36", "54"],
            [html("?", "−", 28, "=", 46), "+", "46 + 28", "74"],
            [html(4, "×", "?", "=", 28), "÷", "28 ÷ 4", "7"],
            [html("n", "÷", 3, "=", 6), "×", "6 × 3", "<i>n</i> = 18"],
        ]) +
        "<figure class='sn-fig'>" + parts_svg(4, "?", 28) +
        "<figcaption>4 equal parts make 28: 4 × □ = 28, so □ = 28 ÷ 4 = 7.</figcaption></figure>" +
        ex("Example", html("n", "÷", 3, "=", 6),
           "<i>n</i> is the number you start with. Undo ÷ 3 by multiplying: 6 × 3 = 18. Check: 18 ÷ 3 = 6.",
           "<i>n</i> = 18") +
        ex("Example", html(2400, "+", "?", "=", 5000),
           "Undo + 2400 by subtracting: 5000 − 2400 = 2600. Check: 2400 + 2600 = 5000.", "2600") +
        "<h2>Write an equation for a story</h2>"
        "<p>Use a box or a letter for the number you do not know. Joining is +, taking away is −, "
        "equal groups are ×, and sharing equally is ÷.</p>"
        "<figure class='sn-fig'>" + bar_svg(400, 185, "?") +
        "<figcaption>$185 raised, goal $400: 185 + □ = 400, so □ = 400 − 185 = 215.</figcaption></figure>" +
        ex("Example", "56 chairs are put in 7 equal rows. How many chairs are in each row?",
           "Equation: 7 × <i>r</i> = 56. Use the inverse: <i>r</i> = 56 ÷ 7 = 8. Check: 7 × 8 = 56.", "8 chairs") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["6 + 4 = □ + 5, so □ = 10", "10 is the left side. □ + 5 = 10, so □ = 5"],
            ["□ + 36 = 90, so □ = 126 (90 + 36)", "Use the inverse: 90 − 36 = 54"],
            ["4 × □ = 28, so □ = 112 (28 × 4)", "Use the inverse: 28 ÷ 4 = 7"],
            ["<i>n</i> ÷ 3 = 6, so <i>n</i> = 2 (6 ÷ 3)", "Undo ÷ 3 by multiplying: 6 × 3 = 18"],
            ["4 × □ = 28, so □ = 24 (28 − 4)", "× is undone by ÷, not by −"],
            ["4 × 5 = 20 + 6 = 26", "Write two equations: 4 × 5 = 20, then 20 + 6 = 26"],
        ])
    )


FAQ = [
    {"q": "What are one-step equations in Grade 4 math in BC?",
     "a": "They are equations like □ + 36 = 90, 4 × □ = 28 or n ÷ 3 = 6 with one unknown number. The BC Grade 4 Patterning standard asks students to solve them using all four operations."},
    {"q": "How do you solve 4 × □ = 28?",
     "a": "Use the inverse operation. Division undoes multiplication, so □ = 28 ÷ 4 = 7. Check by putting 7 back in: 4 × 7 = 28."},
    {"q": "What does the equal sign mean in Grade 4 math?",
     "a": "The equal sign means “is the same as”, not “the answer is”. In 6 + 4 = □ + 5, both sides must be 10, so the box is 5."},
    {"q": "Are equations on the Grade 4 FSA?",
     "a": "The FSA numeracy section checks math skills and problem solving from the BC curriculum. Writing and solving simple equations for word problems, like the ones here, is good practice for it."},
]


def gen_unit():
    rnd = random.Random(34808)
    P = People(rnd)
    sets = [set_same_as(P), set_add_sub(P), set_mul_div(P), set_write(P), set_words(P)]
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
        "country": "ca-bc", "subject": "math", "grade": "grade-4", "slug": "one-step-equations", "sort": 8,
        "updated": UPDATED, "pdf_url": "",
        "title": "Grade 4 One-Step Equations",
        "seo_title": "Grade 4 One-Step Equations Worksheets: Free Math with Answer Key (BC Curriculum)",
        "short_title": "One-Step Equations",
        "domain": "Patterning",
        "standard_code": "Grade 4: Patterning",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/4/core",
        "standard_text": "One-step equations with an unknown number, using all operations",
        "meta_desc": "Free Grade 4 math worksheets on one-step equations for the BC curriculum: the equal sign as a balance, unknowns like □ + 36 = 90, 4 × □ = 28 and n ÷ 3 = 6, writing equations for stories and word problems. 100 questions with an answer key, good FSA practice.",
        "key_big": "Use the inverse to find the unknown: subtraction undoes addition, and division undoes multiplication.",
        "key_sub": "4 × □ = 28, so □ = 28 ÷ 4 = 7. n ÷ 3 = 6, so n = 6 × 3 = 18. The = sign means “is the same as”.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen_unit()
    mark_large(u, "bar model|pan balance|equal parts bar")
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(u, f, ensure_ascii=False, indent=1)
    print("wrote", path)
