# -*- coding: utf-8 -*-
"""México 4.º grado: Cuadriláteros: clasificación por lados, ángulos y diagonales (Figuras geométricas y sus características). Reutiliza España 4.º/5.º con otra semilla y añade preguntas de diagonales y lados."""
import random
from mx_common import src, unit, mcq, num
import gen_es_matematicas_4_triangulos_y_cuadrilateros as T4

cuad, prop, pol = src("gen_es_matematicas_4_triangulos_y_cuadrilateros", 64219, "s3_cuad", "s4_prop", "s4_poligonos")
cuad5 = src("gen_es_matematicas_6_poligonos_y_circulo", 64319, "s3_cuadrilateros", lv=5)
R = random.Random(64119)

PERP = ["cuadrado", "rombo"]
IGUALES = ["cuadrado", "rectángulo"]


def diag():
    k = R.choice(["otra", "otra", "mitad", "corte", "cuantas", "perp"])
    if k == "otra":
        f = R.choice(IGUALES)
        d = R.randint(5, 40)
        return mcq("Una diagonal de un %s mide %d cm. ¿Cuánto mide la otra diagonal?" % (f, d), "%d cm" % d, ["%d cm" % (d // 2), "%d cm" % (2 * d), "%d cm" % (d + 4)],
                   "En el cuadrado y en el rectángulo las dos diagonales miden lo mismo: <b>%d cm</b>." % d)
    if k == "mitad":
        f = R.choice(["cuadrado", "rectángulo", "rombo", "romboide"])
        d = 2 * R.randint(3, 25)
        return mcq("En un %s, las diagonales se cortan en su punto medio. Si una diagonal mide %d cm, ¿cuánto mide cada mitad de esa diagonal?" % (f, d), "%d cm" % (d // 2),
                   ["%d cm" % d, "%d cm" % (2 * d), "%d cm" % (d // 2 + 2)], "En los paralelogramos, las diagonales se cortan por la mitad: %d ÷ 2 = <b>%d cm</b>." % (d, d // 2))
    if k == "corte":
        f = R.choice(PERP)
        return mcq("¿Qué ángulo forman las diagonales de un %s al cortarse?" % f, "un ángulo recto (90°)", ["un ángulo agudo", "un ángulo obtuso", "no se cortan"],
                   "En el cuadrado y en el rombo las diagonales son <b>perpendiculares</b>: forman ángulos rectos.")
    if k == "cuantas":
        f = R.choice(["un cuadrado", "un trapecio", "un rombo", "un romboide", "un rectángulo", "un trapezoide"])
        return mcq("¿Cuántas diagonales tiene %s?" % f, "2", ["1", "4", "3"], "Una diagonal une dos vértices que no están juntos. Todo cuadrilátero tiene <b>2</b> diagonales.")
    q = R.choice([("¿En qué cuadrilátero las diagonales son iguales y perpendiculares?", "en el cuadrado", ["en el rectángulo", "en el rombo", "en el romboide"]),
                  ("¿En qué cuadrilátero las diagonales son perpendiculares pero de distinta longitud?", "en el rombo", ["en el cuadrado", "en el rectángulo", "en el romboide"]),
                  ("¿En qué cuadrilátero las diagonales son iguales pero no perpendiculares?", "en el rectángulo", ["en el cuadrado", "en el rombo", "en el romboide"]),
                  ("¿En qué paralelogramo las diagonales no son iguales ni perpendiculares?", "en el romboide", ["en el cuadrado", "en el rombo", "en el rectángulo"])])
    return mcq(q[0], q[1], q[2], "Cuadrado: iguales y perpendiculares. Rectángulo: iguales. Rombo: perpendiculares. Romboide: ni una cosa ni otra. Respuesta: <b>%s</b>." % q[1])


def lados():
    k = R.choice(["cuadrado", "rombo", "rect", "romboide", "falta", "falta_r"])
    a, b = R.sample(range(3, 40), 2)
    if k in ("cuadrado", "rombo"):
        return mcq("Un %s tiene un lado de %d cm. ¿Cuál es su perímetro?" % (k, a), "%d cm" % (4 * a), ["%d cm" % (2 * a), "%d cm" % (a + 4), "%d cm" % (a * a)],
                   "El %s tiene 4 lados iguales: 4 × %d = <b>%d cm</b>." % (k, a, 4 * a))
    if k in ("rect", "romboide"):
        f = "rectángulo" if k == "rect" else "romboide"
        return mcq("Un %s tiene lados de %d cm y %d cm. ¿Cuál es su perímetro?" % (f, a, b), "%d cm" % (2 * (a + b)), ["%d cm" % (a + b), "%d cm" % (a * b), "%d cm" % (4 * a + b)],
                   "Los lados opuestos son iguales: %d + %d + %d + %d = <b>%d cm</b>." % (a, b, a, b, 2 * (a + b)))
    if k == "falta":
        return mcq("El perímetro de un rombo es %d cm. ¿Cuánto mide cada lado?" % (4 * a), "%d cm" % a, ["%d cm" % (2 * a), "%d cm" % (4 * a), "%d cm" % (a + 4)],
                   "Los 4 lados son iguales: %d ÷ 4 = <b>%d cm</b>." % (4 * a, a))
    p = 2 * (a + b)
    return mcq("Un rectángulo mide %d cm de largo y su perímetro es %d cm. ¿Cuánto mide de ancho?" % (a, p), "%d cm" % b, ["%d cm" % (p - a), "%d cm" % (p - 2 * a), "%d cm" % (p // 2)],
               "%d − %d − %d = %d; %d ÷ 2 = <b>%d cm</b>." % (p, a, a, p - 2 * a, p - 2 * a, b))


unit("cuadrilateros", 17, "F",
     "Clasifica cuadriláteros (cuadrado, rectángulo, rombo, romboide, trapecio y trapezoide) por el paralelismo y la longitud de sus lados, sus ángulos y sus diagonales; calcula perímetros con sus propiedades",
     "Cuadriláteros: lados, ángulos y diagonales", "Cuadriláteros",
     "Ejercicios de matemáticas de 4.º grado de primaria: cuadrado, rectángulo, rombo, romboide, trapecio y trapezoide; lados paralelos, ángulos, diagonales y perímetro. 100 ejercicios con respuestas.",
     "Mira los lados paralelos", "Luego los ángulos y las diagonales.",
     ["Un <b>cuadrilátero</b> tiene 4 lados. Si tiene dos pares de lados paralelos es un <b>paralelogramo</b>: cuadrado, rectángulo, rombo o romboide.",
      "Con un solo par de lados paralelos es un <b>trapecio</b>; sin lados paralelos, un <b>trapezoide</b>.",
      "Cuadrado: 4 lados iguales y 4 ángulos rectos. Rectángulo: 4 ángulos rectos. Rombo: 4 lados iguales. Romboide: lados opuestos iguales, sin ángulos rectos.",
      "Las <b>diagonales</b> unen vértices opuestos. En el cuadrado y el rombo son perpendiculares; en el cuadrado y el rectángulo, iguales."],
     [("4 lados iguales, sin ángulos rectos", ["dos pares de lados paralelos", "lados iguales: rombo o cuadrado", "sin ángulos rectos"], "rombo"),
      ("Perímetro de un romboide de 9 cm y 5 cm", ["9 + 5 + 9 + 5"], "28 cm")],
     [["Pensar que el cuadrado no es un rectángulo", "Tiene 4 ángulos rectos: también es rectángulo."], ["Confundir trapecio y trapezoide", "El trapecio tiene un par de lados paralelos; el trapezoide, ninguno."],
      ["Creer que todas las diagonales son iguales", "En el rombo y en el romboide son distintas."]],
     [("¿Qué diferencia hay entre un rombo y un romboide?", "Los dos tienen lados opuestos paralelos y ningún ángulo recto, pero el rombo tiene los 4 lados iguales y el romboide solo los lados opuestos."),
      ("¿Qué es una diagonal?", "Un segmento que une dos vértices que no están uno al lado del otro. Todo cuadrilátero tiene dos diagonales.")],
     [("¿Qué cuadrilátero es?", [(cuad, 20)]), ("Lados paralelos y ángulos", [(prop, 10), (cuad5, 10)]), ("Diagonales", [(diag, 20)]), ("Perímetro de cuadriláteros", [(lados, 20)]), ("Polígonos", [(pol, 20)])],
     64017, pic=T4.shape("romboide") if hasattr(T4, "shape") else "", lv=4)
