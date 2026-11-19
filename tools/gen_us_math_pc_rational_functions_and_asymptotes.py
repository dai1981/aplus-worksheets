# -*- coding: utf-8 -*-
"""
US Precalculus: Rational Functions and Asymptotes (Common Core F-IF.C.7d, A-APR.D.6)
  python3 tools/gen_us_math_pc_rational_functions_and_asymptotes.py
Vertical asymptotes and holes, horizontal and slant asymptotes, intercepts and domain, matching graphs to
equations, and models such as average cost and mixing.
Wrong answers come from real mistakes: calling a cancelled factor an asymptote, using the zeros of the
numerator, comparing the wrong coefficients for the horizontal asymptote, and flipping the sign of a shift.
"""
import random
from fractions import Fraction as F
from us_hs import B, S, make, lesson, collect, T, fig, num, MINUS, People, usd
from a2_common import sf, ps, poly, lin, pmul, synth, X
from pc_common import GRADE, curve_svg

R = random.Random(97101)
Y = "<i>y</i>"


def fx(n, d):
    return "<i>f</i>(%s) = %s" % (X, "<span class='fr'><span class='fn'>%s</span><span class='fd'>%s</span></span>" % (n, d))


def xeq(vs):
    vs = sorted(vs)
    return " and ".join("%s = %s" % (X, sf(v)) for v in vs)


def fact(zs):
    return "".join("(%s)" % lin(z) for z in zs)


# ------------------------------------------------------------ set 1: vertical asymptotes and holes
def one_va(r):
    a, b = r.sample([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5], 2)
    kind = r.choice(["va", "va", "hole", "hole"])
    show_fact = r.random() < 0.5
    den = fact([a, b]) if show_fact else poly(pmul([1, -a], [1, -b]))
    if kind == "va":
        c = r.choice([z for z in range(-6, 7) if z not in (a, b)])
        num_ = lin(c) if show_fact else lin(c)
        q = "What are the vertical asymptotes of %s?" % fx(num_, den)
        right = xeq([a, b])
        return T(q, right, [xeq([-a, -b]), xeq([c]) if c else "%s = 0" % X, xeq([a, c]) if c != b else xeq([b])],
                 "The denominator is %s, which is 0 at %s = %s and %s = %s. The numerator is not 0 there, so the asymptotes are <b>%s</b>." % (fact([a, b]), X, sf(a), X, sf(b), right))
    num_ = lin(a)
    den = fact([a, b]) if show_fact else poly(pmul([1, -a], [1, -b]))
    which = r.choice(["hole", "va"])
    yv = F(1, a - b)
    if which == "hole":
        q = "Where is the hole in the graph of %s?" % fx(num_, den)
        right = "(%s, %s)" % (sf(a), sf(yv))
        return T(q, right, ["(%s, %s)" % (sf(b), sf(yv)), "(%s, 0)" % sf(a), "(%s, %s)" % (sf(-a), sf(yv)), "There is no hole"],
                 "(%s) cancels, so there is a hole at %s = %s. The simplified function is 1/(%s); at %s = %s it is %s. The hole is <b>%s</b>." % (lin(a), X, sf(a), lin(b), X, sf(a), sf(yv), right))
    q = "What are the vertical asymptotes of %s?" % fx(num_, den)
    right = xeq([b])
    return T(q, right, [xeq([a, b]), xeq([a]), xeq([-b])],
             "(%s) cancels, so %s = %s is a hole, not an asymptote. Only <b>%s</b> is a vertical asymptote." % (lin(a), X, sf(a), right))


