# -*- coding: utf-8 -*-
"""
Texas Grade 3 Math: Frequency Tables, Dot Plots, Pictographs and Bar Graphs (TEKS 3.8A, 3.8B)
  python3 tools/gen_ustx_math_g3_data.py
Tally marks and frequency tables (the Ontario Grade 3 maker), pictographs with a key and scaled bar graphs (the US
Grade 3 makers), dot plots of categorical data, and one- and two-step problems, all with Texas names and US
spelling.
Wrong answers come from real mistakes: counting symbols without using the key, reading the bar between grid
lines as the next line, counting the dots in the wrong column, and stopping after one step.
"""
import random
from tx_common import (Kid, mcq, collect, finish, make, fig, figure, lesson, S, run_many, adopt, People, svg_wrap,
                       text, line, GREEN, INK, example)
import gen_caon_math_g3_data as on
import gen_us_math_g3_picture_bar_graphs as usg

adopt(on)
adopt(usg)
R = random.Random(62001)

TOPICS = [("Favorite fruit", ["Apple", "Banana", "Grapes", "Mango", "Peach"]),
          ("Favorite sport", ["Soccer", "Football", "Baseball", "Basketball", "Swimming"]),
          ("Pets at home", ["Dog", "Cat", "Fish", "Bird", "None"]),
          ("Weather in March", ["Sunny", "Cloudy", "Rainy", "Windy"]),
          ("How we get to school", ["Bus", "Car", "Walk", "Bike"]),
          ("Favorite Texas animal", ["Armadillo", "Longhorn", "Mockingbird", "Horned lizard"])]


def dot_plot(cats, vals, title):
    w = 92
    W = w * len(cats) + 40
    top = max(vals)
    H = 50 + top * 20 + 40
    base = H - 40
    s = [text(W / 2, 20, title, 15), line(20, base, W - 20, base, INK, 2)]
    for i, (c, v) in enumerate(zip(cats, vals)):
        cx = 20 + w * i + w / 2
        s.append(text(cx, base + 22, c, 13, weight=400))
        for j in range(v):
            s.append("<circle cx='%.1f' cy='%d' r='7' fill='%s'/>" % (cx, base - 12 - j * 20, GREEN))
    return svg_wrap(W, H, "".join(s), "dot plot of %s" % title.lower())


# ------------------------------------------------------------ set 4: dot plots
def one_dot(r):
    title, cats = r.choice(TOPICS)
    cats = cats[:r.choice([3, 4])] if len(cats) > 4 else cats
    vals = [r.randint(1, 9) for _ in cats]
    if len(set(vals)) < len(vals):
        return None
    pic = fig(dot_plot(cats, vals, title))
    kind = r.choice(["count", "most", "fewest", "more", "total"])
    i, j = r.sample(range(len(cats)), 2)
    if kind == "count":
        return mcq(pic + "Each dot is 1 student. How many students chose <b>%s</b>?" % cats[i], vals[i], [vals[j], vals[i] + 1, vals[i] - 1 if vals[i] > 1 else vals[i] + 2, sum(vals)],
                   "Count the dots above %s: <b>%d</b>." % (cats[i], vals[i]))
    if kind in ("most", "fewest"):
        t = max(vals) if kind == "most" else min(vals)
        c = cats[vals.index(t)]
        return mcq(pic + "Which choice has the %s dots?" % kind, c, [x for x in cats if x != c], "The %s column of dots is %s: <b>%s</b> (%d)." % (c, "tallest" if kind == "most" else "shortest", c, t))
    if kind == "more":
        a, b = (i, j) if vals[i] > vals[j] else (j, i)
        d = vals[a] - vals[b]
        return mcq(pic + "How many more students chose %s than %s?" % (cats[a], cats[b]), d, [vals[a] + vals[b], vals[a], d + 1, d - 1 if d > 1 else d + 2],
                   "%d − %d = <b>%d</b>." % (vals[a], vals[b], d))
    return mcq(pic + "How many students are shown in the dot plot in all?", sum(vals), [sum(vals) - vals[i], sum(vals) + 1, len(cats), max(vals) * len(cats)],
               "Add the dots in every column: %s = <b>%d</b>." % (" + ".join(map(str, vals)), sum(vals)))


