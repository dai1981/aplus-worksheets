# -*- coding: utf-8 -*-
"""
Texas Grade 3 Math: Adding and Subtracting within 1,000 (TEKS 3.4A, 3.5A)
  python3 tools/gen_ustx_math_g3_add_subtract.py
Adding and subtracting 3-digit numbers with and without regrouping (the question makers of the US Grade 3
add-subtract unit, with Texas names and new numbers), strip diagrams and number lines for one- and two-step
problems, and two-step word problems.
Wrong answers come from real mistakes: forgetting to regroup, subtracting the smaller digit from the larger in
each place, adding when the problem takes away, and stopping after the first step of a two-step problem.
"""
import random
from tx_common import (Kid, mcq, collect, finish, make, fig, figure, lesson, S, comma, run, adopt, strip_svg,
                       FILL, example)
import gen_us_math_g3_add_sub as us

adopt(us)
R = random.Random(60401)
WHITE = "#ffffff"


# ------------------------------------------------------------ set 4: strip diagrams
def one_strip(r):
    kind = r.choice(["part", "whole", "match", "match"])
    a, b = r.randint(105, 560), r.randint(105, 430)
    if a + b > 1000:
        return None
    if kind == "whole":
        pic = strip_svg([(str(a), a, FILL), (str(b), b, FILL)], "?")
        return mcq(fig(pic) + "What number does the ? stand for?", a + b, [a - b if a > b else b - a, a + b + 100, a + b - 10, a + b + 10],
                   "The ? is the whole. Add the parts: %d + %d = <b>%s</b>." % (a, b, comma(a + b)))
    if kind == "part":
        pic = strip_svg([(str(a), a, FILL), ("?", b, WHITE)], comma(a + b))
        return mcq(fig(pic) + "What number does the ? stand for?", b, [a + (a + b), a, b + 100, b - 10 if b > 110 else b + 10],
                   "The whole is %s and one part is %d. Subtract: %s − %d = <b>%d</b>." % (comma(a + b), a, comma(a + b), a, b))
    k = Kid(r).next()
    what = r.choice(["shells", "stickers", "baseball cards", "beads", "stamps"])
    w = a + b
    q = "%s has %s %s. %s gives away %d. How many %s are left? Which strip diagram matches?" % (k["n"], comma(w), what, k["He"], a, what)
    right = "Whole %s, one part %d, other part ?" % (comma(w), a)
    wrong = ["Whole ?, parts %s and %d" % (comma(w), a), "Whole %d, one part %s, other part ?" % (a, comma(w)), "Whole %s, parts %d and %s" % (comma(w), a, comma(w))]
    return mcq(q, right, wrong, "%s is the whole. %d is the part given away. The part left is unknown: <b>%s</b>. %s − %d = %d." % (comma(w), a, right, comma(w), a, b))


# ------------------------------------------------------------ set 5: two-step word problems
def one_two_step(r):
    k = Kid(r).next()
    kind = r.choice(["add_sub", "sub_sub", "add_add", "compare"])
    if kind == "add_sub":
        a, b, c = r.randint(150, 450), r.randint(120, 380), r.randint(60, 290)
        if a + b > 999 or c >= a + b:
            return None
        q = "A school library has %d books about animals and %d books about space. It lends out %d books. How many of these books are still in the library?" % (a, b, c)
        return mcq(q, a + b - c, [a + b, a + b + c, a - c + b - 10 if a - c + b - 10 > 0 else 7], "First add: %d + %d = %d. Then subtract: %d − %d = <b>%d</b>." % (a, b, a + b, a + b, c, a + b - c))
    if kind == "sub_sub":
        a = r.randint(600, 990)
        b, c = r.randint(110, 290), r.randint(110, 290)
        q = "A food bank in %s had %d cans. On Monday it gave away %d cans. On Tuesday it gave away %d cans. How many cans were left?" % (r.choice(["Austin", "Houston", "El Paso", "Waco"]), a, b, c)
        return mcq(q, a - b - c, [a - b, a - c, a - b + c], "%d − %d = %d. Then %d − %d = <b>%d</b>." % (a, b, a - b, a - b, c, a - b - c))
    if kind == "add_add":
        a, b, c = r.randint(110, 330), r.randint(110, 330), r.randint(110, 330)
        if a + b + c > 999:
            return None
        q = "%s's class collects bottle caps. They collect %d in March, %d in April and %d in May. How many caps is that in all?" % (k["n"], a, b, c)
        return mcq(q, a + b + c, [a + b, b + c, a + b + c + 100, a + b + c - 10], "%d + %d = %d. Then %d + %d = <b>%d</b>." % (a, b, a + b, a + b, c, a + b + c))
    a = r.randint(250, 520)
    d = r.randint(45, 180)
    if a + a + d > 999:
        return None
    q = "%s scores %d points in a game. %s brother scores %d more points than %s. How many points do they score together?" % (k["n"], a, k["His"], d, k["him"])
    return mcq(q, a + a + d, [a + d, a + a, a + a + d + 10, a + a - d], "Brother: %d + %d = %d. Together: %d + %d = <b>%d</b>." % (a, d, a + d, a, a + d, a + a + d))


