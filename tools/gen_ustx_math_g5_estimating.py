# -*- coding: utf-8 -*-
"""
Texas Grade 5 Math: Estimating with Whole Numbers, Decimals and Fractions (TEKS 5.3A)
  python3 tools/gen_ustx_math_g5_estimating.py
Estimating sums and differences of decimals, products and quotients of whole numbers, fraction sums with
benchmarks, checking answers, and word problems.
Wrong answers come from real mistakes: rounding to the wrong place, finding the exact answer, and choosing numbers
that do not divide easily.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)

tx_common.GRADE = "grade-5"

def rnd_to(n, p):
    return (n + p // 2) // p * p


def one_dec(r):
    a, b = r.randint(105, 9895), r.randint(105, 9895)
    op = r.choice(["+", "−"])
    if op == "−" and a < b:
        a, b = b, a
    ra, rb = rnd_to(a, 100) // 100, rnd_to(b, 100) // 100
    est = ra + rb if op == "+" else ra - rb
    if a % 100 in (0, 50) or b % 100 in (0, 50) or est <= 0:
        return None
    exact = (a + b if op == "+" else a - b) / 100.0
    return mcq("Round each number to the nearest whole number to estimate %d.%02d %s %d.%02d." % (a // 100, a % 100, op, b // 100, b % 100), est, [round(exact, 2), est + 1, est - 1 if est > 1 else est + 2],
               "%d.%02d ≈ %d and %d.%02d ≈ %d. %d %s %d = <b>%d</b>." % (a // 100, a % 100, ra, b // 100, b % 100, rb, ra, op, rb, est))


def one_prod(r):
    a, b = r.randint(110, 980), r.randint(11, 98)
    ra, rb = rnd_to(a, 100), rnd_to(b, 10)
    if ra == a or rb == b:
        return None
    return mcq("Estimate %d × %d by rounding %d to the nearest hundred and %d to the nearest ten." % (a, b, a, b), comma(ra * rb), [comma(a * b), comma(ra * rb * 10), comma(ra + rb), comma(ra * rb // 10)],
               "%d × %d = <b>%s</b>." % (ra, rb, comma(ra * rb)))


def one_quot(r):
    d = r.randint(12, 89)
    rd = rnd_to(d, 10)
    q = r.randint(3, 90)
    c = rd * q
    n = c + r.randint(-rd // 3, rd // 3)
    if n == c or n < 100 or rd == d:
        return None
    return mcq("Use compatible numbers to estimate %s ÷ %d." % (comma(n), d), comma(q), [comma(q * 10), comma(q + 10), comma(n // 10)],
               "%d is close to %d, and %s is close to %s. %s ÷ %d = <b>%d</b>." % (d, rd, comma(n), comma(c), comma(c), rd, q))


def one_frac(r):
    pairs = [(fr(1, 3), 1 / 3.0), (fr(3, 8), 3 / 8.0), (fr(5, 6), 5 / 6.0), (fr(7, 8), 7 / 8.0), (fr(1, 8), 1 / 8.0), (fr(4, 9), 4 / 9.0), (fr(5, 12), 5 / 12.0), (fr(9, 10), 0.9), (fr(1, 10), 0.1), (fr(2, 5), 0.4), (fr(3, 5), 0.6), (fr(11, 12), 11 / 12.0)]
    (a, va), (b, vb) = r.sample(pairs, 2)
    s = va + vb
    opts = [(0, "0"), (0.5, fr(1, 2)), (1, "1"), (1.5, "1" + fr(1, 2)), (2, "2")]
    best = min(opts, key=lambda o: abs(o[0] - s))
    if sorted(abs(o[0] - s) for o in opts)[1] - abs(best[0] - s) < 0.08:
        return None
    return mcq("Use benchmarks 0, %s and 1 to estimate %s + %s." % (fr(1, 2), a, b), best[1], [o[1] for o in opts if o != best],
               "%s is about %s and %s is about %s, so the sum is about <b>%s</b>." % (a, min(opts[:3], key=lambda o: abs(o[0] - va))[1], b, min(opts[:3], key=lambda o: abs(o[0] - vb))[1], best[1]))


def one_story(r):
    k = Kid(r).next()
    kind = r.choice(["shop", "bus", "save", "fuel"])
    if kind == "shop":
        items = [r.randint(105, 2495) for _ in range(3)]
        est = sum(rnd_to(c, 100) // 100 for c in items)
        if any(c % 100 == 50 for c in items):
            return None
        txt = ", ".join("$%d.%02d" % (c // 100, c % 100) for c in items)
        return mcq("%s buys three items that cost %s. About how much does %s spend? Round each price to the nearest dollar." % (k["n"], txt, k["he"]), "about $%d" % est,
                   ["about $%d" % (est + 3), "about $%d" % (sum(items) // 100), "about $%d" % (est * 10)] if sum(items) // 100 != est else ["about $%d" % (est + 3), "about $%d" % (est - 2), "about $%d" % (est * 10)],
                   "%s ≈ %s. Total ≈ <b>$%d</b>." % (txt, ", ".join("$%d" % (rnd_to(c, 100) // 100) for c in items), est))
    if kind == "bus":
        n, s = r.randint(410, 890), r.choice([46, 47, 48, 52, 53, 54])
        e = (rnd_to(n, 50) + 49) // 50
        return mcq("%d students go to the state fair in Dallas. Each bus holds %d students. About how many buses are needed?" % (n, s), "about %d" % e, ["about %d" % (n // 10), "about %d" % (e * 5), "about %d" % (n - s)],
                   "%d ≈ 50 and %d ≈ %d. %d ÷ 50 ≈ <b>%d</b>." % (s, n, rnd_to(n, 50), rnd_to(n, 50), e))
    if kind == "save":
        w, m = r.randint(18, 49), r.randint(11, 29)
        return mcq("%s saves $%d a week for %d weeks. About how much is that? Round both numbers to the nearest ten." % (k["n"], w, m), "about $%s" % comma(rnd_to(w, 10) * rnd_to(m, 10)), ["about $%s" % comma(w * m + 100), "about $%d" % (w + m), "about $%s" % comma(rnd_to(w, 10) * rnd_to(m, 10) * 10)],
                   "$%d × %d = <b>about $%s</b>." % (rnd_to(w, 10), rnd_to(m, 10), comma(rnd_to(w, 10) * rnd_to(m, 10))))
    g = r.randint(11, 19)
    mi = r.randint(28, 34)
    return mcq("A car can go about %d miles on 1 gallon of gas. About how far can it go on %d.%d gallons? Round both numbers to the nearest ten." % (mi, g, r.randint(1, 4)), "about %d miles" % (rnd_to(mi, 10) * rnd_to(g, 10)),
               ["about %d miles" % (mi + g), "about %d miles" % (rnd_to(mi, 10) * rnd_to(g, 10) * 10), "about %d miles" % (rnd_to(mi, 10) * rnd_to(g, 10) // 2)],
               "%d × %d = <b>about %d miles</b>." % (rnd_to(mi, 10), rnd_to(g, 10), rnd_to(mi, 10) * rnd_to(g, 10)))


def build():
    sets, R = build_sets([
        ("Estimate decimal sums and differences", [("collect", one_dec, 20)]),
        ("Estimate products", [("collect", one_prod, 20)]),
        ("Estimate quotients with compatible numbers", [("collect", one_quot, 20)]),
        ("Estimate fraction sums with benchmarks", [("collect", one_frac, 20)]),
        ("Estimation word problems", [("collect", one_story, 20)]),
    ], 65003)
    finish(sets, R)
    body = lesson('<ul><li>An <b>estimate</b> is a close answer found with easy numbers. Round, then compute.</li><li>For decimals, round to the nearest whole number or tenth. For products, round each factor. For quotients, use <b>compatible numbers</b> that divide easily.</li><li>For fractions, compare each to 0, 1/2 or 1.</li><li>Use estimates to check whether an exact answer is reasonable.</li></ul>',
        [example("Estimate 487 × 32.", ["487 ≈ 500", "32 ≈ 30", "500 × 30"], "15,000"), example("Estimate 2,743 ÷ 38.", ["38 ≈ 40", "2,743 ≈ 2,800", "2,800 ÷ 40"], "70")],
        [['Finding the exact answer', 'An estimate uses rounded or compatible numbers.'], ['Choosing numbers that do not divide easily', 'Pick a nearby multiple of the rounded divisor.'], ['Rounding to the wrong place', 'Use the place the question asks for.']])
    faq = [('What does TEKS 5.3A ask?', 'Estimate to determine solutions to mathematical and real-world problems involving addition, subtraction, multiplication or division.'), ('What are compatible numbers?', 'Nearby numbers that work well together, like 2,800 ÷ 40 instead of 2,743 ÷ 38.'), ('How do you estimate with fractions?', 'Compare each fraction to 0, 1/2 or 1. 7/8 is about 1, and 3/8 is about 1/2.'), ('When is an estimate enough?', "When the question asks 'about how many' or when you only need to check if an answer makes sense.")]
    make('estimating', 3, 'Number and Operations', '5.3A',
         '5.3A estimate to determine solutions to mathematical and real-world problems involving addition, subtraction, multiplication, or division',
         'Estimating with Whole Numbers, Decimals and Fractions', 'Estimating',
         'Free Grade 5 estimation worksheets for Texas TEKS 5.3A: estimate decimal sums and differences, products, quotients with compatible numbers, fraction sums with benchmarks and word problems. 100 questions with answers.',
         'Round or use compatible numbers, then compute.', '2,743 ÷ 38 ≈ 2,800 ÷ 40 = 70. Fractions: compare with 0, 1/2 and 1.',
         body, faq, sets, seo_title='Grade 5 Estimating Worksheets: Decimals, Products and Quotients (TEKS 5.3A, STAAR)')


if __name__ == "__main__":
    build()
