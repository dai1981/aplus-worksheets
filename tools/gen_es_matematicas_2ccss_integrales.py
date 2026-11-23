# -*- coding: utf-8 -*-
"""
España Matemáticas Aplicadas a las Ciencias Sociales II (2.º de Bachillerato): Integrales (Sentido de la medida)
Primitivas inmediatas y casi inmediatas, regla de Barrow, área bajo una curva, área entre dos curvas; aplicaciones: del coste marginal al coste total, ingresos acumulados.
Reutiliza los generadores de Matemáticas II con otra semilla.
Errores: olvidar la constante (el coste fijo), restar F(b) − F(a) al revés, contar como negativa un área bajo el eje X.
"""
import random
from fractions import Fraction as F
from es_ccss import M, mix, num, unit, L, W, eu, use_, nf, E, kurve, BLUE

R = random.Random(54006)
s_inmediatas, s_cadena = use_("gen_es_matematicas_2bach_integrales_indefinidas", 54106, "s_inmediatas", "s_cadena")
s_barrow, s_area, s_entre = use_("gen_es_matematicas_2bach_integrales_definidas", 54206, "s_barrow", "s_area", "s_entre")


def s_aplicaciones():
    t = R.choice(["total", "total", "aumento", "aumento", "ingreso", "poblacion"])
    if t == "total":
        a, b = R.choice([2, 4, 6, 10]), R.randint(3, 30)
        cf = R.randrange(100, 2001, 100)
        x = R.randrange(10, 101, 10)
        C = a // 2 * x * x + b * x + cf
        return M("El coste marginal de una empresa es C′(x) = %dx + %d euros y los costes fijos son %s. ¿Cuánto cuesta producir %d unidades?" % (a, b, eu(cf, 0), x), eu(C, 0),
                 W([eu(C - cf, 0), eu(a * x + b, 0), eu(a * x * x + b * x + cf, 0), eu(a * x + b + cf, 0)]),
                 "C(x) = ∫(%dx + %d) dx = %sx² + %dx + K, y K = %s (costes fijos). C(%d) = <b>%s</b>." % (a, b, "" if a == 2 else a // 2, b, num(cf), x, eu(C, 0)))
    if t == "aumento":
        a, b = R.choice([2, 4, 6]), R.randint(3, 20)
        x1 = R.randrange(10, 61, 10)
        x2 = x1 + R.randrange(10, 41, 10)
        inc = a // 2 * (x2 ** 2 - x1 ** 2) + b * (x2 - x1)
        return M("Si el coste marginal es C′(x) = %dx + %d euros, ¿cuánto aumenta el coste al pasar de %d a %d unidades?" % (a, b, x1, x2), eu(inc, 0),
                 W([eu(a * x2 + b - (a * x1 + b), 0), eu(a // 2 * x2 ** 2 + b * x2, 0), eu(a * (x2 - x1) + b, 0), eu(a // 2 * (x2 - x1) ** 2 + b * (x2 - x1), 0)]),
                 "∫<sub>%d</sub><sup>%d</sup> (%dx + %d) dx = [%sx² + %dx]<sub>%d</sub><sup>%d</sup> = <b>%s</b>." % (x1, x2, a, b, "" if a == 2 else a // 2, b, x1, x2, eu(inc, 0)))
    if t == "ingreso":
        k, c = R.choice([(3, 2), (6, 4), (3, 10), (6, 1), (12, 5)])
        T = R.choice([2, 4, 5, 6, 10])
        val = F(k, 3) * T ** 3 + c * T
        return M("Una tienda online ingresa a un ritmo de v(t) = %dt² + %d miles de euros por mes (t en meses). ¿Cuánto ingresa en los %d primeros meses?" % (k, c, T), "%s miles de euros" % nf(val),
                 W(["%s miles de euros" % nf(k * T * T + c), "%s miles de euros" % nf(2 * k * T), "%s miles de euros" % nf(F(k, 3) * T ** 3), "%s miles de euros" % nf(k * T ** 3 + c * T)]),
                 "∫<sub>0</sub><sup>%d</sup> (%dt² + %d) dt = [%st³ + %dt]<sub>0</sub><sup>%d</sup> = <b>%s miles de euros</b>." % (T, k, c, nf(F(k, 3)) if k != 3 else "", c, T, nf(val)))
    r, T = R.choice([(20, 5), (30, 4), (12, 10), (60, 3), (40, 6)]), R.choice([2, 3, 4])
    r0, b = r
    val = r0 * T + F(b, 2) * T * T
    return M("Un pueblo gana habitantes a un ritmo de P′(t) = %d + %dt habitantes por año. ¿Cuántos habitantes gana en los %d primeros años?" % (r0, b, T), num(int(val)) if val.denominator == 1 else nf(val),
             W([num(r0 + b * T), num(r0 * T), num(r0 * T + b * T * T), num(int(r0 * T + b * T))]),
             "∫<sub>0</sub><sup>%d</sup> (%d + %dt) dt = [%dt + %st²]<sub>0</sub><sup>%d</sup> = <b>%s</b>." % (T, r0, b, r0, nf(F(b, 2)), T, num(int(val)) if val.denominator == 1 else nf(val)))


seen = set()
sets = [("Primitivas", mix(R, seen, [(s_inmediatas, 12), (s_cadena, 8)])), ("Regla de Barrow", mix(R, seen, [(s_barrow, 20)])), ("Área bajo una curva", mix(R, seen, [(s_area, 20)])),
        ("Área entre dos curvas", mix(R, seen, [(s_entre, 20)])), ("Aplicaciones a la economía", mix(R, seen, [(s_aplicaciones, 20)]))]
think = ["Una <b>primitiva</b> de f es una función F con F′ = f. ∫ x<sup>n</sup> dx = x<sup>n+1</sup>/(n + 1) + C (n ≠ −1); ∫ 1/x dx = ln |x| + C; ∫ e<sup>x</sup> dx = e<sup>x</sup> + C.",
         "<b>Regla de Barrow</b>: ∫<sub>a</sub><sup>b</sup> f(x) dx = F(b) − F(a).",
         "<b>Área</b>: si f ≥ 0 en [a, b], el área es ∫<sub>a</sub><sup>b</sup> f. Si cambia de signo, se divide en trozos y se suman los valores absolutos. Entre dos curvas: ∫ (arriba − abajo).",
         "En economía, integrar el coste marginal da el coste total; la constante es el <b>coste fijo</b>. Integrar un ritmo (por mes, por año) da el total acumulado."]
ex = [("C′(x) = 4x + 10, costes fijos 500 €, x = 20", ["C(x) = 2x² + 10x + 500"], "C(20) = 1500 €")]
mist = [["Olvidar la constante", "En el coste, la constante es el coste fijo."], ["Restar F(a) − F(b)", "Barrow: F(b) − F(a)."], ["Área negativa", "Si la curva está bajo el eje X, toma el valor absoluto."]]
body = L(think, ex, mist, kurve([(lambda x: 4 * x + 10, BLUE, "C′(x)")], (0, 25, 5), (0, 110, 20), W=330, H=240, label="coste marginal: el área bajo la recta es el aumento del coste"))
faq = [("¿Qué relación hay entre el coste marginal y el coste total?", "El coste total es una primitiva del coste marginal. La constante de integración es el coste fijo (el coste cuando no se produce nada)."),
       ("¿Para qué sirve la integral definida en ciencias sociales?", "Para calcular totales acumulados a partir de ritmos de cambio: ingresos de varios meses, aumento de población o de costes.")]
unit(2, R, "integrales", "M", "Integrales: primitivas inmediatas, regla de Barrow, área bajo una curva y entre curvas; aplicaciones económicas (coste total a partir del marginal, ingresos acumulados)",
     "Integrales", "Integrales", "Fichas de Matemáticas Aplicadas a las Ciencias Sociales II: primitivas, regla de Barrow, áreas y aplicaciones al coste y a los ingresos. 100 ejercicios.",
     "∫ₐᵇ f(x) dx = F(b) − F(a)", "Coste total: la constante es el coste fijo.", body, faq, sets, 6)
