# -*- coding: utf-8 -*-
"""Schweiz Gymnasium 2. Klasse: Trigonometrie, Folgen und Reihen, gebrochenrationale Funktionen.
Aus Deutschland Klasse 10 (gen_de_mathe_k10_*), dazu eigene Einheiten (ch_gym_a)."""
import ch_gym as G
import ch_gym_a as A

UNITS = [
    ("bogenmass-und-kreisausschnitt", 1, ["3.1 Elementargeometrie", "3.2 Trigonometrie"], "G", "gen_de_mathe_k10_bogenmass_und_kreisausschnitt"),
    ("trigonometrie-am-einheitskreis", 2, ["3.2 Trigonometrie"], "G", "gen_de_mathe_k10_trigonometrie_am_einheitskreis"),
    ("sinus-und-kosinusfunktion", 3, ["2.1 Funktionen", "3.2 Trigonometrie"], "N", "gen_de_mathe_k10_sinus_und_kosinusfunktion"),
    ("sinussatz-und-kosinussatz", 4, ["3.2 Trigonometrie"], "G", "gen_de_mathe_k10_sinussatz_und_kosinussatz"),
    ("arithmetische-und-geometrische-folgen", 5, ["2.1 Funktionen"], "N", G.build(A.folgen)),
    ("reihen-und-grenzwerte", 6, ["2.1 Funktionen"], "N", G.build(A.reihen)),
    ("gebrochenrationale-funktionen-und-asymptoten", 7, ["2.1 Funktionen"], "N", G.build(A.gebrochen)),
]
FIX = {u[0]: G.gymfix for u in UNITS if isinstance(u[4], str)}
PRE = {}
