# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 6: Brüche dividieren（Leitidee Zahl und Operation, Sek I）
  python3 tools/gen_de_mathe_k6_brueche_dividieren.py
Kehrwert, Bruch durch natürliche Zahl, natürliche Zahl durch Bruch, Bruch durch Bruch, gemischte Zahlen, Sachaufgaben (Wie oft passt …?).
Fehler: den ersten Bruch statt des zweiten umgedreht, Zähler durch Zähler und Nenner durch Nenner ohne Ganzzahligkeit, durch eine Zahl geteilt und den Zähler geteilt statt den Nenner multipliziert.
"""
import random
from math import gcd
from fractions import Fraction as Fr
from de_common import lesson, example, make_unit, mix, Kids, fr, MAL, NB, table
from de_k6 import bh, mcq

R = random.Random(49606)
KIDS = Kids(R)
G = ":"


def gk(lo=2, hi=12):
    while True:
        n = R.randint(lo, hi)
        z = R.randint(1, n - 1)
        if gcd(z, n) == 1:
            return z, n


def kehrwert():
    kind = R.choice(["bruch", "bruch", "zahl", "gemischt"])
    if kind == "bruch":
        z, n = gk(2, 15)
        if z == 1:
            return mcq("Was ist der Kehrwert von %s?" % fr(1, n), str(n), [fr(n - 1, n) if n > 2 else fr(1, 3), fr(1, n), "−" + fr(1, n)], "Zähler und Nenner tauschen: %s = <b>%d</b>." % (fr(n, 1), n))
        return mcq("Was ist der Kehrwert von %s?" % fr(z, n), fr(n, z), [fr(n - z, n), fr(z, n), fr(z, n * 2), fr(1, z * n)], "Zähler und Nenner tauschen: <b>%s</b>." % fr(n, z))
    if kind == "zahl":
        k = R.randint(2, 20)
        return mcq("Was ist der Kehrwert von %d?" % k, fr(1, k), [str(k), fr(k, 10) if k < 10 else fr(10, k), fr(1, k + 1)], "%d = %s. Umgedreht: <b>%s</b>." % (k, fr(k, 1), fr(1, k)))
    w = R.randint(1, 4)
    z, n = gk(2, 6)
    v = w + Fr(z, n)
    return mcq("Was ist der Kehrwert von %d%s%s?" % (w, NB, fr(z, n)), bh(1 / v), ["%d%s%s" % (w, NB, fr(n, z)) if z > 1 else "%d%s%s" % (w, NB, fr(1, n + 1)), fr(n, z) if z > 1 else str(n), fr(1, w) if w > 1 else fr(n, w * n + z + 1)],
               "Erst als unechten Bruch schreiben: %s. Dann umdrehen: <b>%s</b>." % (bh(v), bh(1 / v)))


def durch_zahl():
    z, n = gk(2, 12)
    k = R.randint(2, 9)
    v = Fr(z, n) / k
    teil = z % k == 0
    return mcq("%s %s %d = ?" % (fr(z, n), G, k), bh(v), [fr(z * k, n) if not teil else bh(Fr(z * k, n), True), bh(Fr(z, n) * k, True), fr(z, n + k), fr(n, z * k) if z * k != n else None],
               ("Den Zähler durch %d teilen: <b>%s</b>." % (k, bh(v))) if teil else "Mit dem Kehrwert %s multiplizieren: %s %s %s = <b>%s</b>." % (fr(1, k), fr(z, n), MAL, fr(1, k), bh(v)))


def zahl_durch():
    z, n = gk(2, 10)
    k = R.randint(1, 12)
    v = Fr(k) / Fr(z, n)
    return mcq("%d %s %s = ?" % (k, G, fr(z, n)), bh(v, True), [bh(Fr(k * z, n), True), bh(Fr(k, n), True) if Fr(k, n) != v else None, bh(v + 1, True), fr(k * n, z * n) if z > 1 else bh(Fr(k, z * n))],
               "Mit dem Kehrwert multiplizieren: %d %s %s = %s%s." % (k, MAL, fr(n, z), bh(Fr(k * n, z)), (" = <b>%s</b>" % bh(v, True)) if v.denominator > 1 and v > 1 else ""))


def bruch_durch():
    a, b = gk(2, 10)
    c, d = gk(2, 10)
    if Fr(a, b) == Fr(c, d):
        return None
    v = Fr(a, b) / Fr(c, d)
    return mcq("%s %s %s = ?" % (fr(a, b), G, fr(c, d)), bh(v, True), [bh(Fr(a * c, b * d), True), bh(Fr(b * c, a * d), True), bh(v + Fr(1, v.denominator), True) if v.denominator > 1 else bh(v + 1, True), fr(a * c, b + d)],
                   "Mit dem Kehrwert des zweiten Bruchs multiplizieren: %s %s %s = %s%s." % (fr(a, b), MAL, fr(d, c), fr(a * d, b * c), (" = <b>%s</b>" % bh(v, True)) if Fr(a * d, b * c) != v or v > 1 or v.denominator != b * c else ""))


def gemischt():
    w = R.randint(1, 5)
    z, n = gk(2, 6)
    x = w + Fr(z, n)
    kind = R.choice(["zahl", "bruch"])
    if kind == "zahl":
        k = R.randint(2, 6)
        v = x / k
        return mcq("%d%s%s %s %d = ?" % (w, NB, fr(z, n), G, k), bh(v, True), [bh(Fr(w, k) + Fr(z, n), True) if Fr(w, k) + Fr(z, n) != v else None, bh(x * k, True), bh(v + Fr(1, v.denominator), True), bh(Fr(w, k) + Fr(z, n * k) + 1, True)],
                   "%s %s %d = %s %s %s = <b>%s</b>." % (bh(x), G, k, bh(x), MAL, fr(1, k), bh(v, True)))
    c, d = gk(2, 6)
    y = Fr(c, d)
    v = x / y
    return mcq("%d%s%s %s %s = ?" % (w, NB, fr(z, n), G, fr(c, d)), bh(v, True), [bh(x * y, True), bh(w / y + Fr(z, n), True), bh(v + 1, True), bh(y / x, True)],
               "%s %s %s = %s %s %s = <b>%s</b>." % (bh(x), G, fr(c, d), bh(x), MAL, fr(d, c), bh(v, True)))


def sache():
    p, er = KIDS.next()
    kind = R.choice(["flaschen", "band", "teilen", "beutel", "strecke", "kuchen"])
    if kind == "flaschen":
        z, n = R.choice([(1, 2), (1, 4), (3, 4), (1, 5), (2, 5), (1, 3)])
        L = R.choice([3, 4, 5, 6, 9, 10, 12, 15])
        v = Fr(L) / Fr(z, n)
        if v.denominator != 1:
            return None
        return mcq("Wie viele Flaschen zu %s Liter kann man mit %d Litern Saft füllen?" % (fr(z, n), L), str(v.numerator), [bh(Fr(L * z, n), True), str(L * n), str(v.numerator + 1)],
                   "%d %s %s = %d %s %s = <b>%d</b>." % (L, G, fr(z, n), L, MAL, fr(n, z), v.numerator))
    if kind == "band":
        z, n = R.choice([(1, 4), (3, 4), (1, 2), (2, 3), (1, 3), (3, 8)])
        L = Fr(R.randint(2, 6) * z * 3, n)
        v = L / Fr(z, n)
        if v.denominator != 1 or L < 1:
            return None
        return mcq("Ein Band ist %s m lang. %s schneidet Stücke von je %s m ab. Wie viele Stücke bekommt %s?" % (bh(L, True), p, fr(z, n), er), str(v.numerator), [bh(L * Fr(z, n), True), str(v.numerator - 1), str(v.numerator * 2)],
                   "%s %s %s = %s %s %s = <b>%d</b>." % (bh(L, True), G, fr(z, n), bh(L), MAL, fr(n, z), v.numerator))
    if kind == "teilen":
        z, n = gk(2, 6)
        k = R.randint(2, 5)
        v = Fr(z, n) / k
        return mcq("%s einer Torte wird gerecht auf %d Kinder verteilt. Welchen Teil der ganzen Torte bekommt jedes Kind?" % (fr(z, n), k), bh(v), [bh(Fr(z, n) * k, True), fr(z, n + k), bh(Fr(k * n, z) if Fr(z, n * k) != Fr(k * n, z) else v * 2, True)],
                   "%s %s %d = %s %s %s = <b>%s</b>." % (fr(z, n), G, k, fr(z, n), MAL, fr(1, k), bh(v)))
    if kind == "beutel":
        z, n = R.choice([(1, 4), (1, 2), (3, 4), (2, 5), (1, 8)])
        kg = R.choice([2, 3, 4, 5, 6, 9])
        v = Fr(kg) / Fr(z, n)
        if v.denominator != 1:
            return None
        return mcq("%d kg Nüsse werden in Tüten zu je %s kg abgefüllt. Wie viele Tüten werden es?" % (kg, fr(z, n)), str(v.numerator), [bh(Fr(kg * z, n), True), str(kg * n), str(v.numerator + 2)],
                   "%d %s %s = %d %s %s = <b>%d</b> Tüten." % (kg, G, fr(z, n), kg, MAL, fr(n, z), v.numerator))
    if kind == "strecke":
        z, n = R.choice([(1, 2), (1, 4), (3, 4), (1, 3), (2, 3)])
        km = R.choice([3, 4, 6, 9, 12])
        v = Fr(km) / Fr(z, n)
        if v.denominator != 1:
            return None
        return mcq("Ein Radfahrer fährt in %s Stunde %d km. Wie viele Kilometer fährt er in einer ganzen Stunde (gleiches Tempo)?" % (fr(z, n), km), "%d km" % v.numerator, ["%s km" % bh(Fr(km * z, n), True), "%d km" % (km + n), "%d km" % (km * z)],
                   "%d %s %s = %d %s %s = <b>%d km</b>." % (km, G, fr(z, n), km, MAL, fr(n, z), v.numerator))
    z, n = gk(2, 5)
    c, d = R.choice([(1, 8), (1, 12), (1, 6), (1, 10)])
    v = Fr(z, n) / Fr(c, d)
    if v.denominator != 1:
        return None
    return mcq("Vom Kuchen ist noch %s übrig. Jedes Stück ist %s des Kuchens. Wie viele Stücke sind noch da?" % (fr(z, n), fr(c, d)), str(v.numerator), [bh(Fr(z * c, n * d)), str(d - n), str(v.numerator + 1)],
               "%s %s %s = %s %s %d = <b>%d</b>." % (fr(z, n), G, fr(c, d), fr(z, n), MAL, d, v.numerator))


def main():
    seen = set()
    sets = [
        ("Kehrwerte", mix(R, seen, [(kehrwert, 12), (durch_zahl, 8)])),
        ("Bruch durch natürliche Zahl", mix(R, seen, [(durch_zahl, 12), (zahl_durch, 8)])),
        ("Bruch durch Bruch", mix(R, seen, [(bruch_durch, 20)])),
        ("Gemischte Zahlen", mix(R, seen, [(gemischt, 14), (zahl_durch, 6)])),
        ("Sachaufgaben", mix(R, seen, [(sache, 20)])),
    ]
    body = lesson(
        ["Den <b>Kehrwert</b> eines Bruchs bekommt man, wenn man Zähler und Nenner tauscht: Kehrwert von %s ist %s." % (fr(3, 4), fr(4, 3)),
         "<b>Durch einen Bruch dividieren</b> heißt: mit seinem Kehrwert multiplizieren.",
         "Bruch durch natürliche Zahl: Den Nenner mit der Zahl multiplizieren (oder den Zähler teilen, wenn das geht).",
         "Gemischte Zahlen zuerst in unechte Brüche umwandeln."],
        [example("%s %s %s" % (fr(2, 3), G, fr(4, 5)), ["%s %s %s" % (fr(2, 3), MAL, fr(5, 4)), "= %s" % fr(10, 12)], fr(5, 6)),
         example("6 %s %s" % (G, fr(3, 4)), ["6 %s %s = %s" % (MAL, fr(4, 3), fr(24, 3))], "8")],
        [["%s %s %s = %s %s %s" % (fr(2, 3), G, fr(4, 5), fr(3, 2), MAL, fr(4, 5)), "Nur den zweiten Bruch umdrehen: %s %s %s" % (fr(2, 3), MAL, fr(5, 4))],
         ["%s %s 2 = %s (Nenner durch 2 geteilt)" % (fr(3, 8), G, fr(3, 4)), "Teilen macht kleiner, also den Nenner mal 2: %s" % fr(3, 16)],
         ["6 %s %s = %s (wie mal gerechnet)" % (G, fr(3, 4), fr(18, 4)), "6 %s %s = 8. Teilen durch einen echten Bruch macht größer." % (MAL, fr(4, 3))]])
    faq = [
        {"q": "Wie dividiert man durch einen Bruch?", "a": "Man multipliziert mit dem Kehrwert: 2/3 : 4/5 = 2/3 · 5/4 = 10/12 = 5/6."},
        {"q": "Was ist ein Kehrwert?", "a": "Der umgedrehte Bruch: Zähler und Nenner tauschen. Der Kehrwert von 5 ist 1/5."},
        {"q": "Warum wird das Ergebnis beim Teilen durch einen Bruch größer?", "a": "Man fragt, wie oft der Bruch hineinpasst. 3/4 l passt in 6 l achtmal."},
        {"q": "Wie teile ich einen Bruch durch eine natürliche Zahl?", "a": "Man multipliziert den Nenner mit der Zahl: 3/5 : 2 = 3/10."},
    ]
    make_unit(R, "brueche-dividieren", "Z",
              "Die Schülerinnen und Schüler bestimmen Kehrwerte, dividieren Brüche durch natürliche Zahlen und durch Brüche, rechnen mit gemischten Zahlen und lösen Sachaufgaben (Zusammenfassung).",
              "Brüche dividieren",
              "Brüche dividieren Klasse 6 – Kehrwert, Arbeitsblätter mit Lösungen",
              "Brüche dividieren",
              "Brüche dividieren für Klasse 6: Kehrwert, Bruch durch Zahl, Bruch durch Bruch, gemischte Zahlen und Sachaufgaben. 100 Aufgaben mit Lösungen, kostenlos.",
              "Durch einen Bruch teilen heißt: mit dem Kehrwert multiplizieren.",
              "Nur den zweiten Bruch umdrehen.",
              body, faq, sets, 6, grade="klasse-6")


if __name__ == "__main__":
    main()
