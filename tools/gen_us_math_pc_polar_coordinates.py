# -*- coding: utf-8 -*-
"""
US Precalculus: Polar Coordinates and Polar Graphs (Common Core N-CN.B.4 extended to points and curves)
  python3 tools/gen_us_math_pc_polar_coordinates.py
Converting points between polar and rectangular coordinates, equivalent polar coordinates, converting
equations, and recognizing polar graphs: circles, roses, cardioids and limaçons.
Wrong answers come from real mistakes: swapping cos and sin, taking tan⁻¹(y/x) without the quadrant,
thinking (−r, θ) is the same point as (r, θ), and counting n petals for r = a sin nθ when n is even.
"""
import math
import random
from fractions import Fraction as F
from us_hs import B, S, make, lesson, collect, T, fig, num, MINUS, fr
from a2_common import sf
from pc_common import GRADE, pis, trig, rad, rt
from ws_common import svg_wrap, line, text

R = random.Random(98601)
X, Y = "<i>x</i>", "<i>y</i>"
TH = "θ"
SPEC = [30, 45, 60, 90, 120, 135, 150, 180, 210, 225, 240, 270, 300, 315, 330]


def comp(rr, d, fn):
    sg, k = trig(fn, d)
    if k == "0":
        return "0"
    if k == "1":
        return (MINUS if sg < 0 else "") + str(rr)
    h = rr // 2
    m = {"1/2": str(h), "r2/2": ("%d√2" % h) if h > 1 else "√2", "r3/2": ("%d√3" % h) if h > 1 else "√3"}[k]
    return (MINUS if sg < 0 else "") + m


def ppt(rr, d):
    return "(%s, %s)" % (sf(rr) if not isinstance(rr, str) else rr, pis(rad(d)))


# ------------------------------------------------------------ set 1: polar to rectangular
def one_p2r(r):
    rr = r.choice([2, 4, 6, 8])
    d = r.choice(SPEC)
    right = "(%s, %s)" % (comp(rr, d, "cos"), comp(rr, d, "sin"))
    wr = ["(%s, %s)" % (comp(rr, d, "sin"), comp(rr, d, "cos")), "(%s, %s)" % (comp(rr, (d + 180) % 360, "cos"), comp(rr, d, "sin")), "(%s, %s)" % (comp(rr, d, "cos"), comp(rr, (360 - d) % 360, "sin"))]
    if len(set(wr + [right])) < 4:
        wr.append("(%d, %s)" % (rr, pis(rad(d))))
    return T("Convert the polar point %s to rectangular coordinates." % ppt(rr, d), right, wr,
             "<i>x</i> = <i>r</i> cos θ = %d cos %s and <i>y</i> = <i>r</i> sin θ = %d sin %s. <b>%s</b>." % (rr, pis(rad(d)), rr, pis(rad(d)), right))


