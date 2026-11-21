# -*- coding: utf-8 -*-
"""India Class 4 Maths, Maths Mela Chapter 8: Weigh it, Pour it (Weight and Capacity)
Grams and kilograms, millilitres and litres: reading scales and jugs, converting and problems (AU Year 4, Ontario Grade 4 and UK Year 4 set makers)."""
from in_prim import unit, mod, rn, co, le

sc = mod("gen_au_maths_y4_scales", 604080)
ca = mod("gen_caon_math_g4_metric", 604081)
uk = mod("gen_uk_maths_y4_converting_units", 604082)
unit(4, "weigh-it-pour-it", 8, "M", 8, "Weigh it, Pour it", "Weight and Capacity", "weight and capacity",
     "Measurement of weight (kg, g) and capacity (L, mL): estimating, measuring, converting and solving problems (summary of NCERT Maths Mela Class 4)",
     "Class 4 Weigh it, Pour it worksheet (Maths Mela Chapter 8): kg and g, L and mL, scales, jugs, converting and problems. 100 questions with answers.",
     "1 kg = 1,000 g; 1 L = 1,000 mL.", "Read each small mark carefully.",
     "<ul><li>Weight: 1 kg = 1,000 g. Capacity: 1 L = 1,000 mL.</li><li>Find what each small mark on a scale is worth before reading it.</li></ul>",
     [('Write 2 kg 350 g in grams.', ['2,000 + 350'], '2,350 g')],
     [['Using 100 g = 1 kg', '1,000 g make 1 kg.'], ['Reading the scale at the wrong mark', 'Count the value of each small step.']],
     [('How many millilitres are in a litre?', '1,000.'), ('What is weight?', 'How heavy something is, measured in grams and kilograms.')],
     [('Read the weight', [rn(sc, "set_mass", 20)]),
      ('Read the capacity', [rn(sc, "set_capacity", 20)]),
      ('Grams and kilograms', [rn(ca, "set_grams", 20)]),
      ('Litres and millilitres', [rn(ca, "set_litres", 20)]),
      ('Problems', [rn(uk, "set_mass_cap", 10), rn(sc, "set_story", 10)])], 60408)