def build():
    s_add = run(us.set_add1, "rnd", "seen", seed=61)["items"][:10] + run(us.set_add2, "rnd", "seen", seed=62)["items"][:10]
    s_sub = run(us.set_sub1, "rnd", "seen", seed=63)["items"][:10] + run(us.set_sub2, "rnd", "seen", seed=64)["items"][:10]
    sets = [S("Add 3-digit numbers", s_add),
            S("Subtract 3-digit numbers", s_sub),
            S("Missing numbers, estimates and word problems", run(us.set_story, "rnd", seed=65)["items"]),
            S("Strip diagrams", collect(one_strip, 20, R)),
            S("Two-step word problems", collect(one_two_step, 20, R))]
    finish(sets, R)
    body = lesson(
        "<ul><li>Line up the digits by place value. Add or subtract the ones, then the tens, then the hundreds.</li>"
        "<li><b>Regroup</b> when you need to: 10 ones make 1 ten, and 1 hundred can be broken into 10 tens.</li>"
        "<li>A <b>strip diagram</b> shows the parts and the whole. If the whole is missing, add. If a part is missing, subtract.</li>"
        "<li>For a two-step problem, find the first answer, then use it in the second step. Estimate to check.</li></ul>",
        [figure(strip_svg([("245", 245, FILL), ("?", 180, WHITE)], "612"), "Whole 612, one part 245. The missing part is 612 − 245 = 367."),
         example("Subtract 503 − 268.", ["You cannot take 8 from 3, and there are 0 tens.", "Break 1 hundred into 10 tens, then 1 ten into 10 ones: 4 hundreds, 9 tens, 13 ones.", "13 − 8 = 5, 9 − 6 = 3, 4 − 2 = 2."], "235")],
        [["Forgetting to regroup", "If the top digit is smaller, regroup from the next place first."],
         ["Taking the smaller digit from the larger one", "Always take the bottom digit from the top digit, regrouping if needed."],
         ["Stopping after one step", "Read the question again. Does your first answer answer it?"]])
    faq = [("What does TEKS 3.4A ask?", "Solve one-step and two-step addition and subtraction problems within 1,000 fluently, using place value, properties of operations and the relationship between addition and subtraction."),
           ("What is a strip diagram?", "A bar split into parts. The parts and the whole show how the numbers in a problem are related. Texas uses strip diagrams to represent problems (TEKS 3.5A)."),
           ("How do you subtract across zeros?", "Regroup from the hundreds: 503 is 4 hundreds, 9 tens and 13 ones. Then subtract each place."),
           ("How can I check a subtraction answer?", "Add the answer to the number you subtracted. You should get the number you started with.")]
    make("adding-and-subtracting-within-1000", 4, "Number and Operations", "3.4A, 3.5A",
         "3.4A solve with fluency one-step and two-step problems involving addition and subtraction within 1,000 using strategies based on place value, properties of operations, and the relationship between addition and subtraction; 3.5A represent one- and two-step problems involving addition and subtraction of whole numbers to 1,000 using pictorial models, number lines, and equations",
         "Adding and Subtracting within 1,000: Regrouping and Strip Diagrams", "Adding and Subtracting within 1,000",
         "Free Grade 3 addition and subtraction worksheets for Texas TEKS 3.4A and 3.5A: add and subtract 3-digit numbers with regrouping, missing numbers, strip diagrams and two-step word problems. 100 STAAR-style questions with answers.",
         "Line up the places. Regroup when a digit is too small.", "In a strip diagram, add to find the whole and subtract to find a missing part.",
         body, faq, sets, seo_title="Grade 3 Adding and Subtracting within 1,000 Worksheets (TEKS 3.4A, STAAR)")


if __name__ == "__main__":
    build()
