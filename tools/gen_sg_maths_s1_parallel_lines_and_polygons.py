# -*- coding: utf-8 -*-
"""
SG Secondary 1 Maths: Angles in Parallel Lines and Polygons (Sec 1 Geometry and measures)
  python3 gen_sg_maths_s1_parallel_lines_and_polygons.py
Corresponding, alternate and co-interior angles (with diagrams), the sum of interior angles of a polygon,
interior and exterior angles of regular polygons, finding the number of sides, and mixed problems.
Wrong answers come from real mistakes: treating co-interior angles as equal, using n × 180 for the angle sum,
mixing up interior and exterior angles, and dividing by the wrong number.
"""
import math
import random
from sg_sec import num, mcq, B, S, make, lesson, collect, QN, T, svg_wrap, line, text, fig, INK, RED, GREEN

R = random.Random(811400)
POS = {"UR": 0, "UL": 1, "LL": 2, "LR": 3}


def parallel_svg(theta, top_pos, top_lab, bot_pos, bot_lab):
    W, H = 340, 230
    y1, y2 = 70, 160
    cx1 = 170 + (y2 - y1) / 2 / math.tan(math.radians(theta))
    cx2 = 170 - (y2 - y1) / 2 / math.tan(math.radians(theta))
    s = [line(20, y1, W - 20, y1, INK, 2.5), line(20, y2, W - 20, y2, INK, 2.5)]
    for y in (y1, y2):     # parallel arrows
        s.append("<path d='M%d %d l-9 -6 M%d %d l-9 6' stroke='%s' stroke-width='2.5' fill='none'/>" % (W - 60, y, W - 60, y, INK))
    L = 120
    dx, dy = math.cos(math.radians(theta)), -math.sin(math.radians(theta))
    s.append(line(cx1 + dx * 70, y1 + dy * 70, cx2 - dx * 70, y2 - dy * 70, INK, 2.5))
    def lab(cx, cy, pos, t):
        mids = {"UR": theta / 2, "UL": theta + (180 - theta) / 2, "LL": 180 + theta / 2, "LR": 180 + theta + (180 - theta) / 2}
        a = math.radians(mids[pos])
        rr = 30 if (pos in ("UR", "LL") and theta < 50) or (pos in ("UL", "LR") and theta > 130) else 24
        return text(cx + math.cos(a) * rr, cy - math.sin(a) * rr + 6, t, 15, col=RED if t in ("x", "y") else INK, italic=t in ("x", "y"))
    s.append(lab(cx1, y1, top_pos, top_lab))
    s.append(lab(cx2, y2, bot_pos, bot_lab))
    return svg_wrap(W, H, "".join(s), "two parallel lines crossed by a transversal")


def val(theta, pos):
    return theta if pos in ("UR", "LL") else 180 - theta


def relation(tp, bp):
    if tp == bp:
        return "corresponding"
    if (tp, bp) in (("LL", "UR"), ("LR", "UL")):
        return "alternate"
    if (tp, bp) in (("LL", "UL"), ("LR", "UR")):
        return "co-interior"
    return None


# ------------------------------------------------------------ set 1: parallel lines with diagrams
def one_parallel(r):
    theta = r.choice([35, 40, 48, 55, 62, 65, 70, 72, 110, 115, 118, 125, 130, 138])
    tp = r.choice(list(POS))
    bp = r.choice(list(POS))
    rel = relation(tp, bp)
    if rel is None:
        return None
    given = val(theta, tp)
    x = val(theta, bp)
    svg = parallel_svg(theta, tp, "%d°" % given, bp, "x")
    q = "The two lines with arrows are parallel. Find %s.%s<br><small>Not drawn accurately.</small>" % (B("<i>x</i>"), fig(svg))
    if rel == "co-interior":
        e = "These are <b>co-interior</b> angles (a C shape), so they add up to 180°: <i>x</i> = 180 − %d = <b>%d°</b>." % (given, x)
    else:
        e = "These are <b>%s</b> angles (%s), so they are equal: <b><i>x</i> = %d°</b>." % (rel, "an F shape" if rel == "corresponding" else "a Z shape", x)
    return QN(q, x, [180 - x, 360 - given, 90 - given if given < 90 else given - 90], e, unit="°")


def one_name(r):
    theta = r.choice([50, 60, 65, 70, 115, 120])
    tp = r.choice(list(POS))
    bp = r.choice(list(POS))
    rel = relation(tp, bp)
    if rel is None:
        return None
    svg = parallel_svg(theta, tp, "a", bp, "b")
    names = {"corresponding": "Corresponding (equal)", "alternate": "Alternate (equal)", "co-interior": "Co-interior (add to 180°)"}
    right = names[rel]
    q = "The lines with arrows are parallel. What is the relationship between angles <i>a</i> and <i>b</i>?%s" % fig(svg)
    e = "Look for the shape: F for corresponding, Z for alternate, C (or U) for co-interior. These are <b>%s</b>." % right.lower()
    return T(q, right, [v for v in names.values() if v != right] + ["Vertically opposite (equal)"], e)


