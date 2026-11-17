# -*- coding: utf-8 -*-
"""
AU Year 7 Maths: Angle sum of triangles and polygons (Australian Curriculum v9.0: AC9M7M05)
  python3 tools/gen_au_maths_y7_angle_sum_of_triangles_and_polygons.py
The angle sum of a triangle (180°), isosceles, equilateral and right-angled triangles, the exterior angle of a
triangle, quadrilaterals (360°), the interior angle sum of any polygon, regular polygons, and problems.
Wrong answers come from real mistakes: using 360° for a triangle or 180° for a quadrilateral, using the wrong
equal angles in an isosceles triangle, and using n × 180° for a polygon.
"""
import math
import random
from au_hs import num, mcq, B, S, make, lesson, collect, QN, T, svg_wrap, line, text, fig, GREEN, INK, RED

R = random.Random(71701)
DEG = "°"


def lab(v):
    return "%d%s" % (v, DEG)


NOTE = "<br><small>Not drawn to scale.</small>"


def tri_svg(A, Bv, labels, marks=False, right=None):
    """Triangle with angles A at left, B at right; C at top. labels for (A, B, C)."""
    C = 180 - A - Bv
    base = 240.0
    # side lengths by sine rule: side opposite C is base
    b = base * math.sin(math.radians(Bv)) / math.sin(math.radians(C))
    ax, ay = 30, 0
    bx, by = 30 + base, 0
    cx, cy = ax + b * math.cos(math.radians(A)), b * math.sin(math.radians(A))
    H = cy
    sc = min(1.0, 160.0 / H) if H > 0 else 1
    pts = [(ax, ay), (bx, by), (cx, cy)]
    # scale vertically only if very tall
    pts = [(x, y * sc) for x, y in pts]
    top = max(y for _, y in pts)
    W, Hh = 300, int(top + 60)
    P = [(x, Hh - 30 - y) for x, y in pts]
    s = ["<path d='M%.1f %.1f L%.1f %.1f L%.1f %.1f Z' fill='#eef6f0' stroke='%s' stroke-width='2.5'/>" % (P[0] + P[1] + P[2] + (INK,))]
    for i, l in enumerate(labels):
        if l is None:
            continue
        px, py = P[i]
        ox, oy = P[(i + 1) % 3]
        qx, qy = P[(i + 2) % 3]
        mx, my = (ox + qx) / 2, (oy + qy) / 2
        dx, dy = mx - px, my - py
        d = math.hypot(dx, dy)
        k = 34 if i < 2 else 30
        s.append(text(px + dx / d * k, py + dy / d * k + 6, l, 15, col=RED if l in ("x", "y") else INK, italic=l in ("x", "y")))
    if right is not None:
        px, py = P[right]
        u = []
        for j in ((right + 1) % 3, (right + 2) % 3):
            qx, qy = P[j]
            d = math.hypot(qx - px, qy - py)
            u.append(((qx - px) / d * 16, (qy - py) / d * 16))
        s.append("<path d='M%.1f %.1f L%.1f %.1f L%.1f %.1f' fill='none' stroke='%s' stroke-width='2'/>" % (
            px + u[0][0], py + u[0][1], px + u[0][0] + u[1][0], py + u[0][1] + u[1][1], px + u[1][0], py + u[1][1], GREEN))
    if marks:
        for (p1, p2) in marks:
            x1, y1 = P[p1]; x2, y2 = P[p2]
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            ang = math.atan2(y2 - y1, x2 - x1) + math.pi / 2
            s.append(line(mx - 7 * math.cos(ang), my - 7 * math.sin(ang), mx + 7 * math.cos(ang), my + 7 * math.sin(ang), INK, 2))
    return svg_wrap(W, Hh, "".join(s), "triangle, not drawn accurately")


