# -*- coding: utf-8 -*-
"""
South Africa Grade 6 Maths (CAPS): Position and Movement: Grids, Coordinates and Maps (Grade 6: 3.5 Position and movement)
  python3 tools/gen_za_maths_g6_position_movement.py
Grid references and ordered pairs, compass directions, following directions and moving shapes on a grid (Australia
Year 3, Year 4 and Year 5 and UK Year 6 makers, first quadrant only).
Wrong answers come from real mistakes: reading the y-coordinate first, mixing up east and west, and counting the
starting square as a step.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_au_maths_y4_grid_references as aug
adopt(aug)
if isinstance(getattr(aug, 'R', None), random.Random): aug.R = random.Random(806250)
import gen_au_maths_y3_maps as aum
adopt(aum)
if isinstance(getattr(aum, 'R', None), random.Random): aum.R = random.Random(806251)
import gen_au_maths_y5_transformations as aut
adopt(aut)
if isinstance(getattr(aut, 'R', None), random.Random): aut.R = random.Random(806252)
import gen_uk_maths_y6_coordinates as ukc
adopt(ukc)
if isinstance(getattr(ukc, 'R', None), random.Random): ukc.R = random.Random(806253)
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
        ("Grid references", [("run", aug.set_refs, ("rnd", aug.People), 10, flat), ("run", aum.set_birdseye_refs, ("rnd", aum.People), 10, flat)]),
        ("Coordinates", [("run", aut.set_coords, ("rnd", aut.People), 20, flat)]),
        ("Compass directions", [("run", aug.set_compass, ("rnd", aug.People), 10, flat), ("run", aum.set_compass, ("rnd", aum.People), 10, flat)]),
        ("Follow directions", [("run", aug.set_follow, ("rnd", aug.People), 10, flat), ("run", aum.set_directions, ("rnd", aum.People), 10, flat)]),
        ("Move on a grid", [("run", aut.set_translate, ("rnd", aut.People), 10, flat), ("run", aug.set_pathways, ("rnd", aug.People), 10, flat)]),
    ], 80625)
    finish(sets, R)
    body = lesson('<ul><li>A grid reference names a square: letter (column) first, then number (row): D3.</li><li>A coordinate names a point: (x, y). Go across first, then up: (4, 2).</li><li>Compass directions: N, E, S, W and NE, NW, SE, SW in between.</li><li>Give directions with a direction and a number of squares.</li></ul>',
        [example("From (2, 3), move 4 right and 1 up", ["x: 2 + 4", "y: 3 + 1"], "(6, 4)")],
        [['y first', 'Across first, then up.'], ['East and west', 'East is on the right with north at the top.'], ['Counting the start', 'Count the moves only.']])
    faq = [('What does CAPS Grade 6 say about position and movement?', 'Locate positions on a grid with alphabetical and numerical grid references, and describe and follow directions to move between positions on a map or grid.'), ('Which comes first in (3, 5)?', '3, the number across.'), ('What is north-east?', 'Between north and east.'), ('Where are coordinates used?', 'On maps, in games and on graphs.')]
    make('position-and-movement', 25, 'Space and Shape (Geometry)', 'Grade 6: 3.5 Position and movement',
         'Locate positions on a grid with alphabetical and numerical grid references; locate and give directions to specified positions on a map or grid; describe movement between positions using compass directions.',
         'Position and Movement: Grids, Coordinates and Maps', 'Position and Movement',
         'Free CAPS Grade 6 position and movement worksheets: grid references, coordinates, compass directions and following directions. 100 questions with memos.',
         'Grid reference: letter, then number. Coordinate: across, then up.', 'Give a direction and a number of squares.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
