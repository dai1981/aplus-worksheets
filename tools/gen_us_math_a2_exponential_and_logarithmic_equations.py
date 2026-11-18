# -*- coding: utf-8 -*-
"""
US Algebra 2: Exponential and Logarithmic Equations (Common Core F-LE.A.4, A-REI.D.11)
  python3 tools/gen_us_math_a2_exponential_and_logarithmic_equations.py
Equations with a common base, solving with logarithms, logarithmic equations, equations that use the log
properties (with extraneous solutions), and applications: doubling time, interest, pH and decibels.
Wrong answers come from real mistakes: dividing the numbers instead of the logs, forgetting to isolate the
power first, keeping a solution that makes a log argument negative, and taking the log of only one side.
"""
import math
import random
from fractions import Fraction as F
from us_hs import B, S, make, lesson, collect, T, num, MINUS, fr, People
from a2_common import sf, lin

R = random.Random(96101)


def d3(x):
    return "%.3f" % x


def xs(v):
    return "<i>x</i> = %s" % v


# ------------------------------------------------------------ set 1: common base
def one_base(r):
    b = r.choice([2, 3, 5])
    kind = r.choice(["simple", "simple", "pow"])
    if kind == "simple":
        k = r.randint(2, 6) if b == 2 else r.randint(2, 4)
        c = r.randint(-4, 4)
        a = r.choice([1, 2, 3])
        # b^(a x + c) = b^k  -> x = (k - c)/a
        x0 = F(k - c, a)
        ex = "%s%s" % ("" if a == 1 else num(a), "<i>x</i>") + ((" %s %d" % ("+" if c > 0 else MINUS, abs(c))) if c else "")
        q = "Solve %s." % B("%d<sup>%s</sup> = %s" % (b, ex, num(b ** k)))
        return T(q, xs(sf(x0)), [xs(sf(w)) for w in dict.fromkeys([F(b ** k - c, a), F(k + c, a), F(k, a)]) if w != x0][:3],
                 "Write %s as %d<sup>%d</sup>. Set the exponents equal: %s = %d, so <i>x</i> = <b>%s</b>." % (num(b ** k), b, k, ex, k, sf(x0)))
    base1, base2, p, q_ = r.choice([(4, 8, 2, 3), (9, 27, 2, 3), (25, 125, 2, 3), (8, 16, 3, 4), (4, 32, 2, 5), (27, 9, 3, 2), (16, 64, 4, 6)])
    m = r.choice([1, 2])
    # base1^x = base2^(x - m)  -> p x = q (x - m) -> x = q m/(q - p)
    x0 = F(q_ * m, q_ - p)
    q = "Solve %s." % B("%d<sup><i>x</i></sup> = %d<sup><i>x</i> %s %d</sup>" % (base1, base2, MINUS, m))
    bb = round(base1 ** (1 / p))
    return T(q, xs(sf(x0)), [xs(sf(w)) for w in dict.fromkeys([F(m * p, p - q_) if p != q_ else x0 + 1, F(m), -x0]) if w != x0][:3],
             "Rewrite with base %d: %d<sup>%d<i>x</i></sup> = %d<sup>%d(<i>x</i> %s %d)</sup>. So %d<i>x</i> = %d<i>x</i> %s %d and <i>x</i> = <b>%s</b>." % (
                 bb, bb, p, bb, q_, MINUS, m, p, q_, MINUS, q_ * m, sf(x0)))


# ------------------------------------------------------------ set 2: solve with logarithms
def one_log(r):
    kind = r.choice(["plain", "plain", "iso", "e"])
    if kind == "plain":
        b = r.choice([2, 3, 5, 6, 7])
        c = r.choice([10, 15, 20, 40, 50, 75, 100, 200])
        if c in (b ** 2, b ** 3):
            return None
        x0 = math.log(c) / math.log(b)
        q = "Solve %s. Round to the nearest thousandth." % B("%d<sup><i>x</i></sup> = %d" % (b, c))
        return T(q, xs(d3(x0)), [xs(d3(c / b)), xs(d3(math.log10(c / b))), xs(d3(math.log(b) / math.log(c)))],
                 "Take the log of both sides: <i>x</i> log %d = log %d, so <i>x</i> = log %d ÷ log %d ≈ <b>%s</b>." % (b, c, c, b, d3(x0)))
    if kind == "iso":
        a = r.choice([2, 3, 4, 5])
        b = r.choice([2, 3, 10])
        k = r.choice([1, 3, 5, 7])
        c = r.choice([20, 30, 50, 60, 100])
        rhs = c + k
        x0 = math.log(c / a) / math.log(b)
        q = "Solve %s. Round to the nearest thousandth." % B("%d · %d<sup><i>x</i></sup> + %d = %d" % (a, b, k, rhs))
        return T(q, xs(d3(x0)), [xs(d3(math.log(rhs / a) / math.log(b))), xs(d3(math.log(c) / math.log(a * b))), xs(d3(math.log(c - a) / math.log(b)) if c > a else d3(x0 + 1))],
                 "Isolate the power first: %d<sup><i>x</i></sup> = (%d %s %d) ÷ %d = %s. Then <i>x</i> = log(%s) ÷ log %d ≈ <b>%s</b>." % (
                     b, rhs, MINUS, k, a, sf(F(c, a)), sf(F(c, a)), b, d3(x0)))
    c = r.choice([5, 8, 12, 20, 30])
    k = r.choice([2, 3, F(1, 2)])
    x0 = math.log(c) / float(k)
    q = "Solve %s. Round to the nearest thousandth." % B("<i>e</i><sup>%s<i>x</i></sup> = %d" % (sf(k) if k != 1 else "", c))
    return T(q, xs(d3(x0)), [xs(d3(math.log(c) * float(k))), xs(d3(math.log10(c) / float(k))), xs(d3(c / float(k) / math.e))],
             "Take ln of both sides: %s<i>x</i> = ln %d, so <i>x</i> = ln %d ÷ %s ≈ <b>%s</b>." % (sf(k), c, c, sf(k), d3(x0)))


