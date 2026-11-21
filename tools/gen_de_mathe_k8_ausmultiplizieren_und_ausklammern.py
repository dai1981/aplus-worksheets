# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 8: Ausmultiplizieren und Ausklammern（Leitidee Funktionaler Zusammenhang, Sek I）
  python3 tools/gen_de_mathe_k8_ausmultiplizieren_und_ausklammern.py
Produkte von Termen (3x · 4x = 12x²), Klammer mal Zahl/Variable, Summe mal Summe (x + a)(x + b), Ausklammern (gemeinsamer Faktor), Flächeninhalte mit Termen.
Fehler: 3x · 4x = 12x, nur den ersten Summanden multipliziert, (x + 3)(x + 2) = x² + 6, beim Ausklammern den Faktor ganz weggelassen.
"""
import random, math
from de_common import lesson, example, make_unit, mix, MAL
from de_k8 import mcq, expr, par

R = random.Random(49803)
Q = "x²"


def nz(lo=1, hi=9):
    return R.choice([-1, 1]) * R.randint(lo, hi)


def produkt():
    kind = R.choice(["xx", "xy", "zahl", "neg"])
    a, b = R.randint(2, 9), R.randint(2, 9)
    if kind == "xx":
        return mcq("Vereinfache: %dx %s %dx" % (a, MAL, b), "%d%s" % (a * b, Q), ["%dx" % (a * b), "%d%s" % (a + b, Q), "%dx" % (a + b)],
                   "Zahlen multiplizieren, x %s x = x²: <b>%d%s</b>." % (MAL, a * b, Q))
    if kind == "xy":
        return mcq("Vereinfache: %da %s %db" % (a, MAL, b), "%dab" % (a * b), ["%da + %db" % (a, b), "%dab" % (a + b), "%d%s" % (a * b, "a²")],
                   "%d %s %d = %d, a %s b = ab: <b>%dab</b>." % (a, MAL, b, a * b, MAL, a * b))
    if kind == "zahl":
        c = R.randint(2, 6)
        return mcq("Vereinfache: %d %s %dx %s x" % (c, MAL, a, MAL), "%d%s" % (c * a, Q), ["%dx" % (c * a), "%d%s" % (c + a, Q), "%d%s" % (c * a + 1, Q)],
                   "%d %s %d = %d, x %s x = x²: <b>%d%s</b>." % (c, MAL, a, c * a, MAL, c * a, Q))
    return mcq("Vereinfache: (−%dx) %s %dx" % (a, MAL, b), "−%d%s" % (a * b, Q), ["%d%s" % (a * b, Q), "−%dx" % (a * b), "−%d%s" % (a + b, Q)],
               "Minus mal plus ergibt minus: <b>−%d%s</b>." % (a * b, Q))


def klammer():
    kind = R.choice(["zahl", "var", "minus", "summe"])
    a, b = R.randint(2, 9), nz()
    if kind == "zahl":
        k = R.randint(2, 9)
        return mcq("Multipliziere aus: %d(%s)" % (k, expr([(a, "x"), (b, "")])), expr([(k * a, "x"), (k * b, "")]),
                   [expr([(k * a, "x"), (b, "")]), expr([(k + a, "x"), (k + b, "")]), expr([(k * a, "x"), (-k * b, "")])],
                   "Jeden Summanden mit %d multiplizieren: <b>%s</b>." % (k, expr([(k * a, "x"), (k * b, "")])))
    if kind == "var":
        k = R.randint(2, 6)
        return mcq("Multipliziere aus: %dx(%s)" % (k, expr([(a, "x"), (b, "")])), expr([(k * a, Q), (k * b, "x")]),
                   [expr([(k * a, "x"), (k * b, "")]), expr([(k * a, Q), (b, "")]), expr([(k * a, Q), (k * b, Q)])],
                   "%dx %s %dx = %d%s und %dx %s %s = %s. <b>%s</b>" % (k, MAL, a, k * a, Q, k, MAL, par(b), expr([(k * b, "x")]), expr([(k * a, Q), (k * b, "x")])))
    if kind == "minus":
        k = R.randint(2, 7)
        return mcq("Multipliziere aus: −%d(%s)" % (k, expr([(a, "x"), (b, "")])), expr([(-k * a, "x"), (-k * b, "")]),
                   [expr([(-k * a, "x"), (k * b, "")]), expr([(k * a, "x"), (k * b, "")]), expr([(-k * a, "x"), (b, "")])],
                   "Beide Vorzeichen in der Klammer drehen sich um: <b>%s</b>." % expr([(-k * a, "x"), (-k * b, "")]))
    c, d = R.randint(2, 6), nz()
    k = R.randint(2, 5)
    m = R.randint(2, 5)
    res = [(k * a + m * c, "x"), (k * b + m * d, "")]
    return mcq("Vereinfache: %d(%s) + %d(%s)" % (k, expr([(a, "x"), (b, "")]), m, expr([(c, "x"), (d, "")])), expr(res),
               [expr([(k * a + m * c, "x"), (b + d, "")]), expr([(k * a + c, "x"), (k * b + d, "")]), expr([(k * a + m * c, "x"), (k * b - m * d, "")])],
               "%s + %s = <b>%s</b>." % (expr([(k * a, "x"), (k * b, "")]), expr([(m * c, "x"), (m * d, "")]), expr(res)))


def summe():
    a, b = nz(1, 9), nz(1, 9)
    kind = R.choice(["einfach", "einfach", "faktor", "zwei"])
    if kind == "einfach":
        res = [(1, Q), (a + b, "x"), (a * b, "")]
        return mcq("Multipliziere aus: (%s)(%s)" % (expr([(1, "x"), (a, "")]), expr([(1, "x"), (b, "")])), expr(res),
                   [expr([(1, Q), (a * b, "")]), expr([(1, Q), (a * b, "x"), (a + b, "")]), expr([(1, Q), (a + b, "x"), (-a * b, "")]) if a * b else None],
                   "Jeder Summand mal jeder Summand: x² %s %s %s = <b>%s</b>." % (("+ " + expr([(b, "x")])) if b > 0 else ("− " + expr([(-b, "x")])), ("+ " + expr([(a, "x")])) if a > 0 else ("− " + expr([(-a, "x")])), ("+ " + expr([(a * b, "")])) if a * b > 0 else ("− " + expr([(-a * b, "")])), expr(res)))
    p, q = R.randint(2, 5), R.randint(2, 5)
    if kind == "faktor":
        res = [(p * q, Q), (p * b + a * q, "x"), (a * b, "")]
        return mcq("Multipliziere aus: (%s)(%s)" % (expr([(p, "x"), (a, "")]), expr([(q, "x"), (b, "")])), expr(res),
                   [expr([(p * q, Q), (a * b, "")]), expr([(p * q, Q), (p + q, "x"), (a * b, "")]), expr([(p + q, Q), (p * b + a * q, "x"), (a * b, "")])],
                   "%dx %s %dx = %d%s, dann die gemischten Produkte %s und %s, zum Schluss %s %s %s = %s. <b>%s</b>" % (p, MAL, q, p * q, Q, expr([(p * b, "x")]), expr([(a * q, "x")]), par(a), MAL, par(b), expr([(a * b, "")]), expr(res)))
    c = R.randint(2, 6)
    res = [(1, "ab"), (b, "a"), (c, "b"), (c * b, "")]
    return mcq("Multipliziere aus: (a + %d)(b %s %d)" % (c, "+" if b > 0 else "−", abs(b)), expr(res),
               [expr([(1, "ab"), (c * b, "")]), expr([(1, "ab"), (c, "a"), (b, "b"), (c * b, "")]), expr([(1, "a"), (1, "b"), (c + b, "")])],
               "a %s b + a %s %s + %d %s b + %d %s %s = <b>%s</b>." % (MAL, MAL, par(b), c, MAL, c, MAL, par(b), expr(res)))


def ausklammern():
    kind = R.choice(["zahl", "zahl", "var", "beides", "minus"])
    if kind == "zahl":
        k = R.randint(2, 9)
        a, b = R.randint(1, 9), nz()
        if math.gcd(a, abs(b)) != 1:
            return None
        t = expr([(k * a, "x"), (k * b, "")])
        return mcq("Klammere den größten gemeinsamen Faktor aus: %s" % t, "%d(%s)" % (k, expr([(a, "x"), (b, "")])),
                   ["%d(%s)" % (k, expr([(k * a, "x"), (b, "")])), "%d(%s)" % (k, expr([(a, "x"), (k * b, "")])), "%d(%s)" % (k, expr([(a, "x"), (-b, "")]))],
                   "%d ist in beiden Summanden enthalten: <b>%d(%s)</b>. Probe: ausmultiplizieren." % (k, k, expr([(a, "x"), (b, "")])))
    if kind == "var":
        a, b = R.randint(1, 9), nz()
        if math.gcd(a, abs(b)) != 1:
            return None
        t = expr([(a, Q), (b, "x")])
        return mcq("Klammere x aus: %s" % t, "x(%s)" % expr([(a, "x"), (b, "")]), ["x(%s)" % expr([(a, Q), (b, "")]), "x(%s)" % expr([(a, "x"), (b, "x")]), "x²(%s)" % expr([(a, ""), (b, "")])],
                   "x %s x = x², also <b>x(%s)</b>." % (MAL, expr([(a, "x"), (b, "")])))
    if kind == "beides":
        k = R.randint(2, 6)
        a, b = R.randint(1, 7), nz()
        if math.gcd(a, abs(b)) != 1:
            return None
        t = expr([(k * a, Q), (k * b, "x")])
        return mcq("Klammere so viel wie möglich aus: %s" % t, "%dx(%s)" % (k, expr([(a, "x"), (b, "")])),
                   ["%d(%s)" % (k, expr([(a, Q), (b, "x")])), "x(%s)" % expr([(k * a, "x"), (k * b, "")]), "%dx(%s)" % (k, expr([(a, Q), (b, "")]))],
                   "Gemeinsam sind %d und x: <b>%dx(%s)</b>." % (k, k, expr([(a, "x"), (b, "")])))
    k = R.randint(2, 8)
    a, b = R.randint(1, 9), R.randint(1, 9)
    if math.gcd(a, b) != 1:
        return None
    t = expr([(-k * a, "x"), (-k * b, "")])
    return mcq("Klammere −%d aus: %s" % (k, t), "−%d(%s)" % (k, expr([(a, "x"), (b, "")])),
               ["−%d(%s)" % (k, expr([(a, "x"), (-b, "")])), "−%d(%s)" % (k, expr([(-a, "x"), (-b, "")])), "%d(%s)" % (k, expr([(a, "x"), (b, "")]))],
               "Beim Ausklammern von −%d drehen sich die Vorzeichen um: <b>−%d(%s)</b>." % (k, k, expr([(a, "x"), (b, "")])))


def flaeche():
    from de_common import wrap, line, text, INK, GREEN, FILL
    a, b = R.randint(1, 8), R.randint(1, 8)
    kind = R.choice(["rechteck", "rechteck", "wert", "umfang"])
    if kind == "rechteck":
        s = ["<rect x='30' y='20' width='200' height='120' fill='%s' stroke='%s' stroke-width='2.5'/>" % (FILL, GREEN),
             text(130, 158, "x + %d" % a, 15), text(18, 84, "x + %d" % b, 15, anchor="end")]
        pic = wrap(250, 170, "".join(s), "Rechteck mit den Seiten x + %d und x + %d" % (a, b), lg=True)
        res = [(1, Q), (a + b, "x"), (a * b, "")]
        return mcq(pic + "Gib den Flächeninhalt des Rechtecks als Term ohne Klammern an.", expr(res),
                   [expr([(1, Q), (a * b, "")]), expr([(2, "x"), (a + b, "")]), expr([(4, "x"), (2 * (a + b), "")])],
                   "A = (x + %d)(x + %d) = <b>%s</b>." % (a, b, expr(res)))
    if kind == "umfang":
        return mcq("Ein Rechteck hat die Seiten x + %d und 2x + %d. Wie lautet der Umfang als Term?" % (a, b), expr([(6, "x"), (2 * (a + b), "")]),
                   [expr([(3, "x"), (a + b, "")]), expr([(2, Q), (a * 2 + b, "x"), (a * b, "")]), expr([(6, "x"), (a + b, "")])],
                   "u = 2 %s (x + %d + 2x + %d) = 2 %s (%s) = <b>%s</b>." % (MAL, a, b, MAL, expr([(3, "x"), (a + b, "")]), expr([(6, "x"), (2 * (a + b), "")])))
    x = R.randint(2, 9)
    v = (x + a) * (x + b)
    return mcq("Berechne den Flächeninhalt eines Rechtecks mit den Seiten x + %d und x + %d (in cm) für x = %d." % (a, b, x), "%d cm²" % v,
               ["%d cm²" % (x * x + a * b), "%d cm²" % (2 * (2 * x + a + b)), "%d cm²" % (v + x)],
               "(%d + %d) %s (%d + %d) = %d %s %d = <b>%d cm²</b>." % (x, a, MAL, x, b, x + a, MAL, x + b, v))


def main():
    seen = set()
    sets = [
        ("Produkte von Termen", mix(R, seen, [(produkt, 20)])),
        ("Klammern auflösen", mix(R, seen, [(klammer, 20)])),
        ("Summe mal Summe", mix(R, seen, [(summe, 20)])),
        ("Ausklammern", mix(R, seen, [(ausklammern, 20)])),
        ("Flächen mit Termen", mix(R, seen, [(flaeche, 14), (summe, 6)])),
    ]
    body = lesson(
        ["Beim <b>Ausmultiplizieren</b> wird jeder Summand in der Klammer mit dem Faktor davor multipliziert: 3(x + 4) = 3x + 12.",
         "<b>Summe mal Summe</b>: Jeder Summand der ersten Klammer wird mit jedem Summanden der zweiten Klammer multipliziert, dann fasst man zusammen.",
         "<b>Ausklammern</b> ist die Umkehrung: Den gemeinsamen Faktor vor die Klammer schreiben, z. B. 6x + 9 = 3(2x + 3).",
         "Gleiche Variablen werden beim Multiplizieren zur Potenz: x %s x = x²." % MAL],
        [example("(x + 3)(x − 5)", ["x² − 5x + 3x − 15"], "x² − 2x − 15"),
         example("4x² + 10x", ["gemeinsam: 2x"], "2x(2x + 5)")],
        [["3x %s 4x = 12x" % MAL, "x %s x = x², also 12x²" % MAL],
         ["(x + 3)(x + 2) = x² + 6", "Gemischte Produkte nicht vergessen: x² + 5x + 6"],
         ["6x + 3 = 3(2x)", "Die 1 bleibt stehen: 3(2x + 1)"]])
    faq = [
        {"q": "Wie multipliziert man zwei Klammern aus?", "a": "Jeder Summand der ersten Klammer wird mit jedem Summanden der zweiten multipliziert. Danach fasst man gleichartige Terme zusammen."},
        {"q": "Was bedeutet Ausklammern?", "a": "Man schreibt einen gemeinsamen Faktor aller Summanden vor eine Klammer. Das Ergebnis ist ein Produkt."},
        {"q": "Wie prüfe ich das Ausklammern?", "a": "Multipliziere das Ergebnis wieder aus. Es muss der Ausgangsterm herauskommen."},
        {"q": "Was passiert bei einem Minus vor der Klammer?", "a": "Alle Vorzeichen in der Klammer drehen sich beim Ausmultiplizieren um."},
    ]
    make_unit(R, "ausmultiplizieren-und-ausklammern", "F",
              "Die Schülerinnen und Schüler multiplizieren Terme und Klammern aus (auch Summe mal Summe), klammern gemeinsame Faktoren aus und beschreiben Flächeninhalte mit Termen (Zusammenfassung).",
              "Ausmultiplizieren und Ausklammern",
              "Ausmultiplizieren und Ausklammern Klasse 8 – Summe mal Summe, Arbeitsblätter",
              "Ausmultiplizieren",
              "Terme für Klasse 8: Produkte von Termen, Klammern auflösen, Summe mal Summe, Ausklammern und Flächen mit Termen. 100 Aufgaben mit Lösungen, kostenlos.",
              "Jeder Summand mal jeder Summand.",
              "Ausklammern ist die Umkehrung des Ausmultiplizierens.",
              body, faq, sets, 3, grade="klasse-8")


if __name__ == "__main__":
    main()
