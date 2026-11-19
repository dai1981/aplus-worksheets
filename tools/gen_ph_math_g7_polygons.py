# -*- coding: utf-8 -*-
"""
Philippines Grade 7 Math (MATATAG): Polygons: Regular and Irregular, Convex and Non-Convex, and Constructing Triangles (Grade 7: Measurement and Geometry)
  python3 tools/gen_ph_math_g7_polygons.py
Names of polygons, regular and irregular polygons, convex and non-convex polygons (own makers with drawings), and
which side lengths and angle measures make a triangle (US Grade 7 makers).
Wrong answers come from real mistakes: calling a polygon regular when only the sides are equal, mixing up
heptagon and hexagon, and forgetting that the angles of a triangle add up to 180°.
"""
import ph_common
from ph_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, peso, words)
import random
import gen_us_math_g7_constructing_triangles as uct
adopt(uct)
if hasattr(uct, 'R'): uct.R = random.Random(707010)
ph_common.GRADE = "grade-7"

def uniq(fn):
    """Never give the same question twice, even with other wrong answers."""
    seen = set()
    def f(r):
        it = fn(r)
        if it is None or it["q"] in seen:
            raise AssertionError("repeat")
        seen.add(it["q"])
        return it
    f.__name__ = fn.__name__
    return f


import math
from ws_common import svg_wrap, text, GREEN, FILL, INK

PNAME = {3: "triangle", 4: "quadrilateral", 5: "pentagon", 6: "hexagon", 7: "heptagon", 8: "octagon", 9: "nonagon", 10: "decagon", 12: "dodecagon"}


def shape_svg(pts, label):
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    W, H = 220, 180
    s = min((W - 40) / (max(xs) - min(xs)), (H - 40) / (max(ys) - min(ys)))
    P = [(20 + (x - min(xs)) * s, 20 + (y - min(ys)) * s) for x, y in pts]
    b = "<polygon points='%s' fill='%s' stroke='%s' stroke-width='2.5'/>" % (" ".join("%.1f,%.1f" % p for p in P), FILL, GREEN)
    return svg_wrap(W, H, b, label)


def regular(n, rot=0.0):
    return [(math.cos(rot + 2 * math.pi * k / n), math.sin(rot + 2 * math.pi * k / n)) for k in range(n)]


def irregular(r, n):
    for _ in range(200):
        angs = sorted(r.uniform(0, 2 * math.pi) for _ in range(n))
        gaps = [(angs[(i + 1) % n] - angs[i]) % (2 * math.pi) for i in range(n)]
        if min(gaps) > 0.6 * 2 * math.pi / n and max(gaps) < 1.6 * 2 * math.pi / n:
            rad = [r.uniform(0.75, 1.0) for _ in range(n)]
            return [(rad[i] * math.cos(a), rad[i] * math.sin(a)) for i, a in enumerate(angs)]
    raise AssertionError


def concave(r, n):
    pts = regular(n, r.uniform(0, 1))
    k = r.randrange(n)
    pts[k] = (pts[k][0] * 0.3, pts[k][1] * 0.3)
    return pts


def one_pname(r):
    n = r.choice([5, 6, 7, 8, 9, 10, 12])
    if r.random() < 0.5:
        right = PNAME[n]
        wr = [PNAME[m] for m in (n - 1, n + 1, n + 2 if n + 2 in PNAME else 5) if m in PNAME and m != n]
        return mcq("What do you call a polygon with %d sides?" % n, right, wr + ["dodecagon" if n != 12 else "heptagon"],
                   "A polygon with %d sides and %d angles is a <b>%s</b>." % (n, n, right))
    right = n
    return mcq("How many sides does a %s have?" % PNAME[n], right, [n - 1, n + 1, n + 2], "A %s has <b>%d</b> sides and %d angles." % (PNAME[n], n, n))


