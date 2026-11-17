# -*- coding: utf-8 -*-
"""
US Geometry: Dilations and Similar Figures (Common Core G-SRT.A.1, G-SRT.A.2)
  python3 tools/gen_us_math_ge_dilations_and_similarity.py
Dilations centered at the origin and at another point, scale factors, how perimeter and area change,
missing sides of similar polygons, and word problems with scale.
Wrong answers come from real mistakes: adding the scale factor instead of multiplying, dilating from the
origin when the center is another point, scaling area by k instead of k², and setting up the proportion
upside down.
"""
import random
from fractions import Fraction as F
from us_hs import B, S, make, lesson, collect, T, fig, num, MINUS, fr, People
from g8_common import grid_svg
from us_geo import RED, GREEN, BLUE

R = random.Random(93301)


def sg(n):
    n = F(n)
    return num(n) if n >= 0 else MINUS + num(-n)


def pt(p):
    return "(%s, %s)" % (sg(p[0]), sg(p[1]))


def kf(k):
    k = F(k)
    return num(k) if k.denominator == 1 else fr(k.numerator, k.denominator)


KS = [2, 3, 4, F(1, 2), F(1, 3), F(3, 2), F(5, 2), F(1, 4), F(2, 3)]


# ------------------------------------------------------------ set 1: dilations about the origin
def one_org(r):
    k = F(r.choice(KS))
    P = (r.randint(-8, 8), r.randint(-8, 8))
    if 0 in P or (k * P[0]).denominator > 1 or (k * P[1]).denominator > 1 or abs(k * P[0]) > 24:
        return None
    Q = (k * P[0], k * P[1])
    kind = r.choice(["img", "img", "k", "type"])
    if kind == "img":
        q = "Point A%s is dilated by a scale factor of %s with center at the origin. What are the coordinates of A′?" % (pt(P), B(kf(k)))
        wr = [(P[0] + k, P[1] + k), (P[0] / k, P[1] / k), (k * P[0], P[1])]
        wr = [w for w in wr if F(w[0]).denominator == 1 and F(w[1]).denominator == 1 or True]
        e = "Multiply both coordinates by %s: (%s × %s, %s × %s) = <b>%s</b>." % (kf(k), kf(k), sg(P[0]), kf(k), sg(P[1]), pt(Q))
        opts = [pt(w) for w in wr if "None" not in pt(w)]
        return T(q, pt(Q), [w for w in dict.fromkeys(opts) if w != pt(Q)][:3], e)
    if kind == "k":
        q = "A dilation centered at the origin maps A%s to A′%s. What is the scale factor?" % (pt(P), pt(Q))
        wr = [1 / k, Q[0] - P[0], k + 1]
        return T(q, kf(k), [w for w in dict.fromkeys(kf(x) for x in wr if x > 0) if w != kf(k)][:3] + ["%s1" % MINUS],
                 "Divide an image coordinate by the original: %s ÷ %s = <b>%s</b>." % (sg(Q[0]), "(%s)" % sg(P[0]) if P[0] < 0 else sg(P[0]), kf(k)))
    right = "An enlargement" if k > 1 else "A reduction"
    q = "A figure is dilated by a scale factor of %s. Is the image an enlargement or a reduction?" % B(kf(k))
    return T(q, right, ["A reduction" if k > 1 else "An enlargement", "Neither, it is congruent", "It depends on the center"],
             "A scale factor %s 1 makes the image %s. <b>%s</b>." % ("greater than" if k > 1 else "between 0 and", "larger" if k > 1 else "smaller", right))


