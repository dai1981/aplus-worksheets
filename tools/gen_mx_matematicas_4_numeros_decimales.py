# -*- coding: utf-8 -*-
"""México 4.º grado: Números decimales hasta centésimos (Estudio de los números). Reutiliza España 4.º con otra semilla."""
from mx_common import src, unit, mx_text
import es_common as ES

frac, leer, comp, recta, vida = src("gen_es_matematicas_4_numeros_decimales", 64212, "s1_fraccion", "s2_leer", "s3_comparar", "s4_recta", "s5_vida")

unit("numeros-decimales", 10, "N",
     "Lee, escribe y ordena números decimales hasta centésimos; los relaciona con fracciones decimales (décimos y centésimos); los ubica en la recta numérica y los usa en situaciones de dinero y medición",
     "Números decimales: décimos y centésimos", "Números decimales",
     "Ejercicios de matemáticas de 4.º grado de primaria: décimos y centésimos, fracciones decimales, leer, comparar y ordenar decimales, la recta numérica y dinero. 100 ejercicios con respuestas.",
     "1 décimo = 10 centésimos", "El punto separa enteros y decimales.",
     ["El <b>punto decimal</b> separa la parte entera de la parte decimal. La primera cifra después del punto son los <b>décimos</b> y la segunda, los <b>centésimos</b>.",
      "0.1 = %s y 0.01 = %s. Por eso 2.35 son 2 enteros y 35 centésimos." % (ES.fr(1, 10), ES.fr(1, 100)),
      "Para comparar, mira primero los enteros y después los décimos: 3.4 &gt; 3.25 porque 4 décimos &gt; 2 décimos (piensa 3.40 y 3.25)."],
     [("Escribe %s como decimal" % ES.fr(7, 100), ["7 centésimos", "dos cifras después del punto"], "0.07"), ("Compara 0.5 y 0.45", ["0.50 y 0.45", "50 &gt; 45"], "0.5 &gt; 0.45")],
     [["Pensar que 0.45 &gt; 0.5 porque 45 &gt; 5", "Compara 0.50 con 0.45."], ["Escribir %s como 0.7" % ES.fr(7, 100), "Son centésimos: 0.07."], ["Leer 2.05 como «dos punto cinco»", "Son 2 enteros y 5 centésimos."]],
     [("¿Qué es un centésimo?", "Es una de las 100 partes iguales de una unidad: 0.01. Un peso tiene 100 centavos, y cada centavo es un centésimo de peso."),
      ("¿Cómo se lee 4.36?", "«Cuatro enteros, treinta y seis centésimos». Con dinero: $4.36 son 4 pesos con 36 centavos.")],
     [("Fracciones decimales", [(frac, 20)]), ("Leer y escribir decimales", [(leer, 20)]), ("Comparar y ordenar", [(comp, 20)]), ("La recta numérica", [(recta, 20)]), ("Decimales en la vida diaria", [(vida, 20)])],
     64010, pic=mx_text(ES.tabla_decimal(2.35)) if hasattr(ES, "tabla_decimal") else "", lv=4)
