# -*- coding: utf-8 -*-
"""
US Algebra 2: Graphs of Sine and Cosine (Common Core F-TF.B.5, F-IF.C.7e, F-BF.B.3)
  python3 tools/gen_us_math_a2_graphs_of_sine_and_cosine.py
Amplitude, period, midline and maximum and minimum values; horizontal (phase) shifts; matching graphs to
equations; writing an equation from a graph; and periodic models such as Ferris wheels and tides.
Wrong answers come from real mistakes: giving b as the period instead of 2π/b, using a negative amplitude,
reading the midline from the maximum, and shifting the wrong way.
"""
import math
import random
from fractions import Fraction as F
from us_hs import B, S, make, lesson, collect, T, fig, num, MINUS, fr
from a2_common import sf
from g8_common import grid_svg
from us_geo import BLUE

R = random.Random(96401)
X = "<i>x</i>"


def pis(f):
    """f·π as text"""
    f = F(f)
    if f == 0:
        return "0"
    top = ("" if abs(f.numerator) == 1 else str(abs(f.numerator))) + "π"
    s = top if f.denominator == 1 else fr(top, f.denominator)
    return (MINUS if f < 0 else "") + s


def eq(fn, a, b, c, d):
    """y = a fn(b(x - c)) + d with c a multiple of π (Fraction)"""
    pre = "" if a == 1 else (MINUS if a == -1 else sf(a))
    if c:
        inner = "%s(%s %s %s)" % ("" if b == 1 else sf(b), X, MINUS if c > 0 else "+", pis(abs(c)))
    else:
        inner = ("" if b == 1 else sf(b)) + X
    s = "<i>y</i> = %s%s %s" % (pre + " " if pre and pre != MINUS else pre, fn, inner)
    s = s.replace("%s %s(" % (fn, ""), "%s(" % fn) if False else s
    if d:
        s += " %s %s" % ("+" if d > 0 else MINUS, num(abs(d)))
    return s


# ------------------------------------------------------------ set 1: amplitude and period
def one_ap(r):
    a = r.choice([1, 2, 3, 4, 5, -2, -3, F(1, 2)])
    b = r.choice([1, 2, 3, 4, F(1, 2), F(1, 3), 6])
    fn = r.choice(["sin", "cos"])
    want = r.choice(["amp", "per", "per"])
    e_ = eq(fn, a, b, 0, 0)
    per = F(2, 1) / F(b)
    if want == "amp":
        q = "What is the amplitude of %s?" % B(e_)
        ans = sf(abs(F(a)))
        return T(q, ans, [w for w in dict.fromkeys([sf(a) if a < 0 else sf(2 * F(a)), sf(b), pis(per)]) if w != ans][:3],
                 "Amplitude is |<i>a</i>| = |%s| = <b>%s</b>. It is always positive; a negative <i>a</i> only flips the graph." % (sf(a), ans))
    q = "What is the period of %s?" % B(e_)
    ans = pis(per)
    return T(q, ans, [w for w in dict.fromkeys([sf(b), pis(F(b, 2) if False else F(1) / F(b)), pis(2 * F(b)), sf(per * 180) + "°" if False else pis(per * 2)]) if w != ans][:3],
             "Period = 2π ÷ |<i>b</i>| = 2π ÷ %s = <b>%s</b>." % (sf(b), ans))


