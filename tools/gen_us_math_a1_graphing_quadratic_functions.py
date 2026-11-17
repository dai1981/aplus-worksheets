# -*- coding: utf-8 -*-
"""
US Algebra 1: Graphing Quadratic Functions (Common Core F-IF.C.7a, F-IF.B.4, F-BF.B.3)
  python3 tools/gen_us_math_a1_graphing_quadratic_functions.py
Reading the vertex, axis of symmetry, zeros and y-intercept from a graph, finding the vertex from standard form
with x = −b/2a, vertex form and transformations of y = x², features of factored form, and maximum and minimum
problems.
Wrong answers come from real mistakes: sign errors with h in vertex form, using b/2a instead of −b/2a,
swapping the coordinates of the vertex, reading the y-intercept as a zero, and thinking a larger |a| makes the
parabola wider.
"""
import random
from fractions import Fraction as F
from us_hs import num, B, S, make, lesson, collect, QN, T, svg_wrap, line, text, fig, INK, RED, BLUE, expr, MINUS

R = random.Random(91801)
X = "<i>x</i>"
X2 = "<i>x</i><sup>2</sup>"
XLO, XHI, YLO, YHI = -5, 5, -9, 9
UX, UY = 26, 15


def quad(a, b, c):
    return expr([(a, X2), (b, X), (c, "")])


def P(x, y):
    return "(%s, %s)" % (num(x), num(y))


def para_svg(f, hline=None, label="graph of a quadratic"):
    ox = 34 - XLO * UX
    oy = 24 + YHI * UY
    PX = lambda v: ox + v * UX
    PY = lambda v: oy - v * UY
    s = []
    for v in range(XLO, XHI + 1):
        s.append(line(PX(v), PY(YLO), PX(v), PY(YHI), "#dcdcdc", 1))
    for v in range(YLO, YHI + 1):
        s.append(line(PX(XLO), PY(v), PX(XHI), PY(v), "#dcdcdc", 1))
    s.append(line(PX(XLO) - 6, PY(0), PX(XHI) + 10, PY(0), INK, 2))
    s.append(line(PX(0), PY(YLO) + 6, PX(0), PY(YHI) - 8, INK, 2))
    for v in range(XLO, XHI + 1):
        if v:
            s.append(text(PX(v), PY(0) + 15, num(v), 11, weight=400))
    for v in range(YLO, YHI + 1):
        if v and v % 2 == 0:
            s.append(text(PX(0) - 7, PY(v) + 4, num(v), 11, weight=400, anchor="end"))
    s.append(text(PX(XHI) + 14, PY(0) + 5, "x", 14, italic=True))
    s.append(text(PX(0), PY(YHI) - 12, "y", 14, italic=True))
    if hline is not None:
        s.append(line(PX(XLO), PY(hline), PX(XHI), PY(hline), RED, 2.5))
    segs, cur = [], []
    n = 400
    for i in range(n + 1):
        x = XLO + (XHI - XLO) * i / n
        y = f(x)
        if YLO - 0.01 <= y <= YHI + 0.01:
            cur.append("%.1f,%.1f" % (PX(x), PY(y)))
        elif cur:
            segs.append(cur)
            cur = []
    if cur:
        segs.append(cur)
    for sg in segs:
        if len(sg) > 1:
            s.append("<polyline points='%s' fill='none' stroke='%s' stroke-width='3'/>" % (" ".join(sg), BLUE))
    W = (XHI - XLO) * UX + 68
    H = (YHI - YLO) * UY + 48
    return "<svg data-pf='lg'" + svg_wrap(W, H, "".join(s), label)[4:]


def sol(xs):
    xs = sorted(set(xs))
    return " or ".join("%s = %s" % (X, num(v)) for v in xs)


