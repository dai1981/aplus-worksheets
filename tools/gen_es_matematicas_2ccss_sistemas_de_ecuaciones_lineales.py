# -*- coding: utf-8 -*-
"""
España Matemáticas Aplicadas a las Ciencias Sociales II (2.º de Bachillerato): Sistemas de ecuaciones lineales (Sentido algebraico)
Expresión matricial, método de Gauss, teorema de Rouché-Frobenius (rangos), discusión con un parámetro, problemas de economía.
Reutiliza los generadores de Matemáticas I y II y de 1.º CCSS con otra semilla.
Errores: confundir matriz de coeficientes y ampliada, confundir compatible indeterminado e incompatible, desordenar las incógnitas.
"""
import random
from es_ccss import M, mix, unit, L, use_

R = random.Random(54002)
s_economia, = use_("gen_es_matematicas_1ccss_sistemas_de_ecuaciones", 54302, "s_economia"),
s_gauss, = use_("gen_es_matematicas_1bach_sistemas_metodo_de_gauss", 54202, "s_gauss"),
s_matricial, s_rouche, s_discutir = use_("gen_es_matematicas_2bach_sistemas", 54102, "s_matricial", "s_rouche", "s_discutir")

seen = set()
sets = [("Expresión matricial", mix(R, seen, [(s_matricial, 20)])), ("Método de Gauss", mix(R, seen, [(s_gauss, 20)])), ("Teorema de Rouché-Frobenius", mix(R, seen, [(s_rouche, 20)])),
        ("Discusión con un parámetro", mix(R, seen, [(s_discutir, 20)])), ("Problemas de economía", mix(R, seen, [(s_economia, 20)]))]
think = ["Un sistema lineal se escribe como <b>A · X = B</b>: A es la matriz de coeficientes, X las incógnitas y B los términos independientes. A* (ampliada) es A con la columna B.",
         "<b>Gauss</b>: se hacen ceros debajo de la diagonal de A* y se despeja de abajo arriba.",
         "<b>Rouché-Frobenius</b>: si rango(A) = rango(A*) = n.º de incógnitas, compatible determinado; si rango(A) = rango(A*) menor, compatible indeterminado; si rango(A) ≠ rango(A*), incompatible.",
         "Con un parámetro, se buscan los valores que anulan |A| (o que hacen aparecer una fila de ceros) y se estudia cada caso."]
ex = [("x + y = 3; 2x + 2y = m", ["rango(A) = 1", "si m = 6, rango(A*) = 1"], "m = 6: infinitas soluciones; m ≠ 6: ninguna")]
mist = [["Confundir A con A*", "A* lleva además la columna de términos independientes."], ["0 = 0 o 0 = 5", "0 = 0: indeterminado; 0 = 5: incompatible."], ["Olvidar comprobar en el enunciado", "La solución debe tener sentido (cantidades positivas, enteras…)."]]
body = L(think, ex, mist)
faq = [("¿Qué dice el teorema de Rouché-Frobenius?", "Un sistema es compatible si y solo si el rango de la matriz de coeficientes es igual al de la ampliada. Si además coincide con el número de incógnitas, la solución es única."),
       ("¿Qué significa discutir un sistema?", "Decir, según el valor de un parámetro, si el sistema tiene una solución, infinitas o ninguna.")]
unit(2, R, "sistemas-de-ecuaciones-lineales", "A", "Sistemas de ecuaciones lineales: expresión matricial, método de Gauss, teorema de Rouché-Frobenius, discusión con un parámetro y problemas",
     "Sistemas de ecuaciones lineales", "Sistemas lineales", "Fichas de Matemáticas Aplicadas a las Ciencias Sociales II: forma matricial, Gauss, Rouché-Frobenius, discusión de sistemas y problemas. 100 ejercicios.",
     "rango(A) = rango(A*): compatible", "Si además es igual a n, solución única.", body, faq, sets, 2)
