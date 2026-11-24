# -*- coding: utf-8 -*-
"""México 3.er grado de secundaria (Fase 6): Volumen de prismas, pirámides y cilindros."""
import random
import re  # noqa: F401
import mx_s2 as S
from mx_common import src, unit, nomoney, noplanta  # noqa: F401

S.setup(random.Random(69112))
vol, are, prob = src("gen_es_matematicas_2eso_cuerpos", 69371, "s_volumen", "s_areas", "s_problema", lv=2, extra=(nomoney, lambda it: "esfera" not in it["q"]))
unit("volumen-de-prismas-piramides-y-cilindros", 12, "6ME",
     "Calcula el volumen de prismas, pirámides y cilindros y resuelve problemas",
     "Volumen de prismas, pirámides y cilindros", "Volumen de cuerpos",
     "Ejercicios de matemáticas de 3.er grado de secundaria: volumen de prismas, pirámides, cilindros y conos, área total y problemas con capacidad. 100 ejercicios con respuestas.",
     "Prisma y cilindro: base × altura", "Pirámide y cono: la tercera parte.",
     ["El volumen de un <b>prisma</b> o un <b>cilindro</b> es área de la base × altura. En el cilindro, la base es un círculo: V = π r² h.",
      "Una <b>pirámide</b> o un <b>cono</b> tienen la tercera parte del volumen del prisma o cilindro con la misma base y altura: V = área de la base × altura ÷ 3.",
      "1 dm³ = 1 L y 1 cm³ = 1 mL."],
     [("Cilindro r = 3, h = 10", ["3.14 × 9 × 10"], "282.6 cm³"), ("Pirámide base 6 × 6, h = 8", ["36 × 8 ÷ 3"], "96 cm³")],
     [["Olvidar dividir entre 3", "Pirámide y cono llevan ÷ 3."], ["Usar el diámetro como radio", "Si d = 8, r = 4."], ["Confundir área y volumen", "El volumen va en unidades cúbicas."]],
     [("¿Cuántos litros caben en 1 m³?", "1 000 L."), ("¿Por qué la pirámide es un tercio?", "Tres pirámides iguales llenan exactamente el prisma con la misma base y altura.")],
     [("Prismas y pirámides", [(vol, 20)]), ("Cilindros", [(lambda: S.esfera("vcil"), 20)]), ("Conos", [(lambda: S.esfera("vcono"), 20)]), ("Área total", [(are, 20)]), ("Problemas", [(prob, 20)])],
     69012, lv=9)
