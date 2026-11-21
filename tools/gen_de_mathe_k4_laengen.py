# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 4: Längen mit Komma – mm, cm, m, km（Leitidee Größen und Messen）
  python3 tools/gen_de_mathe_k4_laengen.py
Kommaschreibweise (1,25 m = 1 m 25 cm), in kleinere und größere Einheiten umwandeln, rechnen und vergleichen, Sachaufgaben.
Fehler: 3 m 7 cm → 3,7 m, 2,4 km → 2004 m, Einheiten beim Rechnen nicht angeglichen.
"""
import random
from de_common import mcq, num, lesson, example, make_unit, mix, Kids, MAL, table
from de_k4_groessen import lesen, kleiner, groesser, rechnen, komma, u, zwei

R = random.Random(49109)
KIDS = Kids(R)
PAARE = [(100, "m", "cm"), (1000, "km", "m"), (10, "cm", "mm")]


def any_of(fn):
    makers = [fn(R, *p) for p in PAARE]
    return lambda: R.choice(makers)()


def sache():
    p = KIDS.next()
    kind = R.choice(["wandern", "stoff", "sprung", "staffel", "brett"])
    if kind == "wandern":
        a, b = R.randint(1500, 6800), R.randint(1200, 5400)
        a, b = a // 50 * 50, b // 50 * 50
        r = a + b
        q = "Familie Schulz wandert am Vormittag %s und am Nachmittag %s. Wie weit wandert sie insgesamt?" % (komma(a, 1000, "km"), komma(b, 1000, "km"))
        w = [r + 1000, r - 100, a + b // 10]
        return mcq(q, komma(r, 1000, "km"), [komma(x, 1000, "km") for x in w if x != r], "%s + %s = %s = <b>%s</b>." % (u(a, "m"), u(b, "m"), u(r, "m"), komma(r, 1000, "km")))
    if kind == "stoff":
        tot = R.randint(3, 8) * 100
        piece = R.choice([25, 40, 50, 75])
        n = R.randint(2, tot // piece - 1)
        r = tot - n * piece
        q = "%s hat %s Stoff und schneidet %d Stücke zu je %s ab. Wie viel Stoff bleibt übrig?" % (p[0], u(tot // 100, "m"), n, u(piece, "cm"))
        w = [tot - piece, r + piece, tot // 100 * 10 - n * piece if tot // 100 * 10 > n * piece else r + 10]
        return mcq(q, komma(r, 100, "m"), [komma(x, 100, "m") for x in w if x > 0 and x != r],
                   "%d %s %d cm = %d cm. %d cm − %d cm = %d cm = <b>%s</b>." % (n, MAL, piece, n * piece, tot, n * piece, r, komma(r, 100, "m")))
    if kind == "sprung":
        a, b = R.randint(250, 420), R.randint(250, 420)
        if a == b:
            return None
        p2 = KIDS.next()
        q = "Beim Weitsprung springt %s %s, %s springt %s. Wie viel Zentimeter weiter springt %s?" % (p[0], komma(a, 100, "m"), p2[0], komma(b, 100, "m"), p[0] if a > b else p2[0])
        r = abs(a - b)
        return mcq(q, u(r, "cm"), [u(x, "cm") for x in (r + 10, a + b, r * 10) if x != r], "%d cm − %d cm = <b>%d cm</b>." % (max(a, b), min(a, b), r))
    if kind == "staffel":
        n = R.randint(4, 8)
        each = R.choice([250, 400, 750, 1250])
        r = n * each
        q = "Bei einer Staffel laufen %d Kinder je %s. Wie lang ist die Strecke in Kilometern?" % (n, u(each, "m"))
        return mcq(q, komma(r, 1000, "km"), [komma(x, 1000, "km") for x in (r * 10, r // 10 if r // 10 else r + 1000, r + each) if x != r],
                   "%d %s %d m = %s = <b>%s</b>." % (n, MAL, each, u(r, "m"), komma(r, 1000, "km")))
    total = R.randint(2, 4) * 100
    n = R.choice([4, 5, 8])
    if total % n:
        return None
    r = total // n
    q = "Ein Brett ist %s lang. Es wird in %d gleich lange Stücke gesägt. Wie lang ist jedes Stück?" % (u(total // 100, "m"), n)
    return mcq(q, u(r, "cm"), [u(x, "cm") for x in (r * 10, total // 100 * 10 // n if total // 100 * 10 // n else r + 5, r + 5) if x != r],
               "%s = %d cm. %d cm : %d = <b>%d cm</b>." % (u(total // 100, "m"), total, total, n, r))


def main():
    seen = set()
    sets = [
        ("Kommaschreibweise", mix(R, seen, [(any_of(lesen), 20)])),
        ("In die kleinere Einheit", mix(R, seen, [(any_of(kleiner), 20)])),
        ("In die größere Einheit", mix(R, seen, [(any_of(groesser), 20)])),
        ("Rechnen und vergleichen", mix(R, seen, [(any_of(rechnen), 20)])),
        ("Sachaufgaben mit Längen", mix(R, seen, [(sache, 20)])),
    ]
    body = lesson(
        ["1 cm = 10 mm, 1 m = 100 cm, 1 km = 1000 m.",
         "Bei der <b>Kommaschreibweise</b> stehen vor dem Komma die großen Einheiten, dahinter die kleinen: 1,25 m = 1 m 25 cm.",
         "Hinter dem Komma stehen so viele Stellen, wie der Umrechnungsfaktor Nullen hat: m → cm zwei Stellen, km → m drei Stellen, cm → mm eine Stelle.",
         "Zum Rechnen und Vergleichen bringst du alles in <b>dieselbe Einheit</b>."],
        [example("3 m 7 cm mit Komma", ["2 Stellen für cm: 07"], "3,07 m"),
         example("2,450 km in m", ["2 km = 2000 m", "2000 m + 450 m"], "2450 m")],
        [["3 m 7 cm = 3,7 m", "3,07 m (3,7 m wären 3 m 70 cm)"],
         ["2,4 km = 2004 m", "2,400 km = 2400 m"],
         ["1,5 m + 75 cm = 76,5", "Erst umrechnen: 150 cm + 75 cm = 225 cm = 2,25 m"]],
        extra=table(["Einheiten", "Umrechnung", "Stellen nach dem Komma"], [["cm und mm", "1 cm = 10 mm", "1"], ["m und cm", "1 m = 100 cm", "2"], ["km und m", "1 km = 1000 m", "3"]]))
    faq = [
        {"q": "Wann lernt man die Kommaschreibweise bei Längen?", "a": "Meist in Klasse 4. Kommazahlen werden dabei als andere Schreibweise für zwei Einheiten verstanden, nicht als Dezimalbrüche."},
        {"q": "Warum ist 3,7 m nicht 3 m 7 cm?", "a": "Hinter dem Komma stehen bei Metern immer zwei Stellen für die Zentimeter. 3,7 m = 3,70 m = 3 m 70 cm."},
        {"q": "Wie viele Stellen hat km hinter dem Komma?", "a": "Drei, weil 1 km = 1000 m ist: 2,450 km = 2 km 450 m."},
        {"q": "Wie übt man das am besten?", "a": "Mit einer Stellenwerttafel für Längen (km | m | dm | cm | mm) und mit echten Messungen im Alltag."},
    ]
    make_unit(R, "laengen-mit-komma", "G",
              "Die Schülerinnen und Schüler rechnen mit Längen in mm, cm, m und km, nutzen die Kommaschreibweise, wandeln um und lösen Sachaufgaben (Zusammenfassung).",
              "Längen mit Komma: mm, cm, m und km",
              "Längen umrechnen mit Komma Klasse 4 – Arbeitsblätter mit Lösungen",
              "Längen mit Komma",
              "Klasse 4: Längen in Kommaschreibweise, mm, cm, m und km umrechnen, rechnen, vergleichen und Sachaufgaben. 100 Übungsaufgaben mit Lösungen, kostenlos.",
              "1,25 m = 1 m 25 cm = 125 cm",
              "m → cm: 2 Stellen, km → m: 3 Stellen, cm → mm: 1 Stelle.",
              body, faq, sets, 9, grade="klasse-4")


if __name__ == "__main__":
    main()
