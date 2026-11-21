# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 7: Rechnen mit rationalen Zahlen（Leitidee Zahl und Operation, Sek I）
  python3 tools/gen_de_mathe_k7_rechnen_mit_rationalen_zahlen.py
Addieren und subtrahieren (Dezimalzahlen und Brüche mit Vorzeichen), multiplizieren und dividieren, Vorzeichenregeln bei mehreren Faktoren, Rechengesetze und Klammern, Sachaufgaben.
Fehler: − (−a) als −a, Vorzeichen beim Produkt falsch (gerade Anzahl Minus = Plus), Hauptnenner mit Vorzeichen vergessen.
"""
import random
from fractions import Fraction as Fr
from de_common import lesson, example, make_unit, mix, Kids, fr, MAL, table
from de_k6 import bh, dz
from de_k7 import mcq, eur

R = random.Random(49702)
KIDS = Kids(R)
G = ":"


def k(v, f):
    """Zahl in Klammern, wenn negativ; f = Formatfunktion"""
    return "(%s)" % f(v) if v < 0 else f(v)


def dez(lo=-99, hi=99, d=10):
    v = Fr(R.randint(lo, hi), d)
    return v if v else None


def bru():
    n = R.choice([2, 3, 4, 5, 6, 8])
    z = R.randint(1, n - 1)
    v = Fr(R.choice([-1, 1]) * z, n)
    return v if v.denominator == n else None


def addsub_dez():
    a, b = dez(), dez()
    if a is None or b is None:
        return None
    op = R.choice(["+", "−"])
    v = a + b if op == "+" else a - b
    w = a - b if op == "+" else a + b
    return mcq("%s %s %s = ?" % (dz(a), op, k(b, dz)), dz(v), [dz(w), dz(-v) if v else "1", dz(abs(a) + abs(b)) if abs(a) + abs(b) != abs(v) else dz(v + 1)],
               "%s%s %s %s = <b>%s</b>." % (("Minus eine negative Zahl ist Plus. " if op == "−" and b < 0 else "Plus eine negative Zahl ist Minus. " if op == "+" and b < 0 else ""), dz(a), op, k(b, dz), dz(v)))


def addsub_bru():
    a, b = bru(), bru()
    if a is None or b is None or a == b:
        return None
    op = R.choice(["+", "−"])
    v = a + b if op == "+" else a - b
    w = a - b if op == "+" else a + b
    return mcq("%s %s %s = ?" % (bh(a), op, k(b, bh)), bh(v, True), [bh(w, True), bh(-v, True) if v else "1", bh(Fr(a.numerator + (b.numerator if op == "+" else -b.numerator), a.denominator + b.denominator), True) if a.denominator + b.denominator else None],
               "Auf den Hauptnenner bringen, dann die Zähler mit Vorzeichen verrechnen: <b>%s</b>." % bh(v, True))


def maldurch():
    kind = R.choice(["mal", "mal", "durch", "bruch"])
    if kind == "bruch":
        a, b = bru(), bru()
        if a is None or b is None:
            return None
        if R.random() < 0.5:
            v = a * b
            return mcq("%s %s %s = ?" % (k(a, bh), MAL, k(b, bh)), bh(v), [bh(-v), bh(a + b, True), bh(Fr(a.numerator * b.denominator, a.denominator * b.numerator))],
                       "Zähler mal Zähler, Nenner mal Nenner, Vorzeichen: %s. <b>%s</b>" % ("gleich → Plus" if v > 0 else "verschieden → Minus", bh(v)))
        v = a / b
        return mcq("%s %s %s = ?" % (k(a, bh), G, k(b, bh)), bh(v, True), [bh(-v, True), bh(a * b), bh(b / a, True) if b / a != v else None],
                   "Mit dem Kehrwert multiplizieren. Vorzeichen: %s. <b>%s</b>" % ("gleich → Plus" if v > 0 else "verschieden → Minus", bh(v, True)))
    a, b = dez(-50, 50), Fr(R.choice([-1, 1]) * R.randint(2, 9))
    if a is None:
        return None
    if kind == "mal":
        v = a * b
        return mcq("%s %s %s = ?" % (k(a, dz), MAL, k(b, dz)), dz(v), [dz(-v), dz(a + b), dz(v * 10)], "%s %s %s ergibt %s: <b>%s</b>." % ("Minus" if a < 0 else "Plus", MAL, "Minus" if b < 0 else "Plus", "Plus" if v > 0 else "Minus", dz(v)))
    c = a * b
    return mcq("%s %s %s = ?" % (k(c, dz), G, k(b, dz)), dz(a), [dz(-a), dz(c / b / 10), dz(c - b)], "Gleiche Vorzeichen: Plus, verschiedene: Minus. <b>%s</b>" % dz(a))


def mehrere():
    fs = [R.choice([-1, 1]) * R.randint(1, 6) for _ in range(R.choice([3, 4]))]
    if 1 in fs or -1 in fs:
        return None
    v = 1
    for f in fs:
        v *= f
    m = sum(1 for f in fs if f < 0)
    return mcq("%s = ?" % (" %s " % MAL).join(k(f, dz) for f in fs), dz(v), [dz(-v), dz(sum(fs)), dz(abs(v) + 1) if v < 0 else dz(-v - 1)],
               "%d negative Faktoren: %s Anzahl, also %s. Betrag %d. <b>%s</b>" % (m, "gerade" if m % 2 == 0 else "ungerade", "Plus" if m % 2 == 0 else "Minus", abs(v), dz(v)))


def klammern():
    a, b, c = [Fr(R.choice([-1, 1]) * R.randint(1, 9)) for _ in range(3)]
    kind = R.choice(["punkt", "klammer", "vorteil"])
    if kind == "punkt":
        v = a + b * c
        return mcq("%s + %s %s %s = ?" % (dz(a), k(b, dz), MAL, k(c, dz)), dz(v), [dz((a + b) * c), dz(a - b * c), dz(-v) if v else "1"],
                   "Punkt vor Strich: %s %s %s = %s. %s + %s = <b>%s</b>." % (k(b, dz), MAL, k(c, dz), dz(b * c), dz(a), k(b * c, dz), dz(v)))
    if kind == "klammer":
        v = (a - b) * c
        return mcq("(%s − %s) %s %s = ?" % (dz(a), k(b, dz), MAL, k(c, dz)), dz(v), [dz((a + b) * c), dz(a - b * c), dz(-v) if v else "1"],
                   "Klammer zuerst: %s − %s = %s. %s %s %s = <b>%s</b>." % (dz(a), k(b, dz), dz(a - b), k(a - b, dz), MAL, k(c, dz), dz(v)))
    x = Fr(R.choice([-1, 1]) * R.choice([25, 4, 5, 20, 50, 8, 125]), R.choice([1, 10]))
    y = Fr(R.choice([-1, 1]) * R.randint(3, 19))
    z = {Fr(25): Fr(4), Fr(4): Fr(25), Fr(5): Fr(2), Fr(20): Fr(5), Fr(50): Fr(2), Fr(8): Fr(125), Fr(125): Fr(8)}.get(abs(x * (10 if x.denominator == 10 else 1)))
    if z is None:
        return None
    z = z * R.choice([-1, 1])
    v = x * y * z
    return mcq("Rechne geschickt: %s %s %s %s %s" % (k(x, dz), MAL, k(y, dz), MAL, k(z, dz)), dz(v), [dz(-v), dz(x * y + z), dz(v * 10)],
               "Vertauschen: %s %s %s = %s. Dann %s %s %s = <b>%s</b>." % (k(x, dz), MAL, k(z, dz), dz(x * z), dz(x * z), MAL, k(y, dz), dz(v)))


def sache():
    p, er = KIDS.next()
    kind = R.choice(["temp", "konto", "hoehe", "mittel", "aufzug"])
    if kind == "temp":
        t = Fr(R.randint(-60, 30), 10)
        d = Fr(R.randint(5, 25), 10)
        h = R.randint(3, 8)
        v = t - d * h
        return mcq("Um 18 Uhr sind es %s °C. Die Temperatur sinkt jede Stunde um %s °C. Wie warm ist es nach %d Stunden?" % (dz(t), dz(d), h), "%s °C" % dz(v), ["%s °C" % dz(x) for x in (t + d * h, t - d, -v if v else 1)],
                   "%s − %d %s %s = %s − %s = <b>%s °C</b>." % (dz(t), h, MAL, dz(d), dz(t), dz(d * h), dz(v)))
    if kind == "konto":
        s = Fr(R.randint(5000, 30000), 100)
        a = Fr(R.randint(100, 900), 10)
        n = R.randint(3, 6)
        v = s - a * n
        return mcq("%s hat %s auf dem Konto und bezahlt %d-mal %s per Lastschrift. Wie ist der Kontostand danach?" % (p, eur(s), n, eur(a)), eur(v), [eur(x) for x in (s + a * n, s - a, -v)],
                   "%s − %d %s %s = <b>%s</b>." % (eur(s), n, MAL, eur(a), eur(v)))
    if kind == "hoehe":
        a, b = R.randint(100, 3000), -R.randint(10, 400)
        return mcq("Der höchste Punkt einer Wanderung liegt auf %d m, der tiefste Punkt einer Höhle auf %s m (unter dem Meeresspiegel). Wie groß ist der Höhenunterschied?" % (a, dz(b)), "%s m" % dz(a - b), ["%s m" % dz(x) for x in (a + b, a, -(a - b))],
                   "%d − (%s) = %d + %d = <b>%s m</b>." % (a, dz(b), a, -b, dz(a - b)))
    if kind == "mittel":
        vals = [Fr(R.randint(-80, 40), 10) for _ in range(4)]
        m = sum(vals) / 4
        if (m * 100).denominator != 1:
            return None
        return mcq("Tiefsttemperaturen an vier Tagen: %s °C. Berechne den Mittelwert." % "; ".join(dz(v) for v in vals), "%s °C" % dz(m), ["%s °C" % dz(x) for x in (sum(abs(v) for v in vals) / 4, -m if m else 1, sum(vals))],
                   "Summe: %s. %s : 4 = <b>%s °C</b>." % (dz(sum(vals)), dz(sum(vals)), dz(m)))
    s, u, o = R.randint(-3, 2), R.randint(2, 6), R.randint(1, 8)
    v = s - u + o
    return mcq("Ein Aufzug startet im Stockwerk %s, fährt %d Stockwerke nach unten und dann %d nach oben. In welchem Stockwerk hält er?" % (dz(s), u, o), dz(v), [dz(s + u - o), dz(s - u - o), dz(-v) if v else "1"],
               "%s − %d + %d = <b>%s</b>." % (dz(s), u, o, dz(v)))


def main():
    seen = set()
    sets = [
        ("Addieren und subtrahieren", mix(R, seen, [(addsub_dez, 14), (addsub_bru, 6)])),
        ("Brüche mit Vorzeichen", mix(R, seen, [(addsub_bru, 14), (maldurch, 6)])),
        ("Multiplizieren und dividieren", mix(R, seen, [(maldurch, 12), (mehrere, 8)])),
        ("Rechengesetze und Klammern", mix(R, seen, [(klammern, 20)])),
        ("Sachaufgaben", mix(R, seen, [(sache, 20)])),
    ]
    body = lesson(
        ["Addieren und Subtrahieren: Plus eine negative Zahl ist Minus, Minus eine negative Zahl ist Plus.",
         "Multiplizieren und Dividieren: gleiche Vorzeichen ergeben Plus, verschiedene Minus.",
         "Bei mehreren Faktoren zählt man die negativen: gerade Anzahl → Plus, ungerade Anzahl → Minus.",
         "Es gelten die bekannten Regeln: Klammern zuerst, Punkt vor Strich. Vertauschen und Zusammenfassen hilft beim Rechnen."],
        [example("−2,5 − (−4,1)", ["−2,5 + 4,1"], "1,6"),
         example("(−2) %s 3 %s (−5) %s (−1)" % (MAL, MAL, MAL), ["3 negative Faktoren: Minus", "2 %s 3 %s 5 %s 1 = 30" % (MAL, MAL, MAL)], "−30")],
        [["−3 − (−5) = −8", "Minus Minus wird Plus: −3 + 5 = 2"],
         ["(−2) %s (−3) %s (−4) = 24" % (MAL, MAL), "Drei negative Faktoren: −24"],
         ["−%s + %s = %s" % (fr(1, 2), fr(1, 3), fr(2, 5)), "Hauptnenner: −%s + %s = −%s" % (fr(3, 6), fr(2, 6), fr(1, 6))]])
    faq = [
        {"q": "Was ergibt Minus mal Minus?", "a": "Plus. (−3) · (−4) = 12."},
        {"q": "Wie viele Minuszeichen ergeben ein negatives Produkt?", "a": "Eine ungerade Anzahl negativer Faktoren ergibt ein negatives Produkt, eine gerade Anzahl ein positives."},
        {"q": "Wie subtrahiert man eine negative Zahl?", "a": "Man addiert ihre Gegenzahl: 5 − (−2) = 5 + 2 = 7."},
        {"q": "Gelten die Rechengesetze auch für rationale Zahlen?", "a": "Ja. Kommutativ-, Assoziativ- und Distributivgesetz gelten für alle rationalen Zahlen."},
    ]
    make_unit(R, "rechnen-mit-rationalen-zahlen", "Z",
              "Die Schülerinnen und Schüler addieren, subtrahieren, multiplizieren und dividieren rationale Zahlen in Dezimal- und Bruchschreibweise, nutzen Vorzeichenregeln und Rechengesetze und lösen Sachaufgaben (Zusammenfassung).",
              "Rechnen mit rationalen Zahlen",
              "Rechnen mit rationalen Zahlen Klasse 7 – Arbeitsblätter mit Lösungen",
              "Rationale Zahlen rechnen",
              "Rechnen mit rationalen Zahlen für Klasse 7: Vorzeichenregeln, Brüche und Dezimalzahlen mit Vorzeichen, Klammern und Sachaufgaben. 100 Aufgaben mit Lösungen, kostenlos.",
              "Gleiche Vorzeichen: Plus. Verschiedene: Minus.",
              "Minus eine negative Zahl ist Plus.",
              body, faq, sets, 2, grade="klasse-7")


if __name__ == "__main__":
    main()
