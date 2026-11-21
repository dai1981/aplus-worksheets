# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 7: Winkelsummen in Dreiecken und Vielecken（Leitidee Raum und Form, Sek I）
  python3 tools/gen_de_mathe_k7_winkelsummen.py
Winkelsumme im Dreieck (180°), gleichschenklige und gleichseitige Dreiecke, Außenwinkel (Summe der beiden nicht anliegenden Innenwinkel), Winkelsumme im Viereck (360°) und n-Eck ((n − 2) · 180°), regelmäßige Vielecke.
Fehler: im n-Eck n · 180° gerechnet, Außenwinkel als 180° − Außenwinkel verwechselt, beim gleichschenkligen Dreieck den Winkel an der Spitze doppelt genommen.
"""
import random
from de_common import lesson, example, make_unit, mix, Kids, MAL, table
from de_k6 import dz
from fractions import Fraction as Fr
from de_k7 import mcq

R = random.Random(49711)
KIDS = Kids(R)
NAMEN = {5: "Fünfeck", 6: "Sechseck", 7: "Siebeneck", 8: "Achteck", 9: "Neuneck", 10: "Zehneck", 12: "Zwölfeck"}


def dreieck():
    kind = R.choice(["zwei", "gl_basis", "gl_spitze", "verh"])
    if kind == "zwei":
        a, b = R.randint(20, 100), R.randint(20, 100)
        c = 180 - a - b
        if c < 10:
            return None
        return mcq("Im Dreieck ABC ist α = %d° und β = %d°. Wie groß ist γ?" % (a, b), "%d°" % c, ["%d°" % x for x in (360 - a - b, a + b, c + 10)], "180° − %d° − %d° = <b>%d°</b>." % (a, b, c))
    if kind == "gl_basis":
        b = R.randint(25, 85)
        return mcq("In einem gleichschenkligen Dreieck ist jeder Basiswinkel %d°. Wie groß ist der Winkel an der Spitze?" % b, "%d°" % (180 - 2 * b), ["%d°" % x for x in (180 - b, b, 90 - b if b < 90 else b)],
                   "180° − 2 %s %d° = <b>%d°</b>." % (MAL, b, 180 - 2 * b))
    if kind == "gl_spitze":
        s = R.choice(range(20, 160, 2))
        return mcq("In einem gleichschenkligen Dreieck ist der Winkel an der Spitze %d°. Wie groß ist jeder Basiswinkel?" % s, "%d°" % ((180 - s) // 2), ["%d°" % x for x in (180 - s, s // 2, (360 - s) // 2)],
                   "(180° − %d°) : 2 = <b>%d°</b>." % (s, (180 - s) // 2))
    k = R.choice([(1, 2, 3), (1, 1, 2), (2, 3, 4), (1, 2, 6), (3, 4, 5), (1, 3, 5), (2, 3, 7)])
    s = sum(k)
    if 180 % s:
        return None
    u = 180 // s
    return mcq("Die Winkel eines Dreiecks stehen im Verhältnis %d : %d : %d. Wie groß ist der größte Winkel?" % k, "%d°" % (k[2] * u), ["%d°" % x for x in (k[2] * 60 // k[0] if k[2] * 60 % k[0] == 0 else k[2] * u + 10, u, 180 - k[2] * u)],
               "%d Teile = 180°, 1 Teil = %d°. Größter Winkel: %d %s %d° = <b>%d°</b>." % (s, u, k[2], MAL, u, k[2] * u))


def aussen():
    a, b = R.randint(25, 85), R.randint(25, 85)
    c = 180 - a - b
    if c < 15:
        return None
    kind = R.choice(["aussen", "innen"])
    if kind == "aussen":
        return mcq("Im Dreieck ist α = %d° und β = %d°. Wie groß ist der Außenwinkel bei C?" % (a, b), "%d°" % (a + b), ["%d°" % x for x in (c, 180 - a, 360 - a - b)],
                   "Der Außenwinkel ist der Nebenwinkel von γ = %d°: 180° − %d° = <b>%d°</b> (= α + β)." % (c, c, a + b))
    return mcq("Ein Außenwinkel eines Dreiecks ist %d°. Ein nicht anliegender Innenwinkel ist %d°. Wie groß ist der andere nicht anliegende Innenwinkel?" % (a + b, a), "%d°" % b, ["%d°" % x for x in (180 - a - b, 180 - a, a + b - 90 if a + b > 90 else b + 10)],
               "Außenwinkel = Summe der beiden nicht anliegenden Innenwinkel: %d° − %d° = <b>%d°</b>." % (a + b, a, b))


def viereck():
    kind = R.choice(["drei", "paral", "drachen", "trapez"])
    if kind == "drei":
        a, b, c = R.randint(60, 130), R.randint(60, 130), R.randint(60, 130)
        d = 360 - a - b - c
        if not 30 <= d <= 170:
            return None
        return mcq("In einem Viereck sind drei Winkel %d°, %d° und %d°. Wie groß ist der vierte Winkel?" % (a, b, c), "%d°" % d, ["%d°" % x for x in (180 - (a + b + c) % 180, d + 10, 540 - a - b - c)],
                   "Winkelsumme im Viereck: 360°. 360° − %d° = <b>%d°</b>." % (a + b + c, d))
    if kind == "paral":
        a = R.randint(40, 85)
        return mcq("In einem Parallelogramm ist ein Winkel %d°. Wie groß sind die anderen drei Winkel?" % a, "%d°, %d° und %d°" % (180 - a, a, 180 - a), ["%d°, %d° und %d°" % (a, a, a), "%d°, %d° und %d°" % (90 - a, a, 90 - a), "%d°, %d° und %d°" % (180 - a, 180 - a, 180 - a)],
                   "Gegenüberliegende Winkel sind gleich, benachbarte ergeben 180°: <b>%d°, %d° und %d°</b>." % (180 - a, a, 180 - a))
    if kind == "drachen":
        a, b = R.randint(50, 100), R.randint(60, 140)
        d = 360 - 2 * a - b
        if not 20 <= d <= 160:
            return None
        return mcq("Ein Drachenviereck hat zwei gleich große Winkel von je %d° und einen Winkel von %d°. Wie groß ist der vierte Winkel?" % (a, b), "%d°" % d, ["%d°" % x for x in (360 - a - b, 180 - a - b if 180 - a - b > 0 else d + 20, d + 10)],
                   "360° − 2 %s %d° − %d° = <b>%d°</b>." % (MAL, a, b, d))
    a = R.randint(50, 85)
    return mcq("In einem gleichschenkligen Trapez ist ein Winkel an der langen Grundseite %d°. Wie groß ist ein Winkel an der kurzen Grundseite?" % a, "%d°" % (180 - a), ["%d°" % x for x in (a, 90 + a, 360 - 3 * a if 360 - 3 * a > 0 else 2 * a)],
               "Winkel an einem Schenkel zwischen den parallelen Seiten ergeben 180°: <b>%d°</b>." % (180 - a))


def neck():
    n = R.choice(list(NAMEN))
    kind = R.choice(["summe", "regel", "aussen", "n"])
    s = (n - 2) * 180
    if kind == "summe":
        return mcq("Wie groß ist die Winkelsumme in einem %s?" % NAMEN[n], "%d°" % s, ["%d°" % x for x in (n * 180, (n - 1) * 180, n * 360 if n * 360 != s else s + 180)],
                   "(n − 2) %s 180° = (%d − 2) %s 180° = <b>%d°</b>. Man kann das %s in %d Dreiecke zerlegen." % (MAL, n, MAL, s, NAMEN[n], n - 2))
    if kind == "regel":
        w = Fr(s, n)
        return mcq("Wie groß ist jeder Innenwinkel eines regelmäßigen %ss?" % NAMEN[n], "%s°" % dz(w), ["%s°" % dz(x) for x in (Fr(360, n), Fr(180 * (n - 1), n), Fr(s, n - 2))],
                   "Winkelsumme %d° : %d = <b>%s°</b>." % (s, n, dz(w)))
    if kind == "aussen":
        return mcq("Wie groß ist jeder Außenwinkel eines regelmäßigen %ss?" % NAMEN[n], "%s°" % dz(Fr(360, n)), ["%s°" % dz(x) for x in (Fr(s, n), Fr(180, n), Fr(360, n - 2))],
                   "Die Außenwinkel eines Vielecks ergeben zusammen 360°: 360° : %d = <b>%s°</b>." % (n, dz(Fr(360, n))))
    return mcq("Ein Vieleck hat die Winkelsumme %d°. Wie viele Ecken hat es?" % s, str(n), [str(n - 2), str(s // 180), str(n + 1)],
               "(n − 2) %s 180° = %d°. n − 2 = %d, <b>n = %d</b>." % (MAL, s, n - 2, n))


def sache():
    k = R.randrange(7)
    if k == 0:
        a = R.randint(25, 70)
        return mcq("Eine Rampe bildet mit dem Boden einen Winkel von %d°. Die Stütze steht senkrecht auf dem Boden. Welchen Winkel bilden Rampe und Stütze oben?" % a, "%d°" % (90 - a), ["%d°" % x for x in (180 - a, a, 180 - 90 - a + 10)],
                   "Rechtwinkliges Dreieck: 180° − 90° − %d° = <b>%d°</b>." % (a, 90 - a))
    if k == 1:
        return mcq("Ein Fußball ist aus Fünf- und Sechsecken genäht. Wie groß ist jeder Innenwinkel eines regelmäßigen Sechsecks?", "120°", ["108°", "135°", "60°"], "720° : 6 = <b>120°</b>.")
    if k == 2:
        return mcq("Bienenwaben sind regelmäßige Sechsecke. Wie viele Waben treffen an einer Ecke zusammen?", "3", ["2", "4", "6"], "Jeder Innenwinkel ist 120°. 360° : 120° = <b>3</b>.")
    if k == 3:
        a = R.randint(30, 60)
        return mcq("Ein Dach ist ein gleichschenkliges Dreieck mit der Dachneigung %d°. Wie groß ist der Winkel am First?" % a, "%d°" % (180 - 2 * a), ["%d°" % x for x in (180 - a, 90 - a, 2 * a)], "180° − 2 %s %d° = <b>%d°</b>." % (MAL, a, 180 - 2 * a))
    if k == 4:
        return mcq("Ein Stoppschild ist ein regelmäßiges Achteck. Wie groß ist jeder Innenwinkel?", "135°", ["120°", "144°", "45°"], "(8 − 2) %s 180° = 1080°. 1080° : 8 = <b>135°</b>." % MAL)
    if k == 5:
        a = R.randint(35, 75)
        return mcq("Ein Geodreieck ist ein gleichschenkliges, rechtwinkliges Dreieck. Wie groß sind die beiden anderen Winkel?", "je 45°", ["je 60°", "30° und 60°", "je 90°"], "(180° − 90°) : 2 = <b>45°</b>.") if a == 35 else None
    a = R.randint(80, 130)
    b = R.randint(80, 130)
    c = R.randint(80, 130)
    d = R.randint(80, 130)
    e = 540 - a - b - c - d
    if not 70 <= e <= 160:
        return None
    return mcq("Ein Grundstück hat fünf Ecken. Vier Winkel sind %d°, %d°, %d° und %d°. Wie groß ist der fünfte Winkel?" % (a, b, c, d), "%d°" % e, ["%d°" % x for x in (360 - (a + b + c + d) % 360, 720 - a - b - c - d, e + 10)],
               "Winkelsumme im Fünfeck: 540°. 540° − %d° = <b>%d°</b>." % (a + b + c + d, e))


def main():
    seen = set()
    sets = [
        ("Winkelsumme im Dreieck", mix(R, seen, [(dreieck, 20)])),
        ("Außenwinkel", mix(R, seen, [(aussen, 20)])),
        ("Winkelsumme im Viereck", mix(R, seen, [(viereck, 20)])),
        ("Vielecke", mix(R, seen, [(neck, 20)])),
        ("Sachaufgaben", mix(R, seen, [(sache, 12), (dreieck, 4), (viereck, 4)])),
    ]
    body = lesson(
        ["Die Innenwinkel eines <b>Dreiecks</b> ergeben 180°, die eines <b>Vierecks</b> 360°.",
         "Ein n-Eck kann man in n − 2 Dreiecke zerlegen. Seine Winkelsumme ist <b>(n − 2) %s 180°</b>." % MAL,
         "Ein <b>Außenwinkel</b> des Dreiecks ist so groß wie die Summe der beiden nicht anliegenden Innenwinkel.",
         "Im gleichschenkligen Dreieck sind die Basiswinkel gleich, im gleichseitigen ist jeder Winkel 60°."],
        [example("Sechseck", ["(6 − 2) %s 180°" % MAL], "720°"),
         example("α = 50°, β = 70°: Außenwinkel bei C", ["50° + 70°"], "120°")],
        [["Winkelsumme im Sechseck: 6 %s 180°" % MAL, "(6 − 2) %s 180° = 720°" % MAL],
         ["Spitze 40°, Basiswinkel 140°", "(180° − 40°) : 2 = 70°"],
         ["Außenwinkel = 180° − (α + β)", "Außenwinkel = α + β"]])
    faq = [
        {"q": "Warum ist die Winkelsumme im Dreieck 180°?", "a": "Zeichnet man durch eine Ecke eine Parallele zur gegenüberliegenden Seite, liegen die drei Winkel als Wechselwinkel auf einer Geraden: zusammen 180°."},
        {"q": "Wie berechnet man die Winkelsumme in einem n-Eck?", "a": "(n − 2) · 180°, denn man kann das n-Eck in n − 2 Dreiecke zerlegen."},
        {"q": "Was ist ein Außenwinkel?", "a": "Der Nebenwinkel eines Innenwinkels. Im Dreieck ist er so groß wie die beiden anderen Innenwinkel zusammen."},
        {"q": "Wie groß ist ein Innenwinkel im regelmäßigen Sechseck?", "a": "720° : 6 = 120°."},
    ]
    make_unit(R, "winkelsummen-in-dreiecken-und-vielecken", "R",
              "Die Schülerinnen und Schüler nutzen die Winkelsummen in Dreiecken, Vierecken und Vielecken sowie Eigenschaften von Außenwinkeln und besonderen Dreiecken, um Winkel zu berechnen (Zusammenfassung).",
              "Winkelsummen in Dreiecken und Vielecken",
              "Winkelsumme im Dreieck und Vieleck Klasse 7 – Arbeitsblätter mit Lösungen",
              "Winkelsummen",
              "Winkelsummen für Klasse 7: Dreieck, Außenwinkel, Viereck, n-Eck und regelmäßige Vielecke. 100 Aufgaben mit Lösungen, kostenlos.",
              "Dreieck 180°, Viereck 360°, n-Eck (n − 2) · 180°.",
              "Außenwinkel = Summe der beiden nicht anliegenden Innenwinkel.",
              body, faq, sets, 11, grade="klasse-7")


if __name__ == "__main__":
    main()
