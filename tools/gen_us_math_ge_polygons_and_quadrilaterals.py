# -*- coding: utf-8 -*-
"""
US Geometry: Polygons and Quadrilaterals (Common Core G-CO.C.11)
  python3 tools/gen_us_math_ge_polygons_and_quadrilaterals.py
Interior and exterior angle sums of polygons, properties of parallelograms, rectangles, rhombuses and
squares (with algebra), trapezoids and kites, and classifying quadrilaterals.
Wrong answers come from real mistakes: using n × 180 instead of (n − 2) × 180, setting consecutive angles
equal instead of supplementary, thinking every parallelogram has congruent diagonals, and averaging the
wrong pair of sides for a trapezoid midsegment.
"""
import random
from us_hs import B, S, make, lesson, collect, T, fig, num, MINUS
from us_geo import Canvas, RED, GREEN, BLUE

R = random.Random(93201)
POLY = {3: "triangle", 4: "quadrilateral", 5: "pentagon", 6: "hexagon", 7: "heptagon", 8: "octagon", 9: "nonagon", 10: "decagon", 12: "dodecagon"}


def lin(a, b):
    s = ("" if a == 1 else num(a)) + "<i>x</i>"
    if b > 0:
        s += " + %s" % num(b)
    elif b < 0:
        s += " %s %s" % (MINUS, num(-b))
    return s


def solve_eq(k1, d1, k2, d2, x):
    diff = abs(k1 - k2)
    s = "%s = %s, so %s<i>x</i> = %d and <i>x</i> = %d." % (lin(k1, d1), lin(k2, d2), num(diff) if diff > 1 else "", abs(d2 - d1), x)
    return s.replace(", so <i>x</i> = %d and <i>x</i> = " % abs(d2 - d1), ", so <i>x</i> = ")


def pg_fig(labels, diag=False, shape="pg"):
    """labels: dict with keys 'AB','BC','CD','DA','A','B','C','D','AE','EC','BE','ED'"""
    pts = {"pg": [(20, 150), (220, 150), (280, 30), (80, 30)], "rect": [(20, 150), (260, 150), (260, 30), (20, 30)],
           "rh": [(20, 150), (170, 150), (270, 60), (120, 60)]}[shape]
    A, Bp, C, D = pts
    c = Canvas()
    c.poly(pts)
    if diag:
        c.seg(A, C, col=BLUE, w=1.8)
        c.seg(Bp, D, col=BLUE, w=1.8)
    c.vlabels(pts, "ABCD")
    cen = ((A[0] + C[0]) / 2, (A[1] + C[1]) / 2)
    for k, (p, q) in {"AB": (A, Bp), "BC": (Bp, C), "CD": (C, D), "DA": (D, A)}.items():
        if labels.get(k):
            c.side_label(p, q, labels[k], cen, 16, 13)
    for k, (v, p, q) in {"A": (A, Bp, D), "B": (Bp, C, A), "C": (C, D, Bp), "D": (D, A, C)}.items():
        if labels.get(k):
            c.angle(v, p, q, "", r=18)
            c.angle_text(v, p, q, labels[k], r=40 if len(labels[k]) < 6 else 54, fs=13)
    for k, (p, q) in {"AE": (A, cen), "EC": (cen, C), "BE": (Bp, cen), "ED": (cen, D)}.items():
        if labels.get(k):
            ox, oy = {"AE": (-8, -16), "EC": (-8, -16), "BE": (14, -8), "ED": (14, -8)}[k]
            c.text(((p[0] + q[0]) / 2 + ox, (p[1] + q[1]) / 2 + oy), labels[k], 12, BLUE)
    if diag:
        c.text((cen[0], cen[1] + 16), "E", 13)
    if shape == "rect":
        for v, p, q in ((A, Bp, D), (Bp, C, A), (C, D, Bp), (D, A, C)):
            c.right(v, p, q)
    return c.svg("quadrilateral ABCD, not drawn to scale")


