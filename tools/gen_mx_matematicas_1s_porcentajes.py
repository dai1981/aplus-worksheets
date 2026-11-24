# -*- coding: utf-8 -*-
"""México 1.er grado de secundaria (Fase 6): Problemas de porcentajes: descuentos, aumentos, IVA y propinas."""
import random
import mx_s1 as S
from mx_common import src, unit, nomoney, noplanta  # noqa: F401

S.setup(random.Random(67110))
porc, desc = src("gen_es_matematicas_1eso_proporcionalidad_y_porcentajes", 67401, "s_porc", "s_desc", lv=1, extra=(nomoney,))
bas, var = src("gen_es_matematicas_2eso_porcentajes", 67402, "s_basico", "s_variacion", lv=2, extra=(nomoney,))

unit("porcentajes", 10, "6EC",
     "Resuelve problemas de porcentajes en diversas situaciones: porcentaje de una cantidad, el total a partir de una parte, descuentos, aumentos e IVA",
     "Porcentajes: descuentos, aumentos e IVA", "Porcentajes",
     "Ejercicios de matemáticas de 1.er grado de secundaria: porcentaje de una cantidad, qué porcentaje es, el total a partir de una parte, descuentos, aumentos, IVA y propinas. 100 ejercicios con respuestas.",
     "25 % de 80 = 80 × 0.25 = 20", "Con descuento pagas el resto: 100 % − d.",
     ["El <b>porcentaje</b> es una fracción de 100: 25 % = 25/100 = 0.25. Para calcular el 25 % de 80, multiplica 80 × 0.25 = 20.",
      "Con un <b>descuento</b> del 20 % pagas el 80 %: precio × 0.80. Con un <b>aumento</b> o el <b>IVA</b> (16 %) pagas el 116 %: precio × 1.16.",
      "Para saber <b>qué porcentaje</b> es una parte, divide parte ÷ total y multiplica por 100."],
     [("30 % de $450", ["450 × 0.30"], "$135"), ("$1 200 con 15 % de descuento", ["1 200 × 0.85"], "$1 020"), ("18 de 24 alumnos", ["18 ÷ 24 = 0.75"], "75 %")],
     [["Restar el número del porcentaje", "$500 con 20 % de descuento no es $480: es $400."], ["Aplicar dos descuentos sumándolos", "20 % y luego 10 % no es 30 %: es 28 %."], ["Calcular sobre el total equivocado", "El porcentaje de cambio se calcula sobre el precio original."]],
     [("¿Cómo calculo el IVA en México?", "El IVA general es del 16 %: multiplica el precio sin IVA por 1.16 para obtener el total."), ("¿Qué es el 100 %?", "La cantidad completa. El 50 % es la mitad; el 200 %, el doble.")],
     [("Porcentaje de una cantidad", [(porc, 12), (bas, 8)]), ("Descuentos", [(S.pc_problem, 10), (desc, 10)]), ("Aumentos e IVA", [(S.pc_problem, 12), (var, 8)]),
      ("¿Qué porcentaje es?", [(bas, 10), (S.pc_problem, 10)]), ("Problemas", [(S.pc_problem, 20)])],
     67010, lv=7)
