# -*- coding: utf-8 -*-
"""India Class 5 Maths, Maths Mela Chapter 3: Angles as Turns (Angles and Turns)
Angles as turns, right angles, acute and obtuse angles, estimating and measuring with a protractor (AU Year 5, UK Year 5 and Ontario Grade 5 set makers)."""
from in_prim import unit, mod, rn, co, le

au = mod("gen_au_maths_y5_angles", 605030)
uk = mod("gen_uk_maths_y5_angles", 605031)
ca = mod("gen_caon_math_g5_angles", 605032)
unit(5, "angles-as-turns", 3, "G", 3, "Angles as Turns", "Angles and Turns", "angles",
     "Angles: angles as turns, right angles, comparing angles, acute and obtuse angles, and measuring angles in degrees (summary of NCERT Maths Mela Class 5)",
     "Class 5 Angles as Turns worksheet (Maths Mela Chapter 3): turns, right, acute and obtuse angles, estimating and measuring. 100 questions with answers.",
     "A full turn is 360°; a quarter turn is 90°.", "Acute < 90° < obtuse < 180°.",
     "<ul><li>A quarter turn is a <b>right angle</b> (90°); a half turn is 180°; a full turn is 360°.</li><li><b>Acute</b>: less than 90°. <b>Obtuse</b>: between 90° and 180°.</li></ul>",
     [('How many degrees in three quarter turns?', ['3 × 90°'], '270°')],
     [['Reading the wrong scale of the protractor', 'Start from the 0 on the arm you are measuring.'], ['Calling 90° obtuse', '90° is a right angle.']],
     [('What is a degree?', 'The unit for measuring angles; a full turn is 360 degrees.'), ('How are turns and angles linked?', 'An angle measures how much something turns.')],
     [('Name the angle', [rn(au, "set_names", 10), rn(uk, "set_types", 10)]),
      ('Estimate', [rn(au, "set_estimate", 10), rn(ca, "set_estimate", 10)]),
      ('Measure with a protractor', [rn(au, "set_protractor", 10), rn(uk, "set_protractor", 10)]),
      ('Angle facts', [rn(uk, "set_facts", 10), rn(ca, "set_line", 10)]),
      ('Angles around us', [rn(au, "set_everyday", 10), rn(ca, "set_real", 10)])], 60503)
