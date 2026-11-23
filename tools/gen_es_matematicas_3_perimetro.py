# -*- coding: utf-8 -*-
"""
España Matemáticas 3.º de Primaria: El perímetro (Sentido de la medida)
Perímetro en una cuadrícula, de polígonos, del cuadrado y del rectángulo, el lado que falta, problemas. Sin área (4.º).
Reutiliza los generadores de 4.º (mismo ciclo).
"""
from es_low import unit, src
import gen_es_matematicas_4_perimetro_y_area as A4

SEED = 33915
cua, per, falta, prob = src("perimetro_y_area", SEED, "s1_cuadritos", "s2_perimetro", "s4_falta", "s5_problema", sin=("área", "cuadrados de 1"))

unit(3, "perimetro", 15, "M", "Perímetro de figuras planas; medida y cálculo del contorno de polígonos, cuadrados y rectángulos",
     "El perímetro", "Perímetro",
     "Fichas de matemáticas de 3.º de Primaria: perímetro en la cuadrícula, de polígonos, del cuadrado y del rectángulo, y problemas. 100 ejercicios con soluciones.",
     "Perímetro: suma de todos los lados", "Es la medida del borde.",
     ["El <b>perímetro</b> es lo que mide el borde de una figura: se suman todos los lados.", "Cuadrado: 4 lados iguales, perímetro = 4 × lado.", "Rectángulo: largo + ancho + largo + ancho."],
     [("Rectángulo de 6 cm de largo y 4 cm de ancho", ["6 + 4 + 6 + 4"], "20 cm"), ("Cuadrado de 7 m de lado", ["4 × 7"], "28 m")],
     [["Sumar solo dos lados del rectángulo", "Tiene 4 lados: suma los 4."], ["Contar los cuadraditos de dentro", "El perímetro es el borde, no lo de dentro."], ["Olvidar la unidad", "Escribe cm, m…"]],
     [("¿Qué es el perímetro?", "Es la longitud del contorno de una figura. Se calcula sumando todos sus lados."), ("¿Cómo se calcula el perímetro de un cuadrado?", "Se multiplica el lado por 4.")],
     [("En la cuadrícula", [(cua, 20)]), ("Perímetro de polígonos", [(per, 20)]), ("Repaso del perímetro", [(per, 10), (cua, 10)]), ("El lado que falta", [(falta, 20)]), ("Problemas", [(prob, 20)])],
     33015, A4.cuadricula(A4.rect_cells(4, 3)))