# ------------------------------------------------------------ set 2: dilations about another point
def one_ctr(r):
    k = F(r.choice([2, 3, F(1, 2), F(3, 2)]))
    C = (r.randint(-4, 4), r.randint(-4, 4))
    P = (C[0] + r.randint(-4, 4) * 2, C[1] + r.randint(-4, 4) * 2)
    if P[0] == C[0] or P[1] == C[1] or C == (0, 0):
        return None
    Q = (C[0] + k * (P[0] - C[0]), C[1] + k * (P[1] - C[1]))
    if max(abs(Q[0]), abs(Q[1])) > 12:
        return None
    q = "Dilate A%s by a scale factor of %s with center C%s. Where is A′?" % (pt(P), B(kf(k)), pt(C))
    wr = [(k * P[0], k * P[1]), (C[0] + (P[0] - C[0]) / k, C[1] + (P[1] - C[1]) / k), (P[0] + k * (P[0] - C[0]), P[1] + k * (P[1] - C[1]))]
    e = ("Find the step from C to A: (%s, %s). Multiply it by %s: (%s, %s). Add it to C: <b>%s</b>." % (
        sg(P[0] - C[0]), sg(P[1] - C[1]), kf(k), sg(k * (P[0] - C[0])), sg(k * (P[1] - C[1])), pt(Q)))
    opts = [pt(w) for w in wr]
    return T(q, pt(Q), [w for w in dict.fromkeys(opts) if w != pt(Q) and "None" not in w][:3], e)


# ------------------------------------------------------------ set 3: scale factor, perimeter and area
def one_scale(r):
    k = F(r.choice([2, 3, 4, 5, F(1, 2), F(3, 2), F(5, 2), F(2, 3)]))
    kind = r.choice(["len", "k", "perim", "area", "area", "areak"])
    if kind == "len":
        L = r.randint(2, 18) * k.denominator
        q = "A segment of length %d is dilated by a scale factor of %s. How long is the image?" % (L, kf(k))
        ans = k * L
        return T(q, num(ans), [num(w) for w in dict.fromkeys([L + k, L / k, k * k * L]) if w != ans][:3], "Lengths are multiplied by the scale factor: %s × %d = <b>%s</b>." % (kf(k), L, num(ans)))
    if kind == "k":
        L = r.randint(2, 15) * k.denominator
        q = "A side of length %d becomes %s after a dilation. What is the scale factor?" % (L, num(k * L))
        return T(q, kf(k), [w for w in dict.fromkeys([kf(1 / k), num(k * L - L), kf(k * k)]) if w != kf(k)][:3],
                 "Scale factor = image ÷ original = %s ÷ %d = <b>%s</b>." % (num(k * L), L, kf(k)))
    if kind == "perim":
        P = r.randint(6, 40) * k.denominator
        q = "A polygon has perimeter %d. It is dilated by a scale factor of %s. What is the perimeter of the image?" % (P, kf(k))
        ans = k * P
        return T(q, num(ans), [num(w) for w in dict.fromkeys([k * k * P, P + k, P / k]) if w != ans][:3], "Perimeter is a length, so it is multiplied by %s: <b>%s</b>." % (kf(k), num(ans)))
    if kind == "area":
        A = r.randint(3, 30) * k.denominator ** 2
        q = "A polygon has area %d square units. It is dilated by a scale factor of %s. What is the area of the image?" % (A, kf(k))
        ans = k * k * A
        return T(q, "%s square units" % num(ans), ["%s square units" % num(w) for w in dict.fromkeys([k * A, 2 * k * A, A + k * k]) if w != ans][:3],
                 "Area is multiplied by the square of the scale factor: (%s)² × %d = %s × %d = <b>%s square units</b>." % (kf(k), A, kf(k * k), A, num(ans)))
    a, b = r.sample([2, 3, 4, 5, 6, 7], 2)
    if __import__("math").gcd(a, b) > 1:
        return None
    q = "Two similar figures have corresponding sides in the ratio %d : %d. What is the ratio of their areas?" % (a, b)
    right = "%d : %d" % (a * a, b * b)
    return T(q, right, ["%d : %d" % (a, b), "%d : %d" % (2 * a, 2 * b), "%d : %d" % (a ** 3, b ** 3)],
             "The ratio of areas is the square of the ratio of sides: %d² : %d² = <b>%s</b>." % (a, b, right))


