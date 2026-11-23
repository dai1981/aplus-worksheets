# -*- coding: utf-8 -*-
"""
México 3.er grado de primaria: Números hasta 9 999 (Estudio de los números, Fase 4)
Contar, leer y escribir números de hasta cuatro cifras, valor posicional (UM, C, D, U), sucesiones, pares e impares.
Reutiliza los generadores de España (3.º de Primaria) con otra semilla y los pasa a México (mx_common.src).
"""
from mx_common import src, unit, bloques_mx

M = "gen_es_matematicas_3_numeros"
contar, letra_, valor, series, par = src(M, 63101, "s1_contar", "s2_letra", "s3_valor", "s4_series", "s5_par", lv=3)

unit("numeros-hasta-9999", 1, "N",
     "Cuenta, lee y escribe números de hasta cuatro cifras; valor posicional de unidades, decenas, centenas y unidades de millar; sucesiones numéricas; números pares e impares",
     "Los números hasta el 9 999", "Números hasta el 9 999",
     "Ejercicios de matemáticas de 3.er grado de primaria: leer y escribir números hasta el 9 999, valor posicional, sucesiones, pares e impares. 100 ejercicios con respuestas.",
     "UM, C, D y U", "Si falta un orden, escribe 0.",
     ["10 centenas forman una <b>unidad de millar</b> (1 000).",
      "En 4 352, el 4 vale 4 000, el 3 vale 300, el 5 vale 50 y el 2 vale 2. Si falta un orden, escribe 0: «cuatro mil sesenta» = 4 060.",
      "Los números <b>pares</b> terminan en 0, 2, 4, 6 u 8; los <b>impares</b>, en 1, 3, 5, 7 o 9."],
     [("Escribe «cuatro mil sesenta»", ["4 UM, 0 C, 6 D, 0 U"], "4 060"), ("¿Qué número sigue después de 3 999?", ["Sumamos 1"], "4 000")],
     [["Olvidar el cero", "4 060, no 460."], ["Confundir la cifra con su valor", "En 4 352, el 4 vale 4 000."], ["Contar mal al cambiar de millar", "Después de 2 999 va 3 000."]],
     [("¿Cómo se escribe un número con un cero en medio?", "Se escribe un 0 en el lugar que no se nombra. «Cuatro mil sesenta» no tiene centenas ni unidades: 4 060."),
      ("¿Cómo sé si un número es par?", "Mira la última cifra: si es 0, 2, 4, 6 u 8, el número es par.")],
     [("Contar y representar números", [(contar, 20)]), ("Leer y escribir números", [(letra_, 20)]), ("Valor de las cifras", [(valor, 20)]),
      ("Antes, después y sucesiones", [(series, 20)]), ("Pares, impares y decenas", [(par, 20)])],
     63001, pic=bloques_mx(0, 3, 5, 2))
