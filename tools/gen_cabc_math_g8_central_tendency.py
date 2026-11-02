# -*- coding: utf-8 -*-
"""
BC Grade 8 Math: Central tendency (BC Mathematics Curriculum, Data and probability)
  python3 tools/gen_cabc_math_g8_central_tendency.py
Mean, median (odd and even counts), mode, range, and choosing the best measure when a data set has an outlier.
Helpers adapted from gen_us_math_g6_mean_median.py; all wording and contexts rewritten for British Columbia.
Every answer is computed with fractions.Fraction. Data include integers (with the real minus sign −) and decimals.
Wrong answers come from real mistakes: the median taken from the unsorted list, one middle value used for an even
count, dividing by the wrong count, the sum given as the mean, the count given as the mode, signs ignored with
negative numbers, the range taken as the greatest value or as last − first, and averaging the old mean with a new value.
BC number style: 4536, 41 000 (no-break space), real minus sign. HTML attributes use single quotes.
"""
import json, os, random, re
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-8")
UPDATED = "2026-11-02"
GREEN = "#006633"
INK = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"
MINUS = "−"
NBSP = " "
GIRLS = ["Olivia", "Ava", "Chloe", "Simran", "Jasleen", "Mei", "Ji-woo", "Hana", "Sofia", "Emma", "Leah", "Zara", "Nadia"]
BOYS = ["Liam", "Ethan", "Noah", "Arjun", "Harjot", "Wei", "Mateo", "Lucas", "Kai", "Owen", "Ryan"]
ORD = {1: "1st", 2: "2nd", 3: "3rd"}


# ------------------------------------------------------------ numbers
def clean(x):
    """True if x can be written with at most 2 decimal places."""
    return 100 % F(x).denominator == 0


def fmt(x):
    """BC style: 4536, 41 000 (no-break space), 12.5, −7."""
    x = F(x)
    neg = x < 0
    x = abs(x)
    assert clean(x), x
    w, r = divmod(x.numerator, x.denominator)
    s = str(w) if w < 10000 else "{:,}".format(w).replace(",", NBSP)
    if r:
        s += ("%.2f" % float(F(r, x.denominator)))[1:].rstrip("0")
    return (MINUS if neg else "") + s


def money(x):
    return "$" + fmt(x)


def ordn(k):
    return ORD.get(k, "%dth" % k)


def lst(v):
    return ", ".join(fmt(x) for x in v)


def term(x, first=False):
    return fmt(x) if (first or x >= 0) else "(%s)" % fmt(x)


def plus(v):
    return " + ".join(term(x, i == 0) for i, x in enumerate(v))


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


def modes(v):
    f = freq(v)
    top = max(f.values())
    if top == 1:
        return []
    return sorted(k for k in f if f[k] == top)


def rng(v):
    return max(v) - min(v)


# ------------------------------------------------------------ explanations
def e_sort(v):
    return "Put the values in order first: %s." % lst(sorted(v))


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
    return t + "The median is their mean: (%s + %s) ÷ 2 = %s." % (term(a, True), term(c), b(fmt(median(v))))


def e_mean(v, bold=True):
    m = mean(v)
    t = "<b>%s</b>" % fmt(m) if bold else fmt(m)
    return "Add the values: %s = %s. There are %d values, so divide by %d: %s ÷ %d = %s." % (
        plus(v), fmt(sum(v)), len(v), len(v), fmt(sum(v)), len(v), t)


def e_range(v):
    hi, lo = max(v), min(v)
    if lo < 0:
        return "Range = greatest − least = %s − (%s) = %s + %s = <b>%s</b>." % (
            fmt(hi), fmt(lo), fmt(hi), fmt(-lo), fmt(hi - lo))
    return "Range = greatest − least = %s − %s = <b>%s</b>." % (fmt(hi), fmt(lo), fmt(hi - lo))


# ------------------------------------------------------------ choices
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


def mcq_n(q, ans, cands, e, rnd, show=fmt, neg=False, zero=False):
    """ans and cands are numbers. Wrong choices are clean, different in value, and (unless allowed) positive."""
    ans = F(ans)
    vals, cc = {ans}, []
    for c in cands:
        if c is None:
            continue
        c = F(c)
        if c in vals or not clean(c):
            continue
        if (c < 0 and not neg) or (c == 0 and not zero):
            continue
        vals.add(c)
        cc.append(show(c))
    return mcq(q, show(ans), cc, e, rnd)


def fills(ans, step=1):
    a = F(ans)
    return [a + step, a - step, a + 2 * step, a - 2 * step, a + 3 * step]


def balance(sets, rnd):
    """Move the correct choice so each position (A to D) is the answer 5 times in every set."""
    for st in sets:
        pos = [0, 1, 2, 3] * 5
        rnd.shuffle(pos)
        for it, t in zip(st["items"], pos):
            ch = it["c"]
            ch[it["a"]], ch[t] = ch[t], ch[it["a"]]
            it["a"] = t


class People:
    def __init__(self, rnd):
        self.pool = [(n, "she", "her") for n in GIRLS] + [(n, "he", "his") for n in BOYS]
        rnd.shuffle(self.pool)
        self.i = 0

    def next(self):
        p = self.pool[self.i % len(self.pool)]
        self.i += 1
        return p


class Ctx:
    def __init__(self, rnd, pool):
        self.pool = list(pool)
        rnd.shuffle(self.pool)
        self.i = 0

    def next(self):
        c = self.pool[self.i % len(self.pool)]
        self.i += 1
        return c


def find(rnd, make, ok, tries=20000):
    for _ in range(tries):
        x = make()
        if ok(x):
            return x
    raise RuntimeError("no data found")


# ------------------------------------------------------------ figures
def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


FS = 19


def plot_svg(lo, counts, title, what):
    """Dot plot (line plot with X marks), drawn exactly from the counts."""
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
    s.append("<text x='%d' y='%d' font-size='15' fill='%s' text-anchor='middle'>%s</text>" % (W / 2, Y + 54, INK, title))
    lab = "dot plot of %s from %d to %d" % (what, lo, lo + n - 1)
    return svg_wrap(W, H, "".join(s), lab)


def mark_large(u, pattern):
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


