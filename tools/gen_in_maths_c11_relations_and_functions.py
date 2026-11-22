# -*- coding: utf-8 -*-
"""
India Class 11 Maths, NCERT Chapter 2: Relations and Functions (CBSE Unit I Sets and Functions)
  python3 tools/gen_in_maths_c11_relations_and_functions.py
Cartesian products and equal ordered pairs, the number of relations, domain and range of a relation, deciding if a
relation is a function, the modulus, signum and greatest integer functions, domain and range of real functions
(own makers and TX Algebra II makers), and the sum, difference and product of functions (US Algebra 2 makers).
Wrong answers come from real mistakes: n(A) + n(B) for n(A × B), 2^(m + n) relations, mixing up domain and range,
calling a relation a function when one element has two images, and [−2.5] = −2.
"""
import random, math
from in_sr import U, T2, use, X, nz, sn
from in_common import num, comma
import gen_us_math_a2_composition_and_inverse_functions as usc
import gen_ustx_math_a2_domain_range_notation as txd

R = random.Random(911102)
fops = use(usc, "one_ops", R)
dom = use(txd, "one_dom", R)
rng = use(txd, "one_rng", R)


def st(xs):
    return "{" + ", ".join(xs) + "}"


def pr(a, b):
    return "(%s, %s)" % (num(a), num(b))


def one_cart(r):
    k = r.choice(["count", "list", "pair", "count2"])
    if k == "count":
        m, n = r.randint(2, 6), r.randint(2, 6)
        return T2("n(A) = %d and n(B) = %d. How many elements does A × B have?" % (m, n), str(m * n), [str(m + n), str(2 ** (m * n)), str(m ** n)],
                  "n(A × B) = n(A) × n(B) = %d × %d = <b>%d</b>." % (m, n, m * n))
    if k == "count2":
        m = r.randint(2, 5)
        return T2("A has %d elements. How many elements does A × A × A have?" % m, str(m ** 3), [str(3 * m), str(m * m), str(3 ** m)],
                  "n(A × A × A) = %d × %d × %d = <b>%d</b>." % (m, m, m, m ** 3))
    if k == "list":
        A = sorted(r.sample(range(1, 8), 2))
        B = r.sample(list("pqrsxyz"), 2)
        right = st(["(%d, %s)" % (a, b) for a in A for b in B])
        return T2("A = {%d, %d} and B = {%s, %s}. Find A × B." % (A[0], A[1], B[0], B[1]), right,
                  [st(["(%s, %d)" % (b, a) for b in B for a in A]), st(["(%d, %s)" % (A[0], B[0]), "(%d, %s)" % (A[1], B[1])]), st(["(%d, %d)" % (A[0], A[1]), "(%s, %s)" % (B[0], B[1])])],
                  "A × B is the set of all ordered pairs (a, b) with a from A first: <b>%s</b>." % right)
    x, y = r.randint(-6, 9), r.randint(-6, 9)
    a, b = r.randint(1, 5), r.randint(-5, 5)
    c, d = r.randint(1, 4), r.randint(-5, 5)
    p, q = a * x + b, c * y + d
    lhs = "(%s, %s)" % ("%s%s" % ("" if a == 1 else a, X) + ("" if b == 0 else (" + %d" % b if b > 0 else " − %d" % -b)),
                       "%s<i>y</i>" % ("" if c == 1 else c) + ("" if d == 0 else (" + %d" % d if d > 0 else " − %d" % -d)))
    return T2("If %s = %s, find %s and <i>y</i>." % (lhs, pr(p, q), X), "%s = %s, <i>y</i> = %s" % (X, num(x), num(y)),
              ["%s = %s, <i>y</i> = %s" % (X, num(y), num(x)), "%s = %s, <i>y</i> = %s" % (X, num(p), num(q)), "%s = %s, <i>y</i> = %s" % (X, num(x + 1), num(y - 1))],
              "Equal ordered pairs have equal first parts and equal second parts: %s and %s, so <b>%s = %s, <i>y</i> = %s</b>." % (lhs[1:].split(", ")[0] + " = " + num(p), lhs.split(", ")[1][:-1] + " = " + num(q), X, num(x), num(y)))


