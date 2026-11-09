# -*- coding: utf-8 -*-
"""
US Grade 7 Math: Simplifying Linear Expressions (7.EE.A.1, 7.EE.A.2)
  python tools/gen_us_math_g7_simplifying_expressions.py
Combine like terms, distribute, factor and rewrite expressions in context.
Wrong answers come from real mistakes: adding unlike terms (3x + 4 -> 7x), distributing to
only the first term, losing the negative sign when distributing or subtracting a group,
and taking out a factor from only one term.
"""
import random
from fractions import Fraction as F
from ws_common import (num, mcq, balance, B, table, example, write_unit, MINUS, fr)

R = random.Random(70601)
UPDATED = "2026-11-09"


def c(v, st):
    s = num(v, st)
    return s if s is not None else num(v, "f")


def imp(v):
    v = F(v)
    if v.denominator == 1:
        return num(v)
    return (MINUS if v < 0 else "") + fr(abs(v.numerator), v.denominator)


def lin(a, b, v="x", st="d"):
    """Expression a·v + b, written the usual way. Fractions are shown improper."""
    a, b = F(a), F(b)
    c = (lambda w, _s: imp(w)) if st == "f" else globals()["c"]
    V = "<i>%s</i>" % v
    parts = []
    if a != 0:
        if a == 1:
            parts.append(V)
        elif a == -1:
            parts.append(MINUS + V)
        else:
            parts.append(c(a, st) + V)
    if b != 0 or not parts:
        if parts:
            parts.append((" + " if b > 0 else " − ") + c(abs(b), st))
        else:
            parts.append(c(b, st))
    return "".join(parts)


def key(a, b):
    return (F(a), F(b))


def opt(a, b, v="x", st="d"):
    return (lin(a, b, v, st), key(a, b))


