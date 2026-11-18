# -*- coding: utf-8 -*-
"""
Texas Grade 4 Math: Multiplying 2-Digit by 2-Digit Numbers (TEKS 4.4C, 4.4D)
  python3 tools/gen_ustx_math_g4_multiply_two_by_two.py
Area models and the standard algorithm for 2-digit by 2-digit products (the US Grade 4 makers with Texas names),
perfect squares through 15 × 15, arrays and equations, and word problems.
Wrong answers come from real mistakes: multiplying only tens by tens and ones by ones, forgetting the zero in the
second partial product, and adding partial products wrongly.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import gen_us_math_g4_multiplication as usm
adopt(usm)
tx_common.GRADE = "grade-4"

def one_square(r):
    n = r.randint(11, 15) if r.random() < 0.7 else r.randint(2, 10)
    kind = r.choice(["val", "val", "which", "root"])
    if kind == "val":
        return mcq("What is %d × %d?" % (n, n), n * n, [n * 2, n * n - n, n * n + n, n * (n + 1) + 1], "%d × %d = <b>%d</b>. A number times itself is a perfect square." % (n, n, n * n))
    if kind == "root":
        return mcq("A square array has %d dots. How many dots are in each row?" % (n * n), n, [n * n // 2, n + 1, n - 1, n * 2], "%d × %d = %d, so each row has <b>%d</b>." % (n, n, n * n, n))
    sq = n * n
    others = [sq + 1, sq - 2, (n - 1) * (n + 1) if (n - 1) * (n + 1) != sq else sq + 3]
    return mcq("Which number is a perfect square?", sq, others, "<b>%d</b> = %d × %d." % (sq, n, n))


def one_eq(r):
    a, b = r.randint(11, 49), r.randint(11, 39)
    ta, oa, tb, ob = a // 10 * 10, a % 10, b // 10 * 10, b % 10
    if not oa or not ob:
        return None
    kind = r.choice(["parts", "expr"])
    if kind == "expr":
        right = "(%d × %d) + (%d × %d) + (%d × %d) + (%d × %d)" % (ta, tb, ta, ob, oa, tb, oa, ob)
        wrong = ["(%d × %d) + (%d × %d)" % (ta, tb, oa, ob), "(%d + %d) × (%d + %d) + %d" % (ta, oa, tb, ob, oa), "(%d × %d) + (%d × %d) + (%d × %d)" % (ta, tb, ta, ob, oa, ob)]
        return mcq("Which equation shows the four partial products of %d × %d?" % (a, b), right, wrong, "Split %d = %d + %d and %d = %d + %d. Multiply every part by every part: <b>%s</b> = %s." % (a, ta, oa, b, tb, ob, right, comma(a * b)))
    return mcq("%d × %d = %d + %d + %d + ☐. What is the missing partial product?" % (a, b, ta * tb, ta * ob, oa * tb), oa * ob, [oa + ob, oa * tb, ta * ob, oa * ob * 10],
               "The last partial product is the ones times the ones: %d × %d = <b>%d</b>." % (oa, ob, oa * ob))


def build():
    sets, R = build_sets([
        ("Area models: 2-digit × 2-digit", [("run", usm.set_area2, ("rnd", "seen"), 20)]),
        ("Partial products and equations", [("collect", one_eq, 20)]),
        ("Perfect squares through 15 × 15", [("collect", one_square, 20)]),
        ("Standard algorithm: 2-digit × 2-digit", [("run", usm.set_std2, ("rnd", "seen"), 20)]),
        ("Word problems and estimates", [("run", usm.set_story, ("rnd", usm.People), 20)]),
    ], 64007)
    finish(sets, R)
    body = lesson('<ul><li>Split both numbers into tens and ones. An <b>area model</b> has 4 parts: tens × tens, tens × ones, ones × tens and ones × ones.</li><li>Add the 4 <b>partial products</b>: 23 × 14 = 200 + 80 + 30 + 12 = 322.</li><li>In the <b>standard algorithm</b>, multiply by the ones, then by the tens (write a 0 first), then add.</li><li>A <b>perfect square</b> is a number times itself: 12 × 12 = 144.</li></ul>',
        [example("23 × 14 with an area model", ["20 × 10 = 200", "20 × 4 = 80", "3 × 10 = 30", "3 × 4 = 12", "200 + 80 + 30 + 12"], "322"), example("36 × 25 with the standard algorithm", ["36 × 5 = 180", "36 × 20 = 720", "180 + 720"], "900")],
        [['Multiplying only tens × tens and ones × ones: 23 × 14 = 200 + 12', 'There are 4 partial products. Do not skip the middle two.'], ['Forgetting the 0 when multiplying by the tens digit', 'The tens digit stands for tens: 36 × 20, not 36 × 2.'], ['Adding partial products wrongly', 'Line them up by place value before adding.']])
    faq = [('What does TEKS 4.4C ask?', 'Represent the product of two 2-digit numbers using arrays, area models or equations, including perfect squares through 15 by 15.'), ('What does TEKS 4.4D ask?', 'Use strategies and algorithms, including the standard algorithm, to multiply up to a four-digit number by a one-digit number and a two-digit number by a two-digit number.'), ('What are perfect squares?', 'Numbers made by multiplying a number by itself: 1, 4, 9, 16 … 144, 169, 196, 225.'), ('Why does the second row start with a 0?', 'You are multiplying by tens, so every product is a number of tens.')]
    make('multiplying-two-digit-numbers', 7, 'Number and Operations', '4.4C, 4.4D',
         '4.4C represent the product of 2 two-digit numbers using arrays, area models, or equations, including perfect squares through 15 by 15; 4.4D use strategies and algorithms, including the standard algorithm, to multiply up to a four-digit number by a one-digit number and to multiply a two-digit number by a two-digit number',
         'Multiplying 2-Digit by 2-Digit Numbers', 'Multiplying 2-Digit by 2-Digit Numbers',
         'Free Grade 4 multiplication worksheets for Texas TEKS 4.4C and 4.4D: 2-digit by 2-digit area models, partial products, perfect squares through 15 × 15, the standard algorithm and word problems. 100 questions with answers.',
         'Split both numbers and add the 4 partial products.', '23 × 14 = 200 + 80 + 30 + 12 = 322. In the standard algorithm, write a 0 before multiplying by the tens digit.',
         body, faq, sets, seo_title='Grade 4 Multiplying 2-Digit by 2-Digit Numbers Worksheets (TEKS 4.4C, 4.4D, STAAR)')


if __name__ == "__main__":
    build()
