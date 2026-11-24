# -*- coding: utf-8 -*-
"""México 2.º grado de secundaria (Fase 6): Probabilidad en fracción, decimal y porcentaje; eventos complementarios y mutuamente excluyentes."""
import random
import re  # noqa: F401
import mx_s2 as S
from mx_common import src, unit, nomoney, noplanta  # noqa: F401

S.setup(random.Random(68118))
MON = [("{cara, cruz, canto}", "{águila, sol, canto}"), ("{cara, cruz}", "{águila, sol}"), ("caras", "águilas"), ("cara", "águila"), ("cruces", "soles"), ("cruz", "sol")]
cont, lap = src("gen_es_matematicas_1eso_probabilidad", 68441, "s_contrario", "s_laplace", lv=1, rep=MON, extra=(lambda it: " y 1 son" not in it["q"] and not re.search(r"(?<![\d.])1 (bolas|negras|rojas|azules|verdes|blancas|amarillas)", it["q"]),))
unit("probabilidad-de-eventos", 18, "6AZ",
     "Analiza la probabilidad y su equivalencia en decimales, fracciones y porcentajes; resuelve problemas con eventos complementarios y mutuamente excluyentes con la regla de la suma",
     "Eventos complementarios y excluyentes", "Probabilidad de eventos",
     "Ejercicios de matemáticas de 2.º grado de secundaria: probabilidad en fracción, decimal y porcentaje, eventos complementarios, mutuamente excluyentes y regla de la suma. 100 ejercicios con respuestas.",
     "P(A o B) = P(A) + P(B)", "Si A y B no pueden ocurrir a la vez.",
     ["La probabilidad se puede escribir como fracción, decimal o porcentaje: 1/4 = 0.25 = 25 %.",
      "Dos eventos son <b>complementarios</b> si uno es «no ocurre el otro»: P(no A) = 1 − P(A).",
      "Dos eventos son <b>mutuamente excluyentes</b> si no pueden ocurrir al mismo tiempo; entonces P(A o B) = P(A) + P(B) (<b>regla de la suma</b>)."],
     [("P(lluvia) = 0.3", ["1 − 0.3"], "P(no lluvia) = 0.7"), ("Dado: 1 o 6", ["1/6 + 1/6"], "1/3")],
     [["Sumar eventos que no son excluyentes", "«Par» y «mayor que 3» comparten el 4 y el 6."], ["Dar probabilidades mayores que 1", "Siempre entre 0 y 1."], ["Confundir complementario con excluyente", "Complementarios suman 1; excluyentes solo no ocurren juntos."]],
     [("¿Todos los eventos complementarios son excluyentes?", "Sí; pero no todos los excluyentes son complementarios."), ("¿Cómo paso de fracción a porcentaje?", "Divide y multiplica por 100: 3/8 = 0.375 = 37.5 %.")],
     [("Fracción, decimal y porcentaje", [(lambda: S.prob2("formas"), 20)]), ("Eventos complementarios", [(lambda: S.prob2("comp"), 12), (cont, 8)]), ("¿Son excluyentes?", [(lambda: S.prob2("no_excl"), 6), (lap, 14)]),
      ("Regla de la suma", [(lambda: S.prob2("excl"), 20)]), ("Repaso", [(S.prob2, 12), (lap, 8)])],
     68018, lv=8)
