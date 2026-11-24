# -*- coding: utf-8 -*-
"""México, Pensamiento Matemático II (progresión 8): matemática financiera: interés simple y compuesto, ahorro y deudas."""
import random
import mx_pm2 as S
from mx_common import unit

S.setup(random.Random(110108))
unit("matematica-financiera", 8, ("Proporcionalidad y finanzas", 8, "Matemática financiera"),
     "Calcula interés simple y compuesto, montos, tasas y plazos, y analiza ahorros y deudas (tarjetas de crédito) para tomar decisiones en su proyecto de vida",
     "Interés simple, compuesto, ahorro y deudas", "Matemática financiera",
     "Ejercicios de Pensamiento Matemático II: interés simple, monto, tasa y tiempo, interés compuesto anual y mensual, ahorro, tarjetas de crédito y comparar opciones. 100 ejercicios con respuestas.",
     "I = Crt;  M = C(1 + i)ⁿ", "El compuesto gana interés sobre el interés.",
     ["<b>Interés simple</b>: el interés se calcula siempre sobre el capital inicial. I = C × r × t y el monto M = C(1 + rt).",
      "<b>Interés compuesto</b>: el interés se suma al capital cada periodo. M = C(1 + i)ⁿ, con i la tasa por periodo (anual ÷ 12 si es mensual).",
      "Las deudas de una tarjeta de crédito crecen como interés compuesto: pagar solo el mínimo hace que la deuda dure mucho más."],
     [("$10 000 al 8 % anual, 3 años", ["Simple: 10 000 × 0.08 × 3 = $2 400", "Compuesto: 10 000 × 1.08³ ≈ $12 597"], "$12 400 contra $12 597")],
     [["Usar el 8 % como 8 en la fórmula", "Usa 0.08."], ["Olvidar dividir la tasa entre 12", "Si es mensual, i = tasa anual ÷ 12 y n en meses."], ["Confundir interés con monto", "Monto = capital + interés."]],
     [("¿Qué es el CAT?", "El Costo Anual Total: incluye intereses y comisiones. Sirve para comparar créditos en México."),
      ("¿Conviene ahorrar con interés compuesto?", "Sí: con el tiempo, el interés sobre el interés hace crecer más el ahorro.")],
     [("Interés simple", [(lambda: S.lp8("simple"), 12), (lambda: S.lp8("monto"), 8)]), ("Tasa y tiempo", [(lambda: S.lp8("tasa"), 10), (lambda: S.lp8("tiempo"), 10)]),
      ("Interés compuesto", [(lambda: S.lp8("comp"), 12), (lambda: S.lp8("comp_m"), 8)]), ("Ahorro y deudas", [(lambda: S.lp8("ahorro"), 12), (lambda: S.lp8("tarjeta"), 8)]),
      ("Comparar opciones", [(lambda: S.lp8("comparar"), 14), (lambda: S.lp8("comp_m"), 6)])],
     110008, lv=11)
