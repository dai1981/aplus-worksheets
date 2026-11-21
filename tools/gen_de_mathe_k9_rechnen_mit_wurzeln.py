# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 9: Rechnen mit Wurzeln（Leitidee Zahl und Operation, Sek I）
  python3 tools/gen_de_mathe_k9_rechnen_mit_wurzeln.py
Wurzeln multiplizieren und dividieren, teilweise Wurzelziehen (√12 = 2√3), gleichartige Wurzeln addieren, Nenner rational machen,
n-te Wurzeln, Wurzeln mit Variablen, Sachaufgaben (Diagonale, Seitenlänge, Fallzeit).
Fehler: √a + √b = √(a + b), √12 = 6√2 (falscher Faktor), 2√3 + 3√2 = 5√5, beim Rationalmachen nur den Nenner erweitert.
"""
import random, math
from fractions import Fraction as Fr
from de_common import lesson, example, make_unit, mix, MAL, num, fr
from de_k9 import mcq, zahl, zr

R = random.Random(49902)
G = ":"
W = "√"


def w(x):
    x = str(x)
    return W + ("(%s)" % x if (" " in x or "/" in x) else x)


def kw(k, r):
    """k√r vereinfacht dargestellt"""
    if r == 1:
        return num(k)
    return ("" if k == 1 else num(k)) + w(r)


def vereinf(n):
    k, r = 1, n
    for p in range(int(math.isqrt(n)), 1, -1):
        if n % (p * p) == 0:
            return p, n // (p * p)
    return 1, n


def multdiv():
    kind = R.choice(["mal", "mal", "geteilt", "quadrat"])
    if kind == "mal":
        a, b = R.choice([(2, 8), (3, 12), (2, 18), (5, 20), (3, 27), (2, 32), (6, 24), (5, 45), (7, 28), (2, 50), (8, 18), (3, 48)])
        if R.random() < 0.5:
            a, b = b, a
        p = math.isqrt(a * b)
        return mcq("Berechne: %s %s %s" % (w(a), MAL, w(b)), str(p), [w(a + b), str(a * b), kw(1, a * b) if math.isqrt(a * b) ** 2 != a * b else str(p + 1)],
                   "%s %s %s = %s = <b>%d</b>." % (w(a), MAL, w(b), w(a * b), p))
    if kind == "geteilt":
        b = R.choice([2, 3, 5, 6, 7])
        q = R.randint(2, 9)
        a = b * q * q
        return mcq("Berechne: %s %s %s" % (w(a), G, w(b)), str(q), [w(a - b), str(q * q), dz_(Fr(a, b) / 2)],
                   "%s %s %s = %s = <b>%d</b>." % (w(a), G, w(b), w(a // b), q))
    a = R.choice([2, 3, 5, 7, 11, 13])
    k = R.randint(2, 6)
    return mcq("Berechne: (%s)²" % kw(k, a), str(k * k * a), [str(k * a), str(k * k + a), str(2 * k * a)],
               "(%d%s)² = %d² %s %s² = %d %s %d = <b>%d</b>." % (k, w(a), k, MAL, w(a), k * k, MAL, a, k * k * a))


def dz_(v):
    return zahl(v)


def teilweise():
    k = R.randint(2, 7)
    r = R.choice([2, 3, 5, 6, 7, 10, 11])
    n = k * k * r
    if n > 300:
        return None
    return mcq("Ziehe teilweise die Wurzel: %s" % w(n), kw(k, r), ["%d%s" % (r, w(k * k)), "%d%s" % (k * k, w(r)), "%d%s" % (k, w(n // k))] if (n // k) != r else ["%d%s" % (r, w(k * k)), "%d%s" % (k * k, w(r)), "%d%s" % (k + 1, w(r))],
                   "%d = %d %s %d. %s = %s %s %s = <b>%s</b>." % (n, k * k, MAL, r, w(n), w(k * k), MAL, w(r), kw(k, r)))


def addieren():
    kind = R.choice(["gleich", "gleich", "erst", "nicht"])
    r = R.choice([2, 3, 5, 6, 7])
    if kind == "gleich":
        a, b = R.randint(1, 9), R.randint(1, 9)
        op = R.choice(["+", "−"])
        v = a + b if op == "+" else a - b
        if v <= 0:
            return None
        return mcq("Fasse zusammen: %s %s %s" % (kw(a, r), op, kw(b, r)), kw(v, r), ["%d%s" % (v, w(2 * r)), "%d%s" % (a * b, w(r)) if a * b != v else "%d%s" % (a + b + 1, w(r)), "%d" % v],
                   "Gleiche Wurzeln wie gleiche Variablen behandeln: %d %s %d = %d. <b>%s</b>" % (a, op, b, v, kw(v, r)))
    if kind == "erst":
        p, q = R.sample([2, 3, 4, 5], 2)
        n1, n2 = p * p * r, q * q * r
        if n1 > 200 or n2 > 200:
            return None
        return mcq("Fasse zusammen: %s + %s" % (w(n1), w(n2)), kw(p + q, r), [w(n1 + n2), kw(p * q, r), kw(p + q, 2 * r)],
                   "%s = %s und %s = %s. Zusammen <b>%s</b>." % (w(n1), kw(p, r), w(n2), kw(q, r), kw(p + q, r)))
    r2 = R.choice([v for v in [2, 3, 5, 7] if v != r])
    a, b = R.randint(2, 6), R.randint(2, 6)
    return mcq("Kann man %s + %s zu einer Wurzel zusammenfassen?" % (kw(a, r), kw(b, r2)), "Nein, die Radikanden %d und %d sind verschieden." % (r, r2),
               ["Ja: %s" % kw(a + b, r + r2), "Ja: %s" % kw(a * b, r * r2), "Ja: %s" % kw(a + b, r * r2)],
               "Nur Wurzeln mit gleichem Radikanden lassen sich zusammenfassen. <b>Nein</b>")


def rational():
    kind = R.choice(["einfach", "einfach", "faktor", "bruch"])
    r = R.choice([2, 3, 5, 6, 7, 10])
    if kind == "einfach":
        return mcq("Mache den Nenner rational: %s" % fr(1, w(r)), fr(w(r), r), [fr(1, r), w(r), fr(r, w(r))],
                   "Mit %s erweitern: %s = <b>%s</b>." % (w(r), fr(w(r), "%s %s %s" % (w(r), MAL, w(r))), fr(w(r), r)))
    if kind == "faktor":
        k = R.randint(1, 6) * r
        v = Fr(k, r)
        return mcq("Mache den Nenner rational und vereinfache: %s" % fr(k, w(r)), kw(int(v), r), [fr(k, r), kw(k, r), "%s%s" % (num(int(v) * r), w(r)) if int(v) * r != k else fr(k * k, r)],
                   "Mit %s erweitern: %s = <b>%s</b>." % (w(r), fr("%d%s" % (k, w(r)), r), kw(int(v), r)))
    a, b = R.randint(2, 9), R.choice([2, 3, 5])
    return mcq("Vereinfache: %s" % fr(w(a * a * b), w(b)), str(a), [str(a * b), str(a * a), w(a * a * b - b)],
               "%s = %s = <b>%d</b>." % (fr(w(a * a * b), w(b)), w(a * a), a))


def nte():
    kind = R.choice(["kubik", "kubik", "vier", "var", "betrag"])
    if kind == "kubik":
        n = R.randint(2, 10)
        neg = R.random() < 0.3
        v = -n if neg else n
        return mcq("Berechne: <sup>3</sup>%s" % w(("−" if neg else "") + num(n ** 3)), zahl(v), [zahl(-v), dz_(Fr(n ** 3, 3)) if (Fr(n ** 3, 3)).denominator == 1 else str(n + 1), "nicht definiert" if neg else str(n * n)],
                   "%s<sup>3</sup> = %s. <b>%s</b>" % (("(%s)" % zahl(v)) if neg else zahl(v), zahl(v ** 3), zahl(v)))
    if kind == "vier":
        n = R.choice([2, 3, 5, 10])
        return mcq("Berechne: <sup>4</sup>%s" % w(num(n ** 4)), str(n), [str(n * n), num(n ** 4 // 4), str(n + 1)],
                   "%d<sup>4</sup> = %s: <b>%d</b>." % (n, num(n ** 4), n))
    if kind == "var":
        k = R.randint(2, 5)
        e = R.choice([2, 4, 6])
        return mcq("Vereinfache für x ≥ 0: %s" % w("%dx<sup>%d</sup>" % (k * k, e)), "%dx%s" % (k, "<sup>%d</sup>" % (e // 2) if e // 2 > 1 else ""),
                   ["%dx<sup>%d</sup>" % (k * k, e // 2), "%dx<sup>%d</sup>" % (k, e) if e != 2 else "%dx" % (k * k), "%dx%s" % (k, "<sup>%d</sup>" % (e - 2) if e - 2 > 1 else "" if e - 2 == 1 else "") if e != 2 else "%d" % k],
                   "%s = %d und %s = x%s. <b>%dx%s</b>" % (w(k * k), k, w("x<sup>%d</sup>" % e), "<sup>%d</sup>" % (e // 2) if e // 2 > 1 else "", k, "<sup>%d</sup>" % (e // 2) if e // 2 > 1 else ""))
    a = R.randint(2, 9)
    return mcq("Berechne: %s" % w("(−%d)²" % a), str(a), ["−%d" % a, "nicht definiert", str(a * a)],
               "(−%d)² = %d, %s = <b>%d</b>. Allgemein: %s = |x|." % (a, a * a, w(a * a), a, w("x²")))


def sache():
    kind = R.choice(["diag", "seite", "fall", "flaeche", "kubik"])
    if kind == "diag":
        a = R.randint(2, 12)
        return mcq("Ein Quadrat hat die Seitenlänge %d cm. Seine Diagonale ist d = a %s %s. Wie lang ist sie (gerundet)?" % (a, MAL, w(2)), "%s cm" % zr(a * math.sqrt(2)),
                   ["%d cm" % (2 * a), "%s cm" % zr(a * a * math.sqrt(2)), "%s cm" % zr(math.sqrt(2 * a))],
                   "%d %s 1,414… ≈ <b>%s cm</b>. Exakt: %s cm." % (a, MAL, zr(a * math.sqrt(2)), kw(a, 2)))
    if kind == "seite":
        k, r = R.choice([(2, 2), (3, 2), (2, 3), (5, 2), (2, 5), (3, 3), (4, 2), (2, 7)])
        A = k * k * r
        return mcq("Ein Quadrat hat den Flächeninhalt %d cm². Wie lang ist eine Seite (exakt)?" % A, "%s cm" % kw(k, r), ["%d%s cm" % (r, w(k)), "%s cm" % dz_(Fr(A, 4)), "%d%s cm" % (k * k, w(r))],
                   "a = %s = %s = <b>%s cm</b>." % (w(A), "%s %s %s" % (w(k * k), MAL, w(r)), kw(k, r)))
    if kind == "fall":
        h = R.choice([20, 45, 80, 125, 180])
        t = math.sqrt(h / 5)
        return mcq("Ein Stein fällt aus %d m Höhe. Die Fallzeit ist t = %s (in s). Wie lange fällt er?" % (h, w("h %s 5" % G)), "%s s" % zr(t, 0),
                   ["%d s" % (h // 5), "%s s" % zr(math.sqrt(h), 1), "%s s" % zr(t * 2, 0)], "%s = %s = <b>%s s</b>." % (w("%d %s 5" % (h, G)), w(h // 5), zr(t, 0)))
    if kind == "flaeche":
        a, b = R.choice([(2, 8), (3, 12), (2, 18), (5, 20), (3, 27), (2, 32)])
        return mcq("Ein Rechteck hat die Seiten %s cm und %s cm. Wie groß ist sein Flächeninhalt?" % (w(a), w(b)), "%d cm²" % math.isqrt(a * b),
                   ["%s cm²" % w(a + b), "%d cm²" % (a * b), "%d cm²" % (a + b)],
                   "%s %s %s = %s = <b>%d cm²</b>." % (w(a), MAL, w(b), w(a * b), math.isqrt(a * b)))
    V = R.choice([8, 27, 64, 125, 216, 343, 512, 1000])
    return mcq("Ein Würfel hat das Volumen %s cm³. Wie lang ist eine Kante?" % num(V), "%d cm" % round(V ** (1 / 3)),
               ["%s cm" % dz_(Fr(V, 3)) if V % 3 == 0 else "%d cm" % (round(V ** (1 / 3)) + 1), "%s cm" % zr(math.sqrt(V)), "%s cm" % dz_(Fr(V, 6)) if V % 6 == 0 else "%d cm" % (round(V ** (1 / 3)) * 2)],
               "a = <sup>3</sup>%s = <b>%d cm</b>." % (w(num(V)), round(V ** (1 / 3))))


def main():
    seen = set()
    sets = [
        ("Multiplizieren und Dividieren", mix(R, seen, [(multdiv, 20)])),
        ("Teilweise Wurzelziehen", mix(R, seen, [(teilweise, 20)])),
        ("Wurzeln addieren", mix(R, seen, [(addieren, 20)])),
        ("Nenner rational machen und n-te Wurzeln", mix(R, seen, [(rational, 10), (nte, 10)])),
        ("Sachaufgaben", mix(R, seen, [(sache, 20)])),
    ]
    body = lesson(
        ["<b>Multiplizieren und Dividieren</b>: %s %s %s = %s und %s %s %s = %s (a, b ≥ 0)." % (w("a"), MAL, w("b"), w("a %s b" % MAL), w("a"), G, w("b"), w("a %s b" % G)),
         "<b>Teilweise Wurzelziehen</b>: Quadratzahl als Faktor suchen, z. B. %s = %s %s %s = %s." % (w(50), w(25), MAL, w(2), kw(5, 2)),
         "<b>Addieren</b> kann man nur Wurzeln mit gleichem Radikanden: 3%s + 4%s = 7%s. Aber %s + %s ≠ %s." % (w(2), w(2), w(2), w(9), w(16), w(25)),
         "<b>Nenner rational machen</b>: Zähler und Nenner mit der Wurzel erweitern."],
        [example("%s %s %s" % (w(3), MAL, w(12)), [w(36)], "6"),
         example(w(72), ["%s %s %s" % (w(36), MAL, w(2))], kw(6, 2)),
         example(fr(6, w(3)), [fr("6" + w(3), 3)], kw(2, 3))],
        [["%s + %s = %s" % (w(9), w(16), w(25)), "3 + 4 = 7, nur Produkte und Quotienten zusammenziehen"],
         ["%s = 4%s" % (w(12), w(3)), "12 = 4 %s 3, also %s" % (MAL, kw(2, 3))],
         ["2%s + 3%s = 5%s" % (w(3), w(2), w(5)), "Verschiedene Radikanden bleiben getrennt"]])
    faq = [
        {"q": "Welche Wurzelgesetze gibt es?", "a": "√a · √b = √(a · b) und √a : √b = √(a : b) für a, b ≥ 0. Für Summen gibt es kein solches Gesetz."},
        {"q": "Was heißt teilweise Wurzelziehen?", "a": "Man zerlegt den Radikanden in eine Quadratzahl und einen Rest: √18 = √9 · √2 = 3√2."},
        {"q": "Wie mache ich den Nenner rational?", "a": "Man erweitert mit der Wurzel im Nenner: 1/√2 = √2/2."},
        {"q": "Was ist eine n-te Wurzel?", "a": "Die Zahl, die n-mal mit sich selbst multipliziert den Radikanden ergibt, z. B. ³√27 = 3."},
    ]
    make_unit(R, "rechnen-mit-wurzeln", "Z",
              "Die Schülerinnen und Schüler wenden Rechengesetze für Quadratwurzeln an, ziehen teilweise die Wurzel, fassen Wurzelterme zusammen, machen Nenner rational und berechnen n-te Wurzeln (Zusammenfassung).",
              "Rechnen mit Wurzeln",
              "Wurzelgesetze Klasse 9 – teilweise Wurzelziehen, Nenner rational machen, Arbeitsblätter",
              "Wurzelgesetze",
              "Rechnen mit Wurzeln für Klasse 9: Wurzelgesetze, teilweise Wurzelziehen, Wurzeln addieren, Nenner rational machen, n-te Wurzeln und Sachaufgaben. 100 Aufgaben mit Lösungen, kostenlos.",
              "√a · √b = √(a · b)",
              "Addieren nur bei gleichem Radikanden.",
              body, faq, sets, 2, grade="klasse-9")


if __name__ == "__main__":
    main()
