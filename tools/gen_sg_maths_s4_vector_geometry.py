# -*- coding: utf-8 -*-
"""
SG Secondary 4 Maths: Vector Geometry (MOE syllabus G7: expressing vectors in terms of two coplanar vectors;
geometric problems involving vectors)
  python3 tools/gen_sg_maths_s4_vector_geometry.py
Writing vectors in terms of a and b in triangles and parallelograms, midpoints and points dividing a line in a
ratio, extended lines, parallel vectors and collinear points, and ratios of lengths and areas.
Wrong answers come from real mistakes: a − b instead of b − a, using the fraction of AB from the wrong end,
treating parallel as equal, and using a length ratio for an area ratio.
"""
import random
from fractions import Fraction as F
from sg_sec import num, S, make, lesson, collect, T, fig, fr, MINUS
from us_geo import Canvas

R = random.Random(840400)
A_, B_ = "<b>a</b>", "<b>b</b>"


def ov(s):
    return "<span class='ov'>%s</span>" % s


def co(c, first):
    c = F(c)
    if c == 1:
        return "" if first else "+ "
    if c == -1:
        return MINUS if first else MINUS + " "
    mag = num(abs(c)) if c.denominator == 1 else fr(num(abs(c.numerator)), num(c.denominator))
    if first:
        return (MINUS if c < 0 else "") + mag
    return ("+ " if c > 0 else MINUS + " ") + mag


def vab(x, y):
    """x a + y b"""
    x, y = F(x), F(y)
    parts = []
    if x:
        parts.append(co(x, True) + A_)
    if y:
        parts.append(co(y, not parts) + B_)
    return " ".join(parts) if parts else "<b>0</b>"


def tri_fig(extra=(), label="triangle OAB with OA = a and OB = b", para=False, la="<b>a</b>", lb="<b>b</b>"):
    c = Canvas()
    O, A, B = (0, 140), (60, 0), (220, 140)
    C = (A[0] + B[0] - O[0], A[1] + B[1] - O[1])
    if para:
        c.poly([O, A, C, B], fill="#eef6f0")
    else:
        c.poly([O, A, B], fill="#eef6f0")
    for (p, q), name in [((O, A), "a"), ((O, B), "b")]:
        c.seg(p, q, col="#1f6fd1", w=3)
        c.head(((p[0] + q[0]) / 2 + (q[0] - p[0]) * 0.08, (p[1] + q[1]) / 2 + (q[1] - p[1]) * 0.08), p, col="#1f6fd1")
    c.side_label(O, A, la.replace("<b>", "").replace("</b>", ""), B, 18, 16, "#1f6fd1")
    c.side_label(O, B, lb.replace("<b>", "").replace("</b>", ""), A, 18, 16, "#1f6fd1")
    pts = {"O": O, "A": A, "B": B}
    if para:
        pts["C"] = C
    for name, t in extra:
        P0, P1 = pts[name[0]], pts[name[1]]
        pts[name[2]] = (P0[0] + (P1[0] - P0[0]) * t, P0[1] + (P1[1] - P0[1]) * t)
        if t > 1:
            c.seg(P1, pts[name[2]], dash=True)
    cen = (sum(p[0] for p in pts.values()) / len(pts), sum(p[1] for p in pts.values()) / len(pts))
    for n, p in pts.items():
        c.dot(p, 3.5)
        c.vlabel(p, n, cen, 15)
    return fig(c.svg(label))


