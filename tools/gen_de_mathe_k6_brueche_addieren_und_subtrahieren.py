# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 6: Brüche addieren und subtrahieren（Leitidee Zahl und Operation, Sek I）
  python3 tools/gen_de_mathe_k6_brueche_addieren_und_subtrahieren.py
Gleichnamige Brüche, ungleichnamige Brüche mit Hauptnenner, Ergebnisse kürzen, gemischte Zahlen, Ergänzen zu 1, Sachaufgaben.
Fehler: Zähler plus Zähler und Nenner plus Nenner, Hauptnenner falsch, Ergebnis nicht gekürzt, beim Subtrahieren gemischter Zahlen nicht entbündelt.
"""
import random
from math import gcd
from fractions import Fraction as Fr
from de_common import lesson, example, make_unit, mix, Kids, fr, MAL, NB, table
from de_k6 import bh, mcq

R = random.Random(49604)
KIDS = Kids(R)


def lcm(a, b):
    return a * b // gcd(a, b)


def gl():
    n = R.randint(3, 15)
    a, b = R.randint(1, n - 1), R.randint(1, n - 1)
    op = R.choice(["+", "−"])
    if op == "−" and a <= b:
        a, b = b, a
    if a == b:
        return None
    v = Fr(a + b, n) if op == "+" else Fr(a - b, n)
    raw = fr(a + b if op == "+" else a - b, n)
    w = [fr(a + b, n + n) if op == "+" else None, fr(abs(a - b) if op == "+" else a + b, n), bh(v + Fr(1, n), True), raw if raw != bh(v, True) else None]
    return mcq("%s %s %s = ?" % (fr(a, n), op, fr(b, n)), bh(v, True), w,
               "Gleiche Nenner: nur die Zähler %s. <b>%s</b>%s" % ("addieren" if op == "+" else "subtrahieren", raw, (" = <b>%s</b>." % bh(v, True)) if raw != bh(v, True) else "."))


def ungl(einfach):
    while True:
        if einfach:
            n1 = R.choice([2, 3, 4, 5, 6])
            n2 = n1 * R.choice([2, 3, 4])
        else:
            n1, n2 = R.sample([2, 3, 4, 5, 6, 8, 9, 10, 12, 15], 2)
            if n1 % n2 == 0 or n2 % n1 == 0:
                continue
        a, b = R.randint(1, n1 - 1), R.randint(1, n2 - 1)
        if gcd(a, n1) == 1 and gcd(b, n2) == 1:
            break
    op = R.choice(["+", "+", "−"])
    x, y = Fr(a, n1), Fr(b, n2)
    if op == "−" and x <= y:
        a, n1, b, n2 = b, n2, a, n1
        x, y = y, x
    if x == y:
        return None
    v = x + y if op == "+" else x - y
    h = lcm(n1, n2)
    w = [fr(a + b, n1 + n2) if op == "+" else (fr(a - b, abs(n1 - n2)) if a > b and n1 != n2 else None), bh(v + Fr(1, h), True), fr(a * h // n1 + (b if op == "+" else -b), h) if a * h // n1 - b > 0 else None,
         bh(x - y if op == "+" else x + y, True)]
    A, B = a * h // n1, b * h // n2
    return mcq("%s %s %s = ?" % (fr(a, n1), op, fr(b, n2)), bh(v, True), w,
               "Hauptnenner %d: %s %s %s = %s%s." % (h, fr(A, h), op, fr(B, h), fr(A + B if op == "+" else A - B, h), (" = <b>%s</b>" % bh(v, True)) if Fr(A + B if op == "+" else A - B, h).denominator != h or v > 1 else ""))


def gemischt():
    n1, n2 = R.sample([2, 3, 4, 5, 6, 8, 10], 2)
    w1, w2 = R.randint(1, 6), R.randint(1, 5)
    a, b = R.randint(1, n1 - 1), R.randint(1, n2 - 1)
    if gcd(a, n1) > 1 or gcd(b, n2) > 1:
        return None
    x, y = w1 + Fr(a, n1), w2 + Fr(b, n2)
    op = R.choice(["+", "−"])
    if op == "−" and x <= y:
        x, y, w1, w2, a, b, n1, n2 = y, x, w2, w1, b, a, n2, n1
    v = x + y if op == "+" else x - y
    if v <= 0:
        return None
    gx, gy = "%d%s%s" % (w1, NB, fr(a, n1)), "%d%s%s" % (w2, NB, fr(b, n2))
    wrong = [bh((w1 + w2 if op == "+" else w1 - w2) + (Fr(a, n1) + Fr(b, n2) if op == "+" else abs(Fr(a, n1) - Fr(b, n2))), True),
             bh(v + 1, True), bh(v - 1, True) if v > 1 else None, bh(v + Fr(1, lcm(n1, n2)), True)]
    return mcq("%s %s %s = ?" % (gx, op, gy), bh(v, True), wrong,
               "Ganze und Brüche getrennt rechnen oder in unechte Brüche umwandeln: %s %s %s = %s = <b>%s</b>." % (bh(x), op, bh(y), bh(v), bh(v, True)))


def ergaenze():
    n1, n2 = R.sample([2, 3, 4, 5, 6, 8, 10, 12], 2)
    kind = R.choice(["eins", "luecke"])
    if kind == "eins":
        z = R.randint(1, n1 - 1)
        if gcd(z, n1) > 1:
            return None
        return mcq("Was fehlt bis zum Ganzen? %s + ☐ = 1" % fr(z, n1), bh(Fr(n1 - z, n1)), [fr(1, n1) if n1 - z != 1 else fr(2, n1), fr(z, n1), fr(n1, z) if z > 1 else fr(n1 - z, n1 + 1)],
                   "1 = %s. %s − %s = <b>%s</b>." % (fr(n1, n1), fr(n1, n1), fr(z, n1), bh(Fr(n1 - z, n1))))
    a, b = R.randint(1, n1 - 1), R.randint(1, n2 - 1)
    x, y = Fr(a, n1), Fr(b, n2)
    if gcd(a, n1) > 1 or gcd(b, n2) > 1 or x >= y:
        return None
    d = y - x
    return mcq("Ergänze: %s + ☐ = %s" % (fr(a, n1), fr(b, n2)), bh(d), [fr(b - a, abs(n2 - n1)) if b > a and n1 != n2 else None, bh(x + y, True), bh(d + Fr(1, lcm(n1, n2))), fr(b - a, n2) if b > a and Fr(b - a, n2) != d else None],
               "Rechne %s − %s = <b>%s</b>." % (fr(b, n2), fr(a, n1), bh(d)))


def sache():
    p, er = KIDS.next()
    kind = R.choice(["pizza", "weg", "saft", "zeit", "rest", "kuchen"])
    n1, n2 = R.sample([2, 3, 4, 5, 6, 8], 2)
    a, b = R.randint(1, n1 - 1), R.randint(1, n2 - 1)
    if gcd(a, n1) > 1 or gcd(b, n2) > 1:
        return None
    x, y = Fr(a, n1), Fr(b, n2)
    h = lcm(n1, n2)
    if kind == "pizza":
        if x + y > 1:
            return None
        v = 1 - x - y
        if v == 0:
            return None
        return mcq("%s isst %s einer Pizza, ein Freund isst %s. Welcher Teil der Pizza bleibt übrig?" % (p, fr(a, n1), fr(b, n2)), bh(v), [bh(x + y), fr(n1 + n2 - a - b, n1 + n2) if n1 + n2 - a - b > 0 else None, bh(v + Fr(1, h)), bh(1 - x)],
                   "Gegessen: %s + %s = %s. Übrig: 1 − %s = <b>%s</b>." % (fr(a, n1), fr(b, n2), bh(x + y), bh(x + y), bh(v)))
    if kind == "weg":
        return mcq("%s läuft %s km, dann noch %s km. Wie weit läuft %s insgesamt?" % (p, fr(a, n1), fr(b, n2), er), bh(x + y, True) + " km", [fr(a + b, n1 + n2) + " km", bh(x + y + Fr(1, h), True) + " km", bh(abs(x - y), True) + " km" if x != y else None],
                   "Hauptnenner %d: %s + %s = <b>%s km</b>." % (h, fr(a * h // n1, h), fr(b * h // n2, h), bh(x + y, True)))
    if kind == "saft":
        if x <= y:
            return None
        return mcq("In einer Flasche sind %s Liter Saft. %s trinkt %s Liter. Wie viel ist noch in der Flasche?" % (fr(a, n1), p, fr(b, n2)), bh(x - y) + " l", [bh(x + y, True) + " l", fr(a - b, abs(n1 - n2)) + " l" if a > b and n1 != n2 else None, bh(x - y + Fr(1, h)) + " l"],
                   "%s − %s = %s − %s = <b>%s l</b>." % (fr(a, n1), fr(b, n2), fr(a * h // n1, h), fr(b * h // n2, h), bh(x - y)))
    if kind == "zeit":
        n1, n2 = R.sample([2, 3, 4, 6, 12], 2)
        a, b = 1, 1
        x, y = Fr(1, n1), Fr(1, n2)
        return mcq("%s übt %s Stunde Klavier und %s Stunde Flöte. Wie viele Minuten sind das zusammen?" % (p, fr(1, n1), fr(1, n2)), "%d min" % (60 // n1 + 60 // n2),
                   ["%d min" % x for x in (60 // (n1 + n2) if 60 % (n1 + n2) == 0 else 60 // n1, abs(60 // n1 - 60 // n2), 60 // n1 + 60 // n2 + 10)], "%s h = %d min, %s h = %d min. <b>%d min</b>." % (fr(1, n1), 60 // n1, fr(1, n2), 60 // n2, 60 // n1 + 60 // n2))
    if kind == "rest":
        if x + y >= 1:
            return None
        v = 1 - x - y
        return mcq("%s gibt %s des Taschengeldes für Bücher und %s für Süßigkeiten aus. Welcher Anteil bleibt übrig?" % (p, fr(a, n1), fr(b, n2)), bh(v), [bh(x + y), bh(v + Fr(1, h)), bh(1 - y)],
                   "Ausgegeben: %s. Übrig: 1 − %s = <b>%s</b>." % (bh(x + y), bh(x + y), bh(v)))
    w1, w2 = R.randint(2, 9), R.randint(2, 9)
    X, Y = w1 + x, w2 + y
    return mcq("Ein Obststand verkauft am Vormittag %s kg Äpfel und am Nachmittag %s kg Äpfel. Wie viele Kilogramm sind das zusammen?" % (bh(X, True), bh(Y, True)), bh(X + Y, True) + " kg", [bh((w1 + w2) + Fr(a + b, n1 + n2), True) + " kg", bh(X + Y + 1, True) + " kg", bh(X + Y - Fr(1, h), True) + " kg"],
                   "%s + %s = <b>%s kg</b>." % (bh(X, True), bh(Y, True), bh(X + Y, True)))


def main():
    seen = set()
    sets = [
        ("Gleichnamige Brüche", mix(R, seen, [(gl, 20)])),
        ("Ein Nenner ist ein Vielfaches", mix(R, seen, [(lambda: ungl(True), 20)])),
        ("Hauptnenner finden", mix(R, seen, [(lambda: ungl(False), 14), (ergaenze, 6)])),
        ("Gemischte Zahlen", mix(R, seen, [(gemischt, 14), (ergaenze, 6)])),
        ("Sachaufgaben", mix(R, seen, [(sache, 20)])),
    ]
    body = lesson(
        ["<b>Gleichnamige Brüche</b> (gleicher Nenner): Zähler addieren oder subtrahieren, der Nenner bleibt.",
         "<b>Ungleichnamige Brüche</b>: Zuerst auf den Hauptnenner erweitern, dann rechnen.",
         "Das Ergebnis immer vollständig kürzen. Unechte Brüche kann man als gemischte Zahl schreiben.",
         "Bei <b>gemischten Zahlen</b> rechnet man Ganze und Brüche getrennt oder wandelt in unechte Brüche um."],
        [example("%s + %s" % (fr(2, 3), fr(1, 4)), ["Hauptnenner 12", "%s + %s = %s" % (fr(8, 12), fr(3, 12), fr(11, 12))], fr(11, 12)),
         example("%s − %s" % (fr(5, 6), fr(1, 2)), ["%s − %s = %s" % (fr(5, 6), fr(3, 6), fr(2, 6))], fr(1, 3))],
        [["%s + %s = %s" % (fr(1, 2), fr(1, 3), fr(2, 5)), "Nenner nicht addieren: %s + %s = %s" % (fr(3, 6), fr(2, 6), fr(5, 6))],
         ["%s + %s = %s (nicht gekürzt)" % (fr(1, 6), fr(1, 6), fr(2, 6)), "Kürzen: %s" % fr(1, 3)],
         ["3%s%s − 1%s%s = 2%s%s" % (NB, fr(1, 4), NB, fr(3, 4), NB, fr(2, 4)), "Ein Ganzes entbündeln: 2%s%s − 1%s%s = 1%s%s" % (NB, fr(5, 4), NB, fr(3, 4), NB, fr(1, 2))]])
    faq = [
        {"q": "Wie addiert man Brüche mit verschiedenen Nennern?", "a": "Man bringt beide Brüche auf den Hauptnenner. Dann addiert man die Zähler, der Nenner bleibt gleich."},
        {"q": "Darf man die Nenner addieren?", "a": "Nein. 1/2 + 1/3 ist nicht 2/5, sondern 3/6 + 2/6 = 5/6."},
        {"q": "Wie subtrahiere ich gemischte Zahlen?", "a": "Ganze und Brüche getrennt. Ist der Bruch zu klein, nimmt man ein Ganzes dazu (entbündeln) oder rechnet mit unechten Brüchen."},
        {"q": "Muss ich das Ergebnis kürzen?", "a": "Ja, das Ergebnis sollte immer vollständig gekürzt sein."},
    ]
    make_unit(R, "brueche-addieren-und-subtrahieren", "Z",
              "Die Schülerinnen und Schüler addieren und subtrahieren gleichnamige und ungleichnamige Brüche und gemischte Zahlen und lösen Sachaufgaben mit Bruchzahlen (Zusammenfassung).",
              "Brüche addieren und subtrahieren",
              "Brüche addieren und subtrahieren Klasse 6 – Arbeitsblätter mit Lösungen",
              "Brüche addieren",
              "Brüche addieren und subtrahieren für Klasse 6: gleichnamig, Hauptnenner, gemischte Zahlen und Sachaufgaben. 100 Aufgaben mit Lösungen, kostenlos.",
              "Erst gleichnamig machen, dann die Zähler rechnen.",
              "Der Nenner wird nie addiert.",
              body, faq, sets, 4, grade="klasse-6")


if __name__ == "__main__":
    main()
