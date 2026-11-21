# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 4: Umfang und Flächeninhalt（Leitidee Größen und Messen / Raum und Form）
  python3 tools/gen_de_mathe_k4_umfang_und_flaecheninhalt.py
Kästchen zählen (cm²), Umfang von Rechteck und Quadrat, Flächeninhalt mit Länge mal Breite, zusammengesetzte Figuren, Sachaufgaben.
Fehler: Umfang und Fläche verwechselt, nur zwei Seiten addiert, cm statt cm², beim Quadrat 4 · a für die Fläche.
"""
import random
from de_common import mcq, num, lesson, example, make_unit, mix, Kids, MAL, NB, wrap, table
from ws_common import line, text, INK, GREEN, FILL

R = random.Random(49115)
KIDS = Kids(R)
K = 22


def grid(cells, w, h, label):
    """cells: Menge (x, y) gefüllter Kästchen auf einem w × h Gitter"""
    s = []
    for i in range(w + 1):
        s.append(line(10 + i * K, 10, 10 + i * K, 10 + h * K, "#bcd6e6", 1))
    for j in range(h + 1):
        s.append(line(10, 10 + j * K, 10 + w * K, 10 + j * K, "#bcd6e6", 1))
    for (x, y) in cells:
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='#cfe6d6' stroke='%s' stroke-width='1.5'/>" % (10 + x * K, 10 + y * K, K, K, GREEN))
    return wrap(w * K + 20, h * K + 20, "".join(s), label)


def umfang_cells(cells):
    p = 0
    for (x, y) in cells:
        for d in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            if (x + d[0], y + d[1]) not in cells:
                p += 1
    return p


def rect_svg(a, b, la, lb, label="Rechteck"):
    sc = min(26, 220.0 / max(a, b))
    W, H = a * sc, b * sc
    s = ["<rect x='60' y='26' width='%.0f' height='%.0f' fill='%s' stroke='%s' stroke-width='2.5'/>" % (W, H, FILL, GREEN),
         text(60 + W / 2, 18, la, 14), text(52, 26 + H / 2 + 5, lb, 14, anchor="end")]
    return wrap(W + 80, H + 40, "".join(s), label)


def cm(v, sq=False):
    return "%s%s%s" % (num(v), NB, "cm²" if sq else "cm")


def kaestchen():
    w, h = R.randint(2, 7), R.randint(2, 5)
    shape = R.choice(["rect", "L"])
    cells = {(x, y) for x in range(w) for y in range(h)}
    if shape == "L":
        cx, cy = R.randint(1, w - 1), R.randint(1, h - 1)
        cells -= {(x, y) for x in range(w - cx, w) for y in range(0, cy)}
    n = len(cells)
    p = umfang_cells(cells)
    ask = R.choice(["fl", "um"])
    pic = grid(cells, w + 1, h + 1, "Figur auf Kästchenpapier")
    if ask == "fl":
        return mcq(pic + "Jedes Kästchen ist 1 cm². Wie groß ist der Flächeninhalt der Figur?", cm(n, True),
                   [cm(p, True), cm(n, False), cm(n + 1, True) if p == n + 1 else cm(n - 1, True)],
                   "Zähle die Kästchen: %d Kästchen = <b>%s</b>." % (n, cm(n, True)))
    if p == n:
        return None
    return mcq(pic + "Jede Kästchenseite ist 1 cm lang. Wie groß ist der Umfang der Figur?", cm(p),
               [cm(n), cm(p, True), cm(p - 2), cm(p + 2)],
               "Gehe einmal um die Figur herum und zähle die Seiten: <b>%s</b>." % cm(p))


def umfang():
    sq = R.random() < 0.3
    a = R.randint(3, 25)
    b = a if sq else R.randint(2, 20)
    if not sq and a == b:
        return None
    u = 2 * (a + b)
    pic = rect_svg(a, b, cm(a), cm(b), "Quadrat" if sq else "Rechteck")
    name = "Quadrat" if sq else "Rechteck"
    w = [a + b, a * b, u + a if not sq else 2 * a]
    return mcq(pic + "Wie groß ist der Umfang des %ss?" % name, cm(u), [cm(x) for x in w if x != u] + [cm(a * b, True)],
               ("Umfang = 4 %s %d cm = <b>%s</b>." % (MAL, a, cm(u))) if sq else
               "Umfang = %d cm + %d cm + %d cm + %d cm = <b>%s</b>." % (a, b, a, b, cm(u)))


def flaeche():
    sq = R.random() < 0.3
    a = R.randint(2, 15)
    b = a if sq else R.randint(2, 12)
    if not sq and a == b:
        return None
    A = a * b
    name = "Quadrat" if sq else "Rechteck"
    w = [2 * (a + b), a + b, A + a]
    pic = rect_svg(a, b, cm(a), cm(b), name)
    return mcq(pic + "Wie groß ist der Flächeninhalt des %ss?" % name, cm(A, True), [cm(x, True) for x in w if x != A] + [cm(A)],
               "Flächeninhalt = Länge %s Breite = %d cm %s %d cm = <b>%s</b>." % (MAL, a, MAL, b, cm(A, True)))


def rueckwaerts():
    kind = R.choice(["b_aus_A", "b_aus_U", "seite_quadrat"])
    if kind == "b_aus_A":
        a, b = R.randint(3, 12), R.randint(2, 10)
        if a == b:
            return None
        A = a * b
        return mcq("Ein Rechteck hat den Flächeninhalt %s. Es ist %s lang. Wie breit ist es?" % (cm(A, True), cm(a)), cm(b),
                   [cm(x) for x in (A - a, A // 2 - a if A // 2 - a > 0 else b + 2, b + 1) if x != b],
                   "Länge %s Breite = Fläche: %d %s ? = %d. %d : %d = <b>%s</b>." % (MAL, a, MAL, A, A, a, cm(b)))
    if kind == "b_aus_U":
        a, b = R.randint(4, 20), R.randint(2, 15)
        if a == b:
            return None
        U = 2 * (a + b)
        return mcq("Ein Rechteck hat den Umfang %s. Es ist %s lang. Wie breit ist es?" % (cm(U), cm(a)), cm(b),
                   [cm(x) for x in (U - a, U - 2 * a, U // 2) if x != b and x > 0],
                   "Länge + Breite = %d : 2 = %d cm. %d cm − %d cm = <b>%s</b>." % (U, a + b, a + b, a, cm(b)))
    a = R.randint(3, 15)
    U = 4 * a
    return mcq("Ein Quadrat hat den Umfang %s. Wie lang ist eine Seite?" % cm(U), cm(a),
               [cm(x) for x in (U // 2, U - 4, a + 4 if a + 4 != U // 2 else a + 1)],
               "Ein Quadrat hat 4 gleich lange Seiten: %d cm : 4 = <b>%s</b>." % (U, cm(a)))


def sache():
    kind = R.choice(["zaun", "fliesen", "rasen", "bilderrahmen", "beet", "vergleich"])
    p = KIDS.next()
    if kind == "zaun":
        a, b = R.randint(8, 30), R.randint(5, 20)
        if a == b:
            return None
        U = 2 * (a + b)
        return mcq("Ein rechteckiger Garten ist %d m lang und %d m breit. Wie viel Meter Zaun braucht man ringsherum?" % (a, b), "%d%sm" % (U, NB),
                   ["%d%sm" % (x, NB) for x in (a + b, a * b, U + a) if x != U],
                   "Umfang: 2 %s (%d m + %d m) = <b>%d m</b>." % (MAL, a, b, U))
    if kind == "fliesen":
        a, b = R.randint(3, 9), R.randint(2, 6)
        if a == b:
            return None
        A = a * b
        return mcq("Ein Badezimmerboden ist %d m lang und %d m breit. Wie viele Quadratmeter Fliesen braucht man?" % (a, b), "%d%sm²" % (A, NB),
                   ["%d%sm²" % (x, NB) for x in (2 * (a + b), a + b, A + 1) if x != A],
                   "Flächeninhalt: %d m %s %d m = <b>%d m²</b>." % (a, MAL, b, A))
    if kind == "rasen":
        a, b = R.randint(6, 20), R.randint(4, 12)
        c, d = R.randint(2, a // 2), R.randint(2, b // 2)
        A = a * b - c * d
        return mcq("Eine Rasenfläche ist %d m lang und %d m breit. In der Ecke liegt ein Sandkasten, %d m lang und %d m breit. Wie viel m² Rasen bleiben?" % (a, b, c, d),
                   "%d%sm²" % (A, NB), ["%d%sm²" % (x, NB) for x in (a * b, a * b + c * d, a * b - c - d) if x != A],
                   "%d %s %d = %d m², Sandkasten %d %s %d = %d m². %d − %d = <b>%d m²</b>." % (a, MAL, b, a * b, c, MAL, d, c * d, a * b, c * d, A))
    if kind == "bilderrahmen":
        a, b = R.choice([(20, 30), (15, 20), (30, 40), (24, 18), (10, 15), (40, 50)])
        U = 2 * (a + b)
        return mcq("%s klebt ein Band rund um ein Bild. Das Bild ist %d cm breit und %d cm hoch. Wie lang muss das Band sein?" % (p[0], a, b), cm(U),
                   [cm(x) for x in (a + b, U - a, a * b) if x != U],
                   "Umfang: %d + %d + %d + %d = <b>%s</b>." % (a, b, a, b, cm(U)))
    if kind == "beet":
        a = R.randint(2, 4)
        n = R.randint(3, 6)
        A = a * a * n
        return mcq("Ein Schulgarten hat %d quadratische Beete. Jedes Beet ist %d m lang. Wie groß sind die Beete zusammen?" % (n, a), "%d%sm²" % (A, NB),
                   ["%d%sm²" % (x, NB) for x in (4 * a * n, a * n, a * a + n) if x != A],
                   "Ein Beet: %d m %s %d m = %d m². %d Beete: %d %s %d = <b>%d m²</b>." % (a, MAL, a, a * a, n, n, MAL, a * a, A))
    a, b = R.randint(3, 9), R.randint(2, 8)
    c = R.randint(2, 10)
    if a == b or a * b == c * c or 2 * (a + b) == 4 * c:
        return None
    big = "das Rechteck" if a * b > c * c else "das Quadrat"
    return mcq("Ein Rechteck ist %d cm lang und %d cm breit. Ein Quadrat hat %d cm lange Seiten. Welche Figur hat den größeren Flächeninhalt?" % (a, b, c),
               "%s (%s)" % (big.split()[1], cm(max(a * b, c * c), True)),
               ["%s (%s)" % ("Quadrat" if big == "das Rechteck" else "Rechteck", cm(min(a * b, c * c), True)), "Beide sind gleich groß",
                "Das kann man nicht vergleichen"],
               "Rechteck: %d %s %d = %d cm². Quadrat: %d %s %d = %d cm². Größer ist <b>%s</b>." % (a, MAL, b, a * b, c, MAL, c, c * c, big.split()[1]))


def main():
    seen = set()
    sets = [
        ("Kästchen zählen", mix(R, seen, [(kaestchen, 20)])),
        ("Umfang berechnen", mix(R, seen, [(umfang, 20)])),
        ("Flächeninhalt berechnen", mix(R, seen, [(flaeche, 20)])),
        ("Rückwärts rechnen", mix(R, seen, [(rueckwaerts, 20)])),
        ("Sachaufgaben", mix(R, seen, [(sache, 20)])),
    ]
    body = lesson(
        ["Der <b>Umfang</b> ist der Weg einmal ganz um die Figur herum. Man misst ihn in cm oder m.",
         "Der <b>Flächeninhalt</b> sagt, wie viel Platz die Figur bedeckt. Man misst ihn in Quadratzentimetern (cm²) oder Quadratmetern (m²).",
         "Rechteck: Umfang = Länge + Breite + Länge + Breite. Flächeninhalt = Länge %s Breite." % MAL,
         "Quadrat: alle 4 Seiten sind gleich lang. Umfang = 4 %s Seite, Flächeninhalt = Seite %s Seite." % (MAL, MAL)],
        [example("Rechteck 6 cm lang, 4 cm breit", ["Umfang: 6 + 4 + 6 + 4 = 20 cm", "Fläche: 6 %s 4 = 24 cm²" % MAL], "U = 20 cm, A = 24 cm²"),
         example("Quadrat mit 5 cm Seitenlänge", ["Umfang: 4 %s 5 = 20 cm" % MAL, "Fläche: 5 %s 5 = 25 cm²" % MAL], "U = 20 cm, A = 25 cm²")],
        [["Nur zwei Seiten addieren (6 + 4 = 10 cm)", "Alle vier Seiten: 20 cm"],
         ["Fläche in cm angeben", "Fläche immer in cm² oder m²"],
         ["Umfang und Fläche verwechseln", "Zaun → Umfang, Teppich → Fläche"]],
        extra=table(["", "Umfang", "Flächeninhalt"], [["Rechteck", "2 %s (Länge + Breite)" % MAL, "Länge %s Breite" % MAL], ["Quadrat", "4 %s Seite" % MAL, "Seite %s Seite" % MAL]]))
    faq = [
        {"q": "Was ist der Unterschied zwischen Umfang und Flächeninhalt?", "a": "Der Umfang ist eine Länge (der Rand), der Flächeninhalt ist die bedeckte Fläche. Für einen Zaun braucht man den Umfang, für einen Teppich den Flächeninhalt."},
        {"q": "Was bedeutet cm²?", "a": "Ein Quadratzentimeter ist ein Quadrat mit 1 cm langen Seiten. Ein Rechteck mit 24 cm² bedeckt so viel Platz wie 24 solche Quadrate."},
        {"q": "Können zwei Figuren gleiche Fläche, aber verschiedenen Umfang haben?", "a": "Ja. Ein Rechteck 6 cm × 4 cm und eines 12 cm × 2 cm haben beide 24 cm², aber die Umfänge 20 cm und 28 cm."},
        {"q": "Wie findet man die Breite, wenn die Fläche bekannt ist?", "a": "Man teilt die Fläche durch die Länge: 24 cm² : 6 cm = 4 cm."},
    ]
    make_unit(R, "umfang-und-flaecheninhalt", "G",
              "Die Schülerinnen und Schüler bestimmen Flächeninhalte durch Auslegen und Zählen von Einheitsquadraten, berechnen Umfang und Flächeninhalt von Rechteck und Quadrat und lösen Sachaufgaben (Zusammenfassung).",
              "Umfang und Flächeninhalt von Rechteck und Quadrat",
              "Umfang und Flächeninhalt Klasse 4 – Arbeitsblätter mit Lösungen",
              "Umfang und Fläche",
              "Umfang und Flächeninhalt für Klasse 4: Kästchen zählen, Rechteck und Quadrat berechnen, rückwärts rechnen und Sachaufgaben. 100 Übungsaufgaben mit Lösungen, kostenlos.",
              "Umfang = einmal herum. Fläche = Länge mal Breite.",
              "Umfang in cm, Flächeninhalt in cm².",
              body, faq, sets, 15, grade="klasse-4")


if __name__ == "__main__":
    main()
