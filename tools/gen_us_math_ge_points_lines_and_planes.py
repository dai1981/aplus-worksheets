# -*- coding: utf-8 -*-
"""
US Geometry: Points, Lines, and Planes (Common Core G-CO.A.1)
  python3 tools/gen_us_math_ge_points_lines_and_planes.py
Naming lines, rays and segments; collinear and coplanar points; counting lines, segments and rays;
precise definitions; parallel, intersecting and skew edges of a box.
Wrong answers come from real mistakes: mixing up a ray and a line, reversing the endpoint of a ray,
calling any three points collinear, and confusing skew lines with parallel lines.
"""
import random
from itertools import combinations
from us_hs import B, S, make, lesson, collect, T, fig, num
from us_geo import Canvas, RED

R = random.Random(92101)
LETTERS = ["ABCD", "PQRS", "JKLM", "WXYZ", "EFGH", "RSTU", "MNOP", "DEFG", "GHJK", "TUVW"]


def ov(s):
    return "<span class='ov'>%s</span>" % s


def line_fig(kind, a, b, extra=None):
    c = Canvas()
    A, Bp = (40, 60), (200, 60)
    if kind == "line":
        c.fullline(A, Bp, 50)
    elif kind == "ray":
        c.ray(A, Bp, 60)
    elif kind == "rayb":
        c.ray(Bp, A, 60)
    else:
        c.seg(A, Bp)
    for p, n in ((A, a), (Bp, b)):
        c.dot(p)
        c.text((p[0], p[1] - 20), n, 16)
    if extra:
        c.dot((120, 60))
        c.text((120, 40), extra, 16)
    return c.svg("a figure with points %s and %s" % (a, b))


# ------------------------------------------------------------ set 1: naming
def one_name(r):
    a, b, m = r.sample(r.choice(LETTERS), 3)
    kind = r.choice(["line", "ray", "rayb", "seg", "line3", "ray3"])
    if kind in ("line3", "ray3"):
        svg = line_fig("line" if kind == "line3" else "ray", a, b, m)
        if kind == "line3":
            right = "line %s%s" % (m, b)
            q = "Which is another name for line %s%s?%s" % (a, b, fig(svg))
            wr = ["ray %s%s" % (m, b), "segment %s%s" % (a, m), "line %s" % m]
            e = "Any two points on a line name it. %s and %s are both on the line, so <b>%s</b> is the same line." % (m, b, right)
        else:
            right = "ray %s%s" % (a, m)
            q = "The ray starts at %s and goes through %s and %s. Which is another name for it?%s" % (a, m, b, fig(svg))
            wr = ["ray %s%s" % (m, a), "ray %s%s" % (b, a), "line %s" % m]
            e = "A ray is named by its endpoint first, then any other point on it. The endpoint is %s, so <b>%s</b> is the same ray." % (a, right)
        return T(q, right, wr, e)
    svg = line_fig(kind, a, b)
    names = {"line": "line %s%s" % (a, b), "ray": "ray %s%s" % (a, b), "rayb": "ray %s%s" % (b, a), "seg": "segment %s%s" % (a, b)}
    right = names[kind]
    wr = [v for k, v in names.items() if k != kind]
    e = {"line": "Arrows on both ends: it goes on forever both ways. It is <b>%s</b>." % right,
         "ray": "It has one endpoint, %s, and goes on forever through %s. A ray is named endpoint first: <b>%s</b>." % (a, b, right),
         "rayb": "It has one endpoint, %s, and goes on forever through %s. A ray is named endpoint first: <b>%s</b>." % (b, a, right),
         "seg": "It has two endpoints and no arrows. It is <b>%s</b>, written %s." % (right, ov(a + b))}[kind]
    return T("What is the name of this figure?%s" % fig(svg), right, wr, e)


