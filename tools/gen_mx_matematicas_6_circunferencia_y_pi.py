# -*- coding: utf-8 -*-
"""México 6.º grado: La circunferencia y el número π (perímetro del círculo), radio y diámetro (Figuras geométricas; Perímetro y área). Reutiliza España 6.º con otra semilla."""
import re
import random
from mx_common import src, unit, mcq, num


def sin_area(it):
    return not re.search(r"área|superficie|m²|cm²", re.sub(r"<[^>]*>", " ", it["q"] + " ".join(it["c"])))


pi, longi, inv, probl = src("gen_es_matematicas_6_longitud_y_area_del_circulo", 66318, "s1_pi", "s2_longitud", "s4_inversa", "s5_problema", lv=6, extra=(sin_area,))
circ = src("gen_es_matematicas_6_poligonos_y_circulo", 66316, "s4_circulo", lv=6)
R = random.Random(66118)
COSAS = [("Una rueda de bicicleta", "cm"), ("Una mesa redonda", "cm"), ("Una fuente circular del jardín", "m"), ("Un plato", "cm"), ("Una pista circular", "m"), ("Un reloj de pared", "cm"), ("Una alberca redonda", "m")]


def d2(x):
    s = ("%.2f" % x).rstrip("0").rstrip(".")
    return num(int(s)) if "." not in s else num(int(s.split(".")[0])) + "." + s.split(".")[1]


def own():
    cosa, u = R.choice(COSAS)
    k = R.choice(["d", "r", "d", "r"])
    v = R.randint(2, 60) if u == "cm" else R.randint(2, 30)
    d = v if k == "d" else 2 * v
    c = 314 * d / 100
    dato = "%s %d %s de %s" % ("tiene", v, u, "diámetro" if k == "d" else "radio")
    w = [d2(314 * v / 100) if k == "r" else d2(314 * v / 200), d2(3 * d), d2(314 * d * d / 400), d2(c + 3.14)]
    return mcq("%s %s. ¿Cuánto mide su circunferencia? (usa π ≈ 3.14)" % (cosa, dato), "%s %s" % (d2(c), u), ["%s %s" % (x, u) for x in w if x != d2(c)],
               "%sC = 3.14 × %d = <b>%s %s</b>." % ("" if k == "d" else "d = 2 × %d = %d; " % (v, d), d, d2(c), u))

unit("circunferencia-y-pi", 8, "F",
     "Identifica el número π como la razón entre la longitud de la circunferencia y su diámetro; calcula la longitud de una circunferencia con π ≈ 3.14 y, a partir de ella, el diámetro o el radio",
     "La circunferencia y el número π", "Circunferencia y π",
     "Ejercicios de matemáticas de 6.º grado de primaria: radio y diámetro, el número π, longitud de la circunferencia, calcular el diámetro y problemas. 100 ejercicios con respuestas.",
     "Circunferencia = π × diámetro", "π ≈ 3.14",
     ["Si divides la longitud de cualquier circunferencia entre su diámetro, siempre da lo mismo: el número <b>π</b> (pi), que vale aproximadamente <b>3.14</b>.",
      "Por eso, longitud de la circunferencia = π × diámetro = 2 × π × radio. Con un diámetro de 10 cm: 3.14 × 10 = 31.4 cm.",
      "Si conoces la longitud, divide entre π para encontrar el diámetro: 62.8 ÷ 3.14 = 20 cm."],
     [("Radio de 5 cm", ["diámetro = 10 cm", "3.14 × 10"], "31.4 cm"), ("Longitud de 47.1 m", ["47.1 ÷ 3.14"], "diámetro de 15 m")],
     [["Usar el radio en lugar del diámetro", "C = π × d = 2 × π × r."], ["Multiplicar por 3 en lugar de 3.14", "π ≈ 3.14."], ["Confundir longitud y área", "La longitud de la circunferencia va en cm, no en cm²."]],
     [("¿Qué es el número π?", "Es el número de veces que cabe el diámetro en la circunferencia: un poco más de 3, aproximadamente 3.14."),
      ("¿Cómo calculo la longitud de una circunferencia?", "Multiplica el diámetro por 3.14. Si te dan el radio, primero duplícalo.")],
     [("Radio, diámetro y circunferencia", [(circ, 20)]), ("El número π", [(pi, 4), (longi, 16)]), ("Longitud de la circunferencia", [(own, 20)]), ("Calcular el diámetro o el radio", [(inv, 20)]), ("Problemas", [(probl, 12), (own, 8)])],
     66008, lv=6)
