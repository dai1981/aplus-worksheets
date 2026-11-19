# -*- coding: utf-8 -*-
"""
Texas Algebra II: Radicals with Variables and Rational Exponent Equations (TEKS 2A.7G, 2A.7H)
  python3 tools/gen_ustx_math_a2_radicals_rational_exponents.py
Simplifying square roots with variables (US Algebra 1 maker with a new seed), simplifying cube roots and fourth roots
with variables, rewriting between radicals and rational exponents, and solving equations with rational exponents
(own makers).
Wrong answers come from real mistakes: dividing the exponent by 2 for a cube root, swapping the numerator and the
denominator of the exponent, and forgetting ± for an even power.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_a1_simplifying_radicals as rd
adopt(rd)
rd.R = random.Random(697230)
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


ROOT = {3: "∛", 4: "∜"}


def xp(e, v="<i>x</i>"):
    if e == 0:
        return ""
    return v if e == 1 else "%s<sup>%d</sup>" % (v, e)


def one_nroot(r):
    n = r.choice([3, 3, 3, 4])
    k = r.choice([1, 2, 3]) if n == 3 else r.choice([1, 2])
    rest = r.choice([1, 2, 3, 4, 5, 6, 7]) if n == 3 else r.choice([1, 2, 3, 5])
    c = k ** n * rest
    m = r.randint(n, 3 * n + 2)
    q2 = r.randint(0, 2 * n)
    if c == 1 or (rest == 1 and m % n == 0 and q2 % n == 0):
        raise AssertionError
    inside = "%s%s%s" % (comma(c), xp(m), xp(q2, "<i>y</i>"))
    outc = "" if k == 1 else str(k)
    out = outc + xp(m // n) + xp(q2 // n, "<i>y</i>")
    innr = ("" if rest == 1 else str(rest)) + xp(m % n) + xp(q2 % n, "<i>y</i>")
    def show(o, i):
        if not i:
            return o or "1"
        return "%s%s(%s)" % (o, ROOT[n], i) if len(i) > 1 or not i.isdigit() else "%s%s%s" % (o, ROOT[n], i)
    right = show(out, innr)
    w = [show(outc + xp(m // 2) + xp(q2 // 2, "<i>y</i>"), ("" if rest == 1 else str(rest)) + xp(m % 2) + xp(q2 % 2, "<i>y</i>")),
         show(comma(c) + xp(m // n) + xp(q2 // n, "<i>y</i>"), xp(m % n) + xp(q2 % n, "<i>y</i>")),
         show(outc + xp(m - n) + xp(max(q2 - n, 0), "<i>y</i>"), innr),
         show(outc + xp(m // n), ("" if rest == 1 else str(rest)) + xp(m % n) + xp(q2, "<i>y</i>"))]
    w = [v for v in dict.fromkeys(w) if v != right]
    return mcq("Simplify %s(%s)%s." % (ROOT[n], inside, ", where <i>x</i> ≥ 0 and <i>y</i> ≥ 0" if n == 4 else ""), right, w,
               "Take out groups of %d: %s = %s<sup>%d</sup> · %s, and each exponent is divided by %d (the remainder stays inside). <b>%s</b>." % (
                   n, comma(c), k, n, rest, n, right))


def one_conv(r):
    n = r.choice([2, 3, 4, 5])
    m = r.choice([e for e in range(1, 8) if e % n and e != 1] or [1])
    if m == 1 and n == 2:
        m = 3
    v = r.choice(["<i>x</i>", "<i>y</i>", "<i>a</i>"])
    co = r.choice([1, 1, 2, 3, 5])
    rt = "√" if n == 2 else {3: "∛", 4: "∜"}.get(n, "<sup>%d</sup>√" % n)
    ex = "<sup>%d/%d</sup>" % (m, n)
    if r.random() < 0.5:
        q = "Write %s%s%s using a radical." % ("" if co == 1 else co, v, ex)
        right = "%s%s(%s<sup>%d</sup>)" % ("" if co == 1 else co, rt, v, m)
        w = ["%s%s(%s<sup>%d</sup>)" % ("" if co == 1 else co, {2: "√", 3: "∛", 4: "∜"}.get(m, "<sup>%d</sup>√" % m), v, n),
             "%s(%s%s)<sup>%d</sup>" % (rt, "" if co == 1 else co, v, m) if co != 1 else "<span class='fr'><span class='fn'>%d</span><span class='fd'>%d</span></span>%s" % (m, n, v),
             "%s%s(%s<sup>%d</sup>)" % ("" if co == 1 else co, rt, v, m * n)]
        e = "The denominator %d is the root and the numerator %d is the power: <b>%s</b>." % (n, m, right)
    else:
        q = "Write %s%s(%s<sup>%d</sup>) with a rational exponent." % ("" if co == 1 else co, rt, v, m)
        right = "%s%s%s" % ("" if co == 1 else co, v, ex)
        w = ["%s%s<sup>%d/%d</sup>" % ("" if co == 1 else co, v, n, m), "%s%s<sup>%d</sup>" % ("" if co == 1 else co, v, m * n), "%s%s<sup>%d</sup>" % ("" if co == 1 else co, v, m - n) if m - n > 0 else "%s%s<sup>%d</sup>" % ("" if co == 1 else co, v, m + n)]
        e = "The power goes on top and the root on the bottom: <b>%s</b>." % right
    return mcq(q, right, w, e)


def one_req(r):
    n = r.choice([2, 3, 4])
    from math import gcd
    m = r.choice([e for e in range(2, 6) if gcd(e, n) == 1])
    base = r.randint(2, 10)
    x = base ** n
    rhs = base ** m
    if rhs > 10000 or x > 10000:
        raise AssertionError
    q = "Solve <i>x</i><sup>%d/%d</sup> = %s." % (m, n, comma(rhs))
    if m % 2 == 0:
        right = "<i>x</i> = ±%s" % comma(x)
        w = ["<i>x</i> = %s" % comma(x), "<i>x</i> = ±%s" % ft(Fr(rhs * n, m)), "<i>x</i> = ±%s" % comma(rhs ** 2) if rhs ** 2 < 100000 else "<i>x</i> = ±%d" % (x + 1)]
        e = "Raise both sides to the %d/%d power: <i>x</i> = ±(%s)<sup>%d/%d</sup> = ±%d<sup>%d</sup> = ±%s. An even power hides the sign, so both answers work." % (n, m, comma(rhs), n, m, base, n, comma(x))
    else:
        right = "<i>x</i> = %s" % comma(x)
        w = ["<i>x</i> = %s" % ft(Fr(rhs * n, m)), "<i>x</i> = %s" % comma(rhs ** 2) if rhs ** 2 != x else "<i>x</i> = %d" % (x + 1), "<i>x</i> = %d" % base]
        e = "Raise both sides to the %d/%d power (the reciprocal): <i>x</i> = (%s)<sup>%d/%d</sup> = %d<sup>%d</sup> = %s." % (n, m, comma(rhs), n, m, base, n, comma(x))
    return mcq(q, right, w, e + " <b>%s</b>." % right)


def one_req2(r):
    m, n = r.choice([(3, 2), (1, 3), (5, 3), (1, 2), (3, 4), (5, 2)])
    base = r.choice([2, 3]) if m >= 5 or n == 4 else r.choice([2, 3, 4])
    a = r.choice([2, 3, 4, 5])
    b = r.choice([n_ for n_ in range(-20, 21) if n_])
    h = r.choice([0, 0, 1, 2, 3, -1, -2])
    x = base ** n + h
    rhs = a * base ** m + b
    inner = "<i>x</i>" if h == 0 else "(<i>x</i> %s %d)" % (MINUS if h > 0 else "+", abs(h))
    q = "Solve %d%s<sup>%d/%d</sup> %s %d = %s." % (a, inner, m, n, "+" if b > 0 else MINUS, abs(b), sg(rhs))
    right = "<i>x</i> = %s" % sg(x)
    w = ["<i>x</i> = %s" % sg(base ** n - h) if h else "<i>x</i> = %s" % sg(base ** m), "<i>x</i> = %s" % ft(Fr((rhs - b), a) ** 2 + h) if Fr(rhs - b, a) ** 2 + h != x else "<i>x</i> = %s" % sg(x + 2),
         "<i>x</i> = %s" % sg(base ** n + h + a), "<i>x</i> = %s" % sg(base + h)]
    return mcq(q, right, w, "Undo outside first: %s<sup>%d/%d</sup> = (%s − %s) ÷ %d = %d. Then raise to the %d/%d power: %s = %d<sup>%d</sup> = %d. <b>%s</b>." % (
        inner, m, n, sg(rhs), "(%s)" % sg(b) if b < 0 else sg(b), a, base ** m, n, m, inner, base, n, base ** n, right))


def build():
    sets, R = build_sets([
        ("Simplify square roots with variables", [("collect", W(rd.one_var), 20)]),
        ("Simplify cube roots and fourth roots", [("collect", uniq(one_nroot), 20)]),
        ("Radicals and rational exponents", [("collect", uniq(one_conv), 20)]),
        ("Solve x^(m/n) = c", [("collect", uniq(one_req), 20)]),
        ("Multi-step rational exponent equations", [("collect", uniq(one_req2), 20)]),
    ], 69723)
    finish(sets, R)
    body = lesson('<ul><li><i>x</i><sup><i>m</i>/<i>n</i></sup> = <sup><i>n</i></sup>√(<i>x</i><sup><i>m</i></sup>) = (<sup><i>n</i></sup>√<i>x</i>)<sup><i>m</i></sup>: the denominator is the root, the numerator is the power.</li><li>To simplify an <i>n</i>th root, take out groups of <i>n</i>: ∛(<i>x</i><sup>7</sup>) = <i>x</i><sup>2</sup>∛<i>x</i>.</li><li>To solve <i>x</i><sup><i>m</i>/<i>n</i></sup> = <i>c</i>, raise both sides to the reciprocal power <i>n</i>/<i>m</i>.</li><li>If <i>m</i> is even, there are two answers (±).</li></ul>',
        [example("<i>x</i><sup>3/2</sup> = 27", ["<i>x</i> = 27<sup>2/3</sup>", "∛27 = 3, 3<sup>2</sup> = 9"], "<i>x</i> = 9"), example("∛(16<i>x</i><sup>5</sup>)", ["16 = 8 · 2, <i>x</i><sup>5</sup> = <i>x</i><sup>3</sup> · <i>x</i><sup>2</sup>"], "2<i>x</i>∛(2<i>x</i><sup>2</sup>)")],
        [['Dividing by 2 for a cube root', 'For ∛, take out groups of 3.'], ['Swapping the parts of the exponent', '<i>x</i><sup>2/3</sup> is ∛(<i>x</i><sup>2</sup>).'], ['Forgetting ±', '<i>x</i><sup>2/3</sup> = 4 gives <i>x</i> = ±8.']])
    faq = [('What does TEKS 2A.7G ask?', 'Rewrite radical expressions that contain variables to equivalent forms.'), ('What does TEKS 2A.7H ask?', 'Solve equations involving rational exponents.'), ('Why do even roots need x ≥ 0?', 'So the expression is a real number without absolute value signs.'), ('Is x^(1/2) the same as √x?', 'Yes, for x ≥ 0.')]
    make('radicals-and-rational-exponents', 23, 'Number and Algebraic Methods', '2A.7G, 2A.7H',
         '2A.7G rewrite radical expressions that contain variables to equivalent forms; 2A.7H solve equations involving rational exponents',
         'Radicals with Variables and Rational Exponent Equations', 'Radicals and Rational Exponents',
         'Free Algebra II worksheets for Texas TEKS 2A.7G and 2A.7H: simplify square, cube and fourth roots with variables, rational exponents and solving rational exponent equations. 100 questions with answers.',
         'x^(m/n) = ⁿ√(x^m).', 'Solve x^(m/n) = c by raising both sides to n/m.',
         body, faq, sets, seo_title='Algebra II Radicals and Rational Exponents Worksheets (TEKS 2A.7G, 2A.7H)')


if __name__ == "__main__":
    build()
