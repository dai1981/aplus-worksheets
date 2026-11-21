# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 1: Formen und Körper（Leitidee Raum und Form）
  python3 tools/gen_de_mathe_k1_formen_und_koerper.py
Ebene Formen erkennen (Kreis, Dreieck, Quadrat, Rechteck), Ecken zählen, Formen zählen, Was passt nicht?, Körper erkennen und in der Umwelt finden.
Formen- und Körperaufgaben kommen aus Klasse 2 und 3 (mit eigenem Zufall).
Fehler: Quadrat und Rechteck verwechselt, Kreis und Kugel verwechselt, gedrehte Formen nicht erkannt.
"""
import random
from de_common import mcq, lesson, example, make_unit, mix
from de_k2 import de
from k_pics import lettered_shapes_svg
import gen_de_mathe_k2_flaechen_und_koerper as k2

R = random.Random(49414)
k2.R = random.Random(49464)
k2.k3.R = random.Random(49465)

NAME = {"circle": "Kreis", "square": "Quadrat", "triangle": "Dreieck", "rectangle": "Rechteck"}
COLS = ["red", "blue", "yellow", "green"]
DE_COL = {"red": "rot", "blue": "blau", "yellow": "gelb", "green": "grün"}


def anders():
    kind = R.choice(["form", "farbe"])
    if kind == "form":
        a, b = R.sample([k for k in NAME if k != "rectangle"], 2)
        col = R.choice(COLS)
        items = [(a, col)] * 4
        i = R.randrange(4)
        items[i] = (b, col)
        pic = de(lettered_shapes_svg(items), "vier Formen A bis D")
        return mcq(pic + "Welche Form passt nicht dazu?", "ABCD"[i], [c for c in "ABCD" if c != "ABCD"[i]],
                   "Drei Formen sind %se, Form <b>%s</b> ist ein %s." % (NAME[a], "ABCD"[i], NAME[b]))
    k = R.choice([k for k in NAME if k != "rectangle"])
    c1, c2 = R.sample(COLS, 2)
    items = [(k, c1)] * 4
    i = R.randrange(4)
    items[i] = (k, c2)
    pic = de(lettered_shapes_svg(items), "vier Formen A bis D")
    return mcq(pic + "Welche Form hat eine andere Farbe?", "ABCD"[i], [c for c in "ABCD" if c != "ABCD"[i]],
               "Drei sind %s, Form <b>%s</b> ist %s." % (DE_COL[c1], "ABCD"[i], DE_COL[c2]))


def main():
    seen = set()
    sets = [
        ("Formen erkennen", mix(R, seen, [(k2.figur, 20)])),
        ("Ecken zählen und Formen zählen", mix(R, seen, [(k2.zaehlen, 20)])),
        ("Was passt nicht?", mix(R, seen, [(anders, 20)])),
        ("Körper erkennen", mix(R, seen, [(k2.koerper, 20)])),
        ("Körper in der Umwelt", mix(R, seen, [(k2.umwelt, 20)])),
    ]
    body = lesson(
        ["<b>Formen</b> sind flach: Kreis, Dreieck, Quadrat und Rechteck.",
         "Ein Dreieck hat 3 Ecken. Quadrat und Rechteck haben 4 Ecken. Ein Kreis hat keine Ecken.",
         "Beim Quadrat sind alle Seiten gleich lang, beim Rechteck nicht.",
         "<b>Körper</b> kann man anfassen: Würfel, Quader, Kugel, Zylinder."],
        [example("Eine Form mit 3 Ecken", ["3 Ecken, 3 Seiten"], "Dreieck"),
         example("Ein Ball", ["rund, rollt"], "Kugel")],
        [["Ein gedrehtes Quadrat ist kein Quadrat", "Gedreht bleibt es ein Quadrat"],
         ["Kugel und Kreis verwechseln", "Kreis = flach, Kugel = rund zum Anfassen"],
         ["Rechteck und Quadrat verwechseln", "Quadrat: alle Seiten gleich lang"]])
    faq = [
        {"q": "Welche Formen lernen Kinder in Klasse 1?", "a": "Kreis, Dreieck, Quadrat und Rechteck. Dazu die ersten Körper wie Würfel, Quader, Kugel und Zylinder."},
        {"q": "Was ist der Unterschied zwischen Form und Körper?", "a": "Eine Form ist flach wie ein Bild auf Papier. Einen Körper kann man in die Hand nehmen."},
        {"q": "Wie übt man Formen zu Hause?", "a": "Formen in der Wohnung suchen: Der Teller ist ein Kreis, das Fenster ein Rechteck, der Würfel beim Spiel ein Würfel."},
        {"q": "Warum Ecken zählen?", "a": "Die Anzahl der Ecken hilft, Formen sicher zu unterscheiden: 3 Ecken = Dreieck."},
    ]
    make_unit(R, "formen-und-koerper", "R",
              "Die Schülerinnen und Schüler erkennen und benennen ebene Figuren (Kreis, Dreieck, Quadrat, Rechteck) und einfache Körper, beschreiben Ecken und unterscheiden Formen nach Form und Farbe (Zusammenfassung).",
              "Formen und Körper",
              "Formen und Körper Klasse 1 – Arbeitsblätter mit Lösungen",
              "Formen und Körper",
              "Formen und Körper für Klasse 1: Kreis, Dreieck, Quadrat und Rechteck erkennen, Ecken zählen, Was passt nicht?, Würfel, Kugel und Zylinder. 100 Übungsaufgaben mit Bildern und Lösungen, kostenlos.",
              "Formen sind flach, Körper kann man anfassen.",
              "Dreieck: 3 Ecken. Quadrat und Rechteck: 4 Ecken.",
              body, faq, sets, 14, grade="klasse-1")


if __name__ == "__main__":
    main()
