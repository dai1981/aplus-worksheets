# -*- coding: utf-8 -*-
"""
España Matemáticas 3.º de Primaria: Patrones e igualdades (Sentido algebraico)
Series de números y figuras, la regla de una serie, igualdades con hueco, verdadero o falso.
Reutiliza los generadores de 4.º (mismo ciclo) con números hasta 9999.
"""
from es_low import unit, src

SEED = 33910
series, regla, figuras, hueco, verdad, tabla = src("patrones_e_igualdades", SEED, "s1_series", "s1_regla", "s2_figuras", "s3_hueco", "s3_verdad", "s4_tabla")

unit(3, "patrones-e-igualdades", 10, "A", "Patrones numéricos y geométricos; relaciones de igualdad; el signo igual como equivalencia",
     "Patrones e igualdades", "Patrones",
     "Fichas de matemáticas de 3.º de Primaria: series de números y figuras, la regla de una serie e igualdades con hueco. 100 ejercicios con soluciones.",
     "= significa «vale lo mismo»", "Busca la regla y compruébala con todos.",
     ["En una <b>serie</b> cada número sale del anterior con la misma <b>regla</b>.", "El signo <b>=</b> significa que los dos lados valen lo mismo, como una balanza en equilibrio.",
      "Para completar una igualdad con hueco, calcula primero el lado completo."],
     [("Serie: 5, 9, 13, 17, …", ["La regla es sumar 4", "17 + 4"], "21"), ("12 + 8 = 25 − ___", ["12 + 8 = 20", "25 − 5 = 20"], "5")],
     [["Pensar que = es «escribe el resultado»", "En 9 + 6 = ___ + 5, el hueco no es 15: es 10."], ["Mirar solo dos números", "Comprueba la regla con todos."], ["Equivocarse en el grupo que se repite", "Marca dónde empieza y termina cada grupo."]],
     [("¿Qué significa el signo igual?", "Que lo que hay a un lado vale lo mismo que lo que hay al otro. Por eso 8 + 7 = 10 + 5 es verdadera."),
      ("¿Cómo se encuentra la regla de una serie?", "Se mira cuánto cambia cada número respecto al anterior.")],
     [("Series de números", [(series, 14), (regla, 6)]), ("Patrones con figuras", [(figuras, 20)]), ("La regla de la serie", [(regla, 14), (tabla, 6)]),
      ("Igualdades con hueco", [(hueco, 20)]), ("¿Verdadero o falso?", [(verdad, 14), (tabla, 6)])], 33010)
