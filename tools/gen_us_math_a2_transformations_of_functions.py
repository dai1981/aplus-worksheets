# -*- coding: utf-8 -*-
"""
US Algebra 2: Transformations of Functions (Common Core F-BF.B.3)
  python3 tools/gen_us_math_a2_transformations_of_functions.py
Describing shifts, reflections and stretches; writing the equation of a transformed parent function; moving
points; matching graphs; and even and odd functions.
Wrong answers come from real mistakes: shifting the wrong way for f(x − h), mixing up reflections over the
x-axis and the y-axis, confusing a vertical stretch with a horizontal one, and adding k inside the parentheses.
"""
import math
import random
from fractions import Fraction as F
from us_hs import B, S, make, lesson, collect, T, fig, num, MINUS, fr
from g8_common import grid_svg
from a2_common import X, sf, lin
from us_geo import BLUE, RED

R = random.Random(95801)
GRAY = "#9a9a9a"
PARENTS = {
    "abs": ("|%s|", lambda x: abs(x), "absolute value"),
    "sq": ("%s²", lambda x: x * x, "quadratic"),
    "sqrt": ("√%s", lambda x: math.sqrt(x) if x >= 0 else None, "square root"),
    "cube": ("%s³", lambda x: x ** 3, "cubic"),
}


def inner(h):
    return X if h == 0 else "(%s)" % lin(h)


def g_text(kind, a, h, k):
    fmt = PARENTS[kind][0]
    core = fmt % (inner(h) if kind != "abs" else lin(h) if h else X)
    if kind == "sqrt":
        core = "√" + ("(%s)" % lin(h) if h else X)
    if kind == "abs":
        core = "|%s|" % (lin(h) if h else X)
    pre = "" if a == 1 else (MINUS if a == -1 else sf(a))
    s = pre + core
    if k:
        s += " %s %s" % ("+" if k > 0 else MINUS, num(abs(k)))
    return "<i>g</i>(<i>x</i>) = " + s


def words(a, h, k):
    parts = []
    if a < 0:
        parts.append("reflect over the <i>x</i>-axis")
    if abs(a) != 1:
        parts.append("vertical %s by a factor of %s" % ("stretch" if abs(a) > 1 else "shrink", sf(abs(a))))
    if h:
        parts.append("%s %d" % ("right" if h > 0 else "left", abs(h)))
    if k:
        parts.append("%s %d" % ("up" if k > 0 else "down", abs(k)))
    return ", ".join(parts)


# ------------------------------------------------------------ set 1: describe the transformation
def one_desc(r):
    kind = r.choice(list(PARENTS))
    h, k = r.choice([x for x in range(-6, 7) if x]), r.choice([x for x in range(-6, 7) if x])
    q = "Describe how the graph of %s is related to the graph of the parent function %s." % (B(g_text(kind, 1, h, k)), B("<i>f</i>(<i>x</i>) = " + (PARENTS[kind][0] % X)))
    right = "Shift %s" % words(1, h, k)
    wr = ["Shift %s" % words(1, -h, k), "Shift %s" % words(1, h, -k), "Shift %s" % words(1, -h, -k)]
    return T(q, right, wr, "Inside the function, (<i>x</i> %s %s) moves the graph the opposite way: %s %d. Outside, %s%d moves it %s. <b>%s</b>." % (
        MINUS if h > 0 else "+", num(abs(h)), "right" if h > 0 else "left", abs(h), "+" if k > 0 else MINUS, abs(k), "up" if k > 0 else "down", right))


# ------------------------------------------------------------ set 2: write the equation
def one_write(r):
    kind = r.choice(list(PARENTS))
    a = r.choice([1, 1, -1, 2, 3, F(1, 2), -2])
    h, k = r.randint(-5, 5), r.randint(-5, 5)
    if h == 0 and k == 0:
        return None
    desc = words(a, h, k)
    q = "The graph of %s is transformed: %s. Write the new function." % (B("<i>f</i>(<i>x</i>) = " + (PARENTS[kind][0] % X)), desc)
    right = g_text(kind, a, h, k)
    wr = [g_text(kind, a, -h, k), g_text(kind, -a, h, k) if a != 1 or True else g_text(kind, a, h, -k), g_text(kind, a, h, -k)]
    if h == 0:
        wr[0] = g_text(kind, a, k, 0) if k else g_text(kind, a, 1, k)
    return T(q, right, [w for w in dict.fromkeys(wr) if w != right][:3],
             "Horizontal shifts go inside with the opposite sign, vertical shifts go outside, and the stretch or reflection multiplies the function. <b>%s</b>." % right)


