# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 2: Strichlisten und Diagramme（Leitidee Daten und Zufall）
  python3 tools/gen_de_mathe_k2_strichlisten_und_diagramme.py
Strichlisten lesen, Säulendiagramme ablesen, Tabellen und Umfragen auswerten, einfache Kombinationen zählen.
Die Daten-Aufgaben kommen aus Klasse 3 (gen_de_mathe_k3_diagramme_und_tabellen) mit eigenem Zufall und Themen der Klasse 2.
Fehler: Fünferbündel als 4 gezählt, Skala nicht beachtet, beim Kombinieren Möglichkeiten vergessen oder doppelt gezählt.
"""
import random
from de_common import mcq, lesson, example, make_unit, mix, MAL, table
import gen_de_mathe_k3_diagramme_und_tabellen as k3

R = random.Random(49218)
k3.R = random.Random(49318)
k3.TOPICS = [(t.replace("3a", "2a"), c, u) for t, c, u in k3.TOPICS]


def le100(it):
    import re
    if it is None:
        return None
    nums = [int(x) for x in re.findall(r"\d+", re.sub(r"<[^>]+>", " ", it["q"] + " " + " ".join(it["c"])))]
    return it if all(n <= 100 for n in nums) else None


def strich():
    return k3.strich() if R.random() < 0.5 else k3.strich_tab()


def ablesen():
    return le100(k3.ablesen())


def tabelle():
    return le100(k3.tabelle() if R.random() < 0.5 else k3.vergleichen())


def umfrage():
    return le100(k3.umfrage())


KOMBI = [
    ("%s hat %d T-Shirts und %d Hosen. Wie viele verschiedene Kombinationen kann %s anziehen?", "kleid"),
    ("In der Eisdiele gibt es %d Sorten und %d Arten von Waffeln. Wie viele verschiedene Eis mit einer Kugel gibt es?", "eis"),
    ("Zum Frühstück gibt es %d Sorten Brot und %d Sorten Aufstrich. Wie viele verschiedene Brote kann man machen?", "brot"),
]


def kombi():
    kind = R.choice(["mal", "mal", "reihe", "zahlen"])
    if kind == "mal":
        t, k = R.choice(KOMBI)
        a, b = R.randint(2, 4), R.randint(2, 4)
        if k == "kleid":
            names = R.choice([("Mia", "sie"), ("Ben", "er"), ("Lena", "sie"), ("Paul", "er"), ("Ida", "sie"), ("Emil", "er")])
            q = t % (names[0], a, b, names[1])
        else:
            q = t % (a, b)
        return mcq(q, str(a * b), [str(a + b), str(a * b + 1), str(a * b - 1)],
                   "Zu jeder der %d Möglichkeiten passen %d andere: %d %s %d = <b>%d</b>." % (a, b, a, MAL, b, a * b))
    if kind == "reihe":
        names = R.sample(["Mia", "Ben", "Lena", "Paul", "Ida", "Emil", "Anna", "Theo"], 3)
        return mcq("%s, %s und %s stellen sich in eine Reihe. Wie viele verschiedene Reihenfolgen gibt es?" % tuple(names), "6", ["3", "9", "4"],
                   "Schreibe alle auf: Für den ersten Platz gibt es 3 Kinder, dann 2, dann 1. Es sind <b>6</b> Reihenfolgen.")
    ds = R.sample(range(1, 10), 2)
    return mcq("Bilde zweistellige Zahlen mit den Ziffernkarten %d und %d. Jede Karte wird genau einmal benutzt. Welche Zahlen kannst du legen?" % tuple(ds),
               "%d%d und %d%d" % (ds[0], ds[1], ds[1], ds[0]), ["nur %d%d" % (ds[0], ds[1]), "%d%d, %d%d und %d%d" % (ds[0], ds[0], ds[0], ds[1], ds[1], ds[0]), "%d und %d" % (ds[0] + ds[1], abs(ds[0] - ds[1]) or 10)],
               "Mit zwei Karten gibt es zwei Zahlen: <b>%d%d und %d%d</b>." % (ds[0], ds[1], ds[1], ds[0]))


def main():
    seen = set()
    sets = [
        ("Strichlisten", mix(R, seen, [(strich, 20)])),
        ("Säulendiagramme ablesen", mix(R, seen, [(ablesen, 20)])),
        ("Tabellen und Diagramme vergleichen", mix(R, seen, [(tabelle, 20)])),
        ("Umfragen auswerten", mix(R, seen, [(umfrage, 20)])),
        ("Kombinieren", mix(R, seen, [(kombi, 20)])),
    ]
    body = lesson(
        ["In einer <b>Strichliste</b> machst du für jedes Ding einen Strich. Den fünften Strich ziehst du quer: Das ist ein Fünferbündel.",
         "In einem <b>Säulendiagramm</b> zeigt die Höhe jeder Säule eine Anzahl. Schau zuerst, wie viel ein Kästchen bedeutet.",
         "In einer <b>Tabelle</b> stehen die Daten geordnet in Zeilen und Spalten.",
         "Beim <b>Kombinieren</b> schreibst du alle Möglichkeiten geordnet auf, damit du keine vergisst."],
        [example("Strichliste mit 3 Fünferbündeln und 2 Strichen", ["3 %s 5 = 15" % MAL, "15 + 2"], "17"),
         example("3 T-Shirts und 2 Hosen", ["zu jedem T-Shirt 2 Hosen", "3 %s 2" % MAL], "6 Kombinationen")],
        [["Ein Fünferbündel als 4 zählen", "Der Querstrich zählt mit: 5"],
         ["Jedes Kästchen im Diagramm als 1 zählen", "Erst die Skala lesen"],
         ["Beim Kombinieren durcheinander aufschreiben", "Geordnet aufschreiben, zum Beispiel mit einer Tabelle"]])
    faq = [
        {"q": "Warum macht man Fünferbündel?", "a": "So kann man schneller zählen: in Fünferschritten statt jeden Strich einzeln."},
        {"q": "Welche Diagramme lernen Kinder in Klasse 2?", "a": "Strichlisten, einfache Tabellen, Bild- und Säulendiagramme."},
        {"q": "Wie macht man eine Umfrage in der Klasse?", "a": "Man stellt eine Frage, macht für jede Antwort einen Strich in der Strichliste und zeichnet danach ein Säulendiagramm."},
        {"q": "Was ist Kombinieren?", "a": "Man sucht alle Möglichkeiten, Dinge zusammenzustellen, zum Beispiel T-Shirts und Hosen. Geordnetes Aufschreiben hilft, keine zu vergessen."},
    ]
    make_unit(R, "strichlisten-und-diagramme", "D",
              "Die Schülerinnen und Schüler erfassen Daten in Strichlisten und Tabellen, lesen Säulendiagramme ab, werten Umfragen aus und bestimmen bei einfachen kombinatorischen Aufgaben die Anzahl der Möglichkeiten (Zusammenfassung).",
              "Strichlisten, Tabellen und Diagramme",
              "Strichlisten und Diagramme Klasse 2 – Arbeitsblätter mit Lösungen",
              "Strichlisten und Diagramme",
              "Strichlisten und Diagramme für Klasse 2: Strichlisten zählen, Säulendiagramme ablesen, Tabellen, Umfragen und Kombinieren. 100 Übungsaufgaben mit Lösungen, kostenlos.",
              "Ein Fünferbündel sind 5 Striche.",
              "Im Diagramm erst die Skala lesen.",
              body, faq, sets, 18, grade="klasse-2")


if __name__ == "__main__":
    main()
