# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 7: Terme aufstellen und umformen（Leitidee Funktionaler Zusammenhang, Sek I）
  python3 tools/gen_de_mathe_k7_terme_umformen.py
Terme aufstellen, gleichartige Terme zusammenfassen (mit Vorzeichen), Produkte vereinfachen (3a · 4b), ausmultiplizieren, Minusklammern auflösen, ausklammern, Termwerte mit negativen Zahlen.
Fehler: −(a − b) = −a − b, 3a · 4a = 12a statt 12a², beim Ausklammern einen Summanden vergessen, 2x + 3y = 5xy.
"""
import random
from de_common import lesson, example, make_unit, mix, Kids, MAL, table
from de_k6 import dz
from de_k7 import mcq

R = random.Random(49707)
KIDS = Kids(R)


def mono(k, v):
    if k == 0:
        return ""
    if v == "":
        return dz(k)
    if k == 1:
        return v
    if k == -1:
        return "−" + v
    return dz(k) + v


def poly(terms):
    """terms: [(k, v)] → Text mit Vorzeichen"""
    out = ""
    for k, v in terms:
        if k == 0:
            continue
        m = mono(abs(k), v)
        if not out:
            out = ("−" if k < 0 else "") + m
        else:
            out += (" − " if k < 0 else " + ") + m
    return out or "0"


def zusammen():
    v1, v2 = R.sample(["a", "b", "x", "y"], 2)
    a, b, c, d = [R.choice([-1, 1]) * R.randint(1, 9) for _ in range(4)]
    q = poly([(a, v1), (b, v2), (c, v1), (d, v2)])
    if a + c == 0 or b + d == 0:
        return None
    ans = poly([(a + c, v1), (b + d, v2)])
    return mcq("Fasse zusammen: %s" % q, ans, [poly([(a - c, v1), (b - d, v2)]), poly([(a + c + b + d, v1 + v2)]), poly([(abs(a) + abs(c), v1), (abs(b) + abs(d), v2)]) if poly([(abs(a) + abs(c), v1), (abs(b) + abs(d), v2)]) != ans else poly([(a + c, v1), (-(b + d), v2)])],
               "Nur gleichartige Terme mit ihren Vorzeichen: %s und %s. <b>%s</b>" % (poly([(a, v1), (c, v1)]), poly([(b, v2), (d, v2)]), ans))


def produkt():
    kind = R.choice(["verschieden", "gleich", "zahl"])
    a, b = R.choice([-1, 1]) * R.randint(2, 9), R.randint(2, 9)
    if kind == "verschieden":
        return mcq("Vereinfache: %s %s %s" % (mono(a, "a") if a > 0 else "(%s)" % mono(a, "a"), MAL, mono(b, "b")), mono(a * b, "ab"), [mono(a + b, "ab"), mono(-a * b, "ab"), mono(a * b, "a²b")],
                   "Zahlen multiplizieren, Variablen dahinter: %s %s %d = %s. <b>%s</b>" % (dz(a), MAL, b, dz(a * b), mono(a * b, "ab")))
    if kind == "gleich":
        return mcq("Vereinfache: %s %s %s" % (mono(a, "x") if a > 0 else "(%s)" % mono(a, "x"), MAL, mono(b, "x")), mono(a * b, "x²"), [mono(a * b, "x"), mono(a + b, "x²"), mono(a * b, "2x")],
                   "x %s x = x². %s %s %d = %s. <b>%s</b>" % (MAL, dz(a), MAL, b, dz(a * b), mono(a * b, "x²")))
    c = R.randint(2, 9)
    return mcq("Vereinfache: %d %s %s %s %d" % (c, MAL, mono(a, "y") if a > 0 else "(%s)" % mono(a, "y"), MAL, b), mono(a * b * c, "y"), [mono(a + b + c, "y"), mono(-a * b * c, "y"), mono(a * b * c, "y³")],
               "Alle Zahlen multiplizieren: %d %s %s %s %d = %s. <b>%s</b>" % (c, MAL, dz(a), MAL, b, dz(a * b * c), mono(a * b * c, "y")))


def ausmult():
    a = R.choice([-1, 1]) * R.randint(2, 9)
    b, c = R.choice([-1, 1]) * R.randint(1, 9), R.choice([-1, 1]) * R.randint(1, 9)
    v = R.choice(["x", "a", "y"])
    inner = poly([(b, v), (c, "")])
    q = "%s(%s)" % (dz(a) + " " + MAL + " " if a > 0 else "(" + dz(a) + ") " + MAL + " ", inner)
    ans = poly([(a * b, v), (a * c, "")])
    return mcq("Multipliziere aus: %s" % q, ans, [poly([(a * b, v), (c, "")]), poly([(a * b, v), (-a * c, "")]), poly([(a + b, v), (a + c, "")])],
               "Jeder Summand in der Klammer wird mit %s multipliziert: <b>%s</b>." % (dz(a), ans))


def minusklammer():
    v = R.choice(["x", "a", "b"])
    a, b, c = R.randint(2, 12), R.choice([-1, 1]) * R.randint(1, 9), R.choice([-1, 1]) * R.randint(1, 9)
    kind = R.choice(["minus", "plus", "zwei"])
    if kind == "minus":
        q = "%s − (%s)" % (poly([(a, v)]), poly([(b, v), (c, "")]))
        ans = poly([(a - b, v), (-c, "")])
        return mcq("Löse die Klammer auf und fasse zusammen: %s" % q, ans, [poly([(a - b, v), (c, "")]), poly([(a + b, v), (c, "")]), poly([(a + b, v), (-c, "")])],
                   "Minus vor der Klammer: alle Vorzeichen in der Klammer umdrehen. %s − %s %s %s = <b>%s</b>" % (poly([(a, v)]), "(%s)" % poly([(b, v)]) if b < 0 else poly([(b, v)]), "+" if -c > 0 else "−", dz(abs(c)), ans))
    if kind == "plus":
        q = "%s + (%s)" % (poly([(a, v)]), poly([(b, v), (c, "")]))
        ans = poly([(a + b, v), (c, "")])
        return mcq("Löse die Klammer auf und fasse zusammen: %s" % q, ans, [poly([(a - b, v), (-c, "")]), poly([(a + b, v), (-c, "")]), poly([(a * b, v), (c, "")])],
                   "Plus vor der Klammer: Die Klammer fällt einfach weg. <b>%s</b>" % ans)
    d = R.randint(2, 6)
    q = "%d(%s) − %s" % (d, poly([(1, v), (b, "")]), poly([(a, v)]))
    ans = poly([(d - a, v), (d * b, "")])
    return mcq("Vereinfache: %s" % q, ans, [poly([(d - a, v), (b, "")]), poly([(d + a, v), (d * b, "")]), poly([(1 - a, v), (d * b, "")])],
               "Ausmultiplizieren: %s. Zusammenfassen: <b>%s</b>." % (poly([(d, v), (d * b, "")]) + " − " + mono(a, v), ans))


def ausklammern():
    g = R.randint(2, 9)
    b, c = R.randint(1, 9), R.choice([-1, 1]) * R.randint(1, 9)
    v = R.choice(["x", "a", "y"])
    from math import gcd
    if gcd(b, abs(c)) != 1:
        return None
    q = poly([(g * b, v), (g * c, "")])
    ans = "%d(%s)" % (g, poly([(b, v), (c, "")]))
    return mcq("Klammere den größten gemeinsamen Faktor aus: %s" % q, ans, ["%d(%s)" % (g, poly([(b, v), (g * c, "")])), "%d(%s)" % (g * b, poly([(1, v), (c, "")])) if (g * c) % (g * b) == 0 else "%d(%s)" % (g, poly([(b, v), (-c, "")])), "%d%s(%s)" % (g, v, poly([(b, ""), (c, "")]))],
               "Beide Summanden durch %d teilen: <b>%s</b>. Probe durch Ausmultiplizieren." % (g, ans))


def wert():
    a, b, c = R.choice([-1, 1]) * R.randint(1, 6), R.choice([-1, 1]) * R.randint(1, 9), R.choice([-1, 1]) * R.randint(1, 9)
    x = R.choice([-1, 1]) * R.randint(1, 5)
    kind = R.choice(["quad", "lin", "zwei"])
    if kind == "quad":
        v = a * x * x + b * x + c
        t = poly([(a, "x²"), (b, "x"), (c, "")])
        return mcq("Berechne den Term %s für x = %s." % (t, dz(x)), dz(v), [dz(-a * x * x + b * x + c), dz(a * 2 * x + b * x + c), dz(a * x * x - b * x + c) if b * x else dz(v + 1)],
                   "x² = (%s)² = %d. %s = <b>%s</b>." % (dz(x), x * x, " ".join([dz(a * x * x), ("+ " + dz(b * x)) if b * x >= 0 else ("− " + dz(-b * x)), ("+ " + dz(c)) if c >= 0 else ("− " + dz(-c))]), dz(v)))
    if kind == "lin":
        v = a * x + c
        if v == 0:
            return None
        t = poly([(a, "x"), (c, "")])
        return mcq("Berechne den Term %s für x = %s." % (t, dz(x)), dz(v), [dz(-a * x + c), dz(a * x - c), dz(a + x + c)], "%s %s (%s) %s %s = <b>%s</b>." % (dz(a), MAL, dz(x), "+" if c > 0 else "−", dz(abs(c)), dz(v)))
    y = R.choice([-1, 1]) * R.randint(1, 5)
    v = a * x - b * y
    t = poly([(a, "x"), (-b, "y")])
    return mcq("Berechne den Term %s für x = %s und y = %s." % (t, dz(x), dz(y)), dz(v), [dz(a * x + b * y), dz(a * y - b * x) if a * y - b * x != v else dz(v + 1), dz(-v) if v else "1"],
               "Einsetzen: %s %s (%s) %s %s %s (%s) = <b>%s</b>." % (dz(a), MAL, dz(x), "−" if b > 0 else "+", dz(abs(b)), MAL, dz(y), dz(v)))


def aufstellen():
    p, er = KIDS.next()
    k = R.randrange(8)
    D = [("Der Umfang eines Rechtecks mit den Seiten a und b", "2a + 2b", ["ab", "a + b", "4ab"]),
         ("Der Flächeninhalt eines Rechtecks mit den Seiten 3x und 5", "15x", ["3x + 5", "8x", "15x²"]),
         ("Der Umfang eines Quadrats mit der Seite (x + 2)", "4x + 8", ["4x + 2", "x + 8", "(x + 2)²"]),
         ("Die Summe aus dem Doppelten einer Zahl x und 7", "2x + 7", ["2(x + 7)", "x² + 7", "7x + 2"]),
         ("Das Doppelte der Summe aus einer Zahl x und 7", "2(x + 7)", ["2x + 7", "x + 14 + x", "2 + x + 7"]),
         ("Die Differenz aus dem Dreifachen einer Zahl und 4", "3x − 4", ["4 − 3x", "3(x − 4)", "x − 12"]),
         ("Kosten für x Hefte zu 1,20 € und y Stifte zu 0,80 €", "1,2x + 0,8y", ["2xy", "(1,2 + 0,8)xy", "1,2y + 0,8x"]),
         ("Das Alter des Vaters ist 3 Jahre mehr als das Dreifache des Alters x seines Sohnes", "3x + 3", ["3(x + 3)", "x + 9", "3x"])]
    q, a, w = D[k]
    return mcq("Welcher Term beschreibt: %s?" % q, a, w, "<b>%s</b>." % a)


def main():
    seen = set()
    sets = [
        ("Zusammenfassen", mix(R, seen, [(zusammen, 14), (aufstellen, 6)])),
        ("Produkte vereinfachen", mix(R, seen, [(produkt, 20)])),
        ("Ausmultiplizieren und Minusklammern", mix(R, seen, [(ausmult, 10), (minusklammer, 10)])),
        ("Ausklammern", mix(R, seen, [(ausklammern, 16), (aufstellen, 2), (minusklammer, 2)])),
        ("Termwerte berechnen", mix(R, seen, [(wert, 20)])),
    ]
    body = lesson(
        ["Nur <b>gleichartige Terme</b> (gleiche Variablen mit gleichen Exponenten) darf man zusammenfassen: 5a − 8a = −3a, aber 2x + 3y bleibt.",
         "<b>Produkte</b>: Zahlen multiplizieren, Variablen dahinter schreiben: 3a %s 4b = 12ab, 2x %s 5x = 10x²." % (MAL, MAL),
         "<b>Ausmultiplizieren</b>: Jeder Summand in der Klammer wird mit dem Faktor multipliziert. <b>Ausklammern</b> ist der umgekehrte Weg.",
         "<b>Minus vor einer Klammer</b>: Die Klammer fällt weg und alle Vorzeichen darin drehen sich um: −(a − b) = −a + b."],
        [example("4x − (2x − 5)", ["4x − 2x + 5"], "2x + 5"),
         example("18x − 12 ausklammern", ["ggT 6", "6(3x − 2)"], "6(3x − 2)")],
        [["−(a − b) = −a − b", "Vorzeichen umdrehen: −a + b"],
         ["3x %s 4x = 12x" % MAL, "x %s x = x²: 12x²" % MAL],
         ["2x + 3y = 5xy", "Nicht gleichartig: 2x + 3y bleibt"]])
    faq = [
        {"q": "Was bedeutet Ausmultiplizieren?", "a": "Den Faktor vor der Klammer mit jedem Summanden in der Klammer multiplizieren: 3(x − 4) = 3x − 12."},
        {"q": "Wie löse ich eine Minusklammer auf?", "a": "Klammer weglassen und alle Vorzeichen in der Klammer umdrehen: 5 − (x − 2) = 5 − x + 2."},
        {"q": "Was ist Ausklammern?", "a": "Einen gemeinsamen Faktor vor die Klammer ziehen: 6x + 9 = 3(2x + 3)."},
        {"q": "Darf man 3a + 4b zusammenfassen?", "a": "Nein, nur gleichartige Terme mit derselben Variable."},
    ]
    make_unit(R, "terme-umformen", "F",
              "Die Schülerinnen und Schüler stellen Terme auf, fassen gleichartige Terme zusammen, vereinfachen Produkte, multiplizieren aus, lösen Minusklammern auf, klammern aus und berechnen Termwerte (Zusammenfassung).",
              "Terme aufstellen und umformen",
              "Terme umformen Klasse 7 – ausmultiplizieren und ausklammern, Arbeitsblätter",
              "Terme umformen",
              "Terme umformen für Klasse 7: zusammenfassen, Produkte, ausmultiplizieren, Minusklammern, ausklammern und Termwerte. 100 Aufgaben mit Lösungen, kostenlos.",
              "Minus vor der Klammer dreht alle Vorzeichen um.",
              "Nur gleichartige Terme zusammenfassen.",
              body, faq, sets, 7, grade="klasse-7")


if __name__ == "__main__":
    main()
