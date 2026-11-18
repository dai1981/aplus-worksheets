# -*- coding: utf-8 -*-
"""
SG Secondary 4 Maths: Set Language and Venn Diagrams (MOE syllabus N8)
  python3 tools/gen_sg_maths_s4_sets_and_venn_diagrams.py
Set notation (∈, ∉, n(A), ∅, ξ, ⊂, ⊆, A′), union and intersection, reading Venn diagrams, describing shaded
regions, and survey problems.
Wrong answers come from real mistakes: mixing up ∪ and ∩, counting the overlap twice in n(A ∪ B), taking A′
as "only A", and confusing ⊂ (subset) with ∈ (element).
"""
import math
import random
from sg_sec import num, S, make, lesson, collect, T, QN, fig, svg_wrap, text

R = random.Random(840100)
INK, SH, BLUE = "#2b2b2b", "#bcd7f5", "#1f6fd1"
CUP, CAP = "∪", "∩"


def setstr(xs):
    xs = sorted(xs)
    return "{" + ", ".join(num(x) for x in xs) + "}" if xs else "∅"


# ------------------------------------------------------------ Venn diagram drawing
W, H = 300, 190
X1, X2, YC, RR = 115, 185, 100, 62


def lens():
    mx = (X1 + X2) / 2
    h = math.sqrt(RR * RR - ((X2 - X1) / 2) ** 2)
    return "M%.1f %.1f A%d %d 0 0 1 %.1f %.1f A%d %d 0 0 1 %.1f %.1f Z" % (mx, YC - h, RR, RR, mx, YC + h, RR, RR, mx, YC - h)


def circ(x, col):
    return "<circle cx='%d' cy='%d' r='%d' fill='%s'/>" % (x, YC, RR, col)


def shade(region):
    """painter's algorithm for the eight common regions"""
    s = []
    rect = "<rect x='10' y='10' width='%d' height='%d' fill='%s'/>" % (W - 20, H - 20, SH)
    lensp = lambda col: "<path d='%s' fill='%s'/>" % (lens(), col)
    if region == "A∩B":
        s.append(lensp(SH))
    elif region == "A only":
        s += [circ(X1, SH), lensp("#fff")]
    elif region == "B only":
        s += [circ(X2, SH), lensp("#fff")]
    elif region == "A∪B":
        s += [circ(X1, SH), circ(X2, SH)]
    elif region == "(A∪B)′":
        s += [rect, circ(X1, "#fff"), circ(X2, "#fff")]
    elif region == "A′":
        s += [rect, circ(X1, "#fff")]
    elif region == "B′":
        s += [rect, circ(X2, "#fff")]
    elif region == "(A∩B)′":
        s += [rect, lensp("#fff")]
    elif region == "A":
        s.append(circ(X1, SH))
    elif region == "B":
        s.append(circ(X2, SH))
    return "".join(s)


def venn(nums=None, region=None, names=("A", "B"), label="Venn diagram"):
    s = []
    if region:
        s.append(shade(region))
    s.append("<rect x='10' y='10' width='%d' height='%d' fill='none' stroke='%s' stroke-width='2'/>" % (W - 20, H - 20, INK))
    s.append("<circle cx='%d' cy='%d' r='%d' fill='none' stroke='%s' stroke-width='2.4'/>" % (X1, YC, RR, INK))
    s.append("<circle cx='%d' cy='%d' r='%d' fill='none' stroke='%s' stroke-width='2.4'/>" % (X2, YC, RR, INK))
    s.append(text(24, 30, "ξ", 16))
    s.append(text(X1 - 52, YC - 50, names[0], 16))
    s.append(text(X2 + 52, YC - 50, names[1], 16))
    if nums:
        a, ab, b, out = nums
        s.append(text(X1 - 28, YC + 6, a, 16, col=BLUE))
        s.append(text((X1 + X2) / 2, YC + 6, ab, 16, col=BLUE))
        s.append(text(X2 + 28, YC + 6, b, 16, col=BLUE))
        s.append(text(W - 34, H - 24, out, 16, col=BLUE))
    return fig(svg_wrap(W, H, "".join(s), label))


