# -*- coding: utf-8 -*-
"""México, Pensamiento Matemático II (progresión 11): geometría analítica básica: distancia entre puntos, punto medio, perímetros y áreas en el plano."""
import random
import mx_pm2 as S
from mx_common import src, unit

S.setup(random.Random(110111))
dis, pen = src("gen_es_matematicas_4eso_geometria_analitica", 110311, "s_distancia", "s_pendiente")
unit("geometria-analitica", 11, ("Geometría", 11, "Geometría analítica: distancias y áreas"),
     "Usa el sistema de coordenadas para calcular distancias entre puntos, puntos medios, pendientes, perímetros y áreas, y compara este método con la geometría sintética",
     "Distancia, punto medio y áreas en el plano", "Geometría analítica",
     "Ejercicios de Pensamiento Matemático II: distancia entre dos puntos, punto medio, extremo de un segmento, pendiente, perímetro y área de triángulos con coordenadas. 100 ejercicios con respuestas.",
     "d = √((x₂ − x₁)² + (y₂ − y₁)²)", "Es Pitágoras en el plano.",
     ["La <b>distancia</b> entre A(x₁, y₁) y B(x₂, y₂) sale de Pitágoras: d = √((x₂ − x₁)² + (y₂ − y₁)²).",
      "El <b>punto medio</b> es el promedio de las coordenadas: M = ((x₁ + x₂)/2, (y₁ + y₂)/2).",
      "El área de un triángulo con vértices dados: A = ½ |x₁(y₂ − y₃) + x₂(y₃ − y₁) + x₃(y₁ − y₂)|."],
     [("A(1, 2) y B(7, 10)", ["Δx = 6, Δy = 8", "d = √(36 + 64)", "M = (4, 6)"], "d = 10")],
     [["Restar las coordenadas en distinto orden", "Usa (x₂ − x₁) y (y₂ − y₁) con el mismo orden."], ["Olvidar la raíz", "d² = 100 → d = 10."], ["Promediar mal con negativos", "(−3 + 5)/2 = 1."]],
     [("¿Qué ventaja tiene la geometría analítica?", "Convierte problemas de figuras en cálculos con números, que se pueden hacer con calculadora o computadora."),
      ("¿Cómo sé si tres puntos están alineados?", "Si el área del triángulo que forman es 0 (o si las pendientes entre ellos son iguales).")],
     [("Distancia entre puntos", [(lambda: S.lp11("dist"), 10), (dis, 10)]), ("Punto medio", [(lambda: S.lp11("medio"), 14), (lambda: S.lp11("extremo"), 6)]),
      ("Pendiente", [(pen, 20)]), ("Perímetros", [(lambda: S.lp11("perim"), 12), (dis, 8)]), ("Áreas con coordenadas", [(lambda: S.lp11("area"), 20)])],
     110011, lv=11)
