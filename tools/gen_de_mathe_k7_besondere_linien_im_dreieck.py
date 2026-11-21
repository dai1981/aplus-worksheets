# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 7: Besondere Linien im Dreieck（Leitidee Raum und Form, Sek I）
  python3 tools/gen_de_mathe_k7_besondere_linien_im_dreieck.py
Mittelsenkrechte und Umkreis, Winkelhalbierende und Inkreis, Höhen, Seitenhalbierende und Schwerpunkt, Lage der Punkte bei spitz-, recht- und stumpfwinkligen Dreiecken, Satz des Thales, Anwendungen.
Fehler: Mittelsenkrechte und Winkelhalbierende verwechselt, Umkreismittelpunkt immer innen vermutet, Schwerpunkt teilt die Seitenhalbierende im Verhältnis 1 : 1.
"""
import random
from fractions import Fraction as Fr
from de_common import lesson, example, make_unit, mix, Kids, MAL, table
from de_k6 import dz
from de_k7 import mcq

R = random.Random(49713)
KIDS = Kids(R)
LINIEN = ["Mittelsenkrechten", "Winkelhalbierenden", "Höhen", "Seitenhalbierenden"]
PUNKT = {"Mittelsenkrechten": "Umkreismittelpunkt", "Winkelhalbierenden": "Inkreismittelpunkt", "Höhen": "Höhenschnittpunkt", "Seitenhalbierenden": "Schwerpunkt"}


def begriffe():
    k = R.randrange(14)
    D = [("Welche Linie steht senkrecht auf einer Seite und geht durch deren Mittelpunkt?", "Mittelsenkrechte", ["Winkelhalbierende", "Höhe", "Seitenhalbierende"]),
         ("Welche Linie teilt einen Winkel in zwei gleich große Winkel?", "Winkelhalbierende", ["Mittelsenkrechte", "Höhe", "Seitenhalbierende"]),
         ("Welche Linie geht durch eine Ecke und steht senkrecht auf der gegenüberliegenden Seite?", "Höhe", ["Seitenhalbierende", "Mittelsenkrechte", "Winkelhalbierende"]),
         ("Welche Linie verbindet eine Ecke mit dem Mittelpunkt der gegenüberliegenden Seite?", "Seitenhalbierende", ["Höhe", "Mittelsenkrechte", "Winkelhalbierende"]),
         ("Der Schnittpunkt der Mittelsenkrechten ist der Mittelpunkt des …", "Umkreises", ["Inkreises", "Schwerpunkts", "Thaleskreises über jeder Seite"]),
         ("Der Schnittpunkt der Winkelhalbierenden ist der Mittelpunkt des …", "Inkreises", ["Umkreises", "Höhenschnittpunkts", "Schwerpunkts"]),
         ("Der Schnittpunkt der Seitenhalbierenden heißt …", "Schwerpunkt", ["Umkreismittelpunkt", "Inkreismittelpunkt", "Höhenschnittpunkt"]),
         ("Welcher Punkt ist von allen drei Ecken gleich weit entfernt?", "der Umkreismittelpunkt", ["der Inkreismittelpunkt", "der Schwerpunkt", "der Höhenschnittpunkt"]),
         ("Welcher Punkt ist von allen drei Seiten gleich weit entfernt?", "der Inkreismittelpunkt", ["der Umkreismittelpunkt", "der Schwerpunkt", "der Höhenschnittpunkt"]),
         ("Auf welcher Linie liegen alle Punkte, die von A und B gleich weit entfernt sind?", "auf der Mittelsenkrechten von AB", ["auf der Winkelhalbierenden", "auf der Seitenhalbierenden", "auf der Höhe"]),
         ("Auf welcher Linie liegen alle Punkte, die von zwei sich schneidenden Geraden gleich weit entfernt sind?", "auf einer Winkelhalbierenden", ["auf einer Mittelsenkrechten", "auf einer Höhe", "auf einer Seitenhalbierenden"]),
         ("An welchem Punkt kann man ein Pappdreieck auf einer Bleistiftspitze balancieren?", "am Schwerpunkt", ["am Umkreismittelpunkt", "am Höhenschnittpunkt", "an einer Ecke"]),
         ("Wie viele Höhen hat ein Dreieck?", "3", ["1", "2", "6"]),
         ("Der Inkreis berührt …", "alle drei Seiten", ["alle drei Ecken", "nur die längste Seite", "die Mittelpunkte der Seiten"])]
    q, a, w = D[k]
    return mcq(q, a, w, "<b>%s</b>." % a)


def lage():
    art = R.choice(["spitzwinklig", "rechtwinklig", "stumpfwinklig"])
    p = R.choice(["Umkreismittelpunkt", "Höhenschnittpunkt", "Inkreismittelpunkt", "Schwerpunkt"])
    if p in ("Inkreismittelpunkt", "Schwerpunkt"):
        ans = "innerhalb des Dreiecks"
    elif art == "spitzwinklig":
        ans = "innerhalb des Dreiecks"
    elif art == "rechtwinklig":
        ans = "auf der längsten Seite (Hypotenuse)" if p == "Umkreismittelpunkt" else "in der Ecke mit dem rechten Winkel"
    else:
        ans = "außerhalb des Dreiecks"
    opts = ["innerhalb des Dreiecks", "außerhalb des Dreiecks", "auf der längsten Seite (Hypotenuse)", "in der Ecke mit dem rechten Winkel"]
    w = [o for o in opts if o != ans]
    R.shuffle(w)
    return mcq("Wo liegt der %s eines %sen Dreiecks?" % (p, art), ans, w,
               "Inkreismittelpunkt und Schwerpunkt liegen immer innen. Umkreismittelpunkt und Höhenschnittpunkt liegen beim spitzwinkligen Dreieck innen, beim stumpfwinkligen außen; beim rechtwinkligen liegt der Umkreismittelpunkt auf der Hypotenuse, der Höhenschnittpunkt in der rechtwinkligen Ecke. <b>%s</b>." % ans)


def thales():
    kind = R.choice(["winkel", "radius", "dritter", "art"])
    if kind == "winkel":
        a = R.randint(20, 70)
        return mcq("Die Ecke C liegt auf dem Halbkreis über der Strecke AB (Thaleskreis). Der Winkel bei A ist %d°. Wie groß ist der Winkel bei B?" % a, "%d°" % (90 - a), ["%d°" % x for x in (180 - a, a, 180 - 2 * a)],
                   "Nach dem Satz des Thales ist der Winkel bei C ein rechter Winkel. 180° − 90° − %d° = <b>%d°</b>." % (a, 90 - a))
    if kind == "radius":
        c = R.randint(4, 16)
        return mcq("Ein rechtwinkliges Dreieck hat die Hypotenuse %d cm. Wie groß ist der Radius seines Umkreises?" % c, "%s cm" % dz(Fr(c, 2)), ["%d cm" % c, "%s cm" % dz(Fr(c, 3)) if c % 3 == 0 else "%d cm" % (2 * c), "%s cm" % dz(Fr(c, 4))],
                   "Der Umkreismittelpunkt ist der Mittelpunkt der Hypotenuse (Thales): r = %d cm : 2 = <b>%s cm</b>." % (c, dz(Fr(c, 2))))
    if kind == "dritter":
        return mcq("Ein Punkt C liegt auf dem Kreis mit dem Durchmesser AB (nicht auf A oder B). Wie groß ist der Winkel ACB?", "90°", ["45°", "180°", "60°"], "Satz des Thales: Der Winkel ist immer <b>90°</b>.") if R.random() < 0.3 else None
    return mcq("Ein Punkt C liegt innerhalb des Kreises mit dem Durchmesser AB. Wie ist der Winkel ACB?", "größer als 90° (stumpf)", ["genau 90°", "kleiner als 90° (spitz)", "immer 180°"],
               "Auf dem Thaleskreis wäre er 90°, innerhalb ist er größer: <b>stumpf</b>.") if R.random() < 0.3 else mcq("Ein Punkt C liegt außerhalb des Kreises mit dem Durchmesser AB. Wie ist der Winkel ACB?", "kleiner als 90° (spitz)", ["genau 90°", "größer als 90° (stumpf)", "immer 0°"],
               "Auf dem Thaleskreis wäre er 90°, außerhalb ist er kleiner: <b>spitz</b>.")


def schwerpunkt():
    kind = R.choice(["teil", "ganz", "halb"])
    s = R.choice([6, 9, 12, 15, 18, 21, 24, 27, 30])
    if kind == "teil":
        return mcq("Eine Seitenhalbierende ist %d cm lang. Wie weit ist der Schwerpunkt von der Ecke entfernt?" % s, "%d cm" % (2 * s // 3), ["%s cm" % dz(Fr(s, 2)), "%d cm" % (s // 3), "%d cm" % s],
                   "Der Schwerpunkt teilt jede Seitenhalbierende im Verhältnis 2 : 1 (von der Ecke aus): 2/3 von %d cm = <b>%d cm</b>." % (s, 2 * s // 3))
    if kind == "ganz":
        t = R.choice([2, 3, 4, 5, 6, 7, 8])
        return mcq("Der Schwerpunkt ist %d cm von der Seitenmitte entfernt. Wie lang ist die ganze Seitenhalbierende?" % t, "%d cm" % (3 * t), ["%d cm" % (2 * t), "%d cm" % (4 * t), "%d cm" % (t + 2)],
                   "Das kurze Stück ist 1/3: 3 %s %d cm = <b>%d cm</b>." % (MAL, t, 3 * t))
    a = R.randint(4, 20)
    return mcq("Eine Seite ist %d cm lang. Die Seitenhalbierende teilt sie in zwei Stücke. Wie lang ist jedes Stück?" % a, "%s cm" % dz(Fr(a, 2)), ["%s cm" % dz(Fr(a, 3)) if a % 3 == 0 else "%d cm" % a, "%s cm" % dz(Fr(2 * a, 3)) if a % 3 == 0 else "%s cm" % dz(Fr(a, 4)), "%d cm" % (a + 1)],
               "Die Seitenhalbierende trifft die Seite in der Mitte: <b>%s cm</b>." % dz(Fr(a, 2)))


def anwendung():
    k = R.randrange(8)
    D = [("Drei Dörfer wollen einen gemeinsamen Funkmast, der von allen drei Dörfern gleich weit entfernt ist. Wie findet man den Ort?", "Schnittpunkt der Mittelsenkrechten", ["Schnittpunkt der Winkelhalbierenden", "Schnittpunkt der Seitenhalbierenden", "Mitte der längsten Seite"]),
         ("In einem dreieckigen Park soll ein möglichst großer runder Brunnen gebaut werden. Wo liegt sein Mittelpunkt?", "Schnittpunkt der Winkelhalbierenden", ["Schnittpunkt der Mittelsenkrechten", "Schnittpunkt der Höhen", "an einer Ecke"]),
         ("Ein dreieckiges Schild soll an einem Punkt aufgehängt werden, damit es waagerecht hängt. Wo?", "im Schwerpunkt", ["im Umkreismittelpunkt", "an der längsten Seite", "im Höhenschnittpunkt"]),
         ("Zwei Spielplätze A und B. Alle Orte, die zu beiden gleich weit sind, liegen …", "auf der Mittelsenkrechten von AB", ["auf der Strecke AB", "auf einem Kreis um A", "auf der Winkelhalbierenden"]),
         ("Eine Bank soll von zwei geraden Wegen, die sich kreuzen, gleich weit entfernt sein. Wo kann sie stehen?", "auf einer Winkelhalbierenden der beiden Wege", ["auf der Mittelsenkrechten", "im Kreuzungspunkt", "auf einem Kreis"]),
         ("Ein Kreis soll durch alle drei Ecken eines Dreiecks gehen. Wie heißt er?", "Umkreis", ["Inkreis", "Thaleskreis", "Schwerkreis"]),
         ("Mit welchem Werkzeug konstruiert man eine Mittelsenkrechte am einfachsten?", "mit dem Zirkel (zwei Kreisbögen) und dem Lineal", ["nur mit dem Winkelmesser", "mit einem Taschenrechner", "nur mit einem Lineal ohne Skala"]),
         ("Wie konstruiert man den Inkreis?", "Winkelhalbierende schneiden, dann Lot auf eine Seite fällen für den Radius", ["Mittelsenkrechten schneiden, Radius bis zur Ecke", "Seitenhalbierende schneiden", "Höhen schneiden"])]
    q, a, w = D[k]
    return mcq(q, a, w, "<b>%s</b>." % a)


def main():
    seen = set()
    sets = [
        ("Linien im Dreieck", mix(R, seen, [(begriffe, 12), (schwerpunkt, 8)])),
        ("Lage der besonderen Punkte", mix(R, seen, [(lage, 12), (thales, 8)])),
        ("Satz des Thales", mix(R, seen, [(thales, 20)])),
        ("Schwerpunkt und Seitenhalbierende", mix(R, seen, [(schwerpunkt, 18), (begriffe, 2)])),
        ("Anwendungen", mix(R, seen, [(anwendung, 8), (thales, 12)])),
    ]
    body = lesson(
        ["<b>Mittelsenkrechten</b> schneiden sich im Umkreismittelpunkt. Er ist von allen drei Ecken gleich weit entfernt.",
         "<b>Winkelhalbierende</b> schneiden sich im Inkreismittelpunkt. Er ist von allen drei Seiten gleich weit entfernt.",
         "<b>Seitenhalbierende</b> schneiden sich im Schwerpunkt. Er teilt jede Seitenhalbierende im Verhältnis 2 : 1. Die <b>Höhen</b> schneiden sich im Höhenschnittpunkt.",
         "<b>Satz des Thales</b>: Liegt C auf dem Halbkreis über AB, ist der Winkel bei C ein rechter Winkel."],
        [example("Thales: Winkel bei A = 35°", ["Winkel bei C = 90°", "180° − 90° − 35°"], "55°"),
         example("Seitenhalbierende 12 cm", ["2 : 1", "Ecke bis Schwerpunkt: 8 cm"], "8 cm")],
        [["Umkreismittelpunkt liegt immer im Dreieck", "Beim stumpfwinkligen Dreieck liegt er außerhalb"],
         ["Der Schwerpunkt halbiert die Seitenhalbierende", "Er teilt sie im Verhältnis 2 : 1"],
         ["Inkreis geht durch die Ecken", "Der Inkreis berührt die Seiten, der Umkreis geht durch die Ecken"]])
    faq = [
        {"q": "Welcher Punkt ist der Mittelpunkt des Umkreises?", "a": "Der Schnittpunkt der drei Mittelsenkrechten. Er hat zu allen Ecken den gleichen Abstand."},
        {"q": "Welcher Punkt ist der Mittelpunkt des Inkreises?", "a": "Der Schnittpunkt der drei Winkelhalbierenden. Er hat zu allen Seiten den gleichen Abstand."},
        {"q": "Was sagt der Satz des Thales?", "a": "Liegt ein Punkt C auf dem Kreis mit dem Durchmesser AB, dann ist der Winkel ACB ein rechter Winkel."},
        {"q": "Was ist der Schwerpunkt eines Dreiecks?", "a": "Der Schnittpunkt der Seitenhalbierenden. An ihm kann man ein Dreieck aus Pappe balancieren."},
    ]
    make_unit(R, "besondere-linien-im-dreieck", "R",
              "Die Schülerinnen und Schüler kennen Mittelsenkrechte, Winkelhalbierende, Höhen und Seitenhalbierende, nutzen Umkreis, Inkreis und Schwerpunkt, begründen mit dem Satz des Thales und wenden die Eigenschaften an (Zusammenfassung).",
              "Besondere Linien im Dreieck",
              "Mittelsenkrechte, Winkelhalbierende, Thales Klasse 7 – Arbeitsblätter",
              "Linien im Dreieck",
              "Besondere Linien im Dreieck für Klasse 7: Mittelsenkrechte, Winkelhalbierende, Höhen, Seitenhalbierende, Umkreis, Inkreis und Satz des Thales. 100 Aufgaben mit Lösungen, kostenlos.",
              "Mittelsenkrechten → Umkreis. Winkelhalbierende → Inkreis.",
              "Thales: Winkel im Halbkreis = 90°.",
              body, faq, sets, 13, grade="klasse-7")


if __name__ == "__main__":
    main()
