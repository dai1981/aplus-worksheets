# -*- coding: utf-8 -*-
"""México 3.er grado de secundaria (Fase 6): Sólidos de revolución y desarrollos planos de prismas, pirámides, cilindros y conos."""
import random
import re  # noqa: F401
import mx_s2 as S
from mx_common import src, unit, nomoney, noplanta  # noqa: F401

S.setup(random.Random(69111))
unit("solidos-de-revolucion-y-desarrollos-planos", 11, "6CF",
     "Explora la generación de sólidos de revolución y construye desarrollos planos de prismas, cilindros, pirámides y conos",
     "Sólidos de revolución y desarrollos planos", "Sólidos de revolución",
     "Ejercicios de matemáticas de 3.er grado de secundaria: cilindro, cono y esfera como sólidos de revolución y desarrollos planos de prismas, pirámides, cilindros y conos. 100 ejercicios con respuestas.",
     "Rectángulo que gira → cilindro", "Triángulo rectángulo → cono; semicírculo → esfera.",
     ["Un <b>sólido de revolución</b> se forma al girar una figura plana alrededor de un eje: un rectángulo forma un cilindro, un triángulo rectángulo un cono y un semicírculo una esfera.",
      "El <b>desarrollo plano</b> de un cuerpo es la figura que, al doblarla, lo forma: el del cilindro son dos círculos y un rectángulo; el del cono, un círculo y un sector circular.",
      "En el cilindro, el largo del rectángulo es igual al perímetro de la base: 2πr."],
     [("Rectángulo de 3 × 8 que gira sobre el lado de 8", ["radio 3, altura 8"], "cilindro"), ("Desarrollo de cilindro con r = 5", ["2 × 3.14 × 5"], "rectángulo de 31.4 de largo")],
     [["Confundir radio y altura al girar", "El lado del eje es la altura."], ["Usar el diámetro para el largo", "Largo = 2πr = πd."], ["Olvidar una base", "El cilindro tiene dos círculos."]],
     [("¿La esfera tiene desarrollo plano exacto?", "No: solo se puede aproximar, como en los mapas o los gajos de un balón."), ("¿Qué es un cono truncado?", "Un cono al que se le cortó la punta con un plano paralelo a la base.")],
     [("¿Qué sólido se forma?", [(lambda: S.solidos("rev"), 6), (lambda: S.solidos("red"), 14)]), ("Radio y altura", [(lambda: S.solidos("red"), 20)]), ("Desarrollos planos", [(lambda: S.solidos("net"), 7), (lambda: S.solidos("cil"), 13)]),
      ("El rectángulo del cilindro", [(lambda: S.solidos("cil"), 20)]), ("Repaso", [(S.solidos, 20)])],
     69011, lv=9)
