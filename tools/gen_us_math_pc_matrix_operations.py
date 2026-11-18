# -*- coding: utf-8 -*-
"""
US Precalculus: Matrix Operations (Common Core N-VM.C.6, N-VM.C.7, N-VM.C.8, N-VM.C.9)
  python3 tools/gen_us_math_pc_matrix_operations.py
Adding and subtracting matrices, scalar multiplication, dimensions of products, multiplying matrices, and
using matrices to organize data such as sales and prices.
Wrong answers come from real mistakes: multiplying entry by entry, multiplying in the wrong order (BA for
AB), matching the wrong dimensions, and multiplying a scalar into only one entry.
"""
import random
from us_hs import B, S, make, lesson, collect, T, num, MINUS, usd, People
from a2_common import sf
from pc_common import GRADE, mat, mmul

R = random.Random(98001)
A_, B_, C_ = "<i>A</i>", "<i>B</i>", "<i>C</i>"


def rm(r, m, n, lo=-6, hi=9):
    return [[r.randint(lo, hi) for _ in range(n)] for _ in range(m)]


def ew(a, b, f):
    return [[f(x, y) for x, y in zip(ra, rb)] for ra, rb in zip(a, b)]


def tr(a):
    return [list(c) for c in zip(*a)]


# ------------------------------------------------------------ set 1: add and subtract
def one_add(r):
    m, n = r.choice([(2, 2), (2, 2), (2, 3), (3, 2)])
    a, b = rm(r, m, n), rm(r, m, n)
    op = r.choice(["+", "−"])
    f = (lambda x, y: x + y) if op == "+" else (lambda x, y: x - y)
    q = "If %s = %s and %s = %s, find %s %s %s." % (A_, mat(a), B_, mat(b), A_, op, B_)
    right = mat(ew(a, b, f))
    wr = [mat(ew(a, b, (lambda x, y: x - y) if op == "+" else (lambda x, y: x + y))), mat(ew(a, b, lambda x, y: x * y)), mat(ew(b, a, (lambda x, y: x - y)) if op == "−" else [row[::-1] for row in ew(a, b, f)])]
    return T(q, right, wr, "Add or subtract the entries in the same positions. <b>%s</b>." % right)


# ------------------------------------------------------------ set 2: scalars and combinations
def one_scal(r):
    a, b = rm(r, 2, 2, -5, 6), rm(r, 2, 2, -5, 6)
    k = r.choice([2, 3, 4, -2, -3])
    if r.random() < 0.4:
        q = "If %s = %s, find %s%s." % (A_, mat(a), sf(k), A_)
        right = mat([[k * x for x in row] for row in a])
        wr = [mat([[k * a[0][0], a[0][1]], a[1]]), mat([[x + k for x in row] for row in a]), mat([[-k * x for x in row] for row in a])]
        return T(q, right, wr, "Multiply every entry by %s. <b>%s</b>." % (sf(k), right))
    m = r.choice([2, 3, -1])
    q = "If %s = %s and %s = %s, find %s%s %s %s%s." % (A_, mat(a), B_, mat(b), sf(k), A_, "+" if m > 0 else MINUS, "" if abs(m) == 1 else num(abs(m)), B_)
    res = [[k * x + m * y for x, y in zip(ra, rb)] for ra, rb in zip(a, b)]
    right = mat(res)
    wr = [mat([[k * x - m * y for x, y in zip(ra, rb)] for ra, rb in zip(a, b)]), mat([[x + m * y for x, y in zip(ra, rb)] for ra, rb in zip(a, b)]),
          mat([[k * x + m * y for x, y in zip(ra, rb)] for ra, rb in zip(a, b[::-1])])]
    return T(q, right, wr, "Multiply each matrix by its scalar, then combine matching entries. <b>%s</b>." % right)


