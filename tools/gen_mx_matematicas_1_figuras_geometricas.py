# -*- coding: utf-8 -*-
"""México 1.er y 2.º grado: Figuras geométricas y sus características: nombres, lados y vértices, líneas rectas y curvas, polígonos. Reutiliza España 1.º/2.º (gen_es_matematicas_2_figuras_planas) con otra semilla."""
from mx_common import src, unit
from mx_12 import BIG, plain

T = {1: dict(std="Representa objetos con el tangram y otras figuras; nombra y describe figuras geométricas por su forma, número de lados y vértices",
             meta="Ejercicios de matemáticas de 1.er grado de primaria: círculo, triángulo, cuadrado y rectángulo, lados y vértices, líneas rectas y curvas. 100 ejercicios con respuestas.",
             think=["Las figuras tienen <b>lados</b> (las líneas del borde) y <b>vértices</b> (las esquinas donde se juntan dos lados).",
                    "El triángulo tiene 3 lados; el cuadrado y el rectángulo, 4. El círculo no tiene lados rectos ni vértices.",
                    "En el cuadrado los 4 lados miden lo mismo; en el rectángulo, dos son largos y dos son cortos."],
             ex=[("Una figura con 3 lados y 3 vértices", ["cuenta los lados"], "triángulo")]),
     2: dict(std="Construye composiciones con el tangram y el geoplano; clasifica y describe polígonos (triángulos, cuadriláteros, pentágonos, hexágonos y octágonos) por el número de lados y vértices",
             meta="Ejercicios de matemáticas de 2.º grado de primaria: triángulos, cuadriláteros, pentágonos, hexágonos y octágonos; lados, vértices y figuras en cuadrícula. 100 ejercicios con respuestas.",
             think=["Un <b>polígono</b> es una figura cerrada con lados rectos. Se nombra por el número de lados: triángulo (3), cuadrilátero (4), pentágono (5), hexágono (6), octágono (8).",
                    "Un polígono tiene tantos vértices como lados.",
                    "El círculo no es un polígono porque su borde es curvo."],
             ex=[("Figura con 6 lados", ["hexa = seis"], "hexágono"), ("¿Cuántos vértices tiene un pentágono?", ["tiene 5 lados"], "5")])}


def build(lv):
    t = T[lv]
    nom, lados, contar, saber, lineas = src("gen_es_matematicas_2_figuras_planas", 61000 + 1000 * lv + 910, "s_nombre", "s_lados", "s_contar", "s_saber", "s_lineas", lv=lv, mx_=BIG)
    pol = src("gen_es_matematicas_4_triangulos_y_cuadrilateros", 62911, "s4_poligonos", mx_=BIG, extra=(lambda it: not any(w in plain(it) for w in ("eneágono", "decágono", "heptágono", "diagonal", "regular")),)) if lv == 2 else None
    unit("figuras-geometricas", 9 if lv == 1 else 10, "F", t["std"], "Figuras geométricas", "Figuras geométricas", t["meta"], "Cuenta lados y vértices", "Un vértice es donde se juntan dos lados.",
         t["think"], t["ex"],
         [["Contar un lado dos veces", "Marca el lado donde empiezas."], ["Pensar que un cuadrado girado no es cuadrado", "Si gira, sigue siendo cuadrado."], ["Decir que el círculo tiene lados", "Su borde es curvo: no tiene lados ni vértices."]],
         [("¿Qué es un vértice?", "Es la esquina donde se juntan dos lados de una figura."), ("¿El cuadrado es un rectángulo?", "Sí: tiene 4 lados y 4 esquinas iguales como el rectángulo; además sus 4 lados miden lo mismo.")],
         [("Nombres de figuras", [(nom, 20)]), ("Lados y vértices", [(lados, 20)]), ("Contar figuras", [(contar, 20)]), ("¿Qué sabes de las figuras?", [(saber, 8), (nom, 12)]) if lv == 1 else ("Polígonos", [(pol, 8), (saber, 12)]), ("Líneas rectas y curvas", [(lineas, 20)])],
         60000 + 1000 * lv + 9, lv=lv)


if __name__ == "__main__":
    build(1)