# ------------------------------------------------------------ set 1: read a graph
def one_read(r):
    p, q_ = r.randint(-4, 3), r.randint(-3, 4)
    if q_ - p < 2 or q_ - p > 6 or (p + q_) % 2:
        return None
    a = 1 if r.random() < 0.75 else -1
    f = lambda x: a * (x - p) * (x - q_)
    b, c = -a * (p + q_), a * p * q_
    if c == 0:
        return None
    m = (p + q_) // 2
    tv = f(m)
    g = fig(para_svg(f))
    kind = r.choice(["roots", "roots", "turn", "int", "sym"])
    title = "The graph shows %s." % B("y = " + quad(a, b, c))
    if kind == "roots":
        q = g + title + " What are the zeros (where the parabola crosses the %s-axis)?" % X
        right = sol([p, q_])
        wr = [sol([-p, -q_]), sol([c]) if c not in (p, q_) else sol([c + 1]), "%s = %s only" % (X, num(q_))]
        e = "The parabola crosses the %s-axis at %s and %s, so <b>%s</b>." % (X, num(p), num(q_), right)
        if sol([-p, -q_]) == right:
            return None
        return T(q, right, wr, e)
    if kind == "turn":
        q = g + title + " What are the coordinates of the vertex?"
        right = P(m, tv)
        wr = [P(tv, m), P(m, -tv), P(0, c)]
        if right in wr[1:] or tv == m:
            return None
        e = "The %s point of the parabola is at %s = %s, %s = %s: <b>%s</b>." % ("lowest" if a > 0 else "highest", X, num(m), "<i>y</i>", num(tv), right)
        return T(q, right, wr, e)
    if kind == "int":
        q = g + title + " Where does the parabola cross the %s-axis?" % "<i>y</i>"
        right = P(0, c)
        wr = [P(c, 0), P(p, 0), P(m, tv)]
        if right in wr[1:] or c == 0:
            return None
        e = "Read where the parabola meets the %s-axis (when %s = 0): <b>%s</b>. It equals the constant term %s." % ("<i>y</i>", X, right, num(c))
        return T(q, right, wr, e)
    q = g + title + " What is the equation of its line of symmetry?"
    right = "%s = %s" % (X, num(m))
    wr = ["<i>y</i> = %s" % num(m), "%s = %s" % (X, num(-m)) if m else "%s = %s" % (X, num(tv)), "<i>y</i> = %s" % num(tv)]
    e = "The line of symmetry is the vertical line through the vertex: <b>%s</b> (halfway between %s and %s)." % (right, num(p), num(q_))
    return T(q, right, wr, e)


# ------------------------------------------------------------ set 4: features
def one_feature(r):
    k = r.randint(0, 4)
    if k == 0:
        c = r.randint(-9, 9)
        a = r.choice([1, -1])
        if c == 0:
            return None
        q = "What is the vertex of %s?" % B("y = " + quad(a, 0, c))
        right = P(0, c)
        return T(q, right, [P(c, 0), P(0, -c), P(a, c)], "There is no %s term, so the parabola is symmetric about the %s-axis. When %s = 0, %s = %s: <b>%s</b>." % (X, "<i>y</i>", X, "<i>y</i>", num(c), right))
    if k == 1:
        b, c = r.randint(-6, 6), r.randint(-9, 9)
        if c == 0 or b == 0:
            return None
        q = "Where does %s cross the %s-axis?" % (B("y = " + quad(1, b, c)), "<i>y</i>")
        right = P(0, c)
        return T(q, right, [P(c, 0), P(0, b), P(b, c)], "Put %s = 0: %s = %s. <b>%s</b>." % (X, "<i>y</i>", num(c), right))
    if k == 2:
        p, q_ = r.randint(-6, 6), r.randint(-6, 6)
        if p == q_ or p == -q_ or 0 in (p, q_):
            return None
        q = "What are the zeros of %s?" % B("y = (%s)(%s)" % (expr([(1, X), (-p, "")]), expr([(1, X), (-q_, "")])))
        right = sol([p, q_])
        return T(q, right, [sol([-p, -q_]), sol([p, -q_]), sol([p * q_])], "Set each factor equal to zero: %s = %s or %s = %s. <b>%s</b>." % (X, num(p), X, num(q_), right))
    if k == 3:
        p, q_ = r.randint(-6, 6), r.randint(-6, 6)
        if (p + q_) % 2 or p == q_ or p + q_ == 0:
            return None
        m = (p + q_) // 2
        q = "A quadratic graph has zeros %s = %s and %s = %s. What is its line of symmetry?" % (X, num(min(p, q_)), X, num(max(p, q_)))
        right = "%s = %s" % (X, num(m))
        return T(q, right, ["%s = %s" % (X, num(-m)), "<i>y</i> = %s" % num(m), "%s = %s" % (X, num(p + q_))], "The line of symmetry is halfway between the zeros: (%s + %s) ÷ 2 = %s. <b>%s</b>." % (num(p), num(q_), num(m), right))
    a = r.choice([1, -1, 2, -2, 3, -3])
    b, c = r.randint(-5, 5), r.randint(-5, 5)
    q = "What shape is the graph of %s?" % B("y = " + quad(a, b, c))
    right = "Opens up, with a minimum" if a > 0 else "Opens down, with a maximum"
    other = "Opens down, with a maximum" if a > 0 else "Opens up, with a minimum"
    wr = [other, "A straight line", "Opens up, with a maximum" if a > 0 else "Opens down, with a minimum"]
    return T(q, right, wr, "The %s term is %s, so the parabola is <b>%s</b>." % (X2, "positive" if a > 0 else "negative", right))


