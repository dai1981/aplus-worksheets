# -*- coding: utf-8 -*-
"""México 3.er grado de secundaria (Fase 6): Regla del producto para eventos independientes y juegos justos."""
import random
import re  # noqa: F401
import mx_s2 as S
from mx_common import src, unit, nomoney, noplanta  # noqa: F401

S.setup(random.Random(69119))
MON = [("{cara, cruz, canto}", "{águila, sol, canto}"), ("{cara, cruz}", "{águila, sol}"), ("caras", "águilas"), ("cara", "águila"), ("cruces", "soles"), ("cruz", "sol")]
arb, tab = src("gen_es_matematicas_1eso_probabilidad", 69431, "s_arbol", "s_tabla", lv=3, rep=MON, extra=(lambda it: "condicion" not in it["q"] and "sabiendo" not in it["q"],))
unit("eventos-independientes-y-juegos-justos", 19, "6AZ",
     "Calcula la probabilidad de dos eventos independientes con la regla del producto e indaga las condiciones para que un juego de azar sea justo",
     "Eventos independientes y juegos justos", "Eventos independientes",
     "Ejercicios de matemáticas de 3.er grado de secundaria: eventos independientes, regla del producto, diagramas de árbol, tablas de doble entrada y juegos justos. 100 ejercicios con respuestas.",
     "P(A y B) = P(A) × P(B)", "Si un evento no influye en el otro.",
     ["Dos eventos son <b>independientes</b> si el resultado de uno no cambia la probabilidad del otro (lanzar una moneda y un dado).",
      "<b>Regla del producto</b>: P(A y B) = P(A) × P(B). Dos águilas seguidas: 1/2 × 1/2 = 1/4.",
      "Un juego es <b>justo</b> si todos los jugadores tienen la misma probabilidad de ganar. Para saberlo, cuenta los resultados favorables de cada uno."],
     [("Dado y moneda: 6 y sol", ["1/6 × 1/2"], "1/12"), ("Par gana Ana, impar gana Beto", ["3/6 y 3/6"], "juego justo")],
     [["Sumar en lugar de multiplicar", "«Y» con independientes se multiplica."], ["Creer que el resultado anterior influye", "Una moneda no «recuerda»."], ["Contar mal los resultados", "Con dos dados hay 36 combinaciones."]],
     [("¿Cómo hago justo un juego que no lo es?", "Cambiando las reglas o los puntos para que cada jugador tenga la misma probabilidad (o la misma ganancia esperada)."), ("¿Para qué sirve el diagrama de árbol?", "Para ver todas las combinaciones y multiplicar por cada rama.")],
     [("Regla del producto", [(lambda: S.prob3("ind"), 20)]), ("Monedas y dados", [(lambda: S.prob3("dos_mon", "dado_mon"), 8), (lambda: S.prob3("ind"), 12)]), ("Diagramas de árbol y tablas", [(arb, 14), (lambda: S.prob3("ind"), 6)]),
      ("¿Es justo el juego?", [(lambda: S.prob3("justo"), 6), (lambda: S.prob3("ind"), 14)]), ("Repaso", [(lambda: S.prob3("ind"), 14), (arb, 6)])],
     69019, lv=9)
