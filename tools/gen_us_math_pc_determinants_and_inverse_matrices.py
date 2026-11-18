# -*- coding: utf-8 -*-
"""
US Precalculus: Determinants and Inverse Matrices (Common Core N-VM.C.10, N-VM.C.12, A-REI.C.8, A-REI.C.9)
  python3 tools/gen_us_math_pc_determinants_and_inverse_matrices.py
Determinants of 2 × 2 and 3 × 3 matrices, when a matrix has an inverse, the inverse of a 2 × 2 matrix,
solving systems with A⁻¹B, and areas from determinants.
Wrong answers come from real mistakes: computing ad + bc or bc − ad, forgetting to swap a and d or to
change the signs of b and c, forgetting to divide by the determinant, and multiplying B·A⁻¹ instead of
A⁻¹B.
"""
import random
from fractions import Fraction as F
from us_hs import B, S, make, lesson, collect, T, num, MINUS, usd, People, fr
from a2_common import sf
from pc_common import GRADE, mat, det_h, mmul, det2, det3

R = random.Random(98101)
A_ = "<i>A</i>"
AI = "<i>A</i><sup>−1</sup>"


def rm(r, m, n, lo=-5, hi=7):
    return [[r.randint(lo, hi) for _ in range(n)] for _ in range(m)]


def inv2(m):
    d = det2(m)
    a, b = m[0]
    c, e = m[1]
    return [[F(e, d), F(-b, d)], [F(-c, d), F(a, d)]]


# ------------------------------------------------------------ set 1: 2 × 2 determinants
def one_d2(r):
    m = rm(r, 2, 2)
    d = det2(m)
    if d == 0 and r.random() < 0.7:
        return None
    a, b = m[0]
    c, e = m[1]
    q = "Find the determinant %s." % det_h(m) if r.random() < 0.5 else "Find det(%s) if %s = %s." % (A_, A_, mat(m))
    return T(q, sf(d), [sf(a * e + b * c), sf(b * c - a * e) if b * c - a * e != d else sf(d + 1), sf(a * b - c * e) if a * b - c * e != d else sf(d - 2)],
             "<i>ad</i> − <i>bc</i> = (%s)(%s) − (%s)(%s) = %s − %s = <b>%s</b>." % (sf(a), sf(e), sf(b), sf(c), sf(a * e), "(%s)" % sf(b * c) if b * c < 0 else sf(b * c), sf(d)))


# ------------------------------------------------------------ set 2: 3 × 3 determinants
def one_d3(r):
    m = rm(r, 3, 3, -3, 5)
    if r.random() < 0.4:
        m[1][0] = 0
        m[2][0] = 0
    d = det3(m)
    a, b, c = m[0]
    m1 = m[1][1] * m[2][2] - m[1][2] * m[2][1]
    m2 = m[1][0] * m[2][2] - m[1][2] * m[2][0]
    m3 = m[1][0] * m[2][1] - m[1][1] * m[2][0]
    wrong_sign = a * m1 + b * m2 + c * m3
    diag = sum(m[i][i] for i in range(3))
    prod = m[0][0] * m[1][1] * m[2][2]
    wr = [sf(wrong_sign) if wrong_sign != d else sf(d + 3), sf(prod) if prod != d else sf(d - 4), sf(-d) if d else sf(diag)]
    if len(set(wr + [sf(d)])) < 4:
        return None
    q = "Find the determinant %s." % det_h(m)
    return T(q, sf(d), wr, "Expand along row 1 with signs + − +: %s(%s) − %s(%s) + %s(%s) = <b>%s</b>." % (
        "(%s)" % sf(a) if a < 0 else sf(a), sf(m1), "(%s)" % sf(b) if b < 0 else sf(b), sf(m2), "(%s)" % sf(c) if c < 0 else sf(c), sf(m3), sf(d)))


