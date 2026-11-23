# -*- coding: utf-8 -*-
"""
México 3.er grado: Organización e interpretación de datos (tablas de frecuencias, pictogramas, gráficas de barras, moda).
Reutiliza España 4.º con otra semilla y añade preguntas de moda con datos de la escuela.
"""
import random
from mx_common import src, unit, mcq, Kids
import es_common as ES

R = random.Random(63117)
tab, bar, pic = src("gen_es_matematicas_4_graficos_y_tablas", 63219, "s3_tablas", "s1_barras", "s2_picto")

TEMAS = [("fruta favorita", ["mango", "plátano", "manzana", "sandía", "naranja"]), ("deporte favorito", ["futbol", "basquetbol", "natación", "beisbol", "voleibol"]),
         ("color favorito", ["azul", "rojo", "verde", "morado", "amarillo"]), ("animal favorito", ["perro", "gato", "conejo", "tortuga", "perico"]),
         ("sabor de agua fresca", ["jamaica", "horchata", "limón", "tamarindo", "piña"])]


def s_moda():
    tema, ops = R.choice(TEMAS)
    k = R.randint(3, 5)
    cats = R.sample(ops, k)
    vals = R.sample(range(2, 15), k)
    t = R.choice(["moda", "moda", "total", "diferencia"])
    T = ES.table(["Respuesta", "Alumnos"], [[c, str(v)] for c, v in zip(cats, vals)])
    i = vals.index(max(vals))
    if t == "moda":
        return mcq(T + "Se preguntó a un grupo por su %s. ¿Cuál es la moda?" % tema, cats[i], [c for j, c in enumerate(cats) if j != i] + [str(max(vals))],
                   "La <b>moda</b> es el dato que más se repite: %s, con %d alumnos." % (cats[i], max(vals)))
    if t == "total":
        return mcq(T + "Se preguntó a un grupo por su %s. ¿A cuántos alumnos se preguntó?" % tema, str(sum(vals)), [str(sum(vals) - min(vals)), str(max(vals)), str(sum(vals) + 1), str(k)],
                   "Sumamos todas las frecuencias: <b>%d</b>." % sum(vals))
    a, b = R.sample(range(k), 2)
    if vals[a] < vals[b]:
        a, b = b, a
    return mcq(T + "¿Cuántos alumnos más eligieron %s que %s?" % (cats[a], cats[b]), str(vals[a] - vals[b]), [str(vals[a] + vals[b]), str(vals[a]), str(vals[a] - vals[b] + 1)],
               "%d − %d = <b>%d</b>." % (vals[a], vals[b], vals[a] - vals[b]))


unit("tablas-y-graficas", 17, "D",
     "Recolecta, organiza, representa e interpreta datos en tablas de frecuencias, pictogramas y gráficas de barras; reconoce la moda de un conjunto de datos",
     "Tablas y gráficas", "Tablas y gráficas",
     "Ejercicios de matemáticas de 3.er grado de primaria: tablas de frecuencias, pictogramas, gráficas de barras y la moda. 100 ejercicios con respuestas.",
     "La moda es el dato que más se repite", "Lee los títulos antes que los números.",
     ["Una <b>tabla de frecuencias</b> dice cuántas veces aparece cada dato. Para contar, usa marcas de conteo: ||||| = 5.",
      "En un <b>pictograma</b>, cada dibujo vale una cantidad: mira la clave. En una <b>gráfica de barras</b>, la altura de la barra es la frecuencia.",
      "La <b>moda</b> es el dato que más se repite: la barra más alta."],
     [("Mango 8, plátano 5, sandía 11", ["La mayor frecuencia es 11"], "la moda es sandía"), ("Pictograma: cada dibujo vale 2; hay 4 dibujos", ["4 × 2"], "8")],
     [["Contar dibujos sin mirar la clave", "Si cada dibujo vale 2, 4 dibujos son 8."], ["Confundir la moda con el número mayor", "La moda es el dato (sandía), no la frecuencia (11)."], ["Leer mal la escala", "Mira de cuánto en cuánto va el eje."]],
     [("¿Qué es la moda?", "Es el dato que aparece más veces. En una gráfica de barras, es la barra más alta."),
      ("¿Para qué sirve una tabla de frecuencias?", "Para organizar los datos de una encuesta y ver rápido cuántas veces aparece cada respuesta.")],
     [("Conteo y tablas", [(tab, 20)]), ("Gráficas de barras", [(bar, 20)]), ("Pictogramas", [(pic, 20)]), ("La moda", [(s_moda, 20)]), ("Repaso con datos", [(bar, 8), (pic, 6), (tab, 6)])],
     63017)
