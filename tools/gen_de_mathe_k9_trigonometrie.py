# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 9: Trigonometrie im rechtwinkligen Dreieck（Leitidee Raum und Form, Sek I）
  python3 tools/gen_de_mathe_k9_trigonometrie.py
Gegenkathete, Ankathete, Hypotenuse; Sinus, Kosinus, Tangens als Seitenverhältnisse; Seiten berechnen; Winkel berechnen (sin⁻¹, cos⁻¹, tan⁻¹);
Sachaufgaben (Höhenwinkel, Steigung, Leiter, Rampe).
Fehler: Gegenkathete und Ankathete vertauscht, sin α = Hypotenuse : Gegenkathete, durch statt mal (a = c : sin α), Taschenrechner im Bogenmaß.
"""
import random, math
from fractions import Fraction as Fr
from de_common import lesson, example, make_unit, mix, MAL, fr
from de_k6 import dz
from de_k9 import mcq, zr, rdreieck

R = random.Random(49911)
G = ":"
sin, cos, tan = (lambda d: math.sin(math.radians(d))), (lambda d: math.cos(math.radians(d))), (lambda d: math.tan(math.radians(d)))
TRIPEL = [(3, 4, 5), (6, 8, 10), (5, 12, 13), (8, 15, 17), (7, 24, 25), (20, 21, 29), (9, 40, 41), (12, 35, 37)]


def L(v, u="cm"):
    return "%s %s" % (zr(v), u)


def begriffe():
    """rechter Winkel bei C; a = BC (senkrecht), b = AC (waagrecht), c = AB"""
    ang = R.choice(["A", "B"])
    what = R.choice(["Gegenkathete", "Ankathete", "Hypotenuse"])
    g = {"A": {"Gegenkathete": "a", "Ankathete": "b", "Hypotenuse": "c"}, "B": {"Gegenkathete": "b", "Ankathete": "a", "Hypotenuse": "c"}}[ang]
    nm = "α" if ang == "A" else "β"
    pic = rdreieck("a", "b", "c", ang=ang, ang_txt=nm, w=4, h=3)
    return mcq(pic + ("Welche Seite ist die Hypotenuse?" if what == "Hypotenuse" else "Welche Seite ist die %s von %s?" % (what, nm)), "die Seite %s" % g[what], ["die Seite %s" % v for v in "abc" if v != g[what]] + ["keine"],
               "Hypotenuse: gegenüber dem rechten Winkel (c). Gegenkathete: gegenüber von %s. Ankathete: liegt an %s. <b>%s</b>" % (nm, nm, g[what]))


def begriffe_text():
    P, Q, Rr = R.choice([("P", "Q", "R"), ("D", "E", "F"), ("K", "L", "M"), ("X", "Y", "Z"), ("R", "S", "T"), ("U", "V", "W")])
    at = R.choice([P, Q])
    other = Q if at == P else P
    what = R.choice(["Gegenkathete", "Ankathete", "Hypotenuse"])
    ans = {"Gegenkathete": "<span class='ov'>%s%s</span>" % (other, Rr), "Ankathete": "<span class='ov'>%s%s</span>" % (at, Rr), "Hypotenuse": "<span class='ov'>%s%s</span>" % (P, Q)}
    opts = list(ans.values())
    return mcq("Im Dreieck %s%s%s ist der Winkel bei %s ein rechter Winkel. %s" % (P, Q, Rr, Rr, "Welche Strecke ist die Hypotenuse?" if what == "Hypotenuse" else "Welche Strecke ist die %s des Winkels bei %s?" % (what, at)), ans[what], [o for o in opts if o != ans[what]] + ["keine"],
               "Hypotenuse gegenüber dem rechten Winkel: %s. Ankathete am Winkel bei %s: %s. Gegenkathete gegenüber: %s. <b>%s</b>" % (ans["Hypotenuse"], at, ans["Ankathete"], ans["Gegenkathete"], ans[what]))


def verhaeltnis():
    a, b, c = R.choice(TRIPEL)
    ang = R.choice(["A", "B"])
    f = R.choice(["sin", "cos", "tan"])
    nm = "α" if ang == "A" else "β"
    geg, an = (a, b) if ang == "A" else (b, a)
    val = {"sin": (geg, c), "cos": (an, c), "tan": (geg, an)}[f]
    pic = rdreieck("a = %d" % a, "b = %d" % b, "c = %d" % c, ang=ang, ang_txt=nm, w=b, h=a)
    wrong = {(geg, c), (an, c), (geg, an), (c, geg), (an, geg)} - {val}
    return mcq(pic + "Gib %s %s als Bruch an." % (f, nm), fr(*val), [fr(*w) for w in sorted(wrong)][:3],
               "%s = %s. <b>%s %s = %s</b>" % (f, {"sin": "Gegenkathete : Hypotenuse", "cos": "Ankathete : Hypotenuse", "tan": "Gegenkathete : Ankathete"}[f], f, nm, fr(*val)))


def seiten():
    al = R.randint(15, 75)
    kind = R.choice(["geg_hyp", "an_hyp", "geg_an", "hyp_geg", "hyp_an"])
    x = R.randint(3, 20)
    if kind == "geg_hyp":
        v = x * sin(al)
        q = "Im rechtwinkligen Dreieck ist die Hypotenuse c = %d cm und α = %d°. Berechne die Gegenkathete a von α." % (x, al)
        w = [x * cos(al), x / sin(al), x * tan(al)]
        e = "a = c %s sin α = %d %s sin %d°" % (MAL, x, MAL, al)
    elif kind == "an_hyp":
        v = x * cos(al)
        q = "Im rechtwinkligen Dreieck ist die Hypotenuse c = %d cm und α = %d°. Berechne die Ankathete b von α." % (x, al)
        w = [x * sin(al), x / cos(al), x * tan(al)]
        e = "b = c %s cos α = %d %s cos %d°" % (MAL, x, MAL, al)
    elif kind == "geg_an":
        v = x * tan(al)
        q = "Im rechtwinkligen Dreieck ist die Ankathete b = %d cm und α = %d°. Berechne die Gegenkathete a." % (x, al)
        w = [x / tan(al), x * sin(al), x * cos(al)]
        e = "a = b %s tan α = %d %s tan %d°" % (MAL, x, MAL, al)
    elif kind == "hyp_geg":
        v = x / sin(al)
        q = "Im rechtwinkligen Dreieck ist die Gegenkathete a = %d cm und α = %d°. Berechne die Hypotenuse c." % (x, al)
        w = [x * sin(al), x / cos(al), x / tan(al)]
        e = "c = a %s sin α = %d %s sin %d°" % (G, x, G, al)
    else:
        v = x / cos(al)
        q = "Im rechtwinkligen Dreieck ist die Ankathete b = %d cm und α = %d°. Berechne die Hypotenuse c." % (x, al)
        w = [x * cos(al), x / sin(al), x * tan(al)]
        e = "c = b %s cos α = %d %s cos %d°" % (G, x, G, al)
    return mcq(q + " (Runde auf eine Nachkommastelle.)", L(v), [L(t) for t in w], "%s ≈ <b>%s</b>." % (e, L(v)))


def winkel():
    kind = R.choice(["sin", "cos", "tan", "tan"])
    if kind == "sin":
        c = R.randint(6, 20)
        a = R.randint(2, c - 1)
        v = math.degrees(math.asin(a / c))
        q = "In einem rechtwinkligen Dreieck ist die Gegenkathete von α %d cm und die Hypotenuse %d cm lang. Wie groß ist α?" % (a, c)
        w = [math.degrees(math.acos(a / c)), math.degrees(math.atan(a / c)), 90 - math.degrees(math.atan(a / c))]
        e = "sin α = %d : %d ⇒ α = sin⁻¹(%d : %d)" % (a, c, a, c)
    elif kind == "cos":
        c = R.randint(6, 20)
        b = R.randint(2, c - 1)
        v = math.degrees(math.acos(b / c))
        q = "In einem rechtwinkligen Dreieck ist die Ankathete von α %d cm und die Hypotenuse %d cm lang. Wie groß ist α?" % (b, c)
        w = [math.degrees(math.asin(b / c)), math.degrees(math.atan(b / c)), math.degrees(math.atan(c / b))]
        e = "cos α = %d : %d ⇒ α = cos⁻¹(%d : %d)" % (b, c, b, c)
    else:
        a, b = R.randint(2, 15), R.randint(2, 15)
        if a == b:
            return None
        v = math.degrees(math.atan(a / b))
        q = "In einem rechtwinkligen Dreieck ist die Gegenkathete von α %d cm und die Ankathete %d cm lang. Wie groß ist α?" % (a, b)
        w = [math.degrees(math.atan(b / a)), math.degrees(math.asin(min(a, b) / max(a, b))), math.degrees(math.acos(min(a, b) / max(a, b)))]
        e = "tan α = %d : %d ⇒ α = tan⁻¹(%d : %d)" % (a, b, a, b)
    return mcq(q + " (Runde auf eine Nachkommastelle.)", "%s°" % zr(v), ["%s°" % zr(t) for t in w], "%s ≈ <b>%s°</b>." % (e, zr(v)))


def sache():
    kind = R.choice(["turm", "turm", "leiter", "steigung", "rampe", "schatten"])
    if kind == "turm":
        d = R.choice([20, 30, 40, 50, 60, 80, 100])
        al = R.randint(20, 60)
        h = d * tan(al)
        return mcq("Aus %d m Entfernung sieht man die Spitze eines Turms unter einem Höhenwinkel von %d° (vom Boden aus). Wie hoch ist der Turm (auf eine Nachkommastelle)?" % (d, al), L(h, "m"),
                   [L(d * sin(al), "m"), L(d / tan(al), "m"), L(d * cos(al), "m")], "h = %d %s tan %d° ≈ <b>%s</b>." % (d, MAL, al, L(h, "m")))
    if kind == "leiter":
        l = R.choice([3, 4, 5, 6, 8])
        al = R.randint(60, 78)
        h = l * sin(al)
        return mcq("Eine %d m lange Leiter lehnt mit einem Neigungswinkel von %d° zum Boden an einer Wand. Wie hoch reicht sie (auf eine Nachkommastelle)?" % (l, al), L(h, "m"),
                   [L(l * cos(al), "m"), L(l * tan(al), "m"), L(l / sin(al), "m")], "h = %d %s sin %d° ≈ <b>%s</b>." % (l, MAL, al, L(h, "m")))
    if kind == "steigung":
        p = R.choice([5, 8, 10, 12, 15, 20, 25])
        v = math.degrees(math.atan(p / 100))
        return mcq("Eine Straße hat eine Steigung von %d %% (%d m Höhe auf 100 m waagrecht). Wie groß ist der Steigungswinkel (auf eine Nachkommastelle)?" % (p, p), "%s°" % zr(v),
                   ["%d°" % p, "%s°" % zr(math.degrees(math.asin(p / 100)) + 0.5), "%s°" % zr(p * 0.9)], "tan α = %d : 100 ⇒ α ≈ <b>%s°</b>. Ein Prozent ist kein Grad!" % (p, zr(v)))
    if kind == "rampe":
        h = R.choice([Fr(1, 2), Fr(3, 4), 1, Fr(6, 5)])
        al = R.choice([4, 5, 6, 8, 10])
        l = float(h) / sin(al)
        return mcq("Eine Rampe soll %s m Höhe überwinden und darf nur %d° steil sein. Wie lang muss sie mindestens sein (auf eine Nachkommastelle)?" % (dz(h), al), L(l, "m"),
                   [L(float(h) * sin(al), "m"), L(float(h) / tan(al) - 0.3, "m") if abs(float(h) / tan(al) - l) > 0.1 else L(l + 1, "m"), L(float(h) * al, "m")], "l = h %s sin α = %s %s sin %d° ≈ <b>%s</b>." % (G, dz(h), G, al, L(l, "m")))
    h = R.choice([2, 5, 10, 15, 20])
    al = R.randint(25, 55)
    s = h / tan(al)
    return mcq("Ein %d m hoher Mast wirft einen Schatten. Die Sonnenstrahlen treffen unter %d° auf den Boden. Wie lang ist der Schatten (auf eine Nachkommastelle)?" % (h, al), L(s, "m"),
               [L(h * tan(al), "m"), L(h / sin(al), "m"), L(h * cos(al), "m")], "s = h %s tan %d° ≈ <b>%s</b>." % (G, al, L(s, "m")))


def main():
    seen = set()
    sets = [
        ("Seiten benennen", mix(R, seen, [(begriffe, 6), (begriffe_text, 8), (verhaeltnis, 6)])),
        ("Sinus, Kosinus, Tangens", mix(R, seen, [(verhaeltnis, 20)])),
        ("Seiten berechnen", mix(R, seen, [(seiten, 20)])),
        ("Winkel berechnen", mix(R, seen, [(winkel, 20)])),
        ("Sachaufgaben", mix(R, seen, [(sache, 20)])),
    ]
    body = lesson(
        ["Im rechtwinkligen Dreieck ist die <b>Hypotenuse</b> die Seite gegenüber dem rechten Winkel. Vom Winkel α aus gesehen liegt die <b>Ankathete</b> an α, die <b>Gegenkathete</b> gegenüber.",
         "sin α = Gegenkathete %s Hypotenuse, cos α = Ankathete %s Hypotenuse, tan α = Gegenkathete %s Ankathete." % (G, G, G),
         "Seite gesucht: Gleichung nach der Seite umstellen, z. B. Gegenkathete = Hypotenuse %s sin α." % MAL,
         "Winkel gesucht: mit sin⁻¹, cos⁻¹ oder tan⁻¹ (Taschenrechner auf <b>DEG</b> stellen)."],
        [example("c = 10 cm, α = 30°, a = ?", ["a = 10 %s sin 30°" % MAL], "5 cm"),
         example("a = 3, b = 4, α = ?", ["tan α = 3 : 4"], "α ≈ 36,9°")],
        [["Gegen- und Ankathete vertauscht", "Immer vom gesuchten Winkel aus schauen"],
         ["c = a %s sin α" % MAL, "c = a %s sin α" % G],
         ["10 % Steigung = 10°", "tan α = 0,1 ⇒ α ≈ 5,7°"]])
    faq = [
        {"q": "Was sind Sinus, Kosinus und Tangens?", "a": "Seitenverhältnisse im rechtwinkligen Dreieck: sin = Gegenkathete : Hypotenuse, cos = Ankathete : Hypotenuse, tan = Gegenkathete : Ankathete."},
        {"q": "Wie merke ich mir die Formeln?", "a": "Viele merken sich „GAGA HHAA“: sin = G/H, cos = A/H, tan = G/A."},
        {"q": "Wie berechne ich einen Winkel?", "a": "Das Seitenverhältnis ausrechnen und die Umkehrfunktion (sin⁻¹, cos⁻¹, tan⁻¹) des Taschenrechners verwenden."},
        {"q": "Warum bekomme ich falsche Werte?", "a": "Oft ist der Taschenrechner auf RAD (Bogenmaß) statt DEG (Grad) eingestellt."},
    ]
    make_unit(R, "trigonometrie", "R",
              "Die Schülerinnen und Schüler nutzen Sinus, Kosinus und Tangens als Seitenverhältnisse im rechtwinkligen Dreieck, berechnen fehlende Seiten und Winkel und lösen Sachaufgaben (Zusammenfassung).",
              "Trigonometrie im rechtwinkligen Dreieck",
              "Sinus, Kosinus, Tangens Klasse 9 – Trigonometrie Arbeitsblätter mit Lösungen",
              "Sinus, Kosinus, Tangens",
              "Trigonometrie für Klasse 9: Gegenkathete und Ankathete, Sinus, Kosinus und Tangens, Seiten und Winkel berechnen und Sachaufgaben. 100 Aufgaben mit Lösungen, kostenlos.",
              "sin = G : H, cos = A : H, tan = G : A",
              "Immer vom gesuchten Winkel aus schauen.",
              body, faq, sets, 11, grade="klasse-9")


if __name__ == "__main__":
    main()
