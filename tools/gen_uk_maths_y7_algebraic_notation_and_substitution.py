# -*- coding: utf-8 -*-
"""
UK Year 7 Maths: Algebraic Notation and Substitution (KS3 Algebra)
  python3 tools/gen_uk_maths_y7_algebraic_notation_and_substitution.py
Writing expressions with algebraic notation, turning words into expressions, substituting positive and
negative values, and using formulae. Wrong answers come from real mistakes: reading 3a as 3 + a or as
the digits 3 and a side by side, reading a² as 2a, and squaring a negative to a negative.
"""
import random
from fractions import Fraction as F
from uk_ks3 import num, par, mcq, B, S, make, lesson, collect, QN, T, fr, MINUS, v

R = random.Random(71101)
LET = ["a", "b", "c", "n", "x", "y", "p", "t", "m", "k"]


def I(s):
    return "<i>%s</i>" % s


# ------------------------------------------------------------ set 1: notation
def one_notation(r):
    a = r.choice(LET)
    b = r.choice([x for x in LET if x != a])
    k = r.randint(2, 9)
    forms = [
        ("%d × %s" % (k, I(a)), "%d%s" % (k, I(a)), ["%s%d" % (I(a), k) + "", "%d + %s" % (k, I(a)), "%s<sup>%d</sup>" % (I(a), k)]),
        ("%s × %s" % (I(a), I(a)), "%s<sup>2</sup>" % I(a), ["2%s" % I(a), "%s + %s" % (I(a), I(a)), "%s<sup>%s</sup>" % (I(a), I(a))]),
        ("%s ÷ %d" % (I(a), k), fr(I(a), k), [fr(k, I(a)), "%d%s" % (k, I(a)), "%s − %d" % (I(a), k)]),
        ("%s × %s × %d" % (I(a), I(b), k), "%d%s%s" % (k, I(min(a, b)), I(max(a, b))), ["%d + %s + %s" % (k, I(a), I(b)), "%s%s + %d" % (I(a), I(b), k), "%d%s<sup>2</sup>" % (k, I(a))]),
        ("%s + %s + %s" % (I(a), I(a), I(a)), "3%s" % I(a), ["%s<sup>3</sup>" % I(a), "%s3" % I(a), "3 + %s" % I(a)]),
        ("%s × %s × %s" % (I(a), I(a), I(a)), "%s<sup>3</sup>" % I(a), ["3%s" % I(a), "%s<sup>2</sup>" % I(a), "%s + 3" % I(a)]),
        ("%d × (%s + %d)" % (k, I(a), k + 1), "%d(%s + %d)" % (k, I(a), k + 1), ["%d%s + %d" % (k, I(a), k + 1), "%d + %s + %d" % (k, I(a), k + 1), "%d + (%s + %d)" % (k, I(a), k + 1)]),
    ]
    src, right, wr = r.choice(forms)
    q = "Write %s using algebraic notation." % B(src)
    e = {0: "Leave out the × sign and write the number first: <b>%s</b>.",
         1: "A letter times itself is a square: <b>%s</b>.",
         2: "Division is written as a fraction: <b>%s</b>.",
         3: "Write the number first, then the letters in alphabetical order: <b>%s</b>.",
         4: "Three lots of the same letter: <b>%s</b>.",
         5: "A letter multiplied by itself three times is a cube: <b>%s</b>.",
         6: "Leave out the × sign before a bracket: <b>%s</b>."}[[f[0] for f in forms].index(src)] % right
    return T(q, right, wr, e)