# ------------------------------------------------------------ set 4: similar polygons
def one_poly(r):
    L1 = r.sample("ABCDEFGHJKLMNPQRSTUVWXYZ", 8)
    s1, s2 = "".join(L1[:4]), "".join(L1[4:])
    k = F(r.choice([2, 3, F(3, 2), F(5, 2), F(4, 3), F(1, 2), F(2, 3)]))
    sides = [r.randint(2, 12) * k.denominator for _ in range(4)]
    i, j = r.sample(range(4), 2)
    nm = lambda s, t: s[t] + s[(t + 1) % 4]
    known = sides[i]
    q = ("Quadrilateral %s ~ quadrilateral %s. %s = %d, %s = %s and %s = %d. Find %s." % (
        s1, s2, nm(s1, i), known, nm(s2, i), num(k * known), nm(s1, j), sides[j], nm(s2, j)))
    ans = k * sides[j]
    wr = [sides[j] / k, sides[j] + (k * known - known), known * sides[j] / (k * known)]
    e = ("The scale factor from %s to %s is %s ÷ %d = %s. %s = %s × %d = <b>%s</b>." % (s1, s2, num(k * known), known, kf(k), nm(s2, j), kf(k), sides[j], num(ans)))
    opts = [num(w) for w in wr]
    return T(q, num(ans), [w for w in dict.fromkeys(opts) if w != num(ans) and w is not None][:3] + [num(ans + 1)], e) if len(
        [w for w in dict.fromkeys(opts) if w != num(ans) and w is not None]) < 3 else T(q, num(ans), [w for w in dict.fromkeys(opts) if w != num(ans) and w is not None][:3], e)


# ------------------------------------------------------------ set 5: word problems
def one_word(r):
    pp = People(r)
    nm, he, his = pp.next()
    kind = r.choice(["photo", "photo", "map", "model", "pizza", "screen"])
    if kind == "photo":
        w, h = r.choice([(4, 6), (5, 7), (8, 10), (3, 5)])
        W = w * r.choice([2, 3, F(5, 2), 4])
        H = W * F(h, w)
        q = "%s enlarges a %d in. by %d in. photo so that the short side is %s in. How long is the long side?" % (nm, w, h, num(W))
        return T(q, "%s in." % num(H), ["%s in." % num(x) for x in dict.fromkeys([h + W - w, W * F(w, h), H + 2]) if x != H][:3],
                 "The scale factor is %s ÷ %d = %s. Long side = %s × %d = <b>%s in.</b>" % (num(W), w, num(F(W, w)), num(F(W, w)), h, num(H)))
    if kind == "map":
        sc = r.choice([2, 5, 10, 20, 25])
        d = r.choice([F(3, 2), F(5, 2), 3, 4, F(7, 2), 6])
        q = "On a map, 1 inch represents %d miles. Two cities are %s inches apart on the map. How far apart are they?" % (sc, num(d))
        ans = sc * d
        return T(q, "%s miles" % num(ans), ["%s miles" % num(x) for x in dict.fromkeys([sc + d, F(sc, 1) / d, ans * 2]) if x != ans][:3],
                 "Multiply by the scale: %s × %d = <b>%s miles</b>." % (num(d), sc, num(ans)))
    if kind == "model":
        k = r.choice([24, 48, 64, 72, 100])
        L = r.choice([F(3, 2), 2, F(5, 2), 3, 4, 5])
        q = "A model car is built at a scale of 1 : %d. The model is %s ft long. How long is the real car?" % (k, num(L))
        if k * L > 30:
            q = q.replace("model car", "model ship").replace("real car", "real ship")
        ans = k * L
        return T(q, "%s ft" % num(ans), ["%s ft" % num(x) for x in dict.fromkeys([k + L, F(k, 1) / L, ans / 12]) if x != ans and num(x)][:3],
                 "Every real length is %d times the model length: %d × %s = <b>%s ft</b>." % (k, k, num(L), num(ans)))
    if kind == "pizza":
        a, b = r.choice([(10, 15), (8, 12), (12, 16), (10, 14), (9, 12)])
        q = "A %d-inch pizza and a %d-inch pizza are similar circles. How many times as much pizza is the larger one?" % (a, b)
        ans = F(b * b, a * a)
        return T(q, kf(ans) if ans.denominator > 1 else num(ans), [kf(x) for x in dict.fromkeys([F(b, a), F(b * b * b, a * a * a), F(2 * b, a)]) if x != ans][:3],
                 "Areas scale by the square of the ratio: (%d ÷ %d)² = %d ÷ %d = <b>%s</b>." % (b, a, b * b, a * a, kf(ans)))
    w = r.choice([16, 20, 24, 32, 40])
    k = r.choice([F(3, 2), 2, F(5, 4), 3])
    q = "A rectangular screen %d in. wide is dilated by a scale factor of %s to make a larger screen. By what factor does the screen's area increase?" % (w, kf(k))
    return T(q, kf(k * k), [kf(x) for x in dict.fromkeys([k, 2 * k, k ** 3]) if x != k * k][:3],
             "Area scales by the square of the scale factor: (%s)² = <b>%s</b>." % (kf(k), kf(k * k)))


