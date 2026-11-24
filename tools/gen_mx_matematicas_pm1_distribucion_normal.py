# -*- coding: utf-8 -*-
"""México, Pensamiento Matemático I (progresión 14): distribución normal, regla 68-95-99.7, estandarización y áreas bajo la curva."""
import random
import mx_pm1 as S
from mx_common import src, unit

S.setup(random.Random(100114))
tab, tip, inv = src("gen_es_matematicas_2bach_distribuciones", 100314, "s_tabla", "s_tipificar", "s_inversa")
unit("distribucion-normal", 14, ("Estadística", 14, "Distribución normal"),
     "Calcula probabilidades como áreas bajo la curva normal usando la regla empírica, la estandarización z = (x − μ)/σ y la tabla de la normal estándar",
     "Distribución normal y valores z", "Distribución normal",
     "Ejercicios de Pensamiento Matemático I: curva normal, regla 68-95-99.7, valores z, estandarización y probabilidades con la tabla de la normal estándar. 100 ejercicios con respuestas.",
     "z = (x − μ) ÷ σ", "68 % a 1σ, 95 % a 2σ, 99.7 % a 3σ.",
     ["La <b>distribución normal</b> tiene forma de campana, simétrica respecto a la media μ. La probabilidad es el área bajo la curva.",
      "<b>Regla empírica</b>: entre μ ± σ está cerca del 68 %; entre μ ± 2σ, el 95 %; entre μ ± 3σ, el 99.7 %.",
      "Para usar la tabla, <b>estandariza</b>: z = (x − μ) ÷ σ. Luego busca P(Z ≤ z)."],
     [("μ = 160 cm, σ = 7 cm. ¿P(X ≤ 174)?", ["z = (174 − 160) ÷ 7 = 2", "P(Z ≤ 2) = 0.9772"], "≈ 0.977")],
     [["Olvidar dividir entre σ", "z cuenta desviaciones, no unidades."], ["Usar P(Z ≤ z) para «mayor que»", "P(Z ≥ z) = 1 − P(Z ≤ z)."], ["Pensar que la regla es exacta", "68, 95 y 99.7 son aproximaciones."]],
     [("¿Por qué es tan común la distribución normal?", "Muchas medidas que suman muchos efectos pequeños (estaturas, errores de medición) se reparten en forma de campana."),
      ("¿Qué indica un z negativo?", "Que el valor está por debajo de la media.")],
     [("Regla 68-95-99.7", [(lambda: S.p14("regla"), 20)]), ("Valores z", [(lambda: S.p14("z"), 14), (lambda: S.p14("concepto"), 6)]),
      ("Tabla de la normal estándar", [(tab, 20)]), ("Estandarizar", [(tip, 20)]),
      ("Comparar y buscar valores", [(lambda: S.p14("comp"), 10), (inv, 10)])],
     100014, lv=10)
