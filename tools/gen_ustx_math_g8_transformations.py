# -*- coding: utf-8 -*-
"""
Texas Grade 8 Math: Translations, Reflections and Rotations (TEKS 8.10A, 8.10B, 8.10C)
  python3 tools/gen_ustx_math_g8_transformations.py
Translations, reflections over the axes, rotations about the origin, naming the move from a rule, and which
transformations keep congruence (US Grade 8 makers with a new seed, plus an own congruence maker).
Wrong answers come from real mistakes: changing the wrong coordinate in a reflection, swapping without changing
signs in a rotation, and thinking a dilation keeps congruence.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_g8_transformations as trf
adopt(trf)
trf.R = random.Random(680140)
tx_common.GRADE = "grade-8"

from fractions import Fraction as F
from ws_common import num

INK = "#1f2937"


def g(v):
    s = ("%.2f" % v).rstrip("0").rstrip(".")
    if "." in s:
        a, b = s.split(".")
        return ("−" if v < 0 else "") + comma(abs(int(a))) + "." + b
    return num(int(s))


def pt(p):
    return "(%s, %s)" % (g(p[0]), g(p[1]))


CONG = [("Which transformation does <b>not</b> always keep a figure congruent?", "A dilation with scale factor 2", ["A translation", "A reflection over the x-axis", "A rotation of 90°"], "Dilations change the size, so the image is not congruent unless k = 1."),
        ("Which transformation keeps size and shape but can change orientation?", "A reflection", ["A dilation", "A translation", "A rotation of 360°"], "A reflection flips the figure: same size and shape, but the orientation reverses."),
        ("Which transformation keeps the same orientation?", "A translation", ["A reflection over the y-axis", "A reflection over the x-axis", "A dilation with a negative factor"], "A translation slides the figure without turning or flipping it."),
        ("A triangle is rotated 180° about the origin. Which is true?", "The image is congruent to the original", ["The image is twice as large", "The image is a different shape", "The angles change"], "Rotations are rigid motions: lengths and angles stay the same."),
        ("Which list contains only rigid transformations?", "Translation, reflection, rotation", ["Translation, dilation, rotation", "Reflection, dilation", "Dilation only"], "Translations, reflections and rotations keep congruence; dilations do not."),
        ("A figure and its image are congruent but face the opposite way. Which transformation could it be?", "A reflection", ["A translation", "A dilation", "A rotation of 360°"], "A <b>reflection</b> reverses the orientation.")]


def one_cong(r):
    q, a, w, e = r.choice(CONG)
    return mcq(q, a, w, e)


def build():
    sets, R = build_sets([
        ("Translations", [("run", trf.set_translate, (), 20)]),
        ("Reflections over the axes", [("run", trf.set_reflect, (), 20)]),
        ("Rotations about the origin", [("run", trf.set_rotate, (), 20)]),
        ("Name the move", [("run", trf.set_name, (), 20)]),
        ("Congruence and orientation", [("collect", one_cong, 6), ("run", trf.set_name, (), 14)]),
    ], 68014)
    finish(sets, R)
    body = lesson('<ul><li><b>Translation</b>: (x, y) → (x + a, y + b). <b>Reflection</b> over the x-axis: (x, −y); over the y-axis: (−x, y).</li><li><b>Rotation</b> about the origin: 90° counterclockwise (−y, x); 180° (−x, −y); 270° counterclockwise (y, −x).</li><li>Translations, reflections and rotations are <b>rigid</b>: the image is congruent.</li><li>Reflections reverse orientation; translations and rotations keep it.</li></ul>',
        [example("Reflect (3, 4) over the x-axis", ["Change the sign of y"], "(3, −4)"), example("Rotate (3, 1) 90° counterclockwise", ["(−y, x)"], "(−1, 3)")],
        [['Changing the wrong coordinate in a reflection', 'Over the x-axis, the y-value changes sign.'], ['Swapping without changing signs in a rotation', '90° counterclockwise: (x, y) → (−y, x).'], ['Thinking a dilation keeps congruence', 'A dilation changes the size.']])
    faq = [('What does TEKS 8.10A ask?', 'Generalize the properties of orientation and congruence of rotations, reflections, translations and dilations of two-dimensional shapes on a coordinate plane.'), ('What does TEKS 8.10B ask?', 'Differentiate between transformations that preserve congruence and those that do not.'), ('What does TEKS 8.10C ask?', 'Explain the effect of translations, reflections over the x- or y-axis, and rotations limited to 90°, 180°, 270° and 360° as applied to two-dimensional shapes on a coordinate plane using an algebraic representation.'), ('What does a 360° rotation do?', 'It returns every point to where it started.')]
    make('transformations', 14, 'Expressions, Equations and Relationships', '8.10A, 8.10B, 8.10C',
         '8.10A generalize the properties of orientation and congruence of rotations, reflections, translations, and dilations of two-dimensional shapes on a coordinate plane; 8.10B differentiate between transformations that preserve congruence and those that do not; 8.10C explain the effect of translations, reflections over the x- or y-axis, and rotations limited to 90°, 180°, 270°, and 360° as applied to two-dimensional shapes on a coordinate plane using an algebraic representation',
         'Translations, Reflections and Rotations', 'Transformations',
         'Free Grade 8 transformation worksheets for Texas TEKS 8.10: translations, reflections over the axes, rotations about the origin, algebraic rules and congruence. 100 questions with answers.',
         'Rigid moves keep congruence: translate, reflect, rotate.', 'Over the x-axis: (x, −y). 180°: (−x, −y).',
         body, faq, sets, seo_title='Grade 8 Transformations Worksheets: Translations, Reflections and Rotations (TEKS 8.10, STAAR)')


if __name__ == "__main__":
    build()
