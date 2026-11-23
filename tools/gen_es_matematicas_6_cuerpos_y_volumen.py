# -*- coding: utf-8 -*-
"""
España Matemáticas 6.º (y 5.º) de Primaria: Cuerpos geométricos y volumen (Sentido espacial y de la medida)
Poliedros (prismas, pirámides, regulares) y cuerpos redondos; caras, aristas y vértices (fórmula de Euler: C + V = A + 2);
volumen contando cubos, volumen del cubo y del ortoedro; 6.º: unidades de volumen (m³, dm³, cm³) y relación con la capacidad (1 dm³ = 1 L).
Errores: sumar las dimensiones en vez de multiplicarlas, multiplicar por 10 entre unidades cúbicas (es × 1000), contar mal las aristas.
"""
import random
from es_c3 import M, mix, lesson, make_unit, num
from es_common import use, cuerpo_svg

R = None
LV = 6


def cubos(a, b, c):
    """ortoedro de cubitos en perspectiva"""
    s = []
    S, ox, oy = 18, 30, 150
    dx, dy = 9, -7
    for z in range(c):
        for y in range(b - 1, -1, -1):
            for x in range(a):
                X = ox + x * S + y * dx
                Y = oy - z * S + y * dy
                s.append("<polygon points='%d,%d %d,%d %d,%d %d,%d' fill='#cfe6d6' stroke='#333' stroke-width='1'/>" % (X, Y, X + S, Y, X + S, Y - S, X, Y - S))
                s.append("<polygon points='%d,%d %d,%d %d,%d %d,%d' fill='#e8f3ea' stroke='#333' stroke-width='1'/>" % (X, Y - S, X + S, Y - S, X + S + dx, Y - S + dy, X + dx, Y - S + dy))
                s.append("<polygon points='%d,%d %d,%d %d,%d %d,%d' fill='#a9cfb3' stroke='#333' stroke-width='1'/>" % (X + S, Y, X + S + dx, Y + dy, X + S + dx, Y - S + dy, X + S, Y - S))
    W = ox + a * S + b * dx + 20
    return "<div class='fig'><svg viewBox='0 0 %d 165' width='%d' role='img' aria-label='cuerpo hecho de cubitos'>%s</svg></div>" % (W, W, "".join(s))


def s1_euler():
    tipo = R.choice(["prisma", "piramide"])
    n = R.randint(3, 8)
    nm = {3: "triangular", 4: "cuadrangular", 5: "pentagonal", 6: "hexagonal", 7: "heptagonal", 8: "octogonal"}[n]
    if tipo == "prisma":
        C, V, A = n + 2, 2 * n, 3 * n
        full = "un prisma %s" % nm
    else:
        C, V, A = n + 1, n + 1, 2 * n
        full = "una pirámide %s" % nm
    i = R.randrange(3)
    w = ["caras", "vértices", "aristas"][i]
    v = [C, V, A][i]
    q = ("¿Cuántos %s tiene %s?" if w == "vértices" else "¿Cuántas %s tiene %s?") % (w, full)
    return M(q, str(v), [str(x) for x in (C, V, A) if x != v] + [str(v + 1), str(v - 1)], "%s tiene %d caras, %d vértices y %d aristas. Euler: %d + %d = %d + 2." % (full.capitalize(), C, V, A, C, V, A))


def s2_volumen_cubos():
    a, b, c = R.randint(2, 5), R.randint(1, 3), R.randint(1, 4)
    v = a * b * c
    return M(cubos(a, b, c) + "Cada cubito es 1 cm³. ¿Cuál es el volumen del cuerpo?", "%d cm³" % v, ["%d cm³" % (a + b + c), "%d cm³" % (a * c), "%d cm³" % (2 * (a * b + b * c + a * c)) if 2 * (a * b + b * c + a * c) != v else "%d cm³" % (v + 2), "%d cm³" % (v + a)],
             "%d × %d × %d = <b>%d cm³</b>." % (a, b, c, v))


def s3_formula():
    k = R.choice(["orto", "orto", "cubo", "falta"])
    a, b, c = R.randint(2, 15), R.randint(2, 10), R.randint(2, 12)
    if k == "cubo":
        return M("¿Cuál es el volumen de un cubo de %d cm de arista?" % a, "%s cm³" % num(a ** 3), ["%s cm³" % num(a * a), "%s cm³" % num(3 * a), "%s cm³" % num(6 * a * a), "%s cm³" % num(12 * a)], "%d × %d × %d = <b>%s cm³</b>." % (a, a, a, num(a ** 3)))
    if k == "falta":
        return M("Un ortoedro tiene %s cm³ de volumen, %d cm de largo y %d cm de ancho. ¿Cuánto mide de alto?" % (num(a * b * c), a, b), "%d cm" % c, ["%d cm" % (a * b * c - a - b), "%d cm" % (a * b), "%d cm" % (c + 1)], "%s : (%d × %d) = <b>%d cm</b>." % (num(a * b * c), a, b, c))
    return M("¿Cuál es el volumen de un ortoedro de %d cm de largo, %d cm de ancho y %d cm de alto?" % (a, b, c), "%s cm³" % num(a * b * c), ["%d cm³" % (a + b + c), "%s cm³" % num(a * b), "%s cm³" % num(2 * (a * b + b * c + a * c)), "%s cm³" % num(a * b * c + c)],
             "largo × ancho × alto = %d × %d × %d = <b>%s cm³</b>." % (a, b, c, num(a * b * c)))


