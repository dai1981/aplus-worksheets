# -*- coding: utf-8 -*-
"""
South Africa Grade 5 Maths (CAPS): Collecting and Organising Data: Tallies, Frequency Tables and the Mode (Grade 5: 5.1 Collecting and organising data)
  python3 tools/gen_za_maths_g5_collecting_data.py
Tally marks, frequency tables, organising and comparing data, and the mode of ungrouped data (UK Year 4 and Year 5,
Australia Year 4 and Year 5 makers).
Wrong answers come from real mistakes: counting a tally group as 4, giving the largest number instead of the most
common one as the mode, and reading the wrong row of a table.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_uk_maths_y4_statistics as uks
adopt(uks)
if isinstance(getattr(uks, 'R', None), random.Random): uks.R = random.Random(805280)
import gen_uk_maths_y5_line_graphs_tables as ukt
adopt(ukt)
if isinstance(getattr(ukt, 'R', None), random.Random): ukt.R = random.Random(805281)
import gen_au_maths_y4_data as aud
adopt(aud)
if isinstance(getattr(aud, 'R', None), random.Random): aud.R = random.Random(805282)
import gen_au_maths_y5_line_graphs as aul
adopt(aul)
if isinstance(getattr(aul, 'R', None), random.Random): aul.R = random.Random(805283)
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
        ("Tally tables", [("run", uks.set_tally_table, ("rnd",), 20, nodec)]),
        ("Frequency tables", [("run", ukt.set_tables, (), 15, nodec), ("run", aud.set_tally, ("rnd",), 5, nodec)]),
        ("Compare the data", [("run", aud.set_compare, ("rnd",), 20, nodec)]),
        ("The mode", [("run", aul.set_mode, (), 20, nodec)]),
        ("Data questions", [("run", aud.set_words, ("rnd",), 10, nodec), ("run", aul.set_words, (), 10, nodec)]),
    ], 80528)
    finish(sets, R)
    body = lesson('<ul><li>Collect data by asking a question and recording each answer with tally marks.</li><li>A tally group of 5 is 4 lines crossed by a fifth line.</li><li>A frequency table shows how many times each answer appears.</li><li>The <b>mode</b> is the answer that appears most often.</li></ul>',
        [example("Shoe sizes: 4, 5, 5, 6, 5, 4, 7", ["5 appears 3 times"], "the mode is 5")],
        [['A group of 4', 'A tally group is 5.'], ['The biggest number', 'The mode is the most common.'], ['The wrong row', 'Use a ruler to follow the row.']])
    faq = [('What does CAPS Grade 5 say about collecting data?', 'Collect data using tally marks and tables, order data, and summarise data using the mode.'), ('Can there be two modes?', 'Yes, if two values appear equally most often.'), ('What is a frequency?', 'How many times something happens.'), ('Why organise data?', 'It is easier to read and compare.')]
    make('collecting-and-organising-data', 28, 'Data Handling', 'Grade 5: 5.1 Collecting and organising data',
         'Collect data on everyday things using tally marks and tables for recording; order data from smallest group to largest group; summarise and interpret data using the mode.',
         'Collecting and Organising Data: Tallies, Frequency Tables and the Mode', 'Collecting and Organising Data',
         'Free CAPS Grade 5 data handling worksheets: tally marks, frequency tables, comparing data and the mode. 100 questions with memos.',
         'The mode is the most common value.', 'A tally group is 5.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
