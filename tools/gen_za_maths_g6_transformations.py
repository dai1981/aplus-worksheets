# -*- coding: utf-8 -*-
"""
South Africa Grade 6 Maths (CAPS): Transformations: Translations, Reflections, Rotations, Enlargements and Reductions (Grade 6: 3.4 Transformations)
  python3 tools/gen_za_maths_g6_transformations.py
Translations, reflections and rotations, naming the transformation (BC Grade 6 makers), and enlargements and
reductions with scale factors (own maker).
Wrong answers come from real mistakes: mixing up a reflection and a rotation, adding the scale factor instead of
multiplying, and changing only one side in an enlargement.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_cabc_math_g6_transformations as cbt
adopt(cbt)
if isinstance(getattr(cbt, 'R', None), random.Random): cbt.R = random.Random(806240)
za_common.GRADE = "grade-6"

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


def rect_pair_svg(a, b, k):
    s = 32 if max(a, b) * max(k, 1) <= 8 else 16
    W = 40 + a * s + 40 + int(a * k * s) + 20
    H = max(b, b * k) * s + 50
    out = "<svg viewBox='0 0 %d %d' width='%d' height='%d' role='img' aria-label='a rectangle and its %s'>" % (W, H, W, H, "enlargement" if k > 1 else "reduction")
    out += "<rect x='20' y='%d' width='%d' height='%d' fill='#cfe6d6' stroke='#006633' stroke-width='2'/>" % (H - 20 - b * s, a * s, b * s)
    x2 = 20 + a * s + 40
    out += "<rect x='%d' y='%d' width='%d' height='%d' fill='#fff1a8' stroke='#b38f00' stroke-width='2'/>" % (x2, H - 20 - int(b * k * s), int(a * k * s), int(b * k * s))
    out += "<text x='%d' y='%d' font-size='13' text-anchor='middle'>A</text><text x='%d' y='%d' font-size='13' text-anchor='middle'>B</text>" % (20 + a * s // 2, H - 6, x2 + int(a * k * s) // 2, H - 6)
    return out + "</svg>"


def one_enl(r):
    k = r.choice(["new_len", "factor", "reduce", "picture", "perim"])
    a, b = r.randint(2, 9), r.randint(2, 9)
    if a == b:
        raise AssertionError
    if k == "new_len":
        f = r.choice([2, 3, 4, 5])
        return mcq("A rectangle is %d cm long and %d cm wide. It is enlarged by a scale factor of %d. How long is the new rectangle?" % (a, b, f), "%d cm" % (a * f), ["%d cm" % x for x in (a + f, b * f, a * f * f)],
                   "Multiply every length by %d: %d × %d = <b>%d cm</b>." % (f, a, f, a * f))
    if k == "factor":
        f = r.choice([2, 3, 4, 5])
        return mcq("A triangle has a side of %d cm. After an enlargement the side is %d cm. What is the scale factor?" % (a, a * f), str(f), [str(a * f - a), str(a * f), str(f + 1)],
                   "%d ÷ %d = <b>%d</b>. Every side is %d times as long." % (a * f, a, f, f))
    if k == "reduce":
        f = r.choice([2, 4, 5, 10])
        A, B = a * f, b * f
        return mcq("A picture is %d cm by %d cm. It is reduced so that every side is %s as long. What size is the new picture?" % (A, B, "half" if f == 2 else fr(1, f)),
                   "%d cm by %d cm" % (a, b), ["%d cm by %d cm" % x for x in ((A - f, B - f), (A * f, B * f), (a, B))],
                   "Divide every side by %d: %d ÷ %d = %d and %d ÷ %d = %d. <b>%d cm by %d cm</b>." % (f, A, f, a, B, f, b, a, b))
    if k == "picture":
        a, b = r.randint(1, 3), r.randint(1, 3)
        f = r.choice([2, 3])
        if a == b:
            raise AssertionError
        q = fig(rect_pair_svg(a, b, f)) + "Rectangle A is %d squares by %d squares. B is an enlargement of A. What is the scale factor?" % (a, b)
        return mcq(q, str(f), [str(f + 1), str(a * f), "%d squares" % (a * f - a)] if a * f != f + 1 else [str(f + 2), str(a * f + 1), "%d squares" % (a * f - a)],
                   "B is %d by %d squares: %d ÷ %d = <b>%d</b>." % (a * f, b * f, a * f, a, f))
    f = r.choice([2, 3])
    p = 2 * (a + b)
    return mcq("A rectangle %d cm by %d cm is enlarged by a scale factor of %d. What is the perimeter of the new rectangle?" % (a, b, f), "%d cm" % (p * f), ["%d cm" % x for x in (p, p + f * 4, p * f * f)],
               "New sides: %d cm and %d cm. Perimeter = 2 × (%d + %d) = <b>%d cm</b>. (The perimeter is also %d times as long.)" % (a * f, b * f, a * f, b * f, p * f, f))


def build():
    sets, R = build_sets([
        ("Translations and reflections", [("run", cbt.set_translate, ("rnd", cbt.People), 10, noneg), ("run", cbt.set_reflect, ("rnd", cbt.People), 10, noneg)]),
        ("Rotations", [("run", cbt.set_rotate, ("rnd", cbt.People), 20, noneg)]),
        ("Which transformation?", [("run", cbt.set_which, ("rnd", cbt.People), 10, noneg), ("run", cbt.set_combine, ("rnd", cbt.People), 10, noneg)]),
        ("Enlargements", [("collect", uniq(one_enl), 20)]),
        ("Enlargement and reduction problems", [("collect", uniq(one_enl), 20)]),
    ], 80624)
    finish(sets, R)
    body = lesson('<ul><li><b>Translation</b>: slide. <b>Reflection</b>: flip over a line. <b>Rotation</b>: turn around a point. The size stays the same.</li><li>An <b>enlargement</b> makes a shape bigger; a <b>reduction</b> makes it smaller. The shape stays the same.</li><li>The <b>scale factor</b> tells you how many times as long each side is.</li><li>Multiply every side by the scale factor (or divide for a reduction).</li></ul>',
        [example("A 3 cm by 5 cm rectangle, scale factor 2", ["3 × 2", "5 × 2"], "6 cm by 10 cm")],
        [['Reflection or rotation?', 'A reflection makes a mirror image.'], ['Adding the factor', 'Multiply, do not add.'], ['One side only', 'Every side changes.']])
    faq = [('What does CAPS Grade 6 say about transformations?', 'Recognise, describe and perform translations, reflections and rotations, and enlarge and reduce 2-D shapes, comparing sizes.'), ('Does an enlargement change the angles?', 'No, the angles stay the same.'), ('What is a scale factor of 3?', 'Every length is 3 times as long.'), ('Is a photocopy reduction a transformation?', 'Yes, it is a reduction.')]
    make('transformations-enlargements-and-reductions', 24, 'Space and Shape (Geometry)', 'Grade 6: 3.4 Transformations',
         'Recognise, describe and perform translations, reflections and rotations with 2-D shapes; draw enlargements and reductions of 2-D shapes to compare size and shape of triangles and quadrilaterals.',
         'Transformations: Translations, Reflections, Rotations, Enlargements and Reductions', 'Transformations',
         'Free CAPS Grade 6 transformations worksheets: translations, reflections, rotations, enlargements, reductions and scale factors. 100 questions with memos.',
         'Enlarge: multiply every side by the scale factor.', 'Slide, flip, turn: the size stays the same.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
