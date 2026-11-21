# -*- coding: utf-8 -*-
"""
India Class 9 Maths, NCERT Chapter 6: Lines and Angles (CBSE Unit IV Geometry)
  python3 tools/gen_in_maths_c9_lines_and_angles.py
Complementary, supplementary, reflex and linear-pair angles, vertically opposite angles and angles at a point (SG
Secondary 1 makers with figures), parallel lines and a transversal (corresponding, alternate, co-interior angles),
the angle sum of a triangle and the exterior angle property, and problems with x.
Wrong answers come from real mistakes: complement and supplement mixed up, co-interior angles taken as equal,
alternate angles added to 180°, and the exterior angle taken as 180° − (sum of the opposite interior angles).
"""
import random
from in_common import num, S, make, lesson, mix, T, QN, adopt, gb
import gen_sg_maths_s1_angles_triangles_and_quadrilaterals as sga
import gen_sg_maths_s1_parallel_lines_and_polygons as sgp

R = random.Random(909006)
adopt(sga, R)
adopt(sgp, R)


# ---------------------------------------------------------------- set 1: kinds of angles and pairs
def one_pair(r):
    kind = r.choice(["comp", "supp", "supp", "ratio", "reflex", "type", "diff"])
    if kind == "comp":
        a = r.randint(5, 85)
        return QN("Find the complement of %d°." % a, 90 - a, [180 - a, a, 360 - a], "Complementary angles add up to 90°: 90° − %d° = <b>%d°</b>." % (a, 90 - a), unit="°")
    if kind == "supp":
        a = r.randint(5, 175)
        return QN("Find the supplement of %d°." % a, 180 - a, [90 - a if a < 90 else 360 - a, a, 360 - a if a < 90 else 270 - a], "Supplementary angles add up to 180°: 180° − %d° = <b>%d°</b>." % (a, 180 - a), unit="°")
    if kind == "ratio":
        p, q = r.choice([(1, 2), (2, 3), (1, 4), (3, 5), (4, 5), (5, 7), (2, 7), (1, 5)])
        tot = r.choice([90, 180])
        if (tot % (p + q)):
            return None
        k = tot // (p + q)
        return T("Two %s angles are in the ratio %d : %d. Find them." % ("complementary" if tot == 90 else "supplementary", p, q), "%d° and %d°" % (p * k, q * k),
                 ["%d° and %d°" % (p * k * 2, q * k * 2) if tot == 90 else "%d° and %d°" % (p * k / 2, q * k / 2), "%d° and %d°" % (p * k + 5, q * k - 5), "%d° and %d°" % (p * 10, q * 10) if (p + q) * 10 != tot else "%d° and %d°" % (p * 15, q * 15)],
                 "%d + %d = %d parts = %d°, so 1 part = %d°: <b>%d° and %d°</b>." % (p, q, p + q, tot, k, p * k, q * k))
    if kind == "reflex":
        a = r.randint(10, 170)
        return QN("What is the reflex angle that goes with an angle of %d°?" % a, 360 - a, [180 - a, 180 + a, 90 + a], "The angle and its reflex angle make a full turn: 360° − %d° = <b>%d°</b>." % (a, 360 - a), unit="°")
    if kind == "type":
        a = r.choice([r.randint(1, 89), 90, r.randint(91, 179), 180, r.randint(181, 359)])
        nm = "acute" if a < 90 else "right" if a == 90 else "obtuse" if a < 180 else "straight" if a == 180 else "reflex"
        opts = ["acute", "right", "obtuse", "straight", "reflex"]
        return T("What kind of angle is %d°?" % a, "%s angle" % nm.capitalize(), ["%s angle" % o.capitalize() for o in opts if o != nm][:3],
                 "<b>%s</b>: acute &lt; 90°, right = 90°, obtuse between 90° and 180°, straight = 180°, reflex between 180° and 360°." % nm.capitalize())
    d = r.choice([10, 20, 30, 40, 50, 60])
    tot = r.choice([90, 180])
    if d >= tot:
        return None
    a, b = (tot + d) // 2, (tot - d) // 2
    if (tot + d) % 2:
        return None
    return T("Two %s angles differ by %d°. Find the larger angle." % ("complementary" if tot == 90 else "supplementary", d), "%d°" % a, ["%d°" % b, "%d°" % (tot - d), "%d°" % (a + d)],
             "x + (x − %d) = %d, so 2x = %d and the larger angle is <b>%d°</b>." % (d, tot, tot + d, a))


