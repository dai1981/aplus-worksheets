# -*- coding: utf-8 -*-
"""
España Matemáticas 3.º de Primaria: Polígonos, triángulos y cuadriláteros (Sentido espacial)
Reutiliza los generadores de 4.º (mismo ciclo).
"""
from es_low import unit, src
import gen_es_matematicas_4_triangulos_y_cuadrilateros as T4

SEED = 33917
lados, angs, cuad, prop, pol = src("triangulos_y_cuadrilateros", SEED, "s1_lados", "s1_angulos", "s3_cuad", "s4_prop", "s4_poligonos")

unit(3, "poligonos", 17, "E", "Figuras planas: polígonos y sus elementos (lados, vértices, ángulos); clasificación de triángulos y cuadriláteros",
     "Polígonos, triángulos y cuadriláteros", "Polígonos",
     "Fichas de matemáticas de 3.º de Primaria: polígonos y sus nombres, lados y vértices, triángulos, cuadrado, rectángulo, rombo y trapecio. 100 ejercicios con soluciones.",
     "Polígono: lados rectos y cerrado", "Se nombra por su número de lados.",
     ["Un <b>polígono</b> es una figura plana y cerrada con lados rectos. Tiene lados, vértices y ángulos.",
      "3 lados: triángulo; 4: cuadrilátero; 5: pentágono; 6: hexágono; 8: octógono.",
      "Triángulos: equilátero (3 lados iguales), isósceles (2) y escaleno (ninguno).", "Cuadriláteros: cuadrado, rectángulo, rombo, romboide y trapecio."],
     [("Una figura con 6 lados", ["6 lados → hexágono"], "hexágono"), ("Triángulo con lados de 5, 5 y 3 cm", ["Dos lados iguales"], "isósceles")],
     [["Llamar polígono a un círculo", "El círculo no tiene lados rectos."], ["Confundir rombo y cuadrado", "El cuadrado tiene ángulos rectos; el rombo, no."], ["Contar mal los vértices", "Marca cada vértice al contarlo."]],
     [("¿Qué es un polígono?", "Una figura plana cerrada formada por segmentos rectos, que son sus lados."), ("¿Qué es un triángulo isósceles?", "Un triángulo que tiene dos lados iguales.")],
     [("Polígonos y sus elementos", [(pol, 14), (prop, 6)]), ("Triángulos según sus lados", [(lados, 20)]), ("Triángulos según sus ángulos", [(angs, 20)]),
      ("Cuadriláteros", [(cuad, 20)]), ("Repaso", [(lados, 6), (cuad, 6), (pol, 4), (prop, 4)])], 33017, T4.shape("rombo"))
