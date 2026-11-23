# -*- coding: utf-8 -*-
"""
España Matemáticas 6.º (y 5.º) de Primaria: Medidas de superficie (Sentido de la medida)
El metro cuadrado y sus múltiplos y submúltiplos (km², hm², dam², m², dm², cm², mm²), cada unidad es 100 veces la siguiente;
unidades agrarias (hectárea, área, centiárea); cambios de unidad; elegir la unidad; medir superficies con cuadrículas.
Errores: multiplicar por 10 en lugar de por 100, confundir la hectárea con el kilómetro cuadrado.
"""
import random
from fractions import Fraction as F
from es_c3 import M, mix, lesson, make_unit, num, d, table

R = None
LV = 6
U = ["km²", "hm²", "dam²", "m²", "dm²", "cm²", "mm²"]


def s1_cambio():
    i, j = sorted(R.sample(range(7), 2))
    if j - i > 3:
        return None
    if R.random() < 0.5:
        i, j = j, i
    f = F(100) ** (j - i)
    v = R.choice([F(R.randint(2, 99)), F(R.randint(11, 999), 10)]) if LV == 6 else F(R.randint(2, 99))
    r = v * f
    try:
        dr = d(r, 4)
    except ValueError:
        return None
    if r > 10 ** 7:
        return None
    w10 = v * (F(10) ** (j - i))
    return M("¿Cuántos %s son %s %s?" % (U[j], d(v), U[i]), "%s %s" % (dr, U[j]), ["%s %s" % (d(w10), U[j]), "%s %s" % (d(r * 10), U[j]), "%s %s" % (d(v / f), U[j]) if v / f >= F(1, 10 ** 4) else "%s %s" % (d(r / 10), U[j])],
             "Cada salto es × 100 o : 100. De %s a %s hay %d %s: <b>%s %s</b>." % (U[i], U[j], abs(j - i), "salto" if abs(j - i) == 1 else "saltos", dr, U[j]))


