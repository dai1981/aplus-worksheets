# -*- coding: utf-8 -*-
"""
Texas Grade 6 Math: One-Step Inequalities (TEKS 6.9A, 6.9B, 6.10A, 6.10B)
  python3 tools/gen_ustx_math_g6_inequalities.py
Reading and writing inequalities, solutions of an inequality, graphs on a number line, solving one-step
inequalities, and word problems (the US Grade 6 makers, plus an own solving maker).
Wrong answers come from real mistakes: using an open circle for ≥, shading the wrong way, and changing only one side
when solving.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import gen_us_math_g6_inequalities as iq
adopt(iq)
tx_common.GRADE = "grade-6"

SYM = {">": "&gt;", "<": "&lt;", "≥": "≥", "≤": "≤"}


def one_solve(r):
    v = r.choice("xnkpwy")
    s = r.choice([">", "<", "≥", "≤"])
    kind = r.choice(["add", "sub", "mul", "div"])
    a, x = r.randint(2, 15), r.randint(3, 40)
    if kind == "add":
        lhs, rhs = "%s + %d" % (v, a), x + a
        how = "Subtract %d from both sides" % a
        wrong = [x + 2 * a, x + a, x - a if x > a else x + 1]
    elif kind == "sub":
        lhs, rhs = "%s − %d" % (v, a), x - a
        if rhs <= 0:
            return None
        how = "Add %d to both sides" % a
        wrong = [x - 2 * a if x > 2 * a else x + 2 * a, x - a, x + 1]
    elif kind == "mul":
        lhs, rhs = "%d%s" % (a, v), a * x
        how = "Divide both sides by %d" % a
        wrong = [a * x * a, a * x - a, x + a]
    else:
        lhs, rhs = "%s ÷ %d" % (v, a), x
        x = a * x
        how = "Multiply both sides by %d" % a
        wrong = [rhs // a if rhs % a == 0 and rhs // a else rhs + a, rhs + a, rhs - a if rhs > a else rhs + 2 * a]
    right = "%s %s %s" % (v, SYM[s], comma(x))
    w = ["%s %s %s" % (v, SYM[s], comma(t)) for t in dict.fromkeys(wrong) if t != x and t > 0]
    flip = {">": "<", "<": ">", "≥": "≤", "≤": "≥"}[s]
    w.append("%s %s %s" % (v, SYM[flip], comma(x)))
    return mcq("Solve: %s %s %s" % (lhs, SYM[s], comma(rhs)), right, w[:3], "%s: <b>%s</b>." % (how, right))


def build():
    sets, R = build_sets([
        ("Read and write inequalities", [("run", iq.set_read, ("rnd",), 10), ("run", iq.set_words, ("rnd",), 10)]),
        ("Solutions of an inequality", [("run", iq.set_solutions, ("rnd",), 20)]),
        ("Graph inequalities on a number line", [("run", iq.set_graphs, ("rnd", iq.People), 20)]),
        ("Solve one-step inequalities", [("collect", one_solve, 20)]),
        ("Inequality word problems", [("run", iq.set_problems, ("rnd", iq.People), 20)]),
    ], 66020)
    finish(sets, R)
    body = lesson('<ul><li>An <b>inequality</b> compares two amounts with &lt;, &gt;, ≤ (at most) or ≥ (at least).</li><li>An inequality has many <b>solutions</b>: x &gt; 4 means any number greater than 4.</li><li>On a number line, use an <b>open circle</b> for &lt; and &gt;, and a <b>closed circle</b> for ≤ and ≥. Shade toward the solutions.</li><li>Solve a one-step inequality like an equation: use the inverse operation on both sides.</li></ul>',
        [example("x + 7 > 15", ["Subtract 7 from both sides"], "x > 8"), example("4n ≤ 36", ["Divide both sides by 4"], "n ≤ 9")],
        [['Using an open circle for ≥ or ≤', 'At least and at most include the number: closed circle.'], ['Shading the wrong way', 'x > 8 means numbers to the right of 8.'], ['Changing only one side', 'Do the same step to both sides.']])
    faq = [('What does TEKS 6.9B ask?', 'Represent solutions for one-variable, one-step equations and inequalities on number lines.'), ('What does at least mean?', 'Greater than or equal to: ≥.'), ('Is 8 a solution of x > 8?', 'No. 8 is not greater than 8. It would be a solution of x ≥ 8.'), ('How is solving an inequality like solving an equation?', 'You use inverse operations on both sides. In Grade 6 the numbers are positive, so the sign stays the same.')]
    make('one-step-inequalities', 20, 'Expressions, Equations and Relationships', '6.9A, 6.9B, 6.10A, 6.10B',
         '6.9A write one-variable, one-step equations and inequalities to represent constraints or conditions within problems; 6.9B represent solutions for one-variable, one-step equations and inequalities on number lines; 6.10A model and solve one-variable, one-step equations and inequalities that represent problems, including geometric concepts; 6.10B determine if the given value(s) make(s) one-variable, one-step equations or inequalities true',
         'One-Step Inequalities', 'One-Step Inequalities',
         'Free Grade 6 inequality worksheets for Texas TEKS 6.9 and 6.10: read and write inequalities, solutions, number line graphs, solve one-step inequalities and word problems. 100 questions with answers.',
         'Open circle for < and >; closed circle for ≤ and ≥.', 'x + 7 > 15, so x > 8. At least means ≥.',
         body, faq, sets, seo_title='Grade 6 One-Step Inequalities Worksheets (TEKS 6.9B, 6.10A, STAAR)')


if __name__ == "__main__":
    build()