# ------------------------------------------------------------ set 2: vertex and axis from standard form
def one_std(r):
    a = r.choice([1, 1, 2, -1, -2, 3])
    h = r.randint(-5, 5)
    k = r.randint(-9, 9)
    b, c = -2 * a * h, a * h * h + k
    if b == 0:
        return None
    f = "<i>f</i>(<i>x</i>) = %s" % quad(a, b, c)
    kind = r.choice(["axis", "vertex", "vertex", "ext"])
    if kind == "axis":
        q = "What is the axis of symmetry of %s?" % B(f)
        right = "%s = %s" % (X, num(h))
        wr = ["%s = %s" % (X, num(-h)), "%s = %s" % (X, num(-b)), "<i>y</i> = %s" % num(k)]
        e = "<i>x</i> = −<i>b</i> ÷ 2<i>a</i> = −(%s) ÷ (2 × %s) = %s: <b>%s</b>." % (num(b), "(%s)" % num(a) if a < 0 else num(a), num(h), right)
    elif kind == "vertex":
        q = "What is the vertex of %s?" % B(f)
        right = P(h, k)
        wr = [P(-h, k), P(h, c), P(k, h) if k != h else P(h, -k)]
        e = "<i>x</i> = −<i>b</i> ÷ 2<i>a</i> = %s. Then <i>f</i>(%s) = %s. <b>%s</b>." % (num(h), num(h), num(k), right)
    else:
        q = "What is the %s value of %s?" % ("minimum" if a > 0 else "maximum", B(f))
        right = num(k)
        wr = [num(h), num(c), num(-k) if k else num(c + 1)]
        e = "The parabola opens %s, so the vertex gives the %s. <i>x</i> = %s and <i>f</i>(%s) = <b>%s</b>." % ("up" if a > 0 else "down", "minimum" if a > 0 else "maximum", num(h), num(h), num(k))
    wr = [w for w in dict.fromkeys(wr) if w != right]
    if len(wr) < 3:
        return None
    return T(q, right, wr[:3], e)


# ------------------------------------------------------------ set 3: vertex form and transformations
def vform(a, h, k):
    inside = "(%s)<sup>2</sup>" % expr([(1, X), (-h, "")]) if h else X2
    lead = "" if a == 1 else (MINUS if a == -1 else num(a))
    tail = (" %s %s" % ("+" if k > 0 else MINUS, num(abs(k)))) if k else ""
    return "<i>y</i> = %s%s%s" % (lead, inside, tail)