# ------------------------------------------------------------ set 2: rectangular to polar
def one_r2p(r):
    rr = r.choice([2, 4, 6, 8])
    d = r.choice(SPEC)
    x, y = comp(rr, d, "cos"), comp(rr, d, "sin")
    q = "Convert (%s, %s) to polar coordinates (<i>r</i>, θ) with <i>r</i> &gt; 0 and 0 ≤ θ &lt; 2π." % (x, y)
    right = ppt(rr, d)
    ref = d if d <= 90 else 180 - d if d <= 180 else d - 180 if d <= 270 else 360 - d
    wr = [ppt(rr, ref) if ref != d else ppt(rr, (d + 180) % 360), ppt(rr * rr, d), ppt(rr, (d + 180) % 360) if ref != (d + 180) % 360 else ppt(rr, (d + 90) % 360)]
    return T(q, right, wr, "<i>r</i> = √(<i>x</i>² + <i>y</i>²) = %d. The point is %s, so θ = %s. <b>%s</b>." % (
        rr, "on an axis" if d % 90 == 0 else "in Quadrant %s" % ["I", "II", "III", "IV"][d // 90], pis(rad(d)), right))


# ------------------------------------------------------------ set 3: equivalent coordinates
def one_eq(r):
    rr = r.choice([2, 3, 4, 5])
    d = r.choice([30, 45, 60, 120, 135, 150, 210, 240, 300])
    kind = r.choice(["neg", "neg", "plus", "which"])
    if kind == "neg":
        q = "Which polar coordinates name the same point as %s, using a negative <i>r</i>?" % ppt(rr, d)
        right = ppt(-rr, (d + 180) % 360)
        return T(q, right, [ppt(-rr, d), ppt(-rr, (360 - d) % 360), ppt(-rr, (d + 90) % 360)],
                 "(−<i>r</i>, θ + π) is the same point as (<i>r</i>, θ): going backward from the opposite direction. <b>%s</b>." % right)
    if kind == "plus":
        q = "Which polar coordinates name the same point as %s?" % ppt(rr, d)
        right = "(%d, %s)" % (rr, pis(rad(d) - 2))
        return T(q, right, [ppt(-rr, d), ppt(rr, (d + 180) % 360), ppt(rr, (360 - d) % 360)],
                 "Adding or subtracting 2π gives the same direction: %s − 2π = %s. <b>%s</b>." % (pis(rad(d)), pis(rad(d) - 2), right))
    q = "Which point is <b>not</b> the same as %s?" % ppt(rr, d)
    right = ppt(-rr, d)
    return T(q, right, [ppt(-rr, (d + 180) % 360), "(%d, %s)" % (rr, pis(rad(d) + 2)), "(%d, %s)" % (rr, pis(rad(d) - 2))],
             "(−<i>r</i>, θ) is the reflection through the pole, not the same point. <b>%s</b>." % right)


# ------------------------------------------------------------ set 4: converting equations
EQS = [("<i>r</i> = 4", "<i>x</i>² + <i>y</i>² = 16", ["<i>x</i> + <i>y</i> = 4", "<i>x</i>² + <i>y</i>² = 4", "<i>y</i> = 4"], "<i>r</i>² = <i>x</i>² + <i>y</i>²"),
       ("<i>r</i> = 5", "<i>x</i>² + <i>y</i>² = 25", ["<i>x</i>² + <i>y</i>² = 5", "<i>x</i> = 5", "<i>x</i> + <i>y</i> = 5"], "<i>r</i>² = <i>x</i>² + <i>y</i>²"),
       ("θ = π/4", "<i>y</i> = <i>x</i>", ["<i>y</i> = π/4", "<i>x</i>² + <i>y</i>² = π/4", "<i>y</i> = −<i>x</i>"], "tan θ = <i>y</i>/<i>x</i> = 1"),
       ("θ = 3π/4", "<i>y</i> = −<i>x</i>", ["<i>y</i> = <i>x</i>", "<i>y</i> = 3π/4", "<i>x</i> = −1"], "tan θ = <i>y</i>/<i>x</i> = −1"),
       ("<i>r</i> sin θ = 3", "<i>y</i> = 3", ["<i>x</i> = 3", "<i>x</i>² + <i>y</i>² = 9", "<i>y</i> = 3<i>x</i>"], "<i>y</i> = <i>r</i> sin θ"),
       ("<i>r</i> cos θ = −2", "<i>x</i> = −2", ["<i>y</i> = −2", "<i>x</i>² + <i>y</i>² = 4", "<i>x</i> = 2"], "<i>x</i> = <i>r</i> cos θ"),
       ("<i>r</i> = 6 cos θ", "<i>x</i>² + <i>y</i>² = 6<i>x</i>", ["<i>x</i>² + <i>y</i>² = 36", "<i>x</i> = 6", "<i>x</i>² + <i>y</i>² = 6<i>y</i>"], "multiply by <i>r</i>: <i>r</i>² = 6<i>r</i> cos θ"),
       ("<i>r</i> = 4 sin θ", "<i>x</i>² + <i>y</i>² = 4<i>y</i>", ["<i>x</i>² + <i>y</i>² = 4<i>x</i>", "<i>y</i> = 4", "<i>x</i>² + <i>y</i>² = 16"], "multiply by <i>r</i>: <i>r</i>² = 4<i>r</i> sin θ"),
       ("<i>x</i>² + <i>y</i>² = 49", "<i>r</i> = 7", ["<i>r</i> = 49", "θ = 7", "<i>r</i> = 7 cos θ"], "<i>x</i>² + <i>y</i>² = <i>r</i>²"),
       ("<i>x</i> = 5", "<i>r</i> cos θ = 5", ["<i>r</i> sin θ = 5", "<i>r</i> = 5", "θ = 5"], "<i>x</i> = <i>r</i> cos θ"),
       ("<i>y</i> = −4", "<i>r</i> sin θ = −4", ["<i>r</i> cos θ = −4", "<i>r</i> = −4", "<i>r</i> = 4"], "<i>y</i> = <i>r</i> sin θ"),
       ("<i>y</i> = √3<i>x</i>", "θ = π/3", ["θ = π/6", "<i>r</i> = √3", "θ = 2π/3"], "tan θ = √3"),
       ("<i>x</i>² + <i>y</i>² = 8<i>x</i>", "<i>r</i> = 8 cos θ", ["<i>r</i> = 8 sin θ", "<i>r</i> = 8", "<i>r</i> = 64 cos θ"], "<i>r</i>² = 8<i>r</i> cos θ, then divide by <i>r</i>"),
       ("<i>x</i>² + <i>y</i>² = 10<i>y</i>", "<i>r</i> = 10 sin θ", ["<i>r</i> = 10 cos θ", "<i>r</i> = 10", "<i>r</i> = √10"], "<i>r</i>² = 10<i>r</i> sin θ, then divide by <i>r</i>"),
       ("<i>r</i> = 2 sec θ", "<i>x</i> = 2", ["<i>y</i> = 2", "<i>x</i> = 1/2", "<i>x</i>² + <i>y</i>² = 4"], "<i>r</i> = 2/cos θ, so <i>r</i> cos θ = 2"),
       ("<i>r</i> = 3 csc θ", "<i>y</i> = 3", ["<i>x</i> = 3", "<i>y</i> = 1/3", "<i>x</i>² + <i>y</i>² = 9"], "<i>r</i> = 3/sin θ, so <i>r</i> sin θ = 3"),
       ("<i>xy</i> = 4", "<i>r</i>² sin θ cos θ = 4", ["<i>r</i> sin θ cos θ = 4", "<i>r</i>² = 4", "sin θ cos θ = 4"], "<i>x</i> = <i>r</i> cos θ and <i>y</i> = <i>r</i> sin θ"),
       ("<i>r</i>² = 9", "<i>x</i>² + <i>y</i>² = 9", ["<i>x</i>² + <i>y</i>² = 3", "<i>x</i> + <i>y</i> = 9", "<i>y</i> = 9"], "<i>r</i>² = <i>x</i>² + <i>y</i>²"),
       ("θ = π/2", "<i>x</i> = 0", ["<i>y</i> = 0", "<i>y</i> = π/2", "<i>x</i> = π/2"], "the direction straight up is the <i>y</i>-axis"),
       ("<i>r</i> = −2 cos θ", "<i>x</i>² + <i>y</i>² = −2<i>x</i>", ["<i>x</i>² + <i>y</i>² = 2<i>x</i>", "<i>x</i> = −2", "<i>x</i>² + <i>y</i>² = 4"], "multiply by <i>r</i>: <i>r</i>² = −2<i>r</i> cos θ"),
       ("<i>y</i> = <i>x</i>²", "<i>r</i> sin θ = <i>r</i>² cos² θ", ["sin θ = cos² θ", "<i>r</i> = sin θ cos θ", "<i>r</i> sin θ = <i>r</i> cos θ"], "replace <i>x</i> and <i>y</i>"),
       ("<i>r</i> = 5 cos θ + 5 sin θ", "<i>x</i>² + <i>y</i>² = 5<i>x</i> + 5<i>y</i>", ["<i>x</i> + <i>y</i> = 5", "<i>x</i>² + <i>y</i>² = 25", "<i>x</i>² + <i>y</i>² = 5<i>xy</i>"], "multiply by <i>r</i>")]


def one_conv(r):
    a, right, wr, how = r.choice(EQS)
    polar_given = "θ" in a or a.startswith("<i>r</i>")
    q = "Write %s in %s form." % (a, "rectangular" if polar_given else "polar")
    return T(q, right, wr, "Key step: %s. <b>%s</b>." % (how, right))


# ------------------------------------------------------------ set 5: polar graphs
def polar_svg(f, rmax, label):
    W = 220
    c = W / 2
    sc = (W / 2 - 14) / rmax
    s = []
    for k in range(1, int(rmax) + 1):
        s.append("<circle cx='%d' cy='%d' r='%.1f' fill='none' stroke='#dddddd' stroke-width='1'/>" % (c, c, k * sc))
    for a in range(0, 180, 30):
        t = math.radians(a)
        s.append(line(c - math.cos(t) * rmax * sc, c + math.sin(t) * rmax * sc, c + math.cos(t) * rmax * sc, c - math.sin(t) * rmax * sc, "#dddddd", 1))
    s.append(line(14, c, W - 14, c, "#222", 1.5))
    s.append(line(c, 14, c, W - 14, "#222", 1.5))
    pts = []
    for i in range(0, 1441):
        t = math.radians(i / 4)
        rv = f(t)
        pts.append("%.1f,%.1f" % (c + rv * math.cos(t) * sc, c - rv * math.sin(t) * sc))
    s.append("<polyline points='%s' fill='none' stroke='#1f6fd1' stroke-width='2.4'/>" % " ".join(pts[::2]))
    s.append(text(W - 8, c - 5, "%d" % rmax, 10, anchor="end", weight=400))
    return svg_wrap(W, W, "".join(s), label)


def one_graph(r):
    kind = r.choice(["rose", "rose", "cardioid", "circle", "limacon", "count", "count"])
    a = r.choice([2, 3, 4])
    if kind == "count":
        n = r.choice([2, 3, 4, 5, 6])
        fn = r.choice(["sin", "cos"])
        q = "How many petals does the rose <i>r</i> = %d %s %d%s have?" % (a, fn, n, TH)
        ans = n if n % 2 else 2 * n
        return T(q, str(ans), [str(2 * n if n % 2 else n), str(n + 1), str(a * n) if a * n not in (n, 2 * n) else str(n + 2)],
                 "For <i>r</i> = <i>a</i> %s <i>n</i>θ: <i>n</i> petals if <i>n</i> is odd, 2<i>n</i> petals if <i>n</i> is even. Here <i>n</i> = %d, so <b>%d</b>." % (fn, n, ans))
    names = {"rose": None, "cardioid": None, "circle": None, "limacon": None}
    if kind == "rose":
        n = r.choice([2, 3, 4, 5])
        fn = r.choice(["sin", "cos"])
        f = (lambda t: a * math.sin(n * t)) if fn == "sin" else (lambda t: a * math.cos(n * t))
        right = "<i>r</i> = %d %s %d%s" % (a, fn, n, TH)
        wr = ["<i>r</i> = %d %s %d%s" % (a, fn, 2 * n if n % 2 else n // 2 if n // 2 > 1 else n + 1, TH), "<i>r</i> = %d %s %d%s" % (n, fn, a, TH) if n != a else "<i>r</i> = %d %s %d%s" % (a + 1, fn, n, TH),
              "<i>r</i> = %d + %d %s %s" % (a, a, fn, TH)]
        why = "It is a rose with %d petals of length %d." % (n if n % 2 else 2 * n, a)
        rmax = a
    elif kind == "cardioid":
        fn = r.choice(["sin", "cos"])
        sg = r.choice([1, -1])
        f = (lambda t: a + sg * a * (math.sin(t) if fn == "sin" else math.cos(t)))
        right = "<i>r</i> = %d %s %d %s %s" % (a, "+" if sg > 0 else MINUS, a, fn, TH)
        other = "cos" if fn == "sin" else "sin"
        wr = ["<i>r</i> = %d %s %d %s %s" % (a, MINUS if sg > 0 else "+", a, fn, TH), "<i>r</i> = %d %s %d %s %s" % (a, "+" if sg > 0 else MINUS, a, other, TH), "<i>r</i> = %d %s %d%s" % (2 * a, fn, 2, TH)]
        why = "It is a cardioid (heart shape). It points %s, so the equation uses %s with a %s sign." % (
            {("sin", 1): "up", ("sin", -1): "down", ("cos", 1): "right", ("cos", -1): "left"}[(fn, sg)], fn, "plus" if sg > 0 else "minus")
        rmax = 2 * a
    elif kind == "circle":
        fn = r.choice(["sin", "cos"])
        d = 2 * a
        f = (lambda t: d * (math.sin(t) if fn == "sin" else math.cos(t)))
        right = "<i>r</i> = %d %s %s" % (d, fn, TH)
        other = "cos" if fn == "sin" else "sin"
        wr = ["<i>r</i> = %d %s %s" % (d, other, TH), "<i>r</i> = %d" % d, "<i>r</i> = %d %s %s" % (a, fn, TH)]
        why = "It is a circle of diameter %d through the pole, %s." % (d, "above the pole (sine)" if fn == "sin" else "to the right of the pole (cosine)")
        rmax = d
    else:
        b = a + r.choice([1, 2])
        fn = r.choice(["sin", "cos"])
        f = (lambda t: a + b * (math.sin(t) if fn == "sin" else math.cos(t)))
        right = "<i>r</i> = %d + %d %s %s" % (a, b, fn, TH)
        wr = ["<i>r</i> = %d + %d %s %s" % (b, a, fn, TH), "<i>r</i> = %d + %d %s %s" % (a, a, fn, TH), "<i>r</i> = %d %s %d%s" % (a + b, fn, 2, TH)]
        why = "It is a limaçon with an inner loop, because |%d| &gt; |%d|. The longest distance from the pole is %d + %d = %d." % (b, a, a, b, a + b)
        rmax = a + b
    svg = polar_svg(f, rmax, "polar graph")
    return T("Which equation matches the polar graph? The outer circle has radius %d." % rmax + fig(svg), right, wr, "%s <b>%s</b>." % (why, right))


def build():
    sets = [S("Polar to rectangular", collect(one_p2r, 20, R)),
            S("Rectangular to polar", collect(one_r2p, 20, R)),
            S("Equivalent polar coordinates", collect(one_eq, 20, R)),
            S("Converting equations", collect(one_conv, 20, R)),
            S("Polar graphs", collect(one_graph, 20, R))]
    body = lesson(
        "<ul><li>A polar point (<i>r</i>, θ) is <i>r</i> units from the pole in the direction θ.</li>"
        "<li>Polar to rectangular: <i>x</i> = <i>r</i> cos θ, <i>y</i> = <i>r</i> sin θ. Rectangular to polar: <i>r</i> = √(<i>x</i>² + <i>y</i>²), and θ from tan θ = <i>y</i>/<i>x</i> in the correct quadrant.</li>"
        "<li>A point has many names: (<i>r</i>, θ) = (<i>r</i>, θ + 2π) = (−<i>r</i>, θ + π).</li>"
        "<li>Graphs: <i>r</i> = <i>a</i> is a circle; <i>r</i> = <i>a</i> cos θ or <i>a</i> sin θ is a circle through the pole; <i>r</i> = <i>a</i> sin <i>n</i>θ is a rose with <i>n</i> petals (<i>n</i> odd) or 2<i>n</i> (<i>n</i> even); <i>r</i> = <i>a</i> + <i>a</i> cos θ is a cardioid.</li></ul>",
        [("Convert (4, 2π/3) to rectangular coordinates.", ["<i>x</i> = 4 cos(2π/3) = −2", "<i>y</i> = 4 sin(2π/3) = 2√3"], "(−2, 2√3)"),
         ("Write <i>r</i> = 6 cos θ in rectangular form.", ["Multiply by <i>r</i>: <i>r</i>² = 6<i>r</i> cos θ", "<i>x</i>² + <i>y</i>² = 6<i>x</i>"], "a circle centered at (3, 0) with radius 3")],
        ["Swapping cos and sin: <i>x</i> uses cosine.",
         "Using tan⁻¹(<i>y</i>/<i>x</i>) without checking the quadrant.",
         "Thinking (−<i>r</i>, θ) is the same point as (<i>r</i>, θ). Use (−<i>r</i>, θ + π).",
         "Counting <i>n</i> petals when <i>n</i> is even. There are 2<i>n</i>."])
    faq = [("How do you convert polar coordinates to rectangular?", "Use x = r cos θ and y = r sin θ."),
           ("How do you convert rectangular coordinates to polar?", "Find r = √(x² + y²) and an angle θ with tan θ = y/x, choosing the angle in the quadrant where the point lies."),
           ("How many petals does a polar rose have?", "r = a sin nθ or r = a cos nθ has n petals when n is odd and 2n petals when n is even."),
           ("What does r = a cos θ look like?", "A circle of diameter a that passes through the pole, with its center on the x-axis at (a/2, 0).")]
    make("polar-coordinates", 16, "N-CN.B.4",
         "Polar Coordinates and Polar Graphs",
         "Polar Coordinates Worksheet: Converting Points and Equations, Polar Graphs | 100 Questions",
         "Polar Coordinates",
         "Represent complex numbers on the complex plane in rectangular and polar form (including real and imaginary numbers), and explain why the rectangular and polar forms of a given complex number represent the same number.",
         "Free precalculus worksheet on polar coordinates: converting points and equations between polar and rectangular form, equivalent coordinates, roses, cardioids and limaçons. 100 questions.",
         "x = r cos θ, y = r sin θ, r² = x² + y².",
         "(r, θ) = (r, θ + 2π) = (−r, θ + π).",
         body, faq, sets, R, domain="Complex Numbers and Polar Coordinates", grade=GRADE)


if __name__ == "__main__":
    build()
