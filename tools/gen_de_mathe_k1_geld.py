# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 1: Geld bis 20 €（Leitidee Größen und Messen）
  python3 tools/gen_de_mathe_k1_geld.py
Münzen und Scheine erkennen, Euro zählen, Cent zählen, passend bezahlen, Einkaufen.
Fehler: Anzahl der Münzen statt Wert gezählt, Euro und Cent verwechselt, beim Rückgeld falsch gerechnet.
"""
import random
from de_common import mcq, lesson, example, make_unit, mix, Kids, geld_svg, table

R = random.Random(49411)
KIDS = Kids(R)
EUR = [2000, 1000, 500, 200, 100]
CT = [50, 20, 10, 5, 2, 1]


def name(c):
    return "%d €" % (c // 100) if c >= 100 else "%d ct" % c


def erkennen():
    c = R.choice(EUR + CT)
    kind = R.choice(["wert", "art"])
    if kind == "wert":
        w = {2000: ["10 €", "2 €", "20 ct"], 1000: ["1 €", "100 €", "10 ct"], 500: ["50 €", "5 ct", "50 ct"], 200: ["2 ct", "20 €", "20 ct"],
             100: ["1 ct", "10 €", "10 ct"], 50: ["50 €", "5 ct", "5 €"], 20: ["20 €", "2 ct", "2 €"], 10: ["10 €", "1 ct", "1 €"],
             5: ["5 €", "50 ct", "2 ct"], 2: ["2 €", "20 ct", "1 ct"], 1: ["1 €", "10 ct", "2 ct"]}[c]
        return mcq(geld_svg([c]) + "Wie viel ist das wert?", name(c), w, "Das ist <b>%s</b>." % name(c))
    if c >= 500:
        ans = "ein Schein"
    else:
        ans = "eine Münze"
    return mcq(geld_svg([c]) + "Ist das ein Schein oder eine Münze? Wie viel ist es wert?", "%s: %s" % (ans, name(c)),
               ["%s: %s" % ("eine Münze" if ans == "ein Schein" else "ein Schein", name(c)), "%s: %s" % (ans, name(c * 10) if c < 200 else name(c // 10)),
                "%s: %s" % ("eine Münze" if ans == "ein Schein" else "ein Schein", name(c * 10) if c < 200 else name(c // 10))],
               "Scheine gibt es ab 5 €, Münzen bis 2 €. Das ist <b>%s: %s</b>." % (ans, name(c)))


def euro():
    n = R.randint(2, 4)
    items = [R.choice(EUR) for _ in range(n)]
    tot = sum(items) // 100
    if tot > 20:
        return None
    return mcq(geld_svg(items) + "Wie viel Geld ist das?", "%d €" % tot, ["%d €" % x for x in (n, tot + 1, tot - 1 if tot > 1 else tot + 2, tot + 5) if x != tot],
               "Zähle vom größten Wert aus: %s = <b>%d €</b>." % (" + ".join("%d €" % (c // 100) for c in sorted(items, reverse=True)), tot))


def cent():
    n = R.randint(2, 4)
    items = [R.choice([10, 5, 2, 1, 10, 5, 2, 1]) for _ in range(n)]
    tot = sum(items)
    if tot > 20:
        return None
    return mcq(geld_svg(items) + "Wie viel Geld ist das?", "%d ct" % tot, ["%d ct" % x for x in (n, tot + 1, tot - 1, tot + 2) if x != tot and x > 0] + ["%d €" % tot],
               "%s = <b>%d ct</b>." % (" + ".join("%d ct" % c for c in sorted(items, reverse=True)), tot))


def bezahlen():
    kind = R.choice(["passend", "reicht"])
    if kind == "passend":
        target = R.randint(3, 20)
        best = []
        r = target
        for c in (20, 10, 5, 2, 1):
            while r >= c:
                best.append(c)
                r -= c
        ans = " + ".join("%d €" % c for c in best)
        wrong = []
        for _ in range(12):
            alt = list(best)
            i = R.randrange(len(alt))
            alt[i] = R.choice([c for c in (20, 10, 5, 2, 1) if c != alt[i]])
            if sum(alt) != target:
                wrong.append(" + ".join("%d €" % c for c in sorted(alt, reverse=True)))
        wrong = list(dict.fromkeys(wrong))
        if len(wrong) < 3:
            return None
        return mcq("Du willst genau %d € bezahlen. Welches Geld passt?" % target, ans, wrong[:3], "%s = <b>%d €</b>." % (ans, target))
    have = R.randint(3, 20)
    price = R.randint(2, 20)
    if have == price:
        return None
    ok = have > price
    ans = "Ja, es reicht." if ok else "Nein, es fehlen %d €." % (price - have)
    return mcq("%s hat %d €. Ein Spiel kostet %d €. Reicht das Geld?" % (KIDS.next()[0], have, price), ans,
               ["Nein, es fehlen %d €." % abs(price - have) if ok else "Ja, es reicht.", "Nein, es fehlen %d €." % (abs(price - have) + 1), "Ja, es bleiben %d € übrig." % (have + price) if have + price <= 40 else "Ja, es bleiben 1 € übrig."],
               "%d € %s %d €: <b>%s</b>" % (have, "ist mehr als" if ok else "ist weniger als", price, ans))


DINGE = [("ein Heft", 1, 3), ("einen Ball", 3, 9), ("ein Buch", 5, 12), ("ein Eis", 1, 3), ("einen Stift", 1, 2), ("ein Puzzle", 4, 10),
         ("eine Brezel", 1, 2), ("ein Kuscheltier", 6, 15), ("einen Malblock", 2, 4), ("ein Spielzeugauto", 2, 8)]


def einkaufen():
    kind = R.choice(["zusammen", "rueck", "rueck"])
    p = KIDS.next()
    if kind == "zusammen":
        (t1, l1, h1), (t2, l2, h2) = R.sample(DINGE, 2)
        a, b = R.randint(l1, h1), R.randint(l2, h2)
        if a + b > 20:
            return None
        return mcq("%s kauft %s für %d € und %s für %d €. Wie viel kostet das zusammen?" % (p[0], t1, a, t2, b), "%d €" % (a + b),
                   ["%d €" % x for x in (abs(a - b) if a != b else a + b + 2, a + b + 1, a + b - 1)], "%d € + %d € = <b>%d €</b>." % (a, b, a + b))
    t, l, h = R.choice(DINGE)
    a = R.randint(l, h)
    pay = 10 if a < 10 else 20
    if a == pay:
        return None
    return mcq("%s kauft %s für %d € und bezahlt mit einem %d-Euro-Schein. Wie viel Geld bekommt %s zurück?" % (p[0], t, a, pay, p[1]), "%d €" % (pay - a),
               ["%d €" % x for x in (pay + a, pay - a + 1, a) if x != pay - a] + ["%d €" % (pay - a - 1)] if pay - a > 1 else ["%d €" % x for x in (pay + a, 2, a)],
               "%d € + ? = %d €. Zurück gibt es <b>%d €</b>." % (a, pay, pay - a))


def main():
    seen = set()
    sets = [
        ("Münzen und Scheine", mix(R, seen, [(erkennen, 20)])),
        ("Euro zählen", mix(R, seen, [(euro, 20)])),
        ("Cent zählen", mix(R, seen, [(cent, 20)])),
        ("Bezahlen", mix(R, seen, [(bezahlen, 20)])),
        ("Einkaufen", mix(R, seen, [(einkaufen, 20)])),
    ]
    body = lesson(
        ["Es gibt <b>Münzen</b> (1 ct, 2 ct, 5 ct, 10 ct, 20 ct, 50 ct, 1 €, 2 €) und <b>Scheine</b> (5 €, 10 €, 20 € …).",
         "Zähle den <b>Wert</b>, nicht die Anzahl. Eine 2-€-Münze ist mehr wert als drei 10-ct-Münzen.",
         "Beginne beim Zählen mit dem größten Wert.",
         "Euro und Cent darfst du nicht einfach zusammenzählen."],
        [example("10 € + 5 € + 2 €", ["10 + 5 = 15", "15 + 2 = 17"], "17 €"),
         example("Ein Ball kostet 7 €, du zahlst mit 10 €", ["7 + 3 = 10"], "3 € zurück")],
        [["Münzen zählen statt Werte addieren", "Den Wert jeder Münze addieren"],
         ["5 ct und 5 € verwechseln", "Auf das Zeichen achten: ct oder €"],
         ["Beim Rückgeld den Preis nennen", "Ergänzen bis zum bezahlten Betrag"]],
        extra=table(["Münzen", "Scheine"], [["1 ct, 2 ct, 5 ct, 10 ct, 20 ct, 50 ct, 1 €, 2 €", "5 €, 10 €, 20 €"]]))
    faq = [
        {"q": "Welches Geld lernen Kinder in Klasse 1?", "a": "Alle Münzen und die Scheine bis 20 €. Gerechnet wird mit ganzen Euro bis 20 und mit Cent bis 20."},
        {"q": "Wie übt man das Geldzählen?", "a": "Mit Spielgeld beim Kaufladen-Spiel: Preise auf Zettel schreiben, bezahlen und Rückgeld geben."},
        {"q": "Warum fällt Rückgeld schwer?", "a": "Man muss ergänzen: Von 7 € bis 10 € sind es 3 €. Das übt man am besten mit echtem Geld."},
        {"q": "Wie viele Cent sind 1 Euro?", "a": "100 Cent. Das ist für Klasse 1 nur ein erster Ausblick; gerechnet wird mit Euro und Cent getrennt."},
    ]
    make_unit(R, "geld", "G",
              "Die Schülerinnen und Schüler kennen Münzen und Scheine, bestimmen Geldbeträge bis 20 € und bis 20 ct, legen Beträge passend und lösen einfache Einkaufsaufgaben (Zusammenfassung).",
              "Geld: Euro und Cent bis 20",
              "Rechnen mit Geld Klasse 1 – Arbeitsblätter mit Lösungen",
              "Geld",
              "Geld für Klasse 1: Münzen und Scheine erkennen, Euro und Cent zählen, passend bezahlen und Einkaufen. 100 Übungsaufgaben mit Bildern und Lösungen, kostenlos.",
              "Den Wert zählen, nicht die Münzen.",
              "Vom größten Wert aus zählen.",
              body, faq, sets, 11, grade="klasse-1")


if __name__ == "__main__":
    main()
