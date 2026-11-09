# -*- coding: utf-8 -*-
"""
US Grade 7 Math: Constructing Triangles and Cross Sections (7.G.A.2, 7.G.A.3)
  python tools/gen_us_math_g7_constructing_triangles.py
Which side lengths and angles make a triangle (one, many or none), and the 2D shapes made by
slicing prisms and pyramids.
Wrong answers come from real mistakes: forgetting that the two shorter sides must add to MORE than the
longest, thinking three angles fix one triangle, and naming the base shape for every slice.
"""
import random
from ws_common import (mcq, balance, B, table, example, write_unit)

R = random.Random(71901)
UPDATED = "2026-11-09"


def ch(q, good, bad, e):
    return mcq(q, (good, "g"), [(b, b) for b in bad], e)


# ------------------------------------------------------------ set 1: side lengths
def set_sides():
    its = []
    sides = [(3, 4, 5), (2, 3, 6), (5, 5, 10), (7, 8, 9), (1, 2, 4), (6, 6, 6), (4, 9, 12), (10, 3, 6), (5, 12, 13), (2, 2, 3), (8, 3, 4), (9, 9, 17)]
    for a, b, c in sides:
        s = sorted((a, b, c))
        ok = s[0] + s[1] > s[2]
        e = "Add the two shorter sides: %d + %d = %d. %s" % (s[0], s[1], s[0] + s[1],
            "%d > %d, so they make a triangle." % (s[0] + s[1], s[2]) if ok else
            ("%d = %d, so the sides lie flat and do not make a triangle." % (s[0] + s[1], s[2]) if s[0] + s[1] == s[2] else "%d < %d, so the sides cannot meet." % (s[0] + s[1], s[2])))
        its.append(ch("Can sides of %d cm, %d cm and %d cm make a triangle?" % (a, b, c), "Yes" if ok else "No",
                      ["No" if ok else "Yes", "Only if it is a right triangle", "Only if two sides are equal"], e))
    for a, b in [(4, 7), (5, 9), (3, 10), (6, 6)]:
        lo, hi = abs(a - b), a + b
        its.append(ch("Two sides of a triangle are %d m and %d m. Which length could the third side be?" % (a, b), "%d m" % (lo + 1),
                      ["%d m" % lo, "%d m" % hi, "%d m" % (hi + 2)], "The third side must be more than %d − %d = %d and less than %d + %d = %d." % (max(a, b), min(a, b), lo, a, b, hi)))
    for a, b in [(5, 8), (2, 9)]:
        lo, hi = abs(a - b), a + b
        its.append(ch("Two sides of a triangle are %d in. and %d in. What are all the possible lengths x of the third side?" % (a, b),
                      "%d &lt; x &lt; %d" % (lo, hi), ["%d ≤ x ≤ %d" % (lo, hi), "x &lt; %d" % hi, "x &gt; %d" % lo],
                      "x must be greater than %d − %d = %d and less than %d + %d = %d." % (max(a, b), min(a, b), lo, a, b, hi)))
    its.append(ch("What is the rule for three side lengths to make a triangle?", "The two shorter sides must add to more than the longest side",
                  ["All three sides must be equal", "The longest side must be more than the other two together", "Any three lengths work"],
                  "This is the triangle inequality. If the short sides add to exactly the longest, the triangle is flat."))
    its.append(ch("How many different triangles can you make with sides 5 cm, 6 cm and 7 cm?", "Exactly one", ["None", "Two", "Many"],
                  "Three side lengths that work fix the shape: exactly one triangle (copies are the same triangle)."))
    return {"title": "Can these sides make a triangle?", "items": its}


