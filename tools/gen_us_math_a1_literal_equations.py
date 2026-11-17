# -*- coding: utf-8 -*-
"""
US Algebra 1: Literal Equations and Formulas (Common Core A-CED.A.4)
  python3 tools/gen_us_math_a1_literal_equations.py
Solving formulas for a variable in one and two steps, formulas with parentheses, fractions and negatives,
real formulas from math and science (including squares and roots), and using a rearranged formula.
Wrong answers come from real mistakes: using the same operation instead of the inverse, undoing in the wrong
order, dividing only one term, and taking the square root of only part of an expression.
"""
import random
from fractions import Fraction as F
from us_hs import num, mcq, B, S, make, lesson, collect, QN, T, fr, MINUS, expr

R = random.Random(90201)
PAIRS = [("y", "x"), ("p", "q"), ("a", "b"), ("v", "t"), ("w", "m"), ("s", "r"), ("h", "k"), ("d", "e")]


def I(c):
    return "<i>%s</i>" % c


def f(top, bot):
    return fr(top, bot)


# ------------------------------------------------------------ templates: (formula, answer, wrongs, explanation)
def tmpl(r, kind, Y, Xv, k, c):
    y, x = I(Y), I(Xv)
    K, C = str(k), str(c)
    if kind == "add":
        return ("%s = %s + %s" % (y, x, C), "%s = %s − %s" % (x, y, C), ["%s = %s + %s" % (x, y, C), "%s = %s − %s" % (x, C, y), "%s = %s" % (x, f(y, C))],
                "Subtract %s from both sides: <b>%s = %s − %s</b>." % (C, x, y, C))
    if kind == "sub":
        return ("%s = %s − %s" % (y, x, C), "%s = %s + %s" % (x, y, C), ["%s = %s − %s" % (x, y, C), "%s = %s − %s" % (x, C, y), "%s = %s%s" % (x, C, y)],
                "Add %s to both sides: <b>%s = %s + %s</b>." % (C, x, y, C))
    if kind == "mul":
        return ("%s = %s%s" % (y, K, x), "%s = %s" % (x, f(y, K)), ["%s = %s%s" % (x, K, y), "%s = %s − %s" % (x, y, K), "%s = %s" % (x, f(K, y))],
                "Divide both sides by %s: <b>%s = %s</b>." % (K, x, f(y, K)))
    if kind == "div":
        return ("%s = %s" % (y, f(x, K)), "%s = %s%s" % (x, K, y), ["%s = %s" % (x, f(y, K)), "%s = %s + %s" % (x, y, K), "%s = %s" % (x, f(K, y))],
                "Multiply both sides by %s: <b>%s = %s%s</b>." % (K, x, K, y))
    if kind == "mx+c":
        return ("%s = %s%s + %s" % (y, K, x, C), "%s = %s" % (x, f("%s − %s" % (y, C), K)),
                ["%s = %s − %s" % (x, f(y, K), C), "%s = %s" % (x, f("%s + %s" % (y, C), K)), "%s = %s(%s − %s)" % (x, K, y, C)],
                "Subtract %s first: %s − %s = %s%s. Then divide by %s: <b>%s = %s</b>." % (C, y, C, K, x, K, x, f("%s − %s" % (y, C), K)))
    if kind == "mx-c":
        return ("%s = %s%s − %s" % (y, K, x, C), "%s = %s" % (x, f("%s + %s" % (y, C), K)),
                ["%s = %s + %s" % (x, f(y, K), C), "%s = %s" % (x, f("%s − %s" % (y, C), K)), "%s = %s(%s + %s)" % (x, K, y, C)],
                "Add %s first: %s + %s = %s%s. Then divide by %s: <b>%s = %s</b>." % (C, y, C, K, x, K, x, f("%s + %s" % (y, C), K)))
    if kind == "k(x+c)":
        return ("%s = %s(%s + %s)" % (y, K, x, C), "%s = %s − %s" % (x, f(y, K), C),
                ["%s = %s" % (x, f("%s − %s" % (y, C), K)), "%s = %s + %s" % (x, f(y, K), C), "%s = %s%s − %s" % (x, K, y, C)],
                "Divide by %s first: %s = %s + %s. Then subtract %s: <b>%s = %s − %s</b>." % (K, f(y, K), x, C, C, x, f(y, K), C))
    if kind == "(x+c)/k":
        return ("%s = %s" % (y, f("%s + %s" % (x, C), K)), "%s = %s%s − %s" % (x, K, y, C),
                ["%s = %s − %s" % (x, f(y, K), C), "%s = %s(%s − %s)" % (x, K, y, C), "%s = %s%s + %s" % (x, K, y, C)],
                "Multiply by %s first: %s%s = %s + %s. Then subtract %s: <b>%s = %s%s − %s</b>." % (K, K, y, x, C, C, x, K, y, C))
    if kind == "c-kx":
        return ("%s = %s − %s%s" % (y, C, K, x), "%s = %s" % (x, f("%s − %s" % (C, y), K)),
                ["%s = %s" % (x, f("%s − %s" % (y, C), K)), "%s = %s" % (x, f("%s + %s" % (C, y), K)), "%s = %s − %s" % (x, C, f(y, K))],
                "Add %s%s and subtract %s: %s%s = %s − %s. Divide by %s: <b>%s = %s</b>." % (K, x, y, K, x, C, y, K, x, f("%s − %s" % (C, y), K)))
    raise ValueError(kind)


