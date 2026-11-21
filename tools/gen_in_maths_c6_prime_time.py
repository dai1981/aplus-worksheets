# -*- coding: utf-8 -*-
"""
India Class 6 Maths, Ganita Prakash Chapter 5: Prime Time
  python3 tools/gen_in_maths_c6_prime_time.py
Factors and multiples, common factors and common multiples, primes and composite numbers, co-prime numbers, prime
factorisation, and divisibility tests for 2, 3, 4, 5, 8, 9 and 10, with problems (idli-vada game, equal groups).
Wrong answers come from real mistakes: 1 taken as prime, 9 or 15 taken as prime, a multiple confused with a factor, and
the test for 4 applied to the last digit only.
"""
import random
from math import gcd
from in_common import num, unit, T, QN, adopt, gb
import gen_uk_maths_y7_factors_multiples_and_primes as fm

R = random.Random(906005)
adopt(fm, R)


def one_common(r):
    kind = r.choice(["cf", "cm", "coprime", "coprime", "nfac"])
    if kind == "cf":
        a, b = r.choice([(12, 18), (16, 24), (20, 30), (18, 27), (24, 36), (15, 25), (28, 42), (30, 45), (36, 48)])
        cf = [d for d in range(1, a + 1) if a % d == 0 and b % d == 0]
        return QN("How many common factors do %d and %d have?" % (a, b), len(cf), [len(cf) - 1, len([d for d in range(1, a + 1) if a % d == 0]), len(cf) + 2],
                  "Common factors: %s. That is <b>%d</b>." % (", ".join(map(str, cf)), len(cf)))
    if kind == "cm":
        a, b = r.choice([(4, 6), (6, 8), (3, 5), (4, 10), (6, 9), (8, 12), (5, 6), (3, 7)])
        l = a * b // gcd(a, b)
        n = r.choice([50, 60, 100])
        c = n // l
        return QN("How many common multiples of %d and %d are there from 1 to %d?" % (a, b, n), c, [n // (a * b), n // a + n // b, c + 1],
                  "Common multiples are multiples of %d: %s. That is <b>%d</b>." % (l, ", ".join(str(l * k) for k in range(1, c + 1)), c))
    if kind == "coprime":
        pairs = [(a, b) for a in range(4, 30) for b in range(a + 1, 36)]
        a, b = r.choice([p for p in pairs if gcd(*p) == 1 and not (p[0] in (2, 3, 5, 7, 11, 13) and p[1] in (2, 3, 5, 7, 11, 13))])
        w = r.sample([p for p in pairs if gcd(*p) > 1], 3)
        return T("Which pair of numbers is co-prime (their only common factor is 1)?", "%d and %d" % (a, b), ["%d and %d" % p for p in w],
                 "%d and %d have no common factor except 1, so they are <b>co-prime</b>." % (a, b))
    n = r.choice([12, 18, 20, 24, 28, 30, 36, 40, 45, 48, 60, 72, 100])
    f = [d for d in range(1, n + 1) if n % d == 0]
    return QN("How many factors does %d have?" % n, len(f), [len(f) - 2, len(f) // 2, len(f) + 1], "%s: <b>%d factors</b>." % (", ".join(map(str, f)), len(f)))


def one_divt(r):
    d = r.choice([2, 3, 4, 5, 8, 9, 10])
    rule = {2: "the last digit is even", 3: "the digit sum is divisible by 3", 4: "the last two digits make a multiple of 4", 5: "the last digit is 0 or 5",
            8: "the last three digits make a multiple of 8", 9: "the digit sum is divisible by 9", 10: "the last digit is 0"}[d]
    while True:
        n = r.randint(100, 99999)
        if n % d == 0:
            break
    w = []
    while len(w) < 3:
        x = n + r.choice([-1, 1]) * r.randint(1, 30)
        if x % d and x not in w:
            w.append(x)
    lst = ", ".join(num(x) for x in sorted(w + [n]))
    return T("Which of these is divisible by %d: %s?" % (d, lst), num(n), [num(x) for x in w], "<b>%s</b>: %s." % (num(n), rule))


def one_prob(r):
    kind = r.choice(["idli", "groups", "bells", "prime"])
    if kind == "idli":
        a, b = r.choice([(3, 5), (2, 7), (4, 6), (3, 4), (5, 7), (4, 10)])
        l = a * b // gcd(a, b)
        return QN("In the idli-vada game, children count 1, 2, 3, … and say ‘idli’ for multiples of %d and ‘vada’ for multiples of %d. Which is the first number where they say ‘idli-vada’?" % (a, b),
                  l, [a * b if a * b != l else l * 2, a + b, max(a, b)], "The first common multiple of %d and %d is <b>%d</b>." % (a, b, l))
    if kind == "groups":
        a, b = r.choice([(24, 36), (18, 30), (20, 32), (28, 42), (45, 60), (16, 40)])
        g = gcd(a, b)
        return QN("%d boys and %d girls are put into teams. Every team must have the same number of boys and the same number of girls. What is the greatest number of teams?" % (a, b), g,
                  [a * b // g, b - a, g // 2], "The greatest common factor of %d and %d is <b>%d</b>." % (a, b, g))
    if kind == "bells":
        a, b = r.choice([(6, 8), (10, 15), (4, 6), (9, 12), (12, 18), (8, 20)])
        l = a * b // gcd(a, b)
        return QN("Two bells ring together. One rings every %d minutes and the other every %d minutes. After how many minutes do they ring together again?" % (a, b), l,
                  [a * b if a * b != l else l + a, a + b, gcd(a, b)], "Lowest common multiple of %d and %d = <b>%d minutes</b>." % (a, b, l), unit=" minutes")
    lo = r.choice([1, 20, 40, 60, 80])
    ps = [p for p in range(lo, lo + 20) if p > 1 and all(p % k for k in range(2, int(p ** 0.5) + 1))]
    return QN("How many prime numbers are there from %d to %d?" % (lo, lo + 19), len(ps), [len(ps) + 1, len(ps) - 1, 10],
              "The primes are %s: <b>%d</b>." % (", ".join(map(str, ps)), len(ps)))


def main():
    unit(6, 0, 5, "prime-time", 5, "N", "Prime Time: Factors, Multiples and Primes", "prime time",
         "Common multiples and common factors, prime and composite numbers, co-prime numbers, prime factorisation and divisibility tests (summary of NCERT Ganita Prakash Class 6)",
         "Class 6 Prime Time worksheet (Ganita Prakash Chapter 5): factors, multiples, common factors, primes, co-primes, prime factorisation and divisibility tests. 100 questions with answers.",
         "A prime has exactly two factors: 1 and itself", "1 is neither prime nor composite.",
         "<p>A <b>factor</b> divides a number exactly; a <b>multiple</b> is in its times table. A <b>prime</b> has exactly two factors (2, 3, 5, 7, 11, …); a <b>composite</b> number has more.</p>"
         "<p>Two numbers are <b>co-prime</b> if their only common factor is 1, like 8 and 15. Every number can be written as a product of primes: 60 = 2 × 2 × 3 × 5.</p>"
         "<p><b>Divisibility</b>: by 2, 5, 10 look at the last digit; by 4 the last two digits; by 8 the last three; by 3 and 9 the digit sum.</p>",
         [("Find the prime factorisation of 84.", ["84 = 2 × 42 = 2 × 2 × 21"], "2 × 2 × 3 × 7"),
          ("Are 14 and 25 co-prime?", ["Factors of 14: 1, 2, 7, 14", "Factors of 25: 1, 5, 25"], "Yes")],
         ["Calling 1 a prime number.", "Thinking every odd number is prime (9, 15 and 21 are not).", "Mixing up factors and multiples."],
         [("Is 1 a prime number?", "No. A prime has exactly two factors; 1 has only one factor."),
          ("What are co-prime numbers?", "Two numbers whose only common factor is 1, such as 9 and 16."),
          ("How do you test divisibility by 4?", "Check whether the number made by the last two digits is divisible by 4.")],
         [("Factors, multiples and primes", [(gb(fm.one_fmp), 20)]),
          ("Common factors, common multiples and co-primes", [(one_common, 20)]),
          ("Prime factorisation", [(gb(fm.one_pf), 12), (gb(fm.one_hcf), 4), (gb(fm.one_lcm), 4)]),
          ("Divisibility tests", [(one_divt, 20)]),
          ("Problems", [(one_prob, 20)])], R)


if __name__ == "__main__":
    main()
