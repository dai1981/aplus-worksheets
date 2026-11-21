# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 5: Multiplizieren und Dividieren（Leitidee Zahl und Operation, Sek I）
  python3 tools/gen_de_mathe_k5_multiplizieren_und_dividieren.py
Fachbegriffe (Produkt, Faktor, Quotient, Dividend, Divisor), mit Stufenzahlen rechnen, schriftlich multiplizieren, schriftlich dividieren, Sachaufgaben.
Fehler: Nullen falsch gezählt, beim schriftlichen Multiplizieren Teilprodukte nicht eingerückt, Null im Quotienten vergessen, durch 0 geteilt.
"""
import random
from de_common import mcq, num, lesson, example, make_unit, mix, Kids, MAL, GETEILT, table

R = random.Random(49505)
KIDS = Kids(R)


def begriffe():
    items = [("In 24 %s 5 = 120 heißt 120 …" % MAL, "Produkt", ["Faktor", "Quotient", "Summe"]),
             ("In 24 %s 5 = 120 heißen 24 und 5 …" % MAL, "Faktoren", ["Produkte", "Divisoren", "Summanden"]),
             ("In 84 %s 7 = 12 heißt 84 …" % GETEILT, "Dividend", ["Divisor", "Quotient", "Faktor"]),
             ("In 84 %s 7 = 12 heißt 7 …" % GETEILT, "Divisor", ["Dividend", "Quotient", "Produkt"]),
             ("In 84 %s 7 = 12 heißt 12 …" % GETEILT, "Quotient", ["Produkt", "Divisor", "Differenz"]),
             ("Wie heißt das Ergebnis einer Multiplikation?", "Produkt", ["Quotient", "Summe", "Differenz"]),
             ("Wie heißt das Ergebnis einer Division?", "Quotient", ["Produkt", "Summe", "Differenz"]),
             ("Was ist 0 %s 17?" % GETEILT, "0", ["17", "1", "Das geht nicht."]),
             ("Was ist 17 %s 0?" % GETEILT, "Das geht nicht, durch 0 kann man nicht teilen.", ["0", "17", "1"]),
             ("Was ist 1 %s 538?" % MAL, "538", ["1", "539", "0"]),
             ("Was ist 0 %s 538?" % MAL, "0", ["538", "1", "Das geht nicht."])]
    kind = R.choice(["text", "text", "produkt", "quotient"])
    if kind == "text":
        q, a, w = R.choice(items)
        return mcq(q, a, w, "<b>%s</b>." % a.rstrip("."))
    if kind == "produkt":
        a, b = R.randint(12, 99), R.randint(3, 9)
        return mcq("Berechne das Produkt von %d und %d." % (a, b), num(a * b), [num(a + b), num(a * b + a), num(a * b - b)], "%d %s %d = <b>%s</b>." % (a, MAL, b, num(a * b)))
    b, q = R.randint(3, 9), R.randint(12, 99)
    return mcq("Berechne den Quotienten von %d und %d." % (b * q, b), num(q), [num(b * q - b), num(q + 1), num(b * q * b)], "%d %s %d = <b>%s</b>." % (b * q, GETEILT, b, num(q)))


def stufen():
    kind = R.choice(["mal", "mal", "durch"])
    a, b = R.randint(2, 9) * 10 ** R.randint(0, 3), R.randint(2, 9) * 10 ** R.randint(1, 3)
    if kind == "mal":
        r = a * b
        w = [r * 10, r // 10, int(str(a).rstrip("0") or "0") * int(str(b).rstrip("0")) * 10 ** (len(str(a)) - len(str(a).rstrip("0")))]
        return mcq("%s %s %s = ?" % (num(a), MAL, num(b)), num(r), [num(x) for x in w if x != r] + [num(r * 100)],
                   "Multipliziere die Ziffern ohne Nullen und hänge alle Nullen an: <b>%s</b>." % num(r))
    r = a * b
    return mcq("%s %s %s = ?" % (num(r), GETEILT, num(b)), num(a), [num(a * 10), num(a // 10) if a >= 10 else num(a * 100), num(a + 10)],
               "%s %s %s = %s, also <b>%s</b>." % (num(a), MAL, num(b), num(r), num(a)))


def schr_mal():
    a, b = R.randint(102, 999), R.randint(12, 99)
    r = a * b
    fehler = a * (b // 10) + a * (b % 10)
    return mcq("Rechne schriftlich: %d %s %d = ?" % (a, MAL, b), num(r), [num(fehler), num(r + a), num(r - 10 * a)],
               "%d %s %d = %s und %d %s %d = %s (eine Stelle eingerückt). Zusammen: <b>%s</b>." % (a, MAL, (b // 10) * 10, num(a * (b // 10) * 10), a, MAL, b % 10, num(a * (b % 10)), num(r)))


def schr_durch():
    d = R.choice([R.randint(3, 9), R.randint(11, 25)])
    q = R.randint(102, 999)
    if R.random() < 0.4 and "0" not in str(q)[1:]:
        q = int(str(q)[0] + "0" + str(q)[2])
    a = d * q
    s = str(q)
    ohne0 = int(s[0] + s[1:].replace("0", "")) if "0" in s[1:] else q + 10
    return mcq("Rechne schriftlich: %s %s %d = ?" % (num(a), GETEILT, d), num(q), [num(ohne0), num(q + 1), num(q * 10)],
               "Probe: %s %s %d = %s. Ergebnis: <b>%s</b>.%s" % (num(q), MAL, d, num(a), num(q), " Achtung: die 0 im Ergebnis nicht vergessen." if "0" in s[1:] else ""))


def sache():
    kind = R.choice(["ticket", "fahrt", "kisten", "rest", "monat"])
    if kind == "ticket":
        n, p = R.randint(120, 950), R.randint(12, 48)
        return mcq("Für ein Konzert werden %d Karten zu je %d € verkauft. Wie viel Geld wird eingenommen?" % (n, p), "%s €" % num(n * p),
                   ["%s €" % num(x) for x in (n + p, n * p + p, n * (p // 10) + n * (p % 10))], "%d %s %d € = <b>%s €</b>." % (n, MAL, p, num(n * p)))
    if kind == "fahrt":
        d, q = R.choice([12, 15, 18, 24]), R.randint(15, 60)
        return mcq("Eine Klassenfahrt kostet für %d Kinder zusammen %s €. Wie viel bezahlt jedes Kind?" % (d, num(d * q)), "%d €" % q,
                   ["%d €" % x for x in (d * q - d, q + 10, q * 10)], "%s € %s %d = <b>%d €</b>." % (num(d * q), GETEILT, d, q))
    if kind == "kisten":
        k, n = R.choice([6, 12, 20, 24]), R.randint(25, 200)
        return mcq("In eine Kiste passen %d Flaschen. Wie viele Flaschen sind in %d vollen Kisten?" % (k, n), num(k * n), [num(k + n), num(k * n + k), num(k * n - n)],
                   "%d %s %d = <b>%s</b>." % (n, MAL, k, num(k * n)))
    if kind == "rest":
        k = R.choice([25, 30, 32, 45, 50])
        n = R.randint(100, 900)
        if n % k == 0:
            return None
        q, r = divmod(n, k)
        return mcq("%d Kinder fahren mit Bussen. In jeden Bus passen %d Kinder. Wie viele Busse braucht man mindestens?" % (n, k), "%d Busse" % (q + 1),
                   ["%d Busse" % x for x in (q, q + 2, q - 1)], "%d %s %d = %d Rest %d. Für den Rest braucht man noch einen Bus: <b>%d Busse</b>." % (n, GETEILT, k, q, r, q + 1))
    m = R.randint(15, 45)
    p = KIDS.next()
    return mcq("%s spart jeden Monat %d €. Wie viel Geld hat %s nach einem Jahr gespart?" % (p[0], m, p[1]), "%d €" % (12 * m),
               ["%d €" % x for x in (10 * m, 12 + m, 52 * m)], "Ein Jahr hat 12 Monate: 12 %s %d € = <b>%d €</b>." % (MAL, m, 12 * m))


def main():
    seen = set()
    sets = [
        ("Fachbegriffe", mix(R, seen, [(begriffe, 20)])),
        ("Mit Stufenzahlen rechnen", mix(R, seen, [(stufen, 20)])),
        ("Schriftlich multiplizieren", mix(R, seen, [(schr_mal, 20)])),
        ("Schriftlich dividieren", mix(R, seen, [(schr_durch, 20)])),
        ("Sachaufgaben", mix(R, seen, [(sache, 20)])),
    ]
    body = lesson(
        ["<b>Multiplikation</b>: Faktor %s Faktor = Produkt. <b>Division</b>: Dividend %s Divisor = Quotient." % (MAL, GETEILT),
         "Bei Zahlen mit Nullen rechnest du erst ohne Nullen und hängst dann alle Nullen an: 300 %s 40 = 12 000." % MAL,
         "Beim schriftlichen Multiplizieren rückst du jedes Teilprodukt eine Stelle nach links.",
         "Durch 0 kann man nicht teilen. 0 geteilt durch eine Zahl ist 0."],
        [example("234 %s 56" % MAL, ["234 %s 50 = 11 700" % MAL, "234 %s 6 = 1404" % MAL, "11 700 + 1404"], "13 104"),
         example("6120 %s 12" % GETEILT, ["61 : 12 = 5 Rest 1", "12 : 12 = 1", "0 : 12 = 0"], "510")],
        [["300 %s 40 = 1200" % MAL, "Alle Nullen zählen: 12 000"],
         ["Teilprodukt nicht einrücken", "Jede neue Zeile eine Stelle weiter links"],
         ["6120 %s 12 = 51" % GETEILT, "Die 0 im Ergebnis nicht vergessen: 510"]],
        extra=table(["Rechenart", "Name der Zahlen", "Ergebnis"], [["Multiplikation", "Faktor %s Faktor" % MAL, "Produkt"], ["Division", "Dividend %s Divisor" % GETEILT, "Quotient"]]))
    faq = [
        {"q": "Warum kann man nicht durch 0 teilen?", "a": "Weil es keine Zahl gibt, die mit 0 multipliziert z. B. 17 ergibt. Deshalb ist 17 : 0 nicht definiert."},
        {"q": "Wie multipliziert man schriftlich mit zweistelligen Zahlen?", "a": "Man multipliziert nacheinander mit jeder Ziffer des zweiten Faktors, schreibt die Teilprodukte stellengerecht eingerückt untereinander und addiert sie."},
        {"q": "Wie prüft man eine Division?", "a": "Mit der Umkehraufgabe: Quotient mal Divisor muss den Dividenden ergeben (plus Rest)."},
        {"q": "Was sind Stufenzahlen?", "a": "Zahlen wie 10, 100, 1000. Mit ihnen rechnet man besonders leicht, weil man nur Nullen anhängt oder wegnimmt."},
    ]
    make_unit(R, "multiplizieren-und-dividieren", "Z",
              "Die Schülerinnen und Schüler multiplizieren und dividieren natürliche Zahlen im Kopf und schriftlich, verwenden die Fachbegriffe, rechnen mit Stufenzahlen und lösen Sachaufgaben, auch mit Rest (Zusammenfassung).",
              "Multiplizieren und Dividieren",
              "Multiplizieren und Dividieren Klasse 5 – Arbeitsblätter mit Lösungen",
              "Multiplizieren und Dividieren",
              "Multiplizieren und Dividieren für Klasse 5: Produkt und Quotient, Stufenzahlen, schriftlich multiplizieren und dividieren und Sachaufgaben. 100 Übungsaufgaben mit Lösungen, kostenlos.",
              "Faktor · Faktor = Produkt",
              "Dividend : Divisor = Quotient",
              body, faq, sets, 5, grade="klasse-5")


if __name__ == "__main__":
    main()
