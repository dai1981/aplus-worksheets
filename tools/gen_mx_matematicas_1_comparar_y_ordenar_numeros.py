# -*- coding: utf-8 -*-
"""México 1.er grado (hasta 100) y 2.º grado (hasta 1 000): Comparar y ordenar números con <, > e =. Reutiliza España 1.º/2.º (gen_es_matematicas_3_comparar_y_ordenar) con otra semilla."""
from mx_common import src, unit
from mx_12 import BIG

T = {1: dict(std="Compara y ordena colecciones y números de hasta dos cifras; usa las palabras mayor que, menor que e igual",
             title="Comparar y ordenar números hasta el 100", meta="Ejercicios de matemáticas de 1.er grado de primaria: comparar colecciones, mayor que y menor que, ordenar números hasta el 100 y problemas. 100 ejercicios con respuestas.",
             kb="Mira primero las decenas", ks="Si son iguales, compara las unidades.",
             think=["Para comparar dos números, mira primero las <b>decenas</b>: 52 es mayor que 38 porque 5 decenas son más que 3.",
                    "Si las decenas son iguales, compara las unidades: 47 &lt; 49.",
                    "El signo &gt; quiere decir «mayor que» y &lt;, «menor que». La punta señala al número menor."],
             ex=[("Compara 63 y 36", ["6 decenas y 3 decenas"], "63 &gt; 36"), ("Ordena 45, 54, 40", ["40 &lt; 45 &lt; 54"], "40, 45, 54")],
             mist=[["Comparar solo las unidades", "En 29 y 31, 31 es mayor aunque 1 &lt; 9."], ["Voltear el signo", "La boca abierta mira al número mayor."], ["Olvidar un número al ordenar", "Tacha cada número que ya usaste."]],
             faq=[("¿Qué número es mayor, 70 o 69?", "70, porque tiene 7 decenas y 69 solo tiene 6."), ("¿Cómo recuerdo los signos &lt; y &gt;?", "La parte abierta siempre mira al número mayor: 8 &gt; 3.")]),
     2: dict(std="Usa los signos <, > o = para comparar u ordenar dos números menores que 1 000",
             title="Comparar y ordenar números hasta el 1 000", meta="Ejercicios de matemáticas de 2.º grado de primaria: comparar números de tres cifras con &lt;, &gt; e =, ordenar y ubicar en la recta. 100 ejercicios con respuestas.",
             kb="Primero las centenas", ks="Después las decenas y al final las unidades.",
             think=["Para comparar números de tres cifras, mira primero las <b>centenas</b>: 512 &gt; 498 porque 5 centenas son más que 4.",
                    "Si las centenas son iguales, compara las decenas; si también son iguales, las unidades.",
                    "&gt; es «mayor que», &lt; es «menor que» e = es «igual a»."],
             ex=[("Compara 456 y 465", ["4 = 4", "5 &lt; 6 en las decenas"], "456 &lt; 465"), ("Ordena de menor a mayor 308, 380, 83", ["83 tiene menos cifras"], "83, 308, 380")],
             mist=[["Comparar por la última cifra", "Empieza por la izquierda."], ["Creer que 83 &gt; 308", "Un número de dos cifras es menor que uno de tres."], ["Voltear el signo", "La punta señala al menor."]],
             faq=[("¿Qué número es mayor, 699 o 700?", "700, porque tiene 7 centenas y 699 solo 6."), ("¿Qué significa el signo =?", "Que las dos cantidades valen lo mismo: 300 + 20 = 320.")])}
SETS = [("Comparar colecciones", "s1_dibujos"), ("Mayor que, menor que e igual", "s2_signo"), ("Ordenar números", "s3_ordenar"), ("Entre qué números está", "s4_entre"), ("Problemas", "s5_problema")]


def build(lv):
    t = T[lv]
    fs = src("gen_es_matematicas_3_comparar_y_ordenar", 60200 + 1000 * lv, *[n for _, n in SETS], lv=lv, mx_=BIG)
    unit("comparar-y-ordenar-numeros", 2, "N", t["std"], t["title"], "Comparar y ordenar", t["meta"], t["kb"], t["ks"], t["think"], t["ex"], t["mist"], t["faq"],
         [(title, [(f, 20)]) for (title, _), f in zip(SETS, fs)], 60000 + 1000 * lv + 2, lv=lv)


if __name__ == "__main__":
    build(1)
