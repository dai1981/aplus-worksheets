# -*- coding: utf-8 -*-
"""México 1.er grado de secundaria (Fase 6): Suma, resta, multiplicación y división con números con signo; operaciones inversas."""
import random
import mx_s1 as S
from mx_common import src, unit, nomoney, noplanta  # noqa: F401

S.setup(random.Random(67102))
suma, mult, comb, prob = src("gen_es_matematicas_1eso_numeros_enteros", 67321, "s_suma", "s_mult", "s_comb", "s_problema", lv=1, extra=(nomoney, noplanta))
oper, dif = src("gen_es_matematicas_6_numeros_enteros", 67322, "s3_operar", "s3_dif", lv=6, extra=(nomoney, noplanta))

unit("operaciones-con-numeros-con-signo", 2, "6OP",
     "Reconoce el significado de las cuatro operaciones básicas y sus relaciones inversas al resolver problemas que impliquen el uso de números con signo",
     "Operaciones con números con signo", "Operaciones con signo",
     "Ejercicios de matemáticas de 1.er grado de secundaria: suma, resta, multiplicación y división de números positivos y negativos, ley de los signos, operaciones combinadas y problemas. 100 ejercicios con respuestas.",
     "Restar es sumar el opuesto", "Signos iguales dan +; signos distintos dan −.",
     ["<b>Sumar</b> con el mismo signo: sumas y dejas el signo. Con signos distintos: restas y pones el signo del de mayor valor absoluto.",
      "<b>Restar</b> es sumar el opuesto: 5 − (−3) = 5 + 3 = 8. La resta es la operación inversa de la suma.",
      "<b>Multiplicar y dividir</b>: signos iguales dan positivo y signos distintos dan negativo (ley de los signos). La división es la inversa de la multiplicación."],
     [("−7 + 12", ["Signos distintos: 12 − 7 = 5", "Gana el signo de 12"], "5"), ("(−6) × (−4)", ["Signos iguales: positivo"], "24"), ("−20 ÷ 5", ["Signos distintos: negativo"], "−4")],
     [["Restar sin cambiar el signo", "4 − (−2) = 4 + 2 = 6, no 2."], ["Aplicar la ley de los signos a la suma", "−3 + (−5) = −8, no 8."], ["Olvidar la jerarquía", "En −2 + 3 × (−4) primero se multiplica: −2 − 12 = −14."]],
     [("¿Por qué menos por menos da más?", "Multiplicar por −1 cambia el sentido en la recta. Si lo haces dos veces, vuelves al sentido original: positivo."),
      ("¿Cómo compruebo una división?", "Con la operación inversa: si −24 ÷ 6 = −4, entonces −4 × 6 = −24.")],
     [("Sumar y restar", [(suma, 12), (oper, 8)]), ("Multiplicar y dividir", [(mult, 20)]), ("Operaciones combinadas", [(comb, 20)]),
      ("Operaciones inversas", [(suma, 10), (mult, 10)]), ("Problemas", [(prob, 8), (dif, 6), (S.pn_context, 6)])],
     67002, lv=7)
