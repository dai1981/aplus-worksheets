# -*- coding: utf-8 -*-
"""
Texas Grade 7 Math: Constant Rate of Change and d = rt (TEKS 7.4A)
  python3 tools/gen_ustx_math_g7_constant_rate.py
Using d = rt to find distance, rate or time, finding a constant rate of change from tables, reading slope from a
graph, and unit rates as slope (own d = rt and table makers, plus the US Grade 8 slope makers with a new seed).
Wrong answers come from real mistakes: multiplying when you should divide, mixing up minutes and hours, and
reading the rate from one pair only.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_g8_slope as sl
adopt(sl)
sl.R = random.Random(670050)
tx_common.GRADE = "grade-7"

def one_d(r):
    k = Kid(r).next()
    kind = r.choice(["car", "bike", "walk", "train", "plane"])
    rate, u, h = {"car": (r.choice([55, 60, 65, 70, 75]), "mi", r.choice([2, 3, 4, 5, 1.5, 2.5])), "bike": (r.choice([10, 12, 14, 15, 16]), "mi", r.choice([2, 3, 1.5, 2.5])),
                  "walk": (r.choice([3, 4]), "mi", r.choice([2, 3, 1.5, 2.5])), "train": (r.choice([80, 90, 110, 120]), "km", r.choice([2, 3, 4, 1.5])),
                  "plane": (r.choice([450, 480, 500, 520]), "mi", r.choice([2, 3, 4, 1.5]))}[kind]
    d = rate * h
    hs = "%g" % h
    q = {"car": "A car drives at a constant %d mi/h for %s hours. How far does it go?" % (rate, hs),
         "bike": "%s rides a bike at a steady %d mi/h for %s hours. How far does %s ride?" % (k["n"], rate, hs, k["he"]),
         "walk": "%s walks at a steady %d mi/h for %s hours. How far does %s walk?" % (k["n"], rate, hs, k["he"]),
         "train": "A train travels at a constant %d km/h for %s hours. How far does it go?" % (rate, hs),
         "plane": "A plane flies at a constant %d mi/h for %s hours. How far does it fly?" % (rate, hs)}[kind]
    ds = comma(int(d)) if d == int(d) else "%g" % d
    return mcq(q, "%s %s" % (ds, u), ["%g %s" % (rate + h, u), "%g %s" % (rate / h if rate % h == 0 else rate * 2, u), "%s %s" % (comma(int(d * 10)) if d * 10 == int(d * 10) else "%g" % (d * 10), u)],
               "d = r × t = %d × %s = <b>%s %s</b>." % (rate, hs, ds, u))


def one_rt(r):
    rate = r.choice([8, 12, 15, 40, 45, 50, 60, 64, 72])
    t = r.choice([2, 3, 4, 5, 6])
    d = rate * t
    if r.random() < 0.5:
        return mcq("A truck goes %s miles in %d hours at a constant speed. What is its rate?" % (comma(d), t), "%d mi/h" % rate, ["%s mi/h" % comma(d * t), "%d mi/h" % (d - t), "%d mi/h" % (rate * 2)],
                   "r = d ÷ t = %s ÷ %d = <b>%d mi/h</b>." % (comma(d), t, rate))
    who = "A cyclist rides" if rate <= 16 else "A family drives"
    return mcq("%s %s miles at a constant %d mi/h. How long does the trip take?" % (who, comma(d), rate), "%d hours" % t, ["%s hours" % comma(d * rate), "%d hours" % (d - rate), "%d hours" % (t + 2)],
               "t = d ÷ r = %s ÷ %d = <b>%d hours</b>." % (comma(d), rate, t))


def one_table(r):
    m = r.choice([2, 3, 4, 5, 6, 8, 12, 15, 25])
    b = r.choice([0, 0, r.randint(5, 40)])
    st = r.choice([1, 2])
    xs = [st * i for i in range(1, 5)]
    ys = [m * x + b for x in xs]
    ctx = r.choice([("Hours", "Miles"), ("Minutes", "Gallons in the tank"), ("Weeks", "Dollars saved"), ("Days", "Pages read")])
    th = "".join("<td>%d</td>" % x for x in xs)
    td = "".join("<td>%s</td>" % comma(y) for y in ys)
    pic = "<div class='sn-tw'><table class='sn-table'><tbody><tr><th>%s</th>%s</tr><tr><th>%s</th>%s</tr></tbody></table></div>" % (ctx[0], th, ctx[1], td)
    w = ["%d" % (ys[1] - ys[0]) if st != 1 else "%d" % (m + 1), "%d" % (ys[0] // xs[0]) if ys[0] % xs[0] == 0 and ys[0] // xs[0] != m else "%d" % (m * 2), "%d" % ys[0], "%d" % (m + 2)]
    w = [x for x in dict.fromkeys(w) if x != str(m)]
    return mcq(pic + "What is the constant rate of change (%s per %s)?" % (ctx[1].lower().split(" ")[0], ctx[0].lower().rstrip("s")), str(m), w,
               "Change in %s ÷ change in %s = (%s − %s) ÷ (%d − %d) = %d ÷ %d = <b>%d</b>." % (ctx[1].lower(), ctx[0].lower(), comma(ys[1]), comma(ys[0]), xs[1], xs[0], ys[1] - ys[0], xs[1] - xs[0], m))


def build():
    sets, R = build_sets([
        ("Use d = rt to find the distance", [("collect", one_d, 20)]),
        ("Use d = rt to find the rate or the time", [("collect", one_rt, 20)]),
        ("Constant rate of change in a table", [("collect", one_table, 20)]),
        ("Rate of change from a graph", [("run", sl.set_graph, (), 20)]),
        ("The unit rate as the rate of change", [("run", sl.set_prop, (), 20)]),
    ], 67005)
    finish(sets, R)
    body = lesson('<ul><li>A <b>constant rate of change</b> means y changes by the same amount each time x goes up by 1.</li><li>Rate of change = change in y ÷ change in x.</li><li>For motion at a constant speed, use <b>d = rt</b> (distance = rate × time). Then r = d ÷ t and t = d ÷ r.</li><li>On a graph, a constant rate of change is a straight line.</li></ul>',
        [example("60 mi/h for 2.5 hours", ["d = 60 × 2.5"], "150 miles"), example("Hours 1, 2, 3; miles 45, 90, 135", ["(90 − 45) ÷ (2 − 1)"], "45 miles per hour")],
        [['Multiplying when you should divide', 'To find r, divide: r = d ÷ t.'], ['Mixing up minutes and hours', 'Change 30 minutes to 0.5 hour first.'], ['Reading the rate from one pair only', 'Use the change in y ÷ change in x.']])
    faq = [('What does TEKS 7.4A ask?', 'Represent constant rates of change in mathematical and real-world problems given pictorial, tabular, verbal, numeric, graphical and algebraic representations, including d = rt.'), ('What does d = rt mean?', 'Distance equals rate times time.'), ('Is a rate of change the same as a unit rate?', 'Yes, when it is the change for 1 unit of x.'), ('How do I see a constant rate on a graph?', 'The points lie on a straight line.')]
    make('constant-rate-of-change', 5, 'Proportionality', '7.4A',
         '7.4A represent constant rates of change in mathematical and real-world problems given pictorial, tabular, verbal, numeric, graphical, and algebraic representations, including d = rt',
         'Constant Rate of Change and d = rt', 'Constant Rate of Change',
         'Free Grade 7 worksheets for Texas TEKS 7.4A: d = rt for distance, rate and time, constant rates of change in tables and graphs, and unit rates. 100 questions with answers.',
         'Rate of change = change in y ÷ change in x.', 'd = rt: 60 mi/h for 2.5 h is 150 miles.',
         body, faq, sets, seo_title='Grade 7 Constant Rate of Change and d = rt Worksheets (TEKS 7.4A, STAAR)')


if __name__ == "__main__":
    build()
