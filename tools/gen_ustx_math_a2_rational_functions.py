# -*- coding: utf-8 -*-
"""
Texas Algebra II: Rational Functions and Asymptotes (TEKS 2A.6G, 2A.6K)
  python3 tools/gen_ustx_math_a2_rational_functions.py
Transformations of f(x) = 1/x with asymptotes, domain and range (own maker), holes, horizontal and slant asymptotes,
intercepts and graphs (US Precalculus makers with a new seed), and the domain and range of rational functions in
interval, inequality and set notation (own maker).
Wrong answers come from real mistakes: the wrong sign for the vertical asymptote, swapping the asymptotes, and
forgetting the values left out of the domain.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_pc_rational_functions_and_asymptotes as ra
adopt(ra)
ra.R = random.Random(697170)
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


tf_recip = tf("recip")
INF = "∞"


def lin_(h):
    return X if h == 0 else "%s %s %d" % (X, MINUS if h > 0 else "+", abs(h))


def one_rdr(r):
    a = r.choice([1, 2, 3, 4, 5, -1, -2, -3])
    h, k = r.choice([n for n in range(-8, 9) if n]), r.choice([n for n in range(-8, 9) if n])
    f = fx(("" if a > 0 else MINUS) + "<span class='fr'><span class='fn'>%d</span><span class='fd'>%s</span></span> %s %d" % (abs(a), lin_(h), "+" if k > 0 else MINUS, abs(k)))
    which = r.choice(["domain", "range"])
    v, var = (h, "<i>x</i>") if which == "domain" else (k, "<i>y</i>")
    o = k if which == "domain" else h
    note = r.choice(["interval", "set", "ineq"])
    def form(val, vv):
        if note == "interval":
            return "(%s, %s) ∪ (%s, %s)" % (MINUS + INF, sg(val), sg(val), INF)
        if note == "set":
            return "{%s | %s ≠ %s}" % (vv, vv, sg(val))
        return "%s &lt; %s or %s &gt; %s" % (vv, sg(val), vv, sg(val))
    right = form(v, var)
    w = [form(-v, var), form(o, var) if o != v else form(v + 1, var), "(%s, %s)" % (MINUS + INF, INF) if note == "interval" else ("{%s | %s &gt; %s}" % (var, var, sg(v)) if note == "set" else "%s &gt; %s" % (var, sg(v)))]
    nm = {"interval": "interval notation", "set": "set notation", "ineq": "inequalities"}[note]
    e = ("The vertical asymptote is <i>x</i> = %s, so %s is left out of the domain." % (sg(h), sg(h))) if which == "domain" else ("The horizontal asymptote is <i>y</i> = %s, so the function never outputs %s." % (sg(k), sg(k)))
    return mcq("Write the %s of %s in %s." % (which, f, nm), right, w, e + " <b>%s</b>." % right)


def build():
    sets, R = build_sets([
        ("Transformations of f(x) = 1/x", [("collect", uniq(tf_recip), 20)]),
        ("Domain and range in three notations", [("collect", uniq(one_rdr), 20)]),
        ("Holes and vertical asymptotes", [("collect", W(ra.one_va), 20)]),
        ("Horizontal and slant asymptotes", [("collect", W(ra.one_ha), 20)]),
        ("Intercepts, domain and graphs", [("collect", W(ra.one_int), 10), ("collect", W(ra.one_graph), 10)]),
    ], 69717)
    finish(sets, R)
    body = lesson("<ul><li><i>g</i>(<i>x</i>) = <span class='fr'><span class='fn'><i>a</i></span><span class='fd'><i>x</i> − <i>c</i></span></span> + <i>d</i> has a vertical asymptote <i>x</i> = <i>c</i> and a horizontal asymptote <i>y</i> = <i>d</i>.</li><li>Domain: every <i>x</i> except <i>c</i>. Range: every <i>y</i> except <i>d</i>.</li><li>A factor that cancels from the top and bottom makes a <b>hole</b>, not an asymptote.</li><li>Horizontal asymptote: compare degrees. Bottom bigger → <i>y</i> = 0; equal → ratio of leading coefficients; top one bigger → slant asymptote.</li></ul>",
        [example("<i>g</i>(<i>x</i>) = <span class='fr'><span class='fn'>3</span><span class='fd'><i>x</i> + 2</span></span> − 1", ["Left 2, down 1, stretch by 3"], "Asymptotes <i>x</i> = −2 and <i>y</i> = −1")],
        [['The wrong sign for the vertical asymptote', '<i>x</i> + 2 = 0 gives <i>x</i> = −2.'], ['Swapping the asymptotes', '<i>c</i> is vertical (<i>x</i> = <i>c</i>), <i>d</i> is horizontal (<i>y</i> = <i>d</i>).'], ['Calling a hole an asymptote', 'A factor that cancels makes a hole.']])
    faq = [('What does TEKS 2A.6G ask?', 'Analyze the effect on the graphs of f(x) = 1/x when f(x) is replaced by af(x), f(bx), f(x − c), and f(x) + d for specific positive and negative real values of a, b, c, and d.'), ('What does TEKS 2A.6K ask?', 'Determine the asymptotic restrictions on the domain of a rational function and represent domain and range using interval notation, inequalities, and set notation.'), ('Can a graph cross a horizontal asymptote?', 'Sometimes, for more complicated rational functions, but 1/x and its shifts never do.'), ('What does a negative a do?', 'It reflects the graph over the x-axis.')]
    make('rational-functions', 17, 'Cubic, Cube Root, Absolute Value, and Rational Functions, Equations, and Inequalities', '2A.6G, 2A.6K',
         '2A.6G analyze the effect on the graphs of f(x) = 1/x when f(x) is replaced by af(x), f(bx), f(x − c), and f(x) + d for specific positive and negative real values of a, b, c, and d; 2A.6K determine the asymptotic restrictions on the domain of a rational function and represent domain and range using interval notation, inequalities, and set notation',
         'Rational Functions and Asymptotes', 'Rational Functions',
         'Free Algebra II rational function worksheets for Texas TEKS 2A.6G and 2A.6K: transformations of 1/x, asymptotes, holes, domain and range in interval and set notation. 100 questions with answers.',
         'a/(x − c) + d: asymptotes x = c and y = d.', 'Domain: x ≠ c. Range: y ≠ d.',
         body, faq, sets, seo_title='Algebra II Rational Functions Worksheets (TEKS 2A.6G, 2A.6K)')


if __name__ == "__main__":
    build()
