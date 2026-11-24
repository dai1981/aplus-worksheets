# -*- coding: utf-8 -*-
"""México, Pensamiento Matemático III (progresión 10): crecimiento, extremos y concavidad con la derivada; trazo de gráficas."""
import random
import mx_pm3 as S
from mx_common import src, unit

S.setup(random.Random(120110))
mon, ext, cur, gra = src("gen_es_matematicas_1bach_aplicaciones_derivadas", 120310, "s_monotonia", "s_extremos", "s_curvatura", "s_grafica", lv=1)
unit("analisis-de-funciones-con-derivadas", 10, ("Derivadas", 10, "Análisis de funciones con la derivada"),
     "Usa la primera y la segunda derivada para determinar intervalos de crecimiento, máximos y mínimos, concavidad y puntos de inflexión, y trazar la gráfica",
     "Crecimiento, extremos y concavidad", "Análisis con derivadas",
     "Ejercicios de Pensamiento Matemático III: intervalos de crecimiento, puntos críticos, máximos y mínimos, criterio de la segunda derivada, concavidad, puntos de inflexión y gráficas. 100 ejercicios con respuestas.",
     "f′ = 0: posible máximo o mínimo", "f″ decide: &gt; 0 mínimo, &lt; 0 máximo.",
     ["Si f′(x) &gt; 0 la función <b>crece</b>; si f′(x) &lt; 0, <b>decrece</b>. Los <b>puntos críticos</b> cumplen f′(x) = 0.",
      "Si f′ cambia de + a −, hay un <b>máximo</b>; de − a +, un <b>mínimo</b>. También: f″(a) &lt; 0 → máximo, f″(a) &gt; 0 → mínimo.",
      "Si f″ &gt; 0 es cóncava hacia arriba; si f″ &lt; 0, hacia abajo. Donde cambia hay un <b>punto de inflexión</b>."],
     [("f(x) = x³ − 3x", ["f′(x) = 3x² − 3 = 0 → x = ±1", "f″(−1) = −6, f″(1) = 6"], "máximo en x = −1, mínimo en x = 1")],
     [["Creer que f′ = 0 siempre es extremo", "x³ tiene f′(0) = 0 y no hay extremo."], ["Dar el extremo sin la coordenada y", "Calcula f(a)."], ["Confundir concavidad con crecimiento", "Concavidad: signo de f″."]],
     [("¿Para qué sirve la segunda derivada?", "Para saber cómo se curva la gráfica y confirmar si un punto crítico es máximo o mínimo."), ("¿Qué es un punto de inflexión?", "Donde la gráfica cambia de cóncava hacia arriba a hacia abajo, o al revés.")],
     [("Crecimiento", [(mon, 20)]), ("Máximos y mínimos", [(ext, 12), (lambda: S.q4("max"), 8)]), ("Concavidad", [(cur, 14), (lambda: S.q4("concav"), 6)]),
      ("Gráficas y derivadas", [(gra, 20)]), ("Repaso", [(mon, 6), (ext, 6), (cur, 8)])],
     120010, lv=12)
