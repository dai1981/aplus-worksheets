# -*- coding: utf-8 -*-
"""
SG Secondary 4 Maths: Standard Deviation (MOE syllabus S1: range, interquartile range and standard deviation as
measures of spread; standard deviation for grouped and ungrouped data; comparing data with mean and SD)
  python3 tools/gen_sg_maths_s4_standard_deviation.py
Standard deviation of a list, using Σx and Σx², grouped data with mid-values, the effect of adding or multiplying
every value, and comparing two sets of data using the mean and standard deviation.
Answers are correct to 3 significant figures, as in O-Level papers.
Wrong answers come from real mistakes: forgetting the square root, dividing by n − 1 or not dividing at all,
squaring the mean before subtracting the wrong way, using class boundaries instead of mid-values, and thinking
that adding a constant changes the spread.
"""
import math
import random
from sg_sec import num, S, make, lesson, collect, T, table, MINUS, People

R = random.Random(840700)
P = People(R)


def sf3(x):
    if x == 0:
        return "0"
    d = 2 - int(math.floor(math.log10(abs(x))))
    v = round(x, d)
    s = ("%.*f" % (max(d, 0), v)) if d > 0 else num(int(round(v)))
    return s.replace("-", MINUS)


def sd(xs):
    m = sum(xs) / len(xs)
    return math.sqrt(sum((x - m) ** 2 for x in xs) / len(xs))


def distinct(right, wr, alt):
    out = []
    for w in wr + alt:
        if w != right and w not in out:
            out.append(w)
    return out[:3]


# ------------------------------------------------------------ set 1: SD of a list
def one_list(r):
    n = r.choice([5, 6, 7, 8])
    xs = [r.randint(2, 30) for _ in range(n)]
    m = sum(xs) / n
    s = sd(xs)
    if s < 1:
        return None
    var = s * s
    wr = [sf3(var), sf3(math.sqrt(sum((x - m) ** 2 for x in xs) / (n - 1))), sf3(math.sqrt(sum((x - m) ** 2 for x in xs)))]
    right = sf3(s)
    return T("Find the standard deviation of: %s. Give your answer correct to 3 significant figures." % ", ".join(map(str, xs)), right, distinct(right, wr, [sf3(s + 1)]),
             "Mean = %s ÷ %d = %s. SD = √(Σ(<i>x</i> − <i>x̄</i>)² ÷ <i>n</i>) = √(%s ÷ %d) = <b>%s</b>." % (num(sum(xs)), n, sf3(m), sf3(sum((x - m) ** 2 for x in xs)), n, right))


# ------------------------------------------------------------ set 2: using Σx and Σx²
def one_sums(r):
    n = r.choice([10, 12, 15, 20, 25, 40])
    xs = [r.randint(5, 40) for _ in range(n)]
    Sx, Sx2 = sum(xs), sum(x * x for x in xs)
    m = Sx / n
    s = math.sqrt(Sx2 / n - m * m)
    kind = r.choice(["sd", "sd", "mean"])
    if kind == "mean":
        right = sf3(m)
        return T("For a set of %d values, Σ<i>x</i> = %s and Σ<i>x</i>² = %s. Find the mean." % (n, num(Sx), num(Sx2)), right, distinct(right, [sf3(Sx2 / n), sf3(math.sqrt(Sx2 / n)), sf3(Sx / (n - 1))], [sf3(m + 1)]),
                 "Mean = Σ<i>x</i> ÷ <i>n</i> = %s ÷ %d = <b>%s</b>." % (num(Sx), n, right))
    right = sf3(s)
    return T("For a set of %d values, Σ<i>x</i> = %s and Σ<i>x</i>² = %s. Find the standard deviation, correct to 3 significant figures." % (n, num(Sx), num(Sx2)), right,
             distinct(right, [sf3(Sx2 / n - m * m), sf3(math.sqrt(Sx2 / n) - m), sf3(math.sqrt(abs(Sx2 - m * m) / n))], [sf3(s * 2)]),
             "SD = √(Σ<i>x</i>² ÷ <i>n</i> − (Σ<i>x</i> ÷ <i>n</i>)²) = √(%s ÷ %d − %s²) = <b>%s</b>." % (num(Sx2), n, sf3(m), right))


