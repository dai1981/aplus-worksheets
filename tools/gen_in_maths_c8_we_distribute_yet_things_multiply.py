# -*- coding: utf-8 -*-
"""
India Class 8 Maths, Ganita Prakash Part 1, Chapter 6: We Distribute, Yet Things Multiply
  python3 tools/gen_in_maths_c8_we_distribute_yet_things_multiply.py
The distributive property with numbers and letters, multiplying two binomials, the identities (a + b)², (a − b)² and
(a + b)(a − b), and using them for mental multiplication (103 × 97, 98², 51²).
Wrong answers come from real mistakes: (a + b)² = a² + b², multiplying only the first term in the bracket, sign errors
with −, and 103 × 97 worked as 100 × 100 + 3 × 7.
"""
import random
from in_common import num, unit, T, QN, adopt, gb
import gen_uk_maths_y8_expanding_and_factorising as uk
import gen_sg_maths_s2_expansion_and_factorisation as sg

R = random.Random(908006)
adopt(uk, R)
adopt(sg, R)


def one_dist(r):
    kind = r.choice(["num", "num", "split", "factor"])
    if kind == "num":
        a, b, c = r.randint(3, 25), r.randint(11, 60), r.randint(11, 60)
        return QN("Use the distributive property: %d × %d + %d × %d = %d × (? )" % (a, b, a, c, a) if False else "Work out %d × %d + %d × %d by first writing it as %d × (%d + %d)." % (a, b, a, c, a, b, c),
                  a * (b + c), [a * b + c, a + b + c, a * (b + c) + a], "%d × %d = <b>%s</b>." % (a, b + c, num(a * (b + c))))
    if kind == "split":
        a = r.randint(12, 99)
        k = r.choice([99, 101, 999, 1001, 98, 102])
        base = 100 if k < 200 else 1000
        d = k - base
        return QN("Work out %d × %d mentally using %d × (%d %s %d)." % (a, k, a, base, "+" if d > 0 else "−", abs(d)), a * k,
                  [a * base + d, a * base + abs(d) * a if d < 0 else a * base - d * a, a * k + a], "%d × %d %s %d × %d = <b>%s</b>." % (a, base, "+" if d > 0 else "−", a, abs(d), num(a * k)))
    a, b, c = r.randint(2, 9), r.randint(10, 50), r.randint(10, 50)
    return QN("%d × %d − %d × %d = %d × (%d − %d). What is its value?" % (b, a + 10, c, a + 10, a + 10, b, c) if b != c else None, (a + 10) * (b - c),
              [(a + 10) * (b + c), b - c, (a + 10) * b - c], "%d × %d = <b>%s</b>." % (a + 10, b - c, num((a + 10) * (b - c))))


def one_ident(r):
    kind = r.choice(["sq", "sq", "diff", "near"])
    if kind == "sq":
        a = r.choice([10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
        b = r.choice([1, 2, 3, -1, -2, -3])
        n = a + b
        return QN("Use (a %s b)² = a² %s 2ab + b² to find %d²." % ("+" if b > 0 else "−", "+" if b > 0 else "−", n), n * n,
                  [a * a + b * b, n * n - 2 * a * abs(b) if b > 0 else n * n + 2 * a * abs(b), n * 2],
                  "(%d %s %d)² = %s %s %s + %d = <b>%s</b>." % (a, "+" if b > 0 else "−", abs(b), num(a * a), "+" if b > 0 else "−", num(2 * a * abs(b)), b * b, num(n * n)))
    if kind == "diff":
        a = r.choice([20, 30, 40, 50, 60, 100, 200])
        b = r.randint(1, 9)
        return QN("Use (a + b)(a − b) = a² − b² to find %d × %d." % (a + b, a - b), a * a - b * b, [a * a + b * b, a * a, a * a - 2 * b],
                  "%d² − %d² = %s − %d = <b>%s</b>." % (a, b, num(a * a), b * b, num(a * a - b * b)))
    a, b = r.randint(11, 40), r.randint(11, 40)
    if a == b:
        return None
    return QN("Find %d² − %d² without squaring each number." % (max(a, b), min(a, b)), abs(a * a - b * b), [abs(a - b) ** 2, abs(a - b), (a + b) ** 2],
              "(%d + %d)(%d − %d) = %d × %d = <b>%s</b>." % (max(a, b), min(a, b), max(a, b), min(a, b), a + b, abs(a - b), num(abs(a * a - b * b))))


def one_area(r):
    a, b, c, d = r.randint(3, 12), r.randint(2, 9), r.randint(3, 12), r.randint(2, 9)
    return QN("A rectangle is (%d + %d) cm long and (%d + %d) cm wide. Find its area by adding the four smaller rectangles." % (a, b, c, d), (a + b) * (c + d),
              [a * c + b * d, (a + b) + (c + d), a * c + b * d + a * d], "%d×%d + %d×%d + %d×%d + %d×%d = <b>%d cm²</b>." % (a, c, a, d, b, c, b, d, (a + b) * (c + d)), unit=" cm²")


def main():
    unit(8, 1, 6, "we-distribute-yet-things-multiply", 6, "A", "We Distribute, Yet Things Multiply: Distributive Property and Identities", "we distribute, yet things multiply",
         "The distributive property, multiplying expressions, and the identities (a + b)² = a² + 2ab + b², (a − b)² = a² − 2ab + b² and (a + b)(a − b) = a² − b² (summary of NCERT Ganita Prakash Class 8)",
         "Class 8 We Distribute, Yet Things Multiply worksheet (Ganita Prakash Part 1, Chapter 6): distributive property, expanding brackets and algebraic identities. 100 questions with answers.",
         "a(b + c) = ab + ac", "(a + b)² = a² + 2ab + b²; (a + b)(a − b) = a² − b².",
         "<p>The <b>distributive property</b>: a(b + c) = ab + ac. Multiply every term in the bracket.</p>"
         "<p>For two brackets, multiply each term by each term: (a + b)(c + d) = ac + ad + bc + bd.</p>"
         "<p><b>Identities</b>: (a + b)² = a² + 2ab + b², (a − b)² = a² − 2ab + b², (a + b)(a − b) = a² − b². They make mental sums easy: 103 × 97 = 100² − 3² = 9,991.</p>",
         [("Expand 3x(2x − 5).", ["3x × 2x − 3x × 5"], "6x² − 15x"),
          ("Find 98² using an identity.", ["(100 − 2)² = 10,000 − 400 + 4"], "9,604")],
         ["Writing (a + b)² = a² + b² and forgetting 2ab.", "Multiplying only the first term: 3(x + 4) = 3x + 4.", "Losing the sign: −2(x − 5) = −2x + 10, not −2x − 10."],
         [("What is the distributive property?", "a(b + c) = ab + ac: multiplying a sum is the same as multiplying each part and adding."),
          ("What are the standard identities?", "(a + b)² = a² + 2ab + b², (a − b)² = a² − 2ab + b² and (a + b)(a − b) = a² − b²."),
          ("How do identities help with mental maths?", "For example 51² = (50 + 1)² = 2,500 + 100 + 1 = 2,601, and 47 × 53 = 50² − 3² = 2,491.")],
         [("The distributive property with numbers", [(one_dist, 14), (one_area, 6)]),
          ("Multiplying a bracket by a term", [(gb(uk.one_single), 12), (gb(uk.one_simplify), 8)]),
          ("Multiplying two brackets", [(gb(uk.one_double), 10), (gb(sg.one_expand), 10)]),
          ("Identities", [(gb(sg.one_square), 20)]),
          ("Mental maths with identities", [(one_ident, 20)])], R)


if __name__ == "__main__":
    main()
