# -*- coding: utf-8 -*-
"""
Texas Grade 6 Math: Writing and Evaluating Expressions; Expressions vs. Equations (TEKS 6.7B)
  python3 tools/gen_ustx_math_g6_expressions.py
Writing expressions from words, the parts of an expression, expression or equation, evaluating expressions, and
word problems (the US Grade 6 makers with Texas names, plus an own expression-or-equation maker).
Wrong answers come from real mistakes: writing 3 less than n as 3 − n, mixing up terms and factors, and calling an
expression an equation.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import gen_us_math_g6_expressions as xp
adopt(xp)
tx_common.GRADE = "grade-6"

def one_exeq(r):
    v = r.choice("nxyaktm")
    a, b, c = r.randint(2, 12), r.randint(1, 30), r.randint(10, 90)
    exprs = ["%d%s + %d" % (a, v, b), "%s − %d" % (v, b), "%d(%s + %d)" % (a, v, b), "%s ÷ %d" % (v, a), "%d + %d × %d" % (b, a, a + 1)]
    eqs = ["%d%s + %d = %d" % (a, v, b, c), "%s − %d = %d" % (v, b, c), "%s = %d" % (v, c), "%d × %d = %d" % (a, a + 1, a * (a + 1)), "%s ÷ %d = %d" % (v, a, b)]
    if r.random() < 0.5:
        right = r.choice(eqs)
        return mcq("Which of these is an <b>equation</b>?", right, r.sample(exprs, 3), "An equation has an equal sign that shows two amounts are equal: <b>%s</b>." % right)
    right = r.choice(exprs)
    return mcq("Which of these is an <b>expression</b>, not an equation?", right, r.sample(eqs, 3), "An expression has no equal sign: <b>%s</b>." % right)


def build():
    sets, R = build_sets([
        ("Write expressions from words", [("run", xp.set_words, ("rnd", xp.People), 20)]),
        ("Parts of an expression", [("run", xp.set_parts, ("rnd", xp.People), 20)]),
        ("Expression or equation?", [("collect", one_exeq, 20)]),
        ("Evaluate expressions", [("run", xp.set_eval, ("rnd", xp.People), 20)]),
        ("Word problems: write and evaluate", [("run", xp.set_problems, ("rnd", xp.People), 20)]),
    ], 66014)
    finish(sets, R)
    body = lesson('<ul><li>An <b>expression</b> is a math phrase with numbers, variables and operations, but <b>no equal sign</b>: 3n + 5.</li><li>An <b>equation</b> says two expressions are equal: 3n + 5 = 20.</li><li><b>Terms</b> are separated by + or −. A <b>coefficient</b> multiplies a variable; a <b>constant</b> stands alone.</li><li>To evaluate, substitute the value and follow the order of operations.</li></ul>',
        [example("Write: 4 less than twice a number n", ["twice n = 2n", "4 less than: subtract 4"], "2n − 4"), example("Evaluate 3n + 5 when n = 6", ["3 × 6 = 18", "18 + 5"], "23")],
        [['Writing 3 less than n as 3 − n', 'Less than reverses the order: n − 3.'], ['Calling 3n + 5 an equation', 'No equal sign means it is an expression.'], ['Evaluating 3n as 36 when n = 6', '3n means 3 × n = 18.']])
    faq = [('What does TEKS 6.7B ask?', 'Distinguish between expressions and equations verbally, numerically and algebraically.'), ('Can an equation have no variable?', 'Yes. 4 × 5 = 20 is an equation because it has an equal sign.'), ('What is a coefficient?', 'The number multiplied by a variable, like 7 in 7y.'), ('Do I use the order of operations when evaluating?', 'Yes. Substitute first, then follow the order of operations.')]
    make('expressions-and-equations', 14, 'Expressions, Equations and Relationships', '6.7B',
         '6.7B distinguish between expressions and equations verbally, numerically, and algebraically',
         'Writing and Evaluating Expressions; Expressions vs. Equations', 'Expressions and Equations',
         'Free Grade 6 worksheets for Texas TEKS 6.7B: write expressions from words, parts of an expression, expression or equation, evaluate expressions, and word problems. 100 questions with answers.',
         'An expression has no equal sign; an equation does.', '3n + 5 is an expression. 3n + 5 = 20 is an equation.',
         body, faq, sets, seo_title='Grade 6 Expressions and Equations Worksheets: Write and Evaluate (TEKS 6.7B, STAAR)')


if __name__ == "__main__":
    build()