def make_item(r, kinds):
    kind = r.choice(kinds)
    Y, Xv = r.choice(PAIRS)
    k, c = r.randint(2, 9), r.randint(2, 12)
    form, right, wr, e = tmpl(r, kind, Y, Xv, k, c)
    q = "Solve %s for %s." % (B(form), B(I(Xv)))
    return T(q, right, [w for w in wr if w != right], e)


def one_step(r):
    return make_item(r, ["add", "sub", "mul", "div"])


def two_step(r):
    return make_item(r, ["mx+c", "mx-c"])


def brackets(r):
    return make_item(r, ["k(x+c)", "(x+c)/k", "c-kx"])


# ------------------------------------------------------------ set 2: standard form to slope-intercept form
def cf(v):
    v = F(v)
    if v.denominator == 1:
        return num(v)
    s = fr(abs(v.numerator), v.denominator)
    return (MINUS + s) if v < 0 else s


def mx_b(m, b):
    m, b = F(m), F(b)
    if m == 1:
        t = "<i>x</i>"
    elif m == -1:
        t = MINUS + "<i>x</i>"
    else:
        t = cf(m) + "<i>x</i>"
    if b == 0:
        return "<i>y</i> = " + t
    return "<i>y</i> = %s %s %s" % (t, "+" if b > 0 else MINUS, cf(abs(b)))


def one_std(r):
    a, b = r.choice([1, 2, 3, 4, 5, 6, -2, -3]), r.choice([2, 3, 4, 5, -2, -4, 1, -1])
    c = r.choice([n for n in range(-18, 19) if n])
    if abs(a) == abs(b) and abs(a) > 1:
        return None
    left = expr([(a, "<i>x</i>"), (b, "<i>y</i>")])
    q = "Solve %s for %s." % (B("%s = %s" % (left, num(c))), B("<i>y</i>"))
    m, k = F(-a, b), F(c, b)
    right = mx_b(m, k)
    wr = [mx_b(-m, k), mx_b(m, c) if b != 1 else mx_b(m, -k), mx_b(F(-b, a) if a else m, k) if F(-b, a) != m else mx_b(m, k + 1)]
    e = "%s both sides: %s = %s. Divide every term by %s: <b>%s</b>." % (
        ("Subtract %s from" if a > 0 else "Add %s to") % expr([(abs(a), "<i>x</i>")]), expr([(b, "<i>y</i>")]), expr([(-a, "<i>x</i>"), (c, "")]), num(b), right)
    if b == 1:
        e = "%s both sides: <b>%s</b>." % (("Subtract %s from" if a > 0 else "Add %s to") % expr([(abs(a), "<i>x</i>")]), right)
    return T(q, right, [w for w in dict.fromkeys(wr) if w != right][:3], e)


