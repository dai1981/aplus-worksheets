# -*- coding: utf-8 -*-
"""
India Class 11 Maths, NCERT Chapter 7: Binomial Theorem (CBSE Unit II Algebra)
  python3 tools/gen_in_maths_c11_binomial_theorem.py
Pascal's triangle and ⁿCᵣ, the number of terms, expanding (a + b)ⁿ, a coefficient or a term in an expansion, the sum
of the coefficients, and using the theorem to evaluate powers such as 99⁴ and 1.02⁵ (own makers and US Precalculus
makers).
Wrong answers come from real mistakes: n terms instead of n + 1, (a + b)ⁿ = aⁿ + bⁿ, leaving out the powers of
the number in the bracket, and the wrong sign on odd powers of a negative term.
"""
import random, math
from in_sr import U, T2, use, NCR, C, X
from in_common import comma, num
from fractions import Fraction as F
import gen_us_math_pc_binomial_theorem as ub

R = random.Random(911107)
coef = use(ub, "one_coef", R, [NCR])
xy = use(ub, "one_xy", R, [NCR])
term = use(ub, "one_term", R, [NCR])
exp = use(ub, "one_exp", R, [NCR])


def one_power(r):
    k = r.choice(["99", "101", "dec"])
    if k == "dec":
        b = r.choice([F(1, 100), F(2, 100), F(1, 10), F(3, 100)])
        n = r.choice([3, 4, 5])
        v = (1 + b) ** n
        approx = 1 + n * b + math.comb(n, 2) * b * b
        return T2("Use the binomial theorem to find (%s)<sup>%d</sup>, correct to 4 decimal places." % (num(1 + b), n), "%.4f" % float(v),
                  ["%.4f" % float(1 + n * b), "%.4f" % float(1 + b ** n), "%.4f" % float(approx + b) if abs(float(approx + b) - float(v)) > 0.00005 else "%.4f" % float(1 + 2 * n * b)],
                  "(1 + %s)<sup>%d</sup> = 1 + %s + … ; adding the terms gives <b>%.4f</b>. (1 + %s)<sup>%d</sup> is not 1 + %s<sup>%d</sup>." % (num(b), n, C(n, 1) + "(" + num(b) + ")", float(v), num(b), n, num(b), n))
    base = r.choice([10, 100, 1000])
    d = r.choice([1, 2, 3]) * (1 if k == "101" else -1)
    n = r.choice([3, 4]) if base < 1000 else 3
    v = (base + d) ** n
    shown = base + d
    return T2("Use the binomial theorem to evaluate %d<sup>%d</sup>." % (shown, n), comma(v),
              [comma(base ** n + d ** n), comma(base ** n + n * d * base ** (n - 1)), comma(v + 2 * abs(d) * base)],
              "(%d %s %d)<sup>%d</sup> = %s (add all %d terms, not only the first and the last). So %d<sup>%d</sup> = <b>%s</b>." % (
                  base, "+" if d > 0 else "−", abs(d), n, " + ".join("%s·%d<sup>%d</sup>·%s" % (C(n, i), base, n - i, ("(" + num(d) + ")") + ("<sup>%d</sup>" % i if i > 1 else "")) for i in range(n + 1)).replace("·%d<sup>0</sup>" % base, ""),
                  n + 1, shown, n, comma(v)))


def one_sum(r):
    a, b = r.choice([1, 2, 3]), r.choice([1, 2, -1, -2, 3])
    n = r.randint(3, 8)
    if a + b in (0, 1, -1) and r.random() < 0.5:
        return None
    s = (a + b) ** n
    return T2("Find the sum of the coefficients in the expansion of (%s%s %s %d)<sup>%d</sup>." % ("" if a == 1 else a, X, "+" if b > 0 else "−", abs(b), n), comma(s) if s >= 0 else "−" + comma(-s),
              [comma(2 ** n), comma(a ** n + b ** n) if a ** n + b ** n >= 0 else "−" + comma(-(a ** n + b ** n)), str(n + 1)],
              "Put %s = 1: (%d %s %d)<sup>%d</sup> = <b>%s</b>." % (X, a, "+" if b > 0 else "−", abs(b), n, comma(s) if s >= 0 else "−" + comma(-s)))


