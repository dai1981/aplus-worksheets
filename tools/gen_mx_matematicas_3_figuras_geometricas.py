# -*- coding: utf-8 -*-
"""México 3.er grado: Figuras geométricas (polígonos, triángulos según sus lados, cuadriláteros, simetría). Reutiliza España 4.º con otra semilla."""
from mx_common import src, unit
import gen_es_matematicas_4_triangulos_y_cuadrilateros as T4

lados, cuad, prop, pol = src("gen_es_matematicas_4_triangulos_y_cuadrilateros", 63211, "s1_lados", "s3_cuad", "s4_prop", "s4_poligonos")
ejes, figura, sim = src("gen_es_matematicas_4_simetria_y_coordenadas", 63311, "s5_ejes", "s4_figura", "s3_simetrico")

unit("figuras-geometricas", 11, "F",
     "Construye, analiza y clasifica figuras geométricas a partir de retículas; clasifica triángulos según la medida de sus lados; identifica ejes de simetría",
     "Figuras geométricas", "Figuras geométricas",
     "Ejercicios de matemáticas de 3.er grado de primaria: polígonos, triángulos equiláteros, isósceles y escalenos, cuadriláteros y ejes de simetría. 100 ejercicios con respuestas.",
     "Cuenta lados iguales", "Equilátero: 3 iguales. Isósceles: 2. Escaleno: 0.",
     ["Un <b>polígono</b> es una figura plana cerrada con lados rectos. Se llama según sus lados: triángulo (3), cuadrilátero (4), pentágono (5), hexágono (6).",
      "Según sus lados, un triángulo es <b>equilátero</b> (3 lados iguales), <b>isósceles</b> (2 iguales) o <b>escaleno</b> (todos distintos).",
      "Una figura es <b>simétrica</b> si al doblarla por el <b>eje de simetría</b> las dos mitades coinciden."],
     [("Triángulo de lados 5 cm, 5 cm y 3 cm", ["dos lados iguales"], "isósceles"), ("Un cuadrado", ["se puede doblar de 4 formas"], "4 ejes de simetría")],
     [["Contar los vértices como lados", "Un triángulo tiene 3 lados y 3 vértices."], ["Pensar que el cuadrado no es rectángulo", "El cuadrado es un rectángulo con los 4 lados iguales."], ["Ver ejes donde no hay", "Las dos mitades deben coincidir al doblar."]],
     [("¿Qué diferencia hay entre un triángulo isósceles y uno equilátero?", "El isósceles tiene dos lados iguales; el equilátero, los tres."),
      ("¿Cuántos ejes de simetría tiene un rectángulo?", "Dos: uno vertical y otro horizontal, por la mitad.")],
     [("Polígonos y sus elementos", [(pol, 14), (prop, 6)]), ("Triángulos según sus lados", [(lados, 20)]), ("Cuadriláteros", [(cuad, 20)]),
      ("Ejes de simetría", [(ejes, 14), (figura, 6)]), ("Figuras simétricas", [(figura, 10), (sim, 10)])], 63011, pic=T4.shape("rombo"))
