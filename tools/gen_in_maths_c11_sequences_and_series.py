# -*- coding: utf-8 -*-
"""
India Class 11 Maths, NCERT Chapter 8: Sequences and Series (CBSE Unit II Algebra)
  python3 tools/gen_in_maths_c11_sequences_and_series.py
Geometric progressions: the common ratio, the nth term, which term has a given value, the sum of n terms and of an
infinite G.P., the arithmetic and geometric means and A.M. ≥ G.M., sigma notation, and G.P. word problems (own
makers and US Algebra 2 makers).
Wrong answers come from real mistakes: arⁿ for the nth term, r = a₁ − a₂, a(rⁿ − 1)/(r + 1), a sum to infinity
when |r| ≥ 1, and (a + b)/2 for the G.M.
"""
import random, math
from fractions import Fraction as F
from in_sr import U, T2, use, frs
from in_common import comma, num, fv
import gen_us_math_a2_sequences_and_series as us

R = random.Random(911108)
FX = [("+ −", "− "), ("theater", "theatre"), ("Theater", "Theatre")]
geo = use(us, "one_geo", R, FX)
inf = use(us, "one_inf", R, FX)
sig = use(us, "one_sig", R, FX)
_word = use(us, "one_word", R, FX)


def word(r):
    it = _word(r)
    return None if it is None or " ft" in it["q"] else it


def seq(a, r_, n=4):
    return ", ".join(fv(a * r_ ** i) for i in range(n)) + ", …"


def gp(r):
    a = r.choice([1, 2, 3, 4, 5, -2, -3, F(1, 2), 81, 64, 128])
    rr = r.choice([2, 3, -2, -3, F(1, 2), F(-1, 2), F(1, 3), 4])
    if (abs(a) > 20 and abs(rr) > 1) or (F(a).denominator > 1 and abs(rr) < 1):
        return None
    return F(a), F(rr)


def one_nth(r):
    g = gp(r)
    if not g:
        return None
    a, rr = g
    n = r.randint(5, 9)
    t = a * rr ** (n - 1)
    if abs(t.numerator) > 10 ** 6 or t.denominator > 10 ** 4:
        return None
    k = r.choice(["nth", "which", "ratio"])
    if k == "nth":
        return T2("Find the %s term of the G.P. %s" % (["", "", "", "", "", "5th", "6th", "7th", "8th", "9th"][n], seq(a, rr)), fv(t),
                  [fv(a * rr ** n), fv(a + (n - 1) * (a * rr - a)), fv(-t) if t != 0 else "1"],
                  "a = %s, r = %s, so a<sub>%d</sub> = ar<sup>%d</sup> = %s × (%s)<sup>%d</sup> = <b>%s</b>." % (fv(a), fv(rr), n, n - 1, fv(a), fv(rr), n - 1, fv(t)))
    if k == "which":
        return T2("Which term of the G.P. %s is %s?" % (seq(a, rr), fv(t)), "%dth" % n if n > 3 else str(n), ["%dth" % (n + 1), "%dth" % (n - 1), "%dth" % (n + 2)],
                  "ar<sup>n−1</sup> = %s gives (%s)<sup>n−1</sup> = %s, so n − 1 = %d and it is the <b>%dth</b> term." % (fv(t), fv(rr), fv(t / a), n - 1, n))
    return T2("What is the common ratio of the G.P. %s" % seq(a, rr), fv(rr), [fv(1 / rr), fv(a * rr - a), fv(-rr)],
              "r = a<sub>2</sub> ÷ a<sub>1</sub> = %s ÷ %s = <b>%s</b>." % (fv(a * rr), fv(a), fv(rr)))


