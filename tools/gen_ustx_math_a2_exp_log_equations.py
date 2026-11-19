# -*- coding: utf-8 -*-
"""
Texas Algebra II: Exponential and Logarithmic Equations (TEKS 2A.5B, 2A.5D, 2A.5E)
  python3 tools/gen_ustx_math_a2_exp_log_equations.py
Solving exponential equations with a common base or logarithms, solving log equations, applications (US Algebra 2
makers with a new seed), and extraneous solutions of log equations and recursive notation for exponential models (own
makers).
Wrong answers come from real mistakes: keeping a value that makes a log input negative, adding instead of multiplying
in a recursive rule, and multiplying the exponent by the base.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_a2_exponential_and_logarithmic_equations as el
adopt(el)
el.R = random.Random(697140)
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


def one_ext(r):
    b = r.choice([2, 3, 10, 6])
    n = r.choice([1, 2, 3]) if b != 10 else r.choice([1, 2])
    v = b ** n
    for _ in range(100):
        p = r.randint(1, 12)
        qn = -r.randint(1, 12)
        if p * qn == -v:
            break
    else:
        raise AssertionError
    # x(x + k) = v with roots p and qn: x^2 + kx - v = 0, k = -(p + qn)
    k = -(p + qn)
    if k == 0:
        raise AssertionError
    lg_ = "log" if b == 10 else "log<sub>%d</sub>" % b
    inner = "<i>x</i> %s %d" % ("+" if k > 0 else MINUS, abs(k))
    q = "Solve %s <i>x</i> + %s(%s) = %d." % (lg_, lg_, inner, n)
    if k < 0 and p + k <= 0:
        raise AssertionError
    right = "<i>x</i> = %d" % p
    w = ["<i>x</i> = %d or <i>x</i> = %s" % (p, sg(qn)), "<i>x</i> = %s" % sg(qn), "No solution"]
    return mcq(q, right, w, "Combine: %s[<i>x</i>(%s)] = %d, so <i>x</i>(%s) = %s. Then <i>x</i><sup>2</sup> %s %d<i>x</i> − %s = 0 gives <i>x</i> = %d or <i>x</i> = %s. A log input must be positive, so %s is extraneous. <b>%s</b>." % (
        lg_, inner, n, inner, comma(v), "+" if k > 0 else MINUS, abs(k), comma(v), p, sg(qn), sg(qn), right))


def one_ext2(r):
    b = r.choice([2, 3, 5, 10])
    a = r.randint(2, 5)
    c = r.randint(1, 9)
    x = r.randint(1, 8)
    # log(a x + c) = log(x^2 + d) with roots x and y
    y = -r.randint(1, 6)
    s, pr = x + y, x * y
    lg_ = "log" if b == 10 else "log<sub>%d</sub>" % b
    # x^2 - a x + d - c = 0 with roots x, y: a = s, d - c = pr
    a = s
    if a <= 0:
        raise AssertionError
    d = pr + c
    if a * y + c > 0 and y * y + d > 0:
        raise AssertionError
    rhs = poly([1, 0, d])
    q = "Solve %s(%s) = %s(%s)." % (lg_, poly([a, c]), lg_, rhs)
    right = "<i>x</i> = %d" % x
    w = ["<i>x</i> = %s or <i>x</i> = %d" % (sg(y), x), "<i>x</i> = %s" % sg(y), "No solution"]
    return mcq(q, right, w, "Set the inputs equal: %s = %s, so %s = 0 and <i>x</i> = %d or <i>x</i> = %s. Check: <i>x</i> = %s makes %s = %s, and a log input must be positive. <b>%s</b>." % (
        rhs, poly([a, c]), poly([1, -a, d - c]), x, sg(y), sg(y), poly([a, c]), sg(a * y + c), right))


CTX = [("A bacteria culture starts with {a} cells and doubles every hour.", 2, "cells", "hour"), ("A town has {a} people and grows by 5% each year.", "1.05", "people", "year"),
       ("A car worth ${a} loses 15% of its value each year.", "0.85", "dollars", "year"), ("A video has {a} views and the views triple every day.", 3, "views", "day"),
       ("A savings account has ${a} and earns 4% interest each year.", "1.04", "dollars", "year"), ("A pond has {a} square feet of algae, and the area grows by 20% each week.", "1.2", "square feet", "week"),
       ("A medicine dose of {a} mg loses half its amount every 6 hours.", "0.5", "mg", "6 hours"), ("A rumor is known by {a} students and the number doubles every day.", 2, "students", "day")]


def one_rec(r):
    t, m, unit_, per = r.choice(CTX)
    a = r.choice([100, 200, 500, 800, 1000, 1200, 2000, 5000, 20000, 30000])
    if "$" in t and a < 1000:
        raise AssertionError
    txt = t.format(a=comma(a))
    ms = str(m)
    kind = r.choice(["rec", "exp", "next"])
    if kind == "rec":
        right = "<i>a</i><sub>0</sub> = %s, <i>a</i><sub><i>n</i></sub> = %s · <i>a</i><sub><i>n</i>−1</sub>" % (comma(a), ms)
        w = ["<i>a</i><sub>0</sub> = %s, <i>a</i><sub><i>n</i></sub> = <i>a</i><sub><i>n</i>−1</sub> + %s" % (comma(a), ms), "<i>a</i><sub>0</sub> = %s, <i>a</i><sub><i>n</i></sub> = %s · <i>a</i><sub><i>n</i>−1</sub>" % (ms, comma(a)),
             "<i>a</i><sub>0</sub> = %s, <i>a</i><sub><i>n</i></sub> = %s · <i>n</i>" % (comma(a), ms)]
        q = txt + " Which recursive rule models the amount after <i>n</i> periods of one %s?" % per
        e = "Each %s the amount is multiplied by %s, so each term is %s times the one before." % (per, ms, ms)
    elif kind == "exp":
        right = "<i>y</i> = %s(%s)<sup><i>t</i></sup>" % (comma(a), ms)
        w = ["<i>y</i> = %s(%s)<sup><i>t</i></sup>" % (ms, comma(a)), "<i>y</i> = %s + %s<i>t</i>" % (comma(a), ms), "<i>y</i> = %s(%s<i>t</i>)" % (comma(a), ms)]
        q = txt + " Which function gives the amount after <i>t</i> periods of one %s?" % per
        e = "Start value %s, multiplier %s each period." % (comma(a), ms)
    else:
        from fractions import Fraction as F_
        mm = F_(ms)
        v1 = F_(a) * mm
        v2 = v1 * mm
        if v2.denominator != 1 and (v2 * 100).denominator != 1:
            raise AssertionError
        if unit_ != "dollars" and v2.denominator != 1:
            raise AssertionError
        def fm(v):
            if v.denominator == 1:
                return comma(int(v))
            c = int(round(v * 100))
            return "%s.%02d" % (comma(c // 100), c % 100)
        right = fm(v2)
        w = [fm(F_(a) + 2 * mm), fm(v1), fm(F_(a) * mm * 3), fm(v2 + F_(a))]
        w = [x for x in w if x != right]
        q = txt + " Use <i>a</i><sub><i>n</i></sub> = %s · <i>a</i><sub><i>n</i>−1</sub> with <i>a</i><sub>0</sub> = %s. What is <i>a</i><sub>2</sub>?" % (ms, comma(a))
        e = "<i>a</i><sub>1</sub> = %s × %s = %s, <i>a</i><sub>2</sub> = %s × %s = %s." % (comma(a), ms, fm(v1), fm(v1), ms, fm(v2))
    return mcq(q, right, w, e + " <b>%s</b>." % right)


def build():
    sets, R = build_sets([
        ("Exponential equations with a common base", [("collect", W(el.one_base), 20)]),
        ("Solve exponential equations with logarithms", [("collect", W(el.one_log), 20)]),
        ("Solve logarithmic equations", [("collect", W(el.one_logeq), 10), ("collect", W(el.one_prop), 10)]),
        ("Reasonable solutions of log equations", [("collect", uniq(one_ext), 12), ("collect", uniq(one_ext2), 8)]),
        ("Exponential models and recursive rules", [("collect", W(el.one_app), 10), ("collect", uniq(one_rec), 10)]),
    ], 69714)
    finish(sets, R)
    body = lesson('<ul><li>Common base: 8<sup><i>x</i></sup> = 32 → 2<sup>3<i>x</i></sup> = 2<sup>5</sup> → 3<i>x</i> = 5.</li><li>Otherwise take a log of both sides: 5<sup><i>x</i></sup> = 40 → <i>x</i> = ln 40 ÷ ln 5.</li><li>log<sub><i>b</i></sub> <i>A</i> = <i>c</i> → <i>A</i> = <i>b</i><sup><i>c</i></sup>.</li><li><b>Check</b> every answer: a log input must be positive. A value that makes it 0 or negative is extraneous.</li><li>Recursive rule: <i>a</i><sub><i>n</i></sub> = <i>r</i> · <i>a</i><sub><i>n</i>−1</sub>; explicit rule: <i>a</i><sub><i>n</i></sub> = <i>a</i><sub>0</sub> · <i>r</i><sup><i>n</i></sup>.</li></ul>',
        [example("log<sub>2</sub> <i>x</i> + log<sub>2</sub>(<i>x</i> − 2) = 3", ["<i>x</i>(<i>x</i> − 2) = 8", "<i>x</i> = 4 or <i>x</i> = −2", "−2 makes log<sub>2</sub>(−2) undefined"], "<i>x</i> = 4")],
        [['Keeping an extraneous solution', 'Check that every log input is positive.'], ['Adding instead of multiplying', 'Doubling: <i>a</i><sub><i>n</i></sub> = 2 · <i>a</i><sub><i>n</i>−1</sub>.'], ['Multiplying the exponent by the base', '2<sup>3</sup> = 8, not 6.']])
    faq = [('What does TEKS 2A.5B ask?', 'Formulate exponential and logarithmic equations that model real-world situations, including exponential relationships written in recursive notation.'), ('What does TEKS 2A.5D ask?', 'Solve exponential equations of the form y = ab^x where a is a nonzero real number and b is greater than zero and not equal to one and single logarithmic equations having real solutions.'), ('What does TEKS 2A.5E ask?', 'Determine the reasonableness of a solution to a logarithmic equation.'), ('Why can a log equation have an extraneous solution?', 'Combining logs can allow values that make an original log input negative.')]
    make('exponential-and-logarithmic-equations', 14, 'Exponential and Logarithmic Functions and Equations', '2A.5B, 2A.5D, 2A.5E',
         '2A.5B formulate exponential and logarithmic equations that model real-world situations, including exponential relationships written in recursive notation; 2A.5D solve exponential equations of the form y = ab^x where a is a nonzero real number and b is greater than zero and not equal to one and single logarithmic equations having real solutions; 2A.5E determine the reasonableness of a solution to a logarithmic equation',
         'Exponential and Logarithmic Equations', 'Exponential and Log Equations',
         'Free Algebra II worksheets for Texas TEKS 2A.5B, 2A.5D and 2A.5E: solve exponential and log equations, extraneous solutions, applications and recursive rules. 100 questions with answers.',
         'Rewrite with a common base, or take a log of both sides.', 'Check every answer: log inputs must be positive.',
         body, faq, sets, seo_title='Algebra II Exponential and Logarithmic Equations Worksheets (TEKS 2A.5B, 2A.5D, 2A.5E)')


if __name__ == "__main__":
    build()
