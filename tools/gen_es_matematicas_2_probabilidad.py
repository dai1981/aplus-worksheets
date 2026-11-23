# -*- coding: utf-8 -*-
"""
España Matemáticas 2.º de Primaria: Seguro, posible o imposible (Sentido estocástico)
Reutiliza los generadores de 4.º sin la probabilidad como fracción ni números grandes.
"""
from es_low import unit, src
import gen_es_matematicas_4_probabilidad as P4

SEED = 32921
suc, comp, rul, exp = src("probabilidad", SEED, "s1_sucesos", "s2_comparar", "s2_ruleta", "s5_experimento", mx=1000, sin=("fracción",))

unit(2, "seguro-posible-o-imposible", 18, "S", "Incertidumbre en situaciones de la vida cotidiana: sucesos seguros, posibles e imposibles; más y menos probable",
     "Seguro, posible o imposible", "Probabilidad",
     "Fichas de matemáticas de 2.º de Primaria: sucesos seguros, posibles e imposibles, más o menos probable, bolsas, ruletas y experimentos. 100 ejercicios con soluciones.",
     "Seguro, posible o imposible", "Más bolas de un color, más probable.",
     ["Un suceso es <b>seguro</b> si pasa siempre, <b>imposible</b> si no puede pasar y <b>posible</b> si a veces pasa y a veces no.",
      "Si en una bolsa hay más bolas rojas que azules, es <b>más probable</b> sacar una roja."],
     [("Sacar una bola verde de una bolsa con bolas rojas", ["No hay verdes"], "imposible"), ("Mañana sale el sol por el este", ["Pasa siempre"], "seguro")],
     [["Pensar que «posible» es «seguro»", "Posible: puede pasar o no."], ["Mirar solo los colores, no cuántas bolas hay", "Cuenta las bolas de cada color."], ["Creer que siempre sale lo más probable", "Lo más probable no es seguro."]],
     [("¿Qué es un suceso imposible?", "Un suceso que no puede ocurrir nunca, como sacar un 7 con un dado normal."), ("¿Qué es más probable?", "Lo que tiene más posibilidades: si hay 6 bolas rojas y 1 azul, es más probable sacar roja.")],
     [("Seguro, posible o imposible", [(suc, 20)]), ("Más o menos probable", [(comp, 20)]), ("Ruletas", [(rul, 20)]), ("Experimentos", [(exp, 20)]), ("Repaso", [(suc, 8), (comp, 6), (rul, 6)])],
     32018, P4.bolsa([("rojas", 5), ("azules", 2)]))
