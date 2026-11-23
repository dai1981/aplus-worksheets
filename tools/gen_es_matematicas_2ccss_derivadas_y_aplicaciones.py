# -*- coding: utf-8 -*-
"""
España Matemáticas Aplicadas a las Ciencias Sociales II (2.º de Bachillerato): Derivadas y aplicaciones (Sentido de la medida)
Derivadas (reglas y cadena), crecimiento y extremos relativos, curvatura y puntos de inflexión, representación, optimización;
problemas de economía: beneficio máximo, coste medio mínimo, precio que maximiza el ingreso, interpretación del coste marginal.
Reutiliza los generadores de Matemáticas I con otra semilla.
Errores: no comprobar que el extremo es un máximo, confundir el valor de x con el valor del beneficio, derivar el coste medio como C′(x).
"""
import math
import random
from es_ccss import M, mix, num, unit, L, W, eu, use_, r2, kurve, BLUE, RED

R = random.Random(54005)
s_reglas, s_cadena = use_("gen_es_matematicas_1bach_derivadas", 54105, "s_reglas", "s_cadena")
s_monotonia, s_extremos, s_curvatura, s_grafica, s_optim = use_("gen_es_matematicas_1bach_aplicaciones_derivadas", 54205, "s_monotonia", "s_extremos", "s_curvatura", "s_grafica", "s_optim")


