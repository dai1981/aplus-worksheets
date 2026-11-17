# -*- coding: utf-8 -*-
"""
AU Year 7 Maths: Algebraic expressions (Australian Curriculum v9.0: AC9M7A02)
  python3 tools/gen_au_maths_y7_algebraic_expressions.py
Writing algebraic expressions from words and from everyday situations using constants, variables, operations
and brackets, collecting like terms, and expressions for perimeters, patterns and costs.
Wrong answers come from real mistakes: writing subtraction the wrong way round, leaving out brackets
(3 lots of n + 2 is 3(n + 2), not 3n + 2), combining unlike terms (3x + 2y = 5xy), and losing a minus sign.
"""
import random
from fractions import Fraction as F
from au_hs import num, par, mcq, B, S, make, lesson, collect, T, expr, MINUS, fr, aud

R = random.Random(71101)
VARS = ["<i>a</i>", "<i>b</i>", "<i>x</i>", "<i>y</i>", "<i>m</i>", "<i>n</i>", "<i>p</i>", "<i>t</i>"]


def I(s):
    return "<i>%s</i>" % s


def nz(r, lo, hi):
    while True:
        k = r.randint(lo, hi)
        if k:
            return k


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


# ------------------------------------------------------------ set 2: situations
def one_situation(r):
    k = r.randint(2, 9)
    j = r.randint(2, 12)
    kind = r.randint(0, 9)
    if kind == 0:
        q = "Pies cost $%d each. Write an expression for the cost, in dollars, of %s pies." % (k, I("n"))
        return T(q, "%d%s" % (k, I("n")), ["%s + %d" % (I("n"), k), fr(I("n"), k), "%s%d" % (I("n"), k)], "%s pies at $%d each cost <b>%d%s</b> dollars." % (I("n"), k, k, I("n")))
    if kind == 1:
        q = "Mia is %s years old. Her cousin is %d years older. Write an expression for her cousin's age." % (I("a"), j)
        return T(q, "%s + %d" % (I("a"), j), ["%d%s" % (j, I("a")), "%s − %d" % (I("a"), j), "%d − %s" % (j, I("a"))], "Older means add: <b>%s + %d</b>." % (I("a"), j))
    if kind == 2:
        q = "A pizza is cut into %s equal slices and shared equally by %d friends. Write an expression for the slices each friend gets." % (I("s"), k)
        return T(q, fr(I("s"), k), ["%d%s" % (k, I("s")), "%s − %d" % (I("s"), k), fr(k, I("s"))], "Sharing equally means dividing: <b>%s</b>." % fr(I("s"), k))
    if kind == 3:
        q = "A rectangle is %s cm long and %d cm wide. Write an expression for its perimeter." % (I("l"), k)
        return T(q, "2%s + %d" % (I("l"), 2 * k), ["%d%s" % (k, I("l")), "%s + %d" % (I("l"), k), "2%s + %d" % (I("l"), k)], "Two lengths and two widths: 2%s + 2 × %d = <b>2%s + %d</b>." % (I("l"), k, I("l"), 2 * k))
    if kind == 4:
        q = "Liam has %s dollars. He spends $%d. Write an expression for the money he has left." % (I("m"), j)
        return T(q, "%s − %d" % (I("m"), j), ["%d − %s" % (j, I("m")), "%d%s" % (j, I("m")), "%s + %d" % (I("m"), j)], "Spending means take away from what he has: <b>%s − %d</b>." % (I("m"), j))
    if kind == 5:
        q = "Movie tickets cost $%s each and there is a $%d booking fee for the whole order. Write an expression for the cost of %d tickets." % (I("t"), j, k)
        return T(q, "%d%s + %d" % (k, I("t"), j), ["%d(%s + %d)" % (k, I("t"), j), "%d%s" % (k + j, I("t")), "%s + %d" % (I("t"), k + j)],
                 "%d tickets cost %d%s, and the fee is added once: <b>%d%s + %d</b>." % (k, k, I("t"), k, I("t"), j))
    if kind == 6:
        q = "Each show bag has %s lollies and %d stickers. Write an expression for the total number of items in %d show bags." % (I("n"), j, k)
        return T(q, "%d(%s + %d)" % (k, I("n"), j), ["%d%s + %d" % (k, I("n"), j), "%s + %d" % (I("n"), k * j), "%d%s" % (k * j, I("n"))],
                 "Each bag has %s + %d items, and there are %d bags: <b>%d(%s + %d)</b>. The brackets are needed." % (I("n"), j, k, k, I("n"), j))
    if kind == 7:
        q = "A square has sides of %s cm. Write an expression for its perimeter." % I("x")
        return T(q, "4%s" % I("x"), ["%s<sup>2</sup>" % I("x"), "%s + 4" % I("x"), "%s<sup>4</sup>" % I("x")], "Four equal sides: <b>4%s</b>." % I("x"))
    if kind == 8:
        q = "Zara has %s stickers and Kai has %d times as many. Write an expression for the number they have altogether." % (I("s"), k)
        return T(q, "%d%s" % (k + 1, I("s")), ["%d%s" % (k, I("s")), "%s + %d" % (I("s"), k), "%s<sup>%d</sup>" % (I("s"), k)],
                 "Zara has %s and Kai has %d%s. Together: %s + %d%s = <b>%d%s</b>." % (I("s"), k, I("s"), I("s"), k, I("s"), k + 1, I("s")))
    q = "A bus has %s passengers. At a stop %d get off and %d get on. Write an expression for the number of passengers now." % (I("p"), k, j)
    return T(q, expr([(1, I("p")), (j - k, "")]), ["%s − %d" % (I("p"), k + j), "%s + %d" % (I("p"), k + j), expr([(1, I("p")), (k - j, "")]) if k != j else "%s" % I("p") + " + 1"],
             "%s − %d + %d = <b>%s</b>." % (I("p"), k, j, expr([(1, I("p")), (j - k, "")])))