# ------------------------------------------------------------ set 1: notation
def one_notation(r):
    U = list(range(1, r.choice([10, 12, 15]) + 1))
    kind = r.choice(["n", "elem", "subset", "comp", "empty"])
    names = {"even": [x for x in U if x % 2 == 0], "odd": [x for x in U if x % 2], "prime": [x for x in U if x > 1 and all(x % d for d in range(2, x))],
             "multiples of 3": [x for x in U if x % 3 == 0], "square numbers": [x for x in U if int(x ** 0.5) ** 2 == x], "factors of 12": [x for x in U if 12 % x == 0]}
    key = r.choice(list(names))
    A = names[key]
    us = "ξ = {<i>x</i> : <i>x</i> is an integer and 1 ≤ <i>x</i> ≤ %d}" % U[-1]
    desc = "A = {<i>x</i> : <i>x</i> is %s}" % ({"even": "an even number", "odd": "an odd number", "prime": "a prime number", "multiples of 3": "a multiple of 3", "square numbers": "a perfect square", "factors of 12": "a factor of 12"}[key])
    if kind == "n":
        return QN("%s and %s. Find n(A)." % (us, desc), len(A), [len(U) - len(A), len(A) + 1, max(A)], "A = %s, so <b>n(A) = %d</b> (the number of elements)." % (setstr(A), len(A)))
    if kind == "comp":
        Ac = [x for x in U if x not in A]
        return T("%s and %s. List A′." % (us, desc), setstr(Ac), [setstr(A), setstr(Ac[:-1]), setstr(U)], "A′ is everything in ξ that is <b>not</b> in A: <b>%s</b>." % setstr(Ac))
    if kind == "elem":
        x = r.choice(U)
        right = "%d ∈ A" % x if x in A else "%d ∉ A" % x
        wr = ["%d ∉ A" % x if x in A else "%d ∈ A" % x, "{%d} ∈ A" % x, "%d ⊂ A" % x]
        return T("%s and %s. Which statement is true?" % (us, desc), right, wr, "A = %s. %d is %s A, so <b>%s</b>. (∈ is for elements; ⊂ is for sets.)" % (setstr(A), x, "in" if x in A else "not in", right))
    if kind == "subset":
        B = r.sample(A, max(1, len(A) // 2)) if len(A) > 1 else A
        right = "%s ⊆ A" % setstr(B)
        bad = [x for x in U if x not in A]
        if not bad:
            return None
        Cn = sorted(B[:1] + [r.choice(bad)])
        return T("%s and %s. Which statement is true?" % (us, desc), right, ["%s ⊆ A" % setstr(Cn), "%s ∈ A" % setstr(B), "A ⊆ %s" % setstr(B) if len(B) < len(A) else "A = ∅"],
                 "Every element of %s is in A = %s, so it is a subset: <b>%s</b>." % (setstr(B), setstr(A), right))
    return T("Which of these is the empty set?", "{<i>x</i> : <i>x</i> is an even prime number greater than 2}", ["{0}", "{∅}", "{<i>x</i> : <i>x</i> is an odd number less than 2}"],
             "There is no even prime greater than 2, so that set has no elements: <b>∅</b>. {0} and {∅} each have one element.")


# ------------------------------------------------------------ set 2: union and intersection
def one_ops(r):
    U = list(range(1, r.choice([10, 12, 15, 20]) + 1))
    A = sorted(r.sample(U, r.randint(3, 6)))
    B = sorted(r.sample(U, r.randint(3, 6)))
    if not set(A) & set(B) or set(A) == set(B):
        return None
    un = sorted(set(A) | set(B))
    it = sorted(set(A) & set(B))
    kind = r.choice(["cup", "cap", "ncup", "capc", "ncupc"])
    pre = "ξ = %s, A = %s and B = %s." % (setstr(U) if len(U) <= 12 else "{1, 2, 3, …, %d}" % U[-1], setstr(A), setstr(B))
    if kind == "cup":
        return T(pre + " Find A ∪ B.", setstr(un), [setstr(it), setstr(sorted(set(A) ^ set(B))), setstr(sorted(set(U) - set(un)))], "A ∪ B contains everything in A <b>or</b> B (or both): <b>%s</b>." % setstr(un))
    if kind == "cap":
        return T(pre + " Find A ∩ B.", setstr(it), [setstr(un), setstr(sorted(set(A) - set(B))), setstr(sorted(set(B) - set(A)))], "A ∩ B contains the elements in <b>both</b> A and B: <b>%s</b>." % setstr(it))
    if kind == "ncup":
        return QN(pre + " Find n(A ∪ B).", len(un), [len(A) + len(B), len(it), len(U) - len(un)], "A ∪ B = %s, so n(A ∪ B) = <b>%d</b>. (Not %d + %d: the overlap is counted once.)" % (setstr(un), len(un), len(A), len(B)))
    if kind == "capc":
        res = sorted(set(A) - set(B))
        return T(pre + " Find A ∩ B′.", setstr(res), [setstr(it), setstr(sorted(set(B) - set(A))), setstr(sorted(set(U) - set(B)))], "B′ is everything not in B. A ∩ B′ is in A but not in B: <b>%s</b>." % setstr(res))
    return QN(pre + " Find n((A ∪ B)′).", len(U) - len(un), [len(un), len(U) - len(it), len(U) - len(A) - len(B)], "n(A ∪ B) = %d, so n((A ∪ B)′) = %d − %d = <b>%d</b>." % (len(un), len(U), len(un), len(U) - len(un)))


# ------------------------------------------------------------ set 3: reading Venn diagrams
def one_read(r):
    a, ab, b, out = r.randint(2, 15), r.randint(1, 10), r.randint(2, 15), r.randint(1, 12)
    pic = venn((num(a), num(ab), num(b), num(out)), label="Venn diagram with numbers in each region")
    asks = [("n(A)", a + ab, [a, a + ab + b, ab]), ("n(A ∩ B)", ab, [a + ab + b, a + b, ab + out]), ("n(A ∪ B)", a + ab + b, [a + 2 * ab + b, ab, a + b]),
            ("n(A′)", b + out, [a, a + ab, out]), ("n((A ∪ B)′)", out, [a + b + ab, b + out, 0]), ("n(ξ)", a + ab + b + out, [a + b + out, a + ab + b, a + 2 * ab + b + out]),
            ("n(A ∩ B′)", a, [a + ab, b, ab]), ("n(A′ ∩ B)", b, [b + ab, a, out])]
    what, v, wr = r.choice(asks)
    expl = {"n(A)": "everything inside circle A: %d + %d" % (a, ab), "n(A ∩ B)": "the overlap only", "n(A ∪ B)": "everything inside either circle: %d + %d + %d" % (a, ab, b),
            "n(A′)": "everything outside A: %d + %d" % (b, out), "n((A ∪ B)′)": "outside both circles", "n(ξ)": "every region: %d + %d + %d + %d" % (a, ab, b, out),
            "n(A ∩ B′)": "in A but not in B", "n(A′ ∩ B)": "in B but not in A"}[what]
    return QN("The Venn diagram shows the number of elements in each region. Find %s.%s" % (what, pic), v, wr, "%s is %s = <b>%d</b>." % (what, expl, v))


# ------------------------------------------------------------ set 4: shaded regions
REGIONS = [("A∩B", "A ∩ B"), ("A only", "A ∩ B′"), ("B only", "A′ ∩ B"), ("A∪B", "A ∪ B"), ("(A∪B)′", "(A ∪ B)′"), ("A′", "A′"), ("B′", "B′"), ("(A∩B)′", "(A ∩ B)′")]


def one_shade(r):
    reg, name = r.choice(REGIONS)
    others = [n for k, n in REGIONS if n != name]
    pair = {"A ∩ B": ["A ∪ B", "(A ∩ B)′"], "A ∩ B′": ["A′ ∩ B", "A′"], "A′ ∩ B": ["A ∩ B′", "B′"], "A ∪ B": ["A ∩ B", "(A ∪ B)′"],
            "(A ∪ B)′": ["A ∪ B", "(A ∩ B)′"], "A′": ["A ∩ B′", "B′"], "B′": ["A′ ∩ B", "A′"], "(A ∩ B)′": ["A ∩ B", "(A ∪ B)′"]}[name]
    wr = pair + [r.choice([o for o in others if o not in pair])]
    if r.random() < 0.5:
        pic = venn(region=reg, label="Venn diagram with a shaded region")
        return T("Which set is shaded in the Venn diagram?%s" % pic, name, wr, "The shaded part is %s: <b>%s</b>." % ({"A ∩ B": "the overlap of A and B", "A ∩ B′": "in A but not in B", "A′ ∩ B": "in B but not in A",
                                                                                                                       "A ∪ B": "everything in A or B", "(A ∪ B)′": "outside both circles", "A′": "everything outside A",
                                                                                                                       "B′": "everything outside B", "(A ∩ B)′": "everything except the overlap"}[name], name))
    k = r.randint(1, 8)
    other = r.choice(REGIONS)
    while other[1] == name:
        other = r.choice(REGIONS)
    q = "In which region would you put an element that is %s?" % {"A ∩ B": "in both A and B", "A ∩ B′": "in A but not in B", "A′ ∩ B": "in B but not in A", "A ∪ B": "in at least one of A and B",
                                                                    "(A ∪ B)′": "in neither A nor B", "A′": "not in A", "B′": "not in B", "(A ∩ B)′": "not in both A and B"}[name]
    return T(q, name, wr, "That description is the set <b>%s</b>." % name)


# ------------------------------------------------------------ set 5: problems
def one_prob(r):
    kind = r.choice(["neither", "both", "only", "x", "x"])
    clubs = r.choice([("the choir", "the band"), ("the football club", "the basketball club"), ("the Chinese chess club", "the robotics club"), ("the art club", "the drama club"), ("the swimming team", "the badminton team")])
    total = r.randint(30, 45)
    both = r.randint(2, 8)
    a = r.randint(both + 3, 20)
    b = r.randint(both + 3, 18)
    if a + b - both > total:
        return None
    neither = total - (a + b - both)
    pre = "In a class of %d students, %d are in %s, %d are in %s and %d are in both." % (total, a, clubs[0], b, clubs[1], both)
    if kind == "neither":
        return QN(pre + " How many are in neither?", neither, [total - a - b, total - both, a + b - both], "n(A ∪ B) = %d + %d − %d = %d (subtract the overlap once). Neither = %d − %d = <b>%d</b>." % (a, b, both, a + b - both, total, a + b - both, neither))
    if kind == "only":
        return QN(pre + " How many are in %s only?" % clubs[0], a - both, [a, a + both, b - both], "Only %s: %d − %d = <b>%d</b>." % (clubs[0], a, both, a - both))
    if kind == "both":
        pre2 = "In a class of %d students, %d are in %s, %d are in %s and %d are in neither." % (total, a, clubs[0], b, clubs[1], neither)
        return QN(pre2 + " How many are in both?", both, [a + b, total - neither, both + neither], "n(A ∪ B) = %d − %d = %d. Both = %d + %d − %d = <b>%d</b>." % (total, neither, total - neither, a, b, total - neither, both))
    # unknown x in the overlap
    pic = venn((num(a) + " − x", "x", num(b) + " − x", num(neither)), names=(clubs[0].split()[1][:1].upper(), clubs[1].split()[1][:1].upper()), label="Venn diagram with x in the overlap")
    q = "%d students were asked whether they are in %s (%s) or %s (%s). %d are in %s, %d are in %s and %d are in neither. Find <i>x</i>, the number in both.%s" % (
        total, clubs[0], clubs[0].split()[1][:1].upper(), clubs[1], clubs[1].split()[1][:1].upper(), a, clubs[0], b, clubs[1], neither, pic)
    return QN(q, both, [a + b, total - neither, both + neither], "(%d − <i>x</i>) + <i>x</i> + (%d − <i>x</i>) + %d = %d, so %d − <i>x</i> = %d and <i>x</i> = <b>%d</b>." % (
        a, b, neither, total, a + b + neither, total, both))


def build():
    sets = [S("Set notation", collect(one_notation, 20, R)),
            S("Union, intersection and complement", collect(one_ops, 20, R)),
            S("Reading Venn diagrams", collect(one_read, 20, R)),
            S("Shaded regions", collect(one_shade, 20, R)),
            S("Problems", collect(one_prob, 20, R))]
    body = lesson(
        "<ul><li><b>ξ</b> is the universal set. <b>∅</b> is the empty set. <b>n(A)</b> is the number of elements in A.</li>"
        "<li><i>x</i> <b>∈</b> A means <i>x</i> is an element of A. B <b>⊆</b> A means every element of B is in A (B <b>⊂</b> A if B is also smaller than A).</li>"
        "<li><b>A ∪ B</b> (union): in A or B or both. <b>A ∩ B</b> (intersection): in both. <b>A′</b> (complement): not in A.</li>"
        "<li><b>n(A ∪ B) = n(A) + n(B) − n(A ∩ B)</b>, so the overlap is not counted twice.</li></ul>",
        [("ξ = {1, 2, …, 10}, A = {2, 4, 6, 8} and B = {1, 2, 3, 4}. Find A ∩ B and n(A ∪ B).", ["A ∩ B = {2, 4}", "A ∪ B = {1, 2, 3, 4, 6, 8}"], "{2, 4} and 6"),
         ("In a class of 30, 18 like tea, 15 like coffee and 7 like both. How many like neither?", ["18 + 15 − 7 = 26 like at least one"], "4")],
        ["Mixing up ∪ (or) and ∩ (and).",
         "Counting the overlap twice: n(A ∪ B) is not n(A) + n(B).",
         "Taking A′ to mean 'only A'. A′ means everything not in A.",
         "Writing 3 ⊂ A instead of 3 ∈ A. Use ⊂ for sets and ∈ for elements."])
    faq = [("What do ∪ and ∩ mean?", "A ∪ B (union) is everything in A or B or both. A ∩ B (intersection) is only what is in both A and B."),
           ("What is the complement of a set?", "A′ is everything in the universal set ξ that is not in A."),
           ("What is the difference between ∈ and ⊂?", "∈ links an element to a set (3 ∈ A). ⊂ links a set to a set ({3} ⊂ A)."),
           ("How do I solve Venn diagram word problems?", "Start with the overlap, then fill in the 'only' regions, then the outside region, and check that all regions add up to the total.")]
    make(4, "sets-and-venn-diagrams", 1, "N8",
         "Set Language, Notation and Venn Diagrams",
         "", "Sets and Venn diagrams", "",
         "Free Secondary 4 maths worksheets on set language and notation, union, intersection, complement, Venn diagrams, shaded regions and survey problems. 100 questions with answers.",
         "∪ means or, ∩ means and, A′ means not in A.",
         "n(A ∪ B) = n(A) + n(B) − n(A ∩ B): count the overlap once.",
         body, faq, sets, R)


if __name__ == "__main__":
    build()
