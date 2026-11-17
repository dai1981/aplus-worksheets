# -*- coding: utf-8 -*-
"""
AU Year 7 Maths: Formulas and substitution (Australian Curriculum v9.0: AC9M7A01)
  python3 tools/gen_au_maths_y7_formulas_and_substitution.py
Using variables and algebraic notation, substituting values into expressions and everyday formulas, and
substituting into a formula to find an unknown value.
Wrong answers come from real mistakes: reading 3a as 3 + a or as the two-digit number 3a, reading a² as 2a,
ignoring the order of operations, and adding instead of undoing the operation when finding an unknown.
"""
import random
from fractions import Fraction as F
from au_hs import num, par, mcq, B, S, make, lesson, collect, QN, T, fr, MINUS, v

R = random.Random(71001)
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


def one_sub2(r):
    return sub_item(r, False)


# ------------------------------------------------------------ set 3: everyday formulas
def everyday():
    its = []
    data = [
        ("The perimeter of a rectangle is %s. Find %s when %s = 9 and %s = 5." % (B("<i>P</i> = 2<i>l</i> + 2<i>w</i>"), I("P"), I("l"), I("w")), 28, [45, 19, 23],
         "<i>P</i> = 2 × 9 + 2 × 5 = 18 + 10 = <b>28</b>."),
        ("An electrician charges %s dollars, where %s is the number of hours. How much for 4 hours?" % (B("<i>C</i> = 90<i>h</i> + 60"), I("h")), 420, [154, 600, 360],
         "<i>C</i> = 90 × 4 + 60 = 360 + 60 = <b>420</b>."),
        ("Use %s to find %s when %s = 6, %s = 2 and %s = 5." % (B("<i>v</i> = <i>u</i> + <i>at</i>"), I("v"), I("u"), I("a"), I("t")), 16, [40, 13, 30],
         "<i>v</i> = 6 + 2 × 5 = 6 + 10 = <b>16</b>."),
        ("The area of a triangle is %s. Find %s when %s = 12 and %s = 7." % (B("<i>A</i> = ½<i>bh</i>"), I("A"), I("b"), I("h")), 42, [84, F(19, 2), 19],
         "<i>A</i> = ½ × 12 × 7 = <b>42</b>."),
        ("The number of chairs around %s tables pushed in a row is %s. How many chairs for 8 tables?" % (I("t"), B("<i>c</i> = 2<i>t</i> + 2")), 18, [32, 12, 20],
         "<i>c</i> = 2 × 8 + 2 = <b>18</b>."),
        ("A phone plan costs %s dollars a month, where %s is the number of GB used over the limit. What is the bill for 3 extra GB?" % (B("<i>B</i> = 35 + 10<i>g</i>"), I("g")), 65, [135, 48, 45],
         "<i>B</i> = 35 + 10 × 3 = <b>65</b>."),
        ("Use %s to find %s when %s = 4 and %s = 3." % (B("<i>s</i> = <i>a</i><sup>2</sup> + <i>b</i><sup>2</sup>"), I("s"), I("a"), I("b")), 25, [14, 49, 7],
         "<i>s</i> = 16 + 9 = <b>25</b>."),
        ("The mean of three numbers is %s. Find %s when %s = 12, %s = 15 and %s = 21." % (B("<i>M</i> = (<i>a</i> + <i>b</i> + <i>c</i>) ÷ 3"), I("M"), I("a"), I("b"), I("c")), 16, [48, 29, 21],
         "<i>M</i> = (12 + 15 + 21) ÷ 3 = 48 ÷ 3 = <b>16</b>."),
        ("Use %s to find %s when %s = 7." % (B("<i>y</i> = 4(<i>x</i> − 3)"), I("y"), I("x")), 16, [25, 8, 31],
         "<i>y</i> = 4 × (7 − 3) = 4 × 4 = <b>16</b>."),
        ("A pool fills by %s litres after %s minutes. How many litres after 25 minutes?" % (B("<i>L</i> = 120<i>m</i> + 500"), I("m")), 3500, [3000, 645, 15500],
         "<i>L</i> = 120 × 25 + 500 = 3000 + 500 = <b>3500</b>."),
        ("The time to roast a chicken is %s minutes for %s kg. How long for a 2 kg chicken?" % (B("<i>T</i> = 40<i>w</i> + 20"), I("w")), 100, [120, 62, 80],
         "<i>T</i> = 40 × 2 + 20 = <b>100</b> minutes."),
    ]
    for q, a, w, e in data:
        its.append(QN(q, a, [F(str(x)) if not isinstance(x, F) else x for x in w], e))
    its.append(T("A taxi fare is %s dollars for %s km. How much is a 15 km trip?" % (B("<i>F</i> = 4.20 + 2.10<i>d</i>"), I("d")), "$35.70",
                 ["$94.50", "$6.30", "$31.50"], "<i>F</i> = 4.20 + 2.10 × 15 = 4.20 + 31.50 = <b>$35.70</b>."))
    terms = [
        ("In the formula %s, which letter is the subject?" % B("<i>A</i> = <i>lw</i>"), I("A"), [I("l"), I("w"), "There is no subject"], "The subject is the letter on its own on one side: <b><i>A</i></b>."),
        ("Which of these is a %s?" % B("formula"), "<i>P</i> = 4<i>s</i>", ["4<i>s</i>", "4<i>x</i> + 1 = 9", "<i>s</i> + 4"], "A formula connects quantities, for example the perimeter of any square: <b><i>P</i> = 4<i>s</i></b>."),
        ("How many terms are in the expression %s?" % B("6<i>a</i> + 2<i>b</i> − 9"), "3", ["2", "4", "9"], "The terms are 6<i>a</i>, 2<i>b</i> and −9: <b>3</b> terms."),
        ("What is the coefficient of %s in %s?" % (I("x"), B("8 + 3<i>x</i> + <i>y</i>")), "3", ["8", "1", "11"], "The coefficient is the number in front of <i>x</i>: <b>3</b>."),
        ("If %s = 4, which expression has the largest value?" % I("n"), "<i>n</i><sup>2</sup>", ["3<i>n</i>", "<i>n</i> + 10", "20 − <i>n</i>"], "<i>n</i><sup>2</sup> = 16, 3<i>n</i> = 12, <i>n</i> + 10 = 14, 20 − <i>n</i> = 16… check: 20 − 4 = 16 too."),
        ("In %s, what does %s stand for?" % (B("<i>C</i> = 90<i>h</i> + 60"), I("h")), "The number of hours", ["The total cost", "The call-out fee", "90 dollars"], "<i>h</i> is the variable that is multiplied by the hourly rate: <b>the number of hours</b>."),
        ("A variable is…", "a letter that stands for a number that can change", ["a number that never changes", "the answer to a sum", "the equals sign"], "<b>A letter that stands for a number that can change.</b>"),
        ("Which expression is the same as %s?" % B("<i>m</i> + <i>m</i> + <i>m</i> + <i>m</i>"), "4<i>m</i>", ["<i>m</i><sup>4</sup>", "<i>m</i> + 4", "4 + <i>m</i>"], "Four lots of <i>m</i>: <b>4<i>m</i></b>."),
    ]
    terms[4] = ("If %s = 4, which expression has the largest value?" % I("n"), "<i>n</i> + 10", ["3<i>n</i>", "2<i>n</i>", "<i>n</i><sup>2</sup> − 5"],
                "<i>n</i> + 10 = 14, 3<i>n</i> = 12, 2<i>n</i> = 8, <i>n</i><sup>2</sup> − 5 = 11. So <b><i>n</i> + 10</b>.")
    for q, a, w, e in terms:
        its.append(T(q, a[0].upper() + a[1:] if a[0].isalpha() and a[0].islower() and not a.startswith("<") else a, [x[0].upper() + x[1:] if x[0].isalpha() and x[0].islower() else x for x in w], e))
    return its