# ------------------------------------------------------------ set 1: like terms, one letter
def one_like1(r):
    x = r.choice(VARS)
    cs = [r.randint(2, 9), nz(r, -7, 9), nz(r, -6, 8)]
    if r.random() < 0.5:
        cs = cs[:2]
    tot = sum(cs)
    if tot == 0:
        return None
    q = "Simplify %s." % B(expr([(c, x) for c in cs]))
    right = expr([(tot, x)])
    absum = sum(abs(c) for c in cs)
    wr = [expr([(absum, x)]) if absum != tot else expr([(tot + 2, x)]), "%s%s" % (num(tot), x.replace("</i>", "<sup>%d</sup></i>" % len(cs)).replace("<i>", "<i>") if False else x + "<sup>%d</sup>" % len(cs)),
          expr([(-tot, x)]), num(tot)]
    e = "All the terms are %s terms, so add the numbers: %s = %s. The answer is <b>%s</b>." % (
        x, " + ".join("(%s)" % num(c) if c < 0 else num(c) for c in cs), num(tot), right)
    return T(q, right, [w for w in wr if w != right][:3], e)


# ------------------------------------------------------------ set 2: like terms, two letters and numbers
def one_like2(r):
    x, y = sorted(r.sample(VARS, 2))
    a1, b1, a2, b2 = r.randint(1, 9), nz(r, -6, 8), nz(r, -6, 6), nz(r, -6, 7)
    c = nz(r, -9, 9) if r.random() < 0.5 else 0
    terms = [(a1, x), (b1, y), (a2, x), (b2, y)] + ([(c, "")] if c else [])
    r.shuffle(terms)
    A, Bb = a1 + a2, b1 + b2
    if A == 0 or Bb == 0:
        return None
    right = expr([(A, x), (Bb, y), (c, "")])
    wr = [expr([(A + Bb, x + y)] + ([(c, "")] if c else [])),                     # combined unlike terms
          expr([(abs(a1) + abs(a2), x), (abs(b1) + abs(b2), y), (c, "")]),         # ignored signs
          expr([(A, x), (-Bb, y), (c, "")]),
          expr([(A + Bb + c, x + y)])]
    wr = [w for w in wr if w != right]
    q = "Simplify %s." % B(expr(terms))
    e = "Collect the %s terms (%s) and the %s terms (%s)%s. The answer is <b>%s</b>." % (
        x, expr([(A, x)]), y, expr([(Bb, y)]), ", then the number" if c else "", right)
    return T(q, right, wr[:3], e)


