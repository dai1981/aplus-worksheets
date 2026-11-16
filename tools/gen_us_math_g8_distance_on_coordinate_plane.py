# -*- coding: utf-8 -*-
"""
US Grade 8 Math: Distance on the Coordinate Plane (8.G.B.8)
  python3 tools/gen_us_math_g8_distance_on_coordinate_plane.py
Find the distance between two points: straight across or up and down by counting, and slanted by drawing
a right triangle and using the Pythagorean theorem (the distance formula). Also perimeters, comparing
distances and map problems. Wrong answers come from real mistakes: adding the legs, forgetting the
square root, subtracting a negative wrongly, and mixing x and y.
"""
import math, random
from ws_common import num, mcq, balance, B, table, example, write_unit, fig, RED, BLUE, GREEN
from g8_common import grid_svg

R = random.Random(81701)
UPDATED = "2026-11-16"


def rt(n):
    return "√<span style='text-decoration:overline'>%s</span>" % num(n)


def pt(p):
    return "(%s, %s)" % (num(p[0]), num(p[1]))


def dist_txt(d2):
    r = math.isqrt(d2)
    if r * r == d2:
        return num(r)
    return "%s ≈ %.1f" % (rt(d2), math.sqrt(d2))


def sub(a, b):
    """'5 − 2' or '5 − (−2)'."""
    return "%s − %s" % (num(a), ("(%s)" % num(b)) if b < 0 else num(b))


def dist_q(p, q_, pic=True, ask=None):
    dx, dy = q_[0] - p[0], q_[1] - p[1]
    d2 = dx * dx + dy * dy
    ans = dist_txt(d2)
    corner = (q_[0], p[1])
    if pic:
        svg = grid_svg(-7, 7, points=[(p[0], p[1], "A", RED), (q_[0], q_[1], "B", RED)],
                       segs=[(p[0], p[1], q_[0], q_[1], BLUE), (p[0], p[1], corner[0], corner[1], GREEN), (corner[0], corner[1], q_[0], q_[1], GREEN)],
                       unit=16)
        qq = fig(svg) + (ask or "Find the distance from A%s to B%s." % (pt(p), pt(q_)))
    else:
        qq = ask or "Find the distance between %s and %s." % (B(pt(p)), B(pt(q_)))
    if dx == 0 or dy == 0:
        e = "The points are on the same %s line. Count: |%s| = <b>%s</b>." % ("vertical" if dx == 0 else "horizontal",
                                                                             sub(q_[1], p[1]) if dx == 0 else sub(q_[0], p[0]), ans)
        wr = [num(abs(q_[0] + p[0]) + abs(q_[1] + p[1])), num(abs(dx) + abs(dy) + 2), num(d2), num(abs(dx) + abs(dy) - 1)]
    else:
        e = ("Make a right triangle. Across: %s = %s. Up/down: %s = %s. d² = %d² + %d² = %d, so d = <b>%s</b>."
             % (sub(q_[0], p[0]), num(dx), sub(q_[1], p[1]), num(dy), abs(dx), abs(dy), d2, ans))
        wrong_mix = (q_[0] + p[0]) ** 2 + (q_[1] + p[1]) ** 2
        wr = [num(abs(dx) + abs(dy)), num(d2), dist_txt(wrong_mix) if wrong_mix != d2 and wrong_mix > 0 else num(abs(dx) * abs(dy)),
              dist_txt(abs(dx * dx - dy * dy)) if dx * dx != dy * dy else num(2 * abs(dx))]
    return mcq(qq, (ans, ans), [(w, w) for w in wr if w != ans] + [(dist_txt(d2 + 1), dist_txt(d2 + 1)), (dist_txt(d2 + 7), dist_txt(d2 + 7))], e)


