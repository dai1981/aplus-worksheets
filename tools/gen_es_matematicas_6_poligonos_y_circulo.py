# -*- coding: utf-8 -*-
"""
España Matemáticas 6.º (y 5.º) de Primaria: Polígonos y círculo (Sentido espacial)
Polígonos: elementos, regulares e irregulares, diagonales, clasificar triángulos y cuadriláteros (paralelogramos, trapecios, trapezoides);
la circunferencia y el círculo: centro, radio, diámetro, cuerda, arco; sector y segmento circular; posiciones de rectas y circunferencias.
Errores: pensar que el cuadrado no es un rombo, confundir cuerda y diámetro, confundir sector y segmento circular.
"""
import random
from es_c3 import M, mix, lesson, make_unit
from es_common import use

R = None
LV = 6
NAMES = {3: "triángulo", 4: "cuadrilátero", 5: "pentágono", 6: "hexágono", 7: "heptágono", 8: "octógono", 9: "eneágono", 10: "decágono", 12: "dodecágono"}


def s1_poligonos():
    k = R.choice(["nombre", "diag", "regular", "angulo_reg"] if LV == 6 else ["nombre", "diag", "regular"])
    n = R.choice(list(NAMES))
    if k == "nombre":
        if R.random() < 0.5:
            return M("¿Cómo se llama un polígono de %d lados?" % n, NAMES[n], [NAMES[x] for x in NAMES if x != n and abs(x - n) <= 3], "%d lados: <b>%s</b>." % (n, NAMES[n]))
        return M("¿Cuántos lados tiene un %s?" % NAMES[n], str(n), [str(n + 1), str(n - 1), str(n * 2)], "Un %s tiene <b>%d</b> lados." % (NAMES[n], n))
    if k == "diag":
        n = R.choice([4, 5, 6, 7, 8])
        dd = n * (n - 3) // 2
        return M("¿Cuántas diagonales tiene un %s?" % NAMES[n], str(dd), [str(n), str(n - 3), str(n * (n - 3)), str(dd + 1)], "Desde cada vértice salen %d: %d × %d : 2 = <b>%d</b>." % (n - 3, n, n - 3, dd))
    if k == "angulo_reg":
        n = R.choice([3, 4, 5, 6, 8, 9, 10, 12])
        c = 360 // n if 360 % n == 0 else None
        return M("¿Cuánto mide el ángulo central de un %s regular?" % NAMES[n], "%d°" % c, ["%d°" % (180 // n) if 180 % n == 0 else "%d°" % (c + 10), "%d°" % (180 - c), "%d°" % (c * 2)], "360° : %d = <b>%d°</b>." % (n, c)) if c else None
    q, a, w = R.choice([("Un polígono regular tiene…", "todos los lados y los ángulos iguales", ["solo los lados iguales", "algún ángulo recto", "un número par de lados"]),
                        ("¿Cuál de estos polígonos es siempre regular?", "el triángulo equilátero", ["el rombo", "el rectángulo", "el trapecio"]),
                        ("¿Es regular un rombo que no es cuadrado?", "no, sus ángulos no son iguales", ["sí, tiene los lados iguales", "sí, siempre", "solo si es grande"]),
                        ("¿Es regular un rectángulo que no es cuadrado?", "no, sus lados no son iguales", ["sí, tiene los ángulos iguales", "sí, siempre", "solo si está girado"]),
                        ("El segmento que une dos vértices no consecutivos de un polígono es…", "una diagonal", ["un lado", "una apotema", "un radio"]),
                        ("El segmento que une el centro de un polígono regular con el punto medio de un lado es…", "la apotema", ["el radio", "la diagonal", "el diámetro"])])
    return M(q, a, w, "Respuesta: <b>%s</b>." % a)


def s2_triangulos():
    q, a, w = R.choice([("Un triángulo con tres lados iguales es…", "equilátero", ["isósceles", "escaleno", "rectángulo"]),
                        ("Un triángulo con dos lados iguales es…", "isósceles", ["equilátero", "escaleno", "obtusángulo"]),
                        ("Un triángulo con los tres lados distintos es…", "escaleno", ["isósceles", "equilátero", "acutángulo"]),
                        ("Un triángulo con un ángulo recto es…", "rectángulo", ["acutángulo", "obtusángulo", "equilátero"]),
                        ("Un triángulo con un ángulo de 120° es…", "obtusángulo", ["acutángulo", "rectángulo", "equilátero"]),
                        ("Un triángulo con ángulos de 60°, 70° y 50° es…", "acutángulo", ["rectángulo", "obtusángulo", "llano"]),
                        ("¿Puede un triángulo tener dos ángulos rectos?", "no, sumarían ya 180°", ["sí, si es grande", "sí, si es isósceles", "solo si es equilátero"]),
                        ("¿Puede existir un triángulo con lados de 2 cm, 3 cm y 8 cm?", "no, 2 + 3 es menor que 8", ["sí, siempre", "sí, si es escaleno", "solo si es rectángulo"]),
                        ("¿Puede un triángulo ser rectángulo e isósceles a la vez?", "sí, con ángulos de 90°, 45° y 45°", ["no, nunca", "solo si es equilátero", "solo si es obtusángulo"]),
                        ("¿Cómo se llaman los lados que forman el ángulo recto de un triángulo rectángulo?", "catetos", ["hipotenusas", "diagonales", "bases"]),
                        ("¿Cómo se llama el lado opuesto al ángulo recto?", "hipotenusa", ["cateto", "altura", "diagonal"]),
                        ("¿Cuánto mide cada ángulo de un triángulo equilátero?", "60°", ["90°", "45°", "180°"])])
    return M(q, a, w, "Respuesta: <b>%s</b>." % a)


def s3_cuadrilateros():
    q, a, w = R.choice([("¿Qué paralelogramo tiene 4 lados iguales y 4 ángulos rectos?", "el cuadrado", ["el rombo", "el rectángulo", "el romboide"]),
                        ("¿Qué paralelogramo tiene 4 lados iguales y ningún ángulo recto?", "el rombo", ["el cuadrado", "el rectángulo", "el romboide"]),
                        ("¿Qué paralelogramo tiene ángulos rectos y lados contiguos distintos?", "el rectángulo", ["el cuadrado", "el rombo", "el trapecio"]),
                        ("¿Qué paralelogramo no tiene ni ángulos rectos ni todos los lados iguales?", "el romboide", ["el rombo", "el rectángulo", "el trapezoide"]),
                        ("Un cuadrilátero con solo dos lados paralelos es…", "un trapecio", ["un paralelogramo", "un trapezoide", "un rombo"]),
                        ("Un cuadrilátero sin lados paralelos es…", "un trapezoide", ["un trapecio", "un romboide", "un rectángulo"]),
                        ("¿Es el cuadrado un rombo?", "sí, tiene los 4 lados iguales", ["no, tiene ángulos rectos", "solo si está girado", "no, nunca"]),
                        ("¿Es el cuadrado un rectángulo?", "sí, tiene 4 ángulos rectos", ["no, tiene los lados iguales", "solo si es grande", "no, nunca"]),
                        ("¿En qué paralelogramos las diagonales son perpendiculares?", "en el cuadrado y en el rombo", ["en el rectángulo y en el romboide", "solo en el rectángulo", "en todos"]),
                        ("¿En qué paralelogramos las diagonales son iguales?", "en el cuadrado y en el rectángulo", ["en el rombo y en el romboide", "solo en el rombo", "en ninguno"]),
                        ("Un trapecio con dos ángulos rectos es un…", "trapecio rectángulo", ["trapecio isósceles", "trapecio escaleno", "rectángulo"]),
                        ("Un trapecio con los dos lados no paralelos iguales es un…", "trapecio isósceles", ["trapecio rectángulo", "trapecio escaleno", "rombo"])])
    return M(q, a, w, "Respuesta: <b>%s</b>." % a)


def s4_circulo():
    k = R.choice(["rd", "rd", "elem", "elem", "pos"])
    if k == "rd":
        r = R.randint(2, 40)
        if R.random() < 0.5:
            return M("El radio de una circunferencia mide %d cm. ¿Cuánto mide el diámetro?" % r, "%d cm" % (2 * r), ["%d cm" % r, "%d cm" % (r // 2) if r % 2 == 0 else "%d cm" % (r + 2), "%d cm" % (3 * r)], "Diámetro = 2 × radio = <b>%d cm</b>." % (2 * r))
        return M("El diámetro de una circunferencia mide %d cm. ¿Cuánto mide el radio?" % (2 * r), "%d cm" % r, ["%d cm" % (2 * r), "%d cm" % (4 * r), "%d cm" % (r + 2)], "Radio = diámetro : 2 = <b>%d cm</b>." % r)
    if k == "elem":
        q, a, w = R.choice([("El segmento que une el centro con un punto de la circunferencia es…", "el radio", ["el diámetro", "la cuerda", "el arco"]),
                            ("El segmento que une dos puntos de la circunferencia es…", "una cuerda", ["un radio", "un arco", "un sector"]),
                            ("La cuerda que pasa por el centro es…", "el diámetro", ["el radio", "el arco", "la tangente"]),
                            ("La parte de la circunferencia entre dos puntos es…", "un arco", ["una cuerda", "un sector", "un radio"]),
                            ("La parte del círculo entre dos radios y un arco es…", "un sector circular", ["un segmento circular", "una corona circular", "un semicírculo"]),
                            ("La parte del círculo entre una cuerda y su arco es…", "un segmento circular", ["un sector circular", "una corona circular", "un radio"]),
                            ("La figura entre dos circunferencias con el mismo centro es…", "una corona circular", ["un sector circular", "un semicírculo", "un segmento circular"]),
                            ("La mitad de un círculo, limitada por un diámetro, es…", "un semicírculo", ["un sector de 90°", "una corona", "un arco"]),
                            ("¿Qué diferencia hay entre circunferencia y círculo?", "la circunferencia es la línea; el círculo, la línea y su interior", ["son lo mismo", "el círculo es la línea; la circunferencia, el interior", "la circunferencia es más grande"])])
        return M(q, a, w, "Respuesta: <b>%s</b>." % a)
    q, a, w = R.choice([("Una recta que toca la circunferencia en un solo punto es…", "tangente", ["secante", "exterior", "diámetro"]),
                        ("Una recta que corta la circunferencia en dos puntos es…", "secante", ["tangente", "exterior", "radio"]),
                        ("Una recta que no toca la circunferencia es…", "exterior", ["tangente", "secante", "cuerda"]),
                        ("Dos circunferencias con el mismo centro y distinto radio son…", "concéntricas", ["tangentes", "secantes", "iguales"])])
    return M(q, a, w, "Respuesta: <b>%s</b>." % a)


def build(lv):
    global R, LV
    LV = lv
    R = random.Random(40016 + lv * 1000)
    cuad = use("gen_es_matematicas_4_triangulos_y_cuadrilateros", 40116 + lv * 1000, "s3_cuad")
    lados, angs = use("gen_es_matematicas_4_triangulos_y_cuadrilateros", 40116 + lv * 1000, "s1_lados", "s1_angulos")
    seen = set()
    sets = [
        ("Polígonos", mix(R, seen, [(s1_poligonos, 20)])),
        ("Triángulos", mix(R, seen, [(s2_triangulos, 10), (lados, 5), (angs, 5)])),
        ("Cuadriláteros", mix(R, seen, [(s3_cuadrilateros, 10), (cuad, 10)])),
        ("Circunferencia y círculo", mix(R, seen, [(s4_circulo, 20)])),
        ("Repaso", mix(R, seen, [(s1_poligonos, 8), (s4_circulo, 6), (lados, 3), (cuad, 3)])),
    ]
    body = lesson(
        ["Un <b>polígono</b> es una figura plana cerrada formada por segmentos (lados). Es <b>regular</b> si tiene todos los lados y todos los ángulos iguales.",
         "Triángulos: por sus lados, equilátero, isósceles y escaleno; por sus ángulos, acutángulo, rectángulo y obtusángulo. Cuadriláteros: <b>paralelogramos</b> (cuadrado, rectángulo, rombo, romboide), <b>trapecios</b> y <b>trapezoides</b>.",
         "La <b>circunferencia</b> es la línea cuyos puntos están a la misma distancia del centro (el radio). El <b>círculo</b> es la circunferencia y su interior. Diámetro = 2 × radio."],
        [("Diagonales de un hexágono", ["De cada vértice salen 3", "6 × 3 : 2"], "9"),
         ("Radio de 7 cm", ["Diámetro = 2 × 7"], "14 cm")],
        [["Pensar que el cuadrado no es un rombo", "Tiene 4 lados iguales: también es un rombo."],
         ["Confundir cuerda y diámetro", "El diámetro es la cuerda que pasa por el centro."],
         ["Confundir sector y segmento", "Sector: entre dos radios. Segmento: entre una cuerda y su arco."]])
    faq = [("¿Qué es un polígono regular?", "Un polígono con todos sus lados y todos sus ángulos iguales, como el triángulo equilátero, el cuadrado o el hexágono regular."),
           ("¿Cuál es la diferencia entre circunferencia y círculo?", "La circunferencia es solo la línea curva; el círculo es la superficie que encierra, incluida la circunferencia.")]
    make_unit(R, "poligonos-y-circulo", "E",
              "Figuras planas: polígonos y sus elementos, polígonos regulares, clasificación de triángulos y cuadriláteros; circunferencia y círculo: elementos, figuras circulares y posiciones relativas",
              "Polígonos, circunferencia y círculo", "Polígonos y círculo",
              "Fichas de matemáticas de %d.º de Primaria: polígonos regulares, diagonales, triángulos y cuadriláteros, circunferencia y círculo, radio, diámetro, cuerda, arco y sector. 100 ejercicios con soluciones." % lv,
              "Regular: lados y ángulos iguales", "Diámetro = 2 × radio.",
              body, faq, sets, 16, grade="%d-primaria" % lv)


if __name__ == "__main__":
    build(6)
