# -*- coding: utf-8 -*-
"""México, Temas Selectos de Matemáticas I (progresión 9): fractales: conjunto de Cantor, triángulo de Sierpiński, copo de Koch, conjuntos de Mandelbrot y Julia."""
import random
import mx_tsm as S
from mx_common import unit

S.setup(random.Random(130109))
unit("fractales", 9, ("Fractales", 9, "Fractales"),
     "Explora fractales como el conjunto de Cantor, el triángulo de Sierpiński, el copo de Koch y los conjuntos de Mandelbrot y Julia: autosimilitud, iteración y dimensión",
     "Cantor, Sierpiński, Koch y Mandelbrot", "Fractales",
     "Ejercicios de Temas Selectos de Matemáticas I: pasos del conjunto de Cantor, triángulo de Sierpiński y copo de Koch, dimensión de autosimilitud y conjunto de Mandelbrot. 100 ejercicios con respuestas.",
     "Se repite a cualquier escala", "D = log N ÷ log s",
     ["Un <b>fractal</b> es una figura autosimilar: sus partes son copias reducidas del todo. Se construye repitiendo una regla (iteración).",
      "<b>Cantor</b>: se quita el tercio central (quedan 2ⁿ segmentos). <b>Sierpiński</b>: se quita el triángulo central (quedan 3ⁿ). <b>Koch</b>: cada lado se vuelve 4 de 1/3.",
      "La <b>dimensión</b> D = log N ÷ log s (N copias reducidas a 1/s) suele no ser entera. <b>Mandelbrot</b>: los c para los que z → z² + c, desde 0, no se va al infinito."],
     [("Copo de Koch, perímetro inicial 3", ["Cada paso × 4/3", "2 pasos: 3 × 16/9"], "16/3")],
     [["Sumar en vez de multiplicar en cada paso", "Cada paso multiplica por el mismo factor."], ["Pensar que perímetro infinito implica área infinita", "El copo de Koch tiene área finita."], ["Usar log s ÷ log N", "Es log N ÷ log s."]],
     [("¿Dónde hay fractales en la naturaleza?", "En helechos, brócoli romanesco, costas, rayos, ramas de árboles y vasos sanguíneos."), ("¿Quién acuñó la palabra fractal?", "Benoît Mandelbrot, en 1975.")],
     [("Conjunto de Cantor", [(lambda: S.t9("cantor"), 20)]), ("Triángulo de Sierpiński", [(lambda: S.t9("sierp"), 20)]), ("Copo de Koch", [(lambda: S.t9("koch"), 20)]),
      ("Dimensión fractal", [(lambda: S.t9("dim"), 8), (lambda: S.t9("cantor"), 6), (lambda: S.t9("koch"), 6)]), ("Mandelbrot y Julia", [(lambda: S.t9("mandel"), 14), (lambda: S.t9("sierp"), 6)])],
     130009, lv=13)
