# -*- coding: utf-8 -*-
"""
Texas Algebra II: Cubic and Cube Root Functions (TEKS 2A.6A, 2A.6B)
  python3 tools/gen_ustx_math_a2_cubic_cube_root.py
Transformations of f(x) = x³ (US Algebra 2 makers with a new seed, kept to the cubic parent), transformations of
f(x) = ∛x and f(bx) for both (own makers), and solving cube root equations (own maker).
Wrong answers come from real mistakes: shifting the wrong way, squaring instead of cubing, and thinking a cube root
of a negative number has no real value.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_a2_transformations_of_functions as tr
adopt(tr)
tr.R = random.Random(697150)
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


def fam(fn, *kinds):
    """Use a US Algebra 2 transformation maker with only some parent functions."""
    def f(r):
        old = tr.PARENTS
        tr.PARENTS = {k: v for k, v in old.items() if k in kinds}
        try:
            return fn(r)
        finally:
            tr.PARENTS = old
    f.__name__ = fn.__name__
    return f


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


def bfrac(b):
    b = Fr(b)
    return ft(b)


def one_bx_maker(kinds):
    def one_bx(r):
        kind = r.choice(kinds)
        b = r.choice([Fr(2), Fr(3), Fr(4), Fr(1, 2), Fr(1, 3), Fr(-1), Fr(-2)])
        if kind == "abs" and b < 0:
            raise AssertionError
        base = {"sqrt": "√<i>x</i>", "cube": "<i>x</i><sup>3</sup>", "cbrt": "∛<i>x</i>", "abs": "|<i>x</i>|"}[kind]
        bx = ("−" if b == -1 else ft(b)) + "<i>x</i>" if b.denominator == 1 else "%s<i>x</i>" % ft(b)
        g = {"sqrt": "√(%s)" % bx, "cube": "(%s)<sup>3</sup>" % bx, "cbrt": "∛(%s)" % bx, "abs": "|%s|" % bx}[kind]
        ab = abs(b)
        if r.random() < 0.55:
            parts = []
            if ab > 1:
                parts.append("horizontal shrink by a factor of %s" % ft(1 / ab))
            elif ab < 1:
                parts.append("horizontal stretch by a factor of %s" % ft(1 / ab))
            if b < 0:
                parts.append("reflection over the <i>y</i>-axis")
            right = " and ".join(parts)
            right = right[0].upper() + right[1:]
            w = []
            if ab != 1:
                w.append(("Horizontal stretch by a factor of %s" if ab > 1 else "Horizontal shrink by a factor of %s") % ft(ab))
                w.append("Vertical shrink by a factor of %s" % ft(1 / ab) if ab > 1 else "Vertical stretch by a factor of %s" % ft(1 / ab))
            w.append("Shift %s %s" % ("left" if b > 0 else "right", ft(ab)))
            w.append("Shift %s %s" % ("right" if b > 0 else "left", ft(ab)))
            if b == -1:
                w.append("Horizontal stretch by a factor of 2")
            return mcq("How is the graph of <i>g</i>(<i>x</i>) = %s related to the graph of <i>f</i>(<i>x</i>) = %s?" % (g, base), right, w,
                       "Replacing <i>x</i> with <i>bx</i> changes the graph sideways: every <i>x</i>-coordinate is divided by <i>b</i> = %s. <b>%s</b>." % (ft(b), right))
        pts = {"sqrt": [(1, 1), (4, 2), (9, 3), (16, 4)], "cube": [(1, 1), (2, 8), (-1, -1), (-2, -8)], "cbrt": [(1, 1), (8, 2), (-8, -2), (27, 3), (-1, -1)], "abs": [(2, 2), (-3, 3), (4, 4), (-6, 6), (6, 6)]}[kind]
        x0, y0 = r.choice(pts)
        P = lambda x, y: "(%s, %s)" % (ft(x), ft(y))
        right = P(Fr(x0) / b, y0)
        w = [P(Fr(x0) * b, y0), P(x0, Fr(y0) * b), P(Fr(x0) / b, Fr(y0) / b), P(x0 + b, y0)]
        return mcq("The point %s is on the graph of <i>f</i>(<i>x</i>) = %s. Which point is on the graph of <i>g</i>(<i>x</i>) = %s?" % (P(x0, y0), base, g), right, w,
                   "<i>g</i>(%s) = <i>f</i>(%s · %s) = <i>f</i>(%s) = %s. Divide the <i>x</i>-coordinate by %s and keep the <i>y</i>-coordinate. <b>%s</b>." % (ft(Fr(x0) / b), ft(b), ft(Fr(x0) / b), sg(x0), sg(y0), ft(b), right))
    return one_bx


tf_cbrt = tf("cbrt")
one_bx = one_bx_maker(["cube", "cbrt"])


def lin_(h):
    return X if h == 0 else "%s %s %d" % (X, MINUS if h > 0 else "+", abs(h))


def one_cbeq(r):
    kind = r.choice(["a", "b", "c"])
    c = r.choice([n for n in range(-5, 6) if n])
    if kind == "a":
        a = r.choice([1, 2, 3, 4, 5])
        x = r.randint(-12, 12)
        b = c ** 3 - a * x
        q = "Solve ∛(%s) = %s." % (poly([a, b]), sg(c))
        right = "<i>x</i> = %s" % sg(x)
        alt = [Fr(c * c - b, a), Fr(3 * c - b, a), Fr(-c ** 3 - b, a)]
        e = "Cube both sides: %s = %s. So <i>x</i> = %s." % (poly([a, b]), sg(c ** 3), sg(x))
    elif kind == "b":
        m = r.choice([2, 3, 4, -2])
        h = r.randint(-9, 9)
        k = r.choice([n for n in range(-10, 11) if n])
        x = c ** 3 + h
        rhs = m * c + k
        q = "Solve %s∛(%s) %s %d = %s." % (sg(m), lin_(h), "+" if k >= 0 else MINUS, abs(k), sg(rhs))
        right = "<i>x</i> = %s" % sg(x)
        alt = [Fr(c ** 3 - h), Fr(c * c + h), Fr((rhs - k) ** 3 + h) if abs(rhs - k) < 12 else Fr(c ** 3 + h + 2), Fr(-c ** 3 + h)]
        e = "Undo outside first: ∛(%s) = (%s − %s) ÷ %s = %s. Cube: %s = %s, so <i>x</i> = %s." % (lin_(h), sg(rhs), "(%s)" % sg(k) if k < 0 else sg(k), "(%s)" % sg(m) if m < 0 else sg(m), sg(c), lin_(h), sg(c ** 3), sg(x))
    else:
        p = r.choice([2, 3, 4, 5])
        x = r.randint(-9, 9)
        s = r.randint(-9, 9)
        u = s - (p - 1) * x
        q = "Solve ∛(%s) = ∛(%s)." % (poly([p, u]), poly([1, s]))
        right = "<i>x</i> = %s" % sg(x)
        alt = [Fr(s - u, p + 1), Fr(u - s, p - 1), Fr(-x)]
        e = "Cube both sides: %s = %s, so %d<i>x</i> = %s and <i>x</i> = %s." % (poly([p, u]), poly([1, s]), p - 1, sg(s - u), sg(x))
    w = ["<i>x</i> = %s" % ft(v) for v in alt] + ["No real solution"]
    return mcq(q, right, w, e + " A cube root can be negative, so this is a real solution. <b>%s</b>." % right)


def build():
    sets, R = build_sets([
        ("Shifts of f(x) = x³", [("collect", W(fam(tr.one_desc, "cube")), 20)]),
        ("Write and match cubic transformations", [("collect", W(fam(tr.one_write, "cube")), 10), ("collect", W(fam(tr.one_graph, "cube")), 10)]),
        ("Transformations of f(x) = ∛x", [("collect", uniq(tf_cbrt), 20)]),
        ("Horizontal stretches, shrinks and reflections", [("collect", uniq(one_bx), 20)]),
        ("Solve cube root equations", [("collect", uniq(one_cbeq), 20)]),
    ], 69715)
    finish(sets, R)
    body = lesson('<ul><li><i>g</i>(<i>x</i>) = <i>a</i>(<i>b</i>(<i>x</i> − <i>c</i>))<sup>3</sup> + <i>d</i> and <i>g</i>(<i>x</i>) = <i>a</i>∛(<i>b</i>(<i>x</i> − <i>c</i>)) + <i>d</i> move the center point (0, 0) to (<i>c</i>, <i>d</i>).</li><li><i>a</i> stretches or shrinks vertically and a negative <i>a</i> reflects over the <i>x</i>-axis.</li><li><i>bx</i> divides every <i>x</i>-coordinate by <i>b</i>.</li><li>To solve a cube root equation, get the root alone and <b>cube</b> both sides. Cube roots of negative numbers are real: ∛(−8) = −2.</li></ul>',
        [example("∛(2<i>x</i> + 3) = −3", ["2<i>x</i> + 3 = −27"], "<i>x</i> = −15"), example("<i>g</i>(<i>x</i>) = (<i>x</i> + 2)<sup>3</sup> − 1", ["Left 2, down 1"], "Center point (−2, −1)")],
        [['Shifting the wrong way', '(<i>x</i> + 2)<sup>3</sup> moves left 2.'], ['Squaring instead of cubing', 'Undo ∛ by cubing.'], ['Saying a negative has no cube root', '∛(−27) = −3.']])
    faq = [('What does TEKS 2A.6A ask?', 'Analyze the effect on the graphs of f(x) = x³ and f(x) = ∛x when f(x) is replaced by af(x), f(bx), f(x − c), and f(x) + d for specific positive and negative real values of a, b, c, and d.'), ('What does TEKS 2A.6B ask?', 'Solve cube root equations that have real roots.'), ('Can cube root equations have extraneous solutions?', 'No. Cubing does not add solutions, but checking is still a good habit.'), ('What are the domain and range of ∛x?', 'All real numbers for both.')]
    make('cubic-and-cube-root-functions', 15, 'Cubic, Cube Root, Absolute Value, and Rational Functions, Equations, and Inequalities', '2A.6A, 2A.6B',
         '2A.6A analyze the effect on the graphs of f(x) = x^3 and f(x) = ∛x when f(x) is replaced by af(x), f(bx), f(x − c), and f(x) + d for specific positive and negative real values of a, b, c, and d; 2A.6B solve cube root equations that have real roots',
         'Cubic and Cube Root Functions', 'Cubic and Cube Root Functions',
         'Free Algebra II worksheets for Texas TEKS 2A.6A and 2A.6B: transformations of x³ and ∛x, horizontal stretches and reflections, and solving cube root equations. 100 questions with answers.',
         'Undo a cube root by cubing both sides.', '(x − c)³ + d moves the center to (c, d).',
         body, faq, sets, seo_title='Algebra II Cubic and Cube Root Functions Worksheets (TEKS 2A.6A, 2A.6B)')


if __name__ == "__main__":
    build()
