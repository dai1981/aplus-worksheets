# -*- coding: utf-8 -*-
"""
India Class 11 Maths, NCERT Chapter 13: Statistics (CBSE Unit V Statistics and Probability)
  python3 tools/gen_in_maths_c11_statistics.py
Range, mean deviation about the mean and about the median for raw data and for a frequency table, variance and
standard deviation, the shortcut Σx² ÷ n − x̄², the effect of adding or multiplying every value, and comparing
consistency (own makers and SG Secondary 4 makers).
Wrong answers come from real mistakes: forgetting the absolute value, dividing by n − 1, using the mean instead of
the median, giving the variance for the standard deviation, and adding a constant to the standard deviation.
"""
import random, math
from fractions import Fraction as F
from in_sr import U, T2, use
from in_common import num, fv, table

R = random.Random(911113)
FX = [("correct to 3 significant figures", "correct to 2 decimal places")]
sd_list = use(__import__("gen_sg_maths_s4_standard_deviation"), "one_list", R)
sd_sums = use(__import__("gen_sg_maths_s4_standard_deviation"), "one_sums", R)
change = use(__import__("gen_sg_maths_s4_standard_deviation"), "one_change", R)
cmp_ = use(__import__("gen_sg_maths_s4_standard_deviation"), "one_cmp", R)


def data(r, n):
    xs = [r.randint(2, 40) for _ in range(n)]
    return xs


def one_md(r):
    n = r.choice([5, 6, 7, 8, 9, 10])
    xs = data(r, n)
    m = F(sum(xs), n)
    if m.denominator != 1:
        return None
    md = F(sum(abs(x - m) for x in xs), n)
    shown = ", ".join(map(str, xs))
    return T2("Find the mean deviation about the mean of: %s." % shown, num(md) or fv(md),
              [num(F(sum(x - m for x in xs if x > m), n)) or fv(F(sum(x - m for x in xs if x > m), n)) if F(sum(x - m for x in xs if x > m), n) != md else num(md + 1),
               num(F(sum(abs(x - m) for x in xs), n - 1)) or fv(F(sum(abs(x - m) for x in xs), n - 1)), "0"],
              "Mean x̄ = %d. Σ|x − x̄| = %d, so M.D.(x̄) = %d ÷ %d = <b>%s</b>." % (m, sum(abs(x - m) for x in xs), sum(abs(x - m) for x in xs), n, num(md) or fv(md)))


