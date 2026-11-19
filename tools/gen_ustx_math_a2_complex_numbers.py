# -*- coding: utf-8 -*-
"""
Texas Algebra II: Adding, Subtracting and Multiplying Complex Numbers (TEKS 2A.7A)
  python3 tools/gen_ustx_math_a2_complex_numbers.py
Powers of i and square roots of negatives, adding and multiplying complex numbers (US Algebra 2 makers with a new
seed), and subtracting, squaring, conjugate products and mixed expressions (own makers).
Wrong answers come from real mistakes: using i² = 1, subtracting only the real parts, and squaring each part
separately.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_a2_complex_numbers as cx
adopt(cx)
cx.R = random.Random(697190)
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


I = "<i>i</i>"


def cs(a, b):
    if b == 0:
        return sg(a)
    bi = (I if b == 1 else MINUS + I if b == -1 else sg(b) + I)
    if a == 0:
        return bi
    return "%s %s %s" % (sg(a), "+" if b > 0 else MINUS, (I if abs(b) == 1 else str(abs(b)) + I))


def rz(r):
    return r.choice([n for n in range(-9, 10) if n]), r.choice([n for n in range(-9, 10) if n])


def one_sub(r):
    a, b = rz(r)
    c, d = rz(r)
    right = cs(a - c, b - d)
    w = [cs(a - c, b + d), cs(a + c, b - d), cs(a - c, d - b), cs(a + c, b + d)]
    w = [v for v in dict.fromkeys(w) if v != right]
    return mcq("Simplify (%s) − (%s)." % (cs(a, b), cs(c, d)), right, w,
               "Subtract real parts and imaginary parts: (%s − %s) + (%s − %s)%s = <b>%s</b>." % (sg(a), "(%s)" % sg(c) if c < 0 else sg(c), sg(b), "(%s)" % sg(d) if d < 0 else sg(d), I, right))


def one_sq(r):
    a, b = rz(r)
    kind = r.choice(["sq", "conj", "itimes"])
    if kind == "sq":
        right = cs(a * a - b * b, 2 * a * b)
        w = [cs(a * a + b * b, 2 * a * b), cs(a * a - b * b, 0), cs(a * a, b * b) if b * b else cs(a * a, 1), cs(a * a - b * b, a * b)]
        q = "Simplify (%s)<sup>2</sup>." % cs(a, b)
        e = "(%s)(%s) = %d %s %d%s + %d%s<sup>2</sup> = %d %s %d%s − %d." % (cs(a, b), cs(a, b), a * a, "+" if 2 * a * b > 0 else MINUS, abs(2 * a * b), I, b * b, I, a * a, "+" if 2 * a * b > 0 else MINUS, abs(2 * a * b), I, b * b)
    elif kind == "conj":
        right = str(a * a + b * b)
        w = [sg(a * a - b * b), cs(a * a, -b * b), cs(a * a + b * b, 2 * a * b), str(a * a + b * b + 1)]
        q = "Simplify (%s)(%s)." % (cs(a, b), cs(a, -b))
        e = "These are conjugates: (<i>a</i> + <i>bi</i>)(<i>a</i> − <i>bi</i>) = <i>a</i><sup>2</sup> + <i>b</i><sup>2</sup> = %d + %d." % (a * a, b * b)
    else:
        right = cs(-b, a)
        w = [cs(b, a), cs(-b, -a), cs(a, -b), cs(b, -a)]
        q = "Simplify %s(%s)." % (I, cs(a, b))
        e = "%s · %s = %s and %s · %s%s = %s%s<sup>2</sup> = %s." % (I, sg(a), cs(0, a), I, sg(b), I, sg(b), I, sg(-b))
    w = [v for v in dict.fromkeys(w) if v != right]
    return mcq(q, right, w, e + " <b>%s</b>." % right)


def one_mix(r):
    p = r.choice([2, 3, 4, 5, -2, -3])
    a, b = rz(r)
    c, d = rz(r)
    re1, im1 = p * a, p * b
    re2, im2 = -d, c  # i(c + di) = -d + ci
    right = cs(re1 + re2, im1 + im2)
    w = [cs(re1 + d, im1 + im2), cs(re1 + re2, im1 - im2), cs(p * a + c, p * b + d), cs(re1 - re2, im1 + im2)]
    w = [v for v in dict.fromkeys(w) if v != right]
    return mcq("Simplify %s(%s) + %s(%s)." % (sg(p), cs(a, b), I, cs(c, d)), right, w,
               "%s(%s) = %s and %s(%s) = %s (because %s<sup>2</sup> = −1). Add: <b>%s</b>." % (sg(p), cs(a, b), cs(re1, im1), I, cs(c, d), cs(re2, im2), I, right))


def build():
    sets, R = build_sets([
        ("Powers of i and square roots of negatives", [("collect", W(cx.one_i), 20)]),
        ("Add complex numbers", [("collect", W(cx.one_add), 10), ("collect", uniq(one_sub), 10)]),
        ("Multiply complex numbers", [("collect", W(cx.one_mul), 20)]),
        ("Squares, conjugates and i times a number", [("collect", uniq(one_sq), 20)]),
        ("Mixed complex expressions", [("collect", uniq(one_mix), 20)]),
    ], 69719)
    finish(sets, R)
    body = lesson('<ul><li><i>i</i> = √(−1), so <i>i</i><sup>2</sup> = −1. Powers of <i>i</i> repeat every 4: <i>i</i>, −1, −<i>i</i>, 1.</li><li>A complex number is <i>a</i> + <i>bi</i>: real part <i>a</i>, imaginary part <i>b</i>.</li><li>Add or subtract real parts with real parts and imaginary parts with imaginary parts.</li><li>Multiply like binomials, then replace <i>i</i><sup>2</sup> with −1. (<i>a</i> + <i>bi</i>)(<i>a</i> − <i>bi</i>) = <i>a</i><sup>2</sup> + <i>b</i><sup>2</sup>.</li></ul>',
        [example("(3 + 2<i>i</i>)(1 − 4<i>i</i>)", ["3 − 12<i>i</i> + 2<i>i</i> − 8<i>i</i><sup>2</sup>", "3 − 10<i>i</i> + 8"], "11 − 10<i>i</i>")],
        [['Using <i>i</i><sup>2</sup> = 1', '<i>i</i><sup>2</sup> = −1.'], ['Subtracting only the real parts', 'Subtract both parts.'], ['Squaring each part separately', '(<i>a</i> + <i>bi</i>)<sup>2</sup> has a middle term 2<i>abi</i>.']])
    faq = [('What does TEKS 2A.7A ask?', 'Add, subtract, and multiply complex numbers.'), ('Is every real number a complex number?', 'Yes. 5 = 5 + 0i.'), ('What is a conjugate?', 'a − bi is the conjugate of a + bi; their product is a real number.'), ('Why do complex numbers matter?', 'They give solutions to equations like x² + 4 = 0.')]
    make('complex-numbers', 19, 'Number and Algebraic Methods', '2A.7A',
         '2A.7A add, subtract, and multiply complex numbers',
         'Adding, Subtracting and Multiplying Complex Numbers', 'Complex Numbers',
         'Free Algebra II complex number worksheets for Texas TEKS 2A.7A: powers of i, adding, subtracting and multiplying complex numbers, squares and conjugates. 100 questions with answers.',
         'i² = −1.', 'Combine real parts with real parts and imaginary parts with imaginary parts.',
         body, faq, sets, seo_title='Algebra II Complex Numbers Worksheets (TEKS 2A.7A)')


if __name__ == "__main__":
    build()
