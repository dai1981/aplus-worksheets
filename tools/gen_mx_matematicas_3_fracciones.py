# -*- coding: utf-8 -*-
"""México 3.er grado: Fracciones (medios, cuartos, octavos y dieciseisavos; Estudio de los números). Reutiliza España 4.º con otra semilla, solo con esos denominadores."""
import re
from mx_common import src, unit
from es_common import tira, fr

OK = {"2", "4", "8", "16"}
BAD = ("tercio", "quinto", "sexto", "séptimo", "noveno", "décimo", "doceavo", "mixto", "1 y ")


def dens(it):
    t = it["q"] + " ".join(it["c"]) + it["e"]
    return all(d in OK for d in re.findall(r"class='fd'>(\d+)<", t)) and not any(w in t for w in BAD) and not re.search(r"\d\s*<span class='fr'>", t)


leer, comp, de, suma, prob = src("gen_es_matematicas_4_fracciones", 63209, "s1_leer", "s2_comparar", "s3_de_un_numero", "s4_suma", "s5_problema", extra=(dens,))

unit("fracciones", 9, "N",
     "Usa fracciones con denominador 2, 4, 8 y 16 (medios, cuartos, octavos y dieciseisavos) para expresar partes de una unidad y de una colección; las compara, suma y resta",
     "Fracciones", "Fracciones",
     "Ejercicios de matemáticas de 3.er grado de primaria: medios, cuartos y octavos, comparar fracciones, fracción de una cantidad, sumar y restar y problemas. 100 ejercicios con respuestas.",
     "Partes iguales de un entero", "Abajo: en cuántas partes. Arriba: cuántas.",
     ["Una <b>fracción</b> son partes iguales de un entero. En %s, el <b>denominador</b> (4) dice en cuántas partes se divide y el <b>numerador</b> (3), cuántas tomamos." % fr(3, 4),
      "Un entero son 2 medios, 4 cuartos u 8 octavos. Con el mismo denominador, es mayor la que tiene mayor numerador.",
      "Para calcular %s de 20: 20 ÷ 4 = 5 y 5 × 3 = 15." % fr(3, 4)],
     [("¿Cuánto es %s de 16?" % fr(1, 4), ["16 ÷ 4 = 4"], "4"), ("%s + %s" % (fr(3, 8), fr(2, 8)), ["3 + 2 = 5", "el denominador sigue siendo 8"], fr(5, 8))],
     [["Contar las partes sin colorear", "El numerador son las partes coloreadas."], ["Creer que %s &gt; %s porque 8 &gt; 4" % (fr(1, 8), fr(1, 4)), "Más partes: cada parte es más pequeña."],
      ["Sumar los denominadores", "%s + %s = %s, no %s." % (fr(1, 4), fr(2, 4), fr(3, 4), fr(3, 8))]],
     [("¿Cómo se lee una fracción?", "Primero el numerador y después el denominador: 3/4 se lee «tres cuartos» y 5/8, «cinco octavos»."),
      ("¿Cuántos cuartos tiene un entero?", "Cuatro: 4/4 = 1. Del mismo modo, 2/2 = 1 y 8/8 = 1.")],
     [("Leer y representar", [(leer, 20)]), ("Comparar fracciones", [(comp, 20)]), ("Fracción de una cantidad", [(de, 20)]), ("Sumar y restar", [(suma, 20)]), ("Problemas", [(prob, 20)])],
     63009, pic=tira(4, 3))
