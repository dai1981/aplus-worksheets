# -*- coding: utf-8 -*-
"""
Texas Grade 3 Math: Multiplication and Division Word Problems (TEKS 3.4K, 3.5B, 3.5C)
  python3 tools/gen_ustx_math_g3_mult_div_word_problems.py
Choosing the equation for a one-step problem, strip diagrams with equal parts, "times as many" comparisons,
one-step problems to solve, and two-step problems within 100.
Wrong answers come from real mistakes: adding when the problem has equal groups, multiplying when the total is
already given, reading "3 times as many" as "3 more", and stopping after the first step.
"""
import random
from tx_common import (Kid, mcq, collect, finish, make, fig, figure, lesson, S, comma, strip_svg, FILL, example)

R = random.Random(60801)
WHITE = "#ffffff"

GROUPS = [("bags", "apples"), ("boxes", "crayons"), ("rows", "chairs"), ("teams", "players"), ("vases", "flowers"),
          ("packs", "pencils"), ("plates", "tamales"), ("shelves", "books"), ("groups", "students"), ("cartons", "eggs")]


def fact(r, lo=2, hi=10):
    return r.randint(lo, hi), r.randint(lo, hi)


# ------------------------------------------------------------ set 1: which equation?
def one_eq(r):
    g, n = fact(r)
    t = g * n
    cont, thing = r.choice(GROUPS)
    k = Kid(r).next()
    kind = r.choice(["mult", "share", "groups"])
    if kind == "mult":
        q = "%s has %d %s with %d %s in each. How many %s in all? Which equation can you use? (Let ☐ be the unknown.)" % (k["n"], g, cont, n, thing, thing)
        right = "%d × %d = ☐" % (g, n)
        wrong = ["%d + %d = ☐" % (g, n), "%d ÷ %d = ☐" % (g, n) if g >= n else "%d ÷ %d = ☐" % (n, g), "☐ × %d = %d" % (n, g)]
    elif kind == "share":
        q = "%s puts %d %s equally into %d %s. How many %s go in each? Which equation can you use?" % (k["n"], t, thing, g, cont, thing)
        right = "%d ÷ %d = ☐" % (t, g)
        wrong = ["%d × %d = ☐" % (t, g), "%d − %d = ☐" % (t, g), "☐ ÷ %d = %d" % (g, t)]
    else:
        q = "%s has %d %s. %s puts %d in each of the %s. How many %s does %s fill? Which equation can you use?" % (k["n"], t, thing, k["He"], n, cont, cont, k["he"])
        right = "%d × ☐ = %d" % (n, t)
        wrong = ["%d × %d = ☐" % (n, t), "%d + ☐ = %d" % (n, t), "%d − %d = ☐" % (t, n)]
    return mcq(q, right, wrong, "%s" % ("Equal groups put together: multiply. <b>%s</b>." % right if kind == "mult" else "A total split into equal groups: <b>%s</b>." % right))


# ------------------------------------------------------------ set 2: strip diagrams with equal parts
def one_strip(r):
    g, n = r.randint(2, 6), r.randint(3, 10)
    t = g * n
    kind = r.choice(["total", "part"])
    if kind == "total":
        pic = strip_svg([(str(n), 1, FILL)] * g, "?")
        return mcq(fig(pic) + "The strip diagram has %d equal parts. What number does the ? stand for?" % g, t, [g + n, t + n, t - n, n * (g + 1) + 1],
                   "%d equal parts of %d: %d × %d = <b>%d</b>." % (g, n, g, n, t))
    pic = strip_svg([("?", 1, WHITE)] * g, str(t))
    return mcq(fig(pic) + "The whole is %d, split into %d equal parts. What number goes in each part?" % (t, g), n, [t - g, g, n + 1, n - 1],
               "%d ÷ %d = <b>%d</b>, because %d × %d = %d." % (t, g, n, g, n, t))


