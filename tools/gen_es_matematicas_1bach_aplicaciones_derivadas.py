# -*- coding: utf-8 -*-
"""
España Matemáticas I y II (Bachillerato): Aplicaciones de las derivadas (Sentido algebraico)
build(lv): lv = 1 → «aplicaciones-de-las-derivadas» (monotonía, extremos, optimización, representación);
lv = 2 → añade curvatura y puntos de inflexión, teoremas de Rolle y del valor medio, optimización más compleja.
Errores: dar los intervalos de crecimiento con valores de y, decir que f′(a) = 0 siempre es un extremo (x³ en 0), olvidar comprobar los extremos del intervalo.
"""
import math
import random
from fractions import Fraction as F
from es_bach import M, mix, sg, num, unit, L, E, poly, nf, r2, kurve, BLUE, W, MINUS

R = None
LV = 1
INF, MINF = "+∞", MINUS + "∞"


def ivl(a, b):
    return "(%s, %s)" % (MINF if a is None else nf(a), INF if b is None else nf(b))


def cubic():
    """f con f′(x) = 3k(x − p)(x − q)"""
    p, q = sorted(R.sample(range(-4, 5), 2))
    k = R.choice([1, -1])
    # f = k(x³ − 3/2 (p+q) x² + 3pq x) + c → coef enteros si p+q par
    if (p + q) % 2:
        return None
    c = R.randint(-5, 5)
    cs = [k, -k * F(3 * (p + q), 2), 3 * k * p * q, c]
    cs = [int(x) for x in cs]
    return cs, p, q, k


def ev(cs, x):
    v = 0
    for c in cs:
        v = v * x + c
    return v


def s_monotonia():
    r = cubic()
    if not r:
        return None
    cs, p, q, k = r
    t = R.choice(["crece", "decrece", "union"])
    if t == "crece":
        ok = "%s ∪ %s" % (ivl(None, p), ivl(q, None)) if k > 0 else ivl(p, q)
        other = ivl(p, q) if k > 0 else "%s ∪ %s" % (ivl(None, p), ivl(q, None))
    else:
        ok = ivl(p, q) if k > 0 else "%s ∪ %s" % (ivl(None, p), ivl(q, None))
        other = "%s ∪ %s" % (ivl(None, p), ivl(q, None)) if k > 0 else ivl(p, q)
    word = "creciente" if t == "crece" else "decreciente"
    return M("¿En qué intervalos es %s f(x) = %s?" % (word, poly(cs)), ok, W([other, ivl(ev(cs, p), ev(cs, q)) if ev(cs, p) < ev(cs, q) else ivl(ev(cs, q), ev(cs, p)), ivl(p, None), ivl(None, q)]),
             "f′(x) = %s se anula en x = %s y x = %s; estudiamos su signo: <b>%s</b>." % (poly([3 * cs[0], 2 * cs[1], cs[2]]), sg(p), sg(q), ok))


def s_extremos():
    r = cubic()
    if not r:
        return None
    cs, p, q, k = r
    t = R.choice(["max", "min", "x3"])
    if t == "x3":
        a = R.randint(1, 4)
        return M("f(x) = x³ + %d cumple f′(0) = 0. ¿Tiene un extremo en x = 0?" % a, "no, es un punto de inflexión", ["sí, un máximo", "sí, un mínimo", "sí, un máximo y un mínimo"], "f′(x) = 3x² ≥ 0: no cambia de signo en 0, así que <b>no hay extremo</b> (es un punto de inflexión).")
    xm, xn = (p, q) if k > 0 else (q, p)
    want = xm if t == "max" else xn
    other = xn if t == "max" else xm
    P = lambda x: "(%s, %s)" % (sg(x), sg(ev(cs, x)))
    return M("¿Dónde tiene f(x) = %s un %s relativo?" % (poly(cs), "máximo" if t == "max" else "mínimo"), "en %s" % P(want), W(["en %s" % P(other), "en (%s, 0)" % sg(want), "en (0, %s)" % sg(cs[-1]) if want != 0 else "en (1, %s)" % sg(ev(cs, 1)), "en (%s, %s)" % (sg(ev(cs, want)), sg(want)) if ev(cs, want) != want else "en (%s, %s)" % (sg(want), sg(want + 1))]),
             "f′ = 0 en x = %s y x = %s; f′ pasa de %s en x = %s: <b>%s</b>." % (sg(p), sg(q), "+ a −" if t == "max" else "− a +", sg(want), P(want)))


