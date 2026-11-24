# -*- coding: utf-8 -*-
"""México 1.er grado de secundaria (Fase 6): Eventos de azar, espacio muestral, comparación de probabilidades y frecuencia relativa."""
import random
import re
import mx_s1 as S
from mx_common import src, unit, nomoney, noplanta  # noqa: F401

S.setup(random.Random(67121))
MON = [("{cara, cruz, canto}", "{águila, sol, canto}"), ("{cara, cruz}", "{águila, sol}"), ("{cara}", "{águila}"), ("caras", "águilas"), ("cara", "águila"), ("cruces", "soles"), ("cruz", "sol")]
con, lap, fre, cont = src("gen_es_matematicas_1eso_probabilidad", 67501, "s_conceptos", "s_laplace", "s_frecuencia", "s_contrario", lv=1, rep=MON, extra=(lambda it: " y 1 son" not in it["q"] and not re.search(r"(?<![\d.])1 (bolas|negras|rojas|azules|verdes|blancas|amarillas)", it["q"]),))

unit("probabilidad", 21, "6AZ",
     "Compara cualitativamente dos o más eventos a partir de sus resultados posibles («es más probable que», «es menos probable que»); identifica eventos de azar, determina el espacio muestral y registra resultados de experimentos en tablas de frecuencia",
     "Probabilidad: azar y espacio muestral", "Probabilidad",
     "Ejercicios de matemáticas de 1.er grado de secundaria: eventos de azar, espacio muestral, comparar probabilidades, probabilidad clásica y frecuencial con dados, monedas, urnas y ruletas. 100 ejercicios con respuestas.",
     "Favorables ÷ posibles", "Si hay más casos favorables, es más probable.",
     ["Un <b>experimento aleatorio</b> es aquel cuyo resultado no se puede predecir (lanzar un dado). El <b>espacio muestral</b> es la lista de todos los resultados posibles.",
      "Si todos los resultados son igual de probables, la probabilidad de un evento es casos favorables ÷ casos posibles (entre 0 y 1).",
      "La <b>frecuencia relativa</b> de un experimento repetido muchas veces se acerca a la probabilidad teórica."],
     [("Sacar par en un dado", ["Favorables: 2, 4, 6", "Posibles: 6"], "3/6 = 1/2"), ("Urna con 5 rojas y 3 azules", ["5 &gt; 3"], "es más probable roja")],
     [["Olvidar resultados del espacio muestral", "Al lanzar dos monedas hay 4 resultados: AA, AS, SA, SS."], ["Dar probabilidades mayores que 1", "La probabilidad está entre 0 (imposible) y 1 (seguro)."], ["Pensar que «ya toca»", "Cada lanzamiento de una moneda es independiente."]],
     [("¿Qué es un evento seguro?", "Uno que siempre ocurre; su probabilidad es 1. Un evento imposible tiene probabilidad 0."),
      ("¿Qué diferencia hay entre probabilidad frecuencial y teórica?", "La frecuencial sale de los resultados de un experimento; la teórica, de contar los casos posibles.")],
     [("Azar y espacio muestral", [(con, 12), (lambda: S.az_compara("escala"), 8)]), ("¿Qué es más probable?", [(lambda: S.az_compara("urna", "dado", "ruleta"), 20)]), ("Probabilidad clásica", [(lap, 20)]), ("Eventos contrarios", [(cont, 20)]), ("Frecuencia relativa", [(fre, 20)])],
     67021, lv=7)
