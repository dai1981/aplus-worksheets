# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 5: Häufigkeiten und Diagramme（Leitidee Daten und Zufall, Sek I）
  python3 tools/gen_de_mathe_k5_haeufigkeiten_und_diagramme.py
Strichlisten und Häufigkeitstabellen, Säulen- und Liniendiagramme lesen, Kennwerte (Minimum, Maximum, Spannweite, Mittelwert, Median), Umfragen und Anteile.
Diagramm-Aufgaben (ablesen, vergleichen, linien) aus gen_de_mathe_k4_daten_und_diagramme.py mit neuem Zufall und Klassen 5a–5d.
Fehler: Spannweite als Summe, beim Mittelwert durch die falsche Anzahl geteilt, Median ohne Sortieren.
"""
import random
import gen_de_mathe_k4_daten_und_diagramme as k4
from de_common import mcq, num, fr, lesson, example, make_unit, mix, Kids, MAL, table, strichliste as sl

R = random.Random(49518)
k4.R = random.Random(49568)
k4.TOPICS = [(t, [c.replace("3", "5").replace("4", "6") if c[0] in "34" else c for c in cs], u, rg) for t, cs, u, rg in k4.TOPICS]
KIDS = Kids(R)
DATEN = [("Lieblingsfarbe", ["rot", "blau", "grün", "gelb"]), ("Haustier", ["Hund", "Katze", "Hase", "kein Tier"]), ("Schulweg", ["Fuß", "Rad", "Bus", "Auto"]),
         ("Lieblingssport", ["Fußball", "Schwimmen", "Turnen", "Tanzen"]), ("Lieblingsobst", ["Apfel", "Banane", "Erdbeere", "Kiwi"]), ("Augenzahl beim Würfeln", ["1", "2", "3", "4", "5", "6"])]


def strichliste():
    th, cats = R.choice(DATEN)
    vals = [R.randint(2, 17) for _ in cats]
    i = R.randrange(len(cats))
    kind = R.choice(["lesen", "summe", "diff"])
    tab = table([th, "Strichliste"], [[c, sl(v)] for c, v in zip(cats, vals)])
    if kind == "lesen":
        v = vals[i]
        return mcq(tab + "Wie oft wurde „%s“ genannt?" % cats[i], str(v), [str(v + 1), str(v - 1), str(v // 5 + v % 5)], "Ein Bündel (4 Striche und 1 Querstrich) sind 5 Striche. %d %s 5 + %d = <b>%d</b>." % (v // 5, MAL, v % 5, v))
    if kind == "summe":
        t = sum(vals)
        return mcq(tab + "Wie viele Antworten gab es insgesamt?", str(t), [str(t - vals[0]), str(t + 5), str(len(cats))], "%s = <b>%d</b>." % (" + ".join(map(str, vals)), t))
    j = vals.index(max(vals))
    k = vals.index(min(vals))
    if j == k or vals.count(max(vals)) > 1 or vals.count(min(vals)) > 1:
        return None
    d = vals[j] - vals[k]
    return mcq(tab + "Wie viele Nennungen mehr hat die häufigste Antwort als die seltenste?", str(d), [str(vals[j] + vals[k]), str(d + 1), str(vals[j])], "%d − %d = <b>%d</b>." % (vals[j], vals[k], d))


def liste():
    th, cats = R.choice(DATEN[:5])
    n = R.randint(8, 12)
    data = [R.choice(cats) for _ in range(n)]
    c = R.choice(cats)
    h = data.count(c)
    return mcq("Ergebnisse einer Umfrage zum Thema %s: %s. Wie oft kommt „%s“ vor?" % (th, ", ".join(data), c), str(h), [str(h + 1), str(h - 1) if h > 0 else "2", str(n - h)],
               "Zähle alle „%s“: <b>%d</b>-mal." % (c, h) if h != 1 else "„%s“ kommt <b>1</b>-mal vor." % c)


def kennwert():
    n = R.choice([5, 5, 6, 7, 7])
    kind = R.choice(["max", "spann", "mittel", "mittel", "median", "median"])
    while True:
        data = [R.randint(2, 30) for _ in range(n)]
        if len(set(data)) == n:
            break
    ctx = R.choice(["Punkte in einem Test", "Tore pro Spiel", "gelesene Seiten pro Tag", "Liegestütze", "Minuten Schulweg"])
    lst = ", ".join(map(str, data))
    if kind == "max":
        return mcq("%s: %s. Wie groß ist das Maximum?" % (ctx, lst), str(max(data)), [str(data[-1]), str(min(data)), str(max(data) - min(data))], "Der größte Wert ist <b>%d</b>." % max(data))
    if kind == "spann":
        sp = max(data) - min(data)
        return mcq("%s: %s. Wie groß ist die Spannweite?" % (ctx, lst), str(sp), [str(max(data) + min(data)), str(max(data)), str(sp + 1)], "Spannweite = Maximum − Minimum = %d − %d = <b>%d</b>." % (max(data), min(data), sp))
    if kind == "mittel":
        s = sum(data)
        r = s % n
        data[-1] -= r
        if data[-1] < 1 or len(set(data)) < n:
            return None
        s = sum(data)
        m = s // n
        lst = ", ".join(map(str, data))
        return mcq("%s: %s. Berechne den Mittelwert (Durchschnitt)." % (ctx, lst), str(m), [str(s), str(s // (n - 1)) if s % (n - 1) == 0 else str(m + 1), str(sorted(data)[n // 2]) if sorted(data)[n // 2] != m else str(m - 1)],
                   "Summe: %d. Anzahl: %d. %d : %d = <b>%d</b>." % (s, n, s, n, m))
    if n % 2 == 0:
        return None
    srt = sorted(data)
    med = srt[n // 2]
    return mcq("%s: %s. Bestimme den Median (Zentralwert)." % (ctx, lst), str(med), [str(data[n // 2]) if data[n // 2] != med else str(srt[n // 2 + 1]), str(srt[n // 2 - 1]), str(sum(data) // n) if sum(data) // n != med else str(srt[0])],
               "Sortiert: %s. Der mittlere Wert ist <b>%d</b>." % (", ".join(map(str, srt)), med))


def anteil():
    kind = R.choice(["bruch", "wie_viele", "mittel_sache", "mittel_sache", "fehlend"])
    if kind == "bruch":
        t = R.choice([20, 24, 25, 28, 30])
        d = R.choice([x for x in (2, 4, 5, 10) if t % x == 0])
        h = t // d
        th = R.choice(["kommen mit dem Rad", "haben einen Hund", "spielen Fußball im Verein", "lesen gern Comics"])
        return mcq("In einer Klasse mit %d Kindern %s %d Kinder. Welcher Anteil ist das?" % (t, th, h), fr(1, d), [fr(h, 100) if h < 100 else fr(1, h), fr(1, h), fr(d, t)],
                   "%d von %d: %d : %d = <b>%s</b> der Klasse." % (h, t, h, h, fr(1, d)))
    if kind == "wie_viele":
        t = R.choice([20, 24, 28, 30, 32])
        d = R.choice([x for x in (2, 4) if t % x == 0])
        return mcq("Bei einer Umfrage in einer Klasse mit %d Kindern sagt %s „Pizza“. Wie viele Kinder sind das?" % (t, "die Hälfte" if d == 2 else "ein Viertel"), str(t // d), [str(t - t // d), str(t // d + 2), str(d)],
                   "%d : %d = <b>%d</b>." % (t, d, t // d))
    if kind == "fehlend":
        n = R.choice([3, 4, 5])
        m = R.randint(8, 20)
        known = [R.randint(m - 5, m + 5) for _ in range(n - 1)]
        x = n * m - sum(known)
        if x <= 0:
            return None
        return mcq("Bei %d Würfen erzielt %s im Mittel %d Punkte. Die ersten Würfe brachten %s Punkte. Wie viele Punkte brachte der letzte Wurf?" % (n, KIDS.next()[0], m, ", ".join(map(str, known))), str(x),
                   [str(m), str(x + 1), str(n * m)], "Summe: %d %s %d = %d. %d − %d = <b>%d</b>." % (n, MAL, m, n * m, n * m, sum(known), x))
    p, er = KIDS.next()
    n = R.choice([4, 5])
    verb, unit, lo, hi = R.choice([("gelesen", "Minuten", 15, 40), ("Rad gefahren", "Minuten", 20, 45), ("gelaufen", "Kilometer", 8, 15), ("Klavier geübt", "Minuten", 12, 30)])
    m = R.randint(lo, hi)
    vals = [m + d for d in R.sample([-6, -4, -3, -2, 2, 3, 4, 6, 0, -1, 1], n - 1)]
    vals.append(n * m - sum(vals))
    if vals[-1] <= 0 or len(set(vals)) < n:
        return None
    if unit == "Kilometer" and min(vals) < 4:
        return None
    return mcq("%s hat an %d Tagen so viele %s %s: %s. Wie viele %s sind das durchschnittlich pro Tag?" % (p, n, unit, verb, ", ".join(map(str, vals)), unit), str(m), [str(n * m), str(m + 1), str(max(vals) - min(vals))],
               "%s = %d. %d : %d = <b>%d</b>." % (" + ".join(map(str, vals)), n * m, n * m, n, m))


def main():
    seen = set()
    sets = [
        ("Strichlisten und Häufigkeiten", mix(R, seen, [(strichliste, 12), (liste, 8)])),
        ("Säulendiagramme", mix(R, seen, [(k4.ablesen(True), 10), (k4.vergleichen, 10)])),
        ("Liniendiagramme und Tabellen", mix(R, seen, [(k4.linien, 12), (k4.tabelle, 8)])),
        ("Kennwerte: Spannweite, Mittelwert, Median", mix(R, seen, [(kennwert, 20)])),
        ("Umfragen und Durchschnitt", mix(R, seen, [(anteil, 20)])),
    ]
    body = lesson(
        ["Daten sammelt man mit einer <b>Strichliste</b>. Die Anzahl heißt <b>absolute Häufigkeit</b>.",
         "Säulendiagramme vergleichen Anzahlen. Liniendiagramme zeigen, wie sich etwas mit der Zeit ändert. Achte immer auf die <b>Skala</b>.",
         "<b>Spannweite</b> = größter Wert − kleinster Wert.",
         "<b>Mittelwert</b> (Durchschnitt) = Summe aller Werte : Anzahl der Werte.",
         "<b>Median</b> (Zentralwert): Werte der Größe nach ordnen, der mittlere Wert ist der Median."],
        [example("Werte: 4, 9, 2, 7, 8", ["Summe: 30", "30 : 5"], "Mittelwert 6"),
         example("Median von 4, 9, 2, 7, 8", ["Sortiert: 2, 4, 7, 8, 9", "Der mittlere Wert"], "Median 7")],
        [["Spannweite = 9 + 2 = 11", "Spannweite = 9 − 2 = 7"],
         ["Median von 4, 9, 2, 7, 8 ist 2 (Mitte der Liste)", "Erst sortieren: der Median ist 7"],
         ["Mittelwert: durch eine falsche Anzahl geteilt", "Zähle die Werte: Bei 5 Werten durch 5 teilen"]])
    faq = [
        {"q": "Wie berechnet man den Mittelwert?", "a": "Man addiert alle Werte und teilt durch die Anzahl der Werte."},
        {"q": "Was ist der Unterschied zwischen Mittelwert und Median?", "a": "Der Mittelwert ist der Durchschnitt. Der Median ist der Wert in der Mitte der sortierten Liste. Ein Ausreißer ändert den Mittelwert stark, den Median kaum."},
        {"q": "Was ist die Spannweite?", "a": "Der Unterschied zwischen dem größten und dem kleinsten Wert."},
        {"q": "Wann nimmt man ein Säulendiagramm und wann ein Liniendiagramm?", "a": "Säulen vergleichen Anzahlen (z. B. Lieblingsfarben). Linien zeigen eine Entwicklung über die Zeit (z. B. Temperatur)."},
    ]
    make_unit(R, "haeufigkeiten-und-diagramme", "D",
              "Die Schülerinnen und Schüler erfassen Daten in Strichlisten und Tabellen, stellen sie in Diagrammen dar, lesen Diagramme und bestimmen Kennwerte wie Spannweite, Mittelwert und Median (Zusammenfassung).",
              "Häufigkeiten, Diagramme und Mittelwert",
              "Häufigkeiten und Diagramme Klasse 5 – Mittelwert, Median, Arbeitsblätter",
              "Häufigkeiten & Diagramme",
              "Daten für Klasse 5: Strichlisten, Säulen- und Liniendiagramme, Spannweite, Mittelwert und Median, Umfragen. 100 Aufgaben mit Lösungen, kostenlos.",
              "Mittelwert = Summe : Anzahl.",
              "Median: erst sortieren, dann den mittleren Wert nehmen.",
              body, faq, sets, 18, grade="klasse-5")


if __name__ == "__main__":
    main()
