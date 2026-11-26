# -*- coding: utf-8 -*-
"""Shared helpers for the US high school Physics units (gen_us_science_phys_*)."""


def num(x, nd=2):
    """2.0 -> '2', 2.50 -> '2.5', 1368 -> '1,368', -3 -> '−3'"""
    neg = x < 0
    x = abs(x)
    s = ("%.*f" % (nd, x)).rstrip("0").rstrip(".") if nd else "%d" % round(x)
    if "." in s:
        a, b = s.split(".")
        s = "{:,}".format(int(a)) + "." + b
    else:
        s = "{:,}".format(int(s))
    return ("−" if neg and s != "0" else "") + s


def sci(x, nd=2):
    """6.67e-11 -> '6.67 × 10<sup>−11</sup>'"""
    if x == 0:
        return "0"
    e = 0
    m = abs(x)
    while m >= 10:
        m /= 10
        e += 1
    while m < 1:
        m *= 10
        e -= 1
    m = round(m, nd)
    if m >= 10:
        m /= 10
        e += 1
    s = ("%.*f" % (nd, m))
    return ("−" if x < 0 else "") + "%s × 10<sup>%s</sup>" % (s, ("−%d" % -e) if e < 0 else "%d" % e)


def uniq(ans, cands, n=3):
    """first n distinct candidates that differ from the answer"""
    out = []
    for c in cands:
        if c != ans and c not in out:
            out.append(c)
    return out[:n] if len(out) >= n else None


def safe(f):
    """maker wrapper: a question that cannot get 3 distinct wrong answers is skipped (returns None)"""
    def g():
        try:
            return f()
        except (TypeError, AssertionError, ZeroDivisionError):
            return None
    g.__name__ = f.__name__
    return g
