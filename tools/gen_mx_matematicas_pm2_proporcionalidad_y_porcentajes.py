# -*- coding: utf-8 -*-
"""México, Pensamiento Matemático II (progresión 7): proporcionalidad directa e inversa, repartos y porcentajes."""
import random
import mx_s1 as S1
from mx_common import src, unit

S1.setup(random.Random(110107))
tip, tab, reg, com, rep = src("gen_es_matematicas_2eso_proporcionalidad", 110307, "s_tipo", "s_tabla", "s_regla", "s_compuesta", "s_reparto", lv=2)
bas, var = src("gen_es_matematicas_2eso_porcentajes", 110317, "s_basico", "s_variacion")
unit("proporcionalidad-y-porcentajes", 7, ("Proporcionalidad y finanzas", 7, "Proporcionalidad y porcentajes"),
     "Resuelve problemas de proporcionalidad directa e inversa, repartos proporcionales y porcentajes (aumentos y descuentos sucesivos) usando la estructura de los números reales",
     "Proporcionalidad directa, inversa y porcentajes", "Proporcionalidad y porcentajes",
     "Ejercicios de Pensamiento Matemático II: magnitudes directa e inversamente proporcionales, regla de tres, proporcionalidad compuesta, repartos y porcentajes. 100 ejercicios con respuestas.",
     "Directa: y = kx. Inversa: xy = k", "Porcentaje: multiplica por 1 ± r.",
     ["<b>Directa</b>: si una magnitud se duplica, la otra también (y = kx). <b>Inversa</b>: si una se duplica, la otra se reduce a la mitad (x × y = k).",
      "En un <b>reparto proporcional</b> se divide el total entre la suma de las partes y se multiplica por cada parte.",
      "Un aumento del r % multiplica por (1 + r/100); un descuento, por (1 − r/100). Varios cambios seguidos se multiplican."],
     [("Sube 20 % y luego baja 20 %", ["1.2 × 0.8 = 0.96"], "baja un 4 %"), ("4 pintores tardan 6 días; ¿8 pintores?", ["Inversa: 4 × 6 = 24", "24 ÷ 8"], "3 días")],
     [["Usar regla de tres directa en una inversa", "Pregunta: si una aumenta, ¿la otra aumenta o disminuye?"], ["Sumar porcentajes sucesivos", "Se multiplican los factores."], ["Calcular el porcentaje sobre la cantidad final", "El porcentaje es de la cantidad inicial."]],
     [("¿Qué es el factor multiplicador?", "El número por el que se multiplica para aplicar un porcentaje: +15 % es × 1.15 y −15 % es × 0.85."),
      ("¿Cómo sé si es inversa?", "Si al multiplicar una magnitud por 2 la otra se divide entre 2, como trabajadores y días.")],
     [("Directa o inversa", [(tip, 10), (tab, 10)]), ("Regla de tres", [(reg, 20)]), ("Compuesta y repartos", [(com, 8), (rep, 12)]),
      ("Porcentajes", [(bas, 12), (S1.pc_problem, 8)]), ("Aumentos y descuentos", [(var, 14), (S1.pc_problem, 6)])],
     110007, lv=11)
