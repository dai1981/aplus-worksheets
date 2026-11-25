# -*- coding: utf-8 -*-
"""Schweiz 5. Klasse (Lehrplan 21, Zyklus 2): Zahlen bis 1 Milliarde, Brüche, Grössen, Geometrie. Aus Deutschland Klasse 5 (gen_de_mathe_k5_*), ohne negative Zahlen und Potenzen (Zyklus 3)."""
import re

UNITS = [
    ("natuerliche-zahlen-und-stellenwerte", 1, ["MA.1.A.1", "MA.1.A.2"], "Z", "gen_de_mathe_k5_natuerliche_zahlen_und_stellenwerte"),
    ("runden-und-schaetzen", 2, ["MA.1.A.2", "MA.1.A.4"], "Z", "gen_de_mathe_k5_runden_und_schaetzen"),
    ("addieren-und-subtrahieren", 3, ["MA.1.A.3", "MA.1.C.1"], "Z", "gen_de_mathe_k5_addieren_und_subtrahieren"),
    ("multiplizieren-und-dividieren", 4, ["MA.1.A.3", "MA.1.C.1"], "Z", "gen_de_mathe_k5_multiplizieren_und_dividieren"),
    ("terme-und-rechengesetze", 5, ["MA.1.A.4", "MA.1.B.1"], "Z", "gen_de_mathe_k5_terme_und_rechengesetze"),
    ("teiler-vielfache-und-primzahlen", 6, ["MA.1.B.1", "MA.1.B.2"], "Z", "gen_de_mathe_k5_teiler_vielfache_und_primzahlen"),
    ("brueche-und-anteile", 7, ["MA.1.A.1", "MA.1.C.2"], "Z", "gen_de_mathe_k5_brueche_und_anteile"),
    ("muster-terme-und-variablen", 8, ["MA.1.C.2", "MA.3.A.3"], "Z", "gen_de_mathe_k5_muster_terme_und_variablen"),
    ("laengen-massen-und-zeit", 9, ["MA.3.A.1", "MA.3.A.2"], "G", "gen_de_mathe_k5_laengen_massen_und_zeit"),
    ("sachaufgaben-und-kombinatorik", 10, ["MA.3.C.1", "MA.3.C.2"], "G", "gen_de_mathe_k5_sachaufgaben_und_kombinatorik"),
    ("strecken-geraden-und-strahlen", 11, ["MA.2.A.1"], "F", "gen_de_mathe_k5_strecken_geraden_und_strahlen"),
    ("winkel", 12, ["MA.2.A.1", "MA.2.C.2"], "F", "gen_de_mathe_k5_winkel"),
    ("koordinatensystem", 13, ["MA.2.C.4"], "F", "gen_de_mathe_k5_koordinatensystem"),
    ("achsen-und-punktsymmetrie", 14, ["MA.2.B.1", "MA.2.C.3"], "F", "gen_de_mathe_k5_achsen_und_punktsymmetrie"),
    ("flaecheninhalt-und-umfang", 15, ["MA.2.A.3"], "F", "gen_de_mathe_k5_flaecheninhalt_und_umfang"),
    ("volumen-und-oberflaeche-von-quadern", 16, ["MA.2.A.3", "MA.2.C.1"], "F", "gen_de_mathe_k5_volumen_und_oberflaeche_von_quadern"),
    ("haeufigkeiten-und-diagramme", 17, ["MA.3.C.1"], "G", "gen_de_mathe_k5_haeufigkeiten_und_diagramme"),
]
FIX = {}


def _haeuf(mod):
    import importlib
    import ch_k4
    ch_k4._daten(importlib.import_module("gen_de_mathe_k4_daten_und_diagramme"))
    if hasattr(mod, "ENTF"):
        ch_k4._daten(mod)


PRE = {"haeufigkeiten-und-diagramme": _haeuf}


def _noneg(it):
    t = re.sub(r"<[^>]*>", " ", it["q"])
    return not re.search(r"(^|[\s(=,;:])−\d", t)


EXTRA = [_noneg]
