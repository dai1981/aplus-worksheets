# -*- coding: utf-8 -*-
"""México 1.er grado de secundaria (Fase 6): Longitud de la circunferencia y área del círculo (π ≈ 3.14)."""
import random
import mx_s1 as S
from mx_common import src, unit, nomoney, noplanta  # noqa: F401

S.setup(random.Random(67117))
pi, lon, area, inv, prob = src("gen_es_matematicas_6_longitud_y_area_del_circulo", 67461, "s1_pi", "s2_longitud", "s3_area", "s4_inversa", "s5_problema", lv=6, extra=(nomoney,))
arco = src("gen_es_matematicas_1eso_circunferencia_y_circulo", 67462, "s_arco", lv=1)

unit("perimetro-y-area-del-circulo", 17, "6ME",
     "Obtiene y aplica fórmulas, o usa otras estrategias, para calcular el perímetro y el área del círculo",
     "Perímetro y área del círculo", "Área del círculo",
     "Ejercicios de matemáticas de 1.er grado de secundaria: el número π, perímetro de la circunferencia, área del círculo, semicírculo, sector y problemas. 100 ejercicios con respuestas.",
     "P = π × d    A = π × r²", "Usa π ≈ 3.14.",
     ["El <b>perímetro</b> (longitud de la circunferencia) es π × diámetro = 2 × π × radio. <b>π</b> ≈ 3.14 es lo que cabe el diámetro en la circunferencia.",
      "El <b>área del círculo</b> es π × radio². Si te dan el diámetro, divide entre 2 primero.",
      "Un <b>semicírculo</b> tiene la mitad del área; un sector de n°, la fracción n/360 del círculo."],
     [("Radio 5 cm: perímetro", ["2 × 3.14 × 5"], "31.4 cm"), ("Radio 5 cm: área", ["3.14 × 25"], "78.5 cm²")],
     [["Usar el diámetro en π × r²", "Con d = 10, r = 5 y A = 3.14 × 25."], ["Elevar al cuadrado π × r", "Solo r va al cuadrado."], ["Confundir perímetro y área", "Perímetro en cm; área en cm²."]],
     [("¿Qué es π?", "El cociente entre la longitud de una circunferencia y su diámetro. Es el mismo para todos los círculos: 3.14159…"),
      ("¿Por qué el área usa r²?", "Si cortas el círculo en sectores y los acomodas, forman casi un rectángulo de base π × r y altura r.")],
     [("El número π", [(pi, 6), (lon, 7), (area, 7)]), ("Perímetro del círculo", [(lon, 20)]), ("Área del círculo", [(area, 20)]), ("Del perímetro o área al radio", [(inv, 12), (arco, 8)]), ("Problemas", [(prob, 20)])],
     67017, lv=7)
