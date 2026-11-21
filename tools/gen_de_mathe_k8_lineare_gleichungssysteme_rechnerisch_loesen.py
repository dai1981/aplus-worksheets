# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 8: Lineare Gleichungssysteme rechnerisch lösen（Leitidee Funktionaler Zusammenhang, Sek I）
  python3 tools/gen_de_mathe_k8_lineare_gleichungssysteme_rechnerisch_loesen.py
Gleichsetzungsverfahren, Einsetzungsverfahren, Additionsverfahren (auch mit Multiplizieren einer Gleichung), passendes Verfahren wählen, Zwischenschritte.
Fehler: nur x berechnet, beim Einsetzen die Klammer vergessen, beim Addieren eine Variable nicht eliminiert, Vorzeichenfehler beim Subtrahieren.
"""
import random
from fractions import Fraction as Fr
from de_common import lesson, example, make_unit, mix, MAL
from de_k6 import bh, dz
from de_k8 import mcq, expr, gl, par

R = random.Random(49808)


def zahl(v):
    v = Fr(v)
    return bh(v) if v.denominator != 1 else dz(v)


def lgs(e1, e2):
    return "I: %s<br>II: %s<br>" % (e1, e2)


def eq(a, b, c):
    return "%s = %s" % (expr([(a, "x"), (b, "y")]), zahl(c))


def L(x, y):
    return "x = %s, y = %s" % (zahl(x), zahl(y))


def wrongs(x, y):
    return [L(y, x) if x != y else L(x, -y if y else 1), L(x, y + 1), L(-x, y) if x else L(1, y), L(x + 1, y - 1)]


def gleich():
    x, y = R.randint(-5, 6), R.randint(-6, 8)
    m1, m2 = R.sample([-3, -2, -1, 1, 2, 3, 4], 2)
    b1, b2 = y - m1 * x, y - m2 * x
    return mcq(lgs(gl(m1, b1), gl(m2, b2)) + "Löse mit dem Gleichsetzungsverfahren.", L(x, y), wrongs(x, y),
               "%s = %s, also %s = %s und x = %s. In I: y = %s. <b>%s</b>" % (expr([(m1, "x"), (b1, "")]), expr([(m2, "x"), (b2, "")]), expr([(m1 - m2, "x")]), zahl(b2 - b1), zahl(x), zahl(y), L(x, y)))


def einsetz():
    x, y = R.randint(-4, 6), R.randint(-5, 7)
    m, b = R.choice([-3, -2, -1, 1, 2, 3]), None
    b = y - m * x
    a2, c2 = R.choice([1, 2, 3, -2]), R.choice([1, 2, 3, -1, 4])
    if a2 + c2 * m == 0:
        return None
    r = a2 * x + c2 * y
    return mcq(lgs(gl(m, b), eq(a2, c2, r)) + "Löse mit dem Einsetzungsverfahren.", L(x, y), wrongs(x, y),
               "I in II einsetzen: %s %s %s(%s) = %s. Ausmultiplizieren: %s = %s, x = %s. y = %s. <b>%s</b>" % (expr([(a2, "x")]), "+" if c2 > 0 else "−", "" if abs(c2) == 1 else str(abs(c2)), expr([(m, "x"), (b, "")]), zahl(r),
                                                                                            expr([(a2 + c2 * m, "x"), (c2 * b, "")]), zahl(r), zahl(x), zahl(y), L(x, y)))


def addition():
    x, y = R.randint(-5, 6), R.randint(-5, 6)
    a1, b = R.randint(1, 5), R.randint(1, 5)
    a2 = R.randint(1, 5)
    kind = R.choice(["direkt", "direkt", "mal"])
    if kind == "direkt":
        e1, e2 = (a1, b), (a2, -b)
        if a1 + a2 == 0:
            return None
        c1, c2 = a1 * x + b * y, a2 * x - b * y
        return mcq(lgs(eq(a1, b, c1), eq(a2, -b, c2)) + "Löse mit dem Additionsverfahren.", L(x, y), wrongs(x, y),
                   "I + II: %s = %s, also x = %s. In I einsetzen: y = %s. <b>%s</b>" % (expr([(a1 + a2, "x")]), zahl(c1 + c2), zahl(x), zahl(y), L(x, y)))
    k = R.choice([2, 3])
    b2 = R.randint(1, 4)
    # I: a1 x + k*b2 y = c1 ; II: a2 x - b2 y = c2 -> II mal k
    c1, c2 = a1 * x + k * b2 * y, a2 * x - b2 * y
    if a1 + k * a2 == 0:
        return None
    return mcq(lgs(eq(a1, k * b2, c1), eq(a2, -b2, c2)) + "Löse mit dem Additionsverfahren.", L(x, y), wrongs(x, y),
               "II mal %d: %s. Dann I + II: %s = %s, x = %s. Einsetzen: y = %s. <b>%s</b>" % (k, eq(k * a2, -k * b2, k * c2), expr([(a1 + k * a2, "x")]), zahl(c1 + k * c2), zahl(x), zahl(y), L(x, y)))


def schritt():
    kind = R.choice(["welches", "welches", "zwischen", "faktor", "zuerst"])
    if kind == "welches":
        art = R.choice(["gleich", "einsetz", "add"])
        if art == "gleich":
            q = lgs(gl(R.choice([2, 3]), R.randint(1, 6)), gl(R.choice([-1, -2]), R.randint(1, 9)))
            a = "Gleichsetzungsverfahren"
            why = "Beide Gleichungen sind schon nach y aufgelöst."
        elif art == "einsetz":
            q = lgs(gl(R.choice([2, 3, -2]), R.randint(1, 6)), eq(R.choice([3, 4, 5]), R.choice([2, 3]), R.randint(5, 30)))
            a = "Einsetzungsverfahren"
            why = "Nur Gleichung I ist nach y aufgelöst. Man setzt sie in II ein."
        else:
            b = R.randint(2, 5)
            q = lgs(eq(R.randint(2, 5), b, R.randint(5, 30)), eq(R.randint(1, 5), -b, R.randint(1, 20)))
            a = "Additionsverfahren"
            why = "Die y-Glieder haben Gegenzahlen als Faktoren. Beim Addieren fällt y weg."
        return mcq(q + "Welches Verfahren ist hier am günstigsten?", a, [v for v in ["Gleichsetzungsverfahren", "Einsetzungsverfahren", "Additionsverfahren", "Probieren"] if v != a], "%s <b>%s</b>" % (why, a))
    if kind == "zwischen":
        m1, b1, m2, b2 = R.randint(1, 5), R.randint(-6, 6), R.randint(-5, -1), R.randint(-6, 6)
        return mcq(lgs(gl(m1, b1), gl(m2, b2)) + "Welche Gleichung entsteht beim Gleichsetzen?", "%s = %s" % (expr([(m1, "x"), (b1, "")]), expr([(m2, "x"), (b2, "")])),
                   ["%s = %s" % (expr([(m1, "x"), (b2, "")]), expr([(m2, "x"), (b1, "")])) if b1 != b2 else "%s = %s" % (expr([(m1, "x"), (b1 + 1, "")]), expr([(m2, "x"), (b2, "")])), "%s = %s" % (expr([(m1, "x"), (b1, "")]), expr([(m2, "x"), (-b2, "")])) if b2 else "%s = %s" % (expr([(m1, "x"), (b1, "")]), expr([(m2 - 1, "x")])), "%s = %s" % (expr([(m1, "x"), (b1, "")]), expr([(-m2, "x"), (b2, "")]))],
                   "Die rechten Seiten werden gleichgesetzt: <b>%s = %s</b>." % (expr([(m1, "x"), (b1, "")]), expr([(m2, "x"), (b2, "")])))
    if kind == "faktor":
        b1, b2 = R.choice([(2, 1), (3, 1), (4, 2), (6, 2), (6, 3), (4, 1)])
        a1, a2 = R.randint(1, 5), R.randint(1, 5)
        k = b1 // b2
        return mcq(lgs(eq(a1, b1, R.randint(1, 30)), eq(a2, -b2, R.randint(1, 20))) + "Mit welcher Zahl muss man Gleichung II multiplizieren, damit beim Addieren y wegfällt?", str(k),
                   ["−%d" % k, str(b1 + b2), str(b1)] if b1 != k else ["−%d" % k, str(b1 + b2), str(k + 1)],
                   "%s %s %d = %s. Das ist die Gegenzahl zu %dy: <b>%d</b>." % (expr([(-b2, "y")]), MAL, k, expr([(-b1, "y")]), b1, k))
    x, y = R.randint(1, 6), R.randint(-4, 6)
    m = R.choice([2, 3, -1])
    b = y - m * x
    return mcq("Beim Lösen hast du x = %s erhalten. I lautet %s. Wie groß ist y?" % (zahl(x), gl(m, b)), "y = %s" % zahl(y), ["y = %s" % zahl(m + b), "y = %s" % zahl(y + m) if m else "y = 0", "y = %s" % zahl(-y) if y else "y = 1"],
               "x einsetzen: y = %s %s %s %s = <b>%s</b>. Erst x und y zusammen sind die Lösung." % (zahl(m), MAL, zahl(x), ("+ %s" % zahl(b)) if b >= 0 else ("− %s" % zahl(-b)), zahl(y)))


def gemischt():
    return R.choice([gleich, einsetz, addition])()


def main():
    seen = set()
    sets = [
        ("Gleichsetzungsverfahren", mix(R, seen, [(gleich, 20)])),
        ("Einsetzungsverfahren", mix(R, seen, [(einsetz, 20)])),
        ("Additionsverfahren", mix(R, seen, [(addition, 20)])),
        ("Verfahren und Zwischenschritte", mix(R, seen, [(schritt, 20)])),
        ("Gemischte Aufgaben", mix(R, seen, [(gemischt, 20)])),
    ]
    body = lesson(
        ["<b>Gleichsetzungsverfahren</b>: Beide Gleichungen nach y (oder x) auflösen und die rechten Seiten gleichsetzen.",
         "<b>Einsetzungsverfahren</b>: Eine Gleichung nach einer Variablen auflösen und den Term in die andere Gleichung einsetzen (in Klammern).",
         "<b>Additionsverfahren</b>: Die Gleichungen so multiplizieren, dass vor einer Variablen Gegenzahlen stehen. Dann addieren – die Variable fällt weg.",
         "Zum Schluss die zweite Variable berechnen und die Probe in <b>beiden</b> Gleichungen machen."],
        [example("I: y = 2x + 1, II: y = −x + 7", ["2x + 1 = −x + 7", "3x = 6, x = 2", "y = 5"], "x = 2, y = 5"),
         example("I: 3x + 2y = 12, II: x − 2y = 4", ["I + II: 4x = 16, x = 4", "4 − 2y = 4, y = 0"], "x = 4, y = 0")],
        [["Nur x = 2 angeben", "Auch y berechnen: (2 | 5)"],
         ["y = 2x + 1 in 3x − y = 4: 3x − 2x + 1", "Klammer setzen: 3x − (2x + 1)"],
         ["x − 2y = 4 mal 2: 2x − 2y = 8", "Jedes Glied multiplizieren: 2x − 4y = 8"]])
    faq = [
        {"q": "Welche Verfahren gibt es?", "a": "Gleichsetzungs-, Einsetzungs- und Additionsverfahren. Alle führen zur gleichen Lösung; man wählt das, das am wenigsten Rechenarbeit macht."},
        {"q": "Wann nehme ich das Additionsverfahren?", "a": "Wenn vor einer Variablen schon Gegenzahlen stehen oder man sie leicht durch Multiplizieren erzeugen kann."},
        {"q": "Warum setze ich beim Einsetzen Klammern?", "a": "Der eingesetzte Term wird als Ganzes mit dem Faktor multipliziert. Ohne Klammer gehen Vorzeichen verloren."},
        {"q": "Wie mache ich die Probe?", "a": "Setze x und y in beide Gleichungen ein. Beide müssen stimmen."},
    ]
    make_unit(R, "lineare-gleichungssysteme-rechnerisch-loesen", "F",
              "Die Schülerinnen und Schüler lösen lineare Gleichungssysteme mit zwei Variablen mit dem Gleichsetzungs-, Einsetzungs- und Additionsverfahren und wählen ein geeignetes Verfahren (Zusammenfassung).",
              "Lineare Gleichungssysteme rechnerisch lösen",
              "Gleichungssysteme lösen Klasse 8 – Gleichsetzungs-, Einsetzungs-, Additionsverfahren",
              "LGS rechnerisch",
              "Lineare Gleichungssysteme für Klasse 8: Gleichsetzungsverfahren, Einsetzungsverfahren, Additionsverfahren und das passende Verfahren wählen. 100 Aufgaben mit Lösungen, kostenlos.",
              "Gleichsetzen, Einsetzen oder Addieren.",
              "Ziel: eine Variable fällt weg. Dann die zweite berechnen.",
              body, faq, sets, 8, grade="klasse-8")


if __name__ == "__main__":
    main()
