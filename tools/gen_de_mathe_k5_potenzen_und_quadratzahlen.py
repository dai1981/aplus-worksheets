# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 5: Potenzen und Quadratzahlen（Leitidee Zahl und Operation, Sek I）
  python3 tools/gen_de_mathe_k5_potenzen_und_quadratzahlen.py
Potenzschreibweise (Basis, Exponent), Quadratzahlen, Zehnerpotenzen, Potenzen berechnen, Potenz vor Punkt vor Strich.
Fehler: 2³ = 6 (Basis mal Exponent), 10⁶ mit 5 Nullen, Potenz nach Punktrechnung gerechnet.
"""
import random
from de_common import mcq, num, lesson, example, make_unit, mix, MAL, table

R = random.Random(49507)
SUP = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")


def p(b, e):
    return "%s%s" % (num(b), str(e).translate(SUP))


def schreib():
    kind = R.choice(["kurz", "lang", "begriff", "begriff"])
    b, e = R.randint(2, 12), R.randint(2, 6)
    if kind == "kurz":
        prod = (" %s " % MAL).join([str(b)] * e)
        return mcq("Schreibe als Potenz: %s" % prod, p(b, e), [p(e, b), "%d %s %d" % (b, MAL, e), p(b, e + 1)],
                   "Die %d wird %d-mal mit sich selbst multipliziert: <b>%s</b>." % (b, e, p(b, e)))
    if kind == "lang":
        ans = (" %s " % MAL).join([str(b)] * e)
        return mcq("Was bedeutet %s?" % p(b, e), ans, [(" %s " % MAL).join([str(e)] * b) if b <= 8 else "%d %s %d" % (e, MAL, b), "%d %s %d" % (b, MAL, e), " + ".join([str(b)] * e)],
                   "Basis %d, Exponent %d: <b>%s</b>." % (b, e, ans))
    which = R.choice(["Basis", "Exponent"])
    ans = str(b) if which == "Basis" else str(e)
    return mcq("Wie heißt bei %s %s %s?" % (p(b, e), "die" if which == "Basis" else "der", which), ans, [str(e) if which == "Basis" else str(b), num(b ** e), str(b * e)] if b != e else [num(b ** e), str(b * e), str(b + e)],
               "Die Basis ist die untere große Zahl (%d), der Exponent die kleine obere Zahl (%d): <b>%s</b>." % (b, e, ans))


def quadrat():
    n = R.randint(2, 20)
    kind = R.choice(["rechnen", "rechnen", "wurzel", "ist"])
    if kind == "rechnen":
        return mcq("%s = ?" % p(n, 2), num(n * n), [num(2 * n), num(n * n + n), num((n - 1) * (n - 1))], "%d %s %d = <b>%s</b>." % (n, MAL, n, num(n * n)))
    if kind == "wurzel":
        return mcq("Welche Zahl ergibt mit sich selbst multipliziert %s?" % num(n * n), num(n), [num(n * n // 2), num(n + 1), num(n - 1)],
                   "%d %s %d = %s: <b>%d</b>." % (n, MAL, n, num(n * n), n))
    sq = [k * k for k in range(2, 21)]
    good = R.choice(sq)
    bads = R.sample([x for x in range(10, 400) if x not in sq], 3)
    return mcq("Welche Zahl ist eine Quadratzahl?", num(good), [num(x) for x in bads], "%s = %s: <b>%s</b>." % (p(int(good ** 0.5 + 0.5), 2), num(good), num(good)))


def zehner():
    e = R.randint(2, 9)
    kind = R.choice(["wert", "potenz", "mal"])
    if kind == "wert":
        return mcq("%s = ?" % p(10, e), num(10 ** e), [num(10 ** (e - 1)), num(10 ** (e + 1)), num(10 * e)], "Eine 1 mit %d Nullen: <b>%s</b>." % (e, num(10 ** e)))
    if kind == "potenz":
        name = {3: "Tausend", 6: "eine Million", 9: "eine Milliarde"}.get(e)
        q = "Schreibe %s als Zehnerpotenz." % (name if name else num(10 ** e))
        return mcq(q, p(10, e), [p(10, e - 1), p(10, e + 1), p(e, 10)], "%s hat %d Nullen: <b>%s</b>." % (num(10 ** e), e, p(10, e)))
    a = R.randint(2, 9)
    return mcq("%d %s %s = ?" % (a, MAL, p(10, e)), num(a * 10 ** e), [num(a * 10 ** (e - 1)), num(a * 10 ** (e + 1)), num(a * 10 * e)],
               "%d mit %d Nullen: <b>%s</b>." % (a, e, num(a * 10 ** e)))


def berechnen():
    b, e = R.choice([(2, k) for k in range(3, 11)] + [(3, k) for k in range(3, 7)] + [(4, 3), (4, 4), (5, 3), (5, 4), (6, 3), (7, 3), (1, 7), (1, 12), (0, 5)])
    v = b ** e
    return mcq("%s = ?" % p(b, e), num(v), [num(b * e) if b * e != v else num(v + 1), num(b ** (e - 1)) if b ** (e - 1) != v else num(v + 2), num(e ** b) if e ** b != v and e ** b < 10 ** 7 else num(v * b + 1)],
               "%s = <b>%s</b>." % ((" %s " % MAL).join([str(b)] * e), num(v)))


def reihenfolge():
    kind = R.choice(["plus", "mal", "klammer", "vergleich"])
    a, b = R.randint(2, 9), R.randint(2, 5)
    if kind == "plus":
        c = R.randint(2, 20)
        r = c + a ** 2
        return mcq("%d + %s = ?" % (c, p(a, 2)), num(r), [num((c + a) ** 2), num(c + 2 * a), num(r + 1)], "Potenz zuerst: %s = %d. %d + %d = <b>%s</b>." % (p(a, 2), a * a, c, a * a, num(r)))
    if kind == "mal":
        r = b * a ** 2
        return mcq("%d %s %s = ?" % (b, MAL, p(a, 2)), num(r), [num((b * a) ** 2), num(b * a * 2), num(r + a)], "Potenz zuerst: %s = %d. %d %s %d = <b>%s</b>." % (p(a, 2), a * a, b, MAL, a * a, num(r)))
    if kind == "klammer":
        c = R.randint(1, 5)
        r = (a + c) ** 2
        return mcq("(%d + %d)%s = ?" % (a, c, "²"), num(r), [num(a * a + c * c), num(a + c * c), num(2 * (a + c))], "Klammer zuerst: %d. %s = <b>%s</b>." % (a + c, p(a + c, 2), num(r)))
    x, y = R.choice([(2, 5), (5, 2), (3, 4), (4, 3), (2, 6), (6, 2), (3, 5), (5, 3), (2, 10), (10, 2)])
    vx, vy = x ** y, y ** x
    if vx == vy:
        return None
    big = p(x, y) if vx > vy else p(y, x)
    return mcq("Was ist größer: %s oder %s?" % (p(x, y), p(y, x)), big, [p(y, x) if big == p(x, y) else p(x, y), "Beide sind gleich groß", "Das kann man nicht vergleichen"],
               "%s = %s, %s = %s: <b>%s</b> ist größer." % (p(x, y), num(vx), p(y, x), num(vy), big))


def main():
    seen = set()
    sets = [
        ("Potenzschreibweise", mix(R, seen, [(schreib, 20)])),
        ("Quadratzahlen", mix(R, seen, [(quadrat, 20)])),
        ("Zehnerpotenzen", mix(R, seen, [(zehner, 20)])),
        ("Potenzen berechnen", mix(R, seen, [(berechnen, 20)])),
        ("Potenz vor Punkt vor Strich", mix(R, seen, [(reihenfolge, 20)])),
    ]
    body = lesson(
        ["Eine <b>Potenz</b> ist eine kurze Schreibweise für ein Produkt gleicher Faktoren: 2 %s 2 %s 2 = 2³." % (MAL, MAL),
         "Die große Zahl heißt <b>Basis</b>, die kleine hochgestellte Zahl heißt <b>Exponent</b>. Der Exponent sagt, wie oft die Basis multipliziert wird.",
         "Quadratzahlen sind Zahlen wie 1, 4, 9, 16, 25: n² = n %s n." % MAL,
         "Zehnerpotenzen: 10⁶ ist eine 1 mit 6 Nullen. Reihenfolge: Klammer, dann Potenz, dann Punkt vor Strich."],
        [example("2⁵", ["2 %s 2 %s 2 %s 2 %s 2" % (MAL, MAL, MAL, MAL)], "32"),
         example("3 + 4²", ["4² = 16", "3 + 16"], "19")],
        [["2³ = 6", "2³ = 2 %s 2 %s 2 = 8" % (MAL, MAL)],
         ["10⁶ = 100 000", "6 Nullen: 1 000 000"],
         ["3 %s 4² = 144" % MAL, "Potenz zuerst: 3 %s 16 = 48" % MAL]],
        extra=table(["n", "n²", "n³"], [["2", "4", "8"], ["3", "9", "27"], ["4", "16", "64"], ["5", "25", "125"], ["10", "100", "1000"]]))
    faq = [
        {"q": "Was ist der Unterschied zwischen 2³ und 3²?", "a": "2³ = 2 · 2 · 2 = 8, aber 3² = 3 · 3 = 9. Basis und Exponent darf man nicht vertauschen."},
        {"q": "Welche Quadratzahlen sollte man auswendig kennen?", "a": "Mindestens die Quadratzahlen von 1² bis 20²: 1, 4, 9, 16, 25, 36, 49, 64, 81, 100, 121, 144, 169, 196, 225, 256, 289, 324, 361, 400."},
        {"q": "Wozu braucht man Zehnerpotenzen?", "a": "Um sehr große Zahlen kurz zu schreiben, zum Beispiel 10⁹ für eine Milliarde."},
        {"q": "Wird die Potenz vor der Multiplikation gerechnet?", "a": "Ja. Die Reihenfolge ist: Klammern, Potenzen, Punktrechnung, Strichrechnung."},
    ]
    make_unit(R, "potenzen-und-quadratzahlen", "Z",
              "Die Schülerinnen und Schüler verwenden die Potenzschreibweise mit natürlichen Exponenten, kennen Quadratzahlen und Zehnerpotenzen und berechnen Terme mit Potenzen unter Beachtung der Vorrangregeln (Zusammenfassung).",
              "Potenzen und Quadratzahlen",
              "Potenzen Klasse 5 – Arbeitsblätter mit Lösungen",
              "Potenzen",
              "Potenzen und Quadratzahlen für Klasse 5: Basis und Exponent, Quadratzahlen bis 20², Zehnerpotenzen, Potenzen berechnen und Reihenfolge der Rechenarten. 100 Übungsaufgaben mit Lösungen, kostenlos.",
              "2³ = 2 · 2 · 2 = 8",
              "Basis unten, Exponent oben.",
              body, faq, sets, 7, grade="klasse-5")


if __name__ == "__main__":
    main()
