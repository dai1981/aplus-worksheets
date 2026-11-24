# -*- coding: utf-8 -*-
"""
México 2.º y 3.er grado de secundaria (Fase 6): problemas propios.
Usa los mismos ayudantes que mx_s1 (M, sg, fq, dec, peso…). setup(R) antes de usar.
"""
import math
from fractions import Fraction as F
import mx_s1 as S1
from mx_s1 import M, sg, sgd, fq, dexact, tabla_html, MINUS  # noqa: F401
from mx_common import num, dec, peso, NB  # noqa: F401
from ws_common import svg_wrap, text, line, fig

R = None
K = None


def setup(rnd):
    global R, K
    S1.setup(rnd)
    R = S1.R
    K = S1.K


def pick(ks, default):
    return R.choice(ks or default)


def nz(lo, hi):
    while True:
        v = R.randint(lo, hi)
        if v:
            return v


def lin(a, b, v="x"):
    """a x + b → «3x − 5»"""
    s = ("" if a == 1 else MINUS if a == -1 else sg(a)) + v if a else ""
    if b:
        s += (" + %s" % num(b) if b > 0 else " − %s" % num(-b)) if s else sg(b)
    return s or "0"


def quad(a, b, c, v="x"):
    t = []
    for k, e in ((a, "²"), (b, ""), (c, None)):
        if not k:
            continue
        body = (num(abs(k)) if abs(k) != 1 or e is None else "") + (v + e if e is not None else "")
        t.append((k < 0, body))
    if not t:
        return "0"
    s = (MINUS if t[0][0] else "") + t[0][1]
    for neg, body in t[1:]:
        s += (" − " if neg else " + ") + body
    return s


# ============================================================ 2.º: números con signo en la recta, densidad
def rn_recta(*ks):
    t = pick(ks, ["mayor", "mayor", "orden", "entre", "densidad", "recta"])
    if t == "mayor":
        a = F(-R.randint(1, 9), R.choice([2, 3, 4, 5, 8]))
        b = F(-R.randint(1, 9), 10) if R.random() < .5 else F(-R.randint(1, 9), R.choice([3, 4, 6]))
        if a == b:
            return None
        sa, sb = fq(a), (dexact(b) if b.denominator == 10 else fq(b))
        ok = sa if a > b else sb
        return M("¿Qué número es mayor: %s o %s?" % (sa, sb), ok, [sb if ok == sa else sa, "son iguales", "no se pueden comparar"],
                 "%s ≈ %s y %s ≈ %s. Entre negativos, es mayor el que está más cerca del 0: <b>%s</b>." % (sa, sgd(round(float(a), 3)), sb, sgd(round(float(b), 3)), ok))
    if t == "orden":
        vals = set()
        while len(vals) < 4:
            vals.add(F(R.randint(-20, 20), R.choice([1, 2, 4, 5, 10])))
        vals = list(vals)
        if not any(v < 0 for v in vals):
            return None
        show = lambda v: dexact(v) if v.denominator in (5, 10) else fq(v)
        srt = sorted(vals)
        ok = " &lt; ".join(show(v) for v in srt)
        w = [" &lt; ".join(show(v) for v in sorted(vals, key=abs)), " &lt; ".join(show(v) for v in srt[::-1]), " &lt; ".join(show(v) for v in srt[1:2] + srt[:1] + srt[2:])]
        return M("Ordena de menor a mayor: %s" % ", ".join(show(v) for v in vals), ok, w, "Pasa todo a decimal y ubícalo en la recta: <b>%s</b>." % ok)
    if t == "entre":
        a = F(-R.randint(1, 5), R.choice([2, 3, 4]))
        b = a + F(R.choice([1, 2]), R.choice([4, 6, 10]))
        m = (a + b) / 2
        w1 = a - F(1, 10)
        w2 = b + F(1, 10)
        return M("¿Qué número está entre %s y %s?" % (fq(a), fq(b)), fq(m), [fq(w1), fq(w2), fq(-m)],
                 "El promedio de dos números siempre está entre ellos: (%s + %s) ÷ 2 = <b>%s</b>." % (fq(a), fq(b), fq(m)))
    if t == "densidad":
        a = R.randint(0, 8)
        q = R.choice([("¿Cuántos números decimales hay entre %d.1 y %d.2?" % (a, a), "infinitos"), ("¿Cuántos números enteros hay entre %d.1 y %d.2?" % (a, a), "ninguno"),
                      ("¿Cuántas fracciones hay entre 1/%d y 1/%d?" % (a + 3, a + 2), "infinitas"), ("¿Cuántos números enteros hay entre −%d.5 y %d.5?" % (a + 1, a), str(2 * a + 2))])
        pool = ["infinitos", "ninguno", "uno", "diez"] if q[1] in ("infinitos", "ninguno") else ["infinitas", "ninguna", "una", "nueve"] if q[1] == "infinitas" else [str(2 * a + 1), str(2 * a + 3), "infinitos"]
        return M(q[0], q[1], [x for x in pool if x != q[1]],
                 "Entre dos números racionales distintos siempre hay infinitos números (propiedad de densidad); los enteros, en cambio, se pueden contar. Respuesta: <b>%s</b>." % q[1])
    k = R.choice([2, 4, 5])
    v = F(-R.randint(1, 3 * k - 1), k)
    if v.denominator == 1:
        return None
    pic = S1_recta_frac(-3, 0, k, v)
    return M(pic + "¿Qué número marca el punto P?", fq(v), [fq(-v), fq(v - F(1, k)), fq(F(v.numerator, v.denominator + 1))],
             "Cada unidad está dividida en %d partes. P está %d partes a la izquierda del 0: <b>%s</b>." % (k, -v * k, fq(v)))


def S1_recta_frac(lo, hi, k, v):
    W_, H_ = 420, 70
    x0, x1 = 30, 390
    X = lambda t: x0 + (t - lo) * (x1 - x0) / float(hi - lo)
    s = [line(x0 - 10, 35, x1 + 10, 35, "#222", 2)]
    for i in range((hi - lo) * k + 1):
        t = lo + F(i, k)
        big = t.denominator == 1
        s.append(line(X(t), 35 - (9 if big else 5), X(t), 35 + (9 if big else 5), "#222", 2 if big else 1.2))
        if big:
            s.append(text(X(t), 62, sg(int(t)), 13))
    s.append("<circle cx='%.1f' cy='35' r='6' fill='#c0392b'/>" % X(v))
    s.append(text(X(v), 18, "P", 14, col="#c0392b"))
    return fig(svg_wrap(W_, H_, "".join(s), "recta numérica con el punto P"))


# ============================================================ 2.º: propiedades de las operaciones
def prop_ops(*ks):
    t = pick(ks, ["cual", "cual", "cual", "resta", "dist", "dist", "calc"])
    a, b, c = nz(-9, 9), nz(-9, 9), nz(-9, 9)
    P = lambda v: "(%s)" % sg(v) if v < 0 else sg(v)
    if t == "cual":
        q = R.choice([("%s + %s = %s + %s" % (sg(a), P(b), sg(b), P(a)), "conmutativa"), ("%s × %s = %s × %s" % (sg(a), P(b), sg(b), P(a)), "conmutativa"),
                      ("(%s + %s) + %s = %s + (%s + %s)" % (sg(a), P(b), P(c), sg(a), sg(b), P(c)), "asociativa"), ("(%s × %s) × %s = %s × (%s × %s)" % (sg(a), P(b), P(c), sg(a), sg(b), P(c)), "asociativa"),
                      ("%s × (%s + %s) = %s × %s + %s × %s" % (sg(a), sg(b), P(c), sg(a), P(b), P(a), P(c)), "distributiva"), ("%s + 0 = %s" % (sg(a), sg(a)), "elemento neutro"),
                      ("%s × 1 = %s" % (sg(a), sg(a)), "elemento neutro"), ("%s + %s = 0" % (sg(a), P(-a)), "inverso aditivo")])
        return M("¿Qué propiedad se usa? %s" % q[0], q[1], [x for x in ["conmutativa", "asociativa", "distributiva", "elemento neutro", "inverso aditivo"] if x != q[1]][:3],
                 "Es la propiedad <b>%s</b>." % q[1])
    if t == "resta":
        q = R.choice([("¿La resta es conmutativa? Compara %d − %d y %d − %d." % (abs(a) + 5, abs(b), abs(b), abs(a) + 5), "No: %s ≠ %s" % (sg(abs(a) + 5 - abs(b)), sg(abs(b) - abs(a) - 5))),
                      ("¿La división es conmutativa? Compara 12 ÷ 4 y 4 ÷ 12.", "No: 3 ≠ 1/3"), ("¿La multiplicación de números con signo es conmutativa? Compara %s × %s y %s × %s." % (sg(a), P(b), sg(b), P(a)), "Sí: los dos dan %s" % sg(a * b)),
                      ("¿La resta es asociativa? Compara (10 − 6) − 3 y 10 − (6 − 3).", "No: 1 ≠ 7")])
        w = ["Sí: siempre se puede cambiar el orden", "No: nunca da lo mismo", "Solo con números positivos"]
        return M(q[0], q[1], w, "Calculamos los dos lados: <b>%s</b>." % q[1])
    if t == "dist":
        k = nz(-6, 6)
        m, n = nz(-5, 5), nz(-9, 9)
        ok = lin(k * m, k * n)
        return M("Aplica la propiedad distributiva: %s(%s)" % (sg(k) if k != -1 else MINUS, lin(m, n)), ok, [lin(k * m, n), lin(k * m, -k * n), lin(m + k, k * n)],
                 "Multiplicamos %s por cada término (cuidado con los signos): <b>%s</b>." % (sg(k), ok))
    x, y, z = R.randint(11, 99), R.choice([98, 99, 101, 102, 25, 50]), R.randint(2, 9)
    if y in (25, 50):
        return M("Calcula mentalmente con la propiedad asociativa: %d × %d × %d" % (y, x, 4 if y == 25 else 2), num(y * x * (4 if y == 25 else 2)),
                 [num(y * x), num(x * 100 + 4), num(y * x * (4 if y == 25 else 2) + x)], "Agrupamos %d × %d = 100 y luego × %d: <b>%s</b>." % (y, 4 if y == 25 else 2, x, num(y * x * (4 if y == 25 else 2))))
    return M("Calcula con la propiedad distributiva: %d × %d" % (x, y), num(x * y), [num(x * 100), num(x * y + 10), num(x * y - 2 * x), num(x * y + 2 * x)],
             "%d × %d = %d × (100 %s %d) = %s %s %s = <b>%s</b>." % (x, y, x, "−" if y < 100 else "+", abs(100 - y), num(x * 100), "−" if y < 100 else "+", num(x * abs(100 - y)), num(x * y)))


