# -*- coding: utf-8 -*-
"""
Hand-made question makers for the UK maths units that other generators did not cover:
GCSE Year 11 (histograms, iteration, algebraic proof, velocity–time graphs, the equation of a circle with centre the origin)
and A level (proof, the product and quotient rules, hypothesis tests for a normal mean and for correlation).
Every maker takes a random.Random and returns an item or None (uk_alevel._collect keeps the questions different).
Wrong answers come from real mistakes: frequency × width for frequency density, the wrong iterate, a factor that does not
divide every term, a sign slip in the tangent, forgetting one term of the product rule, σ/n for the standard error,
comparing |z| with the one-tailed value in a two-tailed test.
"""
import math
from fractions import Fraction as F
from uk_ks3 import T, num, MINUS, GIRLS, BOYS
from ws_common import svg_wrap, text, line, INK, RED, BLUE, table
from uk_alevel_own import n, d, poly, item, coef, X

Y = "<i>y</i>"
NV = "<i>n</i>"
SUPS = {0: "", 1: "", 2: "²", 3: "³", 4: "⁴", 5: "⁵", 6: "⁶"}


def xp(m, v=X):
    """x to the power m (m ≥ 0)"""
    if m == 0:
        return ""
    return v + SUPS.get(m, "<sup>%d</sup>" % m)


def fx(v, dp=3):
    """fixed decimals with the real minus sign"""
    return ("%." + str(dp) + "f") % v if v >= 0 else MINUS + ("%." + str(dp) + "f") % -v


def who(r):
    return r.choice(GIRLS + BOYS)


def figq(svg):
    return "<div class='qfig'>" + svg.replace("<svg ", "<svg data-pf='lg' ", 1) + "</div>"


# =================================================================== GCSE: histograms
HCTX = [("times taken to finish a puzzle", "minutes", "<i>t</i>", [0, 10], [5, 10, 15, 20]), ("heights of some plants", "cm", "<i>h</i>", [0, 10, 20], [5, 10, 20, 30]),
        ("masses of some apples", "g", "<i>m</i>", [80, 100, 120], [10, 20, 30, 40]), ("ages of the members of a club", "years", "<i>a</i>", [0, 10, 20], [5, 10, 15, 20]),
        ("lengths of some phone calls", "minutes", "<i>t</i>", [0], [2, 4, 5, 10]), ("distances pupils live from school", "km", "<i>d</i>", [0], [1, 2, 4, 5]),
        ("times pupils spent on homework", "minutes", "<i>t</i>", [0, 10], [10, 15, 20, 30]), ("lengths of some leaves", "mm", "<i>l</i>", [20, 40], [5, 10, 20]),
        ("masses of some parcels", "kg", "<i>m</i>", [0], [1, 2, 4, 5]), ("speeds of some cars", "km/h", "<i>s</i>", [20, 30, 40], [10, 20])]
FDS = [F(x) for x in ("0.2", "0.4", "0.5", "0.6", "0.8", "1", "1.2", "1.4", "1.5", "1.6", "1.8", "2", "2.4", "2.5", "3", "3.2", "3.5", "4", "4.5", "5", "6", "7.5")]


def dn(v):
    return num(v) or d(float(v), 2)


def cls(lo, hi, v):
    return "%s &lt; %s ≤ %s" % (num(lo), v, num(hi))


def classes(r, k=None, c=None):
    k = k or r.choice([4, 5])
    c = c or r.choice(HCTX)
    step = r.choice([F(1, 5), F(1, 2), F(1)])
    lo = r.choice(c[3])
    out = []
    for _ in range(k):
        w = r.choice(c[4])
        ok = [step * j for j in range(1, 9) if (step * j * w).denominator == 1 and 2 <= step * j * w <= 60]
        if not ok:
            return None
        out.append((lo, lo + w, r.choice(ok)))
        lo += w
    return out, step


def hist_svg(cl, var, unit, step):
    x0, x1 = cl[0][0], cl[-1][1]
    top = max(c[2] for c in cl)
    ny = max(5, int(math.ceil(top / step)))
    L, TOP, W, H = 54, 14, 300, 170
    X = lambda v: L + float(v - x0) / (x1 - x0) * W
    Yp = lambda v: TOP + H - float(v) / float(ny * step) * H
    s = []
    for j in range(ny + 1):
        s.append(line(L, Yp(j * step), L + W, Yp(j * step), "#e2e2e2", 1))
        s.append(text(L - 6, Yp(j * step) + 4, d(float(j * step), 1), 11, anchor="end", weight=400))
    for lo, hi, fd in cl:
        s.append("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' fill='#cfe0f3' stroke='%s' stroke-width='2'/>" % (X(lo), Yp(fd), X(hi) - X(lo), Yp(0) - Yp(fd), BLUE))
    s.append(line(L, Yp(0), L + W + 6, Yp(0), INK, 2))
    s.append(line(L, Yp(0), L, TOP - 4, INK, 2))
    for b in sorted(set([c[0] for c in cl] + [cl[-1][1]])):
        s.append(text(X(b), Yp(0) + 16, num(b), 11, weight=400))
    s.append(text(L + W / 2, Yp(0) + 36, "%s (%s)" % (var.replace("<i>", "").replace("</i>", ""), unit), 13))
    s.append("<text x='14' y='%d' font-size='12' font-weight='700' fill='%s' text-anchor='middle' transform='rotate(-90 14 %d)'>Frequency density</text>" % (TOP + H / 2, INK, TOP + H / 2))
    return svg_wrap(L + W + 20, TOP + H + 46, "".join(s), "histogram")


def h_fd(r):
    c = r.choice(HCTX)
    w = r.choice(c[4] + [3 * c[4][0]])
    lo = r.choice(c[3]) + r.randint(0, 3) * c[4][0]
    fd = r.choice([f for f in FDS + [F(x) for x in ("0.3", "0.7", "0.9", "1.1", "2.2", "2.8", "3.6")] if (f * w).denominator == 1 and 2 <= f * w <= 80])
    f = int(fd * w)
    q = "The table shows the %s. The class %s has frequency %d. Work out the frequency density for this class." % (c[0], cls(lo, lo + w, c[2]), f)
    return item(q, dn(fd), [n(f * w), dn(F(w, f)), dn(F(f, lo + w))], "Frequency density = frequency ÷ class width = %d ÷ %d = <b>%s</b>." % (f, w, dn(fd)))


def h_freq(r):
    c = r.choice(HCTX)
    w = r.choice(c[4] + [3 * c[4][0]])
    lo = r.choice(c[3]) + r.randint(0, 3) * c[4][0]
    fd = r.choice([f for f in FDS if (f * w).denominator == 1])
    f = fd * w
    q = "On a histogram of the %s, the bar for %s has height (frequency density) %s. How many are in this class?" % (c[0], cls(lo, lo + w, c[2]), dn(fd))
    return item(q, n(f), [dn(fd / w), dn(fd + w), dn(fd * (lo + w)) if lo else n(fd * w * 2)], "Frequency = frequency density × class width = %s × %d = <b>%s</b>." % (dn(fd), w, n(f)))


def h_read(r):
    c = r.choice(HCTX)
    got = classes(r, c=c)
    if not got:
        return None
    cl, step = got
    k = r.choice(["one", "total", "more", "over"])
    svg = figq(hist_svg(cl, c[2], c[1], step))
    fr = [int(fd * (hi - lo)) for lo, hi, fd in cl]
    if k == "one":
        i = r.randrange(len(cl))
        lo, hi, fd = cl[i]
        q = svg + "The histogram shows the %s. How many are in the class %s?" % (c[0], cls(lo, hi, c[2]))
        return item(q, num(fr[i]), [dn(fd), num(fr[i] * 2) if hi - lo != 2 else num(fr[i] + 5), dn(fd * 10) if hi - lo != 10 else num(fr[i] + 10)],
                    "Frequency = frequency density × class width = %s × %d = <b>%d</b>." % (dn(fd), hi - lo, fr[i]))
    if k == "total":
        q = svg + "The histogram shows the %s. Work out the total frequency." % c[0]
        return item(q, num(sum(fr)), [dn(sum(x[2] for x in cl)), num(sum(fr) - fr[0]), num(sum(int(x[2] * 10) for x in cl))],
                    "Add frequency density × width for every bar: %s = <b>%d</b>." % (" + ".join(str(x) for x in fr), sum(fr)))
    if k == "more":
        i, j = r.sample(range(len(cl)), 2)
        if fr[i] == fr[j]:
            return None
        a, b = (i, j) if fr[i] > fr[j] else (j, i)
        q = svg + "The histogram shows the %s. How many more are in the class %s than in the class %s?" % (c[0], cls(cl[a][0], cl[a][1], c[2]), cls(cl[b][0], cl[b][1], c[2]))
        diff = fr[a] - fr[b]
        return item(q, num(diff), [dn(abs(cl[a][2] - cl[b][2])), num(fr[a] + fr[b]), num(abs(diff - 2) if diff != 2 else diff + 4)],
                    "%s class: %d. %s class: %d. Difference <b>%d</b>." % ("First", fr[a], "Second", fr[b], diff))
    i = r.randrange(1, len(cl))
    v = cl[i][0]
    tot = sum(fr[i:])
    q = svg + "The histogram shows the %s. How many have %s &gt; %s %s?" % (c[0], c[2], num(v), c[1])
    return item(q, num(tot), [num(sum(fr[:i])), num(tot - fr[i]), dn(sum(x[2] for x in cl[i:]))], "Add the frequencies of the bars to the right of %s: <b>%d</b>." % (num(v), tot))


def h_est(r):
    c = r.choice(HCTX)
    got = classes(r, 4, c)
    if not got:
        return None
    cl = got[0]
    fr = [int(fd * (hi - lo)) for lo, hi, fd in cl]
    i = r.randrange(len(cl))
    lo, hi, fd = cl[i]
    w = hi - lo
    ks = [k for k in range(1, w) if (fd * k).denominator == 1]
    if not ks:
        return None
    v = hi - r.choice(ks)
    part = fd * (hi - v)
    if part.denominator != 1:
        return None
    rest = sum(fr[i + 1:])
    ans = part + rest
    tb = table(["%s (%s)" % (c[2], c[1]), "Frequency"], [[cls(a, b, c[2]), str(f)] for (a, b, _), f in zip(cl, fr)])
    q = tb + "The table shows the %s. Estimate how many have %s &gt; %s %s." % (c[0], c[2], num(v), c[1])
    return item(q, n(ans), [n(fr[i] + rest), n(rest), n(fd * (v - lo) + rest)],
                "In the class %s, %d %s of the %d %s are above %s, so about %d/%d × %d = %s. Add the classes above: %s + %d = <b>%s</b>." % (cls(lo, hi, c[2]), hi - v, c[1], w, c[1], num(v), hi - v, w, fr[i], n(part), n(part), rest, n(ans)))


def h_scale(r):
    c = r.choice(HCTX)
    w1, w2 = r.sample(c[4] + [3 * c[4][0]], 2)
    f1 = r.choice([6, 8, 10, 12, 15, 16, 18, 20, 24, 30])
    h1 = r.choice([F(3), F(4), F(2), F(5), F(6), F(9, 2), F(5, 2)])
    unit = h1 / (F(f1, w1))  # cm per unit of fd
    f2 = r.choice([6, 9, 10, 12, 14, 15, 18, 20, 21, 24, 27, 30, 36])
    h2 = unit * F(f2, w2)
    if (h2 * 10).denominator != 1 or h2 > 15 or h2 < F(1, 2):
        return None
    lo1 = r.choice(c[3])
    q = ("In a histogram of the %s, the class %s has frequency %d and its bar is %s cm tall. "
         "How tall should the bar be for a class of width %d with frequency %d?" % (c[0], cls(lo1, lo1 + w1, c[2]), f1, d(float(h1), 1), w2, f2))
    wrong = [h1 * f2 / f1, unit * F(f2, w1), h1 * F(w2, w1)]
    return item(q, "%s cm" % d(float(h2), 1), ["%s cm" % d(float(x), 2) for x in wrong if (x * 100).denominator == 1] + ["%s cm" % d(float(h2) * 2, 1)],
                "Height is proportional to frequency density. %d ÷ %d = %s and %d ÷ %d = %s, so height = %s × %s ÷ %s = <b>%s cm</b>." % (f1, w1, dn(F(f1, w1)), f2, w2, dn(F(f2, w2)), d(float(h1), 1), dn(F(f2, w2)), dn(F(f1, w1)), d(float(h2), 1)))


def h_highest(r):
    c = r.choice(HCTX)
    got = classes(r, 4, c)
    if not got:
        return None
    cl = got[0]
    fr = [int(fd * (hi - lo)) for lo, hi, fd in cl]
    tb = table(["%s (%s)" % (c[2], c[1]), "Frequency"], [[cls(a, b, c[2]), str(f)] for (a, b, _), f in zip(cl, fr)])
    fds = [x[2] for x in cl]
    if fds.count(max(fds)) > 1 or fr.index(max(fr)) == fds.index(max(fds)) or fr.count(max(fr)) > 1:
        return None
    i = fds.index(max(fds))
    j = fr.index(max(fr))
    q = tb + "The table shows the %s. Which class will have the tallest bar on a histogram?" % c[0]
    opts = [cls(a, b, c[2]) for a, b, _ in cl]
    right = opts[i]
    return item(q, right, [opts[j]] + [o for o in opts if o not in (right, opts[j])], "The tallest bar has the greatest frequency density (frequency ÷ width), not the greatest frequency: %d ÷ %d = %s." % (fr[i], cl[i][1] - cl[i][0], dn(cl[i][2])))


