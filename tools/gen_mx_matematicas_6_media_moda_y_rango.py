# -*- coding: utf-8 -*-
"""México 6.º grado: Media aritmética, moda y rango (Organización e interpretación de datos). Reutiliza España 6.º con otra semilla."""
from mx_common import src, unit, keep

media, mr, probl = src("gen_es_matematicas_6_estadistica", 66322, "s1_media", "s2_moda_rango", "s5_problema", lv=6, extra=(lambda it: "mediana" not in it["q"] + it["e"],))
moda = keep(mr, lambda it: "moda" in it["q"])
rango = keep(mr, lambda it: "rango" in it["q"])

unit("media-moda-y-rango", 14, "D",
     "Calcula e interpreta la media aritmética, la moda y el rango de un conjunto de datos; decide cuál representa mejor los datos y resuelve problemas",
     "Media, moda y rango", "Media, moda y rango",
     "Ejercicios de matemáticas de 6.º grado de primaria: calcular la media (promedio), la moda y el rango de un conjunto de datos y problemas. 100 ejercicios con respuestas.",
     "Media = suma ÷ número de datos", "Moda: el que más se repite. Rango: mayor − menor.",
     ["La <b>media</b> (promedio) se calcula sumando todos los datos y dividiendo entre cuántos datos hay: (7 + 9 + 8) ÷ 3 = 8.",
      "La <b>moda</b> es el dato que más se repite. El <b>rango</b> es la diferencia entre el dato mayor y el menor.",
      "La media puede no ser uno de los datos; la moda siempre lo es."],
     [("Calificaciones: 8, 9, 7, 10, 6", ["suma: 40", "40 ÷ 5"], "media 8"), ("Datos: 3, 5, 5, 9, 2", ["5 aparece dos veces", "9 − 2"], "moda 5, rango 7")],
     [["Dividir entre un número equivocado", "Divide entre la cantidad de datos."], ["Confundir moda y media", "La moda es el que más se repite."], ["Calcular el rango con los primeros datos", "Es el mayor menos el menor."]],
     [("¿Qué es el promedio?", "Es la media aritmética: la suma de los datos dividida entre el número de datos. Sirve para repartir el total en partes iguales."),
      ("¿Qué indica el rango?", "Cuánto varían los datos: si es grande, los datos están muy separados.")],
     [("La media", [(media, 20)]), ("La moda", [(moda, 20)]), ("El rango", [(rango, 20)]), ("Media, moda y rango", [(media, 10), (mr, 10)]), ("Problemas", [(probl, 20)])],
     66014, lv=6)