# ------------------------------------------------------------ set 1: polygon angles
def one_poly(r):
    n = r.choice([5, 6, 7, 8, 9, 10, 12, 15, 18, 20])
    name = POLY.get(n, "%d-gon" % n)
    kind = r.choice(["sum", "each", "ext", "findn", "findn2", "missing"])
    S_ = (n - 2) * 180
    if kind == "sum":
        q = "What is the sum of the interior angles of a %s?" % B(name)
        return T(q, "%s°" % num(S_), ["%s°" % num(w) for w in [n * 180, (n - 1) * 180, 360]],
                 "Sum = (<i>n</i> %s 2) × 180° = (%d %s 2) × 180° = <b>%s°</b>." % (MINUS, n, MINUS, num(S_)))
    if kind == "each":
        if S_ % n:
            return None
        q = "What is the measure of each interior angle of a regular %s?" % B(name)
        ans = S_ // n
        return T(q, "%d°" % ans, ["%d°" % w for w in dict.fromkeys([360 // n if 360 % n == 0 else 180 - ans + 1, 180 * n // n, S_ // (n - 1) if S_ % (n - 1) == 0 else ans + 10]) if w != ans][:3],
                 "Sum = (%d %s 2) × 180° = %s°. Each of the %d equal angles: %s ÷ %d = <b>%d°</b>." % (n, MINUS, num(S_), n, num(S_), n, ans))
    if kind == "ext":
        if 360 % n:
            return None
        q = "What is the measure of each exterior angle of a regular %s?" % B(name)
        ans = 360 // n
        return T(q, "%d°" % ans, ["%d°" % w for w in dict.fromkeys([180 - ans, 180 // n if 180 % n == 0 else ans * 2, ans + 10]) if w != ans][:3],
                 "The exterior angles of any polygon add to 360°: 360° ÷ %d = <b>%d°</b>." % (n, ans))
    if kind in ("findn", "findn2"):
        if 360 % n:
            return None
        ext = 360 // n
        if kind == "findn":
            q = "Each interior angle of a regular polygon is %d°. How many sides does it have?" % (180 - ext)
            e = "Each exterior angle is 180° %s %d° = %d°. Number of sides = 360 ÷ %d = <b>%d</b>." % (MINUS, 180 - ext, ext, ext, n)
        else:
            q = "Each exterior angle of a regular polygon is %d°. How many sides does it have?" % ext
            e = "The exterior angles add to 360°: 360 ÷ %d = <b>%d</b>." % (ext, n)
        wr = [n + 2, n - 1, 180 // ext if 180 % ext == 0 and 180 // ext != n else n + 4, (180 - ext) // 10]
        return T(q, num(n), [num(w) for w in dict.fromkeys(wr) if w != n and w > 2][:3], e)
    n = r.choice([5, 6])
    S_ = (n - 2) * 180
    angs = [r.randint(90, 150) for _ in range(n - 1)]
    last = S_ - sum(angs)
    if not (60 < last < 175):
        return None
    q = "A %s has angles of %s and <i>x</i>°. Find <i>x</i>." % (POLY[n], ", ".join("%d°" % a for a in angs))
    return T(q, num(last), [num(w) for w in dict.fromkeys([360 - sum(angs) % 360 if (360 - sum(angs)) > 0 else last + 20, n * 180 - sum(angs), last - 10]) if w != last and w > 0][:3],
             "The angles of a %s add to (%d %s 2) × 180° = %d°. <i>x</i> = %d %s %d = <b>%d</b>." % (POLY[n], n, MINUS, S_, S_, MINUS, sum(angs), last))


# ------------------------------------------------------------ set 2: parallelograms
def one_pg(r):
    kind = r.choice(["oppang", "consec", "side", "diag", "alg_ang", "alg_side"])
    if kind == "oppang":
        a = r.randint(50, 130)
        if a == 90:
            return None
        q = "ABCD is a parallelogram. Find <i>x</i>.%s" % fig(pg_fig({"A": "%d°" % a, "C": "<i>x</i>°"}))
        return T(q, num(a), [num(w) for w in [180 - a, 360 - a, 90 - a if a < 90 else a - 90]],
                 "Opposite angles of a parallelogram are congruent: <i>x</i> = <b>%d</b>." % a)
    if kind == "consec":
        a = r.randint(50, 130)
        if a == 90:
            return None
        q = "ABCD is a parallelogram. Find <i>x</i>.%s" % fig(pg_fig({"A": "%d°" % a, "B": "<i>x</i>°"}))
        return T(q, num(180 - a), [num(w) for w in [a, 360 - a, abs(90 - a)] if w != 180 - a][:3],
                 "Consecutive angles of a parallelogram are supplementary: <i>x</i> = 180 %s %d = <b>%d</b>." % (MINUS, a, 180 - a))
    x = r.randint(2, 12)
    k1, k2 = r.sample(range(1, 7), 2)
    d1 = r.randint(-6, 15)
    v = k1 * x + d1
    d2 = v - k2 * x
    if v < 4 or abs(d2) > 30:
        return None
    if kind == "side":
        q = "ABCD is a parallelogram. AB = %s and CD = %s. Find AB.%s" % (lin(k1, d1), lin(k2, d2), fig(pg_fig({"AB": lin(k1, d1), "CD": lin(k2, d2)})))
        return T(q, num(v), [num(w) for w in dict.fromkeys([x, 2 * v, v + 2, 180 - v]) if w != v and w > 0][:3],
                 "Opposite sides of a parallelogram are congruent: %s AB = <b>%d</b>." % (solve_eq(k1, d1, k2, d2, x), v))
    if kind == "diag":
        q = "ABCD is a parallelogram. AE = %s and EC = %s. Find AC.%s" % (lin(k1, d1), lin(k2, d2), fig(pg_fig({"AE": lin(k1, d1), "EC": lin(k2, d2)}, diag=True)))
        return T(q, num(2 * v), [num(w) for w in dict.fromkeys([v, x, 4 * v, 2 * v + 2]) if w != 2 * v][:3],
                 "The diagonals of a parallelogram bisect each other, so AE = EC: %s AC = 2 × %d = <b>%d</b>." % (solve_eq(k1, d1, k2, d2, x), v, 2 * v))
    if kind == "alg_ang":
        a = r.randint(55, 125)
        if a == 90:
            return None
        k1 = r.randint(2, 6)
        x = r.randint(5, 20)
        d1 = a - k1 * x
        k2 = r.randint(1, 5)
        d2 = 180 - a - k2 * x
        if abs(d1) > 40 or abs(d2) > 40:
            return None
        q = "ABCD is a parallelogram. m∠A = (%s)° and m∠B = (%s)°. Find <i>x</i>.%s" % (lin(k1, d1), lin(k2, d2), fig(pg_fig({"A": lin(k1, d1) + "°", "B": lin(k2, d2) + "°"})))
        bad = (d2 - d1) / (k1 - k2) if k1 != k2 else None
        return T(q, num(x), [num(w) for w in dict.fromkeys([int(bad) if bad and bad == int(bad) and bad > 0 else x + 3, a, x + 1, x - 1]) if w != x and w > 0][:3],
                 "∠A and ∠B are consecutive angles, so they are supplementary: (%s) + (%s) = 180, %d<i>x</i> = %d, <i>x</i> = <b>%d</b>." % (
                     lin(k1, d1), lin(k2, d2), k1 + k2, 180 - d1 - d2, x))
    q = "ABCD is a parallelogram. BE = %s and ED = %s. Find <i>x</i>.%s" % (lin(k1, d1), lin(k2, d2), fig(pg_fig({"BE": lin(k1, d1), "ED": lin(k2, d2)}, diag=True)))
    return T(q, num(x), [num(w) for w in dict.fromkeys([v, 2 * v, x + 1, x + 2]) if w != x and w > 0][:3],
             "The diagonals bisect each other, so BE = ED: " + solve_eq(k1, d1, k2, d2, x).replace("<i>x</i> = %d." % x, "<i>x</i> = <b>%d</b>." % x))


# ------------------------------------------------------------ set 3: rectangles, rhombuses, squares
def one_spec(r):
    kind = r.choice(["rect_diag", "rect_diag", "rh_ang", "rh_side", "sq", "rh_perp"])
    if kind == "rect_diag":
        x = r.randint(2, 12)
        k1, k2 = r.sample(range(1, 7), 2)
        d1 = r.randint(-5, 12)
        v = k1 * x + d1
        d2 = 2 * v - k2 * x
        if v < 3 or abs(d2) > 40:
            return None
        q = "ABCD is a rectangle with diagonals meeting at E. AE = %s and BD = %s. Find <i>x</i>.%s" % (lin(k1, d1), lin(k2, d2), fig(pg_fig({"AE": lin(k1, d1)}, diag=True, shape="rect")))
        bad = (d1 - d2) / (k2 - k1) if k2 != k1 else None
        return T(q, num(x), [num(w) for w in dict.fromkeys([int(bad) if bad and bad == int(bad) and bad > 0 else x + 2, v, x + 1, 2 * v]) if w != x and w > 0][:3],
                 "The diagonals of a rectangle are congruent and bisect each other, so BD = AC = 2 × AE: %s = 2(%s), <i>x</i> = <b>%d</b>." % (lin(k2, d2), lin(k1, d1), x))
    if kind == "rh_ang":
        a = r.randint(25, 70)
        q = "ABCD is a rhombus, and m∠BAC = %d°. Find m∠BAD." % a
        return T(q, "%d°" % (2 * a), ["%d°" % w for w in [a, 180 - 2 * a, 90 - a] if w != 2 * a],
                 "The diagonals of a rhombus bisect its angles, so m∠BAD = 2 × %d° = <b>%d°</b>." % (a, 2 * a))
    if kind == "rh_perp":
        a = r.randint(25, 65)
        q = "ABCD is a rhombus with diagonals meeting at E, and m∠ABE = %d°. Find m∠BAE." % a
        return T(q, "%d°" % (90 - a), ["%d°" % w for w in [a, 180 - a, 2 * a] if w != 90 - a],
                 "The diagonals of a rhombus are perpendicular, so m∠AEB = 90°. m∠BAE = 180 %s 90 %s %d = <b>%d°</b>." % (MINUS, MINUS, a, 90 - a))
    if kind == "rh_side":
        s = r.randint(4, 20)
        q = "A rhombus has one side of length %d. What is its perimeter?" % s
        return T(q, num(4 * s), [num(w) for w in [2 * s, s * s, 4 * s + 4]],
                 "All four sides of a rhombus are congruent: 4 × %d = <b>%d</b>." % (s, 4 * s))
    d = r.choice([6, 8, 10, 12, 14, 16, 20])
    q = "The diagonals of a square meet at E. AE = %d. Find BD, and the measure of ∠AEB." % (d // 2)
    right = "BD = %d and m∠AEB = 90°" % d
    wr = ["BD = %d and m∠AEB = 45°" % d, "BD = %d and m∠AEB = 90°" % (d // 2), "BD = %d and m∠AEB = 180°" % d]
    return T(q, right, wr, "A square is a rectangle (congruent diagonals that bisect each other) and a rhombus (perpendicular diagonals). <b>%s</b>." % right)


# ------------------------------------------------------------ set 4: trapezoids and kites
def trap_fig(top, bot, mid):
    c = Canvas()
    A, Bp, C, D = (20, 150), (300, 150), (220, 30), (100, 30)
    c.poly([A, Bp, C, D])
    M1, M2 = ((A[0] + D[0]) / 2, 90), ((Bp[0] + C[0]) / 2, 90)
    c.seg(M1, M2, col=RED)
    c.chevrons((140, 30), (180, 30))
    c.chevrons((140, 150), (180, 150))
    c.text((160, 18), top, 13)
    c.text((160, 170), bot, 13)
    c.text((160, 80), mid, 13, RED)
    return c.svg("trapezoid with its midsegment")


def one_trap(r):
    kind = r.choice(["mid", "mid", "base", "iso", "iso2", "kite"])
    if kind == "mid":
        a, b = r.randint(4, 30), r.randint(8, 40)
        if a == b:
            return None
        q = "Find the length of the midsegment of the trapezoid.%s" % fig(trap_fig(num(min(a, b)), num(max(a, b)), "?"))
        ans = (a + b) / 2
        return T(q, num(ans), [num(w) for w in dict.fromkeys([a + b, abs(a - b), max(a, b) / 2, ans + 1]) if w != ans][:3],
                 "The midsegment of a trapezoid is the average of the bases: (%d + %d) ÷ 2 = <b>%s</b>." % (a, b, num(ans)))
    if kind == "base":
        a, m = r.randint(4, 20), r.randint(10, 30)
        b = 2 * m - a
        if b <= a:
            return None
        q = "The midsegment of a trapezoid is %d and the shorter base is %d. Find the longer base.%s" % (m, a, fig(trap_fig(num(a), "?", num(m))))
        return T(q, num(b), [num(w) for w in dict.fromkeys([m - a, m + a, 2 * m, b + 2]) if w != b and w > 0][:3],
                 "(%d + <i>b</i>) ÷ 2 = %d, so %d + <i>b</i> = %d and <i>b</i> = <b>%d</b>." % (a, m, a, 2 * m, b))
    if kind in ("iso", "iso2"):
        a = r.randint(50, 80)
        if kind == "iso":
            q = "In isosceles trapezoid ABCD, the bases are <span class='ov'>AB</span> and <span class='ov'>CD</span>, and m∠A = %d°. Find m∠B." % a
            return T(q, "%d°" % a, ["%d°" % w for w in [180 - a, 90 - a, 360 - a]],
                     "Base angles of an isosceles trapezoid are congruent: m∠B = m∠A = <b>%d°</b>." % a)
        q = "In isosceles trapezoid ABCD, the bases are <span class='ov'>AB</span> and <span class='ov'>CD</span>, and m∠A = %d°. Find m∠D." % a
        return T(q, "%d°" % (180 - a), ["%d°" % w for w in [a, 90 - a, 360 - 2 * a] if w != 180 - a][:3],
                 "∠A and ∠D are same-side interior angles between the parallel bases, so they are supplementary: 180 %s %d = <b>%d°</b>." % (MINUS, a, 180 - a))
    a, b = r.randint(50, 130), r.randint(40, 110)
    c_ = 360 - a - 2 * b
    if not (30 < c_ < 160):
        return None
    q = "In kite ABCD, AB = AD and CB = CD. m∠A = %d° and m∠C = %d°. Find m∠B." % (a, c_)
    return T(q, "%d°" % b, ["%d°" % w for w in dict.fromkeys([360 - a - c_, 180 - a, a, 180 - b]) if w != b][:3],
             "In a kite, the angles between the pairs of unequal sides (∠B and ∠D) are congruent. 2 × m∠B = 360 %s %d %s %d = %d, so m∠B = <b>%d°</b>." % (
                 MINUS, a, MINUS, c_, 2 * b, b))


# ------------------------------------------------------------ set 5: classify and prove
def one_cls(r):
    items = [
        ("Which quadrilateral always has diagonals that are congruent?", "Rectangle", ["Rhombus", "Parallelogram", "Kite"],
         "Rectangles (including squares) have congruent diagonals. A general rhombus does not."),
        ("Which quadrilateral always has perpendicular diagonals?", "Rhombus", ["Rectangle", "Parallelogram", "Trapezoid"],
         "Rhombuses (including squares) and kites have perpendicular diagonals."),
        ("Which quadrilateral has exactly one pair of parallel sides?", "Trapezoid", ["Parallelogram", "Kite", "Rhombus"],
         "A trapezoid has exactly one pair of parallel sides (its bases)."),
        ("A parallelogram has one right angle. What must it be?", "A rectangle", ["A rhombus", "A square", "A kite"],
         "Consecutive angles are supplementary and opposite angles are equal, so all four angles are 90°."),
        ("A parallelogram has perpendicular diagonals. What must it be?", "A rhombus", ["A rectangle", "A trapezoid", "A kite"],
         "A parallelogram with perpendicular diagonals is a rhombus."),
        ("A parallelogram has congruent diagonals. What must it be?", "A rectangle", ["A rhombus", "A kite", "A trapezoid"],
         "A parallelogram with congruent diagonals is a rectangle."),
        ("Is every square a rhombus?", "Yes, always", ["No, never", "Only if it is large", "Only if its diagonals are not equal"],
         "A square has four congruent sides, which is the definition of a rhombus."),
        ("Is every rhombus a square?", "No, only sometimes", ["Yes, always", "No, never", "Only if it is a trapezoid"],
         "A rhombus is a square only if it has right angles."),
        ("Is a rectangle a parallelogram?", "Yes, always", ["No, never", "Only sometimes", "Only if it is a square"],
         "A rectangle has two pairs of parallel sides."),
        ("Which fact is enough to prove ABCD is a parallelogram?", "The diagonals bisect each other", ["The diagonals are congruent", "One pair of sides is parallel",
         "Two consecutive sides are congruent"], "If the diagonals of a quadrilateral bisect each other, it is a parallelogram."),
        ("Which fact is enough to prove ABCD is a parallelogram?", "One pair of opposite sides is both parallel and congruent",
         ["One pair of opposite sides is parallel", "The diagonals are perpendicular", "Two pairs of consecutive sides are congruent"],
         "One pair of opposite sides that is both parallel and congruent proves a parallelogram."),
        ("Which fact is enough to prove ABCD is a parallelogram?", "Both pairs of opposite angles are congruent",
         ["One pair of opposite angles is congruent", "Two consecutive angles are congruent", "The diagonals are congruent"],
         "If both pairs of opposite angles are congruent, the quadrilateral is a parallelogram."),
        ("Which quadrilateral has two pairs of consecutive congruent sides but opposite sides that are not congruent?", "Kite", ["Rhombus", "Parallelogram", "Trapezoid"],
         "That is the definition of a kite."),
        ("Which property does a rhombus have that a general parallelogram does not?", "Its diagonals bisect its angles", ["Its opposite sides are parallel", "Its diagonals bisect each other",
         "Its opposite angles are congruent"], "Every parallelogram has the other three properties."),
        ("Which property does a rectangle have that a general parallelogram does not?", "Its diagonals are congruent", ["Its diagonals bisect each other", "Its opposite sides are congruent",
         "Its consecutive angles are supplementary"], "Every parallelogram has the other three properties."),
    ]
    if r.random() < 0.25:
        x = r.randint(3, 12)
        k1, k2 = r.sample(range(2, 7), 2)
        d1 = r.randint(-5, 10)
        v = k1 * x + d1
        d2 = v - k2 * x
        if v < 5 or abs(d2) > 30:
            return None
        q = "For what value of <i>x</i> is ABCD a parallelogram, if AB = %s, CD = %s, and <span class='ov'>AB</span> ∥ <span class='ov'>CD</span>?" % (lin(k1, d1), lin(k2, d2))
        return T(q, num(x), [num(w) for w in dict.fromkeys([v, x + 1, x - 1, 2 * x]) if w != x and w > 0][:3],
                 "A pair of opposite sides that is parallel and congruent proves a parallelogram. Set AB = CD: " + solve_eq(k1, d1, k2, d2, x).replace("<i>x</i> = %d." % x, "<i>x</i> = <b>%d</b>." % x))
    q, right, wr, e = r.choice(items)
    return T(q, right, wr, e + " <b>%s</b>." % right)


def build():
    sets = [S("Angles of polygons", collect(one_poly, 20, R)),
            S("Properties of parallelograms", collect(one_pg, 20, R)),
            S("Rectangles, rhombuses and squares", collect(one_spec, 20, R)),
            S("Trapezoids and kites", collect(one_trap, 20, R)),
            S("Classify and prove", collect(one_cls, 20, R))]
    body = lesson(
        "<p>The interior angles of a polygon with <i>n</i> sides add to <b>(<i>n</i> %s 2) × 180°</b>. The exterior angles of any polygon add to <b>360°</b>.</p>"
        "<p>A <b>parallelogram</b> has opposite sides parallel and congruent, opposite angles congruent, consecutive angles supplementary, and diagonals that bisect each other.</p>"
        "<ul><li><b>Rectangle</b>: a parallelogram with four right angles; its diagonals are congruent.</li>"
        "<li><b>Rhombus</b>: a parallelogram with four congruent sides; its diagonals are perpendicular and bisect its angles.</li>"
        "<li><b>Square</b>: both a rectangle and a rhombus.</li>"
        "<li><b>Trapezoid</b>: exactly one pair of parallel sides; its midsegment is the average of the bases. An isosceles trapezoid has congruent base angles.</li>"
        "<li><b>Kite</b>: two pairs of consecutive congruent sides; its diagonals are perpendicular.</li></ul>" % MINUS,
        [("Each interior angle of a regular polygon is 144°. How many sides?", ["Exterior angle: 180 %s 144 = 36°" % MINUS, "360 ÷ 36 = 10"], "10 sides"),
         ("ABCD is a parallelogram with m∠A = (3<i>x</i> + 10)° and m∠B = (2<i>x</i> + 20)°. Find m∠A.",
          ["Consecutive angles add to 180: 5<i>x</i> + 30 = 180", "<i>x</i> = 30, so m∠A = 100°"], "100°")],
        ["Using <i>n</i> × 180° for the angle sum. Subtract 2 first.",
         "Setting consecutive angles of a parallelogram equal. They add to 180°.",
         "Saying every parallelogram has congruent diagonals. Only rectangles do.",
         "For a trapezoid midsegment, averaging the legs instead of the bases."])
    faq = [("What is the formula for the sum of the interior angles of a polygon?", "(n − 2) × 180°, where n is the number of sides."),
           ("What are the properties of a parallelogram?",
            "Opposite sides are parallel and congruent, opposite angles are congruent, consecutive angles are supplementary, and the diagonals bisect each other."),
           ("Is a square a rhombus?", "Yes. A square has four congruent sides, so it is a rhombus. It is also a rectangle."),
           ("How do you find the midsegment of a trapezoid?", "Add the lengths of the two bases and divide by 2.")]
    make("polygons-and-quadrilaterals", 12, "G-CO.C.11",
         "Polygons and Quadrilaterals: Angle Sums and Parallelograms",
         "Polygons and Quadrilaterals Worksheet: Parallelograms, Rhombus, Trapezoid (Geometry) | 100 Questions",
         "Polygons and Quadrilaterals",
         "Prove theorems about parallelograms. Theorems include: opposite sides are congruent, opposite angles are congruent, the diagonals of a parallelogram bisect each other, and conversely, rectangles are parallelograms with congruent diagonals.",
         "Free Geometry worksheet on polygons and quadrilaterals: interior and exterior angle sums, parallelograms, rectangles, rhombuses, trapezoids and kites. 100 questions with answers.",
         "Interior angles of an n-gon add to (n − 2) × 180°. Exterior angles add to 360°.",
         "Parallelograms: opposite sides and angles congruent, diagonals bisect each other.",
         body, faq, sets, R, domain="Polygons and Quadrilaterals", grade="geometry")


if __name__ == "__main__":
    build()
