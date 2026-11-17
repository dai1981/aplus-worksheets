# -*- coding: utf-8 -*-
"""
US Geometry: Midsegments, Bisectors, and Triangle Centers (Common Core G-CO.C.10, G-CO.C.9)
  python3 tools/gen_us_math_ge_midsegments_and_triangle_centers.py
The Triangle Midsegment Theorem, the Perpendicular Bisector and Angle Bisector Theorems, the centroid's
2 : 1 ratio, naming the four centers, and the Triangle Inequality with side and angle order.
Wrong answers come from real mistakes: doubling instead of halving a midsegment, splitting a median 1 : 1,
mixing up the circumcenter and the incenter, and adding instead of subtracting for the smallest third side.
"""
import random
from us_hs import B, S, make, lesson, collect, T, fig, num, MINUS
from us_geo import Canvas, RED, GREEN, BLUE

R = random.Random(93101)


def lin(a, b):
    s = ("" if a == 1 else num(a)) + "<i>x</i>"
    if b > 0:
        s += " + %s" % num(b)
    elif b < 0:
        s += " %s %s" % (MINUS, num(-b))
    return s


TRI = [(20, 180), (300, 180), (110, 20)]


def mid(p, q):
    return ((p[0] + q[0]) / 2, (p[1] + q[1]) / 2)


def mids_fig(lab_mid, lab_base):
    A, Bp, C = TRI
    D, E = mid(A, C), mid(Bp, C)
    c = Canvas()
    c.poly([A, Bp, C])
    c.seg(D, E, col=RED, w=2.5)
    for p in (D, E):
        c.dot(p, 3.5)
    c.ticks(A, D, 1)
    c.ticks(D, C, 1)
    c.ticks(Bp, E, 2)
    c.ticks(E, C, 2)
    c.vlabels([A, Bp, C], "ABC")
    c.text((D[0] - 14, D[1] - 4), "D", 15)
    c.text((E[0] + 14, E[1] - 4), "E", 15)
    c.text(((D[0] + E[0]) / 2, D[1] - 14), lab_mid, 14, RED)
    c.text((160, 202), lab_base, 14)
    return c.svg("triangle ABC with midsegment DE")


def cent_fig(lab1, lab2):
    A, Bp, C = TRI
    M = mid(Bp, C)
    G = ((A[0] + Bp[0] + C[0]) / 3, (A[1] + Bp[1] + C[1]) / 3)
    c = Canvas()
    c.poly([A, Bp, C])
    for v, opp in ((A, mid(Bp, C)), (Bp, mid(A, C)), (C, mid(A, Bp))):
        c.seg(v, opp, col=BLUE, w=1.8)
    c.dot(G, 4, RED)
    c.dot(M, 3.5)
    c.vlabels([A, Bp, C], "ABC")
    c.text((G[0] - 4, G[1] + 18), "G", 15, RED)
    c.text((M[0] + 14, M[1] - 4), "M", 15)
    c.text(((A[0] + G[0]) / 2, (A[1] + G[1]) / 2 - 12), lab1, 13)
    c.text(((G[0] + M[0]) / 2 + 6, (G[1] + M[1]) / 2 - 12), lab2, 13)
    return c.svg("triangle ABC with its three medians meeting at G")


