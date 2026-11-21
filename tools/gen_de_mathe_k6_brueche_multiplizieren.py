# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 6: Brüche multiplizieren（Leitidee Zahl und Operation, Sek I）
  python3 tools/gen_de_mathe_k6_brueche_multiplizieren.py
Bruch mal natürliche Zahl, Bruch mal Bruch, vorher kürzen, gemischte Zahlen, Bruchteile von Größen und von Bruchteilen, Sachaufgaben.
Fehler: auch den Nenner mit der natürlichen Zahl multipliziert, vorher gleichnamig gemacht, gemischte Zahlen Ganze mal Ganze und Bruch mal Bruch.
"""
import random
from math import gcd
from fractions import Fraction as Fr
from de_common import lesson, example, make_unit, mix, Kids, fr, MAL, NB, table
from de_k6 import bh, mcq

R = random.Random(49605)
KIDS = Kids(R)


def gk(lo=2, hi=12):
    while True:
        n = R.randint(lo, hi)
        z = R.randint(1, n - 1)
        if gcd(z, n) == 1:
            return z, n


def mal_zahl():
    z, n = gk()
    k = R.randint(2, 12)
    v = Fr(z * k, n)
    rev = R.random() < 0.4
    q = ("%d %s %s = ?" % (k, MAL, fr(z, n))) if rev else ("%s %s %d = ?" % (fr(z, n), MAL, k))
    return mcq(q, bh(v, True), [fr(z * k, n * k), fr(z, n * k), bh(v + Fr(1, v.denominator), True), fr(z + k, n) if Fr(z + k, n) != v else None],
               "Nur den Zähler mit %d multiplizieren: %s%s." % (k, fr(z * k, n), (" = <b>%s</b>" % bh(v, True)) if v.denominator != n or v > 1 else ""))


def mal_bruch():
    a, b = gk(2, 10)
    c, d = gk(2, 10)
    v = Fr(a * c, b * d)
    h = b * d // gcd(b, d)
    w = [bh(Fr(a * c, h)) if Fr(a * c, h) != v else None, fr(a + c, b + d), fr(a * d, b * c) if Fr(a * d, b * c) != v else None, bh(Fr(a, b) + Fr(c, d), True), fr(a * c, b + d)]
    return mcq("%s %s %s = ?" % (fr(a, b), MAL, fr(c, d)), bh(v, True), w,
               "Zähler mal Zähler, Nenner mal Nenner: %s%s." % (fr(a * c, b * d), (" = <b>%s</b>" % bh(v, True)) if v.denominator != b * d or v > 1 else ""))


def kuerzen_vorher():
    while True:
        a, b, c, d = R.randint(1, 9), R.randint(2, 12), R.randint(1, 9), R.randint(2, 12)
        if a < b and c < d and gcd(a, b) == 1 and gcd(c, d) == 1 and (gcd(a, d) > 1 or gcd(c, b) > 1):
            break
    v = Fr(a * c, b * d)
    return mcq("Kürze vor dem Ausrechnen: %s %s %s = ?" % (fr(a, b), MAL, fr(c, d)), bh(v), [fr(a * c, b * d), bh(v * 2) if v * 2 < 1 else bh(v / 2), fr(a + c, b + d), bh(Fr(a, b) + Fr(c, d), True)],
               "Über Kreuz kürzen (Zähler des einen mit Nenner des anderen). Ergebnis: %s = <b>%s</b>." % (fr(a * c, b * d), bh(v)))


def gemischt():
    w1 = R.randint(1, 4)
    z1, n1 = gk(2, 6)
    kind = R.choice(["zahl", "bruch"])
    x = w1 + Fr(z1, n1)
    if kind == "zahl":
        k = R.randint(2, 6)
        v = x * k
        return mcq("%d%s%s %s %d = ?" % (w1, NB, fr(z1, n1), MAL, k), bh(v, True), [bh(w1 * k + Fr(z1, n1), True), bh(w1 * k + Fr(z1 * k, n1 * k), True), bh(v + 1, True), bh(v - Fr(1, v.denominator), True) if v.denominator > 1 else bh(v - 1, True)],
                   "%d Ganze %s %d = %d, %s %s %d = %s. Zusammen <b>%s</b>." % (w1, MAL, k, w1 * k, fr(z1, n1), MAL, k, bh(Fr(z1 * k, n1), True), bh(v, True)))
    z2, n2 = gk(2, 6)
    w2 = R.randint(1, 3)
    y = w2 + Fr(z2, n2)
    v = x * y
    return mcq("%d%s%s %s %d%s%s = ?" % (w1, NB, fr(z1, n1), MAL, w2, NB, fr(z2, n2)), bh(v, True), [bh(w1 * w2 + Fr(z1 * z2, n1 * n2), True), bh(v + 1, True), bh(x + y, True), bh(v - Fr(1, v.denominator), True) if v.denominator > 1 else None],
               "In unechte Brüche umwandeln: %s %s %s = %s = <b>%s</b>." % (bh(x), MAL, bh(y), bh(v), bh(v, True)))


GR = [("h", "min", 60), ("kg", "g", 1000), ("km", "m", 1000), ("m", "cm", 100), ("€", "ct", 100), ("l", "ml", 1000)]


def von():
    kind = R.choice(["groesse", "bruchteil", "menge"])
    if kind == "groesse":
        g, k, f = R.choice(GR)
        z, n = gk(2, 10)
        m = R.randint(2, 9)
        tot = m * f
        if tot * z % n:
            return None
        v = tot * z // n
        return mcq("Berechne %s von %d %s." % (fr(z, n), m, g), "%d %s" % (v, k), ["%d %s" % (x, k) for x in (tot // n if z > 1 else tot * z, tot * n // z if tot * n % z == 0 and z > 1 else v * 10, tot - v if tot - v != v else v * 2, v // 10 if v % 10 == 0 else v + 1)],
                   "%d %s = %d %s. %d : %d %s %d = <b>%d %s</b>." % (m, g, tot, k, tot, n, MAL, z, v, k))
    if kind == "bruchteil":
        a, b = gk(2, 6)
        c, d = gk(2, 6)
        v = Fr(a * c, b * d)
        return mcq("Wie viel ist %s von %s?" % (fr(a, b), fr(c, d)), bh(v), [bh(Fr(a, b) + Fr(c, d), True), fr(a + c, b + d), bh(Fr(a, b) - Fr(c, d)) if Fr(a, b) > Fr(c, d) else bh(Fr(c, d) - Fr(a, b)) if Fr(c, d) != Fr(a, b) else None, fr(a * c, b + d)],
                   "„von“ heißt „mal“: %s %s %s = <b>%s</b>." % (fr(a, b), MAL, fr(c, d), bh(v)))
    z, n = gk(2, 10)
    N = n * R.randint(2, 12)
    return mcq("Berechne %s von %d." % (fr(z, n), N), str(N * z // n), [str(N // n), str(N * n // z) if N * n % z == 0 and z > 1 else str(N * z // n + z), str(N - N * z // n)],
               "%d : %d = %d, %d %s %d = <b>%d</b>." % (N, n, N // n, N // n, MAL, z, N * z // n))


def sache():
    p, er = KIDS.next()
    kind = R.choice(["garten", "flaschen", "weg", "rezept", "flaeche", "geld"])
    if kind == "garten":
        a, b = gk(2, 5)
        c, d = gk(2, 5)
        v = Fr(a * c, b * d)
        return mcq("%s des Gartens ist Rasen. Auf %s des Rasens stehen Bäume. Welcher Anteil des ganzen Gartens ist das?" % (fr(a, b), fr(c, d)), bh(v), [bh(Fr(a, b) + Fr(c, d), True), fr(a + c, b + d), bh(Fr(c, d))],
                   "%s von %s: %s %s %s = <b>%s</b>." % (fr(c, d), fr(a, b), fr(c, d), MAL, fr(a, b), bh(v)))
    if kind == "flaschen":
        k = R.randint(3, 12)
        z, n = R.choice([(1, 2), (3, 4), (1, 4), (2, 5), (3, 10), (1, 5)])
        v = Fr(z * k, n)
        return mcq("%s kauft %d Flaschen mit je %s Liter Wasser. Wie viel Liter sind das?" % (p, k, fr(z, n)), bh(v, True) + " l", [bh(Fr(z * k, n * k)) + " l", bh(v + 1, True) + " l", "%d l" % (z * k)],
                   "%d %s %s = %s = <b>%s l</b>." % (k, MAL, fr(z, n), fr(z * k, n), bh(v, True)))
    if kind == "weg":
        w = R.randint(2, 9)
        z, n = R.choice([(1, 2), (3, 4), (1, 4), (2, 3), (1, 3), (3, 5)])
        km = w + Fr(z, n)
        t = R.randint(2, 5)
        v = km * t
        return mcq("Der Schulweg von %s ist %s km lang. Wie viele Kilometer sind %d Schulwege?" % (p, bh(km, True), t), bh(v, True) + " km", [bh(w * t + Fr(z, n), True) + " km", bh(v + 1, True) + " km", bh(km + t, True) + " km"],
                   "%s %s %d = %s %s %d = <b>%s km</b>." % (bh(km, True), MAL, t, bh(km), MAL, t, bh(v, True)))
    if kind == "rezept":
        z, n = R.choice([(3, 4), (1, 2), (2, 3), (1, 4), (3, 8)])
        f = R.choice([Fr(1, 2), Fr(3, 2), Fr(2), Fr(1, 3)])
        v = Fr(z, n) * f
        menge = "die doppelte Menge" if f == 2 else "%s des Rezepts" % bh(f, True)
        return mcq("Für ein Rezept braucht man %s Liter Milch. %s macht %s. Wie viel Milch braucht %s?" % (fr(z, n), p, menge, er),
                   bh(v, True) + " l", [bh(Fr(z, n) + f, True) + " l", bh(Fr(z, n) / f, True) + " l" if Fr(z, n) / f != v else None, bh(v + Fr(1, 4), True) + " l"],
                   "%s %s %s = <b>%s l</b>." % (fr(z, n), MAL, bh(f, True), bh(v, True)))
    if kind == "flaeche":
        a, b = gk(2, 6)
        c, d = gk(2, 6)
        v = Fr(a * c, b * d)
        return mcq("Ein Rechteck ist %s m lang und %s m breit. Wie groß ist seine Fläche?" % (fr(a, b), fr(c, d)), bh(v) + " m²", [bh(Fr(a, b) + Fr(c, d), True) + " m²", bh(2 * (Fr(a, b) + Fr(c, d)), True) + " m²", fr(a + c, b + d) + " m²"],
                   "A = %s %s %s = <b>%s m²</b>." % (fr(a, b), MAL, fr(c, d), bh(v)))
    g = R.choice([12, 18, 20, 24, 30, 36, 40, 45, 60])
    z, n = R.choice([(1, 3), (2, 3), (1, 4), (3, 4), (2, 5), (1, 6), (5, 6)])
    if g % n:
        return None
    s = g * z // n
    return mcq("%s hat %d € Taschengeld und gibt %s davon für ein Buch aus. Wie viel Euro kostet das Buch?" % (p, g, fr(z, n)), "%d €" % s, ["%d €" % x for x in (g // n, g - s, g * n // z if g * n % z == 0 and z > 1 else s + n)],
               "%d € : %d %s %d = <b>%d €</b>." % (g, n, MAL, z, s))


def main():
    seen = set()
    sets = [
        ("Bruch mal natürliche Zahl", mix(R, seen, [(mal_zahl, 20)])),
        ("Bruch mal Bruch", mix(R, seen, [(mal_bruch, 20)])),
        ("Vorher kürzen", mix(R, seen, [(kuerzen_vorher, 14), (mal_bruch, 6)])),
        ("Gemischte Zahlen und „von“", mix(R, seen, [(gemischt, 10), (von, 10)])),
        ("Sachaufgaben", mix(R, seen, [(sache, 20)])),
    ]
    body = lesson(
        ["<b>Bruch mal natürliche Zahl</b>: Nur den Zähler multiplizieren, der Nenner bleibt.",
         "<b>Bruch mal Bruch</b>: Zähler mal Zähler und Nenner mal Nenner. Man muss nicht gleichnamig machen.",
         "Vor dem Ausrechnen kann man <b>über Kreuz kürzen</b>. Das spart große Zahlen.",
         "„%s von %s“ bedeutet %s %s %s." % (fr(2, 3), fr(3, 4), fr(2, 3), MAL, fr(3, 4)),
         "Gemischte Zahlen zuerst in unechte Brüche umwandeln."],
        [example("%s %s %s" % (fr(2, 3), MAL, fr(4, 5)), ["2 %s 4 = 8" % MAL, "3 %s 5 = 15" % MAL], fr(8, 15)),
         example("%s %s %s" % (fr(3, 8), MAL, fr(4, 9)), ["3 und 9 durch 3 kürzen", "4 und 8 durch 4 kürzen", "%s %s %s" % (fr(1, 2), MAL, fr(1, 3))], fr(1, 6))],
        [["%s %s 4 = %s" % (fr(2, 5), MAL, fr(8, 20)), "Nur der Zähler: %s" % fr(8, 5)],
         ["Erst den Hauptnenner bilden", "Beim Multiplizieren nicht nötig"],
         ["2%s%s %s 2%s%s = 4%s%s" % (NB, fr(1, 2), MAL, NB, fr(1, 2), NB, fr(1, 4)), "%s %s %s = %s = 6%s%s" % (fr(5, 2), MAL, fr(5, 2), fr(25, 4), NB, fr(1, 4))]])
    faq = [
        {"q": "Wie multipliziert man zwei Brüche?", "a": "Zähler mal Zähler und Nenner mal Nenner, z. B. 2/3 · 4/5 = 8/15."},
        {"q": "Muss ich vorher einen Hauptnenner bilden?", "a": "Nein, beim Multiplizieren nicht. Den Hauptnenner braucht man nur beim Addieren und Subtrahieren."},
        {"q": "Was bedeutet „2/3 von 6“?", "a": "„von“ heißt mal: 2/3 · 6 = 4."},
        {"q": "Warum wird das Ergebnis manchmal kleiner?", "a": "Wenn man mit einem echten Bruch multipliziert, nimmt man nur einen Teil. Das Ergebnis ist kleiner als die Ausgangszahl."},
    ]
    make_unit(R, "brueche-multiplizieren", "Z",
              "Die Schülerinnen und Schüler multiplizieren Brüche mit natürlichen Zahlen und mit Brüchen, kürzen vor dem Ausrechnen, bestimmen Bruchteile und lösen Sachaufgaben (Zusammenfassung).",
              "Brüche multiplizieren",
              "Brüche multiplizieren Klasse 6 – Arbeitsblätter mit Lösungen",
              "Brüche multiplizieren",
              "Brüche multiplizieren für Klasse 6: Bruch mal Zahl, Bruch mal Bruch, kürzen, gemischte Zahlen und Bruchteile. 100 Aufgaben mit Lösungen, kostenlos.",
              "Zähler mal Zähler, Nenner mal Nenner.",
              "„von“ heißt „mal“.",
              body, faq, sets, 5, grade="klasse-6")


if __name__ == "__main__":
    main()