# ------------------------------------------------------------ (multiplying terms are in Year 8): multiply and divide terms
# ------------------------------------------------------------ set 5: expressions in problems
def problems():
    x, n, w = I("x"), I("n"), I("w")
    data = [
        ("A triangle has sides %s cm, (%s + 3) cm and 2%s cm. Write a simplified expression for its perimeter." % (x, x, x), "4%s + 3" % x, ["2%s<sup>2</sup> + 3" % x, "4%s" % x, "3%s + 3" % x], "%s + %s + 3 + 2%s = <b>4%s + 3</b>." % (x, x, x, x)),
        ("Pattern %s of matchstick squares in a row uses 3%s + 1 matches. How many matches are in pattern 10?" % (n, n), "31", ["30", "40", "13"], "3 × 10 + 1 = <b>31</b>."),
        ("Which expression means “add 5 to %s, then multiply by 3”?" % n, "3(%s + 5)" % n, ["3%s + 5" % n, "%s + 15" % n, "5(%s + 3)" % n], "The adding happens first, so it goes in brackets: <b>3(%s + 5)</b>." % n),
        ("Which expression means “multiply %s by 3, then add 5”?" % n, "3%s + 5" % n, ["3(%s + 5)" % n, "%s + 8" % n, "5%s + 3" % n], "Multiply first, then add: <b>3%s + 5</b>." % n),
        ("A rectangle is %s cm wide and 4 cm longer than it is wide. Write an expression for its perimeter." % w, "4%s + 8" % w, ["2%s + 4" % w, "%s<sup>2</sup> + 4%s" % (w, w), "4%s + 4" % w], "Length = %s + 4. Perimeter = 2%s + 2(%s + 4) = <b>4%s + 8</b>." % (w, w, w, w)),
        ("Chloe is %s years old. Her dad is 3 times her age plus 2 years. Write an expression for her dad's age." % I("c"), "3%s + 2" % I("c"), ["3(%s + 2)" % I("c"), "%s + 5" % I("c"), "5%s" % I("c")], "3 times her age is 3%s, then add 2: <b>3%s + 2</b>." % (I("c"), I("c"))),
        ("Which expression is the same as %s?" % B("%s + %s + %s + 2" % (x, x, x)), "3%s + 2" % x, ["%s<sup>3</sup> + 2" % x, "5%s" % x, "3(%s + 2)" % x], "Three lots of %s, plus 2: <b>3%s + 2</b>." % (x, x)),
        ("Which expression is the same as %s?" % B("%s + 2 + %s + 2 + %s + 2" % (x, x, x)), "3(%s + 2)" % x, ["3%s + 2" % x, "%s + 6" % x, "6%s" % x], "Three lots of (%s + 2): <b>3(%s + 2)</b>, which is also 3%s + 6." % (x, x, x)),
        ("A plumber charges a $90 call-out fee plus $70 an hour. Write an expression for the cost, in dollars, of %s hours." % I("h"), "70%s + 90" % I("h"), ["90%s + 70" % I("h"), "160%s" % I("h"), "70(%s + 90)" % I("h")], "$70 for each hour and $90 once: <b>70%s + 90</b>." % I("h")),
        ("Water drains from a 500 L tank at 20 L a minute. Write an expression for the litres left after %s minutes." % I("m"), "500 − 20%s" % I("m"), ["20%s − 500" % I("m"), "480%s" % I("m"), "500 + 20%s" % I("m")], "20%s litres have drained: <b>500 − 20%s</b>." % (I("m"), I("m"))),
        ("What is the value of 2(%s + 7) when %s = 5?" % (n, n), "24", ["17", "19", "70"], "Brackets first: 5 + 7 = 12, then 2 × 12 = <b>24</b>."),
        ("Write an expression for the next even number after the even number %s." % I("e"), "%s + 2" % I("e"), ["%s + 1" % I("e"), "2%s" % I("e"), "%s<sup>2</sup>" % I("e")], "Even numbers go up in 2s: <b>%s + 2</b>." % I("e")),
        ("Write an expression for the sum of three consecutive whole numbers, starting with %s." % n, "3%s + 3" % n, ["3%s" % n, "%s + 3" % n, "3%s + 6" % n], "%s + (%s + 1) + (%s + 2) = <b>3%s + 3</b>." % (n, n, n, n)),
        ("A phone plan costs $%s a month. Write an expression for the cost of one year." % I("c"), "12%s" % I("c"), ["%s + 12" % I("c"), fr(I("c"), 12), "365%s" % I("c")], "12 months: <b>12%s</b>." % I("c")),
        ("Which is a constant in the expression %s?" % B("5%s + 9" % x), "9", ["5", "%s" % x, "5%s" % x], "A constant is a number on its own: <b>9</b>."),
        ("Which expression has a variable, a constant and brackets?", "4(%s − 1)" % x, ["4%s" % x, "4 − 1", "%s<sup>4</sup>" % x], "<b>4(%s − 1)</b> has the variable %s, the constant 1 and brackets." % (x, x)),
        ("A cricket team scored %s runs on Saturday and 25 fewer on Sunday. Write an expression for the total runs." % I("r"), "2%s − 25" % I("r"), ["%s − 25" % I("r"), "2%s + 25" % I("r"), "25 − 2%s" % I("r")], "%s + (%s − 25) = <b>2%s − 25</b>." % (I("r"), I("r"), I("r"))),
        ("Simplify %s." % B("4%s + 3 + 2%s + 5" % (x, x)), "6%s + 8" % x, ["14%s" % x, "6%s + 3" % x, "8%s + 6" % x], "%s terms: 4%s + 2%s = 6%s. Numbers: 3 + 5 = 8. <b>6%s + 8</b>." % (x, x, x, x, x)),
        ("Simplify %s." % B("7%s + 2%s − %s" % (n, I("m"), n)), "6%s + 2%s" % (n, I("m")), ["8%s%s" % (n, I("m")), "7%s + %s" % (n, I("m")), "6%s%s" % (n, I("m"))], "7%s − %s = 6%s. The %s term stays: <b>6%s + 2%s</b>." % (n, n, n, I("m"), n, I("m"))),
        ("Grace buys %s drinks at $3 and %s snacks at $2. Write an expression for the total cost in dollars." % (I("d"), I("s")), "3%s + 2%s" % (I("d"), I("s")), ["5%s%s" % (I("d"), I("s")), "5(%s + %s)" % (I("d"), I("s")), "%s + %s + 5" % (I("d"), I("s"))], "Drinks cost 3%s and snacks cost 2%s: <b>3%s + 2%s</b>. These are unlike terms." % (I("d"), I("s"), I("d"), I("s"))),
    ]
    return [T(q, a, w, e) for q, a, w, e in data]