# ------------------------------------------------------------ set 2: collinear and coplanar
def pts_fig(on, off, ln="ℓ"):
    c = Canvas()
    c.fullline((30, 110), (290, 50), 20)
    c.text((300, 30), ln, 17, italic=True)
    xs = [60, 140, 220]
    for x, n in zip(xs, on):
        y = 110 - (x - 30) * 60 / 260
        c.dot((x, y))
        c.text((x, y + 20), n, 16)
    for (x, y), n in zip([(100, 30), (230, 130)], off):
        c.dot((x, y))
        c.text((x + 14, y - 10), n, 16)
    return c.svg("points on and off a line")


def one_col(r):
    L = list(r.choice(["ABCDE", "PQRST", "JKLMN", "UVWXY", "FGHJK"]))
    r.shuffle(L)
    on, off = L[:3], L[3:5]
    svg = pts_fig(on, off)
    kind = r.choice(["col", "non", "col2", "how"])
    if kind == "col":
        q = "Which three points are collinear?%s" % fig(svg)
        right = ", ".join(sorted(on))
        wr = [", ".join(sorted(on[:2] + [off[0]])), ", ".join(sorted([on[0]] + off)), ", ".join(sorted(on[1:] + [off[1]]))]
        e = "Collinear points lie on the same line. %s are all on line ℓ: <b>%s</b>." % (right, right)
    elif kind == "non":
        q = "Which three points are <b>noncollinear</b>?%s" % fig(svg)
        right = ", ".join(sorted(on[:2] + [off[r.randint(0, 1)]]))
        wr = [", ".join(sorted(on)), "None. Any three points are collinear.", "All of them must be on line ℓ."]
        e = "Noncollinear means they are not all on one line. Two of these are on ℓ and one is off it: <b>%s</b>." % right
    elif kind == "col2":
        p = r.choice(off)
        q = "Is point %s on line ℓ?%s" % (p, fig(svg))
        right = "No. %s is not on line ℓ." % p
        wr = ["Yes. Every point is on line ℓ.", "Yes, because it is near the line.", "Only if %s is between %s and %s." % (p, on[0], on[2])]
        e = "A point is on the line only if the line passes through it. <b>%s</b>" % right
        return T(q, right, wr, e)
    else:
        q = "Through points %s and %s, how many lines can be drawn?%s" % (on[0], off[0], fig(svg))
        right = "Exactly one"
        wr = ["None", "Exactly two", "Infinitely many"]
        e = "Through any two points there is exactly one line. <b>Exactly one</b>."
    return T(q, right, wr, e)


# ------------------------------------------------------------ set 3: counting and postulates
FACTS = [
    ("Two different lines intersect. What is their intersection?", "A point", ["A line", "A plane", "Two points"],
     "Two different lines can cross at only one place, so they meet in <b>a point</b>."),
    ("Two different planes intersect. What is their intersection?", "A line", ["A point", "A plane", "A segment"],
     "Two planes that cross meet in <b>a line</b>, like two walls meeting at a corner."),
    ("How many planes contain three noncollinear points?", "Exactly one", ["None", "Exactly three", "Infinitely many"],
     "Three points that are not on one line determine <b>exactly one</b> plane."),
    ("How many planes contain three collinear points?", "Infinitely many", ["Exactly one", "None", "Exactly three"],
     "Points on one line are like the spine of a book: <b>infinitely many</b> planes (pages) contain them."),
    ("A line and a plane intersect, and the line is not in the plane. What is their intersection?", "A point", ["A line", "A plane", "A ray"],
     "A line that pierces a plane meets it in <b>a point</b>."),
    ("If two points are in a plane, where is the line through them?", "The whole line is in the plane", ["Only the two points are in the plane",
     "The line is outside the plane", "Only the segment between them is in the plane"],
     "If two points lie in a plane, <b>the whole line through them lies in the plane</b>."),
]


