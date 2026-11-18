# -*- coding: utf-8 -*-
"""
Texas Grade 4 Math: Lines of Symmetry (TEKS 4.6B)
  python3 tools/gen_ustx_math_g4_lines_of_symmetry.py
Is it a line of symmetry, how many lines of symmetry, symmetry in letters, completing a picture on a grid, and
real-world pictures. The question makers come from the US Grade 4 symmetry unit with Texas names. Wrong answers
come from real mistakes: counting a diagonal of a rectangle as a line of symmetry and forgetting lines that are not
vertical or horizontal.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, build_sets, example, figure)
import gen_us_math_g4_symmetry as uss
adopt(uss)
tx_common.GRADE = "grade-4"


def build():
    sets, R = build_sets([
        ("Is it a line of symmetry?", [("run", uss.set_is_line, ("rnd",), 20)]),
        ("How many lines of symmetry?", [("run", uss.set_count, ("rnd",), 20)]),
        ("Symmetry in capital letters", [("run", uss.set_letters, ("rnd",), 20)]),
        ("Complete the picture on a grid", [("run", uss.set_grid, ("rnd",), 20)]),
        ("Pictures and word problems", [("run", uss.set_world, ("rnd",), 20)]),
    ], 64019)
    finish(sets, R)
    body = lesson('<ul><li>A <b>line of symmetry</b> folds a figure into two halves that match exactly.</li><li>A figure can have no lines of symmetry, one, or more than one. A square has 4; a rectangle has 2; a circle has infinitely many.</li><li>Check by imagining a fold: every point on one side must land on a matching point on the other side.</li></ul>',
        [example("How many lines of symmetry does a rectangle (not a square) have?", ["Fold up and down: the halves match.", "Fold across: the halves match.", "Fold on a diagonal: the corners do not meet."], "2"), example("Does the letter H have a horizontal line of symmetry?", ["The top half matches the bottom half."], "yes")],
        [['Counting the diagonals of a rectangle', 'A diagonal fold does not match the corners of a rectangle.'], ['Looking only for up-and-down lines', 'Check across and on the diagonals too.'], ['Saying a shape has 0 lines because it is turned', 'Turning does not change symmetry.']])
    faq = [('What does TEKS 4.6B ask?', 'Identify and draw one or more lines of symmetry, if they exist, for a two-dimensional figure.'), ('How many lines of symmetry does a square have?', '4: one up and down, one across, and two along the diagonals.'), ('Can a shape have no line of symmetry?', 'Yes. Many shapes, like most scalene triangles, have no line of symmetry.'), ('How do you complete a symmetric picture?', 'Each square on one side has a matching square the same distance from the line on the other side.')]
    make('lines-of-symmetry', 19, 'Geometry and Measurement', '4.6B',
         '4.6B identify and draw one or more lines of symmetry, if they exist, for a two-dimensional figure',
         'Lines of Symmetry', 'Lines of Symmetry',
         'Free Grade 4 symmetry worksheets for Texas TEKS 4.6B: is it a line of symmetry, how many lines of symmetry, letters, completing pictures on a grid and real-world pictures. 100 questions with answers.',
         'A line of symmetry folds a figure into two matching halves.', 'A square has 4 lines of symmetry, a rectangle 2, and some figures none.',
         body, faq, sets, seo_title='Grade 4 Lines of Symmetry Worksheets (TEKS 4.6B, STAAR)')


if __name__ == "__main__":
    build()
