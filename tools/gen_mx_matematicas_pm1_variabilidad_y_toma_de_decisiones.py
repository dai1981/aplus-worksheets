# -*- coding: utf-8 -*-
"""México, Pensamiento Matemático I (progresión 1): variabilidad, aleatoriedad y toma de decisiones con datos."""
import random
import mx_pm1 as S
from mx_common import src, unit

S.setup(random.Random(100101))
var = src("gen_es_matematicas_1eso_estadistica", 100301, "s_variable", lv=4)
unit("variabilidad-y-toma-de-decisiones", 1, ("Probabilidad", 1, "Variabilidad, aleatoriedad y toma de decisiones"),
     "Reconoce la variabilidad y la aleatoriedad en situaciones cotidianas y valora el uso de datos para tomar decisiones personales y colectivas",
     "Variabilidad y toma de decisiones", "Variabilidad y decisiones",
     "Ejercicios de Pensamiento Matemático I: fenómenos aleatorios y deterministas, preguntas estadísticas, variabilidad con el rango y decisiones con datos. 100 ejercicios con respuestas.",
     "Los datos varían; decide con ellos", "Compara el centro y cuánto varían.",
     ["Un fenómeno es <b>aleatorio</b> si cada vez puede dar un resultado distinto y no se puede saber antes (lanzar un dado). Si siempre da lo mismo, es <b>determinista</b>.",
      "Una <b>pregunta estadística</b> espera respuestas que varían: «¿cuántas horas duermen los alumnos?». «¿Qué día es hoy?» no lo es.",
      "Para decidir con datos mira dos cosas: el <b>centro</b> (la media) y la <b>variabilidad</b> (el rango = mayor − menor)."],
     [("Ruta A: 20, 22, 21, 23, 19 min. Ruta B: 12, 30, 15, 28, 20 min.", ["Media de las dos: 21 min", "Rango A = 4; rango B = 18"], "Para llegar a tiempo, la ruta A"),
      ("¿«Cuántos goles habrá en el partido» es aleatorio?", ["No se puede saber antes"], "Sí, es aleatorio")],
     [["Elegir solo por la media", "Revisa también cuánto varían los datos."], ["Pensar que aleatorio = sin patrón", "Con muchos datos aparecen regularidades."], ["Confundir pregunta estadística con dato único", "Debe esperar respuestas distintas."]],
     [("¿Qué es la variabilidad?", "Que los datos no son todos iguales: cambian de una persona, día o repetición a otra."),
      ("¿Por qué decidir con datos?", "Porque reducen la incertidumbre: muestran qué pasa normalmente y cuánto puede cambiar.")],
     [("Aleatorio o determinista", [(lambda: S.p1("aleat"), 14), (lambda: S.p1("estad"), 6)]),
      ("Preguntas estadísticas y variables", [(lambda: S.p1("estad"), 8), (var, 6), (lambda: S.p6("cual"), 6)]),
      ("Variabilidad con el rango", [(lambda: S.p1("rango"), 20)]),
      ("Decidir con la media", [(lambda: S.p1("decide2"), 20)]),
      ("Decidir con media y variabilidad", [(lambda: S.p1("decide"), 14), (lambda: S.p1("rango"), 6)])],
     100001, lv=10)
