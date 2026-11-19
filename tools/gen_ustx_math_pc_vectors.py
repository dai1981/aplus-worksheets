# -*- coding: utf-8 -*-
"""
Texas Precalculus: Vectors: Magnitude, Direction and Operations (TEKS P.4I, P.4J, P.4K)
  python3 tools/gen_ustx_math_pc_vectors.py
Component form, magnitude and direction, vectors from a magnitude and direction, adding and subtracting vectors,
scalar multiples and linear combinations, and force and velocity problems (US Precalculus makers with a new seed).
Wrong answers come from real mistakes: subtracting the points in the wrong order, adding the magnitudes, and the wrong
quadrant for the direction angle.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_pc_vectors as vc
adopt(vc)
vc.R = random.Random(698200)
import gen_us_math_pc_vector_operations as vo
adopt(vo)
vo.R = random.Random(698201)
tx_common.GRADE = "precalculus"

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


from fractions import Fraction as Fr


def ft(v):
    v = Fr(v)
    if v.denominator == 1:
        return sg(int(v))
    return (MINUS if v < 0 else "") + fr(abs(v.numerator), v.denominator)


def fx(body, name="f"):
    return "<i>%s</i>(<i>x</i>) = %s" % (name, body)



def build():
    sets, R = build_sets([
        ("Component form and magnitude", [("collect", W(vc.one_comp), 10), ("collect", W(vc.one_mag), 10)]),
        ("Direction angles", [("collect", W(vc.one_dir), 10), ("collect", W(vc.one_fromdir), 10)]),
        ("Add and subtract vectors", [("collect", W(vo.one_add), 20)]),
        ("Scalar multiples and combinations", [("collect", W(vo.one_lin), 20)]),
        ("Forces and velocities", [("collect", W(vc.one_word), 10), ("collect", W(vo.one_word), 10)]),
    ], 69820)
    finish(sets, R)
    body = lesson('<ul><li>A <b>vector</b> has magnitude (length) and direction. From <i>P</i>(<i>x</i><sub>1</sub>, <i>y</i><sub>1</sub>) to <i>Q</i>(<i>x</i><sub>2</sub>, <i>y</i><sub>2</sub>): ⟨<i>x</i><sub>2</sub> − <i>x</i><sub>1</sub>, <i>y</i><sub>2</sub> − <i>y</i><sub>1</sub>⟩.</li><li>Magnitude |⟨<i>a</i>, <i>b</i>⟩| = √(<i>a</i><sup>2</sup> + <i>b</i><sup>2</sup>). Direction θ with tan θ = <i>b</i> ÷ <i>a</i>, in the right quadrant.</li><li>Add vectors component by component (tip to tail). A scalar <i>k</i> multiplies each component and stretches the vector.</li><li>Magnitude <i>m</i> and direction θ: ⟨<i>m</i> cos θ, <i>m</i> sin θ⟩.</li></ul>',
        [example("<b>u</b> = ⟨3, −1⟩, <b>v</b> = ⟨−2, 5⟩", ["2<b>u</b> = ⟨6, −2⟩", "2<b>u</b> + <b>v</b> = ⟨4, 3⟩"], "|2<b>u</b> + <b>v</b>| = 5")],
        [['Subtracting in the wrong order', 'Terminal point minus initial point.'], ['Adding magnitudes', 'Add components, then find the magnitude.'], ['The wrong quadrant', 'Check the signs of the components.']])
    faq = [('What does TEKS P.4I ask?', 'Use vectors to model situations involving magnitude and direction.'), ('What does TEKS P.4J ask?', 'Represent the addition of vectors and the multiplication of a vector by a scalar geometrically and symbolically.'), ('What does TEKS P.4K ask?', 'Apply vector addition and multiplication of a vector by a scalar in mathematical and real-world problems.'), ('What is a resultant?', 'The single vector equal to the sum of several vectors.')]
    make('vectors', 20, 'Number and Measure', 'P.4I, P.4J, P.4K',
         'P.4I use vectors to model situations involving magnitude and direction; P.4J represent the addition of vectors and the multiplication of a vector by a scalar geometrically and symbolically; P.4K apply vector addition and multiplication of a vector by a scalar in mathematical and real-world problems',
         'Vectors: Magnitude, Direction and Operations', 'Vectors',
         'Free Precalculus vector worksheets for Texas TEKS P.4I to P.4K: component form, magnitude, direction, vector addition, scalar multiples and force and velocity problems. 100 questions with answers.',
         'Add vectors component by component.', '|⟨a, b⟩| = √(a² + b²).',
         body, faq, sets, seo_title='Precalculus Vectors Worksheets (TEKS P.4I–P.4K)')


if __name__ == "__main__":
    build()
