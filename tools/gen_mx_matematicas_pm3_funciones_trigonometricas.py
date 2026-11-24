# -*- coding: utf-8 -*-
"""México, Pensamiento Matemático III (progresión 13): funciones trigonométricas y fenómenos periódicos."""
import random
import mx_pm3 as S
from mx_common import src, unit

S.setup(random.Random(120113))
rad, fun = src("gen_es_matematicas_1bach_trigonometria", 120313, "s_radianes", "s_funciones")
unit("funciones-trigonometricas", 13, ("Funciones trascendentes", 13, "Funciones trigonométricas"),
     "Modela fenómenos periódicos con las funciones seno y coseno e identifica amplitud, periodo, valores máximo y mínimo y desplazamiento vertical",
     "Seno, coseno y fenómenos periódicos", "Funciones trigonométricas",
     "Ejercicios de Pensamiento Matemático III: radianes, valores de seno y coseno, amplitud, periodo, máximo y mínimo de y = A sen(Bx) + D y fenómenos periódicos. 100 ejercicios con respuestas.",
     "y = A sen(Bx) + D", "Amplitud A, periodo 2π ÷ B.",
     ["Las funciones <b>seno</b> y <b>coseno</b> se repiten cada 2π radianes (360°) y valen entre −1 y 1. π rad = 180°.",
      "En y = A sen(Bx) + D: la <b>amplitud</b> es |A|, el <b>periodo</b> es 2π ÷ B y D sube o baja la gráfica.",
      "El valor máximo es D + |A| y el mínimo D − |A|. Sirven para mareas, ruedas de la fortuna, sonido y estaciones."],
     [("y = 3 sen(2x) + 1", ["Amplitud 3", "Periodo 2π ÷ 2 = π", "Máximo 4, mínimo −2"], "")],
     [["Usar B como periodo", "El periodo es 2π ÷ B."], ["Olvidar D en el máximo", "Máximo = D + A."], ["Mezclar grados y radianes", "Revisa en qué unidad está el ángulo."]],
     [("¿Qué es un radián?", "El ángulo que abarca un arco igual al radio; 2π radianes forman la vuelta completa."), ("¿En qué se diferencia el coseno del seno?", "Tiene la misma forma, pero empieza en su máximo: cos x = sen(x + π/2).")],
     [("Radianes", [(rad, 20)]), ("Valores de seno y coseno", [(lambda: S.q13("valor"), 12), (fun, 8)]), ("Amplitud y periodo", [(lambda: S.q13("amp"), 10), (lambda: S.q13("per"), 10)]),
      ("Máximos y mínimos", [(lambda: S.q13("maxmin"), 20)]), ("Fenómenos periódicos", [(lambda: S.q13("fenomeno"), 7), (fun, 6), (lambda: S.q13("per"), 7)])],
     120013, lv=12)
