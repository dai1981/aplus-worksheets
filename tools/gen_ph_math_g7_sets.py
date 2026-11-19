# -*- coding: utf-8 -*-
"""
Philippines Grade 7 Math (MATATAG): Sets, Subsets, Union and Intersection with Venn Diagrams (Grade 7: Number and Algebra)
  python3 tools/gen_ph_math_g7_sets.py
Set notation, subsets and the number of subsets, union and intersection (own makers and Singapore Secondary 4 makers),
and reading and shading Venn diagrams.
Wrong answers come from real mistakes: mixing up union and intersection, forgetting the empty set as a subset, and
counting the overlap twice.
"""
import ph_common
from ph_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, peso, words)
import random
import gen_sg_maths_s4_sets_and_venn_diagrams as sgv
adopt(sgv)
if hasattr(sgv, 'R'): sgv.R = random.Random(707130)
ph_common.GRADE = "grade-7"

def uniq(fn):
    """Never give the same question twice, even with other wrong answers."""
    seen = set()
    def f(r):
        it = fn(r)
        if it is None or it["q"] in seen:
            raise AssertionError("repeat")
        seen.add(it["q"])
        return it
    f.__name__ = fn.__name__
    return f


def one_sub(r):
    U = r.sample(["a", "b", "c", "d", "e", "1", "2", "3", "4", "5", "6", "7", "8"], 0)
    n = r.randint(1, 5)
    els = r.choice([["a", "b", "c", "d", "e"], ["1", "2", "3", "4", "5"], ["red", "blue", "green", "yellow", "white"], ["x", "y", "z", "w", "v"]])[:n]
    A = "{%s}" % ", ".join(els)
    kind = r.choice(["count", "count", "proper", "is"])
    if kind == "count":
        return mcq("How many subsets does A = %s have?" % A, 2 ** n, [2 * n, n, 2 ** n - 1, n * n if n * n != 2 ** n else n + 1],
                   "A set with %d elements has 2<sup>%d</sup> = <b>%d</b> subsets, including the empty set and A itself." % (n, n, 2 ** n))
    if kind == "proper":
        if n < 2:
            raise AssertionError
        return mcq("How many <b>proper</b> subsets does A = %s have?" % A, 2 ** n - 1, [2 ** n, 2 * n, n],
                   "All subsets: 2<sup>%d</sup> = %d. A proper subset is any subset except A itself: %d − 1 = <b>%d</b>." % (n, 2 ** n, 2 ** n, 2 ** n - 1))
    if n < 3:
        raise AssertionError
    sub = r.sample(els, r.randint(1, n - 1))
    other = [x for x in ["f", "9", "black", "u"] if x not in els][0]
    good = "{%s} ⊆ A" % ", ".join(sorted(sub, key=els.index))
    bad = ["{%s, %s} ⊆ A" % (sub[0], other), "%s ∈ A" % other, "A ⊆ {%s}" % ", ".join(sub)]
    return mcq("A = %s. Which statement is true?" % A, good, bad, "Every element of {%s} is in A, so it is a subset of A. <b>%s</b>." % (", ".join(sub), good))


def one_list(r):
    U = list(range(1, r.choice([10, 12, 15]) + 1))
    kinds = {"even numbers": lambda x: x % 2 == 0, "odd numbers": lambda x: x % 2 == 1, "multiples of 3": lambda x: x % 3 == 0, "factors of 12": lambda x: 12 % x == 0,
             "prime numbers": lambda x: x in (2, 3, 5, 7, 11, 13), "numbers greater than 7": lambda x: x > 7}
    a, b = r.sample(list(kinds), 2)
    A = [x for x in U if kinds[a](x)]
    B = [x for x in U if kinds[b](x)]
    op = r.choice(["∪", "∩"])
    res = sorted(set(A) | set(B)) if op == "∪" else sorted(set(A) & set(B))
    if not res or set(A) == set(B):
        raise AssertionError
    show = lambda v: "{%s}" % ", ".join(map(str, v)) if v else "∅"
    other = sorted(set(A) & set(B)) if op == "∪" else sorted(set(A) | set(B))
    w = [show(other), show(sorted(set(A) - set(B))) if set(A) - set(B) else show(A), show(sorted(set(B) - set(A))) if set(B) - set(A) else show(B)]
    q = "U = {1, 2, …, %d}. A is the set of %s and B is the set of %s in U. What is A %s B?" % (U[-1], a, b, op)
    return mcq(q, show(res), w + [show(A)], "A = %s and B = %s. A %s B is the set of elements in %s: <b>%s</b>." % (show(A), show(B), op, "A or B (or both)" if op == "∪" else "both A and B", show(res)))


def build():
    sets, R = build_sets([
        ("Set notation", [("collect", sgv.one_notation, 20)]),
        ("Subsets", [("collect", uniq(one_sub), 20)]),
        ("Union and intersection", [("collect", uniq(one_list), 10), ("collect", sgv.one_ops, 10)]),
        ("Read a Venn diagram", [("collect", sgv.one_read, 20)]),
        ("Shade a Venn diagram", [("collect", sgv.one_shade, 20)]),
    ], 70713)
    finish(sets, R)
    body = lesson('<ul><li>A <b>set</b> is a well-defined collection of objects called elements. x ∈ A means x is an element of A.</li><li>A is a <b>subset</b> of B (A ⊆ B) when every element of A is in B. A set with n elements has 2<sup>n</sup> subsets, including ∅ and itself.</li><li>The <b>union</b> A ∪ B has the elements in A or B (or both). The <b>intersection</b> A ∩ B has the elements in both.</li><li>In a Venn diagram, the overlap of the circles shows A ∩ B.</li></ul>',
        [example("A = {1, 2, 3, 4}, B = {3, 4, 5}", ["A ∪ B = {1, 2, 3, 4, 5}", "A ∩ B = {3, 4}"], "union and intersection")],
        [['Union or intersection?', '∪: in either set. ∩: in both.'], ['Forgetting ∅', 'The empty set is a subset of every set.'], ['Counting the overlap twice', 'Each element is listed once in A ∪ B.']])
    faq = [('What does MATATAG Math 7 ask about sets?', 'Describe and illustrate sets and their subsets, the union of sets, and the intersection of sets, through the use of Venn diagrams.'), ('What is the universal set?', 'The set of all the elements being considered, U.'), ('Is a set a subset of itself?', 'Yes, but not a proper subset.'), ('What is ∅?', 'The empty set, with no elements.')]
    make('sets-subsets-union-and-intersection', 13, 'Number and Algebra', 'Grade 7: Number and Algebra',
         'Describe sets and their subsets, the union of sets, and the intersection of sets; illustrate sets and their subsets, the union of sets, and the intersection of sets, through the use of Venn diagrams.',
         'Sets, Subsets, Union and Intersection with Venn Diagrams', 'Sets and Venn Diagrams',
         'Free Grade 7 sets worksheets for the DepEd MATATAG curriculum: set notation, subsets, union, intersection and Venn diagrams. 100 questions with answers.',
         '∪: in A or B. ∩: in both A and B.', 'A set with n elements has 2ⁿ subsets.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