# ------------------------------------------------------------ set 3: times as many
def one_times(r):
    k1, k2 = Kid(r).next(), Kid(r).next()
    if k1["n"] == k2["n"]:
        return None
    n, m = r.randint(2, 10), r.randint(2, 5)
    kind = r.choice(["find", "find", "expr", "back"])
    what = r.choice(["shells", "stickers", "marbles", "rocks", "cards"])
    if kind == "find":
        q = "%s has %d %s. %s has %d times as many %s as %s. How many %s does %s have?" % (k1["n"], n, what, k2["n"], m, what, k1["n"], what, k2["n"])
        return mcq(q, m * n, [m + n, m * n + n, m * n - n if m * n - n != n else m * n + 1], "%d times as many as %d is %d × %d = <b>%d</b>." % (m, n, m, n, m * n))
    if kind == "expr":
        q = "Which sentence describes %d × %d?" % (m, n)
        right = "%d times as many as %d" % (m, n)
        return mcq(q, right, ["%d more than %d" % (m, n), "%d less than %d" % (m, n), "%d groups of %d" % (n, m + 1)],
                   "%d × %d means %d groups of %d, or <b>%s</b>." % (m, n, m, n, right))
    t = m * n
    q = "%s has %d %s. That is %d times as many as %s has. How many %s does %s have?" % (k2["n"], t, what, m, k1["n"], what, k1["n"])
    return mcq(q, n, [t - m, t * m if t * m <= 100 else t + m, m], "%d is %d times as many as the unknown: ☐ × %d = %d, so ☐ = %d ÷ %d = <b>%d</b>." % (t, m, m, t, t, m, n))


# ------------------------------------------------------------ set 4: one-step problems
def one_step(r):
    g, n = fact(r)
    t = g * n
    cont, thing = r.choice(GROUPS)
    kind = r.choice(["mult", "div"])
    if kind == "mult":
        q = "There are %d %s. Each has %d %s. How many %s are there in all?" % (g, cont, n, thing, thing)
        return mcq(q, t, [g + n, t - n, t + n, t + 1], "%d × %d = <b>%d</b> %s." % (g, n, t, thing))
    q = "There are %d %s. They are put equally into %d %s. How many %s are in each?" % (t, thing, g, cont, thing)
    return mcq(q, n, [t - g, n + 1, g if g != n else n - 1, t + g], "%d ÷ %d = <b>%d</b>, because %d × %d = %d." % (t, g, n, g, n, t))


# ------------------------------------------------------------ set 5: two-step problems within 100
def two_step(r):
    k = Kid(r).next()
    kind = r.choice(["mult_add", "mult_sub", "div_add", "mult_mult_sum"])
    if kind == "mult_add":
        g, n, e = r.randint(3, 9), r.randint(3, 9), r.randint(4, 15)
        if g * n + e > 100:
            return None
        q = "%s buys %d packs of %d stickers. %s friend gives %s %d more. How many stickers does %s have now?" % (k["n"], g, n, k["His"], k["him"], e, k["he"])
        return mcq(q, g * n + e, [g * n, g + n + e, g * (n + e) if g * (n + e) <= 100 else g * n + e + 10], "%d × %d = %d. Then %d + %d = <b>%d</b>." % (g, n, g * n, g * n, e, g * n + e))
    if kind == "mult_sub":
        g, n = r.randint(4, 10), r.randint(4, 10)
        e = r.randint(3, g * n - 5)
        q = "A class sets up %d rows of %d chairs. %d chairs are taken away. How many chairs are left?" % (g, n, e)
        return mcq(q, g * n - e, [g * n, g * n + e, g + n - e if g + n - e > 0 else g * n - e + 10, g * n - e - 1], "%d × %d = %d. Then %d − %d = <b>%d</b>." % (g, n, g * n, g * n, e, g * n - e))
    if kind == "div_add":
        g, n, e = r.randint(2, 8), r.randint(3, 10), r.randint(2, 9)
        t = g * n
        q = "%s shares %d grapes equally among %d friends and keeps none. Then one friend picks %d more grapes. How many grapes does that friend have now?" % (k["n"], t, g, e)
        return mcq(q, n + e, [n, t + e, t - g + e, n + e + 1], "%d ÷ %d = %d each. Then %d + %d = <b>%d</b>." % (t, g, n, n, e, n + e))
    a, b, c, d = r.randint(2, 6), r.randint(2, 6), r.randint(2, 6), r.randint(2, 6)
    if a * b + c * d > 100 or a * b == c * d:
        return None
    q = "A store sells %d boxes of %d markers and %d boxes of %d pens. How many markers and pens is that in all?" % (a, b, c, d)
    return mcq(q, a * b + c * d, [a + b + c + d, a * b, (a + c) * (b + d), a * b + c * d + 2], "%d × %d = %d and %d × %d = %d. %d + %d = <b>%d</b>." % (a, b, a * b, c, d, c * d, a * b, c * d, a * b + c * d))


