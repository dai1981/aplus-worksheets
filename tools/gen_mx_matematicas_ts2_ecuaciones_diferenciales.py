# -*- coding: utf-8 -*-
"""México, Temas Selectos de Matemáticas II (progresión 6): modelación con ecuaciones diferenciales (crecimiento, presa-depredador, Kuramoto), sin resolverlas analíticamente."""
import random
import mx_tsm as S
import mx_pm3 as P3
from mx_common import unit

S.setup(random.Random(140106))
unit("ecuaciones-diferenciales", 6, ("Modelos y métodos numéricos", 6, "Ecuaciones diferenciales"),
     "Modela fenómenos como el crecimiento de poblaciones, el enfriamiento, el sistema presa-depredador de Lotka-Volterra y la sincronización de Kuramoto con ecuaciones diferenciales, sin resolverlas analíticamente",
     "Modelos con ecuaciones diferenciales", "Ecuaciones diferenciales",
     "Ejercicios de Temas Selectos de Matemáticas II: plantear ecuaciones diferenciales, ritmos de cambio, modelo logístico, enfriamiento, Lotka-Volterra y método de Euler. 100 ejercicios con respuestas.",
     "La ecuación dice cómo cambia", "dP/dt = kP(1 − P/M): crecimiento con límite.",
     ["Una <b>ecuación diferencial</b> describe la rapidez de cambio: dP/dt = kP (crecimiento), dT/dt = −k(T − Tₐ) (enfriamiento).",
      "<b>Logístico</b>: dP/dt = kP(1 − P/M) crece rápido y se frena cerca de la capacidad M. <b>Lotka-Volterra</b>: dos ecuaciones para presas y depredadores.",
      "Sin resolverlas se pueden estudiar: sustituye valores para ver si la cantidad sube o baja, o avanza con el método de Euler."],
     [("dP/dt = 0.1P(1 − P/1 000) con P = 500", ["0.1 × 500 × 0.5"], "crece 25 por unidad de tiempo")],
     [["Olvidar el signo negativo del decaimiento", "Si disminuye, la derivada es negativa."], ["Pensar que el logístico crece sin límite", "Se acerca a M."], ["Confundir la variable con su derivada", "dP/dt es el ritmo; P es la cantidad."]],
     [("¿Qué es la capacidad de carga?", "La población máxima que un ambiente puede sostener."), ("¿Qué estudia el modelo de Kuramoto?", "Cómo muchos osciladores acoplados se sincronizan, como las luciérnagas o las células del corazón.")],
     [("Plantear el modelo", [(lambda: P3.q14("plantear"), 6), (lambda: P3.q14("verifica"), 14)]), ("Crecimiento logístico", [(lambda: S.u6("logistico"), 20)]),
      ("Enfriamiento y presa-depredador", [(lambda: S.u6("newton"), 10), (lambda: S.u6("lotka"), 10)]), ("Método de Euler", [(lambda: P3.q14("euler"), 20)]),
      ("Ideas clave", [(lambda: S.u6("kuramoto"), 6), (lambda: P3.q14("concepto"), 5), (lambda: P3.q14("ritmo"), 9)])],
     140006, lv=14)