def one_factor_out(r):
    v = r.choice(["<i>x</i>", "<i>t</i>", "<i>m</i>"])
    a, b = r.choice(["<i>a</i>", "<i>p</i>", "<i>k</i>"]), r.choice(["<i>b</i>", "<i>q</i>", "<i>c</i>"])
    kind = r.randint(0, 2)
    if kind == 0:
        q = "Solve %s for %s." % (B("%s%s + %s%s = <i>d</i>" % (a, v, b, v)), B(v))
        right = "%s = %s" % (v, fr("<i>d</i>", a + " + " + b))
        wr = ["%s = <i>d</i> − %s − %s" % (v, a, b), "%s = %s" % (v, fr("<i>d</i>", a + b)), "%s = %s − %s" % (v, fr("<i>d</i>", a), b)]
        e = "Factor out %s: %s(%s + %s) = <i>d</i>. Divide by (%s + %s): <b>%s</b>." % (v, v, a, b, a, b, right)
    elif kind == 1:
        q = "Solve %s for %s." % (B("%s%s = %s + <i>d</i>" % (a, v, v)), B(v))
        right = "%s = %s" % (v, fr("<i>d</i>", a + " − 1"))
        wr = ["%s = %s" % (v, fr("<i>d</i>", a)), "%s = %s" % (v, fr("<i>d</i> + 1", a)), "%s = <i>d</i> − %s" % (v, a)]
        e = "Subtract %s: %s%s − %s = <i>d</i>. Factor: %s(%s − 1) = <i>d</i>. Divide: <b>%s</b>." % (v, a, v, v, v, a, right)
    else:
        q = "Solve %s for %s." % (B("%s(%s + %s) = <i>d</i>" % (a, v, b)), B(v))
        right = "%s = %s − %s" % (v, fr("<i>d</i>", a), b)
        wr = ["%s = %s" % (v, fr("<i>d</i> − " + b, a)), "%s = <i>d</i> − %s%s" % (v, a, b), "%s = %s + %s" % (v, fr("<i>d</i>", a), b)]
        e = "Divide by %s: %s = %s + %s. Subtract %s: <b>%s</b>." % (a, fr("<i>d</i>", a), v, b, b, right)
    return T(q, right, wr, e)