def s4_unidades():
    k = R.choice(["m3dm3", "dm3cm3", "dm3L", "cm3mL", "m3L", "inv"])
    n = R.randint(2, 25)
    if k == "m3dm3":
        return M("¿Cuántos dm³ son %d m³?" % n, "%s dm³" % num(n * 1000), ["%s dm³" % num(n * 10), "%s dm³" % num(n * 100), "%s dm³" % num(n * 10000)], "Cada salto en volumen es × 1000: <b>%s dm³</b>." % num(n * 1000))
    if k == "dm3cm3":
        return M("¿Cuántos cm³ son %d dm³?" % n, "%s cm³" % num(n * 1000), ["%s cm³" % num(n * 10), "%s cm³" % num(n * 100), "%d cm³" % n], "× 1000: <b>%s cm³</b>." % num(n * 1000))
    if k == "dm3L":
        return M("¿Cuántos litros caben en un recipiente de %d dm³?" % n, "%d L" % n, ["%s L" % num(n * 1000), "%s L" % num(n * 10), "%s L" % num(n * 100)], "1 dm³ = 1 L: <b>%d L</b>." % n)
    if k == "cm3mL":
        return M("¿Cuántos mililitros son %d cm³?" % (n * 10), "%d mL" % (n * 10), ["%d mL" % n, "%s mL" % num(n * 10000), "%d mL" % (n * 100)], "1 cm³ = 1 mL: <b>%d mL</b>." % (n * 10))
    if k == "m3L":
        return M("¿Cuántos litros caben en un depósito de %d m³?" % n, "%s L" % num(n * 1000), ["%d L" % n, "%s L" % num(n * 100), "%s L" % num(n * 1000000)], "1 m³ = 1000 dm³ = 1000 L: <b>%s L</b>." % num(n * 1000))
    return M("¿Cuántos dm³ son %s cm³?" % num(n * 1000), "%d dm³" % n, ["%d dm³" % (n * 10), "%d dm³" % (n * 100), "%s dm³" % num(n * 1000)], ": 1000: <b>%d dm³</b>." % n)


