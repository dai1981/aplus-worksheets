# -*- coding: utf-8 -*-
"""
South Africa Grade 4 Maths (CAPS): Position and Movement: Grid References and Maps (Grade 4: 3.6 Position and movement)
  python3 tools/gen_za_maths_g4_position_movement.py
Alpha-numeric grid references, compass directions, following directions, pathways on a map and real maps (Australia
Year 4 makers with South African names).
Wrong answers come from real mistakes: reading the number before the letter, mixing up east and west, and counting
the starting square as a step.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_au_maths_y4_grid_references as aug
adopt(aug)
if hasattr(aug, 'R'): aug.R = random.Random(804200)
za_common.GRADE = "grade-4"



def build():
    sets, R = build_sets([
        ("Grid references", [("run", aug.set_refs, ("rnd", aug.People), 20)]),
        ("Compass directions", [("run", aug.set_compass, ("rnd", aug.People), 20)]),
        ("Follow the directions", [("run", aug.set_follow, ("rnd", aug.People), 20)]),
        ("Pathways", [("run", aug.set_pathways, ("rnd", aug.People), 20)]),
        ("Maps", [("run", aug.set_real, ("rnd", aug.People), 20)]),
    ], 80420)
    finish(sets, R)
    body = lesson('<ul><li>A grid reference gives the column letter, then the row number: B4.</li><li>Directions: North (up on the map), South, East (right) and West (left).</li><li>Count the squares you move, not the square you start on.</li><li>Use grid references to find places on maps of towns, parks and schools.</li></ul>',
        [example("Start at C2, move 2 squares east", ["C → D → E"], "E2")],
        [['Number first', 'Letter (column) first, then number (row).'], ['East or west?', 'On a map, east is to the right.'], ['Counting the start', 'Count only the moves.']])
    faq = [('What does CAPS Grade 4 say about position and movement?', 'Locate objects on a grid with alpha-numeric grid references, and locate positions on a map, describing routes.'), ('What is an alpha-numeric grid?', 'Columns labelled with letters and rows with numbers.'), ('Where are grid references used?', 'Street maps and atlases.'), ('Why learn compass directions?', 'To describe where places are.')]
    make('position-and-movement', 20, 'Space and Shape (Geometry)', 'Grade 4: 3.6 Position and movement',
         'Locate objects on an alpha-numeric grid; describe and follow directions on maps; locate positions and describe routes on maps.',
         'Position and Movement: Grid References and Maps', 'Position and Movement',
         'Free CAPS Grade 4 position and movement worksheets: alpha-numeric grid references, compass directions, following directions and maps. 100 questions with memos.',
         'Letter first, then number: B4.', 'East is right, west is left on a map.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