def build():
    sets = [S("Dilations centered at the origin", collect(one_org, 20, R)),
            S("Dilations with another center", collect(one_ctr, 20, R)),
            S("Scale factor, perimeter and area", collect(one_scale, 20, R)),
            S("Similar polygons", collect(one_poly, 20, R)),
            S("Word problems", collect(one_word, 20, R))]
    body = lesson(
        "<p>A <b>dilation</b> with center C and scale factor <i>k</i> moves every point along the ray from C, so its distance from C is multiplied by <i>k</i>. "
        "If <i>k</i> &gt; 1 it is an enlargement; if 0 &lt; <i>k</i> &lt; 1 it is a reduction.</p>"
        "<ul><li>Center at the origin: (<i>x</i>, <i>y</i>) → (<i>kx</i>, <i>ky</i>).</li>"
        "<li>Another center C: find the step from C to the point, multiply it by <i>k</i>, and add it to C.</li></ul>"
        "<p>Dilations keep angles the same and multiply every length by <i>k</i>, so the image is <b>similar</b> to the original. "
        "Perimeters multiply by <i>k</i>, but areas multiply by <i>k</i>².</p>",
        [("Dilate (6, 2) by a scale factor of 3 with center (2, 0).", ["Step from the center: (4, 2)", "Times 3: (12, 6)", "Add to (2, 0)"], "(14, 6)"),
         ("A triangle with area 20 is dilated by a scale factor of 3. Find the new area.", ["Area scales by 3² = 9"], "180")],
        ["Adding the scale factor to the coordinates. Multiply instead.",
         "Dilating from the origin when the center is another point.",
         "Multiplying area by <i>k</i>. Area changes by <i>k</i>².",
         "Writing the proportion upside down. Keep the same figure on top on both sides."])
    faq = [("What is a dilation in geometry?", "A transformation that enlarges or reduces a figure by a scale factor from a center point. The image is similar to the original."),
           ("How do you dilate a point about the origin?", "Multiply both coordinates by the scale factor: (x, y) → (kx, ky)."),
           ("How does a dilation change area?", "Area is multiplied by the square of the scale factor. A scale factor of 3 makes the area 9 times as large."),
           ("Are dilated figures congruent?", "No, unless the scale factor is 1. They are similar: same angles, proportional sides.")]
    make("dilations-and-similarity", 13, "G-SRT.A.2",
         "Dilations and Similar Figures",
         "Dilations and Similar Figures Worksheet: Scale Factor (Geometry, G-SRT.A.2) | 100 Questions",
         "Dilations and Similarity",
         "Given two figures, use the definition of similarity in terms of similarity transformations to decide if they are similar; explain using similarity transformations the meaning of similarity for triangles as the equality of all corresponding pairs of angles and the proportionality of all corresponding pairs of sides.",
         "Free Geometry worksheet on dilations and similar figures: scale factors, dilations about a center, perimeter and area changes, and similar polygons. 100 questions with answers.",
         "A dilation multiplies every length by the scale factor k.",
         "Perimeter changes by k; area changes by k².",
         body, faq, sets, R, domain="Similarity", grade="geometry")


if __name__ == "__main__":
    build()
