# -*- coding: utf-8 -*-
"""
CA Grade 6 Math: Equations and Inequalities (Ontario Mathematics Curriculum 2020, Grade 6: Algebra, C2)
  python3 tools/gen_ca_math_g6_equations.py
One-step and two-step equations (3x + 5 = 26), equations with more than one term (2x + 3x = 35),
checking (verifying) a solution, inequalities with two operations (2x + 1 < 15) graphed on a number line,
and word problems in Canadian contexts written as equations and inequalities. Whole numbers only.
Wrong answers come from real student mistakes: undoing the operations in the wrong order (dividing first),
using the wrong inverse (adding 5 instead of subtracting it), forgetting the second step, multiplying
instead of dividing, multiplying the coefficients (2x + 3x = 6x), forgetting that x means 1x,
reading 3x as the number 37, an open circle for ≤ and ≥ (or a closed one for < and >), the arrow the
wrong way, and answering with the wrong quantity in a word problem.
Every answer is checked in code. HTML attributes use single quotes (no backslashes in the JSON).
Canadian English. Real minus sign −.
"""
import json, os, random, re
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-6")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
GREY = "#e4e4e4"
RED = "#c0392b"
INK = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"
M = "−"
GIRLS = ["Olivia", "Emma", "Maya", "Zoe", "Amira", "Mei", "Chloe", "Priya", "Leah", "Hana", "Ava", "Sofia"]
BOYS = ["Liam", "Noah", "Aiden", "Lucas", "Owen", "Arjun", "Ethan", "Jayden", "Benjamin", "Mateo", "Nathan", "Kai"]

SYM = {">": "&gt;", "<": "&lt;", ">=": "≥", "<=": "≤"}
PSYM = {">": ">", "<": "<", ">=": "≥", "<=": "≤"}
OPP = {">": "<", "<": ">", ">=": "<=", "<=": ">="}          # arrow the other way
SWAP = {">": ">=", ">=": ">", "<": "<=", "<=": "<"}          # open <-> closed circle
RIGHT = {">": True, ">=": True, "<": False, "<=": False}
CLOSED = {">": False, "<": False, ">=": True, "<=": True}
WORDS = {">": "greater than", "<": "less than", ">=": "greater than or equal to", "<=": "less than or equal to"}


# ------------------------------------------------------------ text helpers
def V(v):
    return "<i>%s</i>" % v


def term(a, v):
    return V(v) if a == 1 else "%d%s" % (a, V(v))


def osym(op):
    return "+" if op == "+" else M


def lhs(a, op, b, v="x"):
    return "%s %s %d" % (term(a, v), osym(op), b)


def eq(a, op, b, c, v="x"):
    return "%s = %d" % (lhs(a, op, b, v), c)


def ineq_s(a, op, b, rel, c, v="x"):
    return "%s %s %d" % (lhs(a, op, b, v), SYM[rel], c)


def sol(v, rel, k):
    return "%s %s %d" % (V(v), SYM[rel], k)


def val(a, op, b, x):
    return a * x + b if op == "+" else a * x - b


def solve2(a, op, b, c):
    r = F(c - b if op == "+" else c + b, a)
    assert r.denominator == 1 and r > 0, (a, op, b, c)
    return int(r)


def holds(x, rel, c):
    return {">": x > c, "<": x < c, ">=": x >= c, "<=": x <= c}[rel]


def calc(a, op, b, x):
    """'3 × 7 + 5 = 26'"""
    return "%d × %d %s %d = %d" % (a, x, osym(op), b, val(a, op, b, x))


def whole(v):
    v = F(v)
    return int(v) if v.denominator == 1 and v > 0 else None


def cap(s):
    return s[0].upper() + s[1:]


def plain(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s)).strip()


# ------------------------------------------------------------ question helpers
def mcq(q, correct, cands, e, rnd):
    """correct and cands: strings, or (string, value) pairs. A candidate equal in value (or text) to the
    correct answer or to an earlier candidate is skipped."""
    cs, cv = correct if isinstance(correct, tuple) else (correct, None)
    seen, vals, pick = {plain(cs)}, ({cv} if cv is not None else set()), []
    for c in cands:
        if c is None:
            continue
        s, v = c if isinstance(c, tuple) else (c, None)
        if not s or plain(s) in seen:
            continue
        if v is not None:
            if v in vals:
                continue
            vals.add(v)
        seen.add(plain(s))
        pick.append(s)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, cs, cands)
    ch = pick + [cs]
    rnd.shuffle(ch)
    return {"q": q, "c": ch, "a": ch.index(cs), "e": e}


def mcq_n(q, v, cands, e, rnd, unit="", notes=None):
    """notes (optional, parallel to cands): why a wrong answer happens; added to e for the choices used."""
    notes = notes or [None] * len(cands)
    good = [(c, t) for c, t in zip(cands, notes) if c is not None and F(c).denominator == 1 and c > 0]
    it = mcq(q, (str(v) + unit, F(v)), [(str(c) + unit, F(c)) for c, t in good], e, rnd)
    used, add = set(), []
    for c, t in good:
        if t and str(c) + unit in it["c"] and F(c) not in used:
            used.add(F(c))
            add.append("%s comes from %s" % (c, t))
    if add:
        it["e"] += " Wrong answers: " + "; ".join(add) + "."
    return it


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def tw(t, fs):
    return len(str(t)) * fs * 0.58


def text(x, y, t, fs=16, anchor="middle", col=INK, italic=False, bold=False):
    return ("<text x='%.1f' y='%.1f' font-size='%d'%s%s fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, " font-style='italic'" if italic else "", " font-weight='700'" if bold else "",
               col, anchor, t))