def body():
    return lesson(
        "<p>An <b>expression</b> uses <b>variables</b> (letters), <b>constants</b> (numbers), operations and sometimes brackets. "
        "It has no equals sign. Translate words carefully: “5 less than <i>n</i>” is <i>n</i> − 5, and "
        "“3 lots of <i>n</i> + 2” needs brackets: 3(<i>n</i> + 2).</p>"
        "<p><b>Like terms</b> have exactly the same letters. Only like terms can be collected: 3<i>x</i> + 5<i>x</i> = 8<i>x</i>, "
        "but 3<i>x</i> + 2<i>y</i> stays as it is.</p>",
        [("Write “7 more than twice <i>n</i>”.", ["Twice <i>n</i> is 2<i>n</i>.", "Then add 7."], "2<i>n</i> + 7"),
         ("Each bag holds <i>n</i> apples and 2 oranges. Write the total fruit in 3 bags.", ["One bag: <i>n</i> + 2.", "Three bags: 3(<i>n</i> + 2)."], "3(<i>n</i> + 2)"),
         ("Simplify 5<i>x</i> + 3<i>y</i> − 2<i>x</i> + <i>y</i>.", ["<i>x</i> terms: 3<i>x</i>.", "<i>y</i> terms: 4<i>y</i>."], "3<i>x</i> + 4<i>y</i>")],
        ["Writing subtraction the wrong way round: “5 less than <i>n</i>” is <i>n</i> − 5, not 5 − <i>n</i>.",
         "Leaving out brackets: 3 lots of (<i>n</i> + 2) is 3(<i>n</i> + 2), not 3<i>n</i> + 2.",
         "Combining unlike terms: 3<i>x</i> + 2<i>y</i> is not 5<i>xy</i>.",
         "Losing the sign in front of a term: 7<i>n</i> − <i>n</i> is 6<i>n</i>."])


def main():
    sets = [S("Words to expressions", collect(one_words, 20, R)),
            S("Expressions from situations", collect(one_situation, 20, R)),
            S("Collecting like terms", collect(one_like1, 20, R)),
            S("Like terms with two variables", collect(one_like2, 20, R)),
            S("Expressions in problems", problems())]
    make(7, "algebraic-expressions", 11, "AC9M7A02",
         "Algebraic Expressions: Writing Expressions and Collecting Like Terms",
         "Year 7 Algebraic Expressions Worksheets: Writing Expressions from Words and Like Terms (Free, Answer Key)",
         "Algebraic expressions",
         "formulate algebraic expressions using constants, variables, operations and brackets",
         "Free Year 7 maths worksheets on algebraic expressions for the Australian Curriculum (AC9M7A02): writing expressions "
         "from words and situations, using brackets, and collecting like terms. 100 questions with an answer key.",
         "An expression uses variables, constants, operations and brackets, with no equals sign.",
         "Only like terms can be collected: 3x + 5x = 8x, but 3x + 2y stays as it is.",
         body(),
         [("What is an algebraic expression?", "A combination of variables, numbers and operations with no equals sign, such as 3n + 5."),
          ("When do I need brackets?", "When a whole group is multiplied or divided. Three bags each holding n + 2 items is 3(n + 2)."),
          ("What are like terms?", "Terms with exactly the same letters and powers, such as 3x and −5x. They can be added or subtracted."),
          ("How do I write “5 less than n”?", "n − 5. The 5 is taken away from n.")],
         sets, R)


if __name__ == "__main__":
    main()
