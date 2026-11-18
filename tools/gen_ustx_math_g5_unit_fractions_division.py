# -*- coding: utf-8 -*-
"""
Texas Grade 5 Math: Dividing Whole Numbers and Unit Fractions (TEKS 5.3J, 5.3L)
  python3 tools/gen_ustx_math_g5_unit_fractions_division.py
Sharing a unit fraction into equal parts, how many unit fractions are in a whole number, computing and checking
with multiplication, reasoning about the size of quotients, and word problems. The question makers come from the
US Grade 5 fraction division unit with Texas names.
Wrong answers come from real mistakes: dividing the denominator instead of multiplying, mixing up 6 ÷ 1/2 and
1/2 ÷ 6, and expecting division to make a smaller number.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import gen_us_math_g5_divide_fractions as usd
adopt(usd)
tx_common.GRADE = "grade-5"



def build():
    sets, R = build_sets([
        ("Share a unit fraction into equal parts", [("run", usd.set_uw_models, (), 20)]),
        ("How many unit fractions are in a whole number?", [("run", usd.set_wu_models, (), 20)]),
        ("Compute and check with multiplication", [("run", usd.set_compute, (), 20)]),
        ("Compare, explain and find mistakes", [("run", usd.set_reason, (usd.People,), 20)]),
        ("Word problems", [("run", usd.set_words, (usd.People,), 20)]),
    ], 65011)
    finish(sets, R)
    body = lesson('<ul><li><b>Unit fraction ÷ whole number</b>: share the piece into equal parts. 1/3 ÷ 4 = 1/12, because 4 × 1/12 = 1/3.</li><li><b>Whole number ÷ unit fraction</b>: count how many pieces fit. 5 ÷ 1/4 = 20, because each whole has 4 fourths.</li><li>Check with multiplication.</li></ul>',
        [example("1/2 ÷ 3", ["Cut 1/2 into 3 equal parts.", "Each part is 1/6 of the whole."], "1/6"), example("4 ÷ 1/3", ["Each whole has 3 thirds.", "4 × 3 = 12"], "12")],
        [['Mixing up 6 ÷ 1/2 and 1/2 ÷ 6', '6 ÷ 1/2 asks how many halves are in 6 (12). 1/2 ÷ 6 shares a half into 6 parts (1/12).'], ['Thinking division always makes a number smaller', 'Dividing by a unit fraction makes a bigger number.'], ['Dividing the denominator: 1/3 ÷ 4 = 1/(3 ÷ 4)', 'Sharing into 4 parts makes the denominator 4 times as big: 1/12.']])
    faq = [('What does TEKS 5.3J ask?', 'Represent division of a unit fraction by a whole number and of a whole number by a unit fraction, such as 1/3 ÷ 7 and 7 ÷ 1/3, using objects and pictorial models, including area models.'), ('What does TEKS 5.3L ask?', 'Divide whole numbers by unit fractions and unit fractions by whole numbers.'), ('Why is 3 ÷ 1/4 bigger than 3?', 'It asks how many fourths are in 3. There are 4 fourths in each whole, so 12.'), ('How do I check?', 'Multiply the answer by the divisor. 1/12 × 4 = 1/3.')]
    make('dividing-with-unit-fractions', 11, 'Number and Operations', '5.3J, 5.3L',
         '5.3J represent division of a unit fraction by a whole number and the division of a whole number by a unit fraction such as 1/3 ÷ 7 and 7 ÷ 1/3 using objects and pictorial models, including area models; 5.3L divide whole numbers by unit fractions and unit fractions by whole numbers',
         'Dividing Whole Numbers and Unit Fractions', 'Dividing with Unit Fractions',
         'Free Grade 5 worksheets for Texas TEKS 5.3J and 5.3L: divide a unit fraction by a whole number and a whole number by a unit fraction with models, compute, check and word problems. 100 questions with answers.',
         'Whole ÷ unit fraction: count the pieces. Unit fraction ÷ whole: share the piece.', '5 ÷ 1/4 = 20 and 1/4 ÷ 5 = 1/20. Check with multiplication.',
         body, faq, sets, seo_title='Grade 5 Dividing with Unit Fractions Worksheets (TEKS 5.3J, 5.3L, STAAR)')


if __name__ == "__main__":
    build()
