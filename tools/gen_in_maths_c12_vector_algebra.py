# -*- coding: utf-8 -*-
"""
India Class 12 Maths, NCERT Chapter 10: Vector Algebra (CBSE Unit IV Vectors and Three-Dimensional Geometry)
  python3 tools/gen_in_maths_c12_vector_algebra.py
Vectors in î, ĵ, k̂ form: magnitude, unit vectors, direction cosines, the vector joining two points, the section
formula, collinear vectors, the scalar (dot) product, the angle between vectors, projection, perpendicular vectors,
the vector (cross) product and areas of parallelograms and triangles (own makers).
Wrong answers come from real mistakes: adding the components for the magnitude, A − B for the vector AB, a·b as a
vector, |a × b| without the square root, and forgetting the ½ for a triangle.
"""
import random, math
from fractions import Fraction as F
from in_sr import U, T2, rt, surd, I_, J_, K_
from in_common import num, fv

R = random.Random(912110)
QUAD = [(1, 2, 2, 3), (2, 3, 6, 7), (1, 4, 8, 9), (4, 4, 7, 9), (2, 6, 9, 11), (6, 6, 7, 11), (3, 4, 12, 13), (2, 10, 11, 15), (1, 12, 12, 17), (2, 2, 1, 3)]
A_, B_ = "<b><i>a</i></b>", "<b><i>b</i></b>"


def vec(a, b, c):
    out = ""
    for v, u in ((a, I_), (b, J_), (c, K_)):
        if v == 0:
            continue
        mag = "" if abs(v) == 1 else num(abs(v))
        if not out:
            out = ("−" if v < 0 else "") + mag + u
        else:
            out += " %s %s%s" % ("−" if v < 0 else "+", mag, u)
    return out or "<b>0</b>"


def qv(r):
    a, b, c, d = r.choice(QUAD)
    xs = [a, b, c]
    r.shuffle(xs)
    return [x * r.choice([1, -1]) for x in xs], d


def one_mag(r):
    k = r.choice(["mag", "unit", "dc", "ab"])
    v, d = qv(r)
    if k == "mag":
        return T2("Find the magnitude of %s = %s." % (A_, vec(*v)), str(d), [str(sum(abs(x) for x in v)), str(d * d), rt(abs(sum(v))) if abs(sum(v)) not in (d, sum(abs(x) for x in v), 0) else str(d + 1)],
                  "|%s| = √(%s) = √%d = <b>%d</b>." % (A_, " + ".join("%d²" % abs(x) for x in v), d * d, d))
    if k == "unit":
        right = "(1/%d)(%s)" % (d, vec(*v))
        return T2("Find the unit vector in the direction of %s = %s." % (A_, vec(*v)), right, ["(1/%d)(%s)" % (d * d, vec(*v)), "(1/%d)(%s)" % (sum(abs(x) for x in v), vec(*v)), "%d(%s)" % (d, vec(*v))],
                  "â = %s ÷ |%s| = <b>%s</b>." % (A_, A_, right))
    if k == "dc":
        right = ", ".join(fv(F(x, d)) for x in v)
        return T2("Find the direction cosines of %s = %s." % (A_, vec(*v)), right, [", ".join(num(x) for x in v), ", ".join(fv(F(x, d * d)) for x in v), ", ".join(fv(F(abs(x), d)) for x in v) if any(x < 0 for x in v) else ", ".join(fv(F(x, sum(v))) for x in v) if sum(v) else ", ".join(fv(F(x, d + 1)) for x in v)],
                      "Direction cosines are the components divided by |%s| = %d: <b>%s</b>." % (A_, d, right))
    P = [r.randint(-5, 5) for _ in range(3)]
    Q = [p + x for p, x in zip(P, v)]
    pt = lambda z: "(%s, %s, %s)" % tuple(num(t) for t in z)
    return T2("P = %s and Q = %s. Find the vector PQ and its magnitude." % (pt(P), pt(Q)), "%s, magnitude %d" % (vec(*v), d),
              ["%s, magnitude %d" % (vec(*[-x for x in v]), d), "%s, magnitude %d" % (vec(*[p + q for p, q in zip(P, Q)]), d), "%s, magnitude %d" % (vec(*v), sum(abs(x) for x in v))],
              "PQ = Q − P = <b>%s</b>, and |PQ| = %d." % (vec(*v), d))