# ------------------------------------------------------------ set 4: finding an unknown
UNKNOWN = [
    # formula html, target letter, solve function (gives values dict) -> (question, answer, wrongs, explanation)
    "rect", "square", "speed", "cost", "triangle", "chairs",
]


def one_unknown(r):
    kind = r.choice(UNKNOWN)
    if kind == "rect":
        l, w = r.randint(5, 20), r.randint(2, 12)
        if l == w:
            return None
        P = 2 * l + 2 * w
        q = "Use %s. A rectangle has %s = %d and %s = %d. Find %s." % (B("<i>P</i> = 2<i>l</i> + 2<i>w</i>"), I("P"), P, I("l"), l, I("w"))
        return QN(q, w, [P - 2 * l, F(P - l, 2), P - l], "%d = 2 × %d + 2<i>w</i>, so %d = %d + 2<i>w</i>. 2<i>w</i> = %d, so <i>w</i> = <b>%d</b>." % (P, l, P, 2 * l, 2 * w, w))
    if kind == "square":
        s = r.randint(3, 25)
        q = "Use %s. A square has perimeter %s = %d cm. Find the side length %s." % (B("<i>P</i> = 4<i>s</i>"), I("P"), 4 * s, I("s"))
        return QN(q, s, [4 * s * 4, 4 * s - 4, 2 * s], "%d = 4<i>s</i>, so <i>s</i> = %d ÷ 4 = <b>%d</b> cm." % (4 * s, 4 * s, s), unit="")
    if kind == "speed":
        sp, t = r.choice([40, 50, 60, 80, 90, 100, 110]), r.randint(2, 6)
        d = sp * t
        q = "Use %s, where %s is distance in km, %s is speed in km/h and %s is time in hours. Find %s when %s = %d and %s = %d." % (
            B("<i>d</i> = <i>st</i>"), I("d"), I("s"), I("t"), I("t"), I("d"), d, I("s"), sp)
        return QN(q, t, [d * sp, d - sp, F(sp, d) if F(sp, d).denominator <= 4 else t + 1], "%d = %d × <i>t</i>, so <i>t</i> = %d ÷ %d = <b>%d</b>." % (d, sp, d, sp, t))
    if kind == "cost":
        fee, rate, h = r.choice([40, 50, 60, 80]), r.choice([25, 30, 45, 60, 75]), r.randint(2, 8)
        C = fee + rate * h
        q = "A plumber charges %s dollars, where %s is the number of hours. A bill is $%d. Find %s." % (B("<i>C</i> = %d<i>h</i> + %d" % (rate, fee)), I("h"), C, I("h"))
        return QN(q, h, [F(C, rate) if F(C, rate).denominator == 1 else C - fee, C - fee, F(C + fee, rate) if F(C + fee, rate).denominator == 1 else h + 2],
                  "%d = %d<i>h</i> + %d. Take away %d: %d<i>h</i> = %d. Divide by %d: <i>h</i> = <b>%d</b>." % (C, rate, fee, fee, rate, C - fee, rate, h))
    if kind == "triangle":
        b, h = r.randint(3, 16), r.randint(2, 14)
        if (b * h) % 2:
            return None
        A = b * h // 2
        q = "Use %s. A triangle has area %s = %d cm² and base %s = %d cm. Find the height %s." % (B("<i>A</i> = ½<i>bh</i>"), I("A"), A, I("b"), b, I("h"))
        return QN(q, h, [F(A, b) if F(A, b) != h else h * 2, A * 2, A - b if A - b > 0 else h + 3], "%d = ½ × %d × <i>h</i> = %s<i>h</i>, so <i>h</i> = %d ÷ %s = <b>%d</b> cm." % (A, b, num(F(b, 2)), A, num(F(b, 2)), h))
    t = r.randint(4, 30)
    c = 2 * t + 2
    q = "Chairs around tables in a row: %s. There are %d chairs. How many tables (%s)?" % (B("<i>c</i> = 2<i>t</i> + 2"), c, I("t"))
    return QN(q, t, [F(c, 2), c - 2, F(c + 2, 2)], "%d = 2<i>t</i> + 2, so 2<i>t</i> = %d and <i>t</i> = <b>%d</b>." % (c, c - 2, t))


