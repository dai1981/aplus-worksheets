# -*- coding: utf-8 -*-
"""
US Grade 6 Math: Mean, Median, Mode and Range (6.SP.A.3, 6.SP.B.5c)
  python tools/gen_us_math_g6_mean_median.py
All data are whole numbers. Every answer is computed with fractions.Fraction and written as a whole
number or a terminating decimal (answers are whole numbers or end in .5).
IQR rule (same in the lesson): sort, split at the median; when the count is odd the middle value is left
out of both halves; Q1 / Q3 = medians of the lower / upper half.
Wrong choices come from real mistakes; a choice never has the same value as the right answer.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, os, random, re
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "us", "math", "grade-6")
UPDATED = "2026-11-02"
GREEN = "#006633"
INK = "#2b2b2b"
MINUS = "−"
GIRLS = ["Maya", "Ava", "Mia", "Zoe", "Lily", "Emma", "Nora", "Ruby", "Sofia", "Grace", "Chloe", "Hana"]
BOYS = ["Leo", "Noah", "Eli", "Sam", "Ben", "Omar", "Kai", "Jack", "Luis", "Owen", "Max", "Theo"]
TEACHERS = ["Ms. Lee", "Mr. Diaz", "Mrs. Patel", "Ms. Brown", "Mr. Kim", "Mrs. Green"]
ORD = {1: "1st", 2: "2nd", 3: "3rd"}


# ------------------------------------------------------------ numbers
def clean(x):
    """True if x can be written as a decimal with at most 2 places."""
    d = F(x).denominator
    return 100 % d == 0


def fmt(x):
    x = F(x)
    neg = x < 0
    x = abs(x)
    w, r = divmod(x.numerator, x.denominator)
    s = "{:,}".format(w)
    if r:
        assert clean(x), x
        dec = ("%.2f" % float(F(r, x.denominator)))[1:].rstrip("0")
        s += dec
    return (MINUS if neg else "") + s


def ordn(k):
    return ORD.get(k, "%dth" % k)


def lst(v):
    return ", ".join(fmt(x) for x in v)


def plus(v):
    return " + ".join(fmt(x) for x in v)


def median(v):
    s = sorted(v)
    n = len(s)
    if n % 2:
        return F(s[n // 2])
    return F(s[n // 2 - 1] + s[n // 2], 2)


def mean(v):
    return F(sum(v), len(v))


def freq(v):
    out = {}
    for x in v:
        out[x] = out.get(x, 0) + 1
    return out


def halves(v):
    s = sorted(v)
    n = len(s)
    return s[:n // 2], s[(n + 1) // 2:]


def quart(v):
    lo, hi = halves(v)
    return median(lo), median(hi)


def nword(n, one, many):
    return "%s %s" % (fmt(n), one if n == 1 else many)


# ------------------------------------------------------------ explanations
def e_sort(v):
    return "Sort first: %s." % lst(sorted(v))


def e_median(v, bold=True):
    s = sorted(v)
    n = len(s)
    b = (lambda t: "<b>%s</b>" % t) if bold else (lambda t: t)
    if n % 2:
        k = n // 2 + 1
        return "%s With %d values, the middle one is the %s: %s." % (e_sort(v), n, ordn(k), b(fmt(s[k - 1])))
    a, c = s[n // 2 - 1], s[n // 2]
    t = "%s With %d values, there are two middle values, the %s and %s: %s and %s. " % (
        e_sort(v), n, ordn(n // 2), ordn(n // 2 + 1), fmt(a), fmt(c))
    if a == c:
        return t + "Both are %s, so the median is %s." % (fmt(a), b(fmt(a)))
    return t + "The median is their mean: (%s + %s) ÷ 2 = %s." % (fmt(a), fmt(c), b(fmt(median(v))))


def e_mean(v, bold=True):
    m = mean(v)
    t = fmt(m) if not bold else "<b>%s</b>" % fmt(m)
    return "Add the values: %s = %s. There are %d values, so divide by %d: %s ÷ %d = %s." % (
        plus(v), fmt(sum(v)), len(v), len(v), fmt(sum(v)), len(v), t)


def e_range(v):
    return "Range = greatest − least = %s − %s = <b>%s</b>." % (fmt(max(v)), fmt(min(v)), fmt(max(v) - min(v)))


# ------------------------------------------------------------ helpers
def mcq(q, cs, cands, e, rnd):
    """cs: correct string. cands: strings. Picks the first 3 different ones."""
    seen, pick = {cs}, []
    for c in cands:
        if c is None or c in seen:
            continue
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, cs, cands)
    ch = pick + [cs]
    rnd.shuffle(ch)
    return {"q": q, "c": ch, "a": ch.index(cs), "e": e}


def mcq_n(q, ans, cands, e, rnd, unit=None):
    """ans and cands are numbers (Fraction/int). Wrong choices must be positive, clean and different in value."""
    ans = F(ans)
    s = (lambda x: fmt(x) + unit) if unit else fmt
    vals, cc = set(), []
    for c in cands:
        if c is None:
            continue
        c = F(c)
        if c <= 0 or c == ans or c in vals or not clean(c):
            continue
        vals.add(c)
        cc.append(s(c))
    return mcq(q, s(ans), cc, e, rnd)


def fills(ans, step=1):
    a = F(ans)
    return [a + step, a - step, a + 2 * step, a - 2 * step, a + 3 * step]


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'>%s</svg>" % (w, h, w, h, label, body))


class People:
    def __init__(self, rnd):
        self.pool = [(n, "she", "her") for n in GIRLS] + [(n, "he", "his") for n in BOYS]
        rnd.shuffle(self.pool)
        self.i = 0

    def next(self):
        p = self.pool[self.i % len(self.pool)]
        self.i += 1
        return p


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def mark_large(u, pattern):
    """Tag pictures that must print larger so their labels stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def balance(sets, rnd):
    """Move the correct choice so each position (A to D) is the answer 5 times in every set."""
    for st in sets:
        pos = [0, 1, 2, 3] * 5
        rnd.shuffle(pos)
        for it, t in zip(st["items"], pos):
            ch = it["c"]
            ch[it["a"]], ch[t] = ch[t], ch[it["a"]]
            it["a"] = t


# ------------------------------------------------------------ dot plot picture
FS = 19


