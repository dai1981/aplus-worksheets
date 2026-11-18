# -*- coding: utf-8 -*-
"""
US Algebra 2: The Normal Distribution (Common Core S-ID.A.4)
  python3 tools/gen_us_math_a2_normal_distribution.py
The 68-95-99.7 rule, z-scores, comparing values with z-scores, areas from z-scores, and word problems
with heights, test scores and machine fills.
Wrong answers come from real mistakes: using 68% for two standard deviations, forgetting to halve for one
tail, dividing by the variance instead of the standard deviation, and subtracting in the wrong order.
"""
import math
import random
from fractions import Fraction as F
from us_hs import B, S, make, lesson, collect, T, num, MINUS, People
from a2_common import sf

R = random.Random(96501)


def phi(z):
    return 0.5 * (1 + math.erf(z / math.sqrt(2)))


def zs(z):
    t = ("%.3f" % abs(z)).rstrip("0").rstrip(".")
    return (MINUS if z < 0 else "") + t


def pc(x):
    s = ("%.2f" % x).rstrip("0").rstrip(".")
    return s + "%"


# ------------------------------------------------------------ set 1: the 68-95-99.7 rule
def one_rule(r):
    mu, sd = r.choice([(100, 15), (70, 5), (50, 10), (500, 100), (68, 3), (12, 2), (200, 25), (30, 4)])
    kind = r.choice(["within", "within", "above", "below", "between"])
    if kind == "within":
        k = r.choice([1, 2, 3])
        ans = {1: 68, 2: 95, 3: 99.7}[k]
        q = "A normal distribution has mean %s and standard deviation %s. What percent of the data is between %s and %s?" % (num(mu), num(sd), num(mu - k * sd), num(mu + k * sd))
        wr = [x for x in [68, 95, 99.7, 34, 47.5] if x != ans][:3]
        return T(q, pc(ans), [pc(w) for w in wr], "%s and %s are %d standard deviation%s from the mean, so the rule gives <b>%s</b>." % (num(mu - k * sd), num(mu + k * sd), k, "" if k == 1 else "s", pc(ans)))
    if kind == "above":
        k = r.choice([1, 2])
        ans = {1: 16, 2: 2.5}[k]
        q = "A normal distribution has mean %s and standard deviation %s. What percent of the data is above %s?" % (num(mu), num(sd), num(mu + k * sd))
        wr = {1: [32, 34, 68], 2: [5, 47.5, 95]}[k]
        return T(q, pc(ans), [pc(w) for w in wr],
                 "%s is %d SD above the mean. %s%% is within %d SD, so %s%% is outside, split equally between the two tails: <b>%s</b>." % (
                     num(mu + k * sd), k, {1: "68", 2: "95"}[k], k, {1: "32", 2: "5"}[k], pc(ans)))
    if kind == "below":
        k = r.choice([1, 2])
        ans = {1: 84, 2: 97.5}[k]
        q = "A normal distribution has mean %s and standard deviation %s. What percent of the data is below %s?" % (num(mu), num(sd), num(mu + k * sd))
        wr = {1: [68, 34, 16], 2: [95, 47.5, 2.5]}[k]
        return T(q, pc(ans), [pc(w) for w in wr],
                 "Half the data (50%%) is below the mean, and %s between the mean and %s. Total: <b>%s</b>." % (pc({1: 34, 2: 47.5}[k]), num(mu + k * sd), pc(ans)))
    q = "A normal distribution has mean %s and standard deviation %s. What percent of the data is between %s and %s?" % (num(mu), num(sd), num(mu - sd), num(mu + 2 * sd))
    return T(q, pc(81.5), [pc(95), pc(68), pc(47.5)], "From %s SD to the mean: 34%%. From the mean to +2 SD: 47.5%%. Total: <b>81.5%%</b>." % (MINUS + "1"))


# ------------------------------------------------------------ set 2: z-scores
def one_z(r):
    mu, sd = r.choice([(100, 15), (70, 5), (50, 10), (500, 100), (68, 3), (80, 8), (200, 25), (30, 4), (75, 6)])
    z = F(r.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6]), r.choice([2, 2, 1, 4]))
    x = mu + z * sd
    if x.denominator > 4:
        return None
    if r.random() < 0.65:
        q = "A data set has mean %s and standard deviation %s. Find the <i>z</i>-score of %s." % (num(mu), num(sd), num(x))
        wr = [-z, (x - mu) / (sd * sd), x - mu, z * 2]
        return T(q, num(z), [num(w) for w in dict.fromkeys(wr) if w != z][:3],
                 "<i>z</i> = (<i>x</i> %s μ) ÷ σ = (%s %s %s) ÷ %s = <b>%s</b>." % (MINUS, num(x), MINUS, num(mu), num(sd), num(z)))
    q = "A data set has mean %s and standard deviation %s. Which value has a <i>z</i>-score of %s?" % (num(mu), num(sd), num(z))
    wr = [mu - z * sd, mu + z, z * sd]
    return T(q, num(x), [num(w) for w in dict.fromkeys(wr) if w != x][:3],
             "<i>x</i> = μ + <i>z</i>σ = %s + (%s)(%s) = <b>%s</b>." % (num(mu), num(z), num(sd), num(x)))


