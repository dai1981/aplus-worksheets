# -*- coding: utf-8 -*-
"""
US Precalculus: Complex Numbers in Polar Form (Common Core N-CN.B.4, N-CN.B.5, N-CN.B.6, N-CN.A.3)
  python3 tools/gen_us_math_pc_complex_numbers_in_polar_form.py
Modulus and argument, converting between rectangular form a + bi and polar form r(cos θ + i sin θ),
multiplying, dividing and raising to powers in polar form (De Moivre's theorem), and distance and
midpoint in the complex plane.
Wrong answers come from real mistakes: adding the moduli when multiplying, multiplying the angles,
taking tan⁻¹(b/a) without checking the quadrant, and forgetting the square root in the modulus.
"""
import math
import random
from fractions import Fraction as F
from us_hs import B, S, make, lesson, collect, T, num, MINUS, fr
from a2_common import sf
from pc_common import GRADE, trig, rt

R = random.Random(97701)
I = "<i>i</i>"
SPEC = sorted(set(list(range(0, 360, 30)) + [45, 135, 225, 315]))


def part(c, n):
    """c·√n as html (n in 1, 2, 3)"""
    if c == 0:
        return "0"
    s = MINUS if c < 0 else ""
    c = abs(c)
    if n == 1:
        return s + str(c)
    return s + ("" if c == 1 else str(c)) + "√%d" % n


def cx(re, im):
    """re, im: (c, n). a + bi as html"""
    rc, rn = re
    ic, in_ = im
    if ic == 0:
        return part(rc, rn)
    if in_ == 1:
        imag = ("" if abs(ic) == 1 else str(abs(ic))) + I
    else:
        imag = ("" if abs(ic) == 1 else str(abs(ic))) + I + "√%d" % in_
    if rc == 0:
        return (MINUS if ic < 0 else "") + imag
    return "%s %s %s" % (part(rc, rn), "+" if ic > 0 else MINUS, imag)


def comp(r, d, fn):
    """r·fn(d) as (c, n) for even r"""
    sk = trig(fn, d)
    sg, k = sk
    if k == "0":
        return (0, 1)
    if k == "1":
        return (sg * r, 1)
    half = r // 2
    return (sg * half, {"1/2": 1, "r2/2": 2, "r3/2": 3}[k])


def rect(r, d):
    return cx(comp(r, d, "cos"), comp(r, d, "sin"))


def pol(r, d):
    rr = r if isinstance(r, str) else num(r)
    return "%s(cos %d° + %s sin %d°)" % (rr, d, I, d)


# ------------------------------------------------------------ set 1: modulus and argument
TRI = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (6, 8, 10), (7, 24, 25)]