# ============================================================ set 1: straight lines
def set_straight():
    its = []
    for p, q_ in [((1, 2), (6, 2)), ((-3, 4), (5, 4)), ((2, -1), (2, 6)), ((-4, -5), (-4, 3)), ((-6, 0), (-1, 0)), ((0, -2), (0, 5)),
                  ((3, 3), (-4, 3)), ((-2, 6), (-2, -6)), ((5, -3), (-5, -3)), ((1, -7), (1, -2))]:
        its.append(dist_q(p, q_, pic=len(its) % 2 == 0))
    for q, ans, wr, e in [
        ("How far is (7, 3) from (−2, 3)?", "9", ["5", "6", "10"], "Same y. 7 − (−2) = <b>9</b>."),
        ("How far is (4, −6) from (4, 1)?", "7", ["5", "−7", "8"], "Same x. 1 − (−6) = <b>7</b>."),
        ("How far is (−5, −1) from (−9, −1)?", "4", ["14", "−4", "6"], "Same y. −5 − (−9) = <b>4</b>."),
        ("Point A is (2, 5). Point B is 6 units to the left of A. Where is B?", "(−4, 5)", ["(8, 5)", "(2, −1)", "(2, 11)"],
         "Left means subtract from x: 2 − 6 = −4. <b>(−4, 5)</b>."),
        ("Point A is (−3, −2). Point B is 7 units above A. Where is B?", "(−3, 5)", ["(4, −2)", "(−3, −9)", "(−10, −2)"],
         "Up means add to y: −2 + 7 = 5. <b>(−3, 5)</b>."),
        ("Which two points are 8 units apart?", "(−3, 1) and (5, 1)", ["(−3, 1) and (3, 1)", "(1, 3) and (1, 7)", "(2, 2) and (2, −4)"],
         "5 − (−3) = 8. <b>(−3, 1) and (5, 1)</b>."),
        ("Why can a distance never be negative?", "It is a length, so we use the size of the difference", ["Because x is positive",
         "Because the points are on the right", "It can be negative"], "Distance is how far apart: <b>it is a length, so we use the size of the difference</b>."),
        ("A rectangle has corners (1, 1), (6, 1), (6, 4) and (1, 4). What is its perimeter?", "16", ["15", "8", "30"],
         "Sides: 6 − 1 = 5 and 4 − 1 = 3. Perimeter = 2(5 + 3) = <b>16</b>."),
        ("A square has corners (−2, −2), (2, −2), (2, 2) and (−2, 2). What is its area?", "16", ["8", "4", "64"], "Side = 2 − (−2) = 4. Area = 4 × 4 = <b>16</b>."),
        ("A rectangle has corners (−3, 2), (4, 2), (4, −1) and (−3, −1). What is its area?", "21", ["20", "12", "7"],
         "Sides: 4 − (−3) = 7 and 2 − (−1) = 3. Area = 7 × 3 = <b>21</b>."),
    ]:
        its.append(mcq(q, (ans, ans), [(w, w) for w in wr], e))
    o = its
    order = [o[0], o[1], o[2], o[10], o[3], o[11], o[4], o[13], o[5], o[14], o[6], o[12], o[7], o[15], o[8], o[16], o[9],
             o[17], o[18], o[19]]
    return {"title": "Straight across or up and down", "items": order}


# ============================================================ set 2: with a picture
def set_picture():
    its = []
    for p, q_ in [((0, 0), (3, 4)), ((1, 1), (7, 9)), ((-2, -1), (4, 7)), ((-5, 2), (7, 7)), ((2, -3), (-1, 1)), ((-4, -4), (2, 4)),
                  ((0, 2), (5, -3)), ((-6, -2), (2, 4)), ((1, -5), (4, -1)), ((-3, 3), (2, -2)), ((-1, 0), (1, 1)), ((3, 4), (-3, -4)),
                  ((-6, 6), (-3, 2)), ((2, 5), (-5, -2)), ((0, -6), (5, 6)), ((-7, -3), (1, 3)), ((4, 0), (0, 4)), ((-2, -6), (4, 2)),
                  ((5, 5), (6, -2)), ((-5, -5), (1, 3))]:
        its.append(dist_q(p, q_, pic=True))
    return {"title": "Draw a right triangle", "items": its}


