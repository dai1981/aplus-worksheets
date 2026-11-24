# -*- coding: utf-8 -*-
"""México 3.er grado de secundaria (Fase 6): Rango y desviación media; comparar dos conjuntos de datos."""
import random
import re  # noqa: F401
import mx_s2 as S
from mx_common import src, unit, nomoney, noplanta  # noqa: F401

S.setup(random.Random(69118))
media, moda = src("gen_es_matematicas_6_estadistica", 69421, "s1_media", "s2_moda_rango", lv=6)
unit("medidas-de-dispersion", 18, "6TC",
     "Usa e interpreta la desviación media; determina y compara medidas de tendencia central y de dispersión de dos conjuntos de datos para tomar decisiones",
     "Desviación media y comparación de datos", "Medidas de dispersión",
     "Ejercicios de matemáticas de 3.er grado de secundaria: rango, desviación media, comparar dos conjuntos de datos y tomar decisiones con medidas de tendencia central y dispersión. 100 ejercicios con respuestas.",
     "Promedio de distancias a la media", "Más pequeña = datos más parejos.",
     ["Las medidas de <b>dispersión</b> dicen qué tan alejados están los datos de la media. Dos grupos pueden tener la misma media y ser muy distintos.",
      "<b>Desviación media</b>: calcula la media, la distancia (sin signo) de cada dato a la media y el promedio de esas distancias.",
      "Para decidir, compara media y dispersión: un jugador con buena media y poca dispersión es más constante."],
     [("Datos 4, 6, 8, 10 (media 7)", ["Distancias 3, 1, 1, 3", "8 ÷ 4"], "2"), ("A: media 8, DM 0.5; B: media 8, DM 2", ["misma media"], "A es más constante")],
     [["Sumar las distancias con signo", "Se usan sin signo; con signo siempre suman 0."], ["Fijarse solo en la media", "La dispersión cambia la decisión."], ["Confundir rango con desviación media", "El rango solo usa el mayor y el menor."]],
     [("¿Qué es la desviación estándar?", "Otra medida de dispersión, parecida a la desviación media, que se estudia en el bachillerato."), ("¿Cuándo conviene poca dispersión?", "Cuando se busca constancia: llenado de botellas, tiempos de entrega, calificaciones.")],
     [("Rango", [(lambda: S.dispersion("rango"), 12), (moda, 8)]), ("Desviación media", [(lambda: S.dispersion("dm"), 20)]), ("Comparar dos grupos", [(lambda: S.dispersion("comp"), 8), (lambda: S.dispersion("dm"), 12)]),
      ("Tomar decisiones", [(lambda: S.dispersion("comp2"), 4), (media, 16)]), ("Repaso", [(S.dispersion, 20)])],
     69018, lv=9)
