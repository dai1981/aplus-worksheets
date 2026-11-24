# -*- coding: utf-8 -*-
"""México, Pensamiento Matemático III (progresión 5): límites: comportamiento local de una función y leyes de los límites."""
import random
import mx_pm3 as S
from mx_common import src, unit

S.setup(random.Random(120105))
dire, inf_, ind = src("gen_es_matematicas_1bach_limites", 120305, "s_directo", "s_infinito", "s_indet", lv=1)
unit("limites", 5, ("Límites y continuidad", 5, "Límites"),
     "Describe el comportamiento local de una función con el concepto de límite, usa tablas, gráficas y las leyes de los límites, y resuelve indeterminaciones sencillas",
     "Límites de funciones", "Límites",
     "Ejercicios de Pensamiento Matemático III: límites con tablas, leyes de los límites, límites por sustitución, indeterminaciones 0/0 y límites al infinito. 100 ejercicios con respuestas.",
     "¿A qué se acerca f(x)?", "Si sale 0/0, factoriza y simplifica.",
     ["El <b>límite</b> de f(x) cuando x → a es el valor al que se acerca f(x) cuando x se acerca a a (por la izquierda y por la derecha).",
      "<b>Leyes</b>: el límite de una suma, producto o cociente es la suma, producto o cociente de los límites. En un polinomio basta sustituir.",
      "Si al sustituir sale 0/0, factoriza, simplifica y vuelve a sustituir. Al infinito, en un cociente de polinomios mandan los términos de mayor grado."],
     [("lím x→3 (x² − 9)/(x − 3)", ["0/0", "(x − 3)(x + 3)/(x − 3) = x + 3"], "6")],
     [["Decir que 0/0 = 0", "Es una indeterminación: hay que simplificar."], ["Confundir f(a) con el límite", "El límite puede existir aunque f(a) no."], ["Mirar solo un lado", "Si los laterales no coinciden, no existe."]],
     [("¿Hace falta la definición épsilon-delta?", "En el bachillerato basta la idea intuitiva y las leyes de los límites."), ("¿Qué es un límite infinito?", "Cuando f(x) crece o decrece sin parar al acercarse x a un valor: hay una asíntota vertical.")],
     [("Límites con tablas", [(lambda: S.q5("tabla"), 20)]), ("Leyes de los límites", [(lambda: S.q5("leyes"), 20)]), ("Por sustitución", [(lambda: S.q5("sust"), 8), (dire, 12)]),
      ("Indeterminaciones 0/0", [(lambda: S.q5("factor"), 10), (ind, 10)]), ("Límites al infinito", [(inf_, 20)])],
     120005, lv=12)
