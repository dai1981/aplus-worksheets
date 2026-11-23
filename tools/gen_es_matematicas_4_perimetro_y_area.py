# -*- coding: utf-8 -*-
"""
España Matemáticas 4.º de Primaria: Perímetro y área (Sentido de la medida)
El perímetro de un polígono (suma de los lados), del cuadrado y del rectángulo; el área contando cuadraditos,
el centímetro cuadrado y el metro cuadrado, el área del cuadrado y del rectángulo; lados que faltan; problemas.
Errores: confundir perímetro y área, sumar solo dos lados del rectángulo, escribir cm en lugar de cm².
"""
import random
from es_common import mcq, mix, lesson, make_unit, num, POR, DIV, Kids

R = random.Random(44020)
K = Kids(R)
CELL = 22


def cuadricula(cells, W=10, H=6, label="figura en una cuadrícula"):
    s = []
    for i in range(W + 1):
        s.append("<line x1='%d' y1='4' x2='%d' y2='%d' stroke='#bcd6e6' stroke-width='1'/>" % (4 + i * CELL, 4 + i * CELL, 4 + H * CELL))
    for j in range(H + 1):
        s.append("<line x1='4' y1='%d' x2='%d' y2='%d' stroke='#bcd6e6' stroke-width='1'/>" % (4 + j * CELL, 4 + W * CELL, 4 + j * CELL))
    for (x, y) in cells:
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='#9fd3a8' stroke='#2e7d32' stroke-width='1.5'/>" % (4 + x * CELL, 4 + y * CELL, CELL, CELL))
    w, h = 8 + W * CELL, 8 + H * CELL
    return "<div class='fig'><svg viewBox='0 0 %d %d' width='%d' role='img' aria-label='%s'>%s</svg></div>" % (w, h, w, label, "".join(s))


def perim_cells(cells):
    S = set(cells)
    p = 0
    for (x, y) in S:
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            if (x + dx, y + dy) not in S:
                p += 1
    return p


def random_shape():
    """figura conexa de cuadraditos"""
    n = R.randint(5, 14)
    S = {(R.randint(2, 6), R.randint(1, 3))}
    while len(S) < n:
        x, y = R.choice(sorted(S))
        dx, dy = R.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
        c = (x + dx, y + dy)
        if 0 <= c[0] < 10 and 0 <= c[1] < 6:
            S.add(c)
    return sorted(S)


def rect_cells(w, h, x0=1, y0=1):
    return [(x0 + i, y0 + j) for i in range(w) for j in range(h)]


def s1_cuadritos():
    k = R.choice(["area", "area", "per"])
    if R.random() < 0.5:
        w, h = R.randint(2, 7), R.randint(2, 4)
        cells = rect_cells(w, h, R.randint(0, 9 - w), R.randint(0, 5 - h))
    else:
        cells = random_shape()
    a, p = len(cells), perim_cells(cells)
    pic = cuadricula(cells)
    if k == "area":
        return mcq(pic + "Cada cuadradito es 1 cm². ¿Cuál es el área de la figura verde?", "%d cm²" % a, ["%d cm²" % p if p != a else "%d cm²" % (a + 2), "%d cm²" % (a + 1), "%d cm²" % (a - 1), "%d cm" % a],
                   "Contamos los cuadraditos: <b>%d cm²</b>." % a)
    return mcq(pic + "Cada cuadradito mide 1 cm de lado. ¿Cuál es el perímetro de la figura verde?", "%d cm" % p, ["%d cm" % a if a != p else "%d cm" % (p + 2), "%d cm" % (p + 2), "%d cm" % (p - 2), "%d cm²" % p],
               "Contamos los lados de cuadradito del borde: <b>%d cm</b>." % p)


