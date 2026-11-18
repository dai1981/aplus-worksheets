# -*- coding: utf-8 -*-
"""
Texas Grade 5 Math: Multi-Step Problems and Equations (TEKS 5.4B)
  python3 tools/gen_ustx_math_g5_multi_step_equations.py
Solving one-step equations with a letter for the unknown, finding the value of a letter in a multi-step
equation, choosing the equation that matches a story, and two-step and three-step word problems.
Wrong answers come from real mistakes: doing only one step, using the wrong operation, and doing the steps in
the wrong order.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)

tx_common.GRADE = "grade-5"

THINGS = [("stickers", "sheets", 8, 30), ("markers", "boxes", 8, 24), ("pencils", "boxes", 10, 24), ("muffins", "trays", 6, 12),
          ("juice boxes", "cases", 12, 32), ("baseball cards", "packs", 6, 15), ("crayons", "boxes", 16, 24), ("water bottles", "cases", 12, 36)]


def one_solve(r):
    v = r.choice("nmpkwy")
    kind = r.choice(["mul", "div", "add", "sub"])
    if kind == "mul":
        a, x = r.randint(3, 25), r.randint(6, 60)
        eq, w = "%d × %s = %s" % (a, v, comma(a * x)), [a * x + a, a * x - a, x + a]
    elif kind == "div":
        a, q = r.randint(3, 12), r.randint(8, 90)
        x = a * q
        eq, w = "%s ÷ %d = %d" % (v, a, q), [q + a, q - a, q]
    elif kind == "add":
        a, x = r.randint(120, 2400), r.randint(150, 3000)
        eq, w = "%s + %s = %s" % (v, comma(a), comma(a + x)), [a + x + a, x + 100, x - 10]
    else:
        a, x = r.randint(120, 2400), r.randint(2600, 6000)
        eq, w = "%s − %s = %s" % (v, comma(a), comma(x - a)), [x - a - a, x - 100, x + a]
    w = [comma(t) for t in w if t != x and t > 0]
    inv = {"mul": "divide by %d" % a if kind == "mul" else "", "div": "multiply by %d" % a, "add": "subtract %s" % comma(a), "sub": "add %s" % comma(a)}[kind]
    return mcq("Solve for %s: %s" % (v, eq), comma(x), w, "Use the inverse operation: %s. %s = <b>%s</b>." % (inv, v, comma(x)))


def one_eval(r):
    v = r.choice("nmpktw")
    kind = r.choice(["a", "b", "c", "d"])
    if kind == "a":
        a, b, c = r.randint(3, 9), r.randint(12, 48), r.randint(15, 99)
        ex, val, w = "%d × %d + %d" % (a, b, c), a * b + c, [a * (b + c), a + b + c, a * b]
    elif kind == "b":
        d, q, c = r.randint(3, 9), r.randint(12, 60), r.randint(10, 90)
        ex, val, w = "(%d − %d) ÷ %d" % (d * q + c, c, d), q, [(d * q + c) // d - c if (d * q + c) // d > c else q + c, d * q, q + 1]
    elif kind == "c":
        a, b, c = r.randint(120, 600), r.randint(20, 99), r.randint(3, 8)
        ex, val, w = "%d − %d × %d" % (a + b * c, b, c), a, [(a + b * c - b) * c, a + b, b * c]
    else:
        a, b, c = r.randint(4, 12), r.randint(25, 90), r.randint(25, 90)
        ex, val, w = "%d × (%d + %d)" % (a, b, c), a * (b + c), [a * b + c, a + b + c, a * b * c]
    w = [comma(t) for t in w if t != val and t > 0]
    return mcq("What is the value of %s?<br>%s = %s" % (v, v, ex), comma(val), w,
               "Work inside parentheses first, then multiply or divide, then add or subtract. %s = <b>%s</b>." % (v, comma(val)))


def one_match(r):
    k = Kid(r).next()
    thing, box, lo, hi = r.choice(THINGS)
    a, b = r.randint(3, 9), r.randint(lo, hi)
    kind = r.choice(["give", "more", "share"])
    v = thing[0]
    if kind == "give":
        c = r.randint(5, a * b - 5)
        q = "%s buys %d %s of %s. There are %d %s in each. %s gives away %d. Which equation shows %s, the number of %s %s has left?" % (k["n"], a, box, thing, b, thing, k["He"], c, v, thing, k["he"])
        right, w = "%d × %d − %d = %s" % (a, b, c, v), ["%d + %d − %d = %s" % (a, b, c, v), "%d × %d + %d = %s" % (a, b, c, v), "%d × %d − %d = %s" % (a, c, b, v)]
        ans = a * b - c
    elif kind == "more":
        c = r.randint(5, 40)
        q = "%s has %d %s of %s with %d in each. %s also has %d loose %s. Which equation shows %s, the total number of %s?" % (k["n"], a, box, thing, b, k["He"], c, thing, v, thing)
        right, w = "%d × %d + %d = %s" % (a, b, c, v), ["%d + %d + %d = %s" % (a, b, c, v), "%d × (%d + %d) = %s" % (a, b, c, v), "%d × %d − %d = %s" % (a, b, c, v)]
        ans = a * b + c
    else:
        n = r.randint(3, 6)
        c = r.randint(2, 30)
        tot = n * r.randint(5, 30) + c
        q = "%s has %d %s. %s keeps %d and shares the rest equally among %d friends. Which equation shows %s, the number each friend gets?" % (k["n"], tot, thing, k["He"], c, n, v)
        right, w = "(%d − %d) ÷ %d = %s" % (tot, c, n, v), ["%d − %d ÷ %d = %s" % (tot, c, n, v), "(%d + %d) ÷ %d = %s" % (tot, c, n, v), "(%d − %d) × %d = %s" % (tot, c, n, v)]
        ans = (tot - c) // n
    return mcq(q, right, w, "The equation is %s. %s = <b>%d</b>." % (right, v, ans))


def one_two(r):
    k = Kid(r).next()
    kind = r.choice(["save", "seats", "pack", "trip", "garden"])
    if kind == "save":
        w, n, s = r.randint(12, 45), r.randint(6, 15), r.randint(30, 150)
        t = w * n + s
        return mcq("%s already has $%d. %s saves $%d each week for %d weeks. How much money does %s have then?" % (k["n"], s, k["He"], w, n, k["he"]), "$%s" % comma(t), ["$%s" % comma(w * n), "$%s" % comma(w + n + s), "$%s" % comma(w * (n + s))],
                       "%d × $%d = $%s. $%s + $%d = <b>$%s</b>." % (n, w, comma(w * n), comma(w * n), s, comma(t)))
    if kind == "seats":
        rows, per, taken = r.randint(18, 40), r.randint(12, 30), r.randint(100, 300)
        return mcq("A theater in Austin has %d rows with %d seats in each row. %d seats are taken. How many seats are empty?" % (rows, per, taken), comma(rows * per - taken), [comma(rows * per), comma(rows + per + taken), comma(rows * per + taken)],
                   "%d × %d = %s seats. %s − %d = <b>%s</b>." % (rows, per, comma(rows * per), comma(rows * per), taken, comma(rows * per - taken)))
    if kind == "pack":
        thing, box, lo, hi = r.choice(THINGS)
        b = r.randint(lo, hi)
        n = r.randint(4, 9)
        f = r.choice([2, 3, 4])
        tot = n * b * f
        return mcq("A school gets %s %s. They come in %s of %d. The %s are split equally among %d classrooms. How many %s does each classroom get?" % (comma(tot), thing, box, b, box, f, box), "%d %s" % (n, box), ["%d %s" % (tot // f, box), "%d %s" % (n * b, box), "%d %s" % (tot // b, box)],
                   "%s ÷ %d = %d %s. %d ÷ %d = <b>%d %s</b>." % (comma(tot), b, tot // b, box, tot // b, f, n, box))
    if kind == "trip":
        a, b = r.randint(120, 340), r.randint(120, 340)
        d = r.randint(2, 4)
        tot = (a + b) * d
        return mcq("A family drives %d miles from Houston on Friday and %d miles on Saturday. They drive the same total each weekend for %d weekends. How many miles is that?" % (a, b, d), "%s miles" % comma(tot), ["%s miles" % comma(a + b), "%s miles" % comma(a + b * d), "%s miles" % comma(a * b)],
                   "%d + %d = %d miles. %d × %d = <b>%s miles</b>." % (a, b, a + b, a + b, d, comma(tot)))
    rows, per, dead = r.randint(6, 15), r.randint(8, 20), r.randint(3, 15)
    return mcq("%s plants %d rows of pepper plants with %d plants in each row. %d plants do not grow. How many plants grow?" % (k["n"], rows, per, dead), comma(rows * per - dead), [comma(rows * per), comma(rows * per + dead), comma(rows + per + dead)],
               "%d × %d = %d. %d − %d = <b>%d</b>." % (rows, per, rows * per, rows * per, dead, rows * per - dead))


def one_three(r):
    k = Kid(r).next()
    kind = r.choice(["shop", "fund", "bus", "pages"])
    if kind == "shop":
        a, pa, b, pb = r.randint(2, 6), r.randint(4, 15), r.randint(2, 5), r.randint(8, 25)
        pay = (a * pa + b * pb) // 10 * 10 + r.choice([10, 20])
        ch = pay - a * pa - b * pb
        return mcq("%s buys %d T-shirts for $%d each and %d caps for $%d each. %s pays with $%d. How much change does %s get?" % (k["n"], a, pa, b, pb, k["He"], pay, k["he"]), "$%d" % ch, ["$%d" % (a * pa + b * pb), "$%d" % (pay - pa - pb) if pay - pa - pb != ch else "$%d" % (ch + 5), "$%d" % (ch + pb)],
                   "%d × $%d = $%d. %d × $%d = $%d. $%d + $%d = $%d. $%d − $%d = <b>$%d</b>." % (a, pa, a * pa, b, pb, b * pb, a * pa, b * pb, a * pa + b * pb, pay, a * pa + b * pb, ch))
    if kind == "fund":
        n, p, c, g = r.randint(80, 250), r.randint(2, 5), r.randint(60, 200), r.randint(3, 6)
        net = n * p - c
        if net % g:
            return None
        return mcq("The fifth grade sells %d tickets for $%d each. They pay $%d for supplies. The rest is split equally among %d clubs. How much does each club get?" % (n, p, c, g), "$%s" % comma(net // g), ["$%s" % comma(n * p // g), "$%s" % comma(net), "$%s" % comma((n * p + c) // g)],
                   "%d × $%d = $%s. $%s − $%d = $%s. $%s ÷ %d = <b>$%s</b>." % (n, p, comma(n * p), comma(n * p), c, comma(net), comma(net), g, comma(net // g)))
    if kind == "bus":
        cls, per, ad, cap = r.randint(4, 8), r.randint(20, 28), r.randint(8, 20), r.choice([44, 48, 52])
        tot = cls * per + ad
        b = -(-tot // cap)
        return mcq("%d classes of %d students go on a field trip to San Antonio with %d adults. Each bus holds %d people. How many buses are needed?" % (cls, per, ad, cap), str(b), [str(tot // cap), str(b + 1), str(-(-cls * per // cap)) if -(-cls * per // cap) != b else str(b + 2)],
                   "%d × %d = %d students. %d + %d = %d people. %d ÷ %d = %d R%d, so they need <b>%d buses</b>." % (cls, per, cls * per, cls * per, ad, tot, tot, cap, tot // cap, tot % cap, b))
    pg, d1, n1, d2 = r.randint(240, 480), r.randint(3, 6), r.randint(15, 30), r.randint(2, 5)
    left = pg - d1 * n1
    if left <= 0 or left % d2:
        return None
    return mcq("%s's book has %d pages. %s reads %d pages a day for %d days. %s wants to finish the rest in %d days. How many pages a day must %s read?" % (k["n"], pg, k["He"], n1, d1, k["He"], d2, k["he"]), str(left // d2), [str(left), str(pg // d2), str((pg - n1) // d2)],
               "%d × %d = %d. %d − %d = %d pages left. %d ÷ %d = <b>%d pages a day</b>." % (d1, n1, d1 * n1, pg, d1 * n1, left, left, d2, left // d2))


def build():
    sets, R = build_sets([
        ("Solve one-step equations", [("collect", one_solve, 20)]),
        ("Find the value of the letter", [("collect", one_eval, 20)]),
        ("Which equation matches the story?", [("collect", one_match, 20)]),
        ("Two-step word problems", [("collect", one_two, 20)]),
        ("Multi-step word problems", [("collect", one_three, 20)]),
    ], 65013)
    finish(sets, R)
    body = lesson('<ul><li>A <b>letter</b> such as n stands for the unknown number.</li><li>To solve, use the <b>inverse operation</b>: if 6 × n = 84, then n = 84 ÷ 6 = 14.</li><li>For a story, find the steps first, then write one equation: 4 × 12 − 15 = s.</li><li>Do the work in parentheses first, then × and ÷, then + and −. Check that the answer makes sense.</li></ul>',
        [example("6 × n = 84", ["n = 84 ÷ 6"], "n = 14"), example("Ava buys 4 packs of 12 stickers and gives away 15. Find s.", ["4 × 12 − 15 = s", "48 − 15"], "s = 33")],
        [['Doing only one step', 'Read the question again. What does it ask for at the end?'], ['Using the same operation instead of the inverse', 'For n − 250 = 600, add: n = 850.'], ['Doing steps in the wrong order', 'Multiply or divide before you add or subtract, unless there are parentheses.']])
    faq = [('What does TEKS 5.4B ask?', 'Represent and solve multi-step problems involving the four operations with whole numbers using equations with a letter standing for the unknown quantity.'), ('Which letter should I use?', 'Any letter works. Many people use the first letter of the thing, like s for stickers.'), ('How do I check my answer?', 'Put the number back into the equation and see if both sides are equal.'), ('What are the four operations?', 'Addition, subtraction, multiplication and division.')]
    make('multi-step-problems-and-equations', 13, 'Algebraic Reasoning', '5.4B',
         '5.4B represent and solve multi-step problems involving the four operations with whole numbers using equations with a letter standing for the unknown quantity',
         'Multi-Step Problems and Equations', 'Multi-Step Problems and Equations',
         'Free Grade 5 worksheets for Texas TEKS 5.4B: solve equations with a letter for the unknown, find the value of a letter, match equations to stories and solve multi-step word problems. 100 questions with answers.',
         'Write one equation with a letter for the unknown, then solve.', '4 × 12 − 15 = s, so s = 33. 6 × n = 84, so n = 14.',
         body, faq, sets, seo_title='Grade 5 Multi-Step Word Problems and Equations Worksheets (TEKS 5.4B, STAAR)')


if __name__ == "__main__":
    build()
