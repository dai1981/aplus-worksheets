# -*- coding: utf-8 -*-
"""
España Matemáticas 6.º de Primaria: Longitud de la circunferencia y área del círculo (Sentido de la medida)
El número π (≈ 3,14), longitud de la circunferencia L = 2 × π × r = π × d, área del círculo A = π × r², semicírculo,
problemas (ruedas, pistas, jardines).
Errores: usar el diámetro como radio, multiplicar r × 2 en lugar de r × r en el área, olvidar π.
"""
import random
from fractions import Fraction as F
from es_c3 import M, mix, lesson, make_unit, num, d

R = None
PI = F(314, 100)


def circ(r, lab="r"):
    return ("<div class='fig'><svg viewBox='0 0 200 170' width='200' role='img' aria-label='círculo con su %s'>"
            "<circle cx='100' cy='85' r='70' fill='#d6e2f6' stroke='#333' stroke-width='2'/><circle cx='100' cy='85' r='3' fill='#333'/>"
            "%s</svg></div>") % ("radio" if lab == "r" else "diámetro",
                                 "<line x1='100' y1='85' x2='170' y2='85' stroke='#c0392b' stroke-width='2.5'/><text x='135' y='78' font-size='14' font-weight='700' fill='#c0392b' text-anchor='middle'>%s cm</text>" % r if lab == "r" else
                                 "<line x1='30' y1='85' x2='170' y2='85' stroke='#c0392b' stroke-width='2.5'/><text x='100' y='78' font-size='14' font-weight='700' fill='#c0392b' text-anchor='middle'>%s cm</text>" % r)


def s1_pi():
    q, a, w = R.choice([("¿Cuántas veces cabe, más o menos, el diámetro en la longitud de una circunferencia?", "unas 3,14 veces (π)", ["2 veces", "4 veces", "10 veces"]),
                        ("¿Qué valor aproximado usamos para π?", "3,14", ["3,41", "2,14", "31,4"]),
                        ("¿Qué fórmula da la longitud de una circunferencia de radio r?", "2 × π × r", ["π × r × r", "π × r", "2 × r"]),
                        ("¿Qué fórmula da el área de un círculo de radio r?", "π × r × r", ["2 × π × r", "π × 2 × r", "r × r"]),
                        ("Si conoces el diámetro d, la longitud de la circunferencia es…", "π × d", ["2 × π × d", "π × d × d", "d × d"]),
                        ("¿En qué unidades se da el área de un círculo si el radio está en cm?", "cm²", ["cm", "cm³", "m"]),
                        ("Si el radio de un círculo se duplica, su longitud…", "se duplica", ["se cuadruplica", "no cambia", "se reduce a la mitad"])])
    return M(q, a, w, "Respuesta: <b>%s</b>." % a)


def s2_longitud():
    r = R.randint(1, 20)
    k = R.choice(["r", "r", "d"])
    L = 2 * PI * r
    if k == "r":
        return M(circ(r) + "Calcula la longitud de la circunferencia (π ≈ 3,14).", "%s cm" % d(L), ["%s cm" % d(PI * r), "%s cm" % d(PI * r * r), "%s cm" % d(4 * PI * r), "%s cm" % num(2 * r)],
                 "L = 2 × 3,14 × %d = <b>%s cm</b>." % (r, d(L)))
    return M(circ(2 * r, "d") + "Calcula la longitud de la circunferencia (π ≈ 3,14).", "%s cm" % d(L), ["%s cm" % d(2 * PI * 2 * r), "%s cm" % d(PI * r), "%s cm" % d(PI * 4 * r * r)],
             "L = 3,14 × %d = <b>%s cm</b>." % (2 * r, d(L)))


