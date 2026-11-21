# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 2: Geld – Euro und Cent bis 100 €（Leitidee Größen und Messen）
  python3 tools/gen_de_mathe_k2_geld.py
Geld zählen, Euro und Cent (1 € = 100 ct), Beträge legen, Preise zusammenrechnen, Wechselgeld, Sachaufgaben.
Fehler: Anzahl der Münzen statt Wert gezählt, Euro und Cent vermischt (1 € = 10 ct), beim Wechselgeld falsch ergänzt.
"""
import random
from de_common import mcq, lesson, example, make_unit, mix, Kids, geld_svg, table

R = random.Random(49212)
KIDS = Kids(R)
COINS_CT = [50, 20, 10, 5, 2, 1]
EURO = [5000, 2000, 1000, 500, 200, 100]


def e(c):
    return "%d €" % (c // 100) if c >= 100 else "%d ct" % c


def zaehlen():
    kind = R.choice(["euro", "euro", "cent"])
    n = R.randint(3, 6)
    pool = EURO if kind == "euro" else COINS_CT
    items = [R.choice(pool) for _ in range(n)]
    tot = sum(items)
    if (kind == "euro" and tot > 10000) or (kind == "cent" and tot >= 100):
        return None
    unit = 100 if kind == "euro" else 1
    w = [len(items) * unit, tot + 10 * unit, tot - min(items) if tot - min(items) > 0 else tot + 5 * unit, tot + 5 * unit]
    fmt = (lambda c: "%d €" % (c // 100)) if kind == "euro" else (lambda c: "%d ct" % c)
    return mcq(geld_svg(items) + "Wie viel Geld ist das?", fmt(tot), [fmt(x) for x in w if x > 0 and x != tot],
               "Zähle vom größten Wert aus: %s = <b>%s</b>." % (" + ".join(e(x) for x in sorted(items, reverse=True)), fmt(tot)))


def euro_cent():
    kind = R.choice(["ct", "eur", "legen", "mehr"])
    if kind == "ct":
        a = R.randint(1, 9)
        return mcq("Wie viel Cent sind %d €?" % a, "%d ct" % (100 * a), ["%d ct" % x for x in (10 * a, a, 1000 * a)],
                   "1 € = 100 ct. %d € = <b>%d ct</b>." % (a, 100 * a))
    if kind == "eur":
        a = R.randint(1, 9)
        c = R.randint(1, 9) * 10 if R.random() < 0.6 else R.randint(1, 99)
        tot = 100 * a + c
        return mcq("%d ct = ? € ? ct" % tot, "%d € %d ct" % (a, c), ["%d € %d ct" % (tot // 10, tot % 10), "%d € %d ct" % (a + 1, c), "%d € %d ct" % (c, a)],
                   "100 ct = 1 €. %d ct = %d € und %d ct: <b>%d € %d ct</b>." % (tot, a, c, a, c))
    if kind == "legen":
        target = R.choice([30, 40, 60, 70, 80, 90, 15, 25, 35, 45, 55, 65, 75, 85, 95])
        best = []
        r = target
        for c in COINS_CT:
            while r >= c:
                best.append(c)
                r -= c
        wrong = []
        for _ in range(10):
            alt = list(best)
            i = R.randrange(len(alt))
            alt[i] = R.choice([c for c in COINS_CT if c != alt[i]])
            if sum(alt) != target:
                wrong.append(" + ".join("%d ct" % x for x in sorted(alt, reverse=True)))
        wrong = list(dict.fromkeys(wrong))
        if len(wrong) < 3:
            return None
        ans = " + ".join("%d ct" % x for x in best)
        return mcq("Welche Münzen ergeben genau %d ct?" % target, ans, wrong[:3], "%s = <b>%d ct</b>." % (ans, target))
    a, b = R.choice([(50, 100), (20, 100), (10, 100), (50, 200), (20, 200), (10, 50), (5, 50), (2, 10), (5, 20)])
    n = b // a
    return mcq("Wie viele %s-Münzen braucht man für %s?" % (e(a).replace(" ", "-"), e(b)), str(n), [str(n + 1), str(n * 2), str(b - a) if b - a < 100 else str(n - 1)],
               "%s = %d %s %s: <b>%d</b> Münzen." % (e(b), n, "·", e(a), n))


def preise():
    n = R.choice([2, 2, 3])
    prices = [R.randint(2, 30) for _ in range(n)]
    tot = sum(prices)
    if tot > 100:
        return None
    things = R.sample(["einen Ball", "ein Buch", "ein Puzzle", "eine Mütze", "ein Spiel", "einen Rucksack", "eine Taschenlampe", "ein Malset"], n)
    p = KIDS.next()
    q = "%s kauft %s." % (p[0], " und ".join(["%s für %d €" % (t, c) for t, c in zip(things, prices)]) if n == 2 else
                          ", ".join("%s für %d €" % (t, c) for t, c in zip(things[:-1], prices[:-1])) + " und %s für %d €" % (things[-1], prices[-1]))
    return mcq(q + " Wie viel kostet alles zusammen?", "%d €" % tot,
               ["%d €" % x for x in (tot + 10, tot - 10 if tot > 10 else tot + 20, tot - prices[-1], tot + 1)],
               "%s = <b>%d €</b>." % (" + ".join("%d €" % c for c in prices), tot))


DINGE = [("Ein T-Shirt", 8, 25), ("Ein Buch", 6, 20), ("Ein Spielzeugauto", 3, 15), ("Eine Trinkflasche", 5, 18), ("Ein Federmäppchen", 6, 25),
         ("Ein Kuscheltier", 8, 30), ("Ein Fahrradhelm", 25, 60), ("Ein Schulranzen", 55, 95), ("Ein Paar Inliner", 40, 90), ("Ein Fußball", 9, 35)]


def wechsel():
    thing, lo, hi = R.choice(DINGE)
    price = R.randint(lo, hi)
    pay = min(x for x in (10, 20, 50, 100) if x > price)
    back = pay - price
    z, ee = divmod(price, 10)
    w = [back + 10, back - 10 if back > 10 else back + 2, (9 - z) * 10 + (10 - ee) if ee and pay == 100 else back + 1, price]
    return mcq("%s kostet %d €. Du bezahlst mit einem %d-Euro-Schein. Wie viel Wechselgeld bekommst du?" % (thing, price, pay), "%d €" % back,
               ["%d €" % x for x in w if x > 0 and x != back],
               "Ergänze von %d € bis %d €: %d € + <b>%d €</b> = %d €." % (price, pay, price, back, pay))


def sache():
    kind = R.choice(["sparen", "taschengeld", "teilen", "reicht", "eis"])
    p = KIDS.next()
    if kind == "sparen":
        w, k = R.choice([2, 3, 5]), R.randint(4, 10)
        return mcq("%s spart jede Woche %d €. Wie viel Geld hat %s nach %d Wochen?" % (p[0], w, p[1], k), "%d €" % (w * k),
                   ["%d €" % x for x in (w + k, w * k + w, w * k - w)], "%d %s %d € = <b>%d €</b>." % (k, "·", w, w * k))
    if kind == "taschengeld":
        a, b = R.randint(20, 60), R.randint(5, 19)
        return mcq("%s hat %d €. %s kauft ein Buch für %d €. Wie viel Geld hat %s noch?" % (p[0], a, p[1].capitalize(), b, p[1]), "%d €" % (a - b),
                   ["%d €" % x for x in (a + b, a - b + 10, a - b - 1)], "%d € − %d € = <b>%d €</b>." % (a, b, a - b))
    if kind == "teilen":
        g, k = R.randint(2, 5), R.randint(2, 10)
        return mcq("%d Kinder bekommen zusammen %d €. Sie teilen gerecht. Wie viel bekommt jedes Kind?" % (g, g * k), "%d €" % k,
                   ["%d €" % x for x in (g * k - g, k + 1, g if g != k else k + 2)], "%d € : %d = <b>%d €</b>." % (g * k, g, k))
    if kind == "reicht":
        a, b, have = R.randint(10, 40), R.randint(10, 40), R.randint(30, 80)
        tot = a + b
        ok = have >= tot
        ans = "Ja, es bleiben %d € übrig." % (have - tot) if ok else "Nein, es fehlen %d €." % (tot - have)
        if have == tot:
            return None
        w = ["Nein, es fehlen %d €." % abs(have - tot) if ok else "Ja, es bleiben %d € übrig." % abs(have - tot),
             "Ja, es bleiben %d € übrig." % (have - a) if have > a else "Nein, es fehlen %d €." % (a - have + 5),
             "Nein, es fehlen %d €." % (abs(have - tot) + 10)]
        return mcq("%s hat %d €. %s möchte Schuhe für %d € und eine Jacke für %d € kaufen. Reicht das Geld?" % (p[0], have, p[1].capitalize(), a, b), ans, w,
                   "%d € + %d € = %d €. %s" % (a, b, tot, "<b>%s</b>" % ans))
    k = R.randint(2, 6)
    c = R.choice([1, 2])
    return mcq("Eine Kugel Eis kostet %d €. %s kauft %d Kugeln für sich und %d Kugeln für die Schwester. Wie viel kostet das?" % (c, p[0], k, k), "%d €" % (2 * k * c),
               ["%d €" % x for x in (k * c, 2 * k + c, 2 * k * c + c)], "%d + %d = %d Kugeln. %d %s %d € = <b>%d €</b>." % (k, k, 2 * k, 2 * k, "·", c, 2 * k * c))


def main():
    seen = set()
    sets = [
        ("Geld zählen", mix(R, seen, [(zaehlen, 20)])),
        ("Euro und Cent", mix(R, seen, [(euro_cent, 20)])),
        ("Preise zusammenrechnen", mix(R, seen, [(preise, 20)])),
        ("Wechselgeld", mix(R, seen, [(wechsel, 20)])),
        ("Sachaufgaben mit Geld", mix(R, seen, [(sache, 20)])),
    ]
    body = lesson(
        ["Es gibt Münzen (1 ct bis 2 €) und Scheine (5 € bis 500 €).",
         "<b>1 € = 100 ct</b>. 3 € 40 ct sind 340 ct.",
         "Zähle Geld vom größten Wert zum kleinsten: erst die Scheine, dann die Münzen.",
         "Beim Wechselgeld ergänzt du vom Preis bis zum bezahlten Betrag."],
        [example("20 € + 10 € + 5 € + 2 €", ["20 + 10 = 30", "30 + 5 = 35", "35 + 2 = 37"], "37 €"),
         example("Ein Buch kostet 13 €, du gibst 20 €", ["13 € + 7 € = 20 €"], "7 € Wechselgeld")],
        [["Münzen zählen statt Werte addieren", "Den Wert jeder Münze addieren"],
         ["1 € = 10 ct", "1 € = 100 ct"],
         ["Beim Wechselgeld den Preis nennen", "Gefragt ist, was zurückkommt"]],
        extra=table(["Münzen", "Scheine"], [["1 ct, 2 ct, 5 ct, 10 ct, 20 ct, 50 ct, 1 €, 2 €", "5 €, 10 €, 20 €, 50 €, 100 €, 200 €"]]))
    faq = [
        {"q": "Welche Münzen und Scheine gibt es beim Euro?", "a": "Münzen: 1, 2, 5, 10, 20 und 50 Cent sowie 1 und 2 Euro. Scheine: 5, 10, 20, 50, 100 und 200 Euro (der 500-Euro-Schein wird nicht mehr ausgegeben)."},
        {"q": "Rechnen Kinder in Klasse 2 schon mit Komma?", "a": "Meist noch nicht. In Klasse 2 schreibt man 3 € 40 ct. Die Kommaschreibweise 3,40 € kommt in Klasse 3."},
        {"q": "Wie übt man das Rechnen mit Geld?", "a": "Mit echtem oder Spielgeld beim Einkaufen spielen: Preise zusammenrechnen, bezahlen und Wechselgeld zählen."},
        {"q": "Wie berechnet man Wechselgeld am einfachsten?", "a": "Durch Ergänzen: Vom Preis aus zählt man bis zum bezahlten Betrag, so wie es an der Kasse gemacht wird."},
    ]
    make_unit(R, "geld", "G",
              "Die Schülerinnen und Schüler kennen Münzen und Scheine, wandeln Euro und Cent um, legen und zählen Geldbeträge bis 100 €, rechnen Preise zusammen und bestimmen Wechselgeld (Zusammenfassung).",
              "Geld: Euro und Cent bis 100 €",
              "Rechnen mit Geld Klasse 2 – Arbeitsblätter mit Lösungen",
              "Geld",
              "Geld für Klasse 2: Münzen und Scheine zählen, Euro und Cent, Preise zusammenrechnen, Wechselgeld und Sachaufgaben. 100 Übungsaufgaben mit Lösungen, kostenlos.",
              "1 € = 100 ct",
              "Geld vom größten zum kleinsten Wert zählen.",
              body, faq, sets, 12, grade="klasse-2")


if __name__ == "__main__":
    main()
