# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 9: Scheitelpunktform und Normalform（Leitidee Funktionaler Zusammenhang, Sek I）
  python3 tools/gen_de_mathe_k9_scheitelpunktform_und_normalform.py
Von der Scheitelpunktform zur Normalform (ausmultiplizieren), quadratische Ergänzung, Scheitelpunkt aus der Normalform,
Schnittpunkt mit der y-Achse, Symmetrieachse, größter und kleinster Wert, Optimierungsaufgaben.
Fehler: (x − 3)² = x² − 9, beim Ergänzen die Hälfte nicht quadriert, Scheitel mit +b/2 statt −b/2, Minimum und Maximum verwechselt.
"""
import random
from fractions import Fraction as Fr
from de_common import lesson, example, make_unit, mix, MAL
from de_k9 import mcq, zahl, sform, qf, par, eur

R = random.Random(49904)


def S(d, e):
    return "S(%s | %s)" % (zahl(d), zahl(e))


def zu_normal():
    a = R.choice([1, 1, 1, 2, -1, 3, -2])
    d, e = R.randint(-6, 6), R.randint(-9, 9)
    if d == 0 or e == 0:
        return None
    b, c = -2 * a * d, a * d * d + e
    return mcq("Wandle in die Normalform um: %s" % sform(a, d, e), "y = " + qf(a, b, c),
               ["y = " + qf(a, 0, a * d * d + e), "y = " + qf(a, -a * d, a * d * d + e), "y = " + qf(a, b, d * d + e) if a != 1 else "y = " + qf(a, -b, c)],
               "(x %s %s)² = %s ausmultiplizieren%s, dann %s: <b>y = %s</b>." % ("−" if d > 0 else "+", zahl(abs(d)), qf(1, -2 * d, d * d), (", mal %s" % zahl(a)) if a != 1 else "", ("+ %s" % zahl(e)) if e >= 0 else ("− %s" % zahl(-e)), qf(a, b, c)))


def ergaenzung():
    d = R.randint(-7, 7)
    e = R.randint(-9, 9)
    if d == 0:
        return None
    b, c = -2 * d, d * d + e
    kind = R.choice(["form", "form", "erg", "s"])
    if kind == "erg":
        return mcq("Quadratische Ergänzung: x² %s %dx + ▢ = (x %s %d)². Welche Zahl gehört in das Kästchen?" % ("+" if b > 0 else "−", abs(b), "+" if b > 0 else "−", abs(d)), str(d * d),
                   [str(abs(b)), str(abs(d)), str(b * b)], "(%d : 2)² = %d² = <b>%d</b>." % (abs(b), abs(d), d * d))
    if kind == "form":
        return mcq("Bringe in die Scheitelpunktform: y = %s" % qf(1, b, c), sform(1, d, e), [sform(1, -d, e), sform(1, d, c), sform(1, d, e + d * d)],
                   "y = x² %s %dx + %d − %d %s %s. Die ersten drei Glieder sind eine binomische Formel: <b>%s</b>." % ("+" if b > 0 else "−", abs(b), d * d, d * d, "+" if c >= 0 else "−", zahl(abs(c)), sform(1, d, e)))
    return mcq("Bestimme den Scheitelpunkt von y = %s." % qf(1, b, c), S(d, e), [S(-d, e), S(d, c), S(b, c)],
               "Quadratische Ergänzung: %s. <b>%s</b>" % (sform(1, d, e), S(d, e)))


def mit_a():
    a = R.choice([2, 3, -1, -2, Fr(1, 2)])
    d, e = R.randint(-5, 5), R.randint(-8, 8)
    if d == 0:
        return None
    b, c = -2 * a * d, a * d * d + e
    if Fr(b).denominator != 1 or Fr(c).denominator != 1:
        return None
    kind = R.choice(["s", "s", "form"])
    if kind == "s":
        return mcq("Bestimme den Scheitelpunkt von y = %s." % qf(a, b, c), S(d, e), [S(-d, e), S(-b / 2, c) if (-b / 2) != d else S(d, c), S(d, c)] if c != e else [S(-d, e), S(d, -e), S(-b / 2, e) if -b / 2 != d else S(d + 1, e)],
                   "x<sub>S</sub> = −b : (2a) = %s : %s = %s. y<sub>S</sub> = f(%s) = %s. <b>%s</b>" % (zahl(-b), par(2 * a), zahl(d), zahl(d), zahl(e), S(d, e)))
    return mcq("Bringe in die Scheitelpunktform: y = %s" % qf(a, b, c), sform(a, d, e), [sform(a, -d, e), sform(a, d, c), sform(1, d, e)],
               "%s ausklammern, ergänzen, zurückrechnen: <b>%s</b>." % (zahl(a), sform(a, d, e)))


def eigenschaften():
    a = R.choice([1, 1, -1, 2, -2, 3])
    b, c = R.randint(-8, 8), R.randint(-9, 9)
    d = Fr(-b, 2 * a)
    if d.denominator != 1:
        return None
    e = a * d * d + b * d + c
    kind = R.choice(["y", "achse", "minmax", "wert"])
    if kind == "y":
        return mcq("Wo schneidet y = %s die y-Achse?" % qf(a, b, c), "in (0 | %s)" % zahl(c), ["in (%s | 0)" % zahl(c), "in (0 | %s)" % zahl(b) if b != c else "in (0 | %s)" % zahl(a), "in (0 | %s)" % zahl(e) if e != c else "in (0 | 0)" if c else "in (0 | 1)"],
                   "x = 0 einsetzen: y = %s. <b>(0 | %s)</b>" % (zahl(c), zahl(c)))
    if kind == "achse":
        return mcq("Wie lautet die Symmetrieachse der Parabel y = %s?" % qf(a, b, c), "x = %s" % zahl(d), ["x = %s" % zahl(-d) if d else "x = 1", "y = %s" % zahl(e), "x = %s" % zahl(c) if c != d else "x = %s" % zahl(d + 2)],
                   "Die Symmetrieachse geht durch den Scheitel: x = −b : (2a) = <b>%s</b>." % zahl(d))
    if kind == "minmax":
        ans = ("kleinster Wert %s" % zahl(e)) if a > 0 else ("größter Wert %s" % zahl(e))
        return mcq("Hat y = %s einen größten oder einen kleinsten Wert? Wie groß ist er?" % qf(a, b, c), ans,
                   [("größter Wert %s" % zahl(e)) if a > 0 else ("kleinster Wert %s" % zahl(e)), ("kleinster Wert %s" % zahl(c)) if a > 0 and c != e else ("größter Wert %s" % zahl(c)) if c != e else ("kleinster Wert %s" % zahl(e + 1)), ("kleinster Wert %s" % zahl(d)) if a > 0 and d != e else ("größter Wert %s" % zahl(d)) if d != e else ("größter Wert %s" % zahl(e - 1))],
                   "Scheitel %s, Parabel %s geöffnet: <b>%s</b>." % (S(d, e), "nach oben" if a > 0 else "nach unten", ans))
    return mcq("Welche Parabel hat den Scheitel %s?" % S(d, e), "y = " + qf(a, b, c), ["y = " + qf(a, -b, c) if b else "y = " + qf(a, 2, c), "y = " + qf(a, b, e) if e != c else "y = " + qf(a, b, c + 1), "y = " + qf(-a, b, c)],
               "Mit x<sub>S</sub> = −b : (2a) = %s und f(%s) = %s: <b>y = %s</b>." % (zahl(d), zahl(d), zahl(e), qf(a, b, c)))


def optimum():
    kind = R.choice(["zaun", "zaun", "gewinn", "zahl", "wurf"])
    if kind == "zaun":
        u = R.choice([20, 24, 32, 40, 48, 60, 80])
        s = u // 4
        ask = R.choice(["seite", "flaeche"])
        if ask == "seite":
            return mcq("Mit %d m Zaun soll ein rechteckiges Beet eingezäunt werden. Der Flächeninhalt ist A(x) = x(%d − x). Bei welcher Seitenlänge x wird A am größten?" % (u, u // 2), "x = %d m" % s,
                       ["x = %d m" % (u // 2), "x = %d m" % (u // 3) if u // 3 != s else "x = %d m" % (s + 2), "x = %d m" % (s * 2)],
                       "A(x) = −x² + %dx hat den Scheitel bei x = %d. Das Rechteck ist dann ein Quadrat: <b>%d m</b>." % (u // 2, s, s))
        return mcq("Mit %d m Zaun wird ein rechteckiges Beet eingezäunt. Wie groß ist der größtmögliche Flächeninhalt?" % u, "%d m²" % (s * s), ["%d m²" % (u * u // 4), "%d m²" % (s * (s + 2)), "%d m²" % (u // 2)],
                   "Am größten ist das Quadrat mit der Seite %d : 4 = %d m: <b>%d m²</b>." % (u, s, s * s))
    if kind == "gewinn":
        d, e = R.choice([(10, 400), (20, 900), (15, 450), (30, 1800), (25, 1250)])
        a = Fr(-1) if d < 20 else Fr(-2)
        return mcq("Der Gewinn einer Schulfirma ist G(x) = %s (x: Preis in €, G in €). Bei welchem Preis ist der Gewinn am größten?" % sform(a, d, e).split("= ", 1)[1], "bei %d €" % d,
                   ["bei %d €" % e, "bei %d €" % (2 * d), "bei 0 €"], "Der Scheitel S(%d | %d) ist der höchste Punkt: <b>bei %d €</b> (Gewinn %s)." % (d, e, d, eur(e)))
    if kind == "zahl":
        s = R.choice([10, 12, 16, 20, 30, 40])
        return mcq("Die Summe zweier Zahlen ist %d. Für welche Zahlen wird ihr Produkt x(%d − x) am größten?" % (s, s), "%d und %d" % (s // 2, s // 2), ["%d und %d" % (s // 2 - 1, s // 2 + 1), "0 und %d" % s, "%d und %d" % (s // 4, s - s // 4)],
                   "P(x) = −x² + %dx hat den Scheitel bei x = %d: <b>%d und %d</b>." % (s, s // 2, s // 2, s // 2))
    d, e = R.choice([(2, 5), (3, 7), (4, 9), (5, 12)])
    a = Fr(-1, R.choice([2, 4]))
    b, c = -2 * a * d, a * d * d + e
    return mcq("Ein Wasserstrahl folgt der Bahn y = %s (in m). Wie hoch steigt er höchstens?" % qf(a, b, c), "%s m" % zahl(e), ["%s m" % zahl(c), "%s m" % zahl(d), "%s m" % zahl(b)],
               "Scheitel bei x = −b : (2a) = %s, y = f(%s) = <b>%s m</b>." % (zahl(d), zahl(d), zahl(e)))


def main():
    seen = set()
    sets = [
        ("Scheitelpunktform in Normalform", mix(R, seen, [(zu_normal, 20)])),
        ("Quadratische Ergänzung", mix(R, seen, [(ergaenzung, 20)])),
        ("Parabeln mit Streckfaktor", mix(R, seen, [(mit_a, 20)])),
        ("Eigenschaften ablesen", mix(R, seen, [(eigenschaften, 20)])),
        ("Größter und kleinster Wert", mix(R, seen, [(optimum, 20)])),
    ]
    body = lesson(
        ["<b>Normalform</b>: y = ax² + bx + c. Man sieht sofort den Schnittpunkt mit der y-Achse (0 | c).",
         "<b>Scheitelpunktform</b>: y = a(x − d)² + e. Man sieht sofort den Scheitel S(d | e).",
         "Von der Scheitelpunktform zur Normalform: ausmultiplizieren (binomische Formel). Zurück: <b>quadratische Ergänzung</b> – die Hälfte von b quadrieren, addieren und wieder subtrahieren.",
         "Kurzweg für den Scheitel: x<sub>S</sub> = −b : (2a), y<sub>S</sub> = f(x<sub>S</sub>). Ist a &gt; 0, ist das der kleinste Wert, sonst der größte."],
        [example("y = x² − 6x + 5", ["x² − 6x + 9 − 9 + 5", "(x − 3)² − 4"], "S(3 | −4)"),
         example("y = 2(x + 1)² − 3", ["2(x² + 2x + 1) − 3"], "y = 2x² + 4x − 1")],
        [["(x − 3)² = x² − 9", "x² − 6x + 9"],
         ["x² + 8x: Ergänzung 8", "(8 : 2)² = 16"],
         ["y = x² + 4x: S(2 | …)", "x<sub>S</sub> = −4 : 2 = −2"]])
    faq = [
        {"q": "Was ist der Unterschied zwischen Normalform und Scheitelpunktform?", "a": "Die Normalform y = ax² + bx + c zeigt den y-Achsenabschnitt c, die Scheitelpunktform y = a(x − d)² + e zeigt den Scheitel S(d | e)."},
        {"q": "Wie funktioniert die quadratische Ergänzung?", "a": "Man ergänzt (b : 2)², damit eine binomische Formel entsteht, und zieht dieselbe Zahl wieder ab."},
        {"q": "Wie finde ich den Scheitel schnell?", "a": "x_S = −b : (2a), dann y_S = f(x_S) ausrechnen."},
        {"q": "Wofür braucht man den Scheitel?", "a": "Für größte oder kleinste Werte: größte Fläche, größter Gewinn, höchster Punkt einer Wurfbahn."},
    ]
    make_unit(R, "scheitelpunktform-und-normalform", "F",
              "Die Schülerinnen und Schüler wandeln quadratische Funktionsterme zwischen Normalform und Scheitelpunktform um (quadratische Ergänzung), bestimmen Scheitel, Symmetrieachse und Extremwerte und lösen Optimierungsaufgaben (Zusammenfassung).",
              "Scheitelpunktform und Normalform",
              "Scheitelpunktform und quadratische Ergänzung Klasse 9 – Arbeitsblätter mit Lösungen",
              "Scheitelpunktform",
              "Scheitelpunktform für Klasse 9: Normalform umwandeln, quadratische Ergänzung, Scheitelpunkt, Symmetrieachse, größter und kleinster Wert. 100 Aufgaben mit Lösungen, kostenlos.",
              "x² + bx: (b : 2)² ergänzen.",
              "Scheitel: x = −b : (2a).",
              body, faq, sets, 4, grade="klasse-9")


if __name__ == "__main__":
    main()
