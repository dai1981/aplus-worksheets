# -*- coding: utf-8 -*-
"""México, Pensamiento Matemático III (progresión 15): ideas intuitivas del teorema fundamental del cálculo: área bajo la curva y antiderivadas."""
import random
import mx_pm3 as S
from mx_common import src, unit

S.setup(random.Random(120115))
bar, prop, area = src("gen_es_matematicas_2bach_integrales_definidas", 120315, "s_barrow", "s_propiedades", "s_area", rep=[("regla de Barrow", "teorema fundamental del cálculo")])
inm = src("gen_es_matematicas_2bach_integrales_indefinidas", 120325, "s_inmediatas", rep=[("primitiva", "antiderivada")])
unit("teorema-fundamental-del-calculo", 15, ("Integral", 15, "Teorema fundamental del cálculo"),
     "Relaciona de forma intuitiva el área bajo una curva con las sumas de rectángulos, la antiderivada y el teorema fundamental del cálculo",
     "Área bajo la curva e integral", "Teorema fundamental",
     "Ejercicios de Pensamiento Matemático III: áreas bajo rectas, sumas de rectángulos, antiderivadas de polinomios, integral definida y teorema fundamental del cálculo. 100 ejercicios con respuestas.",
     "∫ₐᵇ f(x) dx = F(b) − F(a)", "F es una antiderivada de f.",
     ["El <b>área bajo la curva</b> se aproxima con rectángulos: más rectángulos, mejor aproximación. Su límite es la integral definida.",
      "Una <b>antiderivada</b> F de f cumple F′ = f. Para xⁿ: xⁿ⁺¹/(n + 1) + C.",
      "<b>Teorema fundamental</b>: ∫ de a a b de f(x) dx = F(b) − F(a). Derivar e integrar son procesos inversos."],
     [("∫ de 0 a 3 de 2x dx", ["F(x) = x²", "F(3) − F(0) = 9"], "9 (área de un triángulo de base 3 y altura 6)")],
     [["Olvidar + C en la antiderivada", "Hay infinitas, que difieren en una constante."], ["Restar F(a) − F(b)", "Es F(b) − F(a)."], ["Derivar en vez de integrar", "Para integrar se sube el exponente."]],
     [("¿Qué relación hay entre velocidad y distancia?", "La distancia recorrida es el área bajo la gráfica de la velocidad."), ("¿Quién descubrió el teorema fundamental?", "Newton y Leibniz, con ideas previas de Barrow, maestro de Newton.")],
     [("Áreas con geometría", [(lambda: S.q15("geo"), 20)]), ("Sumas de rectángulos", [(lambda: S.q15("riemann"), 14), (lambda: S.q15("concepto"), 5), (prop, 1)]),
      ("Antiderivadas", [(lambda: S.q15("anti"), 10), (inm, 10)]), ("Integral definida", [(bar, 12), (lambda: S.q15("tfc"), 8)]), ("Áreas", [(area, 14), (prop, 6)])],
     120015, lv=12)
