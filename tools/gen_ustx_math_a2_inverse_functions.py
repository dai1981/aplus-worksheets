# -*- coding: utf-8 -*-
"""
Texas Algebra II: Inverse Functions (TEKS 2A.2B, 2A.2C, 2A.2D)
  python3 tools/gen_ustx_math_a2_inverse_functions.py
Writing inverses with f⁻¹(x) notation, composing functions and checking inverses (US Algebra 2 makers with a new
seed), plus inverses of quadratic, square root, exponential and logarithmic functions with domain restrictions (own makers).
Wrong answers come from real mistakes: undoing the steps in the wrong order, keeping the same sign, and forgetting
that the range of f becomes the domain of f⁻¹.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_a2_composition_and_inverse_functions as ci
adopt(ci)
ci.R = random.Random(697020)
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


FI = "<i>f</i><sup>−1</sup>(<i>x</i>)"


def m(v):
    return "%s %s %d" % (X, "+" if v > 0 else MINUS, abs(v))


def one_rinv(r):
    h, k, a = r.randint(1, 9), r.randint(1, 9), r.randint(2, 6)
    kind = r.choice(["sqk", "sqh", "root", "ax2", "dom", "dom2"])
    if kind == "sqk":
        q = "Find the inverse of %s, for <i>x</i> ≥ 0." % fx(X + "<sup>2</sup> + %d" % k)
        right = FI + " = √(%s), for <i>x</i> ≥ %d" % (m(-k), k)
        w = [FI + " = √(%s), for <i>x</i> ≥ %d" % (m(k), k), FI + " = √%s %s %d, for <i>x</i> ≥ 0" % (X, MINUS, k), FI + " = <i>x</i><sup>2</sup> %s %d" % (MINUS, k)]
        e = "Swap: <i>x</i> = <i>y</i><sup>2</sup> + %d, so <i>y</i><sup>2</sup> = <i>x</i> − %d and <i>y</i> = √(<i>x</i> − %d). The range of <i>f</i> is <i>y</i> ≥ %d, so that is the domain of the inverse." % (k, k, k, k)
    elif kind == "sqh":
        q = "Find the inverse of %s, for <i>x</i> ≥ %d." % (fx("(%s)<sup>2</sup>" % m(-h)), h)
        right = FI + " = √%s + %d, for <i>x</i> ≥ 0" % (X, h)
        w = [FI + " = √%s %s %d, for <i>x</i> ≥ 0" % (X, MINUS, h), FI + " = √(%s), for <i>x</i> ≥ %d" % (m(-h), h), FI + " = √(%s), for <i>x</i> ≥ 0" % m(h)]
        e = "Swap: <i>x</i> = (<i>y</i> − %d)<sup>2</sup>, so <i>y</i> − %d = √<i>x</i> and <i>y</i> = √<i>x</i> + %d. The range of <i>f</i> is <i>y</i> ≥ 0." % (h, h, h)
    elif kind == "root":
        q = "Find the inverse of %s, for <i>x</i> ≥ %d." % (fx("√(%s) + %d" % (m(-h), k)), h)
        right = FI + " = (%s)<sup>2</sup> + %d, for <i>x</i> ≥ %d" % (m(-k), h, k)
        w = [FI + " = (%s)<sup>2</sup> + %d, for <i>x</i> ≥ %d" % (m(k), h, k), FI + " = (%s)<sup>2</sup> %s %d, for <i>x</i> ≥ %d" % (m(-k), MINUS, h, k), FI + " = (%s)<sup>2</sup> + %d, for <i>x</i> ≥ %d" % (m(-h), k, h)]
        e = "Swap: <i>x</i> = √(<i>y</i> − %d) + %d. Subtract %d and square: (<i>x</i> − %d)<sup>2</sup> = <i>y</i> − %d, so <i>y</i> = (<i>x</i> − %d)<sup>2</sup> + %d. The range of <i>f</i> is <i>y</i> ≥ %d." % (h, k, k, k, h, k, h, k)
    elif kind == "ax2":
        q = "Find the inverse of %s, for <i>x</i> ≥ 0." % fx("%d%s<sup>2</sup>" % (a, X))
        right = FI + " = √(<span class='fr'><span class='fn'><i>x</i></span><span class='fd'>%d</span></span>), for <i>x</i> ≥ 0" % a
        w = [FI + " = %d√<i>x</i>, for <i>x</i> ≥ 0" % a, FI + " = √(%d<i>x</i>), for <i>x</i> ≥ 0" % a, FI + " = <span class='fr'><span class='fn'><i>x</i><sup>2</sup></span><span class='fd'>%d</span></span>" % a]
        e = "Swap: <i>x</i> = %d<i>y</i><sup>2</sup>, so <i>y</i><sup>2</sup> = <i>x</i> ÷ %d and <i>y</i> = √(<i>x</i> ÷ %d)." % (a, a, a)
    elif kind == "dom":
        q = "%s has domain <i>x</i> ≥ %d and range <i>y</i> ≥ %d. What is the domain of %s?" % (fx("√(%s) + %d" % (m(-h), k)), h, k, FI.replace("(<i>x</i>)", ""))
        if h == k:
            raise AssertionError
        right = "<i>x</i> ≥ %d" % k
        w = ["<i>x</i> ≥ %d" % h, "<i>x</i> ≤ %d" % k, "All real numbers"]
        e = "An inverse swaps inputs and outputs, so the range of <i>f</i> becomes the domain of the inverse."
    else:
        q = "To have an inverse function, %s is restricted to <i>x</i> ≥ %d. What is the range of %s?" % (fx("(%s)<sup>2</sup> + %d" % (m(-h), k)), h, FI.replace("(<i>x</i>)", ""))
        if h == k:
            raise AssertionError
        right = "<i>y</i> ≥ %d" % h
        w = ["<i>y</i> ≥ %d" % k, "<i>y</i> ≤ %d" % h, "All real numbers"]
        e = "The domain of <i>f</i> (<i>x</i> ≥ %d) becomes the range of the inverse." % h
    return mcq(q, right, w, e + " <b>%s</b>." % right)


def lg(b):
    return {10: "log ", "e": "ln "}.get(b, "log<sub>%s</sub> " % b)


def pw(b, ex):
    return "%s<sup>%s</sup>" % ("<i>e</i>" if b == "e" else b, ex)


def one_elinv(r):
    b = r.choice([2, 3, 4, 5, 10, "e"])
    h, k = r.randint(1, 9), r.randint(1, 9)
    kind = r.choice(["exp", "log", "expk", "exph", "logk", "logh", "val", "dom"])
    if kind == "exp":
        q, right = "Find the inverse of %s." % fx(pw(b, "<i>x</i>")), FI + " = " + lg(b) + X
        w = [FI + " = " + pw(b, "−<i>x</i>"), FI + " = <i>x</i><sup>%s</sup>" % ("<i>e</i>" if b == "e" else b), FI + " = " + lg(b) + "(−<i>x</i>)"]
        e = "The inverse of an exponential function is the logarithm with the same base."
    elif kind == "log":
        q, right = "Find the inverse of %s." % fx(lg(b) + X), FI + " = " + pw(b, "<i>x</i>")
        w = [FI + " = <i>x</i><sup>%s</sup>" % ("<i>e</i>" if b == "e" else b), FI + " = " + pw(X, b if b != "e" else "<i>e</i>").replace("<i>x</i><sup>", "<i>x</i><sup>"), FI + " = %s<i>x</i>" % ("<i>e</i>" if b == "e" else b)]
        w = list(dict.fromkeys(w))
        if len(w) < 3:
            w.append(FI + " = −" + pw(b, "<i>x</i>"))
        e = "<i>y</i> = %s<i>x</i> means <i>x</i> = %s. Swap <i>x</i> and <i>y</i>." % (lg(b), pw(b, "<i>y</i>"))
    elif kind == "expk":
        q, right = "Find the inverse of %s." % fx(pw(b, "<i>x</i>") + " + %d" % k), FI + " = %s(%s)" % (lg(b), m(-k))
        w = [FI + " = %s(%s)" % (lg(b), m(k)), FI + " = %s<i>x</i> %s %d" % (lg(b), MINUS, k), FI + " = %s<i>x</i> + %d" % (lg(b), k)]
        e = "Swap: <i>x</i> = %s + %d. Subtract %d first, then take the log: <i>y</i> = %s(<i>x</i> − %d)." % (pw(b, "<i>y</i>"), k, k, lg(b), k)
    elif kind == "exph":
        q, right = "Find the inverse of %s." % fx(pw(b, m(-h))), FI + " = %s<i>x</i> + %d" % (lg(b), h)
        w = [FI + " = %s<i>x</i> %s %d" % (lg(b), MINUS, h), FI + " = %s(%s)" % (lg(b), m(h)), FI + " = %s(%s)" % (lg(b), m(-h))]
        e = "Swap: <i>x</i> = %s. Take the log: %s<i>x</i> = <i>y</i> − %d, so <i>y</i> = %s<i>x</i> + %d." % (pw(b, "<i>y</i> − %d" % h), lg(b), h, lg(b), h)
    elif kind == "logk":
        q, right = "Find the inverse of %s." % fx(lg(b) + X + " + %d" % k), FI + " = " + pw(b, m(-k))
        w = [FI + " = " + pw(b, m(k)), FI + " = " + pw(b, "<i>x</i>") + " %s %d" % (MINUS, k), FI + " = " + pw(b, "<i>x</i>") + " + %d" % k]
        e = "Swap: <i>x</i> = %s<i>y</i> + %d, so %s<i>y</i> = <i>x</i> − %d and <i>y</i> = %s." % (lg(b), k, lg(b), k, pw(b, "<i>x</i> − %d" % k))
    elif kind == "logh":
        q, right = "Find the inverse of %s." % fx(lg(b) + "(%s)" % m(-h)), FI + " = " + pw(b, "<i>x</i>") + " + %d" % h
        w = [FI + " = " + pw(b, "<i>x</i>") + " %s %d" % (MINUS, h), FI + " = " + pw(b, m(-h)), FI + " = " + pw(b, m(h))]
        e = "Swap: <i>x</i> = %s(<i>y</i> − %d), so <i>y</i> − %d = %s and <i>y</i> = %s + %d." % (lg(b), h, h, pw(b, "<i>x</i>"), pw(b, "<i>x</i>"), h)
    elif kind == "val":
        if b == "e":
            raise AssertionError
        n = r.randint(2, {2: 7, 3: 5, 4: 4, 5: 4, 10: 5}[b])
        v = b ** n
        q, right = "%s. What is <i>f</i><sup>−1</sup>(%s)?" % (fx(pw(b, "<i>x</i>")), comma(v)), str(n)
        w = [str(v), str(v // b), str(n + 1), str(b * n)]
        e = "<i>f</i><sup>−1</sup>(%s) is the input that gives %s: %s = %s, so it is %d. (It is also %s%s = %d.)" % (comma(v), comma(v), pw(b, n), comma(v), n, lg(b), comma(v), n)
    else:
        q, right = "%s has range <i>y</i> &gt; %d. What is the domain of its inverse?" % (fx(pw(b, "<i>x</i>") + " + %d" % k), k), "<i>x</i> &gt; %d" % k
        w = ["<i>x</i> &gt; 0", "<i>x</i> &gt; %d" % (-k) if False else "<i>x</i> &gt; −%d" % k, "All real numbers"]
        e = "The range of <i>f</i> becomes the domain of the inverse <i>f</i><sup>−1</sup>(<i>x</i>) = %s(<i>x</i> − %d)." % (lg(b), k)
    return mcq(q, right, w, e + " <b>%s</b>." % right)


def build():
    sets, R = build_sets([
        ("Find the inverse of a function", [("collect", W(ci.one_inv), 20)]),
        ("Inverses of quadratic and square root functions", [("collect", uniq(one_rinv), 20)]),
        ("Inverses of exponential and logarithmic functions", [("collect", uniq(one_elinv), 20)]),
        ("Compose two functions", [("collect", W(ci.one_comp), 10), ("collect", W(ci.one_eval), 10)]),
        ("Are they inverses?", [("collect", W(ci.one_check), 20)]),
    ], 69702)
    finish(sets, R)
    body = lesson('<ul><li>To find an inverse, swap <i>x</i> and <i>y</i>, then solve for <i>y</i>. Write it as <i>f</i><sup>−1</sup>(<i>x</i>).</li><li>The graph of <i>f</i><sup>−1</sup> is the reflection of <i>f</i> over the line <i>y</i> = <i>x</i>.</li><li>The domain of <i>f</i> is the range of <i>f</i><sup>−1</sup>, and the range of <i>f</i> is the domain of <i>f</i><sup>−1</sup>.</li><li><i>x</i><sup>2</sup> needs a restricted domain (such as <i>x</i> ≥ 0) to have an inverse function: √<i>x</i>.</li><li><i>f</i> and <i>g</i> are inverses when <i>f</i>(<i>g</i>(<i>x</i>)) = <i>x</i> and <i>g</i>(<i>f</i>(<i>x</i>)) = <i>x</i>.</li></ul>',
        [example("<i>f</i>(<i>x</i>) = <i>x</i><sup>2</sup> + 3, <i>x</i> ≥ 0", ["Swap: <i>x</i> = <i>y</i><sup>2</sup> + 3", "<i>y</i> = √(<i>x</i> − 3)"], "<i>f</i><sup>−1</sup>(<i>x</i>) = √(<i>x</i> − 3), <i>x</i> ≥ 3"), example("<i>f</i>(<i>x</i>) = 2<sup><i>x</i></sup> + 5", ["Swap: <i>x</i> = 2<sup><i>y</i></sup> + 5", "2<sup><i>y</i></sup> = <i>x</i> − 5"], "<i>f</i><sup>−1</sup>(<i>x</i>) = log<sub>2</sub>(<i>x</i> − 5)")],
        [['Undoing in the wrong order', 'Undo the last step first.'], ['Keeping the same sign', 'The inverse of + 5 is − 5.'], ['Forgetting the domain', 'The range of <i>f</i> is the domain of <i>f</i><sup>−1</sup>.']])
    faq = [('What does TEKS 2A.2B ask?', 'Graph and write the inverse of a function using notation such as f⁻¹(x).'), ('What does TEKS 2A.2C ask?', 'Describe and analyze the relationship between a function and its inverse (quadratic and square root, logarithmic and exponential), including the restriction(s) on domain, which will restrict its range.'), ('What does TEKS 2A.2D ask?', 'Use the composition of two functions, including the necessary restrictions on the domain, to determine if the functions are inverses of each other.'), ('Does f⁻¹(x) mean 1/f(x)?', 'No. It means the inverse function.')]
    make('inverse-functions', 2, 'Attributes of Functions and Their Inverses', '2A.2B, 2A.2C, 2A.2D',
         '2A.2B graph and write the inverse of a function using notation such as f^(−1)(x); 2A.2C describe and analyze the relationship between a function and its inverse (quadratic and square root, logarithmic and exponential), including the restriction(s) on domain, which will restrict its range; 2A.2D use the composition of two functions, including the necessary restrictions on the domain, to determine if the functions are inverses of each other',
         'Inverse Functions', 'Inverse Functions',
         'Free Algebra II inverse function worksheets for Texas TEKS 2A.2B to 2A.2D: write f⁻¹(x), inverses of quadratic, square root, exponential and log functions, composition and checking inverses. 100 questions with answers.',
         'To find f⁻¹, swap x and y and solve for y.', 'The range of f is the domain of f⁻¹.',
         body, faq, sets, seo_title='Algebra II Inverse Functions Worksheets (TEKS 2A.2B–2A.2D)')


if __name__ == "__main__":
    build()