# ------------------------------------------------------------ set 2: midline, max and min
def one_mid(r):
    a = r.choice([1, 2, 3, 4, 5])
    d = r.choice([x for x in range(-5, 7) if x])
    b = r.choice([1, 2, 3])
    fn = r.choice(["sin", "cos"])
    sign = r.choice([1, 1, -1])
    e_ = eq(fn, sign * a, b, 0, d)
    want = r.choice(["mid", "max", "min", "range"])
    if want == "mid":
        right = "<i>y</i> = %s" % sf(d)
        return T("What is the midline of %s?" % B(e_), right, ["<i>y</i> = %s" % sf(d + a), "<i>y</i> = %s" % sf(-d), "<i>y</i> = %s" % sf(a)],
                 "The vertical shift <i>d</i> = %s sets the midline: <b>%s</b>." % (sf(d), right))
    if want == "max":
        return T("What is the maximum value of %s?" % B(e_), sf(d + a), [sf(d - a), sf(d), sf(a)],
                 "Midline %s plus the amplitude %d: <b>%s</b>." % (sf(d), a, sf(d + a)))
    if want == "min":
        return T("What is the minimum value of %s?" % B(e_), sf(d - a), [sf(d + a), sf(-a), sf(d)],
                 "Midline %s minus the amplitude %d: <b>%s</b>." % (sf(d), a, sf(d - a)))
    right = "%s ≤ <i>y</i> ≤ %s" % (sf(d - a), sf(d + a))
    return T("What is the range of %s?" % B(e_), right, ["%s ≤ <i>y</i> ≤ %s" % (sf(-a), sf(a)), "%s ≤ <i>y</i> ≤ %s" % (sf(d - 2 * a), sf(d + 2 * a)), "All real numbers"],
             "The graph goes from the midline %s down %d and up %d. <b>%s</b>." % (sf(d), a, a, right))


# ------------------------------------------------------------ set 3: phase shift
def one_shift(r):
    c = F(r.choice([1, 1, 1, 1, 2, 3]), r.choice([2, 3, 4, 6]))
    c = c * r.choice([1, -1])
    fn = r.choice(["sin", "cos"])
    d = r.choice([0, 0, 1, -2, 3])
    a = r.choice([1, 2, 3])
    e_ = eq(fn, a, 1, c, d)
    right = "%s units %s" % (pis(abs(c)), "right" if c > 0 else "left")
    q = "Describe the horizontal shift of %s compared with %s." % (B(e_), B("<i>y</i> = %s%s %s" % ("" if a == 1 else num(a) + " ", fn, X) + ((" %s %d" % ("+" if d > 0 else MINUS, abs(d))) if d else "")))
    return T(q, right, ["%s units %s" % (pis(abs(c)), "left" if c > 0 else "right"), "%s units up" % pis(abs(c)), "%s units %s" % (pis(abs(c) * 2), "right" if c > 0 else "left")],
             "(<i>x</i> %s %s) inside the function moves the graph the opposite way of the sign: <b>%s</b>." % (MINUS if c > 0 else "+", pis(abs(c)), right))


# ------------------------------------------------------------ set 4: from a graph
def tgraph(fn, a, b, d):
    unit = 18
    segs = []
    f = math.sin if fn == "sin" else math.cos
    n = 300
    lo, hi = 0, 12
    xs = [lo + (hi - lo) * i / n for i in range(n + 1)]
    pts = [(x, a * f(b * x * math.pi / 6) + d) for x in xs]
    for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
        segs.append((x1, y1, x2, y2, BLUE))
    ylo, yhi = min(-1, d - abs(a) - 1), max(1, d + abs(a) + 1)
    return grid_svg(lo, hi, segs=segs, unit=unit, label="graph of a sine or cosine function", ylo=int(math.floor(ylo)), yhi=int(math.ceil(yhi)))


def one_graph(r):
    a = r.choice([1, 2, 3, 4])
    d = r.choice([-2, 0, 0, 1, 2, 3])
    b = r.choice([1, 2])
    fn = r.choice(["sin", "cos"])
    sign = r.choice([1, -1])
    # x-axis is in units of π/6 per grid unit, so period 2π/b = 12/b units
    svg = tgraph(fn, sign * a, b, d)
    per = F(2, b)
    right = "<i>y</i> = %s%s %s%s%s" % ("" if sign * a == 1 else (MINUS if sign * a == -1 else sf(sign * a) + " "), fn, "" if b == 1 else num(b), X,
                                        (" %s %d" % ("+" if d > 0 else MINUS, abs(d))) if d else "")
    def var(aa, bb, dd, f2=fn):
        return "<i>y</i> = %s%s %s%s%s" % ("" if aa == 1 else (MINUS if aa == -1 else sf(aa) + " "), f2, "" if bb == 1 else num(bb), X, (" %s %d" % ("+" if dd > 0 else MINUS, abs(dd))) if dd else "")
    wr = [var(-sign * a, b, d), var(sign * a, 3 - b, d), var(sign * a, b, -d) if d else var(sign * a * 2 if a < 3 else sign, b, d)]
    q = "Each grid unit on the <i>x</i>-axis is π/6, so the mark 6 is π and 12 is 2π. Which equation matches the graph?%s" % fig(svg)
    return T(q, right, [w for w in dict.fromkeys(wr) if w != right][:3],
             "Midline <i>y</i> = %s, amplitude %d, period %s (%d grid units), and the graph %s at <i>x</i> = 0, so it is %s%s. <b>%s</b>." % (
                 sf(d), a, pis(per), 12 // b, "starts on the midline going " + ("up" if sign > 0 else "down") if fn == "sin" else "starts at a " + ("maximum" if sign > 0 else "minimum"),
                 "" if sign > 0 else "a negative ", fn, right))


