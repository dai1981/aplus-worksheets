# -*- coding: utf-8 -*-
"""
India Class 12 Maths, NCERT Chapter 4: Determinants (CBSE Unit II Algebra)
  python3 tools/gen_in_maths_c12_determinants.py
Determinants of order 2 and 3, solving for x in a determinant equation, singular matrices, minors and cofactors,
|kA| and |adj A|, the adjoint and inverse of a 2 × 2 matrix, area of a triangle and collinear points, and solving a
system of equations by the matrix method (own makers and US Precalculus makers).
Wrong answers come from real mistakes: ad + bc, forgetting the sign (−1)^(i + j) of a cofactor, |kA| = k|A| for an
n × n matrix, |adj A| = |A|, a negative area, and swapping the diagonal entries without changing the signs.
"""
import random
from fractions import Fraction as F
from in_sr import U, T2, use, X
from in_common import num, fv, comma
from pc_common import mat, det_h

R = random.Random(912104)
FX = [("Find A−1", "Find A<sup>−1</sup>")]
d2 = use(__import__("gen_us_math_pc_determinants_and_inverse_matrices"), "one_d2", R, FX)
d3 = use(__import__("gen_us_math_pc_determinants_and_inverse_matrices"), "one_d3", R, FX)
inv = use(__import__("gen_us_math_pc_determinants_and_inverse_matrices"), "one_inv", R, FX)
sys_ = use(__import__("gen_us_math_pc_determinants_and_inverse_matrices"), "one_sys", R, FX)
_app = use(__import__("gen_us_math_pc_determinants_and_inverse_matrices"), "one_app", R, FX)


def area(r):
    it = _app(r)
    return it if it and "area" in it["q"] else None


def M(rows):
    return mat([[num(v) if not isinstance(v, str) else v for v in row] for row in rows])


def D(rows):
    return det_h([[num(v) if not isinstance(v, str) else v for v in row] for row in rows])


def det(A):
    if len(A) == 2:
        return A[0][0] * A[1][1] - A[0][1] * A[1][0]
    return sum((-1) ** j * A[0][j] * det([row[:j] + row[j + 1:] for row in A[1:]]) for j in range(3))


def one_solve(r):
    x = r.choice([k for k in range(-6, 7) if k])
    a, b = r.randint(1, 4), r.randint(1, 4)
    k = r.randint(-5, 5)
    rhs = x * x * a - b * k
    # |x b; k x/a?| keep simple: |a·x  b ; k  x| = a x² − b k
    if r.random() < 0.5:
        L = [["%s" % ("" if a == 1 else a) + X, num(b)], [num(k), X]]
        val = rhs
        right = "±%s" % num(abs(x))
        return T2("Find %s if %s = %s." % (X, D(L), num(val)), right, [num(abs(x)), "±%s" % num(x * x), "±%s" % num(abs(x) + 1)],
                  "%s%s² − (%s) = %s, so %s² = %s and %s = <b>%s</b>." % ("" if a == 1 else a, X, num(b * k), num(val), X, num(x * x), X, right))
    p, q = r.randint(1, 6), r.choice([k for k in range(-6, 7) if k])
    s, t = r.randint(1, 6), r.choice([k for k in range(-6, 7) if k])
    if p * t - q * s == 0:
        return None
    # singular: |p q; s x| = 0 -> x = q s / p
    xv = F(q * s, p)
    return T2("For what value of %s is %s a singular matrix?" % (X, M([[p, q], [s, X]])), fv(xv), [fv(-xv), fv(F(p * s, q)), fv(F(q, s * p)) if F(q, s * p) not in (xv, -xv) else fv(xv + 1)],
              "Singular means the determinant is 0: %d%s − (%s) = 0, so %s = <b>%s</b>." % (p, X, num(q * s), X, fv(xv)))


def one_cof(r):
    A = [[r.randint(-5, 6) for _ in range(3)] for _ in range(3)]
    i, j = r.randint(1, 3), r.randint(1, 3)
    sub = [row[:j - 1] + row[j:] for k, row in enumerate(A) if k != i - 1]
    mn = det(sub)
    cf = (-1) ** (i + j) * mn
    if mn == 0 or (i + j) % 2 == 0 and r.random() < 0.5:
        return None
    if r.random() < 0.5:
        return T2("A = %s. Find the minor M<sub>%d%d</sub>." % (M(A), i, j), num(mn), [num(-mn), num(sub[0][0] * sub[1][1] + sub[0][1] * sub[1][0]), num(A[i - 1][j - 1])],
                  "Delete row %d and column %d: M<sub>%d%d</sub> = %s = <b>%s</b>." % (i, j, i, j, D(sub), num(mn)))
    return T2("A = %s. Find the cofactor A<sub>%d%d</sub>." % (M(A), i, j), num(cf), [num(-cf), num(A[i - 1][j - 1] * cf), num(sub[0][0] * sub[1][1] + sub[0][1] * sub[1][0]) if sub[0][0] * sub[1][1] + sub[0][1] * sub[1][0] not in (cf, -cf) else num(cf + 1)],
              "M<sub>%d%d</sub> = %s, and A<sub>%d%d</sub> = (−1)<sup>%d</sup> M<sub>%d%d</sub> = <b>%s</b>." % (i, j, num(mn), i, j, i + j, i, j, num(cf)))


