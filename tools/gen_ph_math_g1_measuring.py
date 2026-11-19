# -*- coding: utf-8 -*-
"""
Philippines Grade 1 Math (MATATAG): Measuring Length and Distance with Non-Standard Units (Grade 1: Measurement and Geometry)
  python3 tools/gen_ph_math_g1_measuring.py
Comparing and ordering lengths, measuring with paper clips, cubes, hand spans and steps, measuring the right way, and
problems (US Grade 1 and BC Grade 1 makers).
Wrong answers come from real mistakes: leaving gaps between units, starting away from the end, and mixing units of
different sizes.
"""
import ph_common
from ph_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, peso, words)
import random
import gen_us_math_g1_measuring as usm
adopt(usm)
if hasattr(usm, 'R'): usm.R = random.Random(701100)
import gen_cabc_math_g1_measuring as cbm
adopt(cbm)
if hasattr(cbm, 'R'): cbm.R = random.Random(701101)
ph_common.GRADE = "grade-1"



def build():
    sets, R = build_sets([
        ("Longer and shorter", [("run", usm.set_compare, (usm.People,), 10), ("run", cbm.set_compare, (cbm.People,), 10)]),
        ("Order by length", [("run", usm.set_order, (usm.People,), 20)]),
        ("Measure with units", [("run", usm.set_units, (usm.People,), 10), ("run", cbm.set_units, (cbm.People,), 10)]),
        ("Measure the right way", [("run", usm.set_right_way, (usm.People,), 10), ("run", cbm.set_same_units, (cbm.People,), 10)]),
        ("Length problems", [("run", cbm.set_problems, (cbm.People,), 10), ("run", usm.set_word, (usm.People,), 10)]),
    ], 70110)
    finish(sets, R)
    body = lesson('<ul><li>To compare lengths, line up the ends.</li><li>To measure, place the units end to end, with no gaps and no overlaps.</li><li>Start at one end of the object and count the units.</li><li>Use units of the same size. A big unit gives a smaller count.</li></ul>',
        [example("A pencil is as long as 6 paper clips", ["count the clips end to end"], "6 paper clips long")],
        [['Gaps between units', 'Put the units end to end.'], ['Not starting at the end', 'Line up with the end of the object.'], ['Different-size units', 'Use units that are all the same.']])
    faq = [('What does MATATAG Math 1 ask about measuring?', 'Measure the length of an object and the distance between two objects using non-standard units, compare lengths and distances, and solve problems.'), ('What are non-standard units?', 'Things like paper clips, cubes, hand spans and steps.'), ('Why do two children get different answers?', 'Their hand spans or steps are different sizes.'), ('When do children learn centimeters?', 'In later grades.')]
    make('measuring-length-with-non-standard-units', 10, 'Measurement and Geometry', 'Grade 1: Measurement and Geometry',
         'Measure the length of an object and the distance between two objects using non-standard units; compare lengths and distances using non-standard units; solve problems involving lengths and distances using non-standard units.',
         'Measuring Length and Distance with Non-Standard Units', 'Measuring with Non-Standard Units',
         'Free Grade 1 measuring worksheets for the DepEd MATATAG curriculum: compare lengths, measure with paper clips, cubes and hand spans, and solve problems. 100 questions with pictures and answers.',
         'Units end to end, no gaps.', 'Bigger unit, smaller count.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
