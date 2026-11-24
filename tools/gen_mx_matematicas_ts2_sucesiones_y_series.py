# -*- coding: utf-8 -*-
"""México, Temas Selectos de Matemáticas II (progresión 2): sucesiones y series: límite y convergencia, aritméticas, geométricas, Fibonacci y Sierpiński."""
import random
import mx_tsm as S
from mx_common import src, unit

S.setup(random.Random(140102))
ari, geo, sum_ = src("gen_es_matematicas_3eso_sucesiones", 140302, "s_aritmetica", "s_geometrica", "s_suma", lv=3)
unit("sucesiones-y-series", 2, ("Sucesiones y sistemas dinámicos", 2, "Sucesiones y series"),
     "Analiza sucesiones y series: límite y convergencia, progresiones aritméticas y geométricas, series geométricas infinitas, Fibonacci y el triángulo de Sierpiński",
     "Sucesiones, series y convergencia", "Sucesiones y series",
     "Ejercicios de Temas Selectos de Matemáticas II: límite de una sucesión, progresiones aritméticas y geométricas, sumas, series geométricas infinitas, Fibonacci y Sierpiński. 100 ejercicios con respuestas.",
     "S = a ÷ (1 − r), si |r| < 1", "Una serie infinita puede dar un número finito.",
     ["Una <b>sucesión</b> converge si sus términos se acercan a un número (su límite). Por ejemplo (2n + 1)/n → 2.",
      "<b>Aritmética</b>: aₙ = a₁ + (n − 1)d. <b>Geométrica</b>: aₙ = a₁·rⁿ⁻¹. Una <b>serie</b> es la suma de los términos.",
      "La serie geométrica infinita converge si |r| &lt; 1: S = a₁ ÷ (1 − r). En Sierpiński el área tiende a 0 mientras el perímetro crece sin límite."],
     [("4 + 2 + 1 + 1/2 + …", ["a = 4, r = 1/2", "S = 4 ÷ (1/2)"], "8")],
     [["Usar la fórmula infinita con |r| ≥ 1", "Esa serie no converge."], ["Confundir sucesión con serie", "La serie es la suma."], ["Creer que si los términos van a 0 la serie converge", "La serie armónica 1 + 1/2 + 1/3 + … diverge."]],
     [("¿Qué es la razón áurea?", "φ ≈ 1.618, el número al que se acercan los cocientes de términos de Fibonacci."), ("¿Por qué 0.999… = 1?", "Porque es la serie 0.9 + 0.09 + … = 0.9 ÷ (1 − 0.1) = 1.")],
     [("Límite de una sucesión", [(lambda: S.u2("lim"), 20)]), ("Progresiones aritméticas", [(ari, 12), (sum_, 8)]), ("Progresiones geométricas", [(geo, 20)]),
      ("Series infinitas", [(lambda: S.u2("serie"), 14), (lambda: S.u2("converge"), 6)]), ("Fibonacci y Sierpiński", [(lambda: S.u2("fib"), 12), (lambda: S.u2("sierp"), 8)])],
     140002, lv=14)
