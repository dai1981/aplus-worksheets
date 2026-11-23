# -*- coding: utf-8 -*-
"""
España Matemáticas Aplicadas a las Ciencias Sociales I (1.º de Bachillerato): Números reales y logaritmos (Sentido numérico)
Intervalos y valor absoluto, logaritmos (definición, propiedades), ecuaciones exponenciales y logarítmicas, problemas de crecimiento y depreciación (población, inflación, capital).
Reutiliza los generadores de 3.º de ESO y de Matemáticas I con otra semilla.
Errores: log (a + b) = log a + log b, usar porcentajes simples en un crecimiento compuesto, redondear hacia abajo los años necesarios.
"""
import math
import random
from es_ccss import M, mix, num, unit, L, r2, W, eu, pc, use_

R = random.Random(53002)
s_log_def, s_log_prop, s_ecuaciones = use_("gen_es_matematicas_1bach_numeros_reales_y_logaritmos", 53202, "s_log_def", "s_log_prop", "s_ecuaciones")
S_IVL, S_UNION, S_ABS = use_("gen_es_matematicas_3eso_numeros_reales", 53102, "s_ivl", "s_union", "s_absoluto")


def anos(n):
    return "%d año%s" % (n, "" if n == 1 else "s")


def s_crecimiento():
    t = R.choice(["poblacion", "poblacion", "deprecia", "deprecia", "inflacion", "capital", "baja"])
    if t == "poblacion":
        p0 = R.randrange(20000, 90001, 5000)
        r = R.choice([1.5, 2, 2.5, 3, 4])
        k = R.choice([1.2, 1.25, 1.5, 2])
        p1 = int(p0 * k)
        n = math.log(k) / math.log(1 + r / 100)
        ok = math.ceil(n)
        sitio = R.choice(["Una ciudad", "Un municipio", "Una comarca"])
        return M("%s tiene %s habitantes y crece un %s cada año. ¿Cuántos años completos tardará en superar los %s habitantes?" % (sitio, num(p0), pc(r), num(p1)), anos(ok),
                 W([anos(round((k - 1) * 100 / r)), anos(math.floor(n)) if math.floor(n) != ok else None, anos(ok + 2), anos(ok + 5)]),
                 "%s · %s<sup>t</sup> = %s → t = log %s / log %s ≈ %s. Hacen falta <b>%s</b>." % (num(p0), r2(1 + r / 100, 3), num(p1), r2(k), r2(1 + r / 100, 3), r2(n), anos(ok)))
    if t == "deprecia":
        v = R.randrange(12000, 40001, 1000)
        p = R.choice([8, 10, 12, 15, 20])
        n = R.randint(3, 6)
        obj = R.choice(["Un coche", "Una furgoneta", "Una máquina", "Un ordenador de una empresa"])
        val = v * (1 - p / 100) ** n
        return M("%s cuesta %s y pierde un %d %% de su valor cada año. ¿Cuánto valdrá dentro de %d años?" % (obj, eu(v, 0), p, n), eu(val),
                 W([eu(v * (1 - p * n / 100)), eu(v * (1 - p / 100) ** (n - 1)), eu(v * (p / 100) ** n), eu(v - val)]),
                 "Cada año se multiplica por %s: %s · %s<sup>%d</sup> = <b>%s</b>." % (r2(1 - p / 100), eu(v, 0), r2(1 - p / 100), n, eu(val)))
    if t == "inflacion":
        r = R.choice([2, 2.5, 3, 3.5, 4, 5])
        k = R.choice([20, 25, 50, 100])
        n = math.log(1 + k / 100) / math.log(1 + r / 100)
        ok = math.ceil(n)
        return M("Con una inflación constante del %s anual, ¿cuántos años completos tardan los precios en subir un %d %%?" % (pc(r), k), anos(ok),
                 W([anos(round(k / r)), anos(math.floor(n)) if math.floor(n) != ok else None, anos(ok + 3), anos(round(k / r) + 4)]),
                 "%s<sup>t</sup> = %s → t = log %s / log %s ≈ %s → <b>%s</b>." % (r2(1 + r / 100, 3), r2(1 + k / 100), r2(1 + k / 100), r2(1 + r / 100, 3), r2(n), anos(ok)))
    if t == "baja":
        p0 = R.randrange(2000, 9001, 500)
        p = R.choice([3, 4, 5, 6, 8])
        k = R.choice([0.5, 0.75, 0.8])
        n = math.log(k) / math.log(1 - p / 100)
        ok = math.ceil(n)
        quien = R.choice(["Un pueblo", "Una aldea", "Un barrio"])
        return M("%s tiene %s habitantes y pierde un %d %% cada año. ¿Cuántos años completos pasarán hasta que tenga menos de %s?" % (quien, num(p0), p, num(int(p0 * k))), anos(ok),
                 W([anos(round((1 - k) * 100 / p)), anos(math.floor(n)) if math.floor(n) != ok else None, anos(ok + 2), anos(ok + 4)]),
                 "%s<sup>t</sup> = %s → t = log %s / log %s ≈ %s → <b>%s</b>." % (r2(1 - p / 100), r2(k), r2(k), r2(1 - p / 100), r2(n), anos(ok)))
    C = R.randrange(2000, 20001, 1000)
    r = R.choice([2, 3, 4, 5, 6])
    k = R.choice([1.5, 2, 2.5])
    n = math.log(k) / math.log(1 + r / 100)
    ok = math.ceil(n)
    return M("¿Cuántos años completos tiene que estar un capital de %s al %s compuesto para llegar a %s?" % (eu(C, 0), pc(r), eu(C * k, 0)), anos(ok),
             W([anos(round((k - 1) * 100 / r)), anos(math.floor(n)) if math.floor(n) != ok else None, anos(ok + 3), anos(round(k * 100 / r))]),
             "%s<sup>t</sup> = %s → t = log %s / log %s ≈ %s → <b>%s</b>." % (r2(1 + r / 100, 3), r2(k), r2(k), r2(1 + r / 100, 3), r2(n), anos(ok)))


