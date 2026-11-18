# -*- coding: utf-8 -*-
"""
SG Secondary 2 Maths: Map Scales (MOE syllabus N2 Ratio and Proportion: map scales, distance and area)
  python3 tools/gen_sg_maths_s2_map_scales.py
Map distance to actual distance, actual distance to map distance, writing a scale as 1 : n, area scales
(square the length scale) and mixed map problems.
Wrong answers come from real mistakes: converting cm to km with the wrong power of 10, multiplying when the
map distance is asked, using the length scale for area, and writing the ratio the wrong way round.
"""
import random
from fractions import Fraction as F
from sg_sec import num, B, S, make, lesson, collect, QN, T, People, PLACES

R = random.Random(820900)
P = People(R)
SCALES = [10000, 20000, 25000, 50000, 100000, 200000, 250000, 500000]


def ratio(n):
    return "1 : %s" % num(n)


def km(cm):
    return F(cm, 100000)


# ------------------------------------------------------------ set 1: map to actual
def one_actual(r):
    n = r.choice(SCALES)
    d = r.choice([2, 3, 4, 5, 6, 8, F(5, 2), F(7, 2), F(3, 2), 12])
    act = d * n
    unit = r.choice(["km", "m"]) if act < 100000 else "km"
    val = km(act) if unit == "km" else F(act, 100)
    if val.denominator not in (1, 2, 4, 5, 10, 20, 25, 50, 100):
        return None
    q = "A map has a scale of %s. Two places are %s cm apart on the map. What is the actual distance in %s?" % (B(ratio(n)), num(d), unit)
    wrong_unit = F(act, 1000) if unit == "km" else km(act)
    e = "%s cm × %s = %s cm = <b>%s %s</b>. (1 m = 100 cm, 1 km = 100 000 cm.)" % (num(d), num(n), num(act), num(val), unit)
    return QN(q, val, [wrong_unit, val * 10, F(d, n) * 100000 if unit == "km" else val / 10], e, unit=" " + unit)


# ------------------------------------------------------------ set 2: actual to map
def one_map(r):
    n = r.choice(SCALES)
    d_km = r.choice([1, 2, 3, F(1, 2), F(3, 2), 5, 10, 4, F(5, 2), 8])
    cm = F(d_km) * 100000 / n
    if cm.denominator not in (1, 2, 4, 5, 10) or cm > 40 or cm < F(1, 2):
        return None
    q = "On a map with scale %s, how long is a road that is %s km long in real life?" % (B(ratio(n)), num(d_km))
    e = "%s km = %s cm. %s ÷ %s = <b>%s cm</b>." % (num(d_km), num(d_km * 100000), num(d_km * 100000), num(n), num(cm))
    return QN(q, cm, [cm * 10, cm / 10, d_km * n], e, unit=" cm")


# ------------------------------------------------------------ set 3: writing the scale
def one_scale(r):
    kind = r.choice(["rep", "rep", "find"])
    if kind == "rep":
        a = r.choice([F(1, 2), 1, 2, 5, F(1, 4), 3, 4])
        unit = "km" if a >= 1 else "m"
        real_cm = a * 100000 if unit == "km" else a * 1000 * 100 / 1000 * 1000
        if unit == "m":
            m = r.choice([50, 100, 200, 250, 500])
            real_cm = F(m * 100)
            shown = "%s m" % num(m)
        else:
            shown = "%s km" % num(a)
        n = real_cm
        q = "On a map, 1 cm represents %s. Write the scale in the form 1 : <i>n</i>." % shown
        e = "%s = %s cm, so the scale is <b>%s</b>." % (shown, num(n), ratio(n))
        return T(q, ratio(n), [ratio(n / 100), ratio(n / 1000) if n >= 1000 else ratio(n * 10), "%s : 1" % num(n)], e)
    map_cm = r.choice([2, 4, 5, 8, 3])
    real_km = r.choice([1, 2, 4, 10, 20, 5])
    n = F(real_km * 100000, map_cm)
    if n.denominator != 1:
        return None
    q = "Two towns are %s km apart. On a map they are %s cm apart. Find the scale of the map in the form 1 : <i>n</i>." % (num(real_km), num(map_cm))
    e = "%s km = %s cm. %s ÷ %s = %s, so the scale is <b>%s</b>." % (num(real_km), num(real_km * 100000), num(real_km * 100000), num(map_cm), num(n), ratio(n))
    return T(q, ratio(n), [ratio(n * map_cm), ratio(n / 1000) if n > 1000 else ratio(n * 2), "%s : %s" % (num(map_cm), num(real_km))], e)


