# -*- coding: utf-8 -*-
"""國中七年級の共通部品：負數の書き方など"""
from fractions import Fraction as F
from tw_common import num, fr

MINUS = "－"


def sn(n):
    """整數・Fraction を符號付きで（負は －5、分數は －3/4）"""
    n = F(n)
    neg = n < 0
    a = -n if neg else n
    if a.denominator == 1:
        s = num(a.numerator)
    else:
        s = fr(a.numerator, a.denominator)
    return (MINUS + s) if neg else s


def par(n):
    """負數は（－5）とかっこ付き"""
    return "（%s）" % sn(n) if F(n) < 0 else sn(n)


def term(c, var, first=False):
    """係數 c の項：3x、－x、＋ 2y（first=False なら ＋/－ と空白付き）"""
    c = F(c)
    if c == 0:
        return ""
    a = abs(c)
    body = ("" if a == 1 else (num(a.numerator) if a.denominator == 1 else fr(a.numerator, a.denominator))) + var
    if first:
        return (MINUS if c < 0 else "") + body
    return (" － " if c < 0 else " ＋ ") + body


def const(c, first=False):
    c = F(c)
    if c == 0:
        return "" if not first else "0"
    a = abs(c)
    body = num(a.numerator) if a.denominator == 1 else fr(a.numerator, a.denominator)
    if first:
        return (MINUS if c < 0 else "") + body
    return (" － " if c < 0 else " ＋ ") + body


def lin(a, b, var="x"):
    """ax + b"""
    if a == 0:
        return const(b, True)
    return term(a, var, True) + const(b)


def opv(o, x):
    """「 －（－5）」「 ＋ 5」：演算子と數（負はかっこ）"""
    return " %s%s" % (o, par(x)) if F(x) < 0 else " %s %s" % (o, sn(x))


import re as _re


def _t(s):
    s = _re.sub(r"） ([×÷＋－＝＞＜])", r"）\1", s)
    s = _re.sub(r"([×÷＋－＝＞＜]) （", r"\1（", s)
    return s


def tidy_sets(sets):
    """（－5） × （－2） → （－5）×（－2）：全角かっこの前後の空白を詰める"""
    for _, items in sets:
        for it in items:
            it["q"], it["e"] = _t(it["q"]), _t(it["e"])
            it["c"] = [_t(c) for c in it["c"]]
    return sets


def pw(base, e):
    """次方：負數はかっこ付き、（－3）<sup>2</sup>"""
    b = base if isinstance(base, str) else par(base)
    return "%s<sup>%s</sup>" % (b, e)
