# -*- coding: utf-8 -*-
"""México 5.º grado: Números decimales hasta milésimos; fracciones y decimales (Estudio de los números). Reutiliza España 6.º (nivel 5.º) con otra semilla."""
from mx_common import src, unit, mx_text
import es_common as ES

frac, leer, comp, red, vida = src("gen_es_matematicas_6_numeros_decimales", 65308, "s1_fraccion", "s2_leer", "s3_comparar", "s4_redondear", "s5_vida", lv=5)

unit("numeros-decimales", 3, "N",
     "Lee, escribe, compara y ordena números decimales hasta milésimos; expresa fracciones como 1/2, 1/4, 3/4, 1/5 y 1/8 en forma decimal; redondea decimales",
     "Números decimales hasta milésimos", "Números decimales",
     "Ejercicios de matemáticas de 5.º grado de primaria: décimos, centésimos y milésimos, fracciones y decimales, comparar, ordenar y redondear decimales. 100 ejercicios con respuestas.",
     "Décimos, centésimos, milésimos", "1/2 = 0.5; 1/4 = 0.25; 1/8 = 0.125.",
     ["Después del punto decimal vienen los <b>décimos</b>, los <b>centésimos</b> y los <b>milésimos</b>: en 3.475, el 4 vale 4 décimos, el 7 vale 7 centésimos y el 5, 5 milésimos.",
      "Algunas fracciones tienen un decimal fácil: %s = 0.5, %s = 0.25, %s = 0.75, %s = 0.2 y %s = 0.125." % (ES.fr(1, 2), ES.fr(1, 4), ES.fr(3, 4), ES.fr(1, 5), ES.fr(1, 8)),
      "Para comparar, iguala el número de cifras decimales con ceros: 0.6 = 0.600 &gt; 0.587."],
     [("Escribe %s como decimal" % ES.fr(3, 4), ["%s = %s" % (ES.fr(3, 4), ES.fr(75, 100))], "0.75"), ("Redondea 4.268 a los centésimos", ["el milésimo es 8 ≥ 5"], "4.27")],
     [["Pensar que 0.125 &gt; 0.5 porque 125 &gt; 5", "Compara 0.500 y 0.125."], ["Escribir %s como 1.4" % ES.fr(1, 4), "%s = 0.25." % ES.fr(1, 4)], ["Redondear mirando la cifra equivocada", "A los centésimos, mira los milésimos."]],
     [("¿Qué es un milésimo?", "Una de las 1 000 partes iguales de una unidad: 0.001. Un metro tiene 1 000 milímetros, y cada milímetro es un milésimo de metro."),
      ("¿Cómo paso una fracción a decimal?", "Busca una fracción equivalente con denominador 10, 100 o 1 000: 1/4 = 25/100 = 0.25. También puedes dividir el numerador entre el denominador.")],
     [("Fracciones y decimales", [(frac, 20)]), ("Leer y escribir decimales", [(leer, 20)]), ("Comparar y ordenar", [(comp, 20)]), ("Redondear decimales", [(red, 20)]), ("Decimales en la vida diaria", [(vida, 20)])],
     65003, lv=5)
