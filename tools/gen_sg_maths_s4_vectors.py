# -*- coding: utf-8 -*-
"""
SG Secondary 4 Maths: Vectors in Two Dimensions (MOE syllabus G7)
  python3 tools/gen_sg_maths_s4_vectors.py
Column vectors from a grid, magnitude √(x² + y²), adding, subtracting and multiplying by a scalar, position
vectors and translations, and parallel vectors.
Wrong answers come from real mistakes: writing (y, x) instead of (x, y), forgetting a minus sign for left or
down, computing OB − OA the wrong way round, adding the components for the magnitude, and adding the
scalar instead of multiplying.
"""
import math
import random
from fractions import Fraction as F
from sg_sec import num, S, make, lesson, collect, T, fig, fr, MINUS
from pc_common import mat
from g8_common import grid_svg

R = random.Random(840300)


def cv(x, y):
    return mat([[F(x)], [F(y)]]) if F(x).denominator == 1 and F(y).denominator == 1 else mat([[fv(x)], [fv(y)]])


def fv(v):
    v = F(v)
    return num(v) if v.denominator == 1 else (MINUS if v < 0 else "") + fr(abs(v.numerator), v.denominator)


def surd(n):
    k = 1
    for t in range(int(math.isqrt(n)), 1, -1):
        if n % (t * t) == 0:
            k = t
            break
    m = n // (k * k)
    if m == 1:
        return num(k)
    return ("" if k == 1 else num(k)) + "√" + num(m)


def arrow_grid(a, b, lo=-6, hi=6, name="AB"):
    svg = grid_svg(lo, hi, unit=22, label="vector %s on a grid" % name, ylo=lo, yhi=hi)
    Xp = lambda x: 22 + (x - lo) * 22
    Yp = lambda y: 22 + (hi - y) * 22
    x1, y1, x2, y2 = Xp(a[0]), Yp(a[1]), Xp(b[0]), Yp(b[1])
    d = math.hypot(x2 - x1, y2 - y1)
    ux, uy = (x2 - x1) / d, (y2 - y1) / d
    px, py = -uy, ux
    tip = (x2, y2)
    b1 = (x2 - ux * 11 + px * 6, y2 - uy * 11 + py * 6)
    b2 = (x2 - ux * 11 - px * 6, y2 - uy * 11 - py * 6)
    add = ("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='#1f6fd1' stroke-width='3'/>" % (x1, y1, x2 - ux * 8, y2 - uy * 8) +
           "<path d='M%.1f %.1f L%.1f %.1f L%.1f %.1f Z' fill='#1f6fd1'/>" % (tip[0], tip[1], b1[0], b1[1], b2[0], b2[1]) +
           "<circle cx='%.1f' cy='%.1f' r='4' fill='#c0392b'/><text x='%.1f' y='%.1f' font-size='15' font-weight='700' fill='#c0392b'>%s</text>" % (x1, y1, x1 - 16, y1 - 6, name[0]) +
           "<text x='%.1f' y='%.1f' font-size='15' font-weight='700' fill='#c0392b'>%s</text>" % (x2 + 6, y2 - 6, name[1]))
    return fig(svg.replace("</g></svg>", add + "</g></svg>"))


def vn(name):
    return "<span class='ov'>%s</span>" % name


# ------------------------------------------------------------ set 1: column vectors from a grid
def one_grid(r):
    while True:
        a = (r.randint(-5, 4), r.randint(-5, 4))
        b = (r.randint(-5, 5), r.randint(-5, 5))
        dx, dy = b[0] - a[0], b[1] - a[1]
        if dx and dy and dx != dy and abs(dx) + abs(dy) > 3:
            break
    pic = arrow_grid(a, b)
    right = cv(dx, dy)
    return T("Write %s as a column vector.%s" % (vn("AB"), pic), right, [cv(dy, dx), cv(-dx, -dy), cv(dx, -dy) if dy else cv(dx + 1, dy)],
             "From A to B: %s %d across (%s) and %s %d (%s). <b>%s</b>." % ("right" if dx > 0 else "left", abs(dx), num(dx), "up" if dy > 0 else "down", abs(dy), num(dy), right))


