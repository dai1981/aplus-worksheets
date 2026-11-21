# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 5: Brüche und Anteile（Leitidee Zahl und Operation, Sek I）
  python3 tools/gen_de_mathe_k5_brueche_und_anteile.py
Bruchteile ablesen, Bruchteile von Größen und Mengen, erweitern und kürzen, Brüche vergleichen und am Zahlenstrahl, Anteile in Sachaufgaben.
Rechteckbilder aus Klasse 4 (gen_de_mathe_k4_brueche.rect_svg) mit eigenem Zufall.
Fehler: Zähler und Nenner vertauscht, beim Erweitern nur den Zähler verändert, 1/8 > 1/4 (weil 8 > 4).
"""
import random
from math import gcd
from de_common import mcq, num, lesson, example, make_unit, mix, Kids, fr, MAL, GETEILT, zahlenstrahl, table
import gen_de_mathe_k4_brueche as k4

R = random.Random(49509)
k4.R = random.Random(49559)
KIDS = Kids(R)


def ablesen():
    n = R.choice([3, 4, 5, 6, 8, 9, 10, 12])
    k = R.randint(1, n - 1)
    cols = n if n <= 6 else {8: 4, 9: 3, 10: 5, 12: 4}[n]
    pic = k4.rect_svg(n, k, cols)
    g = gcd(k, n)
    w = [fr(n - k, n), fr(k, n - k) if n - k != k else fr(k, n + 1), fr(k + 1, n), fr(k - 1, n) if k > 1 else fr(k, n - 1), fr(n, k) if k > 1 else fr(2, n)]
    if g > 1 and R.random() < 0.5:
        ans = fr(k // g, n // g)
        return mcq(pic + "Welcher <b>gekürzte</b> Bruch gibt den gefärbten Anteil an?", ans, [fr(k, n), fr(n // g - k // g, n // g), fr(k // g, n), fr(n // g, k // g) if k // g > 1 else fr(k // g + 1, n // g)],
                   "%s gefärbt, gekürzt durch %d: <b>%s</b>." % (fr(k, n), g, ans))
    return mcq(pic + "Welcher Bruchteil ist gefärbt?", fr(k, n), w, "%d von %d gleich großen Teilen: <b>%s</b>." % (k, n, fr(k, n)))


GR = [("h", "min", 60), ("kg", "g", 1000), ("km", "m", 1000), ("m", "cm", 100), ("€", "ct", 100), ("l", "ml", 1000), ("Tag", "h", 24), ("Jahr", "Monate", 12)]


def von():
    kind = R.choice(["menge", "groesse", "groesse"])
    if kind == "menge":
        n = R.choice([3, 4, 5, 6, 8, 10])
        z = R.randint(1, n - 1)
        tot = n * R.randint(3, 15)
        r = tot // n * z
        what = R.choice(["Kinder", "Bonbons", "Murmeln", "Seiten", "Schülerinnen und Schüler"])
        return mcq("Wie viel sind %s von %d %s?" % (fr(z, n), tot, what), "%d %s" % (r, what), ["%d %s" % (x, what) for x in (tot // n, tot * z, tot - r)],
                   "%d : %d = %d (ein %s). %d %s %d = <b>%d</b>." % (tot, n, tot // n, "Teil", tot // n, MAL, z, r))
    big, small, f = R.choice(GR)
    ds = [d for d in (2, 3, 4, 5, 6, 10, 12) if f % d == 0]
    n = R.choice(ds)
    z = R.randint(1, n - 1)
    r = f // n * z
    return mcq("%s %s = ? %s" % (fr(z, n), big, small), "%d %s" % (r, small), ["%d %s" % (x, small) for x in (f // n, z * 10 if z * 10 != r else r + f // n, r + f // n)],
               "1 %s = %s %s. %s : %d = %d, mal %d = <b>%d %s</b>." % (big, num(f), small, num(f), n, f // n, z, r, small))


def erweitern():
    n = R.choice([2, 3, 4, 5, 6, 7, 8, 9])
    z = R.randint(1, n - 1)
    if gcd(z, n) > 1:
        return None
    k = R.randint(2, 6)
    kind = R.choice(["erw", "kuerz", "luecke", "gleich"])
    if kind == "erw":
        return mcq("Erweitere %s mit %d." % (fr(z, n), k), fr(z * k, n * k), [fr(z * k, n), fr(z, n * k), fr(z + k, n + k)],
                   "Zähler und Nenner mal %d: <b>%s</b>." % (k, fr(z * k, n * k)))
    if kind == "kuerz":
        return mcq("Kürze %s vollständig." % fr(z * k, n * k), fr(z, n), [fr(z * k // 2, n * k // 2) if k % 2 == 0 and k > 2 else fr(z * k, n), fr(z, n * k), fr(n, z) if z > 1 else fr(z + 1, n)],
                   "Teile Zähler und Nenner durch %d: <b>%s</b>." % (k, fr(z, n)))
    if kind == "luecke":
        return mcq("%s = ? / %d (Welcher Zähler fehlt?)" % (fr(z, n), n * k), str(z * k), [str(z + k), str(z * k + 1), str(n * k - z)],
                   "Der Nenner wurde mit %d multipliziert, also auch der Zähler: <b>%d</b>." % (k, z * k))
    good = fr(z * k, n * k)
    bads = [fr(z + k, n + k), fr(z * k, n * k + 1), fr(z * (k + 1), n * k)]
    return mcq("Welcher Bruch ist gleich %s?" % fr(z, n), good, bads, "Mit %d erweitert: <b>%s</b>." % (k, good))


def vergleich():
    kind = R.choice(["gleichnamig", "zaehler1", "strahl", "strahl"])
    if kind == "gleichnamig":
        n = R.randint(5, 12)
        a, b = R.sample(range(1, n), 2)
        big = fr(max(a, b), n)
        return mcq("Welcher Bruch ist größer: %s oder %s?" % (fr(a, n), fr(b, n)), big, [fr(min(a, b), n), "Beide sind gleich groß", "Das kann man nicht sagen"],
                   "Gleicher Nenner: der größere Zähler gewinnt. <b>%s</b>." % big)
    if kind == "zaehler1":
        a, b = R.sample([2, 3, 4, 5, 6, 8, 10, 12], 2)
        big = fr(1, min(a, b))
        return mcq("Welcher Bruch ist größer: %s oder %s?" % (fr(1, a), fr(1, b)), big, [fr(1, max(a, b)), "Beide sind gleich groß", "Das kann man nicht sagen"],
                   "Je mehr Teile, desto kleiner ist jedes Teil. <b>%s</b> ist größer." % big)
    n = R.choice([4, 5, 8, 10])
    z = R.randint(1, n - 1)
    pic = zahlenstrahl(0, n, 1, marks=[(z, "A")], labels=[0, n], label="Zahlenstrahl von 0 bis 1")
    pic = pic.replace(">%d<" % n, ">1<")
    return mcq(pic + "Der Zahlenstrahl geht von 0 bis 1. Welcher Bruch gehört zum Pfeil A?", fr(z, n), [fr(z, n + 1), fr(n - z, n) if n - z != z else fr(z + 1, n), fr(z, 10) if n != 10 else fr(z, 8)],
               "Die Strecke von 0 bis 1 ist in %d gleiche Teile geteilt. A ist beim %d. Strich: <b>%s</b>." % (n, z, fr(z, n)))


def sache():
    kind = R.choice(["anteil", "anteil", "rest", "pizza"])
    if kind == "anteil":
        tot = R.choice([20, 24, 25, 28, 30, 32])
        part = R.randint(2, tot - 2)
        g = gcd(part, tot)
        what = R.choice(["spielen Fußball", "haben ein Haustier", "fahren mit dem Rad zur Schule", "lesen gern Comics"])
        if g == 1:
            return None
        return mcq("In einer Klasse sind %d Kinder. %d davon %s. Welcher Anteil ist das (vollständig gekürzt)?" % (tot, part, what), fr(part // g, tot // g),
                   [fr(part, tot), fr(tot // g, part // g) if part // g > 1 else fr(part // g + 1, tot // g), fr(part, tot + part), fr((tot - part) // g, tot // g)],
                   "Anteil = Teil : Ganzes = %s = <b>%s</b>." % (fr(part, tot), fr(part // g, tot // g)))
    if kind == "rest":
        n = R.choice([3, 4, 5, 6, 8])
        z = R.randint(1, n - 1)
        tot = n * R.randint(4, 20)
        r = tot - tot // n * z
        return mcq("Eine Familie hat %d € Urlaubsgeld. %s davon gibt sie für die Unterkunft aus. Wie viel Geld bleibt übrig?" % (tot * 10, fr(z, n)), "%s €" % num(r * 10),
                   ["%s €" % num(x * 10) for x in (tot // n * z, tot // n, tot - z)], "%s von %s € = %s €. %s − %s = <b>%s €</b>." % (fr(z, n), num(tot * 10), num(tot // n * z * 10), num(tot * 10), num(tot // n * z * 10), num(r * 10)))
    n = R.choice([6, 8, 12])
    a, b = R.randint(1, n // 2), R.randint(1, n // 2 - 1)
    r = n - a - b
    if r <= 0:
        return None
    return mcq("Eine Pizza ist in %d gleich große Stücke geteilt. Mia isst %d Stück%s, Ben isst %d Stück%s. Welcher Anteil der Pizza bleibt übrig?" % (n, a, "" if a == 1 else "e", b, "" if b == 1 else "e"),
               fr(r, n), [fr(a + b, n), fr(r + 1, n), fr(r - 1, n) if r > 1 else fr(r + 2, n), fr(a, n), fr(b, n)],
               "%d − %d − %d = %d Stücke bleiben: <b>%s</b>." % (n, a, b, r, fr(r, n)))


def main():
    seen = set()
    sets = [
        ("Bruchteile ablesen", mix(R, seen, [(ablesen, 20)])),
        ("Bruchteile von Größen und Mengen", mix(R, seen, [(von, 20)])),
        ("Erweitern und kürzen", mix(R, seen, [(erweitern, 20)])),
        ("Vergleichen und Zahlenstrahl", mix(R, seen, [(vergleich, 20)])),
        ("Anteile in Sachaufgaben", mix(R, seen, [(sache, 20)])),
    ]
    body = lesson(
        ["Ein <b>Bruch</b> beschreibt einen Anteil: Der <b>Nenner</b> (unten) sagt, in wie viele gleich große Teile das Ganze geteilt ist, der <b>Zähler</b> (oben), wie viele Teile gemeint sind.",
         "%s von 20 € berechnest du so: 20 € : 4 = 5 €, dann 5 € %s 3 = 15 €." % (fr(3, 4), MAL),
         "<b>Erweitern</b>: Zähler und Nenner mit derselben Zahl multiplizieren. <b>Kürzen</b>: durch dieselbe Zahl dividieren. Der Wert bleibt gleich.",
         "Bei gleichem Nenner ist der Bruch mit dem größeren Zähler größer."],
        [example("%s von 24 Kindern" % fr(2, 3), ["24 : 3 = 8", "8 %s 2 = 16" % MAL], "16 Kinder"),
         example("%s kürzen" % fr(12, 18), ["durch 6 teilen"], fr(2, 3))],
        [["Zähler und Nenner vertauschen", "Nenner = Anzahl aller Teile"],
         ["Nur den Zähler erweitern", "Zähler und Nenner mit derselben Zahl"],
         ["%s ist größer als %s, weil 8 &gt; 4" % (fr(1, 8), fr(1, 4)), "Mehr Teile bedeuten kleinere Teile"]])
    faq = [
        {"q": "Was ist der Unterschied zwischen Zähler und Nenner?", "a": "Der Nenner steht unten und nennt die Anzahl der gleich großen Teile. Der Zähler steht oben und zählt, wie viele Teile gemeint sind."},
        {"q": "Warum ändert sich der Wert beim Kürzen nicht?", "a": "Man teilt die Teile nur gröber oder feiner ein. 2/4 einer Pizza ist genauso viel wie 1/2."},
        {"q": "Wie berechnet man einen Bruchteil von einer Größe?", "a": "Erst durch den Nenner teilen, dann mit dem Zähler multiplizieren: 3/4 von 60 min = 60 : 4 · 3 = 45 min."},
        {"q": "Lernt man Brüche in Klasse 5 oder 6?", "a": "Die Einführung mit Anteilen findet oft in Klasse 5 statt, das Rechnen mit Brüchen meist in Klasse 6."},
    ]
    make_unit(R, "brueche-und-anteile", "Z",
              "Die Schülerinnen und Schüler beschreiben Anteile mit Brüchen, bestimmen Bruchteile von Größen und Mengen, erweitern und kürzen Brüche, vergleichen sie und stellen sie am Zahlenstrahl dar (Zusammenfassung).",
              "Brüche und Anteile",
              "Brüche und Anteile Klasse 5 – Arbeitsblätter mit Lösungen",
              "Brüche und Anteile",
              "Brüche und Anteile für Klasse 5: Bruchteile ablesen, Bruchteile von Größen, erweitern und kürzen, vergleichen, Zahlenstrahl und Sachaufgaben. 100 Übungsaufgaben mit Lösungen, kostenlos.",
              "Nenner: in wie viele Teile. Zähler: wie viele Teile.",
              "Erweitern und Kürzen ändern den Wert nicht.",
              body, faq, sets, 9, grade="klasse-5")


if __name__ == "__main__":
    main()
