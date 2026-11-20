# -*- coding: utf-8 -*-
"""
South Africa Grade 4 Maths (CAPS): Collecting and Organising Data: Tally Marks and Tables (Grade 4: 5.1 Collecting and organising data)
  python3 tools/gen_za_maths_g4_collecting_data.py
Tally marks, tally tables and frequency tables, organising data, and comparing data in tables (Australia Year 4, UK
Year 4 and Australia Year 3 makers with South African names).
Wrong answers come from real mistakes: reading a gate of five tally marks as four, counting a value twice, and
adding when the question asks how many more.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_au_maths_y4_data as aud
adopt(aud)
if hasattr(aud, 'R'): aud.R = random.Random(804270)
import gen_uk_maths_y4_statistics as uks
adopt(uks)
if hasattr(uks, 'R'): uks.R = random.Random(804271)
import gen_au_maths_y3_data as au3
adopt(au3)
if hasattr(au3, 'R'): au3.R = random.Random(804272)
za_common.GRADE = "grade-4"



def build():
    sets, R = build_sets([
        ("Tally marks", [("run", aud.set_tally, ("rnd",), 12), ("run", au3.set_compare, ("rnd",), 8)]),
        ("Tally tables", [("run", uks.set_tally_table, ("rnd",), 20)]),
        ("Organise the data", [("run", au3.set_tally, ("rnd",), 12), ("run", uks.set_words, (), 8)]),
        ("Compare the data", [("run", aud.set_compare, ("rnd",), 20)]),
        ("Data questions", [("run", aud.set_words, ("rnd",), 10), ("run", au3.set_words, ("rnd",), 10)]),
    ], 80427)
    finish(sets, R)
    body = lesson('<ul><li>To collect data, ask a question and record each answer.</li><li>Use <b>tally marks</b>: draw 4 lines and cross them with the 5th to make a group of 5.</li><li>Count the tallies in groups of 5 and write the total in a table.</li><li>Organise data in a table so it is easy to compare.</li></ul>',
        [example("Tally: two gates and 3 more", ["5 + 5 + 3"], "13")],
        [['A gate as 4', 'A gate (4 lines crossed) is 5.'], ['Counting twice', 'Cross out each answer as you tally it.'], ['Adding for how many more', 'Subtract to compare.']])
    faq = [('What does CAPS Grade 4 say about collecting data?', 'Collect data using tally marks and tables for recording, and order data from smallest group to largest group.'), ('Why group tally marks in fives?', 'Groups of 5 are quick to count.'), ('What is a frequency table?', 'A table showing how often each answer occurs.'), ('What makes a good survey question?', 'A clear question with clear answer choices.')]
    make('collecting-and-organising-data', 27, 'Data Handling', 'Grade 4: 5.1 Collecting and organising data',
         'Collect data using tally marks and tables for recording; order data from smallest group to largest group; sort, group and organise data in tables.',
         'Collecting and Organising Data: Tally Marks and Tables', 'Collecting and Organising Data',
         'Free CAPS Grade 4 data handling worksheets: tally marks, tally tables, organising and comparing data. 100 questions with memos.',
         'A gate of tally marks is 5.', 'Organise data in a table to compare.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
