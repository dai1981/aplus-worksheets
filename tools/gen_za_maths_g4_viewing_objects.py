# -*- coding: utf-8 -*-
"""
South Africa Grade 4 Maths (CAPS): Viewing Objects from the Front, Side and Top (Grade 4: 3.5 Viewing of objects)
  python3 tools/gen_za_maths_g4_viewing_objects.py
Matching views of objects built from cubes: the view from the top, the front and the side (UK Year 9 makers), and
which object gives a view (BC Grade 8 makers).
Wrong answers come from real mistakes: mixing up the front and side views, counting hidden cubes in a view, and
forgetting that a view shows only one face.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_uk_maths_y9_plans_and_elevations as ukp
adopt(ukp)
if hasattr(ukp, 'R'): ukp.R = random.Random(804190)
import gen_cabc_math_g8_views_nets as cbv
adopt(cbv)
if hasattr(cbv, 'R'): cbv.R = random.Random(804191)
za_common.GRADE = "grade-4"



def build():
    sets, R = build_sets([
        ("View from the top", [("collect", ukp.one_plan, 20)]),
        ("View from the front", [("collect", ukp.one_front, 20)]),
        ("View from the side", [("collect", ukp.one_side, 20)]),
        ("Match the views", [("run", cbv.set_views, ("rnd", "seen"), 20)]),
        ("Which object is it?", [("run", cbv.set_match, ("rnd", "seen"), 20)]),
    ], 80419)
    finish(sets, R)
    body = lesson('<ul><li>An object looks different from different places.</li><li>The <b>top view</b> is what you see looking down from above.</li><li>The <b>front view</b> and <b>side view</b> are what you see from the front and from the side.</li><li>A view shows only what is facing you: cubes behind others are hidden.</li></ul>',
        [example("A row of 3 cubes with 1 cube on top of the left cube", ["front: 3 squares with 1 on the left above"], "an L shape")],
        [['Front or side?', 'Check where the person is standing.'], ['Hidden cubes', 'A view shows only what you can see.'], ['Two faces at once', 'A view shows one direction.']])
    faq = [('What does CAPS Grade 4 say about viewing objects?', 'Match different views of the same everyday objects, and identify everyday objects from different views.'), ('What is a plan?', 'Another name for the top view.'), ('Why learn views?', 'Maps, building plans and drawings use views.'), ('Can two objects have the same front view?', 'Yes, so we need more than one view.')]
    make('viewing-objects', 19, 'Space and Shape (Geometry)', 'Grade 4: 3.5 Viewing of objects',
         'Match different views of the same everyday objects; identify everyday objects from different views.',
         'Viewing Objects from the Front, Side and Top', 'Viewing Objects',
         'Free CAPS Grade 4 viewing objects worksheets: top, front and side views of objects made of cubes, matching views and objects. 100 questions with memos.',
         'Top view: looking down. Front view: looking from the front.', 'A view shows only what you can see.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
