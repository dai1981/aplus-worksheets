# -*- coding: utf-8 -*-
"""India Class 5 Maths, Maths Mela Chapter 7: Shapes and Patterns (Triangles, Quadrilaterals and Patterns)
Classifying triangles and quadrilaterals, their angles and sides, and growing and number patterns (SG Primary 5, Ontario Grade 5 set makers)."""
from in_prim import unit, mod, rn, co, le

tr = mod("gen_sg_maths_p5_triangles", 605070)
qu = mod("gen_sg_maths_p5_quadrilaterals", 605071)
pa = mod("gen_caon_math_g5_patterns", 605072)
unit(5, "shapes-and-patterns", 7, "G", 7, "Shapes and Patterns", "Triangles, Quadrilaterals and Patterns", "shapes and patterns",
     "Shapes and patterns: properties of triangles and quadrilaterals, tiling patterns, and number and shape patterns with rules (summary of NCERT Maths Mela Class 5)",
     "Class 5 Shapes and Patterns worksheet (Maths Mela Chapter 7): triangles, quadrilaterals, angle sums, growing patterns and rules. 100 questions with answers.",
     "Angles in a triangle add up to 180°.", "Find the rule to continue a pattern.",
     "<ul><li>Triangles: equilateral (3 equal sides), isosceles (2 equal), scalene (none). Angles add up to 180°.</li><li>Quadrilaterals: square, rectangle, parallelogram, rhombus, trapezium.</li><li>A growing pattern follows a rule: +3 each step.</li></ul>",
     [('Two angles of a triangle are 50° and 60°.', ['180° − 110°'], '70°')],
     [['Using 360° for a triangle', "A triangle's angles add up to 180°."], ['Thinking a rhombus has right angles', 'Only a square rhombus does.']],
     [('What is an isosceles triangle?', 'A triangle with two equal sides (and two equal angles).'), ('What is a growing pattern?', 'A pattern that changes by the same rule each step.')],
     [('Kinds of triangles', [rn(tr, "set_classify", 20, spots=tr.Spots(__import__("random").Random(605071)))]),
      ('Angles of a triangle', [rn(tr, "set_sum", 20)]),
      ('Quadrilaterals', [rn(qu, "set_name", 10, spots=qu.Spots(__import__("random").Random(605072))), rn(qu, "set_properties", 10)]),
      ('Growing patterns', [rn(pa, "set_grow", 20)]),
      ('Pattern rules', [rn(pa, "set_rules", 10), rn(pa, "set_tables", 10)])], 60507)
