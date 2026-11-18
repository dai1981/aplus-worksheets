# -*- coding: utf-8 -*-
"""
SG Secondary 4 Maths: Problems in Three Dimensions (MOE syllabus G4: problems in two and three dimensions
including angles of elevation and depression and bearings)
  python3 tools/gen_sg_maths_s4_problems_in_three_dimensions.py
Face and space diagonals of cuboids, the angle between a line and a plane, right pyramids (height, slant edge,
angles), angles of elevation in 3D, and problems combining bearings and elevation.
Answers are correct to 3 significant figures or 1 decimal place for angles, as in O-Level papers.
Wrong answers come from real mistakes: using a face diagonal as the space diagonal, choosing the wrong
right angle, using the full base diagonal instead of half of it, and measuring an angle from the vertical.
"""
import math
import random
from sg_sec import num, S, make, lesson, collect, T, fig, MINUS, People
from us_geo import Canvas

R = random.Random(840500)
P = People(R)


def sf3(x):
    d = 2 - int(math.floor(math.log10(abs(x))))
    v = round(x, d)
    s = ("%.*f" % (max(d, 0), v)) if d > 0 else num(int(round(v)))
    return s.replace("-", MINUS)


def d1(x):
    return ("%.1f" % x).replace("-", MINUS)


def deg(x):
    return math.degrees(x)


def cuboid_fig(l, w, h, diag=None, label="cuboid ABCDEFGH"):
    """oblique cuboid: base ABCD (front-left A), top EFGH above it. diag: list of (p, q) to highlight"""
    sc = 150 / max(l, w * 0.6 + 1, h)
    L, Wd, H = l * sc, w * sc * 0.5, h * sc
    ox, oy = Wd * 0.8, -Wd * 0.6
    A = (0, 0)
    B = (L, 0)
    C = (L + ox, oy)
    D = (ox, oy)
    E, F, G, Hh = [(p[0], p[1] - H) for p in (A, B, C, D)]
    pts = dict(zip("ABCDEFGH", [A, B, C, D, E, F, G, Hh]))
    c = Canvas()
    c.poly([A, B, F, E], fill="#eef6f0")
    for a, b in ["BC", "CG", "FG", "GH", "HE"]:
        c.seg(pts[a], pts[b])
    for a, b in ["AD", "DC", "DH"]:
        c.seg(pts[a], pts[b], col="#888", w=1.8, dash=True)
    for a, b in (diag or []):
        c.seg(pts[a], pts[b], col="#c0392b", w=3)
    cen = (L / 2 + ox / 2, (oy - H) / 2)
    for n, p in pts.items():
        c.vlabel(p, n, cen, 14, 14)
    c.side_label(A, B, "%s cm" % num(l), cen, 14, 13, "#1f6fd1")
    c.side_label(B, C, "%s cm" % num(w), cen, 14, 13, "#1f6fd1")
    c.side_label(B, F, "%s cm" % num(h), cen, 18, 13, "#1f6fd1")
    return fig(c.svg(label))


def pyr_fig(a, h=None, edge=None, label="right pyramid VABCD on a square base"):
    sc = 130 / a
    L = a * sc
    ox, oy = L * 0.45, -L * 0.3
    A, B, C, D = (0, 0), (L, 0), (L + ox, oy), (ox, oy)
    M = ((A[0] + C[0]) / 2, (A[1] + C[1]) / 2)
    hh = (h or 1.2 * a) * sc
    V = (M[0], M[1] - hh)
    c = Canvas()
    for p, q in [(A, B), (B, C), (V, A), (V, B), (V, C)]:
        c.seg(p, q)
    for p, q in [(A, D), (D, C), (V, D), (V, M), (A, C)]:
        c.seg(p, q, col="#888", w=1.8, dash=True)
    c.dot(M, 3)
    cen = ((A[0] + C[0]) / 2, (V[1] + A[1]) / 2)
    for n, p in zip("ABCDVM", [A, B, C, D, V, M]):
        if n == "M":
            c.text((p[0] + 12, p[1] + 10), "M", 14)
        else:
            c.vlabel(p, n, cen, 14, 14)
    c.side_label(A, B, "%s cm" % num(a), cen, 14, 13, "#1f6fd1")
    return fig(c.svg(label))


