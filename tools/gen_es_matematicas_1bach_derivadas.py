# -*- coding: utf-8 -*-
"""
España Matemáticas I y II (Bachillerato): Derivadas (Sentido algebraico)
build(lv): lv = 1 → «derivadas» (Matemáticas I); lv = 2 → «derivadas» de 2.º (regla de la cadena más compleja, derivabilidad de funciones a trozos, derivadas sucesivas, derivación logarítmica).
Tasa de variación media, derivada en un punto por la definición, reglas de derivación (potencias, exponenciales, logaritmos, trigonométricas), producto y cociente, regla de la cadena, recta tangente.
Errores: (f · g)′ = f′ · g′, olvidar multiplicar por la derivada de dentro en la cadena, (ln x)′ = 1/x pero (ln 3x)′ también es 1/x.
"""
import random
from fractions import Fraction as F
from es_bach import M, mix, sg, num, unit, L, E, P2, poly, nf, fq, kurve, BLUE, RED, W, MINUS, sup

R = None
LV = 1


def dpoly(cs):
    n = len(cs) - 1
    return [c * (n - i) for i, c in enumerate(cs[:-1])]


def ev(cs, x):
    v = 0
    for c in cs:
        v = v * x + c
    return v


def kx(k, v="x"):
    return v if k == 1 else (MINUS + v if k == -1 else "%d%s" % (k, v))


def s_tvm():
    t = R.choice(["tvm", "tvm", "def", "def", "interp"])
    cs = [R.choice([1, 2, -1, 3]), R.randint(-5, 5), R.randint(-6, 6)]
    if t == "tvm":
        a, b = sorted(R.sample(range(-3, 5), 2))
        v = F(ev(cs, b) - ev(cs, a), b - a)
        return M("Calcula la tasa de variación media de f(x) = %s en [%s, %s]." % (poly(cs), sg(a), sg(b)), nf(v), W([sg(ev(cs, b) - ev(cs, a)), nf(F(b - a, ev(cs, b) - ev(cs, a))) if ev(cs, b) != ev(cs, a) else "1", nf(ev(dpoly(cs), a)) if ev(dpoly(cs), a) != v else nf(v + 1), nf(-v) if v else "2"]),
                 "TVM = (f(%s) − f(%s)) / (%s − %s) = (%s − %s)/%d = <b>%s</b>." % (sg(b), sg(a), sg(b), "(%s)" % sg(a) if a < 0 else sg(a), sg(ev(cs, b)), "(%s)" % sg(ev(cs, a)) if ev(cs, a) < 0 else sg(ev(cs, a)), b - a, nf(v)))
    if t == "def":
        a = R.randint(-3, 4)
        v = ev(dpoly(cs), a)
        return M("Usando la definición f′(a) = lím<sub>h→0</sub> (f(a + h) − f(a))/h, calcula f′(%s) para f(x) = %s." % (sg(a), poly(cs)), sg(v), W([sg(ev(cs, a)), sg(v + cs[0]), sg(2 * a + cs[1]) if 2 * a + cs[1] != v else sg(v - 1), "0" if v else "1"]),
                 "(f(%s + h) − f(%s))/h = %s + %sh → al tender h a 0 queda <b>%s</b>." % (sg(a), sg(a), sg(v), "" if cs[0] == 1 else sg(cs[0]), sg(v)))
    q, a_, w = R.choice([("¿Qué representa f′(a) en la gráfica de f?", "la pendiente de la recta tangente en x = a", ["el valor de f en a", "el área bajo la curva", "el punto de corte con el eje Y"]),
                         ("Si s(t) es la posición de un móvil, ¿qué es s′(t)?", "la velocidad", ["la aceleración", "la distancia total", "el tiempo"]),
                         ("Si f′(a) &gt; 0, la función en x = a es…", "creciente", ["decreciente", "constante", "discontinua"]),
                         ("¿Qué función no es derivable en x = 0?", "f(x) = |x|", ["f(x) = x²", "f(x) = e<sup>x</sup>", "f(x) = sen x"]),
                         ("Si una función es derivable en a, entonces en a es…", "continua", ["discontinua", "creciente", "cero"])])
    return M(q, a_, w, "Respuesta: <b>%s</b>." % a_)


