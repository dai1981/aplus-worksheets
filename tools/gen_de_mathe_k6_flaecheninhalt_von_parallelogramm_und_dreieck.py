# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 6: Flächeninhalt von Parallelogramm und Dreieck（Leitidee Größen und Messen, Sek I）
  python3 tools/gen_de_mathe_k6_flaecheninhalt_von_parallelogramm_und_dreieck.py
Parallelogramm A = g · h, Dreieck A = g · h : 2, Höhe erkennen, fehlende Grundseite oder Höhe, Trapez, zusammengesetzte Flächen, Sachaufgaben.
Fehler: schräge Seite statt Höhe genommen, beim Dreieck nicht durch 2 geteilt, Einheit cm statt cm².
"""
import random
from fractions import Fraction as Fr
from de_common import lesson, example, make_unit, mix, Kids, MAL, table, wrap, line, text, INK, RED, GREEN, FILL, BLUE
from de_k6 import dz, mcq

R = random.Random(49617)
KIDS = Kids(R)
G = ":"
Q = "cm²"


def para_svg(g, h, s, sl):
    sc = min(16, 220.0 / (g + abs(sl)), 140.0 / h)
    x0, y0 = 40, 20 + h * sc
    pts = [(x0, y0), (x0 + g * sc, y0), (x0 + (g + sl) * sc, y0 - h * sc), (x0 + sl * sc, y0 - h * sc)]
    poly = " ".join("%.1f,%.1f" % p for p in pts)
    hx = x0 + sl * sc + 6 if sl > 0 else x0 + 20
    out = ["<polygon points='%s' fill='%s' stroke='%s' stroke-width='2.5'/>" % (poly, FILL, GREEN),
           line(hx, y0, hx, y0 - h * sc, RED, 2, " stroke-dasharray='5 4'"), text(hx + 6, y0 - h * sc / 2 + 4, "h = %s cm" % dz(h), 13, anchor="start", col=RED),
           text(x0 + g * sc / 2, y0 + 18, "g = %s cm" % dz(g), 13), text((pts[1][0] + pts[2][0]) / 2 + 8, (pts[1][1] + pts[2][1]) / 2, "%s cm" % dz(s), 12, anchor="start", col="#666")]
    return wrap(x0 + (g + max(sl, 0)) * sc + 90, y0 + 30, "".join(out), "Parallelogramm mit Grundseite und Höhe")


def drei_svg(g, h, sl, s):
    sc = min(16, 220.0 / max(g, g + sl), 140.0 / h)
    x0, y0 = 40, 20 + h * sc
    top = (x0 + sl * sc, y0 - h * sc)
    out = ["<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='%s' stroke='%s' stroke-width='2.5'/>" % (x0, y0, x0 + g * sc, y0, top[0], top[1], FILL, GREEN),
           line(top[0], y0, top[0], top[1], RED, 2, " stroke-dasharray='5 4'"), text(top[0] + 6, y0 - h * sc / 2 + 4, "h = %s cm" % dz(h), 13, anchor="start", col=RED),
           text(x0 + g * sc / 2, y0 + 18, "g = %s cm" % dz(g), 13), text((x0 + top[0]) / 2 - 6, (y0 + top[1]) / 2, "%s cm" % dz(s), 12, anchor="end", col="#666")]
    return wrap(x0 + max(g, sl) * sc + 90, y0 + 30, "".join(out), "Dreieck mit Grundseite und Höhe")


def para():
    g, h = R.randint(7, 14), R.randint(3, 9)
    sl = R.randint(1, 4)
    s = round((h * h + sl * sl) ** 0.5)
    if s == h:
        s += 1
    A = g * h
    return mcq(para_svg(g, h, s, sl) + "Wie groß ist der Flächeninhalt des Parallelogramms?", "%d %s" % (A, Q), ["%d %s" % (x, Q) for x in (g * s, A // 2 if A % 2 == 0 else A + g, 2 * (g + s))] + ["%d cm" % A],
               "A = g %s h = %d cm %s %d cm = <b>%d %s</b>. (Die schräge Seite %d cm ist nicht die Höhe.)" % (MAL, g, MAL, h, A, Q, s))


def drei():
    g, h = R.randint(3, 14), R.randint(2, 10)
    if g * h % 2:
        if R.random() < 0.5:
            return None
    sl = R.randint(1, g - 1)
    s = round((h * h + sl * sl) ** 0.5)
    A = Fr(g * h, 2)
    return mcq(drei_svg(g, h, sl, s) + "Wie groß ist der Flächeninhalt des Dreiecks?", "%s %s" % (dz(A), Q), ["%s %s" % (dz(x), Q) for x in (g * h, Fr(g * s, 2) if s != h else g * h + 1, g + h)],
               "A = g %s h %s 2 = %d %s %d %s 2 = <b>%s %s</b>." % (MAL, G, g, MAL, h, G, dz(A), Q))


def rueck():
    kind = R.choice(["para_h", "para_g", "drei_h", "drei_g"])
    g, h = R.randint(3, 15), R.randint(2, 12)
    if kind.startswith("para"):
        A = g * h
        if kind == "para_h":
            return mcq("Ein Parallelogramm hat den Flächeninhalt %d %s und die Grundseite %d cm. Wie groß ist die Höhe?" % (A, Q, g), "%d cm" % h, ["%d cm" % x for x in (A - g, 2 * h, A // 2 if A // 2 != h else h + 1)],
                       "h = A %s g = %d %s %d = <b>%d cm</b>." % (G, A, G, g, h))
        return mcq("Ein Parallelogramm hat den Flächeninhalt %d %s und die Höhe %d cm. Wie lang ist die Grundseite?" % (A, Q, h), "%d cm" % g, ["%d cm" % x for x in (A - h, 2 * g, g + 1)],
                   "g = A %s h = %d %s %d = <b>%d cm</b>." % (G, A, G, h, g))
    A = Fr(g * h, 2)
    if A.denominator != 1:
        return None
    if kind == "drei_h":
        return mcq("Ein Dreieck hat den Flächeninhalt %s %s und die Grundseite %d cm. Wie groß ist die Höhe?" % (dz(A), Q, g), "%d cm" % h, ["%s cm" % dz(x) for x in (A / g, A - g if A > g else A + g, h + 1)],
                   "h = 2 %s A %s g = %s %s %d = <b>%d cm</b>." % (MAL, G, dz(2 * A), G, g, h))
    return mcq("Ein Dreieck hat den Flächeninhalt %s %s und die Höhe %d cm. Wie lang ist die Grundseite?" % (dz(A), Q, h), "%d cm" % g, ["%s cm" % dz(x) for x in (A / h, A - h if A > h else A + h, g + 2)],
               "g = 2 %s A %s h = %s %s %d = <b>%d cm</b>." % (MAL, G, dz(2 * A), G, h, g))


def trapez():
    a, c, h = R.randint(6, 14), R.randint(2, 8), R.randint(2, 9)
    if c >= a:
        return None
    A = Fr((a + c) * h, 2)
    return mcq("Ein Trapez hat die parallelen Seiten a = %d cm und c = %d cm und die Höhe h = %d cm. Wie groß ist der Flächeninhalt?" % (a, c, h), "%s %s" % (dz(A), Q), ["%s %s" % (dz(x), Q) for x in ((a + c) * h, a * c * h, a * h)],
               "A = (a + c) %s h %s 2 = %d %s %d %s 2 = <b>%s %s</b>." % (MAL, G, a + c, MAL, h, G, dz(A), Q))


def dez():
    kind = R.choice(["para", "drei"])
    g = Fr(R.randint(25, 120), 10)
    h = Fr(R.randint(15, 80), 10)
    if kind == "para":
        A = g * h
        return mcq("Parallelogramm: g = %s cm, h = %s cm. Berechne den Flächeninhalt." % (dz(g), dz(h)), "%s %s" % (dz(A), Q), ["%s %s" % (dz(x), Q) for x in (A / 2, A * 10, g + h)],
                   "%s %s %s = <b>%s %s</b>." % (dz(g), MAL, dz(h), dz(A), Q))
    A = g * h / 2
    return mcq("Dreieck: g = %s cm, h = %s cm. Berechne den Flächeninhalt." % (dz(g), dz(h)), "%s %s" % (dz(A), Q), ["%s %s" % (dz(x), Q) for x in (g * h, A * 10, (g + h) / 2)],
               "%s %s %s %s 2 = <b>%s %s</b>." % (dz(g), MAL, dz(h), G, dz(A), Q))


def sache():
    p, er = KIDS.next()
    k = R.choice(["segel", "giebel", "beet", "wimpel", "grund", "drachen"])
    if k == "segel":
        g, h = R.randint(2, 4), R.randint(3, 7)
        return mcq("Ein dreieckiges Segel hat die Grundseite %d m und die Höhe %d m. Wie viel Stoff braucht man (ohne Saum)?" % (g, h), "%s m²" % dz(Fr(g * h, 2)), ["%s m²" % dz(x) for x in (g * h, g + h, 2 * (g + h))],
                   "%d %s %d %s 2 = <b>%s m²</b>." % (g, MAL, h, G, dz(Fr(g * h, 2))))
    if k == "giebel":
        b, h = R.choice([8, 9, 10, 12]), R.choice([3, 4, 5])
        pr = R.choice([3, 4, 5])
        A = Fr(b * h, 2)
        return mcq("Ein Hausgiebel ist ein Dreieck: %d m breit und %d m hoch. Farbe für 1 m² kostet %d €. Was kostet die Farbe?" % (b, h, pr), "%s €" % dz(A * pr), ["%s €" % dz(x) for x in (b * h * pr, A, (b + h) * pr)],
                   "Fläche: %d %s %d %s 2 = %s m². %s %s %d € = <b>%s €</b>." % (b, MAL, h, G, dz(A), dz(A), MAL, pr, dz(A * pr)))
    if k == "beet":
        g, h = R.randint(3, 9), R.randint(2, 6)
        return mcq("Ein Beet hat die Form eines Parallelogramms mit g = %d m und h = %d m. Wie groß ist es?" % (g, h), "%d m²" % (g * h), ["%s m²" % dz(x) for x in (Fr(g * h, 2), 2 * (g + h), g + h)],
                   "%d %s %d = <b>%d m²</b>." % (g, MAL, h, g * h))
    if k == "wimpel":
        g, h = R.choice([20, 24, 30]), R.choice([30, 35, 40])
        n = R.randint(5, 12)
        A = g * h // 2
        return mcq("%s bastelt %d dreieckige Wimpel (g = %d cm, h = %d cm). Wie viel Stoff braucht %s insgesamt?" % (p, n, g, h, er), "%s %s" % (dz(A * n), Q), ["%s %s" % (dz(x), Q) for x in (g * h * n, A, (g + h) * n)],
                   "Ein Wimpel: %d %s %d %s 2 = %d %s. %d Wimpel: <b>%s %s</b>." % (g, MAL, h, G, A, Q, n, dz(A * n), Q))
    if k == "grund":
        a, c, h = R.choice([(30, 20, 15), (40, 24, 20), (25, 15, 12), (50, 30, 20)])
        A = (a + c) * h // 2
        return mcq("Ein Grundstück hat die Form eines Trapezes: parallele Seiten %d m und %d m, Abstand %d m. Wie groß ist es?" % (a, c, h), "%d m²" % A, ["%d m²" % x for x in ((a + c) * h, a * h, a * c)],
                   "(%d + %d) %s %d %s 2 = <b>%d m²</b>." % (a, c, MAL, h, G, A))
    e, f = R.randint(4, 12) * 10, R.randint(3, 9) * 10
    return mcq("Ein Drachen hat zwei Diagonalen von %d cm und %d cm, die senkrecht aufeinander stehen. Er besteht aus zwei Dreiecken mit der Grundseite %d cm. Wie groß ist seine Fläche?" % (e, f, e), "%s %s" % (dz(Fr(e * f, 2)), Q), ["%s %s" % (dz(x), Q) for x in (e * f, Fr(e * f, 4), e + f)],
               "Zwei Dreiecke: 2 %s (%d %s %d %s 2) = %d %s %d %s 2 = <b>%s %s</b>." % (MAL, e, MAL, f // 2, G, e, MAL, f, G, dz(Fr(e * f, 2)), Q))


def main():
    seen = set()
    sets = [
        ("Parallelogramm", mix(R, seen, [(para, 20)])),
        ("Dreieck", mix(R, seen, [(drei, 20)])),
        ("Fehlende Seiten und Höhen", mix(R, seen, [(rueck, 20)])),
        ("Trapez und Dezimalzahlen", mix(R, seen, [(trapez, 10), (dez, 10)])),
        ("Sachaufgaben", mix(R, seen, [(sache, 20)])),
    ]
    body = lesson(
        ["Die <b>Höhe</b> h steht senkrecht auf der Grundseite g. Die schräge Seite ist nicht die Höhe.",
         "<b>Parallelogramm</b>: Man kann es in ein Rechteck umlegen. A = g %s h." % MAL,
         "<b>Dreieck</b>: Zwei gleiche Dreiecke ergeben ein Parallelogramm. A = g %s h %s 2." % (MAL, G),
         "<b>Trapez</b>: A = (a + c) %s h %s 2 (a und c sind die parallelen Seiten)." % (MAL, G)],
        [example("Parallelogramm g = 7 cm, h = 4 cm", ["7 %s 4" % MAL], "28 cm²"),
         example("Dreieck g = 9 cm, h = 6 cm", ["9 %s 6 %s 2" % (MAL, G)], "27 cm²")],
        [["A = g %s schräge Seite" % MAL, "Immer die senkrechte Höhe nehmen"],
         ["Dreieck: A = g %s h" % MAL, "Durch 2 teilen: A = g %s h %s 2" % (MAL, G)],
         ["A = 28 cm", "Flächen in cm²"]])
    faq = [
        {"q": "Wie berechnet man den Flächeninhalt eines Parallelogramms?", "a": "Grundseite mal Höhe: A = g · h. Die Höhe steht senkrecht auf der Grundseite."},
        {"q": "Warum teilt man beim Dreieck durch 2?", "a": "Zwei gleiche Dreiecke lassen sich zu einem Parallelogramm zusammenlegen. Ein Dreieck ist also halb so groß."},
        {"q": "Welche Seite ist die Höhe?", "a": "Keine Seite, sondern der senkrechte Abstand von der Grundseite zur gegenüberliegenden Ecke (oder Seite)."},
        {"q": "Wie berechnet man ein Trapez?", "a": "A = (a + c) · h : 2. a und c sind die beiden parallelen Seiten."},
    ]
    make_unit(R, "flaecheninhalt-von-parallelogramm-und-dreieck", "G",
              "Die Schülerinnen und Schüler berechnen Flächeninhalte von Parallelogrammen, Dreiecken und Trapezen, bestimmen fehlende Größen und lösen Sachaufgaben (Zusammenfassung).",
              "Flächeninhalt von Parallelogramm und Dreieck",
              "Flächeninhalt Parallelogramm und Dreieck Klasse 6 – Arbeitsblätter",
              "Parallelogramm & Dreieck",
              "Flächeninhalt für Klasse 6: Parallelogramm, Dreieck und Trapez berechnen, Höhe finden, Sachaufgaben. 100 Aufgaben mit Lösungen, kostenlos.",
              "Parallelogramm: g · h. Dreieck: g · h : 2.",
              "Die Höhe steht immer senkrecht auf der Grundseite.",
              body, faq, sets, 17, grade="klasse-6")


if __name__ == "__main__":
    main()