# =================================================================== GCSE: iteration
def _it(form, a, b):
    if form == "cbrt":
        return lambda x: (a * x + b) ** (1 / 3), "∛(%d%s<sub>n</sub> + %d)" % (a, X, b)
    if form == "sqrt":
        return lambda x: (a * x + b) ** 0.5, "√(%d%s<sub>n</sub> + %d)" % (a, X, b)
    if form == "recip":
        return lambda x: a + b / x, "%d + %d/%s<sub>n</sub>" % (a, b, X)
    if form == "sq":
        return lambda x: a + b / (x * x), "%d + %d/%s<sub>n</sub>²" % (a, b, X)
    return lambda x: (b - a * x) ** (1 / 3) if b - a * x > 0 else float("nan"), "∛(%d − %d%s<sub>n</sub>)" % (b, a, X)


def it_val(r):
    form = r.choice(["cbrt", "sqrt", "recip", "sq", "cbrt2"])
    a, b = r.randint(2, 9), r.randint(1, 12)
    if form == "cbrt2":
        a, b = r.randint(1, 3), r.randint(8, 30)
    g, s = _it(form, a, b)
    x0 = r.choice([1, 1.5, 2, 2.5, 3, 4])
    xs = [x0]
    for _ in range(4):
        xs.append(g(xs[-1]))
    if any(v != v or v <= 0 for v in xs):
        return None
    k = r.choice([1, 2, 3])
    q = "Use the iteration formula %s<sub>n+1</sub> = %s with %s<sub>0</sub> = %s to find %s<sub>%d</sub>. Give your answer to 3 decimal places." % (X, s, X, d(x0), X, k)
    w = ["%.3f" % xs[k - 1] if k > 1 else "%.3f" % (a * x0 + b), "%.3f" % xs[k + 1], "%.3f" % (xs[k] + 0.001 * r.choice([1, -1]) * 3)]
    return item(q, "%.3f" % xs[k], w, "Put each answer back into the formula: %s." % ", ".join("%s<sub>%d</sub> = %.5f" % (X, i, xs[i]) for i in range(1, k + 1)))


def _eqs(form, a, b):
    """(equation, right rearrangement, wrong rearrangements)"""
    if form == "cbrt":
        return ("%s³ − %d%s − %d = 0" % (X, a, X, b), "%s = ∛(%d%s + %d)" % (X, a, X, b), ["%s = ∛(%d%s − %d)" % (X, a, X, b), "%s = ∛(%d − %d%s)" % (X, b, a, X), "%s = (%d%s + %d)/3" % (X, a, X, b)])
    if form == "cbrt2":
        return ("%s³ + %d%s − %d = 0" % (X, a, X, b), "%s = ∛(%d − %d%s)" % (X, b, a, X), ["%s = ∛(%d%s + %d)" % (X, a, X, b), "%s = ∛(%d%s − %d)" % (X, a, X, b), "%s = ∛%d − %d%s" % (X, b, a, X)])
    if form == "sqrt":
        return ("%s² − %d%s − %d = 0" % (X, a, X, b), "%s = √(%d%s + %d)" % (X, a, X, b), ["%s = √(%d%s − %d)" % (X, a, X, b), "%s = √(%d − %d%s)" % (X, b, a, X), "%s = %d − %d/%s" % (X, a, b, X)])
    if form == "recip":
        return ("%s² − %d%s − %d = 0" % (X, a, X, b), "%s = %d + %d/%s" % (X, a, b, X), ["%s = %d − %d/%s" % (X, a, b, X), "%s = %d + %d/%s" % (X, b, a, X), "%s = √(%d%s − %d)" % (X, a, X, b)])
    return ("%s³ − %d%s² − %d = 0" % (X, a, X, b), "%s = %d + %d/%s²" % (X, a, b, X), ["%s = %d − %d/%s²" % (X, a, b, X), "%s = %d + %d/%s²" % (X, b, a, X), "%s = %d + %d/%s" % (X, a, b, X)])


def it_rearr(r):
    form = r.choice(["cbrt", "cbrt2", "sqrt", "recip", "sq"])
    a, b = r.randint(2, 9), r.randint(1, 15)
    if a == b:
        return None
    eq, right, wrong = _eqs(form, a, b)
    if r.random() < 0.6:
        return item("Which of these is a rearrangement of %s?" % eq, right, wrong, "Rearrange carefully, keeping the signs: %s." % right)
    others = [_eqs(f, a, b)[0] for f in ("cbrt", "cbrt2", "sqrt", "sq") if _eqs(f, a, b)[0] != eq]
    alt = {"cbrt": "%s³ + %d%s + %d = 0" % (X, a, X, b), "cbrt2": "%s³ − %d%s + %d = 0" % (X, a, X, b), "sqrt": "%s² + %d%s − %d = 0" % (X, a, X, b),
           "recip": "%s² + %d%s − %d = 0" % (X, a, X, b), "sq": "%s³ + %d%s² − %d = 0" % (X, a, X, b)}[form]
    return item("The iteration %s<sub>n+1</sub> = %s is used to solve an equation. Which equation?" % (X, right.split(" = ", 1)[1].replace(X, X + "<sub>n</sub>")), eq,
                [alt] + others, "Replace %s<sub>n</sub> and %s<sub>n+1</sub> by %s and rearrange to make one side 0: <b>%s</b>." % (X, X, X, eq))


def _root(f, lo, hi):
    for _ in range(80):
        m = (lo + hi) / 2
        if (f(lo) < 0) == (f(m) < 0):
            lo = m
        else:
            hi = m
    return (lo + hi) / 2


def it_sign(r):
    a, b = r.randint(2, 12), r.randint(1, 20)
    p = r.choice([1, -1])
    f = lambda x: x ** 3 - a * x - b if p == 1 else x ** 3 + a * x - b
    eq = "%s³ %s %d%s − %d = 0" % (X, "−" if p == 1 else "+", a, X, b)
    root = _root(f, 0.0, 10.0)
    if abs(root - round(root)) < 0.05 or f(0) >= 0:
        return None
    m = int(math.floor(root))
    k = r.choice(["int", "show", "val"])
    if k == "int":
        return item("Between which two consecutive whole numbers is the positive solution of %s?" % eq, "%d and %d" % (m, m + 1),
                    ["%d and %d" % (m + 1, m + 2), "%d and %d" % (m - 1, m) if m >= 1 else "%d and %d" % (m + 2, m + 3), "%d and %d" % (m + 2, m + 3) if m >= 1 else "%d and %d" % (m + 3, m + 4)],
                    "Let f(%s) = %s. f(%d) = %s and f(%d) = %s. The sign changes, so the solution is between %d and %d." % (X, eq[:-4], m, n(int(f(m))), m + 1, n(int(f(m + 1))), m, m + 1))
    if k == "val":
        v = r.choice([m, m + 1])
        return item("f(%s) = %s. Work out f(%d)." % (X, eq[:-4], v), n(int(f(v))), [n(int(v ** 3 - (a * v if p == 1 else -a * v) + b)), n(int(3 * v - (a * v if p == 1 else -a * v) - b)), n(-int(f(v)))],
                    "Substitute %s = %d: %d³ %s %d × %d − %d = <b>%s</b>." % (X, v, v, "−" if p == 1 else "+", a, v, b, n(int(f(v)))))
    return item("f(%s) = %s. f(%d) = %s and f(%d) = %s. What does this show?" % (X, eq[:-4], m, n(int(f(m))), m + 1, n(int(f(m + 1)))),
                "f(%s) = 0 has a solution between %d and %d, because the sign changes" % (X, m, m + 1),
                ["%s = %d is a solution of f(%s) = 0" % (X, m, X), "f(%s) = 0 has no solution between %d and %d" % (X, m, m + 1), "the solution is %s exactly" % d(m + 0.5, 1)],
                "f is continuous and changes from negative to positive, so it crosses zero between %d and %d." % (m, m + 1))


def it_conv(r):
    form = r.choice(["cbrt", "sqrt", "recip", "sq"])
    a, b = r.randint(2, 9), r.randint(1, 12)
    g, s = _it(form, a, b)
    x = r.choice([1, 2, 3])
    x0 = x
    for _ in range(200):
        x = g(x)
    root = x
    xs = [x0]
    for _ in range(3):
        xs.append(g(xs[-1]))
    right = "%.2f" % root
    w = ["%.2f" % xs[1], "%.2f" % (root + 0.01), "%.2f" % (root - 0.01), "%.2f" % (math.floor(root * 100) / 100)]
    eq = {"cbrt": "%s³ − %d%s − %d = 0" % (X, a, X, b), "sqrt": "%s² − %d%s − %d = 0" % (X, a, X, b), "recip": "%s² − %d%s − %d = 0" % (X, a, X, b), "sq": "%s³ − %d%s² − %d = 0" % (X, a, X, b)}[form]
    q = "Use %s<sub>n+1</sub> = %s with %s<sub>0</sub> = %d. Keep going until the values stop changing, and give a solution of %s to 2 decimal places." % (X, s, X, x0, eq)
    return item(q, right, w, "%s<sub>1</sub> = %.4f, %s<sub>2</sub> = %.4f, %s<sub>3</sub> = %.4f, … The values settle at %.4f, so %s = <b>%s</b> to 2 decimal places." % (X, xs[1], X, xs[2], X, xs[3], root, X, right))


