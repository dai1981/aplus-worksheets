# -*- coding: utf-8 -*-
"""
South Africa Grade 5 Maths (CAPS): Angles: Acute, Right, Obtuse, Straight, Reflex and Revolution (Grade 5: 3.1 Properties of 2-D shapes)
  python3 tools/gen_za_maths_g5_angles.py
Naming and estimating angles, comparing angles with a right angle, angles in shapes and angles around us (UK Year 5,
Australia Year 5 and Ontario Grade 5 makers).
Wrong answers come from real mistakes: judging an angle by the length of its arms, mixing up obtuse and reflex, and
thinking a straight angle is not an angle.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_uk_maths_y5_angles as uka
adopt(uka)
if isinstance(getattr(uka, 'R', None), random.Random): uka.R = random.Random(805160)
import gen_au_maths_y5_angles as aua
adopt(aua)
if isinstance(getattr(aua, 'R', None), random.Random): aua.R = random.Random(805161)
import gen_caon_math_g5_angles as caa
adopt(caa)
if isinstance(getattr(caa, 'R', None), random.Random): caa.R = random.Random(805162)
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
        ("Name the angle", [("run", uka.set_types, ("rnd", uka.People), 20, six)]),
        ("Angles in pictures", [("run", aua.set_names, ("rnd", aua.People), 20, six)]),
        ("Estimate angles", [("run", uka.set_estimate, ("rnd", uka.People), 10, six), ("run", caa.set_estimate, ("rnd", caa.People), 10, six)]),
        ("Angles in shapes", [("run", uka.set_polygons, ("rnd", uka.People), 20, six)]),
        ("Angles around us", [("run", aua.set_everyday, ("rnd", aua.People), 10, six), ("run", caa.set_real, ("rnd", caa.People), 10, six)]),
    ], 80516)
    finish(sets, R)
    body = lesson('<ul><li>A right angle is a quarter turn (90°).</li><li><b>Acute</b>: smaller than a right angle. <b>Obtuse</b>: bigger than a right angle, smaller than a straight angle.</li><li><b>Straight</b> angle: half a turn (180°). <b>Reflex</b>: bigger than a straight angle. <b>Revolution</b>: a full turn (360°).</li><li>The size of an angle is the amount of turn, not the length of the arms.</li></ul>',
        [example("An angle of 250°", ["more than 180°", "less than 360°"], "a reflex angle")],
        [['Long arms, big angle', 'Look at the turn, not the arms.'], ['Obtuse or reflex?', 'Reflex is more than a straight angle.'], ['A straight line', 'It is a straight angle of 180°.']])
    faq = [('What does CAPS Grade 5 say about angles?', 'Recognise, describe and name angles: acute, right, obtuse, straight, reflex and revolution, and estimate and compare angles with a right angle.'), ('How big is a straight angle?', '180°, half a turn.'), ('What is a revolution?', 'A full turn, 360°.'), ("What angle do the hands make at 3 o'clock?", 'A right angle.')]
    make('angles', 16, 'Space and Shape (Geometry)', 'Grade 5: 3.1 Properties of 2-D shapes',
         'Recognise, describe, name and compare angles in 2-D shapes, including acute, right, obtuse, straight, reflex and revolution; estimate and compare angles with a right angle.',
         'Angles: Acute, Right, Obtuse, Straight, Reflex and Revolution', 'Angles',
         'Free CAPS Grade 5 angles worksheets: acute, right, obtuse, straight, reflex and revolution, estimating and angles in shapes. 100 questions with memos.',
         'Compare every angle with a right angle.', 'Acute < right < obtuse < straight < reflex < revolution.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
