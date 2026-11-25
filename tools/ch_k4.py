# -*- coding: utf-8 -*-
"""Schweiz 4. Klasse (Lehrplan 21, Zyklus 2, Orientierungspunkt): Zahlenraum bis 1 Million. Aus Deutschland Klasse 4 (gen_de_mathe_k4_*), auf Schweizer Schreibweise umgestellt."""

import ch_k3_geld

UNITS = [
    ("zahlen-bis-1-million", 1, ["MA.1.A.1", "MA.1.A.2"], "Z", "gen_de_mathe_k4_zahlen_bis_1_million"),
    ("runden-und-ueberschlagen", 2, ["MA.1.A.2", "MA.1.A.4"], "Z", "gen_de_mathe_k4_runden_und_ueberschlagen"),
    ("schriftlich-addieren-und-subtrahieren", 3, ["MA.1.A.3", "MA.1.C.1"], "Z", "gen_de_mathe_k4_schriftlich_addieren_und_subtrahieren"),
    ("schriftliche-multiplikation", 4, ["MA.1.A.3", "MA.1.C.1"], "Z", "gen_de_mathe_k4_schriftliche_multiplikation"),
    ("schriftliche-division", 5, ["MA.1.A.3", "MA.1.C.1"], "Z", "gen_de_mathe_k4_schriftliche_division"),
    ("rechengesetze-und-klammern", 6, ["MA.1.A.4", "MA.1.B.1"], "Z", "gen_de_mathe_k4_rechengesetze_und_klammern"),
    ("brueche-im-alltag", 7, ["MA.1.A.1", "MA.1.C.2"], "Z", "gen_de_mathe_k4_brueche"),
    ("sachaufgaben", 8, ["MA.3.C.2", "MA.3.C.3"], "G", "gen_de_mathe_k4_sachaufgaben"),
    ("laengen-in-dezimalschreibweise", 9, ["MA.3.A.1", "MA.3.A.2"], "G", "gen_de_mathe_k4_laengen"),
    ("gewichte-und-tonnen", 10, ["MA.3.A.1", "MA.3.A.2"], "G", "gen_de_mathe_k4_gewichte"),
    ("rauminhalte", 11, ["MA.3.A.1", "MA.3.A.2"], "G", "gen_de_mathe_k4_rauminhalte"),
    ("rechnen-mit-geld", 12, ["MA.3.A.2", "MA.3.C.2"], "G", ch_k3_geld.build4),
    ("zeit-und-kalender", 13, ["MA.3.A.1", "MA.3.A.2"], "G", "gen_de_mathe_k4_zeit"),
    ("massstab", 14, ["MA.2.C.4", "MA.3.A.3"], "F", "gen_de_mathe_k4_massstab"),
    ("umfang-und-flaecheninhalt", 15, ["MA.2.A.3"], "F", "gen_de_mathe_k4_umfang_und_flaecheninhalt"),
    ("parallel-senkrecht-und-vierecke", 16, ["MA.2.A.1", "MA.2.C.2"], "F", "gen_de_mathe_k4_parallel_senkrecht_und_vierecke"),
    ("wuerfel-und-quader", 17, ["MA.2.C.1", "MA.2.C.3"], "F", "gen_de_mathe_k4_wuerfel_und_quader"),
    ("daten-und-diagramme", 18, ["MA.3.C.1"], "G", "gen_de_mathe_k4_daten_und_diagramme"),
    ("kombinatorik-und-wahrscheinlichkeit", 19, ["MA.3.B.2", "MA.3.C.1"], "G", "gen_de_mathe_k4_kombinatorik_und_wahrscheinlichkeit"),
]
FIX = {}


def _daten(mod):
    # Strassenkilometer zwischen Schweizer Städten (Berlin → Bern, Hamburg → Basel, München → Zürich, Köln → Luzern, Leipzig → Thun)
    mod.ENTF = {("Berlin", "Hamburg"): 97, ("Berlin", "München"): 125, ("Berlin", "Köln"): 111, ("Hamburg", "München"): 87, ("Hamburg", "Köln"): 100,
                ("München", "Köln"): 52, ("Berlin", "Leipzig"): 30, ("Hamburg", "Leipzig"): 125, ("München", "Leipzig"): 150, ("Köln", "Leipzig"): 90}
    mod.STAEDTE = [("Zürich", 427000), ("Genf", 204000), ("Basel", 174000), ("Lausanne", 141000), ("Bern", 134000), ("Winterthur", 117000),
                   ("Luzern", 83000), ("St. Gallen", 76000), ("Lugano", 63000), ("Biel", 56000), ("Thun", 44000), ("Köniz", 43000), ("Freiburg", 38000)]


PRE = {"daten-und-diagramme": _daten}
