# -*- coding: utf-8 -*-
"""
South Africa Grade 5 Maths (CAPS): Temperature: Reading Thermometers in Degrees Celsius (Grade 5: 4.5 Temperature)
  python3 tools/gen_za_maths_g5_temperature.py
Reading thermometers, likely temperatures, differences and tables of temperatures (makers from the Grade 4
generator with new numbers). Positive temperatures only, as in CAPS Grade 5.
Wrong answers come from real mistakes: reading the wrong interval on a thermometer, subtracting the wrong way, and
choosing a temperature that is too hot or too cold for the situation.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_za_maths_g4_temperature as zt4
adopt(zt4)
if isinstance(getattr(zt4, 'R', None), random.Random): zt4.R = random.Random(805260)
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
        ("Read the thermometer", [("collect", zt4.uniq(zt4.one_read), 20)]),
        ("Likely temperatures", [("collect", zt4.one_sense, 8), ("collect", zt4.uniq(zt4.one_read), 12)]),
        ("Temperature differences", [("collect", zt4.uniq(zt4.one_diff), 20)]),
        ("Temperature tables", [("collect", zt4.uniq(zt4.one_table), 20)]),
        ("Temperature problems", [("collect", zt4.uniq(zt4.one_diff), 20)]),
    ], 80526)
    finish(sets, R)
    body = lesson('<ul><li>Temperature is measured in degrees Celsius (°C) with a thermometer.</li><li>Water freezes at 0 °C and boils at 100 °C. Our body is about 37 °C.</li><li>Find what each mark on the thermometer is worth before you read it.</li><li>To find a difference, subtract the lower temperature from the higher one.</li></ul>',
        [example("Morning 12 °C, afternoon 27 °C", ["27 − 12"], "15 °C warmer")],
        [['The wrong interval', 'Work out each mark first.'], ['Subtracting the wrong way', 'Higher − lower.'], ['Not sensible', 'A hot day is about 30 °C, not 80 °C.']])
    faq = [('What does CAPS Grade 5 say about temperature?', 'Estimate, read and record temperature in degrees Celsius using thermometers (positive values only).'), ('What is room temperature?', 'About 20 °C.'), ('Do we use negative numbers?', 'Not in Grade 5.'), ('Where are thermometers used?', 'In weather reports, kitchens and clinics.')]
    make('temperature', 26, 'Measurement', 'Grade 5: 4.5 Temperature',
         'Measure and record temperature in degrees Celsius (°C) using thermometers; read and compare temperatures (positive values only).',
         'Temperature: Reading Thermometers in Degrees Celsius', 'Temperature',
         'Free CAPS Grade 5 temperature worksheets: reading thermometers, likely temperatures, differences and temperature tables. 100 questions with memos.',
         'Read what each mark on the thermometer is worth.', 'Difference: higher − lower.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