# ------------------------------------------------------------ set 3: compare with z-scores
def one_cmp(r):
    pp = People(r)
    n1, h1, s1 = pp.next()
    n2, h2, s2 = pp.next()
    a = (r.choice([70, 75, 80]), r.choice([5, 8, 10]))
    b = (r.choice([500, 520, 480]), r.choice([90, 100, 110]))
    za = F(r.choice([2, 3, 4, 5, 6]), 4)
    zb = F(r.choice([2, 3, 4, 5, 6, 7]), 4)
    if za == zb:
        return None
    xa, xb = a[0] + za * a[1], b[0] + zb * b[1]
    if xa.denominator > 1 or xb.denominator > 1:
        return None
    q = ("%s scored %s on a test with mean %d and standard deviation %d. %s scored %s on a different test with mean %d and standard deviation %d. "
         "Who did better compared with the other students who took the same test?" % (n1, num(xa), a[0], a[1], n2, num(xb), b[0], b[1]))
    right = n1 if za > zb else n2
    third = "%s, because %s is the larger score" % (n2, num(xb)) if right == n1 else "The tests cannot be compared"
    return T(q, right, [n2 if right == n1 else n1, "They did equally well", third],
             "Compare <i>z</i>-scores: %s has <i>z</i> = %s and %s has <i>z</i> = %s. The larger <i>z</i>-score is relatively better. <b>%s</b>." % (n1, num(za), n2, num(zb), right))


# ------------------------------------------------------------ set 4: areas from z-scores
def one_area(r):
    z = r.choice([0.5, 1.2, 1.5, 0.8, 1.0, 2.0, -0.5, -1.2, -1.5, -0.8, 1.96, 1.645])
    kind = r.choice(["below", "above", "between"])
    if kind == "below":
        p = phi(z)
        q = "For a standard normal distribution, what is P(<i>z</i> &lt; %s)? Round to four decimal places." % zs(z)
        right = "%.4f" % p
        wr = ["%.4f" % (1 - p), "%.4f" % abs(p - 0.5), "%.4f" % (2 * p - 1 if p > 0.5 else 1 - 2 * p)]
        e = "Use the normal CDF (or a <i>z</i>-table): the area to the left of %s is <b>%s</b>." % (zs(z), right)
    elif kind == "above":
        p = 1 - phi(z)
        q = "For a standard normal distribution, what is P(<i>z</i> &gt; %s)? Round to four decimal places." % zs(z)
        right = "%.4f" % p
        wr = ["%.4f" % (1 - p), "%.4f" % abs(0.5 - p), "%.4f" % (p / 2)]
        e = "Area to the right = 1 %s (area to the left) = 1 %s %.4f = <b>%s</b>." % (MINUS, MINUS, phi(z), right)
    else:
        z = abs(z)
        p = phi(z) - phi(-z)
        q = "For a standard normal distribution, what is P(%s%s &lt; <i>z</i> &lt; %s)? Round to four decimal places." % (MINUS, zs(z), zs(z))
        right = "%.4f" % p
        wr = ["%.4f" % phi(z), "%.4f" % (1 - p), "%.4f" % (p / 2)]
        e = "Area between = %.4f %s %.4f = <b>%s</b>." % (phi(z), MINUS, phi(-z), right)
    return T(q, right, [w for w in dict.fromkeys(wr) if w != right][:3], e)


