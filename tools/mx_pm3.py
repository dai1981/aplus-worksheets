# -*- coding: utf-8 -*-
"""
México, bachillerato: Pensamiento Matemático III (pensamiento variacional: funciones, límites, derivadas e integral, MCCEMS). Problemas propios.
setup(R) antes de usar.
"""
import math
from fractions import Fraction as F
import mx_pm2 as P2
from mx_pm2 import poly, pt  # noqa: F401
from mx_pm1 import opt, from_bank, d2, show, pick, name  # noqa: F401
from mx_s1 import fq, dexact, tabla_html, MINUS, sg  # noqa: F401
from mx_common import num, dec, NB  # noqa: F401

R = None


def setup(rnd):
    global R
    P2.setup(rnd)
    R = P2.R


def ev(cs, x):
    n = len(cs) - 1
    return sum(c * x ** (n - i) for i, c in enumerate(cs))


def der(cs):
    n = len(cs) - 1
    return [c * (n - i) for i, c in enumerate(cs[:-1])]


def nz(lo, hi):
    while True:
        v = R.randint(lo, hi)
        if v:
            return v


def fs(x):
    """Fraction o número → texto con signo"""
    return fq(F(x).limit_denominator(1000)) if not isinstance(x, float) else d2(x, 2)


# ============================================================ P1: variación promedio, movimiento y procesos infinitos
def q1(*ks):
    t = pick(ks, ["tvm", "vel", "tabla", "zenon", "inst"])
    if t == "tvm":
        cs = [nz(-3, 3), R.randint(-5, 5), R.randint(-9, 9)]
        a, b = sorted(R.sample(range(-3, 6), 2))
        v = F(ev(cs, b) - ev(cs, a), b - a)
        return opt("Calcula la razón de cambio promedio de f(x) = %s en el intervalo [%s, %s]." % (poly(cs), sg(a), sg(b)), fq(v),
                   [fq(F(ev(cs, b) - ev(cs, a))), fq(F(ev(cs, b) + ev(cs, a), b - a)), fq(-v) if v else "1"],
                   "[f(%s) − f(%s)] ÷ (%s − %s) = (%s − %s) ÷ %d = <b>%s</b>." % (sg(b), sg(a), sg(b), sg(a), sg(ev(cs, b)), sg(ev(cs, a)), b - a, fq(v)))
    if t == "vel":
        k = R.choice([2, 3, 4, 5])
        t1, t2 = sorted(R.sample(range(0, 7), 2))
        v = k * (t1 + t2)
        return opt("Un objeto recorre d(t) = %dt² metros en t segundos. ¿Cuál es su velocidad promedio entre t = %d s y t = %d s?" % (k, t1, t2), "%d m/s" % v,
                   ["%d m/s" % (k * t2 * t2), "%d m/s" % (k * (t2 * t2 - t1 * t1)), "%d m/s" % (2 * k * t2)],
                   "v = [d(%d) − d(%d)] ÷ (%d − %d) = (%d − %d) ÷ %d = <b>%d m/s</b>." % (t2, t1, t2, t1, k * t2 * t2, k * t1 * t1, t2 - t1, v))
    if t == "tabla":
        lab, u = R.choice([("Población de una ciudad (miles)", "miles por año"), ("Temperatura de un horno (°C)", "°C por minuto"), ("Agua en un tinaco (litros)", "litros por minuto"), ("Ventas acumuladas (piezas)", "piezas por mes")])
        xs = sorted(R.sample(range(0, 13), 4))
        ys = [R.randint(10, 200) for _ in xs]
        if lab.startswith(("Población", "Ventas")):
            ys.sort()
        i, j = sorted(R.sample(range(4), 2))
        v = F(ys[j] - ys[i], xs[j] - xs[i])
        if v.denominator not in (1, 2, 4, 5):
            return None
        tab = tabla_html(["t"] + [str(x) for x in xs], [[lab] + [num(y) for y in ys]])
        return opt(tab + "¿Cuál es la razón de cambio promedio entre t = %d y t = %d?" % (xs[i], xs[j]), show(v) + " " + u,
                   [show(F(ys[j] - ys[i])) + " " + u, show(F(ys[j], xs[j])) + " " + u if xs[j] else "0 " + u, show(-v) + " " + u if v else "1 " + u],
                   "(%s − %s) ÷ (%d − %d) = <b>%s %s</b>." % (num(ys[j]), num(ys[i]), xs[j], xs[i], show(v), u))
    if t == "zenon":
        r = R.choice([F(1, 2), F(1, 3), F(1, 4), F(2, 3), F(1, 5), F(3, 4)])
        a = R.choice([1, 2, 3, 4, 6, 8, 10, 12])
        s = a / (1 - r)
        return opt("Un corredor avanza %d m, luego %s de esa distancia, luego %s de la anterior, y así sin fin. ¿A qué distancia total se acerca?" % (a, fq(r), fq(r)), fq(s) + " m",
                   ["infinita", fq(a * (1 + r)) + " m", fq(a / r) + " m"],
                   "Es una suma infinita con razón %s: S = a ÷ (1 − r) = %d ÷ %s = <b>%s m</b>. Un proceso infinito puede tener un resultado finito." % (fq(r), a, fq(1 - r), fq(s)))
    a = R.randint(1, 6)
    k = R.choice([1, 2, 3, 4, 5])
    hs = [F(1, 10), F(1, 100), F(1, 1000)]
    vals = [k * (2 * a + h) for h in hs]
    tab = tabla_html(["h", "0.1", "0.01", "0.001"], [["Velocidad promedio en [%d, %d + h]" % (a, a)] + [dexact(v) for v in vals]])
    return opt(tab + "Un objeto se mueve con d(t) = %st². Según la tabla, ¿cuál es la velocidad instantánea en t = %d?" % ("" if k == 1 else str(k), a), "%d" % (2 * k * a),
               [dexact(vals[0]), "%d" % (k * a * a), "%d" % (2 * k * a + 1)],
               "Cuando h se hace muy pequeño, la velocidad promedio se acerca a <b>%d</b>: esa es la velocidad instantánea." % (2 * k * a))


