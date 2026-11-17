# -*- coding: utf-8 -*-
"""
US Geometry: Pythagorean Theorem and Special Right Triangles (Common Core G-SRT.B.4, G-SRT.C.8)
  python3 tools/gen_us_math_ge_pythagorean_theorem_and_special_right_triangles.py
Finding a hypotenuse or a leg in simplest radical form, classifying triangles with the converse,
45°-45°-90° and 30°-60°-90° triangles, and word problems.
Wrong answers come from real mistakes: adding the legs, adding instead of subtracting to find a leg,
not simplifying the radical, multiplying by √2 instead of dividing, and mixing up the short and long legs.
"""
import math
import random
from us_hs import B, S, make, lesson, collect, T, fig, num, MINUS, People
from us_geo import Canvas, RED, GREEN, BLUE

R = random.Random(93501)


def rad(n):
    """simplest radical form of √n (n integer)"""
    a = 1
    for k in range(math.isqrt(n), 1, -1):
        if n % (k * k) == 0:
            a = k
            break
    b = n // (a * a)
    if b == 1:
        return num(a)
    return ("" if a == 1 else num(a)) + "√" + num(b)


def crad(c, b):
    """c√b"""
    if b == 1:
        return num(c)
    return ("" if c == 1 else num(c)) + "√" + num(b)


def dims(a, b):
    k = min(220 / b, 160 / a)
    return max(60, b * k), max(60, a * k)


def rt_fig(a_lab, b_lab, c_lab, ang=None, w=200, h=120):
    """right angle at bottom left; a = vertical leg, b = horizontal leg, c = hypotenuse; ang = (vertex, text)"""
    P, Q, Rr = (20, 20 + h), (20 + w, 20 + h), (20, 20)
    c = Canvas()
    c.poly([P, Q, Rr])
    c.right(P, Q, Rr)
    cen = (20 + w / 3, 20 + 2 * h / 3)
    for (p, q), t in (((P, Rr), a_lab), ((P, Q), b_lab), ((Q, Rr), c_lab)):
        if t:
            pl = t.replace("<i>", "").replace("</i>", "")
            c.side_label(p, q, t, cen, 16 + 3 * max(0, len(pl) - 2), 14, RED if t == "<i>x</i>" else "#2b2b2b")
    if ang:
        v, t = ang
        if v == "Q":
            c.angle(Q, P, Rr, "", r=24)
            c.angle_text(Q, P, Rr, t, r=50, fs=13)
        else:
            c.angle(Rr, P, Q, "", r=22)
            c.angle_text(Rr, P, Q, t, r=44, fs=13)
    return c.svg("right triangle, not drawn to scale")


# ------------------------------------------------------------ set 1: find a side
def one_side(r):
    a, b = r.randint(2, 15), r.randint(2, 15)
    kind = r.choice(["hyp", "hyp", "leg"])
    if kind == "hyp":
        n = a * a + b * b
        right = rad(n)
        q = "Find <i>x</i>. Give your answer in simplest radical form if needed.%s" % fig(rt_fig(num(a), num(b), "<i>x</i>", None, *dims(a, b)))
        wr = [num(a + b), num(n), rad(abs(a * a - b * b)) if a != b else num(2 * a + 1), crad(a + b, 2) if a != b else num(a * a)]
        e = "<i>a</i>² + <i>b</i>² = <i>c</i>²: %d + %d = %d, so <i>x</i> = %s<b>%s</b>." % (a * a, b * b, n, "" if right == "√" + num(n) else "√%s = " % num(n), right)
        return T(q, right, [w for w in dict.fromkeys(wr) if w != right][:3], e)
    c_ = max(a, b) + r.randint(1, 8)
    a = min(a, b)
    n = c_ * c_ - a * a
    right = rad(n)
    q = "Find <i>x</i>. Give your answer in simplest radical form if needed.%s" % fig(rt_fig(num(a), "<i>x</i>", num(c_), None, *dims(a, math.sqrt(n))))
    wr = [rad(c_ * c_ + a * a), num(c_ - a), num(n), rad(n * 4) if right != rad(n * 4) else num(c_ + a)]
    e = "The hypotenuse is %d. <i>x</i>² = %d² %s %d² = %d %s %d = %d, so <i>x</i> = <b>%s</b>." % (c_, c_, MINUS, a, c_ * c_, MINUS, a * a, n, right)
    return T(q, right, [w for w in dict.fromkeys(wr) if w != right][:3], e)


