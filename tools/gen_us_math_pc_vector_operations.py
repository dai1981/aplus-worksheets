# -*- coding: utf-8 -*-
"""
US Precalculus: Vector Operations (Common Core N-VM.B.4, N-VM.B.5)
  python3 tools/gen_us_math_pc_vector_operations.py
Adding and subtracting vectors, scalar multiples and linear combinations, unit vectors and i, j notation,
the dot product and the angle between vectors, and resultant forces and velocities.
Wrong answers come from real mistakes: subtracting in the wrong order, multiplying only one component by
the scalar, dividing by the sum of the components instead of the magnitude, and adding magnitudes of
vectors that point in different directions.
"""
import math
import random
from fractions import Fraction as F
from us_hs import B, S, make, lesson, collect, T, num, MINUS, fr, People
from a2_common import sf
from pc_common import GRADE, vec, rt, surd

R = random.Random(97901)
U, V, W = "<b><i>u</i></b>", "<b><i>v</i></b>", "<b><i>w</i></b>"
IV, JV = "<b><i>i</i></b>", "<b><i>j</i></b>"
TRI = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (6, 8, 10), (7, 24, 25)]


def rv(r):
    return r.choice([1, -1]) * r.randint(1, 8), r.choice([1, -1]) * r.randint(0, 8)


def ij(a, b):
    out = ""
    if a:
        out = ("" if abs(a) == 1 else num(abs(a))) + IV
        if a < 0:
            out = MINUS + out
    if b:
        t = ("" if abs(b) == 1 else num(abs(b))) + JV
        out = (out + (" + " if b > 0 else " " + MINUS + " ") + t) if out else ((MINUS if b < 0 else "") + t)
    return out or "0"


def deg1(d):
    return num(F(round(d, 1)).limit_denominator(10)) + "°"


# ------------------------------------------------------------ set 1: add and subtract
def one_add(r):
    a, b = rv(r)
    c, d = rv(r)
    op = r.choice(["+", "−"])
    q = "If %s = %s and %s = %s, find %s %s %s." % (U, vec(a, b), V, vec(c, d), U, op, V)
    if op == "+":
        right = vec(a + c, b + d)
        wr = [vec(a - c, b - d), vec(a * c, b * d), vec(a + d, b + c)]
    else:
        right = vec(a - c, b - d)
        wr = [vec(c - a, d - b), vec(a + c, b + d), vec(a - c, d - b)]
    return T(q, right, wr, "Work component by component: <b>%s</b>." % right)


# ------------------------------------------------------------ set 2: scalars and linear combinations
def one_lin(r):
    a, b = rv(r)
    c, d = rv(r)
    k, m = r.choice([2, 3, 4, -2, 5]), r.choice([2, 3, -1, -3, 4])
    if r.random() < 0.3:
        q = "If %s = %s, find %s%s." % (V, vec(a, b), sf(k) if k != -1 else MINUS, V)
        right = vec(k * a, k * b)
        return T(q, right, [vec(k * a, b), vec(a + k, b + k), vec(-k * a, -k * b)], "Multiply each component by %s: <b>%s</b>." % (sf(k), right))
    q = "If %s = %s and %s = %s, find %s%s %s %s%s." % (U, vec(a, b), V, vec(c, d), sf(k), U, "+" if m > 0 else MINUS, "" if abs(m) == 1 else num(abs(m)), V)
    right = vec(k * a + m * c, k * b + m * d)
    wr = [vec(k * a - m * c, k * b - m * d), vec(k * a + m * c, b + m * d), vec(a + m * c, b + m * d)]
    cf = lambda t: MINUS if t == -1 else sf(t)
    return T(q, right, wr, "%s%s = %s and %s%s = %s. Add: <b>%s</b>." % (cf(k), U, vec(k * a, k * b), cf(m), V, vec(m * c, m * d), right))


