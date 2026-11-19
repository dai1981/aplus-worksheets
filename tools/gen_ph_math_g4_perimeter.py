# -*- coding: utf-8 -*-
"""
Philippines Grade 4 Math (MATATAG): Perimeter of Quadrilaterals and Composite Figures (Grade 4: Measurement and Geometry)
  python3 tools/gen_ph_math_g4_perimeter.py
Perimeter by adding sides (US Grade 3 maker with Filipino names), perimeter of trapezoids, parallelograms, kites and
other quadrilaterals, composite figures made of triangles and quadrilaterals (own makers), rectilinear shapes (UK Year 4
maker) and missing sides.
Wrong answers come from real mistakes: counting an inside line, leaving out a side, and multiplying instead of adding.
"""
import ph_common
from ph_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, peso, words)
import random
import gen_us_math_g3_perimeter as us3
adopt(us3)
if hasattr(us3, 'R'): us3.R = random.Random(704030)
import gen_uk_maths_y4_area_perimeter as uka
adopt(uka)
if hasattr(uka, 'R'): uka.R = random.Random(704031)
ph_common.GRADE = "grade-4"

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


from ws_common import svg_wrap, text, GREEN, FILL, INK


def poly_svg(pts, labels, label="figure", dashed=None):
    """pts: polygon corners (any units); labels: text for each side pts[i] -> pts[i+1] (None to skip)."""
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    W, H = 300, 170
    s = min((W - 90) / max(1, max(xs) - min(xs)), (H - 60) / max(1, max(ys) - min(ys)))
    P = [(45 + (x - min(xs)) * s, 30 + (y - min(ys)) * s) for x, y in pts]
    cx, cy = sum(p[0] for p in P) / len(P), sum(p[1] for p in P) / len(P)
    b = "<polygon points='%s' fill='%s' stroke='%s' stroke-width='2.5'/>" % (" ".join("%.1f,%.1f" % p for p in P), FILL, GREEN)
    if dashed:
        (i, j) = dashed
        b += "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2' stroke-dasharray='5 4'/>" % (P[i][0], P[i][1], P[j][0], P[j][1], INK)
    for i, t in enumerate(labels):
        if t is None:
            continue
        a, c = P[i], P[(i + 1) % len(P)]
        mx, my = (a[0] + c[0]) / 2, (a[1] + c[1]) / 2
        dx, dy = mx - cx, my - cy
        d = max(1.0, (dx * dx + dy * dy) ** 0.5)
        b += text(mx + dx / d * 20, my + dy / d * 18 + 5, t, 15)
    return svg_wrap(W, H + 10, b, label)


QUADS = [("trapezoid", lambda r: [(0, 0), (r[0], 0), (r[0] - 1.2, 2.4), (1.4, 2.4)]),
         ("parallelogram", lambda r: [(0, 0), (r[0], 0), (r[0] + 1.5, 2.4), (1.5, 2.4)]),
         ("kite", lambda r: [(2, 0), (4, 1.4), (2, 4.5), (0, 1.4)]),
         ("quadrilateral", lambda r: [(0, 0), (r[0], 0.6), (r[0] - 0.5, 2.8), (0.7, 2.2)])]
UNIT = ["cm", "m"]


def one_quad(r):
    name, f = r.choice(QUADS)
    u = r.choice(UNIT)
    if name == "parallelogram":
        a, b = r.randint(6, 25), r.randint(4, 18)
        sides = [a, b, a, b]
        labels = ["%d %s" % (a, u), "%d %s" % (b, u), None, None]
        q = "This parallelogram has opposite sides of equal length. What is its perimeter?"
        e = "Opposite sides are equal: %d + %d + %d + %d = %d %s." % (a, b, a, b, 2 * (a + b), u)
        wr = [a + b, a * b, 2 * a + b]
    elif name == "kite":
        a, b = r.randint(4, 15), r.randint(8, 25)
        if a == b:
            raise AssertionError
        sides = [a, b, b, a]
        labels = ["%d %s" % (a, u), "%d %s" % (b, u), None, None]
        q = "A kite has two pairs of equal sides next to each other. What is its perimeter?"
        e = "The sides are %d, %d, %d and %d: %d + %d + %d + %d = %d %s." % (a, b, b, a, a, b, b, a, 2 * (a + b), u)
        wr = [a + b, a * b, a + 2 * b]
    else:
        sides = [r.randint(5, 30) for _ in range(4)]
        if len(set(sides)) < 3:
            raise AssertionError
        labels = ["%d %s" % (s, u) for s in sides]
        q = "What is the perimeter of this %s?" % name
        e = "Add all four sides: %s = %d %s." % (" + ".join(str(s) for s in sides), sum(sides), u)
        wr = [sum(sides) - sides[1], sum(sides[:2]) * 2, sum(sides) + sides[0]]
    pts = f([4.5 if name != "kite" else 0])
    p = sum(sides)
    return mcq(fig(poly_svg(pts, labels, "%s with side lengths" % name)) + q, "%d %s" % (p, u), ["%d %s" % (w, u) for w in wr if w != p] + ["%d %s" % (p + 2, u)], e)


