# -*- coding: utf-8 -*-
"""
Texas Grade 6 Math: Dividing Fractions and Mixed Numbers (TEKS 6.2E, 6.3A, 6.3B, 6.3E)
  python3 tools/gen_ustx_math_g6_dividing_fractions.py
How many groups with fraction bars, reciprocals, increase or decrease when multiplying by a fraction, dividing
fractions and mixed numbers, and word problems (the US Grade 6 makers with Texas names, plus own makers).
Wrong answers come from real mistakes: flipping the first fraction, dividing tops and bottoms, and thinking that
multiplying always makes a number bigger.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import gen_us_math_g6_divide_fractions as dfm
adopt(dfm)
from fractions import Fraction as F
tx_common.GRADE = "grade-6"

def show(v):
    v = F(v)
    if v.denominator == 1:
        return str(v.numerator)
    w, n = divmod(v.numerator, v.denominator)
    return (str(w) if w else "") + fr(n, v.denominator)


def one_incdec(r):
    n = r.randint(12, 90)
    a, b = r.choice([(1, 2), (2, 3), (3, 4), (5, 6), (3, 8), (4, 3), (3, 2), (5, 4), (7, 5), (9, 8), (5, 5)])
    if a == b:
        if r.random() < 0.7:
            return None
    k = F(a, b)
    q = "%d is multiplied by %s. Is the product greater than, less than or equal to %d?" % (n, fr(a, b) if a != b else fr(a, b), n)
    right = "Greater than %d" % n if k > 1 else "Less than %d" % n if k < 1 else "Equal to %d" % n
    why = "%s is %s 1, so the product is <b>%s</b> %d." % (fr(a, b), "greater than" if k > 1 else "less than" if k < 1 else "equal to", right.split(" %d" % n)[0].lower(), n)
    return mcq(q, right, ["Greater than %d" % n, "Less than %d" % n, "Equal to %d" % n, "It depends on %d" % n], why)


def one_fdiv(r):
    a, b = r.randint(1, 30), r.randint(2, 12)
    if a % b == 0 or F(a, b).denominator != b:
        return None
    return mcq("Which fraction is equal to %d ÷ %d?" % (a, b), fr(a, b), [fr(b, a), fr(a, a * b) if a * b < 100 else fr(1, b), show(F(a, b) + 1)],
               "A fraction is a division: %d ÷ %d = %s%s." % (a, b, fr(a, b), "" if a < b else " = " + show(F(a, b))))


def build():
    sets, R = build_sets([
        ("How many groups? Fraction bars", [("run", dfm.set_groups, (), 20)]),
        ("Fractions as division and increase or decrease", [("collect", one_fdiv, 10), ("collect", one_incdec, 10)]),
        ("Reciprocals and the divide rule", [("run", dfm.set_rule, (), 20)]),
        ("Divide fractions and mixed numbers", [("run", dfm.set_compute, (), 10), ("run", dfm.set_mixed, (), 10)]),
        ("Word problems", [("run", dfm.set_words, (dfm.People,), 20)]),
    ], 66005)
    finish(sets, R)
    body = lesson("<ul><li>A fraction is a division: <span class='fr'><span class='fn'>3</span><span class='fd'>4</span></span> = 3 ÷ 4.</li><li>To divide by a fraction, <b>multiply by its reciprocal</b>: 2/3 ÷ 4/5 = 2/3 × 5/4.</li><li>Change mixed numbers to improper fractions first.</li><li>Multiplying by a fraction less than 1 makes a positive number smaller; by a fraction greater than 1 makes it bigger.</li></ul>",
        [example("3/4 ÷ 1/8", ["3/4 × 8/1", "24/4"], "6"), example("2 1/2 ÷ 3/4", ["5/2 × 4/3", "20/6"], "3 1/3")],
        [['Flipping the first fraction', 'Keep the first fraction; flip only the divisor.'], ['Dividing tops and bottoms without matching', 'Multiply by the reciprocal instead.'], ['Thinking multiplying always makes it bigger', '12 × 3/4 = 9, which is less than 12.']])
    faq = [('What does TEKS 6.3A ask?', 'Recognize that dividing by a rational number and multiplying by its reciprocal result in equivalent values.'), ('What does TEKS 6.3B ask?', 'Determine, with and without computation, whether a quantity is increased or decreased when multiplied by a fraction, including values greater than or less than one.'), ('What does TEKS 6.2E ask?', 'Extend representations for division to include fraction notation such as a/b represents the same number as a ÷ b where b ≠ 0.'), ('Why does flipping work?', 'Dividing by 1/8 asks how many eighths fit. There are 8 in each whole, so multiply by 8.')]
    make('dividing-fractions', 5, 'Number and Operations', '6.2E, 6.3A, 6.3B, 6.3E',
         '6.2E extend representations for division to include fraction notation such as a/b represents the same number as a ÷ b where b ≠ 0; 6.3A recognize that dividing by a rational number and multiplying by its reciprocal result in equivalent values; 6.3B determine, with and without computation, whether a quantity is increased or decreased when multiplied by a fraction, including values greater than or less than one; 6.3E multiply and divide positive rational numbers fluently',
         'Dividing Fractions and Mixed Numbers', 'Dividing Fractions',
         'Free Grade 6 worksheets for Texas TEKS 6.2E, 6.3A, 6.3B and 6.3E: fraction bars, reciprocals, increase or decrease, dividing fractions and mixed numbers, and word problems. 100 questions with answers.',
         'To divide by a fraction, multiply by its reciprocal.', '3/4 ÷ 1/8 = 3/4 × 8 = 6. Change mixed numbers to improper fractions first.',
         body, faq, sets, seo_title='Grade 6 Dividing Fractions Worksheets: Reciprocals and Mixed Numbers (TEKS 6.3A, 6.3E, STAAR)')


if __name__ == "__main__":
    build()
