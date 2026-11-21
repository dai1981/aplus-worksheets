# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 8: Bruchterme und Bruchgleichungen（Leitidee Funktionaler Zusammenhang, Sek I）
  python3 tools/gen_de_mathe_k8_bruchterme_und_bruchgleichungen.py
Definitionsmenge (Nenner ≠ 0), Termwerte, Bruchterme kürzen (auch mit binomischen Formeln), addieren und subtrahieren,
Bruchgleichungen lösen und die Lösung mit der Definitionsmenge prüfen, Sachaufgaben.
Fehler: Summanden gekürzt, Zähler und Nenner einzeln addiert, Definitionslücke als Lösung angegeben, mit dem Hauptnenner nur eine Seite multipliziert.
"""
import random
from fractions import Fraction as Fr
from de_common import lesson, example, make_unit, mix, MAL, fr
from de_k6 import bh, dz
from de_k8 import mcq, expr

R = random.Random(49815)
Q = "x²"


def zahl(v):
    v = Fr(v)
    return bh(v) if v.denominator != 1 else dz(v)


def lin(a, b):
    return expr([(a, "x"), (b, "")])


def Dtxt(*lk):
    lk = sorted(set(lk))
    return "D = ℚ ∖ {%s}" % "; ".join(zahl(v) for v in lk)


def defm():
    kind = R.choice(["eins", "eins", "zwei", "faktor", "keine"])
    if kind == "eins":
        a = R.choice([-1, 1]) * R.randint(1, 9)
        z = R.randint(1, 9)
        return mcq("Bestimme die Definitionsmenge von %s." % fr(z, lin(1, a)), Dtxt(-a), [Dtxt(a), Dtxt(0), "D = ℚ"],
                   "Der Nenner darf nicht 0 sein: %s = 0 für x = %s. <b>%s</b>" % (lin(1, a), zahl(-a), Dtxt(-a)))
    if kind == "zwei":
        a, b = R.sample(range(-8, 9), 2)
        if a == 0 or b == 0:
            return None
        return mcq("Bestimme die Definitionsmenge von %s + %s." % (fr(3, lin(1, a)), fr(5, lin(1, b))), Dtxt(-a, -b), [Dtxt(a, b), Dtxt(-a), Dtxt(-a, -b, 0)],
                   "Beide Nenner dürfen nicht 0 sein: x ≠ %s und x ≠ %s. <b>%s</b>" % (zahl(-a), zahl(-b), Dtxt(-a, -b)))
    if kind == "faktor":
        k = R.randint(2, 6)
        a = R.choice([-1, 1]) * R.randint(1, 12)
        if a % k:
            a = a * k
        return mcq("Bestimme die Definitionsmenge von %s." % fr("x", lin(k, a)), Dtxt(Fr(-a, k)), [Dtxt(-a), Dtxt(Fr(a, k)), Dtxt(0)],
                   "%s = 0 ergibt x = %s. <b>%s</b>" % (lin(k, a), zahl(Fr(-a, k)), Dtxt(Fr(-a, k))))
    c = R.randint(1, 9)
    return mcq("Bestimme die Definitionsmenge von %s." % fr("x + %d" % c, "x² + %d" % c), "D = ℚ", [Dtxt(-c), Dtxt(0), Dtxt(c)],
               "x² + %d ist immer mindestens %d, also nie 0. <b>D = ℚ</b>" % (c, c))


def kuerzen():
    kind = R.choice(["mono", "faktor", "binom", "binom2", "wert"])
    if kind == "mono":
        a, b = R.randint(2, 9), R.randint(2, 9)
        k = R.randint(2, 5)
        return mcq("Kürze so weit wie möglich: %s" % fr("%dx" % (k * a), "%d%s" % (k * b, Q)), fr(Fr(a, b).numerator, "%sx" % (Fr(a, b).denominator if Fr(a, b).denominator != 1 else "")),
                   [fr(a, "%dx" % b) if Fr(a, b).denominator != b else fr(a * k, "%dx" % b), fr("%dx" % Fr(a, b).numerator, Fr(a, b).denominator) if Fr(a, b).denominator != 1 else "%dx" % a, fr(a, "%d%s" % (b, Q))],
                   "Durch %dx kürzen: <b>%s</b>." % (k * __import__("math").gcd(a, b), fr(Fr(a, b).numerator, "%sx" % (Fr(a, b).denominator if Fr(a, b).denominator != 1 else ""))))
    if kind == "faktor":
        k = R.randint(2, 7)
        a = R.choice([-1, 1]) * R.randint(1, 9)
        return mcq("Kürze: %s" % fr(lin(k, k * a), "%d" % k), lin(1, a), [lin(1, k * a), lin(k, a), lin(k - 1, k * a - 1)],
                   "Erst ausklammern: %d(%s). Dann durch %d kürzen: <b>%s</b>. Summanden allein darf man nicht kürzen." % (k, lin(1, a), k, lin(1, a)))
    if kind == "binom":
        a = R.randint(1, 9)
        return mcq("Kürze: %s" % fr("x² − %d" % (a * a), lin(1, a)), lin(1, -a), [lin(1, a), "x − %d" % (a * a) if a > 1 else lin(1, -2), lin(1, a * a)],
                   "3. binomische Formel: x² − %d = (x + %d)(x − %d). Durch (x + %d) kürzen: <b>%s</b>." % (a * a, a, a, a, lin(1, -a)))
    if kind == "binom2":
        a = R.randint(1, 9)
        return mcq("Kürze: %s" % fr(expr([(1, Q), (2 * a, "x"), (a * a, "")]), lin(1, a)), lin(1, a), [lin(1, -a), lin(1, 2 * a), "x² + %d" % a],
                   "x² + %dx + %d = (x + %d)². Durch (x + %d) kürzen: <b>%s</b>." % (2 * a, a * a, a, a, lin(1, a)))
    a, b = R.randint(1, 9), R.choice([-1, 1]) * R.randint(1, 9)
    x = R.randint(-5, 8)
    if x + b == 0:
        return None
    v = Fr(a * x, x + b)
    return mcq("Berechne den Wert von %s für x = %s." % (fr("%dx" % a, lin(1, b)), zahl(x)), zahl(v), [zahl(Fr(a * x + 1, x + b)) if Fr(a * x + 1, x + b) != v else zahl(v + 1), zahl(Fr(a, 1 + b)) if 1 + b and Fr(a, 1 + b) != v else zahl(v * 2) if v else "1", zahl(-v) if v else "2"],
               "%s = %s = <b>%s</b>." % (fr("%d %s %s" % (a, MAL, "(%s)" % zahl(x) if x < 0 else zahl(x)), "%s %s %d" % (zahl(x), "+" if b > 0 else "−", abs(b))), fr(zahl(a * x), zahl(x + b)), zahl(v)))


def addieren():
    kind = R.choice(["gleich", "gleich", "vielfach", "verschieden", "minus"])
    if kind == "gleich":
        a, b = R.randint(1, 9), R.randint(1, 9)
        return mcq("Fasse zusammen: %s + %s" % (fr(a, "x"), fr(b, "x")), fr(a + b, "x"), [fr(a + b, "2x"), fr(a * b, "x"), fr(a + b, Q)],
                   "Gleicher Nenner: Zähler addieren, Nenner bleibt. <b>%s</b>" % fr(a + b, "x"))
    if kind == "minus":
        a, b = R.randint(5, 15), R.randint(1, 4)
        c = R.randint(1, 9)
        return mcq("Fasse zusammen: %s − %s" % (fr("%dx" % a, lin(1, c)), fr("%dx" % b, lin(1, c))), fr("%dx" % (a - b), lin(1, c)), [fr("%dx" % (a - b), "0"), fr("%dx" % (a + b), lin(1, c)), fr("%dx" % (a - b), lin(2, 2 * c))],
                   "Gleicher Nenner %s: <b>%s</b>." % (lin(1, c), fr("%dx" % (a - b), lin(1, c))))
    if kind == "vielfach":
        a, b = R.randint(1, 9), R.randint(1, 9)
        k = R.choice([2, 3, 4])
        return mcq("Fasse zusammen: %s + %s" % (fr(a, "x"), fr(b, "%dx" % k)), fr(k * a + b, "%dx" % k), [fr(a + b, "%dx" % (k + 1)), fr(a + b, "%dx" % k), fr(k * a + b, "%d%s" % (k, Q))],
                   "Hauptnenner %dx: %s + %s = <b>%s</b>." % (k, fr(k * a, "%dx" % k), fr(b, "%dx" % k), fr(k * a + b, "%dx" % k)))
    a, b = R.randint(1, 6), R.randint(1, 6)
    p = R.randint(2, 9)
    if a >= p or __import__("math").gcd(a, p) != 1:
        return None
    return mcq("Fasse zusammen: %s + %s" % (fr(a, p), fr(b, "x")), fr(lin(a, b * p), "%dx" % p), [fr(a + b, "%d + x" % p), fr(a + b, "%dx" % p), fr(lin(a, b), "%dx" % p)],
               "Hauptnenner %dx: %s + %s = <b>%s</b>." % (p, fr("%s" % lin(a, 0), "%dx" % p), fr(b * p, "%dx" % p), fr(lin(a, b * p), "%dx" % p)))


def gleichung():
    kind = R.choice(["einfach", "klammer", "beide", "luecke", "klammer"])
    if kind == "einfach":
        x = R.choice([-1, 1]) * R.randint(1, 9)
        k = R.randint(2, 8)
        a = k * x
        return mcq("Löse: %s = %d" % (fr(zahl(a), "x"), k), "x = %s" % zahl(x), ["x = %s" % zahl(a * k), "x = %s" % zahl(Fr(k, a)), "x = %s" % zahl(a - k)],
                   "Mal x: %s = %dx. Durch %d: <b>x = %s</b>. Probe: %s = %d." % (zahl(a), k, k, zahl(x), fr(zahl(a), zahl(x)), k))
    if kind == "klammer":
        x = R.randint(-6, 9)
        c = R.choice([-1, 1]) * R.randint(1, 6)
        if x + c == 0:
            return None
        k = R.randint(2, 6)
        a = k * (x + c)
        if a == 0:
            return None
        return mcq("Löse: %s = %d" % (fr(zahl(a), lin(1, c)), k), "x = %s" % zahl(x), ["x = %s" % zahl(Fr(a, k) + c), "x = %s" % zahl(Fr(a, k)) if Fr(a, k) != x else "x = %s" % zahl(x + 1), "x = %s" % zahl(-c)],
                   "Mal (%s): %s = %d(%s), %s = %s, x = %s. %s ist in D. <b>x = %s</b>" % (lin(1, c), zahl(a), k, lin(1, c), zahl(a), lin(k, k * c), zahl(x), zahl(x), zahl(x)))
    if kind == "beide":
        x = R.randint(1, 12)
        a, b = R.randint(2, 9), R.randint(2, 9)
        if a == b:
            return None
        # a/x = b/(x + d) → a(x+d) = b x → x = a d / (b - a)
        d = R.randint(1, 6)
        xv = Fr(a * d, b - a)
        if xv.denominator != 1 or xv == 0 or xv + d == 0:
            return None
        return mcq("Löse: %s = %s" % (fr(a, "x"), fr(b, lin(1, d))), "x = %s" % zahl(xv), ["x = %s" % zahl(-xv), "x = %s" % zahl(Fr(b * d, a - b)) if Fr(b * d, a - b) != xv else "x = %s" % zahl(xv + 1), "x = %s" % zahl(Fr(a * d, b))],
                   "Über Kreuz multiplizieren: %d(%s) = %dx, %s = %dx, %s = %d, <b>x = %s</b>." % (a, lin(1, d), b, lin(a, a * d), b, lin(b - a, 0), a * d, zahl(xv)))
    c = R.randint(1, 6)
    return mcq("Löse: %s = %s" % (fr("x", lin(1, -c)), fr(c, lin(1, -c))), "keine Lösung, denn x = %d ist nicht in D" % c,
               ["x = %d" % c, "x = 0", "jede Zahl ist Lösung"],
               "Mal (x − %d): x = %d. Aber für x = %d ist der Nenner 0. %s. <b>keine Lösung</b>" % (c, c, c, Dtxt(c)))


def sache():
    kind = R.choice(["kehr", "teil", "zeit", "durchschnitt"])
    if kind == "kehr":
        x = R.choice([2, 3, 4, 5, 6, 8, 10])
        k = R.choice([1, 2, 3])
        v = Fr(1, x) + k
        return mcq("Addiert man zum Kehrwert einer Zahl %d, erhält man %s. Wie heißt die Zahl?" % (k, bh(v, True)), str(x), [bh(v - k) if v - k != x else str(x + 1), str(x + k), bh(1 / v)],
                   "%s + %d = %s, also %s = %s und <b>x = %d</b>." % (fr(1, "x"), k, bh(v, True), fr(1, "x"), bh(Fr(1, x)), x))
    if kind == "teil":
        x = R.choice([2, 3, 4, 5, 6, 8, 12])
        n = x * R.randint(2, 8)
        return mcq("Wenn man %d durch eine Zahl teilt, erhält man %d. Wie heißt die Zahl?" % (n, n // x), str(x), [str(n * (n // x)), str(n - n // x), bh(Fr(n // x, n))],
                   "%s = %d, also %d = %dx und <b>x = %d</b>." % (fr(n, "x"), n // x, n, n // x, x))
    if kind == "zeit":
        s = R.choice([120, 150, 180, 240, 300])
        v = R.choice([v for v in (40, 50, 60, 75, 80, 100, 120) if s % v == 0])
        return mcq("Für eine Strecke von %d km braucht ein Zug %d Stunden. Gesucht ist die Geschwindigkeit v aus %s = %d. Wie groß ist v?" % (s, s // v, fr(s, "v"), s // v), "%d km/h" % v,
                   ["%d km/h" % (s * (s // v)), "%d km/h" % (s - s // v), "%s km/h" % bh(Fr(s // v, s))], "%d = %d %s v, <b>v = %d km/h</b>." % (s, s // v, MAL, v))
    a = R.randint(2, 5)
    m = R.randint(2, 6)
    x = a * m - m
    return mcq("Der Bruch %s hat den Wert %s. Wie groß ist x?" % (fr("x", "x + %d" % m), bh(Fr(a - 1, a))), "x = %d" % x,
               ["x = %d" % (a - 1), "x = %d" % (x + m), "x = %d" % m], "x %s %d = (x + %d) %s %d, %s = %s, x = %d. <b>x = %d</b>" % (MAL, a, m, MAL, a - 1, lin(a, 0), lin(a - 1, (a - 1) * m), x, x))


def main():
    seen = set()
    sets = [
        ("Definitionsmenge", mix(R, seen, [(defm, 20)])),
        ("Bruchterme kürzen und berechnen", mix(R, seen, [(kuerzen, 20)])),
        ("Bruchterme addieren", mix(R, seen, [(addieren, 20)])),
        ("Bruchgleichungen", mix(R, seen, [(gleichung, 20)])),
        ("Sachaufgaben", mix(R, seen, [(sache, 20)])),
    ]
    body = lesson(
        ["Ein <b>Bruchterm</b> hat eine Variable im Nenner, z. B. %s. Der Nenner darf nie 0 sein: Die <b>Definitionsmenge</b> schließt diese Zahlen aus, hier D = ℚ ∖ {2}." % fr(3, "x − 2"),
         "<b>Kürzen</b> darf man nur gemeinsame Faktoren. Summen erst faktorisieren (ausklammern, binomische Formeln).",
         "<b>Addieren</b>: Auf den Hauptnenner erweitern, dann die Zähler addieren.",
         "<b>Bruchgleichungen</b>: D bestimmen, mit dem Hauptnenner multiplizieren, lösen und prüfen, ob die Lösung in D liegt."],
        [example("%s = 4" % fr(12, "x − 1"), ["D = ℚ ∖ {1}", "12 = 4(x − 1)", "12 = 4x − 4, x = 4"], "x = 4"),
         example(fr("x² − 9", "x + 3"), ["(x + 3)(x − 3)"], "x − 3")],
        [["%s = 5" % fr("x + 5", "x"), "Summanden nicht kürzen"],
         ["%s + %s = %s" % (fr(1, "x"), fr(2, "x"), fr(3, "2x")), "Gleicher Nenner bleibt: %s" % fr(3, "x")],
         ["Lösung x = 2 bei D = ℚ ∖ {2}", "Nicht in D: keine Lösung"]])
    faq = [
        {"q": "Was ist die Definitionsmenge eines Bruchterms?", "a": "Alle Zahlen, die man für x einsetzen darf. Ausgeschlossen sind die Zahlen, für die ein Nenner 0 wird."},
        {"q": "Warum darf man (x + 5)/x nicht zu 5 kürzen?", "a": "Man darf nur Faktoren kürzen, keine Summanden. (x + 5)/x = 1 + 5/x."},
        {"q": "Wie löse ich eine Bruchgleichung?", "a": "Definitionsmenge bestimmen, beide Seiten mit dem Hauptnenner multiplizieren, die entstandene Gleichung lösen und die Lösung mit D vergleichen."},
        {"q": "Kann eine Bruchgleichung keine Lösung haben?", "a": "Ja. Wenn die gefundene Zahl einen Nenner 0 macht, gehört sie nicht zur Definitionsmenge."},
    ]
    make_unit(R, "bruchterme-und-bruchgleichungen", "F",
              "Die Schülerinnen und Schüler bestimmen Definitionsmengen von Bruchtermen, kürzen, berechnen und addieren Bruchterme und lösen einfache Bruchgleichungen unter Beachtung der Definitionsmenge (Zusammenfassung).",
              "Bruchterme und Bruchgleichungen",
              "Bruchterme und Bruchgleichungen Klasse 8 – Definitionsmenge, Arbeitsblätter",
              "Bruchterme",
              "Bruchterme für Klasse 8: Definitionsmenge, Bruchterme kürzen und addieren, Bruchgleichungen lösen und Sachaufgaben. 100 Aufgaben mit Lösungen, kostenlos.",
              "Der Nenner darf nie 0 sein.",
              "Nur Faktoren kürzen, Lösung mit D vergleichen.",
              body, faq, sets, 15, grade="klasse-8")


if __name__ == "__main__":
    main()
