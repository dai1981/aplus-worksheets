# -*- coding: utf-8 -*-
"""
SG Secondary 2 Maths: Changing the Subject of a Formula (Sec 2 Algebra)
  python3 gen_sg_maths_s2_changing_the_subject_of_a_formula.py
One-step and two-step rearranging, formulae with brackets and fractions, formulae with squares and
square roots, and using a rearranged formula to calculate.
Wrong answers come from real mistakes: using the same operation instead of the inverse, undoing the
operations in the wrong order, and dividing only one term.
"""
import random
from fractions import Fraction as F
from sg_sec import num, mcq, B, S, make, lesson, collect, QN, T, fr, MINUS

R = random.Random(820400)
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
    q = "Make %s the subject of %s." % (B(I(Xv)), B(form))
    return T(q, right, [w for w in wr if w != right], e)


def one_step(r):
    return make_item(r, ["add", "sub", "mul", "div"])


def two_step(r):
    return make_item(r, ["mx+c", "mx-c"])


def brackets(r):
    return make_item(r, ["k(x+c)", "(x+c)/k", "c-kx"])


# ------------------------------------------------------------ set 4: real formulae, squares and roots
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
        q = "Make %s the subject of %s." % (B(sub), B(form))
        its.append(T(q, right, wr, how + " <b>%s</b>." % right))
    return its