# ------------------------------------------------------------ set 1: triangles and parallelograms
def one_basic(r):
    ca, cb = r.choice([1, 1, 2, 3]), r.choice([1, 1, 2, 3, 4])
    kind = r.choice(["AB", "BA", "OC", "AC", "BC", "CO"])
    oa, ob = vab(ca, 0), vab(0, cb)
    pre = "%s = %s and %s = %s." % (ov("OA"), oa, ov("OB"), ob)
    if kind in ("AB", "BA"):
        pic = tri_fig(la=oa, lb=ob)
        right = vab(-ca, cb) if kind == "AB" else vab(ca, -cb)
        wrong = vab(ca, -cb) if kind == "AB" else vab(-ca, cb)
        return T("%s Find %s.%s" % (pre, ov(kind), pic), right, [wrong, vab(ca, cb), vab(-ca, -cb)],
                 "%s = %s + %s. Going against a vector changes its sign: <b>%s</b>." % (ov(kind), ov(kind[0] + "O"), ov("O" + kind[1]), right))
    pic = tri_fig(para=True, label="parallelogram OACB", la=oa, lb=ob)
    pre = "OACB is a parallelogram. " + pre
    ans = {"OC": (vab(ca, cb), [vab(-ca, cb), vab(ca, -cb), vab(2 * ca, 2 * cb)], "%s = %s + %s = %s + %s" % (ov("OC"), ov("OA"), ov("AC"), oa, ob)),
           "AC": (vab(0, cb), [vab(ca, 0), vab(-ca, cb), vab(ca, cb)], "AC is parallel and equal to OB"),
           "BC": (vab(ca, 0), [vab(0, cb), vab(ca, -cb), vab(-ca, 0)], "BC is parallel and equal to OA"),
           "CO": (vab(-ca, -cb), [vab(ca, cb), vab(ca, -cb), vab(-ca, cb)], "%s is the reverse of %s = %s" % (ov("CO"), ov("OC"), vab(ca, cb)))}[kind]
    return T("%s Find %s.%s" % (pre, ov(kind), pic), ans[0], ans[1], "%s, so %s = <b>%s</b>." % (ans[2], ov(kind), ans[0]))


# ------------------------------------------------------------ set 2: midpoints and ratios
def one_ratio(r):
    m, n = r.choice([(1, 1), (1, 2), (2, 1), (1, 3), (3, 1), (2, 3), (3, 2), (1, 4), (3, 5)])
    t = F(m, m + n)
    kind = r.choice(["OP", "OP", "AP", "PB"])
    pic = tri_fig([("ABP", float(t))], label="triangle OAB with P on AB")
    lab = "M is the midpoint of AB" if (m, n) == (1, 1) else "P lies on AB with AP : PB = %d : %d" % (m, n)
    nm = "M" if (m, n) == (1, 1) else "P"
    pic = pic.replace(">P<", ">%s<" % nm)
    if kind == "OP":
        right = vab(1 - t, t)
        return T("%s = %s and %s = %s. %s. Find %s.%s" % (ov("OA"), A_, ov("OB"), B_, lab, ov("O" + nm), pic), right, [vab(t, 1 - t) if t != F(1, 2) else vab(1, 1), vab(1, t), vab(-t, t)],
                 "%s = %s + %s %s = %s + %s(%s) = <b>%s</b>." % (ov("O" + nm), ov("OA"), fr(m, m + n) if m + n != 1 else "", ov("AB"), A_, fr(m, m + n), vab(-1, 1), right))
    if kind == "AP":
        right = vab(-t, t)
        return T("%s = %s and %s = %s. %s. Find %s.%s" % (ov("OA"), A_, ov("OB"), B_, lab, ov("A" + nm), pic), right, [vab(t, -t), vab(-(1 - t), 1 - t) if t != F(1, 2) else vab(-1, 1), vab(0, t)],
                 "%s = %s %s = %s(%s) = <b>%s</b>." % (ov("A" + nm), fr(m, m + n), ov("AB"), fr(m, m + n), vab(-1, 1), right))
    right = vab(-(1 - t), 1 - t)
    return T("%s = %s and %s = %s. %s. Find %s.%s" % (ov("OA"), A_, ov("OB"), B_, lab, ov(nm + "B"), pic), right, [vab(1 - t, -(1 - t)), vab(-t, t) if t != F(1, 2) else vab(-1, 1), vab(1 - t, t)],
             "%s = %s %s = %s(%s) = <b>%s</b>." % (ov(nm + "B"), fr(n, m + n), ov("AB"), fr(n, m + n), vab(-1, 1), right))