# ------------------------------------------------------------ set 3: unit vectors and i, j
def one_unit(r):
    kind = r.choice(["unit", "unit", "ij", "ij", "mag"])
    if kind == "unit":
        if r.random() < 0.6:
            a, b, c = r.choice(TRI)
            a, b = a * r.choice([1, -1]), b * r.choice([1, -1])
            right = vec(F(a, c), F(b, c))
            wr = [vec(F(a, abs(a) + abs(b)), F(b, abs(a) + abs(b))), vec(F(c, a), F(c, b)), vec(F(-a, c), F(-b, c))]
            return T("Find the unit vector in the direction of %s = %s." % (V, vec(a, b)), right, wr,
                     "Divide by the magnitude ‖%s‖ = %d: <b>%s</b>." % (V, c, right))
        a, b = r.randint(1, 5) * r.choice([1, -1]), r.randint(1, 5) * r.choice([1, -1])
        s = a * a + b * b
        if math.isqrt(s) ** 2 == s:
            return None
        right = vec(surd(a, s, s), surd(b, s, s))
        wr = [vec(surd(a, 1, s), surd(b, 1, s)), vec(F(a, abs(a) + abs(b)), F(b, abs(a) + abs(b))), vec(surd(-a, s, s), surd(-b, s, s))]
        return T("Find the unit vector in the direction of %s = %s." % (V, vec(a, b)), right, wr,
                 "‖%s‖ = √%d. Divide each component by √%d and rationalize: <b>%s</b>." % (V, s, s, right))
    if kind == "ij":
        a, b = rv(r)
        if b == 0:
            return None
        if r.random() < 0.5:
            q = "Write %s = %s using %s and %s." % (V, vec(a, b), IV, JV)
            return T(q, ij(a, b), [ij(b, a), ij(-a, b), ij(a, -b)], "%s = ⟨1, 0⟩ and %s = ⟨0, 1⟩, so ⟨<i>a</i>, <i>b</i>⟩ = <i>a</i>%s + <i>b</i>%s. <b>%s</b>." % (IV, JV, IV, JV, ij(a, b)))
        c, d = rv(r)
        if d == 0:
            return None
        q = "Find (%s) + (%s)." % (ij(a, b), ij(c, d))
        right = ij(a + c, b + d)
        return T(q, right, [ij(a - c, b - d), ij(a + c, b - d), ij(a + d, b + c)], "Add the %s parts and the %s parts: <b>%s</b>." % (IV, JV, right))
    a, b, c = r.choice(TRI)
    a, b = a * r.choice([1, -1]), b * r.choice([1, -1])
    q = "Find the magnitude of %s." % ij(a, b)
    return T(q, str(c), [str(abs(a) + abs(b)), str(c * c), str(abs(abs(a) - abs(b)))], "√(%d + %d) = <b>%d</b>." % (a * a, b * b, c))


# ------------------------------------------------------------ set 4: dot product and angles
def one_dot(r):
    kind = r.choice(["dot", "dot", "orth", "angle", "angle"])
    a, b = rv(r)
    c, d = rv(r)
    if kind == "dot":
        q = "Find %s · %s if %s = %s and %s = %s." % (U, V, U, vec(a, b), V, vec(c, d))
        ans = a * c + b * d
        return T(q, sf(ans), [vec(a * c, b * d), sf(a * d + b * c) if a * d + b * c != ans else sf(ans + 1), sf(a * c - b * d) if a * c - b * d != ans else sf(-ans)],
                 "%s · %s = (%s)(%s) + (%s)(%s) = <b>%s</b>. The dot product is a number, not a vector." % (U, V, sf(a), sf(c), sf(b), sf(d), sf(ans)))
    if kind == "orth":
        k = r.choice([1, 2, 3, -1, -2])
        if r.random() < 0.5:
            c, d = -b * k, a * k
        if (a, b) == (0, 0) or (c, d) == (0, 0):
            return None
        dp = a * c + b * d
        q = "Are %s = %s and %s = %s orthogonal (perpendicular)?" % (U, vec(a, b), V, vec(c, d))
        right = "Yes, because %s · %s = 0" % (U, V) if dp == 0 else "No, because %s · %s = %s" % (U, V, sf(dp))
        wr = (["No, because %s · %s = 0" % (U, V), "Yes, because the vectors have the same length", "No, because the slopes are equal"] if dp == 0
              else ["Yes, because %s · %s = %s" % (U, V, sf(dp)), "Yes, because one component is negative", "Yes, because %s · %s = 0" % (U, V)])
        return T(q, right, wr, "Vectors are orthogonal exactly when their dot product is 0. %s · %s = %s. <b>%s</b>." % (U, V, sf(dp), right))
    if a * d - b * c == 0:
        return None
    nu, nv = math.hypot(a, b), math.hypot(c, d)
    ang = math.degrees(math.acos((a * c + b * d) / (nu * nv)))
    q = "Find the angle between %s = %s and %s = %s, to the nearest tenth of a degree." % (U, vec(a, b), V, vec(c, d))
    right = deg1(ang)
    wr = [deg1(180 - ang), deg1(abs(90 - ang)), num(F(round(math.radians(ang), 2)).limit_denominator(100)) + "°"]
    if len(set(wr + [right])) < 4 or right == deg1(90):
        return None
    return T(q, right, wr, "cos θ = (%s · %s)/(‖%s‖‖%s‖) = %s/(√%d · √%d), so θ = cos⁻¹(…) ≈ <b>%s</b>." % (U, V, U, V, sf(a * c + b * d), a * a + b * b, c * c + d * d, right))


