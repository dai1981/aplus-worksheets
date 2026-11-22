# -*- coding: utf-8 -*-
"""
India Class 11 Maths, NCERT Chapter 1: Sets (CBSE Unit I Sets and Functions)
  python3 tools/gen_in_maths_c11_sets.py
Roster and set-builder form, empty, finite and equal sets, subsets and intervals, the number of subsets, union,
intersection, difference and complement, Venn diagrams and n(A ∪ B) (own makers and SG Secondary 4 set makers).
Wrong answers come from real mistakes: forgetting the empty set and the set itself among the subsets, mixing up
⊂ and ∈, using the wrong bracket for an interval, mixing up A − B and B − A, and adding n(A) + n(B) without
taking away n(A ∩ B).
"""
import random
from in_sr import U, T2, use, X, nz
import gen_sg_maths_s4_sets_and_venn_diagrams as sgs

R = random.Random(911101)
FIX = [("ξ", "U"), ("Chinese chess", "chess")]
notation = use(sgs, "one_notation", R, FIX)
ops = use(sgs, "one_ops", R, FIX)
read = use(sgs, "one_read", R, FIX)
shade = use(sgs, "one_shade", R, FIX)
prob = use(sgs, "one_prob", R, FIX)


def st(xs):
    return "{" + ", ".join(str(x) for x in xs) + "}" if xs else "φ"


BUILD = [
    ("x is a prime number less than %d", lambda n: [p for p in range(2, n) if all(p % d for d in range(2, p))], [12, 15, 20, 24]),
    ("x is a natural number and x divides %d", lambda n: [d for d in range(1, n + 1) if n % d == 0], [12, 18, 20, 28, 30]),
    ("x is an odd natural number less than %d", lambda n: list(range(1, n, 2)), [8, 10, 12, 14]),
    ("x = n², n ∈ N and n ≤ %d", lambda n: [k * k for k in range(1, n + 1)], [4, 5, 6]),
    ("x ∈ Z and −%d ≤ x &lt; 3", lambda n: list(range(-n, 3)), [2, 3, 4]),
    ("x is a natural number and x² &lt; %d", lambda n: [k for k in range(1, 10) if k * k < n], [20, 30, 40, 50, 70]),
]


def one_roster(r):
    t, f, ns = r.choice(BUILD)
    n = r.choice(ns)
    right = f(n)
    show = lambda xs: st([str(x).replace("-", "−") for x in xs])
    wr = [show(right[:-1]), show(right + [right[-1] + (right[-1] - right[-2] if len(right) > 1 else 1)]), show(right[1:])]
    if "prime" in t:
        wr[2] = show([1] + right)
    if "divides" in t:
        wr[2] = show(right[1:-1])
    return T2("Write the set A = {x : %s} in roster form." % (t % n), show(right), wr,
              "List every element that fits the rule, once each: A = <b>%s</b>." % show(right))


