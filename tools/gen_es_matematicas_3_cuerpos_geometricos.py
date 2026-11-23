# -*- coding: utf-8 -*-
"""
España Matemáticas 3.º de Primaria: Cuerpos geométricos (Sentido espacial)
Reutiliza los generadores de 4.º (mismo ciclo).
"""
from es_low import unit, src
from es_common import cuerpo_svg

SEED = 33918
nom, tip, cont, dib, prop, obj, cual, comp, des = src("cuerpos_geometricos", SEED, "s1_nombre", "s1_tipo", "s2_contar", "s2_dibujo", "s3_prop", "s4_objetos", "s6_cual", "s6_comparar", "s5_desarrollo")

unit(3, "cuerpos-geometricos", 18, "E", "Cuerpos geométricos: prismas, pirámides, cubo, cilindro, cono y esfera; caras, aristas y vértices; desarrollos planos",
     "Cuerpos geométricos", "Cuerpos geométricos",
     "Fichas de matemáticas de 3.º de Primaria: cubo, prisma, pirámide, cilindro, cono y esfera, caras, aristas, vértices y desarrollos. 100 ejercicios con soluciones.",
     "Caras, aristas y vértices", "Los cuerpos redondos ruedan.",
     ["Los <b>poliedros</b> tienen todas las caras planas: cubo, prisma, pirámide.", "Los <b>cuerpos redondos</b> tienen alguna superficie curva: cilindro, cono, esfera.",
      "Una <b>cara</b> es una superficie; una <b>arista</b>, donde se juntan dos caras; un <b>vértice</b>, una esquina."],
     [("El cubo", ["6 caras, 12 aristas, 8 vértices"], "6 caras cuadradas"), ("Una lata de refresco", ["Dos bases circulares y una superficie curva"], "cilindro")],
     [["Llamar «cuadrado» al cubo", "El cuadrado es plano; el cubo tiene 6 caras."], ["Contar solo las caras que se ven", "Hay caras detrás y debajo."], ["Confundir cono y pirámide", "La base del cono es un círculo."]],
     [("¿Cuántas caras tiene un cubo?", "Seis caras, y todas son cuadrados iguales."), ("¿Qué cuerpos ruedan?", "Los cuerpos redondos: la esfera, el cilindro y el cono.")],
     [("Reconocer cuerpos", [(nom, 6), (tip, 6), (obj, 8)]), ("Caras, aristas y vértices", [(dib, 8), (cont, 12)]), ("Propiedades", [(prop, 14), (cual, 6)]),
      ("Comparar cuerpos", [(comp, 14), (obj, 6)]), ("Desarrollos y repaso", [(des, 5), (cont, 10), (comp, 5)])], 33018, cuerpo_svg("prisma"))
