# -*- coding: utf-8 -*-
"""
España Matemáticas I y II (Bachillerato): Límites y continuidad (Sentido algebraico)
build(lv): lv = 1 → «limites-y-continuidad» (Matemáticas I); lv = 2 → «limites-y-continuidad» de 2.º (añade el número e, L'Hôpital y Bolzano).
Límites en un punto y en el infinito, indeterminaciones 0/0, ∞/∞, ∞ − ∞ y 1^∞, asíntotas, continuidad y tipos de discontinuidad, funciones a trozos con parámetro.
Errores: «0/0 = 0», comparar mal los grados en ∞/∞, olvidar los límites laterales.
"""
import math
import random
from fractions import Fraction as F
from es_bach import M, mix, sg, num, unit, L, E, P2, poly, nf, fq, kurve, BLUE, W, MINUS

R = None
LV = 1
INF, MINF = "+∞", MINUS + "∞"


def lim(a, f):
    return "lím<sub>x→%s</sub> %s" % (a, f)


def s_directo():
    t = R.choice(["poli", "rac", "lat", "lat", "inf"])
    a = R.randint(-3, 4)
    if t == "poli":
        c = [R.randint(-3, 3) for _ in range(3)]
        c[0] = c[0] or 1
        v = c[0] * a * a + c[1] * a + c[2]
        return M("Calcula %s." % lim(sg(a), "(%s)" % P2(*c)), sg(v), W([sg(v + 1), sg(-v) if v else "1", "no existe", "+∞"]), "Es un polinomio: basta sustituir x = %s. <b>%s</b>." % (sg(a), sg(v)))
    if t == "rac":
        b = R.randint(1, 5)
        k = R.randint(1, 6)
        d0 = a + b
        if d0 == 0:
            return None
        v = F(a * a + k, d0)
        return M("Calcula %s." % lim(sg(a), "(x² + %d)/(x + %d)" % (k, b)), nf(v), W([nf(F(k, b)), "0", "+∞", nf(v + 1)]), "El denominador no se anula: sustituimos, (%d + %d)/%d = <b>%s</b>." % (a * a, k, d0, nf(v)))
    if t == "lat":
        b = R.randint(-3, 3)
        k = R.choice([1, 2, 3, -1, -2])
        side = R.choice(["+", "−"])
        pos = (k > 0) == (side == "+")
        ok = INF if pos else MINF
        return M("Calcula %s." % ("lím<sub>x→%s<sup>%s</sup></sub> %s/(%s)" % (sg(b), side, sg(k), E((1, "x"), (-b, "")))), ok, [MINF if pos else INF, "0", "no existe"], "Cerca de %s por la %s, x − %s es %s y el numerador %s: <b>%s</b>." % (sg(b), "derecha" if side == "+" else "izquierda", sg(b), "positivo" if side == "+" else "negativo", "positivo" if k > 0 else "negativo", ok))
    k = R.choice(["exp", "expn", "ln", "frac"])
    q, a_, w = {"exp": (lim("+∞", "e<sup>x</sup>"), INF, ["0", MINF, "1"]), "expn": (lim(MINF, "e<sup>x</sup>"), "0", [INF, MINF, "1"]), "ln": (lim("0<sup>+</sup>", "ln x"), MINF, ["0", INF, "1"]), "frac": (lim("+∞", "5/x²"), "0", [INF, "5", "no existe"])}[k]
    return M("Calcula %s." % q, a_, w, "Respuesta: <b>%s</b>." % a_)


def s_infinito():
    t = R.choice(["igual", "igual", "menor", "mayor", "raiz"])
    a, b = R.randint(1, 6), R.randint(1, 6)
    if t == "igual":
        n = R.randint(1, 3)
        num_ = poly([a] + [R.randint(-5, 5) for _ in range(n)])
        den = poly([b] + [R.randint(-5, 5) for _ in range(n)])
        v = F(a, b)
        return M("Calcula %s." % lim("+∞", "(%s)/(%s)" % (num_, den)), nf(v), W([nf(F(b, a)), "0", INF, "1", nf(F(a + 1, b)), nf(F(a, b + 1))]), "Mismo grado: cociente de los coeficientes principales, %d/%d = <b>%s</b>." % (a, b, nf(v)))
    if t == "menor":
        return M("Calcula %s." % lim("+∞", "(%s)/(%s)" % (poly([a, R.randint(-5, 5)]), poly([b, 0, R.randint(-5, 5)]))), "0", [nf(F(a, b)), INF, "1"], "El grado del denominador es mayor: <b>0</b>.")
    if t == "mayor":
        s = R.choice([1, -1])
        ok = INF if s > 0 else MINF
        return M("Calcula %s." % lim("+∞", "(%s)/(%s)" % (poly([s * a, 0, R.randint(-5, 5)]), poly([b, R.randint(-5, 5)]))), ok, [MINF if s > 0 else INF, nf(F(s * a, b)), "0"], "El grado del numerador es mayor: el límite es infinito con el signo de %s/%d: <b>%s</b>." % (sg(s * a), b, ok))
    k = R.choice([1, 4, 9])
    rt = int(math.isqrt(k))
    return M("Calcula %s." % lim("+∞", "√(%sx² + 1)/(%dx − 3)" % ("" if k == 1 else k, b)), nf(F(rt, b)), W([nf(F(k, b)), "0", INF, nf(F(1, b))]), "√(%sx²) = %sx: %s/%d = <b>%s</b>." % ("" if k == 1 else k, rt if rt > 1 else "", rt, b, nf(F(rt, b))))


