# -*- coding: utf-8 -*-
"""México, Pensamiento Matemático III (progresión 1): origen del cálculo: variación promedio e instantánea, movimiento y procesos infinitos."""
import random
import mx_pm3 as S
from mx_common import src, unit

S.setup(random.Random(120101))
tvm = src("gen_es_matematicas_1bach_derivadas", 120301, "s_tvm", lv=1, extra=(lambda it: "definición" not in it["q"],))
unit("origen-del-calculo", 1, ("Variación y funciones", 1, "Origen del cálculo: variación y movimiento"),
     "Explora de forma intuitiva la variación promedio e instantánea, el movimiento y los procesos infinitos que dieron origen al cálculo",
     "Variación promedio e instantánea", "Origen del cálculo",
     "Ejercicios de Pensamiento Matemático III: razón de cambio promedio, velocidad promedio, acercarse a la velocidad instantánea con tablas y sumas infinitas. 100 ejercicios con respuestas.",
     "Promedio: cambio ÷ tiempo", "Instantánea: el intervalo se hace casi 0.",
     ["La <b>razón de cambio promedio</b> de f entre a y b es [f(b) − f(a)] ÷ (b − a). Si f es la posición, es la velocidad promedio.",
      "La <b>velocidad instantánea</b> se obtiene tomando intervalos cada vez más pequeños: las velocidades promedio se acercan a un número.",
      "Un proceso infinito puede dar un resultado finito: 1 + 1/2 + 1/4 + … se acerca a 2. Esta idea llevó a Newton y Leibniz a crear el cálculo."],
     [("d(t) = 5t², entre t = 1 y t = 3", ["d(3) − d(1) = 45 − 5 = 40", "40 ÷ 2"], "20 m/s"), ("1 + 1/2 + 1/4 + …", ["S = 1 ÷ (1 − 1/2)"], "2")],
     [["Dividir solo entre b", "Se divide entre b − a."], ["Confundir velocidad promedio con la del final", "La promedio usa todo el intervalo."], ["Pensar que una suma infinita siempre es infinita", "Si los términos se achican rápido, puede ser finita."]],
     [("¿Qué es la paradoja de Zenón?", "Aquiles nunca alcanzaría a la tortuga si siempre le falta la mitad del camino; se resuelve porque la suma infinita de esas distancias es finita."),
      ("¿Para qué sirve el cálculo?", "Para estudiar cómo cambian las cosas: velocidad, crecimiento, costos y áreas.")],
     [("Razón de cambio promedio", [(lambda: S.q1("tvm"), 12), (tvm, 8)]), ("Datos en tablas", [(lambda: S.q1("tabla"), 20)]), ("Velocidad promedio", [(lambda: S.q1("vel"), 20)]),
      ("Velocidad instantánea", [(lambda: S.q1("inst"), 14), (lambda: S.q1("vel"), 6)]), ("Procesos infinitos", [(lambda: S.q1("zenon"), 14), (tvm, 6)])],
     120001, lv=12)
