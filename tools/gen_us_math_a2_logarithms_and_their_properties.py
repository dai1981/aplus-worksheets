# -*- coding: utf-8 -*-
"""
US Algebra 2: Logarithms and Their Properties (Common Core F-LE.A.4, F-BF.B.5, F-IF.C.8)
  python3 tools/gen_us_math_a2_logarithms_and_their_properties.py
Converting between exponential and logarithmic form, evaluating logarithms, expanding and condensing with
the product, quotient and power properties, the change-of-base formula, and the domain of log functions.
Wrong answers come from real mistakes: swapping the base and the exponent, writing log(a + b) as
log a + log b, dividing logs instead of subtracting, and putting the power inside instead of in front.
"""
import math
import random
from fractions import Fraction as F
from us_hs import B, S, make, lesson, collect, T, num, MINUS, fr
from a2_common import sf

R = random.Random(96001)


def lg(b, x):
    if b == 10:
        return "log %s" % x
    if b == "e":
        return "ln %s" % x
    return "log<sub>%s</sub> %s" % (b, x)


def lgp(b, x):
    """log with argument in parentheses when it is not a single symbol"""
    return lg(b, x if len(x.replace("<i>", "").replace("</i>", "")) <= 1 or x.isdigit() else "(%s)" % x)


# ------------------------------------------------------------ set 1: convert forms
def one_conv(r):
    b = r.choice([2, 3, 4, 5, 6, 10])
    k = r.choice([x for x in range(-3, 6) if x])
    v = F(b) ** k
    if v.denominator > 1000 or v.numerator > 100000:
        return None
    vs = sf(v)
    if r.random() < 0.5:
        q = "Write %s in logarithmic form." % B("%d<sup>%s</sup> = %s" % (b, sf(k), vs))
        right = "%s = %s" % (lg(b, vs), sf(k))
        wr = ["%s = %s" % (lg(b, sf(k)), vs), "%s = %d" % (lg(vs, sf(k)) if v.denominator == 1 else lg(sf(k), vs), b), "%s = %s" % (lg(sf(k), vs) if k > 1 else lg(b, sf(k + 1)), sf(b))]
        return T(q, right, [w for w in dict.fromkeys(wr) if w != right][:3],
                 "<i>b</i><sup><i>y</i></sup> = <i>x</i> means log<sub><i>b</i></sub> <i>x</i> = <i>y</i>. The base stays the base, and the logarithm equals the exponent. <b>%s</b>." % right)
    q = "Write %s in exponential form." % B("%s = %s" % (lg(b, vs), sf(k)))
    right = "%d<sup>%s</sup> = %s" % (b, sf(k), vs)
    wr = ["%s<sup>%d</sup> = %s" % ("(%s)" % sf(k) if k < 0 else sf(k), b, vs), "%s<sup>%s</sup> = %d" % (vs, sf(k), b), "%d<sup>%s</sup> = %s" % (b, vs, sf(k))]
    return T(q, right, [w for w in dict.fromkeys(wr) if w != right][:3],
             "log<sub><i>b</i></sub> <i>x</i> = <i>y</i> means <i>b</i><sup><i>y</i></sup> = <i>x</i>. <b>%s</b>." % right)


# ------------------------------------------------------------ set 2: evaluate
def one_eval(r):
    kind = r.choice(["int", "int", "frac", "ten", "ln", "root"])
    if kind in ("int", "frac"):
        b = r.choice([2, 3, 4, 5, 7])
        k = r.randint(2, 5) if kind == "int" else -r.randint(1, 3)
        v = F(b) ** k
        if v.numerator > 3000:
            return None
        q = "Evaluate %s." % B(lg(b, sf(v)))
        wr = [F(v.numerator if v.denominator == 1 else v.denominator, b), -k, F(1, k) if k else 1, k + 1]
        return T(q, sf(k), [sf(w) for w in dict.fromkeys(wr) if w != k][:3],
                 "Ask: %d to what power is %s? %d<sup>%s</sup> = %s, so the answer is <b>%s</b>." % (b, sf(v), b, sf(k), sf(v), sf(k)))
    if kind == "ten":
        k = r.choice([-3, -2, -1, 2, 3, 4, 5, 6])
        v = F(10) ** k
        q = "Evaluate %s." % B(lg(10, sf(v) if k > 0 else ("0." + "0" * (-k - 1) + "1")))
        return T(q, sf(k), [sf(w) for w in dict.fromkeys([abs(k) + 1 if k > 0 else -k, F(1, abs(k)), 10 * k, -k]) if w != k][:3],
                 "log means base 10. 10<sup>%s</sup> = that number, so the answer is <b>%s</b>." % (sf(k), sf(k)))
    if kind == "ln":
        k = r.choice([2, 3, 4, 5, -1, -2, F(1, 2)])
        q = "Evaluate %s." % B(lg("e", "<i>e</i><sup>%s</sup>" % sf(k)))
        return T(q, sf(k), [sf(w) for w in dict.fromkeys([-F(k), F(k) + 1, 2 * F(k), F(0)]) if w != F(k)][:3],
                 "ln is log base <i>e</i>, and ln <i>e</i><sup><i>k</i></sup> = <i>k</i>. <b>%s</b>." % sf(k))
    b = r.choice([2, 3, 4, 5, 8, 9])
    n = r.choice([2, 3])
    q = "Evaluate %s." % B(lg(b, ("√%d" if n == 2 else "∛%d") % b))
    return T(q, fr(1, n), [num(n), sf(F(b, n)), MINUS + num(n)],
             "%s = %d<sup>1/%d</sup>, so the logarithm is <b>1/%d</b>." % (("√%d" if n == 2 else "∛%d") % b, b, n, n))


