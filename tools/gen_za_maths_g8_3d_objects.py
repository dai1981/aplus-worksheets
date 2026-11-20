# -*- coding: utf-8 -*-
"""
South Africa Grade 8 Maths (CAPS): 3-D Objects: Prisms, Pyramids, Nets and Euler's Formula (Grade 8: 3.4 Geometry of 3D objects)
  python3 tools/gen_za_maths_g8_3d_objects.py
Naming polyhedra, faces, edges and vertices, Euler's formula, nets and cross-sections (Australia Year 6, UK Year 6 and
BC Grade 8 makers).
Wrong answers come from real mistakes: naming a prism after its side faces, counting only visible faces, and choosing
a net with overlapping faces.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_au_maths_y6_prisms as aup
adopt(aup)
if isinstance(getattr(aup, 'R', None), random.Random): aup.R = random.Random(808170)
import gen_uk_maths_y6_circles_nets as ukc
adopt(ukc)
if isinstance(getattr(ukc, 'R', None), random.Random): ukc.R = random.Random(808171)
import gen_cabc_math_g8_views_nets as cbv
adopt(cbv)
if isinstance(getattr(cbv, 'R', None), random.Random): cbv.R = random.Random(808172)
za_common.GRADE = "grade-8"


import re as _re
za_common.GBP_TO_RAND = True


def _txt(it):
    return _re.sub(r"<[^>]+>", " ", _re.sub(r"<svg.*?</svg>", " ", it["q"], flags=_re.S) + " " + " ".join(it["c"]) + " " + it["e"])


def ok8(it):
    """Grade 8: no trigonometry, quadratic formula or surds beyond square roots"""
    return not _re.search(r"\b(sin|cos|tan)\b|quadratic|discriminant|imperial|\bmiles?\b", _txt(it))



def build():
    sets, R = build_sets([
        ("Name the object", [("run", aup.set_name, ("rnd", aup.Pos), 10, ok8), ("run", ukc.set_solids, ("rnd",), 10, ok8)]),
        ("Faces, edges and vertices", [("run", aup.set_fev, ("rnd",), 17, ok8), ("run", cbv.set_count, ("rnd", cbv.People, "seen"), 3, ok8)]),
        ("Nets", [("run", cbv.set_poly_nets, ("rnd",), 10, ok8), ("run", ukc.set_nets, ("rnd", ukc.Pos), 10, ok8)]),
        ("Views", [("run", cbv.set_views, ("rnd", "seen"), 10, ok8), ("run", cbv.set_match, ("rnd", "seen"), 10, ok8)]),
        ("Cross-sections", [("run", aup.set_cut, ("rnd", aup.Pos, aup.People), 10, ok8), ("run", aup.set_which, ("rnd", aup.Pos, aup.People), 10, ok8)]),
    ], 80817)
    finish(sets, R)
    body = lesson("<ul><li>A prism has two identical end faces; a pyramid has one base and an apex.</li><li>Euler's formula for polyhedra: F + V − E = 2.</li><li>A net folds up to make the object.</li><li>A cross-section is the shape you see when you cut straight through an object.</li></ul>",
        [example("An octagonal prism", ["2 octagons + 8 rectangles", "16 vertices"], "F 10, E 24")],
        [['Named after the sides', 'Use the end face or base.'], ['Visible faces only', 'Count hidden faces.'], ['Overlapping net', 'Each face needs its own place.']])
    faq = [('What does CAPS Grade 8 say about 3-D objects?', 'Describe, name and compare the 5 Platonic solids and other polyhedra in terms of faces, vertices and edges, and use nets to build models.'), ('What are the Platonic solids?', 'Tetrahedron, cube, octahedron, dodecahedron and icosahedron.'), ('What is the cross-section of a cylinder cut straight across?', 'A circle.'), ("Does Euler's formula work for a cube?", 'Yes: 6 + 8 − 12 = 2.')]
    make('3d-objects', 17, 'Space and Shape (Geometry)', 'Grade 8: 3.4 Geometry of 3D objects',
         'Describe, sort and compare polyhedra in terms of the shape and number of faces, number of vertices and number of edges; recognise and describe the properties of the 5 Platonic solids; use nets to create models of geometric solids, including cubes, prisms and pyramids.',
         "3-D Objects: Prisms, Pyramids, Nets and Euler's Formula", '3-D Objects',
         "Free CAPS Grade 8 3-D objects worksheets: prisms, pyramids, faces, edges, vertices, Euler's formula, nets and cross-sections. 100 questions with memos.",
         'F + V − E = 2.', 'Prism: end face. Pyramid: base.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
