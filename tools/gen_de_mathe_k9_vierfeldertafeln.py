# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 9: Vierfeldertafeln und bedingte Wahrscheinlichkeit（Leitidee Daten und Zufall, Sek I）
  python3 tools/gen_de_mathe_k9_vierfeldertafeln.py
Vierfeldertafeln mit absoluten Häufigkeiten ergänzen, relative Häufigkeiten und Wahrscheinlichkeiten ablesen (P(A ∩ B), P(A)),
Tafeln aus Texten aufstellen, Anteile innerhalb einer Gruppe (bedingte Wahrscheinlichkeit P<sub>A</sub>(B)), Sachaufgaben.
Fehler: Zeilen- und Spaltensummen verwechselt, P<sub>A</sub>(B) durch die Gesamtzahl statt durch die Gruppe geteilt, P(A ∩ B) mit P(A) verwechselt.
"""
import random
from fractions import Fraction as Fr
from de_common import lesson, example, make_unit, mix, table
from de_k6 import bh, dz, endlich
from de_k9 import mcq

R = random.Random(49914)
G = ":"
NOT = "<span class='ov'>%s</span>"

THEMEN = [
    ("Mädchen", "Jungen", "fahren mit dem Rad", "fahren nicht mit dem Rad", "Schülerinnen und Schüler", "M", "R", "mit dem Rad fährt"),
    ("Klasse 9a", "Klasse 9b", "haben ein Haustier", "haben kein Haustier", "Jugendliche", "A", "H", "ein Haustier hat"),
    ("Erwachsene", "Kinder", "tragen eine Brille", "tragen keine Brille", "Personen", "E", "B", "eine Brille trägt"),
    ("Mädchen", "Jungen", "spielen in einem Verein", "spielen in keinem Verein", "Jugendliche", "M", "V", "in einem Verein spielt"),
    ("Frühstück zu Hause", "kein Frühstück zu Hause", "sind morgens müde", "sind morgens nicht müde", "Schülerinnen und Schüler", "F", "Ü", "morgens müde ist"),
]


def zahlen():
    a, b = R.randint(5, 60), R.randint(5, 60)
    c, d = R.randint(5, 60), R.randint(5, 60)
    return a, b, c, d


def tafel(t, a, b, c, d, hide=()):
    g1, g2, m1, m2 = t[0], t[1], t[2], t[3]
    cells = {"a": a, "b": b, "c": c, "d": d, "r1": a + b, "r2": c + d, "s1": a + c, "s2": b + d, "n": a + b + c + d}
    f = lambda k: "?" if k in hide else ("" if k in hide else str(cells[k]))
    return table(["", m1[0].upper() + m1[1:], m2[0].upper() + m2[1:], "Summe"],
                 [[g1, f("a"), f("b"), f("r1")], [g2, f("c"), f("d"), f("r2")], ["Summe", f("s1"), f("s2"), f("n")]])


def ergaenzen():
    t = R.choice(THEMEN)
    a, b, c, d = zahlen()
    cells = {"a": a, "b": b, "c": c, "d": d, "r1": a + b, "r2": c + d, "s1": a + c, "s2": b + d, "n": a + b + c + d}
    target = R.choice(["a", "b", "c", "d", "r2", "s2", "n"])
    # wir zeigen genug Werte, damit das Feld eindeutig ist
    hide = {target}
    pic = tafel(t, a, b, c, d, hide)
    v = cells[target]
    why = {"a": "Zeilensumme minus Nachbarfeld: %d − %d" % (a + b, b), "b": "%d − %d" % (a + b, a), "c": "%d − %d" % (c + d, d), "d": "%d − %d" % (c + d, c),
           "r2": "%d + %d" % (c, d), "s2": "%d + %d" % (b, d), "n": "%d + %d" % (a + b, c + d)}[target]
    return mcq(pic + "Welche Zahl gehört in das Feld mit dem Fragezeichen?", str(v), [str(v + 10), str(v - 10) if v > 10 else str(v + 20), str(cells["n"] - v) if cells["n"] - v != v else str(v + 5)],
               "%s = <b>%d</b>." % (why, v))


def relativ():
    t = R.choice(THEMEN)
    a, b, c, d = zahlen()
    n = a + b + c + d
    pic = tafel(t, a, b, c, d)
    kind = R.choice(["und", "und", "eins", "nicht"])
    if kind == "und":
        v = Fr(a, n)
        return mcq(pic + "Eine Person wird zufällig ausgewählt. Wie groß ist die Wahrscheinlichkeit, dass sie zur Gruppe „%s“ gehört <b>und</b> %s?" % (t[0], t[7]), bh(v),
                   [bh(Fr(a + b, n)), bh(Fr(a, a + b)), bh(Fr(a + c, n)) if a + c != a + b else bh(Fr(b, n))],
                   "Inneres Feld %d von %d: P = %d %s %d = <b>%s</b>." % (a, n, a, G, n, bh(v)))
    if kind == "eins":
        v = Fr(a + c, n)
        return mcq(pic + "Eine Person wird zufällig ausgewählt. Wie groß ist die Wahrscheinlichkeit, dass sie %s?" % t[7], bh(v), [bh(Fr(a, n)), bh(Fr(a + b, n)) if a + b != a + c else bh(Fr(b + d, n)), bh(Fr(a + c, a + b)) if Fr(a + c, a + b) <= 1 and Fr(a + c, a + b) != v else bh(Fr(c, n))],
                   "Spaltensumme %d von %d: <b>%s</b>." % (a + c, n, bh(v)))
    v = Fr(c + d, n)
    return mcq(pic + "Wie groß ist die Wahrscheinlichkeit, dass eine zufällig ausgewählte Person zur Gruppe „%s“ gehört?" % t[1], bh(v), [bh(Fr(a + b, n)) if a + b != c + d else bh(Fr(c, n)), bh(Fr(c, n)), bh(Fr(c + d, a + b)) if Fr(c + d, a + b) <= 1 and c + d != a + b else bh(Fr(d, n))],
               "Zeilensumme %d von %d: <b>%s</b>." % (c + d, n, bh(v)))


def aufstellen():
    n = R.choice([100, 200, 400, 500])
    pa = R.choice([40, 45, 50, 55, 60])
    pab = R.choice([10, 15, 20, 25, 30])
    pb = R.choice([30, 35, 40, 50])
    if pab >= min(pa, pb) or pa + pb - pab > 100:
        return None
    a = n * pab // 100
    ra = n * pa // 100
    sb = n * pb // 100
    kind = R.choice(["b", "c", "d"])
    vals = {"b": ra - a, "c": sb - a, "d": n - ra - sb + a}
    names = {"b": "Mädchen, die nicht im Chor sind", "c": "Jungen, die im Chor sind", "d": "Jungen, die nicht im Chor sind"}
    v = vals[kind]
    return mcq("An einer Schule mit %d Jugendlichen sind %d %% Mädchen. %d %% aller Jugendlichen singen im Chor, %d %% aller Jugendlichen sind Mädchen im Chor. Wie viele sind %s?" % (n, pa, pb, pab, names[kind]), str(v),
               [str(vals[k]) for k in vals if k != kind] + [str(a)],
               "Mädchen: %d, Chor: %d, Mädchen im Chor: %d. Vierfeldertafel ergänzen: <b>%d</b>." % (ra, sb, a, v))


def bedingt():
    t = R.choice(THEMEN)
    a, b, c, d = zahlen()
    n = a + b + c + d
    pic = tafel(t, a, b, c, d)
    kind = R.choice(["zeile", "zeile", "spalte"])
    if kind == "zeile":
        v = Fr(a, a + b)
        return mcq(pic + "Man wählt zufällig eine Person aus der Gruppe „%s“. Wie groß ist die Wahrscheinlichkeit, dass sie %s?" % (t[0], t[7]), bh(v),
                   [bh(Fr(a, n)), bh(Fr(a, a + c)) if Fr(a, a + c) != v else bh(Fr(b, a + b)), bh(Fr(a + c, n)) if Fr(a + c, n) != v else bh(Fr(c, c + d))],
                   "Nur die Gruppe „%s“ zählt (%d Personen), davon %d: P = %d %s %d = <b>%s</b>. Das ist eine bedingte Wahrscheinlichkeit." % (t[0], a + b, a, a, G, a + b, bh(v)))
    v = Fr(c, a + c)
    return mcq(pic + "Man wählt zufällig eine Person aus, die %s. Wie groß ist die Wahrscheinlichkeit, dass sie zur Gruppe „%s“ gehört?" % (t[7], t[1]), bh(v),
               [bh(Fr(c, n)), bh(Fr(c, c + d)) if Fr(c, c + d) != v else bh(Fr(a, a + c)), bh(Fr(a, a + c)) if Fr(a, a + c) != v else bh(Fr(d, n))],
               "Nur die %d Personen, die %s, zählen; davon gehören %d zu „%s“: <b>%s</b>." % (a + c, t[7], c, t[1], bh(v)))


def sache():
    kind = R.choice(["test", "test", "umfrage", "vergleich"])
    if kind == "test":
        n = 1000
        krank = R.choice([10, 20, 50])
        sens = R.choice([90, 95, 99])
        fp = R.choice([5, 10])
        tp = krank * sens // 100
        fpos = (n - krank) * fp // 100
        pos = tp + fpos
        v = Fr(tp, pos)
        return mcq("Von %d Personen haben %d eine Krankheit. Ein Test erkennt %d %% der Kranken. Bei Gesunden zeigt er in %d %% der Fälle fälschlich „positiv“. Eine Person ist positiv getestet. Wie groß ist die Wahrscheinlichkeit, dass sie wirklich krank ist (auf ganze Prozent)?" % (n, krank, sens, fp, ),
                   "etwa %d %%" % round(float(v) * 100), ["%d %%" % sens, "etwa %d %%" % round(tp / n * 100) if round(tp / n * 100) != round(float(v) * 100) else "etwa 50 %", "%d %%" % (100 - fp)],
                   "Positiv: %d Kranke + %d Gesunde = %d. Davon krank: %d %s %d ≈ <b>%d %%</b>. Viel weniger als %d %%!" % (tp, fpos, pos, tp, G, pos, round(float(v) * 100), sens))
    if kind == "umfrage":
        a, b, c, d = zahlen()
        v1, v2 = Fr(a, a + b), Fr(c, c + d)
        if v1 == v2:
            return None
        g = "Mädchen" if v1 > v2 else "Jungen"
        pic = tafel(THEMEN[3], a, b, c, d)
        return mcq(pic + "Spielen anteilig mehr Mädchen oder mehr Jungen in einem Verein?", "anteilig mehr %s" % g,
                   ["anteilig mehr %s" % ("Jungen" if g == "Mädchen" else "Mädchen"), "Beide gleich viele.", "Das kann man nicht sagen."],
                   "Mädchen: %d %s %d ≈ %s %%, Jungen: %d %s %d ≈ %s %%. <b>Mehr %s</b>." % (a, G, a + b, round(float(v1) * 100), c, G, c + d, round(float(v2) * 100), g))
    q, a, w = R.choice([
        ("Was steht im Feld unten rechts einer Vierfeldertafel?", "die Gesamtzahl", ["die kleinste Zahl", "die Zahl der Personen mit beiden Merkmalen", "die Differenz der Zeilen"]),
        ("Was bedeutet P(A ∩ B)?", "die Wahrscheinlichkeit, dass A und B gleichzeitig eintreten", ["die Wahrscheinlichkeit für A oder B", "die Wahrscheinlichkeit für B, wenn A eingetreten ist", "die Wahrscheinlichkeit für A ohne B"]),
        ("Was bedeutet P<sub>A</sub>(B)?", "die Wahrscheinlichkeit für B, wenn man nur die Fälle mit A betrachtet", ["die Wahrscheinlichkeit, dass A und B eintreten", "die Wahrscheinlichkeit für A", "die Summe aus P(A) und P(B)"]),
        ("Wie viele Felder einer Vierfeldertafel muss man mindestens kennen, um alle zu berechnen?", "drei geeignete Felder (z. B. zwei innere und eine Summe)", ["ein Feld", "alle neun", "nur die Gesamtzahl"]),
    ])
    return mcq(q, a, w, "<b>%s</b>" % a)


def main():
    seen = set()
    sets = [
        ("Vierfeldertafeln ergänzen", mix(R, seen, [(ergaenzen, 20)])),
        ("Wahrscheinlichkeiten ablesen", mix(R, seen, [(relativ, 20)])),
        ("Tafeln aus Texten", mix(R, seen, [(aufstellen, 20)])),
        ("Bedingte Wahrscheinlichkeit", mix(R, seen, [(bedingt, 20)])),
        ("Sachaufgaben", mix(R, seen, [(sache, 20)])),
    ]
    body = lesson(
        ["Eine <b>Vierfeldertafel</b> ordnet Daten nach zwei Merkmalen mit je zwei Ausprägungen (A oder nicht A, B oder nicht B). Zeilen und Spalten werden aufsummiert.",
         "Fehlende Felder findet man über die Summen: Jede Zeile und jede Spalte muss aufgehen.",
         "P(A ∩ B) = Anzahl im inneren Feld %s Gesamtzahl. P(A) = Zeilensumme %s Gesamtzahl." % (G, G),
         "<b>Bedingte Wahrscheinlichkeit</b> P<sub>A</sub>(B): Man betrachtet nur die Gruppe A und teilt durch ihre Größe."],
        [example("12 von 30 Mädchen fahren Rad", ["Gruppe Mädchen: 30"], "P<sub>Mädchen</sub>(Rad) = 12/30 = 0,4"),
         example("Zeile 25 + ? = 40", ["40 − 25"], "15")],
        [["P<sub>A</sub>(B) = Feld : Gesamtzahl", "Durch die Gruppengröße teilen"],
         ["Zeilen- und Spaltensumme vertauscht", "Zeile = Gruppe, Spalte = Merkmal"],
         ["„A und B“ = P(A)", "Nur das innere Feld zählt"]])
    faq = [
        {"q": "Was ist eine Vierfeldertafel?", "a": "Eine Tabelle mit zwei Merkmalen und vier inneren Feldern. Mit den Summen kann man fehlende Werte berechnen."},
        {"q": "Was ist eine bedingte Wahrscheinlichkeit?", "a": "Die Wahrscheinlichkeit für ein Ereignis B, wenn man nur Fälle betrachtet, in denen A eingetreten ist. Man teilt durch die Größe der Gruppe A."},
        {"q": "Wie ergänze ich eine Vierfeldertafel?", "a": "Nutze, dass sich jede Zeile und jede Spalte zur Summe addiert. Mit drei passenden Werten lässt sich alles berechnen."},
        {"q": "Warum ist ein positiver Test nicht sicher?", "a": "Wenn eine Krankheit selten ist, gibt es viele falsch positive Ergebnisse bei Gesunden. Die Vierfeldertafel zeigt das deutlich."},
    ]
    make_unit(R, "vierfeldertafeln", "D",
              "Die Schülerinnen und Schüler stellen Daten in Vierfeldertafeln dar, ergänzen fehlende Werte, bestimmen relative Häufigkeiten und Wahrscheinlichkeiten und berechnen bedingte Wahrscheinlichkeiten in Sachsituationen (Zusammenfassung).",
              "Vierfeldertafeln und bedingte Wahrscheinlichkeit",
              "Vierfeldertafel Klasse 9 – bedingte Wahrscheinlichkeit, Arbeitsblätter mit Lösungen",
              "Vierfeldertafeln",
              "Vierfeldertafeln für Klasse 9: Tafeln ergänzen, Wahrscheinlichkeiten ablesen, Tafeln aus Texten aufstellen, bedingte Wahrscheinlichkeit und Sachaufgaben. 100 Aufgaben mit Lösungen, kostenlos.",
              "Bedingt: nur durch die Gruppe teilen.",
              "Zeilen und Spalten müssen aufgehen.",
              body, faq, sets, 14, grade="klasse-9")


if __name__ == "__main__":
    main()
