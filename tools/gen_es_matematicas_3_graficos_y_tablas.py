# -*- coding: utf-8 -*-
"""
España Matemáticas 3.º de Primaria: Gráficos y tablas (Sentido estocástico)
Recuento y tablas de frecuencias, gráficos de barras, pictogramas, gráficos lineales.
Reutiliza los generadores de 4.º (mismo ciclo) con números hasta 9999.
"""
from es_low import unit, src
from es_common import grafico

SEED = 33920
tab, bar, pic, lin = src("graficos_y_tablas", SEED, "s3_tablas", "s1_barras", "s2_picto", "s4_lineal", rep=[("4.º", "3.º")])

unit(3, "graficos-y-tablas", 20, "S", "Recogida y organización de datos; tablas de frecuencias; pictogramas, gráficos de barras y lineales; interpretación",
     "Gráficos y tablas", "Gráficos y tablas",
     "Fichas de matemáticas de 3.º de Primaria: recuento con marcas, tablas, gráficos de barras, pictogramas y gráficos lineales. 100 ejercicios con soluciones.",
     "Mira la escala y la leyenda", "Cada dibujo puede valer más de 1.",
     ["Para contar datos, haz <b>marcas</b> de 5 en 5 y escríbelas en una <b>tabla</b>.", "En un gráfico de barras, mira hasta dónde llega cada barra en la escala.",
      "En un <b>pictograma</b>, cada dibujo puede valer más de 1: lee la leyenda."],
     [("Cada dibujo vale 2 y hay 4 dibujos", ["4 × 2"], "8"), ("Barra del lunes en 12 y del martes en 8", ["12 − 8"], "4 más el lunes")],
     [["Contar dibujos sin mirar la leyenda", "Si cada dibujo vale 5, 3 dibujos son 15."], ["Leer mal la escala", "Mira de cuánto en cuánto va."], ["Confundir «cuántos más» con el total", "«Cuántos más» es una resta."]],
     [("¿Qué es un pictograma?", "Un gráfico que usa dibujos. Cada dibujo representa una cantidad, que se indica en la leyenda."), ("¿Para qué sirve una tabla de frecuencias?", "Para ordenar los datos y ver cuántas veces aparece cada uno.")],
     [("Recuento y tablas", [(tab, 20)]), ("Gráficos de barras", [(bar, 20)]), ("Pictogramas", [(pic, 20)]), ("Gráficos lineales", [(lin, 20)]), ("Repaso con datos", [(bar, 8), (pic, 6), (tab, 6)])],
     33020, grafico([("lunes", 12), ("martes", 8), ("miércoles", 15)], "alumnos"))
