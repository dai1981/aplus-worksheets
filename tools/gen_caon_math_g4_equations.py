# -*- coding: utf-8 -*-
"""
Canada (Ontario) Grade 4 Math: Equations and Inequalities
(Ontario Curriculum, Grades 1–8: Mathematics, 2020 — Algebra C2.1, C2.2, C2.3)
  python3 tools/gen_caon_math_g4_equations.py
Letters as unknowns and pan balances (C2.1), one-step equations with whole numbers up to 50 such as
n + 8 = 23 and 4 × n = 36 (C2.2), checking (verifying) a solution, inequalities with + and − up to 20
such as n + 5 < 12, solved, checked and graphed with dots on a number line (C2.3), and word problems.
Wrong choices come from real mistakes: doing the same operation instead of the inverse (n + 8 = 23 -> 31),
taking the smaller digit from the larger in each column, forgetting to carry, mixing up < and >,
putting a dot on the boundary number (n < 7 includes 7), treating an inequality as an equation (n = 7),
reading = as “the answer is”, and thinking the letter n means the number 14 (its place in the alphabet).
Every answer is checked in code. HTML attributes use single quotes. Canadian English.
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-4")
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
M = "−"
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
    s = expr.replace(M, "-").replace(NB, "").replace("×", "*").replace("÷", "/")
    return eval(s, {"__builtins__": {}})


def holds(eq, ans=None):
    """'n + 8 = 23' is true with n = ans. Also works for &lt; and &gt;."""
    s = re.sub(r"<[^>]+>", "", eq).replace("&lt;", "<").replace("&gt;", ">")
    if ans is not None:
        s = s.replace(BOX, str(ans))
        s = re.sub(r"\b[a-z]\b", str(ans), s)
    for rel in ("<", ">"):
        if rel in s:
            a, b = s.split(rel)
            return val(a) < val(b) if rel == "<" else val(a) > val(b)
    vals = [val(p.strip()) for p in s.split("=")]
    return all(v == vals[0] for v in vals)


def sols(ineq, lo=0, hi=60):
    return [x for x in range(lo, hi + 1) if holds(ineq, x)]


def sfl(a, b):
    """Smaller digit from larger digit in each column: 45 − 18 -> 33 (a typical mistake)."""
    da, db = str(a), str(b).rjust(len(str(a)), "0")
    return int("".join(str(abs(int(x) - int(y))) for x, y in zip(da, db)))


def nocarry(a, b):
    """Add column by column and drop every carried ten: 27 + 9 -> 26."""
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
        if c in seen or not c:
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


def I(v="n"):
    return "<i>%s</i>" % v


def ineq(*parts):
    """Inequality for HTML: '<' / '>' become entities, the letter in italics."""
    return html(*["&lt;" if p == "<" else "&gt;" if p == ">" else p for p in parts])


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
    """Draw 'n + 9' centred at cx; a single letter in red italics, □ as a red box."""
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


def stand(s, cl, cr, wr, py):
    mid = (cl + cr) / 2
    by = py + 24
    s.append("<rect x='%.1f' y='%d' width='%.1f' height='6' fill='%s'/>" % (cl - 2, by, cr - cl + 4, INK))
    s.append("<path d='M%.1f %d L%.1f %d L%.1f %d Z' fill='%s'/>" % (mid, by + 6, mid - 22, by + 40, mid + 22, by + 40, GREEN))
    s.append("<rect x='%.1f' y='%d' width='80' height='5' fill='%s'/>" % (mid - 40, by + 40, INK))
    return cr + wr / 2 + 8, by + 47


def pan_svg(left, right):
    """A level pan balance with an expression on each pan (a letter or □ allowed)."""
    def box_w(t):
        return max(90, int(expr_w(t) + 24))
    wl, wr = box_w(left), box_w(right)
    cl = 8 + wl / 2
    cr = cl + wl / 2 + 40 + wr / 2
    top, ih = 8, 36
    py = top + ih
    s = []
    for t, c, w in ((left, cl, wl), (right, cr, wr)):
        s.append("<rect x='%.1f' y='%d' width='%d' height='%d' rx='6' fill='%s' stroke='%s' stroke-width='2'/>"
                 % (c - w / 2, top, w, ih, GREY, INK))
        s.append(draw_expr(c, top + 25, t))
        s.append("<rect x='%.1f' y='%d' width='%d' height='6' fill='%s'/>" % (c - w / 2, py, w, INK))
        s.append("<rect x='%.1f' y='%d' width='4' height='18' fill='%s'/>" % (c - 2, py + 6, INK))
    W, H = stand(s, cl, cr, wr, py)
    return svg_wrap(W, H, "".join(s),
                    "pan balance: %s on the left and %s on the right" % (left.replace(BOX, "box"), right.replace(BOX, "box")))


def blocks_svg(k, letter, total):
    """Pan balance: k equal blocks (each the letter) on the left, a weight of total on the right."""
    bw, gap = 32, 6
    tot_w = k * bw + gap * (k - 1)
    wl = max(80, tot_w + 16)
    wr = max(80, int(len(str(total)) * 10 + 30))
    cl = 8 + wl / 2
    cr = cl + wl / 2 + 44 + wr / 2
    top, ih = 10, 34
    py = top + ih
    s = []
    x = cl - tot_w / 2
    for _ in range(k):
        s.append("<rect x='%.1f' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='2'/>" % (x, top, bw, ih, FILL, GREEN))
        s.append("<text x='%.1f' y='%d' font-size='18' font-weight='700' font-style='italic' fill='%s' text-anchor='middle'>%s</text>"
                 % (x + bw / 2, top + 24, RED, letter))
        x += bw + gap
    s.append("<rect x='%.1f' y='%d' width='%d' height='%d' rx='6' fill='%s' stroke='%s' stroke-width='2'/>"
             % (cr - (wr - 16) / 2, top, wr - 16, ih, GREY, INK))
    s.append("<text x='%.1f' y='%d' font-size='18' font-weight='700' fill='%s' text-anchor='middle'>%d</text>" % (cr, top + 24, INK, total))
    for c, w in ((cl, wl), (cr, wr)):
        s.append("<rect x='%.1f' y='%d' width='%d' height='6' fill='%s'/>" % (c - w / 2, py, w, INK))
        s.append("<rect x='%.1f' y='%d' width='4' height='18' fill='%s'/>" % (c - 2, py + 6, INK))
    W, H = stand(s, cl, cr, wr, py)
    return svg_wrap(W, H, "".join(s), "pan balance: %d blocks %s on the left and %d on the right" % (k, letter, total))


def bar_svg(whole, p1, p2):
    """Part-part-whole bar model, drawn to scale. Values are numbers or a letter."""
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
    lab = "bar model: whole %s, parts %s and %s" % tuple(tok(v) for v in vals)
    return svg_wrap(W + 16, 8 + 2 * h + 10 + 8, "".join(s), lab)


NGAP, NPAD = 28, 22


def dots_svg(lo, hi, dots, more=False, label="number line graph"):
    """Whole-number line lo..hi. A green dot on each number in dots. more=True adds a green arrow
    after hi: the dots keep going."""
    W = 2 * NPAD + NGAP * (hi - lo) + 34
    Y, H = 22, 54
    X = lambda v: NPAD + NGAP * (v - lo)
    L = X(lo) - (14 if lo > 0 else 8)
    R = W - 6
    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.8'/>" % (L + (2 if lo > 0 else 0), Y, R - 2, Y, INK),
         "<path d='M%d %d L%d %d L%d %d Z' fill='%s'/>" % (R, Y, R - 9, Y - 5, R - 9, Y + 5, INK)]
    if lo > 0:
        s.append("<path d='M%d %d L%d %d L%d %d Z' fill='%s'/>" % (L, Y, L + 9, Y - 5, L + 9, Y + 5, INK))
    for v in range(lo, hi + 1):
        x = X(v)
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.6'/>" % (x, Y - 6, x, Y + 6, INK))
        s.append("<text x='%d' y='%d' font-size='15' fill='%s' text-anchor='middle'>%d</text>" % (x, Y + 26, INK, v))
    if more:
        x0 = X(hi) + 9
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='4'/>" % (x0, Y - 13, R - 10, Y - 13, GREEN))
        s.append("<path d='M%d %d L%d %d L%d %d Z' fill='%s'/>" % (R, Y - 13, R - 10, Y - 19, R - 10, Y - 7, GREEN))
    for v in dots:
        assert lo <= v <= hi
        s.append("<circle cx='%d' cy='%d' r='7' fill='%s'/>" % (X(v), Y, GREEN))
    return svg_wrap(W, H, "".join(s), label)


def graph_of(ineq_plain, lo, hi):
    """Graph the whole-number solutions of an inequality in the window lo..hi."""
    ss = sols(ineq_plain, 0, 200)
    shown = [x for x in ss if lo <= x <= hi]
    more = any(x > hi for x in ss)
    if not more:
        assert all(x >= lo for x in ss), ineq_plain
    return shown, more


def mark_large(u, pattern):
    rx = re.compile(r"<svg (?=[^>]*aria-label='(?:" + pattern + "))")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


# ------------------------------------------------------------ distractor lists
def sub_cands(big, small, ans):
    """Answer is big − small. Mistakes: adding instead, smaller-from-larger, regrouping slips."""
    return [big + small, sfl(big, small), ans + 10, ans - 10, ans + 1, ans - 1]


def add_cands(a, b, ans):
    """Answer is a + b. Mistakes: subtracting instead, forgetting to carry, slips."""
    return [abs(a - b), nocarry(a, b), ans + 10, ans - 10, ans + 1, ans - 1]


def why_sub(big, small, ans):
    """Notes for the subtraction mistakes that appear as choices."""
    out = " Not %s: that adds instead of subtracting." % n(big + small)
    if sfl(big, small) != ans:
        out += " Not %s: that takes the smaller digit from the larger in each column." % n(sfl(big, small))
    return out


# ============================================================ set 1: balances and letters
def set_letters(P):
    its = []
    # A. which equation matches the balance
    for svg, right, wrongs, v, e in [
        (pan_svg("n + 6", "14"), "n + 6 = 14", ["n + 14 = 6", "n − 6 = 14", "6 + 14 = n"], 8,
         "The pans balance, so both sides have the same value: <b>n + 6 = 14</b>. The letter <i>n</i> stands for the "
         "unknown number. (<i>n</i> = 8, because 8 + 6 = 14.)"),
        (blocks_svg(3, "n", 15), "3 × n = 15", ["n + 3 = 15", "3 + 15 = n", "n = 15 × 3"], 5,
         "There are 3 blocks, and each block is <i>n</i>. 3 blocks are 3 × <i>n</i>, so <b>3 × n = 15</b>. "
         "Not <i>n</i> + 3: the 3 tells how many blocks, not a mass of 3. (<i>n</i> = 5.)"),
        (pan_svg("20", "k + 12"), "20 = k + 12", ["20 + 12 = k", "k − 12 = 20", "k = 20 + 12"], 8,
         "The left pan has 20 and the right pan has <i>k</i> + 12, so <b>20 = k + 12</b>. The = sign can have "
         "the unknown on either side. (<i>k</i> = 8.)"),
        (pan_svg("y − 5", "9"), "y − 5 = 9", ["y + 5 = 9", "5 − y = 9", "y = 9 − 5"], 14,
         "The left pan has <i>y</i> − 5 and the right pan has 9, so <b>y − 5 = 9</b>. "
         "5 − <i>y</i> starts with 5, not with <i>y</i>. (<i>y</i> = 14.)"),
    ]:
        assert holds(right, v) and not any(holds(w, v) for w in wrongs)
        its.append(mcq("The pans balance. Which equation matches?" + fig(svg), right, wrongs, e))
    # B. balance -> value of the letter
    for svg, eq, v, cands, e in [
        (pan_svg("n + 9", "17"), "n + 9 = 17", 8, [26, 9, 7],
         "<i>n</i> + 9 = 17. Use the inverse: <i>n</i> = 17 − 9 = <b>8</b>. Check: 8 + 9 = 17. "
         "Not 26: that adds 9 instead of taking it away."),
        (blocks_svg(4, "n", 20), "4 × n = 20", 5, [16, 24, 80],
         "4 equal blocks balance 20, so 4 × <i>n</i> = 20. Share 20 into 4 equal parts: <i>n</i> = 20 ÷ 4 = <b>5</b>. "
         "Check: 4 × 5 = 20. Not 16: that subtracts 4. Not 24: that adds 4. Not 80: that multiplies."),
        (pan_svg("25", "m + 18"), "25 = m + 18", 7, [43, 13, 8],
         "<i>m</i> + 18 = 25, so <i>m</i> = 25 − 18 = <b>7</b>. Check: 7 + 18 = 25. Not 43: that adds. "
         "Not 13: that takes the smaller digit from the larger (8 − 5 instead of 15 − 8)."),
        (pan_svg("p − 7", "12"), "p − 7 = 12", 19, [5, 18, 20],
         "<i>p</i> − 7 = 12. Undo − 7 by adding 7: <i>p</i> = 12 + 7 = <b>19</b>. Check: 19 − 7 = 12. "
         "Not 5: that subtracts 7 again instead of adding."),
    ]:
        assert holds(eq, v) and sfl(25, 18) == 13
        L = [c for c in eq if c in LETTERS][0]
        its.append(mcq("The pans balance. What is <i>%s</i>?" % L + fig(svg), v, cands, e))
    # C. symbols as variables
    its.append(mcq("In " + html(7, "+", "n", "=", 15) + ", what does the letter <i>n</i> stand for?",
                   "An unknown number", ["The number 14", "Any number you like", "The word “number”"],
                   "A letter in an equation stands for an <b>unknown number</b>. Here <i>n</i> = 8, because 7 + 8 = 15. "
                   "It is not 14 (n is the 14th letter of the alphabet), and it is not just any number: only 8 works."))
    for words, right, wrongs, v in [
        ("a number plus 9 is 21", "n + 9 = 21", ["n = 9 + 21", "9 − n = 21", "n + 21 = 9"], 12),
        ("6 times a number is 42", "6 × n = 42", ["6 + n = 42", "n = 6 × 42", "n ÷ 6 = 42"], 7),
        ("a number take away 8 is 30", "n − 8 = 30", ["8 − n = 30", "n + 8 = 30", "n = 8 − 30"], 38),
        ("a number divided by 5 is 7", "n ÷ 5 = 7", ["5 ÷ n = 7", "n × 5 = 7", "n − 5 = 7"], 35),
    ]:
        assert holds(right, v) and not any(holds(w, v) for w in wrongs)
        op = right.split(" ")[1]
        e = ("Let <i>n</i> be the number. “%s” is <b>%s</b>. Then <i>n</i> = %d." % (words, right, v))
        if op == "−":
            e += " 8 − <i>n</i> starts with 8, not with the number."
        if op == "÷":
            e += " 5 ÷ <i>n</i> divides 5, not the number."
        its.append(mcq("Which equation means “%s”?" % words, right, wrongs, e))
    its.append(mcq(html("m", "+", 6, "=", 6, "+", 13) + ". What is <i>m</i>?", 13, [19, 7, 25],
                   "You can add in any order: 13 + 6 = 6 + 13. So <i>m</i> = <b>13</b>. "
                   "Not 19: that is the value of the right side, 6 + 13. Not 7: that is 13 − 6."))
    for v, right, wrongs in [
        (7, "n + 8 = 15", ["n + 8 = 16", "n − 3 = 5", "3 × n = 24"]),
        (6, "5 × y = 30", ["5 + y = 30", "y + 6 = 13", "y − 2 = 3"]),
    ]:
        L = right[0] if right[0] in LETTERS else right[4]
        assert holds(right, v) and not any(holds(w, v) for w in wrongs)
        lhs = right.split(" = ")[0]
        e = "Put %d in place of <i>%s</i>. %s = %d, so <b>%s</b> is true." % (
            v, L, lhs.replace(L, str(v)), val(lhs.replace(L, str(v))), right)
        its.append(mcq("Which equation is true when <i>%s</i> = %d?" % (L, v), right, wrongs, e))
    its.append(mcq("What is the value of " + html("k", "+", 9) + " when <i>k</i> = 4?", 13, [5, 36, 14],
                   "Put 4 in place of <i>k</i>: 4 + 9 = <b>13</b>. Not 5: that subtracts. Not 36: that multiplies."))
    its.append(mcq("What is the value of 7 × <i>n</i> when <i>n</i> = 6?", 42, [13, 76, 1],
                   "7 × <i>n</i> means 7 times <i>n</i>. Put 6 in place of <i>n</i>: 7 × 6 = <b>42</b>. "
                   "Not 76: the 7 and the 6 are not written side by side. Not 13: that adds. Not 1: that subtracts."))
    its.append(mcq("The pans balance. What is <i>a</i>?" + fig(pan_svg("a + 10", "30 + 5")), 25, [35, 45, 20],
                   "The right side is 30 + 5 = 35. So <i>a</i> + 10 = 35, and <i>a</i> = 35 − 10 = <b>25</b>. "
                   "Not 35: that is the value of the right side. Not 20: that forgets the 5. Not 45: that adds 10."))
    assert holds("a + 10 = 30 + 5", 25)
    nm1, he1, _ = P.next()
    nm2, he2, _ = P.next()
    its.append(mcq("%s writes 3 × <i>n</i> = 24. %s writes 3 × <i>k</i> = 24. What is true?" % (nm1, nm2),
                   "n and k are both 8", ["n is 8 and k is 11", "Only n can be used", "n and k are both 21"],
                   "Any letter can stand for the unknown. In both equations 3 × 8 = 24, so <b><i>n</i> and <i>k</i> are both 8</b>. "
                   "The letter is just a name. It does not change the number. Not 21: that subtracts 3."))
    assert holds("3 × n = 24", 8)
    assert len(its) == 20
    return {"title": "Balances and letters for unknowns", "items": its}


# ============================================================ set 2: solve equations
WHATN = " What is <i>%s</i>?"


def set_solve():
    its = []

    def add(parts, ans, cands, e, pic=None):
        eq = plain(*parts)
        assert holds(eq, ans), eq
        L = [p for p in parts if isinstance(p, str) and len(p) == 1 and p in LETTERS][0]
        q = "Solve: " + html(*parts) + "." + WHATN % L + (fig(pic) if pic else "")
        its.append(mcq(q, ans, cands, e))

    # + : use subtraction
    for parts, a, s in [(["n", "+", 8, "=", 23], 8, 23), ([17, "+", "n", "=", 42], 17, 42), (["y", "+", 26, "=", 50], 26, 50)]:
        ans = s - a
        L = [p for p in parts if isinstance(p, str) and p in LETTERS][0]
        chk = plain(*[ans if p == L else p for p in parts])
        e = ("Subtraction undoes addition: <i>%s</i> = %d − %d = <b>%d</b>. Check: %s." % (L, s, a, ans, chk)) + why_sub(s, a, ans)
        add(parts, ans, sub_cands(s, a, ans), e)
    # − : the letter is the start, use addition
    for parts, a, r in [(["n", "−", 9, "=", 27], 9, 27), (["p", "−", 14, "=", 29], 14, 29)]:
        ans = r + a
        L = parts[0]
        e = ("<i>%s</i> is the number you start with. Addition undoes subtraction: <i>%s</i> = %d + %d = <b>%d</b>. "
             "Check: %d − %d = %d. Not %d: that subtracts instead of adding." % (L, L, r, a, ans, ans, a, r, abs(r - a)))
        if nocarry(r, a) != ans:
            e += " Not %d: that forgets to carry the ten." % nocarry(r, a)
        add(parts, ans, add_cands(r, a, ans), e)
    # a − n = r
    for parts, a, r in [([45, "−", "n", "=", 18], 45, 18), ([32, "−", "t", "=", 15], 32, 15)]:
        ans = a - r
        L = parts[2]
        e = ("%d take away what leaves %d? <i>%s</i> = %d − %d = <b>%d</b>. Check: %d − %d = %d."
             % (a, r, L, a, r, ans, a, ans, r)) + why_sub(a, r, ans)
        add(parts, ans, sub_cands(a, r, ans), e)
    # × : use division
    for parts, k, p in [([4, "×", "n", "=", 36], 4, 36), (["m", "×", 6, "=", 42], 6, 42), ([8, "×", "b", "=", 48], 8, 48),
                        ([7, "×", "n", "=", 28], 7, 28)]:
        ans = p // k
        L = [x for x in parts if isinstance(x, str) and x in LETTERS][0]
        e = ("Division undoes multiplication: <i>%s</i> = %d ÷ %d = <b>%d</b>. Check: %d × %d = %d. "
             "Not %d: that subtracts %d. Not %d: that adds %d. Not %d: that multiplies." % (L, p, k, ans, k, ans, p, p - k, k, p + k, k, p * k))
        add(parts, ans, [p - k, p + k, p * k, ans + 1], e)
    # ÷ : use multiplication
    add(["n", "÷", 4, "=", 6], 24, [2, 10, 20],
        "<i>n</i> is the number you start with. Multiplication undoes division: <i>n</i> = 6 × 4 = <b>24</b>. "
        "Check: 24 ÷ 4 = 6. Not 2: that subtracts. Not 10: that adds. Not 20: that is 4 × 5, one group short.")
    add([42, "÷", "n", "=", 7], 6, [35, 49, 294],
        "42 shared into how many groups gives 7 in each? 42 ÷ 7 = <b>6</b>, so <i>n</i> = 6. Check: 42 ÷ 6 = 7. "
        "Not 35: that subtracts. Not 49: that adds. Not 294: that multiplies.")
    add(["w", "÷", 5, "=", 8], 40, [3, 13, 45],
        "Multiplication undoes division: <i>w</i> = 8 × 5 = <b>40</b>. Check: 40 ÷ 5 = 8. "
        "Not 3: that subtracts. Not 13: that adds. Not 45: that is one group of 5 too many.")
    # = sign first
    add([31, "=", "n", "+", 12], 19, sub_cands(31, 12, 19),
        "The = sign can come first. <i>n</i> + 12 = 31, so <i>n</i> = 31 − 12 = <b>19</b>. Check: 19 + 12 = 31." + why_sub(31, 12, 19))
    add([50, "=", 5, "×", "k"], 10, [45, 55, 250, 9],
        "5 × <i>k</i> = 50, so <i>k</i> = 50 ÷ 5 = <b>10</b>. Check: 5 × 10 = 50. Not 45: that subtracts. Not 55: that adds. Not 250: that multiplies.")
    add([20, "=", "h", "−", 16], 36, add_cands(20, 16, 36),
        "<i>h</i> − 16 = 20. Undo − 16 by adding: <i>h</i> = 20 + 16 = <b>36</b>. Check: 36 − 16 = 20. "
        "Not 4: that subtracts instead of adding.")
    # bar models
    e = ("The two parts make the whole: 19 + <i>n</i> = 47. So <i>n</i> = 47 − 19 = <b>28</b>. Check: 19 + 28 = 47."
         + why_sub(47, 19, 28))
    its.append(mcq("What is <i>n</i> in the bar model?" + fig(bar_svg(47, 19, "n")), 28, sub_cands(47, 19, 28), e))
    its.append(mcq("What is <i>m</i> in the bar model?" + fig(bar_svg("m", 16, 25)), 41, [9, 31, 51],
                   "<i>m</i> is the whole, so add the parts: <i>m</i> = 16 + 25 = <b>41</b>. Not 9: that subtracts. "
                   "Not 31: that forgets to carry the ten from 6 + 5 = 11."))
    assert nocarry(16, 25) == 31
    # both sides
    add(["n", "+", 15, "=", 20, "+", 18], 23, [38, 53, 13],
        "The right side is 20 + 18 = 38. So <i>n</i> + 15 = 38, and <i>n</i> = 38 − 15 = <b>23</b>. "
        "Not 38: that is the right side. Not 53: that adds 15. Not 13: 15 is less than 20, so <i>n</i> is more than 18, not less.")
    assert len(its) == 20, len(its)
    return {"title": "Solve equations", "items": its}


# ============================================================ set 3: check a solution
def set_check(P):
    its = []
    # a. which equation has this solution
    for v, L, right, wrongs in [
        (6, "n", "n + 9 = 15", ["n + 9 = 16", "n − 9 = 15", "9 × n = 15"]),
        (8, "n", "4 × n = 32", ["4 + n = 32", "4 × n = 48", "n ÷ 4 = 32"]),
        (12, "y", "30 − y = 18", ["30 − y = 12", "y + 12 = 30", "y − 12 = 18"]),
        (7, "k", "42 ÷ k = 6", ["42 ÷ k = 7", "k × 6 = 48", "k + 6 = 42"]),
    ]:
        assert holds(right, v) and not any(holds(w, v) for w in wrongs)
        lhs = right.split(" = ")[0]
        e = ("Put %d in place of <i>%s</i> and work out each left side. %s = %d, so <b>%s</b> is true. "
             "The other equations are false when <i>%s</i> = %d." % (v, L, lhs.replace(L, str(v)), val(lhs.replace(L, str(v))), right, L, v))
        its.append(mcq("Which equation has <i>%s</i> = %d as its solution?" % (L, v), right, wrongs, e))
    # b. is it a solution
    for parts, x, ans, wrongvals in [
        (["n", "+", 7, "=", 16], 9, 9, [23, 10, 8]),
        (["n", "−", 8, "=", 15], 7, 23, [22, 13, 17]),
        ([5, "×", "n", "=", 40], 8, 8, [35, 45, 200]),
        (["n", "÷", 3, "=", 6], 2, 18, [9, 3, 15]),
        ([34, "−", "n", "=", 16], 18, 18, [50, 22, 28]),
        (["n", "+", 19, "=", 45], 64, 26, [34, 25, 36]),
    ]:
        eq = plain(*parts)
        assert holds(eq, ans) and all(not holds(eq, w) for w in wrongvals)
        sub = plain(*[x if p == "n" else p for p in parts])
        lhs = sub.split(" = ")[0]
        if x == ans:
            right = "Yes"
            wrong = ["No, n = %d" % w for w in wrongvals]
            e = "Put %d in place of <i>n</i>: %s = %d. Both sides are equal, so <b>yes</b>, %d is a solution." % (x, lhs, val(lhs), x)
        else:
            right = "No, n = %d" % ans
            wrong = ["Yes"] + ["No, n = %d" % w for w in wrongvals]
            chk = plain(*[ans if p == "n" else p for p in parts])
            got = val(lhs)
            e = ("Put %d in place of <i>n</i>: %s is %s, not %s. So %d is <b>not</b> a solution. "
                 "The solution is %d. Check: %s." % (x, lhs, n(int(got)) if got == int(got) else "not a whole number",
                                                    parts[-1], x, ans, chk))
            if x == 7:
                e = ("%d − 8 does not give 15, so %d is <b>not</b> a solution. %d came from 15 − 8: subtracting instead of adding. "
                     "Undo − 8 by adding: <i>n</i> = 15 + 8 = 23. Check: 23 − 8 = 15." % (x, x, x))
            elif x == 2:
                e = ("2 ÷ 3 is not 6, so 2 is <b>not</b> a solution. Undo ÷ 3 by multiplying: <i>n</i> = 6 × 3 = 18. "
                     "Check: 18 ÷ 3 = 6.")
            elif x == 64:
                e += " 64 comes from adding 19 instead of subtracting it."
        its.append(mcq("Is <i>n</i> = %d a solution of %s?" % (x, html(*parts)), right, wrong, e))
    # c. find the mistake
    MIST = ["Added instead of subtracting", "Subtracted instead of adding", "Multiplied instead of dividing",
            "Nothing, the answer is right"]
    for parts, got, k in [
        (["n", "+", 12, "=", 30], 42, 0),
        (["n", "−", 6, "=", 14], 8, 1),
        ([6, "×", "n", "=", 42], 252, 2),
        (["n", "÷", 4, "=", 5], 20, 3),
        ([25, "−", "n", "=", 9], 34, 0),
        (["n", "−", 9, "=", 21], 12, 1),
    ]:
        nm, he, his = P.next()
        eq = plain(*parts)
        sub = plain(*[got if p == "n" else p for p in parts])
        lhs = sub.split(" = ")[0]
        a = [x for x in range(0, 400) if holds(eq, x)]
        assert len(a) == 1
        a = a[0]
        if k == 3:
            assert got == a
            e = "Check: %s. Both sides are equal, so <b>nothing is wrong</b>. %s is right." % (sub, cap(he))
        else:
            assert got != a
            how = {0: "%s added. Subtraction is the inverse of addition" % cap(he),
                   1: "%s subtracted. Addition is the inverse of subtraction" % cap(he),
                   2: "%s multiplied. Division is the inverse of multiplication" % cap(he)}[k]
            if parts[0] == 25:
                how = "%s added 25 + 9. But 25 take away <i>n</i> leaves 9, so subtract: 25 − 9" % cap(he)
            e = ("Check: %s does not give %s, so %d is wrong. %s. The answer is <i>n</i> = <b>%d</b>. Check: %s."
                 % (lhs, parts[-1], got, how, a, plain(*[a if p == "n" else p for p in parts])))
        its.append(mcq("%s solves %s and gets <i>n</i> = %d. What did %s do?" % (nm, html(*parts), got, he),
                       MIST[k], [m for i, m in enumerate(MIST) if i != k], e))
    # d. which equation checks the answer
    for parts, v, right, wrongs in [
        (["n", "+", 8, "=", 23], 15, "15 + 8 = 23", ["23 + 8 = 31", "15 − 8 = 7", "23 + 15 = 38"]),
        ([6, "×", "n", "=", 42], 7, "6 × 7 = 42", ["6 + 7 = 13", "42 − 6 = 36", "7 × 7 = 49"]),
        (["n", "−", 13, "=", 24], 37, "37 − 13 = 24", ["24 − 13 = 11", "37 + 13 = 50", "37 + 24 = 61"]),
    ]:
        assert holds(plain(*parts), v) and holds(right) and all(holds(w) for w in wrongs)
        its.append(mcq("Which can you use to check that <i>n</i> = %d is the solution of %s?" % (v, html(*parts)),
                       right, wrongs,
                       "To check, put %d back in place of <i>n</i>: <b>%s</b>. Both sides are equal, so %d is right. "
                       "The other number sentences are true, but they do not put %d in place of <i>n</i>." % (v, right, v, v)))
    # e. test the choices
    its.append(mcq("Try each number in " + html("n", "+", 14, "=", 31) + ". Which one is the solution?", 17, [45, 23, 18],
                   "Test them: 17 + 14 = 31, so <b>17</b> is the solution. 45 + 14 = 59, 23 + 14 = 37 and 18 + 14 = 32. "
                   "45 adds 31 + 14. 23 takes the smaller digit from the larger."))
    assert sfl(31, 14) == 23
    assert len(its) == 20, len(its)
    return {"title": "Check a solution", "items": its}


# ============================================================ set 4: inequalities
def set_ineq(P):
    its = []
    its.append(mcq("Which is true?", "15 &gt; 9", ["9 &gt; 15", "15 &lt; 9", "15 &lt; 15"],
                   "&gt; means “is greater than”. 15 is greater than 9, so <b>15 &gt; 9</b> is true. "
                   "The open side of the sign faces the greater number. 15 &lt; 15 is false: 15 is equal to 15, not less."))
    its.append(mcq("What does " + ineq("n", "<", 6) + " mean?", "n is less than 6",
                   ["n is greater than 6", "n is 6", "n is 6 or less"],
                   "&lt; means “is less than”. <i>n</i> &lt; 6 means <b><i>n</i> is less than 6</b>: 0, 1, 2, 3, 4 or 5. "
                   "6 itself is not less than 6, so it is not a solution."))
    # solve
    for a, op, b, rel, c in [("n", "+", 5, "<", 12), ("n", "+", 8, ">", 15), (12, "+", "n", "<", 20),
                             ("n", "+", 9, ">", 17), ("n", "−", 6, ">", 9), ("n", "−", 3, ">", 10)]:
        num = b if isinstance(b, int) else a
        k = c - num if op == "+" else c + num
        same = c + num if op == "+" else c - num
        other = ">" if rel == "<" else "<"
        p = plain(a, op, b, rel, c)
        ss = sols(p)
        assert (ss == list(range(0, k)) if rel == "<" else ss == list(range(k + 1, 61)))
        right = "n %s %d" % ("&lt;" if rel == "<" else "&gt;", k)
        wrong = ["n %s %d" % ("&lt;" if other == "<" else "&gt;", k), "n %s %d" % ("&lt;" if rel == "<" else "&gt;", same),
                 "n = %d" % k]
        eqp = plain(a, op, b, "=", c)
        test = k - 1 if rel == "<" else k + 1
        tp = plain(*[test if x == "n" else x for x in (a, op, b)])
        e = ("Think of the equation %s first: <i>n</i> = %d. Is %d a solution? %s = %d, which is not %s %d. "
             "Try %d: %s = %d, and %d %s %d is true. So <b>%s</b>. Not %s %d: that %s instead of %s."
             % (eqp, k, k, plain(*[k if x == "n" else x for x in (a, op, b)]), c,
                "less than" if rel == "<" else "greater than", c, test, tp, val(tp), val(tp),
                "&lt;" if rel == "<" else "&gt;", c, right.replace("n", "<i>n</i>"),
                "<i>n</i> " + ("&lt;" if rel == "<" else "&gt;"), same,
                "adds" if op == "+" else "subtracts", "subtracting" if op == "+" else "adding"))
        its.append(mcq("Solve: " + ineq(a, op, b, rel, c), right, wrong, e))
    # graph -> which inequality
    for (lo, hi), right, wrongs in [
        ((0, 10), ("n", "+", 4, "<", 10), [("n", "+", 4, ">", 10), ("n", "+", 4, "<", 11), ("n", "+", 6, "<", 10)]),
        ((4, 14), ("n", "+", 7, ">", 15), [("n", "+", 7, "<", 15), ("n", "+", 7, ">", 16), ("n", "+", 8, ">", 15)]),
        ((0, 10), ("n", "+", 9, "<", 12), [("n", "+", 9, ">", 12), ("n", "+", 9, "<", 13), ("n", "+", 9, "<", 11)]),
        ((9, 19), ("n", "−", 4, ">", 8), [("n", "−", 4, "<", 8), ("n", "+", 4, ">", 8), ("n", "−", 4, ">", 9)]),
    ]:
        rp = plain(*right)
        dots, more = graph_of(rp, lo, hi)
        ss = sols(rp)
        for w in wrongs:
            assert sols(plain(*w)) != ss, w
        rel = right[3]
        k = ss[-1] + 1 if rel == "<" else ss[0] - 1
        lab = "number line graph: dots on %s" % (("0 to %d" % ss[-1]) if rel == "<" else ("%d and greater" % ss[0]))
        svg = dots_svg(lo, hi, dots, more, lab)
        where = ("0 to %d" % (k - 1)) if rel == "<" else ("%d, %d, %d and so on" % (k + 1, k + 2, k + 3))
        e = ("The dots are on %s, so the graph shows <i>n</i> %s %d. Solve %s: think %s, so <i>n</i> = %d, and "
             "<b>%s</b> gives <i>n</i> %s %d."
             % (where, "&lt;" if rel == "<" else "&gt;", k, ineq(*right), plain(right[0], right[1], right[2], "=", right[4]),
                k, ineq(*right), "&lt;" if rel == "<" else "&gt;", k))
        its.append(mcq("The dots show all the whole-number solutions. Which inequality does the graph show?" + fig(svg),
                       ineq(*right), [ineq(*w) for w in wrongs], e))
    # how to graph
    for parts, right, wrongs in [
        (("n", "+", 3, "<", 9), "Dots on 0 to 5", ["Dots on 0 to 6", "Dots on 6 and greater", "Dots on 7 and greater"]),
        (("n", "+", 6, ">", 14), "Dots on 9 and greater", ["Dots on 8 and greater", "Dots on 0 to 7", "Dots on 0 to 8"]),
        (("n", "−", 5, ">", 6), "Dots on 12 and greater", ["Dots on 11 and greater", "Dots on 0 to 10", "Dots on 2 and greater"]),
    ]:
        ss = sols(plain(*parts))
        if parts[3] == "<":
            assert right == "Dots on 0 to %d" % ss[-1] and ss[0] == 0
            e = ("Solve first: %s gives <i>n</i> &lt; %d. The whole numbers less than %d are 0 to %d, so put <b>dots on 0 to %d</b>. "
                 "%d is not less than %d, so it gets no dot." % (ineq(*parts), ss[-1] + 1, ss[-1] + 1, ss[-1], ss[-1], ss[-1] + 1, ss[-1] + 1))
        else:
            assert right == "Dots on %d and greater" % ss[0] and ss[-1] == 60
            e = ("Solve first: %s gives <i>n</i> &gt; %d. Put <b>dots on %d and greater</b> and an arrow to show they keep going. "
                 "%d itself is not greater than %d, so it gets no dot." % (ineq(*parts), ss[0] - 1, ss[0], ss[0] - 1, ss[0] - 1))
            if parts[1] == "−":
                e += " Not 2 and greater: that subtracts 5 instead of adding it."
        its.append(mcq("How do you graph the whole-number solutions of %s?" % ineq(*parts), right, wrongs, e))
    # verify
    for parts, r, ws, want in [(("n", "+", 6, "<", 15), 5, [9, 10, 12], True),
                               (("n", "+", 4, ">", 11), 9, [7, 6, 3], True),
                               (("n", "−", 2, ">", 10), 12, [13, 15, 18], False)]:
        p = plain(*parts)
        assert holds(p, r) == want and all(holds(p, x) != want for x in ws)
        tests = "; ".join("%s = %d (%s)" % (plain(*[x if t == "n" else t for t in parts[:3]]),
                                          val(plain(*[x if t == "n" else t for t in parts[:3]])),
                                          "yes" if holds(p, x) else "no") for x in [r] + ws)
        rel = "less than" if parts[3] == "<" else "greater than"
        e = "Test each number. Is the left side %s %d? %s. So the answer is <b>%d</b>." % (rel, parts[4], tests, r)
        if want and r == 5:
            e += " 9 + 6 = 15 is equal to 15, not less, so 9 is not a solution."
        if not want:
            e += " 12 − 2 = 10 is equal to 10, not greater, so 12 is not a solution."
        q = "Which number is %s a solution of %s?" % ("" if want else "<b>not</b>", ineq(*parts))
        its.append(mcq(q.replace("is  a", "is a"), r, ws, e))
    # find the mistake in a graph
    nm, he, his = P.next()
    svg = dots_svg(0, 10, list(range(0, 7)), False, "number line graph: dots on 0 to 6")
    assert sols("n + 2 > 9")[0] == 8
    its.append(mcq("%s graphs the whole-number solutions of %s like this. What is wrong?" % (nm, ineq("n", "+", 2, ">", 9)) + fig(svg),
                   "The dots should be on 8 and greater",
                   ["The dots should be on 7 and greater", "The dots should be on 0 to 7", "Nothing is wrong"],
                   "<i>n</i> + 2 &gt; 9 gives <i>n</i> &gt; 7: the numbers <b>greater</b> than 7. So the dots go on "
                   "<b>8 and greater</b>, with an arrow. %s mixed up &gt; and &lt; and put dots on the wrong side. "
                   "7 gets no dot: 7 + 2 = 9 is not greater than 9." % nm))
    nm, he, his = P.next()
    svg = dots_svg(0, 10, list(range(0, 7)), False, "number line graph: dots on 0 to 6")
    assert sols("n + 5 < 11") == list(range(0, 6))
    its.append(mcq("%s graphs the whole-number solutions of %s like this. What is wrong?" % (nm, ineq("n", "+", 5, "<", 11)) + fig(svg),
                   "6 should not have a dot",
                   ["0 should not have a dot", "The dots should be on 7 and greater", "Nothing is wrong"],
                   "<i>n</i> + 5 &lt; 11 gives <i>n</i> &lt; 6. 6 + 5 = 11, which is not less than 11, so <b>6 should not have a dot</b>. "
                   "0 is a solution: 0 + 5 = 5, and 5 &lt; 11."))
    assert len(its) == 20, len(its)
    return {"title": "Inequalities on a number line", "items": its}


# ============================================================ set 5: word problems
def set_words(P):
    its = []

    def match(q, right, wrongs, e, ans):
        assert holds(right, ans), right
        for w in wrongs:
            assert not holds(w, ans), w
        its.append(mcq(q, right, wrongs, e))

    def solve(q, eq, ans, cands, e, unit="", money=False, pic=None):
        assert holds(eq, ans), eq
        f = (lambda v: "$" + n(v)) if money else (lambda v: n(v) + unit)
        cs = [f(c) for c in cands if c > 0]
        q = q + (fig(pic) if pic else "")
        eh = " ".join("<i>n</i>" if t == "n" else t for t in eq.split(" "))
        its.append(mcq(q, f(ans), cs, "Equation: %s. %s" % (eh, e)))

    # 1
    nm, he, his = P.next()
    match("%s has 18 hockey cards. %s gets <i>n</i> more cards. Now %s has 35. Which equation shows this?" % (nm, cap(he), he),
          "18 + n = 35", ["18 + 35 = n", "n − 18 = 35", "35 + n = 18"],
          "%s starts with 18, gets <i>n</i> more and ends with 35: <b>18 + <i>n</i> = 35</b>. Then <i>n</i> = 35 − 18 = 17." % nm, 17)
    # 2
    nm, he, his = P.next()
    solve("%s picks 14 apples at the orchard. %s brother picks some too. Together they have 32 apples. "
          "How many apples did %s brother pick?" % (nm, cap(his), his),
          "14 + n = 32", 18, sub_cands(32, 14, 18),
          "<i>n</i> = 32 − 14 = <b>18</b> apples. Check: 14 + 18 = 32." + why_sub(32, 14, 18), " apples",
          pic=bar_svg(32, 14, "n"))
    # 3
    match("A teacher puts 24 chairs in 4 equal rows for an assembly. Let <i>n</i> be the number of chairs in each row. "
          "Which equation matches?", "4 × n = 24", ["4 + n = 24", "n − 4 = 24", "n = 24 × 4"],
          "4 rows with <i>n</i> chairs in each is 4 × <i>n</i>, and that is 24 chairs: <b>4 × <i>n</i> = 24</b>. Then <i>n</i> = 6.", 6)
    # 4
    nm, he, his = P.next()
    solve("Hot chocolate at the skating rink costs $3 a cup. %s buys some cups for %s friends and pays $27. "
          "How many cups did %s buy?" % (nm, his, he),
          "3 × n = 27", 9, [24, 30, 81],
          "<i>n</i> = 27 ÷ 3 = <b>9</b> cups. Check: 3 × 9 = 27. Not 24: that subtracts 3. Not 81: that multiplies.", " cups")
    # 5
    solve("Each canoe holds 2 campers. There are 34 campers on the canoe trip. How many canoes do they need?",
          "2 × n = 34", 17, [32, 36, 68],
          "<i>n</i> = 34 ÷ 2 = <b>17</b> canoes. Check: 2 × 17 = 34. Not 68: that multiplies. Not 32: that subtracts 2.", " canoes")
    # 6
    solve("A Grade 4 class has raised $28 for the Terry Fox Run. The goal is $50. How much more do they need to raise?",
          "28 + n = 50", 22, sub_cands(50, 28, 22),
          "<i>n</i> = 50 − 28 = <b>$22</b>. Check: $28 + $22 = $50." + why_sub(50, 28, 22).replace("Not ", "Not $"), money=True)
    # 7
    solve("There were some Canada geese on a pond. 17 flew away, and 26 are left. How many geese were there at the start?",
          "n − 17 = 26", 43, add_cands(26, 17, 43),
          "Undo − 17 by adding: <i>n</i> = 26 + 17 = <b>43</b> geese. Check: 43 − 17 = 26. "
          "Not 9: that subtracts instead of adding. Not 33: that forgets to carry the ten.", " geese")
    assert nocarry(26, 17) == 33
    # 8
    nm, he, his = P.next()
    match("%s had <i>n</i> stickers. %s gave 12 to friends and has 19 left. Which equation matches?" % (nm, cap(he)),
          "n − 12 = 19", ["n + 12 = 19", "12 − n = 19", "19 − 12 = n"],
          "Start with <i>n</i>, give away 12, and 19 are left: <b><i>n</i> − 12 = 19</b>. Then <i>n</i> = 19 + 12 = 31.", 31)
    # 9
    nm, he, his = P.next()
    solve("%s shares some maple candies equally among 6 friends. Each friend gets 7 candies. How many candies did %s share?" % (nm, he),
          "n ÷ 6 = 7", 42, [13, 36, 48],
          "Multiplication undoes division: <i>n</i> = 7 × 6 = <b>42</b> candies. Check: 42 ÷ 6 = 7. "
          "Not 13: that adds. Not 36 or 48: that gives each friend 6 or 8 candies instead of 7.", " candies")
    # 10
    solve("A school bus holds 48 students. 29 students are on the bus. How many more students can get on?",
          "29 + n = 48", 19, sub_cands(48, 29, 19),
          "<i>n</i> = 48 − 29 = <b>19</b> students. Check: 29 + 19 = 48." + why_sub(48, 29, 19), " students")
    # 11
    solve("For Thanksgiving, Grandma cuts each pie into 8 equal pieces. There are 40 pieces. How many pies are there?",
          "8 × n = 40", 5, [32, 48, 320],
          "<i>n</i> = 40 ÷ 8 = <b>5</b> pies. Check: 8 × 5 = 40. Not 32: that subtracts 8. Not 320: that multiplies.", " pies")
    # 12
    match("A ringette team has 12 players. The coach can add <i>n</i> more players, but the team must have fewer than 18 players. "
          "Which inequality matches?", "12 + n &lt; 18", ["12 + n &gt; 18", "12 + n = 18", "n + 18 &lt; 12"],
          "12 players plus <i>n</i> more must be <b>fewer than</b> 18, so use &lt;: <b>12 + <i>n</i> &lt; 18</b>. "
          "Not =: the team does not have to have exactly 18.", 5)
    # 13
    its.append(mcq("A ringette team has 12 players. The team must have fewer than 18 players, so 12 + <i>n</i> &lt; 18. "
                   "What is the greatest number of players the coach can add?", "5 players", ["6 players", "30 players", "18 players"],
                   "12 + <i>n</i> &lt; 18 gives <i>n</i> &lt; 6. The greatest whole number less than 6 is <b>5</b>. "
                   "Check: 12 + 5 = 17 and 17 &lt; 18. Not 6: 12 + 6 = 18, which is not fewer than 18. Not 30: that adds."))
    assert max(sols("12 + n < 18")) == 5
    # 14
    nm, he, his = P.next()
    its.append(mcq("%s has read 9 books. To win a prize, %s must read more than 14 books in all, so 9 + <i>n</i> &gt; 14. "
                   "What is the fewest more books %s can read to win?" % (nm, he, he), "6 books", ["5 books", "23 books", "14 books"],
                   "9 + <i>n</i> &gt; 14 gives <i>n</i> &gt; 5. The least whole number greater than 5 is <b>6</b>. "
                   "Check: 9 + 6 = 15 and 15 &gt; 14. Not 5: 9 + 5 = 14, which is not more than 14. Not 23: that adds."))
    assert min(sols("9 + n > 14")) == 6
    # 15
    nm, he, his = P.next()
    solve("%s has $35. %s buys a hockey stick and has $12 left. How much did the stick cost?" % (nm, cap(he)),
          "35 − n = 12", 23, [47, 33, 13],
          "<i>n</i> = 35 − 12 = <b>$23</b>. Check: $35 − $23 = $12. Not $47: that adds instead of subtracting.", money=True)
    # 16
    solve("32 students go on a field trip in 4 vans. Each van has the same number of students. How many students are in each van?",
          "4 × n = 32", 8, [28, 36, 128],
          "<i>n</i> = 32 ÷ 4 = <b>8</b> students. Check: 4 × 8 = 32. Not 28: that subtracts 4. Not 128: that multiplies.", " students")
    # 17
    nm, he, his = P.next()
    match("%s puts the same number of photos, <i>n</i>, on each of 5 pages of %s scrapbook. %s uses 30 photos. "
          "Which equation matches?" % (nm, his, cap(he)),
          "5 × n = 30", ["5 + n = 30", "n ÷ 5 = 30", "n − 5 = 30"],
          "5 pages with <i>n</i> photos on each is 5 × <i>n</i>: <b>5 × <i>n</i> = 30</b>. Then <i>n</i> = 30 ÷ 5 = 6.", 6)
    # 18
    nm, he, his = P.next()
    its.append(mcq("In a board game, %s has 11 points. %s wins with more than 20 points. "
                   "Which number of extra points lets %s win?" % (nm, cap(he), him(he)), 10, [9, 8, 5],
                   "11 + <i>n</i> &gt; 20 gives <i>n</i> &gt; 9. Test 10: 11 + 10 = 21, and 21 &gt; 20, so <b>10</b> works. "
                   "9 does not: 11 + 9 = 20 is equal to 20, not more than 20."))
    assert sols("11 + n > 20")[0] == 10
    # 19
    nm1, _, _ = P.next()
    nm2, he2, his2 = P.next()
    solve("%s has 15 red blocks and 20 blue blocks. %s has 25 red blocks. How many blue blocks does %s need "
          "to have the same number of blocks as %s?" % (nm1, nm2, nm2, nm1),
          "15 + 20 = 25 + n", 10, [35, 30, 60],
          "15 + 20 = 35. So 25 + <i>n</i> = 35, and <i>n</i> = <b>10</b> blue blocks. Not 35: that is %s’s total. "
          "Not 30: 25 is more than 15, so %s needs fewer than 20 blue blocks, not more." % (nm1, nm2), " blocks",
          pic=pan_svg("15 + 20", "25 + n"))
    # 20
    nm, he, his = P.next()
    solve("%s’s family drives 50 km to the cottage. They stop after 18 km, then drive 14 km more and stop again. "
          "How far do they still have to drive?" % nm,
          "18 + 14 + n = 50", 18, [82, 32, 36],
          "18 + 14 = 32. So 32 + <i>n</i> = 50, and <i>n</i> = 50 − 32 = <b>18 km</b>. "
          "Not 32: that forgets the 14 km. Not 36: that forgets the first 18 km. Not 82: that adds all the numbers.", " km")
    assert len(its) == 20, len(its)
    return {"title": "Word problems with equations and inequalities", "items": its}


def him(he):
    return "her" if he == "she" else "him"


# ============================================================ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def body_html():
    g1 = dots_svg(0, 10, list(range(0, 7)), False, "number line graph: dots on 0 to 6")
    g2 = dots_svg(4, 14, list(range(8, 15)), True, "number line graph: dots on 8 and greater")
    return (
        "<h2>Letters stand for unknown numbers</h2>"
        "<p>An <b>equation</b> has an = sign. Both sides have the <b>same value</b>, like a pan balance that is level. "
        "A letter such as <i>n</i> stands for a number we do not know yet. <i>n</i> is a <b>variable</b>.</p>"
        "<figure class='sn-fig'>" + pan_svg("n + 8", "23") +
        "<figcaption>The pans balance, so <i>n</i> + 8 = 23.</figcaption></figure>"
        "<h2>Solve with the inverse</h2>"
        "<p>To <b>solve</b> an equation, find the number that makes both sides equal. "
        "Use the <b>inverse</b> operation to undo what was done to <i>n</i>.</p>" +
        table(["Equation", "Undo it", "Solution"], [
            [html("n", "+", 8, "=", 23), "23 − 8", "<i>n</i> = 15"],
            [html("n", "−", 9, "=", 27), "27 + 9", "<i>n</i> = 36"],
            [html(4, "×", "n", "=", 36), "36 ÷ 4", "<i>n</i> = 9"],
            [html("n", "÷", 4, "=", 6), "6 × 4", "<i>n</i> = 24"],
        ]) +
        "<figure class='sn-fig'>" + blocks_svg(4, "n", 36) +
        "<figcaption>4 equal blocks balance 36, so 4 × <i>n</i> = 36 and each block is 36 ÷ 4 = 9.</figcaption></figure>" +
        ex("Example 1", "Solve " + html("n", "+", 8, "=", 23) + ".",
           "Subtraction undoes addition: <i>n</i> = 23 − 8 = 15.", "<i>n</i> = 15") +
        "<h2>Check your solution</h2>"
        "<p>Put your answer back in place of the letter. If both sides are equal, the answer is right.</p>" +
        ex("Example 2", "Is <i>n</i> = 15 the solution of " + html("n", "+", 8, "=", 23) + "?",
           "15 + 8 = 23. Both sides are 23.", "Yes") +
        "<h2>Inequalities</h2>"
        "<p>An <b>inequality</b> uses &lt; (is less than) or &gt; (is greater than). It has many solutions, not just one. "
        "Solve it like an equation first, then decide which side the solutions are on. "
        "On a number line, put a dot on every whole-number solution.</p>" +
        ex("Example 3", "Solve " + ineq("n", "+", 5, "<", 12) + " and graph the solutions.",
           "Think of <i>n</i> + 5 = 12: <i>n</i> = 7. But 7 + 5 = 12 is not less than 12. "
           "Try 6: 6 + 5 = 11, and 11 &lt; 12 is true. So <i>n</i> &lt; 7: the whole numbers 0 to 6.", "<i>n</i> &lt; 7") +
        "<figure class='sn-fig'>" + g1 +
        "<figcaption><i>n</i> &lt; 7: dots on 0 to 6. There is no dot on 7.</figcaption></figure>" +
        "<figure class='sn-fig'>" + g2 +
        "<figcaption><i>n</i> + 8 &gt; 15 gives <i>n</i> &gt; 7: dots on 8 and greater. The arrow shows they keep going.</figcaption></figure>" +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["<i>n</i> + 8 = 23, so <i>n</i> = 31 (23 + 8)", "Use the inverse: 23 − 8 = 15"],
            ["<i>n</i> − 9 = 27, so <i>n</i> = 18 (27 − 9)", "Undo − 9 by adding: 27 + 9 = 36"],
            ["4 × <i>n</i> = 36, so <i>n</i> = 32 (36 − 4)", "Undo × 4 by dividing: 36 ÷ 4 = 9"],
            ["<i>n</i> &lt; 7, so put a dot on 7", "7 is not less than 7. The dots stop at 6"],
            ["<i>n</i> &gt; 7, so put dots on 0 to 6", "&gt; means greater: dots on 8 and greater"],
            ["The letter <i>n</i> means 14", "<i>n</i> is just a name for the unknown number"],
        ])
    )


FAQ = [
    {"q": "What do Grade 4 students learn about equations and inequalities in Ontario?",
     "a": "In the Ontario Grade 4 Algebra strand (C2), students use letters as variables, solve equations with whole numbers up to 50, and check their solutions. They also solve inequalities with addition and subtraction up to 20, like n + 5 < 12, and graph the solutions on a number line."},
    {"q": "How do you solve an equation like n + 8 = 23 or 4 × n = 36?",
     "a": "Use the inverse operation. Subtraction undoes addition, so n = 23 − 8 = 15. Division undoes multiplication, so n = 36 ÷ 4 = 9. Then put the answer back in to check it."},
    {"q": "How do you solve and graph an inequality in Grade 4?",
     "a": "Solve it like an equation, then test a number to see which side the solutions are on. For n + 5 < 12, n = 7 would make 12, so the solutions are the whole numbers less than 7: put dots on 0 to 6, with no dot on 7."},
    {"q": "Why do Grade 4 students use letters like n in math?",
     "a": "A letter is a variable: it stands for a number we do not know yet. Using letters prepares students for algebra in later grades. Any letter works, so 3 × n = 24 and 3 × k = 24 both have the solution 8."},
]


def gen_unit():
    rnd = random.Random(44810)
    P = People(rnd)
    sets = [set_letters(P), set_solve(), set_check(P), set_ineq(P), set_words(P)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5), s["title"]
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"].count("<svg") <= 1
            assert it["q"] not in seen, it["q"]
            assert "\\" not in it["q"] + "".join(it["c"]) + it["e"]
            seen.add(it["q"])
    return {
        "country": "ca-on", "subject": "math", "grade": "grade-4", "slug": "equations-and-inequalities", "sort": 10,
        "updated": UPDATED, "pdf_url": "",
        "title": "Grade 4 Equations and Inequalities",
        "seo_title": "Grade 4 Equations and Inequalities Worksheets: Free Math with Answer Key (Ontario Curriculum)",
        "short_title": "Equations and Inequalities",
        "domain": "Algebra",
        "standard_code": "Grade 4: C2.2",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Solve equations that involve whole numbers up to 50 in various contexts, and verify solutions",
        "meta_desc": "Free Grade 4 math worksheets on equations and inequalities for the Ontario curriculum: letters as unknowns, pan balances, solving n + 8 = 23 and 4 × n = 36, checking solutions, and inequalities like n + 5 < 12 graphed on a number line. 100 questions with an answer key.",
        "key_big": "Use the inverse to find the unknown: n + 8 = 23, so n = 23 − 8 = 15.",
        "key_sub": "Check by putting the answer back in: 15 + 8 = 23. For n + 5 < 12, the solutions are the whole numbers less than 7, so 7 gets no dot.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen_unit()
    mark_large(u, "bar model|pan balance|number line")
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(u, f, ensure_ascii=False, indent=1)
    print("wrote", path)
