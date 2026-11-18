# -*- coding: utf-8 -*-
"""
US Algebra 2: Polynomial Functions, Zeros, and End Behavior (Common Core A-APR.B.3, F-IF.C.7c, N-CN.C.9)
  python3 tools/gen_us_math_a2_polynomial_functions_and_zeros.py
Degree, leading coefficient and end behavior; zeros and multiplicity from factored form; writing a polynomial
from its zeros; matching graphs to equations; the Rational Root Theorem and the number of zeros.
Wrong answers come from real mistakes: reading the zero of (x + 3) as 3, judging end behavior from the
constant term, ignoring multiplicity, and forgetting the conjugate of a complex zero.
"""
import random
from fractions import Fraction as F
from us_hs import B, S, make, lesson, collect, T, fig, num, MINUS, fr
from g8_common import grid_svg
from a2_common import X, poly, sf, lin, pmul, peval
from us_geo import BLUE, RED

R = random.Random(95301)
UPUP = "Up on both ends"
DD = "Down on both ends"
DU = "Down on the left, up on the right"
UD = "Up on the left, down on the right"


def ends(lead, deg):
    if deg % 2 == 0:
        return UPUP if lead > 0 else DD
    return DU if lead > 0 else UD


def factored(lead, roots):
    """roots: list of (root, multiplicity)"""
    s = "" if lead == 1 else (MINUS if lead == -1 else num(lead))
    for z, m in roots:
        s += "(%s)%s" % (lin(z), "²" if m == 2 else ("³" if m == 3 else ""))
    return s


def expand(lead, roots):
    p = [lead]
    for z, m in roots:
        for _ in range(m):
            p = pmul(p, [1, -z])
    return p


def graph(p, lo=-6, hi=6, span=None):
    segs = []
    n = 300
    xs = [lo + (hi - lo) * i / n for i in range(n + 1)]
    f = lambda x: sum(float(c) * x ** (len(p) - 1 - i) for i, c in enumerate(p))
    k = 1.0
    if span:
        a, b = span
        m = max(abs(f(a + (b - a) * i / 100)) for i in range(101))
        k = 4.0 / m if m else 1.0
    pts = [(x, k * f(x)) for x in xs]
    for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
        if lo <= y1 <= hi and lo <= y2 <= hi:
            segs.append((x1, y1, x2, y2, BLUE))
    return grid_svg(lo, hi, segs=segs, unit=20, label="graph of a polynomial function")


# ------------------------------------------------------------ set 1: degree and end behavior
def one_end(r):
    deg = r.randint(2, 6)
    lead = r.choice([1, 2, 3, -1, -2, -4])
    cs = [lead] + [r.randint(-9, 9) for _ in range(deg)]
    kind = r.choice(["end", "end", "end", "deg"])
    order = list(range(deg + 1))
    shuffled = r.random() < 0.4
    from a2_common import xp
    from us_hs import expr
    terms = [(c, xp(deg - i)) for i, c in enumerate(cs)]
    if shuffled:
        r.shuffle(terms)
    shown = expr(terms)
    if kind == "deg":
        q = "What are the degree and the leading coefficient of %s?" % B("<i>f</i>(<i>x</i>) = " + shown)
        right = "Degree %d, leading coefficient %s" % (deg, sf(lead))
        first = terms[0]
        wr = ["Degree %d, leading coefficient %s" % (deg + 1, sf(lead)), "Degree %d, leading coefficient %s" % (deg, sf(cs[-1]) if cs[-1] != lead else sf(-lead)),
              "Degree %d, leading coefficient %s" % (deg, sf(first[0]) if first[0] != lead else sf(lead + 1))]
        return T(q, right, [w for w in dict.fromkeys(wr) if w != right][:3],
                 "The degree is the highest power (%d), and the leading coefficient is the number in front of it (%s), wherever it is written. <b>%s</b>." % (deg, sf(lead), right))
    q = "Describe the end behavior of %s." % B("<i>f</i>(<i>x</i>) = " + shown)
    right = ends(lead, deg)
    return T(q, right, [x for x in [UPUP, DD, DU, UD] if x != right],
             "Look only at the leading term %s<i>x</i>%s: the degree is %s and the leading coefficient is %s. <b>%s</b>." % (
                 sf(lead) if abs(lead) != 1 else (MINUS if lead < 0 else ""), {2: "²", 3: "³", 4: "⁴", 5: "⁵", 6: "⁶"}[deg],
                 "even" if deg % 2 == 0 else "odd", "positive" if lead > 0 else "negative", right))


