# -*- coding: utf-8 -*-
"""México, Pensamiento Matemático I (progresión 5): probabilidad condicional, eventos independientes y mutuamente excluyentes, teorema de Bayes."""
import random
import mx_pm1 as S
from mx_common import src, unit

S.setup(random.Random(100105))
ind, cond, bay = src("gen_es_matematicas_2bach_probabilidad", 100305, "s_independencia", "s_condicionada", "s_bayes")
cont = src("gen_es_matematicas_1ccss_probabilidad", 100315, "s_contingencia")
unit("probabilidad-condicional-y-teorema-de-bayes", 5, ("Probabilidad", 5, "Probabilidad condicional y teorema de Bayes"),
     "Calcula probabilidades condicionales, distingue eventos mutuamente excluyentes e independientes y usa el teorema de Bayes para actualizar una probabilidad con nueva información",
     "Probabilidad condicional y teorema de Bayes", "Probabilidad condicional",
     "Ejercicios de Pensamiento Matemático I: probabilidad condicional con tablas, eventos independientes, mutuamente excluyentes, probabilidad total y teorema de Bayes. 100 ejercicios con respuestas.",
     "P(A | B) = P(A ∩ B) ÷ P(B)", "La nueva información cambia la probabilidad.",
     ["<b>Probabilidad condicional</b>: P(A | B) = P(A ∩ B) ÷ P(B). En una tabla: casos de A dentro de la fila o columna de B ÷ total de B.",
      "A y B son <b>independientes</b> si P(A ∩ B) = P(A) × P(B). Son <b>mutuamente excluyentes</b> si no pueden ocurrir juntos.",
      "<b>Teorema de Bayes</b>: P(A | B) = P(A) × P(B | A) ÷ P(B), donde P(B) se obtiene con la probabilidad total."],
     [("40 % usa camión y de ellos llega tarde el 10 %; 60 % va en carro y llega tarde el 5 %.", ["P(tarde) = 0.04 + 0.03 = 0.07", "P(camión | tarde) = 0.04 ÷ 0.07"], "≈ 0.571")],
     [["Dividir entre el total y no entre P(B)", "Lo condicional se mide dentro de B."], ["Confundir independientes con excluyentes", "Excluyentes no pueden ocurrir juntos; independientes no se afectan."], ["Olvidar sumar todas las ramas", "P(B) suma todas las formas de que ocurra B."]],
     [("¿Para qué sirve el teorema de Bayes?", "Para invertir una condicional: saber la probabilidad de la causa conociendo el efecto (por ejemplo, de estar enfermo si la prueba salió positiva)."),
      ("¿Dos eventos excluyentes pueden ser independientes?", "No, si los dos tienen probabilidad mayor que 0: si ocurre uno, el otro ya no puede ocurrir.")],
     [("Condicional con tablas", [(cont, 10), (cond, 10)]), ("Probabilidad condicional", [(cond, 20)]), ("Independientes y excluyentes", [(ind, 20)]),
      ("Teorema de Bayes", [(bay, 20)]), ("Repaso", [(bay, 8), (cont, 6), (ind, 6)])],
     100005, lv=10)
