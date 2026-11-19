# -*- coding: utf-8 -*-
"""
Texas Algebra II: Parabolas: Vertex, Focus and Directrix (TEKS 2A.4B)
  python3 tools/gen_ustx_math_a2_parabolas_focus_directrix.py
Finding the focus, directrix and vertex (US Precalculus maker with a new seed), and writing equations of parabolas
from a focus and directrix, a vertex and focus, or a vertex and directrix, plus axis of symmetry and direction of
opening (own makers).
Wrong answers come from real mistakes: using p instead of 4p, the wrong sign of p, and putting the focus as the vertex.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_pc_conic_sections as cs
adopt(cs)
cs.R = random.Random(697080)
tx_common.GRADE = "algebra-2"

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


Y = "<i>y</i>"


def sh(v, var):
    return var if v == 0 else "(%s %s %d)" % (var, MINUS if v > 0 else "+", abs(v))


def side(c, inner):
    """4p(y − k)"""
    c = Fr(c)
    co = "" if c == 1 else (MINUS if c == -1 else ft(c))
    return co + inner


def peq(h, k, p, vert):
    if vert:
        return "%s<sup>2</sup> = %s" % (sh(h, X), side(4 * p, sh(k, Y)))
    return "%s<sup>2</sup> = %s" % (sh(k, Y), side(4 * p, sh(h, X)))


def P(x, y):
    return "(%s, %s)" % (ft(x), ft(y))


def params(r):
    h, k = r.randint(-6, 6), r.randint(-6, 6)
    p = r.choice([1, 2, 3, 4, -1, -2, -3, -4, Fr(1, 2), Fr(-1, 2)])
    return h, k, Fr(p), r.random() < 0.6


def fd(h, k, p, vert):
    focus = P(h, k + p) if vert else P(h + p, k)
    dirx = ("<i>y</i> = %s" % ft(k - p)) if vert else ("<i>x</i> = %s" % ft(h - p))
    return focus, dirx


def wrongs(h, k, p, vert):
    return [peq(h, k, -p, vert), peq(h, k, p / 4, vert), peq(-h, -k, p, vert), peq(h, k, p, not vert)]


def one_ffd(r):
    h, k, p, vert = params(r)
    focus, dirx = fd(h, k, p, vert)
    right = peq(h, k, p, vert)
    if (h, k) == (0, 0):
        raise AssertionError
    w = wrongs(h, k, p, vert)
    w[2] = peq(h, k + p, p, vert) if vert else peq(h + p, k, p, vert)
    return mcq("Write the equation of the parabola with focus %s and directrix %s." % (focus, dirx), right, w,
               "The vertex is halfway between the focus and the directrix: (%s, %s). The focus is %s %s the vertex, so <i>p</i> = %s and 4<i>p</i> = %s. <b>%s</b>." % (
                   ft(h), ft(k), ft(abs(p)) + (" unit" if abs(p) == 1 else " units"), ("above" if p > 0 else "below") if vert else ("to the right of" if p > 0 else "to the left of"), ft(p), ft(4 * p), right))


def one_vf(r):
    h, k, p, vert = params(r)
    focus, dirx = fd(h, k, p, vert)
    right = peq(h, k, p, vert)
    if r.random() < 0.5:
        q = "Write the equation of the parabola with vertex %s and focus %s." % (P(h, k), focus)
    else:
        q = "Write the equation of the parabola with vertex %s and directrix %s." % (P(h, k), dirx)
    return mcq(q, right, wrongs(h, k, p, vert),
               "<i>p</i> is the directed distance from the vertex to the focus: <i>p</i> = %s. Use %s. <b>%s</b>." % (
                   ft(p), "(<i>x</i> − <i>h</i>)<sup>2</sup> = 4<i>p</i>(<i>y</i> − <i>k</i>)" if vert else "(<i>y</i> − <i>k</i>)<sup>2</sup> = 4<i>p</i>(<i>x</i> − <i>h</i>)", right))


def vform(a, h, k):
    co = "" if a == 1 else (MINUS if a == -1 else ft(a))
    s = "<i>y</i> = %s%s<sup>2</sup>" % (co, sh(h, X))
    if k:
        s += " %s %d" % ("+" if k > 0 else MINUS, abs(k))
    return s


def one_vfd(r):
    h, k = r.randint(-6, 6), r.randint(-6, 6)
    p = Fr(r.choice([1, 2, 3, 4, 5, -1, -2, -3, -4]), r.choice([1, 1, 4]))
    a = 1 / (4 * p)
    if a.denominator > 20 or abs(a) > 2:
        raise AssertionError
    eqn = vform(a, h, k)
    if r.random() < 0.5:
        right = P(h, k + p)
        w = [P(h, k - p), P(h, k + a), P(h + p, k), P(h, k + 4 * p)]
        want = "focus"
    else:
        right = "<i>y</i> = %s" % ft(k - p)
        w = ["<i>y</i> = %s" % ft(k + p), "<i>y</i> = %s" % ft(k - a), "<i>x</i> = %s" % ft(h - p), "<i>y</i> = %s" % ft(k - 4 * p)]
        want = "directrix"
    return mcq("What is the %s of the parabola %s?" % (want, eqn), right, w,
               "<i>a</i> = <span class='fr'><span class='fn'>1</span><span class='fd'>4<i>p</i></span></span>, so 4<i>p</i> = %s and <i>p</i> = %s. The vertex is (%s, %s). <b>%s</b>." % (ft(1 / a), ft(p), sg(h), sg(k), right))


OPEN = {(True, True): "up", (True, False): "down", (False, True): "right", (False, False): "left"}


def one_axis(r):
    h, k, p, vert = params(r)
    axis = ("<i>x</i> = %s" % ft(h)) if vert else ("<i>y</i> = %s" % ft(k))
    d = OPEN[(vert, p > 0)]
    right = "Opens %s; axis of symmetry %s" % (d, axis)
    opp = OPEN[(vert, p < 0)]
    oaxis = ("<i>y</i> = %s" % ft(k)) if vert else ("<i>x</i> = %s" % ft(h))
    w = ["Opens %s; axis of symmetry %s" % (opp, axis), "Opens %s; axis of symmetry %s" % (d, oaxis), "Opens %s; axis of symmetry %s" % (OPEN[(not vert, p > 0)], oaxis)]
    return mcq("Which way does the parabola %s open, and what is its axis of symmetry?" % peq(h, k, p, vert), right, w,
               "The squared variable is %s, so the parabola opens %s. 4<i>p</i> = %s is %s, so it opens %s. The axis passes through the vertex (%s, %s). <b>%s</b>." % (
                   "<i>x</i>" if vert else "<i>y</i>", "up or down" if vert else "left or right", ft(4 * p), "positive" if p > 0 else "negative", d, ft(h), ft(k), right))


def build():
    sets, R = build_sets([
        ("Find the focus, directrix or vertex", [("collect", W(cs.one_par), 20)]),
        ("Equation from the focus and directrix", [("collect", uniq(one_ffd), 20)]),
        ("Equation from the vertex and focus or directrix", [("collect", uniq(one_vf), 20)]),
        ("Focus and directrix of y = a(x − h)² + k", [("collect", uniq(one_vfd), 20)]),
        ("Direction of opening and axis of symmetry", [("collect", uniq(one_axis), 20)]),
    ], 69708)
    finish(sets, R)
    body = lesson("<ul><li>A parabola is the set of points the same distance from a point (the <b>focus</b>) and a line (the <b>directrix</b>).</li><li>The vertex is halfway between the focus and the directrix.</li><li>Opens up or down: (<i>x</i> − <i>h</i>)<sup>2</sup> = 4<i>p</i>(<i>y</i> − <i>k</i>), focus (<i>h</i>, <i>k</i> + <i>p</i>), directrix <i>y</i> = <i>k</i> − <i>p</i>.</li><li>Opens left or right: (<i>y</i> − <i>k</i>)<sup>2</sup> = 4<i>p</i>(<i>x</i> − <i>h</i>), focus (<i>h</i> + <i>p</i>, <i>k</i>), directrix <i>x</i> = <i>h</i> − <i>p</i>.</li><li><i>p</i> &gt; 0 opens up or right; <i>p</i> &lt; 0 opens down or left. In <i>y</i> = <i>a</i>(<i>x</i> − <i>h</i>)<sup>2</sup> + <i>k</i>, <i>a</i> = <span class='fr'><span class='fn'>1</span><span class='fd'>4<i>p</i></span></span>.</li></ul>",
        [example("Focus (2, 5), directrix <i>y</i> = 1", ["Vertex (2, 3)", "<i>p</i> = 2, 4<i>p</i> = 8"], "(<i>x</i> − 2)<sup>2</sup> = 8(<i>y</i> − 3)")],
        [['Using <i>p</i> instead of 4<i>p</i>', 'Multiply <i>p</i> by 4.'], ['The wrong sign of <i>p</i>', 'A focus below the vertex gives <i>p</i> &lt; 0.'], ['Using the focus as the vertex', 'The vertex is halfway between focus and directrix.']])
    faq = [('What does TEKS 2A.4B ask?', 'Write the equation of a parabola using given attributes, including vertex, focus, directrix, axis of symmetry, and direction of opening.'), ('What is p?', 'The directed distance from the vertex to the focus.'), ('Does the parabola pass through the focus?', 'No. The focus is inside the curve.'), ('What is the axis of symmetry?', 'The line through the vertex and the focus.')]
    make('parabolas-focus-and-directrix', 8, 'Quadratic and Square Root Functions, Equations, and Inequalities', '2A.4B',
         '2A.4B write the equation of a parabola using given attributes, including vertex, focus, directrix, axis of symmetry, and direction of opening',
         'Parabolas: Vertex, Focus and Directrix', 'Focus and Directrix',
         'Free Algebra II worksheets for Texas TEKS 2A.4B: vertex, focus and directrix of parabolas, writing equations, axis of symmetry and direction of opening. 100 questions with answers.',
         '(x − h)² = 4p(y − k): focus (h, k + p), directrix y = k − p.', 'The vertex is halfway between the focus and the directrix.',
         body, faq, sets, seo_title='Algebra II Parabolas: Focus and Directrix Worksheets (TEKS 2A.4B)')


if __name__ == "__main__":
    build()
