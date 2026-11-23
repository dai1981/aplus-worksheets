# -*- coding: utf-8 -*-
"""Geometría del espacio (2.º de Bachillerato): vectores, rectas y planos."""
import math
from fractions import Fraction as F
from es_bach import sg, nf, E, raiz, MINUS


def V(*c):
    return "(%s)" % ", ".join(nf(x) for x in c)


def add(u, v, k=1):
    return tuple(a + k * b for a, b in zip(u, v))


def esc(u, v):
    return sum(a * b for a, b in zip(u, v))


def cruz(u, v):
    return (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0])


def mod2(u):
    return esc(u, u)


def plano(n, d):
    """ax + by + cz + d = 0"""
    return "%s = 0" % E((n[0], "x"), (n[1], "y"), (n[2], "z"), (d, ""))


def param(P, v):
    return "<span class='sys'>x = %s<br>y = %s<br>z = %s</span>" % tuple(E((p, ""), (c, "λ")) if p or c else "0" for p, c in zip(P, v))


def continua(P, v):
    parts = []
    for name, p, c in zip("xyz", P, v):
        num_ = name if p == 0 else "%s %s %s" % (name, "−" if p > 0 else "+", nf(abs(p)))
        parts.append("(%s)/%s" % (num_, sg(c)) if num_ != name else "%s/%s" % (name, sg(c)))
    return " = ".join(parts)


def simp(v):
    g = 0
    for x in v:
        g = math.gcd(g, int(x))
    g = g or 1
    v = tuple(int(x) // g for x in v)
    if next((x for x in v if x), 0) < 0:
        v = tuple(-x for x in v)
    return v
