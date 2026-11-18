# -*- coding: utf-8 -*-
"""
SG Secondary 1 Maths: Angles (Sec 1 Geometry and measures)
  python3 gen_sg_maths_s1_angles_triangles_and_quadrilaterals.py
Angles on a straight line, around a point, vertically opposite angles, angles in triangles and
quadrilaterals, and problems with algebra. Diagrams are inline SVG, drawn roughly to scale.
Wrong answers come from real mistakes: using 360° on a line, 180° around a point, thinking vertically
opposite angles add to 180°, and using 180° for a quadrilateral.
"""
import math
import random
from sg_sec import num, mcq, B, S, make, lesson, collect, QN, T, svg_wrap, line, text, fig, GREEN, INK, RED, FONT

R = random.Random(811300)
DEG = "°"


def pol(cx, cy, rr, deg):
    a = math.radians(deg)
    return cx + rr * math.cos(a), cy - rr * math.sin(a)


def arc(cx, cy, rr, a1, a2, col=GREEN):
    """Arc from angle a1 to a2 (degrees, anticlockwise)."""
    x1, y1 = pol(cx, cy, rr, a1)
    x2, y2 = pol(cx, cy, rr, a2)
    large = 1 if (a2 - a1) % 360 > 180 else 0
    return "<path d='M%.1f %.1f A%d %d 0 %d 0 %.1f %.1f' fill='none' stroke='%s' stroke-width='2'/>" % (x1, y1, rr, rr, large, x2, y2, col)


def rays(dirs, labels, w=300, h=200, cx=None, cy=None, extend=()):
    """Rays from a centre. dirs: angles in degrees (anticlockwise from east), labels between dirs[i] and dirs[i+1]."""
    cx = w / 2 if cx is None else cx
    cy = h / 2 if cy is None else cy
    L = min(w, h) * 0.46
    s = []
    for d in dirs:
        x, y = pol(cx, cy, L, d)
        s.append(line(cx, cy, x, y, INK, 2.5))
    n = len(dirs)
    for i, lab in enumerate(labels):
        if lab is None:
            continue
        a1, a2 = dirs[i], dirs[(i + 1) % n]
        span = (a2 - a1) % 360
        rr = (20 + 11 * (i % 2)) if span > 40 else 34
        if abs(span - 90) < 0.5:
            p1 = pol(cx, cy, 16, a1); p2 = pol(cx, cy, 16 * 1.414, a1 + 45); p3 = pol(cx, cy, 16, a2)
            s.append("<path d='M%.1f %.1f L%.1f %.1f L%.1f %.1f' fill='none' stroke='%s' stroke-width='2'/>" % (p1 + p2 + p3 + (GREEN,)))
        else:
            s.append(arc(cx, cy, rr, a1, a2))
        mid = a1 + span / 2
        tx, ty = pol(cx, cy, max(rr, 26) + 24 + (8 if span < 35 else 0), mid)
        s.append(text(tx, ty + 6, lab, 16, col=RED if lab.startswith("<tspan") or lab in ("x", "y") else INK, italic=lab in ("x", "y", "a", "b")))
    s.append("<circle cx='%.1f' cy='%.1f' r='3' fill='%s'/>" % (cx, cy, INK))
    return svg_wrap(w, h, "".join(s), "angle diagram, not drawn accurately")


def lab(v):
    return "%d%s" % (v, DEG)


NOTE = "<br><small>Not drawn accurately.</small>"


# ------------------------------------------------------------ set 1: straight line
def one_line(r):
    a = r.randint(25, 155)
    if r.random() < 0.6:
        x = 180 - a
        svg = rays([0, x, 180], ["x", lab(a)], h=150, cy=120)
        q = "Find the angle %s.%s%s" % (B("<i>x</i>"), fig(svg), NOTE)
        e = "Angles on a straight line add up to 180°: 180 − %d = <b>%d°</b>." % (a, x)
        return QN(q, x, [360 - a, a, 90 - a if a < 90 else a - 90], e, unit=DEG)
    b = r.randint(20, 160 - a)
    x = 180 - a - b
    if x < 15 or b < 15:
        return None
    svg = rays([0, a, a + b, 180], [lab(a), lab(b), "x"], h=150, cy=120)
    q = "Find the angle %s.%s%s" % (B("<i>x</i>"), fig(svg), NOTE)
    e = "Angles on a straight line add up to 180°: 180 − %d − %d = <b>%d°</b>." % (a, b, x)
    return QN(q, x, [360 - a - b, a + b, 180 - a], e, unit=DEG)


