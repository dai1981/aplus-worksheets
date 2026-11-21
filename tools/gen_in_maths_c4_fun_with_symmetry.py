# -*- coding: utf-8 -*-
"""India Class 4 Maths, Maths Mela Chapter 11: Fun with Symmetry (Lines of Symmetry)
Is it a line of symmetry, counting lines, completing shapes on a grid, letters and symmetry in the world (UK Year 4 and BC Grade 4 set makers)."""
from in_prim import unit, mod, rn, co, le

uk = mod("gen_uk_maths_y4_symmetry", 604110)
bc = mod("gen_cabc_math_g4_symmetry", 604111)
unit(4, "fun-with-symmetry", 11, "G", 11, "Fun with Symmetry", "Lines of Symmetry", "symmetry",
     "Symmetry: identifying lines of symmetry in shapes, letters and designs, and completing symmetric figures (summary of NCERT Maths Mela Class 4)",
     "Class 4 Fun with Symmetry worksheet (Maths Mela Chapter 11): lines of symmetry, letters, completing shapes and symmetry around us. 100 questions with answers.",
     "A line of symmetry makes two mirror halves.", "Fold along the line: the halves match.",
     "<ul><li>A shape is symmetric if one half is the mirror image of the other.</li><li>A square has 4 lines of symmetry; a rectangle has 2; a circle has many.</li></ul>",
     [('How many lines of symmetry does a rectangle have?', ['Fold it across and down'], '2')],
     [['Counting the diagonals of a rectangle', 'Fold along a diagonal: the halves do not match.'], ['Shifting instead of reflecting', 'Each point must be the same distance from the mirror line.']],
     [('What is a line of symmetry?', 'A line that divides a shape into two halves that are mirror images.'), ('Do all shapes have symmetry?', 'No. A scalene triangle has no line of symmetry.')],
     [('Is it a line of symmetry?', [rn(uk, "set_is_line", 20)]),
      ('How many lines?', [rn(uk, "set_count", 10), rn(bc, "set_count", 10)]),
      ('Complete the shape', [rn(uk, "set_grid", 20)]),
      ('Symmetric letters', [rn(bc, "set_letters", 20)]),
      ('Symmetry around us', [rn(uk, "set_world", 10), rn(bc, "set_world", 10)])], 60411)
