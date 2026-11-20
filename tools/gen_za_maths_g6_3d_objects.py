# -*- coding: utf-8 -*-
"""
South Africa Grade 6 Maths (CAPS): 3-D Objects: Prisms, Pyramids, Cylinders and Nets (Grade 6: 3.2 Properties of 3-D objects)
  python3 tools/gen_za_maths_g6_3d_objects.py
Naming prisms and pyramids, faces, edges and vertices, cross-sections, solids and nets (Australia Year 6 and UK
Year 6 makers).
Wrong answers come from real mistakes: naming a prism after its side faces, counting only the visible faces, and
choosing a net with two faces on top of each other.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_au_maths_y6_prisms as aup
adopt(aup)
if isinstance(getattr(aup, 'R', None), random.Random): aup.R = random.Random(806220)
import gen_uk_maths_y6_circles_nets as ukc
adopt(ukc)
if isinstance(getattr(ukc, 'R', None), random.Random): ukc.R = random.Random(806221)
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
        ("Name the object", [("run", aup.set_name, ("rnd", aup.Pos), 20, nodec)]),
        ("Which object?", [("run", aup.set_which, ("rnd", aup.Pos, aup.People), 10, nodec), ("run", ukc.set_solids, ("rnd",), 10, nodec)]),
        ("Faces, edges and vertices", [("run", aup.set_fev, ("rnd",), 15, nodec), ("run", ukc.set_solids, ("rnd",), 5, nodec)]),
        ("Nets", [("run", ukc.set_nets, ("rnd", ukc.Pos), 20, nodec)]),
        ("Cross-sections and objects around us", [("run", aup.set_cut, ("rnd", aup.Pos, aup.People), 10, nodec), ("run", aup.set_real, ("rnd", aup.People), 10, nodec)]),
    ], 80622)
    finish(sets, R)
    body = lesson('<ul><li>A <b>prism</b> has two identical end faces joined by rectangles; it is named after its end face.</li><li>A <b>pyramid</b> has one base and triangles that meet at the apex; it is named after its base.</li><li>Faces are flat surfaces, edges are where faces meet, vertices are corners.</li><li>A <b>net</b> folds up to make the object.</li></ul>',
        [example("Hexagonal prism", ["2 hexagons + 6 rectangles", "18 edges, 12 vertices"], "8 faces")],
        [['Named after the sides', 'Use the end face or the base.'], ['Visible faces only', 'Count the hidden faces.'], ['Overlapping net', 'Each face needs its own place.']])
    faq = [('What does CAPS Grade 6 say about 3-D objects?', 'Recognise, visualise and name prisms, pyramids, cylinders, cones and spheres, describe their faces, edges and vertices, and make models from nets.'), ('How many faces does a triangular prism have?', '5.'), ('Is a cylinder a prism?', 'No, it has a curved surface.'), ('What is a cross-section?', 'The shape you see when you cut through an object.')]
    make('3d-objects', 22, 'Space and Shape (Geometry)', 'Grade 6: 3.2 Properties of 3-D objects',
         'Recognise, visualise and name 3-D objects in the environment and geometric settings, focusing on rectangular prisms, cubes, tetrahedrons, other pyramids, cylinders, cones and spheres; describe, sort and compare 3-D objects in terms of the number and shape of faces, the number of vertices and the number of edges; make 3-D models using nets.',
         '3-D Objects: Prisms, Pyramids, Cylinders and Nets', '3-D Objects',
         'Free CAPS Grade 6 3-D objects worksheets: prisms, pyramids, faces, edges, vertices, nets and cross-sections. 100 questions with memos.',
         'Prisms: named after the end face. Pyramids: after the base.', 'Count hidden faces too.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
