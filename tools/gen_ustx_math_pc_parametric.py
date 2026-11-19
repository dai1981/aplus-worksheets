# -*- coding: utf-8 -*-
"""
Texas Precalculus: Parametric Equations (TEKS P.3A, P.3B, P.3C)
  python3 tools/gen_ustx_math_pc_parametric.py
Points from parametric equations, eliminating the parameter, writing parametric equations for a rectangular
equation, projectile motion and moving objects (own makers).
Wrong answers come from real mistakes: plugging t into only one equation, solving for t in the wrong equation, and
using the time the object lands as the distance.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)

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


T = "<i>t</i>"


def tp(cs):
    return poly(cs, T)


def P(x, y):
    return "(%s, %s)" % (ft(x), ft(y))


def one_pt(r):
    a, b = r.choice([1, 2, 3, -1, -2]), r.randint(-6, 6)
    c, d = r.choice([1, 2, -1]), r.randint(-6, 6)
    k = r.choice([n for n in range(-4, 5) if n])
    x, y = a * k + b, c * k * k + d
    right = P(x, y)
    w = [P(y, x), P(a * k + b, c * k + d), P(k, y), P(x, -y) if y else P(x, 1)]
    w = [v for v in dict.fromkeys(w) if v != right]
    return mcq("A curve is given by <i>x</i> = %s, <i>y</i> = %s. Which point is on the curve when <i>t</i> = %s?" % (tp([a, b]), tp([c, 0, d]), sg(k)), right, w,
               "Put <i>t</i> = %s into both equations: <i>x</i> = %s, <i>y</i> = %s. <b>%s</b>." % (sg(k), sg(x), sg(y), right))


def one_elim(r):
    kind = r.choice(["par", "line", "circ", "ell"])
    if kind == "par":
        h, k = r.randint(-6, 6), r.randint(-9, 9)
        xs = tp([1, h])
        q = "Eliminate the parameter: <i>x</i> = %s, <i>y</i> = <i>t</i><sup>2</sup> %s %d." % (xs, "+" if k >= 0 else MINUS, abs(k))
        inner = X if h == 0 else "(%s %s %d)" % (X, MINUS if h > 0 else "+", abs(h))
        right = "<i>y</i> = %s<sup>2</sup>%s" % (inner, (" %s %d" % ("+" if k > 0 else MINUS, abs(k))) if k else "")
        inner2 = X if h == 0 else "(%s %s %d)" % (X, "+" if h > 0 else MINUS, abs(h))
        w = ["<i>y</i> = %s<sup>2</sup>%s" % (inner2, (" %s %d" % ("+" if k > 0 else MINUS, abs(k))) if k else ""), "<i>y</i> = <i>x</i><sup>2</sup>%s" % ((" %s %d" % ("+" if k > 0 else MINUS, abs(k))) if k else ""), "<i>x</i> = %s<sup>2</sup>%s" % (inner.replace("<i>x</i>", "<i>y</i>"), (" %s %d" % ("+" if k > 0 else MINUS, abs(k))) if k else "")]
        e = "From the first equation, <i>t</i> = <i>x</i> %s %d. Substitute into the second." % ("−" if h > 0 else "+", abs(h)) if h else "<i>t</i> = <i>x</i>; substitute."
    elif kind == "line":
        a, b, c, d = r.choice([1, 2, 3]), r.randint(-6, 6), r.choice([2, 3, 4, -2, -1]), r.randint(-6, 6)
        q = "Eliminate the parameter: <i>x</i> = %s, <i>y</i> = %s." % (tp([a, b]), tp([c, d]))
        m = Fr(c, a)
        bb = d - m * b
        def ln(m_, b_):
            mt = "" if m_ == 1 else (MINUS if m_ == -1 else ft(m_))
            return "<i>y</i> = %s<i>x</i>%s" % (mt, (" %s %s" % ("+" if b_ > 0 else MINUS, ft(abs(b_)))) if b_ else "")
        right = ln(m, bb)
        w = [ln(1 / m, bb) if 1 / m != m else ln(-m, bb), ln(m, d), ln(m, -bb) if bb else ln(m, 1)]
        e = "<i>t</i> = (<i>x</i> %s %d) ÷ %d. Substitute into <i>y</i>: slope %s ÷ %d = %s." % (MINUS if b >= 0 else "+", abs(b), a, sg(c), a, ft(m))
    elif kind == "circ":
        rr = r.choice([2, 3, 4, 5, 6, 7, 8])
        q = "Eliminate the parameter: <i>x</i> = %d cos <i>t</i>, <i>y</i> = %d sin <i>t</i>." % (rr, rr)
        right = "<i>x</i><sup>2</sup> + <i>y</i><sup>2</sup> = %d" % (rr * rr)
        w = ["<i>x</i><sup>2</sup> + <i>y</i><sup>2</sup> = %d" % rr, "<i>x</i> + <i>y</i> = %d" % rr, "<i>x</i><sup>2</sup> − <i>y</i><sup>2</sup> = %d" % (rr * rr)]
        e = "cos<sup>2</sup> <i>t</i> + sin<sup>2</sup> <i>t</i> = 1, so (<i>x</i>/%d)<sup>2</sup> + (<i>y</i>/%d)<sup>2</sup> = 1." % (rr, rr)
    else:
        a, b = r.sample([2, 3, 4, 5, 6], 2)
        q = "Eliminate the parameter: <i>x</i> = %d cos <i>t</i>, <i>y</i> = %d sin <i>t</i>." % (a, b)
        F = lambda p, s: "<span class='fr'><span class='fn'><i>%s</i><sup>2</sup></span><span class='fd'>%d</span></span>" % (p, s)
        right = "%s + %s = 1" % (F("x", a * a), F("y", b * b))
        w = ["%s + %s = 1" % (F("x", a), F("y", b)), "%s + %s = 1" % (F("x", b * b), F("y", a * a)), "%s − %s = 1" % (F("x", a * a), F("y", b * b))]
        e = "cos <i>t</i> = <i>x</i>/%d and sin <i>t</i> = <i>y</i>/%d; square and add: an ellipse." % (a, b)
    return mcq(q, right, w, e + " <b>%s</b>." % right)


def one_param(r):
    m, b = r.choice([2, 3, -2, -1, 4, 5]), r.choice([n for n in range(-7, 8) if n])
    kind = r.choice(["line", "quad"])
    if kind == "line":
        q = "Which parametric equations represent the line <i>y</i> = %s?" % poly([m, b])
        right = "<i>x</i> = <i>t</i>, <i>y</i> = %s" % tp([m, b])
        w = ["<i>x</i> = %s, <i>y</i> = <i>t</i>" % tp([m, b]), "<i>x</i> = <i>t</i>, <i>y</i> = %s" % tp([b, m]), "<i>x</i> = <i>t</i>, <i>y</i> = %s" % tp([m, -b])]
        e = "Let <i>x</i> = <i>t</i> and replace <i>x</i> with <i>t</i> in the equation."
    else:
        h = r.choice([n for n in range(-5, 6) if n])
        q = "Which parametric equations represent <i>y</i> = %s?" % poly([1, 0, b])
        right = "<i>x</i> = <i>t</i> + %d, <i>y</i> = %s" % (h, tp([1, 2 * h, h * h + b])) if h > 0 else "<i>x</i> = <i>t</i> − %d, <i>y</i> = %s" % (-h, tp([1, 2 * h, h * h + b]))
        w = ["<i>x</i> = <i>t</i> + %d, <i>y</i> = %s" % (h, tp([1, 0, b])) if h > 0 else "<i>x</i> = <i>t</i> − %d, <i>y</i> = %s" % (-h, tp([1, 0, b])),
             "<i>x</i> = <i>t</i><sup>2</sup>, <i>y</i> = %s" % tp([1, b]), "<i>x</i> = <i>t</i>, <i>y</i> = %s" % tp([1, 2 * h, h * h + b])]
        e = "With <i>x</i> = <i>t</i> %s %d, <i>y</i> = (<i>t</i> %s %d)<sup>2</sup> %s %d = %s." % ("+" if h > 0 else "−", abs(h), "+" if h > 0 else "−", abs(h), "+" if b > 0 else "−", abs(b), tp([1, 2 * h, h * h + b]))
    return mcq(q, right, w, e + " <b>%s</b>." % right)


def one_proj(r):
    t1 = r.choice([Fr(-1, 4), Fr(-1, 2)])
    t2 = r.choice([Fr(2), Fr(5, 2), Fr(3), Fr(7, 2), Fr(4), Fr(9, 2), Fr(5)])
    b = 16 * (t1 + t2)
    h = -16 * t1 * t2
    if b.denominator != 1 or h.denominator != 1 or h <= 0:
        raise AssertionError
    vx = r.choice([30, 40, 45, 50, 60, 64, 80])
    thing = r.choice(["A ball", "A golf ball", "A baseball", "A rock"])
    kind = r.choice(["dist", "time", "pos"])
    yq = "<i>y</i> = −16<i>t</i><sup>2</sup> + %d<i>t</i> + %d" % (b, h)
    base = "%s is launched from a height of %d feet. Its position after <i>t</i> seconds is <i>x</i> = %d<i>t</i>, %s (in feet). " % (thing, h, vx, yq)
    dec = lambda v: ("%g" % float(v))
    if kind == "time":
        q = base + "When does it hit the ground?"
        right = "%s seconds" % dec(t2)
        w = ["%s seconds" % dec(-t1), "%s seconds" % dec(t2 / 2), "%s seconds" % dec(t2 * 2)]
        e = "Set <i>y</i> = 0: 16<i>t</i><sup>2</sup> − %d<i>t</i> − %d = 0, so <i>t</i> = %s or <i>t</i> = %s. Time cannot be negative." % (b, h, dec(t2), dec(t1).replace("-", MINUS))
    elif kind == "dist":
        q = base + "How far does it travel horizontally before it hits the ground?"
        right = "%s feet" % comma(int(vx * t2)) if (vx * t2).denominator == 1 else "%s feet" % dec(vx * t2)
        w = ["%s seconds" % dec(t2), "%s feet" % dec(vx * t2 / 2), "%s feet" % dec(vx + t2)]
        e = "It lands at <i>t</i> = %s (where <i>y</i> = 0). <i>x</i> = %d × %s = %s." % (dec(t2), vx, dec(t2), right)
    else:
        tt = r.choice([1, 2])
        y = -16 * tt * tt + b * tt + h
        q = base + "Where is it at <i>t</i> = %d?" % tt
        right = "(%d, %s)" % (vx * tt, comma(int(y)))
        w = ["(%s, %d)" % (comma(int(y)), vx * tt), "(%d, %s)" % (vx, comma(int(y))), "(%d, %s)" % (vx * tt, comma(int(b * tt + h)))]
        e = "<i>x</i> = %d(%d) = %d; <i>y</i> = −16(%d) + %d(%d) + %d = %s." % (vx, tt, vx * tt, tt * tt, b, tt, h, comma(int(y)))
    return mcq(q, right, w, e + " <b>%s</b>." % right)


def one_move(r):
    x0, y0 = r.randint(-6, 6), r.randint(2, 12)
    vx, vy = r.choice([1, 2, 3, -1, -2]), -r.choice([1, 2, 3, 4])
    kind = r.choice(["start", "cross", "dir"])
    xs, ys = tp([vx, x0]), tp([vy, y0])
    base = "An object moves so that <i>x</i> = %s and <i>y</i> = %s, where <i>t</i> is time in seconds. " % (xs, ys)
    if kind == "start":
        right = P(x0, y0)
        w = [P(vx, vy), P(y0, x0), P(x0 + vx, y0 + vy)]
        q = base + "Where does it start (at <i>t</i> = 0)?"
        e = "At <i>t</i> = 0 only the constants remain."
    elif kind == "cross":
        t = Fr(y0, -vy)
        right = "At <i>t</i> = %s, at the point %s" % (ft(t), P(x0 + vx * t, 0))
        w = ["At <i>t</i> = %s, at the point %s" % (ft(t), P(0, x0 + vx * t)), "At <i>t</i> = %s, at the point %s" % (ft(t + 1), P(x0 + vx * (t + 1), 0)),
             "At <i>t</i> = %d, at the point %s" % (y0, P(x0 + vx * y0, 0))]
        q = base + "When and where does it cross the <i>x</i>-axis?"
        e = "Set <i>y</i> = 0: %s = 0 gives <i>t</i> = %s. Then <i>x</i> = %s." % (ys, ft(t), ft(x0 + vx * t))
    else:
        right = "%s and %s" % ("Right" if vx > 0 else "Left", "down")
        w = ["%s and up" % ("Right" if vx > 0 else "Left"), "%s and down" % ("Left" if vx > 0 else "Right"), "%s and up" % ("Left" if vx > 0 else "Right")]
        q = base + "As <i>t</i> increases, which way does it move?"
        e = "<i>x</i> changes by %s each second and <i>y</i> by %s each second." % (sg(vx), sg(vy))
    w = [v for v in dict.fromkeys(w) if v != right]
    return mcq(q, right, w, e + " <b>%s</b>." % right)


def build():
    sets, R = build_sets([
        ("Points on a parametric curve", [("collect", uniq(one_pt), 20)]),
        ("Eliminate the parameter", [("collect", uniq(one_elim), 20)]),
        ("Write parametric equations", [("collect", uniq(one_param), 20)]),
        ("Moving objects", [("collect", uniq(one_move), 20)]),
        ("Projectile motion", [("collect", uniq(one_proj), 20)]),
    ], 69821)
    finish(sets, R)
    body = lesson('<ul><li><b>Parametric equations</b> give <i>x</i> and <i>y</i> in terms of a third variable, the parameter <i>t</i> (often time).</li><li>To plot, make a table of <i>t</i>, <i>x</i> and <i>y</i>. The curve has a direction as <i>t</i> increases.</li><li>To eliminate the parameter, solve one equation for <i>t</i> and substitute, or use cos<sup>2</sup> <i>t</i> + sin<sup>2</sup> <i>t</i> = 1.</li><li>To write parametric equations for <i>y</i> = <i>f</i>(<i>x</i>), let <i>x</i> = <i>t</i> and <i>y</i> = <i>f</i>(<i>t</i>).</li></ul>',
        [example("<i>x</i> = <i>t</i> + 2, <i>y</i> = <i>t</i><sup>2</sup> − 1", ["<i>t</i> = <i>x</i> − 2"], "<i>y</i> = (<i>x</i> − 2)<sup>2</sup> − 1")],
        [['Using <i>t</i> in only one equation', 'Put <i>t</i> into both.'], ['Solving for <i>t</i> in the harder equation', 'Use the simpler one.'], ['Landing time as distance', 'Find <i>x</i> at that time.']])
    faq = [('What does TEKS P.3A ask?', 'Graph a set of parametric equations.'), ('What does TEKS P.3B ask?', 'Convert parametric equations into rectangular relations and convert rectangular relations into parametric equations.'), ('What does TEKS P.3C ask?', 'Use parametric equations to model and solve mathematical and real-world problems.'), ('Why use parametric equations?', 'They show where an object is and when it is there.')]
    make('parametric-equations', 21, 'Relations and Geometric Reasoning', 'P.3A, P.3B, P.3C',
         'P.3A graph a set of parametric equations; P.3B convert parametric equations into rectangular relations and convert rectangular relations into parametric equations; P.3C use parametric equations to model and solve mathematical and real-world problems',
         'Parametric Equations', 'Parametric Equations',
         'Free Precalculus worksheets on parametric equations for Texas TEKS P.3A to P.3C: points, eliminating the parameter, writing parametric equations, motion and projectiles. 100 questions with answers.',
         'Solve one equation for t and substitute into the other.', 'For y = f(x), let x = t and y = f(t).',
         body, faq, sets, seo_title='Precalculus Parametric Equations Worksheets (TEKS P.3A–P.3C)')


if __name__ == "__main__":
    build()
