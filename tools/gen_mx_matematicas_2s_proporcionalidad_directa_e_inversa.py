# -*- coding: utf-8 -*-
"""México 2.º grado de secundaria (Fase 6): Proporcionalidad directa (constante positiva y negativa) e inversa."""
import random
import re  # noqa: F401
import mx_s2 as S
from mx_common import src, unit, nomoney, noplanta  # noqa: F401

S.setup(random.Random(68109))
tab, reg = src("gen_es_matematicas_2eso_proporcionalidad", 68371, "s_tabla", "s_regla", lv=2, extra=(nomoney, lambda it: "grifo" not in it["q"]))
unit("proporcionalidad-directa-e-inversa", 9, "6FU",
     "Modela y resuelve situaciones con ecuaciones de proporcionalidad de constante positiva y negativa; relaciona e interpreta la proporcionalidad inversa en tablas, gráficas y expresiones algebraicas",
     "Proporcionalidad directa e inversa", "Proporcionalidad inversa",
     "Ejercicios de matemáticas de 2.º grado de secundaria: proporcionalidad directa con constante positiva y negativa, proporcionalidad inversa en tablas, expresiones y problemas. 100 ejercicios con respuestas.",
     "Inversa: x · y siempre igual", "Directa: y ÷ x siempre igual.",
     ["En la <b>proporcionalidad directa</b> y = kx, el cociente y ÷ x es constante. Si k es negativa (y = −3x), cuando x aumenta, y disminuye en la misma razón.",
      "En la <b>proporcionalidad inversa</b>, el <b>producto</b> x · y es constante: y = k ÷ x. Si una cantidad se duplica, la otra se reduce a la mitad.",
      "Ejemplo inverso: más trabajadores tardan menos días. Si 4 tardan 6 días (4 × 6 = 24), 8 tardan 24 ÷ 8 = 3 días."],
     [("6 llaves llenan un tinaco en 20 min; ¿4 llaves?", ["6 × 20 = 120", "120 ÷ 4"], "30 min"), ("y = −4x con x = −3", ["−4 × (−3)"], "12")],
     [["Usar regla de tres directa en una inversa", "Más pintores no tardan más días."], ["Pensar que con k negativa no es proporcional", "y = −2x sí es proporcional: y ÷ x = −2."], ["Confundir cociente y producto", "Directa: cociente; inversa: producto."]],
     [("¿Cómo es la gráfica de la proporcionalidad inversa?", "Una curva (hipérbola) que se acerca a los ejes sin tocarlos."), ("¿Cómo sé si es inversa?", "Multiplica x por y en cada pareja: si siempre da lo mismo, es inversa.")],
     [("¿Directa o inversa?", [(lambda: S.prop_inv("tipo"), 8), (lambda: S.prop_inv("tabla_inv"), 12)]), ("Constante negativa", [(lambda: S.prop_inv("neg"), 20)]), ("Tablas de proporcionalidad", [(lambda: S.prop_inv("tabla_inv"), 6), (tab, 14)]),
      ("Problemas de proporcionalidad inversa", [(lambda: S.prop_inv("inv"), 20)]), ("Problemas", [(reg, 12), (lambda: S.prop_inv("inv", "neg"), 8)])],
     68009, lv=8)
