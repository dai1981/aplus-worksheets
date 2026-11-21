# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 6: Kreise und Kreisdiagramme（Leitidee Raum und Form, Sek I）
  python3 tools/gen_de_mathe_k6_kreise.py
Mittelpunkt, Radius, Durchmesser (d = 2 · r), Sehne, Kreisbogen und Kreisausschnitt, Lage von Punkten zum Kreis, Kreisausschnitte als Anteile und Winkel, Kreisdiagramme.
Fehler: Radius und Durchmesser verwechselt, Anteil nicht mit 360° multipliziert (1/4 = 25°), Prozent direkt als Grad genommen.
"""
import math
import random
from fractions import Fraction as Fr
from de_common import lesson, example, make_unit, mix, Kids, fr, MAL, table, wrap, line, text, INK, RED, BLUE, GREEN, FILL
from de_k6 import bh, dz, mcq

R = random.Random(49615)
KIDS = Kids(R)
G = ":"


def kreis_svg(r_cm, zeige):
    R0 = 70
    cx, cy = 100, 92
    s = ["<circle cx='%d' cy='%d' r='%d' fill='%s' stroke='%s' stroke-width='2.5'/>" % (cx, cy, R0, FILL, GREEN), "<circle cx='%d' cy='%d' r='3.5' fill='%s'/>" % (cx, cy, INK), text(cx - 8, cy - 6, "M", 13)]
    if zeige == "r":
        s.append(line(cx, cy, cx + R0, cy, RED, 2.5) + text(cx + R0 / 2, cy + 18, "%s cm" % dz(r_cm), 14, col=RED))
    else:
        s.append(line(cx - R0, cy, cx + R0, cy, RED, 2.5) + text(cx, cy + 18, "%s cm" % dz(2 * r_cm), 14, col=RED))
    return wrap(200, 184, "".join(s), "Kreis mit Mittelpunkt M")


def rd():
    r = Fr(R.randint(2, 40), R.choice([1, 2]))
    kind = R.choice(["r2d", "d2r", "bild_r", "bild_d"])
    if kind == "r2d":
        return mcq("Ein Kreis hat den Radius r = %s cm. Wie groß ist der Durchmesser d?" % dz(r), "%s cm" % dz(2 * r), ["%s cm" % dz(x) for x in (r / 2, r, r + 2)], "d = 2 %s r = 2 %s %s cm = <b>%s cm</b>." % (MAL, MAL, dz(r), dz(2 * r)))
    if kind == "d2r":
        return mcq("Ein Kreis hat den Durchmesser d = %s cm. Wie groß ist der Radius r?" % dz(2 * r), "%s cm" % dz(r), ["%s cm" % dz(x) for x in (4 * r, 2 * r, r + 1)], "r = d %s 2 = <b>%s cm</b>." % (G, dz(r)))
    if kind == "bild_r":
        return mcq(kreis_svg(r, "r") + "Wie groß ist der Durchmesser dieses Kreises?", "%s cm" % dz(2 * r), ["%s cm" % dz(x) for x in (r, r / 2, 3 * r)], "Die rote Strecke ist der Radius. d = 2 %s %s cm = <b>%s cm</b>." % (MAL, dz(r), dz(2 * r)))
    return mcq(kreis_svg(r, "d") + "Wie groß ist der Radius dieses Kreises?", "%s cm" % dz(r), ["%s cm" % dz(x) for x in (2 * r, 4 * r, r + 1)], "Die rote Strecke ist der Durchmesser. r = %s cm %s 2 = <b>%s cm</b>." % (dz(2 * r), G, dz(r)))


def begriffe():
    k = R.randrange(12)
    D = [
        ("Wie heißt eine Strecke vom Mittelpunkt zum Kreisrand?", "Radius", ["Durchmesser", "Sehne", "Tangente"], "Vom Mittelpunkt bis zum Rand: <b>Radius</b>."),
        ("Wie heißt eine Strecke durch den Mittelpunkt von Rand zu Rand?", "Durchmesser", ["Radius", "Kreisbogen", "Sektor"], "Durch den Mittelpunkt von Rand zu Rand: <b>Durchmesser</b>."),
        ("Wie heißt eine Strecke, die zwei Punkte auf dem Kreis verbindet (nicht unbedingt durch M)?", "Sehne", ["Radius", "Kreisbogen", "Mittelpunkt"], "Eine Verbindung zweier Kreispunkte ist eine <b>Sehne</b>."),
        ("Welche Sehne ist die längste in einem Kreis?", "der Durchmesser", ["jede Sehne ist gleich lang", "der Radius", "die kürzeste Sehne am Rand"], "Die längste Sehne geht durch den Mittelpunkt: <b>der Durchmesser</b>."),
        ("Wie heißt ein Stück des Kreisrandes?", "Kreisbogen", ["Sehne", "Radius", "Kreisring"], "Ein Teil der Kreislinie ist ein <b>Kreisbogen</b>."),
        ("Wie heißt die Fläche zwischen zwei Radien und dem Kreisbogen (wie ein Tortenstück)?", "Kreisausschnitt", ["Kreisring", "Sehne", "Kreisbogen"], "Das Tortenstück heißt <b>Kreisausschnitt</b> (Sektor)."),
        ("Welches Werkzeug benutzt man, um einen Kreis zu zeichnen?", "den Zirkel", ["das Geodreieck", "den Taschenrechner", "das Lineal allein"], "Mit dem <b>Zirkel</b>: Einstichspitze in M, Abstand = Radius."),
        ("Wie weit stellt man den Zirkel auf, um einen Kreis mit d = 8 cm zu zeichnen?", "4 cm", ["8 cm", "16 cm", "2 cm"], "Der Zirkel wird auf den Radius eingestellt: 8 cm %s 2 = <b>4 cm</b>." % G),
        ("Alle Punkte eines Kreises haben vom Mittelpunkt …", "denselben Abstand", ["verschiedene Abstände", "den Abstand 0", "den doppelten Abstand"], "Ein Kreis ist die Menge aller Punkte mit <b>demselben Abstand</b> (Radius) von M."),
        ("Ein Punkt P ist 3 cm vom Mittelpunkt entfernt. Der Radius ist 5 cm. Wo liegt P?", "innerhalb des Kreises", ["auf dem Kreis", "außerhalb des Kreises", "im Mittelpunkt"], "3 cm &lt; 5 cm: <b>innerhalb des Kreises</b>."),
        ("Ein Punkt P ist 7 cm vom Mittelpunkt entfernt. Der Radius ist 5 cm. Wo liegt P?", "außerhalb des Kreises", ["auf dem Kreis", "innerhalb des Kreises", "im Mittelpunkt"], "7 cm &gt; 5 cm: <b>außerhalb des Kreises</b>."),
        ("Wie viele Spiegelachsen hat ein Kreis?", "unendlich viele", ["1", "2", "4"], "Jede Gerade durch den Mittelpunkt ist eine Spiegelachse: <b>unendlich viele</b>."),
    ]
    q, a, w, e = D[k]
    return mcq(q, a, w, e)


def lage():
    r = R.randint(2, 9)
    d = r + R.choice([-2, -1, 0, 1, 2]) if r > 2 else r + R.choice([0, 1, 2])
    d = Fr(d) + Fr(R.choice([0, 0, 5]), 10)
    ans = "auf dem Kreis" if d == r else "innerhalb des Kreises" if d < r else "außerhalb des Kreises"
    kind = R.choice(["r", "d"])
    q = ("Ein Kreis hat den Radius %d cm. Ein Punkt ist %s cm vom Mittelpunkt entfernt. Wo liegt der Punkt?" % (r, dz(d))) if kind == "r" else ("Ein Kreis hat den Durchmesser %d cm. Ein Punkt ist %s cm vom Mittelpunkt entfernt. Wo liegt der Punkt?" % (2 * r, dz(d)))
    return mcq(q, ans, [x for x in ("auf dem Kreis", "innerhalb des Kreises", "außerhalb des Kreises") if x != ans] + ["im Mittelpunkt"],
               "%sVergleiche %s cm mit r = %d cm: <b>%s</b>." % ("" if kind == "r" else "r = %d cm %s 2 = %d cm. " % (2 * r, G, r), dz(d), r, ans))


def sektor():
    kind = R.choice(["anteil2grad", "grad2anteil", "prozent2grad"])
    if kind == "anteil2grad":
        z, n = R.choice([(1, 2), (1, 3), (2, 3), (1, 4), (3, 4), (1, 5), (2, 5), (1, 6), (5, 6), (1, 8), (3, 8), (1, 9), (1, 10), (3, 10), (1, 12), (5, 12)])
        g = 360 * z // n
        return mcq("Ein Kreisausschnitt ist %s des ganzen Kreises. Wie groß ist sein Mittelpunktswinkel?" % fr(z, n), "%d°" % g, ["%d°" % x for x in (100 * z // n if 100 * z % n == 0 else z * n * 10, 180 * z // n if 180 * z % n == 0 else g + 10, g + 30)],
                   "Ein ganzer Kreis hat 360°. %s von 360° = 360° %s %d %s %d = <b>%d°</b>." % (fr(z, n), G, n, MAL, z, g))
    if kind == "grad2anteil":
        g = R.choice([30, 40, 45, 60, 72, 90, 120, 135, 144, 150, 180, 240, 270])
        v = Fr(g, 360)
        return mcq("Ein Kreisausschnitt hat den Mittelpunktswinkel %d°. Welcher Anteil des Kreises ist das?" % g, bh(v), [bh(Fr(g, 100)) if g < 100 else bh(Fr(g, 180), True), bh(Fr(g, 180)) if g < 180 else bh(v / 2), fr(1, g // 10)],
                   "%s = <b>%s</b>." % (fr(g, 360), bh(v)))
    p = R.choice([5, 10, 15, 20, 25, 30, 40, 45, 50, 60, 75])
    g = Fr(360 * p, 100)
    if g.denominator != 1:
        return None
    return mcq("In einem Kreisdiagramm sind %d\u00a0%% darzustellen. Wie groß ist der Winkel?" % p, "%d°" % g, ["%d°" % x for x in (p, 3 * p, g + 18)],
               "%d\u00a0%% von 360° = %s %s 360° = <b>%d°</b>." % (p, fr(p, 100), MAL, g))


def diagramm_svg(parts):
    cx, cy, r = 110, 110, 90
    cols = ["#7fb3d5", "#f5b041", "#82e0aa", "#f1948a", "#c39bd3"]
    s = []
    a0 = -90
    for i, (lab, frac_) in enumerate(parts):
        a1 = a0 + 360 * float(frac_)
        x0, y0 = cx + r * math.cos(math.radians(a0)), cy + r * math.sin(math.radians(a0))
        x1, y1 = cx + r * math.cos(math.radians(a1)), cy + r * math.sin(math.radians(a1))
        s.append("<path d='M%d %d L%.1f %.1f A%d %d 0 %d 1 %.1f %.1f Z' fill='%s' stroke='#fff' stroke-width='2'/>" % (cx, cy, x0, y0, r, r, 1 if a1 - a0 > 180 else 0, x1, y1, cols[i]))
        am = math.radians((a0 + a1) / 2)
        s.append(text(cx + 0.6 * r * math.cos(am), cy + 0.6 * r * math.sin(am) + 5, lab, 14))
        a0 = a1
    return wrap(220, 220, "".join(s), "Kreisdiagramm", lg=True)


def kreisdiagramm():
    sets_ = [[Fr(1, 2), Fr(1, 4), Fr(1, 4)], [Fr(1, 2), Fr(1, 3), Fr(1, 6)], [Fr(1, 3), Fr(1, 3), Fr(1, 6), Fr(1, 6)], [Fr(1, 4), Fr(1, 4), Fr(1, 4), Fr(1, 8), Fr(1, 8)], [Fr(1, 2), Fr(1, 8), Fr(3, 8)], [Fr(5, 12), Fr(1, 4), Fr(1, 3)], [Fr(2, 5), Fr(3, 10), Fr(1, 5), Fr(1, 10)]]
    parts = list(R.choice(sets_))
    R.shuffle(parts)
    labs = "ABCDE"[:len(parts)]
    pic = diagramm_svg(list(zip(labs, parts)))
    kind = R.choice(["anteil", "anzahl", "grad"])
    i = R.randrange(len(parts))
    v = parts[i]
    if kind == "anteil":
        return mcq(pic + "Welcher Anteil gehört zu Feld %s?" % labs[i], bh(v), [bh(x) for x in set(parts) if x != v] + [bh(v / 2), bh(min(v * 2, Fr(9, 10)))], "Feld %s ist %d° groß: %s = <b>%s</b>." % (labs[i], 360 * v, fr(360 * v, 360), bh(v)))
    if kind == "grad":
        return mcq(pic + "Wie groß ist der Winkel von Feld %s?" % labs[i], "%d°" % (360 * v), ["%d°" % x for x in (100 * v if (100 * v).denominator == 1 else 360 * v + 15, 180 * v if (180 * v).denominator == 1 else 360 * v - 10, 360 * v + 30)],
                   "%s von 360° = <b>%d°</b>." % (bh(v), 360 * v))
    t = R.choice([24, 48, 72, 120, 240])
    if (t * v).denominator != 1:
        return None
    return mcq(pic + "Bei einer Umfrage antworteten %d Personen. Wie viele wählten %s?" % (t, labs[i]), str(t * v), [str(x) for x in (t - t * v, int(t * v) + len(parts), t // len(parts) if t // len(parts) != t * v else t * v * 2)],
               "%s von %d = <b>%d</b>." % (bh(v), t, t * v))


def main():
    seen = set()
    sets = [
        ("Radius und Durchmesser", mix(R, seen, [(rd, 20)])),
        ("Begriffe am Kreis", mix(R, seen, [(begriffe, 12), (lage, 8)])),
        ("Kreisausschnitte und Winkel", mix(R, seen, [(sektor, 20)])),
        ("Kreisdiagramme lesen", mix(R, seen, [(kreisdiagramm, 20)])),
        ("Gemischte Aufgaben", mix(R, seen, [(lage, 6), (rd, 7), (sektor, 7)])),
    ]
    body = lesson(
        ["Alle Punkte eines <b>Kreises</b> haben denselben Abstand vom <b>Mittelpunkt</b> M. Dieser Abstand ist der <b>Radius</b> r.",
         "Der <b>Durchmesser</b> d geht durch M von Rand zu Rand: d = 2 %s r." % MAL,
         "Ein <b>Kreisausschnitt</b> ist ein Tortenstück. Sein Winkel am Mittelpunkt zeigt den Anteil am Kreis: 90° = %s Kreis." % fr(1, 4),
         "Im <b>Kreisdiagramm</b> gehört zu jedem Anteil der Winkel: Anteil %s 360°." % MAL],
        [example("r = 3,5 cm", ["d = 2 %s 3,5 cm" % MAL], "d = 7 cm"),
         example("%s als Kreisausschnitt" % fr(3, 8), ["360° %s 8 = 45°" % G, "3 %s 45°" % MAL], "135°")],
        [["r = 6 cm, also d = 3 cm", "Der Durchmesser ist doppelt so lang: 12 cm"],
         ["%s des Kreises = 25°" % fr(1, 4), "%s von 360° = 90°" % fr(1, 4)],
         ["30\u00a0% im Kreisdiagramm = 30°", "30\u00a0% von 360° = 108°"]])
    faq = [
        {"q": "Was ist der Unterschied zwischen Radius und Durchmesser?", "a": "Der Radius geht vom Mittelpunkt zum Rand. Der Durchmesser geht durch den Mittelpunkt von Rand zu Rand und ist doppelt so lang."},
        {"q": "Wie zeichne ich einen Kreis mit dem Zirkel?", "a": "Zirkel auf den Radius einstellen, Spitze in den Mittelpunkt stechen und einmal herumdrehen."},
        {"q": "Wie berechnet man den Winkel im Kreisdiagramm?", "a": "Anteil mal 360°. Zum Beispiel 25 % = 1/4, 1/4 von 360° = 90°."},
        {"q": "Was ist eine Sehne?", "a": "Eine Strecke zwischen zwei Punkten auf dem Kreis. Die längste Sehne ist der Durchmesser."},
    ]
    make_unit(R, "kreise-und-kreisdiagramme", "R",
              "Die Schülerinnen und Schüler beschreiben Kreise mit Mittelpunkt, Radius und Durchmesser, benennen Kreisteile, bestimmen Mittelpunktswinkel von Kreisausschnitten und lesen Kreisdiagramme (Zusammenfassung).",
              "Kreise und Kreisdiagramme",
              "Kreise Klasse 6 – Radius, Durchmesser und Kreisdiagramme, Arbeitsblätter",
              "Kreise",
              "Kreise für Klasse 6: Radius und Durchmesser, Kreisteile, Kreisausschnitte und Winkel, Kreisdiagramme. 100 Aufgaben mit Lösungen, kostenlos.",
              "Durchmesser = 2 · Radius.",
              "Im Kreisdiagramm: Anteil · 360°.",
              body, faq, sets, 15, grade="klasse-6")


if __name__ == "__main__":
    main()
