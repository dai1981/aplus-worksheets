# -*- coding: utf-8 -*-
"""
Texas Precalculus: Composition of Functions (TEKS P.2A, P.2B, P.2C)
  python3 tools/gen_ustx_math_pc_composition.py
Evaluating and writing compositions (US Algebra 2 makers with a new seed), showing that composition is not always
commutative, decomposing a function into an outer and an inner function, and composition in real situations (own makers).
Wrong answers come from real mistakes: working from the outside in, swapping the outer and inner functions, and
applying the steps in the wrong order.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_a2_composition_and_inverse_functions as ci
adopt(ci)
ci.R = random.Random(698010)
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


def lin_(a, b):
    return poly([a, b])


def one_nc(r):
    a, b = r.choice([2, 3, 4, -2, -3, 5]), r.choice([n for n in range(-6, 7) if n])
    c = r.choice([n for n in range(-6, 7) if n])
    k = r.choice([n for n in range(-4, 5) if n])
    f = fx(lin_(a, b))
    g = fx(X + "<sup>2</sup> %s %d" % ("+" if c > 0 else MINUS, abs(c)), "g")
    fg = a * (k * k + c) + b
    gf = (a * k + b) ** 2 + c
    if fg == gf:
        raise AssertionError
    T = lambda p, q: "<i>f</i>(<i>g</i>(%s)) = %s and <i>g</i>(<i>f</i>(%s)) = %s" % (sg(k), sg(p), sg(k), sg(q))
    right = T(fg, gf)
    w = [T(gf, fg), T(fg, fg), T(gf, gf)]
    return mcq("%s and %s. Find <i>f</i>(<i>g</i>(%s)) and <i>g</i>(<i>f</i>(%s))." % (f, g, sg(k), sg(k)), right, w,
               "<i>g</i>(%s) = %s, so <i>f</i>(<i>g</i>(%s)) = <i>f</i>(%s) = %s. <i>f</i>(%s) = %s, so <i>g</i>(<i>f</i>(%s)) = <i>g</i>(%s) = %s. The order matters: composition is not commutative. <b>%s</b>." % (
                   sg(k), sg(k * k + c), sg(k), sg(k * k + c), sg(fg), sg(k), sg(a * k + b), sg(k), sg(a * k + b), sg(gf), right))


OUT = [("cube", lambda u: "(%s)<sup>3</sup>" % u, "<i>x</i><sup>3</sup>"), ("sq", lambda u: "(%s)<sup>2</sup>" % u, "<i>x</i><sup>2</sup>"),
       ("root", lambda u: "√(%s)" % u, "√<i>x</i>"), ("rec", lambda u: "<span class='fr'><span class='fn'>1</span><span class='fd'>%s</span></span>" % u, "<span class='fr'><span class='fn'>1</span><span class='fd'><i>x</i></span></span>"),
       ("abs", lambda u: "|%s|" % u, "|<i>x</i>|"), ("exp", lambda u: "2<sup>%s</sup>" % u, "2<sup><i>x</i></sup>"), ("log", lambda u: "log(%s)" % u, "log <i>x</i>")]


def one_dec(r):
    key, outer, otxt = r.choice(OUT)
    a = r.choice([2, 3, 4, 5, -2, -3])
    b = r.choice([n for n in range(-9, 10) if n])
    inner = poly([a, b])
    h = "<i>h</i>(<i>x</i>) = " + outer(inner)
    P = lambda f_, g_: "<i>f</i>(<i>x</i>) = %s, <i>g</i>(<i>x</i>) = %s" % (f_, g_)
    right = P(otxt, inner)
    w = [P(inner, otxt), P(otxt, poly([a, 0])), P(otxt.replace("<i>x</i>", "<i>x</i>") if False else otxt + " %s %d" % ("+" if b > 0 else MINUS, abs(b)), poly([a, 0]))]
    return mcq("%s. Which functions <i>f</i> and <i>g</i> give <i>h</i>(<i>x</i>) = <i>f</i>(<i>g</i>(<i>x</i>))?" % h, right, w,
               "The inner function <i>g</i> is what you do first (%s); the outer function <i>f</i> is what you do to the result. Check: <i>f</i>(<i>g</i>(<i>x</i>)) = %s. <b>%s</b>." % (inner, outer(inner), right))


def money(v):
    c = int(round(v * 100))
    return "$%s.%02d" % (comma(c // 100), c % 100)


def one_cw(r):
    kind = r.choice(["shop", "shop", "spill", "cur", "temp"])
    if kind == "shop":
        p = r.choice([10, 15, 20, 25, 30, 40])
        d = r.choice([5, 10, 15, 20])
        P = r.choice([40, 60, 80, 120, 150, 200, 250])
        g = (100 - p) / 100 * P
        q = "A store takes %d%% off a price, <i>g</i>(<i>x</i>) = %s<i>x</i>, and a coupon takes $%d off, <i>f</i>(<i>x</i>) = <i>x</i> − %d. What is <i>f</i>(<i>g</i>(%d)), the price of a $%d jacket when the coupon is used after the discount?" % (p, "%.2f" % ((100 - p) / 100), d, d, P, P)
        right = money(g - d)
        w = [money((100 - p) / 100 * (P - d)), money(P - d - p) if P - d - p > 0 else money(g), money(P - d)]
        e = "<i>g</i>(%d) = %s, then <i>f</i>(%s) = %s − %d = %s. (Using the coupon first gives <i>g</i>(<i>f</i>(%d)) = %s.)" % (P, money(g), money(g)[1:], money(g)[1:], d, right, P, money((100 - p) / 100 * (P - d)))
    elif kind == "spill":
        v = r.choice([2, 3, 4, 5, 6, 8, 10])
        t = r.choice([2, 3, 4, 5, 6])
        q = "The radius of an oil spill is <i>r</i>(<i>t</i>) = %d<i>t</i> meters after <i>t</i> hours, and the area of a circle is <i>A</i>(<i>r</i>) = π<i>r</i><sup>2</sup>. What is <i>A</i>(<i>r</i>(%d))?" % (v, t)
        right = "%sπ square meters" % comma((v * t) ** 2)
        w = ["%sπ square meters" % comma(v * t * t), "%sπ square meters" % comma(2 * v * t), "%sπ square meters" % comma(v * v * t)]
        e = "<i>r</i>(%d) = %d, then <i>A</i>(%d) = π(%d)<sup>2</sup> = %sπ." % (t, v * t, v * t, v * t, comma((v * t) ** 2))
    elif kind == "cur":
        a = r.choice([0.8, 0.9, 0.85, 0.75])
        b = r.choice([150, 160, 120, 140])
        x = r.choice([50, 100, 200, 250, 400])
        q = "One US dollar buys %.2f euros: <i>e</i>(<i>d</i>) = %.2f<i>d</i>. One euro buys %d yen: <i>y</i>(<i>e</i>) = %d<i>e</i>. How many yen is <i>y</i>(<i>e</i>(%d))?" % (a, a, b, b, x)
        val = a * x * b
        right = "%s yen" % comma(int(round(val)))
        w = ["%s yen" % comma(int(round(x * b / a))), "%s yen" % comma(int(round(a * x + b))), "%s yen" % comma(int(round(x * b)))]
        e = "<i>e</i>(%d) = %s euros, then <i>y</i>(%s) = %s yen." % (x, ("%.2f" % (a * x)).rstrip("0").rstrip("."), ("%.2f" % (a * x)).rstrip("0").rstrip("."), comma(int(round(val))))
    else:
        F = r.choice([32, 50, 68, 86, 104, 212, 14, -4])
        C = (F - 32) * 5 // 9
        q = "<i>C</i>(<i>F</i>) = <span class='fr'><span class='fn'>5</span><span class='fd'>9</span></span>(<i>F</i> − 32) changes °F to °C, and <i>K</i>(<i>C</i>) = <i>C</i> + 273 changes °C to kelvins. Find <i>K</i>(<i>C</i>(%s))." % sg(F)
        right = "%d K" % (C + 273)
        w = ["%d K" % (F + 273), "%d K" % (C + 273 + 32) if C + 305 != F + 273 else "%d K" % (C + 300), "%s K" % sg(C - 273)]
        e = "<i>C</i>(%s) = %s, then <i>K</i>(%s) = %s + 273 = %d." % (sg(F), sg(C), sg(C), sg(C), C + 273)
    return mcq(q, right, w, e + " <b>%s</b>." % right)


def build():
    sets, R = build_sets([
        ("Evaluate compositions", [("collect", W(ci.one_eval), 20)]),
        ("Write compositions", [("collect", W(ci.one_comp), 20)]),
        ("Is composition commutative?", [("collect", uniq(one_nc), 20)]),
        ("Decompose a function", [("collect", uniq(one_dec), 20)]),
        ("Composition in context", [("collect", uniq(one_cw), 20)]),
    ], 69801)
    finish(sets, R)
    body = lesson('<ul><li>(<i>f</i> ∘ <i>g</i>)(<i>x</i>) = <i>f</i>(<i>g</i>(<i>x</i>)): do <i>g</i> first, then put the result into <i>f</i>.</li><li>Composition is <b>not</b> always commutative: <i>f</i>(<i>g</i>(<i>x</i>)) and <i>g</i>(<i>f</i>(<i>x</i>)) are usually different.</li><li>To decompose <i>h</i>, look for an inner expression. In (2<i>x</i> + 1)<sup>3</sup>, the inner function is 2<i>x</i> + 1 and the outer function is <i>x</i><sup>3</sup>.</li><li>In real situations, the output of the first step is the input of the second.</li></ul>',
        [example("<i>f</i>(<i>x</i>) = 2<i>x</i> + 1, <i>g</i>(<i>x</i>) = <i>x</i><sup>2</sup>", ["<i>f</i>(<i>g</i>(3)) = <i>f</i>(9) = 19", "<i>g</i>(<i>f</i>(3)) = <i>g</i>(7) = 49"], "19 ≠ 49")],
        [['Working from the outside in', 'Start with the inner function.'], ['Swapping <i>f</i> and <i>g</i>', '<i>f</i>(<i>g</i>(<i>x</i>)): <i>g</i> is inside.'], ['Assuming the order does not matter', 'Check both orders: they are usually different.']])
    faq = [('What does TEKS P.2A ask?', 'Use the composition of two functions to model and solve real-world problems.'), ('What does TEKS P.2B ask?', 'Demonstrate that function composition is not always commutative.'), ('What does TEKS P.2C ask?', 'Represent a given function as a composite function of two or more functions.'), ('Is there more than one way to decompose a function?', 'Yes. Any pair that gives the same h works; the usual choice uses a clear inner expression.')]
    make('composition-of-functions', 1, 'Functions', 'P.2A, P.2B, P.2C',
         'P.2A use the composition of two functions to model and solve real-world problems; P.2B demonstrate that function composition is not always commutative; P.2C represent a given function as a composite function of two or more functions',
         'Composition of Functions', 'Composition of Functions',
         'Free Precalculus worksheets on composition of functions for Texas TEKS P.2A to P.2C: evaluate and write f(g(x)), order of composition, decomposing functions and real-world composition. 100 questions with answers.',
         'f(g(x)): do g first, then f.', 'f(g(x)) and g(f(x)) are usually different.',
         body, faq, sets, seo_title='Precalculus Composition of Functions Worksheets (TEKS P.2A–P.2C)')


if __name__ == "__main__":
    build()
