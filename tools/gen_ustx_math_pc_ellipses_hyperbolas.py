# -*- coding: utf-8 -*-
"""
Texas Precalculus: Ellipses and Hyperbolas with Center (h, k) (TEKS P.3H, P.3I)
  python3 tools/gen_ustx_math_pc_ellipses_hyperbolas.py
Features of ellipses and hyperbolas (US Precalculus makers with a new seed), and writing equations of ellipses and
hyperbolas with center (h, k) from vertices, co-vertices and foci, and asymptotes of hyperbolas (own makers).
Wrong answers come from real mistakes: putting a² under the wrong variable, c² = a² + b² for an ellipse, and the wrong
signs for the center.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_pc_conic_sections as cs
adopt(cs)
cs.R = random.Random(698240)
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


Y = "<i>y</i>"


def sh(v, var):
    return var if v == 0 else "(%s %s %d)" % (var, MINUS if v > 0 else "+", abs(v))


def F(top, den):
    return "<span class='fr'><span class='fn'>%s<sup>2</sup></span><span class='fd'>%d</span></span>" % (top, den)


def eq(h, k, xx, yy, minus=False):
    return "%s %s %s = 1" % (F(sh(h, X), xx), MINUS if minus else "+", F(sh(k, Y), yy))


def heq(h, k, a2, b2, horiz):
    if horiz:
        return "%s − %s = 1" % (F(sh(h, X), a2), F(sh(k, Y), b2))
    return "%s − %s = 1" % (F(sh(k, Y), a2), F(sh(h, X), b2))


def P(x, y):
    return "(%s, %s)" % (sg(x), sg(y))


TRI = [(5, 4, 3), (5, 3, 4), (10, 8, 6), (10, 6, 8), (13, 12, 5), (13, 5, 12), (4, 3, None), (6, 4, None), (7, 2, None), (3, 2, None), (9, 5, None)]


def one_wel(r):
    h, k = r.randint(-6, 6), r.randint(-6, 6)
    a, b, c = r.choice(TRI)
    horiz = r.random() < 0.5
    A2, B2 = a * a, b * b
    right = eq(h, k, A2, B2) if horiz else eq(h, k, B2, A2)
    if c and r.random() < 0.5:
        info = "center %s, a vertex at %s and a focus at %s" % (P(h, k), P(h + a, k) if horiz else P(h, k + a), P(h + c, k) if horiz else P(h, k + c))
        e = "<i>a</i> = %d (center to vertex), <i>c</i> = %d (center to focus), <i>b</i><sup>2</sup> = <i>a</i><sup>2</sup> − <i>c</i><sup>2</sup> = %d." % (a, c, B2)
    else:
        info = "vertices %s and %s and co-vertices %s and %s" % ((P(h - a, k), P(h + a, k), P(h, k - b), P(h, k + b)) if horiz else (P(h, k - a), P(h, k + a), P(h - b, k), P(h + b, k)))
        e = "The center is the midpoint %s; <i>a</i> = %d along the %s major axis and <i>b</i> = %d." % (P(h, k), a, "horizontal" if horiz else "vertical", b)
    w = [eq(h, k, B2, A2) if horiz else eq(h, k, A2, B2), eq(-h, -k, A2, B2) if horiz else eq(-h, -k, B2, A2), eq(h, k, a, b) if horiz else eq(h, k, b, a)]
    w = [v for v in dict.fromkeys(w) if v != right]
    if len(w) < 3:
        w.append(eq(h, k, A2, B2, True))
    return mcq("Write the equation of the ellipse with %s." % info, right, w, e + " <b>%s</b>." % right)


HTRI = [(3, 4, 5), (4, 3, 5), (6, 8, 10), (8, 6, 10), (5, 12, 13), (12, 5, 13), (8, 15, 17)]


def one_why(r):
    h, k = r.randint(-6, 6), r.randint(-6, 6)
    a, b, c = r.choice(HTRI)
    horiz = r.random() < 0.5
    right = heq(h, k, a * a, b * b, horiz)
    info = "vertices %s and %s and foci %s and %s" % ((P(h - a, k), P(h + a, k), P(h - c, k), P(h + c, k)) if horiz else (P(h, k - a), P(h, k + a), P(h, k - c), P(h, k + c)))
    w = [heq(h, k, a * a, c * c, horiz), heq(h, k, a * a, b * b, not horiz), heq(-h, -k, a * a, b * b, horiz) if (h, k) != (0, 0) else heq(h, k, b * b, a * a, horiz)]
    w = [v for v in dict.fromkeys(w) if v != right]
    if len(w) < 3:
        w.append(heq(h, k, b * b, a * a, horiz))
    return mcq("Write the equation of the hyperbola with %s." % info, right, w,
               "Center %s, <i>a</i> = %d, <i>c</i> = %d. For a hyperbola <i>b</i><sup>2</sup> = <i>c</i><sup>2</sup> − <i>a</i><sup>2</sup> = %d. The %s term comes first. <b>%s</b>." % (
                   P(h, k), a, c, b * b, "<i>x</i>" if horiz else "<i>y</i>", right))


def one_asy(r):
    h, k = r.randint(-6, 6), r.randint(-6, 6)
    a, b = r.sample([1, 2, 3, 4, 5, 6], 2)
    horiz = r.random() < 0.5
    f = heq(h, k, a * a, b * b, horiz)
    m = Fr(b, a) if horiz else Fr(a, b)
    def ln(mm):
        mt = "" if mm == 1 else ft(mm)
        return "<i>y</i> %s = ±%s%s" % ("− %d" % k if k > 0 else ("+ %d" % -k if k < 0 else ""), mt, sh(h, X))
    right = ln(m).replace("<i>y</i>  =", "<i>y</i> =")
    w = [ln(1 / m), ln(m * m) if m * m != m else ln(m + 1), ln(Fr(a * a, b * b) if horiz else Fr(b * b, a * a))]
    w = [v.replace("<i>y</i>  =", "<i>y</i> =") for v in dict.fromkeys(w) if v != ln(m)]
    if len(w) < 3:
        w.append(ln(m + 2).replace("<i>y</i>  =", "<i>y</i> ="))
    return mcq("What are the asymptotes of the hyperbola %s?" % f, right, w,
               "The slopes are ±%s: %s. They pass through the center (%s, %s). <b>%s</b>." % (ft(m), "rise <i>b</i> over run <i>a</i> for a horizontal hyperbola" if horiz else "<i>a</i> over <i>b</i> for a vertical hyperbola", sg(h), sg(k), right))


def build():
    sets, R = build_sets([
        ("Features of ellipses", [("collect", W(cs.one_ell), 20)]),
        ("Write the equation of an ellipse", [("collect", uniq(one_wel), 20)]),
        ("Features of hyperbolas", [("collect", W(cs.one_hyp), 20)]),
        ("Write the equation of a hyperbola", [("collect", uniq(one_why), 20)]),
        ("Asymptotes of hyperbolas", [("collect", uniq(one_asy), 20)]),
    ], 69824)
    finish(sets, R)
    body = lesson("<ul><li>Ellipse with center (<i>h</i>, <i>k</i>): <span class='fr'><span class='fn'>(<i>x</i> − <i>h</i>)<sup>2</sup></span><span class='fd'><i>a</i><sup>2</sup></span></span> + <span class='fr'><span class='fn'>(<i>y</i> − <i>k</i>)<sup>2</sup></span><span class='fd'><i>b</i><sup>2</sup></span></span> = 1 (horizontal major axis). The bigger denominator is <i>a</i><sup>2</sup>. <i>c</i><sup>2</sup> = <i>a</i><sup>2</sup> − <i>b</i><sup>2</sup>.</li><li>Hyperbola: <span class='fr'><span class='fn'>(<i>x</i> − <i>h</i>)<sup>2</sup></span><span class='fd'><i>a</i><sup>2</sup></span></span> − <span class='fr'><span class='fn'>(<i>y</i> − <i>k</i>)<sup>2</sup></span><span class='fd'><i>b</i><sup>2</sup></span></span> = 1 opens left and right. <i>c</i><sup>2</sup> = <i>a</i><sup>2</sup> + <i>b</i><sup>2</sup>.</li><li><i>a</i> is the distance from the center to a vertex; <i>c</i> is the distance to a focus.</li><li>Asymptotes of a horizontal hyperbola: <i>y</i> − <i>k</i> = ±<span class='fr'><span class='fn'><i>b</i></span><span class='fd'><i>a</i></span></span>(<i>x</i> − <i>h</i>).</li></ul>",
        [example("Vertices (−1, 2) and (7, 2), foci (−2, 2) and (8, 2)", ["Center (3, 2), <i>a</i> = 4, <i>c</i> = 5", "Hyperbola: <i>b</i><sup>2</sup> = 25 − 16 = 9"], "<span class='fr'><span class='fn'>(<i>x</i> − 3)<sup>2</sup></span><span class='fd'>16</span></span> − <span class='fr'><span class='fn'>(<i>y</i> − 2)<sup>2</sup></span><span class='fd'>9</span></span> = 1")],
        [['<i>a</i><sup>2</sup> under the wrong variable', '<i>a</i> goes with the axis through the vertices.'], ['<i>c</i><sup>2</sup> = <i>a</i><sup>2</sup> + <i>b</i><sup>2</sup> for an ellipse', 'Ellipse: minus. Hyperbola: plus.'], ['The wrong signs for the center', 'Center (3, −2) gives (<i>x</i> − 3) and (<i>y</i> + 2).']])
    faq = [('What does TEKS P.3H ask?', 'Use the characteristics of an ellipse to write the equation of an ellipse with center (h, k).'), ('What does TEKS P.3I ask?', 'Use the characteristics of a hyperbola to write the equation of a hyperbola with center (h, k).'), ('How can I tell an ellipse from a hyperbola?', 'Ellipse: plus between the terms. Hyperbola: minus.'), ('Which way does a hyperbola open?', 'Toward the variable whose term is positive.')]
    make('ellipses-and-hyperbolas', 24, 'Relations and Geometric Reasoning', 'P.3H, P.3I',
         'P.3H use the characteristics of an ellipse to write the equation of an ellipse with center (h, k); P.3I use the characteristics of a hyperbola to write the equation of a hyperbola with center (h, k)',
         'Ellipses and Hyperbolas with Center (h, k)', 'Ellipses and Hyperbolas',
         'Free Precalculus worksheets on ellipses and hyperbolas for Texas TEKS P.3H and P.3I: vertices, foci, writing equations with center (h, k) and asymptotes. 100 questions with answers.',
         'Ellipse: c² = a² − b². Hyperbola: c² = a² + b².', 'a is the distance from the center to a vertex.',
         body, faq, sets, seo_title='Precalculus Ellipses and Hyperbolas Worksheets (TEKS P.3H, P.3I)')


if __name__ == "__main__":
    build()