def one_nrel(r):
    m, n = r.randint(1, 4), r.randint(2, 4)
    if m * n > 12:
        return None
    if r.random() < 0.6:
        return T2("A has %d elements and B has %d elements. How many relations are there from A to B?" % (m, n), comma(2 ** (m * n)),
                  [str(m * n), comma(2 ** (m + n)), comma(2 ** (m * n) - 1)],
                  "A relation is any subset of A × B, which has %d elements, so there are 2<sup>%d</sup> = <b>%s</b> relations." % (m * n, m * n, comma(2 ** (m * n))))
    return T2("A = {1, 2, …, %d}. How many relations are there on A (from A to A)?" % n, comma(2 ** (n * n)), [str(n * n), comma(2 ** (2 * n)), str(2 ** n)],
              "A × A has %d elements, so there are 2<sup>%d</sup> = <b>%s</b> relations." % (n * n, n * n, comma(2 ** (n * n))))


RULES = [("<i>y</i> = %s + %d", lambda x, k: x + k), ("<i>y</i> = %d%s", lambda x, k: k * x), ("<i>y</i> = %s² + %d", lambda x, k: x * x + k)]


def one_dr(r):
    xs = sorted(r.sample(range(1, 9), r.randint(3, 5)))
    t, f = r.choice([(0, None), (1, None), (2, None)]), None
    i = r.randrange(3)
    k = r.randint(1, 4) if i != 1 else r.randint(2, 4)
    form, f = RULES[i]
    rule = form % ((X, k) if i != 1 else (k, X))
    pairs = [(x, f(x, k)) for x in xs]
    D = st([str(x) for x, _ in pairs])
    Rg = st([str(y) for y in sorted(set(y for _, y in pairs))])
    rel = st([pr(a, b) for a, b in pairs])
    if r.random() < 0.5:
        return T2("R = {(%s, <i>y</i>) : %s, %s ∈ %s}. What is the range of R?" % (X, rule, X, D), Rg, [D, st([str(y) for _, y in pairs][:-1]), st([str(x + k) for x in xs]) if i else st([str(k * x) for x in xs])],
                  "R = %s. The range is the set of second elements: <b>%s</b>." % (rel, Rg))
    return T2("R = %s. What is the domain of R?" % rel, D, [Rg, st([str(x) for x in xs[:-1]]), st([str(x) for x in xs] + [str(xs[-1] + 1)])],
              "The domain is the set of first elements: <b>%s</b>." % D)


def one_isfn(r):
    xs = r.sample(range(1, 9), 4)
    ys = [r.randint(1, 9) for _ in xs]
    good = [pr(a, b) for a, b in zip(xs, ys)]
    bad = good[:3] + [pr(xs[0], ys[0] + r.randint(1, 3))]
    same = [pr(a, ys[0]) for a in xs]
    k = r.random()
    if k < 0.5:
        r.shuffle(bad)
        return T2("Is R = %s a function?" % st(bad), "No, because %d has two images" % xs[0], ["Yes, because every element has an image", "Yes, because no two elements share an image",
                  "No, because two elements have the same image"],
                  "In a function each first element has exactly one image. %d appears with two different second elements, so <b>R is not a function</b>." % xs[0])
    return T2("Is R = %s a function?" % st(same), "Yes, every first element has exactly one image", ["No, because every element has the same image", "No, because the range has one element",
              "No, because the domain has 4 elements"],
              "Different elements may share an image; what matters is that no first element appears twice. <b>R is a function</b>.")