def s_reglas():
    t = R.choice(["poli", "poli", "pot", "raiz", "elem", "elem"])
    if t == "poli":
        cs = [R.choice([1, 2, 3, -1, -2, 4]), R.randint(-6, 6), R.randint(-6, 6), R.randint(-9, 9)]
        d_ = dpoly(cs)
        return M("Deriva f(x) = %s." % poly(cs), "f′(x) = %s" % poly(d_), W(["f′(x) = %s" % poly([c for c in cs[:-1]]), "f′(x) = %s" % poly(d_[:-1] + [d_[-1] + cs[-1]]) if cs[-1] else "f′(x) = %s" % poly(d_ + [0]), "f′(x) = %s" % poly([3 * cs[0], cs[1], cs[2]])]),
                 "Derivamos término a término (axⁿ → n·a·xⁿ⁻¹; la constante desaparece): <b>%s</b>." % poly(d_))
    if t == "pot":
        n = R.randint(2, 5)
        k = R.randint(1, 6)
        return M("Deriva f(x) = %d/x%s." % (k, sup(n) if n > 1 else ""), "f′(x) = %s/x%s" % (sg(-k * n), sup(n + 1)), W(["f′(x) = %s/x%s" % (sg(k * n), sup(n + 1)), "f′(x) = %s/x%s" % (sg(-k * n), sup(n - 1)) if n > 1 else "f′(x) = %d" % k, "f′(x) = %d/x%s" % (k, sup(n - 1)) if n > 1 else "f′(x) = 0"]),
                 "%d/x%s = %dx<sup>−%d</sup> → derivada %sx<sup>−%d</sup> = <b>%s/x%s</b>." % (k, sup(n), k, n, sg(-k * n), n + 1, sg(-k * n), sup(n + 1)))
    if t == "raiz":
        k = R.randint(1, 6)
        return M("Deriva f(x) = %s√x." % ("" if k == 1 else k), "f′(x) = %s" % (("1/(2√x)" if k == 1 else ("%s/√x" % nf(F(k, 2)) if k % 2 == 0 else "%d/(2√x)" % k))), W(["f′(x) = %s√x" % (nf(F(k, 2)) if k != 2 else ""), "f′(x) = %d/√x" % (2 * k), "f′(x) = %s/(2x)" % ("" if k == 1 else k) if k > 1 else "f′(x) = 1/x"]),
                 "√x = x<sup>1/2</sup> → (1/2)x<sup>−1/2</sup> = 1/(2√x). <b>Multiplicado por %d</b>." % k)
    k = R.randint(2, 7)
    q, a_, w = R.choice([("%de<sup>x</sup>" % k, "%de<sup>x</sup>" % k, ["%dxe<sup>x − 1</sup>" % k, "e<sup>x</sup>", "%de<sup>x − 1</sup>" % k]), ("%d ln x" % k, "%d/x" % k, ["%d" % k, "1/(%dx)" % k, "%d ln x/x" % k]),
                         ("%d sen x" % k, "%d cos x" % k, ["%s sen x" % sg(-k), "%s cos x" % sg(-k), "cos %dx" % k]), ("%d cos x" % k, "%s sen x" % sg(-k), ["%d sen x" % k, "%s cos x" % sg(-k), "sen %dx" % k]),
                         ("%d<sup>x</sup>" % k, "%d<sup>x</sup> · ln %d" % (k, k), ["x · %d<sup>x − 1</sup>" % k, "%d<sup>x</sup>" % k, "%d<sup>x</sup>/ln %d" % (k, k)]), ("log<sub>%d</sub> x" % k, "1/(x ln %d)" % k, ["1/x", "ln %d/x" % k, "%d/x" % k])])
    return M("Deriva f(x) = %s." % q, "f′(x) = " + a_, ["f′(x) = " + x for x in w], "Derivada inmediata: <b>%s</b>." % a_)


