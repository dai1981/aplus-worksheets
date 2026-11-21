# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 1: Längen vergleichen und messen（Leitidee Größen und Messen）
  python3 tools/gen_de_mathe_k1_laengen_vergleichen_und_messen.py
Länger und kürzer, höher und niedriger, mit Würfeln messen, mit dem Lineal in cm messen, schätzen und Sachaufgaben.
Fehler: Anfänge nicht auf einer Linie verglichen, beim Lineal bei 1 statt bei 0 angefangen, Würfel doppelt gezählt.
"""
import random
from de_common import mcq, lesson, example, make_unit, mix, Kids
from de_k2 import de
from k_pics import pencils_svg, towers_svg
from gen_de_mathe_k3_laengen import lineal

R = random.Random(49412)
KIDS = Kids(R)
FARBE = ["rot", "blau", "gelb", "grün"]


def stifte():
    n = R.choice([2, 3, 3, 4])
    ls = R.sample(range(2, 9), n)
    kind = R.choice(["lang", "kurz"])
    pic = de(pencils_svg(ls), "%d Stifte A bis %s" % (n, "ABCD"[n - 1]))
    k = ls.index(max(ls)) if kind == "lang" else ls.index(min(ls))
    letters = "ABCD"[:n]
    others = [c for c in letters if c != letters[k]] + ["Alle sind gleich lang", "Das kann man nicht sehen"]
    return mcq(pic + "Welcher Stift ist am %s?" % ("längsten" if kind == "lang" else "kürzesten"), letters[k], others[:3],
               "Die Stifte beginnen alle an derselben Linie. Am %s ist Stift <b>%s</b>." % ("längsten" if kind == "lang" else "kürzesten", letters[k]))


def tuerme():
    n = R.choice([2, 3, 4])
    hs = R.sample(range(2, 9), n)
    kind = R.choice(["hoch", "niedrig", "diff", "zahl"])
    pic = de(towers_svg(hs), "%d Würfeltürme" % n)
    letters = "ABCD"[:n]
    if kind == "zahl":
        k = R.randrange(n)
        return mcq(pic + "Wie viele Würfel hat Turm %s?" % letters[k], str(hs[k]), [str(hs[k] + 1), str(hs[k] - 1), str(hs[k] + 2)],
                   "Zähle die Würfel von unten nach oben: <b>%d</b>." % hs[k])
    if kind == "diff":
        i, j = sorted(R.sample(range(n), 2), key=lambda x: -hs[x])
        d = hs[i] - hs[j]
        return mcq(pic + "Um wie viele Würfel ist Turm %s höher als Turm %s?" % (letters[i], letters[j]), str(d), [str(hs[i]), str(d + 1), str(hs[i] + hs[j]) if hs[i] + hs[j] <= 20 else str(d + 2)],
                   "%d − %d = <b>%d</b>." % (hs[i], hs[j], d))
    k = hs.index(max(hs)) if kind == "hoch" else hs.index(min(hs))
    others = [c for c in letters if c != letters[k]] + ["Alle sind gleich hoch", "Das kann man nicht sehen"]
    return mcq(pic + "Welcher Turm ist am %s?" % ("höchsten" if kind == "hoch" else "niedrigsten"), letters[k], others[:3],
               "Turm %s hat %s Würfel: <b>%s</b>." % (letters[k], "die meisten" if kind == "hoch" else "die wenigsten", letters[k]))


def wuerfel_messen():
    kind = R.choice(["zaehlen", "zaehlen", "diff"])
    if kind == "zaehlen":
        n = R.randint(2, 9)
        cols = ["#e74c3c", "#3498db", "#f4d03f", "#27ae60"]
        s = []
        u = 30
        s.append("<rect x='10' y='10' width='%d' height='18' rx='4' fill='#c9a46b' stroke='#7a5a2a' stroke-width='1.5'/>" % (n * u))
        for i in range(n):
            s.append("<rect x='%d' y='34' width='%d' height='%d' fill='%s' stroke='#2b2b2b' stroke-width='1.5'/>" % (10 + i * u, u, u, cols[i % 4]))
        from ws_common import svg_wrap, fig
        pic = fig(svg_wrap(n * u + 20, 74, "".join(s), "ein Stab und Würfel darunter"))
        return mcq(pic + "Wie viele Würfel lang ist der Stab?", str(n), [str(n + 1), str(n - 1) if n > 2 else str(n + 2), str(2 * n)],
                   "Die Würfel liegen ohne Lücke unter dem Stab. Zähle sie: <b>%d</b>." % n)
    ls = R.sample(range(2, 10), 2)
    pic = de(pencils_svg(ls, unit=30), "zwei Stifte A und B")
    return mcq(pic + "Stift A ist %d Würfel lang. Stift B ist %d Würfel lang. Um wie viele Würfel ist der längere Stift länger?" % (ls[0], ls[1]),
               str(abs(ls[0] - ls[1])), [str(max(ls)), str(ls[0] + ls[1]), str(abs(ls[0] - ls[1]) + 1)],
               "%d − %d = <b>%d</b> Würfel." % (max(ls), min(ls), abs(ls[0] - ls[1])))


def lineal_messen():
    start = R.choice([0, 0, 0, 10, 20])
    L = R.randint(2, 10 - start // 10) * 10
    pic = lineal(start, L, cm=12)
    c = L // 10
    w = [c + 1, c - 1, c + start // 10] if start else [c + 1, c - 1, c + 2]
    return mcq(pic + "Wie lang ist der Streifen?", "%d cm" % c, ["%d cm" % x for x in w if x > 0 and x != c] + ["%d cm" % (c + 3)],
               ("Der Streifen beginnt bei 0 und endet bei %d: <b>%d cm</b>." % (c, c)) if not start else
               "Der Streifen beginnt bei %d und endet bei %d: %d − %d = <b>%d cm</b>." % (start // 10, start // 10 + c, start // 10 + c, start // 10, c))


SCHATZ = [("Wie lang ist ein Bleistift ungefähr?", "17 cm", ["17 m", "2 cm", "70 cm"]),
          ("Wie lang ist ein Radiergummi ungefähr?", "5 cm", ["5 m", "50 cm", "1 cm"]),
          ("Wie breit ist ein Finger ungefähr?", "1 cm", ["1 m", "10 cm", "20 cm"]),
          ("Wie hoch ist eine Tür ungefähr?", "2 m", ["2 cm", "20 cm", "20 m"]),
          ("Wie lang ist ein Schuh eines Kindes ungefähr?", "20 cm", ["2 cm", "20 m", "2 m"]),
          ("Wie lang ist ein Löffel ungefähr?", "15 cm", ["15 m", "1 cm", "1 m"]),
          ("Was ist länger?", "ein Bus", ["ein Auto", "ein Fahrrad", "ein Bleistift"]),
          ("Was ist am kürzesten?", "eine Ameise", ["eine Maus", "ein Hund", "ein Pferd"]),
          ("Was ist am höchsten?", "ein Haus", ["ein Kind", "ein Tisch", "ein Stuhl"])]


def sache():
    kind = R.choice(["schaetz", "schaetz", "band", "sprung", "zusammen"])
    p = KIDS.next()
    if kind == "schaetz":
        q, a, w = R.choice(SCHATZ)
        return mcq(q, a, w, "Stell dir den Gegenstand vor: <b>%s</b>." % a)
    if kind == "band":
        a, b = R.randint(8, 20), R.randint(2, 7)
        return mcq("%s hat ein Band, das %d cm lang ist. %s schneidet %d cm ab. Wie lang ist das Band jetzt?" % (p[0], a, p[1].capitalize(), b), "%d cm" % (a - b),
                   ["%d cm" % x for x in (a + b, a - b + 1, b)], "%d cm − %d cm = <b>%d cm</b>." % (a, b, a - b))
    if kind == "sprung":
        (n1, _), (n2, _) = KIDS.two()
        a, b = R.sample(range(5, 15), 2)
        win = n1 if a > b else n2
        return mcq("%s springt %d Fußlängen weit. %s springt %d Fußlängen weit. Wer springt weiter?" % (n1, a, n2, b), win, [n2 if win == n1 else n1, "Beide gleich weit", "Das kann man nicht sagen"],
                   "%d Fußlängen sind mehr als %d: <b>%s</b>." % (max(a, b), min(a, b), win))
    a, b = R.randint(3, 10), R.randint(2, 8)
    if a + b > 20:
        return None
    return mcq("Ein Zug hat einen Wagen, der %d cm lang ist, und einen Wagen, der %d cm lang ist. Wie lang ist der Zug zusammen?" % (a, b), "%d cm" % (a + b),
               ["%d cm" % x for x in (abs(a - b) if a != b else a + b + 2, a + b + 1, a + b - 1)], "%d cm + %d cm = <b>%d cm</b>." % (a, b, a + b))


def main():
    seen = set()
    sets = [
        ("Länger oder kürzer?", mix(R, seen, [(stifte, 20)])),
        ("Höher oder niedriger?", mix(R, seen, [(tuerme, 20)])),
        ("Mit Würfeln messen", mix(R, seen, [(wuerfel_messen, 20)])),
        ("Mit dem Lineal messen", mix(R, seen, [(lineal_messen, 20)])),
        ("Schätzen und Sachaufgaben", mix(R, seen, [(sache, 20)])),
    ]
    body = lesson(
        ["Zum Vergleichen legst du die Dinge an <b>einer Linie</b> nebeneinander.",
         "Du kannst mit Würfeln, Büroklammern oder Füßen messen. Alle Messteile müssen gleich groß sein.",
         "Mit dem Lineal misst du in <b>Zentimetern</b> (cm). Fange immer bei der <b>0</b> an.",
         "Ein Zentimeter ist ungefähr so breit wie ein Finger."],
        [example("Stift A ist 7 Würfel lang, Stift B 4 Würfel", ["7 − 4"], "A ist 3 Würfel länger"),
         example("Der Streifen geht am Lineal von 0 bis 6", ["Ende bei 6"], "6 cm")],
        [["Anfänge nicht auf einer Linie", "Alles an derselben Linie anlegen"],
         ["Am Lineal bei 1 anfangen", "Immer bei 0 anfangen"],
         ["Würfel mit Lücken anlegen", "Würfel ohne Lücke aneinanderlegen"]])
    faq = [
        {"q": "Warum messen Kinder zuerst mit Würfeln oder Füßen?", "a": "So verstehen sie, was Messen bedeutet: Man zählt, wie oft eine Einheit hineinpasst. Danach lernen sie das Lineal und den Zentimeter."},
        {"q": "Warum muss man beim Lineal bei 0 anfangen?", "a": "Die 0 ist der Anfang. Fängt man bei 1 an, ist das Ergebnis um 1 cm zu groß."},
        {"q": "Welche Einheiten lernt man in Klasse 1?", "a": "Den Zentimeter und oft schon den Meter. Millimeter kommen erst später."},
        {"q": "Wie übt man Schätzen?", "a": "Erst schätzen, dann messen und vergleichen. So bekommt man ein Gefühl für Längen."},
    ]
    make_unit(R, "laengen-vergleichen-und-messen", "G",
              "Die Schülerinnen und Schüler vergleichen Längen direkt und indirekt, messen mit nicht genormten Einheiten und mit dem Lineal in Zentimetern und schätzen Längen aus ihrer Umwelt (Zusammenfassung).",
              "Längen vergleichen und messen",
              "Längen messen Klasse 1 – Arbeitsblätter mit Lösungen",
              "Längen messen",
              "Längen für Klasse 1: länger und kürzer, höher und niedriger, mit Würfeln und mit dem Lineal messen, schätzen und Sachaufgaben. 100 Übungsaufgaben mit Bildern und Lösungen, kostenlos.",
              "An einer Linie anlegen, dann vergleichen.",
              "Am Lineal bei 0 anfangen.",
              body, faq, sets, 12, grade="klasse-1")


if __name__ == "__main__":
    main()
