# -*- coding: utf-8 -*-
"""
대한민국 고등학교 수학（2022 개정：공통수학1・2、대수、미적분Ⅰ、확률과 통계）の共通部品。
kr_mid（M・N・neg・par・figure・kosy・kurve、tidy の拡張）の上に：
  px(cs)        係数のリスト（次数の高い順）→ 2x³ − x + 5
  pmul・padd・peval・pdiv（多項式の割り算：商と나머지）
  cx(a, b)      복소수 a + bi
  sq_split・surd（√ の簡約：c√n）
  mx(rows)      행렬（ws.css の .mx）
  roots(a, b)   「x = −2 또는 x = 3」
  W(...)        誤答のリストから None と重複を落とす
"""
import math
from fractions import Fraction as Fr
from kr_mid import (M, N, neg, par, sg, dec, sup, unit, figure, kosy, kurve, fig, svg_wrap, text, line,  # noqa: F401
                    INK, RED, BLUE, GREEN, josa, Names, num, fr)
from kr_m2a import poly2


def px(cs, v="x"):
    n = len(cs) - 1
    d = {(n - i, 0): Fr(c) for i, c in enumerate(cs) if c}
    return poly2(d, (v, "_")) if d else "0"


def trim(a):
    a = list(a)
    while len(a) > 1 and a[0] == 0:
        a.pop(0)
    return a


def padd(a, b, k=1):
    n = max(len(a), len(b))
    a = [0] * (n - len(a)) + list(a)
    b = [0] * (n - len(b)) + list(b)
    return trim([x + k * y for x, y in zip(a, b)])


def pmul(a, b):
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return trim(out)


def peval(a, x):
    v = 0
    for c in a:
        v = v * x + c
    return v


def pdiv(a, b):
    a = [Fr(x) for x in a]
    q = []
    while len(a) >= len(b):
        c = a[0] / b[0]
        q.append(c)
        a = [x - c * y for x, y in zip(a, list(b) + [0] * (len(a) - len(b)))][1:]
    return trim(q or [0]), trim(a or [0])


def cx(a, b):
    """a + bi"""
    a, b = Fr(a), Fr(b)
    if b == 0:
        return neg(a)
    bi = ("" if abs(b) == 1 else neg(abs(b))) + "i"
    if a == 0:
        return ("−" if b < 0 else "") + bi
    return "%s %s %s" % (neg(a), "−" if b < 0 else "+", bi)


def sq_split(n):
    a, b, k = 1, int(n), 2
    while k * k <= b:
        while b % (k * k) == 0:
            a *= k
            b //= k * k
        k += 1
    return a, b


def surd(c, n):
    a, b = sq_split(n)
    c = Fr(c) * a
    if c == 0:
        return "0"
    if b == 1:
        return neg(c)
    s = "√%d" % b
    if c == 1:
        return s
    if c == -1:
        return "−" + s
    return neg(c) + s


def mx(rows):
    n = len(rows[0])
    cells = "".join("<span>%s</span>" % (c if isinstance(c, str) else neg(c)) for row in rows for c in row)
    return "<span class='mx m%d'>%s</span>" % (n, cells)


def roots(*rs):
    rs = sorted(set(Fr(r) for r in rs))
    if len(rs) == 1:
        return "x = %s (중근)" % neg(rs[0])
    return " 또는 ".join("x = %s" % neg(r) for r in rs)


def W(*xs):
    out = []
    for x in xs:
        if x is None or x in out:
            continue
        out.append(x)
    return out


def svgf(W_, H, body, label):
    return fig(svg_wrap(int(W_), int(H), body, label).replace("<svg ", "<svg data-pf='lg' ", 1))


def graph(fs, xr=(-5, 5, 1), yr=(-5, 5, 1), pts=(), label="그래프", xlab=None):
    g = kurve(fs, xr, yr, pts, label=label, W=380, H=360, xlab=xlab)
    g = g if "data-pf" in g else g.replace("<svg ", "<svg data-pf='lg' ", 1)
    return g if "qfig" in g else fig(g)
