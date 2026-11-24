# -*- coding: utf-8 -*-
"""México 2.º grado de secundaria (Fase 6): Notación científica y exponentes negativos."""
import random
import re  # noqa: F401
import mx_s2 as S
from mx_common import src, unit, nomoney, noplanta  # noqa: F401

S.setup(random.Random(68104))
cie, prop = src("gen_es_matematicas_2eso_potencias", 68341, "s_cient", "s_prop", lv=2)
unit("notacion-cientifica", 4, "6OP",
     "Usa potencias con exponente entero (positivo y negativo) y la notación científica para expresar cantidades muy grandes y muy pequeñas",
     "Notación científica", "Notación científica",
     "Ejercicios de matemáticas de 2.º grado de secundaria: notación científica, potencias de 10, exponentes negativos y operaciones con números muy grandes y muy pequeños. 100 ejercicios con respuestas.",
     "a × 10ⁿ, con 1 ≤ a &lt; 10", "Exponente negativo: número menor que 1.",
     ["Un número en <b>notación científica</b> se escribe a × 10ⁿ, donde a está entre 1 y 10 (sin llegar a 10).",
      "Si el número es muy grande, n es positivo y cuenta cuántos lugares se mueve el punto a la izquierda: 45 000 000 = 4.5 × 10⁷.",
      "Si es muy pequeño, n es <b>negativo</b>: 0.00032 = 3.2 × 10⁻⁴. Recuerda: 10⁻³ = 1/1 000."],
     [("3 600 000", ["El punto se mueve 6 lugares"], "3.6 × 10⁶"), ("0.0007", ["El punto se mueve 4 lugares a la derecha"], "7 × 10⁻⁴")],
     [["Dejar a mayor que 10", "45 × 10⁶ no está en notación científica: es 4.5 × 10⁷."], ["Signo equivocado del exponente", "0.002 = 2 × 10⁻³, no 2 × 10³."], ["Sumar exponentes al sumar", "Solo se suman al multiplicar."]],
     [("¿Dónde se usa la notación científica?", "En ciencias: distancias entre planetas, tamaño de células o bacterias, población del mundo."), ("¿Qué es 10⁻¹?", "1/10 = 0.1.")],
     [("Números grandes", [(cie, 20)]), ("Números pequeños", [(cie, 20)]), ("Exponentes negativos", [(prop, 20)]), ("Operaciones con potencias de 10", [(prop, 10), (cie, 10)]), ("Repaso", [(cie, 12), (prop, 8)])],
     68004, lv=8)