def one_tri(r):
    kind = r.choice(["plain", "plain", "iso_base", "iso_top", "right"])
    if kind == "plain":
        A, Bv = r.randint(30, 85), r.randint(30, 85)
        C = 180 - A - Bv
        svg = tri_svg(A, Bv, [lab(A), lab(Bv), "x"])
        e = "Angles in a triangle add up to 180°: 180 − %d − %d = <b>%d°</b>." % (A, Bv, C)
        return QN("Find %s.%s%s" % (B("<i>x</i>"), fig(svg), NOTE), C, [360 - A - Bv, A + Bv, 90 - A if A < 90 else 100], e, unit=DEG)
    if kind == "iso_base":
        A = r.randint(30, 75)
        C = 180 - 2 * A
        svg = tri_svg(A, A, [lab(A), "x", None], marks=[(0, 2), (1, 2)])
        e = "The triangle is isosceles (two equal sides are marked), so the base angles are equal: <b><i>x</i> = %d°</b>." % A
        return QN("Find %s.%s%s" % (B("<i>x</i>"), fig(svg), NOTE), A, [C, 180 - A, 90 - A], e, unit=DEG)
    if kind == "iso_top":
        C = r.choice([20, 30, 36, 40, 50, 64, 70, 80, 90, 100, 110])
        A = (180 - C) // 2
        svg = tri_svg(A, A, ["x", None, lab(C)], marks=[(0, 2), (1, 2)])
        e = "The base angles are equal: (180 − %d) ÷ 2 = <b>%d°</b>." % (C, A)
        return QN("The triangle is isosceles. Find %s.%s%s" % (B("<i>x</i>"), fig(svg), NOTE), A, [180 - C, C, 180 - 2 * C if 180 - 2 * C > 0 else C + 20], e, unit=DEG)
    A = r.randint(20, 70)
    svg = tri_svg(90, A, [None, lab(A), "x"], right=0)
    x = 90 - A
    e = "The triangle has a right angle (90°): 180 − 90 − %d = <b>%d°</b>." % (A, x)
    return QN("Find %s.%s%s" % (B("<i>x</i>"), fig(svg), NOTE), x, [180 - A, 90 + A if 90 + A < 180 else 45, A], e, unit=DEG)


def quad_svg(labels):
    P = [(40, 170), (260, 180), (230, 40), (90, 60)]
    s = ["<path d='M%d %d L%d %d L%d %d L%d %d Z' fill='#eef6f0' stroke='%s' stroke-width='2.5'/>" % (P[0] + P[1] + P[2] + P[3] + (INK,))]
    cx = sum(p[0] for p in P) / 4; cy = sum(p[1] for p in P) / 4
    for (px, py), l in zip(P, labels):
        dx, dy = cx - px, cy - py
        d = math.hypot(dx, dy)
        s.append(text(px + dx / d * 34, py + dy / d * 34 + 6, l, 15, col=RED if l == "x" else INK, italic=l == "x"))
    return svg_wrap(300, 210, "".join(s), "quadrilateral, not drawn accurately")


def one_quad(r):
    a, b, c = r.randint(60, 120), r.randint(55, 125), r.randint(60, 130)
    x = 360 - a - b - c
    if not 40 <= x <= 160:
        return None
    k = r.randrange(4)
    vals = [a, b, c]
    labels = [lab(v) for v in vals]
    labels.insert(k, "x")
    svg = quad_svg(labels)
    e = "Angles in a quadrilateral add up to 360°: 360 − %d − %d − %d = <b>%d°</b>." % (a, b, c, x)
    return QN("Find %s.%s%s" % (B("<i>x</i>"), fig(svg), NOTE), x, [180 - a - b - c if 180 - a - b - c > 0 else x + 180, x - 20, 360 - a - b], e, unit=DEG)



