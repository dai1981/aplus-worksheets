# -*- coding: utf-8 -*-
"""
Texas Grade 6 Math: Multiplying and Dividing Integers (TEKS 6.3D)
  python3 tools/gen_ustx_math_g6_multiply_divide_integers.py
Sign rules for multiplying, dividing integers, many factors and powers, mixed practice, and word problems (the US
makers with a new seed, plus own mixed practice).
Wrong answers come from real mistakes: using the addition sign rules, getting the sign wrong with two negatives,
and dividing the wrong way.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_g7_multiply_divide_integers as mdi
adopt(mdi)
mdi.R = random.Random(66004)
from ws_common import num, par
tx_common.GRADE = "grade-6"

def one_mixed(r):
    a, b = r.randint(2, 12), r.randint(2, 12)
    sa, sb = r.choice([1, -1]), r.choice([1, -1])
    if sa == sb == 1:
        sa = -1
    if r.random() < 0.5:
        x, y = sa * a, sb * b
        v = x * y
        return mcq("Find %s × %s." % (num(x), par(y)), num(v), [num(-v), num(x + y), num(-(a + b)) if -(a + b) != v else num(a + b)],
                   "%d × %d = %d. %s, so the product is <b>%s</b>." % (a, b, a * b, "The signs are the same" if sa == sb else "The signs are different", num(v)))
    x, y = sa * a * b, sb * b
    v = x // y
    return mcq("Find %s ÷ %s." % (num(x), par(y)), num(v), [num(-v), num(x - y) if x - y != v else num(x + y), num(-y)],
               "%d ÷ %d = %d. %s, so the quotient is <b>%s</b>." % (a * b, b, a, "The signs are the same" if sa == sb else "The signs are different", num(v)))


def build():
    sets, R = build_sets([
        ("Multiply integers: the sign rules", [("run", mdi.set_multiply, (), 20)]),
        ("Divide integers", [("run", mdi.set_divide, (), 20)]),
        ("Mixed practice", [("collect", one_mixed, 20)]),
        ("Many factors and mixed operations", [("run", mdi.set_many, (), 20)]),
        ("Word problems", [("run", mdi.set_words, (), 20)]),
    ], 66004)
    finish(sets, R)
    body = lesson('<ul><li>Multiply or divide the absolute values first.</li><li><b>Same signs</b> give a <b>positive</b> answer: (−4)(−3) = 12.</li><li><b>Different signs</b> give a <b>negative</b> answer: −20 ÷ 5 = −4.</li><li>With many factors, count the negative signs: an even number gives a positive product.</li></ul>',
        [example("(−6)(4)", ["6 × 4 = 24", "Different signs"], "−24"), example("−42 ÷ (−7)", ["42 ÷ 7 = 6", "Same signs"], "6")],
        [['Using the addition rules: (−4)(−3) = −12', 'For × and ÷, same signs give a positive answer.'], ['Forgetting a sign with three factors', 'Count the negatives: odd means negative.'], ['Dividing the wrong way', '−24 ÷ 6 means 24 split into 6 groups: −4.']])
    faq = [('What does TEKS 6.3D ask?', 'Add, subtract, multiply and divide integers fluently.'), ('Why is a negative times a negative positive?', 'Multiplying by −1 flips a number to its opposite. Flipping twice brings it back to positive.'), ('Is the rule the same for division?', 'Yes. Same signs give a positive quotient; different signs give a negative quotient.'), ('What is (−2)³?', '(−2)(−2)(−2) = −8.')]
    make('multiplying-and-dividing-integers', 4, 'Number and Operations', '6.3D',
         '6.3D add, subtract, multiply, and divide integers fluently',
         'Multiplying and Dividing Integers', 'Multiplying and Dividing Integers',
         'Free Grade 6 worksheets for Texas TEKS 6.3D: multiply and divide integers with the sign rules, many factors, mixed practice and word problems. 100 questions with answers.',
         'Same signs: positive. Different signs: negative.', '(−6)(4) = −24. −42 ÷ (−7) = 6.',
         body, faq, sets, seo_title='Grade 6 Multiplying and Dividing Integers Worksheets (TEKS 6.3D, STAAR)')


if __name__ == "__main__":
    build()
