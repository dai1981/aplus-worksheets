# -*- coding: utf-8 -*-
"""
España Matemáticas 6.º (y 5.º) de Primaria: Medidas de longitud, masa y capacidad (Sentido de la medida)
Unidades del Sistema Métrico Decimal (km … mm, kg … mg, t, kL … mL), cambios de unidad con decimales,
expresiones complejas e incomplejas, comparar y ordenar medidas, elegir la unidad, problemas.
Errores: mover la coma hacia el lado equivocado, contar mal los saltos entre unidades, sumar medidas en unidades distintas.
"""
import random
from fractions import Fraction as F
from es_c3 import M, mix, lesson, make_unit, num, d, table

R = None
LV = 6
ESC = {"L": ["km", "hm", "dam", "m", "dm", "cm", "mm"], "M": ["kg", "hg", "dag", "g", "dg", "cg", "mg"], "C": ["kL", "hL", "daL", "L", "dL", "cL", "mL"]}
PAIRS = {"L": [("km", "m"), ("m", "cm"), ("m", "mm"), ("cm", "mm"), ("km", "hm"), ("dm", "cm"), ("hm", "m"), ("m", "dm")],
         "M": [("kg", "g"), ("g", "mg"), ("kg", "dag"), ("hg", "g"), ("g", "cg"), ("kg", "hg")],
         "C": [("L", "mL"), ("L", "cL"), ("L", "dL"), ("kL", "L"), ("hL", "L"), ("dL", "mL")]}


def val():
    k = R.choice([1, 2, 2, 3] if LV == 6 else [1, 1, 2])
    return F(R.randint(10 ** k + 1, 50 * 10 ** k), 10 ** k)


def s1_cambio():
    m = R.choice("LMC")
    a, b = R.choice(PAIRS[m])
    if R.random() < 0.5:
        a, b = b, a
    i, j = ESC[m].index(a), ESC[m].index(b)
    f = F(10) ** (j - i)
    v = val()
    r = v * f
    if r < F(1, 10) or r > 100000:
        return None
    try:
        d(r, 3)
        return M("¿Cuántos %s son %s %s?" % (b, d(v), a), "%s %s" % (d(r), b), ["%s %s" % (d(v / f), b), "%s %s" % (d(r * 10), b), "%s %s" % (d(r / 10), b)],
                 "De %s a %s %s por %s: <b>%s %s</b>." % (a, b, "multiplicamos" if f > 1 else "dividimos", num(int(f if f > 1 else 1 / f)), d(r), b))
    except ValueError:
        return None