def one_vform(r):
    a = r.choice([1, -1, 2, -2, 3, F(1, 2)])
    h, k = r.randint(-6, 6), r.randint(-8, 8)
    if h == 0 and k == 0:
        return None
    kind = r.choice(["vertex", "vertex", "open", "shift", "write"])
    if kind == "vertex":
        q = "What is the vertex of %s?" % B(vform(a, h, k))
        right = P(h, k)
        wr = [P(-h, k), P(h, -k) if k else P(-h, 1), P(k, h) if k != h else P(-h, -k)]
        e = "In <i>y</i> = <i>a</i>(<i>x</i> − <i>h</i>)<sup>2</sup> + <i>k</i>, the vertex is (<i>h</i>, <i>k</i>). Watch the sign inside: <b>%s</b>." % right
    elif kind == "open":
        q = "Which describes the graph of %s?" % B(vform(a, h, k))
        up = a > 0
        wide = abs(a) < 1
        right = "Opens %s, %s than y = x²" % ("up" if up else "down", "wider" if wide else ("narrower" if abs(a) > 1 else "the same width"))
        wr = ["Opens %s, %s than y = x²" % ("down" if up else "up", "wider" if wide else ("narrower" if abs(a) > 1 else "the same width")),
              "Opens %s, %s than y = x²" % ("up" if up else "down", "narrower" if wide else "wider"),
              "Opens %s, %s than y = x²" % ("down" if up else "up", "narrower" if wide else "wider")]
        e = "<i>a</i> = %s is %s, so it opens %s; |<i>a</i>| %s 1, so it is %s." % (
            num(a) if F(a).denominator == 1 else "½", "positive" if up else "negative", "up" if up else "down",
            "&lt;" if wide else ("&gt;" if abs(a) > 1 else "="), "wider" if wide else ("narrower" if abs(a) > 1 else "the same width"))
    elif kind == "shift":
        if a != 1:
            return None
        q = "How is the graph of %s related to the graph of <i>y</i> = <i>x</i><sup>2</sup>?" % B(vform(1, h, k))
        hs = ("%d %s" % (abs(h), "right" if h > 0 else "left")) if h else ""
        vs = ("%d %s" % (abs(k), "up" if k > 0 else "down")) if k else ""
        right = "Shifted " + " and ".join(x for x in (hs, vs) if x)
        hs2 = ("%d %s" % (abs(h), "left" if h > 0 else "right")) if h else ""
        vs2 = ("%d %s" % (abs(k), "down" if k > 0 else "up")) if k else ""
        wr = ["Shifted " + " and ".join(x for x in (hs2, vs) if x), "Shifted " + " and ".join(x for x in (hs, vs2) if x), "Shifted " + " and ".join(x for x in (hs2, vs2) if x)]
        e = "(<i>x</i> − <i>h</i>) moves the graph <i>h</i> to the right, and + <i>k</i> moves it up: <b>%s</b>." % right.lower()
    else:
        if F(a).denominator != 1:
            return None
        q = "A parabola has vertex %s and opens %s with <i>a</i> = %s. Which equation fits?" % (B(P(h, k)), "up" if a > 0 else "down", num(a))
        right = vform(a, h, k)
        wr = [vform(a, -h, k), vform(a, h, -k) if k else vform(a, -h, 1), vform(-a, h, k)]
        e = "Use <i>y</i> = <i>a</i>(<i>x</i> − <i>h</i>)<sup>2</sup> + <i>k</i> with <i>h</i> = %s and <i>k</i> = %s: <b>%s</b>." % (num(h), num(k), right)
    wr = [w for w in dict.fromkeys(wr) if w != right]
    if len(wr) < 3:
        return None
    return T(q, right, wr[:3], e)


