# -*- coding: utf-8 -*-
"""México 5.º grado: Porcentajes 10 %, 20 %, 25 %, 50 % y 75 % como fracciones; porcentaje de una cantidad (Relaciones de proporcionalidad). Reutiliza España 6.º (nivel 5.º) con otra semilla."""
import re
from mx_common import src, unit

OK = {"10", "20", "25", "50", "75", "100"}


def faciles(it):
    t = re.sub(r"<[^>]*>", " ", it["q"] + " " + " ".join(it["c"]))
    return all(p in OK for p in re.findall(r"(\d+)\s?%", it["q"])) and not re.search(r"IVA|interés", t)


conc, calc, desc, que, probl = src("gen_es_matematicas_6_porcentajes", 65313, "s1_concepto", "s2_calcular", "s3_descuento", "s4_que_porcentaje", "s5_problema", lv=5, extra=(faciles,))

unit("porcentajes", 9, "Q",
     "Interpreta y calcula porcentajes sencillos (10 %, 20 %, 25 %, 50 % y 75 %) relacionándolos con fracciones; calcula el porcentaje de una cantidad y descuentos",
     "Porcentajes: 10 %, 25 %, 50 % y 75 %", "Porcentajes",
     "Ejercicios de matemáticas de 5.º grado de primaria: qué es un porcentaje, 50 %, 25 %, 20 % y 10 % como fracciones, porcentaje de una cantidad y descuentos. 100 ejercicios con respuestas.",
     "50 % = 1/2; 25 % = 1/4; 10 % = 1/10", "Porcentaje: de cada 100.",
     ["Un <b>porcentaje</b> dice cuántos de cada 100: 30 % = 30 de cada 100 = 30/100.",
      "Algunos porcentajes son fracciones fáciles: 50 % es la mitad, 25 % la cuarta parte, 20 % la quinta parte y 10 % la décima parte. 75 % son tres cuartas partes.",
      "Para calcular el 25 % de 480: 480 ÷ 4 = 120. Para el 10 % de 350: 350 ÷ 10 = 35."],
     [("20 % de 150", ["20 % = 1/5", "150 ÷ 5"], "30"), ("Una playera de $240 con 25 % de descuento", ["descuento: 240 ÷ 4 = 60", "240 − 60"], "$180")],
     [["Confundir 25 % con 1/25", "25 % = 25/100 = 1/4."], ["Restar el porcentaje como pesos", "25 % de $240 no es $25: es $60."], ["Dar el descuento en lugar del precio final", "Resta el descuento al precio."]],
     [("¿Qué significa 100 %?", "El total, todo. 50 % es la mitad y 25 %, la cuarta parte."),
      ("¿Cómo calculo el 10 % de un número?", "Divide entre 10: el 10 % de 350 es 35. Con el 10 % puedes calcular el 20 % (el doble) o el 5 % (la mitad).")],
     [("Porcentajes y fracciones", [(conc, 20)]), ("Porcentaje de una cantidad", [(calc, 20)]), ("¿Qué porcentaje es?", [(que, 12), (conc, 8)]), ("Descuentos", [(desc, 20)]), ("Problemas", [(probl, 20)])],
     65009, lv=5)
