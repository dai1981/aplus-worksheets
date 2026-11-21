# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 10: Erwartungswert（Leitidee Daten und Zufall, Sek I）
  python3 tools/gen_de_mathe_k10_erwartungswert.py
Zufallsgrößen und Wahrscheinlichkeitsverteilungen, fehlende Wahrscheinlichkeit, E(X) = x₁ · P(X = x₁) + …, Würfel- und Glücksradspiele,
faire Spiele (erwarteter Gewinn 0), fairer Einsatz, mehrstufige Experimente (Münzen, Ziehen ohne Zurücklegen), Sachaufgaben (Lose, Versicherung).
Fehler: Mittelwert der Werte statt gewichteter Mittelwert, Einsatz nicht abgezogen, Summe der Wahrscheinlichkeiten ≠ 1, Erwartungswert als sicheres Ergebnis gedeutet.
"""
import random
from fractions import Fraction as Fr
from de_common import lesson, example, make_unit, mix, MAL, num, table
from de_k6 import bh, dz, endlich
from de_k10 import mcq, zr

R = random.Random(50010)
M = "−"


def zz(v):
    v = Fr(v)
    if v < 0:
        return M + zz(-v)
    return dz(v) if endlich(v) else bh(v)


def eu(v):
    v = Fr(v)
    if not endlich(v) or (v * 100).denominator != 1:
        return "≈ " + ((M if v < 0 else "") + "%s €" % zr(abs(float(v)), 2))
    s = M if v < 0 else ""
    v = abs(v)
    return s + ("%s €" % dz(v) if v.denominator == 1 else "%s €" % zr(float(v), 2))


def tab(xs, ps, xn="x", fmt=zz):
    head = "<table class='sn-table'><tbody><tr><th>%s</th>%s</tr><tr><th>P(X = %s)</th>%s</tr></tbody></table>" % (
        xn, "".join("<td>%s</td>" % fmt(x) for x in xs), xn, "".join("<td>%s</td>" % (p if isinstance(p, str) else zz(p)) for p in ps))
    return "<div class='sn-tw'>%s</div>" % head


def verteilung():
    n = R.choice([3, 4, 4, 5])
    xs = sorted(R.sample(range(0, 10), n))
    den = R.choice([10, 20, 8, 5])
    parts = sorted(R.sample(range(1, den), n - 1))
    ps = [Fr(b - a, den) for a, b in zip([0] + parts, parts + [den])]
    if min(ps) == 0:
        return None
    kind = R.choice(["fehl", "fehl", "ge", "kl"])
    if kind == "fehl":
        i = R.randrange(n)
        shown = [("?" if j == i else ps[j]) for j in range(n)]
        return mcq("Die Tabelle zeigt die Wahrscheinlichkeitsverteilung einer Zufallsgröße X. Welche Wahrscheinlichkeit fehlt?" + tab(xs, shown), zz(ps[i]),
                   [zz(1 - ps[i]), zz(sum(ps) - ps[i]) if sum(ps) - ps[i] != ps[i] else zz(ps[i] + Fr(1, den)), zz(Fr(1, n))],
                   "Alle Wahrscheinlichkeiten zusammen ergeben 1: 1 − %s = <b>%s</b>." % (zz(1 - ps[i]), zz(ps[i])))
    k = R.randrange(1, n)
    if kind == "ge":
        v = sum(ps[k:])
        return mcq("Wie groß ist P(X ≥ %s)?" % zz(xs[k]) + tab(xs, ps), zz(v), [zz(ps[k]), zz(sum(ps[k + 1:])) if sum(ps[k + 1:]) != v else zz(1 - v + ps[k]), zz(1 - v)],
                   "Addiere alle Wahrscheinlichkeiten ab x = %s: <b>%s</b>." % (zz(xs[k]), zz(v)))
    v = sum(ps[:k])
    return mcq("Wie groß ist P(X &lt; %s)?" % zz(xs[k]) + tab(xs, ps), zz(v), [zz(sum(ps[:k + 1])), zz(ps[k - 1]) if ps[k - 1] != v else zz(1 - v + ps[k]), zz(1 - v)],
               "„Kleiner als %s“: nur die Werte davor: <b>%s</b>." % (zz(xs[k]), zz(v)))


def erwartung():
    n = R.choice([3, 4])
    xs = sorted(R.sample([-5, -2, -1, 0, 1, 2, 3, 4, 5, 6, 8, 10], n))
    den = R.choice([10, 4, 5, 8, 20])
    parts = sorted(R.sample(range(1, den), n - 1))
    ps = [Fr(b - a, den) for a, b in zip([0] + parts, parts + [den])]
    E = sum(x * p for x, p in zip(xs, ps))
    return mcq("Berechne den Erwartungswert E(X)." + tab(xs, ps), zz(E),
               [zz(Fr(sum(xs), n)) if Fr(sum(xs), n) != E else zz(E + 1), zz(sum(abs(x) * p for x, p in zip(xs, ps))) if any(x < 0 for x in xs) and sum(abs(x) * p for x, p in zip(xs, ps)) != E else zz(E * 2 if E else 1), zz(sum(xs)) if sum(xs) != E else zz(E - 1)],
               "E(X) = %s = <b>%s</b>." % (" + ".join("%s %s %s" % ("(%s)" % zz(x) if x < 0 else zz(x), MAL, zz(p)) for x, p in zip(xs, ps)), zz(E)))


def spiel():
    kind = R.choice(["wuerfel", "wuerfel", "rad", "rad", "muenze"])
    if kind == "wuerfel":
        g6 = R.choice([3, 4, 5, 6, 10])
        g5 = R.choice([0, 1, 2])
        e = R.choice([1, 2])
        E = Fr(g6, 6) + Fr(g5, 6) - e
        return mcq("Ein Spiel kostet %d € Einsatz. Man würfelt einmal: Bei einer 6 bekommt man %d € ausgezahlt%s, sonst nichts. Wie groß ist der erwartete Gewinn pro Spiel?" % (e, g6, (", bei einer 5 bekommt man %d €" % g5) if g5 else ""),
                   eu(E), [eu(Fr(g6 + g5, 6)), eu(Fr(g6 + g5, 6) + e), eu(-E) if E else eu(Fr(1, 6))],
                   "Auszahlung im Mittel %s, minus Einsatz %d €: <b>%s</b>. %s" % (eu(Fr(g6 + g5, 6)), e, eu(E), "Auf lange Sicht verliert man." if E < 0 else ("Das Spiel ist fair." if E == 0 else "Auf lange Sicht gewinnt man.")))
    if kind == "rad":
        secs = R.choice([4, 5, 6, 8])
        vals = [R.choice([0, 0, 1, 2, 5, 10]) for _ in range(secs)]
        if len(set(vals)) < 2:
            return None
        E = Fr(sum(vals), secs)
        cnt = {}
        for v in vals:
            cnt[v] = cnt.get(v, 0) + 1
        desc = ", ".join("%d %s %d €" % (c, "Feld mit" if c == 1 else "Felder mit", v) for v, c in sorted(cnt.items()))
        return mcq("Ein Glücksrad hat %d gleich große Felder: %s. Wie viel Euro wird im Mittel pro Drehung ausgezahlt?" % (secs, desc), eu(E),
                   [eu(Fr(sum(cnt), len(cnt))) if Fr(sum(cnt), len(cnt)) != E else eu(E + 1), eu(max(vals)), eu(Fr(sum(vals), secs - 1)) if secs > 1 else eu(E * 2)],
                   "E = (%s) : %d = <b>%s</b>." % (" + ".join(str(v) for v in vals), secs, eu(E)))
    g = R.choice([1, 2, 3, 4, 5])
    v = R.choice([1, 2, 3])
    E = Fr(1, 4) * g * 2 + Fr(1, 2) * 0 - Fr(1, 4) * v
    return mcq("Zwei Münzen werden geworfen. Bei zweimal Kopf gewinnt man %d €, bei zweimal Zahl gewinnt man ebenfalls %d €, sonst verliert man %d €. Wie groß ist der Erwartungswert des Gewinns?" % (g, g, v * 2),
               eu(Fr(1, 2) * g - Fr(1, 2) * 2 * v), [eu(Fr(2 * g - 2 * v, 3)), eu(Fr(1, 4) * g - Fr(1, 2) * 2 * v), eu(Fr(1, 2) * g)],
               "P(gleich) = ½, P(verschieden) = ½: E = ½ %s %d − ½ %s %d = <b>%s</b>." % (MAL, g, MAL, 2 * v, eu(Fr(1, 2) * g - Fr(1, 2) * 2 * v)))


def fair():
    kind = R.choice(["ist", "einsatz", "einsatz", "aus"])
    if kind == "ist":
        e = R.choice([1, 2, 3])
        n = R.choice([4, 5, 6, 8, 10])
        a = R.choice([e * n, e * n - 1, e * n + 2, e * (n - 1)])
        E = Fr(a, n) - e
        ans = "fair" if E == 0 else ("nicht fair, zugunsten des Veranstalters" if E < 0 else "nicht fair, zugunsten der Spieler")
        return mcq("Bei einem Spiel zahlt man %d € Einsatz. Mit der Wahrscheinlichkeit 1/%d gewinnt man %d € (sonst nichts). Ist das Spiel fair?" % (e, n, a), "Es ist %s." % ans,
                   ["Es ist %s." % t for t in ["fair", "nicht fair, zugunsten des Veranstalters", "nicht fair, zugunsten der Spieler", "nicht zu entscheiden"] if t != ans][:3],
                   "Erwarteter Gewinn %d : %d − %d = %s: <b>%s</b>." % (a, n, e, eu(E), ans))
    if kind == "einsatz":
        n = R.choice([4, 5, 6, 8, 10, 20])
        a = R.choice([10, 20, 30, 40, 50, 100])
        k = R.choice([1, 1, 2, 3])
        if k >= n:
            return None
        E = Fr(a * k, n)
        return mcq("Ein Los gewinnt mit der Wahrscheinlichkeit %s den Betrag %d € (sonst nichts). Bei welchem Einsatz ist das Spiel fair?" % (zz(Fr(k, n)), a), eu(E),
                   [eu(Fr(a, 2)), eu(Fr(a * k, n) * 2), eu(Fr(a, n * k)) if k != 1 else eu(a - E)],
                   "Fair heißt: Einsatz = erwartete Auszahlung = %d %s %s = <b>%s</b>." % (a, MAL, zz(Fr(k, n)), eu(E)))
    e = R.choice([1, 2, 3, 5])
    n = R.choice([4, 5, 6, 8, 10])
    return mcq("Ein Spiel kostet %d € Einsatz. Mit der Wahrscheinlichkeit 1/%d bekommt man eine Auszahlung, sonst nichts. Wie hoch muss die Auszahlung sein, damit das Spiel fair ist?" % (e, n), "%d €" % (e * n),
               ["%d €" % (e * (n - 1)), "%d €" % (e + n), "%d €" % (e * n + e)], "1/%d %s A = %d € ⇒ <b>A = %d €</b>." % (n, MAL, e, e * n))


def sach():
    kind = R.choice(["lose", "lose", "vers", "lang", "ziehen", "zwei"])
    if kind == "lose":
        N = R.choice([100, 200, 500, 1000])
        prizes = [(R.choice([50, 100, 200]), 1), (R.choice([10, 20]), R.choice([2, 4, 5])), (R.choice([2, 5]), R.choice([10, 20, 25]))]
        price = R.choice([1, 2])
        tot = sum(p * c for p, c in prizes)
        E = Fr(tot, N) - price
        d = ", ".join("%d %s %d €" % (c, "Gewinn zu" if c == 1 else "Gewinne zu", p) for p, c in prizes)
        return mcq("Bei einer Tombola gibt es %s Lose zu je %d €. Es gibt %s; die übrigen Lose sind Nieten. Wie groß ist der erwartete Gewinn pro Los?" % (num(N), price, d), eu(E),
                   [eu(Fr(tot, N)), eu(Fr(tot, len(prizes)) - price), eu(-price)],
                   "Erwartete Auszahlung %s : %s = %s, minus %d € Lospreis: <b>%s</b>." % (num(tot), num(N), eu(Fr(tot, N)), price, eu(E)))
    if kind == "vers":
        p = R.choice([Fr(1, 100), Fr(1, 200), Fr(1, 50), Fr(2, 100)])
        S = R.choice([500, 1000, 2000, 3000])
        B = R.choice([25, 30, 40, 50, 60])
        E = B - p * S
        return mcq("Eine Fahrradversicherung kostet %d € im Jahr. Mit der Wahrscheinlichkeit %s wird ein Rad gestohlen; dann zahlt sie %s €. Wie viel nimmt die Versicherung im Mittel pro Vertrag ein?" % (B, zz(p), num(S)), eu(E),
                   [eu(B), eu(p * S), eu(B + p * S)], "E = %d − %s %s %s = <b>%s</b>." % (B, zz(p), MAL, num(S), eu(E)))
    if kind == "lang":
        e = R.choice([1, 2])
        n = R.choice([6, 8, 10])
        a = R.choice([e * n - 2, e * n - 4, e * n - 1]) if e * n > 4 else e * n - 1
        E = Fr(a, n) - e
        k = R.choice([50, 100, 200, 500])
        return mcq("Bei einem Spiel (Einsatz %d €) gewinnt man mit der Wahrscheinlichkeit 1/%d den Betrag %d €. Mit welchem Ergebnis kann man nach %d Spielen etwa rechnen?" % (e, n, a, k), eu(E * k),
                   [eu(Fr(a, n) * k), eu(-e * k), eu(E)], "Pro Spiel %s, also %d %s %s = <b>%s</b> (ungefähr, nicht sicher)." % (eu(E), k, MAL, "(%s)" % eu(E).replace("≈ ", "") if E < 0 else eu(E).replace("≈ ", ""), eu(E * k)))
    if kind == "ziehen":
        r = R.choice([2, 3, 4])
        b = R.choice([3, 4, 5, 6])
        g = R.choice([2, 4, 5, 10])
        P = Fr(r, r + b) * Fr(r - 1, r + b - 1)
        return mcq("In einer Urne liegen %d rote und %d blaue Kugeln. Man zieht zwei Kugeln ohne Zurücklegen. Sind beide rot, bekommt man %d €. Wie hoch ist die Auszahlung im Mittel?" % (r, b, g), eu(P * g),
                   [eu(Fr(r, r + b) ** 2 * g), eu(Fr(r, r + b) * g), eu(Fr(2 * r, r + b) * g / 2 + 1)],
                   "P(rot, rot) = %s %s %s = %s, E = %s %s %d = <b>%s</b>." % (bh(Fr(r, r + b)), MAL, bh(Fr(r - 1, r + b - 1)), bh(P), bh(P), MAL, g, eu(P * g)))
    k = R.choice([2, 3])
    E = Fr(k, 2)
    return mcq("%s Münzen werden geworfen. X ist die Anzahl der Wappen. Wie groß ist E(X)?" % ("Zwei" if k == 2 else "Drei"), zz(E),
               [zz(Fr(k + 1, 2)), zz(Fr(1, 2)), zz(k)],
               "Jede Münze trägt im Mittel ½ Wappen bei: E(X) = %d %s ½ = <b>%s</b>." % (k, MAL, zz(E)))


def main():
    seen = set()
    sets = [
        ("Wahrscheinlichkeitsverteilungen", mix(R, seen, [(verteilung, 20)])),
        ("Erwartungswert berechnen", mix(R, seen, [(erwartung, 20)])),
        ("Würfel, Glücksrad, Münzen", mix(R, seen, [(spiel, 20)])),
        ("Faire Spiele", mix(R, seen, [(fair, 20)])),
        ("Sachaufgaben", mix(R, seen, [(sach, 20)])),
    ]
    body = lesson(
        ["Eine <b>Zufallsgröße</b> X ordnet jedem Ergebnis eines Zufallsexperiments eine Zahl zu (z. B. den Gewinn). Die Wahrscheinlichkeiten aller Werte ergeben zusammen 1.",
         "Der <b>Erwartungswert</b> ist der gewichtete Mittelwert: E(X) = x₁ %s P(X = x₁) + x₂ %s P(X = x₂) + …" % (MAL, MAL),
         "Er gibt an, welchen Wert man <b>auf lange Sicht im Mittel</b> erhält – nicht, was bei einem Spiel sicher herauskommt.",
         "Ein Spiel ist <b>fair</b>, wenn der erwartete Gewinn (Auszahlung minus Einsatz) 0 ist."],
        [example("x: 0, 2, 5 mit P: 0,5; 0,3; 0,2", ["E = 0 %s 0,5 + 2 %s 0,3 + 5 %s 0,2" % (MAL, MAL, MAL)], "E = 1,6"),
         example("Einsatz 1 €, bei einer 6 gibt es 5 €", ["5 %s ⅙ − 1" % MAL], "≈ −0,17 € pro Spiel")],
        [["Mittelwert von 0, 2, 5 = 2,33", "mit den Wahrscheinlichkeiten gewichten"],
         ["Auszahlung = Gewinn", "Einsatz abziehen"],
         ["E = 1,6: Man bekommt immer 1,6", "Nur im Mittel bei vielen Durchgängen"]])
    faq = [
        {"q": "Was ist der Erwartungswert?", "a": "Der Wert, den eine Zufallsgröße auf lange Sicht im Mittel annimmt: Summe aus Wert mal Wahrscheinlichkeit."},
        {"q": "Wann ist ein Spiel fair?", "a": "Wenn der erwartete Gewinn 0 ist, also die mittlere Auszahlung gleich dem Einsatz."},
        {"q": "Muss der Erwartungswert ein möglicher Wert sein?", "a": "Nein. Beim Würfel ist E = 3,5, obwohl man nie 3,5 würfelt."},
        {"q": "Wie berechne ich einen fairen Einsatz?", "a": "Erwartete Auszahlung berechnen; genau dieser Betrag ist der faire Einsatz."},
    ]
    for _, items in sets:
        for it in items:
            it["e"] = it["e"].replace("= <b>≈ ", "≈ <b>").replace("= ≈ ", "≈ ")
    make_unit(R, "erwartungswert", "D",
              "Die Schülerinnen und Schüler beschreiben Zufallsexperimente mit Zufallsgrößen und Wahrscheinlichkeitsverteilungen, berechnen Erwartungswerte und beurteilen, ob Spiele fair sind (Zusammenfassung).",
              "Erwartungswert und faire Spiele",
              "Erwartungswert Klasse 10 – Zufallsgrößen, faire Spiele, Arbeitsblätter mit Lösungen",
              "Erwartungswert",
              "Erwartungswert für Klasse 10: Wahrscheinlichkeitsverteilungen, Erwartungswert berechnen, Würfel- und Glücksradspiele, faire Spiele und Sachaufgaben. 100 Aufgaben mit Lösungen, kostenlos.",
              "E(X) = x₁ · P(X = x₁) + x₂ · P(X = x₂) + …",
              "Fair: erwarteter Gewinn = 0.",
              body, faq, sets, 10, grade="klasse-10")


if __name__ == "__main__":
    main()
