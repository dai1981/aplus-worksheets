# -*- coding: utf-8 -*-
"""
Texas Precalculus: Bearings and Angles of Elevation (TEKS P.4E, P.4F)
  python3 tools/gen_ustx_math_pc_bearings.py
Compass and true bearings, standard-position angles from bearings, north and east components of a trip, two-leg
trips and back bearings, and angles of elevation and depression (own makers).
Wrong answers come from real mistakes: measuring a bearing from the x-axis, using sine for the north component, and
putting the angle of depression at the wrong corner.
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


def tb(b):
    return "%03d°" % (b % 360)


def compass(b):
    b %= 360
    if b < 90:
        return "N %d° E" % b
    if b < 180:
        return "S %d° E" % (180 - b)
    if b < 270:
        return "S %d° W" % (b - 180)
    return "N %d° W" % (360 - b)


def one_conv(r):
    b = r.choice([v for v in range(5, 356) if v % 90])
    kind = r.choice(["c2t", "t2c", "std"])
    if kind == "c2t":
        q = "Write the compass bearing %s as a true bearing (degrees clockwise from north)." % compass(b)
        right = tb(b)
        w = [tb(360 - b), tb(90 - b), tb(b + 180)]
        e = "Start at north and turn clockwise to %s: %s." % (compass(b), right)
    elif kind == "t2c":
        q = "Write the true bearing %s as a compass bearing." % tb(b)
        right = compass(b)
        w = [compass(360 - b), compass(b + 180), compass(90 - b if 90 - b > 0 else 450 - b)]
        e = "%s is in the %s quarter, so measure from %s: %s." % (tb(b), {0: "NE", 1: "SE", 2: "SW", 3: "NW"}[b // 90], "north" if b < 90 or b > 270 else "south", right)
    else:
        q = "A ship sails on a true bearing of %s. What angle does its path make in standard position (counterclockwise from east)?" % tb(b)
        th = (90 - b) % 360
        right = "%d°" % th
        w = ["%d°" % b, "%d°" % ((b + 90) % 360), "%d°" % ((360 - b) % 360)]
        e = "Standard position θ = 90° − bearing (add 360° if needed): 90° − %d° → %d°." % (b, th)
    w = [v for v in dict.fromkeys(w) if v != right]
    return mcq(q, right, w, e + " <b>%s</b>." % right)


def one_comp(r):
    d = r.choice([12, 15, 20, 25, 30, 40, 50, 60, 80, 120])
    b = r.choice([v for v in range(10, 351) if v % 90 and v % 5 == 0 and v % 45])
    th = math.radians(b)
    N, E = d * math.cos(th), d * math.sin(th)
    want = r.choice(["north", "east"])
    val = N if want == "north" else E
    dirw = ("north" if val > 0 else "south") if want == "north" else ("east" if val > 0 else "west")
    right = "%s miles %s" % (n1(abs(val)), dirw)
    oth = E if want == "north" else N
    w = ["%s miles %s" % (n1(abs(oth)), dirw), "%s miles %s" % (n1(abs(val)), {"north": "south", "south": "north", "east": "west", "west": "east"}[dirw]), "%s miles %s" % (n1(d * abs(math.tan(th)) if abs(math.tan(th)) < 20 else d / 2), dirw)]
    w = [v for v in dict.fromkeys(w) if v != right]
    return mcq("A boat travels %d miles on a bearing of %s. How far %s or %s of its start is it now? Round to the nearest tenth." % (d, tb(b), "north" if want == "north" else "east", "south" if want == "north" else "west"), right, w,
               "Bearings are measured from north, so north–south = <i>d</i> cos β and east–west = <i>d</i> sin β. %d %s %d° ≈ %s. <b>%s</b>." % (d, "cos" if want == "north" else "sin", b, n1(val).replace("-", MINUS), right))


def one_two(r):
    a = r.choice([3, 5, 6, 8, 9, 12, 15, 20])
    c = r.choice([4, 7, 8, 10, 12, 16, 21])
    if a == c:
        raise AssertionError
    d1, d2 = r.sample(["east", "west"], 1)[0], r.sample(["north", "south"], 1)[0]
    kind = r.choice(["dist", "bear"])
    dist = math.hypot(a, c)
    ang = math.degrees(math.atan2(a, c))
    if d2 == "north":
        b = ang if d1 == "east" else 360 - ang
    else:
        b = 180 - ang if d1 == "east" else 180 + ang
    q0 = "A hiker walks %d km %s and then %d km %s. " % (a, d1, c, d2)
    if kind == "dist":
        right = "%s km" % n1(dist)
        w = ["%d km" % (a + c), "%s km" % n1(abs(c - a)), "%s km" % n1(math.sqrt(a * a + c * c) / 2)]
        q = q0 + "How far is she from her start? Round to the nearest tenth."
        e = "The two legs are at right angles: √(%d<sup>2</sup> + %d<sup>2</sup>) ≈ %s." % (a, c, n1(dist))
    else:
        right = "%03d°" % int(round(b)) if round(b) < 360 else "000°"
        alt = [ang, 90 - ang, (b + 180) % 360]
        w = ["%03d°" % (int(round(v)) % 360) for v in alt]
        q = q0 + "What is her bearing from the start, to the nearest degree?"
        e = "tan<sup>−1</sup>(%d ÷ %d) ≈ %.0f° from the %s–%s line, so the true bearing is about %s." % (a, c, ang, d2, "south" if d2 == "south" else "north", right)
    w = [v for v in dict.fromkeys(w) if v != right]
    return mcq(q, right, w, e + " <b>%s</b>." % right)


def one_back(r):
    b = r.choice([v for v in range(5, 356) if v % 5 == 0 and v % 90])
    kind = r.choice(["back", "angle"])
    if kind == "back":
        q = "A plane flies from town A to town B on a bearing of %s. On what bearing must it fly to go straight back from B to A?" % tb(b)
        right = tb(b + 180)
        w = [tb(360 - b), tb(b + 90), tb(180 - b)]
        e = "The return trip is the opposite direction: add or subtract 180°."
    else:
        c = r.choice([v for v in range(5, 356) if v % 5 == 0 and abs(v - b) > 10 and abs(v - b) < 350])
        d = abs(c - b)
        if d > 180:
            d = 360 - d
        q = "From a lighthouse, ship P is on a bearing of %s and ship Q is on a bearing of %s. What is the angle between the two lines of sight?" % (tb(b), tb(c))
        right = "%d°" % d
        w = ["%d°" % (360 - d), "%d°" % ((b + c) % 360), "%d°" % abs(180 - d) if abs(180 - d) != d else "%d°" % (d + 10)]
        e = "Subtract the bearings: |%d° − %d°| = %d°%s." % (c, b, abs(c - b), " and 360° − that is smaller" if abs(c - b) > 180 else "")
    w = [v for v in dict.fromkeys(w) if v != right]
    return mcq(q, right, w, e + " <b>%s</b>." % right)


ELEV = [("A lighthouse is %(h)d feet tall. From the top, the angle of depression to a boat is %(a)d°. How far is the boat from the base of the lighthouse?", "adj", "feet"),
        ("A kite string is %(h)d feet long and makes an angle of %(a)d° with the ground. How high is the kite?", "opp_hyp", "feet"),
        ("From a point %(h)d meters from the base of a building, the angle of elevation to the top is %(a)d°. How tall is the building?", "opp_adj", "meters"),
        ("A ramp rises at an angle of %(a)d° and is %(h)d feet long. How high does it rise?", "opp_hyp", "feet"),
        ("A plane flying at %(h)d feet sees a runway at an angle of depression of %(a)d°. How far is the plane from the runway along its line of sight?", "hyp", "feet")]


def one_elev(r):
    t, kind, u = r.choice(ELEV)
    a = r.choice([12, 15, 18, 20, 25, 28, 32, 35, 40, 48, 52, 58, 65])
    h = r.choice([30, 40, 50, 60, 75, 80, 100, 120, 150, 200, 250])
    if "plane" in t:
        h = r.choice([2000, 3000, 4500, 6000, 8000])
    rad = math.radians(a)
    if kind == "adj":
        v, wrong = h / math.tan(rad), [h * math.tan(rad), h / math.sin(rad), h * math.cos(rad)]
        how = "tan %d° = %d ÷ <i>d</i>, so <i>d</i> = %d ÷ tan %d°" % (a, h, h, a)
    elif kind == "opp_hyp":
        v, wrong = h * math.sin(rad), [h * math.cos(rad), h * math.tan(rad), h / math.sin(rad)]
        how = "sin %d° = <i>h</i> ÷ %d, so <i>h</i> = %d sin %d°" % (a, h, h, a)
    elif kind == "opp_adj":
        v, wrong = h * math.tan(rad), [h * math.sin(rad), h / math.tan(rad), h * math.cos(rad)]
        how = "tan %d° = <i>h</i> ÷ %d, so <i>h</i> = %d tan %d°" % (a, h, h, a)
    else:
        v, wrong = h / math.sin(rad), [h / math.tan(rad), h * math.sin(rad), h / math.cos(rad)]
        how = "sin %d° = %s ÷ <i>d</i>, so <i>d</i> = %s ÷ sin %d°" % (a, comma(h), comma(h), a)
    right = "%s %s" % (n1(v), u)
    w = ["%s %s" % (n1(x), u) for x in wrong]
    q = t % {"h": h, "a": a} if "plane" not in t else t.replace("%(h)d", comma(h)) % {"a": a}
    return mcq(q + " Round to the nearest tenth.", right, w, "%s ≈ %s. <b>%s</b>." % (how, n1(v), right))


def build():
    sets, R = build_sets([
        ("Compass and true bearings", [("collect", uniq(one_conv), 20)]),
        ("North and east components", [("collect", uniq(one_comp), 20)]),
        ("Two-leg trips", [("collect", uniq(one_two), 20)]),
        ("Back bearings and angles between bearings", [("collect", uniq(one_back), 20)]),
        ("Angles of elevation and depression", [("collect", uniq(one_elev), 20)]),
    ], 69818)
    finish(sets, R)
    body = lesson('<ul><li>A <b>true bearing</b> is measured clockwise from north, with three digits: 045°. A <b>compass bearing</b> like N 45° E starts at north or south and turns toward east or west.</li><li>Standard-position angle θ = 90° − bearing.</li><li>For a trip of distance <i>d</i> on bearing β: north component <i>d</i> cos β, east component <i>d</i> sin β.</li><li>The angle of elevation is measured up from the horizontal; the angle of depression is measured down from the horizontal.</li></ul>',
        [example("20 miles on a bearing of 060°", ["North: 20 cos 60° = 10", "East: 20 sin 60° ≈ 17.3"], "10 miles north, 17.3 miles east")],
        [['Measuring from the <i>x</i>-axis', 'Bearings start at north and go clockwise.'], ['Sine for the north component', 'North uses cosine of the bearing.'], ['The depression angle at the wrong corner', 'It equals the elevation angle from the other end.']])
    faq = [('What does TEKS P.4E ask?', 'Determine the value of trigonometric ratios of angles and solve problems involving trigonometric ratios in mathematical and real-world problems.'), ('What does TEKS P.4F ask?', 'Use trigonometry in mathematical and real-world problems, including directional bearing.'), ('Why do bearings use three digits?', 'So 045° and 450 cannot be confused, and all directions look the same.'), ('How do I find a back bearing?', 'Add 180° (or subtract it if the bearing is over 180°).')]
    make('bearings-and-angles-of-elevation', 18, 'Number and Measure', 'P.4E, P.4F',
         'P.4E determine the value of trigonometric ratios of angles and solve problems involving trigonometric ratios in mathematical and real-world problems; P.4F use trigonometry in mathematical and real-world problems, including directional bearing',
         'Bearings and Angles of Elevation', 'Bearings and Elevation',
         'Free Precalculus worksheets on bearings and angles of elevation for Texas TEKS P.4E and P.4F: true and compass bearings, trip components, two-leg trips, back bearings and elevation. 100 questions with answers.',
         'Bearings are measured clockwise from north.', 'North component d cos β; east component d sin β.',
         body, faq, sets, seo_title='Precalculus Bearings and Angles of Elevation Worksheets (TEKS P.4E, P.4F)')


if __name__ == "__main__":
    build()