def plot_svg(lo, counts, title, what):
    n = len(counts)
    mxc = max(max(counts), 1)
    pad = 30
    gap = max(44, int(320 / (n - 1)))
    W = int(2 * pad + gap * (n - 1))
    Y = 30 + 16 * (mxc - 1)
    H = Y + 62
    X = lambda i: pad + gap * i
    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (pad - 18, Y, W - pad + 18, Y, INK)]
    for i in range(n):
        x = X(i)
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.8'/>" % (x, Y - 6, x, Y + 6, INK))
        s.append("<text x='%d' y='%d' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%d</text>"
                 % (x, Y + 28, FS, INK, lo + i))
        for k in range(counts[i]):
            cy = Y - 18 - 16 * k
            s.append("<path d='M%d %d L%d %d M%d %d L%d %d' stroke='%s' stroke-width='2.4' stroke-linecap='round'/>"
                     % (x - 6, cy - 6, x + 6, cy + 6, x - 6, cy + 6, x + 6, cy - 6, GREEN))
    s.append("<text x='%d' y='%d' font-size='14' fill='%s' text-anchor='middle'>%s</text>" % (W / 2, Y + 54, INK, title))
    lab = "dot plot of %s from %d to %d" % (what, lo, lo + n - 1)
    return svg_wrap(W, H, "".join(s), lab)


# ------------------------------------------------------------ data contexts (lists)
def C(**k):
    return k


# t: sentence before the list. {n} = how many, {name}/{pro}/{pos} = a person. lo/hi = realistic values.
# u: unit word for explanations. hi_ok: largest value that still makes sense (for outliers).
LIST_CTX = [
    C(t="The ages of {n} cousins, in years, are", lo=3, hi=17, u="years"),
    C(t="{name} did push-ups every day for {n} days. The numbers of push-ups {pro} did are", lo=10, hi=40, u="push-ups"),
    C(t="{name} scored these points in {n} basketball games:", lo=6, hi=28, u="points"),
    C(t="The high temperatures, in °F, for {n} days in May were", lo=61, hi=84, u="°F"),
    C(t="A teacher asked {n} students to time their walk to school. The times, in minutes, are", lo=4, hi=25, u="minutes"),
    C(t="{name}'s scores on {n} spelling tests (out of 20) are", lo=11, hi=20, u="points"),
    C(t="The prices of {n} books at a used-book sale, in dollars, are", lo=2, hi=15, u="dollars"),
    C(t="The heights of {n} tomato plants, in inches, are", lo=12, hi=34, u="inches"),
    C(t="The weights of {n} puppies at a shelter, in pounds, are", lo=5, hi=24, u="pounds"),
    C(t="The numbers of students on {n} school buses are", lo=28, hi=52, u="students"),
    C(t="{name} read every day for {n} days. The numbers of pages {pro} read are", lo=12, hi=45, u="pages"),
    C(t="{name} counted the birds at a feeder on {n} mornings. The counts are", lo=3, hi=22, u="birds"),
    C(t="The times, in seconds, of {n} runners in a 100-meter race are", lo=13, hi=22, u="seconds"),
    C(t="At swim practice, {n} swimmers counted their laps. The numbers of laps are", lo=8, hi=30, u="laps"),
    C(t="{name} saved money for {n} weeks. The amounts {pro} saved, in dollars, are", lo=4, hi=25, u="dollars"),
    C(t="The numbers of cars in a parking lot at {n} different times were", lo=20, hi=60, u="cars"),
]


class Ctx:
    def __init__(self, rnd, pool):
        self.rnd = rnd
        self.pool = list(pool)
        rnd.shuffle(self.pool)
        self.i = 0

    def next(self):
        c = self.pool[self.i % len(self.pool)]
        self.i += 1
        return c


def say(c, n, P):
    name, pro, pos = P.next()
    return c["t"].format(n=n, name=name, pro=pro, pos=pos)


def dq(c, v, P, ask):
    """Question with the data list in bold."""
    t = say(c, len(v), P)
    return "%s <b>%s</b>. %s" % (t, lst(v), ask)


def rand_vals(rnd, c, n, distinct=False):
    lo, hi = c["lo"], c["hi"]
    if distinct:
        return rnd.sample(range(lo, hi + 1), n)
    return [rnd.randint(lo, hi) for _ in range(n)]


