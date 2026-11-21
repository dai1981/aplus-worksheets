# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 2: Plus und minus bis 20（Wiederholung, Leitidee Zahl und Operation）
  python3 tools/gen_de_mathe_k2_plus_und_minus_bis_20.py
Zerlegungen bis 10, Verdoppeln und Halbieren, plus über die 10, minus über die 10, Umkehraufgaben, Sachaufgaben.
Fehler: um 1 verzählt, beim Zehnerübergang falsch zerlegt (8 + 5 = 12), minus und plus verwechselt.
"""
import random
from de_common import mcq, lesson, example, make_unit, mix, Kids, table
from de_k2 import reihe, KINDS, DING

R = random.Random(49203)
KIDS = Kids(R)


def partner():
    kind = R.choice(["zehn", "zehn", "haus"])
    if kind == "zehn":
        a = R.randint(1, 9)
        k = R.choice(KINDS)
        pic = reihe(a, k, per_row=10)
        return mcq(pic + "%d + ? = 10" % a, str(10 - a), [str(9 - a) if a < 9 else "2", str(11 - a), str(a)],
                   "%d und <b>%d</b> sind zusammen 10." % (a, 10 - a))
    n = R.randint(5, 10)
    a = R.randint(1, n - 1)
    return mcq("Zahlenhaus %d: %d + ? = %d" % (n, a, n), str(n - a), [str(n - a + 1), str(n - a - 1) if n - a > 1 else str(n + a), str(n + a)],
               "%d + <b>%d</b> = %d." % (a, n - a, n))


def doppel():
    kind = R.choice(["dopp", "halb", "fast"])
    if kind == "dopp":
        a = R.randint(2, 10)
        return mcq("Verdopple %d." % a, str(2 * a), [str(2 * a + 1), str(a + 2), str(a // 2) if a % 2 == 0 and a // 2 != 2 else str(2 * a - 1)],
                   "%d + %d = <b>%d</b>." % (a, a, 2 * a))
    if kind == "halb":
        a = R.randint(2, 10) * 2
        return mcq("Halbiere %d." % a, str(a // 2), [str(a * 2) if a * 2 <= 40 else str(a // 2 + 2), str(a // 2 + 1), str(a - 2)],
                   "%d + %d = %d. Die Hälfte von %d ist <b>%d</b>." % (a // 2, a // 2, a, a, a // 2))
    a = R.randint(3, 9)
    return mcq("%d + %d = ?" % (a, a + 1), str(2 * a + 1), [str(2 * a), str(2 * a + 2), str(2 * a + 1 + 10) if 2 * a + 11 <= 20 else str(2 * a - 1)],
               "Fast verdoppeln: %d + %d = %d, dann 1 mehr: <b>%d</b>." % (a, a, 2 * a, 2 * a + 1))


def plus_ueber():
    a = R.randint(3, 9)
    b = R.randint(11 - a, 9)
    r = a + b
    if r > 18:
        return None
    if R.random() < 0.3:
        return mcq("%d + ? = %d" % (a, r), str(b), [str(b + 1), str(b - 1), str(r - 10)],
                   "%d + %d = 10, dann noch %d bis %d. Zusammen %d + %d = <b>%d</b>." % (a, 10 - a, r - 10, r, 10 - a, r - 10, b))
    return mcq("%d + %d = ?" % (a, b), str(r), [str(r - 1), str(r + 1), str(r - 10)],
               "Erst bis zur 10: %d + %d = 10. Dann noch %d: 10 + %d = <b>%d</b>." % (a, 10 - a, b - (10 - a), b - (10 - a), r))


def minus_ueber():
    a = R.randint(11, 18)
    b = R.randint(a - 9, 9)
    if a - b >= 10 or b <= a - 10:
        return None
    r = a - b
    if R.random() < 0.3:
        return mcq("%d − ? = %d" % (a, r), str(b), [str(b + 1), str(b - 1), str(a + r) if a + r <= 20 else str(r)],
                   "Umkehraufgabe: %d + %d = %d. Gesucht ist <b>%d</b>." % (r, b, a, b))
    return mcq("%d − %d = ?" % (a, b), str(r), [str(r + 1), str(r - 1) if r > 1 else str(r + 2), str(b - (a - 10)) if b - (a - 10) != r else str(r + 10)],
               "Erst bis zur 10: %d − %d = 10. Dann noch %d weg: 10 − %d = <b>%d</b>." % (a, a - 10, b - (a - 10), b - (a - 10), r))


def sache():
    kind = R.choice(["dazu", "weg", "vergleich", "fehlt"])
    p = KIDS.next()
    if kind == "dazu":
        a, b = R.randint(5, 9), R.randint(3, 9)
        if a + b > 20 or a + b <= 10:
            return None
        return mcq("%s hat %d Murmeln. %s bekommt %d Murmeln dazu. Wie viele Murmeln hat %s jetzt?" % (p[0], a, p[1].capitalize(), b, p[1]), str(a + b),
                   [str(a + b - 1), str(a + b + 1), str(abs(a - b)) if a != b else str(a + b - 2)],
                   "%d + %d = <b>%d</b>." % (a, b, a + b))
    if kind == "weg":
        a = R.randint(11, 18)
        b = R.randint(a - 9, 9)
        if a - b >= 10:
            return None
        return mcq("Im Bus sitzen %d Kinder. An der Haltestelle steigen %d Kinder aus. Wie viele Kinder sitzen noch im Bus?" % (a, b), str(a - b),
                   [str(a - b + 1), str(a + b) if a + b <= 20 else str(a - b + 2), str(a - b - 1)],
                   "%d − %d = <b>%d</b>." % (a, b, a - b))
    if kind == "vergleich":
        (a, _), (b, _) = KIDS.two()
        x, y = R.randint(10, 20), R.randint(3, 12)
        if x <= y:
            return None
        return mcq("%s hat %d Karten. %s hat %d Karten. Wie viele Karten hat %s mehr?" % (a, x, b, y, a), str(x - y),
                   [str(x + y) if x + y <= 30 else str(x - y + 2), str(x - y + 1), str(x - y - 1) if x - y > 1 else str(y)],
                   "%d − %d = <b>%d</b>." % (x, y, x - y))
    a = R.randint(4, 9)
    n = R.randint(11, 18)
    if n <= a + 1:
        return None
    return mcq("%s will %d Bilder malen. %d Bilder sind schon fertig. Wie viele Bilder fehlen noch?" % (p[0], n, a), str(n - a),
               [str(n + a) if n + a <= 25 else str(n - a + 2), str(n - a + 1), str(n - a - 1)],
               "%d + ? = %d. Es fehlen <b>%d</b> Bilder." % (a, n, n - a))


def main():
    seen = set()
    sets = [
        ("Zerlegen und Partnerzahlen", mix(R, seen, [(partner, 20)])),
        ("Verdoppeln und Halbieren", mix(R, seen, [(doppel, 20)])),
        ("Plus über die 10", mix(R, seen, [(plus_ueber, 20)])),
        ("Minus über die 10", mix(R, seen, [(minus_ueber, 20)])),
        ("Sachaufgaben", mix(R, seen, [(sache, 20)])),
    ]
    body = lesson(
        ["Die <b>Partnerzahlen</b> zur 10 musst du sicher können: 1 + 9, 2 + 8, 3 + 7, 4 + 6, 5 + 5.",
         "Beim Rechnen über die 10 rechnest du erst bis zur 10 und dann weiter.",
         "8 + 5: 8 + 2 = 10, dann noch 3: 13.",
         "13 − 5: 13 − 3 = 10, dann noch 2 weg: 8."],
        [example("7 + 6", ["7 + 3 = 10", "10 + 3 = 13"], "13"),
         example("15 − 7", ["15 − 5 = 10", "10 − 2 = 8"], "8")],
        [["8 + 5 = 12", "Die 5 zerlegen in 2 und 3: 13"],
         ["13 − 5 = 7", "Erst bis zur 10 (−3), dann noch −2: 8"],
         ["Bei „wie viele fehlen“ plus rechnen und das Ergebnis nehmen", "Gesucht ist die Zahl, die fehlt"]],
        extra=table(["Aufgabe", "Umkehraufgabe"], [["8 + 5 = 13", "13 − 5 = 8"], ["6 + 7 = 13", "13 − 7 = 6"]]))
    faq = [
        {"q": "Warum ist das Rechnen bis 20 in Klasse 2 so wichtig?", "a": "Alle Aufgaben bis 100 bauen darauf auf. Wer 8 + 5 sicher kann, rechnet auch 48 + 5 schnell."},
        {"q": "Was ist der Zehnerübergang?", "a": "Wenn das Ergebnis über die 10 geht. Man rechnet in zwei Schritten: erst bis zur 10, dann den Rest."},
        {"q": "Was sind Verdopplungsaufgaben?", "a": "Aufgaben wie 6 + 6 oder 8 + 8. Mit ihnen löst man auch Nachbaraufgaben: 6 + 7 ist 1 mehr als 6 + 6."},
        {"q": "Was ist eine Umkehraufgabe?", "a": "Zu 8 + 5 = 13 gehört 13 − 5 = 8. Mit der Umkehraufgabe kann man das Ergebnis prüfen."},
    ]
    make_unit(R, "plus-und-minus-bis-20", "Z",
              "Die Schülerinnen und Schüler beherrschen die Grundaufgaben der Addition und Subtraktion bis 20 sicher, nutzen Zerlegungen, Verdopplungen und Umkehraufgaben und rechnen über den Zehner (Zusammenfassung).",
              "Plus und minus bis 20",
              "Plus und minus bis 20 Klasse 2 – Arbeitsblätter mit Lösungen",
              "Plus und minus bis 20",
              "Plus und minus bis 20 für Klasse 2: Partnerzahlen, Verdoppeln und Halbieren, Rechnen über die 10 und Sachaufgaben. 100 Übungsaufgaben mit Lösungen, kostenlos.",
              "Erst bis zur 10, dann weiter.",
              "8 + 5 = 8 + 2 + 3 = 13",
              body, faq, sets, 3, grade="klasse-2")


if __name__ == "__main__":
    main()
