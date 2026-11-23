# -*- coding: utf-8 -*-
"""México 6.º grado: Gráficas circulares, tablas de frecuencia absoluta y relativa (Organización e interpretación de datos). Reutiliza España 6.º con otra semilla."""
from mx_common import src, unit, keep

frec, graf, probl = src("gen_es_matematicas_6_estadistica", 66321, "s3_frecuencias", "s4_graficos", "s5_problema", lv=6)
sect = keep(graf, lambda it: "sector" in it["q"] + it["e"] or "circular" in it["q"] + it["e"])

unit("graficas-circulares", 13, "D",
     "Lee e interpreta gráficas circulares y de barras; organiza datos en tablas de frecuencia absoluta y relativa (fracción y porcentaje) y resuelve problemas con ellas",
     "Gráficas circulares y frecuencias", "Gráficas circulares",
     "Ejercicios de matemáticas de 6.º grado de primaria: gráficas circulares, frecuencia absoluta y relativa, porcentajes en gráficas y gráficas de barras. 100 ejercicios con respuestas.",
     "Todo el círculo es el 100 %", "Media vuelta = 50 %; un cuarto = 25 %.",
     ["En una <b>gráfica circular</b>, el círculo completo representa el total (100 %) y cada sector, una parte: la mitad es 50 %, un cuarto es 25 %.",
      "La <b>frecuencia absoluta</b> dice cuántas veces aparece un dato; la <b>relativa</b>, qué parte del total es: 6 de 24 = 6/24 = 1/4 = 25 %.",
      "Para saber cuántos son, multiplica el porcentaje por el total: 25 % de 40 alumnos = 10 alumnos."],
     [("40 alumnos; el sector de futbol es la mitad", ["50 % de 40"], "20 alumnos"), ("8 de 32 eligen mango", ["8/32 = 1/4"], "25 %")],
     [["Pensar que el sector más grande es el número mayor de la tabla, sin mirar el total", "Compara partes del mismo total."], ["Sumar porcentajes que no dan 100 %", "Todos los sectores suman 100 %."], ["Confundir frecuencia absoluta y relativa", "La relativa es una fracción del total."]],
     [("¿Para qué sirve una gráfica circular?", "Para ver qué parte del total representa cada categoría. Todos los sectores juntos forman el 100 %."),
      ("¿Qué es la frecuencia relativa?", "La frecuencia de un dato dividida entre el total de datos. Se puede escribir como fracción, decimal o porcentaje.")],
     [("Tablas de frecuencias", [(frec, 20)]), ("Gráficas circulares", [(sect, 20)]), ("Gráficas de barras y circulares", [(graf, 20)]), ("Frecuencia relativa", [(frec, 20)]), ("Problemas con datos", [(probl, 10), (graf, 10)])],
     66013, lv=6)