# ------------------------------------------------------------ set 3: points on extended lines
def one_ext(r):
    kind = r.choice(["OC", "BC", "CD", "QA"])
    k = r.choice([2, 3, F(3, 2), F(5, 2), F(4, 3)])
    if kind in ("OC", "BC"):
        pic = tri_fig([("OAC", float(k))], label="OA extended to C")
        pre = "%s = %s and %s = %s. OA is extended to C so that OC = %s OA." % (ov("OA"), A_, ov("OB"), B_, num(k) if F(k).denominator == 1 else fr(num(F(k).numerator), num(F(k).denominator)))
        if kind == "OC":
            return T(pre + " Find %s.%s" % (ov("OC"), pic), vab(k, 0), [vab(k - 1, 0), vab(k, 1), vab(1, k)], "%s = %s × %s = <b>%s</b>." % (ov("OC"), fr(num(F(k).numerator), num(F(k).denominator)) if F(k).denominator != 1 else num(k), A_, vab(k, 0)))
        return T(pre + " Find %s.%s" % (ov("BC"), pic), vab(k, -1), [vab(-k, 1), vab(k, 1), vab(k - 1, -1)], "%s = %s + %s = −%s + %s = <b>%s</b>." % (ov("BC"), ov("BO"), ov("OC"), B_, vab(k, 0), vab(k, -1)))
    if kind == "CD":
        p, q = r.choice([(2, 3), (3, 2), (1, 2), (2, 1), (3, 4)])
        pre = "%s = %s and %s = %s. C is the point with %s = %s and D is the point with %s = %s." % (ov("OA"), A_, ov("OB"), B_, ov("OC"), vab(p, 0), ov("OD"), vab(0, q))
        return T(pre + " Find %s." % ov("CD"), vab(-p, q), [vab(p, -q), vab(p, q), vab(-q, p)], "%s = %s − %s = <b>%s</b> (end minus start)." % (ov("CD"), ov("OD"), ov("OC"), vab(-p, q)))
    m, n = r.choice([(1, 2), (2, 1), (1, 3), (3, 1), (2, 3)])
    t = F(m, m + n)
    pre = "%s = %s and %s = %s. Q lies on OB with OQ : QB = %d : %d." % (ov("OA"), A_, ov("OB"), B_, m, n)
    pic = tri_fig([("OBQ", float(t))], label="triangle OAB with Q on OB")
    return T(pre + " Find %s.%s" % (ov("QA"), pic), vab(1, -t), [vab(-1, t), vab(1, -(1 - t)), vab(1, t)], "%s = %s %s = %s, so %s = %s − %s = <b>%s</b>." % (
        ov("OQ"), fr(m, m + n), ov("OB"), vab(0, t), ov("QA"), ov("OA"), ov("OQ"), vab(1, -t)))


