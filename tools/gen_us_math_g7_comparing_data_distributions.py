# -*- coding: utf-8 -*-
"""
US Grade 7 Math: Comparing Data Distributions (7.SP.B.3, 7.SP.B.4)
  python tools/gen_us_math_g7_comparing_data_distributions.py
Mean and mean absolute deviation (MAD), median and interquartile range (IQR), and comparing two groups,
including the difference in centers measured in MADs.
Wrong answers come from real mistakes: forgetting to divide by the count, finding the median without
sorting, using the range instead of the IQR, and comparing centers without looking at the spread.
"""
import random
from fractions import Fraction as F
from ws_common import (num, mcq, balance, B, table, example, write_unit)

R = random.Random(71801)
UPDATED = "2026-11-09"


def n(v):
    return num(F(v))


def mean(xs):
    return F(sum(xs), len(xs))


def mad(xs):
    m = mean(xs)
    return sum(abs(F(x) - m) for x in xs) / len(xs)


def median(xs):
    s = sorted(xs)
    k = len(s)
    return F(s[k // 2]) if k % 2 else F(s[k // 2 - 1] + s[k // 2], 2)


def quartiles(xs):
    s = sorted(xs)
    k = len(s)
    lo, hi = s[:k // 2], s[(k + 1) // 2:]
    return median(lo), median(hi)


def item(q, v, ws, e, unit=""):
    v = F(v)
    cands = []
    for w in list(ws) + [v + 1, v - 1, v * 2]:
        w = F(w)
        if w >= 0 and w != v and num(w) is not None:
            cands.append((n(w) + unit, w))
    return mcq(q, (n(v) + unit, v), cands, e)


def L(xs):
    return ", ".join(str(x) for x in xs)


# ------------------------------------------------------------ set 1: mean and MAD
def set_mad():
    its = []
    data = [[4, 6, 8, 10, 12], [2, 3, 5, 6, 9], [10, 12, 14, 16, 18, 20], [5, 5, 7, 9, 9], [20, 24, 26, 30], [1, 3, 4, 8], [11, 13, 15, 17, 19],
            [6, 8, 8, 10, 13], [30, 34, 36, 40], [3, 5, 9, 11]]
    for xs in data:
        m = mean(xs)
        its.append(item("Find the mean of %s." % B(L(xs)), m, [sum(xs), median(xs) if median(xs) != m else m + 2, F(sum(xs), len(xs) - 1)],
                        "Add the values: %d. Divide by how many there are (%d): %s." % (sum(xs), len(xs), n(m))))
    for xs in data[:8]:
        m, d = mean(xs), mad(xs)
        devs = ", ".join(n(abs(F(x) - m)) for x in xs)
        its.append(item("The mean of %s is %s. What is the mean absolute deviation (MAD)?" % (B(L(xs)), n(m)), d,
                        [sum(abs(F(x) - m) for x in xs), max(xs) - min(xs), d + F(1, 2)],
                        "Distances from the mean: %s. Their mean is %s ÷ %d = %s." % (devs, n(sum(abs(F(x) - m) for x in xs)), len(xs), n(d))))
    its.append(mcq("What does the MAD tell you?", ("How far the values are from the mean, on average", "a"),
                   [("The middle value", "b"), ("The largest value minus the smallest", "c"), ("How many values there are", "d")],
                   "The MAD is the average distance from the mean. A bigger MAD means the data are more spread out."))
    its.append(mcq("Data set A has MAD 2. Data set B has MAD 7. Which is true?", ("B is more spread out", "a"),
                   [("A is more spread out", "b"), ("B has a larger mean", "c"), ("They have the same spread", "d")], "A larger MAD means more variability."))
    return {"title": "Mean and mean absolute deviation", "items": its}


# ------------------------------------------------------------ set 2: median and IQR
def set_iqr():
    its = []
    data = [[3, 9, 5, 7, 1], [12, 4, 8, 10, 6, 2], [15, 11, 19, 13, 17, 21, 23], [40, 25, 30, 35, 45, 50], [7, 2, 9, 4, 6, 8, 3, 5],
            [18, 22, 20, 26, 24, 16, 28]]
    for xs in data:
        md = median(xs)
        its.append(item("Find the median of %s." % B(L(xs)), md, [F(xs[len(xs) // 2]) if F(xs[len(xs) // 2]) != md else md + 3, mean(xs) if mean(xs) != md else md + 1, max(xs) - min(xs)],
                        "Order them: %s. The middle value is %s." % (L(sorted(xs)), n(md))))
    data2 = [[2, 4, 5, 7, 8, 10, 12, 14], [10, 12, 15, 16, 18, 20, 25], [1, 3, 3, 6, 7, 9, 11, 12], [20, 22, 25, 28, 30, 31, 35, 40, 42],
             [5, 6, 8, 10, 11, 13, 15, 16], [30, 32, 35, 36, 40, 44, 45, 50], [4, 7, 8, 10, 14, 15, 17, 20]]
    for xs in data2:
        q1, q3 = quartiles(xs)
        its.append(item("The data in order are %s. What is the interquartile range (IQR)?" % B(L(xs)), q3 - q1, [max(xs) - min(xs), q3, median(xs)],
                        "Q1 (middle of the lower half) = %s. Q3 (middle of the upper half) = %s. IQR = %s − %s = %s. Not %s: that is the range." % (
                            n(q1), n(q3), n(q3), n(q1), n(q3 - q1), n(max(xs) - min(xs)))))
    con = [("What does the IQR measure?", "The spread of the middle half of the data", ["The middle value", "The average of the data", "The largest value"]),
           ("Which measure of center is better when there is an outlier?", "The median", ["The mean", "The range", "The MAD"]),
           ("Which pair goes together?", "Median and IQR", ["Mean and IQR", "Median and MAD", "Range and mean"]),
           ("A box plot shows Q1 = 12, median = 15 and Q3 = 20. What is the IQR?", "8", ["3", "5", "15"]),
           ("In a box plot, the box shows…", "the middle 50% of the data", ["all of the data", "only the outliers", "the mean"]),
           ("A data set is 2, 3, 3, 4, 40. Why is the median a better center than the mean?", "40 is an outlier that pulls the mean up", ["The median is always bigger", "There is no mode", "The data are in order"]),
           ("Adding a very large value to a data set changes which measure more?", "The mean", ["The median", "Neither", "Both the same"])]
    for q, g, bad in con:
        its.append(mcq(q, (g, "g"), [(b, b) for b in bad],
                       {"The spread of the middle half of the data": "IQR = Q3 − Q1, the width of the middle 50%.", "The median": "The median is not pulled by extreme values.",
                        "Median and IQR": "Use median with IQR, and mean with MAD.", "8": "IQR = Q3 − Q1 = 20 − 12 = 8.", "the middle 50% of the data": "The box goes from Q1 to Q3.",
                        "40 is an outlier that pulls the mean up": "The mean is 10.4, larger than 4 of the 5 values. The median, 3, fits the data better.",
                        "The mean": "Every value is in the mean, so one large value pulls it a lot. The median moves little."}[g]))
    return {"title": "Median and interquartile range", "items": its}


# ------------------------------------------------------------ set 3: compare two groups
def set_compare():
    its = []
    pairs = [("Class A test scores", [70, 75, 80, 85, 90], "Class B test scores", [78, 80, 82, 84, 86]),
             ("Team A heights (in.)", [58, 60, 62, 64, 66], "Team B heights (in.)", [62, 64, 66, 68, 70]),
             ("Store A prices ($)", [4, 6, 8, 10, 12], "Store B prices ($)", [7, 8, 8, 9, 13]),
             ("Plant A heights (cm)", [10, 12, 13, 15, 20], "Plant B heights (cm)", [11, 11, 14, 16, 18])]
    for na, a, nb, b in pairs:
        ma, mb = mean(a), mean(b)
        good = "%s has the greater mean (%s vs %s)" % (na.split(" ")[0] + " " + na.split(" ")[1], n(max(ma, mb)), n(min(ma, mb))) if ma != mb else "The means are equal (%s)" % n(ma)
        if ma > mb:
            good = "Group A has the greater mean (%s vs %s)" % (n(ma), n(mb))
        elif mb > ma:
            good = "Group B has the greater mean (%s vs %s)" % (n(mb), n(ma))
        else:
            good = "The means are equal (%s)" % n(ma)
        bad = [x for x in ["Group A has the greater mean (%s vs %s)" % (n(ma) if ma > mb else n(mb), n(mb) if ma > mb else n(ma)),
                           "Group B has the greater mean (%s vs %s)" % (n(mb) if mb > ma else n(ma), n(ma) if mb > ma else n(mb)),
                           "The means are equal (%s)" % n(ma), "Group A has the greater mean because it has the largest value"] if x != good]
        its.append(mcq("Group A: %s: %s. Group B: %s: %s. Compare the means." % (na, L(a), nb, L(b)), (good, "g"), [(x, x) for x in bad[:3]],
                       "Mean A = %s ÷ 5 = %s. Mean B = %s ÷ 5 = %s." % (sum(a), n(ma), sum(b), n(mb))))
        da, db = mad(a), mad(b)
        g2 = "Group A" if da > db else ("Group B" if db > da else "Neither: they are the same")
        its.append(mcq("Group A: %s. Group B: %s. Which group's data are more spread out (larger MAD)?" % (L(a), L(b)), (g2, "g"),
                       [(x, x) for x in ["Group A", "Group B", "Neither: they are the same", "It cannot be told"] if x != g2][:3],
                       "MAD A = %s and MAD B = %s." % (n(da), n(db))))
    ratio = [(80, 85, 5), (62, 68, 3), (40, 46, 2), (100, 112, 4), (25, 27, 4), (150, 165, 5), (50, 53, 1), (70, 79, 3), (12, 16, 2), (90, 99, 6)]
    for m1, m2, d in ratio:
        k = F(m2 - m1, d)
        its.append(item("Two groups have means %d and %d. Both have a MAD of %d. How many MADs apart are the means?" % (m1, m2, d), k,
                        [m2 - m1, F(m2 - m1, 2 * d), d], "Difference of means = %d. %d ÷ %d = %s MADs." % (m2 - m1, m2 - m1, d, n(k))))
    lab = [("The means of two groups are 1 MAD apart.", "The groups overlap a lot", ["The groups do not overlap at all", "One group has no spread", "The means are equal"]),
           ("The means of two groups are 4 MADs apart.", "The groups are very different with little overlap", ["The groups are almost the same", "The groups have equal means", "Nothing can be said"])]
    for q, g, bad in lab:
        its.append(mcq(q + " What does this suggest?", (g, "g"), [(b, b) for b in bad],
                       "The more MADs apart the centers are, the less the groups overlap. About 2 or more MADs suggests a real difference."))
    return {"title": "Compare two groups", "items": its}


# ------------------------------------------------------------ set 4: dot plots and box plots in words
def set_plots():
    its = []
    bp = [((10, 15, 20, 25, 30), (12, 18, 22, 24, 28)), ((40, 50, 55, 60, 80), (45, 48, 52, 58, 62)), ((5, 8, 10, 14, 20), (2, 9, 12, 13, 16))]
    for A, Bv in bp:
        iqa, iqb = A[3] - A[1], Bv[3] - Bv[1]
        tbl = table(["", "Min", "Q1", "Median", "Q3", "Max"], [["Group A"] + [str(x) for x in A], ["Group B"] + [str(x) for x in Bv]])
        g = "Group A" if A[2] > Bv[2] else "Group B"
        its.append(mcq("The table gives box plot values." + tbl + "Which group has the greater median?", (g, "g"),
                       [("Group A" if g == "Group B" else "Group B", "o"), ("They are equal", "e"), ("It cannot be told", "c")], "Median A = %d, median B = %d." % (A[2], Bv[2])))
        g = "Group A" if iqa > iqb else ("Group B" if iqb > iqa else "They are equal")
        its.append(mcq("The table gives box plot values." + tbl + "Which group has the greater IQR?", (g, "g"),
                       [(x, x) for x in ["Group A", "Group B", "They are equal", "It cannot be told"] if x != g][:3],
                       "IQR A = %d − %d = %d. IQR B = %d − %d = %d." % (A[3], A[1], iqa, Bv[3], Bv[1], iqb)))
        its.append(item("The table gives box plot values." + tbl + "What is the difference between the medians?", abs(A[2] - Bv[2]),
                        [abs(A[4] - Bv[4]), abs(iqa - iqb) if abs(iqa - iqb) != abs(A[2] - Bv[2]) else 1, A[2] + Bv[2]], "|%d − %d| = %d." % (A[2], Bv[2], abs(A[2] - Bv[2]))))
    qs = [("A dot plot shows most values between 20 and 30, with one value at 70. Which measures best describe it?", "Median and IQR", ["Mean and MAD", "Mean and range", "Mode only"]),
          ("A dot plot is symmetric with no outliers. Which measures fit well?", "Mean and MAD", ["Median and IQR only", "Range only", "Mode and range"]),
          ("Two dot plots have the same center, but one is much wider. What is different?", "The spread (variability)", ["The center", "The number of values", "Nothing"]),
          ("Two box plots have the same IQR, but one is shifted 10 units to the right. What is different?", "The center", ["The spread", "The shape", "Nothing"]),
          ("Seventh graders' reaction times have median 0.32 s, and eighth graders' have median 0.28 s, with similar IQRs. Which inference is reasonable?",
           "Eighth graders tend to react a bit faster", ["Every eighth grader is faster", "Seventh graders are always faster", "The groups are the same"]),
          ("Random samples of 7th and 8th graders' sleep: means 8.2 h and 7.6 h, MAD 0.6 h each. How many MADs apart are the means?", "1", ["0.6", "2", "0.1"]),
          ("Two random samples show median screen time of 3 h (Group A) and 5 h (Group B), with IQRs of 1 h. What can you infer?", "Group B tends to have more screen time",
           ["Group A has more screen time", "The groups are the same", "Nothing at all"]),
          ("Which comparison uses a measure of center?", "The median height of Team A is 2 inches more than Team B", ["Team A's heights are more spread out",
           "Team B has a larger range", "Team A has a larger IQR"]),
          ("Which comparison uses a measure of variability?", "Team A's MAD is greater than Team B's", ["Team A's mean is greater", "Team B's median is greater", "Team A has more players"])]
    for q, g, bad in qs:
        its.append(mcq(q, (g, "g"), [(b, b) for b in bad], "Center (mean, median) tells a typical value. Spread (MAD, IQR, range) tells how much values vary."))
    its.append(mcq("Group A: 2, 4, 6, 8, 10. Group B: 4, 5, 6, 7, 8. Which is true?", ("Same mean; A is more spread out", "a"),
                   [("Same mean; B is more spread out", "b"), ("A has a larger mean", "c"), ("Same mean and same spread", "d")],
                   "Both means are 6. MAD A = 2.4 and MAD B = 1.2."))
    its.append(mcq("Group A: 10, 12, 14. Group B: 20, 22, 24. Which is true?", ("Same spread; B has a larger center", "a"),
                   [("Same center; B is more spread out", "b"), ("A has a larger center", "c"), ("They are the same", "d")], "Both have range 4 and MAD 4/3. Mean B = 22 > mean A = 12."))
    return {"title": "Box plots, dot plots and inferences", "items": its}


# ------------------------------------------------------------ set 5: word problems
def set_words():
    its = []
    w = [("Five friends ran these miles in a week: 3, 5, 4, 6, 7. What is the mean?", 5, [25, 4, 6], "25 ÷ 5 = 5 miles.", " miles"),
         ("Ten quiz scores: 6, 7, 7, 8, 8, 8, 9, 9, 10, 10. What is the median?", 8, [F("8.2"), 9, 4], "The middle two values are 8 and 8, so the median is 8.", ""),
         ("Daily high temperatures (°F): 62, 65, 70, 68, 75. What is the mean?", 68, [340, 70, 13], "340 ÷ 5 = 68°F.", "°F"),
         ("Points in 4 games: 12, 18, 20, 30. The mean is 20. What is the MAD?", 5, [20, 18, 8], "Distances: 8, 2, 0, 10. Mean = 20 ÷ 4 = 5.", ""),
         ("Test scores: 60, 70, 75, 80, 85, 90, 95, 100. What is the IQR?", 20, [40, 82, 15], "Q1 = 72.5, Q3 = 92.5. IQR = 20.", ""),
         ("Hours of practice: 1, 2, 2, 3, 12. What is the median?", 2, [4, 3, 11], "In order, the middle value is 2. (The mean, 4, is pulled up by 12.)", " hours"),
         ("Team A's mean score is 74 and Team B's is 82. Both have a MAD of 4. How many MADs apart are the means?", 2, [8, 4, 1], "82 − 74 = 8. 8 ÷ 4 = 2 MADs.", ""),
         ("Prices of 6 books: $8, $10, $12, $14, $16, $18. What is the mean price?", 13, [78, 12, 10], "78 ÷ 6 = $13.", ""),
         ("A basketball team scored 45, 52, 60, 48 and 55 points. What is the range?", 15, [52, 260, 7], "60 − 45 = 15 points.", " points"),
         ("Heights (cm) of 5 plants: 14, 18, 16, 20, 12. What is the MAD?", F("2.4"), [16, 8, F("4.8")], "Mean = 16. Distances: 2, 2, 0, 4, 4. 12 ÷ 5 = 2.4 cm.", " cm")]
    for q, v, ws, e, u in w:
        if "$" in q and u == "":
            its.append(mcq(q, ("$%s" % n(v), v), [("$%s" % n(x), x) for x in ws if F(x) != v], e))
        else:
            its.append(item(q, v, ws, e, u))
    conc = [("Class A's median reading time is 30 min with IQR 10. Class B's median is 45 min with IQR 12. Which statement is best?", "Class B tends to read longer",
             ["Class A tends to read longer", "The classes read the same amount", "Class B's data have no spread"]),
            ("Two classes have the same mean score, 80. Class A's MAD is 3 and Class B's is 12. Which is true?", "Class B's scores vary much more",
             ["Class A's scores vary more", "Class B did better", "The classes are the same in every way"]),
            ("Random samples from two schools: mean commute 15 min and 17 min, MAD 6 min each. What is reasonable to say?", "The commutes are similar; the difference is small compared to the spread",
             ["School B's commute is much longer", "Every student at B travels 2 min longer", "The samples must be biased"]),
            ("A salary list has values 30, 32, 35, 36, 200 (thousands). Which center best shows a typical salary?", "The median (35)", ["The mean (66.6)", "The range (170)", "The largest (200)"]),
            ("Two plant fertilizers: plants with A grew a median of 12 cm, plants with B grew 20 cm. Both IQRs are 3 cm. What can you infer?", "Fertilizer B likely leads to more growth",
             ["Fertilizer A works better", "The fertilizers are the same", "Nothing can be said"]),
            ("A coach compares two runners' race times. Runner A: mean 52 s, MAD 1 s. Runner B: mean 51 s, MAD 4 s. Who is more consistent?", "Runner A",
             ["Runner B", "Both are the same", "It cannot be told"]),
            ("Which shows the most overlap between two groups?", "Means 0.5 MAD apart", ["Means 2 MADs apart", "Means 3 MADs apart", "Means 5 MADs apart"]),
            ("A new value equal to the mean is added to a data set. What happens to the mean?", "It stays the same", ["It goes up", "It goes down", "It doubles"]),
            ("The scores 5, 5, 5, 5, 5 have what MAD?", "0", ["5", "1", "25"]),
            ("Group A: median 40, IQR 20. Group B: median 42, IQR 22. Which statement fits?", "The groups are very similar", ["Group B is much higher", "Group A has no spread",
             "The groups do not overlap"])]
    for q, g, bad in conc:
        its.append(mcq(q, (g, "g"), [(b, b) for b in bad], "Compare the centers, and judge the difference against the spread."))
    return {"title": "Word problems", "items": its}


def body():
    rows = [["Mean", "Add, then divide by the count", "Mean absolute deviation (MAD)", "Average distance from the mean"],
            ["Median", "Middle value in order", "Interquartile range (IQR)", "Q3 − Q1, the middle half"]]
    return ("<h2>Center and spread</h2><p>To describe data, give a <b>center</b> (a typical value) and a <b>spread</b> (how much the values vary). "
            "Use the mean with the MAD for data without outliers. Use the median with the IQR when there are outliers.</p>"
            + table(["Center", "How to find it", "Spread", "Meaning"], rows)
            + example("Find the mean and MAD of 4, 6, 8, 10, 12.", ["Mean = 40 ÷ 5 = 8.", "Distances from 8: 4, 2, 0, 2, 4.", "MAD = 12 ÷ 5 = 2.4."], "mean 8, MAD 2.4")
            + "<h2>Compare two groups</h2><p>Compare the centers, then look at the spread. Divide the difference in means by the MAD: "
            "if the means are 2 or more MADs apart, the groups are clearly different.</p>"
            + example("Means 74 and 82, both with MAD 4. How different are the groups?", ["Difference = 8.", "8 ÷ 4 = 2 MADs."], "2 MADs apart: a clear difference")
            + "<h2>Common mistakes</h2><ul><li>Finding the median without putting the data in order.</li><li>Using the range when the question asks for the IQR.</li>"
            "<li>Calling a small difference in means important without looking at the spread.</li></ul>")


def main():
    sets = [set_mad(), set_iqr(), set_compare(), set_plots(), set_words()]
    balance(sets, R)
    unit = {
        "slug": "comparing-data-distributions",
        "title": "Comparing Data Distributions",
        "seo_title": "Grade 7 Comparing Data Distributions Worksheets: Mean, MAD, Median and IQR",
        "short_title": "Comparing data distributions",
        "domain": "Statistics & Probability",
        "standard_code": "7.SP.B.3–4",
        "standard_url": "https://www.thecorestandards.org/Math/Content/7/SP/B/3/",
        "standard_text": "Informally assess the degree of visual overlap of two numerical data distributions with similar variabilities, measuring the difference between the centers by expressing it as a multiple of a measure of variability. Use measures of center and measures of variability for numerical data from random samples to draw informal comparative inferences about two populations.",
        "meta_desc": "Free Grade 7 comparing data distributions worksheets: mean and mean absolute deviation, median and IQR, box plots and dot plots, comparing two groups and differences measured in MADs. 100 practice questions with an answer key.",
        "key_big": "Compare the centers, then judge the difference against the spread.",
        "key_sub": "Mean with MAD, median with IQR. Means 2 or more MADs apart show a clear difference.",
        "body_html": body(),
        "faq": [
            {"q": "What is the mean absolute deviation?", "a": "The average distance of the values from the mean. For 4, 6, 8, 10, 12 the mean is 8 and the MAD is (4 + 2 + 0 + 2 + 4) ÷ 5 = 2.4."},
            {"q": "How do you find the interquartile range?", "a": "Order the data, find Q1 (middle of the lower half) and Q3 (middle of the upper half), then subtract: IQR = Q3 − Q1."},
            {"q": "When should I use the median instead of the mean?", "a": "When the data have outliers or are skewed. The median is not pulled by extreme values."},
            {"q": "How do I compare two data sets?", "a": "Compare their centers and spreads. Divide the difference in means by the MAD to see how far apart the groups are."}],
        "sets": sets,
        "pdf_url": "",
        "sort": 18,
        "updated": UPDATED,
    }
    write_unit("us", "math", "grade-7", unit)


if __name__ == "__main__":
    main()
