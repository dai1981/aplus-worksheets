# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 4: Rechnen mit Geld（Leitidee Größen und Messen）
  python3 tools/gen_de_mathe_k4_geld.py
Euro und Cent mit Komma, schriftlich addieren und subtrahieren, malnehmen und teilen, Preise vergleichen, Sachaufgaben.
Fehler: 4,05 € als 4,50 € gelesen, Komma beim Rechnen nicht untereinander, Wechselgeld vom falschen Betrag.
"""
import random
from de_common import mcq, num, lesson, example, make_unit, mix, Kids, MAL, GETEILT, eur, NB, table

R = random.Random(49112)
KIDS = Kids(R)


def falsch_ct(c):
    e, r = divmod(c, 100)
    if r < 10 and r:
        return e * 100 + r * 10
    return None


def umwandeln():
    kind = R.choice(["ct", "eur", "eur"])
    c = R.randint(101, 99999)
    if c % 100 == 0:
        return None
    if R.random() < 0.3:
        c = c // 100 * 100 + R.randint(1, 9)
    if kind == "ct":
        w = [c // 10, c * 10, falsch_ct(c)]
        return mcq("%s = ? ct" % eur(c), "%s%sct" % (num(c), NB), ["%s%sct" % (num(x), NB) for x in w if x and x != c],
                   "1 € = 100 ct. %s = <b>%s ct</b>." % (eur(c), num(c)))
    w = [falsch_ct(c), c * 10, c + 100]
    if c % 100 < 10:
        wrong = "%s,%d%s€" % (num(c // 100), c % 100, NB)
    else:
        wrong = None
    return mcq("%s ct = ? €" % num(c), eur(c), [x for x in [wrong] + [eur(v) for v in w if v] if x and x != eur(c)],
               "100 ct = 1 €. %s ct = <b>%s</b>." % (num(c), eur(c)))


def plusminus():
    op = R.choice(["+", "−"])
    a = R.randint(150, 9999)
    b = R.randint(99, 4999) if op == "+" else R.randint(99, a - 50)
    r = a + b if op == "+" else a - b
    w = [r + 100, r - 10 if r > 10 else r + 10, r + 1000 if r > 1000 else r + 90, a + b // 10 if op == "+" else a - b // 10]
    return mcq("%s %s %s = ?" % (eur(a), op, eur(b)), eur(r), [eur(x) for x in w if x > 0 and x != r],
               "Komma unter Komma schreiben und wie mit Cent rechnen: %s ct %s %s ct = %s ct = <b>%s</b>." % (num(a), op, num(b), num(r), eur(r)))


def maldurch():
    kind = R.choice(["mal", "durch"])
    if kind == "mal":
        a = R.randint(105, 2499)
        n = R.randint(2, 9)
        r = a * n
        w = [r + 100, a * n // 10, a + n * 100, r - n]
        return mcq("%d %s %s = ?" % (n, MAL, eur(a)), eur(r), [eur(x) for x in w if x > 0 and x != r],
                   "%d %s %s ct = %s ct = <b>%s</b>." % (n, MAL, num(a), num(r), eur(r)))
    n = R.randint(2, 9)
    q = R.randint(105, 2499)
    a = q * n
    w = [q + 100, q * 10, q - 10 if q > 10 else q + 5, a - n]
    return mcq("%s %s %d = ?" % (eur(a), GETEILT, n), eur(q), [eur(x) for x in w if x > 0 and x != q],
               "%s ct %s %d = %s ct = <b>%s</b>." % (num(a), GETEILT, n, num(q), eur(q)))


def angebot():
    n1, n2 = R.choice([(2, 3), (3, 5), (4, 6), (2, 5), (6, 10)])
    p1 = R.randint(80, 400)
    unit1 = p1
    unit2 = R.choice([unit1 - R.randint(3, 20), unit1 + R.randint(3, 20)])
    pr1, pr2 = n1 * unit1, n2 * unit2
    thing = R.choice([("Joghurts", "Joghurt"), ("Brötchen", "Brötchen"), ("Äpfel", "Apfel"), ("Hefte", "Heft")])
    q = ("Angebot A: %d %s für %s. Angebot B: %d %s für %s. Bei welchem Angebot kostet ein Stück weniger?"
         % (n1, thing[0], eur(pr1), n2, thing[0], eur(pr2)))
    cheaper = "A" if unit1 < unit2 else "B"
    ans = "Angebot %s" % cheaper
    return mcq(q, ans, ["Angebot %s" % ("B" if cheaper == "A" else "A"), "Beide gleich teuer", "Das kann man nicht berechnen"],
               "Preis für 1 Stück: A %s %s %d = %s, B %s %s %d = %s. Günstiger ist <b>%s</b>."
               % (eur(pr1), GETEILT, n1, eur(unit1), eur(pr2), GETEILT, n2, eur(unit2), ans))


SHOP = [("ein Fahrradhelm", 3999), ("ein Rucksack", 2495), ("eine Jacke", 4990), ("ein Paar Schuhe", 5999), ("ein Spiel", 1999),
        ("ein Buch", 1295), ("ein Fußball", 1849), ("eine Trinkflasche", 899), ("ein Federmäppchen", 1450)]


def sache():
    p = KIDS.next()
    kind = R.choice(["einkauf", "sparen", "teilen", "reicht"])
    if kind == "einkauf":
        (a, pa), (b, pb) = R.sample(SHOP, 2)
        pay = R.choice([5000, 10000])
        if pa + pb >= pay:
            return None
        r = pay - pa - pb
        q = "%s kauft %s für %s und %s für %s. %s bezahlt mit %s. Wie viel Wechselgeld bekommt %s?" % (p[0], a, eur(pa), b, eur(pb), p[1].capitalize(), eur(pay), p[1])
        return mcq(q, eur(r), [eur(x) for x in (pa + pb, pay - pa, r + 100, r + 10) if x > 0 and x != r],
                   "%s + %s = %s. %s − %s = <b>%s</b>." % (eur(pa), eur(pb), eur(pa + pb), eur(pay), eur(pa + pb), eur(r)))
    if kind == "sparen":
        w, s = R.randint(6, 30), R.choice([250, 350, 450, 500, 750])
        r = w * s
        q = "%s spart jede Woche %s. Wie viel Geld hat %s nach %d Wochen?" % (p[0], eur(s), p[1], w)
        return mcq(q, eur(r), [eur(x) for x in (r + s, w * (s // 100) * 100, s * (w + 1) + 100) if x != r], "%d %s %s = <b>%s</b>." % (w, MAL, eur(s), eur(r)))
    if kind == "teilen":
        n = R.randint(3, 6)
        each = R.randint(450, 2499)
        tot = n * each
        q = "%d Freunde kaufen zusammen ein Geschenk für %s und teilen den Preis gerecht. Wie viel zahlt jeder?" % (n, eur(tot))
        return mcq(q, eur(each), [eur(x) for x in (each + 100, each * 10, tot - n) if x != each], "%s %s %d = <b>%s</b>." % (eur(tot), GETEILT, n, eur(each)))
    (a, pa), (b, pb), (c, pc) = R.sample(SHOP, 3)
    have = (pa + pb + pc) // 1000 * 1000 + R.choice([-1000, 1000])
    if have <= 0:
        return None
    tot = pa + pb + pc
    ok = tot <= have
    q = "%s hat %s und möchte %s (%s), %s (%s) und %s (%s) kaufen. Reicht das Geld?" % (p[0], eur(have), a, eur(pa), b, eur(pb), c, eur(pc))
    ans = ("Ja, es bleiben %s übrig." % eur(have - tot)) if ok else ("Nein, es fehlen %s." % eur(tot - have))
    w = [("Nein, es fehlen %s." % eur(abs(have - tot))) if ok else ("Ja, es bleiben %s übrig." % eur(abs(have - tot))),
         "Ja, es bleiben %s übrig." % eur(abs(have - tot) + 100), "Nein, es fehlen %s." % eur(abs(have - tot) + 100)]
    return mcq(q, ans, w, "Zusammen: %s. <b>%s</b>" % (eur(tot), ans))


def main():
    seen = set()
    sets = [
        ("Euro und Cent", mix(R, seen, [(umwandeln, 20)])),
        ("Addieren und subtrahieren", mix(R, seen, [(plusminus, 20)])),
        ("Malnehmen und teilen", mix(R, seen, [(maldurch, 20)])),
        ("Preise vergleichen", mix(R, seen, [(angebot, 20)])),
        ("Sachaufgaben mit Geld", mix(R, seen, [(sache, 20)])),
    ]
    body = lesson(
        ["1 € = 100 ct. Hinter dem Komma stehen immer zwei Ziffern für die Cent: 4,05 € = 4 € 5 ct.",
         "Beim schriftlichen Rechnen steht <b>Komma unter Komma</b>. Du kannst auch alles in Cent umrechnen.",
         "Um Angebote zu vergleichen, berechnest du den Preis für <b>ein Stück</b>.",
         "Wechselgeld berechnest du mit Minus oder durch Ergänzen bis zum bezahlten Betrag."],
        [example("3 %s 12,45 €" % MAL, ["3 %s 1245 ct = 3735 ct" % MAL], "37,35 €"),
         example("Angebot A: 3 Joghurts für 1,80 €, B: 5 Joghurts für 2,75 €", ["A: 1,80 € : 3 = 0,60 €", "B: 2,75 € : 5 = 0,55 €"], "B ist günstiger")],
        [["4,05 € = 4 € 50 ct", "4,05 € = 4 € 5 ct"],
         ["Komma nicht untereinander", "Komma unter Komma, Cent unter Cent"],
         ["Das Angebot mit dem kleineren Gesamtpreis ist billiger", "Den Preis für ein Stück vergleichen"]],
        extra=table(["Münzen", "Scheine"], [["1 ct, 2 ct, 5 ct, 10 ct, 20 ct, 50 ct, 1 €, 2 €", "5 €, 10 €, 20 €, 50 €, 100 €, 200 €"]]))
    faq = [
        {"q": "Wie rechnet man mit Kommabeträgen?", "a": "Entweder in Cent umrechnen und ohne Komma rechnen oder schriftlich mit Komma unter Komma."},
        {"q": "Wie vergleicht man Angebote?", "a": "Man rechnet den Preis für ein Stück aus (Gesamtpreis geteilt durch die Anzahl) und vergleicht diese Preise."},
        {"q": "Wann lernen Kinder das Rechnen mit Geld in Kommaschreibweise?", "a": "Die Kommaschreibweise bei Geld beginnt in Klasse 3, in Klasse 4 wird schriftlich und mit größeren Beträgen gerechnet."},
        {"q": "Warum ist Geld gut zum Üben?", "a": "Weil Kinder Preise aus dem Alltag kennen und das Ergebnis sofort überprüfen können."},
    ]
    make_unit(R, "rechnen-mit-geld", "G",
              "Die Schülerinnen und Schüler rechnen mit Geldbeträgen in Kommaschreibweise in allen Grundrechenarten, vergleichen Preise und lösen Sachaufgaben zum Einkaufen (Zusammenfassung).",
              "Rechnen mit Geld: Euro und Cent mit Komma",
              "Rechnen mit Geld Klasse 4 – Kommabeträge, Arbeitsblätter mit Lösungen",
              "Rechnen mit Geld",
              "Klasse 4: Euro und Cent mit Komma, addieren, subtrahieren, malnehmen und teilen, Preise vergleichen und Sachaufgaben. 100 Übungsaufgaben mit Lösungen, kostenlos.",
              "Komma unter Komma – oder in Cent rechnen.",
              "Angebote vergleichst du mit dem Preis für ein Stück.",
              body, faq, sets, 12, grade="klasse-4")


if __name__ == "__main__":
    main()
