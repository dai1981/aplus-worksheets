# -*- coding: utf-8 -*-
"""México 6.º grado: Fracciones y decimales: equivalencias, comparar y ordenar, ubicar en la recta, redondear (Estudio de los números). Reutiliza España 6.º con otra semilla."""
from mx_common import src, unit
from es_common import fr

frac, comp, red, vida = src("gen_es_matematicas_6_numeros_decimales", 66308, "s1_fraccion", "s3_comparar", "s4_redondear", "s5_vida", lv=6)
equiv, compf, mixtos = src("gen_es_matematicas_6_fracciones", 66306, "s1_equiv", "s2_comparar", "s3_mixtos", lv=6)

unit("fracciones-y-decimales", 2, "N",
     "Convierte fracciones en decimales y decimales en fracciones; compara y ordena fracciones y decimales; usa fracciones equivalentes y números mixtos; redondea decimales",
     "Fracciones y decimales", "Fracciones y decimales",
     "Ejercicios de matemáticas de 6.º grado de primaria: pasar fracciones a decimales y decimales a fracciones, comparar y ordenar, números mixtos y redondear. 100 ejercicios con respuestas.",
     "Fracción = numerador ÷ denominador", "3/8 = 3 ÷ 8 = 0.375.",
     ["Una fracción es una división: %s = 3 ÷ 8 = 0.375. Si el denominador es 10, 100 o 1 000, el decimal se escribe directo: %s = 0.07." % (fr(3, 8), fr(7, 100)),
      "Un decimal se convierte en fracción decimal y luego se simplifica: 0.45 = %s = %s." % (fr(45, 100), fr(9, 20)),
      "Para comparar una fracción y un decimal, escríbelos en la misma forma: %s = 0.75 &gt; 0.7." % fr(3, 4)],
     [("Escribe 0.6 como fracción", ["%s" % fr(6, 10), "simplifica entre 2"], fr(3, 5)), ("¿Qué es mayor, %s o 0.4?" % fr(3, 8), ["%s = 0.375" % fr(3, 8)], "0.4")],
     [["Escribir %s como 3.8" % fr(3, 8), "Es 3 ÷ 8 = 0.375."], ["Leer 0.45 como %s" % fr(45, 10), "Dos cifras decimales: centésimos."], ["Comparar decimales por su número de cifras", "0.4 &gt; 0.375."]],
     [("¿Cómo convierto una fracción en decimal?", "Divide el numerador entre el denominador: 1/8 = 1 ÷ 8 = 0.125."),
      ("¿Cómo convierto 0.25 en fracción?", "0.25 son 25 centésimos: 25/100, que simplificado es 1/4.")],
     [("Fracciones y decimales", [(frac, 20)]), ("Fracciones equivalentes y números mixtos", [(equiv, 10), (mixtos, 10)]), ("Comparar fracciones", [(compf, 20)]), ("Comparar y redondear decimales", [(comp, 10), (red, 10)]),
      ("Decimales en la vida diaria", [(vida, 20)])],
     66002, lv=6)