# ------------------------------------------------------------ set 2: exterior angles and triangle facts
def one_ext(r):
    kind = r.choice(["ext", "ext", "ext_back", "fact"])
    if kind == "ext":
        a, b = r.randint(25, 80), r.randint(25, 80)
        q = "A triangle has interior angles of %d° and %d°. The side next to the third angle is extended. What is the exterior angle there?" % (a, b)
        return QN(q, a + b, [180 - a - b, 360 - a - b, 180 - a], "The exterior angle equals the sum of the two opposite interior angles: %d + %d = <b>%d°</b>. (Or 180 − third angle %d°.)" % (a, b, a + b, 180 - a - b), unit=DEG)
    if kind == "ext_back":
        ext = r.randint(100, 160)
        a = r.randint(30, ext - 30)
        q = "An exterior angle of a triangle is %d°. One of the opposite interior angles is %d°. Find the other opposite interior angle." % (ext, a)
        return QN(q, ext - a, [180 - ext, 180 - a, ext + a - 180 if ext + a > 180 else ext - a + 10], "Exterior angle = sum of the two opposite interior angles: %d − %d = <b>%d°</b>." % (ext, a, ext - a), unit=DEG)
    facts = [("What is each angle in an equilateral triangle?", "60°", ["90°", "180°", "45°"], "Three equal angles: 180 ÷ 3 = <b>60°</b>."),
             ("Can a triangle have two right angles?", "No, because 90° + 90° = 180° leaves nothing for the third angle", ["Yes, if it is isosceles", "Yes, the third angle is 0°", "Only in a square"], "<b>No.</b> Two right angles already make 180°."),
             ("Can a triangle have an obtuse angle and a right angle?", "No, because they would add to more than 180°", ["Yes", "Only if it is isosceles", "Only if the obtuse angle is 95°"], "<b>No.</b> 90° + more than 90° is already over 180°."),
             ("In a right-angled triangle, the two other angles add up to…", "90°", ["180°", "45°", "360°"], "180 − 90 = <b>90°</b>."),
             ("Why do the angles in a triangle add up to 180°?", "Torn off and placed together, they make a straight line", ["Because a triangle has 3 sides", "Because 3 × 60 = 180", "Because each angle is 60°"],
              "If you tear off the three corners and put them side by side, they <b>make a straight line</b>, which is 180°."),
             ("A triangle has angles 50°, 60° and 70°. What type of triangle is it?", "Acute-angled scalene", ["Right-angled isosceles", "Obtuse-angled", "Equilateral"], "All angles are less than 90° and all different: <b>acute-angled scalene</b>.")]
    q, a, w, e = r.choice(facts)
    return T(q, a, w, e)


NAMES = {3: "triangle", 4: "quadrilateral", 5: "pentagon", 6: "hexagon", 7: "heptagon", 8: "octagon", 9: "nonagon", 10: "decagon", 12: "dodecagon"}


def one_sum(r):
    n = r.choice(list(NAMES) + [15, 20])
    s = (n - 2) * 180
    name = NAMES.get(n, "%d-sided polygon" % n)
    if r.random() < 0.6 or n > 12:
        q = "What is the sum of the interior angles of a %s?" % B(name)
        e = "Sum = (<i>n</i> − 2) × 180° = (%d − 2) × 180 = <b>%s°</b>." % (n, num(s))
        return QN(q, s, [n * 180, (n - 1) * 180, 360], e, unit="°")
    known = []
    left = s
    for i in range(n - 1):
        v = r.randint(80, 175) if n > 4 else r.randint(50, 130)
        known.append(v)
    x = s - sum(known)
    if not 30 <= x <= 179:
        return None
    q = "A %s has angles of %s and <i>x</i>. Find <i>x</i>." % (name, ", ".join("%d°" % v for v in known))
    e = "The angles add up to %s°. <i>x</i> = %s − %s = <b>%d°</b>." % (num(s), num(s), num(sum(known)), x)
    return QN(q, x, [n * 180 - sum(known) if 0 < n * 180 - sum(known) < 400 else None, 360 - sum(known) if 360 - sum(known) > 0 else x + 180, x - 180 if x > 180 else x + 30], e, unit="°")


# ------------------------------------------------------------ set 3: regular polygons
def one_regular(r):
    n = r.choice([3, 4, 5, 6, 8, 9, 10, 12, 15, 18, 20, 24, 30, 36])
    ext = 360 / n
    inn = 180 - ext
    name = {3: "an equilateral triangle", 4: "a square"}.get(n, "a regular " + NAMES.get(n, "%d-sided polygon" % n))
    if r.random() < 0.5:
        q = "What is the size of each %s angle of %s?" % (B("exterior"), name)
        e = "Exterior angles add up to 360°. 360 ÷ %d = <b>%s°</b>." % (n, num(ext))
        return QN(q, ext, [inn, 180 / n if (180 / n) == int(180 / n) else ext + 10, (n - 2) * 180 / n * 2 if False else 360 - ext], e, unit="°")
    q = "What is the size of each %s angle of %s?" % (B("interior"), name)
    e = "Exterior angle = 360 ÷ %d = %s°. Interior = 180 − %s = <b>%s°</b>." % (n, num(ext), num(ext), num(inn))
    return QN(q, inn, [ext, n * 180 / n if False else 180 * (n - 1) / n if (180 * (n - 1)) % n == 0 else inn + 10, 360 - inn], e, unit="°")



