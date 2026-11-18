# -*- coding: utf-8 -*-
"""
US Algebra 2: Sequences and Series (Common Core A-SSE.B.4, F-BF.A.2, F-IF.A.3)
  python3 tools/gen_us_math_a2_sequences_and_series.py
Summation notation, arithmetic series, finite geometric series, infinite geometric series and word problems
such as loan payments, salaries and bouncing balls.
Wrong answers come from real mistakes: counting the terms wrong, using the last term for n, using the formula
for one term instead of the sum, and summing an infinite series when |r| ≥ 1.
"""
import random
from fractions import Fraction as F
from us_hs import B, S, make, lesson, collect, T, num, MINUS, fr, People
from a2_common import sf, ps

R = random.Random(96201)


def sig(lo, hi, body):
    return "Σ<sub><i>k</i>=%s</sub><sup>%s</sup> %s" % (lo, hi, body)


# ------------------------------------------------------------ set 1: summation notation
def one_sig(r):
    kind = r.choice(["lin", "lin", "sq", "geo"])
    lo = r.choice([1, 1, 2, 3])
    hi = lo + r.randint(3, 5)
    if kind == "lin":
        a, b = r.choice([2, 3, 4, 5, -2]), r.randint(-5, 6)
        body = "(%s<i>k</i> %s %d)" % (sf(a) if a != 1 else "", "+" if b >= 0 else MINUS, abs(b))
        vals = [a * k + b for k in range(lo, hi + 1)]
    elif kind == "sq":
        b = r.randint(-3, 3)
        body = "(<i>k</i>²%s)" % ((" %s %d" % ("+" if b > 0 else MINUS, abs(b))) if b else "")
        vals = [k * k + b for k in range(lo, hi + 1)]
    else:
        c = r.choice([1, 2, 3])
        body = "%s2<sup><i>k</i></sup>" % ("" if c == 1 else num(c) + " · ")
        vals = [c * 2 ** k for k in range(lo, hi + 1)]
    ans = sum(vals)
    q = "Evaluate %s." % B(sig(lo, hi, body))
    return T(q, sf(ans), [sf(w) for w in dict.fromkeys([sum(vals[:-1]), sum(vals) - vals[0] + (vals[0] - (vals[1] - vals[0]) if kind == "lin" else 0) if False else sum(vals) + vals[-1], vals[-1], ans + len(vals)]) if w != ans][:3],
             "List the terms for <i>k</i> = %d to %d: %s. Add them: <b>%s</b>. There are %d terms, not %d." % (lo, hi, ", ".join(sf(v) for v in vals), sf(ans), hi - lo + 1, hi - lo))