# ------------------------------------------------------------ set 5: using rearranged formulae
def problems():
    its = []
    data = [
        ("The area of a rectangle is 48 cm² and its length is 8 cm. Use <i>A</i> = <i>lw</i> to find the width.", 6, [40, 384, 56], "<i>w</i> = <i>A</i> ÷ <i>l</i> = 48 ÷ 8 = <b>6 cm</b>.", " cm"),
        ("Use <i>v</i> = <i>u</i> + <i>at</i> to find <i>t</i> when <i>v</i> = 30, <i>u</i> = 10 and <i>a</i> = 4.", 5, [10, 80, F(15, 2)], "<i>t</i> = (<i>v</i> − <i>u</i>) ÷ <i>a</i> = 20 ÷ 4 = <b>5</b>.", ""),
        ("Use <i>F</i> = 1.8<i>C</i> + 32 to find <i>C</i> when <i>F</i> = 86.", 30, [F(86, 1) - 32, 64, F(301, 10)], "<i>C</i> = (86 − 32) ÷ 1.8 = 54 ÷ 1.8 = <b>30</b>.", ""),
        ("A triangle has area 24 cm² and base 8 cm. Use <i>A</i> = ½<i>bh</i> to find its height.", 6, [3, 12, 96], "<i>h</i> = 2<i>A</i> ÷ <i>b</i> = 48 ÷ 8 = <b>6 cm</b>.", " cm"),
        ("A car travels 150 km at 50 km/h. Use <i>s</i> = <i>d</i> ÷ <i>t</i> to find the time.", 3, [F(1, 3), 7500, 100], "<i>t</i> = <i>d</i> ÷ <i>s</i> = 150 ÷ 50 = <b>3 hours</b>.", " hours"),
        ("A plumber charges <i>T</i> = 15<i>m</i> + 30 dollars for <i>m</i> minutes. The bill is $135. How many minutes did the job take?", 7, [11, 9, 1575], "<i>m</i> = (135 − 30) ÷ 15 = 105 ÷ 15 = <b>7 minutes</b>.", " minutes"),
        ("Use <i>y</i> = <i>x</i><sup>2</sup> + 5 to find the positive value of <i>x</i> when <i>y</i> = 54.", 7, [F(49, 2), 49, 59], "<i>x</i> = √(54 − 5) = √49 = <b>7</b>.", ""),
        ("The mean of two numbers is <i>M</i> = (<i>a</i> + <i>b</i>) ÷ 2. The mean is 15 and <i>b</i> = 11. Find <i>a</i>.", 19, [4, 13, 41], "<i>a</i> = 2<i>M</i> − <i>b</i> = 30 − 11 = <b>19</b>.", ""),
        ("A circle has circumference 31.4 cm. Use <i>C</i> = 2<i>πr</i> with <i>π</i> = 3.14 to find the radius.", 5, [10, F(314, 10) - F(628, 100), 98.596], "<i>r</i> = <i>C</i> ÷ 2<i>π</i> = 31.4 ÷ 6.28 = <b>5 cm</b>.", " cm"),
        ("A box has volume 120 cm³, length 6 cm and width 4 cm. Use <i>V</i> = <i>lwh</i> to find its height.", 5, [110, 2880, 20], "<i>h</i> = 120 ÷ (6 × 4) = 120 ÷ 24 = <b>5 cm</b>.", " cm"),
    ]
    for q, a, w, e, u in data:
        its.append(QN(q, a, [F(str(x)) for x in w if F(str(x)) > 0 and F(str(x)).denominator <= 10], e, unit=u))
    texts = [
        ("What is the subject of the formula <i>A</i> = <i>lw</i>?", "<i>A</i>", ["<i>l</i>", "<i>w</i>", "<i>lw</i>"], "The subject is the letter on its own on one side: <b><i>A</i></b>."),
        ("To make <i>x</i> the subject of <i>y</i> = 4<i>x</i> + 7, what should you do first?", "Subtract 7 from both sides", ["Divide both sides by 4", "Add 7 to both sides", "Subtract 4 from both sides"],
         "Undo the operations in reverse order: the + 7 was last, so <b>subtract 7 first</b>."),
        ("Jun Jie makes <i>x</i> the subject of <i>y</i> = 2<i>x</i> + 6 and gets <i>x</i> = <i>y</i>/2 − 6. What is the correct answer?", "<i>x</i> = " + f("<i>y</i> − 6", "2"), ["<i>x</i> = " + f("<i>y</i>", "2") + " − 6", "<i>x</i> = " + f("<i>y</i> + 6", "2"), "<i>x</i> = 2<i>y</i> − 6"],
         "Subtract 6 first, then divide everything by 2: <b><i>x</i> = (<i>y</i> − 6) ÷ 2</b>. Jun Jie only divided <i>y</i>."),
        ("Which rearrangement of <i>p</i> = <i>q</i> − <i>r</i> is correct?", "<i>q</i> = <i>p</i> + <i>r</i>", ["<i>q</i> = <i>p</i> − <i>r</i>", "<i>q</i> = <i>r</i> − <i>p</i>", "<i>r</i> = <i>p</i> + <i>q</i>"], "Add <i>r</i> to both sides: <b><i>q</i> = <i>p</i> + <i>r</i></b>."),
        ("Which rearrangement of <i>p</i> = <i>q</i> − <i>r</i> gives <i>r</i>?", "<i>r</i> = <i>q</i> − <i>p</i>", ["<i>r</i> = <i>p</i> − <i>q</i>", "<i>r</i> = <i>p</i> + <i>q</i>", "<i>r</i> = " + f("<i>q</i>", "<i>p</i>")], "Add <i>r</i> and subtract <i>p</i>: <b><i>r</i> = <i>q</i> − <i>p</i></b>."),
        ("Rearrange <i>y</i> = 5 − <i>x</i> to make <i>x</i> the subject.", "<i>x</i> = 5 − <i>y</i>", ["<i>x</i> = <i>y</i> − 5", "<i>x</i> = 5 + <i>y</i>", "<i>x</i> = −5 − <i>y</i>"], "Add <i>x</i> and subtract <i>y</i>: <b><i>x</i> = 5 − <i>y</i></b>."),
        ("A formula for the cost of a taxi is <i>C</i> = 3 + 2<i>d</i>. Which formula gives the distance <i>d</i>?", "<i>d</i> = " + f("<i>C</i> − 3", "2"), ["<i>d</i> = " + f("<i>C</i>", "2") + " − 3", "<i>d</i> = 2(<i>C</i> − 3)", "<i>d</i> = " + f("<i>C</i> + 3", "2")],
         "Subtract 3, then divide by 2: <b><i>d</i> = (<i>C</i> − 3) ÷ 2</b>."),
        ("Which is the inverse of “square”?", "Square root", ["Halve", "Divide by 2", "Cube"], "Squaring is undone by taking the <b>square root</b>."),
        ("Make <i>x</i> the subject of <i>y</i> = " + f("<i>x</i>", "4") + " − 1.", "<i>x</i> = 4(<i>y</i> + 1)", ["<i>x</i> = 4<i>y</i> + 1", "<i>x</i> = " + f("<i>y</i> + 1", "4"), "<i>x</i> = 4<i>y</i> − 1"], "Add 1, then multiply by 4: <b><i>x</i> = 4(<i>y</i> + 1)</b>."),
        ("Make <i>t</i> the subject of <i>w</i> = 3(<i>t</i> − 2).", "<i>t</i> = " + f("<i>w</i>", "3") + " + 2", ["<i>t</i> = " + f("<i>w</i> + 2", "3"), "<i>t</i> = " + f("<i>w</i>", "3") + " − 2", "<i>t</i> = 3<i>w</i> + 2"], "Divide by 3, then add 2: <b><i>t</i> = <i>w</i>/3 + 2</b>."),
    ]
    for q, a, w, e in texts:
        its.append(T(q, a, w, e))
    return its