# ============================================================ P2: la recta tangente
def q2(*ks):
    t = pick(ks, ["secante", "acerca", "pend", "ecuacion", "concepto"])
    a = R.randint(-3, 4)
    k = R.choice([1, 2, 3, -1])
    cs = [k, R.randint(-4, 4), R.randint(-5, 5)]
    if t == "secante":
        h = R.choice([1, 2, 3])
        v = F(ev(cs, a + h) - ev(cs, a), h)
        return opt("Calcula la pendiente de la recta secante a f(x) = %s que pasa por x = %s y x = %s." % (poly(cs), sg(a), sg(a + h)), fq(v),
                   [fq(v + k * h), fq(F(ev(cs, a + h) + ev(cs, a), h)), fq(F(ev(cs, a + h)))], "m = [f(%s) − f(%s)] ÷ %d = <b>%s</b>." % (sg(a + h), sg(a), h, fq(v)))
    if t == "acerca":
        m = 2 * k * a + cs[1]
        tab = tabla_html(["h", "1", "0.1", "0.01"], [["pendiente de la secante"] + [dexact(F(m) + k * F(h)) for h in (1, F(1, 10), F(1, 100))]])
        return opt(tab + "Las pendientes de las secantes a f(x) = %s entre x = %s y x = %s + h están en la tabla. ¿Cuál es la pendiente de la recta tangente en x = %s?" % (poly(cs), sg(a), sg(a), sg(a)),
                   sg(m), [dexact(F(m) + k), sg(m + 1), sg(ev(cs, a))], "Al hacer h → 0 las secantes se acercan a la tangente: pendiente <b>%s</b>." % sg(m))
    if t == "pend":
        m = 2 * k * a + cs[1]
        return opt("La pendiente de la tangente a f(x) = %s en x = %s es…" % (poly(cs), sg(a)), sg(m), [sg(ev(cs, a)), sg(k * a * a), sg(m + 2 * k)],
                   "Con f′(x) = %s: f′(%s) = <b>%s</b>." % (poly(der(cs)), sg(a), sg(m)))
    if t == "ecuacion":
        m = 2 * k * a + cs[1]
        y0 = ev(cs, a)
        b = y0 - m * a
        return opt("¿Cuál es la ecuación de la recta tangente a f(x) = %s en el punto de abscisa x = %s?" % (poly(cs), sg(a)), "y = " + poly([m, b]),
                   ["y = " + poly([y0, m]) if y0 else "y = " + poly([1, m]), "y = " + poly([m, y0]), "y = " + poly([-m, b]) if m else "y = " + poly([1, b])],
                   "Punto (%s, %s), pendiente f′(%s) = %s. y − %s = %s(x − %s) → <b>y = %s</b>." % (sg(a), sg(y0), sg(a), sg(m), sg(y0), sg(m), sg(a), poly([m, b])))
    items = [("La recta tangente a una curva en un punto…", "toca la curva en ese punto y tiene su misma inclinación", ["siempre corta la curva en dos puntos", "es horizontal", "pasa por el origen"], "La tangente indica la dirección de la curva en ese punto."),
             ("¿Qué pasa con la recta secante entre P y Q cuando Q se acerca a P?", "se acerca a la recta tangente en P", ["se vuelve vertical", "desaparece", "se aleja de la curva"], "Ese límite de secantes es la idea de la derivada."),
             ("Si la tangente en un punto es horizontal, su pendiente es…", "0", ["1", "infinita", "−1"], "Recta horizontal: pendiente 0; ahí puede haber un máximo o un mínimo."),
             ("¿Quiénes desarrollaron el cálculo en el siglo XVII?", "Newton y Leibniz", ["Euclides y Pitágoras", "Descartes y Fermat solamente", "Gauss y Euler"], "Newton (movimiento) y Leibniz (tangentes) lo desarrollaron de forma independiente."),
             ("La pendiente de la tangente representa…", "la razón de cambio instantánea", ["la razón de cambio promedio en un intervalo grande", "el área bajo la curva", "el valor de la función"], "Es la derivada en ese punto.")]
    return from_bank(items)


# ============================================================ P3: operaciones con funciones y modelación
def q3(*ks):
    t = pick(ks, ["suma", "prod", "coc", "comp", "comp2", "modelo"])
    f = [nz(-4, 4), R.randint(-6, 6)]
    g = [nz(-2, 2), R.randint(-3, 3), R.randint(-5, 5)]
    a = R.randint(-3, 3)
    fa, ga = ev(f, a), ev(g, a)
    head = "Si f(x) = %s y g(x) = %s, " % (poly(f), poly(g))
    if t == "suma":
        return opt(head + "¿cuánto vale (f + g)(%s)?" % sg(a), sg(fa + ga), [sg(fa - ga), sg(fa * ga), sg(fa + ga + 1)], "(f + g)(%s) = f(%s) + g(%s) = %s + %s = <b>%s</b>." % (sg(a), sg(a), sg(a), sg(fa), sg(ga), sg(fa + ga)))
    if t == "prod":
        return opt(head + "¿cuánto vale (f · g)(%s)?" % sg(a), sg(fa * ga), [sg(fa + ga), sg(ev(f, ga)), sg(fa * ga + 2)], "(f · g)(%s) = %s × %s = <b>%s</b>." % (sg(a), sg(fa), sg(ga), sg(fa * ga)))
    if t == "coc":
        if ga == 0:
            return None
        v = F(fa, ga)
        return opt(head + "¿cuánto vale (f/g)(%s)?" % sg(a), fq(v), [fq(F(ga, fa)) if fa else "0", fq(v + 1), sg(fa - ga)], "(f/g)(%s) = %s ÷ %s = <b>%s</b>." % (sg(a), sg(fa), sg(ga), fq(v)))
    if t == "comp":
        v = ev(f, ga)
        return opt(head + "¿cuánto vale (f ∘ g)(%s) = f(g(%s))?" % (sg(a), sg(a)), sg(v), [sg(ev(g, fa)), sg(fa * ga), sg(fa + ga)],
                   "Primero g(%s) = %s; luego f(%s) = <b>%s</b>." % (sg(a), sg(ga), sg(ga), sg(v)))
    if t == "comp2":
        m, b = f
        p, q = nz(-3, 3), R.randint(-5, 5)
        res = [m * p, m * q + b]
        return opt("Si f(x) = %s y h(x) = %s, ¿cuál es f(h(x))?" % (poly(f), poly([p, q])), poly(res), [poly([m * p, p * b + q]), poly([m + p, b + q]), poly([m * p, q + b])],
                   "f(h(x)) = %s(%s) %s %s = <b>%s</b>." % (sg(m), poly([p, q]), "+" if b >= 0 else "−", num(abs(b)), poly(res)))
    c, k, fijo = R.choice([(8, 20, 30), (12, 15, 40), (25, 10, 100), (6, 30, 50)])
    n = R.randint(5, 40)
    return opt("Una fábrica hace q(t) = %dt piezas en t horas, y el costo de q piezas es C(q) = %dq + %d pesos. ¿Cuánto cuesta lo que se produce en %d horas?" % (k, c, fijo, n),
               "$" + num(c * k * n + fijo), ["$" + num(c * n + fijo), "$" + num(k * n), "$" + num((c + fijo) * k * n)],
               "C(q(t)) = %d(%dt) + %d = %dt + %d. Con t = %d: <b>$%s</b>." % (c, k, fijo, c * k, fijo, n, num(c * k * n + fijo)))


