# -*- coding: utf-8 -*-
"""México 1.er grado (longitud y masa) y 2.º grado (longitud, masa y capacidad): comparar, estimar y medir con unidades no convencionales (Medición de longitud, masa y capacidad). Reutiliza España 1.º/2.º (gen_es_matematicas_2_medidas) con otra semilla, sin unidades convencionales."""
from mx_common import src, unit
from mx_12 import BIG, std_units

T = {1: dict(slug="longitud-y-masa", std="Compara longitudes de manera directa o indirecta con un intermediario (objetos o partes del cuerpo); estima qué objeto tiene más o menos masa sopesando y lo comprueba con una balanza; expresa las comparaciones con dibujos y números",
             title="Longitud y masa: comparar y medir", short="Longitud y masa",
             meta="Ejercicios de matemáticas de 1.er grado de primaria: más largo y más corto, medir con clips, cuadritos y pasos, más pesado y más ligero con la balanza. 100 ejercicios con respuestas.",
             kb="Mide con la misma unidad", ks="Empieza en el mismo punto para comparar.",
             think=["Para saber qué es más <b>largo</b>, pon los objetos uno junto al otro empezando en el mismo punto.",
                    "Para medir, cuenta cuántas veces cabe una unidad (un clip, un lápiz, un cuadrito, un paso) sin dejar huecos.",
                    "En la <b>balanza</b>, baja el lado del objeto más pesado."],
             ex=[("Una cinta mide 6 clips y otra 4 clips", ["6 &gt; 4"], "la primera es más larga")],
             mist=[["No empezar en el mismo punto", "Alinea los extremos antes de comparar."], ["Dejar huecos al medir", "Pon las unidades una tras otra."], ["Pensar que lo más grande pesa más", "Una pluma grande pesa menos que una piedra chica."]],
             faq=[("¿Por qué medimos con clips o pasos?", "Para aprender a medir: contamos cuántas veces cabe la unidad. Después usaremos la regla."), ("¿Cómo funciona una balanza?", "El lado que baja tiene el objeto más pesado; si queda derecha, pesan lo mismo.")]),
     2: dict(slug="longitud-masa-y-capacidad", std="Estima, mide, compara y ordena longitudes, capacidades y masas con unidades arbitrarias o de la comunidad; representa longitudes en la recta numérica y los resultados con dibujos y números",
             title="Longitud, masa y capacidad", short="Longitud, masa y capacidad",
             meta="Ejercicios de matemáticas de 2.º grado de primaria: medir con unidades como cuartas, pasos y cuadritos, comparar longitudes, masas y capacidades y problemas. 100 ejercicios con respuestas.",
             kb="Cuenta cuántas veces cabe la unidad", ks="Unidad más chica: número más grande.",
             think=["Para medir una longitud, elige una unidad (una cuarta, un paso, un lápiz) y cuenta cuántas veces cabe.",
                    "Si usas una unidad más pequeña, necesitas más: la mesa mide 5 cuartas o 10 lápices.",
                    "Para comparar capacidades, llena un recipiente y vacíalo en el otro, o cuenta cuántos vasos caben."],
             ex=[("Una jarra llena 6 vasos y otra 9 vasos", ["9 &gt; 6"], "la segunda tiene más capacidad")],
             mist=[["Comparar medidas con unidades distintas", "Usa la misma unidad para los dos."], ["Olvidar las partes que sobran", "Di «casi 5» o «un poco más de 4»."], ["Pensar que el recipiente más alto tiene más", "Uno ancho y bajo puede tener más."]],
             faq=[("¿Qué es una unidad de medida?", "Lo que usamos para medir y contar cuántas veces cabe: un paso, una cuarta, un vaso."), ("¿Por qué dos niños miden distinto con sus pasos?", "Porque sus pasos no son del mismo tamaño. Por eso se usan unidades iguales para todos.")])}


def build(lv):
    t = T[lv]
    largo, pesa, cabe, probl, metro = src("gen_es_matematicas_2_medidas", 61000 + 1000 * lv + 911, "s_largo", "s_pesa", "s_cabe", "s_problema", "s_metro", lv=lv, mx_=BIG, extra=(std_units,))
    if lv == 1:
        spec = [("Más largo y más corto", [(largo, 20)]), ("Medir y contar", [(largo, 20)]), ("Más pesado y más ligero", [(pesa, 20)]), ("Comparar y ordenar", [(largo, 10), (pesa, 10)]), ("Problemas", [(probl, 20)])]
    else:
        spec = [("Comparar longitudes", [(largo, 20)]), ("Medir con unidades", [(cabe, 20)]), ("Masa", [(pesa, 20)]), ("Unidades y estimación", [(cabe, 10), (largo, 10)]), ("Problemas", [(probl, 20)])]
    unit(t["slug"], 10 if lv == 1 else 11, "L", t["std"], t["title"], t["short"], t["meta"], t["kb"], t["ks"], t["think"], t["ex"], t["mist"], t["faq"], spec, 60000 + 1000 * lv + 10, lv=lv)


if __name__ == "__main__":
    build(1)
