# -*- coding: utf-8 -*-
"""
SG Secondary 3 Maths: Angle Properties of Circles (MOE syllabus G3)
  python3 tools/gen_sg_maths_s3_angle_properties_of_circles.py
Angle at the centre is twice the angle at the circumference, angle in a semicircle, tangent and radius,
angles in the same segment, angles in opposite segments (cyclic quadrilaterals), and multi-step problems.
Every diagram is drawn to scale from the numbers in the question.
Wrong answers come from real mistakes: halving instead of doubling, using 180° instead of 90° in a semicircle,
adding opposite angles of a cyclic quadrilateral to 360°, and forgetting that OA = OB makes an isosceles triangle.
"""
import random
from sg_sec import num, S, make, lesson, collect, QN, T, fig
from us_geo import Canvas, pol

R = random.Random(831600)
RAD = 85


def P(d):
    return pol(0, 0, RAD, d)


def cfig(pts, segs, marks=(), rights=(), centre=True, extra=None, label="circle diagram"):
    """pts: {name: position in degrees}; segs: [(n1, n2)]; marks: [(vertex, a, b, text)]"""
    c = Canvas()
    O = (0, 0)
    c.circle(O, RAD)
    xy = {n: P(d) for n, d in pts.items()}
    xy["O"] = O
    if extra:
        extra(c, xy)
    for a, b in segs:
        c.seg(xy[a], xy[b], col="#1f6fd1" if "O" in (a, b) else "#2b2b2b")
    for v, a, b in rights:
        c.right(xy[v], xy[a], xy[b])
    for v, a, b, t in marks:
        c.angle(xy[v], xy[a], xy[b], t, r=20 if v != "O" else 16, tr=38 if v != "O" else 32)
    for n, p in xy.items():
        if n == "O":
            if centre:
                c.dot(p, 3.5)
                c.text((p[0] - 12, p[1] + 14), "O", 15)
        elif n in pts:
            c.dot(p, 3.5)
            c.vlabel(p, n, O, 16)
    return fig(c.svg(label))


def deg(v):
    return "%s°" % num(v)


