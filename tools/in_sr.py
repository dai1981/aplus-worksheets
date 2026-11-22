# -*- coding: utf-8 -*-
"""
Shared helpers for India Class 11-12 (CBSE Senior Secondary / NCERT) generators, on top of in_common.
U() writes one chapter with in_common.unit (level 11 or 12, no Ganita Prakash part, CBSE Senior Secondary syllabus URL).
"""
import random, math, re
from fractions import Fraction as F
from in_common import num, fv, T, QN, expr, MINUS, fr, People, adopt, gb, comma, unit as _unit

X, Y, Z = "<i>x</i>", "<i>y</i>", "<i>z</i>"
I_, J_, K_ = "<i>î</i>", "<i>ĵ</i>", "<i>k̂</i>"
_SUP = str.maketrans("0123456789-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁻")


def sup(n):
    return str(n).translate(_SUP)


def xp(n, v=X):
    if n == 0:
        return ""
    return v if n == 1 else v + sup(n)


def poly(cs, v=X):
    """coefficients from the highest power down: [3, 0, -2] -> 3x² − 2"""
    d = len(cs) - 1
    return expr([(c, xp(d - i, v)) for i, c in enumerate(cs)])


def sn(n):
    """signed number with the real minus sign"""
    return num(n)


def fx(v):
    """exact value as html (whole number or fraction, minus sign in front)"""
    return fv(v)


def nz(lo, hi):
    return [k for k in range(lo, hi + 1) if k]


def pi(q):
    """multiple of π: 1/3 -> π/3, 2/3 -> 2π/3, -1/4 -> −π/4"""
    q = F(q)
    if q == 0:
        return "0"
    s = MINUS if q < 0 else ""
    q = abs(q)
    top = "π" if q.numerator == 1 else "%dπ" % q.numerator
    return s + (top if q.denominator == 1 else "%s/%d" % (top, q.denominator))


def surd(n):
    """n = a² b with b square-free: returns (a, b)"""
    a, b = 1, n
    k = 2
    while k * k <= b:
        while b % (k * k) == 0:
            b //= k * k
            a *= k
        k += 1
    return a, b


def rt(n, coef=1):
    """coef·√n simplified, as text: 2√3, √5, 6"""
    a, b = surd(n)
    a *= coef
    if b == 1:
        return num(a)
    return ("" if a == 1 else (MINUS if a == -1 else num(a))) + "√" + str(b)


def T2(q, right, wrongs, e):
    """T with the wrong answers cleaned: no repeats, none equal to the right answer"""
    ws = []
    for w in wrongs:
        if w is None or w == right or w in ws:
            continue
        ws.append(w)
    return T(q, right, ws, e)


def frs(v):
    """fraction as inline text a/b (for use inside expressions)"""
    v = F(v)
    s = MINUS if v < 0 else ""
    v = abs(v)
    return s + (str(v.numerator) if v.denominator == 1 else "%d/%d" % (v.numerator, v.denominator))


_PM = [(re.compile(r"− −(?=[\d(<a-zA-Z])"), "+ "), (re.compile(r"\+ −(?=[\d(<a-zA-Z])"), "− ")]


def tidy(fn):
    """'x − −2' -> 'x + 2' and 'a + −3' -> 'a − 3' outside pictures"""
    def f(r):
        it = fn(r)
        if not it:
            return it
        def t(s):
            parts = re.split(r"(<svg.*?</svg>)", s, flags=re.S)
            for i, p in enumerate(parts):
                if not p.startswith("<svg"):
                    for a, b in _PM:
                        p = a.sub(b, p)
                    parts[i] = p
            return "".join(parts)
        it["q"], it["e"] = t(it["q"]), t(it["e"])
        it["c"] = [t(c) for c in it["c"]]
        return it
    f.__name__ = getattr(fn, "__name__", "maker")
    return f


def U(level, chapter, slug, sort, strand, title, short_title, std_text, meta, key_big, key_sub,
      think, examples, mistakes, faq, spec, seed):
    spec = [(t, [(tidy(f), n) for f, n in parts]) for t, parts in spec]
    _unit(level, None, chapter, slug, sort, strand, title, short_title, std_text, meta, key_big, key_sub,
          think, examples, mistakes, faq, spec, random.Random(seed))


def fix(fn, pairs):
    """wrap a reused maker: plain text replacements in the question, choices and explanation"""
    def f(r):
        it = fn(r)
        if not it:
            return None
        for a, b in pairs:
            sub = (lambda t: a.sub(b, t)) if hasattr(a, "sub") else (lambda t: t.replace(a, b))
            it["q"], it["e"] = sub(it["q"]), sub(it["e"])
            it["c"] = [sub(c) for c in it["c"]]
        return it
    f.__name__ = getattr(fn, "__name__", "maker")
    return f


def use(mod, name, rnd, pairs=()):
    """a reused maker from another country's generator: Indian names and money, British spelling, extra replacements"""
    adopt(mod, rnd)
    return fix(gb(getattr(mod, name)), list(pairs))


NCR = (re.compile(r"<sub>(\d+|<i>n</i>)</sub>C<sub>"), r"<sup>\1</sup>C<sub>")


def C(n, k):
    """NCERT notation ⁿCᵣ"""
    return "<sup>%s</sup>C<sub>%s</sub>" % (n, k)


def P(n, k):
    return "<sup>%s</sup>P<sub>%s</sub>" % (n, k)