# ------------------------------------------------------------ set 3: inverses
def nice_mat(r):
    for _ in range(200):
        m = rm(r, 2, 2, -4, 6)
        d = det2(m)
        if d in (1, -1, 2, -2, 4) and m[0][1] and m[1][0]:
            return m
    return None


def one_inv(r):
    kind = r.choice(["inv", "inv", "inv", "exists"])
    if kind == "exists":
        k = r.choice([2, 3, -2])
        a, b = r.randint(1, 5), r.randint(-4, 5)
        if r.random() < 0.5:
            m = [[a, b], [k * a, k * b]]
        else:
            m = [[a, b], [r.randint(-4, 5), r.randint(1, 6)]]
        d = det2(m)
        q = "Does %s = %s have an inverse?" % (A_, mat(m))
        right = "No, because det(%s) = 0" % A_ if d == 0 else "Yes, because det(%s) = %s, which is not 0" % (A_, sf(d))
        wr = (["Yes, because det(%s) = 0" % A_, "Yes, every square matrix has an inverse", "No, because it has a negative entry" if any(x < 0 for row in m for x in row) else "No, because no entry is 0"]
              if d == 0 else ["No, because det(%s) = %s" % (A_, sf(d)), "No, only the identity matrix has an inverse", "No, because det(%s) = 0" % A_])
        return T(q, right, wr, "A square matrix has an inverse exactly when its determinant is not 0. det(%s) = %s. <b>%s</b>." % (A_, sf(d), right))
    m = nice_mat(r)
    if m is None:
        return None
    d = det2(m)
    a, b = m[0]
    c, e = m[1]
    right = mat(inv2(m))
    wr = [mat([[F(a, d), F(-b, d)], [F(-c, d), F(e, d)]]), mat([[F(e, d), F(b, d)], [F(c, d), F(a, d)]]), mat([[e, -b], [-c, a]]) if d != 1 else mat([[F(-e), F(b)], [F(c), F(-a)]])]
    if len(set(wr + [right])) < 4:
        return None
    return T("Find %s if %s = %s." % (AI, A_, mat(m)), right, wr,
             "det(%s) = %s. Swap <i>a</i> and <i>d</i>, change the signs of <i>b</i> and <i>c</i>, then divide by %s: <b>%s</b>." % (A_, sf(d), sf(d), right))


# ------------------------------------------------------------ set 4: solving systems
def one_sys(r):
    m = nice_mat(r)
    if m is None or 0 in m[0] + m[1]:
        return None
    x, y = r.randint(-5, 6), r.randint(-5, 6)
    rhs = mmul(m, [[x], [y]])
    a, b = m[0]
    c, e = m[1]

    def lin(p, q_):
        s = ("" if p == 1 else MINUS if p == -1 else sf(p)) + "<i>x</i>"
        s += " %s %s<i>y</i>" % ("+" if q_ > 0 else MINUS, "" if abs(q_) == 1 else num(abs(q_)))
        return s
    kind = r.choice(["solve", "solve", "solve", "eq"])
    sysh = "%s = %s and %s = %s" % (lin(a, b), sf(rhs[0][0]), lin(c, e), sf(rhs[1][0]))
    if kind == "eq":
        q = "Which matrix equation represents the system %s?" % sysh
        right = "%s%s = %s" % (mat(m), mat([["<i>x</i>"], ["<i>y</i>"]]), mat(rhs))
        wr = ["%s%s = %s" % (mat([[a, c], [b, e]]), mat([["<i>x</i>"], ["<i>y</i>"]]), mat(rhs)), "%s%s = %s" % (mat(m), mat([["<i>x</i>"], ["<i>y</i>"]]), mat([[rhs[1][0]], [rhs[0][0]]])), "%s%s = %s" % (mat([["<i>x</i>", "<i>y</i>"]]), mat(m), mat(rhs))]
        if len(set(wr + [right])) < 4:
            return None
        return T(q, right, wr, "The coefficients go in the rows of the matrix, in the same order as the equations: <b>%s</b>." % right)
    q = "Solve %s using an inverse matrix." % sysh
    right = "(%s, %s)" % (sf(x), sf(y))
    bx = mmul([[rhs[0][0], rhs[1][0]]], inv2(m))[0]
    wr = ["(%s, %s)" % (sf(y), sf(x)) if x != y else "(%s, %s)" % (sf(-x), sf(y)), "(%s, %s)" % (sf(bx[0]), sf(bx[1])) if (bx[0], bx[1]) != (x, y) else "(%s, %s)" % (sf(x + 1), sf(y)),
          "(%s, %s)" % (sf(-x), sf(-y)) if (x, y) != (0, 0) else "(1, 1)"]
    if len(set(wr + [right])) < 4:
        return None
    return T(q, right, wr, "Write %s<i>X</i> = <i>B</i>, so <i>X</i> = %s<i>B</i> with %s = %s. Multiply %s<i>B</i> (in that order): <b>%s</b>." % (A_, AI, AI, mat(inv2(m)), AI, right))


