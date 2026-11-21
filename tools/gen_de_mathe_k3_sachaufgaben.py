# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 3: Sachaufgaben（Leitidee Zahl und Operation / Sachrechnen）
  python3 tools/gen_de_mathe_k3_sachaufgaben.py
Welche Rechnung passt?, einfache und zweischrittige Sachaufgaben, Antwortsätze, Sachaufgaben mit Tabellen.
Fehler: falsche Rechenart (dazu ↔ weg), nur einen Schritt gerechnet, Zahl aus dem Text, die gar nicht gebraucht wird.
"""
import random
from de_common import mcq, num, lesson, example, make_unit, mix, Kids, MAL, GETEILT, table, eur

R = random.Random(49010)
KIDS = Kids(R)


def ops_story():
    p = KIDS.next()
    kind = R.choice(["plus", "minus", "mal", "geteilt"])
    if kind == "plus":
        a, b = R.randint(120, 480), R.randint(30, 290)
        q = "%s hat %s Sammelkarten. Zum Geburtstag bekommt %s %s dazu. Wie viele Karten hat %s jetzt?" % (p[0], num(a), p[1], num(b), p[1])
        r, ans = a + b, "%s + %s" % (num(a), num(b))
        w = ["%s − %s" % (num(a), num(b)), "%s %s %s" % (num(a), MAL, num(b)), "%s + %s + %s" % (num(a), num(b), num(b))]
    elif kind == "minus":
        a, b = R.randint(200, 700), R.randint(30, 190)
        q = "Im Kino sind %s Plätze. %s Plätze sind besetzt. Wie viele Plätze sind noch frei?" % (num(a), num(b))
        r, ans = a - b, "%s − %s" % (num(a), num(b))
        w = ["%s + %s" % (num(a), num(b)), "%s − %s" % (num(b), num(a)), "%s %s %s" % (num(a), GETEILT, num(b))]
    elif kind == "mal":
        a, b = R.randint(3, 9), R.randint(4, 12)
        q = "Ein Kind bekommt jeden Tag %d Gummibärchen. Wie viele Gummibärchen sind das in %d Tagen?" % (a, b) if R.random() < 0.5 else \
            "In einem Regal stehen %d Reihen mit je %d Büchern. Wie viele Bücher sind es?" % (b, a)
        r, ans = a * b, "%d %s %d" % (b, MAL, a)
        w = ["%d + %d" % (b, a), "%d %s %d" % (b * a, GETEILT, a), "%d − %d" % (max(a, b), min(a, b))]
    else:
        a, b = R.randint(3, 9), R.randint(3, 9)
        t = a * b
        q = "%d Kinder bilden Gruppen zu je %d. Wie viele Gruppen gibt es?" % (t, a)
        r, ans = b, "%d %s %d" % (t, GETEILT, a)
        w = ["%d %s %d" % (t, MAL, a), "%d − %d" % (t, a), "%d + %d" % (t, a)]
    return mcq(q + " Welche Rechnung passt?", ans, w, "Passend ist <b>%s</b> = %s." % (ans, num(r)))


def one_step():
    p, p2 = KIDS.two()
    kind = R.choice(["preis", "weg", "tiere", "kuchen", "rest"])
    if kind == "preis":
        a, b = R.randint(12, 48) * 10, R.randint(3, 9) * 10
        q = "Ein Fahrrad kostet %s €. Im Angebot ist es %d € billiger. Was kostet es jetzt?" % (num(a), b)
        r, u = a - b, "€"
        w = [a + b, a - b + 10, b]
        e = "Billiger heißt minus: %s − %d = <b>%s €</b>." % (num(a), b, num(r))
    elif kind == "weg":
        a = R.randint(150, 450)
        q = "%s läuft jeden Tag %d m zur Schule und %d m zurück. Wie viele Meter sind das an einem Tag?" % (p[0], a, a)
        r, u = 2 * a, "m"
        w = [a, a + 2, 4 * a if 4 * a <= 1000 else 3 * a]
        e = "Hin und zurück: %d m + %d m = <b>%d m</b>." % (a, a, r)
    elif kind == "tiere":
        a, b = R.randint(3, 9), R.choice([2, 4])
        tier = "Hühner" if b == 2 else "Kühe"
        q = "Auf dem Bauernhof stehen %d %s. Wie viele Beine haben sie zusammen?" % (a, tier)
        r, u = a * b, "Beine"
        w = [a + b, a * (b + 1), a * b + b]
        e = "Jedes Tier hat %d Beine: %d %s %d = <b>%d Beine</b>." % (b, a, MAL, b, r)
    elif kind == "kuchen":
        k = R.choice([6, 8, 12])
        n = R.randint(2, 6)
        q = "Ein Blech Kuchen wird in %d Stücke geschnitten. Mama backt %d Bleche. Wie viele Stücke gibt es?" % (k, n)
        r, u = k * n, "Stücke"
        w = [k + n, k * (n - 1), k * n + k]
        e = "%d Bleche mit je %d Stücken: %d %s %d = <b>%d Stücke</b>." % (n, k, n, MAL, k, r)
    else:
        a = R.randint(20, 50)
        b = R.randint(5, a - 5)
        q = "%s hat %d €. %s kauft ein Buch für %d €. Wie viel Geld hat %s noch?" % (p[0], a, p[1].capitalize(), b, p[1])
        r, u = a - b, "€"
        w = [a + b, a - b - 1, b]
        e = "Ausgeben heißt minus: %d − %d = <b>%d €</b>." % (a, b, r)
    return mcq(q, "%s %s" % (num(r), u), ["%s %s" % (num(x), u) for x in w if x > 0 and x != r], e)


def two_step():
    p = KIDS.next()
    kind = R.choice(["einkauf", "bus", "taschengeld", "eintritt", "regal"])
    if kind == "einkauf":
        n, c, have = R.randint(2, 5), R.randint(3, 9), R.choice([20, 50])
        if n * c >= have:
            return None
        q = "%s kauft %d Malblöcke zu je %d € und bezahlt mit einem %d-€-Schein. Wie viel Wechselgeld bekommt %s?" % (p[0], n, c, have, p[1])
        r, u = have - n * c, "€"
        w = [n * c, have - c, have - n - c]
        e = "Erst: %d %s %d = %d €. Dann: %d − %d = <b>%d €</b>." % (n, MAL, c, n * c, have, n * c, r)
    elif kind == "bus":
        a, b, c = R.randint(20, 45), R.randint(3, 15), R.randint(3, 15)
        q = "In einem Bus sitzen %d Kinder. An der ersten Haltestelle steigen %d aus, an der zweiten %d ein. Wie viele Kinder sitzen jetzt im Bus?" % (a, b, c)
        r, u = a - b + c, "Kinder"
        w = [a + b + c, a - b - c, a - b]
        e = "Erst: %d − %d = %d. Dann: %d + %d = <b>%d</b>." % (a, b, a - b, a - b, c, r)
    elif kind == "taschengeld":
        k = R.randint(3, 8)
        n = R.randint(4, 10)
        spent = R.randint(5, k * n - 5)
        q = "%s bekommt jede Woche %d € Taschengeld. Nach %d Wochen kauft %s ein Spiel für %d €. Wie viel Geld bleibt übrig?" % (p[0], k, n, p[1], spent)
        r, u = k * n - spent, "€"
        w = [k * n, k * n + spent, k + n - spent if k + n > spent else spent - k]
        e = "Erst: %d %s %d = %d €. Dann: %d − %d = <b>%d €</b>." % (n, MAL, k, k * n, k * n, spent, r)
    elif kind == "eintritt":
        e1, k1 = R.choice([8, 9, 10, 12]), R.choice([4, 5, 6])
        ne, nk = R.choice([1, 2]), R.randint(2, 4)
        q = "Im Zoo kostet der Eintritt für Erwachsene %d € und für Kinder %d €. Familie Klein geht mit %s und %d Kindern hin. Wie viel zahlt sie?" % (
            e1, k1, "einem Erwachsenen" if ne == 1 else "zwei Erwachsenen", nk)
        r, u = ne * e1 + nk * k1, "€"
        w = [e1 + k1, (ne + nk) * e1, ne * e1 + k1]
        e = "Erwachsene: %d %s %d = %d €. Kinder: %d %s %d = %d €. Zusammen <b>%d €</b>." % (ne, MAL, e1, ne * e1, nk, MAL, k1, nk * k1, r)
    else:
        rows, per, extra = R.randint(3, 6), R.randint(6, 12), R.randint(3, 15)
        q = "In einem Regal stehen %d Reihen mit je %d Büchern. Daneben liegen noch %d Bücher. Wie viele Bücher sind es insgesamt?" % (rows, per, extra)
        r, u = rows * per + extra, "Bücher"
        w = [rows * per, rows + per + extra, rows * (per + extra)]
        e = "Erst: %d %s %d = %d. Dann: %d + %d = <b>%d</b>." % (rows, MAL, per, rows * per, rows * per, extra, r)
    return mcq(q, "%s %s" % (num(r), u), ["%s %s" % (num(x), u) for x in w if x > 0 and x != r], e)


def antwort():
    p = KIDS.next()
    a, b = R.randint(3, 9), R.randint(3, 9)
    kind = R.choice(["mal", "geteilt", "minus"])
    if kind == "mal":
        q = "%s kauft %d Packungen mit je %d Stiften. Wie viele Stifte hat %s? Welcher Antwortsatz passt?" % (p[0], a, b, p[1])
        ans = "%s hat %d Stifte." % (p[0], a * b)
        w = ["%s hat %d Packungen." % (p[0], a), "%s hat %d Stifte." % (p[0], a + b), "Eine Packung hat %d Stifte." % b]
    elif kind == "geteilt":
        t = a * b
        q = "%d Muffins werden auf %d Teller verteilt, auf jeden gleich viele. Wie viele Muffins liegen auf einem Teller? Welcher Antwortsatz passt?" % (t, a)
        ans = "Auf einem Teller liegen %d Muffins." % b
        w = ["Es sind %d Teller." % a, "Auf einem Teller liegen %d Muffins." % (t - a), "Es gibt %d Muffins." % t]
    else:
        big = R.randint(50, 99)
        small = R.randint(10, big - 10)
        q = "Ein Kirchturm ist %d m hoch, ein Wohnhaus %d m. Wie viel höher ist der Kirchturm? Welcher Antwortsatz passt?" % (big, small)
        ans = "Der Kirchturm ist %d m höher." % (big - small)
        w = ["Der Kirchturm ist %d m hoch." % big, "Der Kirchturm ist %d m höher." % (big + small), "Das Wohnhaus ist %d m höher." % (big - small)]
    return mcq(q, ans, w, "Der Antwortsatz beantwortet genau die Frage: <b>%s</b>" % ans)


PREISE = [("Brötchen", 40), ("Brezel", 90), ("Croissant", 120), ("Muffin", 150), ("Kakao", 180), ("Apfelsaft", 130)]


def tabelle():
    items = R.sample(PREISE, 4)
    tab = table(["Ware", "Preis"], [[n, eur(c)] for n, c in items])
    kind = R.choice(["zwei", "mehr", "unterschied"])
    p = KIDS.next()
    if kind == "zwei":
        (n1, c1), (n2, c2) = R.sample(items, 2)
        q = tab + "%s kauft %s und %s. Wie viel muss %s bezahlen?" % (p[0], art(n1), art(n2), p[1])
        r = c1 + c2
        w = [abs(c1 - c2), r + 10, r - 10 if r > 10 else r + 20, c1 + c2 + 100]
    elif kind == "mehr":
        n1, c1 = R.choice(items)
        k = R.randint(2, 5)
        q = tab + "%s kauft %d %s. Wie viel kostet das?" % (p[0], k, PL[n1])
        r = k * c1
        w = [c1 + k * 10, (k - 1) * c1, k * c1 + c1]
    else:
        (n1, c1), (n2, c2) = R.sample(items, 2)
        if c1 == c2:
            return None
        if c1 < c2:
            (n1, c1), (n2, c2) = (n2, c2), (n1, c1)
        q = tab + "Um wie viel ist %s teurer als %s?" % (art(n1, True), art(n2, True))
        r = c1 - c2
        w = [c1 + c2, r + 10, c1]
    return mcq(q, eur(r), [eur(x) for x in w if x > 0 and x != r], "Aus der Tabelle ablesen und rechnen: <b>%s</b>." % eur(r))


PL = {"Brötchen": "Brötchen", "Brezel": "Brezeln", "Croissant": "Croissants", "Muffin": "Muffins", "Kakao": "Becher Kakao", "Apfelsaft": "Flaschen Apfelsaft"}
ART = {"Brötchen": ("ein", "das"), "Brezel": ("eine", "die"), "Croissant": ("ein", "das"), "Muffin": ("einen", "der"),
       "Kakao": ("einen", "der"), "Apfelsaft": ("einen", "der")}


def art(n, best=False):
    return ("%s %s" % (ART[n][1], n)) if best else ("%s %s" % (ART[n][0], n))


def main():
    seen = set()
    sets = [
        ("Welche Rechnung passt?", mix(R, seen, [(ops_story, 20)])),
        ("Sachaufgaben mit einem Schritt", mix(R, seen, [(one_step, 20)])),
        ("Sachaufgaben mit zwei Schritten", mix(R, seen, [(two_step, 20)])),
        ("Der passende Antwortsatz", mix(R, seen, [(antwort, 20)])),
        ("Sachaufgaben mit Tabellen", mix(R, seen, [(tabelle, 20)])),
    ]
    body = lesson(
        ["Lies die Aufgabe genau. Was ist gegeben? Was ist <b>gefragt</b>?",
         "Überlege die Rechenart: dazu → plus, weg → minus, gleich große Gruppen → mal, gleich verteilen → geteilt.",
         "Manche Aufgaben brauchen <b>zwei Schritte</b>. Rechne erst das eine, dann das andere.",
         "Schreibe <b>F</b>rage, <b>R</b>echnung und <b>A</b>ntwort auf. Der Antwortsatz beantwortet genau die Frage."],
        [example("Lena kauft 3 Hefte zu je 2 € und zahlt mit 10 €. Wie viel Wechselgeld bekommt sie?",
                 ["Schritt 1: 3 %s 2 € = 6 €" % MAL, "Schritt 2: 10 € − 6 € = 4 €", "Antwort: Lena bekommt 4 € zurück."], "4 €")],
        [["Nur den ersten Schritt rechnen (6 €)", "Bis zur Frage weiterrechnen: 10 € − 6 € = 4 €"],
         ["„Aussteigen“ mit plus rechnen", "Aussteigen heißt weniger: minus"],
         ["Antwortsatz passt nicht zur Frage", "Die Frage im Antwortsatz wieder aufnehmen"]])
    faq = [
        {"q": "Warum fallen Kindern Sachaufgaben schwer?", "a": "Sie müssen den Text verstehen, die wichtigen Zahlen finden und die passende Rechenart wählen. Das übt man am besten mit kurzen Aufgaben und einer festen Reihenfolge: Frage, Rechnung, Antwort."},
        {"q": "Was bedeutet F, R, A?", "a": "Frage, Rechnung, Antwort. So schreiben viele Klassen ihre Lösungen zu Sachaufgaben auf."},
        {"q": "Wie hilft eine Skizze?", "a": "Eine kleine Zeichnung oder Tabelle macht sichtbar, was passiert, zum Beispiel wer einsteigt und wer aussteigt."},
        {"q": "Wie viele Schritte haben Sachaufgaben in Klasse 3?", "a": "Meist einen oder zwei Rechenschritte, oft mit Geld, Längen oder Zeit."},
    ]
    make_unit(R, "sachaufgaben", "Z",
              "Die Schülerinnen und Schüler lösen einfache und mehrschrittige Sachaufgaben, wählen passende Rechenoperationen, entnehmen Informationen aus Texten und Tabellen und formulieren Antworten (Zusammenfassung).",
              "Sachaufgaben: Frage, Rechnung, Antwort",
              "Sachaufgaben Klasse 3 – Arbeitsblätter mit Lösungen",
              "Sachaufgaben",
              "Sachaufgaben für Klasse 3: passende Rechnung finden, Aufgaben mit einem und zwei Schritten, Antwortsätze und Tabellen. 100 Übungsaufgaben mit Lösungen, kostenlos.",
              "Frage, Rechnung, Antwort.",
              "Erst verstehen, was gefragt ist, dann die Rechenart wählen.",
              body, faq, sets, 10)


if __name__ == "__main__":
    main()
