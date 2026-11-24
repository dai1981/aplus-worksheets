# -*- coding: utf-8 -*-
"""México 3.er grado de secundaria (Fase 6): Relaciones de volumen entre esfera, cono y cilindro; área de la esfera."""
import random
import re  # noqa: F401
import mx_s2 as S
from mx_common import src, unit, nomoney, noplanta  # noqa: F401

S.setup(random.Random(69113))
unit("esfera-cono-y-cilindro", 13, "6CC",
     "Encuentra las relaciones de volumen entre esfera, cono y cilindro; calcula el volumen y el área de la esfera",
     "Esfera, cono y cilindro", "Esfera, cono y cilindro",
     "Ejercicios de matemáticas de 3.er grado de secundaria: relaciones de volumen entre cono, cilindro y esfera, volumen y área de la esfera. 100 ejercicios con respuestas.",
     "Cono : esfera : cilindro = 1 : 2 : 3", "Con el mismo radio y altura = diámetro.",
     ["Si un cono, una esfera y un cilindro tienen el mismo radio y la altura es el diámetro, sus volúmenes están en razón <b>1 : 2 : 3</b>.",
      "El cono es 1/3 del cilindro y la esfera es 2/3 del cilindro. De ahí sale V esfera = 4/3 π r³.",
      "El área de la superficie de la esfera es 4 π r²: cuatro veces el área de su círculo máximo."],
     [("Esfera r = 3", ["4 × 3.14 × 27 ÷ 3"], "113.04 cm³"), ("Cilindro de 600 cm³", ["cono 600 ÷ 3", "esfera 600 × 2/3"], "200 y 400 cm³")],
     [["Usar r² en el volumen de la esfera", "Es r³."], ["Confundir área y volumen de la esfera", "Área 4πr² (cm²); volumen 4/3 πr³ (cm³)."], ["Olvidar el 4/3", "V = 4/3 π r³."]],
     [("¿Quién descubrió la relación?", "Arquímedes, en la Antigua Grecia; pidió que en su tumba grabaran una esfera dentro de un cilindro."), ("¿Por qué 4πr²?", "La superficie de la esfera equivale a 4 círculos máximos.")],
     [("Relaciones de volumen", [(lambda: S.esfera("rel"), 20)]), ("Volumen de la esfera", [(lambda: S.esfera("vesf"), 20)]), ("Área de la esfera", [(lambda: S.esfera("aesf"), 20)]),
      ("Cono y cilindro", [(lambda: S.esfera("vcono", "vcil"), 20)]), ("Repaso", [(S.esfera, 20)])],
     69013, lv=9)
