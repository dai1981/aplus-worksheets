# -*- coding: utf-8 -*-
"""
South Africa Grade 6 Maths (CAPS): Temperature: Reading Thermometers and Temperature Differences (Grade 6: 4.5 Temperature)
  python3 tools/gen_za_maths_g6_temperature.py
Reading thermometers, likely temperatures, differences and tables of temperatures (makers from the Grade 4
generator with new numbers). Positive temperatures only.
Wrong answers come from real mistakes: reading the wrong interval on a thermometer, subtracting the wrong way, and
choosing a temperature that is too hot or too cold for the situation.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_za_maths_g4_temperature as zt4
adopt(zt4)
if isinstance(getattr(zt4, 'R', None), random.Random): zt4.R = random.Random(806300)
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
        ("Read the thermometer", [("collect", zt4.uniq(zt4.one_read), 20)]),
        ("Likely temperatures", [("collect", zt4.one_sense, 8), ("collect", zt4.uniq(zt4.one_read), 12)]),
        ("Temperature differences", [("collect", zt4.uniq(zt4.one_diff), 20)]),
        ("Temperature tables", [("collect", zt4.uniq(zt4.one_table), 20)]),
        ("Temperature problems", [("collect", zt4.uniq(zt4.one_diff), 20)]),
    ], 80630)
    finish(sets, R)
    body = lesson('<ul><li>Temperature is measured in degrees Celsius (°C) with a thermometer.</li><li>Water freezes at 0 °C and boils at 100 °C. Our body is about 37 °C.</li><li>Find what each mark on the thermometer is worth before you read it.</li><li>To find a difference, subtract the lower temperature from the higher one.</li></ul>',
        [example("Upington 38 °C, Cape Town 24 °C", ["38 − 24"], "14 °C warmer in Upington")],
        [['The wrong interval', 'Work out each mark first.'], ['Subtracting the wrong way', 'Higher − lower.'], ['Not sensible', 'A cold winter morning is about 5 °C, not 50 °C.']])
    faq = [('What does CAPS Grade 6 say about temperature?', 'Measure, read and record temperature in degrees Celsius using thermometers, and compare temperatures.'), ('What is a normal body temperature?', 'About 37 °C.'), ('What is room temperature?', 'About 20 °C.'), ('Where is temperature used?', 'In weather reports, cooking and clinics.')]
    make('temperature', 30, 'Measurement', 'Grade 6: 4.5 Temperature',
         'Measure and record temperature in degrees Celsius (°C) using thermometers; read and compare temperatures.',
         'Temperature: Reading Thermometers and Temperature Differences', 'Temperature',
         'Free CAPS Grade 6 temperature worksheets: reading thermometers, likely temperatures, differences and temperature tables. 100 questions with memos.',
         'Read what each mark on the thermometer is worth.', 'Difference: higher − lower.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
