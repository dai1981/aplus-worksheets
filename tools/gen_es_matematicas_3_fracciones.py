# -*- coding: utf-8 -*-
"""
España Matemáticas 3.º de Primaria: Fracciones (Sentido numérico)
Leer y representar, comparar, fracción de un número, sumar y restar con el mismo denominador, problemas.
Reutiliza los generadores de 4.º (mismo ciclo) sin números mixtos.
"""
from es_low import unit, src
from es_common import fr, tira

SEED = 33909
leer, comp, de, suma, prob = src("fracciones", SEED, "s1_leer", "s2_comparar", "s3_de_un_numero", "s4_suma", "s5_problema", sin=("mixto", "1 y "))

unit(3, "fracciones", 9, "N", "Fracciones en contextos cotidianos: lectura, representación y comparación; fracción de una cantidad; suma y resta con el mismo denominador",
     "Fracciones", "Fracciones",
     "Fichas de matemáticas de 3.º de Primaria: leer y representar fracciones, comparar, fracción de un número, sumar y restar y problemas. 100 ejercicios con soluciones.",
     "Partes iguales de una unidad", "Abajo: en cuántas partes. Arriba: cuántas.",
     ["Una <b>fracción</b> son partes iguales de una unidad. En %s, el <b>denominador</b> (4) dice en cuántas partes se divide y el <b>numerador</b> (3), cuántas tomamos." % fr(3, 4),
      "Con el mismo denominador, es mayor la que tiene mayor numerador.", "Para calcular %s de 20: 20 : 4 = 5 y 5 × 3 = 15." % fr(3, 4)],
     [("¿Cuánto es %s de 12?" % fr(1, 3), ["12 : 3 = 4"], "4"), ("%s + %s" % (fr(2, 6), fr(3, 6)), ["2 + 3 = 5", "el denominador sigue siendo 6"], fr(5, 6))],
     [["Contar las partes sin colorear", "El numerador son las partes coloreadas."], ["Creer que %s &gt; %s porque 8 &gt; 4" % (fr(1, 8), fr(1, 4)), "Más partes: cada parte es más pequeña."],
      ["Sumar los denominadores", "%s + %s = %s, no %s." % (fr(1, 5), fr(2, 5), fr(3, 5), fr(3, 10))]],
     [("¿Cómo se lee una fracción?", "Primero el numerador y después el denominador: 3/4 se lee «tres cuartos» y 2/5, «dos quintos»."),
      ("¿Cómo se calcula la fracción de un número?", "Se divide el número entre el denominador y se multiplica por el numerador.")],
     [("Leer y representar", [(leer, 20)]), ("Comparar fracciones", [(comp, 20)]), ("Fracción de un número", [(de, 20)]), ("Sumar y restar", [(suma, 20)]), ("Problemas", [(prob, 20)])],
     33009, tira(4, 3))