# ------------------------------------------------------------ set 1
def set_like_terms():
    its = []
    cases = [  # (terms text, a, b)
        ("3<i>x</i> + 5<i>x</i>", 8, 0, [(15, 0), (8, 0, "x2"), (2, 0)]),
        ("7<i>y</i> − 2<i>y</i>", 5, 0, [(9, 0), (-5, 0), (5, 0, "y2")]),
        ("4<i>x</i> + 3 + 2<i>x</i>", 6, 3, [(9, 0), (6, 0), (4, 5)]),
        ("9<i>a</i> + 4 − 3<i>a</i> − 1", 6, 3, [(12, 5), (6, 5), (9, 0)]),
        ("<i>x</i> + <i>x</i> + <i>x</i>", 3, 0, [(1, 3), (3, 3), (0, 3)]),
        ("5<i>m</i> − 8<i>m</i>", -3, 0, [(3, 0), (13, 0), (-13, 0)]),
        ("−2<i>x</i> + 7 + 6<i>x</i>", 4, 7, [(-8, 7), (11, 0), (8, 7)]),
        ("6 + 3<i>n</i> − 10 + <i>n</i>", 4, -4, [(3, -4), (4, 16), (0, 0)]),
        ("−4<i>p</i> − 5<i>p</i> + 2", -9, 2, [(-1, 2), (9, 2), (-7, 0)]),
        ("8<i>x</i> − 3 − 8<i>x</i>", 0, -3, [(16, -3), (0, 3), (-3, 0)]),
        ("2.5<i>x</i> + 1.5<i>x</i> − 4", 4, -4, [(0, 0), (4, 4), (1, -4)]),
        ("0.3<i>y</i> + 2 − 0.8<i>y</i>", F("-0.5"), 2, [(F("0.5"), 2), (F("1.1"), 2), (F("1.5"), 0)]),
        ("12<i>k</i> − 7 − 5<i>k</i> + 9", 7, 2, [(17, 2), (7, -16), (9, 0)]),
        ("−<i>x</i> + 4 − 3<i>x</i> − 4", -4, 0, [(-3, 0), (-4, -8), (-2, 0)]),
    ]
    var_of = {"x": "x", "y": "y", "a": "a", "m": "m", "n": "n", "p": "p", "k": "k"}
    for txt, a, b, wrongs in cases:
        v = [k for k in var_of if "<i>%s</i>" % k in txt][0]
        ws = []
        for w in wrongs:
            if len(w) == 3:
                ws.append((lin(w[0], w[1], v) + "<sup>2</sup>", ("sq", w[0])))
            else:
                ws.append(opt(w[0], w[1], v))
        e = "Combine the terms with %s, then combine the numbers. The answer is %s." % (v, lin(a, b, v))
        if any(len(w) == 2 and w[1] == 0 and b != 0 for w in wrongs):
            e += " A number and a term with %s are not like terms, so they cannot be added." % v
        its.append(mcq("Simplify %s." % B(txt), opt(a, b, v), ws, e))
    # like terms recognition
    its.append(mcq("Which pair are like terms?", ("4<i>x</i> and −9<i>x</i>", "a"),
                   [("4<i>x</i> and 4", "b"), ("4<i>x</i> and 4<i>y</i>", "c"), ("4<i>x</i> and <i>x</i><sup>2</sup>", "d")],
                   "Like terms have the same variable part. 4x and −9x both have x."))
    its.append(mcq("What is the coefficient of <i>x</i> in %s?" % B("7 − 5<i>x</i>"), ("−5", "a"), [("5", "b"), ("7", "c"), ("2", "d")],
                   "The coefficient is the number multiplying x, including its sign: 7 − 5x = 7 + (−5)x."))
    its.append(mcq("How many terms are in %s?" % B("3<i>x</i> − 4 + 2<i>y</i>"), ("3", 3), [("2", 2), ("4", 4), ("9", 9)],
                   "Terms are separated by + and − signs: 3x, −4 and 2y."))
    its.append(mcq("What is the constant term in %s?" % B("6<i>a</i> − 11"), ("−11", "a"), [("11", "b"), ("6", "c"), ("−5", "d")],
                   "The constant term is the number with no variable. Keep its sign: −11."))
    its.append(mcq("Which expression is equivalent to %s?" % B("5<i>x</i> + 2 + 3<i>x</i>"), opt(8, 2),
                   [opt(10, 0), opt(8, 0), ("10<i>x</i><sup>2</sup>", "sq")],
                   "5x + 3x = 8x and the 2 stays: 8x + 2."))
    its.append(mcq("Simplify %s." % B("<i>x</i> + 4<i>y</i> + 3<i>x</i> − <i>y</i>"),
                   ("4<i>x</i> + 3<i>y</i>", "a"), [("7<i>x</i><i>y</i>", "b"), ("4<i>x</i> + 5<i>y</i>", "c"), ("3<i>x</i> + 4<i>y</i>", "d")],
                   "x + 3x = 4x and 4y − y = 3y. x-terms and y-terms are not like terms, so the answer is 4x + 3y."))
    return {"title": "Combine like terms", "items": its}


# ------------------------------------------------------------ set 2
def dist_item(k, a, b, v="x", st="d"):
    """k(a·v + b)."""
    k, a, b = F(k), F(a), F(b)
    inner = lin(a, b, v, st)
    kt = c(k, st) if k not in (-1,) else MINUS
    txt = "%s(%s)" % (kt, inner)
    good = (k * a, k * b)
    ws = [(k * a, b), (k * a, -k * b), (-k * a, k * b), (a, k * b), (k * a + k * b, 0)]
    e = "Multiply %s by each term: %s × %s = %s and %s × %s = %s. So %s = %s." % (
        c(k, st), c(k, st), lin(a, 0, v, st) if a > 0 else "(" + lin(a, 0, v, st) + ")", lin(k * a, 0, v, st), c(k, st), c(b, st) if b >= 0 else "(" + c(b, st) + ")",
        c(k * b, st), txt, lin(*good, v=v, st=st))
    e += " Not %s: multiply both terms, not just the first." % lin(k * a, b, v, st)
    return mcq("Use the distributive property to expand %s." % B(txt), opt(*good, v=v, st=st),
               [opt(w[0], w[1], v, st) for w in ws], e)