# ------------------------------------------------------------ set 5: word problems
def one_word(r):
    kind = r.choice(["height", "fill", "score", "life", "cut"])
    if kind == "height":
        mu, sd = r.choice([(64, 3), (69, 3), (66, 2)])
        k = r.choice([1, 2])
        q = "Adult heights in a group are normally distributed with mean %d in. and standard deviation %d in. About what percent are taller than %d in.?" % (mu, sd, mu + k * sd)
        ans = {1: 16, 2: 2.5}[k]
        return T(q, pc(ans), [pc(w) for w in {1: [32, 34, 84], 2: [5, 47.5, 97.5]}[k]],
                 "%d in. is %d SD above the mean, so <b>%s</b> are taller." % (mu + k * sd, k, pc(ans)))
    if kind == "fill":
        mu, sd = r.choice([(500, 4), (355, 2), (1000, 10), (250, 3)])
        lo, hi = mu - 2 * sd, mu + 2 * sd
        n = r.choice([1000, 2000, 5000])
        q = "A machine fills bottles with a mean of %d mL and a standard deviation of %d mL. Out of %s bottles, about how many hold between %d mL and %d mL?" % (mu, sd, num(n), lo, hi)
        ans = round(0.95 * n)
        return T(q, num(ans), [num(round(0.68 * n)), num(round(0.475 * n)), num(round(0.997 * n))],
                 "%d and %d are 2 SD from the mean, so about 95%% of the bottles: 0.95 × %s = <b>%s</b>." % (lo, hi, num(n), num(ans)))
    if kind == "score":
        mu, sd = r.choice([(500, 100), (75, 8), (100, 15)])
        x = mu + r.choice([1, 2]) * sd
        pct = 84 if x == mu + sd else 97.5
        q = "Test scores are normally distributed with mean %d and standard deviation %d. A student scores %d. About what percentile is this?" % (mu, sd, x)
        return T(q, "About the %s percentile" % ("84th" if pct == 84 else "97.5th"), ["About the 68th percentile" if pct == 84 else "About the 95th percentile",
                                                                                     "About the 16th percentile" if pct == 84 else "About the 2.5th percentile", "About the 50th percentile"],
                 "%d is %d SD above the mean, and %s of scores are below it. <b>About the %s percentile</b>." % (x, 1 if pct == 84 else 2, pc(pct), "84th" if pct == 84 else "97.5th"))
    if kind == "life":
        mu, sd = r.choice([(1000, 100), (800, 50), (50, 5)])
        x = mu - sd
        q = "Light bulb lifetimes are normally distributed with mean %s hours and standard deviation %s hours. What is the probability that a bulb lasts less than %s hours?" % (num(mu), num(sd), num(x))
        return T(q, "About 0.16", ["About 0.34", "About 0.68", "About 0.32"],
                 "%s is 1 SD below the mean. 34%% is between it and the mean, so 50%% %s 34%% = 16%% is below it. <b>About 0.16</b>." % (num(x), MINUS))
    mu, sd = r.choice([(70, 10), (500, 100), (60, 8)])
    q = "Exam scores are normal with mean %d and standard deviation %d. The top 2.5%% earn an award. What is the lowest score that earns it?" % (mu, sd)
    ans = mu + 2 * sd
    return T(q, num(ans), [num(mu + sd), num(mu + 3 * sd), num(mu - 2 * sd)],
             "The top 2.5%% is above 2 standard deviations over the mean: %d + 2(%d) = <b>%d</b>." % (mu, sd, ans))


def build():
    sets = [S("The 68-95-99.7 rule", collect(one_rule, 20, R)),
            S("z-scores", collect(one_z, 20, R)),
            S("Compare with z-scores", collect(one_cmp, 20, R)),
            S("Areas under the normal curve", collect(one_area, 20, R)),
            S("Word problems", collect(one_word, 20, R))]
    body = lesson(
        "<p>A <b>normal distribution</b> is a symmetric, bell-shaped curve centered at the mean μ. Its spread is the standard deviation σ.</p>"
        "<p><b>Empirical rule</b>: about 68%% of the data is within 1σ of the mean, 95%% within 2σ, and 99.7%% within 3σ. Each tail outside 1σ holds 16%%, and outside 2σ holds 2.5%%.</p>"
        "<p>A <b><i>z</i>-score</b> tells how many standard deviations a value is from the mean: <i>z</i> = (<i>x</i> %s μ) ÷ σ. "
        "Use <i>z</i>-scores to compare values from different distributions, and a normal CDF or <i>z</i>-table to find areas.</p>" % MINUS,
        [("IQ scores: μ = 100, σ = 15. What percent are above 130?", ["130 is 2σ above the mean", "Outside 2σ is 5%%, half in each tail"], "2.5%%"),
         ("Find the <i>z</i>-score of 82 when μ = 70 and σ = 8.", ["(82 %s 70) ÷ 8" % MINUS], "1.5")],
        ["Using 68%% for 2 standard deviations. 68%% is for 1, 95%% is for 2.",
         "Forgetting to split the outside percent between the two tails.",
         "Dividing by the variance σ² instead of σ.",
         "Comparing raw scores from different tests instead of <i>z</i>-scores."])
    body = body.replace("%%", "%")
    faq = [("What is the empirical rule?", "In a normal distribution, about 68% of values are within 1 standard deviation of the mean, 95% within 2, and 99.7% within 3."),
           ("How do you find a z-score?", "Subtract the mean from the value and divide by the standard deviation: z = (x − μ)/σ."),
           ("What does a negative z-score mean?", "The value is below the mean. For example, z = −1.5 is 1.5 standard deviations below the mean."),
           ("How do you find the probability from a z-score?", "Use a z-table or a calculator's normal CDF to find the area to the left; subtract from 1 for the area to the right.")]
    make("normal-distribution", 15, "S-ID.A.4",
         "The Normal Distribution and z-Scores",
         "Normal Distribution Worksheet: Empirical Rule and z-Scores (Algebra 2, S-ID.A.4) | 100 Questions",
         "Normal Distribution",
         "Use the mean and standard deviation of a data set to fit it to a normal distribution and to estimate population percentages. Recognize that there are data sets for which such a procedure is not appropriate. Use calculators, spreadsheets, and tables to estimate areas under the normal curve.",
         "Free Algebra 2 worksheet on the normal distribution: the 68-95-99.7 rule, z-scores, comparing values, areas under the curve and word problems. 100 questions with answers.",
         "68% within 1 SD, 95% within 2 SD, 99.7% within 3 SD.",
         "z = (x − μ)/σ tells how many standard deviations x is from the mean.",
         body, faq, sets, R, domain="Statistics and Probability", grade="algebra-2")


if __name__ == "__main__":
    build()
