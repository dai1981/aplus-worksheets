# -*- coding: utf-8 -*-
"""
SG Secondary 3 Maths: Symmetry Properties of Circles (MOE syllabus G3)
  python3 tools/gen_sg_maths_s3_symmetry_properties_of_circles.py
The perpendicular from the centre bisects a chord, finding chord lengths, distances and radii with Pythagoras'
theorem, equal chords are equidistant from the centre, tangents from an external point are equal, the tangent
is perpendicular to the radius, and the line from the external point to the centre bisects the angle between
the tangents.
Wrong answers come from real mistakes: using the whole chord instead of half of it, adding the squares when
one should be subtracted, forgetting to double the half-chord, and thinking the angle between the tangents
equals the angle at the centre.
"""
import math
import random
from sg_sec import num, S, make, lesson, collect, T, QN, fig, MINUS
from us_geo import Canvas, pol

R = random.Random(831500)
TRIP = [(3, 4, 5), (5, 12, 13), (6, 8, 10), (8, 15, 17), (9, 12, 15), (12, 16, 20), (7, 24, 25), (20, 21, 29), (12, 5, 13), (8, 6, 10), (4, 3, 5), (15, 8, 17)]


def r1(x):
    from fractions import Fraction
    return Fraction("%.1f" % x)


def d1(x):
    return ("%.1f" % x).replace("-", MINUS)


def chord_fig(r_px=90, d_frac=0.5, labels=None, label="circle with a chord and the perpendicular from the centre"):
    """chord AB below O at distance d; M is the midpoint"""
    c = Canvas()
    O = (0, 0)
    c.circle(O, r_px)
    d = d_frac * r_px
    h = math.sqrt(r_px * r_px - d * d)
    A, B, M = (-h, d), (h, d), (0, d)
    c.seg(A, B)
    c.seg(O, M, dash=True)
    c.seg(O, B, col="#1f6fd1")
    c.right(M, B, O)
    for p in (O, A, B, M):
        c.dot(p, 3.5)
    lab = labels or {}
    c.text((O[0] - 12, O[1] - 10), "O", 15)
    c.text((A[0] - 14, A[1] + 6), "A", 15)
    c.text((B[0] + 14, B[1] + 6), "B", 15)
    c.text((M[0], M[1] + 18), "M", 15)
    if "OM" in lab:
        c.text((-16, d / 2), lab["OM"], 14, col="#c0392b")
    if "OB" in lab:
        c.text((h / 2 + 12, d / 2 - 8), lab["OB"], 14, col="#1f6fd1")
    if "AB" in lab:
        c.text((0, d + 36), lab["AB"], 14, col="#c0392b")
    if "MB" in lab:
        c.text((h / 2, d + 18), lab["MB"], 14, col="#c0392b")
    return fig(c.svg(label))


def tangent_fig(t_deg=60, labels=None, label="two tangents from an external point T to a circle with centre O"):
    """tangents TA and TB from T on the right; angle ATB = t_deg"""
    c = Canvas()
    O = (0, 0)
    r_px = 70
    half = math.radians(t_deg / 2)
    dist = r_px / math.sin(half)
    T_ = (dist, 0)
    # tangent points: angle at O between OT and OA is 90 − t/2
    phi = 90 - t_deg / 2
    A = pol(0, 0, r_px, phi)
    B = pol(0, 0, r_px, -phi)
    c.circle(O, r_px)
    c.seg(T_, A)
    c.seg(T_, B)
    c.seg(O, A, col="#1f6fd1")
    c.seg(O, B, col="#1f6fd1")
    c.seg(O, T_, dash=True)
    c.right(A, O, T_)
    c.right(B, O, T_)
    for p in (O, A, B, T_):
        c.dot(p, 3.5)
    c.text((O[0] - 14, O[1]), "O", 15)
    c.vlabel(A, "A", O, 16)
    c.vlabel(B, "B", O, 16)
    c.text((T_[0] + 14, T_[1]), "T", 15)
    lab = labels or {}
    if "T" in lab:
        c.arc(T_, A, B, r=22)
        L = min(46, 0.6 * r_px / math.tan(half))
        off = min(10, 0.5 * L * math.tan(half))
        c.text((T_[0] - L, T_[1] - off), lab["T"], 14)
    if "O" in lab:
        c.angle(O, A, B, lab["O"], r=20, tr=36)
    if "TA" in lab:
        c.side_label(T_, A, lab["TA"], O, 14, 14, "#c0392b")
    if "OA" in lab:
        c.side_label(O, A, lab["OA"], T_, 12, 14, "#1f6fd1")
    return fig(c.svg(label))


