# -*- coding: utf-8 -*-
"""México 1.er grado de secundaria (Fase 6): Propiedades de los sólidos: prismas, pirámides, cilindro, cono y esfera; fórmula de Euler."""
import random
import mx_s1 as S
from mx_common import src, unit, nomoney, noplanta  # noqa: F401

S.setup(random.Random(67114))
eu = src("gen_es_matematicas_6_cuerpos_y_volumen", 67431, "s1_euler", lv=6)
eu2 = src("gen_es_matematicas_2eso_cuerpos", 67432, "s_euler", lv=2)

unit("cuerpos-geometricos", 14, "6CF",
     "Reconoce las propiedades de los sólidos: caras, aristas y vértices de prismas y pirámides, cuerpos redondos y la relación de Euler",
     "Cuerpos geométricos: caras, aristas y vértices", "Cuerpos geométricos",
     "Ejercicios de matemáticas de 1.er grado de secundaria: prismas y pirámides, caras, aristas y vértices, fórmula de Euler y cuerpos redondos (cilindro, cono y esfera). 100 ejercicios con respuestas.",
     "Prisma de base n: 3n aristas", "Caras + vértices = aristas + 2",
     ["Un <b>poliedro</b> solo tiene caras planas (prismas, pirámides). El <b>cilindro</b>, el <b>cono</b> y la <b>esfera</b> tienen superficies curvas: son cuerpos redondos.",
      "Si la base tiene n lados, el <b>prisma</b> tiene n + 2 caras, 2n vértices y 3n aristas; la <b>pirámide</b>, n + 1 caras, n + 1 vértices y 2n aristas.",
      "En todo poliedro convexo se cumple la <b>fórmula de Euler</b>: caras + vértices = aristas + 2."],
     [("Prisma hexagonal", ["n = 6"], "8 caras, 12 vértices, 18 aristas"), ("Poliedro con 5 caras y 6 vértices", ["A = 5 + 6 − 2"], "9 aristas")],
     [["Olvidar las bases al contar caras", "Un prisma triangular tiene 3 laterales + 2 bases = 5 caras."], ["Llamar poliedro al cilindro", "Tiene superficie curva: no es poliedro."], ["Confundir la base", "La pirámide cuadrangular tiene base de 4 lados."]],
     [("¿Qué diferencia hay entre prisma y pirámide?", "El prisma tiene dos bases iguales y caras laterales rectangulares; la pirámide tiene una base y caras laterales triangulares que se unen en la cúspide."),
      ("¿La esfera tiene caras?", "No: tiene una sola superficie curva, sin aristas ni vértices.")],
     [("Prismas", [(lambda: S.cuerpos("cvAp", "cvAp", "basep", "latp"), 20)]), ("Pirámides", [(lambda: S.cuerpos("cvAy", "cvAy", "basey", "laty"), 20)]), ("Fórmula de Euler", [(lambda: S.cuerpos("euler"), 12), (eu2, 8)]),
      ("Cuerpos redondos y poliedros", [(lambda: S.cuerpos("redondo", "redondo", "redondo", "nopoli"), 18), (eu, 2)]), ("Repaso", [(S.cuerpos, 16), (eu, 4)])],
     67014, lv=7)
