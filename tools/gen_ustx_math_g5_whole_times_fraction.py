# -*- coding: utf-8 -*-
"""
Texas Grade 5 Math: Multiplying Whole Numbers and Fractions (TEKS 5.3I)
  python3 tools/gen_ustx_math_g5_whole_times_fraction.py
A fraction of a whole number with counters and bar models (the US Grade 5 maker), whole number times a
fraction, repeated addition, comparing the product with the whole number, and word problems.
Wrong answers come from real mistakes: multiplying the bottom number too, adding instead of multiplying, and
dividing by the top number.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import gen_us_math_g5_multiply_fractions as mf
import gen_us_math_g5_scaling as sc
adopt(mf)
adopt(sc)
from fractions import Fraction as F
tx_common.GRADE = "grade-5"

def show(v):
    v = F(v)
    if v.denominator == 1:
        return str(v.numerator)
    w, n = divmod(v.numerator, v.denominator)
    return (str(w) if w else "") + fr(n, v.denominator)


def one_compute(r):
    b = r.choice([3, 4, 5, 6, 8, 10, 12])
    a = r.randint(1, b - 1)
    n = r.randint(2, 12)
    if F(a, b).denominator != b:
        return None
    v = F(n * a, b)
    w = [show(F(n * a, n * b)), show(F(a, b * n)), show(F(n + a, b)), show(F(n * a, 1)), show(v + 1)]
    w = [x for x in dict.fromkeys(w) if x != show(v)]
    return mcq("%d × %s = ?" % (n, fr(a, b)), show(v), w[:3],
               "Multiply the whole number by the top number: %d × %d = %d. Keep the bottom number: %s = <b>%s</b>." % (n, a, n * a, fr(n * a, b), show(v)))


def one_repeat(r):
    b = r.choice([3, 4, 5, 6, 8])
    a = r.randint(1, b - 1)
    n = r.randint(3, 6)
    if F(a, b).denominator != b:
        return None
    v = F(n * a, b)
    q = "Which multiplication matches %s?" % " + ".join([fr(a, b)] * n)
    return mcq(q, "%d × %s = %s" % (n, fr(a, b), show(v)), ["%d × %s = %s" % (n, fr(a, b), fr(n * a, n * b)), "%d + %s = %s" % (n, fr(a, b), show(n + F(a, b))), "%d × %s = %s" % (n, fr(a, b), show(v + F(a, b)))],
               "%d groups of %s is %d × %s. %d × %d = %d, so the product is %s = <b>%s</b>." % (n, fr(a, b), n, fr(a, b), n, a, n * a, fr(n * a, b), show(v)))


def one_story(r):
    k = Kid(r).next()
    b = r.choice([2, 3, 4, 8])
    a = r.randint(1, b - 1)
    if F(a, b).denominator != b:
        return None
    kind = r.choice(["run", "flour", "ribbon", "juice", "class"])
    if kind == "class":
        n = b * r.randint(4, 8)
        v = F(n * a, b)
        return mcq("There are %d students in %s's class. %s of them ride the bus. How many students ride the bus?" % (n, k["n"], fr(a, b)), "%d students" % v, ["%d students" % (n // b), "%d students" % (n - v), "%d students" % (n * a)],
                   "%s of %d = %d × %d ÷ %d = <b>%d students</b>." % (fr(a, b), n, n, a, b, v))
    n = r.randint(3, 9)
    v = F(n * a, b)
    unit, act = {"run": ("mile", "runs %s mile every day for %d days. How far does %s run in all?"),
                 "flour": ("cup", "uses %s cup of flour for each batch of tortillas. %s makes %d batches. How much flour does %s use?"),
                 "ribbon": ("yard", "uses %s yard of ribbon for each gift. %s wraps %d gifts. How much ribbon does %s use?"),
                 "juice": ("liter", "drinks %s liter of juice each day for %d days. How much juice is that?")}[kind]
    if kind == "run":
        t = act % (fr(a, b), n, k["he"])
    elif kind == "juice":
        t = act % (fr(a, b), n)
    else:
        t = act % (fr(a, b), k["He"], n, k["he"])
    u = unit if v <= 1 else unit + "s"
    def q(x):
        return "%s %s" % (show(x), unit if F(x) <= 1 else unit + "s")
    return mcq("%s %s" % (k["n"], t), q(v), [q(F(n + a, b)), q(F(a, b * n)), q(v + 1)],
               "%d × %s = %s = <b>%s %s</b>." % (n, fr(a, b), fr(n * a, b), show(v), u))


def build():
    sets, R = build_sets([
        ("Fraction of a whole number", [("run", mf.set_of, ("rnd",), 20)]),
        ("Repeated addition and multiplication", [("collect", one_repeat, 20)]),
        ("Whole number times a fraction", [("collect", one_compute, 20)]),
        ("Is the product bigger or smaller?", [("run", sc.set_compare_one, ("rnd",), 20)]),
        ("Word problems", [("collect", one_story, 20)]),
    ], 65010)
    finish(sets, R)
    body = lesson("<ul><li>3 × <span class='fr'><span class='fn'>2</span><span class='fd'>5</span></span> means 3 groups of 2/5: 2/5 + 2/5 + 2/5 = 6/5.</li><li>Multiply the whole number by the top number and <b>keep the bottom number</b>.</li><li>A fraction of a number: 2/3 of 12 means split 12 into 3 equal groups and take 2 of them: 8.</li><li>Multiplying by a fraction less than 1 gives a product smaller than the whole number.</li></ul>",
        [example("4 × 3/8", ["4 × 3 = 12", "12/8", "Simplify"], "1 1/2"), example("2/3 of 12", ["12 ÷ 3 = 4", "4 × 2"], "8")],
        [['Multiplying the bottom number too: 3 × 2/5 = 6/15', 'The bottom number tells the size of the parts. It does not change.'], ['Adding: 3 × 2/5 = 3 2/5', 'Multiply 3 by the top number.'], ['Thinking the product is always bigger', '2/3 × 12 = 8, which is less than 12.']])
    faq = [('What does TEKS 5.3I ask?', 'Represent and solve for products of a fraction and a whole number using objects and pictorial models, including area models.'), ('How do you multiply a whole number by a fraction?', 'Multiply the whole number by the numerator and keep the denominator. Then simplify.'), ('Is 5 × 3/4 the same as 3/4 of 5?', 'Yes. Multiplication can be done in any order. Both equal 15/4 = 3 3/4.'), ('Why is 1/2 × 10 less than 10?', 'You are taking half of 10, which is 5.')]
    make('multiplying-whole-numbers-and-fractions', 10, 'Number and Operations', '5.3I',
         '5.3I represent and solve for products of a fraction and a whole number using objects and pictorial models, including area models',
         'Multiplying Whole Numbers and Fractions', 'Multiplying Whole Numbers and Fractions',
         'Free Grade 5 worksheets for Texas TEKS 5.3I: multiply whole numbers and fractions with counters and bar models, repeated addition, comparing products and word problems. 100 questions with answers.',
         'Multiply the whole number by the top number; keep the bottom number.', '4 × 3/8 = 12/8 = 1 1/2. 2/3 of 12 = 8.',
         body, faq, sets, seo_title='Grade 5 Multiplying Whole Numbers and Fractions Worksheets (TEKS 5.3I, STAAR)')


if __name__ == "__main__":
    build()
