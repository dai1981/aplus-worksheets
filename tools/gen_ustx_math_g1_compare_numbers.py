# -*- coding: utf-8 -*-
"""
Texas Grade 1 Math: Comparing and Ordering Numbers to 120 (TEKS 1.2D, 1.2E, 1.2F, 1.2G)
  python3 tools/gen_ustx_math_g1_compare_numbers.py
Comparing tens first, then ones, the symbols >, < and =, greatest, least and in order, comparing with blocks, and
word problems (the US Grade 1 makers with Texas names).
Wrong answers come from real mistakes: comparing the ones first, turning the symbol the wrong way, and reading 52 as 25.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import gen_us_math_g1_compare as cm
adopt(cm)
tx_common.GRADE = "grade-1"



def build():
    sets, R = build_sets([
        ("Compare with tens and ones blocks", [("run", cm.set_blocks, ("rnd", "seen"), 20)]),
        ("Compare the tens first, then the ones", [("run", cm.set_places, ("rnd", "seen"), 20)]),
        ("Use the symbols >, < and =", [("run", cm.set_symbols, ("rnd", "seen"), 20)]),
        ("Greatest, least and in order", [("run", cm.set_order, ("rnd", "seen"), 20)]),
        ("Word problems", [("run", cm.set_words, ("rnd", "seen", cm.People), 20)]),
    ], 69102)
    finish(sets, R)
    body = lesson('<ul><li>Compare the <b>tens</b> first. More tens means a greater number.</li><li>If the tens are the same, compare the <b>ones</b>.</li><li>&gt; means greater than, &lt; means less than, = means equal to. The open side faces the greater number.</li><li>To order numbers, find the least, then the next, and so on.</li></ul>',
        [example("Compare 43 and 61", ["4 tens &lt; 6 tens"], "43 &lt; 61")],
        [['Comparing the ones first', 'Look at the tens first.'], ['Turning the symbol the wrong way', 'The open side faces the greater number.'], ['Reading 52 as 25', 'Say the tens digit first.']])
    faq = [('What does TEKS 1.2E ask?', 'Use place value to compare whole numbers up to 120 using comparative language.'), ('What does TEKS 1.2G ask?', 'Represent the comparison of two numbers to 100 using the symbols &gt;, &lt;, or =.'), ('What does TEKS 1.2F ask?', 'Order whole numbers up to 120 using place value and open number lines.'), ('What does TEKS 1.2D ask?', 'Generate a number that is greater than or less than a given whole number up to 120.')]
    make('comparing-and-ordering-numbers', 2, 'Number and Operations', '1.2D, 1.2E, 1.2F, 1.2G',
         '1.2D generate a number that is greater than or less than a given whole number up to 120; 1.2E use place value to compare whole numbers up to 120 using comparative language; 1.2F order whole numbers up to 120 using place value and open number lines; 1.2G represent the comparison of two numbers to 100 using the symbols >, <, or =',
         'Comparing and Ordering Numbers to 120', 'Comparing and Ordering Numbers',
         'Free Grade 1 worksheets for Texas TEKS 1.2D–1.2G: compare numbers to 120 with blocks and place value, use >, < and =, and order numbers. 100 questions with answers.',
         'Compare the tens first, then the ones.', '43 &lt; 61 because 4 tens &lt; 6 tens.',
         body, faq, sets, seo_title='Grade 1 Comparing and Ordering Numbers Worksheets (TEKS 1.2E)')


if __name__ == "__main__":
    build()
