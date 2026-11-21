# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 2: Minus bis 100（Leitidee Zahl und Operation）
  python3 tools/gen_de_mathe_k2_minus_bis_100.py
Zehnerzahlen subtrahieren, Einer weg (mit und ohne Zehnerübergang), zweistellige Zahlen subtrahieren, Umkehraufgaben, Sachaufgaben.
Fehler: die kleinere Einerziffer von der größeren abziehen (43 − 5 = 42), Zehnerübergang vergessen (62 − 27 = 45), plus statt minus.
"""
import random
from de_common import mcq, lesson, example, make_unit, mix, Kids

R = random.Random(49205)
KIDS = Kids(R)


def dreh_fehler(a, b):
    """typischer Fehler: in jeder Stelle die kleinere von der größeren Ziffer abziehen"""
    z = abs(a // 10 - b // 10)
    e = abs(a % 10 - b % 10)
    return 10 * z + e


def zehner():
    kind = R.choice(["zz", "zez"])
    if kind == "zz":
        a = R.randint(3, 10) * 10
        b = R.randint(1, a // 10 - 1) * 10
        return mcq("%d − %d = ?" % (a, b), str(a - b), [str(a // 10 - b // 10), str(a + b) if a + b <= 100 else str(a - b + 20), str(a - b - 10) if a - b > 10 else str(a - b + 10)],
                   "%d Zehner − %d Zehner = %d Zehner = <b>%d</b>." % (a // 10, b // 10, (a - b) // 10, a - b))
    a = R.randint(31, 99)
    if a % 10 == 0:
        return None
    b = R.randint(1, a // 10 - 1) * 10
    r = a - b
    return mcq("%d − %d = ?" % (a, b), str(r), [str(a - b // 10), str(r + 10), str(r - 10) if r > 10 else str(r + 1)],
               "Nur die Zehner ändern sich: %d − %d = <b>%d</b>." % (a, b, r))


def einer():
    a = R.randint(21, 99)
    b = R.randint(2, 9)
    if a % 10 == 0 and R.random() < 0.5:
        return None
    r = a - b
    ueber = a % 10 < b
    w = [str(dreh_fehler(a, b)), str(r + 10) if ueber else str(r - 10), str(r + 1), str(a + b) if a + b <= 100 else str(r - 1)]
    if ueber:
        e = "Erst bis zum Zehner: %d − %d = %d. Dann noch %d weg: <b>%d</b>." % (a, a % 10, a - a % 10, b - a % 10, r) if a % 10 else \
            "%d − %d: Ein Zehner wird aufgelöst. %d − %d = <b>%d</b>." % (a, b, a, b, r)
    else:
        e = "Nur die Einer: %d − %d = %d. Also <b>%d</b>." % (a % 10, b, a % 10 - b, r)
    return mcq("%d − %d = ?" % (a, b), str(r), w, e)


def zwei(ueber):
    def mk():
        a, b = R.randint(31, 99), R.randint(11, 69)
        if a % 10 == 0 or b % 10 == 0 or b >= a:
            return None
        if (a % 10 < b % 10) != ueber:
            return None
        r = a - b
        zb = b // 10 * 10
        w = [str(dreh_fehler(a, b)) if ueber else str(r + 10), str(r + 10) if ueber else str(r - 10) if r > 10 else str(r + 2), str(r + 1), str(r - 1)]
        return mcq("%d − %d = ?" % (a, b), str(r), w,
                   "Erst die Zehner weg: %d − %d = %d. Dann die Einer: %d − %d = <b>%d</b>." % (a, zb, a - zb, a - zb, b % 10, r))
    return mk


def umkehr():
    a, b = R.randint(31, 99), R.randint(11, 69)
    if b >= a or a % 10 == 0:
        return None
    r = a - b
    kind = R.choice(["luecke", "probe"])
    if kind == "luecke":
        return mcq("%d − ? = %d" % (a, r), str(b), [str(a + r) if a + r <= 100 else str(b + 10), str(b + 10), str(b - 1)],
                   "Umkehraufgabe: %d + ? = %d. Es fehlen <b>%d</b>." % (r, a, b))
    ans = "%d + %d = %d" % (r, b, a)
    return mcq("Mit welcher Aufgabe kannst du %d − %d = %d prüfen?" % (a, b, r), ans,
               ["%d + %d = %d" % (a, b, a + b), "%d − %d = %d" % (a, r, b), "%d + %d = %d" % (a, r, a + r)],
               "Ergebnis plus die abgezogene Zahl muss die Ausgangszahl geben: <b>%s</b>." % ans)


def sache():
    kind = R.choice(["geld", "kekse", "seiten", "bus", "unterschied"])
    p = KIDS.next()
    a, b = R.randint(32, 99), R.randint(12, 49)
    if b >= a or b % 10 == 0:
        return None
    r = a - b
    w = [str(dreh_fehler(a, b)), str(r + 10), str(r - 1), str(a + b) if a + b <= 100 else str(r + 1)]
    e = "%d − %d = <b>%d</b>." % (a, b, r)
    if kind == "geld":
        return mcq("%s hat %d €. %s kauft ein Spiel für %d €. Wie viel Geld bleibt übrig?" % (p[0], a, p[1].capitalize(), b), "%d €" % r,
                   ["%s €" % x for x in w], e.replace("</b>.", " €</b>."))
    if kind == "kekse":
        return mcq("Auf dem Schulfest gibt es %d Waffeln. %d Waffeln sind schon verkauft. Wie viele Waffeln sind noch da?" % (a, b), str(r), w, e)
    if kind == "seiten":
        return mcq("Ein Buch hat %d Seiten. %s hat schon %d Seiten gelesen. Wie viele Seiten fehlen noch?" % (a, p[0], b), str(r), w, e)
    if kind == "bus":
        return mcq("Im Zug sitzen %d Menschen. In Köln steigen %d Menschen aus. Wie viele Menschen sitzen noch im Zug?" % (a, b), str(r), w, e)
    (n1, _), (n2, _) = KIDS.two()
    return mcq("%s hat %d Murmeln, %s hat %d Murmeln. Wie viele Murmeln hat %s mehr?" % (n1, a, n2, b, n1), str(r), w, e)


def main():
    seen = set()
    sets = [
        ("Mit Zehnerzahlen", mix(R, seen, [(zehner, 20)])),
        ("Einer weg", mix(R, seen, [(einer, 20)])),
        ("Ohne Zehnerübergang", mix(R, seen, [(zwei(False), 20)])),
        ("Mit Zehnerübergang", mix(R, seen, [(zwei(True), 14), (umkehr, 6)])),
        ("Sachaufgaben", mix(R, seen, [(sache, 20)])),
    ]
    body = lesson(
        ["Zehner von Zehnern, Einer von Einern: 70 − 30 ist wie 7 − 3, nur mit Zehnern.",
         "Bei 46 − 3 ändern sich nur die Einer: 6 − 3 = 3, also 43.",
         "Bei 43 − 5 geht es über den Zehner: 43 − 3 = 40, dann noch 2 weg: 38.",
         "Zwei zweistellige Zahlen: erst die Zehner weg, dann die Einer. 62 − 27: 62 − 20 = 42, 42 − 7 = 35."],
        [example("85 − 40", ["8 Zehner − 4 Zehner = 4 Zehner"], "45"),
         example("62 − 27", ["62 − 20 = 42", "42 − 2 = 40", "40 − 5 = 35"], "35")],
        [["43 − 5 = 42 (5 − 3 gerechnet)", "Über den Zehner: 43 − 3 − 2 = 38"],
         ["62 − 27 = 45", "Erst 20 weg, dann 7 weg: 35"],
         ["Probe mit minus", "Probe mit plus: 35 + 27 = 62"]])
    faq = [
        {"q": "Warum rechnen Kinder bei 43 − 5 oft 42?", "a": "Sie ziehen die kleinere Ziffer von der größeren ab (5 − 3), weil 3 − 5 „nicht geht“. Hilfe: erst bis zum Zehner abziehen (43 − 3 = 40), dann den Rest (40 − 2 = 38)."},
        {"q": "Welche Rechenwege gibt es für 62 − 27?", "a": "Schrittweise (62 − 20 − 7), Ergänzen (27 + ? = 62) oder Hilfsaufgabe (62 − 30 + 3). Alle führen zu 35."},
        {"q": "Wie prüft man eine Minusaufgabe?", "a": "Mit der Umkehraufgabe: Ergebnis plus die abgezogene Zahl muss die Ausgangszahl ergeben."},
        {"q": "Wann lernen Kinder die schriftliche Subtraktion?", "a": "In der Regel in Klasse 3. In Klasse 2 wird im Kopf und halbschriftlich gerechnet."},
    ]
    make_unit(R, "minus-bis-100", "Z",
              "Die Schülerinnen und Schüler subtrahieren im Zahlenraum bis 100 im Kopf und halbschriftlich, mit und ohne Zehnerübergang, prüfen mit der Umkehraufgabe und lösen Sachaufgaben (Zusammenfassung).",
              "Minus bis 100: Subtrahieren mit und ohne Zehnerübergang",
              "Minus bis 100 Klasse 2 – Arbeitsblätter mit Lösungen",
              "Minus bis 100",
              "Minus bis 100 für Klasse 2: Zehnerzahlen, Einer weg, Subtrahieren mit und ohne Zehnerübergang, Umkehraufgaben und Sachaufgaben. 100 Übungsaufgaben mit Lösungen, kostenlos.",
              "Erst die Zehner weg, dann die Einer.",
              "62 − 27 = 62 − 20 − 7 = 35",
              body, faq, sets, 5, grade="klasse-2")


if __name__ == "__main__":
    main()
