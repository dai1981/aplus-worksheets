# -*- coding: utf-8 -*-
"""
South Africa Grade 9 Maths (CAPS): 3-D Objects: Views, Plans, Elevations and Nets (Grade 9: 3.4 Geometry of 3D objects)
  python3 tools/gen_za_maths_g9_3d_objects.py
Plans and front and side views of cube stacks, matching views, nets of solids and faces, edges and vertices (UK Year 9,
BC Grade 8 and Australia Year 6 makers).
Wrong answers come from real mistakes: drawing what you know instead of what you see, mixing up the plan and the
elevation, and choosing a net with overlapping faces.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_uk_maths_y9_plans_and_elevations as ukp
adopt(ukp)
if isinstance(getattr(ukp, 'R', None), random.Random): ukp.R = random.Random(809150)
import gen_cabc_math_g8_views_nets as cbv
adopt(cbv)
if isinstance(getattr(cbv, 'R', None), random.Random): cbv.R = random.Random(809151)
import gen_au_maths_y6_prisms as aup
adopt(aup)
if isinstance(getattr(aup, 'R', None), random.Random): aup.R = random.Random(809152)
za_common.GRADE = "grade-9"

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
za_common.GBP_TO_RAND = True


def _txt(it):
    return _re.sub(r"<[^>]+>", " ", _re.sub(r"<svg.*?</svg>", " ", it["q"], flags=_re.S) + " " + " ".join(it["c"]) + " " + it["e"])


def ok9(it):
    """Grade 9: no trigonometry, quadratic formula, simultaneous equations or cones and spheres (Grade 10+)"""
    return not _re.search(r"\b(sin|cos|tan)\b|quadratic formula|discriminant|simultaneous|\bcone|\bsphere|imperial|\bmiles?\b", _txt(it))



def build():
    sets, R = build_sets([
        ("Plans", [("collect", uniq(ukp.one_plan), 20)]),
        ("Front and side elevations", [("collect", uniq(ukp.one_front), 10), ("collect", uniq(ukp.one_side), 10)]),
        ("Match the views", [("run", cbv.set_views, ("rnd", "seen"), 10, ok9), ("collect", uniq(ukp.one_numbered), 10)]),
        ("Nets", [("run", cbv.set_poly_nets, ("rnd",), 10, ok9), ("run", cbv.set_cyl, ("rnd", cbv.People), 10, ok9)]),
        ("Faces, edges and vertices", [("run", aup.set_fev, ("rnd",), 20, ok9)]),
    ], 80915)
    finish(sets, R)
    body = lesson('<ul><li>A <b>plan</b> is the view from above. An <b>elevation</b> is the view from the front or the side.</li><li>Draw only what you can see from that direction.</li><li>A net is a flat pattern that folds into the solid.</li><li>Euler: F + V − E = 2 for polyhedra.</li></ul>',
        [example("A row of stacks 2, 3, 1", ["front elevation shows heights 2, 3, 1"], "plan: 3 squares in a row")],
        [['What you know', 'Draw what you see.'], ['Plan or elevation?', 'The plan is from above.'], ['Overlapping net', 'Each face needs its own place.']])
    faq = [('What does CAPS Grade 9 say about 3-D objects?', 'Describe, name and compare 3-D objects, use nets, and draw and interpret views (plans and elevations) of objects.'), ('What is an elevation?', 'A view from the front or side.'), ('How many faces does a cylinder have?', '2 flat faces and 1 curved surface.'), ('Can two objects have the same plan?', 'Yes.')]
    make('3d-objects-views-and-nets', 15, 'Space and Shape (Geometry)', 'Grade 9: 3.4 Geometry of 3D objects',
         'Revise properties and definitions of the 5 Platonic solids; recognise and describe the properties of spheres and cylinders; use nets to create models of geometric solids; draw and interpret views of 3-D objects from different positions.',
         '3-D Objects: Views, Plans, Elevations and Nets', '3-D Objects',
         'Free CAPS Grade 9 3-D objects worksheets: plans, front and side elevations, nets and faces, edges and vertices. 100 questions with memos.',
         'Plan: from above. Elevation: from the front or side.', 'Draw only what you see.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