def s_indet():
    t = R.choice(["00", "00", "00", "conj", "resta", "e"] if LV >= 2 else ["00", "00", "00", "conj", "resta"])
    if t == "00":
        a = R.randint(-4, 4)
        b = R.choice([x for x in range(-5, 6) if x != a])
        c = R.choice([x for x in range(-5, 6) if x != a])
        num_ = P2(1, -(a + b), a * b)
        den = P2(1, -(a + c), a * c)
        v = F(a - b, a - c)
        return M("Calcula %s." % lim(sg(a), "(%s)/(%s)" % (num_, den)), nf(v), W(["0", "no existe", nf(F(b, c)) if c else "1", nf(-v) if v else "1"]), "0/0: factorizamos y simplificamos (x − %s): (%s − %s)/(%s − %s) = <b>%s</b>." % (sg(a), sg(a), "(%s)" % sg(b) if b < 0 else sg(b), sg(a), "(%s)" % sg(c) if c < 0 else sg(c), nf(v)))
    if t == "conj":
        k = R.choice([1, 4, 9, 16, 25])
        r = int(math.isqrt(k))
        v = F(1, 2 * r)
        return M("Calcula %s." % lim(str(k), "(√x − %d)/(x − %d)" % (r, k)), nf(v), W(["0", "1", nf(F(1, r)), nf(F(r, 2))]), "Multiplicamos por el conjugado √x + %d: queda 1/(√x + %d) → <b>%s</b>." % (r, r, nf(v)))
    if t == "resta":
        a = R.randint(1, 8)
        return M("Calcula %s." % lim("+∞", "(√(x² + %dx) − x)" % a), nf(F(a, 2)), W(["0", INF, nf(F(a, 1)), "1"]), "∞ − ∞: multiplicamos y dividimos por el conjugado → %dx/(√(x² + %dx) + x) → <b>%s</b>." % (a, a, nf(F(a, 2))))
    k = R.randint(2, 6)
    return M("Calcula %s." % lim("+∞", "(1 + 1/x)<sup>%dx</sup>" % k), "e<sup>%d</sup>" % k, ["1", "e", INF], "Indeterminación 1<sup>∞</sup>: (1 + 1/x)<sup>x</sup> → e, así que el límite es <b>e<sup>%d</sup></b>." % k)


def s_asintotas():
    t = R.choice(["vert", "vert", "hor", "obl", "ninguna"] if LV >= 1 else ["vert"])
    a = R.randint(-5, 5)
    k = R.randint(1, 6)
    if t == "vert":
        b = R.choice([x for x in range(-5, 6) if x != a])
        return M("¿Qué asíntotas verticales tiene f(x) = (x + %d)/(%s)?" % (k, P2(1, -(a + b), a * b)), "x = %s y x = %s" % (sg(min(a, b)), sg(max(a, b))) if -k not in (a, b) else "x = %s" % sg(a if -k == b else b),
                 W(["x = %s y x = %s" % (sg(-max(a, b)), sg(-min(a, b))), "y = %s" % sg(a * b), "x = %s" % sg(-k), "no tiene"]), "Valores que anulan el denominador (y no el numerador): <b>%s</b>." % ("x = %s y x = %s" % (sg(min(a, b)), sg(max(a, b))) if -k not in (a, b) else "x = %s" % sg(a if -k == b else b)))
    if t == "hor":
        p, q = R.randint(1, 6), R.randint(1, 4)
        return M("¿Qué asíntota horizontal tiene f(x) = (%s)/(%s)?" % (E((p, "x"), (k, "")), E((q, "x"), (-a, ""))), "y = %s" % nf(F(p, q)), W(["x = %s" % nf(F(a, q)), "y = %s" % nf(F(q, p)), "y = 0", "y = %s" % nf(F(-k, a)) if a else "y = 1"]), "lím en ∞ = %d/%d: <b>y = %s</b>." % (p, q, nf(F(p, q))))
    if t == "obl":
        m, n = R.randint(1, 3), R.randint(-4, 4)
        # (m x² + (n − m a) x + c)/(x − a) = m x + n + r/(x − a)
        rr = R.choice([1, 2, 3, -2])
        c = rr - n * (-a) if False else rr - (-a) * n
        num_ = poly([m, n - m * a, -n * a + rr])
        return M("¿Qué asíntota oblicua tiene f(x) = (%s)/(%s)?" % (num_, E((1, "x"), (-a, ""))), "y = %s" % E((m, "x"), (n, "")), W(["y = %s" % E((m, "x"), (-n, "")) if n else "y = %s" % E((m, "x"), (1, "")), "y = %dx" % m if n else "y = %s" % E((m, "x"), (2, "")), "x = %s" % sg(a), "y = %s" % E((m + 1, "x"), (n, ""))]),
                 "Dividimos: cociente %s. <b>y = %s</b>." % (E((m, "x"), (n, "")), E((m, "x"), (n, ""))))
    return M("¿Tiene asíntotas verticales f(x) = 1/(x² + %d)?" % k, "no, el denominador nunca es 0", ["sí, x = %s" % sg(-k), "sí, x = 0", "sí, x = ±%d" % k], "x² + %d &gt; 0 siempre: <b>no tiene</b>." % k)