def set_distribute():
    its = []
    for k, a, b in [(3, 1, 4), (5, 2, -3), (4, 3, 7), (2, 6, -1), (-2, 1, 5), (-3, 2, -4), (6, 1, -8), (-4, 5, 1),
                    (7, 2, 3), (-1, 3, -6), (10, F("0.5"), 2), (F("0.5"), 4, -6), (-5, 3, 2), (8, -1, 4), (F("1.5"), 2, 6),
                    (-6, -2, 3)]:
        its.append(dist_item(k, a, b))
    for k, a, b in [(F(1, 2), 6, 8), (F(2, 3), 9, -3), (F(-1, 4), 8, 12), (F(3, 5), 10, 5)]:
        its.append(dist_item(k, a, b, st="f"))
    return {"title": "The distributive property", "items": its}


# ------------------------------------------------------------ set 3
def set_dist_combine():
    its = []
    # p(ax + b) + (cx + d)
    for k, a, b, cc, d in [(2, 1, 3, 4, 1), (3, 2, -1, -5, 6), (4, 1, -2, 3, 5), (-2, 3, 1, 7, 0), (5, 1, 4, -2, -9), (-3, 2, -5, 1, 4)]:
        A, Bc = k * a + cc, k * b + d
        txt = "%s(%s) %s" % (c(k, "d"), lin(a, b), ("+ " + lin(cc, d)) if cc > 0 else ("− " + lin(-cc, -d)))
        ws = [(k * a + cc, b + d), (a + cc, k * b + d), (k * a - cc, k * b - d), (A + Bc, 0), (A, -Bc)]
        e = "Distribute first: %s(%s) = %s. Then combine like terms: %s." % (c(k, "d"), lin(a, b), lin(k * a, k * b), lin(A, Bc))
        its.append(mcq("Simplify %s." % B(txt), opt(A, Bc), [opt(*w) for w in ws], e))
    # subtracting a group
    for a, b, cc, d in [(5, 3, 2, 1), (7, -2, 3, 4), (4, 6, 1, -5), (9, 1, 9, 8), (3, -4, -2, -6), (6, 0, 2, 7)]:
        A, Bc = a - cc, b - d
        txt = "%s − (%s)" % (lin(a, b) if b == 0 else "(%s)" % lin(a, b), lin(cc, d))
        ws = [(a - cc, b + d), (a + cc, b - d), (a - cc, d - b), (A + Bc, 0), (a + cc, b + d)]
        e = "Subtracting a group subtracts every term: (%s) − (%s) = %s %s. Combine: %s. Not %s: the minus sign must reach both terms." % (
            lin(a, b), lin(cc, d), lin(a, b), ("− " + lin(cc, 0) if cc > 0 else "+ " + lin(-cc, 0)) + ("" if d == 0 else (" − %s" % c(d, "d") if d > 0 else " + %s" % c(-d, "d"))),
            lin(A, Bc), lin(a - cc, b + d))
        its.append(mcq("Simplify %s." % B(txt), opt(A, Bc), [opt(*w) for w in ws], e))
    # two groups
    for k1, a1, b1, k2, a2, b2 in [(2, 1, 3, 3, 1, -1), (4, 2, 1, -2, 1, 5), (3, 1, -4, 2, 3, 2), (5, 1, 2, -3, 1, 4),
                                   (-1, 2, 7, 4, 1, -2), (6, 1, -1, -2, 3, -3), (2, 5, 4, 3, -1, 2), (3, -2, 1, -4, 1, -2)]:
        A, Bc = k1 * a1 + k2 * a2, k1 * b1 + k2 * b2
        t2 = ("+ " + c(k2, "d")) if k2 > 0 else ("− " + c(-k2, "d"))
        txt = "%s(%s) %s(%s)" % (c(k1, "d") if k1 != -1 else MINUS, lin(a1, b1), t2, lin(a2, b2))
        ws = [(k1 * a1 + abs(k2) * a2, k1 * b1 + abs(k2) * b2), (k1 * a1 + k2 * a2, b1 + b2), (A, -Bc), (A + Bc, 0), (k1 * a1 + k2 * a2, k1 * b1 - k2 * b2)]
        e = "Distribute each group: %s and %s. Combine like terms: %s." % (lin(k1 * a1, k1 * b1), lin(k2 * a2, k2 * b2), lin(A, Bc))
        its.append(mcq("Simplify %s." % B(txt), opt(A, Bc), [opt(*w) for w in ws], e))
    return {"title": "Distribute, then combine", "items": its}