# ------------------------------------------------------------ set 3: grouped data
def one_group(r):
    w = r.choice([10, 5, 20])
    start = r.choice([0, 10, 20, 40]) if w != 20 else 0
    k = r.choice([4, 5])
    fs = [r.randint(2, 15) for _ in range(k)]
    mids = [start + w * i + w / 2 for i in range(k)]
    n = sum(fs)
    m = sum(f * x for f, x in zip(fs, mids)) / n
    s = math.sqrt(sum(f * (x - m) ** 2 for f, x in zip(fs, mids)) / n)
    kind = r.choice(["sd", "sd", "mean"])
    what = r.choice(["Time (min)", "Mass (kg)", "Distance (km)", "Score"])
    rows = [["%s &lt; <i>x</i> ≤ %s" % (num(start + w * i), num(start + w * (i + 1))), num(f)] for i, f in enumerate(fs)]
    tb = table([what, "Frequency"], rows)
    lows = [start + w * i for i in range(k)]
    if kind == "mean":
        right = sf3(m)
        wl = sum(f * x for f, x in zip(fs, lows)) / n
        return T("Estimate the mean of the grouped data, correct to 3 significant figures.%s" % tb, right, distinct(right, [sf3(wl), sf3(sum(mids) / k), sf3(m * k / n * 2)], [sf3(m + w / 2)]),
                 "Use the mid-values %s. Mean = Σ<i>fx</i> ÷ Σ<i>f</i> = %s ÷ %d = <b>%s</b>." % (", ".join("%g" % x for x in mids), "%g" % sum(f * x for f, x in zip(fs, mids)), n, right))
    right = sf3(s)
    sl = math.sqrt(sum(f * (x - m) ** 2 for f, x in zip(fs, lows)) / n)
    return T("Estimate the standard deviation of the grouped data, correct to 3 significant figures.%s" % tb, right,
             distinct(right, [sf3(s * s), sf3(math.sqrt(sum((x - sum(mids) / k) ** 2 for x in mids) / k)), sf3(sl * 1.15)], [sf3(s * 2)]),
             "Use mid-values. Σ<i>f</i> = %d, Σ<i>fx</i> = %s and Σ<i>fx</i>² = %s. SD = √(Σ<i>fx</i>² ÷ Σ<i>f</i> − mean²) = <b>%s</b>." % (
                 n, "%g" % sum(f * x for f, x in zip(fs, mids)), "%g" % sum(f * x * x for f, x in zip(fs, mids)), right))


# ------------------------------------------------------------ set 4: changing every value
def one_change(r):
    m = r.randint(20, 80)
    s = r.choice([2, 3, 4, 5, 6, 8, 1.5, 2.5])
    kind = r.choice(["add", "add", "mul", "both"])
    if kind == "add":
        c = r.choice([3, 5, 10, -4, 2])
        nm = r.choice(["Every mark is increased by %d." % c if c > 0 else "%d is taken away from every mark." % (-c)])
        return T("A set of marks has mean %d and standard deviation %g. %s What are the new mean and standard deviation?" % (m, s, nm),
                 "mean %d, SD %g" % (m + c, s), ["mean %d, SD %g" % (m + c, s + abs(c)), "mean %d, SD %g" % (m, s + abs(c)), "mean %d, SD %g" % (m, s)],
                 "%s the same amount for every value moves the mean by %d but does not change the spread: <b>mean %d, SD %g</b>." % ("Adding" if c > 0 else "Taking away", abs(c), m + c, s))
    if kind == "mul":
        k = r.choice([2, 3, 10])
        return T("A data set has mean %d and standard deviation %g. Every value is multiplied by %d. What is the new standard deviation?" % (m, s, k),
                 "%g" % (s * k), ["%g" % s, "%g" % (s * k * k), "%g" % (s + k)],
                 "Multiplying every value by %d multiplies the spread by %d: %g × %d = <b>%g</b>." % (k, k, s, k, s * k))
    k = r.choice([2, 3])
    c = r.choice([5, 10])
    return T("Values with mean %d and standard deviation %g are each multiplied by %d and then increased by %d. What are the new mean and standard deviation?" % (m, s, k, c),
             "mean %d, SD %g" % (m * k + c, s * k), ["mean %d, SD %g" % (m * k + c, s * k + c), "mean %d, SD %g" % ((m + c) * k, s * k), "mean %d, SD %g" % (m * k, s)],
             "Mean: %d × %d + %d = %d. SD: only the multiplication matters, %g × %d = %g. <b>mean %d, SD %g</b>." % (m, k, c, m * k + c, s, k, s * k, m * k + c, s * k))


