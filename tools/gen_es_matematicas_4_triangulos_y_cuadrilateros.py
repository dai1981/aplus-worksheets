# -*- coding: utf-8 -*-
"""
España Matemáticas 4.º de Primaria: Triángulos y cuadriláteros (Sentido espacial)
Polígonos (lados, vértices, ángulos, diagonales; regulares e irregulares), clasificar triángulos por sus lados
(equilátero, isósceles, escaleno) y por sus ángulos (acutángulo, rectángulo, obtusángulo), la suma de los ángulos de un triángulo,
cuadriláteros: paralelogramos (cuadrado, rectángulo, rombo, romboide), trapecios y trapezoides; circunferencia y círculo.
Errores: pensar que el cuadrado no es un rectángulo, confundir rombo y cuadrado girado, confundir circunferencia y círculo.
"""
import random
from es_common import mcq, mix, lesson, make_unit, relabel, fig, bank
import gen_au_maths_y5_angles as AU

R = random.Random(44019)
LADOS = ["equilátero", "isósceles", "escaleno"]
ANG = ["acutángulo", "rectángulo", "obtusángulo"]
CUAD = ["cuadrado", "rectángulo", "rombo", "romboide", "trapecio isósceles", "trapecio rectángulo", "trapezoide"]


def tri(a, b, rot=0, ticks=(), base=150):
    pts = AU.tri_pts(a, b, base, rot)
    c = 180 - a - b
    rights = tuple(i for i, v in enumerate((a, b, c)) if v == 90)
    return fig(relabel(AU.shape_svg(pts, {}, "un triángulo", rights=rights, ticks=ticks), "un triángulo"))


def s1_lados():
    k = R.choice(LADOS)
    if k == "equilátero":
        a, b, t = 60, 60, ((0, 1), (1, 1), (2, 1))
    elif k == "isósceles":
        a = R.choice([35, 40, 50, 55, 65, 70, 75])
        b, t = a, ((1, 1), (2, 1))
    else:
        while True:
            a, b = R.randint(30, 80), R.randint(30, 80)
            if abs(a - b) >= 12 and abs(180 - 2 * a - b) >= 12 and abs(180 - a - 2 * b) >= 12 and a + b != 90:
                break
        t = ()
    if R.random() < 0.5:
        return mcq(tri(a, b, R.choice([0, 0, 10, -10]), ticks=t) + "Las rayitas indican los lados iguales. ¿Qué triángulo es según sus lados?", k, [x for x in LADOS if x != k] + ["rectángulo"],
                   "%s: es <b>%s</b>." % ({"equilátero": "Tres lados iguales", "isósceles": "Dos lados iguales", "escaleno": "Ningún lado igual"}[k], k))
    if k == "equilátero":
        l = [R.randint(3, 12)] * 3
    elif k == "isósceles":
        x, y = R.sample(range(4, 13), 2)
        if 2 * x <= y:
            return None
        l = [x, x, y]
        R.shuffle(l)
    else:
        l = R.sample(range(4, 14), 3)
        if max(l) >= sum(l) - max(l):
            return None
    return mcq("Un triángulo tiene lados de %s cm. ¿Qué triángulo es?" % ", ".join(map(str, l)), k, [x for x in LADOS if x != k] + ["obtusángulo"],
               "%s: es <b>%s</b>." % ({"equilátero": "Tres lados iguales", "isósceles": "Dos lados iguales", "escaleno": "Tres lados distintos"}[k], k))


def s1_angulos():
    k = R.choice(ANG)
    if k == "rectángulo":
        a = R.choice([30, 35, 40, 50, 55, 60])
        b = 90 if R.random() < 0.5 else 90 - a
        if b != 90:
            a, b = a, b
    elif k == "acutángulo":
        while True:
            a, b = R.randint(45, 80), R.randint(45, 80)
            if 180 - a - b < 85 and 180 - a - b > 30:
                break
    else:
        a = R.choice([100, 110, 115, 120, 130])
        b = R.choice([20, 25, 30])
    angs = (a, b, 180 - a - b)
    if R.random() < 0.5:
        return mcq(tri(a, b, R.choice([0, 0, 10])) + "¿Qué triángulo es según sus ángulos?", k, [x for x in ANG if x != k] + ["isósceles"],
                   "%s: es <b>%s</b>." % ({"acutángulo": "Tres ángulos agudos", "rectángulo": "Un ángulo recto", "obtusángulo": "Un ángulo obtuso"}[k], k))
    return mcq("Un triángulo tiene ángulos de %d°, %d° y %d°. ¿Qué triángulo es según sus ángulos?" % angs, k, [x for x in ANG if x != k] + ["equilátero"],
               "%s: es <b>%s</b>." % ({"acutángulo": "Los tres son agudos", "rectángulo": "Tiene un ángulo de 90°", "obtusángulo": "Tiene un ángulo de más de 90°"}[k], k))


