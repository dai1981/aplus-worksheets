# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 8: Kreisumfang und Kreisfläche（Leitidee Größen und Messen, Sek I）
  python3 tools/gen_de_mathe_k8_kreisumfang_und_kreisflaeche.py
Umfang u = 2πr = πd, Flächeninhalt A = πr², Radius aus Umfang oder Fläche, Kreisring, Kreisausschnitt (Halb- und Viertelkreis, Winkel α),
zusammengesetzte Figuren, Sachaufgaben (Räder, Pizza, Beete). Gerundet mit π aus dem Taschenrechner.
Fehler: Durchmesser statt Radius in A = πr², u und A verwechselt, πr² als (πr)², Kreisring als π(R − r)².
"""
import random, math
from fractions import Fraction as Fr
from de_common import lesson, example, make_unit, mix, MAL, wrap, line, text, INK, BLUE, RED, GREEN, FILL
from de_k6 import dz
from de_k8 import mcq

R = random.Random(49812)
PI = math.pi
G = ":"


def z(v, k=1):
    n = int(abs(float(v)) * 10 ** k + 0.5)
    ip, fp = divmod(n, 10 ** k)
    return ("−" if v < 0 else "") + dz(ip) + ("," + str(fp).rjust(k, "0") if k else "")


def kreis_svg(r_txt, d=False):
    s = ["<circle cx='110' cy='100' r='75' fill='%s' stroke='%s' stroke-width='2.5'/>" % (FILL, GREEN), "<circle cx='110' cy='100' r='3' fill='%s'/>" % INK]
    if d:
        s.append(line(35, 100, 185, 100, RED, 2) + text(110, 92, r_txt, 14, col=RED))
    else:
        s.append(line(110, 100, 185, 100, RED, 2) + text(148, 92, r_txt, 14, col=RED))
    return wrap(220, 200, "".join(s), "Kreis", lg=True)


def umfang():
    kind = R.choice(["r", "d", "bild"])
    r = R.randint(2, 30) if R.random() < 0.7 else Fr(R.randint(5, 95), 10)
    r = Fr(r)
    u = 2 * PI * float(r)
    if kind == "d":
        d = 2 * r
        return mcq("Ein Kreis hat den Durchmesser d = %s cm. Berechne den Umfang (auf eine Nachkommastelle)." % dz(d), "%s cm" % z(PI * float(d)),
                   ["%s cm" % z(2 * PI * float(d)), "%s cm" % z(PI * float(d) ** 2 / 4), "%s cm" % z(PI * float(d) ** 2)],
                   "u = π %s d = π %s %s ≈ <b>%s cm</b>." % (MAL, MAL, dz(d), z(PI * float(d))))
    pic = kreis_svg("r = %s cm" % dz(r)) if kind == "bild" else ""
    return mcq(pic + ("Berechne den Umfang des Kreises (auf eine Nachkommastelle)." if pic else "Ein Kreis hat den Radius r = %s cm. Berechne den Umfang (auf eine Nachkommastelle)." % dz(r)), "%s cm" % z(u),
               ["%s cm" % z(PI * float(r)), "%s cm" % z(PI * float(r) ** 2), "%s cm" % z(4 * PI * float(r))],
               "u = 2 %s π %s r = 2 %s π %s %s ≈ <b>%s cm</b>." % (MAL, MAL, MAL, MAL, dz(r), z(u)))


def flaeche():
    kind = R.choice(["r", "d", "bild"])
    r = Fr(R.randint(2, 25)) if R.random() < 0.7 else Fr(R.randint(5, 95), 10)
    A = PI * float(r) ** 2
    if kind == "d":
        d = 2 * r
        return mcq("Ein Kreis hat den Durchmesser d = %s m. Berechne den Flächeninhalt (auf eine Nachkommastelle)." % dz(d), "%s m²" % z(A),
                   ["%s m²" % z(PI * float(d) ** 2), "%s m²" % z(PI * float(d)), "%s m²" % z(2 * PI * float(r))],
                   "r = %s m. A = π %s r² = π %s %s² ≈ <b>%s m²</b>." % (dz(r), MAL, MAL, dz(r), z(A)))
    pic = kreis_svg("d = %s cm" % dz(2 * r), d=True) if kind == "bild" else ""
    return mcq(pic + ("Berechne den Flächeninhalt des Kreises (auf eine Nachkommastelle)." if pic else "Ein Kreis hat den Radius r = %s cm. Berechne den Flächeninhalt (auf eine Nachkommastelle)." % dz(r)), "%s cm²" % z(A),
               ["%s cm²" % z(2 * PI * float(r)), "%s cm²" % z(PI * float(2 * r) ** 2), "%s cm²" % z((PI * float(r)) ** 2)],
               "%sA = π %s r² = π %s %s² ≈ <b>%s cm²</b>." % ("r = d : 2 = %s cm. " % dz(r) if pic else "", MAL, MAL, dz(r), z(A)))


def rueck():
    kind = R.choice(["r_u", "d_u", "r_A"])
    r = R.randint(2, 20)
    if kind == "r_u":
        u = 2 * PI * r
        uu = Fr(int(u * 10 + 0.5), 10)
        return mcq("Ein Kreis hat den Umfang %s cm. Wie groß ist der Radius (gerundet)?" % dz(uu), "etwa %d cm" % r, ["etwa %s cm" % z(float(uu) / PI), "etwa %s cm" % z(float(uu) / 2), "etwa %s cm" % z(math.sqrt(float(uu) / PI))],
                   "r = u %s (2π) = %s %s %s ≈ <b>%d cm</b>." % (G, dz(uu), G, z(2 * PI, 2), r))
    if kind == "d_u":
        u = PI * 2 * r
        uu = Fr(int(u * 10 + 0.5), 10)
        return mcq("Ein Rad hat den Umfang %s cm. Wie groß ist sein Durchmesser (gerundet)?" % dz(uu), "etwa %d cm" % (2 * r), ["etwa %d cm" % r, "etwa %s cm" % z(float(uu) / 2), "etwa %s cm" % z(float(uu) * PI, 0)],
                   "d = u %s π = %s %s π ≈ <b>%d cm</b>." % (G, dz(uu), G, 2 * r))
    A = PI * r * r
    AA = Fr(int(A * 10 + 0.5), 10)
    return mcq("Ein Kreis hat den Flächeninhalt %s cm². Wie groß ist der Radius (gerundet)?" % dz(AA), "etwa %d cm" % r, ["etwa %s cm" % z(float(AA) / PI), "etwa %s cm" % z(float(AA) / (2 * PI)), "etwa %d cm" % (2 * r)],
               "r² = A %s π ≈ %d, also r = √%d = <b>%d cm</b>." % (G, r * r, r * r, r))


def teile():
    kind = R.choice(["halb", "viertel", "sektor", "ring", "sektor_b"])
    r = R.randint(2, 15)
    if kind == "halb":
        return mcq("Berechne den Flächeninhalt eines Halbkreises mit r = %d cm (auf eine Nachkommastelle)." % r, "%s cm²" % z(PI * r * r / 2), ["%s cm²" % z(PI * r * r), "%s cm²" % z(PI * r), "%s cm²" % z(PI * r * r / 4)],
                   "A = π %s r² %s 2 = <b>%s cm²</b>." % (MAL, G, z(PI * r * r / 2)))
    if kind == "viertel":
        return mcq("Berechne den Umfang eines Viertelkreises mit r = %d cm (Bogen und zwei Radien, auf eine Nachkommastelle)." % r, "%s cm" % z(PI * r / 2 + 2 * r), ["%s cm" % z(PI * r / 2), "%s cm" % z(2 * PI * r + 2 * r), "%s cm" % z(PI * r / 2 + r)],
                   "Bogen: 2πr %s 4 = %s cm. Dazu 2 %s %d cm: <b>%s cm</b>." % (G, z(PI * r / 2), MAL, r, z(PI * r / 2 + 2 * r)))
    if kind in ("sektor", "sektor_b"):
        a = R.choice([30, 45, 60, 72, 90, 120, 135, 150, 240, 270])
        if kind == "sektor":
            v = PI * r * r * a / 360
            return mcq("Berechne den Flächeninhalt eines Kreisausschnitts mit r = %d cm und α = %d° (auf eine Nachkommastelle)." % (r, a), "%s cm²" % z(v), ["%s cm²" % z(2 * PI * r * a / 360), "%s cm²" % z(PI * r * r), "%s cm²" % z(PI * r * r * a / 180)],
                       "A = π %s r² %s α %s 360° = π %s %d² %s %d %s 360 ≈ <b>%s cm²</b>." % (MAL, MAL, G, MAL, r, MAL, a, G, z(v)))
        v = 2 * PI * r * a / 360
        return mcq("Wie lang ist der Kreisbogen bei r = %d cm und α = %d° (auf eine Nachkommastelle)?" % (r, a), "%s cm" % z(v), ["%s cm" % z(PI * r * r * a / 360), "%s cm" % z(2 * PI * r), "%s cm" % z(PI * r * a / 360)],
                   "b = 2 %s π %s r %s α %s 360° ≈ <b>%s cm</b>." % (MAL, MAL, MAL, G, z(v)))
    R2 = r + R.randint(1, 6)
    v = PI * (R2 * R2 - r * r)
    return mcq("Ein Kreisring hat den Außenradius %d cm und den Innenradius %d cm. Berechne seinen Flächeninhalt (auf eine Nachkommastelle)." % (R2, r), "%s cm²" % z(v),
               ["%s cm²" % z(PI * (R2 - r) ** 2), "%s cm²" % z(PI * R2 * R2), "%s cm²" % z(2 * PI * (R2 - r))],
               "A = π %s (R² − r²) = π %s (%d − %d) ≈ <b>%s cm²</b>." % (MAL, MAL, R2 * R2, r * r, z(v)))


def sache():
    kind = R.choice(["rad", "pizza", "beet", "uhr", "tisch", "runde"])
    if kind == "rad":
        d = R.choice([50, 60, 66, 70, 71])
        n = R.choice([100, 500, 1000])
        s = PI * d * n / 100
        return mcq("Ein Fahrradreifen hat den Durchmesser %d cm. Wie weit kommt das Rad bei %s Umdrehungen (in m, auf ganze Meter)?" % (d, "%d" % n if n < 1000 else "1000"), "etwa %d m" % int(s + 0.5),
                   ["etwa %d m" % int(2 * s + 0.5), "etwa %d m" % int(d * n / 100 + 0.5), "etwa %d m" % int(s / 2 + 0.5)],
                   "Umfang: π %s %d cm ≈ %s cm. Mal %d ≈ %s cm ≈ <b>%d m</b>." % (MAL, d, z(PI * d), n, z(PI * d * n, 0), int(s + 0.5)))
    if kind == "pizza":
        d1, d2 = R.choice([(26, 32), (28, 36), (30, 40), (24, 32)])
        p1, p2 = R.choice([(7, 10), (8, 12), (9, 14), (6, 9)])
        e1, e2 = PI * (d1 / 2) ** 2 / p1, PI * (d2 / 2) ** 2 / p2
        best = "die große Pizza" if e2 > e1 else "die kleine Pizza"
        return mcq("Eine Pizza mit %d cm Durchmesser kostet %d €, eine mit %d cm kostet %d €. Bei welcher bekommt man mehr Pizza pro Euro?" % (d1, p1, d2, p2), best,
                   ["die kleine Pizza" if best == "die große Pizza" else "die große Pizza", "Beide gleich viel.", "Das kann man ohne Gewicht nicht sagen."],
                   "Klein: %s cm² %s %d ≈ %s cm² pro €. Groß: %s cm² %s %d ≈ %s cm² pro €. <b>%s</b>" % (z(PI * (d1 / 2) ** 2, 0), G, p1, z(e1, 0), z(PI * (d2 / 2) ** 2, 0), G, p2, z(e2, 0), best.capitalize()))
    if kind == "beet":
        r = R.choice([2, 3, 4, Fr(5, 2), Fr(3, 2)])
        return mcq("Ein rundes Beet hat den Radius %s m. Wie viele Meter Rasenkante braucht man ringsherum (auf eine Nachkommastelle)?" % dz(r), "%s m" % z(2 * PI * float(r)),
                   ["%s m" % z(PI * float(r) ** 2), "%s m" % z(PI * float(r)), "%s m" % z(4 * float(r))],
                   "Gesucht ist der Umfang: 2 %s π %s %s ≈ <b>%s m</b>." % (MAL, MAL, dz(r), z(2 * PI * float(r))))
    if kind == "uhr":
        l = R.choice([6, 8, 10, 12, 15])
        return mcq("Der Minutenzeiger einer Uhr ist %d cm lang. Welchen Weg legt seine Spitze in einer Stunde zurück (auf eine Nachkommastelle)?" % l, "%s cm" % z(2 * PI * l),
                   ["%s cm" % z(PI * l * l), "%s cm" % z(PI * l), "%s cm" % z(2 * PI * l / 12)],
                   "Eine volle Runde: u = 2 %s π %s %d ≈ <b>%s cm</b>." % (MAL, MAL, l, z(2 * PI * l)))
    if kind == "tisch":
        d = R.choice([80, 90, 100, 120, 140])
        return mcq("Ein runder Tisch hat %d cm Durchmesser. Wie groß ist die Tischplatte (in m², auf zwei Nachkommastellen)?" % d, "%s m²" % z(PI * (d / 200) ** 2, 2),
                   ["%s m²" % z(PI * (d / 100) ** 2, 2), "%s m²" % z(PI * d / 100, 2), "%s m²" % z(PI * (d / 200), 2)],
                   "r = %s m. A = π %s %s² ≈ <b>%s m²</b>." % (dz(Fr(d, 200)), MAL, dz(Fr(d, 200)), z(PI * (d / 200) ** 2, 2)))
    r = R.choice([20, 25, 30, 36, 40])
    n = R.choice([3, 4, 5])
    return mcq("Eine Laufbahn ist kreisförmig mit r = %d m. Lena läuft %d Runden. Wie weit läuft sie (auf ganze Meter)?" % (r, n), "etwa %d m" % int(2 * PI * r * n + 0.5),
               ["etwa %d m" % int(PI * r * n + 0.5), "etwa %d m" % int(PI * r * r * n + 0.5), "etwa %d m" % int(2 * PI * r + 0.5)],
               "Eine Runde: 2 %s π %s %d ≈ %s m. Mal %d: <b>%d m</b>." % (MAL, MAL, r, z(2 * PI * r), n, int(2 * PI * r * n + 0.5)))


def main():
    seen = set()
    sets = [
        ("Kreisumfang", mix(R, seen, [(umfang, 20)])),
        ("Kreisfläche", mix(R, seen, [(flaeche, 20)])),
        ("Radius und Durchmesser bestimmen", mix(R, seen, [(rueck, 20)])),
        ("Kreisteile und Kreisringe", mix(R, seen, [(teile, 20)])),
        ("Sachaufgaben", mix(R, seen, [(sache, 20)])),
    ]
    body = lesson(
        ["Die Kreiszahl <b>π</b> ≈ 3,14 gibt an, wie oft der Durchmesser in den Umfang passt.",
         "<b>Umfang</b>: u = 2 %s π %s r = π %s d. <b>Flächeninhalt</b>: A = π %s r² (immer mit dem Radius!)." % (MAL, MAL, MAL, MAL),
         "Kreisausschnitt mit dem Winkel α: A = π r² %s α %s 360°, Bogen b = 2πr %s α %s 360°." % (MAL, G, MAL, G),
         "Kreisring: A = π %s (R² − r²). Ergebnisse rundet man sinnvoll, z. B. auf eine Nachkommastelle." % MAL],
        [example("r = 5 cm", ["u = 2 %s π %s 5 ≈ 31,4 cm" % (MAL, MAL), "A = π %s 25 ≈ 78,5 cm²" % MAL], "u ≈ 31,4 cm, A ≈ 78,5 cm²"),
         example("d = 10 m, A = ?", ["r = 5 m", "π %s 5²" % MAL], "≈ 78,5 m²")],
        [["d = 10 cm: A = π %s 10²" % MAL, "Erst den Radius bilden: π %s 5²" % MAL],
         ["A = 2 %s π %s r" % (MAL, MAL), "Das ist der Umfang. Fläche: π %s r²" % MAL],
         ["Ring: π %s (R − r)²" % MAL, "π %s (R² − r²)" % MAL]])
    faq = [
        {"q": "Wie berechne ich den Umfang eines Kreises?", "a": "u = 2 · π · r oder u = π · d. Mit dem Durchmesser geht es ohne die 2."},
        {"q": "Wie berechne ich die Kreisfläche?", "a": "A = π · r². Ist der Durchmesser gegeben, zuerst halbieren."},
        {"q": "Wie finde ich den Radius aus der Fläche?", "a": "r² = A : π, danach die Wurzel ziehen."},
        {"q": "Was ist π?", "a": "Die Kreiszahl π ≈ 3,14159… ist irrational. Sie gibt das Verhältnis von Umfang zu Durchmesser an."},
    ]
    make_unit(R, "kreisumfang-und-kreisflaeche", "G",
              "Die Schülerinnen und Schüler berechnen Umfang und Flächeninhalt von Kreisen, Kreisteilen und Kreisringen, bestimmen Radius und Durchmesser aus gegebenen Größen und lösen Sachaufgaben (Zusammenfassung).",
              "Kreisumfang und Kreisfläche",
              "Kreisumfang und Kreisfläche Klasse 8 – π, Kreisring, Kreisausschnitt, Arbeitsblätter",
              "Kreisberechnung",
              "Kreisberechnung für Klasse 8: Umfang u = 2πr, Fläche A = πr², Radius bestimmen, Kreisausschnitt, Kreisring und Sachaufgaben. 100 Aufgaben mit Lösungen, kostenlos.",
              "u = 2πr, A = πr²",
              "Für die Fläche immer den Radius nehmen.",
              body, faq, sets, 12, grade="klasse-8")


if __name__ == "__main__":
    main()