# ------------------------------------------------------------ set 2: around a point
def one_point(r):
    n = r.choice([3, 3, 4])
    angs = []
    left = 360
    for i in range(n - 1):
        v = r.randint(40, min(170, left - 40 * (n - 1 - i)))
        angs.append(v)
        left -= v
    x = left
    if x < 30 or x > 200 or any(v > 179 for v in angs) and r.random() < 0.5:
        return None
    k = r.randrange(n)
    allv = angs[:k] + [x] + angs[k:]
    dirs = [10]
    for v in allv[:-1]:
        dirs.append(dirs[-1] + v)
    labels = [("x" if i == k else lab(v)) for i, v in enumerate(allv)]
    svg = rays(dirs, labels, w=300, h=260)
    q = "Find the angle %s.%s%s" % (B("<i>x</i>"), fig(svg), NOTE)
    e = "Angles around a point add up to 360°: 360 − %s = <b>%d°</b>." % (" − ".join(str(v) for v in angs), x)
    return QN(q, x, [180 - sum(angs) if 180 - sum(angs) > 0 else sum(angs), x - 180 if x > 180 else x + 180, sum(angs)], e, unit=DEG)


# ------------------------------------------------------------ set 3: vertically opposite
def one_vopp(r):
    a = r.randint(30, 150)
    if abs(a - 90) < 8:
        return None
    rot = r.randint(-10, 20)
    dirs = [rot, rot + a, rot + 180, rot + 180 + a]
    which = r.choice(["opp", "adj"])
    if which == "opp":
        labels = [lab(a), None, "x", None]
        x = a
        e = "Vertically opposite angles are equal, so <b><i>x</i> = %d°</b>." % a
        wr = [180 - a, 360 - a, 90 - a if a < 90 else a - 90]
    else:
        labels = [lab(a), "x", None, None]
        x = 180 - a
        e = "<i>x</i> and %d° are on a straight line, so <i>x</i> = 180 − %d = <b>%d°</b>." % (a, a, x)
        wr = [a, 360 - a, 360 - 2 * a if 360 - 2 * a > 0 else a + 90]
    svg = rays(dirs, labels, w=300, h=220)
    q = "Two straight lines cross. Find %s.%s%s" % (B("<i>x</i>"), fig(svg), NOTE)
    return QN(q, x, wr, e, unit=DEG)


def one_vopp2(r):
    a = r.randint(35, 145)
    if abs(a - 90) < 8:
        return None
    dirs = [0, a, 180, 180 + a]
    labels = [lab(a), "x", "y", None]
    svg = rays(dirs, labels, w=300, h=220)
    y = a
    q = "Two straight lines cross. Find %s.%s%s" % (B("<i>y</i>"), fig(svg), NOTE)
    e = "<i>y</i> is vertically opposite %d°, so <b><i>y</i> = %d°</b>. (And <i>x</i> = 180 − %d = %d°.)" % (a, a, a, 180 - a)
    return QN(q, y, [180 - a, 360 - a, 90], e, unit=DEG)


# ------------------------------------------------------------ set 4: triangles and quadrilaterals
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


# ------------------------------------------------------------ set 5: types, algebra and reasoning
def problems():
    its = []
    for ang, typ in [(35, "Acute"), (90, "Right angle"), (128, "Obtuse"), (215, "Reflex"), (179, "Obtuse"), (300, "Reflex")]:
        all_t = ["Acute", "Right angle", "Obtuse", "Reflex"]
        its.append(T("What type of angle is %s?" % B(lab(ang)), typ, [t for t in all_t if t != typ],
                     "Acute: less than 90°. Right: 90°. Obtuse: between 90° and 180°. Reflex: between 180° and 360°. So %d° is <b>%s</b>." % (ang, typ.lower())))
    for q, ans, wr, e in [
        ("Angles on a straight line are 2<i>x</i> and 3<i>x</i>. Find <i>x</i>.", 36, [72, 30, 18], "2<i>x</i> + 3<i>x</i> = 180, so 5<i>x</i> = 180 and <i>x</i> = <b>36°</b>."),
        ("Angles around a point are <i>x</i>, 2<i>x</i>, 3<i>x</i> and 4<i>x</i>. Find <i>x</i>.", 36, [18, 90, 40], "10<i>x</i> = 360, so <i>x</i> = <b>36°</b>."),
        ("The angles of a triangle are <i>x</i>, <i>x</i> + 20 and <i>x</i> + 40. Find <i>x</i>.", 40, [60, 100, 80], "3<i>x</i> + 60 = 180, so 3<i>x</i> = 120 and <i>x</i> = <b>40°</b>."),
        ("Two angles in a triangle are 47° and 68°. What is the third angle?", 65, [245, 115, 75], "180 − 47 − 68 = <b>65°</b>."),
        ("A triangle has angles of 90° and 45°. What is the third angle?", 45, [135, 225, 90], "180 − 90 − 45 = <b>45°</b>, so it is a right-angled isosceles triangle."),
        ("Three angles of a quadrilateral are 90°, 90° and 115°. Find the fourth angle.", 65, [245, 25, 115], "360 − 90 − 90 − 115 = <b>65°</b>."),
        ("One angle where two straight lines cross is 64°. What are the other three angles?", None, None, None),
        ("Each angle in an equilateral triangle is…", 60, [90, 180, 45], "All three angles are equal: 180 ÷ 3 = <b>60°</b>."),
        ("The two base angles of an isosceles triangle are each 52°. What is the third angle?", 76, [128, 52, 104], "180 − 52 − 52 = <b>76°</b>."),
        ("A kite has angles of 120°, 70° and 70°. What is the fourth angle?", 100, [10, 120, 280], "360 − 120 − 70 − 70 = <b>100°</b>."),
    ]:
        if ans is None:
            its.append(T(q, "64°, 116° and 116°", ["64°, 64° and 64°", "116°, 116° and 116°", "26°, 64° and 26°"],
                         "The vertically opposite angle is also 64°. The other two are 180 − 64 = 116° each: <b>64°, 116° and 116°</b>."))
            continue
        its.append(QN(q, ans, wr, e, unit=DEG))
    data = [
        ("Can a triangle have angles of 100° and 90°?", "No, because 100° + 90° is already more than 180°", ["Yes, the third angle is −10°", "Yes, if it is isosceles", "No, because 100 is not a multiple of 90"],
         "The three angles must add up to exactly 180°, and 100° + 90° = 190°. So <b>no</b>."),
        ("Ethan says the angles in a quadrilateral add up to 180°. Is he right?", "No, they add up to 360°", ["Yes", "No, they add up to 270°", "Only for a square"],
         "A quadrilateral can be split into two triangles: 2 × 180° = <b>360°</b>."),
        ("What is the size of a full turn?", "360°", ["180°", "90°", "100°"], "A full turn is <b>360°</b>."),
        ("How many degrees does the minute hand of a clock turn in 15 minutes?", "90°", ["15°", "60°", "180°"], "15 minutes is a quarter of a turn: 360 ÷ 4 = <b>90°</b>."),
    ]
    for q, a, w, e in data:
        its.append(T(q, a, w, e))
    return its