# ------------------------------------------------------------ set 3: dimensions
def one_dim(r):
    m, n, p = r.choice([1, 2, 3, 4]), r.choice([2, 3, 4]), r.choice([1, 2, 3, 4, 5])
    kind = r.choice(["ab", "ab", "ba", "def"])
    if kind == "ab":
        q = "%s is %d × %d and %s is %d × %d. What are the dimensions of %s%s?" % (A_, m, n, B_, n, p, A_, B_)
        right = "%d × %d" % (m, p)
        wr = ["%d × %d" % (n, n) if (n, n) != (m, p) else "%d × %d" % (p, m), "%d × %d" % (p, m) if p != m else "%d × %d" % (m, n), "%s%s is not defined" % (A_, B_)]
        return T(q, right, wr, "The inside numbers match (%d = %d), so the product is defined. Its size is the outside numbers: <b>%s</b>." % (n, n, right))
    if kind == "ba":
        if p == m:
            return None
        q = "%s is %d × %d and %s is %d × %d. Is %s%s defined?" % (A_, m, n, B_, n, p, B_, A_)
        right = "No, because %s has %d columns but %s has %d rows" % (B_, p, A_, m)
        return T(q, right, ["Yes, it is %d × %d" % (n, n), "Yes, because %s%s is defined" % (A_, B_), "Yes, it is %d × %d" % (p, m)],
                 "For %s%s, the columns of %s (%d) must equal the rows of %s (%d). <b>%s</b>." % (B_, A_, B_, p, A_, m, right))
    x, y = r.choice([(2, 3), (3, 2), (2, 4), (4, 1), (1, 3)])
    u, w = r.choice([(3, 2), (2, 2), (4, 3), (1, 4), (2, 5)])
    q = "%s is %d × %d and %s is %d × %d. Is %s%s defined, and if so, what are its dimensions?" % (A_, x, y, B_, u, w, A_, B_)
    if y == u:
        right = "Yes, %d × %d" % (x, w)
        wr = ["No, it is not defined", "Yes, %d × %d" % (y, u) if (y, u) != (x, w) else "Yes, %d × %d" % (w, x), "Yes, %d × %d" % (w, x) if (w, x) != (x, w) else "Yes, %d × %d" % (x, y)]
    else:
        right = "No, it is not defined"
        wr = ["Yes, %d × %d" % (x, w), "Yes, %d × %d" % (y, u), "Yes, %d × %d" % (x, u)]
    if len(set(wr + [right])) < 4:
        return None
    return T(q, right, wr, "%s has %d columns and %s has %d rows. %s" % (A_, y, B_, u, "They match, so the product is %d × %d. <b>%s</b>." % (x, w, right) if y == u else "They do not match. <b>%s</b>." % right))


# ------------------------------------------------------------ set 4: multiplying
def one_mul(r):
    kind = r.choice(["22", "22", "21", "entry"])
    a = rm(r, 2, 2, -4, 6)
    if kind == "21":
        v = rm(r, 2, 1, -4, 6)
        q = "Find %s%s if %s = %s and %s = %s." % (A_, B_, A_, mat(a), B_, mat(v))
        right = mat(mmul(a, v))
        wr = [mat([[a[0][0] * v[0][0]], [a[1][1] * v[1][0]]]), mat(mmul(tr(a), v)), mat([[sum(a[0]) * v[0][0]], [sum(a[1]) * v[1][0]]])]
        return T(q, right, wr, "Row times column: (%s)(%s) + (%s)(%s) = %s and (%s)(%s) + (%s)(%s) = %s. <b>%s</b>." % (
            sf(a[0][0]), sf(v[0][0]), sf(a[0][1]), sf(v[1][0]), sf(mmul(a, v)[0][0]), sf(a[1][0]), sf(v[0][0]), sf(a[1][1]), sf(v[1][0]), sf(mmul(a, v)[1][0]), right))
    b = rm(r, 2, 2, -4, 6)
    if mmul(a, b) == mmul(b, a):
        return None
    if kind == "entry":
        i, j = r.randint(0, 1), r.randint(0, 1)
        ab = mmul(a, b)
        q = "If %s = %s and %s = %s, what is the entry in row %d, column %d of %s%s?" % (A_, mat(a), B_, mat(b), i + 1, j + 1, A_, B_)
        ans = ab[i][j]
        wr = [sf(a[i][j] * b[i][j]), sf(mmul(b, a)[i][j]) if mmul(b, a)[i][j] != ans else sf(ans + 1), sf(a[j][0] * b[0][i] + a[j][1] * b[1][i]) if a[j][0] * b[0][i] + a[j][1] * b[1][i] != ans else sf(ans - 2)]
        return T(q, sf(ans), wr, "Row %d of %s times column %d of %s: (%s)(%s) + (%s)(%s) = <b>%s</b>." % (
            i + 1, A_, j + 1, B_, sf(a[i][0]), sf(b[0][j]), sf(a[i][1]), sf(b[1][j]), sf(ans)))
    q = "Find %s%s if %s = %s and %s = %s." % (A_, B_, A_, mat(a), B_, mat(b))
    right = mat(mmul(a, b))
    wr = [mat(ew(a, b, lambda x, y: x * y)), mat(mmul(b, a)), mat(mmul(tr(a), b)) if mmul(tr(a), b) != mmul(a, b) else mat(mmul(a, tr(b)))]
    return T(q, right, wr, "Each entry is a row of %s times a column of %s. Do not multiply entry by entry, and keep the order: %s%s ≠ %s%s in general. <b>%s</b>." % (A_, B_, A_, B_, B_, A_, right))