# ------------------------------------------------------------ set 5: comparing two data sets
def one_cmp(r):
    groups = r.choice([("Class A", "Class B"), ("Machine X", "Machine Y"), ("Ahmad", "Wei Jie"), ("Team P", "Team Q")])
    m1, m2 = r.randint(40, 80), r.randint(40, 80)
    s1, s2 = r.choice([3, 4, 5, 6, 8, 10, 12]), r.choice([3, 4, 5, 6, 8, 10, 12])
    if m1 == m2 or s1 == s2:
        return None
    tb = table(["", "Mean", "Standard deviation"], [[groups[0], num(m1), num(s1)], [groups[1], num(m2), num(s2)]])
    kind = r.choice(["avg", "cons", "cons", "both"])
    if kind == "avg":
        g = groups[0] if m1 > m2 else groups[1]
        return T("Which group did better on average?%s" % tb, "%s, because its mean is higher" % g,
                 ["%s, because its standard deviation is higher" % (groups[0] if s1 > s2 else groups[1]), "%s, because its mean is lower" % (groups[1] if g == groups[0] else groups[0]), "You cannot tell without the range"],
                 "Compare the means: %d and %d. <b>%s</b> has the higher mean." % (m1, m2, g))
    if kind == "cons":
        g = groups[0] if s1 < s2 else groups[1]
        return T("Which group's results were more consistent?%s" % tb, "%s, because its standard deviation is smaller" % g,
                 ["%s, because its standard deviation is larger" % (groups[1] if g == groups[0] else groups[0]), "%s, because its mean is higher" % (groups[0] if m1 > m2 else groups[1]), "Both are equally consistent"],
                 "Consistency is about spread. The smaller standard deviation (%d vs %d) means the results are closer to the mean: <b>%s</b>." % (min(s1, s2), max(s1, s2), g))
    hi = groups[0] if m1 > m2 else groups[1]
    cons = groups[0] if s1 < s2 else groups[1]
    right = "%s scored higher on average; %s was more consistent" % (hi, cons)
    return T("Which statement best compares the two groups?%s" % tb, right,
             ["%s scored higher on average; %s was more consistent" % (cons if cons != hi else (groups[1] if hi == groups[0] else groups[0]), hi if cons != hi else (groups[1] if hi == groups[0] else groups[0])),
              "%s was more consistent because its mean is higher" % hi, "The group with the larger standard deviation was more consistent"],
             "Higher mean → better on average (%s). Smaller standard deviation → more consistent (%s). <b>%s</b>." % (hi, cons, right))


def build():
    sets = [S("Standard deviation of a list", collect(one_list, 20, R)),
            S("Using Σx and Σx²", collect(one_sums, 20, R)),
            S("Grouped data", collect(one_group, 20, R)),
            S("Adding to or multiplying every value", collect(one_change, 20, R)),
            S("Comparing data sets", collect(one_cmp, 20, R))]
    body = lesson(
        "<ul><li>The <b>standard deviation</b> measures how spread out the data is from the mean.</li>"
        "<li>SD = √(Σ(<i>x</i> − <i>x̄</i>)² ÷ <i>n</i>) = √(Σ<i>x</i>² ÷ <i>n</i> − <i>x̄</i>²).</li>"
        "<li>For <b>grouped data</b>, use the mid-value of each class: SD = √(Σ<i>fx</i>² ÷ Σ<i>f</i> − <i>x̄</i>²).</li>"
        "<li>Adding a constant to every value does not change the SD; multiplying every value by <i>k</i> multiplies the SD by <i>k</i>.</li>"
        "<li>To compare data sets: a higher mean is better on average; a smaller SD is more consistent.</li></ul>",
        [("Find the SD of 2, 4, 4, 4, 5, 5, 7, 9.", ["Mean = 40 ÷ 8 = 5", "Σ(x − 5)² = 32", "√(32 ÷ 8)"], "2"),
         ("For 10 values, Σx = 50 and Σx² = 340. Find the SD.", ["Mean = 5", "√(340 ÷ 10 − 5²) = √9"], "3")],
        ["Forgetting the square root (that gives the variance).",
         "Dividing by n − 1 or forgetting to divide by n.",
         "Using class boundaries instead of mid-values for grouped data.",
         "Thinking that adding a number to every value changes the standard deviation."])
    faq = [("What does the standard deviation tell you?", "How far, on average, the values are from the mean. A small SD means the data is close together; a large SD means it is spread out."),
           ("Which formula should I use?", "SD = √(Σx²/n − x̄²) is quickest when you are given Σx and Σx², or when using a calculator. For grouped data use Σfx² and Σf with mid-values."),
           ("What happens to the SD if I add 5 to every value?", "Nothing. The whole data set shifts, but the spread stays the same. Only the mean increases by 5."),
           ("How do I compare two data sets?", "Use the mean to compare the average and the standard deviation to compare consistency. The smaller SD is more consistent.")]
    make(4, "standard-deviation", 7, "S1",
         "Standard Deviation: Ungrouped and Grouped Data",
         "", "Standard deviation", "",
         "Free Secondary 4 maths worksheets on standard deviation: lists of data, Σx and Σx² formulas, grouped data with mid-values, transformations and comparing data sets with mean and SD. 100 questions with answers.",
         "SD = √(Σx²/n − x̄²): it measures spread about the mean.",
         "Higher mean = better on average; smaller SD = more consistent.",
         body, faq, sets, R)


if __name__ == "__main__":
    build()
