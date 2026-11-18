# -*- coding: utf-8 -*-
"""
Texas Grade 1 Math: Measuring Length with Units (TEKS 1.7A, 1.7B, 1.7C, 1.7D)
  python3 tools/gen_ustx_math_g1_measuring_length.py
Measuring with cubes and paper clips, measuring the right way (no gaps or overlaps), two different units, ordering
by length, and how many longer (the US Grade 1 and Grade 2 makers with Texas names).
Wrong answers come from real mistakes: leaving gaps, starting past the end, and thinking a bigger unit gives a
bigger number.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import gen_us_math_g1_measuring as me
adopt(me)
import gen_us_math_g2_measuring as me2
adopt(me2)
tx_common.GRADE = "grade-1"



def build():
    sets, R = build_sets([
        ("Measure with cubes and paper clips", [("run", me.set_units, (me.People,), 20)]),
        ("Measure the right way", [("run", me.set_right_way, (me.People,), 20)]),
        ("Two different units", [("run", me2.set_two_units, (me2.People,), 20)]),
        ("Order by length", [("run", me.set_order, (me.People,), 20)]),
        ("How many longer?", [("run", me.set_word, (me.People,), 20)]),
    ], 69117)
    finish(sets, R)
    body = lesson('<ul><li>Lay same-size units <b>end to end</b>. No gaps. No overlaps.</li><li>Start at one end and stop at the other end.</li><li>Say the number and the unit: 6 cubes long.</li><li>Bigger units: fewer of them. Smaller units: more of them.</li></ul>',
        [example("A pencil is 6 cubes long", ["Count the cubes end to end"], "6 cubes")],
        [['Leaving gaps', 'Units must touch.'], ['Starting past the end', 'Line up the first unit with the end.'], ['Thinking bigger units give a bigger number', 'Bigger units mean fewer units.']])
    faq = [('What does TEKS 1.7B ask?', 'Illustrate that the length of an object is the number of same-size units of length that, when laid end-to-end with no gaps or overlaps, reach from one end of the object to the other.'), ('What does TEKS 1.7C ask?', 'Measure the same object/distance with units of two different lengths and describe how and why the measurements differ.'), ('What does TEKS 1.7D ask?', 'Describe a length to the nearest whole unit using a number and a unit.'), ('What does TEKS 1.7A ask?', 'Use measuring tools to measure the length of objects to reinforce the continuous nature of linear measurement.')]
    make('measuring-length', 17, 'Geometry and Measurement', '1.7A, 1.7B, 1.7C, 1.7D',
         '1.7A use measuring tools to measure the length of objects to reinforce the continuous nature of linear measurement; 1.7B illustrate that the length of an object is the number of same-size units of length that, when laid end-to-end with no gaps or overlaps, reach from one end of the object to the other; 1.7C measure the same object/distance with units of two different lengths and describe how and why the measurements differ; 1.7D describe a length to the nearest whole unit using a number and a unit',
         'Measuring Length with Units', 'Measuring Length',
         'Free Grade 1 measuring worksheets for Texas TEKS 1.7A–1.7D: measure with cubes and paper clips, no gaps or overlaps, two different units and comparing lengths. 100 questions with answers.',
         'Units end to end: no gaps, no overlaps.', 'Bigger units, fewer units.',
         body, faq, sets, seo_title='Grade 1 Measuring Length Worksheets (TEKS 1.7B)')


if __name__ == "__main__":
    build()
