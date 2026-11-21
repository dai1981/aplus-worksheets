# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 7: Proportionale und antiproportionale Zuordnungen（Leitidee Funktionaler Zusammenhang, Sek I）
  python3 tools/gen_de_mathe_k7_proportionale_und_antiproportionale_zuordnungen.py
Quotientengleichheit und Produktgleichheit, Proportionalitätsfaktor k und y = k · x, antiproportional y = c : x, Graphen (Ursprungsgerade, Hyperbel), Dreisatz in beiden Richtungen, Sachaufgaben.
Fehler: jede wachsende Zuordnung für proportional gehalten, bei antiproportionalen Zuordnungen wie bei proportionalen gerechnet, k falsch herum (x : y).
"""
import random
from fractions import Fraction as Fr
from de_common import lesson, example, make_unit, mix, Kids, MAL, table, wrap, line, text, INK, RED, BLUE
from de_k6 import dz
from de_k7 import mcq, eur

R = random.Random(49706)
KIDS = Kids(R)
G = ":"


def tab(h, xs, ys):
    return table([h[0]] + [dz(x) for x in xs], [[h[1]] + [y if isinstance(y, str) else dz(y) for y in ys]])


def erkennen():
    kind = R.choice(["prop", "anti", "keine", "keine"])
    xs = sorted(R.sample([1, 2, 3, 4, 5, 6, 8, 10, 12], 4))
    if kind == "prop":
        k = Fr(R.choice([3, 5, 7, 12, 15, 25]), R.choice([1, 2, 10]))
        ys = [k * x for x in xs]
        e = "y : x ist immer %s. Die Zuordnung ist <b>proportional</b>." % dz(k)
    elif kind == "anti":
        c = R.choice([60, 120, 240])
        xs = sorted(R.sample([x for x in (1, 2, 3, 4, 5, 6, 8, 10, 12) if c % x == 0], 4))
        ys = [Fr(c, x) for x in xs]
        e = "x %s y ist immer %d. Die Zuordnung ist <b>antiproportional</b>." % (MAL, c)
    else:
        a, b = R.randint(2, 9), R.choice([-3, -2, 2, 3, 5, 10])
        ys = [a * x + b for x in xs]
        if min(ys) <= 0:
            return None
        e = "Weder y : x noch x %s y ist konstant: <b>weder noch</b>. (Es gilt y = %d %s x %s %d – mit Startwert, also nicht proportional.)" % (MAL, a, MAL, "+" if b > 0 else "−", abs(b))
    ans = {"prop": "proportional", "anti": "antiproportional", "keine": "weder noch"}[kind]
    return mcq(tab(("x", "y"), xs, ys) + "Welche Zuordnung liegt vor?", ans, [v for v in ("proportional", "antiproportional", "weder noch") if v != ans] + ["beides"], e)


def faktor():
    k = Fr(R.choice([2, 3, 4, 5, 6, 8, 12, 15, 25, 35]), R.choice([1, 2, 4, 10]))
    x = R.choice([2, 3, 4, 5, 6, 8, 10])
    y = k * x
    if k == 1:
        return None
    kind = R.choice(["k", "gl", "y"])
    if kind == "k":
        return mcq("Die Zuordnung ist proportional. Zu x = %d gehört y = %s. Wie groß ist der Proportionalitätsfaktor k?" % (x, dz(y)), dz(k), [dz(Fr(x) / y) if (Fr(x) / y * 1000).denominator == 1 else dz(k + 1), dz(y - x) if y > x else dz(k * 2), dz(y * x)],
                   "k = y %s x = %s %s %d = <b>%s</b>." % (G, dz(y), G, x, dz(k)))
    if kind == "gl":
        return mcq("Die Zuordnung ist proportional. Zu x = %d gehört y = %s. Welche Gleichung beschreibt sie?" % (x, dz(y)), "y = %s %s x" % (dz(k), MAL), ["y = %s %s x" % (dz(Fr(x) / y) if (Fr(x) / y * 1000).denominator == 1 else dz(k + 1), MAL), "y = x + %s" % dz(y - x) if y > x else "y = x − %s" % dz(x - y), "y = %s : x" % dz(y * x)],
                   "k = %s %s %d = %s. <b>y = %s %s x</b>" % (dz(y), G, x, dz(k), dz(k), MAL))
    x2 = R.choice([v for v in (3, 7, 9, 11, 15, 20) if v != x])
    return mcq("Für eine proportionale Zuordnung gilt y = %s %s x. Berechne y für x = %d." % (dz(k), MAL, x2), dz(k * x2), [dz(k + x2), dz(Fr(x2) / k) if (Fr(x2) / k * 1000).denominator == 1 else dz(k * x2 + k), dz(k * (x2 - 1))],
               "%s %s %d = <b>%s</b>." % (dz(k), MAL, x2, dz(k * x2)))


def anti():
    c = R.choice([24, 36, 48, 60, 72, 90, 120, 180])
    xs = [x for x in range(1, 13) if c % x == 0]
    a, b = R.sample(xs, 2)
    kind = R.choice(["wert", "prod", "gl"])
    if kind == "wert":
        return mcq("Die Zuordnung ist antiproportional. Zu x = %d gehört y = %d. Welcher y-Wert gehört zu x = %d?" % (a, c // a, b), str(c // b), [str(c // a * b // a) if c // a * b % a == 0 else str(c // b + 1), str(c // a + b - a) if c // a + b - a > 0 else str(c // b + 2), str(c)],
                   "Das Produkt ist %d %s %d = %d. %d %s %d = <b>%d</b>." % (a, MAL, c // a, c, c, G, b, c // b))
    if kind == "prod":
        return mcq("Bei einer antiproportionalen Zuordnung gehört zu x = %d der Wert y = %d. Welches Produkt x %s y gilt für alle Paare?" % (a, c // a, MAL), str(c), [str(a + c // a), str(c // a - a) if c // a > a else str(a - c // a + 1), str(Fr(c // a, a)) if (c // a) % a == 0 else str(c * 2)],
                   "x %s y = %d %s %d = <b>%d</b>." % (MAL, a, MAL, c // a, c))
    return mcq("Bei einer antiproportionalen Zuordnung gehört zu x = %d der Wert y = %d. Welche Gleichung passt?" % (a, c // a), "y = %d : x" % c, ["y = %s %s x" % (dz(Fr(c // a, a)), MAL), "y = %d − x" % (a + c // a), "y = x : %d" % c],
               "x %s y = %d, also <b>y = %d : x</b>." % (MAL, c, c))


def graph():
    kind = R.choice(["prop", "anti"])
    W, H, x0, y0, u = 300, 230, 34, 200, 26
    s = [line(x0, y0, x0 + 9 * u + 10, y0, INK, 2), line(x0, y0, x0, y0 - 7 * u - 10, INK, 2)]
    for i in range(1, 10):
        s.append(line(x0 + i * u, y0, x0 + i * u, y0 - 7 * u, "#d5dfec", 1) + text(x0 + i * u, y0 + 16, str(i), 11, weight=500))
    for j in range(1, 8):
        s.append(line(x0, y0 - j * u, x0 + 9 * u, y0 - j * u, "#d5dfec", 1) + text(x0 - 10, y0 - j * u + 4, str(j), 11, weight=500))
    s.append(text(x0 + 9 * u + 6, y0 + 16, "x", 12, italic=True) + text(x0 - 4, y0 - 7 * u - 14, "y", 12, italic=True))
    if kind == "prop":
        k = Fr(R.choice([1, 2, 3, 1, 3]), R.choice([1, 2, 4]))
        if k > 3:
            return None
        xe = min(9, int(7 / k))
        s.append(line(x0, y0, x0 + xe * u, y0 - float(k * xe) * u, BLUE, 3))
        x = R.randint(1, xe)
        q = "Der Graph zeigt eine Zuordnung. Wie groß ist der Proportionalitätsfaktor k?" if R.random() < 0.5 else "Welcher y-Wert gehört laut Graph zu x = %d?" % x
        pic = wrap(W, H, "".join(s), "Graph einer Zuordnung", lg=True)
        if "Faktor" in q:
            return mcq(pic + q, dz(k), [dz(1 / k), dz(k + 1), dz(k * 2)], "Es ist eine Gerade durch den Ursprung. Bei x = 1 ist y = %s: <b>k = %s</b>." % (dz(k), dz(k)))
        return mcq(pic + q, dz(k * x), [dz(k * x + k), dz(Fr(x) / k) if (Fr(x) / k * 100).denominator == 1 and Fr(x) / k != k * x else dz(k * x + 1), dz(x)], "Vom x-Wert %d senkrecht hoch bis zur Geraden: <b>y = %s</b>." % (x, dz(k * x)))
    c = R.choice([4, 6, 8, 12])
    pts = []
    for i in range(10, 91):
        xv = i / 10.0
        yv = c / xv
        if yv <= 7.2:
            pts.append("%.1f,%.1f" % (x0 + xv * u, y0 - yv * u))
    s.append("<polyline points='%s' fill='none' stroke='%s' stroke-width='3'/>" % (" ".join(pts), BLUE))
    pic = wrap(W, H, "".join(s), "Graph einer Zuordnung", lg=True)
    x = R.choice([d for d in (1, 2, 3, 4, 6, 8) if c % d == 0 and Fr(c, d) <= 7])
    q = R.choice(["Welche Art von Zuordnung zeigt der Graph?", "Welcher y-Wert gehört laut Graph zu x = %d?" % x])
    if "Art" in q:
        return mcq(pic + q, "antiproportional", ["proportional", "weder noch", "linear mit Startwert"], "Die Kurve ist eine Hyperbel: Je größer x, desto kleiner y, und x %s y bleibt gleich. <b>antiproportional</b>" % MAL)
    return mcq(pic + q, str(c // x), [str(c // x + 1), str(x), str(c)], "Vom x-Wert %d senkrecht hoch bis zur Kurve: <b>y = %d</b>. (Probe: %d %s %d = %d)" % (x, c // x, x, MAL, c // x, c))


def sache():
    p_, er = KIDS.next()
    kind = R.choice(["benzin", "arbeiter", "geschw", "kopien", "vorrat", "stoff", "rezept"])
    if kind == "benzin":
        l = R.choice([30, 40, 45, 50])
        pr = Fr(R.randint(165, 199), 100)
        l2 = R.choice([20, 25, 35, 60])
        return mcq("%d Liter Benzin kosten %s. Wie viel kosten %d Liter?" % (l, eur(pr * l), l2), eur(pr * l2), [eur(pr * l + (l2 - l)), eur(pr * l * l2 / 10), eur(pr * l * l / l2)],
                   "1 Liter: %s. %d Liter: <b>%s</b>." % (eur(pr), l2, eur(pr * l2)))
    if kind == "arbeiter":
        a, t = R.choice([(3, 12), (4, 9), (6, 10), (5, 12), (8, 6)])
        b = R.choice([x for x in (2, 3, 4, 5, 6, 8, 9, 10, 12) if a * t % x == 0 and x != a])
        return mcq("%d Handwerker brauchen für einen Auftrag %d Tage. Wie lange brauchen %d Handwerker (gleich schnell)?" % (a, t, b), "%d Tage" % (a * t // b), ["%s Tage" % dz(Fr(t * b, a)), "%d Tage" % (t + a - b) if t + a - b > 0 else "%d Tage" % (t + 2), "%d Tage" % (a * t)],
                   "Antiproportional: %d %s %d = %d Arbeitstage. %d %s %d = <b>%d Tage</b>." % (a, MAL, t, a * t, a * t, G, b, a * t // b))
    if kind == "geschw":
        v, t = R.choice([(60, 3), (80, 3), (90, 2), (100, 3), (120, 2), (50, 6)])
        v2 = R.choice([x for x in (40, 60, 75, 80, 90, 100, 120, 150) if v * t * 60 % x == 0 and x != v])
        m = v * t * 60 // v2
        return mcq("Bei %d km/h dauert eine Fahrt %d Stunden. Wie lange dauert sie bei %d km/h?" % (v, t, v2), "%d h %d min" % divmod(m, 60) if m % 60 else "%d h" % (m // 60),
                   ["%d h %d min" % divmod(t * v2 // v * 60 if t * v2 % v == 0 else m + 30, 60), "%d h" % t, "%d h %d min" % divmod(m + 15, 60)],
                   "Strecke: %d %s %d = %d km. %d km %s %d km/h = <b>%s</b>." % (v, MAL, t, v * t, v * t, G, v2, ("%d h %d min" % divmod(m, 60)) if m % 60 else "%d h" % (m // 60)))
    if kind == "kopien":
        n, pr = R.choice([(20, 160), (25, 150), (40, 320), (50, 300)])
        n2 = R.choice([15, 30, 35, 60, 75, 120])
        e = Fr(pr, 100) / n * n2
        return mcq("%d Kopien kosten %s. Was kosten %d Kopien?" % (n, eur(Fr(pr, 100)), n2), eur(e), [eur(Fr(pr, 100) * n2 / 10), eur(Fr(pr, 100) + Fr(n2 - n, 10)), eur(Fr(pr, 100) * n / n2)],
                   "1 Kopie: %s. %d Kopien: <b>%s</b>." % (eur(Fr(pr, 100) / n), n2, eur(e)))
    if kind == "vorrat":
        a, t = R.choice([(12, 20), (15, 16), (20, 18), (24, 10)])
        b = R.choice([x for x in (8, 10, 16, 30, 40, 48) if a * t % x == 0])
        return mcq("Ein Futtervorrat reicht für %d Tiere %d Tage. Wie lange reicht er für %d Tiere?" % (a, t, b), "%d Tage" % (a * t // b), ["%s Tage" % dz(Fr(t * b, a)), "%d Tage" % t, "%d Tage" % (a * t)],
                   "%d %s %d = %d. %d %s %d = <b>%d Tage</b>." % (a, MAL, t, a * t, a * t, G, b, a * t // b))
    if kind == "stoff":
        m = Fr(R.choice([15, 20, 25, 30]), 10)
        pr = R.choice([8, 12, 14, 16, 18])
        m2 = Fr(R.choice([35, 40, 45, 60]), 10)
        return mcq("%s m Stoff kosten %s. Wie viel kosten %s m?" % (dz(m), eur(m * pr), dz(m2)), eur(m2 * pr), [eur(m * pr + (m2 - m)), eur(m * pr * m2), eur(m2 * pr / 10)],
                   "1 m: %s. %s m: <b>%s</b>." % (eur(pr), dz(m2), eur(m2 * pr)))
    a = R.choice([4, 6, 8])
    g = R.choice([300, 360, 480])
    b = R.choice([x for x in (3, 5, 10, 12) if g * x % a == 0])
    return mcq("Für %d Portionen braucht man %d g Nudeln. Wie viel braucht man für %d Portionen?" % (a, g, b), "%d g" % (g * b // a), ["%d g" % x for x in (g + 50 * (b - a), g * a // b if g * a % b == 0 else g // 2, g * b)],
               "1 Portion: %s g. %d Portionen: <b>%d g</b>." % (dz(Fr(g, a)), b, g * b // a))


def main():
    seen = set()
    sets = [
        ("Zuordnungen erkennen", mix(R, seen, [(erkennen, 20)])),
        ("Proportionalitätsfaktor", mix(R, seen, [(faktor, 20)])),
        ("Antiproportionale Zuordnungen", mix(R, seen, [(anti, 20)])),
        ("Graphen", mix(R, seen, [(graph, 14), (erkennen, 6)])),
        ("Sachaufgaben", mix(R, seen, [(sache, 20)])),
    ]
    body = lesson(
        ["<b>Proportional</b>: Der Quotient y : x ist immer gleich, das ist der Proportionalitätsfaktor k. Es gilt y = k %s x. Der Graph ist eine Gerade durch den Ursprung." % MAL,
         "<b>Antiproportional</b>: Das Produkt x %s y ist immer gleich. Es gilt y = c : x. Der Graph ist eine Hyperbel." % MAL,
         "Nicht jede steigende Zuordnung ist proportional: y = 2x + 3 hat einen Startwert und ist weder proportional noch antiproportional.",
         "Mit dem <b>Dreisatz</b> rechnet man über die Einheit: bei proportionalen Zuordnungen erst teilen, dann multiplizieren – bei antiproportionalen umgekehrt."],
        [example("4 kg kosten 10 €. Was kosten 7 kg?", ["k = 10 : 4 = 2,5", "7 %s 2,5" % MAL], "17,50 €"),
         example("6 Pumpen brauchen 4 h. Wie lange brauchen 8 Pumpen?", ["6 %s 4 = 24" % MAL, "24 : 8"], "3 h")],
        [["Mehr Arbeiter, also mehr Tage", "Antiproportional: mehr Arbeiter, weniger Tage"],
         ["k = x : y", "k = y : x"],
         ["y = 2x + 3 ist proportional", "Kein Graph durch den Ursprung: nicht proportional"]])
    faq = [
        {"q": "Was ist der Proportionalitätsfaktor?", "a": "Der immer gleiche Quotient y : x einer proportionalen Zuordnung. Mit ihm gilt y = k · x."},
        {"q": "Woran erkenne ich eine antiproportionale Zuordnung?", "a": "Das Produkt x · y ist für alle Wertepaare gleich. Verdoppelt sich x, halbiert sich y."},
        {"q": "Wie sieht der Graph einer antiproportionalen Zuordnung aus?", "a": "Er ist eine Hyperbel: eine Kurve, die mit wachsendem x immer weiter absinkt, aber die Achsen nie erreicht."},
        {"q": "Ist jede Gerade eine proportionale Zuordnung?", "a": "Nein. Nur eine Gerade durch den Ursprung (0|0) gehört zu einer proportionalen Zuordnung."},
    ]
    make_unit(R, "proportionale-und-antiproportionale-zuordnungen", "F",
              "Die Schülerinnen und Schüler erkennen proportionale und antiproportionale Zuordnungen an Tabellen, Gleichungen und Graphen, bestimmen den Proportionalitätsfaktor und lösen Sachaufgaben mit dem Dreisatz (Zusammenfassung).",
              "Proportionale und antiproportionale Zuordnungen",
              "Proportionale und antiproportionale Zuordnungen Klasse 7 – Arbeitsblätter",
              "Zuordnungen",
              "Zuordnungen für Klasse 7: proportional und antiproportional erkennen, Proportionalitätsfaktor, Graphen und Dreisatz. 100 Aufgaben mit Lösungen, kostenlos.",
              "Proportional: y : x gleich. Antiproportional: x · y gleich.",
              "Proportionaler Graph: Gerade durch den Ursprung.",
              body, faq, sets, 6, grade="klasse-7")


if __name__ == "__main__":
    main()
