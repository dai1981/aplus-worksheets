# -*- coding: utf-8 -*-
"""
Texas Algebra I: Transformations of Linear Functions (TEKS A.3E)
  python3 tools/gen_ustx_math_a1_linear_transformations.py
How f(x) + d, f(x − c), af(x) and f(bx) change the graph of the parent function f(x) = x: shifts, steeper or less
steep, reflections, new slope and y-intercept, and moving points (own makers).
Wrong answers come from real mistakes: shifting left for f(x − c), reading f(x) + d as a horizontal shift, and
thinking a = 1/2 makes the line steeper.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)

tx_common.GRADE = "algebra-1"

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


def un(n):
    return "unit" if n == 1 else "units"


def ft(v):
    if isinstance(v, Fr) and v.denominator != 1:
        return (MINUS if v < 0 else "") + fr(abs(v.numerator), v.denominator)
    return sg(int(v))


def one_v(r):
    d = r.choice([n for n in range(-9, 10) if n])
    form = r.choice(["<i>g</i>(<i>x</i>) = <i>f</i>(<i>x</i>) %s %d" % ("+" if d > 0 else MINUS, abs(d)), "<i>g</i>(<i>x</i>) = %s %s %d" % (X, "+" if d > 0 else MINUS, abs(d))])
    up = "up" if d > 0 else "down"
    right = "Translated %s %d %s" % (up, abs(d), un(abs(d)))
    w = ["Translated %s %d %s" % ("down" if d > 0 else "up", abs(d), un(abs(d))), "Translated %s %d %s" % ("left" if d > 0 else "right", abs(d), un(abs(d))), "Steeper, with slope %d" % abs(d) if abs(d) > 1 else "Reflected over the <i>x</i>-axis"]
    return mcq("<i>f</i>(<i>x</i>) = %s. How does the graph of %s compare with the graph of <i>f</i>?" % (X, form), right, w,
               "Adding %s outside the function moves every point %s %d. The <i>y</i>-intercept becomes %s: <b>%s</b>." % (sg(d), up, abs(d), sg(d), right.lower()))


def one_h(r):
    c = r.choice([n for n in range(-9, 10) if n])
    nm = r.choice(["g", "h", "p"])
    form = "<i>%s</i>(<i>x</i>) = <i>f</i>(<i>x</i> %s %d)" % (nm, MINUS if c > 0 else "+", abs(c))
    side = "right" if c > 0 else "left"
    right = "Translated %s %d %s" % (side, abs(c), un(abs(c)))
    w = ["Translated %s %d %s" % ("left" if c > 0 else "right", abs(c), un(abs(c))), "Steeper, with slope %d" % abs(c) if abs(c) > 1 else "Less steep, with slope 1/2", "Reflected over the <i>x</i>-axis"]
    return mcq("<i>f</i>(<i>x</i>) = %s. How does the graph of %s compare with the graph of <i>f</i>?" % (X, form), right, w,
               "<i>f</i>(<i>x</i> − <i>c</i>) moves the graph <i>c</i> units right; <i>f</i>(<i>x</i> + <i>c</i>) moves it left. Here: <b>%s</b>." % right.lower())


AS = [Fr(2), Fr(3), Fr(4), Fr(5), Fr(1, 2), Fr(1, 3), Fr(1, 4), Fr(-1), Fr(-2), Fr(-3), Fr(-1, 2), Fr(3, 2)]


def desc(a):
    if a == -1:
        return "Reflected over the <i>x</i>-axis, with slope −1"
    s = []
    if a < 0:
        s.append("Reflected over the <i>x</i>-axis")
    s.append("steeper" if abs(a) > 1 else "less steep")
    t = ", ".join(s)
    return t[0].upper() + t[1:] + ", with slope %s" % ft(a)


def one_a(r):
    a = r.choice(AS)
    kind = r.choice(["a", "b", "plain"])
    if kind == "a":
        form = "<i>g</i>(<i>x</i>) = %s<i>f</i>(<i>x</i>)" % (MINUS if a == -1 else ft(a))
    elif kind == "b":
        form = "<i>g</i>(<i>x</i>) = <i>f</i>(%s<i>x</i>)" % (MINUS if a == -1 else ft(a))
    else:
        form = "<i>g</i>(<i>x</i>) = %s" % ((MINUS + X) if a == -1 else ft(a) + X)
    right = desc(a)
    w = [desc(-a), desc(1 / a) if abs(a) != 1 else "Translated up 1 unit", "Translated up %s %s" % (ft(abs(a)), un(abs(a)))]
    return mcq("<i>f</i>(<i>x</i>) = %s. How does the graph of %s compare with the graph of <i>f</i>?" % (X, form), right, w,
               "For <i>f</i>(<i>x</i>) = <i>x</i>, both <i>af</i>(<i>x</i>) and <i>f</i>(<i>bx</i>) multiply the slope. The new slope is %s: <b>%s</b>." % (ft(a), right[0].lower() + right[1:]))


def one_mb(r):
    m = r.choice([n for n in range(-6, 7) if n not in (0, 1)])
    b = r.choice([n for n in range(-9, 10) if n])
    g = "%s%s %s %d" % ("" if m != -1 else MINUS, (sg(m) if m != -1 else "") + X, "+" if b > 0 else MINUS, abs(b))
    st = lambda mm, bb: "Slope %s and <i>y</i>-intercept %s" % (sg(mm), sg(bb))
    right = st(m, b)
    w = [st(b, m), st(m, -b), st(-m, b)]
    return mcq("The parent function <i>f</i>(<i>x</i>) = %s is changed to <i>g</i>(<i>x</i>) = %s. What are the slope and <i>y</i>-intercept of <i>g</i>?" % (X, g), right, w,
               "The parent has slope 1 and <i>y</i>-intercept 0. <i>g</i> has <b>slope %s and <i>y</i>-intercept %s</b>: %s and moved %s %d." % (sg(m), sg(b), desc(Fr(m)).split(",")[0].lower(), "up" if b > 0 else "down", abs(b)))


def one_pt(r):
    p = r.choice([n for n in range(-6, 7) if n])
    kind = r.choice(["d", "c", "a"])
    if kind == "d":
        d = r.choice([n for n in range(-8, 9) if n])
        form = "<i>g</i>(<i>x</i>) = <i>f</i>(<i>x</i>) %s %d" % ("+" if d > 0 else MINUS, abs(d))
        ans, w = (p, p + d), [(p + d, p), (p - d, p), (p, p - d)]
    elif kind == "c":
        c = r.choice([n for n in range(-8, 9) if n])
        form = "<i>g</i>(<i>x</i>) = <i>f</i>(<i>x</i> %s %d)" % (MINUS if c > 0 else "+", abs(c))
        ans, w = (p + c, p), [(p - c, p), (p, p + c), (p, p - c)]
    else:
        a = r.choice([2, 3, 4, -1, -2, -3])
        form = "<i>g</i>(<i>x</i>) = %s<i>f</i>(<i>x</i>)" % (MINUS if a == -1 else sg(a))
        ans, w = (p, a * p), [(a * p, p), (p, p + a), (-p, p)]
    f = lambda t: "(%s, %s)" % (sg(t[0]), sg(t[1]))
    w = [f(t) for t in w if t != ans]
    return mcq("The point (%s, %s) is on the graph of <i>f</i>(<i>x</i>) = %s. Which point is on the graph of %s?" % (sg(p), sg(p), X, form), f(ans), w,
               "Apply the change to the point: <b>%s</b>." % f(ans))


def build():
    sets, R = build_sets([
        ("Vertical shifts: f(x) + d", [("collect", uniq(one_v), 20)]),
        ("Horizontal shifts: f(x − c)", [("collect", uniq(one_h), 20)]),
        ("Steeper, less steep or reflected: af(x) and f(bx)", [("collect", uniq(one_a), 20)]),
        ("New slope and y-intercept", [("collect", uniq(one_mb), 20)]),
        ("Where does a point move?", [("collect", uniq(one_pt), 20)]),
    ], 69513)
    finish(sets, R)
    body = lesson('<ul><li>The parent function is <i>f</i>(<i>x</i>) = <i>x</i>: slope 1, through (0, 0).</li><li><i>f</i>(<i>x</i>) + <i>d</i> moves the line <b>up</b> <i>d</i> (down if <i>d</i> &lt; 0).</li><li><i>f</i>(<i>x</i> − <i>c</i>) moves it <b>right</b> <i>c</i>; <i>f</i>(<i>x</i> + <i>c</i>) moves it left.</li><li><i>af</i>(<i>x</i>) and <i>f</i>(<i>bx</i>) change the slope: bigger than 1 is steeper, between 0 and 1 is less steep, negative reflects over the <i>x</i>-axis.</li></ul>',
        [example("<i>g</i>(<i>x</i>) = 3<i>x</i> − 2", ["slope 3: steeper", "−2: down 2"], "steeper and translated down 2")],
        [['Shifting left for <i>f</i>(<i>x</i> − <i>c</i>)', 'Minus inside moves right.'], ['Reading <i>f</i>(<i>x</i>) + <i>d</i> as a sideways shift', 'Outside changes move up or down.'], ['Thinking 1/2 makes it steeper', 'A slope of 1/2 is less steep.']])
    faq = [('What does TEKS A.3E ask?', 'Determine the effects on the graph of the parent function f(x) = x when f(x) is replaced by af(x), f(x) + d, f(x − c), f(bx) for specific values of a, b, c, and d.'), ('What is a parent function?', 'The simplest function of a family; for lines it is f(x) = x.'), ('What does a negative a do?', 'It reflects the line over the x-axis.'), ('Do f(x − 3) and f(x) − 3 look the same for f(x) = x?', 'Yes, for this line both give y = x − 3, but one is described as a shift right and the other as a shift down.')]
    make('transformations-of-linear-functions', 13, 'Linear Functions, Equations, and Inequalities', 'A.3E',
         'A.3E determine the effects on the graph of the parent function f(x) = x when f(x) is replaced by af(x), f(x) + d, f(x − c), f(bx) for specific values of a, b, c, and d',
         'Transformations of Linear Functions', 'Transformations of Linear Functions',
         'Free Algebra I worksheets for Texas TEKS A.3E: transformations of the linear parent function f(x) = x with af(x), f(x) + d, f(x − c) and f(bx). 100 questions with answers.',
         '+d outside: up. −c inside: right. a: steeper or less steep.', 'g(x) = 3x − 2 is steeper and down 2.',
         body, faq, sets, seo_title='Algebra I Transformations of Linear Functions Worksheets (TEKS A.3E)')


if __name__ == "__main__":
    build()
