# -*- coding: utf-8 -*-
"""
Texas Kindergarten Math: Sorting and Picture Graphs (TEKS K.8A, K.8B, K.8C)
  python3 tools/gen_ustx_math_gk_graphs.py
Which does not belong, sorting by color or shape, the most and the fewest (US Kindergarten makers with Texas names),
and reading and comparing picture graphs (the Australian Foundation makers with US spelling).
Wrong answers come from real mistakes: counting a picture twice, reading the wrong row, and picking the row with the
biggest pictures.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import gen_us_math_gk_sort_and_count as sc
adopt(sc)
import gen_au_maths_f_sorting_and_data as sd
adopt(sd)
tx_common.GRADE = "kindergarten"



def build():
    sets, R = build_sets([
        ("Which does not belong?", [("run", sc.set_odd, ("rnd", sc.Kids), 20)]),
        ("Sort by color or shape", [("run", sc.set_shapes, ("rnd", sc.Kids), 20)]),
        ("Most and fewest", [("run", sc.set_most, ("rnd", sc.Kids), 20)]),
        ("Read a picture graph", [("run", sd.set_read, ("rnd",), 20)]),
        ("Compare the data", [("run", sd.set_compare, ("rnd",), 20)]),
    ], 69015)
    finish(sets, R)
    body = lesson('<ul><li><b>Sort</b> things into 2 or 3 groups: by color, shape or kind.</li><li>Count each group.</li><li>In a <b>picture graph</b>, each picture is one thing. The row with the most pictures is the most.</li></ul>',
        [example("Dogs 5, cats 3", ["5 is more than 3"], "more dogs")],
        [['Counting a picture twice', 'Touch each picture once.'], ['Reading the wrong row', 'Find the label first.'], ['Picking the longest row by looks', 'Count the pictures.']])
    faq = [('What does TEKS K.8A ask?', 'Collect, sort, and organize data into two or three categories.'), ('What does TEKS K.8B ask?', 'Use data to create real-object and picture graphs.'), ('What does TEKS K.8C ask?', 'Draw conclusions from real-object and picture graphs.'), ('What is a picture graph?', 'A graph where each picture stands for one thing.')]
    make('sorting-and-picture-graphs', 15, 'Data Analysis', 'K.8A, K.8B, K.8C',
         'K.8A collect, sort, and organize data into two or three categories; K.8B use data to create real-object and picture graphs; K.8C draw conclusions from real-object and picture graphs',
         'Sorting and Picture Graphs', 'Sorting and Picture Graphs',
         'Free kindergarten data worksheets for Texas TEKS K.8: sort into groups, count, read picture graphs and compare data. 100 questions with answers.',
         'Sort, count, then compare.', 'The row with the most pictures is the most.',
         body, faq, sets, seo_title='Kindergarten Sorting and Picture Graphs Worksheets (TEKS K.8)')


if __name__ == "__main__":
    build()