class People:
    def __init__(self, rnd):
        self.pool = [(x, "she", "her") for x in GIRLS] + [(x, "he", "his") for x in BOYS]
        rnd.shuffle(self.pool)
        self.i = 0

    def next(self):
        p = self.pool[self.i % len(self.pool)]
        self.i += 1
        return p


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def mark_large(u, pattern):
    """Tag pictures that must print larger so their labels stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def balance(sets, rnd):
    """Spread the correct answers evenly over the 4 positions (5 each per set)."""
    for s in sets:
        targets = [0, 1, 2, 3] * 5
        rnd.shuffle(targets)
        for it, t in zip(s["items"], targets):
            c = it["c"]
            c[it["a"]], c[t] = c[t], c[it["a"]]
            it["a"] = t
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5), s["title"]


# ------------------------------------------------------------ pictures
def scale_svg(left, right, label):
    """A level pan balance. left / right: lists of 'x' (a block) or a number (a weight)."""
    def item_w(t):
        return 34 if t == "x" else max(34, int(tw(t, 16) + 14))
    gap = 6

    def pan_w(items):
        return max(80, sum(item_w(t) for t in items) + gap * (len(items) - 1) + 16)
    wl, wr = pan_w(left), pan_w(right)
    cl = 8 + wl / 2
    cr = cl + wl / 2 + 44 + wr / 2
    mid = (cl + cr) / 2
    top, ih = 10, 34
    py = top + ih
    s = []
    for items, c, w in ((left, cl, wl), (right, cr, wr)):
        tot = sum(item_w(t) for t in items) + gap * (len(items) - 1)
        x = c - tot / 2
        for t in items:
            iw = item_w(t)
            if t == "x":
                s.append("<rect x='%.1f' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='2'/>" % (x, top, iw, ih, FILL, GREEN))
                s.append(text(x + iw / 2, top + 24, "x", 18, col=RED, italic=True))
            else:
                s.append("<rect x='%.1f' y='%d' width='%d' height='%d' rx='6' fill='%s' stroke='%s' stroke-width='2'/>" % (x, top, iw, ih, GREY, INK))
                s.append(text(x + iw / 2, top + 23, t))
            x += iw + gap
        s.append("<rect x='%.1f' y='%d' width='%.1f' height='6' fill='%s'/>" % (c - w / 2, py, w, INK))
        s.append("<rect x='%.1f' y='%d' width='4' height='18' fill='%s'/>" % (c - 2, py + 6, INK))
    by = py + 24
    s.append("<rect x='%.1f' y='%d' width='%.1f' height='6' fill='%s'/>" % (cl - 2, by, cr - cl + 4, INK))
    s.append("<path d='M%.1f %d L%.1f %d L%.1f %d Z' fill='%s'/>" % (mid, by + 6, mid - 22, by + 40, mid + 22, by + 40, GREEN))
    s.append("<rect x='%.1f' y='%d' width='80' height='5' fill='%s'/>" % (mid - 40, by + 40, INK))
    W = int(cr + wr / 2 + 8)
    return svg_wrap(W, by + 47, "".join(s), "pan balance: " + label)


GAP, PAD, FS = 30, 30, 15


def nline(lo, rel, k, label=None):
    """Number line from lo to lo + 10. Circle at k: open for > <, closed for >= <=.
    A thick green arrow shows the solutions."""
    hi = lo + 10
    assert lo <= k <= hi
    W = 2 * PAD + GAP * 10
    Y, H = 24, 56
    X = lambda v: PAD + GAP * (v - lo)
    L, R = PAD - 22, W - PAD + 22
    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.8'/>" % (L + 2, Y, R - 2, Y, INK),
         "<path d='M%d %d L%d %d L%d %d Z' fill='%s'/>" % (L, Y, L + 9, Y - 5, L + 9, Y + 5, INK),
         "<path d='M%d %d L%d %d L%d %d Z' fill='%s'/>" % (R, Y, R - 9, Y - 5, R - 9, Y + 5, INK)]
    for v in range(lo, hi + 1):
        x = X(v)
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.6'/>" % (x, Y - 6, x, Y + 6, INK))
        s.append(text(x, Y + 26, str(v), FS))
    xc = X(k)
    end = R - 1 if RIGHT[rel] else L + 1
    tip = 12 if RIGHT[rel] else -12
    s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='5'/>" % (xc, Y, end - tip, Y, GREEN))
    s.append("<path d='M%d %d L%d %d L%d %d Z' fill='%s'/>" % (end, Y, end - tip, Y - 8, end - tip, Y + 8, GREEN))
    s.append("<circle cx='%d' cy='%d' r='7' fill='%s' stroke='%s' stroke-width='2.5'/>"
             % (xc, Y, GREEN if CLOSED[rel] else "#ffffff", GREEN))
    return svg_wrap(W, H, "".join(s), label or "number line graph")


def window(rnd, k):
    return max(0, k - rnd.choice([3, 4, 5, 6, 7]))


def describe(rel, k):
    return "%s circle at %d, arrow to the %s" % ("Closed" if CLOSED[rel] else "Open", k, "right" if RIGHT[rel] else "left")


def why_graph(rel, k, v="x"):
    circ = ("a closed (filled-in) circle, because %d is a solution" if CLOSED[rel]
            else "an open circle, because %d is not a solution") % k
    side = "right, toward greater numbers" if RIGHT[rel] else "left, toward lesser numbers"
    return "%s has %s, and the arrow points %s." % (sol(v, rel, k), circ, side)


# ------------------------------------------------------------ explanations
def steps2(a, op, b, c, v="x"):
    """Undo + or − first, then undo ×."""
    x = solve2(a, op, b, c)
    mid = c - b if op == "+" else c + b
    undo = ("Subtract %d from both sides" % b) if op == "+" else ("Add %d to both sides" % b)
    return ("%s: %s = %d. Then divide both sides by %d: %s = %d ÷ %d = %d. Check: %s."
            % (undo, term(a, v), mid, a, V(v), mid, a, x, calc(a, op, b, x)))


def wrong2(a, op, b, c):
    """Answers from real mistakes, most common first."""
    if op == "+":
        return [c - b, F(c + b, a), F(c, a) - b, (c - b) * a, c - b - a, F(c, a)]
    return [c + b, F(c - b, a), F(c, a) + b, (c + b) * a, c + b - a, F(c, a)]


# ------------------------------------------------------------ set 1: one-step and two-step equations
def set_two_step(rnd, P):
    its = []
    # one-step equations with their own mistakes
    its.append(mcq_n("Solve: %s + 17 = 45" % V("x"), 28, [62, 32, 45],
                     "Undo + 17 by subtracting 17 from both sides: %s = 45 − 17 = 28. Check: 28 + 17 = 45. "
                     "(32 comes from subtracting 5 − 7 as 7 − 5. 62 comes from adding 17.)" % V("x"), rnd))
    its.append(mcq_n("Solve: %s − 23 = 58" % V("n"), 81, [35, 71, 58],
                     "Undo − 23 by adding 23 to both sides: %s = 58 + 23 = 81. Check: 81 − 23 = 58. "
                     "(35 comes from subtracting instead of adding. 71 forgets to regroup.)" % V("n"), rnd))
    its.append(mcq_n("Solve: 6%s = 54" % V("y"), 9, [48, 60, 324],
                     "6%s means 6 × %s. Undo × 6 by dividing both sides by 6: %s = 54 ÷ 6 = 9. Check: 6 × 9 = 54." % (V("y"), V("y"), V("y")), rnd))
    its.append(mcq_n("Solve: %s ÷ 4 = 9" % V("m"), 36, [13, 5, 9],
                     "Undo ÷ 4 by multiplying both sides by 4: %s = 9 × 4 = 36. Check: 36 ÷ 4 = 9. "
                     "(13 is 9 + 4 and 5 is 9 − 4, but the operation to undo is ÷ 4.)" % V("m"), rnd))
    # pan balances
    for k, b, c in [(3, 5, 26), (2, 9, 23)]:
        x = solve2(k, "+", b, c)
        svg = scale_svg(["x"] * k + [str(b)], [str(c)], "%d blocks x and %d balance %d" % (k, b, c))
        e = ("The balance shows %s. Take %d off both pans: %s = %d. %d equal blocks make %d, so each block is %d ÷ %d = %d. Check: %s."
             % (eq(k, "+", b, c), b, term(k, "x"), c - b, k, c - b, c - b, k, x, calc(k, "+", b, x)))
        its.append(mcq_n(fig(svg) + "The pan balance is level. Each block has the same mass, %s. What is %s?" % (V("x"), V("x")),
                         x, wrong2(k, "+", b, c), e, rnd))
    # what to do first
    its.append(mcq("What is the best first step to solve %s?" % eq(3, "+", 5, 26),
                   "Subtract 5 from both sides",
                   ["Divide 26 by 3", "Add 5 to both sides", "Subtract 3 from both sides"],
                   "Undo the operations in reverse order. 3%s + 5 means “multiply by 3, then add 5,” so first undo the + 5 by "
                   "subtracting 5 from both sides: 3%s = 21. Dividing only 26 by 3 leaves out the 5 and gives a decimal." % (V("x"), V("x")), rnd))
    its.append(mcq("What is the best first step to solve %s?" % eq(4, "-", 7, 29, "n"),
                   "Add 7 to both sides",
                   ["Divide 29 by 4", "Subtract 7 from both sides", "Add 4 to both sides"],
                   "4%s − 7 means “multiply by 4, then subtract 7.” Undo the last operation first: add 7 to both sides to get 4%s = 36. "
                   "Then divide by 4: %s = 9." % (V("n"), V("n"), V("n")), rnd))
    # two-step equations, easier to harder
    T = [(3, "+", 6, 27, "x"), (2, "+", 9, 31, "y"), (4, "+", 8, 44, "n"), (4, "-", 3, 25, "m"),
         (3, "-", 6, 24, "k"), (5, "+", 10, 65, "x"), (6, "-", 12, 30, "p"), (8, "-", 5, 51, "a"),
         (7, "+", 14, 84, "t"), (9, "+", 4, 76, "n"), (5, "-", 15, 35, "y"), (12, "+", 6, 90, "x")]
    for a, op, b, c, v in T:
        x = solve2(a, op, b, c)
        e = steps2(a, op, b, c, v)
        w = wrong2(a, op, b, c)
        if whole(w[2]):
            e += " Dividing first (%d ÷ %d, then %s %d) gives %d, which is wrong." % (
                c, a, "subtract" if op == "+" else "add", b, int(w[2]))
        else:
            e += " Do not stop at %s = %d: you still need to divide by %d." % (term(a, v), c - b if op == "+" else c + b, a)
        its.append(mcq_n("Solve: %s" % eq(a, op, b, c, v), x, w, e, rnd))
    return {"title": "One-step and two-step equations", "items": its}


# ------------------------------------------------------------ set 2: equations with more than one term
def set_terms(rnd, P):
    its = []
    # simplify
    its.append(mcq("Simplify: 2%s + 3%s + 4" % (V("x"), V("x")), "5%s + 4" % V("x"),
                   ["9%s" % V("x"), "6%s + 4" % V("x"), "5%s" % V("x")],
                   "2%s and 3%s are like terms: 2 + 3 = 5, so 2%s + 3%s = 5%s. 4 has no %s, so it stays: 5%s + 4. "
                   "Do not multiply 2 × 3, and do not add the 4 to the %s terms." % ((V("x"),) * 5 + (V("x"), V("x"), V("x"))), rnd))
    its.append(mcq("Simplify: 7%s − 2%s + 3" % (V("n"), V("n")), "5%s + 3" % V("n"),
                   ["9%s + 3" % V("n"), "8%s" % V("n"), "5%s" % V("n")],
                   "7%s − 2%s = 5%s (7 − 2 = 5). Keep the + 3: 5%s + 3. Watch the sign: 7%s − 2%s is not 9%s."
                   % ((V("n"),) * 7), rnd))
    its.append(mcq("Simplify: %s + %s + %s + 6" % (V("y"), V("y"), V("y")), "3%s + 6" % V("y"),
                   ["9%s" % V("y"), "%s + 6" % V("y"), "3%s" % V("y")],
                   "Each %s is 1%s, so %s + %s + %s = 3%s. The 6 is not a %s term, so it stays: 3%s + 6."
                   % ((V("y"),) * 8), rnd))

    def item(q_eq, x, cands, e, v, notes=None):
        its.append(mcq_n("Solve: %s" % q_eq, x, cands, e, rnd, notes=notes))

    def T(a, v):
        return term(a, v)

    # ax + bx = c
    for a, b, c, v in [(2, 3, 35, "x"), (4, 2, 48, "n"), (3, 6, 72, "y"), (6, 4, 90, "p")]:
        x = F(c, a + b)
        assert x.denominator == 1
        x = int(x)
        e = ("Combine the like terms: %s + %s = %s. Then divide: %s = %d ÷ %d = %d. Check: %d × %d + %d × %d = %d."
             % (T(a, v), T(b, v), T(a + b, v), V(v), c, a + b, x, a, x, b, x, c))
        item("%s + %s = %d" % (T(a, v), T(b, v), c), x,
             [F(c, a * b), F(c, a), F(c, b), c - a - b, F(c - b, a), F(c - a, b)], e, v,
             ["multiplying %d × %d instead of adding" % (a, b), "leaving out %s" % T(b, v), "leaving out %s" % T(a, v),
              "subtracting %d and %d from %d" % (a, b, c), "treating %s as the number %d" % (T(b, v), b),
              "treating %s as the number %d" % (T(a, v), a)])
    # ax − bx = c
    a, b, c, v = 8, 2, 60, "m"
    x = c // (a - b)
    item("%s %s %s = %d" % (T(a, v), M, T(b, v), c), x, [F(c, a + b), F(c, b), c - (a - b), F(c, a)],
         "%s %s %s = %s (8 − 2 = 6). Then %s = 60 ÷ 6 = 10. Check: 80 − 20 = 60. Adding 8 + 2 gives the wrong answer 6."
         % (T(a, v), M, T(b, v), T(6, v), V(v)), v)
    # x + x + 4 = 20 style
    item("%s + %s + 4 = 20" % (V("x"), V("x")), 8, [16, 12, 4],
         "%s + %s = 2%s, so 2%s + 4 = 20. Subtract 4: 2%s = 16. Divide by 2: %s = 8. Check: 8 + 8 + 4 = 20. "
         "16 is only %s + %s, not one %s." % ((V("x"),) * 6 + (V("x"), V("x"), V("x"))), "x")
    item("10 + %s + %s = 34" % (V("k"), V("k")), 12, [24, 22, 44],
         "%s + %s = 2%s, so 10 + 2%s = 34. Subtract 10: 2%s = 24. Divide by 2: %s = 12. Check: 10 + 12 + 12 = 34. 24 is 2%s, not %s, and 22 comes from adding 10 instead of subtracting it."
         % ((V("k"),) * 8), "k")
    item("%s + 2%s + 4%s = 56" % (V("x"), V("x"), V("x")), 8, [7, 49, 14, 28],
         "%s is 1%s, so %s + 2%s + 4%s = 7%s (1 + 2 + 4 = 7). Then %s = 56 ÷ 7 = 8. Check: 8 + 16 + 32 = 56. "
         "Forgetting the 1 gives 6%s, and multiplying 2 × 4 gives 8%s." % ((V("x"),) * 9), "x")
    item("3%s + 2%s + 5%s = 80" % (V("w"), V("w"), V("w")), 8, [16, 70, 15],
         "3 + 2 + 5 = 10, so 10%s = 80 and %s = 8. Check: 24 + 16 + 40 = 80. "
         "16 uses only 3%s + 2%s, and 15 treats 5%s as the number 5." % ((V("w"),) * 5), "w")
    item("2%s + 2%s + 2%s = 54" % (V("a"), V("a"), V("a")), 9, [27, 18, 48],
         "2 + 2 + 2 = 6, so 6%s = 54 and %s = 54 ÷ 6 = 9. Check: 18 + 18 + 18 = 54. 27 uses only one 2%s." % ((V("a"),) * 3), "a")
    # combine, then two steps
    for a, b, op, d, c, v in [(2, 4, "+", 6, 54, "x"), (3, 1, "+", 8, 48, "n"), (5, 2, "-", 7, 63, "k"),
                              (7, -3, "+", 4, 40, "y"), (4, 2, "+", 3, 39, "x")]:
        s = a + b
        x = solve2(s, op, d, c)
        bt = ("%s %s %s" % (T(a, v), M, T(-b, v))) if b < 0 else ("%s + %s" % (T(a, v), T(b, v)))
        if (a, b) == (4, 2):
            q = "%s + %d + %s = %d" % (T(a, v), d, T(b, v), c)
        else:
            q = "%s %s %d = %d" % (bt, osym(op), d, c)
        e = ("Combine the like terms first: %s = %s. Now solve %s. %s"
             % (bt, T(s, v), eq(s, op, d, c, v), steps2(s, op, d, c, v)))
        if b == 1:
            e += " Remember that %s means 1%s, so 3%s + %s = 4%s, not 3%s." % ((V(v),) * 6)
        mid = c - d if op == "+" else c + d
        cands = wrong2(s, op, d, c)[:3] + [F(mid, a * b) if b > 1 else None, F(mid, a), F(c, s)]
        notes = ["forgetting to divide by %d" % s,
                 "%s %d instead of %s it" % ("adding" if op == "+" else "subtracting", d, "subtracting" if op == "+" else "adding"),
                 "dividing by %d before %s %d" % (s, "subtracting" if op == "+" else "adding", d),
                 "multiplying %d × %d instead of adding" % (a, b),
                 ("treating %s as just %s" % (bt, T(a, v))) if b > 0 else "leaving out %s" % T(-b, v),
                 "leaving out the %d" % d]
        item(q, x, cands, e, v, notes)
    # several constants
    item("12 + %s + 15 = 50" % V("x"), 23, [77, 38, 35],
         "Combine the numbers first: 12 + 15 = 27, so %s + 27 = 50. Subtract 27: %s = 23. Check: 12 + 23 + 15 = 50. "
         "38 and 35 subtract only one of the numbers." % (V("x"), V("x")), "x")
    item("9 + 2%s + 5 + 3%s = 64" % (V("n"), V("n")), 10, [50, 25, 11],
         "Combine like terms: 2%s + 3%s = 5%s and 9 + 5 = 14. So 5%s + 14 = 64. Subtract 14: 5%s = 50. Divide by 5: %s = 10. "
         "Check: 9 + 20 + 5 + 30 = 64." % ((V("n"),) * 6), "n")
    assert len(its) == 20, len(its)
    return {"title": "Equations with more than one term", "items": its}


# ------------------------------------------------------------ set 3: check a solution
MIST_PLUS = ["Added %d instead of subtracting %d", "Forgot to divide by %d", "Divided by %d before subtracting %d",
             "Multiplied by %d instead of dividing"]
MIST_MINUS = ["Subtracted %d instead of adding %d", "Forgot to divide by %d", "Divided by %d before adding %d",
              "Multiplied by %d instead of dividing"]


def mistake_vals(a, op, b, c):
    w = wrong2(a, op, b, c)
    return [w[1], w[0], w[2], w[3]]          # same order as MIST_*


def mistake_texts(a, op, b):
    t = MIST_PLUS if op == "+" else MIST_MINUS
    return [t[0] % (b, b), t[1] % a, t[2] % (a, b), t[3] % a]


def set_check(rnd, P):
    its = []
    # a) which equation has this solution?
    for x, a, op, b in [(6, 3, "+", 4), (8, 5, "-", 7), (9, 4, "+", 6), (7, 6, "-", 5), (12, 2, "+", 9)]:
        c = val(a, op, b, x)
        other = "-" if op == "+" else "+"
        wr = [(b, op, a), (a, other, b)]
        for ca, cop, cb in wr:
            assert val(ca, cop, cb, x) != c
        add_all = x + a + b if op == "+" else x + a - b
        assert add_all != c
        right = eq(a, op, b, c)
        wrong = [eq(ca, cop, cb, c) for ca, cop, cb in wr] + ["%s + %d %s %d = %d" % (V("x"), a, osym(op), b, c)]
        e = ("Put %d in for %s in each one. %s ✓. The others are false: %s; %s; %d + %d %s %d = %d."
             % (x, V("x"), calc(a, op, b, x), calc(b, op, a, x), calc(a, other, b, x), x, a, osym(op), b, add_all))
        its.append(mcq("Which equation has %s = %d as its solution?" % (V("x"), x), right, wrong, e, rnd))
    # b) is it a solution? which check is right?
    for a, op, b, x0, d in [(3, "+", 5, 7, 0), (5, "+", 4, 6, 1), (4, "-", 9, 8, 0),
                            (6, "-", 2, 5, -1), (2, "+", 13, 9, 0), (7, "+", 3, 4, 1)]:
        c = val(a, op, b, x0)
        x = x0 + d
        digits = "%d%d %s %d = %d" % (a, x, osym(op), b, val(1, op, b, int("%d%d" % (a, x))))
        q = "Is %s = %d a solution of %s? Which check is correct?" % (V("x"), x, eq(a, op, b, c))
        if d == 0:
            right = "Yes, because %s" % calc(a, op, b, x)
            wrong = ["No, because %s" % digits,
                     "No, because %d + %d %s %d = %d" % (a, x, osym(op), b, val(1, op, b, a + x)),
                     "No, because %d %s %d = %d, not %d" % (c, osym("-" if op == "+" else "+"), b,
                                                           c - b if op == "+" else c + b, x)]
            e = ("Put %d in for %s: %s. Both sides are equal, so %d is a solution. %s means %d × %s, not the number %d%d."
                 % (x, V("x"), calc(a, op, b, x), x, term(a, "x"), a, V("x"), a, x))
        else:
            mid = c - b if op == "+" else c + b
            right = "No, because %s, not %d" % (calc(a, op, b, x), c)
            wrong = ["Yes, because %d %s %d = %d and %d ÷ %d = %d" % (c, osym("-" if op == "+" else "+"), b, mid, mid, a, x),
                     "No, because %s" % digits,
                     "No, because %d × %d = %d, not %d" % (a, x, a * x, c)]
            assert mid != a * x
            e = ("Put %d in for %s: %s. That is not %d, so %d is not a solution. (The solution is %d.) "
                 "%d ÷ %d is %d, not %d, and you must check the whole left side, %s."
                 % (x, V("x"), calc(a, op, b, x), c, x, x0, mid, a, x0, x, lhs(a, op, b)))
        its.append(mcq(q, right, wrong, e, rnd))
    # c) find the mistake
    for a, op, b, c, k in [(2, "+", 9, 31, 0), (3, "+", 6, 33, 2), (4, "+", 7, 43, 1),
                           (5, "-", 5, 40, 0), (6, "-", 3, 45, 3), (4, "-", 8, 36, 2)]:
        nm, he, his = P.next()
        mv = mistake_vals(a, op, b, c)
        got = whole(mv[k])
        assert got, (a, op, b, c, k)
        assert all(F(v) != mv[k] for i, v in enumerate(mv) if i != k)
        x = solve2(a, op, b, c)
        texts = mistake_texts(a, op, b)
        q = "%s solved %s and got %s = %d. What mistake did %s make?" % (nm, eq(a, op, b, c), V("x"), got, he)
        e = ("Check: %s, not %d, so %d is wrong. %s. The right way: %s"
             % (calc(a, op, b, got), c, got, {0: "Using the wrong inverse operation gives %d",
                                              1: "Stopping after the first step gives %d",
                                              2: "Undoing in the wrong order gives %d",
                                              3: "Multiplying gives %d"}[k] % got, steps2(a, op, b, c)))
        its.append(mcq(q, texts[k], [t for i, t in enumerate(texts) if i != k], e, rnd))
    # d) which check shows it
    for x, a, op, b in [(9, 4, "-", 6), (7, 5, "+", 8), (11, 3, "+", 7)]:
        c = val(a, op, b, x)
        right = "%d × %d %s %d = %d %s %d = %d" % (a, x, osym(op), b, a * x, osym(op), b, c)
        dig = int("%d%d" % (a, x))
        wrong = ["%d %s %d = %d" % (dig, osym(op), b, val(1, op, b, dig)),
                 "%d + %d %s %d = %d" % (a, x, osym(op), b, val(1, op, b, a + x)),
                 "%d %s %d = %d and %d × %d = %d" % (x, osym(op), b, val(1, op, b, x), val(1, op, b, x), a, a * val(1, op, b, x))]
        e = ("%s means %d × %s. Multiply first, then %s: %s. The left side equals %d, so %s = %d is correct."
             % (term(a, "x"), a, V("x"), "add" if op == "+" else "subtract", right, c, V("x"), x))
        its.append(mcq("Which work correctly checks that %s = %d is the solution of %s?" % (V("x"), x, eq(a, op, b, c)),
                       right, wrong, e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Check a solution", "items": its}


# ------------------------------------------------------------ set 4: inequalities with two operations
def ineq_bound(a, op, b, c):
    return solve2(a, op, b, c)


def set_ineq(rnd, P):
    its = []
    # a) solve
    for a, op, b, rel, c in [(2, "+", 1, "<", 15), (3, "+", 4, ">", 19), (4, "-", 3, "<=", 25),
                             (5, "+", 10, ">=", 45), (6, "-", 4, "<", 50), (8, "+", 6, "<=", 94)]:
        k = ineq_bound(a, op, b, c)
        w = whole(F(c + b, a) if op == "+" else F(c - b, a))
        cands = [(sol("x", OPP[rel], k), (OPP[rel], k)), (sol("x", SWAP[rel], k), (SWAP[rel], k))]
        if w and w != k:
            cands.append((sol("x", rel, w), (rel, w)))
        mid = c - b if op == "+" else c + b
        cands.append((sol("x", rel, mid), (rel, mid)))
        e = ("Solve it like an equation. %s: %s %s %d. Divide both sides by %d: %s. "
             "The sign stays %s, and %s %s the number itself."
             % ("Subtract %d from both sides" % b if op == "+" else "Add %d to both sides" % b,
                term(a, "x"), SYM[rel], mid, a, sol("x", rel, k), SYM[rel], SYM[rel],
                "includes" if CLOSED[rel] else "does not include"))
        its.append(mcq("Solve: %s" % ineq_s(a, op, b, rel, c), (sol("x", rel, k), (rel, k)), cands, e, rnd))
    # b) graph -> which inequality
    for (a, op, b, rel, c), alt in [((3, "+", 2, "<", 20), (3, "+", 2, "<", 26)),
                                    ((2, "-", 4, ">=", 10), (2, "+", 4, ">=", 10)),
                                    ((4, "+", 1, ">", 33), (4, "+", 9, ">", 33)),
                                    ((5, "-", 5, "<=", 20), (5, "+", 5, "<=", 20))]:
        k = ineq_bound(a, op, b, c)
        ka = ineq_bound(*alt[:3], alt[4])
        assert ka != k
        svg = nline(window(rnd, k), rel, k, "number line graph of x %s %d" % (PSYM[rel], k))
        right = ineq_s(a, op, b, rel, c)
        wrong = [ineq_s(a, op, b, SWAP[rel], c), ineq_s(a, op, b, OPP[rel], c), ineq_s(alt[0], alt[1], alt[2], alt[3], alt[4])]
        e = ("The graph shows %s: %s circle at %d, arrow to the %s. Solve %s: %s, so %s. "
             "%s gives %s instead."
             % (sol("x", rel, k), "a closed" if CLOSED[rel] else "an open", k, "right" if RIGHT[rel] else "left",
                right, "%s %s %d" % (term(a, "x"), SYM[rel], c - b if op == "+" else c + b), sol("x", rel, k),
                ineq_s(*alt), sol("x", alt[3], ka)))
        its.append(mcq(fig(svg) + "The graph shows the solution of which inequality?", right, wrong, e, rnd))
    # c) how to graph
    for a, op, b, rel, c in [(4, "+", 3, ">=", 23), (2, "+", 7, "<", 21), (3, "-", 5, ">", 13)]:
        k = ineq_bound(a, op, b, c)
        right = describe(rel, k)
        wrong = [describe(SWAP[rel], k), describe(OPP[rel], k), describe(OPP[SWAP[rel]], k)]
        e = "First solve: %s gives %s. %s" % (ineq_s(a, op, b, rel, c), sol("x", rel, k), why_graph(rel, k))
        its.append(mcq("How do you graph the solution of %s on a number line?" % ineq_s(a, op, b, rel, c), right, wrong, e, rnd))
    # d) verify: which number is (not) a solution
    for a, op, b, rel, c, r, ws, want in [(3, "+", 4, ">", 19, 6, [5, 4, 2], True),
                                          (2, "+", 5, ">=", 21, 8, [7, 6, 3], True),
                                          (4, "-", 2, "<", 30, 7, [8, 9, 12], True),
                                          (5, "+", 3, "<=", 48, 10, [9, 8, 2], False)]:
        assert holds(val(a, op, b, r), rel, c) == want
        for x in ws:
            assert holds(val(a, op, b, x), rel, c) != want
        tests = "; ".join("%s → %d %s %d is %s" % (calc(a, op, b, x), val(a, op, b, x), SYM[rel], c,
                                                  "true" if holds(val(a, op, b, x), rel, c) else "false") for x in [r] + ws)
        q = "Which number is %s a solution of %s?" % ("" if want else "<b>not</b>", ineq_s(a, op, b, rel, c))
        q = q.replace("is  a", "is a")
        k = ineq_bound(a, op, b, c)
        e = "Test each number. %s. The solution is %s." % (tests, sol("x", rel, k))
        its.append(mcq_n(q, r, ws, e, rnd))
    # e) find the mistake in a graph
    for (a, op, b, rel, c), drawn, kdrawn in [((2, "+", 5, "<=", 17), "<", 6),
                                              ((3, "-", 1, ">", 14), "<", 5),
                                              ((4, "+", 2, ">=", 30), ">=", 8)]:
        nm, he, his = P.next()
        k = ineq_bound(a, op, b, c)
        svg = nline(window(rnd, min(k, kdrawn)), drawn, kdrawn, "number line graph of x %s %d" % (PSYM[drawn], kdrawn))
        if kdrawn != k:
            right = "The circle should be at %d" % k
            wrong = ["The circle should be open", "The arrow should point left", "Nothing is wrong"]
            why = "%s added %d instead of subtracting it: (%d + %d) ÷ %d = %d." % (nm, b, c, b, a, kdrawn)
        elif CLOSED[drawn] != CLOSED[rel]:
            right = "The circle should be %s" % ("closed (filled in)" if CLOSED[rel] else "open")
            wrong = ["The arrow should point %s" % ("left" if RIGHT[drawn] else "right"), "The circle should be at %d" % (k + 1), "Nothing is wrong"]
            why = "%s used the wrong circle." % nm
        else:
            right = "The arrow should point %s" % ("right" if RIGHT[rel] else "left")
            wrong = ["The circle should be closed (filled in)", "The circle should be at %d" % (k + 1), "Nothing is wrong"]
            why = "%s drew the arrow the wrong way." % nm
        q = fig(svg) + "%s solved %s and drew this graph. What is wrong?" % (nm, ineq_s(a, op, b, rel, c))
        e = "%s gives %s. %s %s" % (ineq_s(a, op, b, rel, c), sol("x", rel, k), why_graph(rel, k), why)
        its.append(mcq(q, right, wrong, e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Solve and graph inequalities", "items": its}


# ------------------------------------------------------------ set 5: word problems
def set_words(rnd, P):
    its = []
    # 1 hockey tape: which equation
    n1, he, his = P.next()
    its.append(mcq("%s buys a $14 hockey stick bag and 3 rolls of tape. Each roll costs the same, %s dollars. "
                   "%s pays $29 in all. Which equation fits?" % (n1, V("t"), cap(he)),
                   eq(3, "+", 14, 29, "t"),
                   [eq(14, "+", 3, 29, "t"), "3 + %s + 14 = 29" % V("t"), "3%s = 29 + 14" % V("t")],
                   "3 rolls at %s dollars each cost 3%s. Add the $14 bag: 3%s + 14 = 29. (Solving it: 3%s = 15, so each roll costs $5.)"
                   % ((V("t"),) * 4), rnd))
    # 2 skating rink
    its.append(mcq_n("A family pays $12 to rent skates for everyone, plus $4 per person to get into the skating rink. "
                     "They pay $36 in all. Solve 4%s + 12 = 36 to find the number of people." % V("p"), 6, [24, 12, 9],
                     steps2(4, "+", 12, 36, "p") + " 9 forgets the $12 rental.", rnd, " people"))
    # 3 maple syrup
    n3, he, his = P.next()
    its.append(mcq_n("At a sugar shack, %s buys a $9 tin of maple cookies and some bottles of maple syrup at $9 each. "
                     "%s spends $54. How many bottles of syrup did %s buy?" % (n3, cap(he), he), 5, [45, 7, 6],
                     "Let %s be the number of bottles: 9%s + 9 = 54. %s The answer 6 forgets the cookies." % (V("b"), V("b"), steps2(9, "+", 9, 54, "b")),
                     rnd, " bottles"))
    # 4 field trip
    its.append(mcq_n("A Grade 6 field trip to the science centre costs $15 per student plus $90 for the bus. "
                     "The total cost is $450. How many students are going?", 24, [360, 36, 30],
                     "15%s + 90 = 450. %s 360 is the cost for the students, not the number of students."
                     % (V("s"), steps2(15, "+", 90, 450, "s")), rnd, " students"))
    # 5 Terry Fox Run
    n5, he, his = P.next()
    its.append(mcq_n("For the Terry Fox Run, %s has already collected $35 in donations. %s aunt will give $5 for every "
                     "kilometre %s runs. How many kilometres must %s run to raise $85 in all?" % (n5, cap(his), he, he),
                     10, [50, 24, 17],
                     "5%s + 35 = 85. %s" % (V("k"), steps2(5, "+", 35, 85, "k")), rnd, " km"))
    # 6 canoe trip: which equation
    its.append(mcq("A canoe trip is 38 km long. The group paddles the same distance, %s km, on each of the first 3 days and "
                   "5 km on the last morning. Which equation fits?" % V("d"),
                   eq(3, "+", 5, 38, "d"),
                   [eq(5, "+", 3, 38, "d"), "3 + %s + 5 = 38" % V("d"), "3%s = 38 + 5" % V("d")],
                   "3 days of %s km is 3%s. Add the last 5 km: 3%s + 5 = 38. (Then 3%s = 33, so %s = 11 km a day.)"
                   % ((V("d"),) * 5), rnd))
    # 7 hockey wins
    n7, he, his = P.next()
    its.append(mcq_n("%s’s hockey team won some games in October and 3 times as many in November. They won 24 games in all. "
                     "How many games did they win in October?" % n7, 6, [8, 21, 18],
                     "Let %s be the October wins. November is 3%s. %s + 3%s = 24, so 4%s = 24 and %s = 6. "
                     "18 is the number of November wins." % ((V("w"),) * 6), rnd, " games"))
    # 8 garden perimeter
    its.append(mcq_n("A rectangular garden is 3 times as long as it is wide. Its perimeter is 48 m. "
                     "What is the width?", 6, [12, 24, 18],
                     "Let %s be the width. The sides are %s, 3%s, %s and 3%s: %s + 3%s + %s + 3%s = 8%s = 48, so %s = 6 m. "
                     "(The length is 18 m. 12 forgets that a rectangle has two widths and two lengths.)"
                     % ((V("w"),) * 11), rnd, " m"))
    # 9 isosceles triangle
    its.append(mcq_n("An isosceles triangle has two equal sides, each %s cm, and a base of 10 cm. Its perimeter is 34 cm. "
                     "How long is each equal side?" % V("s"), 12, [24, 22, 8],
                     "2%s + 10 = 34. %s 8 treats all three sides as equal." % (V("s"), steps2(2, "+", 10, 34, "s")), rnd, " cm"))
    # 10 Thanksgiving cookies
    n10, he, his = P.next()
    its.append(mcq_n("For Thanksgiving, %s bakes 4 trays of cookies with the same number on each tray, plus 8 extra cookies. "
                     "%s has 56 cookies. How many cookies are on each tray?" % (n10, cap(he)), 12, [48, 16, 6],
                     "4%s + 8 = 56. %s" % (V("c"), steps2(4, "+", 8, 56, "c")), rnd, " cookies"))
    # 11 movies
    n11, he, his = P.next()
    its.append(mcq_n("%s and 2 friends go to a movie. Each ticket costs the same. They also share a $12 popcorn. "
                     "They spend $45 in all. What does one ticket cost?" % n11, 11, [33, 19, 15],
                     "3 tickets: 3%s + 12 = 45. %s 15 forgets the popcorn." % (V("t"), steps2(3, "+", 12, 45, "t")), rnd))
    for it in its[-1:]:
        it["c"] = ["$" + c for c in it["c"]]
    # 12 money left
    n12, he, his = P.next()
    its.append(mcq_n("%s has $60. %s buys 4 pairs of winter mitts that cost the same. %s has $16 left. "
                     "What does one pair cost?" % (n12, cap(he), cap(he)), 11, [44, 19, 15],
                     "60 − 4%s = 16. 4%s is the amount spent: 60 − 16 = 44, so 4%s = 44 and %s = 11. "
                     "Check: 60 − 44 = 16. 44 is the total spent, not the cost of one pair." % ((V("m"),) * 4), rnd))
    its[-1]["c"] = ["$" + c for c in its[-1]["c"]]
    # 13 age
    n13, he, his = P.next()
    its.append(mcq_n("%s’s dad is 42. That is 6 more than 3 times %s’s age. How old is %s?" % (n13, n13, n13), 12, [36, 16, 8],
                     "Let %s be %s’s age: 3%s + 6 = 42. %s" % (V("a"), n13, V("a"), steps2(3, "+", 6, 42, "a")), rnd, " years old"))
    # 14 words -> equation
    its.append(mcq("Which equation means “6 more than twice a number %s is 30”?" % V("n"),
                   eq(2, "+", 6, 30, "n"),
                   [eq(6, "+", 2, 30, "n"), "2%s = 30 + 6" % V("n"), "%s + 2 + 6 = 30" % V("n")],
                   "“Twice a number” is 2%s. “6 more than” means add 6: 2%s + 6 = 30. (Then %s = 12.)" % ((V("n"),) * 3), rnd))
    # 15 CN Tower
    its.append(mcq("The CN Tower in Toronto is 553 m tall. That is 13 m more than 4 times the height %s of an office tower. "
                   "Which equation fits?" % V("h"),
                   eq(4, "+", 13, 553, "h"),
                   [eq(13, "+", 4, 553, "h"), "4%s = 553 + 13" % V("h"), "%s + 4 + 13 = 553" % V("h")],
                   "4 times the height is 4%s. 13 m more: 4%s + 13 = 553. (Then 4%s = 540, so %s = 135 m.)" % ((V("h"),) * 4), rnd))
    # 16 snowplow
    its.append(mcq_n("After a snowstorm, a snowplow has already cleared 12 km of road. It clears 6 km each hour. "
                     "How many more hours until it has cleared 60 km?", 8, [48, 12, 10],
                     "6%s + 12 = 60. %s 10 forgets the 12 km already done." % (V("h"), steps2(6, "+", 12, 60, "h")), rnd, " hours"))
    # 17 inequality: notebooks
    n17, he, his = P.next()
    its.append(mcq_n("%s has $50. %s buys a $14 book and some notebooks at $6 each. %s spends at most $50, so "
                     "6%s + 14 ≤ 50. What is the greatest number of notebooks %s can buy?" % (n17, cap(he), cap(he), V("n"), he),
                     6, [36, 8, 10],
                     "Subtract 14: 6%s ≤ 36. Divide by 6: %s ≤ 6. Check: 6 × 6 + 14 = 50, which is allowed. "
                     "7 notebooks would cost 6 × 7 + 14 = 56, too much. 8 forgets the book." % (V("n"), V("n")), rnd, " notebooks"))
    # 18 canoe weight: which inequality
    n18, he, his = P.next()
    its.append(mcq("A canoe can carry at most 270 kg. %s and %s dad weigh 120 kg together. Each pack of gear is 15 kg. "
                   "Which inequality shows the number of packs %s they can bring?" % (n18, his, V("p")),
                   ineq_s(15, "+", 120, "<=", 270, "p"),
                   [ineq_s(15, "+", 120, ">=", 270, "p"), ineq_s(15, "+", 120, "<", 270, "p"), ineq_s(120, "+", 15, "<=", 270, "p")],
                   "%s packs weigh 15%s kg. Add the 120 kg of people. “At most 270” means 270 is allowed, so use ≤: %s. "
                   "(Solving it: %s ≤ 10 packs.)" % (V("p"), V("p"), ineq_s(15, "+", 120, "<=", 270, "p"), V("p")), rnd))
    # 19 class points
    its.append(mcq_n("A class has 35 points. They earn 5 points each day. They get a pizza party when they have <b>more than</b> 80 points, "
                     "so 5%s + 35 &gt; 80. What is the least number of days they need?" % V("d"), 10, [9, 45, 23],
                     "Subtract 35: 5%s &gt; 45. Divide by 5: %s &gt; 9. 9 days gives exactly 80 points, which is not more than 80, "
                     "so the least whole number is 10." % (V("d"), V("d")), rnd, " days"))
    # 20 graph description
    n20, he, his = P.next()
    its.append(mcq("%s’s ringette team has 10 points and gets 3 points for each win. They need at least 40 points, "
                   "so 3%s + 10 ≥ 40. How do you graph the solution?" % (n20, V("w")),
                   describe(">=", 10), [describe(">", 10), describe("<=", 10), describe("<", 10)],
                   "3%s ≥ 30, so %s ≥ 10. %s" % (V("w"), V("w"), why_graph(">=", 10, "w")), rnd))
    assert len(its) == 20, len(its)
    return {"title": "Equation and inequality word problems", "items": its}


# ------------------------------------------------------------ lesson
def body_html():
    bal = scale_svg(["x", "x", "x", "5"], ["26"], "3 blocks x and 5 balance 26")
    g1 = nline(0, "<", 7, "number line graph of x < 7")
    g2 = nline(2, ">=", 5, "number line graph of x ≥ 5")
    X = V("x")
    return (
        "<h2>What is an equation?</h2>"
        "<p>An <b>equation</b> says that two sides have the same value, like a level pan balance. "
        "A letter such as %s stands for an unknown number. 3%s means 3 × %s.</p>"
        "<p>To <b>solve</b> an equation, find the value of the letter that makes both sides equal.</p>" % (X, X, X) +
        "<h2>Solve two-step equations</h2>"
        "<p>Undo the operations in <b>reverse order</b>. 3%s + 5 means “multiply by 3, then add 5”. "
        "So undo the + 5 first, then undo the × 3. Do the same thing to both sides.</p>" % X +
        table(["Operation", "Undo it with"], [["+ 5", M + " 5"], [M + " 7", "+ 7"], ["× 3", "÷ 3"], ["÷ 4", "× 4"]]) +
        "<figure class='sn-fig'>" + bal +
        "<figcaption>3%s + 5 = 26. Take 5 off both pans: 3%s = 21. Each block is 21 ÷ 3 = 7.</figcaption></figure>" % (X, X) +
        ex("Example 1", "Solve %s." % eq(4, "-", 7, 29),
           "Add 7 to both sides: 4%s = 36. Divide both sides by 4: %s = 9. Check: 4 × 9 − 7 = 29." % (X, X), "%s = 9" % X) +
        "<h2>Equations with more than one term</h2>"
        "<p>First <b>combine like terms</b>. Add the numbers in front of the letter: 2%s + 3%s = 5%s. "
        "A letter on its own means 1 of it: %s + 2%s = 3%s. Then solve.</p>" % (X, X, X, X, X, X) +
        ex("Example 2", "Solve 2%s + 4%s + 6 = 54." % (X, X),
           "Combine: 6%s + 6 = 54. Subtract 6: 6%s = 48. Divide by 6: %s = 8." % (X, X, X), "%s = 8" % X) +
        "<h2>Check (verify) a solution</h2>"
        "<p>Put the answer back in place of the letter and work out the left side. If both sides are equal, the answer is right.</p>" +
        ex("Example 3", "Is %s = 8 a solution of 2%s + 4%s + 6 = 54?" % (X, X, X),
           "2 × 8 + 4 × 8 + 6 = 16 + 32 + 6 = 54. Both sides are 54.", "Yes") +
        "<h2>Inequalities with two operations</h2>"
        "<p>An <b>inequality</b> uses &lt;, &gt;, ≤ or ≥. Solve it with the same steps as an equation. "
        "The answer is a range of numbers, not just one.</p>" +
        ex("Example 4", "Solve 2%s + 1 &lt; 15 and graph the solution." % X,
           "Subtract 1: 2%s &lt; 14. Divide by 2: %s &lt; 7. Check one number: 2 × 6 + 1 = 13, and 13 &lt; 15 is true. "
           "Check 7: 2 × 7 + 1 = 15, and 15 &lt; 15 is false." % (X, X), "%s &lt; 7" % X) +
        "<figure class='sn-fig'>" + g1 +
        "<figcaption>%s &lt; 7: open circle at 7 (7 is not a solution), arrow to the left.</figcaption></figure>" % X +
        table(["Symbol", "Circle", "Arrow"], [
            ["&lt;", "open", "left"], ["≤", "closed (filled in)", "left"],
            ["&gt;", "open", "right"], ["≥", "closed (filled in)", "right"]]) +
        "<figure class='sn-fig'>" + g2 +
        "<figcaption>3%s − 4 ≥ 11 gives %s ≥ 5: closed circle at 5 (5 is a solution), arrow to the right.</figcaption></figure>" % (X, X) +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Dividing first in 3%s + 6 = 27 (27 ÷ 3 − 6 = 3)" % X, "Undo + 6 first: 3%s = 21, so %s = 7" % (X, X)],
            ["Adding 5 in 3%s + 5 = 26" % X, "Undo + 5 with − 5"],
            ["Stopping at 3%s = 21" % X, "Finish: divide by 3 to get %s = 7" % X],
            ["2%s + 3%s = 6%s" % (X, X, X), "Add like terms: 2%s + 3%s = 5%s" % (X, X, X)],
            ["Reading 3%s with %s = 7 as 37" % (X, X), "3%s means 3 × 7 = 21" % X],
            ["A closed circle for &lt; or &gt;", "Closed circles are only for ≤ and ≥"],
        ])
    )


FAQ = [
    {"q": "What do Grade 6 students learn about equations and inequalities in the Ontario math curriculum?",
     "a": "In Grade 6 (Algebra, C2), students solve equations with more than one term and whole numbers, such as 3x + 5 = 26 or 2x + 3x = 35, and check their solutions. They also solve inequalities with two operations, like 2x + 1 < 15, and graph the solutions on a number line."},
    {"q": "How do you solve a two-step equation like 3x + 5 = 26?",
     "a": "Undo the operations in reverse order. Subtract 5 from both sides to get 3x = 21, then divide both sides by 3 to get x = 7. Check: 3 × 7 + 5 = 26."},
    {"q": "How is solving an inequality different from solving an equation?",
     "a": "You use the same steps, but the answer is a range of numbers instead of one number. 2x + 1 < 15 gives x < 7, so every number less than 7 works, but 7 does not."},
    {"q": "When do you use an open or a closed circle on a number line?",
     "a": "Use an open circle for < and >, because the number itself is not a solution. Use a closed (filled-in) circle for ≤ and ≥, because the number is included."},
]


def gen_unit():
    rnd = random.Random(36811)
    P = People(rnd)
    sets = [set_two_step(rnd, P), set_terms(rnd, P), set_check(rnd, P), set_ineq(rnd, P), set_words(rnd, P)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        for it in s["items"]:
            assert len({plain(c) for c in it["c"]}) == 4, it
            assert it["e"], it
            assert it["q"].count("<svg") <= 1
            assert "\\" not in it["q"] + "".join(it["c"]) + it["e"]
            k = plain(it["q"])
            assert k not in seen, it["q"]
            seen.add(k)
    return {
        "country": "ca-on", "subject": "math", "grade": "grade-6", "slug": "equations-and-inequalities", "sort": 11,
        "updated": UPDATED, "pdf_url": "",
        "title": "Equations and Inequalities: Two-Step Equations, Checking Solutions and Graphing",
        "seo_title": "Grade 6 Equations and Inequalities Worksheets: Free Math with Answer Key (Ontario Curriculum)",
        "short_title": "Equations and Inequalities",
        "domain": "Algebra",
        "standard_code": "Grade 6: Algebra, C2",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Solve equations that involve multiple terms and whole numbers in various contexts, and verify solutions; solve inequalities that involve two operations and whole numbers up to 100, and verify and graph the solutions",
        "meta_desc": "Free Grade 6 math worksheets on equations and inequalities for the Ontario curriculum: two-step equations like 3x + 5 = 26, equations with more than one term, checking solutions, and inequalities like 2x + 1 < 15 graphed on a number line. 100 questions with an answer key, good EQAO practice.",
        "key_big": "Undo the operations in reverse order: 3x + 5 = 26, so 3x = 21 and x = 7.",
        "key_sub": "Check by putting the answer back in: 3 × 7 + 5 = 26. Inequalities use the same steps: 2x + 1 < 15 gives x < 7, graphed with an open circle at 7.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen_unit()
    mark_large(u, "number line")
    os.makedirs(OUT, exist_ok=True)
    path_ = os.path.join(OUT, u["slug"] + ".json")
    with open(path_, "w", encoding="utf-8") as f:
        json.dump(u, f, ensure_ascii=False, indent=1)
    print("wrote", path_)