def one_prop(r):
    n = r.choice([2, 3])
    d = r.choice([k for k in range(-6, 7) if k not in (0, 1, -1)])
    k = r.choice([2, 3, -2])
    t = r.choice(["kA", "adj", "inv", "AT", "Aadj"])
    if t == "kA":
        return T2("A is a square matrix of order %d with |A| = %s. Find |%sA|." % (n, num(d), num(k)), num(k ** n * d), [num(k * d), num(k ** (n + 1) * d), num(k + d)],
                  "Each of the %d rows is multiplied by %s, so |%sA| = (%s)<sup>%d</sup> × %s = <b>%s</b>." % (n, num(k), num(k), num(k), n, num(d), num(k ** n * d)))
    if t == "adj":
        return T2("A is a square matrix of order %d with |A| = %s. Find |adj A|." % (n, num(d)), num(d ** (n - 1)), [num(d), num(d ** n), num(n * d)],
                  "|adj A| = |A|<sup>n−1</sup> = (%s)<sup>%d</sup> = <b>%s</b>." % (num(d), n - 1, num(d ** (n - 1))))
    if t == "inv":
        return T2("A is invertible with |A| = %s. Find |A<sup>−1</sup>|." % num(d), fv(F(1, d)), [num(d), num(-d), fv(F(-1, d))],
                  "|A<sup>−1</sup>| = 1 ÷ |A| = <b>%s</b>." % fv(F(1, d)))
    if t == "AT":
        return T2("|A| = %s for a square matrix A. Find |A′|." % num(d), num(d), [num(-d), fv(F(1, d)), num(d * d)],
                  "A matrix and its transpose have the same determinant: <b>%s</b>." % num(d))
    I = "I"
    return T2("A is a square matrix of order %d with |A| = %s. What is A(adj A)?" % (n, num(d)), "%s%s" % (num(d), I), [I, "%s%s" % (num(d ** n), I), "adj A"],
              "A(adj A) = (adj A)A = |A| I = <b>%s I</b>." % num(d))


def one_adj(r):
    a, b, c, d = [r.randint(-6, 7) for _ in range(4)]
    dt = a * d - b * c
    if dt == 0:
        return None
    adj = [[d, -b], [-c, a]]
    return T2("Find adj A if A = %s." % M([[a, b], [c, d]]), M(adj), [M([[d, b], [c, a]]), M([[a, -b], [-c, d]]), M([[-d, b], [c, -a]])],
              "For a 2 × 2 matrix, swap the diagonal entries and change the signs of the other two: <b>%s</b>." % M(adj))


def one_coll(r):
    x1, y1 = r.randint(-5, 5), r.randint(-5, 5)
    dx, dy = r.choice([1, 2, -1, 3]), r.randint(-4, 4)
    t = r.choice([2, 3, -1])
    kk = y1 + t * dy
    return T2("Find k if the points (%s, %s), (%s, %s) and (%s, k) are collinear." % (num(x1), num(y1), num(x1 + dx), num(y1 + dy), num(x1 + t * dx)), num(kk),
              [num(-kk) if kk else "1", num(kk + dy), num(y1 - t * dy) if y1 - t * dy != kk else num(kk + 2)],
              "Collinear points make a triangle of area 0: setting the determinant to 0 gives <b>k = %s</b>." % num(kk))


U(12, 4, "determinants", 4, "II", "Determinants: Minors, Cofactors, Adjoint, Inverse and Area", "determinants",
  "Determinant of a square matrix (up to 3 × 3 matrices), minors, co-factors and applications of determinants in finding the area of a triangle; adjoint and inverse of a square matrix; consistency, inconsistency and number of solutions of a system of linear equations by examples, solving a system of linear equations in two or three variables (having unique solution) using the inverse of a matrix (summary of the CBSE syllabus)",
  "Class 12 Determinants worksheet (NCERT Chapter 4): determinants of order 2 and 3, singular matrices, minors and cofactors, |kA|, adjoint and inverse, area of a triangle and the matrix method. 100 questions with answers.",
  "A⁻¹ = (1/|A|) adj A, which exists only when |A| ≠ 0.", "|kA| = kⁿ|A| and |adj A| = |A|ⁿ⁻¹ for an n × n matrix.",
  "<ul><li>|a b; c d| = ad − bc. Expand a 3 × 3 determinant along any row or column.</li>"
  "<li>Minor M<sub>ij</sub>: delete row i and column j. Cofactor A<sub>ij</sub> = (−1)<sup>i+j</sup>M<sub>ij</sub>.</li>"
  "<li>adj A is the transpose of the matrix of cofactors; A(adj A) = |A| I; A<sup>−1</sup> = adj A ÷ |A| when |A| ≠ 0.</li>"
  "<li>Area of a triangle = ½|det| with rows (x<sub>i</sub>, y<sub>i</sub>, 1); the points are collinear when it is 0.</li>"
  "<li>AX = B has the unique solution X = A<sup>−1</sup>B when |A| ≠ 0.</li></ul>",
  [("Find |A| for A = [2 −3; 4 5].", ["ad − bc = 2 × 5 − (−3) × 4", "= 10 + 12"], "22")],
  ["Computing ad + bc instead of ad − bc.", "Forgetting the sign (−1)^(i + j) in a cofactor.", "Writing |3A| = 3|A| for a 3 × 3 matrix (it is 27|A|)."],
  [("When is a matrix singular?", "When its determinant is 0; then it has no inverse."),
   ("Does a 2 × 3 matrix have a determinant?", "No. Only square matrices have determinants.")],
  [("Determinants of order 2 and 3", [(d2, 8), (d3, 8), (one_solve, 4)]),
   ("Equations and singular matrices", [(one_solve, 14), (one_coll, 6)]),
   ("Minors and cofactors", [(one_cof, 16), (one_prop, 4)]),
   ("Adjoint and inverse", [(one_adj, 6), (inv, 8), (one_prop, 6)]),
   ("Area and systems of equations", [(area, 6), (sys_, 8), (one_prop, 6)])], 912104)