# ============================================================ set 1: median, mode and range
def set_mmr(rnd, P, CC):
    kinds = (["med_odd"] * 4 + ["med_even"] * 5 + ["mode"] * 4 + ["range"] * 4 + ["bimodal"] * 2 + ["nomode"])
    order = ["med_odd", "mode", "range", "med_even", "med_odd", "mode", "range", "med_even", "med_odd", "mode",
             "range", "med_even", "bimodal", "med_odd", "mode", "range", "med_even", "nomode", "bimodal", "med_even"]
    assert sorted(order) == sorted(kinds)
    its = []
    even_half = [True, False, True, False, True]
    ie = 0
    for kind in order:
        c = CC.next()
        if kind == "med_odd":
            for _ in range(2000):
                n = rnd.choice([5, 7, 9])
                v = rand_vals(rnd, c, n)
                s = sorted(v)
                m = n // 2
                if v[m] != s[m] and s[m - 1] != s[m] and s[m + 1] != s[m] and len(set(v)) >= n - 1:
                    break
            ans = median(v)
            q = dq(c, v, P, "What is the median?")
            e = e_median(v) + " (The middle of the unsorted list, %s, is not the median.)" % fmt(v[m])
            its.append(mcq_n(q, ans, [v[m], s[m - 1], s[m + 1], mean(v)] + fills(ans), e, rnd))
        elif kind == "med_even":
            want_half = even_half[ie]
            ie += 1
            for _ in range(5000):
                n = rnd.choice([6, 8, 10])
                v = rand_vals(rnd, c, n)
                s = sorted(v)
                a, b = s[n // 2 - 1], s[n // 2]
                um = F(v[n // 2 - 1] + v[n // 2], 2)
                if a != b and ((a + b) % 2 == 1) == want_half and um != median(v) and len(set(v)) >= n - 1:
                    break
            ans = median(v)
            q = dq(c, v, P, "What is the median?")
            e = e_median(v)
            its.append(mcq_n(q, ans, [a, b, um, a + b, mean(v)] + fills(ans), e, rnd))
        elif kind == "mode":
            for _ in range(2000):
                n = rnd.choice([7, 8, 9, 10])
                base = rnd.sample(range(c["lo"], c["hi"] + 1), n - 3)
                md, sec = base[0], base[1]
                v = base + [md, md, sec]
                rnd.shuffle(v)
                if v.index(md) > 1 and md != 3 and median(v) != md:
                    break
            q = dq(c, v, P, "What is the mode?")
            e = ("Count how many times each value appears: %s appears 3 times, more than any other value. "
                 "The mode is the value <b>%s</b>, not the count 3." % (fmt(md), fmt(md)))
            its.append(mcq_n(q, md, [3, sec, median(v), max(v), v[0]] + fills(md), e, rnd))
        elif kind == "range":
            for _ in range(2000):
                n = rnd.choice([6, 7, 8, 9])
                v = rand_vals(rnd, c, n)
                r = max(v) - min(v)
                if v[0] not in (max(v), min(v)) and v[-1] not in (max(v), min(v)) and abs(v[-1] - v[0]) != r and r > 3:
                    break
            q = dq(c, v, P, "What is the range?")
            s = sorted(v)
            its.append(mcq_n(q, r, [max(v), abs(v[-1] - v[0]), s[-1] - s[1], s[-2] - s[0], max(v) + min(v)] + fills(r),
                             e_range(v) + " Use the greatest and least values, not the first and last in the list.", rnd))
        elif kind == "bimodal":
            for _ in range(2000):
                n = rnd.choice([8, 9, 10])
                base = rnd.sample(range(c["lo"], c["hi"] + 1), n - 2)
                a, b = sorted(base[:2])
                v = base + [a, b]
                rnd.shuffle(v)
                if True:
                    break
            q = dq(c, v, P, "What is the mode?")
            cs = "%s and %s" % (fmt(a), fmt(b))
            e = ("%s and %s each appear 2 times. Every other value appears once. A data set can have two modes: "
                 "<b>%s</b>." % (fmt(a), fmt(b), cs))
            its.append(mcq(q, cs, [fmt(a), fmt(b), "no mode", "2"], e, rnd))
        else:  # no mode
            n = rnd.choice([6, 7])
            v = rand_vals(rnd, c, n, distinct=True)
            q = dq(c, v, P, "What is the mode?")
            e = ("Each value appears only once, so no value is more common than the others. The data set has "
                 "<b>no mode</b>. (The mode is never a count like 1.)")
            cands = ["1", fmt(median(v)), fmt(v[0]), fmt(max(v))]
            its.append(mcq(q, "no mode", cands, e, rnd))
    return {"title": "Median, mode and range", "items": its}


# ============================================================ set 2: find the mean
TOTAL_CTX = [
    ("The mean of {n} test scores is {m}. What is the sum of the {n} scores?", "points", 72, 92),
    ("{name} read for {n} days. {Pro} read a mean of {m} pages per day. How many pages did {pro} read in all?", "pages", 18, 40),
    ("A team scored a mean of {m} points per game in {n} games. How many points did the team score in all?", "points", 41, 68),
    ("The mean weight of {n} backpacks is {m} pounds. What is the total weight of the backpacks?", "pounds", 9, 17),
]


def set_mean(rnd, P, CC):
    order = ["whole"] * 5 + ["half"] + ["whole"] * 3 + ["total"] + ["whole"] * 2 + ["half"] + ["total"] + \
            ["whole"] * 2 + ["half", "total", "whole", "half"]
    assert len(order) == 20
    its = []
    tc = list(TOTAL_CTX)
    rnd.shuffle(tc)
    ti = 0
    for kind in order:
        if kind == "total":
            t, unit, lo, hi = tc[ti]
            ti += 1
            n = rnd.choice([5, 6, 7, 8])
            m = rnd.randint(lo, hi)
            name, pro, pos = P.next()
            q = t.format(n=n, m=m, name=name, pro=pro, Pro=pro.capitalize())
            ans = n * m
            e = ("Mean = sum ÷ count, so sum = mean × count. Sum = %d × %d = <b>%s</b> %s."
                 % (m, n, fmt(ans), unit))
            its.append(mcq_n(q, ans, [m + n, (n - 1) * m, (n + 1) * m, F(m, n) if m % n == 0 else None] + fills(ans, 10),
                             e, rnd))
            continue
        c = CC.next()
        for _ in range(5000):
            if kind == "half":
                n = rnd.choice([6, 8])
            else:
                n = rnd.choice([5, 6, 7, 8])
            v = rand_vals(rnd, c, n)
            m = mean(v)
            if kind == "half" and m.denominator != 2:
                continue
            if kind == "whole" and m.denominator != 1:
                continue
            if median(v) == m:
                continue
            break
        S = sum(v)
        q = dq(c, v, P, "What is the mean?")
        cands = [F(S, n - 1), F(S, n + 1), median(v), F(max(v) + min(v), 2), F(S, len(set(v))) if len(set(v)) < n else None]
        cands = [x for x in cands if x is not None and clean(x)]
        its.append(mcq_n(q, m, [S] + cands + fills(m), e_mean(v), rnd))
    return {"title": "Find the mean", "items": its}


# ============================================================ set 3: read a dot plot
DOT_CTX = [
    C(t="A class survey asked {n} students how many books they read last month.", title="Books read last month", what="books read", lo=0, hi=8, x="student"),
    C(t="The dot plot shows the goals {name}'s soccer team scored in {n} games.", title="Goals per game", what="goals per game", lo=0, hi=6, x="game"),
    C(t="In a class, {n} students took a 10-point quiz. The dot plot shows their scores.", title="Quiz score (points)", what="quiz scores", lo=3, hi=10, x="student"),
    C(t="In a survey, {n} students counted the pets they have at home.", title="Number of pets", what="number of pets", lo=0, hi=5, x="student"),
    C(t="The dot plot shows how many hours each of {n} band members practiced last week.", title="Hours of practice", what="hours of practice", lo=1, hi=8, x="band member"),
    C(t="In a class, {n} students counted the letters in their first names.", title="Letters in first name", what="letters in first names", lo=3, hi=9, x="student"),
    C(t="In a survey, {n} students recorded how many hours they slept last night.", title="Hours of sleep", what="hours of sleep", lo=6, hi=11, x="student"),
    C(t="The dot plot shows how many runs a softball team scored in each of {n} games.", title="Runs per game", what="runs per game", lo=0, hi=8, x="game"),
]


def make_counts(rnd, c, N, ok):
    lo, hi = c["lo"], c["hi"]
    nm = hi - lo + 1
    for _ in range(20000):
        md = rnd.uniform(0, nm - 1)
        cn = [0] * nm
        for _ in range(N):
            cn[int(round(rnd.triangular(0, nm - 1, md)))] += 1
        if max(cn) > 5:
            continue
        vals = [lo + i for i in range(nm) for _ in range(cn[i])]
        if ok(cn, vals):
            return cn, vals
    raise RuntimeError("no plot for %s" % c["title"])


def tallest(cn):
    m = max(cn)
    return [i for i in range(len(cn)) if cn[i] == m]


def set_dot(rnd, P, CC):
    order = ["count", "mode", "range", "median", "mean", "mode", "median", "range", "mean", "count",
             "median", "mean", "range", "mode", "median", "mean", "range", "median", "mean", "mean"]
    assert len(order) == 20
    its = []
    for kind in order:
        c = CC.next()
        lo = c["lo"]
        nm = c["hi"] - lo + 1
        name, pro, pos = P.next()
        if kind == "count":
            N = rnd.randint(9, 15)
            cn, v = make_counts(rnd, c, N, lambda cn, v: True)
            ask = "How many %ss are shown on the dot plot?" % c["x"]
            e = "Each X is one %s. Add the X's in every column: %s = <b>%d</b>." % (
                c["x"], " + ".join(str(x) for x in cn if x), N)
            cands = [nm, sum(1 for x in cn if x), max(cn), lo + nm - 1, N + 1, N - 1]
            ans = N
        elif kind == "mode":
            N = rnd.randint(9, 14)
            cn, v = make_counts(rnd, c, N, lambda cn, v: len(tallest(cn)) == 1 and lo + tallest(cn)[0] != max(cn)
                                and lo + tallest(cn)[0] > 0)
            i = tallest(cn)[0]
            ans = lo + i
            sec = sorted(range(nm), key=lambda k: (-cn[k], k))[1]
            ask = "What is the mode of the data?"
            e = ("The tallest stack of X's is above %d, so the mode is <b>%d</b>. "
                 "(The stack has %d X's, but the mode is the value, not the count.)" % (ans, ans, max(cn)))
            cands = [max(cn), lo + sec, median(v), lo + (nm - 1) // 2 if nm % 2 else None, N]
        elif kind == "range":
            N = rnd.randint(8, 14)
            cn, v = make_counts(rnd, c, N, lambda cn, v: (cn[0] == 0 or cn[-1] == 0) and max(v) - min(v) >= 2)
            ans = max(v) - min(v)
            ask = "What is the range of the data?"
            e = ("The X farthest to the left is at %d and the X farthest to the right is at %d. "
                 "Range = %d − %d = <b>%d</b>. Use the X's, not the ends of the number line."
                 % (min(v), max(v), max(v), min(v), ans))
            cands = [nm - 1, max(v), N, lo + nm - 1, max(cn), ans + 1, ans - 1]
        elif kind == "median":
            N = rnd.randint(9, 14)
            mid_line = F(2 * lo + nm - 1, 2)

            cn, v = make_counts(rnd, c, N, lambda cn, v: median(v) != mid_line)
            ans = median(v)
            ask = "What is the median of the data?"
            if N % 2:
                k = N // 2 + 1
                e = ("There are %d X's. The median is the %s X when you count from the left. It is above %d, "
                     "so the median is <b>%d</b>." % (N, ordn(k), v[k - 1], v[k - 1]))
            else:
                k = N // 2
                a, b = v[k - 1], v[k]
                if a == b:
                    e = ("There are %d X's. The two middle X's are the %s and %s from the left. Both are above %d, "
                         "so the median is <b>%d</b>." % (N, ordn(k), ordn(k + 1), a, a))
                else:
                    e = ("There are %d X's. The two middle X's are the %s and %s from the left, above %d and %d. "
                         "Median = (%d + %d) ÷ 2 = <b>%s</b>." % (N, ordn(k), ordn(k + 1), a, b, a, b, fmt(ans)))
            ti = tallest(cn)
            cands = [mid_line, lo + ti[0], mean(v), ans + F(1, 2) if N % 2 == 0 else None, ans + 1, ans - 1, N // 2]
            cands = [x for x in cands if x is not None]
        else:  # mean
            N = rnd.randint(8, 12)
            cn, v = make_counts(rnd, c, N, lambda cn, v: mean(v).denominator in (1, 2) and mean(v) != median(v)
                                and sum(1 for x in cn if x) >= 4)
            ans = mean(v)
            S = sum(v)
            ask = "What is the mean of the data?"
            parts = ["%d × %d" % (lo + i, cn[i]) for i in range(nm) if cn[i]]
            e = ("Multiply each value by its number of X's and add: %s = %d. There are %d X's, so divide by %d: "
                 "%d ÷ %d = <b>%s</b>." % (" + ".join(parts), S, N, N, S, N, fmt(ans)))
            used = sum(1 for x in cn if x)
            cands = [F(S, used), F(S, nm), median(v), F(sum(lo + i for i in range(nm) if cn[i]), used), S]
        q = fig(plot_svg(lo, cn, c["title"], c["what"])) + c["t"].format(n=N, name=name) + " " + ask
        its.append(mcq_n(q, ans, cands + fills(ans), e, rnd))
    return {"title": "Read a dot plot", "items": its}


# ============================================================ set 4: outliers, IQR and missing values
OUT_CTX = [
    C(t="{name} recorded how long, in minutes, {pro} spent on homework on {n} nights:", lo=25, hi=45, out=(5, 10), u="minutes"),
    C(t="The prices, in dollars, of {n} T-shirts in a store are", lo=12, hi=20, out=(48, 60), u="dollars"),
    C(t="The numbers of visitors to a small museum on {n} days were", lo=40, hi=70, out=(150, 190), u="visitors"),
    C(t="The weights, in pounds, of {n} dogs at a dog park are", lo=18, hi=34, out=(85, 110), u="pounds"),
    C(t="{name} counted the emails {pro} got on {n} days:", lo=10, hi=20, out=(55, 70), u="emails"),
    C(t="The ages of {n} people at a family picnic are", lo=30, hi=45, out=(2, 6), u="years"),
    C(t="The heights, in inches, of {n} sunflowers are", lo=58, hi=74, out=(20, 26), u="inches"),
    C(t="The numbers of pages in {n} books on a shelf are", lo=180, hi=260, out=(620, 700), u="pages"),
    C(t="{name} rode {pos} bike to school on {n} days. The times, in minutes, were", lo=12, hi=18, out=(40, 46), u="minutes"),
]


def outlier_data(rnd, c, n, ok=lambda v, x: True):
    for _ in range(20000):
        base = [rnd.randint(c["lo"], c["hi"]) for _ in range(n - 1)]
        x = rnd.randint(*c["out"])
        v = base + [x]
        rnd.shuffle(v)
        if ok(v, x):
            return v, x
    raise RuntimeError(c["t"])


def set_outlier(rnd, P, CC):
    order = ["which_out", "remove", "typical", "add", "missing", "iqr", "variation", "which_out", "remove", "typical",
             "add", "missing", "iqr", "which_out", "remove", "typical", "add", "missing", "variation", "iqr"]
    assert len(order) == 20
    its = []
    iqr_n = [8, 9, 7]
    ii = 0
    for kind in order:
        if kind == "which_out":
            c = CC.next()
            v, x = outlier_data(rnd, c, rnd.choice([7, 8]), lambda v, x: len(set(v)) >= 6)
            rest = [y for y in v if y != x]
            q = dq(c, v, P, "Which value is an outlier?")
            e = ("Most values are between %s and %s. The value <b>%s</b> is far away from all the others, "
                 "so it is an outlier." % (fmt(min(rest)), fmt(max(rest)), fmt(x)))
            near = max(rest) if x > max(rest) else min(rest)
            far = min(rest) if x > max(rest) else max(rest)
            its.append(mcq_n(q, x, [near, far, median(v), sorted(rest)[len(rest) // 2]], e, rnd))
        elif kind == "remove":
            c = CC.next()
            v, x = outlier_data(rnd, c, rnd.choice([6, 7]),
                                lambda v, x: mean([y for y in v if y != x]).denominator == 1 and mean(v).denominator in (1, 2)
                                and v.count(x) == 1)
            rest = [y for y in v if y != x]
            n, S = len(v), sum(v)
            ans = mean(rest)
            q = dq(c, v, P, "The outlier, %s, is removed. What is the mean of the other values?" % fmt(x))
            e = ("Without %s there are %d values. Their sum is %s = %s. Mean = %s ÷ %d = <b>%s</b>. "
                 "(With the outlier the mean was %s ÷ %d = %s.)" % (
                     fmt(x), n - 1, plus(rest), fmt(sum(rest)), fmt(sum(rest)), n - 1, fmt(ans), fmt(S), n, fmt(mean(v))))
            its.append(mcq_n(q, ans, [F(S - x, n), mean(v), median(rest), F(S, n - 1)] + fills(ans), e, rnd))
        elif kind == "typical":
            c = CC.next()
            v, x = outlier_data(rnd, c, rnd.choice([7, 8]),
                                lambda v, x: mean(v).denominator == 1 and median(v).denominator == 1 and v.count(x) == 1
                                and ((x > max(y for y in v if y != x) and mean(v) > max(y for y in v if y != x)) or
                                     (x < min(y for y in v if y != x) and mean(v) < min(y for y in v if y != x))))
            m, md, r = mean(v), median(v), max(v) - min(v)
            q = dq(c, v, P, "Which measure best describes a typical value?")
            side = "greater" if x > md else "less"
            pull = "up" if x > md else "down"
            cs = "the median, %s" % fmt(md)
            e = ("The outlier %s pulls the mean %s to %s, which is %s than every other value. "
                 "The median, %s, stays in the middle of the data, so <b>the median</b> describes a typical value better."
                 % (fmt(x), pull, fmt(m), side, fmt(md)))
            its.append(mcq(q, cs, ["the mean, %s" % fmt(m), "the range, %s" % fmt(r),
                                   "the %s, %s" % ("greatest value" if x > md else "least value", fmt(x))], e, rnd))
        elif kind == "variation":
            c = CC.next()
            for _ in range(5000):
                n = rnd.choice([7, 8])
                base = [rnd.randint(c["lo"], c["hi"]) for _ in range(n - 1)]
                v = base + [base[0]]
                rnd.shuffle(v)
                f = freq(v)
                top = max(f.values())
                modes = [k for k in f if f[k] == top]
                m, md, r = mean(v), median(v), max(v) - min(v)
                if (len(modes) == 1 and m.denominator == 1 and md.denominator == 1
                        and len({m, md, modes[0], r}) == 4):
                    break
            q = dq(c, v, P, "Which number describes how much the values vary?")
            cs = "the range, %s" % fmt(r)
            e = ("The mean, median and mode are measures of center: each gives one typical value. "
                 "The range is a measure of variation: %s − %s = %s tells how spread out the values are. So the answer is <b>%s</b>."
                 % (fmt(max(v)), fmt(min(v)), fmt(r), cs))
            its.append(mcq(q, cs, ["the mean, %s" % fmt(m), "the median, %s" % fmt(md), "the mode, %s" % fmt(modes[0])],
                           e, rnd))
        elif kind == "add":
            c = CC_LIST.next()
            for _ in range(5000):
                n = rnd.choice([4, 5])
                v = rand_vals(rnd, c, n)
                x = rnd.randint(c["lo"], c["hi"])
                m0, m1 = mean(v), mean(v + [x])
                if (m0.denominator == 1 and m1.denominator in (1, 2) and abs(x - m0) >= 4
                        and F(m0 + x, 2) != m1 and median(v + [x]) != m1):
                    break
            S = sum(v)
            q = dq(c, v, P, "The mean is %s. The value %s is added to the data. What is the new mean?" % (fmt(m0), fmt(x)))
            e = ("The new sum is %s + %s = %s, and now there are %d values. New mean = %s ÷ %d = <b>%s</b>. "
                 "(Do not just average the old mean and the new value.)" % (
                     fmt(S), fmt(x), fmt(S + x), n + 1, fmt(S + x), n + 1, fmt(m1)))
            its.append(mcq_n(q, m1, [F(m0 + x, 2), F(S + x, n), m0, median(v + [x])] + fills(m1), e, rnd))
        elif kind == "missing":
            for _ in range(5000):
                n = rnd.choice([5, 6])
                m = rnd.randint(12, 30)
                known = [rnd.randint(m - 8, m + 8) for _ in range(n - 1)]
                ans = n * m - sum(known)
                if 3 <= ans <= m + 15 and ans not in known and abs(ans - m) >= 2 and (n - 1) * m - sum(known) != 0:
                    break
            q = ("The mean of %d numbers is %d. Four of them are " if n == 5 else "The mean of %d numbers is %d. Five of them are ") % (n, m)
            q += "<b>%s</b>. What is the missing number?" % lst(known)
            e = ("The sum of all %d numbers must be %d × %d = %d. The known numbers add to %s = %d. "
                 "Missing number = %d − %d = <b>%d</b>." % (n, n, m, n * m, plus(known), sum(known), n * m, sum(known), ans))
            its.append(mcq_n(q, ans, [(n - 1) * m - sum(known), m, n * m, F(sum(known), n - 1)] + fills(ans), e, rnd))
        else:  # iqr
            c = CC_LIST.next()
            n = iqr_n[ii]
            ii += 1
            for _ in range(5000):
                v = rand_vals(rnd, c, n)
                s = sorted(v)
                q1, q3 = quart(v)
                incl = None
                if n % 2:
                    incl = median(s[:n // 2 + 1]), median(s[n // 2:])
                ok = (q1.denominator == 1 and q3.denominator == 1 and q3 - q1 >= 3 and len(set(v)) >= n - 1
                      and q3 - q1 != max(v) - min(v) and q3 - q1 != q3 - median(v))
                if n % 2:
                    ok = ok and (incl[1] - incl[0]) != q3 - q1
                if ok:
                    break
            ans = q3 - q1
            lo_h, hi_h = halves(v)
            md = median(v)
            if n % 2:
                split = "The median is %s. Leave it out of both halves. " % fmt(md)
            else:
                split = "The median is %s. " % fmt(md)
            e = ("%s %sLower half: %s, so Q1 = %s. Upper half: %s, so Q3 = %s. IQR = Q3 − Q1 = %s − %s = <b>%s</b>."
                 % (e_sort(v), split, lst(lo_h), fmt(q1), lst(hi_h), fmt(q3), fmt(q3), fmt(q1), fmt(ans)))
            q = dq(c, v, P, "What is the interquartile range (IQR)?")
            cands = [max(v) - min(v), q3, q3 - md, md - q1]
            if n % 2:
                cands.insert(1, incl[1] - incl[0])
            its.append(mcq_n(q, ans, cands + fills(ans), e, rnd))
    return {"title": "Outliers, IQR and missing values", "items": its}


# ============================================================ set 5: word problems
def set_word(rnd, P):
    its = []

    # --- needed score on the last test / game (4)
    NEED = [
        ("test", "tests", "scores", 85, 72, 96, 4, "score"),
        ("test", "tests", "scores", 90, 80, 99, 3, "score"),
        ("bowling game", "bowling games", "scores", 120, 98, 140, 4, "score"),
        ("basketball game", "basketball games", "points", 18, 10, 26, 5, "points"),
    ]
    for one, many, what, T, lo, hi, k, word in NEED:
        name, pro, pos = P.next()
        for _ in range(5000):
            v = [rnd.randint(lo, hi) for _ in range(k)]
            ans = (k + 1) * T - sum(v)
            top = 100 if one == "test" else (200 if "bowling" in one else 40)
            cur = mean(v)
            if (lo <= ans <= min(hi + 8, top) and ans != T and clean(2 * T - cur)
                    and 2 * T - cur != ans and abs(ans - T) >= 3):
                break
        if one == "test":
            q = ("%s's %s on the first %d %s are <b>%s</b>. What score does %s need on the %s test to have a mean score of %d?"
                 % (name, what, k, many, lst(v), pro, ordn(k + 1), T))
        elif "bowling" in one:
            q = ("%s's scores in %d bowling games are <b>%s</b>. What score does %s need in the next game to average %d "
                 "for all %d games?" % (name, k, lst(v), pro, T, k + 1))
        else:
            q = ("%s scored <b>%s</b> points in %d basketball games. How many points does %s need in the next game "
                 "to average %d points per game?" % (name, lst(v), k, pro, T))
        e = ("To have a mean of %d over %d %s, the total must be %d × %d = %s. So far: %s = %s. "
             "%s needs %s − %s = <b>%s</b>." % (T, k + 1, many, k + 1, T, fmt((k + 1) * T), plus(v), fmt(sum(v)),
                                                name, fmt((k + 1) * T), fmt(sum(v)), fmt(ans)))
        its.append(mcq_n(q, ans, [2 * T - cur, T, k * T - sum(v) if k * T > sum(v) else None, (k + 1) * T] + fills(ans),
                         e, rnd))

    # --- temperatures (3)
    CITY = [("Denver", 48, 66), ("Phoenix", 82, 99), ("Seattle", 52, 68)]
    for (city, lo, hi), ask in zip(CITY, ["mean", "median", "range"]):
        for _ in range(5000):
            v = [rnd.randint(lo, hi) for _ in range(7)]
            if ask == "mean" and (mean(v).denominator != 1 or mean(v) == median(v)):
                continue
            s = sorted(v)
            if ask == "median" and (v[3] == s[3] or s[2] == s[3] or s[4] == s[3]):
                continue
            if ask == "range" and (abs(v[-1] - v[0]) == max(v) - min(v) or max(v) - min(v) < 5):
                continue
            break
        days = "Monday to Sunday"
        q = "The high temperatures, in °F, in %s from %s were <b>%s</b>. " % (city, days, lst(v))
        if ask == "mean":
            q += "What was the mean high temperature?"
            its.append(mcq_n(q, mean(v), [sum(v), F(sum(v), 6), median(v), F(max(v) + min(v), 2)] + fills(mean(v)),
                             e_mean(v) + " The mean high temperature was %s°F." % fmt(mean(v)), rnd))
        elif ask == "median":
            q += "What was the median high temperature?"
            its.append(mcq_n(q, median(v), [v[3], s[2], s[4], mean(v)] + fills(median(v)), e_median(v), rnd))
        else:
            q += "What was the range of the temperatures?"
            its.append(mcq_n(q, max(v) - min(v), [max(v), abs(v[-1] - v[0]), s[-1] - s[1], s[-2] - s[0]]
                             + fills(max(v) - min(v)), e_range(v), rnd))

    # --- plant heights (3)
    for ask in ["mean", "diff", "median"]:
        t = TEACHERS[rnd.randrange(len(TEACHERS))]
        n = 8 if ask != "mean" else rnd.choice([6, 8])
        for _ in range(5000):
            v = [rnd.randint(9, 24) for _ in range(n)]
            m, md = mean(v), median(v)
            if ask == "mean" and (m.denominator != 1 or m == md):
                continue
            if ask == "diff" and not (m.denominator == 1 and md.denominator in (1, 2) and m != md and m - md != 1):
                continue
            if ask == "median" and (md.denominator != 2):
                continue
            break
        q = ("%s's class grew %d bean plants. After 3 weeks, the heights in centimeters were <b>%s</b>. "
             % (t, n, lst(v)))
        if ask == "mean":
            q += "What was the mean height?"
            its.append(mcq_n(q, m, [sum(v), F(sum(v), n - 1), md, F(max(v) + min(v), 2)] + fills(m),
                             e_mean(v) + " The mean height was %s cm." % fmt(m), rnd))
        elif ask == "median":
            q += "What was the median height?"
            s = sorted(v)
            its.append(mcq_n(q, md, [s[3], s[4], F(v[3] + v[4], 2), m] + fills(md, F(1, 2)), e_median(v), rnd))
        else:
            q += "What is the difference between the mean and the median?"
            d = abs(m - md)
            e = ("Mean: %s = %s, and %s ÷ %d = %s. Median: %s Difference: %s − %s = <b>%s</b>." % (
                plus(v), fmt(sum(v)), fmt(sum(v)), n, fmt(m), e_median(v, bold=False),
                fmt(max(m, md)), fmt(min(m, md)), fmt(d)))
            its.append(mcq_n(q, d, [m, md, m + md, max(v) - min(v)] + fills(d, F(1, 2)), e, rnd))

    # --- points per game (3)
    name, pro, pos = P.next()
    n, m = 6, rnd.randint(14, 22)
    q = ("%s averaged %d points per game in %d games. How many points did %s score in all?" % (name, m, n, pro))
    its.append(mcq_n(q, n * m, [m + n, (n - 1) * m, (n + 1) * m] + fills(n * m, 6),
                     "Total = mean × number of games = %d × %d = <b>%d</b> points." % (m, n, n * m), rnd))
    name, pro, pos = P.next()
    for _ in range(5000):
        n, m = rnd.choice([4, 5]), rnd.randint(12, 20)
        x = rnd.randint(m + 5, m + 14)
        m1 = F(n * m + x, n + 1)
        if m1.denominator in (1, 2) and F(m + x, 2) != m1:
            break
    q = ("%s averaged %d points per game in %d games. Then %s scored %d points in the next game. "
         "What is %s new average for all %d games?" % (name, m, n, pro, x, pos, n + 1))
    e = ("Points before: %d × %d = %d. New total: %d + %d = %d. New average = %d ÷ %d = <b>%s</b> points."
         % (m, n, n * m, n * m, x, n * m + x, n * m + x, n + 1, fmt(m1)))
    its.append(mcq_n(q, m1, [F(m + x, 2), F(n * m + x, n), m + 1, x] + fills(m1), e, rnd))
    name, pro, pos = P.next()
    for _ in range(5000):
        v = [rnd.randint(38, 60) for _ in range(8)]
        if mean(v).denominator == 2 and mean(v) != median(v):
            break
    q = "A basketball team scored <b>%s</b> points in its first 8 games. What was the mean number of points per game?" % lst(v)
    its.append(mcq_n(q, mean(v), [sum(v), F(sum(v), 7), median(v), F(max(v) + min(v), 2)] + fills(mean(v)),
                     e_mean(v), rnd))

    # --- compare two players (2)
    for sport, lo, hi, unit in [("quiz", 6, 10, "points"), ("long jump", 8, 14, "feet")]:
        a, ap, _ = P.next()
        b, bp, _ = P.next()
        for _ in range(5000):
            va = [rnd.randint(lo, hi) for _ in range(5)]
            vb = [rnd.randint(lo, hi) for _ in range(5)]
            ma, mb = mean(va), mean(vb)
            if (ma.denominator == 1 and mb.denominator == 1 and ma - mb >= 1 and sum(va) - sum(vb) != ma - mb
                    and median(va) - median(vb) != ma - mb):
                break
        if sport == "quiz":
            q = ("On 5 quizzes, %s scored <b>%s</b> and %s scored <b>%s</b>. How many points greater is %s's mean score "
                 "than %s's?" % (a, lst(va), b, lst(vb), a, b))
        else:
            q = ("In 5 long jumps, %s jumped <b>%s</b> feet and %s jumped <b>%s</b> feet. How many feet greater is %s's "
                 "mean jump than %s's?" % (a, lst(va), b, lst(vb), a, b))
        d = ma - mb
        e = ("%s: %s = %d, and %d ÷ 5 = %s. %s: %s = %d, and %d ÷ 5 = %s. Difference: %s − %s = <b>%s</b>." % (
            a, plus(va), sum(va), sum(va), fmt(ma), b, plus(vb), sum(vb), sum(vb), fmt(mb), fmt(ma), fmt(mb), fmt(d)))
        its.append(mcq_n(q, d, [sum(va) - sum(vb), median(va) - median(vb), ma, mb] + fills(d), e, rnd))

    # --- combined groups (2)
    GROUPS = [("In a class, %d girls read a mean of %d books over the summer and %d boys read a mean of %d books. "
               "What is the mean number of books for all %d students?", "books", (3, 12)),
              ("On the red team, %d players scored a mean of %d points. On the blue team, %d players scored a mean of "
               "%d points. What is the mean score of all %d players?", "points", (4, 20))]
    for t, unit, (lo, hi) in GROUPS:
        for _ in range(5000):
            n1, n2 = rnd.randint(3, 8), rnd.randint(3, 8)
            m1, m2 = rnd.randint(lo, hi), rnd.randint(lo, hi)
            M = F(n1 * m1 + n2 * m2, n1 + n2)
            if n1 != n2 and abs(m1 - m2) >= 3 and M.denominator in (1, 2) and F(m1 + m2, 2) != M:
                break
        q = t % (n1, m1, n2, m2, n1 + n2)
        e = ("Find each total first: %d × %d = %d and %d × %d = %d. All together: %d + %d = %d %s for %d students. "
             % (n1, m1, n1 * m1, n2, m2, n2 * m2, n1 * m1, n2 * m2, n1 * m1 + n2 * m2, unit, n1 + n2))
        if unit == "points":
            e = e.replace("students", "players")
        e += "Mean = %d ÷ %d = <b>%s</b>. (Averaging %d and %d does not work, because the groups are different sizes.)" % (
            n1 * m1 + n2 * m2, n1 + n2, fmt(M), m1, m2)
        its.append(mcq_n(q, M, [F(m1 + m2, 2), n1 * m1 + n2 * m2, m1 + m2] + fills(M), e, rnd))

    # --- misc (3)
    name, pro, pos = P.next()
    for _ in range(5000):
        v = [rnd.randint(5, 20) for _ in range(6)]
        if mean(v).denominator == 1 and mean(v) != median(v):
            break
    q = "%s saved <b>%s</b> dollars in 6 weeks. What is the mean amount %s saved per week, in dollars?" % (name, lst(v), pro)
    its.append(mcq_n(q, mean(v), [sum(v), F(sum(v), 5), median(v), F(max(v) + min(v), 2)] + fills(mean(v)),
                     e_mean(v), rnd))
    name, pro, pos = P.next()
    for _ in range(5000):
        v = [5 * rnd.randint(3, 12) for _ in range(10)]
        s = sorted(v)
        if s[4] != s[5] and F(v[4] + v[5], 2) != median(v) and len(set(v)) >= 8:
            break
    q = ("%s read for <b>%s</b> minutes on 10 days. What is the median number of minutes %s read?" % (name, lst(v), pro))
    its.append(mcq_n(q, median(v), [s[4], s[5], F(v[4] + v[5], 2), s[4] + s[5]] + fills(median(v), 5), e_median(v), rnd))
    for _ in range(5000):
        v = [rnd.randint(24, 60) for _ in range(6)]
        r = max(v) - min(v)
        if v[0] not in (max(v), min(v)) and v[-1] not in (max(v), min(v)) and abs(v[-1] - v[0]) != r:
            break
    q = ("A bakery sold <b>%s</b> muffins on 6 days. What is the range of the number of muffins sold?" % lst(v))
    s = sorted(v)
    its.append(mcq_n(q, r, [max(v), abs(v[-1] - v[0]), s[-1] - s[1], max(v) + min(v)] + fills(r), e_range(v), rnd))

    assert len(its) == 20, len(its)
    rnd.shuffle(its)
    return {"title": "Word problems", "items": its}


# ============================================================ lesson
LV = [8, 5, 9, 6, 9, 3, 9]              # quiz scores: mean 7, median 8, mode 9, range 6, IQR 4
EV = [12, 7, 10, 15, 9, 14]             # even count: median 11
DOT_LO, DOT_C = 0, [1, 3, 2, 2, 1, 0, 0, 0, 1]   # books read by 10 students: mean 2.5, median 2, mode 1, range 8


def body_html():
    s = sorted(LV)
    assert mean(LV) == 7 and median(LV) == 8 and max(LV) - min(LV) == 6 and quart(LV) == (5, 9)
    assert median(EV) == 11
    dv = [DOT_LO + i for i in range(len(DOT_C)) for _ in range(DOT_C[i])]
    assert len(dv) == 10 and mean(dv) == F(5, 2) and median(dv) == 2 and max(dv) - min(dv) == 8
    plot = plot_svg(DOT_LO, DOT_C, "Books read last month", "books read by 10 students")
    plot = plot.replace("<svg ", "<svg data-pf='lg' ", 1)
    return (
        "<h2>Center and variation</h2>"
        "<p>A <b>measure of center</b> sums up a whole data set with one number: the <b>mean</b> or the <b>median</b>. "
        "The <b>mode</b> also tells which value is most typical. "
        "A <b>measure of variation</b> tells, with one number, how spread out the values are: the <b>range</b> or the "
        "<b>interquartile range (IQR)</b>.</p>"
        "<p>Seven quiz scores: <b>" + lst(LV) + "</b>. Sorted: " + lst(s) + ".</p>" +
        table(["Measure", "How to find it", "Example"], [
            ["Mean", "Add all the values. Divide by how many values there are.", "49 ÷ 7 = <b>7</b>"],
            ["Median", "Sort the values. Take the middle one.", "3, 5, 6, <b>8</b>, 9, 9, 9 → <b>8</b>"],
            ["Mode", "The value that appears most often", "9 appears 3 times → <b>9</b>"],
            ["Range", "Greatest − least", "9 − 3 = <b>6</b>"],
        ]) +
        "<h2>Median of an even number of values</h2>"
        "<p>With an even count there are two middle values. The median is their mean, so it can end in .5.</p>" +
        ex("Example", "Find the median of " + lst(EV) + ".",
           "Sort: " + lst(sorted(EV)) + ". There are 6 values, so the middle values are the 3rd and 4th: 10 and 12. "
           "(10 + 12) ÷ 2 = 11.", "11") +
        "<h2>Read a dot plot</h2>"
        "<p>Each X is one value. Ten students told how many books they read last month.</p>"
        "<figure class='sn-fig'>" + plot +
        "<figcaption>10 X's. Mean 2.5, median 2, mode 1, range 8.</figcaption></figure>"
        "<p><b>Mean:</b> 0 × 1 + 1 × 3 + 2 × 2 + 3 × 2 + 4 × 1 + 8 × 1 = 25, and 25 ÷ 10 = 2.5. "
        "<b>Median:</b> the 5th and 6th X's from the left are both at 2, so the median is 2. "
        "<b>Mode:</b> the tallest stack is at 1. <b>Range:</b> 8 − 0 = 8.</p>"
        "<h2>Outliers: mean or median?</h2>"
        "<p>An <b>outlier</b> is a value far from the others, like the 8 above. It pulls the mean toward it, "
        "but it barely moves the median. Here the mean (2.5) is greater than the median (2). "
        "When a data set has an outlier, the median usually describes a typical value better.</p>"
        "<h2>Interquartile range (IQR)</h2>"
        "<p>Sort the data and find the median. <b>Q1</b> is the median of the lower half and <b>Q3</b> is the median "
        "of the upper half. When the count is odd, leave the middle value out of both halves. IQR = Q3 − Q1.</p>" +
        ex("Example", "Find the IQR of the quiz scores " + lst(s) + ".",
           "The median is 8. Lower half: 3, 5, 6, so Q1 = 5. Upper half: 9, 9, 9, so Q3 = 9. IQR = 9 − 5 = 4.", "4") +
        "<h2>Find a missing value</h2>" +
        ex("Example", "Ava’s first 4 test scores are 82, 88, 79 and 87. What score does she need on the 5th test to have a "
           "mean of 85?",
           "For a mean of 85 on 5 tests, the total must be 5 × 85 = 425. So far: 82 + 88 + 79 + 87 = 336. "
           "425 − 336 = 89.", "89") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Taking the middle of the list without sorting", "Sort from least to greatest first"],
            ["Picking one middle value when the count is even", "Use the mean of the two middle values"],
            ["Dividing by the wrong count for the mean", "Divide by how many values there are (count the X's on a dot plot)"],
            ["Giving the greatest value as the range", "Range = greatest − least"],
            ["Giving the count as the mode (“3 times”)", "The mode is the value that repeats, not how many times"],
            ["Mixing up mean and median", "Mean: add and divide. Median: sort and take the middle"],
            ["Averaging two group means of different sizes", "Find each total, add them, then divide by everyone"],
        ])
    )


FAQ = [
    {"q": "How do you find the mean, median, mode and range?",
     "a": "Mean: add the values and divide by how many there are. Median: sort the values and take the middle one. Mode: the value that appears most often. Range: greatest value minus least value."},
    {"q": "How do you find the median when there is an even number of values?",
     "a": "Sort the values and find the two middle ones, then take their mean. For 7, 9, 10, 12, 14, 15 the middle values are 10 and 12, so the median is 11."},
    {"q": "What is the difference between a measure of center and a measure of variation?",
     "a": "A measure of center (mean or median) gives one typical value for the data. A measure of variation (range or interquartile range) gives one number for how spread out the values are."},
    {"q": "When is the median better than the mean?",
     "a": "When the data has an outlier or is very lopsided. One very large or very small value pulls the mean toward it, but the median stays near the middle of the data."},
]


CC_LIST = None


def gen_unit():
    global CC_LIST
    rnd = random.Random(616)
    P = People(rnd)
    CC_LIST = Ctx(rnd, LIST_CTX)
    sets = [set_mmr(rnd, P, Ctx(rnd, LIST_CTX)), set_mean(rnd, P, Ctx(rnd, LIST_CTX)), set_dot(rnd, P, Ctx(rnd, DOT_CTX)),
            set_outlier(rnd, P, Ctx(rnd, OUT_CTX)), set_word(rnd, P)]
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"] not in seen, it["q"]
            seen.add(it["q"])
    balance(sets, rnd)
    for s in sets:
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5)
    return {
        "country": "us", "subject": "math", "grade": "grade-6", "slug": "mean-median-mode-range", "sort": 16,
        "updated": UPDATED, "pdf_url": "",
        "title": "Mean, Median, Mode and Range",
        "seo_title": "Grade 6 Mean, Median, Mode and Range Worksheets: Dot Plots, Outliers and IQR with Answer Key",
        "short_title": "Mean, Median, Mode and Range",
        "domain": "Statistics and Probability",
        "standard_code": "6.SP.A.3",
        "standard_url": "https://www.thecorestandards.org/Math/Content/6/SP/A/3/",
        "standard_text": "Recognize that a measure of center for a numerical data set summarizes all of its values with a single number, while a measure of variation describes how its values vary with a single number.",
        "meta_desc": "Free Grade 6 mean, median, mode and range worksheets: find the median of even and odd data sets, compute the mean, read dot plots, see how outliers change the mean, find the IQR and a missing score. 100 practice questions with answers.",
        "key_big": "Mean = sum ÷ count. Median = middle value after sorting. Range = greatest − least.",
        "key_sub": "The mode is the value that appears most often. With an even count, the median is the mean of the two middle values. An outlier pulls the mean, but not the median.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen_unit()
    mark_large(u, "dot plot")
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(u, f, ensure_ascii=False, indent=1)
    print("wrote", path)
