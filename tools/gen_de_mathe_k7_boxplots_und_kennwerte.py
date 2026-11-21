# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 7: Daten auswerten – Kennwerte und Boxplots（Leitidee Daten und Zufall, Sek I）
  python3 tools/gen_de_mathe_k7_boxplots_und_kennwerte.py
Minimum, Maximum, Spannweite, Median, unteres und oberes Quartil, Quartilsabstand, arithmetisches Mittel, Ausreißer, Boxplots lesen und vergleichen.
Fehler: Median ohne Sortieren, Quartile wie Mittelwerte berechnet, Box als Spannweite gelesen, Mittelwert und Median verwechselt.
"""
import random
from fractions import Fraction as Fr
from de_common import lesson, example, make_unit, mix, Kids, MAL, table, wrap, line, text, INK, RED, BLUE, FILL, GREEN
from de_k6 import dz
from de_k7 import mcq

R = random.Random(49716)
KIDS = Kids(R)
G = ":"


def med(xs):
    s = sorted(xs)
    n = len(s)
    return Fr(s[n // 2]) if n % 2 else Fr(s[n // 2 - 1] + s[n // 2], 2)


def quart(xs):
    s = sorted(xs)
    n = len(s)
    lo, hi = s[:n // 2], s[(n + 1) // 2:]
    return med(lo), med(s), med(hi)


def daten(n=None):
    n = n or R.choice([7, 8, 9, 10, 11])
    xs = [R.randint(2, 40) for _ in range(n)]
    return xs


def kennwert(kinds):
    xs = daten()
    q1, m, q3 = quart(xs)
    kind = R.choice(kinds)
    lst = ", ".join(map(str, xs))
    srt = ", ".join(map(str, sorted(xs)))
    if kind == "median":
        return mcq("Daten: %s. Bestimme den Median." % lst, dz(m), [dz(Fr(xs[len(xs) // 2])) if Fr(xs[len(xs) // 2]) != m else dz(m + 1), dz(Fr(sum(xs), len(xs))) if (Fr(sum(xs), len(xs)) * 100).denominator == 1 and Fr(sum(xs), len(xs)) != m else dz(m - 1), dz(q1)],
                   "Sortiert: %s. Der mittlere Wert: <b>%s</b>." % (srt, dz(m)))
    if kind == "q1":
        return mcq("Daten: %s. Bestimme das untere Quartil q<sub>u</sub>." % lst, dz(q1), [dz(m), dz(Fr(min(xs))), dz(q1 + 1) if q1 + 1 != m else dz(q3)],
                   "Sortiert: %s. Das untere Quartil ist der Median der unteren Hälfte: <b>%s</b>." % (srt, dz(q1)))
    if kind == "q3":
        return mcq("Daten: %s. Bestimme das obere Quartil q<sub>o</sub>." % lst, dz(q3), [dz(m), dz(Fr(max(xs))), dz(q3 - 1) if q3 - 1 != m else dz(q1)],
                   "Sortiert: %s. Das obere Quartil ist der Median der oberen Hälfte: <b>%s</b>." % (srt, dz(q3)))
    if kind == "qa":
        return mcq("Daten: %s. Wie groß ist der Quartilsabstand?" % lst, dz(q3 - q1), [dz(Fr(max(xs) - min(xs))), dz(q3 + q1), dz(m - q1)],
                   "Sortiert: %s. q<sub>u</sub> = %s, q<sub>o</sub> = %s. %s − %s = <b>%s</b>." % (srt, dz(q1), dz(q3), dz(q3), dz(q1), dz(q3 - q1)))
    return mcq("Daten: %s. Wie groß ist die Spannweite?" % lst, str(max(xs) - min(xs)), [str(max(xs) + min(xs)), dz(q3 - q1) if q3 - q1 != max(xs) - min(xs) else str(max(xs)), str(max(xs))],
               "Maximum − Minimum = %d − %d = <b>%d</b>." % (max(xs), min(xs), max(xs) - min(xs)))


def mittel():
    n = R.choice([5, 6, 8])
    xs = [R.randint(1, 50) for _ in range(n)]
    m = Fr(sum(xs), n)
    if (m * 100).denominator != 1:
        return None
    kind = R.choice(["mittel", "ausreisser"])
    if kind == "mittel":
        return mcq("Daten: %s. Berechne das arithmetische Mittel." % ", ".join(map(str, xs)), dz(m), [dz(med(xs)) if med(xs) != m else dz(m + 1), str(sum(xs)), dz(Fr(sum(xs), n - 1)) if (Fr(sum(xs), n - 1) * 100).denominator == 1 else dz(m + 2)],
                   "Summe %d, Anzahl %d: %d %s %d = <b>%s</b>." % (sum(xs), n, sum(xs), G, n, dz(m)))
    ys = [R.randint(10, 20) for _ in range(5)] + [R.randint(80, 120)]
    mm = Fr(sum(ys), 6)
    if (mm * 100).denominator != 1:
        return None
    md = med(ys)
    return mcq("Daten: %s. Welcher Kennwert beschreibt die Mitte hier besser?" % ", ".join(map(str, ys)), "der Median (%s), weil der Ausreißer %d den Mittelwert (%s) stark verzerrt" % (dz(md), max(ys), dz(mm)),
               ["der Mittelwert (%s), weil er alle Werte benutzt" % dz(mm), "die Spannweite (%d)" % (max(ys) - min(ys)), "das Maximum (%d)" % max(ys)],
               "Der Wert %d ist ein Ausreißer. Der Median %s ist robust, der Mittelwert %s nicht: <b>der Median</b>." % (max(ys), dz(md), dz(mm)))


def box_svg(mn, q1, m, q3, mx, lo=0, hi=50, step=5, label=None):
    W, x0, y = 420, 20, 40
    u = (W - 40) / float(hi - lo)
    X = lambda v: x0 + (float(v) - lo) * u
    s = [line(X(lo), y + 34, X(hi), y + 34, INK, 1.5)]
    for v in range(lo, hi + 1):
        if (v - lo) % step:
            s.append(line(X(v), y + 32, X(v), y + 36, INK, 0.8))
    for v in range(lo, hi + 1, step):
        s.append(line(X(v), y + 29, X(v), y + 39, INK, 1.4) + text(X(v), y + 53, str(v), 12, weight=500))
    s.append(line(X(mn), y, X(q1), y, INK, 2) + line(X(q3), y, X(mx), y, INK, 2))
    s.append(line(X(mn), y - 8, X(mn), y + 8, INK, 2) + line(X(mx), y - 8, X(mx), y + 8, INK, 2))
    s.append("<rect x='%.1f' y='%d' width='%.1f' height='24' fill='%s' stroke='%s' stroke-width='2'/>" % (X(q1), y - 12, X(q3) - X(q1), FILL, GREEN))
    s.append(line(X(m), y - 12, X(m), y + 12, RED, 3))
    if label:
        s.append(text(X(lo), y - 18, label, 12, anchor="start"))
    return wrap(W, y + 60, "".join(s), "Boxplot", lg=True)


def boxplot():
    vals = sorted(R.sample(range(0, 51, 2), 5))
    mn, q1, m, q3, mx = vals
    if q1 - mn < 4 or m - q1 < 2 or q3 - m < 2 or mx - q3 < 4:
        return None
    pic = box_svg(mn, q1, m, q3, mx)
    kind = R.choice(["median", "qa", "spann", "anteil", "q1"])
    if kind == "median":
        return mcq(pic + "Wie groß ist der Median?", str(m), [str(q1), str(q3), str((mn + mx) // 2) if (mn + mx) // 2 != m else str(m + 2)], "Der Strich in der Box ist der Median: <b>%d</b>." % m)
    if kind == "q1":
        return mcq(pic + "Wie groß ist das untere Quartil?", str(q1), [str(mn), str(m), str(q3)], "Der linke Rand der Box ist das untere Quartil: <b>%d</b>." % q1)
    if kind == "qa":
        return mcq(pic + "Wie groß ist der Quartilsabstand?", str(q3 - q1), [str(mx - mn), str(m - q1), str(q3)], "Breite der Box: %d − %d = <b>%d</b>." % (q3, q1, q3 - q1))
    if kind == "spann":
        return mcq(pic + "Wie groß ist die Spannweite?", str(mx - mn), [str(q3 - q1), str(mx), str(mx - m)], "Von Antenne zu Antenne: %d − %d = <b>%d</b>." % (mx, mn, mx - mn))
    return mcq(pic + "Etwa wie viel Prozent der Daten liegen zwischen %d und %d?" % (q1, q3), "50 %", ["25 %", "75 %", "100 %"], "In der Box liegen die mittleren Daten: etwa <b>50 %</b>.")


def vergleich():
    p1, p2 = "Klasse 7a", "Klasse 7b"
    a = sorted(R.sample(range(4, 47, 2), 5))
    b = sorted(R.sample(range(4, 47, 2), 5))
    if a[2] == b[2] or (a[3] - a[1]) == (b[3] - b[1]):
        return None
    pic = box_svg(*a, label="7a") + box_svg(*b, label="7b")
    kind = R.choice(["median", "streuung"])
    if kind == "median":
        best = p1 if a[2] > b[2] else p2
        return mcq(pic + "Die Boxplots zeigen Punkte in einem Test. Welche Klasse hat den höheren Median?", best, [p2 if best == p1 else p1, "Beide gleich.", "Das kann man nicht ablesen."],
                   "Median 7a: %d, 7b: %d. <b>%s</b>." % (a[2], b[2], best))
    best = p1 if a[3] - a[1] < b[3] - b[1] else p2
    return mcq(pic + "In welcher Klasse liegen die mittleren 50 % der Ergebnisse näher beieinander?", best, [p2 if best == p1 else p1, "Beide gleich.", "Das kann man nicht ablesen."],
               "Quartilsabstand 7a: %d, 7b: %d. Die schmalere Box: <b>%s</b>." % (a[3] - a[1], b[3] - b[1], best))


def main():
    seen = set()
    sets = [
        ("Median und Spannweite", mix(R, seen, [(lambda: kennwert(["median", "spann"]), 20)])),
        ("Mittelwert und Ausreißer", mix(R, seen, [(mittel, 20)])),
        ("Quartile", mix(R, seen, [(lambda: kennwert(["q1", "q3", "qa"]), 20)])),
        ("Boxplots lesen", mix(R, seen, [(boxplot, 20)])),
        ("Boxplots vergleichen", mix(R, seen, [(vergleich, 14), (boxplot, 6)])),
    ]
    body = lesson(
        ["<b>Median</b> (Zentralwert): Daten ordnen, der mittlere Wert. Bei gerader Anzahl der Mittelwert der beiden mittleren.",
         "<b>Unteres Quartil</b> q<sub>u</sub>: Median der unteren Hälfte. <b>Oberes Quartil</b> q<sub>o</sub>: Median der oberen Hälfte. <b>Quartilsabstand</b> = q<sub>o</sub> − q<sub>u</sub>.",
         "Ein <b>Boxplot</b> zeigt Minimum, q<sub>u</sub>, Median, q<sub>o</sub> und Maximum. In der Box liegen etwa die mittleren 50 % der Daten.",
         "Das <b>arithmetische Mittel</b> wird von Ausreißern stark beeinflusst, der Median kaum."],
        [example("3, 8, 5, 12, 9, 6, 10", ["sortiert: 3, 5, 6, 8, 9, 10, 12", "Median 8", "q<sub>u</sub> = 5, q<sub>o</sub> = 10"], "Quartilsabstand 5"),
         example("Mittelwert von 4, 7, 10", ["21 %s 3" % G], "7")],
        [["Median ohne Sortieren", "Immer zuerst ordnen"],
         ["Spannweite = Breite der Box", "Spannweite = Maximum − Minimum (ganze Länge)"],
         ["Mittelwert ist immer der beste Wert", "Bei Ausreißern ist der Median besser"]])
    faq = [
        {"q": "Was zeigt ein Boxplot?", "a": "Minimum, unteres Quartil, Median, oberes Quartil und Maximum. Die Box enthält die mittlere Hälfte der Daten."},
        {"q": "Wie bestimmt man die Quartile?", "a": "Daten ordnen, den Median bestimmen. Der Median der unteren Hälfte ist das untere Quartil, der der oberen Hälfte das obere Quartil."},
        {"q": "Wann ist der Median besser als der Mittelwert?", "a": "Wenn es Ausreißer gibt, also einzelne sehr große oder kleine Werte."},
        {"q": "Was ist der Quartilsabstand?", "a": "Oberes minus unteres Quartil. Er zeigt, wie stark die mittleren 50 % der Daten streuen."},
    ]
    make_unit(R, "boxplots-und-kennwerte", "D",
              "Die Schülerinnen und Schüler bestimmen Kennwerte (Minimum, Maximum, Spannweite, Median, Quartile, arithmetisches Mittel), erstellen und lesen Boxplots und vergleichen Datenreihen (Zusammenfassung).",
              "Kennwerte und Boxplots",
              "Boxplot, Median und Quartile Klasse 7 – Arbeitsblätter mit Lösungen",
              "Boxplots",
              "Daten auswerten für Klasse 7: Median, Quartile, Spannweite, Mittelwert, Ausreißer und Boxplots lesen und vergleichen. 100 Aufgaben mit Lösungen, kostenlos.",
              "Boxplot: Minimum, unteres Quartil, Median, oberes Quartil, Maximum.",
              "In der Box liegen die mittleren 50 % der Daten.",
              body, faq, sets, 16, grade="klasse-7")


if __name__ == "__main__":
    main()
