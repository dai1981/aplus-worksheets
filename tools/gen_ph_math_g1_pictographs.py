# -*- coding: utf-8 -*-
"""
Philippines Grade 1 Math (MATATAG): Pictographs: Collecting, Showing and Reading Data (Grade 1: Data and Probability)
  python3 tools/gen_ph_math_g1_pictographs.py
Reading pictographs without a scale, most and fewest, how many more, totals, tally tables and picture graphs (Singapore
Primary 1, US Grade 1 and Australia Year 1 makers).
Wrong answers come from real mistakes: counting a row twice, comparing the length of rows with different-size
pictures, and adding when the question asks how many more.
"""
import ph_common
from ph_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, peso, words)
import random
import gen_sg_maths_p1_picture_graphs as sgp
adopt(sgp)
if hasattr(sgp, 'R'): sgp.R = random.Random(701150)
import gen_us_math_g1_data as usd
adopt(usd)
if hasattr(usd, 'R'): usd.R = random.Random(701151)
import gen_au_maths_y1_data as aud
adopt(aud)
if hasattr(aud, 'R'): aud.R = random.Random(701152)
ph_common.GRADE = "grade-1"



def build():
    sets, R = build_sets([
        ("Read a pictograph", [("run", sgp.set_count, ("rnd",), 20)]),
        ("Most and fewest", [("run", sgp.set_most, ("rnd",), 20)]),
        ("How many more?", [("run", sgp.set_more, ("rnd",), 20)]),
        ("Pictographs and tables", [("run", usd.set_picture, ("rnd", usd.Picker), 10), ("run", aud.set_tally, ("rnd", aud.Picker), 10)]),
        ("Pictograph questions", [("run", sgp.set_total, ("rnd",), 10), ("run", sgp.set_words, ("rnd",), 10)]),
    ], 70115)
    finish(sets, R)
    body = lesson('<ul><li>Ask a question and write down each answer to <b>collect</b> data (a simple interview).</li><li>In a <b>pictograph</b>, each picture stands for 1.</li><li>Count the pictures in each row. The longest row shows the most.</li><li>A <b>table</b> shows the same data with numbers.</li></ul>',
        [example("Mango 5, Banana 3", ["5 − 3"], "2 more like mango")],
        [['Counting a row twice', 'Point to each picture once.'], ['Comparing lengths only', 'Count the pictures.'], ['Adding for “how many more”', 'Subtract to compare.']])
    faq = [('What does MATATAG Math 1 ask about data?', 'Collect data in one variable through a simple interview, present and interpret data in a pictograph without a scale, and organize the data into a table.'), ('What is a pictograph?', 'A graph that uses pictures to show data.'), ('What does without a scale mean?', 'Each picture stands for 1.'), ('What questions can children ask?', 'What is your favorite fruit? How do you go to school?')]
    make('pictographs', 15, 'Data and Probability', 'Grade 1: Data and Probability',
         'Collect data in one variable through a simple interview; present data in a pictograph without a scale; interpret a pictograph without a scale; organize data in a pictograph without a scale into a table.',
         'Pictographs: Collecting, Showing and Reading Data', 'Pictographs',
         'Free Grade 1 pictograph worksheets for the DepEd MATATAG curriculum: read pictographs, most and fewest, how many more, totals and tables. 100 questions with pictures and answers.',
         'Each picture stands for 1.', 'Subtract to find how many more.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
