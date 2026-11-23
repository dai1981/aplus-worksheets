# -*- coding: utf-8 -*-
"""México 6.º grado: Suma, resta, multiplicación y división de números decimales entre naturales (Suma y resta; Multiplicación y división). Reutiliza España 6.º con otra semilla."""
import re
from mx_common import src, unit, mx_text
import es_common as ES


def por_natural(it):
    t = re.sub(r"<[^>]*>", " ", it["q"] + " " + it["e"])
    return not re.search(r"\d\s(?::|÷)\s\d+,\d|dos factores", t)


sumar, por10, mult, probl = src("gen_es_matematicas_6_operaciones_con_decimales", 66309, "s1_sumar", "s2_por10", "s3_mult", "s5_problema", lv=6)
div = src("gen_es_matematicas_6_operaciones_con_decimales", 66309, "s4_div", lv=6, extra=(por_natural,))

unit("operaciones-con-decimales", 4, "P",
     "Resuelve sumas, restas y multiplicaciones con números decimales y divisiones de un decimal entre un natural; multiplica y divide entre 10, 100 y 1 000; resuelve problemas",
     "Operaciones con decimales", "Operaciones con decimales",
     "Ejercicios de matemáticas de 6.º grado de primaria: sumar, restar y multiplicar decimales, dividir decimales entre naturales, por 10, 100 y 1 000 y problemas. 100 ejercicios con respuestas.",
     "Cuenta las cifras decimales", "Al dividir, sube el punto al cociente.",
     ["Al multiplicar decimales, multiplica como si fueran naturales y pon en el resultado tantas cifras decimales como tengan los factores juntos: 2.4 × 1.5 = 3.60.",
      "Para dividir un decimal entre un natural, divide normalmente y pon el punto en el cociente cuando bajes la primera cifra decimal: 9.6 ÷ 4 = 2.4.",
      "Multiplicar por 10, 100 o 1 000 mueve el punto a la derecha; dividir, a la izquierda."],
     [("Calcula 3.25 × 1.2", ["325 × 12 = 3 900", "3 cifras decimales"], "3.9"), ("Calcula 13.5 ÷ 6", ["13 ÷ 6 = 2, sobra 1", "15 ÷ 6 = 2, sobran 3", "30 ÷ 6 = 5"], "2.25")],
     [["Contar mal las cifras decimales", "2.4 × 1.5 tiene dos cifras decimales: 3.60."], ["Olvidar el punto en el cociente", "9.6 ÷ 4 = 2.4, no 24."], ["Mover el punto hacia el lado equivocado", "× 100 hace el número más grande."]],
     [("¿Por qué 0.5 × 8 da menos que 8?", "Porque multiplicar por 0.5 es tomar la mitad: 0.5 × 8 = 4."),
      ("¿Cómo divido 7.2 entre 100?", "Mueve el punto dos lugares a la izquierda: 0.072.")],
     [("Sumar y restar decimales", [(sumar, 20)]), ("Por 10, 100 y 1 000", [(por10, 20)]), ("Multiplicar decimales", [(mult, 20)]), ("Dividir decimales entre naturales", [(div, 20)]), ("Problemas", [(probl, 20)])],
     66004, pic=mx_text(ES.vertical(["3.25", "1.2"], op="×")), lv=6)
