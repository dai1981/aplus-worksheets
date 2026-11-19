# -*- coding: utf-8 -*-
"""
Texas Geometry: Points, Lines, Planes, Definitions and Spherical Geometry (TEKS G.4A, G.4D)
  python3 tools/gen_ustx_math_ge_points_lines.py
Naming lines, rays and segments, collinear points, counting and postulates, precise definitions (US Geometry makers
with a new seed), and undefined terms, postulates and theorems, and Euclidean versus spherical geometry (own maker).
Wrong answers come from real mistakes: calling a point defined, mixing up a postulate and a theorem, and thinking
parallel lines exist on a sphere.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_ge_points_lines_and_planes as pl
adopt(pl)
pl.R = random.Random(696010)
tx_common.GRADE = "geometry"

import us_hs
adopt(us_hs)


def W(fn, keep=None):
    """Use an item maker of another generator: its odd failures count as a skipped try, and a question text
    is used only once (not again with other wrong answers)."""
    seen = set()

    def f(r):
        try:
            it = fn(r)
        except (TypeError, ValueError, ZeroDivisionError, IndexError, KeyError):
            raise AssertionError("skip")
        if not it or (keep and not keep(it)) or it["q"] in seen:
            raise AssertionError("skip")
        seen.add(it["q"])
        return it
    f.__name__ = fn.__name__
    return f


def PR(fn, keep=None):
    """A fixed word-problem list of another generator as a set maker: a shuffled share of it."""
    def f(r):
        its = [it for it in fn() if keep is None or keep(it)]
        r.shuffle(its)
        return {"title": fn.__name__, "items": its * 3}
    f.__name__ = fn.__name__
    return f


MINUS = "−"
X = "<i>x</i>"


def sg(v):
    return ("−%s" % abs(v)) if v < 0 else str(v)


def poly(cs, v="<i>x</i>"):
    """[a, b, c] highest power first, e.g. 2x² − 3x + 1."""
    deg = len(cs) - 1
    out = ""
    for i, c in enumerate(cs):
        if c == 0:
            continue
        p = deg - i
        mag = abs(c)
        if p == 0:
            body = str(mag)
        else:
            body = ("" if mag == 1 else str(mag)) + v + ("<sup>%d</sup>" % p if p > 1 else "")
        if not out:
            out = (MINUS if c < 0 else "") + body
        else:
            out += (" − " if c < 0 else " + ") + body
    return out or "0"
def uniq(fn):
    """Never give the same question twice, even with other wrong answers."""
    seen = set()
    def f(r):
        it = fn(r)
        if it["q"] in seen:
            raise AssertionError("repeat")
        seen.add(it["q"])
        return it
    f.__name__ = fn.__name__
    return f



TERMS = [("point", "an undefined term"), ("line", "an undefined term"), ("plane", "an undefined term"), ("segment", "a definition"), ("ray", "a definition"),
         ("angle", "a definition"), ("midpoint", "a definition"), ("“Through any two points there is exactly one line.”", "a postulate"),
         ("“If two lines intersect, they intersect in exactly one point.”", "a postulate"), ("“Vertical angles are congruent.”", "a theorem"),
         ("“The angles of a triangle add to 180°.”", "a theorem"), ("“The base angles of an isosceles triangle are congruent.”", "a theorem"),
         ("“The sum of the angles of any quadrilateral seems to be 360°,” said after measuring three quadrilaterals", "a conjecture"),
         ("“The diagonals of every rectangle seem to be equal,” said after drawing two rectangles", "a conjecture"),
         ("“A ruler can measure the distance between any two points.” (Ruler Postulate)", "a postulate")]
KINDS = ["an undefined term", "a definition", "a postulate", "a theorem", "a conjecture"]
WHY = {"an undefined term": "It is described, not defined, and is used to define other terms.", "a definition": "It is described exactly using undefined terms.",
       "a postulate": "It is accepted as true without proof.", "a theorem": "It is proved from definitions, postulates and other theorems.",
       "a conjecture": "It is a guess based on patterns that has not been proved."}


def one_term(r):
    t, k = r.choice(TERMS)
    return mcq("Which kind is this: an undefined term, a definition, a postulate, a theorem or a conjecture? <b>%s</b>" % (t[0].upper() + t[1:] if t[0] != "“" else t), k[0].upper() + k[1:], [x[0].upper() + x[1:] for x in KINDS if x != k],
               "%s <b>%s</b>." % (WHY[k], k[0].upper() + k[1:]))


SPH = [("On a sphere, a “line” is a great circle. How many lines through a point are parallel to a given line?", "None: every two great circles meet", ["Exactly one", "Exactly two", "Infinitely many"],
        "Any two great circles cross, so on a sphere there are <b>no parallel lines</b>."),
       ("In Euclidean (flat) geometry, how many lines through a point not on a line are parallel to it?", "Exactly one", ["None", "Exactly two", "Infinitely many"],
        "This is the Parallel Postulate: <b>exactly one</b>."),
       ("What can the sum of the angles of a triangle on a sphere be?", "More than 180°", ["Exactly 180°", "Less than 180°", "Exactly 90°"],
        "Spherical triangles bulge outward, so their angles add to <b>more than 180°</b>."),
       ("What is the sum of the angles of a triangle in Euclidean geometry?", "Exactly 180°", ["More than 180°", "Less than 180°", "360°"], "In a plane the angles of a triangle add to <b>180°</b>."),
       ("On a sphere, how many times do two different great circles intersect?", "Twice", ["Once", "Never", "Infinitely many times"], "Two great circles meet at <b>two</b> opposite points."),
       ("Which is a “line” in spherical geometry?", "The equator", ["A line of latitude near the North Pole", "A straight tunnel through the Earth", "A circle around a city"],
        "A line on a sphere is a great circle, like <b>the equator</b>."),
       ("A triangle on a globe has three 90° angles. What is the angle sum?", "270°", ["180°", "90°", "360°"], "90° + 90° + 90° = <b>270°</b>, more than 180°."),
       ("Which statement is true in Euclidean geometry but false on a sphere?", "Parallel lines never meet", ["A line can be extended", "Two points lie on a line", "Angles can be measured"],
        "On a sphere every two lines meet, so <b>parallel lines never meet</b> is false there.")]


def one_sph(r):
    q, a, w, e = r.choice(SPH)
    return mcq(q, a, w, e)


def build():
    sets, R = build_sets([
        ("Name lines, rays and segments", [("collect", W(pl.one_name), 20)]),
        ("Collinear and coplanar points", [("collect", W(pl.one_col), 20)]),
        ("Precise definitions", [("collect", W(pl.one_def), 20)]),
        ("Undefined terms, postulates and theorems", [("collect", uniq(one_term), 12), ("collect", W(pl.one_count), 8)]),
        ("Euclidean and spherical geometry", [("collect", uniq(one_sph), 8), ("collect", W(pl.one_box), 12)]),
    ], 69601)
    finish(sets, R)
    body = lesson("<ul><li><b>Undefined terms</b>: point, line and plane. They are described, not defined.</li><li>A <b>definition</b> uses those terms: a segment is part of a line between two endpoints.</li><li>A <b>postulate</b> is accepted without proof. A <b>theorem</b> is proved. A <b>conjecture</b> is a guess not yet proved.</li><li>On a <b>sphere</b>, lines are great circles: there are no parallel lines and a triangle's angles add to more than 180°.</li></ul>",
        [example("“Vertical angles are congruent.”", ["it can be proved"], "a theorem")],
        [['Calling a point defined', 'Point, line and plane are undefined.'], ['Mixing up a postulate and a theorem', 'Only theorems are proved.'], ['Thinking parallel lines exist on a sphere', 'Great circles always meet.']])
    faq = [('What does TEKS G.4A ask?', 'Distinguish between undefined terms, definitions, postulates, conjectures, and theorems.'), ('What does TEKS G.4D ask?', 'Compare geometric relationships between Euclidean and spherical geometries, including parallel lines and the sum of the angles in a triangle.'), ('What is a ray?', 'Part of a line with one endpoint that goes on forever in one direction.'), ('Are any three points coplanar?', 'Yes. Any three points lie in a plane.')]
    make('points-lines-planes-and-definitions', 1, 'Logical Argument and Constructions', 'G.4A, G.4D',
         'G.4A distinguish between undefined terms, definitions, postulates, conjectures, and theorems; G.4D compare geometric relationships between Euclidean and spherical geometries, including parallel lines and the sum of the angles in a triangle',
         'Points, Lines, Planes, Definitions and Spherical Geometry', 'Points, Lines and Planes',
         'Free Geometry worksheets for Texas TEKS G.4A and G.4D: points, lines and planes, definitions, postulates, theorems and conjectures, and Euclidean versus spherical geometry. 100 questions with answers.',
         'Point, line and plane are undefined; theorems are proved.', "On a sphere a triangle's angles add to more than 180°.",
         body, faq, sets, seo_title='Geometry Points, Lines, Planes and Definitions Worksheets (TEKS G.4A)')


if __name__ == "__main__":
    build()
