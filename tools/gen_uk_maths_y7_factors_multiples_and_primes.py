# -*- coding: utf-8 -*-
"""
UK Year 7 Maths: Factors, Multiples and Primes (KS3 Number)
  python3 tools/gen_uk_maths_y7_factors_multiples_and_primes.py
Factors, multiples and prime numbers, prime factorisation in index form, HCF and LCM, and problems.
Wrong answers come from real mistakes: mixing up factors and multiples, counting 1 or 9 as prime,
leaving a non-prime in a factor tree, and giving the product instead of the LCM.
"""
import random
from math import gcd
from uk_ks3 import num, mcq, B, S, make, lesson, collect, QN, T, People

R = random.Random(70401)
P = People(R)
PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]


def lcm(a, b):
    return a * b // gcd(a, b)


def factors(n):
    return [d for d in range(1, n + 1) if n % d == 0]


def pf(n):
    out, p = {}, 2
    while n > 1:
        while n % p == 0:
            out[p] = out.get(p, 0) + 1
            n //= p
        p += 1
    return out


def ixf(d):
    return " × ".join("%d<sup>%d</sup>" % (p, e) if e > 1 else str(p) for p, e in sorted(d.items()))


# ------------------------------------------------------------ set 1: factors, multiples, primes
def one_fmp(r):
    kind = r.choice(["factor", "multiple", "prime", "notprime", "factor"])
    if kind == "factor":
        n = r.choice([24, 36, 40, 42, 45, 48, 54, 56, 60, 63, 64, 72, 75, 84, 90, 96])
        fs = [d for d in factors(n) if 2 < d < n]
        right = r.choice(fs)
        wr = [n * 2, n + right, right + 1 if n % (right + 1) else right + 3, n // right * 2 + 1]
        wr = [w for w in wr if n % w]
        q = "Which number is a %s of %s?" % (B("factor"), num(n))
        e = "%d ÷ %d = %d with no remainder, so <b>%d</b> is a factor of %d. A factor divides into the number exactly." % (n, right, n // right, right, n)
        return QN(q, right, wr, e)
    if kind == "multiple":
        k = r.choice([6, 7, 8, 9, 11, 12, 13, 15])
        right = k * r.randint(4, 12)
        cands = [d for d in factors(right) if d not in (1, right) and d % k]
        wr = [right + 1, right - k + 2, k + 10] + cands[:1]
        wr = [w for w in wr if w % k]
        q = "Which number is a %s of %d?" % (B("multiple"), k)
        e = "%d = %d × %d, so <b>%d</b> is in the %d times table. A multiple is the number times a whole number." % (right, k, right // k, right, k)
        return QN(q, right, wr, e)
    if kind == "prime":
        p = r.choice([p for p in PRIMES if 20 < p < 98])
        wr = r.sample([n for n in [21, 27, 33, 39, 49, 51, 57, 63, 69, 77, 81, 87, 91, 93] if abs(n - p) < 40], 3)
        q = "Which of these is a %s number?" % B("prime")
        e = "<b>%d</b> has exactly two factors, 1 and itself. %s" % (p, "; ".join(
            "%d = %s" % (w, " × ".join(str(x) for x in [min(f for f in factors(w) if f > 1), w // min(f for f in factors(w) if f > 1)])) for w in wr))
        return QN(q, p, wr, e)
    n = r.choice([1, 9, 15, 21, 27, 39, 51, 57, 91])
    pr = r.sample([2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37], 3)
    q = "Which of these is %s a prime number?" % B("not")
    why = "1 has only one factor, so it is not prime." if n == 1 else "%d = %d × %d, so it has more than two factors." % (
        n, min(f for f in factors(n) if f > 1), n // min(f for f in factors(n) if f > 1))
    return QN(q, n, pr, "<b>%d</b> is not prime: %s" % (n, why))


# ------------------------------------------------------------ set 2: prime factorisation
def one_pf(r):
    n = r.choice([12, 18, 20, 24, 28, 30, 36, 40, 42, 45, 48, 50, 54, 56, 60, 63, 66, 70, 72, 75, 78, 80, 84, 88, 90,
                  96, 98, 100, 108, 112, 120, 126, 132, 135, 140, 144, 150, 168, 180, 196, 200, 225, 252, 300, 360])
    d = pf(n)
    if len(d) == 1 and list(d.values())[0] < 3:
        return None
    right = ixf(d)
    wrongs = []
    ps = sorted(d)
    # wrong power
    p0 = r.choice(ps)
    d2 = dict(d); d2[p0] += 1; wrongs.append(ixf(d2))
    d3 = dict(d)
    if d3[p0] > 1:
        d3[p0] -= 1
    else:
        del d3[p0]
    wrongs.append(ixf(d3) if d3 else "1")
    # non-prime factor pair
    f = [x for x in factors(n) if 1 < x < n and x not in PRIMES]
    if f:
        a = r.choice(f)
        wrongs.append("%d × %d" % (min(a, n // a), max(a, n // a)))
    # powers multiplied instead of shown: 2 × 3 written as 2^2... use sum mistake: exponents swapped
    if len(ps) >= 2 and d[ps[0]] != d[ps[1]]:
        d4 = dict(d); d4[ps[0]], d4[ps[1]] = d[ps[1]], d[ps[0]]; wrongs.append(ixf(d4))
    wrongs = [w for w in wrongs if w != right]
    if len(set(wrongs)) < 3:
        return None
    q = "Write %s as a product of prime factors in index form." % B(num(n))
    e = "Divide by primes: %s. So %d = <b>%s</b>." % (
        ", ".join("%d appears %d time%s" % (p, k, "" if k == 1 else "s") for p, k in sorted(d.items())), n, right)
    return T(q, right, wrongs[:3], e)


# ------------------------------------------------------------ set 3: HCF
def one_hcf(r):
    h = r.choice([2, 3, 4, 5, 6, 7, 8, 9, 12, 14, 15, 18])
    a, b = r.sample([2, 3, 4, 5, 7], 2)
    if gcd(a, b) != 1:
        return None
    x, y = h * a, h * b
    if max(x, y) > 150:
        return None
    L = lcm(x, y)
    small_common = [d for d in factors(h) if 1 < d < h]
    wr = [L, min(x, y), small_common[0] if small_common else h * 2, x * y]
    q = "Find the %s of %d and %d." % (B("highest common factor (HCF)"), x, y)
    e = "Factors of %d: %s. Factors of %d: %s. The biggest number in both lists is <b>%d</b>." % (
        x, ", ".join(map(str, factors(x))), y, ", ".join(map(str, factors(y))), h)
    return QN(q, h, wr, e)


# ------------------------------------------------------------ set 4: LCM
def one_lcm(r):
    x, y = r.sample([4, 6, 8, 9, 10, 12, 14, 15, 16, 18, 20, 21, 24], 2)
    if gcd(x, y) == 1 or gcd(x, y) in (x, y):
        return None
    L = lcm(x, y)
    if L > 200:
        return None
    wr = [x * y, gcd(x, y), max(x, y), L * 2]
    q = "Find the %s of %d and %d." % (B("lowest common multiple (LCM)"), x, y)
    mx = [x * k for k in range(1, L // x + 1)]
    e = "Multiples of %d: %s, … The first one that is also a multiple of %d is <b>%d</b>. (%d × %d = %d is a common multiple, but not the lowest.)" % (
        x, ", ".join(map(str, mx)), y, L, x, y, x * y)
    return QN(q, L, wr, e)


def one_pf_use(r):
    """HCF / LCM from prime factor form."""
    a = r.choice([2, 3]); b = r.choice([3, 5, 7])
    if a == b:
        return None
    da = {2: r.randint(1, 3), 3: r.randint(1, 2), 5: r.randint(0, 1)}
    db = {2: r.randint(1, 3), 3: r.randint(0, 2), 7: r.randint(0, 1)}
    da = {p: e for p, e in da.items() if e}; db = {p: e for p, e in db.items() if e}
    x = 1
    for p, e in da.items(): x *= p ** e
    y = 1
    for p, e in db.items(): y *= p ** e
    if x == y or gcd(x, y) in (x, y):
        return None
    which = r.choice(["HCF", "LCM"])
    val = gcd(x, y) if which == "HCF" else lcm(x, y)
    other = lcm(x, y) if which == "HCF" else gcd(x, y)
    q = "%d = %s and %d = %s. Find the %s of %d and %d." % (x, ixf(da), y, ixf(db), B(which), x, y)
    e = ("HCF: take each prime in <i>both</i>, with the lower power. LCM: take every prime, with the higher power. "
         "The %s is <b>%d</b>." % (which, val))
    return QN(q, val, [other, x * y, val * 2], e)


# ------------------------------------------------------------ set 5: problems
def problems():
    its = []
    for a, b, start in [(12, 18, "8:00 am"), (15, 20, "9:00 am"), (10, 25, "7:00 am"), (6, 8, "noon"), (20, 30, "6:00 am")]:
        L = lcm(a, b)
        q = ("Bus A leaves the station every %d minutes and bus B every %d minutes. Both leave at %s. "
             "After how many minutes do they next leave together?" % (a, b, start))
        e = "This is the LCM of %d and %d: <b>%d minutes</b>." % (a, b, L)
        its.append(QN(q, L, [a * b, gcd(a, b), a + b], e, unit=" minutes"))
    for a, b, it1, it2 in [(24, 36, "pencils", "rubbers"), (30, 45, "apples", "pears"), (18, 27, "red counters", "blue counters"),
                           (40, 56, "sweets", "biscuits"), (42, 70, "boys", "girls")]:
        h = gcd(a, b)
        what = "teams" if it1 == "boys" else "bags"
        q = ("There are %d %s and %d %s. They are shared into identical %s with nothing left over. "
             "What is the greatest number of %s that can be made?" % (a, it1, b, it2, what, what))
        e = "This is the HCF of %d and %d: <b>%d</b>. Each of the %d %s has %d %s and %d %s." % (a, b, h, h, what, a // h, it1, b // h, it2)
        its.append(QN(q, h, [lcm(a, b), a + b, h // 2 if h % 2 == 0 else h * 2], e))
    for a, b, what in [(6, 8, "Hot dogs come in packs of 6 and buns in packs of 8"),
                       (10, 12, "Plates come in packs of 10 and cups in packs of 12"),
                       (9, 12, "Pens come in boxes of 9 and pencils in boxes of 12")]:
        L = lcm(a, b)
        q = "%s. What is the smallest number of each you can buy to have the same number?" % what
        e = "The LCM of %d and %d is <b>%d</b>." % (a, b, L)
        its.append(QN(q, L, [a * b, gcd(a, b), max(a, b)], e))
    for w, l in [(12, 18), (24, 40), (30, 42)]:
        h = gcd(w, l)
        q = "A floor is %d m by %d m. It is covered with the largest possible square tiles, with no cutting. What is the side length of each tile?" % (w, l)
        e = "The side must divide both %d and %d, so use the HCF: <b>%d m</b>." % (w, l, h)
        its.append(QN(q, h, [lcm(w, l), h // 2, w], e, unit=" m"))
    for n in [36, 64, 81, 100]:
        fs = factors(n)
        q = "How many factors does %d have?" % n
        e = "Factors of %d: %s. That is <b>%d factors</b>. A square number has an odd number of factors." % (n, ", ".join(map(str, fs)), len(fs))
        its.append(QN(q, len(fs), [len(fs) - 1, len(fs) + 1, len(fs) - 2], e))
    return its


def body():
    return lesson(
        "<p>A <b>factor</b> divides a number exactly. A <b>multiple</b> is in its times table. "
        "A <b>prime</b> has exactly two factors: 1 and itself (1 is not prime).</p>"
        "<p>Every whole number above 1 can be written as a <b>product of primes</b>. Use a factor tree and keep "
        "splitting until every branch ends in a prime.</p>",
        [("Write 60 as a product of prime factors.", ["60 = 6 × 10 = 2 × 3 × 2 × 5.", "Put in order with powers: 2² × 3 × 5."], "2² × 3 × 5"),
         ("Find the HCF and LCM of 12 and 18.", ["Factors of 12: 1, 2, 3, 4, 6, 12. Factors of 18: 1, 2, 3, 6, 9, 18. HCF = 6.",
                                                 "Multiples of 12: 12, 24, 36. 36 is also a multiple of 18, so LCM = 36."], "HCF 6, LCM 36")],
        ["Mixing up factors (they go into the number) and multiples (the number goes into them).",
         "Thinking 1, 9 or 51 is prime. 1 has one factor; 9 = 3 × 3; 51 = 3 × 17.",
         "Stopping a factor tree at a number that is not prime, such as 4 or 9.",
         "Giving the product as the LCM: 12 × 18 = 216 is a common multiple, but the lowest is 36."])


def main():
    sets = [S("Factors, multiples and primes", collect(one_fmp, 20, R)),
            S("Prime factorisation", collect(one_pf, 20, R)),
            S("Highest common factor", collect(one_hcf, 20, R)),
            S("Lowest common multiple", collect(one_lcm, 12, R) + collect(one_pf_use, 8, R)),
            S("Problems", problems())]
    make(7, "factors-multiples-and-primes", 4, "N",
         "Factors, Multiples and Primes: Prime Factorisation, HCF and LCM",
         "Year 7 Prime Factorisation, HCF and LCM Worksheets: Factors, Multiples and Primes with Answers",
         "Factors, multiples and primes",
         "Use the concepts and vocabulary of prime numbers, factors (or divisors), multiples, common factors, common "
         "multiples, highest common factor, lowest common multiple, prime factorisation, including using product notation "
         "and the unique factorisation property.",
         "Free Year 7 maths worksheets on factors, multiples and primes: prime factorisation in index form, highest common "
         "factor, lowest common multiple and HCF/LCM word problems. 100 questions with worked answers.",
         "Every number above 1 is a product of primes: 60 = 2² × 3 × 5.",
         "HCF: the biggest number that divides both. LCM: the smallest number both divide into.",
         body(),
         [("Is 1 a prime number?", "No. A prime number has exactly two factors. 1 has only one factor, itself."),
          ("How do I find the HCF using prime factors?", "Write both numbers as products of primes. Multiply the primes they share, using the lower power of each."),
          ("How do I find the LCM using prime factors?", "Multiply every prime that appears in either number, using the higher power of each."),
          ("When do I use HCF or LCM in a word problem?", "Use HCF when you split things into the largest equal groups. Use LCM when things repeat and you want when they next happen together.")],
         sets, R)


if __name__ == "__main__":
    main()
