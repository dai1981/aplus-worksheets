# -*- coding: utf-8 -*-
"""
South Africa Grade 5 Maths (CAPS): Pictographs, Bar Graphs, Double Bar Graphs and Pie Charts (Grade 5: 5.2 Representing data; 5.3 Analysing, interpreting and reporting data)
  python3 tools/gen_za_maths_g5_representing_data.py
Pictographs with many-to-one keys, bar graphs, double bar graphs, pie charts and interpreting graphs (US Grade 3,
Australia Year 4, BC Grade 5 and UK Year 6 makers).
Wrong answers come from real mistakes: counting each picture as 1, reading the scale wrongly, and comparing the wrong
bars.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_us_math_g3_picture_bar_graphs as usg
adopt(usg)
if isinstance(getattr(usg, 'R', None), random.Random): usg.R = random.Random(805290)
import gen_au_maths_y4_data as aud
adopt(aud)
if isinstance(getattr(aud, 'R', None), random.Random): aud.R = random.Random(805291)
import gen_cabc_math_g5_double_bar_graphs as cbd
adopt(cbd)
if isinstance(getattr(cbd, 'R', None), random.Random): cbd.R = random.Random(805292)
import gen_uk_maths_y6_pie_line as ukp
adopt(ukp)
if isinstance(getattr(ukp, 'R', None), random.Random): ukp.R = random.Random(805293)
za_common.GRADE = "grade-5"


import re as _re


def _txt(it):
    return _re.sub(r"<[^>]+>", " ", _re.sub(r"<svg.*?</svg>", " ", it["q"], flags=_re.S) + " " + " ".join(it["c"]) + " " + it["e"])


def _nums(it):
    return [int(x.replace(",", "").replace("\u00a0", "")) for x in _re.findall(r"(?<![\d.])\d[\d,\u00a0]*(?![.\d])", _txt(it)) if x.replace(",", "").replace("\u00a0", "").isdigit()]


def six(it):
    """whole numbers to 6 digits, no decimals, no negatives"""
    t = _txt(it)
    return all(n <= 999999 for n in _nums(it)) and not _re.search(r"\d\.\d|−\d", t)


def nodec(it):
    return not _re.search(r"\d\.\d|−\d", _txt(it))


def den12(it):
    ds = [int(d) for d in _re.findall(r"<span class='fd'>(\d+)</span>", it["q"] + " " + it["c"][it["a"]])]
    return all(d <= 12 for d in ds) and nodec(it)



def build():
    sets, R = build_sets([
        ("Pictographs", [("run", usg.set_picture, ("rnd", usg.Picker), 20, nodec)]),
        ("Bar graphs", [("run", usg.set_bar, ("rnd", usg.Picker), 10, nodec), ("run", aud.set_column, ("rnd", aud.Picker), 10, nodec)]),
        ("Double bar graphs", [("run", cbd.set_read, (), 10, nodec), ("run", cbd.set_compare, (), 10, nodec)]),
        ("Pie charts", [("run", ukp.set_amounts, (), 15, nodec), ("run", ukp.set_problems, (), 5, nodec)]),
        ("Interpret the graph", [("run", cbd.set_concl, (), 5, nodec), ("run", cbd.set_make, (), 5, nodec), ("run", cbd.set_scale, (), 10, nodec)]),
    ], 80529)
    finish(sets, R)
    body = lesson('<ul><li>In a pictograph, the key tells you what one picture stands for: one picture = 5 learners.</li><li>In a bar graph, read the top of each bar against the scale.</li><li>A double bar graph compares two sets of data side by side.</li><li>A pie chart shows parts of a whole: half the circle is half the data.</li></ul>',
        [example("Key: 1 picture = 4 learners. 6 pictures", ["6 × 4"], "24 learners")],
        [['Each picture as 1', 'Use the key.'], ['Reading the scale', 'Check what each line on the scale is worth.'], ['The wrong bars', 'Use the legend to find each set.']])
    faq = [('What does CAPS Grade 5 say about representing data?', 'Draw a variety of graphs to display and interpret data, including pictographs with many-to-one correspondence, bar graphs and double bar graphs, and read and interpret pie charts.'), ('What is a key?', 'It tells you what each picture stands for.'), ('What does a double bar graph show?', 'Two sets of data for each category.'), ('When is a pie chart useful?', 'To show parts of a whole.')]
    make('pictographs-bar-graphs-and-pie-charts', 29, 'Data Handling', 'Grade 5: 5.2 Representing data; 5.3 Analysing, interpreting and reporting data',
         'Draw a variety of graphs to display and interpret data, including pictographs (many-to-one correspondence), bar graphs and double bar graphs; read and interpret data presented in a variety of ways, including pie charts; analyse data by answering questions related to data categories and data sources.',
         'Pictographs, Bar Graphs, Double Bar Graphs and Pie Charts', 'Representing Data',
         'Free CAPS Grade 5 graphs worksheets: pictographs with keys, bar graphs, double bar graphs and pie charts. 100 questions with memos.',
         'Use the key and the scale.', 'A pie chart shows parts of a whole.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
