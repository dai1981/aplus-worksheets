# -*- coding: utf-8 -*-
"""
Texas Precalculus: Arc Length, Linear Velocity and Angular Velocity (TEKS P.4D)
  python3 tools/gen_ustx_math_pc_angular_velocity.py
Arc length s = rθ, angular velocity in radians per unit of time, linear velocity v = rω, car and bike wheels, and
how many turns a wheel makes (own makers).
Wrong answers come from real mistakes: using degrees in s = rθ, forgetting the 2π in each revolution, and using the
diameter as the radius.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)

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


import math


def n1(v):
    s = "%.1f" % v
    i, _, f_ = s.partition(".")
    return comma(int(i)) + "." + f_


def one_arc(r):
    rad = r.choice([3, 4, 5, 6, 8, 10, 12, 15, 20])
    kind = r.choice(["rad", "deg", "theta"])
    if kind == "rad":
        th = Fr(r.choice([1, 2, 3, 5]), r.choice([2, 3, 4, 6]))
        q = "A circle has radius %d cm. Find the length of the arc cut off by a central angle of %s radians." % (rad, ft(th) if th.denominator == 1 else "<span class='fr'><span class='fn'>%dπ</span><span class='fd'>%d</span></span>" % (th.numerator, th.denominator) if th.numerator > 1 else "<span class='fr'><span class='fn'>π</span><span class='fd'>%d</span></span>" % th.denominator)
        v = rad * th
        right = ("%sπ cm" % ft(v)) if v != 1 else "π cm"
        w = ["%sπ cm" % ft(v * 2), "%sπ cm" % ft(Fr(th.numerator, th.denominator)), "%sπ cm" % ft(v / 2)]
        e = "<i>s</i> = <i>r</i>θ = %d × %s = %s." % (rad, "%sπ" % ft(th), right)
    elif kind == "deg":
        d = r.choice([30, 45, 60, 72, 90, 120, 135, 150, 210, 240])
        th = Fr(d, 180)
        v = rad * th
        q = "A circle has radius %d inches. Find the length of the arc cut off by a %d° angle, in terms of π." % (rad, d)
        right = "%sπ inches" % (ft(v) if v != 1 else "")
        w = ["%s inches" % comma(rad * d), "%sπ inches" % ft(v * 2), "%sπ inches" % ft(Fr(d, rad))]
        e = "Change to radians first: %d° = %sπ. <i>s</i> = %d × %sπ = %s." % (d, ft(th), rad, ft(th), right)
    else:
        s = rad * r.choice([1, 2, 3])
        th = Fr(s, rad)
        q = "An arc of length %d m is on a circle of radius %d m. What is the central angle in radians?" % (s, rad)
        right = "%s radians" % ft(th) if th != 1 else "1 radian"
        w = ["%s radians" % ft(Fr(rad, s)) if Fr(rad, s) != 1 else "%d radians" % s, "%d°" % (s * rad if s * rad < 360 else s), "%s radians" % ft(th * 2)]
        e = "θ = <i>s</i> ÷ <i>r</i> = %d ÷ %d = %s." % (s, rad, ft(th))
    return mcq(q, right, w, e + " <b>%s</b>." % right)


def one_ang(r):
    rpm = r.choice([10, 15, 20, 30, 45, 60, 90, 120, 150, 300])
    thing = r.choice(["A fan", "A wheel", "A record", "A pottery wheel", "A ceiling fan"])
    kind = r.choice(["min", "sec"])
    if kind == "min":
        q = "%s turns at %d revolutions per minute. What is its angular velocity in radians per minute?" % (thing, rpm)
        right = "%sπ radians per minute" % comma(2 * rpm)
        w = ["%sπ radians per minute" % comma(rpm), "%s radians per minute" % comma(360 * rpm), "%sπ radians per minute" % ft(Fr(rpm, 2))]
        e = "Each revolution is 2π radians: %d × 2π = %sπ." % (rpm, comma(2 * rpm))
    else:
        w_ = Fr(2 * rpm, 60)
        q = "%s turns at %d revolutions per minute. What is its angular velocity in radians per second?" % (thing, rpm)
        right = "%sπ radians per second" % (ft(w_) if w_ != 1 else "")
        w = ["%sπ radians per second" % comma(2 * rpm), "%sπ radians per second" % ft(Fr(rpm, 60)), "%s radians per second" % ft(Fr(360 * rpm, 60))]
        e = "%d × 2π = %sπ radians per minute; divide by 60: %s." % (rpm, comma(2 * rpm), right)
    return mcq(q, right, w, e + " <b>%s</b>." % right)


def one_lin(r):
    rad = r.choice([2, 3, 4, 5, 6, 8, 10])
    omega = r.choice([2, 3, 4, 5, 6, 8, 10, 12])
    unit_ = r.choice(["feet", "meters"])
    use_d = r.random() < 0.4
    q = "A point is on the edge of a wheel with %s %d %s. The wheel turns at %d radians per second. How fast is the point moving?" % ("diameter" if use_d else "radius", rad * 2 if use_d else rad, unit_, omega)
    right = "%d %s per second" % (rad * omega, unit_)
    w = ["%d %s per second" % (2 * rad * omega, unit_) if use_d else "%d %s per second" % (2 * rad * omega, unit_), "%s %s per second" % (n1(2 * math.pi * rad * omega), unit_), "%s %s per second" % (ft(Fr(omega, rad)), unit_)]
    w = [v for v in dict.fromkeys(w) if v != right]
    if len(w) < 3:
        w.append("%d %s per second" % (rad + omega, unit_))
    return mcq(q, right, w, "<i>v</i> = <i>r</i>ω%s = %d × %d = %d. <b>%s</b>." % (" (the radius is half the diameter)" if use_d else "", rad, omega, rad * omega, right))


def one_wheel(r):
    d = r.choice([24, 26, 27, 28, 30])
    rpm = r.choice([150, 180, 200, 240, 300, 360, 400, 500, 600, 800])
    veh = r.choice(["A bike wheel", "A car tire", "A go-kart tire"])
    inches_per_min = math.pi * d * rpm
    mph = inches_per_min * 60 / 63360
    q = "%s has a diameter of %d inches and turns at %d revolutions per minute. How fast is the vehicle going, in miles per hour? (1 mile = 63,360 inches.) Round to the nearest tenth." % (veh, d, rpm)
    right = "%s mph" % n1(mph)
    w = ["%s mph" % n1(mph * 2), "%s mph" % n1(mph / math.pi), "%s mph" % n1(mph / 60)]
    return mcq(q, right, w, "Each turn covers the circumference π × %d inches. %d turns a minute: π(%d)(%d) ≈ %s inches per minute. × 60 ÷ 63,360 ≈ <b>%s</b>." % (d, rpm, d, rpm, comma(int(round(inches_per_min))), right))


def one_rev(r):
    rad = r.choice([10, 12, 14, 15, 18, 20])
    dist = r.choice([100, 200, 300, 500, 1000, 1500])
    q = "A wheel with a radius of %d inches rolls %s feet. About how many full revolutions does it make? (1 foot = 12 inches.)" % (rad, comma(dist))
    rev = dist * 12 / (2 * math.pi * rad)
    right = "About %s revolutions" % comma(int(round(rev)))
    w = ["About %s revolutions" % comma(int(round(rev * 2))), "About %s revolutions" % comma(int(round(dist * 12 / (math.pi * rad * rad)))), "About %s revolutions" % comma(int(round(dist / (2 * math.pi * rad))))]
    w = [v for v in dict.fromkeys(w) if v != right]
    return mcq(q, right, w, "One revolution covers 2π(%d) ≈ %s inches. %s feet = %s inches. %s ÷ %s ≈ %s. <b>%s</b>." % (
        rad, n1(2 * math.pi * rad), comma(dist), comma(dist * 12), comma(dist * 12), n1(2 * math.pi * rad), n1(rev), right))


def build():
    sets, R = build_sets([
        ("Arc length", [("collect", uniq(one_arc), 20)]),
        ("Angular velocity", [("collect", uniq(one_ang), 20)]),
        ("Linear velocity", [("collect", uniq(one_lin), 20)]),
        ("Wheels and speed", [("collect", uniq(one_wheel), 20)]),
        ("How many revolutions?", [("collect", uniq(one_rev), 20)]),
    ], 69812)
    finish(sets, R)
    body = lesson('<ul><li>Arc length: <i>s</i> = <i>r</i>θ, with θ in <b>radians</b>.</li><li>Angular velocity ω is the angle turned per unit of time. One revolution is 2π radians.</li><li>Linear velocity: <i>v</i> = <i>r</i>ω, the distance a point on the edge travels per unit of time.</li><li>A rolling wheel moves one circumference, 2π<i>r</i>, per revolution.</li></ul>',
        [example("Radius 3 ft, 20 revolutions per minute", ["ω = 20 × 2π = 40π rad/min", "<i>v</i> = 3 × 40π"], "120π ≈ 377 ft per minute")],
        [['Using degrees in <i>s</i> = <i>r</i>θ', 'Change to radians first.'], ['Forgetting 2π', 'Revolutions × 2π = radians.'], ['Using the diameter as <i>r</i>', 'Halve the diameter.']])
    faq = [('What does TEKS P.4D ask?', 'Represent angles in radians or degrees based on the concept of rotation in mathematical and real-world problems, including linear and angular velocity.'), ('Do all points on a wheel have the same angular velocity?', 'Yes, but points farther from the center have greater linear velocity.'), ('What unit is angular velocity in?', 'Radians (or revolutions or degrees) per unit of time.'), ('Why does radian measure make v = rω work?', 'An angle of 1 radian cuts off an arc of length r.')]
    make('linear-and-angular-velocity', 12, 'Number and Measure', 'P.4D',
         'P.4D represent angles in radians or degrees based on the concept of rotation in mathematical and real-world problems, including linear and angular velocity',
         'Arc Length, Linear Velocity and Angular Velocity', 'Linear and Angular Velocity',
         'Free Precalculus worksheets for Texas TEKS P.4D: arc length, angular velocity, linear velocity, wheel speed and revolutions. 100 questions with answers.',
         's = rθ and v = rω, with angles in radians.', 'One revolution is 2π radians.',
         body, faq, sets, seo_title='Precalculus Linear and Angular Velocity Worksheets (TEKS P.4D)')


if __name__ == "__main__":
    build()
