# -*- coding: utf-8 -*-
"""
Texas Precalculus: Piecewise and Step Functions (TEKS P.2F, P.2I)
  python3 tools/gen_ustx_math_pc_piecewise_step.py
Evaluating piecewise functions, the greatest integer function, step functions in context, continuity and jumps,
and writing piecewise rules from words (own makers).
Wrong answers come from real mistakes: using the wrong piece at a boundary, rounding −2.3 down to −2, and rounding a
part of an hour down instead of up.
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


def pw(p1, c, s1, p2, s2):
    return "<i>f</i>(<i>x</i>) = %s if <i>x</i> %s %s, and <i>f</i>(<i>x</i>) = %s if <i>x</i> %s %s" % (p1, s1, sg(c), p2, s2, sg(c))


def one_pw(r):
    a, b = r.choice([2, 3, -1, -2, 4]), r.randint(-6, 6)
    m, n = r.choice([1, 2, -1, 3]), r.randint(-9, 9)
    c = r.randint(-3, 4)
    strict = r.random() < 0.5
    s1, s2 = ("&lt;", "≥") if strict else ("≤", "&gt;")
    q2 = lambda x: m * x * x + n
    q1 = lambda x: a * x + b
    p2 = poly([m, 0, n])
    k = r.choice([c, c, c - 1, c + 1, c + 2, c - 2])
    left = (k < c) or (k == c and not strict)
    val = q1(k) if left else q2(k)
    oth = q2(k) if left else q1(k)
    if val == oth:
        raise AssertionError
    right = sg(val)
    w = [sg(oth), sg(val + 1), sg(q1(k) + q2(k))]
    return mcq("%s. Find <i>f</i>(%s)." % (pw(poly([a, b]), c, s1, p2, s2), sg(k)), right, w,
               "%s %s %s, so use the %s piece: <i>f</i>(%s) = %s." % (sg(k), "&lt;" if k < c else ("&gt;" if k > c else "="), sg(c), "first" if left else "second", sg(k), right) + " <b>%s</b>." % right)


def gi(v):
    import math
    return math.floor(v)


def one_floor(r):
    kind = r.choice(["floor", "floor", "neg", "expr", "ceil"])
    if kind in ("floor", "neg"):
        v = Fr(r.randint(1, 98), 10) * (1 if kind == "floor" else -1)
        if v.denominator == 1:
            raise AssertionError
        right = sg(gi(v))
        w = [sg(gi(v) + 1), sg(round(float(v))) if round(float(v)) not in (gi(v), gi(v) + 1) else sg(gi(v) - 1), ("%.1f" % float(v)).replace("-", MINUS)]
        q = "The greatest integer function ⌊<i>x</i>⌋ gives the greatest integer less than or equal to <i>x</i>. Find ⌊%s⌋." % ("%.1f" % float(v)).replace("-", MINUS)
        e = "The greatest integer ≤ %s is %s%s." % (("%.1f" % float(v)).replace("-", MINUS), right, " (go left on the number line, not toward 0)" if v < 0 else "")
    elif kind == "expr":
        a, b = r.choice([2, 3, -2, 5]), r.randint(-5, 5)
        v = Fr(r.randint(-60, 60), 10)
        if v.denominator == 1:
            raise AssertionError
        val = a * gi(v) + b
        right = sg(val)
        w = [sg(a * (gi(v) + 1) + b), sg(int(round(a * float(v) + b))) if int(round(a * float(v) + b)) != val else sg(val + a + 1), sg(gi(a * v) + b) if gi(a * v) + b != val else sg(val - 1)]
        q = "Let <i>f</i>(<i>x</i>) = %s⌊<i>x</i>⌋ %s %d. Find <i>f</i>(%s)." % (sg(a), "+" if b >= 0 else MINUS, abs(b), ("%.1f" % float(v)).replace("-", MINUS))
        e = "⌊%s⌋ = %s, so <i>f</i> = %s(%s) %s %d = %s." % (("%.1f" % float(v)).replace("-", MINUS), sg(gi(v)), sg(a), sg(gi(v)), "+" if b >= 0 else MINUS, abs(b), right)
    else:
        import math
        v = Fr(r.randint(-60, 60), 10)
        if v.denominator == 1:
            raise AssertionError
        right = sg(math.ceil(v))
        w = [sg(math.ceil(v) - 1), sg(math.ceil(v) + 1), ("%.1f" % float(v)).replace("-", MINUS)]
        q = "The ceiling function ⌈<i>x</i>⌉ gives the least integer greater than or equal to <i>x</i>. Find ⌈%s⌉." % ("%.1f" % float(v)).replace("-", MINUS)
        e = "The least integer ≥ %s is %s." % (("%.1f" % float(v)).replace("-", MINUS), right)
    return mcq(q, right, w, e + " <b>%s</b>." % right)


def money(v):
    c = int(round(v * 100))
    return "$%s.%02d" % (comma(c // 100), c % 100)


STEP = [("A parking garage charges $%(a)s for the first hour and $%(b)s for each additional hour or part of an hour.", "hour"),
        ("A shipping company charges $%(a)s for the first pound and $%(b)s for each additional pound or part of a pound.", "pound"),
        ("A phone call costs $%(a)s for the first minute and $%(b)s for each additional minute or part of a minute.", "minute"),
        ("A bike rental costs $%(a)s for the first hour and $%(b)s for each additional half hour or part of a half hour.", "half hour")]


def one_step(r):
    import math
    t, u = r.choice(STEP)
    a = r.choice([2, 3, 4, 5, 6, 8, 10]) if u != "minute" else r.choice([0.5, 0.75, 1])
    b = r.choice([1, 1.5, 2, 2.5, 3]) if u != "minute" else r.choice([0.1, 0.15, 0.2, 0.25])
    if u == "half hour":
        x = Fr(r.randint(11, 59), 10)
        extra_units = math.ceil((x - 1) * 2)
        unit_ = "hours"
    else:
        x = Fr(r.randint(11, 99), 10)
        extra_units = math.ceil(x - 1)
        unit_ = u + "s"
    if x.denominator == 1 or extra_units <= 0:
        raise AssertionError
    cost = a + b * extra_units
    down = a + b * (extra_units - 1)
    fa = ("%g" % a)
    fb = "%.2f" % b
    q = t % {"a": ("%.2f" % a) if a < 1 or a != int(a) else str(int(a)), "b": fb if b != int(b) else str(int(b))} + " What is the cost for %s %s?" % (("%.1f" % float(x)), unit_)
    right = money(cost)
    w = [money(down), money(a + b * float(x - 1)) if money(a + b * float(x - 1)) not in (right, money(down)) else money(cost + b), money(b * math.ceil(x * (2 if u == "half hour" else 1)))]
    return mcq(q, right, w, "After the first %s there are %d more %s (a part counts as a whole), so the cost is %s + %d × %s = <b>%s</b>." % (
        "hour" if u == "half hour" else u, extra_units, "half hours" if u == "half hour" else u + "s", money(a), extra_units, money(b), right))


def one_pwk(r):
    a = r.choice([1, 2, 3, -1, -2])
    m = r.choice([1, 2, 3, -1, 4])
    c = r.randint(-3, 4)
    n = r.randint(-8, 8)
    kind = r.choice(["k", "k", "jump", "cont"])
    if kind == "k":
        k = m * c + n - a * c
        q = "For what value of <i>k</i> is the function continuous? %s" % pw(poly([a, 0]) + " + <i>k</i>" if a else "<i>k</i>", c, "&lt;", poly([m, n]), "≥")
        right = sg(k)
        w = [sg(m * c + n), sg(-k), sg(k + a)]
        e = "The pieces must meet at <i>x</i> = %s: %s(%s) + <i>k</i> = %s(%s) %s %d, so <i>k</i> = %s." % (sg(c), sg(a), sg(c), sg(m), sg(c), "+" if n >= 0 else MINUS, abs(n), right)
    else:
        b = r.randint(-8, 8)
        L, Rv = a * c + b, m * c + n
        f = pw(poly([a, b]), c, "&lt;", poly([m, n]), "≥")
        if kind == "jump":
            if L == Rv:
                raise AssertionError
            q = "%s. How big is the jump in the graph at <i>x</i> = %s?" % (f, sg(c))
            right = str(abs(L - Rv))
            w = [str(abs(L + Rv)) if abs(L + Rv) != abs(L - Rv) else str(abs(L - Rv) + 2), str(abs(L - Rv) + 1), "There is no jump"]
            e = "Just left of %s the value approaches %s; at %s it is %s. The jump is |%s − (%s)| = %s." % (sg(c), sg(L), sg(c), sg(Rv), sg(L), sg(Rv), right) if Rv < 0 else "Just left of %s the value approaches %s; at %s it is %s. The jump is |%s − %s| = %s." % (sg(c), sg(L), sg(c), sg(Rv), sg(L), sg(Rv), right)
        else:
            q = "%s. Is <i>f</i> continuous at <i>x</i> = %s?" % (f, sg(c))
            right = "Yes, both pieces give %s there" % sg(L) if L == Rv else "No, the pieces give %s and %s" % (sg(L), sg(Rv))
            w = ["No, the pieces give %s and %s" % (sg(L), sg(L + 1)) if L == Rv else "Yes, both pieces give %s there" % sg(Rv), "Yes, every piecewise function is continuous", "No, a piecewise function is never continuous"]
            e = "Put <i>x</i> = %s into both pieces: %s and %s." % (sg(c), sg(L), sg(Rv))
    return mcq(q, right, w, e + " <b>%s</b>." % right)


def one_pwword(r):
    kind = r.choice(["pay", "pay", "elec", "ship"])
    if kind == "pay":
        p = r.choice([12, 14, 15, 16, 18, 20, 22])
        h = r.randint(41, 55)
        q = "Ana earns $%d an hour for the first 40 hours of a week and 1.5 times that rate for each hour over 40. How much does she earn for %d hours?" % (p, h)
        val = 40 * p + 1.5 * p * (h - 40)
        right = money(val)
        w = [money(1.5 * p * h), money(p * h), money(40 * p + 1.5 * p * h)]
        e = "40 × $%d = %s, plus %d × $%s = %s." % (p, money(40 * p), h - 40, ("%g" % (1.5 * p)), money(1.5 * p * (h - 40)))
    elif kind == "elec":
        a, b = r.choice([(0.10, 0.15), (0.12, 0.18), (0.08, 0.14), (0.11, 0.16)])
        lim = r.choice([500, 600, 800, 1000])
        k = r.randint(lim + 50, lim + 600)
        val = a * lim + b * (k - lim)
        q = "A power company charges $%.2f per kWh for the first %s kWh and $%.2f per kWh after that. What is the bill for %s kWh?" % (a, comma(lim), b, comma(k))
        right = money(val)
        w = [money(b * k), money(a * k), money(a * lim + b * k)]
        e = "%s × $%.2f = %s, plus %s × $%.2f = %s." % (comma(lim), a, money(a * lim), comma(k - lim), b, money(b * (k - lim)))
    else:
        a = r.choice([5, 6, 8])
        b = r.choice([0.5, 0.75, 1])
        free = r.choice([35, 50, 75])
        x = r.choice([v for v in range(10, 120, 5) if v != free])
        val = 0 if x >= free else a + b * (x // 5)
        q = "An online store charges $%d plus $%.2f for every $5 of the order for shipping, but shipping is free for orders of $%d or more. What is the shipping for a $%d order?" % (a, b, free, x)
        right = money(val) if val else "$0.00 (free)"
        w = [money(a + b * (x // 5)) if val == 0 else "$0.00 (free)", money(a + b * x), money(a)]
        w = [v for v in w if v != right]
        if len(w) < 3:
            w.append(money(b * (x // 5)))
        e = ("$%d ≥ $%d, so shipping is free." % (x, free)) if not val else "$%d &lt; $%d: $%d + %d × $%.2f = %s." % (x, free, a, x // 5, b, money(val))
    return mcq(q, right, w, e + " <b>%s</b>." % right)


def build():
    sets, R = build_sets([
        ("Evaluate piecewise functions", [("collect", uniq(one_pw), 20)]),
        ("The greatest integer function", [("collect", uniq(one_floor), 20)]),
        ("Step functions in context", [("collect", uniq(one_step), 20)]),
        ("Continuity and jumps", [("collect", uniq(one_pwk), 20)]),
        ("Piecewise rules from words", [("collect", uniq(one_pwword), 20)]),
    ], 69803)
    finish(sets, R)
    body = lesson('<ul><li>A <b>piecewise function</b> uses different rules on different parts of the domain. First decide which piece the input belongs to.</li><li>At a boundary, check the signs: &lt; and &gt; leave the point out, ≤ and ≥ include it.</li><li>The greatest integer function ⌊<i>x</i>⌋ rounds <b>down</b>: ⌊3.7⌋ = 3 and ⌊−2.3⌋ = −3. Its graph looks like steps.</li><li>A piecewise function is continuous at a boundary when both pieces give the same value there.</li></ul>',
        [example("<i>f</i>(<i>x</i>) = 2<i>x</i> + 1 if <i>x</i> &lt; 3, <i>x</i><sup>2</sup> if <i>x</i> ≥ 3; find <i>f</i>(3)", ["3 ≥ 3, so use <i>x</i><sup>2</sup>"], "<i>f</i>(3) = 9"), example("Parking: $4 the first hour, $2 each extra hour or part; 3.2 hours", ["2.2 extra hours → 3 parts"], "$4 + 3 × $2 = $10")],
        [['The wrong piece at the boundary', 'Look at ≤ and &lt; carefully.'], ['⌊−2.3⌋ = −2', 'Round down: −3.'], ['Rounding a part of an hour down', 'A part counts as a whole step.']])
    faq = [('What does TEKS P.2F ask?', 'Graph exponential, logarithmic, rational, polynomial, power, trigonometric, inverse trigonometric, and piecewise defined functions, including step functions.'), ('What does TEKS P.2I ask?', 'Determine and analyze the key features of functions, including piecewise defined functions and step functions, such as domain, range, symmetry, relative maximum, relative minimum, zeros, asymptotes, and intervals over which the function is increasing or decreasing.'), ('What does a step function graph look like?', 'Horizontal segments with a closed dot at one end and an open dot at the other.'), ('Is |x| a piecewise function?', 'Yes: −x if x < 0 and x if x ≥ 0.')]
    make('piecewise-and-step-functions', 3, 'Functions', 'P.2F, P.2I',
         'P.2F graph exponential, logarithmic, rational, polynomial, power, trigonometric, inverse trigonometric, and piecewise defined functions, including step functions; P.2I determine and analyze the key features of exponential, logarithmic, rational, polynomial, power, trigonometric, inverse trigonometric, and piecewise defined functions, including step functions such as domain, range, symmetry, relative maximum, relative minimum, zeros, asymptotes, and intervals over which the function is increasing or decreasing',
         'Piecewise and Step Functions', 'Piecewise and Step Functions',
         'Free Precalculus worksheets on piecewise and step functions for Texas TEKS P.2F and P.2I: evaluate piecewise functions, greatest integer function, step functions in context and continuity. 100 questions with answers.',
         'First decide which piece the input belongs to.', '⌊x⌋ rounds down: ⌊−2.3⌋ = −3.',
         body, faq, sets, seo_title='Precalculus Piecewise and Step Functions Worksheets (TEKS P.2F, P.2I)')


if __name__ == "__main__":
    build()