# ------------------------------------------------------------ set 5: applications
def one_app(r):
    kind = r.choice(["tri", "tri", "par", "tickets", "tickets"])
    if kind == "tri":
        pts = [(r.randint(-5, 6), r.randint(-5, 6)) for _ in range(3)]
        (x1, y1), (x2, y2), (x3, y3) = pts
        d = x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)
        if d == 0:
            return None
        area = F(abs(d), 2)
        q = "Use a determinant to find the area of the triangle with vertices (%s, %s), (%s, %s) and (%s, %s)." % tuple(sf(v) for p in pts for v in p)
        return T(q, "%s square units" % num(area), ["%s square units" % num(abs(d)), "%s square units" % num(area + 2), "%s square units" % num(F(abs(d), 4)) if F(abs(d), 4).denominator in (1, 2, 4) else "%s square units" % num(area + 1)],
                 "Area = ½ |det| of the matrix with rows (<i>x</i>, <i>y</i>, 1). The determinant is %s, so the area is ½ × %d = <b>%s square units</b>." % (sf(d), abs(d), num(area)))
    if kind == "par":
        a, b = r.randint(1, 7), r.randint(-3, 4)
        c, e = r.randint(-3, 4), r.randint(1, 7)
        d = a * e - b * c
        if d == 0:
            return None
        q = "A parallelogram has sides given by the vectors ⟨%s, %s⟩ and ⟨%s, %s⟩. What is its area?" % (sf(a), sf(b), sf(c), sf(e))
        return T(q, "%d square units" % abs(d), ["%s square units" % num(F(abs(d), 2)), "%d square units" % abs(a * e + b * c) if abs(a * e + b * c) != abs(d) else "%d square units" % (abs(d) + 2), "%d square units" % abs(a * c + b * e) if abs(a * c + b * e) != abs(d) else "%d square units" % (abs(d) + 1)],
                 "The area is |det| = |(%s)(%s) − (%s)(%s)| = <b>%d square units</b>." % (sf(a), sf(e), sf(b), sf(c), abs(d)))
    pa, pc = r.choice([(12, 7), (15, 9), (10, 6), (14, 8), (9, 5)])
    na, nc = r.randint(40, 120), r.randint(40, 150)
    total = na + nc
    money = na * pa + nc * pc
    q = ("A school play sold %d tickets for a total of %s. Adult tickets cost %s and student tickets cost %s. "
         "The system %s = %s, %s = %s is solved with an inverse matrix. How many adult tickets were sold?" % (
             total, usd(money), usd(pa), usd(pc), "<i>a</i> + <i>s</i>", num(total), "%d<i>a</i> + %d<i>s</i>" % (pa, pc), num(money)))
    return T(q, str(na), [str(nc), str(total // 2) if total // 2 not in (na, nc) else str(na + 5), str(round(money / pa)) if round(money / pa) not in (na, nc) else str(na - 3)],
             "The coefficient matrix %s has determinant %s. <i>X</i> = %s<i>B</i> gives <i>a</i> = %d and <i>s</i> = %d. <b>%d adult tickets</b>." % (mat([[1, 1], [pa, pc]]), sf(pc - pa), AI, na, nc, na))


def build():
    sets = [S("2 × 2 determinants", collect(one_d2, 20, R)),
            S("3 × 3 determinants", collect(one_d3, 20, R)),
            S("Inverse matrices", collect(one_inv, 20, R)),
            S("Solving systems with matrices", collect(one_sys, 20, R)),
            S("Applications", collect(one_app, 20, R))]
    body = lesson(
        "<ul><li>For " + mat([["<i>a</i>", "<i>b</i>"], ["<i>c</i>", "<i>d</i>"]]) + ", the <b>determinant</b> is <i>ad</i> − <i>bc</i>.</li>"
        "<li>For a 3 × 3 matrix, expand along the first row with signs + − +, using the 2 × 2 determinant left when you cross out each entry's row and column.</li>"
        "<li>A square matrix has an <b>inverse</b> only if its determinant is not 0. For 2 × 2: <i>A</i><sup>−1</sup> = (1/det) · " + mat([["<i>d</i>", "−<i>b</i>"], ["−<i>c</i>", "<i>a</i>"]]) + ".</li>"
        "<li>A system can be written <i>AX</i> = <i>B</i>. Then <i>X</i> = <i>A</i><sup>−1</sup><i>B</i> (multiply on the left).</li></ul>",
        [("Find <i>A</i><sup>−1</sup> for <i>A</i> = " + mat([[3, 1], [5, 2]]) + ".", ["det = 3(2) − 1(5) = 1", "Swap 3 and 2; change the signs of 1 and 5"], mat([[2, -1], [-5, 3]])),
         ("Solve 3<i>x</i> + <i>y</i> = 7, 5<i>x</i> + 2<i>y</i> = 12.", ["<i>X</i> = <i>A</i><sup>−1</sup><i>B</i> = " + mat([[2, -1], [-5, 3]]) + mat([[7], [12]]), "= " + mat([[2], [1]])], "(2, 1)")],
        ["Computing <i>ad</i> + <i>bc</i> instead of <i>ad</i> − <i>bc</i>.",
         "Forgetting to swap <i>a</i> and <i>d</i> or to change the signs of <i>b</i> and <i>c</i>.",
         "Forgetting to divide by the determinant.",
         "Multiplying <i>B</i><i>A</i><sup>−1</sup>. The inverse goes on the left."])
    faq = [("How do you find the determinant of a 2 × 2 matrix?", "Multiply the main diagonal and subtract the product of the other diagonal: ad − bc."),
           ("When does a matrix have an inverse?", "A square matrix has an inverse exactly when its determinant is not 0."),
           ("How do you find the inverse of a 2 × 2 matrix?", "Swap a and d, change the signs of b and c, and divide every entry by the determinant ad − bc."),
           ("How do you solve a system with an inverse matrix?", "Write the system as AX = B, then multiply both sides on the left by A⁻¹: X = A⁻¹B.")]
    make("determinants-and-inverse-matrices", 11, "N-VM.C.10",
         "Determinants and Inverse Matrices",
         "Determinants and Inverse Matrices Worksheet: Solve Systems with Matrices | 100 Questions",
         "Determinants and Inverses",
         "Understand that the zero and identity matrices play a role in matrix addition and multiplication similar to the role of 0 and 1 in the real numbers. The determinant of a square matrix is nonzero if and only if the matrix has a multiplicative inverse.",
         "Free precalculus worksheet on determinants and inverse matrices: 2 × 2 and 3 × 3 determinants, inverses, solving systems with A⁻¹B and area. 100 questions with answers.",
         "det = ad − bc. A matrix has an inverse only when det ≠ 0.",
         "A⁻¹ = (1/det) [d −b; −c a], and X = A⁻¹B.",
         body, faq, sets, R, domain="Vectors and Matrices", grade=GRADE)


if __name__ == "__main__":
    build()