def s_prod():
    t = R.choice(["prod", "prod", "coc", "coc"])
    a = R.randint(-5, 5)
    if t == "prod":
        k = R.choice(["xe", "xln", "x2e", "xsen"])
        q, ok, w = {"xe": ("x · e<sup>x</sup>", "e<sup>x</sup>(x + 1)", ["e<sup>x</sup>", "x · e<sup>x</sup>", "e<sup>x</sup>(x − 1)"]), "xln": ("x · ln x", "ln x + 1", ["1/x", "ln x", "x/x"]),
                    "x2e": ("x² · e<sup>x</sup>", "e<sup>x</sup>(x² + 2x)", ["2x · e<sup>x</sup>", "e<sup>x</sup>(x² + 2)", "x² · e<sup>x</sup>"]), "xsen": ("x · sen x", "sen x + x cos x", ["cos x", "x cos x", "sen x − x cos x"])}[k]
        return M("Deriva f(x) = %s." % q, "f′(x) = " + ok, ["f′(x) = " + x for x in w], "(f · g)′ = f′g + fg′: <b>%s</b>." % ok)
    if a == 0:
        return None
    b = R.choice([x for x in range(-5, 6) if x not in (a, 0)])
    nume = E((1, "x"), (-a, ""))
    den = E((1, "x"), (-b, ""))
    r = a - b
    ok = "%s/(%s)²" % (sg(r), den)
    return M("Deriva f(x) = (%s)/(%s)." % (nume, den), "f′(x) = " + ok, W(["f′(x) = %s/(%s)²" % (sg(-r), den), "f′(x) = 1", "f′(x) = %s/(%s)" % (sg(r), den), "f′(x) = %s/(%s)²" % (sg(a + b) if a + b else "1", den)]),
             "(f/g)′ = (f′g − fg′)/g² = ((%s) − (%s))/(%s)² = <b>%s</b>." % (den, nume, den, ok))


def s_cadena():
    t = R.choice(["exp", "ln", "sen", "pot", "raiz", "comp"] if LV >= 2 else ["exp", "ln", "sen", "pot", "raiz"])
    a, b = R.randint(2, 6), R.randint(-5, 5)
    inner = E((a, "x"), (b, ""))
    if t == "exp":
        return M("Deriva f(x) = e<sup>%s</sup>." % inner, "f′(x) = %de<sup>%s</sup>" % (a, inner), ["f′(x) = e<sup>%s</sup>" % inner, "f′(x) = (%s)e<sup>%s</sup>" % (inner, E((a, "x"), (b - 1, ""))), "f′(x) = %de<sup>%s</sup>" % (a, E((a - 1, "x"), (b, "")))], "Cadena: e<sup>u</sup> · u′ con u′ = %d: <b>%de<sup>%s</sup></b>." % (a, a, inner))
    if t == "ln":
        ok = "%d/(%s)" % (a, inner)
        return M("Deriva f(x) = ln (%s)." % inner, "f′(x) = " + ok, ["f′(x) = 1/(%s)" % inner, "f′(x) = %d" % a, "f′(x) = 1/x"], "u′/u = <b>%s</b>." % ok)
    if t == "sen":
        k = R.choice(["sen", "cos"])
        ok = ("%d cos (%s)" % (a, inner)) if k == "sen" else ("%s sen (%s)" % (sg(-a), inner))
        return M("Deriva f(x) = %s (%s)." % (k, inner), "f′(x) = " + ok, W(["f′(x) = cos (%s)" % inner if k == "sen" else "f′(x) = %s sen (%s)" % (MINUS, inner), "f′(x) = %d cos x" % a if k == "sen" else "f′(x) = %d sen (%s)" % (a, inner), "f′(x) = %s cos (%s)" % (sg(-a), inner) if k == "sen" else "f′(x) = %d cos (%s)" % (a, inner)]), "Cadena: <b>%s</b>." % ok)
    if t == "pot":
        n = R.randint(2, 6)
        ok = "%d(%s)%s" % (n * a, inner, sup(n - 1) if n > 2 else "")
        return M("Deriva f(x) = (%s)%s." % (inner, sup(n)), "f′(x) = " + ok, W(["f′(x) = %d(%s)%s" % (n, inner, sup(n - 1) if n > 2 else ""), "f′(x) = %d(%s)%s" % (n * a, inner, sup(n)), "f′(x) = %d" % (n * a), "f′(x) = %d(%s)%s" % (a, inner, sup(n - 1) if n > 2 else "")]), "n · u<sup>n−1</sup> · u′ = %d · (%s)%s · %d = <b>%s</b>." % (n, inner, sup(n - 1) if n > 2 else "", a, ok))
    if t == "raiz":
        ok = "%s/√(%s)" % (nf(F(a, 2)), inner) if a % 2 == 0 else "%d/(2√(%s))" % (a, inner)
        return M("Deriva f(x) = √(%s)." % inner, "f′(x) = " + ok, W(["f′(x) = 1/(2√(%s))" % inner, "f′(x) = %d/√(%s)" % (a, inner), "f′(x) = %d√(%s)" % (a, inner)]), "u′/(2√u): <b>%s</b>." % ok)
    q, a_, w = R.choice([("e<sup>x²</sup>", "2x · e<sup>x²</sup>", ["e<sup>x²</sup>", "x² · e<sup>x²−1</sup>", "2e<sup>x²</sup>"]), ("ln (x² + 1)", "2x/(x² + 1)", ["1/(x² + 1)", "2x", "1/(2x)"]),
                         ("sen² x", "2 sen x cos x", ["2 sen x", "cos² x", "2 cos x"]), ("e<sup>sen x</sup>", "cos x · e<sup>sen x</sup>", ["e<sup>sen x</sup>", "sen x · e<sup>cos x</sup>", "e<sup>cos x</sup>"]),
                         ("x<sup>x</sup>", "x<sup>x</sup>(ln x + 1)", ["x · x<sup>x − 1</sup>", "x<sup>x</sup> ln x", "x<sup>x</sup>"]), ("ln (sen x)", "cos x / sen x", ["1/sen x", "cos x", "ln (cos x)"])])
    return M("Deriva f(x) = %s." % q, "f′(x) = " + a_, ["f′(x) = " + x for x in w], "Regla de la cadena (o derivación logarítmica): <b>%s</b>." % a_)