# ------------------------------------------------------------ set 5: problems
def problems():
    data = [
        ("A ball's height is <i>h</i> = −16<i>t</i><sup>2</sup> + 64<i>t</i> + 4 feet. When does it reach its maximum height?", "After 2 seconds", ["After 4 seconds", "After 64 seconds", "After 1 second"], "<i>t</i> = −<i>b</i> ÷ 2<i>a</i> = −64 ÷ (−32) = <b>2 s</b>."),
        ("What is the maximum height of the ball in <i>h</i> = −16<i>t</i><sup>2</sup> + 64<i>t</i> + 4?", "68 ft", ["64 ft", "4 ft", "132 ft"], "<i>h</i>(2) = −64 + 128 + 4 = <b>68 ft</b>."),
        ("A farmer has 40 m of fencing for a rectangular pen. The area is <i>A</i> = <i>w</i>(20 − <i>w</i>). What width gives the greatest area?", "10 m", ["20 m", "40 m", "5 m"], "The zeros are 0 and 20, so the vertex is halfway: <b><i>w</i> = 10 m</b> (area 100 m²)."),
        ("A company's profit is <i>P</i> = −2<i>x</i><sup>2</sup> + 40<i>x</i> − 50. What is the greatest profit?", "150", ["10", "350", "−50"], "<i>x</i> = −40 ÷ (−4) = 10. <i>P</i>(10) = −200 + 400 − 50 = <b>150</b>."),
        ("Which function has a vertex at (2, −3) and opens down?", "<i>y</i> = −(<i>x</i> − 2)<sup>2</sup> − 3", ["<i>y</i> = (<i>x</i> − 2)<sup>2</sup> − 3", "<i>y</i> = −(<i>x</i> + 2)<sup>2</sup> − 3", "<i>y</i> = −(<i>x</i> − 3)<sup>2</sup> + 2"], "Vertex form with <i>a</i> &lt; 0: <b><i>y</i> = −(<i>x</i> − 2)<sup>2</sup> − 3</b>."),
        ("What are the zeros of <i>y</i> = 2(<i>x</i> + 1)(<i>x</i> − 5)?", "−1 and 5", ["1 and −5", "2, −1 and 5", "−2 and 10"], "Set each factor to 0: <b>−1 and 5</b>. The 2 does not change the zeros."),
        ("What is the axis of symmetry of <i>y</i> = (<i>x</i> + 1)(<i>x</i> − 5)?", "<i>x</i> = 2", ["<i>x</i> = −2", "<i>x</i> = 4", "<i>y</i> = 2"], "Halfway between the zeros −1 and 5: <b><i>x</i> = 2</b>."),
        ("The graph of <i>y</i> = <i>x</i><sup>2</sup> is moved 3 units left and 4 units down. What is the new equation?", "<i>y</i> = (<i>x</i> + 3)<sup>2</sup> − 4", ["<i>y</i> = (<i>x</i> − 3)<sup>2</sup> − 4", "<i>y</i> = (<i>x</i> + 3)<sup>2</sup> + 4", "<i>y</i> = (<i>x</i> − 4)<sup>2</sup> + 3"], "Left 3 → (<i>x</i> + 3); down 4 → − 4."),
        ("How many <i>x</i>-intercepts does <i>y</i> = (<i>x</i> − 3)<sup>2</sup> + 2 have?", "0", ["1", "2", "3"], "The vertex (3, 2) is above the <i>x</i>-axis and the graph opens up, so it never touches it: <b>0</b>."),
        ("What is the range of <i>y</i> = −(<i>x</i> + 4)<sup>2</sup> + 6?", "<i>y</i> ≤ 6", ["<i>y</i> ≥ 6", "<i>y</i> ≤ −4", "All real numbers"], "It opens down with vertex (−4, 6): <b><i>y</i> ≤ 6</b>."),
        ("Over which interval is <i>y</i> = (<i>x</i> − 1)<sup>2</sup> decreasing?", "<i>x</i> &lt; 1", ["<i>x</i> &gt; 1", "<i>x</i> &lt; 0", "All real numbers"], "It opens up with vertex at <i>x</i> = 1, so it goes down to the left of the vertex: <b><i>x</i> &lt; 1</b>."),
        ("A bridge arch is <i>y</i> = −0.02<i>x</i><sup>2</sup> + 2<i>x</i> (meters). How high is the top of the arch?", "50 m", ["100 m", "2 m", "25 m"], "<i>x</i> = −2 ÷ (−0.04) = 50, and <i>y</i>(50) = −50 + 100 = <b>50 m</b>."),
        ("Which form shows the vertex of a parabola most directly?", "Vertex form <i>y</i> = <i>a</i>(<i>x</i> − <i>h</i>)<sup>2</sup> + <i>k</i>", ["Standard form <i>y</i> = <i>ax</i><sup>2</sup> + <i>bx</i> + <i>c</i>", "Factored form <i>y</i> = <i>a</i>(<i>x</i> − <i>p</i>)(<i>x</i> − <i>q</i>)", "Point-slope form"],
         "<b>Vertex form</b> shows (<i>h</i>, <i>k</i>). Factored form shows the zeros; standard form shows the <i>y</i>-intercept."),
        ("Which form shows the zeros of a parabola most directly?", "Factored form", ["Vertex form", "Standard form", "Slope-intercept form"], "In <i>y</i> = <i>a</i>(<i>x</i> − <i>p</i>)(<i>x</i> − <i>q</i>), the zeros are <i>p</i> and <i>q</i>: <b>factored form</b>."),
        ("What is the <i>y</i>-intercept of <i>y</i> = 3<i>x</i><sup>2</sup> − 5<i>x</i> + 7?", "(0, 7)", ["(7, 0)", "(0, 3)", "(0, −5)"], "Put <i>x</i> = 0: <i>y</i> = 7. <b>(0, 7)</b>."),
        ("The vertex of a parabola is (−2, 5) and it passes through (0, 1). What is <i>a</i> in <i>y</i> = <i>a</i>(<i>x</i> + 2)<sup>2</sup> + 5?", "−1", ["1", "−4", "4"], "1 = <i>a</i>(2)<sup>2</sup> + 5, so 4<i>a</i> = −4 and <b><i>a</i> = −1</b>."),
        ("Which parabola is the widest?", "<i>y</i> = ¼<i>x</i><sup>2</sup>", ["<i>y</i> = <i>x</i><sup>2</sup>", "<i>y</i> = 4<i>x</i><sup>2</sup>", "<i>y</i> = −2<i>x</i><sup>2</sup>"], "The smaller |<i>a</i>| is, the wider the parabola: <b>¼</b>."),
        ("A rocket's height is <i>h</i> = −5<i>t</i><sup>2</sup> + 40<i>t</i>. For how long is it in the air?", "8 seconds", ["4 seconds", "40 seconds", "5 seconds"], "−5<i>t</i>(<i>t</i> − 8) = 0, so it lands at <b><i>t</i> = 8</b>."),
        ("What is the average rate of change of <i>f</i>(<i>x</i>) = <i>x</i><sup>2</sup> from <i>x</i> = 1 to <i>x</i> = 4?", "5", ["3", "15", "4"], "(<i>f</i>(4) − <i>f</i>(1)) ÷ (4 − 1) = (16 − 1) ÷ 3 = <b>5</b>."),
        ("Write <i>y</i> = (<i>x</i> − 3)<sup>2</sup> + 1 in standard form.", "<i>y</i> = <i>x</i><sup>2</sup> − 6<i>x</i> + 10", ["<i>y</i> = <i>x</i><sup>2</sup> + 10", "<i>y</i> = <i>x</i><sup>2</sup> − 6<i>x</i> + 1", "<i>y</i> = <i>x</i><sup>2</sup> − 3<i>x</i> + 10"], "(<i>x</i> − 3)<sup>2</sup> = <i>x</i><sup>2</sup> − 6<i>x</i> + 9, plus 1: <b><i>x</i><sup>2</sup> − 6<i>x</i> + 10</b>."),
    ]
    return [T(q, a, w, e) for q, a, w, e in data]