# ------------------------------------------------------------ set 2: horizontal and slant asymptotes
def one_ha(r):
    kind = r.choice(["lower", "same", "same", "slant", "slant"])
    if kind == "lower":
        p = r.choice([2, 3, 5, -4])
        c = r.choice([1, -3, 7])
        d2 = [r.choice([1, 2, 3]), r.choice([0, 2, -1]), r.choice([-4, 5, 6])]
        q = "What is the horizontal asymptote of %s?" % fx(poly([p, c]), poly(d2))
        right = "%s = 0" % Y
        return T(q, right, ["%s = %s" % (Y, sf(F(p, d2[0]))), "%s = %s" % (Y, sf(F(c, d2[2]))), "There is no horizontal asymptote"],
                 "The degree of the numerator (1) is less than the degree of the denominator (2), so the asymptote is <b>%s</b>." % right)
    if kind == "same":
        p = r.choice([1, 2, 3, 4, -2, 6])
        qd = r.choice([1, 2, 3, 5])
        if F(p, qd) == 1 and r.random() < 0.5:
            return None
        deg = r.choice([1, 2])
        if deg == 1:
            n_, d_ = [p, r.choice([-5, 3, 1])], [qd, r.choice([-2, 4, 7])]
        else:
            n_, d_ = [p, 0, r.choice([-5, 3])], [qd, r.choice([1, -3]), r.choice([-2, 4])]
        if n_[-1] * qd == d_[-1] * p:
            return None
        q = "What is the horizontal asymptote of %s?" % fx(poly(n_), poly(d_))
        right = "%s = %s" % (Y, sf(F(p, qd)))
        return T(q, right, ["%s = 0" % Y, "%s = %s" % (Y, sf(F(n_[-1], d_[-1]))), "%s = %s" % (Y, sf(F(qd, p))) if F(qd, p) != F(p, qd) else "There is no horizontal asymptote"],
                 "The degrees are equal, so divide the leading coefficients: %s ÷ %s, so <b>%s</b>." % (sf(p), sf(qd), right))
    a = r.choice([-3, -2, -1, 1, 2, 3, 4])
    b = r.choice([-4, -2, 1, 3, 5])
    c = r.choice([-6, -1, 2, 7])
    qt, rem = synth([1, b, c], a)
    if rem == 0:
        return None
    q = "What is the slant asymptote of %s?" % fx(poly([1, b, c]), lin(a))
    right = "%s = %s" % (Y, poly(qt))
    return T(q, right, ["%s = %s" % (Y, poly([1, b])), "%s = %s" % (Y, poly([1, b - a])) if b - a != b + a else "%s = %s" % (Y, X), "%s = 1" % Y],
             "The numerator's degree is one more than the denominator's, so divide: (%s) ÷ (%s) = %s with remainder %s. The slant asymptote is <b>%s</b>." % (poly([1, b, c]), lin(a), poly(qt), sf(rem), right))


# ------------------------------------------------------------ set 3: intercepts and domain
def one_int(r):
    a, b, c = r.sample([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5], 3)
    k = r.choice([1, 2, 3])
    n_ = [k * t for t in [1, -c]]
    den = fact([a, b])
    want = r.choice(["x", "y", "dom", "dom"])
    numh = (sf(k) if k != 1 else "") + "(%s)" % lin(c) if k != 1 else lin(c)
    if want == "x":
        q = "What is the <i>x</i>-intercept of %s?" % fx(numh, den)
        right = "(%s, 0)" % sf(c)
        return T(q, right, ["(%s, 0)" % sf(-c), "(%s, 0)" % sf(a), "(0, %s)" % sf(c)],
                 "The graph crosses the <i>x</i>-axis where the numerator is 0: %s = %s. The <i>x</i>-intercept is <b>%s</b>." % (X, sf(c), right))
    if want == "y":
        yv = F(-k * c, a * b)
        q = "What is the <i>y</i>-intercept of %s?" % fx(numh, den)
        right = "(0, %s)" % sf(yv)
        return T(q, right, ["(0, %s)" % sf(-yv), "(0, %s)" % sf(F(k * c, 1)) if F(k * c) != abs(yv) else "(0, %s)" % sf(yv + 1), "(0, %s)" % sf(F(-k * c, a + b)) if a + b else "(0, 0)"],
                 "Put %s = 0: %s ÷ ((%s)(%s)) = %s ÷ %s = %s. The <i>y</i>-intercept is <b>%s</b>." % (X, sf(-k * c), sf(-a), sf(-b), sf(-k * c), ps(a * b), sf(yv), right))
    q = "What is the domain of %s?" % fx(numh, den)
    right = "All real numbers except %s" % xeq([a, b])
    return T(q, right, ["All real numbers except %s" % xeq([c]), "All real numbers except %s" % xeq([-a, -b]), "All real numbers"],
             "The denominator cannot be 0, so leave out %s = %s and %s = %s. <b>%s</b>." % (X, sf(a), X, sf(b), right))


