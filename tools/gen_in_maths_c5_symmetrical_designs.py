# -*- coding: utf-8 -*-
"""India Class 5 Maths, Maths Mela Chapter 10: Symmetrical Designs (Reflection, Rotation and Symmetry)
Reflections and rotations, which picture shows a flip or a turn, and symmetric designs (Ontario Grade 5, AU Year 5, BC Grade 5 and UK Year 5 set makers)."""
from in_prim import unit, mod, rn, co, le

ca = mod("gen_caon_math_g5_transformations", 605100)
au = mod("gen_au_maths_y5_transformations", 605101)
bc = mod("gen_cabc_math_g5_transformations", 605102)
uk = mod("gen_uk_maths_y5_reflection_translation", 605103)
unit(5, "symmetrical-designs", 10, "G", 10, "Symmetrical Designs", "Reflection, Rotation and Symmetry", "symmetrical designs",
     "Symmetry: reflection (line) symmetry and rotational symmetry in designs, and making symmetric patterns by flipping and turning (summary of NCERT Maths Mela Class 5)",
     "Class 5 Symmetrical Designs worksheet (Maths Mela Chapter 10): reflections, rotations, flips and turns and symmetric designs. 100 questions with answers.",
     "A reflection flips a shape over a mirror line.", "A rotation turns it about a point.",
     "<ul><li>A <b>reflection</b> (flip) makes a mirror image across a line.</li><li>A <b>rotation</b> (turn) turns a shape about a point: quarter, half or full turn.</li><li>Many rangoli designs have both kinds of symmetry.</li></ul>",
     [('A shape looks the same after a half turn.', ['It fits twice in a full turn'], 'It has rotational symmetry of order 2')],
     [['Shifting instead of flipping', 'Each point moves to the same distance on the other side of the mirror.'], ['Turning the wrong way', 'Clockwise is the way clock hands move.']],
     [('What is rotational symmetry?', 'A shape has it if it looks the same after a turn of less than a full turn.'), ('What is a reflection?', 'A flip over a mirror line.')],
     [('Reflections', [rn(ca, "set_reflect", 10), rn(au, "set_reflect", 10)]),
      ('Rotations', [rn(ca, "set_rotate", 10), rn(au, "set_rotate", 10)]),
      ('Flip or turn?', [rn(bc, "set_flip", 10), rn(bc, "set_turn", 10)]),
      ('Which transformation?', [rn(ca, "set_which", 10), rn(bc, "set_which", 10)]),
      ('Reflect on a grid', [rn(uk, "set_reflect", 20)])], 60510)