# ------------------------------------------------------------ set 2: arithmetic series
def one_ar(r):
    a1 = r.randint(-10, 20)
    d = r.choice([x for x in range(-6, 9) if x])
    n = r.randint(8, 40)
    an = a1 + (n - 1) * d
    Sn = n * (a1 + an) // 2 if (n * (a1 + an)) % 2 == 0 else None
    if Sn is None:
        return None
    kind = r.choice(["given", "given", "list"])
    if kind == "given":
        q = "Find the sum of the first %d terms of the arithmetic sequence with <i>a</i><sub>1</sub> = %s and <i>d</i> = %s." % (n, sf(a1), sf(d))
    else:
        q = "Find the sum of the first %d terms of the arithmetic series %s, %s, %s, ..." % (n, sf(a1), sf(a1 + d), sf(a1 + 2 * d))
    wr = [n * (a1 + an + d) // 2 if (n * (a1 + an + d)) % 2 == 0 else Sn + d, (n - 1) * (a1 + an) // 2 if ((n - 1) * (a1 + an)) % 2 == 0 else Sn - an, an, n * (a1 + an)]
    return T(q, sf(Sn), [sf(w) for w in dict.fromkeys(wr) if w != Sn][:3],
             "Last term: <i>a</i><sub>%d</sub> = %s + (%d %s 1)(%s) = %s. Sum: <i>S</i> = <i>n</i>(<i>a</i><sub>1</sub> + <i>a</i><sub><i>n</i></sub>)/2 = %d(%s + %s)/2 = <b>%s</b>." % (
                 n, sf(a1), n, MINUS, sf(d), sf(an), n, sf(a1), ps(an), sf(Sn)))


# ------------------------------------------------------------ set 3: finite geometric series
def one_geo(r):
    a1 = r.choice([1, 2, 3, 4, 5, 6, 10])
    rr = r.choice([2, 3, -2, F(1, 2), 4, -3])
    n = r.randint(4, 8)
    if abs(F(rr)) >= 3 and n > 6:
        return None
    rr = F(rr)
    Sn = a1 * (1 - rr ** n) / (1 - rr)
    if Sn.denominator > 128:
        return None
    q = "Find the sum of the first %d terms of the geometric series %s + %s + %s + ..." % (n, sf(a1), sf(a1 * rr), sf(a1 * rr * rr))
    wr = [a1 * rr ** (n - 1), a1 * (1 - rr ** (n - 1)) / (1 - rr), a1 * (1 - rr ** (n + 1)) / (1 - rr), a1 / (1 - rr) if abs(rr) < 1 else a1 * n * rr]
    return T(q, sf(Sn), [sf(w) for w in dict.fromkeys(wr) if w != Sn][:3],
             "<i>S</i><sub><i>n</i></sub> = <i>a</i><sub>1</sub>(1 %s <i>r</i><sup><i>n</i></sup>)/(1 %s <i>r</i>) with <i>a</i><sub>1</sub> = %s, <i>r</i> = %s and <i>n</i> = %d: <b>%s</b>." % (
                 MINUS, MINUS, sf(a1), sf(rr), n, sf(Sn)))


# ------------------------------------------------------------ set 4: infinite geometric series
def one_inf(r):
    a1 = r.choice([2, 3, 4, 5, 6, 8, 9, 10, 12, 20])
    rr = F(r.choice([1, 1, 2, 3, -1, -2]), r.choice([2, 3, 4, 5]))
    big = r.random() < 0.2
    if big:
        rr = F(r.choice([3, 5, 4, -3]), 2)
    if abs(rr) >= 1 and not big:
        return None
    q = "Find the sum of the infinite geometric series %s + %s + %s + ..., if it exists." % (sf(a1), sf(a1 * rr), sf(a1 * rr * rr))
    if big:
        right = "The sum does not exist"
        return T(q, right, [sf(F(a1) / (1 - rr)), sf(F(a1) / (1 + rr)), sf(a1 * rr * 10)],
                 "<i>r</i> = %s and |<i>r</i>| ≥ 1, so the terms do not shrink and the series diverges. <b>%s</b>." % (sf(rr), right))
    Sm = F(a1) / (1 - rr)
    return T(q, sf(Sm), [sf(w) for w in dict.fromkeys([F(a1) / (1 + rr), F(a1) * (1 - rr), F(a1) / rr, "none"]) if w != "none" and w != Sm][:3] + ["The sum does not exist"],
             "|<i>r</i>| = |%s| &lt; 1, so the sum is <i>a</i><sub>1</sub>/(1 %s <i>r</i>) = %s ÷ (1 %s %s) = <b>%s</b>." % (sf(rr), MINUS, sf(a1), MINUS, ps(rr), sf(Sm)))


# ------------------------------------------------------------ set 5: word problems
def one_word(r):
    pp = People(r)
    nm, he, his = pp.next()
    kind = r.choice(["salary", "seats", "ball", "save", "decimal"])
    if kind == "salary":
        s0 = r.choice([40000, 45000, 50000, 52000])
        g = r.choice([3, 4, 5])
        n = r.choice([5, 10])
        tot = s0 * ((1 + g / 100) ** n - 1) / (g / 100)
        q = "%s's starting salary is %s and rises %d%% each year. What are %s total earnings over %d years, to the nearest dollar?" % (nm, "$" + num(s0), g, his, n)
        right = "$" + num(round(tot))
        return T(q, right, ["$" + num(round(s0 * (1 + g / 100) ** (n - 1))), "$" + num(round(s0 * n * (1 + g / 100))), "$" + num(round(s0 * ((1 + g / 100) ** (n + 1) - 1) / (g / 100)))],
                 "This is a geometric series with <i>a</i><sub>1</sub> = %s, <i>r</i> = 1.0%d and <i>n</i> = %d: %s(1.0%d<sup>%d</sup> %s 1)/0.0%d ≈ <b>%s</b>." % (num(s0), g, n, num(s0), g, n, MINUS, g, right))
    if kind == "seats":
        a1, d, n = r.choice([(20, 2, 25), (18, 3, 20), (24, 2, 30), (15, 4, 12)])
        an = a1 + (n - 1) * d
        Sn = n * (a1 + an) // 2
        q = "A theater has %d seats in the first row, and each row has %d more seats than the row in front. There are %d rows. How many seats are there in all?" % (a1, d, n)
        return T(q, num(Sn), [num(an), num(n * (a1 + an)), num(n * a1 + n * d)],
                 "Last row: %d + %d(%d) = %d. Total: %d(%d + %d)/2 = <b>%s</b>." % (a1, n - 1, d, an, n, a1, an, num(Sn)))
    if kind == "ball":
        h = r.choice([6, 8, 10, 12, 16])
        rr = F(r.choice([1, 3, 2]), r.choice([2, 4, 3]))
        if rr >= 1:
            return None
        down = F(h) / (1 - rr)
        up = F(h) * rr / (1 - rr)
        total = down + up
        q = "A ball is dropped from %d ft. Each bounce reaches %s of the previous height. What total vertical distance does it travel before it comes to rest?" % (h, fr(rr.numerator, rr.denominator))
        return T(q, "%s ft" % sf(total), ["%s ft" % sf(down), "%s ft" % sf(2 * down), "%s ft" % sf(up)],
                 "Down: %d ÷ (1 %s %s) = %s. Up: %s ÷ (1 %s %s) = %s. Total: <b>%s ft</b>." % (h, MINUS, sf(rr), sf(down), sf(h * rr), MINUS, sf(rr), sf(up), sf(total)))
    if kind == "save":
        a1, d = r.choice([(5, 5), (10, 2), (1, 1), (2, 3)])
        n = r.choice([12, 20, 26, 30])
        an = a1 + (n - 1) * d
        Sn = n * (a1 + an) // 2 if n * (a1 + an) % 2 == 0 else None
        if Sn is None:
            return None
        q = "%s saves %s the first week and %s more each week after that. How much has %s saved after %d weeks?" % (nm, "$" + num(a1), "$" + num(d), he, n)
        return T(q, "$" + num(Sn), ["$" + num(an), "$" + num(n * a1 + n * d), "$" + num(n * (a1 + an))],
                 "Arithmetic series: the last week is %s + %d(%s) = %s. Sum: %d(%s + %s)/2 = <b>%s</b>." % (num(a1), n - 1, num(d), "$" + num(an), n, num(a1), num(an), "$" + num(Sn)))
    dgt = r.choice([3, 6, 7, 2, 4, 5, 8])
    q = "Write the repeating decimal 0.%d%d%d... as a fraction, using an infinite geometric series." % (dgt, dgt, dgt)
    v = F(dgt, 9)
    return T(q, sf(v), [sf(F(dgt, 10)), sf(F(dgt, 99)), sf(F(dgt, 100))],
             "0.%d%d%d... = %s + %s + ... with <i>r</i> = 1/10. Sum = (%d/10) ÷ (9/10) = <b>%s</b>." % (dgt, dgt, dgt, fr(dgt, 10), fr(dgt, 100), dgt, sf(v)))


def build():
    sets = [S("Summation notation", collect(one_sig, 20, R)),
            S("Arithmetic series", collect(one_ar, 20, R)),
            S("Finite geometric series", collect(one_geo, 20, R)),
            S("Infinite geometric series", collect(one_inf, 20, R)),
            S("Word problems", collect(one_word, 20, R))]
    body = lesson(
        "<p>A <b>series</b> is the sum of the terms of a sequence. Summation (sigma) notation lists the terms to add: write each term for <i>k</i> = the start value up to the end value.</p>"
        "<ul><li><b>Arithmetic series</b>: <i>S</i><sub><i>n</i></sub> = <i>n</i>(<i>a</i><sub>1</sub> + <i>a</i><sub><i>n</i></sub>)/2, where <i>a</i><sub><i>n</i></sub> = <i>a</i><sub>1</sub> + (<i>n</i> %s 1)<i>d</i>.</li>"
        "<li><b>Geometric series</b>: <i>S</i><sub><i>n</i></sub> = <i>a</i><sub>1</sub>(1 %s <i>r</i><sup><i>n</i></sup>)/(1 %s <i>r</i>).</li>"
        "<li><b>Infinite geometric series</b>: if |<i>r</i>| &lt; 1, the sum is <i>a</i><sub>1</sub>/(1 %s <i>r</i>). If |<i>r</i>| ≥ 1, there is no sum.</li></ul>" % (MINUS, MINUS, MINUS, MINUS),
        [("Find 3 + 7 + 11 + ... for 20 terms.", ["<i>a</i><sub>20</sub> = 3 + 19(4) = 79", "<i>S</i> = 20(3 + 79)/2"], "820"),
         ("Find 12 + 6 + 3 + ...", ["<i>r</i> = 1/2", "12 ÷ (1 %s 1/2)" % MINUS], "24")],
        ["Counting terms wrong: <i>k</i> = 3 to 8 has 6 terms, not 5.",
         "Using the last term instead of the number of terms for <i>n</i>.",
         "Giving the <i>n</i>th term when the question asks for the sum.",
         "Finding an infinite sum when |<i>r</i>| ≥ 1. It does not exist."])
    faq = [("What is the formula for an arithmetic series?", "S_n = n(a_1 + a_n)/2. Average the first and last terms and multiply by the number of terms."),
           ("What is the formula for a finite geometric series?", "S_n = a_1(1 − r^n)/(1 − r), where r is the common ratio and n is the number of terms."),
           ("When does an infinite geometric series have a sum?", "Only when |r| < 1. Then the sum is a_1/(1 − r)."),
           ("What does sigma notation mean?", "Σ means add. The numbers below and above the sigma give the first and last values of the index k.")]
    make("sequences-and-series", 12, "A-SSE.B.4",
         "Arithmetic and Geometric Series",
         "Arithmetic and Geometric Series Worksheet: Sigma Notation, Infinite Series (Algebra 2) | 100 Questions",
         "Sequences and Series",
         "Derive the formula for the sum of a finite geometric series (when the common ratio is not 1), and use the formula to solve problems. For example, calculate mortgage payments.",
         "Free Algebra 2 worksheet on series: sigma notation, arithmetic series, finite and infinite geometric series and word problems like salaries and bouncing balls. 100 questions.",
         "Arithmetic: S = n(a₁ + aₙ)/2. Geometric: S = a₁(1 − rⁿ)/(1 − r).",
         "An infinite geometric series has a sum a₁/(1 − r) only when |r| < 1.",
         body, faq, sets, R, domain="Sequences and Series", grade="algebra-2")


if __name__ == "__main__":
    build()
