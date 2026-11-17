# -*- coding: utf-8 -*-
"""
UK Year 9 Maths: Bearings and Loci (KS3 Geometry and measures)
  python3 tools/gen_uk_maths_y9_bearings_and_loci.py
Reading three-figure bearings from diagrams, back bearings, compass directions as bearings, recognising loci
(circles, perpendicular bisectors, angle bisectors, parallel lines) and problems with scale.
Wrong answers come from real mistakes: measuring anticlockwise, missing the leading zero (45° instead of 045°),
measuring from the wrong point, and mixing up the perpendicular bisector and the angle bisector.
"""
import math
import random
from uk_ks3 import num, B, S, make, lesson, collect, T, svg_wrap, line, text, fig, INK, RED, BLUE, GREEN

R = random.Random(91101)


def brg(t):
    return "%03d°" % (t % 360)


def bearing_svg(theta, show, labA="A", labB="B"):
    """North line at A, line AB on bearing theta. show='cw' marks the clockwise angle theta from north,
    show='acw' marks the anticlockwise angle 360 - theta."""
    cx, cy, L, ar = 130, 130, 100, 34
    t = math.radians(theta)
    bx, by = cx + L * math.sin(t), cy - L * math.cos(t)
    s = [line(cx, cy, cx, cy - 112, INK, 2),
         "<path d='M%d %d l-6 12 l12 0 Z' fill='%s'/>" % (cx, cy - 118, INK),
         text(cx, cy - 122, "N", 14),
         line(cx, cy, bx, by, BLUE, 3),
         "<circle cx='%d' cy='%d' r='4' fill='%s'/>" % (cx, cy, INK),
         "<circle cx='%.1f' cy='%.1f' r='4' fill='%s'/>" % (bx, by, BLUE),
         ]
    oa = (theta + 180) % 360
    if oa < 40 or oa > 320:
        oa = 90 if theta > 180 else 270
    s.append(text(cx + 20 * math.sin(math.radians(oa)), cy - 20 * math.cos(math.radians(oa)) + 5, labA, 15))
    ox, oy = math.sin(t), -math.cos(t)
    s.append(text(bx + 14 * ox, by + 14 * oy + 5, labB, 15, col=BLUE))
    ex, ey = cx + ar * math.sin(t), cy - ar * math.cos(t)
    if show == "cw":
        big = 1 if theta > 180 else 0
        s.append("<path d='M%d %d A%d %d 0 %d 1 %.1f %.1f' fill='none' stroke='%s' stroke-width='2'/>" % (cx, cy - ar, ar, ar, big, ex, ey, RED))
        m = t / 2
        ang = theta
    else:
        big = 1 if (360 - theta) > 180 else 0
        s.append("<path d='M%d %d A%d %d 0 %d 0 %.1f %.1f' fill='none' stroke='%s' stroke-width='2'/>" % (cx, cy - ar, ar, ar, big, ex, ey, RED))
        m = -math.radians(360 - theta) / 2
        ang = 360 - theta
    s.append(text(cx + 54 * math.sin(m), cy - 54 * math.cos(m) + 5, "%d°" % ang, 14, col=RED))
    return svg_wrap(260, 260, "".join(s), "bearing diagram")


def pick(right, c):
    out = []
    for x in c:
        if x != right and x not in out:
            out.append(x)
    return out[:3]


# ------------------------------------------------------------ set 1: reading bearings
def one_read(r):
    theta = r.choice([r.randint(3, 17) * 5, r.randint(19, 35) * 5, r.randint(37, 53) * 5, r.randint(55, 70) * 5])
    if theta % 90 == 0:
        return None
    show = "cw" if theta <= 180 or r.random() < 0.4 else "acw"
    q = fig(bearing_svg(theta, show)) + "What is the bearing of B from A?"
    right = brg(theta)
    wr = [brg(360 - theta), "%d°" % theta if theta < 100 else brg(theta + 180), brg(theta + 180), brg(360 - theta + 180) if show == "acw" else brg(theta + 10)]
    if show == "cw":
        e = "Measure clockwise from north at A: <b>%s</b>. Bearings always have three figures." % right
    else:
        e = "The marked angle is anticlockwise. The bearing is 360° − %d° = <b>%s</b>." % (360 - theta, right)
    return T(q, right, pick(right, wr), e)


