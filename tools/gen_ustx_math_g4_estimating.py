# -*- coding: utf-8 -*-
"""
Texas Grade 4 Math: Estimating with Rounding and Compatible Numbers (TEKS 4.4G)
  python3 tools/gen_ustx_math_g4_estimating.py
Estimating sums, differences, products and quotients by rounding to the nearest 10, 100 or 1,000 or with
compatible numbers, checking answers, and word problems.
Wrong answers come from real mistakes: rounding to the wrong place, finding the exact answer instead of an
estimate, and choosing numbers that do not divide easily.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)

tx_common.GRADE = "grade-4"

def rnd_to(n, p):
    return (n + p // 2) // p * p


def one_sum(r):
    p = r.choice([10, 100, 1000])
    a, b = r.randint(p * 2, p * 90 if p < 1000 else 9999), r.randint(p * 2, p * 60 if p < 1000 else 8999)
    op = r.choice(["+", "−"])
    if op == "−" and a < b:
        a, b = b, a
    ra, rb = rnd_to(a, p), rnd_to(b, p)
    if ra == a or rb == b or (op == "−" and ra <= rb):
        return None
    est = ra + rb if op == "+" else ra - rb
    exact = a + b if op == "+" else a - b
    name = {10: "ten", 100: "hundred", 1000: "thousand"}[p]
    return mcq("Round each number to the nearest %s to estimate %s %s %s." % (name, comma(a), op, comma(b)), comma(est), [comma(exact), comma(est + p), comma(est - p) if est > p else comma(est + 2 * p)],
               "%s ≈ %s and %s ≈ %s. %s %s %s = <b>%s</b>." % (comma(a), comma(ra), comma(b), comma(rb), comma(ra), op, comma(rb), comma(est)))


def one_prod(r):
    a = r.randint(2, 9)
    n = r.randint(110, 980) if r.random() < 0.5 else r.randint(11, 98)
    p = 100 if n >= 100 else 10
    rn = rnd_to(n, p)
    if rn == n:
        return None
    return mcq("Estimate %d × %s by rounding %s to the nearest %s." % (a, comma(n), comma(n), "hundred" if p == 100 else "ten"), comma(a * rn), [comma(a * n), comma(a * rn + p), comma(a + rn), comma(a * rn * 10)],
               "%s ≈ %s. %d × %s = <b>%s</b>." % (comma(n), comma(rn), a, comma(rn), comma(a * rn)))


def one_quot(r):
    d = r.randint(3, 9)
    q = r.randint(12, 90)
    c = d * q * (10 if r.random() < 0.5 else 1)
    n = c + r.randint(-d + 1, d - 1)
    if n == c or n < 100:
        return None
    wrong = [c // d + d, rnd_to(n, 100) // d if rnd_to(n, 100) % d == 0 and rnd_to(n, 100) // d != c // d else c // d * 10, c // d // 10 if c // d >= 100 else c // d + 10]
    return mcq("Use compatible numbers to estimate %s ÷ %d." % (comma(n), d), comma(c // d), [comma(w) for w in wrong],
               "%s is close to %s, which divides easily by %d: %s ÷ %d = <b>%s</b>." % (comma(n), comma(c), d, comma(c), d, comma(c // d)))


def one_check(r):
    k = Kid(r).next()
    a, b = r.randint(21, 89), r.randint(3, 9)
    exact = a * b
    shown = exact if r.random() < 0.5 else exact * 10
    est = rnd_to(a, 10) * b
    ok = shown == exact
    right = ("Yes. It is close to %s" if ok else "No. It should be close to %s") % comma(est)
    return mcq("%s says %d × %d = %s. Use an estimate to check. Is it reasonable?" % (k["n"], a, b, comma(shown)), right,
               [("No. It should be close to %s" if ok else "Yes. It is close to %s") % comma(est), "Yes. All products are reasonable", "We cannot tell without the exact answer"],
               "%d ≈ %d, and %d × %d = %s. %s is %s that: <b>%s</b>." % (a, rnd_to(a, 10), rnd_to(a, 10), b, comma(est), comma(shown), "close to" if ok else "far from", right))


def one_story(r):
    k = Kid(r).next()
    kind = r.choice(["bus", "books", "money", "seats"])
    if kind == "bus":
        n, s = r.randint(312, 788), r.choice([48, 52, 49, 51])
        return mcq("%s students go on a field trip. Each bus holds %d students. About how many buses are needed? Use compatible numbers." % (n, s), "about %d" % ((rnd_to(n, 50) + 49) // 50), ["about %d" % (n // 10), "about %d" % (n - s), "about %d" % ((rnd_to(n, 50) + 49) // 50 + 5)],
                   "%d ≈ %d and %d ≈ 50. %d ÷ 50 = <b>about %d</b>." % (n, rnd_to(n, 50), s, rnd_to(n, 50), (rnd_to(n, 50) + 49) // 50))
    if kind == "books":
        a, b, c = r.randint(1100, 2900), r.randint(1100, 2900), r.randint(1100, 2900)
        est = rnd_to(a, 1000) + rnd_to(b, 1000) + rnd_to(c, 1000)
        return mcq("A library lends %s books in March, %s in April and %s in May. About how many books is that, to the nearest thousand?" % (comma(a), comma(b), comma(c)), "about %s" % comma(est),
                   ["about %s" % comma(a + b + c), "about %s" % comma(est + 1000), "about %s" % comma(est - 1000)], "%s + %s + %s = <b>about %s</b>." % (comma(rnd_to(a, 1000)), comma(rnd_to(b, 1000)), comma(rnd_to(c, 1000)), comma(est)))
    if kind == "money":
        p = r.randint(18, 39)
        n = r.randint(4, 9)
        return mcq("A video game costs $%d. %s wants to buy %d of them as gifts. About how much will they cost?" % (p, k["n"], n), "about $%d" % (rnd_to(p, 10) * n), ["about $%d" % (p + n), "about $%d" % (rnd_to(p, 10) * n + 100), "about $%d" % (rnd_to(p, 10))],
                   "$%d ≈ $%d. %d × $%d = <b>about $%d</b>." % (p, rnd_to(p, 10), n, rnd_to(p, 10), rnd_to(p, 10) * n))
    rows, seats = r.randint(21, 48), r.randint(18, 29)
    return mcq("A theater has %d rows with %d seats in each row. About how many seats is that? Round both numbers to the nearest ten." % (rows, seats), "about %s" % comma(rnd_to(rows, 10) * rnd_to(seats, 10)),
               ["about %s" % comma(rows * seats + 100), "about %d" % (rows + seats), "about %s" % comma(rnd_to(rows, 10) * rnd_to(seats, 10) * 10)], "%d × %d = <b>about %s</b>." % (rnd_to(rows, 10), rnd_to(seats, 10), comma(rnd_to(rows, 10) * rnd_to(seats, 10))))


def build():
    sets, R = build_sets([
        ("Estimate sums and differences", [("collect", one_sum, 20)]),
        ("Estimate products", [("collect", one_prod, 20)]),
        ("Estimate quotients with compatible numbers", [("collect", one_quot, 20)]),
        ("Is the answer reasonable?", [("collect", one_check, 20)]),
        ("Estimation word problems", [("collect", one_story, 20)]),
    ], 64010)
    finish(sets, R)
    body = lesson('<ul><li>An <b>estimate</b> is a close answer that is easy to find. Round to the nearest 10, 100 or 1,000, then compute.</li><li><b>Compatible numbers</b> are close numbers that work well together: 362 ÷ 9 is about 360 ÷ 9 = 40.</li><li>Use estimates to check whether an exact answer is reasonable.</li></ul>',
        [example("Estimate 4,387 + 2,812 to the nearest thousand.", ["4,387 ≈ 4,000", "2,812 ≈ 3,000"], "about 7,000"), example("Estimate 283 ÷ 7 with compatible numbers.", ["280 is close to 283 and divides by 7."], "280 ÷ 7 = 40")],
        [['Rounding to the wrong place', 'Read which place the question asks for.'], ['Finding the exact answer', 'An estimate uses rounded or compatible numbers.'], ['Using numbers that do not divide easily', 'For division, choose a nearby number that is a multiple of the divisor.']])
    faq = [('What does TEKS 4.4G ask?', 'Round to the nearest 10, 100 or 1,000 or use compatible numbers to estimate solutions involving whole numbers.'), ('What are compatible numbers?', 'Numbers close to the real ones that are easy to compute mentally, like 420 ÷ 6 instead of 418 ÷ 6.'), ('When should I estimate?', "To check answers, to answer 'about how many' questions, and to decide whether you have enough."), ('Is there only one right estimate?', 'Different rounding gives different estimates. On the test, follow the place or method the question gives.')]
    make('estimating-with-rounding-and-compatible-numbers', 10, 'Number and Operations', '4.4G',
         '4.4G round to the nearest 10, 100, or 1,000 or use compatible numbers to estimate solutions involving whole numbers',
         'Estimating with Rounding and Compatible Numbers', 'Estimating',
         'Free Grade 4 estimation worksheets for Texas TEKS 4.4G: estimate sums, differences, products and quotients by rounding or compatible numbers, check answers and word problems. 100 questions with answers.',
         'Round or use compatible numbers, then compute.', '362 ÷ 9 is about 360 ÷ 9 = 40. Use an estimate to check if an answer makes sense.',
         body, faq, sets, seo_title='Grade 4 Estimating Worksheets: Rounding and Compatible Numbers (TEKS 4.4G, STAAR)')


if __name__ == "__main__":
    build()
