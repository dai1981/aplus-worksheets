# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 2: Multiplizieren verstehen（Leitidee Zahl und Operation）
  python3 tools/gen_de_mathe_k2_multiplizieren_verstehen.py
Gleiche Gruppen, Plusaufgabe und Malaufgabe, Punktefelder, Tauschaufgaben, Sachaufgaben.
Fehler: plus statt mal (3 · 4 = 7), Anzahl der Gruppen und Anzahl in jeder Gruppe verwechselt, ungleiche Gruppen als Malaufgabe.
"""
import random
from de_common import mcq, lesson, example, make_unit, mix, Kids, MAL
from de_k2 import gruppen, punktfeld, KINDS, DING

R = random.Random(49207)
KIDS = Kids(R)


def gleich():
    g, k = R.randint(2, 5), R.randint(2, 5)
    kind = R.choice(KINDS)
    pic = gruppen(g, k, kind)
    if R.random() < 0.5:
        ans = "%d %s %d = %d" % (g, MAL, k, g * k)
        return mcq(pic + "Welche Malaufgabe passt zum Bild?", ans,
                   ["%d + %d = %d" % (g, k, g + k), "%d %s %d = %d" % (g, MAL, k + 1, g * (k + 1)), "%d %s %d = %d" % (g + 1, MAL, k, (g + 1) * k)],
                   "%d Gruppen mit je %d: <b>%s</b>." % (g, k, ans))
    return mcq(pic + "Wie viele %s sind es insgesamt?" % DING[kind][1], str(g * k), [str(g + k), str(g * k + k), str(g * k - 1)],
               "%d Gruppen mit je %d: %d %s %d = <b>%d</b>." % (g, k, g, MAL, k, g * k))


def plus_mal():
    g, k = R.randint(2, 6), R.randint(2, 9)
    if R.random() < 0.5:
        q = " + ".join([str(k)] * g) + " = ?"
        ans = "%d %s %d" % (g, MAL, k)
        return mcq("Welche Malaufgabe passt? " + q, ans, ["%d %s %d" % (k, MAL, k) if k != g else "%d %s %d" % (g, MAL, k + 1), "%d + %d" % (g, k), "%d %s %d" % (g + 1, MAL, k)],
                   "Die %d kommt %d-mal vor: <b>%s</b> = %d." % (k, g, ans, g * k))
    ans = " + ".join([str(k)] * g)
    w = [" + ".join([str(g)] * k) if g != k and k <= 6 else " + ".join([str(k)] * (g + 1)), "%d + %d" % (g, k), " + ".join([str(k)] * (g - 1)) if g > 2 else " + ".join([str(k + 1)] * g)]
    return mcq("Welche Plusaufgabe passt zu %d %s %d?" % (g, MAL, k), ans, w,
               "%d %s %d heißt: %d-mal die %d. <b>%s</b> = %d." % (g, MAL, k, g, k, ans, g * k))


def feld():
    r, c = R.randint(2, 6), R.randint(2, 8)
    if r == c:
        return None
    pic = punktfeld(r, c)
    if R.random() < 0.5:
        return mcq(pic + "Wie viele Punkte sind es?", str(r * c), [str(r + c), str(r * c + c), str(r * c - r)],
                   "%d Reihen mit je %d Punkten: %d %s %d = <b>%d</b>." % (r, c, r, MAL, c, r * c))
    ans = "%d %s %d" % (r, MAL, c)
    return mcq(pic + "Welche Malaufgabe passt? (Zähle die Reihen zuerst.)", ans, ["%d + %d" % (r, c), "%d %s %d" % (r + 1, MAL, c), "%d %s %d" % (r, MAL, c - 1)],
               "%d Reihen mit je %d Punkten: <b>%s</b> = %d." % (r, c, ans, r * c))


def tausch():
    kind = R.choice(["tausch", "rechnen", "rechnen"])
    a, b = R.randint(2, 9), R.randint(2, 6)
    if a == b:
        return None
    if kind == "tausch":
        return mcq("%d %s %d = %d %s ?" % (a, MAL, b, b, MAL), str(a), [str(b), str(a * b), str(a + 1)],
                   "Tauschaufgabe: %d %s %d = %d %s <b>%d</b>. Beide ergeben %d." % (a, MAL, b, b, MAL, a, a * b))
    return mcq("%d %s %d = ?" % (b, MAL, a), str(a * b), [str(a + b), str(a * b + a), str(a * b - b)],
               "%s = <b>%d</b>." % (" + ".join([str(a)] * b), a * b))


SACHE = [("Fahrräder", "Räder", 2), ("Dreiräder", "Räder", 3), ("Autos", "Räder", 4), ("Hunde", "Beine", 4), ("Hühner", "Beine", 2),
         ("Hände", "Finger", 5), ("Marienkäfer", "Beine", 6), ("Spinnen", "Beine", 8), ("volle Eierkartons mit je 6 Eiern", "Eier", 6), ("Kleeblätter mit vier Blättern", "Blätter", 4),
         ("Tüten mit je 5 Äpfeln", "Äpfel", 5), ("Packungen mit je 10 Stiften", "Stifte", 10), ("Teller mit je 3 Keksen", "Kekse", 3)]


def sache():
    t, u, k = R.choice(SACHE)
    g = R.randint(2, 6)
    if k * g > 60:
        return None
    if t.startswith(("Tüten", "Packungen", "Teller", "volle")):
        q = "Es gibt %d %s. Wie viele %s sind das?" % (g, t, u)
    else:
        q = "Es sind %d %s. Wie viele %s haben sie zusammen?" % (g, t, u)
    return mcq(q, str(g * k), [str(g + k), str(g * k + k), str(g * k - g)],
               "%d-mal %d: %d %s %d = <b>%d</b>." % (g, k, g, MAL, k, g * k))


def main():
    seen = set()
    sets = [
        ("Gleiche Gruppen", mix(R, seen, [(gleich, 20)])),
        ("Plusaufgabe und Malaufgabe", mix(R, seen, [(plus_mal, 20)])),
        ("Punktefelder", mix(R, seen, [(feld, 20)])),
        ("Tauschaufgaben und Rechnen", mix(R, seen, [(tausch, 20)])),
        ("Sachaufgaben", mix(R, seen, [(sache, 20)])),
    ]
    body = lesson(
        ["Malnehmen ist eine kurze Schreibweise für gleiche Plusaufgaben.",
         "3 %s 4 heißt: 3-mal die 4. Also 4 + 4 + 4 = 12." % MAL,
         "Die erste Zahl sagt, wie viele Gruppen es sind. Die zweite Zahl sagt, wie viele in jeder Gruppe sind.",
         "Tauschaufgabe: 3 %s 4 und 4 %s 3 haben dasselbe Ergebnis." % (MAL, MAL)],
        [example("3 Teller mit je 5 Keksen", ["5 + 5 + 5", "3 %s 5" % MAL], "15 Kekse"),
         example("Punktefeld mit 2 Reihen und je 6 Punkten", ["2 %s 6" % MAL], "12 Punkte")],
        [["3 %s 4 = 7" % MAL, "3 %s 4 = 4 + 4 + 4 = 12" % MAL],
         ["Ungleiche Gruppen als Malaufgabe schreiben", "Mal nur bei gleich großen Gruppen"],
         ["Gruppen und Anzahl verwechseln", "Erste Zahl: wie oft. Zweite Zahl: wie viele"]])
    faq = [
        {"q": "Wann lernen Kinder das Malnehmen?", "a": "In Klasse 2. Zuerst verstehen sie die Malaufgabe als wiederholte Addition, dann lernen sie das kleine Einmaleins."},
        {"q": "Was bedeutet der Malpunkt?", "a": "In Deutschland schreibt man 3 · 4 mit einem Punkt. Man liest „drei mal vier“."},
        {"q": "Ist 3 · 4 dasselbe wie 4 · 3?", "a": "Das Ergebnis ist gleich (12). Im Bild bedeutet es aber etwas anderes: 3 Gruppen mit je 4 oder 4 Gruppen mit je 3."},
        {"q": "Wie hilft ein Punktefeld?", "a": "Man sieht die Reihen und die Punkte in jeder Reihe. Dreht man das Feld, sieht man die Tauschaufgabe."},
    ]
    make_unit(R, "multiplizieren-verstehen", "Z",
              "Die Schülerinnen und Schüler verstehen die Multiplikation als wiederholte Addition gleicher Summanden, stellen Malaufgaben mit Gruppen und Punktefeldern dar, nutzen Tauschaufgaben und lösen einfache Sachaufgaben (Zusammenfassung).",
              "Multiplizieren verstehen: Malaufgaben",
              "Malaufgaben verstehen Klasse 2 – Arbeitsblätter mit Lösungen",
              "Malaufgaben verstehen",
              "Multiplizieren verstehen für Klasse 2: gleiche Gruppen, Plusaufgabe und Malaufgabe, Punktefelder, Tauschaufgaben und Sachaufgaben. 100 Übungsaufgaben mit Lösungen, kostenlos.",
              "3 · 4 heißt 3-mal die 4.",
              "4 + 4 + 4 = 3 · 4 = 12",
              body, faq, sets, 7, grade="klasse-2")


if __name__ == "__main__":
    main()
