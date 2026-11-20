# -*- coding: utf-8 -*-
"""
South Africa Grade 4 Maths (CAPS): Pictographs, Bar Graphs and Pie Charts (Grade 4: 5.2 Representing data; 5.3 Analysing, interpreting and reporting data)
  python3 tools/gen_za_maths_g4_representing_data.py
Reading and drawing pictographs and bar graphs (Australia Year 4, UK Year 4 and US Grade 3 makers), comparing and
two-step questions, and reading simple pie charts (UK Year 6 maker).
Wrong answers come from real mistakes: forgetting the key in a pictograph, reading a bar between grid lines wrongly,
and reading a pie chart part as a number of people.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_au_maths_y4_data as aud
adopt(aud)
if hasattr(aud, 'R'): aud.R = random.Random(804280)
import gen_uk_maths_y4_statistics as uks
adopt(uks)
if hasattr(uks, 'R'): uks.R = random.Random(804281)
import gen_us_math_g3_picture_bar_graphs as usg
adopt(usg)
if hasattr(usg, 'R'): usg.R = random.Random(804282)
import gen_uk_maths_y6_pie_line as ukp
adopt(ukp)
if hasattr(ukp, 'R'): ukp.R = random.Random(804283)
za_common.GRADE = "grade-4"



def build():
    sets, R = build_sets([
        ("Pictographs", [("run", aud.set_pictograph, ("rnd", aud.Picker), 10), ("run", uks.set_pictogram, ("rnd", uks.Picker), 10)]),
        ("Bar graphs", [("run", aud.set_column, ("rnd", aud.Picker), 10), ("run", uks.set_bar, ("rnd", uks.Picker), 10)]),
        ("Compare in graphs", [("run", usg.set_compare, ("rnd", usg.Picker), 20)]),
        ("Two-step questions", [("run", usg.set_two_step, ("rnd", usg.Picker), 20)]),
        ("Pie charts", [("run", ukp.set_fractions, (), 20)]),
    ], 80428)
    finish(sets, R)
    body = lesson('<ul><li>A <b>pictograph</b> uses pictures. Read the key: one picture may stand for 2, 5 or 10.</li><li>A <b>bar graph</b> uses bars. Read the scale on the side and the top of each bar.</li><li>A <b>pie chart</b> shows parts of a whole: half the circle is half of the data.</li><li>Answer questions, compare categories and write a short summary of what the graph shows.</li></ul>',
        [example("Key: one picture = 5 learners; 4 pictures", ["4 × 5"], "20 learners")],
        [['Forgetting the key', 'Multiply by what one picture stands for.'], ['Between grid lines', 'Halfway between 10 and 20 is 15.'], ['Pie part as a number', 'A quarter of 40 learners is 10.']])
    faq = [('What does CAPS Grade 4 say about graphs?', 'Draw pictographs and bar graphs, and read, interpret and report on data in words, pictographs, bar graphs and pie charts.'), ('What is a key?', 'It tells what one picture stands for.'), ('When is a pie chart useful?', 'To show parts of a whole.'), ('What should learners write about a graph?', 'The biggest and smallest groups and what that means.')]
    make('pictographs-bar-graphs-and-pie-charts', 28, 'Data Handling', 'Grade 4: 5.2 Representing data; 5.3 Analysing, interpreting and reporting data',
         'Draw a variety of graphs to display and interpret data, including pictographs and bar graphs; critically read and interpret data represented in words, pictographs, bar graphs and pie charts; analyse data by answering questions related to data categories and report on the data.',
         'Pictographs, Bar Graphs and Pie Charts', 'Pictographs, Bar Graphs and Pie Charts',
         'Free CAPS Grade 4 data handling worksheets: pictographs with keys, bar graphs, comparing data, two-step questions and pie charts. 100 questions with memos.',
         'Read the key or the scale first.', 'A pie chart shows parts of a whole.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
