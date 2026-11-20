# -*- coding: utf-8 -*-
"""
South Africa Grade 5 Maths (CAPS): Line Symmetry in 2-D Shapes and Patterns (Grade 5: 3.3 Symmetry)
  python3 tools/gen_za_maths_g5_symmetry.py
Lines of symmetry in shapes, letters and pictures, counting lines of symmetry and completing symmetric shapes on a
grid (US Grade 4, Singapore Primary 4 and Australia Year 4 makers).
Wrong answers come from real mistakes: taking any line through the middle as a line of symmetry, missing the
diagonal lines, and reflecting a shape the wrong way.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_us_math_g4_symmetry as uss
adopt(uss)
if isinstance(getattr(uss, 'R', None), random.Random): uss.R = random.Random(805180)
import gen_sg_maths_p4_symmetry as sgs
adopt(sgs)
if isinstance(getattr(sgs, 'R', None), random.Random): sgs.R = random.Random(805181)
import gen_au_maths_y4_symmetry as aus
adopt(aus)
if isinstance(getattr(aus, 'R', None), random.Random): aus.R = random.Random(805182)
za_common.GRADE = "grade-5"


import re as _re


def _txt(it):
    return _re.sub(r"<[^>]+>", " ", _re.sub(r"<svg.*?</svg>", " ", it["q"], flags=_re.S) + " " + " ".join(it["c"]) + " " + it["e"])


def _nums(it):
    return [int(x.replace(",", "").replace("\u00a0", "")) for x in _re.findall(r"(?<![\d.])\d[\d,\u00a0]*(?![.\d])", _txt(it)) if x.replace(",", "").replace("\u00a0", "").isdigit()]


def six(it):
    """whole numbers to 6 digits, no decimals, no negatives"""
    t = _txt(it)
    return all(n <= 999999 for n in _nums(it)) and not _re.search(r"\d\.\d|−\d", t)


def nodec(it):
    return not _re.search(r"\d\.\d|−\d", _txt(it))


def den12(it):
    ds = [int(d) for d in _re.findall(r"<span class='fd'>(\d+)</span>", it["q"] + " " + it["c"][it["a"]])]
    return all(d <= 12 for d in ds) and nodec(it)



def build():
    sets, R = build_sets([
        ("Is it a line of symmetry?", [("run", sgs.set_is_line, ("rnd",), 20)]),
        ("Count the lines of symmetry", [("run", uss.set_count, ("rnd",), 10), ("run", sgs.set_count, ("rnd",), 10)]),
        ("Letters and symbols", [("run", uss.set_letters, ("rnd",), 20)]),
        ("Complete the shape", [("run", sgs.set_grid, ("rnd",), 10), ("run", aus.set_grid, ("rnd",), 10)]),
        ("Symmetry around us", [("run", sgs.set_symmetric, ("rnd",), 10), ("run", uss.set_world, ("rnd",), 10)]),
    ], 80518)
    finish(sets, R)
    body = lesson('<ul><li>A line of symmetry folds a shape into two halves that match exactly.</li><li>Some shapes have more than one line of symmetry: a square has 4.</li><li>Check diagonal lines too.</li><li>To complete a symmetric shape, reflect each point the same distance on the other side of the line.</li></ul>',
        [example("A rectangle", ["across the middle", "down the middle", "not the diagonals"], "2 lines of symmetry")],
        [['Any line through the middle', 'The halves must match when folded.'], ['Missing diagonals', 'Try the diagonal lines.'], ['Wrong way', 'Count squares from the line.']])
    faq = [('What does CAPS Grade 5 say about symmetry?', 'Recognise, draw and describe line(s) of symmetry in 2-D shapes.'), ('Does a circle have lines of symmetry?', 'Yes, any line through the centre.'), ('How many lines does an equilateral triangle have?', '3.'), ('Is the letter A symmetric?', 'Yes, it has 1 vertical line of symmetry.')]
    make('symmetry', 18, 'Space and Shape (Geometry)', 'Grade 5: 3.3 Symmetry',
         'Recognise, draw and describe line(s) of symmetry in 2-D shapes.',
         'Line Symmetry in 2-D Shapes and Patterns', 'Symmetry',
         'Free CAPS Grade 5 symmetry worksheets: lines of symmetry in shapes, letters and pictures, and completing symmetric shapes. 100 questions with memos.',
         'A line of symmetry makes two matching halves.', 'Check the diagonals too.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
