# -*- coding: utf-8 -*-
"""
South Africa Grade 5 Maths (CAPS): Transformations: Slides, Flips, Turns and Tessellations (Grade 5: 3.4 Transformations)
  python3 tools/gen_za_maths_g5_transformations.py
Translations (slides), reflections (flips) and rotations (turns), naming the transformation, and tessellations
(BC Grade 5, UK Year 5 and Australia Year 6 makers).
Wrong answers come from real mistakes: mixing up a flip and a turn, counting squares from the wrong corner, and
thinking any shape tessellates.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_cabc_math_g5_transformations as cbt
adopt(cbt)
if isinstance(getattr(cbt, 'R', None), random.Random): cbt.R = random.Random(805190)
import gen_uk_maths_y5_reflection_translation as ukr
adopt(ukr)
if isinstance(getattr(ukr, 'R', None), random.Random): ukr.R = random.Random(805191)
import gen_au_maths_y6_tessellations as aut
adopt(aut)
if isinstance(getattr(aut, 'R', None), random.Random): aut.R = random.Random(805192)
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
        ("Slides", [("run", cbt.set_slide, ("rnd", cbt.People), 10, nodec), ("run", ukr.set_describe, ("rnd", ukr.People), 10, nodec)]),
        ("Flips", [("run", cbt.set_flip, ("rnd", cbt.People), 10, nodec), ("run", ukr.set_reflect, ("rnd", ukr.People), 10, nodec)]),
        ("Turns", [("run", cbt.set_turn, ("rnd", cbt.People), 20, nodec)]),
        ("Which transformation?", [("run", cbt.set_which, ("rnd", cbt.People), 10, nodec), ("run", ukr.set_which, ("rnd", ukr.People), 10, nodec)]),
        ("Tessellations", [("run", aut.set_identify, ("rnd", aut.People), 10, nodec), ("run", aut.set_which, ("rnd", aut.People), 10, nodec)]),
    ], 80519)
    finish(sets, R)
    body = lesson('<ul><li>A <b>translation</b> (slide) moves a shape without turning or flipping it.</li><li>A <b>reflection</b> (flip) makes a mirror image across a line.</li><li>A <b>rotation</b> (turn) turns a shape around a point.</li><li>The shape stays the same size in all three. A <b>tessellation</b> covers a surface with shapes and no gaps or overlaps.</li></ul>',
        [example("The shape faces the other way across a line", ["mirror image"], "a reflection")],
        [['Flip or turn?', 'A flip makes a mirror image.'], ['Wrong corner', 'Count from the same corner.'], ['Every shape tessellates', 'Circles leave gaps.']])
    faq = [('What does CAPS Grade 5 say about transformations?', 'Recognise, describe and perform translations, reflections and rotations with 2-D shapes and 3-D objects, and make tessellations.'), ('Does a translation change the size?', 'No.'), ('Which shapes tessellate?', 'Squares, rectangles, equilateral triangles and regular hexagons.'), ('Where do we see tessellations?', 'In tiles, paving and bricks.')]
    make('transformations', 19, 'Space and Shape (Geometry)', 'Grade 5: 3.4 Transformations',
         'Draw composite shapes by translating, reflecting and rotating; describe patterns in terms of line symmetry, translation, reflection and rotation; tessellate 2-D shapes.',
         'Transformations: Slides, Flips, Turns and Tessellations', 'Transformations',
         'Free CAPS Grade 5 transformations worksheets: slides, flips, turns, naming transformations and tessellations. 100 questions with memos.',
         'Slide, flip, turn: the shape stays the same size.', 'A tessellation has no gaps or overlaps.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
