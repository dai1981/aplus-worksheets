# -*- coding: utf-8 -*-
"""México 4.º grado: Fracciones equivalentes (Estudio de los números). Reutiliza España 4.º con otra semilla."""
import re
from mx_common import src, unit
from es_common import tira, fr


def dens(it):
    t = it["q"] + " ".join(it["c"]) + it["e"]
    return all(int(d) <= 20 for d in re.findall(r"class='fd'>(\d+)<", t)) and not re.search(r"\d\s*<span class='fr'>", t)


dib, ampl, simp, comp, prob = src("gen_es_matematicas_4_fracciones_equivalentes", 64211, "s1_dibujo", "s2_amplificar", "s3_simplificar", "s4_comprobar", "s5_problema", extra=(dens,))

unit("fracciones-equivalentes", 9, "N",
     "Identifica y genera fracciones equivalentes multiplicando o dividiendo el numerador y el denominador por el mismo número; las usa para comparar fracciones con distinto denominador",
     "Fracciones equivalentes", "Fracciones equivalentes",
     "Ejercicios de matemáticas de 4.º grado de primaria: fracciones equivalentes con dibujos, amplificar, simplificar, comprobar y problemas. 100 ejercicios con respuestas.",
     "Multiplica arriba y abajo igual", "La misma parte del entero, otro nombre.",
     ["Dos fracciones son <b>equivalentes</b> si representan la misma parte del entero: %s = %s = %s." % (fr(1, 2), fr(2, 4), fr(5, 10)),
      "Para obtener una equivalente, multiplica (o divide) el numerador y el denominador <b>por el mismo número</b>: %s = %s (× 3)." % (fr(2, 3), fr(6, 9)),
      "Para comprobar, multiplica en cruz: %s y %s son equivalentes porque 2 × 9 = 3 × 6." % (fr(2, 3), fr(6, 9))],
     [("Completa %s = ?/10" % fr(3, 5), ["5 × 2 = 10", "3 × 2 = 6"], fr(6, 10)), ("Simplifica %s" % fr(6, 9), ["6 ÷ 3 = 2", "9 ÷ 3 = 3"], fr(2, 3))],
     [["Multiplicar solo el denominador", "%s no es %s: multiplica también el numerador." % (fr(1, 3), fr(1, 6))], ["Sumar en vez de multiplicar", "Sumar 1 arriba y abajo no sirve: %s y %s no son equivalentes." % (fr(1, 2), fr(2, 3))],
      ["Dividir entre números distintos", "Arriba y abajo, entre el mismo número."]],
     [("¿Cómo sé si dos fracciones son equivalentes?", "Multiplica en cruz: si 2 × 9 da lo mismo que 3 × 6, entonces 2/3 y 6/9 son equivalentes."),
      ("¿Qué es simplificar una fracción?", "Dividir el numerador y el denominador entre el mismo número para obtener una fracción equivalente con números más pequeños.")],
     [("Con dibujos", [(dib, 14), (ampl, 6)]), ("Amplificar", [(ampl, 20)]), ("Simplificar", [(simp, 20)]), ("¿Son equivalentes?", [(comp, 20)]), ("Problemas", [(prob, 20)])],
     64009, pic=tira(3, 2) + tira(6, 4), lv=4)
