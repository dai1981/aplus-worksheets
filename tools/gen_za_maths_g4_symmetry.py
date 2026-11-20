# -*- coding: utf-8 -*-
"""
South Africa Grade 4 Maths (CAPS): Line Symmetry in 2-D Shapes (Grade 4: 3.3 Symmetry)
  python3 tools/gen_za_maths_g4_symmetry.py
Is it a line of symmetry, how many lines of symmetry, symmetry in turned shapes, completing shapes on a grid and
symmetry in the world (UK Year 4 makers).
Wrong answers come from real mistakes: taking the diagonal of a rectangle as a line of symmetry, counting only
vertical lines, and copying a half instead of reflecting it.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_uk_maths_y4_symmetry as uks
adopt(uks)
if hasattr(uks, 'R'): uks.R = random.Random(804170)
za_common.GRADE = "grade-4"



def build():
    sets, R = build_sets([
        ("Is it a line of symmetry?", [("run", uks.set_is_line, ("rnd",), 20)]),
        ("How many lines of symmetry?", [("run", uks.set_count, ("rnd",), 20)]),
        ("Turned shapes", [("run", uks.set_turned, ("rnd",), 20)]),
        ("Complete the shape", [("run", uks.set_grid, ("rnd",), 20)]),
        ("Symmetry around us", [("run", uks.set_world, ("rnd",), 20)]),
    ], 80417)
    finish(sets, R)
    body = lesson('<ul><li>A <b>line of symmetry</b> divides a shape into two halves that match exactly when folded.</li><li>A shape can have no line, one line or many lines of symmetry. A square has 4.</li><li>The line can be vertical, horizontal or diagonal.</li><li>To complete a symmetric shape, reflect each point to the same distance on the other side.</li></ul>',
        [example("Rectangle", ["fold across", "fold down"], "2 lines of symmetry")],
        [['Diagonal of a rectangle', 'The halves do not match when folded.'], ['Only vertical lines', 'Look for horizontal and diagonal lines too.'], ['Copying the half', 'Reflect it so it faces the other way.']])
    faq = [('What does CAPS Grade 4 say about symmetry?', 'Recognise, draw and describe line(s) of symmetry in 2-D shapes.'), ('How many lines of symmetry does a circle have?', 'Infinitely many.'), ('Can a shape have no symmetry?', 'Yes.'), ('How can learners check?', 'Fold the shape or use a mirror.')]
    make('symmetry', 17, 'Space and Shape (Geometry)', 'Grade 4: 3.3 Symmetry',
         'Recognise, draw and describe line(s) of symmetry in 2-D shapes.',
         'Line Symmetry in 2-D Shapes', 'Symmetry',
         'Free CAPS Grade 4 symmetry worksheets: lines of symmetry in 2-D shapes, counting lines of symmetry and completing symmetric shapes. 100 questions with memos.',
         'Fold on the line: the halves match.', 'Reflect each point the same distance.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