# ------------------------------------------------------------ set 1: diagonals of cuboids
def one_diag(r):
    l, w, h = r.randint(4, 15), r.randint(3, 10), r.randint(3, 12)
    kind = r.choice(["face", "space", "space"])
    if kind == "face":
        pic = cuboid_fig(l, w, h, [("A", "C")])
        v = math.hypot(l, w)
        return T("ABCDEFGH is a cuboid. Find the length of the diagonal AC of the base, correct to 3 significant figures.%s" % pic, "%s cm" % sf3(v),
                 ["%s cm" % sf3(math.sqrt(l * l + w * w + h * h)), "%s cm" % num(l + w), "%s cm" % sf3(math.hypot(l, h))],
                 "AC is the hypotenuse of right-angled triangle ABC: √(%d² + %d²) = <b>%s cm</b>." % (l, w, sf3(v)))
    pic = cuboid_fig(l, w, h, [("A", "C"), ("C", "E") if False else ("A", "G")])
    v = math.sqrt(l * l + w * w + h * h)
    return T("ABCDEFGH is a cuboid. Find the length of the space diagonal AG, correct to 3 significant figures.%s" % pic, "%s cm" % sf3(v),
             ["%s cm" % sf3(math.hypot(l, w)), "%s cm" % num(l + w + h), "%s cm" % sf3(math.hypot(l, h))],
             "First AC = √(%d² + %d²). Then triangle ACG has a right angle at C: AG = √(%d² + %d² + %d²) = <b>%s cm</b>." % (l, w, l, w, h, sf3(v)))


# ------------------------------------------------------------ set 2: angle between a line and a plane
def one_lp(r):
    l, w, h = r.randint(4, 15), r.randint(3, 10), r.randint(3, 12)
    kind = r.choice(["AG", "AG", "AF", "EC"])
    if kind == "AG":
        pic = cuboid_fig(l, w, h, [("A", "C"), ("A", "G"), ("C", "G")])
        base = math.hypot(l, w)
        a = deg(math.atan(h / base))
        return T("ABCDEFGH is a cuboid. Find the angle between the diagonal AG and the base ABCD, correct to 1 decimal place.%s" % pic, "%s°" % d1(a),
                 ["%s°" % d1(90 - a), "%s°" % d1(deg(math.atan(h / l))), "%s°" % d1(deg(math.atan(h / w)))],
                 "The projection of AG on the base is AC = √(%d² + %d²) = %s. tan ∠GAC = %d ÷ %s, so ∠GAC = <b>%s°</b>." % (l, w, sf3(base), h, sf3(base), d1(a)))
    if kind == "AF":
        pic = cuboid_fig(l, w, h, [("A", "F")])
        a = deg(math.atan(h / l))
        return T("ABCDEFGH is a cuboid. Find the angle between AF and the base ABCD, correct to 1 decimal place.%s" % pic, "%s°" % d1(a),
                 ["%s°" % d1(90 - a), "%s°" % d1(deg(math.atan(h / math.hypot(l, w)))), "%s°" % d1(deg(math.atan(w / l)))],
                 "F is directly above B, so the angle is ∠FAB. tan ∠FAB = %d ÷ %d, so the angle is <b>%s°</b>." % (h, l, d1(a)))
    pic = cuboid_fig(l, w, h, [("E", "C"), ("E", "G")])
    a = deg(math.atan(h / math.hypot(l, w)))
    return T("ABCDEFGH is a cuboid. Find the angle between the diagonal EC and the top face EFGH, correct to 1 decimal place.%s" % pic, "%s°" % d1(a),
             ["%s°" % d1(90 - a), "%s°" % d1(deg(math.atan(h / l))), "%s°" % d1(deg(math.atan(l / h)))],
             "C is directly below G, so the angle is ∠CEG with EG = √(%d² + %d²). tan ∠CEG = %d ÷ %s, so the angle is <b>%s°</b>." % (l, w, h, sf3(math.hypot(l, w)), d1(a)))


