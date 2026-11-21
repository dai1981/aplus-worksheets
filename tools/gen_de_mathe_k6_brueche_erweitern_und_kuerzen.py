# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 6: Brüche erweitern und kürzen（Leitidee Zahl und Operation, Sek I）
  python3 tools/gen_de_mathe_k6_brueche_erweitern_und_kuerzen.py
Erweitern, Kürzen, vollständig kürzen mit dem ggT, gleichwertige Brüche, fehlende Zähler und Nenner, Anteile als gekürzte Brüche.
Fehler: nur Zähler oder nur Nenner verändert, subtrahiert statt dividiert, nicht vollständig gekürzt.
"""
import random
from math import gcd
from fractions import Fraction as Fr
from de_common import lesson, example, make_unit, mix, Kids, fr, MAL, GETEILT, table
from de_k6 import bh, fq, mcq

R = random.Random(49601)
KIDS = Kids(R)


def gk(lo=2, hi=12):
    while True:
        n = R.randint(lo, hi)
        z = R.randint(1, n - 1)
        if gcd(z, n) == 1:
            return z, n


def erweitern():
    z, n = gk(2, 10)
    k = R.randint(2, 9)
    kind = R.choice(["mit", "zaehler", "nenner"])
    if kind == "mit":
        return mcq("Erweitere %s mit %d." % (fr(z, n), k), fr(z * k, n * k), [fr(z * k, n), fr(z, n * k), fr(z + k, n + k), fr(z * k, n + k)],
                   "Zähler und Nenner mal %d: %d %s %d = %d, %d %s %d = %d. <b>%s</b>" % (k, z, MAL, k, z * k, n, MAL, k, n * k, fr(z * k, n * k)))
    if kind == "zaehler":
        return mcq("Ergänze: %s = %s" % (fr(z, n), fr("?", n * k)), str(z * k), [str(z + n * k - n), str(z * n * k), str(z + k)],
                   "Der Nenner wurde mit %d multipliziert (%d %s %d = %d). Also auch der Zähler: %d %s %d = <b>%d</b>." % (k, n, MAL, k, n * k, z, MAL, k, z * k))
    return mcq("Ergänze: %s = %s" % (fr(z, n), fr(z * k, "?")), str(n * k), [str(n + z * k - z), str(n * z * k), str(n * k + 1)],
               "Der Zähler wurde mit %d multipliziert. Also auch der Nenner: %d %s %d = <b>%d</b>." % (k, n, MAL, k, n * k))


def kuerzen():
    z, n = gk(2, 12)
    k = R.choice([2, 3, 4, 5, 6, 7, 8, 9, 10, 12])
    Z, N = z * k, n * k
    kind = R.choice(["voll", "voll", "durch"])
    if kind == "durch":
        d = R.choice([x for x in range(2, k + 1) if k % x == 0])
        return mcq("Kürze %s durch %d." % (fr(Z, N), d), fr(Z // d, N // d), [fr(Z - d, N - d), fr(Z // d, N), fr(Z, N // d), fr(Z // d + 1, N // d)],
                   "Zähler und Nenner durch %d: <b>%s</b>." % (d, fr(Z // d, N // d)))
    p = min(x for x in range(2, k + 1) if k % x == 0)
    w = [fr(Z // p, N // p) if p < k else fr(Z - 1, N - 1), fr(z, n + 1), fr(Z - z, N - n) if Z - z > 0 and (Z - z, N - n) != (z, n) else fr(z + 1, n)]
    return mcq("Kürze %s vollständig." % fr(Z, N), fr(z, n), w, "ggT(%d, %d) = %d. %d : %d = %d, %d : %d = %d. <b>%s</b>" % (Z, N, k, Z, k, z, N, k, n, fr(z, n)))


def gleich():
    z, n = gk(2, 9)
    k1, k2 = R.sample(range(2, 8), 2)
    a = fr(z * k1, n * k1)
    kind = R.choice(["welcher", "nicht"])
    if kind == "welcher":
        good = fr(z * k2, n * k2)
        bad = [fr(z * k2, n * k2 + 1), fr(z + k2, n + k2), fr(z * k2 + 1, n * k2), fr(n * k2, z * k2) if z != n else fr(1, 2)]
        return mcq("Welcher Bruch ist gleich %s?" % a, good, bad, "%s = %s = <b>%s</b> (gekürzt und neu erweitert)." % (a, fr(z, n), good))
    goods = [fr(z * k, n * k) for k in (1, k2, k2 + 1)]
    bad = fr(z + k2, n + k2)
    if bad in goods:
        return None
    return mcq("Welcher Bruch ist <b>nicht</b> gleich %s? %s" % (a, ", ".join(sorted(goods + [bad]))), bad, goods, "Alle anderen ergeben gekürzt %s. %s nicht: Hier wurde addiert statt multipliziert. <b>%s</b>" % (fr(z, n), bad, bad))


def hundert():
    kind = R.choice(["h", "z", "t"])
    if kind == "h":
        n = R.choice([2, 4, 5, 20, 25, 50])
        z = R.choice([x for x in range(1, n) if gcd(x, n) == 1])
        k = 100 // n
        return mcq("Erweitere %s auf den Nenner 100." % fr(z, n), fr(z * k, 100), [fr(z, 100), fr(z + 100 - n, 100), fr(z * 10, 100) if z * 10 != z * k else fr(z * k + 1, 100)],
                   "%d %s %d = 100, also Zähler %s %d: <b>%s</b>." % (n, MAL, k, MAL, k, fr(z * k, 100)))
    if kind == "z":
        n = R.choice([2, 5])
        z = R.choice([x for x in range(1, n) if gcd(x, n) == 1])
        k = 10 // n
        return mcq("Erweitere %s auf den Nenner 10." % fr(z, n), fr(z * k, 10), [fr(z, 10), fr(z + 10 - n, 10), fr(z * k + 1, 10)], "%d %s %d = 10: <b>%s</b>." % (n, MAL, k, fr(z * k, 10)))
    n = R.choice([8, 4, 125, 250, 40, 200])
    z = R.choice([x for x in range(1, min(n, 40)) if gcd(x, n) == 1])
    k = 1000 // n
    return mcq("Erweitere %s auf den Nenner 1000." % fr(z, n), fr(z * k, 1000), [fr(z, 1000), fr(z * k // 10 if z * k % 10 == 0 else z * k + 1, 1000), fr(z * k, 100)], "%d %s %d = 1000: <b>%s</b>." % (n, MAL, k, fr(z * k, 1000)))


def sache():
    kind = R.choice(["klasse", "minuten", "geld", "spiel", "saft", "cm"])
    if kind == "klasse":
        t = R.choice([24, 25, 27, 28, 30, 32])
        h = R.choice([x for x in range(2, t) if gcd(x, t) > 1])
        g = gcd(h, t)
        what = R.choice(["fahren mit dem Bus", "haben ein Haustier", "spielen ein Instrument", "sind im Sportverein"])
        return mcq("In einer Klasse mit %d Kindern %s %d Kinder. Welcher gekürzte Bruch gibt diesen Anteil an?" % (t, what, h), bh(Fr(h, t)), [fr(h, t), fr(t - h, t) if gcd(t - h, t) == 1 else bh(Fr(t - h, t)), fr(h // g, t), fr(t // g, h // g) if h // g > 1 else fr(1, h)],
                   "%s, gekürzt durch %d: <b>%s</b>." % (fr(h, t), g, bh(Fr(h, t))))
    if kind == "minuten":
        m = R.choice([10, 12, 15, 20, 24, 25, 30, 36, 40, 45, 48, 50])
        return mcq("Welcher Bruchteil einer Stunde sind %d Minuten?" % m, bh(Fr(m, 60)), [fr(m, 100), fr(1, m) if m < 60 else fr(1, 2), fr(m // gcd(m, 60), 100), bh(Fr(m, 60) + Fr(1, 60 // gcd(m, 60)))],
                   "1 h = 60 min. %s = <b>%s</b>." % (fr(m, 60), bh(Fr(m, 60))))
    if kind == "geld":
        c = R.choice([5, 10, 20, 25, 40, 50, 60, 75, 80])
        return mcq("Welcher Bruchteil von 1 € sind %d ct?" % c, bh(Fr(c, 100)), [fr(c, 10) if c < 10 else fr(1, c), bh(Fr(c, 100) + Fr(1, 100 // gcd(c, 100))), fr(100 // gcd(c, 100), c // gcd(c, 100)) if c // gcd(c, 100) > 1 else fr(2, 100 // gcd(c, 100) + 1)],
                   "1 € = 100 ct. %s = <b>%s</b>." % (fr(c, 100), bh(Fr(c, 100))))
    if kind == "spiel":
        n = R.choice([12, 15, 16, 18, 20, 24])
        w = R.choice([x for x in range(2, n) if gcd(x, n) > 1])
        p, er = KIDS.next()
        return mcq("%s hat %d von %d Spielen gewonnen. Welchen Anteil hat %s gewonnen (gekürzt)?" % (p, w, n, er), bh(Fr(w, n)), [fr(w, n), bh(Fr(n - w, n)), fr(w // gcd(w, n), n), fr(n // gcd(w, n), w // gcd(w, n)) if w // gcd(w, n) > 1 else None],
                   "%s = <b>%s</b>." % (fr(w, n), bh(Fr(w, n))))
    if kind == "saft":
        ml = R.choice([100, 150, 200, 250, 300, 400, 500, 600, 750])
        return mcq("Welcher Bruchteil von 1 Liter sind %d ml?" % ml, bh(Fr(ml, 1000)), [fr(ml, 100) if ml < 100 else fr(ml // 50, 100 // 5), bh(Fr(ml, 1000) + Fr(1, Fr(ml, 1000).denominator)), fr(1, ml // 50) if ml // 50 > 1 else fr(1, 3)],
                   "1 l = 1000 ml. %s = <b>%s</b>." % (fr(ml, 1000), bh(Fr(ml, 1000))))
    c = R.choice([10, 20, 25, 30, 40, 50, 60, 75, 80])
    return mcq("Welcher Bruchteil von 1 m sind %d cm?" % c, bh(Fr(c, 100)), [fr(c, 1000), bh(Fr(c, 100) + Fr(1, Fr(c, 100).denominator)), fr(1, c // 10) if c // 10 > 1 else fr(1, 3)],
               "1 m = 100 cm. %s = <b>%s</b>." % (fr(c, 100), bh(Fr(c, 100))))


def main():
    seen = set()
    sets = [
        ("Erweitern", mix(R, seen, [(erweitern, 20)])),
        ("Kürzen", mix(R, seen, [(kuerzen, 20)])),
        ("Gleichwertige Brüche", mix(R, seen, [(gleich, 14), (erweitern, 6)])),
        ("Auf 10, 100 und 1000 erweitern", mix(R, seen, [(hundert, 14), (kuerzen, 6)])),
        ("Anteile in Sachaufgaben", mix(R, seen, [(sache, 20)])),
    ]
    body = lesson(
        ["<b>Erweitern</b>: Zähler und Nenner mit derselben Zahl multiplizieren. Der Wert des Bruchs bleibt gleich.",
         "<b>Kürzen</b>: Zähler und Nenner durch dieselbe Zahl dividieren.",
         "<b>Vollständig gekürzt</b> ist ein Bruch, wenn Zähler und Nenner keinen gemeinsamen Teiler mehr haben. Am schnellsten kürzt man mit dem ggT.",
         "Erweitern und Kürzen ändern nur die Einteilung: Es sind mehr kleinere oder weniger größere Stücke."],
        [example("Erweitere %s mit 4" % fr(3, 5), ["3 %s 4 = 12" % MAL, "5 %s 4 = 20" % MAL], fr(12, 20)),
         example("Kürze %s vollständig" % fr(18, 24), ["ggT(18, 24) = 6", "18 : 6 = 3, 24 : 6 = 4"], fr(3, 4))],
        [["%s mit 2 erweitert: %s" % (fr(2, 3), fr(4, 3)), "Auch den Nenner: %s" % fr(4, 6)],
         ["%s gekürzt: %s (minus 2)" % (fr(6, 8), fr(4, 6)), "Dividieren, nicht subtrahieren: %s" % fr(3, 4)],
         ["%s = %s und fertig" % (fr(12, 18), fr(6, 9)), "Weiter kürzen: %s" % fr(2, 3)]])
    faq = [
        {"q": "Was bedeutet einen Bruch erweitern?", "a": "Man multipliziert Zähler und Nenner mit derselben Zahl. Der Bruch bleibt gleich groß, z. B. 2/3 = 8/12."},
        {"q": "Was bedeutet einen Bruch kürzen?", "a": "Man dividiert Zähler und Nenner durch dieselbe Zahl, z. B. 15/20 = 3/4 (durch 5)."},
        {"q": "Wann ist ein Bruch vollständig gekürzt?", "a": "Wenn Zähler und Nenner nur noch den gemeinsamen Teiler 1 haben."},
        {"q": "Wie kürze ich am schnellsten?", "a": "Mit dem größten gemeinsamen Teiler (ggT) von Zähler und Nenner. Dann reicht ein Schritt."},
    ]
    make_unit(R, "brueche-erweitern-und-kuerzen", "Z",
              "Die Schülerinnen und Schüler erweitern und kürzen Brüche, erkennen gleichwertige Brüche und geben Anteile als vollständig gekürzte Brüche an (Zusammenfassung).",
              "Brüche erweitern und kürzen",
              "Brüche erweitern und kürzen Klasse 6 – Arbeitsblätter mit Lösungen",
              "Erweitern & Kürzen",
              "Brüche erweitern und kürzen für Klasse 6: vollständig kürzen mit dem ggT, gleichwertige Brüche, Anteile. 100 Aufgaben mit Lösungen, kostenlos.",
              "Zähler und Nenner immer mit derselben Zahl.",
              "Erweitern: mal. Kürzen: geteilt durch.",
              body, faq, sets, 1, grade="klasse-6")


if __name__ == "__main__":
    main()