# ------------------------------------------------------------ set 4: area scales
def one_area(r):
    k = r.choice([F(1, 2), 1, 2, 3, 4, 5])          # 1 cm represents k km
    kind = r.choice(["unit", "area", "area", "back"])
    if kind == "unit":
        q = "On a map, 1 cm represents %s km. What area does 1 cm² on the map represent?" % num(k)
        e = "Square the length scale: 1 cm² represents %s² = <b>%s km²</b>." % (num(k), num(k * k))
        return QN(q, k * k, [k, 2 * k, k * 100], e, unit=" km²")
    if kind == "area":
        a = r.choice([2, 3, 5, 6, F(3, 2), 8, 12])
        ans = a * k * k
        q = "On a map, 1 cm represents %s km. A park covers %s cm² on the map. What is its actual area?" % (num(k), num(a))
        e = "1 cm² represents %s km². %s × %s = <b>%s km²</b>." % (num(k * k), num(a), num(k * k), num(ans))
        return QN(q, ans, [a * k, a * 2 * k, a * k * k * 10], e, unit=" km²")
    act = r.choice([4, 9, 16, 25, 36, 18, 50])
    if F(act, k * k).denominator not in (1, 2, 4):
        return None
    ans = F(act, k * k)
    q = "On a map, 1 cm represents %s km. A lake has an actual area of %s km². What is its area on the map?" % (num(k), num(act))
    e = "1 cm² represents %s km². %s ÷ %s = <b>%s cm²</b>." % (num(k * k), num(act), num(k * k), num(ans))
    return QN(q, ans, [F(act, k), act * k * k, F(act, 2 * k)], e, unit=" cm²")


# ------------------------------------------------------------ set 5: problems
def one_prob(r):
    nm, he, his = P.next()
    a, b = r.sample(PLACES, 2)
    kind = r.choice(["walk", "area2", "compare", "time"])
    if kind == "walk":
        n = r.choice([25000, 50000, 20000])
        d = r.choice([6, 8, 10, 12, 9])
        dist = F(d * n, 100000)
        speed = r.choice([4, 5, 6])
        t = dist / speed
        if t.denominator not in (1, 2, 4):
            return None
        q = "On a map of scale %s, the path from %s to %s is %s cm long. %s walks at %s km/h. How long does the walk take, in hours?" % (B(ratio(n)), a, b, num(d), nm, num(speed))
        e = "Actual distance = %s × %s cm = %s km. Time = %s ÷ %s = <b>%s hours</b>." % (num(d), num(n), num(dist), num(dist), num(speed), num(t))
        return QN(q, t, [dist, t * 10, F(d, speed)], e, unit=" hours")
    if kind == "area2":
        n = r.choice([50000, 20000, 10000])
        w, h = r.choice([(4, 3), (6, 2), (5, 4), (8, 5)])
        k = F(n, 100000)          # km per cm
        ans = w * h * k * k
        q = "A rectangular field is %s cm by %s cm on a map of scale %s. What is its actual area in km²?" % (num(w), num(h), B(ratio(n)))
        e = "Actual sides: %s km and %s km. Area = %s × %s = <b>%s km²</b>." % (num(w * k), num(h * k), num(w * k), num(h * k), num(ans))
        return QN(q, ans, [w * h * k, ans * 100, (w + h) * 2 * k], e, unit=" km²")
    if kind == "compare":
        n1, n2 = r.sample([10000, 25000, 50000, 100000], 2)
        q = "Which map shows more detail: one with scale %s or one with scale %s?" % (ratio(n1), ratio(n2))
        right = ratio(min(n1, n2))
        return T(q, "The map with scale %s" % right, ["The map with scale %s" % ratio(max(n1, n2)), "They show the same detail", "You cannot tell from the scale"],
                 "1 cm represents less ground on the %s map, so things look bigger: <b>%s</b> shows more detail." % (right, right))
    n = r.choice([200000, 250000, 500000])
    d = r.choice([4, 6, 8, 10])
    dist = F(d * n, 100000)
    sp = r.choice([60, 80, 50, 40])
    t = dist / sp
    if (t * 60).denominator != 1:
        return None
    q = "Two towns are %s cm apart on a map of scale %s. A bus travels between them at %s km/h. How many minutes does the trip take?" % (num(d), B(ratio(n)), num(sp))
    e = "Distance = %s km. Time = %s ÷ %s h = <b>%s minutes</b>." % (num(dist), num(dist), num(sp), num(t * 60))
    return QN(q, t * 60, [t, dist, t * 100], e, unit=" minutes")