# ------------------------------------------------------------ set 2: angles
def set_angles():
    its = []
    angs = [(50, 60), (90, 45), (30, 30), (100, 35), (25, 65), (110, 40), (60, 60), (15, 120)]
    for a, b in angs:
        c = 180 - a - b
        its.append(mcq("Two angles of a triangle are %d° and %d°. What is the third angle?" % (a, b), ("%d°" % c, c),
                       [("%d°" % w, w) for w in [360 - a - b, a + b, 90 - a if a < 90 else c + 10, c + 20, c - 10] if 0 < w != c],
                       "The angles of a triangle add to 180°: 180 − %d − %d = %d°." % (a, b, c)))
    sets_ = [(60, 70, 50, "One triangle shape, but many sizes", ["Exactly one triangle", "No triangle", "Two triangles"],
              "60 + 70 + 50 = 180, so the angles work. But angles do not fix the size: you can draw small or large triangles with these angles."),
             (90, 60, 40, "No triangle", ["Exactly one triangle", "Many triangles", "Two triangles"], "90 + 60 + 40 = 190, not 180, so no triangle has these angles."),
             (45, 45, 90, "One triangle shape, but many sizes", ["Exactly one triangle", "No triangle", "Only a tiny triangle"], "45 + 45 + 90 = 180. Many sizes are possible."),
             (100, 50, 20, "No triangle", ["Exactly one triangle", "Many triangles", "One right triangle"], "100 + 50 + 20 = 170, not 180.")]
    for a, b, c, good, bad, e in sets_:
        its.append(ch("How many triangles have angles %d°, %d° and %d°?" % (a, b, c), good, bad, e))
    cons = [("Two sides (5 cm and 7 cm) and the angle between them (40°)", "Exactly one triangle"),
            ("Two angles (50° and 60°) and the side between them (8 cm)", "Exactly one triangle"),
            ("Three angles: 30°, 60° and 90°", "Many triangles"),
            ("Three sides: 2 cm, 3 cm and 8 cm", "No triangle"),
            ("Three sides: 6 cm, 8 cm and 10 cm", "Exactly one triangle"),
            ("Two angles of 100° and 90°", "No triangle"),
            ("One angle of 70° and nothing else", "Many triangles"),
            ("Two sides of 4 cm and 6 cm, with no angle given", "Many triangles")]
    for cond, good in cons:
        bad = [x for x in ["Exactly one triangle", "Many triangles", "No triangle", "Two triangles"] if x != good][:3]
        its.append(ch("How many triangles can be made with these conditions? %s" % cond, good, bad,
                      {"Exactly one triangle": "These facts fix the size and shape, so every triangle drawn is the same.",
                       "Many triangles": "These facts do not fix the size or shape, so many different triangles fit.",
                       "No triangle": "These facts break a triangle rule (the angles add to 180°, and the two shorter sides add to more than the longest)."}[good]))
    return {"title": "Angles: one, many or no triangles", "items": its}


# ------------------------------------------------------------ set 3: classify
def set_classify():
    its = []
    tri = [((5, 5, 5), "Equilateral"), ((6, 6, 9), "Isosceles"), ((4, 7, 9), "Scalene"), ((8, 8, 3), "Isosceles"), ((10, 12, 14), "Scalene"), ((7, 7, 7), "Equilateral")]
    for s, good in tri:
        bad = [x for x in ["Equilateral", "Isosceles", "Scalene", "Right"] if x != good][:3]
        its.append(ch("A triangle has sides %d, %d and %d. What kind of triangle is it (by its sides)?" % s, good, bad,
                      "Equilateral: 3 equal sides. Isosceles: at least 2 equal sides. Scalene: no equal sides."))
    an = [((90, 45, 45), "Right"), ((60, 60, 60), "Acute"), ((120, 30, 30), "Obtuse"), ((70, 60, 50), "Acute"), ((90, 30, 60), "Right"), ((100, 50, 30), "Obtuse")]
    for a, good in an:
        bad = [x for x in ["Acute", "Right", "Obtuse", "Straight"] if x != good][:3]
        its.append(ch("A triangle has angles %d°, %d° and %d°. What kind of triangle is it (by its angles)?" % a, good, bad,
                      "Acute: all angles less than 90°. Right: one 90° angle. Obtuse: one angle more than 90°."))
    poss = [("Can a triangle have two right angles?", "No: 90 + 90 = 180 leaves 0° for the third angle", ["Yes, if it is large", "Yes, a square has four", "Only if it is isosceles"]),
            ("Can a triangle be both right and isosceles?", "Yes, with angles 90°, 45° and 45°", ["No, never", "Only if all sides are equal", "Only if it is obtuse"]),
            ("Can a triangle be both obtuse and equilateral?", "No: equilateral angles are all 60°", ["Yes, if it is large", "Yes, always", "Only if it is a right triangle"]),
            ("Can a scalene triangle be a right triangle?", "Yes, like sides 3, 4 and 5", ["No, never", "Only if two sides are equal", "Only if it is acute"]),
            ("A triangle has an obtuse angle. How many acute angles does it have?", "2", ["0", "1", "3"]),
            ("An isosceles triangle has a 40° angle between its equal sides. What are the other two angles?", "70° and 70°", ["40° and 100°", "40° and 40°", "50° and 90°"]),
            ("An isosceles triangle has two 50° angles. What is the third angle?", "80°", ["50°", "130°", "100°"]),
            ("What is each angle of an equilateral triangle?", "60°", ["90°", "45°", "180°"])]
    for q, good, bad in poss:
        its.append(ch(q, good, bad, "Use the facts: angles add to 180°, a right angle is 90°, and equal sides have equal opposite angles."))
    return {"title": "Classify triangles", "items": its}


