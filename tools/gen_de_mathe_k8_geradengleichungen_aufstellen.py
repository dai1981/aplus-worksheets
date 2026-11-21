# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 8: Geradengleichungen aufstellen（Leitidee Funktionaler Zusammenhang, Sek I）
  python3 tools/gen_de_mathe_k8_geradengleichungen_aufstellen.py
Steigung aus zwei Punkten, Gleichung aus Steigung und Punkt, Gleichung aus zwei Punkten, parallele Geraden, Gleichung aus dem Graphen,
Sachaufgaben (Tarif aus zwei Angaben).
Fehler: m = Δx : Δy, Differenzen in verschiedener Reihenfolge, b = y-Koordinate des Punktes, parallele Geraden mit gleichem b statt gleichem m.
"""
import random
from fractions import Fraction as Fr
from de_common import lesson, example, make_unit, mix, MAL, BLUE
from de_k6 import bh, dz
from de_k8 import mcq, expr, gl, par, kosy, eur

R = random.Random(49806)
G = ":"


def zahl(v):
    v = Fr(v)
    return bh(v) if v.denominator != 1 else dz(v)


def P(n, x, y):
    return "%s(%s | %s)" % (n, zahl(x), zahl(y))


def m_two():
    m = Fr(R.choice([-4, -3, -2, -1, 1, 2, 3, 4, Fr(1, 2), Fr(-1, 2), Fr(2, 3), Fr(-3, 2)]))
    x1 = R.randint(-5, 4)
    dx = R.choice([2, 3, 4, 6]) if m.denominator != 1 else R.randint(1, 5)
    if (m * dx).denominator != 1:
        return None
    y1 = R.randint(-6, 6)
    x2, y2 = x1 + dx, y1 + m * dx
    return mcq("Berechne die Steigung der Geraden durch %s und %s." % (P("A", x1, y1), P("B", x2, y2)), "m = %s" % zahl(m),
               ["m = %s" % zahl(1 / m), "m = %s" % zahl(-m), "m = %s" % zahl(Fr(y2 + y1, x2 + x1)) if x2 + x1 and Fr(y2 + y1, x2 + x1) not in (m, -m, 1 / m) else "m = %s" % zahl(m * 2)],
               "m = (y₂ − y₁) %s (x₂ − x₁) = (%s − %s) %s (%s − %s) = %s %s %s = <b>%s</b>." % (G, zahl(y2), par(y1), G, zahl(x2), par(x1), zahl(y2 - y1), G, zahl(dx), zahl(m)))


def punkt_m():
    m = Fr(R.choice([-4, -3, -2, -1, 1, 2, 3, 4, 5, Fr(1, 2), Fr(-1, 2)]))
    x = R.randint(-4, 5)
    if (m * x).denominator != 1 or x == 0:
        return None
    b = Fr(R.randint(-7, 7))
    y = m * x + b
    return mcq("Eine Gerade hat die Steigung m = %s und geht durch %s. Wie lautet ihre Gleichung?" % (zahl(m), P("P", x, y)), gl(m, b),
               [gl(m, y), gl(m, y + m * x) if y + m * x != b else gl(m, b + 1), gl(m, x - m * y) if x - m * y != b else gl(-m, b)],
               "In %s + b einsetzen: %s = %s %s %s + b, also b = %s. <b>%s</b>" % (gl(m, 0), zahl(y), zahl(m), MAL, par(x), zahl(b), gl(m, b)))


def zwei():
    m = Fr(R.choice([-3, -2, -1, 1, 2, 3, 4]))
    b = Fr(R.randint(-6, 6))
    x1, x2 = sorted(R.sample([v for v in range(-4, 6) if v != 0], 2))
    y1, y2 = m * x1 + b, m * x2 + b
    return mcq("Bestimme die Gleichung der Geraden durch %s und %s." % (P("A", x1, y1), P("B", x2, y2)), gl(m, b),
               [gl(1 / m, b) if 1 / m != m else gl(m, -b) if b else gl(m, 1), gl(m, y1), gl(-m, b + 2 * m * x1) if gl(-m, b + 2 * m * x1) != gl(m, b) else gl(m, b + 2)],
               "m = (%s − %s) %s (%s − %s) = %s. Mit A: %s = %s %s %s + b, b = %s. <b>%s</b>" % (zahl(y2), par(y1), G, zahl(x2), par(x1), zahl(m), zahl(y1), zahl(m), MAL, par(x1), zahl(b), gl(m, b)))


def parallel():
    m = Fr(R.choice([-3, -2, -1, 1, 2, 3, Fr(1, 2), Fr(-1, 2)]))
    b = Fr(R.randint(-5, 5))
    kind = R.choice(["par", "par", "achsen", "welche"])
    if kind == "par":
        x = R.randint(-3, 4)
        if (m * x).denominator != 1:
            return None
        c = Fr(R.randint(-6, 6))
        y = m * x + c
        if c == b:
            return None
        return mcq("Die Gerade h ist parallel zu g: %s und geht durch %s. Wie lautet die Gleichung von h?" % (gl(m, b), P("P", x, y)), gl(m, c),
                   [gl(-m, c), gl(m, b + y), gl(m, y)],
                   "Parallele Geraden haben dieselbe Steigung m = %s. Mit P: b = %s − %s %s %s = %s. <b>%s</b>" % (zahl(m), zahl(y), par(m), MAL, par(x), zahl(c), gl(m, c)))
    if kind == "achsen":
        if b == 0 or (b / m).denominator > 2:
            return None
        x0 = -b / m
        return mcq("In welchen Punkten schneidet %s die Koordinatenachsen?" % gl(m, b), "(0 | %s) und (%s | 0)" % (zahl(b), zahl(x0)),
                   ["(%s | 0) und (0 | %s)" % (zahl(b), zahl(x0)), "(0 | %s) und (%s | 0)" % (zahl(b), zahl(-x0)), "(0 | %s) und (%s | 0)" % (zahl(m), zahl(b))],
                   "y-Achse: x = 0, y = %s. x-Achse: %s = 0, x = %s. <b>(0 | %s) und (%s | 0)</b>" % (zahl(b), expr([(m, "x"), (b, "")]), zahl(x0), zahl(b), zahl(x0)))
    c = b + R.choice([-3, -2, 2, 3])
    return mcq("Welche Gerade ist parallel zu %s?" % gl(m, b), gl(m, c), [gl(-m, b), gl(1 / m, c) if abs(m) != 1 else gl(m + 1, c), gl(m * 2, b)],
               "Parallel heißt: gleiche Steigung m = %s. <b>%s</b>" % (zahl(m), gl(m, c)))


def graph():
    m = Fr(R.choice([-2, -1, 1, 2, Fr(1, 2), Fr(-1, 2), Fr(1, 3), Fr(2, 3), Fr(-2, 3), Fr(3, 2)]))
    b = Fr(R.randint(-3, 3))
    x1 = R.choice([-3, -2, 1, 2, 3])
    if (m * x1).denominator != 1 or not -4 <= m * x1 + b <= 4:
        return None
    pic = kosy([(m, b, BLUE, "g")], pts=[(0, b, "A"), (x1, m * x1 + b, "B")], label="Gerade g durch A und B")
    return mcq(pic + "Bestimme die Gleichung der Geraden g durch A und B.", gl(m, b), [gl(1 / m, b), gl(-m, b), gl(m, m * x1 + b)],
               "A(0 | %s) liefert b = %s. Von A nach B: %s nach rechts, %s nach %s, m = %s. <b>%s</b>" % (zahl(b), zahl(b), dz(abs(x1)), zahl(abs(m * x1)), "oben" if m * x1 > 0 else "unten", zahl(m), gl(m, b)))


def sache():
    kind = R.choice(["tarif", "tarif", "kerze", "temp", "vergleich"])
    if kind == "tarif":
        g = R.choice([3, 4, 5, 6, 8])
        p = Fr(R.choice([150, 175, 200, 225, 250]), 100)
        k1, k2 = sorted(R.sample(range(2, 16), 2))
        c1, c2 = g + p * k1, g + p * k2
        return mcq("Eine Taxifahrt über %d km kostet %s, über %d km kostet sie %s. Wie hoch ist die Grundgebühr?" % (k1, eur(c1), k2, eur(c2)), eur(g),
                   [eur(p), eur(c1 - p), eur(c2 - c1)],
                   "m = (%s − %s) %s %d = %s pro km. b = %s − %d %s %s = <b>%s</b>." % (eur(c2), eur(c1), G, k2 - k1, eur(p), eur(c1), k1, MAL, eur(p), eur(g)))
    if kind == "kerze":
        h0, r = R.choice([24, 30, 36, 40]), R.choice([2, 3, 4])
        t1, t2 = sorted(R.sample(range(1, 6), 2))
        return mcq("Eine Kerze ist nach %d Stunden %d cm hoch und nach %d Stunden %d cm hoch. Wie hoch war sie am Anfang?" % (t1, h0 - r * t1, t2, h0 - r * t2), "%d cm" % h0,
                   ["%d cm" % (h0 - r * t1), "%d cm" % (h0 - r), "%d cm" % (h0 - r * t1 + r * t2)],
                   "Pro Stunde: (%d − %d) %s %d = %d cm weniger. Anfang: %d + %d %s %d = <b>%d cm</b>." % (h0 - r * t1, h0 - r * t2, G, t2 - t1, r, h0 - r * t1, t1, MAL, r, h0))
    if kind == "temp":
        a, d = R.choice([8, 10, 12, 15]), R.choice([2, 3])
        h1, h2 = sorted(R.sample([1, 2, 3, 4], 2))
        return mcq("Ab 7 Uhr morgens steigt die Temperatur gleichmäßig. Um %d Uhr sind es %d °C, um %d Uhr %d °C. Welche Gleichung beschreibt die Temperatur y nach x Stunden ab 7 Uhr?" % (7 + h1, a + d * h1, 7 + h2, a + d * h2),
                   gl(d, a), [gl(d, a + d * h1), gl(Fr(h2 - h1, d * (h2 - h1)), a), gl(a, d)],
                   "m = %d °C pro Stunde, b = %d − %d %s %d = %d. <b>%s</b>" % (d, a + d * h1, h1, MAL, d, a, gl(d, a)))
    a = (R.choice([0, 6, 12]), Fr(R.choice([3, 4])))
    b = (R.choice([15, 20, 24]), Fr(R.choice([1, 2])))
    if a[1] <= b[1] or b[0] <= a[0]:
        return None
    x = Fr(b[0] - a[0], 1) / (a[1] - b[1])
    if x.denominator != 1:
        return None
    return mcq("Tarif A: %d € Grundgebühr und %s € pro Stunde. Tarif B: %d € Grundgebühr und %s € pro Stunde. Ab wie vielen Stunden ist B günstiger?" % (a[0], dz(a[1]), b[0], dz(b[1])),
               "ab mehr als %s Stunden" % dz(x), ["ab mehr als %s Stunden" % dz(x + 2), "ab mehr als %s Stunden" % dz(Fr(b[0] + a[0], a[1] + b[1])) if Fr(b[0] + a[0], a[1] + b[1]) != x else "ab mehr als %s Stunden" % dz(x - 1), "B ist nie günstiger."],
               "Gleichsetzen: %s = %s, also x = %s. Danach steigt A schneller: <b>ab mehr als %s Stunden</b>." % (expr([(a[1], "x"), (a[0], "")]), expr([(b[1], "x"), (b[0], "")]), dz(x), dz(x)))


def main():
    seen = set()
    sets = [
        ("Steigung aus zwei Punkten", mix(R, seen, [(m_two, 20)])),
        ("Steigung und Punkt", mix(R, seen, [(punkt_m, 20)])),
        ("Gerade durch zwei Punkte", mix(R, seen, [(zwei, 12), (graph, 8)])),
        ("Parallelen und Achsenpunkte", mix(R, seen, [(parallel, 20)])),
        ("Sachaufgaben", mix(R, seen, [(sache, 20)])),
    ]
    body = lesson(
        ["Steigung aus zwei Punkten: m = (y₂ − y₁) %s (x₂ − x₁). Beide Differenzen in derselben Reihenfolge bilden." % G,
         "Gleichung aus m und einem Punkt: Die Koordinaten in y = mx + b einsetzen und nach b auflösen.",
         "<b>Parallele Geraden</b> haben dieselbe Steigung m, aber verschiedene y-Achsenabschnitte.",
         "Schnittpunkt mit der y-Achse: (0 | b). Schnittpunkt mit der x-Achse: y = 0 setzen."],
        [example("A(1 | 3), B(4 | 9)", ["m = (9 − 3) : (4 − 1) = 2", "3 = 2 %s 1 + b, b = 1" % MAL], "y = 2x + 1")],
        [["m = (x₂ − x₁) : (y₂ − y₁)", "y-Differenz durch x-Differenz"],
         ["P(2 | 5), m = 3: y = 3x + 5", "b ausrechnen: 5 = 3 %s 2 + b, b = −1" % MAL],
         ["Parallel zu y = 2x + 1 ist y = 3x + 1", "Parallel heißt gleiche Steigung: y = 2x + c"]])
    faq = [
        {"q": "Wie berechne ich die Steigung aus zwei Punkten?", "a": "m = (y₂ − y₁) : (x₂ − x₁). Man teilt den Höhenunterschied durch den Unterschied in x-Richtung."},
        {"q": "Wie finde ich b, wenn m und ein Punkt gegeben sind?", "a": "Setze die Koordinaten des Punktes und m in y = mx + b ein und löse nach b auf."},
        {"q": "Woran erkenne ich parallele Geraden?", "a": "Sie haben die gleiche Steigung m. Nur der y-Achsenabschnitt ist verschieden."},
        {"q": "Wie stelle ich eine Gleichung aus zwei Punkten auf?", "a": "Erst m aus den beiden Punkten berechnen, dann mit einem Punkt b bestimmen."},
    ]
    make_unit(R, "geradengleichungen-aufstellen", "F",
              "Die Schülerinnen und Schüler bestimmen die Steigung aus zwei Punkten, stellen Geradengleichungen aus Steigung und Punkt, aus zwei Punkten und aus Graphen auf, erkennen parallele Geraden und lösen Sachaufgaben (Zusammenfassung).",
              "Geradengleichungen aufstellen",
              "Geradengleichung aufstellen Klasse 8 – zwei Punkte, Steigung, Arbeitsblätter",
              "Geradengleichungen",
              "Geradengleichungen für Klasse 8: Steigung aus zwei Punkten, Gleichung aus Punkt und Steigung, parallele Geraden, Achsenschnittpunkte und Sachaufgaben. 100 Aufgaben mit Lösungen, kostenlos.",
              "m = (y₂ − y₁) : (x₂ − x₁)",
              "Dann einen Punkt einsetzen und b ausrechnen.",
              body, faq, sets, 6, grade="klasse-8")


if __name__ == "__main__":
    main()
