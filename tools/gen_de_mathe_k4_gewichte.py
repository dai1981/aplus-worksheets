# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 4: Gewichte – g, kg und t mit Komma（Leitidee Größen und Messen）
  python3 tools/gen_de_mathe_k4_gewichte.py
Kommaschreibweise (1,250 kg = 1 kg 250 g), umwandeln in g, kg und t, rechnen und vergleichen, Sachaufgaben.
Fehler: 2 kg 50 g → 2,5 kg, 1 t = 100 kg, Einheiten beim Rechnen nicht angeglichen.
"""
import random
from de_common import mcq, num, lesson, example, make_unit, mix, Kids, MAL, GETEILT, table
from de_k4_groessen import lesen, kleiner, groesser, rechnen, komma, u

R = random.Random(49110)
KIDS = Kids(R)
PAARE = [(1000, "kg", "g"), (1000, "t", "kg")]


def any_of(fn):
    makers = [fn(R, *p) for p in PAARE]
    return lambda: R.choice(makers)()


def sache():
    p = KIDS.next()
    kind = R.choice(["lkw", "einkauf", "brot", "aufzug", "paket"])
    if kind == "lkw":
        cap = R.choice([7500, 12000, 18000])
        n, per = R.randint(10, 40), R.choice([250, 300, 400, 500])
        load = n * per
        if load >= cap:
            return None
        q = "Ein Lastwagen darf %s laden. Er hat schon %d Kisten zu je %s geladen. Wie viel darf er noch laden?" % (komma(cap, 1000, "t"), n, u(per, "kg"))
        r = cap - load
        return mcq(q, komma(r, 1000, "t"), [komma(x, 1000, "t") for x in (load, r + per, cap - n - per) if x > 0 and x != r],
                   "%d %s %d kg = %s kg. %s kg − %s kg = %s kg = <b>%s</b>." % (n, MAL, per, num(load), num(cap), num(load), num(r), komma(r, 1000, "t")))
    if kind == "einkauf":
        items = [(R.choice([500, 750, 1000, 1500, 2500]), "Kartoffeln"), (R.choice([250, 400, 500]), "Käse"), (R.choice([1000, 2000]), "Mehl")]
        tot = sum(x for x, _ in items)
        q = "%s kauft %s, %s und %s. Wie schwer ist der Einkauf?" % (p[0], *["%s %s" % (komma(x, 1000, "kg") if x >= 1000 else u(x, "g"), n) for x, n in items])
        return mcq(q, komma(tot, 1000, "kg"), [komma(x, 1000, "kg") for x in (tot + 1000, tot - 250, sum(x // 10 if x >= 1000 else x for x, _ in items)) if x > 0 and x != tot],
                   "Alles in Gramm: %s = %s g = <b>%s</b>." % (" + ".join(num(x) for x, _ in items), num(tot), komma(tot, 1000, "kg")))
    if kind == "brot":
        n, per = R.randint(20, 80), R.choice([500, 750, 1000])
        tot = n * per
        q = "Eine Bäckerei backt %d Brote zu je %s. Wie viele Kilogramm Brot sind das?" % (n, u(per, "g") if per < 1000 else u(1, "kg"))
        return mcq(q, komma(tot, 1000, "kg"), [komma(x, 1000, "kg") for x in (tot * 10, tot // 10, tot + per) if x != tot],
                   "%d %s %d g = %s g = <b>%s</b>." % (n, MAL, per, num(tot), komma(tot, 1000, "kg")))
    if kind == "aufzug":
        cap = R.choice([630, 800, 1000])
        kids = R.randint(30, 45)
        n = cap // kids
        q = "Ein Aufzug darf höchstens %s tragen. Ein Kind wiegt etwa %s. Wie viele Kinder dürfen höchstens mitfahren?" % (u(cap, "kg"), u(kids, "kg"))
        return mcq(q, "%d Kinder" % n, ["%d Kinder" % x for x in (n + 1, n - 1, cap // 100) if x != n and x > 0],
                   "%d kg %s %d kg = %d Rest %d. Es dürfen nur <b>%d Kinder</b> mitfahren." % (cap, GETEILT, kids, n, cap % kids, n))
    n = R.randint(3, 8)
    per = R.choice([1250, 2500, 750, 1500])
    tot = n * per
    q = "Die Post bringt %d Pakete zu je %s. Wie schwer sind alle Pakete zusammen?" % (n, komma(per, 1000, "kg") if per >= 1000 else u(per, "g"))
    return mcq(q, komma(tot, 1000, "kg"), [komma(x, 1000, "kg") for x in (tot + per, n * (per // 1000 * 1000 + (per % 1000) // 10), tot - 1000) if x > 0 and x != tot],
               "%d %s %d g = %s g = <b>%s</b>." % (n, MAL, per, num(tot), komma(tot, 1000, "kg")))


def main():
    seen = set()
    sets = [
        ("Kommaschreibweise", mix(R, seen, [(any_of(lesen), 20)])),
        ("In die kleinere Einheit", mix(R, seen, [(any_of(kleiner), 20)])),
        ("In die größere Einheit", mix(R, seen, [(any_of(groesser), 20)])),
        ("Rechnen und vergleichen", mix(R, seen, [(any_of(rechnen), 20)])),
        ("Sachaufgaben mit Gewichten", mix(R, seen, [(sache, 20)])),
    ]
    body = lesson(
        ["1 kg = 1000 g und 1 t (Tonne) = 1000 kg.",
         "Mit Komma: 1,250 kg = 1 kg 250 g. Hinter dem Komma stehen immer <b>drei Stellen</b>.",
         "Schwere Dinge wie Autos oder Lastwagen wiegt man in Tonnen, leichte Dinge in Gramm.",
         "Zum Rechnen und Vergleichen bringst du alles in dieselbe Einheit."],
        [example("2 kg 50 g mit Komma", ["3 Stellen für die Gramm: 050"], "2,050 kg"),
         example("3,5 t in kg", ["3,500 t", "3000 kg + 500 kg"], "3500 kg")],
        [["2 kg 50 g = 2,5 kg", "2,050 kg (2,5 kg wären 2 kg 500 g)"],
         ["1 t = 100 kg", "1 t = 1000 kg"],
         ["900 g sind mehr als 1,2 kg", "1,2 kg = 1200 g, also mehr als 900 g"]],
        extra=table(["Einheiten", "Umrechnung", "Beispiel"], [["g und kg", "1 kg = 1000 g", "Tafel Schokolade 100 g, Mehl 1 kg"], ["kg und t", "1 t = 1000 kg", "Auto etwa 1,5 t"]]))
    faq = [
        {"q": "Wann lernen Kinder die Tonne?", "a": "In Klasse 4 kommt zur Einheit Gramm und Kilogramm die Tonne dazu: 1 t = 1000 kg."},
        {"q": "Warum hat kg drei Stellen hinter dem Komma?", "a": "Weil 1 kg = 1000 g ist. Die drei Stellen sind die Gramm von 000 bis 999."},
        {"q": "Wie schätzt man Gewichte?", "a": "Mit Vergleichsgrößen: 1 Liter Wasser wiegt etwa 1 kg, ein Auto etwa 1 bis 2 t."},
        {"q": "Sagt man Gewicht oder Masse?", "a": "In der Grundschule meist Gewicht. Physikalisch ist es die Masse; die Einheiten sind dieselben."},
    ]
    make_unit(R, "gewichte-und-tonnen", "G",
              "Die Schülerinnen und Schüler rechnen mit Gewichtsangaben in g, kg und t, nutzen die Kommaschreibweise, wandeln um und lösen Sachaufgaben (Zusammenfassung).",
              "Gewichte mit Komma: Gramm, Kilogramm und Tonnen",
              "Gewichte umrechnen Klasse 4 – g, kg, t Arbeitsblätter mit Lösungen",
              "Gewichte und Tonnen",
              "Klasse 4: Gewichte in g, kg und t umrechnen, Kommaschreibweise, rechnen, vergleichen und Sachaufgaben. 100 Übungsaufgaben mit Lösungen, kostenlos.",
              "1 t = 1000 kg, 1 kg = 1000 g",
              "Hinter dem Komma stehen drei Stellen: 2,050 kg = 2 kg 50 g.",
              body, faq, sets, 10, grade="klasse-4")


if __name__ == "__main__":
    main()