# ------------------------------------------------------------ set 1: finding the chord length
def one_chord(r):
    a, b, h = r.choice(TRIP)       # OM = a, half chord = b, radius = h
    k = r.choice([1, 1, 2])
    a, b, h = a * k, b * k, h * k
    pic = chord_fig(90, a / h, {"OM": "%d cm" % a, "OB": "%d cm" % h})
    q = "O is the centre of the circle. OM is perpendicular to the chord AB, OM = %d cm and the radius is %d cm. Find the length of AB.%s" % (a, h, pic)
    return QN(q, 2 * b, [b, r1(math.hypot(a, h) * 2), 2 * (h - a)], "OM bisects AB. MB = √(%d² − %d²) = √%d = %d cm, so AB = 2 × %d = <b>%d cm</b>." % (h, a, h * h - a * a, b, b, 2 * b), unit=" cm")


# ------------------------------------------------------------ set 2: finding the distance or the radius
def one_dist(r):
    a, b, h = r.choice(TRIP)
    k = r.choice([1, 1, 2])
    a, b, h = a * k, b * k, h * k
    kind = r.choice(["dist", "radius", "dp"])
    if kind == "dist":
        pic = chord_fig(90, a / h, {"OB": "%d cm" % h, "AB": "AB = %d cm" % (2 * b)})
        q = "A chord AB of length %d cm is in a circle of radius %d cm with centre O. Find the distance OM of the chord from the centre.%s" % (2 * b, h, pic)
        return QN(q, a, [r1(math.sqrt(abs(h * h - 4 * b * b))) if h * h != 4 * b * b else h - b, h - b, r1(math.hypot(h, b))],
                  "M is the midpoint, so MB = %d cm. OM = √(%d² − %d²) = <b>%d cm</b>." % (b, h, b, a), unit=" cm")
    if kind == "radius":
        pic = chord_fig(90, a / h, {"OM": "%d cm" % a, "AB": "AB = %d cm" % (2 * b)})
        q = "A chord AB of length %d cm is %d cm from the centre O. Find the radius of the circle.%s" % (2 * b, a, pic)
        return QN(q, h, [r1(math.hypot(a, 2 * b)), a + b, b], "MB = %d cm. Radius OB = √(%d² + %d²) = <b>%d cm</b>." % (b, a, b, h), unit=" cm")
    rr = r.randint(6, 15)
    ch = r.randint(4, 2 * rr - 2)
    dd = math.sqrt(rr * rr - (ch / 2) ** 2)
    q = "A chord of length %d cm is drawn in a circle of radius %d cm. Find its distance from the centre, correct to 1 decimal place." % (ch, rr)
    return T(q, "%s cm" % d1(dd), ["%s cm" % d1(math.sqrt(abs(rr * rr - ch * ch))) if rr > ch else "%s cm" % d1(rr - ch / 2), "%s cm" % d1(math.hypot(rr, ch / 2)), "%s cm" % d1(rr - ch / 2) if abs(rr - ch / 2 - dd) > 0.05 else "%s cm" % d1(dd + 1)],
             "Half the chord is %s cm. Distance = √(%d² − %s²) = <b>%s cm</b>." % ("%g" % (ch / 2), rr, "%g" % (ch / 2), d1(dd)))