# ------------------------------------------------------------ set 2: words to expressions
def one_words(r):
    a = r.choice(["n", "x", "y", "t"])
    k = r.randint(2, 12)
    j = r.randint(2, 6)
    forms = [
        ("%d more than %s" % (k, I(a)), "%s + %d" % (I(a), k), ["%d%s" % (k, I(a)), "%d − %s" % (k, I(a)), "%s − %d" % (I(a), k)]),
        ("%d less than %s" % (k, I(a)), "%s − %d" % (I(a), k), ["%d − %s" % (k, I(a)), "%s + %d" % (I(a), k), fr(I(a), k)]),
        ("%s subtracted from %d" % (I(a), k), "%d − %s" % (k, I(a)), ["%s − %d" % (I(a), k), "%d%s" % (k, I(a)), "%s + %d" % (I(a), k)]),
        ("%s multiplied by %d" % (I(a), k), "%d%s" % (k, I(a)), ["%s + %d" % (I(a), k), "%s<sup>%d</sup>" % (I(a), k), fr(I(a), k)]),
        ("%s divided by %d" % (I(a), k), fr(I(a), k), [fr(k, I(a)), "%d%s" % (k, I(a)), "%s − %d" % (I(a), k)]),
        ("%s squared" % I(a), "%s<sup>2</sup>" % I(a), ["2%s" % I(a), "%s + 2" % I(a), "%s<sup>%s</sup>" % (I(a), I(a))]),
        ("%d more than %d times %s" % (k, j, I(a)), "%d%s + %d" % (j, I(a), k), ["%d(%s + %d)" % (j, I(a), k), "%d%s + %d" % (k, I(a), j), "%d%s" % (j + k, I(a))]),
        ("%d times the sum of %s and %d" % (j, I(a), k), "%d(%s + %d)" % (j, I(a), k), ["%d%s + %d" % (j, I(a), k), "%s + %d" % (I(a), j * k), "%d%s" % (j * k, I(a))]),
        ("%s is doubled and then %d is taken away" % (I(a), k), "2%s − %d" % (I(a), k), ["2(%s − %d)" % (I(a), k), "%d − 2%s" % (k, I(a)), "%s<sup>2</sup> − %d" % (I(a), k)]),
        ("half of %s, plus %d" % (I(a), k), "%s + %d" % (fr(I(a), 2), k), [fr("%s + %d" % (I(a), k), 2), "2%s + %d" % (I(a), k), "%s + %d" % (fr(2, I(a)), k)]),
    ]
    src, right, wr = r.choice(forms)
    q = "Write an expression for: %s." % B(src)
    return T(q, right, wr, "<b>%s</b>." % right + (" The order matters for subtraction." if "less" in src or "subtracted" in src else ""))


def one_context(r):
    data = [
        ("A pen costs %s pence. How much do 5 pens cost, in pence?" % I("p"), "5%s" % I("p"), ["%s + 5" % I("p"), fr(I("p"), 5), "%s5" % I("p")]),
        ("Ava is %s years old. Her brother is 3 years older. How old is her brother?" % I("a"), "%s + 3" % I("a"), ["3%s" % I("a"), "%s − 3" % I("a"), "3 − %s" % I("a")]),
        ("A pizza is cut into %s equal slices. 4 friends share them equally. How many slices does each friend get?" % I("s"), fr(I("s"), 4), ["4%s" % I("s"), "%s − 4" % I("s"), fr(4, I("s"))]),
        ("A rectangle is %s cm long and 6 cm wide. What is its perimeter?" % I("l"), "2%s + 12" % I("l"), ["6%s" % I("l"), "%s + 6" % I("l"), "2%s + 6" % I("l")]),
        ("A rectangle is %s cm long and 6 cm wide. What is its area?" % I("l"), "6%s" % I("l"), ["2%s + 12" % I("l"), "%s + 6" % I("l"), "%s<sup>6</sup>" % I("l")]),
        ("Leo has %s marbles. He gives away 7. How many are left?" % I("m"), "%s − 7" % I("m"), ["7 − %s" % I("m"), "7%s" % I("m"), fr(I("m"), 7)]),
        ("A square has side %s cm. What is its area?" % I("x"), "%s<sup>2</sup>" % I("x"), ["4%s" % I("x"), "2%s" % I("x"), "%s + 4" % I("x")]),
        ("A square has side %s cm. What is its perimeter?" % I("x"), "4%s" % I("x"), ["%s<sup>2</sup>" % I("x"), "%s<sup>4</sup>" % I("x"), "%s + 4" % I("x")]),
        ("Tickets cost £%s each and a booking fee of £2 is added once. What is the cost of 3 tickets?" % I("t"), "3%s + 2" % I("t"), ["3(%s + 2)" % I("t"), "5%s" % I("t"), "%s + 5" % I("t")]),
        ("Isla has %s sweets and Arjun has twice as many. How many do they have altogether?" % I("s"), "3%s" % I("s"), ["2%s" % I("s"), "%s + 2" % I("s"), "%s<sup>2</sup>" % I("s")]),
    ]
    q, right, wr = r.choice(data)
    return T(q, right, wr, "The expression is <b>%s</b>." % right)


