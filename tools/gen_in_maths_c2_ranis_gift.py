# -*- coding: utf-8 -*-
"""India Class 2 Maths, Joyful Mathematics Chapter 7: Rani's Gift (Measurement)
Measuring length with hand spans and centimetres, reading a ruler, metres and centimetres, comparing and problems (Ontario Grade 2 and US Grade 2 set makers)."""
from in_prim import unit, mod, rn
ca = mod("gen_caon_math_g2_length", 602071)
us = mod("gen_us_math_g2_measuring", 602072)
unit(2, "ranis-gift", 7, "M", 7, "Rani's Gift", "Measuring Length", "measuring length",
     "Measurement of length: using non-standard units such as hand spans, the need for a standard unit, measuring in centimetres and metres (summary of NCERT Joyful Mathematics Class 2)",
     "Class 2 Rani's Gift worksheet (Joyful Mathematics Chapter 7): measuring length, choosing units, reading a ruler in centimetres, metres and centimetres. 100 questions with answers.",
     "Start measuring at 0 on the ruler.", "Small things in cm, long things in m.",
     "<ul><li>Hand spans differ from person to person, so we use <b>centimetres</b> (cm) and <b>metres</b> (m).</li><li>Line up one end with 0 on the ruler and read the other end.</li><li>100 cm = 1 m.</li></ul>",
     [("A pencil starts at 0 and ends at 12. How long is it?", ["Read the end mark"], "12 cm")],
     [["Starting at 1 on the ruler", "Start at 0, or subtract the start mark."], ["Measuring a room in cm", "Long lengths are measured in metres."]],
     [("Why do we need standard units?", "Everyone's hand span is different, but a centimetre is the same everywhere."), ("How many centimetres make a metre?", "100.")],
     [("Choose the unit", [rn(ca, "set_units", 20)]),
      ("Read the ruler", [rn(ca, "set_from_zero", 20)]),
      ("Not starting at 0", [rn(ca, "set_not_zero", 10), rn(us, "set_not_zero", 10)]),
      ("Metres and centimetres", [rn(ca, "set_cm_m", 12), rn(ca, "set_not_zero", 8)]),
      ("Length problems", [rn(ca, "set_problems", 14), rn(ca, "set_not_zero", 6)])], 60207)
