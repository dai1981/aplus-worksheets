# -*- coding: utf-8 -*-
"""
Texas Grade 6 Math: Operations with Decimals (TEKS 6.3E)
  python3 tools/gen_ustx_math_g6_decimal_operations.py
Adding and subtracting, multiplying, dividing by whole numbers and by decimals, and multi-step word problems (the
US Grade 6 makers with Texas names).
Wrong answers come from real mistakes: lining up the last digits instead of the decimal points, counting decimal
places wrongly, and moving the decimal point in only one number.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import gen_us_math_g6_decimal_operations as dop
adopt(dop)
tx_common.GRADE = "grade-6"



def build():
    sets, R = build_sets([
        ("Add and subtract decimals", [("run", dop.set_add_sub, (dop.People,), 20)]),
        ("Multiply decimals", [("run", dop.set_multiply, (dop.People,), 20)]),
        ("Divide a decimal by a whole number", [("run", dop.set_div_whole, (dop.People,), 20)]),
        ("Divide by a decimal", [("run", dop.set_div_dec, (dop.People,), 20)]),
        ("Multi-step word problems", [("run", dop.set_words, (dop.People,), 20)]),
    ], 66006)
    finish(sets, R)
    body = lesson('<ul><li>Add and subtract: line up the <b>decimal points</b>. Write zeros to fill empty places.</li><li>Multiply: multiply as whole numbers, then count the decimal places in both factors.</li><li>Divide by a whole number: put the decimal point straight up into the quotient.</li><li>Divide by a decimal: move the decimal point in <b>both</b> numbers the same number of places to make the divisor a whole number.</li></ul>',
        [example("4.56 ÷ 0.12", ["Move both points 2 places", "456 ÷ 12"], "38"), example("2.35 × 1.4", ["235 × 14 = 3,290", "3 decimal places"], "3.29")],
        [['Lining up the last digits', 'Line up the decimal points.'], ['Counting decimal places wrongly', 'Add the decimal places of both factors.'], ['Moving the decimal point in only the divisor', 'Move it the same number of places in both numbers.']])
    faq = [('What does TEKS 6.3E ask?', 'Multiply and divide positive rational numbers fluently.'), ('Why move the decimal point in both numbers?', 'It multiplies both by the same power of 10, so the quotient does not change.'), ('How do I check a decimal answer?', 'Estimate: 4.56 ÷ 0.12 is about 4.8 ÷ 0.12 = 40.'), ('Do I need zeros at the end?', 'Write zeros to fill places when adding or dividing. They do not change the value.')]
    make('multiplying-and-dividing-decimals', 6, 'Number and Operations', '6.3E',
         '6.3E multiply and divide positive rational numbers fluently',
         'Operations with Decimals', 'Multiplying and Dividing Decimals',
         'Free Grade 6 decimal worksheets for Texas TEKS 6.3E: add, subtract, multiply and divide decimals, divide by a decimal, and multi-step word problems. 100 questions with answers.',
         'To divide by a decimal, move both decimal points the same number of places.', '4.56 ÷ 0.12 = 456 ÷ 12 = 38.',
         body, faq, sets, seo_title='Grade 6 Multiplying and Dividing Decimals Worksheets (TEKS 6.3E, STAAR)')


if __name__ == "__main__":
    build()
