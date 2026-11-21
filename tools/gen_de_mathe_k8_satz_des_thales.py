# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 8: Satz des Thales（Leitidee Raum und Form, Sek I）
  python3 tools/gen_de_mathe_k8_satz_des_thales.py
Thaleskreis, rechter Winkel bei C, fehlende Winkel im Thalesdreieck, gleichschenklige Teildreiecke (MA = MB = MC),
Umkehrung des Satzes, Radius und Mittelpunkt, Anwendungen (rechtwinklige Dreiecke konstruieren, Tangenten).
Fehler: Winkel bei C für beliebig gehalten, 180° statt 90° als Summe von α und β, Mittelpunkt auf dem Kreis, Radius mit Durchmesser verwechselt.
"""
import random, math
from fractions import Fraction as Fr
from de_common import lesson, example, make_unit, mix, wrap, line, text, INK, BLUE, RED, GREEN, FILL
from de_k6 import dz
from de_k8 import mcq

R = random.Random(49811)


def thales_svg(alpha, show=("α",), vals=None, label="Thaleskreis über AB"):
    r = 110
    cx, cy = 150, 140
    A, B = (cx - r, cy), (cx + r, cy)
    # Winkel bei A = alpha → Mittelpunktswinkel BMC = 2 alpha
    t = math.radians(2 * alpha)
    C = (cx + r * math.cos(t), cy - r * math.sin(t))
    s = ["<path d='M%d %d A%d %d 0 0 1 %d %d' fill='none' stroke='%s' stroke-width='1.6' stroke-dasharray='5 4'/>" % (A[0], A[1], r, r, B[0], B[1], INK)]
    s.append("<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='%s' stroke='%s' stroke-width='2.4'/>" % (A + B + C + (FILL, GREEN)))
    s.append("<circle cx='%d' cy='%d' r='3.5' fill='%s'/>" % (cx, cy, INK) + text(cx, cy + 18, "M", 14))
    s.append(text(A[0] - 10, A[1] + 16, "A", 15) + text(B[0] + 10, B[1] + 16, "B", 15) + text(C[0], C[1] - 10, "C", 15))
    vals = vals or {}
    if "α" in show:
        s.append(text(A[0] + 36, A[1] - 8, vals.get("α", "α"), 13, col=RED))
    if "β" in show:
        s.append(text(B[0] - 36, B[1] - 8, vals.get("β", "β"), 13, col=RED))
    if "γ" in show:
        s.append(text(C[0], C[1] + 30, vals.get("γ", "γ"), 13, col=RED))
    if "MC" in show:
        s.append(line(cx, cy, C[0], C[1], BLUE, 2, " stroke-dasharray='4 3'"))
    return wrap(300, 175, "".join(s), label, lg=True)


def grund():
    q, a, w = R.choice([
        ("C liegt auf dem Halbkreis über der Strecke AB. Wie groß ist der Winkel bei C?", "90°", ["180°", "60°", "45°"]),
        ("Was besagt der Satz des Thales?", "Liegt C auf dem Halbkreis über AB, so hat das Dreieck ABC bei C einen rechten Winkel.", ["Jedes Dreieck hat einen rechten Winkel.", "Die Winkelsumme im Dreieck ist 90°.", "Der Winkel bei C ist immer 60°."]),
        ("Wo liegt der Mittelpunkt des Thaleskreises über AB?", "in der Mitte der Strecke AB", ["im Punkt C", "im Punkt A", "über der Mitte von AB auf dem Kreis"]),
        ("Wie lautet die Umkehrung des Satzes des Thales?", "Hat ABC bei C einen rechten Winkel, so liegt C auf dem Kreis mit dem Durchmesser AB.", ["Liegt C auf dem Kreis, ist das Dreieck gleichseitig.", "Jeder Punkt auf AB ergibt einen rechten Winkel.", "Ein rechter Winkel liegt immer bei A."]),
        ("Welche Strecke ist der Durchmesser des Thaleskreises?", "AB", ["AC", "BC", "MC"]),
        ("C liegt innerhalb des Thaleskreises über AB (nicht auf AB). Wie ist der Winkel bei C?", "größer als 90° (stumpf)", ["genau 90°", "kleiner als 90° (spitz)", "immer 180°"]),
        ("C liegt außerhalb des Thaleskreises über AB. Wie ist der Winkel bei C?", "kleiner als 90° (spitz)", ["genau 90°", "größer als 90° (stumpf)", "genau 0°"]),
        ("Warum sind die Dreiecke AMC und BMC gleichschenklig?", "MA, MB und MC sind Radien und gleich lang.", ["Weil AB = AC ist.", "Weil der Winkel bei C 90° ist.", "Weil M auf dem Kreis liegt."]),
        ("Welche Dreiecksart ist ein Dreieck ABC mit C auf dem Thaleskreis über AB?", "rechtwinklig", ["gleichseitig", "stumpfwinklig", "immer gleichschenklig"]),
        ("Wie viele Punkte C auf dem Halbkreis über AB ergeben einen rechten Winkel bei C?", "alle (außer A und B)", ["genau einer", "genau zwei", "keiner"]),
        ("Die Hypotenuse eines rechtwinkligen Dreiecks ist 10 cm lang. Wie groß ist der Radius seines Thaleskreises?", "5 cm", ["10 cm", "20 cm", "2,5 cm"]),
        ("Welche Seite liegt im Thalesdreieck dem rechten Winkel gegenüber?", "die Seite AB (Hypotenuse)", ["die Seite AC", "die Seite BC", "die Strecke MC"]),
    ])
    return mcq(q, a, w, "<b>%s</b>" % a)


def winkel():
    a = R.randint(15, 75)
    if a == 45 and R.random() < 0.5:
        return None
    kind = R.choice(["beta", "alpha", "bild"])
    if kind == "beta":
        return mcq("Im Dreieck ABC liegt C auf dem Thaleskreis über AB. Es ist α = %d°. Wie groß ist β?" % a, "%d°" % (90 - a), ["%d°" % (180 - a), "%d°" % a, "%d°" % (180 - 90 - a + 10)],
                   "γ = 90° (Thales). β = 180° − 90° − %d° = <b>%d°</b>." % (a, 90 - a))
    if kind == "alpha":
        b = 90 - a
        return mcq("Im Dreieck ABC liegt C auf dem Halbkreis über AB. Es ist β = %d°. Wie groß ist α?" % b, "%d°" % a, ["%d°" % (180 - b), "%d°" % (90 + b) if 90 + b < 180 else "%d°" % b, "%d°" % (b // 2)],
                   "α + β = 90°, also α = 90° − %d° = <b>%d°</b>." % (b, a))
    pic = thales_svg(a, show=("α", "β"), vals={"α": "%d°" % a})
    return mcq(pic + "Wie groß ist der Winkel β?", "%d°" % (90 - a), ["%d°" % (180 - a), "%d°" % a, "%d°" % (180 - 2 * a) if 180 - 2 * a != 90 - a else "%d°" % (90 - a + 5)],
               "Bei C ist ein rechter Winkel. β = 90° − %d° = <b>%d°</b>." % (a, 90 - a))


def teil():
    a = R.randint(20, 70)
    kind = R.choice(["acm", "amc", "bmc", "bcm"])
    pic = thales_svg(a, show=("α", "MC"), vals={"α": "%d°" % a})
    if kind == "acm":
        return mcq(pic + "MA und MC sind Radien. Wie groß ist der Winkel ACM?", "%d°" % a, ["%d°" % (90 - a), "%d°" % (180 - 2 * a), "%d°" % (90 + a)],
                   "△AMC ist gleichschenklig (MA = MC). Die Basiswinkel sind gleich: <b>%d°</b>." % a)
    if kind == "amc":
        return mcq(pic + "MA und MC sind Radien. Wie groß ist der Winkel AMC?", "%d°" % (180 - 2 * a), ["%d°" % (180 - a), "%d°" % (2 * a), "%d°" % (90 - a)],
                   "Basiswinkel je %d°: 180° − 2 · %d° = <b>%d°</b>." % (a, a, 180 - 2 * a))
    if kind == "bmc":
        return mcq(pic + "Wie groß ist der Winkel BMC?", "%d°" % (2 * a), ["%d°" % (180 - 2 * a), "%d°" % a, "%d°" % (90 - a)],
                   "∠AMC = %d°. Mit ∠BMC zusammen 180°: <b>%d°</b>." % (180 - 2 * a, 2 * a))
    return mcq(pic + "Wie groß ist der Winkel BCM?", "%d°" % (90 - a), ["%d°" % a, "%d°" % (2 * a), "%d°" % (180 - a)],
               "∠ACB = 90°, ∠ACM = %d°. ∠BCM = 90° − %d° = <b>%d°</b>." % (a, a, 90 - a))


def umkehr():
    kind = R.choice(["recht", "nicht", "abstand", "abstand_n", "radius"])
    if kind == "recht":
        a = R.randint(20, 70)
        return mcq("Im Dreieck ABC ist α = %d° und β = %d°. Liegt C auf dem Kreis mit dem Durchmesser AB?" % (a, 90 - a), "Ja, denn γ = 90°.", ["Nein, denn γ = %d°." % (90 + a), "Ja, denn α ist spitz.", "Nein, C liegt immer innerhalb."],
                   "γ = 180° − %d° − %d° = 90°. Umkehrung des Thalessatzes: <b>Ja</b>." % (a, 90 - a))
    if kind == "nicht":
        a = R.randint(20, 70)
        b = R.randint(20, 85)
        if a + b == 90 or a + b >= 170:
            return None
        g = 180 - a - b
        lage = "innerhalb" if g > 90 else "außerhalb"
        return mcq("Im Dreieck ABC ist α = %d° und β = %d°. Wo liegt C bezogen auf den Kreis mit dem Durchmesser AB?" % (a, b), lage + " des Kreises",
                   ["auf dem Kreis", "außerhalb des Kreises" if g > 90 else "innerhalb des Kreises", "genau im Mittelpunkt"],
                   "γ = %d°. %s 90°: C liegt <b>%s</b> des Kreises." % (g, "Größer als" if g > 90 else "Kleiner als", lage))
    if kind in ("abstand", "abstand_n"):
        ab = R.choice([6, 8, 10, 12, 14])
        r = ab // 2
        d = r if kind == "abstand" else r + R.choice([-2, -1, 1, 2])
        ans = "Ja, denn MC = %d cm ist der Radius." % d if d == r else "Nein, denn MC = %d cm ist nicht der Radius %d cm." % (d, r)
        return mcq("AB ist %d cm lang, M ist der Mittelpunkt von AB. C hat von M den Abstand %d cm. Ist der Winkel bei C ein rechter Winkel?" % (ab, d), ans,
                   ["Nein, denn MC = %d cm ist nicht der Radius %d cm." % (d, r) if d == r else "Ja, denn MC = %d cm ist der Radius." % d, "Ja, jeder Punkt hat einen rechten Winkel.", "Nein, rechte Winkel liegen nur bei A."],
                   "Radius des Thaleskreises: %d : 2 = %d cm. <b>%s</b>" % (ab, r, "Ja" if d == r else "Nein"))
    ab = Fr(R.randint(5, 30), R.choice([1, 2]))
    return mcq("Die Strecke AB ist %s cm lang. Welchen Radius hat der Thaleskreis über AB?" % dz(ab), "%s cm" % dz(ab / 2), ["%s cm" % dz(ab), "%s cm" % dz(ab * 2), "%s cm" % dz(ab / 4)],
               "Der Radius ist die Hälfte des Durchmessers AB: <b>%s cm</b>." % dz(ab / 2))


def anwendung():
    kind = R.choice(["konstr", "tangente", "koord", "quadrat", "sach"])
    if kind == "konstr":
        c = R.randint(5, 12)
        return mcq("Du sollst ein rechtwinkliges Dreieck mit der Hypotenuse c = %d cm zeichnen. Womit beginnst du?" % c, "AB = %d cm zeichnen und den Halbkreis mit dem Radius %s cm um die Mitte von AB" % (c, dz(Fr(c, 2))),
                   ["AB = %d cm zeichnen und einen Kreis mit dem Radius %d cm um A" % (c, c), "einen rechten Winkel bei A zeichnen", "einen Kreis mit dem Radius %d cm um C" % c],
                   "C muss auf dem Thaleskreis über der Hypotenuse liegen: <b>Halbkreis mit r = %s cm</b>." % dz(Fr(c, 2)))
    if kind == "tangente":
        return mcq("Man konstruiert eine Tangente von einem Punkt P an einen Kreis mit Mittelpunkt M. Wozu zeichnet man den Thaleskreis über PM?", "Er schneidet den Kreis in den Berührpunkten, dort ist der Winkel 90°.",
                   ["Er gibt den Radius des Kreises an.", "Er halbiert die Strecke PM nicht.", "Er ersetzt den ursprünglichen Kreis."],
                   "Radius und Tangente stehen senkrecht aufeinander. Die Punkte mit rechtem Winkel liegen auf dem Thaleskreis über PM: <b>die Berührpunkte</b>.")
    if kind == "koord":
        x1, x2 = sorted(R.sample(range(-6, 9, 2), 2))
        y = R.randint(-3, 3)
        return mcq("A(%s | %s) und B(%s | %s). Wo liegt der Mittelpunkt des Thaleskreises über AB?" % (dz(x1), dz(y), dz(x2), dz(y)), "M(%s | %s)" % (dz((x1 + x2) // 2), dz(y)),
                   ["M(%s | %s)" % (dz(x2 - x1), dz(y)), "M(%s | 0)" % dz((x1 + x2) // 2) if y else "M(%s | 1)" % dz((x1 + x2) // 2), "M(%s | %s)" % (dz((x2 - x1) // 2), dz(y)) if (x2 - x1) // 2 != (x1 + x2) // 2 else "M(%s | %s)" % (dz(x1), dz(y))],
                   "Mitte von AB: x = (%s + %s) : 2 = %s. <b>M(%s | %s)</b>, Radius %d." % (dz(x1), dz(x2), dz((x1 + x2) // 2), dz((x1 + x2) // 2), dz(y), (x2 - x1) // 2))
    if kind == "quadrat":
        return mcq("C liegt auf dem Thaleskreis über AB genau über M (MC senkrecht zu AB). Wie groß sind α und β?", "beide 45°", ["beide 90°", "beide 60°", "30° und 60°"],
                   "Dann ist AC = BC, das Dreieck ist gleichschenklig-rechtwinklig: <b>45° und 45°</b>.")
    d = R.choice([6, 8, 10, 12])
    return mcq("Ein Zimmermann prüft, ob eine Ecke rechtwinklig ist: Er legt einen Halbkreis mit dem Durchmesser %d dm an die beiden Endpunkte. Die Ecke liegt genau auf dem Halbkreis. Was folgt?" % d, "Die Ecke ist rechtwinklig.",
               ["Die Ecke ist stumpf.", "Die Ecke ist spitz.", "Man kann nichts sagen."], "Umkehrung des Satzes des Thales: <b>Die Ecke ist rechtwinklig.</b>")


def main():
    seen = set()
    sets = [
        ("Der Satz des Thales", mix(R, seen, [(grund, 12), (umkehr, 8)])),
        ("Winkel im Thalesdreieck", mix(R, seen, [(winkel, 20)])),
        ("Gleichschenklige Teildreiecke", mix(R, seen, [(teil, 20)])),
        ("Umkehrung und Radius", mix(R, seen, [(umkehr, 20)])),
        ("Anwendungen", mix(R, seen, [(anwendung, 12), (winkel, 8)])),
    ]
    body = lesson(
        ["<b>Satz des Thales</b>: Liegt der Punkt C auf dem Halbkreis über der Strecke AB, so ist der Winkel bei C ein rechter Winkel (90°).",
         "Der Kreis heißt <b>Thaleskreis</b>. Sein Mittelpunkt M ist die Mitte von AB, sein Radius ist die Hälfte von AB.",
         "Da γ = 90°, gilt α + β = 90°. MA = MB = MC sind Radien, deshalb sind die Dreiecke AMC und BMC gleichschenklig.",
         "<b>Umkehrung</b>: Hat ein Dreieck bei C einen rechten Winkel, liegt C auf dem Kreis mit dem Durchmesser AB."],
        [example("C auf dem Thaleskreis, α = 35°", ["γ = 90°", "β = 90° − 35°"], "β = 55°"),
         example("AB = 9 cm", ["r = 9 cm : 2"], "r = 4,5 cm")],
        [["α + β = 180°", "γ ist schon 90°: α + β = 90°"],
         ["Radius = AB", "Radius = halbe Strecke AB"],
         ["Jeder Punkt über AB gibt 90°", "Nur Punkte auf dem Halbkreis"]])
    faq = [
        {"q": "Was sagt der Satz des Thales?", "a": "Jeder Winkel, dessen Scheitel auf einem Halbkreis liegt und dessen Schenkel durch die Enden des Durchmessers gehen, ist ein rechter Winkel."},
        {"q": "Wo liegt der Mittelpunkt des Thaleskreises?", "a": "In der Mitte der Strecke AB. Der Radius ist halb so lang wie AB."},
        {"q": "Wofür braucht man den Satz des Thales?", "a": "Zum Konstruieren rechtwinkliger Dreiecke, zum Prüfen rechter Winkel und zum Konstruieren von Tangenten an einen Kreis."},
        {"q": "Was passiert, wenn C nicht auf dem Kreis liegt?", "a": "Liegt C innerhalb, ist der Winkel bei C stumpf; liegt C außerhalb, ist er spitz."},
    ]
    make_unit(R, "satz-des-thales", "R",
              "Die Schülerinnen und Schüler nutzen den Satz des Thales und seine Umkehrung, berechnen Winkel im Thalesdreieck und in den gleichschenkligen Teildreiecken und wenden den Thaleskreis bei Konstruktionen an (Zusammenfassung).",
              "Satz des Thales",
              "Satz des Thales Klasse 8 – Thaleskreis, Winkel berechnen, Arbeitsblätter",
              "Satz des Thales",
              "Satz des Thales für Klasse 8: Thaleskreis, rechter Winkel bei C, Winkel berechnen, gleichschenklige Teildreiecke, Umkehrung und Anwendungen. 100 Aufgaben mit Lösungen, kostenlos.",
              "Auf dem Halbkreis über AB ist der Winkel bei C immer 90°.",
              "Also α + β = 90°.",
              body, faq, sets, 11, grade="klasse-8")


if __name__ == "__main__":
    main()
