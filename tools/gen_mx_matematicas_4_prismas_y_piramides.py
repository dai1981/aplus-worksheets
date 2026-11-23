# -*- coding: utf-8 -*-
"""México 4.º grado: Prismas y pirámides: caras, aristas y vértices; desarrollos planos (Cuerpos geométricos y sus características). Reutiliza España 5.º/4.º con otra semilla."""
from mx_common import src, unit
import gen_es_matematicas_4_cuerpos_geometricos as C4

euler = src("gen_es_matematicas_6_cuerpos_y_volumen", 64321, "s1_euler", lv=5)
nom, tip, cont, prop, obj, cual, comp, des = src("gen_es_matematicas_4_cuerpos_geometricos", 64221, "s1_nombre", "s1_tipo", "s2_contar", "s3_prop", "s4_objetos", "s6_cual", "s6_comparar", "s5_desarrollo")

unit("prismas-y-piramides", 16, "C",
     "Describe y clasifica prismas y pirámides por la forma de sus bases y de sus caras; cuenta caras, aristas y vértices; relaciona cuerpos con sus desarrollos planos, como el del cubo",
     "Prismas y pirámides", "Prismas y pirámides",
     "Ejercicios de matemáticas de 4.º grado de primaria: prismas y pirámides, bases y caras, contar caras, aristas y vértices, desarrollos planos y cuerpos en la vida diaria. 100 ejercicios con respuestas.",
     "Prisma: 2 bases. Pirámide: 1 base", "El nombre lo da el polígono de la base.",
     ["Un <b>prisma</b> tiene dos bases iguales y paralelas, y sus caras laterales son rectángulos. Una <b>pirámide</b> tiene una sola base y sus caras laterales son triángulos que se juntan en un vértice.",
      "El nombre lo da la base: prisma triangular, cuadrangular, pentagonal…; pirámide hexagonal…",
      "Un prisma con base de n lados tiene n + 2 caras, 2 × n vértices y 3 × n aristas. Una pirámide tiene n + 1 caras, n + 1 vértices y 2 × n aristas."],
     [("Prisma hexagonal", ["caras: 6 + 2 = 8", "vértices: 2 × 6 = 12", "aristas: 3 × 6 = 18"], "8 caras, 12 vértices y 18 aristas"),
      ("Pirámide cuadrangular", ["caras: 4 + 1 = 5", "aristas: 2 × 4 = 8"], "5 caras y 8 aristas")],
     [["Contar solo las caras laterales", "Suma también las bases."], ["Confundir prisma y pirámide", "La pirámide termina en punta."], ["Pensar que el cubo no es un prisma", "Es un prisma cuadrangular con 6 caras cuadradas."]],
     [("¿Qué diferencia hay entre un prisma y una pirámide?", "El prisma tiene dos bases iguales y caras laterales rectangulares; la pirámide tiene una base y caras laterales triangulares que terminan en un vértice."),
      ("¿Qué es el desarrollo plano de un cuerpo?", "Es la figura que se obtiene al «desarmar» el cuerpo y extender sus caras sobre una mesa. Al doblarla se vuelve a formar el cuerpo.")],
     [("Nombres de cuerpos", [(nom, 14), (tip, 6)]), ("Caras, aristas y vértices", [(euler, 20)]), ("Contar y comparar", [(cont, 10), (comp, 10)]), ("Propiedades y desarrollos", [(prop, 12), (des, 4), (cual, 4)]),
      ("Cuerpos en la vida diaria", [(obj, 10), (comp, 10)])],
     64016, lv=4)
