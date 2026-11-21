# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 5: Flächeninhalt und Umfang（Leitidee Größen und Messen, Sek I）
  python3 tools/gen_de_mathe_k5_flaecheninhalt_und_umfang.py
Flächeneinheiten (mm², cm², dm², m², a, ha, km²) mit Umrechnungszahl 100, Flächeninhalt und Umfang von Rechteck und Quadrat, fehlende Seiten, zusammengesetzte Figuren, Sachaufgaben.
Rechteck-Aufgaben (umfang, flaeche, rueckwaerts) aus gen_de_mathe_k4_umfang_und_flaecheninhalt.py mit neuem Zufall.
Fehler: Umrechnungszahl 10 statt 100, Umfang und Fläche verwechselt, bei zusammengesetzten Figuren eine Teilfläche doppelt gezählt.
"""
import random
import gen_de_mathe_k4_umfang_und_flaecheninhalt as k4
from de_common import mcq, num, eur, lesson, example, make_unit, mix, Kids, MAL, NB, table, wrap, text, FILL, GREEN

R = random.Random(49516)
k4.R = random.Random(49566)
KIDS = Kids(R)
EIN = ["mm²", "cm²", "dm²", "m²", "a", "ha", "km²"]


def umrechnen():
    i = R.randint(0, 5)
    big, small = EIN[i + 1], EIN[i]
    kind = R.choice(["gross_klein", "klein_gross", "zwei", "zwei"])
    if kind == "gross_klein":
        n = R.randint(2, 95)
        return mcq("%d %s = ? %s" % (n, big, small), "%s %s" % (num(n * 100), small), ["%s %s" % (num(x), small) for x in (n * 10, n * 1000, n * 100 + 100)],
                   "1 %s = 100 %s. %d %s 100 = <b>%s %s</b>." % (big, small, n, MAL, num(n * 100), small))
    if kind == "klein_gross":
        n = R.randint(2, 95)
        return mcq("%s %s = ? %s" % (num(n * 100), small, big), "%d %s" % (n, big), ["%s %s" % (num(x), big) for x in (n * 10, n * 1000)] + ["%d %s" % (n + 1, big)],
                   "100 %s = 1 %s. %s : 100 = <b>%d %s</b>." % (small, big, num(n * 100), n, big))
    a, b = R.randint(1, 30), R.randint(1, 99)
    t = a * 100 + b
    return mcq("%d %s %d %s = ? %s" % (a, big, b, small, small), "%s %s" % (num(t), small), ["%s %s" % (num(x), small) for x in (a * 10 + b, a * 1000 + b, a * 100 + b * 10 if b < 10 else a + b)],
               "%d %s = %s %s, dazu %d %s: <b>%s %s</b>." % (a, big, num(a * 100), small, b, small, num(t), small))


def vergleich():
    i = R.randint(0, 5)
    big, small = EIN[i + 1], EIN[i]
    n = R.randint(2, 40)
    m = n * 100 + R.choice([-50, -10, 0, 10, 50]) * (1 if n > 1 else 0)
    s = ">" if n * 100 > m else "<" if n * 100 < m else "="
    sym = {"<": "&lt;", ">": "&gt;", "=": "="}
    return mcq("Setze das richtige Zeichen ein: %d %s ☐ %s %s" % (n, big, num(m), small), sym[s], [sym[x] for x in "<>=" if x != s] + ["≈"],
               "%d %s = %s %s. Also %d %s <b>%s</b> %s %s." % (n, big, num(n * 100), small, n, big, sym[s], num(m), small))


def wahl():
    D = [("einem Fußballfeld", "ha", ["cm²", "mm²", "km²"]), ("einer Briefmarke", "cm²", ["m²", "ha", "km²"]), ("einem Klassenzimmer", "m²", ["mm²", "km²", "cm²"]), ("dem Saarland", "km²", ["m²", "a", "dm²"]),
         ("einem Schulheft", "dm²", ["km²", "ha", "mm²"]), ("einem Stecknadelkopf", "mm²", ["m²", "a", "dm²"]), ("einem Kleingarten", "a", ["mm²", "km²", "cm²"]), ("einer Tischplatte", "dm²", ["km²", "ha", "mm²"]),
         ("einem Bauernhof mit Feldern", "ha", ["cm²", "mm²", "dm²"]), ("der Stadt Berlin", "km²", ["m²", "dm²", "cm²"])]
    th, a, w = R.choice(D)
    return mcq("Welche Einheit passt am besten für die Fläche von %s?" % th, a, w, "Die Fläche von %s gibt man meist in <b>%s</b> an." % (th, a))


def lfig(a, b, c, d, label):
    """L-Form: außen a×b, rechts oben fehlt c×d"""
    sc = min(22, 230.0 / max(a, b))
    x0, y0 = 50, 26
    pts = [(0, 0), (a - c, 0), (a - c, d), (a, d), (a, b), (0, b)]
    poly = " ".join("%.0f,%.0f" % (x0 + x * sc, y0 + y * sc) for x, y in pts)
    s = ["<polygon points='%s' fill='%s' stroke='%s' stroke-width='2.5'/>" % (poly, FILL, GREEN),
         text(x0 + (a - c) * sc / 2, y0 - 8, "%d cm" % (a - c), 13), text(x0 + a * sc / 2, y0 + b * sc + 18, "%d cm" % a, 13),
         text(x0 - 6, y0 + b * sc / 2 + 4, "%d cm" % b, 13, anchor="end"), text(x0 + a * sc + 6, y0 + (d + b) * sc / 2 + 4, "%d cm" % (b - d), 13, anchor="start"),
         text(x0 + (a - c) * sc + c * sc / 2, y0 + d * sc - 6, "%d cm" % c, 12), text(x0 + (a - c) * sc - 4, y0 + d * sc / 2 + 4, "%d cm" % d, 12, anchor="end")]
    return wrap(a * sc + 110, b * sc + 50, "".join(s), label)


def zusammen():
    a, b = R.randint(6, 14), R.randint(5, 12)
    c, d = R.randint(2, a - 3), R.randint(2, b - 2)
    A = a * b - c * d
    U = 2 * (a + b)
    kind = R.choice(["A", "A", "U"])
    pic = lfig(a, b, c, d, "zusammengesetzte Figur (L-Form)")
    if kind == "A":
        return mcq(pic + "Wie groß ist der Flächeninhalt der Figur?", "%d cm²" % A, ["%d cm²" % x for x in (a * b, a * b + c * d, A + c * (b - d))] + ["%d cm" % A],
                   "Ergänzen: großes Rechteck %d %s %d = %d cm², fehlendes Stück %d %s %d = %d cm². %d − %d = <b>%d cm²</b>." % (a, MAL, b, a * b, c, MAL, d, c * d, a * b, c * d, A))
    return mcq(pic + "Wie groß ist der Umfang der Figur?", "%d cm" % U, ["%d cm" % x for x in (U - 2 * c, U - 2 * d, U - c - d)] + ["%d cm²" % U],
               "Alle Seiten addieren: %d + %d + %d + %d + %d + %d = <b>%d cm</b> (so groß wie beim ganzen Rechteck)." % (a - c, d, c, b - d, a, b, U))


def sache():
    kind = R.choice(["fliesen", "rasen", "teppich", "zaun", "grund", "wand", "acker", "beet"])
    p, er = KIDS.next()
    if kind == "fliesen":
        a, b = R.randint(3, 6), R.randint(2, 5)
        f = R.choice([20, 25, 50])
        n = (a * 100 // f) * (b * 100 // f)
        return mcq("Ein Badezimmer ist %d m lang und %d m breit. Es wird mit quadratischen Fliesen (%d cm %s %d cm) ausgelegt. Wie viele Fliesen braucht man?" % (a, b, f, MAL, f), num(n),
                   [num(x) for x in (a * b * f, a * b * 100 // f, n // 2)],
                   "Länge: %d cm : %d = %d Fliesen, Breite: %d cm : %d = %d. %d %s %d = <b>%s</b>." % (a * 100, f, a * 100 // f, b * 100, f, b * 100 // f, a * 100 // f, MAL, b * 100 // f, num(n)))
    if kind == "rasen":
        a, b = R.randint(8, 25), R.randint(6, 20)
        pr = R.choice([3, 4, 5])
        A = a * b
        return mcq("Ein Rasen ist %d m lang und %d m breit. Rasensamen für 1 m² kostet %d €. Was kostet der Samen für den ganzen Rasen?" % (a, b, pr), "%s €" % num(A * pr), ["%s €" % num(x) for x in (2 * (a + b) * pr, A, (a + b) * pr)],
                   "%d %s %d = %d m². %d %s %d € = <b>%s €</b>." % (a, MAL, b, A, A, MAL, pr, num(A * pr)))
    if kind == "teppich":
        a, b = R.randint(3, 7), R.randint(2, 5)
        A = a * b
        r = R.randint(A + 2, A + 15)
        return mcq("Ein Zimmer hat %d m². Ein Teppich ist %d m lang und %d m breit. Wie viel Quadratmeter Boden bleiben frei?" % (r, a, b), "%d m²" % (r - A), ["%d m²" % x for x in (r - 2 * (a + b), A, r - a - b)],
                   "Teppich: %d %s %d = %d m². %d − %d = <b>%d m²</b>." % (a, MAL, b, A, r, A, r - A))
    if kind == "zaun":
        a, b = R.randint(10, 40), R.randint(8, 30)
        t = R.choice([2, 3, 4])
        U = 2 * (a + b) - t
        return mcq("Ein rechteckiges Grundstück ist %d m lang und %d m breit. Es bekommt einen Zaun, nur für das Tor bleiben %d m frei. Wie viele Meter Zaun braucht man?" % (a, b, t), "%d m" % U,
                   ["%d m" % x for x in (2 * (a + b), a * b - t, a + b - t)], "Umfang: 2 %s %d + 2 %s %d = %d m. %d − %d = <b>%d m</b>." % (MAL, a, MAL, b, 2 * (a + b), 2 * (a + b), t, U))
    if kind == "grund":
        a, b = R.choice([(20, 30), (25, 40), (20, 50), (40, 50), (30, 30), (25, 20), (10, 40), (50, 60), (30, 40), (20, 20), (40, 40), (10, 70)])
        A = a * b
        return mcq("Ein Grundstück ist %d m lang und %d m breit. Wie viel Ar (a) sind das? (1 a = 100 m²)" % (a, b), "%s a" % num(A // 100),
                   ["%s a" % num(A // 10), "%s a" % num(A), "%s a" % num(2 * (a + b) // 10)], "%d %s %d = %s m² = <b>%s a</b>." % (a, MAL, b, num(A), num(A // 100)))
    if kind == "wand":
        a, h = R.randint(4, 8), R.choice([2, 3])
        f, g = R.randint(1, 2), R.randint(1, 2)
        A = a * h - f * g
        return mcq("Eine Wand ist %d m breit und %d m hoch. Ein Fenster (%d m %s %d m) wird nicht gestrichen. Wie viel Fläche wird gestrichen?" % (a, h, f, MAL, g), "%d m²" % A, ["%d m²" % x for x in (a * h, a * h + f * g, 2 * (a + h))],
                   "Wand: %d %s %d = %d m², Fenster: %d %s %d = %d m². %d − %d = <b>%d m²</b>." % (a, MAL, h, a * h, f, MAL, g, f * g, a * h, f * g, A))
    if kind == "acker":
        n = R.randint(2, 9)
        return mcq("Ein Bauer hat ein Feld von %d ha. Wie viel Quadratmeter sind das? (1 ha = 10 000 m²)" % n, "%s m²" % num(n * 10000), ["%s m²" % num(x) for x in (n * 100, n * 1000, n * 100000)],
                   "1 ha = 100 a = 10 000 m². %d %s 10 000 = <b>%s m²</b>." % (n, MAL, num(n * 10000)))
    a = R.randint(2, 9)
    A = a * a
    return mcq("%s legt ein quadratisches Beet an. Es soll %d m² groß sein. Wie lang ist eine Seite?" % (p, A), "%d m" % a, ["%d m" % x for x in (A // 4 if A // 4 != a else a + 2, A // 2, a + 1)],
               "Quadrat: Seite %s Seite = %d. %d %s %d = %d: <b>%d m</b>." % (MAL, A, a, MAL, a, A, a))


def main():
    seen = set()
    sets = [
        ("Flächeneinheiten umrechnen", mix(R, seen, [(umrechnen, 14), (vergleich, 3), (wahl, 3)])),
        ("Rechteck und Quadrat", mix(R, seen, [(k4.flaeche, 10), (k4.umfang, 10)])),
        ("Fehlende Seiten", mix(R, seen, [(k4.rueckwaerts, 14), (wahl, 3), (vergleich, 3)])),
        ("Zusammengesetzte Figuren", mix(R, seen, [(zusammen, 20)])),
        ("Sachaufgaben", mix(R, seen, [(sache, 20)])),
    ]
    body = lesson(
        ["Der <b>Flächeninhalt</b> sagt, wie viele Einheitsquadrate in eine Figur passen. Der <b>Umfang</b> ist die Länge des Randes.",
         "Rechteck: A = a %s b, u = 2 %s a + 2 %s b. Quadrat: A = a %s a, u = 4 %s a." % (MAL, MAL, MAL, MAL, MAL),
         "Flächeneinheiten: mm² → cm² → dm² → m² → a → ha → km². Die <b>Umrechnungszahl ist 100</b>.",
         "Zusammengesetzte Figuren zerlegt man in Rechtecke oder ergänzt sie zu einem großen Rechteck und zieht das fehlende Stück ab."],
        [example("Rechteck 8 cm lang, 5 cm breit", ["A = 8 %s 5 = 40 cm²" % MAL, "u = 2 %s 8 + 2 %s 5 = 26 cm" % (MAL, MAL)], "A = 40 cm², u = 26 cm"),
         example("3 m² in dm²", ["1 m² = 100 dm²", "3 %s 100" % MAL], "300 dm²")],
        [["1 m² = 10 dm²", "1 m² = 100 dm² (10 dm %s 10 dm)" % MAL],
         ["Fläche in cm angegeben", "Fläche hat die Einheit cm², Umfang die Einheit cm"],
         ["Umfang mit a %s b berechnet" % MAL, "Umfang: alle Seiten addieren"]],
        extra=table(["Einheit", "entspricht"], [["1 cm²", "100 mm²"], ["1 dm²", "100 cm²"], ["1 m²", "100 dm²"], ["1 a", "100 m²"], ["1 ha", "100 a"], ["1 km²", "100 ha"]]))
    faq = [
        {"q": "Warum ist die Umrechnungszahl bei Flächen 100?", "a": "1 m² ist ein Quadrat mit 10 dm Länge und 10 dm Breite. Es passen 10 · 10 = 100 dm² hinein."},
        {"q": "Was ist der Unterschied zwischen Umfang und Flächeninhalt?", "a": "Der Umfang ist die Länge des Randes (cm, m). Der Flächeninhalt ist die Größe der Fläche (cm², m²)."},
        {"q": "Was sind Ar und Hektar?", "a": "1 a = 100 m² (ein Quadrat mit 10 m Seitenlänge). 1 ha = 100 a = 10 000 m². Man benutzt sie für Grundstücke und Felder."},
        {"q": "Wie berechne ich die Fläche einer L-Form?", "a": "Zerlege sie in zwei Rechtecke und addiere, oder ergänze sie zu einem großen Rechteck und ziehe das fehlende Rechteck ab."},
    ]
    make_unit(R, "flaecheninhalt-und-umfang", "G",
              "Die Schülerinnen und Schüler berechnen Flächeninhalt und Umfang von Rechtecken, Quadraten und zusammengesetzten Figuren und rechnen Flächeneinheiten um (Zusammenfassung).",
              "Flächeninhalt und Umfang",
              "Flächeninhalt und Umfang Klasse 5 – Arbeitsblätter mit Lösungen",
              "Fläche & Umfang",
              "Flächeninhalt und Umfang für Klasse 5: Rechteck und Quadrat, Flächeneinheiten umrechnen, zusammengesetzte Figuren, Sachaufgaben. 100 Aufgaben mit Lösungen, kostenlos.",
              "Rechteck: A = a · b, u = 2 · a + 2 · b.",
              "Flächeneinheiten: Umrechnungszahl 100.",
              body, faq, sets, 16, grade="klasse-5")


if __name__ == "__main__":
    main()