# ------------------------------------------------------------ set 4: graphs
def eq_simple(a, h, k):
    n = "%s" % sf(a)
    s = "<i>f</i>(%s) = <span class='fr'><span class='fn'>%s</span><span class='fd'>%s</span></span>" % (X, n, lin(h))
    if k:
        s += " %s %s" % ("+" if k > 0 else MINUS, num(abs(k)))
    return s


def one_graph(r):
    a = r.choice([1, 2, 3, -1, -2, -3])
    h = r.choice([-3, -2, -1, 1, 2, 3])
    k = r.choice([-3, -2, -1, 0, 1, 2, 3])
    svg = curve_svg(lambda x: None if abs(x - h) < 1e-9 else a / (x - h) + k, -6, 6, -6, 6, 20,
                    vasym=[h], hasym=[k], label="graph of a rational function with dashed asymptotes")
    want = r.choice(["eq", "eq", "va", "ha"])
    if want == "eq":
        q = "Which function matches the graph? The dashed lines are asymptotes." + fig(svg)
        right = eq_simple(a, h, k)
        return T(q, right, [eq_simple(a, -h, k), eq_simple(-a, h, k), eq_simple(a, k, h) if h != k else eq_simple(a, -h, -k)],
                 "The vertical asymptote is %s = %s, so the denominator is %s. The horizontal asymptote is %s = %s. The graph is in the %s, so <i>a</i> is %s. <b>%s</b>." % (
                     X, sf(h), lin(h), Y, sf(k), "upper right and lower left" if a > 0 else "upper left and lower right", "positive" if a > 0 else "negative", right))
    if want == "va":
        q = "What is the vertical asymptote of the graph shown?" + fig(svg)
        right = "%s = %s" % (X, sf(h))
        return T(q, right, ["%s = %s" % (Y, sf(h)), "%s = %s" % (X, sf(-h)), "%s = %s" % (X, sf(k)) if k != h else "%s = %s" % (X, sf(h + 1))],
                 "The graph runs up or down along the dashed vertical line <b>%s</b>." % right)
    q = "What is the horizontal asymptote of the graph shown?" + fig(svg)
    right = "%s = %s" % (Y, sf(k))
    return T(q, right, ["%s = %s" % (X, sf(k)), "%s = %s" % (Y, sf(-k)) if k else "%s = %s" % (Y, sf(a)), "%s = %s" % (Y, sf(h)) if h != k else "%s = %s" % (Y, sf(k + 1))],
             "Far to the left and right, the graph levels off at the dashed line <b>%s</b>." % right)


