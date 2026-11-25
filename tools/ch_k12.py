# -*- coding: utf-8 -*-
"""Schweiz Gymnasium 3. Klasse: Vektorgeometrie und Stochastik (eigene Einheiten ch_gym_b, Erwartungswert aus Deutschland Klasse 10)."""
import ch_gym as G
import ch_gym_b as B

UNITS = [
    ("vektoren", 1, ["3.3 Vektorgeometrie"], "G", G.build(B.vektoren)),
    ("skalarprodukt-und-winkel", 2, ["3.3 Vektorgeometrie"], "G", G.build(B.skalar)),
    ("geraden-und-ebenen-im-raum", 3, ["3.3 Vektorgeometrie"], "G", G.build(B.raum)),
    ("kombinatorik", 4, ["4.1 Kombinatorik"], "S", G.build(B.kombi)),
    ("bedingte-wahrscheinlichkeit", 5, ["4.2 Wahrscheinlichkeit"], "S", G.build(B.bedingt)),
    ("erwartungswert", 6, ["4.2 Wahrscheinlichkeit"], "S", "gen_de_mathe_k10_erwartungswert"),
    ("binomialverteilung", 7, ["4.2 Wahrscheinlichkeit"], "S", G.build(B.binom)),
]
FIX = {u[0]: G.gymfix for u in UNITS if isinstance(u[4], str)}
PRE = {}
