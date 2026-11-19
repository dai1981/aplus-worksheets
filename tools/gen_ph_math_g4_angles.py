# -*- coding: utf-8 -*-
"""
Philippines Grade 4 Math (MATATAG): Angles: Right, Acute and Obtuse; Measuring with a Protractor (Grade 4: Measurement and Geometry)
  python3 tools/gen_ph_math_g4_angles.py
Naming right, acute and obtuse angles, estimating, and measuring and drawing angles with a protractor (US Grade 4
and Singapore Primary 4 makers with Filipino names).
Wrong answers come from real mistakes: reading the wrong scale of the protractor, calling a 100° angle acute, and
thinking longer arms make a bigger angle.
"""
import ph_common
from ph_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, peso, words)
import random
import gen_us_math_g4_angles as usa
adopt(usa)
if hasattr(usa, 'R'): usa.R = random.Random(704010)
import gen_sg_maths_p4_angles as sga
adopt(sga)
if hasattr(sga, 'R'): sga.R = random.Random(704011)
ph_common.GRADE = "grade-4"



def build():
    sets, R = build_sets([
        ("Right, acute and obtuse angles", [("run", usa.set_kinds, ("rnd",), 20)]),
        ("Name and compare angles", [("run", sga.set_names, ("rnd", sga.People), 20)]),
        ("Estimate angles", [("run", sga.set_estimate, ("rnd", sga.People), 20)]),
        ("Read a protractor", [("run", usa.set_protractor, ("rnd",), 20)]),
        ("Measure and draw angles", [("run", sga.set_protractor, ("rnd", sga.People), 20)]),
    ], 70401)
    finish(sets, R)
    body = lesson('<ul><li>An <b>angle</b> is made by two rays that meet at a vertex.</li><li>A <b>right angle</b> is exactly 90°, like the corner of a sheet of paper. An <b>acute angle</b> is less than 90°. An <b>obtuse angle</b> is more than 90° but less than 180°.</li><li>To measure: put the center of the protractor on the vertex and the 0° line on one ray. Read the scale that starts at 0 on that ray.</li><li>The length of the rays does not change the size of the angle.</li></ul>',
        [example("Measure an angle", ["Center on the vertex", "One ray on 0°", "Read where the other ray crosses"], "65°: acute")],
        [['Reading the wrong scale', 'Use the scale that starts at 0 on your ray.'], ['Calling a 100° angle acute', 'More than 90° is obtuse.'], ['Longer arms, bigger angle', 'Only the opening matters.']])
    faq = [('What does MATATAG Math 4 ask about angles?', 'Illustrate different angles (right, acute, and obtuse) using models, and measure and draw angles using a protractor.'), ('How many degrees is a right angle?', '90 degrees.'), ('Is a straight angle obtuse?', 'No. A straight angle is exactly 180°; obtuse angles are between 90° and 180°.'), ('How can I check a right angle without a protractor?', 'Use the corner of a sheet of paper.')]
    make('angles', 1, 'Measurement and Geometry', 'Grade 4: Measurement and Geometry',
         'Illustrate different angles (right, acute, and obtuse) using models; measure and draw angles using a protractor.',
         'Angles: Right, Acute and Obtuse; Measuring with a Protractor', 'Angles',
         'Free Grade 4 angles worksheets for the DepEd MATATAG curriculum: right, acute and obtuse angles, estimating, and measuring and drawing angles with a protractor. 100 questions with answers.',
         'Right = 90°, acute < 90°, obtuse between 90° and 180°.', 'Read the protractor scale that starts at 0 on one ray.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
