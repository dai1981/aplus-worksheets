# -*- coding: utf-8 -*-
"""
Texas Grade 4 Math: Measuring Angles: Degrees, Protractors and Unknown Angles (TEKS 4.7A–4.7E)
  python3 tools/gen_ustx_math_g4_measuring_angles.py
Angles as turns and parts of a circle (1° is 1/360 of a turn), naming and estimating angles, reading a protractor,
angles that add up, and unknown adjacent angles. The question makers come from the US Grade 4 angle unit with
Texas names. Wrong answers come from real mistakes: reading the wrong scale of the protractor, adding instead of
subtracting for an unknown part, and thinking a longer ray makes a bigger angle.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, build_sets, example, figure)
import gen_us_math_g4_angles as usa
adopt(usa)
tx_common.GRADE = "grade-4"


def build():
    sets, R = build_sets([
        ("Angles as turns: degrees", [("run", usa.set_turns, ("rnd",), 20)]),
        ("Acute, right, obtuse and straight: estimate", [("run", usa.set_kinds, ("rnd",), 20)]),
        ("Read a protractor", [("run", usa.set_protractor, ("rnd",), 20)]),
        ("Angle measures add up", [("run", usa.set_add, ("rnd",), 20)]),
        ("Unknown angles and word problems", [("run", usa.set_unknown, ("rnd", usa.People), 20)]),
    ], 64020)
    finish(sets, R)
    body = lesson('<ul><li>An angle measures a <b>turn</b>. A full turn is 360°, so 1° is 1/360 of a circle. A quarter turn is 90°.</li><li>To use a <b>protractor</b>, put the center on the vertex and one ray on 0. Read the scale that starts at 0 on that ray.</li><li>Angles next to each other <b>add</b>. To find an unknown part, subtract the known part from the whole.</li></ul>',
        [example("Angle ABC is 125°. Ray BD splits it, and angle ABD is 40°. What is angle DBC?", ["125 − 40 = 85"], "85°"), example("How many degrees is a half turn?", ["A full turn is 360°.", "360 ÷ 2 = 180"], "180°")],
        [['Reading the wrong protractor scale', 'Start from the 0 that lines up with one ray.'], ['Adding when a part is missing', 'Whole minus known part = unknown part.'], ['Thinking longer rays mean a bigger angle', 'The size of the turn matters, not the length of the rays.']])
    faq = [('What do TEKS 4.7A and 4.7B ask?', 'Understand an angle as the part of a circle cut out by its rays, and degrees as 1/360 of a circle.'), ('What does TEKS 4.7C ask?', 'Measure angles in whole-number degrees with a protractor.'), ('What does TEKS 4.7E ask?', 'Find an unknown angle formed by two non-overlapping adjacent angles, given one or both measures.'), ('Why are there two scales on a protractor?', 'So you can measure from either side. Use the scale that starts at 0 on the ray you lined up.')]
    make('measuring-angles', 20, 'Geometry and Measurement', '4.7A–4.7E',
         '4.7A illustrate the measure of an angle as the part of a circle whose center is at the vertex of the angle that is “cut out” by the rays of the angle; 4.7B illustrate degrees as the units used to measure an angle, where 1/360 of any circle is one degree; 4.7C determine the approximate measures of angles in degrees to the nearest whole number using a protractor; 4.7D draw an angle with a given measure; 4.7E determine the measure of an unknown angle formed by two non-overlapping adjacent angles given one or both angle measures',
         'Measuring Angles: Degrees, Protractors and Unknown Angles', 'Measuring Angles',
         'Free Grade 4 angle worksheets for Texas TEKS 4.7: angles as turns and degrees, acute, right and obtuse angles, reading a protractor, adding angles and finding unknown adjacent angles. 100 questions with answers.',
         'A full turn is 360°. Adjacent angles add up.', "Line up the protractor's 0 with one ray and read that scale. Unknown part = whole − known part.",
         body, faq, sets, seo_title='Grade 4 Measuring Angles Worksheets: Protractors and Unknown Angles (TEKS 4.7, STAAR)')


if __name__ == "__main__":
    build()