# ------------------------------------------------------------ set 4: cross sections
def set_cross():
    its = []
    cs = [("A rectangular prism is sliced parallel to its base.", "A rectangle the same size as the base", ["A triangle", "A circle", "A trapezoid"]),
          ("A rectangular prism is sliced perpendicular to its base (straight down, parallel to a side face).", "A rectangle", ["A triangle", "A circle", "A pentagon"]),
          ("A cube is sliced parallel to one face.", "A square", ["A triangle", "A hexagon", "A circle"]),
          ("A cube has one corner cut off with a single straight cut.", "A triangle", ["A square", "A circle", "A rectangle"]),
          ("A square pyramid is sliced parallel to its base.", "A square (smaller than the base)", ["A triangle", "A rectangle that is longer than the base", "A circle"]),
          ("A square pyramid is sliced straight down through its top point, perpendicular to the base.", "A triangle", ["A square", "A circle", "A rectangle"]),
          ("A triangular prism is sliced parallel to its triangle bases.", "A triangle the same size as the bases", ["A rectangle", "A square", "A circle"]),
          ("A triangular prism is sliced parallel to one of its rectangle faces.", "A rectangle", ["A triangle", "A circle", "A hexagon"]),
          ("A cylinder is sliced parallel to its base.", "A circle", ["A rectangle", "A triangle", "An oval only"]),
          ("A cylinder is sliced straight down through its center, perpendicular to the base.", "A rectangle", ["A circle", "A triangle", "A trapezoid"]),
          ("A cone is sliced parallel to its base.", "A circle", ["A triangle", "A rectangle", "A square"]),
          ("A cone is sliced straight down through its tip, perpendicular to the base.", "A triangle", ["A circle", "A rectangle", "A square"]),
          ("A rectangular pyramid is sliced parallel to its base.", "A rectangle", ["A triangle", "A circle", "A square only"]),
          ("A sphere is sliced by any plane.", "A circle", ["A square", "A triangle", "A rectangle"]),
          ("A hexagonal prism is sliced parallel to its bases.", "A hexagon", ["A rectangle", "A triangle", "A circle"])]
    for q, good, bad in cs:
        its.append(ch(q + " What shape is the cross section?", good, bad,
                      "A slice parallel to the base of a prism or cylinder has the same shape and size as the base. A slice through the top of a pyramid or cone makes a triangle."))
    more = [("Which solid can have a triangle cross section?", "A square pyramid", ["A cylinder (sliced any way)", "A sphere", "A cylinder sliced parallel to the base"]),
            ("Which solid always has a circle cross section, however it is sliced?", "A sphere", ["A cylinder", "A cone", "A cube"]),
            ("Slices of a square pyramid parallel to the base get ___ as they get closer to the top.", "smaller", ["larger", "the same size", "triangular"]),
            ("A loaf of bread is a rectangular prism. Each slice (parallel to the end) is a…", "rectangle", ["triangle", "circle", "trapezoid"]),
            ("Cutting a cylindrical log straight across makes a…", "circle", ["rectangle", "triangle", "square"])]
    for q, good, bad in more:
        its.append(ch(q, good, bad, "Picture the cut. A cut parallel to a base copies the base shape."))
    return {"title": "Cross sections of solids", "items": its}