def one_sum(r):
    a = r.choice([1, 2, 3, 5, 7])
    rr = r.choice([2, 3, F(1, 2), F(1, 3), -2])
    n = r.randint(4, 8)
    s = a * (1 - F(rr) ** n) / (1 - F(rr))
    if s.denominator > 1000:
        return None
    return T2("Find the sum of the first %d terms of the G.P. %s" % (n, seq(F(a), F(rr), 3)), fv(s),
              [fv(a * F(rr) ** (n - 1)), fv(a * (F(rr) ** n - 1) / (F(rr) + 1)), fv(a * (1 - F(rr) ** (n + 1)) / (1 - F(rr)))],
              "S<sub>n</sub> = a(r<sup>n</sup> − 1) ÷ (r − 1) = %s × ((%s)<sup>%d</sup> − 1) ÷ (%s − 1) = <b>%s</b>." % (a, fv(rr), n, fv(rr), fv(s)))


def one_means(r):
    k = r.choice(["gm", "am", "find", "insert"])
    if k == "gm":
        m, p, q = r.randint(1, 9), r.randint(1, 6), r.randint(1, 6)
        a, b = m * p * p, m * q * q
        if a == b:
            return None
        g = m * p * q
        return T2("Find the geometric mean of %d and %d." % (a, b), str(g), [fv(F(a + b, 2)), comma(a * b), str(g * 2)],
                  "G.M. = √(ab) = √(%d × %d) = √%s = <b>%d</b>." % (a, b, comma(a * b), g))
    if k == "am":
        a, b = r.randint(2, 60), r.randint(2, 60)
        if (a + b) % 2:
            return None
        return T2("Find the arithmetic mean of %d and %d." % (a, b), str((a + b) // 2), [str(a + b), str(abs(a - b) // 2), str(int(math.isqrt(a * b))) if math.isqrt(a * b) ** 2 == a * b else str((a + b) // 2 + 1)],
                  "A.M. = (a + b) ÷ 2 = <b>%d</b>." % ((a + b) // 2))
    if k == "find":
        p, q = r.sample(range(1, 13), 2)
        a, b = p * p, q * q
        if (a + b) % 2:
            return None
        A, G = (a + b) // 2, p * q
        return T2("The A.M. and G.M. of two positive numbers are %d and %d. Find the numbers." % (A, G), "%d and %d" % (min(a, b), max(a, b)),
                  ["%d and %d" % (min(p, q), max(p, q)), "%d and %d" % (A - G, A + G), "%d and %d" % (G, A)],
                  "a + b = %d and ab = %d, so a and b are the roots of t² − %dt + %d = 0: <b>%d and %d</b>. (A.M. ≥ G.M.: %d ≥ %d.)" % (2 * A, G * G, 2 * A, G * G, min(a, b), max(a, b), A, G))
    a = r.choice([1, 2, 3, 5])
    rr = r.choice([2, 3])
    n = r.choice([2, 3])
    b = a * rr ** (n + 1)
    means = [a * rr ** i for i in range(1, n + 1)]
    return T2("Insert %d numbers between %d and %d so that the resulting sequence is a G.P." % (n, a, b), ", ".join(map(str, means)),
              [", ".join(str(a + i * (b - a) // (n + 1)) for i in range(1, n + 1)) if (b - a) % (n + 1) == 0 else ", ".join(str(x * 2) for x in means),
               ", ".join(str(x * rr) for x in means), ", ".join(str(a * (rr + 1) ** i) for i in range(1, n + 1))],
              "%d = %d × r<sup>%d</sup>, so r = %d. The numbers are <b>%s</b>." % (b, a, n + 1, rr, ", ".join(map(str, means))))


def one_story(r):
    k = r.choice(["bacteria", "ball", "salary"])
    if k == "bacteria":
        n0, h = r.choice([30, 50, 100, 200, 500]), r.randint(3, 8)
        return T2("A culture has %d bacteria, and the number doubles every hour. How many bacteria are there at the end of hour %d?" % (n0, h), comma(n0 * 2 ** h),
                  [comma(n0 * 2 ** (h - 1)), comma(n0 * 2 * h), comma(n0 * 2 ** (h + 1))],
                  "The counts form a G.P. with a = %d, r = 2: after %d hours there are %d × 2<sup>%d</sup> = <b>%s</b>." % (n0, h, n0, h, comma(n0 * 2 ** h)))
    if k == "ball":
        hgt = r.choice([81, 64, 125, 243, 32])
        rr = F(2, 3) if hgt in (81, 243) else (F(3, 4) if hgt == 64 else (F(4, 5) if hgt == 125 else F(1, 2)))
        n = r.randint(2, 4)
        v = hgt * rr ** n
        return T2("A ball is dropped from %d m. Each bounce reaches %s of the height before it. How high does it rise after bounce %d?" % (hgt, frs(rr), n), "%s m" % fv(v),
                  ["%s m" % fv(hgt * rr ** (n - 1)), "%s m" % fv(hgt - n * hgt * (1 - rr)), "%s m" % fv(hgt * rr ** (n + 1))],
                  "The heights form a G.P.: %d × (%s)<sup>%d</sup> = <b>%s m</b>." % (hgt, frs(rr), n, fv(v)))
    s0, p, y = r.choice([20000, 25000, 30000, 40000]), r.choice([5, 10, 20]), r.randint(2, 4)
    v = F(s0) * (1 + F(p, 100)) ** y
    if v.denominator != 1:
        return None
    return T2("A salary of ₹%s a month rises by %d%% every year. What is the monthly salary after %d years?" % (comma(s0), p, y), "₹" + comma(v),
              ["₹" + comma(s0 + s0 * p * y // 100), "₹" + comma(F(s0) * (1 + F(p, 100)) ** (y - 1)), "₹" + comma(s0 * (100 + p * y) // 100 + 1000)],
              "Each year it is multiplied by %s: %s × (%s)<sup>%d</sup> = <b>₹%s</b>." % (num(1 + F(p, 100)), comma(s0), num(1 + F(p, 100)), y, comma(v)))


U(11, 8, "sequences-and-series", 8, "II", "Sequences and Series: G.P., Sums, A.M. and G.M.", "sequences and series",
  "Sequence and series; arithmetic mean (A.M.); geometric progression (G.P.), general term of a G.P., sum of n terms of a G.P., infinite G.P. and its sum, geometric mean (G.M.), relation between A.M. and G.M. (summary of the CBSE syllabus)",
  "Class 11 Sequences and Series worksheet (NCERT Chapter 8): G.P. nth term, common ratio, sum of n terms, infinite G.P., A.M., G.M., inserting means, A.M. ≥ G.M. and word problems. 100 questions with answers.",
  "In a G.P., aₙ = arⁿ⁻¹ and Sₙ = a(rⁿ − 1)/(r − 1).", "For |r| &lt; 1, the sum to infinity is a/(1 − r).",
  "<ul><li>A <b>G.P.</b> multiplies by the same ratio r: a, ar, ar², …; a<sub>n</sub> = ar<sup>n−1</sup>.</li>"
  "<li>Sum of n terms: S<sub>n</sub> = a(r<sup>n</sup> − 1) ÷ (r − 1) (r ≠ 1). If |r| &lt; 1, S<sub>∞</sub> = a ÷ (1 − r).</li>"
  "<li>A.M. of a and b = (a + b) ÷ 2; G.M. = √(ab). For positive a, b: A.M. ≥ G.M.</li></ul>",
  [("Find the 10th term of 5, 25, 125, …", ["a = 5, r = 5", "a₁₀ = 5 × 5⁹ = 5¹⁰"], "5¹⁰ = 97,65,625")],
  ["Using arⁿ instead of arⁿ⁻¹ for the nth term.", "Finding a sum to infinity when |r| ≥ 1.", "Using (a + b)/2 for the G.M."],
  [("When does an infinite G.P. have a sum?", "Only when −1 &lt; r &lt; 1."), ("Is the A.M. always at least the G.M.?", "Yes, for two positive numbers; they are equal only when the numbers are equal.")],
  [("Terms of a G.P.", [(one_nth, 20)]),
   ("Sum of a G.P.", [(one_sum, 10), (geo, 10)]),
   ("Infinite G.P. and sigma notation", [(inf, 12), (sig, 8)]),
   ("A.M. and G.M.", [(one_means, 20)]),
   ("Word problems", [(one_story, 14), (word, 6)])], 911108)
