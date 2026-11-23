# -*- coding: utf-8 -*-
"""México 5.º grado: Suma y resta de fracciones con distinto denominador (Suma y resta). Reutiliza España 6.º (nivel 5.º) con otra semilla."""
import re
from mx_common import src, unit, keep
from es_common import fr


def sin_por(it):
    return not re.search(r"×|÷| : ", re.sub(r"<[^>]*>", " ", it["q"] + it["e"]))


mismo, distinto, probl = src("gen_es_matematicas_6_operaciones_con_fracciones", 65307, "s1_mismo", "s2_distinto", "s5_problema", lv=5, extra=(sin_por,))
suma = keep(distinto, lambda it: " + " in re.sub(r"<[^>]*>", "", it["q"]))
resta = keep(distinto, lambda it: " − " in re.sub(r"<[^>]*>", "", it["q"]))

unit("suma-y-resta-de-fracciones", 6, "S",
     "Resuelve sumas y restas de fracciones con distinto denominador buscando fracciones equivalentes con un denominador común; calcula mentalmente sumas y restas sencillas; resuelve problemas",
     "Suma y resta de fracciones", "Suma y resta de fracciones",
     "Ejercicios de matemáticas de 5.º grado de primaria: sumar y restar fracciones con igual y distinto denominador, común denominador, simplificar y problemas. 100 ejercicios con respuestas.",
     "Primero, un denominador común", "Después suma o resta los numeradores.",
     ["Con el mismo denominador, se suman o restan los numeradores: %s + %s = %s." % (fr(3, 8), fr(2, 8), fr(5, 8)),
      "Con distinto denominador, busca un <b>denominador común</b> (un múltiplo de los dos) y convierte las fracciones: %s + %s = %s + %s = %s." % (fr(2, 3), fr(1, 4), fr(8, 12), fr(3, 12), fr(11, 12)),
      "Al final, simplifica si se puede."],
     [("%s − %s" % (fr(5, 6), fr(1, 4)), ["denominador común 12", "%s − %s" % (fr(10, 12), fr(3, 12))], fr(7, 12))],
     [["Sumar numeradores y denominadores", "%s + %s no es %s." % (fr(2, 3), fr(1, 4), fr(3, 7))], ["Cambiar el denominador sin cambiar el numerador", "%s = %s, no %s." % (fr(2, 3), fr(8, 12), fr(2, 12))], ["No simplificar", "%s = %s." % (fr(6, 8), fr(3, 4))]],
     [("¿Cómo encuentro un denominador común?", "Busca un múltiplo de los dos denominadores. Para 3 y 4, sirve 12, porque 3 × 4 = 12."),
      ("¿Hay que simplificar el resultado?", "Es lo mejor: 6/8 y 3/4 son iguales, pero 3/4 es más sencillo.")],
     [("Mismo denominador", [(mismo, 20)]), ("Sumar con distinto denominador", [(suma, 20)]), ("Restar con distinto denominador", [(resta, 20)]), ("Sumas y restas", [(distinto, 20)]), ("Problemas", [(probl, 20)])],
     65006, lv=5)
