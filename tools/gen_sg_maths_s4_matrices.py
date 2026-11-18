# -*- coding: utf-8 -*-
"""
SG Secondary 4 Maths: Matrices (MOE syllabus N9)
  python3 tools/gen_sg_maths_s4_matrices.py
Displaying and interpreting information in a matrix, addition, subtraction and scalar multiples, the order of a
matrix and when a product is defined, matrix multiplication, and real-world problems (costs and totals).
Sets 2 to 4 reuse the US Precalculus makers, with "order" in place of "dimensions".
Wrong answers come from real mistakes: multiplying entry by entry, mixing up rows and columns, adding matrices
of different orders, and multiplying in the wrong order.
"""
import random
from sg_sec import num, S, make, lesson, collect, T, QN, sgd, People, adopt
from pc_common import mat
import gen_us_math_pc_matrix_operations as us

R = random.Random(840200)
adopt(us, R)
P = People(R)

FIX = [("What are the dimensions", "What is the order"), ("dimensions", "order"), ("Dimensions", "Order"), (" has 1 columns", " has 1 column"), (" has 1 rows", " has 1 row")]


def wrap(fn):
    def f(r):
        it = fn(r)
        if not it:
            return None
        for k in ("q", "e"):
            for a, b in FIX:
                it[k] = it[k].replace(a, b)
        it["c"] = [c.replace("dimensions", "order").replace(" has 1 columns", " has 1 column").replace(" has 1 rows", " has 1 row") for c in it["c"]]
        return it
    return f


SHOPS = ["Jurong", "Tampines", "Bishan", "Punggol", "Clementi"]
ITEMS = [("pens", "notebooks", "files"), ("burgers", "drinks", "fries"), ("adult tickets", "child tickets", "senior tickets"), ("shirts", "shorts", "caps")]


def addm(a, b):
    return [[x + y for x, y in zip(ra, rb)] for ra, rb in zip(a, b)]


