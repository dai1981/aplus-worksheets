# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 6: Gemischte Zahlen und unechte Brüche（Leitidee Zahl und Operation, Sek I）
  python3 tools/gen_de_mathe_k6_gemischte_zahlen.py
Echte und unechte Brüche, unechter Bruch → gemischte Zahl, gemischte Zahl → unechter Bruch, vergleichen, Größen (2 ¾ h), Sachaufgaben.
Fehler: Ganze mal Nenner vergessen (2 ¾ = 5/4), Rest als Zähler und Ganze als Nenner verwechselt.
"""
import random
from math import gcd
from fractions import Fraction as Fr
from de_common import lesson, example, make_unit, mix, Kids, fr, MAL, NB, table
from de_k6 import bh, mcq

R = random.Random(49603)
KIDS = Kids(R)


def gm(w, z, n):
    return "%d%s%s" % (w, NB, fr(z, n))


def zu_gemischt():
    n = R.randint(2, 12)
    w = R.randint(1, 9)
    z = R.randint(1, n - 1)
    if gcd(z, n) > 1:
        return None
    Z = w * n + z
    return mcq("Schreibe %s als gemischte Zahl." % fr(Z, n), gm(w, z, n), [gm(z, w, n) if w < n and z != w else gm(w + 1, z, n), gm(w, n - z, n) if n - z != z else gm(w - 1 if w > 1 else w + 2, z, n), gm(Z // 10 if Z >= 10 else w + 1, Z % 10 if Z % 10 and Z % 10 < n else 1, n)],
               "%d : %d = %d Rest %d. Also %d Ganze und %s: <b>%s</b>." % (Z, n, w, z, w, fr(z, n), gm(w, z, n)))


def zu_unecht():
    n = R.randint(2, 12)
    w = R.randint(1, 9)
    z = R.randint(1, n - 1)
    if gcd(z, n) > 1:
        return None
    Z = w * n + z
    return mcq("Schreibe %s als unechten Bruch." % gm(w, z, n), fr(Z, n), [fr(w + z, n), fr(w * z + n, n) if w * z + n != Z else fr(Z + 1, n), fr(Z, w * n)],
               "%d Ganze = %s. %d %s %d + %d = %d. <b>%s</b>" % (w, fr(w * n, n), w, MAL, n, z, Z, fr(Z, n)))


def art():
    kind = R.choice(["echt", "unecht", "ganz"])
    n = R.randint(2, 12)
    if kind == "echt":
        a = fr(R.randint(1, n - 1), n)
        w = [fr(n + R.randint(1, 5), n), fr(n, n), fr(2 * n + 1, n)]
        q = "Welcher Bruch ist ein <b>echter</b> Bruch?"
        e = "Bei einem echten Bruch ist der Zähler kleiner als der Nenner: <b>%s</b>." % a
    elif kind == "unecht":
        a = fr(n + R.randint(1, n), n)
        w = [fr(z, n) for z in R.sample(range(1, n), min(3, n - 1))]
        if len(w) < 3:
            return None
        q = "Welcher Bruch ist ein <b>unechter</b> Bruch?"
        e = "Bei einem unechten Bruch ist der Zähler größer als der Nenner: <b>%s</b>." % a
    else:
        k = R.randint(2, 6)
        a = fr(k * n, n)
        w = [fr(k * n + 1, n), fr(k * n - 1, n), fr(k + n, n)]
        q = "Welcher Bruch ist eine <b>ganze Zahl</b>?"
        e = "%d : %d = %d. <b>%s</b> ist eine ganze Zahl." % (k * n, n, k, a)
    return mcq(q + " " + ", ".join(sorted([a] + w)), a, w, e)


def vergleich():
    n1, n2 = R.sample([2, 3, 4, 5, 6, 8, 10], 2)
    w = R.randint(1, 5)
    z1, z2 = R.randint(1, n1 - 1), R.randint(1, n2 - 1)
    if gcd(z1, n1) > 1 or gcd(z2, n2) > 1:
        return None
    a = w + Fr(z1, n1)
    b = Fr((w * n2 + z2) + n2 * R.choice([-1, 0, 0, 1]), n2)
    if a == b or b < 1:
        return None
    s = "&lt;" if a < b else "&gt;"
    return mcq("Setze &lt;, &gt; oder = ein: %s ☐ %s" % (gm(w, z1, n1), fr(b.numerator, b.denominator) if b.denominator == n2 else fr(b.numerator * (n2 // b.denominator), n2)), s,
               [x for x in ("&lt;", "&gt;", "=") if x != s] + ["≈"], "%s = %s. Vergleiche die Ganzen, dann die Bruchteile: <b>%s</b>." % (fr(b.numerator, b.denominator), bh(b, True), s))


GR = [("h", "min", 60, [2, 3, 4, 5, 6, 10, 12, 15, 20]), ("kg", "g", 1000, [2, 4, 5, 8, 10, 20, 25]), ("km", "m", 1000, [2, 4, 5, 8, 10]), ("m", "cm", 100, [2, 4, 5, 10, 20, 25]),
      ("l", "ml", 1000, [2, 4, 5, 8, 10]), ("€", "ct", 100, [2, 4, 5, 10, 20])]


def groesse():
    g, k, f, ns = R.choice(GR)
    n = R.choice(ns)
    z = R.randint(1, n - 1)
    if gcd(z, n) > 1:
        return None
    w = R.randint(1, 5)
    v = w * f + z * f // n
    return mcq("%s %s = ? %s" % (gm(w, z, n), g, k), "%d %s" % (v, k), ["%d %s" % (x, k) for x in (w * 100 + z * f // n if f != 100 else w * 10 + z, w * f + z, w * f + f // n)],
               "%d %s = %d %s. %s %s = %d %s. Zusammen <b>%d %s</b>." % (w, g, w * f, k, fr(z, n), g, z * f // n, k, v, k))


def sache():
    p, er = KIDS.next()
    kind = R.choice(["pizza", "torte", "saft", "band", "zeit"])
    if kind in ("pizza", "torte"):
        n = R.choice([4, 6, 8, 12])
        st = R.randint(n + 1, 4 * n - 1)
        if st % n == 0:
            return None
        w, z = divmod(st, n)
        d = Fr(z, n)
        ding = "Pizzas" if kind == "pizza" else "Torten"
        return mcq("Jede von mehreren %s wird in %d gleich große Stücke geteilt. Bei der Feier werden %d Stücke gegessen. Wie viele %s sind das?" % (ding, n, st, ding), bh(Fr(st, n), True),
                   [gm(z, w, n) if 0 < w < n and gcd(w, n) == 1 else None, gm(w, z, n + w) if gcd(z, n + w) == 1 and z < n + w else None, bh(Fr(st, n) + Fr(1, d.denominator), True), bh(Fr(st, n) - 1, True)],
                   "%d : %d = %d Rest %d: <b>%s</b> %s." % (st, n, w, z, bh(Fr(st, n), True), ding))
    if kind == "saft":
        k = R.randint(5, 15)
        n = R.choice([4, 2, 5])
        tot = Fr(k, n)
        if tot.denominator == 1 or tot < 1:
            return None
        return mcq("%s füllt %d Gläser mit je %s Liter Saft. Wie viel Liter sind das zusammen?" % (p, k, fr(1, n)), bh(tot, True) + " l", [bh(Fr(k, n * 2), True) + " l" if Fr(k, 2 * n) > 1 else None, bh(tot + 1, True) + " l", "%d l" % k, bh(Fr(k + 1, n), True) + " l"],
                   "%d %s %s = %s = <b>%s l</b>." % (k, MAL, fr(1, n), fr(k, n), bh(tot, True)))
    if kind == "band":
        n = R.choice([2, 4, 5, 10])
        z = R.randint(1, n - 1)
        if gcd(z, n) > 1:
            return None
        w = R.randint(1, 4)
        return mcq("Ein Band ist %s m lang. Wie viele Zentimeter sind das?" % gm(w, z, n), "%d cm" % (w * 100 + z * 100 // n), ["%d cm" % x for x in (w * 100 + z, w * 10 + z * 10 // n, w * 100 + 100 // n)],
                   "%d m = %d cm, %s m = %d cm. <b>%d cm</b>." % (w, w * 100, fr(z, n), z * 100 // n, w * 100 + z * 100 // n))
    m = R.choice([75, 90, 100, 105, 135, 150, 165, 195, 210, 225, 255])
    v = Fr(m, 60)
    return mcq("Ein Ausflug dauert %d Minuten. Wie viele Stunden sind das als gemischte Zahl?" % m, bh(v, True) + " h", [bh(Fr(m, 100), True) + " h" if Fr(m, 100) > 1 else None, "%d%s%s h" % (m // 60, NB, fr(m % 60, 100)), bh(v + Fr(1, v.denominator), True) + " h" if (v + Fr(1, v.denominator)).denominator != 1 else None, bh(Fr(m // 60 * 60 + 60 - m % 60, 60), True) + " h" if m % 60 != 30 else None],
               "%d min = %d h %d min. %d min = %s h. <b>%s h</b>." % (m, m // 60, m % 60, m % 60, bh(Fr(m % 60, 60)), bh(v, True)))


def main():
    seen = set()
    sets = [
        ("Echte und unechte Brüche", mix(R, seen, [(art, 8), (zu_gemischt, 12)])),
        ("Gemischte Zahl in unechten Bruch", mix(R, seen, [(zu_unecht, 20)])),
        ("Vergleichen", mix(R, seen, [(vergleich, 12), (zu_gemischt, 8)])),
        ("Gemischte Zahlen bei Größen", mix(R, seen, [(groesse, 20)])),
        ("Sachaufgaben", mix(R, seen, [(sache, 20)])),
    ]
    body = lesson(
        ["Ein <b>echter Bruch</b> ist kleiner als 1 (%s). Ein <b>unechter Bruch</b> ist größer als 1 (%s)." % (fr(3, 4), fr(7, 4)),
         "Einen unechten Bruch kann man als <b>gemischte Zahl</b> schreiben: %s = 1%s%s." % (fr(7, 4), NB, fr(3, 4)),
         "Unechter Bruch → gemischte Zahl: Zähler durch Nenner teilen. Das Ergebnis sind die Ganzen, der Rest ist der neue Zähler.",
         "Gemischte Zahl → unechter Bruch: Ganze mal Nenner, plus Zähler."],
        [example("%s als gemischte Zahl" % fr(17, 5), ["17 : 5 = 3 Rest 2"], gm(3, 2, 5)),
         example("%s als unechter Bruch" % gm(2, 3, 4), ["2 %s 4 = 8" % MAL, "8 + 3 = 11"], fr(11, 4))],
        [["%s = %s" % (gm(2, 3, 4), fr(5, 4)), "Die Ganzen in Viertel umwandeln: %s" % fr(11, 4)],
         ["%s = %s (Rest und Ganze vertauscht)" % (fr(17, 5), gm(2, 3, 5)), "17 : 5 = 3 Rest 2: %s" % gm(3, 2, 5)],
         ["%s h = 2 h 30 min" % gm(2, 3, 10), "%s h = 18 min: 2 h 18 min" % fr(3, 10)]])
    faq = [
        {"q": "Was ist eine gemischte Zahl?", "a": "Eine ganze Zahl und ein Bruch zusammen, z. B. 2 3/4. Das bedeutet 2 + 3/4."},
        {"q": "Wie wandle ich einen unechten Bruch in eine gemischte Zahl um?", "a": "Teile den Zähler durch den Nenner. 17/5: 17 : 5 = 3 Rest 2, also 3 2/5."},
        {"q": "Wie wandle ich eine gemischte Zahl in einen Bruch um?", "a": "Ganze mal Nenner plus Zähler: 2 3/4 = (2 · 4 + 3)/4 = 11/4."},
        {"q": "Was ist ein unechter Bruch?", "a": "Ein Bruch, dessen Zähler größer als der Nenner ist, z. B. 9/4. Er ist größer als 1."},
    ]
    make_unit(R, "gemischte-zahlen", "Z",
              "Die Schülerinnen und Schüler unterscheiden echte und unechte Brüche, wandeln unechte Brüche und gemischte Zahlen ineinander um und nutzen gemischte Zahlen bei Größen (Zusammenfassung).",
              "Gemischte Zahlen und unechte Brüche",
              "Gemischte Zahlen Klasse 6 – unechte Brüche umwandeln, Arbeitsblätter",
              "Gemischte Zahlen",
              "Gemischte Zahlen für Klasse 6: echte und unechte Brüche, umwandeln, vergleichen und Größen. 100 Aufgaben mit Lösungen, kostenlos.",
              "Gemischte Zahl → Bruch: Ganze mal Nenner plus Zähler.",
              "Bruch → gemischte Zahl: Zähler durch Nenner mit Rest teilen.",
              body, faq, sets, 3, grade="klasse-6")


if __name__ == "__main__":
    main()