# ------------------------------------------------------------ substitution helpers
EXPRS = [
    # (html, working, value, wrong values)
    ("{k}{a}", "{k} × {X}", lambda k, j, x, y: k * x, lambda k, j, x, y: [k + x, int("%d%d" % (k, x)) if x >= 0 else None]),
    ("{k}{a} + {j}", "{k} × {X} + {j}", lambda k, j, x, y: k * x + j, lambda k, j, x, y: [k + x + j, k * (x + j)]),
    ("{k}{a} − {j}", "{k} × {X} − {j}", lambda k, j, x, y: k * x - j, lambda k, j, x, y: [k * (x - j), k + x - j]),
    ("{a}<sup>2</sup>", "{X}<sup>2</sup> = {X} × {X}", lambda k, j, x, y: x * x, lambda k, j, x, y: [2 * x, -x * x if x < 0 else x + 2]),
    ("{a}<sup>2</sup> + {k}", "{X}<sup>2</sup> + {k}", lambda k, j, x, y: x * x + k, lambda k, j, x, y: [2 * x + k, (x + k) ** 2]),
    ("{k}{a}<sup>2</sup>", "{k} × {X}<sup>2</sup>", lambda k, j, x, y: k * x * x, lambda k, j, x, y: [(k * x) ** 2, 2 * k * x]),
    ("{k}({a} + {j})", "{k} × ({x} + {j})", lambda k, j, x, y: k * (x + j), lambda k, j, x, y: [k * x + j, k + x + j]),
    ("{a}{b}", "{X} × {Y}", lambda k, j, x, y: x * y, lambda k, j, x, y: [x + y, int("%d%d" % (x, y)) if x >= 0 and y >= 0 else None]),
    ("{k}{a} + {b}", "{k} × {X} + {Y}", lambda k, j, x, y: k * x + y, lambda k, j, x, y: [k * (x + y), k + x + y]),
    ("{a}<sup>2</sup> − {b}", "{X}<sup>2</sup> − {Y}", lambda k, j, x, y: x * x - y, lambda k, j, x, y: [2 * x - y, x - y]),
    ("{frac}", "({x} + {j}) ÷ {k}", lambda k, j, x, y: F(x + j, k), lambda k, j, x, y: [F(x, k) + j, x + j]),
]


def sub_item(r, negs):
    html, work, fn, wfn = r.choice(EXPRS)
    a, b = sorted(r.sample(["a", "b", "c", "n", "p", "q", "x", "y"], 2))
    k, j = r.randint(2, 9), r.randint(1, 12)
    if negs:
        x = -r.randint(1, 8)
        y = r.choice([-1, 1]) * r.randint(1, 9)
    else:
        x, y = r.randint(2, 9), r.randint(2, 9)
    if html == "{frac}":
        if (x + j) % k or x + j == 0:
            return None
        shown = fr("%s + %d" % (I(a), j), k)
    else:
        shown = html.format(k=k, j=j, a=I(a), b=I(b))
    val = fn(k, j, x, y)
    if F(val).denominator != 1:
        return None
    uses_b = "{b}" in html
    given = "%s = %s" % (I(a), num(x)) + (" and %s = %s" % (I(b), num(y)) if uses_b else "")
    q = "Find the value of %s when %s." % (B(shown), given)
    X = num(x) if x >= 0 else "(%s)" % num(x)
    Y = num(y) if y >= 0 else "(%s)" % num(y)
    w = work.format(k=k, j=j, X=X, Y=Y, x=num(x))
    e = "Substitute: %s = <b>%s</b>." % (w, num(val))
    if "<sup>2</sup>" in html and x < 0:
        e += " A negative number squared is positive: (%s)<sup>2</sup> = %d." % (num(x), x * x)
    return QN(q, val, [w for w in wfn(k, j, x, y) if w is not None], e)


def one_sub(r):
    return sub_item(r, False)


def one_sub_neg(r):
    return sub_item(r, True)


