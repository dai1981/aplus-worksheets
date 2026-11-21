# -*- coding: utf-8 -*-
"""India Class 3 Maths, Maths Mela Chapter 11: Filling and Lifting (Capacity and Weight)
Litres and millilitres, kilograms and grams: choosing units, reading scales and jugs, comparing and problems (Ontario Grade 3 and US Grade 3 set makers)."""
from in_prim import unit, mod, rn, co, le

ca = mod("gen_caon_math_g3_mass_capacity", 603110)
us = mod("gen_us_math_g3_mass_volume", 603111)
unit(3, "filling-and-lifting", 11, "M", 11, "Filling and Lifting", "Capacity and Weight", "capacity and weight",
     "Capacity and weight: comparing and measuring with non-standard and standard units (litre, millilitre, kilogram, gram) (summary of NCERT Maths Mela Class 3)",
     "Class 3 Filling and Lifting worksheet (Maths Mela Chapter 11): litres, millilitres, kilograms and grams, scales, jugs and problems. 100 questions with answers.",
     "1 L = 1,000 mL and 1 kg = 1,000 g.", "Choose a sensible unit.",
     "<ul><li><b>Capacity</b> is how much a container holds: litres (L) and millilitres (mL).</li><li><b>Weight</b> is how heavy something is: kilograms (kg) and grams (g).</li><li>Read the scale where the pointer stops.</li></ul>",
     [('A jug holds 2 L. How many mL is that?', ['1 L = 1,000 mL'], '2,000 mL')],
     [['Weighing a bag of rice in grams only', 'Heavy things are measured in kg.'], ['Reading the scale at the wrong mark', 'Count what each small mark is worth.']],
     [('What is the difference between capacity and weight?', 'Capacity is how much a container holds; weight is how heavy something is.'), ('How many grams make a kilogram?', '1,000.')],
     [('Choose the unit', [rn(ca, "set_units", 10), rn(us, "set_units", 10)]),
      ('Read the scale', [rn(ca, "set_scale", 10), rn(us, "set_scale", 10)]),
      ('Read the jug', [rn(ca, "set_jug", 10), rn(us, "set_container", 10)]),
      ('Compare', [rn(ca, "set_compare", 10), rn(us, "set_balance", 10)]),
      ('Problems', [rn(ca, "set_story", 10), rn(us, "set_story", 10)])], 60311)