# ------------------------------------------------------------ set 2: zeros and multiplicity
def one_zero(r):
    zs = r.sample([x for x in range(-6, 7) if x], 3)
    ms = [r.choice([1, 1, 2, 3]) for _ in zs]
    lead = r.choice([1, 1, 2, -1, 3])
    roots = list(zip(zs, ms))
    f = factored(lead, roots)
    kind = r.choice(["zeros", "zeros", "touch", "cross"])
    if kind == "zeros":
        q = "Find the zeros of %s." % B("<i>f</i>(<i>x</i>) = " + f)
        right = ", ".join(sf(z) for z in sorted(zs))
        return T(q, right, [", ".join(sf(-z) for z in sorted(zs, reverse=True)), ", ".join(sf(z) for z in sorted(zs)) + ", " + sf(lead) if lead != 1 else ", ".join(sf(abs(z)) for z in sorted(zs)),
                            ", ".join(sf(z) for z in sorted(zs)[:2])],
                 "Set each factor equal to 0. (%s) = 0 gives <i>x</i> = %s, and so on. <b>%s</b>." % (lin(zs[0]), sf(zs[0]), right))
    if all(m == ms[0] for m in ms) or not any(m == 2 for m in ms) and kind == "touch":
        return None
    if kind == "touch":
        z = [zz for zz, m in roots if m == 2][0]
        q = "At which zero does the graph of %s touch the <i>x</i>-axis and turn around, instead of crossing it?" % B("<i>f</i>(<i>x</i>) = " + f)
        right = "<i>x</i> = %s" % sf(z)
        return T(q, right, ["<i>x</i> = %s" % sf(x) for x in [zz for zz in zs if zz != z]] + ["<i>x</i> = %s" % sf(-z)],
                 "A factor with even multiplicity (squared) touches the axis and turns around. (%s)² gives <b>%s</b>." % (lin(z), right))
    m3 = [(zz, m) for zz, m in roots if m == 3]
    z, m = m3[0] if m3 else roots[0]
    q = "What is the multiplicity of the zero <i>x</i> = %s in %s, and does the graph cross or touch there?" % (sf(z), B("<i>f</i>(<i>x</i>) = " + f))
    right = "Multiplicity %d, %s" % (m, "crosses" if m % 2 else "touches")
    wr = ["Multiplicity %d, %s" % (m, "touches" if m % 2 else "crosses"), "Multiplicity %d, crosses" % (m + 1), "Multiplicity 1, crosses" if m != 1 else "Multiplicity 2, touches"]
    return T(q, right, [w for w in dict.fromkeys(wr) if w != right][:3],
             "The exponent on (%s) is %d. Odd multiplicity crosses the axis; even multiplicity touches. <b>%s</b>." % (lin(z), m, right))


# ------------------------------------------------------------ set 3: write the polynomial
def one_write(r):
    kind = r.choice(["real", "real", "complex", "complex"])
    if kind == "real":
        zs = r.sample([x for x in range(-5, 6) if x], 3)
        p = expand(1, [(z, 1) for z in zs])
        q = "Write the polynomial of least degree with leading coefficient 1 and zeros %s." % B(", ".join(sf(z) for z in sorted(zs)))
        right = poly(p)
        wr = [poly(expand(1, [(-z, 1) for z in zs])), poly(expand(1, [(zs[0], 1), (zs[1], 1), (-zs[2], 1)])), poly(expand(1, [(zs[0], 1), (zs[1], 1)]))]
        return T(q, right, [w for w in dict.fromkeys(wr) if w != right][:3],
                 "Each zero <i>a</i> gives a factor (<i>x</i> %s <i>a</i>): %s. Multiply out: <b>%s</b>." % (MINUS, factored(1, [(z, 1) for z in sorted(zs)]), right))
    a, b = r.randint(-4, 4), r.randint(1, 4)
    c = r.choice([x for x in range(-4, 5) if x])
    quad = [1, -2 * a, a * a + b * b]
    p = pmul(quad, [1, -c])
    z = "%s %s %s<i>i</i>" % (sf(a), "+", "" if b == 1 else num(b)) if a else "%s<i>i</i>" % ("" if b == 1 else num(b))
    q = "A cubic with real coefficients and leading coefficient 1 has zeros %s and %s. Write the polynomial." % (B(sf(c)), B(z))
    right = poly(p)
    wr = [poly(pmul([1, -2 * a, a * a - b * b], [1, -c])), poly(pmul([1, 2 * a, a * a + b * b], [1, -c])), poly(pmul(quad, [1, c]))]
    return T(q, right, [w for w in dict.fromkeys(wr) if w != right][:3],
             "Complex zeros come in conjugate pairs, so %s is also a zero. Those two give %s. Multiply by (%s): <b>%s</b>." % (
                 z.replace("+", MINUS), poly(quad), lin(c), right))