# ------------------------------------------------------------ set 5: problems
def set_words():
    its = []
    w = [("Maya has sticks of 4 in., 6 in. and 11 in. Can she make a triangle?", "No: 4 + 6 = 10 is less than 11", ["Yes: all sides are different", "Yes: 4 + 6 + 11 = 21", "No: the sides must be equal"]),
         ("A garden fence has sides of 12 m and 9 m. Which length could the third side be?", "15 m", ["3 m", "21 m", "25 m"]),
         ("A roof has two angles of 35° at the bottom. What is the angle at the top?", "110°", ["35°", "70°", "145°"]),
         ("A ramp makes a right triangle with the ground. The ramp meets the ground at 12°. What is the angle at the top of the ramp?", "78°", ["12°", "168°", "88°"]),
         ("Two students each draw a triangle with sides 6, 8 and 10 cm. Which is true?", "The triangles are the same size and shape", ["The triangles must be different",
          "One must be a right triangle and one not", "They cannot be drawn"]),
         ("Two students each draw a triangle with angles 40°, 60° and 80°. Which is true?", "The triangles have the same shape but may be different sizes",
          ["The triangles must be the same size", "The triangles cannot be drawn", "One triangle must be right"]),
         ("A baker slices a round cake straight down through the center. What shape is the cut face?", "A rectangle", ["A circle", "A triangle", "A square"]),
         ("A block of cheese is a rectangular prism. You cut off a corner with one straight cut. What shape could the cut face be?", "A triangle", ["A circle", "A cylinder", "A cone"]),
         ("An ice cream cone (a cone) is cut straight across near the top. What shape is the cut?", "A circle", ["A triangle", "A square", "A rectangle"]),
         ("A tent is a triangular prism. A pole slices it parallel to the front. What shape is that slice?", "A triangle", ["A rectangle", "A circle", "A square"]),
         ("Three towns are 30 km, 40 km and 80 km apart in pairs. Is that possible on a flat map?", "No: 30 + 40 is less than 80", ["Yes: any three distances work", "Yes: 30 + 40 + 80 = 150", "Only if the towns are on a line"]),
         ("A triangle has angles x°, 2x° and 3x°. What is x?", "30", ["60", "90", "20"]),
         ("A triangle has angles 3x°, 4x° and 5x°. What is the largest angle?", "75°", ["60°", "15°", "90°"]),
         ("One angle of a right triangle is 37°. What is the third angle?", "53°", ["143°", "37°", "63°"]),
         ("A builder needs a triangular frame with sides 2 ft, 3 ft and an unknown side. Which length is NOT possible?", "5 ft", ["2 ft", "3 ft", "4 ft"]),
         ("A pyramid-shaped tower has a square base. A floor is built parallel to the base halfway up. What shape is the floor?", "A smaller square", ["A triangle", "A larger square", "A circle"]),
         ("An architect uses a triangle with sides 5 m, 5 m and 8 m. What type of triangle is it?", "Isosceles", ["Equilateral", "Scalene", "Right"]),
         ("Which set of conditions gives exactly one triangle?", "Sides 3 cm and 5 cm with a 60° angle between them", ["Angles 50°, 60° and 70°", "Sides 2, 3 and 6 cm",
          "One side of 4 cm"]),
         ("Which side lengths make a right triangle?", "6, 8, 10", ["4, 5, 6", "2, 3, 4", "5, 5, 5"]),
         ("A slice of a cube shows a rectangle that is not a square. How could the cube have been cut?", "Through two opposite edges (a diagonal cut)", ["Parallel to a face",
          "It is impossible", "Through only one corner"])]
    for q, good, bad in w:
        its.append(ch(q, good, bad, {
            "15 m": "The third side must be between 12 − 9 = 3 and 12 + 9 = 21 m, not equal to either.",
            "110°": "180 − 35 − 35 = 110°.", "78°": "180 − 90 − 12 = 78°.", "30": "x + 2x + 3x = 180, so 6x = 180 and x = 30.",
            "75°": "3x + 4x + 5x = 180, so 12x = 180 and x = 15. Largest: 5 × 15 = 75°.", "53°": "180 − 90 − 37 = 53°.",
            "5 ft": "2 + 3 = 5, so a 5 ft side would make a flat shape, not a triangle.", "6, 8, 10": "6² + 8² = 36 + 64 = 100 = 10².",
            "Isosceles": "Two sides are 5 m, so it is isosceles."}.get(good, "Use the triangle rules: the two shorter sides add to more than the longest, and the angles add to 180°. For slices, picture the cut.")))
    return {"title": "Word problems", "items": its}


