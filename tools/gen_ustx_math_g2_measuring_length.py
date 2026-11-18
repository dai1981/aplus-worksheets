# -*- coding: utf-8 -*-
"""
Texas Grade 2 Math: Measuring Length with Rulers (TEKS 2.9A, 2.9B, 2.9D)
  python3 tools/gen_ustx_math_g2_measuring_length.py
Measuring from zero, measuring when the object does not start at zero, estimating, measuring with two units, and
comparing lengths (the US Grade 2 makers with Texas names).
Wrong answers come from real mistakes: starting at 1 instead of 0, counting the tick marks instead of the spaces,
and thinking a bigger unit gives a bigger number.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import gen_us_math_g2_measuring as me
adopt(me)
tx_common.GRADE = "grade-2"



def build():
    sets, R = build_sets([
        ("Measure from zero", [("run", me.set_from_zero, (me.People,), 20)]),
        ("When it does not start at zero", [("run", me.set_not_zero, (me.People,), 20)]),
        ("Estimate length", [("run", me.set_estimate, (me.People,), 20)]),
        ("Bigger units, fewer units", [("run", me.set_two_units, (me.People,), 20)]),
        ("Which is longer? How much longer?", [("run", me.set_longer, (me.People,), 20)]),
    ], 69215)
    finish(sets, R)
    body = lesson('<ul><li>Line up one end of the object with the <b>0 mark</b> on the ruler.</li><li>If it starts at another mark, subtract: from 3 to 8 is 5 units.</li><li>A <b>bigger unit</b> means <b>fewer units</b>: a desk is about 1 yard or about 3 feet.</li><li>Use inches, feet and yards, or centimeters and meters.</li></ul>',
        [example("A pencil goes from 2 in. to 9 in.", ["9 − 2"], "7 inches")],
        [['Starting at 1 instead of 0', 'Line up the end with 0.'], ['Counting the tick marks', 'Count the spaces between marks.'], ['Thinking a bigger unit gives a bigger number', 'Bigger units mean fewer of them.']])
    faq = [('What does TEKS 2.9A ask?', 'Find the length of objects using concrete models for standard units of length.'), ('What does TEKS 2.9B ask?', 'Describe the inverse relationship between the size of the unit and the number of units needed to equal the length of an object.'), ('What does TEKS 2.9D ask?', 'Determine the length of an object to the nearest marked unit using rulers, yardsticks, meter sticks or measuring tapes.'), ('Which is longer, a centimeter or an inch?', 'An inch. 1 inch is about 2 and a half centimeters.')]
    make('measuring-length', 15, 'Geometry and Measurement', '2.9A, 2.9B, 2.9D',
         '2.9A find the length of objects using concrete models for standard units of length; 2.9B describe the inverse relationship between the size of the unit and the number of units needed to equal the length of an object; 2.9D determine the length of an object to the nearest marked unit using rulers, yardsticks, meter sticks, or measuring tapes',
         'Measuring Length with Rulers', 'Measuring Length',
         'Free Grade 2 length worksheets for Texas TEKS 2.9A, 2.9B and 2.9D: measure with rulers from zero and from other marks, estimate, compare units and compare lengths. 100 questions with answers.',
         'Line up the end with 0 and count the spaces.', 'From 2 in. to 9 in. is 7 inches. Bigger units, fewer units.',
         body, faq, sets, seo_title='Grade 2 Measuring Length Worksheets (TEKS 2.9A, 2.9D)')


if __name__ == "__main__":
    build()
