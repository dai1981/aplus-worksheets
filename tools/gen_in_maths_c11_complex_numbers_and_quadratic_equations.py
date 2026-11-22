# -*- coding: utf-8 -*-
"""
India Class 11 Maths, NCERT Chapter 4: Complex Numbers and Quadratic Equations (CBSE Unit II Algebra)
  python3 tools/gen_in_maths_c11_complex_numbers_and_quadratic_equations.py
Powers of i, real and imaginary parts, equality of complex numbers, adding, multiplying and dividing, the conjugate,
modulus and multiplicative inverse, the Argand plane, and quadratic equations with non-real roots (own makers and
US Algebra 2 / Precalculus / TX Algebra II makers).
Wrong answers come from real mistakes: i² = 1, √−a · √−b = √(ab), forgetting to multiply by the conjugate,
|a + ib| = a + b, and missing the ± in the roots.
"""
import random
from fractions import Fraction as F
from in_sr import U, T2, use, X
from in_common import num, fv
import gen_us_math_a2_complex_numbers as uc
import gen_us_math_pc_complex_numbers_in_polar_form as pc
import gen_ustx_math_a2_complex_numbers as tx

R = random.Random(911104)
FX = [("Quadrant IV", "the fourth quadrant"), ("Quadrant III", "the third quadrant"), ("Quadrant II", "the second quadrant"), ("Quadrant I", "the first quadrant"),
      ("complex plane", "Argand plane"), ("nonreal", "non-real"), ("complex conjugate", "conjugate")]
powi = use(uc, "one_i", R, FX)
add = use(uc, "one_add", R, FX)
mul = use(uc, "one_mul", R, FX)
div = use(uc, "one_div", R, FX)
quad = use(uc, "one_quad", R, FX)
sq = use(tx, "one_sq", R, FX)
_plane = use(pc, "one_plane", R, FX)
_mod = use(pc, "one_mod", R, FX)


def plane(r):
    it = _plane(r)
    return None if it is None or "cos" in it["q"] else it


def modz(r):
    it = _mod(r)
    return None if it is None or "argument" in it["q"] else it


def cz(a, b):
    """a + ib as text"""
    a, b = F(a), F(b)
    if b == 0:
        return fv(a)
    bi = ("" if abs(b) == 1 else fv(abs(b))) + "<i>i</i>"
    if a == 0:
        return ("−" if b < 0 else "") + bi
    return "%s %s %s" % (fv(a), "−" if b < 0 else "+", bi)


TRIPLES = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (6, 8, 10), (7, 24, 25), (1, 1, None), (2, 1, None), (1, 2, None), (3, 1, None), (2, 3, None)]


def one_parts(r):
    a, b = r.randint(-9, 9), r.choice([k for k in range(-9, 10) if k])
    c, d = r.randint(-6, 6), r.choice([k for k in range(-6, 7) if k])
    re_, im = a * c - b * d, a * d + b * c
    if r.random() < 0.5:
        return T2("Find the real part of (%s)(%s)." % (cz(a, b), cz(c, d)), num(re_), [num(a * c + b * d), num(im), num(a * c)],
                  "(%s)(%s) = %s, using <i>i</i>² = −1. The real part is <b>%s</b>." % (cz(a, b), cz(c, d), cz(re_, im), num(re_)))
    return T2("Find the imaginary part of (%s)(%s)." % (cz(a, b), cz(c, d)), num(im), [num(re_), cz(0, im), num(b * d)],
              "(%s)(%s) = %s. The imaginary part is the real number <b>%s</b> (not %s)." % (cz(a, b), cz(c, d), cz(re_, im), num(im), cz(0, im)))


def one_equal(r):
    x, y = r.randint(-8, 9), r.randint(-8, 9)
    p, q = r.randint(1, 4), r.randint(1, 4)
    s, t = r.randint(-6, 6), r.randint(-6, 6)
    lhs = "(%s%s%s) + <i>i</i>(%s<i>y</i>%s)" % ("" if p == 1 else p, X, "" if s == 0 else (" + %d" % s if s > 0 else " − %d" % -s),
                                                 "" if q == 1 else q, "" if t == 0 else (" + %d" % t if t > 0 else " − %d" % -t))
    A, B = p * x + s, q * y + t
    return T2("Find real numbers %s and <i>y</i> if %s = %s." % (X, lhs, cz(A, B)), "%s = %s, <i>y</i> = %s" % (X, num(x), num(y)),
              ["%s = %s, <i>y</i> = %s" % (X, num(y), num(x)), "%s = %s, <i>y</i> = %s" % (X, num(A), num(B)), "%s = %s, <i>y</i> = %s" % (X, num(x), num(-y))],
              "Equal complex numbers have equal real parts and equal imaginary parts: %s = %s and %s = %s, so <b>%s = %s, <i>y</i> = %s</b>." % (
                  lhs.split(") + ")[0][1:], num(A), lhs.split("<i>i</i>(")[1][:-1], num(B), X, num(x), num(y)))


