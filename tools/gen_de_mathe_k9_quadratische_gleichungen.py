# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 9: Quadratische Gleichungen（Leitidee Funktionaler Zusammenhang, Sek I）
  python3 tools/gen_de_mathe_k9_quadratische_gleichungen.py
Reinquadratische Gleichungen, Ausklammern und Satz vom Nullprodukt, p-q-Formel, abc-Formel (Mitternachtsformel),
Diskriminante und Anzahl der Lösungen, Linearfaktoren.
Fehler: x² = 49 nur x = 7, beim Ausklammern x = 0 vergessen, −p/2 mit falschem Vorzeichen, Diskriminante falsch gedeutet.
"""
import random, math
from fractions import Fraction as Fr
from de_common import lesson, example, make_unit, mix, MAL
from de_k9 import mcq, zahl, qf, par

R = random.Random(49905)
W = "√"


def L(*xs):
    xs = sorted(set(Fr(x) for x in xs))
    return "L = {%s}" % "; ".join(zahl(x) for x in xs) if xs else "L = { }"


def rein():
    kind = R.choice(["einfach", "a", "minus", "keine", "klammer"])
    r = R.randint(1, 12)
    if kind == "einfach":
        return mcq("Löse: x² = %d" % (r * r), L(-r, r), [L(r), L(Fr(r * r, 2)), L(-r * r, r * r)],
                   "x = %s%d oder x = −%s%d: <b>%s</b>." % (W, r * r, W, r * r, L(-r, r)))
    if kind == "a":
        a = R.randint(2, 5)
        c = a * r * r
        return mcq("Löse: %dx² − %d = 0" % (a, c), L(-r, r), [L(-r * r, r * r), L(r), L(-Fr(c, 2 * a), Fr(c, 2 * a)) if Fr(c, 2 * a) != r else L(-r - 1, r + 1)],
                   "%dx² = %d, x² = %d, <b>%s</b>." % (a, c, r * r, L(-r, r)))
    if kind == "minus":
        c = R.randint(1, 30)
        return mcq("Löse: x² + %d = %d" % (c, c + r * r), L(-r, r), [L(r), L(-r * r, r * r), L(-math.isqrt(c + r * r), math.isqrt(c + r * r)) if math.isqrt(c + r * r) ** 2 == c + r * r else L(-r - 1, r + 1)],
                   "x² = %d − %d = %d, <b>%s</b>." % (c + r * r, c, r * r, L(-r, r)))
    if kind == "keine":
        c = R.randint(1, 50)
        return mcq("Löse: x² + %d = 0" % c, "L = { } (keine Lösung)", [L(-math.isqrt(c), math.isqrt(c)) if math.isqrt(c) ** 2 == c else "x = −%s%d" % (W, c), "x = %s%d" % (W, c), "L = {0}"],
                   "x² = −%d. Ein Quadrat ist nie negativ: <b>keine Lösung</b>." % c)
    d = R.randint(-6, 6)
    if d == 0:
        return None
    return mcq("Löse: (x %s %d)² = %d" % ("−" if d > 0 else "+", abs(d), r * r), L(d - r, d + r), [L(-d - r, -d + r), L(d + r), L(-r, r)],
               "x %s %d = %d oder x %s %d = −%d: <b>%s</b>." % ("−" if d > 0 else "+", abs(d), r, "−" if d > 0 else "+", abs(d), r, L(d - r, d + r)))


def nullprodukt():
    kind = R.choice(["aus", "aus", "prod", "prod", "aus_a"])
    if kind == "aus":
        b = R.choice([-1, 1]) * R.randint(1, 12)
        return mcq("Löse durch Ausklammern: %s = 0" % qf(1, b, 0), L(0, -b), [L(-b), L(b), L(0, b)],
                   "x(%s) = 0. Ein Produkt ist 0, wenn ein Faktor 0 ist: x = 0 oder x = %s. <b>%s</b>" % (qf(0, 1, b).replace("x²", ""), zahl(-b), L(0, -b)))
    if kind == "aus_a":
        a = R.randint(2, 5)
        k = R.choice([-1, 1]) * R.randint(1, 8)
        b = -a * k
        return mcq("Löse: %s = 0" % qf(a, b, 0), L(0, k), [L(k), L(0, -k), L(0, b)],
                   "x(%s) = 0: x = 0 oder %dx = %s, x = %s. <b>%s</b>" % (qf(0, a, b).replace("x²", ""), a, zahl(-b), zahl(k), L(0, k)))
    p, q = R.sample(range(-8, 9), 2)
    if 0 in (p, q):
        return None
    return mcq("Löse: (x %s %d)(x %s %d) = 0" % ("−" if p > 0 else "+", abs(p), "−" if q > 0 else "+", abs(q)), L(p, q), [L(-p, -q), L(p * q), L(p, -q)],
               "Satz vom Nullprodukt: x %s %d = 0 oder x %s %d = 0. <b>%s</b>" % ("−" if p > 0 else "+", abs(p), "−" if q > 0 else "+", abs(q), L(p, q)))


def pq():
    x1, x2 = R.randint(-9, 9), R.randint(-9, 9)
    if x1 == x2 or 0 in (x1, x2):
        return None
    p, q = -(x1 + x2), x1 * x2
    D = Fr(p * p, 4) - q
    kind = R.choice(["l", "l", "l", "schritt"])
    if kind == "schritt":
        return mcq("Für x² + px + q = 0 gilt x = −p/2 ± %s((p/2)² − q). Welche Werte haben p und q in %s = 0?" % (W, qf(1, p, q)), "p = %s, q = %s" % (zahl(p), zahl(q)),
                   ["p = %s, q = %s" % (zahl(-p), zahl(q)), "p = %s, q = %s" % (zahl(q), zahl(p)), "p = %s, q = %s" % (zahl(p), zahl(-q))],
                   "Vorzeichen mitnehmen: <b>p = %s, q = %s</b>." % (zahl(p), zahl(q)))
    return mcq("Löse mit der p-q-Formel: %s = 0" % qf(1, p, q), L(x1, x2), [L(-x1, -x2), L(x1, -x2) if x1 != -x2 else L(x1 + 1, x2), L(Fr(-p, 2))],
               "x = %s ± %s(%s − %s) = %s ± %s. <b>%s</b>" % (zahl(Fr(-p, 2)), W, zahl(Fr(p * p, 4)), par(q), zahl(Fr(-p, 2)), zahl(Fr(abs(x1 - x2), 2)), L(x1, x2)))


def abc():
    a = R.choice([2, 3, -1, -2, 4])
    x1 = Fr(R.randint(-6, 6), R.choice([1, 1, 2]))
    x2 = Fr(R.randint(-6, 6))
    if x1 == x2:
        return None
    b, c = -a * (x1 + x2), a * x1 * x2
    if b.denominator != 1 or c.denominator != 1:
        return None
    D = b * b - 4 * a * c
    return mcq("Löse: %s = 0" % qf(a, b, c), L(x1, x2), [L(-x1, -x2), L(x1 * a, x2 * a) if a * x1 != x1 else L(x1 + 1, x2), L(x1, -x2) if x1 != -x2 and x2 else L(x2)],
               "abc-Formel: x = (−b ± %s(b² − 4ac)) : (2a) = (%s ± %s%s) : %s. <b>%s</b>" % (W, zahl(-b), W, zahl(D), par(2 * a), L(x1, x2)))


def diskr():
    kind = R.choice(["zwei", "eine", "keine"])
    a = R.choice([1, 1, 2, -1, 3])
    if kind == "zwei":
        x1, x2 = R.sample(range(-6, 7), 2)
        b, c = -a * (x1 + x2), a * x1 * x2
    elif kind == "eine":
        x1 = R.randint(-6, 6)
        b, c = -2 * a * x1, a * x1 * x1
    else:
        b = R.randint(-6, 6)
        c = Fr(b * b, 4 * a) + R.randint(1, 6) * (1 if a > 0 else -1)
        if c.denominator != 1:
            return None
    D = b * b - 4 * a * c
    ans = {"zwei": "zwei Lösungen", "eine": "genau eine Lösung", "keine": "keine Lösung"}[kind]
    return mcq("Wie viele Lösungen hat %s = 0? (Tipp: Diskriminante D = b² − 4ac)" % qf(a, b, c), ans, [v for v in ["zwei Lösungen", "genau eine Lösung", "keine Lösung", "unendlich viele Lösungen"] if v != ans],
               "D = %s² − 4 %s %s %s %s = %s. D %s 0: <b>%s</b>." % (par(b), MAL, par(a), MAL, par(c), zahl(D), "&gt;" if D > 0 else ("=" if D == 0 else "&lt;"), ans))


def linear():
    x1, x2 = R.sample([v for v in range(-8, 9) if v], 2)
    p, q = -(x1 + x2), x1 * x2
    kind = R.choice(["fak", "gl"])
    f = lambda x: "(x %s %d)" % ("−" if x > 0 else "+", abs(x))
    if kind == "fak":
        return mcq("Zerlege in Linearfaktoren: %s" % qf(1, p, q), f(x1) + f(x2), [f(-x1) + f(-x2), f(x1) + f(-x2) if x1 != -x2 else f(x1 + 1) + f(x2), "x(%s)" % qf(0, 1, p).replace("x²", "") if q else f(x1) + f(x2 + 1)],
                   "Nullstellen %s und %s (Probe: %s + %s = %s, %s %s %s = %s). <b>%s</b>" % (zahl(x1), zahl(x2), zahl(x1), par(x2), zahl(-p), zahl(x1), MAL, par(x2), zahl(q), f(x1) + f(x2)))
    return mcq("Welche Gleichung hat die Lösungen %s und %s?" % (zahl(min(x1, x2)), zahl(max(x1, x2))), "%s = 0" % qf(1, p, q), ["%s = 0" % qf(1, -p, q), "%s = 0" % qf(1, p, -q), "%s = 0" % qf(1, q, p) if p != q else "%s = 0" % qf(1, p, q + 1)],
               "(x − x₁)(x − x₂) ausmultiplizieren: <b>%s = 0</b>." % qf(1, p, q))


def main():
    seen = set()
    sets = [
        ("Reinquadratische Gleichungen", mix(R, seen, [(rein, 20)])),
        ("Ausklammern und Nullprodukt", mix(R, seen, [(nullprodukt, 20)])),
        ("p-q-Formel", mix(R, seen, [(pq, 20)])),
        ("abc-Formel", mix(R, seen, [(abc, 20)])),
        ("Anzahl der Lösungen und Linearfaktoren", mix(R, seen, [(diskr, 12), (linear, 8)])),
    ]
    body = lesson(
        ["<b>Reinquadratisch</b> (ohne x-Glied): nach x² auflösen, dann Wurzel ziehen – meist zwei Lösungen: x² = 25 ⇒ x = 5 oder x = −5.",
         "<b>Ohne Zahlglied</b>: x ausklammern. Ein Produkt ist 0, wenn ein Faktor 0 ist (<b>Satz vom Nullprodukt</b>).",
         "<b>p-q-Formel</b> für x² + px + q = 0: x = −p/2 ± %s((p/2)² − q). Steht vor x² eine Zahl a, erst durch a teilen oder die <b>abc-Formel</b> x = (−b ± %s(b² − 4ac)) : (2a) nehmen." % (W, W),
         "Die <b>Diskriminante</b> D = b² − 4ac entscheidet: D &gt; 0 zwei, D = 0 eine, D &lt; 0 keine Lösung."],
        [example("x² + 2x − 15 = 0", ["p = 2, q = −15", "x = −1 ± %s(1 + 15) = −1 ± 4" % W], "L = {−5; 3}"),
         example("x² − 7x = 0", ["x(x − 7) = 0"], "L = {0; 7}")],
        [["x² = 49 ⇒ x = 7", "Auch −7 ist Lösung"],
         ["x² − 5x = 0 ⇒ x = 5", "x = 0 nicht vergessen"],
         ["x² − 4x + 3 = 0: −p/2 = −2", "p = −4, also −p/2 = 2"]])
    faq = [
        {"q": "Wie lautet die p-q-Formel?", "a": "Für x² + px + q = 0 gilt x = −p/2 ± √((p/2)² − q)."},
        {"q": "Was ist die abc-Formel (Mitternachtsformel)?", "a": "Für ax² + bx + c = 0 gilt x = (−b ± √(b² − 4ac)) : (2a)."},
        {"q": "Wie viele Lösungen hat eine quadratische Gleichung?", "a": "Zwei, eine oder keine – je nachdem, ob die Diskriminante positiv, null oder negativ ist."},
        {"q": "Wann lohnt sich Ausklammern?", "a": "Wenn das Zahlglied fehlt (z. B. x² − 6x = 0). Dann ist immer x = 0 eine Lösung."},
    ]
    make_unit(R, "quadratische-gleichungen", "F",
              "Die Schülerinnen und Schüler lösen quadratische Gleichungen durch Wurzelziehen, Ausklammern (Satz vom Nullprodukt), mit der p-q-Formel und der abc-Formel, bestimmen die Anzahl der Lösungen mit der Diskriminante und zerlegen in Linearfaktoren (Zusammenfassung).",
              "Quadratische Gleichungen",
              "Quadratische Gleichungen Klasse 9 – p-q-Formel, abc-Formel, Arbeitsblätter mit Lösungen",
              "Quadratische Gleichungen",
              "Quadratische Gleichungen für Klasse 9: reinquadratisch, Ausklammern, Satz vom Nullprodukt, p-q-Formel, abc-Formel, Diskriminante und Linearfaktoren. 100 Aufgaben mit Lösungen, kostenlos.",
              "x = −p/2 ± √((p/2)² − q)",
              "D > 0: zwei, D = 0: eine, D < 0: keine Lösung.",
              body, faq, sets, 5, grade="klasse-9")


if __name__ == "__main__":
    main()
