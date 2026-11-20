# -*- coding: utf-8 -*-
"""
South Africa Grade 6 Maths (CAPS): Collecting and Organising Data: Tables, Mode and Median (Grade 6: 5.1 Collecting and organising data)
  python3 tools/gen_za_maths_g6_collecting_data.py
Kinds of data, frequency tables, the mode, the median and the range, and comparing data (Australia Year 6 and Ontario
Grade 6 makers).
Wrong answers come from real mistakes: finding the median without ordering the data, giving the largest value as
the mode, and reading the wrong row of a table.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_au_maths_y6_data as aud
adopt(aud)
if isinstance(getattr(aud, 'R', None), random.Random): aud.R = random.Random(806320)
import gen_caon_math_g6_data as cad
adopt(cad)
if isinstance(getattr(cad, 'R', None), random.Random): cad.R = random.Random(806321)
za_common.GRADE = "grade-6"

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


CTX = [("goals scored in netball matches", ""), ("learners' marks out of 20", ""), ("books read by learners this term", ""), ("ages of the players in a soccer team", " years"), ("rainfall amounts on school days", " mm"), ("pumpkins sold each day at a farm stall", "")]


def one_mmr(r):
    what, u = r.choice(CTX)
    n = r.choice([5, 7, 9, 6, 8])
    lo = r.randint(1, 12)
    data = [r.randint(lo, lo + 14) for _ in range(n)]
    m = r.choice(data)
    data[r.randrange(n)] = m
    srt = sorted(data)
    counts = {x: data.count(x) for x in data}
    top = max(counts.values())
    modes = [x for x in counts if counts[x] == top]
    k = r.choice(["median", "mode", "range"])
    if k == "median":
        if n % 2 == 0:
            a, b = srt[n // 2 - 1], srt[n // 2]
            if (a + b) % 2:
                raise AssertionError
            med = (a + b) // 2
        else:
            med = srt[n // 2]
        right = str(med)
        wr = [str(data[n // 2]) if data[n // 2] != med else str(med + 1), str(max(data) - min(data)), str(modes[0]) if modes[0] != med else str(med + 2)]
        e = "In order: %s. The middle value is <b>%d</b>." % (", ".join(map(str, srt)), med)
    elif k == "mode":
        if top == 1 or len(modes) > 1:
            raise AssertionError
        right = str(modes[0])
        wr = [str(max(data)), str(srt[n // 2]) if srt[n // 2] != modes[0] else str(modes[0] + 1), str(top)]
        e = "%d appears %d times, more than any other value. Mode: <b>%d</b>." % (modes[0], top, modes[0])
    else:
        rg = max(data) - min(data)
        right = str(rg)
        wr = [str(max(data)), str(max(data) + min(data)), str(rg + 1)]
        e = "Range = %d − %d = <b>%d</b>." % (max(data), min(data), rg)
    wr = [w for w in dict.fromkeys(wr) if w != right]
    if len(wr) < 3:
        wr.append(str(int(right) + 3))
    q = "Here are the %s: %s. What is the <b>%s</b>?" % (what, ", ".join(str(x) + u for x in data), k)
    return mcq(q, right + u, [w + u for w in wr[:3]], e)


def build():
    sets, R = build_sets([
        ("Kinds of data", [("run", aud.set_kinds, (), 10, nomean), ("run", cad.set_kinds, (), 10, nomean)]),
        ("Read the table", [("run", aud.set_read, (), 12, nomean), ("run", cad.set_read, (), 8, nomean)]),
        ("Mode and range", [("run", aud.set_mode_range, (), 17, nomean), ("collect", uniq(one_mmr), 3)]),
        ("Mode, median and range", [("run", cad.set_mmmr, (), 7, lambda it: dec3(it) and "mean" not in _txt(it).lower()), ("collect", uniq(one_mmr), 13)]),
        ("Compare the data", [("run", aud.set_compare, (), 7, nomean), ("run", cad.set_compare, (), 9, nomean), ("run", cad.set_claims, (), 4, nomean)]),
    ], 80632)
    finish(sets, R)
    body = lesson('<ul><li>Collect data with a questionnaire, tally marks or a table.</li><li>The <b>mode</b> is the value that appears most often.</li><li>The <b>median</b> is the middle value when the data is in order.</li><li>The <b>range</b> is the biggest value − the smallest value.</li></ul>',
        [example("Scores: 7, 3, 9, 7, 5", ["in order: 3, 5, 7, 7, 9"], "mode 7, median 7, range 6")],
        [['Median without ordering', 'Put the data in order first.'], ['The biggest value', 'The mode is the most common.'], ['The wrong row', 'Use a ruler to follow the row.']])
    faq = [('What does CAPS Grade 6 say about data?', 'Collect and organise data using tally marks, tables and stem-and-leaf displays, and summarise data using the mode and the median.'), ('What if there are two middle values?', 'The median is halfway between them.'), ('Can there be no mode?', 'Yes, if no value repeats.'), ('What is a frequency table?', 'A table of each value and how often it appears.')]
    make('collecting-and-organising-data', 32, 'Data Handling', 'Grade 6: 5.1 Collecting and organising data',
         'Collect data using questionnaires (yes/no type questions and multiple-choice questions); organise data using tally marks, tables and stem-and-leaf displays; group data in intervals; summarise and distinguish between ungrouped numerical data by determining the mode and the median.',
         'Collecting and Organising Data: Tables, Mode and Median', 'Collecting and Organising Data',
         'Free CAPS Grade 6 data handling worksheets: kinds of data, frequency tables, mode, median and range. 100 questions with memos.',
         'Mode: most often. Median: middle when in order.', 'Order the data first.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