def one_count(r):
    kind = r.choice(["lines", "segs", "rays", "fact"])
    if kind == "fact":
        q, right, wr, e = r.choice(FACTS)
        return T(q, right, wr, e)
    n = r.randint(3, 10)
    if kind == "lines":
        q = "There are %d points in a plane, and no three of them are collinear. How many lines can you draw through pairs of these points?" % n
        ans = n * (n - 1) // 2
        wr = [n * (n - 1), n, n - 1]
        e = "Each pair of points makes one line. The number of pairs is %d × %d ÷ 2 = <b>%d</b>. Do not count line AB and line BA twice." % (n, n - 1, ans)
    elif kind == "segs":
        q = "%d points are marked on a line. How many segments have two of these points as endpoints?" % n
        ans = n * (n - 1) // 2
        wr = [n - 1, n * (n - 1), n]
        e = "Each pair of points is the endpoints of one segment: %d × %d ÷ 2 = <b>%d</b>. Short segments and long ones both count." % (n, n - 1, ans)
    else:
        q = "%d points are marked on a line. How many different rays start at one of these points and go through another one of them?" % n
        ans = 2 * (n - 1)
        wr = [n * (n - 1) // 2, n - 1, n * (n - 1)]
        e = ("Rays that start at the same point and go the same way are the same ray. So each point gives one ray to the right "
             "(except the last) and one to the left (except the first): 2 × %d = <b>%d</b>." % (n - 1, ans))
    wr = [w for w in wr if w != ans]
    wr += [ans + 1, ans - 1, ans + 2]
    return T(q, num(ans), [num(w) for w in dict.fromkeys(wr) if w != ans][:3], e)


# ------------------------------------------------------------ set 4: definitions
DEFS = [
    ("line segment", "part of a line with two endpoints"),
    ("ray", "part of a line with one endpoint that goes on forever in one direction"),
    ("angle", "two rays with the same endpoint"),
    ("circle", "all points in a plane at a given distance from a center point"),
    ("parallel lines", "lines in the same plane that never intersect"),
    ("perpendicular lines", "lines that intersect to form right angles"),
    ("skew lines", "lines that are not in the same plane and never intersect"),
    ("midpoint", "the point that divides a segment into two congruent segments"),
    ("congruent segments", "segments that have the same length"),
    ("opposite rays", "two rays with the same endpoint that form a line"),
    ("vertex of an angle", "the common endpoint of the two rays of an angle"),
]


def one_def(r):
    term, d = r.choice(DEFS)
    others = [x for x in DEFS if x[0] != term]
    r.shuffle(others)
    if r.random() < 0.5:
        q = "Which is the definition of %s?" % B(term)
        return T(q, cap1(d), [cap1(x[1]) for x in others[:3]], "%s: %s. <b>%s</b>." % (cap1(term), d, cap1(d)))
    q = "What is the name for %s?" % B(d)
    return T(q, cap1(term), [cap1(x[0]) for x in others[:3]], "%s: <b>%s</b>." % (cap1(d), term))


def cap1(s):
    return s[0].upper() + s[1:]


# ------------------------------------------------------------ set 5: a box
V = {"A": (40, 200), "B": (200, 200), "C": (260, 160), "D": (100, 160),
     "E": (40, 80), "F": (200, 80), "G": (260, 40), "H": (100, 40)}
EDGES = ["AB", "BC", "CD", "DA", "EF", "FG", "GH", "HE", "AE", "BF", "CG", "DH"]
DIRS = {"x": ["AB", "DC", "EF", "HG"], "y": ["BC", "AD", "FG", "EH"], "z": ["AE", "BF", "CG", "DH"]}
FACES = ["ABCD", "EFGH", "ABFE", "DCGH", "BCGF", "ADHE"]


def box_svg():
    c = Canvas()
    hidden = {"CD", "DA", "DH"}
    for e in EDGES:
        c.seg(V[e[0]], V[e[1]], dash=e in hidden, w=2.2)
    for k, p in V.items():
        dx = -14 if k in "AEDH" else 14
        dy = 14 if k in "AB" else (12 if k == "F" else -10)
        c.text((p[0] + dx, p[1] + dy), k, 15)
    return c.svg("a rectangular box with vertices A to H; dashed edges are hidden", big=True)


def dir_of(e):
    for k, es in DIRS.items():
        if e in es or e[::-1] in es:
            return k


def norm(e):
    return e if e in EDGES else e[::-1]


def one_box(r):
    svg = fig(box_svg())
    kind = r.choice(["par", "skew", "int", "faces", "planes", "word"])
    e0 = r.choice(EDGES)
    d0 = dir_of(e0)
    par = [norm(x) for x in DIRS[d0] if norm(x) != e0]
    inter = [x for x in EDGES if x != e0 and set(x) & set(e0)]
    skew = [x for x in EDGES if x != e0 and x not in par and x not in inter]
    if kind == "par":
        right = r.choice(par)
        q = "Which edge is parallel to %s?%s" % (ov(e0), svg)
        e = "Parallel edges point the same way and never meet. %s and %s are in the same face and never meet: <b>%s</b>." % (ov(e0), ov(right), ov(right))
        wr = r.sample(skew, 2) + r.sample(inter, 1)
    elif kind == "skew":
        right = r.choice(skew)
        q = "Which edge is skew to %s?%s" % (ov(e0), svg)
        e = "Skew lines never meet and are not parallel, so no flat surface holds both. <b>%s</b> is skew to %s." % (ov(right), ov(e0))
        wr = r.sample(par, 2) + r.sample(inter, 1)
    elif kind == "int":
        right = r.choice(inter)
        q = "Which edge intersects %s and is perpendicular to it?%s" % (ov(e0), svg)
        e = "The edges that share an endpoint with %s meet it at a right angle in a box: <b>%s</b>." % (ov(e0), ov(right))
        wr = r.sample(par, 1) + r.sample(skew, 2)
    elif kind == "faces":
        f1, f2 = r.choice([(a, b) for a, b in combinations(FACES, 2) if len(set(a) & set(b)) == 2])
        common = "".join(x for x in f1 if x in f2)
        right = "line " + norm(common)
        q = "Plane %s and plane %s intersect. What is their intersection?%s" % (f1, f2, svg)
        other = [x for x in EDGES if x != norm(common)]
        r.shuffle(other)
        e = "Two planes meet in a line. The points in both planes are %s and %s, so they meet in <b>%s</b>." % (common[0], common[1], right)
        return T(q, right, ["line " + x for x in other[:2]] + ["point " + common[0]], e)
    elif kind == "planes":
        f = r.choice(FACES)
        opp = {"ABCD": "EFGH", "EFGH": "ABCD", "ABFE": "DCGH", "DCGH": "ABFE", "BCGF": "ADHE", "ADHE": "BCGF"}[f]
        right = "plane " + opp
        q = "Which plane is parallel to plane %s?%s" % (f, svg)
        others = [x for x in FACES if x not in (f, opp)]
        r.shuffle(others)
        e = "Opposite faces of a box never meet: <b>%s</b>. The other faces share an edge with plane %s." % (right, f)
        return T(q, right, ["plane " + x for x in others[:3]], e)
    else:
        items = [("A hallway's floor and ceiling", "Parallel planes", ["Intersecting planes", "Skew lines", "Perpendicular lines"],
                  "The floor and ceiling never meet, like the top and bottom of a box: <b>parallel planes</b>."),
                 ("Two walls of a room that meet at a corner", "Intersecting planes", ["Parallel planes", "Skew lines", "Parallel lines"],
                  "Two walls meet along a vertical line: <b>intersecting planes</b>."),
                 ("A road on a bridge and a road below it that goes in a different direction", "Skew lines", ["Parallel lines", "Intersecting lines", "Perpendicular lines"],
                  "They never meet and do not go the same way, and they are at different heights: <b>skew lines</b>."),
                 ("The two rails of a straight train track", "Parallel lines", ["Skew lines", "Intersecting lines", "Perpendicular lines"],
                  "The rails are in the same plane and never meet: <b>parallel lines</b>."),
                 ("The edge where a wall meets the floor, and the edge where that wall meets the next wall", "Perpendicular lines",
                  ["Parallel lines", "Skew lines", "Parallel planes"], "They meet at a corner at a right angle: <b>perpendicular lines</b>.")]
        a, right, wr, e = r.choice(items)
        return T("Which best describes this pair? %s." % B(a), right, wr, e)
    return T(q, ov(right), [ov(w) for w in wr], e)


def build():
    sets = [S("Name lines, rays and segments", collect(one_name, 20, R)),
            S("Collinear points", collect(one_col, 20, R)),
            S("Counting and postulates", collect(one_count, 20, R)),
            S("Precise definitions", collect(one_def, 20, R)),
            S("Parallel, intersecting and skew", collect(one_box, 20, R))]
    body = lesson(
        "<p>Geometry starts with three words we do not define: <b>point</b> (a location), <b>line</b> (straight, goes on forever both ways) "
        "and <b>plane</b> (a flat surface that goes on forever). Everything else is defined from them.</p>"
        "<ul><li><b>Segment %s</b>: two endpoints.</li><li><b>Ray AB</b>: starts at A and goes on through B forever. Name the endpoint first.</li>"
        "<li><b>Line AB</b>: any two points on it name it.</li></ul>"
        "<p><b>Collinear</b> points are on one line. <b>Coplanar</b> points are in one plane. Two lines meet in a point; two planes meet in a line.</p>"
        "<p><b>Parallel lines</b> are in one plane and never meet. <b>Skew lines</b> never meet and are not in one plane.</p>" % ov("AB"),
        [("Points A, B, C, D are on a line in that order. Is ray BC the same as ray BD?",
          ["Both rays start at B and go the same way, through C and on to D."], "Yes, they are the same ray."),
         ("In a box, edge AB is on the bottom front and edge CG is a back vertical edge. How are they related?",
          ["They never meet.", "They point in different directions, so they are not parallel."], "They are skew.")],
        ["Naming a ray with the endpoint second. Ray BA starts at B, not A.",
         "Thinking any three points are collinear. Two points are always collinear, but a third may be off the line.",
         "Calling skew lines parallel. Parallel lines must be in the same plane.",
         "Counting line AB and line BA as two lines. They are the same line."])
    faq = [("What is the difference between a line, a ray and a segment?",
            "A line goes on forever in both directions. A ray has one endpoint and goes on forever in one direction. A segment has two endpoints."),
           ("What are undefined terms in geometry?",
            "Point, line and plane. They are described, not defined, and every other term is defined using them."),
           ("What are skew lines?", "Lines that never intersect and are not in the same plane. They can only happen in three dimensions."),
           ("How many points determine a line and a plane?",
            "Two points determine exactly one line. Three noncollinear points determine exactly one plane.")]
    make("points-lines-and-planes", 1, "G-CO.A.1",
         "Points, Lines, and Planes",
         "Points, Lines, and Planes Worksheet (Geometry, G-CO.A.1) | 100 Questions with Answers",
         "Points, Lines, and Planes",
         "Know precise definitions of angle, circle, perpendicular line, parallel line, and line segment, based on the undefined notions of point, line, distance along a line, and distance around a circular arc.",
         "Free Geometry worksheet on points, lines and planes: name rays and segments, collinear points, postulates, definitions and skew lines. 100 questions with answers.",
         "A ray is named endpoint first. Two lines meet in a point; two planes meet in a line.",
         "Collinear means on one line. Skew lines never meet and are not in one plane.",
         body, faq, sets, R, domain="Foundations of Geometry", grade="geometry")


if __name__ == "__main__":
    build()
