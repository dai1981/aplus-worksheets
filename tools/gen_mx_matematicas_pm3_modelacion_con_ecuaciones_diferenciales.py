# -*- coding: utf-8 -*-
"""México, Pensamiento Matemático III (progresión 14): modelación con funciones derivables: planteamiento de ecuaciones diferenciales (sin resolverlas)."""
import random
import mx_pm3 as S
from mx_common import unit

S.setup(random.Random(120114))
unit("modelacion-con-ecuaciones-diferenciales", 14, ("Funciones trascendentes", 14, "Modelación con ecuaciones diferenciales"),
     "Plantea, sin resolverlas, ecuaciones diferenciales que modelan fenómenos como el crecimiento de bacterias, el decaimiento radiactivo, el enfriamiento y el modelo presa-depredador",
     "Plantear ecuaciones diferenciales", "Ecuaciones diferenciales",
     "Ejercicios de Pensamiento Matemático III: traducir «la rapidez de cambio es proporcional a…» a una ecuación diferencial, ritmo de cambio, método de Euler y comprobar soluciones. 100 ejercicios con respuestas.",
     "«Rapidez de cambio» = derivada", "dP/dt = kP: crecimiento exponencial.",
     ["Una <b>ecuación diferencial</b> relaciona una función con su derivada. «La rapidez con que cambia P» se escribe dP/dt.",
      "«Proporcional a P» se escribe kP. Crecimiento: dP/dt = kP (k &gt; 0). Decaimiento: dN/dt = −kN. Enfriamiento: dT/dt = −k(T − T<sub>a</sub>).",
      "Para estimar valores sin resolverla se puede usar el <b>método de Euler</b>: y(t + h) ≈ y(t) + h · y′(t)."],
     [("dP/dt = 0.05P con P = 2 000", ["0.05 × 2 000"], "crece 100 por unidad de tiempo")],
     [["Escribir P = kt", "La rapidez de cambio es dP/dt, no P."], ["Olvidar el signo en el decaimiento", "Si disminuye, la derivada es negativa."], ["Confundir la constante k con la población", "k es la tasa; P es la cantidad."]],
     [("¿Qué es el modelo logístico?", "dP/dt = kP(1 − P/M): crece rápido al principio y se frena al acercarse a la capacidad M."), ("¿Por qué importan?", "Describen cómo cambian las cosas: epidemias, poblaciones, medicamentos en la sangre o circuitos.")],
     [("Plantear el modelo", [(lambda: S.q14("plantear"), 6), (lambda: S.q14("concepto"), 5), (lambda: S.q14("ritmo"), 9)]), ("Ritmo de cambio", [(lambda: S.q14("ritmo"), 20)]),
      ("Método de Euler", [(lambda: S.q14("euler"), 20)]), ("Comprobar soluciones", [(lambda: S.q14("verifica"), 20)]),
      ("Repaso", [(lambda: S.q14("euler"), 10), (lambda: S.q14("ritmo"), 10)])],
     120014, lv=12)