def s_optim():
    t = R.choice(["rect", "num", "caja", "valla", "cilindro", "ingreso"])
    if t == "rect":
        P = R.choice([20, 24, 40, 60, 80, 100])
        return M("De todos los rectángulos de perímetro %d cm, ¿cuál tiene el área máxima?" % P, "el cuadrado de lado %s cm" % nf(F(P, 4)), ["el de lados %s cm y %s cm" % (nf(F(P, 4) - 1), nf(F(P, 4) + 1)), "el de lados %s cm y %s cm" % (nf(F(P, 2) - 1), "1"), "todos tienen la misma área"],
                 "A(x) = x(%s − x); A′(x) = %s − 2x = 0 → x = %s: <b>un cuadrado</b>." % (nf(F(P, 2)), nf(F(P, 2)), nf(F(P, 4))))
    if t == "num":
        s = R.choice([10, 12, 16, 20, 30, 40])
        return M("Descompón %d en dos sumandos positivos cuyo producto sea máximo." % s, "%d y %d" % (s // 2, s // 2), ["%d y %d" % (s // 2 - 1, s // 2 + 1), "%d y %d" % (1, s - 1), "%d y 0" % s], "P(x) = x(%d − x); P′(x) = %d − 2x = 0 → <b>x = %d</b>." % (s, s, s // 2))
    if t == "caja":
        L_ = R.choice([12, 18, 24, 30, 36])
        x = F(L_, 6)
        V_ = (L_ - 2 * x) ** 2 * x
        return M("Con una hoja cuadrada de %d cm de lado se hace una caja sin tapa cortando un cuadrado de lado x en cada esquina. ¿Qué x da el volumen máximo?" % L_, "x = %s cm" % nf(x), W(["x = %s cm" % nf(F(L_, 4)), "x = %s cm" % nf(F(L_, 2)), "x = %s cm" % nf(F(L_, 3)), "x = %s cm" % nf(x + 1)]),
                 "V(x) = (%d − 2x)² x; V′(x) = 0 → x = %s (la otra solución, %s, da volumen 0). Volumen máximo %s cm³. <b>x = %s cm</b>." % (L_, nf(x), nf(F(L_, 2)), nf(V_), nf(x)))
    if t == "valla":
        A = R.choice([200, 450, 800, 1250, 1800])
        x = int(math.isqrt(A // 2))
        if 2 * x * x != A:
            return None
        return M("Se quiere vallar un terreno rectangular de %s m² junto a un río (ese lado no se valla). ¿Qué dimensiones gastan menos valla?" % num(A), "%d m (perpendicular al río) y %d m" % (x, 2 * x), W(["%d m y %d m" % (2 * x, x) if False else "%d m (perpendicular al río) y %d m" % (2 * x, x // 2 if x % 2 == 0 else x), "%s m y %s m" % (r2(math.sqrt(A)), r2(math.sqrt(A))), "%d m y %d m" % (x + 5, A // (x + 5)) if A % (x + 5) == 0 else "%d m y %d m" % (x // 2 if x % 2 == 0 else x + 1, A // (x // 2) if x % 2 == 0 else 2 * x - 1)]),
                 "L(x) = 2x + %d/x; L′(x) = 2 − %d/x² = 0 → x = %d: <b>%d m y %d m</b>." % (A, A, x, x, 2 * x))
    if t == "cilindro":
        V_ = R.choice([16, 54, 128, 250])
        r = round((V_ / (2 * math.pi)) ** (1 / 3) * 1000) / 1000
        rr = (V_ / (2 * math.pi)) ** (1 / 3)
        return M("Una lata cilíndrica debe contener %d π cm³. ¿Qué radio minimiza el material (área total)?" % V_, "r = %s cm" % r2((V_ / 2) ** (1 / 3)), W(["r = %s cm" % r2(V_ ** (1 / 3)), "r = %s cm" % r2((V_ / 2) ** 0.5), "r = %s cm" % r2(V_ / 4)]),
                 "h = %d/r²; A(r) = 2πr² + 2π · %d/r; A′(r) = 0 → r³ = %d/2 → <b>r = %s cm</b> (la altura es el doble del radio)." % (V_, V_, V_, r2((V_ / 2) ** (1 / 3))))
    p0, a = R.choice([(20, 1), (30, 2), (40, 1), (50, 5), (60, 3)])
    # ingreso I(p) = p · (p0·10 − a·10 p)? usar demanda q = 100 − a·p
    q0 = 100
    pmax = F(q0, 2 * a)
    return M("La demanda de un producto es q = %d − %dp (p en euros). ¿Qué precio da el ingreso máximo?" % (q0, a), "%s €" % nf(pmax), W(["%s €" % nf(F(q0, a)), "%s €" % nf(F(q0, 4 * a)), "%d €" % q0, "%s €" % nf(pmax + 5)]), "I(p) = p(%d − %dp); I′(p) = %d − %dp = 0 → <b>p = %s €</b>." % (q0, a, q0, 2 * a, nf(pmax)))


def s_curvatura():
    t = R.choice(["inflex", "inflex", "concava", "teo"])
    r = cubic()
    if not r:
        return None
    cs, p, q, k = r
    xi = F(p + q, 2)
    if t == "inflex":
        return M("¿Dónde tiene f(x) = %s un punto de inflexión?" % poly(cs), "en x = %s" % nf(xi), W(["en x = %s" % sg(p), "en x = %s" % sg(q), "en x = %s" % nf(-xi) if xi else "en x = 1", "no tiene"]), "f″(x) = %s = 0 → <b>x = %s</b> (f″ cambia de signo)." % (poly([6 * cs[0], 2 * cs[1]]), nf(xi)))
    if t == "concava":
        up = (k > 0)
        ok = ivl(xi, None) if up else ivl(None, xi)
        return M("¿En qué intervalo es f(x) = %s cóncava hacia arriba (convexa, ∪)?" % poly(cs), ok, W([ivl(None, xi) if up else ivl(xi, None), ivl(p, q), "en todo ℝ"]), "f″(x) = %s &gt; 0 → <b>%s</b>." % (poly([6 * cs[0], 2 * cs[1]]), ok))
    q_, a, w = R.choice([("Si f″(a) &gt; 0 y f′(a) = 0, en x = a hay…", "un mínimo relativo", ["un máximo relativo", "un punto de inflexión", "una asíntota"]),
                         ("Si f″(a) &lt; 0 y f′(a) = 0, en x = a hay…", "un máximo relativo", ["un mínimo relativo", "un punto de inflexión", "un corte con el eje X"]),
                         ("En un punto de inflexión…", "la curva cambia de concavidad", ["la función alcanza un máximo", "la derivada no existe", "la función se anula"])])
    return M(q_, a, w, "Respuesta: <b>%s</b>." % a)


def s_teoremas():
    t = R.choice(["rolle", "tvm", "tvm", "teo"])
    if t == "rolle":
        a, b = sorted(R.sample(range(-4, 5), 2))
        s = a + b
        return M("f(x) = %s cumple f(%s) = f(%s). ¿En qué punto c asegura Rolle que f′(c) = 0?" % (poly([1, -s, a * b]), sg(a), sg(b)), "c = %s" % nf(F(s, 2)), W(["c = %s" % sg(a), "c = %s" % sg(b), "c = %s" % nf(F(-s, 2)) if s else "c = 1", "c = %s" % nf(F(s, 2) + 1)]),
                 "f′(x) = 2x %s %d = 0 → <b>c = %s</b>, que está en (%s, %s)." % ("−" if s >= 0 else "+", abs(s), nf(F(s, 2)), sg(a), sg(b)))
    if t == "tvm":
        a, b = sorted(R.sample(range(-3, 5), 2))
        c = F(a + b, 2)
        return M("Aplica el teorema del valor medio a f(x) = x² en [%s, %s]. ¿Qué punto c cumple f′(c) = (f(b) − f(a))/(b − a)?" % (sg(a), sg(b)), "c = %s" % nf(c), W(["c = %s" % sg(a + b), "c = %s" % nf(F(b - a, 2)), "c = %s" % nf(F(a * a + b * b, 2)), "c = %s" % nf(c + 1)]),
                 "(%d − %d)/%d = %s = 2c → <b>c = %s</b>." % (b * b, a * a, b - a, sg(a + b), nf(c)))
    q_, a, w = R.choice([("¿Qué exige el teorema de Rolle?", "f continua en [a, b], derivable en (a, b) y f(a) = f(b)", ["f creciente en [a, b]", "f(a) · f(b) &lt; 0", "f derivable y f(a) = 0"]),
                         ("¿Qué asegura el teorema del valor medio?", "que hay un c donde la tangente es paralela a la cuerda", ["que f tiene un cero en (a, b)", "que f es creciente", "que f(a) = f(b)"]),
                         ("¿Se puede aplicar Rolle a f(x) = |x| en [−1, 1]?", "no, porque no es derivable en x = 0", ["sí", "no, porque f(−1) ≠ f(1)", "no, porque no es continua"])])
    return M(q_, a, w, "Respuesta: <b>%s</b>." % a)


def s_grafica():
    r = cubic()
    if not r:
        return None
    cs, p, q, k = r
    f = lambda x: ev(cs, x)
    ys = [f(x) for x in (p, q)]
    if max(abs(y) for y in ys) > 30:
        return None
    step = 5 if max(abs(y) for y in ys) > 10 else 2
    lo = int(math.floor((min(ys) - 3) / step)) * step
    hi = int(math.ceil((max(ys) + 3) / step)) * step
    pic = kurve([(f, BLUE, "")], (-5, 5, 1), (lo, hi, step), W=330, H=280, label="gráfica de una función polinómica")
    t = R.choice(["n", "fp", "fp", "izq"])
    if t == "izq":
        return M(pic + "¿Qué signo tiene f′(x) para x &lt; %s?" % sg(p), "positivo" if k > 0 else "negativo", ["negativo" if k > 0 else "positivo", "cero", "cambia varias veces"], "A la izquierda de x = %s la función %s: f′ es <b>%s</b>." % (sg(p), "sube" if k > 0 else "baja", "positivo" if k > 0 else "negativo"))
    if t == "n":
        return M(pic + "¿En cuántos puntos se anula la derivada de esta función?", "en 2", ["en 1", "en 3", "en ninguno"], "La tangente es horizontal en el máximo y en el mínimo: <b>en 2</b>.")
    return M(pic + "¿Qué signo tiene f′(x) entre x = %s y x = %s?" % (sg(p), sg(q)), "negativo" if k > 0 else "positivo", ["positivo" if k > 0 else "negativo", "cero", "cambia varias veces"], "En ese tramo la función %s: f′ es <b>%s</b>." % ("baja" if k > 0 else "sube", "negativo" if k > 0 else "positivo"))


def build(lv):
    global R, LV
    LV = lv
    R = random.Random(51013 + (lv - 1) * 1000)
    seen = set()
    if lv == 1:
        sets = [("Crecimiento y decrecimiento", mix(R, seen, [(s_monotonia, 20)])), ("Máximos y mínimos", mix(R, seen, [(s_extremos, 20)])), ("Leer la derivada en una gráfica", mix(R, seen, [(s_grafica, 8), (s_monotonia, 12)])),
                ("Optimización", mix(R, seen, [(s_optim, 20)])), ("Problemas y extremos", mix(R, seen, [(s_optim, 10), (s_extremos, 10)]))]
    else:
        sets = [("Monotonía y extremos", mix(R, seen, [(s_monotonia, 10), (s_extremos, 10)])), ("Curvatura y puntos de inflexión", mix(R, seen, [(s_curvatura, 20)])), ("Teoremas de Rolle y del valor medio", mix(R, seen, [(s_teoremas, 20)])),
                ("Optimización", mix(R, seen, [(s_optim, 20)])), ("Representación de funciones", mix(R, seen, [(s_grafica, 8), (s_curvatura, 6), (s_extremos, 6)]))]
    think = ["Si f′(x) &gt; 0 en un intervalo, f es <b>creciente</b>; si f′(x) &lt; 0, <b>decreciente</b>.",
             "Los <b>extremos relativos</b> están donde f′ cambia de signo (de + a − es un máximo; de − a +, un mínimo). f′(a) = 0 no basta.",
             "<b>Optimizar</b>: se escribe la magnitud en función de una sola variable, se deriva, se iguala a 0 y se comprueba que es máximo o mínimo."]
    if lv == 2:
        think.append("<b>Curvatura</b>: f″ &gt; 0, cóncava hacia arriba (∪); f″ &lt; 0, hacia abajo (∩). En los puntos de inflexión f″ cambia de signo. Rolle y el valor medio aseguran puntos con tangente horizontal o paralela a la cuerda.")
    ex = [("f(x) = x³ − 3x", ["f′(x) = 3x² − 3 = 0 → x = ±1"], "máximo (−1, 2), mínimo (1, −2)"), ("Rectángulo de perímetro 20 con área máxima", ["A = x(10 − x)", "A′ = 10 − 2x"], "cuadrado de lado 5")]
    mist = [["Intervalos con valores de y", "Los intervalos de monotonía son de x."], ["f′(a) = 0 → extremo", "x³ en 0 no tiene extremo."], ["No comprobar el tipo de extremo", "Mira el signo de f′ o de f″."]]
    body = L(think, ex, mist, kurve([(lambda x: x ** 3 - 3 * x, BLUE, "")], (-3, 3, 1), (-4, 4, 1), W=330, H=260, label="f(x) = x³ − 3x con un máximo y un mínimo"))
    faq = [("¿Para qué sirve optimizar?", "Para encontrar la mejor opción: el envase que gasta menos material, el precio que da más ingresos o el camino más corto."),
           ("¿Cómo sé si es máximo o mínimo?", "Por el cambio de signo de f′ o con la derivada segunda: f″ &lt; 0 máximo, f″ &gt; 0 mínimo.")]
    if lv == 1:
        unit(1, R, "aplicaciones-de-las-derivadas", "A", "Aplicaciones de la derivada: monotonía, extremos relativos, optimización y representación de funciones",
             "Aplicaciones de las derivadas", "Aplicaciones de la derivada", "Fichas de Matemáticas I (1.º de Bachillerato): crecimiento, máximos y mínimos, optimización y lectura de gráficas con la derivada. 100 ejercicios con soluciones.",
             "f′ &gt; 0 crece; f′ &lt; 0 decrece", "Extremo: f′ cambia de signo.", body, faq, sets, 13)
    else:
        unit(2, R, "aplicaciones-de-las-derivadas", "A", "Aplicaciones de la derivada: monotonía, extremos, curvatura, puntos de inflexión, teoremas de Rolle y del valor medio, optimización y representación",
             "Aplicaciones de las derivadas", "Aplicaciones de la derivada", "Fichas de Matemáticas II (2.º de Bachillerato): monotonía, extremos, curvatura, inflexión, Rolle, valor medio y optimización. 100 ejercicios con soluciones.",
             "f″ &gt; 0: ∪; f″ &lt; 0: ∩", "Optimiza: deriva, iguala a 0 y comprueba.", body, faq, sets, 9)


if __name__ == "__main__":
    build(1)