# ------------------------------------------------------------ set 3: right pyramids
def one_pyr(r):
    a = r.choice([6, 8, 10, 12, 14, 16])
    kind = r.choice(["height", "edge", "angle", "vol"])
    half_diag = a * math.sqrt(2) / 2
    if kind == "height":
        e = r.randint(int(half_diag) + 2, int(half_diag) + 12)
        hh = math.sqrt(e * e - half_diag ** 2)
        pic = pyr_fig(a, hh)
        return T("VABCD is a right pyramid on a square base of side %d cm. Each slant edge is %d cm. M is the centre of the base. Find the height VM, correct to 3 significant figures.%s" % (a, e, pic),
                 "%s cm" % sf3(hh), ["%s cm" % sf3(math.sqrt(e * e - (a / 2) ** 2)), "%s cm" % sf3(math.sqrt(e * e - 2 * a * a) if e * e > 2 * a * a else e - a / 2), "%s cm" % sf3(math.hypot(e, half_diag))],
                 "AC = √(%d² + %d²) = %s, so AM = %s. VM = √(%d² − %s²) = <b>%s cm</b>." % (a, a, sf3(2 * half_diag), sf3(half_diag), e, sf3(half_diag), sf3(hh)))
    if kind == "edge":
        hh = r.randint(5, 20)
        e = math.hypot(hh, half_diag)
        pic = pyr_fig(a, hh)
        return T("VABCD is a right pyramid on a square base of side %d cm, with height %d cm. Find the length of the slant edge VA, correct to 3 significant figures.%s" % (a, hh, pic),
                 "%s cm" % sf3(e), ["%s cm" % sf3(math.hypot(hh, a / 2)), "%s cm" % sf3(math.hypot(hh, a)), "%s cm" % num(hh + a // 2)],
                 "AM is half of AC: AM = %s cm. VA = √(%d² + %s²) = <b>%s cm</b>." % (sf3(half_diag), hh, sf3(half_diag), sf3(e)))
    if kind == "angle":
        hh = r.randint(5, 20)
        ang = deg(math.atan(hh / half_diag))
        pic = pyr_fig(a, hh)
        return T("VABCD is a right pyramid on a square base of side %d cm, with height %d cm. Find the angle between the edge VA and the base, correct to 1 decimal place.%s" % (a, hh, pic),
                 "%s°" % d1(ang), ["%s°" % d1(deg(math.atan(hh / (a / 2)))), "%s°" % d1(90 - ang), "%s°" % d1(deg(math.atan(hh / a)))],
                 "The angle is ∠VAM. AM = %s cm, so tan ∠VAM = %d ÷ %s and ∠VAM = <b>%s°</b>." % (sf3(half_diag), hh, sf3(half_diag), d1(ang)))
    hh = r.randint(5, 20)
    ang = deg(math.atan(hh / (a / 2)))
    pic = pyr_fig(a, hh)
    return T("VABCD is a right pyramid on a square base of side %d cm, with height %d cm. N is the midpoint of AB. Find the angle between the face VAB and the base, correct to 1 decimal place.%s" % (a, hh, pic),
             "%s°" % d1(ang), ["%s°" % d1(deg(math.atan(hh / half_diag))), "%s°" % d1(90 - ang), "%s°" % d1(deg(math.atan(hh / a)))],
             "The angle is ∠VNM, where MN = %s cm (half the side). tan ∠VNM = %d ÷ %s, so the angle is <b>%s°</b>." % (num(a // 2), hh, num(a // 2), d1(ang)))


# ------------------------------------------------------------ set 4: elevation in 3D
def one_elev(r):
    l, w = r.randint(20, 80), r.randint(15, 60)
    kind = r.choice(["corner", "corner", "height", "far"])
    if kind == "corner":
        hgt = r.randint(8, 30)
        d = math.hypot(l, w)
        a = deg(math.atan(hgt / d))
        return T("A vertical pole %d m tall stands at corner A of a rectangular field ABCD, with AB = %d m and BC = %d m. Find the angle of elevation of the top of the pole from C, correct to 1 decimal place." % (hgt, l, w),
                 "%s°" % d1(a), ["%s°" % d1(deg(math.atan(hgt / l))), "%s°" % d1(90 - a), "%s°" % d1(deg(math.atan(hgt / (l + w))))],
                 "AC = √(%d² + %d²) = %s m. tan θ = %d ÷ %s, so θ = <b>%s°</b>." % (l, w, sf3(d), hgt, sf3(d), d1(a)))
    if kind == "height":
        a = r.randint(15, 45)
        d = math.hypot(l, w)
        hgt = d * math.tan(math.radians(a))
        return T("A lamp post stands at corner A of a rectangular car park ABCD with AB = %d m and BC = %d m. From C, the angle of elevation of the top is %d°. Find the height of the lamp post, correct to 3 significant figures." % (l, w, a),
                 "%s m" % sf3(hgt), ["%s m" % sf3(l * math.tan(math.radians(a))), "%s m" % sf3(d * math.sin(math.radians(a))), "%s m" % sf3(d / math.tan(math.radians(a)))],
                 "AC = √(%d² + %d²) = %s m. Height = %s × tan %d° = <b>%s m</b>." % (l, w, sf3(d), sf3(d), a, sf3(hgt)))
    hgt = r.randint(10, 40)
    a1 = deg(math.atan(hgt / l))
    a2 = deg(math.atan(hgt / math.hypot(l, w)))
    return T("A tower %d m tall stands at corner A of a rectangular plot ABCD with AB = %d m and BC = %d m. Find the difference between the angles of elevation of the top from B and from C, correct to 1 decimal place." % (hgt, l, w),
             "%s°" % d1(a1 - a2), ["%s°" % d1(a1 + a2), "%s°" % d1(deg(math.atan(hgt / w)) - a2) if abs(deg(math.atan(hgt / w)) - a1) > 0.05 else "%s°" % d1(a1), "%s°" % d1(a2)],
             "From B: tan<sup>−1</sup>(%d ÷ %d) = %s°. From C: AC = %s, tan<sup>−1</sup>(%d ÷ %s) = %s°. Difference = <b>%s°</b>." % (hgt, l, d1(a1), sf3(math.hypot(l, w)), hgt, sf3(math.hypot(l, w)), d1(a2), d1(a1 - a2)))


# ------------------------------------------------------------ set 5: bearings and elevation
def one_brg(r):
    kind = r.choice(["two", "two", "bearing", "dist"])
    nm, he, his = P.next()
    if kind == "two":
        hgt = r.randint(20, 80)
        a = r.randint(20, 50)
        b = r.randint(15, a - 3)
        da = hgt / math.tan(math.radians(a))
        db = hgt / math.tan(math.radians(b))
        AB = math.hypot(da, db)
        return T("A tower of height %d m stands at T. From a point A due south of T, the angle of elevation of the top is %d°. From a point B due east of T, it is %d°. Find the distance AB, correct to 3 significant figures." % (hgt, a, b),
                 "%s m" % sf3(AB), ["%s m" % sf3(da + db), "%s m" % sf3(abs(db - da)), "%s m" % sf3(math.hypot(hgt / math.tan(math.radians(90 - a)), db))],
                 "TA = %d ÷ tan %d° = %s m and TB = %d ÷ tan %d° = %s m. ∠ATB = 90°, so AB = √(%s² + %s²) = <b>%s m</b>." % (hgt, a, sf3(da), hgt, b, sf3(db), sf3(da), sf3(db), sf3(AB)))
    if kind == "bearing":
        n_, e_ = r.randint(20, 90), r.randint(20, 90)
        ang = deg(math.atan(e_ / n_))
        return T("A drone flies from P to a point %d m north and %d m east of P. Find the bearing of the drone's position from P, correct to 1 decimal place." % (n_, e_),
                 "%s°" % ("%05.1f" % ang), ["%s°" % ("%05.1f" % (90 - ang)), "%s°" % ("%05.1f" % (180 + ang)), "%s°" % ("%05.1f" % (360 - ang))],
                 "tan θ = %d ÷ %d, so θ = %s° clockwise from north: <b>%s°</b>." % (e_, n_, d1(ang), "%05.1f" % ang))
    if kind == "dist":
        hgt = r.randint(30, 120)
        a = r.randint(10, 40)
        d = hgt / math.tan(math.radians(a))
        return T("From the top of a %d m building, %s sees a car due east at an angle of depression of %d°. How far is the car from the foot of the building, correct to 3 significant figures?" % (hgt, nm, a),
                 "%s m" % sf3(d), ["%s m" % sf3(hgt * math.tan(math.radians(a))), "%s m" % sf3(hgt / math.sin(math.radians(a))), "%s m" % sf3(hgt * math.cos(math.radians(a)))],
                 "tan %d° = %d ÷ <i>d</i>, so <i>d</i> = %d ÷ tan %d° = <b>%s m</b>." % (a, hgt, hgt, a, sf3(d)))
    return None


def build():
    sets = [S("Diagonals of cuboids", collect(one_diag, 20, R)),
            S("Angle between a line and a plane", collect(one_lp, 20, R)),
            S("Right pyramids", collect(one_pyr, 20, R)),
            S("Angles of elevation in three dimensions", collect(one_elev, 20, R)),
            S("Bearings and elevation", collect(one_brg, 20, R))]
    body = lesson(
        "<ul><li>Find a <b>right-angled triangle</b> inside the solid and draw it flat. Most 3D problems need two triangles: one on the base and one standing up.</li>"
        "<li>Space diagonal of a cuboid = √(<i>l</i>² + <i>w</i>² + <i>h</i>²).</li>"
        "<li>The <b>angle between a line and a plane</b> is the angle between the line and its projection (shadow) on the plane.</li>"
        "<li>In a right pyramid, the apex is directly above the centre of the base, so use <b>half the base diagonal</b>.</li></ul>",
        [("A cuboid is 8 cm by 6 cm by 5 cm. Find the angle between the space diagonal and the base.", ["Base diagonal = √(8² + 6²) = 10", "tan θ = 5 ÷ 10"], "26.6°"),
         ("A right pyramid has a square base of side 10 cm and height 12 cm. Find the slant edge.", ["Half the base diagonal = √50 = 7.07 cm", "√(12² + 7.07²)"], "13.9 cm")],
        ["Using a face diagonal instead of the space diagonal.",
         "Using the whole base diagonal instead of half of it for a pyramid.",
         "Measuring the angle with the vertical instead of with the plane.",
         "Forgetting to find the base length first in 3D elevation problems."])
    faq = [("How do you solve 3D trigonometry problems?", "Identify a right-angled triangle that contains the length or angle you need, draw it in 2D, and use Pythagoras' theorem or SOH CAH TOA. You may need to find a side from another triangle first."),
           ("What is the angle between a line and a plane?", "Drop a perpendicular from the top of the line to the plane. The angle is between the line and the line joining its foot to the point where the line meets the plane."),
           ("How do you find the space diagonal of a cuboid?", "Use √(l² + w² + h²): first the base diagonal √(l² + w²), then Pythagoras again with the height."),
           ("Why do pyramid problems use half the base diagonal?", "The apex of a right pyramid is directly above the centre of the base, and the centre is halfway along each diagonal.")]
    make(4, "problems-in-three-dimensions", 5, "G4",
         "Problems in Three Dimensions: Cuboids, Pyramids and Elevation",
         "", "Problems in three dimensions", "",
         "Free Secondary 4 maths worksheets on 3D trigonometry: diagonals of cuboids, angles between lines and planes, right pyramids, angles of elevation in 3D and bearings. 100 questions with answers.",
         "Find a right-angled triangle inside the solid and draw it flat.",
         "Space diagonal = √(l² + w² + h²); a pyramid's apex is above the centre of its base.",
         body, faq, sets, R)


if __name__ == "__main__":
    build()