# ------------------------------------------------------------ set 4: real formulas, squares and roots
REAL = [
    ("<i>A</i> = <i>lw</i>", "<i>w</i>", "<i>w</i> = " + f("<i>A</i>", "<i>l</i>"), ["<i>w</i> = <i>Al</i>", "<i>w</i> = <i>A</i> − <i>l</i>", "<i>w</i> = " + f("<i>l</i>", "<i>A</i>")], "Divide both sides by <i>l</i>."),
    ("<i>P</i> = 2<i>l</i> + 2<i>w</i>", "<i>l</i>", "<i>l</i> = " + f("<i>P</i> − 2<i>w</i>", "2"), ["<i>l</i> = " + f("<i>P</i>", "2") + " − 2<i>w</i>", "<i>l</i> = <i>P</i> − <i>w</i>", "<i>l</i> = " + f("<i>P</i> + 2<i>w</i>", "2")], "Subtract 2<i>w</i>, then divide by 2."),
    ("<i>v</i> = <i>u</i> + <i>at</i>", "<i>a</i>", "<i>a</i> = " + f("<i>v</i> − <i>u</i>", "<i>t</i>"), ["<i>a</i> = " + f("<i>v</i>", "<i>t</i>") + " − <i>u</i>", "<i>a</i> = <i>t</i>(<i>v</i> − <i>u</i>)", "<i>a</i> = " + f("<i>v</i> + <i>u</i>", "<i>t</i>")], "Subtract <i>u</i>, then divide by <i>t</i>."),
    ("<i>v</i> = <i>u</i> + <i>at</i>", "<i>u</i>", "<i>u</i> = <i>v</i> − <i>at</i>", ["<i>u</i> = <i>v</i> + <i>at</i>", "<i>u</i> = " + f("<i>v</i>", "<i>at</i>"), "<i>u</i> = <i>at</i> − <i>v</i>"], "Subtract <i>at</i> from both sides."),
    ("<i>A</i> = ½<i>bh</i>", "<i>h</i>", "<i>h</i> = " + f("2<i>A</i>", "<i>b</i>"), ["<i>h</i> = " + f("<i>A</i>", "2<i>b</i>"), "<i>h</i> = 2<i>Ab</i>", "<i>h</i> = " + f("<i>A</i>", "<i>b</i>")], "Multiply by 2, then divide by <i>b</i>."),
    ("<i>F</i> = 1.8<i>C</i> + 32", "<i>C</i>", "<i>C</i> = " + f("<i>F</i> − 32", "1.8"), ["<i>C</i> = " + f("<i>F</i>", "1.8") + " − 32", "<i>C</i> = " + f("<i>F</i> + 32", "1.8"), "<i>C</i> = 1.8(<i>F</i> − 32)"], "Subtract 32, then divide by 1.8."),
    ("<i>s</i> = " + f("<i>d</i>", "<i>t</i>"), "<i>d</i>", "<i>d</i> = <i>st</i>", ["<i>d</i> = " + f("<i>s</i>", "<i>t</i>"), "<i>d</i> = " + f("<i>t</i>", "<i>s</i>"), "<i>d</i> = <i>s</i> + <i>t</i>"], "Multiply both sides by <i>t</i>."),
    ("<i>s</i> = " + f("<i>d</i>", "<i>t</i>"), "<i>t</i>", "<i>t</i> = " + f("<i>d</i>", "<i>s</i>"), ["<i>t</i> = <i>ds</i>", "<i>t</i> = " + f("<i>s</i>", "<i>d</i>"), "<i>t</i> = <i>d</i> − <i>s</i>"], "Multiply by <i>t</i>: <i>st</i> = <i>d</i>. Then divide by <i>s</i>."),
    ("<i>A</i> = <i>πr</i><sup>2</sup>", "<i>r</i>", "<i>r</i> = √" + "(" + f("<i>A</i>", "<i>π</i>") + ")", ["<i>r</i> = " + f("<i>A</i>", "2<i>π</i>"), "<i>r</i> = " + f("√<i>A</i>", "2<i>π</i>") if False else "<i>r</i> = (" + f("<i>A</i>", "<i>π</i>") + ")<sup>2</sup>", "<i>r</i> = √<i>A</i> − <i>π</i>"], "Divide by <i>π</i>, then square root."),
    ("<i>y</i> = <i>x</i><sup>2</sup> + 5", "<i>x</i>", "<i>x</i> = √(<i>y</i> − 5)", ["<i>x</i> = √<i>y</i> − 5", "<i>x</i> = (<i>y</i> − 5)<sup>2</sup>", "<i>x</i> = " + f("<i>y</i> − 5", "2")], "Subtract 5, then square root the whole of <i>y</i> − 5."),
    ("<i>E</i> = <i>mc</i><sup>2</sup>", "<i>m</i>", "<i>m</i> = " + f("<i>E</i>", "<i>c</i><sup>2</sup>"), ["<i>m</i> = <i>Ec</i><sup>2</sup>", "<i>m</i> = " + f("√<i>E</i>", "<i>c</i>"), "<i>m</i> = <i>E</i> − <i>c</i><sup>2</sup>"], "Divide both sides by <i>c</i><sup>2</sup>."),
    ("<i>y</i> = √<i>x</i>", "<i>x</i>", "<i>x</i> = <i>y</i><sup>2</sup>", ["<i>x</i> = √<i>y</i>", "<i>x</i> = " + f("<i>y</i>", "2"), "<i>x</i> = 2<i>y</i>"], "Square both sides."),
    ("<i>V</i> = <i>lwh</i>", "<i>h</i>", "<i>h</i> = " + f("<i>V</i>", "<i>lw</i>"), ["<i>h</i> = <i>V</i> − <i>lw</i>", "<i>h</i> = <i>Vlw</i>", "<i>h</i> = " + f("<i>lw</i>", "<i>V</i>")], "Divide both sides by <i>lw</i>."),
    ("<i>C</i> = 2<i>πr</i>", "<i>r</i>", "<i>r</i> = " + f("<i>C</i>", "2<i>π</i>"), ["<i>r</i> = 2<i>πC</i>", "<i>r</i> = " + f("2<i>π</i>", "<i>C</i>"), "<i>r</i> = <i>C</i> − 2<i>π</i>"], "Divide both sides by 2<i>π</i>."),
    ("<i>M</i> = " + f("<i>a</i> + <i>b</i>", "2"), "<i>a</i>", "<i>a</i> = 2<i>M</i> − <i>b</i>", ["<i>a</i> = " + f("<i>M</i>", "2") + " − <i>b</i>", "<i>a</i> = 2(<i>M</i> − <i>b</i>)", "<i>a</i> = 2<i>M</i> + <i>b</i>"], "Multiply by 2, then subtract <i>b</i>."),
    ("<i>T</i> = 15<i>m</i> + 30", "<i>m</i>", "<i>m</i> = " + f("<i>T</i> − 30", "15"), ["<i>m</i> = " + f("<i>T</i>", "15") + " − 30", "<i>m</i> = 15(<i>T</i> − 30)", "<i>m</i> = " + f("<i>T</i> + 30", "15")], "Subtract 30, then divide by 15."),
    ("<i>k</i> = " + f("<i>m</i>", "<i>v</i><sup>2</sup>"), "<i>m</i>", "<i>m</i> = <i>kv</i><sup>2</sup>", ["<i>m</i> = " + f("<i>k</i>", "<i>v</i><sup>2</sup>"), "<i>m</i> = <i>k</i> + <i>v</i><sup>2</sup>", "<i>m</i> = √(<i>kv</i>)"], "Multiply both sides by <i>v</i><sup>2</sup>."),
    ("<i>y</i> = 3<i>x</i><sup>2</sup>", "<i>x</i>", "<i>x</i> = √(" + f("<i>y</i>", "3") + ")", ["<i>x</i> = " + f("√<i>y</i>", "1") .replace("<span class='fr'><span class='fn'>√<i>y</i></span><span class='fd'>1</span></span>", "√<i>y</i> ÷ 3") if False else "<i>x</i> = " + f("<i>y</i>", "6"), "<i>x</i> = √(3<i>y</i>)", "<i>x</i> = (" + f("<i>y</i>", "3") + ")<sup>2</sup>"], "Divide by 3, then square root."),
    ("<i>P</i> = <i>I</i><sup>2</sup><i>R</i>", "<i>R</i>", "<i>R</i> = " + f("<i>P</i>", "<i>I</i><sup>2</sup>"), ["<i>R</i> = <i>PI</i><sup>2</sup>", "<i>R</i> = " + f("<i>P</i>", "2<i>I</i>"), "<i>R</i> = <i>P</i> − <i>I</i><sup>2</sup>"], "Divide both sides by <i>I</i><sup>2</sup>."),
    ("<i>W</i> = 8<i>h</i> − 20", "<i>h</i>", "<i>h</i> = " + f("<i>W</i> + 20", "8"), ["<i>h</i> = " + f("<i>W</i> − 20", "8"), "<i>h</i> = " + f("<i>W</i>", "8") + " + 20", "<i>h</i> = 8(<i>W</i> + 20)"], "Add 20, then divide by 8."),
]


