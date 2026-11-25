# -*- coding: utf-8 -*-
"""Sverige årskurs 7–9（högstadiet）: gemensamma delar för se_h_*.py（単元関数は lv = 7, 8, 9 を受け取る）。
se_m（årskurs 4–6）の上に:
・M(q, a, w, e): 4 alternativ, negativa tal tillåtna, felsvar med samma värde som svaret (2,5 och 2,50, 5/10 och 1/2) tas bort
・d(x): Fraction → 2,35（se_m.d）、fq(x): Fraction → bråk i HTML、par(x): (−3)
・expr([(k, "x"), (m, "")]) → 3x − 5、lin(k, m) → y = 3x − 5
・kosy・kurve・figure: diagram (de_k8, de_k10, fr_c4) med svenska aria-label
"""
import math
import re
from fractions import Fraction as F
import se_m as S
from se_m import ri, ch, sh, cap, fr, fq, d, unit, tab  # noqa: F401
from se_common import num, kr, NB, wrap, text, line, fig, INK, GREEN, FILL, RED, BLUE  # noqa: F401

MIN = "−"


def K():
    return S.K


def R():
    return S.R


def coin():
    return S.R.random() < 0.5


def par(x):
    x = F(x)
    s = fq(x) if x.denominator != 1 else d(x)
    return "(%s)" % s if x < 0 else s


def sg(x):
    return fq(F(x)) if F(x).denominator != 1 else d(x)


def coef(k, var, first):
    k = F(k)
    a = abs(k)
    body = ("" if (a == 1 and var) else (fq(a) if a.denominator != 1 else d(a))) + var
    if first:
        return (MIN if k < 0 else "") + body
    return " %s %s" % (MIN if k < 0 else "+", body)


def expr(terms):
    out = ""
    for k, v in terms:
        if F(k) == 0:
            continue
        out += coef(k, v, out == "")
    return out or "0"


def lin(k, m, y="y"):
    return "%s = %s" % (y, expr([(k, "x"), (m, "")]))


def val(t):
    """värdet av ett svar（「−3,50 kr」→ (Fraction, 'kr')）eller None"""
    t = re.sub(r"<span class='fn'>([^<]*)</span><span class='fd'>([^<]*)</span>", r"/\1/\2", str(t))
    t = re.sub(r"<[^>]+>", "", t).replace(NB, "").replace(" ", "").replace(MIN, "-")
    m = re.match(r"^(-?)(\d+(?:,\d+)?)?(?:/(\d+)/(\d+))?([a-zA-Zåäö%²³°]*)$", t)
    if not m or (m.group(2) is None and m.group(3) is None):
        return None
    v = F(m.group(2).replace(",", ".")) if m.group(2) else F(0)
    if m.group(3):
        v += F(int(m.group(3)), int(m.group(4)))
    return (-v if m.group(1) else v, m.group(5))


def M(q, a, w, e):
    a = str(a)
    va = val(a)
    ws = []
    for x in w:
        if x is None:
            continue
        x = str(x)
        if va is not None and val(x) == va:
            continue
        ws.append(x)
    return S.M(q, a, ws, e)


def MN(q, a, w, e, unit_=""):
    """svar som tal (Fraction/int) → text med enhet; felsvar likaså"""
    def term(v):
        try:
            d(v)
            return True
        except ValueError:
            return False

    def f(v):
        v = F(v)
        try:
            t = d(v)
        except ValueError:
            t = fq(v)
        return t + ((("" if unit_ == "°" else NB) + unit_) if unit_ else "")
    ok = term(a)
    return M(q, f(a), [f(x) for x in w if x is not None and (term(x) or not ok)], e)


def rd(x, k=1):
    """avrunda till k decimaler（halva uppåt）, text med komma"""
    x = F(x).limit_denominator(10 ** 9) if isinstance(x, float) else F(x)
    n = int(abs(x) * 10 ** k + F(1, 2))
    s = num(n // 10 ** k) + ("," + str(n % 10 ** k).rjust(k, "0") if k else "")
    return (MIN if x < 0 and n else "") + s


def sup(n):
    if isinstance(n, str):
        return "<sup>%s</sup>" % n.replace("-", MIN)
    return "<sup>%s</sup>" % (MIN + str(-n) if n < 0 else str(n))


def kosy(lines=(), pts=(), lo=-5, hi=5, u=24, label="koordinatsystem"):
    import de_k8
    return de_k8.kosy(lines, pts, lo, hi, u, label)


def kurve(fs, xr, yr, pts=(), W=330, H=250, label="graf"):
    import de_k10
    return de_k10.kurve(fs, xr, yr, pts, W, H, label)


def figure(pts, segs, sides=(), right=(), W=340, H=230, label="geometrisk figur", ticks=(), dashed=()):
    import fr_c4
    return fr_c4.figure(pts, segs, sides, right, W, H, label, ticks, dashed)


def gcd(a, b):
    return math.gcd(a, b)


NAMES_F = ["Alice", "Maja", "Vera", "Ella", "Wilma", "Elsa", "Astrid", "Saga", "Alma", "Selma", "Ebba", "Nora", "Amira", "Freja"]


def lista(xs):
    xs = list(xs)
    return ", ".join(xs[:-1]) + " och " + xs[-1] if len(xs) > 1 else xs[0]


def MQ(t, r, w, e):
    """alternativen står också i frågan（「Vilket tal är delbart med 3: 412, 513, 610 och 722?」）"""
    w = [str(x) for x in w if x is not None and str(x) != str(r)]
    seen, ws = set(), []
    for x in w:
        if x not in seen:
            seen.add(x)
            ws.append(x)
    ws = ws[:3]
    if len(ws) < 3:
        return None
    opts = sh([str(r)] + ws)
    return M("%s %s?" % (t, lista(opts)), r, ws, e)


def gen(n):
    """genitiv: Olles, Elias"""
    return n if n[-1] in "sxz" else n + "s"