def build():
    sets = [S("Map distance to actual distance", collect(one_actual, 20, R)),
            S("Actual distance to map distance", collect(one_map, 20, R)),
            S("Writing the scale as 1 : n", collect(one_scale, 20, R)),
            S("Area scales", collect(one_area, 20, R)),
            S("Map problems", collect(one_prob, 20, R))]
    body = lesson(
        "<ul><li>A scale of <b>1 : <i>n</i></b> means 1 cm on the map is <i>n</i> cm in real life.</li>"
        "<li>Map to real: multiply by <i>n</i>, then change units (100 cm = 1 m, 100 000 cm = 1 km).</li>"
        "<li>Real to map: change to cm first, then divide by <i>n</i>.</li>"
        "<li><b>Area</b>: if 1 cm represents <i>k</i> km, then 1 cm² represents <i>k</i>² km². Square the length scale.</li></ul>",
        [("A map has scale 1 : 50 000. Two places are 6 cm apart. Find the actual distance.", ["6 × 50 000 = 300 000 cm", "300 000 cm = 3 km"], "3 km"),
         ("1 cm represents 2 km. A lake is 5 cm² on the map. Find its actual area.", ["1 cm² represents 2² = 4 km²", "5 × 4 = 20"], "20 km²")],
        ["Using 1000 cm in a km. There are 100 000 cm in 1 km.",
         "Using the length scale for area. Square it: 1 cm : 3 km gives 1 cm² : 9 km².",
         "Writing the scale backwards as <i>n</i> : 1.",
         "Multiplying when you need the map distance. Real to map means divide."])
    faq = [("What does a map scale of 1 : 50 000 mean?", "1 cm on the map stands for 50 000 cm in real life, which is 500 m or 0.5 km."),
           ("How do you change a map distance into kilometres?", "Multiply the map distance in cm by the scale number, then divide by 100 000 to change cm into km."),
           ("How do area scales work?", "Square the length scale. If 1 cm represents 2 km, then 1 cm² represents 4 km²."),
           ("Which map shows more detail?", "The one with the smaller scale number, such as 1 : 10 000 compared with 1 : 100 000, because 1 cm covers less ground.")]
    make(2, "map-scales", 9, "N2",
         "Map Scales: Distance and Area",
         "",
         "Map scales",
         "",
         "Free Secondary 2 maths worksheets on map scales: map distance to actual distance, actual distance to map distance, writing scales as 1 : n, and area scales. 100 questions with answers.",
         "A scale of 1 : n means 1 cm on the map is n cm in real life.",
         "There are 100 000 cm in 1 km. For area, square the length scale.",
         body, faq, sets, R)


if __name__ == "__main__":
    build()