def real_items():
    its = []
    for form, sub, right, wr, how in REAL:
        q = "Solve %s for %s." % (B(form), B(sub))
        its.append(T(q, right, wr, how + " <b>%s</b>." % right))
    return its


# ------------------------------------------------------------ set 5: using rearranged formulas
def problems():
    its = []
    data = [
        ("The area of a rectangle is 48 cm² and its length is 8 cm. Use <i>A</i> = <i>lw</i> to find the width.", 6, [40, 384, 56], "<i>w</i> = <i>A</i> ÷ <i>l</i> = 48 ÷ 8 = <b>6 cm</b>.", " cm"),
        ("Use <i>v</i> = <i>u</i> + <i>at</i> to find <i>t</i> when <i>v</i> = 30, <i>u</i> = 10 and <i>a</i> = 4.", 5, [10, 80, F(15, 2)], "<i>t</i> = (<i>v</i> − <i>u</i>) ÷ <i>a</i> = 20 ÷ 4 = <b>5</b>.", ""),
        ("Use <i>F</i> = 1.8<i>C</i> + 32 to find <i>C</i> when <i>F</i> = 86.", 30, [F(86, 1) - 32, 64, F(301, 10)], "<i>C</i> = (86 − 32) ÷ 1.8 = 54 ÷ 1.8 = <b>30</b>.", ""),
        ("A triangle has area 24 cm² and base 8 cm. Use <i>A</i> = ½<i>bh</i> to find its height.", 6, [3, 12, 96], "<i>h</i> = 2<i>A</i> ÷ <i>b</i> = 48 ÷ 8 = <b>6 cm</b>.", " cm"),
        ("A car travels 150 miles at 50 mph. Use <i>s</i> = <i>d</i> ÷ <i>t</i> to find the time.", 3, [F(1, 3), 7500, 100], "<i>t</i> = <i>d</i> ÷ <i>s</i> = 150 ÷ 50 = <b>3 hours</b>.", " hours"),
        ("A plumber charges <i>T</i> = 15<i>m</i> + 30 dollars for <i>m</i> minutes of work. The bill is $135. How many minutes did the job take?", 7, [11, 9, 1575], "<i>m</i> = (135 − 30) ÷ 15 = 105 ÷ 15 = <b>7 minutes</b>.", " minutes"),
        ("Use <i>y</i> = <i>x</i><sup>2</sup> + 5 to find the positive value of <i>x</i> when <i>y</i> = 54.", 7, [F(49, 2), 49, 59], "<i>x</i> = √(54 − 5) = √49 = <b>7</b>.", ""),
        ("The mean of two numbers is <i>M</i> = (<i>a</i> + <i>b</i>) ÷ 2. The mean is 15 and <i>b</i> = 11. Find <i>a</i>.", 19, [4, 13, 41], "<i>a</i> = 2<i>M</i> − <i>b</i> = 30 − 11 = <b>19</b>.", ""),
        ("A circle has a circumference of 31.4 cm. Use <i>C</i> = 2<i>πr</i> with <i>π</i> = 3.14 to find the radius.", 5, [10, F(314, 10) - F(628, 100), 98.596], "<i>r</i> = <i>C</i> ÷ 2<i>π</i> = 31.4 ÷ 6.28 = <b>5 cm</b>.", " cm"),
        ("A box has volume 120 cm³, length 6 cm and width 4 cm. Use <i>V</i> = <i>lwh</i> to find its height.", 5, [110, 2880, 20], "<i>h</i> = 120 ÷ (6 × 4) = 120 ÷ 24 = <b>5 cm</b>.", " cm"),
    ]
    for q, a, w, e, u in data:
        its.append(QN(q, a, [F(str(x)) for x in w if F(str(x)) > 0 and F(str(x)).denominator <= 10], e, unit=u))
    texts = [
        ("In the formula <i>A</i> = <i>lw</i>, which variable has the formula been solved for?", "<i>A</i>", ["<i>l</i>", "<i>w</i>", "<i>lw</i>"], "The formula is solved for the variable that is alone on one side: <b><i>A</i></b>."),
        ("To solve <i>y</i> = 4<i>x</i> + 7 for <i>x</i>, what should you do first?", "Subtract 7 from both sides", ["Divide both sides by 4", "Add 7 to both sides", "Subtract 4 from both sides"],
         "Undo the operations in reverse order: the + 7 was last, so <b>subtract 7 first</b>."),
        ("Marcus solves <i>y</i> = 2<i>x</i> + 6 for <i>x</i> and gets <i>x</i> = <i>y</i>/2 − 6. What is the correct answer?", "<i>x</i> = " + f("<i>y</i> − 6", "2"), ["<i>x</i> = " + f("<i>y</i>", "2") + " − 6", "<i>x</i> = " + f("<i>y</i> + 6", "2"), "<i>x</i> = 2<i>y</i> − 6"],
         "Subtract 6 first, then divide everything by 2: <b><i>x</i> = (<i>y</i> − 6) ÷ 2</b>. Marcus only divided <i>y</i>."),
        ("Which rearrangement of <i>p</i> = <i>q</i> − <i>r</i> is correct?", "<i>q</i> = <i>p</i> + <i>r</i>", ["<i>q</i> = <i>p</i> − <i>r</i>", "<i>q</i> = <i>r</i> − <i>p</i>", "<i>r</i> = <i>p</i> + <i>q</i>"], "Add <i>r</i> to both sides: <b><i>q</i> = <i>p</i> + <i>r</i></b>."),
        ("Which rearrangement of <i>p</i> = <i>q</i> − <i>r</i> gives <i>r</i>?", "<i>r</i> = <i>q</i> − <i>p</i>", ["<i>r</i> = <i>p</i> − <i>q</i>", "<i>r</i> = <i>p</i> + <i>q</i>", "<i>r</i> = " + f("<i>q</i>", "<i>p</i>")], "Add <i>r</i> and subtract <i>p</i>: <b><i>r</i> = <i>q</i> − <i>p</i></b>."),
        ("Solve <i>y</i> = 5 − <i>x</i> for <i>x</i>.", "<i>x</i> = 5 − <i>y</i>", ["<i>x</i> = <i>y</i> − 5", "<i>x</i> = 5 + <i>y</i>", "<i>x</i> = −5 − <i>y</i>"], "Add <i>x</i> and subtract <i>y</i>: <b><i>x</i> = 5 − <i>y</i></b>."),
        ("A formula for the cost of a taxi is <i>C</i> = 3 + 2<i>d</i>. Which formula gives the distance <i>d</i>?", "<i>d</i> = " + f("<i>C</i> − 3", "2"), ["<i>d</i> = " + f("<i>C</i>", "2") + " − 3", "<i>d</i> = 2(<i>C</i> − 3)", "<i>d</i> = " + f("<i>C</i> + 3", "2")],
         "Subtract 3, then divide by 2: <b><i>d</i> = (<i>C</i> − 3) ÷ 2</b>."),
        ("Which is the inverse of “square”?", "Square root", ["Halve", "Divide by 2", "Cube"], "Squaring is undone by taking the <b>square root</b>."),
        ("Solve <i>y</i> = " + f("<i>x</i>", "4") + " − 1 for <i>x</i>.", "<i>x</i> = 4(<i>y</i> + 1)", ["<i>x</i> = 4<i>y</i> + 1", "<i>x</i> = " + f("<i>y</i> + 1", "4"), "<i>x</i> = 4<i>y</i> − 1"], "Add 1, then multiply by 4: <b><i>x</i> = 4(<i>y</i> + 1)</b>."),
        ("Solve <i>w</i> = 3(<i>t</i> − 2) for <i>t</i>.", "<i>t</i> = " + f("<i>w</i>", "3") + " + 2", ["<i>t</i> = " + f("<i>w</i> + 2", "3"), "<i>t</i> = " + f("<i>w</i>", "3") + " − 2", "<i>t</i> = 3<i>w</i> + 2"], "Divide by 3, then add 2: <b><i>t</i> = <i>w</i>/3 + 2</b>."),
    ]
    for q, a, w, e in texts:
        its.append(T(q, a, w, e))
    return its