# ------------------------------------------------------------ set 4: parallel vectors and collinear points
def one_par(r):
    kind = r.choice(["par", "par", "ratio", "col", "k"])
    x, y = r.choice([(1, 2), (2, 3), (1, -3), (3, 1), (2, -1), (1, 4)])
    m = r.choice([2, 3, 4, F(1, 2), F(3, 2)])
    if kind == "par":
        q = "%s = %s and %s = %s. What can you say about PQ and RS?" % (ov("PQ"), vab(m * x, m * y), ov("RS"), vab(x, y))
        right = "PQ is parallel to RS and PQ = %s RS" % (num(m) if F(m).denominator == 1 else fr(num(F(m).numerator), num(F(m).denominator)))
        return T(q, right, ["PQ is perpendicular to RS", "PQ and RS are equal vectors", "PQ is parallel to RS and PQ = RS"],
                 "%s = %s × %s, a scalar multiple, so <b>%s</b>." % (ov("PQ"), num(m) if F(m).denominator == 1 else fr(num(F(m).numerator), num(F(m).denominator)), ov("RS"), right))
    if kind == "ratio":
        if F(m).denominator != 1:
            return None
        q = "%s = %s and %s = %s. Find the ratio PQ : RS." % (ov("PQ"), vab(m * x, m * y), ov("RS"), vab(x, y))
        return T(q, "%s : 1" % num(m), ["1 : %s" % num(m), "%s : 1" % num(m * m), "%s : %s" % (num(abs(m * x) + abs(m * y)), num(abs(x) + abs(y))) if m * x != m else "1 : 1"],
                 "%s = %s %s, so PQ is %s times as long: <b>%s : 1</b>." % (ov("PQ"), num(m), ov("RS"), num(m), num(m)))
    if kind == "col":
        a1, b1 = r.choice([(1, 1), (2, 1), (1, 2), (3, 1)])
        k = r.choice([2, 3])
        q = "%s = %s and %s = %s. Which statement is true?" % (ov("OP"), vab(a1, b1), ov("OQ"), vab(k * a1, k * b1))
        right = "O, P and Q are collinear, and OQ = %d OP" % k
        return T(q, right, ["OPQ is a triangle with OP perpendicular to PQ", "O, P and Q are collinear, and OP = %d OQ" % k, "P is the midpoint of OQ" if k != 2 else "Q is the midpoint of OP"],
                 "%s = %d %s, so the two vectors are parallel and share the point O: <b>%s</b>." % (ov("OQ"), k, ov("OP"), right))
    k = r.choice([2, 3, 4, -2])
    q = "%s = %s and %s = %s + <i>h</i>%s. If XY is parallel to %s, find <i>h</i>." % (ov("XY"), vab(k * x, 0) + (" + <i>h</i>" + B_ if False else ""), ov("XY"), vab(k * x, 0), B_, vab(x, y))
    q = "%s = %s + <i>h</i>%s and XY is parallel to %s. Find <i>h</i>." % (ov("XY"), vab(k * x, 0), B_, vab(x, y))
    return T(q, num(k * y), [num(y), num(k * x), num(-k * y)], "Parallel means %s = <i>m</i>(%s). Comparing %s: <i>m</i> = %s, so <i>h</i> = %s × %s = <b>%s</b>." % (
        ov("XY"), vab(x, y), A_, num(k), num(k), num(y), num(k * y)))


# ------------------------------------------------------------ set 5: lengths and areas
def one_area(r):
    kind = r.choice(["tri", "tri", "len", "len", "par"])
    if kind == "tri":
        m, n = r.choice([(1, 2), (2, 1), (1, 3), (2, 3), (3, 2), (1, 4), (3, 1), (4, 1), (2, 5)])
        side, pt, other = r.choice([("OA", "P", "B"), ("OB", "Q", "A")])
        q = "In △OAB, %s is on %s with O%s : %s%s = %d : %d. Find the ratio area of △O%s%s : area of △OAB." % (pt, side, pt, pt, side[1], m, n, pt, other)
        return T(q, "%d : %d" % (m, m + n), ["%d : %d" % (m, n), "%d : %d" % (m * m, (m + n) ** 2), "%d : %d" % (n, m + n)],
                 "Both triangles have the same height from %s, so their areas are in the ratio of the bases O%s : %s = <b>%d : %d</b>." % (other, pt, side, m, m + n))
    if kind == "len":
        k = r.choice([2, 3, 4, 5])
        x, y = r.choice([(-1, 1), (1, 2), (2, -1), (1, -3), (3, 1), (-2, 1)])
        q = "%s = %s and %s = %s. Find the ratio XY : AB." % (ov("AB"), vab(x, y), ov("XY"), vab(k * x, k * y))
        return T(q, "%d : 1" % k, ["1 : %d" % k, "%d : 1" % (k * k), "1 : 1"], "%s = %d(%s) = %d %s, so XY is %d times as long as AB: <b>%d : 1</b>." % (ov("XY"), k, vab(x, y), k, ov("AB"), k, k))
    k = r.choice([2, 3, 4])
    x, y = r.choice([(1, 0), (0, 1), (1, 1), (2, 1), (1, -1), (1, 2)])
    q = "ABCD is a quadrilateral with %s = %s, %s = %s and %s = %s. What type of quadrilateral is ABCD?" % (ov("AB"), vab(x, y), ov("DC"), vab(k * x, k * y), ov("AD"), vab(y + 1, x + 2))
    return T(q, "A trapezium", ["A parallelogram", "A rhombus", "A rectangle"],
             "%s = %d %s, so AB is parallel to DC but %d times as long. Exactly one pair of parallel sides: <b>a trapezium</b>." % (ov("DC"), k, ov("AB"), k))


