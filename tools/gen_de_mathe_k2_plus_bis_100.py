# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 2: Plus bis 100（Leitidee Zahl und Operation）
  python3 tools/gen_de_mathe_k2_plus_bis_100.py
Zehnerzahlen addieren, Einer dazu (mit und ohne Zehnerübergang), zweistellige Zahlen addieren (Schritt für Schritt), Sachaufgaben.
Fehler: Einer zu den Zehnern gerechnet (34 + 5 = 84), Zehnerübergang vergessen (38 + 47 = 75), um 10 verrechnet.
"""
import random
from de_common import mcq, lesson, example, make_unit, mix, Kids, dienes

R = random.Random(49204)
KIDS = Kids(R)


def zehner():
    kind = R.choice(["zz", "zez"])
    if kind == "zz":
        a, b = R.randint(1, 8) * 10, R.randint(1, 8) * 10
        if a + b > 100:
            return None
        return mcq("%d + %d = ?" % (a, b), str(a + b), [str(a // 10 + b // 10), str(a + b + 10) if a + b < 100 else str(a + b - 20), str(a + b - 10)],
                   "%d Zehner + %d Zehner = %d Zehner = <b>%d</b>." % (a // 10, b // 10, (a + b) // 10, a + b))
    a = R.randint(11, 79)
    if a % 10 == 0:
        return None
    b = R.randint(1, (99 - a) // 10) * 10
    r = a + b
    return mcq("%d + %d = ?" % (a, b), str(r), [str(a + b // 10), str(r + 10) if r + 10 < 100 else str(r - 20), str(r - 1)],
               "Nur die Zehner ändern sich: %d + %d = <b>%d</b>." % (a, b, r))


def einer():
    a = R.randint(12, 94)
    b = R.randint(2, 9)
    r = a + b
    if r > 100 or a % 10 == 0:
        return None
    ueber = a % 10 + b >= 10
    w = [str(a + 10 * b) if a + 10 * b <= 100 else None, str(r - 10) if ueber else str(r + 10) if r + 10 <= 100 else None, str(r + 1), str(r - 1)]
    if ueber:
        bis = 10 - a % 10
        e = ("Erst bis zum Zehner: %d + %d = %d. Dann noch %d: <b>%d</b>." % (a, bis, a + bis, b - bis, r)) if b > bis else \
            "%d + %d = 10. Das ergibt genau den nächsten Zehner: <b>%d</b>." % (a % 10, b, r)
    else:
        e = "Nur die Einer: %d + %d = %d. Also <b>%d</b>." % (a % 10, b, a % 10 + b, r)
    return mcq("%d + %d = ?" % (a, b), str(r), w, e)


def zwei(ueber):
    def mk():
        a, b = R.randint(12, 78), R.randint(11, 68)
        if a % 10 == 0 or b % 10 == 0:
            return None
        r = a + b
        if r > 100 or (a % 10 + b % 10 >= 10) != ueber or r == 100:
            return None
        za, zb = a // 10 * 10, b // 10 * 10
        w = [str(r - 10) if ueber else str(r + 10), str(r + 1), str(r - 1), str(za + zb + abs(a % 10 - b % 10))]
        pic = dienes(0, a // 10, a % 10, "%d als Zehnerstangen und Einerwürfel" % a) if R.random() < 0.3 else ""
        return mcq(pic + "%d + %d = ?" % (a, b), str(r), w,
                   "Erst die Zehner: %d + %d = %d. Dann die Einer: %d + %d = <b>%d</b>." % (a, zb, a + zb, a + zb, b % 10, r))
    return mk


def sache():
    kind = R.choice(["geld", "sammeln", "seiten", "lauf", "kinder"])
    p = KIDS.next()
    a, b = R.randint(15, 60), R.randint(12, 39)
    r = a + b
    if r > 100 or a % 10 == 0 or b % 10 == 0:
        return None
    w = [str(r - 10) if a % 10 + b % 10 >= 10 else str(r + 10), str(r + 1), str(a - b) if a > b else str(b - a), str(r - 1)]
    e = "%d + %d = <b>%d</b>." % (a, b, r)
    if kind == "geld":
        return mcq("%s hat %d € gespart. Zum Geburtstag bekommt %s %d €. Wie viel Geld hat %s jetzt?" % (p[0], a, p[1], b, p[1]), "%d €" % r,
                   ["%s €" % x for x in w], e.replace("</b>.", " €</b>."))
    if kind == "sammeln":
        return mcq("%s hat %d Sticker im Album. %s klebt %d neue Sticker ein. Wie viele Sticker sind es jetzt?" % (p[0], a, p[1].capitalize(), b), str(r), w, e)
    if kind == "seiten":
        return mcq("%s liest am Montag %d Seiten und am Dienstag %d Seiten. Wie viele Seiten sind das zusammen?" % (p[0], a, b), str(r), w, e)
    if kind == "lauf":
        return mcq("Beim Spendenlauf läuft die Klasse 2a %d Runden und die Klasse 2b %d Runden. Wie viele Runden laufen beide Klassen zusammen?" % (a, b), str(r), w, e)
    return mcq("In der Turnhalle sind %d Kinder. Dann kommen noch %d Kinder dazu. Wie viele Kinder sind jetzt in der Turnhalle?" % (a, b), str(r), w, e)


def main():
    seen = set()
    sets = [
        ("Mit Zehnerzahlen", mix(R, seen, [(zehner, 20)])),
        ("Einer dazu", mix(R, seen, [(einer, 20)])),
        ("Ohne Zehnerübergang", mix(R, seen, [(zwei(False), 20)])),
        ("Mit Zehnerübergang", mix(R, seen, [(zwei(True), 20)])),
        ("Sachaufgaben", mix(R, seen, [(sache, 20)])),
    ]
    body = lesson(
        ["Zehner zu Zehnern, Einer zu Einern: 30 + 40 ist wie 3 + 4, nur mit Zehnern.",
         "Bei 34 + 5 ändern sich nur die Einer: 4 + 5 = 9, also 39.",
         "Bei 38 + 5 geht es über den Zehner: 38 + 2 = 40, dann noch 3: 43.",
         "Zwei zweistellige Zahlen: erst die Zehner dazu, dann die Einer. 38 + 47: 38 + 40 = 78, 78 + 7 = 85."],
        [example("46 + 30", ["4 Zehner + 3 Zehner = 7 Zehner"], "76"),
         example("38 + 47", ["38 + 40 = 78", "78 + 2 = 80", "80 + 5 = 85"], "85")],
        [["34 + 5 = 84", "Die 5 sind Einer: 34 + 5 = 39"],
         ["38 + 47 = 75", "Über den Zehner rechnen: 85"],
         ["40 + 30 = 7", "4 Zehner + 3 Zehner = 70"]])
    faq = [
        {"q": "Welche Rechenwege lernen Kinder in Klasse 2?", "a": "Schrittweise (erst Zehner, dann Einer), stellenweise (Zehner und Einer getrennt) und Hilfsaufgaben wie 38 + 47 = 40 + 47 − 2. Das schriftliche Verfahren kommt erst in Klasse 3."},
        {"q": "Was ist der Zehnerübergang?", "a": "Wenn die Einer zusammen 10 oder mehr ergeben, entsteht ein neuer Zehner, zum Beispiel bei 38 + 5."},
        {"q": "Wie kann man das Ergebnis prüfen?", "a": "Mit der Umkehraufgabe: 85 − 47 = 38. Oder mit einem Überschlag: 40 + 50 = 90, das Ergebnis muss in der Nähe liegen."},
        {"q": "Welches Material hilft?", "a": "Zehnerstangen und Einerwürfel, das Hunderterfeld und der Zahlenstrahl, auf dem man in Zehner- und Einersprüngen springt."},
    ]
    make_unit(R, "plus-bis-100", "Z",
              "Die Schülerinnen und Schüler addieren im Zahlenraum bis 100 im Kopf und halbschriftlich, mit und ohne Zehnerübergang, nutzen schrittweises Rechnen und lösen Sachaufgaben (Zusammenfassung).",
              "Plus bis 100: Addieren mit und ohne Zehnerübergang",
              "Plus bis 100 Klasse 2 – Arbeitsblätter mit Lösungen",
              "Plus bis 100",
              "Plus bis 100 für Klasse 2: Zehnerzahlen, Einer dazu, Addieren mit und ohne Zehnerübergang und Sachaufgaben. 100 Übungsaufgaben mit Lösungen, kostenlos.",
              "Erst die Zehner, dann die Einer.",
              "38 + 47 = 38 + 40 + 7 = 85",
              body, faq, sets, 4, grade="klasse-2")


if __name__ == "__main__":
    main()
