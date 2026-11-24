# -*- coding: utf-8 -*-
"""México 1.er grado de secundaria (Fase 6): Tablas, gráficas de barras y gráficas circulares para analizar información."""
import random
import mx_s1 as S
from mx_common import src, unit, nomoney, noplanta  # noqa: F401

S.setup(random.Random(67119))
frec, graf = src("gen_es_matematicas_6_estadistica", 67481, "s3_frecuencias", "s4_graficos", lv=6)
var, tab = src("gen_es_matematicas_1eso_estadistica", 67482, "s_variable", "s_tabla2", lv=1)

unit("tablas-y-graficas", 19, "6OR",
     "Usa tablas, gráficas de barras y circulares para el análisis de información",
     "Tablas, gráficas de barras y circulares", "Tablas y gráficas",
     "Ejercicios de matemáticas de 1.er grado de secundaria: tablas de frecuencias, gráficas de barras y gráficas circulares; leer, construir e interpretar información. 100 ejercicios con respuestas.",
     "Sector = porcentaje × 360°", "25 % → 90°; 50 % → 180°.",
     ["Una <b>tabla de frecuencias</b> cuenta cuántas veces aparece cada dato. La <b>gráfica de barras</b> compara esas cantidades con la altura de las barras.",
      "La <b>gráfica circular</b> muestra partes de un todo: cada sector mide su porcentaje de 360°. El 25 % ocupa 90°.",
      "Antes de responder, lee el título, los ejes y la escala de la gráfica."],
     [("30 de 120 alumnos", ["30 ÷ 120 = 25 %", "25 % de 360°"], "90°"), ("Sector de 72°", ["72 ÷ 360 = 0.2"], "20 %")],
     [["No leer la escala", "Si cada línea vale 5, una barra a 4 líneas vale 20."], ["Usar 100° como el total", "Un círculo tiene 360°."], ["Comparar porcentajes de grupos distintos", "El 50 % de 40 no es lo mismo que el 50 % de 400."]],
     [("¿Cuándo uso una gráfica circular?", "Cuando quieres mostrar cómo se reparte un total en partes."), ("¿Qué es la frecuencia absoluta?", "El número de veces que aparece un dato.")],
     [("Tablas de frecuencias", [(frec, 20)]), ("Gráficas de barras", [(graf, 20)]), ("Gráficas circulares", [(S.circular, 20)]), ("Tipos de datos y tablas", [(var, 8), (tab, 12)]), ("Problemas", [(S.circular, 10), (graf, 10)])],
     67019, lv=7)
