# -*- coding: utf-8 -*-
"""
South Africa Grade 7 Maths (CAPS): 3-D Objects: Polyhedra, Faces, Edges, Vertices and Nets (Grade 7: 3.3 Geometry of 3D objects)
  python3 tools/gen_za_maths_g7_3d_objects.py
Naming prisms and pyramids, faces, edges and vertices, nets of cubes and other solids (Australia Year 5 and Year 6,
UK Year 6, BC Grade 8 and US Grade 6 makers).
Wrong answers come from real mistakes: naming a prism after its side faces, counting only the visible faces, and
choosing a net with overlapping faces.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_au_maths_y6_prisms as aup
adopt(aup)
if isinstance(getattr(aup, 'R', None), random.Random): aup.R = random.Random(807200)
import gen_au_maths_y5_nets as aun
adopt(aun)
if isinstance(getattr(aun, 'R', None), random.Random): aun.R = random.Random(807201)
import gen_uk_maths_y6_circles_nets as ukc
adopt(ukc)
if isinstance(getattr(ukc, 'R', None), random.Random): ukc.R = random.Random(807202)
import gen_cabc_math_g8_views_nets as cbv
adopt(cbv)
if isinstance(getattr(cbv, 'R', None), random.Random): cbv.R = random.Random(807203)
import gen_us_math_g6_surface_area as uss
adopt(uss)
if isinstance(getattr(uss, 'R', None), random.Random): uss.R = random.Random(807204)
za_common.GRADE = "grade-7"


import re as _re
za_common.GBP_TO_RAND = True


def _txt(it):
    return _re.sub(r"<[^>]+>", " ", _re.sub(r"<svg.*?</svg>", " ", it["q"], flags=_re.S) + " " + " ".join(it["c"]) + " " + it["e"])


def ok7(it):
    """Grade 7: no circles, pi or standard form (they come in Grade 8 and 9)"""
    return not _re.search(r"π|\bpi\b|circumference|radius|diameter|×\s?10<sup>|standard form|scientific notation", _txt(it))


def noneg(it):
    return ok7(it) and not _re.search(r"(?<![\d)] )[−-]\d", _txt(it))



def build():
    sets, R = build_sets([
        ("Name the polyhedron", [("run", aup.set_name, ("rnd", aup.Pos), 10, ok7), ("run", uss.set_identify, ("rnd",), 10, ok7)]),
        ("Faces, edges and vertices", [("run", aup.set_fev, ("rnd",), 10, ok7), ("run", aun.set_fev, ("rnd",), 10, ok7)]),
        ("Nets of cubes", [("run", aun.set_cube_nets, ("rnd",), 20, ok7)]),
        ("Nets of other solids", [("run", cbv.set_poly_nets, ("rnd",), 10, ok7), ("run", ukc.set_nets, ("rnd", ukc.Pos), 10, ok7)]),
        ("Objects around us", [("run", aup.set_real, ("rnd", aup.People), 10, ok7), ("run", aun.set_folding, ("rnd",), 10, ok7)]),
    ], 80720)
    finish(sets, R)
    body = lesson('<ul><li>A <b>polyhedron</b> is a 3-D object with flat faces: prisms and pyramids are polyhedra.</li><li>A prism is named after its end face; a pyramid after its base.</li><li>Euler: faces + vertices − edges = 2. A cube: 6 + 8 − 12 = 2.</li><li>A net folds up to make the object; a cube has 11 different nets.</li></ul>',
        [example("A pentagonal pyramid", ["1 pentagon + 5 triangles", "6 vertices, 10 edges"], "6 faces")],
        [['Named after the sides', 'Use the end face or base.'], ['Visible faces only', 'Count the hidden faces.'], ['Overlapping net', 'Each face needs its own place.']])
    faq = [('What does CAPS Grade 7 say about 3-D objects?', 'Describe, sort and compare polyhedra in terms of the shape and number of faces, vertices and edges, and use nets to make models.'), ('Is a cone a polyhedron?', 'No, it has a curved surface.'), ('How many edges does a triangular prism have?', '9.'), ('What is a regular polyhedron?', 'One with identical regular faces, like a cube.')]
    make('3d-objects', 20, 'Space and Shape (Geometry)', 'Grade 7: 3.3 Geometry of 3D objects',
         'Describe, sort and compare polyhedra in terms of the shape and number of faces, number of vertices and number of edges; revise properties and definitions of the five Platonic solids; use nets to create models of geometric solids, including cubes and prisms.',
         '3-D Objects: Polyhedra, Faces, Edges, Vertices and Nets', '3-D Objects',
         "Free CAPS Grade 7 3-D objects worksheets: polyhedra, faces, edges and vertices, Euler's formula and nets. 100 questions with memos.",
         'Faces + vertices − edges = 2.', 'Prism: end face. Pyramid: base.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
