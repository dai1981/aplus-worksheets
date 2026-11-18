# -*- coding: utf-8 -*-
"""
US Precalculus: Permutations and Combinations (Common Core S-CP.B.9)
  python3 tools/gen_us_math_pc_permutations_and_combinations.py
The fundamental counting principle, factorials and permutations, combinations, deciding whether order
matters (and arranging letters with repeats), and probabilities found by counting.
Wrong answers come from real mistakes: adding choices instead of multiplying, using a permutation when order
does not matter (or the reverse), forgetting to divide by repeated letters, and counting with replacement.
"""
import math
import random
from fractions import Fraction as F
from us_hs import B, S, make, lesson, collect, T, num, MINUS, People
from a2_common import sf
from pc_common import GRADE, C, P

R = random.Random(98401)


def nPr(n, k):
    return "<sub>%d</sub>P<sub>%d</sub>" % (n, k)


def nCr(n, k):
    return "<sub>%d</sub>C<sub>%d</sub>" % (n, k)


# ------------------------------------------------------------ set 1: counting principle
def one_fcp(r):
    pp = People(r)
    nm, he, his = pp.next()
    kind = r.choice(["outfit", "meal", "plate", "code", "code2"])
    if kind == "outfit":
        a, b, c = r.randint(3, 8), r.randint(2, 6), r.randint(2, 5)
        q = "%s has %d shirts, %d pairs of pants and %d pairs of shoes. How many different outfits can %s make?" % (nm, a, b, c, he)
        ans = a * b * c
        return T(q, num(ans), [num(a + b + c), num(a * b + c), num(C(a + b + c, 3))], "Multiply the choices: %d × %d × %d = <b>%s</b>." % (a, b, c, num(ans)))
    if kind == "meal":
        a, b, c = r.randint(3, 6), r.randint(4, 8), r.randint(2, 5)
        q = "A restaurant offers %d appetizers, %d main dishes and %d desserts. How many meals with one of each are possible?" % (a, b, c)
        ans = a * b * c
        return T(q, num(ans), [num(a + b + c), num(a * b), num(P(a + b + c, 3)) if P(a + b + c, 3) < 10000 else num(ans * 2)], "%d × %d × %d = <b>%s</b>." % (a, b, c, num(ans)))
    if kind == "plate":
        L, D = r.choice([(2, 3), (3, 3), (2, 4), (3, 2)])
        q = "A license plate has %d letters followed by %d digits. Letters and digits may repeat. How many plates are possible?" % (L, D)
        ans = 26 ** L * 10 ** D
        return T(q, num(ans), [num(P(26, L) * P(10, D)), num(26 * L + 10 * D), num(26 ** L + 10 ** D)], "26<sup>%d</sup> × 10<sup>%d</sup> = <b>%s</b>." % (L, D, num(ans)))
    n = r.choice([3, 4, 5])
    rep = kind == "code"
    q = "A lock code uses %d digits (0–9)%s. How many codes are possible?" % (n, "" if rep else " with no digit repeated")
    ans = 10 ** n if rep else P(10, n)
    other = P(10, n) if rep else 10 ** n
    return T(q, num(ans), [num(other), num(10 * n), num(C(10, n))], ("10 choices for each digit: 10<sup>%d</sup> = <b>%s</b>." % (n, num(ans))) if rep else
             ("10 × 9 × … (%d factors) = %s = <b>%s</b>." % (n, nPr(10, n), num(ans))))