# ============================================================ P4: simetría, crecimiento, extremos y concavidad
def q4(*ks):
    t = pick(ks, ["paridad", "paridad", "crece", "concav", "max"])
    if t == "paridad":
        kind = R.choice(["par", "impar", "ninguna"])
        if kind == "par":
            cs = [nz(-3, 3), 0, R.randint(-5, 5), 0, R.randint(-9, 9)]
        elif kind == "impar":
            cs = [nz(-3, 3), 0, nz(-5, 5), 0]
        else:
            cs = [nz(-3, 3), nz(-4, 4), R.randint(-5, 5)]
        ans = {"par": "par: simétrica respecto al eje y", "impar": "impar: simétrica respecto al origen", "ninguna": "ni par ni impar"}
        return opt("¿Qué simetría tiene f(x) = %s?" % poly(cs), ans[kind], [v for k, v in ans.items() if k != kind] + ["simétrica respecto al eje x"],
                   {"par": "Solo hay potencias pares: f(−x) = f(x).", "impar": "Solo hay potencias impares: f(−x) = −f(x).", "ninguna": "Mezcla potencias pares e impares: no cumple ninguna."}[kind])
    a = nz(-3, 3)
    h, k = R.randint(-4, 4), R.randint(-6, 6)
    cs = [a, -2 * a * h, a * h * h + k]
    if t == "crece":
        ok = "(%s, ∞)" % sg(h) if a > 0 else "(−∞, %s)" % sg(h)
        return opt("¿En qué intervalo es <b>creciente</b> f(x) = %s?" % poly(cs), ok, ["(−∞, %s)" % sg(h) if a > 0 else "(%s, ∞)" % sg(h), "(%s, ∞)" % sg(k), "en todo ℝ"],
                   "Es una parábola con vértice en x = %s que abre hacia %s: crece en <b>%s</b>." % (sg(h), "arriba" if a > 0 else "abajo", ok))
    if t == "concav":
        return opt("La gráfica de f(x) = %s es cóncava…" % poly(cs), "hacia arriba (forma de U)" if a > 0 else "hacia abajo (forma de ∩)",
                   ["hacia abajo (forma de ∩)" if a > 0 else "hacia arriba (forma de U)", "hacia arriba solo para x &gt; 0", "no tiene concavidad"],
                   "El coeficiente de x² es %s: cóncava <b>%s</b>." % (sg(a), "hacia arriba" if a > 0 else "hacia abajo"))
    kind = "mínimo" if a > 0 else "máximo"
    return opt("¿Qué extremo tiene f(x) = %s y dónde?" % poly(cs), "un %s en %s" % (kind, pt(h, k)), ["un %s en %s" % ("máximo" if a > 0 else "mínimo", pt(h, k)), "un %s en %s" % (kind, pt(-h, k)), "un %s en %s" % (kind, pt(k, h))],
               "Vértice en x = −b/(2a) = %s, f(%s) = %s; como a %s 0 es un <b>%s</b>." % (sg(h), sg(h), sg(k), "&gt;" if a > 0 else "&lt;", kind))


# ============================================================ P5: límites (tabla y leyes)
def q5(*ks):
    t = pick(ks, ["tabla", "leyes", "sust", "factor"])
    if t == "tabla":
        L = R.randint(-5, 9)
        a = R.randint(-3, 5)
        eps = [F(1, 10), F(1, 100), F(1, 1000)]
        left = [L - e * R.choice([1, 2, 3]) for e in eps]
        right = [L + e * R.choice([1, 2, 3]) for e in eps]
        tab = tabla_html(["x"] + [dexact(a - e) for e in eps] + [dexact(a + e) for e in reversed(eps)], [["f(x)"] + [dexact(v) for v in left] + [dexact(v) for v in reversed(right)]])
        return opt(tab + "Según la tabla, ¿cuál es el límite de f(x) cuando x → %s?" % sg(a), sg(L), [sg(L + 1), dexact(left[0]), "no existe"],
                   "Por la izquierda y por la derecha, f(x) se acerca a <b>%s</b>." % sg(L))
    if t == "leyes":
        A, B = nz(-6, 6), nz(-5, 5)
        k = R.choice(["comb", "prod", "coc", "pot"])
        if k == "comb":
            m, n = nz(-4, 4), nz(-4, 4)
            v = m * A + n * B
            exp_ = "%s·f(x) %s %s·g(x)" % (sg(m), "+" if n > 0 else "−", num(abs(n)))
            w = [sg(m * A - n * B), sg(A + B), sg(v + m)]
        elif k == "prod":
            v = A * B
            exp_ = "f(x) · g(x)"
            w = [sg(A + B), sg(A - B), sg(v + 1)]
        elif k == "coc":
            v = F(A, B)
            exp_ = "f(x) ÷ g(x)"
            w = [fq(F(B, A)), sg(A - B), fq(v + 1)]
        else:
            v = A * A + B
            exp_ = "[f(x)]² + g(x)"
            w = [sg(2 * A + B), sg(A + B), sg(A * A - B)]
        return opt("Si lím<sub>x→a</sub> f(x) = %s y lím<sub>x→a</sub> g(x) = %s, ¿cuánto vale lím<sub>x→a</sub> [%s]?" % (sg(A), sg(B), exp_), fq(v), w,
                   "Por las leyes de los límites, se sustituye cada límite: <b>%s</b>." % fq(v))
    if t == "sust":
        cs = [nz(-3, 3), R.randint(-5, 5), R.randint(-9, 9)]
        a = R.randint(-3, 3)
        return opt("Calcula lím<sub>x→%s</sub> (%s)." % (sg(a), poly(cs)), sg(ev(cs, a)), [sg(ev(cs, -a)) if a else sg(ev(cs, 1)), sg(cs[-1]), sg(ev(cs, a) + 1)],
                   "Un polinomio es continuo: basta sustituir x = %s → <b>%s</b>." % (sg(a), sg(ev(cs, a))))
    a = nz(-5, 5)
    b = R.randint(-6, 6)
    if b == -a:
        return None
    # (x − a)(x + b)/(x − a) → a + b
    num_ = poly([1, b - a, -a * b])
    return opt("Calcula lím<sub>x→%s</sub> (%s) ÷ (%s)." % (sg(a), num_, poly([1, -a])), sg(a + b), ["0", "no existe", sg(a - b)],
               "Al sustituir sale 0/0. Factorizamos: (x %s %d)(x %s %d)/(x %s %d) = x %s %d → <b>%s</b>." % ("−" if a > 0 else "+", abs(a), "+" if b >= 0 else "−", abs(b), "−" if a > 0 else "+", abs(a), "+" if b >= 0 else "−", abs(b), sg(a + b)))


