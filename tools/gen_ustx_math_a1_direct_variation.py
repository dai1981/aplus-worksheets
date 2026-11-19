# -*- coding: utf-8 -*-
"""
Texas Algebra I: Direct Variation: y = kx (TEKS A.2D)
  python3 tools/gen_ustx_math_a1_direct_variation.py
Finding the constant of variation, writing y = kx, deciding if a relation is a direct variation, finding a missing
value, and direct variation word problems (own makers).
Wrong answers come from real mistakes: dividing x by y, adding instead of multiplying, and calling y = kx + b a direct
variation.
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
KS = [Fr(2), Fr(3), Fr(4), Fr(5), Fr(6), Fr(7), Fr(8), Fr(9), Fr(12), Fr(1, 2), Fr(1, 3), Fr(3, 2), Fr(2, 3), Fr(5, 2), Fr(3, 4), Fr(-2), Fr(-3), Fr(-4), Fr(-1, 2)]


def ks(k):
    if k.denominator == 1:
        return sg(k.numerator)
    return (MINUS if k < 0 else "") + fr(abs(k.numerator), k.denominator)


def kx(k):
    if k == 1:
        return X
    if k == -1:
        return MINUS + X
    return ks(k) + X


def pair(r, k):
    x = r.choice([n for n in range(-9, 13) if n]) * k.denominator
    if abs(x) > 24:
        raise AssertionError
    return x, k * x


def one_k(r):
    k = r.choice(KS)
    x, y = pair(r, k)
    w = [ks(1 / k), sg(int(y - x)) if (y - x).denominator == 1 else None, sg(int(x * y)) if (x * y).denominator == 1 else None, ks(-k)]
    w = [c for c in w if c and c != ks(k)]
    return mcq("<i>y</i> varies directly with <i>x</i>. When <i>x</i> = %s, <i>y</i> = %s. What is the constant of variation <i>k</i>?" % (sg(x), sg(int(y))), ks(k), w,
               "<i>k</i> = <i>y</i> ÷ <i>x</i> = %s ÷ %s = <b>%s</b>." % (sg(int(y)), sg(x), ks(k)))


def one_write(r):
    k = r.choice(KS)
    x, y = pair(r, k)
    right = "<i>y</i> = %s" % kx(k)
    w = ["<i>y</i> = %s" % kx(1 / k), "<i>y</i> = %s + %s" % (X, sg(int(y - x))) if (y - x) > 0 else "<i>y</i> = %s − %s" % (X, abs(int(y - x))), "<i>y</i> = %s + %s" % (kx(k), abs(x)), "<i>y</i> = %s" % kx(-k)]
    w = [c for c in w if c != right]
    return mcq("<i>y</i> varies directly with <i>x</i>, and <i>y</i> = %s when <i>x</i> = %s. Write the direct variation equation." % (sg(int(y)), sg(x)), right, w,
               "<i>k</i> = %s ÷ %s = %s, so <b>%s</b>." % (sg(int(y)), sg(x), ks(k), right))


def one_is(r):
    k = r.choice([n for n in range(-6, 10) if n not in (0, 1)])
    b = r.choice([n for n in range(-9, 10) if n])
    kind = r.choice(["dv", "dv", "lin", "add", "table", "tableno"])
    if kind in ("table", "tableno"):
        xs = sorted(r.sample(range(1, 9), 3))
        ys = [k * v for v in xs] if kind == "table" else [k * v + b for v in xs]
        t = "<table class='sn-table'><tr><th><i>x</i></th>%s</tr><tr><th><i>y</i></th>%s</tr></table>" % ("".join("<td>%d</td>" % v for v in xs), "".join("<td>%s</td>" % sg(v) for v in ys))
        q = t + "Does this table show a direct variation?"
    else:
        eq = {"dv": "<i>y</i> = %s" % kx(Fr(k)), "lin": "<i>y</i> = %s %s %d" % (kx(Fr(k)), "+" if b > 0 else MINUS, abs(b)), "add": "<i>y</i> = %s %s %d" % (X, "+" if b > 0 else MINUS, abs(b))}[kind]
        q = "Does %s show a direct variation?" % eq
    yes = kind in ("dv", "table")
    ch = ["Yes, <i>k</i> = %s" % sg(k), "No, the graph does not pass through (0, 0)", "No, <i>y</i> ÷ <i>x</i> is not the same for every point", "Yes, <i>k</i> = %s" % sg(b if kind not in ("dv", "table") else k + 1)]
    if yes:
        right, w = ch[0], [ch[1], ch[2], "Yes, <i>k</i> = %s" % sg(-k)]
        e = "<i>y</i> ÷ <i>x</i> = %s every time, so it is a direct variation with <b><i>k</i> = %s</b>." % (sg(k), sg(k))
    else:
        right = ch[2] if kind == "tableno" else ch[1]
        w = [c for c in ch if c != right][:3]
        e = "A direct variation has the form <i>y</i> = <i>kx</i>: its graph passes through (0, 0) and <i>y</i> ÷ <i>x</i> is constant. This one does not, so <b>no</b>."
    return mcq(q, right, w, e)


def one_find(r):
    k = r.choice(KS)
    x1, y1 = pair(r, k)
    x2, y2 = pair(r, k)
    if x1 == x2 or y2.denominator != 1:
        raise AssertionError
    w = [sg(int(y1 + (x2 - x1))) if (y1 + x2 - x1).denominator == 1 else None, sg(int(y2 + k)) if (y2 + k).denominator == 1 else None, sg(int(-y2)), sg(int(x2 / k)) if (x2 / k).denominator == 1 else None]
    w = [c for c in w if c and c != sg(int(y2))]
    return mcq("<i>y</i> varies directly with <i>x</i>. If <i>y</i> = %s when <i>x</i> = %s, find <i>y</i> when <i>x</i> = %s." % (sg(int(y1)), sg(x1), sg(x2)), sg(int(y2)), w,
               "<i>k</i> = %s ÷ %s = %s. <i>y</i> = %s × %s = <b>%s</b>." % (sg(int(y1)), sg(x1), ks(k), ks(k), sg(x2), sg(int(y2))))


CTX = [("Maria's pay varies directly with the hours she works. She earns ${y1} for {x1} hours. How much does she earn for {x2} hours?", "$", ""),
       ("The distance a car travels at a steady speed varies directly with time. It goes {y1} miles in {x1} hours. How far does it go in {x2} hours?", "", " miles"),
       ("The cost of pecans varies directly with their weight. {x1} pounds cost ${y1}. How much do {x2} pounds cost?", "$", ""),
       ("The water used by a sprinkler varies directly with time. It uses {y1} gallons in {x1} minutes. How much does it use in {x2} minutes?", "", " gallons"),
       ("The number of calories varies directly with the number of servings. {x1} servings have {y1} calories. How many calories are in {x2} servings?", "", " calories"),
       ("The weight of a stack of books varies directly with the number of books. {x1} books weigh {y1} pounds. How much do {x2} books weigh?", "", " pounds"),
       ("A printer's pages vary directly with time. It prints {y1} pages in {x1} minutes. How many pages does it print in {x2} minutes?", "", " pages")]


def one_word(r):
    t, pre, post = r.choice(CTX)
    k = r.choice([3, 4, 5, 6, 8, 9, 12, 15, 18, 20, 24, 45, 55, 60, 65])
    x1 = r.randint(2, 8)
    x2 = r.choice([n for n in range(3, 16) if n != x1])
    y1, y2 = k * x1, k * x2
    f = lambda v: "%s%s%s" % (pre, comma(v), post)
    w = [f(y1 + x2 - x1), f(y1 * x2), f(y2 + k), f(y2 - k)]
    w = [c for c in w if c != f(y2)]
    return mcq(t.format(x1=x1, y1=y1, x2=x2), f(y2), w, "<i>k</i> = %d ÷ %d = %d per unit. %d × %d = <b>%s</b>." % (y1, x1, k, k, x2, f(y2)))


def build():
    sets, R = build_sets([
        ("Find the constant of variation", [("collect", uniq(one_k), 20)]),
        ("Write the equation y = kx", [("collect", uniq(one_write), 20)]),
        ("Is it a direct variation?", [("collect", uniq(one_is), 20)]),
        ("Find a missing value", [("collect", uniq(one_find), 20)]),
        ("Direct variation word problems", [("collect", uniq(one_word), 20)]),
    ], 69507)
    finish(sets, R)
    body = lesson('<ul><li><i>y</i> <b>varies directly</b> with <i>x</i> when <i>y</i> = <i>kx</i> for a constant <i>k</i> ≠ 0.</li><li>Find <i>k</i> = <i>y</i> ÷ <i>x</i> from any point.</li><li>The graph is a line through the origin (0, 0).</li><li><i>y</i> = <i>kx</i> + <i>b</i> with <i>b</i> ≠ 0 is linear but <b>not</b> a direct variation.</li></ul>',
        [example("<i>y</i> = 18 when <i>x</i> = 6", ["<i>k</i> = 18 ÷ 6 = 3"], "<i>y</i> = 3<i>x</i>")],
        [['Dividing <i>x</i> by <i>y</i>', '<i>k</i> = <i>y</i> ÷ <i>x</i>.'], ['Adding instead of multiplying', 'Direct variation multiplies by <i>k</i>.'], ['Calling <i>y</i> = <i>kx</i> + <i>b</i> a direct variation', 'It must pass through (0, 0).']])
    faq = [('What does TEKS A.2D ask?', 'Write and solve equations involving direct variation.'), ('What is the constant of variation?', 'The number k in y = kx.'), ('Can k be negative?', 'Yes. Then y decreases as x increases.'), ('Is every proportional relationship a direct variation?', 'Yes. Both are y = kx.')]
    make('direct-variation', 7, 'Linear Functions, Equations, and Inequalities', 'A.2D',
         'A.2D write and solve equations involving direct variation',
         'Direct Variation: y = kx', 'Direct Variation',
         'Free Algebra I direct variation worksheets for Texas TEKS A.2D: find k, write y = kx, decide if a table or equation is a direct variation, find missing values and word problems. 100 questions with answers.',
         'Direct variation: y = kx, with k = y ÷ x.', 'The graph passes through (0, 0).',
         body, faq, sets, seo_title='Algebra I Direct Variation Worksheets (TEKS A.2D)')


if __name__ == "__main__":
    build()