def s2_perimetro():
    k = R.choice(["cuad", "rect", "tri", "poli", "regular"])
    if k == "cuad":
        l = R.randint(4, 60)
        return mcq("Un cuadrado tiene %d cm de lado. ¿Cuál es su perímetro?" % l, "%d cm" % (4 * l), ["%d cm" % (2 * l), "%d cm²" % (l * l), "%d cm" % (l + 4), "%d cm" % (l * l)],
                   "4 lados iguales: %d %s 4 = <b>%d cm</b>." % (l, POR, 4 * l))
    if k == "rect":
        a, b = R.randint(8, 60), R.randint(3, 30)
        if a == b:
            return None
        return mcq("Un rectángulo mide %d cm de largo y %d cm de ancho. ¿Cuál es su perímetro?" % (a, b), "%d cm" % (2 * (a + b)), ["%d cm" % (a + b), "%d cm" % (a * b), "%d cm" % (2 * a + b), "%d cm" % (a + 2 * b)],
                   "%d + %d + %d + %d = <b>%d cm</b>." % (a, b, a, b, 2 * (a + b)))
    if k == "tri":
        l = R.sample(range(4, 20), 3)
        if max(l) >= sum(l) - max(l):
            return None
        return mcq("Un triángulo tiene lados de %d cm, %d cm y %d cm. ¿Cuál es su perímetro?" % tuple(l), "%d cm" % sum(l), ["%d cm" % (l[0] * l[1]), "%d cm" % (sum(l) + 10), "%d cm" % (l[0] + l[1]), "%d cm" % (sum(l) - 1)],
                   "%d + %d + %d = <b>%d cm</b>." % (l[0], l[1], l[2], sum(l)))
    if k == "poli":
        n = R.choice([5, 6])
        l = [R.randint(3, 15) for _ in range(n)]
        return mcq("Un %s tiene lados de %s cm. ¿Cuál es su perímetro?" % ("pentágono" if n == 5 else "hexágono", ", ".join(map(str, l))), "%d cm" % sum(l), ["%d cm" % (sum(l) - l[-1]), "%d cm" % (sum(l) + 10), "%d cm" % (sum(l) + l[0]), "%d cm" % (max(l) * n)],
                   "Sumamos los %d lados: <b>%d cm</b>." % (n, sum(l)))
    n = R.choice([3, 5, 6, 8])
    l = R.randint(3, 25)
    nm = {3: "triángulo equilátero", 5: "pentágono regular", 6: "hexágono regular", 8: "octógono regular"}[n]
    return mcq("Un %s tiene %d cm de lado. ¿Cuál es su perímetro?" % (nm, l), "%d cm" % (n * l), ["%d cm" % ((n - 1) * l), "%d cm" % (n + l), "%d cm" % ((n + 1) * l), "%d cm" % (4 * l) if n != 4 else "%d cm" % (2 * l)],
               "%d lados iguales: %d %s %d = <b>%d cm</b>." % (n, l, POR, n, n * l))


def s3_area():
    k = R.choice(["rect", "rect", "cuad", "m2", "comp"])
    if k == "rect":
        a, b = R.randint(3, 25), R.randint(2, 15)
        if a == b:
            return None
        return mcq("Un rectángulo mide %d cm de largo y %d cm de ancho. ¿Cuál es su área?" % (a, b), "%d cm²" % (a * b), ["%d cm²" % (2 * (a + b)), "%d cm²" % (a + b), "%d cm" % (a * b), "%d cm²" % (a * b + a)],
                   "Área = largo %s ancho = %d %s %d = <b>%d cm²</b>." % (POR, a, POR, b, a * b))
    if k == "cuad":
        l = R.randint(2, 15)
        return mcq("Un cuadrado tiene %d cm de lado. ¿Cuál es su área?" % l, "%d cm²" % (l * l), ["%d cm²" % (4 * l) if 4 * l != l * l else "%d cm²" % (l * l + 1), "%d cm²" % (2 * l), "%d cm" % (l * l), "%d cm²" % (l + l + 1)],
                   "Área = lado %s lado = %d %s %d = <b>%d cm²</b>." % (POR, l, POR, l, l * l))
    if k == "m2":
        a, b = R.randint(3, 12), R.randint(2, 9)
        if a == b:
            return None
        return mcq("Una habitación rectangular mide %d m de largo y %d m de ancho. ¿Cuántos metros cuadrados tiene el suelo?" % (a, b), "%d m²" % (a * b), ["%d m²" % (2 * (a + b)), "%d m²" % (a + b), "%d cm²" % (a * b), "%d m²" % (a * b * 10)],
                   "%d %s %d = <b>%d m²</b>." % (a, POR, b, a * b))
    w1, h1 = R.randint(3, 5), R.randint(1, 2)
    w2, h2 = R.randint(1, w1 - 1), R.randint(1, 3)
    cells = rect_cells(w1, h1, 1, 5 - h1) + rect_cells(w2, h2, 1, 5 - h1 - h2)
    cells = sorted(set(cells))
    a = len(cells)
    return mcq(cuadricula(cells) + "La figura está formada por dos rectángulos. Cada cuadradito es 1 cm². ¿Cuál es su área?", "%d cm²" % a, ["%d cm²" % (w1 * h1), "%d cm²" % (a + w2), "%d cm²" % perim_cells(cells) if perim_cells(cells) != a else "%d cm²" % (a + 1), "%d cm²" % (a - 1)],
               "%d %s %d + %d %s %d = <b>%d cm²</b>." % (w1, POR, h1, w2, POR, h2, a))