# ============================================================ P6: continuidad y teorema del valor intermedio
def q6(*ks):
    t = pick(ks, ["tvi", "intervalo", "param", "tipo"])
    if t == "tvi":
        a, b = sorted(R.sample(range(-4, 6), 2))
        fa, fb = R.randint(-9, -1), R.randint(1, 9)
        if R.random() < .5:
            fa, fb = fb, fa
        return opt("f es continua en [%s, %s], con f(%s) = %s y f(%s) = %s. ¿Qué asegura el teorema del valor intermedio?" % (sg(a), sg(b), sg(a), sg(fa), sg(b), sg(fb)),
                   "que f tiene al menos un cero entre %s y %s" % (sg(a), sg(b)), ["que f tiene exactamente un cero en x = %s" % fs(F(a + b, 2)), "que f no tiene ceros en el intervalo", "que f es creciente"],
                   "f cambia de signo y no tiene saltos: debe pasar por 0 en algún punto de (%s, %s)." % (sg(a), sg(b)))
    if t == "intervalo":
        while True:
            cs = [1, R.randint(-3, 3), R.randint(-6, 6), R.randint(-6, 6)]
            ints = [(i, i + 1) for i in range(-3, 3)]
            good = [(i, j) for i, j in ints if ev(cs, i) * ev(cs, j) < 0]
            if len(good) == 1 and all(ev(cs, i) != 0 for i in range(-3, 4)):
                break
        g = good[0]
        bad = [x for x in ints if x != g]
        return opt("¿En qué intervalo tiene un cero f(x) = %s?" % poly(cs), "[%s, %s]" % (sg(g[0]), sg(g[1])), ["[%s, %s]" % (sg(i), sg(j)) for i, j in R.sample(bad, 3)],
                   "f(%s) = %s y f(%s) = %s: cambia de signo, así que hay un cero en <b>[%s, %s]</b>." % (sg(g[0]), sg(ev(cs, g[0])), sg(g[1]), sg(ev(cs, g[1])), sg(g[0]), sg(g[1])))
    if t == "param":
        a = R.randint(-3, 4)
        m, b = nz(-3, 3), R.randint(-5, 5)
        n = nz(-3, 3)
        k = m * a + b - n * a
        return opt("¿Qué valor de k hace continua a f(x) = %s si x &lt; %s, y f(x) = %s si x ≥ %s?" % (poly([m, b]), sg(a), poly([n, 0]) + " + k", sg(a)), sg(k),
                   [sg(m * a + b), sg(-k) if k else "1", sg(k + n)], "Los dos lados deben coincidir en x = %s: %s = %s + k → k = <b>%s</b>." % (sg(a), sg(m * a + b), sg(n * a), sg(k)))
    items = [("f(x) = 1/x en x = 0 es…", "discontinua: no está definida y tiene una asíntota", ["continua", "discontinua por un salto finito", "continua por la derecha"], "f(0) no existe y los valores crecen sin límite."),
             ("f(x) = (x² − 1)/(x − 1) en x = 1 tiene…", "una discontinuidad evitable (un hueco)", ["una asíntota vertical", "un salto", "ninguna discontinuidad"], "Se simplifica a x + 1 salvo en x = 1: el límite existe (2) pero f(1) no."),
             ("Una función es continua en x = a si…", "f(a) existe, el límite existe y son iguales", ["f(a) = 0", "el límite es infinito", "es un polinomio"], "Son las tres condiciones de continuidad."),
             ("Las funciones polinomiales son…", "continuas en todos los reales", ["discontinuas en x = 0", "continuas solo en x &gt; 0", "discontinuas en sus ceros"], "Se dibujan sin levantar el lápiz."),
             ("La tarifa de estacionamiento cobra $20 por cada hora o fracción. Su gráfica es…", "discontinua: tiene saltos", ["continua", "una recta", "una parábola"], "El precio salta de $20 a $40 al pasar de 1 h."),
             ("f(x) = √x es continua…", "para x ≥ 0", ["para todo x real", "solo en x = 0", "para x &lt; 0"], "La raíz cuadrada solo está definida para x ≥ 0.")]
    return from_bank(items)


# ============================================================ P7: la derivada por definición
def q7(*ks):
    t = pick(ks, ["def", "cociente", "valor", "concepto"])
    a, b, c = nz(-4, 4), R.randint(-6, 6), R.randint(-9, 9)
    x0 = R.randint(-3, 4)
    if t == "def":
        return opt("Usando la definición f′(a) = lím<sub>h→0</sub> [f(a + h) − f(a)] ÷ h, calcula f′(%s) para f(x) = %s." % (sg(x0), poly([a, b, c])), sg(2 * a * x0 + b),
                   [sg(a * x0 * x0 + b * x0 + c), sg(2 * a * x0), sg(a * x0 + b)],
                   "[f(%s + h) − f(%s)] ÷ h = %s + %sh → con h → 0: <b>%s</b>." % (sg(x0), sg(x0), sg(2 * a * x0 + b), sg(a) if a != 1 else "", sg(2 * a * x0 + b)))
    if t == "cociente":
        ok = "%s + %sh" % (poly([2 * a, b]), "" if a == 1 else MINUS if a == -1 else sg(a))
        ok = ok.replace("+ −", "− ")
        w = ["%s + %sh" % (poly([a, b]), "" if a == 1 else sg(a)), poly([2 * a, b]) + " + h²", "%s + %sh" % (poly([2 * a, b + c]), "" if a == 1 else sg(a))]
        w = [x.replace("+ −", "− ") for x in w]
        return opt("Para f(x) = %s, simplifica el cociente [f(x + h) − f(x)] ÷ h." % poly([a, b, c]), ok, w,
                   "f(x + h) − f(x) = %s·(2xh + h²) %s %sh. Al dividir entre h: <b>%s</b>. Con h → 0 queda f′(x) = %s." % (sg(a), "+" if b >= 0 else "−", num(abs(b)), ok, poly([2 * a, b])))
    if t == "valor":
        k = R.randint(2, 4)
        cs = [nz(-3, 3)] + [R.randint(-5, 5) for _ in range(k)]
        d = der(cs)
        return opt("Si f(x) = %s, ¿cuánto vale f′(%s)?" % (poly(cs), sg(x0)), sg(ev(d, x0)), [sg(ev(cs, x0)), sg(ev(d, -x0)) if x0 else sg(ev(d, 1)), sg(ev(d, x0) + cs[0])],
                   "f′(x) = %s; f′(%s) = <b>%s</b>." % (poly(d), sg(x0), sg(ev(d, x0))))
    items = [("La derivada de una función constante f(x) = 7 es…", "0", ["7", "1", "x"], "Una constante no cambia: su razón de cambio es 0."),
             ("La derivada de f(x) = mx + b es…", "m", ["b", "mx", "0"], "La pendiente de una recta es constante."),
             ("f′(a) representa…", "la pendiente de la tangente en x = a", ["el valor de f en a", "el área bajo f", "la ordenada al origen"], "Es la razón de cambio instantánea en a."),
             ("Si f′(a) &gt; 0, la función en x = a…", "es creciente", ["es decreciente", "tiene un máximo", "vale 0"], "Pendiente positiva: la función sube."),
             ("La derivada de f(x) = xⁿ es…", "n·xⁿ⁻¹", ["xⁿ⁻¹", "n·xⁿ", "(n − 1)xⁿ"], "Regla de la potencia."),
             ("Si f′(a) = 0, la tangente en x = a es…", "horizontal", ["vertical", "inexistente", "de pendiente 1"], "Pendiente 0: recta horizontal.")]
    return from_bank(items)


