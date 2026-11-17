# -*- coding: utf-8 -*-
"""
AU Year 7 Maths: Prime factorisation and index notation (Australian Curriculum v9.0: AC9M7N02)
  python3 tools/gen_au_maths_y7_prime_factorisation_and_index_notation.py
Writing repeated multiplication with exponents, primes and composites, the prime factors of a number, writing
a number as a product of powers of primes (factor trees), working back from index form, and using prime
factors for HCF and LCM problems.
Wrong answers come from real mistakes: 2³ = 6, writing 2 × 2 × 2 as 3², leaving a composite number (4 or 9)
in a factor tree, counting 1 as prime, and giving the product instead of the LCM.
"""
import random
from math import gcd
from au_hs import num, B, S, make, lesson, collect, QN, T

R = random.Random(70201)
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


def val(d):
    v = 1
    for p, e in d.items():
        v *= p ** e
    return v


# ------------------------------------------------------------ set 1: index notation
def one_index(r):
    kind = r.choice(["write1", "write2", "eval", "eval"])
    if kind == "write1":
        b, e = r.randint(2, 9), r.randint(3, 6)
        if b == e:
            return None
        q = "Write %s using index notation." % B(" × ".join([str(b)] * e))
        right = "%d<sup>%d</sup>" % (b, e)
        return T(q, right, ["%d<sup>%d</sup>" % (e, b), "%d × %d" % (b, e), str(b * e)],
                 "%d is multiplied by itself %d times, so it is <b>%s</b>. The base is %d and the exponent (index) is %d." % (b, e, right, b, e))
    if kind == "write2":
        a, b = r.sample([2, 3, 5, 7], 2)
        a, b = min(a, b), max(a, b)
        ea, eb = r.randint(2, 4), r.randint(1, 3)
        if ea == eb:
            return None
        q = "Write %s using index notation." % B(" × ".join([str(a)] * ea + [str(b)] * eb))
        right = ixf({a: ea, b: eb})
        wr = [ixf({a: eb, b: ea}), "%d<sup>%d</sup>" % (a * b, ea + eb), "%d<sup>%d</sup> × %d<sup>%d</sup>" % (a, ea + 1, b, eb) if eb > 1 else "%d<sup>%d</sup>" % (a, ea + eb)]
        return T(q, right, wr, "There are %d lots of %d and %d lot%s of %d: <b>%s</b>." % (ea, a, eb, "" if eb == 1 else "s", b, right))
    b, e = r.choice([(2, 3), (2, 4), (2, 5), (2, 6), (3, 3), (3, 4), (5, 3), (4, 3), (10, 4), (2, 7), (6, 2), (7, 2), (3, 5), (10, 5)])
    v = b ** e
    return QN("Work out %s." % B("%d<sup>%d</sup>" % (b, e)), v, [b * e, e ** b if e ** b != v else v + b, v // b],
              "%d<sup>%d</sup> = %s = <b>%s</b>, not %d × %d." % (b, e, " × ".join([str(b)] * e), num(v), b, e))


# ------------------------------------------------------------ set 2: primes, composites and prime factors
def one_prime(r):
    kind = r.choice(["prime", "notprime", "pfs", "pfs"])
    if kind == "prime":
        p = r.choice([p for p in PRIMES if 20 < p < 98])
        wr = r.sample([n for n in [21, 27, 33, 39, 49, 51, 57, 63, 69, 77, 81, 87, 91, 93] if abs(n - p) < 40], 3)
        e = "<b>%d</b> has exactly two factors, 1 and itself. The others are composite: %s." % (p, "; ".join(
            "%d = %d × %d" % (w, min(f for f in factors(w) if f > 1), w // min(f for f in factors(w) if f > 1)) for w in wr))
        return QN("Which of these is a %s number?" % B("prime"), p, wr, e)
    if kind == "notprime":
        n = r.choice([1, 9, 15, 21, 27, 39, 51, 57, 91, 87])
        pr = r.sample([2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43], 3)
        why = "1 has only one factor, so it is not prime." if n == 1 else "%d = %d × %d, so it is composite (it has more than two factors)." % (
            n, min(f for f in factors(n) if f > 1), n // min(f for f in factors(n) if f > 1))
        return QN("Which of these is %s a prime number?" % B("not"), n, pr, "<b>%d</b> is not prime. %s" % (n, why))
    n = r.choice([30, 42, 66, 70, 78, 84, 90, 105, 110, 126, 130, 140, 154, 165, 180, 198, 210, 220, 231, 260])
    d = pf(n)
    right = ", ".join(str(p) for p in sorted(d))
    comp = [x for x in factors(n) if 1 < x < n and x not in PRIMES]
    w1 = ", ".join(str(p) for p in sorted(list(d) + [comp[0]])) if comp else right + ", 1"
    w2 = "1, " + right
    w3 = ", ".join(str(p) for p in sorted(d)[:-1]) if len(d) > 2 else ", ".join(str(x) for x in factors(n)[1:4])
    return T("What are the prime factors of %s?" % B(num(n)), right, [w1, w2, w3],
             "%d = %s. The prime factors are <b>%s</b>. 1 is not prime, and %s is not prime." % (n, ixf(d), right, comp[0] if comp else "4"))


# ------------------------------------------------------------ set 3: prime factorisation in index form
def one_pf(r):
    n = r.choice([24, 28, 36, 40, 44, 45, 48, 52, 54, 56, 63, 72, 75, 80, 88, 96, 98, 99, 104, 108, 112, 117, 120, 135,
                  144, 147, 150, 160, 162, 175, 189, 196, 216, 225, 240, 250, 252, 288, 324, 350, 375, 392, 400, 450, 500])
    d = pf(n)
    right = ixf(d)
    ps = sorted(d)
    wrongs = []
    p0 = r.choice(ps)
    d2 = dict(d)
    d2[p0] += 1
    wrongs.append(ixf(d2))
    f = [x for x in factors(n) if 1 < x < n and x not in PRIMES]
    if f:
        a = r.choice(f)
        b = n // a
        wrongs.append("%d × %d" % (min(a, b), max(a, b)))
    if len(ps) >= 2 and d[ps[0]] != d[ps[1]]:
        d4 = dict(d)
        d4[ps[0]], d4[ps[1]] = d[ps[1]], d[ps[0]]
        wrongs.append(ixf(d4))
    big = max(ps, key=lambda p: d[p])
    if d[big] >= 2:
        wrongs.append(ixf(d).replace("%d<sup>%d</sup>" % (big, d[big]), "%d" % (big * d[big]), 1))
    wrongs = [w for w in dict.fromkeys(wrongs) if w != right]
    if len(wrongs) < 3:
        return None
    q = "Write %s as a product of its prime factors in index notation." % B(num(n))
    e = "Use a factor tree and keep going until every branch is prime: %s. So %d = <b>%s</b>." % (
        ", ".join("%d appears %d time%s" % (p, k, "" if k == 1 else "s") for p, k in sorted(d.items())), n, right)
    return T(q, right, wrongs[:3], e)


# ------------------------------------------------------------ set 4: from index form
def one_back(r):
    kind = r.choice(["value", "value", "missing"])
    d = {2: r.randint(1, 4), 3: r.randint(0, 2), 5: r.randint(0, 2), 7: r.randint(0, 1)}
    d = {p: e for p, e in d.items() if e}
    if len(d) < 2:
        return None
    n = val(d)
    if n > 2000:
        return None
    if kind == "value":
        q = "Which number is equal to %s?" % B(ixf(d))
        wrong1 = 1
        for p, e in d.items():
            wrong1 *= p * e
        wrong2 = sum(p ** e for p, e in d.items())
        wrong3 = n * 2
        return QN(q, n, [wrong1, wrong2, wrong3], "%s = <b>%s</b>." % (" × ".join(str(p ** e) for p, e in sorted(d.items())), num(n)))
    big = [p for p in d if d[p] >= 2]
    if not big:
        return None
    p = r.choice(big)
    e = d[p]
    rest = dict(d)
    del rest[p]
    shown = " × ".join(["%d<sup><i>k</i></sup>" % p] + ["%d<sup>%d</sup>" % (q, x) if x > 1 else str(q) for q, x in sorted(rest.items())])
    q = "%s = %s. What is the value of %s?" % (num(n), B(shown), "<i>k</i>")
    return QN(q, e, [p ** e, e + 1, n // val(rest)] if n // val(rest) != e else [p ** e, e + 1, e + 2],
              "%d ÷ %s = %d = %d<sup>%d</sup>, so <i>k</i> = <b>%d</b>." % (n, num(val(rest)), p ** e, p, e, e))


# ------------------------------------------------------------ set 5: problems (HCF and LCM)
def one_hcf_lcm(r):
    da = {2: r.randint(1, 3), 3: r.randint(1, 2), 5: r.randint(0, 1)}
    db = {2: r.randint(1, 3), 3: r.randint(0, 2), 7: r.randint(0, 1)}
    da = {p: e for p, e in da.items() if e}
    db = {p: e for p, e in db.items() if e}
    x, y = val(da), val(db)
    if x == y or gcd(x, y) in (x, y):
        return None
    which = r.choice(["highest common factor (HCF)", "lowest common multiple (LCM)"])
    v = gcd(x, y) if "HCF" in which else lcm(x, y)
    other = lcm(x, y) if "HCF" in which else gcd(x, y)
    q = "%d = %s and %d = %s. Find the %s of %d and %d." % (x, ixf(da), y, ixf(db), B(which), x, y)
    e = ("HCF: multiply the primes in <i>both</i> numbers, using the lower power. LCM: multiply every prime, using the higher power. "
         "The answer is <b>%s</b>." % num(v))
    return QN(q, v, [other, x * y, v * 2], e)


def problems():
    its = collect(one_hcf_lcm, 6, R)
    for a, b, what in [(12, 15, "The 412 bus leaves every 12 minutes and the 415 bus every 15 minutes"),
                       (8, 10, "One lighthouse flashes every 8 seconds and another every 10 seconds"),
                       (20, 30, "Ferry A leaves Circular Quay every 20 minutes and ferry B every 30 minutes"),
                       (6, 9, "Mia trains every 6 days and Lachlan every 9 days")]:
        L = lcm(a, b)
        unit = " seconds" if "seconds" in what else " days" if "days" in what else " minutes"
        q = "%s. They start together. How long until they are together again?" % what
        its.append(QN(q, L, [a * b, gcd(a, b), a + b], "This is the LCM of %d and %d: <b>%d%s</b>." % (a, b, L, unit), unit=unit))
    for a, b, it1, it2 in [(24, 36, "sausages", "bread rolls"), (36, 48, "muesli bars", "apples"), (28, 42, "boys", "girls"), (45, 60, "red pens", "blue pens")]:
        h = gcd(a, b)
        what = "teams" if it1 == "boys" else "bags"
        q = "There are %d %s and %d %s. They are split into identical %s with nothing left over. What is the greatest number of %s?" % (a, it1, b, it2, what, what)
        its.append(QN(q, h, [lcm(a, b), a + b, h // 2 if h % 2 == 0 else h * 2],
                      "This is the HCF of %d and %d: <b>%d</b>. Each has %d %s and %d %s." % (a, b, h, a // h, it1, b // h, it2)))
    data = [
        ("Which is the same as 2<sup>5</sup>?", "32", ["10", "25", "7"], "2 × 2 × 2 × 2 × 2 = <b>32</b>."),
        ("Which number is a product of three different primes?", "30", ["8", "12", "49"], "30 = 2 × 3 × 5, three different primes: <b>30</b>."),
        ("The prime factorisation of a number is 2<sup>3</sup> × 3. What is the number?", "24", ["18", "12", "36"], "8 × 3 = <b>24</b>."),
        ("How many prime numbers are between 20 and 40?", "4", ["5", "3", "6"], "23, 29, 31 and 37: <b>4</b>."),
        ("Which is the smallest number that has 2, 3 and 5 as prime factors?", "30", ["10", "15", "60"], "2 × 3 × 5 = <b>30</b>."),
        ("A square number has prime factorisation 2<sup>2</sup> × 3<sup>2</sup>. What is its square root?", "6", ["36", "12", "18"],
         "2<sup>2</sup> × 3<sup>2</sup> = 36 and √36 = 2 × 3 = <b>6</b>."),
    ]
    its += [T(q, a, w, e) for q, a, w, e in data]
    return its


def body():
    return lesson(
        "<p><b>Index notation</b> shows repeated multiplication: 2 × 2 × 2 = 2<sup>3</sup>. The 2 is the <b>base</b> and the 3 is the <b>exponent</b> (or index).</p>"
        "<p>Every whole number above 1 is either prime or a product of primes. Use a <b>factor tree</b>: split the number into "
        "two factors and keep going until every branch is prime. Then write the primes in order with exponents.</p>",
        [("Write 72 as a product of prime factors.", ["72 = 8 × 9 = 2 × 2 × 2 × 3 × 3."], "2<sup>3</sup> × 3<sup>2</sup>"),
         ("Work out 3<sup>4</sup>.", ["3 × 3 × 3 × 3."], "81"),
         ("Use primes to find the HCF of 12 = 2<sup>2</sup> × 3 and 18 = 2 × 3<sup>2</sup>.", ["Shared primes, lower powers: 2 × 3."], "6")],
        ["Working out 2<sup>3</sup> as 2 × 3 = 6. It is 2 × 2 × 2 = 8.",
         "Stopping the factor tree at 4 or 9. They are not prime.",
         "Writing 1 as a prime factor. 1 is not prime.",
         "Swapping the base and exponent: 2 × 2 × 2 is 2<sup>3</sup>, not 3<sup>2</sup>."])


def main():
    sets = [S("Index notation", collect(one_index, 20, R)),
            S("Primes and prime factors", collect(one_prime, 20, R)),
            S("Prime factorisation in index notation", collect(one_pf, 20, R)),
            S("Working back from index notation", collect(one_back, 20, R)),
            S("Prime factor problems", problems())]
    make(7, "prime-factorisation-and-index-notation", 2, "AC9M7N02",
         "Prime Factorisation and Index Notation",
         "Year 7 Prime Factorisation Worksheets: Factor Trees, Index Notation, HCF and LCM (Free, Answer Key)",
         "Prime factorisation",
         "represent natural numbers as products of powers of prime numbers using exponent notation",
         "Free Year 7 maths worksheets on prime factorisation for the Australian Curriculum (AC9M7N02): index notation, "
         "primes and prime factors, factor trees, products of powers of primes, and HCF and LCM problems. 100 questions with an answer key.",
         "Every number above 1 is a product of primes: 72 = 2³ × 3².",
         "Use a factor tree. Stop only when every branch is a prime.",
         body(),
         [("What is index notation?", "A short way to write repeated multiplication. 5 × 5 × 5 = 5³, where 5 is the base and 3 is the exponent."),
          ("How do I write a number as a product of prime factors?", "Draw a factor tree, splitting the number until every branch is prime. Then write the primes in order using exponents, for example 72 = 2³ × 3²."),
          ("Is 1 a prime number?", "No. A prime number has exactly two factors. 1 has only one."),
          ("How do prime factors help with HCF and LCM?", "For the HCF, multiply the primes both numbers share, with the lower power. For the LCM, multiply every prime, with the higher power.")],
         sets, R)


if __name__ == "__main__":
    main()
