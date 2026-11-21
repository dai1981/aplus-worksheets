# -*- coding: utf-8 -*-
"""
India Class 10 Maths, NCERT Chapter 1: Real Numbers (CBSE Unit I Number Systems)
  python3 tools/gen_in_maths_c10_real_numbers.py
Fundamental Theorem of Arithmetic (prime factorisation), HCF and LCM by prime factorisation, HCF × LCM = product of two
numbers, irrational numbers (√2, √3, √5, 3 + 2√5) and proof by contradiction, word problems (bells, tiles, columns, trays).
Wrong answers come from real mistakes: taking the highest powers for the HCF, adding HCF and LCM, multiplying three
numbers to get the LCM, treating √4 as irrational, thinking a rational plus an irrational can be rational.
"""
import random, math
from fractions import Fraction as F
from in_common import num, S, make, lesson, collect, mix, T, People, inr, MINUS

R = random.Random(910001)
P = People(R)
PR = [2, 3, 5, 7, 11, 13]


def fac(n):
    out, p = {}, 2
    while p * p <= n:
        while n % p == 0:
            out[p] = out.get(p, 0) + 1
            n //= p
        p += 1
    if n > 1:
        out[n] = out.get(n, 0) + 1
    return out


def pf(d, dot=True):
    parts = []
    for p in sorted(d):
        parts.append("%d<sup>%d</sup>" % (p, d[p]) if d[p] > 1 else "%d" % p)
    return " × ".join(parts)


def rnd_num(lo, hi):
    while True:
        n = R.randint(lo, hi)
        d = fac(n)
        if len(d) >= 2 and max(d) <= 13 and sum(d.values()) >= 3:
            return n