def body():
    return lesson(
        "<p>A <b>literal equation</b> has more than one variable, like a formula. To <b>solve for</b> one variable, treat the "
        "other letters like numbers: use inverse operations on both sides, undoing the last operation first.</p>",
        [("Solve <i>y</i> = 4<i>x</i> + 7 for <i>x</i>.", ["Subtract 7: <i>y</i> − 7 = 4<i>x</i>.", "Divide by 4."], "<i>x</i> = (<i>y</i> − 7)/4"),
         ("Solve <i>A</i> = ½<i>bh</i> for <i>h</i>.", ["Multiply by 2: 2<i>A</i> = <i>bh</i>.", "Divide by <i>b</i>."], "<i>h</i> = 2<i>A</i>/<i>b</i>"),
         ("Solve <i>A</i> = <i>πr</i><sup>2</sup> for <i>r</i>.", ["Divide by <i>π</i>.", "Square root."], "<i>r</i> = √(<i>A</i>/<i>π</i>)")],
        ["Doing the same operation instead of the inverse: <i>y</i> = <i>x</i> + 3 gives <i>x</i> = <i>y</i> − 3, not <i>y</i> + 3.",
         "Undoing in the wrong order: for <i>y</i> = 2<i>x</i> + 6, subtract 6 before dividing by 2.",
         "Dividing only one term: (<i>y</i> − 6)/2 is not the same as <i>y</i>/2 − 6.",
         "Square rooting only part of an expression: <i>x</i> = √(<i>y</i> − 5), not √<i>y</i> − 5."])


