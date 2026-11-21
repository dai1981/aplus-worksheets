# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 9: Satz des Pythagoras（Leitidee Raum und Form, Sek I）
  python3 tools/gen_de_mathe_k9_satz_des_pythagoras.py
a² + b² = c², Hypotenuse und Katheten erkennen, Hypotenuse berechnen, Kathete berechnen, Umkehrung (rechtwinklig prüfen),
Sachaufgaben (Leiter, Bildschirmdiagonale, Abkürzung, Rampe).
Fehler: c = a + b, Kathete mit Addition statt Subtraktion, falsche Seite als Hypotenuse, Wurzel vergessen.
"""
import random, math
from fractions import Fraction as Fr
from de_common import lesson, example, make_unit, mix, MAL, num
from de_k9 import mcq, zahl, zr, rdreieck
from de_k6 import dz

R = random.Random(49907)
W = "√"
TRIPEL = [(3, 4, 5), (6, 8, 10), (5, 12, 13), (8, 15, 17), (9, 12, 15), (7, 24, 25), (12, 16, 20), (20, 21, 29), (9, 40, 41), (15, 20, 25), (10, 24, 26), (12, 35, 37), (15, 36, 39), (18, 24, 30)]


def L(v, u="cm"):
    return "%s %s" % (zr(v) if abs(v - round(v)) > 1e-9 else num(int(round(v))), u)


def hyp():
    kind = R.choice(["tripel", "tripel", "rund", "bild"])
    if kind in ("tripel", "bild"):
        a, b, c = R.choice(TRIPEL)
        if R.random() < 0.5:
            a, b = b, a
    else:
        a, b = R.randint(2, 15), R.randint(2, 15)
        c = math.hypot(a, b)
        if abs(c - round(c)) < 1e-9:
            return None
    pic = rdreieck("a = %d cm" % a, "b = %d cm" % b, "c = ?", w=b, h=a) if kind == "bild" else ""
    q = (pic + "Berechne die Hypotenuse c.") if pic else "In einem rechtwinkligen Dreieck sind die Katheten a = %d cm und b = %d cm. Wie lang ist die Hypotenuse%s?" % (a, b, " (auf eine Nachkommastelle)" if kind == "rund" else "")
    return mcq(q, L(c), [L(a + b), L(a * a + b * b), L(math.sqrt(abs(a * a - b * b))) if a != b else L(c + 1)],
               "c² = %d² + %d² = %d + %d = %d. c = %s%d %s <b>%s</b>." % (a, b, a * a, b * b, a * a + b * b, W, a * a + b * b, "≈" if kind == "rund" else "=", L(c)))


def kathete():
    kind = R.choice(["tripel", "tripel", "rund", "bild"])
    if kind in ("tripel", "bild"):
        a, b, c = R.choice(TRIPEL)
        if R.random() < 0.5:
            a, b = b, a
    else:
        c, b = R.randint(6, 20), R.randint(2, 15)
        if b >= c:
            return None
        a = math.sqrt(c * c - b * b)
        if abs(a - round(a)) < 1e-9:
            return None
    pic = rdreieck("a = ?", "b = %d cm" % b, "c = %d cm" % c, w=b, h=a) if kind == "bild" else ""
    q = (pic + "Berechne die Kathete a.") if pic else "In einem rechtwinkligen Dreieck ist die Hypotenuse c = %d cm und die Kathete b = %d cm. Wie lang ist die andere Kathete a%s?" % (c, b, " (auf eine Nachkommastelle)" if kind == "rund" else "")
    return mcq(q, L(a), [L(math.hypot(b, c)), L(c - b), L(c * c - b * b)],
               "a² = c² − b² = %d − %d = %d. a = %s%d %s <b>%s</b>." % (c * c, b * b, c * c - b * b, W, c * c - b * b, "≈" if kind == "rund" else "=", L(a)))


def erkennen():
    kind = R.choice(["hyp", "gl", "umkehr", "umkehr", "formel"])
    if kind == "hyp":
        names = R.choice([("r", "s", "t"), ("e", "f", "g"), ("k", "l", "m"), ("u", "v", "w")])
        rw = R.choice(["R", "S", "T"]) if names[0] == "r" else None
        x, y, z = names
        return mcq("In einem Dreieck mit den Seiten %s, %s und %s liegt der rechte Winkel gegenüber der Seite %s. Welche Gleichung gilt?" % (x, y, z, y), "%s² + %s² = %s²" % (x, z, y),
                   ["%s² + %s² = %s²" % (x, y, z), "%s² + %s² = %s²" % (y, z, x), "%s + %s = %s" % (x, z, y)],
                   "Die Hypotenuse liegt dem rechten Winkel gegenüber: %s. <b>%s² + %s² = %s²</b>" % (y, x, z, y))
    if kind == "formel":
        q, a, w = R.choice([
            ("Welche Seite ist im rechtwinkligen Dreieck immer die längste?", "die Hypotenuse", ["die kürzere Kathete", "die längere Kathete", "Das ist verschieden."]),
            ("Was sind die Katheten?", "die beiden Seiten, die den rechten Winkel bilden", ["die Seite gegenüber dem rechten Winkel", "alle drei Seiten", "die Höhen des Dreiecks"]),
            ("Für welche Dreiecke gilt der Satz des Pythagoras?", "nur für rechtwinklige Dreiecke", ["für alle Dreiecke", "nur für gleichseitige Dreiecke", "nur für gleichschenklige Dreiecke"]),
            ("Was bedeutet c² geometrisch?", "den Flächeninhalt des Quadrats über der Hypotenuse", ["den Umfang des Dreiecks", "die doppelte Hypotenuse", "den Flächeninhalt des Dreiecks"]),
        ])
        return mcq(q, a, w, "<b>%s</b>" % a)
    if R.random() < 0.5:
        a, b, c = R.choice(TRIPEL)
        ok = True
    else:
        a, b, c = R.choice(TRIPEL)
        c += R.choice([-1, 1])
        ok = False
    ans = "Ja, denn %d + %d = %d = %d²." % (a * a, b * b, c * c, c) if ok else "Nein, denn %d + %d = %d ≠ %d = %d²." % (a * a, b * b, a * a + b * b, c * c, c)
    return mcq("Ist ein Dreieck mit den Seiten %d cm, %d cm und %d cm rechtwinklig?" % (a, b, c), ans,
               ["Nein, denn %d + %d ≠ %d." % (a, b, c) if ok else "Ja, denn %d + %d &gt; %d." % (a, b, c), "Ja, jedes Dreieck mit ganzen Zahlen ist rechtwinklig." if not ok else "Nein, die Seiten sind verschieden lang.", "Das kann man ohne Winkelmesser nicht sagen."],
               "Umkehrung des Satzes des Pythagoras: Gilt a² + b² = c² für die längste Seite c, ist das Dreieck rechtwinklig. <b>%s</b>" % ("Ja" if ok else "Nein"))


def sache():
    kind = R.choice(["leiter", "tv", "weg", "rampe", "mast", "drachen"])
    if kind == "leiter":
        l, d = R.choice([(5, 3), (10, 6), (13, 5), (6, 2), (8, 2), (7, 2), (4, 1)])
        h = math.sqrt(l * l - d * d)
        return mcq("Eine %d m lange Leiter lehnt an einer Wand. Ihr Fuß steht %d m von der Wand entfernt. Wie hoch reicht sie (auf eine Nachkommastelle)?" % (l, d), L(h, "m"),
                   [L(math.hypot(l, d), "m"), L(l - d, "m"), L(l * l - d * d, "m")], "h² = %d² − %d² = %d, h ≈ <b>%s</b>." % (l, d, l * l - d * d, L(h, "m")))
    if kind == "tv":
        b, h = R.choice([(80, 45), (96, 54), (64, 36), (112, 63), (48, 27)])
        d = math.hypot(b, h)
        return mcq("Ein Bildschirm ist %d cm breit und %d cm hoch. Wie lang ist seine Diagonale (auf ganze cm)?" % (b, h), "%d cm" % round(d), ["%d cm" % (b + h), "%d cm" % round(math.sqrt(b * b - h * h)), "%d cm" % round((b + h) / 2)],
                   "d² = %d² + %d² = %s, d ≈ <b>%d cm</b>." % (b, h, num(b * b + h * h), round(d)))
    if kind == "weg":
        a, b = R.choice([(60, 80), (30, 40), (120, 50), (90, 120), (45, 60), (70, 240)])
        c = math.hypot(a, b)
        return mcq("Ein rechteckiger Park ist %d m lang und %d m breit. Wie viele Meter spart man, wenn man diagonal hindurchgeht statt außen herum?" % (b, a), "%d m" % round(a + b - c), ["%d m" % round(c), "%d m" % (a + b), "%d m" % abs(b - a)],
                   "Diagonale: %s(%d² + %d²) = %d m. Außen herum: %d m. Ersparnis: <b>%d m</b>." % (W, a, b, round(c), a + b, round(a + b - c)))
    if kind == "rampe":
        l, h = R.choice([(4, 1), (6, Fr(1, 2)), (5, Fr(3, 2)), (3, Fr(1, 2)), (10, 2)])
        g = math.sqrt(l * l - float(h) ** 2)
        return mcq("Eine Rampe ist %s m lang und überwindet %s m Höhe. Wie lang ist sie waagrecht gemessen (auf zwei Nachkommastellen)?" % (dz(l), dz(h)), "%s m" % zr(g, 2),
                   ["%s m" % zr(math.hypot(l, float(h)), 2), "%s m" % zr(l - float(h), 2), "%s m" % zr(l * l - float(h) ** 2, 2)],
                   "x² = %s² − %s² ⇒ x ≈ <b>%s m</b>." % (dz(l), dz(h), zr(g, 2)))
    if kind == "mast":
        hm, d = R.choice([(12, 5), (8, 6), (15, 8), (24, 7), (9, 12)])
        s = math.hypot(hm, d)
        return mcq("Ein %d m hoher Mast wird mit einem Seil gesichert, das %d m vom Fuß entfernt im Boden befestigt ist. Wie lang ist das Seil?" % (hm, d), L(s, "m"), [L(hm + d, "m"), L(math.sqrt(abs(hm * hm - d * d)), "m"), L(hm * hm + d * d, "m")],
                   "s² = %d² + %d² = %d, <b>s = %s</b>." % (hm, d, hm * hm + d * d, L(s, "m")))
    l, x = R.choice([(50, 30), (100, 60), (65, 25), (130, 50), (25, 7)])
    h = math.sqrt(l * l - x * x)
    return mcq("Ein Drachen hängt an einer %d m langen Schnur. Er steht %d m waagrecht vom Kind entfernt. Wie hoch fliegt er (Schnur gerade, Hand am Boden)?" % (l, x), L(h, "m"), [L(math.hypot(l, x), "m"), L(l - x, "m"), L(l, "m")],
               "h² = %d² − %d² = %s, <b>h = %s</b>." % (l, x, num(l * l - x * x), L(h, "m")))


def main():
    seen = set()
    sets = [
        ("Hypotenuse berechnen", mix(R, seen, [(hyp, 20)])),
        ("Kathete berechnen", mix(R, seen, [(kathete, 20)])),
        ("Seiten erkennen und Umkehrung", mix(R, seen, [(erkennen, 20)])),
        ("Gemischte Aufgaben", mix(R, seen, [(hyp, 10), (kathete, 10)])),
        ("Sachaufgaben", mix(R, seen, [(sache, 20)])),
    ]
    body = lesson(
        ["Im rechtwinkligen Dreieck heißen die beiden Seiten am rechten Winkel <b>Katheten</b> (a, b), die längste Seite gegenüber dem rechten Winkel <b>Hypotenuse</b> (c).",
         "<b>Satz des Pythagoras</b>: a² + b² = c².",
         "Hypotenuse: c = %s(a² + b²). Kathete: a = %s(c² − b²)." % (W, W),
         "<b>Umkehrung</b>: Gilt a² + b² = c² (c die längste Seite), dann ist das Dreieck rechtwinklig."],
        [example("a = 6 cm, b = 8 cm", ["c² = 36 + 64 = 100"], "c = 10 cm"),
         example("c = 13 cm, b = 5 cm", ["a² = 169 − 25 = 144"], "a = 12 cm")],
        [["c = a + b", "Quadrieren, addieren, Wurzel ziehen"],
         ["Kathete: c² + b²", "Bei der Kathete subtrahieren: c² − b²"],
         ["Wurzel am Ende vergessen", "c² = 100 heißt c = 10"]])
    faq = [
        {"q": "Was sagt der Satz des Pythagoras?", "a": "In jedem rechtwinkligen Dreieck ist die Summe der Kathetenquadrate gleich dem Hypotenusenquadrat: a² + b² = c²."},
        {"q": "Welche Seite ist die Hypotenuse?", "a": "Die Seite gegenüber dem rechten Winkel. Sie ist immer die längste Seite."},
        {"q": "Wie berechne ich eine Kathete?", "a": "a = √(c² − b²): Hypotenusenquadrat minus das Quadrat der bekannten Kathete, dann die Wurzel."},
        {"q": "Wie prüfe ich, ob ein Dreieck rechtwinklig ist?", "a": "Mit der Umkehrung: Ist die Summe der Quadrate der beiden kürzeren Seiten gleich dem Quadrat der längsten Seite, ist es rechtwinklig."},
    ]
    make_unit(R, "satz-des-pythagoras", "R",
              "Die Schülerinnen und Schüler nutzen den Satz des Pythagoras und seine Umkehrung, berechnen fehlende Seitenlängen in rechtwinkligen Dreiecken und lösen Sachaufgaben (Zusammenfassung).",
              "Satz des Pythagoras",
              "Satz des Pythagoras Klasse 9 – Hypotenuse und Kathete berechnen, Arbeitsblätter",
              "Satz des Pythagoras",
              "Satz des Pythagoras für Klasse 9: Hypotenuse und Katheten berechnen, Umkehrung, rechtwinklige Dreiecke erkennen und Sachaufgaben. 100 Aufgaben mit Lösungen, kostenlos.",
              "a² + b² = c²",
              "c ist die Hypotenuse, gegenüber dem rechten Winkel.",
              body, faq, sets, 7, grade="klasse-9")


if __name__ == "__main__":
    main()
