# -*- coding: utf-8 -*-
"""
US Algebra 1: Box Plots and Standard Deviation (Common Core S-ID.A.1, S-ID.A.2, S-ID.A.3)
  python3 tools/gen_us_math_a1_box_plots_and_standard_deviation.py
The five-number summary and interquartile range, reading box plots, outliers with the 1.5 × IQR rule and
their effect on the mean and median, standard deviation (meaning, small calculations and the effect of adding
or multiplying), and comparing distributions by shape, center and spread.
Wrong answers come from real mistakes: finding quartiles without ordering the data, giving the range instead
of the IQR, reading the whiskers as quartiles, thinking an outlier pulls the median as much as the mean, and
thinking adding a constant changes the spread.
"""
import random
from fractions import Fraction as F
from math import sqrt
from us_hs import num, B, S, make, lesson, collect, T, QN, svg_wrap, line, text, fig, INK, BLUE, dec

R = random.Random(91901)


def nv(v):
    v = F(v)
    return num(v) if v.denominator == 1 else dec(v)


def median(xs):
    s = sorted(xs)
    n = len(s)
    return F(s[n // 2]) if n % 2 else F(s[n // 2 - 1] + s[n // 2], 2)


def five(xs):
    s = sorted(xs)
    n = len(s)
    lo, hi = s[:n // 2], s[(n + 1) // 2:]
    return s[0], median(lo), median(s), median(hi), s[-1]


def box_svg(mn, q1, md, q3, mx, lo, hi, step, label="box plot"):
    W, x0 = 420, 24
    u = (W - 2 * x0) / (hi - lo)
    Xp = lambda v: x0 + (float(v) - lo) * u
    y, bh = 34, 30
    s = [line(x0 - 6, 84, W - x0 + 6, 84, INK, 1.8)]
    v = lo
    while v <= hi:
        s.append(line(Xp(v), 80, Xp(v), 88, INK, 1.5))
        s.append(text(Xp(v), 104, num(v), 12, weight=400))
        v += step
    s.append(line(Xp(mn), y, Xp(q1), y, INK, 2))
    s.append(line(Xp(q3), y, Xp(mx), y, INK, 2))
    s.append(line(Xp(mn), y - 9, Xp(mn), y + 9, INK, 2))
    s.append(line(Xp(mx), y - 9, Xp(mx), y + 9, INK, 2))
    s.append("<rect x='%.1f' y='%d' width='%.1f' height='%d' fill='#dbe8f6' stroke='%s' stroke-width='2'/>" % (Xp(q1), y - bh // 2, Xp(q3) - Xp(q1), bh, BLUE))
    s.append(line(Xp(md), y - bh // 2, Xp(md), y + bh // 2, BLUE, 3))
    return svg_wrap(W, 114, "".join(s), label)


def uniq(right, wr):
    out = [w for w in dict.fromkeys(wr) if w != right]
    return out[:3] if len(out) >= 3 else None


# ------------------------------------------------------------ set 1: five-number summary and IQR
def one_five(r):
    n = r.choice([8, 9, 11, 12])
    xs = [r.randint(10, 60) for _ in range(n)]
    mn, q1, md, q3, mx = five(xs)
    data = ", ".join(num(x) for x in xs)
    kind = r.choice(["med", "q1", "q3", "iqr", "iqr"])
    s = sorted(xs)
    if kind == "med":
        q = "Find the median of: %s." % B(data)
        right = nv(md)
        wr = uniq(right, [nv(median(xs[:])) if False else nv(F(xs[n // 2])), nv(F(sum(xs), n)) if F(sum(xs), n).denominator in (1, 2, 4, 5) else nv(md + 1), nv(F(mn + mx, 2)), nv(q3)])
        e = "Order the data: %s. The middle value is <b>%s</b>." % (", ".join(num(x) for x in s), right)
    elif kind in ("q1", "q3"):
        val = q1 if kind == "q1" else q3
        q = "Find the %s quartile (%s) of: %s." % ("first" if kind == "q1" else "third", "Q1" if kind == "q1" else "Q3", B(data))
        right = nv(val)
        wr = uniq(right, [nv(q3 if kind == "q1" else q1), nv(md), nv(median(xs[:n // 2]) if kind == "q1" else median(xs[(n + 1) // 2:])), nv(mn if kind == "q1" else mx)])
        e = "Order the data: %s. %s is the median of the %s half: <b>%s</b>." % (", ".join(num(x) for x in s), "Q1" if kind == "q1" else "Q3", "lower" if kind == "q1" else "upper", right)
    else:
        q = "Find the interquartile range (IQR) of: %s." % B(data)
        right = nv(q3 - q1)
        wr = uniq(right, [nv(mx - mn), nv(q3 - md), nv(median(xs[(n + 1) // 2:]) - median(xs[:n // 2])), nv(q3 - q1 + 2)])
        e = "Order the data: %s. Q1 = %s and Q3 = %s, so IQR = Q3 − Q1 = <b>%s</b>." % (", ".join(num(x) for x in s), nv(q1), nv(q3), right)
    if not wr:
        return None
    return T(q, right, wr, e)


# ------------------------------------------------------------ set 2: read a box plot
def one_box(r):
    lo = r.choice([0, 10, 20, 40])
    step = r.choice([5, 10])
    hi = lo + step * 10
    pts = sorted(r.sample(range(lo + step // 5, hi, step // 5 if step == 10 else 1), 5)) if False else None
    mn = lo + r.randint(0, 2) * step // 2 * 1
    mn = lo + step * r.randint(0, 2)
    q1 = mn + step * r.randint(1, 2)
    md = q1 + step * r.randint(1, 2)
    q3 = md + step * r.randint(1, 3)
    mx = q3 + step * r.randint(1, 3)
    if mx > hi:
        return None
    g = fig(box_svg(mn, q1, md, q3, mx, lo, hi, step))
    ctx = r.choice(["test scores", "minutes spent on homework", "heights of plants in cm", "ages of people at a concert"])
    kind = r.choice(["med", "iqr", "range", "pct", "pct2", "q3"])
    if kind == "med":
        q = "The box plot shows %s. What is the median?%s" % (ctx, g)
        right, wr = num(md), [num(q1), num(q3), num((mn + mx) // 2) if (mn + mx) // 2 != md else num(md + step)]
        e = "The median is the line inside the box: <b>%s</b>." % right
    elif kind == "q3":
        q = "The box plot shows %s. What is the third quartile?%s" % (ctx, g)
        right, wr = num(q3), [num(mx), num(md), num(q1)]
        e = "Q3 is the right edge of the box: <b>%s</b>." % right
    elif kind == "iqr":
        q = "The box plot shows %s. What is the interquartile range?%s" % (ctx, g)
        right, wr = num(q3 - q1), [num(mx - mn), num(q3 - md), num(md - q1) if md - q1 != q3 - md else num(q3)]
        e = "IQR = Q3 − Q1 = %s − %s = <b>%s</b>: the width of the box." % (num(q3), num(q1), right)
    elif kind == "range":
        q = "The box plot shows %s. What is the range?%s" % (ctx, g)
        right, wr = num(mx - mn), [num(q3 - q1), num(mx), num(mx - md)]
        e = "Range = maximum − minimum = %s − %s = <b>%s</b>." % (num(mx), num(mn), right)
    elif kind == "pct":
        q = "The box plot shows %s. About what percent of the data is between %s and %s?%s" % (ctx, num(q1), num(q3), g)
        right, wr = "50%", ["25%", "75%", "100%"]
        e = "The box holds the middle half of the data: <b>50%</b>."
    else:
        q = "The box plot shows %s. About what percent of the data is greater than %s?%s" % (ctx, num(q1), g)
        right, wr = "75%", ["25%", "50%", "100%"]
        e = "25% of the data is below Q1, so <b>75%</b> is above it."
    wr = uniq(right, wr)
    if not wr:
        return None
    return T(q, right, wr, e)


# ------------------------------------------------------------ set 3: outliers
def one_out(r):
    n = r.choice([8, 9, 11])
    xs = [r.randint(20, 40) for _ in range(n - 1)]
    big = r.choice([75, 80, 90, 95, 110])
    xs2 = xs + [big]
    mn, q1, md, q3, mx = five(xs2)
    iqr = q3 - q1
    fence = q3 + F(3, 2) * iqr
    kind = r.choice(["fence", "is", "mean", "median"])
    data = ", ".join(num(x) for x in sorted(xs2))
    if kind == "fence":
        q = "For the data %s, Q1 = %s and Q3 = %s. What is the upper fence, Q3 + 1.5 × IQR?" % (B(data), nv(q1), nv(q3))
        right = nv(fence)
        wr = uniq(right, [nv(q3 + iqr), nv(q3 + F(3, 2) * (mx - mn)), nv(F(3, 2) * iqr)])
        e = "IQR = %s − %s = %s. Upper fence = %s + 1.5 × %s = <b>%s</b>." % (nv(q3), nv(q1), nv(iqr), nv(q3), nv(iqr), right)
    elif kind == "is":
        if big <= fence:
            return None
        q = "Is %s an outlier in the data %s? (Use the 1.5 × IQR rule.)" % (num(big), B(data))
        right = "Yes, it is above %s" % nv(fence)
        wr = ["No, it is inside the box", "No, only values below Q1 can be outliers", "Yes, because it is the largest value"]
        e = "Q1 = %s, Q3 = %s, IQR = %s. Upper fence = %s + 1.5 × %s = %s. %s is above it: <b>yes</b>." % (nv(q1), nv(q3), nv(iqr), nv(q3), nv(iqr), nv(fence), num(big))
    elif kind == "mean":
        m1, m2 = F(sum(xs), len(xs)), F(sum(xs2), len(xs2))
        if m1.denominator not in (1, 2, 4, 5, 10) or m2.denominator not in (1, 2, 4, 5, 10):
            return None
        q = "The data %s has a mean of %s. The value %s is added. What is the new mean?" % (B(", ".join(num(x) for x in sorted(xs))), nv(m1), num(big))
        right = nv(m2)
        wr = uniq(right, [nv(m1 + big), nv(F(m1 + big, 2)), nv(F(sum(xs2), len(xs)))])
        e = "New total = %s + %s = %s, divided by %d: <b>%s</b>. One outlier moves the mean a lot." % (num(sum(xs)), num(big), num(sum(xs2)), len(xs2), right)
    else:
        q = "The value %s is added to the data %s. How does the median change compared with the mean?" % (num(big), B(", ".join(num(x) for x in sorted(xs))))
        right = "The median changes a little; the mean increases a lot"
        wr = ["The median increases a lot; the mean barely changes", "Both increase by the same amount", "Neither changes"]
        e = "The median only moves to the next middle value (%s → %s), but the mean is pulled up by the large value. <b>The median is resistant to outliers.</b>" % (nv(median(xs)), nv(median(xs2)))
    if not wr:
        return None
    return T(q, right, wr, e)


# ------------------------------------------------------------ set 4: standard deviation
SETS = [[2, 4, 4, 4, 5, 5, 7, 9], [1, 3, 5, 7, 9], [10, 10, 10, 10], [6, 8, 10, 12, 14], [3, 7, 7, 19], [5, 5, 9, 9], [2, 6, 10, 14], [4, 8, 12]]


def one_sd(r):
    kind = r.choice(["calc", "compare", "shift", "scale", "zero"])
    if kind == "calc":
        xs = r.choice([[2, 4, 4, 4, 5, 5, 7, 9], [5, 5, 9, 9], [3, 7, 7, 19], [1, 1, 7, 7], [10, 12, 14, 16, 18]])
        k = r.choice([0, 10, 20])
        xs = [x + k for x in xs]
        m = F(sum(xs), len(xs))
        var = sum((x - m) ** 2 for x in xs) / len(xs)
        sd = sqrt(var)
        q = "Find the (population) standard deviation of %s." % B(", ".join(num(x) for x in xs))
        right = nv(F(round(sd * 100), 100))
        wr = uniq(right, [nv(var), nv(F(round(sqrt(var * len(xs) / (len(xs) - 1)) * 100), 100)), nv(F(sum(abs(x - m) for x in xs), len(xs)))])
        e = "Mean = %s. Squared deviations average to %s, so the standard deviation is √%s %s <b>%s</b>." % (nv(m), nv(var), nv(var), "=" if abs(sd - round(sd)) < 1e-9 else "≈", right)
        if not wr:
            return None
        return T(q, right, wr, e)
    if kind == "compare":
        a = [50, 50, 51, 49, 50]
        b = [30, 70, 45, 55, 50]
        q = "Set A: %s. Set B: %s. Which has the larger standard deviation?" % (B(", ".join(map(str, a))), B(", ".join(map(str, b))))
        return T(q, "Set B", ["Set A", "They are equal", "You cannot tell without a calculator"], "Both have mean 50, but set B's values are much farther from 50: <b>set B</b>.")
    if kind == "shift":
        k = r.choice([5, 10, 20])
        sd = r.choice([3, 4, 6, 8])
        q = "A data set has a standard deviation of %d. Every value is increased by %d. What is the new standard deviation?" % (sd, k)
        return T(q, num(sd), [num(sd + k), num(sd * k), num(0)], "Adding the same amount moves every value but not the spread: <b>%d</b>. (The mean increases by %d.)" % (sd, k))
    if kind == "scale":
        k = r.choice([2, 3, 10])
        sd = r.choice([2, 3, 4, 5])
        q = "A data set has a standard deviation of %d. Every value is multiplied by %d. What is the new standard deviation?" % (sd, k)
        return T(q, num(sd * k), [num(sd), num(sd + k), num(sd * k * k)], "Multiplying every value by %d stretches the spread by %d: <b>%d</b>." % (k, k, sd * k))
    q = "Which data set has a standard deviation of 0?"
    v = r.randint(3, 20)
    return T(q, "%d, %d, %d, %d" % (v, v, v, v), ["%d, %d, %d, %d" % (v, v + 1, v, v + 1), "0, 0, 1, 1", ", ".join(num(t) for t in (-v, v, -v, v))], "Every value equals the mean, so there is <b>no spread</b>.")


# ------------------------------------------------------------ set 5: comparing distributions
def problems():
    data = [
        ("A data set is skewed right (a long tail of high values). Which is usually larger?", "The mean", ["The median", "They are always equal", "The mode"], "The high values pull the mean up: <b>the mean</b> is larger."),
        ("Which measures of center and spread are best for a skewed data set with outliers?", "Median and IQR", ["Mean and standard deviation", "Mode and range", "Mean and range"], "The median and IQR are not affected much by outliers: <b>median and IQR</b>."),
        ("Which measures are best for a symmetric data set with no outliers?", "Mean and standard deviation", ["Median and IQR", "Mode and range", "Minimum and maximum"], "For symmetric data the <b>mean and standard deviation</b> describe it well."),
        ("Class A's test scores have mean 78 and SD 4. Class B's have mean 78 and SD 12. What does this tell you?", "Class B's scores are more spread out", ["Class B did better", "Class A did better", "The classes are identical"], "Same center, but a larger SD means <b>more spread</b>."),
        ("Two box plots have the same median, but box A is twice as wide as box B. What does this mean?", "The middle half of A is more spread out", ["A has a higher median", "A has more data values", "B has outliers"], "The box width is the IQR: <b>A's middle half is more spread out</b>."),
        ("In a normal (bell-shaped) distribution, about what percent of data is within 1 standard deviation of the mean?", "68%", ["50%", "95%", "99.7%"], "The 68–95–99.7 rule: about <b>68%</b> within 1 SD."),
        ("Heights of adult women have mean 64 in. and SD 2.5 in. About 95% of women are between which heights?", "59 in. and 69 in.", ["61.5 in. and 66.5 in.", "56.5 in. and 71.5 in.", "62 in. and 66 in."], "95% is within 2 SD: 64 ± 5 → <b>59 to 69 in.</b>"),
        ("Which graph best shows the five-number summary?", "A box plot", ["A histogram", "A circle graph", "A scatter plot"], "A <b>box plot</b> shows the minimum, Q1, median, Q3 and maximum."),
        ("Which graph best shows the shape of a large data set?", "A histogram", ["A box plot only", "A table", "A line graph of time"], "A <b>histogram</b> shows how the data is distributed (peaks, skew and gaps)."),
        ("A store's daily sales: mean $2,400, median $1,900. What shape is the distribution likely to be?", "Skewed right", ["Skewed left", "Symmetric", "Uniform"], "The mean is greater than the median, so a few very high days pull it up: <b>skewed right</b>."),
        ("A teacher adds 5 points to every test score. What happens to the median and IQR?", "The median goes up 5; the IQR stays the same", ["Both go up 5", "Both stay the same", "The median stays the same; the IQR goes up 5"], "Adding a constant shifts the center but not the spread."),
        ("Which data set has the larger IQR: A: Q1 = 20, Q3 = 35; B: Q1 = 15, Q3 = 25?", "A", ["B", "They are equal", "You need the medians"], "A: 15. B: 10. <b>A</b>."),
        ("The ages at a children's party are 5, 6, 6, 7, 7, 7, 8 and one adult aged 38. Which measure of center describes a typical age best?", "The median", ["The mean", "The range", "The maximum"], "The adult is an outlier that pulls the mean up to 10.5; the median 7 is more typical."),
        ("What does a standard deviation of 0 mean?", "All the values are the same", ["The mean is 0", "There are no data values", "The data is skewed"], "No value is away from the mean: <b>all the values are the same</b>."),
        ("Two classes have these quiz scores. Class A: median 8, IQR 2. Class B: median 7, IQR 5. Which statement is true?", "Class A scored higher and more consistently", ["Class B scored higher", "Class B was more consistent", "The classes are the same"], "Higher median and smaller IQR: <b>Class A scored higher and more consistently</b>."),
        ("Which is NOT part of the five-number summary?", "The mean", ["The median", "Q1", "The maximum"], "The five-number summary is min, Q1, median, Q3 and max. <b>The mean</b> is not part of it."),
        ("A data set is skewed left. Which is true?", "The mean is usually less than the median", ["The mean is usually greater than the median", "The mean equals the median", "There are no outliers"], "A tail of low values pulls the mean down: <b>mean &lt; median</b>."),
        ("A box plot's left whisker is much longer than its right whisker. What shape is the data?", "Skewed left", ["Skewed right", "Symmetric", "Bell-shaped"], "The long tail is on the low (left) side: <b>skewed left</b>."),
        ("Which change would increase the standard deviation of 10, 12, 14, 16, 18?", "Replace 18 with 30", ["Add 5 to every value", "Replace 10 with 14", "Remove 18 and 10"], "Moving a value far from the mean increases the spread: <b>replace 18 with 30</b>."),
        ("Battery A lasts a mean of 10 h with SD 0.5 h. Battery B lasts a mean of 10.5 h with SD 3 h. Which is more reliable?", "Battery A", ["Battery B", "They are the same", "You cannot compare them"], "Battery A's times vary much less: <b>battery A</b> is more reliable, even though B's mean is a bit higher."),
    ]
    return [T(q, a, w, e) for q, a, w, e in data]


def body():
    return lesson(
        "<p>The <b>five-number summary</b> is the minimum, Q1, median, Q3 and maximum. Order the data first; Q1 and Q3 are the medians of the lower and upper halves. "
        "A <b>box plot</b> draws these five numbers. The <b>IQR</b> = Q3 − Q1 is the spread of the middle half.</p>"
        "<p>An <b>outlier</b> is below Q1 − 1.5 × IQR or above Q3 + 1.5 × IQR. Outliers pull the mean but hardly move the median.</p>"
        "<p>The <b>standard deviation</b> measures how far values typically are from the mean. Adding a constant to every value does not change it; "
        "multiplying every value by <i>k</i> multiplies it by <i>k</i>.</p>"
        + fig(box_svg(12, 20, 26, 32, 44, 10, 50, 5, "box plot with minimum 12, Q1 20, median 26, Q3 32 and maximum 44")),
        [("Find the five-number summary of 3, 7, 8, 5, 12, 14, 21, 13, 18.", ["Order: 3, 5, 7, 8, 12, 13, 14, 18, 21.", "Lower half 3, 5, 7, 8 → Q1 = 6. Upper half 13, 14, 18, 21 → Q3 = 16."], "3, 6, 12, 16, 21"),
         ("Is 40 an outlier if Q1 = 6 and Q3 = 16?", ["IQR = 10.", "Upper fence = 16 + 15 = 31."], "Yes, 40 &gt; 31")],
        ["Finding the median or quartiles without ordering the data first.",
         "Giving the range (max − min) when asked for the IQR (Q3 − Q1).",
         "Reading the ends of the whiskers as the quartiles. The quartiles are the edges of the box.",
         "Thinking that adding the same number to every value changes the spread."])


def main():
    sets = [S("Five-number summary and IQR", collect(one_five, 20, R)),
            S("Read a box plot", collect(one_box, 20, R)),
            S("Outliers", collect(one_out, 20, R)),
            S("Standard deviation", collect(one_sd, 20, R)),
            S("Compare distributions", problems())]
    make("box-plots-and-standard-deviation", 19, "S-ID.A.2",
         "Box Plots, Outliers and Standard Deviation",
         "Algebra 1 Statistics Worksheets: Box Plots, IQR, Outliers and Standard Deviation (Free, Answer Key)",
         "Box plots and standard deviation",
         "Use statistics appropriate to the shape of the data distribution to compare center (median, mean) and spread (interquartile range, "
         "standard deviation) of two or more different data sets.",
         "Free Algebra 1 statistics worksheets (S-ID.A.1–3): five-number summary and IQR, reading box plots, outliers with the 1.5 × IQR "
         "rule, standard deviation and comparing distributions by shape, center and spread. 100 questions with an answer key.",
         "Median and IQR resist outliers; mean and standard deviation suit symmetric data.",
         "IQR = Q3 − Q1. Outliers lie more than 1.5 × IQR beyond the box.",
         body(),
         [("What is the five-number summary?", "The minimum, first quartile (Q1), median, third quartile (Q3) and maximum of a data set. A box plot shows all five."),
          ("How do you find outliers?", "Find IQR = Q3 − Q1. Any value below Q1 − 1.5 × IQR or above Q3 + 1.5 × IQR is an outlier."),
          ("What does standard deviation measure?", "How spread out the data is around the mean. A small standard deviation means the values are close to the mean."),
          ("When should I use the median instead of the mean?", "When the data is skewed or has outliers. The median is not pulled by extreme values.")],
         sets, R, domain="Statistics")


if __name__ == "__main__":
    main()
