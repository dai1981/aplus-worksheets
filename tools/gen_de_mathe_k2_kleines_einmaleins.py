# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 2: Das kleine Einmaleins（Leitidee Zahl und Operation）
  python3 tools/gen_de_mathe_k2_kleines_einmaleins.py
Dreier- und Viererreihe, Sechser- und Achterreihe (verdoppeln), Siebener- und Neunerreihe, gemischt mit Platzhalter, Sachaufgaben.
Fehler: Nachbarergebnis der Reihe (7 · 8 = 54), plus statt mal, beim Ableiten um eine Reihe verrutscht.
"""
import random
from de_common import mcq, lesson, example, make_unit, mix, Kids, MAL, table
from de_k2 import punktfeld

R = random.Random(49209)
KIDS = Kids(R)


def wr(a, k):
    r = a * k
    return [str(r + k), str(r - k) if r > k else str(r + 2 * k), str(r + 1), str(a + k), str(r - 2)]


def reihen(ks, hilfe):
    def mk():
        k = R.choice(ks)
        a = R.randint(2, 10)
        kind = R.choice(["mal", "mal", "tausch", "luecke", "bild"])
        r = a * k
        if kind == "mal":
            return mcq("%d %s %d = ?" % (a, MAL, k), str(r), wr(a, k), hilfe(a, k))
        if kind == "tausch":
            return mcq("%d %s %d = ?" % (k, MAL, a), str(r), wr(a, k), hilfe(a, k))
        if kind == "bild":
            if a > 6 or k > 9:
                return None
            return mcq(punktfeld(a, k) + "Wie viele Punkte sind es?", str(r), wr(a, k), hilfe(a, k))
        return mcq("? %s %d = %d" % (MAL, k, r), str(a), [str(a + 1), str(a - 1), str(r - k)],
                   "In der %der-Reihe: <b>%d</b> %s %d = %d." % (k, a, MAL, k, r))
    return mk


def h34(a, k):
    if k == 4:
        return "Verdopple 2 %s %d: %d + %d = <b>%d</b>." % (MAL, a, 2 * a, 2 * a, 4 * a)
    return "%d %s 3 = %d %s 2 + %d = %d + %d = <b>%d</b>." % (a, MAL, a, MAL, a, 2 * a, a, 3 * a)


def h68(a, k):
    h = k // 2
    return "Verdopple %d %s %d: %d + %d = <b>%d</b>." % (a, MAL, h, a * h, a * h, a * k)


def h79(a, k):
    if k == 9:
        return "10 %s %d − %d = %d − %d = <b>%d</b>." % (MAL, a, a, 10 * a, a, 9 * a)
    return "5 %s %d + 2 %s %d = %d + %d = <b>%d</b>." % (MAL, a, MAL, a, 5 * a, 2 * a, 7 * a)


def gemischt():
    k, a = R.randint(2, 10), R.randint(2, 10)
    r = a * k
    kind = R.choice(["zwei", "vergleich", "luecke"])
    if kind == "zwei":
        cands = [(x, y) for x in range(2, 11) for y in range(x, 11) if x * y == r]
        if len(cands) < 2:
            return None
        x, y = R.choice([c for c in cands if c != (min(a, k), max(a, k))] or cands)
        return mcq("Welche Malaufgabe hat auch das Ergebnis %d? (%d %s %d = %d)" % (r, a, MAL, k, r), "%d %s %d" % (x, MAL, y),
                   ["%d %s %d" % (x + 1, MAL, y), "%d %s %d" % (x, MAL, y - 1), "%d + %d" % (x, y)],
                   "%d %s %d = <b>%d</b>." % (x, MAL, y, r))
    if kind == "vergleich":
        b, c = R.randint(2, 10), R.randint(2, 10)
        if b * c == r:
            return None
        big = "%d %s %d" % (a, MAL, k) if r > b * c else "%d %s %d" % (b, MAL, c)
        return mcq("Welche Aufgabe hat das größere Ergebnis: %d %s %d oder %d %s %d?" % (a, MAL, k, b, MAL, c), big,
                   ["%d %s %d" % (b, MAL, c) if big.startswith("%d %s %d" % (a, MAL, k)) else "%d %s %d" % (a, MAL, k), "Beide sind gleich", "Das kann man nicht sagen"],
                   "%d %s %d = %d und %d %s %d = %d: <b>%s</b>." % (a, MAL, k, r, b, MAL, c, b * c, big))
    return mcq("%d %s ? = %d" % (a, MAL, r), str(k), [str(k + 1), str(k - 1), str(r - a)],
               "%d %s <b>%d</b> = %d." % (a, MAL, k, r))


SACHE = [("Kinder sitzen an %d Tischen. An jedem Tisch sitzen %d Kinder. Wie viele Kinder sind es?", None),
         ("%s kauft %d Packungen Joghurt. In jeder Packung sind %d Becher. Wie viele Becher sind es?", "p"),
         ("Im Garten sind %d Beete. In jedem Beet wachsen %d Salatköpfe. Wie viele Salatköpfe sind es?", None),
         ("Eine Woche hat 7 Tage. Wie viele Tage haben %d Wochen?", "w"),
         ("Ein Kinoticket kostet %d €. %s kauft %d Tickets. Wie viel kostet das?", "k"),
         ("In einem Regal stehen %d Reihen mit je %d Büchern. Wie viele Bücher sind es?", None),
         ("Ein Insekt hat 6 Beine. Wie viele Beine haben %d Insekten?", "i"),
         ("Eine Spinne hat 8 Beine. Wie viele Beine haben %d Spinnen?", "s")]


def sache():
    t, kind = R.choice(SACHE)
    p = KIDS.next()
    a, k = R.randint(3, 9), R.randint(3, 9)
    if kind == "w":
        k = 7
        q = t % a
    elif kind == "i":
        k = 6
        q = t % a
    elif kind == "s":
        k = 8
        q = t % a
    elif kind == "p":
        q = t % (p[0], a, k)
    elif kind == "k":
        k = R.randint(4, 9)
        q = t % (k, p[0], a)
        r = a * k
        return mcq(q, "%d €" % r, ["%d €" % x for x in (a + k, r + k, r - k)], "%d %s %d € = <b>%d €</b>." % (a, MAL, k, r))
    else:
        q = t % (a, k)
    r = a * k
    return mcq(q, str(r), [str(a + k), str(r + k), str(r - k), str(r - a)], "%d %s %d = <b>%d</b>." % (a, MAL, k, r))


def main():
    seen = set()
    sets = [
        ("Dreier- und Viererreihe", mix(R, seen, [(reihen([3, 4], h34), 20)])),
        ("Sechser- und Achterreihe", mix(R, seen, [(reihen([6, 8], h68), 20)])),
        ("Siebener- und Neunerreihe", mix(R, seen, [(reihen([7, 9], h79), 20)])),
        ("Alle Reihen gemischt", mix(R, seen, [(gemischt, 20)])),
        ("Sachaufgaben", mix(R, seen, [(sache, 20)])),
    ]
    body = lesson(
        ["Das <b>kleine Einmaleins</b> sind alle Malaufgaben von 1 %s 1 bis 10 %s 10." % (MAL, MAL),
         "Die Viererreihe ist das Doppelte der Zweierreihe. Die Achterreihe ist das Doppelte der Viererreihe.",
         "Die Sechserreihe ist das Doppelte der Dreierreihe.",
         "Die Neunerreihe: 10-mal minus 1-mal. 9 %s 7 = 70 − 7 = 63." % MAL],
        [example("8 %s 6" % MAL, ["4 %s 6 = 24" % MAL, "24 + 24 = 48"], "48"),
         example("7 %s 8" % MAL, ["5 %s 8 = 40" % MAL, "2 %s 8 = 16" % MAL, "40 + 16"], "56")],
        [["7 %s 8 = 54" % MAL, "7 %s 8 = 56 (54 ist 6 %s 9)" % (MAL, MAL)],
         ["9 %s 6 = 60 − 9" % MAL, "9 %s 6 = 60 − 6 = 54" % MAL],
         ["6 %s 7 = 13" % MAL, "6-mal die 7 = 42"]],
        extra=table(["Reihe", "Hilfe"], [["4er", "2er verdoppeln"], ["8er", "4er verdoppeln"], ["6er", "3er verdoppeln"], ["9er", "10er minus einmal"]]))
    faq = [
        {"q": "Muss mein Kind das ganze Einmaleins am Ende von Klasse 2 können?", "a": "In den meisten Bundesländern sollen die Kinder am Ende von Klasse 2 das kleine Einmaleins sicher beherrschen. In Klasse 3 wird es weiter gefestigt."},
        {"q": "Welche Aufgaben sind am schwersten?", "a": "Meist 6 · 7, 6 · 8, 7 · 8, 7 · 9 und 8 · 9. Sie lassen sich gut aus Kernaufgaben ableiten."},
        {"q": "Was hilft beim Auswendiglernen?", "a": "Kurze tägliche Übungen, Reihen laut aufsagen, Tauschaufgaben nutzen und schwierige Aufgaben auf Karteikarten üben."},
        {"q": "Wie hängen Mal und Geteilt zusammen?", "a": "Zu jeder Malaufgabe gehört eine Geteiltaufgabe: 7 · 8 = 56, also 56 : 8 = 7."},
    ]
    make_unit(R, "kleines-einmaleins", "Z",
              "Die Schülerinnen und Schüler beherrschen das kleine Einmaleins, leiten schwierige Aufgaben aus Kernaufgaben ab (Verdoppeln, Nachbaraufgaben) und lösen Sachaufgaben zur Multiplikation (Zusammenfassung).",
              "Das kleine Einmaleins",
              "Kleines Einmaleins Klasse 2 – Arbeitsblätter mit Lösungen",
              "Kleines Einmaleins",
              "Das kleine Einmaleins für Klasse 2: Dreier-, Vierer-, Sechser-, Achter-, Siebener- und Neunerreihe, gemischte Aufgaben und Sachaufgaben. 100 Übungsaufgaben mit Lösungen, kostenlos.",
              "Schwierige Aufgaben aus leichten ableiten.",
              "8 · 6 = 4 · 6 + 4 · 6 = 48",
              body, faq, sets, 9, grade="klasse-2")


if __name__ == "__main__":
    main()