def s2_complejas():
    k = R.choice(["kmm", "mcm", "kgg", "lml", "inv"])
    if k == "inv":
        n = R.randint(1001, 9999)
        u = R.choice([("m", "km", 1000), ("g", "kg", 1000), ("mL", "L", 1000), ("cm", "m", 100)])
        big, small = divmod(n, u[2])
        if small == 0:
            return None
        return M("Expresa %s %s en forma compleja." % (num(n), u[0]), "%d %s y %d %s" % (big, u[1], small, u[0]), ["%d %s y %d %s" % (big * 10, u[1], small // 10, u[0]) if small >= 10 else "%d %s y %d %s" % (big + 1, u[1], small, u[0]), "%d %s y %d %s" % (small, u[1], big, u[0]), "%d %s y %d %s" % (big, u[1], small * 10, u[0])],
                 "%s %s = <b>%d %s y %d %s</b>." % (num(n), u[0], big, u[1], small, u[0]))
    big, small, f = {"kmm": ("km", "m", 1000), "mcm": ("m", "cm", 100), "kgg": ("kg", "g", 1000), "lml": ("L", "mL", 1000)}[k]
    a, b = R.randint(1, 9), R.randint(1, f - 1)
    t = a * f + b
    return M("¿Cuántos %s son %d %s y %d %s?" % (small, a, big, b, small), "%s %s" % (num(t), small), ["%s %s" % (num(a * 10 + b) if a * 10 + b != t else num(t + f), small), "%s %s" % (num(a + b), small), "%s %s" % (num(a * f * 10 + b), small)],
             "%d %s = %s %s; %s + %d = <b>%s %s</b>." % (a, big, num(a * f), small, num(a * f), b, num(t), small))


def s3_comparar():
    m = R.choice("LMC")
    a, b = R.choice(PAIRS[m])
    i, j = ESC[m].index(a), ESC[m].index(b)
    f = 10 ** (j - i)
    x = val()
    y = x * f + R.choice([F(-1, 1), F(1, 1), 0, F(f, 10)])
    if y <= 0:
        return None
    A, B = "%s %s" % (d(x), a), "%s %s" % (d(y), b)
    xv = x * f
    s = "&gt;" if xv > y else "&lt;" if xv < y else "="
    ok = "%s %s %s" % (A, s, B)
    return M("Compara %s y %s." % (A, B), ok, ["%s %s %s" % (A, t, B) for t in ("&gt;", "&lt;", "=") if t != s] + ["no se pueden comparar"], "%s = %s %s: <b>%s</b>." % (A, d(xv), b, ok))


def s4_unidad():
    q, a, w = R.choice([("¿Qué unidad usarías para medir la distancia entre Madrid y Valencia?", "kilómetros", ["metros", "centímetros", "milímetros"]),
                        ("¿Qué unidad usarías para medir la masa de un camión cargado?", "toneladas", ["gramos", "miligramos", "kilolitros"]),
                        ("¿Qué unidad usarías para medir el grosor de una moneda?", "milímetros", ["metros", "kilómetros", "decámetros"]),
                        ("¿Qué unidad usarías para medir el agua de una piscina?", "kilolitros", ["mililitros", "centilitros", "gramos"]),
                        ("¿Qué unidad usarías para medir un medicamento en pastillas?", "miligramos", ["kilogramos", "toneladas", "litros"]),
                        ("¿Cuántos kilos son una tonelada?", "1000 kg", ["100 kg", "10 kg", "10 000 kg"]),
                        ("¿Cuántos mililitros tiene un litro?", "1000 mL", ["100 mL", "10 mL", "10 000 mL"]),
                        ("¿Cuántos metros tiene un kilómetro?", "1000 m", ["100 m", "10 m", "10 000 m"]),
                        ("¿Cuántos gramos tiene un kilogramo?", "1000 g", ["100 g", "10 g", "10 000 g"]),
                        ("¿Cuántos centilitros tiene un litro?", "100 cL", ["10 cL", "1000 cL", "1 cL"]),
                        ("¿Cuántos milímetros tiene un metro?", "1000 mm", ["100 mm", "10 mm", "10 000 mm"]),
                        ("¿Cuántos litros caben en un decímetro cúbico?", "1 L", ["10 L", "100 L", "1000 L"]),
                        ("¿Cuánto puede medir de alto un aula?", "3 m", ["3 cm", "30 m", "3 km"]),
                        ("¿Cuánto puede pesar un balón de fútbol?", "450 g", ["450 kg", "45 mg", "4,5 t"])])
    return M(q, a, w, "Respuesta: <b>%s</b>." % a)


def s5_problema():
    k = R.choice(["carrera", "botellas", "paquete", "cuerda", "receta", "camion"])
    if k == "carrera":
        a, b = F(R.randint(15, 95), 10), R.randint(200, 900)
        return M("Lucía corre %s km y después %d m más. ¿Cuántos metros corre en total?" % (d(a), b), "%s m" % num(int(a * 1000) + b), ["%s m" % num(int(a * 100) + b), "%s m" % d(a + b), "%s m" % num(int(a * 1000) + b * 10)],
                 "%s km = %s m; %s + %d = <b>%s m</b>." % (d(a), num(int(a * 1000)), num(int(a * 1000)), b, num(int(a * 1000) + b)))
    if k == "botellas":
        v = R.choice([25, 33, 50, 75])
        n = R.choice([6, 12, 24, 4, 8])
        t = F(v * n, 100)
        return M("Una caja tiene %d latas de %d cL. ¿Cuántos litros hay?" % (n, v), "%s L" % d(t), ["%s L" % num(v * n), "%s L" % d(t * 10), "%s L" % d(t / 10)], "%d × %d = %s cL = <b>%s L</b>." % (n, v, num(v * n), d(t)))
    if k == "paquete":
        g = R.choice([125, 250, 400, 500, 750])
        n = R.randint(2, 8)
        t = F(g * n, 1000)
        return M("Compramos %d paquetes de %d g de arroz. ¿Cuántos kilos son?" % (n, g), "%s kg" % d(t), ["%s kg" % num(g * n), "%s kg" % d(t * 10), "%s kg" % d(t / 10)], "%d × %d = %s g = <b>%s kg</b>." % (n, g, num(g * n), d(t)))
    if k == "cuerda":
        L = R.randint(3, 9)
        c = R.choice([25, 40, 50, 75, 125])
        if c * 2 > L * 100:
            return None
        n = L * 100 // c
        return M("Una cuerda mide %d m. ¿Cuántos trozos de %d cm se pueden cortar?" % (L, c), str(n), [str(L * 10 // c) if L * 10 // c else str(n + 1), str(n * 10), str(L * c)], "%d m = %d cm; %d : %d = <b>%d</b>%s." % (L, L * 100, L * 100, c, n, " (sobran %d cm)" % (L * 100 % c) if L * 100 % c else ""))
    if k == "receta":
        a, b = R.choice([F(3, 4), F(1, 2), F(1, 4)]), R.choice([150, 200, 300, 350])
        return M("Una receta lleva %s kg de harina y %d g de azúcar. ¿Cuántos gramos pesan juntos?" % (d(a), b), "%s g" % num(int(a * 1000) + b), ["%s g" % num(int(a * 100) + b), "%s g" % d(a + b), "%s g" % num(int(a * 1000) - b)],
                 "%s kg = %d g; %d + %d = <b>%s g</b>." % (d(a), int(a * 1000), int(a * 1000), b, num(int(a * 1000) + b)))
    c = R.randint(20, 60)
    w = R.choice([25, 40, 50])
    t = F(c * w, 1000)
    return M("Un camión lleva %d sacos de %d kg. ¿Cuántas toneladas lleva?" % (c, w), "%s t" % d(t), ["%s t" % num(c * w), "%s t" % d(t * 10), "%s t" % d(t / 10)], "%d × %d = %s kg = <b>%s t</b>." % (c, w, num(c * w), d(t)))


def build(lv):
    global R, LV
    LV = lv
    R = random.Random(40013 + lv * 1000)
    seen = set()
    sets = [
        ("Cambiar de unidad", mix(R, seen, [(s1_cambio, 20)])),
        ("Más cambios de unidad", mix(R, seen, [(s1_cambio, 20)])),
        ("Forma compleja e incompleja", mix(R, seen, [(s2_complejas, 20)])),
        ("Comparar medidas y elegir la unidad", mix(R, seen, [(s3_comparar, 10), (s4_unidad, 10)])),
        ("Problemas", mix(R, seen, [(s5_problema, 20)])),
    ]
    body = lesson(
        ["Longitud: km, hm, dam, <b>m</b>, dm, cm, mm. Masa: kg, hg, dag, <b>g</b>, dg, cg, mg (y la tonelada: 1 t = 1000 kg). Capacidad: kL, hL, daL, <b>L</b>, dL, cL, mL.",
         "Cada unidad es 10 veces la siguiente. Para pasar a una unidad <b>menor</b>, multiplica por 10 por cada salto (la coma va a la derecha). Para pasar a una <b>mayor</b>, divide (la coma va a la izquierda).",
         "Forma compleja: 3 km y 250 m. Forma incompleja: 3250 m o 3,25 km."],
        [("3,45 km → m", ["De km a m hay 3 saltos: × 1000"], "3450 m"),
         ("750 g → kg", ["De g a kg hay 3 saltos: : 1000"], "0,75 kg")],
        [["Mover la coma al lado equivocado", "Al pasar a una unidad menor, el número se hace mayor."],
         ["Contar mal los saltos", "De m a mm hay 3 saltos: × 1000."],
         ["Sumar medidas distintas", "2 kg + 300 g = 2300 g, no 302."]],
        table(["km", "hm", "dam", "m", "dm", "cm", "mm"], [["1000 m", "100 m", "10 m", "1 m", "0,1 m", "0,01 m", "0,001 m"]]))
    faq = [("¿Cómo se pasa de una unidad a otra?", "Se cuentan los saltos entre las dos unidades en la escala. Hacia una unidad menor se multiplica por 10 en cada salto; hacia una mayor se divide entre 10."),
           ("¿Qué es una medida en forma compleja?", "Una medida expresada con varias unidades, como 2 m y 35 cm. En forma incompleja se usa una sola unidad: 235 cm o 2,35 m.")]
    make_unit(R, "medidas-de-longitud-masa-y-capacidad", "M",
              "Unidades del Sistema Métrico Decimal de longitud, masa y capacidad: equivalencias, cambios de unidad con números decimales, expresiones complejas e incomplejas, comparación y elección de la unidad adecuada",
              "Longitud, masa y capacidad", "Longitud, masa y capacidad",
              "Fichas de matemáticas de %d.º de Primaria: cambios de unidad de longitud, masa y capacidad con decimales, forma compleja e incompleja, comparar medidas y problemas. 100 ejercicios con soluciones." % lv,
              "Cada salto: × 10 o : 10", "A una unidad menor, la coma a la derecha.",
              body, faq, sets, 13, grade="%d-primaria" % lv)


if __name__ == "__main__":
    build(6)