def one_special(r):
    from fractions import Fraction as Fr
    k = r.choice(["floor", "floor", "mod", "sgn"])
    if k == "floor":
        v = Fr(r.randint(-60, 60), 10)
        if v.denominator == 1:
            return None
        fl = math.floor(v)
        tr = int(v)
        wr = [num(fl + 1), num(fl - 1) if tr == fl else num(tr), num(fl + 2) if tr == fl + 1 else num(fl - 1)]
        return T2("f(%s) = [%s] is the greatest integer function. Find f(%s)." % (X, X, num(v)), num(fl), wr,
                  "[%s] is the greatest integer that is less than or equal to %s, so the answer is <b>%s</b>." % (X, num(v), num(fl)))
    if k == "mod":
        a, c = r.randint(-9, 9), r.randint(-9, 9)
        if a == c:
            return None
        sh = (" − %d" % c) if c > 0 else (" + %d" % -c if c < 0 else "")
        right = abs(a - c)
        return T2("f(%s) = |%s%s|. Find f(%s)." % (X, X, sh, num(a)), num(right), [num(a - c) if a - c < 0 else num(-(a - c)), num(abs(a + c)) if abs(a + c) != right else num(right + 1), num(abs(a) + abs(c)) if abs(a) + abs(c) != right else num(right + 2)],
                  "f(%s) = |%s| = <b>%s</b>." % (num(a), num(a - c), num(right)))
    v = r.choice([-9, -7, -4, -3, -1, 0, 2, 5, 6, 9]) if r.random() < 0.6 else None
    if v is None:
        a = r.randint(-9, 9)
        if a == 0:
            return None
        s_ = (a > 0) - (a < 0)
        return T2("f is the signum function. Find f(%s) + f(%s)." % (num(a), num(-a)), "0", ["2", MINUS_ + "2", "1"],
                  "One of the numbers is positive and one is negative, so the sum is 1 + (−1) = <b>0</b>.")
    s_ = (v > 0) - (v < 0)
    right = num(s_)
    wr = [x for x in [MINUS_ + "1", "0", "1", num(v)] if x != right][:3]
    if len(wr) < 3:
        wr.append("2")
    return T2("f is the signum function. Find f(%s)." % num(v), right, wr,
              "The signum function gives 1 for positive numbers, 0 for 0 and −1 for negative numbers: <b>%s</b>." % right)


MINUS_ = "\u2212"


U(11, 2, "relations-and-functions", 2, "SF", "Relations and Functions: Cartesian Products, Domain and Range", "relations and functions",
  "Ordered pairs, Cartesian product of sets, number of elements in the Cartesian product of two finite sets; definition of relation, pictorial diagrams, domain, co-domain and range of a relation; function as a special type of relation; domain, co-domain and range of a function; real valued functions and their graphs: constant, identity, polynomial, rational, modulus, signum and greatest integer functions; sum, difference, product and quotients of functions (summary of the CBSE syllabus)",
  "Class 11 Relations and Functions worksheet (NCERT Chapter 2): Cartesian products, number of relations, domain and range, functions, modulus, signum and greatest integer functions, and algebra of functions. 100 questions with answers.",
  "A function gives each element of the domain exactly one image.", "n(A × B) = n(A) × n(B); there are 2^(mn) relations from A to B.",
  "<ul><li>A × B = {(a, b) : a ∈ A, b ∈ B}. If n(A) = m and n(B) = n, then n(A × B) = mn.</li>"
  "<li>A <b>relation</b> from A to B is any subset of A × B, so there are 2<sup>mn</sup> of them.</li>"
  "<li>The <b>domain</b> is the set of first elements, the <b>range</b> the set of second elements.</li>"
  "<li>A relation is a <b>function</b> when every element of the domain has exactly one image.</li>"
  "<li>Special functions: |x| (modulus), signum (1, 0 or −1) and [x] (greatest integer ≤ x).</li></ul>",
  [("A = {1, 2}, B = {3, 4, 5}. How many relations are there from A to B?", ["n(A × B) = 2 × 3 = 6", "2⁶ = 64"], "64")],
  ["Using n(A) + n(B) for n(A × B).", "Swapping domain and range.", "Thinking [−2.5] = −2 (it is −3)."],
  [("Is every relation a function?", "No. A relation is a function only if each element of the domain has exactly one image."),
   ("What is the range of the greatest integer function?", "The set of integers Z.")],
  [("Cartesian products", [(one_cart, 20)]),
   ("Relations", [(one_nrel, 8), (one_dr, 12)]),
   ("Functions", [(one_isfn, 6), (one_special, 14)]),
   ("Domain and range", [(dom, 10), (rng, 10)]),
   ("Algebra of functions", [(fops, 14), (one_dr, 6)])], 911102)