def build():
    sets = [S("Triangles and parallelograms", collect(one_basic, 20, R)),
            S("Midpoints and ratios", collect(one_ratio, 20, R)),
            S("Points on extended lines", collect(one_ext, 20, R)),
            S("Parallel vectors and collinear points", collect(one_par, 20, R)),
            S("Lengths, areas and shapes", collect(one_area, 20, R))]
    body = lesson(
        "<ul><li>Follow a route along known vectors: <span class='ov'>AB</span> = <span class='ov'>AO</span> + <span class='ov'>OB</span> = −<b>a</b> + <b>b</b>.</li>"
        "<li>If P is on AB with AP : PB = <i>m</i> : <i>n</i>, then <span class='ov'>AP</span> = <i>m</i>/(<i>m</i> + <i>n</i>) <span class='ov'>AB</span>.</li>"
        "<li>If <span class='ov'>PQ</span> = <i>k</i> <span class='ov'>RS</span>, then PQ is <b>parallel</b> to RS and <i>k</i> times as long.</li>"
        "<li>If <span class='ov'>OQ</span> = <i>k</i> <span class='ov'>OP</span>, then O, P and Q are <b>collinear</b> (on one straight line).</li></ul>",
        [("OA = a, OB = b and M is the midpoint of AB. Find OM.", ["AB = b − a", "OM = OA + ½AB = a + ½(b − a)"], "½a + ½b"),
         ("PQ = 6a + 3b and RS = 2a + b. Compare PQ and RS.", ["6a + 3b = 3(2a + b)"], "PQ is parallel to RS and 3 times as long")],
        ["Writing a − b for AB. Go from A back to O, then to B: −a + b.",
         "Using the fraction from the wrong end of the line.",
         "Saying parallel vectors are equal. They can have different lengths.",
         "Using the length ratio for an area ratio without checking the heights."])
    faq = [("How do you express a vector in terms of a and b?", "Find a route from the start point to the end point along vectors you know, then add them, using a minus sign when you go against a vector."),
           ("How do you find the vector to a point that divides a line in a ratio?", "If AP : PB = m : n, then AP = m/(m + n) of AB, so OP = OA + m/(m + n) AB."),
           ("How do you show that three points are collinear?", "Show that two vectors joining them are scalar multiples of each other and share a common point, for example OQ = 3 OP."),
           ("What does PQ = k RS tell you?", "PQ is parallel to RS and k times as long. If k is negative, it points the opposite way.")]
    make(4, "vector-geometry", 4, "G7",
         "Vector Geometry: Expressing Vectors and Proving Parallel Lines",
         "", "Vector geometry", "",
         "Free Secondary 4 maths worksheets on vector geometry: expressing vectors in terms of a and b, midpoints, ratios, extended lines, parallel vectors, collinear points and area ratios. 100 questions with answers.",
         "Follow a route: AB = AO + OB = −a + b.",
         "PQ = k RS means PQ is parallel to RS and k times as long.",
         body, faq, sets, R)


if __name__ == "__main__":
    build()
