# -*- coding: utf-8 -*-
"""México 4.º grado: Fracciones (tercios, quintos, sextos, novenos y décimos; Estudio de los números). Reutiliza España 4.º con otra semilla, con esos denominadores."""
import re
from mx_common import src, unit
from es_common import tira, fr

NUEVOS = {"3", "5", "6", "9", "10"}
OK = NUEVOS | {"2", "4", "8", "12"}
BAD = ("séptimo", "doceavo", "mixto", "1 y ")


def dens(it):
    t = it["q"] + " ".join(it["c"]) + it["e"]
    ds = re.findall(r"class='fd'>(\d+)<", t)
    return all(d in OK for d in ds) and any(d in NUEVOS for d in ds) and not any(w in t for w in BAD) and not re.search(r"\d\s*<span class='fr'>", t)


leer, comp, de, suma, prob = src("gen_es_matematicas_4_fracciones", 64210, "s1_leer", "s2_comparar", "s3_de_un_numero", "s4_suma", "s5_problema", extra=(dens,))

unit("fracciones", 8, "N",
     "Usa fracciones con denominador 3, 5, 6, 9 y 10 (tercios, quintos, sextos, novenos y décimos) para expresar partes de una unidad y de una colección; las lee, compara, suma y resta",
     "Fracciones: tercios, quintos, sextos y décimos", "Fracciones",
     "Ejercicios de matemáticas de 4.º grado de primaria: tercios, quintos, sextos, novenos y décimos, comparar fracciones, fracción de una cantidad, sumar y restar y problemas. 100 ejercicios con respuestas.",
     "Partes iguales de un entero", "Abajo: en cuántas partes. Arriba: cuántas.",
     ["En %s, el <b>denominador</b> (5) dice en cuántas partes iguales se divide el entero y el <b>numerador</b> (3), cuántas partes tomamos. Se lee «tres quintos»." % fr(3, 5),
      "Con el mismo denominador, es mayor la de mayor numerador: %s &gt; %s. Con el mismo numerador, es mayor la de <b>menor</b> denominador: %s &gt; %s." % (fr(4, 6), fr(1, 6), fr(1, 3), fr(1, 9)),
      "Para calcular %s de 30: 30 ÷ 5 = 6 y 6 × 2 = 12." % fr(2, 5)],
     [("¿Cuánto es %s de 18?" % fr(2, 3), ["18 ÷ 3 = 6", "6 × 2 = 12"], "12"), ("%s + %s" % (fr(4, 10), fr(3, 10)), ["4 + 3 = 7", "el denominador sigue siendo 10"], fr(7, 10))],
     [["Creer que %s &gt; %s porque 9 &gt; 3" % (fr(1, 9), fr(1, 3)), "Más partes: cada parte es más pequeña."], ["Sumar los denominadores", "%s + %s = %s, no %s." % (fr(1, 5), fr(2, 5), fr(3, 5), fr(3, 10))],
      ["Dividir entre el numerador", "%s de 30: divide entre 5, no entre 2." % fr(2, 5)]],
     [("¿Cómo se leen las fracciones con denominador 10?", "Como décimos: 3/10 se lee «tres décimos». Con 9 son novenos y con 6, sextos."),
      ("¿Cuántos quintos tiene un entero?", "Cinco: 5/5 = 1. Del mismo modo, 3/3 = 1 y 10/10 = 1.")],
     [("Leer y representar", [(leer, 20)]), ("Comparar fracciones", [(comp, 20)]), ("Fracción de una cantidad", [(de, 20)]), ("Sumar y restar", [(suma, 20)]), ("Problemas", [(prob, 20)])],
     64008, pic=tira(5, 3), lv=4)
