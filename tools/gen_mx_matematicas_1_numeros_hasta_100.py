# -*- coding: utf-8 -*-
"""México 1.er grado (hasta 100) y 2.º grado (hasta 1 000): Estudio de los números. Contar, leer y escribir, valor de las cifras, pares e impares. Reutiliza España 1.º/2.º (gen_es_matematicas_3_numeros, build(lv)) con otra semilla."""
from mx_common import src, unit
from mx_12 import BIG

T = {1: dict(slug="numeros-hasta-100", std="Cuenta oralmente hacia adelante y hacia atrás hasta 120; cuenta, ordena, representa, lee y escribe colecciones de hasta 100 elementos",
             title="Los números hasta el 100", short="Números hasta el 100",
             meta="Ejercicios de matemáticas de 1.er grado de primaria: contar, leer y escribir números hasta el 100, decenas y unidades, antes y después, pares e impares. 100 ejercicios con respuestas.",
             kb="10 unidades forman 1 decena", ks="En 47 hay 4 decenas y 7 unidades.",
             think=["Cuenta de uno en uno y, cuando juntes 10, haz un grupo: 10 unidades forman <b>1 decena</b>.",
                    "En 47, el 4 dice cuántas decenas hay y el 7, cuántas unidades sueltas: 40 + 7.",
                    "Después de 29 viene 30: al llegar a 10 unidades, cambia la decena."],
             ex=[("¿Cuántos hay? 3 grupos de 10 y 5 sueltos", ["3 decenas = 30", "30 + 5"], "35"), ("¿Qué número va después de 59?", ["59 + 1"], "60")],
             mist=[["Escribir 304 para «treinta y cuatro»", "Es 3 decenas y 4 unidades: 34."], ["Confundir 15 y 51", "El primer número son las decenas."], ["Saltar un número al contar", "Señala cada objeto una sola vez."]],
             faq=[("¿Qué es una decena?", "Un grupo de 10. En el número 36 hay 3 decenas (30) y 6 unidades."), ("¿Cómo sé si un número es par?", "Si termina en 0, 2, 4, 6 u 8, es par: se puede repartir en dos grupos iguales.")],
             sets=[("Contar", "s1_contar"), ("Leer y escribir números", "s2_letra"), ("Decenas y unidades", "s3_valor"), ("Antes, después y de 10 en 10", "s4_series"), ("Pares e impares", "s5_par")]),
     2: dict(slug="numeros-hasta-1000", std="Cuenta oralmente hasta 1 000; cuenta, ordena, representa, lee y escribe números menores que 1 000; identifica regularidades en unidades, decenas y centenas",
             title="Los números hasta el 1 000", short="Números hasta el 1 000",
             meta="Ejercicios de matemáticas de 2.º grado de primaria: contar, leer y escribir números hasta el 1 000, centenas, decenas y unidades, pares e impares. 100 ejercicios con respuestas.",
             kb="10 decenas forman 1 centena", ks="En 365 hay 3 centenas, 6 decenas y 5 unidades.",
             think=["10 unidades forman 1 decena y 10 decenas forman <b>1 centena</b> (100).",
                    "En 365, el 3 vale 300, el 6 vale 60 y el 5 vale 5: 300 + 60 + 5.",
                    "Si falta un lugar, se escribe 0: «doscientos ocho» = 208."],
             ex=[("Escribe «cuatrocientos treinta»", ["4 centenas, 3 decenas, 0 unidades"], "430"), ("¿Qué número va después de 399?", ["399 + 1"], "400")],
             mist=[["Escribir 2008 para «doscientos ocho»", "Son 2 centenas y 8 unidades: 208."], ["Confundir la cifra con su valor", "En 365, el 3 vale 300."], ["Contar mal al cambiar de centena", "Después de 199 va 200."]],
             faq=[("¿Qué es una centena?", "Un grupo de 100, o sea 10 decenas. En 528 hay 5 centenas."), ("¿Cómo se escribe un número con cero en medio?", "Pon 0 en el lugar que no se nombra: «setecientos cinco» = 705.")],
             sets=[("Contar con bloques", "s1_contar"), ("Leer y escribir números", "s2_letra"), ("Centenas, decenas y unidades", "s3_valor"), ("Antes, después y sucesiones", "s4_series"), ("Pares e impares", "s5_par")])}


def build(lv):
    t = T[lv]
    names = [n for _, n in t["sets"]]
    fs = src("gen_es_matematicas_3_numeros", 60100 + 1000 * lv, *names, lv=lv, mx_=BIG)
    unit(t["slug"], 1, "N", t["std"], t["title"], t["short"], t["meta"], t["kb"], t["ks"], t["think"], t["ex"], t["mist"], t["faq"],
         [(title, [(f, 20)]) for (title, _), f in zip(t["sets"], fs)], 60000 + 1000 * lv + 1, lv=lv)


if __name__ == "__main__":
    build(1)
