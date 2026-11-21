# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 1: Muster und Zahlenfolgen（Leitidee Muster, Strukturen und funktionaler Zusammenhang）
  python3 tools/gen_de_mathe_k1_muster_und_zahlenfolgen.py
Formenmuster fortsetzen, Zahlenfolgen vorwärts und rückwärts bis 20, kleine Zahlenmauern, wachsende Türme.
Formenmuster und Zahlenmauer-Bild kommen aus Klasse 2 und 3 (mit eigenem Zufall).
Fehler: Muster um ein Glied verschoben, Regel nur an zwei Zahlen geprüft, in der Zahlenmauer alle Steine addiert.
"""
import random
from de_common import mcq, lesson, example, make_unit, mix
from de_k2 import de
from k_pics import towers_svg
import gen_de_mathe_k2_zahlenmauern_und_muster as k2
from gen_de_mathe_k3_zahlenfolgen_und_muster import mauer_svg

R = random.Random(49416)
k2.R = random.Random(49466)


def vor():
    d = R.choice([1, 2, 2, 3, 5, 10])
    s = R.randint(0, 20 - 4 * d)
    seq = [s + d * i for i in range(5)]
    if seq[-1] > 20:
        return None
    k = R.choice([4, 4, 2, 3])
    shown = [str(x) if i != k else "?" for i, x in enumerate(seq)]
    ans = seq[k]
    return mcq("Welche Zahl fehlt? %s" % ", ".join(shown), str(ans), [str(x) for x in (ans + 1, ans - 1, ans + d) if 0 <= x <= 25 and x != ans][:3] + ([str(ans + 2)] if d != 2 else [str(ans - 2)]),
               "Es geht immer %d weiter: <b>%d</b>." % (d, ans))


def rueck():
    d = R.choice([1, 1, 2, 3, 5])
    s = R.randint(4 * d, 20)
    seq = [s - d * i for i in range(5)]
    ans = seq[4]
    return mcq("Wie geht es weiter? %s, ?" % ", ".join(map(str, seq[:4])), str(ans), [str(x) for x in (ans + 1, ans - 1, seq[3] + d, ans + 2) if x >= 0 and x != ans],
               "Es geht immer %d zurück: %d − %d = <b>%d</b>." % (d, seq[3], d, ans))


def mauer():
    a, b, c = R.randint(1, 6), R.randint(1, 6), R.randint(1, 6)
    m1, m2 = a + b, b + c
    top = m1 + m2
    if top > 20:
        return None
    kind = R.choice(["oben", "oben", "mitte"])
    if kind == "oben":
        return mcq(mauer_svg([[a, b, c], [m1, m2], [None]]) + "Welche Zahl gehört in den obersten Stein?", str(top), [str(a + b + c), str(top + 1), str(top - 1)],
                   "Zwei Steine nebeneinander ergeben den Stein darüber: %d + %d = <b>%d</b>." % (m1, m2, top))
    return mcq(mauer_svg([[a, b, c], [None, m2], [top]]) + "Welche Zahl gehört in den linken Stein in der Mitte?", str(m1), [str(top + m2) if top + m2 <= 30 else str(m1 + 2), str(m1 + 1), str(a)],
               "%d + %d = <b>%d</b>. Probe: %d + %d = %d." % (a, b, m1, m1, m2, top))


def tuerme():
    s, d = R.randint(1, 3), R.randint(1, 2)
    hs = [s + d * i for i in range(3)]
    if hs[-1] + d > 9:
        return None
    pic = de(towers_svg(hs, labels=["1", "2", "3"]), "drei Türme mit %s Würfeln" % ", ".join(map(str, hs)))
    nxt = hs[-1] + d
    if R.random() < 0.5:
        return mcq(pic + "Wie viele Würfel hat der nächste Turm?", str(nxt), [str(nxt + 1), str(hs[-1]), str(nxt + d)],
                   "Es %s immer %d Würfel dazu: %d + %d = <b>%d</b>." % ("kommt" if d == 1 else "kommen", d, hs[-1], d, nxt))
    n5 = hs[0] + 4 * d
    return mcq(pic + "Wie viele Würfel hat Turm 5?", str(n5), [str(n5 - d), str(n5 + d), str(5)],
               "Turm 4: %d, Turm 5: <b>%d</b>." % (hs[0] + 3 * d, n5))


def punkte():
    a, d = R.randint(1, 5), R.randint(1, 4)
    n = R.choice([4, 5])
    r = a + (n - 1) * d
    if r > 20:
        return None
    return mcq("Bild 1 hat %d Punkt%s, Bild 2 hat %d Punkte, Bild 3 hat %d Punkte. Wie viele Punkte hat Bild %d?" % (a, "" if a == 1 else "e", a + d, a + 2 * d, n), str(r),
               [str(r + d), str(r - d), str(r + 1)], "Es %s immer %d Punkt%s dazu: <b>%d</b>." % ("kommt" if d == 1 else "kommen", d, "" if d == 1 else "e", r))


def main():
    seen = set()
    sets = [
        ("Formenmuster", mix(R, seen, [(k2.formen, 20)])),
        ("Zahlenfolgen vorwärts", mix(R, seen, [(vor, 20)])),
        ("Zahlenfolgen rückwärts", mix(R, seen, [(rueck, 20)])),
        ("Kleine Zahlenmauern", mix(R, seen, [(mauer, 20)])),
        ("Wachsende Muster", mix(R, seen, [(tuerme, 10), (punkte, 10)])),
    ]
    body = lesson(
        ["Ein <b>Muster</b> wiederholt sich immer gleich: Kreis, Dreieck, Kreis, Dreieck …",
         "Bei einer <b>Zahlenfolge</b> suchst du die Regel: immer 2 mehr, immer 1 weniger …",
         "Prüfe die Regel an allen Zahlen, nicht nur an den ersten beiden.",
         "In einer <b>Zahlenmauer</b> ist jeder Stein die Summe der zwei Steine darunter."],
        [example("2, 4, 6, 8, ?", ["immer 2 mehr"], "10"),
         example("Zahlenmauer: unten 3 und 4", ["3 + 4"], "oben 7")],
        [["Beim Muster ein Glied überspringen", "Muster laut mitsprechen"],
         ["Die Regel nur an zwei Zahlen raten", "An allen Zahlen prüfen"],
         ["In der Zahlenmauer alle Zahlen addieren", "Nur die zwei Steine darunter"]])
    faq = [
        {"q": "Warum sind Muster in Mathe wichtig?", "a": "Wer Muster erkennt, kann vorhersagen, was als Nächstes kommt. Das ist die Grundlage für Rechenstrategien und Algebra."},
        {"q": "Wie übt man Muster zu Hause?", "a": "Mit Perlen auffädeln, Bausteine legen oder Klatschmuster: klatschen, stampfen, klatschen, stampfen."},
        {"q": "Was sind Zahlenmauern?", "a": "Steine wie in einer Mauer. Jeder Stein ist die Summe der zwei Steine darunter. Sie üben das Plusrechnen."},
        {"q": "Welche Zahlenfolgen kommen in Klasse 1 vor?", "a": "Zählen in Einer-, Zweier-, Fünfer- und Zehnerschritten, vorwärts und rückwärts bis 20."},
    ]
    make_unit(R, "muster-und-zahlenfolgen", "M",
              "Die Schülerinnen und Schüler erkennen, beschreiben und setzen Formenmuster und Zahlenfolgen fort, lösen kleine Zahlenmauern und beschreiben wachsende Muster (Zusammenfassung).",
              "Muster und Zahlenfolgen",
              "Muster und Zahlenfolgen Klasse 1 – Arbeitsblätter mit Lösungen",
              "Muster und Zahlenfolgen",
              "Muster und Zahlenfolgen für Klasse 1: Formenmuster, Zahlenfolgen vorwärts und rückwärts, kleine Zahlenmauern und wachsende Türme. 100 Übungsaufgaben mit Bildern und Lösungen, kostenlos.",
              "Regel finden, dann fortsetzen.",
              "2, 4, 6, 8, 10: immer 2 mehr",
              body, faq, sets, 16, grade="klasse-1")


if __name__ == "__main__":
    main()
