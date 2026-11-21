# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 8: Zylinder – Volumen und Oberfläche（Leitidee Größen und Messen, Sek I）
  python3 tools/gen_de_mathe_k8_zylinder.py
Volumen V = πr²h, Mantelfläche M = 2πrh, Oberfläche O = 2πr² + 2πrh, Netz des Zylinders, Höhe oder Radius aus dem Volumen,
Hohlzylinder, Sachaufgaben (Dosen, Gläser, Rohre, Litfaßsäule). Gerundet mit π aus dem Taschenrechner.
Fehler: Durchmesser statt Radius, nur eine Grundfläche bei O, Mantel als πr²h, cm³ und Liter verwechselt.
"""
import random, math
from fractions import Fraction as Fr
from de_common import lesson, example, make_unit, mix, MAL, wrap, line, text, INK, RED, GREEN, FILL
from de_k6 import dz
from de_k8 import mcq

R = random.Random(49813)
PI = math.pi
G = ":"


def z(v, k=1):
    n = int(abs(float(v)) * 10 ** k + 0.5)
    ip, fp = divmod(n, 10 ** k)
    return dz(ip) + ("," + str(fp).rjust(k, "0") if k else "")


def zyl_svg(lr, lh):
    s = ["<path d='M40 50 L40 170 A70 18 0 0 0 180 170 L180 50' fill='%s' stroke='%s' stroke-width='2.5'/>" % (FILL, GREEN),
         "<ellipse cx='110' cy='50' rx='70' ry='18' fill='#e6f2ea' stroke='%s' stroke-width='2.5'/>" % GREEN,
         "<path d='M40 170 A70 18 0 0 1 180 170' fill='none' stroke='%s' stroke-width='1.5' stroke-dasharray='5 4'/>" % GREEN,
         line(110, 50, 180, 50, RED, 2) + text(145, 42, lr, 13, col=RED),
         line(196, 50, 196, 170, RED, 2) + text(202, 114, lh, 13, col=RED, anchor="start")]
    return wrap(280, 200, "".join(s), "Zylinder", lg=True)


def rh(big=False):
    r = R.randint(3, 12) if not big else R.randint(3, 15)
    h = R.randint(3, 25)
    return r, h


def volumen():
    r, h = rh()
    kind = R.choice(["r", "d", "bild"])
    V = PI * r * r * h
    w = ["%s cm³" % z(PI * (2 * r) ** 2 * h), "%s cm³" % z(2 * PI * r * h), "%s cm³" % z(PI * r * h)]
    if kind == "d":
        return mcq("Ein Zylinder hat den Durchmesser %d cm und die Höhe %d cm. Berechne das Volumen (auf eine Nachkommastelle)." % (2 * r, h), "%s cm³" % z(V), w,
                   "r = %d cm. V = π %s r² %s h = π %s %d² %s %d ≈ <b>%s cm³</b>." % (r, MAL, MAL, MAL, r, MAL, h, z(V)))
    pic = zyl_svg("r = %d cm" % r, "h = %d cm" % h) if kind == "bild" else ""
    return mcq(pic + ("Berechne das Volumen des Zylinders (auf eine Nachkommastelle)." if pic else "Ein Zylinder hat r = %d cm und h = %d cm. Berechne das Volumen (auf eine Nachkommastelle)." % (r, h)), "%s cm³" % z(V), w,
               "V = π %s r² %s h = π %s %d %s %d ≈ <b>%s cm³</b>." % (MAL, MAL, MAL, r * r, MAL, h, z(V)))


def mantel():
    r, h = rh()
    kind = R.choice(["m", "m", "netz", "grund"])
    if kind == "m":
        M = 2 * PI * r * h
        return mcq("Berechne die Mantelfläche eines Zylinders mit r = %d cm und h = %d cm (auf eine Nachkommastelle)." % (r, h), "%s cm²" % z(M),
                   ["%s cm²" % z(PI * r * h), "%s cm²" % z(PI * r * r * h), "%s cm²" % z(2 * PI * r * h + 2 * PI * r * r)],
                   "M = 2 %s π %s r %s h = 2 %s π %s %d %s %d ≈ <b>%s cm²</b>." % (MAL, MAL, MAL, MAL, MAL, r, MAL, h, z(M)))
    if kind == "netz":
        return mcq("Das Netz eines Zylinders besteht aus einem Rechteck und zwei Kreisen. Wie lang ist die lange Seite des Rechtecks bei r = %d cm (auf eine Nachkommastelle)?" % r, "%s cm" % z(2 * PI * r),
                   ["%s cm" % z(PI * r), "%s cm" % z(PI * r * r), "%d cm" % (2 * r)],
                   "Das Rechteck wird um die Grundfläche gewickelt. Seine Länge ist der Kreisumfang: 2 %s π %s %d ≈ <b>%s cm</b>." % (MAL, MAL, r, z(2 * PI * r)))
    return mcq("Berechne die Grundfläche eines Zylinders mit dem Durchmesser %d cm (auf eine Nachkommastelle)." % (2 * r), "%s cm²" % z(PI * r * r),
               ["%s cm²" % z(PI * 4 * r * r), "%s cm²" % z(2 * PI * r), "%s cm²" % z(PI * r)],
               "G = π %s r² = π %s %d² ≈ <b>%s cm²</b>." % (MAL, MAL, r, z(PI * r * r)))


def oberflaeche():
    r, h = rh()
    O = 2 * PI * r * r + 2 * PI * r * h
    kind = R.choice(["r", "bild", "offen"])
    if kind == "offen":
        v = PI * r * r + 2 * PI * r * h
        return mcq("Ein oben offenes zylinderförmiges Glas hat r = %d cm und h = %d cm. Wie groß ist seine Oberfläche (Boden und Mantel, auf eine Nachkommastelle)?" % (r, h), "%s cm²" % z(v),
                   ["%s cm²" % z(O), "%s cm²" % z(2 * PI * r * h), "%s cm²" % z(PI * r * r * h)],
                   "Nur ein Kreis: π %s %d² + 2 %s π %s %d %s %d ≈ <b>%s cm²</b>." % (MAL, r, MAL, MAL, r, MAL, h, z(v)))
    pic = zyl_svg("r = %d cm" % r, "h = %d cm" % h) if kind == "bild" else ""
    return mcq(pic + ("Berechne die Oberfläche des Zylinders (auf eine Nachkommastelle)." if pic else "Berechne die Oberfläche eines Zylinders mit r = %d cm und h = %d cm (auf eine Nachkommastelle)." % (r, h)), "%s cm²" % z(O),
               ["%s cm²" % z(PI * r * r + 2 * PI * r * h), "%s cm²" % z(2 * PI * r * h), "%s cm²" % z(PI * r * r * h)],
               "O = 2 %s π r² + 2 %s π r h = %s + %s ≈ <b>%s cm²</b>." % (MAL, MAL, z(2 * PI * r * r), z(2 * PI * r * h), z(O)))


def rueck():
    kind = R.choice(["h", "h", "liter", "r"])
    r, h = rh()
    if kind == "h":
        V = Fr(int(PI * r * r * h * 10 + 0.5), 10)
        return mcq("Ein Zylinder hat r = %d cm und das Volumen %s cm³. Wie hoch ist er (gerundet)?" % (r, dz(V)), "etwa %d cm" % h,
                   ["etwa %s cm" % z(float(V) / (PI * r)), "etwa %s cm" % z(float(V) / (r * r)), "etwa %s cm" % z(float(V) / (2 * PI * r))],
                   "h = V %s (π %s r²) = %s %s %s ≈ <b>%d cm</b>." % (G, MAL, dz(V), G, z(PI * r * r), h))
    if kind == "liter":
        V = PI * r * r * h
        return mcq("Wie viele Liter passen in einen Zylinder mit r = %d cm und h = %d cm (auf zwei Nachkommastellen)?" % (r, h), "%s l" % z(V / 1000, 2),
                   ["%s l" % z(V / 100, 2), "%s l" % z(V / 10, 1), "%s l" % z(V, 0)],
                   "V ≈ %s cm³. 1000 cm³ = 1 l: <b>%s l</b>." % (z(V), z(V / 1000, 2)))
    V = Fr(int(PI * r * r * h * 10 + 0.5), 10)
    return mcq("Ein Zylinder hat die Höhe %d cm und das Volumen %s cm³. Wie groß ist der Radius (gerundet)?" % (h, dz(V)), "etwa %d cm" % r,
               ["etwa %s cm" % z(float(V) / (PI * h)), "etwa %d cm" % (2 * r), "etwa %s cm" % z(float(V) / (2 * PI * h))],
               "r² = V %s (π %s h) ≈ %d, r = √%d = <b>%d cm</b>." % (G, MAL, r * r, r * r, r))


def sache():
    kind = R.choice(["dose", "rohr", "litfass", "tank", "etikett", "kerzen"])
    if kind == "dose":
        d, h = R.choice([(7, 11), (8, 12), (10, 12), (6, 10), (9, 14)])
        V = PI * (d / 2) ** 2 * h
        return mcq("Eine Konservendose hat den Durchmesser %d cm und die Höhe %d cm. Wie viel ml passen hinein (auf ganze ml)?" % (d, h), "etwa %d ml" % int(V + 0.5),
                   ["etwa %d ml" % int(PI * d * d * h + 0.5), "etwa %d ml" % int(PI * d * h + 0.5), "etwa %d ml" % int(V / 10 + 0.5)],
                   "V = π %s %s² %s %d ≈ %s cm³ = <b>%d ml</b>." % (MAL, dz(Fr(d, 2)), MAL, h, z(V), int(V + 0.5)))
    if kind == "rohr":
        ra, ri, l = R.choice([(5, 4, 100), (6, 5, 200), (3, 2, 150), (10, 8, 100), (4, 3, 50)])
        v = PI * (ra * ra - ri * ri) * l
        return mcq("Ein Rohr (Hohlzylinder) hat außen den Radius %d cm, innen %d cm und ist %d cm lang. Wie viel Material braucht man (auf ganze cm³)?" % (ra, ri, l), "etwa %d cm³" % int(v + 0.5),
                   ["etwa %d cm³" % int(PI * (ra - ri) ** 2 * l + 0.5), "etwa %d cm³" % int(PI * ra * ra * l + 0.5), "etwa %d cm³" % int(2 * PI * (ra - ri) * l + 0.5)],
                   "V = π %s (R² − r²) %s h = π %s (%d − %d) %s %d ≈ <b>%d cm³</b>." % (MAL, MAL, MAL, ra * ra, ri * ri, MAL, l, int(v + 0.5)))
    if kind == "litfass":
        d, h = R.choice([(1.2, 3), (1.4, 3), (1.2, 2.5), (1.5, 3.5)])
        M = PI * d * h
        return mcq("Eine Litfaßsäule hat den Durchmesser %s m und ist %s m hoch. Wie viel Fläche steht für Plakate zur Verfügung (Mantel, auf eine Nachkommastelle)?" % (dz(Fr(d).limit_denominator(10)), dz(Fr(h).limit_denominator(10))), "%s m²" % z(M),
                   ["%s m²" % z(PI * (d / 2) ** 2 * h), "%s m²" % z(2 * PI * d * h), "%s m²" % z(M + 2 * PI * (d / 2) ** 2)],
                   "M = π %s d %s h = π %s %s %s %s ≈ <b>%s m²</b>." % (MAL, MAL, MAL, dz(Fr(d).limit_denominator(10)), MAL, dz(Fr(h).limit_denominator(10)), z(M)))
    if kind == "tank":
        r, h = R.choice([(1, 2), (Fr(1, 2), 1), (Fr(3, 2), 2), (2, 3)])
        V = PI * float(r) ** 2 * float(h)
        return mcq("Ein zylinderförmiger Wassertank hat den Radius %s m und die Höhe %s m. Wie viele Liter fasst er (auf ganze Liter)?" % (dz(r), dz(h)), "etwa %s l" % z(V * 1000, 0),
                   ["etwa %s l" % z(V * 100, 0), "etwa %s l" % z(V, 1), "etwa %s l" % z(2 * PI * float(r) * float(h) * 1000, 0)],
                   "V = π %s %s² %s %s ≈ %s m³. 1 m³ = 1000 l: <b>%s l</b>." % (MAL, dz(r), MAL, dz(h), z(V, 3), z(V * 1000, 0)))
    if kind == "etikett":
        d, h = R.choice([(7, 8), (8, 10), (6, 9), (10, 6)])
        return mcq("Um eine Dose mit %d cm Durchmesser wird ein Etikett geklebt, das %d cm hoch ist und genau einmal herumreicht. Wie groß ist das Etikett (auf eine Nachkommastelle)?" % (d, h), "%s cm²" % z(PI * d * h),
                   ["%s cm²" % z(PI * (d / 2) ** 2 * h), "%s cm²" % z(2 * PI * d * h), "%s cm²" % z(d * h)],
                   "Länge = Umfang π %s %d ≈ %s cm. Mal %d: <b>%s cm²</b>." % (MAL, d, z(PI * d), h, z(PI * d * h)))
    r, h, n = R.choice([(Fr(3, 2), 10, 20), (3, 12, 10), (4, 15, 12), (Fr(5, 2), 8, 30)])
    V = PI * float(r) ** 2 * h * n
    return mcq("Wie viel Wachs braucht man für %d Kerzen (Zylinder mit r = %s cm, h = %d cm)? Runde auf ganze cm³." % (n, dz(r), h), "etwa %s cm³" % z(V, 0),
               ["etwa %s cm³" % z(V / n, 0), "etwa %s cm³" % z(V * 4, 0), "etwa %s cm³" % z(2 * PI * float(r) * h * n, 0)],
               "Eine Kerze: π %s %s² %s %d ≈ %s cm³. Mal %d: <b>%s cm³</b>." % (MAL, dz(r), MAL, h, z(V / n), n, z(V, 0)))


def main():
    seen = set()
    sets = [
        ("Volumen", mix(R, seen, [(volumen, 20)])),
        ("Grundfläche, Mantel und Netz", mix(R, seen, [(mantel, 20)])),
        ("Oberfläche", mix(R, seen, [(oberflaeche, 20)])),
        ("Rückwärts rechnen", mix(R, seen, [(rueck, 20)])),
        ("Sachaufgaben", mix(R, seen, [(sache, 20)])),
    ]
    body = lesson(
        ["Ein <b>Zylinder</b> hat zwei gleich große Kreise als Grund- und Deckfläche und eine gewölbte Mantelfläche.",
         "<b>Volumen</b>: V = G %s h = π %s r² %s h." % (MAL, MAL, MAL),
         "<b>Mantelfläche</b>: Abgewickelt ist der Mantel ein Rechteck mit der Länge 2πr (Kreisumfang) und der Breite h: M = 2 %s π %s r %s h." % (MAL, MAL, MAL),
         "<b>Oberfläche</b>: O = 2 %s G + M = 2πr² + 2πrh. 1 dm³ = 1 l, 1 cm³ = 1 ml." % MAL],
        [example("r = 3 cm, h = 10 cm", ["V = π %s 9 %s 10 ≈ 282,7 cm³" % (MAL, MAL), "O = 2π %s 9 + 2π %s 3 %s 10 ≈ 245,0 cm²" % (MAL, MAL, MAL)], "V ≈ 282,7 cm³, O ≈ 245,0 cm²")],
        [["d = 8 cm: V = π %s 8² %s h" % (MAL, MAL), "Radius 4 cm verwenden"],
         ["O = πr² + 2πrh", "Zwei Kreise: 2πr² + 2πrh (bei offenen Gefäßen nur einer)"],
         ["1000 cm³ = 10 l", "1000 cm³ = 1 l"]])
    faq = [
        {"q": "Wie berechne ich das Volumen eines Zylinders?", "a": "V = π · r² · h: Grundfläche (Kreis) mal Höhe."},
        {"q": "Wie berechne ich die Oberfläche?", "a": "O = 2πr² + 2πrh: zwei Kreise plus Mantel. Ein offenes Glas hat nur einen Kreis."},
        {"q": "Wie sieht das Netz eines Zylinders aus?", "a": "Ein Rechteck (Länge = Kreisumfang, Breite = Höhe) und zwei Kreise."},
        {"q": "Wie rechne ich in Liter um?", "a": "1 cm³ = 1 ml und 1000 cm³ = 1 dm³ = 1 l. 1 m³ = 1000 l."},
    ]
    make_unit(R, "zylinder", "G",
              "Die Schülerinnen und Schüler berechnen Volumen, Mantelfläche und Oberfläche von Zylindern und Hohlzylindern, bestimmen fehlende Größen und lösen Sachaufgaben (Zusammenfassung).",
              "Zylinder: Volumen und Oberfläche",
              "Zylinder Volumen und Oberfläche Klasse 8 – Arbeitsblätter mit Lösungen",
              "Zylinder",
              "Zylinder für Klasse 8: Volumen V = πr²h, Mantelfläche, Oberfläche, Netz, Höhe und Radius bestimmen, Hohlzylinder und Sachaufgaben. 100 Aufgaben mit Lösungen, kostenlos.",
              "V = πr²h",
              "O = 2πr² + 2πrh",
              body, faq, sets, 13, grade="klasse-8")


if __name__ == "__main__":
    main()