# ---------------------------------------------------------------- set 3: transversal with algebra
def one_trans(r):
    kind = r.choice(["co", "co", "alt", "corr", "check"])
    if kind == "check":
        a = r.randint(50, 130)
        b = r.choice([180 - a, 180 - a + r.choice([5, 10, -10])])
        ok = a + b == 180
        return T("A transversal cuts two lines. The interior angles on the same side are %d° and %d°. Are the lines parallel?" % (a, b), "Yes, because they add up to 180°" if ok else "No, because they do not add up to 180°",
                 ["No, because they do not add up to 180°" if ok else "Yes, because they add up to 180°", "Yes, because they are equal" if a != b else "No, because they are equal", "It cannot be decided"],
                 "Co-interior angles add up to 180° only when the lines are parallel. %d° + %d° = %d°, so <b>%s</b>." % (a, b, a + b, "yes" if ok else "no"))
    x = r.randint(10, 40)
    m, c = r.choice([2, 3, 4]), r.randint(-20, 30)
    a1 = m * x + c
    if not (20 <= a1 <= 160):
        return None
    if kind == "co":
        a2 = 180 - a1
        k = r.choice([1, 2])
        cc = a2 - k * x
        if cc <= -30 or cc >= 150:
            return None
        e1 = "(%dx %s %d)°" % (m, "+" if c >= 0 else "−", abs(c)) if c else "%dx°" % m
        e2 = ("(x %s %d)°" % ("+" if cc >= 0 else "−", abs(cc)) if k == 1 else "(%dx %s %d)°" % (k, "+" if cc >= 0 else "−", abs(cc))) if cc else ("x°" if k == 1 else "%dx°" % k)
        return T("Lines l ∥ m are cut by a transversal. Two co-interior angles are %s and %s. Find x." % (e1, e2), "x = %d" % x,
                 ["x = %s" % num((cc - c) / (m - k)) if m != k and (cc - c) % (m - k) == 0 and (cc - c) // (m - k) != x else "x = %d" % (x + 5), "x = %d" % (x - 5), "x = %d" % (x + 10)],
                 "Co-interior angles add up to 180°: %s + %s = 180, so %dx = %d and <b>x = %d</b>." % (e1.strip("°"), e2.strip("°"), m + k, 180 - c - cc, x))
    k = r.choice([1, 2, 5])
    cc = a1 - k * x
    if k == m or cc <= -40 or cc >= 150:
        return None
    e1 = "(%dx %s %d)°" % (m, "+" if c >= 0 else "−", abs(c)) if c else "%dx°" % m
    e2 = ("(%sx %s %d)°" % ("" if k == 1 else str(k), "+" if cc >= 0 else "−", abs(cc))) if cc else ("%sx°" % ("" if k == 1 else str(k)))
    nm = "alternate interior" if kind == "alt" else "corresponding"
    wrong = (180 - c - cc) / (m + k)
    return T("Lines l ∥ m are cut by a transversal. Two %s angles are %s and %s. Find x." % (nm, e1, e2), "x = %d" % x,
             ["x = %s" % num(wrong) if wrong == int(wrong) and wrong != x else "x = %d" % (x + 4), "x = %d" % (x * 2), "x = %d" % (x - 3)],
             "%s angles are equal: %s = %s, so <b>x = %d</b>." % (nm.capitalize(), e1.strip("°"), e2.strip("°"), x))


# ---------------------------------------------------------------- set 4: angle sum of a triangle and exterior angle
def one_tri(r):
    kind = r.choice(["third", "third", "ext", "ext", "ratio"])
    if kind == "third":
        a, b = r.randint(20, 100), r.randint(20, 100)
        if a + b >= 170:
            return None
        return QN("Two angles of a triangle are %d° and %d°. Find the third angle." % (a, b), 180 - a - b, [180 - a, 360 - a - b, a + b], "The angles of a triangle add up to 180°: 180° − %d° − %d° = <b>%d°</b>." % (a, b, 180 - a - b), unit="°")
    if kind == "ext":
        a, b = r.randint(20, 80), r.randint(20, 80)
        if r.random() < 0.5:
            return QN("In △ABC, side BC is produced to D. ∠A = %d° and ∠B = %d°. Find the exterior angle ∠ACD." % (a, b), a + b, [180 - a - b, 180 - a, 90 + a], "The exterior angle equals the sum of the two interior opposite angles: %d° + %d° = <b>%d°</b>." % (a, b, a + b), unit="°")
        return QN("An exterior angle of a triangle is %d° and one interior opposite angle is %d°. Find the other interior opposite angle." % (a + b, a), b, [180 - a - b, a + b - 90 if a + b > 90 else a, 180 - (a + b)], "Exterior angle = sum of the interior opposite angles: %d° − %d° = <b>%d°</b>." % (a + b, a, b), unit="°")
    p, q, s = r.choice([(2, 3, 4), (1, 2, 3), (3, 4, 5), (1, 1, 2), (2, 3, 5), (4, 5, 6), (1, 3, 5), (5, 6, 7)])
    if 180 % (p + q + s):
        return None
    k = 180 // (p + q + s)
    return T("The angles of a triangle are in the ratio %d : %d : %d. Find the largest angle." % (p, q, s), "%d°" % (s * k), ["%d°" % (p * k), "%d°" % (s * 360 // (p + q + s)) if 360 % (p + q + s) == 0 else "%d°" % (s * k + 10), "%d°" % (s * 10)],
             "%d parts = 180°, 1 part = %d°, so the largest angle is %d × %d = <b>%d°</b>." % (p + q + s, k, s, k, s * k))


def main():
    seen = set()
    sets = [
        S("Pairs and kinds of angles", mix(R, [(one_pair, 20)], seen)),
        S("Linear pairs and vertically opposite angles", mix(R, [(gb(sga.one_line), 7), (gb(sga.one_vopp), 7), (gb(sga.one_point), 6)], seen)),
        S("Parallel lines and a transversal", mix(R, [(gb(sgp.one_parallel), 10), (gb(sgp.one_name), 4), (one_trans, 6)], seen)),
        S("Angle sum of a triangle", mix(R, [(one_tri, 20)], seen)),
        S("Problems with x", mix(R, [(one_trans, 14), (gb(sga.one_vopp2), 6)], seen)),
    ]
    body = lesson(
        "<p>Angles on a straight line (a <b>linear pair</b>) add up to 180°. <b>Vertically opposite angles</b> are equal. Angles round a point add up to 360°.</p>"
        "<p>When a transversal cuts two <b>parallel</b> lines: corresponding angles are equal, alternate interior angles are equal, and interior angles on the same side (co-interior) add up to 180°.</p>"
        "<p>The angles of a triangle add up to 180°. An <b>exterior angle</b> equals the sum of the two interior opposite angles.</p>",
        [("Two lines intersect and one angle is 40°. Find the other three.", ["Vertically opposite: 40°", "Linear pair: 180° − 40° = 140°"], "40°, 140°, 140°"),
         ("Co-interior angles are (2x + 10)° and (3x − 30)°. Find x.", ["5x − 20 = 180"], "x = 40")],
        ["Mixing up complement (adds to 90°) and supplement (adds to 180°).",
         "Taking co-interior angles as equal. They add up to 180°.",
         "Writing exterior angle = 180° − (the two opposite interior angles). It equals their sum."])
    faq = [
        ("What is a linear pair of angles?", "Two adjacent angles whose non-common arms form a straight line. They add up to 180°."),
        ("What are the angle relationships for parallel lines and a transversal?", "Corresponding angles are equal, alternate interior angles are equal, and interior angles on the same side add up to 180°."),
        ("What is the angle sum property of a triangle?", "The three angles of a triangle add up to 180°."),
        ("What is the exterior angle property?", "An exterior angle of a triangle equals the sum of the two interior opposite angles."),
    ]
    make(9, "lines-and-angles", 6, "IV", 6, "Lines and Angles", "lines and angles",
         "If a ray stands on a line, the sum of the two adjacent angles so formed is 180° and the converse; if two lines intersect, vertically opposite angles are equal; lines parallel to a given line are parallel; angles formed by a transversal with parallel lines (summary of the CBSE syllabus)",
         "Class 9 Lines and Angles worksheet (NCERT Chapter 6): complementary and supplementary angles, linear pairs, vertically opposite angles, parallel lines and a transversal, angle sum of a triangle. 100 questions with answers.",
         "Linear pair = 180°, vertically opposite angles are equal", "Parallel lines: corresponding and alternate angles are equal, co-interior angles add to 180°.",
         body, faq, sets, R)


if __name__ == "__main__":
    main()