def one_mdmed(r):
    n = r.choice([5, 7, 9, 11])
    xs = sorted(data(r, n))
    med = xs[n // 2]
    md = F(sum(abs(x - med) for x in xs), n)
    m = F(sum(xs), n)
    shown = ", ".join(map(str, r.sample(xs, n)))
    wr_mean = F(sum(abs(x - m) for x in xs), n)
    return T2("Find the mean deviation about the median of: %s." % shown, num(md) or fv(md),
              [num(wr_mean) or fv(wr_mean) if wr_mean != md else num(md + 1), str(med), num(F(sum(abs(x - med) for x in xs), n - 1)) or fv(F(sum(abs(x - med) for x in xs), n - 1))],
              "In order, the median is %d. Σ|x − M| = %d, so M.D.(M) = %d ÷ %d = <b>%s</b>." % (med, sum(abs(x - med) for x in xs), sum(abs(x - med) for x in xs), n, num(md) or fv(md)))


def one_var(r):
    n = r.choice([4, 5, 6, 8])
    m = r.randint(5, 30)
    devs = None
    for _ in range(50):
        d = [r.randint(-6, 6) for _ in range(n - 1)]
        last = -sum(d)
        if abs(last) <= 8:
            devs = d + [last]
            break
    if devs is None:
        return None
    xs = [m + d for d in devs]
    var = F(sum(d * d for d in devs), n)
    k = r.choice(["var", "sd", "range"])
    shown = ", ".join(map(str, xs))
    if k == "range":
        return T2("Find the range of: %s." % shown, str(max(xs) - min(xs)), [str(max(xs)), str(max(xs) + min(xs)), str(m)],
                  "Range = largest − smallest = %d − %d = <b>%d</b>." % (max(xs), min(xs), max(xs) - min(xs)))
    if k == "var":
        return T2("Find the variance of: %s." % shown, num(var) or fv(var), [num(F(sum(d * d for d in devs), n - 1)) or fv(F(sum(d * d for d in devs), n - 1)),
                                                                         num(F(sum(abs(d) for d in devs), n)) or fv(F(sum(abs(d) for d in devs), n)), str(m)],
                  "x̄ = %d. Σ(x − x̄)² = %d, so σ² = %d ÷ %d = <b>%s</b>." % (m, sum(d * d for d in devs), sum(d * d for d in devs), n, num(var) or fv(var)))
    s = math.isqrt(var.numerator) if var.denominator == 1 and math.isqrt(var.numerator) ** 2 == var.numerator else None
    if s is None:
        return None
    return T2("Find the standard deviation of: %s." % shown, str(s), [num(var), num(F(sum(abs(d) for d in devs), n)) or fv(F(sum(abs(d) for d in devs), n)), str(s + 1)],
              "x̄ = %d, σ² = %d ÷ %d = %d, so σ = √%d = <b>%d</b>." % (m, sum(d * d for d in devs), n, var, var, s))


def one_freq(r):
    xs = sorted(r.sample(range(2, 30, 2), 4))
    fs = [r.randint(1, 8) for _ in xs]
    N = sum(fs)
    m = F(sum(x * f for x, f in zip(xs, fs)), N)
    if m.denominator not in (1, 2, 4, 5, 10):
        return None
    md = F(sum(f * abs(x - m) for x, f in zip(xs, fs)), N)
    if md.denominator not in (1, 2, 4, 5, 8, 10, 20, 25, 50):
        return None
    tbl = table(["<i>x</i>", "<i>f</i>"], [[x, f] for x, f in zip(xs, fs)])
    wr = F(sum(abs(x - m) for x in xs), len(xs))
    return T2("Find the mean deviation about the mean for the data below." + tbl, num(md), [num(wr) or fv(wr) if wr != md else num(md + 1), num(m), num(F(sum(f * abs(x - m) for x, f in zip(xs, fs)), len(xs))) or "0"],
              "x̄ = Σfx ÷ Σf = %s ÷ %d = %s. Σf|x − x̄| = %s, so M.D. = <b>%s</b>." % (sum(x * f for x, f in zip(xs, fs)), N, num(m), num(sum(f * abs(x - m) for x, f in zip(xs, fs))), num(md)))


U(11, 13, "statistics", 13, "VII", "Statistics: Mean Deviation, Variance and Standard Deviation", "statistics",
  "Measures of dispersion; range, mean deviation, variance and standard deviation of ungrouped and grouped data (summary of the CBSE syllabus)",
  "Class 11 Statistics worksheet (NCERT Chapter 13): range, mean deviation about the mean and median, variance and standard deviation for raw and grouped data, and comparing consistency. 100 questions with answers.",
  "Mean deviation = Σ|x − a| ÷ n; variance = Σ(x − x̄)² ÷ n.", "Standard deviation σ is the square root of the variance.",
  "<ul><li><b>Range</b> = largest value − smallest value.</li>"
  "<li><b>Mean deviation</b> about a (the mean or the median): Σ|x − a| ÷ n, or Σf|x − a| ÷ Σf for a frequency table.</li>"
  "<li><b>Variance</b> σ² = Σ(x − x̄)² ÷ n = Σx² ÷ n − x̄²; <b>standard deviation</b> σ = √(variance).</li>"
  "<li>Adding a constant to every value does not change σ; multiplying every value by k multiplies σ by |k|.</li></ul>",
  [("Find the mean deviation about the mean of 6, 7, 10, 12, 13, 4, 8, 12.", ["x̄ = 72 ÷ 8 = 9", "Σ|x − 9| = 3 + 2 + 1 + 3 + 4 + 5 + 1 + 3 = 22", "22 ÷ 8"], "2.75")],
  ["Forgetting the absolute value in the mean deviation.", "Giving the variance when the question asks for the standard deviation.", "Adding a constant to σ when every value is increased."],
  [("Which is used more, mean deviation or standard deviation?", "Standard deviation, because it works well with further calculations."), ("Can the variance be negative?", "No. It is an average of squares.")],
  [("Range and mean deviation about the mean", [(one_md, 14), (one_var, 6)]),
   ("Mean deviation about the median", [(one_mdmed, 14), (one_freq, 6)]),
   ("Variance and standard deviation", [(one_var, 12), (sd_list, 8)]),
   ("Grouped data and shortcuts", [(one_freq, 8), (sd_sums, 12)]),
   ("Comparing and changing data", [(change, 12), (cmp_, 8)])], 911113)