def body():
    return lesson(
        "<p>The graph of a quadratic function is a <b>parabola</b>. If <i>a</i> &gt; 0 it opens up (it has a minimum); if <i>a</i> &lt; 0 it opens down (a maximum). "
        "The <b>vertex</b> is the turning point, and the <b>axis of symmetry</b> is the vertical line through it.</p>"
        "<ul><li>Standard form <i>y</i> = <i>ax</i><sup>2</sup> + <i>bx</i> + <i>c</i>: axis <i>x</i> = −<i>b</i>/2<i>a</i>; <i>y</i>-intercept (0, <i>c</i>).</li>"
        "<li>Vertex form <i>y</i> = <i>a</i>(<i>x</i> − <i>h</i>)<sup>2</sup> + <i>k</i>: vertex (<i>h</i>, <i>k</i>).</li>"
        "<li>Factored form <i>y</i> = <i>a</i>(<i>x</i> − <i>p</i>)(<i>x</i> − <i>q</i>): zeros <i>p</i> and <i>q</i>; the axis is halfway between them.</li></ul>",
        [("Find the vertex of <i>y</i> = <i>x</i><sup>2</sup> − 4<i>x</i> + 1.", ["<i>x</i> = −(−4) ÷ 2 = 2.", "<i>y</i> = 4 − 8 + 1 = −3."], "(2, −3)"),
         ("Describe <i>y</i> = −2(<i>x</i> + 1)<sup>2</sup> + 3.", ["<i>a</i> = −2: opens down, narrower.", "Vertex (−1, 3)."], "Maximum 3 at <i>x</i> = −1")],
        ["Sign errors in vertex form: (<i>x</i> + 3)<sup>2</sup> means <i>h</i> = −3.",
         "Using <i>x</i> = <i>b</i>/2<i>a</i> instead of −<i>b</i>/2<i>a</i>.",
         "Reading the <i>y</i>-intercept as a zero.",
         "Thinking a bigger |<i>a</i>| makes the parabola wider. It makes it narrower."])


