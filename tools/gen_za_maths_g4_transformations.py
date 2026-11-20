# -*- coding: utf-8 -*-
"""
South Africa Grade 4 Maths (CAPS): Composite Shapes and Tessellations (Grade 4: 3.4 Transformations)
  python3 tools/gen_za_maths_g4_transformations.py
Building composite 2-D shapes and counting the shapes in them (Australia Year 4 makers), and tessellations: which
shapes tessellate, combining shapes and tessellated patterns (Australia Year 6 makers).
Wrong answers come from real mistakes: counting only the small shapes, thinking circles tessellate, and leaving gaps
in a pattern.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_au_maths_y4_composite_shapes as auc
adopt(auc)
if hasattr(auc, 'R'): auc.R = random.Random(804180)
import gen_au_maths_y6_tessellations as aut
adopt(aut)
if hasattr(aut, 'R'): aut.R = random.Random(804181)
za_common.GRADE = "grade-4"



def build():
    sets, R = build_sets([
        ("Make composite shapes", [("run", auc.set_make, ("rnd", auc.Pos), 20)]),
        ("Count the shapes", [("run", auc.set_count, ("rnd", auc.People), 20)]),
        ("Does it tessellate?", [("run", aut.set_identify, ("rnd", aut.People), 20)]),
        ("Tessellated patterns", [("run", aut.set_patterns, ("rnd", aut.People), 10), ("run", aut.set_which, ("rnd", aut.People), 10)]),
        ("Patterns in nature and everyday life", [("run", auc.set_objects, ("rnd", auc.People), 10), ("run", aut.set_problems, ("rnd", aut.People), 10)]),
    ], 80418)
    finish(sets, R)
    body = lesson('<ul><li>A <b>composite shape</b> is made of two or more shapes: a house shape is a square and a triangle.</li><li>Shapes <b>tessellate</b> when they cover a surface with no gaps and no overlaps, like floor tiles.</li><li>Squares, rectangles, triangles and regular hexagons tessellate. Circles do not.</li><li>Look for tessellations in nature (honeycomb) and in South African beadwork and wall art.</li></ul>',
        [example("Regular hexagons", ["3 meet at each point: 120° × 3 = 360°"], "they tessellate")],
        [['Only small shapes', 'Look for bigger shapes made of smaller ones.'], ['Circles tessellate', 'Circles leave gaps.'], ['Gaps or overlaps', 'A tessellation has neither.']])
    faq = [('What does CAPS Grade 4 say about transformations?', 'Build composite 2-D shapes and tessellated patterns, and describe patterns in nature, everyday life and our cultural heritage.'), ('What is a tessellation?', 'A pattern of shapes that covers a surface with no gaps or overlaps.'), ('Do all triangles tessellate?', 'Yes.'), ('Where do we see tessellations?', 'Floors, walls, honeycomb and Ndebele designs.')]
    make('composite-shapes-and-tessellations', 18, 'Space and Shape (Geometry)', 'Grade 4: 3.4 Transformations',
         'Build composite 2-D shapes; draw and describe tessellated patterns; describe patterns in nature, everyday life and our cultural heritage (e.g. in buildings, beadwork, mats and cloth).',
         'Composite Shapes and Tessellations', 'Composite Shapes and Tessellations',
         'Free CAPS Grade 4 worksheets on composite shapes and tessellations: building shapes, counting shapes, which shapes tessellate and tessellated patterns. 100 questions with memos.',
         'Tessellate: no gaps, no overlaps.', 'Composite shapes are built from smaller shapes.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