def build():
    sets = [S("Tally marks and frequency tables", run_many(on.set_tally, "rnd", seed=211)),
            S("Pictographs with a key", run_many(usg.set_picture, "rnd", usg.Picker, seed=212)),
            S("Bar graphs with scaled intervals", run_many(usg.set_bar, "rnd", usg.Picker, seed=213)),
            S("Dot plots", collect(one_dot, 20, R))]
    sets.append(S("One- and two-step problems", run_many(usg.set_compare, "rnd", usg.Picker, seed=214, n=10, avoid=sets) + run_many(usg.set_two_step, "rnd", usg.Picker, seed=215, n=10, avoid=sets)))
    finish(sets, R)
    body = lesson(
        "<ul><li>A <b>frequency table</b> lists each category and how many (often with tally marks).</li>"
        "<li>A <b>pictograph</b> uses a key: if each picture is 2 students, 4 pictures mean 8 students.</li>"
        "<li>A <b>bar graph with scaled intervals</b> counts by 2s, 5s or 10s. A bar between two lines is halfway between their numbers.</li>"
        "<li>A <b>dot plot</b> shows one dot for each answer above its category.</li>"
        "<li>To solve problems, read each number you need, then add or subtract. Some questions take two steps.</li></ul>",
        [figure(dot_plot(["Bus", "Car", "Walk", "Bike"], [6, 4, 3, 2], "How we get to school"), "6 by bus, 4 by car, 3 walk and 2 by bike. 6 − 4 = 2 more ride the bus than come by car."),
         example("A pictograph key says each star is 5 books. Maya's row has 3 stars. How many books?", ["3 stars × 5 books"], "15 books")],
        [["Counting pictures without using the key", "Multiply the number of pictures by the key."],
         ["Reading a bar between lines as the next line", "Halfway between 10 and 20 on a scale of 10 is 15."],
         ["Stopping after one step", "Check what the question asks: in all, how many more, or how many fewer?"]])
    faq = [("What does TEKS 3.8A ask?", "Summarize a data set with several categories using a frequency table, dot plot, pictograph or bar graph with scaled intervals."),
           ("What does TEKS 3.8B ask?", "Solve one- and two-step problems using categorical data shown in a frequency table, dot plot, pictograph or bar graph with scaled intervals."),
           ("What is a scaled interval?", "The amount between grid lines on a bar graph, such as 2, 5 or 10. It lets a graph show big numbers in a small space."),
           ("What is the difference between a pictograph and a dot plot?", "A pictograph uses pictures and a key, so one picture can stand for more than 1. A dot plot uses one dot for each piece of data.")]
    make("frequency-tables-dot-plots-and-bar-graphs", 20, "Data Analysis", "3.8A, 3.8B",
         "3.8A summarize a data set with multiple categories using a frequency table, dot plot, pictograph, or bar graph with scaled intervals; 3.8B solve one- and two-step problems using categorical data represented with a frequency table, dot plot, pictograph, or bar graph with scaled intervals",
         "Frequency Tables, Dot Plots, Pictographs and Bar Graphs", "Data and Graphs",
         "Free Grade 3 data worksheets for Texas TEKS 3.8A and 3.8B: tally marks and frequency tables, pictographs with a key, scaled bar graphs, dot plots and one- and two-step problems. 100 STAAR-style questions with answers.",
         "Read the key or the scale before you count.", "A picture or a grid space can stand for more than 1. Add or subtract the numbers you read to solve problems.",
         body, faq, sets, seo_title="Grade 3 Data Worksheets: Frequency Tables, Dot Plots and Bar Graphs (TEKS 3.8A, 3.8B)")


if __name__ == "__main__":
    build()