# ============================================================ 2.º: perímetros y áreas con expresiones
def alg_figuras(*ks):
    t = pick(ks, ["perim", "perim", "area", "area", "cuad", "exp"])
    if t == "perim":
        kind = R.choice(["rect", "tri", "cuad", "hexa", "trap"])
        a, b = R.randint(1, 5), R.randint(1, 9)
        if kind == "rect":
            ok = lin(4 * a if False else 2 * (a + 1), 2 * b)
            return M("Un rectángulo mide x cm de ancho y (%s) cm de largo. ¿Qué expresión da su perímetro?" % lin(a, b), lin(2 + 2 * a, 2 * b),
                     [lin(1 + a, b), lin(2 * a, 2 * b), quad(a, b, 0)], "P = 2(x) + 2(%s) = <b>%s</b>." % (lin(a, b), lin(2 + 2 * a, 2 * b)))
        if kind == "tri":
            return M("Los lados de un triángulo miden x, %s y %s. ¿Qué expresión da su perímetro?" % (lin(1, b), lin(a, 0)), lin(2 + a, b),
                     [lin(1 + a, b), lin(2 + a, 2 * b), lin(3, b)], "Sumamos los tres lados: x + (%s) + %s = <b>%s</b>." % (lin(1, b), lin(a, 0), lin(2 + a, b)))
        if kind == "cuad":
            return M("El lado de un cuadrado mide (%s) cm. ¿Qué expresión da su perímetro?" % lin(a, b), lin(4 * a, 4 * b), [lin(4 * a, b), lin(a + 4, b), quad(a * a, 2 * a * b, b * b)],
                     "P = 4(%s) = <b>%s</b>." % (lin(a, b), lin(4 * a, 4 * b)))
        if kind == "hexa":
            return M("Un hexágono regular tiene lados de (%s) cm. ¿Qué expresión da su perímetro?" % lin(a, b), lin(6 * a, 6 * b), [lin(6 * a, b), lin(a, 6 * b), lin(5 * a, 5 * b)],
                     "6 lados iguales: 6(%s) = <b>%s</b>." % (lin(a, b), lin(6 * a, 6 * b)))
        return M("Un trapecio isósceles tiene bases de 2x y %s, y lados iguales de %s cada uno. ¿Qué expresión da su perímetro?" % (lin(1, b), lin(a, 0)), lin(3 + 2 * a, b),
                 [lin(3 + a, b), lin(3 + 2 * a, 2 * b), lin(2 + 2 * a, b)], "2x + (%s) + 2(%s) = <b>%s</b>." % (lin(1, b), lin(a, 0), lin(3 + 2 * a, b)))
    if t == "area":
        a = R.randint(1, 6)
        b = R.randint(1, 9)
        kind = R.choice(["rect", "tri", "cuad"])
        if kind == "rect":
            return M("Un rectángulo mide x de ancho y (%s) de largo. ¿Qué expresión da su área?" % lin(a, b), quad(a, b, 0), [lin(a + 1, b), quad(a, 0, b), lin(2 * a + 2, 2 * b)],
                     "A = x(%s) = <b>%s</b>." % (lin(a, b), quad(a, b, 0)))
        if kind == "tri":
            a2 = 2 * a
            return M("Un triángulo tiene base %s y altura x. ¿Qué expresión da su área?" % lin(a2, 2 * b), quad(a, b, 0), [quad(a2, 2 * b, 0), lin(a2 + 1, 2 * b), quad(a, 2 * b, 0)],
                     "A = (%s)(x) ÷ 2 = <b>%s</b>." % (lin(a2, 2 * b), quad(a, b, 0)))
        return M("El lado de un cuadrado mide %s. ¿Qué expresión da su área?" % lin(a, 0), quad(a * a, 0, 0), [lin(4 * a, 0), quad(a, 0, 0), lin(a * a, 0)],
                 "A = (%s)² = <b>%s</b>." % (lin(a, 0), quad(a * a, 0, 0)))
    if t == "cuad":
        a, b = R.randint(1, 6), R.randint(1, 6)
        return M("Un terreno cuadrado de lado x se agranda %d m de largo y %d m de ancho. ¿Qué expresión da el área nueva?" % (a, b), quad(1, a + b, a * b),
                 [quad(1, 0, a * b), quad(1, a * b, a + b), lin(2, a + b)], "(x + %d)(x + %d) = x² + %dx + %dx + %d = <b>%s</b>." % (a, b, b, a, a * b, quad(1, a + b, a * b)))
    m, n = R.randint(2, 6), R.randint(2, 6)
    k = R.choice(["mult", "div", "pot"])
    if k == "mult":
        return M("Simplifica: x<sup>%d</sup> · x<sup>%d</sup>" % (m, n), "x<sup>%d</sup>" % (m + n), ["x<sup>%d</sup>" % (m * n), "2x<sup>%d</sup>" % (m + n), "x<sup>%d</sup>" % abs(m - n) if m != n else "x"],
                 "Al multiplicar potencias de la misma base se suman los exponentes: <b>x<sup>%d</sup></b>." % (m + n))
    if k == "div":
        m = n + R.randint(1, 5)
        return M("Simplifica: x<sup>%d</sup> ÷ x<sup>%d</sup>" % (m, n), "x<sup>%d</sup>" % (m - n) if m - n > 1 else "x", ["x<sup>%d</sup>" % (m + n), "x<sup>%d</sup>" % (m * n), "1"],
                 "Al dividir se restan los exponentes: %d − %d = <b>%d</b>." % (m, n, m - n))
    return M("Simplifica: (x<sup>%d</sup>)<sup>%d</sup>" % (m, n), "x<sup>%d</sup>" % (m * n), ["x<sup>%d</sup>" % (m + n), "x<sup>%d</sup>" % (m ** n) if m ** n < 100 else "%dx<sup>%d</sup>" % (n, m), "x<sup>%d</sup>" % (m * n + 1)],
             "Potencia de una potencia: se multiplican los exponentes: <b>x<sup>%d</sup></b>." % (m * n))


