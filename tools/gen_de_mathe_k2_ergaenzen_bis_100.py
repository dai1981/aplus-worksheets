# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 2: Ergänzen bis 100（Leitidee Zahl und Operation）
  python3 tools/gen_de_mathe_k2_ergaenzen_bis_100.py
Ergänzen zum nächsten Zehner, ergänzen bis 100, ergänzen zwischen zwei Zahlen, Platzhalteraufgaben, Sachaufgaben „Wie viel fehlt?“.
Fehler: jede Ziffer zu 10 ergänzt (37 + 73 = 100), um 10 verrechnet, die Zielzahl statt der Differenz angegeben.
"""
import random
from de_common import mcq, lesson, example, make_unit, mix, Kids
from de_k2 import hunderterfeld

R = random.Random(49206)
KIDS = Kids(R)


def zum_zehner():
    a = R.randint(11, 98)
    if a % 10 == 0:
        return None
    z = (a // 10 + 1) * 10
    r = z - a
    return mcq("%d + ? = %d" % (a, z), str(r), [str(10 - r) if 10 - r != r else str(r + 1), str(r + 1), str(z), str(r + 10)],
               "Von %d bis zum Zehner %d fehlen <b>%d</b>." % (a, z, r))


def bis_hundert():
    a = R.randint(11, 89)
    if a % 10 == 0 and R.random() < 0.7:
        return None
    r = 100 - a
    z, e = divmod(a, 10)
    w = [str(10 * (10 - z) + (10 - e)) if e else None, str(r + 10), str(r - 10) if r > 10 else str(r + 1), str(r + 1)]
    pic = hunderterfeld(a) if R.random() < 0.4 else ""
    return mcq(pic + "%d + ? = 100" % a, str(r), w,
               ("Erst bis zum Zehner: %d + %d = %d. Dann bis 100: %d + %d = 100. Zusammen <b>%d</b>." % (a, (z + 1) * 10 - a, (z + 1) * 10, (z + 1) * 10, 100 - (z + 1) * 10, r))
               if e else "%d Zehner fehlen bis 10 Zehner: <b>%d</b>." % (10 - z, r))


def zwischen():
    a = R.randint(12, 70)
    b = R.randint(a + 11, 99)
    if a % 10 == 0 or b % 10 == 0:
        return None
    r = b - a
    nz = (a // 10 + 1) * 10
    return mcq("%d + ? = %d" % (a, b), str(r), [str(b), str(r + 10), str(r - 10) if r > 10 else str(r + 2), str(r + 1)],
               "%d + %d = %d, dann bis %d noch %d. Zusammen %d + %d = <b>%d</b>." % (a, nz - a, nz, b, b - nz, nz - a, b - nz, r))


def platzhalter():
    kind = R.choice(["vorne", "minus", "minus_vorne"])
    a, b = R.randint(12, 68), R.randint(12, 31)
    s = a + b
    if s > 100:
        return None
    if kind == "vorne":
        return mcq("? + %d = %d" % (b, s), str(a), [str(s + b) if s + b <= 100 else str(a + 10), str(a + 10), str(a - 1)],
                   "Rechne rückwärts: %d − %d = <b>%d</b>." % (s, b, a))
    if kind == "minus":
        return mcq("%d − ? = %d" % (s, a), str(b), [str(s + a) if s + a <= 100 else str(b + 10), str(b + 10), str(b - 1)],
                   "Von %d bis %d fehlen <b>%d</b>." % (a, s, b))
    return mcq("? − %d = %d" % (b, a), str(s), [str(a - b) if a > b else str(s - 10), str(s + 10) if s + 10 <= 100 else str(s - 1), str(s - 10)],
               "Umkehraufgabe: %d + %d = <b>%d</b>." % (a, b, s))


def sache():
    kind = R.choice(["geld", "seiten", "puzzle", "plaetze", "sammeln"])
    p = KIDS.next()
    a = R.randint(13, 87)
    if a % 10 == 0:
        return None
    if kind == "geld":
        z = R.choice([50, 60, 80, 100])
        if a >= z:
            return None
        return mcq("%s möchte ein Fahrradschloss für %d € kaufen. %s hat schon %d €. Wie viel Geld fehlt noch?" % (p[0], z, p[1].capitalize(), a), "%d €" % (z - a),
                   ["%d €" % x for x in (z + a if z + a <= 150 else z - a + 10, z - a + 10, z - a - 1)],
                   "%d + ? = %d. Es fehlen <b>%d €</b>." % (a, z, z - a))
    if kind == "seiten":
        return mcq("Ein Buch hat 100 Seiten. %s ist auf Seite %d. Wie viele Seiten sind es noch bis zum Ende?" % (p[0], a), str(100 - a),
                   [str(10 * (10 - a // 10) + 10 - a % 10), str(100 - a + 10), str(100 - a - 10) if a < 90 else str(100 - a + 1)],
                   "%d + ? = 100. Es sind noch <b>%d</b> Seiten." % (a, 100 - a))
    if kind == "puzzle":
        return mcq("Ein Puzzle hat 100 Teile. %d Teile liegen schon richtig. Wie viele Teile fehlen noch?" % a, str(100 - a),
                   [str(10 * (10 - a // 10) + 10 - a % 10), str(100 - a + 10), str(a)],
                   "%d + ? = 100. Es fehlen <b>%d</b> Teile." % (a, 100 - a))
    if kind == "plaetze":
        n = R.choice([60, 70, 80, 90])
        if a >= n:
            return None
        return mcq("Im Kino gibt es %d Plätze. %d Plätze sind schon besetzt. Wie viele Plätze sind noch frei?" % (n, a), str(n - a),
                   [str(n - a + 10), str(n - a - 1), str(n + a) if n + a <= 150 else str(n - a + 2)],
                   "%d + ? = %d. Es sind noch <b>%d</b> Plätze frei." % (a, n, n - a))
    z = R.choice([50, 60, 70, 80, 90, 100])
    if a >= z:
        return None
    return mcq("%s sammelt Kastanien. %s möchte %d haben und hat schon %d. Wie viele Kastanien fehlen noch?" % (p[0], p[1].capitalize(), z, a), str(z - a),
               [str(z - a + 10), str(z - a + 1), str(z)],
               "%d + ? = %d. Es fehlen <b>%d</b>." % (a, z, z - a))


def main():
    seen = set()
    sets = [
        ("Bis zum nächsten Zehner", mix(R, seen, [(zum_zehner, 20)])),
        ("Bis 100 ergänzen", mix(R, seen, [(bis_hundert, 20)])),
        ("Zwischen zwei Zahlen ergänzen", mix(R, seen, [(zwischen, 20)])),
        ("Platzhalteraufgaben", mix(R, seen, [(platzhalter, 20)])),
        ("Wie viel fehlt noch?", mix(R, seen, [(sache, 20)])),
    ]
    body = lesson(
        ["Beim <b>Ergänzen</b> fragst du: Wie viel fehlt noch bis zur Zielzahl?",
         "Rechne in zwei Schritten: erst bis zum nächsten Zehner, dann weiter in Zehnern.",
         "37 + ? = 100: 37 + 3 = 40, 40 + 60 = 100. Es fehlen 63.",
         "Prüfe mit plus: 37 + 63 = 100."],
        [example("46 + ? = 50", ["Von 46 bis 50"], "4"),
         example("28 + ? = 75", ["28 + 2 = 30", "30 + 45 = 75", "2 + 45"], "47")],
        [["37 + 73 = 100", "37 + 63 = 100 (die Einer ergeben nur einen Zehner)"],
         ["Die Zielzahl als Antwort schreiben", "Gefragt ist, wie viel fehlt"],
         ["Beim zweiten Schritt um 10 verrechnen", "Mit der Plusaufgabe prüfen"]])
    faq = [
        {"q": "Warum ist Ergänzen so wichtig?", "a": "Ergänzen hilft beim Wechselgeld, bei „Wie viel fehlt noch?“ und beim Subtrahieren: 62 − 58 rechnet man am leichtesten als 58 + ? = 62."},
        {"q": "Warum schreiben Kinder bei 37 + ? = 100 oft 73?", "a": "Sie ergänzen jede Ziffer zu 10 (3 + 7 und 7 + 3). Dabei entsteht aber 110. Richtig ist: Die Einer ergänzen zu 10, die Zehner nur zu 9."},
        {"q": "Wie übt man Ergänzen bis 100?", "a": "Mit dem Hunderterfeld: Die blauen Punkte sind gegeben, die weißen fehlen. Auch Geld hilft: Wie viel fehlt von 37 € bis 100 €?"},
        {"q": "Was ist eine Platzhalteraufgabe?", "a": "Eine Aufgabe, in der eine Zahl fehlt, zum Beispiel 45 + ? = 80 oder ? − 20 = 35."},
    ]
    make_unit(R, "ergaenzen-bis-100", "Z",
              "Die Schülerinnen und Schüler ergänzen im Zahlenraum bis 100 zum nächsten Zehner, bis 100 und zwischen zwei Zahlen, lösen Platzhalteraufgaben und Sachaufgaben zum Ergänzen (Zusammenfassung).",
              "Ergänzen bis 100: Wie viel fehlt?",
              "Ergänzen bis 100 Klasse 2 – Arbeitsblätter mit Lösungen",
              "Ergänzen bis 100",
              "Ergänzen bis 100 für Klasse 2: bis zum Zehner, bis 100, zwischen zwei Zahlen, Platzhalteraufgaben und Sachaufgaben. 100 Übungsaufgaben mit Lösungen, kostenlos.",
              "Erst bis zum Zehner, dann in Zehnern weiter.",
              "37 + 3 = 40, 40 + 60 = 100: Es fehlen 63.",
              body, faq, sets, 6, grade="klasse-2")


if __name__ == "__main__":
    main()
