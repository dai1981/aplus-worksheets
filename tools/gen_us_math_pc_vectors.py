# -*- coding: utf-8 -*-
"""
US Precalculus: Vectors: Components, Magnitude and Direction (Common Core N-VM.A.1, N-VM.A.2, N-VM.A.3)
  python3 tools/gen_us_math_pc_vectors.py
Component form from initial and terminal points, magnitude, direction angle, component form from magnitude
and direction, and velocity, displacement and force problems.
Wrong answers come from real mistakes: subtracting terminal minus initial the wrong way, adding the
components instead of using the Pythagorean theorem, ignoring the quadrant of the direction angle, and
swapping sine and cosine for the components.
"""
import math
import random
from fractions import Fraction as F
from us_hs import B, S, make, lesson, collect, T, num, MINUS, fr, People
from a2_common import sf
from pc_common import GRADE, vec, rt, trig

R = random.Random(97801)
V = "<b><i>v</i></b>"
TRI = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (6, 8, 10), (7, 24, 25), (9, 12, 15)]


def deg1(d):
    return num(F(round(d, 1)).limit_denominator(10)) + "°"


def dir_angle(x, y):
    return math.degrees(math.atan2(y, x)) % 360


# ------------------------------------------------------------ set 1: component form
def one_comp(r):
    x1, y1 = r.randint(-6, 6), r.randint(-6, 6)
    x2, y2 = r.randint(-6, 6), r.randint(-6, 6)
    if (x1, y1) == (x2, y2) or x1 == x2 or y1 == y2:
        return None
    q = "Find the component form of the vector from <i>P</i>(%s, %s) to <i>Q</i>(%s, %s)." % (sf(x1), sf(y1), sf(x2), sf(y2))
    right = vec(x2 - x1, y2 - y1)
    return T(q, right, [vec(x1 - x2, y1 - y2), vec(x2 + x1, y2 + y1), vec(y2 - y1, x2 - x1)],
             "Terminal minus initial: ⟨%s − %s, %s − %s⟩ = <b>%s</b>." % (sf(x2), "(%s)" % sf(x1) if x1 < 0 else sf(x1), sf(y2), "(%s)" % sf(y1) if y1 < 0 else sf(y1), right))


# ------------------------------------------------------------ set 2: magnitude
def one_mag(r):
    if r.random() < 0.6:
        a, b, c = r.choice(TRI)
        if r.random() < 0.5:
            a, b = b, a
        x, y = a * r.choice([1, -1]), b * r.choice([1, -1])
        right = str(c)
        wr = [str(abs(x) + abs(y)), str(c * c), rt(abs(x * x - y * y)) if x * x != y * y else str(c + 1)]
    else:
        x, y = r.choice([1, -1]) * r.randint(1, 7), r.choice([1, -1]) * r.randint(1, 7)
        s = x * x + y * y
        if int(math.isqrt(s)) ** 2 == s:
            return None
        right = rt(s)
        wr = [str(abs(x) + abs(y)), str(s), rt(abs(x * x - y * y)) if x * x != y * y and rt(abs(x * x - y * y)) != right else "√%d" % (s + 2)]
    q = "Find the magnitude of %s = %s." % (V, vec(x, y))
    return T(q, right, wr, "‖%s‖ = √(%s² + %s²) = √%d = <b>%s</b>." % (V, "(%s)" % sf(x) if x < 0 else sf(x), "(%s)" % sf(y) if y < 0 else sf(y), x * x + y * y, right))


