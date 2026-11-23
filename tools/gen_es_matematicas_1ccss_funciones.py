# -*- coding: utf-8 -*-
"""
España Matemáticas Aplicadas a las Ciencias Sociales I (1.º de Bachillerato): Funciones (Sentido algebraico)
Dominio, funciones elementales (lineales, cuadráticas, de proporcionalidad inversa, exponenciales y logarítmicas), transformaciones, funciones a trozos;
funciones en contextos sociales y económicos: costes, tarifas, oferta y demanda, crecimiento exponencial.
Reutiliza los generadores de Matemáticas I con otra semilla.
Errores: confundir coste fijo y variable, aplicar el precio del segundo tramo a todo el consumo, despejar mal el precio de equilibrio.
"""
import random
from es_ccss import M, mix, num, unit, L, r2, W, eu, pc, use_, kurve, BLUE, RED

R = random.Random(53005)
s_dominio, s_elementales, s_transformacion, s_trozos = use_("gen_es_matematicas_1bach_funciones", 53205, "s_dominio", "s_elementales", "s_transformacion", "s_trozos")


def s_mercado():
    return s_contexto(R.choice(["equilibrio", "equilibrio", "lineal"]))


def s_modelos():
    return s_contexto(R.choice(["tramos", "tramos", "exponencial", "teo"]))


