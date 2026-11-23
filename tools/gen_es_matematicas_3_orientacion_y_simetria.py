# -*- coding: utf-8 -*-
"""
España Matemáticas 3.º de Primaria: Orientación y simetría (Sentido espacial)
Coordenadas en la cuadrícula, desplazamientos e itinerarios, ejes de simetría, figuras simétricas.
Reutiliza los generadores de 4.º (mismo ciclo).
"""
from es_low import unit, src
import gen_es_matematicas_4_simetria_y_coordenadas as S4

SEED = 33919
coord, mover, camino, ejes, figura, sim = src("simetria_y_coordenadas", SEED, "s1_coord", "s2_mover", "s2_camino", "s5_ejes", "s4_figura", "s3_simetrico")

unit(3, "orientacion-y-simetria", 19, "E", "Localización y desplazamientos en cuadrículas con coordenadas; itinerarios; simetría axial",
     "Orientación y simetría", "Orientación y simetría",
     "Fichas de matemáticas de 3.º de Primaria: coordenadas en la cuadrícula, desplazamientos, itinerarios, ejes de simetría y figuras simétricas. 100 ejercicios con soluciones.",
     "Primero se cuenta hacia la derecha", "Después, hacia arriba: (3, 5).",
     ["En la cuadrícula, (3, 5) significa: 3 hacia la <b>derecha</b> y 5 hacia <b>arriba</b>.", "Para moverte, cuenta los cuadritos: 2 a la derecha, 1 abajo…",
      "Una figura es <b>simétrica</b> si al doblarla por el <b>eje</b> las dos mitades coinciden."],
     [("Punto A en (3, 5)", ["3 a la derecha", "5 hacia arriba"], "(3, 5)"), ("Un corazón", ["Se puede doblar por la mitad"], "1 eje de simetría")],
     [["Cambiar el orden de las coordenadas", "Primero la derecha, después arriba."], ["Contar el punto de salida", "Cuenta los saltos, no los puntos."], ["Pensar que todas las líneas son ejes", "Las dos mitades deben coincidir."]],
     [("¿Qué es un eje de simetría?", "Una línea que divide una figura en dos mitades iguales que coinciden al doblarla."), ("¿Cómo se leen las coordenadas?", "El primer número indica cuánto se va a la derecha y el segundo, cuánto hacia arriba.")],
     [("Coordenadas", [(coord, 20)]), ("Desplazamientos", [(mover, 12), (camino, 8)]), ("Ejes de simetría", [(ejes, 14), (figura, 6)]), ("Figuras simétricas", [(figura, 10), (sim, 10)]),
      ("Itinerarios y repaso", [(camino, 8), (sim, 6), (coord, 6)])], 33019, S4.plano([(3, 5, "A")], n=6))
