# -*- coding: utf-8 -*-
"""México 4.º grado: Cálculo de perímetro y área con cuadrículas y centímetros cuadrados (Cálculo de perímetro y área). Reutiliza España 4.º con otra semilla."""
from mx_common import src, unit
import gen_es_matematicas_4_perimetro_y_area as P4

cua, per, area, falta, prob = src("gen_es_matematicas_4_perimetro_y_area", 64220, "s1_cuadritos", "s2_perimetro", "s3_area", "s4_falta", "s5_problema")

unit("perimetro-y-area", 15, "A",
     "Calcula el perímetro y el área de figuras dibujadas en una cuadrícula y de rectángulos y cuadrados, usando el centímetro y el centímetro cuadrado; distingue entre perímetro y área; resuelve problemas",
     "Perímetro y área", "Perímetro y área",
     "Ejercicios de matemáticas de 4.º grado de primaria: perímetro y área en cuadrícula, centímetros cuadrados, rectángulos y cuadrados, la medida que falta y problemas. 100 ejercicios con respuestas.",
     "Perímetro: borde. Área: superficie", "El área se mide en cuadritos (cm²).",
     ["El <b>perímetro</b> es la medida del contorno: se suman todos los lados. Se mide en cm o m.",
      "El <b>área</b> es lo que ocupa la superficie: se cuentan los cuadritos de adentro. Un cuadrito de 1 cm de lado es un <b>centímetro cuadrado</b> (1 cm²).",
      "En un rectángulo, área = largo × ancho: 6 cm × 4 cm = 24 cm². Perímetro = 6 + 4 + 6 + 4 = 20 cm."],
     [("Rectángulo de 7 cm por 3 cm", ["perímetro: 7 + 3 + 7 + 3 = 20 cm", "área: 7 × 3 = 21 cm²"], "20 cm y 21 cm²"), ("Cuadrado de lado 5 cm", ["área: 5 × 5"], "25 cm²")],
     [["Confundir perímetro y área", "El perímetro se suma; el área se cuenta o se multiplica."], ["Olvidar dos lados del rectángulo", "Son 4 lados: 7 + 3 + 7 + 3."], ["Escribir cm en el área", "El área va en cm²."]],
     [("¿Qué diferencia hay entre perímetro y área?", "El perímetro mide el borde de la figura (en cm) y el área mide la superficie de adentro (en cm²)."),
      ("¿Cómo calculo el área de un rectángulo?", "Multiplica el largo por el ancho. Un rectángulo de 8 cm por 5 cm tiene 8 × 5 = 40 cm².")],
     [("Contar cuadritos", [(cua, 20)]), ("Perímetro", [(per, 20)]), ("Área", [(area, 20)]), ("La medida que falta", [(falta, 20)]), ("Problemas", [(prob, 20)])],
     64015, pic=P4.cuadricula(P4.rect_cells(6, 4)) if hasattr(P4, "rect_cells") else "", lv=4)