# ------------------------------------------------------------ set 3: expand
def one_exp(r):
    b = r.choice([2, 3, 5, 10, "e"])
    kind = r.choice(["prod", "quot", "pow", "mix", "mix"])
    x, y, z = "<i>x</i>", "<i>y</i>", "<i>z</i>"
    if kind == "prod":
        k = r.choice([3, 5, 7, 8])
        q = "Expand %s." % B(lg(b, "%d%s" % (k, x)))
        right = "%s + %s" % (lg(b, str(k)), lg(b, x))
        wr = ["%s · %s" % (lg(b, str(k)), lg(b, x)), "%d %s" % (k, lg(b, x)), "%s %s %s" % (lg(b, str(k)), MINUS, lg(b, x))]
        e = "Product property: the log of a product is the sum of the logs."
    elif kind == "quot":
        q = "Expand %s." % B(lg(b, fr(x, y)))
        right = "%s %s %s" % (lg(b, x), MINUS, lg(b, y))
        wr = ["%s ÷ %s" % (lg(b, x), lg(b, y)), "%s + %s" % (lg(b, x), lg(b, y)), "%s %s %s" % (lg(b, y), MINUS, lg(b, x))]
        e = "Quotient property: the log of a quotient is the difference of the logs, top minus bottom."
    elif kind == "pow":
        p = r.choice([2, 3, 4, 5])
        q = "Expand %s." % B(lg(b, "%s<sup>%d</sup>" % (x, p)))
        right = "%d %s" % (p, lg(b, x))
        wr = ["(%s)<sup>%d</sup>" % (lg(b, x), p), "%s + %d" % (lg(b, x), p), "%s" % lg(b, "%d%s" % (p, x))]
        e = "Power property: bring the exponent to the front as a multiplier."
    else:
        p, m = r.choice([2, 3, 4]), r.choice([2, 3, 5])
        q = "Expand %s." % B(lg(b, fr("%s<sup>%d</sup>%s" % (x, p, y), z + ("<sup>%d</sup>" % m if m > 1 else ""))))
        right = "%d %s + %s %s %d %s" % (p, lg(b, x), lg(b, y), MINUS, m, lg(b, z))
        wr = ["%d %s + %s + %d %s" % (p, lg(b, x), lg(b, y), m, lg(b, z)), "%d %s · %s %s %d %s" % (p, lg(b, x), lg(b, y), MINUS, m, lg(b, z)),
              "%d(%s + %s) %s %d %s" % (p, lg(b, x), lg(b, y), MINUS, m, lg(b, z))]
        e = "Product (add) for the top, quotient (subtract) for the bottom, and power (bring exponents to the front)."
    return T(q, right, wr, e + " <b>%s</b>." % right)