def s4_falta():
    k = R.choice(["ladocuad", "anchoP", "anchoA", "ladoA"])
    if k == "ladocuad":
        l = R.randint(3, 30)
        return mcq("El perímetro de un cuadrado es %d cm. ¿Cuánto mide su lado?" % (4 * l), "%d cm" % l, ["%d cm" % (2 * l), "%d cm" % (4 * l - 4), "%d cm" % (l + 4), "%d cm" % (l * 4 // 3) if 4 * l % 3 == 0 and l * 4 // 3 != l else "%d cm" % (l - 1)],
                   "%d %s 4 = <b>%d cm</b>." % (4 * l, DIV, l))
    if k == "anchoP":
        a, b = R.randint(8, 30), R.randint(3, 15)
        if a == b:
            return None
        P = 2 * (a + b)
        return mcq("Un rectángulo tiene %d cm de perímetro y %d cm de largo. ¿Cuánto mide de ancho?" % (P, a), "%d cm" % b, ["%d cm" % (P - a), "%d cm" % (P - 2 * a), "%d cm" % (P // 2), "%d cm" % (b + 1)],
                   "%d − %d − %d = %d; %d %s 2 = <b>%d cm</b>." % (P, a, a, 2 * b, 2 * b, DIV, b))
    if k == "anchoA":
        a, b = R.randint(4, 15), R.randint(2, 12)
        if a == b:
            return None
        return mcq("Un rectángulo tiene %d cm² de área y %d cm de largo. ¿Cuánto mide de ancho?" % (a * b, a), "%d cm" % b, ["%d cm" % (a * b - a), "%d cm" % (a * b // 2), "%d cm" % (b + 1), "%d cm" % (a)],
                   "%d %s %d = <b>%d cm</b>." % (a * b, DIV, a, b))
    l = R.randint(2, 12)
    return mcq("Un cuadrado tiene %d cm² de área. ¿Cuánto mide su lado?" % (l * l), "%d cm" % l, ["%d cm" % (l * l // 4) if l * l % 4 == 0 and l * l // 4 != l else "%d cm" % (l + 2), "%d cm" % (l * l // 2) if l * l // 2 != l else "%d cm" % (l + 1), "%d cm" % (l + 1), "%d cm" % (l - 1)],
               "%d %s %d = %d: <b>%d cm</b>." % (l, POR, l, l * l, l))


def s5_problema():
    p, g = K.next()
    k = R.choice(["valla", "baldosas", "marco", "huerto", "cinta", "pintura", "campo"])
    if k == "valla":
        a, b = R.randint(10, 40), R.randint(5, 25)
        return mcq("Un huerto rectangular mide %d m de largo y %d m de ancho. ¿Cuántos metros de valla hacen falta para rodearlo?" % (a, b), "%d m" % (2 * (a + b)), ["%d m" % (a + b), "%d m" % (a * b), "%d m²" % (a * b), "%d m" % (2 * a + b)],
                   "Es el perímetro: 2 %s (%d + %d) = <b>%d m</b>." % (POR, a, b, 2 * (a + b)))
    if k == "baldosas":
        a, b = R.randint(3, 8), R.randint(3, 8)
        return mcq("Un patio mide %d m por %d m. ¿Cuántas baldosas de 1 m² hacen falta para cubrirlo?" % (a, b), str(a * b), [str(2 * (a + b)) if 2 * (a + b) != a * b else str(a * b + 1), str(a + b), str(a * b + a), str(a * b - 1)],
                   "Es el área: %d %s %d = <b>%d</b> baldosas." % (a, POR, b, a * b))
    if k == "marco":
        a, b = R.randint(15, 50), R.randint(10, 40)
        if a == b:
            return None
        return mcq("%s quiere poner una cinta alrededor de un cuadro de %d cm por %d cm. ¿Cuántos centímetros de cinta necesita?" % (p, a, b), "%d cm" % (2 * (a + b)), ["%d cm" % (a + b), "%d cm" % (a * b), "%d cm²" % (a * b), "%d cm" % (2 * (a + b) + 10)],
                   "Perímetro: %d + %d + %d + %d = <b>%d cm</b>." % (a, b, a, b, 2 * (a + b)))
    if k == "huerto":
        l = R.randint(4, 12)
        return mcq("Un jardín cuadrado tiene %d m de lado. ¿Cuántos metros cuadrados de césped hacen falta?" % l, "%d m²" % (l * l), ["%d m²" % (4 * l) if 4 * l != l * l else "%d m²" % (l * l + 4), "%d m²" % (2 * l), "%d m" % (l * l), "%d m²" % (l * l + l)],
                   "Área: %d %s %d = <b>%d m²</b>." % (l, POR, l, l * l))
    if k == "cinta":
        l = R.randint(5, 25)
        n = R.choice([3, 4, 5, 6])
        nm = {3: "triangular equilátera", 4: "cuadrada", 5: "pentagonal regular", 6: "hexagonal regular"}[n]
        return mcq("Una mesa %s tiene %d dm de lado. ¿Cuánto mide su contorno?" % (nm, l), "%d dm" % (n * l), ["%d dm" % (l * l), "%d dm" % (n + l), "%d dm" % ((n - 1) * l), "%d dm" % ((n + 1) * l)],
                   "%d %s %d = <b>%d dm</b>." % (l, POR, n, n * l))
    if k == "pintura":
        a, b = R.randint(3, 6), R.randint(2, 3)
        c = R.choice([2, 4, 5])
        A = a * b
        if A % c:
            return None
        return mcq("Una pared mide %d m de ancho y %d m de alto. Con un bote de pintura se pintan %d m². ¿Cuántos botes hacen falta?" % (a, b, c), str(A // c), [str(A), str(2 * (a + b) // c) if 2 * (a + b) // c != A // c else str(A // c + 1), str(A * c), str(A // c + 2)],
                   "Área: %d %s %d = %d m²; %d %s %d = <b>%d</b> botes." % (a, POR, b, A, A, DIV, c, A // c))
    a, b = R.choice([(100, 64), (105, 68), (90, 45), (110, 70), (40, 20)])
    return mcq("Un campo de deporte rectangular mide %d m de largo y %d m de ancho. %s le da una vuelta corriendo. ¿Cuántos metros recorre?" % (a, b, p), "%d m" % (2 * (a + b)), ["%d m" % (a + b), "%s m" % num(a * b), "%d m" % (2 * a + b), "%d m" % (4 * a)],
               "Perímetro: 2 %s (%d + %d) = <b>%d m</b>." % (POR, a, b, 2 * (a + b)))


def main():
    seen = set()
    sets = [
        ("Contar cuadraditos", mix(R, seen, [(s1_cuadritos, 20)])),
        ("El perímetro", mix(R, seen, [(s2_perimetro, 20)])),
        ("El área del cuadrado y del rectángulo", mix(R, seen, [(s3_area, 20)])),
        ("Lados que faltan", mix(R, seen, [(s4_falta, 20)])),
        ("Problemas", mix(R, seen, [(s5_problema, 20)])),
    ]
    body = lesson(
        ["El <b>perímetro</b> es la longitud del borde de una figura: se suman todos sus lados. Se mide en cm, m…",
         "El <b>área</b> es lo que ocupa la superficie de la figura. Se mide en unidades cuadradas: cm², m². Un cm² es un cuadrado de 1 cm de lado.",
         "Rectángulo: perímetro = largo + ancho + largo + ancho; área = largo × ancho. Cuadrado: perímetro = 4 × lado; área = lado × lado."],
        [("Rectángulo de 8 cm por 5 cm", ["Perímetro: 8 + 5 + 8 + 5 = 26 cm", "Área: 8 × 5 = 40 cm²"], "26 cm y 40 cm²"),
         ("Cuadrado de perímetro 36 cm", ["Lado: 36 : 4 = 9 cm", "Área: 9 × 9"], "81 cm²")],
        [["Confundir perímetro y área", "Perímetro: el borde (cm). Área: la superficie (cm²)."],
         ["Sumar solo dos lados", "El rectángulo tiene 4 lados: suma los 4."],
         ["Olvidar el ² en el área", "El área se mide en cm², no en cm."]],
        cuadricula(rect_cells(4, 3, 1, 1), 8, 5, "rectángulo de 4 por 3 cuadraditos"))
    faq = [("¿Qué diferencia hay entre perímetro y área?", "El perímetro es la medida del contorno (se suma la longitud de los lados) y el área es la medida de la superficie (se cuentan unidades cuadradas o se multiplica largo por ancho)."),
           ("¿Cómo se calcula el área de un rectángulo?", "Se multiplica el largo por el ancho. Un rectángulo de 6 cm por 4 cm tiene 6 × 4 = 24 cm².")]
    make_unit(R, "perimetro-y-area", "M",
              "Perímetro de polígonos; medida de superficies con unidades no convencionales y convencionales (cm², m²); área del cuadrado y del rectángulo; resolución de problemas",
              "Perímetro y área", "Perímetro y área",
              "Fichas de matemáticas de 4.º de Primaria: perímetro de polígonos, área contando cuadraditos, cm² y m², área del cuadrado y del rectángulo, lados que faltan y problemas. 100 ejercicios con soluciones.",
              "Perímetro: suma los lados. Área: largo × ancho", "El perímetro se mide en cm; el área, en cm².",
              body, faq, sets, 20)


if __name__ == "__main__":
    main()