def one_larger(r):
    a = r.choice([F(11, 10), F(101, 100), F(1001, 1000)])
    n = int(1 / (a - 1))
    big = n * 10 if r.random() < 0.5 else 1000
    if a == F(11, 10):
        n, other = 10, r.choice([2, 3])
        return T2("Which is larger: (1.1)<sup>10</sup> or %d?" % other, "(1.1)<sup>10</sup>", ["%d" % other, "They are equal", "Cannot be decided without a calculator"],
                  "(1 + 0.1)<sup>10</sup> = 1 + 10(0.1) + 45(0.01) + … = 1 + 1 + 0.45 + … &gt; 2.45, so <b>(1.1)<sup>10</sup></b> is larger." if other == 2 else
                  "(1 + 0.1)<sup>10</sup> = 1 + 1 + 0.45 + 0.12 + 0.021 + … ≈ 2.59 &lt; 3, so <b>3</b> is larger." if False else
                  "(1 + 0.1)<sup>10</sup> ≈ 2.59, which is less than 3.") if other == 2 else None
    return T2("Which is larger: (%s)<sup>%s</sup> or 2?" % (num(a), comma(n)), "(%s)<sup>%s</sup>" % (num(a), comma(n)), ["2", "They are equal", "Cannot be decided without a calculator"],
              "(1 + 1/%s)<sup>%s</sup> = 1 + %s × (1/%s) + (positive terms) = 2 + (positive terms), so <b>(%s)<sup>%s</sup></b> is larger." % (comma(n), comma(n), comma(n), comma(n), num(a), comma(n)))


U(11, 7, "binomial-theorem", 7, "II", "Binomial Theorem: Pascal's Triangle, Expansions and Coefficients", "binomial theorem",
  "Historical perspective, statement and proof of the binomial theorem for positive integral indices; Pascal's triangle; simple applications (summary of the CBSE syllabus)",
  "Class 11 Binomial Theorem worksheet (NCERT Chapter 7): Pascal's triangle, ⁿCᵣ, number of terms, expansions, coefficients, sum of coefficients and evaluating powers like 99⁴. 100 questions with answers.",
  "(a + b)ⁿ = Σ ⁿCᵣ aⁿ⁻ʳ bʳ, with n + 1 terms.", "The coefficients are row n of Pascal's triangle.",
  "<ul><li>(a + b)<sup>n</sup> = <sup>n</sup>C<sub>0</sub>a<sup>n</sup> + <sup>n</sup>C<sub>1</sub>a<sup>n−1</sup>b + … + <sup>n</sup>C<sub>n</sub>b<sup>n</sup>; there are n + 1 terms.</li>"
  "<li>The coefficients are row n of Pascal's triangle: 1, 4, 6, 4, 1 for n = 4.</li>"
  "<li>In (a − b)<sup>n</sup> the signs alternate. Put <i>x</i> = 1 to find the sum of the coefficients.</li>"
  "<li>Powers like 99<sup>4</sup> = (100 − 1)<sup>4</sup> can be found term by term.</li></ul>",
  [("Expand (<i>x</i> + 2)<sup>4</sup>.", ["1, 4, 6, 4, 1 are the coefficients", "<i>x</i>⁴ + 4·2<i>x</i>³ + 6·4<i>x</i>² + 4·8<i>x</i> + 16"], "<i>x</i>⁴ + 8<i>x</i>³ + 24<i>x</i>² + 32<i>x</i> + 16")],
  ["Writing (a + b)ⁿ = aⁿ + bⁿ.", "Counting n terms instead of n + 1.", "Forgetting to raise the number in the bracket to its power."],
  [("How many terms does (a + b)ⁿ have?", "n + 1."), ("What is the sum of the numbers in row n of Pascal's triangle?", "2ⁿ.")],
  [("Pascal's triangle and ⁿCᵣ", [(coef, 14), (xy, 6)]),
   ("Expanding", [(exp, 14), (xy, 6)]),
   ("Coefficients and terms", [(term, 20)]),
   ("Sum of coefficients", [(one_sum, 14), (coef, 6)]),
   ("Evaluating powers", [(one_power, 16), (term, 4)])], 911107)
