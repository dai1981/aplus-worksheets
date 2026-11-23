# -*- coding: utf-8 -*-
"""México 6.º grado: Porcentajes: 50 %, 25 %, 10 % y 1 %; porcentaje de una cantidad, descuentos y qué porcentaje es (Relaciones de proporcionalidad). Reutiliza España 6.º con otra semilla."""
import re
from mx_common import src, unit

conc, calc, desc, que, probl = src("gen_es_matematicas_6_porcentajes", 66313, "s1_concepto", "s2_calcular", "s3_descuento", "s4_que_porcentaje", "s5_problema", lv=6,
                                   extra=(lambda it: not re.search(r"IVA|interés", it["q"]),))

unit("porcentajes", 7, "Q",
     "Calcula porcentajes de una cantidad usando 50 %, 25 %, 10 % y 1 % y sus combinaciones; calcula descuentos y aumentos; determina qué porcentaje representa una cantidad de otra",
     "Porcentajes de una cantidad", "Porcentajes",
     "Ejercicios de matemáticas de 6.º grado de primaria: porcentaje de una cantidad con 50 %, 25 %, 10 % y 1 %, descuentos, qué porcentaje es y problemas. 100 ejercicios con respuestas.",
     "10 % = ÷ 10; 1 % = ÷ 100", "Combina: 35 % = 25 % + 10 %.",
     ["Para calcular porcentajes de memoria usa los más fáciles: 50 % (la mitad), 25 % (la cuarta parte), 10 % (÷ 10) y 1 % (÷ 100).",
      "Los demás se forman combinando: 35 % de 800 = 25 % (200) + 10 % (80) = 280. 15 % = 10 % + la mitad del 10 %.",
      "Para saber qué porcentaje es una parte del total, escribe la fracción y conviértela a centésimos: 12 de 48 = 1/4 = 25/100 = 25 %."],
     [("15 % de $640", ["10 % = $64", "5 % = $32", "64 + 32"], "$96"), ("Precio $850 con 20 % de descuento", ["descuento: 850 ÷ 10 × 2 = 170", "850 − 170"], "$680")],
     [["Pensar que 1 % = 1", "1 % de 300 es 3."], ["Dar solo el descuento", "El precio final es precio − descuento."], ["Sumar porcentajes de cantidades distintas", "Calcula cada porcentaje sobre su cantidad."]],
     [("¿Cómo calculo el 1 % de un número?", "Divide entre 100: el 1 % de 4 500 es 45. Así el 3 % es 3 × 45 = 135."),
      ("¿Qué porcentaje es 18 de 72?", "18/72 = 1/4 = 25 %.")],
     [("Porcentajes, fracciones y decimales", [(conc, 20)]), ("Porcentaje de una cantidad", [(calc, 20)]), ("¿Qué porcentaje es?", [(que, 20)]), ("Descuentos y aumentos", [(desc, 20)]), ("Problemas", [(probl, 20)])],
     66007, lv=6)
