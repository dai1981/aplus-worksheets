# -*- coding: utf-8 -*-
"""
Texas Precalculus: Trigonometric Identities (TEKS P.5L)
  python3 tools/gen_ustx_math_pc_trig_identities.py
Pythagorean, reciprocal and quotient identities, simplifying expressions (US Precalculus makers with a new seed),
cofunction and even/odd identities (own maker), and sum and difference identities for sine and cosine (US Precalculus
maker with a new seed).
Wrong answers come from real mistakes: sin(−θ) = sin θ, cos(90° − θ) = cos θ, and splitting sin(A + B) into sin A + sin B.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_pc_trigonometric_identities as ti
adopt(ti)
ti.R = random.Random(698160)
import gen_us_math_pc_sum_and_difference_formulas as sd
adopt(sd)
sd.R = random.Random(698161)
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


import math


def f4(v):
    return ("%.4f" % v).replace("-", MINUS)


def one_cof(r):
    t = r.randint(5, 85)
    kind = r.choice(["cof", "eo"])
    if kind == "cof":
        fn, co = r.choice([("sin", "cos"), ("cos", "sin"), ("tan", "cot"), ("sec", "csc")])
        F = {"sin": math.sin, "cos": math.cos, "tan": math.tan, "sec": lambda a: 1 / math.cos(a), "csc": lambda a: 1 / math.sin(a), "cot": lambda a: 1 / math.tan(a)}
        v = F[fn](math.radians(t))
        q = "%s %d° ≈ %s. Which is also equal to %s?" % (fn, t, f4(v), f4(v))
        right = "%s %d°" % (co, 90 - t)
        w = ["%s %d°" % (fn, 90 - t), "%s %d°" % (co, t), "%s %d°" % (co, 180 - t)]
        e = "Cofunction identity: %s θ = %s(90° − θ)." % (fn, co)
    elif kind == "eo":
        fn = r.choice(["sin", "cos", "tan"])
        v = {"sin": math.sin, "cos": math.cos, "tan": math.tan}[fn](math.radians(t))
        q = "%s %d° ≈ %s. What is %s(−%d°)?" % (fn, t, f4(v), fn, t)
        right = f4(v) if fn == "cos" else f4(-v)
        w = [f4(-v) if fn == "cos" else f4(v), f4(1 / v), f4(-1 / v)]
        e = "%s is %s: %s(−θ) = %s." % (fn, "even" if fn == "cos" else "odd", fn, "cos θ" if fn == "cos" else "−%s θ" % fn)
    else:
        pick = r.choice([("sin(−θ)", "−sin θ", ["sin θ", "cos θ", "−cos θ"]), ("cos(−θ)", "cos θ", ["−cos θ", "sin θ", "−sin θ"]), ("tan(−θ)", "−tan θ", ["tan θ", "cot θ", "−cot θ"]),
                         ("sin(90° − θ)", "cos θ", ["sin θ", "−cos θ", "−sin θ"]), ("cos(90° − θ)", "sin θ", ["cos θ", "−sin θ", "−cos θ"]), ("tan(90° − θ)", "cot θ", ["tan θ", "−tan θ", "sec θ"]),
                         ("csc(90° − θ)", "sec θ", ["csc θ", "−sec θ", "sin θ"]), ("sec(−θ)", "sec θ", ["−sec θ", "csc θ", "cos θ"]), ("csc(−θ)", "−csc θ", ["csc θ", "sec θ", "−sin θ"]),
                         ("cot(−θ)", "−cot θ", ["cot θ", "tan θ", "−tan θ"])])
        q, right, w = "Which expression is equal to %s?" % pick[0], pick[1], pick[2]
        e = "Use the even/odd and cofunction identities."
    return mcq(q, right, w, e + " <b>%s</b>." % right)


def build():
    sets, R = build_sets([
        ("Pythagorean identities", [("collect", W(ti.one_pyth), 20)]),
        ("Reciprocal, quotient and Pythagorean identities", [("collect", W(ti.one_basic), 20)]),
        ("Cofunction and even/odd identities", [("collect", uniq(one_cof), 20)]),
        ("Simplify expressions", [("collect", W(ti.one_simp), 20)]),
        ("Sum and difference identities", [("collect", W(sd.one_exact), 10), ("collect", W(sd.one_recog), 10)]),
    ], 69816)
    finish(sets, R)
    body = lesson('<ul><li>Reciprocal: csc θ = 1/sin θ, sec θ = 1/cos θ, cot θ = 1/tan θ. Quotient: tan θ = sin θ/cos θ.</li><li>Pythagorean: sin<sup>2</sup> θ + cos<sup>2</sup> θ = 1, 1 + tan<sup>2</sup> θ = sec<sup>2</sup> θ, 1 + cot<sup>2</sup> θ = csc<sup>2</sup> θ.</li><li>Cofunction: sin(90° − θ) = cos θ. Even/odd: cos(−θ) = cos θ, sin(−θ) = −sin θ.</li><li>Sum and difference: sin(<i>A</i> ± <i>B</i>) = sin <i>A</i> cos <i>B</i> ± cos <i>A</i> sin <i>B</i>; cos(<i>A</i> ± <i>B</i>) = cos <i>A</i> cos <i>B</i> ∓ sin <i>A</i> sin <i>B</i>.</li></ul>',
        [example("Simplify sec θ − tan θ sin θ", ["<span class='fr'><span class='fn'>1</span><span class='fd'>cos θ</span></span> − <span class='fr'><span class='fn'>sin<sup>2</sup> θ</span><span class='fd'>cos θ</span></span>", "<span class='fr'><span class='fn'>cos<sup>2</sup> θ</span><span class='fd'>cos θ</span></span>"], "cos θ")],
        [['sin(−θ) = sin θ', 'Sine is odd: sin(−θ) = −sin θ.'], ['cos(90° − θ) = cos θ', 'It equals sin θ.'], ['sin(<i>A</i> + <i>B</i>) = sin <i>A</i> + sin <i>B</i>', 'Use the sum identity.']])
    faq = [('What does TEKS P.5L ask?', 'Use trigonometric identities such as reciprocal, quotient, Pythagorean, cofunctions, even/odd, and sum and difference identities for cosine and sine to simplify trigonometric expressions.'), ('How should I start simplifying?', 'Write everything in sine and cosine.'), ('Why is cosine even?', 'Points at θ and −θ on the unit circle have the same x-coordinate.'), ('Where do the Pythagorean identities come from?', 'x² + y² = 1 on the unit circle.')]
    make('trigonometric-identities', 16, 'Algebraic Reasoning', 'P.5L',
         'P.5L use trigonometric identities such as reciprocal, quotient, Pythagorean, cofunctions, even/odd, and sum and difference identities for cosine and sine to simplify trigonometric expressions',
         'Trigonometric Identities', 'Trigonometric Identities',
         'Free Precalculus worksheets on trigonometric identities for Texas TEKS P.5L: Pythagorean, reciprocal, quotient, cofunction, even/odd and sum and difference identities. 100 questions with answers.',
         'Write everything in sine and cosine.', 'sin² θ + cos² θ = 1.',
         body, faq, sets, seo_title='Precalculus Trigonometric Identities Worksheets (TEKS P.5L)')


if __name__ == "__main__":
    build()
