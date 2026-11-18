# -*- coding: utf-8 -*-
"""
Texas Grade 5 Math: Adding and Subtracting Decimals (TEKS 5.3K)
  python3 tools/gen_ustx_math_g5_add_subtract_decimals.py
Lining up decimal points, hundredths grids, adding with regrouping, subtracting with zeros, and money and
measurement word problems. The question makers come from the US Grade 5 decimal unit with Texas names.
Wrong answers come from real mistakes: lining up the last digits, forgetting to write a zero, and regrouping in
the wrong place.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import gen_us_math_g5_add_sub_decimals as usd
adopt(usd)
tx_common.GRADE = "grade-5"



def build():
    sets, R = build_sets([
        ("Line up the decimal points", [("run", usd.set_line_up, (usd.People, "rnd", "seen"), 20)]),
        ("Add and subtract with hundredths grids", [("run", usd.set_models, (usd.People,), 20)]),
        ("Add with regrouping", [("run", usd.set_regroup, (usd.People, "rnd", "seen"), 20)]),
        ("Subtract decimals and write zeros", [("run", usd.set_subtract, (usd.People, "rnd", "seen"), 20)]),
        ("Word problems and estimating", [("run", usd.set_words, (usd.People,), 20)]),
    ], 65009)
    finish(sets, R)
    body = lesson('<ul><li>Line up the <b>decimal points</b> so each place lines up: tenths with tenths, hundredths with hundredths.</li><li>Write zeros so both numbers have the same number of places: 5 = 5.00.</li><li>Add or subtract as with whole numbers, regrouping as needed, and bring the decimal point straight down.</li></ul>',
        [example("3.6 + 2.45", ["3.60 + 2.45"], "6.05"), example("5 − 2.37", ["5.00 − 2.37"], "2.63")],
        [['Lining up the last digits: 3.6 + 2.45 = 2.81', 'Line up the decimal points.'], ['Not writing zeros: 5 − 2.37', 'Write 5 as 5.00 first.'], ['Dropping the decimal point', 'Bring it straight down into the answer.']])
    faq = [('What does TEKS 5.3K ask?', 'Add and subtract positive rational numbers, including decimals, fluently.'), ('Why line up the decimal points?', 'So that digits with the same place value are added together.'), ('Can I write extra zeros?', 'Yes. 4.5 = 4.50 = 4.500. Zeros at the end of a decimal do not change its value.'), ('How do I check?', 'Estimate by rounding to whole numbers, or add the difference back.')]
    make('adding-and-subtracting-decimals', 9, 'Number and Operations', '5.3K',
         '5.3K add and subtract positive rational numbers fluently',
         'Adding and Subtracting Decimals', 'Adding and Subtracting Decimals',
         'Free Grade 5 decimal worksheets for Texas TEKS 5.3K: line up decimal points, hundredths grids, add with regrouping, subtract with zeros and money word problems. 100 questions with answers.',
         'Line up the decimal points.', 'Write zeros so both numbers have the same places: 5 − 2.37 = 5.00 − 2.37 = 2.63.',
         body, faq, sets, seo_title='Grade 5 Adding and Subtracting Decimals Worksheets (TEKS 5.3K, STAAR)')


if __name__ == "__main__":
    build()
