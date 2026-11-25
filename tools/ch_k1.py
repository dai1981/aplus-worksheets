# -*- coding: utf-8 -*-
"""Schweiz 1. Klasse (Lehrplan 21, Zyklus 1): Zahlenraum bis 20. Aus Deutschland Klasse 1 (gen_de_mathe_k1_*), auf Schweizer Schreibweise umgestellt; Geld selbst (Schweizer Münzen und Noten)."""
import ch_k3_geld

UNITS = [
    ("zahlen-bis-10", 1, ["MA.1.A.1", "MA.1.A.2"], "Z", "gen_de_mathe_k1_zahlen_bis_10"),
    ("zahlen-bis-20", 2, ["MA.1.A.1", "MA.1.C.2"], "Z", "gen_de_mathe_k1_zahlen_bis_20"),
    ("zahlen-vergleichen", 3, ["MA.1.A.2"], "Z", "gen_de_mathe_k1_zahlen_vergleichen"),
    ("zerlegen-und-ergaenzen", 4, ["MA.1.A.3", "MA.1.C.2"], "Z", "gen_de_mathe_k1_zerlegen_und_ergaenzen"),
    ("plus-bis-10", 5, ["MA.1.A.3"], "Z", "gen_de_mathe_k1_plus_bis_10"),
    ("minus-bis-10", 6, ["MA.1.A.3"], "Z", "gen_de_mathe_k1_minus_bis_10"),
    ("plus-und-minus-bis-20", 7, ["MA.1.A.3"], "Z", "gen_de_mathe_k1_plus_und_minus_bis_20"),
    ("plus-und-minus-ueber-die-10", 8, ["MA.1.A.3", "MA.1.C.1"], "Z", "gen_de_mathe_k1_plus_und_minus_ueber_die_10"),
    ("verdoppeln-und-halbieren", 9, ["MA.1.A.3"], "Z", "gen_de_mathe_k1_verdoppeln_und_halbieren"),
    ("rechengeschichten-und-sachaufgaben", 10, ["MA.3.C.2", "MA.3.C.3"], "G", "gen_de_mathe_k1_rechengeschichten_und_sachaufgaben"),
    ("geld", 11, ["MA.3.A.1", "MA.3.A.2"], "G", ch_k3_geld.build1),
    ("laengen-vergleichen-und-messen", 12, ["MA.3.A.1", "MA.3.A.2"], "G", "gen_de_mathe_k1_laengen_vergleichen_und_messen"),
    ("uhrzeit-und-tagesablauf", 13, ["MA.3.A.1"], "G", "gen_de_mathe_k1_uhrzeit_und_tagesablauf"),
    ("formen-und-koerper", 14, ["MA.2.A.1"], "F", "gen_de_mathe_k1_formen_und_koerper"),
    ("lage-und-richtung", 15, ["MA.2.C.3"], "F", "gen_de_mathe_k1_lage_und_richtung"),
    ("muster-und-zahlenfolgen", 16, ["MA.1.B.1", "MA.1.C.2"], "Z", "gen_de_mathe_k1_muster_und_zahlenfolgen"),
    ("strichlisten-und-tabellen", 17, ["MA.3.C.1"], "G", "gen_de_mathe_k1_strichlisten_und_tabellen"),
]
FIX = {}
PRE = {}