# ============================================================ P9: la derivada como razón de cambio
def q9(*ks):
    t = pick(ks, ["vel", "acel", "costo", "area", "poblacion"])
    if t in ("vel", "acel"):
        a = R.choice([-5, -4.9, 2, 3, 4, -3, 1.5, 2.5])
        b, c = R.randint(1, 30), R.randint(1, 50)
        tt = R.randint(1, 5)
        st = "%st² + %dt + %d" % ("" if a == 1 else d2(a, 1), b, c)
        if t == "vel":
            v = 2 * a * tt + b
            return opt("La posición de un objeto es s(t) = %s metros (t en segundos). ¿Cuál es su velocidad en t = %d s?" % (st, tt),
                       d2(v, 1) + " m/s", [d2(a * tt * tt + b * tt + c, 1) + " m/s", d2(a * tt + b, 1) + " m/s", d2(2 * a, 1) + " m/s"],
                       "v(t) = s′(t) = %st + %d. v(%d) = <b>%s m/s</b>." % (d2(2 * a, 1), b, tt, d2(v, 1)))
        return opt("Si la posición de un objeto es s(t) = %s metros, ¿cuál es su aceleración?" % st, d2(2 * a, 1) + " m/s²", [d2(a, 1) + " m/s²", d2(2 * a * tt + b, 1) + " m/s²", "%d m/s²" % b],
                   "v(t) = %st + %d y a(t) = v′(t) = <b>%s m/s²</b>." % (d2(2 * a, 1), b, d2(2 * a, 1)))
    if t == "costo":
        a, b, c = R.choice([1, 2, 3]), R.choice([20, 40, 50, 80]), R.choice([500, 1000, 2000])
        q = R.randint(5, 40)
        return opt("El costo de producir q piezas es C(q) = %s pesos. ¿Cuál es el costo marginal cuando q = %d?" % (poly([a, b, c]).replace("x", "q"), q), "$" + num(2 * a * q + b) + " por pieza",
                   ["$" + num(a * q * q + b * q + c) + " por pieza", "$" + num(a * q + b) + " por pieza", "$" + num(b) + " por pieza"],
                   "Costo marginal = C′(q) = %s. C′(%d) = <b>$%s por pieza</b>: lo que cuesta, aproximadamente, una pieza más." % (poly([2 * a, b]).replace("x", "q"), q, num(2 * a * q + b)))
    if t == "area":
        r = R.randint(2, 15)
        return opt("El área de un círculo es A(r) = πr². ¿Cuál es la razón de cambio del área respecto al radio cuando r = %d cm?" % r, "%dπ cm²/cm" % (2 * r),
                   ["%dπ cm²/cm" % (r * r), "%dπ cm²/cm" % r, "%d cm²/cm" % (2 * r)], "A′(r) = 2πr = <b>%dπ</b> cm² por cm (es el perímetro)." % (2 * r))
    P0, k = R.choice([1000, 2000, 5000, 500]), R.choice([20, 30, 40, 50])
    tt = R.randint(1, 10)
    return opt("Una población crece según P(t) = %s + %dt² (t en años). ¿A qué ritmo crece en t = %d?" % (num(P0), k, tt), "%s por año" % num(2 * k * tt),
               ["%s por año" % num(P0 + k * tt * tt), "%s por año" % num(k * tt), "%s por año" % num(2 * k)], "P′(t) = %dt; P′(%d) = <b>%s</b> habitantes por año." % (2 * k, tt, num(2 * k * tt)))


