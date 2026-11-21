# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 3: Multiplizieren und Dividieren bis 1000（Leitidee Zahl und Operation）
  python3 tools/gen_de_mathe_k3_multiplizieren_und_dividieren.py
Mal und geteilt mit Zehnerzahlen (3 · 40, 240 : 6), halbschriftlich multiplizieren (6 · 47) und dividieren (96 : 6), Sachaufgaben.
Fehler: Null vergessen (3 · 40 → 12) oder doppelt (→ 1200), Teilprodukt vergessen (4 · 23 → 83), Zehner und Einer einzeln geteilt ohne Rest-Übertrag.
"""
import random
from de_common import mcq, num, lesson, example, make_unit, mix, Kids, MAL, GETEILT

R = random.Random(49008)
KIDS = Kids(R)


def s1_mal():
    a = R.randint(2, 9)
    b = R.randint(2, 9) * 10
    if a * b > 1000:
        return None
    if R.random() < 0.4:
        a, b = b, a
    r = a * b
    da, db = (a if a < 10 else a // 10), (b if b < 10 else b // 10)
    small = da * db
    w = [small, r * 10, r + max(a, b), r - max(a, b), a + b]
    return mcq("%s %s %s = ?" % (num(a), MAL, num(b)), num(r), [num(x) for x in w if x > 0 and x != r],
               "%d %s %d = %d, dann die Null anhängen: <b>%s</b>." % (da, MAL, db, small, num(r)))


def s1_hundert():
    m = R.randint(1, 5)
    a = R.randint(2, 10 // m)
    b = 100 * m
    r = a * b
    if R.random() < 0.4:
        a, b = b, a
    w = [r // 10, r * 10, r + 100, a + b]
    return mcq("%s %s %s = ?" % (num(a), MAL, num(b)), num(r), [num(x) for x in w if x > 0 and x != r],
               "%d %s %d = %d, dann zwei Nullen anhängen: <b>%s</b>." % (min(a, b), MAL, max(a, b) // 100, r // 100, num(r)))


def s2_geteilt():
    a = R.randint(2, 9)
    b = R.randint(2, 9)
    kind = R.choice(["e", "z"])
    t = a * b * 10
    if kind == "e":
        q, r = "%s %s %d = ?" % (num(t), GETEILT, a), b * 10
        w = [b, b * 100, r + 10, r - 10]
        e = "%d %s %d = %d, also %s %s %d = <b>%s</b>." % (a * b, GETEILT, a, b, num(t), GETEILT, a, num(r))
    else:
        q, r = "%s %s %d = ?" % (num(t), GETEILT, a * 10), b
        w = [b * 10, b + 1, b - 1, a]
        e = "%d Zehner %s %d Zehner = <b>%d</b>." % (a * b, GETEILT, a, b)
    return mcq(q, num(r), [num(x) for x in w if x > 0 and x != r], e)


def s3_mal():
    a = R.randint(3, 9)
    b = R.randint(12, 99)
    if b % 10 == 0 or a * b > 1000:
        return None
    r = a * b
    z, e = b // 10 * 10, b % 10
    w = [a * z + e, a * (b // 10) + a * e, a * z + a * e + 10 if a * e >= 10 else r + 10, r + a, r - 10]
    return mcq("Rechne halbschriftlich: %d %s %d" % (a, MAL, b), num(r), [num(x) for x in w if x > 0 and x != r],
               "Zerlege %d in %d und %d: %d %s %d = %d, %d %s %d = %d. Zusammen <b>%s</b>." % (b, z, e, a, MAL, z, a * z, a, MAL, e, a * e, num(r)))


def s4_geteilt():
    a = R.randint(2, 9)
    q = R.randint(11, 99)
    t = a * q
    if t > 999 or t < 40:
        return None
    big = (t // a // 10) * 10 * a
    rest = t - big
    if rest == 0 or big == 0:
        return None
    zq, eq = big // a, rest // a
    w = [int(str(t // 10 // a) + str(t % 10 // a)) if t % 10 // a else None, q + 1, q - 1, q + 10]
    return mcq("Rechne halbschriftlich: %s %s %d" % (num(t), GETEILT, a), num(q), [num(x) for x in w if x and x > 0 and x != q],
               "Zerlege %s in %s und %d: %s %s %d = %d, %d %s %d = %d. Zusammen <b>%d</b>. Probe: %d %s %d = %s."
               % (num(t), num(big), rest, num(big), GETEILT, a, zq, rest, GETEILT, a, eq, q, q, MAL, a, num(t)))


def s5_sache():
    kind = R.choice(["preis", "preis", "fahrt", "kiste", "teilen"])
    p = KIDS.next()
    if kind == "preis":
        n = R.randint(3, 9)
        c = R.randint(12, 99)
        if n * c > 1000 or c % 10 == 0:
            return None
        thing = R.choice(["ein Fußball", "ein Puzzle", "eine Jacke", "ein Rucksack"])
        plural = {"ein Fußball": "Fußbälle", "ein Puzzle": "Puzzles", "eine Jacke": "Jacken", "ein Rucksack": "Rucksäcke"}[thing]
        q = "%s kostet %d €. Die Schule kauft %d %s. Wie viel kosten sie zusammen?" % (thing[0].upper() + thing[1:], c, n, plural)
        r = n * c
        w = [n * (c // 10 * 10) + c % 10, n + c, r + 10, r - n]
        return mcq(q, "%s €" % num(r), ["%s €" % num(x) for x in w if x > 0 and x != r],
                   "%d %s %d = %d %s %d + %d %s %d = %d + %d = <b>%s €</b>."
                   % (n, MAL, c, n, MAL, c // 10 * 10, n, MAL, c % 10, n * (c // 10 * 10), n * (c % 10), num(r)))
    if kind == "fahrt":
        k = R.choice([20, 30, 40, 50, 60, 70, 80, 90])
        n = R.randint(3, 9)
        if n * k > 1000:
            return None
        q = "Ein Bus fährt jeden Tag %d km. Wie viele Kilometer fährt er in %d Tagen?" % (k, n)
        r = n * k
        w = [n * k // 10, n * k * 10 if n * k * 10 < 10000 else r + 100, r + k, n + k]
        return mcq(q, "%s km" % num(r), ["%s km" % num(x) for x in w if x > 0 and x != r],
                   "%d %s %d = <b>%s km</b>." % (n, MAL, k, num(r)))
    if kind == "kiste":
        k = R.randint(12, 48)
        n = R.randint(3, 8)
        if n * k > 1000:
            return None
        q = "In einer Kiste sind %d Flaschen. Wie viele Flaschen sind in %d Kisten?" % (k, n)
        r = n * k
        w = [n * (k // 10 * 10) + k % 10, n + k, r + 10, r - 10]
        return mcq(q, "%s Flaschen" % num(r), ["%s Flaschen" % num(x) for x in w if x > 0 and x != r],
                   "%d %s %d = <b>%s Flaschen</b>." % (n, MAL, k, num(r)))
    a = R.randint(3, 8)
    q2 = R.randint(12, 40)
    t = a * q2
    q = "%s verteilt %s Sammelkarten gleichmäßig an %d Freunde. Wie viele Karten bekommt jeder?" % (p[0], num(t), a)
    w = [q2 + 1, q2 - 1, t - a, q2 + 10]
    return mcq(q, "%d Karten" % q2, ["%d Karten" % x for x in w if x > 0 and x != q2],
               "%s %s %d = <b>%d</b>. Probe: %d %s %d = %s." % (num(t), GETEILT, a, q2, q2, MAL, a, num(t)))


def main():
    seen = set()
    sets = [
        ("Mal mit Zehner- und Hunderterzahlen", mix(R, seen, [(s1_mal, 15), (s1_hundert, 5)])),
        ("Geteilt mit Zehnerzahlen", mix(R, seen, [(s2_geteilt, 20)])),
        ("Halbschriftlich multiplizieren", mix(R, seen, [(s3_mal, 20)])),
        ("Halbschriftlich dividieren", mix(R, seen, [(s4_geteilt, 20)])),
        ("Sachaufgaben", mix(R, seen, [(s5_sache, 20)])),
    ]
    body = lesson(
        ["Mit Zehnerzahlen rechnest du wie im Einmaleins und hängst die Null an: 3 %s 4 = 12, also 3 %s 40 = 120." % (MAL, MAL),
         "Beim Teilen ist es genauso: 24 %s 6 = 4, also 240 %s 6 = 40." % (GETEILT, GETEILT),
         "<b>Halbschriftlich multiplizieren</b>: Zerlege die größere Zahl in Zehner und Einer und rechne zwei leichte Aufgaben.",
         "<b>Halbschriftlich dividieren</b>: Zerlege die Zahl so, dass sich beide Teile gut teilen lassen."],
        [example("6 %s 47" % MAL, ["6 %s 40 = 240" % MAL, "6 %s 7 = 42" % MAL, "240 + 42 = 282"], "282"),
         example("96 %s 6" % GETEILT, ["96 = 60 + 36", "60 %s 6 = 10, 36 %s 6 = 6" % (GETEILT, GETEILT), "10 + 6 = 16"], "16")],
        [["3 %s 40 = 12" % MAL, "Die Null gehört dazu: 120"],
         ["4 %s 23 = 83 (nur die Zehner mal genommen)" % MAL, "Beide Teile mal 4: 80 + 12 = 92"],
         ["96 %s 6: 9 %s 6 und 6 %s 6 einzeln" % (GETEILT, GETEILT, GETEILT), "So zerlegen, dass es aufgeht: 60 + 36"]])
    faq = [
        {"q": "Was ist halbschriftliches Multiplizieren?", "a": "Man zerlegt eine Zahl in Zehner und Einer, multipliziert beide Teile und addiert die Ergebnisse. Die Zwischenschritte schreibt man auf."},
        {"q": "Muss man schriftlich multiplizieren können?", "a": "Die schriftliche Multiplikation kommt meist erst in Klasse 4. In Klasse 3 rechnet man im Kopf und halbschriftlich."},
        {"q": "Warum hängt man eine Null an?", "a": "3 %s 40 heißt 3-mal 4 Zehner, also 12 Zehner. 12 Zehner sind 120." % MAL},
        {"q": "Wie prüft man eine Geteiltaufgabe?", "a": "Mit der Malaufgabe: 96 %s 6 = 16, denn 16 %s 6 = 96." % (GETEILT, MAL)},
    ]
    make_unit(R, "multiplizieren-und-dividieren", "Z",
              "Die Schülerinnen und Schüler multiplizieren und dividieren im Zahlenraum bis 1000 mit Zehnerzahlen sowie halbschriftlich und nutzen dabei das Verteilungsgesetz (Zusammenfassung).",
              "Multiplizieren und Dividieren bis 1000",
              "Multiplizieren und Dividieren Klasse 3 – halbschriftlich, Arbeitsblätter mit Lösungen",
              "Mal und geteilt bis 1000",
              "Mathe Klasse 3: mal und geteilt mit Zehnerzahlen, halbschriftlich multiplizieren und dividieren, Sachaufgaben. 100 Übungsaufgaben mit Lösungen und Arbeitsblatt zum Ausdrucken, kostenlos.",
              "Zerlegen macht schwere Aufgaben leicht.",
              "6 · 47 = 6 · 40 + 6 · 7 = 240 + 42 = 282.",
              body, faq, sets, 8)


if __name__ == "__main__":
    main()