# ------------------------------------------------------------ set 4: match the graph
def one_graph(r):
    zs = sorted(r.sample([-5, -3, -1, 1, 3, 5], 3))
    if r.random() < 0.5:
        zs = sorted(r.sample([-4, -2, 0, 2, 4], 3))
        if 0 in zs:
            return None
    lead = r.choice([F(1, 2), F(-1, 2), F(1, 3), F(-1, 3)])
    mult = r.choice([None, 0, 1, 2])
    roots = [(z, 2 if i == mult else 1) for i, z in enumerate(zs)]
    if mult is not None:
        roots = [(z, m) for z, m in roots]
    p = expand(lead, roots)
    svg = graph(p, span=(zs[0], zs[-1]))
    sign = "" if lead > 0 else MINUS
    def fz(rs, s=sign):
        return "<i>y</i> = %s%s" % (s, "".join("(%s)%s" % (lin(z), "²" if m == 2 else "") for z, m in rs))
    right = fz(roots)
    wr = [fz([(-z, m) for z, m in roots]), fz(roots, "" if lead < 0 else MINUS),
          fz([(z, 1) for z, m in roots]) if mult is not None else fz([(z, 2 if i == 0 else 1) for i, (z, m) in enumerate(roots)])]
    q = "Which equation could match the graph? (Each answer may also have a positive constant factor.)%s" % fig(svg)
    return T(q, right, [w for w in dict.fromkeys(wr) if w != right][:3],
             "The graph meets the <i>x</i>-axis at %s%s. The right end goes %s, so the leading coefficient is %s. <b>%s</b>." % (
                 ", ".join(sf(z) for z in zs), " and only touches at %s (squared factor)" % sf(zs[mult]) if mult is not None else "",
                 "up" if (lead > 0) else "down", "positive" if lead > 0 else "negative", right))


# ------------------------------------------------------------ set 5: rational roots and counting zeros
def one_rrt(r):
    kind = r.choice(["rrt", "rrt", "count", "turn", "find"])
    if kind == "rrt":
        lead, const = r.choice([(1, 6), (2, 3), (3, 4), (1, 8), (2, 5), (1, 10), (4, 3), (3, 2)])
        q = "By the Rational Root Theorem, which list shows all possible rational zeros of %s?" % B(poly([lead, r.randint(-5, 5), r.randint(-5, 5), const]))
        ps_ = [d for d in range(1, const + 1) if const % d == 0]
        qs = [d for d in range(1, lead + 1) if lead % d == 0]
        cands = sorted({F(a, b) for a in ps_ for b in qs})
        right = "±" + ", ±".join(sf(c) for c in cands)
        wrong1 = "±" + ", ±".join(sf(c) for c in sorted({F(b, a) for a in ps_ for b in qs}))
        wrong2 = "±" + ", ±".join(sf(c) for c in ps_)
        wrong3 = ", ".join(sf(c) for c in cands)
        return T(q, right, [w for w in dict.fromkeys([wrong1, wrong2, wrong3]) if w != right][:3] + (["±1"] if len({wrong1, wrong2, wrong3} - {right}) < 3 else []),
                 "Possible rational zeros are ± (factors of the constant %d) ÷ (factors of the leading coefficient %d). <b>%s</b>." % (const, lead, right))
    if kind == "count":
        n = r.randint(3, 7)
        q = "How many complex zeros (counting multiplicity) does a polynomial of degree %d have?" % n
        return T(q, num(n), [num(n - 1), num(n + 1), "It depends on the coefficients"],
                 "Fundamental Theorem of Algebra: a polynomial of degree <i>n</i> has exactly <i>n</i> complex zeros, counting multiplicity. <b>%d</b>." % n)
    if kind == "turn":
        n = r.randint(3, 8)
        q = "What is the greatest number of turning points the graph of a degree-%d polynomial can have?" % n
        return T(q, num(n - 1), [num(n), num(n + 1), num(n - 2) if n > 3 else num(2 * n)],
                 "A polynomial of degree <i>n</i> has at most <i>n</i> %s 1 turning points: <b>%d</b>." % (MINUS, n - 1))
    zs = r.sample([x for x in range(-5, 6) if x], 3)
    p = expand(1, [(z, 1) for z in zs])
    z0 = zs[0]
    q = "<i>x</i> = %s is a zero of %s. Find the other zeros." % (sf(z0), B(poly(p)))
    rest = sorted(zs[1:])
    right = "%s and %s" % (sf(rest[0]), sf(rest[1]))
    return T(q, right, ["%s and %s" % (sf(-rest[1]), sf(-rest[0])), "%s and %s" % (sf(rest[0]), sf(-rest[1])), "%s and %s" % (sf(-z0), sf(rest[0]))],
             "Divide by (%s) with synthetic division to get a quadratic, then factor it: (%s)(%s). <b>%s</b>." % (lin(z0), lin(rest[0]), lin(rest[1]), right))


