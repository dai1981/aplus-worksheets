# -*- coding: utf-8 -*-
"""México, Temas Selectos de Matemáticas I (progresión 1): ángulos, semejanza, congruencia, autosimilitud y razones trigonométricas en el triángulo rectángulo."""
import random
import mx_tsm as S
from mx_common import src, unit, nomoney

S.setup(random.Random(130101))
raz, res, pro = src("gen_es_matematicas_4eso_trigonometria", 130301, "s_razones", "s_resolver", "s_problema", lv=4)
sem = src("gen_es_matematicas_2eso_semejanza", 130311, "s_razon", lv=2, extra=(nomoney,))
unit("geometria-y-razones-trigonometricas", 1, ("Geometría y trigonometría", 1, "Geometría básica y razones trigonométricas"),
     "Aplica ángulos, semejanza, congruencia y autosimilitud, y las razones trigonométricas seno, coseno y tangente para resolver triángulos rectángulos",
     "Semejanza y razones trigonométricas", "Razones trigonométricas",
     "Ejercicios de Temas Selectos de Matemáticas I: seno, coseno y tangente, calcular lados y ángulos de triángulos rectángulos, semejanza y problemas de alturas. 100 ejercicios con respuestas.",
     "sen = op/hip,  cos = ady/hip", "tan = op/ady. Vienen de la semejanza.",
     ["Todos los triángulos rectángulos con el mismo ángulo agudo α son <b>semejantes</b>, por eso sus razones entre lados son fijas.",
      "<b>sen α</b> = cateto opuesto ÷ hipotenusa; <b>cos α</b> = cateto adyacente ÷ hipotenusa; <b>tan α</b> = opuesto ÷ adyacente.",
      "Para un ángulo con sus lados se usa la inversa: α = tan⁻¹(opuesto ÷ adyacente). En figuras semejantes, las áreas se multiplican por k²."],
     [("Escalera de 5 m a 60° del suelo", ["altura = 5 sen 60°", "5 × 0.866"], "≈ 4.33 m")],
     [["Usar el lado equivocado", "Ubica opuesto y adyacente respecto al ángulo dado."], ["Calculadora en radianes", "Revisa que esté en grados (DEG)."], ["Multiplicar áreas por k", "Las áreas van por k², los volúmenes por k³."]],
     [("¿Qué significa SOH-CAH-TOA?", "Una forma de recordar: Seno = Opuesto/Hipotenusa, Coseno = Adyacente/Hipotenusa, Tangente = Opuesto/Adyacente."), ("¿Qué es la autosimilitud?", "Que una figura está hecha de copias más pequeñas de sí misma, como un helecho o un fractal.")],
     [("Razones trigonométricas", [(lambda: S.t1("razon"), 12), (raz, 8)]), ("Calcular lados", [(lambda: S.t1("lado"), 14), (res, 6)]), ("Calcular ángulos", [(lambda: S.t1("angulo"), 20)]),
      ("Semejanza y áreas", [(sem, 12), (lambda: S.t1("autosim"), 8)]), ("Problemas", [(pro, 20)])],
     130001, lv=13)