def s_contexto(t):
    if t == "equilibrio":
        p = R.randint(4, 30)
        b, dd = R.randint(2, 8), R.randint(1, 6)
        c = R.randint(10, 60)
        q = c + dd * p
        a = q + b * p
        ok = "%s (se venden %s unidades)" % (eu(p, 0), num(q))
        wp = [(a + c) / (b + dd), (a - c) / (b - dd) if b != dd else None, a / b, (a - c) / (b + dd) + 2]
        return M("La demanda de un producto es D(p) = %d − %dp y la oferta O(p) = %d + %sp (p en euros). ¿Cuál es el precio de equilibrio?" % (a, b, c, "" if dd == 1 else dd), ok,
                 W(["%s (se venden %s unidades)" % (eu(v), num(int(round(c + dd * v)))) if v is not None and v > 0 and v != int(v) else
                    "%s (se venden %s unidades)" % (eu(v, 0), num(int(c + dd * v))) if v is not None and v > 0 else None for v in wp]),
                 "D(p) = O(p): %d − %dp = %d + %sp → %dp = %d → p = %d. Cantidad: %d + %d · %d = %s. <b>%s</b>." % (a, b, c, "" if dd == 1 else dd, b + dd, a - c, p, c, dd, p, num(q), ok))
    if t == "tramos":
        p1, p2 = R.choice([(0.8, 1.2), (0.6, 1.0), (1.0, 1.5), (0.5, 0.9), (0.7, 1.3)])
        lim = R.choice([10, 15, 20])
        x = R.randint(lim + 2, lim + 25)
        val = p1 * lim + p2 * (x - lim)
        return M("Una compañía de agua cobra %s por m³ los primeros %d m³ y %s por m³ el consumo que pase de %d m³. ¿Cuánto paga un hogar que gasta %d m³?" % (eu(p1 * 100 / 100), lim, eu(p2), lim, x), eu(val),
                 W([eu(p2 * x), eu(p1 * x), eu(p1 * lim + p1 * (x - lim) + p2), eu(p1 * lim + p2 * x)]),
                 "f(x) = %s · %d + %s · (x − %d) si x &gt; %d: %s + %s · %d = <b>%s</b>." % (r2(p1), lim, r2(p2), lim, lim, eu(p1 * lim), r2(p2), x - lim, eu(val)))
    if t == "lineal":
        f, v = R.randrange(200, 3001, 100), R.choice([2, 3, 4, 5, 6, 8, 12, 15])
        x = R.randrange(50, 1001, 50)
        ask = R.choice(["coste", "unidades"])
        if ask == "coste":
            return M("Producir x unidades cuesta C(x) = %s + %dx euros. ¿Cuánto cuesta producir %s unidades?" % (num(f), v, num(x)), eu(f + v * x, 0),
                     W([eu(v * x, 0), eu(f + v + x, 0), eu((f + x) * v, 0), eu(f + v * x + v, 0)]), "C(%s) = %s + %d · %s = <b>%s</b>." % (num(x), num(f), v, num(x), eu(f + v * x, 0)))
        return M("Producir x unidades cuesta C(x) = %s + %dx euros. ¿Cuántas unidades se pueden producir con %s?" % (num(f), v, eu(f + v * x, 0)), "%s unidades" % num(x),
                 W(["%s unidades" % num((f + v * x) // v), "%s unidades" % num(x + f // v) if f % v == 0 else None, "%s unidades" % num(x - 10), "%s unidades" % num(x + 50)]),
                 "%s + %dx = %s → %dx = %s → x = <b>%s</b>." % (num(f), v, num(f + v * x), v, num(v * x), num(x)))
    if t == "exponencial":
        p0 = R.randrange(10, 91, 5)
        r = R.choice([2, 3, 4, 5])
        n = R.randint(3, 10)
        v = p0 * (1 + r / 100) ** n
        return M("Los usuarios de una aplicación (en miles) siguen U(t) = %d · %s<sup>t</sup>, con t en años. ¿Cuántos usuarios habrá dentro de %d años?" % (p0, r2(1 + r / 100), n), "%s mil" % r2(v, 1),
                 W(["%s mil" % r2(p0 * (1 + r * n / 100), 1), "%s mil" % r2(p0 * (1 + r / 100) ** (n - 1), 1), "%s mil" % r2(p0 * r / 100 * n, 1), "%s mil" % r2(p0 * (1 + r / 100) ** (n + 1), 1)]),
                 "U(%d) = %d · %s<sup>%d</sup> ≈ <b>%s mil</b>." % (n, p0, r2(1 + r / 100), n, r2(v, 1)))
    f, v, k = R.randrange(300, 2001, 100), R.choice([3, 4, 5, 7, 9]), R.choice([0.85, 0.9, 0.95, 1.03, 1.05])
    q, a, w = R.choice([("C(x) = %s + %dx es el coste de x unidades. ¿Qué representa %s?" % (num(f), v, num(f)), "el coste fijo (aunque no se produzca nada)", ["el coste de cada unidad", "el beneficio", "el número de unidades"]),
                        ("C(x) = %s + %dx es el coste de x unidades. ¿Qué representa %d?" % (num(f), v, v), "lo que cuesta cada unidad más (coste variable unitario)", ["el coste fijo", "el número de trabajadores", "el precio de venta"]),
                        ("En V(t) = 20 000 · %s<sup>t</sup> (valor de un bien en euros, t en años), ¿qué significa %s?" % (r2(k), r2(k)),
                         ("cada año pierde un %s de su valor" % pc((1 - k) * 100)) if k < 1 else ("cada año gana un %s de valor" % pc((k - 1) * 100)),
                         [("cada año pierde %s €" % r2(k)) if k < 1 else "cada año gana %s €" % r2(k), ("cada año gana un %s de valor" % pc((1 - k) * 100)) if k < 1 else "cada año pierde un %s de su valor" % pc((k - 1) * 100), "el valor inicial"]),
                        ("¿Qué tipo de función describe un crecimiento de un porcentaje fijo cada año (%s)?" % pc(R.choice([2, 3, 5, 7])), "exponencial", ["lineal", "cuadrática", "de proporcionalidad inversa"])])
    return M(q, a, w, "Respuesta: <b>%s</b>." % a)


seen = set()
sets = [("Dominio", mix(R, seen, [(s_dominio, 20)])), ("Funciones elementales y transformaciones", mix(R, seen, [(s_elementales, 8), (s_transformacion, 12)])), ("Funciones a trozos", mix(R, seen, [(s_trozos, 20)])),
        ("Costes y mercado", mix(R, seen, [(s_mercado, 20)])), ("Tarifas y crecimiento", mix(R, seen, [(s_modelos, 20)]))]
think = ["Una <b>función</b> asigna a cada x un único valor f(x). El <b>dominio</b> son los x en los que se puede calcular.",
         "<b>Lineal</b> y = mx + n: crece lo mismo cada vez (costes, tarifas). <b>Exponencial</b> y = a · b<sup>x</sup>: crece un porcentaje fijo (población, dinero).",
         "Una <b>función a trozos</b> usa una fórmula distinta en cada tramo (tarifas, impuestos): primero mira en qué tramo está x.",
         "<b>Equilibrio de mercado</b>: el precio en el que la demanda D(p) es igual a la oferta O(p)."]
ex = [("D(p) = 100 − 3p, O(p) = 20 + 2p", ["100 − 3p = 20 + 2p", "5p = 80"], "p = 16 €, 52 unidades")]
mist = [["Aplicar el segundo precio a todo el consumo", "Cada tramo se paga a su precio."], ["Confundir coste fijo y variable", "En C(x) = 500 + 4x, 500 es fijo; 4 es lo que cuesta cada unidad."],
        ["Creer que un 3 % anual es lineal", "Un porcentaje fijo da una función exponencial."]]
body = L(think, ex, mist, kurve([(lambda p: 100 - 3 * p, BLUE, "D(p)"), (lambda p: 20 + 2 * p, RED, "O(p)")], (0, 32, 4), (0, 104, 20), W=330, H=260, label="demanda y oferta: se cortan en el precio de equilibrio"))
faq = [("¿Qué es el precio de equilibrio?", "El precio al que la cantidad que quieren comprar los consumidores (demanda) coincide con la que quieren vender los productores (oferta)."),
       ("¿Por qué las tarifas son funciones a trozos?", "Porque el precio cambia según el tramo de consumo: los primeros m³ de agua o los primeros kWh se pagan a un precio y el resto a otro.")]
unit(1, R, "funciones", "A", "Funciones: dominio, funciones elementales, transformaciones y funciones a trozos; modelos de costes, tarifas, oferta y demanda y crecimiento exponencial",
     "Funciones", "Funciones", "Fichas de Matemáticas Aplicadas a las Ciencias Sociales I: dominio, funciones elementales, funciones a trozos, tarifas, oferta y demanda. 100 ejercicios con soluciones.",
     "Equilibrio: D(p) = O(p)", "Tarifas: cada tramo a su precio.", body, faq, sets, 5)
