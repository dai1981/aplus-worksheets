# -*- coding: utf-8 -*-
"""
South Africa Grade 6 Maths (CAPS): Pictographs, Bar Graphs, Pie Charts and Line Graphs (Grade 6: 5.2 Representing data; 5.3 Analysing, interpreting and reporting data)
  python3 tools/gen_za_maths_g6_representing_data.py
Pictographs with keys, bar graphs, pie charts and line graphs, and interpreting graphs (US Grade 3, Australia Year 3
and Year 4, UK Year 4 and Year 6 and BC Grade 6 makers).
Wrong answers come from real mistakes: counting each picture as 1, reading the scale wrongly, and mixing up parts
of a pie chart.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_us_math_g3_picture_bar_graphs as usg
adopt(usg)
if isinstance(getattr(usg, 'R', None), random.Random): usg.R = random.Random(806330)
import gen_au_maths_y3_data as au3
adopt(au3)
if isinstance(getattr(au3, 'R', None), random.Random): au3.R = random.Random(806331)
import gen_uk_maths_y4_statistics as uks
adopt(uks)
if isinstance(getattr(uks, 'R', None), random.Random): uks.R = random.Random(806332)
import gen_uk_maths_y6_pie_line as ukp
adopt(ukp)
if isinstance(getattr(ukp, 'R', None), random.Random): ukp.R = random.Random(806333)
import gen_cabc_math_g6_line_graphs as cbl
adopt(cbl)
if isinstance(getattr(cbl, 'R', None), random.Random): cbl.R = random.Random(806334)
za_common.GRADE = "grade-6"


import re as _re


def _txt(it):
    return _re.sub(r"<[^>]+>", " ", _re.sub(r"<svg.*?</svg>", " ", it["q"], flags=_re.S) + " " + " ".join(it["c"]) + " " + it["e"])


def _nums(it):
    return [int(x.replace(",", "").replace("\u00a0", "")) for x in _re.findall(r"(?<![\d.])\d[\d,\u00a0]*(?![.\d])", _txt(it)) if x.replace(",", "").replace("\u00a0", "").isdigit()]


def noneg(it):
    return not _re.search(r"(?<![\d)] )[−-]\d", _txt(it)) and "negative" not in _txt(it).lower()


def nine(it):
    """whole numbers to 9 digits, no negatives"""
    return all(n <= 999999999 for n in _nums(it)) and noneg(it)


def dec3(it):
    """decimals with at most 3 places, no negatives"""
    return noneg(it) and not _re.search(r"\d\.\d{4}", _txt(it))


def nodec(it):
    return noneg(it) and not _re.search(r"\d\.\d", _txt(it))


def flat(it):
    """first quadrant only: no negative numbers in the text or the picture"""
    return nodec(it) and "−" not in it["q"] and "-1" not in it["q"]


def nomean(it):
    return dec3(it) and not _re.search(r"\bmean\b", _txt(it))


def den12(it):
    ds = [int(d) for d in _re.findall(r"<span class='fd'>(\d+)</span>", it["q"] + " " + it["c"][it["a"]])]
    return all(d <= 12 or d in (20, 25, 50, 100) for d in ds) and nodec(it)



def build():
    sets, R = build_sets([
        ("Pictographs", [("run", usg.set_two_step, ("rnd", usg.Picker), 10, dec3), ("run", au3.set_pictograph, ("rnd", au3.Picker), 10, dec3)]),
        ("Bar graphs", [("run", au3.set_column, ("rnd", au3.Picker), 10, dec3), ("run", uks.set_bar, ("rnd", uks.Picker), 10, dec3)]),
        ("Pie charts", [("run", ukp.set_angles, (), 18, dec3), ("run", ukp.set_problems, (), 2, dec3)]),
        ("Line graphs", [("run", cbl.set_read, (), 5, dec3), ("run", cbl.set_trends, (), 4, dec3), ("run", ukp.set_line, (), 11, dec3)]),
        ("Interpret the graph", [("run", cbl.set_choose, (), 10, dec3), ("run", cbl.set_words, (), 4, dec3), ("run", ukp.set_problems, (), 6, dec3)]),
    ], 80633)
    finish(sets, R)
    body = lesson('<ul><li>In a pictograph, the key tells you what one picture stands for.</li><li>In a bar graph, read the top of each bar against the scale.</li><li>A pie chart shows parts of a whole. A quarter of the circle is a quarter of the data (90°).</li><li>A line graph shows how something changes over time.</li></ul>',
        [example("A pie chart of 60 learners: soccer is half", ["half of 60"], "30 learners")],
        [['Each picture as 1', 'Use the key.'], ['Reading the scale', 'Check what each line is worth.'], ['Parts of a pie', 'The whole circle is all the data.']])
    faq = [('What does CAPS Grade 6 say about graphs?', 'Draw and interpret pictographs, bar graphs and double bar graphs, and read and interpret pie charts and other graphs.'), ('When is a pie chart useful?', 'To show parts of a whole.'), ('When is a line graph useful?', 'To show change over time.'), ('What is a key?', 'It tells you what each picture stands for.')]
    make('pictographs-bar-graphs-and-pie-charts', 33, 'Data Handling', 'Grade 6: 5.2 Representing data; 5.3 Analysing, interpreting and reporting data',
         'Draw a variety of graphs to display and interpret data, including pictographs (many-to-one correspondence), bar graphs and double bar graphs; critically read and interpret data presented in a variety of ways, including pie charts; analyse data by answering questions related to data categories, data sources and contexts.',
         'Pictographs, Bar Graphs, Pie Charts and Line Graphs', 'Representing Data',
         'Free CAPS Grade 6 graphs worksheets: pictographs, bar graphs, pie charts and line graphs. 100 questions with memos.',
         'Use the key and the scale.', 'A pie chart shows parts of a whole.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