# ------------------------------------------------------------ set 5: formulae
def formulae():
    its = []
    data = [
        ("The perimeter of a rectangle is %s. Find %s when %s = 7 and %s = 4." % (B("<i>P</i> = 2<i>l</i> + 2<i>w</i>"), I("P"), I("l"), I("w")), 22, [28, 13, 18],
         "<i>P</i> = 2 × 7 + 2 × 4 = 14 + 8 = <b>22</b>."),
        ("A plumber charges %s pounds, where %s is the number of hours. How much for 3 hours?" % (B("<i>C</i> = 35<i>h</i> + 40"), I("h")), 145, [78, 225, 105],
         "<i>C</i> = 35 × 3 + 40 = 105 + 40 = <b>145</b>."),
        ("Use %s to find %s when %s = 5, %s = 3 and %s = 4." % (B("<i>v</i> = <i>u</i> + <i>at</i>"), I("v"), I("u"), I("a"), I("t")), 17, [32, 12, 23],
         "<i>v</i> = 5 + 3 × 4 = 5 + 12 = <b>17</b>."),
        ("The area of a triangle is %s. Find %s when %s = 10 and %s = 6." % (B("<i>A</i> = ½<i>bh</i>"), I("A"), I("b"), I("h")), 30, [60, 8, 16],
         "<i>A</i> = ½ × 10 × 6 = <b>30</b>."),
        ("Use %s to change 20 °C into °F." % B("<i>F</i> = 1.8<i>C</i> + 32"), 68, [36, 52, 93.6],
         "<i>F</i> = 1.8 × 20 + 32 = 36 + 32 = <b>68</b>."),
        ("Use %s to find %s when %s = 3 and %s = 5." % (B("<i>s</i> = <i>a</i><sup>2</sup> + <i>b</i><sup>2</sup>"), I("s"), I("a"), I("b")), 34, [16, 64, 30],
         "<i>s</i> = 9 + 25 = <b>34</b>."),
        ("A taxi costs %s pounds for %s miles. How much is a 12-mile journey?" % (B("<i>T</i> = 3 + 2<i>m</i>"), I("m")), 27, [60, 17, 36],
         "<i>T</i> = 3 + 2 × 12 = 3 + 24 = <b>27</b>."),
        ("The mean of three numbers is %s. Find %s when %s = 8, %s = 11 and %s = 14." % (B("<i>M</i> = (<i>a</i> + <i>b</i> + <i>c</i>) ÷ 3"), I("M"), I("a"), I("b"), I("c")), 11, [33, 26.67, 14],
         "<i>M</i> = (8 + 11 + 14) ÷ 3 = 33 ÷ 3 = <b>11</b>."),
        ("Use %s to find %s when %s = 6." % (B("<i>y</i> = 3(<i>x</i> − 2)"), I("y"), I("x")), 12, [16, 7, 4],
         "<i>y</i> = 3 × (6 − 2) = 3 × 4 = <b>12</b>."),
        ("Use %s to find %s when %s = −4." % (B("<i>y</i> = 2<i>x</i> + 10"), I("y"), I("x")), 2, [18, -18, 6],
         "<i>y</i> = 2 × (−4) + 10 = −8 + 10 = <b>2</b>."),
        ("Use %s to find %s when %s = −3." % (B("<i>y</i> = <i>x</i><sup>2</sup> − 5"), I("y"), I("x")), 4, [-14, -11, 1],
         "<i>y</i> = (−3)<sup>2</sup> − 5 = 9 − 5 = <b>4</b>."),
        ("Use %s to find %s when %s = 10." % (B("<i>D</i> = <i>s</i><sup>2</sup> ÷ 20 + <i>s</i>"), I("D"), I("s")), 15, [11, 20, 6],
         "<i>D</i> = 100 ÷ 20 + 10 = 5 + 10 = <b>15</b>."),
    ]
    for q, a, w, e in data:
        its.append(QN(q, a, [F(str(x)) for x in w if F(str(x)).denominator <= 10], e))
    terms = [
        ("In the formula %s, which letter is the subject?" % B("<i>A</i> = <i>lw</i>"), I("A"), [I("l"), I("w"), "There is no subject"], "The subject is the letter on its own on one side: <b><i>A</i></b>."),
        ("Which of these is an %s?" % B("equation"), "3<i>x</i> + 1 = 10", ["3<i>x</i> + 1", "<i>A</i> = <i>lw</i> (true for every rectangle)", "4<i>x</i> + 2<i>x</i> ≡ 6<i>x</i>"],
         "An equation has an equals sign and is only true for some values: <b>3<i>x</i> + 1 = 10</b> (true when <i>x</i> = 3)."),
        ("Which of these is an %s?" % B("expression"), "5<i>n</i> − 2", ["5<i>n</i> − 2 = 8", "<i>P</i> = 4<i>s</i>", "<i>y</i> &gt; 3"], "An expression has no equals sign: <b>5<i>n</i> − 2</b>."),
        ("How many terms are in the expression %s?" % B("4<i>a</i> + 3<i>b</i> − 7"), "3", ["2", "4", "7"], "The terms are 4<i>a</i>, 3<i>b</i> and −7: <b>3</b> terms."),
        ("Which of these is a %s?" % B("formula"), "<i>P</i> = 2<i>l</i> + 2<i>w</i>", ["2<i>l</i> + 2<i>w</i>", "2<i>x</i> + 1 = 9", "3<i>x</i>"], "A formula connects quantities, for example the perimeter of any rectangle: <b><i>P</i> = 2<i>l</i> + 2<i>w</i></b>."),
        ("What is the coefficient of %s in %s?" % (I("x"), B("7 − 5<i>x</i> + <i>x</i><sup>2</sup>")), "−5", ["5", "7", "1"], "The coefficient is the number in front of <i>x</i>, including its sign: <b>−5</b>."),
        ("Which expression is the same as %s?" % B("<i>a</i> + <i>a</i> + <i>b</i> + <i>a</i>"), "3<i>a</i> + <i>b</i>", ["4<i>ab</i>", "3<i>ab</i>", "<i>a</i><sup>3</sup> + <i>b</i>"], "There are three <i>a</i>s and one <i>b</i>: <b>3<i>a</i> + <i>b</i></b>."),
        ("If %s = 5, which expression has the largest value?" % I("n"), "<i>n</i><sup>2</sup>", ["2<i>n</i>", "<i>n</i> + 2", "20 − <i>n</i>"], "<i>n</i><sup>2</sup> = 25, 2<i>n</i> = 10, <i>n</i> + 2 = 7, 20 − <i>n</i> = 15. So <b><i>n</i><sup>2</sup></b>."),
    ]
    for q, a, w, e in terms:
        its.append(T(q, a, w, e))
    return its


