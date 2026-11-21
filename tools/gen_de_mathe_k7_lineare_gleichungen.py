# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 7: Lineare Gleichungen lösen（Leitidee Funktionaler Zusammenhang, Sek I）
  python3 tools/gen_de_mathe_k7_lineare_gleichungen.py
Äquivalenzumformungen, Variable auf beiden Seiten, Gleichungen mit Klammern, Gleichungen mit Brüchen, Probe, Lösungsmenge (keine oder unendlich viele Lösungen).
Fehler: nur auf einer Seite umgeformt, beim Herüberbringen das Vorzeichen nicht gewechselt, Minusklammer falsch aufgelöst, durch den falschen Faktor geteilt.
"""
import random
from fractions import Fraction as Fr
from de_common import lesson, example, make_unit, mix, Kids, MAL, fr, table
from de_k6 import bh, dz
from de_k7 import mcq

R = random.Random(49708)
KIDS = Kids(R)


def poly(a, b, v="x"):
    """a·x + b als Text"""
    s = ""
    if a:
        s = ("−" if a < 0 else "") + ("" if abs(a) == 1 else dz(abs(a))) + v
    if b:
        if s:
            s += (" + " if b > 0 else " − ") + dz(abs(b))
        else:
            s = dz(b)
    return s or "0"


def L(x):
    return "x = %s" % bh(x, True) if Fr(x).denominator not in (1,) else "x = %s" % dz(x)


def einfach():
    x = R.choice([-1, 1]) * R.randint(1, 15)
    a, b = R.choice([-1, 1]) * R.randint(2, 9), R.choice([-1, 1]) * R.randint(1, 30)
    r = a * x + b
    return mcq("Löse: %s = %s" % (poly(a, b), dz(r)), L(x), [L(Fr(r + b, a)), L(-x), L(Fr(r - b, -a)) if Fr(r - b, -a) != x else L(x + 1), L(r - b)],
               "%s auf beiden Seiten: %s = %s. Durch %s: <b>%s</b>." % (("− %s" % dz(b)) if b > 0 else ("+ %s" % dz(-b)), poly(a, 0), dz(r - b), dz(a), L(x)))


def beide():
    x = R.choice([-1, 1]) * R.randint(1, 12)
    a, c = R.sample([v for v in range(-9, 10) if v not in (0,)], 2)
    b = R.choice([-1, 1]) * R.randint(1, 20)
    d = (a - c) * x + b
    if a == c:
        return None
    return mcq("Löse: %s = %s" % (poly(a, b), poly(c, d)), L(x), [L(Fr(d - b, a + c)) if a + c and Fr(d - b, a + c) != x else L(x + 2), L(Fr(d + b, a - c)) if Fr(d + b, a - c) != x else L(-x if x else 3), L(-x) if x else L(1)],
               "%s auf beiden Seiten: %s = %s. Dann %s: %s = %s. <b>%s</b>" % (("− %s" % poly(c, 0)) if c > 0 else ("+ %s" % poly(-c, 0)), poly(a - c, b), dz(d), ("− %s" % dz(b)) if b > 0 else ("+ %s" % dz(-b)), poly(a - c, 0), dz(d - b), L(x)))


def klammer():
    x = R.choice([-1, 1]) * R.randint(1, 10)
    a, b = R.randint(2, 6), R.choice([-1, 1]) * R.randint(1, 9)
    c = R.choice([-1, 1]) * R.randint(1, 9)
    kind = R.choice(["mal", "minus"])
    if kind == "mal":
        r = a * (x + b) + c * x
        q = "%d(%s) %s %s = %s" % (a, poly(1, b), "+" if c > 0 else "−", poly(abs(c), 0), dz(r))
        if a + c in (0, 1):
            return None
        return mcq("Löse: %s" % q, L(x), [L(Fr(r - b, a + c)) if Fr(r - b, a + c) != x else L(x + 1), L(-x) if x else L(2), L(Fr(r - a * b, a - c)) if a != c and Fr(r - a * b, a - c) != x else L(x - 1)],
                   "Ausmultiplizieren: %s = %s. %s = %s. <b>%s</b>" % (poly(a + c, a * b), dz(r), poly(a + c, 0), dz(r - a * b), L(x)))
    k = R.randint(2, 9)
    r = k * x - (x + b)
    if k == 1:
        return None
    q = "%s − (%s) = %s" % (poly(k, 0), poly(1, b), dz(r))
    return mcq("Löse: %s" % q, L(x), [L(Fr(r + b, k - 1)) if Fr(r + b, k - 1) != x else L(x + 1), L(Fr(r - b, k + 1)) if Fr(r - b, k + 1) != x else L(x + 2), L(-x) if x else L(2)],
               "Minusklammer: %s − x %s %s = %s. %s = %s. <b>%s</b>" % (poly(k, 0), "−" if b > 0 else "+", dz(abs(b)), dz(r), poly(k - 1, 0), dz(r + b), L(x)))


def bruch():
    x = R.choice([-1, 1]) * R.randint(1, 12)
    n = R.choice([2, 3, 4, 5])
    kind = R.choice(["teil", "summe"])
    if kind == "teil":
        if x % n:
            x = x * n
        b = R.choice([-1, 1]) * R.randint(1, 9)
        r = Fr(x, n) + b
        return mcq("Löse: x/%d %s %d = %s" % (n, "+" if b > 0 else "−", abs(b), dz(r)), L(x), [L(Fr(x, n)), L((r + b) * n) if (r + b) * n != x else L(x + n), L(r * n)],
                   "%s %d: x/%d = %s. Mal %d: <b>%s</b>" % ("−" if b > 0 else "+", abs(b), n, dz(r - b), n, L(x)))
    m = R.choice([2, 3, 4, 6])
    if n == m:
        return None
    if x % (n * m):
        x = n * m * R.choice([-1, 1]) * R.randint(1, 3)
    r = Fr(x, n) + Fr(x, m)
    return mcq("Löse: x/%d + x/%d = %s" % (n, m, dz(r)), L(x), [L(r * (n + m)), L(r * n * m / 2), L(-x)],
               "Mit dem Hauptnenner %d multiplizieren: %s. Dann <b>%s</b>." % (n * m // __import__("math").gcd(n, m), "%dx + %dx = %s" % (n * m // __import__("math").gcd(n, m) // n, n * m // __import__("math").gcd(n, m) // m, dz(r * n * m // __import__("math").gcd(n, m))), L(x)))


def menge():
    kind = R.choice(["keine", "alle", "eine", "probe"])
    a, b, c = R.randint(2, 9), R.randint(1, 20), R.randint(1, 20)
    if kind == "keine":
        if b == c:
            return None
        return mcq("Wie viele Lösungen hat die Gleichung %s = %s?" % (poly(a, b), poly(a, c)), "keine Lösung", ["genau eine Lösung", "unendlich viele Lösungen", "zwei Lösungen"],
                   "Minus %s auf beiden Seiten: %d = %d. Das ist falsch: <b>keine Lösung</b> (L = { })." % (poly(a, 0), b, c))
    if kind == "alle":
        k = R.randint(2, 5)
        return mcq("Wie viele Lösungen hat die Gleichung %d(%s) = %s?" % (k, poly(a, b), poly(k * a, k * b)), "unendlich viele Lösungen", ["keine Lösung", "genau eine Lösung", "x = 0"],
                   "Ausmultipliziert stehen links und rechts dieselben Terme. Jede Zahl ist Lösung: <b>unendlich viele</b>.")
    if kind == "eine":
        x = R.randint(-9, 9)
        d = R.randint(1, 9)
        return mcq("Wie viele Lösungen hat die Gleichung %s = %s?" % (poly(a, b), poly(a + d, b - d * x)), "genau eine Lösung", ["keine Lösung", "unendlich viele Lösungen", "zwei Lösungen"],
                   "Die Faktoren vor x sind verschieden. Es gibt <b>genau eine Lösung</b>: x = %s." % dz(x))
    x = R.randint(-6, 8)
    y = x + R.choice([-2, -1, 1, 2])
    r = a * x + b
    return mcq("Ist x = %s eine Lösung von %s = %s?" % (dz(y), poly(a, b), dz(r)), "Nein, denn %s %s %s + %d = %s." % (dz(a), MAL, "(%s)" % dz(y) if y < 0 else dz(y), b, dz(a * y + b)),
               ["Ja, denn beide Seiten sind gleich.", "Nein, denn x muss positiv sein.", "Ja, denn %s ist eine ganze Zahl." % dz(y)],
               "Probe: %s %s %s + %d = %s ≠ %s. <b>Nein</b>, richtig wäre x = %s." % (dz(a), MAL, "(%s)" % dz(y) if y < 0 else dz(y), b, dz(a * y + b), dz(r), dz(x)))


def main():
    seen = set()
    sets = [
        ("Zweischrittgleichungen", mix(R, seen, [(einfach, 20)])),
        ("x auf beiden Seiten", mix(R, seen, [(beide, 20)])),
        ("Gleichungen mit Klammern", mix(R, seen, [(klammer, 20)])),
        ("Gleichungen mit Brüchen", mix(R, seen, [(bruch, 14), (einfach, 6)])),
        ("Lösungsmengen und Probe", mix(R, seen, [(menge, 12), (beide, 8)])),
    ]
    body = lesson(
        ["Eine Gleichung bleibt richtig, wenn man auf <b>beiden Seiten</b> dasselbe tut (Äquivalenzumformung): addieren, subtrahieren, multiplizieren oder dividieren (nicht durch 0).",
         "Ziel: Alle x-Terme auf eine Seite, alle Zahlen auf die andere. Zum Schluss durch den Faktor vor x teilen.",
         "Klammern zuerst auflösen. Bei Brüchen mit dem Hauptnenner multiplizieren.",
         "Mit der <b>Probe</b> (einsetzen) prüft man die Lösung. Eine Gleichung kann auch keine oder unendlich viele Lösungen haben."],
        [example("5x − 7 = 2x + 8", ["− 2x: 3x − 7 = 8", "+ 7: 3x = 15", ": 3"], "x = 5"),
         example("4(x − 2) = 2x + 6", ["4x − 8 = 2x + 6", "2x = 14"], "x = 7")],
        [["5x − 7 = 2x + 8 → 7x = 15", "2x auf die andere Seite: minus 2x"],
         ["3 − (x − 4) = 3 − x − 4", "Vorzeichen umdrehen: 3 − x + 4"],
         ["3x = 15 → x = 12", "Durch 3 teilen, nicht 3 abziehen: x = 5"]])
    faq = [
        {"q": "Was ist eine Äquivalenzumformung?", "a": "Eine Umformung, die man auf beiden Seiten gleich macht. Dadurch ändert sich die Lösung nicht."},
        {"q": "Wie löse ich eine Gleichung mit x auf beiden Seiten?", "a": "Bringe alle x-Terme auf eine Seite und alle Zahlen auf die andere. Dann teile durch den Faktor vor x."},
        {"q": "Kann eine Gleichung keine Lösung haben?", "a": "Ja. Wenn am Ende eine falsche Aussage wie 3 = 7 entsteht, ist die Lösungsmenge leer."},
        {"q": "Wozu macht man die Probe?", "a": "Man setzt die Lösung in die Ausgangsgleichung ein. Stimmen beide Seiten, ist die Lösung richtig."},
    ]
    make_unit(R, "lineare-gleichungen", "F",
              "Die Schülerinnen und Schüler lösen lineare Gleichungen mit Äquivalenzumformungen, auch mit Klammern, Brüchen und Variablen auf beiden Seiten, machen die Probe und bestimmen Lösungsmengen (Zusammenfassung).",
              "Lineare Gleichungen lösen",
              "Lineare Gleichungen lösen Klasse 7 – Äquivalenzumformungen, Arbeitsblätter",
              "Gleichungen lösen",
              "Lineare Gleichungen für Klasse 7: Äquivalenzumformungen, x auf beiden Seiten, Klammern, Brüche, Probe und Lösungsmengen. 100 Aufgaben mit Lösungen, kostenlos.",
              "Auf beiden Seiten das Gleiche tun.",
              "x-Terme auf eine Seite, Zahlen auf die andere.",
              body, faq, sets, 8, grade="klasse-7")


if __name__ == "__main__":
    main()