# ------------------------------------------------------------ set 5: problems
def problems():
    its = []
    for q, ans, wr, e in [
        ("The angles of a triangle are <i>x</i>, <i>x</i> + 10 and <i>x</i> + 50. Find <i>x</i>.", 40, [60, 90, 50], "3<i>x</i> + 60 = 180, so 3<i>x</i> = 120 and <i>x</i> = <b>40°</b>."),
        ("The angles of a triangle are <i>x</i>, 2<i>x</i> and 3<i>x</i>. Find the largest angle.", 90, [30, 60, 180], "6<i>x</i> = 180, so <i>x</i> = 30 and 3<i>x</i> = <b>90°</b>."),
        ("Two angles in a triangle are 53° and 71°. What is the third angle?", 56, [236, 124, 66], "180 − 53 − 71 = <b>56°</b>."),
        ("The two base angles of an isosceles triangle are each 64°. What is the third angle?", 52, [116, 64, 128], "180 − 64 − 64 = <b>52°</b>."),
        ("Three angles of a quadrilateral are 85°, 110° and 95°. Find the fourth angle.", 70, [250, 110, 90], "360 − 85 − 110 − 95 = <b>70°</b>."),
        ("A kite has angles of 110°, 80° and 80°. What is the fourth angle?", 90, [10, 110, 270], "360 − 110 − 80 − 80 = <b>90°</b>."),
        ("A quadrilateral has angles <i>x</i>, 2<i>x</i>, 2<i>x</i> and 3<i>x</i>. Find <i>x</i>.", 45, [22.5, 90, 60], "8<i>x</i> = 360, so <i>x</i> = <b>45°</b>."),
        ("A pentagon has angles 100°, 110°, 120° and 95°. Find the fifth angle.", 115, [295, 35, 105], "The angles add up to 540°. 540 − 425 = <b>115°</b>."),
        ("A parallelogram has one angle of 65°. What are the other three angles?", None, None, None),
    ]:
        if ans is None:
            its.append(T(q, "65°, 115° and 115°", ["65°, 65° and 65°", "115°, 115° and 115°", "25°, 65° and 25°"],
                         "Opposite angles are equal and neighbouring angles add to 180°: <b>65°, 115° and 115°</b>."))
            continue
        from fractions import Fraction as F
        its.append(QN(q, ans, [F(str(w)) for w in wr], e, unit=DEG))
    data = [
        ("Can a triangle have angles of 100° and 85°?", "No, because 100° + 85° is already more than 180°", ["Yes, the third angle is −5°", "Yes, if it is isosceles", "No, because 100 is even"],
         "The three angles must add up to exactly 180°. So <b>no</b>."),
        ("Liam says the angles in a quadrilateral add up to 180°. Is he right?", "No, they add up to 360°", ["Yes", "No, they add up to 270°", "Only for a square"],
         "A quadrilateral can be split into two triangles: 2 × 180° = <b>360°</b>."),
        ("How many triangles can a hexagon be split into, using diagonals from one corner?", "4", ["6", "3", "5"], "A polygon with <i>n</i> sides splits into <i>n</i> − 2 triangles: 6 − 2 = <b>4</b>."),
        ("Why do the interior angles of a pentagon add up to 540°?", "It splits into 3 triangles from one corner", ["It has 5 sides and 5 × 108 = 540", "It is 360° + 90°", "Each angle is 90°"],
         "From one corner you can draw 2 diagonals, making 3 triangles: 3 × 180° = <b>540°</b>."),
        ("What is each interior angle of a regular hexagon?", "120°", ["60°", "108°", "720°"], "Sum = 720°. 720 ÷ 6 = <b>120°</b>."),
        ("Matilda says the interior angles of a hexagon add up to 6 × 180 = 1080°. What is the correct sum?", "720°", ["1080°", "360°", "900°"], "(6 − 2) × 180 = <b>720°</b>."),
        ("An isosceles triangle has one angle of 100°. What are the other two angles?", "40° and 40°", ["100° and 40°", "80° and 80°", "40° and 140°"],
         "100° must be the top angle (two 100° angles would be too big). (180 − 100) ÷ 2 = <b>40° each</b>."),
        ("An isosceles triangle has one angle of 70°. Which could be the other two angles?", "55° and 55°, or 70° and 40°", ["Only 55° and 55°", "Only 70° and 40°", "70° and 70°"],
         "If 70° is the top angle, the base angles are 55° each. If 70° is a base angle, the angles are 70°, 70° and 40°. <b>Both are possible.</b>"),
        ("The angles of a quadrilateral are all equal. What is each angle?", "90°", ["45°", "180°", "60°"], "360 ÷ 4 = <b>90°</b>."),
        ("What is the sum of the interior angles of an octagon?", "1080°", ["1440°", "720°", "360°"], "(8 − 2) × 180 = <b>1080°</b>."),
        ("A triangle has an exterior angle of 120° at one corner. What is the interior angle at that corner?", "60°", ["120°", "240°", "30°"], "They lie on a straight line: 180 − 120 = <b>60°</b>."),
    ]
    its += [T(q, a, w, e) for q, a, w, e in data]
    return its


