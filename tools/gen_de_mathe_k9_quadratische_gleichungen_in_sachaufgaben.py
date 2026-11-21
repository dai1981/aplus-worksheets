# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 9: Quadratische Gleichungen in Sachaufgaben（Leitidee Funktionaler Zusammenhang, Sek I）
  python3 tools/gen_de_mathe_k9_quadratische_gleichungen_in_sachaufgaben.py
Nullstellen von Parabeln, Schnittpunkte von Parabel und Gerade, Zahlenrätsel, Rechtecke und Rahmen, Wurf- und Fallbewegungen.
Fehler: negative Lösung bei Längen nicht verworfen, nur eine Nullstelle angegeben, Gleichung falsch aufgestellt (Umfang statt Fläche).
"""
import random, math
from fractions import Fraction as Fr
from de_common import lesson, example, make_unit, mix, MAL
from de_k9 import mcq, zahl, qf, sform, par

R = random.Random(49906)


def P(x, y):
    return "(%s | %s)" % (zahl(x), zahl(y))


def nullstellen():
    a = R.choice([1, 1, -1, 2])
    x1, x2 = R.sample([v for v in range(-7, 8) if v], 2)
    b, c = -a * (x1 + x2), a * x1 * x2
    kind = R.choice(["ns", "ns", "x"])
    lo, hi = min(x1, x2), max(x1, x2)
    if kind == "ns":
        return mcq("Berechne die Nullstellen von f(x) = %s." % qf(a, b, c), "x₁ = %s, x₂ = %s" % (zahl(lo), zahl(hi)),
                   ["x₁ = %s, x₂ = %s" % (zahl(-hi), zahl(-lo)), "x₁ = %s, x₂ = %s" % (zahl(lo), zahl(-hi)) if lo != -hi else "x₁ = %s, x₂ = %s" % (zahl(lo + 1), zahl(hi)), "x = %s" % zahl(c)],
                   "f(x) = 0 lösen (%s): <b>x₁ = %s, x₂ = %s</b>." % ("p-q-Formel" if a == 1 else "erst durch %s teilen" % zahl(a), zahl(lo), zahl(hi)))
    return mcq("In welchen Punkten schneidet die Parabel y = %s die x-Achse?" % qf(a, b, c), "%s und %s" % (P(lo, 0), P(hi, 0)),
               ["%s und %s" % (P(0, lo), P(0, hi)), "%s und %s" % (P(-hi, 0), P(-lo, 0)), "nur in %s" % P(0, c)],
               "y = 0 setzen und lösen: x = %s oder x = %s. <b>%s und %s</b>" % (zahl(lo), zahl(hi), P(lo, 0), P(hi, 0)))


def schnitt():
    x1, x2 = R.sample(range(-5, 6), 2)
    m, n = R.randint(-3, 3), R.randint(-4, 4)
    # Parabel y = x² + b x + c mit x² + (b - m) x + (c - n) = (x - x1)(x - x2)
    b = m - (x1 + x2)
    c = n + x1 * x2
    lo, hi = min(x1, x2), max(x1, x2)
    from de_k9 import gl
    return mcq("In welchen Punkten schneiden sich die Parabel y = %s und die Gerade %s?" % (qf(1, b, c), gl(m, n)), "%s und %s" % (P(lo, m * lo + n), P(hi, m * hi + n)),
               ["%s und %s" % (P(-hi, -m * hi + n), P(-lo, -m * lo + n)), "%s und %s" % (P(lo, 0), P(hi, 0)), "Sie schneiden sich nicht."],
               "Gleichsetzen: %s = %s, also %s = 0, x = %s oder x = %s. y aus der Geradengleichung. <b>%s und %s</b>" % (qf(1, b, c), qf(0, m, n).replace("x²", "") if m else zahl(n), qf(1, b - m, c - n), zahl(lo), zahl(hi), P(lo, m * lo + n), P(hi, m * hi + n)))


def raetsel():
    kind = R.choice(["folge", "quadrat", "produkt", "doppel"])
    if kind == "folge":
        n = R.randint(4, 20)
        return mcq("Das Produkt zweier aufeinanderfolgender natürlicher Zahlen ist %d. Wie heißen die Zahlen?" % (n * (n + 1)), "%d und %d" % (n, n + 1),
                   ["%d und %d" % (n - 1, n), "%d und %d" % (n + 1, n + 2), "%d und %d" % (n * (n + 1) // 2, 2)],
                   "x(x + 1) = %d ⇒ x² + x − %d = 0 ⇒ x = %d (die negative Lösung −%d ist keine natürliche Zahl). <b>%d und %d</b>" % (n * (n + 1), n * (n + 1), n, n + 1, n, n + 1))
    if kind == "quadrat":
        x = R.randint(3, 15)
        k = R.randint(2, 30)
        return mcq("Wenn man von einer positiven Zahl das Quadrat bildet und %d addiert, erhält man %d. Wie heißt die Zahl?" % (k, x * x + k), str(x), [str(x * x), "−%d" % x, str(x + 1)],
                   "x² + %d = %d ⇒ x² = %d ⇒ x = %d (positiv). <b>%d</b>" % (k, x * x + k, x * x, x, x))
    if kind == "produkt":
        x = R.randint(2, 12)
        d = R.randint(2, 8)
        return mcq("Eine Zahl ist um %d größer als eine andere positive Zahl. Ihr Produkt ist %d. Wie heißt die kleinere Zahl?" % (d, x * (x + d)), str(x), [str(x + d), "−%d" % (x + d), str(x + 1)],
                   "x(x + %d) = %d ⇒ x² + %dx − %d = 0 ⇒ x = %d oder x = −%d. Positiv: <b>%d</b>" % (d, x * (x + d), d, x * (x + d), x, x + d, x))
    x = R.randint(2, 15)
    return mcq("Das Quadrat einer positiven Zahl ist das %d-Fache der Zahl. Wie heißt die Zahl?" % x, str(x), ["0", str(x * x), str(2 * x)],
               "x² = %dx ⇒ x(x − %d) = 0 ⇒ x = 0 oder x = %d. Positiv: <b>%d</b>" % (x, x, x, x))


def geometrie():
    kind = R.choice(["rechteck", "rechteck", "quadrat", "rahmen", "dreieck"])
    if kind == "rechteck":
        b = R.randint(3, 15)
        d = R.randint(2, 10)
        A = b * (b + d)
        return mcq("Ein Rechteck ist %d cm länger als breit und hat den Flächeninhalt %d cm². Wie breit ist es?" % (d, A), "%d cm" % b, ["%d cm" % (b + d), "%d cm" % (b + 1), "%s cm" % zahl(Fr(A, 4))],
                   "x(x + %d) = %d ⇒ x² + %dx − %d = 0 ⇒ x = %d (die Lösung −%d ist als Länge nicht sinnvoll). <b>%d cm</b>" % (d, A, d, A, b, b + d, b))
    if kind == "quadrat":
        a = R.randint(3, 12)
        k = R.randint(1, 5)
        A2 = (a + k) ** 2
        return mcq("Verlängert man die Seiten eines Quadrats um %d cm, so hat es den Flächeninhalt %d cm². Wie lang war die Seite?" % (k, A2), "%d cm" % a, ["%d cm" % (a + k), "%d cm" % (a - k) if a - k > 0 else "%d cm" % (a + 2 * k), "%s cm" % zahl(Fr(A2 - k, 4))],
                   "(x + %d)² = %d ⇒ x + %d = %d ⇒ <b>x = %d cm</b>." % (k, A2, k, a + k, a))
    if kind == "rahmen":
        w, h = R.choice([(20, 30), (30, 40), (40, 50), (20, 25), (30, 50)])
        x = R.randint(2, 6)
        A = (w + 2 * x) * (h + 2 * x)
        return mcq("Ein Bild ist %d cm breit und %d cm hoch. Mit einem gleich breiten Rahmen ist die Gesamtfläche %s cm². Wie breit ist der Rahmen?" % (w, h, "{:,}".format(A).replace(",", " ") if A >= 10000 else str(A)), "%d cm" % x,
                   ["%d cm" % (2 * x), "%s cm" % zahl(Fr(A - w * h, w + h)) if Fr(A - w * h, w + h) != x else "%d cm" % (x + 1), "%d cm" % (x + 2)],
                   "(%d + 2x)(%d + 2x) = %d ⇒ 4x² + %dx − %d = 0 ⇒ <b>x = %d cm</b>." % (w, h, A, 2 * (w + h), A - w * h, x))
    g = R.randint(3, 12)
    k = R.randint(2, 5)
    A = Fr(g * (g + k), 2)
    if A.denominator != 1:
        return None
    return mcq("In einem Dreieck ist die Höhe %d cm länger als die Grundseite. Der Flächeninhalt ist %s cm². Wie lang ist die Grundseite?" % (k, zahl(A)), "%d cm" % g, ["%d cm" % (g + k), "%s cm" % zahl(A / 2), "%d cm" % (g * 2)],
               "%s %s x %s (x + %d) = %s ⇒ x² + %dx − %s = 0 ⇒ <b>x = %d cm</b>." % ("½", MAL, MAL, k, zahl(A), k, zahl(2 * A), g))


def bewegung():
    kind = R.choice(["fall", "wurf", "wurf", "hoehe"])
    if kind == "fall":
        t = R.randint(2, 6)
        h = 5 * t * t
        return mcq("Für den freien Fall gilt ungefähr h = 5t² (h in m, t in s). Wie lange braucht ein Stein, um %d m tief zu fallen?" % h, "%d s" % t, ["%d s" % (h // 5), "%s s" % zahl(Fr(h, 10)), "%d s" % (t * t)],
                   "5t² = %d ⇒ t² = %d ⇒ <b>t = %d s</b>." % (h, t * t, t))
    if kind == "wurf":
        T = R.randint(2, 6)
        v = 5 * T
        return mcq("Ein Ball wird senkrecht hochgeworfen. Seine Höhe ist h(t) = −5t² + %dt (h in m, t in s). Nach wie vielen Sekunden ist er wieder am Boden?" % v, "nach %d s" % T, ["nach %s s" % zahl(Fr(T, 2)), "nach %d s" % v, "nach 0 s"],
                   "−5t² + %dt = 0 ⇒ t(−5t + %d) = 0 ⇒ t = 0 (Abwurf) oder <b>t = %d s</b>." % (v, v, T))
    T = R.randint(2, 6)
    v = 10 * T
    hmax = 5 * T * T
    return mcq("Ein Ball fliegt auf der Bahn h(t) = −5t² + %dt. Wann erreicht er die größte Höhe, und wie hoch ist sie?" % v, "nach %d s, %d m" % (T, hmax), ["nach %d s, 0 m" % (2 * T), "nach %d s, %d m" % (T, 2 * hmax), "nach %d s, %d m" % (T, v)],
               "Nullstellen 0 und %d, der Scheitel liegt in der Mitte: t = %d, h = −5 %s %d + %d %s %d = <b>%d m</b>." % (2 * T, T, MAL, T * T, v, MAL, T, hmax))


def main():
    seen = set()
    sets = [
        ("Nullstellen von Parabeln", mix(R, seen, [(nullstellen, 20)])),
        ("Parabel und Gerade", mix(R, seen, [(schnitt, 20)])),
        ("Zahlenrätsel", mix(R, seen, [(raetsel, 20)])),
        ("Flächen", mix(R, seen, [(geometrie, 20)])),
        ("Bewegungen und Flächen", mix(R, seen, [(bewegung, 12), (geometrie, 8)])),
    ]
    body = lesson(
        ["1. Die Unbekannte festlegen (z. B. x = Breite in cm).",
         "2. Eine Gleichung aufstellen und in die Form ax² + bx + c = 0 bringen.",
         "3. Lösen (Ausklammern, p-q- oder abc-Formel).",
         "4. Prüfen: Passen beide Lösungen zum Text? Längen, Zeiten und Anzahlen können nicht negativ sein."],
        [example("Rechteck: 3 cm länger als breit, A = 40 cm²", ["x(x + 3) = 40", "x² + 3x − 40 = 0", "x = 5 oder x = −8"], "Breite 5 cm"),
         example("Parabel y = x² − 4 und x-Achse", ["x² − 4 = 0"], "(−2 | 0) und (2 | 0)")],
        [["x = −8 cm als Breite angeben", "Negative Längen verwerfen"],
         ["Nur eine Nullstelle angeben", "Meist gibt es zwei"],
         ["Gleichsetzen vergessen", "Schnittpunkte: beide Terme gleichsetzen"]])
    faq = [
        {"q": "Wie finde ich die Nullstellen einer Parabel?", "a": "f(x) = 0 setzen und die quadratische Gleichung lösen. Die Lösungen sind die x-Werte der Schnittpunkte mit der x-Achse."},
        {"q": "Wie schneide ich Parabel und Gerade?", "a": "Beide Terme gleichsetzen, alles auf eine Seite bringen und die quadratische Gleichung lösen. Die y-Werte bekommt man durch Einsetzen."},
        {"q": "Warum verwirft man manche Lösungen?", "a": "Die Gleichung kennt den Sachzusammenhang nicht. Negative Längen oder Zeiten vor dem Start ergeben keinen Sinn."},
        {"q": "Wann landet ein geworfener Ball?", "a": "Wenn die Höhe h(t) = 0 ist. Die Lösung t = 0 ist der Abwurf, die andere die Landung."},
    ]
    make_unit(R, "quadratische-gleichungen-in-sachaufgaben", "F",
              "Die Schülerinnen und Schüler bestimmen Nullstellen von Parabeln und Schnittpunkte mit Geraden, übersetzen Sachsituationen in quadratische Gleichungen, lösen sie und deuten die Lösungen im Kontext (Zusammenfassung).",
              "Quadratische Gleichungen in Sachaufgaben",
              "Quadratische Gleichungen Textaufgaben Klasse 9 – Nullstellen, Schnittpunkte, mit Lösungen",
              "Textaufgaben quadratisch",
              "Textaufgaben zu quadratischen Gleichungen für Klasse 9: Nullstellen, Parabel und Gerade, Zahlenrätsel, Flächen, Wurf und Fall. 100 Aufgaben mit Lösungen, kostenlos.",
              "Aufstellen, auf null bringen, lösen, prüfen.",
              "Negative Längen und Zeiten verwerfen.",
              body, faq, sets, 6, grade="klasse-9")


if __name__ == "__main__":
    main()