def s_continuidad():
    t = R.choice(["param", "param", "tipo", "tipo", "bolzano"] if LV >= 2 else ["param", "param", "tipo", "tipo", "graf"])
    if t == "param":
        x0 = R.randint(-2, 3)
        b, c = R.randint(1, 4), R.randint(-3, 3)
        k = x0 * x0 + c - b * x0
        return M("¿Qué valor de k hace continua f(x) = %s + k si x &lt; %s; f(x) = %s si x ≥ %s?" % (E((b, "x")), sg(x0), P2(1, 0, c), sg(x0)), "k = %s" % sg(k), W(["k = %s" % sg(-k) if k else "k = 1", "k = %s" % sg(x0 * x0 + c), "k = %s" % sg(k + b), "k = %s" % sg(k - 1)]),
                 "Límites laterales iguales en x = %s: %s + k = %s → <b>k = %s</b>." % (sg(x0), sg(b * x0), sg(x0 * x0 + c), sg(k)))
    if t == "tipo":
        a = R.randint(-4, 4)
        b = R.choice([x for x in range(-4, 5) if x != a])
        k = R.choice(["evitable", "infinito", "salto"])
        if k == "evitable":
            f = "(%s)/(%s)" % (P2(1, -(a + b), a * b), E((1, "x"), (-a, "")))
            ok = "evitable"
        elif k == "infinito":
            f = "%d/(%s)" % (R.randint(1, 5), E((1, "x"), (-a, "")))
            ok = "de salto infinito (asíntota vertical)"
        else:
            f = "|%s|/(%s)" % (E((1, "x"), (-a, "")), E((1, "x"), (-a, "")))
            ok = "de salto finito"
        return M("¿Qué tipo de discontinuidad tiene f(x) = %s en x = %s?" % (f, sg(a)), ok, [o for o in ["evitable", "de salto infinito (asíntota vertical)", "de salto finito", "es continua"] if o != ok], "Calculamos los límites laterales en x = %s: <b>%s</b>." % (sg(a), ok))
    if t == "bolzano":
        a, b = R.randint(0, 2), R.randint(2, 4)
        f = R.choice(["x³ + x − 3", "x³ − 2x − 1", "e<sup>x</sup> − 3", "x³ + 2x − 10", "ln x + x − 2"])
        q, aa, w = R.choice([("El teorema de Bolzano asegura que si f es continua en [a, b] y f(a) y f(b) tienen signos distintos…", "f tiene al menos un cero en (a, b)", ["f tiene un máximo en (a, b)", "f es creciente", "f(a) = f(b)"]),
                             ("¿Qué hace falta para aplicar Bolzano a f en [a, b]?", "f continua en [a, b] y f(a) · f(b) &lt; 0", ["f derivable y f(a) = f(b)", "f creciente", "f(a) = 0"]),
                             ("f(x) = x³ + x − 3 cumple f(1) = −1 y f(2) = 7. ¿Qué se puede asegurar?", "que se anula entre 1 y 2", ["que se anula en x = 1,5", "que no tiene ceros", "que tiene un máximo en (1, 2)"])])
        return M(q, aa, w, "Respuesta: <b>%s</b>." % aa)
    a = R.randint(-3, 3)
    fn = lambda x: 1 / (x - a) if abs(x - a) > 0.15 else None
    pic = kurve([(fn, BLUE, "")], (-6, 6, 1), (-5, 5, 1), W=330, H=280, label="gráfica con una asíntota vertical")
    return M(pic + "¿En qué punto es discontinua la función de la gráfica?", "x = %s" % sg(a), W(["x = %s" % sg(-a) if a else "x = 1", "y = 0", "x = 0" if a else "x = 2", "es continua"]), "La gráfica se rompe en la asíntota vertical: <b>x = %s</b>." % sg(a))


