# -*- coding: utf-8 -*-
"""Schweiz 3. Klasse (Lehrplan 21, Zyklus 2): Zahlenraum bis 1000. Die meisten Einheiten aus Deutschland Klasse 3 (gen_de_mathe_k3_*), auf Schweizer Schreibweise umgestellt."""
import ch_k3_geld

UNITS = [
    ("zahlen-bis-1000", 1, ["MA.1.A.1", "MA.1.C.2"], "Z", "gen_de_mathe_k3_zahlen_bis_1000"),
    ("zahlen-vergleichen-und-ordnen", 2, ["MA.1.A.2"], "Z", "gen_de_mathe_k3_zahlen_vergleichen_und_ordnen"),
    ("runden-und-ueberschlagen", 3, ["MA.1.A.2", "MA.1.A.4"], "Z", "gen_de_mathe_k3_runden_und_ueberschlagen"),
    ("plus-und-minus-bis-1000", 4, ["MA.1.A.3"], "Z", "gen_de_mathe_k3_plus_und_minus_bis_1000"),
    ("schriftliche-addition", 5, ["MA.1.A.3", "MA.1.C.1"], "Z", "gen_de_mathe_k3_schriftliche_addition"),
    ("schriftliche-subtraktion", 6, ["MA.1.A.3", "MA.1.C.1"], "Z", "gen_de_mathe_k3_schriftliche_subtraktion"),
    ("einmaleins", 7, ["MA.1.A.3"], "Z", "gen_de_mathe_k3_einmaleins"),
    ("multiplizieren-und-dividieren", 8, ["MA.1.A.3", "MA.1.B.1"], "Z", "gen_de_mathe_k3_multiplizieren_und_dividieren"),
    ("dividieren-mit-rest", 9, ["MA.1.A.3"], "Z", "gen_de_mathe_k3_dividieren_mit_rest"),
    ("sachaufgaben", 10, ["MA.3.C.2", "MA.3.C.3"], "G", "gen_de_mathe_k3_sachaufgaben"),
    ("geld", 11, ["MA.3.A.2", "MA.3.C.2"], "G", ch_k3_geld.build),
    ("laengen", 12, ["MA.3.A.1", "MA.3.A.2"], "G", "gen_de_mathe_k3_laengen"),
    ("gewichte", 13, ["MA.3.A.1", "MA.3.A.2"], "G", "gen_de_mathe_k3_gewichte"),
    ("uhrzeit-und-zeitspannen", 14, ["MA.3.A.1", "MA.3.A.2"], "G", "gen_de_mathe_k3_uhrzeit_und_zeitspannen"),
    ("koerper-und-figuren", 15, ["MA.2.A.1", "MA.2.C.1"], "F", "gen_de_mathe_k3_koerper_und_figuren"),
    ("achsensymmetrie", 16, ["MA.2.B.1", "MA.2.C.2"], "F", "gen_de_mathe_k3_achsensymmetrie"),
    ("zahlenfolgen-und-muster", 17, ["MA.1.B.1", "MA.1.C.2"], "Z", "gen_de_mathe_k3_zahlenfolgen_und_muster"),
    ("diagramme-und-tabellen", 18, ["MA.3.C.1"], "G", "gen_de_mathe_k3_diagramme_und_tabellen"),
    ("wahrscheinlichkeit", 19, ["MA.3.B.2", "MA.3.C.1"], "G", "gen_de_mathe_k3_wahrscheinlichkeit"),
]


def _einmaleins(g):
    for f in g["faq"]:
        if "Malpunkt" in f["a"]:
            f["q"] = "Warum schreibt man × und :?"
            f["a"] = "In der Schweiz schreibt man für mal das Zeichen × (3 × 4) und für geteilt einen Doppelpunkt (12 : 3)."


FIX = {"einmaleins": _einmaleins}
