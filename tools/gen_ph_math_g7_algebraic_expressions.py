# -*- coding: utf-8 -*-
"""
Philippines Grade 7 Math (MATATAG): Algebraic Expressions: Variables, Constants, Translating and Evaluating (Grade 7: Number and Algebra)
  python3 tools/gen_ph_math_g7_algebraic_expressions.py
Variables, constants and coefficients (own maker), algebraic notation, translating verbal phrases into expressions,
writing expressions for situations, and evaluating expressions with positive and negative values (UK Year 7 makers).
Wrong answers come from real mistakes: reading 3x as 3 + x, writing "5 less than n" as 5 − n, and squaring a
negative value without parentheses.
"""
import ph_common
from ph_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, peso, words)
import random
import gen_uk_maths_y7_algebraic_notation_and_substitution as uka
adopt(uka)
if hasattr(uka, 'R'): uka.R = random.Random(707250)
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


def term(c, v):
    if c == 1:
        return v
    if c == -1:
        return "−" + v
    return ("−%d" % -c if c < 0 else "%d" % c) + v


def expr(parts):
    out = parts[0]
    for p in parts[1:]:
        out += " − " + p[1:] if p.startswith("−") else " + " + p
    return out


def one_vc(r):
    vs = r.sample(["x", "y", "a", "b", "n", "m"], 2)
    a, b, k = r.choice([2, 3, 4, 5, 7, 9, -2, -3, -6]), r.choice([1, 2, 6, 8, -1, -4]), r.choice([3, 5, 8, 10, 12, -7, -9])
    parts = [term(a, vs[0]), term(b, vs[1]), ("−%d" % -k) if k < 0 else str(k)]
    r.shuffle(parts)
    e = expr(parts)
    kind = r.choice(["const", "vars", "coef"])
    if kind == "const":
        right = ("−%d" % -k) if k < 0 else str(k)
        return mcq("In <b>%s</b>, what is the constant term?" % e, right, [str(abs(a)), vs[0], term(b, vs[1]), str(-k).replace("-", "−")],
                   "A constant has no variable, so its value never changes. The constant is <b>%s</b>." % right)
    if kind == "vars":
        right = "%s and %s" % tuple(sorted(vs))
        return mcq("Which are the variables in <b>%s</b>?" % e, right, ["%s and %s" % (abs(a), abs(k)), "%s only" % vs[0], "%s, %s and %d" % (vs[0], vs[1], abs(k))],
                   "Variables are letters that stand for numbers that can change: <b>%s</b>." % right)
    right = ("−%d" % -a) if a < 0 else str(a)
    return mcq("In <b>%s</b>, what is the numerical coefficient of %s?" % (e, vs[0]), right, [str(-a).replace("-", "−"), str(k).replace("-", "−"), vs[0]],
               "The coefficient is the number multiplied by the variable: <b>%s</b>." % right)


def build():
    sets, R = build_sets([
        ("Variables, constants and coefficients", [("collect", uniq(one_vc), 20)]),
        ("Algebraic notation", [("collect", uka.one_notation, 20)]),
        ("Translate verbal phrases", [("collect", uka.one_words, 20)]),
        ("Expressions for situations", [("collect", uka.one_context, 8), ("collect", uka.one_words, 12)]),
        ("Evaluate expressions", [("collect", uka.one_sub, 10), ("collect", uka.one_sub_neg, 10)]),
    ], 70725)
    finish(sets, R)
    body = lesson('<ul><li>A <b>variable</b> is a letter that stands for a number that can change. A <b>constant</b> is a number whose value does not change.</li><li>In 4x − 7, 4 is the <b>coefficient</b> of x and −7 is the constant term.</li><li>Translate words carefully: “5 less than n” is n − 5; “twice a number increased by 3” is 2n + 3.</li><li>To <b>evaluate</b>, replace each variable with its value in parentheses, then follow GEMDAS: if x = −3, then x² = (−3)² = 9.</li></ul>',
        [example("3a − 2b when a = 4, b = −1", ["3(4) − 2(−1)", "12 + 2"], "14")],
        [['3x as 3 + x', '3x means 3 × x.'], ['“5 less than n” as 5 − n', 'It is n − 5.'], ['−3² for x²', 'Use (−3)² = 9.']])
    faq = [('What does MATATAG Math 7 ask about expressions?', 'Distinguish a variable from a constant, evaluate algebraic expressions given the values of the variables, and translate verbal phrases into algebraic expressions.'), ('Is π a variable?', 'No. It is a constant, about 3.14.'), ('What is a term?', 'A part of an expression separated by + or −.'), ('How do I write “the sum of a and b, squared”?', '(a + b)².')]
    make('algebraic-expressions', 25, 'Number and Algebra', 'Grade 7: Number and Algebra',
         'Distinguish a variable from a constant in an algebraic expression; evaluate algebraic expressions given the value/s of the variable/s; translate verbal phrases into algebraic expressions.',
         'Algebraic Expressions: Variables, Constants, Translating and Evaluating', 'Algebraic Expressions',
         'Free Grade 7 algebraic expressions worksheets for the DepEd MATATAG curriculum: variables and constants, translating verbal phrases, writing and evaluating expressions. 100 questions with answers.',
         'Variable: a letter that can change. Constant: a fixed number.', 'Substitute with parentheses, then use GEMDAS.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