# ============================================================ set 3: from coordinates
def set_formula():
    its = []
    for p, q_ in [((1, 2), (4, 6)), ((-3, 1), (2, 13)), ((2, -4), (8, 4)), ((-1, -1), (2, 3)), ((0, 5), (12, 0)), ((6, -2), (-2, 4)),
                  ((-7, 3), (-4, 7)), ((10, 1), (2, 16)), ((-2, -3), (1, -1)), ((3, 7), (5, 4)), ((-4, 2), (0, -2)), ((1, 1), (2, 2)),
                  ((-6, -8), (0, 0)), ((5, -9), (-4, 3)), ((-1, 4), (-1, 4 - 5))]:
        its.append(dist_q(p, q_, pic=False))
    for q, ans, wr, e in [
        ("Which is the distance formula?", "d = √((x₂ − x₁)² + (y₂ − y₁)²)", ["d = (x₂ − x₁) + (y₂ − y₁)", "d = √(x₂ + x₁ + y₂ + y₁)",
         "d = (x₂ − x₁)² + (y₂ − y₁)²"], "It is the Pythagorean theorem for the two points: <b>d = √((x₂ − x₁)² + (y₂ − y₁)²)</b>."),
        ("To find the distance between (2, 3) and (5, 7), Ana adds 3 + 4 = 7. What should she do?", "Use √(3² + 4²) = 5", ["Nothing, 7 is right",
         "Multiply 3 × 4 = 12", "Use 3² + 4² = 25"], "Add the squares, then take the root: <b>√(3² + 4²) = 5</b>."),
        ("Ben finds d² = 100 for two points. What is the distance?", "10", ["100", "50", "20"], "d = √100 = <b>10</b>."),
        ("Does it matter which point you call (x₁, y₁)?", "No, the squares give the same answer", ["Yes, always start with the left point",
         "Yes, it changes the sign of the answer", "Only if the points are negative"], "(−3)² = 3², so <b>no, the squares give the same answer</b>."),
        ("Kim subtracts 2 − (−3) and gets −1. What is right?", "5", ["−1", "1", "−5"], "Subtracting a negative adds: 2 + 3 = <b>5</b>."),
    ]:
        its.append(mcq(q, (ans, ans), [(w, w) for w in wr], e))
    o = its
    order = [o[0], o[1], o[15], o[2], o[3], o[17], o[4], o[5], o[16], o[6], o[7], o[19], o[8], o[9], o[18], o[10], o[11],
             o[12], o[13], o[14]]
    return {"title": "Use the coordinates", "items": order}


