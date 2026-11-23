# -*- coding: utf-8 -*-
"""México 5.º grado: Noción de volumen: contar cubos, volumen de prismas rectangulares; caras, aristas y vértices (Perímetro, área y noción de volumen). Reutiliza España 6.º (nivel 5.º) con otra semilla."""
from mx_common import src, unit

euler, cubos, formula, unid, probl = src("gen_es_matematicas_6_cuerpos_y_volumen", 65319, "s1_euler", "s2_volumen_cubos", "s3_formula", "s4_unidades", "s5_problema", lv=5)

unit("volumen", 12, "V",
     "Construye la noción de volumen contando cubos unitarios en prismas rectangulares; calcula el volumen como largo × ancho × alto; usa el centímetro cúbico; identifica caras, aristas y vértices de prismas y pirámides",
     "Volumen: cubos y prismas", "Volumen",
     "Ejercicios de matemáticas de 5.º grado de primaria: volumen contando cubos, volumen de prismas rectangulares, centímetros cúbicos, caras, aristas y vértices. 100 ejercicios con respuestas.",
     "Volumen = largo × ancho × alto", "Se mide en cubos: cm³, m³.",
     ["El <b>volumen</b> es el espacio que ocupa un cuerpo. Se mide contando cubos: un cubo de 1 cm de arista es un <b>centímetro cúbico</b> (1 cm³).",
      "En un prisma rectangular, cuenta los cubos de una capa (largo × ancho) y multiplica por el número de capas (alto): V = largo × ancho × alto.",
      "Un prisma con base de n lados tiene n + 2 caras; una pirámide, n + 1."],
     [("Caja de 5 cm × 4 cm × 3 cm", ["una capa: 5 × 4 = 20 cubos", "3 capas: 20 × 3"], "60 cm³")],
     [["Sumar las medidas", "5 + 4 + 3 no es el volumen: hay que multiplicar."], ["Escribir cm²", "El volumen va en cm³."], ["Contar solo los cubos que se ven", "También hay cubos escondidos detrás."]],
     [("¿Qué diferencia hay entre área y volumen?", "El área mide una superficie (cm²) y el volumen, el espacio que ocupa un cuerpo (cm³)."),
      ("¿Cómo cuento los cubos de un prisma?", "Cuenta los de una capa (largo × ancho) y multiplica por el número de capas.")],
     [("Contar cubos", [(cubos, 20)]), ("Volumen de prismas rectangulares", [(formula, 20)]), ("Unidades de volumen", [(unid, 20)]), ("Caras, aristas y vértices", [(euler, 20)]), ("Problemas", [(probl, 20)])],
     65012, lv=5)
