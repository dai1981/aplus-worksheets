# -*- coding: utf-8 -*-
"""México 3.er grado: Sucesiones y patrones (sucesiones numéricas y de figuras, la regla, igualdades). Reutiliza España 4.º con otra semilla."""
from mx_common import src, unit

series, regla, figuras, hueco, verdad, tabla = src("gen_es_matematicas_4_patrones_e_igualdades", 63217, "s1_series", "s1_regla", "s2_figuras", "s3_hueco", "s3_verdad", "s4_tabla")

unit("sucesiones-y-patrones", 18, "N",
     "Identifica la regularidad de sucesiones numéricas ascendentes y descendentes y de sucesiones de figuras; encuentra términos faltantes y reconoce igualdades",
     "Sucesiones y patrones", "Sucesiones",
     "Ejercicios de matemáticas de 3.er grado de primaria: sucesiones de números y de figuras, la regla de una sucesión e igualdades con hueco. 100 ejercicios con respuestas.",
     "Busca la regla y compruébala", "= significa «vale lo mismo».",
     ["En una <b>sucesión</b>, cada número sale del anterior con la misma <b>regla</b>: 5, 9, 13, 17… (suma 4).",
      "El signo <b>=</b> significa que los dos lados valen lo mismo, como una balanza en equilibrio.",
      "Para completar una igualdad con hueco, calcula primero el lado completo."],
     [("Sucesión: 5, 9, 13, 17, …", ["La regla es sumar 4", "17 + 4"], "21"), ("12 + 8 = 25 − ___", ["12 + 8 = 20", "25 − 5 = 20"], "5")],
     [["Pensar que = es «escribe el resultado»", "En 9 + 6 = ___ + 5, el hueco no es 15: es 10."], ["Mirar solo dos números", "Comprueba la regla con todos."], ["Equivocarse en el grupo que se repite", "Marca dónde empieza y termina cada grupo."]],
     [("¿Qué significa el signo igual?", "Que lo que hay de un lado vale lo mismo que lo que hay del otro. Por eso 8 + 7 = 10 + 5 es verdadera."),
      ("¿Cómo encuentro la regla de una sucesión?", "Mira cuánto cambia cada número respecto al anterior y comprueba que pasa lo mismo en toda la sucesión.")],
     [("Sucesiones de números", [(series, 14), (regla, 6)]), ("Sucesiones de figuras", [(figuras, 20)]), ("La regla de la sucesión", [(regla, 14), (tabla, 6)]),
      ("Igualdades con hueco", [(hueco, 20)]), ("¿Verdadero o falso?", [(verdad, 14), (tabla, 6)])], 63018)