# ------------------------------------------------------------ set 3: direction angle
def one_dir(r):
    if r.random() < 0.45:
        rr = r.choice([2, 4, 6])
        d = r.choice([30, 45, 60, 120, 135, 150, 210, 225, 240, 300, 315, 330])
        ck, sk = trig("cos", d), trig("sin", d)
        def comp(k):
            s, key = k
            m = {"1/2": str(rr // 2), "r2/2": ("%d√2" % (rr // 2)) if rr // 2 > 1 else "√2", "r3/2": ("%d√3" % (rr // 2)) if rr // 2 > 1 else "√3"}[key]
            return (MINUS if s < 0 else "") + m
        q = "Find the direction angle of %s = %s, with 0° ≤ θ &lt; 360°." % (V, vec(comp(ck), comp(sk)))
        ref = [d, 180 - d, d - 180, 360 - d][d // 90]
        return T(q, "%d°" % d, ["%d°" % ref if ref != d else "%d°" % (d + 180), "%d°" % ((d + 180) % 360), "%d°" % (90 - ref if 90 - ref != ref else (360 - d) % 360)],
                 "tan⁻¹|<i>y</i>/<i>x</i>| gives the reference angle %d°. The vector points into Quadrant %s, so θ = <b>%d°</b>." % (ref, ["I", "II", "III", "IV"][d // 90], d))
    x, y = r.choice([1, -1]) * r.randint(1, 9), r.choice([1, -1]) * r.randint(1, 9)
    if abs(x) == abs(y):
        return None
    d = dir_angle(x, y)
    raw = math.degrees(math.atan(y / x))
    q = "Find the direction angle of %s = %s to the nearest tenth of a degree, with 0° ≤ θ &lt; 360°." % (V, vec(x, y))
    right = deg1(d)
    wr = [deg1(raw), deg1((d + 180) % 360), deg1(math.degrees(math.atan2(x, y)) % 360)]
    if right in wr:
        return None
    return T(q, right, wr, "tan⁻¹(%s/%s) ≈ %s, but %s points into Quadrant %s, so θ ≈ <b>%s</b>." % (
        sf(y), sf(x), deg1(raw), V, ["I", "II", "III", "IV"][int(d // 90)], right))


# ------------------------------------------------------------ set 4: components from magnitude and direction
def one_fromdir(r):
    rr = r.choice([4, 6, 8, 10, 12, 20])
    d = r.choice([30, 45, 60, 120, 135, 150, 210, 225, 240, 300, 315, 330, 90, 180, 270])
    ck, sk = trig("cos", d), trig("sin", d)

    def comp(k):
        s, key = k
        if key == "0":
            return "0"
        if key == "1":
            return (MINUS if s < 0 else "") + str(rr)
        h = rr // 2
        m = {"1/2": str(h), "r2/2": "%d√2" % h, "r3/2": "%d√3" % h}[key]
        return (MINUS if s < 0 else "") + m
    q = "A vector has magnitude %d and direction angle %d°. What is its component form?" % (rr, d)
    right = vec(comp(ck), comp(sk))
    wr = [vec(comp(sk), comp(ck)), vec(comp((-ck[0], ck[1])), comp(sk)), vec(comp(ck), comp((-sk[0], sk[1])))]
    if len(set(wr + [right])) < 4:
        wr.append(vec(str(rr), "0") if d else vec("0", str(rr)))
    return T(q, right, wr, "%s = ⟨%d cos %d°, %d sin %d°⟩ = <b>%s</b>." % (V, rr, d, rr, d, right))


# ------------------------------------------------------------ set 5: word problems
def one_word(r):
    pp = People(r)
    nm, he, his = pp.next()
    kind = r.choice(["walk", "walk", "force", "force", "plane", "boat"])
    if kind == "walk":
        a, b, c = r.choice(TRI)
        e_, n_ = r.choice([("east", "north"), ("west", "north"), ("east", "south")])
        want = r.choice(["dist", "dir"])
        if want == "dist":
            q = "%s walks %d km %s and then %d km %s. How far is %s from the starting point?" % (nm, a, e_, b, n_, he)
            return T(q, "%d km" % c, ["%d km" % (a + b), "%d km" % (c * c), "%d km" % abs(b - a) if abs(b - a) else "%d km" % (c + 1)],
                     "The displacement is ⟨%d, %d⟩ (ignoring signs), and its magnitude is √(%d + %d) = <b>%d km</b>." % (a, b, a * a, b * b, c))
        ang = math.degrees(math.atan(b / a))
        q = "%s walks %d km %s and then %d km %s. To the nearest degree, at what angle %s of %s is %s from the start?" % (nm, a, e_, b, n_, n_, e_, he)
        right = "%d°" % round(ang)
        return T(q, right, ["%d°" % round(90 - ang), "%d°" % round(math.degrees(math.atan(a / b)) + 4), "%d°" % round(math.degrees(math.asin(min(1, b / (a + b)))))],
                 "tan θ = %d/%d, so θ = tan⁻¹(%d/%d) ≈ <b>%s</b> %s of %s." % (b, a, b, a, right, n_, e_))
    if kind == "force":
        f = r.choice([20, 40, 50, 80, 100, 120])
        d = r.choice([20, 25, 30, 35, 40, 50, 60])
        want = r.choice(["horizontal", "vertical"])
        val = f * (math.cos(math.radians(d)) if want == "horizontal" else math.sin(math.radians(d)))
        oth = f * (math.sin(math.radians(d)) if want == "horizontal" else math.cos(math.radians(d)))
        q = "%s pulls a wagon with a force of %d N at an angle of %d° above the ground. To the nearest tenth, what is the %s component of the force?" % (nm, f, d, want)
        right = num(F(round(val, 1)).limit_denominator(10)) + " N"
        wr = [num(F(round(oth, 1)).limit_denominator(10)) + " N", "%d N" % f, num(F(round(f * d / 90, 1)).limit_denominator(10)) + " N"]
        if len(set(wr + [right])) < 4:
            return None
        return T(q, right, wr, "The %s component is %d %s %d° ≈ <b>%s</b>." % (want, f, "cos" if want == "horizontal" else "sin", d, right))
    if kind == "plane":
        sp = r.choice([200, 300, 400, 500])
        wind = r.choice([30, 40, 50, 60])
        q = "A plane flies due north at %d mph, and the wind blows due east at %d mph. To the nearest mph, what is the plane's ground speed?" % (sp, wind)
        g = math.hypot(sp, wind)
        right = "%s mph" % num(round(g))
        return T(q, right, ["%s mph" % num(sp + wind), "%s mph" % num(sp - wind), "%s mph" % num(sp)],
                 "The velocities are ⟨%d, %d⟩ together, so the speed is √(%d² + %d²) ≈ <b>%s</b>." % (wind, sp, wind, sp, right))
    sp = r.choice([6, 8, 10, 12])
    cur = r.choice([2, 3, 4, 5])
    q = "A boat heads straight across a river at %d mph, and the current flows downstream at %d mph. To the nearest degree, how far off the straight-across direction does the boat travel?" % (sp, cur)
    ang = math.degrees(math.atan(cur / sp))
    right = "%d°" % round(ang)
    return T(q, right, ["%d°" % round(90 - ang), "%d°" % round(math.degrees(math.asin(cur / sp))) if round(math.degrees(math.asin(cur / sp))) != round(ang) else "%d°" % (round(ang) + 3), "%d°" % round(cur / sp * 90)],
             "The current is opposite and the boat's speed is adjacent: θ = tan⁻¹(%d/%d) ≈ <b>%s</b>." % (cur, sp, right))


def build():
    sets = [S("Component form", collect(one_comp, 20, R)),
            S("Magnitude", collect(one_mag, 20, R)),
            S("Direction angle", collect(one_dir, 20, R)),
            S("Components from magnitude and direction", collect(one_fromdir, 20, R)),
            S("Word problems", collect(one_word, 20, R))]
    body = lesson(
        "<ul><li>A vector has <b>magnitude</b> (length) and <b>direction</b>. From <i>P</i>(<i>x</i><sub>1</sub>, <i>y</i><sub>1</sub>) to <i>Q</i>(<i>x</i><sub>2</sub>, <i>y</i><sub>2</sub>): "
        "<b><i>v</i></b> = ⟨<i>x</i><sub>2</sub> − <i>x</i><sub>1</sub>, <i>y</i><sub>2</sub> − <i>y</i><sub>1</sub>⟩ (terminal minus initial).</li>"
        "<li>Magnitude: ‖⟨<i>a</i>, <i>b</i>⟩‖ = √(<i>a</i>² + <i>b</i>²).</li>"
        "<li>Direction angle: the reference angle is tan⁻¹|<i>b</i>/<i>a</i>|; then choose the quadrant from the signs of <i>a</i> and <i>b</i>.</li>"
        "<li>From magnitude <i>r</i> and direction θ: <b><i>v</i></b> = ⟨<i>r</i> cos θ, <i>r</i> sin θ⟩.</li></ul>",
        [("Find the vector from <i>P</i>(2, −1) to <i>Q</i>(−4, 7) and its magnitude.", ["⟨−4 − 2, 7 − (−1)⟩ = ⟨−6, 8⟩", "√(36 + 64) = 10"], "⟨−6, 8⟩, magnitude 10"),
         ("Find the direction angle of ⟨−3, 3⟩.", ["Reference angle tan⁻¹(1) = 45°", "Quadrant II"], "135°")],
        ["Subtracting initial minus terminal. Always terminal minus initial.",
         "Adding the components to get the magnitude. Use the Pythagorean theorem.",
         "Using tan⁻¹(<i>b</i>/<i>a</i>) without checking the quadrant.",
         "Swapping cosine and sine: the <i>x</i>-component uses cos θ."])
    faq = [("How do you find the component form of a vector?", "Subtract the coordinates of the initial point from the coordinates of the terminal point: ⟨x₂ − x₁, y₂ − y₁⟩."),
           ("How do you find the magnitude of a vector?", "Use the Pythagorean theorem: the magnitude of ⟨a, b⟩ is √(a² + b²)."),
           ("How do you find the direction angle?", "Find the reference angle with tan⁻¹|b/a|, then adjust for the quadrant the vector points into."),
           ("How do you write a vector from its magnitude and direction?", "Multiply the magnitude by cos θ for the x-component and by sin θ for the y-component.")]
    make("vectors", 8, "N-VM.A.1",
         "Vectors: Components, Magnitude and Direction",
         "Vectors Worksheet: Component Form, Magnitude and Direction | 100 Questions with Answers",
         "Vectors",
         "Recognize vector quantities as having both magnitude and direction. Represent vector quantities by directed line segments, and use appropriate symbols for vectors and their magnitudes.",
         "Free precalculus worksheet on vectors: component form, magnitude, direction angle, components from magnitude and direction, and velocity and force problems. 100 questions.",
         "A vector = magnitude + direction. Component form is terminal minus initial.",
         "Magnitude √(a² + b²); components ⟨r cos θ, r sin θ⟩.",
         body, faq, sets, R, domain="Vectors and Matrices", grade=GRADE)


if __name__ == "__main__":
    build()