# ------------------------------------------------------------ set 3: logarithmic equations
def one_logeq(r):
    b = r.choice([2, 3, 4, 5, 10])
    k = r.choice([1, 2, 3]) if b != 10 else r.choice([1, 2])
    a = r.choice([1, 2, 3])
    c = r.randint(-6, 9)
    x0 = F(b ** k - c, a)
    if (a * x0 + c) <= 0:
        return None
    inside = "%s<i>x</i>%s" % ("" if a == 1 else num(a), (" %s %d" % ("+" if c > 0 else MINUS, abs(c))) if c else "")
    lgs = "log<sub>%d</sub>" % b if b != 10 else "log"
    q = "Solve %s." % B("%s(%s) = %d" % (lgs, inside, k))
    return T(q, xs(sf(x0)), [xs(sf(w)) for w in dict.fromkeys([F(k * b - c, a), F(k ** b - c, a) if k ** b < 1000 else x0 + 2, F(b ** k + c, a)]) if w != x0][:3],
             "Rewrite in exponential form: %s = %d<sup>%d</sup> = %s. So <i>x</i> = <b>%s</b>." % (inside, b, k, num(b ** k), sf(x0)))


# ------------------------------------------------------------ set 4: using the properties
def one_prop(r):
    kind = r.choice(["sum", "sum", "diff", "same"])
    if kind == "sum":
        # log_b x + log_b (x + d) = k  ->  x(x + d) = b^k, roots p and -(p + d)
        p = r.randint(1, 9)
        d = r.choice([x for x in range(-5, 8) if x and p + x > 0])
        v = p * (p + d)
        b, k = None, None
        for bb in (2, 3, 4, 5, 6, 10):
            for kk in (1, 2, 3, 4):
                if bb ** kk == v:
                    b, k = bb, kk
        if b is None:
            return None
        other = -(p + d)
        lgs = "log<sub>%d</sub>" % b if b != 10 else "log"
        q = "Solve %s." % B("%s <i>x</i> + %s(%s) = %d" % (lgs, lgs, lin(-d), k))
        right = xs(sf(p))
        return T(q, right, [xs("%s, %s" % (sf(min(p, other)), sf(max(p, other)))), xs(sf(other)), "No solution"],
                 "Product property: %s(<i>x</i>(%s)) = %d, so <i>x</i>(%s) = %d. That gives <i>x</i> = %s or %s. A log of a negative number is undefined, so %s is extraneous. <b>%s</b>." % (
                     lgs, lin(-d), k, lin(-d), v, sf(p), sf(other), sf(other), right))
    if kind == "diff":
        b = r.choice([2, 3, 10])
        k = r.choice([1, 2])
        m = b ** k
        c = r.randint(1, 20)
        # log(x + c) - log x = k -> x + c = m x -> x = c/(m - 1)
        x0 = F(c, m - 1)
        if x0.denominator > 9:
            return None
        lgs = "log<sub>%d</sub>" % b if b != 10 else "log"
        q = "Solve %s." % B("%s(<i>x</i> + %d) %s %s <i>x</i> = %d" % (lgs, c, MINUS, lgs, k))
        return T(q, xs(sf(x0)), [xs(sf(w)) for w in dict.fromkeys([F(c, m), F(m - c) if m != c else x0 + 1, F(c, m + 1)]) if w != x0][:3],
                 "Quotient property: %s((<i>x</i> + %d)/<i>x</i>) = %d, so (<i>x</i> + %d)/<i>x</i> = %d. Then <i>x</i> + %d = %d<i>x</i> and <i>x</i> = <b>%s</b>." % (lgs, c, k, c, m, c, m, sf(x0)))
    a, c = r.randint(2, 5), r.randint(-6, 6)
    d = r.randint(1, 9)
    # log(a x + c) = log(x + d) -> a x + c = x + d -> x = (d - c)/(a - 1)
    x0 = F(d - c, a - 1)
    if x0 + d <= 0 or a * x0 + c <= 0:
        return None
    q = "Solve %s." % B("ln(%s<i>x</i>%s) = ln(<i>x</i> + %d)" % (num(a), (" %s %d" % ("+" if c > 0 else MINUS, abs(c))) if c else "", d))
    return T(q, xs(sf(x0)), [xs(sf(w)) for w in dict.fromkeys([F(d + c, a - 1), F(d - c, a + 1), F(d, a)]) if w != x0][:3],
             "If ln <i>M</i> = ln <i>N</i>, then <i>M</i> = <i>N</i>. %d<i>x</i> %s %d = <i>x</i> + %d, so <i>x</i> = <b>%s</b>, and both arguments are positive." % (a, "+" if c >= 0 else MINUS, abs(c), d, sf(x0)))