def one_comp(r):
    u = r.choice(UNIT)
    kind = r.choice(["house", "house", "rt", "trap"])
    if kind == "house":
        w, h, s = r.choice([8, 10, 12, 14, 16, 18, 20]), r.randint(5, 14), None
        s = r.randint(w // 2 + 1, w)
        pts = [(0, 1.6), (2, 0), (4, 1.6), (4, 4), (0, 4)]
        labels = ["%d %s" % (s, u), "%d %s" % (s, u), "%d %s" % (h, u), "%d %s" % (w, u), "%d %s" % (h, u)]
        P = 2 * s + 2 * h + w
        q = "A square or rectangle with a triangle on top makes this figure. What is the perimeter of the whole figure?"
        e = "Go around the outside only (not the dashed line): %d + %d + %d + %d + %d = %d %s." % (s, s, h, w, h, P, u)
        wr = [P + w, 2 * (w + h), P - s]
        dashed = (0, 2)
    elif kind == "rt":
        a, b = r.randint(6, 15), r.randint(5, 12)
        c = {(3, 4): 5}.get((a, b), None)
        a, b, c = r.choice([(6, 8, 10), (9, 12, 15), (5, 12, 13), (8, 15, 17), (12, 16, 20), (6, 8, 10)])
        L = r.randint(8, 20)
        pts = [(0, 0), (3, 0), (3, 2.2), (0, 2.2), (-1.6, 2.2)]
        pts = [(0, 0), (4, 0), (4, 2.5), (0, 2.5), (-2.4, 2.5)]
        labels = ["%d %s" % (L, u), "%d %s" % (b, u), "%d %s" % (L, u), "%d %s" % (a, u), "%d %s" % (c, u)]
        P = L + b + L + a + c
        q = "A rectangle and a right triangle are joined to make this figure. What is its perimeter?"
        e = "Add the outside sides: %d + %d + %d + %d + %d = %d %s." % (L, b, L, a, c, P, u)
        wr = [P + b, 2 * (L + b), P - c]
        dashed = (0, 3)
    else:
        a, b, h = r.randint(10, 20), r.randint(4, 9), r.randint(4, 10)
        sl = r.randint(h + 1, h + 6)
        pts = [(0, 3), (1.2, 0), (4.2, 0), (5.4, 3)]
        labels = ["%d %s" % (sl, u), "%d %s" % (b, u), "%d %s" % (sl, u), "%d %s" % (a, u)]
        P = 2 * sl + a + b
        q = "This trapezoid has two equal slanted sides. What is its perimeter?"
        e = "%d + %d + %d + %d = %d %s." % (sl, b, sl, a, P, u)
        wr = [sl + a + b, 2 * (a + b), P + h]
        dashed = None
    return mcq(fig(poly_svg(pts, labels, "composite figure with side lengths", dashed)) + q, "%d %s" % (P, u), ["%d %s" % (w, u) for w in wr if w != P] + ["%d %s" % (P + 1, u)], e)


def build():
    sets, R = build_sets([
        ("Add the sides", [("run", us3.set_add, ("rnd",), 20)]),
        ("Perimeter of quadrilaterals", [("collect", uniq(one_quad), 20)]),
        ("Composite figures", [("collect", uniq(one_comp), 20)]),
        ("Rectilinear shapes", [("run", uka.set_rectilinear, ("rnd",), 20)]),
        ("Missing sides and word problems", [("run", us3.set_missing, ("rnd",), 10), ("run", uka.set_story, ("rnd", uka.People), 10)]),
    ], 70403)
    finish(sets, R)
    body = lesson('<ul><li>The <b>perimeter</b> is the distance around a figure. Add the lengths of all the outside sides.</li><li>Equal sides help: a parallelogram has 2 pairs of equal opposite sides, a kite has 2 pairs of equal sides next to each other.</li><li>For a composite figure, go around the <b>outside</b> only. Lines inside the figure are not part of the perimeter.</li><li>Write the unit (cm or m) in the answer.</li></ul>',
        [example("House shape: square sides 10 cm, roof sides 7 cm", ["Outside: 7 + 7 + 10 + 10 + 10"], "44 cm")],
        [['Counting an inside line', 'Only the outside counts.'], ['Leaving out a side', 'Count the sides before adding.'], ['Multiplying the sides', 'Perimeter is a sum; area uses multiplication.']])
    faq = [('What does MATATAG Math 4 ask about perimeter?', 'Find the perimeter of quadrilaterals that are not squares or rectangles, and find the perimeter of composite figures composed of triangles and quadrilaterals.'), ('What unit is perimeter in?', 'A unit of length, like cm or m.'), ('Is perimeter the same as area?', 'No. Perimeter is the distance around; area is the space inside.'), ('How do I find a missing side?', 'Subtract the known sides from the perimeter.')]
    make('perimeter', 3, 'Measurement and Geometry', 'Grade 4: Measurement and Geometry',
         'Find the perimeter of quadrilaterals that are not squares or rectangles; find the perimeter of composite figures composed of triangles and quadrilaterals.',
         'Perimeter of Quadrilaterals and Composite Figures', 'Perimeter',
         'Free Grade 4 perimeter worksheets for the DepEd MATATAG curriculum: perimeter of trapezoids, parallelograms, kites and composite figures made of triangles and quadrilaterals. 100 questions with answers.',
         'Perimeter: add all the outside sides.', 'Lines inside a composite figure do not count.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