# ------------------------------------------------------------ set 2: magnitude
def one_mag(r):
    exact = r.random() < 0.5
    if exact:
        x, y = r.choice([(3, 4), (5, 12), (6, 8), (8, 15), (9, 12), (12, 5), (4, 3), (7, 24)])
        x, y = x * r.choice([1, -1]), y * r.choice([1, -1])
        right = num(int(math.hypot(x, y)))
    else:
        x, y = r.randint(-9, 9), r.randint(-9, 9)
        if x == 0 or y == 0 or int(math.hypot(x, y)) ** 2 == x * x + y * y:
            return None
        right = surd(x * x + y * y)
    v = cv(x, y)
    wr = [num(abs(x) + abs(y)), num(x * x + y * y), surd(abs(x * x - y * y)) if x * x != y * y else num(abs(x) + 1)]
    if right in wr:
        return None
    return T("Find the magnitude of the vector %s.%s" % (v, " Leave your answer in surd form if needed." if not exact else ""), right, wr,
             "|v| = √(%s² + %s²) = √%d = <b>%s</b>." % ("(%s)" % num(x) if x < 0 else num(x), "(%s)" % num(y) if y < 0 else num(y), x * x + y * y, right))


# ------------------------------------------------------------ set 3: operations
def one_ops(r):
    a = (r.randint(-6, 6), r.randint(-6, 6))
    b = (r.randint(-6, 6), r.randint(-6, 6))
    kind = r.choice(["add", "sub", "comb", "comb"])
    pre = "<b>a</b> = %s and <b>b</b> = %s." % (cv(*a), cv(*b))
    if kind == "add":
        res = (a[0] + b[0], a[1] + b[1])
        return T(pre + " Find <b>a</b> + <b>b</b>.", cv(*res), [cv(a[0] - b[0], a[1] - b[1]), cv(a[0] * b[0], a[1] * b[1]), cv(a[0] + b[1], a[1] + b[0])],
                 "Add the top numbers and the bottom numbers: <b>%s</b>." % cv(*res))
    if kind == "sub":
        res = (a[0] - b[0], a[1] - b[1])
        return T(pre + " Find <b>a</b> − <b>b</b>.", cv(*res), [cv(b[0] - a[0], b[1] - a[1]), cv(a[0] + b[0], a[1] + b[1]), cv(a[0] - b[0], a[1] + b[1])],
                 "Subtract each component: %s − (%s) = %s and %s − (%s) = %s. <b>%s</b>." % (num(a[0]), num(b[0]), num(res[0]), num(a[1]), num(b[1]), num(res[1]), cv(*res)))
    p, q = r.choice([2, 3, -2, 1]), r.choice([2, 3, -1, -3, 4])
    res = (p * a[0] + q * b[0], p * a[1] + q * b[1])
    ex = "%s<b>a</b> %s %s<b>b</b>" % ("" if p == 1 else num(p), "+" if q > 0 else MINUS, "" if abs(q) == 1 else num(abs(q)))
    return T(pre + " Find %s." % ex, cv(*res), [cv(p + a[0] + q + b[0], p + a[1] + q + b[1]), cv(p * a[0] + b[0], p * a[1] + b[1]), cv(p * a[0] - q * b[0], p * a[1] - q * b[1])],
             "Multiply each vector by its number, then add components: <b>%s</b>." % cv(*res))


