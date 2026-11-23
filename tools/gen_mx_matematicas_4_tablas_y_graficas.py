# -*- coding: utf-8 -*-
"""México 4.º grado: Organización e interpretación de datos (tablas de frecuencias, gráficas de barras y la moda). Reutiliza España 4.º/5.º con otra semilla y añade preguntas propias."""
import random
from mx_common import src, unit, mcq, num, keep
import es_common as ES

NO = ("rango", "media", "relativa", "porcentaje", "sectores", "%")


def ok(it):
    t = it["q"] + " ".join(it["c"]) + it["e"]
    return not any(w in t for w in NO)


tab, bar, lin = src("gen_es_matematicas_4_graficos_y_tablas", 64222, "s3_tablas", "s1_barras", "s4_lineal", extra=(ok,), rep=[("gráfico lineal", "gráfica de línea")])
moda5, frec5, graf5 = src("gen_es_matematicas_6_estadistica", 64322, "s2_moda_rango", "s3_frecuencias", "s4_graficos", lv=5, extra=(ok,))
R = random.Random(64122)

TEMAS = [("fruta favorita", ["mango", "plátano", "guayaba", "sandía", "papaya", "piña"]), ("deporte favorito", ["futbol", "basquetbol", "natación", "beisbol", "voleibol", "atletismo"]),
         ("transporte para ir a la escuela", ["a pie", "en camión", "en carro", "en bicicleta", "en metro"]), ("antojito favorito", ["tacos", "tamales", "quesadillas", "elotes", "sopes", "tostadas"]),
         ("sabor de agua fresca", ["jamaica", "horchata", "limón", "tamarindo", "piña", "melón"])]


def tabla():
    tema, ops = R.choice(TEMAS)
    k = R.randint(4, 5)
    cats = R.sample(ops, k)
    vals = R.sample(range(5, 60), k)
    T = ES.table(["Respuesta", "Alumnos"], [[c, str(v)] for c, v in zip(cats, vals)])
    t = R.choice(["moda", "total", "diferencia", "menos", "juntos"])
    i = vals.index(max(vals))
    if t == "moda":
        return mcq(T + "En una escuela se preguntó por el %s. ¿Cuál es la moda?" % tema, cats[i], [c for j, c in enumerate(cats) if j != i] + [str(max(vals))],
                   "La <b>moda</b> es el dato con mayor frecuencia: %s, con %d alumnos." % (cats[i], max(vals)))
    if t == "menos":
        j = vals.index(min(vals))
        return mcq(T + "En una escuela se preguntó por el %s. ¿Qué respuesta tuvo menos votos?" % tema, cats[j], [c for m, c in enumerate(cats) if m != j],
                   "La frecuencia menor es %d: <b>%s</b>." % (min(vals), cats[j]))
    if t == "total":
        return mcq(T + "En una escuela se preguntó por el %s. ¿A cuántos alumnos se preguntó?" % tema, num(sum(vals)), [num(sum(vals) - min(vals)), num(max(vals)), num(sum(vals) + 10), num(sum(vals) - 1)],
                   "Sumamos todas las frecuencias: <b>%s</b>." % num(sum(vals)))
    a, b = R.sample(range(k), 2)
    if t == "juntos":
        return mcq(T + "¿Cuántos alumnos eligieron %s o %s?" % (cats[a], cats[b]), str(vals[a] + vals[b]), [str(abs(vals[a] - vals[b])), str(vals[a] + vals[b] + 1), str(max(vals[a], vals[b]))],
                   "%d + %d = <b>%d</b>." % (vals[a], vals[b], vals[a] + vals[b]))
    if vals[a] < vals[b]:
        a, b = b, a
    return mcq(T + "¿Cuántos alumnos más eligieron %s que %s?" % (cats[a], cats[b]), str(vals[a] - vals[b]), [str(vals[a] + vals[b]), str(vals[a]), str(vals[a] - vals[b] + 1)],
               "%d − %d = <b>%d</b>." % (vals[a], vals[b], vals[a] - vals[b]))


unit("tablas-y-graficas", 18, "D",
     "Recolecta, registra y organiza datos en tablas de frecuencias; los representa e interpreta en gráficas de barras; identifica la moda y responde preguntas a partir de los datos",
     "Tablas, gráficas de barras y moda", "Tablas y gráficas",
     "Ejercicios de matemáticas de 4.º grado de primaria: tablas de frecuencias, gráficas de barras, la moda, comparar datos y gráficas de línea. 100 ejercicios con respuestas.",
     "La moda es el dato que más se repite", "En la gráfica, es la barra más alta.",
     ["Una <b>tabla de frecuencias</b> dice cuántas veces aparece cada dato. La suma de las frecuencias es el total de datos.",
      "En una <b>gráfica de barras</b>, la altura de cada barra es la frecuencia. Mira de cuánto en cuánto va la escala del eje.",
      "La <b>moda</b> es el dato que más se repite: el que tiene mayor frecuencia o la barra más alta."],
     [("Tacos 18, tamales 12, elotes 25", ["La frecuencia mayor es 25"], "la moda es elotes"), ("¿Cuántos más eligieron tacos que tamales?", ["18 − 12"], "6")],
     [["Dar la frecuencia en lugar del dato", "La moda es «elotes», no 25."], ["Leer mal la escala", "Si el eje va de 5 en 5, la marca entre 10 y 20 vale 15."], ["Olvidar un dato al sumar", "Suma todas las frecuencias para el total."]],
     [("¿Qué es la moda?", "Es el dato que aparece más veces. En una tabla, el de mayor frecuencia; en una gráfica de barras, el de la barra más alta."),
      ("¿Para qué sirve una gráfica de barras?", "Para comparar de un vistazo cuántas veces aparece cada dato: la barra más alta es la más frecuente.")],
     [("Tablas de frecuencias", [(tab, 8), (frec5, 12)]), ("Gráficas de barras", [(bar, 12), (graf5, 8)]), ("La moda", [(moda5, 20)]), ("Preguntas con datos", [(tabla, 20)]),
      ("Gráficas de línea", [(lin, 20)])],
     64018, lv=4)
