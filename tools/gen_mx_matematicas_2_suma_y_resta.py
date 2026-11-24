# -*- coding: utf-8 -*-
"""México 2.º grado: Suma y resta con agrupamientos y el algoritmo convencional (números de dos cifras), la recta numérica (Construcción de la noción de suma y resta). Reutiliza España 2.º con otra semilla."""
from mx_common import src, unit, mx_text
from mx_12 import BIG, q_le
import es_common as ES

calc, falta, term, probl = src("gen_es_matematicas_3_suma_y_resta", 62401, "s2_calcular", "s3_falta", "s4_terminos", "s5_problema", lv=2, mx_=BIG, extra=(q_le(99),))
comp, nueve = src("gen_es_matematicas_2_calculo_mental", 62402, "s_completar", "s_nueve", lv=1, mx_=BIG)

unit("suma-y-resta", 4, "S3",
     "Resuelve sumas y restas con números de hasta dos cifras usando agrupamientos y el algoritmo convencional; representa sumas como avanzar y restas como retroceder en la recta numérica",
     "Suma y resta en columna", "Suma y resta",
     "Ejercicios de matemáticas de 2.º grado de primaria: sumas y restas de dos cifras en columna con y sin reagrupar, el número que falta y problemas. 100 ejercicios con respuestas.",
     "Unidades bajo unidades", "Si juntas 10 unidades, forma una decena.",
     ["Escribe los números en columna: <b>unidades bajo unidades</b> y decenas bajo decenas. Empieza por las unidades.",
      "Si las unidades suman 10 o más, forma una decena y pásala a la columna de las decenas: 38 + 25 → 8 + 5 = 13, escribe 3 y pasa 1.",
      "Para restar, si arriba hay menos unidades, cambia una decena por 10 unidades: 52 − 17 → 12 − 7 = 5 y 4 − 1 = 3."],
     [("38 + 25", ["8 + 5 = 13: escribo 3, paso 1", "3 + 2 + 1 = 6"], "63"), ("52 − 17", ["12 − 7 = 5", "4 − 1 = 3"], "35")],
     [["Olvidar la decena que se pasa", "38 + 25 = 63, no 53."], ["Restar el número pequeño del grande en cada columna", "52 − 17 no es 45: cambia una decena."], ["Alinear mal", "Unidades bajo unidades."]],
     [("¿Qué es reagrupar?", "Formar una decena con 10 unidades al sumar, o cambiar una decena por 10 unidades al restar."),
      ("¿Cómo uso la recta para sumar?", "Empieza en el primer número y avanza tantos lugares como el segundo. Para restar, retrocede.")],
     [("Sumar y restar en columna", [(calc, 20)]), ("El número que falta", [(falta, 20)]), ("Sumandos, resta y comprobación", [(term, 20)]), ("Sumar sin reagrupar y sumar 9", [(comp, 10), (nueve, 10)]), ("Problemas", [(probl, 20)])],
     62004, pic=mx_text(ES.vertical(["38", "25"], op="+")), lv=2)
