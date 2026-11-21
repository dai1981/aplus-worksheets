# -*- coding: utf-8 -*-
"""India Class 5 Maths, Maths Mela Chapter 8: Weight and Capacity (Weight and Capacity)
Kilograms and grams, litres and millilitres: reading scales, converting, comparing and problems (UK Year 5, AU Year 5, Ontario Grade 5 and SG Primary 5 set makers)."""
from in_prim import unit, mod, rn, co, le

uk = mod("gen_uk_maths_y5_converting_units", 605080)
au = mod("gen_au_maths_y5_metric_units", 605081)
ca = mod("gen_caon_math_g5_metric", 605082)
sg = mod("gen_sg_maths_p5_volume", 605083)
unit(5, "weight-and-capacity", 8, "M", 8, "Weight and Capacity", "Weight and Capacity", "weight and capacity",
     "Measurement of weight and capacity: estimating and measuring in kg, g, L and mL, converting and solving problems (summary of NCERT Maths Mela Class 5)",
     "Class 5 Weight and Capacity worksheet (Maths Mela Chapter 8): kg and g, L and mL, converting, comparing and problems. 100 questions with answers.",
     "1 kg = 1,000 g; 1 L = 1,000 mL.", "Convert to one unit, then compare or add.",
     "<ul><li>2 kg 450 g = 2,450 g; 1.5 L = 1,500 mL.</li><li>Add or subtract after changing to the same unit.</li></ul>",
     [('A bucket holds 12 L. How many 500 mL mugs fill it?', ['12 L = 12,000 mL', '12,000 ÷ 500'], '24 mugs')],
     [['Using 100 g = 1 kg', '1,000 g make 1 kg.'], ['Adding kg and g directly', 'Change both to grams first.']],
     [('How many grams are in 2.5 kg?', '2,500 g.'), ('What is capacity?', 'How much a container can hold.')],
     [('Convert weight and capacity', [rn(uk, "set_mass_cap", 20)]),
      ('Read the scale', [rn(au, "set_read", 20)]),
      ('Weight and capacity', [rn(ca, "set_mass_cap", 20)]),
      ('Litres', [rn(sg, "set_litres", 20)]),
      ('Problems', [rn(au, "set_story", 10), rn(ca, "set_story", 10)])], 60508)
