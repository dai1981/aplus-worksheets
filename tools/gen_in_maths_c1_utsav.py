# -*- coding: utf-8 -*-
"""India Class 1 Maths, Joyful Mathematics Chapter 9: Utsav (Patterns)
Repeating patterns of shapes, colours and numbers: what comes next, the repeating part, missing pieces, number patterns."""
from in_prim import unit, mod, rn
ap = mod("gen_au_maths_y1_repeating_patterns", 601091)
cp = mod("gen_caon_math_g1_patterns", 601092)
unit(1, "utsav", 9, "P", 9, "Utsav", "Patterns", "patterns",
     "Patterns: identifying, describing and extending repeating patterns of shapes, colours, sounds and numbers (summary of NCERT Joyful Mathematics Class 1)",
     "Class 1 Utsav worksheet (Joyful Mathematics Chapter 9): repeating patterns, what comes next, the repeating part, missing pieces and number patterns. 100 picture questions with answers.",
     "Find the part that repeats.", "Then say what comes next.",
     "<ul><li>A <b>pattern</b> repeats the same part again and again: red, blue, red, blue, …</li><li>Find the repeating part, then continue it.</li></ul>",
     [("What comes next: ▲ ● ▲ ● ▲ …?", ["▲ ● repeats"], "●")],
     [["Copying only the last shape", "Find the whole part that repeats."], ["Missing a gap in the middle", "Say the pattern aloud from the start."]],
     [("What is a repeating pattern?", "A pattern where the same group of things comes again and again."), ("Where can children see patterns?", "In rangoli, garlands, clothes and festival decorations.")],
     [("What comes next?", [rn(ap, "set_next", 20)]),
      ("The repeating part", [rn(ap, "set_unit", 20)]),
      ("Fill the gap", [rn(ap, "set_gaps", 20)]),
      ("Number patterns", [rn(ap, "set_numbers", 20)]),
      ("Pattern stories", [rn(ap, "set_stories", 12), rn(cp, "set_core", 8)])], 60109)
