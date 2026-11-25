# -*- coding: utf-8 -*-
"""Schweiz 6. Klasse (Lehrplan 21, Ende Zyklus 2): Brüche, Dezimalzahlen, Prozente, Proportionalität, Dreiecke und Vierecke, Kreise. Aus Deutschland Klasse 6 (gen_de_mathe_k6_*), ohne negative Zahlen und Gleichungen (Zyklus 3)."""
from ch_k5 import _noneg

UNITS = [
    ("brueche-erweitern-und-kuerzen", 1, ["MA.1.A.4", "MA.1.C.2"], "Z", "gen_de_mathe_k6_brueche_erweitern_und_kuerzen"),
    ("brueche-vergleichen-und-ordnen", 2, ["MA.1.A.2"], "Z", "gen_de_mathe_k6_brueche_vergleichen_und_ordnen"),
    ("gemischte-zahlen", 3, ["MA.1.A.1"], "Z", "gen_de_mathe_k6_gemischte_zahlen"),
    ("brueche-addieren-und-subtrahieren", 4, ["MA.1.A.3"], "Z", "gen_de_mathe_k6_brueche_addieren_und_subtrahieren"),
    ("dezimalzahlen-und-stellenwerte", 5, ["MA.1.A.1", "MA.1.C.2"], "Z", "gen_de_mathe_k6_dezimalzahlen_und_stellenwerte"),
    ("brueche-und-dezimalzahlen", 6, ["MA.1.A.1", "MA.1.B.3"], "Z", "gen_de_mathe_k6_brueche_und_dezimalzahlen"),
    ("dezimalzahlen-addieren-und-subtrahieren", 7, ["MA.1.A.3"], "Z", "gen_de_mathe_k6_dezimalzahlen_addieren_und_subtrahieren"),
    ("dezimalzahlen-multiplizieren-und-dividieren", 8, ["MA.1.A.3", "MA.1.B.2"], "Z", "gen_de_mathe_k6_dezimalzahlen_multiplizieren_und_dividieren"),
    ("prozente", 9, ["MA.1.A.1", "MA.3.A.3"], "Z", "gen_de_mathe_k6_prozente"),
    ("zuordnungen-und-dreisatz", 10, ["MA.3.A.3", "MA.3.C.3"], "G", "gen_de_mathe_k6_zuordnungen_und_dreisatz"),
    ("sachaufgaben-mit-bruechen-und-dezimalzahlen", 11, ["MA.3.C.2"], "G", "gen_de_mathe_k6_sachaufgaben_mit_bruechen_und_dezimalzahlen"),
    ("dreiecke-und-vierecke", 12, ["MA.2.A.1", "MA.2.C.2"], "F", "gen_de_mathe_k6_dreiecke_und_vierecke"),
    ("kreise", 13, ["MA.2.C.2"], "F", "gen_de_mathe_k6_kreise"),
    ("daten-und-wahrscheinlichkeit", 14, ["MA.3.B.2", "MA.3.C.1"], "G", "gen_de_mathe_k6_daten_und_wahrscheinlichkeit"),
]
FIX = {}
PRE = {}
EXTRA = [_noneg]
