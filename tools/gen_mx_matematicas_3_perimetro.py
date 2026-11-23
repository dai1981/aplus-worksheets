# -*- coding: utf-8 -*-
"""México 3.er grado: Perímetro (contorno de figuras; Cálculo de perímetro y área). Reutiliza España 4.º con otra semilla, sin área."""
from mx_common import src, unit
import gen_es_matematicas_4_perimetro_y_area as A4

cua, per, falta, prob = src("gen_es_matematicas_4_perimetro_y_area", 63214, "s1_cuadritos", "s2_perimetro", "s4_falta", "s5_problema", sin_=("área", "cuadrados de 1"))

unit("perimetro", 14, "A",
     "Distingue el contorno y la superficie de una figura; mide y calcula el perímetro de polígonos, cuadrados y rectángulos con unidades convencionales",
     "El perímetro", "Perímetro",
     "Ejercicios de matemáticas de 3.er grado de primaria: perímetro en la cuadrícula, de polígonos, del cuadrado y del rectángulo, y problemas. 100 ejercicios con respuestas.",
     "Perímetro: suma de todos los lados", "Es la medida del contorno.",
     ["El <b>perímetro</b> es lo que mide el contorno de una figura: se suman todos los lados.", "Cuadrado: 4 lados iguales, perímetro = 4 × lado.", "Rectángulo: largo + ancho + largo + ancho."],
     [("Rectángulo de 6 cm de largo y 4 cm de ancho", ["6 + 4 + 6 + 4"], "20 cm"), ("Cuadrado de 7 m de lado", ["4 × 7"], "28 m")],
     [["Sumar solo dos lados del rectángulo", "Tiene 4 lados: suma los 4."], ["Contar los cuadritos de adentro", "El perímetro es el contorno, no la superficie."], ["Olvidar la unidad", "Escribe cm, m…"]],
     [("¿Qué es el perímetro?", "Es la longitud del contorno de una figura. Se calcula sumando todos sus lados."), ("¿Cómo se calcula el perímetro de un cuadrado?", "Se multiplica el lado por 4.")],
     [("En la cuadrícula", [(cua, 20)]), ("Perímetro de polígonos", [(per, 20)]), ("Repaso del perímetro", [(per, 10), (cua, 10)]), ("El lado que falta", [(falta, 20)]), ("Problemas", [(prob, 20)])],
     63014, pic=A4.cuadricula(A4.rect_cells(4, 3)))
