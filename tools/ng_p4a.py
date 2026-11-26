# -*- coding: utf-8 -*-
"""
Nigeria Primary 4 Mathematics: question makers written for Nigeria (naira and kobo, Nigerian names, British spelling).
Each maker takes a random.Random and returns one multiple-choice item (ng_common.mcq); AssertionError means "draw again".
Used by ng_p4.py.
"""
import math
import random
from fractions import Fraction as F
from ng_common import mcq, comma, naira, words, fig, fr, Kid, PLACES, svg_wrap, text, GREEN, FILL, INK, RED, BLUE


def K(r):
    return Kid(r).next()


def ch(r, xs):
    return xs[r.randrange(len(xs))]


def dec(x, k=None):
    """Fraction/float -> '2.35' (exact), k digits if given."""
    x = F(x).limit_denominator(10 ** 6)
    if k is None:
        k = 0
        while (x * 10 ** k).denominator != 1:
            k += 1
            assert k <= 4
    n = int(round(abs(x) * 10 ** k))
    s = comma(n // 10 ** k) + ("." + str(n % 10 ** k).rjust(k, "0") if k else "")
    return ("−" if x < 0 else "") + s


def frac(x):
    x = F(x)
    if x.denominator == 1:
        return str(x.numerator)
    return fr(x.numerator, x.denominator)


# ============================================================ counting in steps
STEPS = [5, 7, 60, 100, 1000, 25, 50, 500]


def sk_next(r):
    st = ch(r, STEPS)
    a = r.randint(1, 40) * st if st < 100 else r.randint(1, 60) * st + ch(r, [0, 0, st // 2])
    seq = [a + i * st for i in range(4)]
    nx = seq[-1] + st
    w = [seq[-1] + st + 1, seq[-1] + st * 10 if st < 1000 else seq[-1] + 100, seq[-1] - st, seq[-1] + st // 5 if st >= 25 else seq[-1] + 10]
    return mcq("Count on in %ss. What comes next? %s, …" % (comma(st), ", ".join(comma(x) for x in seq)), nx, w,
               "Each number is %s more than the one before: %s + %s = <b>%s</b>." % (comma(st), comma(seq[-1]), comma(st), comma(nx)))


def sk_missing(r):
    st = ch(r, STEPS)
    a = r.randint(1, 50) * st
    seq = [a + i * st for i in range(5)]
    k = r.randint(1, 3)
    ans = seq[k]
    show = [comma(x) if i != k else "___" for i, x in enumerate(seq)]
    return mcq("Find the missing number: %s" % ", ".join(show), ans, [ans + 1, ans + 10, seq[k - 1] + st // 2 if st >= 10 else ans + 2, ans - 1],
               "The numbers go up in %ss: %s + %s = <b>%s</b>." % (comma(st), comma(seq[k - 1]), comma(st), comma(ans)))


def sk_back(r):
    st = ch(r, STEPS)
    a = r.randint(8, 80) * st
    seq = [a - i * st for i in range(4)]
    nx = seq[-1] - st
    return mcq("Count back in %ss. What comes next? %s, …" % (comma(st), ", ".join(comma(x) for x in seq)), nx, [seq[-1] + st, nx - 1, nx + 1, seq[-1] - 2 * st],
               "Each number is %s less: %s − %s = <b>%s</b>." % (comma(st), comma(seq[-1]), comma(st), comma(nx)))


def sk_60(r):
    k = r.randint(0, 2)
    if k == 0:
        h = r.randint(2, 12)
        return mcq("There are 60 minutes in 1 hour. Count in 60s: how many minutes are there in %d hours?" % h, 60 * h, [60 * h + 60, 60 * h - 60, 100 * h, 6 * h],
                   "60, 120, 180, … → %d × 60 = <b>%s minutes</b>." % (h, comma(60 * h)))
    if k == 1:
        n = r.randint(2, 12)
        return mcq("A crate holds 7 bottles of water. Count in 7s: how many bottles are in %d crates?" % n, 7 * n, [7 * n + 7, 7 * n - 7, 7 + n, 10 * n],
                   "7, 14, 21, … → %d × 7 = <b>%s bottles</b>." % (n, comma(7 * n)))
    n = r.randint(3, 10)
    st = ch(r, [100, 1000])
    return mcq("Ngozi saves ₦%s every month. Count in %ss: how much has she saved after %d months?" % (comma(st), comma(st), n), "₦" + comma(st * n),
               ["₦" + comma(st * (n + 1)), "₦" + comma(st * (n - 1)), "₦" + comma(st + n), "₦" + comma(st * n * 10)],
               "%s, %s, … → %d × %s = <b>₦%s</b>." % (comma(st), comma(2 * st), n, comma(st), comma(st * n)))


def sk_nth(r):
    st = ch(r, [5, 7, 25, 50, 60, 100])
    n = r.randint(6, 15)
    ans = st * n
    return mcq("Count in %ss starting from %s: %s, %s, %s, … What is the %s number in the list?" % (comma(st), comma(st), comma(st), comma(2 * st), comma(3 * st), ORD[n]), ans,
               [st * (n + 1), st * (n - 1), st + n, ans + 1],
               "The %s number is %d × %s = <b>%s</b>." % (ORD[n], n, comma(st), comma(ans)))


ORD = {6: "6th", 7: "7th", 8: "8th", 9: "9th", 10: "10th", 11: "11th", 12: "12th", 13: "13th", 14: "14th", 15: "15th"}


# ============================================================ whole numbers to one million
def wn_words(r):
    n = r.randint(10, 999) * 1000 + ch(r, [r.randint(1, 999), r.randint(1, 99), r.randint(100, 999)])
    if r.random() < 0.5:
        w1 = n - (n // 1000 % 10) * 1000 + ((n // 1000 % 10 + 1) % 10) * 1000
        w2 = int(str(n).replace("0", "", 1)) if "0" in str(n)[1:] else n + 10
        w3 = n // 1000 * 1000 + (n % 1000) // 10
        return mcq("Write %s in figures." % words(n), n, [w1, w2, w3, n * 10],
                   "%s thousand and %s: <b>%s</b>." % (comma(n // 1000), n % 1000, comma(n)))
    wrong = [n + 1000, n // 1000 * 1000 + (n % 1000 + 10) % 1000, n - 100 if n % 1000 >= 100 else n + 100]
    return mcq("Write the number %s using words." % comma(n), words(n), [words(x) for x in wrong if 0 < x < 1000000],
               "Read the thousands first, then the rest: <b>%s</b>." % words(n))


def wn_more(r):
    n = r.randint(10000, 989999)
    k = ch(r, [1000, 10000, 100000, 100])
    if n + k >= 1000000:
        raise AssertionError
    op = r.random() < 0.6
    ans = n + k if op else n - k
    return mcq("What is %s %s than %s?" % (comma(k), "more" if op else "less", comma(n)), ans,
               [n - k if op else n + k, n + k * 10 if op else n - k * 10, n + k // 10 if op else n - k // 10, ans + 1],
               "Only the %s digit changes: <b>%s</b>." % ({100: "hundreds", 1000: "thousands", 10000: "ten thousands", 100000: "hundred thousands"}[k], comma(ans)))


# ============================================================ comparing and ordering
def cmp_true(r):
    a = r.randint(10000, 999999)
    k = ch(r, [1, 10, 100, 1000, 10000])
    b = a + ch(r, [-1, 1]) * k * r.randint(1, 9)
    if not 10000 <= b <= 999999 or a == b:
        raise AssertionError
    hi, lo = max(a, b), min(a, b)
    good = "%s &gt; %s" % (comma(hi), comma(lo))
    return mcq("Compare %s and %s. Which statement is true?" % (comma(a), comma(b)), good, ["%s &lt; %s" % (comma(hi), comma(lo)), "%s &gt; %s" % (comma(lo), comma(hi)), "%s = %s" % (comma(hi), comma(lo))],
               "Both have the same number of digits. Compare from the left until the digits differ: <b>%s</b>." % good)


def cmp_len(r):
    a = r.randint(10000, 99999)
    b = r.randint(100000, 199999)
    if int(str(a)[0]) <= int(str(b)[0]):
        a = int("9" + str(a)[1:])
    good = "%s &lt; %s" % (comma(a), comma(b))
    return mcq("Compare %s and %s. Which statement is true?" % (comma(b), comma(a)), good, ["%s &gt; %s" % (comma(a), comma(b)), "%s = %s" % (comma(a), comma(b)), "%s &lt; %s" % (comma(b), comma(a))],
               "%s has 5 digits and %s has 6 digits, so %s is smaller even though it starts with a bigger digit: <b>%s</b>." % (comma(a), comma(b), comma(a), good))


def ord_asc(r):
    base = r.randint(10, 98) * 10000
    xs = set()
    while len(xs) < 4:
        xs.add(base + r.randint(0, 9) * 1000 + r.randint(0, 999))
    xs = sorted(xs)
    if r.random() < 0.3:
        xs[0] = xs[0] // 10
    asc = sorted(xs)
    up = r.random() < 0.5
    good = asc if up else asc[::-1]
    show = list(xs)
    r.shuffle(show)
    sw = list(good)
    sw[1], sw[2] = sw[2], sw[1]
    sw2 = list(good)
    sw2[0], sw2[1] = sw2[1], sw2[0]
    return mcq("Arrange from %s: %s" % ("smallest to greatest" if up else "greatest to smallest", ", ".join(comma(x) for x in show)),
               ", ".join(comma(x) for x in good), [", ".join(comma(x) for x in good[::-1]), ", ".join(comma(x) for x in sw), ", ".join(comma(x) for x in sw2)],
               "Compare the digits from the left: <b>%s</b>." % ", ".join(comma(x) for x in good))


def ord_digits(r):
    ds = r.sample(range(0, 10), ch(r, [5, 6]))
    big = r.random() < 0.5
    s = sorted(ds, reverse=big)
    if not big and s[0] == 0:
        s[0], s[1] = s[1], s[0]
    ans = int("".join(map(str, s)))
    w1 = int("".join(map(str, sorted(ds, reverse=not big)))) if not (big and sorted(ds)[0] == 0) else int("".join(map(str, sorted(ds)[1:])))
    sw = list(s)
    sw[-1], sw[-2] = sw[-2], sw[-1]
    w2 = int("".join(map(str, sw)))
    w3 = int("".join(map(str, sorted(ds)))) if not big else ans - 9
    return mcq("Use each of the digits %s once. What is the %s number you can make?" % (", ".join(map(str, ds)), "greatest" if big else "smallest"), ans, [w1, w2, w3, ans + 9],
               "Put the %s digits in the highest places%s: <b>%s</b>." % ("biggest" if big else "smallest", "" if big else " (0 cannot be first)", comma(ans)))


def ord_town(r):
    towns = r.sample(PLACES, 4)
    base = r.randint(20, 90) * 10000
    pops = r.sample(range(base, base + 90000, 37), 4)
    most = r.random() < 0.5
    i = pops.index(max(pops) if most else min(pops))
    rows = "; ".join("%s: %s" % (t, comma(p)) for t, p in zip(towns, pops))
    return mcq("The number of people who came to four football matches was: %s. Which city had the %s people?" % (rows, "most" if most else "fewest"), towns[i],
               [t for t in towns if t != towns[i]], "Compare the numbers: <b>%s</b> (%s)." % (towns[i], comma(pops[i])))


# ============================================================ division by multiples of 10 and sharing
def div_tens(r):
    d = ch(r, [10, 20, 30, 40, 50])
    q = r.randint(3, 40)
    n = d * q
    if n > 999:
        raise AssertionError
    return mcq("Work out %s ÷ %d." % (comma(n), d), q, [q * 10, n // (d // 10) if d > 10 else q + 10, q + 1, q - 1],
               "%s ÷ %d = (%s ÷ 10) ÷ %d = %d ÷ %d = <b>%d</b>." % (comma(n), d, comma(n), d // 10, n // 10, d // 10, q))


def div_share(r):
    k = K(r)
    d = r.randint(3, 9)
    q = r.randint(12, 99)
    rem = ch(r, [0, 0, r.randint(1, d - 1)])
    n = d * q + rem
    thing = ch(r, ["oranges", "exercise books", "sweets", "pencils", "mangoes", "biscuits"])
    if rem:
        return mcq("%s shares %d %s equally among %d friends. How many does each friend get, and how many are left over?" % (k["n"], n, thing, d),
                   "%d each, %d left over" % (q, rem), ["%d each, %d left over" % (q + 1, rem), "%d each, %d left over" % (q, d - rem), "%d each, 0 left over" % q],
                   "%d ÷ %d = %d remainder %d: <b>%d each, %d left over</b>." % (n, d, q, rem, q, rem))
    return mcq("%s shares %d %s equally among %d friends. How many does each friend get?" % (k["n"], n, thing, d), q, [q + 1, q - 1, n - d, q * 10],
               "%d ÷ %d = <b>%d</b>." % (n, d, q))


# ============================================================ LCM and HCF
def lcm(a, b):
    return a * b // math.gcd(a, b)


def mult_list(r):
    n = r.randint(3, 12)
    good = ", ".join(str(n * i) for i in range(1, 6))
    return mcq("Which list shows the first five multiples of %d?" % n, good,
               [", ".join(str(n + i) for i in range(5)), ", ".join(str(n * i) for i in range(2, 7)), ", ".join(str(d) for d in range(1, n + 1) if n % d == 0) if len([d for d in range(1, n + 1) if n % d == 0]) > 2 else ", ".join(str(n * i + 1) for i in range(1, 6))],
               "Multiply %d by 1, 2, 3, 4 and 5: <b>%s</b>." % (n, good))


def common_mult(r):
    a, b = r.sample(range(2, 10), 2)
    L = lcm(a, b)
    if L > 60:
        raise AssertionError
    good = L * r.randint(1, 2)
    w = [a * b + a if (a * b + a) % b else a * b + 1, a + b, L + a if (L + a) % b else L + 1, L + b if (L + b) % a else L - 1]
    return mcq("Which number is a common multiple of %d and %d?" % (a, b), good, [x for x in w if x % a or x % b],
               "%d is in the list of multiples of %d and of %d: <b>%d</b>." % (good, a, b, good))


def lcm2(r):
    a, b = r.sample(range(2, 13), 2)
    L = lcm(a, b)
    return mcq("Find the LCM of %d and %d." % (a, b), L, [a * b if a * b != L else L * 2, math.gcd(a, b) if math.gcd(a, b) > 1 else a + b, max(a, b), L * 2],
               "Multiples of %d: %s, … Multiples of %d: %s, … The lowest one in both lists is <b>%d</b>." % (
                   a, ", ".join(str(a * i) for i in range(1, L // a + 1)), b, ", ".join(str(b * i) for i in range(1, L // b + 1)), L))


def lcm3(r):
    a, b, c = sorted(r.sample(range(2, 10), 3))
    L = lcm(lcm(a, b), c)
    if L > 120:
        raise AssertionError
    return mcq("Find the LCM of %d, %d and %d." % (a, b, c), L, [a * b * c if a * b * c != L else L * 2, lcm(a, b) if lcm(a, b) != L else L + c, lcm(b, c) if lcm(b, c) != L else L * 3, c],
               "List multiples of %d until you find one that %d and %d also divide: <b>%d</b>." % (c, a, b, L))


def lcm_word(r):
    a, b = r.sample(range(3, 16), 2)
    L = lcm(a, b)
    if L > 120 or L == a * b and r.random() < 0.3:
        raise AssertionError
    k = r.randint(0, 1)
    if k == 0:
        return mcq("Two school bells ring together at 8:00 a.m. One rings every %d minutes and the other every %d minutes. After how many minutes will they next ring together?" % (a, b),
                   "%d minutes" % L, ["%d minutes" % x for x in (a * b if a * b != L else L * 2, a + b, max(a, b), math.gcd(a, b) if math.gcd(a, b) > 1 else L + 1)],
                   "We need the lowest common multiple of %d and %d: <b>%d minutes</b>." % (a, b, L))
    return mcq("Biscuits come in packets of %d and drinks come in packs of %d. What is the smallest number of each you can buy so that you have the same number of biscuits and drinks?" % (a, b),
               L, [a * b if a * b != L else L * 2, a + b, max(a, b), L + a],
               "LCM of %d and %d = <b>%d</b>." % (a, b, L))


def factors(n):
    return [d for d in range(1, n + 1) if n % d == 0]


def common_fac(r):
    g = r.randint(2, 12)
    a, b = g * r.randint(2, 8), g * r.randint(2, 8)
    if a == b or a > 99 or b > 99:
        raise AssertionError
    cf = [d for d in factors(a) if b % d == 0]
    good = ", ".join(map(str, cf))
    w1 = ", ".join(map(str, factors(a)))
    w2 = ", ".join(map(str, cf[1:])) if len(cf) > 1 else "1, %d" % a
    w3 = ", ".join(map(str, sorted(set(factors(a)) | set(factors(b)))))
    return mcq("What are the common factors of %d and %d?" % (a, b), good, [w1, w2, w3, ", ".join(map(str, factors(b)))],
               "Factors of %d: %s. Factors of %d: %s. In both: <b>%s</b>." % (a, ", ".join(map(str, factors(a))), b, ", ".join(map(str, factors(b))), good))


def hcf2(r):
    g = r.randint(2, 15)
    p, q = r.sample(range(1, 9), 2)
    if math.gcd(p, q) != 1:
        raise AssertionError
    a, b = g * p, g * q
    if a > 99 or b > 99:
        raise AssertionError
    return mcq("Find the HCF of %d and %d." % (a, b), g, [lcm(a, b), min(a, b) if min(a, b) != g else g * 2, g // 2 if g % 2 == 0 and g > 2 else g + 1, 1 if g != 1 else 2],
               "The highest number that divides both %d and %d is <b>%d</b>." % (a, b, g))


def hcf_word(r):
    g = r.randint(3, 15)
    p, q = r.sample(range(2, 8), 2)
    if math.gcd(p, q) != 1 or g * max(p, q) > 99:
        raise AssertionError
    a, b = g * p, g * q
    k = K(r)
    return mcq("%s has %d red beads and %d blue beads. %s wants to make bags with the same number of red beads and the same number of blue beads in each bag, with none left over. What is the greatest number of bags %s can make?" % (k["n"], a, b, k["He"], k["he"]),
               g, [lcm(a, b), a + b, g * 2 if a % (g * 2) or b % (g * 2) else g + 1, p + q],
               "We need the highest common factor of %d and %d: <b>%d bags</b>." % (a, b, g))


# ============================================================ decimals
def dec_addsub(r):
    k = ch(r, [1, 2])
    a = F(r.randint(11, 999), 10 ** k)
    b = F(r.randint(11, 999), 10 ** ch(r, [1, 2]))
    add = r.random() < 0.55
    if not add and a < b:
        a, b = b, a
    ans = a + b if add else a - b
    if ans <= 0:
        raise AssertionError
    w = [ans + F(1, 10) if add else ans - F(1, 10), ans * 10, (a + b / 10) if add else a - b / 10, ans + F(1, 100)]
    return mcq("Work out %s %s %s." % (dec(a), "+" if add else "−", dec(b)), dec(ans), [dec(x) for x in w if x > 0],
               "Line up the decimal points and %s: <b>%s</b>." % ("add" if add else "subtract", dec(ans)))


def dec_word(r):
    k = K(r)
    a = F(r.randint(12, 95), 10)
    b = F(r.randint(12, 95), 10)
    t = ch(r, [("kg of rice", "kg"), ("metres of cloth", "m"), ("litres of palm oil", "litres")])
    ans = a + b
    return mcq("%s bought %s %s on Monday and %s %s on Friday. How much did %s buy altogether?" % (k["n"], dec(a), t[0], dec(b), t[0], k["he"]),
               "%s %s" % (dec(ans), t[1]), ["%s %s" % (dec(x), t[1]) for x in (ans + 1, abs(a - b), ans * 10, ans - F(1, 10))],
               "%s + %s = <b>%s %s</b>." % (dec(a), dec(b), dec(ans), t[1]))


def dec_mul1(r):
    a = F(r.randint(11, 999), ch(r, [10, 100]))
    m = r.randint(2, 9)
    ans = a * m
    return mcq("Work out %s × %d." % (dec(a), m), dec(ans), [dec(ans * 10), dec(ans / 10), dec(ans + a), dec(a + m)],
               "Multiply as whole numbers, then put back the same number of decimal places: <b>%s</b>." % dec(ans))


def dec_div1(r):
    m = r.randint(2, 9)
    q = F(r.randint(11, 499), ch(r, [10, 100]))
    a = q * m
    return mcq("Work out %s ÷ %d." % (dec(a), m), dec(q), [dec(q * 10), dec(q / 10), dec(q + F(1, 10)), dec(a - m) if a > m else dec(q * 2)],
               "Divide as usual and keep the decimal point in the same place: <b>%s</b>." % dec(q))


def dec_10(r):
    p = ch(r, [10, 100, 1000])
    a = F(r.randint(11, 9999), ch(r, [10, 100]))
    mul = r.random() < 0.5
    ans = a * p if mul else a / p
    z = {10: 1, 100: 2, 1000: 3}[p]
    try:
        w = [dec(a * p / 10) if mul else dec(a / p * 10), dec(a / p) if mul else dec(a * p), dec(a * p * 10) if mul else dec(a / p / 10), dec(a + p) if mul else dec(a)]
        ans_s = dec(ans)
    except AssertionError:
        raise
    return mcq("Work out %s %s %s." % (dec(a), "×" if mul else "÷", comma(p)), ans_s, w,
               "%s by %s moves each digit %d place%s to the %s: <b>%s</b>." % ("Multiplying" if mul else "Dividing", comma(p), z, "" if z == 1 else "s", "left" if mul else "right", ans_s))


def frac_dec(r):
    d = ch(r, [10, 100, 1000])
    n = r.randint(1, d - 1)
    if n % 10 == 0 and d > 10 and r.random() < 0.6:
        raise AssertionError
    x = F(n, d)
    k = {10: 1, 100: 2, 1000: 3}[d]
    good = dec(x, k).rstrip("0") if "." in dec(x, k) else dec(x, k)
    if good.endswith("."):
        good = good[:-1]
    w = ["0." + str(n), str(n) + "." + str(d)[1:] if False else dec(F(n, d * 10)), dec(F(n, max(10, d // 10))) if F(n, max(10, d // 10)) < 1 else "1." + str(n), str(n)]
    return mcq("Write %s as a decimal." % fr(n, d), good, [x for x in w if x != good],
               "%s means %d %s: <b>%s</b>." % (fr(n, d), n, {10: "tenths", 100: "hundredths", 1000: "thousandths"}[d], good))


# ============================================================ squares and square roots
def sq_of(r):
    n = r.randint(2, 20)
    return mcq(ch(r, ["What is the square of %d (%d × %d)?", "Work out %d² (%d × %d)."]) % (n, n, n), n * n, [2 * n, n * n + n, (n + 1) ** 2, n + n * 10],
               "%d × %d = <b>%d</b>. Do not double: %d × 2 = %d." % (n, n, n * n, n, 2 * n))


def sq_perfect(r):
    n = r.randint(4, 20)
    good = n * n
    w = set()
    while len(w) < 3:
        x = good + ch(r, [-3, -2, -1, 1, 2, 3, 5, 7, 10, -10])
        if x > 1 and math.isqrt(x) ** 2 != x:
            w.add(x)
    opts = sorted(w | {good})
    return mcq("Which of these numbers is a perfect square: %s?" % ", ".join(map(str, opts)), good, sorted(w), "%d = %d × %d, so <b>%d</b> is a perfect square." % (good, n, n, good))


def sq_root(r):
    n = r.randint(2, 20)
    return mcq(ch(r, ["What is the square root of %d (√%d)?", "Which number multiplied by itself gives %d? (Find √%d.)"]) % (n * n, n * n), n, [n * n // 2, n + 1, n - 1, n * 2],
               "%d × %d = %d, so √%d = <b>%d</b>." % (n, n, n * n, n * n, n))


def sq_word(r):
    n = r.randint(3, 20)
    k = r.randint(0, 2)
    if k == 0:
        return mcq("A square garden has sides of %d m. What is its area?" % n, "%d m²" % (n * n), ["%d m²" % x for x in (4 * n, 2 * n, n * n + n, (n + 1) ** 2)],
                   "Area of a square = side × side = %d × %d = <b>%d m²</b>." % (n, n, n * n))
    if k == 1:
        return mcq("A square floor has an area of %d m². How long is one side?" % (n * n), "%d m" % n, ["%d m" % x for x in (n * n // 4 if n * n % 4 == 0 else n + 2, n + 1, n * 2, n - 1)],
                   "√%d = %d: <b>%d m</b>." % (n * n, n, n))
    return mcq("Chairs are arranged in a square with %d rows and %d chairs in each row. How many chairs are there?" % (n, n), n * n, [2 * n, n * n - n, (n + 1) ** 2, n * 4],
               "%d × %d = <b>%d chairs</b>." % (n, n, n * n))


def sq_sum(r):
    a, b = r.sample(range(2, 13), 2)
    op = r.random() < 0.6
    ans = a * a + b * b if op else abs(a * a - b * b)
    return mcq("Work out %d² %s %d²." % (max(a, b) if not op else a, "+" if op else "−", min(a, b) if not op else b), ans,
               [(a + b) ** 2 if op else abs(a - b) ** 2, 2 * a + 2 * b if op else abs(2 * a - 2 * b), ans + 1, a * b * 2],
               "%d² = %d and %d² = %d, so the answer is <b>%d</b>." % (a, a * a, b, b * b, ans))


# ============================================================ money: naira and kobo
def mo_convert(r):
    k = r.randint(0, 2)
    if k == 0:
        n, kb = r.randint(1, 99), ch(r, [25, 50, 75, 10, 20, 5])
        return mcq("How many kobo are in %s?" % naira(n + F(kb, 100)), "%s kobo" % comma(n * 100 + kb),
                   ["%s kobo" % comma(x) for x in (n * 10 + kb, n * 1000 + kb, n + kb, n * 100 + kb * 10)],
                   "₦1 = 100 kobo, so ₦%d = %s kobo. Add %d kobo: <b>%s kobo</b>." % (n, comma(n * 100), kb, comma(n * 100 + kb)))
    if k == 1:
        t = r.randint(105, 9995)
        if t % 100 == 0 or t % 5:
            raise AssertionError
        return mcq("Change %s kobo to naira and kobo." % comma(t), naira(F(t, 100)), [naira(F(t, 10)), naira(t), naira(F(t, 1000)) if t >= 1000 else naira(F(t, 100) + 1)],
                   "Divide by 100: <b>%s</b> (%d naira and %d kobo)." % (naira(F(t, 100)), t // 100, t % 100))
    n = r.randint(2, 40)
    return mcq("How many 50 kobo coins make %s?" % naira(n), n * 2, [n * 50, n, n * 5, n * 20],
               "₦1 = two 50 kobo coins, so ₦%d = <b>%d coins</b>." % (n, 2 * n))


def mo_addsub(r):
    a = F(r.randint(200, 9999) * 5, 100) if r.random() < 0.6 else r.randint(50, 9999)
    b = F(r.randint(200, 9999) * 5, 100) if r.random() < 0.6 else r.randint(50, 9999)
    add = r.random() < 0.5
    if not add and a < b:
        a, b = b, a
    ans = a + b if add else a - b
    if ans <= 0:
        raise AssertionError
    return mcq("Work out %s %s %s." % (naira(a), "+" if add else "−", naira(b)), naira(ans), [naira(ans + 1), naira(ans - F(1, 2)) if ans > 1 else naira(ans + 10), naira(ans + 100), naira(a - b if add else a + b) if a != b else naira(ans * 2)],
               "Line up naira with naira and kobo with kobo: <b>%s</b>." % naira(ans))


def mo_change(r):
    k = K(r)
    items = [("a loaf of bread", 900, 1600), ("a bottle of groundnut oil", 2500, 4500), ("a tin of milk", 500, 1200), ("an exercise book", 250, 600),
             ("a pair of slippers", 1500, 3500), ("a bag of garri (small)", 1200, 2800), ("a pen", 150, 400), ("a meat pie", 600, 1500)]
    a, b = r.sample(items, 2)
    pa = r.randint(a[1] // 50, a[2] // 50) * 50
    pb = r.randint(b[1] // 50, b[2] // 50) * 50
    note = ch(r, [5000, 10000])
    if pa + pb >= note:
        raise AssertionError
    ch_ = note - pa - pb
    return mcq("%s buys %s for %s and %s for %s. %s pays with a %s note. How much change does %s get?" % (k["n"], a[0], naira(pa), b[0], naira(pb), k["He"], naira(note), k["he"]),
               naira(ch_), [naira(pa + pb), naira(note - pa), naira(ch_ + 100), naira(ch_ - 50) if ch_ > 50 else naira(ch_ + 50)],
               "Cost: %s + %s = %s. Change: %s − %s = <b>%s</b>." % (naira(pa), naira(pb), naira(pa + pb), naira(note), naira(pa + pb), naira(ch_)))


def mo_profit(r):
    k = K(r)
    cp = r.randint(20, 300) * 50
    d = r.randint(2, 40) * 50
    gain = r.random() < 0.55
    sp = cp + d if gain else cp - d
    if sp <= 0:
        raise AssertionError
    thing = ch(r, ["a bicycle", "a radio", "a bag of rice", "a sewing machine", "a goat", "a school bag", "a fan"])
    q = r.randint(0, 1)
    if q == 0:
        good = "%s of %s" % ("profit" if gain else "loss", naira(d))
        return mcq("%s bought %s for %s and sold it for %s. Did %s make a profit or a loss, and how much?" % (k["n"], thing, naira(cp), naira(sp), k["he"]),
                   good, ["%s of %s" % ("loss" if gain else "profit", naira(d)), "%s of %s" % ("profit" if gain else "loss", naira(cp + sp)), "%s of %s" % ("profit" if gain else "loss", naira(d + 100))],
                   "Selling price %s cost price, so it is a %s: %s − %s = <b>%s</b>." % ("&gt;" if gain else "&lt;", "profit" if gain else "loss", naira(max(cp, sp)), naira(min(cp, sp)), naira(d)))
    return mcq("A trader bought %s for %s and wants a profit of %s. At what price should she sell it?" % (thing, naira(cp), naira(d)), naira(cp + d),
               [naira(cp - d) if cp > d else naira(cp + 2 * d), naira(d), naira(cp + d + 100), naira(cp)],
               "Selling price = cost price + profit = %s + %s = <b>%s</b>." % (naira(cp), naira(d), naira(cp + d)))


def mo_muldiv(r):
    k = K(r)
    mul = r.random() < 0.5
    if mul:
        p = F(r.randint(10, 600) * 25, 100) if r.random() < 0.4 else r.randint(5, 250) * 10
        n = r.randint(2, 9)
        thing = ch(r, ["oranges", "pencils", "exercise books", "packets of biscuits", "bottles of water", "tins of tomato paste"])
        return mcq("One of these %s costs %s. How much do %d cost?" % (thing, naira(p), n), naira(p * n), [naira(p * n + p), naira(p + n), naira(p * n * 10), naira(p * (n - 1))],
                   "%s × %d = <b>%s</b>." % (naira(p), n, naira(p * n)))
    n = r.randint(2, 9)
    each = r.randint(10, 999) * 10
    tot = each * n
    return mcq("%s shares %s equally among %d children. How much does each child get?" % (k["n"], naira(tot), n), naira(each),
               [naira(each * 10), naira(tot - n), naira(each + 100), naira(each // 10) if each % 100 == 0 else naira(each - 10)],
               "%s ÷ %d = <b>%s</b>." % (naira(tot), n, naira(each)))


def mo_online(r):
    k = K(r)
    price = r.randint(30, 400) * 100
    deliv = ch(r, [1000, 1500, 2000, 2500])
    n = r.randint(1, 3)
    tot = price * n + deliv
    return mcq("%s orders %d %s online. Each costs %s and delivery costs %s for the whole order. What is the total cost?" % (k["n"], n, "pair of shoes" if n == 1 else "pairs of shoes", naira(price), naira(deliv)),
               naira(tot), [naira(price * n), naira((price + deliv) * n) if n > 1 else naira(tot + deliv), naira(price + deliv * n) if n > 1 else naira(tot - 100), naira(tot + 1000)],
               "%d × %s = %s, plus delivery %s: <b>%s</b>." % (n, naira(price), naira(price * n), naira(deliv), naira(tot)))


# ============================================================ open sentences
def os_box(r):
    op = ch(r, "+−×÷")
    if op == "+":
        a, x = r.randint(100, 9999), r.randint(100, 9999)
        q, ans, w = "%s + □ = %s" % (comma(a), comma(a + x)), x, [a + x + a, x + 10, x - 1, a]
    elif op == "−":
        a, x = r.randint(1000, 9999), r.randint(100, 999)
        if r.random() < 0.5:
            q, ans, w = "%s − □ = %s" % (comma(a), comma(a - x)), x, [a + (a - x), x + 100, x - 10, a - x]
        else:
            q, ans, w = "□ − %s = %s" % (comma(x), comma(a - x)), a, [a - 2 * x, a + 100, a - 1, x]
    elif op == "×":
        a, x = r.randint(2, 12), r.randint(3, 50)
        q, ans, w = "%d × □ = %d" % (a, a * x), x, [a * x - a, x + 1, a * x + a, x * 10]
    else:
        a, x = r.randint(2, 12), r.randint(3, 40)
        if r.random() < 0.5:
            q, ans, w = "□ ÷ %d = %d" % (a, x), a * x, [x - a if x > a else x + a, x + a, a * x + a, x]
        else:
            q, ans, w = "%d ÷ □ = %d" % (a * x, x), a, [a * x * x, a + 1, a * x - x, x]
    return mcq("Find the missing number: %s" % q, ans, w, "Use the inverse operation to find the number in the box: <b>%s</b>." % comma(ans))


def os_write(r):
    k = K(r)
    a, b = r.randint(5, 90), r.randint(5, 90)
    t = r.randint(0, 3)
    if t == 0:
        q = "%s had some oranges. %s bought %d more and now has %d. Which number sentence finds how many %s had at first?" % (k["n"], k["He"], a, a + b, k["he"])
        good, w = "□ + %d = %d" % (a, a + b), ["□ − %d = %d" % (a, a + b), "%d + %d = □" % (a, a + b), "□ × %d = %d" % (a, a + b)]
    elif t == 1:
        n = r.randint(3, 9)
        q = "%d children share some sweets equally. Each child gets %d. Which number sentence finds the number of sweets?" % (n, a)
        good, w = "□ ÷ %d = %d" % (n, a), ["□ × %d = %d" % (n, a), "%d ÷ %d = □" % (a, n), "□ − %d = %d" % (n, a)]
    elif t == 2:
        n = r.randint(3, 9)
        q = "A number multiplied by %d gives %d. Which number sentence shows this?" % (n, n * a)
        good, w = "□ × %d = %d" % (n, n * a), ["□ + %d = %d" % (n, n * a), "%d × %d = □" % (n, n * a), "□ ÷ %d = %d" % (n, n * a)]
    else:
        q = "%s spent ₦%d and has ₦%d left. Which number sentence finds how much money %s had?" % (k["n"], a * 10, b * 10, k["he"])
        good, w = "□ − %d = %d" % (a * 10, b * 10), ["□ + %d = %d" % (a * 10, b * 10), "%d − □ = %d" % (a * 10, b * 10), "%d − %d = □" % (a * 10, b * 10)]
    return mcq(q, good, w, "<b>%s</b> describes the story." % good)


def os_solve(r):
    k = K(r)
    n = r.randint(3, 9)
    x = r.randint(4, 30)
    c = r.randint(2, 30)
    t = r.randint(0, 1)
    if t == 0:
        return mcq("I think of a number, multiply it by %d and add %d. The answer is %d. What is my number?" % (n, c, n * x + c), x, [(n * x + c) // n, x + c, n * x, x + 1],
                   "Work backwards: %d − %d = %d, then %d ÷ %d = <b>%d</b>." % (n * x + c, c, n * x, n * x, n, x))
    return mcq("%s buys %d books at the same price and gets ₦%d change from ₦%d. How much does one book cost?" % (k["n"], n, c * 10, n * x * 10 + c * 10),
               naira(x * 10), [naira((n * x * 10 + c * 10) // n), naira(x * 10 + c * 10), naira(n * x * 10), naira(x * 10 + 10)],
               "Cost of the books: ₦%d − ₦%d = ₦%d. One book: ₦%d ÷ %d = <b>%s</b>." % (n * x * 10 + c * 10, c * 10, n * x * 10, n * x * 10, n, naira(x * 10)))


def os_true(r):
    a, b = r.randint(10, 99), r.randint(2, 9)
    good = "%d × %d = %d × %d" % (a, b, b, a)
    w = ["%d − %d = %d − %d" % (a, b, b, a), "%d ÷ %d = %d ÷ %d" % (a * b, b, b, a * b), "%d + %d = %d × %d" % (a, b, a, b)]
    if r.random() < 0.5:
        good = "%d + %d = %d + %d" % (a, b, b, a)
        w[2] = "%d × %d = %d + %d" % (a, b, b, a)
    return mcq("Which number sentence with %d and %d is always true?" % (a, b), good, w, "We can add or multiply in any order: <b>%s</b>." % good)


# ============================================================ length, weight and capacity
def km_m(v):
    km, m = divmod(v, 1000)
    return ("%d km" % km if km else "") + (" " if km and m else "") + ("%d m" % m if m else "")


def kg_g(v):
    kg, g = divmod(v, 1000)
    return ("%d kg" % kg if kg else "") + (" " if kg and g else "") + ("%d g" % g if g else "")


def l_cl(v):
    l, c = divmod(v, 100)
    return ("%d litre%s" % (l, "" if l == 1 else "s") if l else "") + (" " if l and c else "") + ("%d cl" % c if c else "")


def len_conv(r):
    k = r.randint(0, 2)
    if k == 0:
        km, m = r.randint(1, 15), r.randint(5, 995)
        return mcq("Change %s to metres." % km_m(km * 1000 + m), "%s m" % comma(km * 1000 + m), ["%s m" % comma(x) for x in (km * 100 + m, km * 1000 + m * 10 if m < 100 else km * 10000 + m, km + m, km * 1000)],
                   "1 km = 1,000 m, so %d km = %s m. Add %d m: <b>%s m</b>." % (km, comma(km * 1000), m, comma(km * 1000 + m)))
    if k == 1:
        v = r.randint(1005, 29995)
        return mcq("Change %s m to kilometres and metres." % comma(v), km_m(v), [km_m(v // 10) if v // 10 > 0 else "1 km", "%d km %d m" % (v // 100, v % 100) if v % 100 else "%d km" % (v // 100), km_m(v + 1000)],
                   "%s m = %d × 1,000 m + %d m = <b>%s</b>." % (comma(v), v // 1000, v % 1000, km_m(v)))
    m, cm = r.randint(1, 30), r.randint(1, 99)
    return mcq("Change %d m %d cm to centimetres." % (m, cm), "%s cm" % comma(m * 100 + cm), ["%s cm" % comma(x) for x in (m * 10 + cm, m * 1000 + cm, m + cm, m * 100)],
               "1 m = 100 cm: %d × 100 + %d = <b>%s cm</b>." % (m, cm, comma(m * 100 + cm)))


def len_addsub(r):
    a, b = r.randint(1050, 15900), r.randint(1050, 9900)
    add = r.random() < 0.5
    if not add and a < b:
        a, b = b, a
    ans = a + b if add else a - b
    return mcq("Work out %s %s %s." % (km_m(a), "+" if add else "−", km_m(b)), km_m(ans), [km_m(ans + 1000), km_m(ans - 100) if ans > 1100 else km_m(ans + 100), km_m(a - b if add else a + b)] + ["%d km %d m" % (ans // 1000, ans % 1000 + 1000)] if False else [km_m(ans + 1000), km_m(ans - 100) if ans > 1100 else km_m(ans + 100), km_m(abs(a - b) if add else a + b), km_m(ans + 10)],
               "Change to metres: %s m %s %s m = %s m = <b>%s</b>." % (comma(a), "+" if add else "−", comma(b), comma(ans), km_m(ans)))


def len_est(r):
    P = [("the length of a classroom", "about 8 m", ["about 8 cm", "about 8 km", "about 80 m"]), ("the distance from Lagos to Ibadan", "about 130 km", ["about 130 m", "about 13 m", "about 1,300 cm"]),
         ("the length of a pencil", "about 18 cm", ["about 18 m", "about 18 km", "about 180 m"]), ("the height of a door", "about 2 m", ["about 2 cm", "about 2 km", "about 20 m"]),
         ("the length of a football field", "about 100 m", ["about 100 cm", "about 100 km", "about 10 cm"]), ("the distance a car travels in one hour on a highway", "about 80 km", ["about 80 m", "about 80 cm", "about 8 m"]),
         ("the length of your exercise book", "about 25 cm", ["about 25 m", "about 25 km", "about 2 m"]), ("the height of a two-storey building", "about 7 m", ["about 7 cm", "about 7 km", "about 70 m"]),
         ("the length of a grain of rice", "about 6 mm", ["about 6 cm", "about 6 m", "about 60 cm"]), ("the width of your thumbnail", "about 1 cm", ["about 1 m", "about 1 km", "about 10 m"]),
         ("the height of a Primary 4 pupil", "about 130 cm", ["about 130 m", "about 13 cm", "about 130 mm"]), ("the length of a danfo bus", "about 5 m", ["about 5 cm", "about 50 m", "about 5 km"]),
         ("the length of a teacher's table", "about 120 cm", ["about 120 m", "about 12 cm", "about 12 km"]), ("the distance from Abuja to Kano", "about 400 km", ["about 400 m", "about 40 m", "about 4,000 cm"]),
         ("the length of a new piece of chalk", "about 8 cm", ["about 8 m", "about 80 cm", "about 8 mm"]), ("the height of a coconut tree", "about 20 m", ["about 20 cm", "about 2 km", "about 200 m"]),
         ("the thickness of a coin", "about 2 mm", ["about 2 cm", "about 2 m", "about 20 cm"]), ("the length of a school compound wall", "about 150 m", ["about 150 cm", "about 150 km", "about 15 cm"]),
         ("the length of a matchstick", "about 4 cm", ["about 4 m", "about 40 cm", "about 4 km"]), ("the width of a road with two lanes", "about 7 m", ["about 7 cm", "about 70 m", "about 7 km"]),
         ("a walk of about 15 minutes", "about 1 km", ["about 1 m", "about 1 cm", "about 100 km"]), ("the length of a mobile phone", "about 15 cm", ["about 15 m", "about 15 mm", "about 1 m"])]
    q, good, w = ch(r, P)
    return mcq("Which is the best estimate for %s?" % q, good, w, "<b>%s</b> is the sensible size." % good)


def len_word(r):
    k = K(r)
    a, b = r.randint(1100, 4900), r.randint(600, 3900)
    t = r.randint(0, 1)
    if t == 0:
        return mcq("%s walks %s to school and then %s to the market. How far does %s walk altogether?" % (k["n"], km_m(a), km_m(b), k["he"]), km_m(a + b),
                   [km_m(abs(a - b)) if a != b else "1 km", km_m(a + b + 1000), km_m(a + b - 100), "%d km %d m" % ((a + b) // 1000 + 1, (a + b) % 1000) if (a + b) % 1000 else km_m(a + b + 10)],
                   "%s m + %s m = %s m = <b>%s</b>." % (comma(a), comma(b), comma(a + b), km_m(a + b)))
    tot = r.randint(20, 60) * 100
    run = r.randint(5, tot // 100 - 5) * 100
    return mcq("A road is %s long. Workers have tarred %s. How much is left to tar?" % (km_m(tot), km_m(run)), km_m(tot - run), [km_m(tot + run), km_m(tot - run + 1000), km_m(run), km_m(tot - run - 100)],
               "%s m − %s m = <b>%s</b>." % (comma(tot), comma(run), km_m(tot - run)))


def wt_conv(r):
    k = r.randint(0, 1)
    if k == 0:
        kg, g = r.randint(1, 25), r.randint(5, 995)
        return mcq("Change %s to grams." % kg_g(kg * 1000 + g), "%s g" % comma(kg * 1000 + g), ["%s g" % comma(x) for x in (kg * 100 + g, kg + g, kg * 1000, kg * 10000 + g)],
                   "1 kg = 1,000 g: %d × 1,000 + %d = <b>%s g</b>." % (kg, g, comma(kg * 1000 + g)))
    v = r.randint(1005, 29995)
    return mcq("Change %s g to kilograms and grams." % comma(v), kg_g(v), [kg_g(v // 10) if v >= 1000 else "1 kg", "%d kg %d g" % (v // 100, v % 100) if v % 100 else "%d kg" % (v // 100), kg_g(v + 1000)],
               "%s g = %d kg and %d g: <b>%s</b>." % (comma(v), v // 1000, v % 1000, kg_g(v)))


def wt_addsub(r):
    a, b = r.randint(1100, 15900), r.randint(1050, 9900)
    add = r.random() < 0.5
    if not add and a < b:
        a, b = b, a
    ans = a + b if add else a - b
    return mcq("Work out %s %s %s." % (kg_g(a), "+" if add else "−", kg_g(b)), kg_g(ans), [kg_g(ans + 1000), kg_g(ans - 100) if ans > 1100 else kg_g(ans + 100), kg_g(abs(a - b) if add else a + b), kg_g(ans + 10)],
               "In grams: %s g %s %s g = %s g = <b>%s</b>." % (comma(a), "+" if add else "−", comma(b), comma(ans), kg_g(ans)))


def wt_muldiv(r):
    mul = r.random() < 0.5
    n = r.randint(2, 9)
    if mul:
        a = r.randint(1050, 9900) // 10 * 10
        thing = ch(r, ["bag of beans", "tuber of yam", "carton of tomatoes", "basket of oranges"])
        return mcq("One %s weighs %s. How much do %d of them weigh?" % (thing, kg_g(a), n), kg_g(a * n), [kg_g(a * n + a), kg_g(a + n * 1000), kg_g(a * n - 1000) if a * n > 2000 else kg_g(a * n + 10), kg_g(a * n * 10)],
                   "%s × %d = %s g = <b>%s</b>." % (comma(a), n, comma(a * n), kg_g(a * n)))
    each = r.randint(110, 2900)
    tot = each * n
    return mcq("%s of rice is shared equally into %d bags. How much rice is in each bag?" % (kg_g(tot), n), kg_g(each), [kg_g(each * 10), kg_g(each + 100), kg_g(tot - n * 100) if tot > n * 200 else kg_g(each + 1000), kg_g(each - 10)],
               "%s g ÷ %d = %s g = <b>%s</b>." % (comma(tot), n, comma(each), kg_g(each)))


def wt_est(r):
    P = [("a bag of cement", "about 50 kg", ["about 50 g", "about 5 g", "about 500 kg"]), ("an egg", "about 60 g", ["about 60 kg", "about 6 kg", "about 600 kg"]),
         ("a Primary 4 pupil", "about 30 kg", ["about 30 g", "about 300 kg", "about 3 g"]), ("a mango", "about 300 g", ["about 300 kg", "about 30 kg", "about 3 g"]),
         ("a tuber of yam", "about 2 kg", ["about 2 g", "about 200 kg", "about 20 g"]), ("a pencil", "about 5 g", ["about 5 kg", "about 50 kg", "about 500 kg"]),
         ("a cow", "about 400 kg", ["about 400 g", "about 4 kg", "about 40 g"]), ("a sachet of pure water", "about 500 g", ["about 500 kg", "about 5 kg", "about 5 g"]),
         ("a big bag of rice", "about 50 kg", ["about 50 g", "about 5 g", "about 5,000 kg"]), ("a loaf of bread", "about 500 g", ["about 500 kg", "about 5 kg", "about 5 g"]),
         ("a goat", "about 25 kg", ["about 25 g", "about 250 kg", "about 2 g"]), ("a car", "about 1,200 kg", ["about 1,200 g", "about 12 kg", "about 120 g"]),
         ("a tomato", "about 80 g", ["about 80 kg", "about 8 kg", "about 800 kg"]), ("an exercise book", "about 100 g", ["about 100 kg", "about 10 kg", "about 1 g"]),
         ("a watermelon", "about 4 kg", ["about 4 g", "about 400 kg", "about 40 g"]), ("a chicken", "about 2 kg", ["about 2 g", "about 200 kg", "about 20 g"]),
         ("a new baby", "about 3 kg", ["about 3 g", "about 300 kg", "about 30 g"]), ("a sheet of paper", "about 5 g", ["about 5 kg", "about 500 g", "about 50 kg"]),
         ("a schoolbag full of books", "about 5 kg", ["about 5 g", "about 500 kg", "about 50 g"]), ("an orange", "about 150 g", ["about 150 kg", "about 15 kg", "about 1 g"]),
         ("a crate of 30 eggs", "about 2 kg", ["about 2 g", "about 200 kg", "about 20 g"]), ("a plastic chair", "about 3 kg", ["about 3 g", "about 300 kg", "about 30 g"])]
    q, good, w = ch(r, P)
    return mcq("Which is the best estimate for the weight of %s?" % q, good, w, "<b>%s</b> is the sensible weight." % good)


def cap_conv(r):
    k = r.randint(0, 2)
    if k == 0:
        l, c = r.randint(1, 25), r.randint(5, 95)
        return mcq("Change %s to centilitres." % l_cl(l * 100 + c), "%s cl" % comma(l * 100 + c), ["%s cl" % comma(x) for x in (l * 10 + c, l * 1000 + c, l + c, l * 100)],
                   "1 litre = 100 cl: %d × 100 + %d = <b>%s cl</b>." % (l, c, comma(l * 100 + c)))
    if k == 1:
        v = r.randint(105, 2995)
        if v % 100 == 0:
            raise AssertionError
        return mcq("Change %s cl to litres and centilitres." % comma(v), l_cl(v), [l_cl(v // 10) if v >= 100 else "1 litre", "%d litres %d cl" % (v // 1000, v % 1000) if v >= 1000 and v % 1000 < 100 else l_cl(v + 100), l_cl(v + 10)],
                   "%s cl = %d litres and %d cl: <b>%s</b>." % (comma(v), v // 100, v % 100, l_cl(v)))
    l = r.randint(2, 20)
    return mcq("How many 50 cl bottles can be filled from %d litres of zobo?" % l, l * 2, [l * 50, l, l * 5, l * 20],
               "%d litres = %s cl, and %s ÷ 50 = <b>%d bottles</b>." % (l, comma(l * 100), comma(l * 100), l * 2))


def cap_addsub(r):
    a, b = r.randint(110, 2590), r.randint(105, 990)
    add = r.random() < 0.5
    if not add and a < b:
        a, b = b, a
    ans = a + b if add else a - b
    if ans % 100 == 0 or ans < 100:
        raise AssertionError
    return mcq("Work out %s %s %s." % (l_cl(a), "+" if add else "−", l_cl(b)), l_cl(ans), [l_cl(ans + 100), l_cl(ans - 10) if ans > 110 else l_cl(ans + 10), l_cl(abs(a - b) if add else a + b), l_cl(ans + 1)],
               "In centilitres: %s cl %s %s cl = %s cl = <b>%s</b>." % (comma(a), "+" if add else "−", comma(b), comma(ans), l_cl(ans)))


def cap_muldiv(r):
    n = r.randint(2, 9)
    mul = r.random() < 0.5
    if mul:
        a = r.randint(105, 990)
        if (a * n) % 100 == 0:
            raise AssertionError
        thing = ch(r, ["jerrycan of water", "bottle of palm oil", "keg of kerosene", "jug of zobo"])
        return mcq("One %s holds %s. How much do %d of them hold?" % (thing, l_cl(a), n), l_cl(a * n), [l_cl(a * n + a), l_cl(a + n * 100), l_cl(a * n + 10), l_cl(a * n - 100) if a * n > 200 else l_cl(a * n + 100)],
                   "%s cl × %d = %s cl = <b>%s</b>." % (comma(a), n, comma(a * n), l_cl(a * n)))
    each = r.randint(25, 450)
    tot = each * n
    return mcq("%s of groundnut oil is poured equally into %d bottles. How much is in each bottle?" % (l_cl(tot), n), l_cl(each), [l_cl(each * 10), l_cl(each + 10), l_cl(each + 100), l_cl(tot - n) if tot - n > 0 and (tot - n) != each else l_cl(each + 5)],
               "%s cl ÷ %d = <b>%s</b>." % (comma(tot), n, l_cl(each)))


def cap_est(r):
    P = [("a bucket", "about 10 litres", ["about 10 cl", "about 100 litres", "about 1 cl"]), ("a teaspoon", "about 1 cl", ["about 1 litre", "about 10 litres", "about 100 cl"]),
         ("a cup of tea", "about 25 cl", ["about 25 litres", "about 250 litres", "about 2 cl"]), ("a car's fuel tank", "about 50 litres", ["about 50 cl", "about 5 cl", "about 500 litres"]),
         ("a bottle of soft drink", "about 50 cl", ["about 50 litres", "about 5 litres", "about 500 litres"]), ("a drum of water", "about 200 litres", ["about 200 cl", "about 2 cl", "about 20 cl"]),
         ("a sachet of pure water", "about 50 cl", ["about 50 litres", "about 5 litres", "about 5 cl"]), ("a bathtub", "about 150 litres", ["about 150 cl", "about 15 cl", "about 1,500 litres"]),
         ("a jerrycan", "about 25 litres", ["about 25 cl", "about 250 litres", "about 2 cl"]), ("a glass of water", "about 20 cl", ["about 20 litres", "about 2 litres", "about 200 litres"]),
         ("a big pot of jollof rice", "about 10 litres", ["about 10 cl", "about 1 cl", "about 1,000 litres"]), ("an overhead water tank", "about 1,000 litres", ["about 1,000 cl", "about 10 litres", "about 10 cl"]),
         ("a kettle", "about 2 litres", ["about 2 cl", "about 200 litres", "about 20 litres"]), ("a tablespoon", "about 1.5 cl", ["about 15 litres", "about 1.5 litres", "about 150 cl"]),
         ("a family-size bottle of groundnut oil", "about 3 litres", ["about 3 cl", "about 300 litres", "about 30 litres"]), ("a small tin of milk", "about 17 cl", ["about 17 litres", "about 170 litres", "about 1 cl"]),
         ("a watering can", "about 8 litres", ["about 8 cl", "about 800 litres", "about 80 litres"]), ("a medicine spoon", "about 0.5 cl", ["about 5 litres", "about 0.5 litres", "about 50 cl"]),
         ("a basin for washing clothes", "about 20 litres", ["about 20 cl", "about 2 cl", "about 2,000 litres"]), ("a water bottle for school", "about 75 cl", ["about 75 litres", "about 7 litres", "about 750 litres"]),
         ("a large cooler for drinks", "about 40 litres", ["about 40 cl", "about 4 cl", "about 4,000 litres"]), ("a fish pond", "about 5,000 litres", ["about 5,000 cl", "about 50 litres", "about 5 cl"])]
    q, good, w = ch(r, P)
    return mcq("Which is the best estimate for how much %s holds?" % q, good, w, "<b>%s</b> is sensible." % good)


# ============================================================ time: calendar
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
DAYS_IN = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
WEEK = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


def cal_days(r):
    k = r.randint(0, 2)
    if k == 0:
        m = r.randrange(12)
        return mcq("How many days are there in %s (not a leap year)?" % MONTHS[m], DAYS_IN[m], [x for x in (28, 29, 30, 31, 32) if x != DAYS_IN[m]],
                   "Thirty days have September, April, June and November; February has 28 (29 in a leap year); the rest have 31: <b>%d</b>." % DAYS_IN[m])
    if k == 1:
        w = r.randint(2, 15)
        return mcq("How many days are there in %d weeks?" % w, 7 * w, [7 * w + 7, 5 * w, 10 * w, w + 7], "1 week = 7 days: %d × 7 = <b>%d days</b>." % (w, 7 * w))
    y = r.randint(2, 9)
    return mcq("How many months are there in %d years?" % y, 12 * y, [10 * y, 12 * y + 12, 52 * y, 365 * y], "1 year = 12 months: %d × 12 = <b>%d months</b>." % (y, 12 * y))


def cal_after(r):
    d = r.randrange(7)
    n = r.randint(2, 30)
    good = WEEK[(d + n) % 7]
    return mcq("Today is %s. What day of the week will it be in %d days?" % (WEEK[d], n), good,
               [WEEK[(d + n + 1) % 7], WEEK[(d + n - 1) % 7], WEEK[(d + n % 7 + 2) % 7], WEEK[d] if WEEK[d] != good else WEEK[(d + 3) % 7]],
               "%d days = %d weeks and %d day%s. Count on %d day%s from %s: <b>%s</b>." % (n, n // 7, n % 7, "" if n % 7 == 1 else "s", n % 7, "" if n % 7 == 1 else "s", WEEK[d], good))


def cal_span(r):
    m = r.randrange(11)
    a = r.randint(1, DAYS_IN[m] - 5)
    b = r.randint(1, 25)
    days = DAYS_IN[m] - a + b
    return mcq("A holiday starts on %d %s and ends on %d %s. How many days is that, counting both the first and the last day?" % (a, MONTHS[m], b, MONTHS[m + 1]), days + 1,
               [days, days + 2, b - a if b > a else days - 1, 30 - a + b + 1 if DAYS_IN[m] != 30 else days + 3],
               "%s has %d days: %d − %d = %d days left in %s, plus %d days in %s, plus the first day: <b>%d days</b>." % (MONTHS[m], DAYS_IN[m], DAYS_IN[m], a, DAYS_IN[m] - a, MONTHS[m], b, MONTHS[m + 1], days + 1))


# ============================================================ cardinal points, lines and 2D/3D
DIRS = ["North", "North-East", "East", "South-East", "South", "South-West", "West", "North-West"]


def compass_svg():
    b = "<circle cx='90' cy='90' r='62' fill='%s' stroke='%s' stroke-width='2'/>" % (FILL, GREEN)
    b += "<path d='M90 20 L98 90 L90 160 L82 90 Z' fill='#fff' stroke='%s' stroke-width='1.5'/>" % INK
    b += "<path d='M20 90 L90 82 L160 90 L90 98 Z' fill='#fff' stroke='%s' stroke-width='1.5'/>" % INK
    b += "<path d='M90 20 L98 90 L82 90 Z' fill='%s'/>" % RED
    b += text(90, 14, "N", 16) + text(90, 178, "S", 16) + text(172, 95, "E", 16) + text(8, 95, "W", 16)
    return svg_wrap(180, 184, b, "compass showing North, East, South and West")


def cp_turn(r):
    d = r.randrange(8)
    t = ch(r, [(2, "a quarter turn clockwise"), (-2, "a quarter turn anticlockwise"), (4, "a half turn"), (6, "a three-quarter turn clockwise"), (1, "an eighth of a turn clockwise")])
    good = DIRS[(d + t[0]) % 8]
    k = K(r)
    return mcq("%s is facing %s. %s makes %s. Which direction is %s facing now?" % (k["n"], DIRS[d], k["He"], t[1], k["he"]) + fig(compass_svg()), good,
               [DIRS[(d - t[0]) % 8], DIRS[(d + t[0] + 1) % 8], DIRS[(d + t[0] - 1) % 8], DIRS[d]],
               "Turn clockwise N → E → S → W. %s from %s gives <b>%s</b>." % (t[1][0].upper() + t[1][1:], DIRS[d], good))


def cp_opposite(r):
    d = r.randrange(8)
    good = DIRS[(d + 4) % 8]
    return mcq("Which direction is opposite to %s?" % DIRS[d] + fig(compass_svg()), good, [DIRS[(d + 2) % 8], DIRS[(d + 6) % 8], DIRS[(d + 3) % 8]],
               "Opposite directions are a half turn apart: <b>%s</b>." % good)


def cp_map(r):
    places = r.sample(["school", "market", "church", "mosque", "clinic", "park", "post office", "bank", "petrol station"], 5)
    ds = r.sample(range(8), 4)
    cell = {0: (1, 0), 1: (2, 0), 2: (2, 1), 3: (2, 2), 4: (1, 2), 5: (0, 2), 6: (0, 1), 7: (0, 0)}
    b = "<line x1='40' y1='100' x2='290' y2='100' stroke='#ccc' stroke-dasharray='4 4'/><line x1='165' y1='14' x2='165' y2='186' stroke='#ccc' stroke-dasharray='4 4'/>"
    for i, dd in enumerate(ds):
        cx, cy = cell[dd]
        x, y = 55 + cx * 110, 36 + cy * 64
        b += "<rect x='%d' y='%d' width='100' height='26' rx='4' fill='#fff' stroke='%s'/>" % (x - 50, y - 13, GREEN) + text(x, y + 5, places[i + 1], 13)
    b += "<rect x='115' y='87' width='100' height='26' rx='4' fill='%s' stroke='%s'/>" % (FILL, RED) + text(165, 105, places[0], 13, col=RED)
    b += text(344, 20, "N", 14) + "<path d='M344 26 L344 50 M338 32 L344 26 L350 32' stroke='%s' stroke-width='2' fill='none'/>" % INK
    svg = svg_wrap(360, 200, b, "map with places around the %s" % places[0])
    i = r.randrange(4)
    good = DIRS[ds[i]]
    return mcq("On the map, in which direction is the %s from the %s?" % (places[i + 1], places[0]) + fig(svg), good,
               [DIRS[(ds[i] + 4) % 8], DIRS[(ds[i] + 2) % 8], DIRS[(ds[i] + 6) % 8]], "North is up. The %s is to the <b>%s</b> of the %s." % (places[i + 1], good, places[0]))


def line_svg(kind):
    if kind == "horizontal":
        b = "<line x1='20' y1='40' x2='140' y2='40' stroke='%s' stroke-width='4'/>" % BLUE
    elif kind == "vertical":
        b = "<line x1='80' y1='6' x2='80' y2='74' stroke='%s' stroke-width='4'/>" % BLUE
    elif kind == "slanting":
        b = "<line x1='30' y1='70' x2='130' y2='10' stroke='%s' stroke-width='4'/>" % BLUE
    else:
        b = "<path d='M20 60 Q60 0 100 40 T150 30' fill='none' stroke='%s' stroke-width='4'/>" % BLUE
    return svg_wrap(160, 80, b, "%s line" % kind)


def hv_line(r):
    kind = ch(r, ["horizontal", "vertical", "slanting", "curved"])
    n = r.randint(1, 9)
    return mcq("What kind of line is this? (Line %d)" % n + fig(line_svg(kind)), kind.capitalize(), [x.capitalize() for x in ("horizontal", "vertical", "slanting", "curved") if x != kind],
               "A horizontal line goes straight across like the horizon; a vertical line goes straight up and down: <b>%s</b>." % kind)


def hv_real(r):
    P = [("the edge of a table top", "Horizontal"), ("a flagpole", "Vertical"), ("the floor of a room", "Horizontal"), ("an electric pole", "Vertical"),
         ("the surface of still water in a bucket", "Horizontal"), ("a wall of a house", "Vertical"), ("a ladder leaning on a wall", "Slanting"), ("the roof of a house", "Slanting"),
         ("a plumb line (a string with a weight)", "Vertical"), ("the line where the sky meets the sea", "Horizontal"), ("a tall palm tree on a still day", "Vertical"),
         ("a slide in a playground", "Slanting"), ("the top edge of a blackboard", "Horizontal"), ("the side edge of a door", "Vertical"), ("a road going up a hill", "Slanting"),
         ("a bed lying on the floor", "Horizontal"), ("a ramp into a building", "Slanting"), ("the goalpost of a football field", "Vertical")]
    q, good = ch(r, P)
    return mcq("Is %s horizontal, vertical or slanting?" % q, good, [x for x in ("Horizontal", "Vertical", "Slanting", "Curved") if x != good], "<b>%s</b>." % good)


def dim23(r):
    P = [("a cube", "3D"), ("a square", "2D"), ("a cylinder", "3D"), ("a circle", "2D"), ("a cone", "3D"), ("a triangle", "2D"), ("a sphere", "3D"), ("a rectangle", "2D"),
         ("a cuboid", "3D"), ("a pentagon", "2D"), ("a pyramid", "3D"), ("a hexagon", "2D")]
    q, good = ch(r, P)
    n = r.randint(1, 9)
    return mcq("Is %s a 2D shape or a 3D shape? (Shape %d)" % (q, n), "%s shape" % good, ["%s shape" % ("2D" if good == "3D" else "3D"), "Both 2D and 3D", "Neither"],
               "2D shapes are flat (length and width). 3D shapes are solid (length, width and height): <b>%s</b>." % good)


def obj3d(r):
    P = [("a tin of tomato paste", "cylinder"), ("a football", "sphere"), ("a box of matches", "cuboid"), ("a dice", "cube"), ("an ice cream cone", "cone"),
         ("a brick", "cuboid"), ("an orange", "sphere"), ("a drum", "cylinder"), ("a sugar cube", "cube"), ("a party hat", "cone"), ("a carton of milk", "cuboid"), ("a gas cylinder", "cylinder"),
         ("a water tank on a roof", "cylinder"), ("a marble", "sphere"), ("a shoe box", "cuboid"), ("a Rubik's cube", "cube"), ("a funnel turned upside down", "cone"),
         ("a candle", "cylinder"), ("a tennis ball", "sphere"), ("a textbook", "cuboid"), ("a building block shaped like a box with equal sides", "cube"), ("a traffic cone", "cone")]
    q, good = ch(r, P)
    tpl = ch(r, ["Which 3D shape does %s look like?", "%s is shaped like which 3D shape?"])
    return mcq(tpl % (q if tpl.startswith("W") else q[0].upper() + q[1:]), good.capitalize(), [x.capitalize() for x in ("cube", "cuboid", "cylinder", "sphere", "cone") if x != good][:3] if good != "cube" else ["Cuboid", "Cylinder", "Sphere"],
               "<b>%s</b>." % good.capitalize())


def fev(r):
    S = [("cube", 6, 12, 8), ("cuboid", 6, 12, 8), ("square-based pyramid", 5, 8, 5), ("triangular prism", 5, 9, 6), ("cylinder", 3, 2, 0), ("cone", 2, 1, 1), ("tetrahedron (triangular-based pyramid)", 4, 6, 4)]
    s = ch(r, S)
    what = ch(r, [("faces", 1), ("edges", 2), ("vertices (corners)", 3)])
    good = s[what[1]]
    return mcq("How many %s does a %s have?" % (what[0], s[0]), good, [x for x in (s[1], s[2], s[3], good + 1, good + 2, max(0, good - 1)) if x != good],
               "A %s has %d faces, %d edges and %d vertices: <b>%d</b>." % (s[0], s[1], s[2], s[3], good), allow_zero=True)


# ============================================================ statistics: mode
def mode_list(r):
    vals = [r.randint(1, 12) for _ in range(r.randint(7, 11))]
    from collections import Counter
    c = Counter(vals)
    top = c.most_common()
    if len(top) > 1 and top[0][1] == top[1][1]:
        raise AssertionError
    m = top[0][0]
    w = [max(vals), round(sum(vals) / len(vals)), sorted(vals)[len(vals) // 2], top[1][1] if len(top) > 1 else m + 1, top[0][1]]
    return mcq("What is the mode of these scores: %s?" % ", ".join(map(str, vals)), m, [x for x in w if x != m],
               "The mode is the number that appears most often. %d appears %d times: <b>%d</b>." % (m, top[0][1], m))


def mode_table(r):
    things = r.sample(["rice", "beans", "yam", "plantain", "jollof rice", "eba", "moi moi", "akara"], 4)
    vals = r.sample(range(3, 15), 4)
    m = things[vals.index(max(vals))]
    rows = "".join("<tr><td>%s</td><td>%d</td></tr>" % (t, v) for t, v in zip(things, vals))
    tab = "<table class='sn-table'><tr><th>Favourite food</th><th>Number of pupils</th></tr>%s</table>" % rows
    return mcq("The table shows the favourite foods of a Primary 4 class. What is the mode?" + tab, m.capitalize(), [t.capitalize() for t in things if t != m],
               "The mode is the food chosen most often: <b>%s</b> (%d pupils)." % (m, max(vals)))


def chance_word(r):
    P = [("The sun will rise in the east tomorrow.", "Certain"), ("It will rain somewhere in Nigeria during the rainy season.", "Certain"), ("A goat will fly to school.", "Impossible"),
         ("You will pick a red ball from a bag of only blue balls.", "Impossible"), ("A tossed coin will land on heads.", "Equally likely"), ("You will roll a 7 on a normal dice.", "Impossible"),
         ("You will roll an even number on a dice.", "Equally likely"), ("It will rain in Kano in July.", "Likely"), ("You will pick a red ball from a bag with 9 red balls and 1 blue ball.", "Likely"),
         ("You will pick a blue ball from a bag with 9 red balls and 1 blue ball.", "Unlikely"), ("A baby will be born somewhere in Nigeria today.", "Certain")]
    q, good = ch(r, P)
    return mcq("How likely is this? %s" % q, good, [x for x in ("Impossible", "Unlikely", "Equally likely", "Likely", "Certain") if x != good][:3] if good not in ("Likely",) else ["Impossible", "Unlikely", "Certain"],
               "<b>%s</b>." % good)


# ============================================================ Roman numerals (writing up to M)
ROM = [(1000, "M"), (900, "CM"), (500, "D"), (400, "CD"), (100, "C"), (90, "XC"), (50, "L"), (40, "XL"), (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")]


def roman(n):
    out = ""
    for v, s in ROM:
        while n >= v:
            out += s
            n -= v
    return out


def rm_write(r):
    n = ch(r, [r.randint(1, 49), r.randint(40, 199), r.randint(200, 999), r.randint(400, 1000)])
    good = roman(n)
    w = set()
    # common mistakes: IIII-style, wrong subtraction, reversed pair
    s1 = good.replace("IV", "IIII").replace("XL", "XXXX").replace("CD", "CCCC").replace("IX", "VIIII").replace("XC", "LXXXX").replace("CM", "DCCCC")
    s2 = good.replace("IX", "XI", 1) if "IX" in good else good.replace("IV", "VI", 1) if "IV" in good else good.replace("XC", "CX", 1) if "XC" in good else good + "I"
    s3 = roman(n + 10) if n + 10 <= 1000 else roman(n - 10)
    s4 = roman(n - 1) if n > 1 else "II"
    return mcq("Write the number %d as a Roman numeral." % n, good, [x for x in (s1, s2, s3, s4) if x != good],
               "Split %d into %s: <b>%s</b>." % (n, " + ".join(str(v) for v in parts(n)), good))


def parts(n):
    out = []
    for p in (1000, 100, 10, 1):
        d = n // p % 10 * p if p < 1000 else n // 1000 * 1000
        if d:
            out.append(d)
    return out