def s_tangente():
    t = R.choice(["tg", "tg", "tg", "horiz", "pend"] if LV == 1 else ["tg", "tg", "horiz", "deriv2", "trozos"])
    cs = [R.choice([1, -1, 2]), R.randint(-5, 5), R.randint(-6, 6)]
    if t == "tg":
        a = R.randint(-3, 3)
        m, y0 = ev(dpoly(cs), a), ev(cs, a)
        n = y0 - m * a
        ok = "y = %s" % E((m, "x"), (n, "")) if m or n else "y = 0"
        return M("Halla la recta tangente a f(x) = %s en x = %s." % (poly(cs), sg(a)), ok, W(["y = %s" % E((y0, "x"), (m, "")) if y0 else "y = %s" % sg(m), "y = %s" % E((m, "x"), (y0, "")) if y0 != n else "y = %s" % E((m, "x"), (n + 1, "")), "y = %s" % E((-m, "x"), (n, "")) if m else "y = %s" % sg(n + 2), "y = %s" % E((m, "x"), (-n, "")) if n else "y = %s" % E((m, "x"), (1, ""))]),
                 "f(%s) = %s y f′(%s) = %s → %s = %s(%s) → <b>%s</b>." % (sg(a), sg(y0), sg(a), sg(m), E((1, "y"), (-y0, "")), sg(m), E((1, "x"), (-a, "")), ok))
    if t == "horiz":
        a = cs[0]
        x0 = F(-cs[1], 2 * a)
        return M("¿En qué punto tiene f(x) = %s la tangente horizontal?" % poly(cs), "x = %s" % nf(x0), W(["x = %s" % nf(-x0) if x0 else "x = 1", "x = %s" % nf(F(-cs[1], a)) if cs[1] else "x = 2", "x = %s" % nf(F(cs[1], 2 * a)) if cs[1] else "x = −1", "x = %s" % nf(x0 + 1)]), "f′(x) = %s = 0 → <b>x = %s</b>." % (poly(dpoly(cs)), nf(x0)))
    if t == "pend":
        m = R.randint(-6, 6)
        x0 = F(m - cs[1], 2 * cs[0])
        return M("¿En qué punto la tangente a f(x) = %s tiene pendiente %s?" % (poly(cs), sg(m)), "x = %s" % nf(x0), W(["x = %s" % nf(F(m, 2 * cs[0])) if F(m, 2 * cs[0]) != x0 else "x = %s" % nf(x0 + 1), "x = %s" % sg(m), "x = %s" % nf(-x0) if x0 else "x = 1"]), "f′(x) = %s = %s → <b>x = %s</b>." % (poly(dpoly(cs)), sg(m), nf(x0)))
    if t == "deriv2":
        c4 = [R.randint(1, 3), R.randint(-4, 4), R.randint(-4, 4), R.randint(-4, 4), R.randint(-5, 5)]
        d2 = dpoly(dpoly(c4))
        return M("Calcula la derivada segunda de f(x) = %s." % poly(c4), "f″(x) = %s" % poly(d2), W(["f″(x) = %s" % poly(dpoly(c4)), "f″(x) = %s" % poly(dpoly(d2)), "f″(x) = %s" % poly([d2[0], d2[1], d2[2] + 1])]), "Derivamos dos veces: <b>%s</b>." % poly(d2))
    x0, b = R.randint(-2, 2), R.randint(1, 4)
    # f = x² si x ≤ x0 ; ax + c si x > x0 → derivable: a = 2x0, c = x0² − a x0
    a = 2 * x0
    c = x0 * x0 - a * x0
    return M("¿Qué valores de a y b hacen derivable f(x) = x² si x ≤ %s; ax + b si x &gt; %s?" % (sg(x0), sg(x0)), "a = %s, b = %s" % (sg(a), sg(c)), W(["a = %s, b = %s" % (sg(x0), sg(x0 * x0 - x0 * x0)), "a = %s, b = %s" % (sg(a), sg(-c)) if c else "a = %s, b = 1" % sg(a), "a = %s, b = %s" % (sg(x0 * x0), sg(0)), "a = 1, b = %s" % sg(x0 * x0 - x0)]),
             "Continua: %s = %sa + b; derivable: 2 · %s = a → a = %s, b = %s. <b>a = %s, b = %s</b>." % (sg(x0 * x0), sg(x0), sg(x0), sg(a), sg(c), sg(a), sg(c)))