def body():
    return lesson(
        "<p>The <b>subject</b> of a formula is the letter on its own, such as <i>A</i> in <i>A</i> = <i>lw</i>. To change the "
        "subject, treat the formula like an equation: use inverse operations on both sides, undoing the last operation first.</p>",
        [("Make <i>x</i> the subject of <i>y</i> = 4<i>x</i> + 7.", ["Subtract 7: <i>y</i> − 7 = 4<i>x</i>.", "Divide by 4."], "<i>x</i> = (<i>y</i> − 7)/4"),
         ("Make <i>h</i> the subject of <i>A</i> = ½<i>bh</i>.", ["Multiply by 2: 2<i>A</i> = <i>bh</i>.", "Divide by <i>b</i>."], "<i>h</i> = 2<i>A</i>/<i>b</i>"),
         ("Make <i>r</i> the subject of <i>A</i> = <i>πr</i><sup>2</sup>.", ["Divide by <i>π</i>.", "Square root."], "<i>r</i> = √(<i>A</i>/<i>π</i>)")],
        ["Doing the same operation instead of the inverse: <i>y</i> = <i>x</i> + 3 gives <i>x</i> = <i>y</i> − 3, not <i>y</i> + 3.",
         "Undoing in the wrong order: for <i>y</i> = 2<i>x</i> + 6, subtract 6 before dividing by 2.",
         "Dividing only one term: (<i>y</i> − 6)/2 is not the same as <i>y</i>/2 − 6.",
         "Square rooting only part of an expression: <i>x</i> = √(<i>y</i> − 5), not √<i>y</i> − 5."])


def main():
    sets = [S("One-step rearranging", collect(one_step, 20, R)),
            S("Two-step rearranging", collect(two_step, 20, R)),
            S("Brackets, fractions and negatives", collect(brackets, 20, R)),
            S("Real formulae, squares and roots", real_items()),
            S("Using and checking rearranged formulae", problems())]
    make(2, "changing-the-subject-of-a-formula", 3, "N5",
         "Changing the Subject of a Formula",
         "Secondary 2 Rearranging Formulae Worksheets: Changing the Subject, Two-Step, Squares and Roots",
         "Changing the subject",
         "Understand and use standard mathematical formulae; rearrange formulae to change the subject; substitute "
         "numerical values into formulae and expressions, including scientific formulae.",
         "Free Secondary 2 worksheets on changing the subject of a formula: one-step and two-step rearranging, brackets and "
         "fractions, real formulae with squares and roots, and using rearranged formulae. 100 questions with answers.",
         "Rearrange like solving an equation: use inverse operations and undo the last operation first.",
         "y = 4x + 7 becomes x = (y − 7)/4: subtract 7 first, then divide everything by 4.",
         body(),
         [("What does changing the subject of a formula mean?", "Rearranging it so a different letter is on its own. A = lw can be rearranged to w = A/l."),
          ("How is rearranging like solving an equation?", "You use the same inverse operations on both sides, but you finish with letters instead of a number."),
          ("Which operation do I undo first?", "The last one that was done to the letter. In y = 4x + 7, x is multiplied by 4 and then 7 is added, so subtract 7 first."),
          ("How do I undo a square?", "Take the square root of the whole other side. From y = x² + 5, x = √(y − 5).")],
         sets, R)


if __name__ == "__main__":
    main()
