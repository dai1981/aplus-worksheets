# -*- coding: utf-8 -*-
"""México, Pensamiento Matemático I (progresión 13): media, mediana, moda, varianza, desviación estándar y rango intercuartílico."""
import random
import mx_pm1 as S
from mx_common import src, unit

S.setup(random.Random(100113))
cua, dis = src("gen_es_matematicas_1eso_estadistica", 100313, "s_cuartiles", "s_dispersion", lv=4)
unit("medidas-de-tendencia-central-y-dispersion", 13, ("Estadística", 13, "Medidas de tendencia central y de dispersión"),
     "Describe fenómenos con la media, la mediana, la moda, la varianza, la desviación estándar y el rango intercuartílico, e interpreta lo que indican",
     "Media, varianza y desviación estándar", "Tendencia central y dispersión",
     "Ejercicios de Pensamiento Matemático I: media, mediana, cuartiles, rango intercuartílico, varianza y desviación estándar, e interpretación de la dispersión. 100 ejercicios con respuestas.",
     "σ = √(promedio de (x − x̄)²)", "Mayor σ: datos más dispersos.",
     ["<b>Centro</b>: media (suma ÷ n), mediana (dato central ordenado) y moda (el más frecuente).",
      "<b>Varianza</b> σ²: promedio de los cuadrados de las distancias a la media. <b>Desviación estándar</b> σ = √σ².",
      "<b>Rango intercuartílico</b>: RIC = Q₃ − Q₁; mide la dispersión del 50 % central y no le afectan los atípicos."],
     [("Datos 4, 6, 8, 10, 12 (media 8)", ["Distancias: −4, −2, 0, 2, 4", "Cuadrados: 16 + 4 + 0 + 4 + 16 = 40", "σ² = 40 ÷ 5 = 8"], "σ = √8 ≈ 2.83")],
     [["Olvidar elevar al cuadrado", "Las distancias con signo suman 0."], ["Confundir varianza con desviación estándar", "σ es la raíz de σ²."], ["No ordenar para la mediana", "Ordena antes de buscar el centro."]],
     [("¿Por qué a veces se divide entre n − 1?", "En una muestra, dividir entre n − 1 da una mejor estimación de la varianza de la población (varianza muestral)."),
      ("¿Qué indica una desviación estándar grande?", "Que los datos están muy separados de la media.")],
     [("Media y mediana", [(lambda: S.p13("media"), 10), (lambda: S.p13("mediana"), 10)]), ("Cuartiles y RIC", [(cua, 10), (lambda: S.p13("ric"), 10)]),
      ("Varianza", [(lambda: S.p13("var"), 20)]), ("Desviación estándar", [(lambda: S.p13("sd"), 20)]),
      ("Comparar e interpretar", [(dis, 14), (lambda: S.p13("interp"), 6)])],
     100013, lv=10)
