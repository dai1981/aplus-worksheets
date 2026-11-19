# -*- coding: utf-8 -*-
"""
Texas Algebra II: Writing a Quadratic Function Through Three Points (TEKS 2A.4A, 2A.4E)
  python3 tools/gen_ustx_math_a2_quadratic_three_points.py
Writing the system for a, b and c, finding y = ax² + bx + c through three points, writing quadratics from tables with
second differences, and projectile models from data (own makers).
Wrong answers come from real mistakes: using x instead of x², a sign error in b, and halving the wrong difference.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)

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


ABC = ["<i>a</i>", "<i>b</i>", "<i>c</i>"]


def tl(cs):
    out = ""
    for c, v in zip(cs, ABC):
        if c == 0:
            continue
        body = ("" if abs(c) == 1 else str(abs(c))) + v
        out += ((MINUS if c < 0 else "") + body) if not out else ((" − " if c < 0 else " + ") + body)
    return out


def coefs(r):
    a = r.choice([1, -1, 2, -2, 3, -3])
    b = r.choice([n for n in range(-7, 8) if n and n != a])
    c = r.choice([n for n in range(-9, 10) if n and n != b])
    return a, b, c


def f(a, b, c, x):
    return a * x * x + b * x + c


def P(x, y):
    return "(%s, %s)" % (sg(x), sg(y))


def eqs(xs, a, b, c, mode=""):
    out = []
    for x in xs:
        y = f(a, b, c, x)
        if mode == "lin":
            row = [x, x * x, 1]
        elif mode == "abs":
            row = [x * x, abs(x), 1]
        elif mode == "sq":
            row = [x * x, x * x, 1]
        else:
            row = [x * x, x, 1]
        out.append("%s = %s" % (tl(row), sg(y)))
    return "; ".join(out)


def one_sys(r):
    a, b, c = coefs(r)
    xs = sorted(r.sample([n for n in range(-3, 5) if n], 3))
    if not any(x < 0 for x in xs):
        raise AssertionError
    pts = ", ".join(P(x, f(a, b, c, x)) for x in xs)
    right = eqs(xs, a, b, c)
    w = [eqs(xs, a, b, c, "lin"), eqs(xs, a, b, c, "abs"), eqs(xs, a, b, c, "sq")]
    return mcq("A parabola <i>y</i> = <i>ax</i><sup>2</sup> + <i>bx</i> + <i>c</i> passes through %s. Which system gives <i>a</i>, <i>b</i> and <i>c</i>?" % pts, right, w,
               "Put each point into <i>y</i> = <i>ax</i><sup>2</sup> + <i>bx</i> + <i>c</i>: <i>x</i><sup>2</sup> goes with <i>a</i> and <i>x</i> (with its sign) goes with <i>b</i>. <b>%s</b>." % right)


def eq(a, b, c):
    return "<i>y</i> = " + poly([a, b, c])


def wr(a, b, c):
    return [eq(a, -b, c), eq(b, a, c), eq(a, b, -c), eq(-a, b, c)]


def one_zero(r):
    a, b, c = coefs(r)
    x1, x2 = r.sample([n for n in range(-3, 4) if n], 2)
    pts = [(0, c), (x1, f(a, b, c, x1)), (x2, f(a, b, c, x2))]
    r.shuffle(pts)
    return mcq("Write the quadratic function whose graph passes through %s." % ", ".join(P(*p) for p in pts), eq(a, b, c), wr(a, b, c),
               "(0, %s) gives <i>c</i> = %s. The other two points give two equations in <i>a</i> and <i>b</i>; solving gives <i>a</i> = %s and <i>b</i> = %s. <b>%s</b>." % (sg(c), sg(c), sg(a), sg(b), eq(a, b, c)))


def one_gen(r):
    a, b, c = coefs(r)
    xs = sorted(r.sample([n for n in range(-4, 5) if n], 3))
    pts = ", ".join(P(x, f(a, b, c, x)) for x in xs)
    return mcq("Write the quadratic function whose graph passes through %s." % pts, eq(a, b, c), wr(a, b, c),
               "Write three equations, one for each point. Subtract pairs to eliminate <i>c</i>, solve for <i>a</i> and <i>b</i>, then find <i>c</i>: <i>a</i> = %s, <i>b</i> = %s, <i>c</i> = %s. <b>%s</b>." % (sg(a), sg(b), sg(c), eq(a, b, c)))


def table(xs, ys):
    return "<table class='sn-table'><tr><th><i>x</i></th>%s</tr><tr><th><i>y</i></th>%s</tr></table>" % ("".join("<td>%s</td>" % sg(v) for v in xs), "".join("<td>%s</td>" % sg(v) for v in ys))


def one_table(r):
    a, b, c = coefs(r)
    s = r.randint(-3, 1)
    xs = list(range(s, s + 5))
    ys = [f(a, b, c, x) for x in xs]
    d1 = [ys[i + 1] - ys[i] for i in range(4)]
    w = wr(a, b, c)
    w[1] = eq(2 * a, b, c)
    return mcq(table(xs, ys) + "Which quadratic function fits the table?", eq(a, b, c), w,
               "First differences: %s. Second differences are all %s, so 2<i>a</i> = %s and <i>a</i> = %s. Then use two points to find <i>b</i> = %s and <i>c</i> = %s. <b>%s</b>." % (
                   ", ".join(sg(v) for v in d1), sg(2 * a), sg(2 * a), sg(a), sg(b), sg(c), eq(a, b, c)))


THINGS = ["ball", "rock", "water balloon", "toy rocket", "beanbag", "soccer ball"]


def one_proj(r):
    v = r.choice(range(32, 97, 8))
    s = r.choice([0, 4, 5, 6, 10, 12, 16, 20, 24, 30, 40, 48])
    h = lambda t: -16 * t * t + v * t + s
    thing = r.choice(THINGS)
    xs = r.choice([[0, 1, 2], [1, 2, 3], [0, 1, 3], [0, 2, 3]])
    if h(xs[-1]) <= 0:
        raise AssertionError
    tb = "<table class='sn-table'><tr><th>Time <i>t</i> (s)</th>%s</tr><tr><th>Height <i>h</i> (ft)</th>%s</tr></table>" % ("".join("<td>%d</td>" % t for t in xs), "".join("<td>%d</td>" % h(t) for t in xs))
    model = "<i>h</i> = −16<i>t</i><sup>2</sup> + %d<i>t</i>%s" % (v, (" + %d" % s) if s else "")
    if r.random() < 0.5:
        right = model
        w = ["<i>h</i> = −16<i>t</i><sup>2</sup> + %d<i>t</i>%s" % (v + 16, (" + %d" % s) if s else ""), "<i>h</i> = 16<i>t</i><sup>2</sup> + %d<i>t</i>%s" % (v - 32, (" + %d" % s) if s else ""),
             "<i>h</i> = −16<i>t</i><sup>2</sup> + %d<i>t</i> + %d" % (v, s + 16), "<i>h</i> = −8<i>t</i><sup>2</sup> + %d<i>t</i>%s" % (v, (" + %d" % s) if s else "")]
        return mcq(tb + "The table shows the height of a %s. Which quadratic model fits the data?" % thing, right, w,
                   "Write three equations for <i>h</i> = <i>at</i><sup>2</sup> + <i>bt</i> + <i>c</i> and solve: <i>a</i> = −16, <i>b</i> = %d, <i>c</i> = %d. <b>%s</b>." % (v, s, model))
    ts = [t for t in range(1, 7) if t not in xs and h(t) > 0]
    if not ts:
        raise AssertionError
    t3 = r.choice(ts)
    right = "%d feet" % h(t3)
    w = ["%d feet" % (h(t3) + 16 * t3), "%d feet" % (h(t3 - 1)) if t3 > 1 else "%d feet" % (h(t3) + 32), "%d feet" % (v * t3 + s), "%d feet" % (h(t3) - 16)]
    w = [x for x in w if x != right and not x.startswith("-")]
    return mcq(tb + "The table shows the height of a %s. Use a quadratic model to predict its height at <i>t</i> = %d seconds." % (thing, t3), right, w,
               "The data fit %s. <i>h</i>(%d) = −16(%d) + %d(%d)%s = <b>%s</b>." % (model, t3, t3 * t3, v, t3, (" + %d" % s) if s else "", right))


def build():
    sets, R = build_sets([
        ("Write the system for a, b and c", [("collect", uniq(one_sys), 20)]),
        ("Quadratic through three points with a y-intercept", [("collect", uniq(one_zero), 20)]),
        ("Quadratic through any three points", [("collect", uniq(one_gen), 20)]),
        ("Quadratic models from tables", [("collect", uniq(one_table), 20)]),
        ("Projectile data and predictions", [("collect", uniq(one_proj), 20)]),
    ], 69707)
    finish(sets, R)
    body = lesson('<ul><li>Three points (with different <i>x</i>-values) decide exactly one parabola <i>y</i> = <i>ax</i><sup>2</sup> + <i>bx</i> + <i>c</i>.</li><li>Put each point into the equation: you get three equations in <i>a</i>, <i>b</i> and <i>c</i>.</li><li>A point (0, <i>c</i>) gives <i>c</i> right away.</li><li>In a table with equal steps in <i>x</i>, the second differences are equal to 2<i>a</i>.</li></ul>',
        [example("Through (0, 3), (1, 4), (2, 9)", ["<i>c</i> = 3", "<i>a</i> + <i>b</i> = 1 and 4<i>a</i> + 2<i>b</i> = 6", "<i>a</i> = 2, <i>b</i> = −1"], "<i>y</i> = 2<i>x</i><sup>2</sup> − <i>x</i> + 3")],
        [['Using <i>x</i> instead of <i>x</i><sup>2</sup> with <i>a</i>', '(−2, 5) gives 4<i>a</i> − 2<i>b</i> + <i>c</i> = 5.'], ['Dropping the sign of <i>x</i>', '<i>x</i> = −2 gives −2<i>b</i>.'], ['Using the second difference as <i>a</i>', 'The second difference is 2<i>a</i>.']])
    faq = [('What does TEKS 2A.4A ask?', 'Write the quadratic function given three specified points in the plane.'), ('What does TEKS 2A.4E ask?', 'Formulate quadratic and square root equations using technology given a table of data.'), ('Why are three points needed?', 'There are three unknowns: a, b and c.'), ('How can a calculator help?', 'Quadratic regression gives a, b and c from the data.')]
    make('quadratic-through-three-points', 7, 'Quadratic and Square Root Functions, Equations, and Inequalities', '2A.4A, 2A.4E',
         '2A.4A write the quadratic function given three specified points in the plane; 2A.4E formulate quadratic and square root equations using technology given a table of data',
         'Writing a Quadratic Function Through Three Points', 'Quadratic Through Three Points',
         'Free Algebra II worksheets for Texas TEKS 2A.4A and 2A.4E: write y = ax² + bx + c through three points, quadratic models from tables and projectile data. 100 questions with answers.',
         'Put each point into y = ax² + bx + c and solve for a, b and c.', 'Second differences = 2a.',
         body, faq, sets, seo_title='Algebra II Quadratic Through Three Points Worksheets (TEKS 2A.4A, 2A.4E)')


if __name__ == "__main__":
    build()
