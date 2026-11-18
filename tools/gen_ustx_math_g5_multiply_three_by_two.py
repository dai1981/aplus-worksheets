# -*- coding: utf-8 -*-
"""
Texas Grade 5 Math: Multiplying 3-Digit by 2-Digit Numbers (TEKS 5.3B)
  python3 tools/gen_ustx_math_g5_multiply_three_by_two.py
2-digit by 2-digit warm-up, 3-digit by 2-digit with the standard algorithm, partial products, larger numbers with
zeros, and word problems (the US Grade 5 multiplication makers with Texas names).
Wrong answers come from real mistakes: forgetting the 0 in the second partial product, adding the regrouped digit
twice, and lining up partial products wrongly.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import gen_us_math_g5_multiplication as usm
adopt(usm)
tx_common.GRADE = "grade-5"

def one_partial(r):
    a, b = r.randint(102, 989), r.randint(12, 98)
    t, o = b // 10 * 10, b % 10
    if not o:
        return None
    kind = r.choice(["first", "second", "sum"])
    if kind == "first":
        return mcq("In the standard algorithm for %d × %d, what is the first partial product (%d × %d)?" % (a, b, a, o), comma(a * o), [comma(a * t), comma(a * (b // 10)), comma(a * o + a)],
                   "Multiply by the ones digit first: %d × %d = <b>%s</b>." % (a, o, comma(a * o)))
    if kind == "second":
        return mcq("In the standard algorithm for %d × %d, what is the second partial product (%d × %d)?" % (a, b, a, t), comma(a * t), [comma(a * (b // 10)), comma(a * o), comma(a * t * 10)],
                   "The tens digit means %d tens: %d × %d = <b>%s</b>. Write a 0 in the ones place first." % (b // 10, a, t, comma(a * t)))
    return mcq("%d × %d = %s + %s. What is the product?" % (a, b, comma(a * o), comma(a * t)), comma(a * b), [comma(a * o + a * (b // 10)), comma(a * b + 100), comma(a * b - 10)],
               "Add the partial products: <b>%s</b>." % comma(a * b))


def build():
    sets, R = build_sets([
        ("Warm-up: 2-digit × 2-digit", [("run", usm.set_warm, ("rnd", "seen"), 20)]),
        ("Partial products", [("collect", one_partial, 20)]),
        ("3-digit × 2-digit with the standard algorithm", [("run", usm.set_3x2, ("rnd", "seen"), 20)]),
        ("Larger numbers and zeros", [("run", usm.set_4x2, ("rnd", "seen"), 20)]),
        ("Word problems and estimates", [("run", usm.set_story, ("rnd", usm.People), 20)]),
    ], 65004)
    finish(sets, R)
    body = lesson('<ul><li>In the <b>standard algorithm</b>, multiply the top number by the ones digit, then by the tens digit (write a 0 first), then add the two partial products.</li><li>Regroup carefully in each row, and cross out regrouped digits before the next row.</li><li>Estimate first to check: 467 × 32 is about 500 × 30 = 15,000.</li></ul>',
        [example("467 × 32", ["467 × 2 = 934", "467 × 30 = 14,010", "934 + 14,010"], "14,944")],
        [['Forgetting the 0 in the second row', 'The tens digit stands for tens: 467 × 30, not 467 × 3.'], ['Adding a regrouped digit twice', 'Use each regrouped digit once, then cross it out.'], ['Lining up the partial products wrongly', 'Line up by place value before adding.']])
    faq = [('What does TEKS 5.3B ask?', 'Multiply with fluency a three-digit number by a two-digit number using the standard algorithm.'), ('Why do we write a 0 in the second row?', 'We are multiplying by tens, so every product is a multiple of 10.'), ('How can I check my product?', 'Estimate by rounding, or multiply in a different order.'), ('What are partial products?', 'The products from each digit of the 2-digit number, such as 467 × 2 and 467 × 30.')]
    make('multiplying-three-digit-by-two-digit-numbers', 4, 'Number and Operations', '5.3B',
         '5.3B multiply with fluency a three-digit number by a two-digit number using the standard algorithm',
         'Multiplying 3-Digit by 2-Digit Numbers', 'Multiplying 3-Digit by 2-Digit Numbers',
         'Free Grade 5 multiplication worksheets for Texas TEKS 5.3B: 3-digit by 2-digit multiplication with the standard algorithm, partial products, numbers with zeros and word problems. 100 questions with answers.',
         'Multiply by the ones, then by the tens (write a 0), then add.', '467 × 32 = 934 + 14,010 = 14,944. Estimate to check.',
         body, faq, sets, seo_title='Grade 5 Multiplying 3-Digit by 2-Digit Numbers Worksheets (TEKS 5.3B, STAAR)')


if __name__ == "__main__":
    build()