# ------------------------------------------------------------ set 2: converse and classifying
def one_conv(r):
    trip = r.choice([(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (6, 8, 10), (9, 12, 15), (20, 21, 29), (9, 40, 41)])
    kind = r.choice(["right", "acute", "obtuse", "obtuse"])
    a, b, c_ = trip
    if kind == "acute":
        c_ -= r.randint(1, 2)
    elif kind == "obtuse":
        c_ += r.randint(1, 3)
        if c_ >= a + b:
            return None
    if c_ <= b:
        return None
    s = a * a + b * b
    q = "A triangle has side lengths %d, %d and %d. Is it acute, right, or obtuse?" % (a, b, c_)
    cmp = "=" if c_ * c_ == s else ("&lt;" if c_ * c_ < s else "&gt;")
    right = {"=": "Right", "&lt;": "Acute", "&gt;": "Obtuse"}[cmp]
    e = "Compare the longest side squared with the sum of the other two squared: %d² = %d and %d² + %d² = %d. %d %s %d, so the triangle is <b>%s</b>." % (
        c_, c_ * c_, a, b, s, c_ * c_, cmp, s, right.lower())
    return T(q, right, [x for x in ["Acute", "Right", "Obtuse", "It is not a triangle"] if x != right], e)


# ------------------------------------------------------------ set 3: 45-45-90
def one_45(r):
    k = r.randint(2, 15)
    kind = r.choice(["hyp", "hyp", "leg", "leg_rad", "diag"])
    if kind == "hyp":
        q = "In a 45°-45°-90° triangle, each leg is %d. Find the hypotenuse.%s" % (k, fig(rt_fig(num(k), num(k), "<i>x</i>", ("Q", "45°"), w=150, h=150)))
        right = crad(k, 2)
        return T(q, right, [num(2 * k), crad(k, 3), num(k)], "The hypotenuse is leg × √2: <b>%s</b>." % right)
    if kind == "leg":
        q = "In a 45°-45°-90° triangle, the hypotenuse is %s. Find each leg." % crad(k, 2)
        return T(q, num(k), [crad(2 * k, 2), num(2 * k), crad(k, 3)], "Leg = hypotenuse ÷ √2 = %s ÷ √2 = <b>%d</b>." % (crad(k, 2), k))
    if kind == "leg_rad":
        h = 2 * k
        q = "In a 45°-45°-90° triangle, the hypotenuse is %d. Find each leg in simplest radical form.%s" % (h, fig(rt_fig("<i>x</i>", "", num(h), ("Q", "45°"), w=150, h=150)))
        right = crad(k, 2)
        return T(q, right, [num(k), crad(h, 2), crad(k, 3)],
                 "Leg = %d ÷ √2 = %d√2 ÷ 2 = <b>%s</b> (multiply the top and bottom by √2)." % (h, h, right))
    s = r.randint(3, 20)
    q = "A square has sides of %d in. How long is its diagonal?" % s
    right = crad(s, 2) + " in."
    return T(q, right, [num(2 * s) + " in.", crad(s, 3) + " in.", num(s * s) + " in."],
             "The diagonal splits the square into two 45°-45°-90° triangles. Diagonal = side × √2 = <b>%s</b>." % right)


# ------------------------------------------------------------ set 4: 30-60-90
def one_30(r):
    s = r.randint(2, 14)
    kind = r.choice(["from_short", "from_short", "from_hyp", "from_long", "from_long_rad", "equi"])
    if kind == "from_short":
        want = r.choice(["hypotenuse", "longer leg"])
        q = "In a 30°-60°-90° triangle, the shorter leg is %d. Find the %s.%s" % (s, want, fig(rt_fig(num(s), "", "", ("R", "60°"), w=210, h=121)))
        right = num(2 * s) if want == "hypotenuse" else crad(s, 3)
        wr = [crad(s, 3), crad(s, 2), num(3 * s)] if want == "hypotenuse" else [num(2 * s), crad(s, 2), crad(2 * s, 3)]
        e = "Short leg : long leg : hypotenuse = 1 : √3 : 2. The %s is %s." % (want, "2 × %d = <b>%s</b>" % (s, right) if want == "hypotenuse" else "%d√3 = <b>%s</b>" % (s, right))
        return T(q, right, wr, e)
    if kind == "from_hyp":
        h = 2 * s
        q = "In a 30°-60°-90° triangle, the hypotenuse is %d. Find the shorter leg and the longer leg." % h
        right = "%d and %s" % (s, crad(s, 3))
        return T(q, right, ["%s and %d" % (crad(s, 3), s), "%d and %s" % (s, crad(s, 2)), "%d and %s" % (h // 2 + 1, crad(h, 3))],
                 "The shorter leg is half the hypotenuse: %d. The longer leg is the shorter leg × √3: %s. <b>%s</b>." % (s, crad(s, 3), right))
    if kind == "from_long":
        q = "In a 30°-60°-90° triangle, the longer leg is %s. Find the shorter leg." % crad(s, 3)
        return T(q, num(s), [num(2 * s), num(3 * s), crad(s, 3)], "Shorter leg = longer leg ÷ √3 = %s ÷ √3 = <b>%d</b>." % (crad(s, 3), s))
    if kind == "from_long_rad":
        L = 3 * s if r.random() < 0.5 else s
        if L % 3:
            return None
        q = "In a 30°-60°-90° triangle, the longer leg is %d. Find the shorter leg in simplest radical form." % L
        right = crad(L // 3, 3)
        return T(q, right, [num(L // 3), crad(L, 3), num(L * 2)], "Shorter leg = %d ÷ √3 = %d√3 ÷ 3 = <b>%s</b>." % (L, L, right))
    side = 2 * s
    q = "An equilateral triangle has sides of %d. Find its height." % side
    right = crad(s, 3)
    return T(q, right, [crad(side, 3), num(s), crad(s, 2)],
             "The height splits it into two 30°-60°-90° triangles with hypotenuse %d and shorter leg %d. Height = shorter leg × √3 = <b>%s</b>." % (side, s, right))


# ------------------------------------------------------------ set 5: word problems
def one_word(r):
    pp = People(r)
    nm, he, his = pp.next()
    kind = r.choice(["ladder", "tv", "walk", "ramp", "kite", "field"])
    a, b, c_ = r.choice([(3, 4, 5), (5, 12, 13), (8, 15, 17), (6, 8, 10), (9, 12, 15), (12, 16, 20), (7, 24, 25), (15, 20, 25), (10, 24, 26)])
    if kind == "ladder":
        q = "A %d ft ladder leans against a wall. Its foot is %d ft from the wall. How high up the wall does it reach?" % (c_, a)
        return T(q, "%d ft" % b, ["%d ft" % (c_ - a), "%d ft" % (c_ + a), rad(c_ * c_ + a * a) + " ft"],
                 "The ladder is the hypotenuse: <i>h</i>² = %d² %s %d² = %d, so <i>h</i> = <b>%d ft</b>." % (c_, MINUS, a, b * b, b))
    if kind == "tv":
        w, h, d = r.choice([(32, 18, None), (48, 36, 60), (40, 30, 50), (24, 18, 30), (16, 12, 20), (64, 48, 80)])
        if d is None:
            return None
        q = "A screen is %d in. wide and %d in. tall. What is the length of its diagonal?" % (w, h)
        return T(q, "%d in." % d, ["%d in." % (w + h), "%s in." % num(d * d), "%d in." % (w - h)], "<i>d</i>² = %d² + %d² = %s, so <i>d</i> = <b>%d in.</b>" % (w, h, num(d * d), d))
    if kind == "walk":
        q = "%s walks %d blocks east and then %d blocks north. How far is %s from the start in a straight line?" % (nm, a, b, he)
        return T(q, "%d blocks" % c_, ["%d blocks" % (a + b), "%d blocks" % (b - a), "%d blocks" % (c_ * c_)],
                 "The two walks are the legs of a right triangle: √(%d² + %d²) = √%d = <b>%d blocks</b>." % (a, b, c_ * c_, c_))
    if kind == "ramp":
        h = r.choice([2, 3, 4])
        L = 2 * h
        q = "A ramp makes a 30° angle with the ground and rises %d ft. How long is the ramp?" % h
        return T(q, "%d ft" % L, ["%s ft" % crad(h, 3), "%s ft" % crad(h, 2), "%d ft" % (3 * h)],
                 "The ramp is the hypotenuse of a 30°-60°-90° triangle. The rise is opposite the 30° angle, so it is the shorter leg. Ramp = 2 × %d = <b>%d ft</b>." % (h, L))
    if kind == "kite":
        q = "A kite string is %d m long, and the kite is directly above a point %d m away from %s along the ground. How high is the kite?" % (c_, b, nm)
        return T(q, "%d m" % a, ["%d m" % (c_ - b), "%d m" % (c_ + b), "%s m" % rad(c_ * c_ + b * b)],
                 "The string is the hypotenuse: <i>h</i> = √(%d² %s %d²) = √%d = <b>%d m</b>." % (c_, MINUS, b, a * a, a))
    s = r.choice([30, 40, 60, 90, 100])
    q = "A square field has sides of %d yd. About how far is it from one corner to the opposite corner? (Use √2 ≈ 1.41.)" % s
    ans = round(s * 1.41, 1)
    return T(q, "%s yd" % ("{:,.1f}".format(ans).rstrip("0").rstrip(".")),
             ["%d yd" % (2 * s), "%s yd" % ("{:,.1f}".format(s * 1.73).rstrip("0").rstrip(".")), "%d yd" % (s * s)],
             "The diagonal of a square is side × √2 ≈ %d × 1.41 = <b>%s yd</b>." % (s, "{:,.1f}".format(ans).rstrip("0").rstrip(".")))


def build():
    sets = [S("Find a missing side", collect(one_side, 20, R)),
            S("Acute, right or obtuse?", collect(one_conv, 20, R)),
            S("45°-45°-90° triangles", collect(one_45, 20, R)),
            S("30°-60°-90° triangles", collect(one_30, 20, R)),
            S("Word problems", collect(one_word, 20, R))]
    body = lesson(
        "<p><b>Pythagorean Theorem</b>: in a right triangle, <i>a</i>² + <i>b</i>² = <i>c</i>², where <i>c</i> is the hypotenuse. "
        "To find a leg, subtract: <i>a</i>² = <i>c</i>² %s <i>b</i>². Leave answers in simplest radical form: √50 = 5√2.</p>"
        "<p><b>Converse</b>: compare <i>c</i>² with <i>a</i>² + <i>b</i>² (<i>c</i> is the longest side). Equal: right. Smaller: acute. Larger: obtuse.</p>"
        "<ul><li><b>45°-45°-90°</b>: legs <i>x</i>, <i>x</i>; hypotenuse <i>x</i>√2.</li>"
        "<li><b>30°-60°-90°</b>: shorter leg <i>x</i> (opposite 30°), longer leg <i>x</i>√3, hypotenuse 2<i>x</i>.</li></ul>" % MINUS,
        [("The legs of a right triangle are 4 and 6. Find the hypotenuse.", ["16 + 36 = 52", "√52 = √(4 × 13)"], "2√13"),
         ("In a 30°-60°-90° triangle, the hypotenuse is 18. Find the longer leg.", ["Shorter leg = 9", "Longer leg = 9√3"], "9√3")],
        ["Adding the legs: 3 + 4 is not 5... the hypotenuse is √(9 + 16) = 5, not 7.",
         "Adding the squares when finding a leg. Subtract from the hypotenuse squared.",
         "Leaving √48 unsimplified. Take out the largest perfect square: 4√3.",
         "Mixing up the legs of a 30°-60°-90° triangle. The shorter leg is opposite 30°."])
    faq = [("What is the Pythagorean theorem?", "In a right triangle, the squares of the two legs add up to the square of the hypotenuse: a² + b² = c²."),
           ("How do you tell if a triangle is acute, right or obtuse from its sides?", "Square the longest side and compare it with the sum of the squares of the other two. Equal means right, less means acute, more means obtuse."),
           ("What are the side ratios of a 45-45-90 triangle?", "1 : 1 : √2. The hypotenuse is a leg times √2."),
           ("What are the side ratios of a 30-60-90 triangle?", "1 : √3 : 2. The hypotenuse is twice the shorter leg, and the longer leg is the shorter leg times √3.")]
    body = body.replace("Adding the legs: 3 + 4 is not 5... the hypotenuse is √(9 + 16) = 5, not 7.", "Adding the legs. With legs 3 and 4, the hypotenuse is √(9 + 16) = 5, not 7.")
    make("pythagorean-theorem-and-special-right-triangles", 15, "G-SRT.B.4",
         "Pythagorean Theorem and Special Right Triangles",
         "Pythagorean Theorem and Special Right Triangles Worksheet (Geometry) | 100 Questions",
         "Pythagorean Theorem and Special Right Triangles",
         "Prove theorems about triangles. Theorems include: a line parallel to one side of a triangle divides the other two proportionally, and conversely; the Pythagorean Theorem proved using triangle similarity.",
         "Free Geometry worksheet on the Pythagorean theorem and special right triangles: radical answers, the converse, 45-45-90 and 30-60-90 triangles, and word problems. 100 questions.",
         "a² + b² = c². 45-45-90: x, x, x√2. 30-60-90: x, x√3, 2x.",
         "Compare c² with a² + b² to tell right, acute or obtuse.",
         body, faq, sets, R, domain="Right Triangles and Trigonometry", grade="geometry")


if __name__ == "__main__":
    build()
