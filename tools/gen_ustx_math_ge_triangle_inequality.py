# -*- coding: utf-8 -*-
"""
Texas Geometry: The Triangle Inequality Theorem (TEKS G.5D)
  python3 tools/gen_ustx_math_ge_triangle_inequality.py
Can three lengths make a triangle, the possible lengths of the third side, side and angle order (US Geometry maker),
and triangle inequality word problems (own makers).
Wrong answers come from real mistakes: checking only one pair of sides, including the endpoints of the range, and
putting the largest angle opposite the shortest side.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_ge_midsegments_and_triangle_centers as mc
adopt(mc)
mc.R = random.Random(696100)
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



def one_can(r):
    a, b = r.randint(2, 15), r.randint(2, 15)
    kind = r.choice(["yes", "no", "eq"])
    if kind == "yes":
        c = r.randint(abs(a - b) + 1, a + b - 1)
    elif kind == "eq":
        c = a + b
    else:
        c = a + b + r.randint(1, 6)
    s = sorted([a, b, c])
    ok = s[0] + s[1] > s[2]
    right = "Yes" if ok else "No, %d + %d %s %d" % (s[0], s[1], "=" if s[0] + s[1] == s[2] else "&lt;", s[2])
    w = (["No, %d + %d &lt; %d" % (s[0], s[2], s[1]), "No, the sides are different", "Only if it is a right triangle"] if ok else
         ["Yes", "Yes, because %d + %d &gt; %d" % (s[1], s[2], s[0]), "Only if it is a right triangle"])
    return mcq("Can segments of lengths %d, %d and %d form a triangle?" % (a, b, c), right, w,
               "The two shorter sides must add to more than the longest: %d + %d = %d, %s %d. <b>%s</b>." % (s[0], s[1], s[0] + s[1], "more than" if ok else "not more than", s[2], right))


def one_range(r):
    a, b = sorted(r.sample(range(3, 25), 2))
    lo, hi = b - a, a + b
    right = "%d &lt; <i>x</i> &lt; %d" % (lo, hi)
    w = ["%d ≤ <i>x</i> ≤ %d" % (lo, hi), "%d &lt; <i>x</i> &lt; %d" % (a, b), "0 &lt; <i>x</i> &lt; %d" % hi]
    return mcq("Two sides of a triangle are %d and %d. Which describes the possible lengths <i>x</i> of the third side?" % (a, b), right, w,
               "The third side is more than %d − %d = %d and less than %d + %d = %d: <b>%s</b>." % (b, a, lo, a, b, hi, right))


def one_count(r):
    a, b = sorted(r.sample(range(3, 16), 2))
    n = (a + b - 1) - (b - a + 1) + 1
    return mcq("Two sides of a triangle are %d cm and %d cm. The third side is a whole number of centimeters. How many lengths are possible?" % (a, b), str(n), [str(n + 2), str(n - 1), str(a + b)],
               "The third side is between %d and %d, not equal to either: %d to %d, which is <b>%d</b> lengths." % (b - a, a + b, b - a + 1, a + b - 1, n))


PLACES = [("a school", "a library", "a park"), ("a house", "a store", "a gym"), ("a farm", "a barn", "a pond"), ("Austin", "a lake", "a ranch")]


def one_word(r):
    p1, p2, p3 = r.choice(PLACES)
    a, b = sorted(r.sample(range(2, 12), 2))
    lo, hi = b - a, a + b
    kind = r.randrange(2)
    if kind == 0:
        c = r.choice([lo, hi, hi + r.randint(1, 4)] + [r.randint(lo + 1, hi - 1)] * 2)
        ok = lo < c < hi
        right = "Yes" if ok else "No"
        cap = lambda t: t[0].upper() + t[1:]
        return mcq("%s is %d miles from %s. %s is %d miles from %s. The three places are not in a straight line. Could %s be %d miles from %s?" % (cap(p1), a, p2, cap(p2), b, p3, p1.replace("a ", "the ", 1), c, p3.replace("a ", "the ", 1)),
                   right, ["No" if ok else "Yes", "Only if the roads are straight", "Only if the distance is a whole number"], "The distance must be between %d and %d miles: <b>%s</b>." % (lo, hi, right.lower()))
    return mcq("A triangular garden has sides of %d m and %d m. What is the greatest whole-number length the third side can have?" % (a, b), "%d m" % (hi - 1), ["%d m" % hi, "%d m" % (hi + 1), "%d m" % (b - a)],
               "The third side must be less than %d + %d = %d, so the greatest whole number is <b>%d m</b>." % (a, b, hi, hi - 1))


def build():
    sets, R = build_sets([
        ("Can the lengths form a triangle?", [("collect", uniq(one_can), 20)]),
        ("Possible lengths of the third side", [("collect", uniq(one_range), 20)]),
        ("How many whole-number lengths?", [("collect", uniq(one_count), 20)]),
        ("Side lengths and angle order", [("collect", W(mc.one_ineq), 20)]),
        ("Triangle inequality word problems", [("collect", uniq(one_word), 20)]),
    ], 69610)
    finish(sets, R)
    body = lesson('<ul><li><b>Triangle Inequality Theorem</b>: the sum of any two sides is greater than the third side.</li><li>Check the two shortest sides against the longest.</li><li>If two sides are <i>a</i> and <i>b</i>, the third side is between |<i>a</i> − <i>b</i>| and <i>a</i> + <i>b</i>.</li><li>The longest side is opposite the largest angle.</li></ul>',
        [example("Sides 5 and 9", ["9 − 5 = 4", "9 + 5 = 14"], "4 &lt; <i>x</i> &lt; 14")],
        [['Checking only one pair', 'Check the two shortest against the longest.'], ['Including the endpoints', 'Equal to the sum makes a flat line.'], ['Largest angle opposite the shortest side', 'It is opposite the longest side.']])
    faq = [('What does TEKS G.5D ask?', 'Verify the Triangle Inequality theorem using constructions and apply the theorem to solve problems.'), ('Can 3, 4 and 7 make a triangle?', 'No. 3 + 4 = 7, so the sides lie flat.'), ('Why does it work?', 'The shortest path between two points is a straight segment.'), ('Which side is opposite the smallest angle?', 'The shortest side.')]
    make('triangle-inequality-theorem', 10, 'Logical Argument and Constructions', 'G.5D',
         'G.5D verify the Triangle Inequality theorem using constructions and apply the theorem to solve problems',
         'The Triangle Inequality Theorem', 'Triangle Inequality',
         'Free Geometry worksheets for Texas TEKS G.5D: the Triangle Inequality Theorem, possible third-side lengths, side and angle order and word problems. 100 questions with answers.',
         'Any two sides add to more than the third.', 'Sides 5 and 9: 4 < x < 14.',
         body, faq, sets, seo_title='Geometry Triangle Inequality Theorem Worksheets (TEKS G.5D)')


if __name__ == "__main__":
    build()