def body():
    return lesson(
        "<p>A <b>variable</b> is a letter that stands for a number. We leave out the × sign: 3 × <i>a</i> = 3<i>a</i> and "
        "<i>a</i> × <i>b</i> = <i>ab</i>. We write <i>a</i> × <i>a</i> = <i>a</i>² and <i>a</i> ÷ 4 as a fraction.</p>"
        "<p>To <b>substitute</b>, replace each letter with its value, then use the order of operations. "
        "A <b>formula</b> such as <i>P</i> = 2<i>l</i> + 2<i>w</i> links quantities. If you know all but one value, "
        "substitute the ones you know and undo the operations to find the unknown.</p>",
        [("Find 3<i>a</i> + 2 when <i>a</i> = 5.", ["3<i>a</i> means 3 × 5 = 15.", "15 + 2 = 17."], "17"),
         ("Use <i>A</i> = <i>lw</i> to find <i>A</i> when <i>l</i> = 8 and <i>w</i> = 3.", ["8 × 3."], "24"),
         ("Use <i>P</i> = 2<i>l</i> + 2<i>w</i> with <i>P</i> = 30 and <i>l</i> = 9 to find <i>w</i>.", ["30 = 18 + 2<i>w</i>.", "2<i>w</i> = 12."], "<i>w</i> = 6")],
        ["Reading 3<i>a</i> as 3 + <i>a</i>, or as a two-digit number: if <i>a</i> = 5, 3<i>a</i> is 15, not 8 or 35.",
         "Reading <i>a</i>² as 2<i>a</i>: if <i>a</i> = 6, <i>a</i>² is 36, not 12.",
         "Ignoring the order of operations: 2 × 9 + 2 × 5 is 28, not 2 × 14 × 5.",
         "Finding an unknown by adding instead of undoing: if 2<i>w</i> = 12, then <i>w</i> = 6, not 24."])


