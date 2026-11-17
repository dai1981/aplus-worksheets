# -*- coding: utf-8 -*-
"""
AU Year 7 Maths: Mean, median, mode and range (Australian Curriculum v9.0: AC9M7ST01)
  python3 tools/gen_au_maths_y7_mean_median_mode_and_range.py
Calculating the mean, median, mode and range, missing values, comparing data sets, and deciding which measure
of centre gives the most useful picture of the data.
Wrong answers come from real mistakes: not ordering before finding the median, giving the position instead of
the value, dividing by the wrong number, and giving the largest value as the range.
"""
import random
from fractions import Fraction as F
from au_hs import num, mcq, B, S, make, lesson, collect, QN, T, People

R = random.Random(71972)
P = People(R)


def lst(xs):
    return ", ".join(num(x) for x in xs)


def median(xs):
    s = sorted(xs)
    n = len(s)
    return F(s[n // 2]) if n % 2 else F(s[n // 2 - 1] + s[n // 2], 2)


def mode(xs):
    c = {}
    for x in xs:
        c[x] = c.get(x, 0) + 1
    m = max(c.values())
    ms = [k for k, v in c.items() if v == m]
    return ms[0] if len(ms) == 1 and m > 1 else None


# ------------------------------------------------------------ set 1: mean
def one_mean(r):
    n = r.choice([4, 5, 5, 6])
    xs = [r.randint(1, 20) for _ in range(n)]
    if r.random() < 0.3:
        xs = [x - 8 for x in xs]
    m = F(sum(xs), n)
    if m.denominator not in (1, 2, 4, 5):
        return None
    q = "Find the %s of %s." % (B("mean"), B(lst(xs)))
    e = "Add them up: %s. Divide by how many there are (%d): %s ÷ %d = <b>%s</b>." % (num(sum(xs)), n, num(sum(xs)), n, num(m))
    return QN(q, m, [F(sum(xs)), F(sum(xs), n - 1), median(xs), F(sum(xs), n + 1)], e)


# ------------------------------------------------------------ set 2: median
def one_median(r):
    n = r.choice([5, 6, 7, 8])
    xs = r.sample(range(1, 40), n)
    md = median(xs)
    mid_unsorted = F(xs[n // 2]) if n % 2 else F(xs[n // 2 - 1] + xs[n // 2], 2)
    q = "Find the %s of %s." % (B("median"), B(lst(xs)))
    s = sorted(xs)
    if n % 2:
        e = "Put them in order: %s. The middle value is <b>%s</b>." % (lst(s), num(md))
    else:
        e = "Put them in order: %s. The two middle values are %s and %s, so the median is halfway: <b>%s</b>." % (lst(s), num(s[n // 2 - 1]), num(s[n // 2]), num(md))
    return QN(q, md, [mid_unsorted, F(n + 1, 2), F(sum(xs), n) if F(sum(xs), n).denominator <= 2 else None, F(s[n // 2])], e)


# ------------------------------------------------------------ set 3: mode and range
def one_mode_range(r):
    if r.random() < 0.5:
        base = r.sample(range(1, 30), 5)
        m = r.choice(base)
        xs = base + [m, m if r.random() < 0.4 else r.randint(1, 30)]
        if mode(xs) != m:
            return None
        r.shuffle(xs)
        q = "Find the %s of %s." % (B("mode"), B(lst(xs)))
        e = "The mode is the value that appears most often: <b>%s</b>." % num(m)
        cnt = xs.count(m)
        return QN(q, m, [cnt, max(xs), median(xs) if median(xs) != m else min(xs)], e)
    n = r.choice([5, 6, 7])
    xs = [r.randint(-10, 40) for _ in range(n)]
    rg = max(xs) - min(xs)
    q = "Find the %s of %s." % (B("range"), B(lst(xs)))
    e = "Range = largest − smallest = %s − %s = <b>%s</b>." % (num(max(xs)), "(%s)" % num(min(xs)) if min(xs) < 0 else num(min(xs)), num(rg))
    return QN(q, rg, [max(xs), xs[-1] - xs[0] if xs[-1] - xs[0] != rg and xs[-1] - xs[0] > 0 else None, max(xs) + min(xs) if min(xs) < 0 else max(xs) - min(xs) + 1], e)


# ------------------------------------------------------------ set 4: missing values, comparing
def one_missing(r):
    n = r.choice([3, 4, 5])
    m = r.randint(5, 20)
    xs = [r.randint(1, 30) for _ in range(n - 1)]
    last = n * m - sum(xs)
    if last <= 0 or last > 60:
        return None
    q = "The mean of %d numbers is %d. %s of them are %s. What is the missing number?" % (n, m, ["", "", "Two", "Three", "Four"][n - 1], lst(xs))
    e = "Total = %d × %d = %d. Missing = %d − %d = <b>%d</b>." % (n, m, n * m, n * m, sum(xs), last)
    return QN(q, last, [m, n * m, m * (n - 1) - sum(xs) if m * (n - 1) - sum(xs) > 0 else None], e)


def one_compare(r):
    a = [r.randint(10, 30) for _ in range(5)]
    b = [r.randint(10, 30) for _ in range(5)]
    ma, mb = F(sum(a), 5), F(sum(b), 5)
    ra, rb = max(a) - min(a), max(b) - min(b)
    if ma == mb or ra == rb:
        return None
    n1, n2 = P.next()[0], P.next()[0]
    if r.random() < 0.5:
        q = "%s scored %s in five tests. %s scored %s. Who has the %s?" % (n1, lst(a), n2, lst(b), B("higher mean"))
        right = n1 if ma > mb else n2
        e = "Mean: %s %s, %s %s. So <b>%s</b>." % (n1, num(ma), n2, num(mb), right)
    else:
        q = "%s scored %s in five tests. %s scored %s. Whose scores are %s (smaller range)?" % (n1, lst(a), n2, lst(b), B("more consistent"))
        right = n1 if ra < rb else n2
        e = "Range: %s %d, %s %d. The smaller range is more consistent: <b>%s</b>." % (n1, ra, n2, rb, right)
    return T(q, right, [n2 if right == n1 else n1, "They are the same", "You cannot tell"], e)


# ------------------------------------------------------------ set 5: problems
def problems():
    its = []
    data = [
        ("The mean of 4 numbers is 12. A fifth number, 22, is added. What is the new mean?", 14, [17, 12, F(34, 2)], "Old total = 48. New total = 70. 70 ÷ 5 = <b>14</b>."),
        ("Five students have a mean height of 152 cm. One student of 164 cm leaves. What is the mean height of the other four?", 149, [152, 140, 146], "Total = 760. 760 − 164 = 596. 596 ÷ 4 = <b>149 cm</b>."),
        ("The range of 4, 9, 12, <i>x</i> is 10, and <i>x</i> is the largest number. Find <i>x</i>.", 14, [22, 10, 16], "Range = <i>x</i> − 4 = 10, so <i>x</i> = <b>14</b>."),
        ("The median of 3, 7, <i>x</i>, 12, 15 (in order) is 9. Find <i>x</i>.", 9, [7, 10, 12], "With 5 values in order, the median is the 3rd: <i>x</i> = <b>9</b>."),
        ("Ten students' shoe sizes have a mean of 6.5. What is the total of their shoe sizes?", 65, [F(13, 2), 16, 60], "Total = mean × number = 6.5 × 10 = <b>65</b>."),
        ("Overnight lows in Thredbo one week were −3, 1, 2, −5, 0, 6 and 6 °C. What was the mean temperature?", 1, [F(23, 7), 0, 6], "Total = 7. 7 ÷ 7 = <b>1 °C</b>."),
        ("Overnight lows in Thredbo one week were −3, 1, 2, −5, 0, 6 and 6 °C. What was the range?", 11, [6, 1, 9], "6 − (−5) = <b>11 °C</b>."),
        ("Three numbers have a mode of 4, a median of 4 and a mean of 6. What is the largest number?", 10, [6, 8, 14], "Two numbers are 4 (mode and median). Total = 18, so the third is 18 − 8 = <b>10</b>."),
    ]
    for q, a, w, e in data:
        its.append(QN(q, a, [x for x in w if F(x).denominator <= 2], e))
    texts = [
        ("Which measure should be used for shoe sizes when ordering stock for a shop?", "The mode", ["The mean", "The range", "The median"],
         "The shop wants the size sold most often: <b>the mode</b>. A mean such as 5.7 is not a real shoe size."),
        ("House prices in a street are $650 000, $680 000, $700 000, $720 000 and $3 200 000. Which measure best represents a typical price?", "The median", ["The mean", "The mode", "The range"],
         "The $3 200 000 is an outlier that pulls the mean up. <b>The median</b> ($700 000) is more typical."),
        ("What does the range tell you?", "How spread out the data is", ["The most common value", "The middle value", "The total"],
         "The range = largest − smallest. It measures <b>how spread out</b> the data is."),
        ("Which set of data has no mode?", "3, 5, 7, 9, 11", ["3, 5, 5, 7, 9", "2, 2, 2, 8, 8", "1, 4, 4, 6, 6, 6"], "In <b>3, 5, 7, 9, 11</b> every value appears once, so there is no mode."),
        ("Which statement is always true?", "The median of an odd number of values is one of the values", ["The mean is one of the values", "The mode is the middle value", "The range is bigger than the mean"],
         "With an odd number of values the median is the middle value itself, so <b>it is one of the values</b>."),
        ("Mia's mean score in 4 netball games is 15. What must she score in the 5th game to raise her mean to 16?", "20", ["16", "17", "21"], "She needs a total of 5 × 16 = 80. She has 60, so she needs <b>20</b>."),
        ("Five numbers have a mean of 8. Which list could they be?", "4, 6, 8, 10, 12", ["8, 9, 10, 11, 12", "2, 4, 6, 8, 10", "8, 8, 8, 8, 9"], "4 + 6 + 8 + 10 + 12 = 40 and 40 ÷ 5 = 8: <b>4, 6, 8, 10, 12</b>."),
        ("The median of 2, 5, 8, 11 is…", "6.5", ["5", "8", "13"], "The middle two are 5 and 8, and halfway between is <b>6.5</b>."),
        ("Team A's mean score is 12 with range 3. Team B's mean score is 12 with range 15. Which statement is correct?", "Team A's scores are more consistent", ["Team B is better", "Team A is better", "The teams are the same in every way"],
         "The means are the same, but Team A has a smaller range, so <b>Team A's scores are more consistent</b>."),
        ("A data set is 7, 7, 8, 10, 13. If 13 is changed to 30, which average changes?", "The mean", ["The median", "The mode", "None of them"],
         "The median (8) and mode (7) stay the same. The total changes, so <b>the mean</b> changes."),
        ("Find the mean of 1.2, 3.4 and 2.9.", "2.5", ["7.5", "3.4", "2.9"], "1.2 + 3.4 + 2.9 = 7.5, and 7.5 ÷ 3 = <b>2.5</b>."),
        ("The mean age of 3 children is 8. Their ages are all different whole numbers. What is the largest possible age of the oldest?", "21", ["24", "10", "22"], "The total is 24. The other two must be at least 1 and 2, so the oldest can be 24 − 3 = <b>21</b>."),
    ]
    for q, a, w, e in texts:
        its.append(T(q, a, w, e))
    return its


def body():
    return lesson(
        "<ul><li><b>Mean</b>: add up all the values and divide by how many there are.</li>"
        "<li><b>Median</b>: put the values in order and find the middle one (or halfway between the middle two).</li>"
        "<li><b>Mode</b>: the value that appears most often.</li>"
        "<li><b>Range</b>: largest − smallest. It shows how spread out the data is.</li></ul>",
        [("Find the mean, median, mode and range of 5, 9, 2, 9, 10.", ["Mean: 35 ÷ 5 = 7.", "In order: 2, 5, 9, 9, 10, so the median is 9.",
                                                                      "Mode: 9. Range: 10 − 2 = 8."], "7, 9, 9 and 8"),
         ("The mean of 4 numbers is 6. Three are 3, 5 and 8. Find the fourth.", ["Total = 4 × 6 = 24.", "24 − 16 = 8."], "8")],
        ["Finding the median without putting the values in order first.",
         "Giving the position instead of the value: for 7 values the median is the 4th value, not 4.",
         "Dividing by the wrong number when finding the mean.",
         "Giving the largest value as the range instead of largest − smallest."])


def main():
    sets = [S("The mean", collect(one_mean, 20, R)),
            S("The median", collect(one_median, 20, R)),
            S("The mode and range", collect(one_mode_range, 20, R)),
            S("Missing values and comparing data", collect(one_missing, 10, R) + collect(one_compare, 10, R)),
            S("Problems and choosing an average", problems())]
    make(7, "mean-median-mode-and-range", 19, "AC9M7ST01",
         "Mean, Median, Mode and Range",
         "Year 7 Mean, Median, Mode and Range Worksheets: Measures of Centre and Spread (Free, Answer Key)",
         "Mean, median, mode and range",
         "acquire data sets for discrete and continuous numerical variables and calculate the range, median, mean and mode; "
         "make and justify decisions about which measures of central tendency provide useful insights into the nature of the distribution of data",
         "Free Year 7 maths worksheets on mean, median, mode and range for the Australian Curriculum (AC9M7ST01): calculating "
         "each measure, missing values, comparing data and choosing the best measure of centre. 100 questions with an answer key.",
         "Mean: add and divide. Median: middle value in order. Mode: most common. Range: largest − smallest.",
         "An outlier pulls the mean, so the median can describe a typical value better.",
         body(),
         [("What is the difference between mean, median and mode?", "The mean is the total shared equally, the median is the middle value in order, and the mode is the most common value."),
          ("How do I find the median of an even number of values?", "Put them in order and find the two middle values. The median is halfway between them."),
          ("Is range an average?", "No. The range measures spread: largest minus smallest. A smaller range means more consistent data."),
          ("Which average should I use?", "Use the mode for the most common item, the median when there are outliers, and the mean when you want to use every value.")],
         sets, R)


if __name__ == "__main__":
    main()
