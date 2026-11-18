# -*- coding: utf-8 -*-
"""
Texas Grade 6 Math: Comparing and Ordering Rational Numbers (TEKS 6.2C, 6.2D)
  python3 tools/gen_ustx_math_g6_compare_order_rational.py
Fractions and decimals on a number line, comparing and ordering integers and rational numbers, absolute value
versus order, and word problems (the US Grade 6 makers with Texas names).
Wrong answers come from real mistakes: thinking −7 is greater than −3, ordering by absolute value, and reading the
number line from the wrong side of zero.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import gen_us_math_g6_negative_numbers as nn
import gen_us_math_g6_absolute_value as av
adopt(nn)
adopt(av)
tx_common.GRADE = "grade-6"



def build():
    sets, R = build_sets([
        ("Fractions and decimals on the number line", [("run", nn.set_fractions, ("rnd", nn.People), 20)]),
        ("Compare numbers on a number line", [("run", av.set_compare, ("rnd", av.People), 20)]),
        ("Order rational numbers", [("run", av.set_order, ("rnd", av.People), 20)]),
        ("Absolute value and order", [("run", av.set_vs, ("rnd", av.People), 20)]),
        ("Word problems", [("run", av.set_words, ("rnd", av.People), 20)]),
    ], 66002)
    finish(sets, R)
    body = lesson('<ul><li>On a number line, numbers <b>increase to the right</b>. The number farther right is greater.</li><li>Every positive number is greater than every negative number.</li><li>For two negative numbers, the one closer to 0 is greater: −3 &gt; −7.</li><li>To order fractions and decimals, write them in the same form, then place them on a number line.</li></ul>',
        [example("Order −2.5, 1/2, −3, 0 from least to greatest.", ["−3 is farthest left", "then −2.5, then 0", "1/2 is right of 0"], "−3, −2.5, 0, 1/2")],
        [['Thinking −7 > −3 because 7 > 3', '−7 is farther left, so −7 < −3.'], ['Ordering by absolute value', '|−8| is large, but −8 is less than 2.'], ['Comparing −1/2 and −0.4 without converting', '−1/2 = −0.5, which is less than −0.4.']])
    faq = [('What does TEKS 6.2C ask?', 'Locate, compare and order integers and rational numbers using a number line.'), ('What does TEKS 6.2D ask?', 'Order a set of rational numbers arising from mathematical and real-world contexts.'), ('Is −0.5 greater than −0.25?', 'No. −0.5 is farther from 0 on the left, so −0.5 < −0.25.'), ('How do I compare a fraction and a decimal?', 'Change the fraction to a decimal (or the decimal to a fraction) and compare.')]
    make('comparing-and-ordering-rational-numbers', 2, 'Number and Operations', '6.2C, 6.2D',
         '6.2C locate, compare, and order integers and rational numbers using a number line; 6.2D order a set of rational numbers arising from mathematical and real-world contexts',
         'Comparing and Ordering Rational Numbers', 'Comparing and Ordering Rational Numbers',
         'Free Grade 6 worksheets for Texas TEKS 6.2C and 6.2D: compare and order integers, fractions and decimals on a number line, absolute value and order, and word problems. 100 questions with answers.',
         'Numbers increase to the right on a number line.', '−3 > −7 because −3 is closer to 0. Write fractions and decimals in the same form to order them.',
         body, faq, sets, seo_title='Grade 6 Comparing and Ordering Rational Numbers Worksheets (TEKS 6.2C, 6.2D, STAAR)')


if __name__ == "__main__":
    build()
