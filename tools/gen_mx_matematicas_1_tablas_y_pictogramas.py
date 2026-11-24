# -*- coding: utf-8 -*-
"""México 1.er y 2.º grado: Tablas y pictogramas (Organización e interpretación de datos): contar y clasificar, marcas de conteo, tablas, pictogramas y gráficas de barras sencillas. Reutiliza España 1.º/2.º (gen_es_matematicas_2_graficos) y 4.º (tablas y pictogramas hasta 100, solo 2.º) con otra semilla."""
from mx_common import src, unit
from mx_12 import BIG, q_le, all_le
from f_common import pictograph_svg
import es_pics as P

T = {1: dict(sort=12, std="Recolecta, organiza, representa e interpreta datos en tablas y pictogramas para responder preguntas de su entorno",
             meta="Ejercicios de matemáticas de 1.er grado de primaria: contar y clasificar, marcas de conteo, pictogramas y gráficas de barras sencillas. 100 ejercicios con respuestas.",
             kb="Cuenta de 5 en 5 con marcas", ks="Cuatro palitos y uno que los cruza.",
             think=["Para contar muchas cosas, sepáralas en grupos: las iguales juntas.", "Las <b>marcas de conteo</b> se hacen de 5 en 5: cuatro palitos y uno que los cruza.",
                    "En un <b>pictograma</b>, cada dibujo es una cosa. La fila más larga es la que tiene más."],
             ex=[("<s>||||</s> ||", ["Un grupo de 5 y 2 más"], "7"), ("5 perros y 3 gatos", ["5 − 3"], "2 perros más")]),
     2: dict(sort=13, std="Recolecta, registra, organiza e interpreta datos en tablas de frecuencia y pictogramas para responder preguntas de su entorno",
             meta="Ejercicios de matemáticas de 2.º grado de primaria: marcas de conteo, tablas, pictogramas con valor de 2 y gráficas de barras. 100 ejercicios con respuestas.",
             kb="Lee qué vale cada dibujo", ks="Si un dibujo vale 2, cuenta de 2 en 2.",
             think=["Con <b>marcas de conteo</b> contamos de 5 en 5. Luego escribimos el número en una <b>tabla</b>.",
                    "En un pictograma, lee qué vale cada dibujo: si cada dibujo vale 2, tres dibujos son 6.",
                    "Para saber cuántos más, resta: el mayor menos el menor."],
             ex=[("Cada dibujo vale 2 y hay 4 dibujos", ["2 + 2 + 2 + 2"], "8"), ("Fútbol 9 votos y béisbol 4 votos", ["9 − 4"], "5 votos más")])}


def build(lv):
    t = T[lv]
    seed = 61000 + 1000 * lv + 931
    picto, marcas, clasif, barras = src("gen_es_matematicas_2_graficos", seed, "s_picto", "s_marcas", "s_clasificar", "s_barras", lv=lv, mx_=BIG, extra=(all_le(20 if lv == 1 else 100),))
    if lv == 1:
        spec = [("Contar y clasificar", [(clasif, 20)]), ("Marcas de conteo", [(marcas, 20)]), ("Pictogramas", [(picto, 20)]), ("Gráficas de barras", [(barras, 20)]), ("Repaso", [(picto, 8), (clasif, 6), (barras, 6)])]
    else:
        tab, pic2 = src("gen_es_matematicas_4_graficos_y_tablas", seed + 1, "s3_tablas", "s2_picto", lv=4, mx_=BIG, extra=(q_le(100), all_le(100), lambda it: "moda" not in it["q"]))
        spec = [("Marcas de conteo y tablas", [(marcas, 6), (tab, 14)]), ("Pictogramas", [(picto, 20)]), ("Pictogramas: cada dibujo vale más", [(pic2, 20)]),
                ("Gráficas de barras", [(barras, 20)]), ("Repaso con datos", [(tab, 6), (pic2, 6), (barras, 8)])]
    mist = [["Contar dos veces el mismo dibujo", "Tacha cada dibujo al contarlo."], ["Leer mal la escala", "Mira de cuánto en cuánto va."], ["Confundir «cuántos más» con el total", "«Cuántos más» es una resta."]]
    faq = [("¿Qué son las marcas de conteo?", "Palitos que se hacen al contar. Cada cinco se agrupan: cuatro palitos y uno que los cruza."), ("¿Qué es un pictograma?", "Una gráfica con dibujos. Cada dibujo representa una cantidad.")]
    pic = P.pic(pictograph_svg([("apple", 5), ("star", 3), ("fish", 4)]), "pictograma: 5 manzanas, 3 estrellas, 4 peces")
    unit("tablas-y-pictogramas", t["sort"], "D", t["std"], "Tablas y pictogramas", "Tablas y pictogramas", t["meta"], t["kb"], t["ks"], t["think"], t["ex"], mist, faq, spec,
         60000 + 1000 * lv + 12, pic=pic, lv=lv)


if __name__ == "__main__":
    build(1)
