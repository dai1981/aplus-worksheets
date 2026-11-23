# -*- coding: utf-8 -*-
"""México 4.º grado: Suma y resta de números de hasta cinco cifras (Suma y resta). Reutiliza España 4.º con otra semilla."""
from mx_common import src, unit, mx_text
import es_common as ES

M = "gen_es_matematicas_4_suma_y_resta"
suma, tres, resta, ceros, falta, prueba, probl = src(M, 64203, "s1_suma", "s1_tres", "s2_resta", "s2_ceros", "s3_falta", "s4_prueba", "s5_problema", mx_=99999)

unit("suma-y-resta", 3, "S",
     "Resuelve sumas y restas con números naturales de hasta cinco cifras con el algoritmo convencional; reconoce la resta como operación inversa de la suma y la usa para comprobar; resuelve problemas",
     "Suma y resta", "Suma y resta",
     "Ejercicios de matemáticas de 4.º grado de primaria: sumas y restas en columna con reagrupación, restas con ceros, el término que falta, comprobar y problemas. 100 ejercicios con respuestas.",
     "Coloca unidades bajo unidades", "Comprueba la resta con una suma.",
     ["Escribe los números en columna: <b>unidades bajo unidades</b>, decenas bajo decenas… y empieza por la derecha.",
      "En la suma, si una columna pasa de 9, escribe las unidades y lleva 1 a la columna siguiente.",
      "En la resta, si arriba hay menos, cambia 1 de la columna de la izquierda por 10. Con ceros (40 000 − 1 283), el cambio pasa por varias columnas.",
      "La resta es la operación inversa de la suma: si 52 410 − 18 375 = 34 035, entonces 34 035 + 18 375 = 52 410."],
     [("Calcula 36 458 + 27 386", ["8 + 6 = 14: escribo 4 y llevo 1", "5 + 8 + 1 = 14: escribo 4 y llevo 1", "…"], "63 844"),
      ("Calcula 40 000 − 1 283", ["Cambio 1 decena de millar por 9 UM, 9 C, 9 D y 10 U"], "38 717")],
     [["Olvidar lo que se lleva", "Suma el 1 en la columna siguiente."], ["Restar el menor del mayor en cada columna", "Si arriba hay menos, reagrupa."], ["Alinear mal los números", "Unidades bajo unidades."]],
     [("¿Cómo compruebo una resta?", "Suma el resultado y el número que restaste: debe dar el primer número."),
      ("¿Qué hago si hay ceros en una resta?", "Reagrupa desde la primera cifra distinta de cero de la izquierda: cada 0 por el que pasas se convierte en 9.")],
     [("Sumas en columna", [(suma, 14), (tres, 6)]), ("Restas en columna", [(resta, 20)]), ("Restas con ceros", [(ceros, 20)]), ("El término que falta y comprobar", [(falta, 10), (prueba, 10)]),
      ("Problemas", [(probl, 20)])],
     64003, pic=mx_text(ES.vertical(["36458", "27386"], op="+")), lv=4)