# ------------------------------------------------------------ set 4
def set_factor():
    its = []
    for g, a, b in [(3, 2, 5), (4, 3, -2), (5, 1, 4), (6, 2, -3), (7, 3, 1), (2, 5, 9), (8, 1, -3), (9, 2, 1), (4, 5, 3), (10, 3, -7)]:
        A, Bc = g * a, g * b
        good = ("%d(%s)" % (g, lin(a, b)), "g")
        ws = [("%d(%s)" % (g, lin(a, Bc)), "w1"), ("%d(%s)" % (g, lin(A, b)), "w2"), ("%d(%s)" % (g, lin(Bc, a)), "w3"),
              ("%d%s" % (g, lin(a, b)), "w4")]
        e = "The GCF of %d and %d is %d. %s ÷ %d = %s and %s ÷ %d = %s, so %s = %s. Check by distributing." % (
            A, abs(Bc), g, lin(A, 0), g, lin(a, 0), c(Bc, "d"), g, c(b, "d"), lin(A, Bc), good[0])
        its.append(mcq("Factor %s using the GCF." % B(lin(A, Bc)), good, ws, e))
    for g, a, b in [(-2, 3, -4), (-5, 1, 2)]:
        A, Bc = g * a, g * b
        good = ("%s(%s)" % (c(g, "d"), lin(a, b)), "g")
        ws = [("%s(%s)" % (c(g, "d"), lin(a, -b)), "w1"), ("%s(%s)" % (c(g, "d"), lin(-a, b)), "w2"), ("%s(%s)" % (c(-g, "d"), lin(a, b)), "w3")]
        e = "Take out %s: %s ÷ (%s) = %s and %s ÷ (%s) = %s. Check: %s(%s) = %s." % (
            c(g, "d"), lin(A, 0), c(g, "d"), lin(a, 0), c(Bc, "d"), c(g, "d"), c(b, "d"), c(g, "d"), lin(a, b), lin(A, Bc))
        its.append(mcq("Factor out %s from %s." % (B(c(g, "d")), B(lin(A, Bc))), good, ws, e))
    # rational coefficients
    for txt, a, b, ws, e in [
        ("<span class='fr'><span class='fn'>1</span><span class='fd'>2</span></span><i>x</i> + <span class='fr'><span class='fn'>1</span><span class='fd'>4</span></span><i>x</i>",
         F(3, 4), 0, [(F(2, 6), 0), (F(1, 8), 0), (F(2, 4), 0)], "Use a common denominator: 2/4 + 1/4 = 3/4, so the answer is 3/4 x."),
        ("<span class='fr'><span class='fn'>2</span><span class='fd'>3</span></span><i>x</i> − <span class='fr'><span class='fn'>1</span><span class='fd'>6</span></span><i>x</i> + 1",
         F(1, 2), 1, [(F(1, 3), 1), (F(1, 2), 0), (F(3, 2), 1)], "2/3 = 4/6, and 4/6 − 1/6 = 3/6 = 1/2. The answer is 1/2 x + 1."),
        ("<span class='fr'><span class='fn'>3</span><span class='fd'>4</span></span>(8<i>x</i> − 4)",
         6, -3, [(6, -4), (8, -3), (F(32, 3), F(-16, 3))], "3/4 × 8x = 6x and 3/4 × (−4) = −3. The answer is 6x − 3."),
        ("<i>x</i> − <span class='fr'><span class='fn'>1</span><span class='fd'>5</span></span><i>x</i>",
         F(4, 5), 0, [(F(-1, 5), 0), (F(6, 5), 0), (F(1, 5), 0)], "x is 5/5 x, and 5/5 − 1/5 = 4/5. The answer is 4/5 x."),
        ("0.4(5<i>x</i> + 15) − 2", 2, 4, [(2, 13), (F("5.4"), 13), (2, 6)], "0.4 × 5x = 2x and 0.4 × 15 = 6. Then 6 − 2 = 4: 2x + 4."),
        ("1.2<i>x</i> + 3 − 0.7<i>x</i> + 0.5", F("0.5"), F("3.5"), [(F("1.9"), F("3.5")), (F("0.5"), F("2.5")), (4, 0)], "1.2x − 0.7x = 0.5x and 3 + 0.5 = 3.5. The answer is 0.5x + 3.5."),
        ("−<span class='fr'><span class='fn'>1</span><span class='fd'>2</span></span>(6<i>x</i> − 10)", -3, 5, [(-3, -5), (3, 5), (-3, -10)],
         "−1/2 × 6x = −3x and −1/2 × (−10) = 5. The answer is −3x + 5."),
        ("2(<i>x</i> + <span class='fr'><span class='fn'>1</span><span class='fd'>2</span></span>) + <span class='fr'><span class='fn'>1</span><span class='fd'>2</span></span><i>x</i>",
         F(5, 2), 1, [(F(5, 2), F(1, 2)), (2, F(3, 2)), (F(3, 2), 1)], "2(x + 1/2) = 2x + 1. Then 2x + 1/2 x = 5/2 x. The answer is 5/2 x + 1.")]:
        st = "f" if "fr" in txt and "0." not in txt else "d"
        its.append(mcq("Simplify %s." % B(txt), opt(a, b, st=st), [opt(w[0], w[1], st=st) for w in ws], e))
    return {"title": "Factoring and rational coefficients", "items": its}


