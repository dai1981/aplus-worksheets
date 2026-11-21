# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 8: Lineare Funktionen（Leitidee Funktionaler Zusammenhang, Sek I）
  python3 tools/gen_de_mathe_k8_lineare_funktionen.py
Funktionswerte und Wertetabellen von f(x) = mx + b, Steigung m und y-Achsenabschnitt b, steigend/fallend, Graphen ablesen,
Punktprobe, Nullstelle, Sachaufgaben (Grundgebühr und Preis pro Einheit, Kerze, Wassertank).
Fehler: m und b vertauscht, Vorzeichen von m beim Ablesen, Punktprobe mit x und y vertauscht, Nullstelle = b.
"""
import random
from fractions import Fraction as Fr
from de_common import lesson, example, make_unit, mix, MAL, table, BLUE
from de_k6 import bh, dz
from de_k8 import mcq, expr, gl, par, kosy, eur

R = random.Random(49805)
G = ":"


def zahl(v):
    v = Fr(v)
    return bh(v) if v.denominator != 1 else dz(v)


def mb():
    m = R.choice([-1, 1]) * R.choice([1, 2, 3, 4, 5, Fr(1, 2), Fr(3, 2), Fr(1, 3)])
    b = R.randint(-6, 6)
    return Fr(m), Fr(b)


def fx(m, b):
    return "f(x) = %s" % expr([(m, "x"), (b, "")])


def werte():
    m, b = Fr(R.choice([-4, -3, -2, -1, 1, 2, 3, 4, 5])), Fr(R.randint(-8, 8))
    kind = R.choice(["wert", "wert", "tabelle", "x"])
    if kind == "wert":
        x = R.randint(-5, 6)
        y = m * x + b
        return mcq("Berechne f(%s) für %s." % (dz(x), fx(m, b)), zahl(y), [zahl(m + x + b) if m + x + b != y else zahl(y + 1), zahl(m * x - b) if b else zahl(y - 1), zahl(b * x + m)],
                   "f(%s) = %s %s %s%s = <b>%s</b>." % (dz(x), zahl(m), MAL, par(x), (" + %s" % zahl(b)) if b > 0 else (" − %s" % zahl(-b)) if b < 0 else "", zahl(y)))
    if kind == "x":
        x = R.randint(-5, 8)
        y = m * x + b
        return mcq("Für %s gilt f(x) = %s. Wie groß ist x?" % (fx(m, b), zahl(y)), "x = %s" % zahl(x), ["x = %s" % zahl(m * y + b), "x = %s" % zahl((y + b) / m) if (y + b) / m != x else "x = %s" % zahl(x + 1), "x = %s" % zahl(-x) if x else "x = 1"],
                   "%s = %s. %s auf beiden Seiten und durch %s teilen: <b>x = %s</b>." % (expr([(m, "x"), (b, "")]), zahl(y), ("− %s" % zahl(b)) if b >= 0 else ("+ %s" % zahl(-b)), zahl(m), zahl(x)))
    xs = [0, 1, 2, 3]
    ys = [m * x + b for x in xs]
    miss = R.randint(1, 3)
    shown = [zahl(y) if i != miss else "?" for i, y in enumerate(ys)]
    tab = table(["x"] + [str(x) for x in xs], [["f(x)"] + shown])
    return mcq(tab + "Die Tabelle gehört zu %s. Welche Zahl fehlt?" % fx(m, b), zahl(ys[miss]), [zahl(ys[miss] + m), zahl(ys[miss] - b) if b else zahl(ys[miss] + 1), zahl(m * miss)],
               "f(%d) = %s %s %d %s = <b>%s</b>." % (miss, zahl(m), MAL, miss, ("+ %s" % zahl(b)) if b >= 0 else ("− %s" % zahl(-b)), zahl(ys[miss])))


def steigung():
    m, b = mb()
    kind = R.choice(["m", "b", "richtung", "welche"])
    if kind == "m":
        return mcq("Wie groß ist die Steigung m von %s?" % fx(m, b), "m = %s" % zahl(m), ["m = %s" % zahl(b) if b != m else "m = %s" % zahl(m + 1), "m = %s" % zahl(-m), "m = %s" % zahl(1 / m)],
                   "In f(x) = mx + b steht m vor dem x: <b>m = %s</b>." % zahl(m))
    if kind == "b":
        if b == 0:
            return None
        return mcq("Wo schneidet der Graph von %s die y-Achse?" % fx(m, b), "in (0 | %s)" % zahl(b), ["in (%s | 0)" % zahl(b), "in (0 | %s)" % zahl(m), "in (0 | %s)" % zahl(-b)],
                   "Für x = 0 ist f(0) = b = %s: <b>(0 | %s)</b>." % (zahl(b), zahl(b)))
    if kind == "richtung":
        ans = "steigend" if m > 0 else "fallend"
        return mcq("Ist der Graph von %s steigend oder fallend?" % fx(m, b), ans, ["fallend" if m > 0 else "steigend", "parallel zur x-Achse", "Das hängt von b ab."],
                   "m = %s ist %s: <b>%s</b>." % (zahl(m), "positiv" if m > 0 else "negativ", ans))
    m2 = Fr(R.choice([2, 3, 4, 5]))
    return mcq("Welche Gerade ist am steilsten?", "y = %s" % expr([(-m2 - 1, "x"), (1, "")]), [gl(m2, 3), gl(Fr(1, 2), -m2), gl(1, 5 * m2)],
               "Am steilsten ist die Gerade, deren m den größten Betrag hat: |%s| = %s. <b>%s</b>" % (zahl(-m2 - 1), zahl(m2 + 1), gl(-m2 - 1, 1)))


def ablesen():
    m = Fr(R.choice([-3, -2, -1, 1, 2, 3, Fr(1, 2), Fr(-1, 2), Fr(1, 3), Fr(-2, 3), Fr(3, 2)]))
    b = Fr(R.randint(-3, 3))
    pic = kosy([(m, b, BLUE, "")], lo=-5, hi=5, label="Graph einer linearen Funktion")
    kind = R.choice(["m", "b", "gl"])
    if kind == "m":
        return mcq(pic + "Lies die Steigung m der Geraden ab.", "m = %s" % zahl(m), ["m = %s" % zahl(-m), "m = %s" % zahl(1 / m), "m = %s" % zahl(b) if b != m and b != -m else "m = %s" % zahl(m + 1)],
                   "Steigungsdreieck: %d nach rechts, %s nach %s. m = <b>%s</b>." % (m.denominator, dz(abs(m.numerator)), "oben" if m > 0 else "unten", zahl(m)))
    if kind == "b":
        return mcq(pic + "Wo schneidet die Gerade die y-Achse?", "b = %s" % zahl(b), ["b = %s" % zahl(-b) if b else "b = 1", "b = %s" % zahl(m) if m != b else "b = %s" % zahl(b + 2), "b = %s" % zahl(-b / m) if b and -b / m != b else "b = %s" % zahl(b - 1)],
                   "Die Gerade schneidet die y-Achse bei <b>%s</b>." % zahl(b))
    return mcq(pic + "Welche Funktionsgleichung gehört zum Graphen?", gl(m, b), [gl(-m, b), gl(b, m) if b not in (0, m) else gl(m, b + 1), gl(1 / m, b)],
               "y-Achsenabschnitt %s, Steigung %s: <b>%s</b>." % (zahl(b), zahl(m), gl(m, b)))


def probe():
    m, b = Fr(R.choice([-3, -2, -1, 1, 2, 3, 4])), Fr(R.randint(-6, 6))
    kind = R.choice(["probe", "probe", "null", "null"])
    if kind == "probe":
        x = R.randint(-4, 5)
        y = m * x + b + R.choice([0, 0, 1, -1, 2])
        on = y == m * x + b
        ans = "Ja, denn f(%s) = %s." % (dz(x), zahl(m * x + b)) if on else "Nein, denn f(%s) = %s." % (dz(x), zahl(m * x + b))
        return mcq("Liegt der Punkt P(%s | %s) auf dem Graphen von %s?" % (dz(x), zahl(y), fx(m, b)), ans,
                   ["Nein, denn f(%s) = %s." % (dz(x), zahl(m * x + b + 1)) if on else "Ja, denn f(%s) = %s." % (dz(x), zahl(y)), "Ja, denn %s ist eine ganze Zahl." % zahl(y), "Nein, denn x muss positiv sein." if x < 0 else "Nein, denn ein Punkt liegt nie genau auf einer Geraden."],
                   "Punktprobe: x = %s einsetzen. f(%s) = %s%s. <b>%s</b>" % (dz(x), dz(x), zahl(m * x + b), " = y" if on else " ≠ %s" % zahl(y), "Ja" if on else "Nein"))
    x0 = Fr(R.randint(-6, 6), R.choice([1, 1, 2]))
    b = -m * x0
    if b == 0 or (b * 2).denominator != 1:
        return None
    return mcq("Berechne die Nullstelle von %s." % fx(m, b), "x = %s" % zahl(x0), ["x = %s" % zahl(b), "x = %s" % zahl(-x0) if x0 else "x = 1", "x = %s" % zahl(b / m)],
               "f(x) = 0: %s = 0, also %s = %s und <b>x = %s</b>." % (expr([(m, "x"), (b, "")]), expr([(m, "x")]), zahl(-b), zahl(x0)))


def sache():
    kind = R.choice(["taxi", "handy", "kerze", "tank", "lesen"])
    if kind == "taxi":
        g, p = Fr(R.choice([350, 400, 450, 500]), 100), Fr(R.choice([180, 200, 220, 250]), 100)
        k = R.randint(3, 15)
        return mcq("Eine Taxifahrt kostet %s Grundgebühr und %s pro km. Wie viel kostet eine Fahrt von %d km?" % (eur(g), eur(p), k), eur(g + p * k),
                   [eur((g + p) * k), eur(p * k), eur(g * k + p)],
                   "y = %s %s x + %s. Für x = %d: %s + %s = <b>%s</b>." % (dz(p), MAL, dz(g), k, eur(p * k), eur(g), eur(g + p * k)))
    if kind == "handy":
        g, p = R.choice([5, 8, 10, 12]), Fr(R.choice([5, 9, 10, 15]), 100)
        return mcq("Ein Handytarif kostet %d € im Monat plus %s ct pro Minute. Welche Funktion beschreibt die Kosten y (in €) für x Minuten?" % (g, dz(p * 100)), "y = %s %s x + %d" % (dz(p), MAL, g),
                   ["y = %d %s x + %s" % (g, MAL, dz(p)), "y = %s %s x + %d" % (dz(p * 100), MAL, g), "y = %s %s x" % (dz(p + g), MAL)],
                   "Grundgebühr = b = %d, Preis pro Minute = m = %s €. <b>y = %s %s x + %d</b>" % (g, dz(p), dz(p), MAL, g))
    if kind == "kerze":
        h, r = R.choice([20, 24, 25, 30]), Fr(R.choice([2, 3, 4, 5]), 2)
        t = R.randint(2, 6)
        if h - r * t <= 0:
            return None
        return mcq("Eine Kerze ist %d cm hoch und brennt pro Stunde %s cm ab. Wie hoch ist sie nach %d Stunden?" % (h, dz(r), t), "%s cm" % dz(h - r * t), ["%s cm" % dz(h + r * t), "%s cm" % dz(r * t), "%s cm" % dz(h - r - t)],
                   "y = %s − %s %s x. Für x = %d: %d − %s = <b>%s cm</b>." % (h, dz(r), MAL, t, h, dz(r * t), dz(h - r * t)))
    if kind == "tank":
        v, r = R.choice([60, 80, 100, 120]), R.choice([4, 5, 8, 10])
        if v % r:
            return None
        return mcq("Ein Tank enthält %d Liter. Pro Minute fließen %d Liter ab. Nach wie vielen Minuten ist er leer?" % (v, r), "nach %d Minuten" % (v // r), ["nach %d Minuten" % (v - r), "nach %d Minuten" % (v * r // 10), "nach %d Minuten" % (v // r + 1)],
                   "y = %d − %dx = 0 ergibt x = %d %s %d = <b>%d Minuten</b> (Nullstelle)." % (v, r, v, G, r, v // r))
    m, b = R.choice([(2, 10), (3, 5), (5, 20), (4, 12), (Fr(3, 2), 6)])
    x = R.randint(2, 8)
    return mcq("In einem Glas steigt der Wasserstand gleichmäßig: y = %s (y in cm, x in Minuten). Was bedeutet die Zahl %s?" % (expr([(m, "x"), (b, "")]), dz(b)),
               "Am Anfang steht das Wasser %s cm hoch." % dz(b), ["Das Wasser steigt pro Minute um %s cm." % dz(b), "Nach %s Minuten ist das Glas voll." % dz(b), "Am Ende steht das Wasser %s cm hoch." % dz(b)],
               "b ist der Wert bei x = 0, also der Anfangswert: <b>%s cm am Anfang</b>. m = %s ist die Zunahme pro Minute." % (dz(b), zahl(m)))


def main():
    seen = set()
    sets = [
        ("Funktionswerte", mix(R, seen, [(werte, 20)])),
        ("Steigung und y-Achsenabschnitt", mix(R, seen, [(steigung, 20)])),
        ("Graphen ablesen", mix(R, seen, [(ablesen, 20)])),
        ("Punktprobe und Nullstelle", mix(R, seen, [(probe, 20)])),
        ("Sachaufgaben", mix(R, seen, [(sache, 20)])),
    ]
    body = lesson(
        ["Eine <b>lineare Funktion</b> hat die Gleichung f(x) = mx + b. Ihr Graph ist eine Gerade.",
         "<b>m</b> ist die Steigung: Geht man 1 nach rechts, geht der Graph m nach oben (m &gt; 0, steigend) oder nach unten (m &lt; 0, fallend).",
         "<b>b</b> ist der y-Achsenabschnitt: Der Graph schneidet die y-Achse im Punkt (0 | b).",
         "Die <b>Nullstelle</b> ist der x-Wert mit f(x) = 0. Bei der <b>Punktprobe</b> setzt man x ein und vergleicht mit y."],
        [example("f(x) = 2x − 3, f(4) = ?", ["2 %s 4 − 3" % MAL], "5"),
         example("Nullstelle von f(x) = 3x − 6", ["3x − 6 = 0", "3x = 6"], "x = 2")],
        [["f(x) = 3x + 2: m = 2", "m steht vor dem x: m = 3, b = 2"],
         ["Punktprobe P(2 | 5) mit x = 5", "x ist die erste Koordinate: x = 2"],
         ["Nullstelle von f(x) = 2x − 4 ist −4", "−4 ist der y-Achsenabschnitt. Nullstelle: x = 2"]])
    faq = [
        {"q": "Was bedeuten m und b in f(x) = mx + b?", "a": "m ist die Steigung, b der y-Achsenabschnitt. Der Graph geht durch (0 | b) und steigt pro Schritt nach rechts um m."},
        {"q": "Wie lese ich die Steigung am Graphen ab?", "a": "Mit einem Steigungsdreieck: Gehe eine Einheit (oder mehrere) nach rechts und zähle, wie viel es nach oben oder unten geht. Teile beides."},
        {"q": "Wie berechne ich die Nullstelle?", "a": "Setze f(x) = 0 und löse die Gleichung nach x auf."},
        {"q": "Was ist eine Punktprobe?", "a": "Man setzt die x-Koordinate eines Punktes in die Funktion ein. Kommt die y-Koordinate heraus, liegt der Punkt auf dem Graphen."},
    ]
    make_unit(R, "lineare-funktionen", "F",
              "Die Schülerinnen und Schüler beschreiben lineare Funktionen mit Gleichung, Wertetabelle und Graph, deuten Steigung und y-Achsenabschnitt, bestimmen Nullstellen, führen Punktproben durch und nutzen lineare Funktionen in Sachsituationen (Zusammenfassung).",
              "Lineare Funktionen",
              "Lineare Funktionen Klasse 8 – Steigung, y-Achsenabschnitt, Arbeitsblätter",
              "Lineare Funktionen",
              "Lineare Funktionen für Klasse 8: Funktionswerte, Steigung m und y-Achsenabschnitt b, Graphen ablesen, Punktprobe, Nullstelle und Sachaufgaben. 100 Aufgaben mit Lösungen, kostenlos.",
              "f(x) = mx + b",
              "m: Steigung. b: y-Achsenabschnitt.",
              body, faq, sets, 5, grade="klasse-8")


if __name__ == "__main__":
    main()