# ------------------------------------------------------------ set 2: interior angle sums
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


# ------------------------------------------------------------ set 4: number of sides
def one_sides(r):
    n = r.choice([5, 6, 8, 9, 10, 12, 15, 18, 20, 24, 30, 36])
    ext = 360 // n
    if 360 % n:
        return None
    if r.random() < 0.5:
        q = "Each exterior angle of a regular polygon is %d°. How many sides does it have?" % ext
        e = "360 ÷ %d = <b>%d sides</b>." % (ext, n)
        return QN(q, n, [w for w in [180 // ext if 180 % ext == 0 else n + 2, 360 - ext if 360 - ext < 200 else n - 2, ext] if w >= 3], e, unit=" sides")
    inn = 180 - ext
    q = "Each interior angle of a regular polygon is %d°. How many sides does it have?" % inn
    e = "Exterior angle = 180 − %d = %d°. 360 ÷ %d = <b>%d sides</b>." % (inn, ext, ext, n)
    return QN(q, n, [w for w in [round(360 / inn) if round(360 / inn) != n else n + 1, 180 // ext if 180 % ext == 0 and 180 // ext != n else n - 1, ext] if w >= 3], e, unit=" sides", near=(1, -1, 2, 4))


# ------------------------------------------------------------ set 5: problems
def problems():
    its = []
    data = [
        ("What do the exterior angles of any polygon add up to?", "360°", ["180°", "540°", "It depends on the number of sides"], "Walking round any polygon you turn through one full turn: <b>360°</b>."),
        ("Why do the interior angles of a pentagon add up to 540°?", "It can be split into 3 triangles from one vertex", ["It has 5 sides and 5 × 108 = 540", "It is 360° + 180°", "Each angle is 90°"],
         "From one vertex you can draw 2 diagonals, making 3 triangles: 3 × 180° = <b>540°</b>."),
        ("Can a regular polygon have an exterior angle of 25°?", "No, because 360 ÷ 25 is not a whole number", ["Yes, it has 25 sides", "Yes, it has 14 sides", "No, exterior angles must be 90°"],
         "360 ÷ 25 = 14.4, which is not a whole number of sides. So <b>no</b>."),
        ("An interior angle and its exterior angle add up to…", "180°", ["360°", "90°", "It depends on the polygon"], "They sit on a straight line, so they add up to <b>180°</b>."),
        ("In a triangle, one exterior angle is 125°. The opposite interior angles are 70° and <i>x</i>. Find <i>x</i>.", "55°", ["65°", "35°", "125°"],
         "The exterior angle equals the sum of the two opposite interior angles: <i>x</i> = 125 − 70 = <b>55°</b>."),
        ("What is the interior angle of a regular hexagon?", "120°", ["60°", "108°", "720°"], "Sum = 720°, ÷ 6 = <b>120°</b>."),
        ("Which regular polygons tessellate on their own?", "Triangles, squares and hexagons", ["Pentagons and octagons", "All regular polygons", "Only squares"],
         "Their interior angles (60°, 90°, 120°) divide exactly into 360°: <b>triangles, squares and hexagons</b>."),
        ("Co-interior angles between parallel lines are <i>x</i> and 2<i>x</i>. Find <i>x</i>.", "60°", ["90°", "120°", "45°"], "Co-interior angles add to 180°: 3<i>x</i> = 180, so <i>x</i> = <b>60°</b>."),
        ("Alternate angles are 3<i>x</i> + 10 and 70. Find <i>x</i>.", "20°", ["80°", "26.7°", "60°"], "Alternate angles are equal: 3<i>x</i> + 10 = 70, so <i>x</i> = <b>20°</b>."),
        ("A polygon has an interior angle sum of 1440°. How many sides does it have?", "10", ["8", "12", "9"], "(<i>n</i> − 2) × 180 = 1440, so <i>n</i> − 2 = 8 and <i>n</i> = <b>10</b>."),
        ("What is the interior angle of a regular octagon?", "135°", ["45°", "1080°", "120°"], "Exterior = 360 ÷ 8 = 45°. Interior = 180 − 45 = <b>135°</b>."),
        ("Ethan says the interior angles of a hexagon add up to 6 × 180 = 1080°. What is the correct sum?", "720°", ["1080°", "360°", "900°"], "(6 − 2) × 180 = <b>720°</b>."),
        ("A quadrilateral has angles <i>x</i>, 2<i>x</i>, 3<i>x</i> and 4<i>x</i>. What is the largest angle?", "144°", ["36°", "90°", "72°"], "10<i>x</i> = 360, so <i>x</i> = 36 and the largest is 4 × 36 = <b>144°</b>."),
        ("Five angles of a hexagon are 110°, 125°, 130°, 95° and 140°. Find the sixth angle.", "120°", ["300°", "540°", "60°"], "Total 720°. 720 − 600 = <b>120°</b>."),
        ("Which pair of angles are equal?", "Alternate angles", ["Co-interior angles", "Angles on a straight line", "Angles in a triangle"], "<b>Alternate angles</b> (Z shape) are equal. Co-interior angles add to 180°."),
        ("A regular polygon has interior angles of 150°. How many sides does it have?", "12", ["10", "15", "30"], "Exterior = 30°. 360 ÷ 30 = <b>12</b>."),
        ("In an isosceles triangle, the angle between the equal sides is 40°. A line parallel to the base is drawn across. What is the angle it makes with one of the equal sides (corresponding to a base angle)?", "70°", ["40°", "140°", "50°"],
         "Base angles = (180 − 40) ÷ 2 = 70°. The corresponding angle is equal: <b>70°</b>."),
        ("What is the sum of the interior angles of a 20-sided polygon?", "3240°", ["3600°", "3420°", "360°"], "(20 − 2) × 180 = <b>3240°</b>."),
        ("What is each exterior angle of an equilateral triangle?", "120°", ["60°", "180°", "90°"], "360 ÷ 3 = <b>120°</b>."),
        ("Two angles are co-interior between parallel lines. One is 4 times the other. What is the smaller angle?", "36°", ["45°", "144°", "72°"], "<i>x</i> + 4<i>x</i> = 180, so <i>x</i> = <b>36°</b>."),
    ]
    for q, a, w, e in data:
        its.append(T(q, a, w, e))
    return its


def body():
    return lesson(
        "<p>When a line crosses two <b>parallel</b> lines:</p><ul>"
        "<li><b>Corresponding</b> angles (F shape) are equal.</li><li><b>Alternate</b> angles (Z shape) are equal.</li>"
        "<li><b>Co-interior</b> angles (C shape) add up to 180°.</li></ul>"
        "<p>The interior angles of a polygon with <i>n</i> sides add up to <b>(<i>n</i> − 2) × 180°</b>. The exterior angles "
        "of any polygon add up to <b>360°</b>. For a regular polygon, exterior angle = 360° ÷ <i>n</i> and interior = 180° − exterior.</p>"
        + fig(parallel_svg(65, "UR", "65°", "UR", "x")),
        [("Find <i>x</i> in the diagram above.", ["The angles are corresponding (F shape)."], "<i>x</i> = 65°"),
         ("Find the interior angle of a regular pentagon.", ["Exterior = 360 ÷ 5 = 72°.", "Interior = 180 − 72."], "108°")],
        ["Thinking co-interior angles are equal. They add up to 180°.",
         "Using <i>n</i> × 180° for the angle sum instead of (<i>n</i> − 2) × 180°.",
         "Mixing up interior and exterior angles of a regular polygon.",
         "Using these rules when the lines are not parallel (look for the arrows)."])


def main():
    sets = [S("Angles in parallel lines", collect(one_parallel, 14, R) + collect(one_name, 6, R)),
            S("Interior angle sums", collect(one_sum, 20, R)),
            S("Regular polygons", collect(one_regular, 20, R)),
            S("Finding the number of sides", collect(one_sides, 20, R)),
            S("Problems", problems())]
    make(1, "parallel-lines-and-polygons", 13, "G1",
         "Angles in Parallel Lines and Polygons",
         "Secondary 1 Angles Worksheets: Corresponding, Alternate and Co-interior Angles, Polygon Interior and Exterior Angles",
         "Parallel lines and polygons",
         "Understand and use the relationship between parallel lines and alternate and corresponding angles; derive and "
         "use the sum of angles in a triangle and use it to deduce the angle sum in any polygon, and to derive properties "
         "of regular polygons.",
         "Free Secondary 1 angles worksheets with diagrams: corresponding, alternate and co-interior angles, interior angle sums, "
         "interior and exterior angles of regular polygons and number of sides. 100 questions with answers.",
         "Corresponding and alternate angles are equal; co-interior angles add up to 180°.",
         "Interior angle sum = (n − 2) × 180°. Exterior angles add up to 360°.",
         body(),
         [("What are corresponding, alternate and co-interior angles?", "Angles made when a line crosses parallel lines. Corresponding (F) and alternate (Z) angles are equal; co-interior (C) angles add up to 180°."),
          ("How do I find the sum of the interior angles of a polygon?", "Use (n − 2) × 180°, where n is the number of sides. A hexagon: 4 × 180° = 720°."),
          ("How do I find each interior angle of a regular polygon?", "Find the exterior angle (360° ÷ n) and subtract it from 180°."),
          ("How do I find the number of sides from an angle?", "Find the exterior angle and divide 360° by it.")],
         sets, R)


if __name__ == "__main__":
    main()
