# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 10: Bogenmaß und Kreisausschnitt（Leitidee Größen und Messen, Sek I）
  python3 tools/gen_de_mathe_k10_bogenmass_und_kreisausschnitt.py
Kreisbogen b = α/360° · 2πr, Kreisausschnitt A = α/360° · πr² = b · r / 2, Gradmaß ↔ Bogenmaß (x = α/180° · π),
Bogenlänge am Einheitskreis, Mittelpunktswinkel und Radius zurückrechnen, Sachaufgaben (Uhrzeiger, Scheibenwischer, Pizza).
Fehler: α/360 · πr² mit 2πr verwechselt, Bogenmaß mit 360 statt 180, Durchmesser statt Radius, Faktor α/360 vergessen.
"""
import random, math
from fractions import Fraction as Fr
from de_common import lesson, example, make_unit, mix, MAL, num, wrap, line, text, INK, RED, BLUE, FILL
from de_k6 import bh, dz
from de_k10 import mcq, zr, pi_txt

R = random.Random(50006)
PI = math.pi
WINKEL = [30, 36, 40, 45, 60, 72, 80, 90, 100, 108, 120, 135, 144, 150, 160, 180, 210, 225, 240, 270, 288, 300, 315]


def sektor(r_txt, a, lab_a=True, b_txt=None, label="Kreisausschnitt"):
    W, H = 300, 260
    cx, cy, r = 150, 132, 104
    a0 = 90 - a / 2.0
    a1 = 90 + a / 2.0
    P = lambda ang, rr=r: (cx + rr * math.cos(math.radians(ang)), cy - rr * math.sin(math.radians(ang)))
    x0, y0 = P(a0)
    x1, y1 = P(a1)
    s = ["<circle cx='%d' cy='%d' r='%d' fill='none' stroke='#999' stroke-width='1.6' stroke-dasharray='5 5'/>" % (cx, cy, r),
         "<path d='M%d %d L%.1f %.1f A%d %d 0 %d 0 %.1f %.1f Z' fill='%s' stroke='%s' stroke-width='2.6'/>" % (cx, cy, x0, y0, r, r, 1 if a > 180 else 0, x1, y1, FILL, INK),
         "<circle cx='%d' cy='%d' r='3.5' fill='%s'/>" % (cx, cy, INK)]
    # Radius-Beschriftung außen neben dem rechten Schenkel
    if a <= 250:
        mxr, myr = P(a0, r * 0.62)
        nx, ny = math.cos(math.radians(a0 - 90)), -math.sin(math.radians(a0 - 90))
        s.append(text(mxr + nx * 16, myr + ny * 16 + 6, r_txt, 17, col=BLUE, weight=700, anchor="start" if nx >= -0.2 else "end"))
    else:
        # eigener Radius nach links (liegt im Ausschnitt), Beschriftung darüber
        s.append(line(cx, cy, cx - r, cy, BLUE, 2.2))
        s.append(text(cx - r * 0.62, cy - 10, r_txt, 17, col=BLUE, weight=700))
    if lab_a:
        rr = 30 if a >= 60 else 46
        s.append("<path d='M%.1f %.1f A%d %d 0 %d 0 %.1f %.1f' fill='none' stroke='%s' stroke-width='2'/>" % (P(a0, rr)[0], P(a0, rr)[1], rr, rr, 1 if a > 180 else 0, P(a1, rr)[0], P(a1, rr)[1], RED))
        tx, ty = P(90, rr + 20)
        s.append(text(tx, ty + 6, "%d°" % a, 17, col=RED, weight=700))
    if b_txt:
        bx, by = P(90, r + 16)
        s.append(text(bx, by + 4, b_txt, 17, col=INK, weight=700))
    return wrap(W, H, "".join(s), label, lg=True)


def gr2rad():
    a = R.choice(WINKEL + [360, 18, 20, 330])
    x = Fr(a, 180)
    if R.random() < 0.6:
        return mcq("Gib %d° im Bogenmaß an (als Vielfaches von π)." % a, pi_txt(x),
                   [pi_txt(Fr(a, 360)), pi_txt(Fr(a, 90)), pi_txt(Fr(180, a)) if Fr(180, a) != x else pi_txt(x * 3)],
                   "x = %d°/180° %s π = <b>%s</b>." % (a, MAL, pi_txt(x)))
    return mcq("Welches Gradmaß gehört zum Bogenmaß %s?" % pi_txt(x), "%d°" % a,
               ["%s°" % zr(a / 2, 0) if a % 2 == 0 else "%d°" % (a * 2), "%d°" % (a * 2) if a * 2 != a else "%d°" % (a + 90), "%s°" % zr(float(x) * 360, 0) if x * 360 != a * 2 else "%d°" % (a + 180)],
               "π entspricht 180°, also %s = %s %s 180° = <b>%d°</b>." % (pi_txt(x), bh(x) if x.denominator != 1 else dz(x), MAL, a))


def dezimal():
    kind = R.choice(["g", "g", "r", "e"])
    if kind == "g":
        a = R.choice([10, 25, 50, 75, 100, 110, 130, 200, 250, 57, 15, 5])
        x = a * PI / 180
        return mcq("Gib %d° im Bogenmaß an (auf zwei Nachkommastellen)." % a, "≈ %s" % zr(x, 2),
                   ["≈ %s" % zr(a * PI / 360, 2), "≈ %s" % zr(a / 180, 2), "≈ %s" % zr(a * PI / 90, 2)], "x = %d %s π : 180 ≈ <b>%s</b>." % (a, MAL, zr(x, 2)))
    if kind == "r":
        x = R.choice([Fr(1), Fr(2), Fr(3), Fr(1, 2), Fr(3, 2), Fr(5, 2), Fr(4), Fr(6, 5)])
        a = float(x) * 180 / PI
        return mcq("Welchem Winkel im Gradmaß entspricht das Bogenmaß %s (auf eine Nachkommastelle)?" % dz(x), "≈ %s°" % zr(a, 1),
                   ["≈ %s°" % zr(float(x) * 180, 1), "≈ %s°" % zr(float(x) * 90 / PI, 1), "≈ %s°" % zr(float(x) * 360 / PI, 1)], "α = %s %s 180° : π ≈ <b>%s°</b>." % (dz(x), MAL, zr(a, 1)))
    a = R.choice(WINKEL)
    x = Fr(a, 180)
    return mcq("Wie lang ist am Einheitskreis (r = 1) der Bogen zum Winkel %d°?" % a, "%s ≈ %s" % (pi_txt(x), zr(float(x) * PI, 2)),
               ["%s ≈ %s" % (pi_txt(x * 2), zr(float(x) * 2 * PI, 2)), "%s ≈ %s" % (pi_txt(x / 2), zr(float(x) / 2 * PI, 2)), "%d" % a],
               "Am Einheitskreis ist die Bogenlänge gleich dem Bogenmaß: <b>%s ≈ %s</b>." % (pi_txt(x), zr(float(x) * PI, 2)))


def bogen():
    r = R.choice([3, 4, 5, 6, 8, 10, 12, 15, 2.5])
    a = R.choice(WINKEL)
    b = a / 360 * 2 * PI * r
    rs = dz(Fr(r).limit_denominator(10))
    pic = sektor("r = %s cm" % rs, a, label="Kreisausschnitt mit Radius %s cm und Winkel %d Grad" % (rs, a)) if R.random() < 0.7 else ""
    q = (pic + "Berechne die Länge des Kreisbogens (auf eine Nachkommastelle).") if pic else "Ein Kreis hat den Radius %s cm. Wie lang ist der Bogen zum Mittelpunktswinkel %d° (auf eine Nachkommastelle)?" % (rs, a)
    return mcq(q, "b ≈ %s cm" % zr(b, 1),
               ["b ≈ %s cm" % zr(a / 360 * PI * r * r, 1), "b ≈ %s cm" % zr(2 * PI * r, 1), "b ≈ %s cm" % zr(a / 360 * PI * r, 1)],
               "b = %d°/360° %s 2π %s %s ≈ <b>%s cm</b>." % (a, MAL, MAL, rs, zr(b, 1)))


def flaeche():
    r = R.choice([3, 4, 5, 6, 7, 8, 10, 12, 9])
    a = R.choice(WINKEL)
    A = a / 360 * PI * r * r
    kind = R.choice(["bild", "bild", "text", "br"])
    if kind == "br":
        b = R.choice([4, 5, 6, 8, 9, 10, 12, 15])
        if b >= 2 * PI * r:
            return None
        return mcq("Ein Kreisausschnitt hat den Radius %d cm und die Bogenlänge %d cm. Wie groß ist sein Flächeninhalt?" % (r, b), "%s cm²" % dz(Fr(b * r, 2)),
                   ["%s cm²" % dz(b * r), "%s cm²" % zr(b * r * PI / 2, 1), "%s cm²" % dz(Fr(b * r * r, 2))],
                   "A = b %s r : 2 = %d %s %d : 2 = <b>%s cm²</b>." % (MAL, b, MAL, r, dz(Fr(b * r, 2))))
    pic = sektor("r = %d cm" % r, a, label="Kreisausschnitt mit Radius %d cm und Winkel %d Grad" % (r, a)) if kind == "bild" else ""
    q = (pic + "Berechne den Flächeninhalt des Kreisausschnitts (auf eine Nachkommastelle).") if pic else "Wie groß ist der Flächeninhalt eines Kreisausschnitts mit r = %d cm und α = %d° (auf eine Nachkommastelle)?" % (r, a)
    return mcq(q, "A ≈ %s cm²" % zr(A, 1),
               ["A ≈ %s cm²" % zr(a / 360 * 2 * PI * r, 1), "A ≈ %s cm²" % zr(PI * r * r, 1), "A ≈ %s cm²" % zr(a / 360 * PI * (2 * r) ** 2, 1)],
               "A = %d°/360° %s π %s %d² ≈ <b>%s cm²</b>." % (a, MAL, MAL, r, zr(A, 1)))


def sach():
    kind = R.choice(["alpha", "radius", "uhr", "wisch", "pizza", "rad"])
    if kind == "alpha":
        r = R.choice([3, 6, 9, 12, 18])
        a = R.choice([40, 60, 80, 120, 150, 200, 240])
        k = Fr(a, 360) * 2 * r
        return mcq("Ein Kreisbogen mit dem Radius %d cm ist %s cm lang. Wie groß ist der Mittelpunktswinkel?" % (r, (bh(k) if k.denominator != 1 else dz(k)) + "π"),
                   "α = %d°" % a, ["α = %d°" % (a // 2), "α = %d°" % (a * 2) if a * 2 < 360 else "α = %d°" % (a + 30), "α = %s°" % zr(float(k) * 180 / r, 0) if float(k) * 180 / r != a else "α = %d°" % (a + 10)],
                   "α = b : (2πr) %s 360° = %sπ : %dπ %s 360° = <b>%d°</b>." % (MAL, bh(k) if k.denominator != 1 else dz(k), 2 * r, MAL, a))
    if kind == "radius":
        a = R.choice([60, 90, 120, 180])
        r = R.choice([4, 5, 6, 8, 10])
        A = Fr(a, 360) * r * r
        return mcq("Ein Kreisausschnitt mit α = %d° hat den Flächeninhalt %sπ cm². Wie groß ist der Radius?" % (a, dz(A) if A.denominator == 1 else bh(A)), "r = %d cm" % r,
                   ["r = %s cm" % zr(math.sqrt(float(A)), 1), "r = %d cm" % (r * r), "r = %s cm" % zr(float(A) * 360 / a / 2, 1)],
                   "π r² = %sπ %s 360/%d = %dπ ⇒ r² = %d ⇒ <b>r = %d cm</b>." % (dz(A) if A.denominator == 1 else bh(A), MAL, a, r * r, r * r, r))
    if kind == "uhr":
        L = R.choice([8, 10, 12, 15, 20])
        m = R.choice([10, 15, 20, 25, 40, 45])
        b = m / 60 * 2 * PI * L
        return mcq("Der Minutenzeiger einer Uhr ist %d cm lang. Welchen Weg legt seine Spitze in %d Minuten zurück (auf eine Nachkommastelle)?" % (L, m), "≈ %s cm" % zr(b, 1),
                   ["≈ %s cm" % zr(m / 60 * PI * L * L, 1), "≈ %s cm" % zr(m / 60 * PI * L, 1), "≈ %s cm" % zr(m / 360 * 2 * PI * L, 1)],
                   "%d min sind %d° (%s Umdrehung): b = %d/60 %s 2π %s %d ≈ <b>%s cm</b>." % (m, m * 6, bh(Fr(m, 60)), m, MAL, MAL, L, zr(b, 1)))
    if kind == "wisch":
        L = R.choice([40, 45, 50, 55, 60])
        a = R.choice([90, 100, 110, 120, 135])
        A = a / 360 * PI * L * L
        return mcq("Ein Scheibenwischer ist %d cm lang und überstreicht einen Winkel von %d°. Welche Fläche wischt er (auf ganze cm²)?" % (L, a), "≈ %s cm²" % num(round(A)),
                   ["≈ %s cm²" % num(round(a / 360 * 2 * PI * L)), "≈ %s cm²" % num(round(PI * L * L)), "≈ %s cm²" % num(round(a / 180 * PI * L * L))],
                   "A = %d/360 %s π %s %d² ≈ <b>%s cm²</b>." % (a, MAL, MAL, L, num(round(A))))
    if kind == "pizza":
        d = R.choice([24, 26, 28, 30, 32, 36])
        n = R.choice([6, 8, 10, 12])
        A = PI * (d / 2) ** 2 / n
        return mcq("Eine Pizza (Durchmesser %d cm) wird in %d gleiche Stücke geschnitten. Wie groß ist ein Stück (auf eine Nachkommastelle)?" % (d, n), "≈ %s cm²" % zr(A, 1),
                   ["≈ %s cm²" % zr(PI * d * d / n, 1), "≈ %s cm²" % zr(PI * d / n, 1), "≈ %s cm²" % zr(PI * (d / 2) ** 2 / (n / 2), 1)],
                   "r = %d cm, Winkel 360° : %d = %d°: A = π %s %d² : %d ≈ <b>%s cm²</b>." % (d // 2, n, 360 // n, MAL, d // 2, n, zr(A, 1)))
    r = R.choice([30, 35, 40, 50, 60])
    k = R.choice([1, 2, 5, 10, 100])
    s = k * 2 * PI * r / 100
    return mcq("Ein Rad hat den Radius %d cm. Welche Strecke legt es bei %d %s zurück (auf zwei Nachkommastellen, in m)?" % (r, k, "Umdrehung" if k == 1 else "Umdrehungen"), "≈ %s m" % zr(s, 2),
               ["≈ %s m" % zr(k * PI * r / 100, 2), "≈ %s m" % zr(k * PI * r * r / 100, 2), "≈ %s m" % zr(k * 2 * PI * r / 10, 2)],
               "Pro Umdrehung 2π %s %d cm ≈ %s cm: %d %s %s cm ≈ <b>%s m</b>." % (MAL, r, zr(2 * PI * r, 1), k, MAL, zr(2 * PI * r, 1), zr(s, 2)))


def main():
    seen = set()
    sets = [
        ("Gradmaß und Bogenmaß", mix(R, seen, [(gr2rad, 20)])),
        ("Bogenmaß als Dezimalzahl", mix(R, seen, [(dezimal, 20)])),
        ("Kreisbogen", mix(R, seen, [(bogen, 20)])),
        ("Kreisausschnitt", mix(R, seen, [(flaeche, 20)])),
        ("Sachaufgaben", mix(R, seen, [(sach, 20)])),
    ]
    body = lesson(
        ["Ein <b>Kreisausschnitt</b> ist ein Teil des Kreises mit dem Mittelpunktswinkel α. Er ist der Anteil α/360° vom ganzen Kreis.",
         "Kreisbogen: b = α/360° %s 2πr. Flächeninhalt: A = α/360° %s πr² = b %s r : 2." % (MAL, MAL, MAL),
         "<b>Bogenmaß</b>: Der Winkel wird durch die Bogenlänge am Einheitskreis (r = 1) angegeben. 180° = π, also x = α/180° %s π." % MAL],
        [example("r = 6 cm, α = 120°", ["b = 120/360 %s 2π %s 6 = 4π" % (MAL, MAL), "A = 120/360 %s π %s 36 = 12π" % (MAL, MAL)], "b ≈ 12,6 cm, A ≈ 37,7 cm²"),
         example("90° im Bogenmaß", ["90/180 %s π" % MAL], "π/2")],
        [["Bogen: α/360 %s πr²" % MAL, "Bogen mit Umfang 2πr, Fläche mit πr²"],
         ["60° = 60/360 %s π = π/6" % MAL, "60° = 60/180 %s π = π/3" % MAL],
         ["Pizza 30 cm: r = 30", "Durchmesser halbieren: r = 15 cm"]])
    faq = [
        {"q": "Wie berechne ich die Länge eines Kreisbogens?", "a": "b = α/360° · 2πr, also der Anteil des Winkels am Kreisumfang."},
        {"q": "Wie berechne ich den Flächeninhalt eines Kreisausschnitts?", "a": "A = α/360° · πr² oder, wenn der Bogen bekannt ist, A = b · r / 2."},
        {"q": "Was ist das Bogenmaß?", "a": "Die Länge des Bogens am Einheitskreis. 180° entsprechen π, 90° entsprechen π/2."},
        {"q": "Wie rechne ich 1 im Bogenmaß in Grad um?", "a": "α = 1 · 180° : π ≈ 57,3°."},
    ]
    make_unit(R, "bogenmass-und-kreisausschnitt", "G",
              "Die Schülerinnen und Schüler berechnen Kreisbögen und Kreisausschnitte, rechnen zwischen Gradmaß und Bogenmaß um und lösen Sachaufgaben mit Kreisteilen (Zusammenfassung).",
              "Bogenmaß und Kreisausschnitt",
              "Bogenmaß und Kreisausschnitt Klasse 10 – Kreisbogen, Sektor, Arbeitsblätter mit Lösungen",
              "Bogenmaß und Kreisausschnitt",
              "Bogenmaß und Kreisausschnitt für Klasse 10: Gradmaß und Bogenmaß umrechnen, Kreisbogen, Flächeninhalt des Kreisausschnitts und Sachaufgaben. 100 Aufgaben mit Lösungen, kostenlos.",
              "b = α/360° · 2πr",
              "A = α/360° · πr². 180° = π im Bogenmaß.",
              body, faq, sets, 6, grade="klasse-10")


if __name__ == "__main__":
    main()
