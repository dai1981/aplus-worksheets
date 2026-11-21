# -*- coding: utf-8 -*-
"""
India Class 10 Maths, NCERT Chapter 13: Statistics — Mean, Mode and Median of Grouped Data (CBSE Unit VII)
  python3 tools/gen_in_maths_c10_statistics.py
Class marks and the mean by the direct method, the assumed mean and step-deviation methods, the modal class and the
mode formula, cumulative frequency, the median class and the median formula, a missing frequency from the mean, and
the empirical relation 3 Median = Mode + 2 Mean.
Wrong answers come from real mistakes: using the lower limits instead of the class marks, dividing by the number of
classes, f₁ − f₂ in the numerator of the mode formula, taking the class with the largest cumulative frequency as the
median class, and n/2 without subtracting the cumulative frequency before.
"""
import random
from fractions import Fraction as F
from in_common import num, S, make, lesson, mix, T, table, People

R = random.Random(910013)
P = People(R)


def d2(v):
    v = F(v)
    if (v * 100).denominator == 1:
        return num(v)
    return num(F(int(v * 100 + (F(1, 2) if v > 0 else -F(1, 2))), 100))


def classes(r, k=None):
    h = r.choice([5, 10, 10, 20, 10])
    k = k or r.choice([5, 5, 6])
    start = r.choice([0, 0, 10, 20, 100, 50]) if h != 5 else r.choice([0, 5, 10, 15, 25])
    return [(start + i * h, start + (i + 1) * h) for i in range(k)], h


def tab(cl, fr, name="Class", fname="Frequency"):
    return table([name] + ["%d–%d" % c for c in cl], [[fname] + [str(f) for f in fr]])


def unimodal(r, k):
    """frequencies with a single clear peak (not at an end)"""
    while True:
        fr = [r.randint(2, 20) for _ in range(k)]
        m = max(fr)
        i = fr.index(m)
        if fr.count(m) == 1 and 0 < i < k - 1 and m - max(fr[i - 1], fr[i + 1]) >= 2:
            return fr


# ---------------------------------------------------------------- set 1: direct method
def one_direct(r):
    cl, h = classes(r)
    fr = [r.randint(2, 15) for _ in cl]
    n = sum(fr)
    xs = [F(a + b, 2) for a, b in cl]
    m = sum(f * x for f, x in zip(fr, xs)) / n
    kind = r.choice(["mean", "mean", "mean", "mark", "sum"])
    t = tab(cl, fr)
    if kind == "mark":
        i = r.randrange(len(cl))
        a, b = cl[i]
        return T("What is the class mark of the class %d–%d?" % (a, b), num(F(a + b, 2)), [num(b - a), num(a), num(a + b)],
                 "Class mark = (lower limit + upper limit) ÷ 2 = (%d + %d) ÷ 2 = <b>%s</b>." % (a, b, num(F(a + b, 2))))
    if kind == "sum":
        s = sum(f * x for f, x in zip(fr, xs))
        return T("For this data, find Σf<sub>i</sub>x<sub>i</sub>, where x<sub>i</sub> are the class marks." + t, num(s),
                 [num(sum(f * a for f, (a, b) in zip(fr, cl))), num(sum(xs)), num(s + n * h)],
                 "Multiply each frequency by its class mark and add: <b>%s</b>." % num(s))
    return T("Find the mean of this grouped data (direct method, correct to 2 decimal places where needed)." + t, d2(m),
             [d2(sum(f * a for f, (a, b) in zip(fr, cl)) / n), d2(sum(f * x for f, x in zip(fr, xs)) / len(cl)), d2(sum(xs) / len(xs)) if d2(sum(xs) / len(xs)) != d2(m) else d2(m + h)],
             "Class marks x<sub>i</sub>: %s. Σf<sub>i</sub> = %d, Σf<sub>i</sub>x<sub>i</sub> = %s. Mean = %s ÷ %d = <b>%s</b>." % (
                 ", ".join(num(x) for x in xs), n, num(sum(f * x for f, x in zip(fr, xs))), num(sum(f * x for f, x in zip(fr, xs))), n, d2(m)))


