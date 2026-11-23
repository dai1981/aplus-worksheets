# -*- coding: utf-8 -*-
"""México 5.º grado: Organización e interpretación de datos: tablas de frecuencias, gráficas de barras y la moda (Fase 5). Reutiliza España 6.º (nivel 5.º) y 4.º con otra semilla."""
from mx_common import src, unit

NO = ("media", "mediana", "sectores", "relativa", "%")


def ok(it):
    t = it["q"] + " ".join(it["c"]) + it["e"]
    return not any(w in t for w in NO)


moda, frec, graf, probl = src("gen_es_matematicas_6_estadistica", 65321, "s2_moda_rango", "s3_frecuencias", "s4_graficos", "s5_problema", lv=5, extra=(ok,))
bar, tab, lin = src("gen_es_matematicas_4_graficos_y_tablas", 65221, "s1_barras", "s3_tablas", "s4_lineal", extra=(ok,), rep=[("gráfico lineal", "gráfica de línea")])

unit("tablas-y-graficas", 15, "D",
     "Recolecta, registra y organiza datos en tablas de frecuencia absoluta; los representa en gráficas de barras; interpreta la información e identifica la moda y el rango",
     "Tablas, gráficas, moda y rango", "Tablas y gráficas",
     "Ejercicios de matemáticas de 5.º grado de primaria: tablas de frecuencias, gráficas de barras y de línea, la moda y el rango, y problemas con datos. 100 ejercicios con respuestas.",
     "Moda: el dato más frecuente", "Rango: el mayor menos el menor.",
     ["Una <b>tabla de frecuencias</b> dice cuántas veces aparece cada dato. La suma de las frecuencias es el total de datos.",
      "En una <b>gráfica de barras</b>, lee primero el título y la escala del eje. La barra más alta es la <b>moda</b>.",
      "El <b>rango</b> mide cuánto varían los datos: dato mayor − dato menor."],
     [("Datos: 4, 7, 7, 2, 9, 7", ["el 7 aparece 3 veces", "9 − 2"], "moda 7, rango 7")],
     [["Dar la frecuencia en lugar del dato", "La moda es el dato, no cuántas veces aparece."], ["Leer mal la escala", "Mira de cuánto en cuánto va el eje."], ["Restar dos datos cualquiera para el rango", "Es el mayor menos el menor."]],
     [("¿Qué es la moda?", "El dato que más se repite. Si en una encuesta 12 alumnos eligen futbol y es la mayor frecuencia, la moda es futbol."),
      ("¿Qué es el rango?", "La diferencia entre el dato mayor y el menor. Dice qué tan separados están los datos.")],
     [("Tablas de frecuencias", [(frec, 14), (tab, 6)]), ("Gráficas de barras", [(bar, 12), (graf, 8)]), ("Moda y rango", [(moda, 20)]), ("Gráficas de línea", [(lin, 20)]), ("Problemas con datos", [(probl, 4), (bar, 8), (tab, 8)])],
     65015, lv=5)
