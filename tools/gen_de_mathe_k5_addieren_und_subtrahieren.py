# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 5: Addieren und Subtrahieren（Leitidee Zahl und Operation, Sek I）
  python3 tools/gen_de_mathe_k5_addieren_und_subtrahieren.py
Fachbegriffe (Summe, Differenz, Summand, Minuend, Subtrahend), schriftlich addieren und subtrahieren mit großen Zahlen,
geschickt rechnen mit Kommutativ- und Assoziativgesetz, Platzhalter und Sachaufgaben.
Fehler: Übertrag vergessen, Differenz in falscher Reihenfolge gebildet, Summand und Summe verwechselt.
"""
import random
from de_common import mcq, num, lesson, example, make_unit, mix, Kids, table

R = random.Random(49504)
KIDS = Kids(R)


def begriffe():
    kind = R.choice(["summe", "differenz", "name", "name"])
    a, b = R.randint(120, 9800), R.randint(110, 9800)
    if kind == "summe":
        return mcq("Berechne die Summe von %s und %s." % (num(a), num(b)), num(a + b), [num(abs(a - b)), num(a * b) if a * b < 10 ** 8 else num(a + b + 100), num(a + b + 1000)],
                   "Summe heißt: addieren. %s + %s = <b>%s</b>." % (num(a), num(b), num(a + b)))
    if kind == "differenz":
        a, b = max(a, b), min(a, b)
        if a == b:
            return None
        return mcq("Berechne die Differenz von %s und %s." % (num(a), num(b)), num(a - b), [num(a + b), num(a - b + 1000), num(a - b - 10) if a - b > 10 else num(a - b + 10)],
                   "Differenz heißt: subtrahieren. %s − %s = <b>%s</b>." % (num(a), num(b), num(a - b)))
    items = [("In 245 + 318 = 563 heißt 563 …", "Summe", ["Summand", "Differenz", "Minuend"]),
             ("In 245 + 318 = 563 heißen 245 und 318 …", "Summanden", ["Summen", "Faktoren", "Subtrahenden"]),
             ("In 900 − 350 = 550 heißt 900 …", "Minuend", ["Subtrahend", "Differenz", "Summand"]),
             ("In 900 − 350 = 550 heißt 350 …", "Subtrahend", ["Minuend", "Differenz", "Summe"]),
             ("In 900 − 350 = 550 heißt 550 …", "Differenz", ["Summe", "Minuend", "Subtrahend"]),
             ("Wie heißt das Ergebnis einer Addition?", "Summe", ["Differenz", "Produkt", "Quotient"]),
             ("Wie heißt das Ergebnis einer Subtraktion?", "Differenz", ["Summe", "Produkt", "Quotient"]),
             ("Welche Rechenart gehört zur „Summe“?", "Addition", ["Subtraktion", "Multiplikation", "Division"]),
             ("Welche Rechenart gehört zur „Differenz“?", "Subtraktion", ["Addition", "Multiplikation", "Division"]),
             ("Die Summe zweier Zahlen ist 1000. Ein Summand ist 375. Wie heißt der andere Summand?", "625", ["1375", "725", "635"]),
             ("Der Minuend ist 2000, die Differenz ist 760. Wie groß ist der Subtrahend?", "1240", ["2760", "1340", "1260"])]
    q, a_, w = R.choice(items)
    return mcq(q, a_, w, "<b>%s</b>." % a_)


def schr_add():
    n = R.choice([2, 2, 3])
    nums = [R.randint(10 ** (R.randint(4, 6)), 10 ** 7) for _ in range(n)]
    s = sum(nums)
    w = [s - 10 ** R.randint(1, 4), s + 10 ** R.randint(1, 4), s - 1000 if s > 1000 else s + 1]
    return mcq("Rechne schriftlich: %s = ?" % " + ".join(num(x) for x in nums), num(s), [num(x) for x in w],
               "Stellengerecht untereinander schreiben, von rechts addieren und Überträge beachten: <b>%s</b>." % num(s))


def schr_sub():
    a = R.randint(10 ** 5, 10 ** 7)
    b = R.randint(10 ** 4, a - 1)
    r = a - b
    da, db = str(a), str(b).rjust(len(str(a)), "0")
    fehler = int("".join(str(abs(int(x) - int(y))) for x, y in zip(da, db)))
    w = [fehler if fehler != r else r + 100, r + 10 ** R.randint(1, 4), r - 10 ** R.randint(1, 3) if r > 1000 else r + 1]
    return mcq("Rechne schriftlich: %s − %s = ?" % (num(a), num(b)), num(r), [num(x) for x in w],
               "Probe: %s + %s = %s. Ergebnis: <b>%s</b>." % (num(r), num(b), num(a), num(r)))


def geschickt():
    kind = R.choice(["drei", "vier", "minus", "gesetz"])
    if kind == "drei":
        a = R.randint(11, 89)
        c = 100 - a
        b = R.randint(12, 98)
        s = a + b + c
        return mcq("Rechne geschickt: %d + %d + %d" % (a, b, c), num(s), [num(s + 10), num(s - 10), num(s + 1)],
                   "Vertausche: %d + %d = 100, dann + %d = <b>%s</b>." % (a, c, b, num(s)))
    if kind == "vier":
        a, b = R.randint(110, 890), R.randint(110, 890)
        c, d = 1000 - a, 1000 - b
        s = a + b + c + d
        return mcq("Rechne geschickt: %d + %d + %d + %d" % (a, b, c, d), num(s), [num(s + 100), num(s - 100), num(s + 10)],
                   "(%d + %d) + (%d + %d) = 1000 + 1000 = <b>%s</b>." % (a, c, b, d, num(s)))
    if kind == "minus":
        a = R.randint(2000, 9000)
        b, c = R.randint(100, 900), 0
        c = R.choice([1000, 500, 2000]) - b
        r = a - b - c
        if r <= 0 or c <= 0:
            return None
        return mcq("Rechne geschickt: %s − %d − %d" % (num(a), b, c), num(r), [num(a - b + c), num(r + 100), num(r - 10)],
                   "Fasse zusammen: %d + %d = %s. %s − %s = <b>%s</b>." % (b, c, num(b + c), num(a), num(b + c), num(r)))
    items = [("Welches Gesetz zeigt 37 + 85 = 85 + 37?", "Kommutativgesetz (Vertauschungsgesetz)", ["Assoziativgesetz (Verbindungsgesetz)", "Distributivgesetz", "Es gilt kein Gesetz"]),
             ("Welches Gesetz zeigt (24 + 59) + 41 = 24 + (59 + 41)?", "Assoziativgesetz (Verbindungsgesetz)", ["Kommutativgesetz (Vertauschungsgesetz)", "Distributivgesetz", "Es gilt kein Gesetz"]),
             ("Gilt 50 − 20 = 20 − 50?", "Nein, bei der Subtraktion darf man nicht vertauschen.", ["Ja, das Kommutativgesetz gilt immer.", "Ja, beide sind 30.", "Nur bei kleinen Zahlen."]),
             ("Gilt (80 − 30) − 10 = 80 − (30 − 10)?", "Nein, 40 ist nicht 60.", ["Ja, das Assoziativgesetz gilt auch hier.", "Ja, beide sind 40.", "Ja, beide sind 60."])]
    q, a_, w = R.choice(items)
    return mcq(q, a_, w, "<b>%s</b>" % a_)


def sache():
    kind = R.choice(["platz", "platz2", "einwohner", "auto", "spenden"])
    if kind == "platz":
        a, s = R.randint(1000, 50000), R.randint(60000, 99000)
        return mcq("%s + ? = %s" % (num(a), num(s)), num(s - a), [num(s + a), num(s - a + 1000), num(s - a - 100)], "Umkehraufgabe: %s − %s = <b>%s</b>." % (num(s), num(a), num(s - a)))
    if kind == "platz2":
        a, b = R.randint(5000, 90000), R.randint(1000, 4000)
        return mcq("? − %s = %s" % (num(b), num(a)), num(a + b), [num(a - b), num(a + b + 1000), num(a + b - 10)], "Umkehraufgabe: %s + %s = <b>%s</b>." % (num(a), num(b), num(a + b)))
    if kind == "einwohner":
        a, d = R.randint(80000, 400000), R.randint(1000, 9000)
        up = R.choice([True, False])
        r = a + d if up else a - d
        return mcq("Eine Stadt hatte %s Einwohner. In zehn Jahren ist die Zahl um %s %s. Wie viele Einwohner hat die Stadt jetzt?" % (num(a), num(d), "gestiegen" if up else "gesunken"),
                   num(r), [num(a - d if up else a + d), num(r + 1000), num(r - 100)], "%s %s %s = <b>%s</b>." % (num(a), "+" if up else "−", num(d), num(r)))
    if kind == "auto":
        a, b, c = R.randint(15000, 30000), R.randint(800, 3000), R.randint(500, 2500)
        r = a + b - c
        return mcq("Ein Auto kostet %s €. Extras kosten %s €. Der Händler gibt %s € Rabatt. Wie viel kostet das Auto am Ende?" % (num(a), num(b), num(c)), "%s €" % num(r),
                   ["%s €" % num(x) for x in (a + b + c, a - b - c, a + b)], "%s + %s − %s = <b>%s €</b>." % (num(a), num(b), num(c), num(r)))
    a, b, c = R.randint(1200, 4800), R.randint(1200, 4800), R.randint(1200, 4800)
    z = R.choice([10000, 15000])
    if a + b + c >= z:
        return None
    return mcq("Für einen neuen Spielplatz werden %s € gebraucht. Gesammelt wurden %s €, %s € und %s €. Wie viel Geld fehlt noch?" % (num(z), num(a), num(b), num(c)), "%s €" % num(z - a - b - c),
               ["%s €" % num(x) for x in (a + b + c, z - a - b, z - a - b - c + 1000)], "%s + %s + %s = %s. %s − %s = <b>%s €</b>." % (num(a), num(b), num(c), num(a + b + c), num(z), num(a + b + c), num(z - a - b - c)))


def main():
    seen = set()
    sets = [
        ("Fachbegriffe", mix(R, seen, [(begriffe, 20)])),
        ("Schriftlich addieren", mix(R, seen, [(schr_add, 20)])),
        ("Schriftlich subtrahieren", mix(R, seen, [(schr_sub, 20)])),
        ("Geschickt rechnen", mix(R, seen, [(geschickt, 20)])),
        ("Platzhalter und Sachaufgaben", mix(R, seen, [(sache, 20)])),
    ]
    body = lesson(
        ["<b>Addition</b>: Summand + Summand = Summe. <b>Subtraktion</b>: Minuend − Subtrahend = Differenz.",
         "Beim schriftlichen Rechnen schreibst du die Zahlen <b>stellengerecht</b> untereinander und beginnst rechts bei den Einern.",
         "Bei der Addition darfst du Summanden vertauschen (Kommutativgesetz) und beliebig zusammenfassen (Assoziativgesetz). Bei der Subtraktion nicht!",
         "Mit der Umkehraufgabe machst du die Probe."],
        [example("37 + 85 + 63", ["37 + 63 = 100", "100 + 85"], "185"),
         example("8000 − 275 − 725", ["275 + 725 = 1000", "8000 − 1000"], "7000")],
        [["Übertrag vergessen", "Jeden Übertrag klein notieren"],
         ["Bei der Subtraktion die kleinere von der größeren Ziffer abziehen", "Entbündeln oder Ergänzen"],
         ["50 − 20 = 20 − 50", "Bei der Subtraktion darf man nicht vertauschen"]],
        extra=table(["Rechenart", "Name der Zahlen", "Ergebnis"], [["Addition", "Summand + Summand", "Summe"], ["Subtraktion", "Minuend − Subtrahend", "Differenz"]]))
    faq = [
        {"q": "Was ist der Unterschied zwischen Summe und Summand?", "a": "Summanden sind die Zahlen, die addiert werden. Die Summe ist das Ergebnis."},
        {"q": "Warum darf man bei der Subtraktion nicht vertauschen?", "a": "Weil 50 − 20 = 30, aber 20 − 50 nicht 30 ist. Das Kommutativgesetz gilt nur für Addition und Multiplikation."},
        {"q": "Wie macht man die Probe bei der Subtraktion?", "a": "Man addiert die Differenz und den Subtrahenden. Es muss der Minuend herauskommen."},
        {"q": "Was bedeutet geschickt rechnen?", "a": "Man nutzt die Rechengesetze, um Zahlen so zu kombinieren, dass glatte Zahlen wie 100 oder 1000 entstehen."},
    ]
    make_unit(R, "addieren-und-subtrahieren", "Z",
              "Die Schülerinnen und Schüler addieren und subtrahieren natürliche Zahlen im Kopf und schriftlich, verwenden die Fachbegriffe, nutzen Rechengesetze zum vorteilhaften Rechnen und lösen Sachaufgaben (Zusammenfassung).",
              "Addieren und Subtrahieren",
              "Addieren und Subtrahieren Klasse 5 – Arbeitsblätter mit Lösungen",
              "Addieren und Subtrahieren",
              "Addieren und Subtrahieren für Klasse 5: Summe und Differenz, schriftlich rechnen mit großen Zahlen, Rechengesetze, geschickt rechnen und Sachaufgaben. 100 Übungsaufgaben mit Lösungen, kostenlos.",
              "Summand + Summand = Summe",
              "Minuend − Subtrahend = Differenz",
              body, faq, sets, 4, grade="klasse-5")


if __name__ == "__main__":
    main()
