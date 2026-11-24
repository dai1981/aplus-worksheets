# -*- coding: utf-8 -*-
"""México 2.º grado de secundaria (Fase 6): Moda, media aritmética, mediana y rango."""
import random
import re  # noqa: F401
import mx_s2 as S
from mx_common import src, unit, nomoney, noplanta  # noqa: F401

S.setup(random.Random(68117))
media, moda, prob = src("gen_es_matematicas_6_estadistica", 68431, "s1_media", "s2_moda_rango", "s5_problema", lv=6)
tab = src("gen_es_matematicas_1eso_estadistica", 68432, "s_tabla2", lv=1)
unit("media-mediana-moda-y-rango", 17, "6TC",
     "Usa e interpreta la moda, la media aritmética, la mediana y el rango de un conjunto de datos",
     "Media, mediana, moda y rango", "Media, mediana, moda y rango",
     "Ejercicios de matemáticas de 2.º grado de secundaria: calcular e interpretar media, mediana, moda y rango con listas de datos y tablas de frecuencias. 100 ejercicios con respuestas.",
     "Rango = mayor − menor", "Media, mediana y moda resumen los datos.",
     ["<b>Media</b>: suma de los datos ÷ número de datos. <b>Mediana</b>: el valor central con los datos ordenados. <b>Moda</b>: el más frecuente.",
      "El <b>rango</b> es la diferencia entre el dato mayor y el menor: dice qué tan dispersos están.",
      "Con una tabla de frecuencias, multiplica cada valor por su frecuencia para sumar."],
     [("4, 7, 7, 9, 13", ["Suma 40 ÷ 5 = 8", "Mediana 7", "Moda 7", "Rango 13 − 4"], "8, 7, 7 y 9"), ("Calificaciones 6, 8, 9, 10", ["Mediana (8 + 9) ÷ 2"], "8.5")],
     [["No ordenar antes de la mediana", "Primero ordena."], ["Olvidar la frecuencia en la tabla", "Un 5 que aparece 3 veces cuenta 15."], ["Confundir rango con el dato mayor", "Es mayor menos menor."]],
     [("¿Qué medida conviene si hay un dato muy grande?", "La mediana, porque casi no cambia con un dato extremo."), ("¿La media siempre es uno de los datos?", "No: puede ser un número que no aparece.")],
     [("La media", [(media, 20)]), ("Mediana, moda y rango", [(moda, 20)]), ("Tablas de frecuencias", [(tab, 20)]), ("Interpretar", [(prob, 10), (tab, 10)]), ("Problemas", [(prob, 10), (media, 5), (moda, 5)])],
     68017, lv=8)