# ------------------------------------------------------------ set 5: applications
def one_app(r):
    pp = People(r)
    nm, he, his = pp.next()
    kind = r.choice(["double", "double", "goal", "ph", "db"])
    if kind == "double":
        rate = r.choice([3, 4, 5, 6, 7, 8])
        cont = r.random() < 0.5
        t = math.log(2) / (rate / 100) if cont else math.log(2) / math.log(1 + rate / 100)
        q = "How long does it take money to double at %d%% interest compounded %s? Round to the nearest tenth of a year." % (rate, "continuously" if cont else "annually")
        right = "%.1f years" % t
        wr = ["%.1f years" % (100 / rate / 2), "%.1f years" % (2 / (rate / 100)), "%.1f years" % (math.log(2) / (rate / 100) if not cont else math.log(2) / math.log(1 + rate / 100))]
        return T(q, right, [w for w in dict.fromkeys(wr) if w != right][:3] + (["%.1f years" % (t + 1)] if len(set(wr) - {right}) < 3 else []),
                 ("Solve %s: " % ("<i>e</i><sup>%s<i>t</i></sup> = 2" % ("%.2f" % (rate / 100)) if cont else "(1.%02d)<sup><i>t</i></sup> = 2" % rate)) +
                 ("<i>t</i> = ln 2 ÷ %.2f ≈ <b>%s</b>." % (rate / 100, right) if cont else "<i>t</i> = log 2 ÷ log 1.%02d ≈ <b>%s</b>." % (rate, right)))
    if kind == "goal":
        P = r.choice([1000, 2000, 5000])
        goal = P * r.choice([3, F(3, 2), F(5, 2), 4])
        rate = r.choice([4, 5, 6])
        t = math.log(float(goal) / P) / math.log(1 + rate / 100 / 12) / 12
        q = "%s invests %s at %d%% compounded monthly. After how many years will the balance first reach %s? Round to the nearest tenth." % (nm, "$" + num(P), rate, "$" + num(goal))
        right = "%.1f years" % t
        return T(q, right, ["%.1f years" % (math.log(float(goal) / P) / math.log(1 + rate / 100)), "%.1f years" % ((float(goal) / P - 1) / (rate / 100)), "%.1f years" % (t * 12)],
                 "%s(1 + %.2f/12)<sup>12<i>t</i></sup> = %s, so 12<i>t</i> = log(%s) ÷ log(1 + %.2f/12) and <i>t</i> ≈ <b>%s</b>." % (
                     num(P), rate / 100, num(goal), sf(F(goal) / P), rate / 100, right))
    if kind == "ph":
        e = r.choice([2, 3, 4, 5, 6, 8, 9, 10, 11])
        if r.random() < 0.5:
            q = "The pH of a solution is pH = %slog[H<sup>+</sup>]. A solution has [H<sup>+</sup>] = 10<sup>%s%d</sup> moles per liter. What is its pH?" % (MINUS, MINUS, e)
            return T(q, num(e), [MINUS + num(e), num(10 - e) if 10 - e != e and 10 - e > 0 else num(e + 2), num(e * 10)],
                     "pH = %slog(10<sup>%s%d</sup>) = %s(%s%d) = <b>%d</b>." % (MINUS, MINUS, e, MINUS, MINUS, e, e))
        q = "A solution has pH %d. What is its hydrogen ion concentration [H<sup>+</sup>], using pH = %slog[H<sup>+</sup>]?" % (e, MINUS)
        right = "10<sup>%s%d</sup> moles per liter" % (MINUS, e)
        return T(q, right, ["10<sup>%d</sup> moles per liter" % e, "%s%d moles per liter" % (MINUS, e), "%d<sup>10</sup> moles per liter" % e],
                 "%d = %slog[H<sup>+</sup>], so log[H<sup>+</sup>] = %s%d and [H<sup>+</sup>] = <b>%s</b>." % (e, MINUS, MINUS, e, right))
    d = r.choice([10, 20, 30])
    q = "Sound level in decibels is <i>L</i> = 10 log(<i>I</i>/<i>I</i><sub>0</sub>). If one sound is %d dB louder than another, how many times as intense is it?" % d
    ans = 10 ** (d // 10)
    return T(q, num(ans) + " times", [num(d) + " times", num(d // 10) + " times", num(2 ** (d // 10)) + " times"],
             "A difference of %d dB means log(ratio) = %d ÷ 10 = %d, so the ratio is 10<sup>%d</sup> = <b>%s times</b>." % (d, d, d // 10, d // 10, num(ans)))


def build():
    sets = [S("Equations with a common base", collect(one_base, 20, R)),
            S("Solve with logarithms", collect(one_log, 20, R)),
            S("Logarithmic equations", collect(one_logeq, 20, R)),
            S("Using the log properties", collect(one_prop, 20, R)),
            S("Applications", collect(one_app, 20, R))]
    body = lesson(
        "<ul><li>If both sides can use the <b>same base</b>, set the exponents equal: 2<sup><i>x</i>+1</sup> = 2<sup>5</sup> gives <i>x</i> + 1 = 5.</li>"
        "<li>Otherwise, isolate the power and <b>take the log of both sides</b>: 5<sup><i>x</i></sup> = 40 gives <i>x</i> = log 40 ÷ log 5. Use ln with base <i>e</i>.</li>"
        "<li>To solve log<sub><i>b</i></sub>(<i>M</i>) = <i>k</i>, rewrite it as <i>M</i> = <i>b</i><sup><i>k</i></sup>. Combine logs with the properties first if there is more than one.</li></ul>"
        "<p>Always check log equations: the argument of every log must be positive, so some answers are extraneous.</p>",
        [("Solve 3 · 2<sup><i>x</i></sup> = 48.", ["2<sup><i>x</i></sup> = 16 = 2<sup>4</sup>"], "<i>x</i> = 4"),
         ("Solve log<sub>2</sub> <i>x</i> + log<sub>2</sub>(<i>x</i> %s 2) = 3." % MINUS, ["<i>x</i>(<i>x</i> %s 2) = 8" % MINUS, "<i>x</i> = 4 or %s2; %s2 is extraneous" % (MINUS, MINUS)], "<i>x</i> = 4")],
        ["Dividing the numbers instead of the logs: 5<sup><i>x</i></sup> = 40 does not give <i>x</i> = 8.",
         "Taking logs before isolating the power, such as with 3 · 2<sup><i>x</i></sup>.",
         "Keeping a solution that makes a log argument zero or negative.",
         "Writing log<sub><i>b</i></sub> <i>x</i> = <i>k</i> as <i>x</i> = <i>kb</i> instead of <i>x</i> = <i>b</i><sup><i>k</i></sup>."])
    faq = [("How do you solve an exponential equation?", "If you can write both sides with the same base, set the exponents equal. Otherwise, isolate the power and take the log of both sides."),
           ("How do you solve a logarithmic equation?", "Combine logs into one using the properties, rewrite in exponential form, solve, and check that every log argument is positive."),
           ("Why can log equations have extraneous solutions?", "Logs are only defined for positive numbers. An algebraic answer that makes an argument zero or negative must be rejected."),
           ("How long does it take money to double?", "Solve (1 + r)^t = 2 for annual compounding, or e^(rt) = 2 for continuous compounding: t = ln 2 ÷ r.")]
    make("exponential-and-logarithmic-equations", 11, "F-LE.A.4",
         "Exponential and Logarithmic Equations",
         "Solving Exponential and Logarithmic Equations Worksheet (Algebra 2, F-LE.A.4) | 100 Questions",
         "Exponential and Log Equations",
         "For exponential models, express as a logarithm the solution to ab^(ct) = d where a, c, and d are numbers and the base b is 2, 10, or e; evaluate the logarithm using technology.",
         "Free Algebra 2 worksheet on solving exponential and logarithmic equations: common bases, taking logs, log properties, extraneous solutions, doubling time and pH. 100 questions.",
         "Same base: set the exponents equal. Otherwise, take the log of both sides.",
         "log_b M = k means M = b^k. Check that every log argument is positive.",
         body, faq, sets, R, domain="Exponential and Logarithmic Functions", grade="algebra-2")


if __name__ == "__main__":
    build()
