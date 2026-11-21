# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 2: Einmaleins mit 2, 5 und 10 – Kernaufgaben（Leitidee Zahl und Operation）
  python3 tools/gen_de_mathe_k2_einmaleins_mit_2_5_und_10.py
Zweier-, Fünfer- und Zehnerreihe, Platzhalter, Kernaufgaben nutzen (Nachbaraufgaben, Verdoppeln), Sachaufgaben.
Fehler: plus statt mal, in der Reihe um eins verrutscht, Nachbaraufgabe in die falsche Richtung.
"""
import random
from de_common import mcq, lesson, example, make_unit, mix, Kids, MAL, table
from de_k2 import punktfeld

R = random.Random(49208)
KIDS = Kids(R)


def reihe(k):
    def mk():
        a = R.randint(0 if R.random() < 0.05 else 1, 10)
        kind = R.choice(["mal", "mal", "tausch", "luecke"])
        r = a * k
        w = [str(r + k), str(r - k) if r >= k else str(r + 2 * k), str(a + k), str(r + 1)]
        if kind == "mal":
            return mcq("%d %s %d = ?" % (a, MAL, k), str(r), w, "%d-mal die %d: <b>%d</b>." % (a, k, r))
        if kind == "tausch":
            return mcq("%d %s %d = ?" % (k, MAL, a), str(r), w, "%d %s %d = %d %s %d = <b>%d</b>." % (k, MAL, a, a, MAL, k, r))
        if a == 0:
            return None
        return mcq("? %s %d = %d" % (MAL, k, r), str(a), [str(a + 1), str(a - 1) if a > 1 else str(a + 2), str(r - k) if r - k != a else str(r)],
                   "In der %der-Reihe: <b>%d</b> %s %d = %d." % (k, a, MAL, k, r))
    return mk


def zehner_reihe():
    k = R.choice([10, 10, 1])
    return reihe(k)()


def nutzen():
    kind = R.choice(["plus", "minus", "dopp", "folge"])
    if kind == "plus":
        k = R.choice([2, 3, 4, 6, 7, 8, 9])
        a = 6 if R.random() < 0.5 else 11
        if a == 11:
            return None
        return mcq("Du weißt: 5 %s %d = %d. Wie viel ist 6 %s %d?" % (MAL, k, 5 * k, MAL, k), str(6 * k), [str(5 * k + 1), str(5 * k + 6), str(4 * k)],
                   "Nachbaraufgabe: einmal %d mehr. %d + %d = <b>%d</b>." % (k, 5 * k, k, 6 * k))
    if kind == "minus":
        k = R.choice([3, 4, 6, 7, 8, 9])
        return mcq("Du weißt: 10 %s %d = %d. Wie viel ist 9 %s %d?" % (MAL, k, 10 * k, MAL, k), str(9 * k), [str(10 * k - 1), str(10 * k - 9), str(11 * k)],
                   "Nachbaraufgabe: einmal %d weniger. %d − %d = <b>%d</b>." % (k, 10 * k, k, 9 * k))
    if kind == "dopp":
        a = R.randint(2, 10)
        return mcq("Du weißt: 2 %s %d = %d. Wie viel ist 4 %s %d?" % (MAL, a, 2 * a, MAL, a), str(4 * a), [str(2 * a + 2), str(2 * a + 4), str(6 * a)],
                   "4-mal ist das Doppelte von 2-mal: %d + %d = <b>%d</b>." % (2 * a, 2 * a, 4 * a))
    k = R.choice([2, 5, 10])
    st = R.randint(1, 5)
    seq = [k * (st + i) for i in range(4)]
    return mcq("Wie geht die Malreihe weiter? %s, ?" % ", ".join(map(str, seq)), str(k * (st + 4)), [str(seq[-1] + 1), str(seq[-1] + 2 * k), str(seq[-1] + k + 1)],
               "Immer %d mehr: %d + %d = <b>%d</b>." % (k, seq[-1], k, k * (st + 4)))


SACHE = [("Paar Socken", "Socken", 2, "Im Schrank liegen %d Paar Socken. Wie viele Socken sind das?"),
         ("Hände", "Finger", 5, "%d Kinder strecken eine Hand hoch. Wie viele Finger sind das?"),
         ("Zehnerpackungen", "Eier", 10, "Mama kauft %d Packungen mit je 10 Eiern. Wie viele Eier sind das?"),
         ("Fünf-Euro-Scheine", "€", 5, "%s hat %d Fünf-Euro-Scheine. Wie viel Geld ist das?"),
         ("Zehn-Cent-Münzen", "ct", 10, "%s hat %d Zehn-Cent-Münzen. Wie viel Geld ist das?"),
         ("Fahrräder", "Räder", 2, "Vor der Schule stehen %d Fahrräder. Wie viele Räder haben sie zusammen?"),
         ("Seesterne", "Arme", 5, "Im Aquarium sind %d Seesterne mit je 5 Armen. Wie viele Arme sind das?"),
         ("Zweiertische", "Kinder", 2, "In der Klasse stehen %d Zweiertische. An jedem sitzen 2 Kinder. Wie viele Kinder sind das?"),
         ("Kisten", "Flaschen", 10, "Im Keller stehen %d Kisten mit je 10 Flaschen. Wie viele Flaschen sind das?")]


def sache():
    t, u, k, q = R.choice(SACHE)
    a = R.randint(3, 10)
    p = KIDS.next()
    qq = q % ((p[0], a) if q.startswith("%s") else (a,))
    unit = " %s" % u if u in ("€", "ct") else ""
    r = a * k
    return mcq(qq, "%d%s" % (r, unit), ["%d%s" % (x, unit) for x in (a + k, r + k, r - k)],
               "%d %s %d = <b>%d%s</b>." % (a, MAL, k, r, unit))


def main():
    seen = set()
    sets = [
        ("Die Zweierreihe", mix(R, seen, [(reihe(2), 20)])),
        ("Die Fünferreihe", mix(R, seen, [(reihe(5), 20)])),
        ("Die Zehnerreihe und die Einerreihe", mix(R, seen, [(zehner_reihe, 20)])),
        ("Kernaufgaben nutzen", mix(R, seen, [(nutzen, 20)])),
        ("Sachaufgaben", mix(R, seen, [(sache, 20)])),
    ]
    body = lesson(
        ["Die <b>Kernaufgaben</b> sind 1 %s, 2 %s, 5 %s und 10 %s. Sie musst du auswendig können." % (MAL, MAL, MAL, MAL),
         "Die Zweierreihe sind die Verdopplungen: 2 %s 6 = 6 + 6 = 12." % MAL,
         "5 %s ist die Hälfte von 10 %s: 5 %s 8 = 40, weil 10 %s 8 = 80." % (MAL, MAL, MAL, MAL),
         "Aus den Kernaufgaben findest du andere Aufgaben: 6 %s 4 ist 5 %s 4 und noch einmal 4." % (MAL, MAL)],
        [example("6 %s 7" % MAL, ["5 %s 7 = 35" % MAL, "35 + 7 = 42"], "42"),
         example("9 %s 4" % MAL, ["10 %s 4 = 40" % MAL, "40 − 4 = 36"], "36")],
        [["5 %s 6 = 11" % MAL, "5 %s 6 = 30 (5-mal die 6)" % MAL],
         ["6 %s 5 = 5 %s 5 + 1" % (MAL, MAL), "6 %s 5 = 5 %s 5 + 5 = 30" % (MAL, MAL)],
         ["In der Reihe eine Zahl überspringen", "Mit Fingern in Schritten mitzählen"]],
        extra=table(["Reihe", "Zahlen"], [["2", "2, 4, 6, 8, 10, 12, 14, 16, 18, 20"], ["5", "5, 10, 15, 20, 25, 30, 35, 40, 45, 50"], ["10", "10, 20, 30, 40, 50, 60, 70, 80, 90, 100"]]))
    faq = [
        {"q": "Was sind Kernaufgaben?", "a": "Die leichten Malaufgaben mit 1, 2, 5 und 10 (und oft auch die Quadrataufgaben). Aus ihnen kann man alle anderen Aufgaben ableiten."},
        {"q": "In welcher Reihenfolge lernt man das Einmaleins?", "a": "Meist zuerst die Zweier-, Fünfer- und Zehnerreihe, dann die Vierer- und Achterreihe (Verdoppeln), dann die Dreier-, Sechser-, Siebener- und Neunerreihe."},
        {"q": "Wie hilft 10 · für die 9er-Reihe?", "a": "9 · 6 ist 10 · 6 minus einmal 6: 60 − 6 = 54."},
        {"q": "Wie übt man die Reihen?", "a": "Laut in Schritten zählen, Malaufgaben mit Geld (5-Euro-Scheine, 10-Cent-Münzen) und kurze tägliche Übungen von wenigen Minuten."},
    ]
    make_unit(R, "einmaleins-mit-2-5-und-10", "Z",
              "Die Schülerinnen und Schüler beherrschen die Kernaufgaben des Einmaleins mit 1, 2, 5 und 10 und leiten daraus Nachbaraufgaben und Verdopplungen ab (Zusammenfassung).",
              "Einmaleins mit 2, 5 und 10: die Kernaufgaben",
              "Einmaleins mit 2, 5 und 10 Klasse 2 – Arbeitsblätter mit Lösungen",
              "Einmaleins 2, 5, 10",
              "Einmaleins mit 2, 5 und 10 für Klasse 2: Zweier-, Fünfer- und Zehnerreihe, Kernaufgaben nutzen und Sachaufgaben. 100 Übungsaufgaben mit Lösungen, kostenlos.",
              "Kernaufgaben: 1 ·, 2 ·, 5 · und 10 ·",
              "6 · 4 = 5 · 4 + 4",
              body, faq, sets, 8, grade="klasse-2")


if __name__ == "__main__":
    main()
