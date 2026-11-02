# -*- coding: utf-8 -*-
"""
US Grade 6 Math: Inequalities x > c, x < c (6.EE.B.8)
  python tools/gen_us_math_g6_inequalities.py
An inequality is stored as (variable, op, c) with op in > < >= <= and c a Fraction.
Every answer is checked in code: solutions with holds(), equal-meaning choices with canon().
HTML: &lt; and &gt; are escaped, ≤ and ≥ are plain characters, variables are in italics.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, os, random, re
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "us", "math", "grade-6")
UPDATED = "2026-11-02"
GREEN = "#006633"
INK = "#2b2b2b"
GRAY = "#8a8a8a"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Maya", "Ava", "Mia", "Zoe", "Lily", "Emma", "Nora", "Ruby", "Sofia", "Grace"]
BOYS = ["Leo", "Noah", "Eli", "Sam", "Ben", "Omar", "Kai", "Jack", "Luis", "Owen"]

OPS = [">", "<", ">=", "<="]
SYM = {">": "&gt;", "<": "&lt;", ">=": "≥", "<=": "≤"}
WORDS = {">": "greater than", "<": "less than", ">=": "greater than or equal to", "<=": "less than or equal to"}
MIRROR = {">": "<", "<": ">", ">=": "<=", "<=": ">="}        # 6 < x is the same as x > 6
STRICT = {">": ">", "<": "<", ">=": ">", "<=": "<"}
CLOSED = {">": ">=", "<": "<=", ">=": ">=", "<=": "<="}
RIGHT = {">": True, ">=": True, "<": False, "<=": False}


# ------------------------------------------------------------ numbers and inequalities
def fr(a, b):
    return "<span class='fr'><span class='fn'>%s</span><span class='fd'>%d</span></span>" % (a, b)


def num(v):
    """Fraction -> text: commas, real minus sign, decimals for tenths and hundredths, mixed numbers otherwise."""
    v = F(v)
    neg = v < 0
    a = -v if neg else v
    if a.denominator == 1:
        s = "{:,}".format(a.numerator)
    elif 100 % a.denominator == 0 and a.denominator in (10, 100, 5, 20, 50, 25):
        s = ("%.2f" % float(a)).rstrip("0").rstrip(".")
    elif a.denominator in (2, 4) and not neg:
        w, r = divmod(a.numerator, a.denominator)
        s = ("%d %s" % (w, fr(r, a.denominator))) if w else fr(r, a.denominator)
    else:
        s = ("%.2f" % float(a)).rstrip("0").rstrip(".")
    return ("−" + s) if neg else s


def dec(v):
    """Always a decimal (6.5, not 6 1/2)."""
    v = F(v)
    s = ("%.2f" % float(abs(v))).rstrip("0").rstrip(".")
    if abs(v) >= 1000:
        w, _, d = s.partition(".")
        s = "{:,}".format(int(w)) + ("." + d if d else "")
    return ("−" + s) if v < 0 else s


def V(var):
    return "<i>%s</i>" % var


def ineq(var, op, c, flip=False):
    if flip:
        return "%s %s %s" % (num(c), SYM[MIRROR[op]], V(var))
    return "%s %s %s" % (V(var), SYM[op], num(c))


def holds(v, op, c):
    v, c = F(v), F(c)
    return {">": v > c, "<": v < c, ">=": v >= c, "<=": v <= c}[op]


def canon(op, c, flip=False):
    """Meaning of ineq(var, op, c, flip): writing it the other way round does not change it."""
    return (op, F(c))


def cmp_text(v, op, c):
    """'7 &lt; 7 is false' style check."""
    return "%s %s %s is %s" % (num(v), SYM[op], num(c), "true" if holds(v, op, c) else "false")


# ------------------------------------------------------------ helpers
def mcq(q, correct, wrong, e, keys=None):
    """keys (optional): meaning of each choice (correct first). Choices with the same meaning are not allowed."""
    ch = [correct] + list(wrong)
    assert len(ch) == 4 and len(set(ch)) == 4, (q, ch)
    if keys is not None:
        assert len(keys) == 4 and len(set(keys)) == 4, (q, keys)
    return {"q": q, "c": ch, "a": 0, "e": e}


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


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
    """Move the correct choice so each position (A to D) is the answer 5 times in every set."""
    for st in sets:
        pos = [0, 1, 2, 3] * 5
        rnd.shuffle(pos)
        for it, t in zip(st["items"], pos):
            ch = it["c"]
            rest = ch[:it["a"]] + ch[it["a"] + 1:]
            rnd.shuffle(rest)
            rest.insert(t, ch[it["a"]])
            it["c"] = rest
            it["a"] = t


# ------------------------------------------------------------ number line picture
GAP, PAD, FS = 30, 30, 15


def nline(lo, op, c, label="number line graph"):
    """Number line from lo to lo + 10 (integers). Circle at c: open for > <, filled for >= <=.
    A thick green ray with an arrowhead shows the solutions."""
    hi = lo + 10
    assert lo <= c <= hi and F(c).denominator == 1
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
        s.append("<text x='%d' y='%d' font-size='%d' fill='%s' text-anchor='middle'>%s</text>"
                 % (x, Y + 26, FS, INK, num(v)))
    xc = X(c)
    end = R - 1 if RIGHT[op] else L + 1
    tip = 12 if RIGHT[op] else -12
    s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='5'/>" % (xc, Y, end - tip, Y, GREEN))
    s.append("<path d='M%d %d L%d %d L%d %d Z' fill='%s'/>" % (end, Y, end - tip, Y - 8, end - tip, Y + 8, GREEN))
    if op in (">=", "<="):
        s.append("<circle cx='%d' cy='%d' r='7' fill='%s' stroke='%s' stroke-width='2.5'/>" % (xc, Y, GREEN, GREEN))
    else:
        s.append("<circle cx='%d' cy='%d' r='7' fill='#ffffff' stroke='%s' stroke-width='2.5'/>" % (xc, Y, GREEN))
    return svg_wrap(W, H, "".join(s), label)


def window(rnd, c):
    k = rnd.choice([3, 4, 5, 6, 7])
    return int(c) - k


def describe(op, c):
    return "%s circle at %s, shaded to the %s" % ("Closed" if op in (">=", "<=") else "Open", num(c),
                                                   "right" if RIGHT[op] else "left")


def why_graph(op, c, var="x"):
    circ = ("closed (filled-in) circle, because %s itself is a solution" % num(c)) if op in (">=", "<=") else \
           ("open circle, because %s itself is not a solution" % num(c))
    side = "right, toward greater numbers" if RIGHT[op] else "left, toward lesser numbers"
    return "%s has an %s, and the arrow points %s." % (ineq(var, op, c), circ, side) if op in (">", "<") else \
           "%s has a %s, and the arrow points %s." % (ineq(var, op, c), circ, side)


# ------------------------------------------------------------ set 1: read and write inequalities
VARS = ["x", "y", "n", "m", "k", "p", "t", "w", "z", "r"]


def set_read(rnd):
    its = []
    vs = VARS[:]
    rnd.shuffle(vs)
    nums = rnd.sample(range(2, 41), 20)
    # A: meaning of an inequality
    for i, op in enumerate([">", "<", ">=", "<=", ">", "<"]):
        var, c = vs[i % 10], nums[i]
        right = "%s is %s %s" % (V(var), WORDS[op], num(c))
        wrong = ["%s is %s %s" % (V(var), WORDS[o], num(c)) for o in OPS if o != op]
        e = "Read from left to right: %s is %s %s. " % (V(var), WORDS[op], num(c))
        e += {">": "The symbol opens toward %s, the greater side." % V(var),
              "<": "The point of the symbol is toward %s, the lesser side." % V(var),
              ">=": "The line under the symbol means “or equal to,” so %s can also be %s." % (V(var), num(c)),
              "<=": "The line under the symbol means “or equal to,” so %s can also be %s." % (V(var), num(c))}[op]
        its.append(mcq("What does %s mean?" % ineq(var, op, c), right, wrong, e, keys=[op] + [o for o in OPS if o != op]))
    # B: words -> inequality (one wrong choice is written in the reverse order)
    for i, op in enumerate(["<", ">", "<=", ">=", "<", ">"]):
        var, c = vs[(i + 6) % 10], nums[6 + i]
        cand = [(MIRROR[op], True)] + [(o, False) for o in OPS if o not in (op, MIRROR[op])]
        keys = [canon(op, c)] + [canon(o, c, f) for o, f in cand]
        wrong = [ineq(var, o, c, flip=f) for o, f in cand]
        e = ("“%s is %s %s” is written %s, with %s first. %s says “%s is %s %s,” which is the opposite."
             % (V(var), WORDS[op], num(c), ineq(var, op, c), V(var), ineq(var, MIRROR[op], c, True),
                num(c), WORDS[op], V(var)))
        its.append(mcq("Which inequality means “%s is %s %s”?" % (V(var), WORDS[op], num(c)),
                       ineq(var, op, c), wrong, e, keys=keys))
    # C: c < x means x > c
    for i, op in enumerate([">", "<", ">=", "<="]):
        var, c = vs[(i + 2) % 10], nums[12 + i]
        mo = MIRROR[op]
        wrong_ops = [mo, CLOSED[op] if op in (">", "<") else STRICT[op], MIRROR[CLOSED[op] if op in (">", "<") else STRICT[op]]]
        keys = [op] + wrong_ops
        e = ("%s says “%s is %s %s.” Turn it around: %s is %s %s, so %s. The symbol still opens toward the greater side."
             % (ineq(var, op, c, True), num(c), WORDS[mo], V(var), V(var), WORDS[op], num(c), ineq(var, op, c)))
        its.append(mcq("Which inequality means the same as %s?" % ineq(var, op, c, True), ineq(var, op, c),
                       [ineq(var, o, c) for o in wrong_ops], e, keys=keys))
    # D: which sentence is true for c > x
    for i, op in enumerate(["<", ">", "<=", ">="]):
        var, c = vs[(i + 5) % 10], nums[16 + i]
        right = "%s is %s %s" % (V(var), WORDS[op], num(c))
        wrong_ops = [MIRROR[op], CLOSED[op] if op in (">", "<") else STRICT[op], MIRROR[CLOSED[op] if op in (">", "<") else STRICT[op]]]
        wrong = ["%s is %s %s" % (V(var), WORDS[o], num(c)) for o in wrong_ops]
        e = ("%s is read “%s is %s %s.” That means %s is %s %s." %
             (ineq(var, op, c, True), num(c), WORDS[MIRROR[op]], V(var), V(var), WORDS[op], num(c)))
        its.append(mcq("Which sentence means the same as %s?" % ineq(var, op, c, True), right, wrong, e,
                       keys=[op] + wrong_ops))
    return {"title": "Read and write inequalities", "items": its}


# ------------------------------------------------------------ set 2: solutions
def check_solution_item(op, c, right, wrongs, want=True):
    assert holds(right, op, c) == want
    for w in wrongs:
        assert holds(w, op, c) != want, (op, c, w)
    assert len({F(x) for x in [right] + list(wrongs)}) == 4


def e_test(op, c, vals, var="x"):
    return "Test each number in %s: %s." % (ineq(var, op, c), "; ".join(cmp_text(v, op, c) for v in vals))


def set_solutions(rnd):
    its = []
    # A: which number is a solution (7 items)
    A = [(">", 9, F(19, 2), [9, 8, 3]),
         ("<", 7, F(69, 10), [7, F(71, 10), 8]),
         (">=", 12, 12, [11, F(23, 2), 2]),
         ("<=", 15, 15, [16, F(31, 2), 20]),
         (">", -2, 0, [-2, -5, -3]),
         ("<", -4, -6, [-4, -2, 0]),
         (">", F(5, 2), 3, [F(5, 2), 2, F(3, 2)])]
    vs = VARS[:]
    rnd.shuffle(vs)
    for i, (op, c, r, w) in enumerate(A):
        c = F(c)
        check_solution_item(op, c, r, w, True)
        var = vs[i]
        e = e_test(op, c, [r] + w, var) + " Only %s makes it true." % num(r)
        if op in (">", "<") and F(c) in [F(x) for x in w]:
            e += " %s is not a solution, because %s is not %s itself." % (num(c), num(c), WORDS[op])
        if c < 0 and op == ">":
            e += " On a number line, −5 is to the left of −2, so −5 &lt; −2."
        if c < 0 and op == "<":
            e += " On a number line, −6 is to the left of −4, so −6 &lt; −4."
        if op in (">=", "<="):
            e += " ≥ and ≤ include the number itself."
        its.append(mcq("Which number is a solution of %s?" % ineq(var, op, c), num(r), [num(x) for x in w], e))
    # B: which number is NOT a solution (4 items)
    B = [(">", 5, 5, [F(51, 10), 6, 20]),
         ("<", 10, 10, [F(99, 10), 9, 0]),
         (">=", 8, F(15, 2), [8, F(17, 2), 30]),
         ("<=", -3, -2, [-3, -4, -10])]
    for i, (op, c, r, w) in enumerate(B):
        c = F(c)
        check_solution_item(op, c, r, w, False)
        var = vs[7 + i if 7 + i < 10 else i]
        e = e_test(op, c, [r] + w, var) + " %s is the only one that makes it false." % num(r)
        if F(r) == c:
            e += " The number itself is not a solution of %s." % ineq(var, op, c)
        its.append(mcq("Which number is <b>not</b> a solution of %s?" % ineq(var, op, c), num(r), [num(x) for x in w], e))
    # C: is c itself a solution? (4 items)
    for i, (op, c) in enumerate([(">", 7), ("<=", 11), ("<", 4), (">=", 20)]):
        var = vs[(i + 3) % 10]
        sol = holds(c, op, c)
        if op == ">":
            right = "No, because %s is not greater than %s" % (c, c)
            wrong = ["Yes, because %s = %s" % (c, c), "Yes, because %s is the number in the inequality" % c,
                     "No, because only numbers less than %s are solutions" % c]
        elif op == "<":
            right = "No, because %s is not less than %s" % (c, c)
            wrong = ["Yes, because %s = %s" % (c, c), "Yes, because %s is the number in the inequality" % c,
                     "No, because only numbers greater than %s are solutions" % c]
        elif op == "<=":
            right = "Yes, because %s = %s and ≤ includes equal" % (c, c)
            wrong = ["No, because %s is not less than %s" % (c, c), "No, the circle at %s is open" % c,
                     "Yes, because every number is a solution"]
        else:
            right = "Yes, because %s = %s and ≥ includes equal" % (c, c)
            wrong = ["No, because %s is not greater than %s" % (c, c), "No, the circle at %s is open" % c,
                     "Yes, because every number is a solution"]
        assert right.startswith("Yes") == sol
        e = "%s. %s" % (cap(cmp_text(c, op, c)),
                        "The sign has no “or equal to,” so %s is left out." % c if not sol else
                        "The line under the sign means “or equal to,” so %s is included." % c)
        its.append(mcq("Is %s a solution of %s?" % (c, ineq(var, op, c)), right, wrong, e))
    # D: which list has only solutions (3 items)
    D = [("<=", 4, [1, 3, 4], [[1, 3, 5], [4, 6, 8], [0, 2, 9]]),
         (">", 6, [F(13, 2), 7, 10], [[6, 7, 10], [2, 4, 8], [5, F(13, 2), 9]]),
         ("<", 0, [-1, F(-1, 2), -8], [[-1, 0, -3], [-4, -2, 2], [-5, -1, F(1, 2)]])]
    for i, (op, c, r, w) in enumerate(D):
        c = F(c)
        var = vs[(i + 6) % 10]
        assert all(holds(v, op, c) for v in r)
        for lst in w:
            assert not all(holds(v, op, c) for v in lst)
        fmt = lambda L: ", ".join(dec(v) for v in L)
        bad = [[v for v in lst if not holds(v, op, c)] for lst in w]
        e = ("Every number in %s makes %s true. Each other list has a number that does not work: %s."
             % (fmt(r), ineq(var, op, c), "; ".join("%s in %s" % (dec(b[0]), fmt(l)) for b, l in zip(bad, w))))
        its.append(mcq("Which list has <b>only</b> solutions of %s?" % ineq(var, op, c), fmt(r), [fmt(l) for l in w], e))
    # E: how many solutions (2 items)
    its.append(mcq("How many solutions does %s have?" % ineq("x", ">", 3), "Infinitely many",
                   ["Only 1, the number 4", "3", "None"],
                   "Every number greater than 3 works: 4, 3.5, 3.01, 100, 1,000,000 and so on. There is no end, so there are infinitely many solutions."))
    its.append(mcq("How many solutions does %s have?" % ineq("y", "<", 10), "Infinitely many",
                   ["9", "10", "Only the whole numbers 0 to 9"],
                   "Not just whole numbers work. 9.5, 2.25, 0 and −40 are also less than 10. There is no end, so there are infinitely many solutions."))
    return {"title": "Solutions of an inequality", "items": its}


# ------------------------------------------------------------ set 3: number line graphs
def set_graphs(rnd, P):
    its = []
    # A: graph -> inequality (10 items)
    cs = [4, -2, 7, 1, -5, 12, 0, 9, -3, 16]
    ops = [">", "<", ">=", "<=", ">", "<=", ">=", "<", ">=", "<"]
    for c, op in zip(cs, ops):
        c = F(c)
        svg = nline(window(rnd, c), op, c)
        wrong = [o for o in OPS if o != op]
        e = "The circle is at %s. %s, so the inequality is %s." % (
            num(c), ("The circle is open, so %s is not included" if op in (">", "<") else
                     "The circle is closed, so %s is included") % num(c) +
            ", and the arrow points %s (%s numbers)" % ("right" if RIGHT[op] else "left", "greater" if RIGHT[op] else "lesser"),
            ineq("x", op, c))
        its.append(mcq(fig(svg) + "Which inequality does the graph show?", ineq("x", op, c),
                       [ineq("x", o, c) for o in wrong], e, keys=[op] + wrong))
    # B: inequality -> description (4 items)
    for op, c in [("<=", 3), (">", 8), ("<", -1), (">=", 25)]:
        c = F(c)
        wrong = [describe(o, c) for o in OPS if o != op]
        its.append(mcq("Which describes the graph of %s on a number line?" % ineq("x", op, c), describe(op, c), wrong,
                       why_graph(op, c)))
    # C: find the mistake (4 items)
    for want, drawn, c in [(">=", ">", 2), ("<", ">", 6), ("<=", "<", -4), (">", "<", 10)]:
        c = F(c)
        n, he, his = P.next()
        if STRICT[want] == STRICT[drawn]:          # wrong circle
            right = "The circle should be %s" % ("closed (filled in)" if want in (">=", "<=") else "open")
            other = "The arrow should point the other way"
        else:                                       # wrong direction
            right = "The arrow should point to the %s" % ("right" if RIGHT[want] else "left")
            other = "The circle should be %s" % ("closed (filled in)" if drawn in (">", "<") else "open")
        wrong = [other, "The circle should be at %s" % num(c + 1), "Nothing is wrong"]
        svg = nline(window(rnd, c), drawn, c)
        q = fig(svg) + "%s graphed %s like this. What is wrong?" % (n, ineq("x", want, c))
        e = why_graph(want, c) + " %s’s graph shows %s instead." % (n, ineq("x", drawn, c))
        its.append(mcq(q, right, wrong, e))
    # D: graph -> a solution (2 items)
    for op, c, r, w in [("<", 5, 2, [5, 6, 9]), (">=", -1, -1, [-2, -4, F(-3, 2)])]:
        c = F(c)
        check_solution_item(op, c, r, w, True)
        svg = nline(window(rnd, c), op, c)
        e = ("The graph shows %s. %s" % (ineq("x", op, c), e_test(op, c, [r] + w)))
        if op == "<":
            e += " The open circle means %s is not included." % num(c)
        else:
            e += " The closed circle means %s is included." % num(c)
        its.append(mcq(fig(svg) + "Which number is a solution shown by the graph?", num(r), [num(x) for x in w], e))
    return {"title": "Graph inequalities on a number line", "items": its}


# ------------------------------------------------------------ set 4: words -> inequalities
PHRASE = {
    ">": [("is more than", "“More than %s” does not include %s, so use &gt;."),
          ("is greater than", "“Greater than %s” does not include %s, so use &gt;."),
          ("is over", "“Over %s” does not include %s, so use &gt;.")],
    "<": [("is less than", "“Less than %s” does not include %s, so use &lt;."),
          ("is under", "“Under %s” does not include %s, so use &lt;."),
          ("is below", "“Below %s” does not include %s, so use &lt;.")],
    ">=": [("is at least", "“At least %s” means %s or more, so use ≥."),
           ("is no less than", "“No less than %s” means %s or more, so use ≥.")],
    "<=": [("is at most", "“At most %s” means %s or less, so use ≤."),
           ("is no more than", "“No more than %s” means %s or less, so use ≤.")],
}


def set_words(rnd):
    its = []
    vs = VARS[:]
    rnd.shuffle(vs)
    nums = rnd.sample(range(3, 61), 20)
    # A: phrase -> inequality (10 items)
    order = [(">", 0), (">", 1), (">", 2), ("<", 0), ("<", 1), ("<", 2), (">=", 0), (">=", 1), ("<=", 0), ("<=", 1)]
    for i, (op, k) in enumerate(order):
        var, c = vs[i], nums[i]
        ph, why = PHRASE[op][k]
        wrong = [o for o in OPS if o != op]
        e = why % (c, c) + " The inequality is %s." % ineq(var, op, c)
        its.append(mcq("Which inequality shows “%s %s %s”?" % (V(var), ph, c), ineq(var, op, c),
                       [ineq(var, o, c) for o in wrong], e, keys=[op] + wrong))
    # B: minimum / maximum / or more / or fewer (4 items)
    MM = [(">=", "the minimum value of %s is %s", "The minimum is the least value allowed, so %s can be %s or more: %s."),
          ("<=", "the maximum value of %s is %s", "The maximum is the greatest value allowed, so %s can be %s or less: %s."),
          (">=", "%s is %s or more", "“Or more” includes the number, so %s can be %s or greater: %s."),
          ("<=", "%s is %s or fewer", "“Or fewer” includes the number, so %s can be %s or less: %s.")]
    for i, (op, t, why) in enumerate(MM):
        var, c = vs[(10 + i) % 10], nums[10 + i]
        txt = t % (V(var), c)
        wrong = [o for o in OPS if o != op]
        e = why % (V(var), c, ineq(var, op, c))
        its.append(mcq("Which inequality shows “%s”?" % txt, ineq(var, op, c),
                       [ineq(var, o, c) for o in wrong], e, keys=[op] + wrong))
    # C: inequality -> phrase (6 items)
    PH = {">": "is more than", "<": "is less than", ">=": "is at least", "<=": "is at most"}
    for i, op in enumerate(["<=", ">=", "<", ">", "<=", ">="]):
        var, c = vs[(14 + i) % 10], nums[14 + i]
        right = "%s %s %s" % (V(var), PH[op], c)
        wrong_ops = [o for o in OPS if o != op]
        wrong = ["%s %s %s" % (V(var), PH[o], c) for o in wrong_ops]
        e = "%s means %s is %s %s. %s" % (ineq(var, op, c), V(var), WORDS[op], c, {
            "<=": "“At most” means that number or less.", ">=": "“At least” means that number or more.",
            "<": "“Less than” leaves the number out.", ">": "“More than” leaves the number out."}[op])
        its.append(mcq("Which phrase means %s?" % ineq(var, op, c), right, wrong, e, keys=[op] + wrong_ops))
    return {"title": "Write inequalities from words", "items": its}


# ------------------------------------------------------------ set 5: word problems
def ineq_choices(var, op, c):
    wrong = [o for o in OPS if o != op]
    return ineq(var, op, c), [ineq(var, o, c) for o in wrong]


def set_problems(rnd, P):
    its = []
    # 1 roller coaster: at least
    h = rnd.choice([42, 44, 48, 52, 54])
    r, w = ineq_choices("h", ">=", h)
    its.append(mcq("To ride a roller coaster, you must be at least %d inches tall. Let %s be a rider’s height in inches. "
                   "Which inequality shows the heights that can ride?" % (h, V("h")), r, w,
                   "“At least %d” means %d inches or taller. A rider who is exactly %d inches can ride, so use ≥: %s." % (h, h, h, ineq("h", ">=", h))))
    # 2 who can ride: the boundary is included
    h2 = [x for x in [42, 44, 48, 52, 54] if x != h][rnd.randrange(4)]
    n, he, his = P.next()
    opts = [F(h2), F(h2) - F(1, 2), F(h2 - 1), F(h2 - 3)]
    assert holds(opts[0], ">=", h2) and not any(holds(x, ">=", h2) for x in opts[1:])
    its.append(mcq("A water slide says: “Riders must be at least %d inches tall.” Four friends measured their heights. "
                   "Which height is allowed on the slide?" % h2, "%s inches" % num(opts[0]),
                   ["%s inches" % num(x) for x in opts[1:]],
                   "The heights allowed are %s. %s is equal to %d, and ≥ includes equal, so it is allowed. The others are less than %d." %
                   (ineq("h", ">=", h2), num(h2), h2, h2)))
    # 3 kids under 12 eat free
    a = rnd.choice([10, 12, 13])
    r, w = ineq_choices("a", "<", a)
    its.append(mcq("At a restaurant, kids under %d eat free. Let %s be a child’s age in years. "
                   "Which inequality shows the ages that eat free?" % (a, V("a")), r, w,
                   "“Under %d” means less than %d. A child who is %d does not eat free, so use &lt;, not ≤: %s." % (a, a, a, ineq("a", "<", a))))
    # 4 budget
    n, he, his = P.next()
    b = rnd.choice([15, 20, 25, 30])
    r, w = ineq_choices("c", "<=", b)
    its.append(mcq("%s has $%d to spend on a gift. Let %s be the cost of the gift in dollars. "
                   "Which inequality shows the costs %s can pay?" % (n, b, V("c"), he), r, w,
                   "%s can spend all $%d or less, so the cost is at most %d: %s." % (n, b, b, ineq("c", "<=", b))))
    # 5 speed limit: which speed breaks it
    s = rnd.choice([35, 45, 55, 65])
    sp = [F(s + 2), F(s), F(s - 1), F(s - 10)]
    assert not holds(sp[0], "<=", s) and all(holds(x, "<=", s) for x in sp[1:])
    its.append(mcq("The speed limit on a road is %d miles per hour. The legal speeds are %s. "
                   "Which speed is <b>not</b> allowed?" % (s, ineq("s", "<=", s)),
                   "%d mph" % sp[0], ["%d mph" % x for x in sp[1:]],
                   "%d &gt; %d, so %d mph is over the limit. %d mph is exactly the limit, and ≤ includes it." % (s + 2, s, s + 2, s)))
    # 6 elevator: whole numbers only
    p = rnd.choice([10, 12, 15])
    its.append(mcq("A sign in an elevator says: “No more than %d people.” Let %s be the number of people. "
                   "Which numbers make sense as solutions?" % (p, V("p")),
                   "The whole numbers 0 to %d" % p,
                   ["Every number less than or equal to %d" % p, "Only %d" % p, "The whole numbers 0 to %d" % (p - 1)],
                   "%s, but you cannot have %s or −2 people. Only whole numbers make sense, and %d is allowed, so the solutions are 0, 1, 2, … , %d."
                   % (ineq("p", "<=", p), "3.5", p, p)))
    # 7 fewer than 30 students: greatest possible
    k = rnd.choice([25, 28, 30])
    its.append(mcq("A class has fewer than %d students. What is the greatest number of students the class could have?" % k,
                   str(k - 1), [str(k), str(k + 1), dec(F(2 * k - 1, 2))],
                   "“Fewer than %d” means %s, so %d is not allowed. Students come in whole numbers, so the greatest is %d. (%s students makes no sense.)"
                   % (k, ineq("s", "<", k), k, k - 1, dec(F(2 * k - 1, 2)))))
    # 8 more than 80 points: least whole number
    t = rnd.choice([70, 80, 90])
    its.append(mcq("To win a prize, you need a score of more than %d points. Scores are whole numbers. "
                   "What is the least score that wins?" % t,
                   str(t + 1), [str(t), str(t - 1), str(t + 10)],
                   "“More than %d” means %s, so %d does not win. The next whole number is %d. (%d also wins, but it is not the least.)"
                   % (t, ineq("s", ">", t), t, t + 1, t + 10)))
    # 9 temperature: infinitely many
    its.append(mcq("Water freezes when the temperature is below 32°F. Let %s be the temperature in °F. "
                   "How many temperatures are solutions of %s?" % (V("t"), ineq("t", "<", 32)),
                   "Infinitely many", ["31", "32", "Only the whole numbers from 0 to 31"],
                   "Any temperature less than 32 works: 31.9, 20, 0, −5 and so on. Temperatures do not have to be whole numbers, and there is no end, so there are infinitely many solutions."))
    # 10 bag limit: which weight is allowed
    L = rnd.choice([40, 50])
    bw = [F(L), F(2 * L + 1, 2), F(L + 1), F(L + 5)]
    assert holds(bw[0], "<=", L) and not any(holds(x, "<=", L) for x in bw[1:])
    its.append(mcq("An airline says a checked bag can weigh at most %d pounds. Which bag weight is allowed?" % L,
                   "%s pounds" % dec(bw[0]), ["%s pounds" % dec(x) for x in bw[1:]],
                   "“At most %d” means %s. %d = %d, so a %d-pound bag is allowed. The others are more than %d." % (L, ineq("w", "<=", L), L, L, L, L)))
    # 11 graph -> situation (>= 8)
    g = rnd.choice([8, 10, 12])
    svg = nline(window(rnd, g), ">=", g)
    its.append(mcq(fig(svg) + "Which rule could this graph show? (%s is age in years.)" % V("x"),
                   "You must be at least %d years old" % g,
                   ["You must be under %d years old" % g, "You must be over %d years old" % g, "You can be at most %d years old" % g],
                   "The closed circle at %d means %d is included, and the arrow points right. That is %s: %d or older, which is “at least %d.” “Over %d” would need an open circle."
                   % (g, g, ineq("x", ">=", g), g, g, g)))
    # 12 graph -> situation (< 5)
    svg = nline(window(rnd, 5), "<", 5)
    its.append(mcq(fig(svg) + "Which sentence could this graph show? (%s is the temperature in °F.)" % V("x"),
                   "The temperature was below 5°F",
                   ["The temperature was above 5°F", "The temperature was at most 5°F", "The temperature was at least 5°F"],
                   "The open circle at 5 means 5 is not included, and the arrow points left. That is %s, “below 5.” “At most 5” would need a closed circle."
                   % ineq("x", "<", 5)))
    # 13 field trip needs at least 15
    m = rnd.choice([15, 20, 24])
    r, w = ineq_choices("s", ">=", m)
    its.append(mcq("A field trip will happen only if at least %d students sign up. Let %s be the number of students who sign up. "
                   "Which inequality shows when the trip will happen?" % (m, V("s")), r, w,
                   "“At least %d” means %d or more. A common mistake is to use ≤ or &lt; because of the word “least.” The answer is %s." % (m, m, ineq("s", ">=", m))))
    # 14 phone data plan
    d = rnd.choice([5, 10, 15])
    r, w = ineq_choices("d", "<=", d)
    its.append(mcq("A phone plan lets you use no more than %d GB of data each month. Let %s be the data used in GB. "
                   "Which inequality matches the plan?" % (d, V("d")), r, w,
                   "“No more than %d” means %d or less, and %d is allowed: %s." % (d, d, d, ineq("d", "<=", d))))
    # 15 plant taller than 14 cm
    n, he, his = P.next()
    ph = rnd.choice([14, 18, 22])
    pv = [F(2 * ph + 1, 2), F(ph), F(2 * ph - 1, 2), F(ph - 2)]
    assert holds(pv[0], ">", ph) and not any(holds(x, ">", ph) for x in pv[1:])
    its.append(mcq("%s’s plant is taller than %d centimeters. Which could be the height of the plant?" % (n, ph),
                   "%s cm" % dec(pv[0]), ["%s cm" % dec(x) for x in pv[1:]],
                   "“Taller than %d” means %s. Only %s is greater than %d. A plant that is exactly %d cm is not taller than %d cm."
                   % (ph, ineq("h", ">", ph), dec(pv[0]), ph, ph, ph)))
    # 16 bake for at least 25 minutes
    bm = rnd.choice([25, 30, 35])
    r, w = ineq_choices("t", ">=", bm)
    its.append(mcq("A recipe says to bake the bread for at least %d minutes. Let %s be the baking time in minutes. "
                   "Which inequality shows the baking times?" % (bm, V("t")), r, w,
                   "“At least %d minutes” means %d minutes or longer: %s." % (bm, bm, ineq("t", ">=", bm))))
    # 17 elevator weight limit (commas)
    wl = rnd.choice([2000, 2500, 3000])
    r, w = ineq_choices("w", "<=", wl)
    its.append(mcq("An elevator can carry a maximum of %s pounds. Let %s be the weight it carries in pounds. "
                   "Which inequality shows the weights it can carry?" % (num(wl), V("w")), r, w,
                   "The maximum is the greatest weight allowed, and %s pounds itself is allowed: %s." % (num(wl), ineq("w", "<=", wl))))
    # 18 error analysis: minimum of 16 players
    n, he, his = P.next()
    mp = rnd.choice([11, 16, 18])
    its.append(mcq("A soccer league needs a minimum of %d players on each team. %s writes %s. Which is right?" % (mp, n, ineq("p", "<=", mp)),
                   "%s, because a minimum of %d means %d or more" % (ineq("p", ">=", mp), mp, mp),
                   ["%s is right, because a minimum is a small number" % ineq("p", "<=", mp),
                    "%s, because the minimum is not included" % ineq("p", ">", mp),
                    "%s, because the team must be smaller" % ineq("p", "<", mp)],
                   "A minimum is the least number allowed. A team can have %d players or more, so %s." % (mp, ineq("p", ">=", mp))))
    # 19 only four solutions?
    n, he, his = P.next()
    its.append(mcq("%s says %s has only 4 solutions: 4, 5, 6 and 7. Is %s right?" % (n, ineq("x", ">", 3), he),
                   "No. Every number greater than 3 works, so there are infinitely many",
                   ["Yes. Those are all the solutions", "No. 3 is also a solution", "No. Only 4 is a solution"],
                   "8, 3.5, 100 and 1,000 are also greater than 3. The solutions never end, so %s has infinitely many solutions. 3 is not one of them." % ineq("x", ">", 3)))
    # 20 school zone: graph description
    z = rnd.choice([15, 20, 25])
    its.append(mcq("In a school zone, cars must drive no faster than %d mph. Which describes the graph of the speeds %s?"
                   % (z, ineq("s", "<=", z)), describe("<=", z),
                   [describe(o, z) for o in [">", ">=", "<"]],
                   why_graph("<=", z, "s")))
    return {"title": "Inequality word problems", "items": its}


# ------------------------------------------------------------ lesson
def body_html():
    g1 = nline(-1, ">", 3, "number line graph of x greater than 3")
    g2 = nline(-4, "<=", 2, "number line graph of x less than or equal to 2")
    return (
        "<h2>What is an inequality?</h2>"
        "<p>An inequality compares two amounts that may not be equal. "
        "It uses one of four symbols. Read it from left to right.</p>" +
        table(["Symbol", "Read it as", "Example"], [
            ["&gt;", "is greater than", "%s: x is greater than 4" % ineq("x", ">", 4)],
            ["&lt;", "is less than", "%s: x is less than 4" % ineq("x", "<", 4)],
            ["≥", "is greater than or equal to", "%s: x is 4 or more" % ineq("x", ">=", 4)],
            ["≤", "is less than or equal to", "%s: x is 4 or less" % ineq("x", "<=", 4)],
        ]) +
        "<p>The open side of &gt; or &lt; faces the greater amount. 6 &lt; %s means the same as %s.</p>" % (V("x"), ineq("x", ">", 6)) +
        "<h2>Solutions</h2>"
        "<p>A <b>solution</b> is a value of the variable that makes the inequality true. "
        "%s has <b>infinitely many</b> solutions: 8, 7.5, 7.01, 100 and every other number greater than 7. "
        "But 7 itself is not a solution, because 7 &gt; 7 is false.</p>" % ineq("x", ">", 7) +
        ex("Example", "Which of these are solutions of %s? 5, 6, 6.5, 9" % ineq("x", ">=", 6),
           "Test each one. 5 ≥ 6 is false. 6 ≥ 6 is true, because ≥ includes equal. 6.5 ≥ 6 and 9 ≥ 6 are true.", "6, 6.5 and 9") +
        "<h2>Graph on a number line</h2>"
        "<p>Draw a circle at the number. Then shade the side with the solutions and draw an arrow, because the solutions go on forever.</p>" +
        table(["Symbol", "Circle", "Arrow"], [
            ["&gt;", "open (not included)", "right"],
            ["≥", "closed, filled in (included)", "right"],
            ["&lt;", "open (not included)", "left"],
            ["≤", "closed, filled in (included)", "left"],
        ]) +
        "<figure class='sn-fig'>" + g1 +
        "<figcaption>%s: open circle at 3, arrow to the right. 3 is not a solution, but 3.1 and 4 are.</figcaption></figure>" % ineq("x", ">", 3) +
        "<figure class='sn-fig'>" + g2 +
        "<figcaption>%s: closed circle at 2, arrow to the left. 2, 0 and −3 are all solutions.</figcaption></figure>" % ineq("x", "<=", 2) +
        "<h2>Write an inequality from words</h2>" +
        table(["Words", "Symbol", "Example"], [
            ["more than, greater than, over, above", "&gt;", "more than 10 people: %s" % ineq("p", ">", 10)],
            ["less than, fewer than, under, below", "&lt;", "under 12 years old: %s" % ineq("a", "<", 12)],
            ["at least, no less than, minimum, or more", "≥", "at least 48 inches tall: %s" % ineq("h", ">=", 48)],
            ["at most, no more than, maximum, or less", "≤", "no more than $20: %s" % ineq("c", "<=", 20)],
        ]) +
        ex("Example", "An elevator holds at most 12 people. Write an inequality and list the solutions.",
           "“At most 12” means 12 or fewer, so %s. People come in whole numbers, so the solutions that make sense are 0, 1, 2, … , 12." % ineq("p", "<=", 12),
           ineq("p", "<=", 12)) +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Using a closed circle for &gt; or &lt;", "Closed circles are only for ≥ and ≤"],
            ["Pointing the arrow the wrong way for %s" % ineq("x", "<", 3), "&lt; means lesser numbers, so the arrow points left"],
            ["Writing “at least 5” as %s" % ineq("x", "<", 5), "“At least 5” means 5 or more: %s" % ineq("x", ">=", 5)],
            ["Saying 7 is a solution of %s" % ineq("x", ">", 7), "7 &gt; 7 is false. Only numbers greater than 7 work"],
            ["Reading %s as “3 is less than x”" % ineq("x", "<", 3), "Read left to right: x is less than 3"],
            ["Thinking %s has only the solutions 4, 5, 6, …" % ineq("x", ">", 3), "Decimals and fractions like 3.5 work too: infinitely many"],
        ])
    )


FAQ = [
    {"q": "How do you write an inequality in 6th grade?",
     "a": "Choose a letter for the unknown and find the key words. “More than” is >, “less than” is <, “at least” is ≥ and “at most” is ≤. For example, “you must be at least 48 inches tall” is h ≥ 48."},
    {"q": "When do you use an open circle or a closed circle on a number line?",
     "a": "Use an open circle for > and <, because the number itself is not a solution. Use a closed (filled-in) circle for ≥ and ≤, because the number is included."},
    {"q": "Why does x > 5 have infinitely many solutions?",
     "a": "Every number greater than 5 makes it true, including decimals and fractions like 5.1 and 5 1/2. The numbers never end, so there are infinitely many solutions."},
    {"q": "Does “at least” mean greater than or less than?",
     "a": "“At least” means greater than or equal to (≥). “At least 10” means 10 or more, so 10 is included. “At most” means less than or equal to (≤)."},
]


def gen():
    rnd = random.Random(615)
    P = People(rnd)
    sets = [set_read(rnd), set_solutions(rnd), set_graphs(rnd, P), set_words(rnd), set_problems(rnd, P)]
    for s in sets:
        rnd.shuffle(s["items"])
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5), s["title"]
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert "\\" not in it["q"] + "".join(it["c"]) + it["e"]
            k = it["q"] + "|" + "|".join(sorted(it["c"]))
            assert k not in seen, it["q"]
            seen.add(k)
    u = {
        "country": "us", "subject": "math", "grade": "grade-6", "slug": "inequalities", "sort": 15,
        "updated": UPDATED, "pdf_url": "",
        "title": "Inequalities: Write, Solve and Graph x > c and x < c",
        "seo_title": "Grade 6 Inequalities Worksheets: Write Inequalities, Find Solutions and Graph on a Number Line",
        "short_title": "Inequalities",
        "domain": "Expressions and Equations",
        "standard_code": "6.EE.B.8",
        "standard_url": "https://www.thecorestandards.org/Math/Content/6/EE/B/8/",
        "standard_text": "Write an inequality of the form x > c or x < c to represent a constraint or condition in a real-world or mathematical problem. Recognize that inequalities of the form x > c or x < c have infinitely many solutions; represent solutions of such inequalities on number line diagrams.",
        "meta_desc": "Free Grade 6 inequalities worksheets: read and write inequalities with >, <, ≥ and ≤, test solutions, graph them on a number line with open and closed circles, and turn words like “at least” and “at most” into inequalities. 100 practice questions with answer key.",
        "key_big": "x > c has infinitely many solutions. Open circle for > and <, closed circle for ≥ and ≤.",
        "key_sub": "“At least 5” is x ≥ 5 and “at most 5” is x ≤ 5. 7 is not a solution of x > 7, because 7 > 7 is false.",
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
