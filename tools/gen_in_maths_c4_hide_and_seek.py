# -*- coding: utf-8 -*-
"""India Class 4 Maths, Maths Mela Chapter 2: Hide and Seek (Position, Maps and Directions)
Grid references, compass directions, following and describing paths, and bird's-eye views (AU Year 4 and Year 3 set makers)."""
from in_prim import unit, mod, rn, co, le

gr = mod("gen_au_maths_y4_grid_references", 604020)
mp = mod("gen_au_maths_y3_maps", 604021)
unit(4, "hide-and-seek", 2, "G", 2, "Hide and Seek", "Position, Maps and Directions", "maps and position",
     "Spatial understanding: describing position, reading simple maps from above (top view), using directions and grid references to locate and hide objects (summary of NCERT Maths Mela Class 4)",
     "Class 4 Hide and Seek worksheet (Maths Mela Chapter 2): grid references, compass directions, paths and maps from above. 100 questions with answers.",
     "Read across first, then up (B3).", "North is up on most maps.",
     "<ul><li>A <b>grid reference</b> such as C4 gives the column, then the row.</li><li>Compass directions: North, South, East, West.</li><li>A map shows a place as seen from above (a bird's-eye view).</li></ul>",
     [('Start at the gate, go 2 squares east and 1 north.', ['Move across, then up'], 'You reach the well')],
     [['Reading the row before the column', 'Letters across first, then numbers up.'], ['Mixing up east and west', 'Never Eat Shredded Wheat: N, E, S, W clockwise.']],
     [("What is a bird's-eye view?", 'How something looks from straight above, as on a map.'), ('What is a grid reference?', 'A letter and a number that name one square on a map.')],
     [('Grid references', [rn(gr, "set_refs", 20)]),
      ('Compass directions', [rn(gr, "set_compass", 20)]),
      ('Follow the path', [rn(gr, "set_follow", 20)]),
      ('Views from above', [rn(mp, "set_birdseye_refs", 10), rn(mp, "set_read", 10)]),
      ('Maps in real life', [rn(gr, "set_pathways", 10), rn(gr, "set_real", 10)])], 60402)
