# -*- coding: utf-8 -*-
"""
Philippines Grade 4 Math (MATATAG): Line Symmetry: Identifying and Completing Symmetric Figures (Grade 4: Measurement and Geometry)
  python3 tools/gen_ph_math_g4_line_symmetry.py
Identifying lines of symmetry, counting them, letters and real objects, symmetric figures on a grid (US Grade 4
makers), and completing a figure that is symmetric with respect to a line (Singapore Primary 4 maker).
Wrong answers come from real mistakes: taking a diagonal of a rectangle as a line of symmetry, counting only straight
up-and-down lines, and copying the half instead of flipping it.
"""
import ph_common
from ph_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, peso, words)
import random
import gen_us_math_g4_symmetry as uss
adopt(uss)
if hasattr(uss, 'R'): uss.R = random.Random(704190)
import gen_sg_maths_p4_symmetry as sgs
adopt(sgs)
if hasattr(sgs, 'R'): sgs.R = random.Random(704191)
ph_common.GRADE = "grade-4"



def build():
    sets, R = build_sets([
        ("Is it a line of symmetry?", [("run", uss.set_is_line, ("rnd",), 20)]),
        ("How many lines of symmetry?", [("run", uss.set_count, ("rnd",), 20)]),
        ("Letters and objects", [("run", uss.set_letters, ("rnd",), 10), ("run", uss.set_world, ("rnd",), 10)]),
        ("Symmetry on a grid", [("run", uss.set_grid, ("rnd",), 20)]),
        ("Complete the symmetric figure", [("run", sgs.set_symmetric, ("rnd",), 20)]),
    ], 70419)
    finish(sets, R)
    body = lesson('<ul><li>A figure has <b>line symmetry</b> if you can fold it along a line so that the two halves match exactly.</li><li>The fold line is the <b>line of symmetry</b>. A figure can have no line, one line or many lines of symmetry.</li><li>A rectangle has 2 lines of symmetry; its diagonals are not lines of symmetry.</li><li>To complete a symmetric figure, flip each point to the other side: the same distance from the line.</li></ul>',
        [example("Lines of symmetry of a square", ["up and down, across", "the two diagonals"], "4")],
        [['Diagonals of a rectangle', 'Folding along a diagonal does not match the halves.'], ['Only up-and-down lines', 'Lines across and diagonal lines count too.'], ['Copying the half', 'Flip it, so it faces the other way.']])
    faq = [('What does MATATAG Math 4 ask about symmetry?', 'Identify symmetry with respect to a line, and complete a figure that is symmetric with respect to a line.'), ('How can I check a line of symmetry?', 'Fold the paper or use a mirror on the line.'), ('How many lines of symmetry does a circle have?', 'Infinitely many: every line through the center.'), ('Does the letter N have line symmetry?', 'No.')]
    make('line-symmetry', 19, 'Measurement and Geometry', 'Grade 4: Measurement and Geometry',
         'Identify symmetry with respect to a line; complete a figure that is symmetric with respect to a line.',
         'Line Symmetry: Identifying and Completing Symmetric Figures', 'Line Symmetry',
         'Free Grade 4 line symmetry worksheets for the DepEd MATATAG curriculum: lines of symmetry, letters, objects and completing symmetric figures. 100 questions with answers.',
         'Fold on the line: the two halves match.', 'Each point flips to the same distance on the other side.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
