# -*- coding: utf-8 -*-
"""
España Matemáticas Aplicadas a las Ciencias Sociales II (2.º de Bachillerato): Probabilidad (Sentido estocástico)
Sucesos y Laplace, tablas de contingencia, probabilidad condicionada, independencia, probabilidad total y teorema de Bayes.
Reutiliza los generadores de Matemáticas II y de 1.º CCSS con otra semilla.
Errores: confundir P(A|B) con P(B|A), confundir independientes con incompatibles, olvidar una rama del árbol.
"""
import random
from es_ccss import M, mix, unit, L, use_

R = random.Random(54007)
s_contingencia, = use_("gen_es_matematicas_1ccss_probabilidad", 54307, "s_contingencia"),
s_sucesos, s_laplace, s_independencia, s_condicionada, s_bayes = use_("gen_es_matematicas_2bach_probabilidad", 54107, "s_sucesos", "s_laplace", "s_independencia", "s_condicionada", "s_bayes")

seen = set()
sets = [("Sucesos y Laplace", mix(R, seen, [(s_sucesos, 10), (s_laplace, 10)])), ("Tablas de contingencia", mix(R, seen, [(s_contingencia, 20)])), ("Probabilidad condicionada", mix(R, seen, [(s_condicionada, 20)])),
        ("Sucesos independientes", mix(R, seen, [(s_independencia, 20)])), ("Probabilidad total y Bayes", mix(R, seen, [(s_bayes, 20)]))]
think = ["P(A ∪ B) = P(A) + P(B) − P(A ∩ B); P(Ā) = 1 − P(A). Leyes de De Morgan: el contrario de A ∪ B es Ā ∩ B̄.",
         "<b>Condicionada</b>: P(A|B) = P(A ∩ B)/P(B). En una tabla de contingencia, se mira solo la fila o columna de B.",
         "<b>Independientes</b>: P(A ∩ B) = P(A) · P(B). No es lo mismo que incompatibles (P(A ∩ B) = 0).",
         "<b>Probabilidad total</b>: P(B) = Σ P(A<sub>i</sub>) · P(B|A<sub>i</sub>). <b>Bayes</b>: P(A<sub>i</sub>|B) = P(A<sub>i</sub>) · P(B|A<sub>i</sub>)/P(B). Ayúdate de un árbol."]
ex = [("El 60 % compra en tienda (el 10 % devuelve) y el 40 % online (el 25 % devuelve). P(online | devuelve)", ["P(devuelve) = 0,6 · 0,1 + 0,4 · 0,25 = 0,16", "0,4 · 0,25 / 0,16"], "0,625")]
mist = [["Confundir P(A|B) con P(B|A)", "La condición va detrás de la barra."], ["Independientes = incompatibles", "Si son incompatibles (y posibles), no pueden ser independientes."], ["Olvidar una rama", "En la probabilidad total se suman todas las ramas que llegan a B."]]
body = L(think, ex, mist)
faq = [("¿Cuándo se usa el teorema de Bayes?", "Cuando se conoce el resultado y se pregunta por la causa: sabiendo que un cliente devolvió el producto, ¿qué probabilidad hay de que lo comprara online?"),
       ("¿Qué diferencia hay entre sucesos independientes e incompatibles?", "Independientes: saber que ocurre uno no cambia la probabilidad del otro. Incompatibles: no pueden ocurrir a la vez.")]
unit(2, R, "probabilidad", "S", "Probabilidad: sucesos, regla de Laplace, tablas de contingencia, probabilidad condicionada, independencia, probabilidad total y teorema de Bayes",
     "Probabilidad", "Probabilidad", "Fichas de Matemáticas Aplicadas a las Ciencias Sociales II: tablas de contingencia, probabilidad condicionada, independencia, probabilidad total y Bayes. 100 ejercicios.",
     "P(A|B) = P(A ∩ B) / P(B)", "Bayes: de la consecuencia a la causa.", body, faq, sets, 7)
