# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 6: Prozente – Anteile vergleichen（Leitidee Zahl und Operation, Sek I）
  python3 tools/gen_de_mathe_k6_prozente.py
Prozent als Hundertstel, Bruch – Dezimalzahl – Prozent, wichtige Prozentsätze (50 %, 25 %, 10 % …), Prozent von Größen, Anteile in Prozent vergleichen, Sachaufgaben.
Fehler: 0,5 = 5 %, 1/4 = 4 %, Prozentsatz von der falschen Größe genommen, Anteile ohne gemeinsamen Grundwert verglichen.
"""
import random
from math import gcd
from fractions import Fraction as Fr
from de_common import lesson, example, make_unit, mix, Kids, fr, MAL, table
from de_k6 import bh, dz, mcq

R = random.Random(49611)
KIDS = Kids(R)
P = " %"


def pz(v):
    return dz(Fr(v) * 100) + P


BR = [(1, 2), (1, 4), (3, 4), (1, 5), (2, 5), (3, 5), (4, 5), (1, 10), (3, 10), (7, 10), (9, 10), (1, 20), (3, 20), (1, 25), (2, 25), (1, 50), (3, 50), (1, 8), (3, 8)]


def umwandeln():
    kind = R.choice(["b2p", "d2p", "p2b", "p2d"])
    if kind == "b2p":
        z, n = R.choice(BR)
        v = Fr(z, n)
        return mcq("Schreibe %s in Prozent." % fr(z, n), pz(v), ["%d%s" % (z, P) if z * 100 // n != z else None, "%d%s" % (n, P), "%d,%d%s" % (z, n, P), pz(v / 10)],
                   ("Auf Hundertstel erweitern: %s = %s = <b>%s</b>." % (fr(z, n), fr((v * 100).numerator, 100), pz(v))) if (v * 100).denominator == 1 else "%s = %s = <b>%s</b>." % (fr(z, n), dz(v), pz(v)))
    if kind == "d2p":
        v = Fr(R.randint(1, 199), 100) if R.random() < 0.7 else Fr(R.randint(1, 9), 10)
        return mcq("Schreibe %s in Prozent." % dz(v), pz(v), [pz(v / 10), pz(v * 10) if v * 10 < 10 else pz(v / 100), dz(v) + P],
                   "Mal 100: <b>%s</b>." % pz(v))
    if kind == "p2b":
        z, n = R.choice(BR)
        v = Fr(z, n)
        if (v * 100).denominator != 1:
            return None
        p = (v * 100).numerator
        return mcq("Schreibe %d%s als vollständig gekürzten Bruch." % (p, P), bh(v), [fr(p, 10) if p < 10 else fr(p, 1000), fr(1, p) if p > 1 else fr(1, 10), fr(p, 100) if bh(v) != fr(p, 100) else fr(p, 1000)],
                   "%d%s = %s = <b>%s</b>." % (p, P, fr(p, 100), bh(v)))
    p = R.randint(1, 150)
    v = Fr(p, 100)
    return mcq("Schreibe %d%s als Dezimalzahl." % (p, P), dz(v), [dz(v * 10), dz(v / 10), "%d,0" % p],
               "Durch 100: <b>%s</b>." % dz(v))


def von():
    p = R.choice([1, 5, 10, 20, 25, 50, 75, 2, 30, 40, 60])
    g = R.choice([20, 40, 60, 80, 100, 120, 200, 240, 300, 400, 500, 600, 800, 1000])
    v = Fr(p * g, 100)
    if v.denominator != 1:
        return None
    unit = R.choice(["€", "m", "kg", "Schüler", "Punkte"])
    us = lambda x: "%s %s" % (dz(x), unit) if unit != "Schüler" else "%s" % dz(x)
    q = "Berechne %d%s von %d %s." % (p, P, g, unit) if unit != "Schüler" else "Berechne %d%s von %d." % (p, P, g)
    return mcq(q, us(v), [us(Fr(g, p)) if g % p == 0 and p > 1 else us(v * 10), us(g - v), us(Fr(p * g, 10)) if Fr(p * g, 10) != v else us(v + 10)],
               "%d%s = %s. %d %s %s = <b>%s</b>." % (p, P, bh(Fr(p, 100)), g, MAL, bh(Fr(p, 100)), us(v)))


def anteil():
    g = R.choice([20, 25, 50, 200, 40, 80])
    a = R.randint(1, g - 1)
    v = Fr(a, g)
    if (v * 100).denominator != 1:
        return None
    th = R.choice(["Kinder einer Schule fahren mit dem Bus", "Lose sind Gewinne", "Fragen wurden richtig beantwortet", "Äpfel in einer Kiste sind rot"])
    return mcq("%d von %d %s. Wie viel Prozent sind das?" % (a, g, th.replace("Kinder einer Schule", "Kindern").replace("Lose sind", "Losen sind").replace("Fragen", "Fragen").replace("Äpfel in einer Kiste", "Äpfeln")), pz(v),
               ["%d%s" % (a, P), pz(1 - v), pz(v / 10) if v > Fr(1, 10) else pz(v * 10)],
               "%s = %s = <b>%s</b>." % (fr(a, g), fr((v * 100).numerator, 100), pz(v)))


def vergleich():
    p1, _ = KIDS.next()
    p2, _ = KIDS.next()
    if p1 == p2:
        return None
    while True:
        g1, g2 = R.sample([20, 25, 40, 50], 2)
        a1, a2 = R.randint(g1 // 2, g1 - 1), R.randint(g2 // 2, g2 - 1)
        v1, v2 = Fr(a1, g1), Fr(a2, g2)
        if v1 != v2 and (a1 > a2) != (v1 > v2):
            break
    best = p1 if v1 > v2 else p2
    return mcq("Beim Freiwurf trifft %s %d von %d Würfen, %s %d von %d Würfen. Wer hat die bessere Trefferquote?" % (p1, a1, g1, p2, a2, g2), best, [p2 if best == p1 else p1, "Beide gleich gut.", "Wer mehr Treffer hat."],
               "%s: %s = %s, %s: %s = %s. Besser ist <b>%s</b> (nicht die größere Anzahl, sondern der größere Anteil)." % (p1, fr(a1, g1), pz(v1), p2, fr(a2, g2), pz(v2), best))


def sache():
    p, er = KIDS.next()
    kind = R.choice(["rabatt", "akku", "klasse", "saft", "spar", "grund"])
    if kind == "rabatt":
        pr = R.choice([20, 40, 50, 60, 80, 100, 120])
        r = R.choice([10, 20, 25, 50])
        s = pr * r // 100
        return mcq("Ein Paar Schuhe kostet %d €. Im Schlussverkauf gibt es %d%s Rabatt. Was kosten die Schuhe jetzt?" % (pr, r, P), "%d €" % (pr - s), ["%d €" % x for x in (s, pr - r, pr + s, pr - 2 * s if pr > 2 * s else pr // 4)],
                   "%d%s von %d € = %d €. %d € − %d € = <b>%d €</b>." % (r, P, pr, s, pr, s, pr - s))
    if kind == "akku":
        p_ = R.choice([10, 20, 25, 40, 60, 75, 80])
        return mcq("Der Akku eines Tablets ist zu %d%s geladen. Welcher Anteil fehlt noch bis zur vollen Ladung?" % (p_, P), "%d%s" % (100 - p_, P), ["%d%s" % (x, P) for x in (p_, 100 - p_ + 10 if 100 - p_ + 10 <= 100 else p_ + 5, 100 - p_ - 5 if 100 - p_ - 5 > 0 else p_ + 10)],
                   "Voll sind 100%s. 100%s − %d%s = <b>%d%s</b>." % (P, P, p_, P, 100 - p_, P))
    if kind == "klasse":
        t = R.choice([20, 25])
        a = R.randint(2, t - 2)
        v = Fr(a, t)
        return mcq("In einer Klasse mit %d Kindern haben %d Kinder ein Haustier. Wie viel Prozent haben <b>kein</b> Haustier?" % (t, a), pz(1 - v), [pz(v), "%d%s" % (t - a, P), pz(1 - v + Fr(1, 10)) if 1 - v + Fr(1, 10) < 1 else pz(1 - v - Fr(1, 10))],
                   "%d Kinder ohne Haustier: %s = <b>%s</b>." % (t - a, fr(t - a, t), pz(1 - v)))
    if kind == "saft":
        p_ = R.choice([10, 20, 25, 30, 40, 50])
        ml = R.choice([200, 500, 1000, 1500])
        return mcq("Ein Getränk besteht zu %d%s aus Orangensaft. Wie viel Saft ist in %d ml?" % (p_, P, ml), "%d ml" % (ml * p_ // 100), ["%d ml" % x for x in (ml - ml * p_ // 100, p_ * 10, ml * p_ // 10 if ml * p_ // 10 != ml * p_ // 100 else ml // 2 + 10)],
                   "%d%s von %d ml = <b>%d ml</b>." % (p_, P, ml, ml * p_ // 100))
    if kind == "spar":
        g = R.choice([200, 300, 400, 500, 1000])
        p_ = R.choice([1, 2, 3])
        return mcq("%s hat %d € auf dem Sparkonto. Nach einem Jahr gibt es %d%s Zinsen. Wie viel Euro Zinsen sind das?" % (p, g, p_, P), "%d €" % (g * p_ // 100), ["%d €" % x for x in (g * p_ // 10, p_, g + g * p_ // 100)],
                   "%d%s von %d € = %d %s %d € = <b>%d €</b>." % (p_, P, g, p_, MAL, g // 100, g * p_ // 100))
    a, g = R.choice([(3, 20), (9, 25), (7, 50), (13, 20), (21, 25), (31, 50)])
    return mcq("Bei einem Turnier gewinnt eine Mannschaft %d von %d Spielen. Wie hoch ist der Anteil der Siege in Prozent?" % (a, g), pz(Fr(a, g)), ["%d%s" % (a, P), pz(Fr(g - a, g)), "%d%s" % (g, P)],
               "%s = %s = <b>%s</b>." % (fr(a, g), fr(a * 100 // g, 100), pz(Fr(a, g))))


def main():
    seen = set()
    sets = [
        ("Bruch, Dezimalzahl und Prozent", mix(R, seen, [(umwandeln, 20)])),
        ("Anteile in Prozent", mix(R, seen, [(anteil, 14), (umwandeln, 6)])),
        ("Prozent von Größen", mix(R, seen, [(von, 20)])),
        ("Anteile vergleichen", mix(R, seen, [(vergleich, 14), (anteil, 6)])),
        ("Sachaufgaben", mix(R, seen, [(sache, 20)])),
    ]
    body = lesson(
        ["<b>Prozent</b> bedeutet „von Hundert“: 1%s = %s = 0,01." % (P, fr(1, 100)),
         "Ein Bruch wird zu Prozent, indem man auf den Nenner 100 erweitert: %s = %s = 75%s." % (fr(3, 4), fr(75, 100), P),
         "Eine Dezimalzahl wird zu Prozent, indem man mit 100 multipliziert: 0,4 = 40%s." % P,
         "Anteile mit verschiedenen Grundwerten vergleicht man am besten in Prozent."],
        [example("12 von 20 in Prozent", ["%s = %s" % (fr(12, 20), fr(60, 100))], "60" + P),
         example("25%s von 80 €" % P, ["25%s = %s" % (P, fr(1, 4)), "80 € : 4"], "20 €")],
        [["0,5 = 5%s" % P, "0,5 = 0,50 = 50%s" % P],
         ["%s = 4%s" % (fr(1, 4), P), "%s = %s = 25%s" % (fr(1, 4), fr(25, 100), P)],
         ["18 Treffer sind besser als 12 Treffer", "Anteil vergleichen: 18 von 30 = 60%s, 12 von 16 = 75%s" % (P, P)]],
        extra=table(["Bruch", "Dezimalzahl", "Prozent"], [[fr(1, 2), "0,5", "50" + P], [fr(1, 4), "0,25", "25" + P], [fr(3, 4), "0,75", "75" + P], [fr(1, 5), "0,2", "20" + P], [fr(1, 10), "0,1", "10" + P], [fr(1, 100), "0,01", "1" + P]]))
    faq = [
        {"q": "Was bedeutet Prozent?", "a": "Prozent heißt „von Hundert“. 30 % bedeutet 30 von 100, also 30/100 = 0,3."},
        {"q": "Wie rechne ich einen Bruch in Prozent um?", "a": "Auf den Nenner 100 erweitern: 2/5 = 40/100 = 40 %."},
        {"q": "Wie berechne ich 25 % von 60?", "a": "25 % = 1/4. 60 : 4 = 15."},
        {"q": "Warum vergleicht man Anteile in Prozent?", "a": "Weil die Gesamtzahlen oft verschieden sind. In Prozent haben beide denselben Grundwert 100."},
    ]
    make_unit(R, "prozente", "Z",
              "Die Schülerinnen und Schüler stellen Anteile als Bruch, Dezimalzahl und Prozent dar, berechnen einfache Prozentanteile von Größen und vergleichen Anteile (Zusammenfassung).",
              "Prozente – Anteile vergleichen",
              "Prozente Klasse 6 – Bruch, Dezimalzahl, Prozent, Arbeitsblätter",
              "Prozente",
              "Prozente für Klasse 6: Brüche und Dezimalzahlen in Prozent, Prozent von Größen, Anteile vergleichen. 100 Aufgaben mit Lösungen, kostenlos.",
              "Prozent heißt „von Hundert“.",
              "Bruch auf den Nenner 100 erweitern – schon hast du Prozent.",
              body, faq, sets, 11, grade="klasse-6")


if __name__ == "__main__":
    main()
