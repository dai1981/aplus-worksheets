# -*- coding: utf-8 -*-
"""
India Class 7 Maths, Ganita Prakash Part 1, Chapter 5: Parallel and Intersecting Lines
  python3 tools/gen_in_maths_c7_parallel_and_intersecting_lines.py
Intersecting lines: linear pairs and vertically opposite angles; parallel lines cut by a transversal: corresponding,
alternate and co-interior (interior angles on the same side) angles, finding angles and checking whether lines are
parallel. Reuses the SG Secondary 1, UK Year 7 and AU Year 7 makers with figures.
Wrong answers come from real mistakes: corresponding angles taken as supplementary, co-interior angles taken as equal,
and a linear pair taken as 90°.
"""
import random
from in_common import unit, T, adopt, gb
import gen_sg_maths_s1_parallel_lines_and_polygons as sg
import gen_uk_maths_y7_angles as uk
import gen_au_maths_y7_angles_and_parallel_lines as au

R = random.Random(907005)
for m in (sg, uk, au):
    adopt(m, R)

FACTS = [("When two lines intersect, the vertically opposite angles are", "equal", ["supplementary", "complementary", "always 90°"]),
         ("Two angles that form a linear pair add up to", "180°", ["90°", "360°", "they are equal"]),
         ("If a transversal cuts two parallel lines, corresponding angles are", "equal", ["supplementary", "complementary", "unequal"]),
         ("If a transversal cuts two parallel lines, alternate angles are", "equal", ["supplementary", "complementary", "unequal"]),
         ("If a transversal cuts two parallel lines, interior angles on the same side add up to", "180°", ["90°", "360°", "they are equal"]),
         ("Two lines in a plane that never meet are", "parallel", ["perpendicular", "intersecting", "transversals"]),
         ("A line that cuts two or more lines at different points is a", "transversal", ["parallel line", "ray", "diagonal"]),
         ("Two lines that meet at a right angle are", "perpendicular", ["parallel", "skew", "a linear pair"]),
         ("If corresponding angles made by a transversal are equal, the lines are", "parallel", ["perpendicular", "intersecting at 45°", "the same line"])]


def one_fact(r):
    q, a, w = r.choice(FACTS)
    return T(q + " ___.", a, w, "<b>%s</b>." % a)


def main():
    unit(7, 1, 5, "parallel-and-intersecting-lines", 5, "G", "Parallel and Intersecting Lines: Angles and Transversals", "parallel and intersecting lines",
         "Intersecting lines, linear pairs and vertically opposite angles; parallel lines and transversals; corresponding, alternate and interior angles; checking for parallel lines (summary of NCERT Ganita Prakash Class 7)",
         "Class 7 Parallel and Intersecting Lines worksheet (Ganita Prakash Part 1, Chapter 5): vertically opposite angles, linear pairs, corresponding, alternate and co-interior angles. 100 questions with answers.",
         "Corresponding and alternate angles are equal", "Interior angles on the same side add up to 180°.",
         "<p>When two lines cross, <b>vertically opposite angles</b> are equal and angles next to each other form a <b>linear pair</b> (add up to 180°).</p>"
         "<p>A <b>transversal</b> crossing two <b>parallel</b> lines makes equal <b>corresponding</b> angles (same position, F-shape) and equal <b>alternate</b> angles (Z-shape). Interior angles on the same side (C-shape) add up to 180°.</p>",
         [("Two lines cross; one angle is 65°. Find the angle next to it.", ["Linear pair: 180° − 65°"], "115°"),
          ("Alternate angles on parallel lines: one is 48°. Find the other.", ["Alternate angles are equal"], "48°")],
         ["Taking corresponding angles as supplementary.", "Taking interior angles on the same side as equal.", "Using 90° for a linear pair instead of 180°."],
         [("What are vertically opposite angles?", "The opposite angles formed when two lines cross. They are always equal."),
          ("What angles are formed when a transversal cuts two parallel lines?", "Corresponding angles (equal), alternate angles (equal) and interior angles on the same side (add up to 180°)."),
          ("How can you check whether two lines are parallel?", "If a transversal makes equal corresponding or alternate angles, the lines are parallel.")],
         [("Linear pairs", [(gb(uk.one_line), 14), (one_fact, 6)]),
          ("Vertically opposite angles", [(gb(uk.one_vopp), 12), (gb(uk.one_vopp2), 8)]),
          ("Naming angle pairs", [(gb(sg.one_name), 12), (gb(au.one_name), 8)]),
          ("Finding angles on parallel lines", [(gb(sg.one_parallel), 10), (gb(au.one_parallel2), 10)]),
          ("Algebra and checking for parallel lines", [(gb(au.one_alg), 12), (gb(au.one_check), 8)])], R)


if __name__ == "__main__":
    main()