# ============================================================ set 4: shapes and comparisons
def set_shapes():
    its = []
    for tri in [[(0, 0), (4, 0), (0, 3)], [(1, 1), (7, 1), (1, 9)], [(-2, -1), (3, -1), (-2, 11)], [(0, 0), (6, 0), (6, 8)],
                [(-3, 2), (1, 2), (1, -1)], [(2, 2), (2, 7), (14, 2)]]:
        a, b, c = tri
        sides = [math.dist(a, b), math.dist(b, c), math.dist(c, a)]
        per = sum(sides)
        assert abs(per - round(per)) < 1e-9
        per = int(round(per))
        svg = grid_svg(-4, 14, ylo=-3, yhi=12, polys=[(tri, "#1f5fa8", BLUE)], unit=12, tick_every=2)
        q = fig(svg) + "Find the perimeter of the triangle with corners %s." % ", ".join(pt(p) for p in tri)
        e = "Sides: %s. Perimeter = <b>%d</b>." % (" + ".join(num(int(round(s))) for s in sides), per)
        leg_sum = int(round(sorted(sides)[0] + sorted(sides)[1]))
        its.append(mcq(q, (str(per), per), [(str(leg_sum), "l"), (str(per + int(round(sorted(sides)[0]))), "x"), (str(2 * leg_sum), "d"),
                                            (str(per - 1), "m")], e))
    for o, a_, b_ in [((0, 0), (3, 4), (5, 1)), ((1, 1), (4, 5), (6, 2)), ((0, 0), (-6, 2), (5, -4)), ((2, -1), (7, -1), (5, 4)),
                      ((-2, -2), (1, 2), (4, -2)), ((0, 0), (5, 12), (9, 9))]:
        da, db = math.dist(o, a_), math.dist(o, b_)
        assert abs(da - db) > 0.01
        far = pt(a_) if da > db else pt(b_)
        q = "Which point is farther from %s: %s or %s?" % (B(pt(o)), B(pt(a_)), B(pt(b_)))
        e = "Distance to %s: %s. Distance to %s: %s. <b>%s</b> is farther." % (
            pt(a_), dist_txt((a_[0] - o[0]) ** 2 + (a_[1] - o[1]) ** 2), pt(b_), dist_txt((b_[0] - o[0]) ** 2 + (b_[1] - o[1]) ** 2), far)
        other = pt(b_) if far == pt(a_) else pt(a_)
        its.append(mcq(q, (far, far), [(other, other), ("They are the same distance", "s"), ("We cannot tell", "c")], e))
    for q, ans, wr, e in [
        ("A circle has center (0, 0) and passes through (3, 4). What is its radius?", "5", ["7", "25", "3.5"], "r = √(3² + 4²) = <b>5</b>."),
        ("Is (6, 8) on the circle with center (0, 0) and radius 10?", "Yes", ["No", "Only if it is inside", "We cannot tell"],
         "√(36 + 64) = √100 = 10: <b>yes</b>."),
        ("Triangle with corners (0, 0), (5, 0), (0, 5). How long is the longest side, exactly?", "√50", ["10", "5", "25"],
         "From (5, 0) to (0, 5): √(25 + 25) = <b>√50</b> ≈ 7.1."),
        ("Is the triangle with corners (0, 0), (4, 0) and (4, 3) a right triangle?", "Yes", ["No", "Only if it is drawn big", "We cannot tell"],
         "Sides 4, 3, 5 and 3² + 4² = 5²: <b>yes</b>."),
        ("What is the midpoint between (2, 4) and (8, 10)?", "(5, 7)", ["(6, 6)", "(10, 14)", "(3, 3)"],
         "Average the coordinates: ((2 + 8) ÷ 2, (4 + 10) ÷ 2) = <b>(5, 7)</b>."),
        ("A square has corners (0, 0), (3, 1), (2, 4) and (−1, 3). How long is each side, exactly?", "√10", ["4", "10", "3"],
         "(0, 0) to (3, 1): √(9 + 1) = <b>√10</b>."),
        ("Two points are 13 apart. One leg of the right triangle between them is 5. What is the other leg?", "12", ["8", "18", "√194"],
         "13² − 5² = 144, so <b>12</b>."),
        ("Point A is (1, 2). B is 5 units from A, straight up. Where is B?", "(1, 7)", ["(6, 2)", "(1, −3)", "(5, 2)"], "Up 5: <b>(1, 7)</b>."),
    ]:
        its.append(mcq(q, (ans, ans), [(w, w) for w in wr], e))
    o = its
    order = [o[6], o[12], o[0], o[7], o[13], o[1], o[8], o[15], o[2], o[9], o[14], o[3], o[10], o[16], o[4], o[11], o[17],
             o[5], o[18], o[19]]
    return {"title": "Shapes and comparisons", "items": order}