def body():
    rows = [["Three sides (that work)", "exactly one"], ["Two sides and the angle between them", "exactly one"], ["Two angles and the side between them", "exactly one"],
            ["Three angles that add to 180°", "many (same shape, different sizes)"], ["Sides where the two shorter add to the longest or less", "none"]]
    cs = [["Prism or cylinder, parallel to the base", "same shape as the base"], ["Pyramid or cone, parallel to the base", "smaller copy of the base"],
          ["Pyramid or cone, straight down through the top", "triangle"], ["Any slice of a sphere", "circle"]]
    return ("<h2>When do sides make a triangle?</h2><p>The <b>two shorter sides must add to more than the longest side</b>. "
            "3, 4 and 5 work (3 + 4 = 7 &gt; 5). 2, 3 and 6 do not (2 + 3 = 5 &lt; 6). The angles of every triangle add to 180°.</p>"
            + table(["What you are given", "How many triangles"], rows)
            + example("Two sides are 5 in. and 8 in. What can the third side be?", ["More than 8 − 5 = 3.", "Less than 8 + 5 = 13."], "between 3 in. and 13 in.")
            + "<h2>Cross sections</h2><p>A <b>cross section</b> is the flat shape you see when you slice a solid.</p>"
            + table(["Slice", "Cross section"], cs)
            + "<h2>Common mistakes</h2><ul><li>Checking only one pair of sides: always use the two shortest.</li>"
            "<li>Thinking three angles give one triangle: they give one shape in many sizes.</li>"
            "<li>Saying every slice of a prism looks like the base: a slice through the side can be a rectangle.</li></ul>")


def main():
    sets = [set_sides(), set_angles(), set_classify(), set_cross(), set_words()]
    balance(sets, R)
    unit = {
        "slug": "constructing-triangles-and-cross-sections",
        "title": "Constructing Triangles and Cross Sections",
        "seo_title": "Grade 7 Constructing Triangles and Cross Sections Worksheets: Triangle Inequality and Slicing Solids",
        "short_title": "Triangles and cross sections",
        "domain": "Geometry",
        "standard_code": "7.G.A.2–3",
        "standard_url": "https://www.thecorestandards.org/Math/Content/7/G/A/2/",
        "standard_text": "Draw geometric shapes with given conditions, focusing on constructing triangles from three measures of angles or sides, noticing when the conditions determine a unique triangle, more than one triangle, or no triangle. Describe the two-dimensional figures that result from slicing three-dimensional figures, as in plane sections of right rectangular prisms and right rectangular pyramids.",
        "meta_desc": "Free Grade 7 constructing triangles worksheets: the triangle inequality, angle sums, when conditions give one, many or no triangles, classifying triangles, and cross sections of prisms, pyramids, cylinders and cones. 100 practice questions with an answer key.",
        "key_big": "The two shorter sides must add to more than the longest. The angles always add to 180°.",
        "key_sub": "Three sides that work give exactly one triangle; three angles give one shape in many sizes. A slice parallel to a base copies the base.",
        "body_html": body(),
        "faq": [
            {"q": "How do you know if three lengths make a triangle?", "a": "Add the two shorter lengths. If the sum is more than the longest length, they make a triangle. 3, 4, 5 work; 2, 3, 6 do not."},
            {"q": "Do three angles make a unique triangle?", "a": "No. If they add to 180°, they fix the shape, but you can draw the triangle in many sizes."},
            {"q": "What is a cross section?", "a": "The flat shape you get when you slice a solid. Slicing a rectangular prism parallel to its base gives a rectangle like the base."},
            {"q": "What cross sections can a pyramid have?", "a": "A slice parallel to the base is a smaller copy of the base. A slice straight down through the top point is a triangle."}],
        "sets": sets,
        "pdf_url": "",
        "sort": 19,
        "updated": UPDATED,
    }
    write_unit("us", "math", "grade-7", unit)


if __name__ == "__main__":
    main()
