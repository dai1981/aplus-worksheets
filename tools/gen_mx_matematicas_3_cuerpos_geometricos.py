# -*- coding: utf-8 -*-
"""México 3.er grado: Cuerpos geométricos (prismas rectos, pirámides, cilindro, cono, esfera; caras, aristas, vértices; desarrollos). Reutiliza España 4.º."""
from mx_common import src, unit
from es_common import cuerpo_svg

nom, tip, cont, dib, prop, obj, cual, comp, des = src("gen_es_matematicas_4_cuerpos_geometricos", 63210, "s1_nombre", "s1_tipo", "s2_contar", "s2_dibujo", "s3_prop", "s4_objetos", "s6_cual", "s6_comparar", "s5_desarrollo")

unit("cuerpos-geometricos", 10, "C",
     "Identifica cuerpos geométricos en objetos de su entorno; reconoce caras, aristas y vértices; construye prismas rectos a partir de cuadrados y rectángulos y reconoce sus desarrollos planos",
     "Cuerpos geométricos", "Cuerpos geométricos",
     "Ejercicios de matemáticas de 3.er grado de primaria: cubo, prisma, pirámide, cilindro, cono y esfera; caras, aristas, vértices y desarrollos planos. 100 ejercicios con respuestas.",
     "Caras, aristas y vértices", "Los cuerpos redondos ruedan.",
     ["Los <b>poliedros</b> tienen todas sus caras planas: cubo, prisma, pirámide.", "Los <b>cuerpos redondos</b> tienen alguna superficie curva: cilindro, cono, esfera.",
      "Una <b>cara</b> es una superficie plana; una <b>arista</b>, donde se juntan dos caras; un <b>vértice</b>, una esquina."],
     [("El cubo", ["6 caras, 12 aristas, 8 vértices"], "6 caras cuadradas"), ("Una lata de refresco", ["Dos bases circulares y una superficie curva"], "cilindro")],
     [["Llamar «cuadrado» al cubo", "El cuadrado es plano; el cubo tiene 6 caras."], ["Contar solo las caras que se ven", "Hay caras atrás y abajo."], ["Confundir cono y pirámide", "La base del cono es un círculo."]],
     [("¿Cuántas caras tiene un cubo?", "Seis caras, y todas son cuadrados iguales."), ("¿Qué cuerpos ruedan?", "Los cuerpos redondos: la esfera, el cilindro y el cono.")],
     [("Reconocer cuerpos", [(nom, 7), (tip, 7), (obj, 6)]), ("Caras, aristas y vértices", [(dib, 8), (cont, 12)]), ("Propiedades", [(prop, 12), (cual, 8)]),
      ("Comparar cuerpos", [(comp, 16), (prop, 4)]), ("Desarrollos y repaso", [(des, 5), (cont, 10), (comp, 5)])], 63010, pic=cuerpo_svg("prisma"))