# ------------------------------------------------------------ set 5
def set_context():
    its = []
    q = [("A price <i>p</i> goes up by 5%. Which expression shows the new price?", "1.05<i>p</i>", ["0.05<i>p</i>", "<i>p</i> + 5", "5<i>p</i>"],
          "p + 0.05p = 1.05p. Both show the price plus 5% of the price."),
         ("A jacket costs <i>j</i> dollars and is 20% off. Which expression shows the sale price?", "0.8<i>j</i>", ["0.2<i>j</i>", "<i>j</i> − 20", "1.2<i>j</i>"],
          "j − 0.2j = 0.8j. You pay 80% of the price."),
         ("A rectangle has length <i>x</i> + 4 and width 3. Which expression is its perimeter?", "2<i>x</i> + 14", ["2<i>x</i> + 7", "3<i>x</i> + 12", "<i>x</i> + 14"],
          "P = 2(x + 4) + 2(3) = 2x + 8 + 6 = 2x + 14."),
         ("Each of 4 friends buys a ticket for <i>t</i> dollars and a $3 snack. Which expression is the total cost?", "4<i>t</i> + 12",
          ["4<i>t</i> + 3", "<i>t</i> + 12", "7<i>t</i>"], "4(t + 3) = 4t + 12. Each friend pays t + 3."),
         ("A square has side length <i>s</i> + 2. Which expression is its perimeter?", "4<i>s</i> + 8", ["4<i>s</i> + 2", "<i>s</i> + 8", "8<i>s</i>"],
          "P = 4(s + 2) = 4s + 8."),
         ("Ana has <i>n</i> dollars. Ben has $6 more than Ana. Which expression shows how much they have together?", "2<i>n</i> + 6",
          ["<i>n</i> + 6", "2<i>n</i> + 12", "6<i>n</i>"], "n + (n + 6) = 2n + 6."),
         ("A worker earns <i>h</i> dollars an hour and works 8 hours, then gets a $15 bonus. Which expression shows the pay?", "8<i>h</i> + 15",
          ["8(<i>h</i> + 15)", "<i>h</i> + 23", "15<i>h</i> + 8"], "8 hours at h dollars is 8h. Add the bonus: 8h + 15."),
         ("A store adds a 7% tax to a price <i>p</i>. Which expression is the total?", "1.07<i>p</i>", ["0.07<i>p</i>", "<i>p</i> + 7", "1.7<i>p</i>"],
          "p + 0.07p = 1.07p."),
         ("Which expression is equivalent to <i>a</i> + 0.25<i>a</i>?", "1.25<i>a</i>", ["0.25<i>a</i>", "<i>a</i> + 25", "2.5<i>a</i>"],
          "a = 1a, and 1a + 0.25a = 1.25a. It means a increased by 25%."),
         ("Which expression is equivalent to 0.75<i>x</i>?", "<i>x</i> − 0.25<i>x</i>", ["<i>x</i> − 0.75", "<i>x</i> + 0.25<i>x</i>", "0.25<i>x</i> + 0.5"],
          "x − 0.25x = 0.75x. Taking 25% off leaves 75%."),
         ("Three consecutive whole numbers start at <i>n</i>. Which expression is their sum?", "3<i>n</i> + 3", ["3<i>n</i>", "<i>n</i> + 3", "3<i>n</i> + 2"],
          "n + (n + 1) + (n + 2) = 3n + 3."),
         ("A triangle has sides <i>x</i>, 2<i>x</i> and <i>x</i> + 5. Which expression is its perimeter?", "4<i>x</i> + 5", ["3<i>x</i> + 5", "4<i>x</i>", "2<i>x</i><sup>2</sup> + 5"],
          "x + 2x + x + 5 = 4x + 5."),
         ("A class orders <i>p</i> pizzas at $12 each and pays a $5 delivery fee. Then it gets $3 off. Which expression is the cost?", "12<i>p</i> + 2",
          ["12<i>p</i> + 8", "15<i>p</i>", "12(<i>p</i> + 2)"], "12p + 5 − 3 = 12p + 2."),
         ("Which expression shows 5 less than twice a number, all multiplied by 3?", "6<i>n</i> − 15", ["6<i>n</i> − 5", "3(5 − 2<i>n</i>)", "2<i>n</i> − 15"],
          "3(2n − 5) = 6n − 15."),
         ("Maya saves <i>d</i> dollars each week for 6 weeks, then spends $20. Which expression is equivalent to what she has left?", "6<i>d</i> − 20",
          ["6(<i>d</i> − 20)", "<i>d</i> − 14", "20 − 6<i>d</i>"], "6 weeks of d dollars is 6d. Spending $20 gives 6d − 20."),
         ("Which expression is equivalent to 4(<i>x</i> + 2) − 2<i>x</i>?", "2<i>x</i> + 8", ["2<i>x</i> + 2", "6<i>x</i> + 8", "4<i>x</i>"],
          "4x + 8 − 2x = 2x + 8."),
         ("Which two expressions are equivalent?", "3(<i>x</i> + 4) and 3<i>x</i> + 12", ["3(<i>x</i> + 4) and 3<i>x</i> + 4", "3<i>x</i> + 4 and 7<i>x</i>", "2<i>x</i> + 3<i>x</i> and 5<i>x</i><sup>2</sup>"],
          "3(x + 4) = 3x + 12. Test with x = 1: 3(5) = 15 and 3 + 12 = 15."),
         ("Jon says 2(<i>x</i> + 5) = 2<i>x</i> + 5. What mistake did he make?", "He did not multiply 5 by 2.",
          ["He added instead of multiplying.", "He should have added 2 and 5 first.", "There is no mistake."],
          "The 2 multiplies both terms: 2(x + 5) = 2x + 10."),
         ("A garden is <i>w</i> meters wide. Its length is 3 meters less than twice the width. Which expression is the perimeter?", "6<i>w</i> − 6",
          ["3<i>w</i> − 3", "6<i>w</i> − 3", "4<i>w</i> − 6"], "Length = 2w − 3. P = 2w + 2(2w − 3) = 2w + 4w − 6 = 6w − 6."),
         ("A gym membership costs $25 a month plus a $10 fee each month for classes. Which expression shows the cost for <i>m</i> months?", "35<i>m</i>",
          ["25<i>m</i> + 10", "35 + <i>m</i>", "250<i>m</i>"], "Each month costs 25 + 10 = 35 dollars, so m months cost 35m. 25m + 10m = 35m too.")]
    for text_, good, bad, e in q:
        its.append(mcq(text_, (good, "g"), [(b, b) for b in bad], e))
    return {"title": "Equivalent expressions in context", "items": its}


