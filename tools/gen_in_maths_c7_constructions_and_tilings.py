# -*- coding: utf-8 -*-
"""
India Class 7 Maths, Ganita Prakash Part 2, Chapter 6: Constructions and Tilings
  python3 tools/gen_in_maths_c7_constructions_and_tilings.py
Angles of regular polygons (interior and exterior), the angle sum of a polygon, angles meeting at a point in a tiling,
which regular polygons tile the plane, and combinations of shapes that fit around a point.
Wrong answers come from real mistakes: the angle sum taken as n × 180°, the exterior angle confused with the interior
angle, and pentagons thought to tile.
"""
import random
from in_common import unit, T, QN, adopt, gb
import gen_sg_maths_s1_parallel_lines_and_polygons as pg

R = random.Random(907014)
adopt(pg, R)
REG = {3: ("equilateral triangle", 60), 4: ("square", 90), 5: ("regular pentagon", 108), 6: ("regular hexagon", 120), 8: ("regular octagon", 135), 10: ("regular decagon", 144), 12: ("regular dodecagon", 150)}


def one_tile(r):
    kind = r.choice(["count", "which", "not", "mix", "mix", "can", "can", "point", "point", "point"])
    if kind == "can":
        n = r.choice(list(REG))
        name, a = REG[n]
        yes = 360 % a == 0
        return T("Can %ss alone tile a floor with no gaps or overlaps?" % name, "Yes" if yes else "No", ["No" if yes else "Yes", "Only if they are large", "Only on a round floor"],
                 "Each angle is %d°, and 360° ÷ %d° %s a whole number: <b>%s</b>." % (a, a, "is" if yes else "is not", "Yes" if yes else "No"))
    if kind == "point":
        k = r.randint(2, 4)
        angs = [r.randint(40, 150) for _ in range(k)]
        if sum(angs) >= 340:
            return None
        return QN("In a tiling, %d shapes meet at a point with angles %s. One more shape completes the point. What is its angle?" % (k + 1, ", ".join("%d°" % a for a in angs)),
                  360 - sum(angs), [180 - sum(angs) if sum(angs) < 170 else 360 - sum(angs) + 20, sum(angs), 360 - sum(angs) - 10], "360° − %d° = <b>%d°</b>." % (sum(angs), 360 - sum(angs)), unit="°")
    if kind == "count":
        n = r.choice([3, 4, 6])
        name, a = REG[n]
        return QN("How many %ss fit around a point in a tiling (each angle %d°)?" % (name, a), 360 // a, [n, 360 // a + 1, 360 // a * 2], "360° ÷ %d° = <b>%d</b>." % (a, 360 // a))
    if kind == "which":
        n = r.choice([3, 4, 6])
        return T("Which regular polygon can tile a floor on its own, with no gaps?", REG[n][0].capitalize(), [REG[m][0].capitalize() for m in r.sample([5, 8, 10, 12], 3)],
                 "Its angle %d° divides 360° exactly: <b>%s</b>." % (REG[n][1], REG[n][0]))
    if kind == "not":
        n = r.choice([5, 8, 10])
        name, a = REG[n]
        return T("Why can't %ss tile a floor on their own?" % name, "%d° does not divide 360° exactly" % a, ["They have too many sides", "Their sides are not equal", "They have no right angles"],
                 "360° ÷ %d° is not a whole number, so gaps are left: <b>%d° does not divide 360° exactly</b>." % (a, a))
    combo = r.choice([((8, 8, 4), "square"), ((6, 6, 3, 3), "triangle"), ((12, 12, 3), "triangle"), ((6, 4, 4, 3), "triangle"), ((4, 4, 3, 3), "triangle"), ((6, 6, 6), "hexagon")])
    shapes, last = combo
    known = shapes[:-1]
    s = sum(REG[n][1] for n in known)
    return QN("At a point in a tiling there are %s. One more shape fills the gap. What angle is needed?" % ", ".join("a %s" % REG[n][0] for n in known), 360 - s, [180 - s if 180 > s else 360 - s + 30, s, 360 - s + 10],
              "360° − %d° = <b>%d°</b>, which is a %s." % (s, 360 - s, REG[shapes[-1]][0]), unit="°")


def main():
    unit(7, 2, 6, "constructions-and-tilings", 14, "G", "Constructions and Tilings: Polygon Angles and Tessellations", "constructions and tilings",
         "Constructing regular polygons, the angle sum of polygons, interior and exterior angles of regular polygons, and tilings (tessellations) of the plane (summary of NCERT Ganita Prakash Class 7)",
         "Class 7 Constructions and Tilings worksheet (Ganita Prakash Part 2, Chapter 6): angle sum of polygons, regular polygon angles, which shapes tile and angles at a point. 100 questions with answers.",
         "Angles meeting at a point in a tiling add up to 360°", "Angle sum of an n-sided polygon = (n − 2) × 180°.",
         "<p>A polygon with n sides splits into n − 2 triangles, so its angles add up to <b>(n − 2) × 180°</b>. In a regular polygon each interior angle is this ÷ n, and each exterior angle is 360° ÷ n.</p>"
         "<p>In a <b>tiling</b>, the angles that meet at a point add up to 360°. Only equilateral triangles (60°), squares (90°) and regular hexagons (120°) tile on their own.</p>",
         [("Find each interior angle of a regular octagon.", ["(8 − 2) × 180° = 1,080°", "1,080° ÷ 8"], "135°"),
          ("Two regular octagons meet at a point. What else fits?", ["360° − 270° = 90°"], "A square")],
         ["Using n × 180° for the angle sum.", "Mixing up interior and exterior angles.", "Thinking regular pentagons can tile a floor."],
         [("What is the angle sum of a polygon?", "(n − 2) × 180° for an n-sided polygon."),
          ("Which regular polygons tile the plane?", "Only equilateral triangles, squares and regular hexagons, because 60°, 90° and 120° divide 360° exactly."),
          ("What is the exterior angle of a regular polygon?", "360° ÷ number of sides.")],
         [("Angle sum of polygons", [(gb(pg.one_sum), 20)]),
          ("Angles of regular polygons", [(gb(pg.one_regular), 20)]),
          ("Finding the number of sides", [(gb(pg.one_sides), 20)]),
          ("Tilings", [(one_tile, 20)]),
          ("Mixed problems", [(one_tile, 8), (gb(pg.one_regular), 6), (gb(pg.one_sum), 6)])], R)


if __name__ == "__main__":
    main()