def s3_area():
    r = R.randint(1, 15)
    k = R.choice(["r", "r", "d", "semi"])
    A = PI * r * r
    if k == "r":
        return M(circ(r) + "Calcula el área del círculo (π ≈ 3,14).", "%s cm²" % d(A), ["%s cm²" % d(2 * PI * r), "%s cm²" % d(PI * 2 * r * 2 * r), "%s cm²" % d(PI * r), "%s cm²" % num(r * r)],
                 "A = 3,14 × %d × %d = <b>%s cm²</b>." % (r, r, d(A)))
    if k == "d":
        return M(circ(2 * r, "d") + "Calcula el área del círculo (π ≈ 3,14).", "%s cm²" % d(A), ["%s cm²" % d(PI * 4 * r * r), "%s cm²" % d(2 * PI * r), "%s cm²" % d(PI * r)],
                 "El radio es %d : 2 = %d; A = 3,14 × %d × %d = <b>%s cm²</b>." % (2 * r, r, r, r, d(A)))
    return M("¿Cuál es el área de un semicírculo de %d cm de radio (π ≈ 3,14)?" % r, "%s cm²" % d(A / 2), ["%s cm²" % d(A), "%s cm²" % d(PI * r), "%s cm²" % d(A / 4)], "3,14 × %d × %d : 2 = <b>%s cm²</b>." % (r, r, d(A / 2)))


def s4_inversa():
    r = R.randint(2, 20)
    k = R.choice(["L", "rL"])
    L = 2 * PI * r
    if k == "L":
        return M("Una circunferencia mide %s cm. ¿Cuánto mide su diámetro (π ≈ 3,14)?" % d(L), "%d cm" % (2 * r), ["%d cm" % r, "%d cm" % (4 * r), "%s cm" % d(L / 2)], "d = L : 3,14 = %s : 3,14 = <b>%d cm</b>." % (d(L), 2 * r))
    return M("Una circunferencia mide %s cm. ¿Cuánto mide su radio (π ≈ 3,14)?" % d(L), "%d cm" % r, ["%d cm" % (2 * r), "%d cm" % (r + 1), "%s cm" % d(L / 2)], "r = L : (2 × 3,14) = <b>%d cm</b>." % r)


