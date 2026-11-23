# -*- coding: utf-8 -*-
"""
España Matemáticas 1.º de ESO: Polígonos, perímetros y áreas (Sentido de la medida)
Clasificar polígonos, triángulos y cuadriláteros; áreas de triángulos, paralelogramos, rombos, trapecios y polígonos regulares; figuras compuestas; problemas.
Reutiliza problemas de 6.º de Primaria (polígonos y áreas) con otra semilla y añade el cálculo inverso (del área al lado).
Errores: olvidar dividir entre 2 en el triángulo, usar el lado inclinado como altura, confundir perímetro y área.
"""
import random
from fractions import Fraction as F
from es_eso import M, mix, d, num, unit, L, Kids, use_

R = random.Random(47011)
K = Kids(R)
pol, tris, cuads = use_("gen_es_matematicas_6_poligonos_y_circulo", 47911, "s1_poligonos", "s2_triangulos", "s3_cuadrilateros")
tp, otros, comp, prob = use_("gen_es_matematicas_6_area_de_figuras_planas", 47912, "s2_tri_para", "s3_otros", "s4_compuesta", "s5_problema")
import gen_es_matematicas_6_area_de_figuras_planas as A6


def s_inversa():
    t = R.choice(["cuad", "rect", "tri", "per"])
    if t == "cuad":
        l = R.randint(3, 25)
        return M("Un cuadrado tiene %s cm² de área. ¿Cuánto mide su lado?" % num(l * l), "%d cm" % l, ["%s cm" % d(F(l * l, 4)), "%s cm" % d(F(l * l, 2)), "%d cm" % (l + 1)], "√%s = <b>%d cm</b>." % (num(l * l), l))
    if t == "rect":
        a, b = R.randint(3, 20), R.randint(2, 15)
        if a == b:
            return None
        return M("Un rectángulo tiene %s cm² de área y %d cm de base. ¿Cuánto mide su altura?" % (num(a * b), a), "%d cm" % b, ["%d cm" % (a * b - a), "%s cm" % d(F(a * b, 2 * a)), "%d cm" % (b + 2)], "altura = área : base = %s : %d = <b>%d cm</b>." % (num(a * b), a, b))
    if t == "tri":
        a, h = R.randint(4, 20), R.randint(2, 15)
        A = F(a * h, 2)
        return M("Un triángulo tiene %s cm² de área y %d cm de base. ¿Cuánto mide su altura?" % (d(A), a), "%d cm" % h, ["%s cm" % d(A / a), "%s cm" % d(A * 2), "%d cm" % (h + 2)], "altura = 2 · área : base = %s : %d = <b>%d cm</b>." % (d(2 * A), a, h))
    l = R.randint(3, 20)
    return M("Un cuadrado tiene %d cm de perímetro. ¿Cuál es su área?" % (4 * l), "%s cm²" % num(l * l), ["%s cm²" % num(16 * l * l), "%d cm²" % (4 * l), "%d cm²" % (2 * l)], "lado = %d : 4 = %d cm; área = %d² = <b>%s cm²</b>." % (4 * l, l, l, num(l * l)))


seen = set()
sets = [("Polígonos, triángulos y cuadriláteros", mix(R, seen, [(pol, 8), (tris, 6), (cuads, 6)])), ("Triángulos y paralelogramos", mix(R, seen, [(tp, 20)])),
        ("Rombo, trapecio y polígonos regulares", mix(R, seen, [(otros, 20)])), ("Figuras compuestas", mix(R, seen, [(comp, 12), (s_inversa, 8)])), ("Problemas", mix(R, seen, [(prob, 14), (s_inversa, 6)]))]
body = L(["Rectángulo y romboide: base · altura. Triángulo: base · altura : 2. Rombo: D · d : 2. Trapecio: (B + b) · h : 2.",
          "Polígono regular: perímetro · apotema : 2.", "La <b>altura</b> siempre es perpendicular a la base, no el lado inclinado.",
          "Para una figura compuesta, divídela en figuras conocidas y suma (o resta) sus áreas."],
         [("Trapecio con B = 10 cm, b = 6 cm y h = 4 cm", ["(10 + 6) · 4 : 2"], "32 cm²"), ("Hexágono regular de lado 6 cm y apotema 5,2 cm", ["perímetro 36 cm", "36 · 5,2 : 2"], "93,6 cm²")],
         [["Olvidar dividir entre 2 en el triángulo", "Un triángulo es medio rectángulo."], ["Usar el lado inclinado como altura", "La altura es la línea perpendicular."], ["Confundir perímetro y área", "Perímetro en cm; área en cm²."]],
         A6.figura("trap", 10, 6, 4))
faq = [("¿Cómo se calcula el área de un polígono regular?", "Multiplicando el perímetro por la apotema y dividiendo entre 2."), ("¿Qué es la apotema?", "El segmento que va del centro de un polígono regular al punto medio de un lado, perpendicular a él.")]
unit(1, R, "poligonos-y-areas", "M", "Polígonos: clasificación de triángulos y cuadriláteros; perímetros y áreas de figuras planas y polígonos regulares; figuras compuestas",
     "Polígonos, perímetros y áreas", "Polígonos y áreas",
     "Fichas de matemáticas de 1.º de ESO: triángulos y cuadriláteros, áreas de paralelogramos, rombos, trapecios, polígonos regulares y figuras compuestas. 100 ejercicios con soluciones.",
     "Triángulo: base · altura : 2", "Polígono regular: perímetro · apotema : 2.", body, faq, sets, 11)