def one_inv(r):
    a, b, m = r.choice([t for t in TRIPLES])
    a, b = a * r.choice([1, -1]), b * r.choice([1, -1])
    if r.random() < 0.5:
        n2 = a * a + b * b
        mod = m if m else None
        if r.random() < 0.5 and mod:
            return T2("Find |%s|." % cz(a, b), num(mod), [num(abs(a) + abs(b)), num(n2), num(abs(a - b)) if abs(a - b) not in (mod, abs(a) + abs(b), n2) else num(mod + 1)],
                      "|a + <i>i</i>b| = √(a² + b²) = √%d = <b>%d</b>." % (n2, mod))
        return T2("Find the multiplicative inverse of %s." % cz(a, b), cz(F(a, n2), F(-b, n2)),
                  [cz(F(1, a) if a else 0, F(-1, b)), cz(F(a, n2), F(b, n2)), cz(-a, b)],
                  "z<sup>−1</sup> = z̄ ÷ |z|² = (%s) ÷ %d = <b>%s</b>." % (cz(a, -b), n2, cz(F(a, n2), F(-b, n2))))
    c = r.choice([2, 3, 5, 10])
    return T2("Express (%s) ÷ (%s) in the form a + <i>i</i>b." % (cz(a * c, b * c), cz(a, b)) if False else "Find the conjugate of (%s)<sup>2</sup>." % cz(a, b),
              cz(a * a - b * b, -2 * a * b), [cz(a * a - b * b, 2 * a * b), cz(a * a + b * b, -2 * a * b), cz(a * a, -b * b)],
              "(%s)² = %s, so its conjugate is <b>%s</b>." % (cz(a, b), cz(a * a - b * b, 2 * a * b), cz(a * a - b * b, -2 * a * b)))


def one_roots(r):
    k = r.choice(["pure", "full", "full"])
    if k == "pure":
        a, n = r.choice([1, 2, 3, 4]), r.randint(1, 9)
        return T2("Solve %s%s² + %d = 0." % ("" if a == 1 else a, X, a * n * n), "%s = ±%s" % (X, cz(0, n)), ["%s = ±%d" % (X, n), "%s = %s" % (X, cz(0, n)), "%s = ±%s" % (X, cz(0, n * n))],
                  "%s² = −%d, so %s = ±√(−%d) = <b>±%s</b>." % (X, n * n, X, n * n, cz(0, n)))
    p, q = r.randint(-5, 5), r.randint(1, 5)
    if p == 0:
        return None
    b, c = -2 * p, p * p + q * q
    eq = "%s² %s %s%s + %d = 0" % (X, "−" if b < 0 else "+", "" if abs(b) == 1 else abs(b), X, c)
    root = lambda u, w: "%s = %s ± %s" % (X, num(u), cz(0, w))
    return T2("Solve %s." % eq, root(p, q), [root(-p, q), "%s = %s ± %d" % (X, num(p), q), "%s = %s" % (X, cz(p, q))],
              "D = b² − 4ac = %d − %d = %d &lt; 0, so the roots are (−b ± √D) ÷ 2a = <b>%s</b>." % (b * b, 4 * c, b * b - 4 * c, root(p, q).split(" = ")[1]))


U(11, 4, "complex-numbers-and-quadratic-equations", 4, "II", "Complex Numbers and Quadratic Equations: i, Conjugate, Modulus and Argand Plane", "complex numbers",
  "Need for complex numbers, especially √−1, to be motivated by inability to solve some of the quadratic equations; algebraic properties of complex numbers; Argand plane (summary of the CBSE syllabus)",
  "Class 11 Complex Numbers worksheet (NCERT Chapter 4): powers of i, real and imaginary parts, equality, operations, conjugate, modulus, multiplicative inverse, Argand plane and quadratic equations. 100 questions with answers.",
  "i² = −1, so a quadratic with D &lt; 0 has two complex roots.", "Divide by multiplying top and bottom by the conjugate.",
  "<ul><li><i>i</i> = √−1, so <i>i</i>² = −1, <i>i</i>³ = −<i>i</i>, <i>i</i>⁴ = 1. Powers of <i>i</i> repeat every 4.</li>"
  "<li>z = a + <i>i</i>b has real part a and imaginary part b. Two complex numbers are equal when both parts are equal.</li>"
  "<li>Conjugate z̄ = a − <i>i</i>b; modulus |z| = √(a² + b²); z z̄ = |z|²; z<sup>−1</sup> = z̄ ÷ |z|².</li>"
  "<li>For a<i>x</i>² + b<i>x</i> + c = 0 with D = b² − 4ac &lt; 0, <i>x</i> = (−b ± <i>i</i>√−D) ÷ 2a.</li></ul>",
  [("Express (3 + 2<i>i</i>) ÷ (1 − <i>i</i>) in the form a + <i>i</i>b.", ["Multiply top and bottom by 1 + <i>i</i>", "(3 + 2<i>i</i>)(1 + <i>i</i>) = 1 + 5<i>i</i>; (1 − <i>i</i>)(1 + <i>i</i>) = 2"], "1/2 + (5/2)<i>i</i>")],
  ["Writing √−4 · √−9 = √36 = 6 (it is −6).", "Giving the imaginary part as 3<i>i</i> instead of 3.", "Taking |3 + 4<i>i</i>| = 7."],
  [("What is the imaginary part of 5 − 2i?", "−2. The imaginary part is a real number."), ("Can a complex number be real?", "Yes, when its imaginary part is 0.")],
  [("Powers of i and parts", [(powi, 10), (one_parts, 10)]),
   ("Equality and addition", [(one_equal, 8), (add, 12)]),
   ("Multiplying and dividing", [(mul, 8), (sq, 6), (div, 6)]),
   ("Conjugate, modulus and inverse", [(one_inv, 12), (modz, 3), (plane, 5)]),
   ("Quadratic equations", [(one_roots, 12), (quad, 8)])], 911104)
