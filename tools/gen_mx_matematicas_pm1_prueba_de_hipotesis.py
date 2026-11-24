# -*- coding: utf-8 -*-
"""México, Pensamiento Matemático I (progresión 15): estadística inferencial, hipótesis nula y alternativa, valor p y simulación."""
import random
import mx_pm1 as S
from mx_common import src, unit

S.setup(random.Random(100115))
cri = src("gen_es_matematicas_2ccss_intervalos_de_confianza", 100315, "s_critico")
unit("prueba-de-hipotesis", 15, ("Estadística", 15, "Estadística inferencial y prueba de hipótesis"),
     "Usa propiedades de la distribución normal y simulaciones para hacer inferencias y decidir sobre hipótesis con el valor p y el nivel de significancia",
     "Prueba de hipótesis y valor p", "Prueba de hipótesis",
     "Ejercicios de Pensamiento Matemático I: hipótesis nula y alternativa, nivel de significancia, valor p, simulaciones, estadístico z y errores tipo I y II. 100 ejercicios con respuestas.",
     "Si p < α, se rechaza H₀", "p pequeño: datos raros si H₀ fuera cierta.",
     ["<b>H₀</b> (hipótesis nula) es lo que se afirma, con «=». <b>H₁</b> (alternativa) es lo que se sospecha: &lt;, &gt; o ≠.",
      "El <b>valor p</b> es la probabilidad de obtener datos tan extremos si H₀ fuera cierta. Se puede estimar con una <b>simulación</b>.",
      "Se fija α (por ejemplo 0.05). Si p &lt; α, se <b>rechaza H₀</b>. Con σ conocida: z = (x̄ − μ₀) ÷ (σ/√n)."],
     [("Moneda: 16 águilas de 20. En 1 000 simulaciones justas, 6 dieron 16 o más.", ["p ≈ 6 ÷ 1 000 = 0.006", "0.006 &lt; 0.05"], "se rechaza H₀: parece cargada")],
     [["Decir que H₀ quedó demostrada", "Solo no hay evidencia para rechazarla."], ["Poner la sospecha en H₀", "La sospecha va en H₁."], ["Comparar z con α", "Compara p con α, o z con el valor crítico."]],
     [("¿Qué valor de α se usa más?", "0.05 (5 %). En estudios médicos a veces se usa 0.01."),
      ("¿Qué relación hay con los intervalos de confianza?", "Si el valor de H₀ queda fuera del intervalo de confianza del 95 %, se rechaza H₀ con α = 0.05 (prueba bilateral).")],
     [("Plantear hipótesis", [(lambda: S.p15("h0"), 5), (lambda: S.p15("pval"), 10), (lambda: S.p15("error"), 4), (lambda: S.p15("concepto"), 1)]), ("Valor p y simulación", [(lambda: S.p15("sim"), 20)]),
      ("Estadístico z", [(lambda: S.p15("z"), 20)]), ("Valores críticos", [(cri, 6), (lambda: S.p15("pval"), 8), (lambda: S.p15("z"), 6)]),
      ("Repaso", [(lambda: S.p15("sim"), 12), (lambda: S.p15("z"), 4), (lambda: S.p15("concepto"), 4)])],
     100015, lv=10)