def one_mod(r):
    if r.random() < 0.55:
        a, b, c = r.choice(TRI)
        if r.random() < 0.5:
            a, b = b, a
        a *= r.choice([1, -1])
        b *= r.choice([1, -1])
        q = "Find the modulus |<i>z</i>| of <i>z</i> = %s." % cx((a, 1), (b, 1))
        return T(q, str(c), [str(abs(a) + abs(b)), str(c * c), str(abs(a - b)) if abs(a - b) not in (c,) else str(c + 1)],
                 "|<i>z</i>| = √(<i>a</i>² + <i>b</i>²) = √(%d + %d) = √%d = <b>%d</b>." % (a * a, b * b, c * c, c))
    rr = r.choice([2, 4, 6, 8])
    d = r.choice([d for d in SPEC if d % 90])
    z = rect(rr, d)
    q = "Find the argument θ of <i>z</i> = %s, with 0° ≤ θ &lt; 360°." % z
    ref = [d, 180 - d, d - 180, 360 - d][(d // 90)]
    wr = ["%d°" % ref, "%d°" % ((d + 180) % 360), "%d°" % (90 - ref if 90 - ref != ref else 360 - d)]
    return T(q, "%d°" % d, wr, "tan⁻¹ gives the reference angle %d°. The point is in Quadrant %s, so θ = <b>%d°</b>." % (ref, ["I", "II", "III", "IV"][d // 90], d))


# ------------------------------------------------------------ set 2: rectangular to polar
def one_topol(r):
    rr = r.choice([2, 4, 6, 8])
    d = r.choice(SPEC)
    z = rect(rr, d)
    q = "Write <i>z</i> = %s in polar form." % z
    ref = [d, 180 - d, d - 180, 360 - d][(d // 90)] if d % 90 else d
    wr = [pol(rr, ref) if ref != d else pol(rr, (d + 180) % 360), pol(rr * rr, d), pol(rr, (d + 90) % 360) if d % 90 else pol(rr * 2, d)]
    return T(q, pol(rr, d), wr, "<i>r</i> = |<i>z</i>| = %d and θ = %d° (check the quadrant). <b>%s</b>." % (rr, d, pol(rr, d)))


# ------------------------------------------------------------ set 3: polar to rectangular
def one_torect(r):
    rr = r.choice([2, 4, 6, 8, 10])
    d = r.choice([d for d in SPEC])
    right = rect(rr, d)
    co, si = comp(rr, d, "cos"), comp(rr, d, "sin")
    wr = [cx(si, co), cx((-co[0], co[1]), si), cx(co, (-si[0], si[1]))]
    if right in wr:
        wr = [w for w in wr if w != right] + [cx((co[0] * 2, co[1]), (si[0] * 2, si[1]))]
    q = "Write %s in rectangular form <i>a</i> + <i>b</i>%s." % (pol(rr, d), I)
    return T(q, right, wr, "<i>a</i> = %d cos %d° and <i>b</i> = %d sin %d°. <b>%s</b>." % (rr, d, rr, d, right))


# ------------------------------------------------------------ set 4: multiply, divide, powers
def one_ops(r):
    kind = r.choice(["mul", "mul", "div", "div", "pow", "pow"])
    if kind == "mul":
        r1, r2 = r.choice([2, 3, 4, 5]), r.choice([2, 3, 6])
        d1, d2 = r.choice([20, 40, 50, 70, 110, 130]), r.choice([10, 25, 35, 65, 80, 100])
        q = "Find <i>z</i><sub>1</sub><i>z</i><sub>2</sub> if <i>z</i><sub>1</sub> = %s and <i>z</i><sub>2</sub> = %s." % (pol(r1, d1), pol(r2, d2))
        right = pol(r1 * r2, (d1 + d2) % 360)
        wr = [pol(r1 + r2, (d1 + d2) % 360), pol(r1 * r2, (d1 * d2) % 360), pol(r1 * r2, abs(d1 - d2))]
        return T(q, right, wr, "Multiply the moduli and add the angles: %d × %d = %d and %d° + %d° = %d°. <b>%s</b>." % (r1, r2, r1 * r2, d1, d2, (d1 + d2) % 360, right))
    if kind == "div":
        r2 = r.choice([2, 3, 4])
        r1 = r2 * r.choice([2, 3, 5])
        d1, d2 = r.choice([150, 200, 240, 300, 120]), r.choice([30, 45, 60, 90, 20])
        q = "Find <i>z</i><sub>1</sub> ÷ <i>z</i><sub>2</sub> if <i>z</i><sub>1</sub> = %s and <i>z</i><sub>2</sub> = %s." % (pol(r1, d1), pol(r2, d2))
        right = pol(r1 // r2, d1 - d2)
        wr = [pol(r1 - r2, d1 - d2), pol(r1 // r2, (d1 + d2) % 360), pol(r1 * r2, d1 - d2)]
        return T(q, right, wr, "Divide the moduli and subtract the angles: %d ÷ %d = %d and %d° − %d° = %d°. <b>%s</b>." % (r1, r2, r1 // r2, d1, d2, d1 - d2, right))
    rr = r.choice([2, 3, "√2", 2])
    d = r.choice([30, 45, 60, 20, 40, 90, 120])
    n = r.choice([2, 3, 4, 5, 6])
    rv = {"√2": math.sqrt(2)}.get(rr, rr)
    rn = round(rv ** n)
    if abs(rv ** n - rn) > 1e-9:
        rn_h = "%d√2" % round(rv ** n / math.sqrt(2))
    else:
        rn_h = num(rn)
    if rn > 1000:
        return None
    ang = (d * n) % 360
    q = "Use De Moivre's theorem to find [%s]<sup>%d</sup>." % (pol(rr, d), n)
    right = pol(rn_h, ang)
    wr = [pol(rn_h, d), pol("%s" % (num(rv * n) if rr != "√2" else "%d√2" % n), ang), pol(rn_h, (d + n) % 360)]
    return T(q, right, wr, "Raise the modulus to the power and multiply the angle: (%s)<sup>%d</sup> = %s and %d × %d° = %d°%s. <b>%s</b>." % (
        rr, n, rn_h, n, d, d * n, "" if d * n < 360 else ", which is the same as %d°" % ang, right))


# ------------------------------------------------------------ set 5: the complex plane
def one_plane(r):
    kind = r.choice(["dist", "dist", "mid", "mid", "quad", "conj"])
    if kind == "dist":
        a, b, c = r.choice(TRI)
        x1, y1 = r.randint(-5, 5), r.randint(-5, 5)
        x2, y2 = x1 + a * r.choice([1, -1]), y1 + b * r.choice([1, -1])
        q = "Find the distance between <i>z</i> = %s and <i>w</i> = %s in the complex plane." % (cx((x1, 1), (y1, 1)), cx((x2, 1), (y2, 1)))
        return T(q, str(c), [str(a + b), str(c * c), rt(x2 * x2 + y2 * y2 + x1 * x1 + y1 * y1) if x2 * x2 + y2 * y2 + x1 * x1 + y1 * y1 != c * c else str(c + 2)],
                 "The distance is |<i>z</i> − <i>w</i>| = √((%s)² + (%s)²) = √%d = <b>%d</b>." % (sf(x1 - x2), sf(y1 - y2), c * c, c))
    if kind == "mid":
        x1, y1, x2, y2 = [r.randint(-8, 8) for _ in range(4)]
        if (x1 + x2) % 2 or (y1 + y2) % 2 or (x1, y1) == (x2, y2):
            return None
        mx, my = (x1 + x2) // 2, (y1 + y2) // 2
        q = "Find the midpoint of the segment joining %s and %s in the complex plane." % (cx((x1, 1), (y1, 1)), cx((x2, 1), (y2, 1)))
        right = cx((mx, 1), (my, 1))
        wr = [cx((x1 + x2, 1), (y1 + y2, 1)), cx(((x2 - x1) // 2 if (x2 - x1) % 2 == 0 else x2 - x1, 1), ((y2 - y1) // 2 if (y2 - y1) % 2 == 0 else y2 - y1, 1)), cx((my, 1), (mx, 1)) if mx != my else cx((mx + 1, 1), (my, 1))]
        return T(q, right, wr, "Average the parts: ((%s) + (%s))/2 = <b>%s</b>." % (cx((x1, 1), (y1, 1)), cx((x2, 1), (y2, 1)), right))
    if kind == "quad":
        a, b = r.choice([1, -1]) * r.randint(1, 7), r.choice([1, -1]) * r.randint(1, 7)
        qd = 1 if a > 0 and b > 0 else 2 if a < 0 < b else 3 if a < 0 and b < 0 else 4
        q = "The complex number %s is plotted with the real part on the horizontal axis. In which quadrant is it?" % cx((a, 1), (b, 1))
        names = ["Quadrant I", "Quadrant II", "Quadrant III", "Quadrant IV"]
        right = names[qd - 1]
        return T(q, right, [n for n in names if n != right], "Real part %s, imaginary part %s: <b>%s</b>." % (sf(a), sf(b), right))
    rr = r.choice([2, 3, 4, 5, 6])
    d = r.choice([20, 35, 50, 70, 110, 140])
    q = "If <i>z</i> = %s, what is its conjugate <span class='ov'><i>z</i></span> in polar form?" % pol(rr, d)
    right = pol(rr, 360 - d)
    return T(q, right, [pol(rr, 180 - d), pol(rr, d + 180), pol(rr, (90 - d) % 360)], "The conjugate reflects <i>z</i> over the real axis, so the angle becomes −%d°, which is %d°. <b>%s</b>." % (d, 360 - d, right))


def build():
    sets = [S("Modulus and argument", collect(one_mod, 20, R)),
            S("Rectangular to polar form", collect(one_topol, 20, R)),
            S("Polar to rectangular form", collect(one_torect, 20, R)),
            S("Multiplying, dividing and powers", collect(one_ops, 20, R)),
            S("The complex plane", collect(one_plane, 20, R))]
    body = lesson(
        "<ul><li>Plot <i>a</i> + <i>bi</i> at (<i>a</i>, <i>b</i>). Its <b>modulus</b> is |<i>z</i>| = √(<i>a</i>² + <i>b</i>²), the distance from 0.</li>"
        "<li>Its <b>argument</b> θ is the angle from the positive real axis. Find the reference angle with tan⁻¹|<i>b</i>/<i>a</i>| and then use the quadrant.</li>"
        "<li><b>Polar form</b>: <i>z</i> = <i>r</i>(cos θ + <i>i</i> sin θ). Back to rectangular: <i>a</i> = <i>r</i> cos θ, <i>b</i> = <i>r</i> sin θ.</li>"
        "<li>To multiply, multiply the moduli and add the angles. To divide, divide and subtract. <b>De Moivre</b>: [<i>r</i>(cos θ + <i>i</i> sin θ)]<sup><i>n</i></sup> = <i>r</i><sup><i>n</i></sup>(cos <i>n</i>θ + <i>i</i> sin <i>n</i>θ).</li></ul>",
        [("Write −2 + 2√3" + I + " in polar form.", ["<i>r</i> = √(4 + 12) = 4", "Reference angle 60°; Quadrant II, so θ = 120°"], pol(4, 120)),
         ("Find [2(cos 30° + " + I + " sin 30°)]<sup>4</sup>.", ["2<sup>4</sup> = 16", "4 × 30° = 120°"], pol(16, 120))],
        ["Adding the moduli when multiplying. Multiply them.",
         "Multiplying the angles when multiplying numbers. Add them.",
         "Using tan⁻¹(<i>b</i>/<i>a</i>) directly in Quadrants II and III. Check where the point is.",
         "Forgetting the square root: |3 + 4" + I + "| is 5, not 25."])
    faq = [("What is the polar form of a complex number?", "z = r(cos θ + i sin θ), where r is the distance from 0 (the modulus) and θ is the angle from the positive real axis (the argument)."),
           ("How do you multiply complex numbers in polar form?", "Multiply the moduli and add the arguments. To divide, divide the moduli and subtract the arguments."),
           ("What is De Moivre's theorem?", "[r(cos θ + i sin θ)]ⁿ = rⁿ(cos nθ + i sin nθ): raise the modulus to the power and multiply the angle by n."),
           ("How do you find the distance between two complex numbers?", "Subtract them and take the modulus: |z − w|. It is the same as the distance formula for the points.")]
    make("complex-numbers-in-polar-form", 7, "N-CN.B.4",
         "Complex Numbers in Polar Form",
         "Complex Numbers in Polar Form Worksheet: Modulus, Argument, De Moivre | 100 Questions",
         "Polar Form of Complex Numbers",
         "Represent complex numbers on the complex plane in rectangular and polar form (including real and imaginary numbers), and explain why the rectangular and polar forms of a given complex number represent the same number.",
         "Free precalculus worksheet on complex numbers in polar form: modulus and argument, converting forms, multiplying, dividing, De Moivre's theorem and the complex plane. 100 questions.",
         "z = r(cos θ + i sin θ)",
         "Multiply: multiply the moduli and add the angles. Powers: rⁿ and nθ.",
         body, faq, sets, R, domain="Complex Numbers and Polar Coordinates", grade=GRADE)


if __name__ == "__main__":
    build()
