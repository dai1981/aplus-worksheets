# -*- coding: utf-8 -*-
"""
Texas Precalculus: Rational Inequalities (TEKS P.5K)
  python3 tools/gen_ustx_math_pc_rational_inequalities.py
Critical numbers, signs on intervals, solving rational inequalities in interval notation, inequalities that need one
side to be 0 first, and rational inequalities in context (own makers).
Wrong answers come from real mistakes: including a zero of the denominator, multiplying both sides by the denominator,
and forgetting the zeros of the numerator.
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


def fr_(t, b):
    return "<span class='fr'><span class='fn'>%s</span><span class='fd'>%s</span></span>" % (t, b)


def one_crit(r):
    a, b = r.sample([n for n in range(-8, 9)], 2)
    k = r.choice([1, 2, 3])
    f = fr_(poly([k, -k * a]), fac(b))
    right = "%s and %s" % tuple(ft(v) for v in sorted([a, b]))
    w = ["%s and %s" % tuple(ft(v) for v in sorted([-a, -b])), "%s only" % ft(a), "%s only" % ft(b)]
    return mcq("What are the critical numbers of %s ≥ 0?" % f, right, w,
               "Critical numbers are the zeros of the top (%s) and of the bottom (%s). <b>%s</b>." % (ft(a), ft(b), right))


def one_sign(r):
    a, b = r.sample(range(-8, 9), 2)
    t = r.choice([v for v in range(-10, 11) if v not in (a, b)])
    f = fr_(fac(a), fac(b))
    s = (1 if t > a else -1) * (1 if t > b else -1)
    right = "Positive" if s > 0 else "Negative"
    w = ["Negative" if s > 0 else "Positive", "Zero", "Undefined"]
    return mcq("Is %s positive or negative when <i>x</i> = %s?" % (f, sg(t)), right, w,
               "Top: %s − (%s) = %s; bottom: %s − (%s) = %s. %s. <b>%s</b>." % (sg(t), sg(a), sg(t - a), sg(t), sg(b), sg(t - b), "Same signs give a positive quotient" if s > 0 else "Different signs give a negative quotient", right))


def one_rin(r):
    a, b = r.sample(range(-8, 9), 2)
    rel = r.choice(["lt", "le", "gt", "ge"])
    factors = [(a, 1, False), (b, 1, True)]
    shown = fr_(fac(a), fac(b))
    right = solve_ineq(factors, 1, rel)
    flip = {"lt": "gt", "gt": "lt", "le": "ge", "ge": "le"}[rel]
    w = [solve_ineq(factors, 1, flip), solve_ineq([(a, 1, False), (b, 1, False)], 1, rel), solve_ineq([(-a, 1, False), (-b, 1, True)], 1, rel)]
    w = [v for v in dict.fromkeys(w) if v != right]
    if len(w) < 3:
        w.append(solve_ineq([(b, 1, False), (a, 1, True)], 1, rel))
        w = [v for v in dict.fromkeys(w) if v != right]
    if len(w) < 3:
        raise AssertionError
    return mcq("Solve %s %s 0. Write the answer in interval notation." % (shown, REL[rel]), right, w,
               "Critical numbers %s and %s. Test each interval. %s can never be included: it makes the bottom 0. <b>%s</b>." % (ft(min(a, b)), ft(max(a, b)), ft(b), right))


def one_rin2(r):
    b = r.randint(-6, 6)
    c = r.choice([1, 2, 3, -1, -2])
    a2 = r.randint(-8, 8)
    # (x + a2)/(x - b) >= c  ->  ((1 - c)x + a2 + c b)/(x - b) >= 0
    if c == 1:
        raise AssertionError
    top_root = Fr(-(a2 + c * b), 1 - c)
    if top_root == b:
        raise AssertionError
    rel = r.choice(["lt", "le", "gt", "ge"])
    lead = 1 if (1 - c) > 0 else -1
    factors = [(top_root, 1, False), (Fr(b), 1, True)]
    right = solve_ineq(factors, lead, rel)
    wrongx = Fr(-a2 + c * b * 0 + 0, 1)
    w = [solve_ineq(factors, -lead, rel), solve_ineq([(top_root, 1, False), (Fr(b), 1, False)], lead, rel), solve_ineq([(Fr(c * b - a2), 1, False), (Fr(b), 1, True)], 1, rel) if Fr(c * b - a2) != b else solve_ineq([(top_root + 1, 1, False), (Fr(b), 1, True)], lead, rel)]
    w = [v for v in dict.fromkeys(w) if v != right]
    if len(w) < 3:
        raise AssertionError
    shown = fr_(poly([1, a2]), fac(b))
    return mcq("Solve %s %s %s. Write the answer in interval notation." % (shown, REL[rel], sg(c)), right, w,
               "Do not multiply by %s (its sign changes). Subtract %s and combine: <span class='fr'><span class='fn'>%s</span><span class='fd'>%s</span></span> %s 0. Critical numbers %s and %s. <b>%s</b>." % (
                   fac(b), sg(c), poly([1 - c, a2 + c * b]), fac(b), REL[rel], ft(top_root), sg(b), right))


def one_rword(r):
    kind = r.choice(["cost", "cost", "mix"])
    if kind == "cost":
        F = r.choice([600, 1200, 1500, 2400, 3000, 4800])
        v = r.choice([2, 3, 4, 5, 6, 8])
        tg = v + r.choice([1, 2, 3, 4, 6])
        x = F / (tg - v)
        if x != int(x):
            raise AssertionError
        q = "A company's average cost per item is <i>C</i>(<i>x</i>) = %s dollars for <i>x</i> items. For which numbers of items is the average cost at most $%d?" % (fr_("%s + %d<i>x</i>" % (comma(F), v), "<i>x</i>"), tg)
        right = "<i>x</i> ≥ %s" % comma(int(x))
        w = ["<i>x</i> ≤ %s" % comma(int(x)), "<i>x</i> ≥ %s" % comma(F // tg), "0 &lt; <i>x</i> ≤ %s" % comma(int(x))]
        e = "%s ≤ %d<i>x</i> − %d<i>x</i> (for <i>x</i> &gt; 0), so %s ≤ %d<i>x</i> and <i>x</i> ≥ %s." % (comma(F), tg, v, comma(F), tg - v, comma(int(x)))
    else:
        s = r.choice([10, 20, 30, 40])
        p = r.choice([5, 8, 10, 15])
        goal = r.choice([g for g in (20, 25, 40, 50, 60) if g > p])
        # s liters at p% + x liters pure: (s p/100 + x)/(s + x) >= goal/100
        x = Fr(s * (goal - p), 100 - goal)
        if x.denominator != 1:
            raise AssertionError
        q = "A %d-liter drink is %d%% juice. Pure juice is added: after adding <i>x</i> liters, the juice share is %s. How much juice must be added so the drink is at least %d%% juice?" % (s, p, fr_("%s + <i>x</i>" % ("%g" % (s * p / 100)), "%d + <i>x</i>" % s), goal)
        right = "At least %s liters" % ft(x)
        w = ["At most %s liters" % ft(x), "At least %s liters" % ft(Fr(s * goal, 100)), "At least %d liters" % (goal - p)]
        e = "%s ≥ %s; multiply by %d + <i>x</i> (positive): %s + <i>x</i> ≥ %s + %s<i>x</i>, so <i>x</i> ≥ %s." % (fr_("%s + <i>x</i>" % ("%g" % (s * p / 100)), "%d + <i>x</i>" % s), "%.2f" % (goal / 100), s, "%g" % (s * p / 100), "%g" % (s * goal / 100), "%.2f" % (goal / 100), ft(x))
    return mcq(q, right, w, e + " <b>%s</b>." % right)


def build():
    sets, R = build_sets([
        ("Critical numbers", [("collect", uniq(one_crit), 20)]),
        ("Signs on intervals", [("collect", uniq(one_sign), 20)]),
        ("Solve rational inequalities", [("collect", uniq(one_rin), 20)]),
        ("Get 0 on one side first", [("collect", uniq(one_rin2), 20)]),
        ("Rational inequalities in context", [("collect", uniq(one_rword), 20)]),
    ], 69828)
    finish(sets, R)
    body = lesson('<ul><li>Get 0 on one side and write one fraction. Do <b>not</b> multiply both sides by an expression with <i>x</i>: its sign can change.</li><li>Critical numbers are the zeros of the numerator and of the denominator.</li><li>Test one value in each interval to find the sign of the fraction.</li><li>Zeros of the numerator are included for ≤ and ≥; zeros of the denominator are <b>never</b> included.</li></ul>',
        [example("<span class='fr'><span class='fn'><i>x</i> − 3</span><span class='fd'><i>x</i> + 1</span></span> ≤ 0", ["Critical numbers −1 and 3", "Negative between them"], "(−1, 3]")],
        [['Including a zero of the denominator', 'It makes the fraction undefined.'], ['Multiplying by the denominator', 'Subtract and combine instead.'], ["Forgetting the top's zeros", 'Both top and bottom give critical numbers.']])
    faq = [('What does TEKS P.5K ask?', 'Solve rational inequalities with real coefficients by applying a variety of techniques and write the solution set of the rational inequality in interval notation in mathematical and real-world problems.'), ("Why is the denominator's zero always open?", 'The expression is not defined there.'), ('Can I use a graph?', 'Yes: look where the graph is above or below the x-axis.'), ('When can I multiply by the denominator?', 'Only when you know it is positive, such as a number of items.')]
    make('rational-inequalities', 28, 'Algebraic Reasoning', 'P.5K',
         'P.5K solve rational inequalities with real coefficients by applying a variety of techniques and write the solution set of the rational inequality in interval notation in mathematical and real-world problems',
         'Rational Inequalities', 'Rational Inequalities',
         'Free Precalculus rational inequality worksheets for Texas TEKS P.5K: critical numbers, sign charts, solving in interval notation and real-world rational inequalities. 100 questions with answers.',
         'Critical numbers come from the top and the bottom.', 'A zero of the denominator is never included.',
         body, faq, sets, seo_title='Precalculus Rational Inequalities Worksheets (TEKS P.5K)')


if __name__ == "__main__":
    build()
