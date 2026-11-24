# -*- coding: utf-8 -*-
"""México, Pensamiento Matemático I (progresión 2): probabilidad frecuencial, simulación y ley de los grandes números."""
import random
import mx_pm1 as S
from mx_common import unit

S.setup(random.Random(100102))
unit("probabilidad-frecuencial", 2, ("Probabilidad", 2, "Incertidumbre y probabilidad frecuencial"),
     "Relaciona la incertidumbre con la variabilidad y estima la probabilidad de un evento con la frecuencia relativa obtenida de datos o simulaciones",
     "Probabilidad frecuencial y simulaciones", "Probabilidad frecuencial",
     "Ejercicios de Pensamiento Matemático I: frecuencia relativa, estimar probabilidades con datos y simulaciones, predicciones y ley de los grandes números. 100 ejercicios con respuestas.",
     "P ≈ veces que ocurre ÷ total", "Con más ensayos, mejor estimación.",
     ["La <b>frecuencia relativa</b> es: veces que ocurre ÷ número total de repeticiones. Sirve para <b>estimar</b> la probabilidad.",
      "Para <b>predecir</b>, multiplica la probabilidad estimada por el número de repeticiones nuevas.",
      "Con <b>muchas</b> repeticiones la frecuencia relativa se estabiliza cerca de la probabilidad (ley de los grandes números)."],
     [("Una tachuela cayó de punta 30 de 50 veces.", ["30 ÷ 50 = 0.6"], "P ≈ 0.6"), ("¿Cuántas veces de punta en 400 lanzamientos?", ["0.6 × 400"], "240 veces")],
     [["Dividir total ÷ veces", "Es veces ÷ total."], ["Confiar en pocos ensayos", "Con 10 ensayos la estimación varía mucho."], ["Creer que la predicción es exacta", "Es lo esperado, no un resultado seguro."]],
     [("¿Qué diferencia hay con la probabilidad teórica?", "La frecuencial se estima con datos; la teórica se calcula suponiendo resultados igual de probables."),
      ("¿Para qué sirve simular?", "Para repetir un experimento muchas veces de forma rápida y estimar su probabilidad.")],
     [("Frecuencia relativa", [(lambda: S.p2("fr"), 20)]), ("En porcentaje", [(lambda: S.p2("pct"), 12), (lambda: S.p2("fr"), 8)]),
      ("Predecir resultados", [(lambda: S.p2("pred"), 20)]), ("Ley de los grandes números", [(lambda: S.p2("concepto"), 8), (lambda: S.p2("fiable"), 12)]),
      ("Repaso", [(lambda: S.p2("pred"), 10), (lambda: S.p2("fr"), 10)])],
     100002, lv=10)
