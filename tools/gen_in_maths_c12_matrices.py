# -*- coding: utf-8 -*-
"""
India Class 12 Maths, NCERT Chapter 3: Matrices (CBSE Unit II Algebra)
  python3 tools/gen_in_maths_c12_matrices.py
Order of a matrix, building a matrix from a rule for aᵢⱼ, equality of matrices, addition, subtraction and scalar
multiples, when a product is defined, multiplying matrices and AB ≠ BA, the transpose, symmetric and skew symmetric
matrices, and the number of matrices of a given order (own makers and US Precalculus makers).
Wrong answers come from real mistakes: rows and columns swapped, multiplying entry by entry, assuming AB = BA,
(AB)′ = A′B′, and a skew symmetric matrix with non-zero diagonal entries.
"""
import random
from fractions import Fraction as F
from in_sr import U, T2, use, X, Y
from in_common import num, fv, comma
from pc_common import mat

R = random.Random(912103)
FX = [("what are its dimensions", "what is its order"), ("What are the dimensions", "What is the order"), ("inside dimensions", "inner orders"), ("dimensions", "order"), ("Dimensions", "Order")]
add = use(__import__("gen_us_math_pc_matrix_operations"), "one_add", R, FX)
scal = use(__import__("gen_us_math_pc_matrix_operations"), "one_scal", R, FX)
dim = use(__import__("gen_us_math_pc_matrix_operations"), "one_dim", R, FX)
mul = use(__import__("gen_us_math_pc_matrix_operations"), "one_mul", R, FX)
word = use(__import__("gen_us_math_pc_matrix_operations"), "one_word", R, FX)


def M(rows):
    return mat([[num(v) if not isinstance(v, str) else v for v in row] for row in rows])


def mm(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]


def tr(A):
    return [list(c) for c in zip(*A)]


def rnd(r, m, n, lo=-5, hi=6):
    return [[r.randint(lo, hi) for _ in range(n)] for _ in range(m)]


