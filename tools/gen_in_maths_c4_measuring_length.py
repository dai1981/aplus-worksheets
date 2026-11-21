# -*- coding: utf-8 -*-
"""India Class 4 Maths, Maths Mela Chapter 6: Measuring Length (Millimetres, Centimetres, Metres and Kilometres)
Choosing units, reading scales, converting between mm, cm, m and km, comparing and problems (UK Year 4, Ontario Grade 4 and AU Year 4 set makers)."""
from in_prim import unit, mod, rn, co, le

uk = mod("gen_uk_maths_y4_converting_units", 604060)
ca = mod("gen_caon_math_g4_metric", 604061)
sc = mod("gen_au_maths_y4_scales", 604062)
unit(4, "measuring-length", 6, "M", 6, "Measuring Length", "Millimetres, Centimetres, Metres and Kilometres", "measuring length",
     "Measurement of length: estimating and measuring in mm, cm, m and km, converting between units, and solving problems (summary of NCERT Maths Mela Class 4)",
     "Class 4 Measuring Length worksheet (Maths Mela Chapter 6): mm, cm, m and km, reading scales, converting and problems. 100 questions with answers.",
     "1 cm = 10 mm, 1 m = 100 cm, 1 km = 1,000 m.", "Choose the unit to suit the length.",
     "<ul><li>10 mm = 1 cm; 100 cm = 1 m; 1,000 m = 1 km.</li><li>A pencil is measured in cm, a room in m, a journey in km.</li></ul>",
     [('Write 3 m 25 cm in cm.', ['3 × 100 + 25'], '325 cm')],
     [['Using 10 cm = 1 m', '100 cm make 1 m.'], ['Measuring from 1 on the ruler', 'Start at 0.']],
     [('How many metres are in a kilometre?', '1,000.'), ('What is a millimetre?', 'A tenth of a centimetre; the tiny marks on a ruler.')],
     [('Choose the unit', [rn(ca, "set_choose", 14), rn(sc, "set_story", 6)]),
      ('Read the scale', [rn(sc, "set_length", 20)]),
      ('Convert units', [rn(uk, "set_length", 20)]),
      ('Metric prefixes', [rn(ca, "set_prefix", 16), rn(uk, "set_compare", 4)]),
      ('Length problems', [rn(uk, "set_story", 10), rn(ca, "set_story", 10)])], 60406)
