# -*- coding: utf-8 -*-
"""
Texas Grade 4 Math: Multi-Step Problems with Strip Diagrams and Equations (TEKS 4.5A)
  python3 tools/gen_ustx_math_g4_multi_step.py
Representing multi-step problems with the four operations using strip diagrams and equations with a letter for
the unknown, multi-step problems and times-as-many statements (the US Grade 4 comparison makers with Texas names),
and solving equations with a letter.
Wrong answers come from real mistakes: using the wrong operation for the second step, putting the unknown in the
wrong place in the strip diagram, and stopping after one step.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import gen_us_math_g4_comparison_problems as usc
from tx_common import strip_svg, FILL
adopt(usc)
tx_common.GRADE = "grade-4"

WHITE = "#ffffff"


def one_strip(r):
    k = Kid(r).next()
    kind = r.choice(["groups_plus", "total_minus", "times"])
    if kind == "groups_plus":
        g, n, e = r.randint(3, 6), r.randint(12, 45), r.randint(10, 60)
        pic = strip_svg([(str(n), 1, FILL)] * g + [(str(e), 1, FILL)], "t")
        return mcq(fig(pic) + "%s buys %d packs of %d cards. Then %s gets %d more cards. Which equation matches the strip diagram?" % (k["n"], g, n, k["he"], e),
                   "t = (%d × %d) + %d" % (g, n, e), ["t = %d + %d + %d" % (g, n, e), "t = %d × (%d + %d)" % (g, n, e), "t = (%d × %d) − %d" % (g, n, e)],
                   "%d equal parts of %d, plus %d: <b>t = (%d × %d) + %d</b> = %d." % (g, n, e, g, n, e, g * n + e))
    if kind == "total_minus":
        t, a, g = r.randint(300, 900), r.randint(40, 150), r.randint(3, 6)
        rest = t - a
        if rest % g:
            t += g - rest % g
            rest = t - a
        pic = strip_svg([(str(a), 1, FILL)] + [("p", 1, WHITE)] * g, str(t))
        return mcq(fig(pic) + "A school has %d tickets. It keeps %d and shares the rest equally among %d classes. Let p be the tickets for each class. Which equation matches?" % (t, a, g),
                   "p = (%d − %d) ÷ %d" % (t, a, g), ["p = %d − %d ÷ %d" % (t, a, g), "p = (%d + %d) ÷ %d" % (t, a, g), "p = %d × %d − %d" % (g, t, a)],
                   "Take away %d first, then share: <b>p = (%d − %d) ÷ %d</b> = %d." % (a, t, a, g, rest // g))
    n, m = r.randint(12, 60), r.randint(3, 6)
    pic = strip_svg([(str(n), 1, FILL)] * m, "b", compare=[(str(n), 1)])
    return mcq(fig(pic) + "A blue ribbon is %d times as long as a %d-inch red ribbon. Let b be the length of the blue ribbon. Which equation matches?" % (m, n),
               "b = %d × %d" % (m, n), ["b = %d + %d" % (m, n), "b = %d ÷ %d" % (n, m), "b = %d × %d + %d" % (m, n, n)],
               "%d equal parts of %d: <b>b = %d × %d</b> = %d inches." % (m, n, m, n, m * n))


def one_letter(r):
    kind = r.choice(["add", "sub", "mul", "div", "two"])
    if kind == "add":
        a, x = r.randint(120, 2400), r.randint(120, 2400)
        return mcq("Solve: n + %s = %s" % (comma(a), comma(a + x)), comma(x), [comma(2 * a + x), comma(x + 10), comma(a)], "n = %s − %s = <b>%s</b>." % (comma(a + x), comma(a), comma(x)))
    if kind == "sub":
        a, x = r.randint(120, 2400), r.randint(120, 2400)
        return mcq("Solve: n − %s = %s" % (comma(a), comma(x)), comma(a + x), [comma(abs(x - a)) if x != a else "0", comma(a + x + 100), comma(x)], "n = %s + %s = <b>%s</b>." % (comma(x), comma(a), comma(a + x)))
    if kind == "mul":
        a, x = r.randint(3, 9), r.randint(12, 120)
        return mcq("Solve: %d × n = %s" % (a, comma(a * x)), comma(x), [comma(a * x - a), comma(a * x * a), comma(x + 1)], "n = %s ÷ %d = <b>%s</b>." % (comma(a * x), a, comma(x)))
    if kind == "div":
        a, x = r.randint(3, 9), r.randint(12, 150)
        return mcq("Solve: n ÷ %d = %d" % (a, x), comma(a * x), [comma(x // a) if x >= a else comma(x + a), comma(x + a), comma(a * x + a)], "n = %d × %d = <b>%s</b>." % (x, a, comma(a * x)))
    a, b, x = r.randint(3, 8), r.randint(10, 90), r.randint(11, 60)
    return mcq("Solve: (%d × n) + %d = %s" % (a, b, comma(a * x + b)), x, [a * x, x + b, (a * x + b) // a], "Subtract %d: %d × n = %s. Divide by %d: n = <b>%d</b>." % (b, a, comma(a * x), a, x))


def build():
    sets, R = build_sets([
        ("Strip diagrams for multi-step problems", [("collect", one_strip, 20)]),
        ("Times as many: statements and equations", [("run", usc.set_statements, ("rnd", usc.People), 20)]),
        ("Equations with a letter", [("collect", one_letter, 20)]),
        ("Multi-step problems: equations, remainders and estimates", [("run", usc.set_multistep, ("rnd", usc.People), 20)]),
        ("Find the smaller amount", [("run", usc.set_smaller, ("rnd", usc.People), 20)]),
    ], 64012)
    finish(sets, R)
    body = lesson('<ul><li>A <b>strip diagram</b> shows how the numbers in a problem fit together: equal parts for multiplication and division, parts and a whole for addition and subtraction.</li><li>Write an <b>equation</b> with a letter for the unknown: t = (4 × 25) + 18.</li><li>Solve one step at a time. Use the order the story describes, and check that the answer makes sense.</li></ul>',
        [example("Ana buys 4 packs of 25 stickers and gets 18 more. How many stickers?", ["t = (4 × 25) + 18", "4 × 25 = 100", "100 + 18 = 118"], "118 stickers"), example("Solve (3 × n) + 12 = 57.", ["57 − 12 = 45", "45 ÷ 3 = 15"], "n = 15")],
        [['Using the wrong operation in step 2', 'Ask what the story does next: adds, takes away, shares or groups.'], ['Putting the unknown in the wrong place', 'The letter stands for the number the question asks for.'], ['Stopping after one step', 'Reread the question: does your number answer it?']])
    faq = [('What does TEKS 4.5A ask?', 'Represent multi-step problems involving the four operations with whole numbers using strip diagrams and equations with a letter standing for the unknown quantity.'), ('Why use a letter in an equation?', 'The letter stands for the unknown number, so the equation shows the whole problem before you solve it.'), ('How do strip diagrams help?', 'They show which amounts are equal parts, which are wholes and which is unknown, so you can choose the operations.'), ('How do I check a multi-step answer?', 'Put your answer back into the story or the equation, or estimate to see if it is reasonable.')]
    make('multi-step-problems-and-strip-diagrams', 12, 'Algebraic Reasoning', '4.5A',
         '4.5A represent multi-step problems involving the four operations with whole numbers using strip diagrams and equations with a letter standing for the unknown quantity',
         'Multi-Step Problems with Strip Diagrams and Equations', 'Multi-Step Problems and Strip Diagrams',
         'Free Grade 4 worksheets for Texas TEKS 4.5A: multi-step problems with strip diagrams, equations with a letter for the unknown, times as many and two-step word problems. 100 STAAR-style questions with answers.',
         'Draw a strip diagram, then write an equation with a letter for the unknown.', 't = (4 × 25) + 18 shows both steps. Solve one step at a time.',
         body, faq, sets, seo_title='Grade 4 Multi-Step Problems with Strip Diagrams and Equations (TEKS 4.5A, STAAR)')


if __name__ == "__main__":
    build()
