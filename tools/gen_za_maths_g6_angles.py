# -*- coding: utf-8 -*-
"""
South Africa Grade 6 Maths (CAPS): Angles: Naming, Estimating and Measuring with a Protractor (Grade 6: 3.1 Properties of 2-D shapes)
  python3 tools/gen_za_maths_g6_angles.py
Naming angles, estimating, measuring with a protractor, reflex angles and angles around us (BC Grade 6 and Ontario
Grade 6 makers).
Wrong answers come from real mistakes: reading the wrong scale on the protractor, judging an angle by its arm length,
and mixing up obtuse and reflex angles.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_cabc_math_g6_angles as cba
adopt(cba)
if isinstance(getattr(cba, 'R', None), random.Random): cba.R = random.Random(806210)
import gen_caon_math_g6_angles as caa
adopt(caa)
if isinstance(getattr(caa, 'R', None), random.Random): caa.R = random.Random(806211)
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
        ("Name the angle", [("run", cba.set_classify, ("rnd", cba.People), 10, nodec), ("run", caa.set_names, ("rnd", caa.People), 10, nodec)]),
        ("Estimate angles", [("run", cba.set_estimate, ("rnd", cba.People), 20, nodec)]),
        ("Measure with a protractor", [("run", cba.set_protractor, ("rnd", cba.People), 10, nodec), ("run", caa.set_protractor, ("rnd", caa.People), 10, nodec)]),
        ("Reflex angles and turns", [("run", caa.set_reflex, ("rnd", caa.People), 10, nodec), ("run", caa.set_turns, ("rnd", caa.People), 10, nodec)]),
        ("Angles around us", [("run", cba.set_real, ("rnd", cba.People), 10, nodec), ("run", caa.set_real, ("rnd", caa.People), 10, nodec)]),
    ], 80621)
    finish(sets, R)
    body = lesson('<ul><li>Acute: less than 90°. Right: 90°. Obtuse: between 90° and 180°. Straight: 180°. Reflex: between 180° and 360°. Revolution: 360°.</li><li>To measure, put the centre of the protractor on the vertex and the 0° line on one arm.</li><li>Read the scale that starts at 0° on that arm.</li><li>Estimate first, so you choose the right scale.</li></ul>',
        [example("An angle a bit bigger than a right angle", ["obtuse", "about 100°"], "the protractor shows 105°")],
        [['The wrong scale', 'Start from 0° on one arm.'], ['Arm length', 'Long arms do not make a big angle.'], ['Obtuse or reflex?', 'Reflex is more than 180°.']])
    faq = [('What does CAPS Grade 6 say about angles?', 'Recognise, describe, classify and measure angles, including acute, right, obtuse, straight, reflex and revolution, using a protractor.'), ('How do I measure a reflex angle?', 'Measure the small angle and take it away from 360°.'), ('What is a right angle?', '90°, a quarter turn.'), ('Why estimate first?', 'To read the correct scale.')]
    make('angles', 21, 'Space and Shape (Geometry)', 'Grade 6: 3.1 Properties of 2-D shapes',
         'Recognise, describe, classify, estimate and measure angles in degrees using a protractor: acute, right, obtuse, straight, reflex and revolution.',
         'Angles: Naming, Estimating and Measuring with a Protractor', 'Angles',
         'Free CAPS Grade 6 angles worksheets: naming angles, estimating, measuring with a protractor and reflex angles. 100 questions with memos.',
         'Centre on the vertex, 0° on one arm.', 'Estimate first, then read the right scale.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