def one_order(r):
    k = r.choice(["orders", "count", "aij", "build"])
    if k == "orders":
        n = r.choice([6, 8, 12, 18, 24, 5, 7, 13])
        ords = ["%d × %d" % (a, n // a) for a in range(1, n + 1) if n % a == 0]
        right = ", ".join(ords)
        return T2("A matrix has %d elements. What are its possible orders?" % n, right,
                  [", ".join(ords[:len(ords) // 2 + 1]) if len(ords) > 2 else "%d × 1 only" % n, ", ".join(o for o in ords if o.split(" × ")[0] <= o.split(" × ")[1]) if len(ords) > 2 else "1 × %d only" % n, "%d × %d" % (n, n)],
                  "The order m × n needs mn = %d, so it can be <b>%s</b>." % (n, right))
    if k == "count":
        m, n = r.randint(1, 3), r.randint(2, 3)
        v = r.choice([2, 3])
        return T2("How many matrices of order %d × %d can be made with each entry %s?" % (m, n, "0 or 1" if v == 2 else "0, 1 or 2"), comma(v ** (m * n)),
                  [str(v * m * n), comma(2 ** (m + n)), comma((m * n) ** v)],
                  "There are %d entries, each with %d choices: %d<sup>%d</sup> = <b>%s</b>." % (m * n, v, v, m * n, comma(v ** (m * n))))
    if k == "aij":
        A = rnd(r, r.randint(2, 3), r.randint(2, 4))
        i, j = r.randint(1, len(A)), r.randint(1, len(A[0]))
        if j > len(A) or A[i - 1][j - 1] == A[j - 1][i - 1] or i == j:
            return None
        return T2("A = %s. Find a<sub>%d%d</sub>." % (M(A), i, j), num(A[i - 1][j - 1]), [num(A[j - 1][i - 1]), num(A[i - 1][j - 1] + 1), num(-A[i - 1][j - 1]) if A[i - 1][j - 1] else "1"],
                  "a<sub>%d%d</sub> is in row %d and column %d: <b>%s</b>." % (i, j, i, j, num(A[i - 1][j - 1])))
    rule = r.choice([("i + 2j", lambda i, j: i + 2 * j), ("2i − j", lambda i, j: 2 * i - j), ("i × j", lambda i, j: i * j), ("(i + j)²/2", lambda i, j: F((i + j) ** 2, 2)),
                     ("|i − 3j|", lambda i, j: abs(i - 3 * j)), ("3i − 2j", lambda i, j: 3 * i - 2 * j)])
    m, n = 2, r.choice([2, 3])
    A = [[rule[1](i, j) for j in range(1, n + 1)] for i in range(1, m + 1)]
    Bw = [[rule[1](j, i) for j in range(1, n + 1)] for i in range(1, m + 1)]
    show = lambda Mx: mat([[fv(v) for v in row] for row in Mx])
    if A == Bw:
        Bw = [[v + 1 for v in row] for row in A]
    return T2("Build the %d × %d matrix with a<sub>ij</sub> = %s." % (m, n, rule[0]), show(A), [show(Bw), show(tr(A)) if n == m else show([[v + 1 for v in row] for row in A]), show([[v * 2 for v in row] for row in A])],
              "Put i = row number and j = column number into %s: <b>%s</b>." % (rule[0], show(A)))


def one_eq(r):
    x, y, z = r.randint(-6, 6), r.randint(-6, 6), r.randint(-6, 6)
    a, b = r.randint(1, 3), r.randint(1, 3)
    p, q = a * x + b * y, x - y
    A = [["%s + %s" % (X if a == 1 else "%d%s" % (a, X), Y if b == 1 else "%d%s" % (b, Y)), "%s"], ["%s − %s" % (X, Y), "<i>z</i>"]]
    A[0][1] = num(r.randint(1, 9))
    B = [[p, A[0][1]], [q, z]]
    return T2("Find %s, %s and <i>z</i> if %s = %s." % (X, Y, mat(A), M(B)), "%s = %s, %s = %s, <i>z</i> = %s" % (X, num(x), Y, num(y), num(z)),
              ["%s = %s, %s = %s, <i>z</i> = %s" % (X, num(y), Y, num(x), num(z)), "%s = %s, %s = %s, <i>z</i> = %s" % (X, num(p), Y, num(q), num(z)), "%s = %s, %s = %s, <i>z</i> = %s" % (X, num(x), Y, num(-y), num(-z)) if (y or z) else "%s = 1, %s = 1, <i>z</i> = 1" % (X, Y)],
              "Equal matrices have equal corresponding entries: %s = %s and %s − %s = %s, so <b>%s = %s, %s = %s, <i>z</i> = %s</b>." % (A[0][0], num(p), X, Y, num(q), X, num(x), Y, num(y), num(z)))


def one_comm(r):
    A, B = rnd(r, 2, 2, -3, 4), rnd(r, 2, 2, -3, 4)
    AB, BA = mm(A, B), mm(B, A)
    if AB == BA:
        return None
    k = r.choice(["ab", "ba", "sq"])
    if k == "sq":
        A2 = mm(A, A)
        return T2("A = %s. Find A²." % M(A), M(A2), [M([[v * v for v in row] for row in A]), M([[2 * v for v in row] for row in A]), M(tr(A2)) if tr(A2) != A2 else M([[v + 1 for v in row] for row in A2])],
                  "A² = A × A, multiplying rows by columns (not squaring each entry): <b>%s</b>." % M(A2))
    X_, Y_ = (B, A) if k == "ba" else (A, B)
    P = mm(X_, Y_)
    lab = "BA" if k == "ba" else "AB"
    return T2("A = %s and B = %s. Find %s." % (M(A), M(B), lab), M(P), [M(mm(Y_, X_)), M([[A[i][j] * B[i][j] for j in range(2)] for i in range(2)]), M(tr(P)) if tr(P) != P else M([[v + 1 for v in row] for row in P])],
              "Multiply rows of the first matrix by columns of the second: <b>%s</b>. (Here AB ≠ BA.)" % M(P))


def one_trans(r):
    k = r.choice(["t", "sym", "skew", "which", "ab"])
    if k == "t":
        A = rnd(r, 2, 3)
        return T2("A = %s. Find A′." % M(A), M(tr(A)), [M(A), M([[v for v in row[::-1]] for row in A]), M([row[::-1] for row in tr(A)])],
                  "Rows become columns: <b>%s</b>." % M(tr(A)))
    if k in ("sym", "skew"):
        A = rnd(r, 2, 2) if r.random() < 0.5 else rnd(r, 3, 3)
        n = len(A)
        S = [[F(A[i][j] + A[j][i], 2) for j in range(n)] for i in range(n)]
        K = [[F(A[i][j] - A[j][i], 2) for j in range(n)] for i in range(n)]
        show = lambda Mx: mat([[fv(v) for v in row] for row in Mx])
        if k == "sym":
            return T2("A = %s. Find the symmetric part ½(A + A′)." % M(A), show(S), [show(K), show([[A[i][j] + A[j][i] for j in range(n)] for i in range(n)]), show(tr(A))],
                      "½(A + A′) = <b>%s</b>; it equals its own transpose." % show(S))
        return T2("A = %s. Find the skew symmetric part ½(A − A′)." % M(A), show(K), [show(S), show([[F(A[j][i] - A[i][j], 2) for j in range(n)] for i in range(n)]), show([[A[i][j] - A[j][i] for j in range(n)] for i in range(n)])],
                  "½(A − A′) = <b>%s</b>; its diagonal entries are 0." % show(K))
    if k == "ab":
        return T2("For matrices A and B for which AB is defined, which is always true?", "(AB)′ = B′A′", ["(AB)′ = A′B′", "AB = BA", "(A + B)′ = A′ − B′"],
                  "The transpose of a product reverses the order: <b>(AB)′ = B′A′</b>.")
    a, b, c = r.sample([k for k in range(-6, 7) if k], 3)
    sym = [[a, b], [b, c]]
    skew = [[0, b], [-b, 0]]
    bad = [[a, b], [-b, c]]
    bad2 = [[0, b], [b, 0]]
    if r.random() < 0.5:
        return T2("Which matrix is skew symmetric?", M(skew), [M(sym), M(bad), M(bad2)],
                  "A skew symmetric matrix has A′ = −A, so its diagonal is 0 and a<sub>ji</sub> = −a<sub>ij</sub>: <b>%s</b>." % M(skew))
    return T2("Which matrix is symmetric?", M(sym), [M(skew), M(bad), M([[a, b], [c, a]]) if c != b else M([[a, b], [c + 1, a]])],
              "A symmetric matrix has A′ = A, so a<sub>ji</sub> = a<sub>ij</sub>: <b>%s</b>." % M(sym))


U(12, 3, "matrices", 3, "II", "Matrices: Order, Operations, Transpose and Symmetric Matrices", "matrices",
  "Concept, notation, order, equality, types of matrices, zero and identity matrix, transpose of a matrix, symmetric and skew symmetric matrices; operations on matrices: addition and multiplication and multiplication with a scalar; simple properties of addition, multiplication and scalar multiplication; non-commutativity of multiplication of matrices; invertible matrices (summary of the CBSE syllabus)",
  "Class 12 Matrices worksheet (NCERT Chapter 3): order, aᵢⱼ, equality, addition, scalar multiples, multiplication, AB ≠ BA, transpose, symmetric and skew symmetric matrices. 100 questions with answers.",
  "AB is defined only when columns of A = rows of B.", "(AB)′ = B′A′; any square matrix = symmetric part + skew symmetric part.",
  "<ul><li>An m × n matrix has m rows and n columns; a<sub>ij</sub> is in row i, column j.</li>"
  "<li>Add matrices of the same order entry by entry; kA multiplies every entry by k.</li>"
  "<li>AB is defined when the number of columns of A equals the number of rows of B; multiply rows by columns. In general AB ≠ BA.</li>"
  "<li>Transpose A′: rows become columns. Symmetric: A′ = A. Skew symmetric: A′ = −A (diagonal entries 0). A = ½(A + A′) + ½(A − A′).</li></ul>",
  [("A = [1 2; 3 4]. Find A².", ["Row 1 × columns: 1·1 + 2·3 = 7, 1·2 + 2·4 = 10", "Row 2: 3·1 + 4·3 = 15, 3·2 + 4·4 = 22"], "[7 10; 15 22]")],
  ["Swapping rows and columns when giving the order.", "Multiplying matrices entry by entry.", "Assuming AB = BA."],
  [("Can a non-square matrix be symmetric?", "No. A′ = A needs the same order, so the matrix must be square."),
   ("What is the identity matrix?", "A square matrix with 1s on the diagonal and 0s elsewhere; AI = IA = A.")],
  [("Order and elements", [(one_order, 14), (dim, 6)]),
   ("Equality, addition and scalar multiples", [(one_eq, 6), (add, 7), (scal, 7)]),
   ("Multiplying matrices", [(mul, 10), (one_comm, 10)]),
   ("Transpose, symmetric and skew symmetric", [(one_trans, 20)]),
   ("Mixed problems", [(one_comm, 8), (word, 6), (one_order, 6)])], 912103)
