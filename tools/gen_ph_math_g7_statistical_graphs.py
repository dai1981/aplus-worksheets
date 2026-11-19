# -*- coding: utf-8 -*-
"""
Philippines Grade 7 Math (MATATAG): Pie Graphs, Bar Graphs, Line Graphs and Stem-and-Leaf Plots (Grade 7: Data and Probability)
  python3 tools/gen_ph_math_g7_statistical_graphs.py
Reading pie graphs and finding amounts and angles (BC Grade 7 makers), stem-and-leaf plots (Australia Year 7
makers), choosing the right graph and interpreting graphs (Ontario Grade 7 makers).
Wrong answers come from real mistakes: reading a pie graph percent as an amount, misreading a stem-and-leaf key, and
using a line graph for data that does not change over time.
"""
import ph_common
from ph_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, peso, words)
import random
import gen_cabc_math_g7_circle_graphs as cbg
adopt(cbg)
if hasattr(cbg, 'R'): cbg.R = random.Random(707200)
import gen_au_maths_y7_stem_and_leaf_plots as aus
adopt(aus)
if hasattr(aus, 'R'): aus.R = random.Random(707201)
import gen_caon_math_g7_data as cad
adopt(cad)
if hasattr(cad, 'R'): cad.R = random.Random(707202)
ph_common.GRADE = "grade-7"

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


def one_pie(r):
    p = r.choice([5, 10, 15, 20, 25, 30, 35, 40, 45, 55, 60, 65, 70, 75, 80])
    a = p * 360 // 100
    if p * 360 % 100:
        raise AssertionError
    what = r.choice(["rice", "transportation", "school expenses", "electricity", "savings", "rent"])
    if r.random() < 0.5:
        return mcq("In a pie graph of a family's budget, %s is %d%%. What is the angle of its sector?" % (what, p), "%d°" % a, ["%d°" % x for x in (p, 3 * p, 360 - a)],
                   "%d%% of 360° = %s × 360° = <b>%d°</b>." % (p, "%g" % (p / 100), a))
    return mcq("In a pie graph of a family's budget, the sector for %s is %d°. What percent of the budget is it?" % (what, a), "%d%%" % p, ["%d%%" % x for x in (a // 3 if a // 3 != p else p + 5, 100 - p, p * 2)],
               "%d° ÷ 360° × 100%% = <b>%d%%</b>." % (a, p))


def build():
    sets, R = build_sets([
        ("Read a pie graph", [("run", cbg.set_read, (), 10), ("run", cbg.set_amounts, (), 10)]),
        ("Angles in a pie graph", [("run", cbg.set_degrees, (), 14), ("collect", uniq(one_pie), 6)]),
        ("Stem-and-leaf plots", [("collect", aus.one_read, 10), ("collect", aus.one_build, 10)]),
        ("Choose the right graph", [("run", cad.set_choose, (), 12), ("run", cad.set_make, (), 8)]),
        ("Interpret graphs", [("run", cad.set_read, (), 10), ("run", cad.set_claims, (), 10)]),
    ], 70720)
    finish(sets, R)
    body = lesson("<ul><li>A <b>pie graph</b> (circle graph) shows parts of a whole. Each part's angle is its percent × 360°.</li><li>A <b>bar graph</b> compares categories. A <b>line graph</b> shows change over time.</li><li>A <b>stem-and-leaf plot</b> keeps every value: the stem is the tens digit and each leaf is a ones digit. Read the key: 4 | 7 means 47.</li><li>Before interpreting, read the title, the labels and the scale.</li></ul>",
        [example("25% of a pie graph", ["0.25 × 360°"], "90°")],
        [['Percent as amount', 'Multiply the percent by the total.'], ['Ignoring the key', 'Check what one stem and leaf mean.'], ['Line graph for categories', 'Use a bar graph for categories.']])
    faq = [('What does MATATAG Math 7 ask about graphs?', 'Use appropriate graphs to represent organized data (pie graph, bar graph, line graph, and stem-and-leaf plot) and interpret statistical graphs.'), ('When should I use a pie graph?', 'When showing parts of one whole.'), ('Why use a stem-and-leaf plot?', 'It shows the shape of the data and keeps every value.'), ('Can a bar graph be misleading?', 'Yes, if the scale does not start at 0.')]
    make('statistical-graphs', 20, 'Data and Probability', 'Grade 7: Data and Probability',
         'Use appropriate graphs to represent organized data: pie graph, bar graph, line graph, and stem-and-leaf plot; interpret statistical graphs.',
         'Pie Graphs, Bar Graphs, Line Graphs and Stem-and-Leaf Plots', 'Statistical Graphs',
         'Free Grade 7 statistical graphs worksheets for the DepEd MATATAG curriculum: pie graphs, bar graphs, line graphs, stem-and-leaf plots and choosing the right graph. 100 questions with answers.',
         'Pie: parts of a whole. Bar: compare. Line: change over time.', 'Pie graph angle = percent × 360°.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
