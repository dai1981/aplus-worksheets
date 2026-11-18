# -*- coding: utf-8 -*-
"""
SG Secondary 3 Maths: Bearings and Angles of Elevation and Depression (MOE syllabus G4: problems in two
dimensions including angles of elevation and depression and bearings)
  python3 tools/gen_sg_maths_s3_bearings_and_angles_of_elevation.py
Three-figure bearings from diagrams, back bearings, angles of elevation, angles of depression, and problems
that combine bearings with right-angled trigonometry.
Wrong answers come from real mistakes: measuring from east or anticlockwise, writing 45° instead of 045°,
adding 90° instead of 180° for a back bearing, and using sin or cos where tan is needed.
"""
import math
import random
from sg_sec import num, S, make, lesson, collect, T, fig, svg_wrap, line, text, MINUS, People

R = random.Random(831300)
P = People(R)
RED, BLUE, INK = "#c0392b", "#1f6fd1", "#2b2b2b"


def brg(d):
    return "%03d°" % (d % 360)


def d1(x):
    return ("%.1f" % x).replace("-", MINUS)


def tn(d):
    return math.tan(math.radians(d))


def sn(d):
    return math.sin(math.radians(d))


def cs(d):
    return math.cos(math.radians(d))


def compass(b, ref, ang):
    """A at centre, north arrow, line to B on bearing b; the marked angle ang is between AB and the ref direction"""
    cx, cy, L = 130, 125, 92
    dirs = {"N": 0, "E": 90, "S": 180, "W": 270}
    s = [line(cx, cy + 100, cx, cy - 98, "#999", 1.5, " stroke-dasharray='4 4'"), line(cx - 98, cy, cx + 98, cy, "#999", 1.5, " stroke-dasharray='4 4'")]
    s.append("<path d='M%d %d l-7 14 l14 0 Z' fill='%s'/>" % (cx, cy - 104, INK))
    s.append(text(cx, cy - 110, "N", 15))
    bx, by = cx + L * sn(b), cy - L * cs(b)
    s.append(line(cx, cy, bx, by, BLUE, 3))
    s.append("<circle cx='%d' cy='%d' r='4' fill='%s'/>" % (cx, cy, INK))
    s.append(text(cx + 20 * sn(b + 180 + 25), cy - 20 * cs(b + 180 + 25) + 5, "A", 15))
    s.append(text(bx + 12 * sn(b), by - 12 * cs(b) + 5, "B", 15))
    r0 = dirs[ref]
    # arc between ref and b, the short way
    a1, a2 = r0, b
    if (a2 - a1) % 360 > 180:
        a1, a2 = a2, a1
    rr = 34
    x1, y1 = cx + rr * sn(a1), cy - rr * cs(a1)
    x2, y2 = cx + rr * sn(a2), cy - rr * cs(a2)
    s.append("<path d='M%.1f %.1f A%d %d 0 0 1 %.1f %.1f' fill='none' stroke='%s' stroke-width='2'/>" % (x1, y1, rr, rr, x2, y2, RED))
    mid = a1 + ((a2 - a1) % 360) / 2
    s.append(text(cx + 58 * sn(mid), cy - 58 * cs(mid) + 5, "%d°" % ang, 14, col=RED))
    return fig(svg_wrap(260, 245, "".join(s), "compass diagram: the line AB makes %d degrees with the %s direction" % (ang, ref)))


# ------------------------------------------------------------ set 1: reading bearings
def one_read(r):
    ref = r.choice(["N", "E", "S", "W"])
    ang = r.randint(20, 70)
    side = r.choice([1, -1])
    base = {"N": 0, "E": 90, "S": 180, "W": 270}[ref]
    b = (base + side * ang) % 360
    q = "Find the bearing of B from A.%s" % compass(b, ref, ang)
    wr = [brg(ang) if brg(ang) != brg(b) else brg(360 - ang), brg(360 - b) if (360 - b) % 360 != b else brg(b + 90), brg(b + 180)]
    wr = [w for w in dict.fromkeys(wr) if w != brg(b)]
    if len(wr) < 3:
        wr.append(brg(b + 90))
    return T(q, brg(b), wr[:3], "Bearings are measured clockwise from north. %s So the bearing is <b>%s</b>." % (
        {"N": "", "E": "East is 090°. ", "S": "South is 180°. ", "W": "West is 270°. "}[ref] + ("Then %s %d°." % ("add" if side > 0 else "subtract", ang) if ref != "N" else ("Clockwise from north: %d°." % ang if side > 0 else "Anticlockwise %d° from north is 360° − %d°." % (ang, ang))), brg(b)))


