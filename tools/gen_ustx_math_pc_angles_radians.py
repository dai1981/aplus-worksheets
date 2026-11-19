# -*- coding: utf-8 -*-
"""
Texas Precalculus: Degrees, Radians and Reference Angles (TEKS P.4B, P.4C)
  python3 tools/gen_ustx_math_pc_angles_radians.py
Converting between degrees and radians, coterminal and reference angles in degrees and radians (US Algebra 2 and
Precalculus makers with a new seed), and angles in radians in standard position and angles of rotation (own makers).
Wrong answers come from real mistakes: multiplying by 180/π the wrong way, measuring a reference angle from the y-axis,
and forgetting that a full turn is 2π.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_a2_unit_circle_and_radians as uc
adopt(uc)
uc.R = random.Random(698110)
import gen_us_math_pc_six_trigonometric_functions as six
adopt(six)
six.R = random.Random(698111)
tx_common.GRADE = "precalculus"

import us_hs
adopt(us_hs)


def W(fn, keep=None):
    """Use an item maker of another generator: its odd failures count as a skipped try, and a question text
    is used only once (not again with other wrong answers)."""
    seen = set()

    def f(r):
        try:
            it = fn(r)
        except (TypeError, ValueError, ZeroDivisionError, IndexError, KeyError):
            raise AssertionError("skip")
        if not it or (keep and not keep(it)) or it["q"] in seen:
            raise AssertionError("skip")
        seen.add(it["q"])
        return it
    f.__name__ = fn.__name__
    return f


def PR(fn, keep=None):
    """A fixed word-problem list of another generator as a set maker: a shuffled share of it."""
    def f(r):
        its = [it for it in fn() if keep is None or keep(it)]
        r.shuffle(its)
        return {"title": fn.__name__, "items": its * 3}
    f.__name__ = fn.__name__
    return f


MINUS = "−"
X = "<i>x</i>"


def sg(v):
    return ("−%s" % abs(v)) if v < 0 else str(v)


def poly(cs, v="<i>x</i>"):
    """[a, b, c] highest power first, e.g. 2x² − 3x + 1."""
    deg = len(cs) - 1
    out = ""
    for i, c in enumerate(cs):
        if c == 0:
            continue
        p = deg - i
        mag = abs(c)
        if p == 0:
            body = str(mag)
        else:
            body = ("" if mag == 1 else str(mag)) + v + ("<sup>%d</sup>" % p if p > 1 else "")
        if not out:
            out = (MINUS if c < 0 else "") + body
        else:
            out += (" − " if c < 0 else " + ") + body
    return out or "0"
def uniq(fn):
    """Never give the same question twice, even with other wrong answers."""
    seen = set()
    def f(r):
        it = fn(r)
        if it["q"] in seen:
            raise AssertionError("repeat")
        seen.add(it["q"])
        return it
    f.__name__ = fn.__name__
    return f


from fractions import Fraction as Fr


def ft(v):
    v = Fr(v)
    if v.denominator == 1:
        return sg(int(v))
    return (MINUS if v < 0 else "") + fr(abs(v.numerator), v.denominator)


def fx(body, name="f"):
    return "<i>%s</i>(<i>x</i>) = %s" % (name, body)


def pin(n, d):
    """n·π/d as html"""
    f = Fr(n, d)
    if f == 0:
        return "0"
    s = MINUS if f < 0 else ""
    f = abs(f)
    if f.denominator == 1:
        return s + ("π" if f.numerator == 1 else "%dπ" % f.numerator)
    top = "π" if f.numerator == 1 else "%dπ" % f.numerator
    return s + "<span class='fr'><span class='fn'>%s</span><span class='fd'>%d</span></span>" % (top, f.denominator)


QD = ["Quadrant I", "Quadrant II", "Quadrant III", "Quadrant IV"]


def one_rad(r):
    d = r.choice([3, 4, 6])
    n = r.choice([k for k in range(-4 * d, 6 * d + 1) if Fr(k, d).denominator == d])
    deg = Fr(n, d) * 180
    kind = r.choice(["quad", "cot", "cot"])
    if kind == "quad":
        m = deg % 360
        right = QD[int(m // 90)]
        q = "In which quadrant does the terminal side of θ = %s lie?" % pin(n, d)
        w = [v for v in QD if v != right]
        e = "%s = %s°, which is the same as %s°: %s." % (pin(n, d), ft(deg), ft(m), right)
    else:
        k = r.choice([1, -1, 2])
        right = pin(n + 2 * d * k, d)
        w = [pin(n + d * k, d), pin(-n, d), pin(n + 2 * k, d) if Fr(n + 2 * k, d) != Fr(n + 2 * d * k, d) else pin(n + 4 * d, d)]
        q = "Which angle is coterminal with %s?" % pin(n, d)
        e = "Add or subtract full turns of 2π: %s %s %s = %s." % (pin(n, d), "+" if k > 0 else "−", pin(2 * abs(k), 1), right)
    return mcq(q, right, w, e + " <b>%s</b>." % right)


def one_rot(r):
    kind = r.choice(["turns", "turns", "clock", "deg"])
    if kind == "turns":
        t = Fr(r.choice([1, 3, 5, 7, 9, 2, 4]), r.choice([2, 4, 1, 3]))
        if t.denominator == 1 and t.numerator in (1,):
            raise AssertionError
        thing = r.choice(["A wheel", "A fan blade", "A merry-go-round", "A drill bit"])
        q = "%s makes %s of a full rotation counterclockwise. Through how many radians does it turn?" % (thing, ft(t) + (" turns" if t > 1 else " turn"))
        q = "%s turns %s %s counterclockwise. Through how many radians does it turn?" % (thing, ft(t), "full rotations" if t > 1 else "of a full rotation")
        right = pin(2 * t.numerator, t.denominator)
        w = [pin(t.numerator, t.denominator), "%s°" % ft(360 * t), pin(4 * t.numerator, t.denominator)]
        e = "One full rotation is 2π radians: %s × 2π = %s." % (ft(t), right)
    elif kind == "clock":
        m = r.choice([5, 10, 15, 20, 25, 30, 40, 45, 50])
        right = pin(-m, 30)
        q = "The minute hand of a clock moves for %d minutes. Through what angle does it turn, in radians? (Clockwise turns are negative.)" % m
        w = [pin(m, 30), pin(-m, 60), "−%d°" % (6 * m)]
        e = "60 minutes is one full turn, −2π. %d minutes is %d/60 of that: −%s · 2π = %s." % (m, m, ft(Fr(m, 60)), right)
    else:
        a = r.choice([400, 450, 480, 510, 540, 600, 630, 720, 750, -30, -120, -210, -300])
        m = a % 360
        right = QD[int(m // 90)] if m % 90 else "On an axis"
        if m % 90 == 0:
            raise AssertionError
        q = "An angle of %s° is drawn in standard position. In which quadrant does its terminal side lie?" % sg(a)
        w = [v for v in QD if v != right]
        e = "Add or subtract 360° until it is between 0° and 360°: %d°. <b>%s</b>." % (m, right)
        return mcq(q, right, w, e)
    return mcq(q, right, w, e + " <b>%s</b>." % right)


def build():
    sets, R = build_sets([
        ("Convert degrees and radians", [("collect", W(uc.one_conv), 20)]),
        ("Coterminal and reference angles", [("collect", W(uc.one_ref), 20)]),
        ("Reference angles in radians", [("collect", W(six.one_ref), 20)]),
        ("Angles in radians in standard position", [("collect", uniq(one_rad), 20)]),
        ("Angles of rotation", [("collect", uniq(one_rot), 20)]),
    ], 69811)
    finish(sets, R)
    body = lesson("<ul><li>A full turn is 360° = 2π radians, so 180° = π radians.</li><li>Degrees to radians: multiply by <span class='fr'><span class='fn'>π</span><span class='fd'>180</span></span>. Radians to degrees: multiply by <span class='fr'><span class='fn'>180</span><span class='fd'>π</span></span>.</li><li>An angle in standard position starts on the positive <i>x</i>-axis. Counterclockwise is positive.</li><li>Coterminal angles differ by full turns. The reference angle is the acute angle to the <i>x</i>-axis.</li></ul>",
        [example("Convert 135°", ["135 × <span class='fr'><span class='fn'>π</span><span class='fd'>180</span></span>"], "<span class='fr'><span class='fn'>3π</span><span class='fd'>4</span></span>"), example("Reference angle of <span class='fr'><span class='fn'>7π</span><span class='fd'>6</span></span>", ["210°, Quadrant III", "210° − 180°"], "<span class='fr'><span class='fn'>π</span><span class='fd'>6</span></span>")],
        [['Using 180/π to get radians', 'Degrees to radians uses π/180.'], ['Measuring from the <i>y</i>-axis', 'Reference angles go to the <i>x</i>-axis.'], ['A full turn of π', 'A full turn is 2π.']])
    faq = [('What does TEKS P.4B ask?', 'Describe the relationship between degree and radian measure on the unit circle.'), ('What does TEKS P.4C ask?', 'Represent angles in radians or degrees based on the concept of rotation and find the measure of reference angles and angles in standard position.'), ('What is one radian?', 'The angle that cuts off an arc as long as the radius, about 57.3°.'), ('Why use radians?', 'They make arc length and many formulas simpler: s = rθ.')]
    make('degrees-radians-and-reference-angles', 11, 'Number and Measure', 'P.4B, P.4C',
         'P.4B describe the relationship between degree and radian measure on the unit circle; P.4C represent angles in radians or degrees based on the concept of rotation and find the measure of reference angles and angles in standard position',
         'Degrees, Radians and Reference Angles', 'Degrees and Radians',
         'Free Precalculus worksheets for Texas TEKS P.4B and P.4C: convert degrees and radians, coterminal and reference angles, standard position and angles of rotation. 100 questions with answers.',
         '180° = π radians.', 'Coterminal angles differ by full turns of 2π.',
         body, faq, sets, seo_title='Precalculus Degrees, Radians and Reference Angles Worksheets (TEKS P.4B, P.4C)')


if __name__ == "__main__":
    build()
