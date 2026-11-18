# -*- coding: utf-8 -*-
"""
Texas Grade 4 Math: Multiplying up to 4-Digit Numbers by 1-Digit Numbers (TEKS 4.4D)
  python3 tools/gen_ustx_math_g4_multiply_by_one_digit.py
Area models and the standard algorithm for 2-, 3- and 4-digit numbers times a 1-digit number (the US Grade 4
makers with Texas names), partial products in expanded form, and word problems.
Wrong answers come from real mistakes: forgetting a regrouped digit, multiplying only the ones, and writing a
partial product in the wrong place.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import gen_us_math_g4_multiplication as usm
adopt(usm)
tx_common.GRADE = "grade-4"

def one_partial(r):
    d = r.randint(3, 9)
    n = r.randint(1001, 9999)
    parts = [(int(c) * 10 ** (3 - i)) for i, c in enumerate(str(n))]
    if 0 in parts:
        return None
    kind = r.choice(["expr", "total"])
    if kind == "expr":
        right = " + ".join("(%d × %s)" % (d, comma(p)) for p in parts)
        wrong = [" + ".join("(%d × %d)" % (d, int(c)) for c in str(n)), "(%d × %s) + %s" % (d, comma(parts[0]), comma(sum(parts[1:]))), " + ".join("(%d × %s)" % (d + 1, comma(p)) for p in parts)]
        return mcq("Which expression is equal to %d × %s?" % (d, comma(n)), right, wrong, "Expand %s and multiply each part by %d: <b>%s</b>." % (comma(n), d, right))
    return mcq("%d × %s = %s. What is the full product?" % (d, comma(n), " + ".join(comma(d * p) for p in parts)), comma(d * n), [comma(d * n + 100), comma(d * n - 10), comma(sum(d * int(c) for c in str(n)))],
               "Add the partial products: <b>%s</b>." % comma(d * n))


def build():
    sets, R = build_sets([
        ("Area models: 2- and 3-digit × 1-digit", [("run", usm.set_area1, ("rnd", "seen"), 20)]),
        ("Partial products with 4-digit numbers", [("collect", one_partial, 20)]),
        ("Standard algorithm: 3- and 4-digit × 1-digit", [("run", usm.set_std1, ("rnd", "seen"), 20)]),
        ("More standard algorithm practice", [("run", usm.set_std1, ("rnd", "seen"), 20)]),
        ("Word problems", [("run", usm.set_story, ("rnd", usm.People), 20)]),
    ], 64008)
    finish(sets, R)
    body = lesson('<ul><li>Break the bigger number into place values: 3,427 = 3,000 + 400 + 20 + 7.</li><li>Multiply each part by the 1-digit number and add the <b>partial products</b>.</li><li>In the <b>standard algorithm</b>, multiply from the ones place. Regroup and add the regrouped digit to the next product.</li><li>Estimate first: 6 × 3,427 is about 6 × 3,000 = 18,000.</li></ul>',
        [example("6 × 3,427", ["6 × 3,000 = 18,000", "6 × 400 = 2,400", "6 × 20 = 120", "6 × 7 = 42", "18,000 + 2,400 + 120 + 42"], "20,562")],
        [['Forgetting a regrouped digit', 'Write it above the next place and add it after you multiply.'], ['Multiplying only some places', 'Every digit is multiplied by the 1-digit number.'], ['Lining up partial products wrongly', 'Line up by place value before adding.']])
    faq = [('What does TEKS 4.4D ask?', 'Use strategies and algorithms, including the standard algorithm, to multiply up to a four-digit number by a one-digit number.'), ('What are partial products?', 'The products of each place value part, such as 6 × 400 = 2,400. Their sum is the full product.'), ('How do I check my answer?', 'Estimate by rounding the bigger number. 6 × 3,427 should be close to 6 × 3,000 = 18,000.'), ('What if there is a zero in the number?', 'That place gives a partial product of 0, but keep the place in the standard algorithm.')]
    make('multiplying-by-one-digit-numbers', 8, 'Number and Operations', '4.4D',
         '4.4D use strategies and algorithms, including the standard algorithm, to multiply up to a four-digit number by a one-digit number and to multiply a two-digit number by a two-digit number',
         'Multiplying up to 4-Digit Numbers by 1-Digit Numbers', 'Multiplying by 1-Digit Numbers',
         'Free Grade 4 multiplication worksheets for Texas TEKS 4.4D: multiply 2-, 3- and 4-digit numbers by 1-digit numbers with area models, partial products and the standard algorithm, and word problems. 100 questions with answers.',
         'Multiply each place, then add the partial products.', 'In the standard algorithm, start with the ones and add each regrouped digit to the next product.',
         body, faq, sets, seo_title='Grade 4 Multiplying by 1-Digit Numbers Worksheets: up to 4 Digits (TEKS 4.4D, STAAR)')


if __name__ == "__main__":
    build()