def main():
    sets = [S("Algebraic notation", collect(one_notation, 20, R)),
            S("Substituting into expressions", collect(one_sub, 20, R)),
            S("More substitution", collect(one_sub2, 20, R)),
            S("Everyday formulas", everyday()),
            S("Finding an unknown in a formula", collect(one_unknown, 20, R))]
    make(7, "formulas-and-substitution", 10, "AC9M7A01",
         "Formulas and Substitution: Variables, Expressions and Everyday Formulas",
         "Year 7 Substitution Worksheets: Algebraic Notation, Substituting into Formulas and Finding Unknowns (Free, Answer Key)",
         "Formulas and substitution",
         "recognise and use variables to represent everyday formulas algebraically and substitute values into formulas to determine an unknown",
         "Free Year 7 maths worksheets on formulas and substitution for the Australian Curriculum (AC9M7A01): algebraic notation, "
         "substituting into expressions, everyday formulas and finding an unknown in a formula. 100 questions with an answer key.",
         "3a means 3 × a, ab means a × b, and a² means a × a.",
         "To substitute, replace each letter with its value, then follow the order of operations.",
         body(),
         [("What does 3a mean?", "3 × a. If a = 5, then 3a = 15."),
          ("Is a² the same as 2a?", "No. a² = a × a and 2a = a + a. If a = 6, a² = 36 but 2a = 12."),
          ("What is a formula?", "A rule that links quantities using variables, such as P = 2l + 2w for the perimeter of a rectangle."),
          ("How do I find an unknown in a formula?", "Substitute the values you know, then undo the operations. If 30 = 18 + 2w, then 2w = 12 and w = 6.")],
         sets, R)


if __name__ == "__main__":
    main()
