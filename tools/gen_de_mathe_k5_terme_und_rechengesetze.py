# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 5: Terme und Rechengesetze（Leitidee Zahl und Operation, Sek I）
  python3 tools/gen_de_mathe_k5_terme_und_rechengesetze.py
Punkt vor Strich, Klammern zuerst, Distributivgesetz, Rechenvorteile bei der Multiplikation, Terme aus Texten aufstellen.
Fehler: von links nach rechts gerechnet (3 + 4 · 5 = 35), Klammer übersehen, beim Ausklammern einen Summanden vergessen.
"""
import random
from de_common import mcq, num, lesson, example, make_unit, mix, MAL, GETEILT, table

R = random.Random(49506)


def punkt():
    kind = R.choice(["plusmal", "malplus", "minusmal", "durch", "zwei"])
    a, b, c = R.randint(2, 30), R.randint(2, 12), R.randint(2, 12)
    if kind == "plusmal":
        r, links = a + b * c, (a + b) * c
        t = "%d + %d %s %d" % (a, b, MAL, c)
        e = "Erst %d %s %d = %d, dann %d + %d = <b>%s</b>." % (b, MAL, c, b * c, a, b * c, num(r))
    elif kind == "malplus":
        r, links = b * c + a, b * (c + a)
        t = "%d %s %d + %d" % (b, MAL, c, a)
        e = "Erst %d %s %d = %d, dann + %d = <b>%s</b>." % (b, MAL, c, b * c, a, num(r))
        links = r + 1 if links == r else links
    elif kind == "minusmal":
        a = R.randint(b * c + 1, b * c + 60)
        r, links = a - b * c, (a - b) * c
        t = "%d − %d %s %d" % (a, b, MAL, c)
        e = "Erst %d %s %d = %d, dann %d − %d = <b>%s</b>." % (b, MAL, c, b * c, a, b * c, num(r))
    elif kind == "durch":
        q = R.randint(2, 12)
        t = "%d + %d %s %d" % (a, b * q, GETEILT, b)
        r = a + q
        links = (a + b * q) // b if (a + b * q) % b == 0 else a + b * q - b
        e = "Erst %d %s %d = %d, dann %d + %d = <b>%s</b>." % (b * q, GETEILT, b, q, a, q, num(r))
    else:
        d = R.randint(2, 9)
        r = a * b + c * d
        t = "%d %s %d + %d %s %d" % (a, MAL, b, c, MAL, d)
        links = (a * b + c) * d
        e = "%d + %d = <b>%s</b>." % (a * b, c * d, num(r))
    return mcq("%s = ?" % t, num(r), [num(links), num(r + 1), num(r + 10)], e)


def klammer():
    a, b, c = R.randint(2, 30), R.randint(2, 30), R.randint(2, 9)
    kind = R.choice(["mal", "minus", "durch", "doppelt"])
    if kind == "mal":
        r = (a + b) * c
        return mcq("(%d + %d) %s %d = ?" % (a, b, MAL, c), num(r), [num(a + b * c), num(r + c), num(r - a)], "Klammer zuerst: %d. Dann %d %s %d = <b>%s</b>." % (a + b, a + b, MAL, c, num(r)))
    if kind == "minus":
        x, y = R.randint(40, 99), R.randint(5, 30)
        r = x - (y + c)
        return mcq("%d − (%d + %d) = ?" % (x, y, c), num(r), [num(x - y + c), num(r + 1), num(x + y + c)], "Klammer zuerst: %d + %d = %d. %d − %d = <b>%s</b>." % (y, c, y + c, x, y + c, num(r)))
    if kind == "durch":
        q = R.randint(2, 9)
        s = q * c
        a = R.randint(1, s - 1)
        r = s // c
        return mcq("(%d + %d) %s %d = ?" % (a, s - a, GETEILT, c), num(r), [num(a + (s - a) // c) if (s - a) % c == 0 else num(r + a), num(r + 1), num(r * c)],
                   "Klammer zuerst: %d. %d %s %d = <b>%s</b>." % (s, s, GETEILT, c, num(r)))
    x, y = R.randint(10, 30), R.randint(2, 9)
    r = (x - y) * (c + 1)
    return mcq("(%d − %d) %s (%d + 1) = ?" % (x, y, MAL, c), num(r), [num(x - y * c + 1), num(r + x), num(r - c)],
               "Beide Klammern zuerst: %d und %d. %d %s %d = <b>%s</b>." % (x - y, c + 1, x - y, MAL, c + 1, num(r)))


def distributiv():
    kind = R.choice(["fast100", "ausklammern", "zerlegen", "minus"])
    if kind == "fast100":
        a = R.randint(3, 19)
        b = R.choice([98, 99, 101, 102, 199, 201, 49, 51])
        base = round(b, -1) if b < 100 else round(b, -2)
        r = a * b
        return mcq("Rechne geschickt: %d %s %d" % (a, MAL, b), num(r), [num(a * base), num(a * base + (b - base)), num(r + a)],
                   "%d %s %d %s %d %s %d = %s %s %d = <b>%s</b>." % (a, MAL, base, "+" if b > base else "−", a, MAL, abs(b - base), num(a * base), "+" if b > base else "−", a * abs(b - base), num(r)))
    if kind == "ausklammern":
        a = R.randint(3, 25)
        b = R.randint(11, 89)
        c = R.choice([100, 50, 20, 200]) - b
        if c <= 0:
            return None
        r = a * (b + c)
        return mcq("Rechne geschickt: %d %s %d + %d %s %d" % (a, MAL, b, a, MAL, c), num(r), [num(a * b + c), num(r + a), num(a + b + c)],
                   "Ausklammern: %d %s (%d + %d) = %d %s %d = <b>%s</b>." % (a, MAL, b, c, a, MAL, b + c, num(r)))
    if kind == "zerlegen":
        a = R.randint(12, 19)
        b = R.randint(3, 9)
        r = a * b
        return mcq("Welche Rechnung passt zu %d %s %d?" % (a, MAL, b), "10 %s %d + %d %s %d" % (MAL, b, a - 10, MAL, b),
                   ["10 %s %d + %d" % (MAL, b, a - 10), "10 + %d %s %d" % (a - 10, MAL, b), "10 %s %d %s %d" % (MAL, b, MAL, a - 10)],
                   "Zerlege %d in 10 + %d und multipliziere beide Teile: 10 %s %d + %d %s %d = <b>%s</b>." % (a, a - 10, MAL, b, a - 10, MAL, b, num(r)))
    a = R.randint(3, 15)
    b = R.randint(110, 190)
    c = b - 100
    r = a * 100
    return mcq("Rechne geschickt: %d %s %d − %d %s %d" % (a, MAL, b, a, MAL, c), num(r), [num(a * b - c), num(r + a), num(a * (b + c))],
               "Ausklammern: %d %s (%d − %d) = %d %s 100 = <b>%s</b>." % (a, MAL, b, c, a, MAL, num(r)))


def vorteil():
    kind = R.choice(["25", "5", "125", "gesetz"])
    if kind in ("25", "5", "125"):
        f = int(kind)
        g = {25: 4, 5: 2, 125: 8}[f]
        x = R.randint(3, 49)
        r = f * x * g
        order = R.choice([(f, x, g), (g, x, f), (x, f, g)])
        return mcq("Rechne geschickt: %d %s %d %s %d" % (order[0], MAL, order[1], MAL, order[2]), num(r), [num(r + x), num(r // 10) if r % 10 == 0 else num(r - 1), num(f * x + g)],
                   "Vertausche: %d %s %d = %d, dann %d %s %d = <b>%s</b>." % (f, MAL, g, f * g, f * g, MAL, x, num(r)))
    items = [("Welches Gesetz zeigt 7 %s 13 = 13 %s 7?" % (MAL, MAL), "Kommutativgesetz", ["Assoziativgesetz", "Distributivgesetz", "Punkt vor Strich"]),
             ("Welches Gesetz zeigt (4 %s 9) %s 25 = 9 %s (4 %s 25)?" % (MAL, MAL, MAL, MAL), "Kommutativ- und Assoziativgesetz", ["nur Distributivgesetz", "Punkt vor Strich", "Es gilt kein Gesetz"]),
             ("Welches Gesetz zeigt 6 %s (10 + 3) = 6 %s 10 + 6 %s 3?" % (MAL, MAL, MAL), "Distributivgesetz", ["Kommutativgesetz", "Assoziativgesetz", "Punkt vor Strich"]),
             ("Gilt (48 %s 8) %s 2 = 48 %s (8 %s 2)?" % (GETEILT, GETEILT, GETEILT, GETEILT), "Nein: links 3, rechts 12.", ["Ja, beide sind 3.", "Ja, beide sind 12.", "Ja, das Assoziativgesetz gilt immer."])]
    q, a, w = R.choice(items)
    return mcq(q, a, w, "<b>%s</b>" % a)


TEXTE = [("Addiere 12 und 8 und multipliziere die Summe mit 5.", "(12 + 8) %s 5" % MAL, "100", ["12 + 8 %s 5" % MAL, "12 %s 8 + 5" % MAL, "(12 %s 8) + 5" % MAL]),
         ("Multipliziere 7 mit der Differenz von 20 und 6.", "7 %s (20 − 6)" % MAL, "98", ["7 %s 20 − 6" % MAL, "(7 %s 20) − 6" % MAL, "7 %s 6 − 20" % MAL]),
         ("Subtrahiere das Produkt von 4 und 9 von 50.", "50 − 4 %s 9" % MAL, "14", ["(50 − 4) %s 9" % MAL, "4 %s 9 − 50" % MAL, "50 − 4 + 9"]),
         ("Dividiere die Summe von 36 und 24 durch 6.", "(36 + 24) %s 6" % GETEILT, "10", ["36 + 24 %s 6" % GETEILT, "36 %s 6 + 24" % GETEILT, "6 %s (36 + 24)" % GETEILT]),
         ("Addiere zum Produkt von 6 und 8 die Zahl 12.", "6 %s 8 + 12" % MAL, "60", ["6 %s (8 + 12)" % MAL, "(6 + 8) %s 12" % MAL, "6 + 8 + 12"]),
         ("Multipliziere die Summe von 3 und 5 mit der Differenz von 10 und 4.", "(3 + 5) %s (10 − 4)" % MAL, "48", ["3 + 5 %s 10 − 4" % MAL, "(3 + 5) %s 10 − 4" % MAL, "3 + 5 %s (10 − 4)" % MAL]),
         ("Subtrahiere 15 von der Summe von 40 und 25.", "40 + 25 − 15", "50", ["15 − (40 + 25)", "40 − 25 + 15", "40 + (25 + 15)"]),
         ("Dividiere 100 durch die Differenz von 30 und 10.", "100 %s (30 − 10)" % GETEILT, "5", ["100 %s 30 − 10" % GETEILT, "(100 − 30) %s 10" % GETEILT, "(30 − 10) %s 100" % GETEILT]),
         ("Verdopple die Summe von 17 und 23.", "2 %s (17 + 23)" % MAL, "80", ["2 %s 17 + 23" % MAL, "17 + 23 + 2", "2 + 17 + 23"]),
         ("Addiere den Quotienten von 56 und 8 zum Produkt von 3 und 4.", "56 %s 8 + 3 %s 4" % (GETEILT, MAL), "19", ["(56 %s 8 + 3) %s 4" % (GETEILT, MAL), "56 %s (8 + 3) %s 4" % (GETEILT, MAL), "56 %s 8 %s 3 + 4" % (GETEILT, MAL)])]


def texte():
    order = list(range(len(TEXTE)))
    R.shuffle(order)
    st = {"i": 0, "w": 0}

    def mk():
        if st["i"] >= 2 * len(order):
            return None
        k = order[st["i"] % len(order)]
        second = st["i"] >= len(order)
        st["i"] += 1
        q, term, val, w = TEXTE[k]
        if not second:
            return mcq("Welcher Term passt? „%s“" % q, term, w, "Was zuerst gerechnet wird, kommt in Klammern (außer Punkt vor Strich regelt es schon): <b>%s</b>." % term)
        return mcq("Berechne: „%s“" % q, val, [str(int(val) + 10), str(int(val) - 2), str(int(val) * 2)], "%s = <b>%s</b>." % (term, val))
    return mk


def main():
    seen = set()
    sets = [
        ("Punkt vor Strich", mix(R, seen, [(punkt, 20)])),
        ("Klammern zuerst", mix(R, seen, [(klammer, 20)])),
        ("Das Distributivgesetz", mix(R, seen, [(distributiv, 20)])),
        ("Rechenvorteile nutzen", mix(R, seen, [(vorteil, 20)])),
        ("Terme aus Texten", mix(R, seen, [(texte(), 20)])),
    ]
    body = lesson(
        ["Ein <b>Term</b> ist ein Rechenausdruck wie 3 + 4 %s 5." % MAL,
         "Reihenfolge: <b>Klammern zuerst</b>, dann <b>Punkt vor Strich</b> (· und : vor + und −), sonst von links nach rechts.",
         "<b>Distributivgesetz</b>: 6 %s (10 + 3) = 6 %s 10 + 6 %s 3. Damit kannst du geschickt rechnen und ausklammern." % (MAL, MAL, MAL),
         "Bei der Multiplikation darfst du vertauschen und zusammenfassen: 25 %s 17 %s 4 = 100 %s 17." % (MAL, MAL, MAL)],
        [example("3 + 4 %s 5" % MAL, ["erst 4 %s 5 = 20" % MAL, "dann 3 + 20"], "23"),
         example("8 %s 99" % MAL, ["8 %s 100 − 8 %s 1" % (MAL, MAL), "800 − 8"], "792")],
        [["3 + 4 %s 5 = 35" % MAL, "Punkt vor Strich: 23"],
         ["50 − (20 + 5) = 35", "Klammer zuerst: 50 − 25 = 25"],
         ["7 %s 13 + 7 %s 7 = 7 %s 13 + 7" % (MAL, MAL, MAL), "Ausklammern: 7 %s (13 + 7) = 140" % MAL]],
        extra=table(["Regel", "Beispiel"], [["Klammern zuerst", "(2 + 3) %s 4 = 20" % MAL], ["Punkt vor Strich", "2 + 3 %s 4 = 14" % MAL], ["von links nach rechts", "20 − 5 − 3 = 12"]]))
    faq = [
        {"q": "Was bedeutet Punkt vor Strich?", "a": "Mal und geteilt (Punktrechnung) werden vor plus und minus (Strichrechnung) gerechnet, wenn keine Klammern etwas anderes sagen."},
        {"q": "Was ist das Distributivgesetz?", "a": "Eine Zahl, die mit einer Summe multipliziert wird, kann mit jedem Summanden einzeln multipliziert werden: 6 · (10 + 3) = 6 · 10 + 6 · 3."},
        {"q": "Wozu braucht man Rechengesetze?", "a": "Um geschickt im Kopf zu rechnen, zum Beispiel 25 · 17 · 4 = 100 · 17 = 1700."},
        {"q": "Wie stellt man aus einem Text einen Term auf?", "a": "Man sucht die Rechenwörter (Summe, Differenz, Produkt, Quotient) und setzt Klammern um das, was zuerst gerechnet werden soll."},
    ]
    make_unit(R, "terme-und-rechengesetze", "Z",
              "Die Schülerinnen und Schüler berechnen Terme unter Beachtung der Vorrangregeln, nutzen Kommutativ-, Assoziativ- und Distributivgesetz zum vorteilhaften Rechnen und übersetzen Texte in Terme (Zusammenfassung).",
              "Terme und Rechengesetze",
              "Punkt vor Strich und Rechengesetze Klasse 5 – Arbeitsblätter mit Lösungen",
              "Terme und Rechengesetze",
              "Terme und Rechengesetze für Klasse 5: Punkt vor Strich, Klammern, Distributivgesetz, Rechenvorteile und Terme aus Texten. 100 Übungsaufgaben mit Lösungen, kostenlos.",
              "Klammern zuerst, dann Punkt vor Strich.",
              "6 · (10 + 3) = 6 · 10 + 6 · 3",
              body, faq, sets, 6, grade="klasse-5")


if __name__ == "__main__":
    main()