def main():
    sets = [S("Solve for a variable in one or two steps", collect(one_step, 8, R) + collect(two_step, 12, R)),
            S("Solve for y: standard form to slope-intercept form", collect(one_std, 20, R)),
            S("Parentheses, fractions and factoring out", collect(brackets, 14, R) + collect(one_factor_out, 6, R)),
            S("Formulas from math and science", real_items()),
            S("Using rearranged formulas", problems())]
    make("literal-equations", 2, "A-CED.A.4",
         "Literal Equations: Solving Formulas for a Variable",
         "Algebra 1 Literal Equations Worksheets: Solve Formulas for a Variable (Free, Answer Key)",
         "Literal equations",
         "Rearrange formulas to highlight a quantity of interest, using the same reasoning as in solving equations. "
         "For example, rearrange Ohm's law V = IR to highlight resistance R.",
         "Free Algebra 1 literal equations worksheets (A-CED.A.4): solve formulas for a variable in one and two steps, with "
         "parentheses, fractions and negatives, real formulas from math and science, and using rearranged formulas. 100 questions with an answer key.",
         "Rearrange like solving an equation: use inverse operations and undo the last operation first.",
         "y = 4x + 7 becomes x = (y − 7)/4: subtract 7 first, then divide everything by 4.",
         body(),
         [("What is a literal equation?", "An equation with two or more variables, such as a formula. A = lw is a literal equation, and solving it for w gives w = A/l."),
          ("How is solving a literal equation like solving a normal equation?", "You use the same inverse operations on both sides, but you finish with letters instead of a number."),
          ("Which operation do I undo first?", "The last one that was done to the letter. In y = 4x + 7, x is multiplied by 4 and then 7 is added, so subtract 7 first."),
          ("How do I undo a square?", "Take the square root of the whole other side. From y = x² + 5, x = √(y − 5).")],
         sets, R, domain="Equations & Inequalities")


if __name__ == "__main__":
    main()
