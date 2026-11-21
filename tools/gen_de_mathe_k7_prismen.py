# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 7: Prismen – Volumen und Oberfläche（Leitidee Größen und Messen, Sek I）
  python3 tools/gen_de_mathe_k7_prismen.py
Prismen erkennen (Grundfläche, Höhe), Ecken, Kanten, Flächen, Volumen V = G · h (Dreiecks- und Trapezprisma), Mantelfläche M = u · h, Oberfläche O = 2 · G + M, Einheiten, Sachaufgaben.
Fehler: die Höhe der Grundfläche mit der Körperhöhe verwechselt, Grundfläche nur einmal gezählt, Dreiecksfläche nicht durch 2 geteilt.
"""
import random
from fractions import Fraction as Fr
from de_common import lesson, example, make_unit, mix, Kids, MAL, table
from de_k6 import dz
from de_k7 import mcq

R = random.Random(49715)
KIDS = Kids(R)
G = ":"


def zaehlen():
    n = R.choice([3, 4, 5, 6, 8])
    name = {3: "dreiseitiges Prisma", 4: "vierseitiges Prisma", 5: "fünfseitiges Prisma", 6: "sechsseitiges Prisma", 8: "achtseitiges Prisma"}[n]
    kind = R.choice(["ecken", "kanten", "flaechen"])
    v = {"ecken": 2 * n, "kanten": 3 * n, "flaechen": n + 2}[kind]
    wort = {"ecken": "Ecken", "kanten": "Kanten", "flaechen": "Flächen"}[kind]
    w = [2 * n, 3 * n, n + 2, n, 4 * n]
    return mcq("Wie viele %s hat ein %s?" % (wort, name), str(v), [str(x) for x in w if x != v],
               "Ein n-seitiges Prisma hat 2n Ecken, 3n Kanten und n + 2 Flächen. Hier n = %d: <b>%d %s</b>." % (n, v, wort))


def volumen_drei():
    g, hg, h = R.randint(3, 12), R.randint(2, 10), R.randint(4, 20)
    G_ = Fr(g * hg, 2)
    V = G_ * h
    return mcq("Ein Prisma hat als Grundfläche ein Dreieck mit g = %d cm und h<sub>g</sub> = %d cm. Die Körperhöhe ist %d cm. Wie groß ist das Volumen?" % (g, hg, h), "%s cm³" % dz(V), ["%s cm³" % dz(x) for x in (g * hg * h, G_ + h, G_ * 2 + h * (g + hg))],
               "G = %d %s %d %s 2 = %s cm². V = G %s h = %s %s %d = <b>%s cm³</b>." % (g, MAL, hg, G, dz(G_), MAL, dz(G_), MAL, h, dz(V)))


def volumen_trap():
    a, c, hg, h = R.randint(5, 14), R.randint(2, 8), R.randint(2, 8), R.randint(5, 25)
    if c >= a:
        return None
    G_ = Fr((a + c) * hg, 2)
    V = G_ * h
    return mcq("Ein Prisma hat als Grundfläche ein Trapez mit a = %d cm, c = %d cm und h<sub>T</sub> = %d cm. Die Körperhöhe ist %d cm. Wie groß ist das Volumen?" % (a, c, hg, h), "%s cm³" % dz(V), ["%s cm³" % dz(x) for x in ((a + c) * hg * h, a * hg * h, G_ * h / 10)],
               "G = (%d + %d) %s %d %s 2 = %s cm². V = %s %s %d = <b>%s cm³</b>." % (a, c, MAL, hg, G, dz(G_), dz(G_), MAL, h, dz(V)))


def rueck():
    kind = R.choice(["h", "G"])
    G_, h = R.choice([12, 15, 18, 20, 24, 30, 35, 40, 45]), R.randint(3, 15)
    V = G_ * h
    if kind == "h":
        return mcq("Ein Prisma hat das Volumen %d cm³ und die Grundfläche %d cm². Wie hoch ist es?" % (V, G_), "%d cm" % h, ["%d cm" % x for x in (V - G_, V // 2 // G_ if V // 2 // G_ != h else h * 2, G_)],
                   "h = V %s G = %d %s %d = <b>%d cm</b>." % (G, V, G, G_, h))
    return mcq("Ein Prisma ist %d cm hoch und hat das Volumen %d cm³. Wie groß ist die Grundfläche?" % (h, V), "%d cm²" % G_, ["%d cm²" % x for x in (V - h, G_ * 2, V // 3 if V % 3 == 0 and V // 3 != G_ else G_ + 5)],
               "G = V %s h = %d %s %d = <b>%d cm²</b>." % (G, V, G, h, G_))


def oberflaeche():
    kind = R.choice(["rw", "gl"])
    h = R.randint(5, 20)
    if kind == "rw":
        a, b, c = R.choice([(3, 4, 5), (6, 8, 10), (5, 12, 13), (9, 12, 15)])
        G_ = Fr(a * b, 2)
        M = (a + b + c) * h
        O = 2 * G_ + M
        return mcq("Ein Prisma hat als Grundfläche ein rechtwinkliges Dreieck mit den Seiten %d cm, %d cm und %d cm (rechter Winkel zwischen %d cm und %d cm). Es ist %d cm hoch. Wie groß ist die Oberfläche?" % (a, b, c, a, b, h),
                   "%s cm²" % dz(O), ["%s cm²" % dz(x) for x in (G_ + M, M, 2 * a * b + M)],
                   "G = %d %s %d %s 2 = %s cm². M = u %s h = %d %s %d = %d cm². O = 2 %s %s + %d = <b>%s cm²</b>." % (a, MAL, b, G, dz(G_), MAL, a + b + c, MAL, h, M, MAL, dz(G_), M, dz(O)))
    a = R.choice([4, 6, 8, 10])
    hg = {4: Fr(35, 10), 6: Fr(52, 10), 8: Fr(69, 10), 10: Fr(87, 10)}[a]
    G_ = a * hg / 2
    M = 3 * a * h
    O = 2 * G_ + M
    return mcq("Ein Prisma hat als Grundfläche ein gleichseitiges Dreieck (Seite %d cm, Höhe etwa %s cm). Es ist %d cm hoch. Wie groß ist die Mantelfläche?" % (a, dz(hg), h), "%d cm²" % M, ["%s cm²" % dz(x) for x in (O, a * h, 2 * G_ + a * h)],
               "Die Mantelfläche besteht aus 3 Rechtecken: 3 %s %d %s %d = <b>%d cm²</b>." % (MAL, a, MAL, h, M))


def einheit():
    kind = R.choice(["cm_l", "m_l", "dm"])
    if kind == "cm_l":
        v = R.choice([1500, 2400, 3600, 750, 4800, 12000])
        return mcq("Ein Gefäß hat ein Volumen von %s cm³. Wie viel Liter sind das?" % dz(v), "%s l" % dz(Fr(v, 1000)), ["%s l" % dz(x) for x in (Fr(v, 100), Fr(v, 10000), v)],
                   "1 l = 1000 cm³. %s : 1000 = <b>%s l</b>." % (dz(v), dz(Fr(v, 1000))))
    if kind == "m_l":
        v = Fr(R.randint(5, 60), 10)
        return mcq("Ein Becken hat ein Volumen von %s m³. Wie viel Liter sind das?" % dz(v), "%s l" % dz(v * 1000), ["%s l" % dz(x) for x in (v * 100, v * 10, v * 10000)],
                   "1 m³ = 1000 l. <b>%s l</b>." % dz(v * 1000))
    v = R.choice([2, 5, 8, 12, 25])
    return mcq("Wie viele cm³ sind %d dm³?" % v, "%s cm³" % dz(v * 1000), ["%s cm³" % dz(x) for x in (v * 100, v * 10, v * 10000)], "1 dm³ = 1000 cm³: <b>%s cm³</b>." % dz(v * 1000))


def sache():
    p, er = KIDS.next()
    kind = R.choice(["zelt", "becken", "kanal", "dach", "schokolade"])
    if kind == "zelt":
        b, hg, l = R.choice([(2, 1.5, 3), (3, 2, 4), (2.4, 1.5, 2.5), (2, 1.6, 2.5)])
        b, hg, l = Fr(b).limit_denominator(10), Fr(hg).limit_denominator(10), Fr(l).limit_denominator(10)
        V = b * hg / 2 * l
        return mcq("Ein Zelt hat die Form eines Dreiecksprismas: Boden %s m breit, %s m lang, Firsthöhe %s m. Wie viel Luft (m³) ist im Zelt?" % (dz(b), dz(l), dz(hg)), "%s m³" % dz(V), ["%s m³" % dz(x) for x in (b * hg * l, b * l, V + 1)],
                   "G = %s %s %s %s 2 = %s m². V = %s %s %s = <b>%s m³</b>." % (dz(b), MAL, dz(hg), G, dz(b * hg / 2), dz(b * hg / 2), MAL, dz(l), dz(V)))
    if kind == "becken":
        l, b, t1, t2 = R.choice([(25, 10, 1, 2), (20, 8, 1, 3), (25, 12, 1, 2), (50, 20, 1, 2)])
        G_ = Fr((t1 + t2) * l, 2)
        V = G_ * b
        return mcq("Ein Schwimmbecken ist %d m lang und %d m breit. Es ist an einem Ende %d m und am anderen %d m tief (gleichmäßig abfallend). Wie viel Wasser passt hinein?" % (l, b, t1, t2), "%s m³" % dz(V), ["%s m³" % dz(x) for x in (l * b * t2, l * b * t1, l * b * (t1 + t2))],
                   "Grundfläche (Seitenansicht) ist ein Trapez: (%d + %d) %s %d %s 2 = %s m². V = %s %s %d = <b>%s m³</b>." % (t1, t2, MAL, l, G, dz(G_), dz(G_), MAL, b, dz(V)))
    if kind == "kanal":
        a, c, t, l = R.choice([(4, 2, 1, 100), (6, 3, 2, 50), (5, 3, 1, 200), (8, 4, 2, 150), (3, 1, 1, 80)])
        G_ = Fr((a + c) * t, 2)
        return mcq("Ein Graben hat einen trapezförmigen Querschnitt: oben %d m, unten %d m breit, %d m tief. Wie viel Erde wird für %d m Graben ausgehoben?" % (a, c, t, l), "%s m³" % dz(G_ * l), ["%s m³" % dz(x) for x in ((a + c) * t * l, a * t * l, G_)],
                   "Querschnitt: (%d + %d) %s %d %s 2 = %s m². V = %s %s %d = <b>%s m³</b>." % (a, c, MAL, t, G, dz(G_), dz(G_), MAL, l, dz(G_ * l)))
    if kind == "dach":
        b, h, l = R.choice([(8, 3, 10), (10, 4, 12), (9, 3, 11), (12, 5, 15), (11, 4, 14), (7, 3, 9)])
        V = Fr(b * h, 2) * l
        return mcq("Ein Dachboden hat die Form eines Dreiecksprismas: Breite %d m, Höhe %d m, Länge %d m. Wie groß ist der umbaute Raum?" % (b, h, l), "%s m³" % dz(V), ["%s m³" % dz(x) for x in (b * h * l, Fr(b * h, 2), V / 2)],
                   "%d %s %d %s 2 %s %d = <b>%s m³</b>." % (b, MAL, h, G, MAL, l, dz(V)))
    g, hg, l = R.choice([(3, 3, 20), (4, 3, 21), (3, 2, 25), (4, 4, 18)])
    V = Fr(g * hg, 2) * l
    return mcq("Eine Schokolade hat die Form eines Dreiecksprismas: Dreieck g = %d cm, h = %d cm, Länge %d cm. Wie groß ist ihr Volumen?" % (g, hg, l), "%s cm³" % dz(V), ["%s cm³" % dz(x) for x in (g * hg * l, Fr(g * hg, 2) + l, V / 10)],
               "%d %s %d %s 2 %s %d = <b>%s cm³</b>." % (g, MAL, hg, G, MAL, l, dz(V)))


def main():
    seen = set()
    sets = [
        ("Prismen erkennen", mix(R, seen, [(zaehlen, 14), (einheit, 6)])),
        ("Volumen von Dreiecksprismen", mix(R, seen, [(volumen_drei, 20)])),
        ("Trapezprismen und fehlende Größen", mix(R, seen, [(volumen_trap, 12), (rueck, 8)])),
        ("Mantel und Oberfläche", mix(R, seen, [(oberflaeche, 14), (einheit, 6)])),
        ("Sachaufgaben", mix(R, seen, [(sache, 20)])),
    ]
    body = lesson(
        ["Ein <b>Prisma</b> hat zwei deckungsgleiche, parallele Grundflächen (Vielecke). Die Seitenflächen sind Rechtecke und bilden den Mantel.",
         "<b>Volumen</b>: V = G %s h (Grundfläche mal Körperhöhe)." % MAL,
         "<b>Mantelfläche</b>: M = u %s h (Umfang der Grundfläche mal Höhe). <b>Oberfläche</b>: O = 2 %s G + M." % (MAL, MAL),
         "Achtung: Die Höhe der Grundfläche (z. B. des Dreiecks) ist nicht die Körperhöhe."],
        [example("Dreiecksprisma: g = 6 cm, h<sub>g</sub> = 4 cm, h = 10 cm", ["G = 6 %s 4 %s 2 = 12 cm²" % (MAL, G), "V = 12 %s 10" % MAL], "120 cm³"),
         example("O bei G = 6 cm², u = 12 cm, h = 5 cm", ["M = 12 %s 5 = 60 cm²" % MAL, "O = 2 %s 6 + 60" % MAL], "72 cm²")],
        [["Dreiecksfläche g %s h ohne : 2" % MAL, "G = g %s h %s 2" % (MAL, G)],
         ["O = G + M", "Zwei Grundflächen: O = 2 %s G + M" % MAL],
         ["Höhe des Dreiecks als Körperhöhe genommen", "Die Körperhöhe ist der Abstand der beiden Grundflächen"]])
    faq = [
        {"q": "Wie berechnet man das Volumen eines Prismas?", "a": "Grundfläche mal Höhe: V = G · h. Das gilt für jedes Prisma, auch für den Quader."},
        {"q": "Was ist die Mantelfläche?", "a": "Die Summe aller Seitenflächen. Man berechnet sie mit M = u · h."},
        {"q": "Wie berechnet man die Oberfläche?", "a": "O = 2 · G + M: zwei Grundflächen und der Mantel."},
        {"q": "Wie viele Ecken hat ein sechsseitiges Prisma?", "a": "12 Ecken, 18 Kanten und 8 Flächen."},
    ]
    make_unit(R, "prismen", "G",
              "Die Schülerinnen und Schüler erkennen Prismen, berechnen Volumen, Mantel- und Oberfläche von Dreiecks- und Trapezprismen und lösen Sachaufgaben (Zusammenfassung).",
              "Prismen: Volumen und Oberfläche",
              "Prisma Volumen und Oberfläche Klasse 7 – Arbeitsblätter mit Lösungen",
              "Prismen",
              "Prismen für Klasse 7: Ecken und Kanten, Volumen V = G · h, Mantel- und Oberfläche, Sachaufgaben. 100 Aufgaben mit Lösungen, kostenlos.",
              "Volumen: V = G · h.",
              "Oberfläche: O = 2 · G + M.",
              body, faq, sets, 15, grade="klasse-7")


if __name__ == "__main__":
    main()
