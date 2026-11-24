# -*- coding: utf-8 -*-
"""México 1.er grado: Sumas y restas hasta 20 con dibujos, recta y cálculo mental (Construcción de la noción de suma y resta). Reutiliza España 1.º (gen_es_matematicas_3_suma_y_resta, nivel 1) con otra semilla."""
from mx_common import src, unit
from mx_12 import BIG

dib, calc, falta, term, probl = src("gen_es_matematicas_3_suma_y_resta", 61401, "s1_dibujos", "s2_calcular", "s3_falta", "s4_terminos", "s5_problema", lv=1, mx_=BIG)

unit("sumas-y-restas-hasta-20", 4, "S3",
     "Reconoce que la suma permite obtener el total de dos o más cantidades y la resta representa quitar elementos; representa las operaciones con material, dibujos y los signos +, − e =; calcula mentalmente con números de una cifra",
     "Sumas y restas hasta 20", "Sumas y restas hasta 20",
     "Ejercicios de matemáticas de 1.er grado de primaria: sumar y restar hasta 20 con dibujos, el número que falta y problemas sencillos. 100 ejercicios con respuestas.",
     "Sumar es juntar; restar es quitar", "Usa los dedos, dibujos o la recta.",
     ["<b>Sumar</b> es juntar: 5 manzanas y 3 manzanas son 5 + 3 = 8 manzanas.",
      "<b>Restar</b> es quitar: si tienes 9 globos y se van 4, te quedan 9 − 4 = 5.",
      "Para sumar 8 + 5, completa primero el 10: 8 + 2 = 10 y luego 10 + 3 = 13."],
     [("7 + 6", ["7 + 3 = 10", "10 + 3"], "13"), ("15 − 7", ["15 − 5 = 10", "10 − 2"], "8")],
     [["Contar dos veces el primer número", "En 7 + 6 empieza en 7 y cuenta 6 más: 8, 9, 10, 11, 12, 13."], ["Sumar cuando hay que quitar", "«Se van», «regala», «se come» es restar."], ["Restar al revés", "9 − 4, no 4 − 9."]],
     [("¿Cómo sumo con los dedos más de 10?", "Empieza con el número mayor en la cabeza y cuenta con los dedos el otro: para 9 + 4, di 9 y cuenta 10, 11, 12, 13."),
      ("¿Para qué sirve el signo =?", "Indica que los dos lados valen lo mismo: 4 + 3 = 7.")],
     [("Con dibujos", [(dib, 20)]), ("Sumar y restar", [(calc, 20)]), ("El número que falta", [(falta, 20)]), ("Sumandos y signos", [(term, 8), (calc, 12)]), ("Problemas", [(probl, 20)])],
     61004, lv=1)