def one_sect(r):
    P = [r.randint(-6, 6) for _ in range(3)]
    Q = [r.randint(-6, 6) for _ in range(3)]
    m, n = r.choice([(1, 1), (1, 2), (2, 1), (1, 3), (3, 1), (2, 3), (3, 2)])
    if any((m * q + n * p) % (m + n) for p, q in zip(P, Q)):
        return None
    S = [(m * q + n * p) // (m + n) for p, q in zip(P, Q)]
    W = [(n * q + m * p) // (m + n) if (n * q + m * p) % (m + n) == 0 else None for p, q in zip(P, Q)]
    if S == P or S == Q:
        return None
    ex = [(m * q - n * p) // (m - n) if m != n and (m * q - n * p) % (m - n) == 0 else None for p, q in zip(P, Q)]
    wr = [vec(*W) if None not in W and W != S else vec(*[p + q for p, q in zip(P, Q)]), vec(*ex) if None not in ex and ex != S else vec(*[q - p for p, q in zip(P, Q)]), vec(*[x + 1 for x in S])]
    what = "the midpoint of PQ" if m == n else "the point R dividing PQ internally in the ratio %d : %d" % (m, n)
    return T2("P and Q have position vectors %s and %s. Find the position vector of %s." % (vec(*P), vec(*Q), what), vec(*S), wr,
              "R = (%s Q + %s P) ÷ %d = <b>%s</b>." % ("" if m == 1 else m, "" if n == 1 else n, m + n, vec(*S)))


def one_dot(r):
    k = r.choice(["dot", "perp", "angle", "proj"])
    a = [r.randint(-5, 5) for _ in range(3)]
    b = [r.randint(-5, 5) for _ in range(3)]
    dot = sum(x * y for x, y in zip(a, b))
    if k == "dot":
        return T2("%s = %s and %s = %s. Find %s · %s." % (A_, vec(*a), B_, vec(*b), A_, B_), num(dot), [vec(*[x * y for x, y in zip(a, b)]), num(sum(abs(x * y) for x, y in zip(a, b))) if sum(abs(x * y) for x, y in zip(a, b)) != dot else num(dot + 1), num(sum(a) * sum(b)) if sum(a) * sum(b) != dot else num(dot - 1)],
                  "%s · %s = %s = <b>%s</b>." % (A_, B_, " + ".join("(%s)(%s)" % (num(x), num(y)) for x, y in zip(a, b)), num(dot)))
    if k == "perp":
        if b[2] == 0:
            return None
        part = a[0] * b[0] + a[1] * b[1]
        lam = F(-part, b[2])
        if lam.denominator != 1:
            return None
        A = [a[0], a[1], "λ"]
        s = vec(a[0], a[1], 1).replace(K_, "λ" + K_) if True else ""
        s = vec(a[0], a[1], 0) + " + λ" + K_
        return T2("Find λ if %s and %s are perpendicular." % (s, vec(*b)), num(lam), [num(-lam) if lam else "1", num(part) if part != lam else num(lam + 1), fv(F(part, b[2])) if F(part, b[2]) not in (lam, -lam) else num(lam + 2)],
                  "Perpendicular vectors have dot product 0: %s + %sλ = 0, so <b>λ = %s</b>." % (num(part), num(b[2]), num(lam)))
    if k == "angle":
        case = r.choice([("90°", 0), ("60°", F(1, 2)), ("120°", F(-1, 2)), ("45°", None)])
        if case[1] == 0:
            u = [r.randint(1, 4), r.randint(-3, 3), 0]
            w = [-u[1], u[0], r.randint(-3, 3)]
        elif case[1] is None:
            t = r.randint(1, 4)
            u, w = [t, 0, 0], [t, t, 0]
            r.shuffle(u)
        else:
            t = r.randint(1, 3)
            u, w = [t, t, 0], [0, t, t] if case[1] > 0 else [0, -t, -t]
        right = case[0]
        return T2("Find the angle between %s and %s." % (vec(*u), vec(*w)), right, [x for x in ["30°", "45°", "60°", "90°", "120°", "135°"] if x != right][:3],
                  "cos θ = (%s · %s) ÷ (|%s||%s|) = %s, so <b>θ = %s</b>." % (A_, B_, A_, B_, {"90°": "0", "60°": "1/2", "120°": "−1/2", "45°": "1/√2"}[right], right))
    bq, d = qv(r)
    p = F(sum(x * y for x, y in zip(a, bq)), d)
    if p == 0:
        return None
    return T2("Find the projection of %s = %s on %s = %s." % (A_, vec(*a), B_, vec(*bq)), fv(p), [num(sum(x * y for x, y in zip(a, bq))), fv(p / d), fv(-p)],
              "Projection = (%s · %s) ÷ |%s| = %s ÷ %d = <b>%s</b>." % (A_, B_, B_, num(sum(x * y for x, y in zip(a, bq))), d, fv(p)))


def cross(a, b):
    return [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]


def one_cross(r):
    a = [r.randint(-3, 4) for _ in range(3)]
    b = [r.randint(-3, 4) for _ in range(3)]
    c = cross(a, b)
    if c == [0, 0, 0]:
        return None
    n2 = sum(x * x for x in c)
    k = r.choice(["cross", "para", "tri", "basis"])
    if k == "cross":
        return T2("%s = %s and %s = %s. Find %s × %s." % (A_, vec(*a), B_, vec(*b), A_, B_), vec(*c), [vec(*[-x for x in c]), vec(*[x * y for x, y in zip(a, b)]), vec(c[0], -c[1], c[2]) if c[1] else vec(c[0] + 1, c[1], c[2])],
                  "Expand the determinant with rows (î, ĵ, k̂), (%s), (%s): <b>%s</b>." % (", ".join(num(x) for x in a), ", ".join(num(x) for x in b), vec(*c)))
    if k == "para":
        return T2("Find the area of the parallelogram with adjacent sides %s and %s." % (vec(*a), vec(*b)), rt(n2) + " sq units",
                  [str(n2) + " sq units", "(1/2)" + rt(n2) + " sq units", num(abs(sum(x * y for x, y in zip(a, b)))) + " sq units" if abs(sum(x * y for x, y in zip(a, b))) != math.isqrt(n2) or math.isqrt(n2) ** 2 != n2 else rt(n2 + 1) + " sq units"],
                  "%s × %s = %s, so the area is |%s × %s| = √%d = <b>%s sq units</b>." % (A_, B_, vec(*c), A_, B_, n2, rt(n2)))
    if k == "tri":
        def part(fr_):
            a_, b_ = surd(n2)
            c_ = F(a_) * fr_
            if b_ == 1:
                return fv(c_)
            return ("" if c_ == 1 else fv(c_)) + "√%d" % b_
        right = part(F(1, 2)) + " sq units"
        return T2("Find the area of the triangle with two sides %s and %s." % (vec(*a), vec(*b)), right,
                  [rt(n2) + " sq units", fv(F(n2, 2)) + " sq units", part(F(1, 4)) + " sq units"],
                  "Area = ½|%s × %s| = ½ × %s = <b>%s</b>." % (A_, B_, rt(n2), right))
    pairs = [(I_ + " × " + J_, K_), (J_ + " × " + K_, I_), (K_ + " × " + I_, J_), (J_ + " × " + I_, "−" + K_), (K_ + " × " + J_, "−" + I_), (I_ + " × " + K_, "−" + J_)]
    q, ans = r.choice(pairs)
    return T2("What is %s?" % q, ans, [w for w in [K_, "−" + K_, I_, "−" + I_, J_, "−" + J_, "0"] if w != ans and w.strip("−") != ans.strip("−")][:2] + ["0" if ans != "0" else "1"],
              "Going round î → ĵ → k̂ → î gives +; going the other way gives −: <b>%s</b>." % ans)


def one_coll(r):
    a = [r.choice([k for k in range(-4, 5) if k]) for _ in range(3)]
    t = r.choice([2, 3, -2, F(1, 2), -1])
    b = [x * t for x in a]
    if any(F(x).denominator != 1 for x in b):
        return None
    j = r.randrange(3)
    shown = [num(x) for x in b]
    shown[j] = "λ"
    sb = " + ".join("%s%s" % (s_, u) for s_, u in zip(shown, (I_, J_, K_))).replace("+ −", "− ")
    return T2("Find λ if %s and %s are collinear." % (vec(*a), sb), num(b[j]), [num(-b[j]), num(a[j]), num(b[j] + a[j])],
              "Collinear vectors are multiples of each other: the scale factor is %s, so <b>λ = %s</b>." % (num(t) if F(t).denominator == 1 else fv(t), num(b[j])))


U(12, 10, "vector-algebra", 10, "V3", "Vector Algebra: Magnitude, Dot Product, Cross Product and Areas", "vector algebra",
  "Vectors and scalars, magnitude and direction of a vector; direction cosines and direction ratios of a vector; types of vectors (equal, unit, zero, parallel and collinear vectors), position vector of a point, negative of a vector, components of a vector, addition of vectors, multiplication of a vector by a scalar, position vector of a point dividing a line segment in a given ratio; definition, geometrical interpretation, properties and application of scalar (dot) product of vectors, vector (cross) product of vectors (summary of the CBSE syllabus)",
  "Class 12 Vector Algebra worksheet (NCERT Chapter 10): magnitude, unit vectors, direction cosines, section formula, dot product, angle, projection, cross product and areas. 100 questions with answers.",
  "a · b = |a||b| cos θ is a number; a × b is a vector.", "Area of a parallelogram = |a × b|; of a triangle = ½|a × b|.",
  "<ul><li>For <b><i>a</i></b> = x î + y ĵ + z k̂: |<b><i>a</i></b>| = √(x² + y² + z²); unit vector â = <b><i>a</i></b> ÷ |<b><i>a</i></b>|; direction cosines x/|<b><i>a</i></b>|, y/|<b><i>a</i></b>|, z/|<b><i>a</i></b>|.</li>"
  "<li>Vector AB = (position vector of B) − (position vector of A). The point dividing AB in the ratio m : n is (m<b>b</b> + n<b>a</b>) ÷ (m + n).</li>"
  "<li><b><i>a</i></b> · <b><i>b</i></b> = a<sub>1</sub>b<sub>1</sub> + a<sub>2</sub>b<sub>2</sub> + a<sub>3</sub>b<sub>3</sub> = |<b><i>a</i></b>||<b><i>b</i></b>| cos θ; perpendicular vectors have <b><i>a</i></b> · <b><i>b</i></b> = 0. Projection of <b><i>a</i></b> on <b><i>b</i></b> = <b><i>a</i></b> · <b><i>b</i></b> ÷ |<b><i>b</i></b>|.</li>"
  "<li><b><i>a</i></b> × <b><i>b</i></b> is found from a determinant; |<b><i>a</i></b> × <b><i>b</i></b>| is the area of the parallelogram on <b><i>a</i></b> and <b><i>b</i></b>.</li></ul>",
  [("Find the angle between î + ĵ and ĵ + k̂.", ["Dot product = 0 + 1 + 0 = 1", "|a| = |b| = √2, so cos θ = 1/2"], "60°")],
  ["Adding the components to get the magnitude.", "Writing the vector AB as A − B.", "Forgetting the ½ for the area of a triangle."],
  [("Is a · b a vector?", "No. The dot product is a number; the cross product is a vector."),
   ("What is î × î?", "The zero vector, because the angle between them is 0.")],
  [("Magnitude, unit vectors and direction cosines", [(one_mag, 20)]),
   ("Section formula and collinear vectors", [(one_sect, 12), (one_coll, 8)]),
   ("Dot product, angle and projection", [(one_dot, 20)]),
   ("Cross product and area", [(one_cross, 20)]),
   ("Mixed problems", [(one_dot, 8), (one_cross, 6), (one_mag, 6)])], 912110)
