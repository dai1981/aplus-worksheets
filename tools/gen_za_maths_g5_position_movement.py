# -*- coding: utf-8 -*-
"""
South Africa Grade 5 Maths (CAPS): Position and Movement: Grids, Maps and Directions (Grade 5: 3.6 Position and movement)
  python3 tools/gen_za_maths_g5_position_movement.py
Grid references, compass directions, following and giving directions on a map, and maps of real places (Australia
Year 3 and Year 4 makers with South African names and places).
Wrong answers come from real mistakes: reading the row before the column, mixing up east and west, and counting the
starting square as a step.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_au_maths_y4_grid_references as aug
adopt(aug)
if isinstance(getattr(aug, 'R', None), random.Random): aug.R = random.Random(805210)
import gen_au_maths_y3_maps as aum
adopt(aum)
if isinstance(getattr(aum, 'R', None), random.Random): aum.R = random.Random(805211)
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
        ("Grid references", [("run", aug.set_refs, ("rnd", aug.People), 20, nodec)]),
        ("Compass directions", [("run", aum.set_compass, ("rnd", aum.People), 10, nodec), ("run", aug.set_compass, ("rnd", aug.People), 10, nodec)]),
        ("Follow directions", [("run", aug.set_follow, ("rnd", aug.People), 10, nodec), ("run", aum.set_directions, ("rnd", aum.People), 10, nodec)]),
        ("Paths on a map", [("run", aug.set_pathways, ("rnd", aug.People), 20, nodec)]),
        ("Maps around us", [("run", aum.set_read, ("rnd", aum.People), 10, nodec), ("run", aug.set_real, ("rnd", aug.People), 10, nodec)]),
    ], 80521)
    finish(sets, R)
    body = lesson('<ul><li>A grid reference names a square by its column letter and row number: C4.</li><li>Read the letter along the bottom first, then the number up the side.</li><li>Compass directions: north (N), east (E), south (S), west (W). North-east is between north and east.</li><li>Directions on a map: say the direction and the number of squares.</li></ul>',
        [example("From B2, go 3 squares east and 2 squares north", ["B → C, D, E", "2 → 3, 4"], "E4")],
        [['Row first', 'Letter first, then number.'], ['East and west', 'East is on the right of a map with north at the top.'], ['Counting the start', 'Count the moves, not the starting square.']])
    faq = [('What does CAPS Grade 5 say about position and movement?', 'Locate positions on a grid with alphabetical and numerical grid references, and describe the movement between positions on a map or grid.'), ('Which comes first in B4?', 'The letter (column), then the number (row).'), ('Where is south-west?', 'Between south and west.'), ('Why use grid references?', 'To find places on a map quickly.')]
    make('position-and-movement', 21, 'Space and Shape (Geometry)', 'Grade 5: 3.6 Position and movement',
         'Locate positions on a grid with alphabetical and numerical grid references; locate and give directions to specified positions on a map or grid; describe the movement between positions.',
         'Position and Movement: Grids, Maps and Directions', 'Position and Movement',
         'Free CAPS Grade 5 position and movement worksheets: grid references, compass directions and following directions on maps. 100 questions with memos.',
         'Letter first, then number.', 'Give the direction and the number of squares.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
