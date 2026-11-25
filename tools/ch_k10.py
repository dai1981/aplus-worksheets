# -*- coding: utf-8 -*-
"""Schweiz Gymnasium 1. Klasse (Rahmenlehrplan Gymnasiale Maturitätsschulen, EDK 2024): Funktionen und Gleichungen.
Aus Deutschland Klasse 10 (gen_de_mathe_k10_*), dazu eigene Einheiten (ch_gym_a)."""
import ch_gym as G
import ch_gym_a as A

UNITS = [
    ("potenzfunktionen", 1, ["2.1 Funktionen"], "N", "gen_de_mathe_k10_potenzfunktionen"),
    ("polynomfunktionen", 2, ["2.1 Funktionen"], "N", "gen_de_mathe_k10_polynomfunktionen"),
    ("gleichungssysteme-mit-drei-unbekannten", 3, ["1.3 Gleichungen"], "A", G.build(A.lgs3)),
    ("exponentialfunktionen", 4, ["2.1 Funktionen"], "N", "gen_de_mathe_k10_exponentialfunktionen"),
    ("exponentielles-wachstum-und-zerfall", 5, ["2.1 Funktionen", "1.3 Gleichungen"], "N", "gen_de_mathe_k10_exponentielles_wachstum_und_zerfall"),
    ("logarithmus", 6, ["1.1 Zahlen", "1.3 Gleichungen"], "A", "gen_de_mathe_k10_logarithmus"),
]
FIX = {u[0]: G.gymfix for u in UNITS if isinstance(u[4], str)}
PRE = {}
