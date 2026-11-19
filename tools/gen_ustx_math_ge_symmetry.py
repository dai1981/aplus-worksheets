# -*- coding: utf-8 -*-
"""
Texas Geometry: Reflectional and Rotational Symmetry (TEKS G.3D)
  python3 tools/gen_ustx_math_ge_symmetry.py
Symmetry and properties of transformations (US Geometry maker), and lines of symmetry, order and angle of
rotational symmetry, and which kind of symmetry a figure has (own makers).
Wrong answers come from real mistakes: counting the diagonals of a rectangle as lines of symmetry, giving 360° as the
angle, and thinking a parallelogram has a line of symmetry.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_ge_rigid_transformations as rt
adopt(rt)
rt.R = random.Random(696080)
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


FIG = [("an equilateral triangle", 3, 3), ("a square", 4, 4), ("a rectangle that is not a square", 2, 2), ("a rhombus that is not a square", 2, 2),
       ("a parallelogram that is not a rectangle or rhombus", 0, 2), ("an isosceles trapezoid", 1, 1), ("a kite that is not a rhombus", 1, 1),
       ("a regular pentagon", 5, 5), ("a regular hexagon", 6, 6), ("a regular octagon", 8, 8), ("a regular decagon", 10, 10),
       ("an isosceles triangle that is not equilateral", 1, 1), ("a scalene triangle", 0, 1), ("a circle", None, None), ("a regular heptagon", 7, 7), ("a regular 12-gon", 12, 12)]


def one_lines(r):
    name, l, o = r.choice([f for f in FIG if f[1] is not None])
    w = [str(x) for x in (l + 2, l * 2, l - 1 if l > 1 else 4, l + 1)]
    return mcq("How many lines of symmetry does %s have?" % name, str(l), w, "%s has <b>%d</b> line%s of symmetry." % (name[0].upper() + name[1:], l, "" if l == 1 else "s"))


def one_angle(r):
    name, l, o = r.choice([f for f in FIG if f[2] and f[2] > 1])
    a = 360 // o
    w = ["%d°" % x for x in (360, 360 * 2 // o if o > 2 else 90, a // 2 if a > 30 else a * 3, 180 if a != 180 else 120)]
    return mcq("What is the smallest angle you can rotate %s so it looks the same?" % name, "%d°" % a, w, "It has rotational symmetry of order %d: 360° ÷ %d = <b>%d°</b>." % (o, o, a))


def one_order(r):
    name, l, o = r.choice([f for f in FIG if f[2]])
    w = [str(x) for x in (o + 1, 2 * o, o + 2, 360 // o, 4)]
    return mcq("What is the order of rotational symmetry of %s?" % name, str(o), w, "It matches itself <b>%d</b> time%s in a full turn." % (o, "" if o == 1 else "s"))


LINES = {"A": 1, "B": 1, "C": 1, "D": 1, "E": 1, "H": 2, "I": 2, "M": 1, "O": 2, "T": 1, "U": 1, "V": 1, "W": 1, "X": 2, "Y": 1, "K": 1,
         "F": 0, "G": 0, "J": 0, "L": 0, "N": 0, "P": 0, "R": 0, "S": 0, "Z": 0}
ROT = set("HINOSXZ")


def one_letter(r):
    c = r.choice(sorted(LINES))
    if r.random() < 0.5:
        n = LINES[c]
        return mcq("How many lines of symmetry does the block capital letter <b>%s</b> have?" % c, str(n), [str(x) for x in (0, 1, 2, 4) if x != n],
                   "The letter %s has <b>%d</b> line%s of symmetry." % (c, n, "" if n == 1 else "s"))
    yes = c in ROT
    right = "Yes, after a half turn (180°)" if yes else "No"
    return mcq("Does the block capital letter <b>%s</b> have rotational symmetry?" % c, right, ["No" if yes else "Yes, after a half turn (180°)", "Yes, after a quarter turn (90°)", "Yes, after a full turn only"],
               "Turn %s upside down: it %s. <b>%s</b>." % (c, "looks the same" if yes else "looks different", right))


KIND = ["Both reflectional and rotational symmetry", "Reflectional symmetry only", "Rotational symmetry only", "Neither"]


def one_kind(r):
    name, l, o = r.choice([f for f in FIG if f[1] is not None])
    k = 0 if (l and o > 1) else (1 if l else (2 if o > 1 else 3))
    return mcq("What kind of symmetry does %s have?" % name, KIND[k], [x for i, x in enumerate(KIND) if i != k],
               "It has %d line%s of symmetry and rotational order %d: <b>%s</b>." % (l, "" if l == 1 else "s", o, KIND[k].lower()))


def build():
    sets, R = build_sets([
        ("Lines of symmetry", [("collect", uniq(one_lines), 15), ("collect", uniq(one_kind), 5)]),
        ("Order of rotational symmetry", [("collect", uniq(one_order), 14), ("collect", uniq(one_kind), 6)]),
        ("Angle of rotational symmetry", [("collect", uniq(one_angle), 11), ("collect", uniq(one_kind), 4), ("collect", W(rt.one_sym), 5)]),
        ("Symmetry of letters", [("collect", uniq(one_letter), 20)]),
        ("Symmetry and transformations", [("collect", W(rt.one_sym), 20)]),
    ], 69608)
    finish(sets, R)
    body = lesson('<ul><li><b>Reflectional (line) symmetry</b>: a line splits the figure into two mirror images.</li><li><b>Rotational symmetry</b>: the figure looks the same after a turn of less than 360°.</li><li>The <b>order</b> is how many times it matches itself in a full turn. The smallest angle is 360° ÷ order.</li><li>A regular <i>n</i>-gon has <i>n</i> lines of symmetry and order <i>n</i>.</li></ul>',
        [example("Regular hexagon", ["6 lines", "360° ÷ 6"], "6 lines of symmetry; rotates by 60°")],
        [["Counting a rectangle's diagonals", 'They are not lines of symmetry.'], ['Giving 360° as the angle', 'Every figure looks the same after 360°.'], ['Thinking a parallelogram has a line of symmetry', 'It has only rotational symmetry.']])
    faq = [('What does TEKS G.3D ask?', 'Identify and distinguish between reflectional and rotational symmetry in a plane figure.'), ('How many lines of symmetry does a circle have?', 'Infinitely many.'), ('Does a scalene triangle have symmetry?', 'No.'), ('What is order 1?', 'No rotational symmetry.')]
    make('reflectional-and-rotational-symmetry', 8, 'Coordinate and Transformational Geometry', 'G.3D',
         'G.3D identify and distinguish between reflectional and rotational symmetry in a plane figure',
         'Reflectional and Rotational Symmetry', 'Symmetry',
         'Free Geometry symmetry worksheets for Texas TEKS G.3D: lines of symmetry, order and angle of rotational symmetry, and reflectional versus rotational symmetry. 100 questions with answers.',
         'Regular n-gon: n lines, order n, angle 360° ÷ n.', 'A parallelogram has rotational symmetry only.',
         body, faq, sets, seo_title='Geometry Reflectional and Rotational Symmetry Worksheets (TEKS G.3D)')


if __name__ == "__main__":
    build()
