# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 6: Rechnen mit negativen Zahlen（Leitidee Zahl und Operation, Sek I）
  python3 tools/gen_de_mathe_k6_rechnen_mit_negativen_zahlen.py
Betrag und Gegenzahl, ganze Zahlen addieren und subtrahieren (Zahlengerade), Minus einer negativen Zahl, multiplizieren und dividieren (Vorzeichenregeln), Sachaufgaben (Temperatur, Konto, Höhen).
Fehler: −3 − 5 = 2 oder −2, 4 − (−6) = −2, (−3) · (−4) = −12, Betrag als Gegenzahl.
"""
import random
from de_common import num, lesson, example, make_unit, mix, Kids, MAL, table
from de_k6 import mcq as _mcq

R = random.Random(49612)
KIDS = Kids(R)
G = ":"


def mcq(q, a, c, e):
    return _mcq(q, a, c, e, neg=True)


def n(v):
    return num(v)


def k(v):
    """in Klammern, wenn negativ"""
    return "(%s)" % num(v) if v < 0 else num(v)


def betrag():
    v = R.choice([x for x in range(-60, 61) if x != 0])
    kind = R.choice(["betrag", "gegen", "abstand"])
    if kind == "betrag":
        return mcq("Was ist |%s|?" % n(v), n(abs(v)), [n(-abs(v)), n(abs(v) + 1), "0"], "Der Betrag ist der Abstand zur 0, immer ohne Minus: <b>%s</b>." % n(abs(v)))
    if kind == "gegen":
        return mcq("Was ist die Gegenzahl von %s?" % n(v), n(-v), [n(v), n(abs(v) + 1) if v > 0 else n(v - 1), "0"], "Die Gegenzahl liegt auf der anderen Seite der 0, gleich weit entfernt: <b>%s</b>." % n(-v))
    a, b = R.randint(-30, -1), R.randint(1, 30)
    return mcq("Wie weit liegen %s und %s auf der Zahlengeraden auseinander?" % (n(a), n(b)), str(b - a), [str(b + a) if b + a > 0 else str(abs(b + a) + 1), str(abs(a)), str(b - a + 1)],
               "Von %s bis 0 sind %d, von 0 bis %d sind %d: <b>%d</b>." % (n(a), -a, b, b, b - a))


def addsub():
    a, b = R.randint(-20, 20), R.randint(1, 20)
    op = R.choice(["+", "−"])
    if a == 0 or (a > 0 and op == "+") or (a > 0 and a >= b):
        return None
    v = a + b if op == "+" else a - b
    w = [n(-v), n(a - b) if op == "+" else n(a + b), n(abs(a) + b) if a < 0 else n(v + 1), n(v - 1)]
    return mcq("%s %s %d = ?" % (n(a), op, b), n(v), w,
               "Auf der Zahlengeraden bei %s starten und %d nach %s gehen: <b>%s</b>." % (n(a), b, "rechts" if op == "+" else "links", n(v)))


def klammer():
    a, b = R.randint(-15, 15), R.choice([x for x in range(-15, 16) if x])
    op = R.choice(["+", "−"])
    v = a + b if op == "+" else a - b
    if b > 0 and R.random() < 0.6:
        b = -b
        v = a + b if op == "+" else a - b
    regel = ("+ (−%d) heißt − %d" % (-b, -b)) if op == "+" and b < 0 else ("− (−%d) heißt + %d" % (-b, -b)) if b < 0 else ""
    w = [n(a - b) if op == "+" else n(a + b), n(-v), n(v + 2), n(v - 2)]
    return mcq("%s %s %s = ?" % (n(a), op, k(b)), n(v), w, "%s%s %s %s = <b>%s</b>." % (("Regel: " + regel + ". ") if regel else "", n(a), op, k(b), n(v)))


def malteil():
    a, b = R.choice([x for x in range(-12, 13) if x not in (0, 1, -1)]), R.choice([x for x in range(-12, 13) if x not in (0, 1, -1)])
    if a > 0 and b > 0:
        a = -a
    op = R.choice(["mal", "mal", "durch"])
    if op == "mal":
        v = a * b
        return mcq("%s %s %s = ?" % (k(a), MAL, k(b)), n(v), [n(-v), n(a + b), n(abs(a) + abs(b)) if a + b != abs(a) + abs(b) else n(v + 1)],
                   "%s %s %s ergibt %s. %d %s %d = %d: <b>%s</b>." % ("Minus" if a < 0 else "Plus", MAL, "Minus" if b < 0 else "Plus", "Plus" if v > 0 else "Minus", abs(a), MAL, abs(b), abs(v), n(v)))
    c = a * b
    return mcq("%s %s %s = ?" % (k(c), G, k(b)), n(a), [n(-a), n(c - b) if c - b != a else n(a + 1), n(abs(a) + 1)],
               "Gleiche Vorzeichen: Plus. Verschiedene Vorzeichen: Minus. %d %s %d = %d: <b>%s</b>." % (abs(c), G, abs(b), abs(a), n(a)))


def gemischt():
    a, b, c = R.randint(-9, 9), R.randint(-9, 9), R.randint(-9, 9)
    if 0 in (a, b, c):
        return None
    kind = R.choice(["punkt", "klammer", "drei"])
    if kind == "punkt":
        v = a + b * c
        return mcq("%s + %s %s %s = ?" % (n(a), k(b), MAL, k(c)), n(v), [n((a + b) * c), n(a - b * c), n(v + 1) if v + 1 != (a + b) * c else n(v - 1)],
                   "Punkt vor Strich: %s %s %s = %s. %s + %s = <b>%s</b>." % (k(b), MAL, k(c), n(b * c), n(a), k(b * c), n(v)))
    if kind == "klammer":
        v = (a - b) * c
        return mcq("(%s − %s) %s %s = ?" % (n(a), k(b), MAL, k(c)), n(v), [n(a - b * c), n((a + b) * c), n(-v)],
                   "Klammer zuerst: %s − %s = %s. %s %s %s = <b>%s</b>." % (n(a), k(b), n(a - b), k(a - b), MAL, k(c), n(v)))
    v = a - b - c
    return mcq("%s − %s − %s = ?" % (n(a), k(b), k(c)), n(v), [n(a - b + c), n(a + b + c), n(-v) if v else "1"],
               "Von links nach rechts: %s − %s = %s, %s − %s = <b>%s</b>." % (n(a), k(b), n(a - b), n(a - b), k(c), n(v)))


def sache():
    p, er = KIDS.next()
    kind = R.choice(["temp", "temp2", "konto", "hoehe", "aufzug", "tauch"])
    if kind == "temp":
        t = R.randint(-12, 8)
        d = R.randint(3, 15)
        v = t - d
        return mcq("Am Abend sind es %s °C. In der Nacht sinkt die Temperatur um %d °C. Wie kalt ist es dann?" % (n(t), d), "%s °C" % n(v), ["%s °C" % n(x) for x in (t + d, -(abs(t) - d) if t < 0 else d - t, v + 2)],
                   "%s − %d = <b>%s °C</b>." % (n(t), d, n(v)))
    if kind == "temp2":
        a, b = R.randint(-15, -1), R.randint(1, 20)
        return mcq("Morgens sind es %s °C, mittags %s °C. Um wie viel Grad ist es wärmer geworden?" % (n(a), n(b)), "%d °C" % (b - a), ["%d °C" % x for x in (b + a if b + a > 0 else b + a + 20, b, b - a + 1)],
                   "%s − (%s) = %d + %d = <b>%d °C</b>." % (n(b), n(a), b, -a, b - a))
    if kind == "konto":
        s = R.randint(20, 200)
        a = R.randint(s + 10, s + 250)
        e = R.randint(20, 150)
        v = s - a + e
        return mcq("Auf dem Konto von %s sind %d €. %s hebt %d € ab und zahlt danach %d € ein. Wie ist der Kontostand?" % (p, s, er.capitalize(), a, e), "%s €" % n(v), ["%s €" % n(x) for x in (s + a + e, s - a - e, -v)],
                   "%d − %d + %d = <b>%s €</b>." % (s, a, e, n(v)))
    if kind == "hoehe":
        b, t = R.randint(200, 2900), R.randint(-400, -20)
        return mcq("Ein Berg ist %d m hoch. Ein See liegt %d m unter dem Meeresspiegel (%s m). Wie groß ist der Höhenunterschied?" % (b, -t, n(t)), "%s m" % num(b - t), ["%s m" % num(x) for x in (b + t, b, b - t + 100)],
                   "%d − (%s) = %d + %d = <b>%s m</b>." % (b, n(t), b, -t, num(b - t)))
    if kind == "aufzug":
        s = R.randint(-3, 5)
        u = R.randint(2, 8)
        v = s - u
        if v < -4:
            return None
        lab = lambda x: "Stockwerk %s" % n(x) if x != 0 else "Erdgeschoss (0)"
        return mcq("Ein Aufzug ist im %s. Er fährt %d Stockwerke nach unten. Wo ist er dann?" % (lab(s).replace("Stockwerk", "Stockwerk") if s else "Erdgeschoss", u), lab(v), [lab(s + u), lab(v + 1), lab(-v) if v else lab(1)],
                   "%s − %d = <b>%s</b>." % (n(s), u, n(v)))
    d, z = R.randint(5, 30), R.randint(2, 5)
    v = -d * z
    return mcq("Ein Taucher sinkt jede Minute %d m tiefer. Wo ist er nach %d Minuten, wenn er an der Oberfläche (0 m) startet?" % (d, z), "bei %s m" % n(v), ["bei %s m" % n(x) for x in (-v, -d - z, v + d)],
               "%d %s (−%d) = <b>%s m</b>." % (z, MAL, d, n(v)))


def main():
    seen = set()
    sets = [
        ("Betrag und Gegenzahl", mix(R, seen, [(betrag, 12), (addsub, 8)])),
        ("Addieren und subtrahieren", mix(R, seen, [(addsub, 10), (klammer, 10)])),
        ("Multiplizieren und dividieren", mix(R, seen, [(malteil, 20)])),
        ("Gemischte Aufgaben", mix(R, seen, [(gemischt, 20)])),
        ("Sachaufgaben", mix(R, seen, [(sache, 20)])),
    ]
    body = lesson(
        ["Der <b>Betrag</b> |−5| = 5 ist der Abstand zur 0. Die <b>Gegenzahl</b> von 5 ist −5.",
         "Plus einer Zahl: auf der Zahlengeraden nach rechts. Minus: nach links.",
         "<b>Minus eine negative Zahl</b> ist plus: 4 − (−6) = 4 + 6 = 10. Plus eine negative Zahl ist minus: 4 + (−6) = −2.",
         "Beim <b>Multiplizieren und Dividieren</b>: gleiche Vorzeichen ergeben Plus, verschiedene Vorzeichen ergeben Minus."],
        [example("−3 − 5", ["Bei −3 starten, 5 nach links"], "−8"),
         example("(−4) %s (−6)" % MAL, ["Minus mal Minus = Plus", "4 %s 6 = 24" % MAL], "24")],
        [["−3 − 5 = 2", "Weiter nach links: −8"],
         ["4 − (−6) = −2", "Minus Minus wird Plus: 10"],
         ["(−3) %s (−4) = −12" % MAL, "Gleiche Vorzeichen: +12"]],
        extra=table(["Rechnung", "Vorzeichen"], [["Plus %s Plus" % MAL, "Plus"], ["Minus %s Minus" % MAL, "Plus"], ["Plus %s Minus" % MAL, "Minus"], ["Minus %s Plus" % MAL, "Minus"]]))
    faq = [
        {"q": "Warum ist Minus mal Minus Plus?", "a": "Multipliziert man mit −1, dreht sich die Richtung auf der Zahlengeraden um. Zweimal umdrehen ergibt wieder die ursprüngliche Richtung."},
        {"q": "Was ist 5 − (−3)?", "a": "Minus einer negativen Zahl ist Plus: 5 + 3 = 8."},
        {"q": "Was ist der Betrag einer Zahl?", "a": "Der Abstand zur 0 auf der Zahlengeraden. |−7| = 7 und |7| = 7."},
        {"q": "Wie dividiert man ganze Zahlen?", "a": "Erst die Beträge dividieren. Dann das Vorzeichen bestimmen: gleiche Vorzeichen Plus, verschiedene Minus."},
    ]
    make_unit(R, "rechnen-mit-negativen-zahlen", "Z",
              "Die Schülerinnen und Schüler bestimmen Betrag und Gegenzahl, addieren, subtrahieren, multiplizieren und dividieren ganze Zahlen und lösen Sachaufgaben (Zusammenfassung).",
              "Rechnen mit negativen Zahlen",
              "Rechnen mit negativen Zahlen Klasse 6 – Arbeitsblätter mit Lösungen",
              "Negative Zahlen rechnen",
              "Rechnen mit negativen Zahlen für Klasse 6: Betrag, Addition und Subtraktion, Vorzeichenregeln, gemischte Aufgaben und Sachaufgaben. 100 Aufgaben mit Lösungen, kostenlos.",
              "Minus mal Minus ergibt Plus.",
              "Minus einer negativen Zahl ist Plus.",
              body, faq, sets, 12, grade="klasse-6")


if __name__ == "__main__":
    main()
