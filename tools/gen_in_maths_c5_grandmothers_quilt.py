# -*- coding: utf-8 -*-
"""India Class 5 Maths, Maths Mela Chapter 11: Grandmother's Quilt (Area and Perimeter)
Perimeter of shapes, area of rectangles and composite shapes, estimating area and quilt stories (UK Year 5 and BC Grade 5 set makers)."""
from in_prim import unit, mod, rn, co, le

uk = mod("gen_uk_maths_y5_area_perimeter", 605110)
bc = mod("gen_cabc_math_g5_area_perimeter", 605111)
unit(5, "grandmothers-quilt", 11, "M", 11, "Grandmother's Quilt", "Area and Perimeter", "area and perimeter",
     "Area and perimeter: measuring area in square units, area of rectangles, perimeter, and shapes with the same area but different perimeters (summary of NCERT Maths Mela Class 5)",
     "Class 5 Grandmother's Quilt worksheet (Maths Mela Chapter 11): perimeter, area of rectangles and composite shapes, estimating and problems. 100 questions with answers.",
     "Area = length × width.", "Perimeter = distance around.",
     "<ul><li>Perimeter: add all the sides. Rectangle: 2 × (length + width).</li><li>Area: count square units, or length × width for a rectangle.</li><li>Split an L-shape into rectangles.</li></ul>",
     [('A quilt is 6 squares by 4 squares.', ['6 × 4'], '24 squares')],
     [['Mixing up area and perimeter', 'Area is inside (square units); perimeter is around.'], ['Counting corner squares twice in perimeter', 'Count the edges, not the squares.']],
     [('What is area?', 'The amount of surface a shape covers, in square units.'), ('Can two shapes have the same area but different perimeters?', 'Yes: 1 × 12 and 3 × 4 rectangles both have area 12.')],
     [('Perimeter', [rn(uk, "set_perimeter", 10), rn(bc, "set_perimeter", 10)]),
      ('Area by counting', [rn(bc, "set_count", 20)]),
      ('Area of rectangles', [rn(uk, "set_rect_area", 10), rn(bc, "set_formula", 10)]),
      ('Composite shapes', [rn(uk, "set_composite_area", 10), rn(bc, "set_missing", 10)]),
      ('Quilt stories', [rn(uk, "set_story", 10), rn(bc, "set_story", 10)])], 60511)