def build():
    sets = [S("Degree and end behavior", collect(one_end, 20, R)),
            S("Zeros and multiplicity", collect(one_zero, 20, R)),
            S("Write a polynomial from its zeros", collect(one_write, 20, R)),
            S("Match the graph", collect(one_graph, 20, R)),
            S("Rational roots and counting zeros", collect(one_rrt, 20, R))]
    body = lesson(
        "<p><b>End behavior</b> depends only on the leading term. Even degree: both ends point the same way (up if the leading coefficient is positive). "
        "Odd degree: the ends point opposite ways (up on the right if the leading coefficient is positive).</p>"
        "<p>In factored form, each factor (<i>x</i> %s <i>a</i>) gives a <b>zero</b> at <i>x</i> = <i>a</i>. If the factor is squared (even multiplicity), the graph touches the axis and turns; "
        "with odd multiplicity it crosses.</p>"
        "<p>A polynomial of degree <i>n</i> has exactly <i>n</i> complex zeros (counting multiplicity) and at most <i>n</i> %s 1 turning points. "
        "Complex zeros of real polynomials come in conjugate pairs. The <b>Rational Root Theorem</b> lists the possible rational zeros: ± factors of the constant ÷ factors of the leading coefficient.</p>" % (MINUS, MINUS),
        [("Find the zeros of <i>f</i>(<i>x</i>) = (<i>x</i> + 2)(<i>x</i> %s 3)²." % MINUS, ["<i>x</i> + 2 = 0 → %s2 (crosses)" % MINUS, "<i>x</i> %s 3 = 0 → 3 (touches)" % MINUS], "%s2 and 3" % MINUS),
         ("Write the polynomial with zeros 1, 2 and %s3." % MINUS, ["(<i>x</i> %s 1)(<i>x</i> %s 2)(<i>x</i> + 3)" % (MINUS, MINUS)], "<i>x</i>³ %s 7<i>x</i> + 6" % MINUS)],
        ["Reading the zero of (<i>x</i> + 3) as 3. It is %s3." % MINUS,
         "Judging end behavior from the constant or the first term written. Use the term with the highest power.",
         "Ignoring multiplicity: a squared factor touches the axis instead of crossing it.",
         "Forgetting that 2 + <i>i</i> comes with 2 %s <i>i</i>." % MINUS])
    faq = [("How do you find the end behavior of a polynomial?", "Look at the degree and the sign of the leading coefficient. Even degree: both ends the same direction. Odd degree: opposite directions."),
           ("What does multiplicity mean?", "How many times a factor appears. An even multiplicity means the graph touches the x-axis and turns around; an odd multiplicity means it crosses."),
           ("What is the Rational Root Theorem?", "Any rational zero p/q of a polynomial with integer coefficients has p dividing the constant term and q dividing the leading coefficient."),
           ("How many zeros does a polynomial have?", "A polynomial of degree n has exactly n complex zeros when you count multiplicity (the Fundamental Theorem of Algebra).")]
    make("polynomial-functions-and-zeros", 3, "A-APR.B.3",
         "Polynomial Functions: Zeros, Multiplicity, and End Behavior",
         "Polynomial Functions Worksheet: Zeros, Multiplicity, End Behavior (Algebra 2) | 100 Questions",
         "Polynomial Functions and Zeros",
         "Identify zeros of polynomials when suitable factorizations are available, and use the zeros to construct a rough graph of the function defined by the polynomial.",
         "Free Algebra 2 worksheet on polynomial functions: end behavior, zeros and multiplicity, writing polynomials from zeros, graphs and the Rational Root Theorem. 100 questions with answers.",
         "End behavior comes from the leading term. Each factor (x − a) gives a zero at a.",
         "Even multiplicity touches the x-axis; odd multiplicity crosses it.",
         body, faq, sets, R, domain="Polynomials", grade="algebra-2")


if __name__ == "__main__":
    build()
