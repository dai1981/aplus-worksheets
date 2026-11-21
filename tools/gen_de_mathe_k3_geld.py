# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 3: Geld – Euro und Cent（Leitidee Größen und Messen）
  python3 tools/gen_de_mathe_k3_geld.py
Geld zählen, Euro und Cent umwandeln, Kommaschreibweise, Preise addieren, Wechselgeld, Sachaufgaben.
Fehler: 3,05 € als 3 € 50 ct gelesen, 1 € = 10 ct, Wechselgeld vom falschen Betrag, Münzen beim Zählen doppelt.
"""
import random
from de_common import mcq, lesson, example, make_unit, mix, Kids, eur, geld_svg, MAL, NB, table

R = random.Random(49011)
KIDS = Kids(R)
COINS = [200, 100, 50, 20, 10, 5, 2, 1]
NOTES = [2000, 1000, 500]


def zaehlen():
    n = R.randint(3, 6)
    pool = NOTES + COINS if R.random() < 0.5 else COINS
    items = [R.choice(pool) for _ in range(n)]
    tot = sum(items)
    w = [tot + 10, tot - 10 if tot > 10 else tot + 20, tot + 100, tot - max(items) if len(items) > 1 else tot + 5, tot + min(items)]
    return mcq(geld_svg(items) + "Wie viel Geld ist das?", eur(tot), [eur(x) for x in w if x > 0 and x != tot],
               "Zähle vom größten Wert aus: %s = <b>%s</b>." % (" + ".join(eur(x, ct=True) for x in sorted(items, reverse=True)), eur(tot)))


def umwandeln():
    kind = R.choice(["ct", "eur", "ctzu"])
    if kind == "ct":
        e = R.randint(1, 9)
        c = R.choice([0, 5, 10, 20, 25, 30, 45, 50, 75, 80, 95, R.randint(1, 99)])
        tot = e * 100 + c
        ans = "%d%sct" % (tot, NB)
        w = ["%d%sct" % (x, NB) for x in (e * 10 + c, e * 1000 + c, int("%d%d" % (e, c)) if c >= 10 else e * 100 + c * 10)]
        return mcq("Wie viel Cent sind %s?" % eur(tot), ans, [x for x in w if x != ans],
                   "1 € = 100 ct. %d € = %d ct, dazu %d ct: <b>%d ct</b>." % (e, e * 100, c, tot))
    if kind == "eur":
        tot = R.randint(101, 999)
        if tot % 100 == 0:
            return None
        e, c = divmod(tot, 100)
        ans = eur(tot)
        w = ["%d,%d%s€" % (e, c, NB) if c < 10 else "%d,%d%s€" % (e, c // 10, NB), "%d,%02d%s€" % (tot // 10, tot % 10, NB), "%d,%02d%s€" % (e + 1, c, NB)]
        return mcq("Schreibe mit Komma: %d ct = ?" % tot, ans, [x for x in w if x != ans],
                   "100 ct = 1 €. %d ct = %d € %d ct = <b>%s</b>. Hinter dem Komma stehen immer zwei Stellen." % (tot, e, c, ans))
    e = R.randint(1, 9)
    c = R.randint(1, 9)
    tot = e * 100 + c
    ans = eur(tot)
    w = ["%d,%d%s€" % (e, c, NB), "%d,%d0%s€" % (e, c, NB), "%d,%02d%s€" % (c, e, NB)]
    return mcq("Wie schreibt man %d Euro und %d Cent mit Komma?" % (e, c), ans, [x for x in w if x != ans],
               "Cent hat immer zwei Stellen hinter dem Komma: %d ct → 0%d. Also <b>%s</b>." % (c, c, ans))


def preise():
    n = R.choice([2, 2, 3])
    prices = [R.randint(1, 15) * 100 + R.choice([0, 20, 49, 50, 75, 90, 95, 99]) for _ in range(n)]
    tot = sum(prices)
    w = [tot + 100, tot - 100 if tot > 100 else tot + 200, tot + 10, sum(p // 100 for p in prices) * 100 + sum(p % 100 for p in prices) % 100]
    return mcq("Rechne zusammen: %s" % " + ".join(eur(p) for p in prices), eur(tot), [eur(x) for x in w if x > 0 and x != tot],
               "Euro und Cent getrennt rechnen. Werden es mehr als 100 ct, ist das 1 € mehr. Ergebnis: <b>%s</b>." % eur(tot))


def wechsel():
    pay = R.choice([500, 1000, 2000, 5000])
    price = R.randint(1, pay // 100 - 1) * 100 + R.choice([0, 10, 25, 49, 50, 75, 90, 99])
    if price >= pay:
        return None
    back = pay - price
    w = [back + 100, back - 100 if back > 100 else back + 200, (pay // 100 - price // 100) * 100 + (100 - price % 100 if price % 100 else 0),
         back + 10, price]
    return mcq("Ein Spiel kostet %s. Du bezahlst mit %s. Wie viel Wechselgeld bekommst du?" % (eur(price), eur(pay)), eur(back),
               [eur(x) for x in w if x > 0 and x != back],
               "Ergänze von %s bis %s: <b>%s</b>." % (eur(price), eur(pay), eur(back)))


SHOP = [("ein Eis", 150, "Kugeln Eis"), ("eine Brezel", 90, "Brezeln"), ("ein Buch", 899, "Bücher"), ("einen Stift", 120, "Stifte"),
        ("ein Heft", 75, "Hefte"), ("einen Ball", 650, "Bälle"), ("eine Trinkflasche", 499, "Trinkflaschen"),
        ("ein Kuscheltier", 1299, "Kuscheltiere"), ("ein Puzzle", 795, "Puzzles"), ("einen Malblock", 249, "Malblöcke")]


def sache():
    p = KIDS.next()
    kind = R.choice(["kaufen", "reicht", "sparen", "mal"])
    if kind == "kaufen":
        (a, pa, _), (b, pb, _) = R.sample(SHOP, 2)
        have = R.choice([1000, 2000, 5000])
        if pa + pb >= have:
            return None
        q = "%s hat %s. %s kauft %s für %s und %s für %s. Wie viel Geld hat %s noch?" % (p[0], eur(have), p[1].capitalize(), a, eur(pa), b, eur(pb), p[1])
        r = have - pa - pb
        w = [pa + pb, have - pa, r + 100, r - 10 if r > 10 else r + 20]
        return mcq(q, eur(r), [eur(x) for x in w if x > 0 and x != r],
                   "Zusammen: %s + %s = %s. %s − %s = <b>%s</b>." % (eur(pa), eur(pb), eur(pa + pb), eur(have), eur(pa + pb), eur(r)))
    if kind == "reicht":
        (a, pa, _), (b, pb, _) = R.sample(SHOP, 2)
        have = (pa + pb) // 100 * 100 + R.choice([-200, -100, 100, 200])
        if have <= 0:
            return None
        ok = have >= pa + pb
        q = "%s hat %s und möchte %s (%s) und %s (%s) kaufen. Reicht das Geld?" % (p[0], eur(have), a, eur(pa), b, eur(pb))
        ans = ("Ja, es bleiben %s übrig." % eur(have - pa - pb)) if ok else ("Nein, es fehlen %s." % eur(pa + pb - have))
        w = [("Nein, es fehlen %s." % eur(abs(have - pa - pb))) if ok else ("Ja, es bleiben %s übrig." % eur(abs(have - pa - pb))),
             ("Ja, es bleiben %s übrig." % eur(abs(have - pa - pb) + 100)), ("Nein, es fehlen %s." % eur(abs(have - pa - pb) + 100))]
        return mcq(q, ans, w, "Zusammen kostet es %s + %s = %s. %s" % (eur(pa), eur(pb), eur(pa + pb), "<b>" + ans + "</b>"))
    if kind == "sparen":
        k = R.choice([150, 200, 250, 300, 500])
        n = R.randint(3, 8)
        q = "%s spart jede Woche %s. Wie viel Geld hat %s nach %d Wochen gespart?" % (p[0], eur(k), p[1], n)
        r = k * n
        w = [k + n * 100, k * (n - 1), r + 100, r + k]
        return mcq(q, eur(r), [eur(x) for x in w if x > 0 and x != r], "%d %s %s = <b>%s</b>." % (n, MAL, eur(k), eur(r)))
    (a, pa, pl) = R.choice(SHOP[:6])
    n = R.randint(2, 5)
    q = "%s kauft %d %s für je %s. Wie viel muss %s bezahlen?" % (p[0], n, pl, eur(pa), p[1])
    r = n * pa
    w = [pa + n * 100, (n - 1) * pa, r + 100, r - 10]
    return mcq(q, eur(r), [eur(x) for x in w if x > 0 and x != r], "%d %s %s = <b>%s</b>." % (n, MAL, eur(pa), eur(r)))


def main():
    seen = set()
    sets = [
        ("Geld zählen", mix(R, seen, [(zaehlen, 20)])),
        ("Euro und Cent", mix(R, seen, [(umwandeln, 20)])),
        ("Preise zusammenrechnen", mix(R, seen, [(preise, 20)])),
        ("Wechselgeld", mix(R, seen, [(wechsel, 20)])),
        ("Sachaufgaben mit Geld", mix(R, seen, [(sache, 20)])),
    ]
    body = lesson(
        ["1 Euro (€) hat 100 Cent (ct). 1 € = 100 ct.",
         "Mit Komma: Vor dem Komma stehen die Euro, dahinter die Cent. Hinter dem Komma stehen <b>immer zwei Ziffern</b>: 3,05 € = 3 € 5 ct.",
         "Zähle Geld vom größten Schein oder der größten Münze aus.",
         "Wechselgeld findest du durch <b>Ergänzen</b>: vom Preis bis zum bezahlten Betrag."],
        [example("Wie viel Cent sind 4,75 €?", ["4 € = 400 ct", "400 ct + 75 ct = 475 ct"], "475 ct"),
         example("Preis 6,40 €, bezahlt mit 10 €. Wechselgeld?", ["6,40 € + 0,60 € = 7 €", "7 € + 3 € = 10 €", "0,60 € + 3 € = 3,60 €"], "3,60 €")],
        [["3,05 € als 3 € 50 ct lesen", "Die erste Ziffer nach dem Komma sind die Zehner-Cent: 3,05 € = 3 € 5 ct"],
         ["1 € = 10 ct", "1 € = 100 ct"],
         ["Wechselgeld: Preis + bezahlter Betrag", "Ergänzen oder bezahlter Betrag minus Preis"]],
        extra=table(["Münzen", "Scheine"], [["1 ct, 2 ct, 5 ct, 10 ct, 20 ct, 50 ct, 1 €, 2 €", "5 €, 10 €, 20 €, 50 €, 100 €, 200 €"]]))
    faq = [
        {"q": "Wann lernen Kinder die Kommaschreibweise bei Geld?", "a": "In Klasse 3: Beträge wie 3,50 € werden gelesen, geschrieben und in Cent umgewandelt."},
        {"q": "Warum stehen hinter dem Komma zwei Ziffern?", "a": "Weil 1 € = 100 ct ist. Die zwei Stellen sind die Cent von 0 bis 99."},
        {"q": "Wie rechnet man Wechselgeld am einfachsten?", "a": "Durch Ergänzen wie an der Kasse: vom Preis bis zum nächsten vollen Euro, dann bis zum bezahlten Betrag."},
        {"q": "Welche Münzen und Scheine gibt es?", "a": "Münzen: 1, 2, 5, 10, 20, 50 Cent sowie 1 und 2 Euro. Scheine: 5, 10, 20, 50, 100 und 200 Euro."},
    ]
    make_unit(R, "geld", "G",
              "Die Schülerinnen und Schüler rechnen mit Geldbeträgen in Euro und Cent, nutzen die Kommaschreibweise, wandeln Einheiten um und lösen Sachaufgaben zum Einkaufen (Zusammenfassung).",
              "Geld: Euro und Cent",
              "Rechnen mit Geld Klasse 3 – Euro und Cent Arbeitsblätter mit Lösungen",
              "Geld: Euro und Cent",
              "Rechnen mit Geld für Klasse 3: Geld zählen, Euro und Cent mit Komma, Preise addieren, Wechselgeld und Sachaufgaben. 100 Übungsaufgaben mit Lösungen, kostenlos.",
              "1 € = 100 ct",
              "Hinter dem Komma stehen immer zwei Stellen: 3,05 € = 3 € 5 ct.",
              body, faq, sets, 11)


if __name__ == "__main__":
    main()