# ------------------------------------------------------------ set 5: word problems
def one_word(r):
    pp = People(r)
    nm, he, his = pp.next()
    kind = r.choice(["cost", "cost", "limit", "mix", "mix", "drug"])
    if kind == "cost":
        fixed = r.choice([600, 1200, 2400, 900, 1500])
        c = r.choice([2, 3, 4, 5, 8])
        n = r.choice([100, 150, 200, 300, 400, 600])
        avg = F(fixed + c * n, n)
        if avg.denominator not in (1, 2, 4, 5, 10, 20, 25, 50, 100):
            return None
        q = ("%s starts a T-shirt business. Setup costs %s, and each shirt costs %s to make. The average cost per shirt is "
             "<i>A</i>(<i>x</i>) = (%s + %s<i>x</i>) / <i>x</i>. What is the average cost when %s makes %s shirts?" % (nm, usd(fixed), usd(c), num(fixed), num(c), he, num(n)))
        right = usd(avg)
        return T(q, right, [usd(c), usd(F(fixed, n)), usd(fixed + c * n)],
                 "<i>A</i>(%s) = (%s + %s) ÷ %s = %s ÷ %s = <b>%s</b>." % (num(n), num(fixed), num(c * n), num(n), num(fixed + c * n), num(n), right))
    if kind == "limit":
        fixed = r.choice([800, 2000, 5000])
        c = r.choice([3, 6, 12])
        q = ("A printer charges %s to set up and %s per poster. The average cost per poster is <i>A</i>(<i>x</i>) = (%s + %s<i>x</i>) / <i>x</i>. "
             "What value does the average cost approach as the number of posters gets very large?" % (usd(fixed), usd(c), num(fixed), num(c)))
        right = usd(c)
        return T(q, right, [usd(0), usd(fixed), usd(fixed + c)],
                 "The horizontal asymptote is <i>y</i> = %s ÷ 1 = %s: the setup cost is shared by more and more posters. <b>%s</b>." % (num(c), num(c), right))
    if kind == "mix":
        v0 = r.choice([20, 40, 50, 100])
        s0 = r.choice([5, 10, 20])
        rate = r.choice([2, 4, 5])
        conc = r.choice([F(1, 2), 1, 2, F(3, 2)])
        if r.random() < 0.5:
            q = ("A tank holds %s L of water with %s g of salt. Salt water with %s g of salt per liter flows in at %s L per minute. "
                 "The concentration after <i>t</i> minutes is <i>C</i>(<i>t</i>) = (%s + %s<i>t</i>) / (%s + %s<i>t</i>) grams per liter. "
                 "What concentration does the tank approach over time?" % (num(v0), num(s0), num(conc), num(rate), num(s0), num(conc * rate), num(v0), num(rate)))
            right = "%s g per liter" % num(conc)
            return T(q, right, ["%s g per liter" % num(F(s0, v0)) if F(s0, v0) != conc else "0 g per liter", "%s g per liter" % num(conc * rate), "%s g per liter" % num(rate) if rate != conc else "%s g per liter" % num(conc + 1)],
                     "Compare the leading coefficients: %s ÷ %s = %s. Over time the tank fills with the incoming mixture. <b>%s</b>." % (num(conc * rate), num(rate), num(conc), right))
        t = r.choice([5, 10, 20, 30])
        cval = F(s0 + conc * rate * t, v0 + rate * t)
        if cval.denominator not in (1, 2, 4, 5, 10, 20, 25, 50, 100):
            return None
        q = ("A tank holds %s L of water with %s g of salt. Salt water with %s g of salt per liter flows in at %s L per minute, so "
             "<i>C</i>(<i>t</i>) = (%s + %s<i>t</i>) / (%s + %s<i>t</i>). What is the concentration after %s minutes?" % (num(v0), num(s0), num(conc), num(rate), num(s0), num(conc * rate), num(v0), num(rate), num(t)))
        right = "%s g per liter" % num(cval)
        return T(q, right, ["%s g per liter" % num(conc) if conc != cval else "%s g per liter" % num(cval * 2), "%s g per liter" % num(F(s0 + conc * rate * t, v0)), "%s g per liter" % num(s0 + conc * rate * t)],
                 "<i>C</i>(%s) = (%s + %s) ÷ (%s + %s) = %s ÷ %s = <b>%s</b>." % (num(t), num(s0), num(conc * rate * t), num(v0), num(rate * t), num(s0 + conc * rate * t), num(v0 + rate * t), right))
    a = r.choice([20, 30, 40, 50])
    b = r.choice([4, 9, 16, 25])
    t = r.choice([1, 2, 3, 4, 5])
    cv = F(a * t, t * t + b)
    if cv.denominator not in (1, 2, 4, 5, 10, 20, 25, 50):
        return None
    q = ("The amount of a medicine in the blood <i>t</i> hours after a dose is <i>C</i>(<i>t</i>) = %s<i>t</i> / (<i>t</i>² + %s) mg per liter. "
         "What is <i>C</i>(%s)%s?" % (num(a), num(b), num(t), "" if r.random() < 0.6 else ", and what happens to C in the long run"))
    if q.endswith("long run?"):
        right = "%s mg per liter, and it approaches 0" % num(cv)
        return T(q, right, ["%s mg per liter, and it approaches %s" % (num(cv), num(a)), "%s mg per liter, and it approaches 0" % (num(F(a * t, t + b)) or num(F(a * t, t + b), "f")) if F(a * t, t + b) != cv else "%s mg per liter, and it approaches 0" % num(cv + 1),
                            "%s mg per liter, and it keeps growing" % num(cv)],
                 "<i>C</i>(%s) = %s ÷ %s = %s. The denominator has the higher degree, so the horizontal asymptote is <i>y</i> = 0. <b>%s</b>." % (num(t), num(a * t), num(t * t + b), num(cv), right))
    right = "%s mg per liter" % num(cv)
    return T(q, right, ["%s mg per liter" % (num(F(a * t, t + b)) or num(F(a * t, t + b), "f")) if F(a * t, t + b) != cv else "%s mg per liter" % num(cv + 2), "%s mg per liter" % (num(F(a, t * t + b) if F(a, t * t + b) != cv else cv + 1) or num(F(a, t * t + b), "f")), "%s mg per liter" % num(a * t)],
             "<i>C</i>(%s) = %s × %s ÷ (%s² + %s) = %s ÷ %s = <b>%s</b>." % (num(t), num(a), num(t), num(t), num(b), num(a * t), num(t * t + b), right))