# ------------------------------------------------------------ set 4: position vectors and translation
def one_pos(r):
    A = (r.randint(-6, 6), r.randint(-6, 6))
    B = (r.randint(-6, 6), r.randint(-6, 6))
    if A == B:
        return None
    kind = r.choice(["ab", "ab", "trans", "find", "mag"])
    if kind == "ab":
        res = (B[0] - A[0], B[1] - A[1])
        return T("The position vectors of A and B are %s = %s and %s = %s. Find %s." % (vn("OA"), cv(*A), vn("OB"), cv(*B), vn("AB")), cv(*res),
                 [cv(-res[0], -res[1]), cv(A[0] + B[0], A[1] + B[1]), cv(res[1], res[0]) if res[0] != res[1] else cv(res[0] + 1, res[1])],
                 "%s = %s − %s = %s − %s = <b>%s</b> (end minus start)." % (vn("AB"), vn("OB"), vn("OA"), cv(*B), cv(*A), cv(*res)))
    if kind == "trans":
        v = (r.randint(-5, 5), r.randint(-5, 5))
        res = (A[0] + v[0], A[1] + v[1])
        return T("The point P(%s, %s) is translated by the vector %s. Find the coordinates of its image." % (num(A[0]), num(A[1]), cv(*v)),
                 "(%s, %s)" % (num(res[0]), num(res[1])), ["(%s, %s)" % (num(A[0] - v[0]), num(A[1] - v[1])), "(%s, %s)" % (num(A[0] + v[1]), num(A[1] + v[0])), "(%s, %s)" % (num(v[0]), num(v[1]))],
                 "Add the vector to the coordinates: (%s + %s, %s + %s) = <b>(%s, %s)</b>." % (num(A[0]), "(%s)" % num(v[0]) if v[0] < 0 else num(v[0]), num(A[1]), "(%s)" % num(v[1]) if v[1] < 0 else num(v[1]), num(res[0]), num(res[1])))
    if kind == "find":
        ab = (r.randint(-6, 6), r.randint(-6, 6))
        Bp = (A[0] + ab[0], A[1] + ab[1])
        return T("%s = %s and %s = %s. Find the coordinates of B." % (vn("OA"), cv(*A), vn("AB"), cv(*ab)), "(%s, %s)" % (num(Bp[0]), num(Bp[1])),
                 ["(%s, %s)" % (num(A[0] - ab[0]), num(A[1] - ab[1])), "(%s, %s)" % (num(ab[0]), num(ab[1])), "(%s, %s)" % (num(ab[0] - A[0]), num(ab[1] - A[1]))],
                 "%s = %s + %s = <b>%s</b>, so B is <b>(%s, %s)</b>." % (vn("OB"), vn("OA"), vn("AB"), cv(*Bp), num(Bp[0]), num(Bp[1])))
    res = (B[0] - A[0], B[1] - A[1])
    n = res[0] ** 2 + res[1] ** 2
    right = surd(n)
    wr = [surd(B[0] ** 2 + B[1] ** 2) if B[0] ** 2 + B[1] ** 2 != n else num(abs(res[0]) + abs(res[1]) + 1), num(abs(res[0]) + abs(res[1])), num(n)]
    if right in wr or len(set(wr)) < 3:
        return None
    return T("A is (%s, %s) and B is (%s, %s). Find |%s|." % (num(A[0]), num(A[1]), num(B[0]), num(B[1]), vn("AB")), right, wr,
             "%s = %s, so |%s| = √(%s² + %s²) = <b>%s</b>." % (vn("AB"), cv(*res), vn("AB"), num(res[0]), num(res[1]), right))


# ------------------------------------------------------------ set 5: parallel vectors and unknowns
def one_par(r):
    kind = r.choice(["k", "k", "which", "eq", "magk"])
    if kind == "k":
        x, y = r.choice([(2, 3), (1, -2), (3, 4), (-2, 5), (4, -1), (3, -2), (1, 3)])
        m = r.choice([2, 3, -2, 4, -3])
        unknown = r.choice([0, 1])
        v2 = [m * x, m * y]
        shown = list(v2)
        shown[unknown] = "<i>k</i>"
        q = "%s is parallel to %s. Find <i>k</i>." % (cv(x, y), mat([[shown[0]], [shown[1]]]))
        right = v2[unknown]
        other = 1 - unknown
        return T(q, num(right), [num(m * (x if unknown == 1 else y)) if m * (x if unknown == 1 else y) != right else num(right + 1), num(right + m), num(-right) if right else "1"],
                 "Parallel vectors are multiples of each other. The %s component is %s times as big (%s ÷ %s), so <i>k</i> = %s × %s = <b>%s</b>." % (
                     "top" if other == 0 else "bottom", num(m), num(v2[other]), num([x, y][other]), num(m), ("(%s)" % num([x, y][unknown])) if [x, y][unknown] < 0 else num([x, y][unknown]), num(right)))
    if kind == "which":
        x, y = r.choice([(2, 3), (1, -2), (3, 4), (-2, 5), (4, -1)])
        m = r.choice([2, 3, -2, -1])
        right = cv(m * x, m * y)
        return T("Which vector is parallel to %s?" % cv(x, y), right, [cv(m * y, m * x), cv(x + m, y + m), cv(m * x, -m * y)],
                 "%s = %s × %s, a scalar multiple, so it is parallel: <b>%s</b>." % (right, num(m), cv(x, y), right))
    if kind == "eq":
        a, b = r.randint(-5, 5), r.randint(-5, 5)
        p, q = r.randint(1, 4), r.randint(-6, 6)
        # (p x + q, y − 2) = (a', b)
        x = r.randint(-4, 5)
        top = p * x + q
        yv = r.randint(-5, 5)
        return T("Given that %s = %s, find <i>x</i> and <i>y</i>." % (mat([["%s<i>x</i> %s %s" % ("" if p == 1 else num(p), "+" if q >= 0 else MINUS, num(abs(q)))], ["<i>y</i> − 2"]]), cv(top, yv)),
                 "<i>x</i> = %s, <i>y</i> = %s" % (num(x), num(yv + 2)), ["<i>x</i> = %s, <i>y</i> = %s" % (num(x), num(yv - 2)), "<i>x</i> = %s, <i>y</i> = %s" % (fv(F(top + q, p)), num(yv + 2)) if F(top + q, p) != x else "<i>x</i> = %s, <i>y</i> = %s" % (num(x + 1), num(yv + 2)), "<i>x</i> = %s, <i>y</i> = %s" % (num(top), num(yv))],
                 "Equal vectors have equal components: %s<i>x</i> %s %s = %s gives <i>x</i> = %s, and <i>y</i> − 2 = %s gives <i>y</i> = %s. <b><i>x</i> = %s, <i>y</i> = %s</b>." % (
                     "" if p == 1 else num(p), "+" if q >= 0 else MINUS, num(abs(q)), num(top), num(x), num(yv), num(yv + 2), num(x), num(yv + 2)))
    x, y = r.choice([(3, 4), (5, 12), (6, 8), (8, 15), (12, 5)])
    q = "The vector %s has magnitude %d, and <i>k</i> &gt; 0. Find <i>k</i>." % (mat([[num(x)], ["<i>k</i>"]]), int(math.hypot(x, y)))
    h = int(math.hypot(x, y))
    return T(q, num(y), [num(h - x), num(h * h - x * x), num(h + x)],
             "√(%d² + <i>k</i>²) = %d, so <i>k</i>² = %d − %d = %d and <i>k</i> = <b>%d</b>." % (x, h, h * h, x * x, y * y, y))


