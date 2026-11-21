# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 4: Rechengesetze, Punkt vor Strich und Klammern（Leitidee Zahl und Operation）
  python3 tools/gen_de_mathe_k4_rechengesetze_und_klammern.py
Punkt vor Strich, Klammern zuerst, geschickt rechnen (Tausch- und Verbindungsgesetz), Verteilungsgesetz, Terme zu Sachaufgaben.
Fehler: von links nach rechts rechnen (3 + 4 · 5 = 35), Klammer ignorieren, Minus-Klammer falsch aufgelöst.
"""
import random
from de_common import mcq, num, lesson, example, make_unit, mix, Kids, MAL, GETEILT

R = random.Random(49106)
KIDS = Kids(R)


def pvs():
    kind = R.choice(["a+b*c", "a-b*c", "a*b+c", "a+b:c", "a*b-c*d", "a:b+c*d"])
    if kind == "a+b*c":
        a, b, c = R.randint(2, 60), R.randint(2, 9), R.randint(2, 9)
        t, r, wr = "%d + %d %s %d" % (a, b, MAL, c), a + b * c, (a + b) * c
    elif kind == "a-b*c":
        b, c = R.randint(2, 9), R.randint(2, 9)
        a = R.randint(b * c + 1, b * c + 60)
        t, r, wr = "%d − %d %s %d" % (a, b, MAL, c), a - b * c, (a - b) * c
    elif kind == "a*b+c":
        a, b, c = R.randint(2, 9), R.randint(2, 9), R.randint(2, 40)
        t, r, wr = "%d %s %d + %d" % (a, MAL, b, c), a * b + c, a * (b + c)
    elif kind == "a+b:c":
        c, q = R.randint(2, 9), R.randint(2, 9)
        b = c * q
        a = R.randint(2, 60)
        if (a + b) % c:
            wr = a + b + 1
        else:
            wr = (a + b) // c
        t, r = "%d + %d %s %d" % (a, b, GETEILT, c), a + q
    elif kind == "a*b-c*d":
        a, b, c, d = R.randint(4, 9), R.randint(4, 9), R.randint(2, 5), R.randint(2, 5)
        if a * b <= c * d:
            return None
        t, r, wr = "%d %s %d − %d %s %d" % (a, MAL, b, c, MAL, d), a * b - c * d, (a * b - c) * d
    else:
        b, q = R.randint(2, 9), R.randint(2, 9)
        a = b * q
        c, d = R.randint(2, 9), R.randint(2, 9)
        t, r, wr = "%d %s %d + %d %s %d" % (a, GETEILT, b, c, MAL, d), q + c * d, (q + c) * d
    w = [wr, r + 1, r - 1, r + 10]
    return mcq("%s = ?" % t, num(r), [num(x) for x in w if x > 0 and x != r],
               "Punkt vor Strich: Erst mal und geteilt, dann plus und minus. %s = <b>%s</b>." % (t, num(r)))


def klammer():
    kind = R.choice(["(a+b)*c", "a*(b-c)", "a-(b+c)", "(a-b):c", "a-(b-c)"])
    if kind == "(a+b)*c":
        a, b, c = R.randint(2, 30), R.randint(2, 30), R.randint(2, 9)
        t, r, wr = "(%d + %d) %s %d" % (a, b, MAL, c), (a + b) * c, a + b * c
    elif kind == "a*(b-c)":
        a, c = R.randint(2, 9), R.randint(2, 20)
        b = R.randint(c + 2, c + 30)
        t, r, wr = "%d %s (%d − %d)" % (a, MAL, b, c), a * (b - c), a * b - c
    elif kind == "a-(b+c)":
        b, c = R.randint(10, 90), R.randint(10, 90)
        a = R.randint(b + c + 10, b + c + 300)
        t, r, wr = "%d − (%d + %d)" % (a, b, c), a - b - c, a - b + c
    elif kind == "(a-b):c":
        c, q = R.randint(2, 9), R.randint(3, 20)
        b = R.randint(5, 80)
        a = b + c * q
        t, r = "(%d − %d) %s %d" % (a, b, GETEILT, c), q
        wr = a - b // c if b % c == 0 else q + c
    else:
        c = R.randint(5, 40)
        b = R.randint(c + 5, c + 80)
        a = R.randint(b + 10, b + 300)
        t, r, wr = "%d − (%d − %d)" % (a, b, c), a - (b - c), a - b - c
    w = [wr, r + 10, r - 1, r + 1]
    return mcq("%s = ?" % t, num(r), [num(x) for x in w if x > 0 and x != r],
               "Was in Klammern steht, rechnest du zuerst. %s = <b>%s</b>." % (t, num(r)))


def geschickt():
    kind = R.choice(["plus", "mal25", "mal5", "plus3"])
    if kind == "plus":
        a = R.randint(11, 89)
        b = 100 - a
        c = R.randint(12, 88)
        t = "%d + %d + %d" % (a, c, b)
        r = a + b + c
        e = "Tausche: %d + %d = 100, dann + %d = <b>%d</b>." % (a, b, c, r)
    elif kind == "mal25":
        c = R.randint(3, 19)
        t = "25 %s %d %s 4" % (MAL, c, MAL)
        r = 100 * c
        e = "25 %s 4 = 100, dann 100 %s %d = <b>%s</b>." % (MAL, MAL, c, num(r))
    elif kind == "mal5":
        c = R.randint(3, 29)
        t = "5 %s %d %s 2" % (MAL, c, MAL)
        r = 10 * c
        e = "5 %s 2 = 10, dann 10 %s %d = <b>%d</b>." % (MAL, MAL, c, r)
    else:
        a = R.randint(101, 499)
        b = R.choice([150, 250, 350]) - a % 100 if a % 100 < 50 else None
        if not b or b <= 0:
            return None
        c = R.randint(20, 300)
        t = "%d + %d + %d" % (a, c, b)
        r = a + b + c
        e = "Erst %d + %d = %d, dann + %d = <b>%d</b>." % (a, b, a + b, c, r)
    w = [r + 10, r - 10, r + 100, r + 1]
    return mcq("Rechne geschickt: %s" % t, num(r), [num(x) for x in w if x > 0 and x != r], e)


def verteilen():
    a = R.randint(3, 9)
    kind = R.choice(["minus", "plus"])
    if kind == "minus":
        k = R.choice([1, 2, 3])
        b = 100 - k
        ans = "%d %s 100 − %d %s %d" % (a, MAL, a, MAL, k)
        w = ["%d %s 100 − %d" % (a, MAL, k), "%d %s 100 + %d %s %d" % (a, MAL, a, MAL, k), "%d %s 90 − %d %s %d" % (a, MAL, a, MAL, 10 - k)]
        r = a * b
    else:
        b = R.randint(11, 49)
        if b % 10 == 0:
            return None
        ans = "%d %s %d + %d %s %d" % (a, MAL, b // 10 * 10, a, MAL, b % 10)
        w = ["%d %s %d + %d" % (a, MAL, b // 10 * 10, b % 10), "%d %s %d + %d %s %d" % (a, MAL, b // 10, a, MAL, b % 10), "%d + %d %s %d" % (a, b // 10 * 10, MAL, b % 10)]
        r = a * b
    return mcq("Welcher Rechenweg passt zu %d %s %d?" % (a, MAL, b), ans, w,
               "Zerlege %d und nimm <b>beide</b> Teile mal %d: %s = %s." % (b, a, ans, num(r)))


def term():
    p = KIDS.next()
    kind = R.choice(["kauf", "rest", "gruppen", "klammer"])
    if kind == "kauf":
        n, a, b = R.randint(2, 6), R.randint(2, 9), R.randint(3, 15)
        q = "%s kauft %d Hefte zu je %d € und ein Buch für %d €. Welcher Term passt?" % (p[0], n, a, b)
        ans = "%d %s %d + %d" % (n, MAL, a, b)
        w = ["(%d + %d) %s %d" % (n, b, MAL, a), "%d + %d + %d" % (n, a, b), "%d %s (%d + %d)" % (n, MAL, a, b)]
        r = n * a + b
    elif kind == "rest":
        have, n, a = R.choice([20, 50, 100]), R.randint(2, 6), R.randint(2, 9)
        if n * a >= have:
            return None
        q = "%s hat %d € und kauft %d Hefte zu je %d €. Welcher Term berechnet, wie viel Geld übrig bleibt?" % (p[0], have, n, a)
        ans = "%d − %d %s %d" % (have, n, MAL, a)
        w = ["(%d − %d) %s %d" % (have, n, MAL, a), "%d − %d − %d" % (have, n, a), "%d %s %d − %d" % (n, MAL, a, have)]
        r = have - n * a
    elif kind == "gruppen":
        a, b, c = R.randint(10, 30), R.randint(10, 30), R.randint(2, 6)
        if (a + b) % c:
            return None
        q = "In der 4a sind %d Kinder, in der 4b %d. Alle werden auf %d gleich große Gruppen verteilt. Welcher Term passt?" % (a, b, c)
        ans = "(%d + %d) %s %d" % (a, b, GETEILT, c)
        w = ["%d + %d %s %d" % (a, b, GETEILT, c), "%d %s %d + %d" % (a, GETEILT, c, b), "(%d + %d) %s %d" % (a, b, MAL, c)]
        r = (a + b) // c
    else:
        n, a, b = R.randint(3, 8), R.randint(3, 9), R.randint(2, 6)
        q = "Ein Kinoticket kostet %d €, eine Tüte Popcorn %d €. %d Kinder kaufen je ein Ticket und eine Tüte. Welcher Term passt?" % (a, b, n)
        ans = "%d %s (%d + %d)" % (n, MAL, a, b)
        w = ["%d %s %d + %d" % (n, MAL, a, b), "%d + %d + %d" % (n, a, b), "(%d + %d) + %d" % (n, a, b)]
        r = n * (a + b)
    return mcq(q, ans, w, "Der Term <b>%s</b> passt. Ergebnis: %s." % (ans, num(r)))


def main():
    seen = set()
    sets = [
        ("Punkt vor Strich", mix(R, seen, [(pvs, 20)])),
        ("Klammern zuerst", mix(R, seen, [(klammer, 20)])),
        ("Geschickt rechnen", mix(R, seen, [(geschickt, 20)])),
        ("Das Verteilungsgesetz", mix(R, seen, [(verteilen, 14), (pvs, 6)])),
        ("Terme zu Sachaufgaben", mix(R, seen, [(term, 20)])),
    ]
    body = lesson(
        ["<b>Klammern zuerst</b>: Was in Klammern steht, wird zuerst gerechnet.",
         "<b>Punkt vor Strich</b>: Mal (·) und geteilt (:) werden vor plus und minus gerechnet.",
         "Bei Plus und bei Mal darfst du <b>tauschen</b> und <b>zusammenfassen</b>: 25 · 7 · 4 = 25 · 4 · 7 = 700.",
         "Beim <b>Verteilungsgesetz</b> zerlegst du eine Zahl: 7 · 98 = 7 · 100 − 7 · 2 = 686."],
        [example("3 + 4 %s 5" % MAL, ["Punkt vor Strich: 4 %s 5 = 20" % MAL, "3 + 20 = 23"], "23"),
         example("(3 + 4) %s 5" % MAL, ["Klammer zuerst: 3 + 4 = 7", "7 %s 5 = 35" % MAL], "35")],
        [["3 + 4 %s 5 = 35" % MAL, "Erst 4 %s 5, dann plus 3: 23" % MAL],
         ["80 − (20 + 10) = 70", "Klammer zuerst: 80 − 30 = 50"],
         ["7 %s 98 = 7 %s 100 − 2" % (MAL, MAL), "Beide Teile mal 7: 700 − 14 = 686"]])
    faq = [
        {"q": "Was bedeutet Punkt vor Strich?", "a": "Mal und geteilt (Punktrechnungen) werden vor plus und minus (Strichrechnungen) gerechnet, wenn keine Klammern stehen."},
        {"q": "Darf man bei Minus tauschen?", "a": "Nein. Das Tauschgesetz gilt nur für Plus und Mal. 10 − 3 ist nicht 3 − 10."},
        {"q": "Wozu braucht man Rechengesetze?", "a": "Damit man geschickt im Kopf rechnen kann, zum Beispiel 25 · 4 zuerst oder 37 + 63 zuerst."},
        {"q": "Was ist ein Term?", "a": "Eine Rechenaufgabe ohne Ergebnis, zum Beispiel 3 · 4 + 5. Terme helfen, Sachaufgaben in einer Zeile aufzuschreiben."},
    ]
    make_unit(R, "rechengesetze-und-klammern", "Z",
              "Die Schülerinnen und Schüler nutzen Rechengesetze (Tausch-, Verbindungs- und Verteilungsgesetz) und die Regeln Klammern zuerst und Punkt vor Strich und stellen Terme zu Sachsituationen auf (Zusammenfassung).",
              "Punkt vor Strich, Klammern und Rechengesetze",
              "Punkt vor Strich und Klammern Klasse 4 – Arbeitsblätter mit Lösungen",
              "Punkt vor Strich",
              "Klasse 4: Punkt vor Strich, Klammerregel, Tausch- und Verbindungsgesetz, Verteilungsgesetz und Terme zu Sachaufgaben. 100 Übungsaufgaben mit Lösungen, kostenlos.",
              "Klammern zuerst, dann Punkt vor Strich.",
              "Bei Plus und Mal darfst du tauschen und zusammenfassen.",
              body, faq, sets, 6, grade="klasse-4")


if __name__ == "__main__":
    main()