def body():
    rows = [["Combine like terms", "4<i>x</i> + 3 + 2<i>x</i>", "6<i>x</i> + 3"],
            ["Distribute", "3(2<i>x</i> − 5)", "6<i>x</i> − 15"],
            ["Subtract a group", "(5<i>x</i> + 3) − (2<i>x</i> + 1)", "3<i>x</i> + 2"],
            ["Factor", "12<i>x</i> + 8", "4(3<i>x</i> + 2)"]]
    return ("<h2>Like terms</h2><p><b>Like terms</b> have the same variable part. 4<i>x</i> and 2<i>x</i> are like terms. "
            "4<i>x</i> and 3 are not. To simplify, add the coefficients of like terms and keep the variable.</p>"
            + "<h2>The distributive property</h2><p>a(b + c) = ab + ac. Multiply the number outside by <b>every</b> term inside. "
            "A minus sign in front of a group changes the sign of every term: −(2<i>x</i> + 1) = −2<i>x</i> − 1.</p>"
            + table(["Skill", "Expression", "Simplified"], rows)
            + example("Simplify 3(2<i>x</i> − 1) + 4<i>x</i> + 7.", ["Distribute: 6<i>x</i> − 3 + 4<i>x</i> + 7.", "Combine: 6<i>x</i> + 4<i>x</i> = 10<i>x</i> and −3 + 7 = 4."], "10<i>x</i> + 4")
            + example("A price <i>p</i> goes up 5%. Write the new price two ways.", ["Price plus 5% of the price: <i>p</i> + 0.05<i>p</i>.", "Combine: 1.05<i>p</i>."], "<i>p</i> + 0.05<i>p</i> = 1.05<i>p</i>")
            + "<h2>Common mistakes</h2><ul><li>Adding unlike terms: 4<i>x</i> + 3 is not 7<i>x</i>.</li>"
            "<li>Distributing to one term: 3(2<i>x</i> − 5) is 6<i>x</i> − 15, not 6<i>x</i> − 5.</li>"
            "<li>Subtracting a group: (5<i>x</i> + 3) − (2<i>x</i> + 1) is 3<i>x</i> + 2, not 3<i>x</i> + 4.</li></ul>")