def build():
    sets = [S("Vertical asymptotes and holes", collect(one_va, 20, R)),
            S("Horizontal and slant asymptotes", collect(one_ha, 20, R)),
            S("Intercepts and domain", collect(one_int, 20, R)),
            S("Graphs of rational functions", collect(one_graph, 20, R)),
            S("Word problems", collect(one_word, 20, R))]
    body = lesson(
        "<ul><li>Factor the numerator and denominator first. A factor that <b>cancels</b> makes a <b>hole</b>. A zero of the denominator that does not cancel is a <b>vertical asymptote</b>.</li>"
        "<li><b>Horizontal asymptote</b>: compare degrees. Top degree smaller: <i>y</i> = 0. Equal degrees: <i>y</i> = ratio of the leading coefficients. Top degree one larger: a <b>slant asymptote</b> from division.</li>"
        "<li><i>x</i>-intercepts come from the zeros of the numerator; the <i>y</i>-intercept is <i>f</i>(0).</li>"
        "<li>For <i>f</i>(<i>x</i>) = <i>a</i>/(<i>x</i> − <i>h</i>) + <i>k</i>, the asymptotes are <i>x</i> = <i>h</i> and <i>y</i> = <i>k</i>.</li></ul>",
        [("Find the asymptotes and holes of " + fx("(%s)(%s)" % (lin(2), lin(-1)), "(%s)(%s)" % (lin(2), lin(3))) + ".",
          ["(%s) cancels: hole at %s = 2" % (lin(2), X), "Vertical asymptote: %s = 3" % X, "Degrees are equal: %s = 1 ÷ 1 = 1" % Y],
          "hole at %s = 2, %s = 3, %s = 1" % (X, X, Y)),
         ("Find the slant asymptote of " + fx(poly([1, 3, 1]), lin(1)) + ".", ["Divide: %s ÷ (%s) = %s, remainder 5" % (poly([1, 3, 1]), lin(1), poly([1, 4]))], "%s = %s" % (Y, poly([1, 4])))],
        ["Calling a cancelled factor an asymptote. It is a hole.",
         "Using the zeros of the numerator as vertical asymptotes. They are <i>x</i>-intercepts.",
         "Using the constant terms for the horizontal asymptote. Use the leading coefficients.",
         "Shifting the wrong way: <i>x</i> − 3 in the denominator gives the asymptote <i>x</i> = 3, not −3."])
    faq = [("How do you find the vertical asymptotes of a rational function?", "Factor and cancel common factors. The zeros of the denominator that remain are vertical asymptotes; cancelled factors give holes."),
           ("How do you find the horizontal asymptote?", "Compare degrees. If the numerator has the lower degree, it is y = 0. If the degrees are equal, divide the leading coefficients. If the numerator's degree is one higher, there is a slant asymptote instead."),
           ("What is a hole in a graph?", "A single missing point where a factor cancels from the numerator and denominator."),
           ("What does a horizontal asymptote mean in a real problem?", "It is the long-run value, such as the average cost per item approaching the cost to make one item.")]
    make("rational-functions-and-asymptotes", 1, "F-IF.C.7d",
         "Rational Functions and Asymptotes",
         "Rational Functions and Asymptotes Worksheet (Precalculus) | 100 Questions with Answers",
         "Rational Functions",
         "Graph rational functions, identifying zeros and asymptotes when suitable factorizations are available, and showing end behavior.",
         "Free precalculus worksheet on rational functions: vertical, horizontal and slant asymptotes, holes, intercepts, domain, graphs and models. 100 questions with answers.",
         "Factor first: cancelled factors are holes, the rest of the denominator's zeros are asymptotes.",
         "Compare degrees to find the horizontal or slant asymptote.",
         body, faq, sets, R, domain="Rational Functions", grade=GRADE)


if __name__ == "__main__":
    build()