# ------------------------------------------------------------ set 2: back bearings and angles between bearings
def one_back(r):
    kind = r.choice(["back", "back", "between", "turn"])
    if kind == "back":
        b = r.randint(5, 355)
        if b in (90, 180, 270):
            return None
        q = "The bearing of Q from P is %s. Find the bearing of P from Q." % brg(b)
        return T(q, brg(b + 180), [brg(360 - b), brg(b + 90), brg(b - 90) if b > 90 else brg(b + 270)],
                 "The bearing back is 180° different: %s %s 180° = <b>%s</b>." % (brg(b), "+" if b < 180 else MINUS, brg(b + 180)))
    if kind == "between":
        b1, b2 = sorted(r.sample(range(10, 350, 5), 2))
        d = b2 - b1
        if d > 180:
            d = 360 - d
        q = "From a lighthouse L, ship A is on a bearing of %s and ship B is on a bearing of %s. Find ∠ALB." % (brg(b1), brg(b2))
        return T(q, "%d°" % d, ["%d°" % (b1 + b2) if b1 + b2 < 360 and b1 + b2 != d else "%d°" % (180 - d), "%d°" % (360 - d), "%d°" % abs(180 - d) if abs(180 - d) != d else "%d°" % (d + 10)],
                 "Both bearings are measured from north, so the angle between them is the difference: %d° − %d° = <b>%d°</b>%s." % (b2, b1, b2 - b1, "" if d == b2 - b1 else ", and the smaller angle is 360° − %d° = %d°" % (b2 - b1, d)))
    nm, he, his = P.next()
    b = r.choice(range(10, 350, 5))
    t = r.choice([90, 45, 30, 60, 120])
    side = r.choice(["right", "left"])
    nb = b + t if side == "right" else b - t
    q = "%s walks on a bearing of %s, then turns %d° to the %s. What is %s new bearing?" % (nm, brg(b), t, side, his)
    return T(q, brg(nb), [brg(b - t if side == "right" else b + t), brg(nb + 180), brg(t)],
             "Turning right adds to the bearing; turning left subtracts. %s %s %d° = <b>%s</b>." % (brg(b), "+" if side == "right" else MINUS, t, brg(nb)))


# ------------------------------------------------------------ set 3: angles of elevation
def one_elev(r):
    kind = r.choice(["height", "height", "dist", "angle"])
    nm, he, his = P.next()
    if kind == "height":
        d = r.randint(15, 80)
        a = r.randint(15, 65)
        eye = r.choice([0, 0, 1.5, 1.6])
        h = d * tn(a) + eye
        obj = r.choice(["flagpole", "tree", "block of flats", "lamp post", "tower"])
        q = "%s stands %d m from the foot of a %s. The angle of elevation of the top is %d°%s. Find the height of the %s, correct to 1 decimal place." % (
            nm, d, obj, a, (" and %s eyes are %s m above the ground" % (his, ("%g" % eye))) if eye else "", obj)
        right = "%s m" % d1(h)
        return T(q, right, ["%s m" % d1(d * sn(a) + eye), "%s m" % d1(d / tn(a) + eye), "%s m" % d1(d * tn(a)) if eye else "%s m" % d1(d * cs(a))],
                 "tan %d° = height ÷ %d, so height = %d tan %d° = %s m%s. <b>%s</b>." % (a, d, d, a, d1(d * tn(a)), (", plus %g m for the eye level" % eye) if eye else "", right))
    if kind == "dist":
        h = r.randint(10, 120)
        a = r.randint(20, 70)
        d = h / tn(a)
        q = "The angle of elevation of the top of a %d m tall building from a point on level ground is %d°. How far is the point from the building, correct to 1 decimal place?" % (h, a)
        return T(q, "%s m" % d1(d), ["%s m" % d1(h * tn(a)), "%s m" % d1(h / sn(a)), "%s m" % d1(h * cs(a))],
                 "tan %d° = %d ÷ <i>d</i>, so <i>d</i> = %d ÷ tan %d° = <b>%s m</b>." % (a, h, h, a, d1(d)))
    h = r.randint(10, 90)
    d = r.randint(20, 120)
    a = math.degrees(math.atan(h / d))
    q = "A kite is %d m above the ground, directly above a point %d m from %s. Find the angle of elevation of the kite from %s, correct to 1 decimal place." % (h, d, nm, nm)
    return T(q, "%s°" % d1(a), ["%s°" % d1(90 - a), "%s°" % d1(math.degrees(math.asin(min(1, h / d)))) if h < d else "%s°" % d1(a / 2), "%s°" % d1(math.degrees(math.atan(d / h)) / 2)],
             "tan θ = %d ÷ %d, so θ = tan<sup>−1</sup>(%s) = <b>%s°</b>." % (h, d, ("%.4f" % (h / d)), d1(a)))


