# -*- coding: utf-8 -*-
"""México 6.º grado: Suma y resta de fracciones con distinto denominador y de números mixtos (Suma y resta). Reutiliza España 6.º con otra semilla."""
import re
from mx_common import src, unit, keep
from es_common import fr


def sin_por(it):
    return not re.search(r"×|÷| : ", re.sub(r"<[^>]*>", " ", it["q"] + it["e"]))


mismo, distinto, probl = src("gen_es_matematicas_6_operaciones_con_fracciones", 66307, "s1_mismo", "s2_distinto", "s5_problema", lv=6, extra=(sin_por,))
suma = keep(distinto, lambda it: " + " in re.sub(r"<[^>]*>", "", it["q"]))
resta = keep(distinto, lambda it: " − " in re.sub(r"<[^>]*>", "", it["q"]))
equiv = src("gen_es_matematicas_6_fracciones", 66309, "s1_equiv", lv=6)

unit("suma-y-resta-de-fracciones", 3, "S",
     "Resuelve sumas y restas de fracciones con distinto denominador usando el mínimo común denominador o fracciones equivalentes; simplifica el resultado y resuelve problemas",
     "Suma y resta de fracciones", "Suma y resta de fracciones",
     "Ejercicios de matemáticas de 6.º grado de primaria: sumar y restar fracciones con distinto denominador, común denominador, simplificar y problemas. 100 ejercicios con respuestas.",
     "Iguala los denominadores", "Después opera los numeradores y simplifica.",
     ["Para sumar o restar fracciones con distinto denominador, conviértelas en <b>equivalentes</b> con un denominador común, de preferencia el menor múltiplo común.",
      "%s + %s: un múltiplo común de 6 y 4 es 12 → %s + %s = %s." % (fr(5, 6), fr(3, 4), fr(10, 12), fr(9, 12), fr(19, 12)),
      "Si el resultado es mayor que 1, se puede escribir como número mixto: %s = 1 %s." % (fr(19, 12), fr(7, 12))],
     [("%s − %s" % (fr(7, 10), fr(1, 4)), ["común denominador 20", "%s − %s" % (fr(14, 20), fr(5, 20))], fr(9, 20))],
     [["Sumar los denominadores", "%s + %s no es %s." % (fr(5, 6), fr(3, 4), fr(8, 10))], ["Multiplicar solo el denominador", "%s = %s." % (fr(3, 4), fr(9, 12))], ["No simplificar", "%s = %s." % (fr(10, 12), fr(5, 6))]],
     [("¿Cuál es el mejor denominador común?", "El menor múltiplo común de los denominadores. Para 6 y 4 es 12, aunque 24 también sirve."),
      ("¿Cómo resto una fracción a un entero?", "Escribe el entero como fracción con el mismo denominador: 2 − 3/5 = 10/5 − 3/5 = 7/5.")],
     [("Fracciones equivalentes", [(equiv, 10), (mismo, 10)]), ("Sumar con distinto denominador", [(suma, 20)]), ("Restar con distinto denominador", [(resta, 20)]), ("Sumas y restas", [(distinto, 20)]), ("Problemas", [(probl, 20)])],
     66003, lv=6)
