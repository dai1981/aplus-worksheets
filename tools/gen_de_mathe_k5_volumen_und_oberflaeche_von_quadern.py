# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 5: Volumen und Oberfläche von Quadern（Leitidee Größen und Messen, Sek I）
  python3 tools/gen_de_mathe_k5_volumen_und_oberflaeche_von_quadern.py
Raumeinheiten (mm³, cm³, dm³, m³, ml, l) mit Umrechnungszahl 1000, Volumen von Quader und Würfel, Oberfläche, fehlende Kanten, Quader aus Einheitswürfeln, Sachaufgaben.
Würfel-Bauaufgaben (quader_wuerfel) aus gen_de_mathe_k4_wuerfel_und_quader.py mit neuem Zufall.
Fehler: Umrechnungszahl 100 statt 1000, Volumen und Oberfläche verwechselt, bei der Oberfläche nur 3 statt 6 Flächen gezählt.
"""
import random
import gen_de_mathe_k4_wuerfel_und_quader as k4
from de_common import mcq, num, lesson, example, make_unit, mix, Kids, MAL, table, wrap, text, line, GREEN, FILL, INK

R = random.Random(49517)
k4.R = random.Random(49567)
KIDS = Kids(R)
EIN = ["mm³", "cm³", "dm³", "m³"]


def quader_svg(a, b, c, u="cm"):
    sc = min(16, 150.0 / max(a, b, c))
    W, H, D = a * sc, c * sc, b * sc * 0.5
    x0, y0 = 40, 24 + D
    front = [(x0, y0), (x0 + W, y0), (x0 + W, y0 + H), (x0, y0 + H)]
    top = [(x0, y0), (x0 + D, y0 - D), (x0 + W + D, y0 - D), (x0 + W, y0)]
    side = [(x0 + W, y0), (x0 + W + D, y0 - D), (x0 + W + D, y0 - D + H), (x0 + W, y0 + H)]
    pg = lambda P, f: "<polygon points='%s' fill='%s' stroke='%s' stroke-width='2'/>" % (" ".join("%.1f,%.1f" % p for p in P), f, GREEN)
    s = [pg(front, FILL), pg(top, "#e6f2ea"), pg(side, "#d4eadb"),
         text(x0 + W / 2, y0 + H + 18, "%s %s" % (num(a), u), 13), text(x0 + W + D / 2 + 8, y0 + H - D / 2 + 14, "%s %s" % (num(b), u), 13, anchor="start"),
         text(x0 - 6, y0 + H / 2 + 4, "%s %s" % (num(c), u), 13, anchor="end")]
    return wrap(W + D + 110, H + D + 52, "".join(s), "Quader")


def umrechnen():
    i = R.randint(0, 2)
    big, small = EIN[i + 1], EIN[i]
    kind = R.choice(["gk", "kg", "liter", "liter"])
    if kind == "gk":
        n = R.randint(2, 40)
        return mcq("%d %s = ? %s" % (n, big, small), "%s %s" % (num(n * 1000), small), ["%s %s" % (num(x), small) for x in (n * 100, n * 10, n * 10000)],
                   "1 %s = 1000 %s. %d %s 1000 = <b>%s %s</b>." % (big, small, n, MAL, num(n * 1000), small))
    if kind == "kg":
        n = R.randint(2, 40)
        return mcq("%s %s = ? %s" % (num(n * 1000), small, big), "%d %s" % (n, big), ["%s %s" % (num(x), big) for x in (n * 10, n * 100)] + ["%d %s" % (n + 1, big)],
                   "1000 %s = 1 %s. %s : 1000 = <b>%d %s</b>." % (small, big, num(n * 1000), n, big))
    k = R.choice(["dm_l", "cm_ml", "l_cm", "m_l"])
    n = R.randint(2, 60)
    if k == "dm_l":
        return mcq("%d dm³ = ? l" % n, "%d l" % n, ["%s l" % num(x) for x in (n * 1000, n * 10, n * 100)], "1 dm³ = 1 l. <b>%d l</b>." % n)
    if k == "cm_ml":
        return mcq("%d cm³ = ? ml" % (n * 10), "%d ml" % (n * 10), ["%s ml" % num(x) for x in (n * 10000, n, n * 100)], "1 cm³ = 1 ml. <b>%d ml</b>." % (n * 10))
    if k == "l_cm":
        return mcq("%d l = ? cm³" % n, "%s cm³" % num(n * 1000), ["%s cm³" % num(x) for x in (n, n * 100, n * 10)], "1 l = 1 dm³ = 1000 cm³. <b>%s cm³</b>." % num(n * 1000))
    n = R.randint(2, 9)
    return mcq("%d m³ = ? l" % n, "%s l" % num(n * 1000), ["%s l" % num(x) for x in (n, n * 100, n * 1000000)], "1 m³ = 1000 dm³ = 1000 l. <b>%s l</b>." % num(n * 1000))


def volumen():
    cube = R.random() < 0.3
    a = R.randint(2, 12)
    b, c = (a, a) if cube else (R.randint(2, 10), R.randint(2, 9))
    if not cube and len({a, b, c}) < 3:
        return None
    V = a * b * c
    O = 2 * (a * b + b * c + a * c)
    name = "Würfels" if cube else "Quaders"
    return mcq(quader_svg(a, b, c) + "Wie groß ist das Volumen des %s?" % name, "%s cm³" % num(V), ["%s cm³" % num(x) for x in (a + b + c, a * b + b * c + a * c, O, a * b * 2)] + ["%s cm²" % num(V)],
               "V = %d cm %s %d cm %s %d cm = <b>%s cm³</b>." % (a, MAL, b, MAL, c, num(V)))


def oberflaeche():
    cube = R.random() < 0.3
    a = R.randint(2, 10)
    b, c = (a, a) if cube else (R.randint(2, 9), R.randint(2, 8))
    if not cube and len({a, b, c}) < 3:
        return None
    O = 2 * (a * b + b * c + a * c)
    if cube:
        return mcq(quader_svg(a, a, a) + "Wie groß ist die Oberfläche des Würfels?", "%s cm²" % num(O), ["%s cm²" % num(x) for x in (a * a, 4 * a * a, a * a * a, 12 * a)],
                   "Ein Würfel hat 6 gleiche Quadrate: 6 %s %d %s %d = <b>%s cm²</b>." % (MAL, a, MAL, a, num(O)))
    return mcq(quader_svg(a, b, c) + "Wie groß ist die Oberfläche des Quaders?", "%s cm²" % num(O), ["%s cm²" % num(x) for x in (a * b + b * c + a * c, a * b * c, 2 * (a * b + b * c), 4 * (a + b + c))],
               "O = 2 %s (%d %s %d + %d %s %d + %d %s %d) = 2 %s %d = <b>%s cm²</b>." % (MAL, a, MAL, b, b, MAL, c, a, MAL, c, MAL, a * b + b * c + a * c, num(O)))


def rueck():
    kind = R.choice(["hoehe", "hoehe", "kante"])
    if kind == "hoehe":
        a, b, c = R.randint(2, 12), R.randint(2, 10), R.randint(2, 10)
        V = a * b * c
        return mcq("Ein Quader hat das Volumen %s cm³. Er ist %d cm lang und %d cm breit. Wie hoch ist er?" % (num(V), a, b), "%d cm" % c, ["%d cm" % x for x in (V // a, V // b, V - a - b, a * b)],
                   "Grundfläche: %d %s %d = %d cm². %s : %d = <b>%d cm</b>." % (a, MAL, b, a * b, num(V), a * b, c))
    a = R.randint(2, 10)
    V = a ** 3
    return mcq("Ein Würfel hat das Volumen %s cm³. Wie lang ist eine Kante?" % num(V), "%d cm" % a, ["%d cm" % x for x in (V // 3, V // 6 if V // 6 != a else a + 2, a + 1, a * a)],
               "%d %s %d %s %d = %s: <b>%d cm</b>." % (a, MAL, a, MAL, a, num(V), a))


def sache():
    kind = R.choice(["aquarium", "aquarium2", "karton", "sand", "kiste", "milch", "geschenk", "pool"])
    p, er = KIDS.next()
    if kind == "aquarium":
        a, b, c = R.choice([60, 80, 100]), R.choice([30, 40, 50]), R.choice([30, 40, 50])
        V = a * b * c
        return mcq("Ein Aquarium ist %d cm lang, %d cm breit und %d cm hoch. Wie viel Liter Wasser passen hinein?" % (a, b, c), "%s l" % num(V // 1000), ["%s l" % num(x) for x in (V // 100, V, V // 10000 or 1)],
                   "%d %s %d %s %d = %s cm³ = %s dm³ = <b>%s l</b>." % (a, MAL, b, MAL, c, num(V), num(V // 1000), num(V // 1000)))
    if kind == "aquarium2":
        a, b = R.choice([5, 6, 8, 10]), R.choice([3, 4, 5])
        h = R.randint(2, 4)
        return mcq("Ein Becken ist innen %d dm lang und %d dm breit. Das Wasser steht %d dm hoch. Wie viel Liter Wasser sind darin?" % (a, b, h), "%d l" % (a * b * h), ["%d l" % x for x in (a * b, a + b + h, a * b * h * 10)],
                   "%d %s %d %s %d = %d dm³ = <b>%d l</b>." % (a, MAL, b, MAL, h, a * b * h, a * b * h))
    if kind == "karton":
        a, b, c = R.randint(20, 40), R.randint(10, 30), R.randint(10, 25)
        O = 2 * (a * b + b * c + a * c)
        return mcq("Ein Karton (Quader) ist %d cm lang, %d cm breit und %d cm hoch. Wie viel Pappe braucht man mindestens (ohne Klebeflächen)?" % (a, b, c), "%s cm²" % num(O),
                   ["%s cm²" % num(x) for x in (a * b + b * c + a * c, a * b * c, 2 * (a * b + b * c))], "O = 2 %s (%d + %d + %d) = <b>%s cm²</b>." % (MAL, a * b, b * c, a * c, num(O)))
    if kind == "sand":
        a, b, c = R.randint(2, 6), R.randint(2, 5), R.randint(1, 2)
        V = a * b * c
        return mcq("Für einen Gartenteich wird eine Grube ausgehoben: %d m lang, %d m breit und %d m tief. Wie viel Kubikmeter Erde werden ausgehoben?" % (a, b, c),
                   "%d m³" % V, ["%d m³" % x for x in (a + b + c, 2 * (a * b + b * c + a * c), a * b * c * 10)], "%d %s %d %s %d = <b>%d m³</b>." % (a, MAL, b, MAL, c, V))
    if kind == "kiste":
        n = R.choice([2, 3, 4, 5])
        a = R.choice([10, 20])
        L, B, H = n * a, R.randint(2, 4) * a, R.randint(1, 3) * a
        k = (L // a) * (B // a) * (H // a)
        return mcq("In eine Kiste (%d cm lang, %d cm breit, %d cm hoch) sollen Würfel mit %d cm Kantenlänge passen. Wie viele Würfel passen genau hinein?" % (L, B, H, a), str(k), [str(x) for x in (L * B * H // a, (L // a) + (B // a) + (H // a), (L // a) * (B // a))],
                   "Länge: %d, Breite: %d, Höhe: %d Würfel. %d %s %d %s %d = <b>%d</b>." % (L // a, B // a, H // a, L // a, MAL, B // a, MAL, H // a, k))
    if kind == "milch":
        a, b, c = 7, 7, R.choice([20, 21])
        V = a * b * c
        return mcq("Eine Saftpackung ist %d cm lang, %d cm breit und %d cm hoch. Passt 1 Liter Saft hinein?" % (a, b, c), "Ja, denn %s cm³ sind mehr als 1000 cm³." % num(V),
                   ["Nein, denn %s cm³ sind weniger als 1 Liter." % num(V), "Nein, denn 1 Liter sind 10 000 cm³.", "Ja, denn 1 Liter sind 100 cm³."],
                   "%d %s %d %s %d = %s cm³. 1 l = 1000 cm³: <b>Ja</b>." % (a, MAL, b, MAL, c, num(V)))
    if kind == "geschenk":
        a = R.randint(10, 30)
        O = 6 * a * a
        return mcq("%s beklebt alle Seiten einer würfelförmigen Geschenkbox mit Papier. Eine Kante ist %d cm lang. Wie viel Papier braucht %s?" % (p, a, er), "%s cm²" % num(O),
                   ["%s cm²" % num(x) for x in (a * a, 4 * a * a, a * a * a)], "6 %s %d %s %d = 6 %s %d = <b>%s cm²</b>." % (MAL, a, MAL, a, MAL, a * a, num(O)))
    a, b, c = R.randint(5, 12), R.randint(3, 6), R.choice([1, 2])
    V = a * b * c
    return mcq("Ein Schwimmbecken ist %d m lang, %d m breit und %d m tief. Wie viel Liter Wasser passen hinein?" % (a, b, c), "%s l" % num(V * 1000), ["%s l" % num(x) for x in (V, V * 100, V * 10000)],
               "%d %s %d %s %d = %d m³. 1 m³ = 1000 l: <b>%s l</b>." % (a, MAL, b, MAL, c, V, num(V * 1000)))


def main():
    seen = set()
    sets = [
        ("Würfel zählen und Raumeinheiten", mix(R, seen, [(k4.quader_wuerfel, 10), (umrechnen, 10)])),
        ("Volumen von Quader und Würfel", mix(R, seen, [(volumen, 20)])),
        ("Oberfläche", mix(R, seen, [(oberflaeche, 20)])),
        ("Fehlende Kanten und Umrechnen", mix(R, seen, [(rueck, 12), (umrechnen, 8)])),
        ("Sachaufgaben", mix(R, seen, [(sache, 20)])),
    ]
    body = lesson(
        ["Das <b>Volumen</b> (Rauminhalt) sagt, wie viele Einheitswürfel in einen Körper passen.",
         "Quader: V = a %s b %s c. Würfel: V = a %s a %s a." % (MAL, MAL, MAL, MAL),
         "Die <b>Oberfläche</b> ist die Summe aller 6 Flächen: O = 2 %s (a %s b + b %s c + a %s c). Würfel: O = 6 %s a %s a." % (MAL, MAL, MAL, MAL, MAL, MAL),
         "Raumeinheiten: mm³ → cm³ → dm³ → m³. Die <b>Umrechnungszahl ist 1000</b>. 1 dm³ = 1 l, 1 cm³ = 1 ml."],
        [example("Quader 5 cm, 4 cm, 3 cm", ["V = 5 %s 4 %s 3 = 60 cm³" % (MAL, MAL), "O = 2 %s (20 + 12 + 15) = 94 cm²" % MAL], "V = 60 cm³, O = 94 cm²"),
         example("3 dm³ in cm³", ["1 dm³ = 1000 cm³", "3 %s 1000" % MAL], "3000 cm³")],
        [["1 dm³ = 100 cm³", "1 dm³ = 1000 cm³ (10 %s 10 %s 10)" % (MAL, MAL)],
         ["Oberfläche nur mit 3 Flächen", "Jede Fläche gibt es zweimal: 6 Flächen"],
         ["Volumen in cm² angegeben", "Volumen: cm³, Oberfläche: cm²"]],
        extra=table(["Einheit", "entspricht"], [["1 cm³", "1000 mm³ = 1 ml"], ["1 dm³", "1000 cm³ = 1 l"], ["1 m³", "1000 dm³ = 1000 l"]]))
    faq = [
        {"q": "Wie berechnet man das Volumen eines Quaders?", "a": "Länge mal Breite mal Höhe: V = a · b · c. Alle Kanten müssen dieselbe Einheit haben."},
        {"q": "Was ist der Unterschied zwischen Volumen und Oberfläche?", "a": "Das Volumen ist der Platz im Inneren (cm³). Die Oberfläche ist die Fläche aller Seiten zusammen (cm²)."},
        {"q": "Wie viele Liter sind ein Kubikmeter?", "a": "1 m³ = 1000 dm³ = 1000 Liter."},
        {"q": "Warum ist die Umrechnungszahl bei Raumeinheiten 1000?", "a": "In einen Würfel mit 1 dm Kante passen 10 · 10 · 10 = 1000 Würfel mit 1 cm Kante."},
    ]
    make_unit(R, "volumen-und-oberflaeche-von-quadern", "G",
              "Die Schülerinnen und Schüler bestimmen Volumen und Oberflächeninhalt von Quadern und Würfeln, rechnen Raumeinheiten um und lösen Sachaufgaben (Zusammenfassung).",
              "Volumen und Oberfläche von Quadern",
              "Volumen und Oberfläche Klasse 5 – Quader und Würfel, Arbeitsblätter",
              "Volumen & Oberfläche",
              "Volumen und Oberfläche für Klasse 5: Quader und Würfel berechnen, Raumeinheiten und Liter umrechnen, Sachaufgaben. 100 Aufgaben mit Lösungen, kostenlos.",
              "Volumen: V = a · b · c. Oberfläche: alle 6 Flächen.",
              "Raumeinheiten: Umrechnungszahl 1000. 1 dm³ = 1 l.",
              body, faq, sets, 17, grade="klasse-5")


if __name__ == "__main__":
    main()