# ------------------------------------------------------------ set 4: angles of depression
def one_dep(r):
    kind = r.choice(["boat", "boat", "car", "angle", "two"])
    if kind == "boat":
        h = r.randint(20, 150)
        a = r.randint(10, 60)
        d = h / tn(a)
        q = "From the top of a cliff %d m high, the angle of depression of a boat is %d°. How far is the boat from the foot of the cliff, correct to 1 decimal place?" % (h, a)
        return T(q, "%s m" % d1(d), ["%s m" % d1(h * tn(a)), "%s m" % d1(h / tn(90 - a)), "%s m" % d1(h / sn(a))],
                 "The angle of depression equals the angle of elevation from the boat (alternate angles). tan %d° = %d ÷ <i>d</i>, so <i>d</i> = <b>%s m</b>." % (a, h, d1(d)))
    if kind == "car":
        h = r.randint(30, 200)
        d = r.randint(40, 300)
        a = math.degrees(math.atan(h / d))
        q = "From the top of a tower %d m high, a car is seen %d m from the foot of the tower. Find the angle of depression of the car, correct to 1 decimal place." % (h, d)
        return T(q, "%s°" % d1(a), ["%s°" % d1(90 - a), "%s°" % d1(math.degrees(math.atan(d / h))) if abs(math.degrees(math.atan(d / h)) - (90 - a)) > 0.05 else "%s°" % d1(a + 5), "%s°" % d1(a * 2)],
                 "The angle of depression is measured down from the horizontal. tan θ = %d ÷ %d, so θ = <b>%s°</b>." % (h, d, d1(a)))
    if kind == "angle":
        a = r.randint(15, 70)
        q = "From the top of a lighthouse, the angle of depression of a ship is %d°. What is the angle of elevation of the top of the lighthouse from the ship?" % a
        return T(q, "%d°" % a, ["%d°" % (90 - a), "%d°" % (180 - a), "%d°" % (2 * a) if 2 * a < 90 else "%d°" % (a + 10)],
                 "The horizontal line at the top and the ground are parallel, so the two angles are alternate angles: <b>%d°</b>." % a)
    h = r.randint(40, 120)
    a1, a2 = sorted(r.sample(range(15, 60), 2))
    d1_, d2_ = h / tn(a2), h / tn(a1)
    q = "From the top of a %d m cliff, the angles of depression of two buoys in a straight line with the foot of the cliff are %d° and %d°. How far apart are the buoys, correct to 1 decimal place?" % (h, a2, a1)
    return T(q, "%s m" % d1(d2_ - d1_), ["%s m" % d1(d2_ + d1_), "%s m" % d1(h / tn(a2 - a1)), "%s m" % d1(h * (tn(a2) - tn(a1)))],
             "Nearer buoy: %d ÷ tan %d° = %s m. Further buoy: %d ÷ tan %d° = %s m. Difference = <b>%s m</b>." % (h, a2, d1(d1_), h, a1, d1(d2_), d1(d2_ - d1_)))


