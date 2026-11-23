# -*- coding: utf-8 -*-
"""México 3.er grado: Comparar y ordenar números hasta 9 999 (Estudio de los números). Reutiliza España 3.º con otra semilla."""
from mx_common import src, unit

M = "gen_es_matematicas_3_comparar_y_ordenar"
dib, signo, ordenar, entre, probl = src(M, 63102, "s1_dibujos", "s2_signo", "s3_ordenar", "s4_entre", "s5_problema", lv=3)

unit("comparar-y-ordenar-numeros", 2, "N",
     "Compara y ordena números de hasta cuatro cifras con los signos <, > e =; los ubica en la recta numérica; redondea a la decena, centena o unidad de millar",
     "Comparar y ordenar números", "Comparar y ordenar",
     "Ejercicios de matemáticas de 3.er grado de primaria: mayor que, menor que e igual, signos < y >, ordenar números, recta numérica y redondeo. 100 ejercicios con respuestas.",
     "El signo mira al número mayor", "Compara de izquierda a derecha.",
     ["Para comparar, mira primero cuántas cifras tiene cada número. Si tienen las mismas, compara de izquierda a derecha.",
      "<b>&gt;</b> significa «mayor que» y <b>&lt;</b>, «menor que». La parte abierta del signo mira al número mayor: 4 521 &gt; 4 512.",
      "Para <b>redondear</b>, mira la cifra siguiente: si es 5 o más, hacia arriba; si es menor que 5, hacia abajo."],
     [("Compara 4 521 y 4 512", ["Miramos la primera cifra distinta: 2 &gt; 1"], "4 521 &gt; 4 512"), ("Ordena de menor a mayor 3 060, 3 600, 3 006", ["Comparamos de izquierda a derecha"], "3 006 &lt; 3 060 &lt; 3 600")],
     [["Mirar solo la última cifra", "En 39 y 41, manda la primera cifra: 39 &lt; 41."], ["Confundir &lt; y &gt;", "La parte abierta del signo mira al número mayor."], ["Redondear el 5 hacia abajo", "Con 5, hacia arriba: 4 350 → 4 400."]],
     [("¿Cómo se comparan dos números?", "Si tienen distinto número de cifras, es mayor el que tiene más. Si tienen las mismas, se comparan las cifras de izquierda a derecha hasta encontrar una distinta."),
      ("¿Qué significan los signos < y >?", "< significa «es menor que» y > significa «es mayor que». La abertura apunta al número mayor.")],
     [("Más, menos o igual", [(dib, 20)]), ("Mayor que, menor que o igual", [(signo, 20)]), ("Ordenar números", [(ordenar, 20)]),
      ("Entre, la recta y el redondeo", [(entre, 20)]), ("Problemas", [(probl, 20)])], 63002)