def build(lv):
    global R, LV
    LV = lv
    R = random.Random(51012 + (lv - 1) * 1000)
    seen = set()
    sets = [("Tasa de variación y definición", mix(R, seen, [(s_tvm, 20)])), ("Derivadas inmediatas", mix(R, seen, [(s_reglas, 20)])), ("Producto y cociente", mix(R, seen, [(s_prod, 20)])),
            ("Regla de la cadena", mix(R, seen, [(s_cadena, 20)])), ("Recta tangente" if lv == 1 else "Tangente, derivabilidad y derivadas sucesivas", mix(R, seen, [(s_tangente, 20)]))]
    think = ["La <b>derivada</b> f′(a) es la pendiente de la recta tangente en x = a: f′(a) = lím<sub>h→0</sub> (f(a + h) − f(a))/h.",
             "Reglas: (xⁿ)′ = n·xⁿ⁻¹; (eˣ)′ = eˣ; (ln x)′ = 1/x; (sen x)′ = cos x; (cos x)′ = −sen x.",
             "Producto: (f·g)′ = f′g + fg′. Cociente: (f/g)′ = (f′g − fg′)/g². <b>Cadena</b>: (f(g(x)))′ = f′(g(x)) · g′(x).",
             "Recta tangente en x = a: y − f(a) = f′(a)(x − a)."]
    ex = [("f(x) = (3x − 1)⁴", ["4(3x − 1)³ · 3"], "f′(x) = 12(3x − 1)³"), ("Tangente a x² en x = 1", ["f(1) = 1, f′(1) = 2"], "y = 2x − 1")]
    mist = [["(f · g)′ = f′ · g′", "Falso: es f′g + fg′."], ["Olvidar la derivada de dentro", "(e<sup>3x</sup>)′ = 3e<sup>3x</sup>."], ["Derivar una constante como 1", "La derivada de una constante es 0."]]
    body = L(think, ex, mist, kurve([(lambda x: x * x / 2, BLUE, "f"), (lambda x: 2 * x - 2, RED, "tangente")], (-3, 5, 1), (-3, 6, 1), W=330, H=260, label="recta tangente a una parábola"))
    faq = [("¿Para qué sirven las derivadas?", "Para medir cómo cambia una magnitud: velocidad, ritmo de crecimiento, costes marginales y para encontrar máximos y mínimos."),
           ("¿Una función continua es siempre derivable?", "No: |x| es continua en 0 pero tiene un pico y no es derivable allí.")]
    if lv == 1:
        unit(1, R, "derivadas", "A", "Derivada de una función: tasa de variación, definición, interpretación geométrica, reglas de derivación y recta tangente",
             "Derivadas", "Derivadas", "Fichas de Matemáticas I (1.º de Bachillerato): tasa de variación media, definición de derivada, reglas de derivación, producto, cociente, cadena y recta tangente. 100 ejercicios.",
             "f′(a) = pendiente de la tangente", "Cadena: f′(g(x)) · g′(x)", body, faq, sets, 12)
    else:
        unit(2, R, "derivadas", "A", "Derivadas: reglas de derivación, regla de la cadena, derivación logarítmica, derivabilidad y derivadas sucesivas",
             "Derivadas", "Derivadas", "Fichas de Matemáticas II (2.º de Bachillerato): reglas de derivación, cadena, derivación logarítmica, derivabilidad de funciones a trozos y derivadas sucesivas. 100 ejercicios.",
             "Cadena: f′(g(x)) · g′(x)", "Derivable implica continua (no al revés).", body, faq, sets, 8)


if __name__ == "__main__":
    build(1)
