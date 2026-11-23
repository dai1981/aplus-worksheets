# -*- coding: utf-8 -*-
"""
España Matemáticas 3.º de Primaria: Probabilidad (Sentido estocástico)
Seguro, posible, imposible; más o menos probable; contar los casos; experimentos.
Reutiliza los generadores de 4.º (mismo ciclo), sin la probabilidad como fracción.
"""
from es_low import unit, src
import gen_es_matematicas_4_probabilidad as P4

SEED = 33921
suc, comp, rul, casos, exp = src("probabilidad", SEED, "s1_sucesos", "s2_comparar", "s2_ruleta", "s4_casos", "s5_experimento", sin=("fracción",))

unit(3, "probabilidad", 21, "S", "Incertidumbre: sucesos seguros, posibles e imposibles; comparación de la probabilidad de dos sucesos; experimentos sencillos",
     "Probabilidad: seguro, posible, imposible", "Probabilidad",
     "Fichas de matemáticas de 3.º de Primaria: seguro, posible o imposible, más o menos probable, contar casos y experimentos. 100 ejercicios con soluciones.",
     "Seguro, posible o imposible", "Más casos a favor, más probable.",
     ["Un suceso es <b>seguro</b> si pasa siempre, <b>imposible</b> si no puede pasar y <b>posible</b> si puede pasar o no.",
      "Es <b>más probable</b> lo que tiene más casos a favor: con 5 bolas rojas y 2 azules, es más probable sacar roja."],
     [("Sacar una bola verde de una bolsa con bolas rojas", ["No hay verdes"], "imposible"), ("Al tirar un dado, sacar un número menor que 7", ["Todos los números son menores que 7"], "seguro")],
     [["Pensar que «posible» es «seguro»", "Posible: puede pasar o no."], ["Mirar solo los colores, no cuántos hay", "Cuenta las bolas de cada color."], ["Creer que tras varias caras sale cruz", "Cada tirada es nueva."]],
     [("¿Qué es un suceso imposible?", "Un suceso que no puede ocurrir nunca, como sacar un 8 con un dado normal."), ("¿Cómo sé qué es más probable?", "Se cuentan los casos favorables: es más probable lo que tiene más.")],
     [("Seguro, posible o imposible", [(suc, 20)]), ("Más o menos probable", [(comp, 12), (rul, 8)]), ("Contar los casos", [(casos, 20)]), ("Ruletas y bolsas", [(rul, 12), (comp, 8)]),
      ("Experimentos", [(exp, 14), (suc, 6)])], 33021, P4.bolsa([("rojas", 5), ("azules", 2)]))