def mulm(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


# ------------------------------------------------------------ set 1: displaying and interpreting
def one_info(r):
    shops = r.sample(SHOPS, 2)
    items = r.choice(ITEMS)
    M = [[r.randint(5, 60) for _ in range(3)] for _ in range(2)]
    kind = r.choice(["entry", "entry", "order", "rowsum", "colsum"])
    pre = "The matrix %s shows the numbers of %s, %s and %s (columns, in that order) sold by shops at %s and %s (rows, in that order)." % (mat(M), items[0], items[1], items[2], shops[0], shops[1])
    if kind == "entry":
        i, j = r.randint(0, 1), r.randint(0, 2)
        return QN(pre + " How many %s did the %s shop sell?" % (items[j], shops[i]), M[i][j], [M[1 - i][j], M[i][(j + 1) % 3], M[i][j] + M[1 - i][j]],
                  "Row %d is %s and column %d is %s: the entry is <b>%d</b>." % (i + 1, shops[i], j + 1, items[j], M[i][j]))
    if kind == "order":
        return T(pre + " What is the order of this matrix?", "2 × 3", ["3 × 2", "6", "2 × 2"], "It has 2 rows and 3 columns. The order is rows × columns: <b>2 × 3</b>.")
    if kind == "rowsum":
        i = r.randint(0, 1)
        return QN(pre + " How many items did the %s shop sell altogether?" % shops[i], sum(M[i]), [sum(M[1 - i]), sum(M[0][j] for j in range(1)) + sum(M[1][j] for j in range(1)), M[i][0] * 3],
                  "Add the entries in row %d: %s = <b>%d</b>." % (i + 1, " + ".join(map(str, M[i])), sum(M[i])))
    j = r.randint(0, 2)
    return QN(pre + " How many %s were sold by the two shops together?" % items[j], M[0][j] + M[1][j], [sum(M[0]), M[0][j] * 2, M[0][(j + 1) % 3] + M[1][(j + 1) % 3]],
              "Add the entries in column %d: %d + %d = <b>%d</b>." % (j + 1, M[0][j], M[1][j], M[0][j] + M[1][j]))


def one_addscal(r):
    return wrap(us.one_add)(r) if r.random() < 0.5 else wrap(us.one_scal)(r)


# ------------------------------------------------------------ set 5: problems
def one_prob(r):
    kind = r.choice(["cost", "cost", "total", "week"])
    items = r.choice(ITEMS)
    if kind == "cost":
        Q = [[r.randint(2, 12) for _ in range(3)] for _ in range(2)]
        prices = r.choice([[2, 3, 5], [4, 2, 3], [6, 3, 2], [8, 5, 4], [12, 7, 5]])
        Pm = [[p] for p in prices]
        prod = mulm(Q, Pm)
        nm1, _, _ = P.next()
        nm2, _, _ = P.next()
        q = ("Q = %s shows the numbers of %s, %s and %s bought by %s (row 1) and %s (row 2). P = %s shows the price of each item in dollars. "
             "Find QP and say what it represents." % (mat(Q), items[0], items[1], items[2], nm1, nm2, mat(Pm)))
        right = "%s: the total amount each person spends" % mat(prod)
        wr = ["%s: the total amount each person spends" % mat([[sum(Q[0]) * sum(prices) // 3], [sum(Q[1]) * sum(prices) // 3]]),
              "%s: the number of items each person buys" % mat([[sum(Q[0])], [sum(Q[1])]]),
              "%s: the total amount each person spends" % mat([[prod[0][0] + 1], [prod[1][0]]])]
        return T(q, right, wr, "Row × column: %s = %d and %s = %d. QP gives <b>the total cost for each person</b>: %s and %s." % (
            " + ".join("%d × %d" % (a, b) for a, b in zip(Q[0], prices)), prod[0][0], " + ".join("%d × %d" % (a, b) for a, b in zip(Q[1], prices)), prod[1][0], sgd(prod[0][0]), sgd(prod[1][0])))
    if kind == "total":
        items = r.choice([("kopi", "teh", "kaya toast"), ("burgers", "drinks", "fries"), ("sandwiches", "muffins", "juices")])
        A = [[r.randint(3, 20) for _ in range(3)] for _ in range(2)]
        B_ = [[r.randint(3, 20) for _ in range(3)] for _ in range(2)]
        i, j = r.randint(0, 1), r.randint(0, 2)
        tot = addm(A, B_)
        q = ("Matrix A = %s shows a café's sales of %s, %s and %s on Saturday (row 1: morning, row 2: afternoon). B = %s shows the same for Sunday. "
             "Find the entry in row %d, column %d of A + B and say what it means." % (mat(A), items[0], items[1], items[2], mat(B_), i + 1, j + 1))
        what = "%s sold in the %s over the weekend" % (items[j], "mornings" if i == 0 else "afternoons")
        return T(q, "%d: %s" % (tot[i][j], what), ["%d: %s" % (A[i][j] * B_[i][j], what), "%d: %s" % (tot[1 - i][j], what), "%d: %s" % (tot[i][j], "%s sold on Sunday" % items[j])],
                 "%d + %d = <b>%d</b>, the number of <b>%s</b>." % (A[i][j], B_[i][j], tot[i][j], what))
    w = r.choice([2, 3, 4, 5])
    M = [[r.randint(5, 30) for _ in range(3)]]
    q = "A stall sells %s, %s and %s each day, as shown in D = %s. It sells the same amounts every day for %d days. Find %dD." % (items[0], items[1], items[2], mat(M), w, w)
    return T(q, mat([[w * x for x in M[0]]]), [mat([[x + w for x in M[0]]]), mat([[w * M[0][0]] + M[0][1:]]), mat([[w * sum(M[0])]])],
             "Multiply every entry by %d: <b>%s</b>." % (w, mat([[w * x for x in M[0]]])))


def build():
    sets = [S("Displaying and reading information", collect(one_info, 20, R)),
            S("Adding, subtracting and scalar multiples", collect(one_addscal, 20, R)),
            S("Order and when products are defined", collect(wrap(us.one_dim), 20, R)),
            S("Multiplying matrices", collect(wrap(us.one_mul), 20, R)),
            S("Problems", collect(one_prob, 20, R))]
    body = lesson(
        "<ul><li>A matrix with <i>m</i> rows and <i>n</i> columns has <b>order <i>m</i> × <i>n</i></b>.</li>"
        "<li>Add or subtract matrices of the <b>same order</b> entry by entry. A scalar multiplies every entry.</li>"
        "<li><b>AB</b> is defined only when the number of columns of A equals the number of rows of B. An <i>m</i> × <i>n</i> matrix times an <i>n</i> × <i>p</i> matrix gives an <i>m</i> × <i>p</i> matrix.</li>"
        "<li>Each entry of AB is a <b>row of A times a column of B</b>: multiply matching entries and add.</li></ul>",
        [("Find " + mat([[1, 2], [3, 4]]) + mat([[5], [6]]) + ".", ["Row 1: 1 × 5 + 2 × 6 = 17", "Row 2: 3 × 5 + 4 × 6 = 39"], mat([[17], [39]])),
         ("A is 2 × 3 and B is 3 × 1. What is the order of AB?", ["Inside numbers 3 and 3 match", "Outside numbers give the order"], "2 × 1")],
        ["Multiplying matrices entry by entry instead of row by column.",
         "Writing the order as columns × rows.",
         "Adding matrices of different orders.",
         "Thinking AB = BA. Matrix multiplication usually depends on the order."])
    faq = [("What is the order of a matrix?", "The number of rows × the number of columns. A matrix with 2 rows and 3 columns has order 2 × 3."),
           ("When can two matrices be multiplied?", "AB is defined when the number of columns in A equals the number of rows in B."),
           ("How do you multiply two matrices?", "For each entry, take a row of the first matrix and a column of the second, multiply matching entries and add the results."),
           ("What does a matrix product mean in a word problem?", "Multiplying a quantity matrix by a price matrix gives total costs: each row of quantities is multiplied by the prices and added.")]
    make(4, "matrices", 2, "N9",
         "Matrices: Order, Addition and Multiplication",
         "", "Matrices", "",
         "Free Secondary 4 maths worksheets on matrices: displaying information, order of a matrix, addition, subtraction, scalar multiples, matrix multiplication and real-world problems. 100 questions with answers.",
         "Multiply row by column; AB needs columns of A = rows of B.",
         "Add and subtract only matrices of the same order, entry by entry.",
         body, faq, sets, R)


if __name__ == "__main__":
    build()
