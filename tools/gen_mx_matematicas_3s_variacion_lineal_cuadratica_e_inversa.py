# -*- coding: utf-8 -*-
"""México 3.er grado de secundaria (Fase 6): Variación lineal, cuadrática y de proporcionalidad inversa en tablas, gráficas y expresiones."""
import random
import re  # noqa: F401
import mx_s2 as S
from mx_common import src, unit, nomoney, noplanta  # noqa: F401

S.setup(random.Random(69107))
par = src("gen_es_matematicas_2eso_funciones", 69351, "s_parabola", lv=2)
unit("variacion-lineal-cuadratica-e-inversa", 7, "6FU",
     "Relaciona e interpreta la variación entre dos cantidades en tablas, gráficas y expresiones algebraicas: lineal, cuadrática y de proporcionalidad inversa",
     "Variación lineal, cuadrática e inversa", "Tipos de variación",
     "Ejercicios de matemáticas de 3.er grado de secundaria: distinguir variación lineal, cuadrática e inversa en tablas y expresiones, valores de funciones cuadráticas y parábolas. 100 ejercicios con respuestas.",
     "Lineal: diferencias iguales", "Cuadrática: 2.ª diferencia igual.",
     ["En una tabla, si y aumenta siempre lo mismo, la variación es <b>lineal</b> (y = mx + b, una recta).",
      "Si las segundas diferencias son iguales, es <b>cuadrática</b> (y = ax² + bx + c, una parábola). Si x · y es constante, es <b>inversa</b> (y = k ÷ x, una hipérbola).",
      "En la parábola y = ax² + bx + c, el <b>vértice</b> es el punto más alto o más bajo; si a &gt; 0 abre hacia arriba."],
     [("y = x² − 4: cortes con el eje x", ["x² = 4"], "(−2, 0) y (2, 0)"), ("x: 1, 2, 3; y: 12, 6, 4", ["x · y = 12"], "inversa")],
     [["Pensar que toda relación que crece es lineal", "El área de un cuadrado crece, pero de forma cuadrática."], ["Olvidar el paréntesis al sustituir", "Si x = −3, x² = 9."], ["Confundir parábola e hipérbola", "La parábola tiene vértice; la hipérbola no toca los ejes."]],
     [("¿Dónde aparece la variación cuadrática?", "En el área de figuras, en la caída de objetos y en la trayectoria de un balón."), ("¿Cómo distingo los tipos en una gráfica?", "Recta: lineal. Parábola (U): cuadrática. Curva que se acerca a los ejes: inversa.")],
     [("¿Qué tipo de variación es?", [(lambda: S.variacion("tipo"), 20)]), ("Valores de funciones cuadráticas", [(lambda: S.variacion("val"), 20)]), ("Parábolas", [(par, 20)]),
      ("Lineal frente a cuadrática", [(lambda: S.variacion("tab", "tipo"), 20)]), ("Repaso", [(S.variacion, 12), (par, 8)])],
     69007, lv=9)
