# -*- coding: utf-8 -*-
"""
Texas Precalculus: Polynomial Equations and Inequalities (TEKS P.5I, P.5J)
  python3 tools/gen_ustx_math_pc_polynomial_inequalities.py
Solving polynomial equations by factoring, grouping and quadratic form (own makers) and from one known factor (US
Algebra 2 maker with a new seed), and solving polynomial inequalities with sign charts in interval notation (own makers).
Wrong answers come from real mistakes: dropping the zero x = 0 after factoring out x, forgetting ± in quadratic form,
and ignoring a squared factor in a sign chart.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_a2_polynomial_division_and_remainder_theorem as pd
adopt(pd)
pd.R = random.Random(698270)
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


INF = "∞"


def ivs(pts, signs, incl, want_pos, closed_pts):
    """pts sorted critical numbers; signs: sign on each of len(pts)+1 intervals; closed_pts: set of pts that can be included."""
    out = []
    edges = [None] + pts + [None]
    for i, sgn in enumerate(signs):
        if (sgn > 0) == want_pos:
            lo, hi = edges[i], edges[i + 1]
            lc = lo is not None and incl and lo in closed_pts
            hc = hi is not None and incl and hi in closed_pts
            out.append([lo, hi, lc, hc])
    merged = []
    for seg in out:
        if merged and merged[-1][1] == seg[0] and merged[-1][3] and seg[2]:
            merged[-1][1], merged[-1][3] = seg[1], seg[3]
        else:
            merged.append(seg)
    if incl:
        for p in closed_pts:
            if not any((s[0] is not None and s[0] == p and s[2]) or (s[1] is not None and s[1] == p and s[3]) for s in merged):
                merged.append([p, p, True, True])
    merged.sort(key=lambda s: (-10 ** 9 if s[0] is None else s[0]))
    def one(s):
        if s[0] == s[1] and s[0] is not None:
            return "{%s}" % ft(s[0])
        return "%s%s, %s%s" % ("[" if s[2] else "(", MINUS + INF if s[0] is None else ft(s[0]), INF if s[1] is None else ft(s[1]), "]" if s[3] else ")")
    return " ∪ ".join(one(s) for s in merged) if merged else "No solution"


def sign_at(factors, x):
    """factors: list of (root, power, in_denominator)"""
    s = 1
    for root, pw, den in factors:
        v = (x - root) ** pw
        if v == 0:
            return 0
        s *= 1 if v > 0 else -1
    return s


def solve_ineq(factors, lead, rel):
    pts = sorted(set(f[0] for f in factors))
    edges = [pts[0] - 1] + [(pts[i] + pts[i + 1]) / 2 for i in range(len(pts) - 1)] + [pts[-1] + 1]
    signs = [sign_at(factors, Fr(x)) * (1 if lead > 0 else -1) for x in edges]
    want_pos = rel in ("gt", "ge")
    incl = rel in ("ge", "le")
    closed = set(f[0] for f in factors if not f[2]) - set(f[0] for f in factors if f[2])
    return ivs(pts, signs, incl, want_pos, closed)


REL = {"lt": "&lt;", "le": "≤", "gt": "&gt;", "ge": "≥"}


def fac(root, pw=1):
    b = X if root == 0 else "(%s %s %s)" % (X, MINUS if root > 0 else "+", ft(abs(root)))
    return b + ("<sup>%d</sup>" % pw if pw > 1 else "")


def pmul(p, q):
    out = [0] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        for j, b in enumerate(q):
            out[i + j] += a * b
    return out


def roots_txt(rs):
    return "<i>x</i> = " + ", ".join(ft(v) for v in sorted(set(rs)))


def one_peq(r):
    kind = r.choice(["x", "group", "group"])
    if kind == "x":
        p, q = r.sample([n for n in range(-7, 8) if n], 2)
        a = r.choice([1, 2, 3])
        cs = pmul([a, 0], pmul([1, -p], [1, -q]))
        right = roots_txt([0, p, q])
        w = [roots_txt([p, q]), roots_txt([0, -p, -q]), roots_txt([-p, -q])]
        e = "Factor out %s<i>x</i>: %s<i>x</i>(%s) = 0, so <i>x</i> = 0 is also a solution." % ("" if a == 1 else a, "" if a == 1 else a, poly([1, -(p + q), p * q]))
    else:
        p = r.choice([n for n in range(-6, 7) if n])
        s = r.choice([1, 4, 9, 16, 25])
        cs = pmul([1, -p], [1, 0, -s])
        q = int(s ** 0.5)
        if q == abs(p):
            raise AssertionError
        right = roots_txt([p, q, -q])
        w = [roots_txt([p, q]), roots_txt([-p, q, -q]), roots_txt([p, s, -s])]
        e = "Group: <i>x</i><sup>2</sup>(%s) − %d(%s) = (%s)(<i>x</i><sup>2</sup> − %d) = 0." % (poly([1, -p]), s, poly([1, -p]), poly([1, -p]), s)
    w = [v for v in dict.fromkeys(w) if v != right]
    return mcq("Solve %s = 0." % poly(cs), right, w, e + " <b>%s</b>." % right)


def one_biq(r):
    a, b = r.sample([1, 4, 9, 16, 25, 36], 2)
    neg = r.random() < 0.25
    if neg:
        b = -b
    cs = [1, 0, -(a + b), 0, a * b]
    ra, rb = int(a ** 0.5), int(abs(b) ** 0.5)
    if neg:
        right = "<i>x</i> = ±%d (and ±%s<i>i</i>)" % (ra, "" if rb == 1 else str(rb))
        w = ["<i>x</i> = ±%d and ±%d" % (ra, rb), "<i>x</i> = %d and %s" % (a, sg(b)), "<i>x</i> = ±%d only" % (a)]
        e = "Let <i>u</i> = <i>x</i><sup>2</sup>: (<i>u</i> − %d)(<i>u</i> + %d) = 0. <i>x</i><sup>2</sup> = %d gives ±%d; <i>x</i><sup>2</sup> = −%d has only imaginary solutions ±%s<i>i</i>." % (a, -b, a, ra, -b, "" if rb == 1 else str(rb))
    else:
        right = "<i>x</i> = ±%d and ±%d" % tuple(sorted([ra, rb]))
        w = ["<i>x</i> = %d and %d" % tuple(sorted([ra, rb])), "<i>x</i> = ±%d and ±%d" % tuple(sorted([a, b])), "<i>x</i> = %d and %d" % tuple(sorted([a, b]))]
        e = "Let <i>u</i> = <i>x</i><sup>2</sup>: (<i>u</i> − %d)(<i>u</i> − %d) = 0, so <i>x</i><sup>2</sup> = %d or %d. Take ± square roots." % (a, b, a, b)
    return mcq("Solve %s = 0%s." % (poly(cs), "" if not neg else " (give the real solutions; note any others)"), right, w, e + " <b>%s</b>." % right)


def ineq_item(r, factors, lead, rel, shown):
    right = solve_ineq(factors, lead, rel)
    flip = {"lt": "gt", "gt": "lt", "le": "ge", "ge": "le"}[rel]
    tog = {"lt": "le", "le": "lt", "gt": "ge", "ge": "gt"}[rel]
    w = [solve_ineq(factors, lead, flip), solve_ineq(factors, lead, tog), solve_ineq([(-f[0], f[1], f[2]) for f in factors], lead, rel)]
    w = [v for v in dict.fromkeys(w) if v != right]
    if len(w) < 3:
        w.append(solve_ineq([(f[0], 1, f[2]) for f in factors], lead, rel))
        w = [v for v in dict.fromkeys(w) if v != right]
    if len(w) < 3:
        raise AssertionError
    pts = sorted(set(f[0] for f in factors))
    return mcq("Solve %s %s 0. Write the answer in interval notation." % (shown, REL[rel]), right, w,
               "The zeros %s split the number line. Test a value in each interval (an even power does not change the sign). <b>%s</b>." % (", ".join(ft(p) for p in pts), right))


def one_pin(r):
    rs = sorted(r.sample(range(-7, 8), 3))
    lead = r.choice([1, 1, -1])
    rel = r.choice(["lt", "le", "gt", "ge"])
    shown = ("" if lead == 1 else MINUS) + "".join(fac(v) for v in rs)
    return ineq_item(r, [(v, 1, False) for v in rs], lead, rel, shown)


def one_pin2(r):
    a, b = sorted(r.sample(range(-6, 7), 2))
    pw = r.choice([(2, 1), (1, 2), (2, 2), (3, 1)])
    rel = r.choice(["lt", "le", "gt", "ge"])
    shown = fac(a, pw[0]) + fac(b, pw[1])
    return ineq_item(r, [(a, pw[0], False), (b, pw[1], False)], 1, rel, shown)


def build():
    sets, R = build_sets([
        ("Solve by factoring", [("collect", uniq(one_peq), 20)]),
        ("Equations in quadratic form", [("collect", uniq(one_biq), 20)]),
        ("Factor completely from one factor", [("collect", W(pd.one_full), 20)]),
        ("Polynomial inequalities", [("collect", uniq(one_pin), 20)]),
        ("Inequalities with repeated factors", [("collect", uniq(one_pin2), 20)]),
    ], 69827)
    finish(sets, R)
    body = lesson('<ul><li>To solve a polynomial equation, move everything to one side and factor: by a common factor, by grouping, by quadratic form, or with a known factor.</li><li>Set each factor equal to 0. Do not lose <i>x</i> = 0.</li><li>To solve a polynomial inequality, find the zeros, then make a sign chart: test one value in each interval.</li><li>A factor with an even power does not change the sign. Use [ ] for zeros when the inequality is ≤ or ≥.</li></ul>',
        [example("(<i>x</i> + 2)(<i>x</i> − 1)(<i>x</i> − 4) &gt; 0", ["Zeros −2, 1, 4", "Signs: −, +, −, +"], "(−2, 1) ∪ (4, ∞)")],
        [['Dropping <i>x</i> = 0', '<i>x</i>(<i>x</i> − 3) = 0 has two solutions.'], ['Forgetting ±', '<i>x</i><sup>2</sup> = 9 gives 3 and −3.'], ['Ignoring a squared factor', '(<i>x</i> − 2)<sup>2</sup> keeps the same sign on both sides of 2.']])
    faq = [('What does TEKS P.5I ask?', 'Solve polynomial equations with real coefficients by applying a variety of techniques in mathematical and real-world problems.'), ('What does TEKS P.5J ask?', 'Solve polynomial inequalities with real coefficients by applying a variety of techniques and write the solution set of the polynomial inequality in interval notation in mathematical and real-world problems.'), ('Why test a value in each interval?', 'A polynomial can only change sign at its zeros.'), ('Can the answer be a single point?', 'Yes, for example (x − 2)² ≤ 0 gives only x = 2.')]
    make('polynomial-equations-and-inequalities', 27, 'Algebraic Reasoning', 'P.5I, P.5J',
         'P.5I solve polynomial equations with real coefficients by applying a variety of techniques in mathematical and real-world problems; P.5J solve polynomial inequalities with real coefficients by applying a variety of techniques and write the solution set of the polynomial inequality in interval notation in mathematical and real-world problems',
         'Polynomial Equations and Inequalities', 'Polynomial Inequalities',
         'Free Precalculus worksheets for Texas TEKS P.5I and P.5J: solve polynomial equations by factoring and quadratic form, and polynomial inequalities with sign charts in interval notation. 100 questions with answers.',
         'Factor, then set each factor equal to 0.', 'Inequalities: zeros, then a sign chart.',
         body, faq, sets, seo_title='Precalculus Polynomial Equations and Inequalities Worksheets (TEKS P.5I, P.5J)')


if __name__ == "__main__":
    build()
