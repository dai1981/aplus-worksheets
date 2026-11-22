# -*- coding: utf-8 -*-
"""
India Class 11 Maths, NCERT Chapter 6: Permutations and Combinations (CBSE Unit II Algebra)
  python3 tools/gen_in_maths_c11_permutations_and_combinations.py
The fundamental principle of counting, factorial notation, ⁿPᵣ and ⁿCᵣ, arrangements of letters with repeated
letters and with conditions, numbers made from digits, and selections such as committees and teams (own makers and
US Precalculus makers).
Wrong answers come from real mistakes: adding instead of multiplying choices, n! ÷ r! for ⁿPᵣ, using ⁿPᵣ when
order does not matter, and not dividing by the factorials of repeated letters.
"""
import random, math
from in_sr import U, T2, use, C, P, NCR
from in_common import comma
import gen_us_math_pc_permutations_and_combinations as up

R = random.Random(911106)
fcp = use(up, "one_fcp", R, [NCR])
perm = use(up, "one_perm", R, [NCR])
which = use(up, "one_which", R, [NCR])
f = math.factorial


def npr(n, r_):
    return f(n) // f(n - r_)


def ncr(n, r_):
    return math.comb(n, r_)


def one_fact(r):
    k = r.choice(["div", "sum", "solve"])
    if k == "div":
        n = r.randint(6, 12)
        m = n - r.randint(1, 3)
        return T2("Evaluate %d! ÷ %d!." % (n, m), comma(f(n) // f(m)), [comma(math.factorial(n - m)), str(n - m), comma(f(n) // f(m) // (n - m) if n - m > 1 else f(n) // f(m) + n)],
                  "%d! ÷ %d! = %s = <b>%s</b>." % (n, m, " × ".join(str(x) for x in range(n, m, -1)), comma(f(n) // f(m))))
    if k == "sum":
        a, b = r.randint(2, 5), r.randint(2, 5)
        return T2("Is %d! + %d! equal to %d!? Find %d! + %d!." % (a, b, a + b, a, b), comma(f(a) + f(b)), [comma(f(a + b)), comma(f(a) * f(b)), comma(f(a) + f(b) + 1)],
                  "%d! + %d! = %d + %d = <b>%s</b>, which is not %d! = %s." % (a, b, f(a), f(b), comma(f(a) + f(b)), a + b, comma(f(a + b))))
    n = r.randint(5, 9)
    rr = r.randint(2, 3)
    return T2("Find n if %s = %s." % (P("n", rr), comma(npr(n, rr))), str(n), [str(n + 1), str(n - 1), str(npr(n, rr) // rr)],
              "%s = n(n − 1)%s = %s. Trying n = %d: %s = %s. So <b>n = %d</b>." % (P("n", rr), "(n − 2)" if rr == 3 else "", comma(npr(n, rr)), n,
                                                                                 " × ".join(str(x) for x in range(n, n - rr, -1)), comma(npr(n, rr)), n))


def one_npr(r):
    n = r.randint(5, 10)
    k = r.randint(2, min(4, n - 1))
    t = r.choice(["val", "flag", "digits", "posts"])
    if t == "val":
        return T2("Evaluate %s." % P(n, k), comma(npr(n, k)), [comma(ncr(n, k)), comma(f(n) // f(k)), comma(n * k)],
                  "%s = %d! ÷ %d! = <b>%s</b>." % (P(n, k), n, n - k, comma(npr(n, k))))
    if t == "flag":
        return T2("A ship has %d different flags. A signal uses %d flags, one above the other. How many signals are possible?" % (n, k), comma(npr(n, k)),
                  [comma(ncr(n, k)), comma(n ** k), comma(n * k)], "Order matters and no flag is used twice: %s = <b>%s</b>." % (P(n, k), comma(npr(n, k))))
    if t == "digits":
        d = r.randint(5, 9)
        return T2("How many %d-digit numbers can be made from the digits 1 to %d if no digit is repeated?" % (k, d), comma(npr(d, k)),
                  [comma(d ** k), comma(ncr(d, k)), comma(d * k)], "Each place uses a new digit: %s = <b>%s</b>." % (P(d, k), comma(npr(d, k))))
    roles = ["a captain and a vice-captain", "a president, a secretary and a treasurer", "first, second and third prizes", "a monitor and an assistant monitor"]
    role = r.choice(roles)
    m = 2 if "vice" in role or "assistant" in role else 3
    return T2("In how many ways can %s be chosen from %d students?" % (role, n), comma(npr(n, m)), [comma(ncr(n, m)), comma(n ** m), comma(n * m)],
              "The posts are different, so order matters: %s = <b>%s</b>." % (P(n, m), comma(npr(n, m))))


WORDS = ["INDIA", "KERALA", "ASSAM", "MUMBAI", "BANANA", "MANGO", "DELHI", "PATNA", "AGRA", "SHIMLA", "GANGA", "MADRAS", "NAGPUR", "JAIPUR", "MATHS", "INDEPENDENCE", "PERMUTATION", "ALLAHABAD", "MISSISSIPPI", "DAUGHTER", "EQUATION", "MONDAY"]


def arr(w):
    from collections import Counter
    c = Counter(w)
    out = f(len(w))
    for v in c.values():
        out //= f(v)
    return out, c


def one_word(r):
    w = r.choice(WORDS)
    n, c = arr(w)
    reps = [(k, v) for k, v in c.items() if v > 1]
    if r.random() < 0.7 or not reps:
        why = "%d! ÷ (%s)" % (len(w), " × ".join("%d!" % v for _, v in reps)) if reps else "%d!" % len(w)
        return T2("How many arrangements of the letters of the word %s are there?" % w, comma(n),
                  [comma(f(len(w))) if reps else comma(f(len(w) - 1)), comma(n * 2), comma(n // 2) if n % 2 == 0 else comma(n + len(w))],
                  "There are %d letters%s: %s = <b>%s</b>." % (len(w), (" with " + ", ".join("%s %d times" % (k, v) for k, v in reps)) if reps else ", all different", why, comma(n)))
    vow = [ch for ch in w if ch in "AEIOU"]
    if len(set(vow)) == len(vow) or len(w) > 8:
        return None
    cons = [ch for ch in w if ch not in "AEIOU"]
    blk, cb = arr(cons + ["*"])
    inside, _ = arr(vow)
    tot = blk * inside
    return T2("In how many arrangements of the letters of %s do all the vowels come together?" % w, comma(tot), [comma(blk), comma(n), comma(tot * 2)],
              "Treat the vowels %s as one block: %s arrangements of the block and the consonants, times %s ways inside the block = <b>%s</b>." % (
                  "".join(vow), comma(blk), comma(inside), comma(tot)))


def one_ncr(r):
    t = r.choice(["val", "team", "eq", "mix", "lines"])
    if t == "val":
        n = r.randint(5, 15)
        k = r.randint(2, n - 2)
        return T2("Evaluate %s." % C(n, k), comma(ncr(n, k)), [comma(npr(n, k)), comma(ncr(n, k) + n), comma(n * k)],
                  "%s = %d! ÷ (%d! %d!) = <b>%s</b>." % (C(n, k), n, k, n - k, comma(ncr(n, k))))
    if t == "eq":
        a, b = r.randint(2, 9), r.randint(2, 9)
        if a == b:
            return None
        n = a + b
        return T2("If %s = %s, find %s." % (C("n", a), C("n", b), C("n", 2)), comma(ncr(n, 2)), [str(n), comma(ncr(n, 3)), comma(npr(n, 2))],
                  "<sup>n</sup>C<sub>a</sub> = <sup>n</sup>C<sub>b</sub> with a ≠ b means n = a + b = %d. So %s = <b>%s</b>." % (n, C(n, 2), comma(ncr(n, 2))))
    if t == "team":
        n = r.randint(6, 15)
        k = r.randint(2, 5)
        what = r.choice(["a team of %d players from %d", "a committee of %d from %d people", "%d books from a shelf of %d", "%d questions to answer out of %d"])
        return T2("In how many ways can you choose %s?" % (what % (k, n)), comma(ncr(n, k)), [comma(npr(n, k)), comma(n ** k) if n ** k < 10 ** 7 else comma(n * k), comma(ncr(n, k - 1))],
                  "Order does not matter, so it is %s = <b>%s</b>." % (C(n, k), comma(ncr(n, k))))
    if t == "lines":
        n = r.randint(5, 14)
        if r.random() < 0.5:
            return T2("How many straight lines can be drawn through %d points, no three of which are collinear?" % n, comma(ncr(n, 2)), [comma(npr(n, 2)), str(n), comma(ncr(n, 3))],
                      "Each line is fixed by a pair of points: %s = <b>%s</b>." % (C(n, 2), comma(ncr(n, 2))))
        return T2("How many diagonals does a polygon with %d sides have?" % n, comma(ncr(n, 2) - n), [comma(ncr(n, 2)), comma(n * (n - 3)), str(n - 3)],
                  "Lines joining vertices: %s = %s; take away the %d sides: <b>%s</b>." % (C(n, 2), comma(ncr(n, 2)), n, comma(ncr(n, 2) - n)))
    b, g = r.randint(4, 8), r.randint(3, 7)
    kb, kg = r.randint(2, 3), r.randint(1, 3)
    tot = ncr(b, kb) * ncr(g, kg)
    return T2("From %d boys and %d girls, a group of %d boys and %d girl%s is chosen. In how many ways?" % (b, g, kb, kg, "" if kg == 1 else "s"), comma(tot),
              [comma(ncr(b, kb) + ncr(g, kg)), comma(ncr(b + g, kb + kg)), comma(npr(b, kb) * npr(g, kg))],
              "%s × %s = %s × %s = <b>%s</b>." % (C(b, kb), C(g, kg), comma(ncr(b, kb)), comma(ncr(g, kg)), comma(tot)))


U(11, 6, "permutations-and-combinations", 6, "II", "Permutations and Combinations: ⁿPᵣ, ⁿCᵣ and Counting", "permutations and combinations",
  "Fundamental principle of counting; factorial n (n!); permutations and combinations, derivation of formulae for ⁿPᵣ and ⁿCᵣ and their connections; simple applications (summary of the CBSE syllabus)",
  "Class 11 Permutations and Combinations worksheet (NCERT Chapter 6): counting principle, factorials, ⁿPᵣ, ⁿCᵣ, arrangements of letters, digits, committees and teams. 100 questions with answers.",
  "Order matters → permutation; order does not matter → combination.", "ⁿPᵣ = n!/(n − r)!, ⁿCᵣ = n!/(r!(n − r)!).",
  "<ul><li><b>Counting principle</b>: if one thing can be done in m ways and the next in n ways, both can be done in mn ways.</li>"
  "<li>n! = n(n − 1)(n − 2)…1, and 0! = 1.</li><li>Arrangements (order matters): <sup>n</sup>P<sub>r</sub> = n! ÷ (n − r)!.</li>"
  "<li>Selections (order does not matter): <sup>n</sup>C<sub>r</sub> = n! ÷ (r!(n − r)!), and <sup>n</sup>C<sub>r</sub> = <sup>n</sup>C<sub>n−r</sub>.</li>"
  "<li>Repeated letters: n! ÷ (p! q! …) where a letter appears p times, another q times, and so on.</li></ul>",
  [("How many arrangements of the letters of ALLAHABAD are there?", ["9 letters: A 4 times, L twice", "9! ÷ (4! 2!)"], "7,560")],
  ["Adding the choices instead of multiplying them.", "Using ⁿPᵣ for a committee, where order does not matter.", "Forgetting to divide by the factorials of repeated letters."],
  [("What is 0!?", "0! = 1. It makes the formulas work when r = n."), ("When is ⁿCᵣ = ⁿCₛ?", "When r = s or r + s = n.")],
  [("Counting principle and factorials", [(fcp, 8), (one_fact, 12)]),
   ("Permutations", [(one_npr, 16), (perm, 4)]),
   ("Arrangements of letters", [(one_word, 14), (which, 6)]),
   ("Combinations", [(one_ncr, 20)]),
   ("Mixed problems", [(one_ncr, 10), (one_npr, 10)])], 911106)
