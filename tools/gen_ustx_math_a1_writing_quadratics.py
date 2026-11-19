# -*- coding: utf-8 -*-
"""
Texas Algebra I: Writing Quadratic Functions (TEKS A.6B, A.6C)
  python3 tools/gen_ustx_math_a1_writing_quadratics.py
Vertex form from the vertex and a point or the y-intercept, vertex form to standard form, and functions from their
zeros (own makers), plus vertex form and transformations (US Algebra 1 maker with a new seed).
Wrong answers come from real mistakes: the wrong sign for h, finding a without squaring, and writing x + 3 for a zero of 3.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_a1_graphing_quadratic_functions as gq
adopt(gq)
gq.R = random.Random(695180)
tx_common.GRADE = "algebra-1"

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



def vf(a, h, k):
    s = "" if a == 1 else (MINUS if a == -1 else sg(a))
    inner = X if h == 0 else "(%s %s %d)" % (X, MINUS if h > 0 else "+", abs(h))
    t = s + inner + "<sup>2</sup>"
    if k:
        t += " %s %d" % ("+" if k > 0 else MINUS, abs(k))
    return "<i>f</i>(<i>x</i>) = " + t


def ff(a, r1, r2):
    s = "" if a == 1 else (MINUS if a == -1 else sg(a))
    one = lambda z: X if z == 0 else "(%s %s %d)" % (X, MINUS if z > 0 else "+", abs(z))
    return "<i>f</i>(<i>x</i>) = %s%s%s" % (s, one(r1), one(r2))


AS = [1, -1, 2, -2, 3, -3]


def one_vp(r):
    a, h, k = r.choice(AS), r.randint(-6, 6), r.randint(-8, 8)
    d = r.choice([-2, -1, 1, 2])
    x, y = h + d, k + a * d * d
    right = vf(a, h, k)
    a2 = (y - k) // d if (y - k) % d == 0 else None
    w = [vf(a, -h, k), vf(a2, h, k) if a2 not in (None, a, 0) else vf(-a, h, k), vf(a, h, -k) if k else vf(a, h, 1)]
    w = [c for c in w if c != right]
    return mcq("A parabola has vertex (%s, %s) and passes through (%s, %s). Write its equation in vertex form." % (sg(h), sg(k), sg(x), sg(y)), right, w,
               "Use <i>f</i>(<i>x</i>) = <i>a</i>(<i>x</i> − %s)<sup>2</sup> + %s: %s = <i>a</i>(%s)<sup>2</sup> + %s, so <i>a</i> = %s. <b>%s</b>." % (sg(h), sg(k), sg(y), sg(d), sg(k), sg(a), right))


def one_vy(r):
    a, h, k = r.choice(AS), r.choice([n for n in range(-4, 5) if n]), r.randint(-8, 8)
    c = a * h * h + k
    right = vf(a, h, k)
    w = [vf(a, -h, k), vf(c - k, h, k) if c - k != a else vf(-a, h, k), vf(a, h, c)]
    w = [x for x in w if x != right]
    return mcq("A parabola has vertex (%s, %s) and <i>y</i>-intercept %s. Write its equation in vertex form." % (sg(h), sg(k), sg(c)), right, w,
               "Put (0, %s) in: %s = <i>a</i>(0 − %s)<sup>2</sup> + %s = %d<i>a</i> + %s, so <i>a</i> = %s. <b>%s</b>." % (sg(c), sg(c), sg(h), sg(k), h * h, sg(k), sg(a), right))


def one_std(r):
    a, h, k = r.choice(AS), r.choice([n for n in range(-6, 7) if n]), r.randint(-9, 9)
    right = "<i>f</i>(<i>x</i>) = " + poly([a, -2 * a * h, a * h * h + k])
    w = ["<i>f</i>(<i>x</i>) = " + poly([a, -a * h, a * h * h + k]), "<i>f</i>(<i>x</i>) = " + poly([a, 2 * a * h, a * h * h + k]), "<i>f</i>(<i>x</i>) = " + poly([a, -2 * a * h, h * h + k]) if a != 1 else "<i>f</i>(<i>x</i>) = " + poly([a, -2 * a * h, -h * h + k])]
    w = [x for x in w if x != right]
    return mcq("Write %s in standard form." % vf(a, h, k), right, w,
               "(<i>x</i> %s %d)<sup>2</sup> = %s. Multiply by %s and add %s: <b>%s</b>." % (MINUS if h > 0 else "+", abs(h), poly([1, -2 * h, h * h]), sg(a), sg(k), right))


def one_zeros(r):
    r1, r2 = r.sample([n for n in range(-9, 10) if n], 2)
    if r.random() < 0.5:
        right = "<i>f</i>(<i>x</i>) = " + poly([1, -(r1 + r2), r1 * r2])
        w = ["<i>f</i>(<i>x</i>) = " + poly([1, r1 + r2, r1 * r2]), "<i>f</i>(<i>x</i>) = " + poly([1, -(r1 + r2), -r1 * r2]), "<i>f</i>(<i>x</i>) = " + poly([1, r1 + r2, -r1 * r2])]
        q = "A quadratic function with leading coefficient 1 has zeros %s and %s. Write it in standard form." % (sg(r1), sg(r2))
    else:
        right = ff(1, r1, r2)
        w = [ff(1, -r1, -r2), ff(1, r1, -r2), ff(1, -r1, r2)]
        q = "Which quadratic function has zeros %s and %s?" % (sg(r1), sg(r2))
    w = [x for x in w if x != right]
    return mcq(q, right, w, "A zero of %s gives the factor (<i>x</i> − %s). <b>%s</b>." % (sg(r1), sg(r1), right))


def one_zp(r):
    r1, r2 = r.sample(range(-6, 7), 2)
    a = r.choice([2, -2, 3, -3, -1])
    x0 = r.choice([n for n in range(-4, 5) if n not in (r1, r2)])
    y0 = a * (x0 - r1) * (x0 - r2)
    right = ff(a, r1, r2)
    w = [ff(1, r1, r2), ff(-a, r1, r2), ff(a, -r1, -r2)]
    w = [x for x in w if x != right]
    return mcq("A parabola crosses the <i>x</i>-axis at %s and %s and passes through (%s, %s). Write its equation in factored form." % (sg(r1), sg(r2), sg(x0), sg(y0)), right, w,
               "<i>f</i>(<i>x</i>) = <i>a</i>(<i>x</i> − %s)(<i>x</i> − %s). Put in (%s, %s): %s = <i>a</i>(%d), so <i>a</i> = %s. <b>%s</b>." % (sg(r1), sg(r2), sg(x0), sg(y0), sg(y0), (x0 - r1) * (x0 - r2), sg(a), right))


def build():
    sets, R = build_sets([
        ("Vertex and a point: vertex form", [("collect", uniq(one_vp), 20)]),
        ("Vertex and the y-intercept", [("collect", uniq(one_vy), 20)]),
        ("Vertex form to standard form", [("collect", uniq(one_std), 20)]),
        ("From the zeros", [("collect", uniq(one_zeros), 12), ("collect", uniq(one_zp), 8)]),
        ("Vertex form and the graph", [("collect", W(gq.one_vform), 20)]),
    ], 69518)
    finish(sets, R)
    body = lesson('<ul><li><b>Vertex form</b>: <i>f</i>(<i>x</i>) = <i>a</i>(<i>x</i> − <i>h</i>)<sup>2</sup> + <i>k</i>, vertex (<i>h</i>, <i>k</i>).</li><li>Put the vertex in, then use another point to find <i>a</i>.</li><li><b>Standard form</b>: <i>f</i>(<i>x</i>) = <i>ax</i><sup>2</sup> + <i>bx</i> + <i>c</i>. Expand the square to get it.</li><li>A <b>zero</b> at <i>r</i> gives a factor (<i>x</i> − <i>r</i>): zeros 3 and −5 give (<i>x</i> − 3)(<i>x</i> + 5).</li></ul>',
        [example("Vertex (2, −3) through (4, 5)", ["5 = <i>a</i>(4 − 2)<sup>2</sup> − 3", "8 = 4<i>a</i>, <i>a</i> = 2"], "<i>f</i>(<i>x</i>) = 2(<i>x</i> − 2)<sup>2</sup> − 3")],
        [['The wrong sign for <i>h</i>', 'Vertex (2, −3) gives (<i>x</i> − 2).'], ['Finding <i>a</i> without squaring', 'Square (<i>x</i> − <i>h</i>) first.'], ['Writing <i>x</i> + 3 for a zero of 3', 'A zero of 3 gives (<i>x</i> − 3).']])
    faq = [('What does TEKS A.6B ask?', 'Write equations of quadratic functions given the vertex and another point on the graph, write the equation in vertex form (f(x) = a(x − h)<sup>2</sup> + k), and rewrite the equation from vertex form to standard form (f(x) = ax<sup>2</sup> + bx + c).'), ('What does TEKS A.6C ask?', 'Write quadratic functions when given real solutions and graphs of their related equations.'), ('Why is a needed?', 'Many parabolas share a vertex; a sets the width and direction.'), ('What does a negative a mean?', 'The parabola opens down.')]
    make('writing-quadratic-functions', 18, 'Quadratic Functions and Equations', 'A.6B, A.6C',
         'A.6B write equations of quadratic functions given the vertex and another point on the graph, write the equation in vertex form (f(x) = a(x − h)^2 + k), and rewrite the equation from vertex form to standard form (f(x) = ax^2 + bx + c); A.6C write quadratic functions when given real solutions and graphs of their related equations',
         'Writing Quadratic Functions', 'Writing Quadratic Functions',
         'Free Algebra I worksheets for Texas TEKS A.6B and A.6C: write quadratic functions in vertex form from a vertex and a point, convert to standard form and write functions from zeros. 100 questions with answers.',
         'Vertex form: f(x) = a(x − h)² + k.', 'Zeros 3 and −5: f(x) = (x − 3)(x + 5).',
         body, faq, sets, seo_title='Algebra I Writing Quadratic Functions Worksheets (TEKS A.6B, A.6C)')


if __name__ == "__main__":
    build()
