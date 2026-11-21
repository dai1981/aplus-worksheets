# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 8: Binomische Formeln（Leitidee Funktionaler Zusammenhang, Sek I）
  python3 tools/gen_de_mathe_k8_binomische_formeln.py
1. (a + b)² = a² + 2ab + b², 2. (a − b)² = a² − 2ab + b², 3. (a + b)(a − b) = a² − b².
Mit Faktoren (2x + 3)², rückwärts faktorisieren, fehlende Glieder ergänzen, geschickt rechnen (51², 49 · 51).
Fehler: (x + 3)² = x² + 9, Mittelglied ab statt 2ab, (x − 3)² = x² − 6x − 9, (2x)² = 2x².
"""
import random
from de_common import lesson, example, make_unit, mix, MAL, num
from de_k8 import mcq, expr

R = random.Random(49804)
Q = "x²"


def sq(t):
    return "(%s)²" % t


def erste_zweite():
    a = R.randint(1, 12)
    s = R.choice([1, -1])
    v = R.choice(["x", "a", "y", "b"])
    v2 = v + "²"
    t = expr([(1, v), (s * a, "")])
    res = [(1, v2), (2 * s * a, v), (a * a, "")]
    return mcq("Multipliziere aus: %s" % sq(t), expr(res),
               [expr([(1, v2), (a * a, "")]), expr([(1, v2), (s * a, v), (a * a, "")]), expr([(1, v2), (2 * s * a, v), (-a * a, "")])],
               "%s: %s² %s 2 %s %s %s %d + %d² = <b>%s</b>." % ("1. binomische Formel" if s > 0 else "2. binomische Formel", v, "+" if s > 0 else "−", MAL, v, MAL, a, a, expr(res)))


def dritte():
    a = R.randint(1, 15)
    v = R.choice(["x", "a", "y", "m"])
    order = R.choice([0, 1])
    t1, t2 = expr([(1, v), (a, "")]), expr([(1, v), (-a, "")])
    q = "(%s)(%s)" % ((t1, t2) if order == 0 else (t2, t1))
    res = [(1, v + "²"), (-a * a, "")]
    return mcq("Multipliziere aus: %s" % q, expr(res), [expr([(1, v + "²"), (a * a, "")]), expr([(1, v + "²"), (-2 * a, v), (-a * a, "")]), expr([(1, v + "²"), (-2 * a, "")])],
               "3. binomische Formel: %s² − %d² = <b>%s</b>. Die gemischten Glieder heben sich auf." % (v, a, expr(res)))


def faktoren():
    p = R.randint(2, 6)
    a = R.randint(1, 9)
    kind = R.choice(["plus", "minus", "drei", "zwei"])
    if kind in ("plus", "minus"):
        s = 1 if kind == "plus" else -1
        res = [(p * p, Q), (2 * s * p * a, "x"), (a * a, "")]
        return mcq("Multipliziere aus: %s" % sq(expr([(p, "x"), (s * a, "")])), expr(res),
                   [expr([(p, Q), (2 * s * p * a, "x"), (a * a, "")]), expr([(p * p, Q), (s * p * a, "x"), (a * a, "")]), expr([(p * p, Q), (a * a, "")])],
                   "(%dx)² = %d%s, 2 %s %dx %s %d = %s, %d² = %d. <b>%s</b>" % (p, p * p, Q, MAL, p, MAL, a, expr([(2 * p * a, "x")]), a, a * a, expr(res)))
    if kind == "drei":
        res = [(p * p, Q), (-a * a, "")]
        return mcq("Multipliziere aus: (%s)(%s)" % (expr([(p, "x"), (a, "")]), expr([(p, "x"), (-a, "")])), expr(res),
                   [expr([(p, Q), (-a * a, "")]), expr([(p * p, Q), (a * a, "")]), expr([(p * p, Q), (-2 * a, "")])],
                   "(%dx)² − %d² = <b>%s</b>." % (p, a, expr(res)))
    q = R.randint(2, 5)
    s = R.choice([1, -1])
    res = [(p * p, "a²"), (2 * s * p * q, "ab"), (q * q, "b²")]
    return mcq("Multipliziere aus: %s" % sq(expr([(p, "a"), (s * q, "b")])), expr(res),
               [expr([(p * p, "a²"), (q * q, "b²")]), expr([(p * p, "a²"), (s * p * q, "ab"), (q * q, "b²")]), expr([(p, "a²"), (2 * s * p * q, "ab"), (q, "b²")])],
               "(%da)² %s 2 %s %da %s %db + (%db)² = <b>%s</b>." % (p, "+" if s > 0 else "−", MAL, p, MAL, q, q, expr(res)))


def rueckwaerts():
    a = R.randint(1, 12)
    kind = R.choice(["plus", "minus", "drei", "luecke", "luecke2"])
    if kind == "plus":
        return mcq("Schreibe als Produkt: %s" % expr([(1, Q), (2 * a, "x"), (a * a, "")]), sq("x + %d" % a),
                   [sq("x + %d" % (2 * a)), "(x + %d)(x − %d)" % (a, a), sq("x − %d" % a)],
                   "%d = %d² und %dx = 2 %s x %s %d. 1. binomische Formel: <b>%s</b>." % (a * a, a, 2 * a, MAL, MAL, a, sq("x + %d" % a)))
    if kind == "minus":
        return mcq("Schreibe als Produkt: %s" % expr([(1, Q), (-2 * a, "x"), (a * a, "")]), sq("x − %d" % a),
                   [sq("x + %d" % a), "(x + %d)(x − %d)" % (a, a), sq("x − %d" % (2 * a))],
                   "Mittelglied negativ: 2. binomische Formel, <b>%s</b>." % sq("x − %d" % a))
    if kind == "drei":
        p = R.choice([1, 1, 2, 3])
        t = expr([(p * p, Q), (-a * a, "")])
        f = expr([(p, "x")])
        return mcq("Schreibe als Produkt: %s" % t, "(%s + %d)(%s − %d)" % (f, a, f, a),
                   [sq("%s − %d" % (f, a)), "(%s + %d)(%s − %d)" % (f, a * a, f, a * a) if a > 1 else sq("%s + %d" % (f, a)), sq("%s + %d" % (f, a))],
                   "Differenz zweier Quadrate: %s = (%s)² − %d². 3. binomische Formel: <b>(%s + %d)(%s − %d)</b>." % (t, f, a, f, a, f, a))
    if kind == "luecke":
        return mcq("Ergänze die Lücke: x² + ▢ + %d = (x + %d)²" % (a * a, a), "%dx" % (2 * a), ["%dx" % a, "%dx" % (a * a), "%d" % (2 * a)],
                   "Das Mittelglied ist 2 %s x %s %d = <b>%dx</b>." % (MAL, MAL, a, 2 * a))
    return mcq("Ergänze die Lücke: x² − %dx + ▢ = (x − %d)²" % (2 * a, a), str(a * a), [str(2 * a), str(a), "−%d" % (a * a)],
               "Das letzte Glied ist %d² = <b>%d</b>." % (a, a * a))


def geschickt():
    kind = R.choice(["plus", "minus", "drei", "flaeche"])
    if kind == "plus":
        b = R.choice([20, 30, 40, 50, 60, 70, 80, 90, 100])
        c = R.randint(1, 3)
        n = b + c
        return mcq("Berechne geschickt mit einer binomischen Formel: %d²" % n, num(n * n), [num(b * b + c * c), num(b * b + b * c + c * c), num(n * n + 10)],
                   "(%d + %d)² = %s + %d + %d = <b>%s</b>." % (b, c, num(b * b), 2 * b * c, c * c, num(n * n)))
    if kind == "minus":
        b = R.choice([20, 30, 40, 50, 60, 70, 80, 90, 100])
        c = R.randint(1, 3)
        n = b - c
        return mcq("Berechne geschickt mit einer binomischen Formel: %d²" % n, num(n * n), [num(b * b - c * c), num(b * b - 2 * b * c - c * c), num(n * n + 2 * c)],
                   "(%d − %d)² = %s − %d + %d = <b>%s</b>." % (b, c, num(b * b), 2 * b * c, c * c, num(n * n)))
    if kind == "drei":
        b = R.choice([20, 30, 40, 50, 60, 70, 80, 90, 100])
        c = R.randint(1, 4)
        return mcq("Berechne geschickt: %d %s %d" % (b - c, MAL, b + c), num(b * b - c * c), [num(b * b + c * c), num(b * b), num(b * b - 2 * c)],
                   "(%d − %d)(%d + %d) = %s − %d = <b>%s</b>." % (b, c, b, c, num(b * b), c * c, num(b * b - c * c)))
    a = R.randint(1, 6)
    x = R.randint(3, 9)
    return mcq("Ein Quadrat mit der Seite x wird an jeder Seite um %d cm verlängert. Um wie viel wächst der Flächeninhalt (als Term)?" % a, expr([(2 * a, "x"), (a * a, "")]) + " cm²",
               [expr([(a * a, "")]) + " cm²", expr([(a, "x"), (a * a, "")]) + " cm²", expr([(4 * a, "")]) + " cm²"],
               "(x + %d)² − x² = x² + %dx + %d − x² = <b>%s cm²</b>." % (a, 2 * a, a * a, expr([(2 * a, "x"), (a * a, "")])))


def main():
    seen = set()
    sets = [
        ("1. und 2. binomische Formel", mix(R, seen, [(erste_zweite, 20)])),
        ("3. binomische Formel", mix(R, seen, [(dritte, 14), (erste_zweite, 6)])),
        ("Formeln mit Faktoren", mix(R, seen, [(faktoren, 20)])),
        ("Rückwärts: Faktorisieren", mix(R, seen, [(rueckwaerts, 20)])),
        ("Geschickt rechnen", mix(R, seen, [(geschickt, 20)])),
    ]
    body = lesson(
        ["<b>1. binomische Formel</b>: (a + b)² = a² + 2ab + b²",
         "<b>2. binomische Formel</b>: (a − b)² = a² − 2ab + b²",
         "<b>3. binomische Formel</b>: (a + b)(a − b) = a² − b²",
         "Das Mittelglied 2ab ist doppelt so groß wie das Produkt der beiden Summanden. Rückwärts gelesen helfen die Formeln beim Faktorisieren und beim Kopfrechnen."],
        [example("(x + 5)²", ["x² + 2 %s x %s 5 + 5²" % (MAL, MAL)], "x² + 10x + 25"),
         example("(3x − 2)²", ["9x² − 12x + 4"], "9x² − 12x + 4"),
         example("49 %s 51" % MAL, ["(50 − 1)(50 + 1) = 2500 − 1"], "2499")],
        [["(x + 3)² = x² + 9", "Mittelglied: x² + 6x + 9"],
         ["(x − 3)² = x² − 6x − 9", "b² ist immer positiv: x² − 6x + 9"],
         ["(2x)² = 2x²", "Auch die Zahl quadrieren: 4x²"]])
    faq = [
        {"q": "Wie lauten die drei binomischen Formeln?", "a": "(a + b)² = a² + 2ab + b², (a − b)² = a² − 2ab + b² und (a + b)(a − b) = a² − b²."},
        {"q": "Warum ist (x + 3)² nicht x² + 9?", "a": "(x + 3)² = (x + 3)(x + 3). Beim Ausmultiplizieren entstehen zweimal 3x, also das Mittelglied 6x."},
        {"q": "Wie erkenne ich eine binomische Formel rückwärts?", "a": "Zwei Quadrate und ein Mittelglied 2ab sprechen für die 1. oder 2. Formel. Eine Differenz zweier Quadrate gehört zur 3. Formel."},
        {"q": "Wozu braucht man die binomischen Formeln?", "a": "Zum schnellen Ausmultiplizieren, zum Faktorisieren, für Kopfrechnen wie 49 · 51 und später für quadratische Gleichungen."},
    ]
    make_unit(R, "binomische-formeln", "F",
              "Die Schülerinnen und Schüler wenden die drei binomischen Formeln zum Ausmultiplizieren und Faktorisieren an, auch mit Faktoren, und nutzen sie zum geschickten Rechnen (Zusammenfassung).",
              "Binomische Formeln",
              "Binomische Formeln Klasse 8 – Aufgaben mit Lösungen zum Ausdrucken",
              "Binomische Formeln",
              "Binomische Formeln für Klasse 8: 1., 2. und 3. binomische Formel, mit Faktoren, rückwärts faktorisieren und geschickt rechnen. 100 Aufgaben mit Lösungen, kostenlos.",
              "(a + b)² = a² + 2ab + b²",
              "(a − b)² = a² − 2ab + b² und (a + b)(a − b) = a² − b²",
              body, faq, sets, 4, grade="klasse-8")


if __name__ == "__main__":
    main()
