# -*- coding: utf-8 -*-
"""México 1.er grado: Cuerpos geométricos y sus características: caras planas y curvas, ruedan o no ruedan, objetos de la vida diaria. Reutiliza España 1.º (gen_es_matematicas_2_cuerpos) con otra semilla."""
from mx_common import src, unit
from mx_12 import BIG

nom, obj, rueda, saber, cuantos = src("gen_es_matematicas_2_cuerpos", 61801, "s_nombre", "s_objeto", "s_rueda", "s_saber", "s_cuantos", lv=1, mx_=BIG)

unit("cuerpos-geometricos", 8, "C",
     "Observa y manipula objetos para identificar líneas rectas o curvas y caras planas o curvas; clasifica objetos y cuerpos geométricos por el tipo de caras y los construye con cajas, bloques o cubos",
     "Cuerpos geométricos", "Cuerpos geométricos",
     "Ejercicios de matemáticas de 1.er grado de primaria: cubo, esfera, cilindro, cono y prisma; caras planas y curvas, ruedan o no ruedan, objetos de la vida diaria. 100 ejercicios con respuestas.",
     "Caras planas o curvas", "Lo que tiene una cara curva puede rodar.",
     ["Los <b>cuerpos geométricos</b> ocupan espacio: el cubo, la esfera, el cilindro, el cono y el prisma.",
      "Algunos tienen solo <b>caras planas</b> (el cubo, como un dado) y otros tienen <b>caras curvas</b> (la esfera, como una pelota).",
      "Los que tienen caras curvas pueden <b>rodar</b>; los de caras planas se pueden apilar."],
     [("Un dado", ["6 caras planas iguales"], "cubo"), ("Una lata", ["dos caras planas y una curva"], "cilindro")],
     [["Confundir cubo y cuadrado", "El cuadrado es plano; el cubo ocupa espacio."], ["Pensar que el cono no rueda", "Rueda haciendo círculos."], ["Confundir esfera y círculo", "La pelota es una esfera."]],
     [("¿Qué forma tiene una pelota?", "De esfera: es redonda por todos lados y rueda en cualquier dirección."), ("¿Qué cuerpos pueden rodar?", "Los que tienen una cara curva: la esfera, el cilindro y el cono.")],
     [("Nombres de cuerpos", [(nom, 20)]), ("Cuerpos en la vida diaria", [(obj, 12), (nom, 8)]), ("¿Rueda o no rueda?", [(rueda, 20)]), ("Caras planas y curvas", [(saber, 8), (cuantos, 12)]), ("Contar cuerpos", [(cuantos, 20)])],
     61008, lv=1)
