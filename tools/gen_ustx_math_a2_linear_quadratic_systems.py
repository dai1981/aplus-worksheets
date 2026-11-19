# -*- coding: utf-8 -*-
"""
Texas Algebra II: Systems of a Linear and a Quadratic Equation (TEKS 2A.3C, 2A.3D)
  python3 tools/gen_ustx_math_a2_linear_quadratic_systems.py
Setting a line and a parabola equal, finding the x-coordinates and points of intersection, deciding how many
solutions there are with the discriminant, and choosing reasonable solutions in context (own makers).
Wrong answers come from real mistakes: adding the line instead of subtracting it, using the wrong y-value, and keeping a
negative time.
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


def ln(m, k):
    return "<i>y</i> = " + poly([m, k])


def pb(a, b, c):
    return "<i>y</i> = " + poly([a, b, c])


def gen(r):
    a = r.choice([1, 1, 1, -1, 2])
    p, q = sorted(r.sample(range(-6, 7), 2))
    m = r.choice([n for n in range(-4, 5)])
    k = r.randint(-8, 8)
    b = m - a * (p + q)
    c = k + a * p * q
    if abs(b) > 14 or abs(c) > 30:
        raise AssertionError
    return a, b, c, m, k, p, q


def sysq(a, b, c, m, k):
    return "%s<br>%s" % (pb(a, b, c), ln(m, k))


def one_set(r):
    a, b, c, m, k, p, q = gen(r)
    right = poly([a, b - m, c - k]) + " = 0"
    w = [poly([a, b + m, c + k]) + " = 0", poly([a, b - m, c + k]) + " = 0", poly([a, b + m, c - k]) + " = 0", poly([a, m - b, k - c]) + " = 0"]
    w = [v for v in dict.fromkeys(w) if v != right]
    return mcq("Substitute to solve the system. Which equation do you get after moving every term to one side?<br>%s" % sysq(a, b, c, m, k), right, w,
               "Set %s = %s, then subtract %s from both sides: <b>%s</b>." % (poly([a, b, c]), poly([m, k]), poly([m, k]), right))


def xs(p, q):
    return "<i>x</i> = %s and <i>x</i> = %s" % (sg(p), sg(q))


def one_x(r):
    a, b, c, m, k, p, q = gen(r)
    right = xs(p, q)
    w = [xs(-q, -p), "<i>x</i> = %s only" % sg(q), xs(p, m * p + k) if m * p + k != q else xs(p + 1, q), xs(p, -q) if q else xs(p, 1)]
    w = [v for v in dict.fromkeys(w) if v != right]
    return mcq("Find the <i>x</i>-coordinates where the parabola and the line meet.<br>%s" % sysq(a, b, c, m, k), right, w,
               "%s = 0 factors as %s(<i>x</i> %s %d)(<i>x</i> %s %d) = 0. <b>%s</b>." % (poly([a, b - m, c - k]), "" if a == 1 else sg(a), MINUS if p > 0 else "+", abs(p), MINUS if q > 0 else "+", abs(q), right))


def pt(x, y):
    return "(%s, %s)" % (sg(x), sg(y))


def one_pts(r):
    a, b, c, m, k, p, q = gen(r)
    yp, yq = m * p + k, m * q + k
    right = "%s and %s" % (pt(p, yp), pt(q, yq))
    w = ["%s and %s" % (pt(p, yq), pt(q, yp)), "%s and %s" % (pt(yp, p), pt(yq, q)), "%s and %s" % (pt(-p, yp), pt(-q, yq)), "%s and %s" % (pt(p, c), pt(q, c))]
    w = [v for v in dict.fromkeys(w) if v != right]
    if len(w) < 3:
        raise AssertionError
    return mcq("Solve the system.<br>%s" % sysq(a, b, c, m, k), right, w,
               "%s = 0 gives <i>x</i> = %s or <i>x</i> = %s. Put each into the line: <i>y</i> = %s and <i>y</i> = %s. <b>%s</b>." % (poly([a, b - m, c - k]), sg(p), sg(q), sg(yp), sg(yq), right))


NS = ["No solutions", "Exactly one solution", "Two solutions", "Infinitely many solutions"]


def one_count(r):
    want = r.choice([0, 1, 2])
    m, k = r.randint(-4, 4), r.randint(-6, 6)
    B = r.choice([n for n in range(-8, 9) if n % 2 == 0]) if want == 1 else r.randint(-8, 8)
    if want == 1:
        C = (B // 2) ** 2
    elif want == 0:
        C = (B * B) // 4 + r.randint(1, 9)
    else:
        C = (B * B) // 4 - r.randint(1, 12)
        if B % 2:
            C = (B * B - 1) // 4 - r.randint(0, 10)
    b, c = B + m, C + k
    D = B * B - 4 * C
    right = NS[2 if D > 0 else 1 if D == 0 else 0]
    return mcq("How many solutions does the system have?<br>%s<br>%s" % (pb(1, b, c), ln(m, k)), right, [v for v in NS if v != right],
               "Set them equal: %s = 0. The discriminant is (%s)<sup>2</sup> − 4(1)(%s) = %s, which is %s. <b>%s</b>." % (
                   poly([1, B, C]), sg(B), sg(C), sg(D), "positive" if D > 0 else "zero" if D == 0 else "negative", right))


def dec(v):
    v = Fr(v)
    return str(int(v)) if v.denominator == 1 else ("%.2f" % float(v)).rstrip("0").rstrip(".").replace("-", MINUS)


CTX = [("A ball is thrown upward from a balcony", "A drone rises from a rooftop"), ("A water balloon is launched from a tower", "A hot-air balloon rises from a platform"),
       ("A rock is thrown upward from a cliff", "A window-washing lift rises along a building"), ("A rocket toy is launched from a deck", "A camera on a pole is raised")]


def one_reason(r):
    t1 = r.choice([Fr(-1, 2), Fr(-1, 4), Fr(-1), Fr(-3, 4)])
    t2 = r.choice([Fr(1), Fr(3, 2), Fr(2), Fr(5, 2), Fr(3), Fr(7, 2), Fr(4)])
    m = r.choice([2, 4, 5, 6, 8, 10])
    kk = r.choice([0, 5, 10, 15, 20, 30])
    b = m + 16 * (t1 + t2)
    s = kk - 16 * t1 * t2
    if b.denominator != 1 or s.denominator != 1 or b <= 0:
        raise AssertionError
    one, two = r.choice(CTX)
    h1 = "−16<i>t</i><sup>2</sup> + %d<i>t</i> + %d" % (b, s)
    h2 = ("%d<i>t</i> + %d" % (m, kk)) if kk else "%d<i>t</i>" % m
    q = "%s. Its height is <i>h</i> = %s feet after <i>t</i> seconds. %s; its height is <i>h</i> = %s feet. When are they at the same height?" % (one, h1, two, h2)
    right = "<i>t</i> = %s seconds only" % dec(t2)
    w = ["<i>t</i> = %s and <i>t</i> = %s seconds" % (dec(t1), dec(t2)), "<i>t</i> = %s seconds only" % dec(-t1), "<i>t</i> = %s seconds only" % dec(t1)]
    return mcq(q, right, w, "Set them equal: 16<i>t</i><sup>2</sup> %s %s<i>t</i> %s %s = 0, so <i>t</i> = %s or <i>t</i> = %s. Time cannot be negative, so <b>%s</b>." % (
        "+" if m - b > 0 else MINUS, dec(abs(m - b)), "+" if kk - s > 0 else MINUS, dec(abs(kk - s)), dec(t1), dec(t2), right))


def build():
    sets, R = build_sets([
        ("Set the equations equal", [("collect", uniq(one_set), 20)]),
        ("Find the x-coordinates", [("collect", uniq(one_x), 20)]),
        ("Solve the system", [("collect", uniq(one_pts), 20)]),
        ("How many solutions?", [("collect", uniq(one_count), 20)]),
        ("Reasonable solutions in context", [("collect", uniq(one_reason), 20)]),
    ], 69705)
    finish(sets, R)
    body = lesson('<ul><li>A line and a parabola can meet at 0, 1 or 2 points.</li><li>Substitute: set the two expressions for <i>y</i> equal, move every term to one side, and solve the quadratic.</li><li>Put each <i>x</i> into the line to get <i>y</i>. Check in both equations.</li><li>The discriminant <i>b</i><sup>2</sup> − 4<i>ac</i> tells how many: positive → 2, zero → 1, negative → 0.</li><li>In context, drop solutions that make no sense, like negative time.</li></ul>',
        [example("<i>y</i> = <i>x</i><sup>2</sup> − 2<i>x</i> − 1 and <i>y</i> = <i>x</i> + 3", ["<i>x</i><sup>2</sup> − 3<i>x</i> − 4 = 0", "(<i>x</i> − 4)(<i>x</i> + 1) = 0"], "(4, 7) and (−1, 2)")],
        [['Adding the line instead of subtracting', 'Move every term of the line to the other side.'], ['Using the wrong <i>y</i>', 'Put each <i>x</i> into the line or the parabola.'], ['Keeping a negative time', 'Time and length cannot be negative.']])
    faq = [('What does TEKS 2A.3C ask?', 'Solve, algebraically, systems of two equations in two variables consisting of a linear equation and a quadratic equation.'), ('What does TEKS 2A.3D ask?', 'Determine the reasonableness of solutions to systems of a linear equation and a quadratic equation in two variables.'), ('Can a line touch a parabola at exactly one point?', 'Yes. The line is tangent and the discriminant is 0.'), ('Can there be three solutions?', 'No. A line and a parabola meet at most twice.')]
    make('linear-quadratic-systems', 5, 'Systems of Equations and Inequalities', '2A.3C, 2A.3D',
         '2A.3C solve, algebraically, systems of two equations in two variables consisting of a linear equation and a quadratic equation; 2A.3D determine the reasonableness of solutions to systems of a linear equation and a quadratic equation in two variables',
         'Systems of a Linear and a Quadratic Equation', 'Linear-Quadratic Systems',
         'Free Algebra II worksheets on linear-quadratic systems for Texas TEKS 2A.3C and 2A.3D: substitution, points of intersection, number of solutions and reasonable solutions. 100 questions with answers.',
         'Set the line and the parabola equal and solve the quadratic.', 'Discriminant > 0: 2 solutions; = 0: 1; < 0: none.',
         body, faq, sets, seo_title='Algebra II Linear-Quadratic Systems Worksheets (TEKS 2A.3C, 2A.3D)')


if __name__ == "__main__":
    build()