# ------------------------------------------------------------ set 3: move a point
def one_point(r):
    px, py = r.randint(-4, 4), r.randint(-4, 4)
    kind = r.choice(["shift", "shift", "refx", "refy", "stretch", "hstretch"])
    if kind == "shift":
        h, k = r.choice([x for x in range(-5, 6) if x]), r.choice([x for x in range(-5, 6) if x])
        rule = "<i>g</i>(<i>x</i>) = <i>f</i>(%s) %s %d" % (lin(h), "+" if k > 0 else MINUS, abs(k))
        ans = (px + h, py + k)
        wr = [(px - h, py + k), (px + h, py - k), (px + k, py + h)]
        e = "<i>x</i> %s %d inside moves the point %s %d; %s%d outside moves it %s %d." % (MINUS if h > 0 else "+", abs(h), "right" if h > 0 else "left", abs(h), "+" if k > 0 else MINUS, abs(k), "up" if k > 0 else "down", abs(k))
    elif kind == "refx":
        rule = "<i>g</i>(<i>x</i>) = %s<i>f</i>(<i>x</i>)" % MINUS
        ans = (px, -py)
        wr = [(-px, py), (-px, -py), (py, px)]
        e = "%s<i>f</i>(<i>x</i>) reflects over the <i>x</i>-axis: the <i>y</i>-coordinate changes sign." % MINUS
    elif kind == "refy":
        rule = "<i>g</i>(<i>x</i>) = <i>f</i>(%s<i>x</i>)" % MINUS
        ans = (-px, py)
        wr = [(px, -py), (-px, -py), (py, px)]
        e = "<i>f</i>(%s<i>x</i>) reflects over the <i>y</i>-axis: the <i>x</i>-coordinate changes sign." % MINUS
    elif kind == "stretch":
        a = r.choice([2, 3, 4])
        rule = "<i>g</i>(<i>x</i>) = %d<i>f</i>(<i>x</i>)" % a
        ans = (px, a * py)
        wr = [(a * px, py), (a * px, a * py), (px, py + a)]
        e = "Multiplying the output by %d is a vertical stretch: multiply the <i>y</i>-coordinate by %d." % (a, a)
    else:
        a = r.choice([2, 3])
        if px % a:
            return None
        rule = "<i>g</i>(<i>x</i>) = <i>f</i>(%d<i>x</i>)" % a
        ans = (F(px, a), py)
        wr = [(a * px, py), (px, a * py), (px, F(py, a))]
        e = "Multiplying the input by %d is a horizontal shrink: divide the <i>x</i>-coordinate by %d." % (a, a)
    if ans == (px, py):
        return None
    pt = lambda p: "(%s, %s)" % (sf(p[0]), sf(p[1]))
    q = "The point %s is on the graph of <i>f</i>. Which point must be on the graph of %s?" % (B(pt((px, py))), B(rule))
    return T(q, pt(ans), [pt(w) for w in dict.fromkeys(wr) if w != ans][:3], e + " <b>%s</b>." % pt(ans))


