# -*- coding: utf-8 -*-
"""México 6.º grado: Relaciones de proporcionalidad: valor faltante, razones, escalas y magnitudes no proporcionales. Reutiliza España 6.º con otra semilla."""
from mx_common import src, unit

tabla, regla, escala, razon, probl = src("gen_es_matematicas_6_proporcionalidad", 66312, "s1_tabla", "s2_regla", "s3_escala", "s4_razon", "s5_problema", lv=6, extra=(lambda it: "gasolina" not in it["q"],))

unit("proporcionalidad", 6, "Q",
     "Resuelve problemas de valor faltante en situaciones de proporcionalidad directa con números naturales, fraccionarios y decimales; usa razones y escalas; distingue situaciones proporcionales y no proporcionales",
     "Proporcionalidad: valor faltante y escalas", "Proporcionalidad",
     "Ejercicios de matemáticas de 6.º grado de primaria: valor faltante, tablas de proporcionalidad, razones, escalas y situaciones no proporcionales. 100 ejercicios con respuestas.",
     "Halla el valor de 1 y multiplica", "Comprueba que la razón sea la misma.",
     ["En una situación de <b>proporcionalidad directa</b>, si una cantidad se multiplica por un número, la otra también. El cociente entre ellas es siempre el mismo.",
      "Para el <b>valor faltante</b>: calcula lo que corresponde a 1 (valor unitario) y multiplica. Si 4 kg cuestan $86, 1 kg cuesta $21.50 y 6 kg, $129.",
      "No todo es proporcional: la edad y la estatura de una persona no lo son."],
     [("5 m de tela cuestan $175; ¿cuánto 8 m?", ["1 m: 175 ÷ 5 = $35", "8 m: 35 × 8"], "$280"), ("Escala 1:200 000; 3.5 cm", ["3.5 × 200 000 = 700 000 cm"], "7 km")],
     [["Sumar la diferencia en vez de multiplicar", "Si 2 → 30, entonces 6 → 90, no 34."], ["Pensar que todo es proporcional", "La edad y la estatura no lo son."], ["Olvidar convertir unidades en la escala", "100 000 cm = 1 km."]],
     [("¿Cómo sé si dos cantidades son proporcionales?", "Divide cada valor de una entre el de la otra: si siempre da lo mismo, son proporcionales."),
      ("¿Qué es una razón?", "Una comparación entre dos cantidades por división, como 3 a 4 o 3/4.")],
     [("Tablas de proporcionalidad", [(tabla, 20)]), ("Valor faltante", [(regla, 20)]), ("Razones", [(razon, 20)]), ("Escalas", [(escala, 20)]), ("Problemas", [(probl, 20)])],
     66006, lv=6)
