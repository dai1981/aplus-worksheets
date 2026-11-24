# -*- coding: utf-8 -*-
"""México 2.º grado de secundaria (Fase 6): Expresiones algebraicas de perímetros y áreas; leyes de los exponentes."""
import random
import re  # noqa: F401
import mx_s2 as S
from mx_common import src, unit, nomoney, noplanta  # noqa: F401

S.setup(random.Random(68105))
unit("expresiones-algebraicas-de-perimetros-y-areas", 5, "6IA",
     "Representa algebraicamente perímetros de figuras y áreas que generan expresiones cuadráticas; usa las propiedades de los exponentes en operaciones algebraicas",
     "Perímetros y áreas con expresiones algebraicas", "Perímetros y áreas algebraicos",
     "Ejercicios de matemáticas de 2.º grado de secundaria: expresiones algebraicas para perímetros y áreas de figuras, expresiones cuadráticas y leyes de los exponentes. 100 ejercicios con respuestas.",
     "Perímetro: suma. Área: multiplica.", "x · x = x²; el área da expresiones cuadráticas.",
     ["El <b>perímetro</b> de una figura con lados algebraicos es la suma de todos sus lados; reduce los términos semejantes: x + x + 3 + x + 3 = 3x + 6.",
      "El <b>área</b> de un rectángulo de lados x y (x + 4) es x(x + 4) = x² + 4x: aparece x², una expresión <b>cuadrática</b>.",
      "<b>Leyes de los exponentes</b>: xᵐ · xⁿ = xᵐ⁺ⁿ, xᵐ ÷ xⁿ = xᵐ⁻ⁿ, (xᵐ)ⁿ = xᵐⁿ."],
     [("Rectángulo x y x + 4: perímetro", ["2x + 2(x + 4)"], "4x + 8"), ("Rectángulo x y x + 4: área", ["x(x + 4)"], "x² + 4x"), ("(x + 2)(x + 3)", ["x² + 3x + 2x + 6"], "x² + 5x + 6")],
     [["Confundir perímetro y área", "El perímetro se suma (cm); el área se multiplica (cm²)."], ["Escribir x · x = 2x", "x · x = x²; x + x = 2x."], ["Olvidar multiplicar todos los términos", "(x + 2)(x + 3) tiene cuatro productos."]],
     [("¿Por qué el área tiene x²?", "Porque se multiplican dos longitudes que tienen x."), ("¿Puedo sumar 3x y x²?", "No: no son términos semejantes.")],
     [("Perímetros", [(lambda: S.alg_figuras("perim"), 20)]), ("Áreas", [(lambda: S.alg_figuras("area"), 20)]), ("Áreas que crecen", [(lambda: S.alg_figuras("cuad"), 20)]),
      ("Leyes de los exponentes", [(lambda: S.alg_figuras("exp"), 20)]), ("Repaso", [(S.alg_figuras, 20)])],
     68005, lv=8)