def body():
    return lesson(
        "<p>In algebra a letter stands for a number. We leave out the × sign: 3 × <i>a</i> = 3<i>a</i> and "
        "<i>a</i> × <i>b</i> = <i>ab</i>. We write <i>a</i> × <i>a</i> = <i>a</i>² and <i>a</i> ÷ 4 = <i>a</i>/4.</p>"
        "<p>To <b>substitute</b>, replace each letter with its value, then use BIDMAS. Put negative numbers in brackets.</p>",
        [("Find 3<i>a</i> + 2 when <i>a</i> = 5.", ["3<i>a</i> means 3 × 5 = 15.", "15 + 2 = 17."], "17"),
         ("Find <i>x</i>² + 2<i>x</i> when <i>x</i> = −3.", ["(−3)² = 9 and 2 × (−3) = −6.", "9 + (−6) = 3."], "3"),
         ("Write “5 less than twice <i>n</i>”.", ["Twice <i>n</i> is 2<i>n</i>.", "Then take away 5."], "2<i>n</i> − 5")],
        ["Reading 3<i>a</i> as 3 + <i>a</i>, or as a two-digit number: if <i>a</i> = 5, 3<i>a</i> is 15, not 8 or 35.",
         "Reading <i>a</i>² as 2<i>a</i>: if <i>a</i> = 6, <i>a</i>² is 36, not 12.",
         "Squaring a negative to get a negative: (−3)² = 9.",
         "Writing subtraction the wrong way round: “5 less than <i>n</i>” is <i>n</i> − 5."])


def main():
    sets = [S("Algebraic notation", collect(one_notation, 20, R)),
            S("Writing expressions", collect(one_words, 12, R) + collect(one_context, 8, R)),
            S("Substitution", collect(one_sub, 20, R)),
            S("Substitution with negative numbers", collect(one_sub_neg, 20, R)),
            S("Formulae and vocabulary", formulae())]
    make(7, "algebraic-notation-and-substitution", 11, "A",
         "Algebraic Notation and Substitution: Writing Expressions and Using Formulae",
         "Year 7 Algebra Worksheets: Algebraic Notation, Writing Expressions, Substitution and Formulae",
         "Algebraic notation and substitution",
         "Use and interpret algebraic notation, including: ab in place of a × b, 3y in place of y + y + y and 3 × y, a² in "
         "place of a × a, a/b in place of a ÷ b, coefficients written as fractions rather than as decimals, brackets; "
         "substitute numerical values into formulae and expressions, including scientific formulae.",
         "Free Year 7 algebra worksheets: algebraic notation, writing expressions from words, substituting positive and "
         "negative values, using formulae, and terms, expressions, equations and formulae. 100 questions with answers.",
         "3a means 3 × a, ab means a × b, and a² means a × a.",
         "To substitute, replace each letter with its value and use BIDMAS. Put negative values in brackets.",
         body(),
         [("What does 3a mean?", "3 × a. If a = 5, then 3a = 15."),
          ("Is a² the same as 2a?", "No. a² = a × a and 2a = a + a. If a = 6, a² = 36 but 2a = 12."),
          ("What is the difference between an expression, an equation and a formula?", "An expression has no equals sign (3x + 1). An equation is true for particular values (3x + 1 = 10). A formula connects quantities (P = 2l + 2w)."),
          ("How do I substitute a negative number?", "Put it in brackets and use the sign rules. If x = −3, x² = (−3)² = 9 and 2x = 2 × (−3) = −6.")],
         sets, R)


if __name__ == "__main__":
    main()
