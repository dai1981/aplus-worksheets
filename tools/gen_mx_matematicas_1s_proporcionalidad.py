# -*- coding: utf-8 -*-
"""México 1.er grado de secundaria (Fase 6): Relaciones proporcionales y no proporcionales en tablas, gráficas y expresiones."""
import random
import mx_s1 as S
from mx_common import src, unit, nomoney, noplanta  # noqa: F401

S.setup(random.Random(67111))
raz, reg = src("gen_es_matematicas_1eso_proporcionalidad_y_porcentajes", 67411, "s_razon", "s_regla", lv=1, extra=(nomoney,))
tipo, tab = src("gen_es_matematicas_2eso_proporcionalidad", 67412, "s_tipo", "s_tabla", lv=2, extra=(lambda it: "inversa" not in it["q"] + " ".join(it["c"]) and "grifo" not in it["q"] and "llaves" not in it["q"],))
rec, fun = src("gen_es_matematicas_1eso_coordenadas_y_graficas", 67413, "s_recta", "s_funcion", lv=1)

unit("proporcionalidad", 11, "6FU",
     "Relaciona e interpreta relaciones proporcionales y no proporcionales a partir de su representación tabular, gráfica y algebraica",
     "Relaciones proporcionales y no proporcionales", "Proporcionalidad",
     "Ejercicios de matemáticas de 1.er grado de secundaria: distinguir relaciones proporcionales y no proporcionales en tablas, gráficas y expresiones; constante de proporcionalidad y valor faltante. 100 ejercicios con respuestas.",
     "Proporcional: y = kx", "Su gráfica es una recta que pasa por (0, 0).",
     ["Dos cantidades son <b>directamente proporcionales</b> si el cociente y ÷ x es siempre el mismo número k (la <b>constante de proporcionalidad</b>): y = kx.",
      "En una <b>tabla</b>, divide cada y entre su x: si siempre da lo mismo, es proporcional. En una <b>gráfica</b>, es una recta que pasa por el origen.",
      "Si hay una cantidad fija (como el banderazo de un taxi), la relación es <b>no proporcional</b>: y = kx + b, con b ≠ 0."],
     [("3 kg → $72, 5 kg → $120", ["72 ÷ 3 = 24", "120 ÷ 5 = 24"], "proporcional, k = 24"), ("Taxi: $15 + $8 por km", ["y = 8x + 15"], "no proporcional")],
     [["Creer que «si los dos aumentan» es proporcional", "Tiene que aumentar en la misma razón."], ["Olvidar comprobar el origen", "Una recta que no pasa por (0, 0) no es proporcional."], ["Sumar en vez de multiplicar", "Si 2 → 30, entonces 6 → 90, no 34."]],
     [("¿Toda recta es proporcional?", "No. Solo las que pasan por el origen (0, 0)."), ("¿Qué es la constante de proporcionalidad?", "El número por el que se multiplica x para obtener y; también es el valor unitario.")],
     [("¿Es proporcional? (tablas)", [(S.fu_table, 20)]), ("Gráficas", [(S.fu_graph, 4), (rec, 16)]), ("Constante y valor faltante", [(raz, 10), (tab, 10)]),
      ("Expresiones algebraicas", [(fun, 10), (S.fu_table, 10)]), ("Problemas", [(reg, 12), (S.fu_table, 8)])],
     67011, lv=7)
