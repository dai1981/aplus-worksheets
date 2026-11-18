# -*- coding: utf-8 -*-
"""
Texas Grade 1 Math: Tally Marks, Picture Graphs and Bar Graphs (TEKS 1.8A, 1.8B, 1.8C)
  python3 tools/gen_ustx_math_g1_graphs.py
Sorting and counting, tally charts, picture graphs, bar graphs, and how many in all, more and fewer (the US Grade 1
makers with Texas names).
Wrong answers come from real mistakes: counting a bundle of tallies as 1, reading the wrong row, and adding when the
question asks how many more.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import gen_us_math_g1_data as da
adopt(da)
tx_common.GRADE = "grade-1"



def build():
    sets, R = build_sets([
        ("Sort and count", [("run", da.set_sort, ("rnd",), 20)]),
        ("Read tally charts", [("run", da.set_tally, ("rnd", da.Picker), 20)]),
        ("Read picture graphs", [("run", da.set_picture, ("rnd", da.Picker), 20)]),
        ("Read bar graphs", [("run", da.set_bar, ("rnd", da.Picker), 20)]),
        ("How many in all, how many more, how many fewer", [("run", da.set_word, ("rnd", da.Picker), 20)]),
    ], 69119)
    finish(sets, R)
    body = lesson('<ul><li><b>Sort</b> things into groups, then count each group.</li><li>A <b>tally mark</b> is 1. A bundle of 5 tallies (four lines and one across) is 5.</li><li>In a <b>picture graph</b>, count the pictures. In a <b>bar graph</b>, read the number at the end of the bar.</li><li>How many more: subtract. In all: add.</li></ul>',
        [example("Tally: one bundle and 2 more", ["5 + 2"], "7")],
        [['Counting a bundle of tallies as 1', 'A bundle is 5.'], ['Reading the wrong row', 'Put your finger on the label first.'], ['Adding when asked how many more', 'How many more means subtract.']])
    faq = [('What does TEKS 1.8A ask?', 'Collect, sort, and organize data in up to three categories using models/representations such as tally marks or T-charts.'), ('What does TEKS 1.8B ask?', 'Use data to create picture and bar-type graphs.'), ('What does TEKS 1.8C ask?', 'Draw conclusions and generate and answer questions using information from picture and bar-type graphs.'), ('Why cross the fifth tally?', 'It makes groups of 5 easy to count.')]
    make('tally-marks-and-graphs', 19, 'Data Analysis', '1.8A, 1.8B, 1.8C',
         '1.8A collect, sort, and organize data in up to three categories using models/representations such as tally marks or T-charts; 1.8B use data to create picture and bar-type graphs; 1.8C draw conclusions and generate and answer questions using information from picture and bar-type graphs',
         'Tally Marks, Picture Graphs and Bar Graphs', 'Tally Marks and Graphs',
         'Free Grade 1 data worksheets for Texas TEKS 1.8: sort and count, tally charts, picture graphs, bar graphs and how many more or fewer. 100 questions with answers.',
         'Count tallies by 5s, then 1s.', 'One bundle and 2 more is 7.',
         body, faq, sets, seo_title='Grade 1 Tally Marks and Graphs Worksheets (TEKS 1.8)')


if __name__ == "__main__":
    build()
