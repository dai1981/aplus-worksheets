# -*- coding: utf-8 -*-
"""México 1.er grado de secundaria (Fase 6): Frecuencia absoluta y relativa; media, mediana y moda."""
import random
import mx_s1 as S
from mx_common import src, unit, nomoney, noplanta  # noqa: F401

S.setup(random.Random(67120))
media, moda, prob = src("gen_es_matematicas_6_estadistica", 67491, "s1_media", "s2_moda_rango", "s5_problema", lv=6)
tab = src("gen_es_matematicas_1eso_estadistica", 67492, "s_tabla2", lv=1)

unit("frecuencias-y-medidas-de-tendencia-central", 20, "6TC",
     "Determina e interpreta la frecuencia absoluta, la frecuencia relativa, la media, la mediana y la moda en un conjunto de datos",
     "Frecuencias, media, mediana y moda", "Media, mediana y moda",
     "Ejercicios de matemáticas de 1.er grado de secundaria: frecuencia absoluta y relativa, media, mediana, moda y rango con datos y tablas. 100 ejercicios con respuestas.",
     "Media: suma ÷ cantidad de datos", "Mediana: el de en medio, con los datos ordenados.",
     ["La <b>frecuencia absoluta</b> es cuántas veces aparece un dato; la <b>relativa</b> es esa cantidad dividida entre el total (como fracción, decimal o %).",
      "<b>Media</b>: suma todos los datos y divide entre cuántos son. <b>Mediana</b>: el valor central de los datos ordenados (si son pares, el promedio de los dos centrales).",
      "<b>Moda</b>: el dato que más se repite. El <b>rango</b> (máximo − mínimo) muestra qué tan dispersos están."],
     [("6, 8, 8, 9, 14", ["Suma 45 ÷ 5"], "media 9"), ("Mediana de 3, 9, 4, 7", ["Ordenados: 3, 4, 7, 9", "(4 + 7) ÷ 2"], "5.5")],
     [["No ordenar para la mediana", "La mediana de 9, 2, 5 es 5, no 2."], ["Dividir entre un número equivocado", "Cuenta todos los datos, también los repetidos."], ["Confundir moda con el número mayor", "La moda es el más frecuente."]],
     [("¿Cuál conviene usar?", "La media usa todos los datos; la mediana no cambia mucho con un dato muy grande o muy pequeño; la moda sirve para datos que no son números."),
      ("¿Puede haber dos modas?", "Sí, si dos datos se repiten la misma cantidad de veces (bimodal).")],
     [("Frecuencia absoluta y relativa", [(tab, 20)]), ("La media", [(media, 20)]), ("Mediana, moda y rango", [(moda, 20)]), ("Interpretar datos", [(prob, 10), (tab, 10)]), ("Problemas", [(prob, 10), (media, 5), (moda, 5)])],
     67020, lv=7)