seen = set()
sets = [("Intervalos y valor absoluto", mix(R, seen, [(S_IVL, 7), (S_UNION, 7), (S_ABS, 6)])), ("Logaritmos", mix(R, seen, [(s_log_def, 20)])),
        ("Propiedades de los logaritmos", mix(R, seen, [(s_log_prop, 20)])), ("Ecuaciones exponenciales y logarítmicas", mix(R, seen, [(s_ecuaciones, 20)])),
        ("Crecimiento y depreciación", mix(R, seen, [(s_crecimiento, 20)]))]
think = ["Los <b>números reales</b> llenan la recta. Un trozo de la recta es un <b>intervalo</b>: [a, b] incluye los extremos, (a, b) no.",
         "log<sub>b</sub> x = y significa b<sup>y</sup> = x. log (ab) = log a + log b; log (a/b) = log a − log b; log a<sup>n</sup> = n · log a.",
         "Un crecimiento del r % anual multiplica cada año por 1 + r/100; una pérdida del p %, por 1 − p/100.",
         "Para saber <b>cuántos años</b> hacen falta, se despeja el exponente con logaritmos: t = log (final/inicial) / log (índice)."]
ex = [("Población de 50 000 que crece un 2 % anual: ¿cuándo supera 60 000?", ["1,02<sup>t</sup> = 1,2", "t = log 1,2 / log 1,02 ≈ 9,21"], "10 años"),
      ("Coche de 20 000 € que pierde un 15 % al año, 3 años", ["20 000 · 0,85³"], "12 282,50 €")]
mist = [["log (a + b) = log a + log b", "Falso: log (ab) = log a + log b."], ["Repartir el porcentaje entre los años", "Un 2 % durante 10 años no es un 20 %: es 1,02¹⁰ ≈ 1,219."],
        ["Redondear hacia abajo", "Si t ≈ 9,2, en 9 años aún no se llega: hacen falta 10."]]
body = L(think, ex, mist)
faq = [("¿Por qué se usan logaritmos en problemas de población o de dinero?", "Porque el tiempo está en el exponente: (1 + r)ᵗ = k. El logaritmo baja el exponente: t = log k / log (1 + r)."),
       ("¿Qué es la depreciación?", "La pérdida de valor de un bien con el tiempo. Si pierde un p % cada año, su valor se multiplica por 1 − p/100 cada año.")]
unit(1, R, "numeros-reales-y-logaritmos", "N", "Números reales: intervalos y valor absoluto; logaritmos y sus propiedades; ecuaciones exponenciales y logarítmicas; problemas de crecimiento y depreciación",
     "Números reales y logaritmos", "Reales y logaritmos", "Fichas de Matemáticas Aplicadas a las Ciencias Sociales I: intervalos, logaritmos, ecuaciones exponenciales y problemas de población, inflación y depreciación. 100 ejercicios.",
     "t = log k / log (1 + r)", "El tiempo está en el exponente: usa logaritmos.", body, faq, sets, 2)
