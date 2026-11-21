# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 2: Geteilt – aufteilen und verteilen（Leitidee Zahl und Operation）
  python3 tools/gen_de_mathe_k2_geteilt_aufteilen_und_verteilen.py
Verteilen (jeder bekommt gleich viel), aufteilen (Gruppen bilden), Geteiltaufgaben, Aufgabenfamilien mit Mal, Sachaufgaben.
Fehler: minus statt geteilt, Anzahl der Gruppen und Anzahl in jeder Gruppe verwechselt, falsche Umkehraufgabe.
"""
import random
from de_common import mcq, lesson, example, make_unit, mix, Kids, MAL, GETEILT
from de_k2 import gruppen, reihe, KINDS, DING

R = random.Random(49210)
KIDS = Kids(R)


def verteilen():
    g, k = R.randint(2, 5), R.randint(2, 5)
    n = g * k
    kind = R.choice(KINDS)
    pic = reihe(n, kind, per_row=10)
    return mcq(pic + "%d %s werden gerecht an %d Kinder verteilt. Wie viele bekommt jedes Kind?" % (n, DING[kind][1], g), str(k),
               [str(g) if g != k else str(k + 2), str(n - g), str(k + 1)],
               "%d %s %d = <b>%d</b>. Jedes Kind bekommt %s." % (n, GETEILT, g, k, "%d %s" % (k, DING[kind][1])))


def aufteilen():
    g, k = R.randint(2, 6), R.randint(2, 5)
    n = g * k
    kind = R.choice(KINDS)
    pic = gruppen(g, k, kind) if R.random() < 0.5 else reihe(n, kind, per_row=10)
    return mcq(pic + "%d %s werden in Gruppen zu je %d gelegt. Wie viele Gruppen gibt es?" % (n, DING[kind][1], k), str(g),
               [str(k) if g != k else str(g + 2), str(n - k), str(g + 1)],
               "%d %s %d = <b>%d</b> Gruppen." % (n, GETEILT, k, g))


def geteilt():
    k = R.choice([2, 5, 10, 2, 5, 10, 3, 4])
    a = R.randint(1, 10)
    n = a * k
    if R.random() < 0.7:
        return mcq("%d %s %d = ?" % (n, GETEILT, k), str(a), [str(n - k), str(a + 1), str(a - 1) if a > 1 else str(a + 2), str(k)],
                   "Welche Zahl mal %d gibt %d? %d %s %d = %d, also <b>%d</b>." % (k, n, a, MAL, k, n, a))
    return mcq("%d %s ? = %d" % (n, GETEILT, a), str(k), [str(k + 1), str(n - a), str(a)],
               "%d %s <b>%d</b> = %d, weil %d %s %d = %d." % (n, GETEILT, k, a, a, MAL, k, n))


def familie():
    a, b = R.randint(2, 9), R.randint(2, 9)
    if a == b:
        return None
    n = a * b
    kind = R.choice(["passt", "nicht", "umkehr"])
    if kind == "passt":
        ans = "%d %s %d = %d" % (n, GETEILT, a, b)
        return mcq("Welche Geteiltaufgabe gehört zu %d %s %d = %d?" % (a, MAL, b, n), ans,
                   ["%d − %d = %d" % (n, a, n - a), "%d %s %d = %d" % (n, GETEILT, a, b + 1), "%d %s %d = %d" % (a, MAL, b, n + a)],
                   "Umkehraufgabe: Wenn %d %s %d = %d, dann ist <b>%s</b>." % (a, MAL, b, n, ans))
    if kind == "nicht":
        good = ["%d %s %d = %d" % (a, MAL, b, n), "%d %s %d = %d" % (b, MAL, a, n), "%d %s %d = %d" % (n, GETEILT, a, b), "%d %s %d = %d" % (n, GETEILT, b, a)]
        bad = "%d %s %d = %d" % (a, GETEILT, b, n) if R.random() < 0.5 else "%d %s %d = %d" % (n, GETEILT, a, a)
        others = R.sample(good, 3)
        return mcq("Welche Aufgabe gehört <b>nicht</b> zur Aufgabenfamilie von %d, %d und %d?" % (a, b, n), bad, others,
                   "Zur Familie gehören zwei Malaufgaben und zwei Geteiltaufgaben. <b>%s</b> ist falsch." % bad)
    return mcq("%d %s %d = ? Denke an %d %s ? = %d." % (n, GETEILT, a, a, MAL, n), str(b), [str(b + 1), str(n - a), str(a)],
               "%d %s %d = %d, also %d %s %d = <b>%d</b>." % (a, MAL, b, n, n, GETEILT, a, b))


def sache():
    kind = R.choice(["kekse", "teams", "boote", "geld", "rest"])
    p = KIDS.next()
    g, k = R.randint(2, 6), R.randint(2, 8)
    n = g * k
    if kind == "kekse":
        return mcq("%s hat %d Kekse. %s verteilt sie gerecht an %d Freunde. Wie viele Kekse bekommt jeder?" % (p[0], n, p[1].capitalize(), g), str(k),
                   [str(n - g), str(k + 1), str(g) if g != k else str(k - 1)], "%d %s %d = <b>%d</b>." % (n, GETEILT, g, k))
    if kind == "teams":
        return mcq("%d Kinder spielen Fußball. Sie bilden Mannschaften mit je %d Kindern. Wie viele Mannschaften gibt es?" % (n, k), str(g),
                   [str(n - k), str(g + 1), str(k) if g != k else str(g + 2)], "%d %s %d = <b>%d</b>." % (n, GETEILT, k, g))
    if kind == "boote":
        k = R.choice([2, 3, 4])
        g = R.randint(3, 9)
        n = g * k
        return mcq("Am See fahren %d Kinder mit dem Tretboot. In jedes Boot passen %d Kinder. Wie viele Boote brauchen sie?" % (n, k), str(g),
                   [str(n - k), str(g + 1), str(g - 1)], "%d %s %d = <b>%d</b> Boote." % (n, GETEILT, k, g))
    if kind == "geld":
        k = R.choice([2, 5, 10])
        g = R.randint(2, 6)
        n = g * k
        return mcq("%d Geschwister bekommen zusammen %d €. Sie teilen gerecht. Wie viel bekommt jedes Kind?" % (g, n), "%d €" % k,
                   ["%d €" % x for x in (n - g, k + 1, g if g != k else k + 2)], "%d € %s %d = <b>%d €</b>." % (n, GETEILT, g, k))
    k = R.randint(3, 5)
    g = R.randint(2, 5)
    r = R.randint(1, k - 1)
    n = g * k + r
    return mcq("%s legt %d Murmeln in Säckchen zu je %d. Wie viele volle Säckchen gibt es?" % (p[0], n, k), str(g),
               [str(g + 1), str(r), str(n - k)],
               "%d %s %d = %d, es bleiben %d übrig. Volle Säckchen: <b>%d</b>." % (g * k, GETEILT, k, g, r, g) if r > 1 else
               "%d %s %d = %d, es bleibt 1 übrig. Volle Säckchen: <b>%d</b>." % (g * k, GETEILT, k, g, g))


def main():
    seen = set()
    sets = [
        ("Verteilen", mix(R, seen, [(verteilen, 20)])),
        ("Aufteilen", mix(R, seen, [(aufteilen, 20)])),
        ("Geteiltaufgaben", mix(R, seen, [(geteilt, 20)])),
        ("Aufgabenfamilien", mix(R, seen, [(familie, 20)])),
        ("Sachaufgaben", mix(R, seen, [(sache, 20)])),
    ]
    body = lesson(
        ["Beim <b>Verteilen</b> bekommt jeder gleich viel: 12 Äpfel an 3 Kinder, jedes bekommt 4.",
         "Beim <b>Aufteilen</b> bildest du gleich große Gruppen: 12 Äpfel in Tüten zu je 4, das sind 3 Tüten.",
         "Beides schreibt man mit dem Geteiltzeichen: 12 %s 3 = 4 und 12 %s 4 = 3." % (GETEILT, GETEILT),
         "Geteilt ist die Umkehrung von mal. Für 24 %s 6 denkst du: 6 %s ? = 24." % (GETEILT, MAL)],
        [example("15 Stifte an 5 Kinder", ["15 %s 5" % GETEILT, "5 %s 3 = 15" % MAL], "3 Stifte für jedes Kind"),
         example("Aufgabenfamilie 4, 6, 24", ["4 %s 6 = 24, 6 %s 4 = 24" % (MAL, MAL), "24 %s 4 = 6, 24 %s 6 = 4" % (GETEILT, GETEILT)], "4 Aufgaben")],
        [["12 %s 3 = 9 (minus gerechnet)" % GETEILT, "12 %s 3 = 4, weil 3 %s 4 = 12" % (GETEILT, MAL)],
         ["Gruppen und Anzahl verwechseln", "Genau lesen: Wie viele Gruppen? Wie viele in jeder Gruppe?"],
         ["4 %s 12 = 3 schreiben" % GETEILT, "Die große Zahl steht vorne: 12 %s 4 = 3" % GETEILT]])
    faq = [
        {"q": "Was ist der Unterschied zwischen Aufteilen und Verteilen?", "a": "Beim Verteilen ist die Anzahl der Empfänger bekannt (an 3 Kinder). Beim Aufteilen ist die Größe der Gruppen bekannt (je 4). Beide Aufgaben rechnet man mit geteilt."},
        {"q": "Welches Zeichen benutzt man in Deutschland für geteilt?", "a": "Den Doppelpunkt: 12 : 3 = 4. Man liest „zwölf geteilt durch drei“."},
        {"q": "Wie rechnet man Geteiltaufgaben schnell?", "a": "Mit dem Einmaleins: Für 35 : 5 sucht man die Zahl, die mal 5 gleich 35 ist. Das ist 7."},
        {"q": "Was ist eine Aufgabenfamilie?", "a": "Drei Zahlen, die zusammengehören, zum Beispiel 3, 5 und 15. Daraus bildet man 3 · 5, 5 · 3, 15 : 3 und 15 : 5."},
    ]
    make_unit(R, "geteilt-aufteilen-und-verteilen", "Z",
              "Die Schülerinnen und Schüler verstehen die Division als Aufteilen und Verteilen, lösen Geteiltaufgaben mit Hilfe des Einmaleins, nutzen den Zusammenhang von Multiplikation und Division und lösen Sachaufgaben (Zusammenfassung).",
              "Geteilt: aufteilen und verteilen",
              "Geteiltaufgaben Klasse 2 – Arbeitsblätter mit Lösungen",
              "Geteilt",
              "Geteilt für Klasse 2: Verteilen, Aufteilen, Geteiltaufgaben, Aufgabenfamilien mit Malaufgaben und Sachaufgaben. 100 Übungsaufgaben mit Lösungen, kostenlos.",
              "12 : 3 = 4, weil 3 · 4 = 12.",
              "Verteilen: jeder gleich viel. Aufteilen: gleich große Gruppen.",
              body, faq, sets, 10, grade="klasse-2")


if __name__ == "__main__":
    main()
