# -*- coding: utf-8 -*-
"""Schweiz Gymnasium 4. Klasse (Maturajahr): Differenzial- und Integralrechnung, Statistik (eigene Einheiten ch_gym_c)."""
import ch_gym as G
import ch_gym_c as N

UNITS = [
    ("ableitung-und-tangente", 1, ["2.2 Differenzialrechnung"], "N", G.build(N.tangente)),
    ("ableitungsregeln", 2, ["2.2 Differenzialrechnung"], "N", G.build(N.regeln)),
    ("kurvendiskussion", 3, ["2.1 Funktionen", "2.2 Differenzialrechnung"], "N", G.build(N.kurven)),
    ("extremwertaufgaben", 4, ["2.2 Differenzialrechnung"], "N", G.build(N.extrem)),
    ("stammfunktionen", 5, ["2.3 Integralrechnung"], "N", G.build(N.stamm)),
    ("bestimmtes-integral-und-flaechen", 6, ["2.3 Integralrechnung"], "N", G.build(N.integral)),
    ("statistische-kennzahlen", 7, ["4.3 Statistik"], "S", G.build(N.statistik)),
]
FIX = {}
PRE = {}
