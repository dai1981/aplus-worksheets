# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 6: Sachaufgaben mit Brüchen und Dezimalzahlen（Leitidee Zahl und Operation, Sek I）
  python3 tools/gen_de_mathe_k6_sachaufgaben_mit_bruechen_und_dezimalzahlen.py
Anteile von Mengen, Rest berechnen, Rezepte umrechnen, Einkaufen mit Dezimalzahlen, Durchschnittspreise, Zeit als Bruch, Mehrschrittaufgaben.
Fehler: Anteil vom Rest statt vom Ganzen, Bruch und Dezimalzahl gemischt falsch verrechnet, einen Rechenschritt vergessen.
"""
import random
from fractions import Fraction as Fr
from de_common import lesson, example, make_unit, mix, Kids, fr, MAL, table
from de_k6 import bh, dz, endlich, mcq

R = random.Random(49619)
KIDS = Kids(R)
G = ":"


def eur(v):
    v = Fr(v)
    c = int(v * 100 + Fr(1, 2))
    return "%d,%02d €" % (c // 100, c % 100)


def anteil():
    p, er = KIDS.next()
    kind = R.choice(["rest", "rest2", "vom_rest", "teil"])
    if kind == "rest":
        z, n = R.choice([(1, 4), (2, 5), (1, 3), (3, 8), (2, 3), (3, 4), (1, 6)])
        t = n * R.randint(3, 12)
        a = t * z // n
        return mcq("Eine Klasse sammelt %d Flaschen. %s davon sind aus Glas, der Rest aus Plastik. Wie viele Flaschen sind aus Plastik?" % (t, fr(z, n)), str(t - a), [str(a), str(t - z), str(t // n)],
                   "Glas: %s von %d = %d. Plastik: %d − %d = <b>%d</b>." % (fr(z, n), t, a, t, a, t - a))
    if kind == "rest2":
        (z1, n1), (z2, n2) = R.sample([(1, 2), (1, 4), (1, 3), (1, 6), (1, 5), (1, 10), (3, 10)], 2)
        x, y = Fr(z1, n1), Fr(z2, n2)
        if x + y >= 1:
            return None
        t = 60 * R.randint(1, 4)
        if (t * (1 - x - y)).denominator != 1:
            return None
        r = t * (1 - x - y)
        return mcq("%s hat %d € gespart. %s gibt %s für ein Spiel und %s für Kleidung aus. Wie viel Euro bleiben übrig?" % (p, t, er.capitalize(), fr(z1, n1), fr(z2, n2)), "%d €" % r, ["%d €" % v for v in (t * (x + y), t - t * x, t * (1 - x) * (1 - y) if (t * (1 - x) * (1 - y)).denominator == 1 else r + 5)],
                   "Ausgegeben: %s + %s = %s. Übrig: %s von %d € = <b>%d €</b>." % (fr(z1, n1), fr(z2, n2), bh(x + y), bh(1 - x - y), t, r))
    if kind == "vom_rest":
        t = R.choice([24, 36, 48, 60, 72])
        z1, n1 = R.choice([(1, 2), (1, 3), (1, 4), (2, 3)])
        z2, n2 = R.choice([(1, 2), (1, 3), (1, 4)])
        r1 = t - t * z1 // n1
        if t * z1 % n1 or r1 * z2 % n2:
            return None
        b = r1 * z2 // n2
        return mcq("Von %d Bonbons isst %s %s. Vom Rest bekommt die Schwester %s. Wie viele Bonbons bekommt die Schwester?" % (t, p, fr(z1, n1), fr(z2, n2)), str(b), [str(t * z2 // n2), str(r1), str(r1 - b)],
                   "Rest: %d − %d = %d. %s von %d = <b>%d</b>." % (t, t * z1 // n1, r1, fr(z2, n2), r1, b))
    km = Fr(R.randint(6, 24), 2)
    z, n = R.choice([(1, 3), (2, 3), (1, 4), (3, 4)])
    v = km * Fr(z, n)
    if not endlich(v):
        return None
    return mcq("Eine Wanderung ist %s km lang. Nach der Pause sind %s geschafft. Wie viele Kilometer sind das?" % (dz(km), fr(z, n)), "%s km" % dz(v), ["%s km" % dz(x) for x in (km - v, km / n, v + 1)],
               "%s von %s km = %s %s %s = <b>%s km</b>." % (fr(z, n), dz(km), dz(km), MAL, fr(z, n), dz(v)))


def einkauf():
    p, er = KIDS.next()
    kind = R.choice(["mehr", "wechsel", "gewicht", "vergleich"])
    if kind == "mehr":
        a, pa = R.randint(2, 5), Fr(R.randint(45, 250), 100)
        b, pb = Fr(R.choice([5, 10, 15, 20, 25]), 10), Fr(R.randint(99, 399), 100)
        t = a * pa + b * pb
        if (b * pb * 100).denominator != 1:
            return None
        return mcq("%s kauft %d Brezeln zu je %s und %s kg Äpfel zu %s pro kg. Wie viel kostet alles?" % (p, a, eur(pa), dz(b), eur(pb)), eur(t), [eur(pa + b * pb), eur(a * pa + pb), eur(t + 1)],
                   "%d %s %s = %s, %s %s %s = %s. Zusammen <b>%s</b>." % (a, MAL, eur(pa), eur(a * pa), dz(b), MAL, eur(pb), eur(b * pb), eur(t)))
    if kind == "wechsel":
        t = Fr(R.randint(320, 1890), 100)
        s = 20 if t < 20 else 50
        return mcq("Der Einkauf kostet %s. %s bezahlt mit %d €. Wie viel Rückgeld gibt es?" % (eur(t), p, s), eur(s - t), [eur(s - t + Fr(1, 10)), eur(t), eur(s - t - 1) if s - t > 1 else eur(s - t + 1)],
                   "%d € − %s = <b>%s</b>." % (s, eur(t), eur(s - t)))
    if kind == "gewicht":
        pr = Fr(R.randint(180, 1290), 100)
        g = R.choice([250, 500, 750, 200, 400])
        v = pr * g / 1000
        return mcq("Käse kostet %s pro kg. Was kosten %d g? (auf Cent runden)" % (eur(pr), g), eur(v), [eur(pr * g / 100), eur(pr / 2 if g != 500 else pr / 4), eur(v + Fr(1, 10))],
                   "%d g = %s kg. %s %s %s ≈ <b>%s</b>." % (g, dz(Fr(g, 1000)), eur(pr), MAL, dz(Fr(g, 1000)), eur(v)))
    a, pa = R.choice([(3, 2), (4, 3), (6, 4), (5, 3)])
    p1 = Fr(R.randint(150, 500), 100)
    p2 = p1 * pa / a * Fr(R.choice([9, 11, 12, 8]), 10)
    p2 = Fr(int(p2 * 100), 100)
    u1, u2 = p1 / pa, p2 / a
    if u1 == u2:
        return None
    best = "die Packung mit %d Stück" % pa if u1 < u2 else "die Packung mit %d Stück" % a
    return mcq("Eine Packung mit %d Joghurts kostet %s, eine Packung mit %d Joghurts kostet %s. Welche ist günstiger pro Stück?" % (pa, eur(p1), a, eur(p2)), best,
               ["die Packung mit %d Stück" % (a if best.endswith("%d Stück" % pa) else pa), "Beide sind gleich günstig.", "immer die größere Packung"],
               "Pro Stück: %s %s %d ≈ %s und %s %s %d ≈ %s. Günstiger ist <b>%s</b>." % (eur(p1), G, pa, eur(u1), eur(p2), G, a, eur(u2), best))


def rezept():
    p, er = KIDS.next()
    kind = R.choice(["mehl", "milch", "butter"])
    a = R.choice([4, 6, 8])
    b = R.choice([x for x in (2, 3, 5, 10, 12) if x != a])
    if kind == "mehl":
        m = Fr(R.choice([1, 3, 1, 5]), 4) * R.choice([1, 2])
        v = m * b / a
        if not endlich(v):
            return None
        return mcq("Für %d Personen braucht man %s kg Mehl. Wie viel Mehl braucht man für %d Personen?" % (a, bh(m, True), b), "%s kg" % dz(v), ["%s kg" % dz(x) for x in (m * b, m + (b - a) if b > a else m / 2, m / a)] + ["%s kg" % dz(v + Fr(1, 4))],
                   "Für 1 Person: %s kg %s %d = %s kg. Für %d Personen: <b>%s kg</b>." % (bh(m, True), G, a, bh(m / a), b, dz(v)))
    if kind == "milch":
        m = Fr(R.choice([1, 3, 1, 5]), R.choice([2, 4]))
        v = m * b / a
        if not endlich(v):
            return None
        return mcq("Ein Rezept für %d Pfannkuchen braucht %s l Milch. Wie viel Milch braucht man für %d Pfannkuchen?" % (a, bh(m, True), b), "%s l" % dz(v), ["%s l" % dz(x) for x in (m * b, m / b, v + Fr(1, 10))],
                   "%s l %s %d %s %d = <b>%s l</b>." % (bh(m, True), G, a, MAL, b, dz(v)))
    g = R.choice([125, 150, 200, 250])
    v = Fr(g * b, a)
    if v.denominator != 1:
        return None
    return mcq("Für einen Kuchen für %d Personen braucht man %d g Butter. Wie viel Butter braucht man für %d Personen?" % (a, g, b), "%d g" % v, ["%d g" % x for x in (g * b, g + 25 * (b - a) if g + 25 * (b - a) > 0 else g // 2, g // a)],
               "%d g %s %d %s %d = <b>%d g</b>." % (g, G, a, MAL, b, v))


def zeit():
    p, er = KIDS.next()
    kind = R.choice(["bruch", "dez", "plan"])
    if kind == "bruch":
        z, n = R.choice([(1, 4), (3, 4), (1, 3), (2, 3), (1, 6), (5, 6), (1, 5), (2, 5), (1, 12)])
        return mcq("%s übt %s Stunde Klavier. Wie viele Minuten sind das?" % (p, fr(z, n)), "%d min" % (60 * z // n), ["%d min" % x for x in (100 * z // n if 100 * z % n == 0 else z * n * 5, 60 // n, 60 - 60 * z // n)],
                   "%s von 60 min = <b>%d min</b>." % (fr(z, n), 60 * z // n))
    if kind == "dez":
        h = Fr(R.choice([1, 2, 3]), 4) + R.randint(1, 3)
        return mcq("Eine Fahrt dauert %s Stunden. Wie lange ist das in Stunden und Minuten?" % dz(h), "%d h %d min" % (int(h), (h - int(h)) * 60), ["%d h %s min" % (int(h), dz((h - int(h)) * 100)), "%d h %d min" % (int(h), (h - int(h)) * 60 + 10), "%d h %d min" % (int(h) + 1, (h - int(h)) * 60)],
                   "%s h = %d h + %s h. %s %s 60 min = %d min. <b>%d h %d min</b>." % (dz(h), int(h), dz(h - int(h)), dz(h - int(h)), MAL, (h - int(h)) * 60, int(h), (h - int(h)) * 60))
    a = R.choice([Fr(1, 4), Fr(1, 2), Fr(3, 4), Fr(1, 3)])
    b = R.choice([Fr(1, 4), Fr(1, 2), Fr(1, 6), Fr(1, 3)])
    if a == b:
        return None
    m = (a + b) * 60
    return mcq("%s macht %s h Hausaufgaben und liest danach %s h. Wie viele Minuten sind das zusammen?" % (p, bh(a), bh(b)), "%d min" % m, ["%d min" % x for x in (m + 10, (a + b) * 100 if ((a + b) * 100).denominator == 1 else m - 5, 60)],
               "%s h = %d min, %s h = %d min. Zusammen <b>%d min</b>." % (bh(a), a * 60, bh(b), b * 60, m))


def mehrschritt():
    p, er = KIDS.next()
    kind = R.choice(["fahrt", "pizza", "lauf", "garten"])
    if kind == "fahrt":
        k = R.randint(18, 28)
        pr = Fr(R.randint(450, 950), 100)
        e = Fr(R.randint(20, 60), 1)
        t = k * pr + e
        return mcq("Eine Klasse mit %d Kindern macht einen Ausflug. Die Fahrt kostet %s pro Kind, dazu kommen %d € Eintritt für die ganze Klasse. Was kostet der Ausflug insgesamt?" % (k, eur(pr), e), eur(t), [eur(k * (pr + e)), eur(k * pr), eur(t + pr)],
                   "%d %s %s = %s. Plus %d € = <b>%s</b>." % (k, MAL, eur(pr), eur(k * pr), e, eur(t)))
    if kind == "pizza":
        n = R.randint(3, 6)
        pr = Fr(R.randint(650, 1190), 100)
        k = R.randint(4, 8)
        t = n * pr
        v = t / k
        if (v * 100).denominator != 1:
            return None
        return mcq("%d Freunde bestellen %d Pizzas zu je %s und teilen die Rechnung gerecht. Wie viel zahlt jeder?" % (k, n, eur(pr), ), eur(v), [eur(pr / k), eur(t), eur(v + 1)],
                   "%d %s %s = %s. %s %s %d = <b>%s</b>." % (n, MAL, eur(pr), eur(t), eur(t), G, k, eur(v)))
    if kind == "lauf":
        r = Fr(R.choice([4, 5, 8]), 10)
        n = R.randint(5, 15)
        z, d = R.choice([(1, 2), (1, 4), (3, 4)])
        km = r * n
        v = km * Fr(z, d)
        if not endlich(v):
            return None
        return mcq("Eine Runde auf dem Sportplatz ist %s km lang. %s läuft %d Runden. %s der Strecke läuft %s schnell. Wie viele Kilometer läuft %s schnell?" % (dz(r), p, n, fr(z, d), er, er), "%s km" % dz(v), ["%s km" % dz(x) for x in (km, km - v, r * Fr(z, d))],
                   "Strecke: %d %s %s = %s km. %s davon: <b>%s km</b>." % (n, MAL, dz(r), dz(km), fr(z, d), dz(v)))
    a, b = Fr(R.randint(20, 80), 10), Fr(R.randint(15, 50), 10)
    z, d = R.choice([(1, 2), (1, 4), (3, 4), (2, 5)])
    A = a * b
    v = A * Fr(z, d)
    if not endlich(v) or len(dz(v).split(",")[-1]) > 3:
        return None
    return mcq("Ein Garten ist %s m lang und %s m breit. Auf %s der Fläche wächst Rasen. Wie groß ist die Rasenfläche?" % (dz(a), dz(b), fr(z, d)), "%s m²" % dz(v), ["%s m²" % dz(x) for x in (A, A - v, (a + b) * 2 * Fr(z, d))],
               "Fläche: %s %s %s = %s m². %s davon: <b>%s m²</b>." % (dz(a), MAL, dz(b), dz(A), fr(z, d), dz(v)))


def main():
    seen = set()
    sets = [
        ("Anteile und Rest", mix(R, seen, [(anteil, 20)])),
        ("Einkaufen", mix(R, seen, [(einkauf, 20)])),
        ("Rezepte und Zeit", mix(R, seen, [(rezept, 10), (zeit, 10)])),
        ("Gemischte Sachaufgaben", mix(R, seen, [(anteil, 6), (einkauf, 7), (zeit, 7)])),
        ("Aufgaben in mehreren Schritten", mix(R, seen, [(mehrschritt, 20)])),
    ]
    body = lesson(
        ["Lies die Aufgabe genau: Was ist gegeben, was ist gesucht? Schreibe die Rechenschritte einzeln auf.",
         "Ein Bruch „von“ einer Größe heißt mal: %s von 24 € = 24 € %s %s = 18 €." % (fr(3, 4), MAL, fr(3, 4)),
         "Achte darauf, ob ein Anteil vom <b>Ganzen</b> oder vom <b>Rest</b> genommen wird.",
         "Brüche und Dezimalzahlen kann man ineinander umwandeln: %s h = 0,25 h = 15 min." % fr(1, 4),
         "Mache zum Schluss einen Überschlag und schreibe einen Antwortsatz."],
        [example("%s von 60 €, dann %s vom Rest" % (fr(1, 3), fr(1, 2)), ["%s von 60 € = 20 €" % fr(1, 3), "Rest 40 €", "%s von 40 € = 20 €" % fr(1, 2)], "20 €"),
         example("2,5 kg Äpfel zu 1,80 € pro kg", ["2,5 %s 1,80 €" % MAL], "4,50 €")],
        [["%s vom Rest wie vom Ganzen gerechnet" % fr(1, 2), "Erst den Rest berechnen, dann den Anteil davon"],
         ["1,25 h = 1 h 25 min", "0,25 h = 15 min: 1 h 15 min"],
         ["Nur den ersten Schritt gerechnet", "Alle Schritte bis zur gesuchten Größe"]])
    faq = [
        {"q": "Wie gehe ich bei Sachaufgaben vor?", "a": "Gegeben und gesucht aufschreiben, Rechenschritte planen, rechnen, Überschlag machen und einen Antwortsatz schreiben."},
        {"q": "Was bedeutet „ein Drittel vom Rest“?", "a": "Man rechnet zuerst aus, was übrig ist, und nimmt davon ein Drittel – nicht vom ursprünglichen Ganzen."},
        {"q": "Wie viele Minuten sind 0,75 Stunden?", "a": "0,75 · 60 min = 45 min."},
        {"q": "Wie finde ich das günstigere Angebot?", "a": "Den Preis pro Stück oder pro kg ausrechnen und vergleichen."},
    ]
    make_unit(R, "sachaufgaben-mit-bruechen-und-dezimalzahlen", "Z",
              "Die Schülerinnen und Schüler lösen Sachaufgaben mit Brüchen und Dezimalzahlen in mehreren Schritten, rechnen Anteile, Preise, Rezepte und Zeitangaben und überprüfen Ergebnisse (Zusammenfassung).",
              "Sachaufgaben mit Brüchen und Dezimalzahlen",
              "Sachaufgaben mit Brüchen und Dezimalzahlen Klasse 6 – Arbeitsblätter",
              "Sachaufgaben",
              "Sachaufgaben für Klasse 6: Anteile und Rest, Einkaufen, Rezepte, Zeit und Aufgaben in mehreren Schritten. 100 Aufgaben mit Lösungen, kostenlos.",
              "Erst planen, dann rechnen, dann prüfen.",
              "Anteil vom Ganzen oder vom Rest? Genau lesen.",
              body, faq, sets, 19, grade="klasse-6")


if __name__ == "__main__":
    main()