# =================================================================== GCSE: algebraic proof
def p_form(r):
    kind = r.choice(["odd", "even", "m3", "m4", "m5", "m6"])
    if kind == "odd":
        b = r.choice([1, 3, 5, 7, -1])
        right = poly({1: 2, 0: b}, NV)
        wr = [poly({1: 2, 0: b + 1}, NV), poly({1: 1, 0: 1}, NV), poly({1: 3, 0: b}, NV), poly({2: 1, 0: 1}, NV)]
        return item("<i>n</i> is an integer. Which expression is always odd?", right, wr, "2<i>n</i> is always even, so 2<i>n</i> plus an odd number is always odd.")
    if kind == "even":
        a, b = r.choice([(2, 2), (2, 4), (4, 2), (2, 6), (6, 4), (4, 6), (2, 0)])
        right = poly({1: a, 0: b}, NV)
        wr = [poly({1: a, 0: b + 1}, NV), poly({1: 1, 0: b + 2}, NV), poly({1: 3, 0: b}, NV), poly({2: 1, 0: 2}, NV)]
        return item("<i>n</i> is an integer. Which expression is always even?", right, wr, "%s = 2(%s), so it is a multiple of 2." % (right, poly({1: a // 2, 0: b // 2}, NV)))
    k = int(kind[1])
    p, c = r.randint(1, 4), r.randint(1, 5)
    right = poly({1: k * p, 0: k * c}, NV)
    wr = [poly({1: k * p, 0: k * c + 1}, NV), poly({1: k * p + 1, 0: k * c}, NV), poly({1: k * p, 0: k * c + k - 1}, NV) if k > 2 else poly({1: p, 0: k * c}, NV), poly({1: p, 0: k * c}, NV)]
    return item("<i>n</i> is an integer. Which expression is always a multiple of %d?" % k, right, wr, "%s = %d(%s), so it is %d × an integer." % (right, k, poly({1: p, 0: c}, NV), k))


def p_consec(r):
    if r.random() < 0.5:
        k = r.choice([2, 3, 4, 5, 6])
        ev = r.random() < 0.5
        st = 0 if ev else 1
        terms = " + ".join("(2<i>n</i> + %d)" % (st + 2 * i) if st + 2 * i else "2<i>n</i>" for i in range(k))
        s0 = sum(st + 2 * i for i in range(k))
        right = poly({1: 2 * k, 0: s0}, NV)
        return item("Simplify the sum of %d consecutive %s numbers %s." % (k, "even" if ev else "odd", terms), right,
                    [poly({1: 2 * k, 0: s0 + 2}, NV), poly({1: k, 0: s0}, NV), poly({1: 2 * k, 0: 2 * k}, NV) if s0 != 2 * k else poly({1: 2, 0: s0}, NV)],
                    "There are %d lots of 2<i>n</i> and the numbers add to %d: <b>%s</b>." % (k, s0, right))
    k = r.choice([2, 3, 4, 5, 6, 7])
    kind = r.choice(["sum", "mult"]) if k % 2 else "sum"
    s0 = k * (k - 1) // 2
    terms = " + ".join(["<i>n</i>"] + ["(<i>n</i> + %d)" % i for i in range(1, k)])
    if kind == "sum":
        right = poly({1: k, 0: s0}, NV)
        wr = [poly({1: k, 0: k}, NV), poly({1: k, 0: s0 + k}, NV), poly({1: 1, 0: s0}, NV), poly({1: k, 0: k - 1}, NV)]
        return item("Simplify the sum of %d consecutive integers %s." % (k, terms), right, wr, "There are %d lots of <i>n</i> and 1 + 2 + … + %d = %d." % (k, k - 1, s0))
    right = "%d, because the sum is %d(%s)" % (k, k, poly({1: 1, 0: s0 // k}, NV))
    wr = ["%d, because the sum is %d(%s)" % (k + 1, k + 1, poly({1: 1, 0: s0 // k}, NV)), "%d, because the sum is %s" % (2 * k, poly({1: k, 0: s0}, NV)),
          "no number, because <i>n</i> can be anything"]
    return item("Which number always divides the sum of %d consecutive integers?" % k, right, wr, "%s = %s = %d(%s)." % (terms, poly({1: k, 0: s0}, NV), k, poly({1: 1, 0: s0 // k}, NV)))


def p_expand(r):
    kind = r.choice(["dsq", "dsq", "plus", "odd", "prod", "odd2"])
    a = r.randint(1, 9)
    if kind == "dsq":
        q = "Expand and simplify (<i>n</i> + %d)² − (<i>n</i> − %d)²." % (a, a)
        right = poly({1: 4 * a}, NV)
        return item(q, right, [poly({1: 2 * a}, NV), "0", poly({2: 2, 0: 2 * a * a}, NV), poly({1: 4 * a, 0: 2 * a * a}, NV)], "(%s) − (%s) = <b>%s</b>, which is always a multiple of %d." % (poly({2: 1, 1: 2 * a, 0: a * a}, NV), poly({2: 1, 1: -2 * a, 0: a * a}, NV), right, 4 * a))
    if kind == "plus":
        b = r.randint(1, 9)
        q = "Expand and simplify (<i>n</i> + %d)² − <i>n</i>(<i>n</i> + %d)." % (a, b)
        if 2 * a == b:
            return None
        right = poly({1: 2 * a - b, 0: a * a}, NV)
        return item(q, right, [poly({1: 2 * a + b, 0: a * a}, NV), poly({1: -b, 0: a * a}, NV), poly({1: 2 * a - b, 0: 2 * a}, NV)], "(%s) − (%s) = <b>%s</b>." % (poly({2: 1, 1: 2 * a, 0: a * a}, NV), poly({2: 1, 1: b}, NV), right))
    if kind == "odd":
        q = "Expand and simplify (2<i>n</i> + %d)² − (2<i>n</i> − %d)²." % (a, a)
        right = poly({1: 8 * a}, NV)
        return item(q, right, [poly({1: 4 * a}, NV), poly({1: 8 * a, 0: 2 * a * a}, NV), "0", poly({2: 8, 0: 2 * a * a}, NV)], "(%s) − (%s) = <b>%s</b>." % (poly({2: 4, 1: 4 * a, 0: a * a}, NV), poly({2: 4, 1: -4 * a, 0: a * a}, NV), right))
    if kind == "odd2":
        b = r.choice([x for x in (1, 3, 5, 7) if x != a])
        if a % 2 == 0:
            return None
        q = "Expand and simplify (2<i>n</i> + %d)² + (2<i>n</i> + %d)²." % (a, b)
        right = poly({2: 8, 1: 4 * (a + b), 0: a * a + b * b}, NV)
        return item(q, right, [poly({2: 8, 1: 2 * (a + b), 0: a * a + b * b}, NV), poly({2: 4, 1: 4 * (a + b), 0: a * a + b * b}, NV), poly({2: 8, 0: a * a + b * b}, NV)],
                    "Expand each bracket and collect: <b>%s</b>. Every term but the last is even and the last is even too, so the sum of two odd squares is even." % right)
    b = r.choice([x for x in range(1, 9) if x != a])
    q = "Expand and simplify (<i>n</i> + %d)(<i>n</i> + %d) − <i>n</i>(<i>n</i> + %d)." % (a, b, a + b)
    return item(q, num(a * b), [poly({1: a + b, 0: a * b}, NV), num(a + b), poly({2: 1, 0: a * b}, NV)], "(%s) − (%s) = <b>%d</b>, the same for every <i>n</i>." % (poly({2: 1, 1: a + b, 0: a * b}, NV), poly({2: 1, 1: a + b}, NV), a * b))


def p_counter(r):
    kind = r.choice(["mult", "mult", "sqgt", "prime", "sqrt", "half"])
    if kind == "mult":
        p = r.choice([2, 3, 4, 5, 6])
        qq = p * r.choice([2, 3])
        c = [p * k for k in range(1, 13) if (p * k) % qq]
        g = [qq * k for k in range(1, 8)]
        right = num(r.choice(c))
        return item("%s says: “Every multiple of %d is a multiple of %d.” Which number shows that this is wrong?" % (who(r), p, qq), right, [num(x) for x in r.sample(g, 3)],
                    "%s is a multiple of %d but not of %d, so it is a counterexample." % (right, p, qq))
    if kind == "sqgt":
        v = r.choice(["0", "1", "½", "0.5", "0.2", "¼", "0.1"])
        return item("%s says: “For every number <i>x</i>, <i>x</i>² &gt; <i>x</i>.” Which value of <i>x</i> is a counterexample?" % who(r), v, [str(x) for x in r.sample([2, 3, 5, 10, -1, -2, -3], 3)],
                    "When <i>x</i> = %s, <i>x</i>² is not bigger than <i>x</i>, so the statement is false." % v)
    if kind == "prime":
        c, ce = r.choice([(1, [4, 5]), (11, [10, 11]), (17, [16, 17]), (41, [40, 41]), (3, [3]), (5, [4, 5])])
        expr_ = poly({2: 1, 1: 1, 0: c}, NV)
        val = ce[0]
        good = [k for k in range(1, 6) if all(((k * k + k + c) % pr) for pr in range(2, int((k * k + k + c) ** 0.5) + 1)) and k != val]
        if len(good) < 3:
            return None
        return item("%s says: “%s is prime for every positive integer <i>n</i>.” Which value of <i>n</i> shows this is false?" % (who(r), expr_), num(val), [num(x) for x in good[:3]],
                    "When <i>n</i> = %d, %s = %d, which is not prime." % (val, expr_, val * val + val + c))
    if kind == "sqrt":
        v = r.choice(["0.25", "0.04", "0.09", "0.16", "¼", "0.36"])
        return item("%s says: “The square root of a number is always smaller than the number.” Which number is a counterexample?" % who(r), v, [str(x) for x in r.sample([4, 9, 16, 25, 100, 36], 3)],
                    "√%s is bigger than %s, so the statement is false." % (v, v))
    a = r.choice([2, 3, 4, 5, 6, 7, 8])
    return item("%s says: “If <i>a</i> &gt; <i>b</i> then <i>a</i>² &gt; <i>b</i>².” Which pair is a counterexample?" % who(r), "<i>a</i> = 1, <i>b</i> = %s" % n(-a),
                ["<i>a</i> = %d, <i>b</i> = %d" % (a + 1, a), "<i>a</i> = %d, <i>b</i> = 1" % a, "<i>a</i> = %d, <i>b</i> = 0" % a], "1 &gt; %s but 1² = 1 is smaller than (%s)² = %d." % (n(-a), n(-a), a * a))


def p_factor(r):
    k = r.choice([2, 3, 4, 5, 6, 7, 8, 9])
    p, c = r.randint(1, 5), r.randint(1, 7)
    e = poly({1: k * p, 0: k * c}, NV)
    right = "%s = %d(%s)" % (e, k, poly({1: p, 0: c}, NV))
    wr = ["%s = %d(%s)" % (e, k, poly({1: p, 0: k * c}, NV)), "%s = %d(%s)" % (e, k * p, poly({1: 1, 0: c}, NV)) if c % k else "%s = %d(%s)" % (e, k + 1, poly({1: p, 0: c}, NV)),
          "%s = %d × %d<i>n</i> + %d" % (e, k, p, k * c), "%s = %d(%s)" % (e, k, poly({1: p, 0: c + 1}, NV))]
    return item("Which line proves that %s is always a multiple of %d for every integer <i>n</i>?" % (e, k), right, wr, "Take out the factor %d: %s. %d × an integer is a multiple of %d." % (k, right, k, k))


def p_odd(r):
    kind = r.choice(["prod", "sum", "sqodd", "evensq"])
    if kind == "prod":
        q = "To prove the product of two odd numbers is odd: (2<i>m</i> + 1)(2<i>n</i> + 1) = 4<i>mn</i> + 2<i>m</i> + 2<i>n</i> + 1 = 2(…) + 1. What goes in the bracket?"
        return None if r.random() < 0.7 else item(q, "2<i>mn</i> + <i>m</i> + <i>n</i>", ["4<i>mn</i> + <i>m</i> + <i>n</i>", "2<i>mn</i> + 2<i>m</i> + 2<i>n</i>", "<i>mn</i> + <i>m</i> + <i>n</i>"], "Divide 4<i>mn</i> + 2<i>m</i> + 2<i>n</i> by 2.")
    a = r.choice([1, 3, 5, 7, 9])
    b = r.choice([2, 4, 6, 8])
    if kind == "sum":
        q = "Prove that an odd number plus an even number is odd. (2<i>m</i> + %d) + (2<i>n</i> + %d) = 2(…) + 1. What goes in the bracket?" % (a, b)
        c = (a + b - 1) // 2
        right = expr_mn(1, 1, c)
        return item(q, right, [expr_mn(2, 2, c), expr_mn(1, 1, a + b), expr_mn(1, 1, c + 1)], "2<i>m</i> + 2<i>n</i> + %d = 2(%s) + 1." % (a + b, right))
    if kind == "sqodd":
        q = "Prove that the square of an odd number is odd: (2<i>n</i> + %d)² = %s = 2(…) + 1. What goes in the bracket?" % (a, poly({2: 4, 1: 4 * a, 0: a * a}, NV))
        right = poly({2: 2, 1: 2 * a, 0: (a * a - 1) // 2}, NV)
        return item(q, right, [poly({2: 4, 1: 4 * a, 0: (a * a - 1) // 2}, NV), poly({2: 2, 1: 2 * a, 0: a * a}, NV), poly({2: 2, 1: a, 0: (a * a - 1) // 2}, NV)], "Take out 2 from %s and leave the 1." % poly({2: 4, 1: 4 * a, 0: a * a - 1}, NV))
    q = "(2<i>n</i> + %d)² is the square of an even number. It equals 4(…). What goes in the bracket?" % b
    right = poly({2: 1, 1: b, 0: b * b // 4}, NV)
    return item(q, right, [poly({2: 4, 1: 4 * b, 0: b * b // 4}, NV), poly({2: 1, 1: b, 0: b * b}, NV), poly({2: 1, 1: 4 * b, 0: b * b // 4}, NV)], "(2<i>n</i> + %d)² = %s = 4(%s), so it is a multiple of 4." % (b, poly({2: 4, 1: 4 * b, 0: b * b}, NV), right))


def expr_mn(a, b, c):
    s = "%s<i>m</i> + %s<i>n</i>" % ("" if a == 1 else str(a), "" if b == 1 else str(b))
    return s + (" + %d" % c if c else "")


# =================================================================== GCSE: velocity–time graphs
VEH = ["A car", "A cyclist", "A train", "A bus", "A runner", "A lorry", "A tram", "A motorbike"]


def veh_for(r, v):
    if v <= 8:
        return r.choice(["A runner", "A cyclist"])
    if v <= 10:
        return r.choice(["A cyclist", "A bus", "A tram"])
    if v <= 15:
        return r.choice(["A bus", "A tram", "A car", "A lorry"])
    return r.choice(["A car", "A train", "A motorbike", "A lorry"])


def vt_svg(pts, tmax, vmax, tstep, vstep, dist=False):
    L, TOP, W, H = 54, 14, 300, 170
    Xp = lambda t: L + float(t) / tmax * W
    Yp = lambda v: TOP + H - float(v) / vmax * H
    s = []
    for i in range(0, int(tmax) + 1, tstep):
        s.append(line(Xp(i), Yp(0), Xp(i), Yp(vmax), "#e2e2e2", 1))
        s.append(text(Xp(i), Yp(0) + 16, num(i), 11, weight=400))
    for j in range(0, int(vmax) + 1, vstep):
        s.append(line(L, Yp(j), L + W, Yp(j), "#e2e2e2", 1))
        s.append(text(L - 6, Yp(j) + 4, num(j), 11, anchor="end", weight=400))
    s.append(line(L, Yp(0), L + W + 6, Yp(0), INK, 2))
    s.append(line(L, Yp(0), L, TOP - 4, INK, 2))
    s.append(text(L + W / 2, Yp(0) + 36, "Time (s)", 13))
    lab = "Distance (m)" if dist else "Velocity (m/s)"
    s.append("<text x='14' y='%d' font-size='12' font-weight='700' fill='%s' text-anchor='middle' transform='rotate(-90 14 %d)'>%s</text>" % (TOP + H / 2, INK, TOP + H / 2, lab))
    s.append("<polyline points='%s' fill='none' stroke='%s' stroke-width='3' stroke-linejoin='round'/>" % (" ".join("%.1f,%.1f" % (Xp(a), Yp(b)) for a, b in pts), BLUE))
    return figq(svg_wrap(L + W + 20, TOP + H + 46, "".join(s), "distance–time graph" if dist else "velocity–time graph"))


def vt_acc(r):
    v0, v1 = r.sample([0, 0, 2, 4, 5, 6, 8, 10, 12, 15, 16, 18, 20, 24], 2)
    dt = r.choice([2, 3, 4, 5, 6, 8, 10])
    a = F(v1 - v0, dt)
    if (a * 100).denominator != 1 or v0 == v1:
        return None
    veh = veh_for(r, max(v0, v1))
    q = "%s's velocity changes uniformly from %d m/s to %d m/s in %d seconds. Work out the %s." % (veh, v0, v1, dt, "acceleration" if a > 0 else "deceleration")
    right = "%s m/s²" % d(abs(float(a)), 2)
    wr = ["%s m/s²" % d(v1 / dt, 2), "%s m/s²" % d((v0 + v1) / dt, 2), "%s m/s²" % d(dt / abs(v1 - v0), 2), "%s m/s²" % d(abs(v1 - v0) * dt, 2)]
    return item(q, right, wr, "Acceleration = change in velocity ÷ time = (%d − %d) ÷ %d = %s m/s²." % (v1, v0, dt, d(float(a), 2)))


def _journey(r):
    v = r.choice([4, 5, 6, 8, 10, 12, 15, 20])
    t1, t2, t3 = r.choice([2, 4, 5, 6, 10]), r.choice([4, 5, 6, 8, 10, 15, 20]), r.choice([2, 4, 5, 10])
    T_ = t1 + t2 + t3
    if T_ > 40:
        return None
    return v, t1, t2, t3


def vt_graph_q(r):
    j = _journey(r)
    if not j:
        return None
    v, t1, t2, t3 = j
    T_ = t1 + t2 + t3
    tstep = next((st for st in (1, 2, 5, 10) if all(x % st == 0 for x in (t1, t1 + t2, T_)) and T_ // st <= 12), None)
    if not tstep:
        return None
    tmax = T_
    vstep = 5 if v % 5 == 0 and v > 10 else (2 if v % 2 == 0 else 1)
    vmax = v + vstep
    pts = [(0, 0), (t1, v), (t1 + t2, v), (T_, 0)]
    svg = vt_svg(pts, tmax, vmax, tstep, vstep)
    veh = veh_for(r, v)
    k = r.choice(["dist", "acc", "dec", "const", "avg"])
    lead = svg + "The graph shows %s's journey. " % veh.lower()
    tot = F(v * t1, 2) + v * t2 + F(v * t3, 2)
    if k == "dist":
        return item(lead + "Work out the total distance travelled.", "%s m" % n(tot), ["%s m" % n(v * T_), "%s m" % n(v * t2), "%s m" % n(tot + F(v * (t1 + t3), 2))],
                    "Area under the graph = ½ × %d × %d + %d × %d + ½ × %d × %d = <b>%s m</b>." % (t1, v, t2, v, t3, v, n(tot)))
    if k == "acc":
        return item(lead + "Work out the acceleration in the first %d seconds." % t1, "%s m/s²" % d(v / t1, 2), ["%s m/s²" % d(t1 / v, 2), "%s m/s²" % n(F(v * t1, 2)), "%s m/s²" % num(v)],
                    "Gradient = %d ÷ %d = <b>%s m/s²</b>." % (v, t1, d(v / t1, 2)))
    if k == "dec":
        return item(lead + "Work out the deceleration in the last part of the journey.", "%s m/s²" % d(v / t3, 2), ["%s m/s²" % d(t3 / v, 2), "%s m/s²" % n(F(v * t3, 2)), "%s m/s²" % d(v / T_, 2)],
                    "Gradient = %d ÷ %d = %s m/s² (the line goes down, so it is a deceleration)." % (v, t3, d(v / t3, 2)))
    if k == "const":
        return item(lead + "How far does it travel at constant speed?", "%s m" % num(v * t2), ["%s m" % num(t2), "%s m" % num(v * (t1 + t2)), "%s m" % n(F(v * t2, 2))],
                    "The flat part: %d m/s for %d s, rectangle area %d × %d = <b>%d m</b>." % (v, t2, v, t2, v * t2))
    avg = tot / T_
    if (avg * 100).denominator != 1:
        return None
    return item(lead + "Work out the average speed for the whole journey.", "%s m/s" % d(float(avg), 2), ["%s m/s" % num(v), "%s m/s" % d(v / 2, 2), "%s m/s" % d(float(tot) / (t2 or 1), 2)],
                "Average speed = total distance ÷ total time = %s ÷ %d = <b>%s m/s</b>." % (n(tot), T_, d(float(avg), 2)))


def vt_area(r):
    v0, v1 = r.sample([0, 2, 3, 4, 5, 6, 8, 10, 12, 14, 15, 20], 2)
    dt = r.choice([2, 3, 4, 5, 6, 8, 10, 12])
    veh = veh_for(r, max(v0, v1))
    s = F(v0 + v1, 2) * dt
    q = "%s's velocity changes uniformly from %d m/s to %d m/s in %d seconds. Work out the distance travelled in this time." % (veh, v0, v1, dt)
    return item(q, "%s m" % n(s), ["%s m" % num(max(v0, v1) * dt), "%s m" % n(F(abs(v1 - v0) * dt, 2)), "%s m" % num(min(v0, v1) * dt) if min(v0, v1) else "%s m" % num((v0 + v1) * dt)],
                "Area of the trapezium = ½ × (%d + %d) × %d = <b>%s m</b>." % (v0, v1, dt, n(s)))


def vt_dt(r):
    k = r.choice(["speed", "speed", "stop", "avg"])
    veh = r.choice(VEH)
    if k == "speed":
        dd = r.choice([100, 120, 150, 200, 240, 300, 400, 450, 500, 600])
        tt = r.choice([10, 15, 20, 25, 30, 40, 50, 60])
        sp = F(dd, tt)
        if (sp * 100).denominator != 1:
            return None
        pts = [(0, 0), (tt, dd)]
        tst = 10 if tt % 10 == 0 else 5
        tm = tt + tst
        ds = 100 if dd % 100 == 0 and dd > 300 else 50
        svg = vt_svg(pts, tm, dd + ds, tst, ds, dist=True)
        veh = veh_for(r, sp)
        return item(svg + "The distance–time graph shows %s moving at a constant speed. Work out the speed." % veh.lower(), "%s m/s" % d(float(sp), 2),
                    ["%s m/s" % d(tt / dd, 3), "%s m/s" % num(dd * tt), "%s m/s" % num(dd)], "Speed = gradient = %d ÷ %d = <b>%s m/s</b>." % (dd, tt, d(float(sp), 2)))
    if k == "stop":
        a, b = r.choice([(10, 20), (20, 30), (10, 25), (15, 30), (20, 40), (30, 40)])
        return item("On a distance–time graph, %s's line is horizontal from %d s to %d s. What is happening?" % (veh.lower(), a, b), "it is stationary (not moving)",
                    ["it is moving at a constant speed", "it is accelerating", "it is travelling back to the start"], "A horizontal line means the distance is not changing, so the speed is 0.")
    d1, t1, t2, d2, t3 = r.choice([200, 300, 400, 500]), r.choice([20, 25, 40, 50]), r.choice([10, 20, 30]), r.choice([100, 200, 300]), r.choice([20, 30, 50])
    avg = F(d1 + d2, t1 + t2 + t3)
    if (avg * 100).denominator != 1:
        return None
    return item("%s travels %d m in %d s, stops for %d s, then travels %d m in %d s. Work out the average speed for the whole journey." % (veh, d1, t1, t2, d2, t3), "%s m/s" % d(float(avg), 2),
                ["%s m/s" % d((d1 + d2) / (t1 + t3), 2), "%s m/s" % d((d1 / t1 + d2 / t3) / 2, 2), "%s m/s" % d((t1 + t2 + t3) / (d1 + d2), 3)],
                "Average speed = total distance ÷ total time = %d ÷ %d = <b>%s m/s</b>. Include the time spent stopped." % (d1 + d2, t1 + t2 + t3, d(float(avg), 2)))


def vt_trap(r):
    kind = r.choice(["sq", "sq", "root"])
    k = r.choice([1, 2, 3, 4, 5])
    h = r.choice([1, 2])
    nst = r.choice([3, 4])
    ts = [i * h for i in range(nst + 1)]
    if kind == "sq":
        vs = [F(k * t * t, 2) if k % 2 else F(k * t * t, 2) for t in ts]
        vs = [k * t * t for t in ts] if h == 1 else [F(k * t * t, 4) for t in ts]
    else:
        vs = [k * 6 * F(t, h) for t in ts]
        vs = [round(k * 6 * math.sqrt(t / (h * nst)), 1) for t in ts]
        vs = [F(str(v)) for v in vs]
    if any((v * 10).denominator != 1 for v in vs):
        return None
    tb = table(["Time (s)"] + [num(t) for t in ts], [["Velocity (m/s)"] + [d(float(v), 1) for v in vs]])
    est = F(h, 2) * (vs[0] + vs[-1] + 2 * sum(vs[1:-1]))
    if r.random() < 0.6:
        q = tb + "The velocity of a particle is shown in the table. Use %d trapezia to estimate the distance travelled in the first %d seconds." % (nst, ts[-1])
        return item(q, "%s m" % d(float(est), 2), ["%s m" % d(float(h * (vs[0] + vs[-1] + 2 * sum(vs[1:-1]))), 2), "%s m" % d(float(h * sum(vs[1:])), 2), "%s m" % d(float(vs[-1] * ts[-1]), 2)],
                    "Area ≈ ½ × %d × [%s + %s + 2(%s)] = <b>%s m</b>." % (h, d(float(vs[0]), 1), d(float(vs[-1]), 1), " + ".join(d(float(v), 1) for v in vs[1:-1]), d(float(est), 2)))
    shape = "curves upwards (it gets steeper)" if kind == "sq" else "curves downwards (it gets less steep)"
    right = "an overestimate" if kind == "sq" else "an underestimate"
    q = tb + "The velocity–time graph for these values %s. Is a trapezium estimate of the distance an overestimate or an underestimate?" % shape
    return item(q, right, ["an underestimate" if kind == "sq" else "an overestimate", "exact", "you cannot tell"],
                "The straight tops of the trapezia are %s the curve, so the estimate is %s." % ("above" if kind == "sq" else "below", right))


# =================================================================== GCSE: equation of a circle (centre the origin)
PTS = {}
for _x in range(-24, 25):
    for _y in range(-24, 25):
        if _x and _y:
            PTS.setdefault(_x * _x + _y * _y, []).append((_x, _y))
R2 = sorted(k for k, v in PTS.items() if len(v) >= 8 and k <= 100)


def rad(r2):
    s = math.isqrt(r2)
    if s * s == r2:
        return num(s)
    k = max(i for i in range(1, s + 1) if r2 % (i * i) == 0)
    return ("%d√%d" % (k, r2 // (k * k))) if k > 1 else "√%d" % r2


def circ(r2):
    return "%s² + %s² = %d" % (X, Y, r2)


def c_basic(r):
    k = r.choice(["rad", "rad", "eq", "axis", "in", "in"])
    rr = r.choice(range(2, 16))
    if k == "in":
        r2 = r.choice([25, 36, 49, 50, 64, 81, 100, 20, 40, 65])
        a, b = r.randint(-9, 9), r.randint(-9, 9)
        s_ = a * a + b * b
        right = "inside the circle" if s_ < r2 else ("on the circle" if s_ == r2 else "outside the circle")
        return item("Is the point (%s, %s) inside, on or outside the circle %s?" % (n(a), n(b), circ(r2)), right,
                    [x for x in ("inside the circle", "on the circle", "outside the circle") if x != right] + ["at the centre of the circle"],
                    "%s² + %s² = %d, which is %s %d." % (par_(a), par_(b), s_, "less than" if s_ < r2 else ("equal to" if s_ == r2 else "more than"), r2))
    if k == "rad":
        r2 = r.choice([x * x for x in range(2, 16)] + [8, 12, 18, 20, 27, 32, 45, 50, 75, 80, 98])
        return item("What is the radius of the circle %s?" % circ(r2), rad(r2), [num(r2), n(F(r2, 2)), rad(r2 * 4) if r2 * 4 != r2 else "1"],
                    "%s² + %s² = <i>r</i>², so <i>r</i> = √%d = <b>%s</b>." % (X, Y, r2, rad(r2)))
    if k == "eq":
        return item("Write down the equation of the circle with centre (0, 0) and radius %d." % rr, circ(rr * rr), [circ(rr), circ(2 * rr), "%s + %s = %d" % (X, Y, rr * rr)],
                    "The equation is %s² + %s² = <i>r</i>² = %d² = <b>%d</b>." % (X, Y, rr, rr * rr))
    return item("Where does the circle %s cross the positive %s-axis?" % (circ(rr * rr), X), "(%d, 0)" % rr, ["(%d, 0)" % (rr * rr), "(0, %d)" % rr, "(%s, 0)" % n(F(rr * rr, 2))],
                "On the %s-axis, %s = 0, so %s² = %d and %s = %d." % (X, Y, X, rr * rr, X, rr))


def c_on(r):
    r2 = r.choice(R2 + [25, 100, 169])
    pts = PTS.get(r2) or [(3, 4)]
    if r2 in (25, 100, 169):
        pts = [p for p in PTS.get(r2, []) if p[0] and p[1]]
    if not pts:
        return None
    p = r.choice(pts)
    k = r.choice(["which", "missing"])
    if k == "which":
        bad = [(p[0] + 1, p[1]), (p[1] + 1, p[0]), (p[0], p[1] - 1), (abs(p[0]) + abs(p[1]), 0)]
        bad = [b for b in bad if b[0] * b[0] + b[1] * b[1] != r2]
        f = lambda t: "(%s, %s)" % (n(t[0]), n(t[1]))
        return item("Which point lies on the circle %s?" % circ(r2), f(p), [f(b) for b in bad], "Check %s² + %s²: (%s)² + (%s)² = %d. ✓" % (X, Y, n(p[0]), n(p[1]), r2))
    xv, yv = p
    if yv < 0:
        return None
    return item("The point (%s, <i>k</i>) lies on the circle %s and <i>k</i> &gt; 0. Find <i>k</i>." % (n(xv), circ(r2)), num(yv), [num(r2 - xv * xv), num(abs(xv)) if abs(xv) != yv else num(yv + 1), rad(r2)],
                "%s² + <i>k</i>² = %d, so <i>k</i>² = %d and <i>k</i> = <b>%d</b>." % (par_(xv), r2, r2 - xv * xv, yv))


def par_(v):
    return "(%s)" % n(v) if v < 0 else n(v)


def c_grad(r):
    r2 = r.choice(R2 + [25, 100])
    p = r.choice(PTS[r2])
    xv, yv = p
    kind = r.choice(["radius", "tangent", "tangent"])
    m = F(yv, xv)
    mt = F(-xv, yv)
    if kind == "radius":
        return item("The point P(%s, %s) is on the circle %s. Find the gradient of the radius OP." % (n(xv), n(yv), circ(r2)), n(m), [n(F(xv, yv)), n(mt), n(-m)],
                    "Gradient = change in %s ÷ change in %s = %s ÷ %s = <b>%s</b>." % (Y, X, n(yv), n(xv), n(m)))
    return item("The point P(%s, %s) is on the circle %s. Find the gradient of the tangent at P." % (n(xv), n(yv), circ(r2)), n(mt), [n(m), n(-m) if -m != mt else n(F(xv, yv)), n(F(xv, yv)) if F(xv, yv) != mt else n(-mt)],
                "Gradient of OP = %s. The tangent is perpendicular, so its gradient is −1 ÷ %s = <b>%s</b>." % (n(m), n(m), n(mt)))


def c_tangent(r):
    r2 = r.choice(R2 + [25, 100, 169])
    p = r.choice([q for q in PTS[r2] if q[0] and q[1]])
    xv, yv = p
    kind = r.choice(["std", "std", "yint"])

    def lin(a, b, c):
        return "%s = %s" % (poly({1: a}, X) + (" + " if b > 0 else " − ") + (coef(abs(b)) + Y), num(c)) if a else None
    if kind == "std":
        g = math.gcd(math.gcd(abs(xv), abs(yv)), r2) * (1 if xv > 0 else -1)
        a_, b_, c_ = xv // g, yv // g, r2 // g
        right = lin(a_, b_, c_)
        wr = [lin(b_, a_, c_) if b_ > 0 else lin(-b_, -a_, c_), lin(a_, -b_, c_), lin(a_, b_, -c_)]
        wr = [w for w in wr if w and w != right]
        return item("Find the equation of the tangent to the circle %s at the point (%s, %s)." % (circ(r2), n(xv), n(yv)), right, wr,
                    "Gradient of the radius = %s, so the tangent gradient = %s. <i>y</i> − %s = %s(<i>x</i> − %s) rearranges to %s%s %s %s%s = %d, which simplifies to <b>%s</b>." % (
                        n(F(yv, xv)), n(F(-xv, yv)), par_(yv), n(F(-xv, yv)), par_(xv), coef(xv), X, "+" if yv > 0 else "−", coef(abs(yv)), Y, r2, right))
    c = F(r2, yv)
    return item("The tangent to the circle %s at (%s, %s) crosses the %s-axis at (0, <i>c</i>). Find <i>c</i>." % (circ(r2), n(xv), n(yv), Y), n(c), [n(F(r2, xv)), n(F(-r2, yv)), n(yv)],
                "Tangent: %s%s %s %s%s = %d. Put %s = 0: <i>c</i> = %d ÷ %s = <b>%s</b>." % (coef(xv), X, "+" if yv > 0 else "−", coef(abs(yv)), Y, r2, X, r2, par_(yv), n(c)))


def c_line(r):
    rr = r.choice([5, 10, 13, 15, 17, 25])
    r2 = rr * rr
    p = [q for q in PTS.get(r2, []) if q[0] > 0 and q[1] > 0]
    if not p:
        return None
    xv, yv = r.choice(p)
    k = r.choice(["vert", "horiz"])
    if k == "vert":
        return item("The line %s = %d meets the circle %s at two points. Find their coordinates." % (X, xv, circ(r2)), "(%d, %d) and (%d, %s)" % (xv, yv, xv, n(-yv)),
                    ["(%d, %d) and (%s, %d)" % (xv, yv, n(-xv), yv), "(%d, %d) only" % (xv, yv), "(%d, %d) and (%d, %s)" % (xv, r2 - xv * xv, xv, n(-(r2 - xv * xv)))],
                    "%d² + %s² = %d, so %s² = %d and %s = ±%d." % (xv, Y, r2, Y, yv * yv, Y, yv))
    return item("The line %s = %d meets the circle %s at two points. Find their coordinates." % (Y, yv, circ(r2)), "(%d, %d) and (%s, %d)" % (xv, yv, n(-xv), yv),
                ["(%d, %d) and (%d, %s)" % (xv, yv, xv, n(-yv)), "(%d, %d) only" % (xv, yv), "(%d, %d) and (%s, %d)" % (r2 - yv * yv, yv, n(-(r2 - yv * yv)), yv)],
                "%s² + %d² = %d, so %s² = %d and %s = ±%d." % (X, yv, r2, X, xv * xv, X, xv))


# =================================================================== A level: proof
def pr_deduct(r):
    kind = r.choice(["cube", "odd8", "sum_sq", "diff", "mult"])
    if kind == "cube":
        return item("Which factorisation shows that <i>n</i>³ − <i>n</i> is the product of three consecutive integers?", "(<i>n</i> − 1)<i>n</i>(<i>n</i> + 1)",
                    ["<i>n</i>(<i>n</i> + 1)(<i>n</i> + 2)", "<i>n</i>(<i>n</i> − 1)²", "<i>n</i>(<i>n</i>² + 1)"], "<i>n</i>³ − <i>n</i> = <i>n</i>(<i>n</i>² − 1) = (<i>n</i> − 1)<i>n</i>(<i>n</i> + 1).") if r.random() < 0.2 else None
    if kind == "odd8":
        a = r.choice([1, 3, 5, 7])
        e = poly({2: 4, 1: 4 * a, 0: a * a - 1}, NV)
        return item("(2<i>n</i> + %d)² − 1 = %s. Which form shows that it is always a multiple of 8?" % (a, e), "4(<i>n</i> + %s)(<i>n</i> + %s)" % (n(F(a - 1, 2)), n(F(a + 1, 2))) if a > 1 else "4<i>n</i>(<i>n</i> + 1)",
                    ["4(%s)" % poly({2: 1, 1: a, 0: F(a * a - 1, 4)}, NV) if a > 1 else "4(<i>n</i>² + 1)", "8(%s)" % poly({2: 1, 1: a, 0: 1}, NV), "2(%s)" % poly({2: 2, 1: 2 * a, 0: F(a * a - 1, 2)}, NV)],
                    "It is 4 × the product of two consecutive integers; one of them is even, so it is 4 × 2 × an integer = a multiple of 8.")
    if kind == "sum_sq":
        a = r.randint(1, 6)
        e = poly({2: 2, 1: 2 * a, 0: a * a}, NV)
        return item("The sum of the squares of <i>n</i> and <i>n</i> + %d is %s. Why is it %s for every integer <i>n</i>?" % (a, e, "odd" if a % 2 else "even"),
                    "%s is even and %d is %s" % (poly({2: 2, 1: 2 * a}, NV), a * a, "odd" if a % 2 else "even"),
                    ["%s is even and %d is %s" % (poly({2: 2, 1: 2 * a}, NV), a * a, "even" if a % 2 else "odd"), "every square number is %s" % ("odd" if a % 2 else "even"), "it is true for <i>n</i> = 1, so it is always true"],
                    "2<i>n</i>² + %d<i>n</i> = 2(<i>n</i>² + %d<i>n</i>) is even, and adding %d makes it %s." % (2 * a, a, a * a, "odd" if a % 2 else "even"))
    if kind == "diff":
        a, b = r.sample(range(1, 10), 2)
        if (a + b) % 2:
            return None
        e = poly({1: 2 * (a - b), 0: a * a - b * b}, NV)
        g = math.gcd(2 * abs(a - b), abs(a * a - b * b))
        return item("Simplify (<i>n</i> + %d)² − (<i>n</i> + %d)² and find the largest number that always divides it." % (a, b), "%s = %d(%s), so %d" % (e, g, poly({1: F(2 * (a - b), g), 0: F(a * a - b * b, g)}, NV), g),
                    ["%s = %d(%s), so %d" % (e, 2, poly({1: a - b, 0: F(a * a - b * b, 2)}, NV), 2) if g != 2 else "%s, so 1" % e,
                     "%s, so %d" % (poly({1: 2 * (a + b), 0: a * a - b * b}, NV), abs(a * a - b * b)), "%s, so %d" % (e, 2 * g)],
                    "Expanding: %s = %d(%s)." % (e, g, poly({1: F(2 * (a - b), g), 0: F(a * a - b * b, g)}, NV)))
    k = r.choice([3, 5, 7])
    a = r.randint(1, 4)
    K = "<i>k</i>"
    return item("<i>n</i> is a multiple of %d, so <i>n</i> = %d<i>k</i>. Which expression shows that <i>n</i>² + %d<i>n</i> is a multiple of %d?" % (k, k, a * k, k * k),
                "%d(%s)" % (k * k, poly({2: 1, 1: a}, K)), ["%d(%s)" % (k, poly({2: 1, 1: a * k}, K)), "%d(%s)" % (k * k, poly({2: 1, 1: a * k}, K)), "%d(%s)" % (k * k, poly({2: a, 1: 1}, K))],
                "(%d<i>k</i>)² + %d(%d<i>k</i>) = %s = %d(%s)." % (k, a * k, k, poly({2: k * k, 1: a * k * k}, K), k * k, poly({2: 1, 1: a}, K)))


def _res(p, m):
    return sorted(set(pow(i, p, m) for i in range(m)))


def pr_exhaust(r):
    p, m = r.choice([(2, m) for m in range(3, 13)] + [(3, m) for m in (4, 7, 9)] + [(4, m) for m in (3, 5, 8, 16)])
    rs = _res(p, m)
    word = {2: "square number", 3: "cube number", 4: "fourth power"}[p]
    k = r.choice(["set", "imp"])
    if k == "set":
        right = ", ".join(str(x) for x in rs)
        alt = [sorted(set(rs) | {max(set(range(m)) - set(rs))}) if set(range(m)) - set(rs) else rs + [m],
               sorted(set(range(0, m, 2)) | {1}) , list(range(min(m, len(rs) + 1)))]
        wr = [", ".join(str(x) for x in a) for a in alt]
        return item("By considering every remainder, find all the possible remainders when a %s number is divided by %d." % (word, m), right, wr + [", ".join(str(x) for x in range(m))],
                    "Check %s = 0, 1, …, %d: %s%s leaves %s." % (NV, m - 1, NV, SUPS[p], right))
    bad = [x for x in range(m) if x not in rs]
    if not bad:
        return None
    right = num(r.choice(bad))
    return item("Which of these can never be the remainder when a %s number is divided by %d?" % (word, m), right, [num(x) for x in r.sample(rs, min(3, len(rs)))] + [num(x) for x in rs],
                "The only possible remainders are %s, so %s is impossible." % (", ".join(str(x) for x in rs), right))


def pr_counter(r):
    kind = r.choice(["poly", "pow", "abs", "sq", "div"])
    if kind == "poly":
        c = r.choice([11, 17, 41])
        cand = [k for k in range(1, c + 1) if any((k * k + k + c) % pr == 0 for pr in range(2, int((k * k + k + c) ** 0.5) + 1))]
        right = cand[0]
        good = [k for k in range(1, 12) if k not in cand]
        return item("Disprove: “<i>n</i>² + <i>n</i> + %d is prime for every positive integer <i>n</i>.” Which value of <i>n</i> is a counterexample?" % c, num(right),
                    [num(x) for x in r.sample(good, 3)], "%d² + %d + %d = %d, which is not prime." % (right, right, c, right * right + right + c))
    if kind == "pow":
        a = r.choice([2, 3])
        good = [k for k in range(1, 7) if all((a ** k + 1) % pr for pr in range(2, int((a ** k + 1) ** 0.5) + 1))] if a == 2 else []
        if a == 2:
            return item("Disprove: “2<sup><i>n</i></sup> + 1 is prime for every positive integer <i>n</i>.” Which value of <i>n</i> is a counterexample?", "3", [num(x) for x in good[:3]],
                        "2³ + 1 = 9 = 3 × 3, which is not prime.")
        return item("Disprove: “2<sup><i>n</i></sup> − 1 is prime for every prime <i>n</i>.” Which value of <i>n</i> is a counterexample?", "11", ["2", "3", "5"], "2<sup>11</sup> − 1 = 2047 = 23 × 89.") if r.random() < 0.3 else None
    if kind == "abs":
        a, b = r.randint(1, 9), r.randint(1, 9)
        return item("Disprove: “|<i>a</i> + <i>b</i>| = |<i>a</i>| + |<i>b</i>| for all real <i>a</i> and <i>b</i>.” Which pair is a counterexample?", "<i>a</i> = %d, <i>b</i> = %s" % (a, n(-b)),
                    ["<i>a</i> = %d, <i>b</i> = %d" % (a, b), "<i>a</i> = %s, <i>b</i> = %s" % (n(-a), n(-b)), "<i>a</i> = 0, <i>b</i> = %s" % n(-b)],
                    "|%d + (%s)| = %d but |%d| + |%s| = %d." % (a, n(-b), abs(a - b), a, n(-b), a + b))
    if kind == "sq":
        a = r.randint(2, 9)
        b = r.randint(1, a - 1)
        return item("Disprove: “If <i>x</i>² &gt; <i>y</i>² then <i>x</i> &gt; <i>y</i>.” Which pair is a counterexample?", "<i>x</i> = %s, <i>y</i> = %d" % (n(-a), b),
                    ["<i>x</i> = %d, <i>y</i> = %d" % (a, b), "<i>x</i> = %d, <i>y</i> = %s" % (a, n(-b)), "<i>x</i> = %d, <i>y</i> = 0" % a],
                    "(%s)² = %d &gt; %d² = %d, but %s is not greater than %d." % (n(-a), a * a, b, b * b, n(-a), b))
    a = r.choice([4, 6, 8, 9, 10, 12])
    f = [x for x in range(2, a) if a % x == 0]
    ps = [(x, a // x) for x in range(2, a) if a % x == 0 and x <= a // x]
    p1, p2 = r.choice(ps)
    return item("Disprove: “If %d divides <i>ab</i>, then %d divides <i>a</i> or %d divides <i>b</i>.” Which pair is a counterexample?" % (a, a, a), "<i>a</i> = %d, <i>b</i> = %d" % (p1, p2),
                ["<i>a</i> = %d, <i>b</i> = 1" % a, "<i>a</i> = %d, <i>b</i> = %d" % (a, a), "<i>a</i> = 1, <i>b</i> = %d" % (2 * a)],
                "%d × %d = %d is divisible by %d, but neither %d nor %d is." % (p1, p2, p1 * p2, a, p1, p2))


def pr_square(r):
    b = r.choice([-10, -8, -6, -4, -2, 2, 4, 6, 8, 10])
    c = r.randint(b * b // 4 + 1, b * b // 4 + 12)
    h, k = F(b, 2), c - F(b * b, 4)
    e = poly({2: 1, 1: b, 0: c})
    kind = r.choice(["form", "min", "why"])
    form = "(%s)² + %s" % (poly({1: 1, 0: h}), n(k))
    if kind == "form":
        return item("Write %s in the form (%s + <i>p</i>)² + <i>q</i>." % (e, X), form, ["(%s)² + %s" % (poly({1: 1, 0: -h}), n(k)), "(%s)² + %s" % (poly({1: 1, 0: h}), n(c)), "(%s)² + %s" % (poly({1: 1, 0: b}), n(c - b * b))],
                    "Halve %s to get %s, then %d − %s = %s." % (n(b), n(h), c, n(h * h), n(k)))
    if kind == "min":
        return item("%s = %s. What is the least value of %s for real %s?" % (e, form, e, X), n(k), [n(c), n(-k), n(h)], "(%s)² ≥ 0, so the least value is %s, when %s = %s." % (poly({1: 1, 0: h}), n(k), X, n(-h)))
    return item("Which statement proves that %s &gt; 0 for every real %s?" % (e, X), "%s = %s, and a square is never negative, so it is at least %s" % (e, form, n(k)),
                ["it is positive when %s = 0, 1 and 2" % X, "%s = %s, and %s is positive" % (e, form, n(c)), "its discriminant %s is positive" % n(b * b - 4 * c)],
                "Completing the square gives (%s)² + %s, which is always at least %s &gt; 0." % (poly({1: 1, 0: h}), n(k), n(k)))


def pr_contra(r):
    kind = r.choice(["irr", "irr", "even", "inf", "rat", "big"])
    if kind == "irr":
        p = r.choice([2, 3, 5, 6, 7, 10, 11, 13, 14, 15, 17, 19, 21, 22, 23])
        if r.random() < 0.3:
            p = r.choice([2, 3, 4, 5, 6, 7, 9, 10])
            return item("You want to prove by contradiction that ∛%d is irrational. What is the first line?" % p, "Assume ∛%d = <i>a</i>/<i>b</i>, where <i>a</i> and <i>b</i> are integers with no common factor" % p,
                        ["Assume ∛%d is irrational" % p, "Assume ∛%d = <i>a</i>/<i>b</i>, where <i>a</i> and <i>b</i> are any real numbers" % p, "Assume ∛%d is an integer" % p],
                        "Assume the opposite: ∛%d is rational, written in its lowest terms. Then %d<i>b</i>³ = <i>a</i>³." % (p, p))
        return item("You want to prove by contradiction that √%d is irrational. What is the first line?" % p, "Assume √%d = <i>a</i>/<i>b</i>, where <i>a</i> and <i>b</i> are integers with no common factor" % p,
                    ["Assume √%d is irrational" % p, "Assume √%d = <i>a</i>/<i>b</i>, where <i>a</i> and <i>b</i> are any real numbers" % p, "Assume √%d is an integer" % p],
                    "Assume the opposite of what you want to prove: √%d is rational, written in its lowest terms." % p)
    if kind == "even":
        p = r.choice([2, 3, 5, 7])
        w = "even" if p == 2 else "a multiple of %d" % p
        nw = "odd" if p == 2 else "not a multiple of %d" % p
        return item("Prove by contradiction: “If <i>n</i>² is %s, then <i>n</i> is %s.” What do you assume?" % (w, w), "<i>n</i>² is %s and <i>n</i> is %s" % (w, nw),
                    ["<i>n</i>² is %s and <i>n</i> is %s" % (nw, w), "<i>n</i>² is %s and <i>n</i> is %s" % (w, w), "<i>n</i> is %s" % w],
                    "Keep the condition and assume the conclusion is false.")
    if kind == "inf":
        return item("Euclid proved by contradiction that there are infinitely many prime numbers. What did he assume?", "There are only finitely many primes, <i>p</i>₁, <i>p</i>₂, …, <i>p</i><sub><i>n</i></sub>",
                    ["There are infinitely many primes", "Every number is prime", "The largest prime is 97"], "Assume finitely many, multiply them all and add 1 to get a contradiction.") if r.random() < 0.15 else None
    if kind == "rat":
        p = r.choice([2, 3, 5, 7])
        return item("Prove by contradiction that a rational number plus an irrational number is irrational. What do you assume?", "<i>a</i> is rational, <i>b</i> is irrational and <i>a</i> + <i>b</i> is rational",
                    ["<i>a</i> is rational, <i>b</i> is irrational and <i>a</i> + <i>b</i> is irrational", "<i>a</i> and <i>b</i> are both rational", "<i>a</i> + <i>b</i> = √%d" % p], "Then <i>b</i> = (<i>a</i> + <i>b</i>) − <i>a</i> would be rational: a contradiction.") if r.random() < 0.2 else None
    w = r.choice(["even number", "multiple of 3", "multiple of 5", "odd number", "square number", "integer"])
    return item("Prove by contradiction that there is no greatest %s. What do you assume?" % w, "There is a greatest %s, <i>N</i>" % w,
                ["There is no greatest %s" % w, "Every %s is less than 100" % w, "<i>N</i> is the smallest %s" % w], "Then find a bigger one from <i>N</i> to get a contradiction.")


# =================================================================== A level: product and quotient rules
def e_(k, v=X):
    return "e<sup>%s%s</sup>" % (coef(k), v)


def trg(f, k):
    return "%s %s%s" % (f, coef(k), X) if k != 1 else "%s %s" % (f, X)


def lin_(a, b):
    """(ax + b) with b first written when a < 0: (2 − x)"""
    if a < 0 and b > 0:
        return "(%s − %s%s)" % (n(b), coef(-a), X)
    return "(%s)" % poly({1: a, 0: b})


def pq_prod(r):
    it = _pq_prod(r)
    if it:
        import re as _re
        for k_ in ("q", "e"):
            it[k_] = _re.sub(r"(\d)(cos|sin) ", r"\1 \2 ", it[k_])
        it["c"] = [_re.sub(r"(\d)(cos|sin) ", r"\1 \2 ", c_) for c_ in it["c"]]
    return it


def _pq_prod(r):
    kind = r.choice(["exp", "exp", "ln", "sin", "cos", "expsin"])
    if kind == "exp":
        m, k = r.randint(1, 4), r.choice([-3, -2, -1, 1, 2, 3])
        g = math.gcd(m, abs(k))
        y = xp(m) + e_(k)
        pre = (n(g) if g > 1 else "") + xp(m - 1) + e_(k)
        right = pre + lin_(k // g, m // g)
        wr = [coef(m) + xp(m - 1) + e_(k) if m > 1 else e_(k), coef(k) + xp(m) + e_(k), coef(m * k) + xp(m - 1) + e_(k) if m > 1 else coef(k) + e_(k), pre + lin_(k // g, -(m // g))]
        return item("Differentiate <i>y</i> = %s." % y, right, wr, "Product rule: <i>u</i> = %s, <i>v</i> = %s. d<i>y</i>/d<i>x</i> = <i>u</i>′<i>v</i> + <i>uv</i>′ = %s%s + %s%s, then factorise." % (xp(m), e_(k), coef(m) + xp(m - 1), e_(k), coef(k) + xp(m), e_(k)))
    if kind == "ln":
        a, m = r.randint(1, 5), r.randint(1, 4)
        y = coef(a) + xp(m) + " ln " + X
        pre = coef(a) + xp(m - 1)
        inner = "(%s ln %s + 1)" % (coef(m) or "", X) if m > 1 else "(ln %s + 1)" % X
        right = (pre + inner) if pre else inner[1:-1]
        wr = [coef(a * m) + xp(m - 1) + " ln " + X if m > 1 else coef(a) + "ln " + X, (coef(a) + xp(m - 1)) or n(a) if m > 1 else n(a), coef(a * m) + xp(m - 2) if m > 2 else (coef(a * m) + X if m == 2 else "%s/%s" % (n(a), X)),
              (pre + "(%s ln %s − 1)" % (coef(m) or "", X)) if pre else "ln %s − 1" % X]
        return item("Differentiate <i>y</i> = %s." % y, right, wr, "<i>u</i> = %s, <i>v</i> = ln %s, <i>v</i>′ = 1/%s. d<i>y</i>/d<i>x</i> = %s ln %s + %s." % (coef(a) + xp(m) or n(a), X, X, coef(a * m) + xp(m - 1) or n(a * m), X, coef(a) + xp(m - 1) or n(a)))
    if kind in ("sin", "cos"):
        m, k = r.randint(1, 3), r.randint(1, 4)
        f1, f2 = ("sin", "cos") if kind == "sin" else ("cos", "sin")
        sg = "+" if kind == "sin" else "−"
        y = xp(m) + " " + trg(f1, k)
        t1 = (coef(m) + xp(m - 1) + " " + trg(f1, k)) if m > 1 else trg(f1, k)
        t2 = coef(k) + xp(m) + " " + trg(f2, k)
        right = "%s %s %s" % (t1, sg, t2)
        wr = ["%s %s %s" % (t1, "−" if sg == "+" else "+", t2), "%s %s %s" % (t1, sg, xp(m) + " " + trg(f2, k)) if k > 1 else "%s %s %s" % (t1, sg, coef(2) + xp(m) + " " + trg(f2, k)),
              ("%s" % (coef(m * k) + xp(m - 1) + " " + trg(f2, k))) if m > 1 else coef(k) + trg(f2, k).replace(f2 + " ", f2 + " ", 1), "%s %s %s" % (t1.replace(f1, f2), sg, t2.replace(f2, f1))]
        return item("Differentiate <i>y</i> = %s." % y, right, wr, "<i>u</i> = %s, <i>v</i> = %s, <i>v</i>′ = %s%s. Use <i>u</i>′<i>v</i> + <i>uv</i>′." % (xp(m), trg(f1, k), "" if kind == "sin" else MINUS, (coef(k) + " " if k > 1 else "") + trg(f2, k)))
    a, b = r.randint(1, 4), r.randint(1, 4)
    y = e_(a) + " " + trg("sin", b)
    right = e_(a) + "(%s %s + %s)" % (coef(a) or "", trg("sin", b), coef(b) + trg("cos", b)) if a > 1 else e_(a) + "(%s + %s)" % (trg("sin", b), coef(b) + trg("cos", b))
    right = right.replace("( ", "(")
    wr = [e_(a) + "(%s − %s)" % ((coef(a) + " " if a > 1 else "") + trg("sin", b), coef(b) + trg("cos", b)), coef(a * b) + e_(a) + " " + trg("cos", b),
          e_(a) + "(%s + %s)" % ((coef(b) + " " if b > 1 else "") + trg("sin", b), coef(a) + trg("cos", b)) if a != b else e_(a) + "(%s + %s)" % (trg("sin", b), trg("cos", b))]
    wr = [w.replace("  ", " ") for w in wr]
    right = right.replace("  ", " ")
    return item("Differentiate <i>y</i> = %s." % y, right, wr, "<i>u</i> = %s, <i>v</i> = %s. <i>u</i>′<i>v</i> + <i>uv</i>′ = %s%s %s + %s%s %s." % (e_(a), trg("sin", b), coef(a), e_(a), trg("sin", b), coef(b), e_(a), trg("cos", b)))


def pq_num(r):
    a, b, c, dd = r.randint(1, 3), r.randint(-4, 4), r.randint(1, 2), r.randint(-4, 4)
    k = r.choice([2, 3, 4])
    v = r.choice([-1, 0, 1, 2])
    if dd == 0 or b == 0:
        return None
    w = c * v + dd
    g = a * w ** k + (a * v + b) * k * c * w ** (k - 1)
    y = "(%s)(%s)%s" % (poly({1: a, 0: b}), poly({1: c, 0: dd}), SUPS[k])
    return item("Find the gradient of <i>y</i> = %s at the point where %s = %s." % (y, X, n(v)), n(g), [n(a * w ** k), n((a * v + b) * k * c * w ** (k - 1)), n(a * k * c * w ** (k - 1))],
                "<i>u</i> = %s, <i>v</i> = (%s)%s. d<i>y</i>/d<i>x</i> = %d(%s)%s + (%s) × %d(%s)%s. At %s = %s: %s + %s = <b>%s</b>." % (
                    poly({1: a, 0: b}), poly({1: c, 0: dd}), SUPS[k], a, poly({1: c, 0: dd}), SUPS[k], poly({1: a, 0: b}), k * c, poly({1: c, 0: dd}), SUPS.get(k - 1, ""), X, n(v), n(a * w ** k), n((a * v + b) * k * c * w ** (k - 1)), n(g)))


def pq_quot(r):
    kind = r.choice(["lin", "lin", "exp", "ln", "pow"])
    if kind == "lin":
        a, b, c, dd = r.randint(1, 5), r.randint(-6, 6), r.randint(1, 4), r.randint(-6, 6)
        N = a * dd - b * c
        if N == 0 or dd == 0:
            return None
        den = "(%s)²" % poly({1: c, 0: dd})
        return item("Differentiate <i>y</i> = (%s)/(%s)." % (poly({1: a, 0: b}), poly({1: c, 0: dd})), "%s/%s" % (n(N), den), ["%s/%s" % (n(-N), den), "%s/(%s)" % (n(N), poly({1: c, 0: dd})), "%s/%s" % (n(a * dd + b * c), den) if a * dd + b * c not in (N, -N) else n(F(a, c))],
                    "Quotient rule: (<i>vu</i>′ − <i>uv</i>′)/<i>v</i>² = [%d(%s) − %d(%s)]/%s = <b>%s/%s</b>." % (a, poly({1: c, 0: dd}), c, poly({1: a, 0: b}), den, n(N), den))
    if kind == "exp":
        m, k = r.randint(1, 3), r.randint(1, 3)
        right = "%s(%s%s − %d)/%s" % (e_(k), coef(k), X, m, xp(m + 1))
        return item("Differentiate <i>y</i> = %s/%s." % (e_(k), xp(m)), right, ["%s(%s%s + %d)/%s" % (e_(k), coef(k), X, m, xp(m + 1)), "%s(%s%s − %d)/%s" % (e_(k), coef(k), X, m, xp(2 * m)) if m > 1 else "%s(%s%s − 1)/%s" % (e_(k), coef(k), X, X),
                                                                  "%s/(%s)" % (coef(k) + e_(k), coef(m) + xp(m - 1) if m > 1 else n(1)), "%s(%d − %s%s)/%s" % (e_(k), m, coef(k), X, xp(m + 1))],
                    "<i>u</i> = %s, <i>v</i> = %s: (%s × %s%s − %s × %s%s)/%s, then cancel %s." % (e_(k), xp(m), xp(m), coef(k), e_(k), e_(k), coef(m), xp(m - 1), xp(2 * m), xp(m - 1) or "nothing"))
    if kind == "ln":
        m = r.randint(1, 4)
        right = "(1 − %sln %s)/%s" % (coef(m) + " " if m > 1 else "", X, xp(m + 1))
        right = right.replace("  ", " ")
        wr = ["(%sln %s − 1)/%s" % (coef(m) + " " if m > 1 else "", X, xp(m + 1)), "1/(%s%s)" % (coef(m), xp(m)), "(1 − %sln %s)/%s" % (coef(m) + " " if m > 1 else "", X, xp(2 * m)) if m > 1 else "(1 + ln %s)/%s²" % (X, X)]
        return item("Differentiate <i>y</i> = (ln %s)/%s." % (X, xp(m)), right, [w.replace("  ", " ") for w in wr],
                    "<i>u</i> = ln %s, <i>v</i> = %s: [%s × (1/%s) − ln %s × %s]/%s, then simplify." % (X, xp(m), xp(m), X, X, coef(m) + xp(m - 1) or n(m), xp(2 * m)))
    m, a = r.randint(2, 3), r.choice([-4, -3, -2, -1, 1, 2, 3, 4, 5])
    num_ = poly({1: m - 1, 0: m * a})
    right = "%s(%s)/(%s)²" % (xp(m - 1), num_, poly({1: 1, 0: a}))
    return item("Differentiate <i>y</i> = %s/(%s)." % (xp(m), poly({1: 1, 0: a})), right,
                ["%s(%s)/(%s)²" % (xp(m - 1), poly({1: m + 1, 0: m * a}), poly({1: 1, 0: a})), "%s/(%s)²" % (coef(m) + xp(m - 1), poly({1: 1, 0: a})), "%s" % (coef(m) + xp(m - 1))],
                "[(%s)%s − %s]/(%s)² = %s(%s)/(%s)²." % (poly({1: 1, 0: a}), coef(m) + xp(m - 1), xp(m), poly({1: 1, 0: a}), xp(m - 1), num_, poly({1: 1, 0: a})))


def pq_stat(r):
    kind = r.choice(["xme", "xe", "xlnx", "lnx", "rat1", "rat2", "xae"])
    if kind == "xme":
        m, k = r.randint(1, 4), r.randint(1, 4)
        return item("Find the %s-coordinate of the stationary point of <i>y</i> = %s%s with %s &gt; 0." % (X, xp(m), e_(-k), X), n(F(m, k)), [n(F(k, m)), n(-F(m, k)), n(m * k)],
                    "d<i>y</i>/d<i>x</i> = %s%s(%s) = 0, so %s = <b>%s</b>." % (xp(m - 1), e_(-k), poly({1: -k, 0: m}).replace(X, X), X, n(F(m, k))))
    if kind == "xe":
        k = r.choice([-4, -3, -2, -1, 1, 2, 3, 4])
        return item("Find the %s-coordinate of the stationary point of <i>y</i> = %s%s." % (X, X, e_(k)), n(F(-1, k)), [n(F(1, k)), n(-k), n(k)],
                    "d<i>y</i>/d<i>x</i> = %s(1 + %s%s) = 0, so %s = <b>%s</b>." % (e_(k), coef(k), X, X, n(F(-1, k))))
    if kind == "xlnx":
        m = r.randint(1, 5)
        ex_ = lambda s: "e<sup>%s</sup>" % s
        right = ex_(MINUS + "1/%d" % m) if m > 1 else "1/e"
        return item("Find the %s-coordinate of the stationary point of <i>y</i> = %s ln %s." % (X, xp(m), X), right, [ex_("1/%d" % m) if m > 1 else "e", ex_(MINUS + str(m)) if m > 1 else ex_(MINUS + "2"), "1/%d" % m if m > 1 else "1"],
                    "d<i>y</i>/d<i>x</i> = %s(%s ln %s + 1) = 0, so ln %s = −1/%d." % (xp(m - 1) or "1", coef(m) or "", X, X, m))
    if kind == "lnx":
        m = r.randint(1, 5)
        ex_ = lambda s: "e<sup>%s</sup>" % s
        right = ex_("1/%d" % m) if m > 1 else "e"
        return item("Find the %s-coordinate of the stationary point of <i>y</i> = (ln %s)/%s." % (X, X, xp(m)), right, [ex_(MINUS + "1/%d" % m) if m > 1 else "1/e", ex_(str(m)) if m > 1 else ex_("2"), "1/%d" % m if m > 1 else "1"],
                    "d<i>y</i>/d<i>x</i> = (1 − %sln %s)/%s = 0, so ln %s = 1/%d." % (coef(m) + " " if m > 1 else "", X, xp(m + 1), X, m))
    if kind in ("rat1", "rat2"):
        a = r.randint(1, 9)
        y = "%s/(%s² + %d)" % (X, X, a * a) if kind == "rat1" else "(%s² + %d)/%s" % (X, a * a, X)
        return item("Find the positive %s-coordinate of the stationary point of <i>y</i> = %s." % (X, y), num(a), [num(a * a), n(F(a, 2)) if a % 2 == 0 else "√%d" % a if a not in (1, 4, 9) else num(2 * a), num(2 * a) if a != 2 else num(a + 1)],
                    ("Quotient rule: (%s² + %d − 2%s²)/(…)² = 0, so %s² = %d." % (X, a * a, X, X, a * a)) if kind == "rat1" else ("Quotient rule: (2%s² − %s² − %d)/%s² = 0, so %s² = %d." % (X, X, a * a, X, X, a * a)))
    a, k = r.randint(-4, 4), r.choice([-2, -1, 1, 2])
    xv = -a - F(1, k)
    return item("Find the %s-coordinate of the stationary point of <i>y</i> = (%s)%s." % (X, poly({1: 1, 0: a}), e_(k)), n(xv), [n(-a + F(1, k)), n(-a), n(a - F(1, k))],
                "d<i>y</i>/d<i>x</i> = %s[1 + %s(%s)] = 0, so %s = <b>%s</b>." % (e_(k), coef(k) or "", poly({1: 1, 0: a}), X, n(xv)))


def pq_tan(r):
    kind = r.choice(["xe", "xe", "quot", "ln"])
    if kind == "xe":
        a, k = r.choice([-4, -3, -2, -1, 1, 2, 3, 4, 5]), r.choice([-3, -2, -1, 1, 2, 3])
        m = 1 + k * a
        if m == 0:
            return None
        right = "<i>y</i> = %s" % poly({1: m, 0: a})
        wr = ["<i>y</i> = %s" % poly({1: k * a, 0: a}), "<i>y</i> = %s" % poly({1: a, 0: m}), "<i>y</i> = %s" % poly({1: m, 0: -a}), "<i>y</i> = %s" % poly({1: m})]
        return item("Find the equation of the tangent to <i>y</i> = (%s)%s at the point where %s = 0." % (poly({1: 1, 0: a}), e_(k), X), right, wr,
                    "At %s = 0, <i>y</i> = %s. d<i>y</i>/d<i>x</i> = %s + %s(%s)%s = %s at %s = 0." % (X, n(a), e_(k), coef(k) or "", poly({1: 1, 0: a}), e_(k), n(m), X))
    if kind == "quot":
        a, b, c = r.randint(1, 5), r.choice([-4, -3, -2, -1, 1, 2, 3, 4]), r.choice([-3, -2, -1, 1, 2, 3])
        m = a - b * c
        if m == 0:
            return None
        return item("Find the equation of the tangent to <i>y</i> = (%s)/(%s) at the point where %s = 0." % (poly({1: a, 0: b}), poly({1: c, 0: 1}), X), "<i>y</i> = %s" % poly({1: m, 0: b}),
                    ["<i>y</i> = %s" % poly({1: a + b * c, 0: b}), "<i>y</i> = %s" % poly({1: a, 0: b}), "<i>y</i> = %s" % poly({1: b, 0: m})],
                    "At %s = 0, <i>y</i> = %s. d<i>y</i>/d<i>x</i> = [%d(%s) − %s(%s)]/(%s)² = %s at %s = 0." % (X, n(b), a, poly({1: c, 0: 1}), n(c), poly({1: a, 0: b}), poly({1: c, 0: 1}), n(m), X))
    a, m = r.randint(1, 6), r.randint(2, 5)
    return item("Find the equation of the tangent to <i>y</i> = %s ln %s at the point where %s = 1." % (coef(a) + xp(m), X, X), "<i>y</i> = %s" % poly({1: a, 0: -a}),
                ["<i>y</i> = %s" % poly({1: a * m, 0: -a * m}), "<i>y</i> = %s" % poly({1: a}), "<i>y</i> = %s" % poly({1: a, 0: a})],
                "At %s = 1, ln 1 = 0 so <i>y</i> = 0. d<i>y</i>/d<i>x</i> = %s(%s ln %s + 1) = %d at %s = 1, so <i>y</i> = %d(%s − 1)." % (X, coef(a) + xp(m - 1), coef(m), X, a, X, a, X))


# =================================================================== A level: hypothesis tests (normal mean, correlation)
NCTX = [("mass of a bag of flour", "g", 500, [5, 8, 10, 12]), ("length of a bolt", "mm", 60, [2, 3, 4, 5]), ("time to assemble a chair", "minutes", 40, [4, 5, 6, 8]),
        ("lifetime of a battery", "hours", 120, [8, 10, 12, 15]), ("height of a sunflower", "cm", 180, [10, 12, 15, 20]), ("volume of a bottle of water", "ml", 750, [6, 8, 10, 12]),
        ("reaction time of a pupil", "ms", 250, [20, 25, 30, 40]), ("journey time to work", "minutes", 35, [3, 4, 5, 6]), ("mass of a loaf of bread", "g", 800, [10, 12, 15, 20]),
        ("length of a cucumber", "cm", 30, [2, 3, 4])]
CRIT = {(0.05, 1): 1.6449, (0.05, 2): 1.96, (0.01, 1): 2.3263, (0.01, 2): 2.5758, (0.1, 1): 1.2816, (0.1, 2): 1.6449, (0.025, 1): 1.96}
SQ = [4, 9, 16, 25, 36, 49, 64, 81, 100]


def pct(s):
    return ("%g" % (s * 100)) + "%"


def h_hyp(r):
    c = r.choice(NCTX)
    mu = c[2]
    dirn = r.choice(["more", "less", "diff"])
    who_ = who(r)
    claim = {"more": "the mean has increased", "less": "the mean has decreased", "diff": "the mean has changed"}[dirn]
    q = "The %s is normally distributed with mean %s %s. %s thinks that %s. Which hypotheses should be used?" % (c[0], num(mu), c[1], who_, claim)
    op = {"more": "&gt;", "less": "&lt;", "diff": "≠"}
    H = lambda o, sym="μ": "H<sub>0</sub>: %s = %s, H<sub>1</sub>: %s %s %s" % (sym, num(mu), sym, o, num(mu))
    right = H(op[dirn])
    wr = [H(op[x]) for x in op if x != dirn] + [H(op[dirn], "<span style='text-decoration:overline'><i>x</i></span>")]
    return item(q, right, wr, "Hypotheses are about the population mean μ. “%s” gives a %s test." % (claim.capitalize(), "two-tailed" if dirn == "diff" else "one-tailed"))


RCTX = [("the hours of sunshine and the number of ice creams sold", "positive"), ("the age of a car and its value", "negative"), ("a pupil's height and their shoe size", "positive"),
        ("the temperature and the amount of gas used for heating", "negative"), ("revision time and test score", "positive"), ("the altitude of a town and its mean temperature", "negative"),
        ("the price of a ticket and the number sold", "negative"), ("arm span and height", "positive"), ("the rainfall in a month and the umbrellas sold", "positive"),
        ("the hours of daylight and the electricity used for lighting", "negative")]


def h_rhyp(r):
    c, sign = r.choice(RCTX)
    kind = r.choice([sign, "any"])
    q = "A scientist wants to test whether there is %s correlation between %s. Which hypotheses should be used?" % ({"positive": "positive", "negative": "negative", "any": "any"}[kind], c)
    op = {"positive": "&gt;", "negative": "&lt;", "any": "≠"}
    H = lambda o, sym="ρ": "H<sub>0</sub>: %s = 0, H<sub>1</sub>: %s %s 0" % (sym, sym, o)
    right = H(op[kind])
    wr = [H(op[x]) for x in op if x != kind] + [H(op[kind], "<i>r</i>")]
    return item(q, right, wr, "Use ρ, the population correlation coefficient. H<sub>0</sub> says there is no correlation.")


def _dec(v, dp=4):
    s = ("%." + str(dp) + "f") % v
    return s.rstrip("0").rstrip(".")


def h_mean_dist(r):
    c = r.choice(NCTX)
    sig = r.choice(c[3])
    nn = r.choice([4, 5, 8, 10, 16, 20, 25, 40, 50, 64, 100])
    var = F(sig * sig, nn)
    if (var * 10000).denominator != 1:
        return None
    k = r.choice(["var", "sd"]) if nn in SQ else "var"
    lead = "The %s is normally distributed with mean %s %s and standard deviation %s %s. A random sample of %d is taken. " % (c[0], num(c[2]), c[1], num(sig), c[1], nn)
    if k == "var":
        return item(lead + "Find the variance of the sample mean <span style='text-decoration:overline'><i>X</i></span>.", _dec(float(var)),
                    [_dec(sig * sig / math.sqrt(nn), 2), _dec(sig / nn), num(sig * sig) if sig * sig != var else _dec(float(var) * 2)],
                    "Var(<span style='text-decoration:overline'><i>X</i></span>) = σ²/<i>n</i> = %d/%d = <b>%s</b>." % (sig * sig, nn, _dec(float(var))))
    se = F(sig, int(math.isqrt(nn)))
    return item(lead + "Find the standard deviation of the sample mean <span style='text-decoration:overline'><i>X</i></span>.", "%s %s" % (_dec(float(se)), c[1]),
                ["%s %s" % (_dec(sig / nn), c[1]), "%s %s" % (num(sig), c[1]), "%s %s" % (_dec(sig * sig / nn), c[1])],
                "Standard deviation = σ/√<i>n</i> = %d/√%d = <b>%s %s</b>." % (sig, nn, _dec(float(se)), c[1]))


def h_z(r):
    c = r.choice(NCTX)
    sig = r.choice(c[3])
    nn = r.choice(SQ)
    rt = math.isqrt(nn)
    delta = F(r.choice([1, 2, 3, 4, 5, 6, 8]) * sig, rt * r.choice([2, 4, 5])) * r.choice([1, -1])
    if (delta * 100).denominator != 1 or delta == 0:
        return None
    xbar = c[2] + delta
    z = float(delta) / (sig / rt)
    q = "The %s has mean %s %s and standard deviation %s %s. A sample of %d has mean %s %s. Find the test statistic <i>z</i>, to 2 decimal places." % (c[0], num(c[2]), c[1], num(sig), c[1], nn, _dec(float(xbar), 2), c[1])
    return item(q, fx(z, 2), [fx(float(delta) / sig, 2), fx(float(delta) / (sig / nn), 2), fx(-z, 2), fx(float(delta) * rt / sig ** 2, 2)],
                "<i>z</i> = (%s − %s) ÷ (%d/√%d) = %s ÷ %s = <b>%s</b>." % (_dec(float(xbar), 2), num(c[2]), sig, nn, fx(float(delta), 2).rstrip("0").rstrip("."), _dec(sig / rt, 4), fx(z, 2)))


def h_dec(r):
    c = r.choice(NCTX)
    sig = r.choice([0.05, 0.05, 0.01, 0.1])
    tails = r.choice([1, 1, 2])
    up = r.random() < 0.5
    cv = CRIT[(sig, tails)]
    z = round(r.uniform(0.6, 3.2), 2) * (1 if up else -1)
    if abs(abs(z) - cv) < 0.03:
        return None
    rej = abs(z) > cv
    who_ = who(r)
    claim = ("increased" if up else "decreased") if tails == 1 else "changed"
    q = ("%s tests whether the mean %s has %s, at the %s significance level. The test statistic is <i>z</i> = %s. The critical value is %s. What is the conclusion?"
         % (who_, c[0], claim, pct(sig), fx(z, 2), ("%s" % ("" if up else MINUS) + "%.4f" % cv if tails == 1 else "±%.4f" % cv).replace("1.9600", "1.96")))
    yes = "Reject H<sub>0</sub>: there is evidence that the mean %s has %s" % (c[0], claim)
    no = "Do not reject H<sub>0</sub>: there is not enough evidence that the mean %s has %s" % (c[0], claim)
    right = yes if rej else no
    return item(q, right, [no if rej else yes, "Accept H<sub>1</sub>: this proves that the mean %s has %s" % (c[0], claim), "Reject H<sub>1</sub>: the mean %s is exactly %s %s" % (c[0], num(c[2]), c[1])],
                "|<i>z</i>| = %s is %s than %s, so <i>z</i> is %s the critical region." % (fx(abs(z), 2), "greater" if rej else "less", "%.4f" % cv if cv != 1.96 else "1.96", "in" if rej else "not in"))


def h_crit(r):
    c = r.choice(NCTX)
    sig_l = r.choice([0.05, 0.01, 0.1])
    s = r.choice(c[3])
    nn = r.choice(SQ)
    rt = math.isqrt(nn)
    up = r.random() < 0.5
    cv = CRIT[(sig_l, 1)]
    se = s / rt
    b = c[2] + cv * se if up else c[2] - cv * se
    bar = "<span style='text-decoration:overline'><i>X</i></span>"
    sym = "&gt;" if up else "&lt;"
    q = ("The %s is normally distributed with standard deviation %s %s. A test of H<sub>0</sub>: μ = %s against H<sub>1</sub>: μ %s %s uses a sample of %d at the %s level (critical <i>z</i> value %s%.4f). Find the critical region for %s, to 2 decimal places."
         % (c[0], num(s), c[1], num(c[2]), sym, num(c[2]), nn, pct(sig_l), "" if up else MINUS, cv, bar))
    right = "%s %s %.2f" % (bar, sym, b)
    wr = ["%s %s %.2f" % (bar, sym, c[2] + (cv * s if up else -cv * s)), "%s %s %.2f" % (bar, sym, c[2] + (cv * s / nn if up else -cv * s / nn)), "%s %s %.2f" % (bar, "&lt;" if up else "&gt;", b)]
    return item(q, right, wr, "Boundary = %s %s %.4f × %s/√%d = %.2f." % (num(c[2]), "+" if up else "−", cv, num(s), nn, b))


RTAB = {(0.05, 1): {6: 0.7293, 7: 0.6694, 8: 0.6215, 10: 0.5494, 12: 0.4973, 15: 0.4409, 20: 0.3783, 25: 0.3365, 30: 0.3061},
        (0.05, 2): {6: 0.8114, 7: 0.7545, 8: 0.7067, 10: 0.6319, 12: 0.5760, 15: 0.5140, 20: 0.4438, 25: 0.3961, 30: 0.3610},
        (0.01, 1): {6: 0.8822, 7: 0.8329, 8: 0.7887, 10: 0.7155, 12: 0.6581, 15: 0.5923, 20: 0.5155, 25: 0.4622, 30: 0.4226}}


def h_corr(r):
    c, sign = r.choice(RCTX)
    level, tails = r.choice(list(RTAB))
    if tails == 2:
        sign = "any"
    nn = r.choice(list(RTAB[(level, tails)]))
    cv = RTAB[(level, tails)][nn]
    mag = round(r.uniform(max(0.1, cv - 0.25), min(0.98, cv + 0.25)), 3)
    if abs(mag - cv) < 0.01:
        return None
    rr = -mag if (sign == "negative" or (sign == "any" and r.random() < 0.5)) else mag
    rej = mag > cv
    word = {"positive": "positive correlation", "negative": "negative correlation", "any": "correlation"}[sign]
    q = ("A sample of %d pairs gives a product moment correlation coefficient of <i>r</i> = %s between %s. Test for %s at the %s level. The critical value is %s%.4f. What is the conclusion?"
         % (nn, fx(rr, 3), c, word, pct(level), "±" if tails == 2 else ("" if sign == "positive" else MINUS), cv))
    yes = "Reject H<sub>0</sub>: there is evidence of %s" % word
    no = "Do not reject H<sub>0</sub>: there is not enough evidence of %s" % word
    right = yes if rej else no
    return item(q, right, [no if rej else yes, "Accept H<sub>0</sub>: this proves there is no correlation", "Reject H<sub>0</sub>: one variable causes the other to change"],
                "|<i>r</i>| = %.3f is %s than %.4f, so %s H<sub>0</sub>." % (mag, "greater" if rej else "less", cv, "reject" if rej else "do not reject"))


def h_tails(r):
    c = r.choice(NCTX)
    level = r.choice([0.05, 0.01, 0.1])
    tails = r.choice([1, 2])
    claim = r.choice(["has increased", "has decreased"]) if tails == 1 else r.choice(["has changed", "is different from %s %s" % (num(c[2]), c[1])])
    cv = CRIT[(level, tails)]
    q = "A test at the %s significance level checks whether the mean %s %s. Which critical value of <i>z</i> should be used?" % (pct(level), c[0], claim)
    right = ("±%.4f" % cv if tails == 2 else ("%s%.4f" % ("" if "increased" in claim else MINUS, cv))).replace("1.9600", "1.96")
    other = CRIT[(level, 3 - tails)]
    wr = [("%.4f" % other if tails == 2 else "±%.4f" % other).replace("1.9600", "1.96"), ("%s%.4f" % (MINUS if "increased" in claim else "", cv)) if tails == 1 else "%.4f" % cv,
          "±%.4f" % CRIT[(0.05 if level != 0.05 else 0.01, tails)] if tails == 2 else "%.4f" % CRIT[(0.05 if level != 0.05 else 0.01, 1)]]
    return item(q, right, [w.replace("1.9600", "1.96") for w in wr], "%s: %s." % ("Two-tailed test, so split %s between the two tails" % pct(level) if tails == 2 else "One-tailed test, so all %s is in one tail" % pct(level), right))
