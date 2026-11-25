# -*- coding: utf-8 -*-
"""
中国 高中の自前の問題の共通部品。数・式・区間・π・根号の書き方と、R の入れ替え。
負の数は初中と同じ「－」、和は「＋」、等号は「＝」。
"""
import math
import random
from fractions import Fraction as F
from ws_common import fr
from cn_common import mcq as _mcq, Names

R = random.Random(0)
NM = Names(R)
M = "－"
SUPT = str.maketrans("0123456789-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁻")


def setup(rnd):
    global R, NM
    R = rnd
    NM = Names(rnd)


def rr():
    return R


import re as _re


def tidy(t):
    """タグの外の文字だけ：-3 → －3、＋ －3 → － 3、－ －3 → ＋ 3、係数の 1x → x"""
    def fix(m):
        x = m.group(0)
        x = _re.sub(r"(?<![\w\)\].])-(?=\d)", "－", x)
        x = x.replace("＋ －", "－ ").replace("－ －", "＋ ")
        x = _re.sub(r"(?<![\d.])1(?=[xy]\b|[xy][²³⁴ ＋－)])", "", x)
        return x
    return _re.sub(r"[^<>]+(?=<|$)", fix, str(t))


def mcq(q, a, w, e):
    """誤答の重複・正解と同じものを落とす（数値として同じものも）"""
    q, a, e = tidy(q), tidy(a), tidy(e)
    w = [tidy(x) if x is not None else None for x in w]
    seen, out = {str(a)}, []
    for x in w:
        if x is None:
            continue
        x = str(x)
        if x in seen:
            continue
        seen.add(x)
        out.append(x)
    return _mcq(q, a, out, e)


def ch(kinds):
    return R.choice(kinds) if isinstance(kinds, (list, tuple)) else kinds


def S(x):
    """数（Fraction は分数の HTML、負は －）"""
    x = F(x)
    neg = x < 0
    a = -x if neg else x
    s = str(a.numerator) if a.denominator == 1 else fr(a.numerator, a.denominator)
    return (M + s) if neg else s


def P(x):
    """負の数はかっこ付き"""
    return "（%s）" % S(x) if F(x) < 0 else S(x)


def dec(x, p=2):
    s = ("%." + str(p) + "f") % x
    s = s.rstrip("0").rstrip(".") if "." in s else s
    return s.replace("-", M)


def sup(n):
    return str(n).translate(SUPT)


def poly(cs, v="x"):
    """係数リスト（次数の高い順）→ x³ － 2x ＋ 1"""
    n = len(cs) - 1
    out = []
    for i, c in enumerate(cs):
        c = F(c)
        d = n - i
        if c == 0:
            continue
        a = abs(c)
        if d == 0:
            body = S(a)
        else:
            coef = "" if a == 1 else S(a)
            body = coef + v + (sup(d) if d > 1 else "")
        if not out:
            out.append((M if c < 0 else "") + body)
        else:
            out.append((" － " if c < 0 else " ＋ ") + body)
    return "".join(out) or "0"


def lin(a, b, v="x"):
    return poly([a, b], v)


def term(c, rest=""):
    """係数 c と後ろの文字（c ＝ ±1 は 1 を省く）"""
    c = F(c)
    if rest and abs(c) == 1:
        return (M if c < 0 else "") + rest
    return S(c) + rest


def surd(n):
    """n ＝ k²·r（r は平方因数なし）"""
    k, r = 1, n
    d = 2
    while d * d <= r:
        while r % (d * d) == 0:
            r //= d * d
            k *= d
        d += 1
    return k, r


def rt(n, k=1):
    """k√n を簡単にして文字列に"""
    a, r = surd(n)
    k *= a
    if r == 1:
        return S(k)
    return ("" if k == 1 else (M if k == -1 else S(k))) + "√%d" % r


def pis(q):
    """q·π（q は Fraction）→ π/6、2π/3、－π/4"""
    q = F(q)
    if q == 0:
        return "0"
    neg = q < 0
    q = abs(q)
    n, d = q.numerator, q.denominator
    s = ("π" if n == 1 else "%dπ" % n) if d == 1 else fr("π" if n == 1 else "%dπ" % n, d)
    return (M + s) if neg else s


def iv(a, b, lc=False, rc=False):
    """区間。a ＝ None は －∞、b ＝ None は ＋∞"""
    L = ("[" if lc else "(") + ("－∞" if a is None else S(a))
    Rr = ("＋∞" if b is None else S(b)) + ("]" if rc else ")")
    return "%s, %s" % (L, Rr)


def C(n, k):
    return math.comb(n, k)


def A(n, k):
    return math.perm(n, k)


def setstr(xs):
    return "{%s}" % ", ".join(S(x) for x in xs)


def nz(lo, hi, ex=()):
    while True:
        v = R.randint(lo, hi)
        if v != 0 and v not in ex:
            return v


TRIPLES = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (6, 8, 10), (9, 12, 15), (20, 21, 29), (12, 16, 20)]
