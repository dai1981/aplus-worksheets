# -*- coding: utf-8 -*-
"""México 3.er grado de secundaria (Fase 6): Teorema de Pitágoras."""
import random
import re  # noqa: F401
import mx_s2 as S
from mx_common import src, unit, nomoney, noplanta  # noqa: F401

S.setup(random.Random(69115))
hip, cat, rect, figs, prob = src("gen_es_matematicas_2eso_teorema_de_pitagoras", 69391, "s_hip", "s_cateto", "s_rect", "s_figuras", "s_problema", lv=2, extra=(nomoney,))
unit("teorema-de-pitagoras", 15, "6ME",
     "Formula, justifica y usa el teorema de Pitágoras",
     "Teorema de Pitágoras", "Teorema de Pitágoras",
     "Ejercicios de matemáticas de 3.er grado de secundaria: hipotenusa, catetos, reconocer triángulos rectángulos, diagonales y problemas con el teorema de Pitágoras. 100 ejercicios con respuestas.",
     "a² + b² = c²", "c es la hipotenusa, el lado mayor.",
     ["En un <b>triángulo rectángulo</b>, el cuadrado de la hipotenusa es igual a la suma de los cuadrados de los catetos: c² = a² + b².",
      "Para la <b>hipotenusa</b>: c = √(a² + b²). Para un <b>cateto</b>: a = √(c² − b²).",
      "Si tres lados cumplen a² + b² = c², el triángulo es rectángulo (como 3, 4, 5 o 5, 12, 13)."],
     [("Catetos 6 y 8", ["36 + 64 = 100", "√100"], "10"), ("Hipotenusa 13, cateto 5", ["169 − 25 = 144"], "12")],
     [["Sumar los lados sin elevar al cuadrado", "6 + 8 ≠ 10 por suma: 6² + 8² = 10²."], ["Sumar para un cateto", "Para un cateto se resta: c² − b²."], ["Usarlo en cualquier triángulo", "Solo en triángulos rectángulos."]],
     [("¿Para qué sirve en la vida real?", "Para calcular diagonales de pantallas, la longitud de una escalera o distancias en un mapa."), ("¿Cómo se justifica?", "Con cuadrados sobre cada lado: el área del cuadrado grande es la suma de las de los pequeños.")],
     [("Calcular la hipotenusa", [(hip, 20)]), ("Calcular un cateto", [(cat, 20)]), ("¿Es rectángulo?", [(rect, 20)]), ("Diagonales y figuras", [(figs, 20)]), ("Problemas", [(prob, 20)])],
     69015, lv=9)
