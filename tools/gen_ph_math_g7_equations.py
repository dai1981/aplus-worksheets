# -*- coding: utf-8 -*-
"""
Philippines Grade 7 Math (MATATAG): Equations: Bar Models, Properties of Equality and Solving for an Unknown (Grade 7: Number and Algebra)
  python3 tools/gen_ph_math_g7_equations.py
Solving equations with bar (tape) models (US Grade 6 maker), the properties of equality (own maker), solving one-
and two-step equations (UK Year 7 maker), and writing equations for situations and word problems (BC Grade 7
makers with Filipino names).
Wrong answers come from real mistakes: doing an operation to one side only, undoing the steps in the wrong order,
and writing the equation backward.
"""
import ph_common
from ph_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, peso, words)
import random
import gen_us_math_g6_one_step_equations as uos
adopt(uos)
if hasattr(uos, 'R'): uos.R = random.Random(707260)
import gen_uk_maths_y7_solving_equations as uks
adopt(uks)
if hasattr(uks, 'R'): uks.R = random.Random(707261)
import gen_cabc_math_g7_two_step_equations as cbe
adopt(cbe)
if hasattr(cbe, 'R'): cbe.R = random.Random(707262)
ph_common.GRADE = "grade-7"

def uniq(fn):
    """Never give the same question twice, even with other wrong answers."""
    seen = set()
    def f(r):
        it = fn(r)
        if it is None or it["q"] in seen:
            raise AssertionError("repeat")
        seen.add(it["q"])
        return it
    f.__name__ = fn.__name__
    return f


PROPS = ["Addition property of equality", "Subtraction property of equality", "Multiplication property of equality", "Division property of equality",
         "Reflexive property", "Symmetric property", "Transitive property", "Substitution property"]


def one_peq(r):
    a, b = r.randint(2, 15), r.randint(2, 40)
    x = r.choice(["x", "y", "n", "m"])
    kind = r.randrange(8)
    if kind == 0:
        s, t, p = "%s − %d = %d" % (x, a, b), "%s = %d" % (x, a + b), PROPS[0]
        how = "add %d to both sides" % a
    elif kind == 1:
        s, t, p = "%s + %d = %d" % (x, a, a + b), "%s = %d" % (x, b), PROPS[1]
        how = "subtract %d from both sides" % a
    elif kind == 2:
        s, t, p = "%s ÷ %d = %d" % (x, a, b), "%s = %d" % (x, a * b), PROPS[2]
        how = "multiply both sides by %d" % a
    elif kind == 3:
        s, t, p = "%d%s = %d" % (a, x, a * b), "%s = %d" % (x, b), PROPS[3]
        how = "divide both sides by %d" % a
    elif kind == 4:
        return mcq("Which property says <b>%d%s + %d = %d%s + %d</b>?" % (a, x, b, a, x, b), PROPS[4], [PROPS[5], PROPS[6], PROPS[0]],
                   "Anything is equal to itself: <b>reflexive property</b>.")
    elif kind == 5:
        return mcq("If <b>%d = 3%s + %d</b>, then <b>3%s + %d = %d</b>. Which property is this?" % (b + 20, x, b, x, b, b + 20), PROPS[5], [PROPS[4], PROPS[6], PROPS[7]],
                   "If a = b, then b = a: <b>symmetric property</b>.")
    elif kind == 6:
        return mcq("If <b>a = %d</b> and <b>%d = b</b>, then <b>a = b</b>. Which property is this?" % (b, b), PROPS[6], [PROPS[5], PROPS[4], PROPS[7]],
                   "If a = b and b = c, then a = c: <b>transitive property</b>.")
    else:
        return mcq("If <b>%s = %d</b> and <b>y = 2%s + 1</b>, then <b>y = 2(%d) + 1</b>. Which property is this?" % (x, a, x, a) if x != "y" else "If <b>n = %d</b> and <b>y = 2n + 1</b>, then <b>y = 2(%d) + 1</b>. Which property is this?" % (a, a),
                   PROPS[7], [PROPS[6], PROPS[2], PROPS[5]], "A quantity may be replaced by its equal value: <b>substitution property</b>.")
    if r.random() < 0.5:
        others = [q for q in PROPS[:4] if q != p]
        return mcq("To solve <b>%s</b>, you %s to get <b>%s</b>. Which property of equality is this?" % (s, how, t), p, others, "You %s, so it is the <b>%s</b>." % (how, p.lower()))
    step = {0: "Add %d to both sides" % a, 1: "Subtract %d from both sides" % a, 2: "Multiply both sides by %d" % a, 3: "Divide both sides by %d" % a}[kind]
    wrong = ["Add %d to both sides" % a, "Subtract %d from both sides" % a, "Multiply both sides by %d" % a, "Divide both sides by %d" % a]
    return mcq("Which step solves <b>%s</b> in one move?" % s, step, [w for w in wrong if w != step], "%s: <b>%s</b>. Doing the same to both sides keeps the equation balanced." % (step, t))


def build():
    sets, R = build_sets([
        ("Bar models", [("run", uos.set_models, ("rnd", uos.People), 20)]),
        ("Properties of equality", [("collect", uniq(one_peq), 20)]),
        ("Solve equations", [("collect", uks.one_step, 20)]),
        ("Write equations", [("run", cbe.set_write, (cbe.People,), 20)]),
        ("Equation word problems", [("run", cbe.set_words, (cbe.People,), 20)]),
    ], 70726)
    finish(sets, R)
    body = lesson('<ul><li>An <b>equation</b> says two expressions are equal, like a balanced scale.</li><li><b>Properties of equality</b>: you may add, subtract, multiply or divide both sides by the same number (not 0 for division) and the equation stays true.</li><li>To solve, undo the operations in reverse order: 3x + 5 = 20 → subtract 5 → 3x = 15 → divide by 3 → x = 5.</li><li>A bar model helps: a bar of 20 split into three equal x parts and 5.</li></ul>',
        [example("2n − 7 = 15", ["add 7: 2n = 22", "divide by 2"], "n = 11")],
        [['One side only', 'Do the same to both sides.'], ['Wrong order', 'Undo + and − first, then × and ÷.'], ['Equation backward', 'Check by putting the answer back in.']])
    faq = [('What does MATATAG Math 7 ask about equations?', 'Solve simple equations represented by bar models, illustrate the properties of equality, write equations in algebraic form, and find the value of an unknown where the unknown is non-negative.'), ('What is the symmetric property?', 'If a = b, then b = a.'), ('How do I check my answer?', 'Substitute it into the original equation.'), ('Can I divide both sides by 0?', 'No.')]
    make('properties-of-equality-and-solving-equations', 26, 'Number and Algebra', 'Grade 7: Number and Algebra',
         'Solve simple equations represented by bar models to find unknowns; illustrate the properties of equality; write equations in algebraic form; find the value of an unknown in an equation where the unknown is non-negative.',
         'Equations: Bar Models, Properties of Equality and Solving for an Unknown', 'Solving Equations',
         'Free Grade 7 equations worksheets for the DepEd MATATAG curriculum: bar models, properties of equality, solving equations, writing equations and word problems. 100 questions with answers.',
         'Do the same to both sides.', 'Undo the operations in reverse order.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
