# -*- coding: utf-8 -*-
"""México 5.º grado: Polígonos, triángulos y cuadriláteros; el círculo y la circunferencia: centro, radio y diámetro (Figuras geométricas y sus características). Reutiliza España 6.º (nivel 5.º) y 4.º con otra semilla."""
from mx_common import src, unit

pol, tri, cuad, circ = src("gen_es_matematicas_6_poligonos_y_circulo", 65316, "s1_poligonos", "s2_triangulos", "s3_cuadrilateros", "s4_circulo", lv=5)
lados, angs, cuad4 = src("gen_es_matematicas_4_triangulos_y_cuadrilateros", 65216, "s1_lados", "s1_angulos", "s3_cuad")

unit("poligonos-y-circulo", 14, "F",
     "Clasifica polígonos por el número de lados, triángulos por sus lados y ángulos, y cuadriláteros por sus lados paralelos; identifica el centro, el radio y el diámetro de una circunferencia y su relación",
     "Polígonos, triángulos y círculo", "Polígonos y círculo",
     "Ejercicios de matemáticas de 5.º grado de primaria: polígonos, triángulos por lados y ángulos, cuadriláteros, circunferencia y círculo, radio y diámetro. 100 ejercicios con respuestas.",
     "Diámetro = 2 × radio", "Polígono: figura cerrada de lados rectos.",
     ["Un <b>polígono</b> es una figura cerrada de lados rectos: triángulo (3), cuadrilátero (4), pentágono (5), hexágono (6), heptágono (7), octágono (8).",
      "Por sus lados, un triángulo es <b>equilátero</b> (3 iguales), <b>isósceles</b> (2 iguales) o <b>escaleno</b> (ninguno igual). Por sus ángulos es acutángulo, rectángulo u obtusángulo.",
      "La <b>circunferencia</b> es la línea curva; el <b>círculo</b>, la superficie de adentro. El <b>radio</b> va del centro a la circunferencia; el <b>diámetro</b> la cruza pasando por el centro y mide el doble del radio."],
     [("Radio de 7 cm", ["diámetro = 2 × 7"], "14 cm"), ("Triángulo con lados 5, 5 y 8 cm", ["dos lados iguales"], "isósceles")],
     [["Confundir circunferencia y círculo", "La circunferencia es el borde."], ["Confundir radio y diámetro", "El diámetro es el doble del radio."], ["Pensar que un triángulo rectángulo tiene lados iguales", "Rectángulo se refiere al ángulo de 90°."]],
     [("¿Qué diferencia hay entre circunferencia y círculo?", "La circunferencia es la línea curva cerrada; el círculo es la superficie que queda dentro de ella."),
      ("¿Cuánto mide el diámetro si el radio mide 9 cm?", "18 cm, porque el diámetro mide el doble del radio.")],
     [("Polígonos", [(pol, 20)]), ("Triángulos por sus lados", [(lados, 14), (tri, 6)]), ("Triángulos por sus ángulos", [(angs, 20)]), ("Cuadriláteros", [(cuad4, 12), (cuad, 8)]),
      ("Circunferencia y círculo", [(circ, 20)])],
     65014, lv=5)
