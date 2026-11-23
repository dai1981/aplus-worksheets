# -*- coding: utf-8 -*-
"""México 5.º grado: Relaciones de proporcionalidad: tablas, valor unitario, dobles y mitades, escalas (Fase 5). Reutiliza España 6.º (nivel 5.º) con otra semilla."""
from mx_common import src, unit

tabla, regla, escala, razon, probl = src("gen_es_matematicas_6_proporcionalidad", 65312, "s1_tabla", "s2_regla", "s3_escala", "s4_razon", "s5_problema", lv=5, extra=(lambda it: "gasolina" not in it["q"],))

unit("proporcionalidad", 8, "Q",
     "Resuelve problemas de proporcionalidad directa con números naturales usando tablas, el valor unitario, dobles, triples y mitades; interpreta escalas sencillas en mapas y planos",
     "Proporcionalidad: tablas y valor unitario", "Proporcionalidad",
     "Ejercicios de matemáticas de 5.º grado de primaria: tablas de proporcionalidad, valor unitario, regla de tres sencilla, razones y escalas. 100 ejercicios con respuestas.",
     "Busca el valor de 1", "Si una cantidad se duplica, la otra también.",
     ["Dos cantidades son <b>proporcionales</b> si al multiplicar una por un número, la otra se multiplica por el mismo número: 2 kg cuestan $60, 4 kg cuestan $120.",
      "El <b>valor unitario</b> es lo que corresponde a 1: si 5 cuadernos cuestan $90, uno cuesta 90 ÷ 5 = $18, y 8 cuestan 18 × 8 = $144.",
      "En una <b>escala</b> 1:100 000, 1 cm del mapa son 100 000 cm = 1 km en la realidad."],
     [("3 tortas cuestan $105. ¿Cuánto cuestan 7?", ["1 torta: 105 ÷ 3 = $35", "7 tortas: 35 × 7"], "$245"), ("Escala 1:50 000; 4 cm en el mapa", ["4 × 50 000 = 200 000 cm"], "2 km")],
     [["Sumar en lugar de multiplicar", "Si 2 → 60, entonces 4 → 120, no 62."], ["Olvidar pasar a la unidad", "Primero calcula el valor de 1."], ["Confundir las unidades de la escala", "100 000 cm = 1 km."]],
     [("¿Qué es el valor unitario?", "Es lo que corresponde a una unidad: el precio de un artículo, la distancia en una hora, etc. Con él se calcula cualquier otra cantidad."),
      ("¿Qué significa la escala 1:100?", "Que 1 cm en el dibujo representa 100 cm (1 m) en la realidad.")],
     [("Tablas de proporcionalidad", [(tabla, 20)]), ("Valor unitario", [(regla, 20)]), ("Razones", [(razon, 20)]), ("Escalas", [(escala, 20)]), ("Problemas", [(probl, 20)])],
     65008, lv=5)
