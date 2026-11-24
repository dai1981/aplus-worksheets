# -*- coding: utf-8 -*-
"""México, Temas Selectos de Matemáticas II (progresión 3): sumas de Riemann y definición de la integral definida."""
import random
import mx_tsm as S
import mx_pm3 as P3
from mx_common import src, unit

S.setup(random.Random(140103))
prop = src("gen_es_matematicas_2bach_integrales_definidas", 140303, "s_propiedades")
unit("sumas-de-riemann", 3, ("Integral", 3, "Sumas de Riemann e integral definida"),
     "Aproxima el área bajo una curva con sumas de rectángulos (sumas de Riemann) y define la integral definida como el límite de esas sumas",
     "Sumas de Riemann e integral definida", "Sumas de Riemann",
     "Ejercicios de Temas Selectos de Matemáticas II: ancho de los subintervalos, sumas de Riemann con extremo derecho y punto medio, notación sigma y propiedades de la integral definida. 100 ejercicios con respuestas.",
     "∫ f dx = lím Σ f(xᵢ)Δx", "Más rectángulos, mejor aproximación.",
     ["Para aproximar el área bajo f en [a, b], se divide en n partes de ancho <b>Δx = (b − a)/n</b> y se suman rectángulos de altura f(xᵢ).",
      "La altura puede tomarse en el extremo izquierdo, el derecho o el punto medio de cada subintervalo. La suma se escribe con <b>Σ</b>.",
      "La <b>integral definida</b> es el límite de estas sumas cuando n → ∞."],
     [("f(x) = x² en [0, 2], n = 2, extremo derecho", ["Δx = 1", "f(1) + f(2) = 1 + 4"], "5 (el área exacta es 8/3)")],
     [["Olvidar multiplicar por Δx", "Cada rectángulo es altura × ancho."], ["Usar el extremo equivocado", "Lee si es izquierdo, derecho o medio."], ["Pensar que la aproximación es exacta", "Solo en el límite se obtiene el valor exacto."]],
     [("¿Por qué el punto medio suele aproximar mejor?", "Porque los excesos y faltantes de cada rectángulo se compensan."), ("¿Qué significa el símbolo ∫?", "Es una «S» alargada de «suma», introducida por Leibniz.")],
     [("Ancho de los rectángulos", [(lambda: S.u3("dx"), 20)]), ("Extremo derecho", [(lambda: S.u3("suma"), 20)]), ("Punto medio", [(lambda: S.u3("medio"), 14), (lambda: P3.q15("riemann"), 6)]),
      ("Notación sigma", [(lambda: S.u3("sigma"), 20)]), ("Propiedades e ideas", [(prop, 15), (lambda: S.u3("limite"), 5)])],
     140003, lv=14)
