# -*- coding: utf-8 -*-
"""México 5.º grado: Nociones de probabilidad: seguro, posible, imposible; registrar resultados en tablas de frecuencia (Fase 5). Reutiliza España 6.º (nivel 5.º) y 4.º con otra semilla."""
from mx_common import src, unit

lap, frec = src("gen_es_matematicas_6_probabilidad", 65322, "s1_laplace", "s4_frecuencia", lv=5)
suc, comp, frac, casos, exp = src("gen_es_matematicas_4_probabilidad", 65222, "s1_sucesos", "s2_comparar", "s3_fraccion", "s4_casos", "s5_experimento")

unit("probabilidad", 16, "B",
     "Identifica eventos seguros, posibles e imposibles; compara qué evento es más probable; registra los resultados de experimentos aleatorios en tablas de frecuencia y los usa para estimar la probabilidad",
     "Probabilidad: seguro, posible o imposible", "Probabilidad",
     "Ejercicios de matemáticas de 5.º grado de primaria: eventos seguros, posibles e imposibles, más o menos probable, casos posibles, experimentos y frecuencias. 100 ejercicios con respuestas.",
     "Favorables entre posibles", "Seguro: 1. Imposible: 0.",
     ["Un evento es <b>seguro</b> si siempre ocurre, <b>imposible</b> si nunca ocurre y <b>posible</b> si a veces ocurre.",
      "Es más probable lo que tiene más casos a favor: en una bolsa con 7 canicas rojas y 3 azules, sacar roja es más probable.",
      "La probabilidad se puede escribir como fracción: casos favorables / casos posibles = %s. Si repetimos un experimento muchas veces, la frecuencia se acerca a ese valor." % "7/10"],
     [("Dado: sacar un número par", ["casos favorables: 2, 4, 6 → 3", "casos posibles: 6"], "3/6 = 1/2")],
     [["Pensar que todo lo posible es igual de probable", "Cuenta los casos a favor."], ["Olvidar casos posibles", "Un dado tiene 6 caras."], ["Creer que lo que salió antes cambia lo siguiente", "La moneda no «recuerda»."]],
     [("¿Qué es un evento imposible?", "Uno que nunca puede ocurrir, como sacar un 7 con un dado normal. Su probabilidad es 0."),
      ("¿Para qué sirve una tabla de frecuencias en un experimento?", "Para anotar cuántas veces sale cada resultado y ver cuál ocurre más.")],
     [("Seguro, posible o imposible", [(suc, 20)]), ("¿Qué es más probable?", [(comp, 20)]), ("Casos posibles", [(casos, 10), (frac, 10)]), ("Probabilidad como fracción", [(lap, 20)]),
      ("Experimentos y frecuencias", [(exp, 8), (frec, 12)])],
     65016, lv=5)
