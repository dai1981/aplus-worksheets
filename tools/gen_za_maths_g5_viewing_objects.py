# -*- coding: utf-8 -*-
"""
South Africa Grade 5 Maths (CAPS): Viewing Objects: Views from the Front, Side and Top (Grade 5: 3.5 Viewing of objects)
  python3 tools/gen_za_maths_g5_viewing_objects.py
Views of objects from the front, the side and the top, matching views to stacks of cubes, and counting cubes (UK
Year 9 plan and elevation makers for cube stacks, and BC Grade 8 makers, with new questions).
Wrong answers come from real mistakes: drawing what you know instead of what you see, mixing up the side and the top,
and forgetting hidden cubes.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_uk_maths_y9_plans_and_elevations as ukp
adopt(ukp)
if isinstance(getattr(ukp, 'R', None), random.Random): ukp.R = random.Random(805200)
import gen_cabc_math_g8_views_nets as cbv
adopt(cbv)
if isinstance(getattr(cbv, 'R', None), random.Random): cbv.R = random.Random(805201)
za_common.GRADE = "grade-5"

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
        ("View from the top", [("collect", uniq(ukp.one_plan), 20)]),
        ("View from the front", [("collect", uniq(ukp.one_front), 20)]),
        ("View from the side", [("collect", uniq(ukp.one_side), 20)]),
        ("Match the views", [("run", cbv.set_views, ("rnd", "seen"), 10, nodec), ("run", cbv.set_match, ("rnd", "seen"), 10, nodec)]),
        ("Count the cubes", [("run", cbv.set_count, ("rnd", cbv.People, "seen"), 20, nodec)]),
    ], 80520)
    finish(sets, R)
    body = lesson('<ul><li>Objects look different from different positions.</li><li>The view from the <b>top</b> shows the squares you see looking down.</li><li>The view from the <b>front</b> shows the tallest stack in each column.</li><li>Some cubes can be hidden behind others.</li></ul>',
        [example("Stacks of 3, 1 and 2 cubes in a row", ["front view: columns 3, 1, 2"], "top view: 3 squares in a row")],
        [['What you know', 'Draw only what you see.'], ['Side or top?', 'The top view looks down.'], ['Hidden cubes', 'Count the cubes underneath.']])
    faq = [('What does CAPS Grade 5 say about viewing objects?', 'Recognise and match different views of the same everyday objects, and identify everyday objects from different positions.'), ('Why do views look different?', 'You see different faces from each position.'), ('Can two stacks have the same top view?', 'Yes, the top view does not show the height.'), ('Where is this useful?', 'In building, maps and drawing plans.')]
    make('viewing-objects', 20, 'Space and Shape (Geometry)', 'Grade 5: 3.5 Viewing of objects',
         'Recognise and match different views of the same everyday objects; identify everyday objects from different positions.',
         'Viewing Objects: Views from the Front, Side and Top', 'Viewing Objects',
         'Free CAPS Grade 5 viewing objects worksheets: views from the front, side and top, matching views and counting cubes. 100 questions with memos.',
         'Draw only what you can see from that position.', 'The top view does not show the height.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
