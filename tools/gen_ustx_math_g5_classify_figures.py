# -*- coding: utf-8 -*-
"""
Texas Grade 5 Math: Classifying Two-Dimensional Figures in a Hierarchy (TEKS 5.5A)
  python3 tools/gen_ustx_math_g5_classify_figures.py
Classifying triangles by sides and angles, naming quadrilaterals by their properties, the hierarchy of
quadrilaterals, always/sometimes/never, and how properties pass down. The question makers come from the US
Grade 5 classify figures unit with Texas names.
Wrong answers come from real mistakes: thinking a square is not a rectangle, thinking a trapezoid can have no
parallel sides, and naming a shape by how it is turned.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import gen_us_math_g5_classify_figures as usc
adopt(usc)
tx_common.GRADE = "grade-5"



def build():
    sets, R = build_sets([
        ("Classify triangles by sides and angles", [("run", usc.set_triangles, ("rnd",), 20)]),
        ("Name quadrilaterals by their properties", [("run", usc.set_quads, ("rnd",), 20)]),
        ("The hierarchy diagram", [("run", usc.set_hierarchy, ("rnd",), 20)]),
        ("Always, sometimes, never", [("run", usc.set_asn, ("rnd",), 20)]),
        ("Properties pass down", [("run", usc.set_reason, ("rnd",), 20)]),
    ], 65018)
    finish(sets, R)
    body = lesson('<ul><li>Figures are sorted into <b>sets and subsets</b>. Every square is a rectangle and a rhombus; every rectangle and rhombus is a parallelogram; every parallelogram is a quadrilateral.</li><li>A subset has all the properties of the set above it.</li><li>Triangles are named by angles (acute, right, obtuse) and by sides (equilateral, isosceles, scalene).</li></ul>',
        [example("Is every rectangle a parallelogram?", ["A rectangle has 2 pairs of parallel sides."], "yes"), example("Is every rhombus a square?", ["A rhombus does not need right angles."], "no")],
        [['Thinking a square is not a rectangle', 'A square has 4 right angles, so it is a special rectangle.'], ['Thinking all parallelograms are rectangles', 'A parallelogram does not need right angles.'], ['Naming a shape by how it is turned', 'Use its sides and angles.']])
    faq = [('What does TEKS 5.5A ask?', 'Classify two-dimensional figures in a hierarchy of sets and subsets using graphic organizers based on their attributes and properties.'), ('What is a hierarchy of figures?', 'A diagram that shows which groups of figures belong inside other groups, such as squares inside rectangles inside parallelograms.'), ('Is an equilateral triangle isosceles?', 'Yes. It has at least two equal sides, so it is always isosceles.'), ('Can a shape have more than one name?', 'Yes. A square is also a rhombus, a rectangle, a parallelogram and a quadrilateral.')]
    make('classifying-two-dimensional-figures', 18, 'Geometry and Measurement', '5.5A',
         '5.5A classify two-dimensional figures in a hierarchy of sets and subsets using graphic organizers based on their attributes and properties',
         'Classifying Two-Dimensional Figures in a Hierarchy', 'Classifying 2D Figures',
         'Free Grade 5 geometry worksheets for Texas TEKS 5.5A: classify triangles, name quadrilaterals, the hierarchy of figures, always/sometimes/never and properties that pass down. 100 questions with answers.',
         'A subset has every property of the set above it.', 'Every square is a rectangle and a rhombus. Every rectangle is a parallelogram.',
         body, faq, sets, seo_title='Grade 5 Classifying 2D Figures Worksheets: Hierarchy (TEKS 5.5A, STAAR)')


if __name__ == "__main__":
    build()
