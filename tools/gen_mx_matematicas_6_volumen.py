# -*- coding: utf-8 -*-
"""México 6.º grado: Volumen de prismas rectangulares con fórmula; unidades cúbicas y capacidad (Perímetro, área y noción de volumen). Reutiliza España 6.º con otra semilla."""
from mx_common import src, unit

cubos, formula, unid, probl = src("gen_es_matematicas_6_cuerpos_y_volumen", 66319, "s2_volumen_cubos", "s3_formula", "s4_unidades", "s5_problema", lv=6)

unit("volumen", 12, "V",
     "Calcula el volumen de prismas rectangulares y cubos con la fórmula largo × ancho × alto; usa el centímetro cúbico, el decímetro cúbico y el metro cúbico y su relación con el litro; resuelve problemas",
     "Volumen de prismas y unidades cúbicas", "Volumen",
     "Ejercicios de matemáticas de 6.º grado de primaria: volumen de cubos y prismas rectangulares, cm³, dm³ y m³, volumen y litros y problemas. 100 ejercicios con respuestas.",
     "V = largo × ancho × alto", "1 dm³ = 1 L; 1 m³ = 1 000 L.",
     ["El volumen de un prisma rectangular es <b>largo × ancho × alto</b>; el de un cubo, arista × arista × arista.",
      "Unidades: 1 dm³ = 1 000 cm³ y 1 m³ = 1 000 dm³. Cada unidad cúbica es 1 000 veces la siguiente más pequeña.",
      "Volumen y capacidad: 1 dm³ = 1 litro, 1 cm³ = 1 mL y 1 m³ = 1 000 L."],
     [("Caja de 20 cm × 15 cm × 10 cm", ["20 × 15 × 10"], "3 000 cm³ = 3 L"), ("Tinaco de 2 m × 1 m × 1.5 m", ["2 × 1 × 1.5 = 3 m³"], "3 000 L")],
     [["Sumar las medidas", "Hay que multiplicar las tres."], ["Usar 100 en lugar de 1 000", "1 dm³ = 1 000 cm³."], ["Mezclar unidades", "Pasa todo a la misma unidad antes de multiplicar."]],
     [("¿Cuántos litros caben en 1 m³?", "1 000 litros, porque 1 m³ = 1 000 dm³ y cada dm³ es un litro."),
      ("¿Cómo calculo el volumen de un cubo de 4 cm de arista?", "4 × 4 × 4 = 64 cm³.")],
     [("Contar cubos", [(cubos, 20)]), ("Volumen con fórmula", [(formula, 20)]), ("Unidades cúbicas", [(unid, 20)]), ("Volumen y litros", [(unid, 4), (formula, 8), (probl, 8)]), ("Problemas", [(probl, 12), (cubos, 8)])],
     66012, lv=6)
