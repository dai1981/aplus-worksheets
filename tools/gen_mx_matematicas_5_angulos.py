# -*- coding: utf-8 -*-
"""México 5.º grado: Ángulos: medir con transportador, clasificar, ángulos en triángulos (Figuras geométricas y sus características). Reutiliza España 6.º (nivel 5.º) y 4.º con otra semilla."""
from mx_common import src, unit

medir, rel, tri, probl = src("gen_es_matematicas_6_angulos", 65315, "s1_medir", "s2_relaciones", "s3_triangulo", "s5_problema", lv=5)
transp, tipo, giros = src("gen_es_matematicas_4_angulos", 65215, "s2_transportador", "s1_tipo", "s4_giros")

unit("angulos", 13, "F",
     "Mide y traza ángulos con el transportador; clasifica ángulos en agudos, rectos, obtusos y llanos; calcula ángulos que faltan en triángulos y en giros",
     "Ángulos: medir y clasificar", "Ángulos",
     "Ejercicios de matemáticas de 5.º grado de primaria: medir ángulos con transportador, ángulos agudos, rectos y obtusos, giros, ángulos de un triángulo y problemas. 100 ejercicios con respuestas.",
     "Recto 90°, llano 180°", "Los ángulos de un triángulo suman 180°.",
     ["Un ángulo se mide en <b>grados</b> (°) con el <b>transportador</b>: pon el centro en el vértice y el 0 sobre un lado.",
      "Agudo: menos de 90°. Recto: 90°. Obtuso: entre 90° y 180°. Llano: 180°. Una vuelta completa: 360°.",
      "Los tres ángulos de un triángulo suman <b>180°</b>: si dos miden 60° y 70°, el tercero mide 180 − 130 = 50°."],
     [("Un triángulo tiene ángulos de 45° y 90°", ["45 + 90 = 135", "180 − 135"], "45°")],
     [["Leer la escala equivocada del transportador", "Empieza en el 0 que está sobre el lado."], ["Pensar que un ángulo más largo es mayor", "La abertura importa, no la longitud de los lados."], ["Sumar a 360° en un triángulo", "En un triángulo suman 180°."]],
     [("¿Cuánto mide un ángulo llano?", "180°: sus dos lados forman una línea recta. Es la mitad de una vuelta."),
      ("¿Cómo uso el transportador?", "Coloca su centro sobre el vértice, alinea el 0 con un lado del ángulo y lee el número por donde pasa el otro lado.")],
     [("Medir con transportador", [(transp, 20)]), ("Agudo, recto u obtuso", [(tipo, 10), (medir, 10)]), ("Giros y relaciones", [(giros, 8), (rel, 12)]), ("Ángulos de un triángulo", [(tri, 20)]), ("Problemas", [(probl, 20)])],
     65013, lv=5)