def s_economia():
    t = R.choice(["beneficio", "beneficio", "medio", "medio", "precio", "unidades"])
    if t == "beneficio":
        a = R.choice([1, 2, 3, 4, 5])
        x0 = R.randint(5, 40)
        b = 2 * a * x0
        c = R.randrange(10, 401, 10)
        Bm = -a * x0 * x0 + b * x0 - c
        if Bm <= 0:
            return None
        ask = R.choice(["x", "B"])
        e = "B′(x) = −%dx + %d = 0 → x = %d; B″ = −%d &lt; 0, es un máximo. B(%d) = %s." % (2 * a, b, x0, 2 * a, x0, num(Bm))
        Bt = "B(x) = −%sx² + %dx − %d" % ("" if a == 1 else a, b, c)
        if ask == "x":
            return M("El beneficio diario de una empresa es %s (cientos de euros), con x el número de unidades. ¿Cuántas unidades dan el beneficio máximo?" % Bt, "%d unidades" % x0,
                     W(["%d unidades" % b, "%d unidades" % (2 * x0), "%d unidades" % (x0 + a), "%d unidades" % max(1, x0 // 2)]), e + " <b>%d unidades</b>." % x0)
        return M("El beneficio diario de una empresa es %s (cientos de euros). ¿Cuál es el beneficio máximo?" % Bt, "%s cientos de euros" % num(Bm),
                 W(["%s cientos de euros" % num(x0), "%s cientos de euros" % num(Bm + c), "%s cientos de euros" % num(-a * (2 * x0) ** 2 + b * 2 * x0 - c) if -a * (2 * x0) ** 2 + b * 2 * x0 - c > 0 else "%s cientos de euros" % num(Bm + 2 * c), "%s cientos de euros" % num(b)]),
                 e + " <b>%s cientos de euros</b>." % num(Bm))
    if t == "medio":
        a, x0 = R.choice([1, 2, 4, 5]), R.choice([10, 20, 30, 40, 50])
        c = a * x0 * x0
        b = R.randint(2, 30)
        cm = 2 * a * x0 + b
        return M("El coste de producir x unidades es C(x) = %sx² + %dx + %s euros. ¿Qué producción hace mínimo el coste medio C(x)/x?" % ("" if a == 1 else a, b, num(c)), "%d unidades (coste medio %s)" % (x0, eu(cm, 0)),
                 W(["%d unidades (coste medio %s)" % (x0 * 2, eu(a * 2 * x0 + b + c / (2 * x0), 0)), None,
                    "%d unidades (coste medio %s)" % (x0 // 2, eu(a * x0 / 2 + b + c / (x0 / 2), 0)), "%s unidades (coste medio %s)" % (num(c), eu(a * c + b + 1, 0)), "%d unidades (coste medio %s)" % (x0, eu(2 * a * x0 + b + 1, 0))]),
                 "CM(x) = %sx + %d + %s/x; CM′(x) = %s − %s/x² = 0 → x² = %s → x = %d. CM(%d) = <b>%s</b>." % ("" if a == 1 else a, b, num(c), a, num(c), num(c // a), x0, x0, eu(cm, 0)))
    if t == "precio":
        q0, k = R.choice([(200, 4), (300, 5), (120, 2), (400, 8), (240, 3), (500, 10)])
        p = q0 / (2 * k)
        ok = eu(p, 0) if p == int(p) else eu(p)
        return M("Si el precio es p euros, se venden q = %d − %dp unidades. ¿Qué precio da el ingreso máximo?" % (q0, k), ok,
                 W([eu(q0 / k, 0) if q0 % k == 0 else eu(q0 / k), eu(q0 / (4 * k)), eu(q0 / 2, 0), eu(k * 2, 0)]),
                 "I(p) = p(%d − %dp) = %dp − %dp²; I′(p) = %d − %dp = 0 → <b>p = %s</b>." % (q0, k, q0, k, q0, 2 * k, ok))
    a, b, c = R.choice([0.5, 1, 2]), R.randint(5, 40), R.randrange(100, 1001, 100)
    pv = R.randint(30, 120)
    # beneficio B(x) = pv·x − (a x² + b x + c) ; máximo en x = (pv − b)/(2a)
    x0 = (pv - b) / (2 * a)
    if x0 != int(x0) or x0 <= 0:
        return None
    x0 = int(x0)
    return M("Cada unidad se vende a %d € y el coste es C(x) = %sx² + %dx + %s €. ¿Cuántas unidades conviene producir para que el beneficio sea máximo?" % (pv, r2(a) if a != 1 else "", b, num(c)), "%d unidades" % x0,
             W(["%d unidades" % int(pv / (2 * a)), "%d unidades" % int((pv + b) / (2 * a)), "%d unidades" % (2 * x0), "%d unidades" % (x0 + 5)]),
             "B(x) = %dx − C(x); B′(x) = %d − %sx − %d = 0 → x = <b>%d</b>. (Es donde el ingreso marginal iguala al coste marginal.)" % (pv, pv, r2(2 * a) if 2 * a != 1 else "", b, x0))


seen = set()
sets = [("Derivadas", mix(R, seen, [(s_reglas, 10), (s_cadena, 10)])), ("Crecimiento y extremos", mix(R, seen, [(s_monotonia, 10), (s_extremos, 10)])),
        ("Curvatura y representación", mix(R, seen, [(s_curvatura, 10), (s_grafica, 10)])), ("Optimización", mix(R, seen, [(s_optim, 20)])), ("Problemas de economía", mix(R, seen, [(s_economia, 20)]))]
think = ["Si f′ &gt; 0 en un intervalo, f <b>crece</b>; si f′ &lt; 0, <b>decrece</b>. Los <b>extremos relativos</b> están donde f′ = 0 y cambia de signo (o f″ ≠ 0).",
         "f″ &gt; 0: cóncava hacia arriba (∪); f″ &lt; 0: hacia abajo (∩). Donde cambia la curvatura hay un <b>punto de inflexión</b>.",
         "<b>Optimizar</b>: escribe la función que hay que maximizar o minimizar con una sola variable, deriva, iguala a 0 y comprueba que es un máximo o un mínimo.",
         "En economía: el beneficio es B = I − C; es máximo cuando el ingreso marginal I′ iguala al coste marginal C′. El coste medio es C(x)/x."]
ex = [("B(x) = −2x² + 120x − 500", ["B′(x) = −4x + 120 = 0 → x = 30", "B″ = −4 &lt; 0: máximo"], "B(30) = 1300")]
mist = [["No comprobar si es máximo o mínimo", "Mira el signo de f″ o el cambio de signo de f′."], ["Dar x en lugar del beneficio", "Lee qué se pregunta: ¿las unidades o el beneficio?"], ["Derivar mal el coste medio", "CM(x) = C(x)/x: primero divide y luego deriva."]]
body = L(think, ex, mist, kurve([(lambda x: -2 * x * x + 120 * x - 500, BLUE, "B(x)")], (0, 60, 10), (-600, 1400, 400), W=330, H=260, label="beneficio con máximo en x = 30"))
faq = [("¿Cómo se halla el beneficio máximo?", "Se deriva B(x), se iguala a 0, se comprueba con B″ (negativa: máximo) y se calcula B en ese punto."),
       ("¿Qué relación hay entre coste marginal y beneficio máximo?", "El beneficio es máximo cuando producir una unidad más cuesta lo mismo que lo que se ingresa por ella: I′(x) = C′(x).")]
unit(2, R, "derivadas-y-aplicaciones", "M", "Derivadas y aplicaciones: crecimiento, extremos relativos, curvatura, puntos de inflexión, representación de funciones y optimización en problemas de economía",
     "Derivadas y aplicaciones", "Derivadas y aplicaciones", "Fichas de Matemáticas Aplicadas a las Ciencias Sociales II: crecimiento, extremos, curvatura, optimización, beneficio máximo y coste medio mínimo. 100 ejercicios.",
     "Máximo: B′ = 0 y B″ < 0", "Beneficio máximo cuando I′(x) = C′(x).", body, faq, sets, 5)
