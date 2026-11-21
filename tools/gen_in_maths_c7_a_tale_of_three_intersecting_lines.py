# -*- coding: utf-8 -*-
"""
India Class 7 Maths, Ganita Prakash Part 1, Chapter 7: A Tale of Three Intersecting Lines
  python3 tools/gen_in_maths_c7_a_tale_of_three_intersecting_lines.py
Triangles: the triangle inequality (can these lengths make a triangle?), the range of the third side, the angle sum
property, exterior angles, equilateral and isosceles triangles, and classifying triangles by sides and angles.
Wrong answers come from real mistakes: allowing a + b = c, the angle sum taken as 360°, the exterior angle taken as
the sum of all three angles, and the base angles of an isosceles triangle found as 180° − apex.
"""
import random
from in_common import unit, T, QN, adopt, gb
import gen_au_maths_y7_angle_sum_of_triangles_and_polygons as au

R = random.Random(907007)
adopt(au, R)


def one_ineq(r):
    kind = r.choice(["can", "can", "range", "range"])
    if kind == "can":
        while True:
            a, b, c = sorted(r.sample(range(2, 25), 3))
            ok = a + b > c
            if r.random() < 0.5 or not ok:
                break
        if r.random() < 0.3:
            c = a + b
            ok = False
        ans = "Yes" if ok else "No"
        return T("Can %d cm, %d cm and %d cm be the sides of a triangle?" % (a, b, c), ans, ["No" if ok else "Yes", "Only if it is right-angled", "Only if two sides are equal"],
                 "%d + %d = %d, which is %s %d, so <b>%s</b>." % (a, b, a + b, "greater than" if ok else ("equal to" if a + b == c else "less than"), c, ans.lower()))
    a, b = r.sample(range(3, 20), 2)
    lo, hi = abs(a - b), a + b
    return T("Two sides of a triangle are %d cm and %d cm. Which length could the third side be?" % (a, b), "%d cm" % r.randint(lo + 1, hi - 1),
             ["%d cm" % lo, "%d cm" % hi, "%d cm" % (hi + r.randint(1, 5))], "The third side must be between %d − %d = %d and %d + %d = %d (not equal to either)." % (max(a, b), min(a, b), lo, a, b, hi))


def one_iso(r):
    kind = r.choice(["base", "apex", "equi", "class", "class"])
    if kind == "base":
        a = r.choice(range(20, 160, 2))
        return QN("An isosceles triangle has an apex angle of %d°. Find each base angle." % a, (180 - a) // 2, [180 - a, a, 90 - a if 90 - a > 0 else a // 2], "(180° − %d°) ÷ 2 = <b>%d°</b>." % (a, (180 - a) // 2), unit="°")
    if kind == "apex":
        b = r.randint(25, 85)
        return QN("Each base angle of an isosceles triangle is %d°. Find the third angle." % b, 180 - 2 * b, [180 - b, b, 90 - b if 90 - b > 0 else 2 * b], "180° − 2 × %d° = <b>%d°</b>." % (b, 180 - 2 * b), unit="°")
    if kind == "equi":
        return T("Each angle of an equilateral triangle is", "60°", ["90°", "45°", "180°"], "180° ÷ 3 = <b>60°</b>.")
    angs = r.choice([(90, 45, 45, "Right-angled"), (100, 40, 40, "Obtuse-angled"), (60, 70, 50, "Acute-angled"), (120, 30, 30, "Obtuse-angled"), (90, 30, 60, "Right-angled"), (80, 60, 40, "Acute-angled"), (110, 35, 35, "Obtuse-angled")])
    return T("A triangle has angles %d°, %d° and %d°. What kind of triangle is it?" % angs[:3], angs[3], [x for x in ["Right-angled", "Obtuse-angled", "Acute-angled", "Straight-angled"] if x != angs[3]],
             "<b>%s</b>." % angs[3])


def main():
    unit(7, 1, 7, "a-tale-of-three-intersecting-lines", 7, "G", "A Tale of Three Intersecting Lines: Triangles", "a tale of three intersecting lines",
         "Triangles: the triangle inequality, constructing triangles from given sides, the angle sum property, exterior angles, and equilateral and isosceles triangles (summary of NCERT Ganita Prakash Class 7)",
         "Class 7 A Tale of Three Intersecting Lines worksheet (Ganita Prakash Part 1, Chapter 7): triangle inequality, angle sum, exterior angles, isosceles and equilateral triangles. 100 questions with answers.",
         "Any two sides of a triangle add up to more than the third", "The angles of a triangle add up to 180°.",
         "<p><b>Triangle inequality</b>: each side must be shorter than the sum of the other two. 3 cm, 4 cm, 8 cm cannot make a triangle.</p>"
         "<p>The three angles of a triangle add up to <b>180°</b>. An <b>exterior angle</b> equals the sum of the two opposite interior angles.</p>"
         "<p>An <b>equilateral</b> triangle has three 60° angles. An <b>isosceles</b> triangle has two equal sides and two equal base angles.</p>",
         [("Can 5 cm, 6 cm and 12 cm make a triangle?", ["5 + 6 = 11 < 12"], "No"),
          ("Two angles of a triangle are 48° and 77°. Find the third.", ["180° − 125°"], "55°")],
         ["Allowing two sides to add up to exactly the third side.", "Using 360° as the angle sum of a triangle.", "Forgetting to halve when finding the base angles of an isosceles triangle."],
         [("What is the triangle inequality?", "In any triangle the sum of two sides is greater than the third side."),
          ("What is the angle sum property?", "The three interior angles of a triangle add up to 180°."),
          ("What is the exterior angle property?", "An exterior angle of a triangle equals the sum of the two interior opposite angles.")],
         [("Can it make a triangle?", [(one_ineq, 20)]),
          ("Angle sum of a triangle", [(gb(au.one_tri), 20)]),
          ("Exterior angles", [(gb(au.one_ext), 20)]),
          ("Isosceles and equilateral triangles", [(one_iso, 20)]),
          ("Mixed triangle problems", [(one_ineq, 7), (one_iso, 7), (gb(au.one_tri), 6)])], R)


if __name__ == "__main__":
    main()
