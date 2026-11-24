# -*- coding: utf-8 -*-
"""México, Pensamiento Matemático I (progresión 7): diagramas de puntos, gráficas de barras e histogramas; tendencia y dispersión."""
import random
import mx_pm1 as S
import mx_s2 as S2
from mx_common import src, unit

S.setup(random.Random(100107))
S2.setup(random.Random(100117))
tab, agr = src("gen_es_matematicas_1eso_estadistica", 100307, "s_tabla2", "s_agrupados", lv=4)
unit("graficas-estadisticas", 7, ("Estadística", 7, "Descripción gráfica de datos"),
     "Describe un conjunto de datos con diagramas de puntos, gráficas de barras e histogramas, y reconoce de forma intuitiva su centro y su dispersión",
     "Diagramas de puntos, barras e histogramas", "Gráficas estadísticas",
     "Ejercicios de Pensamiento Matemático I: leer diagramas de puntos e histogramas, tablas de frecuencias, elegir la gráfica adecuada, moda y mediana en una gráfica. 100 ejercicios con respuestas.",
     "Mira el centro y la dispersión", "Elige la gráfica según el tipo de dato.",
     ["En un <b>diagrama de puntos</b> cada dato es un punto sobre su valor: se ve la moda y qué tan dispersos están.",
      "Un <b>histograma</b> agrupa datos continuos en intervalos; las barras van juntas. Una <b>gráfica de barras</b> sirve para categorías.",
      "Para la mediana, cuenta los puntos de izquierda a derecha hasta llegar al centro."],
     [("Puntos en 6, 7, 7, 8, 8, 8, 9", ["La columna más alta está en 8"], "moda = 8; mediana = 8")],
     [["Usar histograma para categorías", "Las categorías van en barras separadas."], ["Olvidar ordenar para la mediana", "En el diagrama ya están ordenados."], ["Leer la altura como el valor", "La altura es cuántos datos hay."]],
     [("¿Qué diferencia hay entre histograma y gráfica de barras?", "El histograma es para datos numéricos en intervalos (barras juntas); la de barras, para categorías (barras separadas)."),
      ("¿Qué es la forma de una distribución?", "Cómo se reparten los datos: simétrica, sesgada a la derecha o a la izquierda.")],
     [("Diagramas de puntos", [(lambda: S.p7("moda"), 7), (lambda: S.p7("cuantos"), 7), (lambda: S.p7("mayor"), 6)]), ("Mediana en un diagrama", [(lambda: S.p7("mediana"), 20)]),
      ("Histogramas", [(S2.histograma, 20)]), ("Tablas de frecuencias", [(tab, 10), (agr, 10)]),
      ("¿Qué gráfica conviene?", [(lambda: S.p7("cual"), 7), (lambda: S.p7("mayor"), 7), (S2.histograma, 6)])],
     100007, lv=10)