def main():
    sets = [S("Read features from a graph", collect(one_read, 20, R)),
            S("Vertex and axis from standard form", collect(one_std, 20, R)),
            S("Vertex form and transformations", collect(one_vform, 20, R)),
            S("Zeros, intercepts and shape", collect(one_feature, 20, R)),
            S("Quadratic graph problems", problems())]
    make("graphing-quadratic-functions", 18, "F-IF.C.7",
         "Graphing Quadratic Functions: Vertex, Axis of Symmetry and Zeros",
         "Algebra 1 Graphing Quadratic Functions Worksheets: Vertex Form, Axis of Symmetry and Zeros (Free, Answer Key)",
         "Graphing quadratic functions",
         "Graph functions expressed symbolically and show key features of the graph. Graph linear and quadratic functions and show intercepts, maxima, and minima.",
         "Free Algebra 1 worksheets on graphing quadratic functions (F-IF.C.7a): read the vertex, axis of symmetry, zeros and y-intercept "
         "from a graph, use x = −b/2a, vertex form and transformations, and maximum and minimum problems. 100 questions with an answer key.",
         "Vertex form y = a(x − h)² + k shows the vertex (h, k).",
         "Axis of symmetry: x = −b/2a. a > 0 opens up; a < 0 opens down.",
         body(),
         [("How do you find the vertex of a parabola?", "In standard form, use x = −b/2a and substitute to find y. In vertex form y = a(x − h)² + k, the vertex is (h, k)."),
          ("What is the axis of symmetry?", "The vertical line through the vertex, x = −b/2a. The parabola is a mirror image on each side of it."),
          ("How do you know if a parabola opens up or down?", "Look at a, the coefficient of x². If a is positive it opens up; if it is negative it opens down."),
          ("How do you find the maximum height in a projectile problem?", "Find the vertex: the time is t = −b/2a, and the maximum height is the value of the function at that time.")],
         sets, R, domain="Quadratics")


if __name__ == "__main__":
    main()