# ------------------------------------------------------------ set 3: properties and equal chords
FACTS = [
    ("The perpendicular from the centre of a circle to a chord", "bisects the chord", ["is equal to the radius", "bisects the angle at the centre only when the chord is a diameter", "is always half the chord"]),
    ("The perpendicular bisector of a chord", "passes through the centre of the circle", ["is a tangent to the circle", "is parallel to the chord", "is equal in length to the chord"]),
    ("Two equal chords in the same circle", "are the same distance from the centre", ["are parallel", "meet at the centre", "are both diameters"]),
    ("Two tangents drawn to a circle from the same external point", "are equal in length", ["are perpendicular to each other", "are parallel", "meet the circle at the ends of a diameter"]),
    ("A tangent to a circle", "is perpendicular to the radius at the point of contact", ["passes through the centre", "is parallel to the radius at the point of contact", "cuts the circle at two points"]),
    ("The line joining an external point to the centre of the circle", "bisects the angle between the two tangents from that point", ["is perpendicular to both tangents", "is equal to the radius", "bisects both tangents"]),
]


def one_equal(r):
    if r.random() < 0.45:
        stem, right, wr = r.choice(FACTS)
        return T("Complete the statement: %s …" % stem, right, wr, "This is a symmetry property of circles: %s <b>%s</b>." % (stem.lower(), right))
    a, b, h = r.choice(TRIP)
    k = r.choice([1, 2])
    a, b, h = a * k, b * k, h * k
    kind = r.choice(["eqdist", "eqchord", "compare"])
    if kind == "eqdist":
        q = "AB and CD are chords of a circle with centre O and radius %d cm. AB = CD = %d cm. How far is CD from O?" % (h, 2 * b)
        return QN(q, a, [b, h - b, 2 * a], "Equal chords are the same distance from the centre. Distance = √(%d² − %d²) = <b>%d cm</b>." % (h, b, a), unit=" cm")
    if kind == "eqchord":
        q = "In a circle of radius %d cm, chords PQ and RS are both %d cm from the centre. PQ = %d cm. What is RS?" % (h, a, 2 * b)
        return QN(q, 2 * b, [b, a, 2 * h], "Chords the same distance from the centre are equal: <b>RS = %d cm</b>." % (2 * b), unit=" cm")
    c1, c2 = sorted(r.sample(range(4, 2 * h - 1, 2), 2))
    q = "In a circle with centre O, chord AB = %d cm and chord CD = %d cm. Which chord is closer to O?" % (c1, c2)
    return T(q, "CD", ["AB", "They are the same distance from O", "You cannot tell without the radius"],
             "The longer chord is closer to the centre (the half-chord is longer, so the distance √(r² − half²) is smaller): <b>CD</b>.")