def s_lhopital():
    t = R.choice(["sen", "exp", "ln", "pol"])
    k = R.randint(2, 6)
    q, a, w = {"sen": (lim("0", "sen (%dx)/x" % k), str(k), ["1", "0", "1/%d" % k]), "exp": (lim("0", "(e<sup>%dx</sup> − 1)/x" % k), str(k), ["1", "0", "e<sup>%d</sup>" % k]),
               "ln": (lim("1", "ln x/(x − 1)"), "1", ["0", INF, "e"]), "pol": (lim("+∞", "x<sup>%d</sup>/e<sup>x</sup>" % k), "0", [INF, "1", str(k)])}[t]
    return M("Calcula %s." % q, a, w, "Indeterminación: aplicamos la regla de L'Hôpital (derivamos numerador y denominador): <b>%s</b>." % a)


def build(lv):
    global R, LV
    LV = lv
    R = random.Random(51011 + (lv - 1) * 1000)
    seen = set()
    sets = [("Límites directos y laterales", mix(R, seen, [(s_directo, 20)])), ("Límites en el infinito", mix(R, seen, [(s_infinito, 20)])),
            ("Indeterminaciones", mix(R, seen, [(s_indet, 20)] if lv == 1 else [(s_indet, 12), (s_lhopital, 8)])), ("Asíntotas", mix(R, seen, [(s_asintotas, 20)])), ("Continuidad", mix(R, seen, [(s_continuidad, 20)]))]
    think = ["El <b>límite</b> de f en a es el valor al que se acerca f(x) cuando x se acerca a a. Si los límites laterales no coinciden, no existe.",
             "En el infinito, en un cociente de polinomios mandan los términos de mayor grado.",
             "<b>Indeterminaciones</b>: 0/0 (se factoriza y simplifica), ∞/∞ (se comparan grados), ∞ − ∞ (conjugado)%s." % (", 1<sup>∞</sup> (número e) y la regla de L'Hôpital" if lv >= 2 else ""),
             "f es <b>continua</b> en a si existe f(a), existe el límite y coinciden."]
    ex = [("lím<sub>x→2</sub> (x² − 4)/(x − 2)", ["0/0", "(x − 2)(x + 2)/(x − 2)"], "4"), ("lím<sub>x→∞</sub> (3x² + 1)/(2x² − x)", ["mismo grado"], "3/2")]
    mist = [["Decir que 0/0 = 0", "Es una indeterminación: hay que simplificar."], ["Comparar mal los grados", "Mira el exponente mayor arriba y abajo."], ["Olvidar los límites laterales", "En las funciones a trozos y en las asíntotas son clave."]]
    body = L(think, ex, mist, kurve([(lambda x: (2 * x + 1) / (x - 1) if abs(x - 1) > 0.12 else None, BLUE, "")], (-5, 6, 1), (-5, 7, 1), W=330, H=280, label="función con asíntotas x = 1 e y = 2"))
    faq = [("¿Qué es una indeterminación?", "Una expresión como 0/0 o ∞/∞ cuyo valor no se conoce a primera vista; hay que transformar la función para calcular el límite."),
           ("¿Cuántas asíntotas horizontales puede tener una función?", "Como mucho dos: una en +∞ y otra en −∞. Si tiene horizontal en un lado, no tiene oblicua en ese lado.")]
    if lv == 1:
        unit(1, R, "limites-y-continuidad", "A", "Límites de funciones: cálculo, indeterminaciones, asíntotas; continuidad y tipos de discontinuidad",
             "Límites y continuidad", "Límites y continuidad", "Fichas de Matemáticas I (1.º de Bachillerato): límites, límites laterales, indeterminaciones, asíntotas y continuidad. 100 ejercicios con soluciones.",
             "0/0: factoriza y simplifica", "∞/∞: compara los grados.", body, faq, sets, 11)
    else:
        unit(2, R, "limites-y-continuidad", "A", "Límites de funciones: indeterminaciones, número e, regla de L'Hôpital; continuidad y teorema de Bolzano",
             "Límites y continuidad", "Límites y continuidad", "Fichas de Matemáticas II (2.º de Bachillerato): límites, indeterminaciones, número e, L'Hôpital, asíntotas, continuidad y Bolzano. 100 ejercicios.",
             "0/0 o ∞/∞: L'Hôpital", "Bolzano: cambio de signo → hay un cero.", body, faq, sets, 7)


if __name__ == "__main__":
    build(1)