# ============================================================ P11: optimización
def q11(*ks):
    t = pick(ks, ["cerca", "rio", "producto", "caja", "ingreso"])
    if t == "cerca":
        P = R.choice(range(40, 401, 20))
        l = F(P, 4)
        return opt("Con %d m de malla se quiere cercar un terreno rectangular con la mayor área posible. ¿Qué medidas debe tener?" % P, "%s m × %s m" % (show(l), show(l)),
                   ["%s m × %s m" % (show(l / 2), show(3 * l / 2)), "%s m × %s m" % (show(F(P, 2)), show(F(P, 2))), "%s m × %s m" % (show(l + 5), show(l - 5))],
                   "A(x) = x(%d/2 − x). A′(x) = %s − 2x = 0 → x = %s: un cuadrado de <b>%s m</b> por lado." % (P, show(F(P, 2)), show(l), show(l)))
    if t == "rio":
        P = R.choice(range(40, 601, 20))
        x = F(P, 4)
        return opt("Se cercan tres lados de un terreno rectangular junto a un río (el río es el cuarto lado) con %d m de malla. ¿Cuál es el área máxima?" % P, show(x * F(P, 2)) + " m²",
                   [show(F(P, 4) ** 2) + " m²", show(F(P, 3) ** 2) + " m²", show(x * F(P, 2) / 2) + " m²"],
                   "A(x) = x(%d − 2x). A′(x) = %d − 4x = 0 → x = %s m y el otro lado %s m. Área = <b>%s m²</b>." % (P, P, show(x), show(F(P, 2)), show(x * F(P, 2))))
    if t == "producto":
        S = R.choice(range(10, 101, 2))
        return opt("Dos números positivos suman %d. ¿Cuál es el mayor producto posible?" % S, num((S // 2) ** 2), [num((S // 2 - 1) * (S // 2 + 1)), num(S * S // 2), num(S)],
                   "P(x) = x(%d − x); P′(x) = %d − 2x = 0 → x = %d. Producto máximo = %d × %d = <b>%s</b>." % (S, S, S // 2, S // 2, S // 2, num((S // 2) ** 2)))
    if t == "caja":
        L = R.choice(range(12, 121, 6))
        x = L // 6
        V = x * (L - 2 * x) ** 2
        return opt("De una lámina cuadrada de %d cm de lado se cortan cuadrados de x cm en las esquinas para hacer una caja sin tapa. ¿Qué x da el volumen máximo?" % L, "%d cm" % x,
                   ["%d cm" % (L // 4), "%d cm" % (L // 2), "%d cm" % (L // 3)],
                   "V(x) = x(%d − 2x)². V′(x) = 0 da x = %d/6 = <b>%d cm</b> (volumen %s cm³)." % (L, L, x, num(V)))
    d = R.choice([1, 2, 4, 5])
    p = R.choice(range(20, 201, 10))
    n = R.choice(range(100, 801, 20))
    # ingreso I(x) = (p + x)(n − d·x)… precio sube x, se venden d menos por peso
    x = F(n - d * p, 2 * d)
    if x <= 0 or x.denominator != 1:
        return None
    return opt("Un puesto vende %d tortas al día a $%d. Por cada peso que sube el precio, vende %d tortas menos. ¿Qué precio da el mayor ingreso?" % (n, p, d), "$" + num(p + int(x)),
               ["$" + num(p), "$" + num(p + int(x) * 2), "$" + num(p + int(x) // 2)],
               "I(x) = (%d + x)(%d − %dx). I′(x) = 0 → x = %d. Precio = <b>$%s</b>." % (p, n, d, int(x), num(p + int(x))))


# ============================================================ P12: exponenciales y logaritmos
def q12(*ks):
    t = pick(ks, ["log", "inversa", "grafica", "modelo", "ecuacion"])
    if t == "log":
        b = R.choice([2, 3, 5, 10])
        e = R.randint(-2, 5)
        x = F(b) ** e
        return opt("Calcula log<sub>%d</sub> %s." % (b, fq(x)), sg(e), [sg(e + 1), fq(x / b) if x / b != e else "1", sg(-e) if e else "1"], "%d<sup>%s</sup> = %s, así que log<sub>%d</sub> %s = <b>%s</b>." % (b, sg(e), fq(x), b, fq(x), sg(e)))
    if t == "inversa":
        b = R.choice([2, 3, 4, 5, 10])
        y = R.randint(1, 4)
        x = b ** y
        k = R.choice(["exp", "log"])
        if k == "exp":
            return opt("Si log<sub>%d</sub> x = %d, ¿cuánto vale x?" % (b, y), num(x), [num(b * y), num(y ** b), num(x // b)], "log<sub>%d</sub> x = %d significa %d<sup>%d</sup> = x → <b>%s</b>." % (b, y, b, y, num(x)))
        return opt("La función inversa de f(x) = %d<sup>x</sup> es…" % b, "g(x) = log<sub>%d</sub> x" % b, ["g(x) = x<sup>%d</sup>" % b, "g(x) = 1/%d<sup>x</sup>" % b, "g(x) = %dx" % b],
                   "Exponencial y logaritmo de la misma base son inversas: sus gráficas son simétricas respecto a y = x.")
    if t == "grafica":
        items = [("La gráfica de y = 2<sup>x</sup> pasa siempre por el punto…", "(0, 1)", ["(1, 0)", "(0, 0)", "(2, 1)"], "Cualquier b<sup>0</sup> = 1."),
                 ("La gráfica de y = log<sub>3</sub> x pasa por el punto…", "(1, 0)", ["(0, 1)", "(0, 0)", "(3, 0)"], "log<sub>b</sub> 1 = 0 para cualquier base."),
                 ("Si 0 &lt; b &lt; 1, la función y = b<sup>x</sup> es…", "decreciente", ["creciente", "constante", "una recta"], "Por ejemplo (1/2)<sup>x</sup> baja al aumentar x."),
                 ("La función y = 5<sup>x</sup> tiene como asíntota…", "el eje x (y = 0)", ["el eje y", "la recta y = x", "no tiene asíntotas"], "Para x muy negativo, 5<sup>x</sup> se acerca a 0 sin tocarlo."),
                 ("El dominio de y = log x es…", "x &gt; 0", ["todos los reales", "x ≥ 0", "x &lt; 0"], "Solo existen logaritmos de números positivos."),
                 ("¿Qué base crece más rápido para x &gt; 0?", "y = 10<sup>x</sup>", ["y = 2<sup>x</sup>", "y = 3<sup>x</sup>", "y = e<sup>x</sup>"], "A mayor base (mayor que 1), crecimiento más rápido."),
                 ("Las gráficas de y = 2<sup>x</sup> y y = log<sub>2</sub> x son simétricas respecto a…", "la recta y = x", ["el eje x", "el eje y", "el origen"], "Son funciones inversas.")]
        return from_bank(items)
    if t == "modelo":
        P0 = R.choice([100, 200, 500, 1000, 50])
        T = R.choice([2, 3, 4, 5, 6])
        tt = T * R.randint(1, 5)
        kind = R.choice(["dup", "mitad"])
        if kind == "dup":
            v = P0 * 2 ** (tt // T)
            return opt("Un cultivo de %s bacterias se duplica cada %d horas. ¿Cuántas habrá a las %d horas?" % (num(P0), T, tt), num(v), [num(P0 * 2 * tt // T), num(P0 * tt), num(v // 2)],
                       "P(t) = %s × 2<sup>t/%d</sup>; t = %d → 2<sup>%d</sup> × %s = <b>%s</b>." % (num(P0), T, tt, tt // T, num(P0), num(v)))
        m = R.choice([800, 640, 1600, 320, 960])
        v = F(m, 2 ** (tt // T))
        return opt("Una sustancia de %d mg tiene una vida media de %d años. ¿Cuánto queda a los %d años?" % (m, T, tt), show(v) + " mg", [show(F(m, 2 * (tt // T))) + " mg", show(v * 2) + " mg", show(F(m) - F(m, 2) * (tt // T)) + " mg" if tt // T < 2 else show(v / 2) + " mg"],
                   "Cada %d años queda la mitad: %d × (1/2)<sup>%d</sup> = <b>%s mg</b>." % (T, m, tt // T, show(v)))
    b = R.choice([2, 3, 5])
    k = R.randint(1, 5)
    c = R.randint(-2, 3)
    return opt("Resuelve %d<sup>x %s %d</sup> = %s." % (b, "+" if c >= 0 else "−", abs(c), num(b ** k)), "x = %s" % sg(k - c), ["x = %s" % sg(k + c), "x = %d" % k, "x = %s" % sg(b ** k - c)],
               "%s = %d<sup>%d</sup>, entonces x %s %d = %d → <b>x = %s</b>." % (num(b ** k), b, k, "+" if c >= 0 else "−", abs(c), k, sg(k - c)))


# ============================================================ P13: funciones trigonométricas y fenómenos periódicos
def q13(*ks):
    t = pick(ks, ["amp", "per", "maxmin", "fenomeno", "valor"])
    A = R.choice([1, 2, 3, 4, 5, 10])
    B = F(R.choice([1, 2, 3, 4, F(1, 2)]))
    D = R.randint(-3, 5)
    fn = R.choice(["sen", "cos"])
    inner = "x" if B == 1 else ("%dx" % B) if B.denominator == 1 else "x/%d" % B.denominator
    f = "%s%s(%s)%s" % ("" if A == 1 else str(A), fn, inner, (" + %d" % D) if D > 0 else (" − %d" % -D) if D < 0 else "")

    def pif(x):
        x = F(x)
        if x == 1:
            return "π"
        if x.denominator == 1:
            return "%dπ" % x
        return ("π" if x.numerator == 1 else "%dπ" % x.numerator) + "/%d" % x.denominator
    if t == "amp":
        return opt("¿Cuál es la amplitud de y = %s?" % f, str(A), [str(2 * A), pif(2 / B), str(A + 1) if D == 0 or D == A + 1 else sg(D)],
                   "La amplitud es el número que multiplica a %s: <b>%d</b>. Mide qué tanto sube y baja desde el centro." % (fn, A))
    if t == "per":
        P = 2 / B
        return opt("¿Cuál es el periodo de y = %s?" % f, pif(P), [pif(B), pif(P * 2), pif(P / 2)], "Periodo = 2π ÷ %s = <b>%s</b>." % (fq(B), pif(P)))
    if t == "maxmin":
        q = R.choice(["máximo", "mínimo"])
        v = D + A if q == "máximo" else D - A
        return opt("¿Cuál es el valor %s de y = %s?" % (q, f), sg(v), [sg(D - A if q == "máximo" else D + A), str(A), sg(D)],
                   "%s varía entre −1 y 1, así que y va de %s a %s. Valor %s: <b>%s</b>." % (fn.capitalize(), sg(D - A), sg(D + A), q, sg(v)))
    if t == "valor":
        ang, sv, cv = R.choice([(0, "0", "1"), ("π/2", "1", "0"), ("π", "0", "−1"), ("3π/2", "−1", "0"), ("2π", "0", "1"), ("π/6", "1/2", "√3/2"), ("π/3", "√3/2", "1/2")])
        q = R.choice(["sen", "cos"])
        a = sv if q == "sen" else cv
        w = [x for x in ["0", "1", "−1", "1/2", "√3/2", "√2/2"] if x != a]
        return opt("¿Cuánto vale %s(%s)?" % (q, ang), a, R.sample(w, 3), "En el círculo unitario, %s(%s) = <b>%s</b>." % (q, ang, a))
    items = [("La altura de una canastilla de la rueda de la fortuna cambia con el tiempo de forma…", "periódica (se repite cada vuelta)", ["lineal", "exponencial", "constante"], "Se repite en cada vuelta: se modela con seno o coseno."),
             ("¿Qué fenómeno se modela mejor con una función seno?", "la altura de la marea a lo largo del día", ["el crecimiento de una población", "el costo de un taxi", "la caída de un objeto"], "La marea sube y baja de forma repetida."),
             ("Si la temperatura media de un lugar se modela con T(t) = 20 + 8 sen(πt/6) (t en meses), ¿cuál es la temperatura máxima?", "28 °C", ["20 °C", "12 °C", "8 °C"], "20 + 8 = 28 °C."),
             ("En T(t) = 20 + 8 sen(πt/6) (t en meses), ¿cada cuánto se repite el ciclo?", "12 meses", ["6 meses", "8 meses", "20 meses"], "Periodo = 2π ÷ (π/6) = 12."),
             ("Una rueda de la fortuna de 40 m de diámetro tiene su centro a 25 m del suelo. ¿Cuál es la altura mínima de una canastilla?", "5 m", ["25 m", "15 m", "0 m"], "25 − 20 = 5 m."),
             ("El latido del corazón en un electrocardiograma es un ejemplo de fenómeno…", "periódico", ["lineal", "aleatorio sin patrón", "constante"], "Se repite con un ritmo."),
             ("Si un péndulo tarda 2 s en ir y volver, la función que lo describe tiene periodo…", "2 s", ["1 s", "4 s", "π s"], "El periodo es el tiempo de un ciclo completo.")]
    return from_bank(items)


# ============================================================ P14: modelación con ecuaciones diferenciales (plantear, sin resolver)
DE = [("La rapidez con que crece una población es proporcional a la población.", "dP/dt = kP, con k &gt; 0"),
      ("Una sustancia radiactiva se desintegra con una rapidez proporcional a la cantidad que queda.", "dN/dt = −kN, con k &gt; 0"),
      ("Un café se enfría con una rapidez proporcional a la diferencia entre su temperatura y la del cuarto (T<sub>a</sub>).", "dT/dt = −k(T − T<sub>a</sub>)"),
      ("Una población crece proporcionalmente a sí misma, pero frena al acercarse a la capacidad máxima M.", "dP/dt = kP(1 − P/M)"),
      ("Un tinaco se llena con un flujo constante de 20 litros por minuto.", "dV/dt = 20"),
      ("Un objeto cae con aceleración constante g.", "dv/dt = g")]


def q14(*ks):
    t = pick(ks, ["plantear", "ritmo", "euler", "verifica", "concepto"])
    if t == "plantear":
        s, a = R.choice(DE)
        return opt(s + " ¿Qué ecuación diferencial la describe?", a, R.sample([b for _, b in DE if b != a], 3), "La frase «rapidez de cambio» es la derivada: <b>%s</b>." % a)
    if t == "ritmo":
        k = R.choice([0.02, 0.03, 0.05, 0.1, 0.04])
        P = R.choice([1000, 2000, 5000, 10000, 50000])
        neg = R.random() < .4
        v = (-1 if neg else 1) * k * P
        return opt("Una cantidad cumple dP/dt = %s%sP. ¿A qué ritmo cambia cuando P = %s?" % ("−" if neg else "", d2(k, 2), num(P)), d2(v, 0) + " por unidad de tiempo",
                   [d2(-v, 0) + " por unidad de tiempo", num(P) + " por unidad de tiempo", d2(k * P * 2, 0) + " por unidad de tiempo"],
                   "Sustituimos: %s%s × %s = <b>%s</b>." % ("−" if neg else "", d2(k, 2), num(P), d2(v, 0)))
    if t == "euler":
        k = R.choice([0.05, 0.1, 0.2, 0.3, 0.5])
        y0 = R.choice([10, 20, 40, 50, 80, 100, 200])
        h = R.choice([1, 0.5, 0.1])
        y1 = y0 + h * k * y0
        return opt("Para dy/dt = %sy con y(0) = %d, usa un paso de Euler con h = %s: y(h) ≈ y(0) + h × y′(0). ¿Cuánto vale?" % (d2(k, 1), y0, d2(h, 1)), d2(y1, 2),
                   [d2(y0 * k, 2), d2(y0 + k, 2), d2(y0 * (1 + k) ** 2, 2)], "y′(0) = %s × %d = %s; y(h) ≈ %d + %s × %s = <b>%s</b>." % (d2(k, 1), y0, d2(k * y0, 2), y0, d2(h, 1), d2(k * y0, 2), d2(y1, 2)))
    if t == "verifica":
        k = R.choice([2, 3, 5, -1, -2, -4])
        c = R.choice([1, 3, 5, 10])
        ky = lambda v: "y" if v == 1 else MINUS + "y" if v == -1 else sg(v) + "y"
        return opt("¿Qué ecuación diferencial cumple y = %de<sup>%s</sup>?" % (c, (sg(k) + "t") if k not in (1, -1) else ("t" if k == 1 else MINUS + "t")), "y′ = " + ky(k),
                   ["y′ = " + ky(c), "y′ = %s" % sg(k), "y′ = " + ky(-k)], "y′ = %s × %de<sup>…</sup> = %s·y. Por eso las exponenciales modelan crecimiento y decaimiento." % (sg(k), c, sg(k)))
    items = [("Una ecuación diferencial es una ecuación que relaciona…", "una función con sus derivadas", ["dos números", "dos rectas", "una función con su área"], "Por ejemplo dP/dt = 0.03P."),
             ("En el modelo presa-depredador (Lotka-Volterra) se usan…", "dos ecuaciones diferenciales, una para cada población", ["una sola ecuación lineal", "una tabla de frecuencias", "un sistema de desigualdades"], "La rapidez de cambio de cada población depende de las dos."),
             ("En dP/dt = kP, si k &lt; 0 la cantidad…", "decrece", ["crece", "es constante", "se duplica"], "Derivada negativa: la cantidad baja."),
             ("En el modelo logístico, cuando P se acerca a M, el crecimiento…", "se hace cada vez más lento", ["se acelera", "se vuelve negativo de golpe", "no cambia"], "El factor (1 − P/M) se acerca a 0."),
             ("¿Qué fenómeno modela dT/dt = −k(T − T<sub>a</sub>)?", "el enfriamiento de un objeto (ley de Newton)", ["el crecimiento de bacterias", "el interés compuesto", "la caída libre"], "La temperatura se acerca a la del ambiente.")]
    return from_bank(items)


# ============================================================ P15: área bajo la curva y teorema fundamental
def q15(*ks):
    t = pick(ks, ["geo", "riemann", "tfc", "anti", "concepto"])
    if t == "geo":
        m, b = R.randint(0, 3), R.randint(1, 6)
        a, c = sorted(R.sample(range(0, 7), 2))
        A = F(m, 2) * (c * c - a * a) + b * (c - a)
        return opt("Calcula el área bajo f(x) = %s entre x = %d y x = %d (es un trapecio o un rectángulo)." % (poly([m, b]), a, c), show(A) + " u²",
                   [show(F(m * c + b) * (c - a)) + " u²", show(A * 2) + " u²", show(F(m * c + b + m * a + b)) + " u²"],
                   "Área = (f(%d) + f(%d)) ÷ 2 × (%d − %d) = (%d + %d) ÷ 2 × %d = <b>%s u²</b>." % (a, c, c, a, m * a + b, m * c + b, c - a, show(A)))
    if t == "riemann":
        n = R.choice([2, 3, 4])
        b = R.choice([2, 3, 4, 6])
        c = R.choice([1, 2, 3])
        dx = F(b, n)
        side = R.choice(["derecho", "izquierdo"])
        xs = [dx * (i + 1) for i in range(n)] if side == "derecho" else [dx * i for i in range(n)]
        other = [dx * i for i in range(n)] if side == "derecho" else [dx * (i + 1) for i in range(n)]
        S = sum(c * x * x for x in xs) * dx
        exact = F(c * b ** 3, 3)
        fx = "x²" if c == 1 else "%dx²" % c
        return opt("Aproxima el área bajo f(x) = %s entre 0 y %d con %d rectángulos de igual ancho, usando el extremo %s de cada uno." % (fx, b, n, side), show(S) + " u²",
                   [show(exact) + " u²", show(sum(c * x * x for x in other) * dx) + " u²", show(S / dx) + " u²"],
                   "Ancho %s; alturas f(%s). Suma = %s × (%s) = <b>%s u²</b>. Con más rectángulos se acerca a %s." % (show(dx), ", ".join(show(x) for x in xs), show(dx), " + ".join(show(c * x * x) for x in xs), show(S), show(exact)))
    if t == "tfc":
        cs = [nz(-2, 3), R.randint(-4, 4), R.randint(-5, 5)]
        a, b = sorted(R.sample(range(-2, 5), 2))
        d = der(cs)
        v = ev(cs, b) - ev(cs, a)
        return opt("Si F(x) = %s, ¿cuánto vale ∫ de %s a %s de F′(x) dx?" % (poly(cs), sg(a), sg(b)), sg(v), [sg(ev(cs, b)), sg(ev(d, b) - ev(d, a)), sg(ev(cs, b) + ev(cs, a))],
                   "Teorema fundamental: ∫<sub>a</sub><sup>b</sup> F′(x) dx = F(b) − F(a) = %s − %s = <b>%s</b>." % (sg(ev(cs, b)), sg(ev(cs, a)), sg(v)))
    if t == "anti":
        k = R.randint(1, 3)
        cs = [R.randint(1, 4) * (k + 1)] + [R.randint(-6, 6) for _ in range(k)]
        # antiderivada: términos c·x^(n+1)/(n+1)
        n = len(cs) - 1
        terms = [F(c, n - i + 1) for i, c in enumerate(cs)] + [0]
        if any(x.denominator != 1 for x in terms):
            return None
        ok = poly([int(x) for x in terms]) + " + C"
        return opt("¿Cuál es una antiderivada de f(x) = %s?" % poly(cs), ok, [poly(der(cs)) + " + C", poly(cs + [0]) + " + C", poly([int(x) * 2 for x in terms]) + " + C"],
                   "Se sube un grado y se divide entre el nuevo exponente: <b>%s</b>. Comprueba derivando." % ok)
    items = [("El teorema fundamental del cálculo relaciona…", "la derivada y la integral como procesos inversos", ["la suma y la resta", "el seno y el coseno", "la media y la mediana"], "Integrar y derivar se deshacen mutuamente."),
             ("La integral definida de una función positiva entre a y b representa…", "el área bajo la curva entre a y b", ["la pendiente en a", "el valor máximo", "la longitud de la curva"], "Es el límite de las sumas de rectángulos."),
             ("Si v(t) es la velocidad de un carro, ∫ de 0 a 3 de v(t) dt representa…", "la distancia recorrida en 3 horas", ["la aceleración", "la velocidad final", "el tiempo"], "Integrar una razón de cambio da el cambio total."),
             ("Al aumentar el número de rectángulos en una suma de Riemann, la aproximación…", "se acerca al área exacta", ["se aleja", "no cambia", "siempre da 0"], "En el límite se obtiene la integral."),
             ("¿Por qué se escribe + C en una antiderivada?", "porque funciones que difieren en una constante tienen la misma derivada", ["porque C es el área", "porque C siempre vale 1", "por costumbre, no significa nada"], "La derivada de una constante es 0.")]
    return from_bank(items)