# ============================================================ 2.º: desigualdades
def desig(*ks):
    t = pick(ks, ["res", "res", "res", "neg", "check", "prob"])
    sym = R.choice(["&gt;", "&lt;", "≥", "≤"])
    flip = {"&gt;": "&lt;", "&lt;": "&gt;", "≥": "≤", "≤": "≥"}
    if t in ("res", "neg"):
        a = R.randint(2, 9) * (-1 if t == "neg" else 1)
        x = R.randint(-9, 12)
        b = R.randint(-15, 15)
        c = a * x + b
        s2 = flip[sym] if a < 0 else sym
        ok = "x %s %s" % (s2, sg(x))
        w = ["x %s %s" % (flip[s2], sg(x)), "x %s %s" % (s2, sg(-x)) if x else "x %s 1" % s2, "x %s %s" % (s2, fq(F(c + b, a)) if (c + b) != x * a else sg(x + 1))]
        return M("Resuelve la desigualdad: %s %s %s" % (lin(a, b), sym, sg(c)), ok, w,
                 "%s%s Al final dividimos entre %s%s: <b>%s</b>." % ("Restamos %s en los dos lados: " % sg(b) if b > 0 else "Sumamos %s en los dos lados: " % sg(-b) if b < 0 else "",
                                                                       "%s %s %s." % (lin(a, 0), sym, sg(c - b)) if b else "", sg(a), " (negativo: el signo de la desigualdad se invierte)" if a < 0 else "", ok))
    if t == "check":
        a, b = R.randint(2, 6), R.randint(-9, 9)
        lim_ = R.randint(5, 30)
        vals = R.sample(range(-5, 15), 4)
        good = [v for v in vals if a * v + b > lim_]
        bad = [v for v in vals if a * v + b <= lim_]
        if not good or len(bad) < 3:
            return None
        g = good[0]
        return M("¿Cuál de estos valores cumple %s &gt; %d?" % (lin(a, b), lim_), sg(g), [sg(v) for v in bad],
                 "Sustituimos: %s(%s)%s = %s &gt; %d. <b>%s</b> cumple." % (a, sg(g), (" + %d" % b) if b > 0 else (" − %d" % -b) if b < 0 else "", sg(a * g + b), lim_, sg(g)))
    p = R.choice([15, 18, 22, 25, 35])
    tot = R.choice([150, 200, 250, 300, 500])
    fijo = R.choice([0, 20, 30, 40])
    n = (tot - fijo) // p
    return M("%s tiene %s. Gasta %s en el pasaje y quiere comprar paletas de %s cada una. ¿Cuántas paletas puede comprar como máximo?" % (K.next()[0], peso(tot * 100), peso(fijo * 100) if fijo else "$0", peso(p * 100)) if fijo else
             "%s tiene %s y quiere comprar paletas de %s cada una. ¿Cuántas puede comprar como máximo?" % (K.next()[0], peso(tot * 100), peso(p * 100)),
             str(n), [str(n + 1), str(tot // p) if tot // p != n else str(n - 1), str((tot + fijo) // p) if (tot + fijo) // p not in (n, n + 1) else str(n + 2)],
             "%s%dx ≤ %d → x ≤ %s. Como deben ser paletas completas: <b>%d</b>." % ("%d + " % fijo if fijo else "", p, tot, dec((tot - fijo) / float(p), 2), n))


# ============================================================ 2.º: proporcionalidad con constante negativa e inversa
def prop_inv(*ks):
    t = pick(ks, ["inv", "inv", "tabla_inv", "neg", "neg", "tipo"])
    if t == "inv":
        k = R.choice([24, 36, 48, 60, 72, 120])
        a = R.choice([d for d in range(2, 13) if k % d == 0])
        b = R.choice([d for d in range(2, 13) if k % d == 0 and d != a])
        ctx = R.choice([("%d trabajadores terminan una barda en %d días. ¿Cuántos días tardarían %d trabajadores al mismo ritmo?", "días"),
                        ("Un carro a %d km/h tarda %d horas. ¿Cuántas horas tardaría a %d km/h?", "horas"),
                        ("Con %d llaves iguales abiertas, un tinaco se llena en %d minutos. ¿Cuántos minutos tardaría con %d llaves?", "minutos")])
        if ctx[1] == "horas":
            a, b = a * 10, b * 10
            k = k * 10
        dire = F(k // a * b, a)
        w = ["%s %s" % (dexact(dire) or num(int(dire) + 1), ctx[1]), "%d %s" % (k // a + 1, ctx[1]), "%d %s" % (k, ctx[1]), "%d %s" % (k // a * 2, ctx[1])]
        return M(ctx[0] % (a, k // a, b), "%d %s" % (k // b, ctx[1]), w,
                 "Es proporcionalidad <b>inversa</b>: el producto es constante, %d × %d = %d. %d ÷ %d = <b>%d</b>." % (a, k // a, k, k, b, k // b))
    if t == "tabla_inv":
        k = R.choice([12, 24, 36, 60])
        xs = sorted(R.sample([d for d in range(1, 13) if k % d == 0], 4))
        x = xs[R.randint(1, 3)]
        t_ = tabla_html(["x"] + [str(v) for v in xs], [["y"] + [str(k // v) if v != x else "?" for v in xs]])
        return M(t_ + "x e y son inversamente proporcionales. ¿Qué número va en «?»?", str(k // x), [str(k * x), str(k // xs[0] - x), str(x)],
                 "x × y = %d siempre. %d ÷ %d = <b>%d</b>." % (k, k, x, k // x))
    if t == "neg":
        k = nz(-6, -1)
        x = nz(-8, 8)
        if R.random() < .5:
            return M("En la relación y = %sx, ¿cuánto vale y cuando x = %s?" % (sg(k) if k != -1 else MINUS, sg(x)), sg(k * x), [sg(-k * x), sg(k + x), sg(k * x + k)],
                     "y = %s × %s = <b>%s</b>." % (sg(k), "(%s)" % sg(x) if x < 0 else sg(x), sg(k * x)))
        xs = [1, 2, 3, 4]
        t_ = tabla_html(["x"] + [str(v) for v in xs], [["y"] + [sg(k * v) for v in xs]])
        cx = lambda c: ("" if c == 1 else MINUS if c == -1 else sg(c)) + "x"
        return M(t_ + "¿Qué expresión relaciona x e y?", "y = " + cx(k), ["y = " + cx(-k), "y = x %s" % ("− %d" % -k), "y = %s + 1" % cx(k)],
                 "y ÷ x = %s siempre: constante de proporcionalidad negativa, <b>y = %sx</b>." % (sg(k), sg(k) if k != -1 else MINUS))
    q = R.choice([("La velocidad de un carro y el tiempo que tarda en recorrer 100 km", "inversa"), ("El número de pintores y el tiempo que tardan en pintar una casa", "inversa"),
                   ("Los kilos de tortilla y lo que se paga", "directa"), ("El número de boletos y lo que se paga por ellos", "directa"),
                   ("La edad y la estatura de una persona", "ninguna"), ("El número de amigos que se reparten $500 y lo que le toca a cada uno", "inversa"),
                   ("Los litros de agua en un tinaco y el tiempo que lleva llenándose a ritmo constante", "directa"), ("La temperatura del día y la hora", "ninguna")])
    lab = {"directa": "proporcionalidad directa", "inversa": "proporcionalidad inversa", "ninguna": "no son proporcionales"}
    return M("¿Qué relación hay? %s." % q[0], lab[q[1]], [v for k_, v in lab.items() if k_ != q[1]] + ["son iguales"],
             "En la directa, si una se duplica la otra también; en la inversa, si una se duplica la otra se reduce a la mitad. Respuesta: <b>%s</b>." % lab[q[1]])


# ============================================================ 2.º: ángulos al cortarse dos rectas
def cross_svg(a):
    W_, H_, cx, cy, L = 300, 200, 150, 100, 130
    r1 = math.radians(a)
    L2 = min(L, 92 / max(math.sin(r1), .01))
    s = [line(cx - L, cy, cx + L, cy, "#222", 2.5), line(cx - L2 * math.cos(r1), cy + L2 * math.sin(r1), cx + L2 * math.cos(r1), cy - L2 * math.sin(r1), "#222", 2.5)]
    s.append("<path d='M%.1f %.1f A28 28 0 0 0 %.1f %.1f' fill='none' stroke='#c0392b' stroke-width='2'/>" % (cx + 28, cy, cx + 28 * math.cos(r1), cy - 28 * math.sin(r1)))
    s.append(text(cx + 48 * math.cos(r1 / 2) + 6, cy - 40 * math.sin(r1 / 2) + 4, "%d°" % a, 14, col="#c0392b"))
    s.append(text(cx - 44 * math.cos(r1 / 2), cy + 40 * math.sin(r1 / 2) + 12, "x", 15, italic=True, col="#2b6cb0"))
    s.append(text(cx + 38 * math.cos((math.pi + r1) / 2) - 6, cy - 36 * math.sin((math.pi + r1) / 2) + 4, "y", 15, italic=True, col="#1e8449"))
    return fig(svg_wrap(W_, H_, "".join(s), "dos rectas que se cortan; un ángulo de %d grados" % a))


def ang_cruce(*ks):
    t = pick(ks, ["fig", "fig", "op", "ady", "ecu", "tres"])
    a = R.choice([v for v in range(25, 156, 5) if abs(v - 90) > 5])
    if t == "fig":
        which = R.choice(["x", "y"])
        ok = a if which == "x" else 180 - a
        return M(cross_svg(a) + "Dos rectas se cortan. ¿Cuánto mide el ángulo %s?" % which, "%d°" % ok, ["%d°" % (180 - ok), "%d°" % (90 - ok if ok < 90 else ok - 90), "%d°" % (360 - ok)],
                 ("x es opuesto por el vértice al de %d°: son iguales, <b>%d°</b>." % (a, ok)) if which == "x" else ("y es adyacente al de %d°: suman 180°, 180° − %d° = <b>%d°</b>." % (a, a, ok)))
    if t == "op":
        return M("Dos segmentos se cortan y uno de los ángulos mide %d°. ¿Cuánto mide su ángulo opuesto por el vértice?" % a, "%d°" % a, ["%d°" % (180 - a), "%d°" % (360 - a), "%d°" % abs(90 - a)],
                 "Los ángulos opuestos por el vértice son iguales: <b>%d°</b>." % a)
    if t == "ady":
        return M("Dos rectas se cortan y uno de los ángulos mide %d°. ¿Cuánto suman los cuatro ángulos?" % a if R.random() < .3 else
                 "Dos rectas se cortan y uno de los ángulos mide %d°. ¿Cuánto mide cada ángulo adyacente a él?" % a,
                 "360°" if False else "%d°" % (180 - a), ["%d°" % a, "%d°" % (360 - a), "%d°" % abs(90 - a)], "Los adyacentes suman 180°: <b>%d°</b>." % (180 - a))
    if t == "ecu":
        x = R.randint(10, 40)
        k = R.choice([2, 3, 4])
        b = R.randint(-10, 20)
        m = R.randint(5, 30)
        if k * x + b <= 0 or k * x + b >= 180:
            return None
        rel = R.choice(["op", "ady"])
        if rel == "op":
            c = k * x + b - m
            if c <= 0:
                return None
            return M("Dos ángulos opuestos por el vértice miden (%s)° y %d°. ¿Cuánto vale x?" % (lin(k, b), k * x + b), "%d" % x, ["%d" % (k * x + b), "%d" % (x + 1), "%d" % (x + 2)],
                     "Son iguales: %s = %d → %dx = %d → x = <b>%d</b>." % (lin(k, b), k * x + b, k, k * x, x))
        other = 180 - (k * x + b)
        return M("Dos ángulos adyacentes formados por dos rectas que se cortan miden (%s)° y %d°. ¿Cuánto vale x?" % (lin(k, b), other), "%d" % x,
                 ["%d" % ((other - b) // k) if (other - b) % k == 0 and (other - b) // k != x else "%d" % (x + 3), "%d" % (x - 1), "%d" % (180 - other)],
                 "Suman 180°: %s + %d = 180 → %dx = %d → x = <b>%d</b>." % (lin(k, b), other, k, k * x, x))
    b2 = R.choice(range(20, 80, 5))
    c = 180 - a - b2
    if c <= 0:
        return None
    return M("Tres rectas se cortan en un punto y forman, uno junto a otro, ángulos de %d°, %d° y x en media vuelta. ¿Cuánto mide x?" % (a, b2), "%d°" % c, ["%d°" % (360 - a - b2), "%d°" % (a + b2), "%d°" % abs(a - b2)],
             "Juntos forman un ángulo llano: 180° − %d° − %d° = <b>%d°</b>." % (a, b2, c))


# ============================================================ 2.º: rectas y puntos notables del triángulo
NOT = [("altura", "el segmento perpendicular desde un vértice al lado opuesto (o a su prolongación)", "ortocentro"),
       ("mediana", "el segmento que une un vértice con el punto medio del lado opuesto", "baricentro (gravicentro)"),
       ("mediatriz", "la recta perpendicular a un lado por su punto medio", "circuncentro"),
       ("bisectriz", "la recta que divide un ángulo en dos ángulos iguales", "incentro")]


def notables(*ks):
    t = pick(ks, ["def", "punto", "punto2", "med", "bar", "bis", "circ"])
    if t == "def":
        n = R.choice(NOT)
        return M("¿Cómo se llama %s de un triángulo?" % n[1], "la " + n[0], ["la " + x[0] for x in NOT if x != n], "Es <b>la %s</b>." % n[0])
    if t == "punto":
        n = R.choice(NOT)
        plu = {"altura": "alturas", "mediana": "medianas", "mediatriz": "mediatrices", "bisectriz": "bisectrices"}[n[0]]
        return M("¿Qué punto se forma donde se cortan las tres %s de un triángulo?" % plu, n[2], [x[2] for x in NOT if x != n],
                 "Las tres %s se cortan en el <b>%s</b>." % (plu, n[2]))
    if t == "punto2":
        q = R.choice([("¿Qué punto es el centro de la circunferencia que pasa por los tres vértices?", "circuncentro"), ("¿Qué punto es el centro de la circunferencia que toca los tres lados por dentro?", "incentro"),
                      ("¿En qué punto se equilibraría un triángulo de cartón sobre la punta de un lápiz?", "baricentro (gravicentro)"), ("¿Qué punto está a la misma distancia de los tres vértices?", "circuncentro"),
                      ("¿Qué punto está a la misma distancia de los tres lados?", "incentro")])
        return M(q[0], q[1], [x[2] for x in NOT if x[2] != q[1]], "Es el <b>%s</b>." % q[1])
    if t == "med":
        L = R.choice(range(6, 61, 2))
        return M("En el triángulo ABC, la mediana desde A llega al lado BC, que mide %d cm, en el punto M. ¿Cuánto mide BM?" % L, "%d cm" % (L // 2), ["%d cm" % L, "%s cm" % dec(L / 3.0, 1) if L % 3 else "%d cm" % (L // 3), "%d cm" % (2 * L)],
                 "La mediana llega al <b>punto medio</b> del lado: %d ÷ 2 = <b>%d cm</b>." % (L, L // 2))
    if t == "bar":
        L = R.choice(range(6, 91, 3))
        return M("Una mediana mide %d cm. El baricentro la divide en dos partes, una el doble de la otra. ¿Cuánto mide la parte que va del vértice al baricentro?" % L, "%d cm" % (2 * L // 3),
                 ["%d cm" % (L // 3), "%s cm" % dec(L / 2.0), "%d cm" % L], "El baricentro está a 2/3 del vértice: %d × 2/3 = <b>%d cm</b>." % (L, 2 * L // 3))
    if t == "bis":
        a = R.choice(range(30, 151, 2))
        return M("En un triángulo, el ángulo A mide %d°. La bisectriz desde A lo divide en dos ángulos. ¿Cuánto mide cada uno?" % a, "%d°" % (a // 2), ["%d°" % a, "%d°" % (90 - a // 2), "%d°" % (180 - a)],
                 "La bisectriz divide el ángulo en dos partes iguales: <b>%d°</b>." % (a // 2))
    q = R.choice([("¿En qué triángulo el ortocentro está en un vértice?", "en el triángulo rectángulo", ["en el equilátero", "en el obtusángulo", "en el isósceles"]),
                  ("¿En qué triángulo el circuncentro queda fuera del triángulo?", "en el obtusángulo", ["en el acutángulo", "en el equilátero", "en ninguno"]),
                  ("¿En qué triángulo coinciden el baricentro, el ortocentro, el circuncentro y el incentro?", "en el equilátero", ["en el rectángulo", "en el escaleno", "en el obtusángulo"]),
                  ("En un triángulo rectángulo, ¿dónde está el circuncentro?", "en el punto medio de la hipotenusa", ["en el vértice del ángulo recto", "fuera del triángulo", "en el incentro"])])
    return M(q[0], q[1], q[2], "<b>%s</b>." % (q[1][0].upper() + q[1][1:]))


# ============================================================ 2.º: triángulos y cuadriláteros
def triangulos(*ks):
    t = pick(ks, ["suma", "suma", "ext", "clas", "cuad", "exist", "iso"])
    if t == "suma":
        a, b = R.randint(20, 100), R.randint(20, 100)
        c = 180 - a - b
        if c <= 0:
            return None
        return M("Dos ángulos de un triángulo miden %d° y %d°. ¿Cuánto mide el tercero?" % (a, b), "%d°" % c, ["%d°" % (360 - a - b), "%d°" % (a + b), "%d°" % (90 - c if c < 90 else c - 10)],
                 "Los ángulos de un triángulo suman 180°: 180 − %d − %d = <b>%d°</b>." % (a, b, c))
    if t == "ext":
        a, b = R.randint(25, 80), R.randint(25, 80)
        return M("En un triángulo, dos ángulos interiores miden %d° y %d°. ¿Cuánto mide el ángulo exterior del tercer vértice?" % (a, b), "%d°" % (a + b), ["%d°" % (180 - a - b), "%d°" % (360 - a - b), "%d°" % (abs(a - b) + 90)],
                 "El ángulo exterior es igual a la suma de los dos interiores no adyacentes: <b>%d°</b>." % (a + b))
    if t == "clas":
        a = R.choice([R.randint(20, 85), 90, R.randint(95, 150)])
        b = R.randint(15, 175 - a - 5) if a < 170 else 5
        c = 180 - a - b
        if c <= 0:
            return None
        mx = max(a, b, c)
        ok = "rectángulo" if mx == 90 else "obtusángulo" if mx > 90 else "acutángulo"
        return M("Un triángulo tiene ángulos de %d°, %d° y %d°. ¿Cómo se clasifica por sus ángulos?" % (a, b, c), ok, [x for x in ["rectángulo", "obtusángulo", "acutángulo", "equilátero"] if x != ok],
                 "El ángulo mayor mide %d°: es <b>%s</b>." % (mx, ok))
    if t == "cuad":
        a, b, c = R.randint(60, 130), R.randint(60, 130), R.randint(60, 120)
        d = 360 - a - b - c
        if d <= 20 or d >= 180:
            return None
        return M("Tres ángulos de un cuadrilátero miden %d°, %d° y %d°. ¿Cuánto mide el cuarto?" % (a, b, c), "%d°" % d, ["%d°" % (180 - (a + b + c) % 180), "%d°" % (d + 10), "%d°" % (540 - a - b - c)],
                 "Los ángulos de un cuadrilátero suman 360°: <b>%d°</b>." % d)
    if t == "iso":
        v = R.choice(range(20, 141, 2))
        return M("En un triángulo isósceles, el ángulo desigual mide %d°. ¿Cuánto mide cada uno de los otros dos?" % v, "%d°" % ((180 - v) // 2), ["%d°" % (180 - v), "%d°" % v, "%d°" % ((180 - v) // 3 if (180 - v) % 3 == 0 else (180 - v) // 2 + 5)],
                 "Los dos ángulos iguales suman 180 − %d = %d: cada uno <b>%d°</b>." % (v, 180 - v, (180 - v) // 2))
    if t == "exist":
        return S1.cf_construccion("exist")
    q = R.choice([("¿Qué cuadrilátero tiene sus cuatro lados iguales y sus ángulos rectos?", "el cuadrado"), ("¿Qué cuadrilátero tiene solo un par de lados paralelos?", "el trapecio"),
                  ("¿Qué cuadrilátero tiene lados iguales pero ángulos que no son rectos?", "el rombo"), ("¿Qué cuadrilátero tiene ángulos rectos y lados opuestos iguales pero no los cuatro iguales?", "el rectángulo")])
    return M(q[0], q[1], [x for x in ["el cuadrado", "el trapecio", "el rombo", "el rectángulo", "el romboide"] if x != q[1]][:3], "<b>%s</b>." % q[1].capitalize())


# ============================================================ 2.º: ángulos en la circunferencia
def circ_ang_svg(c):
    W_, H_, cx, cy, r = 260, 230, 130, 118, 92
    p = lambda d: (cx + r * math.cos(math.radians(d)), cy - r * math.sin(math.radians(d)))
    a0 = -90 - c / 2.0
    A, B = p(a0), p(a0 + c)
    V = p(90)
    s = ["<circle cx='%d' cy='%d' r='%d' fill='none' stroke='#222' stroke-width='2.2'/>" % (cx, cy, r),
         line(cx, cy, A[0], A[1], "#2b6cb0", 2), line(cx, cy, B[0], B[1], "#2b6cb0", 2),
         line(V[0], V[1], A[0], A[1], "#c0392b", 2), line(V[0], V[1], B[0], B[1], "#c0392b", 2),
         "<circle cx='%d' cy='%d' r='3.5' fill='#222'/>" % (cx, cy), text(cx + 12, cy - 4, "O", 13),
         text(A[0] - 10, A[1] + 14, "A", 14), text(B[0] + 10, B[1] + 14, "B", 14), text(V[0], V[1] - 8, "V", 14)]
    return fig(svg_wrap(W_, H_, "".join(s), "ángulo central AOB y ángulo inscrito AVB que abarcan el mismo arco"))


def circ_ang(*ks):
    t = pick(ks, ["fig", "fig", "ins", "cen", "arco", "semi", "suma"])
    c = R.choice(range(40, 161, 4))
    if t == "fig":
        ask = R.choice(["ins", "cen"])
        if ask == "ins":
            return M(circ_ang_svg(c) + "El ángulo central ∠AOB mide %d°. ¿Cuánto mide el ángulo inscrito ∠AVB?" % c, "%d°" % (c // 2), ["%d°" % c, "%d°" % (2 * c), "%d°" % (180 - c)],
                     "Un ángulo inscrito mide la <b>mitad</b> del central que abarca el mismo arco: <b>%d°</b>." % (c // 2))
        return M(circ_ang_svg(c) + "El ángulo inscrito ∠AVB mide %d°. ¿Cuánto mide el ángulo central ∠AOB?" % (c // 2), "%d°" % c, ["%d°" % (c // 2), "%d°" % (c // 4), "%d°" % (180 - c // 2)],
                 "El central mide el <b>doble</b> del inscrito: %d × 2 = <b>%d°</b>." % (c // 2, c))
    if t == "ins":
        return M("Un arco de una circunferencia mide %d°. ¿Cuánto mide un ángulo inscrito que abarca ese arco?" % c, "%d°" % (c // 2), ["%d°" % c, "%d°" % (2 * c), "%d°" % (360 - c)],
                 "El inscrito mide la mitad del arco: <b>%d°</b>." % (c // 2))
    if t == "cen":
        n = R.choice([3, 4, 5, 6, 8, 9, 10, 12])
        return M("Una circunferencia se divide en %d arcos iguales. ¿Cuánto mide el ángulo central de cada arco?" % n, "%d°" % (360 // n), ["%d°" % (180 // n) if 180 % n == 0 else "%d°" % (360 // n + 10), "%d°" % (360 - 360 // n), "%d°" % n],
                 "360° ÷ %d = <b>%d°</b>." % (n, 360 // n))
    if t == "arco":
        return M("El ángulo central ∠AOB mide %d°. ¿Cuánto mide el arco AB?" % c, "%d°" % c, ["%d°" % (c // 2), "%d°" % (2 * c), "%d°" % (180 - c)],
                 "El arco mide lo mismo que su ángulo central: <b>%d°</b>." % c)
    if t == "semi":
        return M("Un ángulo inscrito abarca un diámetro (media circunferencia). ¿Cuánto mide?", "90°", ["180°", "45°", "60°"],
                 "El arco es de 180° y el inscrito mide la mitad: <b>90°</b>.")
    a, b = R.randint(60, 150), R.randint(60, 150)
    rest = 360 - a - b
    if rest <= 20:
        return None
    return M("Una circunferencia tiene tres arcos: %d°, %d° y x. ¿Cuánto mide x?" % (a, b), "%d°" % rest, ["%d°" % (180 - (a + b) % 180), "%d°" % (a + b), "%d°" % (rest + 10)],
             "Toda la circunferencia mide 360°: 360 − %d − %d = <b>%d°</b>." % (a, b, rest))


# ============================================================ 2.º: distancias y desigualdad del triángulo
def distancias(*ks):
    t = pick(ks, ["rango", "rango", "tercer", "punto", "paral", "corto"])
    if t == "rango":
        a, b = R.randint(3, 15), R.randint(3, 15)
        lo, hi = abs(a - b), a + b
        return M("Dos lados de un triángulo miden %d cm y %d cm. ¿Entre qué valores debe estar el tercer lado?" % (a, b), "entre %d cm y %d cm" % (lo, hi),
                 ["entre 0 cm y %d cm" % hi, "entre %d cm y %d cm" % (min(a, b), max(a, b)), "entre %d cm y %d cm" % (lo, a * b)],
                 "Debe ser mayor que la diferencia (%d) y menor que la suma (%d): <b>entre %d y %d cm</b>." % (lo, hi, lo, hi))
    if t == "tercer":
        a, b = R.randint(4, 12), R.randint(4, 12)
        lo, hi = abs(a - b), a + b
        good = R.randint(lo + 1, hi - 1)
        bads = [hi, hi + R.randint(1, 5), lo if lo > 0 else hi + 6]
        return M("Dos lados de un triángulo miden %d cm y %d cm. ¿Cuál puede ser la medida del tercer lado?" % (a, b), "%d cm" % good, ["%d cm" % x for x in bads],
                 "Tiene que estar entre %d y %d cm (sin incluirlos): <b>%d cm</b>." % (lo, hi, good))
    if t == "punto":
        d = R.randint(3, 12)
        q = R.randint(d + 1, d + 9)
        return M("Desde un punto P, el segmento perpendicular a una recta mide %d cm y otro segmento inclinado mide %d cm. ¿Cuál es la distancia de P a la recta?" % (d, q), "%d cm" % d,
                 ["%d cm" % q, "%d cm" % (q - d), "%d cm" % (q + d)], "La distancia de un punto a una recta se mide sobre la <b>perpendicular</b>, que es el camino más corto: <b>%d cm</b>." % d)
    if t == "paral":
        d = R.randint(2, 15)
        return M("Dos rectas paralelas están separadas %d cm medidos sobre una perpendicular. Si mides sobre una recta inclinada, ¿qué obtienes?" % d, "una medida mayor que %d cm" % d,
                 ["exactamente %d cm" % d, "una medida menor que %d cm" % d, "0 cm"], "La distancia entre paralelas es la de la perpendicular; cualquier segmento inclinado es <b>más largo</b>.")
    a, b = R.randint(300, 900), R.randint(300, 900)
    c = R.randint(abs(a - b) + 50, a + b - 50)
    return M("Del punto A al B hay %d m en línea recta, de B a C %d m y de A a C %d m. ¿Qué camino de A a C es más corto?" % (a, b, c), "ir directo de A a C",
             ["pasar por B", "los dos miden igual", "no se puede saber"], "Por la desigualdad del triángulo, %d &lt; %d + %d = %d: <b>ir directo</b>." % (c, a, b, a + b))


# ============================================================ 2.º: gráficas poligonales, de línea e histogramas
MESES = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]


def line_svg(labels, vals, unit_, title):
    W_, H_, x0, y0, x1, y1 = 420, 230, 46, 196, 404, 20
    mx = max(vals)
    step = 5 if mx <= 40 else 10 if mx <= 80 else 20 if mx <= 160 else 50
    top = (mx // step + 1) * step
    Y = lambda v: y0 - (y0 - y1) * v / float(top)
    X = lambda i: x0 + 16 + i * (x1 - x0 - 32) / float(len(vals) - 1)
    s = [line(x0, y0, x1, y0, "#555", 1.5), line(x0, y0, x0, y1 - 4, "#555", 1.5)]
    for v in range(0, top + 1, step):
        s.append(line(x0, Y(v), x1, Y(v), "#ddd", 1))
        s.append(text(x0 - 6, Y(v) + 4, str(v), 11, anchor="end", weight=400))
    pts = " ".join("%.1f,%.1f" % (X(i), Y(v)) for i, v in enumerate(vals))
    s.append("<polyline points='%s' fill='none' stroke='#c0392b' stroke-width='2.5'/>" % pts)
    for i, v in enumerate(vals):
        s.append("<circle cx='%.1f' cy='%.1f' r='3.5' fill='#c0392b'/>" % (X(i), Y(v)))
        s.append(text(X(i), y0 + 16, labels[i], 11, weight=400))
    s.append(text(x0 + 4, 12, unit_, 11, anchor="start"))
    return "<svg data-pf='lg'" + svg_wrap(W_, H_, "".join(s), title)[4:]


def graf_linea(*ks):
    t = pick(ks, ["max", "dif", "sube", "prom", "lee"])
    n = R.choice([5, 6, 7])
    start = R.randint(0, 12 - n)
    labs = MESES[start:start + n]
    kind = R.choice([("Temperatura máxima promedio en Monterrey (°C)", 15, 38, "°C"), ("Lluvia en Villahermosa (mm)", 40, 150, "mm"), ("Visitantes a un museo (miles)", 10, 60, "miles"),
                     ("Ventas de una tienda (miles de pesos)", 20, 90, "miles de pesos")])
    vals = [R.randint(kind[1], kind[2]) for _ in range(n)]
    if len(set(vals)) < n:
        return None
    pic = fig(line_svg(labs, vals, kind[3], kind[0]))
    if t == "max":
        i = vals.index(max(vals))
        return M(pic + "%s. ¿En qué mes se registró el valor más alto?" % kind[0], labs[i], [labs[j] for j in R.sample([j for j in range(n) if j != i], 3)],
                 "El punto más alto de la gráfica está en <b>%s</b> (%d)." % (labs[i], vals[i]))
    if t == "dif":
        i, j = R.sample(range(n), 2)
        return M(pic + "%s. ¿Cuál es la diferencia entre %s y %s?" % (kind[0], labs[i], labs[j]), "%d %s" % (abs(vals[i] - vals[j]), kind[3]),
                 ["%d %s" % (vals[i] + vals[j], kind[3]), "%d %s" % (abs(vals[i] - vals[j]) + 5, kind[3]), "%d %s" % (max(vals[i], vals[j]), kind[3])],
                 "%d − %d = <b>%d</b>." % (max(vals[i], vals[j]), min(vals[i], vals[j]), abs(vals[i] - vals[j])))
    if t == "sube":
        ds = [vals[k + 1] - vals[k] for k in range(n - 1)]
        k = ds.index(max(ds))
        if ds[k] <= 0:
            return None
        return M(pic + "%s. ¿Entre qué dos meses hubo el mayor aumento?" % kind[0], "%s y %s" % (labs[k], labs[k + 1]),
                 ["%s y %s" % (labs[m], labs[m + 1]) for m in R.sample([m for m in range(n - 1) if m != k], min(3, n - 2))],
                 "El tramo que más sube es de %s a %s: <b>+%d</b>." % (labs[k], labs[k + 1], ds[k]))
    if t == "prom":
        tot = sum(vals)
        if tot % n:
            return None
        return M(pic + "%s. ¿Cuál es el promedio de los %d meses?" % (kind[0], n), "%d %s" % (tot // n, kind[3]), ["%d %s" % (tot, kind[3]), "%d %s" % ((max(vals) + min(vals)) // 2 + 1, kind[3]), "%d %s" % (tot // n + 3, kind[3])],
                 "Suma %d ÷ %d = <b>%d</b>." % (tot, n, tot // n))
    i = R.randrange(n)
    return M(pic + "%s. ¿Qué valor tuvo %s?" % (kind[0], labs[i]), "%d %s" % (vals[i], kind[3]), ["%d %s" % (vals[(i + 1) % n], kind[3]), "%d %s" % (vals[i] + 5, kind[3]), "%d %s" % (vals[i] - 5, kind[3])],
             "Leemos la altura del punto de %s: <b>%d</b>." % (labs[i], vals[i]))


def histo_svg(edges, freqs, title, unit_):
    W_, H_, x0, y0, x1, y1 = 420, 230, 46, 190, 404, 20
    mx = max(freqs)
    step = 2 if mx <= 12 else 5
    top = (mx // step + 1) * step
    Y = lambda v: y0 - (y0 - y1) * v / float(top)
    bw = (x1 - x0 - 20) / float(len(freqs))
    s = [line(x0, y0, x1, y0, "#555", 1.5), line(x0, y0, x0, y1 - 4, "#555", 1.5)]
    for v in range(0, top + 1, step):
        s.append(line(x0, Y(v), x1, Y(v), "#ddd", 1))
        s.append(text(x0 - 6, Y(v) + 4, str(v), 11, anchor="end", weight=400))
    for i, f in enumerate(freqs):
        xa = x0 + 10 + i * bw
        s.append("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' fill='#7fb3d5' stroke='#2b6cb0'/>" % (xa, Y(f), bw, y0 - Y(f)))
        s.append(text(xa, y0 + 15, str(edges[i]), 11, weight=400))
    s.append(text(x0 + 10 + len(freqs) * bw, y0 + 15, str(edges[-1]), 11, weight=400))
    s.append(text((x0 + x1) / 2.0, y0 + 34, unit_, 11, weight=400))
    return "<svg data-pf='lg'" + svg_wrap(W_, H_ + 14, "".join(s), title)[4:]


def histograma(*ks):
    t = pick(ks, ["clase", "tot", "mas", "menos", "porc"])
    kind = R.choice([("Estatura de los alumnos de un grupo", 140, 5, "estatura (cm)"), ("Tiempo de traslado a la escuela", 0, 10, "minutos"), ("Calificaciones de un examen (sobre 100)", 50, 10, "puntos"),
                     ("Peso de mochilas", 2, 1, "kg")])
    k = R.choice([4, 5])
    edges = [kind[1] + i * kind[2] for i in range(k + 1)]
    freqs = [R.randint(1, 12) for _ in range(k)]
    if len(set(freqs)) < k:
        return None
    pic = fig(histo_svg(edges, freqs, kind[0], kind[3]))
    cls = lambda i: "%d a %d" % (edges[i], edges[i + 1])
    if t == "clase":
        i = freqs.index(max(freqs))
        return M(pic + "%s. ¿Qué intervalo tiene más datos?" % kind[0], cls(i), [cls(j) for j in R.sample([j for j in range(k) if j != i], 3)],
                 "La barra más alta es la de <b>%s</b> (%d datos)." % (cls(i), freqs[i]))
    if t == "tot":
        return M(pic + "%s. ¿Cuántos datos hay en total?" % kind[0], str(sum(freqs)), [str(sum(freqs) - freqs[0]), str(max(freqs) * k), str(k)],
                 "Sumamos las alturas: %s = <b>%d</b>." % (" + ".join(map(str, freqs)), sum(freqs)))
    if t == "mas":
        i = R.randrange(1, k)
        v = sum(freqs[i:])
        return M(pic + "%s. ¿Cuántos datos son de %d o más?" % (kind[0], edges[i]), str(v), [str(freqs[i]), str(sum(freqs[:i])), str(v + 1)],
                 "Sumamos las barras desde %d: <b>%d</b>." % (edges[i], v))
    if t == "menos":
        i = R.randrange(1, k)
        v = sum(freqs[:i])
        return M(pic + "%s. ¿Cuántos datos son menores que %d?" % (kind[0], edges[i]), str(v), [str(freqs[i - 1]), str(sum(freqs[i:])), str(v + 2)],
                 "Sumamos las barras antes de %d: <b>%d</b>." % (edges[i], v))
    tot = sum(freqs)
    i = freqs.index(max(freqs))
    p = F(freqs[i] * 100, tot)
    if p.denominator not in (1, 2, 4, 5, 10):
        return None
    return M(pic + "%s. ¿Qué porcentaje de los datos está en el intervalo %s?" % (kind[0], cls(i)), "%s %%" % dexact(p), ["%d %%" % freqs[i], "%s %%" % dexact(p / 2), "%s %%" % dexact(100 - p)],
             "%d de %d = %d ÷ %d × 100 = <b>%s %%</b>." % (freqs[i], tot, freqs[i], tot, dexact(p)))


# ============================================================ 2.º: probabilidad: complementarios, mutuamente excluyentes, formas
def prob2(*ks):
    t = pick(ks, ["comp", "excl", "excl", "formas", "no_excl"])
    if t == "comp":
        p = R.choice([F(1, 4), F(2, 5), F(3, 10), F(1, 5), F(5, 8), F(7, 20), F(3, 25)])
        form = R.choice(["frac", "dec", "pct"])
        sh = lambda x: fq(x) if form == "frac" else dexact(x) if form == "dec" else dexact(x * 100) + " %"
        ev = R.choice(["que llueva mañana", "que un foco salga defectuoso", "ganar una rifa", "que el camión llegue tarde"])
        return M("La probabilidad de %s es %s. ¿Cuál es la probabilidad de que NO ocurra?" % (ev, sh(p)), sh(1 - p), [sh(p), sh(1 - p / 2), sh(p / 2)],
                 "Los eventos complementarios suman 1: 1 − %s = <b>%s</b>." % (sh(p), sh(1 - p)))
    if t == "excl":
        cs = R.sample(["rojas", "azules", "verdes", "amarillas", "blancas"], 3)
        ns = [R.randint(2, 9) for _ in range(3)]
        tot = sum(ns)
        p = F(ns[0] + ns[1], tot)
        return M("Una bolsa tiene %d canicas %s, %d %s y %d %s. ¿Cuál es la probabilidad de sacar una %s o una %s?" % (ns[0], cs[0], ns[1], cs[1], ns[2], cs[2], cs[0][:-1].replace("azule", "azul"), cs[1][:-1].replace("azule", "azul")),
                 fq(p), [fq(F(ns[0] * ns[1], tot * tot)), fq(F(ns[0], tot)), fq(F(ns[2], tot)) if F(ns[2], tot) != p else fq(1 - p + F(1, tot))],
                 "Son eventos mutuamente excluyentes: se suman. %s + %s = <b>%s</b>." % (fq(F(ns[0], tot)), fq(F(ns[1], tot)), fq(p)))
    if t == "no_excl":
        q = R.choice([("Al lanzar un dado: «sacar un número par» y «sacar un 4»", "no: el 4 cumple los dos"), ("Al lanzar un dado: «sacar un 1» y «sacar un 6»", "sí: no pueden ocurrir a la vez"),
                      ("Al sacar una carta: «que sea roja» y «que sea un as»", "no: hay ases rojos"), ("Al lanzar una moneda: «águila» y «sol»", "sí: no pueden ocurrir a la vez"),
                      ("Al lanzar un dado: «número menor que 3» y «número mayor que 4»", "sí: no pueden ocurrir a la vez"), ("Al lanzar un dado: «número primo» y «número par»", "no: el 2 cumple los dos")])
        return M("¿Son eventos mutuamente excluyentes? %s." % q[0], q[1], [x for x in ["no: el 4 cumple los dos", "sí: no pueden ocurrir a la vez", "no: hay ases rojos", "no: el 2 cumple los dos", "sí: siempre lo son"] if x != q[1]][:3],
                 "Son mutuamente excluyentes si no pueden ocurrir al mismo tiempo: <b>%s</b>." % q[1])
    p = R.choice([F(1, 4), F(3, 4), F(1, 5), F(2, 5), F(1, 8), F(3, 20), F(9, 10), F(1, 2), F(7, 25)])
    src_, dst = R.sample(["frac", "dec", "pct"], 2)
    sh = {"frac": lambda x: fq(x), "dec": lambda x: dexact(x), "pct": lambda x: dexact(x * 100) + " %"}
    nm = {"frac": "fracción", "dec": "número decimal", "pct": "porcentaje"}
    return M("Escribe la probabilidad %s como %s." % (sh[src_](p), nm[dst]), sh[dst](p), [sh[dst](p / 10), sh[dst](1 - p), sh[dst](p * 10) if p * 10 <= 1 else sh[dst](p / 2)],
             "%s = %s = %s: <b>%s</b>." % (fq(p), dexact(p), dexact(p * 100) + " %", sh[dst](p)))


# ============================================================ 3.º: jerarquía de operaciones con signos y potencias
def jerarquia(*ks):
    t = pick(ks, ["a", "a", "b", "c", "d"])
    a, b, c, d = nz(-9, 9), nz(-6, 6), nz(-6, 6), nz(2, 5)
    P = lambda v: "(%s)" % sg(v) if v < 0 else sg(v)
    if t == "a":
        r = a + b * c
        return M("Calcula: %s + %s × %s" % (sg(a), P(b), P(c)), sg(r), [sg((a + b) * c), sg(a - b * c), sg(-r) if r else "1"], "Primero la multiplicación: %s × %s = %s; luego %s + %s = <b>%s</b>." % (sg(b), P(c), sg(b * c), sg(a), P(b * c), sg(r)))
    if t == "b":
        e = R.choice([2, 3])
        r = a - b ** e
        return M("Calcula: %s − %s<sup>%d</sup>" % (sg(a), P(b), e), sg(r), [sg(a + b ** e) if b ** e != 0 else "1", sg((a - b) ** e), sg(a - b * e)],
                 "Primero la potencia: %s<sup>%d</sup> = %s; luego %s − %s = <b>%s</b>." % (P(b), e, sg(b ** e), sg(a), P(b ** e), sg(r)))
    if t == "c":
        k = R.choice([2, 3, 4, 5])
        x = nz(-8, 8)
        r = (a + b) * k - x
        return M("Calcula: [%s + %s] × %d − %s" % (sg(a), P(b), k, P(x)), sg(r), [sg(a + b * k - x), sg((a + b) * (k - x)), sg(r + 2 * x)],
                 "Primero el corchete: %s; × %d = %s; − %s = <b>%s</b>." % (sg(a + b), k, sg((a + b) * k), P(x), sg(r)))
    q = b * c
    m = nz(-5, 5)
    r = q * m // m if False else None
    p = nz(-9, 9)
    r = (q * d) // b if q * d % b == 0 else None
    if r is None:
        return None
    return M("Calcula: %s × %d ÷ %s + %s" % (sg(q), d, P(b), P(p)), sg(r + p), [sg(q * d // (b + p)) if (b + p) and q * d % (b + p) == 0 else sg(r - p), sg(-(r + p)) if r + p else "2", sg(r + p + 1)],
             "Multiplicación y división de izquierda a derecha: %s × %d = %s; ÷ %s = %s; + %s = <b>%s</b>." % (sg(q), d, sg(q * d), P(b), sg(r), P(p), sg(r + p)))


# ============================================================ 3.º: sucesiones cuadráticas
def seq_cuad(*ks):
    t = pick(ks, ["sig", "sig", "gen", "term", "fig", "dif2"])
    a = R.choice([1, 1, 2, 3])
    b = R.randint(-3, 4)
    c = R.randint(-4, 6)
    f = lambda n: a * n * n + b * n + c
    xs = [f(n) for n in range(1, 6)]
    if t == "sig":
        d1 = [y - x for x, y in zip(xs, xs[1:])]
        return M("¿Cuál es el siguiente término? %s; …" % "; ".join(sg(v) for v in xs[:4]), sg(xs[4]), [sg(xs[3] + d1[2]), sg(xs[4] + 2 * a), sg(xs[4] - 1)],
                 "Diferencias: %s (aumentan de %d en %d). La siguiente diferencia es %s: %s + %s = <b>%s</b>." % (", ".join(sg(d) for d in d1[:3]), 2 * a, 2 * a, sg(d1[3]), sg(xs[3]), sg(d1[3]), sg(xs[4])))
    if t == "gen":
        ok = quad(a, b, c, "n")
        return M("¿Cuál es la regla general de %s; …?" % "; ".join(sg(v) for v in xs[:4]), ok, [quad(a, b + 1, c - 1, "n") if (a, b + 1, c - 1) != (a, b, c) else quad(a + 1, b, c, "n"), lin(xs[1] - xs[0], xs[0] - (xs[1] - xs[0]), "n"), quad(a, c, b, "n") if b != c else quad(a, b, c + 2, "n")],
                 "La segunda diferencia es %d, así que empieza con %s. Comprobamos n = 1: %s. Regla: <b>%s</b>." % (2 * a, quad(a, 0, 0, "n"), sg(xs[0]), ok))
    if t == "term":
        n = R.choice([8, 10, 12, 15, 20])
        return M("La regla de una sucesión es %s. ¿Cuál es el término %d?" % (quad(a, b, c, "n"), n), sg(f(n)), [sg(a * 2 * n + b * n + c), sg(f(n - 1)), sg(f(n) + 1)],
                 "Sustituimos n = %d: %s = <b>%s</b>." % (n, quad(a, b, c, "n").replace("n", "(%d)" % n), sg(f(n))))
    if t == "fig":
        k = R.choice([0, 1, 2, 3])
        n = R.choice([6, 8, 10, 12, 15])
        return M("Con cuadritos se forman cuadrados: la figura 1 tiene 1×1, la 2 tiene 2×2, la 3 tiene 3×3%s. ¿Cuántos cuadritos tiene la figura %d?" % ((", y a cada una se le agrega%s %d cuadrito%s suelto%s" % ("n" if k > 1 else "", k, "s" if k > 1 else "", "s" if k > 1 else "")) if k else "", n),
                 str(n * n + k), [str(2 * n + k), str(n * n + k + 2 * n), str((n - 1) ** 2 + k)], "Regla: %s. Figura %d: <b>%d</b>." % (quad(1, 0, k, "n"), n, n * n + k))
    return M("En la sucesión %s; …, ¿cuál es la segunda diferencia?" % "; ".join(sg(v) for v in xs[:5]), str(2 * a), [str(a), str(xs[1] - xs[0]), "0"],
             "Primeras diferencias: %s. Sus diferencias son siempre <b>%d</b> (sucesión cuadrática)." % (", ".join(sg(y - x) for x, y in zip(xs, xs[1:])), 2 * a))


# ============================================================ 3.º: áreas y volúmenes con expresiones; despejar
def alg_vol(*ks):
    t = pick(ks, ["vol", "vol", "desp", "desp", "area"])
    if t == "vol" and R.random() < .6:
        def pm(p, q):
            o = [0] * (len(p) + len(q) - 1)
            for i, x in enumerate(p):
                for j, y in enumerate(q):
                    o[i + j] += x * y
            return o
        dims = R.choice([[(1, 0), (1, 0), (0, R.randint(2, 9))], [(1, 0), (1, R.randint(1, 6)), (0, R.randint(2, 6))], [(2, 0), (1, 0), (1, R.randint(1, 5))],
                         [(1, 0), (1, R.randint(1, 4)), (1, R.randint(1, 4))], [(R.randint(2, 4), 0), (1, 0), (0, R.randint(2, 9))]])
        poly = [1]
        for a_, b_ in dims:
            poly = pm(poly, [b_, a_])
        while len(poly) > 1 and poly[-1] == 0:
            poly.pop()
        def ps(c):
            terms = []
            for e in range(len(c) - 1, -1, -1):
                k = c[e]
                if not k:
                    continue
                v = "" if e == 0 else "x" if e == 1 else "x²" if e == 2 else "x³"
                terms.append((num(k) if k != 1 or e == 0 else "") + v)
            return " + ".join(terms)
        ds = [lin(a_, b_) for a_, b_ in dims]
        ok = ps(poly)
        alt1 = ps([c * 2 if i == len(poly) - 1 else c for i, c in enumerate(poly)])
        sm = [0, 0]
        for a_, b_ in dims:
            sm[0] += b_
            sm[1] += a_
        alt2 = ps(sm)
        alt3 = ps(poly[:1] + [x + 1 for x in poly[1:]]) if len(poly) > 1 else ok + "x"
        return M("Un prisma rectangular mide %s de largo, %s de ancho y %s de alto. ¿Qué expresión da su volumen?" % tuple("(%s)" % d if "+" in d else d for d in ds), ok, [alt2, alt3, alt1],
                 "V = largo × ancho × alto = %s = <b>%s</b>." % (" · ".join("(%s)" % d if "+" in d else d for d in ds), ok))
    if t == "vol":
        a, b = R.randint(1, 5), R.randint(1, 6)
        kind = R.choice(["cubo", "prisma", "prisma2"])
        if kind == "cubo":
            return M("Un cubo tiene aristas de %s cm. ¿Qué expresión da su volumen?" % lin(a, 0), "%sx³" % (num(a ** 3) if a > 1 else ""), ["%sx²" % (num(a * a) if a > 1 else ""), "%sx³" % (num(3 * a)), "%sx" % num(12 * a)],
                     "V = (%s)³ = <b>%sx³</b>." % (lin(a, 0), num(a ** 3) if a > 1 else ""))
        if kind == "prisma":
            return M("Un prisma rectangular mide x de largo, x de ancho y %d de alto. ¿Qué expresión da su volumen?" % b, quad(b, 0, 0), [lin(2, b), quad(1, b, 0), ("%dx³" % b) if b > 1 else "x³"],
                     "V = x · x · %d = <b>%s</b>." % (b, quad(b, 0, 0)))
        kx = "x²" if b == 1 else "%dx²" % b
        return M("Un prisma rectangular mide x de largo, x de ancho y (x + %d) de alto. ¿Qué expresión da su volumen?" % b, "x³ + " + kx, ["x³ + %d" % b, "x² + %sx" % ("" if b == 1 else b), "3x + %d" % b],
                 "V = x · x · (x + %d) = <b>x³ + %s</b>." % (b, kx))
    if t == "desp":
        q = R.choice([("A = b · h", "h", "h = A ÷ b", ["h = A · b", "h = b ÷ A", "h = A − b"]), ("A = b · h ÷ 2", "h", "h = 2A ÷ b", ["h = A ÷ 2b", "h = 2b ÷ A", "h = A · b ÷ 2"]),
                      ("P = 2a + 2b", "a", "a = (P − 2b) ÷ 2", ["a = P − 2b", "a = (P + 2b) ÷ 2", "a = P ÷ 2b"]), ("V = l · a · h", "h", "h = V ÷ (l · a)", ["h = V · l · a", "h = V − l − a", "h = l · a ÷ V"]),
                      ("d = v · t", "t", "t = d ÷ v", ["t = d · v", "t = v ÷ d", "t = d − v"]), ("V = π r² h", "h", "h = V ÷ (π r²)", ["h = V · π r²", "h = π r² ÷ V", "h = V − π r²"]),
                      ("C = 5(F − 32) ÷ 9", "F", "F = 9C ÷ 5 + 32", ["F = 5C ÷ 9 + 32", "F = 9C ÷ 5 − 32", "F = 9(C − 32) ÷ 5"]), ("A = π r²", "r", "r = √(A ÷ π)", ["r = A ÷ π", "r = √A ÷ π²", "r = A ÷ 2π"])])
        return M("Despeja %s en la fórmula %s." % (q[1], q[0]), q[2], q[3], "Hacemos la operación inversa en los dos lados: <b>%s</b>." % q[2])
    q = R.choice([("A = b · h", "b = 12 y A = 84", "h = 7"), ("V = l · a · h", "l = 5, a = 4 y V = 120", "h = 6"), ("d = v · t", "v = 80 y d = 360", "t = 4.5"),
                  ("P = 2a + 2b", "P = 46 y b = 9", "a = 14"), ("A = b · h ÷ 2", "b = 10 y A = 35", "h = 7"), ("C = 5(F − 32) ÷ 9", "C = 25", "F = 77")])
    import re as _re
    var, val = q[2].split(" = ")
    v = float(val)
    return M("En la fórmula %s, con %s, ¿cuánto vale %s?" % (q[0], q[1], var), q[2], ["%s = %s" % (var, dec(v * 2)), "%s = %s" % (var, dec(v + 3)), "%s = %s" % (var, dec(v / 2))],
             "Sustituimos los datos y despejamos: <b>%s</b>." % q[2])


# ============================================================ 3.º: reparto proporcional
def reparto(*ks):
    t = pick(ks, ["dir", "dir", "tres", "inv"])
    if t == "dir":
        a, b = R.randint(2, 9), R.randint(2, 9)
        if a == b:
            return None
        u = R.choice([50, 100, 150, 200, 250])
        tot = (a + b) * u
        n1, n2 = K.next()[0], K.next()[0]
        ctx = R.choice(["Para comprar un regalo, %s puso %s y %s puso %s. Les sobraron %s y se los reparten en proporción a lo que pusieron. ¿Cuánto le toca a %s?",
                        "%s trabajó %d horas y %s %d horas. Les pagan %s en total y se reparte en proporción a las horas. ¿Cuánto recibe %s?"])
        if ctx.startswith("Para"):
            q = ctx % (n1, peso(a * 1000), n2, peso(b * 1000), peso(tot * 100), n1)
        else:
            q = ctx % (n1, a, n2, b, peso(tot * 100), n1)
        return M(q, peso(a * u * 100), [peso(tot // 2 * 100), peso(b * u * 100), peso(tot * a // 10 * 10)],
                 "Hay %d partes en total; cada parte vale %s ÷ %d = %s. %s recibe %d partes: <b>%s</b>." % (a + b, peso(tot * 100), a + b, peso(u * 100), n1, a, peso(a * u * 100)))
    if t == "tres":
        r = R.sample(range(1, 8), 3)
        u = R.choice([100, 200, 300, 500])
        tot = sum(r) * u
        return M("Se reparten %s entre tres personas en la razón %d : %d : %d. ¿Cuánto le toca a la que recibe más?" % (peso(tot * 100), r[0], r[1], r[2]), peso(max(r) * u * 100),
                 [peso(tot // 3 * 100), peso(min(r) * u * 100), peso((max(r) + 1) * u * 100)], "%d partes; cada parte %s. La mayor: %d × %s = <b>%s</b>." % (sum(r), peso(u * 100), max(r), peso(u * 100), peso(max(r) * u * 100)))
    a, b = R.choice([(2, 3), (1, 2), (3, 6), (2, 6), (4, 6), (1, 3)])
    u = R.choice([60, 120, 180, 240])
    pa, pb = F(1, a), F(1, b)
    tot = u * 10
    sa = tot * pa / (pa + pb)
    if sa.denominator != 1:
        return None
    n1, n2 = K.next()[0], K.next()[0]
    return M("Un premio de %s se reparte en forma inversamente proporcional a las faltas: %s tiene %d y %s tiene %d. ¿Cuánto recibe %s?" % (peso(tot * 100), n1, a, n2, b, n1), peso(int(sa) * 100),
             [peso(int(tot - sa) * 100), peso(tot // 2 * 100), peso(int(tot * a / (a + b)) * 100), peso((int(sa) + u) * 100), peso((int(sa) - u) * 100)], "Inversa: se reparte en proporción a 1/%d y 1/%d. %s recibe <b>%s</b>." % (a, b, n1, peso(int(sa) * 100)))


# ============================================================ 3.º: variación lineal, cuadrática e inversa
def variacion(*ks):
    t = pick(ks, ["tipo", "tipo", "val", "tab"])
    if t == "tipo":
        kind = R.choice(["lin", "cuad", "inv"])
        xs = [1, 2, 3, 4, 5]
        if kind == "lin":
            m, b = nz(-5, 6), R.randint(-5, 9)
            ys = [m * x + b for x in xs]
        elif kind == "cuad":
            a, c = R.choice([1, 2, 3]), R.randint(-3, 5)
            ys = [a * x * x + c for x in xs]
        else:
            k = 60
            ys = [k // x if k % x == 0 else None for x in xs]
            xs = [1, 2, 3, 4, 5]
        t_ = tabla_html(["x"] + [str(v) for v in xs], [["y"] + [sg(v) for v in ys]])
        ok = {"lin": "lineal", "cuad": "cuadrática", "inv": "de proporcionalidad inversa"}[kind]
        return M(t_ + "¿Qué tipo de variación muestra la tabla?", ok, [x for x in ["lineal", "cuadrática", "de proporcionalidad inversa", "no hay relación"] if x != ok],
                 {"lin": "Las diferencias de y son constantes: <b>lineal</b>.", "cuad": "Las segundas diferencias de y son constantes: <b>cuadrática</b>.", "inv": "x × y = 60 siempre: <b>proporcionalidad inversa</b>."}[kind])
    if t == "val":
        a, b, c = R.choice([1, -1, 2]), R.randint(-4, 4), R.randint(-6, 6)
        x = nz(-4, 4)
        v = a * x * x + b * x + c
        return M("Si y = %s, ¿cuánto vale y cuando x = %s?" % (quad(a, b, c), sg(x)), sg(v), [sg(-a * x * x + b * x + c), sg(a * 2 * x + b * x + c), sg(v + 1)],
                 "Sustituimos: %s = <b>%s</b> (recuerda que (%s)² = %d)." % (quad(a, b, c).replace("x", "(%s)" % sg(x)), sg(v), sg(x), x * x))
    a = R.choice([1, 2, 3, 4, 5])
    xs = [1, 2, 3, 4]
    t_ = tabla_html(["Lado del cuadrado (cm)"] + [str(v * a) for v in xs], [["Área (cm²)"] + [str((v * a) ** 2) for v in xs]])
    return M(t_ + "Si el lado se duplica, ¿qué le pasa al área?", "se multiplica por 4", ["se duplica", "aumenta 2 cm²", "se multiplica por 8"],
             "El área es lado²: al duplicar el lado, el área se multiplica por 2² = <b>4</b>. La variación es cuadrática, no lineal.")


# ============================================================ 3.º: polígonos regulares y teselados
PN = {3: "triángulo equilátero", 4: "cuadrado", 5: "pentágono regular", 6: "hexágono regular", 8: "octágono regular", 9: "eneágono regular", 10: "decágono regular", 12: "dodecágono regular"}


def poligonos(*ks):
    t = pick(ks, ["int", "int", "cen", "ext", "lados", "tesel", "const", "suma", "diag", "perim"])
    n = R.choice(list(PN))
    if t == "suma":
        m = R.randint(5, 20)
        return M("¿Cuánto suman los ángulos interiores de un polígono de %d lados?" % m, "%s°" % num(180 * (m - 2)), ["%s°" % num(180 * m), "%s°" % num(360 * (m - 2)), "%s°" % num(180 * (m - 1))],
                 "180° × (%d − 2) = <b>%s°</b>." % (m, num(180 * (m - 2))))
    if t == "diag":
        m = R.randint(4, 20)
        return M("¿Cuántas diagonales tiene un polígono de %d lados?" % m, str(m * (m - 3) // 2), [str(m * (m - 3)), str(m - 3), str(m * (m - 1) // 2)],
                 "Desde cada vértice salen %d − 3 = %d diagonales; n(n − 3) ÷ 2 = <b>%d</b>." % (m, m - 3, m * (m - 3) // 2))
    if t == "perim":
        l = R.choice([2.5, 3, 4, 4.5, 5, 6, 7.5, 8, 9, 12])
        if R.random() < .5:
            return M("Un %s tiene lados de %s cm. ¿Cuál es su perímetro?" % (PN[n], dec(l)), "%s cm" % dec(l * n), ["%s cm" % dec(l * (n - 1)), "%s cm" % dec(l * 4), "%s cm" % dec(l + n)],
                     "%d lados iguales: %d × %s = <b>%s cm</b>." % (n, n, dec(l), dec(l * n)))
        return M("Un %s tiene un perímetro de %s cm. ¿Cuánto mide cada lado?" % (PN[n], dec(l * n)), "%s cm" % dec(l), ["%s cm" % dec(l * n / 4.0), "%s cm" % dec(l * 2), "%s cm" % dec(l * n - n)],
                 "%s ÷ %d = <b>%s cm</b>." % (dec(l * n), n, dec(l)))
    if t == "int":
        v = F(180 * (n - 2), n)
        return M("¿Cuánto mide cada ángulo interior de un %s?" % PN[n], "%s°" % fq(v), ["%s°" % num(180 * (n - 2)), "%s°" % fq(F(360, n)), "%d°" % (180 - n)],
                 "Suma de interiores: 180 × (%d − 2) = %d°. Entre %d: <b>%s°</b>." % (n, 180 * (n - 2), n, fq(v)))
    if t == "cen":
        return M("¿Cuánto mide el ángulo central de un %s?" % PN[n], "%s°" % fq(F(360, n)), ["%s°" % fq(F(180 * (n - 2), n)), "%s°" % fq(F(180, n)), "%d°" % (360 - n)],
                 "360° ÷ %d = <b>%s°</b>." % (n, fq(F(360, n))))
    if t == "ext":
        return M("¿Cuánto suman los ángulos exteriores de un %s?" % PN[n] if R.random() < .3 else "¿Cuánto mide cada ángulo exterior de un %s?" % PN[n],
                 "%s°" % fq(F(360, n)), ["%s°" % fq(F(180 * (n - 2), n)), "%s°" % num(180 * (n - 2)), "%d°" % (180 - 360 // n) if 360 % n == 0 and 180 - 360 // n > 0 else "90°"], "Los exteriores suman 360°: 360 ÷ %d = <b>%s°</b>." % (n, fq(F(360, n))))
    if t == "lados":
        return M("Cada ángulo interior de un polígono regular mide %s°. ¿Cuántos lados tiene?" % fq(F(180 * (n - 2), n)), str(n), [str(n + 1), str(n - 1), str(2 * n)],
                 "Cada exterior mide 180 − %s = %s°; 360 ÷ %s = <b>%d</b> lados." % (fq(F(180 * (n - 2), n)), fq(F(360, n)), fq(F(360, n)), n))
    if t == "tesel":
        q = R.choice([("¿Con cuál de estos polígonos regulares iguales se puede cubrir un piso sin huecos?", "hexágonos regulares", ["pentágonos regulares", "octágonos regulares", "decágonos regulares"]),
                      ("¿Con cuál de estos polígonos regulares iguales NO se puede cubrir un piso sin huecos?", "pentágonos regulares", ["triángulos equiláteros", "cuadrados", "hexágonos regulares"]),
                      ("¿Cuántos hexágonos regulares se juntan en cada vértice de un teselado?", "3", ["4", "6", "2"]), ("¿Cuántos triángulos equiláteros se juntan en cada vértice de un teselado?", "6", ["3", "4", "8"]),
                      ("¿Cuántos cuadrados se juntan en cada vértice de un teselado?", "4", ["3", "6", "2"]),
                      ("En un teselado con octágonos regulares y cuadrados, ¿cuánto suman 2 octágonos y 1 cuadrado en un vértice?", "360°", ["270°", "315°", "405°"])])
        return M(q[0], q[1], q[2], "Para cubrir sin huecos, los ángulos que se juntan en un vértice deben sumar 360°: <b>%s</b>." % q[1])
    return M("Para construir un %s con compás, se traza una circunferencia y se dividen 360° en partes iguales. ¿Qué ángulo central se usa?" % PN[n], "%s°" % fq(F(360, n)),
             ["%s°" % fq(F(180 * (n - 2), n)), "%s°" % fq(F(180, n)), "%d°" % n], "Se marcan ángulos centrales de 360 ÷ %d = <b>%s°</b> y se unen los puntos." % (n, fq(F(360, n))))


# ============================================================ 3.º: sólidos de revolución y desarrollos planos
def solidos(*ks):
    t = pick(ks, ["rev", "rev", "red", "net", "net", "cil"])
    if t in ("rev",):
        q = R.choice([("un rectángulo sobre uno de sus lados", "un cilindro"), ("un triángulo rectángulo sobre uno de sus catetos", "un cono"), ("un semicírculo sobre su diámetro", "una esfera"),
                      ("un trapecio rectángulo sobre su lado perpendicular a las bases", "un cono truncado"), ("un cuadrado sobre uno de sus lados", "un cilindro"),
                      ("un círculo sobre una recta exterior a él", "un toro (dona)")])
        return M("¿Qué sólido se forma al girar %s?" % q[0], q[1], [x for x in ["un cilindro", "un cono", "una esfera", "un cono truncado", "un prisma"] if x != q[1]][:3], "Se forma <b>%s</b>." % q[1])
    if t == "red":
        r, h = R.randint(2, 9), R.randint(3, 15)
        return M("Un rectángulo de %d cm × %d cm gira sobre su lado de %d cm. ¿Qué radio y altura tiene el cilindro que se forma?" % (r, h, h), "radio %d cm, altura %d cm" % (r, h),
                 ["radio %d cm, altura %d cm" % (h, r), "radio %s cm, altura %d cm" % (dec(r / 2.0), h), "radio %d cm, altura %d cm" % (r * 2, h)],
                 "El lado sobre el que gira es la altura (%d cm); el otro lado es el radio: <b>radio %d cm, altura %d cm</b>." % (h, r, h))
    if t == "net":
        q = R.choice([("un cilindro", "un rectángulo y dos círculos"), ("un cono", "un sector circular y un círculo"), ("una pirámide cuadrangular", "un cuadrado y cuatro triángulos"),
                      ("un prisma triangular", "dos triángulos y tres rectángulos"), ("un cubo", "seis cuadrados"), ("un prisma hexagonal", "dos hexágonos y seis rectángulos"),
                      ("una pirámide pentagonal", "un pentágono y cinco triángulos")])
        return M("¿Qué figuras forman el desarrollo plano de %s?" % q[0], q[1], [x for x in ["un rectángulo y dos círculos", "un sector circular y un círculo", "un cuadrado y cuatro triángulos", "dos triángulos y tres rectángulos", "seis cuadrados", "dos hexágonos y seis rectángulos", "un pentágono y cinco triángulos"] if x != q[1]][:3],
                 "El desarrollo de %s es <b>%s</b>." % (q[0], q[1]))
    r = R.choice([2, 3, 4, 5, 6, 7, 10])
    h = R.randint(5, 20)
    L = 2 * 3.14 * r
    return M("En el desarrollo plano de un cilindro de radio %d cm y altura %d cm, ¿cuánto mide el largo del rectángulo? (π ≈ 3.14)" % (r, h), "%s cm" % dec(round(L, 2)),
             ["%d cm" % h, "%s cm" % dec(round(3.14 * r, 2)), "%s cm" % dec(round(3.14 * r * r, 2))], "El rectángulo da la vuelta al círculo: largo = 2πr = 2 × 3.14 × %d = <b>%s cm</b>." % (r, dec(round(L, 2))))


# ============================================================ 3.º: esfera, cono y cilindro
def esfera(*ks):
    t = pick(ks, ["rel", "rel", "vcil", "vcono", "vesf", "aesf"])
    r = R.choice([1, 2, 3, 4, 5, 6, 10])
    if t == "rel":
        v = R.choice([90, 120, 150, 180, 240, 300, 360, 450, 600, 750, 900, 1200])
        q = R.choice([("Un cilindro tiene %d cm³ de volumen. ¿Cuál es el volumen de un cono con la misma base y la misma altura?" % v, "%d cm³" % (v // 3), ["%d cm³" % (v // 2), "%d cm³" % v, "%s cm³" % num(3 * v)], "El cono es 1/3 del cilindro"),
                      ("Un cono tiene %d cm³ de volumen. ¿Cuál es el volumen del cilindro con la misma base y altura?" % (v // 3), "%d cm³" % v, ["%d cm³" % (v // 3 * 2), "%d cm³" % (v // 3 * 4), "%d cm³" % (v // 6)], "El cilindro es 3 veces el cono"),
                      ("Una esfera cabe exacta en un cilindro (mismo radio y altura igual al diámetro) de %d cm³. ¿Cuál es el volumen de la esfera?" % v, "%d cm³" % (2 * v // 3), ["%d cm³" % (v // 3), "%d cm³" % (v // 2), "%d cm³" % v], "La esfera es 2/3 del cilindro")])
        return M(q[0], q[1], q[2], "%s: <b>%s</b>." % (q[3], q[1]))
    h = R.choice([3, 4, 5, 6, 9, 10, 12])
    if t == "vcil":
        v = 3.14 * r * r * h
        return M("¿Cuál es el volumen de un cilindro de radio %d cm y altura %d cm? (π ≈ 3.14)" % (r, h), "%s cm³" % dec(round(v, 2)), ["%s cm³" % dec(round(v / 3, 2)), "%s cm³" % dec(round(3.14 * 2 * r * h, 2)), "%s cm³" % dec(round(3.14 * r * h, 2))],
                 "V = π r² h = 3.14 × %d × %d = <b>%s cm³</b>." % (r * r, h, dec(round(v, 2))))
    if t == "vcono":
        if (r * r * h) % 3:
            return None
        v = 3.14 * r * r * h / 3
        return M("¿Cuál es el volumen de un cono de radio %d cm y altura %d cm? (π ≈ 3.14)" % (r, h), "%s cm³" % dec(round(v, 2)), ["%s cm³" % dec(round(v * 3, 2)), "%s cm³" % dec(round(v / 2, 2)), "%s cm³" % dec(round(3.14 * r * h / 3, 2))],
                 "V = π r² h ÷ 3 = 3.14 × %d × %d ÷ 3 = <b>%s cm³</b>." % (r * r, h, dec(round(v, 2))))
    if t == "vesf":
        r = R.randint(1, 25)
        v = 4 * 3.14 * r ** 3 / 3
        return M("¿Cuál es el volumen de una esfera de radio %d cm? (π ≈ 3.14)" % r, "%s cm³" % dec(round(v, 2)), ["%s cm³" % dec(round(4 * 3.14 * r * r, 2)), "%s cm³" % dec(round(3.14 * r ** 3, 2)), "%s cm³" % dec(round(v / 2, 2))],
                 "V = 4/3 π r³ = 4 × 3.14 × %d ÷ 3 = <b>%s cm³</b>." % (r ** 3, dec(round(v, 2))))
    r = R.randint(1, 20)
    a = 4 * 3.14 * r * r
    return M("¿Cuál es el área de la superficie de una esfera de radio %d cm? (π ≈ 3.14)" % r, "%s cm²" % dec(round(a, 2)), ["%s cm²" % dec(round(3.14 * r * r, 2)), "%s cm²" % dec(round(2 * 3.14 * r, 2)), "%s cm²" % dec(round(4 * 3.14 * r ** 3 / 3, 2))],
             "A = 4 π r² = 4 × 3.14 × %d = <b>%s cm²</b>." % (r * r, dec(round(a, 2))))


# ============================================================ 3.º: figuras compuestas con círculos
def compuestas(*ks):
    t = pick(ks, ["cuad_circ", "circ_cuad", "semi", "corona", "rect_semi"])
    if t == "cuad_circ":
        l = R.choice(range(2, 41, 2))
        a = l * l - 3.14 * (l / 2.0) ** 2
        return M("Un círculo está dentro de un cuadrado de %d cm de lado y toca sus cuatro lados. ¿Cuál es el área de la parte del cuadrado que no cubre el círculo? (π ≈ 3.14)" % l, "%s cm²" % dec(round(a, 2)),
                 ["%s cm²" % dec(round(l * l - 3.14 * l * l, 2)) if l * l - 3.14 * l * l > 0 else "%s cm²" % dec(round(3.14 * (l / 2.0) ** 2, 2)), "%d cm²" % (l * l), "%s cm²" % dec(round(l * l - 3.14 * l, 2))],
                 "Cuadrado %d − círculo (r = %s) %s = <b>%s cm²</b>." % (l * l, dec(l / 2.0), dec(round(3.14 * (l / 2.0) ** 2, 2)), dec(round(a, 2))))
    if t == "circ_cuad":
        r = R.randint(1, 15)
        d = 2 * r
        sq = d * d / 2.0
        a = 3.14 * r * r - sq
        return M("Un cuadrado está dentro de un círculo de radio %d cm con sus vértices en la circunferencia (su diagonal mide %d cm). ¿Cuál es el área del círculo que queda fuera del cuadrado? (π ≈ 3.14)" % (r, d),
                 "%s cm²" % dec(round(a, 2)), ["%s cm²" % dec(round(3.14 * r * r - d * d, 2)) if 3.14 * r * r - d * d > 0 else "%s cm²" % dec(round(sq, 2)), "%s cm²" % dec(round(3.14 * r * r, 2)), "%s cm²" % dec(round(a + sq / 2, 2))],
                 "Cuadrado = diagonal² ÷ 2 = %s. Círculo = %s. Resta: <b>%s cm²</b>." % (dec(sq), dec(round(3.14 * r * r, 2)), dec(round(a, 2))))
    if t == "semi":
        b, h = R.choice(range(4, 41, 2)), R.randint(5, 30)
        a = b * h + 3.14 * (b / 2.0) ** 2 / 2
        return M("Un vitral tiene forma de rectángulo de %d cm de ancho y %d cm de alto, con un semicírculo encima del lado de %d cm. ¿Cuál es su área total? (π ≈ 3.14)" % (b, h, b), "%s cm²" % dec(round(a, 2)),
                 ["%s cm²" % dec(round(b * h + 3.14 * (b / 2.0) ** 2, 2)), "%d cm²" % (b * h), "%s cm²" % dec(round(b * h + 3.14 * b * b / 2, 2))],
                 "Rectángulo %d + semicírculo %s = <b>%s cm²</b>." % (b * h, dec(round(3.14 * (b / 2.0) ** 2 / 2, 2)), dec(round(a, 2))))
    if t == "corona":
        R2 = R.randint(4, 20)
        r = R.randint(1, R2 - 1)
        a = 3.14 * (R2 * R2 - r * r)
        return M("Un camino circular está entre dos circunferencias del mismo centro, de radios %d m y %d m. ¿Cuál es el área del camino? (π ≈ 3.14)" % (R2, r), "%s m²" % dec(round(a, 2)),
                 ["%s m²" % dec(round(3.14 * (R2 - r) ** 2, 2)), "%s m²" % dec(round(3.14 * R2 * R2, 2)), "%s m²" % dec(round(2 * 3.14 * (R2 - r), 2))],
                 "π(R² − r²) = 3.14 × (%d − %d) = <b>%s m²</b>." % (R2 * R2, r * r, dec(round(a, 2))))
    l = R.choice([10, 20, 30, 40])
    w = R.choice([4, 6, 8, 10])
    p = 2 * l + 3.14 * w
    return M("Una pista tiene dos tramos rectos de %d m y dos semicírculos de %d m de diámetro en los extremos. ¿Cuánto mide una vuelta? (π ≈ 3.14)" % (l, w), "%s m" % dec(round(p, 2)),
             ["%s m" % dec(round(2 * l + 2 * 3.14 * w, 2)), "%s m" % dec(round(l + 3.14 * w, 2)), "%d m" % (2 * l + 2 * w)], "2 × %d + π × %d = <b>%s m</b> (los dos semicírculos forman un círculo)." % (l, w, dec(round(p, 2))))


# ============================================================ 3.º: medidas de dispersión
def dispersion(*ks):
    t = pick(ks, ["dm", "dm", "rango", "comp", "comp2"])
    n = R.choice([4, 5, 6])
    m = R.randint(5, 20)
    devs = [R.randint(-6, 6) for _ in range(n - 1)]
    devs.append(-sum(devs))
    xs = [m + d for d in devs]
    if min(xs) < 0 or abs(devs[-1]) > 9:
        return None
    if t == "dm":
        dm = F(sum(abs(d) for d in devs), n)
        if dexact(dm) is None:
            return None
        return M("Calcula la desviación media de estos datos: %s (su media es %d)." % (", ".join(map(str, xs)), m), dexact(dm), [dexact(F(sum(devs), n)) or "0", dexact(dm * 2) or "1", dexact(F(max(xs) - min(xs), 1))],
                 "Distancias a la media: %s. Suma %d ÷ %d = <b>%s</b>." % (", ".join(str(abs(d)) for d in devs), sum(abs(d) for d in devs), n, dexact(dm)))
    if t == "rango":
        return M("¿Cuál es el rango de estos datos: %s?" % ", ".join(map(str, xs)), str(max(xs) - min(xs)), [str(max(xs)), str(m), str(max(xs) + min(xs))],
                 "Rango = mayor − menor = %d − %d = <b>%d</b>." % (max(xs), min(xs), max(xs) - min(xs)))
    if t == "comp":
        a = [m - 1, m, m, m + 1]
        b = [m - 8, m - 3, m + 3, m + 8]
        g1, g2 = R.sample(["Grupo A", "Grupo B"], 2)
        if min(b) < 0:
            return None
        return M("%s: %s. %s: %s. Los dos tienen media %d. ¿Cuál es más disperso (sus datos están más alejados de la media)?" % (g1, ", ".join(map(str, a)), g2, ", ".join(map(str, b)), m), g2,
                 [g1, "los dos igual", "no se puede saber sin la moda"], "Desviación media de %s: 0.5; de %s: 5.5. <b>%s</b> es más disperso." % (g1, g2, g2))
    q = R.choice([("Dos equipos tienen la misma media de puntos, pero el equipo A tiene desviación media 2 y el B, 7. ¿Cuál es más constante?", "el equipo A"),
                  ("Dos máquinas llenan botellas de 1 L. La máquina A tiene desviación media 5 mL y la B, 18 mL. ¿Cuál conviene usar?", "la máquina A"),
                  ("Si la desviación media de un conjunto es 0, ¿qué significa?", "todos los datos son iguales"),
                  ("Dos alumnas tienen promedio 8. Las calificaciones de Ana van de 7 a 9 y las de Eva de 5 a 10. ¿Quién es más regular?", "Ana")])
    pool = {"el equipo A": ["el equipo B", "los dos igual", "no se puede saber"], "la máquina A": ["la máquina B", "las dos igual", "no se puede saber"],
            "todos los datos son iguales": ["la media es 0", "no hay datos", "los datos son negativos"], "Ana": ["Eva", "las dos igual", "no se puede saber"]}[q[1]]
    return M(q[0], q[1], pool, "Una dispersión menor significa datos más cercanos a la media (más constantes): <b>%s</b>." % q[1])


# ============================================================ 3.º: eventos independientes y juegos justos
def prob3(*ks):
    t = pick(ks, ["ind", "ind", "dos_mon", "dado_mon", "justo", "justo"])
    if t == "ind":
        p1 = R.choice([F(1, 2), F(1, 6), F(1, 3), F(1, 4), F(2, 5), F(2, 3), F(3, 5), F(1, 8), F(5, 6)])
        p2 = R.choice([F(1, 2), F(1, 6), F(1, 3), F(3, 4), F(1, 5), F(2, 7), F(3, 10), F(4, 5), F(1, 10)])
        return M("Dos eventos independientes tienen probabilidades %s y %s. ¿Cuál es la probabilidad de que ocurran los dos?" % (fq(p1), fq(p2)), fq(p1 * p2), [fq(p1 + p2) if p1 + p2 <= 1 else fq(p1 * p2 * 2), fq((p1 + p2) / 2), fq(1 - p1 * p2)],
                 "Regla del producto: %s × %s = <b>%s</b>." % (fq(p1), fq(p2), fq(p1 * p2)))
    if t == "dos_mon":
        q = R.choice([("dos águilas al lanzar dos monedas", F(1, 4)), ("tres soles al lanzar tres monedas", F(1, 8)), ("un 6 y luego otro 6 al lanzar un dado dos veces", F(1, 36)),
                      ("un número par en los dos lanzamientos de un dado", F(1, 4)), ("águila en una moneda y 1 en un dado", F(1, 12))])
        return M("¿Cuál es la probabilidad de obtener %s?" % q[0], fq(q[1]), [fq(q[1] * 2) if q[1] * 2 <= 1 else "1", fq(F(1, q[1].denominator - 1)) if q[1].denominator > 2 else "1/3", fq(1 - q[1])],
                 "Son independientes: se multiplican las probabilidades. <b>%s</b>." % fq(q[1]))
    if t == "dado_mon":
        n = R.randint(1, 6)
        return M("Se lanza un dado y una moneda. ¿Cuál es la probabilidad de obtener un número mayor que %d y sol?" % (n - 1) if n > 1 else "Se lanza un dado y una moneda. ¿Cuál es la probabilidad de obtener cualquier número y sol?",
                 fq(F(7 - n, 6) / 2), [fq(F(7 - n, 6)), fq(F(7 - n, 6) + F(1, 2)) if F(7 - n, 6) + F(1, 2) <= 1 else fq(F(1, 2)), fq(F(1, 12)) if F(7 - n, 12) != F(1, 12) else fq(F(1, 6))],
                 "%s × 1/2 = <b>%s</b>." % (fq(F(7 - n, 6)), fq(F(7 - n, 6) / 2)))
    q = R.choice([("Ana gana si al lanzar un dado sale par; Beto gana si sale impar. ¿El juego es justo?", "sí: los dos tienen probabilidad 1/2"),
                  ("Ana gana si sale 1 o 2 en un dado; Beto gana con 3, 4, 5 o 6. ¿El juego es justo?", "no: Beto tiene 4/6 y Ana 2/6"),
                  ("Se lanzan dos monedas. Ana gana si salen iguales y Beto si salen distintas. ¿El juego es justo?", "sí: los dos tienen probabilidad 1/2"),
                  ("Se suman dos dados. Ana gana si la suma es 7 y Beto si la suma es 12. ¿El juego es justo?", "no: el 7 sale 6 veces de 36 y el 12 solo 1"),
                  ("En una ruleta de 8 sectores iguales, 3 son rojos y 5 azules. Ana gana con rojo y Beto con azul. ¿El juego es justo?", "no: Beto tiene 5/8 y Ana 3/8"),
                  ("Se lanzan dos dados. Ana gana si sale el mismo número en los dos; Beto si salen números distintos. ¿El juego es justo?", "no: Beto tiene 30/36 y Ana 6/36")])
    pool = ["sí: los dos tienen probabilidad 1/2", "no: siempre gana el primero", "sí: los juegos de azar siempre son justos", "no: Beto tiene 4/6 y Ana 2/6"]
    return M(q[0], q[1], [x for x in pool if x != q[1]][:3], "Un juego es justo si todos los jugadores tienen la misma probabilidad de ganar: <b>%s</b>." % q[1])


# ============================================================ 3.º: problemas con ecuaciones cuadráticas
def ec2_problema(*ks):
    t = pick(ks, ["rect", "rect", "cons", "cuad", "marco", "num"])
    if t == "rect":
        w = R.randint(3, 20)
        k = R.randint(1, 9)
        A = w * (w + k)
        return M("El largo de un terreno rectangular mide %d m más que el ancho y su área es %s m². ¿Cuánto mide el ancho?" % (k, num(A)), "%d m" % w,
                 ["%d m" % (w + k), "%d m" % (A // (2 * w + k)) if A // (2 * w + k) not in (w, w + k) else "%d m" % (w + 2), "%d m" % (w - 1)],
                 "x(x + %d) = %s → x² + %dx − %s = 0 → (x − %d)(x + %d) = 0. El ancho es positivo: <b>%d m</b>." % (k, num(A), k, num(A), w, w + k, w))
    if t == "cons":
        n = R.randint(4, 30)
        return M("El producto de dos números enteros positivos consecutivos es %s. ¿Cuál es el menor?" % num(n * (n + 1)), str(n), [str(n + 1), str(n * (n + 1) // 2), str(n - 1)],
                 "x(x + 1) = %s → x² + x − %s = 0 → x = <b>%d</b>." % (num(n * (n + 1)), num(n * (n + 1)), n))
    if t == "cuad":
        n = R.randint(3, 25)
        k = R.randint(1, 30)
        return M("Si al cuadrado de un número positivo le sumas %d, obtienes %s. ¿Cuál es el número?" % (k, num(n * n + k)), str(n), [str((n * n + k) // 2), str(n * n), str(n + 1)],
                 "x² + %d = %s → x² = %s → x = <b>%d</b> (positivo)." % (k, num(n * n + k), num(n * n), n))
    if t == "marco":
        a, b = R.choice([(10, 6), (12, 8), (20, 14), (16, 10), (30, 20)])
        x = R.randint(1, 4)
        A = (a + 2 * x) * (b + 2 * x)
        return M("Una foto de %d cm × %d cm se pone en un marco de ancho x igual por todos lados. El área total (foto y marco) es %s cm². ¿Cuánto mide x?" % (a, b, num(A)), "%d cm" % x,
                 ["%d cm" % (x + 1), "%d cm" % (2 * x), "%d cm" % (x + 2)], "(%d + 2x)(%d + 2x) = %s. Probamos x = %d: %d × %d = %s. <b>x = %d cm</b>." % (a, b, num(A), x, a + 2 * x, b + 2 * x, num(A), x))
    s_, p = R.randint(5, 20), None
    a = R.randint(1, s_ - 1)
    b = s_ - a
    if a == b:
        return None
    return M("Dos números suman %d y su producto es %d. ¿Cuáles son?" % (s_, a * b), "%d y %d" % (min(a, b), max(a, b)), ["%d y %d" % (min(a, b) - 1, max(a, b) + 1), "%d y %d" % (min(a, b) + 1, max(a, b) - 1) if min(a, b) + 1 != max(a, b) - 1 else "%d y %d" % (s_, 0), "%d y %d" % (1, a * b)],
             "x(%d − x) = %d → x² − %dx + %d = 0 → x = %d o x = %d: <b>%d y %d</b>." % (s_, a * b, s_, a * b, a, b, min(a, b), max(a, b)))



def nocommute(it):
    """quita los problemas donde un distractor es la misma factorización en otro orden: (x − 3)(x + 3) y (x + 3)(x − 3)"""
    import re as _re
    key = lambda c: tuple(sorted(_re.findall(r"\(([^()]+)\)", _re.sub(r"<[^>]+>", "", c)))) if _re.fullmatch(r"(\([^()]+\))+", _re.sub(r"<[^>]+>|\s", "", c)) else None
    ok = key(it["c"][it["a"]])
    return not ok or all(key(c) != ok for i, c in enumerate(it["c"]) if i != it["a"])


# ============================================================ 3.º: valores de razones trigonométricas con calculadora
def trig_calc(*ks):
    t = pick(ks, ["val", "val", "ang"])
    a = R.choice([x for x in range(5, 86) if x not in (30, 45, 60)])
    fs = {"sen": math.sin, "cos": math.cos, "tan": math.tan}
    f = R.choice(list(fs))
    v = fs[f](math.radians(a))
    if t == "val":
        others = [g for g in fs if g != f]
        w = [dec(round(fs[g](math.radians(a)), 4), 4) for g in others] + [dec(round(fs[f](math.radians(90 - a)), 4), 4)]
        return M("Con la calculadora en grados, ¿cuánto vale %s %d° (redondeado a diezmilésimos)?" % (f, a), dec(round(v, 4), 4), w,
                 "%s %d° ≈ <b>%s</b>. Revisa que la calculadora esté en modo DEG." % (f, a, dec(round(v, 4), 4)))
    inv = {"sen": "sen⁻¹", "cos": "cos⁻¹", "tan": "tan⁻¹"}[f]
    return M("Si %s A = %s, ¿cuánto mide el ángulo A (redondeado al grado)?" % (f, dec(round(v, 4), 4)), "%d°" % a, ["%d°" % (90 - a), "%d°" % (a + 5), "%d°" % (a - 5)],
             "Usamos la función inversa: A = %s(%s) ≈ <b>%d°</b>." % (inv, dec(round(v, 4), 4), a))