def s5_problema():
    k = R.choice(["acuario", "caja", "piscina", "cubitos", "tetrabrik"] if LV == 6 else ["caja", "cubitos", "acuario"])
    if k == "acuario":
        a, b, c = R.choice([(50, 30, 40), (60, 30, 40), (80, 40, 50), (40, 20, 30), (100, 40, 50)])
        v = a * b * c
        if LV == 6:
            return M("Un acuario mide %d cm × %d cm × %d cm. ¿Cuántos litros de agua caben?" % (a, b, c), "%s L" % num(v // 1000), ["%s L" % num(v), "%s L" % num(v // 100), "%d L" % (a + b + c)], "%s cm³ = %s dm³ = <b>%s L</b>." % (num(v), num(v // 1000), num(v // 1000)))
        return M("Un acuario mide %d cm × %d cm × %d cm. ¿Cuál es su volumen en cm³?" % (a, b, c), "%s cm³" % num(v), ["%d cm³" % (a + b + c), "%s cm³" % num(a * b), "%s cm³" % num(v // 10)], "%d × %d × %d = <b>%s cm³</b>." % (a, b, c, num(v)))
    if k == "caja":
        a, b, c = R.randint(2, 6), R.randint(2, 5), R.randint(2, 4)
        return M("En una caja caben %d cubos de largo, %d de ancho y %d de alto. ¿Cuántos cubos caben en total?" % (a, b, c), str(a * b * c), [str(a + b + c), str(a * b), str(a * b * c + a)], "%d × %d × %d = <b>%d</b>." % (a, b, c, a * b * c))
    if k == "piscina":
        a, b, c = R.choice([(10, 5, 2), (8, 4, 2), (12, 6, 2), (20, 10, 2), (25, 10, 2)])
        v = a * b * c
        return M("Una piscina mide %d m de largo, %d m de ancho y %d m de profundidad. ¿Cuántos litros caben?" % (a, b, c), "%s L" % num(v * 1000), ["%d L" % v, "%s L" % num(v * 100), "%s L" % num(v * 1000000)], "%d m³ = <b>%s L</b>." % (v, num(v * 1000)))
    if k == "cubitos":
        a = R.randint(2, 6)
        return M("¿Cuántos cubitos de 1 cm de arista forman un cubo de %d cm de arista?" % a, str(a ** 3), [str(a * a), str(6 * a), str(a * 3)], "%d × %d × %d = <b>%d</b>." % (a, a, a, a ** 3))
    a, b, c = R.choice([(10, 5, 20), (6, 4, 10), (8, 5, 25)])
    v = a * b * c
    return M("Un brik mide %d cm × %d cm × %d cm. ¿Cuántos mililitros caben?" % (a, b, c), "%s mL" % num(v), ["%s mL" % num(v // 10), "%d mL" % (a + b + c), "%s mL" % num(v * 10)], "%s cm³ = <b>%s mL</b>." % (num(v), num(v)))


def build(lv):
    global R, LV
    LV = lv
    R = random.Random(40019 + lv * 1000)
    nombre, cual, desar = use("gen_es_matematicas_4_cuerpos_geometricos", 40119 + lv * 1000, "s1_nombre", "s6_cual", "s5_desarrollo")
    seen = set()
    sets = [
        ("Poliedros y cuerpos redondos", mix(R, seen, [(nombre, 6), (desar, 5), (cual, 6), (s1_euler, 3)])),
        ("Caras, vértices y aristas", mix(R, seen, [(s1_euler, 20)])),
        ("Volumen con cubitos", mix(R, seen, [(s2_volumen_cubos, 20)])),
        ("Volumen del cubo y del ortoedro" if lv == 5 else "Unidades de volumen y capacidad", mix(R, seen, [(s3_formula, 20)] if lv == 5 else [(s4_unidades, 12), (s3_formula, 8)])),
        ("Problemas", mix(R, seen, [(s5_problema, 20)])),
    ]
    think = ["Los <b>poliedros</b> tienen todas sus caras planas (prismas, pirámides). Los <b>cuerpos redondos</b> tienen superficies curvas (cilindro, cono, esfera).",
             "Un prisma de base de n lados tiene n + 2 caras, 2n vértices y 3n aristas. En todo poliedro: <b>caras + vértices = aristas + 2</b> (Euler).",
             "El <b>volumen</b> es el espacio que ocupa un cuerpo. Ortoedro: <b>largo × ancho × alto</b>. Cubo: arista × arista × arista."]
    if lv == 6:
        think.append("m³, dm³, cm³: cada unidad es <b>1000 veces</b> la siguiente. 1 dm³ = 1 L y 1 cm³ = 1 mL.")
    body = lesson(think,
                  [("Ortoedro de 5 cm × 4 cm × 3 cm", ["5 × 4 × 3"], "60 cm³"),
                   ("Prisma hexagonal", ["caras 6 + 2 = 8; vértices 12; aristas 18", "8 + 12 = 18 + 2"], "8 caras, 12 vértices, 18 aristas")],
                  [["Sumar las dimensiones", "El volumen se multiplica: 5 × 4 × 3, no 5 + 4 + 3."],
                   ["Multiplicar por 10 entre unidades cúbicas" if lv == 6 else "Confundir prisma y pirámide", "1 dm³ = 1000 cm³." if lv == 6 else "Prisma: 2 bases. Pirámide: 1 base y un vértice."],
                   ["Contar mal las aristas", "Cuenta las de las bases y después las laterales."]],
                  cubos(4, 2, 3))
    faq = [("¿Cómo se calcula el volumen de un ortoedro?", "Se multiplican sus tres dimensiones: largo × ancho × alto. Si están en cm, el volumen está en cm³."),
           ("¿Qué relación hay entre volumen y capacidad?", "Un decímetro cúbico (dm³) equivale a un litro (L), y un centímetro cúbico (cm³), a un mililitro (mL).")]
    make_unit(R, "cuerpos-y-volumen", "E",
              "Cuerpos geométricos: poliedros y cuerpos redondos, elementos y relación de Euler; volumen del cubo y del ortoedro" + ("; unidades de volumen y su relación con la capacidad" if lv == 6 else ""),
              "Cuerpos geométricos y volumen", "Cuerpos y volumen",
              "Fichas de matemáticas de %d.º de Primaria: poliedros y cuerpos redondos, caras, vértices y aristas, volumen con cubitos, volumen del cubo y del ortoedro%s y problemas. 100 ejercicios con soluciones." % (lv, ", m³, dm³ y litros" if lv == 6 else ""),
              "Volumen: largo × ancho × alto", "1 dm³ = 1 L." if lv == 6 else "Caras + vértices = aristas + 2.",
              body, faq, sets, 19, grade="%d-primaria" % lv)


if __name__ == "__main__":
    build(6)
