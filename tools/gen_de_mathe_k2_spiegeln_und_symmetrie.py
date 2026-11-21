# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 2: Spiegeln und Symmetrie（Leitidee Raum und Form）
  python3 tools/gen_de_mathe_k2_spiegeln_und_symmetrie.py
Symmetrische Figuren erkennen, symmetrische Buchstaben, Spiegelbilder ergänzen, Symmetrie im Alltag.
Die Figuren auf Karopapier kommen aus Klasse 3 (gen_de_mathe_k3_achsensymmetrie) mit eigenem Zufall.
Fehler: Hälfte verschoben statt gespiegelt, „fast symmetrisch“ übersehen, die Spiegelachse an der falschen Stelle.
"""
import random
from de_common import mcq, lesson, example, make_unit, mix
import gen_de_mathe_k3_achsensymmetrie as k3

R = random.Random(49216)
k3.R = random.Random(49316)

ALLTAG = [("ein Schmetterling", True), ("ein Herz", True), ("eine Hand", False), ("ein Blatt von oben", True), ("ein Fußball von vorn", True),
          ("die Ziffer 8", True), ("die Ziffer 4", False), ("die Ziffer 7", False), ("die Ziffer 0", True), ("ein Regenschirm von der Seite", True),
          ("ein Schlüssel", False), ("ein Tannenbaum", True), ("ein Schuh von oben", False), ("ein Marienkäfer von oben", True),
          ("eine Schere, die offen ist", True), ("ein Fragezeichen", False), ("das Pluszeichen +", True), ("eine Gitarre von vorn", True),
          ("ein Haus mit Tür in der Mitte", True), ("ein Hase von der Seite", False), ("eine Brille", True), ("der Buchstabe R", False)]


def alltag():
    order = list(range(len(ALLTAG)))
    R.shuffle(order)
    st = {"i": 0}

    def mk():
        if st["i"] >= len(order):
            return None
        t, sym = ALLTAG[order[st["i"]]]
        st["i"] += 1
        ans = "Ja, es gibt eine Spiegelachse." if sym else "Nein, es gibt keine Spiegelachse."
        return mcq("Ist %s achsensymmetrisch?" % t, ans,
                   [v for v in ("Ja, es gibt eine Spiegelachse.", "Nein, es gibt keine Spiegelachse.") if v != ans] +
                   ["Nur wenn es bunt ist.", "Das kann man nicht sagen."],
                   ("Faltet man in der Mitte, passen beide Hälften aufeinander: <b>Ja</b>." if sym else
                    "Es gibt keine Faltlinie, bei der beide Hälften genau aufeinanderpassen: <b>Nein</b>."))
    return mk


def main():
    seen = set()
    sets = [
        ("Welche Figur ist symmetrisch?", mix(R, seen, [(k3.welche, 20)])),
        ("Symmetrische Buchstaben", mix(R, seen, [(k3.buchstabe, 20)])),
        ("Das Spiegelbild ergänzen", mix(R, seen, [(k3.ergaenzen, 20)])),
        ("Symmetrie im Alltag", mix(R, seen, [(alltag(), 20)])),
        ("Gemischte Übungen", mix(R, seen, [(k3.welche, 7), (k3.ergaenzen, 7), (k3.buchstabe, 6)])),
    ]
    body = lesson(
        ["Eine Figur ist <b>symmetrisch</b>, wenn man sie in der Mitte falten kann und beide Hälften genau aufeinanderliegen.",
         "Die Faltlinie heißt <b>Spiegelachse</b>.",
         "Beim Spiegeln wird links zu rechts. Was nah an der Achse liegt, bleibt nah an der Achse.",
         "Mit einem kleinen Spiegel auf der Achse kannst du prüfen, ob eine Figur symmetrisch ist."],
        [example("Ein Kästchen liegt 1 Kästchen links neben der Achse", ["gleicher Abstand", "andere Seite"], "1 Kästchen rechts neben der Achse"),
         example("Der Buchstabe A", ["Faltlinie senkrecht in der Mitte"], "symmetrisch")],
        [["Die Hälfte nur verschieben", "Spiegeln: links und rechts tauschen"],
         ["Fast gleiche Hälften für symmetrisch halten", "Jedes Kästchen genau vergleichen"],
         ["Vom Rand aus zählen", "Von der Spiegelachse aus zählen"]])
    faq = [
        {"q": "Wie erklärt man Symmetrie einem Kind?", "a": "Mit einem Klecksbild: Farbe auf eine Hälfte, Blatt zuklappen. Beide Hälften sehen gleich aus, nur gespiegelt."},
        {"q": "Welche Hilfsmittel helfen?", "a": "Ein kleiner Spiegel, Karopapier zum Abzählen und Faltblätter zum Ausschneiden."},
        {"q": "Wo gibt es Symmetrie im Alltag?", "a": "Bei Schmetterlingen, Blättern, Herzen, vielen Buchstaben und Verkehrsschildern."},
        {"q": "Ist ein Kreis symmetrisch?", "a": "Ja, sogar mit unendlich vielen Spiegelachsen: Jede Linie durch die Mitte ist eine Spiegelachse."},
    ]
    make_unit(R, "spiegeln-und-symmetrie", "R",
              "Die Schülerinnen und Schüler erkennen achsensymmetrische Figuren in der Umwelt und auf Karopapier, finden Spiegelachsen und ergänzen Spiegelbilder (Zusammenfassung).",
              "Spiegeln und Symmetrie",
              "Spiegeln und Symmetrie Klasse 2 – Arbeitsblätter mit Lösungen",
              "Symmetrie",
              "Spiegeln und Symmetrie für Klasse 2: symmetrische Figuren und Buchstaben erkennen, Spiegelbilder ergänzen und Symmetrie im Alltag. 100 Übungsaufgaben mit Lösungen, kostenlos.",
              "Falten: Beide Hälften passen genau aufeinander.",
              "Die Faltlinie heißt Spiegelachse.",
              body, faq, sets, 16, grade="klasse-2")


if __name__ == "__main__":
    main()
