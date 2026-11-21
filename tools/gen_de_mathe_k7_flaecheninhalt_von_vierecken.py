# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 7: Flächeninhalt von Trapez, Drachen und Raute（Leitidee Größen und Messen, Sek I）
  python3 tools/gen_de_mathe_k7_flaecheninhalt_von_vierecken.py
Trapez A = (a + c) · h : 2, Drachenviereck und Raute A = e · f : 2, Parallelogramm und Dreieck wiederholen, fehlende Größen, zusammengesetzte Vielecke, Sachaufgaben mit Einheiten.
Fehler: beim Trapez nicht durch 2 geteilt oder nur eine Grundseite genommen, bei der Raute e · f ohne : 2, Schenkel statt Höhe.
"""
import random
from fractions import Fraction as Fr
from de_common import lesson, example, make_unit, mix, Kids, MAL, table, wrap, line, text, INK, RED, GREEN, FILL, BLUE
from de_k6 import dz
from de_k7 import mcq, eur

R = random.Random(49714)
KIDS = Kids(R)
G = ":"
Q = "cm²"


def trapez_svg(a, c, h, off):
    sc = min(220.0 / a, 120.0 / h)
    x0, y0 = 96, 28 + h * sc
    pts = [(x0, y0), (x0 + a * sc, y0), (x0 + (off + c) * sc, y0 - h * sc), (x0 + off * sc, y0 - h * sc)]
    s = ["<polygon points='%s' fill='%s' stroke='%s' stroke-width='2.5'/>" % (" ".join("%.1f,%.1f" % p for p in pts), FILL, GREEN),
         line(pts[3][0], y0, pts[3][0], pts[3][1], RED, 2, " stroke-dasharray='5 4'"), text(x0 - 8, y0 - h * sc / 2 + 5, "h = %s cm" % dz(h), 16, anchor="end", col=RED),
         text(x0 + a * sc / 2, y0 + 22, "a = %s cm" % dz(a), 16), text(pts[3][0] + c * sc / 2, pts[3][1] - 9, "c = %s cm" % dz(c), 16)]
    return wrap(max(x0 + a * sc + 20, pts[3][0] + c * sc / 2 + 60), y0 + 32, "".join(s), "Trapez mit den parallelen Seiten a und c", lg=True)


def trapez():
    a, c, h = R.randint(6, 16), R.randint(2, 10), R.randint(3, 9)
    if c >= a:
        return None
    A = Fr((a + c) * h, 2)
    pic = trapez_svg(a, c, h, R.randint(1, a - c)) if R.random() < 0.6 else ""
    q = pic + ("Wie groß ist der Flächeninhalt des Trapezes?" if pic else "Ein Trapez hat die parallelen Seiten a = %d cm und c = %d cm und die Höhe h = %d cm. Wie groß ist der Flächeninhalt?" % (a, c, h))
    return mcq(q, "%s %s" % (dz(A), Q), ["%s %s" % (dz(x), Q) for x in ((a + c) * h, a * h, Fr(a * c * h, 2))] + ["%s cm" % dz(A)],
               "A = (a + c) %s h %s 2 = %d %s %d %s 2 = <b>%s %s</b>." % (MAL, G, a + c, MAL, h, G, dz(A), Q))


def raute():
    kind = R.choice(["raute", "drachen"])
    e, f = R.randint(4, 16), R.randint(3, 12)
    if kind == "raute" and e == f:
        return None
    A = Fr(e * f, 2)
    name = "eine Raute" if kind == "raute" else "ein Drachenviereck"
    return mcq("%s hat die Diagonalen e = %d cm und f = %d cm. Wie groß ist der Flächeninhalt?" % (name[0].upper() + name[1:], e, f), "%s %s" % (dz(A), Q), ["%s %s" % (dz(x), Q) for x in (e * f, 2 * (e + f), Fr(e * f, 4))],
               "Die Diagonalen stehen senkrecht aufeinander: A = e %s f %s 2 = %d %s %d %s 2 = <b>%s %s</b>." % (MAL, G, e, MAL, f, G, dz(A), Q))


def rueck():
    kind = R.choice(["trapez_h", "trapez_c", "raute_f", "para_h"])
    if kind == "trapez_h":
        a, c, h = R.randint(6, 16), R.randint(2, 10), R.randint(2, 12)
        A = Fr((a + c) * h, 2)
        return mcq("Ein Trapez hat a = %d cm, c = %d cm und den Flächeninhalt %s %s. Wie groß ist die Höhe?" % (a, c, dz(A), Q), "%d cm" % h, ["%s cm" % dz(x) for x in (A / (a + c), A / a, h * 2)],
                   "h = 2 %s A %s (a + c) = %s %s %d = <b>%d cm</b>." % (MAL, G, dz(2 * A), G, a + c, h))
    if kind == "trapez_c":
        a, c, h = R.randint(8, 16), R.randint(2, 7), R.randint(2, 10)
        A = Fr((a + c) * h, 2)
        return mcq("Ein Trapez hat a = %d cm, h = %d cm und den Flächeninhalt %s %s. Wie lang ist c?" % (a, h, dz(A), Q), "%d cm" % c, ["%s cm" % dz(x) for x in (A / h - a if A / h > a else c + 2, 2 * A / h, a + c)],
                   "a + c = 2 %s A %s h = %s %s %d = %d. c = %d − %d = <b>%d cm</b>." % (MAL, G, dz(2 * A), G, h, a + c, a + c, a, c))
    if kind == "raute_f":
        e, f = R.randint(4, 16), R.randint(3, 12)
        A = Fr(e * f, 2)
        return mcq("Eine Raute hat den Flächeninhalt %s %s und die Diagonale e = %d cm. Wie lang ist f?" % (dz(A), Q, e), "%d cm" % f, ["%s cm" % dz(x) for x in (A / e, A - e, f * 2)],
                   "f = 2 %s A %s e = %s %s %d = <b>%d cm</b>." % (MAL, G, dz(2 * A), G, e, f))
    g, h = R.randint(4, 15), R.randint(3, 12)
    return mcq("Ein Parallelogramm hat den Flächeninhalt %d %s und die Grundseite %d cm. Wie groß ist die Höhe?" % (g * h, Q, g), "%d cm" % h, ["%s cm" % dz(x) for x in (Fr(g * h, 2 * g), g * h - g, h + 2)],
               "h = A %s g = %d %s %d = <b>%d cm</b>." % (G, g * h, G, g, h))


def dez():
    kind = R.choice(["trapez", "raute", "einheit"])
    if kind == "trapez":
        a, c, h = Fr(R.randint(40, 120), 10), Fr(R.randint(15, 60), 10), Fr(R.randint(20, 80), 10)
        if c >= a:
            return None
        A = (a + c) * h / 2
        return mcq("Trapez: a = %s m, c = %s m, h = %s m. Berechne den Flächeninhalt." % (dz(a), dz(c), dz(h)), "%s m²" % dz(A), ["%s m²" % dz(x) for x in ((a + c) * h, a * h / 2, A * 10)],
                   "(%s + %s) %s %s %s 2 = <b>%s m²</b>." % (dz(a), dz(c), MAL, dz(h), G, dz(A)))
    if kind == "raute":
        e, f = Fr(R.randint(20, 90), 10), Fr(R.randint(20, 90), 10)
        A = e * f / 2
        return mcq("Raute: e = %s dm, f = %s dm. Berechne den Flächeninhalt." % (dz(e), dz(f)), "%s dm²" % dz(A), ["%s dm²" % dz(x) for x in (e * f, (e + f) * 2, A / 10)],
                   "%s %s %s %s 2 = <b>%s dm²</b>." % (dz(e), MAL, dz(f), G, dz(A)))
    a, c, h = R.randint(2, 9), R.randint(1, 5), R.randint(20, 90)
    if c >= a:
        return None
    A = Fr((a * 100 + c * 100) * h, 2)
    return mcq("Ein Trapez hat a = %d m, c = %d m und h = %d cm. Wie groß ist der Flächeninhalt in cm²?" % (a, c, h), "%s %s" % (dz(A), Q), ["%s %s" % (dz(x), Q) for x in (Fr((a + c) * h, 2), A / 10, A * 100)],
               "Erst in cm umrechnen: a = %d cm, c = %d cm. (%d + %d) %s %d %s 2 = <b>%s %s</b>." % (a * 100, c * 100, a * 100, c * 100, MAL, h, G, dz(A), Q))


def sache():
    p, er = KIDS.next()
    kind = R.choice(["drachen", "grund", "dach", "fliese", "wand"])
    if kind == "drachen":
        e, f = R.choice([60, 70, 80, 90]), R.choice([40, 50, 60])
        A = Fr(e * f, 2)
        return mcq("%s baut einen Drachen mit den Diagonalen %d cm und %d cm. Wie viel Stoff braucht %s (ohne Rand)?" % (p, e, f, er), "%s %s" % (dz(A), Q), ["%s %s" % (dz(x), Q) for x in (e * f, (e + f) * 2, A / 2)],
                   "%d %s %d %s 2 = <b>%s %s</b>." % (e, MAL, f, G, dz(A), Q))
    if kind == "grund":
        a, c, h = R.choice([(40, 24, 18), (50, 30, 20), (36, 20, 15), (60, 44, 25)])
        pr = R.choice([80, 120, 150, 200])
        A = (a + c) * h // 2
        return mcq("Ein Grundstück ist ein Trapez (a = %d m, c = %d m, h = %d m). 1 m² kostet %d €. Was kostet das Grundstück?" % (a, c, h, pr), eur(A * pr), [eur((a + c) * h * pr), eur(a * h * pr), eur(A)],
                   "A = (%d + %d) %s %d %s 2 = %d m². %d %s %d € = <b>%s</b>." % (a, c, MAL, h, G, A, A, MAL, pr, eur(A * pr)))
    if kind == "dach":
        a, c, h = R.choice([(10, 6, 4), (12, 8, 5), (9, 5, 4), (14, 10, 6)])
        A = (a + c) * h // 2
        return mcq("Eine Dachseite hat die Form eines Trapezes: unten %d m, oben %d m, Höhe %d m. Auf 1 m² passen 10 Dachziegel. Wie viele Ziegel braucht man?" % (a, c, h), str(A * 10), [str((a + c) * h * 10), str(A), str(a * h * 10)],
                   "A = (%d + %d) %s %d %s 2 = %d m². %d %s 10 = <b>%d</b>." % (a, c, MAL, h, G, A, A, MAL, A * 10))
    if kind == "fliese":
        e, f = R.choice([(20, 10), (30, 20), (24, 16)])
        A = e * f // 2
        n = R.choice([50, 100, 200])
        return mcq("Rautenförmige Fliesen haben die Diagonalen %d cm und %d cm. Wie viel Fläche bedecken %d Fliesen?" % (e, f, n), "%s %s" % (dz(A * n), Q), ["%s %s" % (dz(x), Q) for x in (e * f * n, A, A * n // 10)],
                   "Eine Fliese: %d %s %d %s 2 = %d %s. %d Fliesen: <b>%s %s</b>." % (e, MAL, f, G, A, Q, n, dz(A * n), Q))
    b, h = R.randint(4, 8), R.randint(3, 5)
    fa, fb = R.choice([(1, 1), (2, 1), (1, 2)])
    A = b * h - fa * fb
    return mcq("Eine Wand ist %d m breit und %d m hoch. Darin ist ein Fenster von %d m %s %d m. Wie groß ist die Fläche, die gestrichen wird?" % (b, h, fa, MAL, fb), "%s m²" % dz(A), ["%s m²" % dz(x) for x in (b * h, b * h + fa * fb, 2 * (b + h))],
               "%d %s %d − %d %s %d = <b>%s m²</b>." % (b, MAL, h, fa, MAL, fb, dz(A)))


def main():
    seen = set()
    sets = [
        ("Trapez", mix(R, seen, [(trapez, 20)])),
        ("Raute und Drachen", mix(R, seen, [(raute, 20)])),
        ("Fehlende Größen", mix(R, seen, [(rueck, 20)])),
        ("Dezimalzahlen und Einheiten", mix(R, seen, [(dez, 20)])),
        ("Sachaufgaben", mix(R, seen, [(sache, 20)])),
    ]
    body = lesson(
        ["<b>Trapez</b>: zwei parallele Seiten a und c, Abstand h. A = (a + c) %s h %s 2 – das ist der Mittelwert der parallelen Seiten mal Höhe." % (MAL, G),
         "<b>Raute und Drachenviereck</b>: Die Diagonalen e und f stehen senkrecht aufeinander. A = e %s f %s 2." % (MAL, G),
         "Die Höhe steht immer senkrecht auf der Grundseite. Schräge Seiten sind keine Höhen.",
         "Alle Längen müssen in derselben Einheit sein."],
        [example("Trapez a = 9 cm, c = 5 cm, h = 4 cm", ["(9 + 5) %s 4 %s 2" % (MAL, G)], "28 cm²"),
         example("Raute e = 8 cm, f = 6 cm", ["8 %s 6 %s 2" % (MAL, G)], "24 cm²")],
        [["Trapez: A = a %s h" % MAL, "Beide Grundseiten: (a + c) %s h %s 2" % (MAL, G)],
         ["Raute: A = e %s f" % MAL, "Durch 2 teilen: e %s f %s 2" % (MAL, G)],
         ["a = 2 m, h = 40 cm direkt multipliziert", "Erst in dieselbe Einheit umrechnen"]])
    faq = [
        {"q": "Wie berechnet man den Flächeninhalt eines Trapezes?", "a": "A = (a + c) · h : 2. a und c sind die parallelen Seiten, h ist ihr Abstand."},
        {"q": "Wie berechnet man die Fläche einer Raute?", "a": "Mit den Diagonalen: A = e · f : 2."},
        {"q": "Gilt die Formel e · f : 2 auch für den Drachen?", "a": "Ja, weil auch beim Drachenviereck die Diagonalen senkrecht aufeinander stehen."},
        {"q": "Wie finde ich die Höhe eines Trapezes, wenn A gegeben ist?", "a": "h = 2 · A : (a + c)."},
    ]
    make_unit(R, "flaecheninhalt-von-vierecken", "G",
              "Die Schülerinnen und Schüler berechnen Flächeninhalte von Trapezen, Rauten und Drachenvierecken, bestimmen fehlende Größen und lösen Sachaufgaben mit Einheiten (Zusammenfassung).",
              "Flächeninhalt von Trapez, Raute und Drachen",
              "Flächeninhalt Trapez, Raute, Drachen Klasse 7 – Arbeitsblätter mit Lösungen",
              "Trapez & Raute",
              "Flächeninhalt für Klasse 7: Trapez, Raute und Drachenviereck berechnen, fehlende Größen und Sachaufgaben. 100 Aufgaben mit Lösungen, kostenlos.",
              "Trapez: (a + c) · h : 2.",
              "Raute und Drachen: e · f : 2.",
              body, faq, sets, 14, grade="klasse-7")


if __name__ == "__main__":
    main()
