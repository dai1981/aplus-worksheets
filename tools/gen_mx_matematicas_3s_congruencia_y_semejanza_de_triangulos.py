# -*- coding: utf-8 -*-
"""México 3.er grado de secundaria (Fase 6): Criterios de congruencia y semejanza, razón de semejanza, teorema de Tales y escalas."""
import random
import re  # noqa: F401
import mx_s2 as S
from mx_common import src, unit, nomoney, noplanta  # noqa: F401

S.setup(random.Random(69110))
raz, tal, esc, cri, prob = src("gen_es_matematicas_2eso_semejanza", 69361, "s_razon", "s_tales", "s_escala", "s_criterios", "s_problema", lv=2, extra=(nomoney,))
unit("congruencia-y-semejanza-de-triangulos", 10, "6CF",
     "Aplica los criterios de congruencia y semejanza de triángulos; usa la razón de semejanza, el teorema de Tales y escalas",
     "Congruencia y semejanza de triángulos", "Semejanza de triángulos",
     "Ejercicios de matemáticas de 3.er grado de secundaria: criterios de congruencia y semejanza, razón de semejanza, teorema de Tales, escalas y problemas de alturas. 100 ejercicios con respuestas.",
     "Semejantes: lados proporcionales", "Congruentes: misma forma y mismo tamaño.",
     ["Dos triángulos son <b>congruentes</b> si son iguales (criterios LLL, LAL, ALA). Son <b>semejantes</b> si tienen los mismos ángulos y lados proporcionales.",
      "La <b>razón de semejanza</b> k compara lados correspondientes: si k = 3, cada lado es el triple. Los perímetros se multiplican por k y las áreas por k².",
      "<b>Teorema de Tales</b>: si varias paralelas cortan a dos rectas, los segmentos que determinan son proporcionales."],
     [("Lados 4, 6, 8 y 6, 9, 12", ["6/4 = 9/6 = 12/8 = 1.5"], "semejantes, k = 1.5"), ("Escala 1:200, 3.5 cm", ["3.5 × 200 = 700 cm"], "7 m")],
     [["Restar en vez de dividir para la razón", "La semejanza es multiplicativa."], ["Multiplicar el área por k", "El área se multiplica por k²."], ["Comparar lados que no se corresponden", "Ordena los lados de menor a mayor."]],
     [("¿Todos los triángulos equiláteros son semejantes?", "Sí: todos tienen ángulos de 60°."), ("¿Cómo se mide un edificio con su sombra?", "Con triángulos semejantes: tu estatura es a tu sombra como la altura del edificio es a su sombra.")],
     [("Criterios", [(cri, 8), (tal, 6), (esc, 6)]), ("Razón de semejanza", [(raz, 20)]), ("Teorema de Tales", [(tal, 20)]), ("Escalas", [(esc, 20)]), ("Problemas", [(prob, 20)])],
     69010, lv=9)
