# -*- coding: utf-8 -*-
"""
Texas Algebra II: Parent Functions and Their Key Attributes (TEKS 2A.2A)
  python3 tools/gen_ustx_math_a2_parent_functions.py
Domain, range, intercepts, asymptotes, symmetry, increasing and decreasing, and maximum and minimum on an interval
for the Algebra II parent functions x², √x, 1/x, x³, ∛x, |x|, 2^x, 10^x, e^x, log₂ x, log x and ln x (own makers).
Wrong answers come from real mistakes: giving √x a domain of all real numbers, mixing up the asymptotes of 2^x and
log₂ x, and taking the maximum at the left end of an interval.
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


RECIP = "<span class='fr'><span class='fn'>1</span><span class='fd'><i>x</i></span></span>"
# key, html, domain, range, asymptotes, intercepts, symmetry, increasing/decreasing, function
PAR = [
    ("sq", X + "<sup>2</sup>", "all", "ge", "none", "o", "y", "vu", lambda x: x * x),
    ("sqrt", "√" + X, "ge", "ge", "none", "o", "no", "inc", None),
    ("recip", RECIP, "ne", "ne", "both", "none", "or", "dec", lambda x: 1 / Fr(x)),
    ("cube", X + "<sup>3</sup>", "all", "all", "none", "o", "or", "inc", lambda x: x ** 3),
    ("cbrt", "∛" + X, "all", "all", "none", "o", "or", "inc", None),
    ("abs", "|" + X + "|", "all", "ge", "none", "o", "y", "vu", lambda x: abs(x)),
    ("exp2", "2<sup><i>x</i></sup>", "all", "gt", "h", "y1", "no", "inc", lambda x: Fr(2) ** x),
    ("exp10", "10<sup><i>x</i></sup>", "all", "gt", "h", "y1", "no", "inc", None),
    ("expe", "<i>e</i><sup><i>x</i></sup>", "all", "gt", "h", "y1", "no", "inc", None),
    ("log2", "log<sub>2</sub> " + X, "gt", "all", "v", "x1", "no", "inc", None),
    ("log10", "log " + X, "gt", "all", "v", "x1", "no", "inc", None),
    ("ln", "ln " + X, "gt", "all", "v", "x1", "no", "inc", None),
]
DOM = {"all": "All real numbers", "ge": "<i>x</i> ≥ 0", "gt": "<i>x</i> &gt; 0", "ne": "<i>x</i> ≠ 0"}
RNG = {"all": "All real numbers", "ge": "<i>y</i> ≥ 0", "gt": "<i>y</i> &gt; 0", "ne": "<i>y</i> ≠ 0"}
DWHY = {"all": "You can put any real number into %s.", "ge": "You cannot take the square root of a negative number, so %s needs <i>x</i> ≥ 0.",
        "gt": "You can only take the logarithm of a positive number, so %s needs <i>x</i> &gt; 0.", "ne": "You cannot divide by 0, so %s needs <i>x</i> ≠ 0."}
RWHY = {"all": "The graph of %s keeps going down and up forever, so every <i>y</i>-value is an output.", "ge": "The outputs of %s are never negative, and 0 is an output.",
        "gt": "A positive base to any power is positive, so the outputs of %s are always above 0 but never reach 0.", "ne": "%s can be any number except 0: a fraction with 1 on top is never 0."}
ASY = {"none": "No asymptotes", "v": "Vertical asymptote <i>x</i> = 0 only", "h": "Horizontal asymptote <i>y</i> = 0 only", "both": "Asymptotes <i>x</i> = 0 and <i>y</i> = 0"}
AWHY = {"none": "The graph of %s is a smooth curve through (0, 0) that keeps growing: no line it gets closer and closer to.",
        "v": "The graph of %s drops down along the <i>y</i>-axis as <i>x</i> gets close to 0: vertical asymptote <i>x</i> = 0.",
        "h": "As <i>x</i> goes far to the left, %s gets closer and closer to 0: horizontal asymptote <i>y</i> = 0.",
        "both": "%s is undefined at <i>x</i> = 0 and gets close to 0 for large |<i>x</i>|: asymptotes <i>x</i> = 0 and <i>y</i> = 0."}
ICP = {"o": "(0, 0) only", "y1": "(0, 1) only", "x1": "(1, 0) only", "none": "No intercepts"}
IWHY = {"o": "%s is 0 when <i>x</i> = 0, so the graph passes through the origin.", "y1": "Any base to the power 0 is 1, so %s crosses the <i>y</i>-axis at (0, 1).",
        "x1": "The log of 1 is 0, so %s crosses the <i>x</i>-axis at (1, 0). It never reaches the <i>y</i>-axis.", "none": "%s is never 0 and is not defined at <i>x</i> = 0, so it has no intercepts."}
SYM = {"y": "Symmetric about the <i>y</i>-axis (even)", "or": "Symmetric about the origin (odd)", "no": "Neither", "xa": "Symmetric about the <i>x</i>-axis"}
SWHY = {"y": "<i>f</i>(−<i>x</i>) = <i>f</i>(<i>x</i>) for %s: the left side is a mirror image of the right side.",
        "or": "<i>f</i>(−<i>x</i>) = −<i>f</i>(<i>x</i>) for %s: turning the graph halfway around the origin gives the same graph.",
        "no": "The graph of %s has no mirror line and no point symmetry."}
MON = {"inc": "Increasing over its whole domain", "vu": "Decreasing for <i>x</i> &lt; 0, increasing for <i>x</i> &gt; 0", "dec": "Decreasing on each part of its domain",
       "uv": "Increasing for <i>x</i> &lt; 0, decreasing for <i>x</i> &gt; 0"}
MWHY = {"inc": "As <i>x</i> gets bigger, %s always gets bigger.", "vu": "%s falls to 0 at <i>x</i> = 0 and then rises.", "dec": "%s falls on the left of 0 and falls again on the right of 0."}


def name(p):
    return fx(p[1])


def one_dr(r):
    p = r.choice(PAR)
    if r.random() < 0.5:
        right = DOM[p[2]]
        return mcq("What is the domain of %s?" % name(p), right, [v for k, v in DOM.items() if k != p[2]], DWHY[p[2]] % p[1] + " <b>%s</b>." % right)
    right = RNG[p[3]]
    return mcq("What is the range of %s?" % name(p), right, [v for k, v in RNG.items() if k != p[3]], RWHY[p[3]] % p[1] + " <b>%s</b>." % right)


def one_ai(r):
    p = r.choice(PAR)
    if r.random() < 0.5:
        right = ASY[p[4]]
        return mcq("Which describes the asymptotes of the graph of %s?" % name(p), right, [v for k, v in ASY.items() if k != p[4]], AWHY[p[4]] % p[1] + " <b>%s</b>." % right)
    right = ICP[p[5]]
    return mcq("Which intercepts does the graph of %s have?" % name(p), right, [v for k, v in ICP.items() if k != p[5]], IWHY[p[5]] % p[1] + " <b>%s</b>." % right)


def one_sm(r):
    p = r.choice(PAR)
    if r.random() < 0.5:
        right = SYM[p[6]]
        return mcq("Which describes the symmetry of the graph of %s?" % name(p), right, [v for k, v in SYM.items() if k != p[6]], SWHY[p[6]] % p[1] + " <b>%s</b>." % right)
    right = MON[p[7]]
    return mcq("Where is %s increasing or decreasing?" % name(p), right, [v for k, v in MON.items() if k != p[7]], MWHY[p[7]] % p[1] + " <b>%s</b>." % right)


def one_mm(r):
    kind = r.choice(["sq", "abs", "cube", "sqrt", "cbrt", "exp2", "log2", "recip"])
    if kind in ("sq", "abs"):
        a = r.randint(-6, 3)
        b = r.randint(a + 2, 6)
        f = (lambda x: x * x) if kind == "sq" else abs
    elif kind == "cube":
        a = r.randint(-4, 2)
        b = r.randint(a + 1, 4)
        f = lambda x: x ** 3
    elif kind == "sqrt":
        a, b = sorted(r.sample([0, 1, 4, 9, 16, 25, 36, 49, 64, 81, 100], 2))
        f = lambda x: Fr(int(round(x ** 0.5)))
    elif kind == "cbrt":
        a, b = sorted(r.sample([-64, -27, -8, -1, 0, 1, 8, 27, 64, 125], 2))
        f = lambda x: Fr(int(round(abs(x) ** (1 / 3)))) * (1 if x >= 0 else -1)
    elif kind == "exp2":
        a = r.randint(-3, 3)
        b = r.randint(a + 1, 7)
        f = lambda x: Fr(2) ** x
    elif kind == "log2":
        a, b = sorted(r.sample([1, 2, 4, 8, 16, 32, 64, 128], 2))
        f = lambda x: Fr(x.bit_length() - 1)
    else:
        a, b = sorted(r.sample([1, 2, 3, 4, 5, 6, 8, 10], 2))
        f = lambda x: 1 / Fr(x)
    p = [q for q in PAR if q[0] == kind][0]
    fa, fb = Fr(f(a)), Fr(f(b))
    if kind in ("sq", "abs") and a < 0 < b:
        mn, mx = Fr(0), max(fa, fb)
    else:
        mn, mx = min(fa, fb), max(fa, fb)
    want = r.choice(["maximum", "minimum"])
    right = mx if want == "maximum" else mn
    other = mn if want == "maximum" else mx
    cands = [other, fa, fb, Fr(b), Fr(a), right + 1, right - 1, right * 2]
    w = [ft(c) for c in cands if c != right]
    if kind in ("sq", "abs") and a < 0 < b:
        e = "%s is smallest at <i>x</i> = 0 (value 0) and largest at the end farthest from 0: <i>f</i>(%s) = %s and <i>f</i>(%s) = %s." % (p[1], sg(a), ft(fa), sg(b), ft(fb))
    elif kind == "recip":
        e = "%s is decreasing for <i>x</i> &gt; 0: the left end gives the maximum %s and the right end the minimum %s." % (p[1], ft(fa), ft(fb))
    else:
        e = "%s on this interval: check both ends. <i>f</i>(%s) = %s and <i>f</i>(%s) = %s." % ("The function is increasing" if kind != "sq" and kind != "abs" else "There is no turning point inside", sg(a), ft(fa), sg(b), ft(fb))
    return mcq("What is the %s value of %s on the interval %s ≤ <i>x</i> ≤ %s?" % (want, name(p), sg(a), sg(b)), ft(right), w, e + " The %s is <b>%s</b>." % (want, ft(right)))


DESC = [(2, lambda v: "domain " + DOM[v].replace("All real numbers", "all real numbers")), (3, lambda v: "range " + RNG[v].replace("All real numbers", "all real numbers")),
        (4, lambda v: {"none": "no asymptotes", "v": "only a vertical asymptote", "h": "only a horizontal asymptote", "both": "a vertical and a horizontal asymptote"}[v]),
        (5, lambda v: {"o": "an intercept at (0, 0)", "y1": "a <i>y</i>-intercept of (0, 1)", "x1": "an <i>x</i>-intercept of (1, 0)", "none": "no intercepts"}[v]),
        (6, lambda v: {"y": "symmetry about the <i>y</i>-axis", "or": "symmetry about the origin", "no": "no symmetry"}[v]),
        (7, lambda v: {"inc": "increases over its whole domain", "vu": "decreases and then increases", "dec": "decreases on each part of its domain"}[v])]


def one_match(r):
    p = r.choice(PAR)
    a1, a2 = sorted(r.sample(DESC, 2), key=lambda d: d[0])
    def ph(d):
        t = d[1](p[d[0]])
        return t if d[0] == 7 else "has " + t
    q = "Which parent function %s and %s?" % (ph(a1), ph(a2))
    others = [o for o in PAR if o[a1[0]] != p[a1[0]] or o[a2[0]] != p[a2[0]]]
    if len(others) < 3 or len(others) == len(PAR) - 1 and False:
        raise AssertionError
    r.shuffle(others)
    fam = {"exp2": "e", "exp10": "e", "expe": "e", "log2": "l", "log10": "l", "ln": "l"}
    w, used = [], set()
    for o in others:
        f = fam.get(o[0], o[0])
        if f in used:
            continue
        used.add(f)
        w.append(name(o))
    same = [o for o in PAR if o[a1[0]] == p[a1[0]] and o[a2[0]] == p[a2[0]] and fam.get(o[0], o[0]) != fam.get(p[0], p[0])]
    if same:
        raise AssertionError("not unique")
    return mcq(q, name(p), w, "%s has domain %s, range %s, %s, intercepts %s and %s. <b>%s</b>." % (
        name(p), DOM[p[2]].replace("All", "all"), RNG[p[3]].replace("All", "all"), ASY[p[4]][0].lower() + ASY[p[4]][1:], ICP[p[5]], {"y": "symmetry about the <i>y</i>-axis", "or": "symmetry about the origin", "no": "no symmetry"}[p[6]], name(p)))


def build():
    sets, R = build_sets([
        ("Domain and range", [("collect", uniq(one_dr), 20)]),
        ("Intercepts and asymptotes", [("collect", uniq(one_ai), 20)]),
        ("Symmetry, increasing and decreasing", [("collect", uniq(one_sm), 20)]),
        ("Maximum and minimum on an interval", [("collect", uniq(one_mm), 20)]),
        ("Which parent function is it?", [("collect", uniq(one_match), 20)]),
    ], 69701)
    finish(sets, R)
    body = lesson("<ul><li>A <b>parent function</b> is the simplest function of a family: <i>x</i><sup>2</sup>, √<i>x</i>, <span class='fr'><span class='fn'>1</span><span class='fd'><i>x</i></span></span>, <i>x</i><sup>3</sup>, ∛<i>x</i>, |<i>x</i>|, <i>b</i><sup><i>x</i></sup> and log<sub><i>b</i></sub> <i>x</i>.</li><li>Domain: √<i>x</i> needs <i>x</i> ≥ 0, logs need <i>x</i> &gt; 0, <span class='fr'><span class='fn'>1</span><span class='fd'><i>x</i></span></span> needs <i>x</i> ≠ 0.</li><li><i>b</i><sup><i>x</i></sup> has the horizontal asymptote <i>y</i> = 0; log<sub><i>b</i></sub> <i>x</i> has the vertical asymptote <i>x</i> = 0.</li><li>On an interval, check both ends, and the turning point if it is inside.</li></ul>",
        [example("Maximum of <i>f</i>(<i>x</i>) = <i>x</i><sup>2</sup> on −4 ≤ <i>x</i> ≤ 3", ["<i>f</i>(−4) = 16, <i>f</i>(3) = 9", "The minimum is 0 at <i>x</i> = 0"], "Maximum 16"), example("Asymptote of <i>f</i>(<i>x</i>) = 2<sup><i>x</i></sup>", ["2<sup><i>x</i></sup> gets close to 0 on the left"], "<i>y</i> = 0")],
        [['All real numbers for √<i>x</i>', '√<i>x</i> needs <i>x</i> ≥ 0.'], ['Mixing up the asymptotes of 2<sup><i>x</i></sup> and log<sub>2</sub> <i>x</i>', 'Exponential: <i>y</i> = 0. Log: <i>x</i> = 0.'], ['Checking only one end of the interval', 'For <i>x</i><sup>2</sup> on −4 ≤ <i>x</i> ≤ 3, the bigger value is at −4.']])
    faq = [('What does TEKS 2A.2A ask?', 'Graph the parent functions and, when applicable, analyze key attributes such as domain, range, intercepts, symmetries, asymptotic behavior, and maximum and minimum given an interval.'), ('Which bases are used for exponential and log functions?', '2, 10 and e.'), ('Which parent functions are odd?', 'x³, ∛x and 1/x are symmetric about the origin.'), ('Do x³ and ∛x have asymptotes?', 'No. Their domain and range are all real numbers.')]
    make('parent-functions', 1, 'Attributes of Functions and Their Inverses', '2A.2A',
         '2A.2A graph the functions f(x) = √x, f(x) = 1/x, f(x) = x^3, f(x) = ∛x, f(x) = b^x, f(x) = |x|, and f(x) = log_b(x) where b is 2, 10, and e, and, when applicable, analyze the key attributes such as domain, range, intercepts, symmetries, asymptotic behavior, and maximum and minimum given an interval',
         'Parent Functions and Their Key Attributes', 'Parent Functions',
         'Free Algebra II parent functions worksheets for Texas TEKS 2A.2A: domain, range, intercepts, asymptotes, symmetry and maximum and minimum on an interval. 100 questions with answers.',
         "Know each parent function's domain, range, intercepts and asymptotes.", '2^x has the asymptote y = 0; log₂ x has the asymptote x = 0.',
         body, faq, sets, seo_title='Algebra II Parent Functions Worksheets (TEKS 2A.2A)')


if __name__ == "__main__":
    build()