# ------------------------------------------------------------ set 4: match the graph
def one_graph(r):
    kind = r.choice(list(PARENTS))
    a = r.choice([1, 1, -1, 2, -1])
    h, k = r.randint(-3, 3), r.randint(-3, 3)
    if h == 0 and k == 0:
        return None
    f = PARENTS[kind][1]
    segs = []
    n = 160
    for col, fn in ((GRAY, lambda x: f(x)), (BLUE, lambda x: (None if f(x - h) is None else a * f(x - h) + k))):
        prev = None
        for i in range(n + 1):
            x = -6 + 12 * i / n
            y = fn(x)
            if y is not None and abs(y) <= 6 and prev is not None:
                segs.append((prev[0], prev[1], x, y, col))
            prev = (x, y) if (y is not None and abs(y) <= 6) else None
    svg = grid_svg(-6, 6, segs=segs, unit=20, label="graph of a parent function (gray) and a transformed function (blue)")
    q = "The gray graph is %s. Which equation matches the blue graph?%s" % (B("<i>f</i>(<i>x</i>) = " + (PARENTS[kind][0] % X)), fig(svg))
    right = g_text(kind, a, h, k)
    wr = [g_text(kind, a, -h, k), g_text(kind, a, h, -k) if k else g_text(kind, a, h, 1), g_text(kind, -a, h, k)]
    return T(q, right, [w for w in dict.fromkeys(wr) if w != right][:3],
             "The key point moved from (0, 0) to (%s, %s)%s. <b>%s</b>." % (sf(h), sf(k), " and the graph is flipped upside down" if a < 0 else (" and the graph is stretched vertically by 2" if a == 2 else ""), right))


# ------------------------------------------------------------ set 5: even and odd functions, domain and range
def one_eo(r):
    kind = r.choice(["eo", "eo", "eo", "range", "domain"])
    if kind == "eo":
        items = [("<i>f</i>(<i>x</i>) = <i>x</i>⁴ %s 3<i>x</i>²" % MINUS, "Even"), ("<i>f</i>(<i>x</i>) = <i>x</i>³ + 2<i>x</i>", "Odd"), ("<i>f</i>(<i>x</i>) = <i>x</i>² + <i>x</i>", "Neither"),
                 ("<i>f</i>(<i>x</i>) = |<i>x</i>| + 5", "Even"), ("<i>f</i>(<i>x</i>) = 5<i>x</i>", "Odd"), ("<i>f</i>(<i>x</i>) = (<i>x</i> %s 1)²" % MINUS, "Neither"),
                 ("<i>f</i>(<i>x</i>) = <i>x</i>⁵ %s <i>x</i>" % MINUS, "Odd"), ("<i>f</i>(<i>x</i>) = 7", "Even"), ("<i>f</i>(<i>x</i>) = <i>x</i>³ + 1", "Neither"),
                 ("<i>f</i>(<i>x</i>) = %s2<i>x</i>⁶ + <i>x</i>² %s 4" % (MINUS, MINUS), "Even")]
        fx, right = r.choice(items)
        why = {"Even": "<i>f</i>(%s<i>x</i>) = <i>f</i>(<i>x</i>), so the graph is symmetric about the <i>y</i>-axis." % MINUS,
               "Odd": "<i>f</i>(%s<i>x</i>) = %s<i>f</i>(<i>x</i>), so the graph is symmetric about the origin." % (MINUS, MINUS),
               "Neither": "<i>f</i>(%s<i>x</i>) equals neither <i>f</i>(<i>x</i>) nor %s<i>f</i>(<i>x</i>)." % (MINUS, MINUS)}[right]
        return T("Is %s even, odd, or neither?" % B(fx), right, [x for x in ["Even", "Odd", "Neither", "Both even and odd"] if x != right], why + " <b>%s</b>." % right)
    k, h = r.randint(-6, 6), r.randint(-6, 6)
    if kind == "range":
        a = r.choice([1, -1, 2, -3])
        fx = g_text("abs", a, h, k)
        right = "<i>y</i> %s %s" % ("≥" if a > 0 else "≤", sf(k))
        return T("What is the range of %s?" % B(fx), right, ["<i>y</i> %s %s" % ("≤" if a > 0 else "≥", sf(k)), "<i>y</i> %s %s" % ("≥" if a > 0 else "≤", sf(h)), "All real numbers"],
                 "The vertex is (%s, %s) and the graph opens %s. <b>%s</b>." % (sf(h), sf(k), "up" if a > 0 else "down", right))
    fx = g_text("sqrt", 1, h, k)
    right = "<i>x</i> ≥ %s" % sf(h)
    return T("What is the domain of %s?" % B(fx), right, ["<i>x</i> ≥ %s" % sf(-h) if h else "<i>x</i> ≥ 1", "<i>x</i> ≥ %s" % sf(k) if k != h else "<i>x</i> ≤ %s" % sf(h), "All real numbers"],
             "The expression under the root must be ≥ 0: %s ≥ 0. <b>%s</b>." % (lin(h) if h else X, right))