# ------------------------------------------------------------ set 5: forces and velocities
def one_word(r):
    kind = r.choice(["perp", "perp", "angle", "equil", "plane"])
    if kind == "perp":
        a, b, c = r.choice(TRI)
        k = r.choice([5, 10, 20])
        q = "Two forces of %d N and %d N act on an object at right angles to each other. What is the magnitude of the resultant force?" % (a * k, b * k)
        return T(q, "%d N" % (c * k), ["%d N" % ((a + b) * k), "%d N" % ((b - a) * k if b > a else (a - b) * k), "%s N" % num(c * k * c * k)],
                 "The resultant is the sum of perpendicular vectors: √(%d² + %d²) = <b>%d N</b>. Magnitudes add only when the forces point the same way." % (a * k, b * k, c * k))
    if kind == "angle":
        f1, f2 = r.choice([30, 40, 50, 60]), r.choice([20, 40, 70, 80])
        d = r.choice([40, 50, 60, 70, 120])
        res = math.sqrt(f1 * f1 + f2 * f2 + 2 * f1 * f2 * math.cos(math.radians(d)))
        q = "Two forces of %d lb and %d lb act on an object with an angle of %d° between them. To the nearest tenth, what is the magnitude of the resultant?" % (f1, f2, d)
        right = num(F(round(res, 1)).limit_denominator(10)) + " lb"
        wrong_m = math.sqrt(max(0, f1 * f1 + f2 * f2 - 2 * f1 * f2 * math.cos(math.radians(d))))
        wr = ["%d lb" % (f1 + f2), num(F(round(wrong_m, 1)).limit_denominator(10)) + " lb", num(F(round(math.hypot(f1, f2), 1)).limit_denominator(10)) + " lb"]
        return T(q, right, wr, "Put one force along the <i>x</i>-axis: ⟨%d, 0⟩ + ⟨%d cos %d°, %d sin %d°⟩. The magnitude of the sum is √(%d² + %d² + 2 · %d · %d cos %d°) ≈ <b>%s</b>." % (
            f1, f2, d, f2, d, f1, f2, f1, f2, d, right))
    if kind == "equil":
        a, b = rv(r)
        c, d = rv(r)
        q = "Forces %s = %s and %s = %s act on an object. What third force %s keeps the object at rest?" % ("<b><i>F</i></b><sub>1</sub>", vec(a, b), "<b><i>F</i></b><sub>2</sub>", vec(c, d), "<b><i>F</i></b><sub>3</sub>")
        right = vec(-(a + c), -(b + d))
        if (a + c, b + d) == (0, 0):
            return None
        return T(q, right, [vec(a + c, b + d), vec(c - a, d - b), vec(-(a - c), -(b - d))], "The three forces must add to ⟨0, 0⟩, so %s = −(%s + %s) = <b>%s</b>." % (
            "<b><i>F</i></b><sub>3</sub>", "<b><i>F</i></b><sub>1</sub>", "<b><i>F</i></b><sub>2</sub>", right))
    sp = r.choice([300, 400, 450, 500])
    w = r.choice([30, 40, 50, 60])
    q = "A plane's velocity in still air is %s mph (east, north), and the wind's velocity is %s mph. What is the plane's resultant velocity?" % (vec(0, sp), vec(w, -w // 2))
    right = vec(w, sp - w // 2)
    return T(q, right + " mph", [vec(w, sp + w // 2) + " mph", vec(-w, sp + w // 2) + " mph", vec(w, sp) + " mph"], "Add the velocity vectors: ⟨0 + %d, %d + (%s)⟩ = <b>%s mph</b>." % (w, sp, sf(-w // 2), right))


def build():
    sets = [S("Adding and subtracting vectors", collect(one_add, 20, R)),
            S("Scalar multiples and combinations", collect(one_lin, 20, R)),
            S("Unit vectors and i, j notation", collect(one_unit, 20, R)),
            S("Dot product and angles", collect(one_dot, 20, R)),
            S("Forces and velocities", collect(one_word, 20, R))]
    body = lesson(
        "<ul><li>Add, subtract and multiply by a scalar <b>component by component</b>: ⟨<i>a</i>, <i>b</i>⟩ + ⟨<i>c</i>, <i>d</i>⟩ = ⟨<i>a</i> + <i>c</i>, <i>b</i> + <i>d</i>⟩ and <i>k</i>⟨<i>a</i>, <i>b</i>⟩ = ⟨<i>ka</i>, <i>kb</i>⟩.</li>"
        "<li>A <b>unit vector</b> has length 1: divide a vector by its magnitude. " + IV + " = ⟨1, 0⟩ and " + JV + " = ⟨0, 1⟩, so ⟨<i>a</i>, <i>b</i>⟩ = <i>a</i>" + IV + " + <i>b</i>" + JV + ".</li>"
        "<li><b>Dot product</b>: ⟨<i>a</i>, <i>b</i>⟩ · ⟨<i>c</i>, <i>d</i>⟩ = <i>ac</i> + <i>bd</i>, a number. The angle between vectors: cos θ = (" + U + " · " + V + ") / (‖" + U + "‖‖" + V + "‖). Dot product 0 means perpendicular.</li>"
        "<li>The <b>resultant</b> of forces or velocities is their vector sum. Add components, then find the magnitude.</li></ul>",
        [("If " + U + " = ⟨3, −2⟩ and " + V + " = ⟨−1, 4⟩, find 2" + U + " − 3" + V + ".", ["2" + U + " = ⟨6, −4⟩, 3" + V + " = ⟨−3, 12⟩", "⟨6 − (−3), −4 − 12⟩"], "⟨9, −16⟩"),
         ("Find the angle between ⟨1, 0⟩ and ⟨1, 1⟩.", ["Dot product 1", "cos θ = 1/(1 · √2)"], "45°")],
        ["Multiplying only the first component by the scalar.",
         "Dividing by <i>a</i> + <i>b</i> instead of the magnitude to make a unit vector.",
         "Writing the dot product as a vector. It is a single number.",
         "Adding the magnitudes of forces that are not in the same direction."])
    faq = [("How do you add vectors?", "Add the matching components: ⟨a, b⟩ + ⟨c, d⟩ = ⟨a + c, b + d⟩. Geometrically, place them tip to tail."),
           ("How do you find a unit vector?", "Divide the vector by its magnitude. For ⟨3, 4⟩, the unit vector is ⟨3/5, 4/5⟩."),
           ("What does the dot product tell you?", "It gives the angle between two vectors through cos θ = (u · v)/(|u||v|). A dot product of 0 means the vectors are perpendicular."),
           ("What is a resultant force?", "The single force equal to the vector sum of all the forces acting on an object.")]
    make("vector-operations", 9, "N-VM.B.4",
         "Vector Operations",
         "Vector Operations Worksheet: Addition, Scalars, Unit Vectors, Dot Product | 100 Questions",
         "Vector Operations",
         "Add and subtract vectors. Multiply a vector by a scalar.",
         "Free precalculus worksheet on vector operations: adding and subtracting, scalar multiples, unit vectors, i and j notation, the dot product, angles and resultant forces. 100 questions.",
         "Work component by component.",
         "Unit vector: divide by the magnitude. Dot product 0 means perpendicular.",
         body, faq, sets, R, domain="Vectors and Matrices", grade=GRADE)


if __name__ == "__main__":
    build()
