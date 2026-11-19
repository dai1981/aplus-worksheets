# -*- coding: utf-8 -*-
"""
Texas Algebra II: Systems of Linear Inequalities (TEKS 2A.3E, 2A.3F, 2A.3G)
  python3 tools/gen_ustx_math_a2_systems_inequalities.py
Matching a system to its graph (US Algebra 1 maker with a new seed), testing points in systems of three
inequalities, writing systems from words and finding possible solutions in context (own makers).
Wrong answers come from real mistakes: reversing at least and at most, testing a point in only one inequality, and
swapping the coefficients.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_a1_systems_of_linear_inequalities as si
adopt(si)
si.R = random.Random(697060)
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


SYMS = [("&lt;", lambda a, b: a < b), ("≤", lambda a, b: a <= b), ("&gt;", lambda a, b: a > b), ("≥", lambda a, b: a >= b)]


def rhs(m, b):
    return poly([m, b]) if m else sg(b)


def make_ineq(r, pt):
    x0, y0 = pt
    kind = r.choice(["line", "line", "line", "v", "h"])
    if kind == "line":
        m, b = r.randint(-3, 3), r.randint(-5, 5)
        if m == 0:
            m = 1
        lhs, val, txt = y0, m * x0 + b, rhs(m, b)
        left, f = "<i>y</i>", (lambda x, y, m=m, b=b: (y, m * x + b))
    elif kind == "v":
        a = r.randint(-5, 5)
        lhs, val, txt, left, f = x0, a, sg(a), "<i>x</i>", (lambda x, y, a=a: (x, a))
    else:
        a = r.randint(-5, 5)
        lhs, val, txt, left, f = y0, a, sg(a), "<i>y</i>", (lambda x, y, a=a: (y, a))
    if lhs == val:
        raise AssertionError
    opts = [s for s in SYMS if s[1](lhs, val)]
    sym = r.choice(opts)
    return "%s %s %s" % (left, sym[0], txt), (lambda x, y, f=f, s=sym: s[1](*f(x, y)))


def one_three(r):
    good = (r.randint(-5, 5), r.randint(-5, 5))
    ins = [make_ineq(r, good) for _ in range(3)]
    if len(set(t for t, _ in ins)) < 3:
        raise AssertionError
    bad = []
    for _ in range(200):
        p = (r.randint(-6, 6), r.randint(-6, 6))
        if p != good and not all(f(*p) for _, f in ins) and p not in bad:
            bad.append(p)
        if len(bad) == 3:
            break
    if len(bad) < 3:
        raise AssertionError
    show = lambda p: "(%s, %s)" % (sg(p[0]), sg(p[1]))
    return mcq("Which point is a solution of the system?<br>%s" % "<br>".join(t for t, _ in ins), show(good), [show(p) for p in bad],
               "Test each point in <b>all three</b> inequalities. Only %s makes every one true. <b>%s</b>." % (show(good), show(good)))


CTX = [("A club sells <i>x</i> cookies for $%(a)d each and <i>y</i> brownies for $%(b)d each. It can bake at most %(n)d items and wants to earn at least $%(m)s.", "cookies", "brownies", "le", "ge"),
       ("Maya mows lawns for $%(a)d an hour (<i>x</i> hours) and tutors for $%(b)d an hour (<i>y</i> hours). She can work at most %(n)d hours a week and wants to earn at least $%(m)s.", "hours mowing", "hours tutoring", "le", "ge"),
       ("A farmer plants <i>x</i> acres of cotton and <i>y</i> acres of corn. He has at most %(n)d acres. Cotton costs $%(a)d an acre and corn $%(b)d an acre, and he can spend at most $%(m)s.", "acres of cotton", "acres of corn", "le", "le"),
       ("A theater sells <i>x</i> adult tickets for $%(a)d and <i>y</i> student tickets for $%(b)d. It has at most %(n)d seats and needs at least $%(m)s in sales.", "adult tickets", "student tickets", "le", "ge"),
       ("A food truck makes <i>x</i> tacos and <i>y</i> burritos. It makes at least %(n)d items a day. Tacos take %(a)d minutes and burritos %(b)d minutes, and there are at most %(m)s minutes of cooking time.", "tacos", "burritos", "ge", "le"),
       ("A store orders <i>x</i> shirts at $%(a)d and <i>y</i> caps at $%(b)d. It needs at least %(n)d items and can spend at most $%(m)s.", "shirts", "caps", "ge", "le")]
SY_ = {"le": "≤", "ge": "≥"}


def ctx(r):
    i = r.randrange(len(CTX))
    t, n1, n2, s1, s2 = CTX[i]
    a, b = r.sample([2, 3, 4, 5, 6, 8, 10, 12, 15], 2)
    n = r.choice([10, 12, 15, 20, 24, 25, 30, 40])
    m = r.randint(n * min(a, b) // 5 + 2, n * max(a, b) // 5 * 4) * 5
    return i, t % {"a": a, "b": b, "n": n, "m": comma(m)}, n1, n2, s1, s2, a, b, n, m


def sysw(s1, s2, a, b, n, m):
    return "<i>x</i> + <i>y</i> %s %d and %d<i>x</i> + %d<i>y</i> %s %s" % (SY_[s1], n, a, b, SY_[s2], comma(m))


def one_form(r):
    i, t, n1, n2, s1, s2, a, b, n, m = ctx(r)
    flip = {"le": "ge", "ge": "le"}
    right = sysw(s1, s2, a, b, n, m)
    w = [sysw(flip[s1], s2, a, b, n, m), sysw(s1, flip[s2], a, b, n, m), sysw(s1, s2, b, a, n, m), sysw(flip[s1], flip[s2], a, b, n, m)]
    return mcq(t + " Which system describes this situation (with <i>x</i> ≥ 0 and <i>y</i> ≥ 0)?", right, w,
               "“At most” means ≤ and “at least” means ≥. Each %s counts %d and each %s counts %d. <b>%s</b>." % (n1.split()[-1][:-1] if False else "x", a, "y", b, right))


def ok(s, v, lim):
    return v <= lim if s == "le" else v >= lim


def one_combo(r):
    i, t, n1, n2, s1, s2, a, b, n, m = ctx(r)
    good, bad = [], []
    for x in range(0, 2 * n + 1):
        for y in range(0, 2 * n + 1):
            c1, c2 = ok(s1, x + y, n), ok(s2, a * x + b * y, m)
            if c1 and c2:
                good.append((x, y))
            elif (c1 or c2) and x + y <= 2 * n:
                bad.append((x, y))
    if not good or len(bad) < 3:
        raise AssertionError
    g = r.choice(good)
    bs = r.sample(bad, 3)
    show = lambda p: "%d %s and %d %s" % (p[0], n1 if p[0] != 1 else n1.replace("hours", "hour").rstrip("s"), p[1], n2 if p[1] != 1 else n2.replace("hours", "hour").rstrip("s"))
    show = lambda p, show=show: show(p).replace("acre of", "acre of").replace("1 acres", "1 acre")
    e = "Check %s: %d + %d = %d %s %d ✓ and %d(%d) + %d(%d) = %s %s %s ✓." % (show(g), g[0], g[1], g[0] + g[1], SY_[s1], n, a, g[0], b, g[1], comma(a * g[0] + b * g[1]), SY_[s2], comma(m))
    return mcq(t + " Which combination is possible?", show(g), [show(p) for p in bs], e + " The others break at least one inequality. <b>%s</b>." % show(g))


def build():
    sets, R = build_sets([
        ("Which system is graphed?", [("collect", W(si.one_graph2), 20)]),
        ("Test points in a system of three inequalities", [("collect", uniq(one_three), 20)]),
        ("Write a system from words", [("collect", uniq(one_form), 20)]),
        ("Possible solutions in context", [("collect", uniq(one_combo), 20)]),
        ("Mixed systems practice", [("collect", uniq(one_three), 10), ("collect", W(si.one_graph2), 10)]),
    ], 69706)
    finish(sets, R)
    body = lesson('<ul><li>The solution of a system of inequalities is the region where <b>all</b> the shadings overlap.</li><li>A point is a solution only if it makes every inequality true.</li><li>“At most” means ≤; “at least” means ≥; “more than” means &gt;.</li><li>In real situations, add <i>x</i> ≥ 0 and <i>y</i> ≥ 0, and keep whole numbers for things you count.</li></ul>',
        [example("Is (2, 1) a solution of <i>y</i> ≤ <i>x</i>, <i>y</i> &gt; −1, <i>x</i> &lt; 4?", ["1 ≤ 2 ✓", "1 &gt; −1 ✓", "2 &lt; 4 ✓"], "Yes")],
        [['Reversing at least and at most', 'At least 20 means ≥ 20.'], ['Testing only one inequality', 'Test every inequality.'], ['Swapping the prices', 'Each price goes with its own variable.']])
    faq = [('What does TEKS 2A.3E ask?', 'Formulate systems of at least two linear inequalities in two variables.'), ('What does TEKS 2A.3F ask?', 'Solve systems of two or more linear inequalities in two variables.'), ('What does TEKS 2A.3G ask?', 'Determine possible solutions in the solution set of systems of two or more linear inequalities in two variables.'), ('Is a point on a dashed line a solution?', 'No. Dashed lines (&lt; or &gt;) are not included.')]
    make('systems-of-linear-inequalities', 6, 'Systems of Equations and Inequalities', '2A.3E, 2A.3F, 2A.3G',
         '2A.3E formulate systems of at least two linear inequalities in two variables; 2A.3F solve systems of two or more linear inequalities in two variables; 2A.3G determine possible solutions in the solution set of systems of two or more linear inequalities in two variables',
         'Systems of Linear Inequalities', 'Systems of Linear Inequalities',
         'Free Algebra II worksheets on systems of linear inequalities for Texas TEKS 2A.3E to 2A.3G: graphs, test points, writing systems from words and possible solutions. 100 questions with answers.',
         'A solution makes every inequality true.', 'At most: ≤. At least: ≥.',
         body, faq, sets, seo_title='Algebra II Systems of Linear Inequalities Worksheets (TEKS 2A.3E–2A.3G)')


if __name__ == "__main__":
    build()
