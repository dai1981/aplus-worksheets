# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 1: Plus und minus bis 20 ohne Zehnerübergang（Leitidee Zahl und Operation）
  python3 tools/gen_de_mathe_k1_plus_und_minus_bis_20.py
Analogieaufgaben (3 + 4 → 13 + 4), plus und minus im zweiten Zehner, mit dem Zehner rechnen, Platzhalter, Rechengeschichten.
Fehler: den Zehner vergessen (13 + 4 = 7), Zehner und Einer vermischt (13 + 4 = 53), plus und minus verwechselt.
"""
import random
from de_common import mcq, lesson, example, make_unit, mix, Kids
from de_k2 import de
from k_pics import tenframe_svg

R = random.Random(49407)
KIDS = Kids(R)


def w(x):
    return [str(v) for v in (x - 1, x + 1, x - 10, x + 2) if 0 <= v <= 20 and v != x]


def analog():
    a, b = R.randint(1, 8), R.randint(1, 8)
    if R.random() < 0.5:
        if a + b > 9:
            return None
        return mcq("Du weißt: %d + %d = %d. Wie viel ist 1%d + %d?" % (a, b, a + b, a, b), str(10 + a + b), [str(a + b), str(10 + a + b + 1), str(10 * b + a + 10) if 10 * b + a + 10 <= 99 else str(19)],
                   "Nur der Zehner kommt dazu: 1%d + %d = <b>%d</b>." % (a, b, 10 + a + b))
    if b >= a:
        a, b = b, a
    if a == b:
        return None
    return mcq("Du weißt: %d − %d = %d. Wie viel ist 1%d − %d?" % (a, b, a - b, a, b), str(10 + a - b), [str(a - b), str(10 + a - b + 1), str(10 + a + b) if a + b < 10 else str(10 + a - b - 1)],
               "Der Zehner bleibt: 1%d − %d = <b>%d</b>." % (a, b, 10 + a - b))


def plus():
    a = R.randint(11, 18)
    b = R.randint(1, 19 - a)
    if a % 10 + b > 9 or b < 1:
        return None
    pic = de(tenframe_svg(a, 2), "Zwanzigerfeld mit %d Punkten" % a) if R.random() < 0.3 else ""
    return mcq(pic + "%d + %d = ?" % (a, b), str(a + b), w(a + b) + [str(a % 10 + b)], "Einer: %d + %d = %d. Mit dem Zehner: <b>%d</b>." % (a % 10, b, a % 10 + b, a + b))


def minus():
    a = R.randint(12, 19)
    b = R.randint(1, a % 10)
    if b < 1:
        return None
    return mcq("%d − %d = ?" % (a, b), str(a - b), w(a - b) + [str(a % 10 - b) if a % 10 - b else "1"], "Einer: %d − %d = %d. Mit dem Zehner: <b>%d</b>." % (a % 10, b, a % 10 - b, a - b))


def zehner():
    kind = R.choice(["10plus", "minus_e", "20minus", "plus10"])
    e = R.randint(1, 9)
    if kind == "10plus":
        return mcq("10 + %d = ?" % e, str(10 + e), [str(10 * e + 1) if e > 1 else "12", str(e), str(11 + e)], "Ein Zehner und %d Einer: <b>%d</b>." % (e, 10 + e))
    if kind == "minus_e":
        return mcq("1%d − %d = ?" % (e, e), "10", [str(e), "1", "11"], "Die Einer sind weg, der Zehner bleibt: <b>10</b>.")
    if kind == "20minus":
        return mcq("20 − %d = ?" % e, str(20 - e), [str(20 - e + 1), str(10 - e), str(20 - e - 1)], "Von 20 zurück: 20 − %d = <b>%d</b>." % (e, 20 - e))
    return mcq("%d + 10 = ?" % e, str(10 + e), [str(e + 1), str(10 * e + 1) if e > 1 else "12", str(11 + e)], "%d und ein Zehner: <b>%d</b>." % (e, 10 + e))


def platz():
    a = R.randint(11, 17)
    b = R.randint(1, 19 - a)
    if a % 10 + b > 9:
        return None
    c = a + b
    kind = R.choice(["plus", "minus"])
    if kind == "plus":
        return mcq("%d + ? = %d" % (a, c), str(b), [str(c), str(b + 1), str(b + 10)], "Von %d bis %d sind es <b>%d</b>." % (a, c, b))
    return mcq("%d − ? = %d" % (c, a), str(b), [str(a), str(b + 1), str(c + a) if c + a < 40 else str(b + 2)], "%d − <b>%d</b> = %d." % (c, b, a))


GESCH = [("%s hat 1%d Murmeln. %s gewinnt %d dazu. Wie viele Murmeln hat %s jetzt?", "+p"),
         ("Im Bus sitzen 1%d Kinder. %d Kinder steigen aus. Wie viele Kinder sitzen noch im Bus?", "-"),
         ("Im Korb liegen 1%d Eier. %d Eier gehen kaputt. Wie viele Eier sind noch ganz?", "-"),
         ("Auf dem Spielplatz spielen 1%d Kinder. %d Kinder kommen dazu. Wie viele Kinder spielen jetzt?", "+"),
         ("%s hat 1%d Sticker. %s verschenkt %d Sticker. Wie viele Sticker hat %s noch?", "-p"),
         ("In der Dose sind 1%d Kekse. Oma legt %d Kekse dazu. Wie viele Kekse sind jetzt in der Dose?", "+")]


def geschichte():
    t, kind = R.choice(GESCH)
    e = R.randint(1, 8)
    p = KIDS.next()
    if kind.startswith("+"):
        if e > 7:
            return None
        b = R.randint(2, 9 - e)
        r = 10 + e + b
    else:
        if e < 2:
            return None
        b = R.randint(2, e)
        r = 10 + e - b
    if kind.endswith("p"):
        q = t % (p[0], e, p[1].capitalize(), b, p[1])
    else:
        q = t % (e, b)
    other = 10 + e - b if kind.startswith("+") else 10 + e + b
    return mcq(q, str(r), [str(other) if other <= 20 else str(r + 2), str(r + 1), str(r - 10)],
               ("Es kommt etwas dazu: 1%d + %d = <b>%d</b>." if kind.startswith("+") else "Es geht etwas weg: 1%d − %d = <b>%d</b>.") % (e, b, r))


def main():
    seen = set()
    sets = [
        ("Aufgaben mit dem Zehner", mix(R, seen, [(zehner, 20)])),
        ("Kleine Aufgabe, große Aufgabe", mix(R, seen, [(analog, 20)])),
        ("Plus und minus im zweiten Zehner", mix(R, seen, [(plus, 10), (minus, 10)])),
        ("Welche Zahl fehlt?", mix(R, seen, [(platz, 20)])),
        ("Rechengeschichten", mix(R, seen, [(geschichte, 20)])),
    ]
    body = lesson(
        ["Bei 13 + 4 rechnest du nur mit den Einern: 3 + 4 = 7. Der Zehner bleibt: 17.",
         "Die kleine Aufgabe hilft bei der großen: 5 − 2 = 3, also 15 − 2 = 13.",
         "10 + 6 = 16 und 16 − 6 = 10.",
         "Prüfe dein Ergebnis: Es muss zwischen 10 und 20 liegen."],
        [example("14 + 5", ["4 + 5 = 9", "dazu der Zehner"], "19"),
         example("18 − 3", ["8 − 3 = 5", "dazu der Zehner"], "15")],
        [["13 + 4 = 7", "Den Zehner nicht vergessen: 17"],
         ["13 + 4 = 53", "Die 4 sind Einer: 17"],
         ["Bei „aussteigen“ plus rechnen", "Aussteigen heißt: weniger, also minus"]])
    faq = [
        {"q": "Was sind Analogieaufgaben?", "a": "Aufgaben, die nach demselben Muster gehen: 3 + 4 = 7 und 13 + 4 = 17. Die kleine Aufgabe hilft bei der großen."},
        {"q": "Was heißt „ohne Zehnerübergang“?", "a": "Die Einer bleiben unter 10, zum Beispiel 12 + 5. Aufgaben wie 8 + 5 gehen über die 10 und kommen danach."},
        {"q": "Welches Material hilft?", "a": "Das Zwanzigerfeld, eine Rechenkette mit 20 Perlen und Zehnerstangen."},
        {"q": "Wie prüft man das Ergebnis?", "a": "Mit der Umkehraufgabe: 17 − 4 = 13 zeigt, dass 13 + 4 = 17 stimmt."},
    ]
    make_unit(R, "plus-und-minus-bis-20", "Z",
              "Die Schülerinnen und Schüler addieren und subtrahieren im zweiten Zehner ohne Zehnerübergang, nutzen Analogien zum ersten Zehner und den Aufbau aus Zehner und Einern und lösen Rechengeschichten (Zusammenfassung).",
              "Plus und minus bis 20 ohne Zehnerübergang",
              "Plus und minus bis 20 Klasse 1 – Arbeitsblätter mit Lösungen",
              "Plus und minus bis 20",
              "Plus und minus bis 20 für Klasse 1: Aufgaben mit dem Zehner, kleine und große Aufgaben, Rechnen im zweiten Zehner, fehlende Zahlen und Rechengeschichten. 100 Übungsaufgaben mit Lösungen, kostenlos.",
              "3 + 4 = 7, also 13 + 4 = 17.",
              "Der Zehner bleibt.",
              body, faq, sets, 7, grade="klasse-1")


if __name__ == "__main__":
    main()
