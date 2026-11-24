# -*- coding: utf-8 -*-
"""México, Pensamiento Matemático II (progresión 14): programación lineal con dos variables: restricciones, región factible, vértices y optimización."""
import random
import re
from mx_common import src, unit, num, NB

tra, pun, ver, opt_ = src("gen_es_matematicas_2ccss_programacion_lineal", 110314, "s_traducir", "s_punto", "s_vertices", "s_optimo")
_pro = src("gen_es_matematicas_2ccss_programacion_lineal", 110314, "s_problema")


def pro():
    """ganancias de España (pocos euros) → pesos ×100"""
    it = _pro()
    if it is None:
        return None
    f = lambda t: re.sub(r"\$(\d[\d" + NB + r"]*)", lambda m: "$" + num(int(m.group(1).replace(NB, "")) * 100), t)
    it = dict(it)
    it["q"], it["e"], it["c"] = f(it["q"]), f(it["e"]).replace("F = ", "F (en cientos de pesos) = "), [f(c) for c in it["c"]]
    return it
unit("programacion-lineal", 14, ("Funciones y sistemas", 14, "Programación lineal"),
     "Resuelve problemas de optimización con desigualdades lineales de dos incógnitas: plantea restricciones, traza la región factible y aplica el teorema fundamental de la programación lineal",
     "Programación lineal: región factible y óptimo", "Programación lineal",
     "Ejercicios de Pensamiento Matemático II: plantear restricciones, puntos de la región factible, vértices, máximo y mínimo de la función objetivo y problemas de producción. 100 ejercicios con respuestas.",
     "El óptimo está en un vértice", "Evalúa la función objetivo en cada vértice.",
     ["1. Define x e y. 2. Escribe las <b>restricciones</b> (desigualdades) y la <b>función objetivo</b> (lo que se quiere maximizar o minimizar).",
      "3. Dibuja la <b>región factible</b>: los puntos que cumplen todas las restricciones. 4. Encuentra sus <b>vértices</b>.",
      "<b>Teorema fundamental</b>: si hay óptimo, está en un vértice. Evalúa la función en cada vértice y elige el mayor (máximo) o el menor (mínimo)."],
     [("Máx F = 3x + 2y con x + y ≤ 4, x ≤ 3, x, y ≥ 0", ["Vértices (0, 0), (3, 0), (3, 1), (0, 4)", "F = 0, 9, 11, 8"], "máximo 11 en (3, 1)")],
     [["Olvidar x ≥ 0 e y ≥ 0", "No se producen cantidades negativas."], ["Evaluar solo un vértice", "Compara todos."], ["Confundir ≤ con ≥ al plantear", "«Como máximo» es ≤; «al menos» es ≥."]],
     [("¿Dónde se usa la programación lineal?", "En fábricas, transporte, dietas y horarios: para ganar lo más posible o gastar lo menos con recursos limitados."),
      ("¿Puede no haber solución?", "Sí, si la región factible está vacía o si no está acotada en la dirección que se quiere optimizar.")],
     [("Plantear restricciones", [(tra, 20)]), ("Región factible", [(pun, 20)]), ("Vértices", [(ver, 20)]), ("Máximos y mínimos", [(opt_, 20)]),
      ("Problemas", [(pro, 12), (opt_, 8)])],
     110014, lv=11)
