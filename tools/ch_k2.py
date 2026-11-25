# -*- coding: utf-8 -*-
"""Schweiz 2. Klasse (Lehrplan 21, Zyklus 1): Zahlenraum bis 100, Einmaleins. Aus Deutschland Klasse 2 (gen_de_mathe_k2_*), auf Schweizer Schreibweise umgestellt."""

UNITS = [
    ("zahlen-bis-100", 1, ["MA.1.A.1", "MA.1.C.2"], "Z", "gen_de_mathe_k2_zahlen_bis_100"),
    ("zahlen-vergleichen-und-ordnen", 2, ["MA.1.A.2"], "Z", "gen_de_mathe_k2_zahlen_vergleichen_und_ordnen"),
    ("plus-und-minus-bis-20", 3, ["MA.1.A.3"], "Z", "gen_de_mathe_k2_plus_und_minus_bis_20"),
    ("plus-bis-100", 4, ["MA.1.A.3"], "Z", "gen_de_mathe_k2_plus_bis_100"),
    ("minus-bis-100", 5, ["MA.1.A.3"], "Z", "gen_de_mathe_k2_minus_bis_100"),
    ("ergaenzen-bis-100", 6, ["MA.1.A.3", "MA.1.A.4"], "Z", "gen_de_mathe_k2_ergaenzen_bis_100"),
    ("multiplizieren-verstehen", 7, ["MA.1.A.3", "MA.1.C.2"], "Z", "gen_de_mathe_k2_multiplizieren_verstehen"),
    ("einmaleins-mit-2-5-und-10", 8, ["MA.1.A.3"], "Z", "gen_de_mathe_k2_einmaleins_mit_2_5_und_10"),
    ("kleines-einmaleins", 9, ["MA.1.A.3"], "Z", "gen_de_mathe_k2_kleines_einmaleins"),
    ("geteilt-aufteilen-und-verteilen", 10, ["MA.1.A.3"], "Z", "gen_de_mathe_k2_geteilt_aufteilen_und_verteilen"),
    ("sachaufgaben", 11, ["MA.3.C.2", "MA.3.C.3"], "G", "gen_de_mathe_k2_sachaufgaben"),
    ("geld", 12, ["MA.3.A.2"], "G", "gen_de_mathe_k2_geld"),
    ("laengen", 13, ["MA.3.A.1", "MA.3.A.2"], "G", "gen_de_mathe_k2_laengen"),
    ("uhrzeit", 14, ["MA.3.A.1", "MA.3.A.2"], "G", "gen_de_mathe_k2_uhrzeit"),
    ("flaechen-und-koerper", 15, ["MA.2.A.1", "MA.2.C.1"], "F", "gen_de_mathe_k2_flaechen_und_koerper"),
    ("spiegeln-und-symmetrie", 16, ["MA.2.B.1", "MA.2.C.2"], "F", "gen_de_mathe_k2_spiegeln_und_symmetrie"),
    ("zahlenmauern-und-muster", 17, ["MA.1.B.1", "MA.1.C.2"], "Z", "gen_de_mathe_k2_zahlenmauern_und_muster"),
    ("strichlisten-und-diagramme", 18, ["MA.3.C.1"], "G", "gen_de_mathe_k2_strichlisten_und_diagramme"),
]
import de_common as D


def _geld(g):
    g["body"] = D.lesson(
        ["In der Schweiz gibt es Münzen (5 Rp. bis 5 Fr.) und Noten (10 Fr. bis 1000 Fr.).",
         "<b>1 Fr. = 100 Rp.</b> 3 Fr. 40 Rp. sind 340 Rp.",
         "Zähle Geld vom grössten Wert zum kleinsten: erst die Noten, dann die Münzen.",
         "Beim Rückgeld ergänzt du vom Preis bis zum bezahlten Betrag."],
        [D.example("20 Fr. + 10 Fr. + 5 Fr. + 2 Fr.", ["20 + 10 = 30", "30 + 5 = 35", "35 + 2 = 37"], "37 Fr."),
         D.example("Ein Buch kostet 13 Fr., du gibst 20 Fr.", ["13 Fr. + 7 Fr. = 20 Fr."], "7 Fr. Rückgeld")],
        [["Münzen zählen statt Werte addieren", "Den Wert jeder Münze addieren"], ["1 Fr. = 10 Rp.", "1 Fr. = 100 Rp."],
         ["Beim Rückgeld den Preis nennen", "Gefragt ist, was zurückkommt"]],
        extra=D.table(["Münzen", "Noten"], [["5 Rp., 10 Rp., 20 Rp., ½ Fr., 1 Fr., 2 Fr., 5 Fr.", "10 Fr., 20 Fr., 50 Fr., 100 Fr., 200 Fr., 1000 Fr."]]))
    for f in g["faq"]:
        if f["q"].startswith("Welche Münzen"):
            f["q"] = "Welche Münzen und Noten gibt es in der Schweiz?"
            f["a"] = "Münzen: 5, 10 und 20 Rappen, ½ Franken, 1, 2 und 5 Franken. Noten: 10, 20, 50, 100, 200 und 1000 Franken."
        if "mit Punkt" in f["q"] or "Komma" in f["q"]:
            f["q"] = "Rechnen Kinder in der 2. Klasse schon mit Punkt?"
            f["a"] = "Meist noch nicht. In der 2. Klasse schreibt man 3 Fr. 40 Rp. Die Schreibweise 3.40 Fr. kommt in der 3. Klasse."


FIX = {"geld": _geld}
PRE = {}
