# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 9: Pythagoras in Figuren und Körpern（Leitidee Größen und Messen, Sek I）
  python3 tools/gen_de_mathe_k9_pythagoras_in_figuren_und_koerpern.py
Diagonalen von Rechteck und Quadrat, Höhe im gleichseitigen und gleichschenkligen Dreieck, Abstand zweier Punkte im Koordinatensystem,
Raumdiagonale von Würfel und Quader, Höhen und Mantellinien von Pyramide und Kegel.
Fehler: Raumdiagonale mit nur zwei Kanten, Höhe im gleichseitigen Dreieck mit der ganzen Seite statt der halben, Koordinatendifferenzen addiert statt quadriert.
"""
import random, math
from fractions import Fraction as Fr
from de_common import lesson, example, make_unit, mix, MAL, num
from de_k6 import dz
from de_k9 import mcq, zahl, zr, par

R = random.Random(49908)
W = "√"


def L(v, u="cm", k=1):
    return "%s %s" % (zr(v, k) if abs(v - round(v)) > 1e-9 else num(int(round(v))), u)


def ebene():
    kind = R.choice(["rechteck", "quadrat", "gleichseitig", "gleichschenklig", "raute"])
    if kind == "rechteck":
        a, b = R.randint(3, 20), R.randint(3, 20)
        if a == b:
            return None
        d = math.hypot(a, b)
        return mcq("Ein Rechteck ist %d cm lang und %d cm breit. Wie lang ist seine Diagonale (auf eine Nachkommastelle)?" % (a, b), L(d), [L(a + b), L(a * a + b * b), L(math.sqrt(abs(a * a - b * b)))],
                   "d = %s(%d² + %d²) = %s%d ≈ <b>%s</b>." % (W, a, b, W, a * a + b * b, L(d)))
    if kind == "quadrat":
        a = R.randint(2, 20)
        return mcq("Ein Quadrat hat die Seitenlänge %d cm. Wie lang ist die Diagonale (auf eine Nachkommastelle)?" % a, L(a * math.sqrt(2)), [L(2 * a), L(a * a), L(a * math.sqrt(3))],
                   "d = %s(%d² + %d²) = %d%s2 ≈ <b>%s</b>." % (W, a, a, a, W, L(a * math.sqrt(2))))
    if kind == "gleichseitig":
        a = R.choice([2, 4, 6, 8, 10, 12, 14, 16, 20])
        h = a * math.sqrt(3) / 2
        return mcq("Ein gleichseitiges Dreieck hat die Seitenlänge %d cm. Wie hoch ist es (auf eine Nachkommastelle)?" % a, L(h), [L(math.sqrt(a * a * 2)), L(a / 2), L(math.sqrt(a * a - a))],
                   "Die Höhe halbiert die Grundseite: h² = %d² − %d² = %d, h ≈ <b>%s</b>." % (a, a // 2, a * a - (a // 2) ** 2, L(h)))
    if kind == "gleichschenklig":
        g, s = R.choice([(6, 5), (10, 13), (16, 10), (24, 13), (8, 5), (12, 10), (14, 25), (18, 15)])
        h = math.sqrt(s * s - (g / 2) ** 2)
        return mcq("Ein gleichschenkliges Dreieck hat die Basis %d cm und die Schenkel %d cm. Wie hoch ist es?" % (g, s), L(h), [L(math.sqrt(s * s - g * g)) if s > g else L(math.hypot(s, g / 2)), L(math.hypot(s, g / 2)), L(s - g / 2)],
                   "h² = %d² − %d² = %d, <b>h = %s</b>." % (s, g // 2, s * s - (g // 2) ** 2, L(h)))
    e, f = R.choice([(6, 8), (10, 24), (12, 16), (16, 30), (18, 24), (14, 48)])
    a = math.hypot(e / 2, f / 2)
    return mcq("Eine Raute hat die Diagonalen %d cm und %d cm. Wie lang ist eine Seite?" % (e, f), L(a), [L(math.hypot(e, f)), L((e + f) / 2), L(e * f / 2)],
               "Die Diagonalen halbieren sich senkrecht: a² = %d² + %d², <b>a = %s</b>." % (e // 2, f // 2, L(a)))


def koord():
    x1, y1 = R.randint(-6, 6), R.randint(-6, 6)
    dx, dy = R.choice([(3, 4), (6, 8), (5, 12), (4, 3), (8, 6), (1, 2), (2, 5), (3, 3), (4, 7), (2, 2)])
    dx *= R.choice([-1, 1])
    dy *= R.choice([-1, 1])
    x2, y2 = x1 + dx, y1 + dy
    d = math.hypot(dx, dy)
    exact = abs(d - round(d)) < 1e-9
    return mcq("Berechne den Abstand der Punkte A(%s | %s) und B(%s | %s)%s." % (zahl(x1), zahl(y1), zahl(x2), zahl(y2), "" if exact else " (auf eine Nachkommastelle)"), L(d, "LE"),
               [L(abs(dx) + abs(dy), "LE"), L(dx * dx + dy * dy, "LE"), L(math.hypot(x1 + x2, y1 + y2), "LE") if math.hypot(x1 + x2, y1 + y2) != d else L(d + 1, "LE")],
               "Δx = %s, Δy = %s. d = %s(%s² + %s²) = %s%d %s <b>%s</b>." % (zahl(abs(dx)), zahl(abs(dy)), W, abs(dx), abs(dy), W, dx * dx + dy * dy, "=" if exact else "≈", L(d, "LE")))


def raum():
    kind = R.choice(["wuerfel", "quader", "quader", "flaeche"])
    if kind == "wuerfel":
        a = R.randint(2, 15)
        return mcq("Wie lang ist die Raumdiagonale eines Würfels mit der Kantenlänge %d cm (auf eine Nachkommastelle)?" % a, L(a * math.sqrt(3)), [L(a * math.sqrt(2)), L(3 * a), L(a * a * 3)],
                   "d = %s(a² + a² + a²) = %d%s3 ≈ <b>%s</b>." % (W, a, W, L(a * math.sqrt(3))))
    a, b, c = R.choice([(3, 4, 12), (2, 3, 6), (1, 4, 8), (2, 6, 9), (4, 4, 7), (6, 6, 7), (2, 10, 11), (5, 8, 10), (3, 6, 9), (10, 20, 30)])
    d = math.sqrt(a * a + b * b + c * c)
    if kind == "quader":
        return mcq("Ein Quader ist %d cm lang, %d cm breit und %d cm hoch. Wie lang ist die Raumdiagonale%s?" % (c, b, a, "" if abs(d - round(d)) < 1e-9 else " (auf eine Nachkommastelle)"), L(d),
                   [L(math.hypot(b, c)), L(a + b + c), L(a * a + b * b + c * c)],
                   "d = %s(%d² + %d² + %d²) = %s%d %s <b>%s</b>." % (W, c, b, a, W, a * a + b * b + c * c, "=" if abs(d - round(d)) < 1e-9 else "≈", L(d)))
    a2 = R.randint(2, 12)
    return mcq("Ein Würfel hat die Kantenlänge %d cm. Wie lang ist eine Flächendiagonale (auf eine Nachkommastelle)?" % a2, L(a2 * math.sqrt(2)), [L(a2 * math.sqrt(3)), L(2 * a2), L(a2 * a2 * 2)],
               "Flächendiagonale: %s(%d² + %d²) = %d%s2 ≈ <b>%s</b>." % (W, a2, a2, a2, W, L(a2 * math.sqrt(2))))


def raum2():
    a, b, c = R.choice([(3, 4, 12), (2, 3, 6), (1, 4, 8), (2, 6, 9), (4, 4, 7), (6, 6, 7), (2, 10, 11), (5, 8, 10), (3, 6, 9), (10, 20, 30)])
    d = math.sqrt(a * a + b * b + c * c)
    s = int(d) + R.choice([-2, -1, 1, 3])
    ok = s <= d
    ans = ("Ja, die Raumdiagonale ist etwa %s lang." % L(d)) if ok else ("Nein, die Raumdiagonale ist nur etwa %s lang." % L(d))
    other = ("Nein, die Raumdiagonale ist nur etwa %s lang." % L(d)) if ok else ("Ja, die Raumdiagonale ist etwa %s lang." % L(d))
    return mcq("Passt ein %d cm langer Stab in eine Kiste mit den Innenmaßen %d cm × %d cm × %d cm?" % (s, c, b, a), ans,
               [other, ("Nein, die längste Kante ist nur %d cm." % c) if ok else ("Ja, die Kiste hat insgesamt %d cm Kantenlänge." % (4 * (a + b + c))), "Das kann man nicht berechnen."],
               "Die längste Strecke in der Kiste ist die Raumdiagonale %s(%d² + %d² + %d²) ≈ %s. <b>%s</b>" % (W, c, b, a, L(d), "Ja" if ok else "Nein"))


def koerper():
    kind = R.choice(["kegel_s", "kegel_h", "pyr_h", "pyr_hs"])
    if kind == "kegel_s":
        r, h = R.choice([(3, 4), (5, 12), (6, 8), (8, 15), (4, 7), (5, 9), (2, 6)])
        s = math.hypot(r, h)
        return mcq("Ein Kegel hat den Radius %d cm und die Höhe %d cm. Wie lang ist die Mantellinie s?" % (r, h), L(s), [L(r + h), L(math.hypot(2 * r, h)), L(math.sqrt(abs(h * h - r * r)))],
                   "Radius, Höhe und Mantellinie bilden ein rechtwinkliges Dreieck: s = %s(%d² + %d²) %s <b>%s</b>." % (W, r, h, "=" if abs(s - round(s)) < 1e-9 else "≈", L(s)))
    if kind == "kegel_h":
        r, s = R.choice([(3, 5), (5, 13), (6, 10), (8, 17), (4, 9), (7, 25)])
        h = math.sqrt(s * s - r * r)
        return mcq("Ein Kegel hat den Radius %d cm und die Mantellinie %d cm. Wie hoch ist er?" % (r, s), L(h), [L(math.hypot(r, s)), L(s - r), L(math.sqrt(s * s - 4 * r * r)) if s > 2 * r else L(h + 2)],
                   "h = %s(%d² − %d²) %s <b>%s</b>." % (W, s, r, "=" if abs(h - round(h)) < 1e-9 else "≈", L(h)))
    if kind == "pyr_h":
        a, hs = R.choice([(6, 5), (10, 13), (8, 5), (16, 10), (12, 10), (24, 13), (14, 25)])
        h = math.sqrt(hs * hs - (a / 2) ** 2)
        return mcq("Eine quadratische Pyramide hat die Grundkante %d cm und die Seitenhöhe (Höhe einer Seitenfläche) %d cm. Wie hoch ist die Pyramide?" % (a, hs), L(h),
                   [L(math.sqrt(abs(hs * hs - a * a))) if hs > a else L(math.hypot(hs, a / 2)), L(math.hypot(hs, a / 2)), L(hs - a / 2)],
                   "Im Inneren: h² = h<sub>s</sub>² − (a : 2)² = %d − %d, <b>h = %s</b>." % (hs * hs, (a // 2) ** 2, L(h)))
    a, h = R.choice([(6, 4), (10, 12), (16, 6), (8, 3), (24, 5), (12, 8)])
    hs = math.hypot(a / 2, h)
    return mcq("Eine quadratische Pyramide hat die Grundkante %d cm und die Höhe %d cm. Wie groß ist die Höhe einer Seitenfläche?" % (a, h), L(hs), [L(math.hypot(a, h)), L(h + a / 2), L(math.sqrt(abs(h * h - (a / 2) ** 2)))],
               "h<sub>s</sub>² = (a : 2)² + h² = %d + %d, <b>h<sub>s</sub> = %s</b>." % ((a // 2) ** 2, h * h, L(hs)))


def main():
    seen = set()
    sets = [
        ("Diagonalen und Höhen in Figuren", mix(R, seen, [(ebene, 20)])),
        ("Abstand im Koordinatensystem", mix(R, seen, [(koord, 20)])),
        ("Raumdiagonalen", mix(R, seen, [(raum, 12), (raum2, 8)])),
        ("Pyramide und Kegel", mix(R, seen, [(koerper, 20)])),
        ("Gemischte Aufgaben", mix(R, seen, [(ebene, 8), (koord, 6), (raum2, 6)])),
    ]
    body = lesson(
        ["Suche in der Figur ein <b>rechtwinkliges Dreieck</b>, in dem die gesuchte Strecke eine Seite ist. Dann hilft a² + b² = c².",
         "Höhe im gleichseitigen Dreieck: h = %s(a² − (a : 2)²) = a : 2 %s %s3." % (W, MAL, W),
         "Abstand zweier Punkte: d = %s(Δx² + Δy²)." % W,
         "Raumdiagonale des Quaders: d = %s(a² + b² + c²), beim Würfel d = a%s3." % (W, W)],
        [example("A(1 | 2), B(4 | 6)", ["Δx = 3, Δy = 4", "%s(9 + 16)" % W], "d = 5"),
         example("Quader 2 × 3 × 6", ["%s(4 + 9 + 36) = %s49" % (W, W)], "7")],
        [["Raumdiagonale = Flächendiagonale", "Alle drei Kanten quadrieren"],
         ["Höhe im gleichseitigen Dreieck mit a statt a : 2", "Die Höhe halbiert die Grundseite"],
         ["Abstand = Δx + Δy", "Quadrieren, addieren, Wurzel ziehen"]])
    faq = [
        {"q": "Wie berechne ich die Raumdiagonale eines Quaders?", "a": "d = √(a² + b² + c²). Man nutzt Pythagoras zweimal: erst die Bodendiagonale, dann mit der Höhe."},
        {"q": "Wie berechne ich den Abstand zweier Punkte?", "a": "Differenzen der x- und y-Koordinaten bilden, quadrieren, addieren und die Wurzel ziehen."},
        {"q": "Wie hoch ist ein gleichseitiges Dreieck?", "a": "h = a/2 · √3 ≈ 0,866 · a."},
        {"q": "Welches rechtwinklige Dreieck steckt im Kegel?", "a": "Radius, Höhe und Mantellinie: r² + h² = s²."},
    ]
    make_unit(R, "pythagoras-in-figuren-und-koerpern", "G",
              "Die Schülerinnen und Schüler erkennen rechtwinklige Teildreiecke in ebenen Figuren und Körpern und berechnen mit dem Satz des Pythagoras Diagonalen, Höhen, Abstände von Punkten, Raumdiagonalen und Mantellinien (Zusammenfassung).",
              "Pythagoras in Figuren und Körpern",
              "Pythagoras Anwendungen Klasse 9 – Raumdiagonale, Abstand, Höhe, Arbeitsblätter",
              "Pythagoras-Anwendungen",
              "Satz des Pythagoras anwenden für Klasse 9: Diagonalen, Höhe im Dreieck, Abstand zweier Punkte, Raumdiagonale, Pyramide und Kegel. 100 Aufgaben mit Lösungen, kostenlos.",
              "Rechtwinkliges Teildreieck suchen.",
              "Raumdiagonale: √(a² + b² + c²)",
              body, faq, sets, 8, grade="klasse-9")


if __name__ == "__main__":
    main()