DOT_CTX = [
    dict(t="Students in a Grade 8 class in Kamloops counted the books they read over the summer.", title="Books read in the summer", what="books read", lo=0, hi=8, x="student"),
    dict(t="The dot plot shows the goals {name}’s hockey team scored in each game this season.", title="Goals per game", what="goals per game", lo=0, hi=6, x="game", mx=3),
    dict(t="A Grade 8 class in Surrey wrote a 10-point quiz. The dot plot shows the scores.", title="Quiz score (points)", what="quiz scores", lo=3, hi=10, x="student"),
    dict(t="Students in a class in Nanaimo counted the pets they have at home.", title="Number of pets", what="number of pets", lo=0, hi=5, x="student", mx=2),
    dict(t="Students in a class in Burnaby recorded how many hours they slept last night.", title="Hours of sleep", what="hours of sleep", lo=6, hi=11, x="student"),
    dict(t="Students in a Vancouver class counted how many SkyTrain trips they took last week.", title="SkyTrain trips last week", what="SkyTrain trips", lo=0, hi=8, x="student"),
    dict(t="The dot plot shows how many hours each member of a Victoria school band practised last week.", title="Hours of practice", what="hours of practice", lo=1, hi=8, x="band member"),
    dict(t="Students in a class in Prince George counted the letters in their first names.", title="Letters in first name", what="letters in first names", lo=3, hi=9, x="student"),
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


def dot_q(c, cn, P, ask):
    name = P.next()[0]
    return fig(plot_svg(c["lo"], cn, c["title"], c["what"])) + c["t"].format(name=name) + " " + ask


# ------------------------------------------------------------ list contexts (BC)
LIST_CTX = [
    dict(t="{name}’s hockey team scored these numbers of goals in {n} games:", lo=0, hi=8),
    dict(t="{name} scored these points in {n} basketball games:", lo=6, hi=28),
    dict(t="The daily rainfall in Vancouver, in millimetres, for {n} days in November was", lo=2, hi=24),
    dict(t="In a survey, {n} students timed their SkyTrain ride to school. The times, in minutes, are", lo=12, hi=45),
    dict(t="The heights, in centimetres, of {n} cedar seedlings in a school garden are", lo=18, hi=42),
    dict(t="{name} cycled every week for {n} weeks. The distances, in kilometres, are", lo=12, hi=40),
    dict(t="{name}’s scores on {n} math quizzes (out of 50) are", lo=28, hi=50),
    dict(t="{name} swam at the community pool on {n} days. The numbers of lengths {pro} swam are", lo=10, hi=40),
    dict(t="The lengths, in kilometres, of {n} hiking trails on Vancouver Island are", lo=3, hi=16),
    dict(t="The new snowfall at Whistler, in centimetres, on {n} days in January was", lo=2, hi=35),
    dict(t="Volunteers counted bald eagles near Squamish on {n} mornings. The counts are", lo=20, hi=90),
    dict(t="{name} read every day for {n} days. The numbers of pages {pro} read are", lo=12, hi=48),
    dict(t="The ages of {n} people on a whale-watching tour from Victoria are", lo=9, hi=68),
    dict(t="The numbers of students on {n} school buses in Kelowna are", lo=24, hi=52),
]

NEG_CTX = [
    dict(t="The low temperatures, in °C, in Prince George on {n} days in January were", lo=-24, hi=2),
    dict(t="The temperatures, in °C, at the top of Whistler Mountain at 8 a.m. on {n} days were", lo=-15, hi=4),
    dict(t="The low temperatures, in °C, in Kamloops on {n} nights in December were", lo=-16, hi=3),
    dict(t="The noon temperatures, in °C, in Fort St. John on {n} days in February were", lo=-25, hi=3),
]

DEC_CTX = [
    dict(t="{name}’s times, in seconds, in {n} races of 100 m are", lo=128, hi=165, k=10),
    dict(t="The masses, in kilograms, of {n} coho salmon caught on a fishing trip on the Fraser River are", lo=22, hi=58, k=10),
    dict(t="The rainfall in Victoria, in centimetres, for {n} months was", lo=12, hi=98, k=10),
    dict(t="The lengths, in metres, of {n} long jumps by {name} at a track meet in Kamloops are", lo=32, hi=52, k=10),
]


def say(c, n, P):
    name, pro, pos = P.next()
    return c["t"].format(n=n, name=name, pro=pro, pos=pos)


def dq(c, v, P, ask):
    return "%s <b>%s</b>. %s" % (say(c, len(v), P), lst(v), ask)


def rand_vals(rnd, c, n):
    if "k" in c:
        out = []
        while len(out) < n:
            x = rnd.randint(c["lo"], c["hi"])
            if x % c["k"]:  # no whole numbers in a list of decimals (no “15” among 15.5, 16.3, …)
                out.append(F(x, c["k"]))
        return out
    return [rnd.randint(c["lo"], c["hi"]) for _ in range(n)]


# ============================================================ set 1: mean
def set_mean(rnd, P):
    CC = Ctx(rnd, LIST_CTX)
    CN = Ctx(rnd, NEG_CTX)
    CD = Ctx(rnd, DEC_CTX)
    order = ["whole", "whole", "whole", "total", "whole", "dec_ans", "whole", "whole", "dec_data", "neg",
             "total", "dec_ans", "neg", "dec_data", "missing", "neg", "missing", "add", "missing", "add"]
    its = []
    tot = [("{name} read for {n} days. {Pro} read a mean of {m} pages per day. How many pages did {pro} read in all?", "pages", 18, 40, (6, 7, 8)),
           ("A lacrosse team scored a mean of {m} goals per game in {n} games. How many goals did the team score in all?", "goals", 8, 14, (8, 10, 12))]
    ti = 0
    for kind in order:
        if kind == "total":
            t, unit, lo, hi, ns = tot[ti]
            ti += 1
            n, m = rnd.choice(ns), rnd.randint(lo, hi)
            name, pro, pos = P.next()
            q = t.format(n=n, m=m, name=name, pro=pro, Pro=pro.capitalize())
            ans = n * m
            e = "Mean = sum ÷ count, so sum = mean × count = %d × %d = <b>%s</b> %s." % (m, n, fmt(ans), unit)
            its.append(mcq_n(q, ans, [m + n, F(m, n) if m % n == 0 else None, (n - 1) * m, (n + 1) * m] + fills(ans, 10), e, rnd))
        elif kind == "missing":
            for _ in range(5000):
                n = rnd.choice([5, 6])
                m = rnd.randint(14, 30)
                known = [rnd.randint(m - 8, m + 8) for _ in range(n - 1)]
                ans = n * m - sum(known)
                if 3 <= ans <= m + 15 and ans not in known and abs(ans - m) >= 2 and (n - 1) * m - sum(known) > 0:
                    break
            q = "The mean of %d numbers is %d. %s of them are <b>%s</b>. What is the missing number?" % (
                n, m, "Four" if n == 5 else "Five", lst(known))
            e = ("The sum of all %d numbers must be %d × %d = %d. The known numbers add to %s = %d. "
                 "Missing number = %d − %d = <b>%d</b>." % (n, n, m, n * m, plus(known), sum(known), n * m, sum(known), ans))
            its.append(mcq_n(q, ans, [(n - 1) * m - sum(known), m, n * m, F(sum(known), n - 1)] + fills(ans), e, rnd))
        elif kind == "add":
            c = CC.next()
            for _ in range(5000):
                n = rnd.choice([4, 5])
                v = rand_vals(rnd, c, n)
                x = rnd.randint(c["lo"], c["hi"])
                m0, m1 = mean(v), mean(v + [x])
                if (m0.denominator == 1 and m1.denominator in (1, 2) and abs(x - m0) >= 4
                        and F(m0 + x, 2) != m1 and median(v + [x]) != m1):
                    break
            S = sum(v)
            q = dq(c, v, P, "The mean is %s. Then the value %s is added to the data. What is the new mean?" % (fmt(m0), fmt(x)))
            e = ("The new sum is %s + %s = %s, and now there are %d values. New mean = %s ÷ %d = <b>%s</b>. "
                 "(Do not just average the old mean and the new value.)" % (fmt(S), fmt(x), fmt(S + x), n + 1,
                                                                          fmt(S + x), n + 1, fmt(m1)))
            its.append(mcq_n(q, m1, [F(m0 + x, 2), F(S + x, n), m0, median(v + [x])] + fills(m1), e, rnd))
        elif kind == "neg":
            c = CN.next()
            v = find(rnd, lambda: rand_vals(rnd, c, rnd.choice([5, 6, 7])),
                     lambda v: mean(v).denominator == 1 and mean(v) != 0 and min(v) < 0 < max(v)
                     and mean(v) != median(v) and F(sum(abs(x) for x in v), len(v)).denominator == 1
                     and F(sum(abs(x) for x in v), len(v)) != abs(mean(v)))
            m = mean(v)
            q = dq(c, v, P, "What is the mean temperature?")
            e = e_mean(v) + " Add the negative numbers as negatives: the signs matter."
            cands = [F(sum(abs(x) for x in v), len(v)), -m, F(sum(v), len(v) - 1), median(v), F(sum(abs(x) for x in v), len(v)) * (-1)]
            its.append(mcq_n(q, m, cands + fills(m), e, rnd, neg=True, zero=True))
        else:
            if kind.startswith("dec_data"):
                c = CD.next()
                n = rnd.choice([4, 5])
            else:
                c = CC.next()
                n = rnd.choice([5, 6, 7, 8]) if kind == "whole" else rnd.choice([4, 5, 8])

            def ok(v):
                m = mean(v)
                if kind == "whole" and m.denominator != 1:
                    return False
                if kind == "dec_ans" and (m.denominator == 1 or not clean(m)):
                    return False
                if kind == "dec_data" and not clean(m):
                    return False
                return median(v) != m
            v = find(rnd, lambda: rand_vals(rnd, c, n), ok)
            S = sum(v)
            m = mean(v)
            q = dq(c, v, P, "What is the mean?")
            cands = [S, F(S, n - 1), F(S, n + 1), median(v), F(max(v) + min(v), 2)]
            its.append(mcq_n(q, m, cands + fills(m, F(1, 10) if kind == "dec_data" else 1), e_mean(v), rnd))
    assert len(its) == 20
    return {"title": "Find the mean", "items": its}


# ============================================================ set 2: median
def set_median(rnd, P):
    CC = Ctx(rnd, LIST_CTX)
    its = []
    order = ["odd", "even", "odd", "even", "odd", "even", "same", "odd", "even", "concept1", "dot", "odd", "even",
             "neg", "dec", "dot", "neg", "dec", "dot", "concept2"]
    halves = [True, False, True, False, True]
    ie = 0
    CN = Ctx(rnd, NEG_CTX)
    CD = Ctx(rnd, DEC_CTX)
    DC = Ctx(rnd, DOT_CTX)
    for kind in order:
        if kind in ("odd", "neg", "dec"):
            c = CN.next() if kind == "neg" else CD.next() if kind == "dec" else CC.next()
            nn = [7, 5] if kind != "odd" else [5, 7, 9]

            def ok(v):
                s = sorted(v)
                n = len(v)
                m = n // 2
                good = v[m] != s[m] and s[m - 1] != s[m] and s[m + 1] != s[m] and len(set(v)) == n
                if kind == "neg":
                    ab = sorted(v, key=abs)
                    good = good and min(v) < 0 < max(v) and ab[m] != s[m] and sum(1 for x in v if x < 0) >= 3
                return good
            v = find(rnd, lambda: rand_vals(rnd, c, rnd.choice(nn)), ok)
            s = sorted(v)
            m = len(v) // 2
            ans = median(v)
            q = dq(c, v, P, "What is the median?")
            e = e_median(v) + " (The middle of the list as written, %s, is not the median.)" % fmt(v[m])
            cands = [v[m], s[m - 1], s[m + 1], mean(v)]
            if kind == "neg":
                e = e_median(v) + " Remember: %s is less than %s, because it is farther below 0." % (fmt(s[0]), fmt(s[1]))
                cands = [sorted(v, key=abs)[m], v[m], s[m - 1], s[m + 1]]
            step = F(1, 10) if kind == "dec" else 1
            its.append(mcq_n(q, ans, cands + fills(ans, step), e, rnd, neg=(kind == "neg"), zero=(kind == "neg")))
        elif kind in ("even", "same"):
            c = CC.next()
            if kind == "even":
                want_half = halves[ie]
                ie += 1

            def ok(v):
                n = len(v)
                s = sorted(v)
                a, b = s[n // 2 - 1], s[n // 2]
                um = F(v[n // 2 - 1] + v[n // 2], 2)
                if len(set(v)) < n - 1 or um == median(v):
                    return False
                if kind == "same":
                    return a == b and v.count(a) == 2
                return a != b and ((a + b) % 2 == 1) == want_half
            v = find(rnd, lambda: rand_vals(rnd, c, rnd.choice([6, 8, 10])), ok)
            n = len(v)
            s = sorted(v)
            a, b = s[n // 2 - 1], s[n // 2]
            ans = median(v)
            q = dq(c, v, P, "What is the median?")
            cands = [a, b, F(v[n // 2 - 1] + v[n // 2], 2), a + b, mean(v), s[n // 2 + 1]]
            its.append(mcq_n(q, ans, cands + fills(ans), e_median(v), rnd))
        elif kind == "dot":
            c = DC.next()
            lo = c["lo"]
            nm = c["hi"] - lo + 1
            N = rnd.choice([11, 12, 13, 14])
            mid_line = F(2 * lo + nm - 1, 2)
            cn, v = make_counts(rnd, c, N, lambda cn, v: median(v) != mid_line and median(v) != mean(v))
            ans = median(v)
            if N % 2:
                k = N // 2 + 1
                e = ("There are %d X’s, already in order from left to right. The median is the %s X from the left. "
                     "It is above %d, so the median is <b>%d</b>." % (N, ordn(k), v[k - 1], v[k - 1]))
            else:
                k = N // 2
                a, b = v[k - 1], v[k]
                if a == b:
                    e = ("There are %d X’s, already in order from left to right. The two middle X’s are the %s and %s "
                         "from the left. Both are above %d, so the median is <b>%d</b>." % (N, ordn(k), ordn(k + 1), a, a))
                else:
                    e = ("There are %d X’s, already in order from left to right. The two middle X’s are the %s and %s "
                         "from the left, above %d and %d. Median = (%d + %d) ÷ 2 = <b>%s</b>."
                         % (N, ordn(k), ordn(k + 1), a, b, a, b, fmt(ans)))
            top = max(range(nm), key=lambda i: (cn[i], -i))
            q = dot_q(c, cn, P, "What is the median?")
            cands = [mid_line, lo + top, mean(v), N // 2, ans + F(1, 2) if N % 2 == 0 else None, ans + 1, ans - 1]
            cands = [x for x in cands if x is not None]
            its.append(mcq_n(q, ans, cands + fills(ans), e, rnd))
        elif kind == "concept1":
            v = find(rnd, lambda: rnd.sample(range(2, 30), 5),
                     lambda v: v[2] == max(v) or v[2] == min(v))
            name, pro, pos = P.next()
            q = ("%s says the median of <b>%s</b> is %s, because %s is in the middle of the list. What mistake did %s make?"
                 % (name, lst(v), fmt(v[2]), fmt(v[2]), pro))
            e = (e_median(v) + " %s took the middle of the list without putting the values in order. "
                 "In fact, %s is the %s value." % (name, fmt(v[2]), "greatest" if v[2] == max(v) else "least"))
            its.append(mcq(q, "%s did not put the values in order first." % pro.capitalize(),
                           ["%s should have added the values and divided by 5." % pro.capitalize(),
                            "%s should have used the value that appears most often." % pro.capitalize(),
                            "%s should have found greatest − least." % pro.capitalize()], e, rnd))
        else:  # concept2
            q = "A data set has 12 values, in order from least to greatest. How do you find the median?"
            e = ("With an even count there is no single middle value. The 6th and 7th values are in the middle "
                 "(5 values before them and 5 after), so the median is their mean.")
            its.append(mcq(q, "Find the mean of the 6th and 7th values.",
                           ["Use the 6th value.", "Use the 7th value.", "Find the mean of the 1st and 12th values."], e, rnd))
    assert len(its) == 20
    return {"title": "Find the median: odd and even counts", "items": its}


# ============================================================ set 3: mode
def set_mode(rnd, P):
    CC = Ctx(rnd, LIST_CTX)
    CN = Ctx(rnd, NEG_CTX)
    DC = Ctx(rnd, DOT_CTX)
    order = ["one", "one", "none", "one", "two", "one", "dot", "cat", "none", "neg", "shoe", "two", "dot", "one",
             "always", "neg", "cat2", "shoe", "dot", "add"]
    its = []
    si, used = 0, set()
    for kind in order:
        if kind in ("one", "neg"):
            c = CN.next() if kind == "neg" else CC.next()

            def make():
                n = rnd.choice([7, 8, 9, 10])
                lo, hi = c["lo"], c["hi"]
                base = rnd.sample(range(lo, hi + 1), n - 3)
                md, sec = base[0], base[1]
                v = base + [md, md, sec]
                rnd.shuffle(v)
                return v, md, sec

            def ok(t):
                v, md, sec = t
                good = v.index(md) > 1 and md != 3 and median(v) != md and v[0] != md
                if kind == "neg":
                    good = good and md < 0 and -md in range(c["lo"], c["hi"] + 1) and -md not in v
                return good
            v, md, sec = find(rnd, make, ok)
            q = dq(c, v, P, "What is the mode?")
            e = ("Count how many times each value appears: %s appears 3 times, more than any other value. "
                 "The mode is the value <b>%s</b>, not the count 3." % (fmt(md), fmt(md)))
            cands = [3, sec, median(v), max(v), v[0]]
            if kind == "neg":
                cands = [-md, 3, sec, median(v), max(v)]
            its.append(mcq_n(q, md, cands + fills(md), e, rnd, neg=(kind == "neg"), zero=(kind == "neg")))
        elif kind == "two":
            c = CC.next()
            n = rnd.choice([8, 9, 10])
            base = rnd.sample(range(c["lo"], c["hi"] + 1), n - 2)
            a, b = sorted(base[:2])
            v = base + [a, b]
            rnd.shuffle(v)
            q = dq(c, v, P, "What is the mode?")
            cs = "%s and %s" % (fmt(a), fmt(b))
            e = ("%s and %s each appear 2 times. Every other value appears once. A data set can have two modes: "
                 "<b>%s</b>." % (fmt(a), fmt(b), cs))
            its.append(mcq(q, cs, [fmt(a), fmt(b), "no mode", "2"], e, rnd))
        elif kind == "none":
            c = CC.next()
            n = rnd.choice([6, 7])
            v = rnd.sample(range(c["lo"], c["hi"] + 1), n)
            q = dq(c, v, P, "What is the mode?")
            e = ("Each value appears only once, so no value is more common than the others. The data set has "
                 "<b>no mode</b>. (The mode is never a count like 1, and it is not 0.)")
            its.append(mcq(q, "no mode", ["1", "0", fmt(median(v)), fmt(v[0])], e, rnd))
        elif kind == "dot":
            c = DC.next()
            lo = c["lo"]
            nm = c["hi"] - lo + 1
            N = rnd.randint(10, 14)

            def ok(cn, v):
                t = [i for i in range(nm) if cn[i] == max(cn)]
                return (len(t) == 1 and lo + t[0] != max(cn) and lo + t[0] > 0 and lo + t[0] != median(v)
                        and lo + t[0] <= c.get("mx", 99))
            cn, v = make_counts(rnd, c, N, ok)
            i = cn.index(max(cn))
            ans = lo + i
            sec = sorted(range(nm), key=lambda k: (-cn[k], k))[1]
            q = dot_q(c, cn, P, "What is the mode?")
            e = ("The tallest stack of X’s is above %d, so the mode is <b>%d</b>. "
                 "(The stack has %d X’s, but the mode is the value, not the count.)" % (ans, ans, max(cn)))
            its.append(mcq_n(q, ans, [max(cn), lo + sec, median(v), N] + fills(ans), e, rnd))
        elif kind == "cat":
            sports = ["soccer", "hockey", "basketball", "lacrosse", "volleyball"]
            for _ in range(100):
                cnts = rnd.sample(range(3, 11), 4)
                if max(cnts) - sorted(cnts)[-2] >= 1:
                    break
            sp = rnd.sample(sports, 4)
            pairs = list(zip(sp, cnts))
            top = max(pairs, key=lambda p: p[1])
            sec = sorted(pairs, key=lambda p: -p[1])[1]
            q = ("Students in a Grade 8 class in Kelowna named their favourite sport: %s. What is the mode?"
                 % ", ".join("%s %d" % (s_, k) for s_, k in pairs))
            q = q.replace(", %s %d" % pairs[-1], " and %s %d" % pairs[-1])
            e = ("The mode is the answer chosen most often. %s was chosen %d times, more than any other sport, "
                 "so the mode is <b>%s</b>. The mode is the category, not the number %d." % (
                     top[0].capitalize(), top[1], top[0], top[1]))
            its.append(mcq(q, top[0], [str(top[1]), sec[0], "no mode"], e, rnd))
        elif kind == "cat2":
            q = ("A class in Victoria recorded each student’s favourite colour. Which measure can describe this data?")
            e = ("Colours are categories, not numbers. You cannot add them (no mean) or put them in number order "
                 "(no median). You can still find the colour chosen most often, so <b>the mode</b> works.")
            its.append(mcq(q, "the mode only", ["the mean only", "the median only", "the mean, median and mode"], e, rnd))
        elif kind == "shoe":
            for _ in range(5000):
                n = rnd.choice([9, 10, 11])
                pool = [F(x, 2) for x in range(12, 21)]  # 6 to 10 in half sizes
                v = [rnd.choice(pool) for _ in range(n)]
                f = freq(v)
                ms = modes(v)
                if (len(ms) == 1 and f[ms[0]] == 3 and median(v) != ms[0] and clean(mean(v)) and mean(v) != ms[0]
                        and v[0] != ms[0] and ms[0] not in used and (ms[0].denominator == 2) == (si == 0)):
                    break
            md = ms[0]
            used.add(md)
            q = (["A shoe store in Burnaby sold these sizes of running shoes on Saturday: <b>%s</b>. What is the mode?",
                  "A soccer team in Surrey ordered cleats in these sizes: <b>%s</b>. What is the mode?"][si] % lst(v))
            si += 1
            e = ("%s appears 3 times, more than any other size, so the mode is <b>%s</b>. "
                 "Half sizes count as their own values." % (fmt(md), fmt(md)))
            its.append(mcq_n(q, md, [3, median(v), md - F(1, 2), md + F(1, 2), v[0]], e, rnd))
        elif kind == "always":
            q = "Which measure is always one of the values in the data set (when it exists)?"
            e = ("The mode is a value that appears in the data most often, so it is always a data value. "
                 "The mean and the median of an even count are often not in the data: the median of 2, 4, 9, 10 is 6.5.")
            its.append(mcq(q, "the mode", ["the mean", "the median", "the range"], e, rnd))
        else:  # add
            for _ in range(5000):
                v = sorted(rnd.sample(range(3, 20), 4))
                d = rnd.choice(v[1:3])
                v = sorted(v + [d])
                others = [x for x in v if x != d]
                if len(others) == 3:
                    break
            ans = rnd.choice(others)
            gaps = [x for x in range(v[0] + 1, v[-1]) if x not in v]
            wrong = rnd.sample(gaps, 2)
            q = ("The data are <b>%s</b>. Which value could you add so that the data set has two modes?" % lst(v))
            e = ("Right now %s appears twice and is the only mode. Adding %s makes %s appear twice too, so %s and %s "
                 "are both modes. Adding %s gives %s three times (one mode). A new value like %s or %s appears only once."
                 % (fmt(d), fmt(ans), fmt(ans), fmt(min(d, ans)), fmt(max(d, ans)), fmt(d), fmt(d),
                    fmt(min(wrong)), fmt(max(wrong))))
            its.append(mcq(q, fmt(ans), [fmt(d), fmt(wrong[0]), fmt(wrong[1])], e, rnd))
    assert len(its) == 20
    return {"title": "Find the mode", "items": its}


# ============================================================ set 4: range
def set_range(rnd, P):
    CC = Ctx(rnd, LIST_CTX)
    CN = Ctx(rnd, NEG_CTX)
    CD = Ctx(rnd, DEC_CTX)
    DC = Ctx(rnd, DOT_CTX)
    order = ["list", "list", "true", "list", "dot", "list", "neg", "dec", "list", "dot", "maxmissing", "neg",
             "notchange", "dec", "minmissing", "dot", "neg", "compare", "newmax", "compare"]
    its = []
    ci = 0
    for kind in order:
        if kind in ("list", "neg", "dec"):
            c = CN.next() if kind == "neg" else CD.next() if kind == "dec" else CC.next()

            def ok(v):
                r = rng(v)
                good = (v[0] not in (max(v), min(v)) and v[-1] not in (max(v), min(v)) and abs(v[-1] - v[0]) != r
                        and r > 3 * (F(1, 10) if kind == "dec" else 1))
                if kind == "neg":
                    good = good and min(v) < 0 < max(v) and max(v) + min(v) != 0 and max(v) != -min(v)
                return good
            v = find(rnd, lambda: rand_vals(rnd, c, rnd.choice([6, 7, 8])), ok)
            r = rng(v)
            s = sorted(v)
            q = dq(c, v, P, "What is the range?")
            e = e_range(v) + " Use the greatest and least values, not the first and last in the list."
            if kind == "neg":
                e = e_range(v) + " Subtracting a negative number is the same as adding its opposite."
                cands = [abs(max(v) + min(v)), max(v), -min(v), s[-1] - s[1], s[-2] - s[0]]
            else:
                cands = [max(v), abs(v[-1] - v[0]), s[-1] - s[1], s[-2] - s[0], max(v) + min(v)]
            step = F(1, 10) if kind == "dec" else 1
            its.append(mcq_n(q, r, cands + fills(r, step), e, rnd))
        elif kind == "dot":
            c = DC.next()
            lo = c["lo"]
            nm = c["hi"] - lo + 1
            N = rnd.randint(9, 14)
            cn, v = make_counts(rnd, c, N, lambda cn, v: (cn[0] == 0 or cn[-1] == 0) and rng(v) >= 2)
            ans = rng(v)
            q = dot_q(c, cn, P, "What is the range?")
            e = ("The X farthest to the left is at %d and the X farthest to the right is at %d. "
                 "Range = %d − %d = <b>%d</b>. Use the X’s, not the ends of the number line."
                 % (min(v), max(v), max(v), min(v), ans))
            its.append(mcq_n(q, ans, [nm - 1, max(v), N, max(cn), ans + 1, ans - 1], e, rnd))
        elif kind == "maxmissing":
            lo_, r = rnd.randint(8, 20), rnd.randint(12, 25)
            name, pro, pos = P.next()
            q = ("The range of %s’s bowling scores in 5-pin bowling is %d. %s lowest score is %d. What is %s highest score?"
                 % (name, r * 5, pos.capitalize(), lo_ * 10, pos))
            r5, l10 = r * 5, lo_ * 10
            e = "Range = highest − lowest, so highest = lowest + range = %d + %d = <b>%d</b>." % (l10, r5, l10 + r5)
            its.append(mcq_n(q, l10 + r5, [abs(r5 - l10), r5, l10 + r5 * 2, F(l10 + r5, 2)] + fills(l10 + r5, 5), e, rnd))
        elif kind == "minmissing":
            hi_, r = rnd.randint(-2, 5), rnd.randint(10, 18)
            q = ("Over one week in Fort St. John, the highest temperature was %s°C and the range of the temperatures "
                 "was %d°C. What was the lowest temperature?" % (fmt(hi_), r))
            ans = hi_ - r
            e = ("Range = highest − lowest, so lowest = highest − range = %s − %d = <b>%s°C</b>." % (fmt(hi_), r, fmt(ans)))
            show = lambda x: fmt(x) + "°C"
            its.append(mcq_n(q, ans, [hi_ + r, r - hi_, -r, ans + 2, ans - 2], e, rnd, show=show, neg=True))
        elif kind == "newmax":
            c = CC.next()
            for _ in range(5000):
                v = rand_vals(rnd, c, 4)
                r_new = rnd.randint(rng(v) + 3, rng(v) + 12)
                x = min(v) + r_new
                if len(set(v)) == 4 and x <= c["hi"] + 10 and x != max(v) + r_new and rng(v) >= 4:
                    break
            q = dq(c, v, P, "One more value is added. It is greater than all the others, and the new range is %d. "
                            "What is the new value?" % r_new)
            e = ("The least value is still %s. New range = new value − least, so new value = %s + %d = <b>%s</b>."
                 % (fmt(min(v)), fmt(min(v)), r_new, fmt(x)))
            its.append(mcq_n(q, x, [max(v) + r_new, r_new, max(v) + r_new - rng(v) + 1, x + 1, x - 1], e, rnd))
        elif kind == "notchange":
            v = sorted(rnd.sample(range(5, 30), 4))
            inside = [x for x in range(v[0] + 1, v[-1]) if x not in v]
            ans = rnd.choice(inside)
            out = [v[0] - rnd.randint(1, 4), v[-1] + rnd.randint(1, 4), v[-1] + rnd.randint(6, 10)]
            q = "The data are <b>%s</b>. Which value could you add without changing the range?" % lst(v)
            e = ("The range is %d − %d = %d. A new value between %d and %d does not change the greatest or least "
                 "value, so <b>%d</b> keeps the range at %d. The other values are outside, so they make the range larger."
                 % (v[-1], v[0], v[-1] - v[0], v[0], v[-1], ans, v[-1] - v[0]))
            its.append(mcq(q, fmt(ans), [fmt(x) for x in out], e, rnd))
        elif kind == "true":
            q = "Which statement about the range of a data set is true?"
            e = ("The range is greatest − least. It tells how spread out the data are. It is not a measure of "
                 "central tendency, because it does not give a typical value.")
            its.append(mcq(q, "It shows how spread out the data are.",
                           ["It is the middle value.", "It is the most common value.", "It is the greatest value."], e, rnd))
        else:  # compare
            ci += 1
            a, _, _ = P.next()
            b, _, _ = P.next()
            lo, hi, what = [(20, 48, "minutes of homework on 6 school nights"), (5, 30, "kilometres cycled in 6 weeks")][ci - 1]
            for _ in range(5000):
                va = [rnd.randint(lo, hi) for _ in range(6)]
                vb = [rnd.randint(lo, hi) for _ in range(6)]
                if (rng(va) - rng(vb) >= 3 and max(vb) > max(va) and len(set(va)) == 6 and len(set(vb)) == 6
                        and abs(va[-1] - va[0]) != rng(va)):
                    break
            q = ("%s recorded %s: <b>%s</b>. %s recorded <b>%s</b>. How much greater is the range of %s’s data than "
                 "the range of %s’s data?" % (a, what, lst(va), b, lst(vb), a, b))
            d = rng(va) - rng(vb)
            e = ("%s: %d − %d = %d. %s: %d − %d = %d. Difference: %d − %d = <b>%d</b>." % (
                a, max(va), min(va), rng(va), b, max(vb), min(vb), rng(vb), rng(va), rng(vb), d))
            its.append(mcq_n(q, d, [max(va) - max(vb) if max(va) > max(vb) else max(vb) - max(va), rng(va), rng(vb),
                                    abs(min(va) - min(vb))] + fills(d), e, rnd))
    assert len(its) == 20
    return {"title": "Find the range", "items": its}


# ============================================================ set 5: word problems — outliers and the best measure
OUT_CTX = [
    dict(t="{name} recorded how many minutes {pro} spent on homework on {n} school nights:", lo=25, hi=45, out=(5, 10)),
    dict(t="The prices, in dollars, of {n} used snowboards for sale in Kelowna are", lo=120, hi=180, out=(420, 480)),
    dict(t="The numbers of visitors to a small museum in Nanaimo on {n} weekdays were", lo=40, hi=70, out=(150, 190)),
    dict(t="The ages of {n} people on a hike up Grouse Mountain are", lo=30, hi=45, out=(9, 12)),
    dict(t="{name} timed {pos} bus ride to school in Surrey on {n} days. The times, in minutes, were", lo=12, hi=18, out=(40, 46)),
    dict(t="The numbers of pages in {n} novels in a classroom library are", lo=180, hi=260, out=(620, 700)),
    dict(t="The lengths, in centimetres, of {n} salmon caught on a fishing trip are", lo=55, hi=70, out=(24, 30)),
    dict(t="The numbers of cars waiting for a BC Ferries sailing at Horseshoe Bay on {n} weekday mornings were", lo=90, hi=140, out=(310, 340)),
    dict(t="The masses, in kilograms, of {n} dogs at a dog park in Burnaby are", lo=18, hi=34, out=(3, 5)),
    dict(t="The high temperatures, in °C, in Kelowna on {n} days in July were", lo=28, hi=36, out=(12, 15)),
    dict(t="The heights, in centimetres, of {n} players on a Grade 8 volleyball team are", lo=156, hi=172, out=(192, 198)),
    dict(t="{name} rode {pos} bike every day for {n} days. The distances, in kilometres, were", lo=8, hi=15, out=(55, 62)),
]


def outlier_data(rnd, c, n, ok=lambda v, x: True):
    for _ in range(50000):
        base = [rnd.randint(c["lo"], c["hi"]) for _ in range(n - 1)]
        x = rnd.randint(*c["out"])
        v = base + [x]
        rnd.shuffle(v)
        if v.count(x) == 1 and ok(v, x):
            return v, x
    raise RuntimeError(c["t"])


def without(v, x):
    r = list(v)
    r.remove(x)
    return r


def set_word(rnd, P):
    CO = Ctx(rnd, OUT_CTX)
    order = ["which", "fair", "which", "remove", "typical", "shoe", "which", "meanchg", "remove", "need", "most",
             "typical", "medchg", "which", "remove", "need", "meanchg", "notchg", "wages", "lowest"]
    its = []
    ni = 0
    for kind in order:
        if kind == "which":
            c = CO.next()
            v, x = outlier_data(rnd, c, rnd.choice([7, 8]), lambda v, x: len(set(v)) >= 6)
            rest = without(v, x)
            q = dq(c, v, P, "Which value is an outlier?")
            e = ("Most values are between %s and %s. The value <b>%s</b> is far away from all the others, "
                 "so it is an outlier." % (fmt(min(rest)), fmt(max(rest)), fmt(x)))
            near = max(rest) if x > max(rest) else min(rest)
            far = min(rest) if x > max(rest) else max(rest)
            its.append(mcq_n(q, x, [near, far, median(v), sorted(rest)[len(rest) // 2]], e, rnd))
        elif kind == "remove":
            c = CO.next()
            v, x = outlier_data(rnd, c, rnd.choice([6, 7]),
                                lambda v, x: mean(without(v, x)).denominator == 1 and clean(mean(v)))
            rest = without(v, x)
            n, S = len(v), sum(v)
            ans = mean(rest)
            q = dq(c, v, P, "The outlier, %s, is removed. What is the mean of the other values?" % fmt(x))
            e = ("Without %s there are %d values. Their sum is %s = %s. Mean = %s ÷ %d = <b>%s</b>. "
                 "(With the outlier, the mean was %s ÷ %d = %s.)" % (
                     fmt(x), n - 1, plus(rest), fmt(sum(rest)), fmt(sum(rest)), n - 1, fmt(ans), fmt(S), n, fmt(mean(v))))
            its.append(mcq_n(q, ans, [F(S - x, n), mean(v), median(rest), F(S, n - 1)] + fills(ans), e, rnd))
        elif kind == "meanchg":
            c = CO.next()
            v, x = outlier_data(rnd, c, rnd.choice([6, 7]),
                                lambda v, x: mean(without(v, x)).denominator == 1 and mean(v).denominator == 1
                                and mean(v) != mean(without(v, x)))
            rest = without(v, x)
            m0, m1 = mean(v), mean(rest)
            d = abs(m0 - m1)
            word = "decrease" if m1 < m0 else "increase"
            q = dq(c, v, P, "The outlier, %s, is removed. By how much does the mean %s?" % (fmt(x), word))
            e = ("With the outlier: %s ÷ %d = %s. Without it: %s ÷ %d = %s. The mean %ss by %s − %s = <b>%s</b>." % (
                fmt(sum(v)), len(v), fmt(m0), fmt(sum(rest)), len(rest), fmt(m1), word, fmt(max(m0, m1)), fmt(min(m0, m1)), fmt(d)))
            its.append(mcq_n(q, d, [abs(median(v) - median(rest)), F(abs(x - m1), len(v)) if F(abs(x - m1), len(v)) != d else None,
                                    abs(x - m0), m1, F(x, len(v))] + fills(d), e, rnd))
        elif kind == "medchg":
            c = CO.next()
            v, x = outlier_data(rnd, c, 8, lambda v, x: median(v) != median(without(v, x)) and
                                abs(median(v) - median(without(v, x))) < 4)
            rest = without(v, x)
            d = abs(median(v) - median(rest))
            q = dq(c, v, P, "The outlier, %s, is removed. By how much does the median change?" % fmt(x))
            e = ("With the outlier: %s Without it: %s The median changes by only %s − %s = <b>%s</b>. "
                 "An outlier hardly moves the median." % (e_median(v, False), e_median(rest, False),
                                                         fmt(max(median(v), median(rest))), fmt(min(median(v), median(rest))), fmt(d)))
            md_m = abs(mean(v) - mean(rest))
            its.append(mcq_n(q, d, [md_m if clean(md_m) else None, abs(x - median(v)), median(rest), d + 1, d * 2, d + F(1, 2)],
                             e, rnd))
        elif kind == "typical":
            c = CO.next()
            v, x = outlier_data(rnd, c, rnd.choice([7, 8]),
                                lambda v, x: mean(v).denominator == 1 and median(v).denominator == 1
                                and ((x > max(without(v, x)) and mean(v) > max(without(v, x))) or
                                     (x < min(without(v, x)) and mean(v) < min(without(v, x)))))
            m, md, r = mean(v), median(v), rng(v)
            q = dq(c, v, P, "Which measure best describes a typical value?")
            side = "greater" if x > md else "less"
            pull = "up" if x > md else "down"
            e = ("The outlier %s pulls the mean %s to %s, which is %s than every other value. "
                 "The median, %s, stays in the middle of the data, so <b>the median</b> describes a typical value better."
                 % (fmt(x), pull, fmt(m), side, fmt(md)))
            its.append(mcq(q, "the median, %s" % fmt(md),
                           ["the mean, %s" % fmt(m), "the range, %s" % fmt(r),
                            "the %s, %s" % ("greatest value" if x > md else "least value", fmt(x))], e, rnd))
        elif kind == "fair":
            for _ in range(5000):
                v = [rnd.randrange(4, 19) for _ in range(5)]
                if mean(v).denominator == 1 and mean(v) != median(v) and len(set(v)) == 5:
                    break
            q = ("Five friends spent <b>%s</b> on snacks for a BC Ferries trip. They want everyone to pay the "
                 "same amount. How much should each person pay in the end?" % ", ".join(money(x) for x in v))
            e = ("Sharing the total equally is the mean: %s = %s, and %s ÷ 5 = <b>$%s</b>. The mean is the fair-share value."
                 % (plus(v), fmt(sum(v)), fmt(sum(v)), fmt(mean(v))))
            its.append(mcq_n(q, mean(v), [median(v), sum(v), F(sum(v), 4), F(max(v) + min(v), 2)] + fills(mean(v)), e, rnd,
                             show=money))
        elif kind == "shoe":
            q = ("A shoe store in Victoria is ordering new hiking boots. It wants to order the most pairs in the size "
                 "that sells most often. Which measure should it use?")
            e = ("The size that sells most often is the <b>mode</b>. A mean size like 8.3 may not even exist, and the "
                 "median does not tell which size is most popular.")
            its.append(mcq(q, "the mode", ["the mean", "the median", "the range"], e, rnd))
        elif kind == "most":
            for _ in range(5000):
                base = sorted(rnd.sample(range(20, 40), 6))
                d = rnd.choice(base[1:5])
                v = base + [d]
                x = rnd.randint(85, 110)
                w = v + [x]
                dm = mean(w) - mean(v)
                dmed = median(w) - median(v)
                if mean(v).denominator == 1 and clean(mean(w)) and 0 < dmed <= 2 and modes(v) == modes(w) == [d]:
                    break
            rnd.shuffle(v)
            q = ("The numbers of salmon counted at a creek on Vancouver Island on 7 days are <b>%s</b>. "
                 "On the 8th day, %d salmon are counted. Which measure changes the most?" % (lst(v), x))
            e = ("Before: mean %s, median %s, mode %s. After: mean %s, median %s, mode %s. "
                 "The outlier %d pulls <b>the mean</b> up by %s, but the median moves only %s and the mode does not change."
                 % (fmt(mean(v)), fmt(median(v)), fmt(d), fmt(mean(w)), fmt(median(w)), fmt(d), x,
                    fmt(dm) if clean(dm) else "about " + fmt(round(float(dm))), fmt(dmed)))
            its.append(mcq(q, "the mean", ["the median", "the mode", "They all change by the same amount."], e, rnd))
        elif kind == "notchg":
            c = CO.next()
            v, x = outlier_data(rnd, c, 8, lambda v, x: len(modes(v)) == 1 and modes(v) == modes(without(v, x))
                                and median(v) != median(without(v, x)) and mean(v) != mean(without(v, x))
                                and clean(mean(v)) and v.count(modes(v)[0]) == 2)
            rest = without(v, x)
            md = modes(v)[0]
            q = dq(c, v, P, "The outlier, %s, is removed. Which measure stays the same?" % fmt(x))
            e = ("%s still appears twice, so the mode stays <b>%s</b>. The mean changes from %s to %s, the median changes "
                 "from %s to %s, and the range gets much smaller." % (
                     fmt(md), fmt(md), fmt(mean(v)), fmt(mean(rest)) if clean(mean(rest)) else "about " + fmt(round(float(mean(rest)))),
                     fmt(median(v)), fmt(median(rest))))
            its.append(mcq(q, "the mode", ["the mean", "the median", "the range"], e, rnd))
        elif kind == "need":
            ni += 1
            name, pro, pos = P.next()
            if ni == 1:
                T, k = 80, 4
                for _ in range(5000):
                    v = [rnd.randint(68, 92) for _ in range(k)]
                    ans = (k + 1) * T - sum(v)
                    if 70 <= ans <= 98 and abs(ans - T) >= 3 and clean(2 * T - mean(v)) and 2 * T - mean(v) != ans:
                        break
                q = ("%s’s marks on the first %d science tests are <b>%s</b> (out of 100). What mark does %s need on the "
                     "5th test to have a mean of %d?" % (name, k, lst(v), pro, T))
                many = "tests"
            else:
                T, k = 180, 3
                for _ in range(5000):
                    v = [5 * rnd.randint(28, 42) for _ in range(k)]
                    ans = (k + 1) * T - sum(v)
                    if 150 <= ans <= 230 and abs(ans - T) >= 10 and clean(2 * T - mean(v)) and 2 * T - mean(v) != ans:
                        break
                q = ("%s bowled <b>%s</b> in 3 games of 5-pin bowling. What score does %s need in the 4th game to have a "
                     "mean score of %d?" % (name, lst(v), pro, T))
                many = "games"
            e = ("For a mean of %d over %d %s, the total must be %d × %d = %s. So far: %s = %s. "
                 "%s needs %s − %s = <b>%s</b>." % (T, k + 1, many, k + 1, T, fmt((k + 1) * T), plus(v), fmt(sum(v)),
                                                    name, fmt((k + 1) * T), fmt(sum(v)), fmt(ans)))
            its.append(mcq_n(q, ans, [2 * T - mean(v), T, (k + 1) * T]
                             + fills(ans, 2), e, rnd))
        elif kind == "wages":
            for _ in range(20000):
                base = sorted(rnd.sample(range(36, 52), 5))
                d = base[1]
                v = sorted(base + [d])
                own = rnd.randint(140, 170)
                w = v + [own]
                m, md = mean(w), median(w)
                if m.denominator == 1 and md.denominator == 1 and modes(w) == [d] and md > d:
                    break
            k = 1000
            q = ("The 7 people who work at a bike shop in Whistler earn these yearly pay amounts: <b>%s</b>. "
                 "The highest amount is the owner’s. The owner says, “Pay here is high.” Which measure of central "
                 "tendency makes the typical pay look highest?" % ", ".join(money(x * k) for x in w))
            e = ("Mean: %s ÷ 7 = %s. Median (4th value): %s. Mode: %s. The owner’s large pay pulls <b>the mean</b> up, "
                 "so it is the highest. The median, %s, describes a typical worker better." % (
                     money(sum(w) * k), money(m * k), money(md * k), money(d * k), money(md * k)))
            its.append(mcq(q, "the mean, %s" % money(m * k), ["the median, %s" % money(md * k), "the mode, %s" % money(d * k),
                                                              "They are all equal."], e, rnd))
        else:  # lowest
            for _ in range(20000):
                v = [rnd.choice(range(30, 125, 5)) for _ in range(7)]
                ms = modes(v)
                if (len(ms) == 1 and v.count(ms[0]) == 2 and ms[0] < median(v) < mean(v) and mean(v).denominator == 1):
                    break
            name, pro, pos = P.next()
            q = ("%s recorded %s screen time, in minutes, for one week: <b>%s</b>. %s wants the typical value to look as "
                 "low as possible. Which measure of central tendency is lowest?" % (name, pos, lst(v), pro.capitalize()))
            e = ("Mean: %s ÷ 7 = %s. Median: %s Mode: %s appears twice, so it is %s. <b>The mode</b> is lowest here." % (
                fmt(sum(v)), fmt(mean(v)), e_median(v, False), fmt(ms[0]), fmt(ms[0])))
            its.append(mcq(q, "the mode, %s" % fmt(ms[0]), ["the mean, %s" % fmt(mean(v)), "the median, %s" % fmt(median(v)),
                                                           "They are all equal."], e, rnd))
    assert len(its) == 20
    return {"title": "Word problems: outliers and the best measure", "items": its}


# ============================================================ lesson
LV = [8, 5, 9, 6, 9, 3, 9]              # mean 7, median 8, mode 9, range 6
EV = [12, 7, 10, 15, 9, 14]             # even count: median 11
TV = [-6, 2, -9, -1, 4]                 # temperatures: mean −2
DOT_LO, DOT_C = 0, [1, 3, 2, 2, 1, 0, 0, 0, 1]   # books read by 10 students: mean 2.5, median 2, mode 1, range 8


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def body_html():
    s = sorted(LV)
    assert mean(LV) == 7 and median(LV) == 8 and modes(LV) == [9] and rng(LV) == 6
    assert median(EV) == 11 and mean(TV) == -2
    dv = [DOT_LO + i for i in range(len(DOT_C)) for _ in range(DOT_C[i])]
    assert len(dv) == 10 and mean(dv) == F(5, 2) and median(dv) == 2 and modes(dv) == [1] and rng(dv) == 8
    plot = plot_svg(DOT_LO, DOT_C, "Books read last month", "books read by 10 students")
    plot = plot.replace("<svg ", "<svg data-pf='lg' ", 1)
    return (
        "<h2>Three ways to describe a typical value</h2>"
        "<p>A <b>measure of central tendency</b> is one number that describes the centre of a data set: the "
        "<b>mean</b>, the <b>median</b> or the <b>mode</b>. The <b>range</b> is different: it tells how spread out the data are.</p>"
        "<p>Seven quiz scores: <b>" + lst(LV) + "</b>. In order: " + lst(s) + ".</p>" +
        table(["Measure", "How to find it", "Example"], [
            ["Mean", "Add all the values. Divide by how many values there are.", "49 ÷ 7 = <b>7</b>"],
            ["Median", "Put the values in order. Take the middle one.", "3, 5, 6, <b>8</b>, 9, 9, 9 → <b>8</b>"],
            ["Mode", "The value that appears most often", "9 appears 3 times → <b>9</b>"],
            ["Range", "Greatest − least", "9 − 3 = <b>6</b>"],
        ]) +
        "<h2>Median of an even number of values</h2>"
        "<p>With an even count there are two middle values. The median is their mean, so it can end in .5.</p>" +
        ex("Example", "Find the median of " + lst(EV) + ".",
           "In order: " + lst(sorted(EV)) + ". There are 6 values, so the middle values are the 3rd and 4th: 10 and 12. "
           "(10 + 12) ÷ 2 = 11.", "11") +
        "<h2>Data with negative numbers</h2>" +
        ex("Example", "The low temperatures in Prince George on 5 days were " + lst(TV) + " °C. Find the mean and the range.",
           "Mean: " + plus(TV) + " = −10, and −10 ÷ 5 = −2. Range: 4 − (−9) = 4 + 9 = 13.", "mean −2°C, range 13°C") +
        "<h2>Read a dot plot</h2>"
        "<p>Each X is one value, and the X’s are already in order from left to right. "
        "Ten students told how many books they read last month.</p>"
        "<figure class='sn-fig'>" + plot +
        "<figcaption>10 X’s. Mean 2.5, median 2, mode 1, range 8.</figcaption></figure>"
        "<p><b>Mean:</b> 0 × 1 + 1 × 3 + 2 × 2 + 3 × 2 + 4 × 1 + 8 × 1 = 25, and 25 ÷ 10 = 2.5. "
        "<b>Median:</b> the 5th and 6th X’s from the left are both at 2, so the median is 2. "
        "<b>Mode:</b> the tallest stack is at 1. <b>Range:</b> 8 − 0 = 8.</p>"
        "<h2>Outliers and the best measure</h2>"
        "<p>An <b>outlier</b> is a value far from the others, like the 8 above. It pulls the mean toward it, "
        "but it barely moves the median. Here the mean (2.5) is greater than the median (2).</p>" +
        table(["Use the …", "When …", "Example"], [
            ["Mean", "the data have no outliers, or you want a fair share of a total", "Sharing a snack bill equally"],
            ["Median", "the data have an outlier", "House prices, pay at a small business"],
            ["Mode", "you want the most common value, or the data are categories", "Shoe sizes, favourite sport"],
        ]) +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Taking the middle of the list without putting it in order", "Order the values from least to greatest first"],
            ["Picking one middle value when the count is even", "Use the mean of the two middle values"],
            ["Ignoring the signs of negative numbers", "−9 is less than −1; add negatives as negatives"],
            ["Giving the count as the mode (“3 times”)", "The mode is the value that repeats, not how many times"],
            ["Giving the greatest value as the range", "Range = greatest − least"],
            ["Using the mean when there is an outlier", "The median describes a typical value better"],
        ])
    )


FAQ = [
    {"q": "Is central tendency taught in Grade 8 in BC?",
     "a": "Yes. Central tendency is a Grade 8 content standard in the Data and probability area of the BC math curriculum. Students find the mean, median and mode, and decide which one best describes a data set."},
    {"q": "How do you find the median when there is an even number of values?",
     "a": "Put the values in order and find the two middle ones, then take their mean. For 7, 9, 10, 12, 14, 15 the middle values are 10 and 12, so the median is 11."},
    {"q": "When is the median better than the mean?",
     "a": "When the data have an outlier. One very large or very small value pulls the mean toward it, but the median stays near the middle of the data."},
    {"q": "Is the range a measure of central tendency?",
     "a": "No. The mean, median and mode describe a typical value. The range (greatest − least) describes how spread out the data are."},
]


def gen_unit():
    rnd = random.Random(58812)
    P = People(rnd)
    sets = [set_mean(rnd, P), set_median(rnd, P), set_mode(rnd, P), set_range(rnd, P), set_word(rnd, P)]
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["e"], it
            assert it["q"].count("<svg") <= 1
            assert it["q"] not in seen, it["q"]
            seen.add(it["q"])
            for x in [it["q"], it["e"]] + it["c"]:
                t = re.sub(r"<svg.*?</svg>", "", x)
                assert not re.search(r"\d,\d{3}", t), x
                assert not re.search(r"\d \d{3}", t), x
    balance(sets, rnd)
    for s in sets:
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5)
    u = {
        "country": "ca-bc", "subject": "math", "grade": "grade-8", "slug": "central-tendency", "sort": 12,
        "updated": UPDATED, "pdf_url": "",
        "title": "Grade 8 Central Tendency: Mean, Median, Mode and Range",
        "seo_title": "Grade 8 Mean, Median and Mode Worksheets: Range, Outliers and the Best Measure (Free, with Answer Key, BC Curriculum)",
        "short_title": "Central tendency",
        "domain": "Data and probability",
        "standard_code": "Grade 8: Data and probability",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/8/core",
        "standard_text": "Central tendency",
        "meta_desc": "Free Grade 8 math worksheets on central tendency for the BC curriculum: find the mean, the median of odd and even counts, the mode and the range, with negative numbers, decimals and dot plots, and choose the best measure when data have an outlier. 100 questions with an answer key.",
        "key_big": "Mean = sum ÷ count. Median = the middle value once the data are in order. Mode = the most common value.",
        "key_sub": "With an even count, the median is the mean of the two middle values. The range (greatest − least) shows spread. An outlier pulls the mean toward it, so the median is often the better typical value.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "dot plot")


if __name__ == "__main__":
    u = gen_unit()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(u, f, ensure_ascii=False, indent=1)
    print("wrote", path)
