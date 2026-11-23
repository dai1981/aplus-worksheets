# -*- coding: utf-8 -*-
"""México 3.er grado: Cálculo mental (Suma y resta). Reutiliza España 3.º/4.º con otra semilla."""
from mx_common import src, unit

redondos, doble = src("gen_es_matematicas_3_calculo_mental", 63104, "s_redondos", "s_doble")
casi, descomp, estimar, probl = src("gen_es_matematicas_4_calculo_mental_y_estimacion", 63204, "s1_casi", "s2_descomponer", "s3_estimar", "s5_problema")

unit("calculo-mental", 4, "S",
     "Calcula mentalmente sumas y restas con decenas, centenas y unidades de millar, dobles y mitades; estima resultados redondeando",
     "Cálculo mental", "Cálculo mental",
     "Ejercicios de matemáticas de 3.er grado de primaria: sumar y restar decenas y centenas de memoria, dobles y mitades, sumar 9 y 99, estimar. 100 ejercicios con respuestas.",
     "Busca números redondos", "Suma 10 y quita 1 es sumar 9.",
     ["Al sumar centenas, solo cambia la cifra de las centenas: 3 425 + 300 = 3 725.",
      "Para sumar 9, suma 10 y quita 1. Para sumar 99, suma 100 y quita 1.",
      "Para <b>estimar</b>, redondea los números y calcula con los redondeados: 398 + 205 ≈ 400 + 200 = 600."],
     [("Calcula 456 + 99", ["456 + 100 = 556", "556 − 1"], "555"), ("Doble de 35", ["30 + 30 = 60", "5 + 5 = 10", "60 + 10"], "70")],
     [["Cambiar la cifra equivocada", "Al sumar 300, cambia las centenas, no las decenas."], ["Olvidar quitar 1", "456 + 99 = 456 + 100 − 1."], ["Estimar sin redondear", "Redondea primero y luego calcula."]],
     [("¿Para qué sirve el cálculo mental?", "Para calcular rápido sin lápiz y para comprobar si un resultado tiene sentido."),
      ("¿Qué es estimar?", "Calcular un resultado aproximado con números redondos.")],
     [("Decenas, centenas y millares", [(redondos, 20)]), ("Sumar 9, 99 y números cercanos", [(casi, 20)]), ("Dobles, mitades y descomponer", [(doble, 10), (descomp, 10)]),
      ("Estimar", [(estimar, 20)]), ("Problemas", [(probl, 20)])], 63004)