# ------------------------------------------------------------ set 2: back bearings
def one_back(r):
    theta = r.randint(1, 71) * 5
    if theta % 90 == 0:
        return None
    pl = r.choice([("A", "B"), ("P", "Q"), ("the ship", "the lighthouse"), ("the school", "the park"), ("Leeds", "York")])
    a, b = pl
    q = "The bearing of %s from %s is %s. What is the bearing of %s from %s?" % (b, a, brg(theta), a, b)
    right = brg(theta + 180)
    wr = [brg(360 - theta), brg(theta), brg(theta + 90), brg(180 - theta)]
    e = "Back bearings differ by 180°. %s %s 180° = <b>%s</b>." % (brg(theta), "+" if theta < 180 else "−", right)
    return T(q.replace("of the", "of the").capitalize() if q[0].islower() else q, right, pick(right, wr), e)


# ------------------------------------------------------------ set 3: compass directions
DIRS = [("north", 0), ("north-east", 45), ("east", 90), ("south-east", 135), ("south", 180), ("south-west", 225), ("west", 270), ("north-west", 315)]


def one_compass(r):
    k = r.randint(0, 2)
    if k == 0:
        nm, t = r.choice(DIRS)
        q = "What is the three-figure bearing for the direction %s?" % nm
        right = brg(t)
        wr = [brg(360 - t), brg(t + 180), "%d°" % t if t < 100 else brg(t + 90), brg(t + 45)]
        return T(q, right, pick(right, wr), "Measure clockwise from north. %s is <b>%s</b>." % (nm.capitalize(), right))
    if k == 1:
        (n1, t1), (n2, t2) = r.sample(DIRS, 2)
        d = (t2 - t1) % 360
        q = "A walker faces %s and turns clockwise to face %s. How many degrees does she turn?" % (n1, n2)
        right = "%d°" % d
        wr = ["%d°" % (360 - d), "%d°" % ((d + 90) % 360 or 360), "%d°" % abs(t2 - t1) if abs(t2 - t1) != d else "%d°" % (d + 45)]
        return T(q, right, pick(right, wr), "%s is %s and %s is %s. Clockwise: <b>%s</b>." % (n1.capitalize(), brg(t1), n2, brg(t2), right))
    t = r.randint(1, 71) * 5
    if t % 45 == 0:
        return None
    opts = ["between north and east", "between east and south", "between south and west", "between west and north"]
    right = opts[t // 90]
    q = "A plane flies on a bearing of %s. In which direction is it flying?" % brg(t)
    wr = [opts[(t // 90 + 1) % 4], opts[(t // 90 + 3) % 4], opts[(t // 90 + 2) % 4]]
    return T(q, "It is " + right, ["It is " + w for w in wr], "%s is between %s and %s, so it is <b>%s</b>." % (brg(t), brg(t // 90 * 90), brg(t // 90 * 90 + 90) if t // 90 < 3 else "360°", right))


# ------------------------------------------------------------ set 4: loci
LOCI = [
    ("The locus of points exactly 3 cm from a point P is…", "a circle with centre P and radius 3 cm",
     ["a straight line 3 cm long", "a square with sides 3 cm", "two lines 3 cm apart"],
     "Every point 3 cm from P lies on <b>a circle with centre P and radius 3 cm</b>."),
    ("The locus of points less than 3 cm from a point P is…", "the region inside a circle of radius 3 cm, centre P",
     ["the region outside a circle of radius 3 cm", "a circle of radius 3 cm only", "a line 3 cm from P"],
     "Less than 3 cm means inside the circle: <b>the region inside a circle of radius 3 cm, centre P</b>."),
    ("The locus of points equidistant from two points A and B is…", "the perpendicular bisector of AB",
     ["the angle bisector at A", "a circle through A and B", "the line AB"],
     "Points the same distance from A and B lie on <b>the perpendicular bisector of AB</b>."),
    ("The locus of points equidistant from two lines that meet at a point is…", "the angle bisector",
     ["the perpendicular bisector", "a circle", "a line parallel to one of the lines"],
     "Points the same distance from two crossing lines lie on <b>the angle bisector</b>."),
    ("The locus of points exactly 2 cm from a straight line (going on forever) is…", "two parallel lines, 2 cm either side",
     ["one parallel line 2 cm above", "a circle of radius 2 cm", "a perpendicular line"],
     "On each side of the line there is a parallel line 2 cm away: <b>two parallel lines, 2 cm either side</b>."),
    ("The locus of points exactly 2 cm from a line segment AB is…", "two parallel lines joined by semicircles at A and B",
     ["two parallel lines only", "a circle of radius 2 cm", "a rectangle"],
     "Beside the segment the points form parallel lines; around each end they form semicircles. The shape is like a running track."),
    ("A goat is tied to a post with a 5 m rope. Which shape shows where it can graze?", "a circle of radius 5 m, including the inside",
     ["a square of side 5 m", "a semicircle of radius 5 m", "a line 5 m long"],
     "It can reach any point up to 5 m from the post: <b>a circle of radius 5 m, including the inside</b>."),
    ("A goat is tied to a 4 m rope that can slide along a 10 m rail. Which shape shows where it can graze?", "a rectangle with a semicircle at each end",
     ["a circle of radius 4 m", "a circle of radius 10 m", "a 10 m by 4 m rectangle only"],
     "Points within 4 m of a segment: <b>a rectangle with a semicircle at each end</b>."),
    ("Which construction gives points the same distance from towns A and B?", "the perpendicular bisector of AB",
     ["the angle bisector at A", "a circle centre A", "a line through B parallel to AB"],
     "Equidistant from two points means <b>the perpendicular bisector of AB</b>."),
    ("Which construction gives points the same distance from two walls of a room that meet at a corner?", "the angle bisector of the corner",
     ["the perpendicular bisector of the walls", "a circle centred on the corner", "a line parallel to one wall"],
     "Equidistant from two lines means <b>the angle bisector of the corner</b>."),
    ("Points closer to A than to B lie…", "on A's side of the perpendicular bisector of AB",
     ["on B's side of the perpendicular bisector of AB", "on the perpendicular bisector", "inside a circle centred B"],
     "The perpendicular bisector divides the plane. Points closer to A are <b>on A's side of the perpendicular bisector</b>."),
    ("A phone mast reaches 20 km. Which shape shows the area it covers?", "a circle of radius 20 km, including the inside",
     ["a circle of radius 10 km", "a square of side 20 km", "a line 20 km long"],
     "Every point within 20 km: <b>a circle of radius 20 km, including the inside</b>."),
    ("To draw a perpendicular bisector of AB with compasses, the compass width must be…", "more than half of AB",
     ["exactly AB", "less than half of AB", "any width at all"],
     "The arcs from A and B must cross, so the width must be <b>more than half of AB</b>."),
    ("Which is equidistant from both sides of angle ABC?", "a point on the bisector of angle ABC",
     ["a point on the line AC", "the midpoint of AB", "a point on the perpendicular bisector of AB"],
     "Points on the angle bisector are the same distance from BA and BC: <b>a point on the bisector of angle ABC</b>."),
    ("Treasure is buried 3 m from tree T and the same distance from posts P and Q. Where should you dig?", "where the circle round T meets the perpendicular bisector of PQ",
     ["at the midpoint of PQ", "3 m from P", "on the angle bisector at T"],
     "Use both loci: the circle of radius 3 m round T and the perpendicular bisector of PQ. Dig <b>where they meet</b>."),
    ("The locus of points exactly 5 cm from the centre of a circle of radius 5 cm is…", "the circle itself",
     ["the centre only", "a circle of radius 10 cm", "a diameter"],
     "Every point of the circle is 5 cm from its centre, so the locus is <b>the circle itself</b>."),
    ("Points more than 2 m from a wall and less than 6 m from a lamp are shown by…", "the overlap of two regions",
     ["a single line", "one point only", "a circle only"],
     "Each condition gives a region. The answer is <b>the overlap of two regions</b>."),
    ("Which tools do you need to construct an angle bisector?", "compasses and a ruler",
     ["a protractor only", "a calculator", "a set square only"],
     "Constructions use <b>compasses and a ruler</b>, not a protractor."),
    ("The locus of the tip of a clock's hour hand over 12 hours is…", "a circle", ["a straight line", "a square", "a spiral"],
     "The tip stays the same distance from the centre: <b>a circle</b>."),
    ("Points equidistant from the lines <i>y</i> = 2 and <i>y</i> = 8 lie on…", "the line <i>y</i> = 5",
     ["the line <i>x</i> = 5", "the line <i>y</i> = 10", "the line <i>y</i> = 6"],
     "Halfway between two parallel lines: (2 + 8) ÷ 2 = 5, so <b>the line <i>y</i> = 5</b>."),
]


def loci():
    up = lambda x: x[0].upper() + x[1:]
    return [T(q, up(a), [up(w) for w in ws], e) for q, a, ws, e in LOCI]


# ------------------------------------------------------------ set 5: problems
def problems():
    data = [
        ("A ship sails 5 km on a bearing of 090°, then 5 km on a bearing of 180°. What is its bearing from the start?", "135°", ["045°", "225°", "315°"],
         "It has gone 5 km east and 5 km south, so it is south-east of the start: <b>135°</b>."),
        ("From the start, the ship is south-east. What is the bearing of the start from the ship?", "315°", ["135°", "045°", "225°"],
         "Back bearing: 135° + 180° = <b>315°</b>."),
        ("On a map, 1 cm represents 2 km. A boat is 7.5 cm from a port. How far is that in real life?", "15 km", ["3.75 km", "9.5 km", "150 km"],
         "7.5 × 2 = <b>15 km</b>."),
        ("A scale is 1 : 50,000. Two villages are 6 cm apart on the map. How far apart are they?", "3 km", ["300 m", "30 km", "50 km"],
         "6 × 50,000 = 300,000 cm = 3,000 m = <b>3 km</b>."),
        ("The bearing of B from A is 070°. The bearing of C from A is 160°. What is angle BAC?", "90°", ["230°", "70°", "160°"],
         "160° − 70° = <b>90°</b>."),
        ("Which of these is not a correctly written bearing?", "45°", ["045°", "300°", "180°"],
         "Bearings have three figures, so 45° should be written 045°. <b>45°</b> is not correct."),
        ("A hiker walks on a bearing of 200°. Which direction is closest?", "south-south-west", ["north-north-east", "south-east", "west"],
         "200° is just past south (180°), towards west: <b>south-south-west</b>."),
        ("A plane flies due west and then turns to fly due north. Through how many degrees has it turned clockwise?", "90°", ["270°", "180°", "360°"],
         "West is 270° and north is 360°: it turns <b>90°</b> clockwise."),
        ("The bearing of X from Y is 310°. What is the bearing of Y from X?", "130°", ["050°", "490°", "230°"],
         "310° − 180° = <b>130°</b>. Subtract 180° when the bearing is more than 180°."),
        ("A lighthouse L is due north of a port P. A ship S is due east of L. What is the bearing of S from P?", "Between 000° and 090°", ["Between 090° and 180°", "Exactly 180°", "Between 270° and 360°"],
         "S is north and east of P, so the bearing is <b>between 000° and 090°</b>."),
        ("A boat is 8 km from a port on a bearing of 090°. A buoy is 6 km from the port on a bearing of 000°. How far is the boat from the buoy?", "10 km", ["14 km", "2 km", "48 km"],
         "The bearings are 90° apart, so use Pythagoras: √(8² + 6²) = <b>10 km</b>."),
        ("A sprinkler waters up to 3 m away. It is placed in the middle of a 4 m by 4 m lawn. Does it water the whole lawn?", "Yes, the corners are less than 3 m away", ["No, the corners are 4 m away", "No, the edges are 3 m away", "Yes, because 3 is less than 4"],
         "The corners are √(2² + 2²) ≈ 2.83 m from the middle. <b>Yes, the corners are less than 3 m away.</b>"),
        ("A dog is tied to the corner of a shed (outside) with a 3 m rope. The shed walls meet at 90°. What fraction of a circle can it reach?", "<span class='fr'><span class='fn'>3</span><span class='fd'>4</span></span>", ["<span class='fr'><span class='fn'>1</span><span class='fd'>4</span></span>", "<span class='fr'><span class='fn'>1</span><span class='fd'>2</span></span>", "The whole circle"],
         "The shed blocks a 90° corner, so it reaches 270° of the circle: <b>¾</b>."),
        ("What is the bearing of south-west?", "225°", ["135°", "315°", "045°"], "South-west is halfway between south (180°) and west (270°): <b>225°</b>."),
        ("Two ships leave port. One sails on 040°, the other on 130°. What is the angle between their paths?", "90°", ["170°", "40°", "130°"],
         "130° − 40° = <b>90°</b>."),
        ("Ava measures the bearing of B from A anticlockwise and gets 60°. What is the correct bearing?", "300°", ["060°", "240°", "120°"],
         "Bearings are measured clockwise: 360° − 60° = <b>300°</b>."),
        ("A ship is 12 km due south of a port. What is the bearing of the port from the ship?", "000°", ["180°", "090°", "360° and 180°"],
         "The port is due north of the ship: <b>000°</b>."),
        ("Where do the perpendicular bisectors of the sides of a triangle meet?", "At a point the same distance from all three corners", ["At the midpoint of the longest side", "At a corner", "They never meet"],
         "Each bisector is equidistant from two corners, so where they meet is <b>the same distance from all three corners</b>."),
        ("A radio mast covers 30 km. Town T is 25 km away on a bearing of 050°. Can people in T hear it?", "Yes, 25 km is within 30 km", ["No, the bearing is wrong", "No, 25 km is outside the range", "Only if the bearing is 000°"],
         "The range is a circle of radius 30 km in every direction. <b>Yes, 25 km is within 30 km.</b>"),
        ("On a 1 : 25,000 map, how many centimetres show 1 km?", "4 cm", ["25 cm", "2.5 cm", "0.4 cm"],
         "1 km = 100,000 cm. 100,000 ÷ 25,000 = <b>4 cm</b>."),
    ]
    return [T(q, a, w, e) for q, a, w, e in data]


def body():
    return lesson(
        "<p>A <b>bearing</b> is an angle measured <b>clockwise from north</b>, written with <b>three figures</b>: 045°, 120°, 300°. "
        "The bearing of B from A is measured at A. The <b>back bearing</b> (A from B) is 180° more or less.</p>"
        "<p>A <b>locus</b> is the set of points that follow a rule. Fixed distance from a point: a <b>circle</b>. "
        "Equidistant from two points: the <b>perpendicular bisector</b>. Equidistant from two lines: the <b>angle bisector</b>.</p>",
        [("The bearing of B from A is 065°. Find the bearing of A from B.", ["065° + 180°."], "245°"),
         ("The anticlockwise angle from north to AB is 110°.", ["360° − 110°."], "250°"),
         ("Where are points 4 cm from P?", ["Same distance from one point."], "A circle, radius 4 cm")],
        ["Measuring anticlockwise or from the wrong point.",
         "Writing 45° instead of 045°.",
         "Getting a back bearing over 360°. If the bearing is more than 180°, subtract 180°.",
         "Using the perpendicular bisector when the rule is about two lines (use the angle bisector)."])


def main():
    sets = [S("Reading bearings", collect(one_read, 20, R)),
            S("Back bearings", collect(one_back, 20, R)),
            S("Compass directions and bearings", collect(one_compass, 20, R)),
            S("Loci", loci()),
            S("Bearings and loci problems", problems())]
    make(9, "bearings-and-loci", 11, "G",
         "Bearings and Loci",
         "Year 9 Bearings and Loci Worksheets: Three-Figure Bearings, Back Bearings and Constructions",
         "Bearings and Loci",
         "Use the standard conventions for labelling and referring to the sides and angles of triangles; draw diagrams from "
         "written description; use standard ruler and compass constructions (perpendicular bisector, angle bisector) and "
         "understand loci; interpret bearings.",
         "Free Year 9 bearings and loci worksheets: read three-figure bearings, back bearings, compass directions, loci "
         "(circles, perpendicular and angle bisectors) and map problems. 100 questions with answers.",
         "Bearings: clockwise from north, three figures.",
         "Back bearing: add or subtract 180°.",
         body(),
         [("What is a bearing?", "An angle measured clockwise from north, written with three figures, such as 045° or 230°."),
          ("How do I find a back bearing?", "Add 180° if the bearing is less than 180°; subtract 180° if it is more."),
          ("What is a locus?", "The set of all points that follow a rule, such as 'exactly 3 cm from P', which is a circle."),
          ("When do I use a perpendicular bisector or an angle bisector?", "Perpendicular bisector: equidistant from two points. Angle bisector: equidistant from two lines.")],
         sets, R)


if __name__ == "__main__":
    main()
