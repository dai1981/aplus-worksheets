# -*- coding: utf-8 -*-
"""México 5.º grado: Números naturales de hasta nueve cifras (Estudio de los números, Fase 5). Reutiliza España 6.º con otra semilla."""
from mx_common import src, unit, mx_text
import es_common as ES

leer, valor, desc, comp, vida = src("gen_es_matematicas_6_numeros_grandes", 65301, "s1_leer", "s2_valor", "s3_desc", "s4_comparar", "s5_vida", mx_=999999999, patch={"D": 9})

unit("numeros-hasta-cientos-de-millones", 1, "N",
     "Lee, escribe, compara y ordena números naturales de hasta nueve cifras; identifica el valor posicional de sus cifras y los descompone",
     "Números hasta cientos de millones", "Números grandes",
     "Ejercicios de matemáticas de 5.º grado de primaria: leer y escribir números de hasta nueve cifras, millones, valor posicional, descomposición y comparar. 100 ejercicios con respuestas.",
     "Lee de tres en tres cifras", "Millones, millares y unidades.",
     ["Los números grandes se leen por <b>periodos</b> de tres cifras: millones, millares y unidades. 305 040 200 se lee «trescientos cinco millones cuarenta mil doscientos».",
      "Un millón (1 000 000) son mil millares. Cada lugar vale 10 veces más que el de su derecha.",
      "Para comparar, cuenta las cifras: el que tiene más es mayor. Si tienen las mismas, compara de izquierda a derecha."],
     [("Escribe «doce millones trescientos mil cinco»", ["12 millones: 12 000 000", "300 mil: 300 000", "5"], "12 300 005"), ("¿Cuánto vale el 7 en 47 285 103?", ["está en las unidades de millón"], "7 000 000")],
     [["Olvidar los ceros de un periodo", "Doce millones cinco = 12 000 005."], ["Confundir millones y millares", "Separa en grupos de tres desde la derecha."], ["Comparar solo la primera cifra", "Primero cuenta cuántas cifras tiene cada número."]],
     [("¿Cuántos ceros tiene un millón?", "Seis: 1 000 000. Mil millones (1 000 000 000) tiene nueve ceros."),
      ("¿Cómo se lee un número de nueve cifras?", "Sepáralo en tres grupos de tres cifras desde la derecha y lee cada grupo seguido de «millones» y de «mil».")],
     [("Leer y escribir", [(leer, 20)]), ("Valor posicional", [(valor, 20)]), ("Descomponer", [(desc, 20)]), ("Comparar y ordenar", [(comp, 16), (leer, 4)]), ("Números en la vida diaria", [(vida, 20)])],
     65001, pic=mx_text(ES.tabla_valor(305040200, 9)), lv=5)
