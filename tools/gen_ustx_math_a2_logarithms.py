# -*- coding: utf-8 -*-
"""
Texas Algebra II: Logarithms: Exponential and Logarithmic Form (TEKS 2A.5C)
  python3 tools/gen_ustx_math_a2_logarithms.py
Rewriting exponential equations as logarithms and back, evaluating logs, expanding and condensing, change of base
(US Algebra 2 makers with a new seed), and inverse properties and estimating logs between integers (own maker).
Wrong answers come from real mistakes: swapping the base and the exponent, dividing instead of subtracting, and
reading log₂ 50 as 25.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_a2_logarithms_and_their_properties as lg
adopt(lg)
lg.R = random.Random(697130)
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


def one_est(r):
    kind = r.choice(["between", "between", "inv", "inv2", "zero"])
    b = r.choice([2, 3, 4, 5, 10])
    if kind == "between":
        n = r.randint(1, {2: 9, 3: 5, 4: 4, 5: 3, 10: 4}[b])
        lo, hi = b ** n, b ** (n + 1)
        x = r.randint(lo + 1, hi - 1)
        lg_ = "log " if b == 10 else "log<sub>%d</sub> " % b
        right = "Between %d and %d" % (n, n + 1)
        w = ["Between %d and %d" % (n - 1, n), "Between %d and %d" % (n + 1, n + 2), "Between %s and %s" % (comma(lo), comma(hi))]
        return mcq("Between which two whole numbers is %s%s?" % (lg_, comma(x)), right, w,
                   "%d<sup>%d</sup> = %s and %d<sup>%d</sup> = %s, and %s is between them. <b>%s</b>." % (b, n, comma(lo), b, n + 1, comma(hi), comma(x), right))
    if kind == "inv":
        x = r.randint(2, 40)
        if x == b:
            raise AssertionError
        lg_ = "log" if b == 10 else "log<sub>%d</sub>" % b
        right = str(x)
        w = [str(b), str(b * x), str(x + b), "1"]
        return mcq("Evaluate %d<sup>%s %d</sup>." % (b, lg_, x), right, w, "%d to the power %s %d is %d, because log asks which power of %d gives %d. <b>%d</b>." % (b, lg_, x, x, b, x, x))
    if kind == "inv2":
        n = r.randint(-5, 12)
        if b == 10 and r.random() < 0.5:
            q, e = "Evaluate log 10<sup>%s</sup>." % sg(n), "log 10<sup><i>n</i></sup> = <i>n</i>."
        else:
            q, e = "Evaluate log<sub>%d</sub> %d<sup>%s</sup>." % (b, b, sg(n)), "log<sub><i>b</i></sub> <i>b</i><sup><i>n</i></sup> = <i>n</i>."
        right = sg(n)
        w = [sg(b * n), sg(-n) if n else "1", sg(n + 1), str(b)]
        return mcq(q, right, w, e + " <b>%s</b>." % right)
    if r.random() < 0.5:
        q, right, w, e = "Evaluate ln <i>e</i><sup>%d</sup>." % (b), str(b), ["<i>e</i>", "1", str(b + 1), "0"], "ln <i>e</i><sup><i>n</i></sup> = <i>n</i>."
    else:
        q, right, w, e = "Evaluate <i>e</i><sup>ln %d</sup>." % (b * 3), str(b * 3), ["<i>e</i>", "1", "ln %d" % (b * 3), str(b * 3 + 1)], "<i>e</i> and ln undo each other: <i>e</i><sup>ln <i>x</i></sup> = <i>x</i>."
    return mcq(q, right, w, e + " <b>%s</b>." % right)


def build():
    sets, R = build_sets([
        ("Exponential and logarithmic form", [("collect", W(lg.one_conv), 20)]),
        ("Evaluate logarithms", [("collect", W(lg.one_eval), 20)]),
        ("Expand and condense", [("collect", W(lg.one_exp), 10), ("collect", W(lg.one_cond), 10)]),
        ("Change of base and domain", [("collect", W(lg.one_cob), 20)]),
        ("Inverse properties and estimates", [("collect", uniq(one_est), 20)]),
    ], 69713)
    finish(sets, R)
    body = lesson('<ul><li>log<sub><i>b</i></sub> <i>x</i> = <i>y</i> means <i>b</i><sup><i>y</i></sup> = <i>x</i>. A logarithm is an exponent.</li><li>log means base 10; ln means base <i>e</i>.</li><li>log<sub><i>b</i></sub> <i>b</i><sup><i>n</i></sup> = <i>n</i> and <i>b</i><sup>log<sub><i>b</i></sub> <i>x</i></sup> = <i>x</i>.</li><li>Product: log(<i>MN</i>) = log <i>M</i> + log <i>N</i>. Quotient: subtract. Power: log <i>M</i><sup><i>k</i></sup> = <i>k</i> log <i>M</i>.</li><li>Change of base: log<sub><i>b</i></sub> <i>x</i> = ln <i>x</i> ÷ ln <i>b</i>.</li></ul>',
        [example("Write 3<sup>4</sup> = 81 in log form", ["The base stays 3; the exponent is the answer"], "log<sub>3</sub> 81 = 4"), example("log<sub>2</sub> 50", ["2<sup>5</sup> = 32, 2<sup>6</sup> = 64"], "Between 5 and 6")],
        [['Swapping the base and the exponent', 'log<sub>3</sub> 81 = 4 means 3<sup>4</sup> = 81.'], ['Dividing logs instead of subtracting', 'log <i>M</i> − log <i>N</i> = log(<i>M</i> ÷ <i>N</i>).'], ['Dividing by the base', 'log<sub>2</sub> 50 is not 25.']])
    faq = [('What does TEKS 2A.5C ask?', 'Rewrite exponential equations as their corresponding logarithmic equations and logarithmic equations as their corresponding exponential equations.'), ('Can you take the log of a negative number?', 'No, not as a real number. The input must be positive.'), ('What is log 1?', '0 in every base, because b⁰ = 1.'), ('Why is ln useful?', 'It is the inverse of e^x, which models continuous growth.')]
    make('logarithms', 13, 'Exponential and Logarithmic Functions and Equations', '2A.5C',
         '2A.5C rewrite exponential equations as their corresponding logarithmic equations and logarithmic equations as their corresponding exponential equations',
         'Logarithms: Exponential and Logarithmic Form', 'Logarithms',
         'Free Algebra II logarithm worksheets for Texas TEKS 2A.5C: exponential and logarithmic form, evaluating logs, properties, change of base and estimates. 100 questions with answers.',
         'log_b x = y means b^y = x.', 'A logarithm is an exponent.',
         body, faq, sets, seo_title='Algebra II Logarithms Worksheets (TEKS 2A.5C)')


if __name__ == "__main__":
    build()