# ------------------------------------------------------------ set 5: word problems
ITEMS = [("T-shirts", "hats"), ("small pizzas", "large pizzas"), ("adult tickets", "child tickets"), ("notebooks", "pens")]


def one_word(r):
    it1, it2 = r.choice(ITEMS)
    p1, p2 = r.choice([(12, 8), (9, 15), (14, 6), (4, 2), (11, 7), (20, 10)])
    s = [[r.randint(10, 60), r.randint(10, 60)] for _ in range(2)]
    pp = People(r)
    n1, _, _ = pp.next()
    n2, _, _ = pp.next()
    kind = r.choice(["one", "one", "both", "diff"])
    rev = mmul(s, [[p1], [p2]])
    rows = "<table class='sn-table'><tr><th></th><th>%s</th><th>%s</th></tr><tr><td>%s</td><td>%d</td><td>%d</td></tr><tr><td>%s</td><td>%d</td><td>%d</td></tr></table>" % (
        it1.capitalize(), it2.capitalize(), n1, s[0][0], s[0][1], n2, s[1][0], s[1][1])
    pre = "The table shows how many items two students sold. %s cost %s each and %s cost %s each. The sales matrix times the price matrix %s gives each student's total.%s" % (
        it1.capitalize(), usd(p1), it2, usd(p2), mat([[usd(p1)], [usd(p2)]]), rows)
    if kind == "one":
        who = r.randint(0, 1)
        q = pre + " How much money did %s collect?" % [n1, n2][who]
        ans = rev[who][0]
        return T(q, usd(ans), [usd(s[who][0] * p2 + s[who][1] * p1), usd((s[who][0] + s[who][1]) * (p1 + p2)), usd(s[0][0] * p1 + s[1][0] * p2) if s[0][0] * p1 + s[1][0] * p2 != ans else usd(ans + p1)],
                 "%d × %s + %d × %s = %s + %s = <b>%s</b>." % (s[who][0], usd(p1), s[who][1], usd(p2), usd(s[who][0] * p1), usd(s[who][1] * p2), usd(ans)))
    if kind == "both":
        q = pre + " Which matrix gives both totals?"
        right = mat([[usd(rev[0][0])], [usd(rev[1][0])]])
        wr = [mat([[usd(s[0][0] * p1 + s[1][0] * p2)], [usd(s[0][1] * p1 + s[1][1] * p2)]]), mat([[usd(s[0][0] * p1), usd(s[0][1] * p2)], [usd(s[1][0] * p1), usd(s[1][1] * p2)]]),
              mat([[usd(s[0][0] * p2 + s[0][1] * p1)], [usd(s[1][0] * p2 + s[1][1] * p1)]])]
        return T(q, right, wr, "Multiply each row of the sales matrix by the price column. The result is a 2 × 1 matrix: <b>%s</b>." % right)
    q = pre + " How much more did the student who collected more money collect?"
    d = abs(rev[0][0] - rev[1][0])
    if d == 0:
        return None
    return T(q, usd(d), [usd(abs(sum(s[0]) - sum(s[1])) * p1) if abs(sum(s[0]) - sum(s[1])) * p1 != d else usd(d + p2), usd(rev[0][0] + rev[1][0]), usd(abs(s[0][0] - s[1][0]) * p1 + abs(s[0][1] - s[1][1]) * p2) if abs(s[0][0] - s[1][0]) * p1 + abs(s[0][1] - s[1][1]) * p2 != d else usd(d * 2)],
             "The totals are %s and %s. The difference is <b>%s</b>." % (usd(rev[0][0]), usd(rev[1][0]), usd(d)))


