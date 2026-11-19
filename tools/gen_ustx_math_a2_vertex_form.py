# -*- coding: utf-8 -*-
"""
Texas Algebra II: Completing the Square and Vertex Form (TEKS 2A.4D)
  python3 tools/gen_ustx_math_a2_vertex_form.py
Rewriting f(x) = ax² + bx + c as f(x) = a(x − h)² + k by completing the square (a = 1 and a ≠ 1), finding the vertex
with x = −b/(2a), reading attributes from vertex form, and expanding vertex form (own makers).
Wrong answers come from real mistakes: the wrong sign of h, forgetting to multiply the added square by a, and
subtracting instead of adding k.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)

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


def vf(a, h, k):
    co = "" if a == 1 else (MINUS if a == -1 else sg(a))
    s = "%s(%s)<sup>2</sup>" % (co, X if h == 0 else "%s %s %d" % (X, MINUS if h > 0 else "+", abs(h)))
    if k:
        s += " %s %d" % ("+" if k > 0 else MINUS, abs(k))
    return fx(s)


def sf_(a, h, k):
    return fx(poly([a, -2 * a * h, a * h * h + k]))


def hk(r):
    return r.choice([n for n in range(-7, 8) if n]), r.choice([n for n in range(-12, 13) if n])


def one_cs1(r):
    h, k = hk(r)
    c = h * h + k
    right = vf(1, h, k)
    w = [vf(1, -h, k), vf(1, h, c - 2 * h * h) if c - 2 * h * h != k else vf(1, h, k + 1), vf(1, h, -k), vf(1, h, c + h * h)]
    return mcq("Complete the square to write %s in vertex form." % sf_(1, h, k), right, w,
               "Half of %s is %s, and (%s)<sup>2</sup> = %d. Add and subtract %d: (<i>x</i> %s %d)<sup>2</sup> %s %d − %d = <b>%s</b>." % (
                   sg(-2 * h), sg(-h), sg(-h), h * h, h * h, MINUS if h > 0 else "+", abs(h), "+" if c >= 0 else MINUS, abs(c), h * h, right[right.index("= ") + 2:]))


def one_cs2(r):
    a = r.choice([2, 3, 4, -1, -2, -3])
    h, k = hk(r)
    if abs(a * h * h + k) > 150:
        raise AssertionError
    c = a * h * h + k
    right = vf(a, h, k)
    w = [vf(a, h, c - h * h), vf(a, -h, k), vf(a, h, c + a * h * h), vf(1, h, k) if a != 1 else vf(2, h, k)]
    w = [v for v in w if v != right]
    return mcq("Write %s in vertex form." % sf_(a, h, k), right, w,
               "Factor %s from the <i>x</i>-terms: %s(<i>x</i><sup>2</sup> %s %d<i>x</i>) %s %d. Complete the square inside: add %d inside, which adds %s, so subtract %s. <b>%s</b>." % (
                   sg(a), sg(a), MINUS if h > 0 else "+", abs(2 * h), "+" if c >= 0 else MINUS, abs(c), h * h, sg(a * h * h), sg(a * h * h), right[right.index("= ") + 2:]))


def P(x, y):
    return "(%s, %s)" % (ft(x), ft(y))


def one_vtx(r):
    a = r.choice([1, 2, -1, -2, 3, -3, 4])
    h, k = hk(r)
    b, c = -2 * a * h, a * h * h + k
    if abs(c) > 150:
        raise AssertionError
    right = P(h, k)
    w = [P(-h, k), P(h, c), P(Fr(-b, a), k), P(h, -k)]
    return mcq("What is the vertex of the graph of %s?" % sf_(a, h, k), right, w,
               "<i>x</i> = −<i>b</i> ÷ (2<i>a</i>) = −(%s) ÷ %s = %s. <i>f</i>(%s) = %s. <b>%s</b>." % (sg(b), "(%s)" % sg(2 * a) if a < 0 else sg(2 * a), sg(h), sg(h), sg(k), right))


def one_attr(r):
    a = r.choice([1, 2, -1, -2, 3, -3])
    h, k = hk(r)
    if abs(a * h * h + k) > 150:
        raise AssertionError
    f = sf_(a, h, k)
    kind = r.choice(["axis", "ext", "range"])
    if kind == "axis":
        right = "<i>x</i> = %s" % sg(h)
        w = ["<i>x</i> = %s" % sg(-h), "<i>y</i> = %s" % sg(k), "<i>x</i> = %s" % sg(k)]
        q = "Write %s in vertex form. What is its axis of symmetry?" % f
    elif kind == "ext":
        mm = "minimum" if a > 0 else "maximum"
        right = "%s value %s" % (mm.capitalize(), sg(k))
        w = ["%s value %s" % ("Maximum" if a > 0 else "Minimum", sg(k)), "%s value %s" % (mm.capitalize(), sg(h)), "%s value %s" % (mm.capitalize(), sg(a * h * h + k))]
        q = "Write %s in vertex form. Does it have a maximum or a minimum value, and what is it?" % f
    else:
        right = ("<i>y</i> ≥ %s" if a > 0 else "<i>y</i> ≤ %s") % sg(k)
        w = [("<i>y</i> ≤ %s" if a > 0 else "<i>y</i> ≥ %s") % sg(k), ("<i>y</i> ≥ %s" if a > 0 else "<i>y</i> ≤ %s") % sg(h), "All real numbers"]
        q = "Write %s in vertex form. What is its range?" % f
    return mcq(q, right, w, "%s, so the vertex is (%s, %s) and the parabola opens %s. <b>%s</b>." % (vf(a, h, k), sg(h), sg(k), "up" if a > 0 else "down", right))


def one_exp(r):
    a = r.choice([1, 2, -1, -2, 3, -3, 4, -4])
    h, k = hk(r)
    if abs(a * h * h + k) > 200:
        raise AssertionError
    right = sf_(a, h, k)
    w = [fx(poly([a, -2 * a * h, h * h + k])), fx(poly([a, 2 * a * h, a * h * h + k])), fx(poly([a, -a * h, a * h * h + k])), fx(poly([a, -2 * a * h, a * h * h - k]))]
    w = [v for v in dict.fromkeys(w) if v != right]
    return mcq("Write %s in standard form." % vf(a, h, k), right, w,
               "(<i>x</i> %s %d)<sup>2</sup> = %s. Multiply by %s and add %s: <b>%s</b>." % (MINUS if h > 0 else "+", abs(h), poly([1, -2 * h, h * h]), sg(a), sg(k), right[right.index("= ") + 2:]))


def build():
    sets, R = build_sets([
        ("Complete the square: x² + bx + c", [("collect", uniq(one_cs1), 20)]),
        ("Complete the square: ax² + bx + c", [("collect", uniq(one_cs2), 20)]),
        ("Find the vertex", [("collect", uniq(one_vtx), 20)]),
        ("Attributes from vertex form", [("collect", uniq(one_attr), 20)]),
        ("Vertex form to standard form", [("collect", uniq(one_exp), 20)]),
    ], 69709)
    finish(sets, R)
    body = lesson('<ul><li>Vertex form: <i>f</i>(<i>x</i>) = <i>a</i>(<i>x</i> − <i>h</i>)<sup>2</sup> + <i>k</i>. The vertex is (<i>h</i>, <i>k</i>) and the axis of symmetry is <i>x</i> = <i>h</i>.</li><li>To complete the square for <i>x</i><sup>2</sup> + <i>bx</i>, add and subtract (<i>b</i> ÷ 2)<sup>2</sup>.</li><li>If <i>a</i> ≠ 1, factor <i>a</i> out of the <i>x</i>-terms first. The square you add inside is worth <i>a</i> times as much outside.</li><li><i>a</i> &gt; 0: minimum value <i>k</i>. <i>a</i> &lt; 0: maximum value <i>k</i>.</li></ul>',
        [example("<i>f</i>(<i>x</i>) = <i>x</i><sup>2</sup> − 6<i>x</i> + 11", ["(−6 ÷ 2)<sup>2</sup> = 9", "<i>x</i><sup>2</sup> − 6<i>x</i> + 9 − 9 + 11"], "(<i>x</i> − 3)<sup>2</sup> + 2, vertex (3, 2)"), example("<i>f</i>(<i>x</i>) = 2<i>x</i><sup>2</sup> + 8<i>x</i> + 3", ["2(<i>x</i><sup>2</sup> + 4<i>x</i> + 4) + 3 − 8"], "2(<i>x</i> + 2)<sup>2</sup> − 5")],
        [['The wrong sign of <i>h</i>', '(<i>x</i> − 3)<sup>2</sup> has <i>h</i> = 3; (<i>x</i> + 3)<sup>2</sup> has <i>h</i> = −3.'], ['Forgetting to multiply by <i>a</i>', 'Adding 4 inside 2( ) adds 8.'], ['Adding the square without subtracting it', 'Add and subtract the same amount.']])
    faq = [('What does TEKS 2A.4D ask?', 'Transform a quadratic function f(x) = ax² + bx + c to the form f(x) = a(x − h)² + k to identify the different attributes of f(x).'), ('Why use vertex form?', 'It shows the vertex, axis of symmetry and maximum or minimum right away.'), ('Is there a shortcut for the vertex?', 'Yes: x = −b ÷ (2a), then find f of that value.'), ('Does a change when you complete the square?', 'No. a is the same in both forms.')]
    make('completing-the-square-and-vertex-form', 9, 'Quadratic and Square Root Functions, Equations, and Inequalities', '2A.4D',
         '2A.4D transform a quadratic function f(x) = ax^2 + bx + c to the form f(x) = a(x − h)^2 + k to identify the different attributes of f(x)',
         'Completing the Square and Vertex Form', 'Vertex Form',
         'Free Algebra II worksheets for Texas TEKS 2A.4D: complete the square, write quadratics in vertex form, find the vertex, axis, maximum or minimum and range. 100 questions with answers.',
         'f(x) = a(x − h)² + k has vertex (h, k).', 'Complete the square: add and subtract (b ÷ 2)².',
         body, faq, sets, seo_title='Algebra II Completing the Square and Vertex Form Worksheets (TEKS 2A.4D)')


if __name__ == "__main__":
    build()
