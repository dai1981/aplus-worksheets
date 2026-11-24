# -*- coding: utf-8 -*-
"""México, Pensamiento Matemático II (progresión 12): funciones lineales, cuadráticas y polinomiales como modelos."""
import random
import mx_pm2 as S
from mx_common import src, unit

S.setup(random.Random(110112))
pen, ecu, par = src("gen_es_matematicas_2eso_funciones", 110312, "s_pend", "s_ecuacion", "s_parabola", lv=2)
cor = src("gen_es_matematicas_3eso_funciones_propiedades", 110322, "s_cortes", lv=3)
unit("funciones-lineales-cuadraticas-y-polinomiales", 12, ("Funciones y sistemas", 12, "Funciones lineales, cuadráticas y polinomiales"),
     "Modela situaciones con funciones lineales, cuadráticas y polinomiales, y reconoce en su expresión algebraica y en su gráfica la pendiente, el vértice, los ceros y la ordenada al origen",
     "Funciones lineales, cuadráticas y polinomiales", "Funciones polinomiales",
     "Ejercicios de Pensamiento Matemático II: pendiente y ordenada al origen, ecuación de la recta, parábolas y vértice, ceros y grado de un polinomio. 100 ejercicios con respuestas.",
     "Grado 1: recta. Grado 2: parábola.", "Los ceros son los cortes con el eje x.",
     ["<b>Lineal</b> f(x) = mx + b: m es la pendiente (cambio por unidad) y b la ordenada al origen.",
      "<b>Cuadrática</b> f(x) = ax² + bx + c: su gráfica es una parábola con vértice en x = −b/(2a); abre hacia arriba si a &gt; 0.",
      "<b>Polinomial</b> de grado n: tiene a lo más n ceros. Si está factorizada, cada factor (x − r) da un cero x = r."],
     [("f(x) = x² − 6x + 5", ["x = −(−6)/2 = 3", "f(3) = 9 − 18 + 5 = −4", "(x − 1)(x − 5)"], "vértice (3, −4); ceros 1 y 5")],
     [["Confundir pendiente con ordenada", "En y = 3x + 2, la pendiente es 3."], ["Signo del cero", "(x + 4) se anula en x = −4."], ["Olvidar el signo de a", "a &lt; 0: la parábola abre hacia abajo."]],
     [("¿Para qué sirven estas funciones?", "Para modelar costos (lineal), áreas y trayectorias (cuadrática) o volúmenes de cajas (cúbica)."),
      ("¿Qué es el grado de un polinomio?", "El mayor exponente de x; indica la forma general de la gráfica.")],
     [("Funciones lineales", [(pen, 10), (ecu, 10)]), ("Parábolas", [(par, 12), (lambda: S.lp12("vertice"), 8)]), ("Cortes con los ejes", [(cor, 12), (lambda: S.lp12("corte"), 8)]),
      ("Funciones polinomiales", [(lambda: S.lp12("eval"), 8), (lambda: S.lp12("grado"), 6), (lambda: S.lp12("raices"), 6)]),
      ("Modelos", [(lambda: S.lp12("tipo"), 6), (lambda: S.lp12("raices"), 6), (ecu, 8)])],
     110012, lv=11)