def build():
    sets = [S("Describe the transformation", collect(one_desc, 20, R)),
            S("Write the transformed function", collect(one_write, 20, R)),
            S("Move a point", collect(one_point, 20, R)),
            S("Match the graph", collect(one_graph, 20, R)),
            S("Even and odd functions, domain and range", collect(one_eo, 20, R))]
    body = lesson(
        "<p>For <i>g</i>(<i>x</i>) = <i>a</i> · <i>f</i>(<i>x</i> %s <i>h</i>) + <i>k</i>:</p>"
        "<ul><li><i>h</i> shifts the graph <b>horizontally</b>, the opposite of the sign you see: <i>f</i>(<i>x</i> %s 3) moves right 3.</li>"
        "<li><i>k</i> shifts it <b>vertically</b>: + up, %s down.</li>"
        "<li><i>a</i> stretches it vertically (|<i>a</i>| &gt; 1) or shrinks it (0 &lt; |<i>a</i>| &lt; 1). A negative <i>a</i> reflects it over the <i>x</i>-axis.</li>"
        "<li><i>f</i>(%s<i>x</i>) reflects over the <i>y</i>-axis.</li></ul>"
        "<p>A function is <b>even</b> if <i>f</i>(%s<i>x</i>) = <i>f</i>(<i>x</i>) (symmetric about the <i>y</i>-axis) and <b>odd</b> if <i>f</i>(%s<i>x</i>) = %s<i>f</i>(<i>x</i>) (symmetric about the origin).</p>" % (
            MINUS, MINUS, MINUS, MINUS, MINUS, MINUS, MINUS),
        [("Describe <i>g</i>(<i>x</i>) = %s2|<i>x</i> + 1| + 4." % MINUS, ["Reflect over the <i>x</i>-axis and stretch by 2", "Left 1, up 4"], "Vertex moves from (0, 0) to (%s1, 4)" % MINUS),
         ("(2, 5) is on <i>f</i>. Where is it on <i>g</i>(<i>x</i>) = <i>f</i>(<i>x</i> + 3) %s 1?" % MINUS, ["Left 3, down 1"], "(%s1, 4)" % MINUS)],
        ["Shifting right for (<i>x</i> + 3). Inside the function, the shift is the opposite way: left 3.",
         "Putting the vertical shift inside the parentheses.",
         "Mixing up %s<i>f</i>(<i>x</i>) (over the <i>x</i>-axis) and <i>f</i>(%s<i>x</i>) (over the <i>y</i>-axis)." % (MINUS, MINUS),
         "Thinking every function is either even or odd. Many are neither."])
    faq = [("How do you shift a graph to the right?", "Replace x with (x − h). For example, f(x − 4) is the graph of f moved 4 units right."),
           ("What does a negative sign in front of a function do?", "−f(x) reflects the graph over the x-axis. A negative inside, f(−x), reflects it over the y-axis."),
           ("What is the difference between a vertical stretch and a horizontal stretch?", "a·f(x) multiplies the y-values (vertical). f(bx) divides the x-values by b (horizontal)."),
           ("How can you tell if a function is even or odd?", "Find f(−x). If it equals f(x), the function is even. If it equals −f(x), the function is odd.")]
    make("transformations-of-functions", 8, "F-BF.B.3",
         "Transformations of Functions: Shifts, Reflections, and Stretches",
         "Transformations of Functions Worksheet: Shifts, Reflections, Stretches (Algebra 2) | 100 Questions",
         "Transformations of Functions",
         "Identify the effect on the graph of replacing f(x) by f(x) + k, k f(x), f(kx), and f(x + k) for specific values of k (both positive and negative); find the value of k given the graphs. Recognize even and odd functions from their graphs and algebraic expressions for them.",
         "Free Algebra 2 worksheet on transformations of functions: shifts, reflections, stretches, moving points, matching graphs and even and odd functions. 100 questions with answers.",
         "g(x) = a·f(x − h) + k: h moves left/right (opposite sign), k moves up/down.",
         "A negative a reflects over the x-axis; |a| > 1 stretches the graph.",
         body, faq, sets, R, domain="Functions", grade="algebra-2")


if __name__ == "__main__":
    build()
