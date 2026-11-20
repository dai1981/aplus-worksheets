# -*- coding: utf-8 -*-
"""
South Africa Grade 9 Maths (CAPS): The Theorem of Pythagoras: Solving Problems (Grade 9: 4.3 The theorem of Pythagoras)
  python3 tools/gen_za_maths_g9_pythagoras.py
Finding the hypotenuse and shorter sides, rounding, testing for right angles and problems (Singapore Secondary 2 makers
with new questions).
Wrong answers come from real mistakes: adding the squares for a shorter side, forgetting the square root, and using
the wrong side as the hypotenuse.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_sg_maths_s2_pythagoras_theorem as sgp
adopt(sgp)
if isinstance(getattr(sgp, 'R', None), random.Random): sgp.R = random.Random(809180)
za_common.GRADE = "grade-9"


import re as _re
za_common.GBP_TO_RAND = True


def _txt(it):
    return _re.sub(r"<[^>]+>", " ", _re.sub(r"<svg.*?</svg>", " ", it["q"], flags=_re.S) + " " + " ".join(it["c"]) + " " + it["e"])


def ok9(it):
    """Grade 9: no trigonometry, quadratic formula, simultaneous equations or cones and spheres (Grade 10+)"""
    return not _re.search(r"\b(sin|cos|tan)\b|quadratic formula|discriminant|simultaneous|\bcone|\bsphere|imperial|\bmiles?\b", _txt(it))



def build():
    sets, R = build_sets([
        ("Find the hypotenuse", [("collect", sgp.one_hyp, 20)]),
        ("Round the answer", [("collect", sgp.one_hyp_dp, 20)]),
        ("Find a shorter side", [("collect", sgp.one_short, 20)]),
        ("Is it right-angled?", [("collect", sgp.one_test, 20)]),
        ("Pythagoras problems", [("run", sgp.problems, (), 18, ok9), ("collect", sgp.one_test, 2)]),
    ], 80918)
    finish(sets, R)
    body = lesson('<ul><li>c² = a² + b², where c is the hypotenuse.</li><li>Shorter side: a² = c² − b².</li><li>Take the square root at the end.</li><li>If a² + b² = c², the triangle is right-angled.</li></ul>',
        [example("A 5 m ladder, foot 1,4 m from the wall", ["h² = 25 − 1,96"], "h = 4,8 m")],
        [['Adding for a short side', 'Subtract.'], ['No square root', 'c² = 169 means c = 13.'], ['The wrong hypotenuse', 'c is opposite the right angle.']])
    faq = [('What does CAPS Grade 9 say about Pythagoras?', 'Use the theorem of Pythagoras to solve problems involving unknown lengths in geometric figures that contain right-angled triangles.'), ('Is 8, 15, 17 right-angled?', 'Yes: 64 + 225 = 289.'), ('Can I use it in 3-D?', 'Yes, with right-angled triangles inside the object.'), ('What is a surd?', 'An answer like √20 left as a root.')]
    make('theorem-of-pythagoras', 18, 'Measurement', 'Grade 9: 4.3 The theorem of Pythagoras',
         'Solve problems using the Theorem of Pythagoras to calculate a missing length in a right-angled triangle, leaving irrational answers in surd form; use the theorem to solve problems involving unknown lengths in geometric figures that contain right-angled triangles.',
         'The Theorem of Pythagoras: Solving Problems', 'Theorem of Pythagoras',
         'Free CAPS Grade 9 Pythagoras worksheets: the hypotenuse, shorter sides, right-angle tests and problems. 100 questions with memos.',
         'c² = a² + b².', 'Square root at the end.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