def main():
    sets = [set_like_terms(), set_distribute(), set_dist_combine(), set_factor(), set_context()]
    balance(sets, R)
    unit = {
        "slug": "simplifying-expressions",
        "title": "Simplifying Expressions",
        "seo_title": "Grade 7 Simplifying Expressions Worksheets: Like Terms, Distributive Property and Factoring",
        "short_title": "Simplifying expressions",
        "domain": "Expressions & Equations",
        "standard_code": "7.EE.A.1",
        "standard_url": "https://www.thecorestandards.org/Math/Content/7/EE/A/1/",
        "standard_text": "Apply properties of operations as strategies to add, subtract, factor, and expand linear expressions with rational coefficients.",
        "meta_desc": "Free Grade 7 simplifying expressions worksheets: combine like terms, use the distributive property, subtract groups, factor with the GCF, work with fraction and decimal coefficients, and write equivalent expressions for real situations. 100 practice questions with an answer key.",
        "key_big": "Combine only like terms, and multiply every term inside the parentheses.",
        "key_sub": "4x + 3 + 2x = 6x + 3 and 3(2x − 5) = 6x − 15. Factoring undoes distributing: 12x + 8 = 4(3x + 2).",
        "body_html": body(),
        "faq": [
            {"q": "What are like terms?", "a": "Terms with the same variable part. 5x and −2x are like terms, so 5x − 2x = 3x. 5x and 5 are not like terms."},
            {"q": "How do you use the distributive property?", "a": "Multiply the number outside the parentheses by every term inside: 4(2x − 3) = 8x − 12."},
            {"q": "How do you subtract an expression in parentheses?", "a": "Change the sign of every term in the group: (7x + 2) − (3x + 4) = 7x + 2 − 3x − 4 = 4x − 2."},
            {"q": "How do you factor a linear expression?", "a": "Find the greatest common factor of the terms and divide each term by it: 15x − 10 = 5(3x − 2). Check by distributing."}],
        "sets": sets,
        "pdf_url": "",
        "sort": 6,
        "updated": UPDATED,
    }
    write_unit("us", "math", "grade-7", unit)


if __name__ == "__main__":
    main()