def build():
    sets = [S("Which equation matches?", collect(one_eq, 20, R)),
            S("Strip diagrams with equal parts", collect(one_strip, 20, R)),
            S("Times as many", collect(one_times, 20, R)),
            S("One-step problems", collect(one_step, 20, R)),
            S("Two-step problems", collect(two_step, 20, R))]
    finish(sets, R)
    body = lesson(
        "<ul><li><b>Equal groups put together</b>: multiply. 6 bags of 4 apples is 6 × 4.</li>"
        "<li><b>A total split into equal groups</b>: divide. 24 apples in 6 bags is 24 ÷ 6.</li>"
        "<li><b>Times as many</b> compares: 3 times as many as 8 is 3 × 8 = 24. It is not 3 more.</li>"
        "<li>A <b>strip diagram</b> with equal parts shows a multiplication or division. Use ☐ for the unknown number in an equation.</li></ul>",
        [figure(strip_svg([("8", 1, FILL)] * 3, "?"), "3 equal parts of 8: 3 × 8 = 24."),
         example("Ana has 4 packs of 6 pencils. She gives away 5. How many pencils are left?", ["Step 1: 4 × 6 = 24", "Step 2: 24 − 5 = 19"], "19 pencils")],
        [["Adding when the problem has equal groups", "Look for words like each, every, rows of, packs of."],
         ["Reading 3 times as many as 3 more", "Times as many means multiply."],
         ["Stopping after the first step", "Ask: does my number answer the question?"]])
    faq = [("What does TEKS 3.4K ask?", "Solve one-step and two-step problems involving multiplication and division within 100 using strategies based on objects, pictorial models, properties and recall of facts."),
           ("What is a multiplicative comparison?", "A comparison such as 'Sam has 4 times as many cards as Lee'. TEKS 3.5C asks students to describe 4 × 9 as 4 times as many as 9."),
           ("How do strip diagrams help with multiplication?", "Equal parts of a strip show equal groups. If the whole is missing, multiply. If a part is missing, divide (TEKS 3.5B)."),
           ("How do I know whether to multiply or divide?", "If you know the number of groups and the size of each, multiply. If you know the total and need the groups or the size, divide.")]
    make("multiplication-and-division-word-problems", 8, "Algebraic Reasoning", "3.4K, 3.5B, 3.5C",
         "3.4K solve one-step and two-step problems involving multiplication and division within 100 using strategies based on objects; pictorial models, including arrays, area models, and equal groups; properties of operations; or recall of facts; 3.5B represent and solve one- and two-step multiplication and division problems within 100 using arrays, strip diagrams, and equations; 3.5C describe a multiplication expression as a comparison such as 3 x 24 represents 3 times as much as 24",
         "Multiplication and Division Word Problems: Strip Diagrams and Times as Many", "Multiplication and Division Word Problems",
         "Free Grade 3 word problem worksheets for Texas TEKS 3.4K, 3.5B and 3.5C: choose the equation, strip diagrams with equal parts, times as many comparisons, one-step and two-step problems within 100. 100 STAAR-style questions with answers.",
         "Equal groups put together: multiply. A total split into equal groups: divide.", "3 times as many as 8 is 3 × 8, not 8 + 3.",
         body, faq, sets, seo_title="Grade 3 Multiplication and Division Word Problems (TEKS 3.4K, 3.5B, STAAR)")


if __name__ == "__main__":
    build()