# ------------------------------------------------------------ set 4: condense and simplify
def one_cond(r):
    kind = r.choice(["num", "num", "num", "var"])
    if kind == "num":
        b = r.choice([2, 3, 5, 10])
        op = r.choice(["+", MINUS, "pow"])
        if op == "+":
            k = r.randint(2, 5)
            m = r.choice([d for d in range(2, 9)])
            n = b ** k
            if n % m:
                return None
            q = "Simplify %s." % B("%s + %s" % (lg(b, str(m)), lg(b, num(n // m))))
            return T(q, sf(k), [sf(w) for w in dict.fromkeys([F(n, b), k + 1, m + n // m if m + n // m < 99 else k - 1]) if w != k][:3],
                     "Product property: %s = %s = <b>%d</b>." % (lg(b, "(%d × %s)" % (m, num(n // m))), lg(b, num(n)), k))
        if op == MINUS:
            k = r.randint(1, 3)
            m = r.choice([2, 3, 4, 5, 6, 7])
            q = "Simplify %s." % B("%s %s %s" % (lg(b, num(m * b ** k)), MINUS, lg(b, num(m))))
            return T(q, sf(k), [sf(w) for w in dict.fromkeys([F(m * b ** k - m), F(1, k) if k > 1 else 2, k + 1, F(b ** k)]) if w != k][:3],
                     "Quotient property: %s = %s = <b>%d</b>." % (lg(b, fr(num(m * b ** k), num(m))), lg(b, num(b ** k)), k))
        k = r.choice([2, 3])
        base = r.choice([2, 3, 4, 5])
        n = base ** k
        if b == base:
            return None
        q = "Write %s as a single logarithm." % B("%d %s" % (k, lg(b, str(base))))
        right = lg(b, num(n))
        return T(q, right, [lg(b, num(base * k)), lg(b, num(k ** base)), "(%s)<sup>%d</sup>" % (lg(b, str(base)), k)],
                 "Power property in reverse: %d %s = %s = <b>%s</b>." % (k, lg(b, str(base)), lg(b, "%d<sup>%d</sup>" % (base, k)), right))
    b = r.choice([2, 3, 10, "e"])
    p, m = r.choice([2, 3]), r.choice([2, 3, 4])
    q = "Write as a single logarithm: %s." % B("%d %s + %s %s %d %s" % (p, lg(b, "<i>x</i>"), lg(b, "<i>y</i>"), MINUS, m, lg(b, "<i>z</i>")))
    right = lg(b, fr("<i>x</i><sup>%d</sup><i>y</i>" % p, "<i>z</i><sup>%d</sup>" % m))
    return T(q, right, [lg(b, fr("<i>x</i><sup>%d</sup><i>y</i><i>z</i><sup>%d</sup>" % (p, m), "1")), lg(b, fr("%d<i>xy</i>" % p, "%d<i>z</i>" % m)), lg(b, "(<i>x</i><sup>%d</sup> + <i>y</i> %s <i>z</i><sup>%d</sup>)" % (p, MINUS, m))],
             "Move the multipliers up as exponents, then add means multiply and subtract means divide. <b>%s</b>." % right)


# ------------------------------------------------------------ set 5: change of base and domain
def one_cob(r):
    kind = r.choice(["calc", "calc", "rewrite", "domain", "inverse"])
    if kind == "calc":
        b = r.choice([2, 3, 5, 6, 7])
        x = r.choice([10, 20, 30, 50, 75, 100, 15])
        val = math.log(x) / math.log(b)
        right = "%.3f" % val
        q = "Use the change-of-base formula to find %s to the nearest thousandth." % B(lg(b, num(x)))
        return T(q, right, ["%.3f" % (math.log(b) / math.log(x)), "%.3f" % math.log10(x / b), "%.3f" % (math.log10(x) - math.log10(b))],
                 "%s = log %d ÷ log %d = %.4f ÷ %.4f ≈ <b>%s</b>. (Dividing is not the same as subtracting the logs.)" % (lg(b, num(x)), x, b, math.log10(x), math.log10(b), right))
    if kind == "rewrite":
        b, x = r.choice([(2, 9), (3, 20), (5, 12), (7, 40), (4, 11)])
        q = "Which expression equals %s?" % B(lg(b, str(x)))
        right = fr("ln %d" % x, "ln %d" % b)
        return T(q, right, [fr("ln %d" % b, "ln %d" % x), "ln %d %s ln %d" % (x, MINUS, b), "ln %s" % fr(str(x), str(b))],
                 "Change of base: log<sub><i>b</i></sub> <i>x</i> = (ln <i>x</i>) ÷ (ln <i>b</i>). <b>%s</b>." % right)
    if kind == "domain":
        h = r.choice([x for x in range(-6, 7) if x])
        b = r.choice([2, 3, 10])
        q = "What is the domain of %s?" % B("<i>f</i>(<i>x</i>) = " + lg(b, "(<i>x</i> %s %d)" % (MINUS if h > 0 else "+", abs(h))))
        right = "<i>x</i> &gt; %s" % sf(h)
        return T(q, right, ["<i>x</i> &gt; %s" % sf(-h), "<i>x</i> ≥ %s" % sf(h), "All real numbers"],
                 "You can only take the log of a positive number: <i>x</i> %s %d &gt; 0. <b>%s</b>. The graph has a vertical asymptote at <i>x</i> = %s." % (MINUS if h > 0 else "+", abs(h), right, sf(h)))
    b = r.choice([2, 3, 4, 5, 10])
    q = "What is the inverse of %s?" % B("<i>f</i>(<i>x</i>) = %d<sup><i>x</i></sup>" % b)
    right = "<i>f</i><sup>%s1</sup>(<i>x</i>) = %s" % (MINUS, lg(b, "<i>x</i>"))
    return T(q, right, ["<i>f</i><sup>%s1</sup>(<i>x</i>) = %s" % (MINUS, lg("<i>x</i>", str(b))), "<i>f</i><sup>%s1</sup>(<i>x</i>) = <i>x</i><sup>%d</sup>" % (MINUS, b),
                        "<i>f</i><sup>%s1</sup>(<i>x</i>) = %d<sup>%s<i>x</i></sup>" % (MINUS, b, MINUS)],
             "Swap <i>x</i> and <i>y</i>: <i>x</i> = %d<sup><i>y</i></sup>. In log form, <i>y</i> = %s. <b>%s</b>." % (b, lg(b, "<i>x</i>"), right))


def build():
    sets = [S("Exponential and logarithmic form", collect(one_conv, 20, R)),
            S("Evaluate logarithms", collect(one_eval, 20, R)),
            S("Expand logarithms", collect(one_exp, 20, R)),
            S("Condense and simplify", collect(one_cond, 20, R)),
            S("Change of base, domain and inverses", collect(one_cob, 20, R))]
    body = lesson(
        "<p>A logarithm is an exponent: <b>log<sub><i>b</i></sub> <i>x</i> = <i>y</i></b> means <b><i>b</i><sup><i>y</i></sup> = <i>x</i></b>. "
        "log means base 10, and ln means base <i>e</i>. Logarithms are the inverses of exponential functions.</p>"
        "<ul><li>Product: log<sub><i>b</i></sub>(<i>MN</i>) = log<sub><i>b</i></sub> <i>M</i> + log<sub><i>b</i></sub> <i>N</i></li>"
        "<li>Quotient: log<sub><i>b</i></sub>(<i>M</i>/<i>N</i>) = log<sub><i>b</i></sub> <i>M</i> %s log<sub><i>b</i></sub> <i>N</i></li>"
        "<li>Power: log<sub><i>b</i></sub>(<i>M</i><sup><i>p</i></sup>) = <i>p</i> log<sub><i>b</i></sub> <i>M</i></li>"
        "<li>Change of base: log<sub><i>b</i></sub> <i>x</i> = (log <i>x</i>) ÷ (log <i>b</i>)</li></ul>" % MINUS,
        [("Evaluate log<sub>2</sub> 32.", ["2 to what power is 32?", "2<sup>5</sup> = 32"], "5"),
         ("Expand log<sub>3</sub>(<i>x</i>²<i>y</i>/<i>z</i>).", ["Add for the top, subtract for the bottom, exponents in front"], "2 log<sub>3</sub> <i>x</i> + log<sub>3</sub> <i>y</i> %s log<sub>3</sub> <i>z</i>" % MINUS)],
        ["Swapping the base and the exponent when converting forms.",
         "Writing log(<i>M</i> + <i>N</i>) as log <i>M</i> + log <i>N</i>. The product property is for log(<i>MN</i>).",
         "Writing log <i>M</i> ÷ log <i>N</i> for log(<i>M</i>/<i>N</i>). It is a difference.",
         "Taking the log of 0 or a negative number. The argument must be positive."])
    faq = [("What is a logarithm?", "A logarithm is an exponent. log_b(x) = y means b^y = x, so log_2(8) = 3 because 2³ = 8."),
           ("What are the properties of logarithms?", "Product: log(MN) = log M + log N. Quotient: log(M/N) = log M − log N. Power: log(M^p) = p log M."),
           ("What is the change-of-base formula?", "log_b(x) = log(x)/log(b) = ln(x)/ln(b). It lets you evaluate any logarithm on a calculator."),
           ("What is the difference between log and ln?", "log usually means base 10 (the common logarithm), and ln means base e (the natural logarithm).")]
    make("logarithms-and-their-properties", 10, "F-LE.A.4",
         "Logarithms and Their Properties",
         "Logarithms Worksheet: Evaluating, Expanding, Condensing, Change of Base (Algebra 2) | 100 Questions",
         "Logarithms",
         "For exponential models, express as a logarithm the solution to ab^(ct) = d where a, c, and d are numbers and the base b is 2, 10, or e; evaluate the logarithm using technology.",
         "Free Algebra 2 worksheet on logarithms: converting forms, evaluating logs, expanding and condensing with log properties, change of base and domain. 100 questions with answers.",
         "A logarithm is an exponent: log_b x = y means b^y = x.",
         "log(MN) = log M + log N, log(M/N) = log M − log N, log(M^p) = p log M.",
         body, faq, sets, R, domain="Exponential and Logarithmic Functions", grade="algebra-2")


if __name__ == "__main__":
    build()
