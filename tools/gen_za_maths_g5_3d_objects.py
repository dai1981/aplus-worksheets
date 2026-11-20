# -*- coding: utf-8 -*-
"""
South Africa Grade 5 Maths (CAPS): 3-D Objects: Prisms, Pyramids, Cylinders, Cones and Nets (Grade 5: 3.2 Properties of 3-D objects)
  python3 tools/gen_za_maths_g5_3d_objects.py
Naming prisms, pyramids, cubes, cylinders, cones and spheres, faces, edges and vertices, and nets (BC Grade 5 and
Australia Year 5 makers).
Wrong answers come from real mistakes: naming a prism after the side faces, counting only the faces you can see, and
choosing a net that folds with two faces on top of each other.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_cabc_math_g5_prisms_pyramids as cbp
adopt(cbp)
if isinstance(getattr(cbp, 'R', None), random.Random): cbp.R = random.Random(805170)
import gen_au_maths_y5_nets as aun
adopt(aun)
if isinstance(getattr(aun, 'R', None), random.Random): aun.R = random.Random(805171)
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
        ("Prism or pyramid?", [("run", cbp.set_kind, ("rnd", cbp.Pos, cbp.People), 20, six)]),
        ("Name the object", [("run", cbp.set_name, ("rnd", cbp.Pos), 10, six), ("run", aun.set_name, ("rnd", aun.Pos), 10, six)]),
        ("Faces, edges and vertices", [("run", cbp.set_fev, ("rnd",), 10, six), ("run", aun.set_fev, ("rnd",), 10, six)]),
        ("Nets", [("run", aun.set_cube_nets, ("rnd",), 10, six), ("run", aun.set_folding, ("rnd",), 10, six)]),
        ("Objects around us", [("run", cbp.set_real, ("rnd", cbp.People), 10, six), ("run", aun.set_real, ("rnd", aun.People), 10, six)]),
    ], 80517)
    finish(sets, R)
    body = lesson('<ul><li>A <b>prism</b> has two identical end faces joined by rectangles. It is named after its end face: triangular prism.</li><li>A <b>pyramid</b> has one base and triangles that meet at a point (apex). It is named after its base.</li><li>Cylinders, cones and spheres have curved surfaces.</li><li>A <b>net</b> is a flat shape that folds up to make the object.</li></ul>',
        [example("2 triangles and 3 rectangles", ["the end faces are triangles"], "a triangular prism")],
        [['Named after the sides', 'Use the end face or the base.'], ['Faces you can see', 'Count the hidden faces too.'], ['Overlapping net', 'Each face needs its own place.']])
    faq = [('What does CAPS Grade 5 say about 3-D objects?', 'Recognise, visualise and name 3-D objects (spheres, cylinders, cones, prisms and pyramids), describe and compare their faces, and make 3-D models with nets.'), ('How many faces does a square-based pyramid have?', '5.'), ('Is a cube a prism?', 'Yes, a square prism with all faces equal.'), ('Does a cylinder have edges?', 'It has 2 curved edges.')]
    make('3d-objects', 17, 'Space and Shape (Geometry)', 'Grade 5: 3.2 Properties of 3-D objects',
         'Recognise, visualise and name 3-D objects in the environment and geometric settings, focusing on rectangular prisms and other prisms, cubes, cylinders, cones and pyramids; describe, sort and compare 3-D objects in terms of shape of faces, number of faces, flat and curved surfaces; make 3-D models using cut-out polygons and nets.',
         '3-D Objects: Prisms, Pyramids, Cylinders, Cones and Nets', '3-D Objects',
         'Free CAPS Grade 5 3-D objects worksheets: prisms, pyramids, cylinders, cones, faces, edges, vertices and nets. 100 questions with memos.',
         'Prisms are named after the end face, pyramids after the base.', 'A net folds into the object.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