def s2_suma():
    k = R.choice(["tercero", "tercero", "rect", "equi", "iso"])
    if k == "tercero":
        a, b = R.randint(25, 100), R.randint(25, 80)
        c = 180 - a - b
        if c < 10:
            return None
        return mcq("Dos ángulos de un triángulo miden %d° y %d°. ¿Cuánto mide el tercero?" % (a, b), "%d°" % c, ["%d°" % (360 - a - b), "%d°" % (a + b), "%d°" % (c + 10), "%d°" % (90 - a) if a < 90 and 90 - a != c else "%d°" % (c - 10)],
                   "Los ángulos de un triángulo suman 180°: 180° − %d° − %d° = <b>%d°</b>." % (a, b, c))
    if k == "rect":
        a = R.randint(20, 70)
        return mcq("Un triángulo rectángulo tiene un ángulo de %d°. ¿Cuánto mide el otro ángulo agudo?" % a, "%d°" % (90 - a), ["%d°" % (180 - a), "%d°" % a, "%d°" % (270 - a)],
                   "180° − 90° − %d° = <b>%d°</b>." % (a, 90 - a))
    if k == "equi":
        return mcq("¿Cuánto mide cada ángulo de un triángulo equilátero?", "60°", ["90°", "45°", "180°", "120°"], "Los tres son iguales: 180° : 3 = <b>60°</b>.")
    a = R.choice([30, 40, 50, 70, 80, 100, 120])
    return mcq("En un triángulo isósceles, el ángulo desigual mide %d°. ¿Cuánto mide cada uno de los otros dos?" % a, "%d°" % ((180 - a) // 2), ["%d°" % (180 - a), "%d°" % a, "%d°" % ((360 - a) // 2)],
               "(180° − %d°) : 2 = <b>%d°</b>." % (a, (180 - a) // 2))


def shape(k, rot=0):
    if k == "cuadrado":
        s = R.choice([90, 100, 110])
        pts, rights, ticks = [(0, 0), (s, 0), (s, -s), (0, -s)], (0, 1, 2, 3), ((0, 1), (1, 1), (2, 1), (3, 1))
    elif k == "rectángulo":
        w, h = R.choice([(150, 80), (160, 70), (130, 90), (170, 60)])
        pts, rights, ticks = [(0, 0), (w, 0), (w, -h), (0, -h)], (0, 1, 2, 3), ((0, 1), (2, 1), (1, 2), (3, 2))
    elif k == "rombo":
        a, b = R.choice([(70, 45), (55, 75), (80, 40)])
        pts, rights, ticks = [(0, 0), (a, -b), (0, -2 * b), (-a, -b)], (), ((0, 1), (1, 1), (2, 1), (3, 1))
    elif k == "romboide":
        w, h, d = R.choice([(130, 70, 45), (140, 60, 55), (120, 80, 40)])
        pts, rights, ticks = [(0, 0), (w, 0), (w + d, -h), (d, -h)], (), ((0, 1), (2, 1), (1, 2), (3, 2))
    elif k == "trapecio isósceles":
        w, h, d = R.choice([(170, 70, 40), (160, 80, 35), (180, 65, 50)])
        pts, rights, ticks = [(0, 0), (w, 0), (w - d, -h), (d, -h)], (), ((1, 1), (3, 1))
    elif k == "trapecio rectángulo":
        w, h, d = R.choice([(160, 80, 60), (170, 70, 50), (150, 90, 55)])
        pts, rights, ticks = [(0, 0), (w, 0), (w - d, -h), (0, -h)], (0, 3), ()
    else:
        pts = R.choice([[(0, 0), (150, 10), (120, -80), (30, -60)], [(0, 0), (170, 0), (110, -90), (-10, -50)], [(0, 0), (140, 20), (160, -70), (40, -90)]])
        rights, ticks = (), ()
    if rot:
        pts = AU.rot_all(pts, rot)
    return fig(relabel(AU.shape_svg(pts, {}, "un cuadrilátero", rights=rights, ticks=ticks), "un cuadrilátero"))


def s3_cuad():
    k = R.choice(CUAD)
    rot = R.choice([0, 0, 0, 20, -20]) if k != "cuadrado" else R.choice([0, 0, 45])
    near = {"cuadrado": ["rombo", "rectángulo"], "rectángulo": ["cuadrado", "romboide"], "rombo": ["cuadrado", "romboide"], "romboide": ["rombo", "rectángulo"],
            "trapecio isósceles": ["trapezoide", "romboide"], "trapecio rectángulo": ["rectángulo", "trapezoide"], "trapezoide": ["trapecio isósceles", "romboide"]}[k]
    why = {"cuadrado": "4 lados iguales y 4 ángulos rectos", "rectángulo": "4 ángulos rectos y los lados opuestos iguales", "rombo": "4 lados iguales y ningún ángulo recto",
           "romboide": "lados paralelos dos a dos, lados opuestos iguales y ningún ángulo recto", "trapecio isósceles": "solo dos lados paralelos y los otros dos iguales",
           "trapecio rectángulo": "solo dos lados paralelos y dos ángulos rectos", "trapezoide": "ningún lado paralelo a otro"}[k]
    w = [x for x in CUAD if x != k]
    R.shuffle(w)
    return mcq(shape(k, rot) + "¿Cómo se llama este cuadrilátero? (las rayitas indican lados iguales)", k, near + w, "Tiene %s: es un <b>%s</b>." % (why, k))


s4_prop = bank(R, [
    ("¿Qué cuadrilátero tiene 4 lados iguales pero ningún ángulo recto?", "el rombo", ["el cuadrado", "el rectángulo", "el trapecio"]),
    ("¿Qué cuadrilátero tiene 4 ángulos rectos y los lados no todos iguales?", "el rectángulo", ["el cuadrado", "el rombo", "el trapecio rectángulo"]),
    ("¿Qué cuadrilátero tiene 4 lados iguales y 4 ángulos rectos?", "el cuadrado", ["el rombo", "el rectángulo", "el romboide"]),
    ("¿Cuántos pares de lados paralelos tiene un paralelogramo?", "2", ["1", "0", "4"]),
    ("¿Cuántos pares de lados paralelos tiene un trapecio?", "1", ["2", "0", "4"]),
    ("¿Cuántos lados paralelos tiene un trapezoide?", "ninguno", ["2", "4", "1 par"]),
    ("¿Cuántas diagonales tiene un cuadrilátero?", "2", ["4", "1", "3"]),
    ("¿El cuadrado es también un rectángulo?", "sí, tiene 4 ángulos rectos", ["no, tiene los lados iguales", "solo si es grande", "no, nunca"]),
    ("¿El cuadrado es también un rombo?", "sí, tiene 4 lados iguales", ["no, tiene ángulos rectos", "solo si está girado", "no, nunca"]),
    ("¿Cuánto suman los ángulos de un cuadrilátero?", "360°", ["180°", "90°", "400°"]),
    ("¿Cuánto suman los ángulos de un triángulo?", "180°", ["360°", "90°", "100°"]),
    ("¿Cuántos ángulos rectos puede tener como máximo un triángulo?", "1", ["2", "3", "0"]),
    ("¿Qué paralelogramos tienen 4 ángulos rectos?", "el cuadrado y el rectángulo", ["el rombo y el romboide", "solo el cuadrado", "todos"]),
], "prop")


def s4_poligonos():
    k = R.choice(["nombre", "nombre", "diag", "regular"])
    names = {3: "triángulo", 4: "cuadrilátero", 5: "pentágono", 6: "hexágono", 7: "heptágono", 8: "octógono", 9: "eneágono", 10: "decágono"}
    if k == "nombre":
        n = R.randint(3, 10)
        if R.random() < 0.5:
            return mcq("¿Cómo se llama un polígono de %d lados?" % n, names[n], [names[x] for x in names if x != n and abs(x - n) <= 3], "%d lados: <b>%s</b>." % (n, names[n]))
        return mcq("¿Cuántos vértices tiene un %s?" % names[n], str(n), [str(n + 1), str(n - 1), str(n * 2)], "Un polígono tiene tantos vértices como lados: <b>%d</b>." % n)
    if k == "diag":
        n = R.choice([4, 5, 6])
        d = n * (n - 3) // 2
        return mcq("¿Cuántas diagonales tiene un %s?" % names[n], str(d), [str(n), str(d + 1), str(n - 3)], "Desde cada vértice salen %d diagonales: %d %s %d : 2 = <b>%d</b>." % (n - 3, n, "×", n - 3, d))
    return bank(R, [
        ("Un polígono regular tiene…", "todos los lados y todos los ángulos iguales", ["al menos un ángulo recto", "solo los lados iguales", "un número par de lados"]),
        ("¿Cuál de estos polígonos es siempre regular?", "el triángulo equilátero", ["el rectángulo", "el rombo", "el trapecio"]),
        ("¿Cómo se llama una señal de STOP según sus lados?", "octógono", ["hexágono", "pentágono", "decágono"]),
        ("¿Cuántos lados tienen las celdas de un panal de abejas?", "6", ["5", "4", "8"]),
    ], "reg")()


s5_circ = bank(R, [
    ("¿Cómo se llama la línea curva y cerrada cuyos puntos están todos a la misma distancia del centro?", "circunferencia", ["círculo", "radio", "diámetro"]),
    ("¿Cómo se llama la figura formada por la circunferencia y su interior?", "círculo", ["circunferencia", "cuerda", "arco"]),
    ("El segmento que une el centro con un punto de la circunferencia es…", "el radio", ["el diámetro", "la cuerda", "el arco"]),
    ("El segmento que une dos puntos de la circunferencia pasando por el centro es…", "el diámetro", ["el radio", "el arco", "el centro"]),
    ("Si el radio mide 5 cm, ¿cuánto mide el diámetro?", "10 cm", ["5 cm", "2,5 cm", "15 cm"]),
    ("Si el diámetro mide 12 cm, ¿cuánto mide el radio?", "6 cm", ["12 cm", "24 cm", "3 cm"]),
    ("Si el radio mide 8 cm, ¿cuánto mide el diámetro?", "16 cm", ["8 cm", "4 cm", "24 cm"]),
    ("Si el diámetro mide 30 cm, ¿cuánto mide el radio?", "15 cm", ["30 cm", "60 cm", "10 cm"]),
    ("¿Con qué instrumento se dibuja una circunferencia?", "con el compás", ["con el transportador", "con la escuadra", "con la regla"]),
    ("¿Cuántos radios tiene un diámetro?", "2", ["1", "3", "4"]),
    ("La rueda de una bicicleta tiene 35 cm de radio. ¿Cuánto mide su diámetro?", "70 cm", ["35 cm", "17,5 cm", "105 cm"]),
], "circ")


def main():
    seen = set()
    sets = [
        ("Triángulos según sus lados", mix(R, seen, [(s1_lados, 20)])),
        ("Triángulos según sus ángulos", mix(R, seen, [(s1_angulos, 12), (s2_suma, 8)])),
        ("Cuadriláteros", mix(R, seen, [(s3_cuad, 20)])),
        ("Propiedades y polígonos", mix(R, seen, [(s4_prop, 10), (s4_poligonos, 10)])),
        ("Ángulos de los triángulos y circunferencia", mix(R, seen, [(s2_suma, 10), (s5_circ, 10)])),
    ]
    body = lesson(
        ["Un <b>polígono</b> es una figura plana cerrada con lados rectos. Según el número de lados: triángulo (3), cuadrilátero (4), pentágono (5), hexágono (6)…",
         "Triángulos según sus lados: <b>equilátero</b> (3 iguales), <b>isósceles</b> (2 iguales), <b>escaleno</b> (ninguno igual). Según sus ángulos: <b>acutángulo</b>, <b>rectángulo</b> (un ángulo recto) y <b>obtusángulo</b> (un ángulo obtuso). Sus ángulos suman <b>180°</b>.",
         "Cuadriláteros: <b>paralelogramos</b> (lados paralelos dos a dos: cuadrado, rectángulo, rombo y romboide), <b>trapecios</b> (solo dos lados paralelos) y <b>trapezoides</b> (ninguno). Sus ángulos suman 360°.",
         "La <b>circunferencia</b> es la línea; el <b>círculo</b> es la línea y su interior. El diámetro mide el doble que el radio."],
        [("Dos ángulos de un triángulo miden 50° y 70°", ["180° − 50° − 70°"], "60°"),
         ("Un cuadrilátero con 4 lados iguales y sin ángulos rectos", ["Paralelogramo con lados iguales"], "rombo")],
        [["Pensar que el cuadrado no es un rectángulo", "El cuadrado tiene 4 ángulos rectos: también es un rectángulo (y un rombo)."],
         ["Llamar rombo a un cuadrado girado", "Si tiene ángulos rectos, es un cuadrado aunque esté girado."],
         ["Confundir circunferencia y círculo", "La circunferencia es el borde; el círculo incluye el interior."]],
        shape("rombo"))
    faq = [("¿Cómo se clasifican los triángulos?", "Por sus lados, en equiláteros, isósceles y escalenos; por sus ángulos, en acutángulos, rectángulos y obtusángulos."),
           ("¿Qué diferencia hay entre un rombo y un romboide?", "Los dos son paralelogramos sin ángulos rectos, pero el rombo tiene los cuatro lados iguales y el romboide solo los lados opuestos.")]
    make_unit(R, "triangulos-y-cuadrilateros", "E",
              "Figuras planas: polígonos y sus elementos; clasificación de triángulos según sus lados y sus ángulos; clasificación de cuadriláteros; la circunferencia y el círculo",
              "Triángulos, cuadriláteros y polígonos", "Triángulos y cuadriláteros",
              "Fichas de matemáticas de 4.º de Primaria: polígonos, triángulos equiláteros, isósceles y escalenos, acutángulos, rectángulos y obtusángulos, cuadriláteros, circunferencia y círculo. 100 ejercicios con soluciones.",
              "Los ángulos de un triángulo suman 180°", "Paralelogramos, trapecios y trapezoides: mira los lados paralelos.",
              body, faq, sets, 19)


if __name__ == "__main__":
    main()