# ============================================================ set 5: maps
def set_maps():
    its = []
    for q, ans, wr, e in [
        ("On a map grid, the school is at (2, 3) and the park is at (8, 11). Each unit is 1 block. How far is it in a straight line?", "10 blocks",
         ["14 blocks", "100 blocks", "6 blocks"], "Across 6, up 8. √(36 + 64) = <b>10 blocks</b>."),
        ("Home is at (0, 0) and the store is at (5, 12). Each unit is 1 km. How far is the store in a straight line?", "13 km", ["17 km", "7 km", "169 km"],
         "√(25 + 144) = √169 = <b>13 km</b>."),
        ("A drone flies from (−3, −2) to (3, 6). Each unit is 10 m. How far does it fly?", "100 m", ["10 m", "140 m", "1,000 m"],
         "Across 6, up 8: distance 10 units = <b>100 m</b>."),
        ("A ship sails from (1, 1) to (13, 6) on a chart where 1 unit = 1 mile. How far does it sail?", "13 miles", ["17 miles", "12 miles", "169 miles"],
         "Across 12, up 5: √(144 + 25) = <b>13 miles</b>."),
        ("Walking along the streets from (0, 0) to (6, 8) takes 6 + 8 = 14 blocks. How much shorter is the straight path?", "4 blocks",
         ["10 blocks", "2 blocks", "14 blocks"], "Straight: √(36 + 64) = 10. 14 − 10 = <b>4 blocks</b> shorter."),
        ("A soccer ball is kicked from (10, 20) to (40, 60) on a field (units are yards). How far does it travel?", "50 yards",
         ["70 yards", "40 yards", "2,500 yards"], "Across 30, up 40: √(900 + 1,600) = <b>50 yards</b>."),
        ("A rescue boat at (0, 0) must reach (−9, 12). Each unit is 1 km. How far is it?", "15 km", ["21 km", "3 km", "225 km"],
         "√(81 + 144) = √225 = <b>15 km</b>."),
        ("A park is at (−2, 5). A library is at (4, −3). About how far apart are they? (1 unit = 1 block)", "10 blocks", ["14 blocks", "2 blocks", "100 blocks"],
         "Across 6, down 8: √(36 + 64) = <b>10 blocks</b>."),
        ("Two towns are at (3, 2) and (7, 5) on a map where 1 unit = 20 miles. How far apart are they?", "100 miles", ["5 miles", "140 miles", "25 miles"],
         "Across 4, up 3: 5 units × 20 = <b>100 miles</b>."),
        ("A robot moves from (1, 2) to (4, 6), then to (4, 10). How far does it travel in all?", "9 units", ["8 units", "13 units", "5 units"],
         "First: √(9 + 16) = 5. Then straight up 4. Total <b>9 units</b>."),
        ("A cell tower at (0, 0) reaches 10 miles. Is a house at (7, 7) in range? (1 unit = 1 mile)", "Yes, it is about 9.9 miles away",
         ["No, it is 14 miles away", "No, it is 49 miles away", "Yes, it is 7 miles away"], "√(49 + 49) = √98 ≈ 9.9 &lt; 10: <b>yes, it is about 9.9 miles away</b>."),
        ("A hiker at (2, −1) walks to (−4, 7). How far, if 1 unit = 1 km?", "10 km", ["14 km", "2 km", "√40 km"],
         "Across 6, up 8: √(36 + 64) = <b>10 km</b>."),
        ("On a grid, a bird flies from (0, 0) to (1, 1). About how far is that?", "1.4 units", ["2 units", "1 unit", "0 units"],
         "√(1 + 1) = √2 ≈ <b>1.4 units</b>."),
        ("A zip line goes from (0, 30) to (40, 0) (in feet). How long is it?", "50 ft", ["70 ft", "10 ft", "35 ft"],
         "√(40² + 30²) = √2,500 = <b>50 ft</b>."),
        ("Point P is (−5, −12). How far is it from the origin?", "13", ["17", "−13", "7"], "√(25 + 144) = <b>13</b>."),
        ("A treasure is 5 units from (0, 0) and on the line y = 4, to the right of the y-axis. Where is it?", "(3, 4)", ["(4, 3)", "(5, 4)", "(1, 4)"],
         "x² + 16 = 25, so x = 3: <b>(3, 4)</b>."),
        ("Which pair of points is farthest apart?", "(0, 0) and (6, 8)", ["(0, 0) and (5, 5)", "(1, 1) and (7, 5)", "(2, 3) and (9, 3)"],
         "Distances: 10, ≈7.1, ≈7.2 and 7. The farthest is <b>(0, 0) and (6, 8)</b>."),
        ("Ana says the distance from (1, 1) to (4, 5) is 7. What did she do?", "She added 3 + 4", ["She used the formula", "She found the midpoint",
         "She squared the numbers"], "The distance is √(9 + 16) = 5. <b>She added 3 + 4</b>."),
        ("Ben says the distance from (−2, 0) to (4, 0) is 2. What went wrong?", "He found 4 − 2 instead of 4 − (−2) = 6", ["Nothing, it is 2",
         "He should add 4 + 0", "He forgot the square root"], "4 − (−2) = 6: <b>he found 4 − 2 instead of 4 − (−2) = 6</b>."),
        ("Lee finds d² = 34 and says d = 17. What is right?", "d = √34 ≈ 5.8", ["d = 17", "d = 34", "d = 68"], "Take the square root, not half: <b>d = √34 ≈ 5.8</b>."),
    ]:
        its.append(mcq(q, (ans, ans), [(w, w) for w in wr], e))
    return {"title": "Maps and real-world distance", "items": its}