# ------------------------------------------------------------ set 2: permutations
def one_perm(r):
    kind = r.choice(["fact", "npr", "race", "seat", "seat"])
    if kind == "fact":
        n = r.randint(4, 8)
        k = r.randint(1, 3)
        q = "Evaluate %d! / %d!." % (n, n - k)
        ans = P(n, k)
        return T(q, num(ans), [num(math.factorial(k)), num(F(n, n - k)) if F(n, n - k).denominator == 1 else num(n * k), num(ans * math.factorial(n - k)) if ans * math.factorial(n - k) < 100000 else num(n)],
                 "%d! / %d! = %s = <b>%s</b>." % (n, n - k, " × ".join(str(n - i) for i in range(k)), num(ans)))
    if kind == "npr":
        n, k = r.randint(5, 10), r.randint(2, 4)
        ans = P(n, k)
        return T("Evaluate %s." % nPr(n, k), num(ans), [num(C(n, k)), num(n ** k), num(n * k)], "%s = %d!/(%d − %d)! = <b>%s</b>." % (nPr(n, k), n, n, k, num(ans)))
    if kind == "race":
        n = r.randint(6, 12)
        q = "%d runners are in a race. In how many ways can gold, silver and bronze be awarded?" % n
        ans = P(n, 3)
        return T(q, num(ans), [num(C(n, 3)), num(n ** 3), num(3 * n)], "Order matters: %d × %d × %d = <b>%s</b>." % (n, n - 1, n - 2, num(ans)))
    n = r.randint(4, 8)
    k = r.choice([n, n - 1, n - 2])
    if k == n:
        q = "In how many ways can %d students stand in a line?" % n
        ans = math.factorial(n)
        return T(q, num(ans), [num(n * n), num(n * (n + 1) // 2), num(2 ** n)], "%d! = <b>%s</b>." % (n, num(ans)))
    q = "In how many ways can %d of %d students sit in a row of %d chairs?" % (k, n, k)
    ans = P(n, k)
    return T(q, num(ans), [num(C(n, k)), num(math.factorial(k)), num(n ** k)], "%s = <b>%s</b>." % (nPr(n, k), num(ans)))


# ------------------------------------------------------------ set 3: combinations
def one_comb(r):
    kind = r.choice(["ncr", "committee", "pizza", "team", "two"])
    if kind == "ncr":
        n, k = r.randint(5, 12), r.randint(2, 5)
        if k >= n:
            return None
        ans = C(n, k)
        return T("Evaluate %s." % nCr(n, k), num(ans), [num(P(n, k)), num(n * k), num(C(n, k - 1)) if C(n, k - 1) != ans else num(ans + 1)],
                 "%s = %d!/(%d! · %d!) = <b>%s</b>." % (nCr(n, k), n, k, n - k, num(ans)))
    if kind == "committee":
        n, k = r.randint(8, 15), r.randint(3, 4)
        q = "A club has %d members. How many different %d-person committees can be chosen?" % (n, k)
        ans = C(n, k)
        return T(q, num(ans), [num(P(n, k)), num(n * k), num(C(n, k - 1))], "Order does not matter: %s = <b>%s</b>." % (nCr(n, k), num(ans)))
    if kind == "pizza":
        n, k = r.randint(8, 14), r.randint(2, 3)
        q = "A pizza shop has %d toppings. How many pizzas with exactly %d different toppings are possible?" % (n, k)
        ans = C(n, k)
        return T(q, num(ans), [num(P(n, k)), num(n ** k), num(n * k)], "Order of toppings does not matter: %s = <b>%s</b>." % (nCr(n, k), num(ans)))
    if kind == "team":
        n = r.randint(9, 13)
        q = "A coach chooses 5 starting players from %d players. How many ways can the starters be chosen?" % n
        ans = C(n, 5)
        return T(q, num(ans), [num(P(n, 5)), num(n * 5), num(C(n, 4))], "%s = <b>%s</b>." % (nCr(n, 5), num(ans)))
    g, b = r.randint(5, 9), r.randint(4, 8)
    kg, kb = r.choice([2, 3]), r.choice([2, 3])
    q = "A class has %d girls and %d boys. How many ways can a group of %d girls and %d boys be chosen?" % (g, b, kg, kb)
    ans = C(g, kg) * C(b, kb)
    return T(q, num(ans), [num(C(g, kg) + C(b, kb)), num(C(g + b, kg + kb)), num(P(g, kg) * P(b, kb))],
             "Choose each part and multiply: %s × %s = %d × %d = <b>%s</b>." % (nCr(g, kg), nCr(b, kb), C(g, kg), C(b, kb), num(ans)))


# ------------------------------------------------------------ set 4: order or not, and repeated letters
WORDS = ["LEVEL", "BANANA", "PEPPER", "BOOK", "APPLE", "COOKIE", "TOMATO", "COFFEE", "BALLOON", "LETTER", "SCISSORS", "TENNESSEE"]


def one_which(r):
    if r.random() < 0.5:
        w = r.choice(WORDS)
        counts = [w.count(ch) for ch in sorted(set(w))]
        ans = math.factorial(len(w))
        for c in counts:
            ans //= math.factorial(c)
        q = "How many different arrangements of the letters in %s are there?" % w
        div = " · ".join("%d!" % c for c in counts if c > 1)
        return T(q, num(ans), [num(math.factorial(len(w))), num(ans * 2) if ans * 2 != math.factorial(len(w)) else num(ans * 3), num(math.factorial(len(set(w))))],
                 "%d letters, with repeats: %d! / (%s) = <b>%s</b>." % (len(w), len(w), div, num(ans)))
    items = [("choosing 3 class officers (president, vice president, secretary) from 20 students", "Permutation, because the roles are different", P(20, 3)),
             ("choosing 3 students from 20 to form a study group", "Combination, because the group has no order", C(20, 3)),
             ("choosing a 4-book reading list from 10 books", "Combination, because the group has no order", C(10, 4)),
             ("arranging 4 of 10 books on a shelf", "Permutation, because the order on the shelf matters", P(10, 4)),
             ("choosing 2 co-captains from 12 players", "Combination, because the co-captains have the same role", C(12, 2)),
             ("choosing a captain and a co-captain from 12 players", "Permutation, because the roles are different", P(12, 2)),
             ("dealing a 5-card hand from 52 cards", "Combination, because the order of the cards in a hand does not matter", C(52, 5)),
             ("awarding first, second and third prize among 15 entries", "Permutation, because the prizes are different", P(15, 3))]
    desc, kind, val = r.choice(items)
    q = "Is %s a permutation or a combination, and how many ways are there?" % desc
    other = "Combination" if kind.startswith("Permutation") else "Permutation"
    n_k = {P(20, 3): (20, 3), C(20, 3): (20, 3), C(10, 4): (10, 4), P(10, 4): (10, 4), C(12, 2): (12, 2), P(12, 2): (12, 2), C(52, 5): (52, 5), P(15, 3): (15, 3)}[val]
    oval = C(*n_k) if kind.startswith("Permutation") else P(*n_k)
    right = "%s; %s ways" % (kind.split(",")[0], num(val))
    return T(q, right, ["%s; %s ways" % (other, num(oval)), "%s; %s ways" % (other, num(val)), "%s; %s ways" % (kind.split(",")[0], num(oval))],
             "%s. <b>%s</b>." % (kind, right))


# ------------------------------------------------------------ set 5: probability by counting
def one_prob(r):
    kind = r.choice(["committee", "committee", "allsame", "lottery", "order"])
    pp = People(r)
    n1, _, _ = pp.next()
    n2, _, _ = pp.next()
    if kind == "committee":
        n, k = r.randint(8, 12), r.choice([3, 4])
        q = "A committee of %d is chosen at random from %d people, including %s and %s. What is the probability that both %s and %s are chosen?" % (k, n, n1, n2, n1, n2)
        ans = F(C(n - 2, k - 2), C(n, k))
        return T(q, sf(ans), [sf(F(1, C(n, k))), sf(F(k, n) * F(k, n)), sf(F(2, n))],
                 "Ways that include both: %s = %d. All committees: %s = %d. %d/%d = <b>%s</b>." % (nCr(n - 2, k - 2), C(n - 2, k - 2), nCr(n, k), C(n, k), C(n - 2, k - 2), C(n, k), sf(ans)))
    if kind == "allsame":
        g, b = r.randint(4, 7), r.randint(4, 7)
        k = 3
        q = "A group of %d students is chosen at random from %d girls and %d boys. What is the probability that all are girls?" % (k, g, b)
        ans = F(C(g, k), C(g + b, k))
        return T(q, sf(ans), [sf(F(g, g + b) ** 3), sf(F(1, C(g + b, k))), sf(F(g, g + b))],
                 "%s ÷ %s = %d/%d = <b>%s</b>. (Without replacement, the fractions are not all %d/%d.)" % (nCr(g, k), nCr(g + b, k), C(g, k), C(g + b, k), sf(ans), g, g + b))
    if kind == "lottery":
        n, k = r.choice([(20, 3), (30, 4), (25, 3), (40, 5), (15, 4)])
        q = "In a lottery, you choose %d different numbers from 1 to %d, in any order. What is the probability that your numbers match the winning numbers?" % (k, n)
        return T(q, "1/%s" % num(C(n, k)), ["1/%s" % num(P(n, k)), "%d/%d" % (k, n), "1/%s" % num(n ** k)],
                 "Order does not matter, so there are %s = %s equally likely sets. <b>1/%s</b>." % (nCr(n, k), num(C(n, k)), num(C(n, k))))
    n = r.randint(4, 7)
    q = "%d books, including a dictionary and an atlas, are placed on a shelf in random order. What is the probability that the dictionary is first and the atlas is second?" % n
    ans = F(math.factorial(n - 2), math.factorial(n))
    return T(q, sf(ans), [sf(F(2, n)), sf(F(1, n)), sf(F(1, math.factorial(n)))],
             "Arrangements with those two fixed: %d! = %d. All arrangements: %d! = %d. <b>%s</b>." % (n - 2, math.factorial(n - 2), n, math.factorial(n), sf(ans)))


def build():
    sets = [S("The counting principle", collect(one_fcp, 20, R)),
            S("Permutations", collect(one_perm, 20, R)),
            S("Combinations", collect(one_comb, 20, R)),
            S("Order or no order", collect(one_which, 20, R)),
            S("Probability by counting", collect(one_prob, 20, R))]
    body = lesson(
        "<ul><li><b>Counting principle</b>: if one choice has <i>m</i> options and another has <i>n</i>, together there are <i>m</i> × <i>n</i>.</li>"
        "<li><b>Permutation</b> (order matters): <sub><i>n</i></sub>P<sub><i>r</i></sub> = <i>n</i>! / (<i>n</i> − <i>r</i>)!. Use it for rankings, roles, arrangements.</li>"
        "<li><b>Combination</b> (order does not matter): <sub><i>n</i></sub>C<sub><i>r</i></sub> = <i>n</i>! / (<i>r</i>!(<i>n</i> − <i>r</i>)!). Use it for groups, committees, hands.</li>"
        "<li>Arranging letters with repeats: divide <i>n</i>! by the factorial of each repeat count.</li>"
        "<li>Probability = (number of favorable outcomes) / (total outcomes), counted the same way.</li></ul>",
        [("How many ways can a president and a treasurer be chosen from 10 people?", ["Order matters (different roles)", "10 × 9"], "90"),
         ("How many 3-person teams can be chosen from 10 people?", ["Order does not matter", "<sub>10</sub>C<sub>3</sub> = 720 ÷ 6"], "120")],
        ["Adding the choices instead of multiplying.",
         "Using a permutation for a group with no order. That counts each group several times.",
         "Forgetting to divide by repeated letters.",
         "Allowing repeats when the problem says no repeats."])
    faq = [("What is the difference between a permutation and a combination?", "In a permutation the order matters (like first, second and third place). In a combination it does not (like choosing a committee)."),
           ("What is the formula for nCr?", "nCr = n! / (r!(n − r)!). It equals nPr divided by r!, because each group of r can be ordered in r! ways."),
           ("How do you count arrangements of a word with repeated letters?", "Divide the factorial of the number of letters by the factorial of each letter's count. BANANA has 6!/(3! · 2!) = 60 arrangements."),
           ("How do you use counting in probability?", "Count the favorable outcomes and the total outcomes the same way, then divide.")]
    make("permutations-and-combinations", 14, "S-CP.B.9",
         "Permutations and Combinations",
         "Permutations and Combinations Worksheet with Probability | 100 Questions with Answers",
         "Permutations and Combinations",
         "Use permutations and combinations to compute probabilities of compound events and solve problems.",
         "Free precalculus worksheet on permutations and combinations: the counting principle, nPr, nCr, arrangements with repeated letters and probability by counting. 100 questions.",
         "Order matters: permutation. Order does not matter: combination.",
         "nPr = n!/(n − r)!, nCr = n!/(r!(n − r)!).",
         body, faq, sets, R, domain="Probability", grade=GRADE)


if __name__ == "__main__":
    build()