def build():
    sets = [S("Adding and subtracting matrices", collect(one_add, 20, R)),
            S("Scalar multiplication", collect(one_scal, 20, R)),
            S("Dimensions of products", collect(one_dim, 20, R)),
            S("Multiplying matrices", collect(one_mul, 20, R)),
            S("Word problems", collect(one_word, 20, R))]
    body = lesson(
        "<ul><li>A matrix with <i>m</i> rows and <i>n</i> columns is <i>m</i> × <i>n</i>. Add or subtract only matrices of the same size, entry by entry.</li>"
        "<li>A <b>scalar</b> multiplies every entry.</li>"
        "<li>The product <i>AB</i> is defined when the columns of <i>A</i> equal the rows of <i>B</i>. An <i>m</i> × <i>n</i> times an <i>n</i> × <i>p</i> gives <i>m</i> × <i>p</i>.</li>"
        "<li>Each entry of <i>AB</i> is a <b>row of A times a column of B</b>: multiply matching numbers and add. In general <i>AB</i> ≠ <i>BA</i>.</li></ul>",
        [("Find " + mat([[1, 2], [3, 4]]) + mat([[5, 0], [1, 2]]) + ".", ["Row 1 · column 1: 1(5) + 2(1) = 7; row 1 · column 2: 1(0) + 2(2) = 4", "Row 2: 3(5) + 4(1) = 19 and 3(0) + 4(2) = 8"], mat([[7, 4], [19, 8]])),
         ("<i>A</i> is 3 × 2 and <i>B</i> is 2 × 4. Find the size of <i>AB</i>.", ["Inside numbers 2 and 2 match", "Outside numbers 3 and 4"], "3 × 4")],
        ["Multiplying entry by entry. Use row times column.",
         "Assuming <i>AB</i> = <i>BA</i>. Matrix multiplication is not commutative.",
         "Checking the wrong numbers for dimensions. The columns of the first must match the rows of the second.",
         "Multiplying a scalar into only some of the entries."])
    faq = [("How do you multiply two matrices?", "Each entry of AB is found by multiplying a row of A by a column of B, matching numbers in order and adding the products."),
           ("When is a matrix product defined?", "When the number of columns of the first matrix equals the number of rows of the second. An m × n times an n × p matrix is m × p."),
           ("Is matrix multiplication commutative?", "No. In general AB and BA are different, and one may be defined when the other is not."),
           ("How are matrices used in real life?", "They organize data. For example, a table of items sold times a column of prices gives each seller's total.")]
    make("matrix-operations", 10, "N-VM.C.8",
         "Matrix Operations",
         "Matrix Operations Worksheet: Add, Subtract and Multiply Matrices | 100 Questions",
         "Matrix Operations",
         "Add, subtract, and multiply matrices of appropriate dimensions.",
         "Free precalculus worksheet on matrix operations: adding and subtracting, scalar multiplication, dimensions of products, multiplying matrices and data problems. 100 questions.",
         "Multiply row times column. The inside dimensions must match.",
         "m × n times n × p gives m × p, and AB ≠ BA in general.",
         body, faq, sets, R, domain="Vectors and Matrices", grade=GRADE)


if __name__ == "__main__":
    build()
