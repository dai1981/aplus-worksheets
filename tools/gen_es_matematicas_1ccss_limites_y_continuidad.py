# -*- coding: utf-8 -*-
"""
España Matemáticas Aplicadas a las Ciencias Sociales I (1.º de Bachillerato): Límites y continuidad (Sentido de la medida)
Límites directos y laterales, límites en el infinito, indeterminaciones, asíntotas, continuidad; límites en contextos (coste medio, curvas de aprendizaje, tarifas).
Reutiliza los generadores de Matemáticas I con otra semilla.
Errores: decir que 0/0 = 0, comparar mal los grados, creer que el coste medio tiende a 0.
"""
import random
from es_ccss import M, mix, num, unit, L, r2, W, eu, use_, kurve, BLUE, fq
from fractions import Fraction as F

R = random.Random(53006)
s_directo, s_infinito, s_indet, s_asintotas, s_continuidad = use_("gen_es_matematicas_1bach_limites", 53206, "s_directo", "s_infinito", "s_indet", "s_asintotas", "s_continuidad")


def s_contexto():
    t = R.choice(["medio", "medio", "aprendizaje", "aprendizaje", "tarifa", "poblacion"])
    if t == "medio":
        f, v = R.randrange(500, 5001, 500), R.choice([2, 3, 4, 5, 6, 8, 12])
        bien = R.choice(["camisetas", "libros", "mochilas", "tazas", "entradas impresas"])
        return M("Producir x %s cuesta C(x) = %s + %dx euros. El coste medio por unidad es C(x)/x. ¿A qué valor tiende cuando x → +∞?" % (bien, num(f), v), eu(v, 0),
                 W([eu(0, 0), eu(f, 0), eu(f + v, 0), "+∞"]),
                 "lím (%s + %dx)/x = lím (%s/x + %d) = %d: el coste fijo se reparte entre muchas unidades. <b>%s</b>." % (num(f), v, num(f), v, v, eu(v, 0)))
    if t == "aprendizaje":
        a, b = R.randrange(20, 121, 10), R.randint(2, 9)
        tarea = R.choice(["piezas montadas al día", "palabras por minuto", "formularios revisados al día", "pedidos preparados por hora"])
        return M("Tras t días de práctica, un trabajador alcanza P(t) = %dt/(t + %d) %s. ¿Cuál es el límite de P(t) cuando t → +∞?" % (a, b, tarea), str(a),
                 W(["0", str(b), fq(F(a, b)) if a % b else str(a // b), "+∞", str(a + b)]),
                 "Mismo grado arriba y abajo: el límite es el cociente de los coeficientes, %d/1 = <b>%d</b>. Nunca supera ese valor." % (a, a))
    if t == "poblacion":
        K, c = R.randrange(2000, 20001, 1000), R.randint(2, 9)
        return M("Una población de aves sigue P(t) = %s/(1 + %d · 0,8<sup>t</sup>). ¿A qué valor tiende cuando t → +∞?" % (num(K), c), num(K),
                 W([num(K // (1 + c)), "0", num(K * c), "+∞"]),
                 "0,8<sup>t</sup> → 0, así que P(t) → %s/1 = <b>%s</b>." % (num(K), num(K)))
    p1, lim = R.choice([3, 4, 5, 6]), R.choice([10, 20, 30])
    p2 = R.choice([v for v in (1, 2, 3, 4) if v < p1])
    a = p1 * lim - p2 * lim
    return M("Un servicio cobra f(x) = %dx si 0 ≤ x ≤ %d y f(x) = a + %dx si x &gt; %d (x en horas). ¿Qué valor de a hace que la tarifa sea continua en x = %d?" % (p1, lim, p2, lim, lim), "a = %s" % num(a) if a >= 0 else "a = −%s" % num(-a),
             W(["a = %s" % num(p1 * lim), "a = %s" % num(p2 * lim), "a = 0", "a = %s" % num(abs(a) + lim)]),
             "Los dos trozos deben valer lo mismo en x = %d: %d · %d = a + %d · %d → <b>a = %s</b>." % (lim, p1, lim, p2, lim, num(a) if a >= 0 else "−" + num(-a)))


seen = set()
sets = [("Límites directos y laterales", mix(R, seen, [(s_directo, 20)])), ("Límites en el infinito", mix(R, seen, [(s_infinito, 20)])), ("Indeterminaciones y asíntotas", mix(R, seen, [(s_indet, 12), (s_asintotas, 8)])),
        ("Continuidad", mix(R, seen, [(s_continuidad, 20)])), ("Límites en contextos", mix(R, seen, [(s_contexto, 20)]))]
think = ["El <b>límite</b> de f en a es el valor al que se acerca f(x) cuando x se acerca a a. Si los límites laterales no coinciden, no existe.",
         "Cuando x → +∞, en un cociente de polinomios mandan los términos de mayor grado.",
         "<b>Indeterminaciones</b>: 0/0 (se factoriza y simplifica), ∞/∞ (se comparan grados).",
         "f es <b>continua</b> en a si f(a) existe, el límite existe y los dos coinciden. Una tarifa continua no tiene «saltos»."]
ex = [("Coste medio (2000 + 5x)/x cuando x → +∞", ["2000/x → 0"], "5 € por unidad"), ("lím<sub>x→2</sub> (x² − 4)/(x − 2)", ["0/0", "(x − 2)(x + 2)/(x − 2)"], "4")]
mist = [["Decir que 0/0 = 0", "Es una indeterminación: hay que simplificar."], ["Creer que el coste medio tiende a 0", "Tiende al coste de cada unidad."], ["Olvidar los límites laterales", "En las funciones a trozos son clave."]]
body = L(think, ex, mist, kurve([(lambda x: (2000 + 5 * x) / x if x > 0.5 else None, BLUE, "C(x)/x")], (0, 1000, 200), (0, 40, 5), W=330, H=240, label="coste medio: se acerca a 5 € cuando x crece"))
faq = [("¿Para qué sirven los límites en ciencias sociales?", "Para saber hacia dónde tiende una magnitud a largo plazo: el coste medio, una población o el rendimiento de un trabajador."),
       ("¿Qué es una asíntota horizontal?", "Una recta y = k a la que se acerca la función cuando x → ±∞: indica el valor a largo plazo.")]
unit(1, R, "limites-y-continuidad", "M", "Límites de funciones: cálculo, indeterminaciones y asíntotas; continuidad; límites en contextos económicos y sociales",
     "Límites y continuidad", "Límites y continuidad", "Fichas de Matemáticas Aplicadas a las Ciencias Sociales I: límites, indeterminaciones, asíntotas, continuidad y coste medio. 100 ejercicios con soluciones.",
     "∞/∞: compara los grados", "Coste medio → coste de cada unidad.", body, faq, sets, 6)
