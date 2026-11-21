# -*- coding: utf-8 -*-
"""India Class 5 Maths, Maths Mela Chapter 14: Maps and Locations (Maps, Coordinates and Directions)
Reading and plotting points on a grid, coordinates in real maps, directions and map scales (US Grade 5, UK Year 4, AU Year 5 set makers and own scale maker)."""
from in_prim import unit, mod, rn, co, le
from in_prim import mcq, Kid


def one_scale(r):
    s = r.choice([2, 3, 5, 10, 20, 25, 50])
    d = r.randint(2, 12)
    places = r.sample(["Jaipur", "Ajmer", "Pushkar", "Kota", "Udaipur", "Bikaner", "Jodhpur", "Alwar"], 2)
    if r.random() < 0.6:
        return mcq("On a map, 1 cm stands for %d km. %s and %s are %d cm apart on the map. How far apart are they really?" % (s, places[0], places[1], d), "%d km" % (s * d),
                   ["%d km" % (s + d), "%d km" % d, "%d km" % (s * d * 10)], "%d × %d = <b>%d km</b>." % (d, s, s * d))
    return mcq("On a map, 1 cm stands for %d km. Two villages are %d km apart. How far apart are they on the map?" % (s, s * d), "%d cm" % d,
               ["%d cm" % (s * d), "%d cm" % (s * d + s), "%d cm" % (d + s)], "%d ÷ %d = <b>%d cm</b>." % (s * d, s, d))
us = mod("gen_us_math_g5_coordinate_plane", 605140)
uk = mod("gen_uk_maths_y4_coordinates", 605141)
unit(5, "maps-and-locations", 14, "G", 14, "Maps and Locations", "Maps, Coordinates and Directions", "maps and locations",
     "Maps and locations: reading maps, using directions and grids to locate places, and understanding a simple map scale (summary of NCERT Maths Mela Class 5)",
     "Class 5 Maps and Locations worksheet (Maths Mela Chapter 14): grids, coordinates, directions and map scales. 100 questions with answers.",
     "Across first, then up: (3, 5).", "Scale: 1 cm on the map = 2 km.",
     "<ul><li>A point on a grid is written (across, up).</li><li>A map <b>scale</b> tells the real distance: if 1 cm = 5 km, then 4 cm = 20 km.</li></ul>",
     [('On a map 1 cm = 3 km. Two towns are 6 cm apart.', ['6 × 3'], '18 km')],
     [['Reading up before across', 'Across first, then up.'], ['Forgetting to use the scale', 'Multiply the map distance by the scale.']],
     [('What is a coordinate?', 'A pair of numbers that gives the position of a point on a grid.'), ('What is a map scale?', 'It shows how map distances match real distances.')],
     [('Read a point', [rn(us, "set_read", 10), rn(uk, "set_read", 10)]),
      ('Plot a point', [rn(us, "set_plot", 10), rn(uk, "set_plot", 10)]),
      ('Move on a grid', [rn(uk, "set_translate", 20)]),
      ('Map scales', [co(one_scale, 20)]),
      ('Maps in real life', [rn(us, "set_real", 10), rn(uk, "set_real", 10)])], 60514)
