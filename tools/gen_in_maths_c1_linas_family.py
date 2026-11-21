# -*- coding: utf-8 -*-
"""India Class 1 Maths, Joyful Mathematics Chapter 7: Lina's Family (Measurement)
Comparing lengths and heights, heavier and lighter, holds more and less, measuring with hand spans and other units."""
from in_prim import unit, mod, rn
af = mod("gen_au_maths_f_comparing_length_mass_capacity", 601071)
us = mod("gen_us_math_g1_measuring", 601072)
uk = mod("gen_uk_maths_y1_measuring", 601073)
unit(1, "linas-family", 7, "M", 7, "Lina's Family", "Comparing and Measuring Length, Weight and Capacity", "measurement",
     "Measurement: comparing lengths, heights, weights and capacities using words such as longer, taller, heavier and holds more; measuring with non-standard units such as hand spans (summary of NCERT Joyful Mathematics Class 1)",
     "Class 1 Lina's Family worksheet (Joyful Mathematics Chapter 7): longer and shorter, taller, heavier and lighter, holds more, measuring with units. 100 picture questions with answers.",
     "Line things up at one end to compare length.", "Count the units with no gaps or overlaps.",
     "<ul><li>Compare <b>length</b> and <b>height</b>: longer, shorter, taller.</li><li>Compare <b>weight</b>: heavier, lighter. Compare <b>capacity</b>: holds more, holds less.</li><li>Measure with the same unit (hand spans, clips) placed end to end.</li></ul>",
     [("A pencil is 6 clips long and a crayon is 4 clips long. Which is longer?", ["6 is more than 4"], "The pencil")],
     [["Not starting at the same line", "Line up the ends before comparing."], ["Leaving gaps between units", "Place units end to end."]],
     [("What are non-standard units?", "Things like hand spans, steps or paper clips used to measure before rulers."), ("Why must units be the same size?", "So the count is fair: big and small clips give different numbers.")],
     [("Longer and taller", [rn(af, "set_length", 10), rn(af, "set_height", 10)]),
      ("Heavier and lighter", [rn(af, "set_mass", 10), rn(uk, "set_mass", 10)]),
      ("Holds more", [rn(af, "set_capacity", 10), rn(uk, "set_capacity", 10)]),
      ("Order by length", [rn(us, "set_order", 20)]),
      ("Measuring with units", [rn(us, "set_units", 10), rn(us, "set_right_way", 10)])], 60107)