def body():
    return lesson(
        "<p>The angles in a <b>triangle</b> add up to <b>180°</b>: tear off the corners and they make a straight line.</p>"
        "<ul><li>An <b>isosceles</b> triangle has two equal sides and two equal base angles.</li>"
        "<li>An <b>equilateral</b> triangle has three 60° angles.</li>"
        "<li>An <b>exterior angle</b> of a triangle equals the sum of the two opposite interior angles.</li>"
        "<li>A <b>quadrilateral</b> splits into 2 triangles, so its angles add up to 360°.</li>"
        "<li>A polygon with <i>n</i> sides splits into <i>n</i> − 2 triangles: angle sum = <b>(<i>n</i> − 2) × 180°</b>.</li></ul>",
        [("Two angles of a triangle are 48° and 75°. Find the third.", ["180 − 48 − 75."], "57°"),
         ("An isosceles triangle has a top angle of 40°. Find each base angle.", ["180 − 40 = 140.", "140 ÷ 2 = 70."], "70°"),
         ("Find the angle sum of a pentagon.", ["5 − 2 = 3 triangles.", "3 × 180."], "540°")],
        ["Using 360° for a triangle, or 180° for a quadrilateral.",
         "In an isosceles triangle, using the wrong pair of equal angles: the equal angles are opposite the equal sides.",
         "Using <i>n</i> × 180° for a polygon instead of (<i>n</i> − 2) × 180°.",
         "Forgetting that an exterior angle and its interior angle add to 180°."])


def main():
    sets = [S("Angles in a triangle", collect(one_tri, 20, R)),
            S("Exterior angles and triangle facts", collect(one_ext, 20, R)),
            S("Angles in a quadrilateral", collect(one_quad, 20, R)),
            S("Angle sums of polygons", collect(one_sum, 12, R) + collect(one_regular, 8, R)),
            S("Angle problems", problems())]
    make(7, "angle-sum-of-triangles-and-polygons", 17, "AC9M7M05",
         "Angle Sum of Triangles, Quadrilaterals and Polygons",
         "Year 7 Angle Sum Worksheets: Triangles, Quadrilaterals and Polygons (Free, Answer Key)",
         "Angle sums",
         "demonstrate that the interior angle sum of a triangle in the plane is 180° and apply this to determine the interior "
         "angle sum of other shapes and the size of unknown angles",
         "Free Year 7 maths worksheets on angle sums for the Australian Curriculum (AC9M7M05): angles in triangles, isosceles "
         "and right-angled triangles, exterior angles, quadrilaterals and polygons. 100 questions with an answer key.",
         "The angles in a triangle add up to 180°.",
         "A polygon with n sides splits into n − 2 triangles, so its angles add up to (n − 2) × 180°.",
         body(),
         [("Why do the angles in a triangle add up to 180°?", "Tear off the three corners and put them together: they make a straight line, which is 180°."),
          ("What do the angles in a quadrilateral add up to?", "360°, because a quadrilateral splits into two triangles."),
          ("How do I find the angle sum of any polygon?", "Use (n − 2) × 180°, where n is the number of sides. A hexagon: 4 × 180° = 720°."),
          ("What is the exterior angle of a triangle?", "The angle between one side and the extension of the next side. It equals the sum of the two opposite interior angles.")],
         sets, R)


if __name__ == "__main__":
    main()