def one_subsets(r):
    n = r.randint(2, 7)
    els = r.sample(list("abcdepqrs"), n) if r.random() < 0.5 else sorted(r.sample(range(1, 20), n))
    A = st(els)
    k = r.choice(["sub", "proper", "power", "elements"])
    if k == "sub":
        return T2("How many subsets does A = %s have?" % A, str(2 ** n), [str(2 ** n - 1), str(2 * n), str(n * n)],
                  "A set with %d elements has 2<sup>%d</sup> = <b>%d</b> subsets (including φ and A itself)." % (n, n, 2 ** n))
    if k == "proper":
        return T2("How many proper subsets does A = %s have?" % A, str(2 ** n - 1), [str(2 ** n), str(2 ** n - 2), str(2 * n)],
                  "There are 2<sup>%d</sup> = %d subsets; all except A itself are proper: <b>%d</b>." % (n, 2 ** n, 2 ** n - 1))
    if k == "power":
        return T2("If A = %s, how many elements does the power set P(A) have?" % A, str(2 ** n), [str(n), str(2 ** n - 1), str(n * n)],
                  "P(A) is the set of all subsets of A, so n[P(A)] = 2<sup>%d</sup> = <b>%d</b>." % (n, 2 ** n))
    m = 2 ** n
    return T2("A power set P(A) has %d elements. How many elements does A have?" % m, str(n), [str(m // 2), str(n + 1), str(m - 1)],
              "n[P(A)] = 2<sup>n</sup> = %d, so n = <b>%d</b>." % (m, n))


def one_interval(r):
    a = r.randint(-9, 5)
    b = a + r.randint(2, 9)
    lo, hi = r.choice([("&lt;", "&lt;"), ("≤", "≤"), ("≤", "&lt;"), ("&lt;", "≤")])
    L = "(" if lo == "&lt;" else "["
    H = ")" if hi == "&lt;" else "]"
    A, B = str(a).replace("-", "−"), str(b).replace("-", "−")
    right = "%s%s, %s%s" % (L, A, B, H)
    other = lambda l, h: "%s%s, %s%s" % (l, A, B, h)
    wr = [other("[" if L == "(" else "(", H), other(L, "]" if H == ")" else ")"), other("[" if L == "(" else "(", "]" if H == ")" else ")")]
    if r.random() < 0.5:
        return T2("Write {x : x ∈ R, %s %s x %s %s} as an interval." % (A, lo, hi, B), right, wr,
                  "A round bracket leaves the end point out (&lt;) and a square bracket keeps it in (≤): <b>%s</b>." % right)
    return T2("Which set is the interval %s?" % right, "{x : %s %s x %s %s}" % (A, lo, hi, B),
              ["{x : %s %s x %s %s}" % (A, l2, h2, B) for l2, h2 in [("≤", "≤"), ("&lt;", "&lt;"), ("≤", "&lt;"), ("&lt;", "≤")] if (l2, h2) != (lo, hi)],
              "( or ) means the end point is not included, [ or ] means it is: <b>{x : %s %s x %s %s}</b>." % (A, lo, hi, B))


def one_diff(r):
    U_ = list(range(1, 11))
    A = sorted(r.sample(U_, r.randint(3, 6)))
    B = sorted(r.sample(U_, r.randint(3, 6)))
    AB, BA, I, Un = [x for x in A if x not in B], [x for x in B if x not in A], [x for x in A if x in B], sorted(set(A) | set(B))
    k = r.choice(["ab", "ba", "comp", "compu"])
    if k == "ab":
        return T2("A = %s and B = %s. Find A − B." % (st(A), st(B)), st(AB), [st(BA), st(I), st(Un)],
                  "A − B keeps the elements of A that are not in B: <b>%s</b>." % st(AB))
    if k == "ba":
        return T2("A = %s and B = %s. Find B − A." % (st(A), st(B)), st(BA), [st(AB), st(I), st(Un)],
                  "B − A keeps the elements of B that are not in A: <b>%s</b>." % st(BA))
    if k == "comp":
        c = [x for x in U_ if x not in A]
        return T2("U = {1, 2, 3, …, 10} and A = %s. Find A′." % st(A), st(c), [st(A), st([x for x in U_ if x not in B]), st(c[1:])],
                  "A′ = U − A, the elements of U not in A: <b>%s</b>." % st(c))
    c = [x for x in U_ if x not in Un]
    return T2("U = {1, 2, 3, …, 10}, A = %s and B = %s. Find (A ∪ B)′." % (st(A), st(B)), st(c), [st(Un), st([x for x in U_ if x not in I]), st(I)],
              "A ∪ B = %s, so (A ∪ B)′ = <b>%s</b> (De Morgan: it equals A′ ∩ B′)." % (st(Un), st(c)))


def one_count(r):
    a, b = r.randint(15, 60), r.randint(15, 60)
    i = r.randint(3, min(a, b) - 2)
    u = a + b - i
    subj = r.choice([("Hindi", "English"), ("tea", "coffee"), ("cricket", "football"), ("Physics", "Chemistry"), ("newspaper H", "newspaper T")])
    k = r.choice(["union", "inter", "only"])
    if k == "union":
        return T2("In a group, %d people like %s, %d like %s and %d like both. How many like at least one of them?" % (a, subj[0], b, subj[1], i), str(u),
                  [str(a + b), str(a + b - 2 * i), str(u - i)], "n(A ∪ B) = n(A) + n(B) − n(A ∩ B) = %d + %d − %d = <b>%d</b>." % (a, b, i, u))
    if k == "inter":
        return T2("%d students each like %s or %s or both. %d like %s and %d like %s. How many like both?" % (u, subj[0], subj[1], a, subj[0], b, subj[1]), str(i),
                  [str(a + b), str(u - a), str(abs(a - b))], "n(A ∩ B) = n(A) + n(B) − n(A ∪ B) = %d + %d − %d = <b>%d</b>." % (a, b, u, i))
    return T2("%d people like %s, %d like %s and %d like both. How many like %s only?" % (a, subj[0], b, subj[1], i, subj[0]), str(a - i),
              [str(a), str(i), str(u - a)], "n(A − B) = n(A) − n(A ∩ B) = %d − %d = <b>%d</b>." % (a, i, a - i))


def one_type(r):
    k = r.choice(["empty", "finite", "equal", "sub"])
    if k == "empty":
        opts = [("{x : x is a natural number and x &lt; 1}", True), ("{x : x is an even prime number}", False), ("{0}", False),
                ("{x : x ∈ N and 2 &lt; x &lt; 3}", True), ("{x : x² = 4 and x is odd}", True), ("{x : x is a whole number less than 1}", False)]
        e = [o for o in opts if o[1]]
        ne = [o for o in opts if not o[1]]
        right = r.choice(e)[0]
        return T2("Which of these is the empty set φ?", right, [o[0] for o in ne],
                  "%s has no elements. {0} has one element (0), and there is exactly one even prime (2)." % right)
    if k == "finite":
        right = r.choice(["{x : x is a month of the year}", "{x : x ∈ N and x &lt; 100}", "the set of states of India", "{x : x is a factor of 360}"])
        return T2("Which set is finite?", right, ["{x : x ∈ N and x is even}", "the set of lines through a point", "{x : x ∈ Z and x &lt; 5}", "the set of points on a circle"],
                  "<b>%s</b> has a definite number of elements; the others go on without end." % right)
    if k == "equal":
        n = r.choice([6, 8, 10, 12, 15])
        d = [x for x in range(1, n + 1) if n % x == 0]
        return T2("Which set is equal to {x : x is a factor of %d}?" % n, st(d), [st(d[:-1]), st([x for x in range(1, n + 1, 2)]), st(d + [2 * n])],
                  "Equal sets have exactly the same elements: <b>%s</b>." % st(d))
    a = r.sample([1, 2, 3, 4, 5], 2)
    A = st(sorted(a))
    return T2("A = {1, 2, 3, 4, 5}. Which statement is true?", "%s ⊂ A" % A, ["%s ∈ A" % A, "%d ⊂ A" % a[0], "A ⊂ %s" % A],
              "%s is a set whose elements are all in A, so it is a subset: <b>%s ⊂ A</b>. ∈ is used for single elements, as in %d ∈ A." % (A, A + " ⊂ A", a[0]))


U(11, 1, "sets", 1, "SF", "Sets: Subsets, Intervals, Venn Diagrams and Set Operations", "sets",
  "Sets and their representations; empty, finite, infinite and equal sets; subsets, subsets of the set of real numbers (intervals); Venn diagrams; union, intersection, difference and complement of sets and their properties (summary of the CBSE syllabus)",
  "Class 11 Sets worksheet (NCERT Chapter 1): roster and set-builder form, subsets, power set, intervals, union, intersection, difference, complement and Venn diagrams. 100 questions with answers.",
  "A set with n elements has 2ⁿ subsets.", "n(A ∪ B) = n(A) + n(B) − n(A ∩ B).",
  "<ul><li><b>Roster form</b> lists the elements: {2, 3, 5, 7}. <b>Set-builder form</b> gives the rule: {x : x is a prime less than 10}.</li>"
  "<li>B ⊂ A when every element of B is in A. A set with n elements has 2<sup>n</sup> subsets; the power set P(A) has 2<sup>n</sup> elements.</li>"
  "<li>Intervals: (a, b) leaves out both ends, [a, b] keeps both, [a, b) keeps only a.</li>"
  "<li>A ∪ B (in A or B), A ∩ B (in both), A − B (in A but not B), A′ = U − A. De Morgan: (A ∪ B)′ = A′ ∩ B′.</li></ul>",
  [("A = {1, 2, 3}. How many subsets does A have?", ["φ, {1}, {2}, {3}, {1, 2}, {1, 3}, {2, 3}, {1, 2, 3}", "2³ = 8"], "8")],
  ["Forgetting φ and A itself when counting subsets.", "Writing {1} ∈ A instead of {1} ⊂ A.", "Adding n(A) + n(B) without subtracting n(A ∩ B)."],
  [("What is the difference between ⊂ and ∈?", "∈ links an element to a set (2 ∈ A); ⊂ links a set to a set ({2} ⊂ A)."),
   ("Is φ a subset of every set?", "Yes. The empty set is a subset of every set, and every set is a subset of itself.")],
  [("Representing sets", [(one_roster, 12), (one_type, 5), (notation, 3)]),
   ("Subsets and intervals", [(one_subsets, 10), (one_interval, 7), (notation, 3)]),
   ("Union, intersection and difference", [(ops, 8), (one_diff, 12)]),
   ("Venn diagrams", [(read, 10), (shade, 6), (one_diff, 4)]),
   ("Counting problems", [(one_count, 12), (prob, 8)])], 911101)
