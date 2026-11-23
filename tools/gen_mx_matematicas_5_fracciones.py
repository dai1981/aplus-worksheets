# -*- coding: utf-8 -*-
"""México 5.º grado: Fracciones: equivalentes, comparar y ordenar, números mixtos, fracción de una cantidad (Estudio de los números). Reutiliza España 6.º (nivel 5.º) con otra semilla."""
from mx_common import src, unit
from es_common import fr

equiv, comp, mixtos, cant, probl = src("gen_es_matematicas_6_fracciones", 65306, "s1_equiv", "s2_comparar", "s3_mixtos", "s4_cantidad", "s5_problema", lv=5)

unit("fracciones", 5, "N",
     "Compara, ordena y encuentra fracciones equivalentes; expresa fracciones impropias como números mixtos y al revés; calcula la fracción de una cantidad y resuelve problemas",
     "Fracciones equivalentes, mixtas y de una cantidad", "Fracciones",
     "Ejercicios de matemáticas de 5.º grado de primaria: fracciones equivalentes, comparar y ordenar fracciones, números mixtos, fracción de una cantidad y problemas. 100 ejercicios con respuestas.",
     "Mismo denominador para comparar", "Numerador mayor que denominador: más de 1.",
     ["Para comparar fracciones con distinto denominador, conviértelas en <b>equivalentes</b> con el mismo denominador: %s y %s → %s y %s, así que %s &lt; %s." % (fr(2, 3), fr(3, 4), fr(8, 12), fr(9, 12), fr(2, 3), fr(3, 4)),
      "Si el numerador es mayor que el denominador, la fracción es mayor que 1 y se puede escribir como <b>número mixto</b>: %s = 2 %s." % (fr(11, 4), fr(3, 4)),
      "Para calcular %s de 40: 40 ÷ 5 = 8 y 8 × 3 = 24." % fr(3, 5)],
     [("Escribe %s como número mixto" % fr(17, 5), ["17 ÷ 5 = 3 y sobran 2"], "3 %s" % fr(2, 5)), ("Compara %s y %s" % (fr(5, 6), fr(7, 9)), ["%s y %s" % (fr(15, 18), fr(14, 18))], "%s &gt; %s" % (fr(5, 6), fr(7, 9)))],
     [["Comparar solo los numeradores", "Primero iguala los denominadores."], ["Escribir %s como 2 %s" % (fr(11, 4), fr(1, 4)), "11 ÷ 4 = 2 y sobran 3: 2 %s." % fr(3, 4)], ["Dividir entre el numerador", "%s de 40: divide entre 5." % fr(3, 5)]],
     [("¿Qué es un número mixto?", "Un número con una parte entera y una fracción, como 2 3/4: son 2 enteros y 3/4 más."),
      ("¿Cómo comparo fracciones con distinto denominador?", "Busca fracciones equivalentes con el mismo denominador y compara los numeradores.")],
     [("Fracciones equivalentes", [(equiv, 20)]), ("Comparar y ordenar", [(comp, 20)]), ("Números mixtos", [(mixtos, 20)]), ("Fracción de una cantidad", [(cant, 20)]), ("Problemas", [(probl, 20)])],
     65005, lv=5)
