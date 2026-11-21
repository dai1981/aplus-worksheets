# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 6: Daten und Wahrscheinlichkeit（Leitidee Daten und Zufall, Sek I）
  python3 tools/gen_de_mathe_k6_daten_und_wahrscheinlichkeit.py
Absolute und relative Häufigkeit (Bruch, Dezimalzahl, Prozent), Mittelwert mit Dezimalzahlen, Median bei gerader Anzahl, Wahrscheinlichkeiten bei Würfel, Glücksrad und Urne (Laplace), sicher – möglich – unmöglich.
Fehler: relative Häufigkeit mit absoluter verwechselt, Wahrscheinlichkeit als „günstige : ungünstige“, Median ohne Sortieren.
"""
import random
from fractions import Fraction as Fr
from de_common import lesson, example, make_unit, mix, Kids, fr, MAL, table
from de_k6 import bh, dz, endlich, mcq

R = random.Random(49618)
KIDS = Kids(R)
G = ":"
P = " %"


def relativ():
    n = R.choice([20, 25, 40, 50])
    a = R.randint(2, n - 2)
    kind = R.choice(["bruch", "dez", "proz"])
    ctx = R.choice(["Bei %d Würfen mit einer Münze kam %d-mal Kopf." % (n, a), "Von %d befragten Kindern mögen %d am liebsten Mathe." % (n, a), "Bei %d Freiwürfen gab es %d Treffer." % (n, a)])
    v = Fr(a, n)
    if kind == "bruch":
        return mcq(ctx + " Wie groß ist die relative Häufigkeit als gekürzter Bruch?", bh(v), [str(a), fr(n, a) if a > 1 else fr(n, 2), fr(a, n - a), bh(1 - v)],
                   "Relative Häufigkeit = absolute Häufigkeit %s Gesamtzahl = %s = <b>%s</b>." % (G, fr(a, n), bh(v)))
    if kind == "dez":
        return mcq(ctx + " Wie groß ist die relative Häufigkeit als Dezimalzahl?", dz(v), [str(a), dz(1 - v), dz(v * 10) if v * 10 < 10 else dz(v / 10)],
                   "%d %s %d = <b>%s</b>." % (a, G, n, dz(v)))
    return mcq(ctx + " Wie groß ist die relative Häufigkeit in Prozent?", dz(v * 100) + P, ["%d%s" % (a, P), dz((1 - v) * 100) + P, dz(v * 10) + P],
               "%s = %s = <b>%s%s</b>." % (fr(a, n), dz(v), dz(v * 100), P))


def mittel():
    n = R.choice([4, 5, 6])
    ctx, lo, hi = R.choice([("Weitsprung in m", 250, 480), ("Tageshöchsttemperatur in °C", 120, 290), ("Niederschlag in mm", 5, 95), ("Gewicht von Kürbissen in kg", 15, 80)])
    f = 100 if ctx.startswith("Weit") else 10
    data = [Fr(R.randint(lo, hi), f) for _ in range(n)]
    if len(set(data)) < n:
        return None
    s = sum(data)
    m = s / n
    if not endlich(m) or len(dz(m).split(",")[-1]) > 3:
        return None
    return mcq("%s: %s. Berechne den Mittelwert." % (ctx, "; ".join(dz(x) for x in data)), dz(m), [dz(s), dz(sorted(data)[n // 2]) if sorted(data)[n // 2] != m else dz(m + Fr(1, 10)), dz(s / (n - 1)) if endlich(s / (n - 1)) else dz(m + Fr(2, 10))],
               "Summe: %s. %s %s %d = <b>%s</b>." % (dz(s), dz(s), G, n, dz(m)))


def median():
    n = R.choice([6, 8, 5, 7])
    data = R.sample(range(2, 40), n)
    srt = sorted(data)
    if n % 2:
        med = Fr(srt[n // 2])
        e = "Sortiert: %s. Der mittlere Wert: <b>%s</b>." % (", ".join(map(str, srt)), dz(med))
    else:
        a, b = srt[n // 2 - 1], srt[n // 2]
        med = Fr(a + b, 2)
        e = "Sortiert: %s. Mittelwert der beiden mittleren Werte: (%d + %d) %s 2 = <b>%s</b>." % (", ".join(map(str, srt)), a, b, G, dz(med))
    wrong = [dz(Fr(data[n // 2])) if Fr(data[n // 2]) != med else None, dz(Fr(srt[n // 2])) if Fr(srt[n // 2]) != med else dz(Fr(srt[n // 2 - 1])), dz(Fr(sum(data), n)) if endlich(Fr(sum(data), n)) and Fr(sum(data), n) != med else dz(med + 1), dz(Fr(srt[-1] - srt[0]))]
    return mcq("Bestimme den Median: %s" % ", ".join(map(str, data)), dz(med), wrong, e)


def wuerfel():
    k = R.randrange(10)
    D = [("eine 6", 1), ("eine gerade Zahl", 3), ("eine Zahl größer als 4", 2), ("eine Primzahl (2, 3 oder 5)", 3), ("höchstens eine 2", 2), ("keine 1", 5), ("eine Zahl kleiner als 7", 6), ("eine 7", 0), ("eine durch 3 teilbare Zahl", 2), ("mindestens eine 3", 4)]
    ev, g = D[k]
    v = Fr(g, 6)
    ans = bh(v) if g not in (0, 6) else ("0 (unmöglich)" if g == 0 else "1 (sicher)")
    w = [fr(g, 6 - g) if 0 < g < 6 else "1 (sicher)" if g == 0 else "0 (unmöglich)", fr(1, 6) if g != 1 else fr(1, 3), fr(g, 10) if g else fr(1, 2), bh(1 - v) if 0 < g < 6 and 1 - v != v else fr(5, 6) if g != 5 else fr(1, 2)]
    return mcq("Ein fairer Würfel wird einmal geworfen. Wie groß ist die Wahrscheinlichkeit für %s?" % ev, ans, w,
               "%d günstige von 6 möglichen Ergebnissen: %s = <b>%s</b>." % (g, fr(g, 6), ans))


def urne():
    r, b, g = R.randint(1, 8), R.randint(1, 8), R.randint(0, 6)
    t = r + b + g
    farbe, n = R.choice([("rote", r), ("blaue", b)] + ([("grüne", g)] if g else []))
    v = Fr(n, t)
    ks = "%d rote, %d blaue%s" % (r, b, (" und %d grüne" % g) if g else "")
    kind = R.choice(["eine", "nicht"])
    if kind == "eine":
        return mcq("In einer Dose liegen %s Kugeln. Eine Kugel wird blind gezogen. Wie groß ist die Wahrscheinlichkeit für eine %s Kugel?" % (ks, farbe.rstrip("e") + "e"), bh(v),
                   [fr(n, t - n) if t - n else None, fr(1, t), fr(n, 10) if n < 10 and Fr(n, 10) != v else fr(n, t + 1), bh(1 - v) if 1 - v != v else None],
                   "%d %s von %d Kugeln: %s = <b>%s</b>." % (n, farbe, t, fr(n, t), bh(v)))
    return mcq("In einer Dose liegen %s Kugeln. Wie groß ist die Wahrscheinlichkeit, <b>keine</b> %s Kugel zu ziehen?" % (ks, farbe), bh(1 - v), [bh(v), fr(t - n, n), fr(t - n, t + n)],
               "%d Kugeln sind nicht %s: %s = <b>%s</b>." % (t - n, farbe.rstrip("e"), fr(t - n, t), bh(1 - v)))


def rad():
    n = R.choice([4, 5, 6, 8, 10, 12])
    k = R.randint(1, n - 1)
    farbe = R.choice(["rot", "gelb", "blau", "grün"])
    v = Fr(k, n)
    davon = ("davon ist eines %s" % farbe) if k == 1 else ("davon sind %d %s" % (k, farbe))
    return mcq("Ein Glücksrad hat %d gleich große Felder, %s. Wie groß ist die Wahrscheinlichkeit, dass der Zeiger auf %s stehen bleibt?" % (n, davon, farbe), bh(v),
               [fr(k, n - k) if k != n - k else fr(1, n), fr(1, k) if k > 1 else fr(1, n + 1), bh(1 - v) if 1 - v != v else fr(k + 1, n), dz(Fr(k, 10)) if k < 10 else None],
               "%d günstige%s von %d gleich wahrscheinlichen Feldern: <b>%s</b>." % (k, "s Feld" if k == 1 else "", n, bh(v)))


def begriff():
    k = R.randrange(10)
    D = [("Mit einem normalen Würfel eine 0 werfen ist …", "unmöglich", ["sicher", "möglich", "sehr wahrscheinlich"]),
         ("Mit einem normalen Würfel eine Zahl von 1 bis 6 werfen ist …", "sicher", ["unmöglich", "unwahrscheinlich", "möglich, aber selten"]),
         ("Mit einer Münze Kopf werfen ist …", "möglich (Wahrscheinlichkeit 1/2)", ["sicher", "unmöglich", "möglich (Wahrscheinlichkeit 1/3)"]),
         ("Welchen Wert hat die Wahrscheinlichkeit eines sicheren Ereignisses?", "1", ["0", "100", "10"]),
         ("Welchen Wert hat die Wahrscheinlichkeit eines unmöglichen Ereignisses?", "0", ["1", "−1", "100"]),
         ("Zwischen welchen Zahlen liegt jede Wahrscheinlichkeit?", "zwischen 0 und 1", ["zwischen 1 und 6", "zwischen 0 und 10", "zwischen −1 und 1"]),
         ("Eine Münze zeigte 7-mal hintereinander Kopf. Wie groß ist die Wahrscheinlichkeit für Kopf beim nächsten Wurf?", fr(1, 2), [fr(1, 8), fr(1, 7), "fast 0"]),
         ("Je öfter man ein Zufallsexperiment wiederholt, desto mehr nähert sich die relative Häufigkeit …", "der Wahrscheinlichkeit", ["der Zahl 0", "der absoluten Häufigkeit", "der Zahl 100"]),
         ("Was bedeutet „Laplace-Experiment“?", "Alle Ergebnisse sind gleich wahrscheinlich.", ["Es gibt nur zwei Ergebnisse.", "Ein Ergebnis ist sicher.", "Man würfelt immer zweimal."]),
         ("Wie viele mögliche Ergebnisse hat das Werfen eines normalen Würfels?", "6", ["1", "12", "36"])]
    q, a, w = D[k]
    return mcq(q, a, w, "<b>%s</b>." % a)


def main():
    seen = set()
    sets = [
        ("Relative Häufigkeit", mix(R, seen, [(relativ, 20)])),
        ("Mittelwert und Median", mix(R, seen, [(mittel, 10), (median, 10)])),
        ("Würfel und Glücksrad", mix(R, seen, [(wuerfel, 10), (rad, 10)])),
        ("Ziehen aus einer Dose", mix(R, seen, [(urne, 20)])),
        ("Gemischte Aufgaben", mix(R, seen, [(begriff, 10), (median, 5), (relativ, 5)])),
    ]
    body = lesson(
        ["<b>Absolute Häufigkeit</b>: wie oft etwas vorkommt. <b>Relative Häufigkeit</b>: absolute Häufigkeit %s Gesamtzahl (als Bruch, Dezimalzahl oder Prozent)." % G,
         "<b>Mittelwert</b> = Summe aller Werte %s Anzahl. <b>Median</b>: Werte ordnen, der mittlere Wert (bei gerader Anzahl der Mittelwert der beiden mittleren)." % G,
         "Sind alle Ergebnisse gleich wahrscheinlich, gilt: <b>Wahrscheinlichkeit = Anzahl günstiger Ergebnisse %s Anzahl aller Ergebnisse</b>." % G,
         "Wahrscheinlichkeiten liegen zwischen 0 (unmöglich) und 1 (sicher)."],
        [example("Würfel: Zahl größer als 4", ["günstig: 5 und 6", "2 von 6"], fr(1, 3)),
         example("Median von 3, 9, 4, 7", ["sortiert: 3, 4, 7, 9", "(4 + 7) %s 2" % G], "5,5")],
        [["12 von 40 Würfen: relative Häufigkeit 12", "%s = 0,3 = 30%s" % (fr(12, 40), P)],
         ["3 rote, 5 blaue: P(rot) = %s" % fr(3, 5), "Durch alle Kugeln teilen: %s" % fr(3, 8)],
         ["Median von 9, 3, 7: 3", "Erst ordnen: 3, 7, 9. Median 7"]])
    faq = [
        {"q": "Was ist die relative Häufigkeit?", "a": "Der Anteil eines Ergebnisses an allen Versuchen: absolute Häufigkeit geteilt durch die Gesamtzahl."},
        {"q": "Wie berechne ich eine Wahrscheinlichkeit?", "a": "Bei gleich wahrscheinlichen Ergebnissen: günstige Ergebnisse geteilt durch alle möglichen Ergebnisse."},
        {"q": "Wie bestimmt man den Median bei einer geraden Anzahl?", "a": "Werte ordnen und den Mittelwert der beiden mittleren Werte nehmen."},
        {"q": "Kann eine Wahrscheinlichkeit größer als 1 sein?", "a": "Nein. 0 bedeutet unmöglich, 1 bedeutet sicher."},
    ]
    make_unit(R, "daten-und-wahrscheinlichkeit", "D",
              "Die Schülerinnen und Schüler bestimmen absolute und relative Häufigkeiten, Mittelwert und Median und berechnen Wahrscheinlichkeiten bei Laplace-Experimenten (Zusammenfassung).",
              "Daten und Wahrscheinlichkeit",
              "Wahrscheinlichkeit und relative Häufigkeit Klasse 6 – Arbeitsblätter",
              "Daten & Wahrscheinlichkeit",
              "Daten und Zufall für Klasse 6: relative Häufigkeit, Mittelwert, Median, Würfel, Glücksrad und Ziehen aus einer Dose. 100 Aufgaben mit Lösungen, kostenlos.",
              "Wahrscheinlichkeit = günstige : alle Ergebnisse.",
              "Relative Häufigkeit = absolute Häufigkeit : Gesamtzahl.",
              body, faq, sets, 18, grade="klasse-6")


if __name__ == "__main__":
    main()