# ---------------------------------------------------------------- set 1: prime factorisation
def one_pf(r):
    kind = r.choice(["pf", "pf", "pf", "count", "which"])
    n = rnd_num(60, 3000)
    d = fac(n)
    if kind == "pf":
        p0 = sorted(d)[0]
        w1 = dict(d)
        w1[p0] += 1
        w2 = {k: 1 for k in d}
        w3 = dict(d)
        k = max(d, key=lambda q: d[q])
        w3[k] = max(1, w3[k] - 1)
        return T("Express %s as a product of its prime factors." % num(n), pf(d),
                 [pf(w1), pf(w2) if w2 != d else pf(w1) + " × 1", pf(w3) if w3 != d else "%d × %d" % (p0, n // p0)],
                 "Keep dividing by primes: %s = <b>%s</b>. By the Fundamental Theorem of Arithmetic this factorisation is unique." % (num(n), pf(d)))
    if kind == "count":
        t = sum(d.values())
        return T("How many prime factors (counted with repetition) does %s have? (%s = %s)" % (num(n), num(n), pf(d)), str(t),
                 [str(len(d)), str(t + 1), str(t - 1) if t - 1 != len(d) else str(t + 2)],
                 "Count every prime, including repeats: %s → <b>%d</b>." % (pf(d), t))
    a = r.choice([4, 6, 8, 9, 12, 15, 10, 20])
    fa = fac(a)
    has = 2 in fa and 5 in fa
    miss = "2 or 5" if (2 not in fa and 5 not in fa) else ("5" if 5 not in fa else "2")
    ans = "Yes" if has else "No"
    return T("Can %d<sup>n</sup> end with the digit 0 for some natural number n?" % a, ans,
             ["No" if has else "Yes", "Only when n is even", "Only when n is odd"],
             "A number ending in 0 is divisible by 10 = 2 × 5, so its prime factors must include both 2 and 5. %d<sup>n</sup> = (%s)<sup>n</sup> %s. <b>%s</b>" % (
                 a, pf(fa), "contains both 2 and 5" if has else "has no prime factor " + miss, ans))


def hcf_lcm_strs(nums_):
    ds = [fac(n) for n in nums_]
    ps = sorted(set(p for d in ds for p in d))
    h = {p: min(d.get(p, 0) for d in ds) for p in ps}
    l = {p: max(d.get(p, 0) for d in ds) for p in ps}
    h = {p: e for p, e in h.items() if e}
    return h, l


def val(d):
    v = 1
    for p, e in d.items():
        v *= p ** e
    return v


# ---------------------------------------------------------------- set 2: HCF and LCM by prime factorisation
def one_hl(r):
    k = r.choice([2, 2, 2, 3])
    while True:
        base = r.choice([2, 3, 4, 6, 5, 7, 9, 12])
        ns = sorted(set(base * r.randint(2, 30) for _ in range(k)))
        if len(ns) == k and max(ns) <= 600 and all(max(fac(n)) <= 13 for n in ns):
            break
    h = math.gcd(*ns)
    l = ns[0]
    for n in ns[1:]:
        l = l * n // math.gcd(l, n)
    if l > 100000:
        return None
    which = r.choice(["HCF", "LCM"])
    hd, ld = hcf_lcm_strs(ns)
    lst = ", ".join(num(n) for n in ns[:-1]) + " and " + num(ns[-1])
    facts = "; ".join("%s = %s" % (num(n), pf(fac(n))) for n in ns)
    prod = 1
    for n in ns:
        prod *= n
    if which == "HCF":
        return T("Find the HCF of %s by prime factorisation." % lst, num(h), [num(l), num(min(ns)) if min(ns) != h else num(h * 2), num(h * base) if h * base not in (l, h) else num(h + 1)],
                 "%s. HCF = product of the <b>smallest</b> power of each common prime = %s = <b>%s</b>." % (facts, pf(hd) if hd else "1", num(h)))
    return T("Find the LCM of %s by prime factorisation." % lst, num(l), [num(h), num(prod) if prod != l else num(l * 2), num(l // 2) if l % 2 == 0 and l // 2 not in ns else num(l + base)],
             "%s. LCM = product of the <b>greatest</b> power of each prime = %s = <b>%s</b>." % (facts, pf(ld), num(l)))


# ---------------------------------------------------------------- set 3: HCF × LCM = product
def one_prod(r):
    kind = r.choice(["lcm", "lcm", "other", "check", "rel"])
    h = r.choice([2, 3, 4, 5, 6, 7, 8, 9, 12, 13, 15, 18])
    a, b = r.sample(range(2, 20), 2)
    if math.gcd(a, b) != 1:
        return None
    x, y = h * a, h * b
    l = h * a * b
    if kind == "lcm":
        return T("The HCF of %s and %s is %s. Find their LCM." % (num(x), num(y), num(h)), num(l),
                 [num(x * y), num(x * y // h // h) if x * y // h // h != l else num(l * 2), num(x + y - h)],
                 "HCF × LCM = product of the two numbers: LCM = %s × %s ÷ %s = <b>%s</b>." % (num(x), num(y), num(h), num(l)))
    if kind == "other":
        return T("The HCF of two numbers is %s and their LCM is %s. One number is %s. Find the other." % (num(h), num(l), num(x)), num(y),
                 [num(l // h), num(l * h // x // h) if l * h // x // h != y else num(y * 2), num(l - x)],
                 "Other number = HCF × LCM ÷ first number = %s × %s ÷ %s = <b>%s</b>." % (num(h), num(l), num(x), num(y)))
    if kind == "check":
        L2 = r.choice([h * a * b + r.choice([1, 2, 3, 5]), h * r.choice([5, 7, 11]) + 1])
        return T("Can two numbers have %s as their HCF and %s as their LCM?" % (num(h), num(L2)), "No, because %s is not divisible by %s" % (num(L2), num(h)),
                 ["Yes, any two numbers can", "Yes, because %s &gt; %s" % (num(L2), num(h)), "No, because the LCM must be less than 100"],
                 "The HCF always divides the LCM. %s ÷ %s is not a whole number, so <b>no</b>." % (num(L2), num(h)))
    return T("For any two positive integers a and b, which statement is always true?", "HCF(a, b) × LCM(a, b) = a × b",
             ["HCF(a, b) + LCM(a, b) = a + b", "HCF(a, b) × LCM(a, b) = a + b", "LCM(a, b) = a × b"],
             "<b>HCF × LCM = a × b</b>. LCM = a × b only when HCF = 1. (This product rule does not hold for three numbers.)")


# ---------------------------------------------------------------- set 4: irrational numbers
SQ = {4: 2, 9: 3, 16: 4, 25: 5, 36: 6, 49: 7, 64: 8, 81: 9, 100: 10}


def one_irr(r):
    kind = r.choice(["which", "which", "sum", "proof", "prod"])
    if kind == "which":
        p = r.choice([2, 3, 5, 6, 7, 11, 13])
        sq = r.sample(sorted(SQ), 3)
        rats = ["√%d" % s for s in sq[:2]] + [r.choice(["%d/%d" % (r.randint(1, 9), r.randint(2, 9)), "0.%d" % r.randint(11, 99), "√%d" % sq[2]])]
        irr = r.choice(["√%d" % p, "%d + √%d" % (r.randint(1, 9), p), "%d√%d" % (r.randint(2, 7), p), "√%d/%d" % (p, r.randint(2, 7))])
        return T("Which of these numbers is irrational?", irr, rats,
                 "%s = %s are rational. √%d cannot be written as p/q, so <b>%s</b> is irrational." % (" and ".join(rats[:2]), " and ".join(str(SQ[s]) for s in sq[:2]), p, irr))
    if kind == "sum":
        a, b = r.randint(2, 9), r.randint(2, 7)
        p = r.choice([2, 3, 5, 7])
        e = r.choice(["%d + %d√%d" % (a, b, p), "%d − %d√%d" % (a, b, p), "%d√%d" % (b, p)])
        return T("%s is" % e, "irrational", ["rational", "an integer", "rational, because %d and %d are rational" % (a, b)],
                 "If %s = r were rational, then √%d = (rational) would be rational — a contradiction. So it is <b>irrational</b>." % (e, p))
    if kind == "prod":
        p = r.choice([2, 3, 5, 7])
        a = r.randint(3, 6)
        c, val_ = r.choice([("(√%d)²" % p, p), ("√%d × √%d" % (p, p), p), ("(%d + √%d)(%d − √%d)" % (a, p, a, p), a * a - p)])
        return T("Is %s rational or irrational?" % c, "rational (= %d)" % val_, ["irrational", "irrational, because it contains √%d" % p, "rational (= %d)" % (val_ + p)],
                 "Work it out: %s = <b>%d</b>, which is rational. A product of irrational numbers can be rational." % (c, val_))
    p = r.choice([2, 3, 5])
    return T("In the proof that √%d is irrational, we assume √%d = a/b (a, b coprime). What do we show next?" % (p, p),
             "%d divides both a and b, which contradicts that they are coprime" % p,
             ["a and b are both even, so √%d is even" % p, "a = %d b, so √%d is an integer" % (p, p), "a² = b², so a = b"],
             "Squaring gives a² = %db², so %d divides a; writing a = %dc gives b² = %dc², so %d divides b. <b>%d divides both a and b — a contradiction.</b>" % (p, p, p, p, p, p))


# ---------------------------------------------------------------- set 5: word problems
def one_word(r):
    kind = r.choice(["bells", "track", "tiles", "army", "trays", "ropes"])
    name, he, his = P.next()
    if kind == "bells":
        a, b, c = sorted(r.sample([6, 8, 9, 10, 12, 15, 18, 20], 3))
        l = a * b // math.gcd(a, b)
        l = l * c // math.gcd(l, c)
        h0 = r.choice([7, 8, 9])
        return T("Three bells ring every %d, %d and %d minutes. They ring together at %d a.m. After how many minutes will they next ring together?" % (a, b, c, h0),
                 "%d minutes" % l, ["%s minutes" % num(a * b * c), "%d minutes" % math.gcd(math.gcd(a, b), c) if math.gcd(math.gcd(a, b), c) > 1 else "%d minutes" % (a + b + c), "%d minutes" % (l * 2)],
                 "They ring together after a common multiple of the times; the first one is the LCM(%d, %d, %d) = <b>%d minutes</b>." % (a, b, c, l))
    if kind == "track":
        a, b = r.sample([12, 15, 18, 20, 24, 30, 36], 2)
        l = a * b // math.gcd(a, b)
        return T("On a circular track, %s takes %d minutes to drive one round and %s friend takes %d minutes. They start together. After how many minutes are they at the start together again?" % (name, a, his, b),
                 "%d minutes" % l, ["%d minutes" % (a * b), "%d minutes" % math.gcd(a, b), "%d minutes" % (a + b)],
                 "LCM(%d, %d) = <b>%d minutes</b>." % (a, b, l))
    if kind == "tiles":
        h = r.choice([20, 25, 30, 40, 45, 50, 60])
        a, b = r.sample(range(3, 12), 2)
        if math.gcd(a, b) != 1:
            return None
        L, W = h * a, h * b
        return T("A room is %s cm long and %s cm wide. What is the largest square tile (side in cm) that covers the floor exactly?" % (num(L), num(W)),
                 "%d cm" % h, ["%s cm" % num(L * W // h), "%d cm" % (h // 5 if h % 5 == 0 and h // 5 > 1 else h * 2), "%s cm" % num(L - W) if L - W != h else "%d cm" % (h * 2)],
                 "The side must divide both lengths: HCF(%s, %s) = <b>%d cm</b>." % (num(L), num(W), h))
    if kind == "army":
        h = r.choice([4, 6, 8, 9, 12, 16])
        a, b = r.sample(range(5, 40), 2)
        if math.gcd(a, b) != 1:
            return None
        x, y = h * a, h * b
        return T("A contingent of %d members marches behind a band of %d members. Both groups march in the same number of columns. What is the greatest number of columns?" % (x, y),
                 str(h), [num(x * y // h), str(math.gcd(x, y) // 2) if h % 2 == 0 and h // 2 > 1 else str(h * 2), str(abs(x - y))],
                 "The number of columns must divide %d and %d: HCF = <b>%d</b>." % (x, y, h))
    if kind == "trays":
        h = r.choice([10, 12, 15, 18, 20, 24, 30])
        a, b = r.sample(range(5, 30), 2)
        if math.gcd(a, b) != 1:
            return None
        x, y = h * a, h * b
        return T("A sweet seller has %d kaju barfis and %d badam barfis. He stacks them so that each stack has the same number of one kind only. What is the most barfis in each stack (fewest trays)?" % (x, y),
                 str(h), [num(x * y // h), num(x + y), str(h // 2) if h % 2 == 0 else str(h * 3)],
                 "HCF(%d, %d) = <b>%d</b> barfis per stack." % (x, y, h))
    h = r.choice([4, 5, 6, 8, 9, 12, 15])
    a, b, c = r.sample(range(3, 20), 3)
    if math.gcd(math.gcd(a, b), c) != 1:
        return None
    x, y, z = h * a, h * b, h * c
    return T("Three ropes are %d m, %d m and %d m long. What is the greatest length (in m) of pieces that can measure all three exactly?" % (x, y, z),
             "%d m" % h, ["%s m" % num(x * y * z // h // h) if x * y * z // h // h < 10 ** 6 else "%d m" % (h * 3), "%d m" % min(x, y, z), "%d m" % (h // 2) if h % 2 == 0 else "%d m" % (h * 2)],
             "HCF(%d, %d, %d) = <b>%d m</b>." % (x, y, z, h))


def main():
    seen = set()
    sets = [
        S("Prime factorisation", mix(R, [(one_pf, 20)], seen)),
        S("HCF and LCM by prime factorisation", mix(R, [(one_hl, 20)], seen)),
        S("HCF × LCM = product of the numbers", mix(R, [(one_prod, 20)], seen)),
        S("Irrational numbers", mix(R, [(one_irr, 20)], seen)),
        S("Word problems", mix(R, [(one_word, 20)], seen)),
    ]
    body = lesson(
        "<p><b>Fundamental Theorem of Arithmetic</b>: every composite number can be written as a product of primes in exactly one way (apart from the order).</p>"
        "<p>HCF = product of the <b>smallest</b> power of each common prime. LCM = product of the <b>greatest</b> power of each prime.</p>"
        "<p>For two numbers, HCF × LCM = product of the numbers.</p>"
        "<p>A number is <b>irrational</b> if it cannot be written as p/q. √2, √3, √5 are irrational. Rational + irrational is irrational.</p>",
        [("Find the HCF and LCM of 96 and 404.", ["96 = 2<sup>5</sup> × 3, 404 = 2<sup>2</sup> × 101", "HCF = 2<sup>2</sup> = 4", "LCM = 2<sup>5</sup> × 3 × 101"], "HCF = 4, LCM = 9,696"),
         ("Show that 5 − √3 is irrational.", ["Suppose 5 − √3 = r (rational)", "Then √3 = 5 − r, which is rational", "Contradiction"], "5 − √3 is irrational")],
        ["Taking the greatest powers for the HCF (that gives the LCM).",
         "Using HCF × LCM = product for three numbers. It works only for two.",
         "Calling √4 or √9 irrational. They equal 2 and 3."])
    faq = [
        ("What is the Fundamental Theorem of Arithmetic?", "Every composite number can be expressed as a product of primes, and this factorisation is unique apart from the order of the factors."),
        ("How do I find the HCF and LCM by prime factorisation?", "Write each number as a product of primes. HCF: multiply the smallest power of each common prime. LCM: multiply the greatest power of every prime that appears."),
        ("Why can 6ⁿ never end with the digit 0?", "A number ending in 0 must have both 2 and 5 as prime factors. 6ⁿ = 2ⁿ × 3ⁿ has no factor 5."),
        ("How do I prove that √2 is irrational?", "Assume √2 = a/b with a and b coprime. Squaring gives a² = 2b², so 2 divides a and then 2 divides b. This contradicts that a and b are coprime."),
    ]
    make(10, "real-numbers", 1, "I", 1, "Real Numbers: HCF, LCM and Irrational Numbers", "real numbers",
         "Fundamental Theorem of Arithmetic (statements after reviewing work done earlier and after illustrating and motivating through examples); proofs of irrationality of √2, √3 and √5 (summary of the CBSE syllabus)",
         "Class 10 Real Numbers worksheet (NCERT Chapter 1): prime factorisation, HCF and LCM, HCF × LCM, irrational numbers and word problems. 100 practice questions with answers, free and printable.",
         "Every composite number = a unique product of primes", "HCF uses the smallest powers, LCM the greatest powers.",
         body, faq, sets, R)


if __name__ == "__main__":
    main()
