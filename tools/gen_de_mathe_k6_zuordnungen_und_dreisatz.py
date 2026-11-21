# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 6: Zuordnungen und Dreisatz（Leitidee Funktionaler Zusammenhang, Sek I）
  python3 tools/gen_de_mathe_k6_zuordnungen_und_dreisatz.py
Proportionale und antiproportionale Zuordnungen erkennen, Wertetabellen ergänzen, Dreisatz, Graphen proportionaler Zuordnungen, Sachaufgaben.
Fehler: jede steigende Zuordnung für proportional gehalten, bei antiproportional multipliziert statt dividiert, im Dreisatz den Zwischenschritt falsch.
"""
import random
from fractions import Fraction as Fr
from de_common import lesson, example, make_unit, mix, Kids, MAL, table, wrap, line, text, INK, RED, BLUE
from de_k6 import dz, mcq

R = random.Random(49613)
KIDS = Kids(R)
G = ":"


def tab(head, xs, ys):
    return table([head[0]] + [str(x) for x in xs], [[head[1]] + [y if isinstance(y, str) else dz(y) for y in ys]])


def art():
    kind = R.choice(["prop", "anti", "keine"])
    xs = sorted(R.sample(range(1, 9), 4))
    if kind == "prop":
        k = R.choice([2, 3, 4, 5, 1.5, 2.5, 12])
        ys = [Fr(k).limit_denominator() * x for x in xs]
    elif kind == "anti":
        c = R.choice([24, 36, 48, 60, 72, 120])
        xs = sorted(R.sample([x for x in range(1, 13) if c % x == 0], 4))
        ys = [Fr(c, x) for x in xs]
    else:
        a, b = R.randint(2, 5), R.randint(1, 6)
        ys = [a * x + b for x in xs]
    T = tab(("x", "y"), xs, ys)
    ans = {"prop": "proportional", "anti": "antiproportional", "keine": "weder noch"}[kind]
    if kind == "prop":
        why = "Der Quotient y : x ist immer gleich (%s)." % dz(ys[0] / xs[0])
    elif kind == "anti":
        why = "Das Produkt x %s y ist immer gleich (%s)." % (MAL, dz(xs[0] * ys[0]))
    else:
        why = "Weder y : x noch x %s y ist immer gleich. (Doppeltes x gibt nicht doppeltes y.)" % MAL
    return mcq(T + "Welche Zuordnung zeigt die Tabelle?", ans, [v for v in ("proportional", "antiproportional", "weder noch") if v != ans] + ["beides"], why + " Antwort: <b>%s</b>." % ans)


def ergaenzen():
    kind = R.choice(["prop", "prop", "anti"])
    if kind == "prop":
        k = Fr(R.choice([2, 3, 4, 5, 6, 8, 12, 15]), R.choice([1, 1, 2]))
        xs = sorted(R.sample(range(1, 11), 3))
        x = R.choice([v for v in range(2, 21) if v not in xs])
        allx = sorted(xs + [x])
        m = lambda c: ("%d,%02d" % divmod(int(c * 100), 100)) if Fr(c).denominator > 1 else str(c)
        T = tab(("Anzahl", "Preis in €"), allx, [m(k * u) if u != x else "?" for u in allx])
        v = k * x
        prev = max([u for u in xs if u < x] or [xs[0]])
        return mcq(T + "Die Zuordnung ist proportional. Welcher Preis gehört zur Anzahl %d?" % x, m(v) + " €", [m(c) + " €" for c in (v + k, k * prev + (x - prev) if x > prev else k * prev - (prev - x), v * 2) if c > 0],
                   "Preis für 1 Stück: %s € (%s %s %d). %d %s %s € = <b>%s €</b>." % (m(k), m(k * xs[0]), G, xs[0], x, MAL, m(k), m(v)))
    c = R.choice([24, 36, 48, 60, 72, 120])
    ds = [d for d in range(1, 13) if c % d == 0]
    xs = sorted(R.sample(ds, 3))
    x = R.choice([d for d in ds if d not in xs])
    allx = sorted(xs + [x])
    T = tab(("Personen", "Tage"), allx, [Fr(c, v) if v != x else "?" for v in allx])
    return mcq(T + "Die Zuordnung ist antiproportional. Welche Zahl gehört zu %d Personen?" % x, str(c // x), [str(c // xs[0] * x // xs[0]) if c // xs[0] * x % xs[0] == 0 else str(c // x + 1), str(c // x + 2), str(c - x)],
               "Das Produkt ist immer %d. %d %s %d = <b>%d</b>." % (c, c, G, x, c // x))


def dreisatz():
    p, er = KIDS.next()
    kind = R.choice(["preis", "preis", "weg", "anti_pers", "anti_hahn"])
    if kind == "preis":
        a = R.choice([3, 4, 5, 6, 8])
        ding, lo, hi = R.choice([("Hefte", 60, 150), ("Brötchen", 35, 60), ("Kugeln Eis", 120, 180), ("Bleistifte", 40, 120), ("Bananen", 25, 45), ("Kinokarten", 750, 1100)])
        pr = Fr(R.randint(lo, hi) // 5 * 5 * a, 100)
        b = R.choice([x for x in range(2, 13) if x != a])
        v = pr / a * b
        f = lambda x: "%d,%02d €" % divmod(int(x * 100 + Fr(1, 2)), 100)
        return mcq("%d %s kosten %s. Wie viel kosten %d %s?" % (a, ding, f(pr), b, ding), f(v), [f(pr * b), f(pr + (b - a)) if b > a else f(pr - Fr(b, 10)), f(pr / a)],
                   "1 Stück: %s %s %d = %s. %d Stück: %s %s %d = <b>%s</b>." % (f(pr).replace(" €", ""), G, a, f(pr / a), b, f(pr / a).replace(" €", ""), MAL, b, f(v)))
    if kind == "weg":
        h = R.choice([2, 3, 4])
        km = h * R.choice([15, 20, 60, 80, 90])
        t = R.choice([x for x in (1, 5, 6, 7) if x != h])
        v = km // h * t
        return mcq("Ein Zug fährt gleichmäßig in %d Stunden %d km. Wie weit fährt er in %d Stunden?" % (h, km, t), "%d km" % v, ["%d km" % x for x in (km * t, km + (t - h) if t > h else km - h, km // h)],
                   "1 Stunde: %d %s %d = %d km. %d Stunden: <b>%d km</b>." % (km, G, h, km // h, t, v))
    if kind == "anti_pers":
        c = R.choice([24, 30, 36, 40, 48, 60])
        a = R.choice([d for d in (2, 3, 4, 5, 6) if c % d == 0])
        b = R.choice([d for d in (2, 3, 4, 5, 6, 8, 10, 12) if c % d == 0 and d != a])
        return mcq("%d Maler streichen ein Haus in %d Tagen. Wie lange brauchen %d Maler (gleich schnell)?" % (a, c // a, b), "%d Tage" % (c // b), ["%d Tage" % x for x in (c // a * b // a if c // a * b % a == 0 else c // a + b, c // a + (a - b) if c // a + a - b > 0 else c // a + 2, c)],
                   "1 Maler bräuchte %d %s %d = %d Tage. %d Maler: %d %s %d = <b>%d Tage</b>. (Mehr Maler, weniger Tage.)" % (a, MAL, c // a, c, b, c, G, b, c // b))
    c = R.choice([60, 120, 180, 240])
    a = R.choice([d for d in (2, 3, 4, 5, 6) if c % d == 0])
    b = R.choice([d for d in (2, 3, 4, 5, 6, 10) if c % d == 0 and d != a])
    return mcq("Mit %d gleichen Pumpen ist ein Becken in %d Minuten leer. Wie lange dauert es mit %d Pumpen?" % (a, c // a, b), "%d min" % (c // b), ["%d min" % x for x in (c // a * b // a if c // a * b % a == 0 else c // a * 2, c // a, c)],
               "1 Pumpe: %d %s %d = %d min. %d Pumpen: %d %s %d = <b>%d min</b>." % (a, MAL, c // a, c, b, c, G, b, c // b))


def sache():
    p, er = KIDS.next()
    kind = R.choice(["rezept", "drucker", "lohn", "futter", "wasser", "fliesen"])
    if kind == "rezept":
        a = R.choice([2, 4, 6])
        g = R.choice([150, 200, 300, 450, 600])
        b = R.choice([x for x in (2, 3, 4, 5, 6, 8, 10, 12) if x != a and g * x % a == 0])
        return mcq("Für %d Personen braucht man %d g Mehl. Wie viel Mehl braucht man für %d Personen?" % (a, g, b), "%d g" % (g * b // a), ["%d g" % x for x in (g * b, g + (b - a) if b > a else g - (a - b), g // a)],
                   "1 Person: %d g %s %d = %s g. %d Personen: <b>%d g</b>." % (g, G, a, dz(Fr(g, a)), b, g * b // a))
    if kind == "drucker":
        s_ = R.choice([12, 15, 18, 20, 24])
        m = R.choice([3, 4, 5, 7, 8, 10])
        return mcq("Ein Drucker druckt %d Seiten in einer Minute. Wie viele Seiten druckt er in %d Minuten?" % (s_, m), str(s_ * m), [str(s_ + m), str(s_ * m // 2), str(s_ * (m + 1))],
                   "%d %s %d = <b>%d</b> Seiten." % (s_, MAL, m, s_ * m))
    if kind == "lohn":
        h = R.choice([3, 4, 5, 6])
        lohn = R.choice([12, 13, 14, 15])
        t = R.choice([x for x in (2, 7, 8, 9, 10) if x != h])
        return mcq("Für %d Stunden Babysitten bekommt %s %d €. Wie viel bekommt %s für %d Stunden (gleicher Stundenlohn)?" % (h, p, h * lohn, er, t), "%d €" % (lohn * t), ["%d €" % x for x in (h * lohn + t, lohn * t + lohn, h * lohn * t)],
                   "1 Stunde: %d € %s %d = %d €. %d Stunden: <b>%d €</b>." % (h * lohn, G, h, lohn, t, lohn * t))
    if kind == "futter":
        c = R.choice([24, 36, 48, 60])
        a = R.choice([d for d in (2, 3, 4, 6) if c % d == 0])
        b = R.choice([d for d in (2, 3, 4, 6, 8, 12) if c % d == 0 and d != a])
        return mcq("Ein Futtervorrat reicht für %d Pferde %d Tage. Wie lange reicht er für %d Pferde?" % (a, c // a, b), "%d Tage" % (c // b), ["%d Tage" % x for x in (c // a * b // a if c // a * b % a == 0 else c // a + 3, c // a, c)],
                   "Für 1 Pferd: %d %s %d = %d Tage. Für %d Pferde: <b>%d Tage</b>. (Mehr Pferde, weniger Tage.)" % (a, MAL, c // a, c, b, c // b))
    if kind == "wasser":
        l = R.choice([6, 8, 9, 12])
        m = R.choice([2, 3])
        t = R.choice([5, 10, 15, 20])
        return mcq("Ein Wasserhahn tropft. In %d Stunden kommen %d Liter zusammen. Wie viel Wasser ist es in %d Stunden?" % (m, l, t), "%s l" % dz(Fr(l * t, m)), ["%s l" % dz(x) for x in (l * t, l + t, Fr(l, m))],
                   "1 Stunde: %d %s %d = %s l. %d Stunden: <b>%s l</b>." % (l, G, m, dz(Fr(l, m)), t, dz(Fr(l * t, m))))
    n = R.choice([60, 72, 90, 120])
    a = R.choice([d for d in (2, 3, 4, 5, 6) if n % d == 0])
    b = R.choice([d for d in (2, 3, 4, 5, 6, 8, 9, 10) if n % d == 0 and d != a])
    return mcq("Für einen Boden braucht man %d Platten zu je %d dm². Wie viele Platten braucht man, wenn jede Platte %d dm² groß ist?" % (n // a, a, b), str(n // b), [str(n // a * b // a) if n // a * b % a == 0 else str(n // a + 1), str(n // a), str(n)],
               "Fläche: %d %s %d = %d dm². %d %s %d = <b>%d</b> Platten." % (n // a, MAL, a, n, n, G, b, n // b))


def graph():
    k = R.choice([Fr(1, 2), 1, 2, 3, Fr(3, 2), 4])
    k = Fr(k)
    W, H, x0, y0, u = 300, 230, 34, 200, 26
    s = [line(x0, y0, x0 + 9 * u + 10, y0, INK, 2), line(x0, y0, x0, y0 - 7 * u - 10, INK, 2)]
    for i in range(1, 10):
        s.append(line(x0 + i * u, y0, x0 + i * u, y0 - 7 * u, "#d5dfec", 1) + text(x0 + i * u, y0 + 16, str(i), 11, weight=500))
    for j in range(1, 8):
        s.append(line(x0, y0 - j * u, x0 + 9 * u, y0 - j * u, "#d5dfec", 1) + text(x0 - 10, y0 - j * u + 4, str(j), 11, weight=500))
    xe = min(9, int(7 / k))
    s.append(line(x0, y0, x0 + xe * u, y0 - float(k * xe) * u, BLUE, 3))
    s.append(text(x0 + 9 * u + 6, y0 + 16, "kg", 11) + text(x0 - 4, y0 - 7 * u - 14, "€", 11))
    pic = wrap(W, H, "".join(s), "Graph einer proportionalen Zuordnung", lg=True)
    x = R.randint(1, xe)
    v = k * x
    return mcq(pic + "Der Graph zeigt den Preis für Kartoffeln. Wie viel kosten %d kg?" % x, "%s €" % dz(v), ["%s €" % dz(t) for t in (v + k, Fr(x) / k if Fr(x) / k != v else v + 1, k)] if x != 1 else ["%s €" % dz(t) for t in (v + k, v * 2, v + 1)],
               "1 kg kostet %s €. %d %s %s = <b>%s €</b>." % (dz(k), x, MAL, dz(k), dz(v)))


def main():
    seen = set()
    sets = [
        ("Zuordnungen erkennen", mix(R, seen, [(art, 20)])),
        ("Tabellen ergänzen", mix(R, seen, [(ergaenzen, 20)])),
        ("Graphen ablesen", mix(R, seen, [(graph, 8), (art, 6), (ergaenzen, 6)])),
        ("Dreisatz", mix(R, seen, [(dreisatz, 20)])),
        ("Sachaufgaben", mix(R, seen, [(sache, 20)])),
    ]
    body = lesson(
        ["<b>Proportional</b>: Zum Doppelten gehört das Doppelte, zur Hälfte die Hälfte. Der Quotient y : x ist immer gleich. Der Graph ist eine Gerade durch den Ursprung.",
         "<b>Antiproportional</b>: Zum Doppelten gehört die Hälfte. Das Produkt x %s y ist immer gleich." % MAL,
         "<b>Dreisatz</b>: 1. Gegeben – 2. auf eins schließen – 3. auf die gesuchte Menge schließen.",
         "Bei antiproportionalen Zuordnungen rechnet man im Dreisatz umgekehrt (erst mal, dann geteilt)."],
        [example("3 Hefte kosten 4,50 €. Was kosten 5 Hefte?", ["1 Heft: 4,50 € %s 3 = 1,50 €" % G, "5 Hefte: 1,50 € %s 5" % MAL], "7,50 €"),
         example("4 Pumpen brauchen 6 h. Wie lange brauchen 3 Pumpen?", ["1 Pumpe: 4 %s 6 = 24 h" % MAL, "3 Pumpen: 24 %s 3" % G], "8 h")],
        [["Alter und Körpergröße sind proportional", "Nicht jede steigende Zuordnung ist proportional"],
         ["Mehr Maler: mehr Tage", "Antiproportional: mehr Maler, weniger Tage"],
         ["3 Hefte 4,50 €, also 5 Hefte 6,50 € (+2)", "Erst auf 1 Heft schließen: 7,50 €"]])
    faq = [
        {"q": "Wie erkenne ich eine proportionale Zuordnung?", "a": "Teile y durch x. Ist das Ergebnis immer gleich, ist die Zuordnung proportional."},
        {"q": "Wie erkenne ich eine antiproportionale Zuordnung?", "a": "Multipliziere x und y. Ist das Produkt immer gleich, ist sie antiproportional."},
        {"q": "Was ist der Dreisatz?", "a": "Ein Rechenweg in drei Schritten: gegebene Werte, auf eins schließen, auf die gesuchte Menge schließen."},
        {"q": "Wie sieht der Graph einer proportionalen Zuordnung aus?", "a": "Eine Gerade durch den Ursprung (0|0)."},
    ]
    make_unit(R, "zuordnungen-und-dreisatz", "F",
              "Die Schülerinnen und Schüler erkennen proportionale und antiproportionale Zuordnungen in Tabellen und Graphen und lösen Sachaufgaben mit dem Dreisatz (Zusammenfassung).",
              "Zuordnungen und Dreisatz",
              "Zuordnungen und Dreisatz Klasse 6 – proportional und antiproportional",
              "Dreisatz",
              "Zuordnungen und Dreisatz für Klasse 6: proportional, antiproportional, Tabellen, Graphen und Sachaufgaben. 100 Aufgaben mit Lösungen, kostenlos.",
              "Dreisatz: erst auf eins schließen.",
              "Proportional: Quotient gleich. Antiproportional: Produkt gleich.",
              body, faq, sets, 13, grade="klasse-6")


if __name__ == "__main__":
    main()
