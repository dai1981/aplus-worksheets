# -*- coding: utf-8 -*-
"""México, Temas Selectos de Matemáticas II (progresión 5): teorema fundamental del cálculo, integral definida y áreas."""
import random
import mx_tsm as S
import mx_pm3 as P3
from mx_common import src, unit

S.setup(random.Random(140105))
bar, are, ent, apl = src("gen_es_matematicas_2bach_integrales_definidas", 140305, "s_barrow", "s_area", "s_entre", "s_aplicaciones", rep=[("regla de Barrow", "teorema fundamental del cálculo"), ("Un móvil se mueve", "Un objeto se mueve"), ("un móvil se mueve", "un objeto se mueve")])
unit("integral-definida-y-teorema-fundamental", 5, ("Integral", 5, "Teorema fundamental del cálculo"),
     "Relaciona una función, su derivada y su antiderivada con el teorema fundamental del cálculo, y calcula integrales definidas, áreas y cambios totales",
     "Teorema fundamental e integral definida", "Integral definida",
     "Ejercicios de Temas Selectos de Matemáticas II: teorema fundamental del cálculo, integrales definidas, área bajo una curva, área entre curvas y aplicaciones. 100 ejercicios con respuestas.",
     "∫ₐᵇ f(x) dx = F(b) − F(a)", "Derivar e integrar son inversos.",
     ["<b>Teorema fundamental del cálculo</b>: si F′ = f, entonces ∫ de a a b de f(x) dx = F(b) − F(a).",
      "Si f ≥ 0, la integral es el <b>área</b> bajo la curva. El área entre dos curvas es ∫ (arriba − abajo) dx.",
      "Integrar una razón de cambio da el <b>cambio total</b>: velocidad → distancia, costo marginal → aumento del costo."],
     [("∫ de 1 a 3 de (2x + 1) dx", ["F(x) = x² + x", "F(3) − F(1) = 12 − 2"], "10")],
     [["Restar F(a) − F(b)", "Es F(b) − F(a)."], ["Olvidar que el área es positiva", "Si f &lt; 0, toma el valor absoluto."], ["No encontrar los cortes entre curvas", "Iguala las funciones para hallar los límites."]],
     [("¿Para qué sirve el teorema fundamental?", "Para calcular áreas y totales sin sumar infinitos rectángulos: basta una antiderivada."), ("¿Qué representa el área bajo una gráfica de velocidad?", "La distancia recorrida.")],
     [("Teorema fundamental", [(lambda: P3.q15("tfc"), 10), (bar, 10)]), ("Integrales definidas", [(bar, 20)]), ("Área bajo una curva", [(are, 14), (lambda: P3.q15("geo"), 6)]),
      ("Área entre curvas", [(ent, 14), (lambda: P3.q15("geo"), 6)]), ("Aplicaciones", [(apl, 20)])],
     140005, lv=14)
