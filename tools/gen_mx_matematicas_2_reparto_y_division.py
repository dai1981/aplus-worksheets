# -*- coding: utf-8 -*-
"""México 2.º grado: Problemas de reparto con divisores menores que 10 y dividendos de dos cifras (Construcción de la noción de multiplicación y división). Reutiliza España 2.º/3.º con otra semilla."""
from mx_common import src, unit
from mx_12 import BIG

dib, grupos, ver, sobra, tabla, probl = src("gen_es_matematicas_2_repartos", 62801, "s_dibujo", "s_grupos", "s_ver", "s_sobra", "s_tabla", "s_problema", lv=2, mx_=BIG)
rep = src("gen_es_matematicas_3_division", 62802, "s_reparto", lv=2, mx_=BIG)

unit("reparto-y-division", 8, "P3",
     "Resuelve problemas de reparto en partes iguales con divisores menores que 10 y dividendos de dos cifras mediante diversos procedimientos (dibujos, sumas o restas repetidas, multiplicación)",
     "Reparto en partes iguales", "Reparto",
     "Ejercicios de matemáticas de 2.º grado de primaria: repartir en partes iguales con dibujos, formar grupos, cuánto sobra y problemas de reparto. 100 ejercicios con respuestas.",
     "Repartir es dar lo mismo a cada uno", "Lo que no alcanza a repartirse, sobra.",
     ["<b>Repartir</b> en partes iguales es dar la misma cantidad a cada uno: 12 dulces entre 3 niños son 4 para cada uno.",
      "Puedes repartir de uno en uno, o pensar en la multiplicación: ¿qué número por 3 da 12? 4 × 3 = 12.",
      "A veces <b>sobra</b> algo: 13 dulces entre 3 niños son 4 para cada uno y sobra 1."],
     [("15 canicas entre 5 niños", ["5 × 3 = 15"], "3 canicas cada uno"), ("17 hojas en grupos de 5", ["5 + 5 + 5 = 15", "sobran 2"], "3 grupos y sobran 2")],
     [["Dar más a unos que a otros", "Todos deben recibir lo mismo."], ["Olvidar lo que sobra", "Si no alcanza para todos, sobra."], ["Confundir cuántos grupos y cuántos en cada grupo", "Lee bien la pregunta."]],
     [("¿Qué hago con lo que sobra?", "Se queda sin repartir, porque no alcanza para dar uno más a cada persona."),
      ("¿Cómo me ayuda la multiplicación a repartir?", "Busca qué número multiplicado por el número de personas da el total: 20 entre 4 → 5 × 4 = 20, así que tocan 5.")],
     [("Repartir con dibujos", [(dib, 20)]), ("Formar grupos", [(grupos, 20)]), ("Grupos y división", [(ver, 10), (rep, 10)]), ("¿Cuánto sobra?", [(sobra, 20)]), ("Problemas", [(probl, 14), (tabla, 6)])],
     62008, lv=2)