# ------------------------------------------------------------ set 1: angle at the centre
def one_centre(r):
    kind = r.choice(["find_c", "find_c", "find_p", "reflex"])
    a0 = r.randint(200, 340)
    if kind in ("find_c", "find_p"):
        cen = r.choice(range(40, 171, 2))
        A, B = a0, a0 + cen
        Pp = A + cen + (360 - cen) * r.uniform(0.35, 0.65)
        pts = {"A": A, "B": B, "P": Pp}
        if kind == "find_c":
            x = cen // 2
            pic = cfig(pts, [("A", "O"), ("B", "O"), ("A", "P"), ("B", "P")], [("P", "A", "B", deg(x))], label="angle at the centre and at the circumference")
            return QN("O is the centre of the circle. ∠APB = %s. Find ∠AOB.%s" % (deg(x), pic), cen, [x, 180 - x, 180 - cen], "The angle at the centre is twice the angle at the circumference: ∠AOB = 2 × %s = <b>%s</b>." % (deg(x), deg(cen)), unit="°")
        pic = cfig(pts, [("A", "O"), ("B", "O"), ("A", "P"), ("B", "P")], [("O", "A", "B", deg(cen))], label="angle at the centre and at the circumference")
        return QN("O is the centre of the circle. ∠AOB = %s. Find ∠APB.%s" % (deg(cen), pic), cen // 2, [cen, 180 - cen, 90 - cen // 2], "∠APB is half the angle at the centre: %s ÷ 2 = <b>%s</b>." % (deg(cen), deg(cen // 2)), unit="°")
    cen = r.choice(range(60, 161, 4))
    A, B = a0, a0 + cen
    Pp = A + cen * r.uniform(0.35, 0.65)
    pts = {"A": A, "B": B, "P": Pp}
    pic = cfig(pts, [("A", "O"), ("B", "O"), ("A", "P"), ("B", "P")], [("O", "A", "B", deg(cen))], label="P on the minor arc")
    ref = 360 - cen
    return QN("O is the centre of the circle. ∠AOB = %s and P is on the minor arc AB. Find ∠APB.%s" % (deg(cen), pic), ref // 2, [cen // 2, ref, 180 - cen], "P is on the minor arc, so use the reflex angle at the centre: 360° − %s = %s. ∠APB = %s ÷ 2 = <b>%s</b>." % (deg(cen), deg(ref), deg(ref), deg(ref // 2)), unit="°")


# ------------------------------------------------------------ set 2: semicircle and tangent
def one_semi(r):
    kind = r.choice(["semi", "semi", "semi_o", "tan", "tan2"])
    if kind in ("semi", "semi_o"):
        x = r.randint(20, 70)
        # AB diameter horizontal, C on the upper arc with ∠CAB = x  ->  C at position 180 − 2x? angle CAB = half of angle COB
        pts = {"A": 180, "B": 0, "C": 2 * (90 - x) if False else 180 - 2 * x}
        # ∠CAB subtends arc CB; ∠COB = 2x, so C is at 2x
        pts["C"] = 2 * x
        if kind == "semi":
            pic = cfig(pts, [("A", "B"), ("A", "C"), ("B", "C")], [("A", "C", "B", deg(x))], label="triangle in a semicircle")
            return QN("AB is a diameter of the circle with centre O. ∠CAB = %s. Find ∠ABC.%s" % (deg(x), pic), 90 - x, [180 - x, x, 90 + x], "The angle in a semicircle is 90°, so ∠ACB = 90°. ∠ABC = 180° − 90° − %s = <b>%s</b>." % (deg(x), deg(90 - x)), unit="°")
        pic = cfig(pts, [("A", "B"), ("A", "C"), ("B", "C"), ("O", "C")], [("A", "C", "B", deg(x))], label="triangle in a semicircle with a radius")
        return QN("AB is a diameter of the circle with centre O. ∠CAB = %s. Find ∠OCB.%s" % (deg(x), pic), 90 - x, [x, 2 * x, 180 - 2 * x], "OB = OC (radii), so ∠OCB = ∠OBC. ∠ACB = 90° (semicircle), so ∠ABC = 90° − %s = %s. <b>∠OCB = %s</b>." % (deg(x), deg(90 - x), deg(90 - x)), unit="°")
    x = r.randint(25, 65)
    # tangent at A (position 90, top), external point T on the tangent to the right, ∠AOT = x
    def ext(c, xy):
        A = xy["A"]
        import math
        L = RAD * math.tan(math.radians(x))
        xy["T"] = (A[0] + L, A[1])
        c.seg((A[0] - 50, A[1]), (A[0] + L + 30, A[1]))
        c.seg(xy["O"], xy["T"], col="#2b2b2b")
        c.dot(xy["T"], 3.5)
        c.text((xy["T"][0] + 4, xy["T"][1] - 16), "T", 15)
    pts = {"A": 90}
    if kind == "tan":
        pic = cfig(pts, [("O", "A")], [("O", "A", "T", deg(x))], rights=[("A", "O", "T")], extra=ext, label="tangent at A and a line from the centre")
        return QN("TA is a tangent to the circle at A, and O is the centre. ∠AOT = %s. Find ∠ATO.%s" % (deg(x), pic), 90 - x, [x, 180 - x, 90 + x], "A tangent is perpendicular to the radius, so ∠OAT = 90°. ∠ATO = 180° − 90° − %s = <b>%s</b>." % (deg(x), deg(90 - x)), unit="°")
    y = 90 - x
    pic = cfig(pts, [("O", "A")], [("T", "A", "O", deg(y))], extra=ext, label="tangent at A and a line from the centre")
    return QN("TA is a tangent to the circle at A, and O is the centre. ∠ATO = %s. Find ∠AOT.%s" % (deg(y), pic), x, [y, 90, 180 - y], "∠OAT = 90° (tangent ⟂ radius), so ∠AOT = 180° − 90° − %s = <b>%s</b>." % (deg(y), deg(x)), unit="°")


# ------------------------------------------------------------ set 3: angles in the same segment
def one_same(r):
    kind = r.choice(["same", "same", "same2", "bow"])
    a0 = r.randint(200, 320)
    arc = r.choice(range(50, 161, 2))
    A, B = a0, a0 + arc
    gap = 360 - arc
    C = B + gap * r.uniform(0.2, 0.4)
    D = B + gap * r.uniform(0.6, 0.8)
    x = arc // 2
    pts = {"A": A, "B": B, "C": C, "D": D}
    if kind == "same":
        pic = cfig(pts, [("A", "C"), ("B", "C"), ("A", "D"), ("B", "D")], [("C", "A", "B", deg(x))], centre=False, label="two angles standing on the same arc")
        return QN("A, B, C and D lie on a circle. ∠ACB = %s. Find ∠ADB.%s" % (deg(x), pic), x, [2 * x, 180 - x, 90 - x], "∠ACB and ∠ADB stand on the same arc AB (angles in the same segment), so ∠ADB = <b>%s</b>." % deg(x), unit="°")
    if kind == "same2":
        y = r.randint(25, 70)
        pic = cfig(pts, [("A", "C"), ("B", "C"), ("A", "D"), ("B", "D")], [("C", "A", "B", deg(x))], centre=False, label="two angles standing on the same arc")
        return QN("A, B, C and D lie on a circle. ∠ACB = %s. What is ∠ADB + ∠ACB?%s" % (deg(x), pic), 2 * x, [x, 180, 180 - x], "Angles in the same segment are equal, so ∠ADB = %s and the sum is <b>%s</b>." % (deg(x), deg(2 * x)), unit="°")
    # bow-tie: chords AC and BD cross at X; ∠BAC = ∠BDC
    y = r.randint(25, 60)
    z = r.randint(30, 70)
    if y + z >= 150:
        return None
    # A, B, C, D in order; ∠BAC stands on arc BC, ∠ABD stands on arc AD
    a = r.randint(100, 140)
    b = a + 2 * z    # arc AB? keep a simple consistent layout
    Bp = 200
    Cp = Bp + 2 * y
    Dp = Cp + r.randint(40, 80)
    Ap = Dp + r.randint(50, 90)
    if Ap - Bp >= 340:
        return None
    pts = {"A": Ap, "B": Bp, "C": Cp, "D": Dp}
    pic = cfig(pts, [("A", "C"), ("B", "D"), ("A", "B"), ("C", "D")], [("A", "B", "C", deg(y))], centre=False, label="chords AC and BD crossing")
    return QN("A, B, C and D lie on a circle, and the chords AC and BD cross. ∠BAC = %s. Find ∠BDC.%s" % (deg(y), pic), y, [2 * y, 180 - y, 90 - y], "∠BAC and ∠BDC both stand on arc BC, so they are equal: <b>%s</b>." % deg(y), unit="°")


# ------------------------------------------------------------ set 4: cyclic quadrilaterals
def one_cyc(r):
    kind = r.choice(["opp", "opp", "ext", "two"])
    # positions A, B, C, D around the circle
    arcs = [r.randint(50, 120) for _ in range(3)]
    if sum(arcs) >= 310:
        return None
    arcs.append(360 - sum(arcs))
    if arcs[3] < 40:
        return None
    s = r.randint(0, 359)
    pos = [s, s + arcs[0], s + arcs[0] + arcs[1], s + arcs[0] + arcs[1] + arcs[2]]
    pts = dict(zip("ABCD", pos))
    # interior angle at A = half of arc BCD = (arcs[1] + arcs[2]) / 2
    angA = (arcs[1] + arcs[2]) / 2
    angC = (arcs[3] + arcs[0]) / 2
    if angA != int(angA):
        return None
    angA, angC = int(angA), int(angC)
    quad = [("A", "B"), ("B", "C"), ("C", "D"), ("D", "A")]
    if kind == "opp":
        pic = cfig(pts, quad, [("A", "D", "B", deg(angA))], centre=False, label="cyclic quadrilateral ABCD")
        return QN("ABCD is a cyclic quadrilateral. ∠DAB = %s. Find ∠BCD.%s" % (deg(angA), pic), angC, [angA, 360 - angA, 90 - angA if angA < 90 else angA - 90], "Opposite angles of a cyclic quadrilateral add up to 180° (angles in opposite segments): ∠BCD = 180° − %s = <b>%s</b>." % (deg(angA), deg(angC)), unit="°")
    if kind == "ext":
        def ext(c, xy):
            # extend DC beyond C to E
            Cx, Cy = xy["C"]
            Dx, Dy = xy["D"]
            E = (Cx + (Cx - Dx) * 0.45, Cy + (Cy - Dy) * 0.45)
            xy["E"] = E
            c.seg(xy["C"], E)
            c.text((E[0] + 10, E[1] + 4), "E", 15)
        pic = cfig(pts, quad, [("A", "D", "B", deg(angA))], centre=False, extra=ext, label="cyclic quadrilateral with DC extended to E")
        return QN("ABCD is a cyclic quadrilateral and DC is extended to E. ∠DAB = %s. Find ∠BCE.%s" % (deg(angA), pic), angA, [angC, 180 - angC if 180 - angC != angA else 90, 360 - angA], "∠BCD = 180° − %s = %s, so ∠BCE = 180° − %s = <b>%s</b>. The exterior angle equals the interior opposite angle." % (deg(angA), deg(angC), deg(angC), deg(angA)), unit="°")
    angB = (arcs[2] + arcs[3]) / 2
    if angB != int(angB):
        return None
    angB = int(angB)
    angD = 180 - angB
    pic = cfig(pts, quad, [("A", "D", "B", deg(angA)), ("B", "A", "C", deg(angB))], centre=False, label="cyclic quadrilateral ABCD")
    return QN("ABCD is a cyclic quadrilateral with ∠DAB = %s and ∠ABC = %s. Find ∠ADC.%s" % (deg(angA), deg(angB), pic), angD, [angC, 360 - angA - angB, angB], "∠ADC is opposite ∠ABC, so ∠ADC = 180° − %s = <b>%s</b>." % (deg(angB), deg(angD)), unit="°")


# ------------------------------------------------------------ set 5: multi-step problems
def one_mix(r):
    kind = r.choice(["iso", "iso", "centre_iso", "facts"])
    if kind == "iso":
        cen = r.choice(range(40, 161, 2))
        a0 = r.randint(200, 320)
        pts = {"A": a0, "B": a0 + cen}
        pic = cfig(pts, [("A", "O"), ("B", "O"), ("A", "B")], [("O", "A", "B", deg(cen))], label="isosceles triangle OAB")
        v = (180 - cen) // 2
        return QN("O is the centre of the circle. ∠AOB = %s. Find ∠OAB.%s" % (deg(cen), pic), v, [180 - cen, cen // 2, cen], "OA = OB (radii), so △OAB is isosceles: ∠OAB = (180° − %s) ÷ 2 = <b>%s</b>." % (deg(cen), deg(v)), unit="°")
    if kind == "centre_iso":
        cen = r.choice(range(40, 141, 4))
        a0 = r.randint(200, 320)
        Pp = a0 + cen + (360 - cen) * 0.5
        pts = {"A": a0, "B": a0 + cen, "P": Pp}
        v = (180 - cen) // 2
        pic = cfig(pts, [("A", "O"), ("B", "O"), ("A", "B"), ("A", "P"), ("B", "P")], [("P", "A", "B", deg(cen // 2))], label="angle at the circumference and triangle OAB")
        return QN("O is the centre of the circle and ∠APB = %s. Find ∠OBA.%s" % (deg(cen // 2), pic), v, [cen, cen // 2, 180 - cen], "∠AOB = 2 × %s = %s (angle at centre). OA = OB, so ∠OBA = (180° − %s) ÷ 2 = <b>%s</b>." % (deg(cen // 2), deg(cen), deg(cen), deg(v)), unit="°")
    facts = [("The angle in a semicircle is", "90°", ["180°", "45°", "twice the angle at the centre"]),
             ("The angle at the centre of a circle is", "twice the angle at the circumference on the same arc", ["half the angle at the circumference", "equal to the angle at the circumference", "always 90°"]),
             ("Angles in the same segment are", "equal", ["supplementary", "complementary", "double each other"]),
             ("Opposite angles of a cyclic quadrilateral", "add up to 180°", ["are equal", "add up to 360°", "add up to 90°"]),
             ("The angle between a tangent and the radius at the point of contact is", "90°", ["180°", "60°", "equal to the angle at the centre"])]
    s, a, w = r.choice(facts)
    return T("Complete the statement: %s …" % s, a, w, "This is an angle property of circles: %s <b>%s</b>." % (s.lower(), a))


def build():
    sets = [S("Angle at the centre", collect(one_centre, 20, R)),
            S("Angle in a semicircle and tangents", collect(one_semi, 20, R)),
            S("Angles in the same segment", collect(one_same, 20, R)),
            S("Cyclic quadrilaterals", collect(one_cyc, 20, R)),
            S("Multi-step problems", collect(one_mix, 20, R))]
    body = lesson(
        "<ul><li>The <b>angle at the centre</b> is twice the angle at the circumference standing on the same arc.</li>"
        "<li>The <b>angle in a semicircle</b> is 90°, and the angle between a <b>tangent and a radius</b> is 90°.</li>"
        "<li><b>Angles in the same segment</b> (standing on the same arc) are equal.</li>"
        "<li><b>Angles in opposite segments</b> add up to 180°: opposite angles of a cyclic quadrilateral are supplementary.</li>"
        "<li>Look for radii: OA = OB makes an isosceles triangle.</li></ul>",
        [("∠APB = 38° at the circumference. Find ∠AOB at the centre.", ["Angle at centre = 2 × angle at circumference"], "76°"),
         ("ABCD is cyclic and ∠A = 104°. Find ∠C.", ["Opposite angles add to 180°"], "76°")],
        ["Halving when you should double (and the other way round).",
         "Using 180° instead of 90° for the angle in a semicircle.",
         "Adding opposite angles of a cyclic quadrilateral to 360°.",
         "Missing the isosceles triangle formed by two radii."])
    faq = [("What are the angle properties of circles?", "The angle at the centre is twice the angle at the circumference, the angle in a semicircle is 90°, angles in the same segment are equal, opposite angles of a cyclic quadrilateral add to 180°, and a tangent meets a radius at 90°."),
           ("What is a cyclic quadrilateral?", "A quadrilateral with all four vertices on a circle. Its opposite angles add up to 180°."),
           ("What does 'angles in the same segment' mean?", "Angles at the circumference that stand on the same chord or arc, on the same side of it. They are always equal."),
           ("How do I give reasons in a circle proof?", "Name the property each time, for example '∠ACB = 90° (angle in a semicircle)' or 'OA = OB (radii)'.")]
    make(3, "angle-properties-of-circles", 16, "G3",
         "Angle Properties of Circles",
         "", "Angle properties of circles", "",
         "Free Secondary 3 maths worksheets on angle properties of circles: angle at the centre, angle in a semicircle, tangent and radius, angles in the same segment and cyclic quadrilaterals. 100 questions with answers.",
         "The angle at the centre is twice the angle at the circumference.",
         "Angle in a semicircle = 90°; same segment angles are equal; opposite angles of a cyclic quadrilateral add to 180°.",
         body, faq, sets, R)


if __name__ == "__main__":
    build()