def build():
    sets = [S("Column vectors from a grid", collect(one_grid, 20, R)),
            S("Magnitude of a vector", collect(one_mag, 20, R)),
            S("Adding, subtracting and scalar multiples", collect(one_ops, 20, R)),
            S("Position vectors and translations", collect(one_pos, 20, R)),
            S("Parallel and equal vectors", collect(one_par, 20, R))]
    body = lesson(
        "<ul><li>A <b>column vector</b> gives the move across (top number: + right, − left) and the move up or down (bottom number: + up, − down).</li>"
        "<li>The <b>magnitude</b> of a vector with components <i>x</i> and <i>y</i> is √(<i>x</i>² + <i>y</i>²).</li>"
        "<li>Add, subtract and multiply by a scalar component by component.</li>"
        "<li>For position vectors, <span class='ov'>AB</span> = <span class='ov'>OB</span> − <span class='ov'>OA</span> (end minus start).</li>"
        "<li>Two vectors are <b>parallel</b> if one is a scalar multiple of the other.</li></ul>",
        [("A is (1, 2) and B is (4, −2). Find AB and |AB|.", ["AB = (4 − 1, −2 − 2) = (3, −4)", "|AB| = √(9 + 16)"], "(3, −4) and 5"),
         ("Find k if (2, k) is parallel to (6, 9).", ["(6, 9) = 3 × (2, 3)"], "k = 3")],
        ["Writing the vertical move on top. The horizontal move goes on top.",
         "Forgetting the minus sign for a move left or down.",
         "Working out OA − OB for AB. It is OB − OA.",
         "Adding the components for the magnitude instead of using √(x² + y²)."])
    faq = [("What is a column vector?", "Two numbers written one above the other: the top number is the horizontal move and the bottom number is the vertical move."),
           ("How do you find the magnitude of a vector?", "Use Pythagoras' theorem: √(x² + y²), where x and y are the components."),
           ("How do you find AB from position vectors?", "Subtract the start from the end: AB = OB − OA."),
           ("How do you know two vectors are parallel?", "One is a number times the other. For example (4, 6) = 2 × (2, 3), so they are parallel.")]
    make(4, "vectors", 3, "G7",
         "Vectors: Column Vectors, Magnitude and Position Vectors",
         "", "Vectors", "",
         "Free Secondary 4 maths worksheets on vectors in two dimensions: column vectors, magnitude, adding and subtracting vectors, scalar multiples, position vectors, translations and parallel vectors. 100 questions with answers.",
         "A column vector shows the move across (top) and up or down (bottom).",
         "Magnitude = √(x² + y²); AB = OB − OA; parallel vectors are scalar multiples.",
         body, faq, sets, R)


if __name__ == "__main__":
    build()
