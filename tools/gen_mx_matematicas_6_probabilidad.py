# -*- coding: utf-8 -*-
"""México 6.º grado: Nociones de probabilidad: eventos, casos posibles, diagramas de árbol, tablas de doble entrada y probabilidad como fracción (Fase 5). Reutiliza España 6.º y 4.º con otra semilla."""
from mx_common import src, unit

lap, formas, arbol, frec = src("gen_es_matematicas_6_probabilidad", 66323, "s1_laplace", "s2_formas", "s3_arbol", "s4_frecuencia", lv=6)
suc, comp, casos = src("gen_es_matematicas_4_probabilidad", 66223, "s1_sucesos", "s2_comparar", "s4_casos")

unit("probabilidad", 15, "B",
     "Identifica eventos seguros, probables e imposibles; cuenta los resultados posibles con diagramas de árbol y tablas de doble entrada; expresa la probabilidad como fracción y la compara con la frecuencia de un experimento",
     "Probabilidad y diagramas de árbol", "Probabilidad",
     "Ejercicios de matemáticas de 6.º grado de primaria: eventos seguros, probables e imposibles, diagramas de árbol, casos posibles, probabilidad como fracción y frecuencia. 100 ejercicios con respuestas.",
     "Favorables entre posibles", "Usa un árbol para contar todos los casos.",
     ["Un evento puede ser <b>seguro</b>, <b>probable</b> o <b>imposible</b>.",
      "Para contar todos los resultados posibles, usa un <b>diagrama de árbol</b> o una tabla de doble entrada: al lanzar dos monedas hay 4 resultados (AA, AS, SA, SS).",
      "La probabilidad de un evento es casos favorables ÷ casos posibles: sacar par con un dado es 3/6 = 1/2."],
     [("Dos monedas: ¿probabilidad de dos águilas?", ["casos: AA, AS, SA, SS → 4", "favorables: 1"], "1/4")],
     [["Olvidar casos en el árbol", "Cada rama se abre en todas las opciones."], ["Contar AS y SA como un solo caso", "Son dos resultados distintos."], ["Pensar que la frecuencia siempre es igual a la probabilidad", "Se parecen más cuando se repite muchas veces."]],
     [("¿Para qué sirve un diagrama de árbol?", "Para encontrar de forma ordenada todos los resultados posibles de un experimento con varios pasos."),
      ("¿Cuánto vale la probabilidad de un evento seguro?", "1. La de un evento imposible es 0, y la de los demás, un número entre 0 y 1.")],
     [("Seguro, probable o imposible", [(suc, 12), (comp, 8)]), ("Casos posibles", [(casos, 8), (formas, 12)]), ("Diagramas de árbol", [(arbol, 20)]), ("Probabilidad como fracción", [(lap, 20)]), ("Experimentos y frecuencias", [(frec, 20)])],
     66015, lv=6)
