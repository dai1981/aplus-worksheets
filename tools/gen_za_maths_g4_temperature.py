# -*- coding: utf-8 -*-
"""
South Africa Grade 4 Maths (CAPS): Temperature: Reading Thermometers in Degrees Celsius (Grade 4: 4.5 Temperature)
  python3 tools/gen_za_maths_g4_temperature.py
Reading thermometers, likely temperatures, differences between temperatures in South African cities and reading a
table of temperatures (own makers on the Australia Year 4 thermometer drawing), with positive whole numbers only, as
in CAPS Grade 4.
Wrong answers come from real mistakes: reading the next mark, adding when the question asks for a difference, and
choosing impossible temperatures.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)

za_common.GRADE = "grade-4"

def uniq(fn):
    """Never give the same question twice, even with other wrong answers."""
    seen = set()
    def f(r):
        it = fn(r)
        if it is None or it["q"] in seen:
            raise AssertionError("repeat")
        seen.add(it["q"])
        return it
    f.__name__ = fn.__name__
    return f


import gen_au_maths_y4_scales as _sc

CITIES = ["Johannesburg", "Cape Town", "Durban", "Pretoria", "Bloemfontein", "Polokwane", "Kimberley", "Upington"]


def one_read(r):
    hi = r.choice([40, 50])
    v = r.randint(4, hi - 4)
    where = r.choice(["in the classroom", "outside at noon", "in the fridge" if v < 10 else "in the shade", "in a cup of water"])
    svg = _sc.strip_svg(0, hi, 1, 10, v, "°C", kind="thermo")
    return mcq(fig(svg) + "What temperature does the thermometer show %s?" % where, "%d °C" % v, ["%d °C" % x for x in (v + 1, v - 1, v + 10 if v + 10 <= hi else v - 10)],
               "Find the top of the red line. Count from the 10s mark below it in 1s: <b>%d °C</b>." % v)


def one_diff(r):
    a, b = r.sample(CITIES, 2)
    x, y = r.randint(12, 36), r.randint(12, 36)
    if x == y:
        raise AssertionError
    kind = r.choice(["diff", "warmer", "change"])
    if kind == "diff":
        q = "One summer day it was %d °C in %s and %d °C in %s. What is the difference in temperature?" % (x, a, y, b)
        d = abs(x - y)
        return mcq(q, "%d °C" % d, ["%d °C" % v for v in (x + y, d + 2, max(x, y))], "%d − %d = <b>%d °C</b>." % (max(x, y), min(x, y), d))
    if kind == "warmer":
        q = "It was %d °C in %s and %d °C in %s. Which city was warmer, and by how many degrees?" % (x, a, y, b)
        w = a if x > y else b
        c = b if w == a else a
        d = abs(x - y)
        return mcq(q, "%s, by %d °C" % (w, d), ["%s, by %d °C" % (c, d), "%s, by %d °C" % (w, x + y), "%s, by %d °C" % (w, d + 1)], "%d &gt; %d, so %s was warmer by %d − %d = <b>%d °C</b>." % (max(x, y), min(x, y), w, max(x, y), min(x, y), d))
    m, n = r.randint(8, 18), r.randint(4, 14)
    q = "At 07:00 the temperature in %s was %d °C. By 14:00 it was %d °C warmer. What was the temperature at 14:00?" % (a, m, n)
    return mcq(q, "%d °C" % (m + n), ["%d °C" % v for v in (m - n if m > n else m + n + 2, n, m + n + 1)], "%d + %d = <b>%d °C</b>." % (m, n, m + n))


SENSE = [("a cup of hot tea", 70, [20, 7, 150]), ("water boiling in a kettle", 100, [50, 30, 200]), ("a healthy person's body", 37, [20, 60, 10]),
         ("a fridge", 4, [40, 25, 70]), ("a warm summer day in Durban", 30, [3, 80, 100]), ("a cold winter morning in Bloemfontein", 2, [25, 40, 60]),
         ("water from a cold tap", 15, [65, 100, 45]), ("an oven baking bread", 200, [37, 30, 70])]


def one_sense(r):
    t, v, w = r.choice(SENSE)
    return mcq("Which is the most likely temperature of %s?" % t, "%d °C" % v, ["%d °C" % x for x in w], "%s is about <b>%d °C</b>. (Water boils at 100 °C and freezes at 0 °C.)" % (t[0].upper() + t[1:], v))


def one_table(r):
    cs = r.sample(CITIES, 4)
    ts = r.sample(range(14, 34), 4)
    tbl = "<br>".join("%s: %d °C" % (c, t) for c, t in zip(cs, ts))
    kind = r.choice(["hot", "cold", "range"])
    if kind == "range":
        d = max(ts) - min(ts)
        return mcq("Midday temperatures:<br>%s<br>What is the difference between the highest and the lowest temperature?" % tbl, "%d °C" % d, ["%d °C" % x for x in (max(ts), min(ts) + max(ts), d + 1)],
                   "%d − %d = <b>%d °C</b>." % (max(ts), min(ts), d))
    t = max(ts) if kind == "hot" else min(ts)
    c = cs[ts.index(t)]
    return mcq("Midday temperatures:<br>%s<br>Which city was the %s?" % (tbl, "warmest" if kind == "hot" else "coolest"), c, [x for x in cs if x != c],
               "The %s temperature is %d °C in <b>%s</b>." % ("highest" if kind == "hot" else "lowest", t, c))


def build():
    sets, R = build_sets([
        ("Read the thermometer", [("collect", uniq(one_read), 20)]),
        ("Likely temperatures", [("collect", one_sense, 8), ("collect", uniq(one_read), 12)]),
        ("Temperature differences", [("collect", uniq(one_diff), 20)]),
        ("Temperature tables", [("collect", uniq(one_table), 20)]),
        ("Temperature problems", [("collect", uniq(one_diff), 20)]),
    ], 80425)
    finish(sets, R)
    body = lesson('<ul><li>We measure temperature in <b>degrees Celsius</b> (°C) with a thermometer.</li><li>Water freezes at 0 °C and boils at 100 °C. Our body temperature is about 37 °C.</li><li>Read the thermometer at the top of the liquid. Check what each small mark stands for.</li><li>The difference between two temperatures: subtract the lower from the higher.</li></ul>',
        [example("Durban 29 °C, Johannesburg 21 °C", ["29 − 21"], "8 °C warmer in Durban")],
        [['The next mark', 'Count the marks carefully from a number.'], ['Adding for a difference', 'Subtract to find the difference.'], ['Impossible values', 'Think: hot tea is not 7 °C.']])
    faq = [('What does CAPS Grade 4 say about temperature?', 'Read and record temperature in degrees Celsius using thermometers, and calculate temperature differences limited to positive whole numbers.'), ('What is room temperature?', 'About 20 to 25 °C.'), ('Why does CAPS use only positive numbers?', 'Negative numbers come in later grades.'), ('What does °C stand for?', 'Degrees Celsius.')]
    make('temperature', 25, 'Measurement', 'Grade 4: 4.5 Temperature',
         'Measure temperature in degrees Celsius using thermometers; read and record temperature; calculate temperature differences limited to positive whole numbers.',
         'Temperature: Reading Thermometers in Degrees Celsius', 'Temperature',
         'Free CAPS Grade 4 temperature worksheets: reading thermometers in degrees Celsius, likely temperatures, differences and temperature tables. 100 questions with memos.',
         'Water freezes at 0 °C and boils at 100 °C.', 'Difference: higher − lower.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
