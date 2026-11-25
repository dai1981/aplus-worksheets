# -*- coding: utf-8 -*-
"""Schweiz 8. Klasse (Lehrplan 21, Zyklus 3, Sekundarstufe I). Aus Deutschland Klasse 5–9 (gen_de_mathe_k*), auf Schweizer Schreibweise umgestellt."""

UNITS = [
    ("rationale-zahlen", 1, ["MA.1.A.1", "MA.1.A.2"], "Z", "gen_de_mathe_k7_rationale_zahlen"),
    ("rechnen-mit-rationalen-zahlen", 2, ["MA.1.A.3"], "Z", "gen_de_mathe_k7_rechnen_mit_rationalen_zahlen"),
    ("potenzen-und-zehnerpotenzen", 3, ["MA.1.A.3"], "Z", "gen_de_mathe_k8_potenzen_und_zehnerpotenzen"),
    ("quadratwurzeln-und-reelle-zahlen", 4, ["MA.1.A.1", "MA.1.A.3"], "Z", "gen_de_mathe_k8_quadratwurzeln_und_reelle_zahlen"),
    ("ausmultiplizieren-und-ausklammern", 5, ["MA.1.A.4"], "Z", "gen_de_mathe_k8_ausmultiplizieren_und_ausklammern"),
    ("binomische-formeln", 6, ["MA.1.A.4"], "Z", "gen_de_mathe_k8_binomische_formeln"),
    ("prozentuale-veraenderung", 7, ["MA.3.C.2"], "G", "gen_de_mathe_k7_prozentuale_veraenderung"),
    ("zinsrechnung", 8, ["MA.3.C.2", "MA.3.A.3"], "G", "gen_de_mathe_k7_zinsrechnung"),
    ("lineare-funktionen", 9, ["MA.3.A.3"], "G", "gen_de_mathe_k8_lineare_funktionen"),
    ("geradengleichungen-aufstellen", 10, ["MA.3.A.3"], "G", "gen_de_mathe_k8_geradengleichungen_aufstellen"),
    ("besondere-linien-im-dreieck", 11, ["MA.2.C.2"], "F", "gen_de_mathe_k7_besondere_linien_im_dreieck"),
    ("kongruenzsaetze", 12, ["MA.2.B.2"], "F", "gen_de_mathe_k8_kongruenzsaetze"),
    ("satz-des-thales", 13, ["MA.2.B.2"], "F", "gen_de_mathe_k8_satz_des_thales"),
    ("kreisumfang-und-kreisflaeche", 14, ["MA.2.A.3"], "F", "gen_de_mathe_k8_kreisumfang_und_kreisflaeche"),
    ("zylinder", 15, ["MA.2.A.3", "MA.2.C.1"], "F", "gen_de_mathe_k8_zylinder"),
    ("boxplots-und-kennwerte", 16, ["MA.3.C.1"], "G", "gen_de_mathe_k7_boxplots_und_kennwerte"),
    ("mehrstufige-zufallsexperimente", 17, ["MA.3.B.2", "MA.3.C.1"], "G", "gen_de_mathe_k8_mehrstufige_zufallsexperimente"),
]
def _mwst_fix(got):
    got["body"] = got["body"].replace("In Deutschland gilt meist 19 % Mehrwertsteuer, für Lebensmittel 7 %.",
                                      "In der Schweiz gilt 8.1 % Mehrwertsteuer (MWST), für Lebensmittel und Bücher 2.6 %.")
    for f in got["faq"]:
        if "Mehrwertsteuer in Deutschland" in f["q"]:
            f["q"] = "Wie hoch ist die Mehrwertsteuer in der Schweiz?"
            f["a"] = "Der Normalsatz ist 8.1 %. Für Lebensmittel und Bücher gilt der reduzierte Satz von 2.6 %."


FIX = {"prozentuale-veraenderung": _mwst_fix}
from fractions import Fraction as Fr


def _mwst(mod):
    """Schweizer Mehrwertsteuer (MWST): 8.1 % Normalsatz, 2.6 % reduzierter Satz (Lebensmittel)"""
    R, mcq, eur, P = mod.R, mod.mcq, mod.eur, mod.P

    def mwst():
        kind = R.choice(["netto", "brutto", "lebensmittel"])
        if kind == "netto":
            n = R.choice(range(200, 3001, 200))
            b = Fr(n * 1081, 1000)
            return mcq("Ein Gerät kostet ohne Mehrwertsteuer %d €. Wie viel kostet es mit 8,1%s Mehrwertsteuer (MWST)?" % (n, P), eur(b),
                       [eur(Fr(n * 81, 1000)), eur(n + 81) if n + 81 != b else eur(n + 8), eur(Fr(n * 919, 1000)), eur(Fr(n * 181, 100))],
                       "%d € · 1,081 = <b>%s</b>." % (n, eur(b)))
        if kind == "brutto":
            n = R.choice(range(200, 3001, 200))
            b = Fr(n * 1081, 1000)
            return mcq("Ein Preis mit 8,1%s Mehrwertsteuer ist %s. Wie hoch ist der Preis ohne Mehrwertsteuer?" % (P, eur(b)), eur(n),
                       [eur(b * Fr(919, 1000)) if (b * Fr(919, 1000) * 20).denominator == 1 else eur(n + 20), eur(n - 20), eur(n + 100)],
                       "%s : 1,081 = <b>%s</b>. (Nicht 8,1%s vom Endpreis abziehen.)" % (eur(b), eur(n), P))
        n = R.choice(range(50, 1001, 50))
        b = Fr(n * 1026, 1000)
        return mcq("Lebensmittel haben 2,6%s Mehrwertsteuer. Ein Einkauf kostet ohne Steuer %d €. Wie viel kostet er mit Steuer?" % (P, n), eur(b),
                   [eur(Fr(n * 1081, 1000)) if (Fr(n * 1081, 1000) * 20).denominator == 1 else eur(b + 1), eur(Fr(n * 26, 1000)) if (Fr(n * 26, 1000) * 20).denominator == 1 else eur(n + 26), eur(n + 26)],
                   "%d € · 1,026 = <b>%s</b>." % (n, eur(b)))
    mod.mwst = mwst


PRE = {"prozentuale-veraenderung": _mwst}
