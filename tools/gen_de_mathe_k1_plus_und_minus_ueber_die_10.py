# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 1: Plus und minus über die 10（Zehnerübergang, Leitidee Zahl und Operation）
  python3 tools/gen_de_mathe_k1_plus_und_minus_ueber_die_10.py
Im Zwanzigerfeld auffüllen, plus über die 10, minus über die 10, Schritt für Schritt (erst bis 10), Rechengeschichten.
Fehler: falsch zerlegt (8 + 5 = 8 + 2 + 2), um 1 verzählt, bei 13 − 5 die Einer vertauscht (5 − 3 = 2 → 12).
"""
import random
from de_common import mcq, lesson, example, make_unit, mix, Kids
from de_k2 import de
from k_pics import tenframe_mix_svg

R = random.Random(49408)
KIDS = Kids(R)


def w(x):
    return [str(v) for v in (x - 1, x + 1, x - 10, x + 2) if 1 <= v <= 20 and v != x]


def paar():
    a = R.randint(3, 9)
    b = R.randint(11 - a, 9)
    if a + b > 18:
        return None
    return a, b


def feld():
    p = paar()
    if not p:
        return None
    a, b = p
    cells = ["r"] * a + ["b"] * (10 - a) + ["b"] * (b - (10 - a)) + [""] * (20 - a - b)
    pic = de(tenframe_mix_svg(cells, 2), "Zwanzigerfeld mit %d roten und %d blauen Punkten" % (a, b))
    return mcq(pic + "%d rote und %d blaue Punkte. Wie viele sind es zusammen?" % (a, b), str(a + b), w(a + b),
               "Das erste Feld ist voll: 10. Im zweiten Feld sind %d: <b>%d</b>." % (a + b - 10, a + b))


def plus():
    p = paar()
    if not p:
        return None
    a, b = p
    r = a + b
    return mcq("%d + %d = ?" % (a, b), str(r), w(r), "Erst bis 10: %d + %d = 10. Dann noch %d: <b>%d</b>." % (a, 10 - a, b - (10 - a), r))


def minus():
    a = R.randint(11, 18)
    b = R.randint(a - 9, 9)
    if b <= a - 10:
        return None
    r = a - b
    fehl = 10 + abs(a % 10 - b)
    return mcq("%d − %d = ?" % (a, b), str(r), [str(fehl)] + w(r), "Erst bis 10: %d − %d = 10. Dann noch %d weg: <b>%d</b>." % (a, a - 10, b - (a - 10), r))


def schritte():
    if R.random() < 0.5:
        p = paar()
        if not p:
            return None
        a, b = p
        x = 10 - a
        return mcq("%d + %d = %d + %d + ?" % (a, b, a, x), str(b - x), [str(x), str(b - x + 1), str(b)],
                   "%d wird zerlegt in %d und <b>%d</b>." % (b, x, b - x))
    a = R.randint(11, 18)
    b = R.randint(a - 9, 9)
    if b <= a - 10:
        return None
    x = a - 10
    return mcq("%d − %d = %d − %d − ?" % (a, b, a, x), str(b - x), [str(x), str(b - x + 1), str(b)],
               "%d wird zerlegt in %d und <b>%d</b>." % (b, x, b - x))


GESCH = [("%s hat %d Murmeln. %s gewinnt %d dazu. Wie viele Murmeln hat %s jetzt?", "+p"),
         ("Im Garten sind %d Tulpen und %d Rosen. Wie viele Blumen sind es zusammen?", "+"),
         ("Im Bus sitzen %d Kinder. %d Kinder steigen aus. Wie viele Kinder sitzen noch im Bus?", "-"),
         ("Auf dem Tisch liegen %d Kekse. Die Kinder essen %d Kekse. Wie viele Kekse liegen noch auf dem Tisch?", "-"),
         ("%s hat %d Sticker. %s verschenkt %d Sticker. Wie viele Sticker hat %s noch?", "-p"),
         ("In einer Reihe stehen %d Kinder. %d Kinder stellen sich dazu. Wie viele Kinder stehen jetzt in der Reihe?", "+")]


def geschichte():
    t, kind = R.choice(GESCH)
    p = KIDS.next()
    if kind.startswith("+"):
        pp = paar()
        if not pp:
            return None
        a, b = pp
        r = a + b
    else:
        a = R.randint(11, 18)
        b = R.randint(max(a - 9, 2), 9)
        if b <= a - 10:
            return None
        r = a - b
    if kind.endswith("p"):
        q = t % (p[0], a, p[1].capitalize(), b, p[1])
    else:
        q = t % (a, b)
    other = a - b if kind.startswith("+") else a + b
    return mcq(q, str(r), [str(other) if 0 < other <= 30 else str(r + 2), str(r + 1), str(r - 1)],
               ("%d + %d = <b>%d</b>." if kind.startswith("+") else "%d − %d = <b>%d</b>.") % (a, b, r))


def main():
    seen = set()
    sets = [
        ("Im Zwanzigerfeld", mix(R, seen, [(feld, 20)])),
        ("Plus über die 10", mix(R, seen, [(plus, 20)])),
        ("Minus über die 10", mix(R, seen, [(minus, 20)])),
        ("Schritt für Schritt", mix(R, seen, [(schritte, 20)])),
        ("Rechengeschichten", mix(R, seen, [(geschichte, 20)])),
    ]
    body = lesson(
        ["Geht eine Aufgabe über die 10, rechnest du in zwei Schritten.",
         "Plus: Erst bis zur 10 auffüllen, dann den Rest dazu. 8 + 5 = 8 + 2 + 3 = 13.",
         "Minus: Erst bis zur 10 zurück, dann den Rest weg. 13 − 5 = 13 − 3 − 2 = 8.",
         "Dafür brauchst du die Partner der 10 und das Zerlegen."],
        [example("7 + 6", ["7 + 3 = 10", "10 + 3 = 13"], "13"),
         example("15 − 7", ["15 − 5 = 10", "10 − 2 = 8"], "8")],
        [["8 + 5 = 8 + 2 + 2", "5 = 2 + 3, also 8 + 2 + 3 = 13"],
         ["13 − 5 = 12 (5 − 3 gerechnet)", "13 − 3 = 10, dann noch 2 weg: 8"],
         ["Alles einzeln abzählen und sich verzählen", "Die 10 als Zwischenstation nutzen"]])
    faq = [
        {"q": "Warum ist der Zehnerübergang schwierig?", "a": "Man muss zwei Dinge gleichzeitig können: die Partner der 10 und das Zerlegen. Deshalb übt man beides vorher."},
        {"q": "Welche Rechenwege gibt es?", "a": "Schrittweise über die 10, mit Verdopplungsaufgaben (6 + 7 = 6 + 6 + 1) oder mit der Kraft der 5 im Zwanzigerfeld."},
        {"q": "Welches Material hilft?", "a": "Das Zwanzigerfeld mit zwei Farben, die Rechenkette und der Zahlenstrahl."},
        {"q": "Wann sollen die Aufgaben auswendig sitzen?", "a": "Bis zum Ende von Klasse 1 sollten die meisten Aufgaben bis 20 schnell gelöst werden. In Klasse 2 werden sie weiter gefestigt."},
    ]
    make_unit(R, "plus-und-minus-ueber-die-10", "Z",
              "Die Schülerinnen und Schüler addieren und subtrahieren im Zahlenraum bis 20 mit Zehnerübergang, zerlegen dazu Zahlen geschickt, nutzen die 10 als Zwischenschritt und lösen Rechengeschichten (Zusammenfassung).",
              "Plus und minus über die 10",
              "Zehnerübergang Klasse 1 – Arbeitsblätter mit Lösungen",
              "Über die 10",
              "Plus und minus über die 10 für Klasse 1: Zwanzigerfeld, Zehnerübergang Schritt für Schritt, Plus- und Minusaufgaben und Rechengeschichten. 100 Übungsaufgaben mit Lösungen, kostenlos.",
              "Erst bis zur 10, dann weiter.",
              "8 + 5 = 8 + 2 + 3 = 13",
              body, faq, sets, 8, grade="klasse-1")


if __name__ == "__main__":
    main()
