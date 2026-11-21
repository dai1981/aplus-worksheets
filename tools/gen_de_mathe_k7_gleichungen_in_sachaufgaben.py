# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 7: Gleichungen in Sachaufgaben（Leitidee Funktionaler Zusammenhang, Sek I）
  python3 tools/gen_de_mathe_k7_gleichungen_in_sachaufgaben.py
Zahlenrätsel, Altersaufgaben, Geometrie (Umfang, Winkel), Tarife vergleichen, Verteilungsaufgaben, Bewegungsaufgaben – Gleichung aufstellen, lösen, Antwort.
Fehler: Variable für die falsche Größe gewählt, eine Bedingung vergessen, die Lösung der Gleichung ist nicht die gefragte Größe.
"""
import random
from de_common import lesson, example, make_unit, mix, Kids, MAL, table
from de_k6 import dz
from de_k7 import mcq, eur

R = random.Random(49709)
KIDS = Kids(R)


def raetsel():
    kind = R.choice(["a", "b", "c", "d"])
    x = R.randint(3, 30)
    if kind == "a":
        a, b = R.randint(2, 7), R.randint(3, 25)
        r = a * x - b
        if r <= 0:
            return None
        q = "Wenn man eine Zahl mit %d multipliziert und dann %d subtrahiert, erhält man %d. Wie heißt die Zahl?" % (a, b, r)
        return mcq(q, str(x), [str((r - b) // a) if (r - b) % a == 0 else str(x - 1), str(r + b), str(x + 1)], "Gleichung: %dx − %d = %d. %dx = %d, <b>x = %d</b>." % (a, b, r, a, r + b, x))
    if kind == "b":
        a = R.randint(2, 6)
        r = a * (x + 4)
        q = "Addiert man zu einer Zahl 4 und multipliziert die Summe mit %d, erhält man %d. Wie heißt die Zahl?" % (a, r)
        return mcq(q, str(x), [str((r - 4) // a) if (r - 4) % a == 0 else str(x + 4), str(r // a), str(x - 4)], "Gleichung: %d(x + 4) = %d. x + 4 = %d, <b>x = %d</b>." % (a, r, r // a, x))
    if kind == "c":
        s = 3 * x + 3
        q = "Die Summe von drei aufeinanderfolgenden natürlichen Zahlen ist %d. Wie heißt die kleinste Zahl?" % s
        return mcq(q, str(x), [str(x + 1), str(s // 3), str(x - 1)] if s // 3 != x + 1 else [str(x + 1), str(x + 2), str(x - 1)],
                   "x + (x + 1) + (x + 2) = %d. 3x + 3 = %d, <b>x = %d</b>. Die Zahlen sind %d, %d und %d." % (s, s, x, x, x + 1, x + 2))
    d = R.randint(3, 12)
    s = 2 * x + d
    q = "Zwei Zahlen haben zusammen den Wert %d. Die eine ist um %d größer als die andere. Wie heißt die kleinere Zahl?" % (s, d)
    return mcq(q, str(x), [str(x + d), str((s + d) // 2) if (s + d) % 2 == 0 and (s + d) // 2 != x + d else str(x + 1), str(s // 2) if s // 2 != x else str(x - 1)],
               "x + (x + %d) = %d. 2x = %d, <b>x = %d</b>." % (d, s, s - d, x))


def alter():
    p, er = KIDS.next()
    kind = R.choice(["vater", "geschwister", "zukunft"])
    if kind == "vater":
        x = R.randint(8, 14)
        k = R.choice([3, 4])
        s = x + k * x
        return mcq("%s und die Mutter sind zusammen %d Jahre alt. Die Mutter ist %s so alt wie %s. Wie alt ist %s?" % (p, s, {3: "dreimal", 4: "viermal"}[k], p, p), "%d Jahre" % x, ["%d Jahre" % v for v in (k * x, s // k, s - k)],
                   "x + %dx = %d. %dx = %d, <b>x = %d</b>." % (k, s, k + 1, s, x))
    if kind == "geschwister":
        x = R.randint(4, 12)
        d = R.randint(2, 6)
        s = 2 * x + d
        return mcq("%s ist %d Jahre älter als sein Bruder. Zusammen sind sie %d Jahre alt. Wie alt ist der Bruder?" % (p, d, s) if er == "er" else "%s ist %d Jahre älter als ihr Bruder. Zusammen sind sie %d Jahre alt. Wie alt ist der Bruder?" % (p, d, s),
                   "%d Jahre" % x, ["%d Jahre" % v for v in (x + d, s // 2 if s // 2 != x else x + 1, s - d)],
                   "x + (x + %d) = %d. 2x = %d, <b>x = %d</b>." % (d, s, s - d, x))
    x = R.randint(5, 11)
    n = R.randint(16, 28)
    mm = 2 * (x + n) - n
    return mcq("%s ist %d Jahre alt, die Mutter %d. In wie vielen Jahren ist die Mutter genau doppelt so alt wie %s?" % (p, x, mm, p), "in %d Jahren" % n, ["in %d Jahren" % v for v in (mm - 2 * x, n + 2, mm - x - x // 2 if mm - x - x // 2 > 0 else n + 4)],
               "%d + t = 2 %s (%d + t). %d + t = %d + 2t, <b>t = %d</b>." % (mm, MAL, x, mm, 2 * x, n))


def geo():
    kind = R.choice(["rechteck", "dreieck", "winkel", "quadrat"])
    if kind == "rechteck":
        b = R.randint(3, 15)
        d = R.randint(2, 10)
        u = 2 * (b + b + d)
        return mcq("Ein Rechteck ist %d cm länger als breit. Sein Umfang beträgt %d cm. Wie breit ist es?" % (d, u), "%d cm" % b, ["%d cm" % v for v in (b + d, u // 4, (u - d) // 2)],
                   "2 %s (x + x + %d) = %d. 4x + %d = %d, <b>x = %d</b>." % (MAL, d, u, 2 * d, u, b))
    if kind == "dreieck":
        a = R.randint(3, 12)
        u = 3 * a + 6
        return mcq("Die Seiten eines Dreiecks sind x, x + 2 und x + 4 (in cm). Der Umfang ist %d cm. Wie lang ist die kürzeste Seite?" % u, "%d cm" % (a), ["%d cm" % v for v in (u // 3, a + 2, u - 6)],
                   "3x + 6 = %d. 3x = %d, <b>x = %d</b>." % (u, u - 6, a))
    if kind == "winkel":
        k = R.choice([2, 3, 4])
        x = R.choice([v for v in (15, 18, 20, 24, 25, 30, 36) if v * (1 + k + 1) < 180])
        rest = 180 - x - k * x
        return mcq("In einem Dreieck ist β %s so groß wie α, und γ = %d°. Wie groß ist α?" % ({2: "doppelt", 3: "dreimal", 4: "viermal"}[k], rest), "%d°" % x, ["%d°" % v for v in (k * x, (180 - rest) // k, 180 - rest)],
                   "x + %dx + %d = 180. %dx = %d, <b>x = %d°</b>." % (k, rest, k + 1, 180 - rest, x))
    a = R.randint(4, 15)
    d = R.randint(1, 5)
    return mcq("Verlängert man die Seiten eines Quadrats um je %d cm, wird der Umfang %d cm. Wie lang war eine Seite?" % (d, 4 * (a + d)), "%d cm" % a, ["%d cm" % v for v in (a + d, a + d + d, 4 * (a + d) // 4 - 2 * d if a - d > 0 else a + 2)],
               "4 %s (x + %d) = %d. x + %d = %d, <b>x = %d</b>." % (MAL, d, 4 * (a + d), d, a + d, a))


def tarif():
    kind = R.choice(["handy", "taxi", "verleih"])
    if kind == "handy":
        g1, p1 = R.choice([(5, 9), (8, 5), (10, 4)])
        g2, p2 = R.choice([(20, 2), (15, 3), (25, 1)])
        if p1 <= p2 or g2 <= g1 or (g2 - g1) % (p1 - p2):
            return None
        x = (g2 - g1) // (p1 - p2)
        return mcq("Tarif A: %d € Grundgebühr und %d ct pro Minute. Tarif B: %d € Grundgebühr und %d ct pro Minute. Bei wie vielen Minuten kosten beide gleich viel? (Rechne in ct.)" % (g1, p1, g2, p2),
                   "%d min" % (x * 100), ["%d min" % v for v in (x, (g2 + g1) * 100 // (p1 + p2), x * 100 + 100)],
                   "%d + %dx = %d + %dx (in ct). %dx = %d, <b>x = %d</b> Minuten." % (g1 * 100, p1, g2 * 100, p2, p1 - p2, (g2 - g1) * 100, x * 100))
    if kind == "taxi":
        g, k = R.choice([(4, 2), (3, 2), (5, 3)])
        t = g + k * R.randint(4, 20)
        x = (t - g) // k
        return mcq("Ein Taxi kostet %d € Grundpreis und %d € pro km. Eine Fahrt kostet %d €. Wie viele Kilometer wurden gefahren?" % (g, k, t), "%d km" % x, ["%d km" % v for v in (t // k, t - g, x + 1)],
                   "%d + %dx = %d. %dx = %d, <b>x = %d</b>." % (g, k, t, k, t - g, x))
    g1, p1, p2 = R.choice([(10, 4, 6), (6, 5, 8), (12, 3, 5), (15, 4, 7)])
    if g1 % (p2 - p1):
        return None
    x = g1 // (p2 - p1)
    return mcq("Fahrradverleih A: %d € Grundgebühr und %d € pro Stunde. Verleih B: keine Grundgebühr, %d € pro Stunde. Ab wie vielen Stunden ist A günstiger?" % (g1, p1, p2), "ab mehr als %d Stunden" % x, ["ab mehr als %d Stunden" % v for v in (g1 // p1, x + 2, g1 // p2 if g1 // p2 != x else x - 1)],
               "Gleich teuer: %d + %dx = %dx → x = %d. Danach ist A günstiger: <b>ab mehr als %d Stunden</b>." % (g1, p1, p2, x, x))


def verteilen():
    p1, _ = KIDS.next()
    p2, _ = KIDS.next()
    if p1 == p2:
        return None
    kind = R.choice(["mehr", "doppelt", "drei"])
    if kind == "mehr":
        x = R.randint(10, 60)
        d = R.randint(5, 20)
        s = 2 * x + d
        return mcq("%s und %s teilen sich %d €. %s bekommt %d € mehr als %s. Wie viel bekommt %s?" % (p1, p2, s, p1, d, p2, p2), eur(x), [eur(x + d), eur(s / 2), eur(s - d)],
                   "x + (x + %d) = %d. 2x = %d, <b>x = %d €</b>." % (d, s, s - d, x))
    if kind == "doppelt":
        x = R.randint(5, 40)
        s = 3 * x
        return mcq("%s und %s sammeln zusammen %d Pfandflaschen. %s sammelt doppelt so viele wie %s. Wie viele sammelt %s?" % (p1, p2, s, p1, p2, p2), str(x), [str(2 * x), str(s // 2), str(x + 2)],
                   "x + 2x = %d. 3x = %d, <b>x = %d</b>." % (s, s, x))
    x = R.randint(10, 40)
    s = x + 2 * x + (x + 10)
    return mcq("Drei Klassen sammeln %d € für einen Ausflug. Die 7b sammelt doppelt so viel wie die 7a, die 7c 10 € mehr als die 7a. Wie viel sammelt die 7a?" % s, eur(x), [eur(2 * x), eur(x + 10), eur(s / 3)],
               "x + 2x + (x + 10) = %d. 4x = %d, <b>x = %d €</b>." % (s, s - 10, x))


def main():
    seen = set()
    sets = [
        ("Zahlenrätsel", mix(R, seen, [(raetsel, 20)])),
        ("Altersaufgaben und Verteilen", mix(R, seen, [(alter, 10), (verteilen, 10)])),
        ("Geometrie", mix(R, seen, [(geo, 20)])),
        ("Tarife vergleichen", mix(R, seen, [(tarif, 12), (verteilen, 8)])),
        ("Gemischte Sachaufgaben", mix(R, seen, [(raetsel, 5), (alter, 5), (geo, 5), (tarif, 5)])),
    ]
    body = lesson(
        ["1. Lies genau und lege fest, wofür die Variable x steht (meist für die gesuchte Größe).",
         "2. Drücke alle anderen Größen mit x aus und stelle die Gleichung auf.",
         "3. Löse die Gleichung, mache die Probe am Text und schreibe einen Antwortsatz.",
         "Achte darauf, ob x schon die gesuchte Größe ist oder ob man noch weiterrechnen muss."],
        [example("Zusammen 52 €, Anna 8 € mehr als Ben", ["Ben: x, Anna: x + 8", "x + x + 8 = 52", "2x = 44"], "Ben 22 €, Anna 30 €"),
         example("Rechteck: 4 cm länger als breit, Umfang 40 cm", ["2(x + x + 4) = 40", "4x + 8 = 40"], "x = 8 cm")],
        [["x für die größere Zahl gewählt, aber die kleinere angegeben", "Klar aufschreiben: x = …"],
         ["Umfang: x + x + 4 = 40", "Jede Seite zweimal: 2(x + x + 4) = 40"],
         ["Nach der Lösung keine Antwort", "Prüfen, was gefragt ist, und einen Antwortsatz schreiben"]])
    faq = [
        {"q": "Wie stelle ich eine Gleichung zu einer Textaufgabe auf?", "a": "Lege fest, wofür x steht, drücke alle Größen mit x aus und setze die Bedingung aus dem Text als Gleichung."},
        {"q": "Welche Größe sollte ich x nennen?", "a": "Meist die kleinste oder die gesuchte Größe. Dann lassen sich die anderen leicht mit x ausdrücken."},
        {"q": "Wie prüfe ich meine Lösung?", "a": "Setze sie in den Text ein, nicht nur in die Gleichung. So merkst du auch Fehler beim Aufstellen."},
        {"q": "Wie vergleiche ich zwei Tarife?", "a": "Für jeden Tarif einen Term aufstellen, beide gleichsetzen und die Gleichung lösen. Die Lösung ist der Punkt, an dem beide gleich viel kosten."},
    ]
    make_unit(R, "gleichungen-in-sachaufgaben", "F",
              "Die Schülerinnen und Schüler übersetzen Sachsituationen in lineare Gleichungen, lösen sie und deuten die Lösung im Sachzusammenhang (Zahlenrätsel, Alter, Geometrie, Tarife, Verteilung) (Zusammenfassung).",
              "Gleichungen in Sachaufgaben",
              "Gleichungen aufstellen – Textaufgaben Klasse 7, Arbeitsblätter mit Lösungen",
              "Textaufgaben mit Gleichungen",
              "Textaufgaben mit Gleichungen für Klasse 7: Zahlenrätsel, Altersaufgaben, Geometrie, Tarife vergleichen und Verteilungen. 100 Aufgaben mit Lösungen, kostenlos.",
              "x festlegen – Gleichung aufstellen – lösen – Antwort.",
              "Probe immer am Text machen.",
              body, faq, sets, 9, grade="klasse-7")


if __name__ == "__main__":
    main()
