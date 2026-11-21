# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 7: Prozentrechnung – Grundwert, Prozentwert, Prozentsatz（Leitidee Zahl und Operation, Sek I）
  python3 tools/gen_de_mathe_k7_prozentrechnung.py
Prozentwert W = G · p %, Prozentsatz p % = W : G, Grundwert G = W : p %, Dreisatz und Formel, Prozentstreifen, Sachaufgaben.
Fehler: Grundwert und Prozentwert vertauscht, durch p statt durch p/100 geteilt, Prozentsatz als W − G.
"""
import random
from fractions import Fraction as Fr
from de_common import lesson, example, make_unit, mix, Kids, MAL, table, wrap, line, text, INK, RED, GREEN, FILL
from de_k6 import dz
from de_k7 import mcq, eur, pz, P

R = random.Random(49703)
KIDS = Kids(R)
G = ":"
PS = [1, 2, 4, 5, 8, 10, 12, 15, 16, 20, 24, 25, 30, 35, 40, 45, 60, 64, 75, 80, 85, 90, 12.5, 2.5, 7.5, 150, 120]


def psatz():
    return Fr(R.choice(PS)).limit_denominator(10)


def gw():
    return R.choice([20, 40, 50, 60, 80, 120, 150, 160, 200, 240, 250, 300, 400, 480, 500, 600, 750, 800, 1200, 1500, 2000, 2400])


def wert():
    p, g = psatz(), gw()
    w = g * p / 100
    if (w * 100).denominator != 1:
        return None
    u = R.choice(["€", "kg", "m", "Schüler", "l"])
    f = (lambda x: eur(x)) if u == "€" else (lambda x: "%s %s" % (dz(x), u))
    q = "Berechne %s von %s." % (pz(p), f(g))
    return mcq(q, f(w), [f(g * 100 / p) if (g * 100 / p * 100).denominator == 1 else f(w * 10), f(g - w), f(g * p / 10) if g * p / 10 != w else f(w + 1)],
               "W = G %s p%s = %s %s %s = <b>%s</b>." % (MAL, P, f(g), MAL, dz(p / 100), f(w)))


def satz():
    p, g = psatz(), gw()
    w = g * p / 100
    if (w * 100).denominator != 1 or p >= 100 and R.random() < 0.6:
        return None
    th = R.choice(["Von %s Losen sind %s Gewinne." % (dz(g), dz(w)), "Von %s Euro werden %s Euro gespart." % (dz(g), dz(w)), "Von %s Befragten antworten %s mit Ja." % (dz(g), dz(w))])
    if "Befragten" in th or "Losen" in th:
        if w.denominator != 1:
            return None
    return mcq(th + " Wie viel Prozent sind das?", pz(p), [pz(w) if w != p else pz(p + 5), pz(Fr(g, w)) if w and (Fr(g, w) * 10).denominator in (1, 2, 5, 10) and Fr(g, w) != p else pz(100 - p) if p < 100 else pz(p - 10), pz(p / 10)],
               "p%s = W %s G = %s %s %s = %s = <b>%s</b>." % (P, G, dz(w), G, dz(g), dz(p / 100), pz(p)))


def grund():
    p, g = psatz(), gw()
    w = g * p / 100
    if (w * 100).denominator != 1 or p >= 100:
        return None
    u = R.choice(["€", "kg", "km"])
    f = (lambda x: eur(x)) if u == "€" else (lambda x: "%s %s" % (dz(x), u))
    return mcq("%s sind %s. Wie groß ist der Grundwert?" % (pz(p), f(w)), f(g), [f(w * p / 100) if (w * p / 100 * 100).denominator == 1 else f(w / 10), f(w + w * p / 100) if ((w + w * p / 100) * 100).denominator == 1 else f(g / 10), f(w * p) if w * p != g else f(g * 2)],
               "G = W %s p%s = %s %s %s = <b>%s</b>." % (G, P, f(w), G, dz(p / 100), f(g)))


def welches():
    p, g = psatz(), gw()
    w = g * p / 100
    if (w * 100).denominator != 1 or p >= 100:
        return None
    kind = R.choice(["G", "W", "p"])
    if kind == "G":
        q = "In der Aufgabe „%s von %s € sind %s €“: Welche Zahl ist der Grundwert?" % (pz(p), dz(g), dz(w))
        return mcq(q, "%s €" % dz(g), ["%s €" % dz(w), pz(p), "Es gibt keinen Grundwert."], "Der Grundwert ist das Ganze (100 %%): <b>%s €</b>." % dz(g))
    if kind == "W":
        q = "In der Aufgabe „%s von %s € sind %s €“: Welche Zahl ist der Prozentwert?" % (pz(p), dz(g), dz(w))
        return mcq(q, "%s €" % dz(w), ["%s €" % dz(g), pz(p), "%s €" % dz(g - w)], "Der Prozentwert ist der Anteil in Euro: <b>%s €</b>." % dz(w))
    q = "In der Aufgabe „%s von %s € sind %s €“: Welche Zahl ist der Prozentsatz?" % (pz(p), dz(g), dz(w))
    return mcq(q, pz(p), ["%s €" % dz(g), "%s €" % dz(w), pz(100 - p)], "Der Prozentsatz ist die Angabe in Prozent: <b>%s</b>." % pz(p))


def streifen():
    p = R.choice([10, 20, 25, 30, 40, 50, 60, 70, 75, 80, 90])
    g = R.choice([40, 80, 120, 200, 240, 400, 600])
    w = g * p // 100
    W = 400
    x = 20 + W * p / 100.0
    s = ["<rect x='20' y='30' width='%d' height='34' fill='#fff' stroke='%s' stroke-width='2'/>" % (W, INK),
         "<rect x='20' y='30' width='%.1f' height='34' fill='%s' stroke='%s' stroke-width='2'/>" % (W * p / 100.0, FILL, GREEN),
         text(20, 22, "0", 12) + text(20 + W, 22, "100%", 12) + text(x, 22, "%d%%" % p, 12, col=RED),
         text(20, 86, "0", 12) + text(20 + W, 86, "%d" % g, 12) + text(x, 86, "?", 14, col=RED)]
    pic = wrap(W + 40, 96, "".join(s), "Prozentstreifen", lg=True)
    return mcq(pic + "Der Prozentstreifen zeigt %d%s von %d. Welche Zahl gehört zum Fragezeichen?" % (p, P, g), str(w), [str(g - w), str(p), str(g * 100 // p) if g * 100 % p == 0 else str(w + 10)],
               "%d%s von %d = %d %s %s = <b>%d</b>." % (p, P, g, g, MAL, dz(Fr(p, 100)), w))


def sache():
    p_, er = KIDS.next()
    kind = R.choice(["mwst", "wahl", "test", "fett", "gehalt", "schule"])
    if kind == "mwst":
        n = R.choice([100, 200, 250, 400, 500, 800])
        return mcq("Ein Fahrrad kostet ohne Mehrwertsteuer %d €. Wie viel Euro Mehrwertsteuer (19%s) kommen dazu?" % (n, P), eur(Fr(n * 19, 100)), [eur(Fr(n * 119, 100)), eur(19), eur(Fr(n * 19, 10))],
                   "19%s von %d € = %d %s 0,19 = <b>%s</b>." % (P, n, n, MAL, eur(Fr(n * 19, 100))))
    if kind == "wahl":
        g = R.choice([400, 500, 800, 1200])
        w = g * R.choice([15, 20, 30, 35, 45, 55]) // 100
        return mcq("Bei der Schülersprecherwahl gaben %d Schülerinnen und Schüler ihre Stimme ab. Lena bekam %d Stimmen. Wie viel Prozent sind das?" % (g, w), pz(Fr(w * 100, g)), [pz(Fr(w, 10)), pz(100 - Fr(w * 100, g)), "%d%s" % (w // 2, P)],
                   "%d %s %d = %s = <b>%s</b>." % (w, G, g, dz(Fr(w, g)), pz(Fr(w * 100, g))))
    if kind == "test":
        g = R.choice([40, 50, 60, 80])
        p = R.choice([60, 75, 80, 85, 90, 95, 70, 65])
        if g * p % 100:
            return None
        w = g * p // 100
        return mcq("Für eine Eins braucht man %d%s der Punkte. Der Test hat %d Punkte. Wie viele Punkte braucht man mindestens?" % (p, P, g), str(w), [str(g - w), str(p), str(w + 5)],
                   "%d%s von %d = <b>%d</b> Punkte." % (p, P, g, w))
    if kind == "fett":
        g = R.choice([125, 150, 200, 250, 400, 500])
        p = R.choice([4, 8, 10, 12, 20, 30])
        w = Fr(g * p, 100)
        return mcq("Ein Joghurt (%d g) enthält %d%s Fett. Wie viel Gramm Fett sind das?" % (g, p, P), "%s g" % dz(w), ["%s g" % dz(x) for x in (Fr(g * 100, p), g - w, Fr(g * p, 10))],
                   "%d g %s %s = <b>%s g</b>." % (g, MAL, dz(Fr(p, 100)), dz(w)))
    if kind == "gehalt":
        w = R.choice([45, 60, 90, 120, 150])
        p = R.choice([3, 5, 10, 15])
        g = Fr(w * 100, p)
        return mcq("%s bekommt %d%s mehr Taschengeld. Das sind %d € im Jahr mehr. Wie viel Taschengeld bekam %s vorher im Jahr?" % (p_, p, P, w, er), eur(g), [eur(Fr(w * p, 100)), eur(w + Fr(w * p, 100)), eur(g / 10)],
                   "G = %d € %s %s = <b>%s</b>." % (w, G, dz(Fr(p, 100)), eur(g)))
    g = R.choice([600, 750, 800, 900, 1200])
    p = R.choice([12, 15, 20, 24, 30, 36])
    w = g * p // 100
    return mcq("An einer Schule mit %d Schülerinnen und Schülern kommen %d%s mit dem Bus. Wie viele kommen <b>nicht</b> mit dem Bus?" % (g, p, P), str(g - w), [str(w), str(g - p), str(g * (100 - p) // 10)],
               "%d%s fahren nicht mit dem Bus: %d %s %s = <b>%d</b>." % (100 - p, P, g, MAL, dz(Fr(100 - p, 100)), g - w))


def main():
    seen = set()
    sets = [
        ("Grundwert, Prozentwert oder Prozentsatz?", mix(R, seen, [(welches, 8), (streifen, 12)])),
        ("Prozentwert berechnen", mix(R, seen, [(wert, 20)])),
        ("Prozentsatz berechnen", mix(R, seen, [(satz, 20)])),
        ("Grundwert berechnen", mix(R, seen, [(grund, 20)])),
        ("Sachaufgaben", mix(R, seen, [(sache, 20)])),
    ]
    body = lesson(
        ["Der <b>Grundwert</b> G ist das Ganze (100 %). Der <b>Prozentwert</b> W ist der Anteil davon. Der <b>Prozentsatz</b> p % sagt, wie groß der Anteil in Prozent ist.",
         "Prozentwert: W = G %s p%%. Prozentsatz: p%% = W %s G. Grundwert: G = W %s p%%." % (MAL, G, G),
         "Man kann auch mit dem <b>Dreisatz</b> rechnen: 100 %% ≙ G, 1 %% ≙ G %s 100, p %% ≙ …" % G,
         "Prozentsätze rechnet man als Dezimalzahl: 15 % = 0,15."],
        [example("18 % von 250 €", ["250 %s 0,18" % MAL], "45 €"),
         example("36 € sind 12 %. Grundwert?", ["36 %s 0,12" % G], "300 €")],
        [["Grundwert und Prozentwert verwechselt", "Der Grundwert ist immer das Ganze (100 %)"],
         ["36 € : 12 = 3 € (Grundwert)", "Durch 0,12 teilen: 300 €"],
         ["Prozentsatz = W − G", "Prozentsatz = W : G"]])
    faq = [
        {"q": "Was ist der Unterschied zwischen Grundwert und Prozentwert?", "a": "Der Grundwert ist das Ganze (100 %). Der Prozentwert ist der Teil davon, der zum Prozentsatz gehört."},
        {"q": "Wie berechne ich den Prozentsatz?", "a": "Prozentwert durch Grundwert: p % = W : G. Zum Beispiel 30 von 120 = 0,25 = 25 %."},
        {"q": "Wie berechne ich den Grundwert?", "a": "Prozentwert durch Prozentsatz: G = W : p %. Zum Beispiel 45 € sind 15 %: 45 : 0,15 = 300 €."},
        {"q": "Kann ich auch mit dem Dreisatz rechnen?", "a": "Ja. Man schließt zuerst auf 1 % und dann auf den gesuchten Wert."},
    ]
    make_unit(R, "prozentrechnung", "Z",
              "Die Schülerinnen und Schüler unterscheiden Grundwert, Prozentwert und Prozentsatz, berechnen sie mit Formel und Dreisatz und lösen Sachaufgaben aus dem Alltag (Zusammenfassung).",
              "Prozentrechnung: Grundwert, Prozentwert, Prozentsatz",
              "Prozentrechnung Klasse 7 – Grundwert, Prozentwert, Prozentsatz, Arbeitsblätter",
              "Prozentrechnung",
              "Prozentrechnung für Klasse 7: Prozentwert, Prozentsatz und Grundwert berechnen, Prozentstreifen und Sachaufgaben. 100 Aufgaben mit Lösungen, kostenlos.",
              "W = G · p %",
              "Grundwert = das Ganze = 100 %.",
              body, faq, sets, 3, grade="klasse-7")


if __name__ == "__main__":
    main()