def one_desc(r):
    n = r.choice([5, 6, 8, 10])
    side = r.randint(3, 15)
    kind = r.choice(["per", "side", "ang"])
    ia = (n - 2) * 180 // n
    if kind == "per":
        return mcq("A regular %s has sides of %d cm. What is its perimeter?" % (PNAME[n], side), "%d cm" % (n * side), ["%d cm" % x for x in ((n - 1) * side, side * side, n + side)],
                   "A regular %s has %d equal sides: %d × %d = <b>%d cm</b>." % (PNAME[n], n, n, side, n * side))
    if kind == "side":
        return mcq("A regular %s has a perimeter of %d cm. How long is each side?" % (PNAME[n], n * side), "%d cm" % side, ["%d cm" % x for x in (side + 1, n * side // 2, side * 2)],
                   "%d ÷ %d = <b>%d cm</b>." % (n * side, n, side))
    return mcq("You draw a regular %s with a protractor. How big must each interior angle be?" % PNAME[n], "%d°" % ia, ["%d°" % x for x in (360 // n, 180 - 360 // n + 10, ia + 12)],
               "The angles add up to (%d − 2) × 180° = %s°. Each angle: %s ÷ %d = <b>%d°</b>." % (n, comma((n - 2) * 180), comma((n - 2) * 180), n, ia))


def one_reg(r):
    n = r.choice([3, 4, 5, 6, 8, 10])
    kind = r.choice(["reg", "sides", "angles", "both"])
    ia = (n - 2) * 180 / n
    ia_s = ("%g" % ia)
    side = r.randint(2, 12)
    if kind == "reg":
        q = "A %s has all sides %d cm long and all angles %s°. Is it regular or irregular?" % (PNAME[n], side, ia_s)
        right = "Regular: equal sides and equal angles"
    elif kind == "sides":
        q = "A %s has all sides %d cm long, but its angles are not all equal. Is it regular or irregular?" % (PNAME[n], side)
        right = "Irregular: the angles are not all equal"
    elif kind == "angles":
        q = "A %s has all angles %s°, but its sides are not all the same length. Is it regular or irregular?" % (PNAME[n], ia_s)
        right = "Irregular: the sides are not all equal"
    else:
        q = "A %s has sides of different lengths and angles of different sizes. Is it regular or irregular?" % PNAME[n]
        right = "Irregular: neither sides nor angles are equal"
    opts = ["Regular: equal sides and equal angles", "Irregular: the angles are not all equal", "Irregular: the sides are not all equal",
            "Irregular: neither sides nor angles are equal", "Regular: equal sides are enough", "Regular: equal angles are enough"]
    wr = [o for o in opts if o != right]
    r.shuffle(wr)
    if kind in ("sides", "angles"):
        wr = [o for o in wr if not o.startswith("Irregular")][:2] + [o for o in wr if o.startswith("Irregular")][:1]
    return mcq(q, right, wr, "A polygon is <b>regular</b> only when all its sides are equal <b>and</b> all its angles are equal. %s." % right)


def one_convex(r):
    n = r.choice([5, 6, 7, 8])
    kind = r.choice(["reg", "irr", "con", "con"])
    pts = regular(n, r.uniform(0, 1)) if kind == "reg" else irregular(r, n) if kind == "irr" else concave(r, n)
    ans = {"reg": "Regular and convex", "irr": "Irregular and convex", "con": "Irregular and non-convex"}[kind]
    opts = ["Regular and convex", "Irregular and convex", "Irregular and non-convex", "Regular and non-convex"]
    why = {"reg": "All sides and angles are equal, and every interior angle is less than 180°.",
           "irr": "The sides are not all equal, but every interior angle is less than 180°: no corner points inward.",
           "con": "One corner points inward: that interior angle is more than 180°, so it is non-convex (concave). Its sides are not all equal."}[kind]
    return mcq(fig(shape_svg(pts, "a %s" % PNAME[n])) + "How do you classify this %s?" % PNAME[n],
               ans, [o for o in opts if o != ans], why + " <b>%s</b>." % ans)


def build():
    sets, R = build_sets([
        ("Names and measures of polygons", [("collect", uniq(one_pname), 12), ("collect", uniq(one_desc), 8)]),
        ("Regular or irregular?", [("collect", uniq(one_reg), 20)]),
        ("Convex or non-convex?", [("collect", one_convex, 20)]),
        ("Which sides make a triangle?", [("run", uct.set_sides, (), 14), ("run", uct.set_classify, (), 6)]),
        ("Which angles make a triangle?", [("run", uct.set_angles, (), 20)]),
    ], 70701)
    finish(sets, R)
    body = lesson('<ul><li>A <b>polygon</b> is a closed figure made of straight sides. Pentagon 5, hexagon 6, heptagon 7, octagon 8, nonagon 9, decagon 10 sides.</li><li>A <b>regular</b> polygon has all sides equal <b>and</b> all angles equal. Otherwise it is <b>irregular</b>.</li><li>A <b>convex</b> polygon has every interior angle less than 180°. A <b>non-convex</b> (concave) polygon has a corner that points inward.</li><li>To draw a triangle with a ruler and protractor, the angles must add up to 180°, and the two shorter sides must add up to more than the longest side.</li></ul>',
        [example("A hexagon with all sides 4 cm, angles 120°", ["equal sides", "equal angles"], "regular hexagon")],
        [['Only equal sides', 'A rhombus has equal sides but is not regular.'], ['Hexagon or heptagon?', 'Hexa- is 6, hepta- is 7.'], ['Angles that do not add to 180°', 'Then no triangle can be drawn.']])
    faq = [('What does MATATAG Math 7 ask about polygons?', 'Draw and describe regular and irregular polygons with 5, 6, 8, or 10 sides using a ruler and protractor, draw triangles, quadrilaterals and regular polygons with given angle measures, and classify polygons by the number of sides, whether they are regular, and whether they are convex.'), ('Is a square a regular polygon?', 'Yes: 4 equal sides and 4 right angles.'), ('What is a concave polygon?', 'Another name for a non-convex polygon.'), ('How do I draw a regular pentagon?', 'Draw 5 equal sides, turning so each interior angle is 108°.')]
    make('classifying-and-drawing-polygons', 1, 'Measurement and Geometry', 'Grade 7: Measurement and Geometry',
         'Draw and describe regular and irregular polygons with 5, 6, 8, or 10 sides based on measurements of sides and angles, using a ruler and protractor; draw triangles, quadrilaterals, and regular polygons (5, 6, 8, or 10 sides) with given angle measures; classify polygons according to the number of sides, whether they are regular or irregular, and whether they are convex or non-convex.',
         'Polygons: Regular and Irregular, Convex and Non-Convex, and Constructing Triangles', 'Polygons',
         'Free Grade 7 polygons worksheets for the DepEd MATATAG curriculum: names of polygons, regular and irregular, convex and non-convex, and constructing triangles. 100 questions with answers.',
         'Regular: all sides equal and all angles equal.', 'Convex: every interior angle is less than 180°.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