# ------------------------------------------------------------ set 4: tangents
def one_tan(r):
    kind = r.choice(["len", "len", "dist", "eq", "ang"])
    if kind in ("len", "dist"):
        a, b, h = r.choice(TRIP)       # radius a, tangent b, OT h
        k = r.choice([1, 2])
        a, b, h = a * k, b * k, h * k
        t = 2 * math.degrees(math.asin(a / h))
        if kind == "len":
            pic = tangent_fig(t, {"OA": "%d" % a})
            q = "TA and TB are tangents to the circle with centre O. The radius is %d cm and OT = %d cm. Find the length of TA.%s" % (a, h, pic)
            return QN(q, b, [h - a, r1(math.hypot(a, h)), h + a], "∠OAT = 90° (tangent ⟂ radius). TA = √(%d² − %d²) = <b>%d cm</b>." % (h, a, b), unit=" cm")
        pic = tangent_fig(t, {"OA": "%d" % a, "TA": "%d" % b})
        q = "TA is a tangent to the circle with centre O. OA = %d cm and TA = %d cm. Find OT.%s" % (a, b, pic)
        return QN(q, h, [a + b, r1(math.sqrt(abs(b * b - a * a))) if b != a else b, b], "∠OAT = 90°, so OT = √(%d² + %d²) = <b>%d cm</b>." % (a, b, h), unit=" cm")
    if kind == "eq":
        t = r.randint(5, 20)
        q = "TA and TB are tangents from the point T to a circle. TA = %d cm. What is TB?" % t
        return QN(q, t, [2 * t, t + 5, F_half(t)], "Tangents from an external point are equal in length: <b>TB = %d cm</b>." % t, unit=" cm")
    t = r.choice([40, 50, 56, 60, 64, 70, 72, 80, 84, 90, 100, 110])
    o = 180 - t
    want = r.choice(["O", "OTA", "OAB"])
    if want == "O":
        pic = tangent_fig(t, {"T": "%d°" % t})
        q = "TA and TB are tangents to the circle with centre O, and ∠ATB = %d°. Find ∠AOB.%s" % (t, pic)
        return QN(q, o, [t, 90 - t // 2, 360 - t], "∠OAT = ∠OBT = 90°. The angles of quadrilateral OATB add up to 360°, so ∠AOB = 360° − 90° − 90° − %d° = <b>%d°</b>." % (t, o), unit="°")
    if want == "OTA":
        pic = tangent_fig(t, {"T": "%d°" % t})
        q = "TA and TB are tangents to the circle with centre O, and ∠ATB = %d°. Find ∠OTA.%s" % (t, pic)
        return QN(q, t // 2 if t % 2 == 0 else t / 2, [t, 90 - t / 2, 180 - t], "OT bisects the angle between the tangents: ∠OTA = %d° ÷ 2 = <b>%s°</b>." % (t, "%g" % (t / 2)), unit="°")
    pic = tangent_fig(t, {"T": "%d°" % t})
    q = "TA and TB are tangents to the circle with centre O, and ∠ATB = %d°. Find ∠TAB.%s" % (t, pic)
    v = (180 - t) / 2
    return QN(q, v, [t, 90 - v, 180 - t], "TA = TB, so △TAB is isosceles: ∠TAB = (180° − %d°) ÷ 2 = <b>%s°</b>." % (t, "%g" % v), unit="°")


def F_half(t):
    return t / 2


# ------------------------------------------------------------ set 5: mixed problems
def one_prob(r):
    kind = r.choice(["two", "two", "perim", "kite", "arch"])
    if kind == "two":
        rr = r.choice([13, 25, 17, 10, 15])
        opts = [(a, b) for a, b, h in TRIP if h == rr] + [(a * 2, b * 2) for a, b, h in TRIP if h * 2 == rr]
        if len(opts) < 2:
            return None
        (a1, b1), (a2, b2) = r.sample(opts, 2)
        same = r.choice([True, False])
        dist = abs(a1 - a2) if same else a1 + a2
        q = "Two parallel chords of lengths %d cm and %d cm are drawn in a circle of radius %d cm, on %s of the centre. Find the distance between the chords." % (2 * b1, 2 * b2, rr, "the same side" if same else "opposite sides")
        return QN(q, dist, [a1 + a2 if same else abs(a1 - a2), abs(b1 - b2) if b1 != b2 else b1, a1], "Distances from the centre: √(%d² − %d²) = %d and √(%d² − %d²) = %d. On %s, %s: <b>%d cm</b>." % (
            rr, b1, a1, rr, b2, a2, "the same side" if same else "opposite sides", "subtract" if same else "add", dist), unit=" cm")
    if kind == "perim":
        a, b, h = r.choice(TRIP)
        q = "TA and TB are tangents from T to a circle with centre O and radius %d cm. OT = %d cm. Find the perimeter of the kite OATB." % (a, h)
        return QN(q, 2 * (a + b), [a + b, 2 * (a + h), 2 * b + h], "TA = TB = √(%d² − %d²) = %d cm and OA = OB = %d cm. Perimeter = 2 × (%d + %d) = <b>%d cm</b>." % (h, a, b, a, a, b, 2 * (a + b)), unit=" cm")
    if kind == "kite":
        a, b, h = r.choice(TRIP)
        q = "TA and TB are tangents from T to a circle with centre O and radius %d cm. TA = %d cm. Find the area of the kite OATB." % (a, b)
        return QN(q, a * b, [a * b // 2 if a * b % 2 == 0 else a * b * 2, a * h, (a + b) * 2], "Triangles OAT and OBT are congruent right-angled triangles, each with area ½ × %d × %d. Kite area = 2 × ½ × %d × %d = <b>%d cm²</b>." % (a, b, a, b, a * b), unit=" cm²")
    a, b, h = r.choice(TRIP)
    k = r.choice([1, 2])
    a, b, h = a * k, b * k, h * k
    q = "A tunnel is shaped like part of a circle of radius %d m. The floor is a horizontal chord %d m wide. How high is the highest point of the tunnel above the floor, if the centre is above the floor?" % (h, 2 * b)
    return QN(q, a + h, [h - a, h, 2 * a], "The centre is √(%d² − %d²) = %d m above the floor, and the top is one radius above the centre: %d + %d = <b>%d m</b>." % (h, b, a, a, h, a + h), unit=" m")


def build():
    sets = [S("Finding the length of a chord", collect(one_chord, 20, R)),
            S("Finding distances and radii", collect(one_dist, 20, R)),
            S("Symmetry facts and equal chords", collect(one_equal, 20, R)),
            S("Tangents from an external point", collect(one_tan, 20, R)),
            S("Problems", collect(one_prob, 20, R))]
    body = lesson(
        "<ul><li>The <b>perpendicular from the centre to a chord bisects the chord</b>, and the perpendicular bisector of a chord passes through the centre.</li>"
        "<li><b>Equal chords are equidistant from the centre</b> (and chords equidistant from the centre are equal).</li>"
        "<li>A <b>tangent is perpendicular to the radius</b> at the point of contact.</li>"
        "<li><b>Tangents from an external point are equal</b>, and the line from the point to the centre bisects the angle between them.</li>"
        "<li>Each fact gives a right angle, so use Pythagoras' theorem with the radius as the hypotenuse.</li></ul>",
        [("A chord is 16 cm long and the radius is 10 cm. How far is the chord from the centre?", ["Half the chord = 8 cm", "√(10² − 8²) = √36"], "6 cm"),
         ("Tangents TA and TB meet at T with ∠ATB = 50°. Find ∠AOB.", ["∠OAT = ∠OBT = 90°", "360° − 90° − 90° − 50°"], "130°")],
        ["Using the whole chord instead of half of it in Pythagoras' theorem.",
         "Adding squares when the radius is the hypotenuse and you need a shorter side.",
         "Forgetting to double the half-chord at the end.",
         "Thinking ∠AOB equals ∠ATB. They add up to 180°."])
    faq = [("What are the symmetry properties of circles?", "The perpendicular from the centre bisects a chord, equal chords are equidistant from the centre, tangents from an external point are equal, and the line from that point to the centre bisects the angle between the tangents."),
           ("Why is a tangent perpendicular to the radius?", "The radius to the point of contact is the shortest distance from the centre to the tangent line, so it meets the tangent at 90°."),
           ("How do I find the length of a chord?", "Draw the perpendicular from the centre. Use Pythagoras' theorem with the radius as the hypotenuse to find half the chord, then double it."),
           ("What is the angle between two tangents and the angle at the centre?", "They add up to 180°, because the two right angles at the points of contact make 180° of the 360° in the kite.")]
    make(3, "symmetry-properties-of-circles", 15, "G3",
         "Symmetry Properties of Circles: Chords and Tangents",
         "", "Symmetry properties of circles", "",
         "Free Secondary 3 maths worksheets on symmetry properties of circles: perpendicular bisectors of chords, equal chords, tangents from an external point and tangent-radius right angles. 100 questions with answers.",
         "The perpendicular from the centre bisects a chord; a tangent meets the radius at 90°.",
         "Tangents from an external point are equal. Use Pythagoras' theorem with the radius.",
         body, faq, sets, R)


if __name__ == "__main__":
    build()
