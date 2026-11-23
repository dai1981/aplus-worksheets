# -*- coding: utf-8 -*-
"""
España Matemáticas 1.º de ESO: Circunferencia y círculo (Sentido de la medida)
Elementos, posiciones relativas, longitud de la circunferencia y del arco, área del círculo, del sector y de la corona circular; problemas. π ≈ 3,14.
Reutiliza problemas de 6.º de Primaria (longitud y área) con otra semilla.
Errores: usar el diámetro como radio, calcular 2πr para el área, olvidar la fracción n/360 en arcos y sectores.
"""
import random
from fractions import Fraction as F
from es_eso import M, mix, d, num, unit, L, Kids, use_

R = random.Random(47012)
K = Kids(R)
lon, area, inv, prob = use_("gen_es_matematicas_6_longitud_y_area_del_circulo", 47913, "s2_longitud", "s3_area", "s4_inversa", "s5_problema")
import gen_es_matematicas_6_longitud_y_area_del_circulo as C6
PI = F(314, 100)


def s_elementos():
    q, a, w = R.choice([("¿Cómo se llama el segmento que une el centro con un punto de la circunferencia?", "radio", ["diámetro", "cuerda", "arco"]),
                        ("¿Cómo se llama el segmento que une dos puntos de la circunferencia?", "cuerda", ["radio", "tangente", "sector"]),
                        ("¿Cómo se llama la cuerda que pasa por el centro?", "diámetro", ["radio", "arco", "secante"]),
                        ("¿Cómo se llama la parte de la circunferencia entre dos puntos?", "arco", ["cuerda", "sector", "segmento"]),
                        ("¿Cómo se llama la parte del círculo entre dos radios y un arco?", "sector circular", ["segmento circular", "corona circular", "semicírculo"]),
                        ("¿Cómo se llama la parte entre dos circunferencias concéntricas?", "corona circular", ["sector circular", "segmento circular", "arco"]),
                        ("Una recta que toca la circunferencia en un solo punto es…", "tangente", ["secante", "exterior", "diámetro"]),
                        ("Una recta que corta la circunferencia en dos puntos es…", "secante", ["tangente", "exterior", "radio"]),
                        ("Si la distancia del centro a una recta es mayor que el radio, la recta es…", "exterior", ["tangente", "secante", "un diámetro"]),
                        ("Si la distancia del centro a una recta es igual al radio, la recta es…", "tangente", ["secante", "exterior", "una cuerda"]),
                        ("¿Cómo es la tangente respecto al radio en el punto de contacto?", "perpendicular", ["paralela", "igual", "secante"]),
                        ("Dos circunferencias con el mismo centro se llaman…", "concéntricas", ["tangentes", "secantes", "exteriores"])])
    if R.random() < 0.3:
        r = R.randint(2, 30)
        k = R.choice(["d", "r"])
        if k == "d":
            return M("Una circunferencia tiene %d cm de radio. ¿Cuánto mide su diámetro?" % r, "%d cm" % (2 * r), ["%s cm" % d(F(r, 2)), "%d cm" % r, "%s cm" % d(2 * r * PI)], "diámetro = 2 · radio = <b>%d cm</b>." % (2 * r))
        return M("Una circunferencia tiene %d cm de diámetro. ¿Cuánto mide su radio?" % (2 * r), "%d cm" % r, ["%d cm" % (4 * r), "%d cm" % (2 * r), "%d cm" % (r + 1)], "radio = diámetro : 2 = <b>%d cm</b>." % r)
    return M(q, a, w, "Respuesta: <b>%s</b>." % a)


def s_arco():
    r = R.randint(2, 20)
    n = R.choice([30, 45, 60, 90, 120, 135, 150, 180, 210, 240, 270, 300])
    t = R.choice(["arco", "sector", "arco", "sector", "corona"])
    if t == "arco":
        Lv = 2 * PI * r * n / 360
        return M("¿Cuánto mide un arco de %d° en una circunferencia de %d cm de radio? (π ≈ 3,14)" % (n, r), "%s cm" % d(Lv), ["%s cm" % d(2 * PI * r), "%s cm" % d(PI * r * r * n / 360), "%s cm" % d(Lv * 2)],
                 "L = 2πr · %d/360 = 2 · 3,14 · %d · %d/360 = <b>%s cm</b>." % (n, r, n, d(Lv)))
    if t == "sector":
        A = PI * r * r * n / 360
        return M("¿Cuál es el área de un sector circular de %d° y %d cm de radio? (π ≈ 3,14)" % (n, r), "%s cm²" % d(A), ["%s cm²" % d(PI * r * r), "%s cm²" % d(2 * PI * r * n / 360), "%s cm²" % d(A * 2)],
                 "A = πr² · %d/360 = 3,14 · %d · %d/360 = <b>%s cm²</b>." % (n, r * r, n, d(A)))
    R2 = r + R.randint(1, 8)
    A = PI * (R2 * R2 - r * r)
    return M("¿Cuál es el área de una corona circular de radios %d cm y %d cm? (π ≈ 3,14)" % (R2, r), "%s cm²" % d(A), ["%s cm²" % d(PI * (R2 - r) ** 2), "%s cm²" % d(PI * R2 * R2), "%s cm²" % d(2 * PI * (R2 - r))],
             "A = π(R² − r²) = 3,14 · (%d − %d) = <b>%s cm²</b>." % (R2 * R2, r * r, d(A)))


seen = set()
sets = [("Elementos y posiciones", mix(R, seen, [(s_elementos, 20)])), ("Longitud de la circunferencia", mix(R, seen, [(lon, 20)])), ("Área del círculo", mix(R, seen, [(area, 14), (inv, 6)])),
        ("Arcos, sectores y coronas", mix(R, seen, [(s_arco, 20)])), ("Problemas", mix(R, seen, [(prob, 14), (s_arco, 6)]))]
body = L(["El <b>radio</b> va del centro a la circunferencia; el <b>diámetro</b> es el doble del radio.",
          "Longitud de la circunferencia: L = 2πr. Área del círculo: A = πr². Usamos π ≈ 3,14.",
          "Un arco o un sector de n° es la fracción n/360 de la circunferencia o del círculo."],
         [("Círculo de 5 cm de radio", ["L = 2 · 3,14 · 5", "A = 3,14 · 25"], "L = 31,4 cm; A = 78,5 cm²"), ("Sector de 90° y radio 4 cm", ["3,14 · 16 · 90/360"], "12,56 cm²")],
         [["Usar el diámetro como radio", "Si te dan el diámetro, divídelo entre 2."], ["Calcular 2πr para el área", "Área = πr²; 2πr es la longitud."], ["Olvidar la fracción del sector", "Multiplica por n/360."]],
         C6.circ(5))
faq = [("¿Qué diferencia hay entre circunferencia y círculo?", "La circunferencia es la línea curva; el círculo es la superficie que encierra."),
       ("¿Por qué usamos 3,14 para π?", "π es un número con infinitas cifras decimales; 3,14 es una buena aproximación para calcular.")]
unit(1, R, "circunferencia-y-circulo", "M", "Circunferencia y círculo: elementos y posiciones relativas; longitud de la circunferencia y del arco; área del círculo, del sector y de la corona circular",
     "Circunferencia y círculo", "Circunferencia y círculo",
     "Fichas de matemáticas de 1.º de ESO: elementos de la circunferencia, longitud, área del círculo, arcos, sectores, coronas y problemas. 100 ejercicios con soluciones.",
     "L = 2πr y A = πr²", "Con π ≈ 3,14.", body, faq, sets, 12)