def s2_agrarias():
    k = R.choice(["ha_m2", "m2_ha", "ha", "a"])
    if k == "ha_m2":
        h = R.randint(2, 50)
        return M("¿Cuántos metros cuadrados tiene un campo de %d hectáreas?" % h, "%s m²" % num(h * 10000), ["%s m²" % num(h * 100), "%s m²" % num(h * 1000), "%s m²" % num(h * 100000)], "1 ha = 1 hm² = 10 000 m²: <b>%s m²</b>." % num(h * 10000))
    if k == "m2_ha":
        h = R.randint(2, 90) * 10000
        return M("¿Cuántas hectáreas son %s m²?" % num(h), "%d ha" % (h // 10000), ["%d ha" % (h // 1000), "%d ha" % (h // 100), "%s ha" % d(F(h, 100000))], "%s : 10 000 = <b>%d ha</b>." % (num(h), h // 10000))
    q, a, w = R.choice([("¿A qué unidad es igual una hectárea (ha)?", "al hectómetro cuadrado (hm²)", ["al kilómetro cuadrado (km²)", "al metro cuadrado (m²)", "al decámetro cuadrado (dam²)"]),
                        ("¿A qué unidad es igual un área (a)?", "al decámetro cuadrado (dam²)", ["al hectómetro cuadrado (hm²)", "al metro cuadrado (m²)", "al kilómetro cuadrado (km²)"]),
                        ("¿A qué unidad es igual una centiárea (ca)?", "al metro cuadrado (m²)", ["al decímetro cuadrado (dm²)", "al hectómetro cuadrado (hm²)", "al decámetro cuadrado (dam²)"]),
                        ("¿Cuántas áreas tiene una hectárea?", "100", ["10", "1000", "10 000"]),
                        ("¿Cuántos metros cuadrados tiene un área?", "100 m²", ["10 m²", "1000 m²", "10 000 m²"]),
                        ("¿Cuántas hectáreas tiene un kilómetro cuadrado?", "100 ha", ["10 ha", "1000 ha", "1 ha"])])
    return M(q, a, w, "Respuesta: <b>%s</b>." % a)


def s3_unidad():
    q, a, w = R.choice([("¿Qué unidad usarías para medir la superficie de un país?", "km²", ["m²", "cm²", "dm²"]),
                        ("¿Qué unidad usarías para medir la superficie de una hoja de papel?", "cm²", ["km²", "ha", "dam²"]),
                        ("¿Qué unidad usarías para medir la superficie de un piso?", "m²", ["km²", "mm²", "ha"]),
                        ("¿Qué unidad usarías para medir un campo de cultivo?", "hectáreas", ["cm²", "mm²", "dm²"]),
                        ("¿Qué unidad usarías para medir la superficie de un sello?", "cm²", ["m²", "ha", "km²"]),
                        ("¿Cuánto puede medir la superficie de un aula?", "60 m²", ["60 cm²", "60 km²", "6 ha"]),
                        ("¿Cuánto puede medir un campo de fútbol?", "7000 m²", ["70 m²", "7000 km²", "70 cm²"]),
                        ("¿Cuánto puede medir la pantalla de un móvil?", "90 cm²", ["90 m²", "9 dam²", "90 km²"]),
                        ("¿Cuánto mide un cuadrado de 1 m de lado?", "1 m² = 100 dm²", ["1 m² = 10 dm²", "1 m² = 1000 dm²", "1 m² = 4 dm²"])])
    return M(q, a, w, "Respuesta: <b>%s</b>." % a)


def cuadricula(cells, W=10, H=6):
    C = 22
    s = []
    for i in range(W + 1):
        s.append("<line x1='%d' y1='4' x2='%d' y2='%d' stroke='#bcd6e6'/>" % (4 + i * C, 4 + i * C, 4 + H * C))
    for j in range(H + 1):
        s.append("<line x1='4' y1='%d' x2='%d' y2='%d' stroke='#bcd6e6'/>" % (4 + j * C, 4 + W * C, 4 + j * C))
    for (x, y) in cells:
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='#9fd3a8' stroke='#2e7d32'/>" % (4 + x * C, 4 + y * C, C, C))
    return "<div class='fig'><svg viewBox='0 0 %d %d' width='%d' role='img' aria-label='figura en una cuadrícula'>%s</svg></div>" % (8 + W * C, 8 + H * C, 8 + W * C, "".join(s))


def s4_cuadricula():
    w, h = R.randint(2, 7), R.randint(2, 5)
    cells = [(1 + i, 0 + j) for i in range(w) for j in range(h)]
    extra = R.randint(0, min(3, w))
    cells += [(1 + i, h) for i in range(extra)]
    u = R.choice([1, 4, 25])
    lab = {1: "1 cm²", 4: "4 cm²", 25: "25 m²"}[u]
    unit = "cm²" if u in (1, 4) else "m²"
    a = len(cells) * u
    return M(cuadricula(cells) + "Cada cuadradito mide %s. ¿Cuál es la superficie de la figura verde?" % lab, "%d %s" % (a, unit), ["%d %s" % (len(cells), unit) if u > 1 else "%d %s" % (a + 1, unit), "%d %s" % (a + u, unit), "%d %s" % (a - u, unit), "%d %s" % (a * 2, unit)],
             "%d cuadraditos × %s = <b>%d %s</b>." % (len(cells), lab, a, unit))


def s5_problema():
    k = R.choice(["piso", "finca", "baldosas", "terreno"])
    if k == "piso":
        a, b = R.randint(3, 9), R.randint(3, 6)
        p = R.choice([15, 20, 25, 30])
        return M("Una habitación mide %d m por %d m. Poner suelo nuevo cuesta %d € el m². ¿Cuánto cuesta?" % (a, b, p), "%d €" % (a * b * p), ["%d €" % (2 * (a + b) * p), "%d €" % (a * b + p), "%d €" % (a * b)], "%d × %d = %d m²; %d × %d = <b>%d €</b>." % (a, b, a * b, a * b, p, a * b * p))
    if k == "finca":
        h = R.randint(2, 12)
        p = R.choice([3, 4, 5])
        return M("Una finca de %d ha se divide en %d parcelas iguales. ¿Cuántos m² tiene cada parcela?" % (h * p, p), "%s m²" % num(h * 10000), ["%s m²" % num(h * 100), "%d m²" % h, "%s m²" % num(h * p * 10000)], "%d ha : %d = %d ha = <b>%s m²</b>." % (h * p, p, h, num(h * 10000)))
    if k == "baldosas":
        a, b = R.randint(2, 6), R.randint(2, 5)
        return M("¿Cuántas baldosas cuadradas de 50 cm de lado hacen falta para un suelo de %d m por %d m?" % (a, b), str(a * b * 4), [str(a * b * 2), str(a * b), str(a * b * 100 // 50)], "Cada m² lleva 2 × 2 = 4 baldosas; %d × %d × 4 = <b>%d</b>." % (a, b, a * b * 4))
    m = R.randint(2, 9) * 1000
    return M("Un terreno mide %s m². ¿Cuántas áreas son?" % num(m), "%d a" % (m // 100), ["%d a" % (m // 10), "%d a" % (m // 1000), "%s a" % num(m)], "1 a = 100 m²; %s : 100 = <b>%d a</b>." % (num(m), m // 100))


def build(lv):
    global R, LV
    LV = lv
    R = random.Random(40014 + lv * 1000)
    seen = set()
    sets = [
        ("Medir con cuadrículas", mix(R, seen, [(s4_cuadricula, 20)])),
        ("Cambiar de unidad de superficie", mix(R, seen, [(s1_cambio, 20)])),
        ("Unidades agrarias", mix(R, seen, [(s2_agrarias, 12), (s1_cambio, 8)])),
        ("Elegir la unidad", mix(R, seen, [(s3_unidad, 9), (s4_cuadricula, 11)])),
        ("Problemas", mix(R, seen, [(s5_problema, 20)])),
    ]
    body = lesson(
        ["La unidad principal de superficie es el <b>metro cuadrado</b> (m²): un cuadrado de 1 m de lado.",
         "km², hm², dam², m², dm², cm², mm²: cada unidad es <b>100 veces</b> la siguiente. Por eso, en cada salto se multiplica o se divide por 100.",
         "Unidades agrarias: 1 hectárea (ha) = 1 hm² = 10 000 m²; 1 área (a) = 1 dam² = 100 m²; 1 centiárea (ca) = 1 m²."],
        [("3 m² → dm²", ["1 salto: × 100"], "300 dm²"),
         ("45 000 m² → ha", ["1 ha = 10 000 m²", "45 000 : 10 000"], "4,5 ha")],
        [["Multiplicar por 10", "1 m² = 100 dm², no 10 dm²."],
         ["Confundir ha y km²", "1 km² = 100 ha."],
         ["Escribir m en vez de m²", "La superficie se mide en unidades cuadradas."]],
        table(["km²", "hm² (ha)", "dam² (a)", "m² (ca)", "dm²", "cm²", "mm²"], [["× 100", "× 100", "× 100", "× 100", "× 100", "× 100", ""]]))
    faq = [("¿Por qué en las unidades de superficie se multiplica por 100?", "Porque 1 m² es un cuadrado de 10 dm × 10 dm, es decir, 100 dm². Lo mismo pasa entre cada unidad y la siguiente."),
           ("¿Cuántos metros cuadrados tiene una hectárea?", "10 000 m². Una hectárea es un cuadrado de 100 m de lado (un hectómetro cuadrado).")]
    make_unit(R, "medidas-de-superficie", "M",
              "Medida de la superficie: unidades del Sistema Métrico Decimal (km² a mm²), equivalencias, unidades agrarias; estimación y medida de superficies",
              "Medidas de superficie", "Medidas de superficie",
              "Fichas de matemáticas de %d.º de Primaria: el metro cuadrado, cambios de unidad de superficie, hectáreas y áreas, medir con cuadrículas y problemas. 100 ejercicios con soluciones." % lv,
              "Cada salto: × 100 o : 100", "1 ha = 10 000 m².",
              body, faq, sets, 14, grade="%d-primaria" % lv)


if __name__ == "__main__":
    build(6)
