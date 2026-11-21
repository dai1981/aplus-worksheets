# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 7: Wahrscheinlichkeit（Leitidee Daten und Zufall, Sek I）
  python3 tools/gen_de_mathe_k7_wahrscheinlichkeit.py
Laplace-Wahrscheinlichkeit, Gegenereignis, zwei Würfel und Münzen, zweistufige Zufallsexperimente mit Baumdiagramm,
Pfadregel (Multiplikation), Summenregel (Addition), Ziehen mit und ohne Zurücklegen, relative Häufigkeit und erwartete Anzahl.
Fehler: Wahrscheinlichkeiten entlang eines Pfades addiert, ohne Zurücklegen den Nenner nicht verkleinert, Augensumme 7 mit 1/11.
"""
import random
from fractions import Fraction as Fr
from de_common import lesson, example, make_unit, mix, Kids, fr, MAL, wrap, line, text, INK, BLUE
from de_k6 import bh, dz, endlich
from de_k7 import mcq

R = random.Random(49717)
KIDS = Kids(R)
G = ":"
P = " %"


def pz(v):
    return dz(v * 100) + P


def laplace():
    kind = R.choice(["wuerfel", "karten", "gegen", "gegen_p"])
    if kind == "wuerfel":
        D = [("eine Zahl größer als 2", 4), ("eine ungerade Zahl", 3), ("eine Quadratzahl (1 oder 4)", 2), ("eine Zahl kleiner als 3", 2), ("keine 6", 5), ("eine Primzahl", 3)]
        ev, g = R.choice(D)
        v = Fr(g, 6)
        return mcq("Ein fairer Würfel wird geworfen. P(%s) = ?" % ev, bh(v), [fr(g, 6 - g), bh(1 - v) if 1 - v != v else fr(1, 6), fr(1, 6) if v != Fr(1, 6) else fr(1, 3)],
                   "%d günstige von 6 Ergebnissen: <b>%s</b>." % (g, bh(v)))
    if kind == "karten":
        n = R.choice([10, 20, 30, 40, 50])
        art, g = R.choice([("eine gerade Zahl", n // 2), ("eine durch 5 teilbare Zahl", n // 5), ("eine durch 10 teilbare Zahl", n // 10), ("eine Zahl größer als %d" % (n - 3), 3)])
        v = Fr(g, n)
        return mcq("Auf %d Karten stehen die Zahlen 1 bis %d. Eine Karte wird blind gezogen. Wie groß ist die Wahrscheinlichkeit für %s?" % (n, n, art), bh(v),
                   [fr(g, n - g), bh(1 - v) if 1 - v != v else fr(1, n), fr(1, n) if Fr(1, n) != v else fr(2, n)],
                   "%d günstige von %d Karten: %s = <b>%s</b>." % (g, n, fr(g, n), bh(v)))
    if kind == "gegen":
        p = R.choice([5, 12, 15, 25, 30, 35, 40, 45, 62, 85])
        ev = R.choice(["Regen morgen", "einen Treffer beim Elfmeter", "einen Gewinn am Losstand", "eine Verspätung des Busses"])
        return mcq("Die Wahrscheinlichkeit für %s beträgt %d %%. Wie groß ist die Wahrscheinlichkeit für das Gegenereignis?" % (ev, p), "%d%s" % (100 - p, P),
                   ["%d%s" % (p, P), "%d%s" % (100 - p + 10 if 100 - p + 10 <= 100 else 100 - p - 10, P), "%d%s" % (abs(100 - 2 * p), P) if p != 50 and abs(100 - 2 * p) not in (p, 100 - p) else "50" + P],
                   "P(Gegenereignis) = 100 %% − %d %% = <b>%d %%</b>." % (p, 100 - p))
    z, n = R.choice([(1, 4), (2, 5), (3, 8), (5, 12), (1, 6), (4, 9), (3, 10), (7, 20)])
    v = Fr(z, n)
    return mcq("P(E) = %s. Berechne P(Ē), die Wahrscheinlichkeit des Gegenereignisses." % fr(z, n), bh(1 - v), [fr(z, n - z), fr(n, z), fr(n - z, n + z)],
               "P(Ē) = 1 − %s = <b>%s</b>." % (fr(z, n), bh(1 - v)))


def zwei():
    kind = R.choice(["summe", "summe", "pasch", "muenzen", "muenzen3", "anzahl"])
    if kind == "summe":
        s = R.choice([2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
        g = 6 - abs(7 - s)
        v = Fr(g, 36)
        w = [fr(1, 11), bh(Fr(g, 12)) if Fr(g, 12) != v else bh(Fr(g, 18)), bh(Fr(g + 1, 36)) if g < 6 else fr(5, 36), fr(1, 36) if g != 1 else fr(2, 36)]
        paare = ", ".join("(%d|%d)" % (a, s - a) for a in range(1, 7) if 1 <= s - a <= 6)
        return mcq("Zwei faire Würfel werden geworfen. Wie groß ist die Wahrscheinlichkeit für die Augensumme %d?" % s, bh(v), w,
                   "36 gleich wahrscheinliche Paare. Günstig: %s – also %d. %s = <b>%s</b>." % (paare, g, fr(g, 36), bh(v)))
    if kind == "pasch":
        return mcq("Zwei faire Würfel werden geworfen. Wie groß ist die Wahrscheinlichkeit für einen Pasch (zwei gleiche Zahlen)?", fr(1, 6), [fr(1, 36), fr(6, 12), fr(1, 12)],
                   "6 Paare (1|1) bis (6|6) von 36: %s = <b>%s</b>." % (fr(6, 36), fr(1, 6)))
    if kind == "muenzen":
        ev, g = R.choice([("zweimal Kopf", 1), ("einmal Kopf und einmal Zahl", 2), ("mindestens einmal Kopf", 3), ("keinmal Kopf", 1)])
        return mcq("Eine Münze wird zweimal geworfen. P(%s) = ?" % ev, bh(Fr(g, 4)), [fr(1, 3), fr(1, 2) if g != 2 else fr(1, 4), fr(3, 4) if g != 3 else fr(2, 3)],
                   "Ergebnisse: KK, KZ, ZK, ZZ. Günstig: %d von 4 = <b>%s</b>." % (g, bh(Fr(g, 4))))
    if kind == "muenzen3":
        ev, g = R.choice([("dreimal Kopf", 1), ("genau einmal Kopf", 3), ("mindestens einmal Zahl", 7), ("genau zweimal Zahl", 3)])
        return mcq("Eine Münze wird dreimal geworfen. P(%s) = ?" % ev, bh(Fr(g, 8)), [fr(1, 3) if g != 1 else fr(1, 6), fr(g, 6), fr(1, 2)],
                   "2 %s 2 %s 2 = 8 gleich wahrscheinliche Ergebnisse, günstig sind %d: <b>%s</b>." % (MAL, MAL, g, bh(Fr(g, 8))))
    a, b = R.choice([(6, 6), (2, 6), (6, 4), (2, 2), (4, 6), (6, 8), (2, 4)])
    na = {6: "einen Würfel", 2: "eine Münze", 4: "einen Tetraeder-Würfel (1 bis 4)", 8: "einen Oktaeder-Würfel (1 bis 8)"}
    if a == b:
        txt = {6: "zwei Würfel", 2: "zwei Münzen"}[a]
    else:
        txt = "%s und %s" % (na[a], na[b])
    return mcq("Man wirft %s. Wie viele mögliche Ergebnisse gibt es?" % txt, str(a * b), [str(a + b), str(a * b // 2) if a * b // 2 != a + b else str(a * b + 2), str(max(a, b))],
               "Zählprinzip: %d %s %d = <b>%d</b>." % (a, MAL, b, a * b))


def tree_svg(p1, labels, p2=None, title="Baumdiagramm"):
    """zweistufig; p1: [(name, wahrsch.)], p2: dict name -> [(name, w)] (None = wie p1)"""
    W, H = 290, 140
    s = []
    x0, x1, x2 = 8, 118, 262
    n1 = len(p1)
    ys1 = [H * (i + 0.5) / n1 for i in range(n1)]
    k = 0
    tot = sum(len((p2 or {}).get(a, p1)) for a, _ in p1)
    for i, (a, pa) in enumerate(p1):
        s.append(line(x0, H / 2, x1, ys1[i], INK, 1.6))
        s.append(text((x0 + x1) / 2 - 8, (H / 2 + ys1[i]) / 2 + (-6 if ys1[i] < H / 2 else 18), pa, 15, weight=600))
        s.append(text(x1 + 12, ys1[i] + 5, a, 17, weight=700))
        for (b, pb) in (p2 or {}).get(a, p1):
            y = H * (k + 0.5) / tot
            k += 1
            s.append(line(x1 + 26, ys1[i], x2, y, INK, 1.4))
            s.append(text((x1 + 26 + x2) / 2, (ys1[i] + y) / 2 + (-6 if y < ys1[i] else 16), pb, 14, weight=600))
            s.append(text(x2 + 14, y + 5, b, 16, weight=700))
    return wrap(W, H, "".join(s), title, lg=True)


def plain(f):
    return "%d/%d" % (f.numerator, f.denominator) if f.denominator != 1 else str(f.numerator)


def pfad():
    """mit Zurücklegen"""
    r = R.randint(1, 6)
    b = R.randint(1, 6)
    t = r + b
    pr, pb = Fr(r, t), Fr(b, t)
    kind = R.choice(["rr", "bb", "rb_einmal", "rr", "mind"])
    pic = tree_svg([("r", plain(pr)), ("b", plain(pb))], None)
    intro = "In einer Urne liegen %d rote (r) und %d blaue (b) Kugeln. Es wird zweimal <b>mit Zurücklegen</b> gezogen. " % (r, b)
    if kind == "rr":
        v = pr * pr
        return mcq(pic + intro + "Wie groß ist P(rot, rot)?", bh(v), [bh(pr + pr) if pr + pr <= 1 else bh(Fr(r, 2 * t)), bh(pr), bh(Fr(r * r, t + t)) if Fr(r * r, 2 * t) <= 1 else bh(Fr(r, t * t))],
                   "Pfadregel: Wahrscheinlichkeiten entlang des Pfades multiplizieren: %s %s %s = <b>%s</b>." % (fr(r, t), MAL, fr(r, t), bh(v)))
    if kind == "bb":
        v = pb * pb
        return mcq(pic + intro + "Wie groß ist P(blau, blau)?", bh(v), [bh(pb + pb) if pb + pb <= 1 else bh(Fr(b, 2 * t)), bh(pb), bh(Fr(b, t * t))],
                   "Pfadregel: %s %s %s = <b>%s</b>." % (fr(b, t), MAL, fr(b, t), bh(v)))
    if kind == "rb_einmal":
        v = 2 * pr * pb
        return mcq(pic + intro + "Wie groß ist die Wahrscheinlichkeit, genau eine rote Kugel zu ziehen?", bh(v), [bh(pr * pb), bh(pr + pb) if pr + pb != v else fr(1, 2), bh(pr)],
                   "Zwei Pfade: (r, b) und (b, r). Summenregel: %s %s %s + %s %s %s = <b>%s</b>." % (fr(r, t), MAL, fr(b, t), fr(b, t), MAL, fr(r, t), bh(v)))
    v = 1 - pb * pb
    return mcq(pic + intro + "Wie groß ist die Wahrscheinlichkeit, mindestens eine rote Kugel zu ziehen?", bh(v), [bh(pr * pr), bh(pb * pb), bh(2 * pr * pb) if 2 * pr * pb != v else bh(pr)],
               "Gegenereignis „keine rote“ = (b, b): %s. 1 − %s = <b>%s</b>." % (bh(pb * pb), bh(pb * pb), bh(v)))


def ohne():
    r = R.randint(2, 6)
    b = R.randint(2, 6)
    t = r + b
    kind = R.choice(["rr", "bb", "eins", "zweite"])
    p2 = {"r": [("r", plain(Fr(r - 1, t - 1))), ("b", plain(Fr(b, t - 1)))], "b": [("r", plain(Fr(r, t - 1))), ("b", plain(Fr(b - 1, t - 1)))]}
    pic = tree_svg([("r", plain(Fr(r, t))), ("b", plain(Fr(b, t)))], p2)
    intro = "In einem Beutel sind %d rote (r) und %d blaue (b) Bonbons. %s nimmt nacheinander zwei Bonbons <b>ohne Zurücklegen</b>. " % (r, b, KIDS.next()[0])
    if kind == "rr":
        v = Fr(r * (r - 1), t * (t - 1))
        return mcq(pic + intro + "Wie groß ist P(rot, rot)?", bh(v), [bh(Fr(r * r, t * t)), bh(Fr(r * (r - 1), t * t)), bh(Fr(r, t) + Fr(r - 1, t - 1)) if Fr(r, t) + Fr(r - 1, t - 1) <= 1 else bh(Fr(r - 1, t))],
                   "Beim zweiten Zug ist ein rotes weniger und eines weniger insgesamt: %s %s %s = <b>%s</b>." % (fr(r, t), MAL, fr(r - 1, t - 1), bh(v)))
    if kind == "bb":
        v = Fr(b * (b - 1), t * (t - 1))
        return mcq(pic + intro + "Wie groß ist P(blau, blau)?", bh(v), [bh(Fr(b * b, t * t)), bh(Fr(b * (b - 1), t * t)), bh(Fr(b, t))],
                   "%s %s %s = <b>%s</b>." % (fr(b, t), MAL, fr(b - 1, t - 1), bh(v)))
    if kind == "eins":
        v = Fr(2 * r * b, t * (t - 1))
        return mcq(pic + intro + "Wie groß ist die Wahrscheinlichkeit für zwei verschiedene Farben?", bh(v), [bh(Fr(r * b, t * (t - 1))), bh(Fr(2 * r * b, t * t)), bh(Fr(1, 2)) if v != Fr(1, 2) else bh(Fr(r * b, t * t))],
                   "(r, b) + (b, r) = %s %s %s + %s %s %s = <b>%s</b>." % (fr(r, t), MAL, fr(b, t - 1), fr(b, t), MAL, fr(r, t - 1), bh(v)))
    v = Fr(r - 1, t - 1)
    return mcq(pic + intro + "Das erste Bonbon war rot. Wie groß ist die Wahrscheinlichkeit, dass auch das zweite rot ist?", bh(v), [bh(Fr(r, t)), bh(Fr(r - 1, t)), bh(Fr(r, t - 1)) if Fr(r, t - 1) <= 1 and Fr(r, t - 1) != v else bh(Fr(b, t - 1))],
               "Übrig sind %d rote von %d Bonbons: <b>%s</b>." % (r - 1, t - 1, bh(v)))


def sache():
    kind = R.choice(["erwartet", "erwartet_w", "relativ", "spiel", "los", "elfmeter"])
    if kind == "erwartet":
        n = R.choice([60, 120, 180, 300, 600])
        ev, g = R.choice([("eine 6", 1), ("eine gerade Zahl", 3), ("eine Zahl größer als 4", 2)])
        e = n * g // 6
        return mcq("Ein fairer Würfel wird %d-mal geworfen. Wie oft erwartet man etwa %s?" % (n, ev), "etwa %d-mal" % e, ["etwa %d-mal" % (n // 6) if n // 6 != e else "etwa %d-mal" % (n // 2), "etwa %d-mal" % (n - e), "genau %d-mal" % e],
                   "Erwartete Anzahl = n %s P = %d %s %s = <b>%d</b>. „Genau“ kann man es nicht sagen." % (MAL, n, MAL, fr(g, 6), e))
    if kind == "erwartet_w":
        p = R.choice([5, 10, 15, 20, 25, 40])
        n = R.choice([200, 400, 500, 800, 1000])
        e = n * p // 100
        thing = R.choice(["Lose sind Gewinne", "Glühbirnen sind defekt", "Äpfel haben eine Druckstelle"])
        return mcq("Erfahrungsgemäß sind %d %% der %s. Wie viele erwartet man unter %d Stück?" % (p, {"Lose sind Gewinne": "Lose Gewinne", "Glühbirnen sind defekt": "Glühbirnen defekt", "Äpfel haben eine Druckstelle": "Äpfel mit Druckstelle"}[thing], n),
                   str(e), [str(n - e), str(p), str(e * 2) if e * 2 < n - e else str(e + n // 10)],
                   "%d %% von %d = %s %s %d = <b>%d</b>." % (p, n, dz(Fr(p, 100)), MAL, n, e))
    if kind == "relativ":
        n = R.choice([50, 80, 200, 250, 400])
        h = R.randint(n // 10, n // 2)
        v = Fr(h, n)
        if not endlich(v) or 2 * h == n:
            return None
        name, _ = KIDS.next()
        return mcq("%s wirft eine Reißzwecke %d-mal. Sie landet %d-mal auf dem Kopf. Schätze die Wahrscheinlichkeit für „Kopf“." % (name, n, h), pz(v), [pz(1 - v), "%d%s" % (h, P), "50" + P if v != Fr(1, 2) else "25" + P],
                   "Relative Häufigkeit %d %s %d = %s = <b>%s</b>. Bei vielen Würfen ist das ein guter Schätzwert." % (h, G, n, dz(v), pz(v)))
    if kind == "spiel":
        return mcq("Bei einem Spiel gewinnt man, wenn man mit zwei Würfeln eine Augensumme von mindestens 10 wirft. Wie groß ist die Gewinnwahrscheinlichkeit?", fr(1, 6), [fr(3, 11), fr(1, 12), fr(5, 36)],
                   "Summe 10: 3 Paare, 11: 2 Paare, 12: 1 Paar. 6 von 36 = <b>%s</b>." % fr(1, 6))
    if kind == "los":
        n = R.choice([100, 200, 250, 500])
        g = R.choice([5, 10, 20, 25, 40, 50])
        if g >= n // 2:
            return None
        v = Fr(g, n)
        return mcq("In einer Lostrommel sind %d Lose, davon %d Gewinne. Man zieht zwei Lose nacheinander ohne Zurücklegen. Wie groß ist die Wahrscheinlichkeit für zwei Nieten?" % (n, g),
                   bh(Fr(n - g, n) * Fr(n - g - 1, n - 1)), [bh(Fr(n - g, n) ** 2), bh(Fr(g, n) * Fr(g - 1, n - 1)), bh(Fr(n - g, n))],
                   "Nieten: %d. %s %s %s = <b>%s</b>." % (n - g, fr(n - g, n), MAL, fr(n - g - 1, n - 1), bh(Fr(n - g, n) * Fr(n - g - 1, n - 1))))
    p = R.choice([60, 70, 75, 80, 90])
    q = Fr(p, 100)
    name, er = KIDS.next()
    v = q * q
    kind2 = R.choice(["beide", "keiner"])
    if kind2 == "beide":
        return mcq("%s trifft beim Elfmeter mit einer Wahrscheinlichkeit von %d %%. %s schießt zweimal. Wie groß ist die Wahrscheinlichkeit, beide Male zu treffen?" % (name, p, er.capitalize()),
                   pz(v), ["%d%s" % (2 * p, P) if 2 * p <= 100 else "%d%s" % (p, P), "%d%s" % (p, P) if 2 * p <= 100 else pz(1 - v), pz(q * (1 - q))],
                   "%s %s %s = <b>%s</b>." % (dz(q), MAL, dz(q), pz(v)))
    w = (1 - q) * (1 - q)
    return mcq("%s trifft beim Elfmeter mit einer Wahrscheinlichkeit von %d %%. %s schießt zweimal. Wie groß ist die Wahrscheinlichkeit, keinmal zu treffen?" % (name, p, er.capitalize()),
               pz(w), [pz(1 - q), pz(1 - v), "%d%s" % (2 * (100 - p), P)],
               "Fehlschuss: %s. %s %s %s = <b>%s</b>." % (dz(1 - q), dz(1 - q), MAL, dz(1 - q), pz(w)))


def main():
    seen = set()
    sets = [
        ("Laplace und Gegenereignis", mix(R, seen, [(laplace, 20)])),
        ("Zwei Würfel und Münzen", mix(R, seen, [(zwei, 20)])),
        ("Pfadregel mit Zurücklegen", mix(R, seen, [(pfad, 20)])),
        ("Ohne Zurücklegen", mix(R, seen, [(ohne, 20)])),
        ("Sachaufgaben", mix(R, seen, [(sache, 20)])),
    ]
    body = lesson(
        ["<b>Laplace</b>: alle Ergebnisse gleich wahrscheinlich → P(E) = Anzahl günstige %s Anzahl mögliche." % G,
         "<b>Gegenereignis</b> Ē: P(Ē) = 1 − P(E).",
         "Zweistufige Experimente zeichnet man als <b>Baumdiagramm</b>. <b>Pfadregel</b>: entlang eines Pfades multiplizieren. <b>Summenregel</b>: mehrere Pfade addieren.",
         "<b>Ohne Zurücklegen</b> ändern sich beim zweiten Zug Zähler und Nenner.",
         "Bei vielen Wiederholungen nähert sich die relative Häufigkeit der Wahrscheinlichkeit. Erwartete Anzahl = n %s P." % MAL],
        [example("2 rote, 3 blaue Kugeln, zweimal mit Zurücklegen: P(r, r)", ["%s %s %s" % (fr(2, 5), MAL, fr(2, 5))], fr(4, 25)),
         example("dasselbe ohne Zurücklegen", ["%s %s %s" % (fr(2, 5), MAL, fr(1, 4))], fr(1, 10)),
         example("zwei Würfel, Augensumme 7", ["(1|6), (2|5), (3|4), (4|3), (5|2), (6|1)", "6 von 36"], fr(1, 6))],
        [["Entlang eines Pfades addieren", "Entlang eines Pfades multiplizieren"],
         ["Ohne Zurücklegen wie mit Zurücklegen rechnen", "Beim zweiten Zug ist eine Kugel weniger da"],
         ["Augensumme 7 hat P = 1/11 (11 Summen)", "Die 11 Summen sind nicht gleich wahrscheinlich: 36 Paare zählen"]])
    faq = [
        {"q": "Was ist die Pfadregel?", "a": "Die Wahrscheinlichkeit eines Pfades im Baumdiagramm ist das Produkt der Wahrscheinlichkeiten entlang des Pfades."},
        {"q": "Was ist die Summenregel?", "a": "Gehören mehrere Pfade zu einem Ereignis, addiert man ihre Wahrscheinlichkeiten."},
        {"q": "Was ändert sich ohne Zurücklegen?", "a": "Beim zweiten Zug ist eine Kugel weniger in der Urne. Nenner und eventuell Zähler werden um 1 kleiner."},
        {"q": "Wie berechnet man das Gegenereignis?", "a": "P(Ē) = 1 − P(E). Das hilft oft bei „mindestens einmal“."},
    ]
    make_unit(R, "wahrscheinlichkeit", "D",
              "Die Schülerinnen und Schüler bestimmen Laplace-Wahrscheinlichkeiten und Wahrscheinlichkeiten von Gegenereignissen, stellen zweistufige Zufallsexperimente in Baumdiagrammen dar und wenden Pfad- und Summenregel an; sie schätzen Wahrscheinlichkeiten über relative Häufigkeiten (Zusammenfassung).",
              "Wahrscheinlichkeit und Baumdiagramme",
              "Wahrscheinlichkeit Klasse 7 – Baumdiagramm und Pfadregel, Arbeitsblätter",
              "Wahrscheinlichkeit",
              "Wahrscheinlichkeit für Klasse 7: Laplace, Gegenereignis, zwei Würfel, Baumdiagramm, Pfad- und Summenregel, mit und ohne Zurücklegen. 100 Aufgaben mit Lösungen, kostenlos.",
              "Entlang eines Pfades multiplizieren, Pfade addieren.",
              "Pfadregel und Summenregel im Baumdiagramm; P(Ē) = 1 − P(E).",
              body, faq, sets, 17, grade="klasse-7")


if __name__ == "__main__":
    main()