# ------------------------------------------------------------ set 1: midsegments
def one_mid(r):
    kind = r.choice(["half", "dbl", "alg", "alg", "perim"])
    if kind == "half":
        L = r.randint(6, 40) * r.choice([1, 2]) + r.choice([0, 0, 1])
        q = "D and E are midpoints. AB = %s. Find DE.%s" % (num(L), fig(mids_fig("?", "AB = %s" % num(L))))
        ans = L / 2
        return T(q, num(ans), [num(w) for w in dict.fromkeys([L, 2 * L, L / 3, ans + 1]) if w != ans][:3],
                 "Triangle Midsegment Theorem: the midsegment is parallel to the third side and half as long. DE = %s ÷ 2 = <b>%s</b>." % (num(L), num(ans)))
    if kind == "dbl":
        L = r.randint(3, 25)
        q = "D and E are midpoints. DE = %d. Find AB.%s" % (L, fig(mids_fig("DE = %d" % L, "?")))
        ans = 2 * L
        return T(q, num(ans), [num(w) for w in dict.fromkeys([L, L / 2, 3 * L, ans + 2]) if w != ans][:3],
                 "The third side is twice the midsegment: AB = 2 × %d = <b>%d</b>." % (L, ans))
    if kind == "perim":
        a, b, c_ = r.randint(6, 30) * 2, r.randint(6, 30) * 2, r.randint(6, 30) * 2
        if max(a, b, c_) >= a + b + c_ - max(a, b, c_):
            return None
        q = ("The sides of a triangle are %d, %d and %d. The three midsegments form a smaller triangle. What is its perimeter?" % (a, b, c_))
        ans = (a + b + c_) // 2
        return T(q, num(ans), [num(w) for w in dict.fromkeys([a + b + c_, (a + b + c_) // 4 if (a + b + c_) % 4 == 0 else ans + 3, 2 * (a + b + c_)]) if w != ans][:3],
                 "Each midsegment is half of a side, so the perimeter is half: (%d + %d + %d) ÷ 2 = <b>%d</b>." % (a, b, c_, ans))
    x = r.randint(2, 12)
    k1, d1 = r.randint(1, 5), r.randint(-6, 10)
    de = k1 * x + d1
    if de < 3:
        return None
    k2 = r.choice([k for k in range(1, 9) if k != 2 * k1])
    d2 = 2 * de - k2 * x
    if abs(d2) > 30:
        return None
    ask = r.choice(["x", "AB"])
    q = "D and E are midpoints. DE = %s and AB = %s. Find %s.%s" % (lin(k1, d1), lin(k2, d2), "<i>x</i>" if ask == "x" else "AB",
                                                                     fig(mids_fig("DE = " + lin(k1, d1), "AB = " + lin(k2, d2))))
    steps = "AB = 2 × DE: %s = 2(%s) = %s. Solve: <i>x</i> = %d." % (lin(k2, d2), lin(k1, d1), lin(2 * k1, 2 * d1), x)
    if ask == "x":
        bad = (d1 - d2) / (k2 - k1) if k2 != k1 else None
        wr = [int(bad) if bad and bad == int(bad) and bad > 0 else x + 2, de, x + 1, 2 * x]
        return T(q, num(x), [num(w) for w in dict.fromkeys(wr) if w != x and w > 0][:3], steps.replace("<i>x</i> = %d." % x, "<i>x</i> = <b>%d</b>." % x))
    return T(q, num(2 * de), [num(w) for w in dict.fromkeys([de, x, 4 * de, 2 * de + 2]) if w != 2 * de][:3], steps + " AB = 2 × %d = <b>%d</b>." % (de, 2 * de))


# ------------------------------------------------------------ set 2: bisector theorems
def one_bis(r):
    x = r.randint(2, 14)
    k1, k2 = r.sample(range(1, 8), 2)
    d1 = r.randint(-8, 15)
    v = k1 * x + d1
    d2 = v - k2 * x
    if v < 4 or abs(d2) > 35:
        return None
    if r.random() < 0.5:
        P, A, Bp = r.choice([("P", "A", "B"), ("Q", "R", "S"), ("D", "E", "F"), ("K", "J", "L")])
        q = "Point %s is on the perpendicular bisector of <span class='ov'>%s%s</span>. %s%s = %s and %s%s = %s. Find %s." % (
            P, A, Bp, P, A, lin(k1, d1), P, Bp, lin(k2, d2), r.choice(["<i>x</i>", "%s%s" % (P, A)]))
        why = "Perpendicular Bisector Theorem: a point on the perpendicular bisector is equidistant from the endpoints, so %s%s = %s%s." % (P, A, P, Bp)
    else:
        P, A = r.choice([("P", "∠ABC"), ("D", "∠XYZ"), ("M", "∠JKL"), ("Q", "∠RST")])
        q = "Point %s is on the bisector of %s. Its distances to the two sides of the angle are %s and %s. Find %s." % (
            P, A, lin(k1, d1), lin(k2, d2), r.choice(["<i>x</i>", "the distance"]))
        why = "Angle Bisector Theorem: a point on an angle bisector is equidistant from the two sides of the angle."
    diff = abs(k1 - k2)
    steps = " %s = %s, so %s<i>x</i> = %d and <i>x</i> = %d." % (lin(k1, d1), lin(k2, d2), num(diff) if diff > 1 else "", abs(d2 - d1), x)
    steps = steps.replace(", so <i>x</i> = %d and <i>x</i> = " % abs(d2 - d1), ", so <i>x</i> = ")
    if q.endswith("<i>x</i>."):
        bad = (d1 + d2) / (k1 + k2)
        wr = [v, x + 1, x + 2, int(bad) if bad == int(bad) and bad > 0 else x - 1]
        return T(q, num(x), [num(w) for w in dict.fromkeys(wr) if w != x and w > 0][:3], why + steps[:steps.rindex("= %d." % x)] + "= <b>%d</b>." % x)
    return T(q, num(v), [num(w) for w in dict.fromkeys([x, 2 * v, v + diff, v - 2]) if w != v and w > 0][:3], why + steps + " The length is <b>%d</b>." % v)


# ------------------------------------------------------------ set 3: centroid
def one_cent(r):
    u = r.randint(2, 15)
    kind = r.choice(["AG", "GM", "AM", "alg", "alg"])
    if kind == "alg":
        x = r.randint(2, 9)
        k1, d1 = r.randint(1, 4), r.randint(-4, 8)
        gm = k1 * x + d1
        if gm < 2:
            return None
        k2 = r.choice([k for k in range(1, 9) if k != 2 * k1])
        d2 = 2 * gm - k2 * x
        if abs(d2) > 30:
            return None
        q = "G is the centroid of △ABC. AG = %s and GM = %s. Find <i>x</i>.%s" % (lin(k2, d2), lin(k1, d1), fig(cent_fig(lin(k2, d2), lin(k1, d1))))
        e = "The centroid is twice as far from the vertex as from the midpoint: AG = 2 × GM. %s = 2(%s), so <i>x</i> = <b>%d</b>." % (lin(k2, d2), lin(k1, d1), x)
        bad = (d1 - d2) / (k2 - k1) if k2 != k1 else None
        wr = [int(bad) if bad and bad == int(bad) and bad > 0 else x + 2, gm, x + 1, 2 * gm]
        return T(q, num(x), [num(w) for w in dict.fromkeys(wr) if w != x and w > 0][:3], e)
    GM, AG, AM = u, 2 * u, 3 * u
    if kind == "AG":
        q = "G is the centroid of △ABC and GM = %d. Find AG.%s" % (GM, fig(cent_fig("?", str(GM))))
        ans, wr = AG, [GM, AM, GM // 2 if GM % 2 == 0 else AG + 1]
        e = "Centroid Theorem: AG is 2/3 of the median and GM is 1/3, so AG = 2 × GM = <b>%d</b>." % AG
    elif kind == "GM":
        q = "G is the centroid of △ABC and AG = %d. Find GM.%s" % (AG, fig(cent_fig(str(AG), "?")))
        ans, wr = GM, [AG, 2 * AG, AM]
        e = "GM is half of AG: %d ÷ 2 = <b>%d</b>." % (AG, GM)
    else:
        q = "G is the centroid of △ABC and AG = %d. Find the length of the median AM.%s" % (AG, fig(cent_fig(str(AG), "")))
        ans, wr = AM, [AG + AG, GM, AG + 1]
        e = "AG is 2/3 of AM, so GM = %d ÷ 2 = %d and AM = %d + %d = <b>%d</b>." % (AG, GM, AG, GM, AM)
    return T(q, num(ans), [num(w) for w in dict.fromkeys(wr) if w != ans and w > 0][:3], e)


# ------------------------------------------------------------ set 4: which center
CENTERS = {
    "circumcenter": ("perpendicular bisectors of the sides", "the same distance from all three vertices", "the center of a circle through all three vertices"),
    "incenter": ("angle bisectors", "the same distance from all three sides", "the center of a circle that touches all three sides"),
    "centroid": ("medians", "the balance point of the triangle", "2/3 of the way from each vertex to the midpoint of the opposite side"),
    "orthocenter": ("altitudes", "where the heights meet", "where the lines through each vertex perpendicular to the opposite side meet"),
}


def one_which(r):
    kind = r.choice(["lines", "prop", "prop", "where", "use"])
    name = r.choice(list(CENTERS))
    names = [n.capitalize() for n in CENTERS]
    if kind == "lines":
        q = "The %s of a triangle meet at which point?" % B(CENTERS[name][0])
        return T(q, name.capitalize(), [n for n in names if n != name.capitalize()], "The %s meet at the <b>%s</b>." % (CENTERS[name][0], name))
    if kind == "prop":
        p = r.choice(CENTERS[name][1:])
        q = "Which point of a triangle is %s?" % B(p)
        return T(q, name.capitalize(), [n for n in names if n != name.capitalize()], "The <b>%s</b> is %s." % (name, p))
    if kind == "where":
        items = [("Where is the circumcenter of a right triangle?", "At the midpoint of the hypotenuse", ["At the right-angle vertex", "Outside the triangle", "At the centroid"],
                  "The hypotenuse is a diameter of the circle through the three vertices."),
                 ("Where is the circumcenter of an obtuse triangle?", "Outside the triangle", ["Inside the triangle", "On the longest side", "At the obtuse vertex"],
                  "The perpendicular bisectors meet outside, beyond the longest side."),
                 ("Where is the orthocenter of a right triangle?", "At the vertex of the right angle", ["At the midpoint of the hypotenuse", "Outside the triangle", "Inside the triangle"],
                  "The two legs are altitudes, and they meet at the right angle."),
                 ("Which center is always inside the triangle?", "The incenter (and the centroid)", ["The circumcenter", "The orthocenter", "None of them"],
                  "Angle bisectors and medians stay inside every triangle."),
                 ("In an equilateral triangle, how are the four centers placed?", "They are all the same point", ["They form a smaller triangle", "Two are inside and two are outside", "They are on one side"],
                  "Every bisector, median and altitude is the same line in an equilateral triangle.")]
        q, right, wr, e = r.choice(items)
        return T(q, right, wr, e + " <b>%s</b>." % right)
    items = [("Three towns want a water tower the same distance from each town. Which center should they use?", "Circumcenter"),
             ("A park ranger wants a lookout the same distance from three straight roads that form a triangle. Which center?", "Incenter"),
             ("A student wants to balance a triangular piece of cardboard on a pencil tip. Which center?", "Centroid"),
             ("A designer wants the largest circle that fits inside a triangular garden. Which center is the circle's center?", "Incenter"),
             ("Three friends live at different houses and want to meet at a point equally far from all three. Which center?", "Circumcenter")]
    q, right = r.choice(items)
    why = {"Circumcenter": "is the same distance from the three vertices (points)", "Incenter": "is the same distance from the three sides (lines)", "Centroid": "is the balance point"}[right]
    return T(q, right, [n for n in names if n != right], "The %s %s. <b>%s</b>." % (right.lower(), why, right))


# ------------------------------------------------------------ set 5: triangle inequality and order
def one_ineq(r):
    kind = r.choice(["can", "can", "range", "range", "order", "order"])
    if kind == "can":
        a, b = r.randint(3, 20), r.randint(3, 20)
        c_ = r.choice([a + b, a + b + r.randint(1, 5), abs(a - b) + r.randint(1, max(1, min(a, b) * 2 - 1)), a + b - 1])
        if c_ <= 0:
            return None
        ok = a + b > c_ and a + c_ > b and b + c_ > a
        q = "Can %d, %d and %d be the side lengths of a triangle?" % tuple(sorted((a, b, c_)))
        s = sorted((a, b, c_))
        right = "Yes" if ok else "No"
        e = "Triangle Inequality: the two shorter sides must add to more than the longest. %d + %d = %d, which is %s %d. <b>%s</b>." % (
            s[0], s[1], s[0] + s[1], "more than" if ok else ("equal to" if s[0] + s[1] == s[2] else "less than"), s[2], right)
        if s[0] + s[1] == s[2]:
            e += " (Equal sums make a flat line, not a triangle.)"
        return T(q, right, ["No" if ok else "Yes", "Only if it is a right triangle", "Only if two sides are equal"], e)
    if kind == "range":
        a, b = sorted(r.sample(range(3, 25), 2))
        q = "Two sides of a triangle are %d and %d. Which describes the possible lengths <i>x</i> of the third side?" % (a, b)
        right = "%d &lt; <i>x</i> &lt; %d" % (b - a, a + b)
        wr = ["%d &lt; <i>x</i> &lt; %d" % (a, b), "0 &lt; <i>x</i> &lt; %d" % (a + b), "%d ≤ <i>x</i> ≤ %d" % (b - a, a + b)]
        return T(q, right, wr, "The third side is longer than the difference and shorter than the sum: %d %s %d &lt; <i>x</i> &lt; %d + %d. <b>%s</b>." % (b, MINUS, a, a, b, right))
    L = r.sample("ABCDEFGHJKLMNPQRSTUVWXYZ", 3)
    s1, s2, s3 = sorted(r.sample(range(4, 30), 3))
    if s1 + s2 <= s3:
        return None
    # side opposite each vertex
    opp = {L[0]: s1, L[1]: s2, L[2]: s3}
    perm = r.sample(L, 3)
    sides = {"%s%s" % tuple(sorted([x for x in L if x != v])): opp[v] for v in L}
    desc = ", ".join("%s = %d" % (k, sides[k]) for k in sorted(sides))
    if r.random() < 0.5:
        q = "In △%s, %s. List the angles from smallest to largest." % ("".join(perm), desc)
        right = "∠%s, ∠%s, ∠%s" % (L[0], L[1], L[2])
        wr = ["∠%s, ∠%s, ∠%s" % (L[2], L[1], L[0]), "∠%s, ∠%s, ∠%s" % (L[1], L[0], L[2]), "∠%s, ∠%s, ∠%s" % (L[0], L[2], L[1])]
        e = "The smallest angle is opposite the shortest side, and the largest angle is opposite the longest side. <b>%s</b>." % right
    else:
        q = "In △%s, %s. Which angle is the largest?" % ("".join(perm), desc)
        right = "∠%s" % L[2]
        wr = ["∠%s" % L[0], "∠%s" % L[1], "They are all equal"]
        e = "The largest angle is opposite the longest side (%d). <b>%s</b>." % (s3, right)
    return T(q, right, wr, e)


def build():
    sets = [S("Triangle Midsegment Theorem", collect(one_mid, 20, R)),
            S("Perpendicular and angle bisectors", collect(one_bis, 20, R)),
            S("Centroid and medians", collect(one_cent, 20, R)),
            S("Name the center", collect(one_which, 20, R)),
            S("Triangle Inequality and side order", collect(one_ineq, 20, R))]
    body = lesson(
        "<p><b>Midsegment Theorem</b>: a segment joining the midpoints of two sides is parallel to the third side and <b>half</b> as long.</p>"
        "<p>A point on a <b>perpendicular bisector</b> is the same distance from the segment's endpoints. A point on an <b>angle bisector</b> is the same distance from the angle's sides.</p>"
        "<ul><li><b>Circumcenter</b>: perpendicular bisectors meet; same distance from the vertices.</li>"
        "<li><b>Incenter</b>: angle bisectors meet; same distance from the sides.</li>"
        "<li><b>Centroid</b>: medians meet; it is 2/3 of the way along each median from the vertex (AG = 2 × GM).</li>"
        "<li><b>Orthocenter</b>: altitudes meet.</li></ul>"
        "<p><b>Triangle Inequality</b>: any two sides add to more than the third. The longest side is opposite the largest angle.</p>",
        [("D and E are midpoints of two sides. DE = 3<i>x</i> + 1 and the third side is 8<i>x</i> %s 6. Find DE." % MINUS,
          ["2(3<i>x</i> + 1) = 8<i>x</i> %s 6" % MINUS, "6<i>x</i> + 2 = 8<i>x</i> %s 6, so <i>x</i> = 4" % MINUS], "DE = 13"),
         ("Two sides of a triangle are 7 and 12. What lengths can the third side have?", ["Bigger than 12 %s 7 = 5" % MINUS, "Smaller than 12 + 7 = 19"], "5 &lt; <i>x</i> &lt; 19")],
        ["Doubling the midsegment when you should halve it. The midsegment is the short one.",
         "Splitting a median in half at the centroid. The ratio is 2 : 1, with the long part at the vertex.",
         "Mixing up circumcenter (vertices) and incenter (sides).",
         "Accepting 3, 4, 7 as a triangle. 3 + 4 = 7 is not more than 7."])
    faq = [("What is the Triangle Midsegment Theorem?", "The segment joining the midpoints of two sides of a triangle is parallel to the third side and half its length."),
           ("What is the difference between the circumcenter and the incenter?",
            "The circumcenter is where the perpendicular bisectors meet and is equidistant from the vertices. The incenter is where the angle bisectors meet and is equidistant from the sides."),
           ("How far is the centroid along a median?", "Two thirds of the way from the vertex to the midpoint of the opposite side, so it splits the median in a 2 : 1 ratio."),
           ("What is the Triangle Inequality Theorem?", "The sum of any two side lengths of a triangle is greater than the third side length.")]
    make("midsegments-and-triangle-centers", 11, "G-CO.C.10",
         "Midsegments, Bisectors, and Triangle Centers",
         "Midsegment, Centroid and Triangle Centers Worksheet (Geometry) | 100 Questions with Answers",
         "Midsegments and Triangle Centers",
         "Prove theorems about triangles. Theorems include: measures of interior angles of a triangle sum to 180°; base angles of isosceles triangles are congruent; the segment joining midpoints of two sides of a triangle is parallel to the third side and half the length; the medians of a triangle meet at a point.",
         "Free Geometry worksheet on midsegments, perpendicular and angle bisectors, the centroid, circumcenter, incenter and the Triangle Inequality. 100 questions with answers.",
         "A midsegment is half the third side. The centroid splits each median 2 : 1.",
         "Any two sides of a triangle add to more than the third side.",
         body, faq, sets, R, domain="Triangles", grade="geometry")


if __name__ == "__main__":
    build()