# ------------------------------------------------------------ set 5: bearing problems
def one_prob(r):
    kind = r.choice(["north", "east", "right", "right", "cos"])
    nm, he, his = P.next()
    if kind in ("north", "east"):
        b = r.choice([v for v in range(20, 80, 5)])
        d = r.randint(5, 40)
        far = d * cs(b) if kind == "north" else d * sn(b)
        q = "A ship sails %d km on a bearing of %s. How far %s of its starting point is it, correct to 1 decimal place?" % (d, brg(b), kind)
        return T(q, "%s km" % d1(far), ["%s km" % d1(d * sn(b) if kind == "north" else d * cs(b)), "%s km" % d1(d * tn(b)), "%s km" % d1(d)],
                 "The bearing is the angle from north, so the distance %s is %d %s %d° = <b>%s km</b>." % (kind, d, "cos" if kind == "north" else "sin", b, d1(far)))
    if kind == "right":
        n, e = r.randint(3, 20), r.randint(3, 20)
        dist = math.hypot(n, e)
        ang = math.degrees(math.atan(e / n))
        q = "%s walks %d km due north and then %d km due east. Find the bearing of %s finishing point from the start, correct to 1 decimal place." % (nm, n, e, his)
        return T(q, "%s°" % ("%05.1f" % ang), ["%s°" % ("%05.1f" % (90 - ang)), "%s°" % ("%05.1f" % (ang + 180)), "%s°" % ("%05.1f" % (360 - ang))],
                 "tan θ = %d ÷ %d, so θ = %s°, measured clockwise from north. The bearing is <b>%s°</b> (the distance is %s km)." % (e, n, d1(ang), "%05.1f" % ang, d1(dist)))
    d1_, d2_ = r.randint(5, 25), r.randint(5, 25)
    b1 = r.choice(range(0, 90, 10))
    b2 = b1 + r.choice([60, 70, 80, 100, 110, 120])
    ang = 180 - (b2 - b1)
    dist = math.sqrt(d1_ ** 2 + d2_ ** 2 - 2 * d1_ * d2_ * cs(ang))
    q = "A boat sails %d km from A to B on a bearing of %s, then %d km from B to C on a bearing of %s. Find the distance AC, correct to 1 decimal place." % (d1_, brg(b1), d2_, brg(b2))
    return T(q, "%s km" % d1(dist), ["%s km" % d1(d1_ + d2_), "%s km" % d1(math.sqrt(d1_ ** 2 + d2_ ** 2)), "%s km" % d1(math.sqrt(d1_ ** 2 + d2_ ** 2 - 2 * d1_ * d2_ * cs(b2 - b1)))],
             "∠ABC = 180° − (%d° − %d°) = %d°. Cosine rule: AC² = %d² + %d² − 2(%d)(%d) cos %d°, so AC = <b>%s km</b>." % (b2, b1, ang, d1_, d2_, d1_, d2_, ang, d1(dist)))


def build():
    sets = [S("Reading bearings", collect(one_read, 20, R)),
            S("Back bearings and angles between bearings", collect(one_back, 20, R)),
            S("Angles of elevation", collect(one_elev, 20, R)),
            S("Angles of depression", collect(one_dep, 20, R)),
            S("Bearing problems", collect(one_prob, 20, R))]
    body = lesson(
        "<ul><li>A <b>bearing</b> is measured <b>clockwise from north</b> and written with three figures: 045°, 120°, 300°.</li>"
        "<li>The <b>back bearing</b> (A from B) differs by 180° from the bearing of B from A.</li>"
        "<li>The <b>angle of elevation</b> is measured up from the horizontal; the <b>angle of depression</b> is measured down from the horizontal. They are equal (alternate angles).</li>"
        "<li>Draw a right-angled triangle and use tan, sin or cos (SOH CAH TOA). Use the sine or cosine rule if the triangle is not right-angled.</li></ul>",
        [("The bearing of B from A is 070°. Find the bearing of A from B.", ["070° + 180°"], "250°"),
         ("From 30 m away, the angle of elevation of the top of a tree is 40°. Find its height.", ["tan 40° = h ÷ 30", "h = 30 tan 40°"], "25.2 m")],
        ["Measuring anticlockwise or from east instead of clockwise from north.",
         "Writing 45° instead of the three-figure bearing 045°.",
         "Adding 90° instead of 180° for a back bearing.",
         "Measuring the angle of depression from the vertical instead of the horizontal."])
    faq = [("What is a three-figure bearing?", "An angle measured clockwise from north, written with three digits, such as 045° or 230°."),
           ("How do you find a back bearing?", "Add 180° if the bearing is less than 180°, or subtract 180° if it is more."),
           ("What is the difference between angles of elevation and depression?", "Elevation is measured upwards from the horizontal to an object above; depression is measured downwards from the horizontal to an object below. From two points, they are equal."),
           ("Which trigonometric ratio should I use?", "Label the sides of the right-angled triangle as opposite, adjacent and hypotenuse from the angle, then choose SOH, CAH or TOA. Height and distance problems usually use tan.")]
    make(3, "bearings-and-angles-of-elevation", 13, "G4",
         "Bearings and Angles of Elevation and Depression",
         "", "Bearings and angles of elevation", "",
         "Free Secondary 3 maths worksheets on three-figure bearings, back bearings, angles of elevation and depression, and bearing problems with trigonometry. 100 questions with answers.",
         "Bearings are measured clockwise from north, with three figures.",
         "Angles of elevation and depression are measured from the horizontal; they are equal.",
         body, faq, sets, R)


if __name__ == "__main__":
    build()
