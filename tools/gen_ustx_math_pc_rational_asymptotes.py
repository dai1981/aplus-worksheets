# -*- coding: utf-8 -*-
"""
Texas Precalculus: Asymptotes of Rational Functions (TEKS P.2K)
  python3 tools/gen_ustx_math_pc_rational_asymptotes.py
Horizontal and slant asymptotes, graphs and applications (US Precalculus makers with a new seed), and oblique
asymptotes by division and behavior near vertical asymptotes (own makers).
Wrong answers come from real mistakes: dropping the remainder step, using the ratio of leading coefficients for a slant
asymptote, and getting the sign wrong on one side of a vertical asymptote.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_pc_rational_functions_and_asymptotes as ra
adopt(ra)
ra.R = random.Random(698070)
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


def lin_(d):
    return X if d == 0 else "%s %s %d" % (X, MINUS if d > 0 else "+", abs(d))


def one_obl(r):
    a = r.choice([1, 2, 3, -1, -2])
    b, c = r.randint(-8, 8), r.randint(-9, 9)
    d = r.choice([n for n in range(-5, 6) if n])
    q1 = b + a * d
    rem = c + d * q1
    if rem == 0:
        raise AssertionError
    f = fx("<span class='fr'><span class='fn'>%s</span><span class='fd'>%s</span></span>" % (poly([a, b, c]), lin_(d)))
    right = "<i>y</i> = " + poly([a, q1])
    w = ["<i>y</i> = " + poly([a, b]), "<i>y</i> = " + poly([a, b - a * d]) if b - a * d != q1 else "<i>y</i> = " + poly([a, q1 + 1]), "<i>y</i> = %s" % sg(a)]
    return mcq("What is the slant (oblique) asymptote of %s?" % f, right, w,
               "Divide: (%s) ÷ (%s) = %s with remainder %s. The remainder part goes to 0 for large |<i>x</i>|, so the graph follows <b>%s</b>." % (poly([a, b, c]), lin_(d), poly([a, q1]), sg(rem), right))


def one_near(r):
    k = r.choice([n for n in range(-9, 10) if n])
    c = r.choice([n for n in range(-6, 7) if n])
    d = r.randint(-5, 5)
    sq = r.random() < 0.35
    side = r.choice([1, -1])
    den = ("(%s)<sup>2</sup>" % lin_(c)) if sq else lin_(c)
    f = fx(("" if k > 0 else MINUS) + "<span class='fr'><span class='fn'>%d</span><span class='fd'>%s</span></span>" % (abs(k), den) + ((" %s %d" % ("+" if d > 0 else MINUS, abs(d))) if d else ""))
    sgn = (1 if k > 0 else -1) * (1 if sq or side > 0 else -1)
    right = INF if sgn > 0 else MINUS + INF
    arrow = "%s<sup>%s</sup>" % (sg(c), "+" if side > 0 else "−")
    w = [MINUS + INF if sgn > 0 else INF, sg(d), "0"]
    return mcq("As <i>x</i> → %s (from the %s), what happens to %s?" % (arrow, "right" if side > 0 else "left", f), "<i>f</i>(<i>x</i>) → " + right, ["<i>f</i>(<i>x</i>) → " + v for v in w],
               "Near <i>x</i> = %s the bottom is a tiny %s number%s, so the fraction is huge and %s. <b><i>f</i>(<i>x</i>) → %s</b>." % (
                   sg(c), "positive" if sq or side > 0 else "negative", " (a square is never negative)" if sq else "", "positive" if sgn > 0 else "negative", right))


def build():
    sets, R = build_sets([
        ("Horizontal asymptotes and degrees", [("collect", W(ra.one_ha), 20)]),
        ("Slant asymptotes", [("collect", uniq(one_obl), 20)]),
        ("Behavior near a vertical asymptote", [("collect", uniq(one_near), 20)]),
        ("Match the graph", [("collect", W(ra.one_graph), 20)]),
        ("Rational functions in context", [("collect", W(ra.one_word), 20)]),
    ], 69807)
    finish(sets, R)
    body = lesson('<ul><li><b>Vertical asymptote</b>: a zero of the denominator that does not cancel.</li><li><b>Horizontal asymptote</b>: bottom degree bigger → <i>y</i> = 0; equal degrees → ratio of leading coefficients.</li><li><b>Slant (oblique) asymptote</b>: when the top degree is one more than the bottom, divide; the quotient (without the remainder) is the asymptote.</li><li>Near a vertical asymptote, check the sign of the fraction on each side: it goes to ∞ or −∞.</li></ul>',
        [example("<i>f</i>(<i>x</i>) = <span class='fr'><span class='fn'><i>x</i><sup>2</sup> + 3<i>x</i> + 1</span><span class='fd'><i>x</i> − 1</span></span>", ["Quotient <i>x</i> + 4, remainder 5"], "Slant asymptote <i>y</i> = <i>x</i> + 4")],
        [['Keeping the remainder', 'The asymptote is the quotient only.'], ['Using the ratio for a slant asymptote', 'That rule is only for equal degrees.'], ['The wrong sign on one side', 'Test a value just left and just right.']])
    faq = [('What does TEKS P.2K ask?', 'Analyze characteristics of rational functions and the behavior of the function around the asymptotes, including horizontal, vertical, and oblique asymptotes.'), ('Can a graph have both a horizontal and a slant asymptote?', 'No, a rational function has at most one of them.'), ('What does x → 3⁺ mean?', 'x gets close to 3 from values bigger than 3.'), ('Why does a squared factor matter?', 'The graph goes the same way on both sides.')]
    make('asymptotes-of-rational-functions', 7, 'Functions', 'P.2K',
         'P.2K analyze characteristics of rational functions and the behavior of the function around the asymptotes, including horizontal, vertical, and oblique asymptotes',
         'Asymptotes of Rational Functions', 'Rational Asymptotes',
         'Free Precalculus worksheets on rational function asymptotes for Texas TEKS P.2K: horizontal, vertical and slant asymptotes, behavior near asymptotes and graphs. 100 questions with answers.',
         'Slant asymptote: divide and keep the quotient.', 'Check the sign of the fraction on each side of a vertical asymptote.',
         body, faq, sets, seo_title='Precalculus Asymptotes of Rational Functions Worksheets (TEKS P.2K)')


if __name__ == "__main__":
    build()