def body():
    svg = grid_svg(-1, 7, ylo=-1, yhi=7, points=[(1, 1, "A(1, 1)", RED), (4, 5, "B(4, 5)", RED)],
                   segs=[(1, 1, 4, 5, BLUE), (1, 1, 4, 1, GREEN), (4, 1, 4, 5, GREEN)], unit=30)
    return ("<h2>Use the Pythagorean theorem</h2>"
            "<p>To find the distance between two points, draw a right triangle. The legs are how far <b>across</b> and how far <b>up or down</b>. "
            "The distance is the hypotenuse.</p>"
            "<figure class='sn-fig'>" + svg + "<figcaption>Across 3, up 4: d = √(3² + 4²) = 5.</figcaption></figure>"
            "<p>Distance formula: <b>d = √((x₂ − x₁)² + (y₂ − y₁)²)</b>.</p>"
            + example("Find the distance from (−2, 1) to (4, 9).", ["Across: 4 − (−2) = 6.", "Up: 9 − 1 = 8.", "d = √(36 + 64) = √100."], "10")
            + "<p>If the points have the same x or the same y, just count (or subtract).</p>"
            + "<h2>Common mistakes</h2><ul><li>Adding the legs: 3 + 4 is not the distance.</li><li>Forgetting the square root.</li>"
            "<li>Subtracting a negative wrongly: 4 − (−2) = 6.</li><li>Mixing an x with a y.</li></ul>")


def main():
    sets = [set_straight(), set_picture(), set_formula(), set_shapes(), set_maps()]
    balance(sets, R)
    unit = {
        "slug": "distance-on-coordinate-plane",
        "title": "Distance on the Coordinate Plane",
        "seo_title": "Grade 8 Distance Between Two Points Worksheets: Pythagorean Theorem and Distance Formula",
        "short_title": "Distance between points",
        "domain": "Geometry",
        "standard_code": "8.G.B.8",
        "standard_url": "https://www.thecorestandards.org/Math/Content/8/G/B/8/",
        "standard_text": "Apply the Pythagorean Theorem to find the distance between two points in a coordinate system.",
        "meta_desc": "Free Grade 8 distance worksheets: find the distance between two points by counting or with the Pythagorean theorem and the distance formula, find perimeters, compare distances and solve map problems. 100 questions with an answer key.",
        "key_big": "Draw a right triangle: d = √(across² + up²).",
        "key_sub": "Same x or same y: just subtract. Otherwise square, add, then take the square root.",
        "body_html": body(),
        "faq": [
            {"q": "How do you find the distance between two points?", "a": "Find how far across (x₂ − x₁) and how far up or down (y₂ − y₁). Then d = √(across² + up²). For (1, 1) and (4, 5): √(9 + 16) = 5."},
            {"q": "What is the distance formula?", "a": "d = √((x₂ − x₁)² + (y₂ − y₁)²). It is the Pythagorean theorem written with coordinates."},
            {"q": "What if the points are on the same horizontal line?", "a": "Then the distance is just the difference of the x-coordinates (as a positive number)."},
            {"q": "Can the distance be a square root?", "a": "Yes. If the sum of squares is not a perfect square, the exact answer is a root like √34 ≈ 5.8."}],
        "sets": sets, "pdf_url": "", "sort": 17, "updated": UPDATED,
    }
    write_unit("us", "math", "grade-8", unit)


if __name__ == "__main__":
    main()