# ---------------------------------------------------------------- set 2: assumed mean and step deviation
def one_step(r):
    cl, h = classes(r)
    fr = [r.randint(2, 15) for _ in cl]
    n = sum(fr)
    xs = [F(a + b, 2) for a, b in cl]
    A = xs[len(xs) // 2]
    us = [(x - A) / h for x in xs]
    fu = sum(f * u for f, u in zip(fr, us))
    m = A + h * fu / n
    t = tab(cl, fr)
    kind = r.choice(["mean", "mean", "fu", "u"])
    if kind == "u":
        i = r.choice([0, len(cl) - 1, 1])
        return T("Using the assumed mean a = %s and class size h = %d, find u<sub>i</sub> = (x<sub>i</sub> − a)/h for the class %d–%d." % (num(A), h, cl[i][0], cl[i][1]), num(us[i]),
                 [num(us[i] * h), num(-us[i]) if us[i] else "1", num(F(cl[i][0] - A, h)) if F(cl[i][0] - A, h) != us[i] else num(us[i] + 1)],
                 "x = %s, so u = (%s − %s)/%d = <b>%s</b>." % (num(xs[i]), num(xs[i]), num(A), h, num(us[i])))
    if kind == "fu":
        return T("Take the assumed mean a = %s and h = %d. Find Σf<sub>i</sub>u<sub>i</sub>." % (num(A), h) + t, num(fu), [num(fu * h), num(-fu) if fu else "1", num(sum(us))],
                 "u<sub>i</sub> = %s. Σf<sub>i</sub>u<sub>i</sub> = <b>%s</b>." % (", ".join(num(u) for u in us), num(fu)))
    return T("Find the mean by the step-deviation method with assumed mean a = %s (correct to 2 decimal places where needed)." % num(A) + t, d2(m),
             [d2(A + fu / n), d2(A + h * fu / len(cl)), d2(A - h * fu / n) if fu else d2(A + h)],
             "Σf<sub>i</sub> = %d, Σf<sub>i</sub>u<sub>i</sub> = %s. Mean = a + h × Σfu/Σf = %s + %d × (%s)/%d = <b>%s</b>." % (n, num(fu), num(A), h, num(fu), n, d2(m)))


# ---------------------------------------------------------------- set 3: mode
def one_mode(r):
    cl, h = classes(r)
    fr = unimodal(r, len(cl))
    i = fr.index(max(fr))
    l = cl[i][0]
    f1, f0, f2 = fr[i], fr[i - 1], fr[i + 1]
    mo = l + F(f1 - f0, 2 * f1 - f0 - f2) * h
    t = tab(cl, fr)
    if r.random() < 0.35:
        return T("What is the modal class of this data?" + t, "%d–%d" % cl[i], ["%d–%d" % cl[j] for j in (i - 1, i + 1, (i + 2) % len(cl)) if j != i][:3],
                 "The modal class has the highest frequency (%d): <b>%d–%d</b>." % (f1, cl[i][0], cl[i][1]))
    return T("Find the mode of this grouped data (correct to 2 decimal places where needed)." + t, d2(mo),
             [d2(l + F(f1 - f2, 2 * f1 - f0 - f2) * h), d2(l + F(f1 - f0, f1 + f0 + f2) * h), num(F(cl[i][0] + cl[i][1], 2)) if F(cl[i][0] + cl[i][1], 2) != mo else d2(mo + 1)],
             "Modal class %d–%d: l = %d, f₁ = %d, f₀ = %d, f₂ = %d, h = %d. Mode = l + (f₁ − f₀)/(2f₁ − f₀ − f₂) × h = %d + %d/%d × %d = <b>%s</b>." % (
                 cl[i][0], cl[i][1], l, f1, f0, f2, h, l, f1 - f0, 2 * f1 - f0 - f2, h, d2(mo)))


# ---------------------------------------------------------------- set 4: median
def one_med(r):
    cl, h = classes(r)
    fr = [r.randint(2, 15) for _ in cl]
    n = sum(fr)
    cf = []
    c = 0
    for f in fr:
        c += f
        cf.append(c)
    half = F(n, 2)
    i = next(j for j, v in enumerate(cf) if v >= half)
    if cf[i] == half:
        return None
    l = cl[i][0]
    cfb = cf[i - 1] if i else 0
    me = l + (half - cfb) / fr[i] * h
    t = tab(cl, fr)
    kind = r.choice(["med", "med", "class", "cf"])
    if kind == "class":
        return T("What is the median class of this data?" + t, "%d–%d" % cl[i], ["%d–%d" % cl[j] for j in sorted(set([fr.index(max(fr)), len(cl) - 1, max(0, i - 1), min(len(cl) - 1, i + 1)]) - {i})][:3],
                 "n = %d, n/2 = %s. The cumulative frequencies are %s; the first to reach %s is in <b>%d–%d</b>." % (n, num(half), ", ".join(str(v) for v in cf), num(half), cl[i][0], cl[i][1]))
    if kind == "cf":
        j = r.randrange(1, len(cl))
        return T("What is the cumulative frequency of the class %d–%d?" % cl[j] + t, str(cf[j]), [str(fr[j]), str(cf[j - 1]), str(n - cf[j - 1]) if n - cf[j - 1] != cf[j] else str(cf[j] + 1)],
                 "Add the frequencies up to and including this class: <b>%d</b>." % cf[j])
    return T("Find the median of this grouped data (correct to 2 decimal places where needed)." + t, d2(me),
             [d2(l + half / fr[i] * h), d2(l + (half - cf[i]) / fr[i] * h), num(F(cl[i][0] + cl[i][1], 2)) if F(cl[i][0] + cl[i][1], 2) != me else d2(me + 1)],
             "n/2 = %s, median class %d–%d: l = %d, cf = %d, f = %d, h = %d. Median = l + (n/2 − cf)/f × h = <b>%s</b>." % (num(half), cl[i][0], cl[i][1], l, cfb, fr[i], h, d2(me)))


# ---------------------------------------------------------------- set 5: problems
def one_prob(r):
    kind = r.choice(["emp", "emp", "missing", "missing", "which"])
    if kind == "emp":
        me = F(r.randint(200, 900), 10)
        mo = me + F(r.choice([-1, 1]) * r.randint(5, 60), 10)
        mean = (3 * me - mo) / 2
        want = r.choice(["mean", "mode", "median"])
        if want == "mean":
            return T("For a distribution, mode = %s and median = %s. Use the empirical relation to find the mean." % (num(mo), num(me)), d2(mean),
                     [d2((3 * mo - me) / 2), d2((mo + me) / 2), d2(3 * me - mo)], "3 Median = Mode + 2 Mean, so Mean = (3 × %s − %s)/2 = <b>%s</b>." % (num(me), num(mo), d2(mean)))
        if want == "mode":
            return T("For a distribution, mean = %s and median = %s. Use the empirical relation to find the mode." % (d2(mean), num(me)), d2(3 * me - 2 * mean),
                     [d2(3 * mean - 2 * me), d2(me + mean), d2((3 * me - mean) / 2)], "Mode = 3 Median − 2 Mean = 3 × %s − 2 × %s = <b>%s</b>." % (num(me), d2(mean), d2(3 * me - 2 * mean)))
        return T("For a distribution, mean = %s and mode = %s. Use the empirical relation to find the median." % (d2(mean), num(mo)), d2((mo + 2 * mean) / 3),
                 [d2((mean + 2 * mo) / 3), d2((mo + mean) / 2), d2(mo + 2 * mean)], "Median = (Mode + 2 Mean)/3 = (%s + 2 × %s)/3 = <b>%s</b>." % (num(mo), d2(mean), d2((mo + 2 * mean) / 3)))
    if kind == "missing":
        cl, h = classes(r, 5)
        fr = [r.randint(3, 15) for _ in cl]
        j = r.randrange(5)
        xs = [F(a + b, 2) for a, b in cl]
        m = sum(f * x for f, x in zip(fr, xs)) / sum(fr)
        if (m * 100).denominator != 1:
            return None
        shown = [str(f) if k != j else "p" for k, f in enumerate(fr)]
        t = table(["Class"] + ["%d–%d" % c for c in cl], [["Frequency"] + shown])
        return T("The mean of this distribution is %s. Find p." % d2(m) + t, "p = %d" % fr[j], ["p = %d" % (fr[j] + 1), "p = %d" % (fr[j] - 1), "p = %d" % (fr[j] + 2)],
                 "Σf = %d + p and Σfx = %s + %s p. Set Σfx/Σf = %s and solve: <b>p = %d</b>." % (sum(fr) - fr[j], num(sum(f * x for f, x in zip(fr, xs)) - fr[j] * xs[j]), num(xs[j]), d2(m), fr[j]))
    st = r.choice([
        ("Which measure of central tendency is read from the class with the highest frequency?", "Mode", ["Mean", "Median", "Range"]),
        ("Which measure of central tendency needs the cumulative frequencies?", "Median", ["Mean", "Mode", "Class mark"]),
        ("Which method is quickest for the mean when the class marks are large and equally spaced?", "Step-deviation method", ["Direct method", "Mode formula", "Counting the classes"]),
        ("In the formulae for grouped data, which value represents a whole class?", "Its class mark (mid-point)", ["Its lower limit", "Its upper limit", "Its frequency"]),
        ("What is the empirical relationship between the three measures of central tendency?", "3 Median = Mode + 2 Mean", ["3 Mean = Mode + 2 Median", "Mode = Mean + Median", "2 Median = Mode + Mean"]),
        ("Which measure is best for 'the most popular shoe size sold'?", "Mode", ["Mean", "Median", "Cumulative frequency"]),
        ("Which measure is least affected by a few extremely large values?", "Median", ["Mean", "Sum of the data", "Range"]),
    ])
    return T(st[0], st[1], st[2], "<b>%s</b>." % st[1])


def main():
    seen = set()
    sets = [
        S("Mean: direct method", mix(R, [(one_direct, 20)], seen)),
        S("Mean: assumed mean and step deviation", mix(R, [(one_step, 20)], seen)),
        S("Mode of grouped data", mix(R, [(one_mode, 20)], seen)),
        S("Median of grouped data", mix(R, [(one_med, 20)], seen)),
        S("Problems and the empirical relation", mix(R, [(one_prob, 20)], seen)),
    ]
    body = lesson(
        "<p>In grouped data each class is represented by its <b>class mark</b> x = (lower limit + upper limit)/2.</p>"
        "<p><b>Mean</b> = Σf<sub>i</sub>x<sub>i</sub>/Σf<sub>i</sub>. With an assumed mean a and class size h: mean = a + h × Σf<sub>i</sub>u<sub>i</sub>/Σf<sub>i</sub>, where u = (x − a)/h.</p>"
        "<p><b>Mode</b> = l + (f₁ − f₀)/(2f₁ − f₀ − f₂) × h (modal class). <b>Median</b> = l + (n/2 − cf)/f × h (median class). Empirical relation: 3 Median = Mode + 2 Mean.</p>",
        [("Classes 0–10, 10–20, 20–30 with frequencies 4, 6, 10. Find the mean.", ["Class marks 5, 15, 25", "Σfx = 20 + 90 + 250 = 360, Σf = 20"], "18"),
         ("Modal class 40–50 with f₁ = 12, f₀ = 7, f₂ = 9. Find the mode.", ["40 + (12 − 7)/(24 − 7 − 9) × 10", "40 + 5/8 × 10"], "46.25")],
        ["Multiplying the frequencies by the lower limits. Use the class marks.",
         "Using f₁ − f₂ on top in the mode formula. It is f₁ − f₀ (the class before).",
         "Using the cumulative frequency of the median class itself. cf is the cumulative frequency of the class before it."])
    faq = [
        ("How do I find the mean of grouped data?", "Find the class marks xᵢ, multiply by the frequencies, add, and divide by the total frequency: mean = Σfᵢxᵢ/Σfᵢ."),
        ("What is the formula for the mode of grouped data?", "Mode = l + (f₁ − f₀)/(2f₁ − f₀ − f₂) × h, where l is the lower limit of the modal class and f₀, f₂ are the frequencies of the classes before and after it."),
        ("What is the formula for the median of grouped data?", "Median = l + (n/2 − cf)/f × h, where cf is the cumulative frequency of the class before the median class."),
        ("What is the empirical relationship between mean, median and mode?", "3 Median = Mode + 2 Mean (for moderately skewed data)."),
    ]
    make(10, "statistics", 13, "VII", 13, "Statistics: Mean, Median and Mode of Grouped Data", "statistics",
         "Mean, median and mode of grouped data (bimodal situation to be avoided) (summary of the CBSE syllabus)",
         "Class 10 Statistics worksheet (NCERT Chapter 13): mean by direct, assumed mean and step-deviation methods, mode and median of grouped data, empirical relation. 100 questions with answers.",
         "Mean = Σfx ÷ Σf", "Mode = l + (f₁ − f₀)/(2f₁ − f₀ − f₂) × h; Median = l + (n/2 − cf)/f × h.",
         body, faq, sets, R)


if __name__ == "__main__":
    main()
