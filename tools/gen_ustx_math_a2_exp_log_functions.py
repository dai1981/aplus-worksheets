# -*- coding: utf-8 -*-
"""
Texas Algebra II: Graphs of Exponential and Logarithmic Functions (TEKS 2A.5A)
  python3 tools/gen_ustx_math_a2_exp_log_functions.py
How af(x), f(x) + d and f(x − c) change the graphs of b^x and log_b x for b = 2, 10 and e: describing the change,
asymptotes, domain and range (own maker), plus asymptotes, growth and decay and continuous growth (US Algebra 2
makers with a new seed).
Wrong answers come from real mistakes: shifting the wrong way, moving the horizontal asymptote with c, and mixing up
the domain and the range.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_a2_exponential_functions_and_e as eg
adopt(eg)
eg.R = random.Random(697120)
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


def inner_x(c):
    return X if c == 0 else "%s %s %d" % (X, MINUS if c > 0 else "+", abs(c))


def coef(a):
    return "" if a == 1 else (MINUS if a == -1 else sg(a))


def btxt(b):
    return "<i>e</i>" if b == "e" else b


def ltxt(b):
    return {"2": "log<sub>2</sub>", "10": "log", "e": "ln"}[b]


def gtext(kind, a, c, d, b="2"):
    ix = inner_x(c)
    if kind == "recip":
        core = "<span class='fr'><span class='fn'>%d</span><span class='fd'>%s</span></span>" % (abs(a), ix)
        core = (MINUS if a < 0 else "") + core
    elif kind == "cbrt":
        core = "%s∛(%s)" % (coef(a), ix) if c else "%s∛%s" % (coef(a), X)
    elif kind == "exp":
        core = "%s%s<sup>%s</sup>" % (coef(a) if abs(a) == 1 else sg(a) + "·", btxt(b), ix)
    else:
        core = "%s%s(%s)" % (coef(a), ltxt(b), ix)
    if d:
        core += " %s %d" % ("+" if d > 0 else MINUS, abs(d))
    return "<i>g</i>(<i>x</i>) = " + core


def ptxt(kind, b):
    return {"recip": "<span class='fr'><span class='fn'>1</span><span class='fd'><i>x</i></span></span>", "cbrt": "∛<i>x</i>", "exp": btxt(b) + "<sup><i>x</i></sup>", "log": ltxt(b) + " <i>x</i>"}[kind]


def tdesc(a, c, d):
    p = []
    if a < 0:
        p.append("reflect over the <i>x</i>-axis")
    if abs(a) > 1:
        p.append("vertical stretch by %d" % abs(a))
    if c:
        p.append("%s %d" % ("right" if c > 0 else "left", abs(c)))
    if d:
        p.append("%s %d" % ("up" if d > 0 else "down", abs(d)))
    t = ", ".join(p)
    return t[0].upper() + t[1:]


def tf(kind):
    def f(r):
        a = r.choice([1, 1, -1, 2, -2, 3])
        c = r.choice([n for n in range(-6, 7) if n])
        d = r.choice([n for n in range(-6, 7) if n])
        b = r.choice(["2", "10", "e"]) if kind in ("exp", "log") else "2"
        g = gtext(kind, a, c, d, b)
        par = "<i>f</i>(<i>x</i>) = " + ptxt(kind, b)
        t = r.randrange(3)
        if t == 0:
            right = tdesc(a, c, d)
            w = [tdesc(a, -c, d), tdesc(a, c, -d), tdesc(-a, c, d)]
            return mcq("Describe how the graph of %s is related to the graph of %s." % (g, par), right, w,
                       "Inside (<i>x</i> − <i>c</i>) moves the graph sideways the opposite way of the sign; outside + <i>d</i> moves it up or down; <i>a</i> stretches and a negative <i>a</i> reflects. <b>%s</b>." % right)
        if t == 1:
            if kind == "recip":
                q, right = "What are the asymptotes of %s?" % g, "<i>x</i> = %s and <i>y</i> = %s" % (sg(c), sg(d))
                w = ["<i>x</i> = %s and <i>y</i> = %s" % (sg(d), sg(c)), "<i>x</i> = %s and <i>y</i> = %s" % (sg(-c), sg(d)), "<i>x</i> = %s and <i>y</i> = %s" % (sg(c), sg(-d))]
                e = "The vertical asymptote moves to <i>x</i> = %s and the horizontal asymptote to <i>y</i> = %s." % (sg(c), sg(d))
            elif kind == "exp":
                q, right = "What is the horizontal asymptote of %s?" % g, "<i>y</i> = %s" % sg(d)
                w = ["<i>y</i> = %s" % sg(-d), "<i>y</i> = %s" % sg(c), "<i>x</i> = %s" % sg(c)]
                e = "%s has asymptote <i>y</i> = 0; shifting %s %d moves it to <b><i>y</i> = %s</b>." % (ptxt(kind, b), "up" if d > 0 else "down", abs(d), sg(d))
            elif kind == "log":
                q, right = "What is the vertical asymptote of %s?" % g, "<i>x</i> = %s" % sg(c)
                w = ["<i>x</i> = %s" % sg(-c), "<i>x</i> = %s" % sg(d), "<i>y</i> = %s" % sg(d)]
                e = "%s has asymptote <i>x</i> = 0; shifting %s %d moves it to <b><i>x</i> = %s</b>." % (ptxt(kind, b), "right" if c > 0 else "left", abs(c), sg(c))
            else:
                q, right = "∛<i>x</i> has its center point at (0, 0). Where is the center point of %s?" % g, "(%s, %s)" % (sg(c), sg(d))
                w = ["(%s, %s)" % (sg(-c), sg(d)), "(%s, %s)" % (sg(c), sg(-d)), "(%s, %s)" % (sg(d), sg(c))]
                e = "The center moves right %s and up %s: <b>(%s, %s)</b>." % (sg(c), sg(d), sg(c), sg(d))
            if right in w:
                raise AssertionError
            return mcq(q, right, w, e)
        if kind == "recip":
            if r.random() < 0.5:
                q, right, w = "What is the domain of %s?" % g, "<i>x</i> ≠ %s" % sg(c), ["<i>x</i> ≠ %s" % sg(-c), "<i>x</i> ≠ %s" % sg(d), "All real numbers"]
            else:
                q, right, w = "What is the range of %s?" % g, "<i>y</i> ≠ %s" % sg(d), ["<i>y</i> ≠ %s" % sg(-d), "<i>y</i> ≠ %s" % sg(c), "All real numbers"]
        elif kind == "exp":
            q = "What is the range of %s?" % g
            right = "<i>y</i> %s %s" % ("&gt;" if a > 0 else "&lt;", sg(d))
            w = ["<i>y</i> %s %s" % ("&lt;" if a > 0 else "&gt;", sg(d)), "<i>y</i> &gt; %s" % sg(c), "All real numbers"]
        elif kind == "log":
            q, right, w = "What is the domain of %s?" % g, "<i>x</i> &gt; %s" % sg(c), ["<i>x</i> &gt; %s" % sg(-c), "<i>x</i> &gt; %s" % sg(d), "All real numbers"]
        else:
            q, right, w = "What is the domain of %s?" % g, "All real numbers", ["<i>x</i> ≥ %s" % sg(c), "<i>x</i> ≠ %s" % sg(c), "<i>x</i> &gt; %s" % sg(-c)]
        if right in w:
            raise AssertionError
        return mcq(q, right, w, "Shift the parent's domain or range with the graph: <b>%s</b>." % right)
    f.__name__ = "tf_" + kind
    return f


tf_exp = tf("exp")
tf_log = tf("log")


def build():
    sets, R = build_sets([
        ("Transformations of exponential functions", [("collect", uniq(tf_exp), 20)]),
        ("Transformations of logarithmic functions", [("collect", uniq(tf_log), 20)]),
        ("Asymptotes and key features", [("collect", W(eg.one_feat), 20)]),
        ("Growth or decay?", [("collect", W(eg.one_gd), 20)]),
        ("The number e", [("collect", W(eg.one_e), 20)]),
    ], 69712)
    finish(sets, R)
    body = lesson('<ul><li><i>g</i>(<i>x</i>) = <i>a</i> · <i>b</i><sup><i>x</i> − <i>c</i></sup> + <i>d</i>: the horizontal asymptote moves to <i>y</i> = <i>d</i>.</li><li><i>g</i>(<i>x</i>) = <i>a</i> log<sub><i>b</i></sub>(<i>x</i> − <i>c</i>) + <i>d</i>: the vertical asymptote moves to <i>x</i> = <i>c</i>, and the domain is <i>x</i> &gt; <i>c</i>.</li><li>A negative <i>a</i> reflects the graph over the <i>x</i>-axis; for an exponential the range becomes <i>y</i> &lt; <i>d</i>.</li><li>log means base 10 and ln means base <i>e</i> ≈ 2.718.</li></ul>',
        [example("<i>g</i>(<i>x</i>) = 2<sup><i>x</i> + 3</sup> − 4", ["Left 3, down 4", "Asymptote <i>y</i> = −4"], "Range <i>y</i> &gt; −4"), example("<i>g</i>(<i>x</i>) = ln(<i>x</i> − 5)", ["Right 5"], "Asymptote <i>x</i> = 5, domain <i>x</i> &gt; 5")],
        [['Shifting the wrong way', '<i>x</i> − 3 moves right 3.'], ['Moving the horizontal asymptote with <i>c</i>', 'Only <i>d</i> moves <i>y</i> = 0.'], ['Mixing up domain and range', 'Logs limit the domain; exponentials limit the range.']])
    faq = [('What does TEKS 2A.5A ask?', 'Determine the effects on the key attributes on the graphs of f(x) = b^x and f(x) = log_b(x) where b is 2, 10, and e when f(x) is replaced by af(x), f(x) + d, and f(x − c) for specific positive and negative real values of a, c, and d.'), ('What is e?', 'A number about 2.718 used for continuous growth.'), ('Are b^x and log_b x related?', 'Yes. They are inverses, reflections of each other over y = x.'), ('Does a log graph have a horizontal asymptote?', 'No. It has a vertical asymptote.')]
    make('exponential-and-logarithmic-functions', 12, 'Exponential and Logarithmic Functions and Equations', '2A.5A',
         '2A.5A determine the effects on the key attributes on the graphs of f(x) = b^x and f(x) = log_b(x) where b is 2, 10, and e when f(x) is replaced by af(x), f(x) + d, and f(x − c) for specific positive and negative real values of a, c, and d',
         'Graphs of Exponential and Logarithmic Functions', 'Exponential and Log Graphs',
         'Free Algebra II worksheets for Texas TEKS 2A.5A: transformations of exponential and logarithmic graphs with bases 2, 10 and e, asymptotes, domain, range, growth and decay. 100 questions with answers.',
         'b^(x − c) + d has asymptote y = d; log_b(x − c) + d has asymptote x = c.', 'A negative a reflects the graph over the x-axis.',
         body, faq, sets, seo_title='Algebra II Exponential and Logarithmic Functions Worksheets (TEKS 2A.5A)')


if __name__ == "__main__":
    build()