def body():
    svg = rays([0, 50, 180], ["x", "130°"], h=150, cy=120)
    return lesson(
        "<p>Key facts:</p><ul><li>Angles on a straight line add up to <b>180°</b>.</li>"
        "<li>Angles around a point add up to <b>360°</b>.</li>"
        "<li><b>Vertically opposite</b> angles (where two straight lines cross) are equal.</li>"
        "<li>Angles in a triangle add up to <b>180°</b>; in a quadrilateral, <b>360°</b>.</li>"
        "<li>An isosceles triangle has two equal sides and two equal base angles.</li></ul>"
        + fig(svg),
        [("Two angles on a straight line are 130° and <i>x</i>. Find <i>x</i>.", ["180 − 130 = 50."], "<i>x</i> = 50°"),
         ("An isosceles triangle has a top angle of 40°. Find each base angle.", ["180 − 40 = 140.", "140 ÷ 2 = 70."], "70°")],
        ["Using 360° for angles on a straight line, or 180° for angles around a point.",
         "Thinking vertically opposite angles add up to 180°. They are equal.",
         "Using 180° for a quadrilateral. It is 360°.",
         "In an isosceles triangle, using the wrong pair of equal angles: the equal angles are at the ends of the base, opposite the equal sides."])


def main():
    sets = [S("Angles on a straight line", collect(one_line, 20, R)),
            S("Angles around a point", collect(one_point, 20, R)),
            S("Vertically opposite angles", collect(one_vopp, 14, R) + collect(one_vopp2, 6, R)),
            S("Angles in triangles and quadrilaterals", collect(one_tri, 14, R) + collect(one_quad, 6, R)),
            S("Angle types, algebra and reasoning", problems())]
    make(1, "angles-triangles-and-quadrilaterals", 12, "G1",
         "Angles: Straight Lines, Points, Triangles and Quadrilaterals",
         "Secondary 1 Angles Worksheets: Angles on a Line, Around a Point, Vertically Opposite, Triangles and Quadrilaterals",
         "Angles",
         "Apply the properties of angles at a point, angles at a point on a straight line, vertically opposite angles; "
         "derive and illustrate properties of triangles, quadrilaterals, circles, and other plane figures using appropriate "
         "language and technologies; use the sum of angles in a triangle to deduce the angle sum in any polygon.",
         "Free Secondary 1 angles worksheets with diagrams: angles on a straight line, around a point, vertically opposite "
         "angles, triangles, isosceles triangles and quadrilaterals, plus angle types and algebra. 100 questions with answers.",
         "Straight line 180°, around a point 360°, triangle 180°, quadrilateral 360°.",
         "Vertically opposite angles are equal. An isosceles triangle has two equal base angles.",
         body(),
         [("What do angles on a straight line add up to?", "180°. If one angle is 130°, the other is 50°."),
          ("What are vertically opposite angles?", "When two straight lines cross they make two pairs of opposite angles. The angles in each pair are equal."),
          ("Why do the angles in a quadrilateral add up to 360°?", "A diagonal splits any quadrilateral into two triangles, and each triangle has 180°."),
          ("How do I find the angles in an isosceles triangle?", "The two base angles are equal. Take the top angle from 180° and halve the result.")],
         sets, R)


if __name__ == "__main__":
    main()