# ------------------------------------------------------------ set 5: periodic models
def one_model(r):
    kind = r.choice(["ferris", "ferris", "tide", "temp", "b"])
    if kind == "ferris":
        dia = r.choice([40, 50, 60, 80, 100, 120])
        ctr = dia // 2 + r.choice([3, 5, 8, 10])
        T_ = r.choice([2, 4, 5, 6, 8, 10])
        want = r.choice(["amp", "mid", "per", "max"])
        q = "A Ferris wheel has a diameter of %d ft, its center is %d ft above the ground, and it turns once every %d minutes. " % (dia, ctr, T_)
        if want == "amp":
            return T(q + "What is the amplitude of the height function?", "%d ft" % (dia // 2), ["%d ft" % dia, "%d ft" % ctr, "%d ft" % (ctr + dia // 2)],
                     "The amplitude is the radius: %d ÷ 2 = <b>%d ft</b>." % (dia, dia // 2))
        if want == "mid":
            return T(q + "What is the midline of the height function?", "<i>h</i> = %d ft" % ctr, ["<i>h</i> = %d ft" % (dia // 2), "<i>h</i> = %d ft" % (ctr + dia // 2), "<i>h</i> = %d ft" % dia],
                     "The midline is the height of the center: <b><i>h</i> = %d ft</b>." % ctr)
        if want == "max":
            return T(q + "What is the greatest height of a seat?", "%d ft" % (ctr + dia // 2), ["%d ft" % (ctr + dia), "%d ft" % ctr, "%d ft" % dia],
                     "Center height plus radius: %d + %d = <b>%d ft</b>." % (ctr, dia // 2, ctr + dia // 2))
        b = F(2, T_)
        return T(q + "In <i>h</i>(<i>t</i>) = <i>a</i> cos(<i>bt</i>) + <i>d</i>, what is <i>b</i>?", pis(b), [num(T_), pis(F(T_, 2)), pis(F(1, T_))],
                 "Period = 2π ÷ <i>b</i>, so <i>b</i> = 2π ÷ %d = <b>%s</b>." % (T_, pis(b)))
    if kind == "tide":
        hi, lo = r.choice([(12, 2), (10, 4), (14, 6), (9, 1), (16, 4)])
        q = "At a harbor, high tide is %d ft and low tide is %d ft. What are the amplitude and midline of a sine model for the water depth?" % (hi, lo)
        right = "Amplitude %s ft, midline <i>y</i> = %s ft" % (num(F(hi - lo, 2)), num(F(hi + lo, 2)))
        return T(q, right, ["Amplitude %d ft, midline <i>y</i> = %s ft" % (hi - lo, num(F(hi + lo, 2))), "Amplitude %s ft, midline <i>y</i> = %d ft" % (num(F(hi - lo, 2)), lo),
                            "Amplitude %d ft, midline <i>y</i> = %d ft" % (hi, lo)],
                 "Amplitude = (max %s min) ÷ 2 = %s. Midline = (max + min) ÷ 2 = %s. <b>%s</b>." % (MINUS, num(F(hi - lo, 2)), num(F(hi + lo, 2)), right))
    if kind == "temp":
        avg, sw = r.choice([(55, 20), (60, 15), (70, 10), (50, 25), (65, 18)])
        q = "The average monthly temperature in a city is modeled by <i>T</i>(<i>m</i>) = %d sin(π<i>m</i>/6) + %d. What is the period, in months?" % (sw, avg)
        return T(q, "12 months", ["6 months", "%d months" % sw, "π/6 months"], "Period = 2π ÷ (π/6) = <b>12 months</b>, one year.")
    p = r.choice([4, 8, 10, 12, 24, 365])
    q = "A periodic model has period %d. Which value of <i>b</i> should be used in <i>y</i> = sin(<i>bx</i>)?" % p
    return T(q, pis(F(2, p)), [num(p), pis(F(p, 2)), pis(2 * p)], "<i>b</i> = 2π ÷ period = 2π ÷ %d = <b>%s</b>." % (p, pis(F(2, p))))


def build():
    sets = [S("Amplitude and period", collect(one_ap, 20, R)),
            S("Midline, maximum and minimum", collect(one_mid, 20, R)),
            S("Horizontal shifts", collect(one_shift, 20, R)),
            S("Match the graph", collect(one_graph, 20, R)),
            S("Periodic models", collect(one_model, 20, R))]
    body = lesson(
        "<p>For <i>y</i> = <i>a</i> sin(<i>b</i>(<i>x</i> %s <i>c</i>)) + <i>d</i> (or cos):</p>"
        "<ul><li><b>Amplitude</b> = |<i>a</i>|, half the distance from the maximum to the minimum. A negative <i>a</i> flips the graph.</li>"
        "<li><b>Period</b> = 2π ÷ |<i>b</i>|, the length of one full cycle.</li>"
        "<li><b>Midline</b>: <i>y</i> = <i>d</i>. The maximum is <i>d</i> + |<i>a</i>| and the minimum is <i>d</i> %s |<i>a</i>|.</li>"
        "<li><b>Horizontal shift</b> <i>c</i>: right for (<i>x</i> %s <i>c</i>), left for (<i>x</i> + <i>c</i>).</li></ul>"
        "<p>sin <i>x</i> starts on the midline going up; cos <i>x</i> starts at a maximum.</p>" % (MINUS, MINUS, MINUS),
        [("Find the amplitude, period and midline of <i>y</i> = 3 cos(2<i>x</i>) %s 1." % MINUS, ["|<i>a</i>| = 3", "2π ÷ 2 = π", "<i>d</i> = %s1" % MINUS], "3, π, <i>y</i> = %s1" % MINUS),
         ("A Ferris wheel 60 ft across has its center 35 ft up and turns every 4 min. Write <i>h</i>(<i>t</i>).", ["Amplitude 30, midline 35", "<i>b</i> = 2π/4 = π/2", "Start at the bottom: %scos" % MINUS],
          "<i>h</i> = %s30 cos(π<i>t</i>/2) + 35" % MINUS)],
        ["Giving <i>b</i> as the period. The period is 2π ÷ <i>b</i>.",
         "Giving a negative amplitude. Amplitude is a distance, so it is positive.",
         "Taking the midline from the maximum. It is halfway between the maximum and the minimum.",
         "Shifting right for (<i>x</i> + <i>c</i>). The shift is to the left."])
    faq = [("How do you find the period of a sine function?", "Divide 2π by |b|. For y = sin(3x), the period is 2π/3."),
           ("What is the amplitude of a trig function?", "|a|, half the distance between the maximum and the minimum values."),
           ("What is the midline of a sinusoidal graph?", "The horizontal line y = d halfway between the maximum and minimum. It comes from the vertical shift."),
           ("What is the difference between the graphs of sine and cosine?", "They have the same shape. cos x is sin x shifted left π/2, so cos starts at a maximum and sin starts on the midline.")]
    make("graphs-of-sine-and-cosine", 14, "F-TF.B.5",
         "Graphs of Sine and Cosine: Amplitude, Period, and Midline",
         "Graphing Sine and Cosine Worksheet: Amplitude, Period, Midline (Algebra 2) | 100 Questions",
         "Graphs of Sine and Cosine",
         "Choose trigonometric functions to model periodic phenomena with specified amplitude, frequency, and midline.",
         "Free Algebra 2 worksheet on graphs of sine and cosine: amplitude, period, midline, phase shift, matching graphs and periodic models like Ferris wheels and tides. 100 questions.",
         "Amplitude |a|, period 2π/|b|, midline y = d.",
         "sin starts on the midline going up; cos starts at a maximum.",
         body, faq, sets, R, domain="Trigonometric Functions", grade="algebra-2")


if __name__ == "__main__":
    build()
