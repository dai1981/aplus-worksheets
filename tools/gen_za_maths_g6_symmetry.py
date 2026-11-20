# -*- coding: utf-8 -*-
"""
South Africa Grade 6 Maths (CAPS): Line Symmetry in 2-D Shapes, Letters and Patterns (Grade 6: 3.3 Symmetry)
  python3 tools/gen_za_maths_g6_symmetry.py
Lines of symmetry in shapes, letters and pictures, counting lines of symmetry and completing symmetric shapes on a
grid (BC Grade 4 and UK Year 4 makers).
Wrong answers come from real mistakes: taking any line through the middle as a line of symmetry, missing the
diagonal lines, and reflecting a shape the wrong way.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_cabc_math_g4_symmetry as cbs
adopt(cbs)
if isinstance(getattr(cbs, 'R', None), random.Random): cbs.R = random.Random(806230)
import gen_uk_maths_y4_symmetry as uks
adopt(uks)
if isinstance(getattr(uks, 'R', None), random.Random): uks.R = random.Random(806231)
za_common.GRADE = "grade-6"


import re as _re


def _txt(it):
    return _re.sub(r"<[^>]+>", " ", _re.sub(r"<svg.*?</svg>", " ", it["q"], flags=_re.S) + " " + " ".join(it["c"]) + " " + it["e"])


def _nums(it):
    return [int(x.replace(",", "").replace("\u00a0", "")) for x in _re.findall(r"(?<![\d.])\d[\d,\u00a0]*(?![.\d])", _txt(it)) if x.replace(",", "").replace("\u00a0", "").isdigit()]


def noneg(it):
    return not _re.search(r"(?<![\d)] )[−-]\d", _txt(it)) and "negative" not in _txt(it).lower()


def nine(it):
    """whole numbers to 9 digits, no negatives"""
    return all(n <= 999999999 for n in _nums(it)) and noneg(it)


def dec3(it):
    """decimals with at most 3 places, no negatives"""
    return noneg(it) and not _re.search(r"\d\.\d{4}", _txt(it))


def nodec(it):
    return noneg(it) and not _re.search(r"\d\.\d", _txt(it))


def flat(it):
    """first quadrant only: no negative numbers in the text or the picture"""
    return nodec(it) and "−" not in it["q"] and "-1" not in it["q"]


def nomean(it):
    return dec3(it) and not _re.search(r"\bmean\b", _txt(it))


def den12(it):
    ds = [int(d) for d in _re.findall(r"<span class='fd'>(\d+)</span>", it["q"] + " " + it["c"][it["a"]])]
    return all(d <= 12 or d in (20, 25, 50, 100) for d in ds) and nodec(it)



def build():
    sets, R = build_sets([
        ("Is it a line of symmetry?", [("run", cbs.set_is_line, ("rnd",), 20)]),
        ("Count the lines of symmetry", [("run", cbs.set_count, ("rnd",), 10), ("run", uks.set_count, ("rnd",), 10)]),
        ("Letters and symbols", [("run", cbs.set_letters, ("rnd",), 20)]),
        ("Complete the shape", [("run", cbs.set_grid, ("rnd",), 10), ("run", uks.set_grid, ("rnd",), 10)]),
        ("Symmetry around us", [("run", cbs.set_world, ("rnd",), 10), ("run", uks.set_world, ("rnd",), 10)]),
    ], 80623)
    finish(sets, R)
    body = lesson('<ul><li>A line of symmetry folds a shape into two halves that match exactly.</li><li>A regular polygon has as many lines of symmetry as sides: a regular hexagon has 6.</li><li>Check the diagonal lines too.</li><li>To complete a symmetric shape, reflect each point the same distance on the other side of the line.</li></ul>',
        [example("A regular pentagon", ["one line through each vertex"], "5 lines of symmetry")],
        [['Any line through the middle', 'The halves must match when folded.'], ['Missing diagonals', 'Try the diagonal lines.'], ['Wrong way', 'Count squares from the line.']])
    faq = [('What does CAPS Grade 6 say about symmetry?', 'Recognise, draw and describe line(s) of symmetry in 2-D shapes.'), ('How many lines does a rhombus have?', '2, along its diagonals.'), ('Does a parallelogram have lines of symmetry?', 'Usually none.'), ('How many does a circle have?', 'Very many: any line through the centre.')]
    make('symmetry', 23, 'Space and Shape (Geometry)', 'Grade 6: 3.3 Symmetry',
         'Recognise, draw and describe line(s) of symmetry in 2-D shapes.',
         'Line Symmetry in 2-D Shapes, Letters and Patterns', 'Symmetry',
         'Free CAPS Grade 6 symmetry worksheets: lines of symmetry in shapes, letters and pictures, and completing symmetric shapes. 100 questions with memos.',
         'A line of symmetry makes two matching halves.', 'A regular polygon: as many lines as sides.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