def s5_problema():
    k = R.choice(["rueda", "vueltas", "pista", "pizza", "mesa", "fuente"])
    if k == "rueda":
        r = R.choice([20, 25, 30, 35, 40, 50])
        return M("La rueda de una bicicleta tiene %d cm de radio. ¿Cuánto avanza en una vuelta (π ≈ 3,14)?" % r, "%s cm" % d(2 * PI * r), ["%s cm" % d(PI * r), "%s cm" % d(PI * r * r), "%d cm" % (2 * r)], "2 × 3,14 × %d = <b>%s cm</b>." % (r, d(2 * PI * r)))
    if k == "vueltas":
        r, n = R.choice([25, 30, 40, 50]), R.choice([10, 100, 50])
        return M("Una rueda de %d cm de radio da %d vueltas. ¿Cuántos metros recorre (π ≈ 3,14)?" % (r, n), "%s m" % d(2 * PI * r * n / 100), ["%s m" % d(PI * r * n / 100), "%s m" % d(2 * PI * r * n), "%s m" % d(2 * PI * r * n / 1000)],
                 "Una vuelta: %s cm; %d vueltas: %s cm = <b>%s m</b>." % (d(2 * PI * r), n, d(2 * PI * r * n), d(2 * PI * r * n / 100)))
    if k == "pista":
        r = R.choice([10, 15, 20, 25, 30])
        return M("Una pista circular tiene %d m de radio. ¿Cuántos metros recorre quien da una vuelta (π ≈ 3,14)?" % r, "%s m" % d(2 * PI * r), ["%s m" % d(PI * r * r), "%s m" % d(PI * r), "%d m" % (4 * r)], "<b>%s m</b>." % d(2 * PI * r))
    if k == "pizza":
        dd = R.choice([20, 30, 40])
        return M("Una pizza redonda mide %d cm de diámetro. ¿Cuál es su superficie (π ≈ 3,14)?" % dd, "%s cm²" % d(PI * (dd // 2) ** 2), ["%s cm²" % d(PI * dd * dd), "%s cm²" % d(PI * dd), "%s cm²" % d(2 * PI * dd)],
                 "r = %d cm; 3,14 × %d × %d = <b>%s cm²</b>." % (dd // 2, dd // 2, dd // 2, d(PI * (dd // 2) ** 2)))
    if k == "mesa":
        r = R.choice([1, 2, 3])
        return M("Queremos poner una cinta alrededor de una mesa redonda de %d m de diámetro. ¿Cuántos metros de cinta hacen falta (π ≈ 3,14)?" % (2 * r), "%s m" % d(2 * PI * r), ["%s m" % d(PI * r * r), "%s m" % d(4 * PI * r), "%d m" % (2 * r)], "3,14 × %d = <b>%s m</b>." % (2 * r, d(2 * PI * r)))
    r = R.choice([2, 3, 4, 5, 6])
    return M("Una fuente circular tiene %d m de radio. ¿Qué superficie ocupa (π ≈ 3,14)?" % r, "%s m²" % d(PI * r * r), ["%s m²" % d(2 * PI * r), "%s m²" % d(PI * 2 * r * 2 * r), "%d m²" % (r * r)], "3,14 × %d × %d = <b>%s m²</b>." % (r, r, d(PI * r * r)))


def build(lv=6):
    global R
    R = random.Random(40018 + lv * 1000)
    seen = set()
    sets = [
        ("El número π", mix(R, seen, [(s1_pi, 7), (s2_longitud, 13)])),
        ("Longitud de la circunferencia", mix(R, seen, [(s2_longitud, 20)])),
        ("Área del círculo", mix(R, seen, [(s3_area, 20)])),
        ("Del resultado al radio", mix(R, seen, [(s4_inversa, 20)])),
        ("Problemas", mix(R, seen, [(s5_problema, 20)])),
    ]
    body = lesson(
        ["En cualquier circunferencia, la longitud dividida entre el diámetro da siempre el mismo número: <b>π</b> (pi), que vale aproximadamente <b>3,14</b>.",
         "Longitud de la circunferencia: <b>L = 2 × π × r</b> (o π × d).",
         "Área del círculo: <b>A = π × r × r</b>. Se mide en unidades cuadradas."],
        [("Longitud con r = 5 cm", ["2 × 3,14 × 5"], "31,4 cm"),
         ("Área con r = 5 cm", ["3,14 × 5 × 5"], "78,5 cm²")],
        [["Usar el diámetro como radio", "Si te dan el diámetro, divide entre 2 para el área."],
         ["Multiplicar r × 2 en el área", "Área: r × r (al cuadrado), no r × 2."],
         ["Olvidar las unidades cuadradas", "Longitud en cm; área en cm²."]],
        circ(5))
    faq = [("¿Qué es el número π?", "Es el número de veces que cabe el diámetro en la longitud de la circunferencia. Vale 3,14159… y en Primaria usamos 3,14."),
           ("¿Cómo se calcula el área de un círculo?", "Se multiplica π por el radio y otra vez por el radio: A = 3,14 × r × r.")]
    make_unit(R, "longitud-y-area-del-circulo", "M",
              "La circunferencia y el círculo: el número π; longitud de la circunferencia y área del círculo; resolución de problemas",
              "Longitud y área del círculo", "Longitud y área del círculo",
              "Fichas de matemáticas de 6.º de Primaria: el número π, longitud de la circunferencia, área del círculo, calcular el radio y problemas con ruedas y pistas. 100 ejercicios con soluciones.",
              "L = 2 × π × r. A = π × r × r", "π ≈ 3,14.",
              body, faq, sets, 18, grade="6-primaria")


if __name__ == "__main__":
    build(6)
