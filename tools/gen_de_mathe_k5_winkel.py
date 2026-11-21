# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 5: Winkel（Leitidee Raum und Form, Sek I）
  python3 tools/gen_de_mathe_k5_winkel.py
Winkelarten (spitz, recht, stumpf, gestreckt, überstumpf, Vollwinkel), Scheitel und Schenkel, Winkel mit dem Geodreieck messen, Winkel schätzen, Drehungen und Uhrzeiger.
Fehler: an der falschen Skala abgelesen (180° − α), stumpf und überstumpf verwechselt, beim überstumpfen Winkel nicht von 360° abgezogen.
"""
import math
import random
from de_common import mcq, lesson, example, make_unit, mix, MAL, table, wrap, line, text, INK, RED, BLUE, GRAY

R = random.Random(49514)
ARTEN = ["spitzer Winkel", "rechter Winkel", "stumpfer Winkel", "gestreckter Winkel", "überstumpfer Winkel", "Vollwinkel"]


def art_of(a):
    if a < 90:
        return ARTEN[0]
    if a == 90:
        return ARTEN[1]
    if a < 180:
        return ARTEN[2]
    if a == 180:
        return ARTEN[3]
    if a < 360:
        return ARTEN[4]
    return ARTEN[5]


def pol(cx, cy, r, deg):
    t = math.radians(deg)
    return cx + r * math.cos(t), cy - r * math.sin(t)


def winkel_svg(a, rot=0, scale=False, lab=("A", "S", "B")):
    L = 120
    if scale:
        cx, cy, W, H = 150, 160, 300, 190
    s = []
    if scale:
        s.append("<path d='M%d %d A130 130 0 0 1 %d %d Z' fill='#eef5ff' stroke='%s' stroke-width='1.2'/>" % (cx - 130, cy, cx + 130, cy, GRAY))
        for d in range(0, 181, 5):
            r1 = 130 - (12 if d % 10 == 0 else 6)
            x1, y1 = pol(cx, cy, 130, d)
            x2, y2 = pol(cx, cy, r1, d)
            s.append(line(x1, y1, x2, y2, GRAY, 1))
            if d % 20 == 0:
                x3, y3 = pol(cx, cy, 104, d)
                s.append(text(x3, y3 + 4, str(d), 11, col=INK, weight=600))
                x4, y4 = pol(cx, cy, 84, d)
                s.append(text(x4, y4 + 4, str(180 - d), 9, col="#9ab", weight=400))
    else:
        # Rahmen aus allen wichtigen Punkten berechnen
        pts = [(0, 0), pol(0, 0, L + 22, rot), pol(0, 0, L + 22, rot + a), (0, 30), (-16, 22)]
        pts += [pol(0, 0, 34, rot + a * k / 12.0) for k in range(13)]
        mx, Mx = min(p[0] for p in pts) - 20, max(p[0] for p in pts) + 20
        my, My = min(p[1] for p in pts) - 16, max(p[1] for p in pts) + 16
        cx, cy, W, H = -mx, -my, Mx - mx, My - my
    p1 = pol(cx, cy, L, rot)
    p2 = pol(cx, cy, L, rot + a)
    large = 1 if a > 180 else 0
    r = 30
    q1 = pol(cx, cy, r, rot)
    q2 = pol(cx, cy, r, rot + a)
    if a == 90:
        c1 = pol(cx, cy, 18, rot)
        c3 = pol(cx, cy, 18, rot + 90)
        c2 = (c1[0] + c3[0] - cx, c1[1] + c3[1] - cy)
        s.append("<path d='M%.1f %.1f L%.1f %.1f L%.1f %.1f' fill='none' stroke='%s' stroke-width='2'/>" % (c1 + c2 + c3 + (RED,)))
        m1 = pol(cx, cy, 9, rot + 45)
        s.append("<circle cx='%.1f' cy='%.1f' r='2.5' fill='%s'/>" % (m1[0], m1[1], RED))
    elif a < 360:
        s.append("<path d='M%.1f %.1f L%.1f %.1f A%d %d 0 %d 0 %.1f %.1f Z' fill='#fde3e0' stroke='%s' stroke-width='2'/>" % ((cx, cy) + q1 + (r, r, large) + q2 + (RED,)))
    s.append(line(cx, cy, p1[0], p1[1], INK, 3) + line(cx, cy, p2[0], p2[1], INK, 3))
    s.append("<circle cx='%.1f' cy='%.1f' r='4' fill='%s'/>" % (cx, cy, INK))
    sp = pol(cx, cy, 20, rot + a / 2.0 + 180) if a < 300 else (cx - 14, cy + 18)
    s.append(text(sp[0], sp[1] + 6, lab[1], 17))
    e1 = pol(cx, cy, L + 14, rot)
    e2 = pol(cx, cy, L + 14, rot + a)
    s.append(text(e1[0], e1[1] + 6, lab[0], 17) + text(e2[0], e2[1] + 6, lab[2], 17))
    return wrap(W, H, "".join(s), "Winkel mit Scheitel %s" % lab[1], lg=scale)


def arten():
    a = R.choice(list(range(15, 90, 5)) + [90, 90, 90] + list(range(95, 180, 5)) + [180, 180] + list(range(190, 360, 10)))
    rot = R.choice([0, 0, 10, 20, 30, 200 if a < 150 else 0])
    q = winkel_svg(a, rot) + "Welche Winkelart ist der markierte Winkel?"
    ans = art_of(a)
    near = {ARTEN[0]: [ARTEN[2], ARTEN[1], ARTEN[4]], ARTEN[1]: [ARTEN[0], ARTEN[2], ARTEN[3]], ARTEN[2]: [ARTEN[4], ARTEN[0], ARTEN[3]],
            ARTEN[3]: [ARTEN[2], ARTEN[5], ARTEN[1]], ARTEN[4]: [ARTEN[2], ARTEN[5], ARTEN[3]]}[ans]
    rng = {ARTEN[0]: "kleiner als 90°", ARTEN[1]: "genau 90°", ARTEN[2]: "zwischen 90° und 180°", ARTEN[3]: "genau 180°", ARTEN[4]: "zwischen 180° und 360°"}[ans]
    return mcq(q, ans, near, "Der Winkel ist %s: <b>%s</b>." % (rng, ans))


def zahl_art():
    a = R.choice([x for x in range(5, 361, 5)])
    ans = art_of(a)
    o = [x for x in ARTEN if x != ans]
    R.shuffle(o)
    return mcq("Welche Winkelart hat ein Winkel von %d°?" % a, ans, o, "%d° ist %s: <b>%s</b>." % (a, {ARTEN[0]: "kleiner als 90°", ARTEN[1]: "genau 90°", ARTEN[2]: "zwischen 90° und 180°", ARTEN[3]: "genau 180°", ARTEN[4]: "zwischen 180° und 360°", ARTEN[5]: "genau 360°"}[ans], ans))


def messen():
    a = R.choice([x for x in range(20, 171, 5) if x != 90])
    q = winkel_svg(a, 0, scale=True) + "Lies den Winkel ∠ASB am Geodreieck ab."
    return mcq(q, "%d°" % a, ["%d°" % (180 - a), "%d°" % (a + 10), "%d°" % (a - 5)], "Der Schenkel SA liegt auf 0°. Lies auf derselben (äußeren) Skala ab: <b>%d°</b>. Nicht %d° von der inneren Skala." % (a, 180 - a))


def schaetzen():
    a = R.choice(range(20, 341, 10))
    if a in (90, 180):
        return None
    rot = R.choice([0, 15, 30])
    q = winkel_svg(a, rot) + "Schätze: Wie groß ist der markierte Winkel ungefähr?"
    c = ["%d°" % x for x in (a, (a + 60) % 360 or 60, abs(a - 60) or 120, 360 - a if 360 - a != a else a + 90)]
    return mcq(q, c[0], c[1:], "Vergleiche mit 90° (rechter Winkel) und 180° (gestreckter Winkel): ungefähr <b>%d°</b>." % a)


def ueber():
    a = R.choice(range(190, 351, 5))
    i = 360 - a
    kind = R.choice(["messen", "rechnen"])
    if kind == "messen":
        return mcq("Ein überstumpfer Winkel soll gemessen werden. Der Innenwinkel daneben ist %d° groß. Wie groß ist der überstumpfe Winkel?" % i, "%d°" % a, ["%d°" % x for x in (180 - i if i < 180 else a - 90, i + 180, i)],
                   "Beide Winkel ergeben zusammen 360°. 360° − %d° = <b>%d°</b>." % (i, a))
    return mcq("Ein Winkel ist %d° groß. Wie groß ist der Winkel, der ihn zum Vollwinkel ergänzt?" % a, "%d°" % i, ["%d°" % x for x in (180 - i if 180 - i > 0 else i + 90, a - 180, i + 10)],
               "360° − %d° = <b>%d°</b>." % (a, i))


def uhr():
    kind = R.choice(["zeit", "zeit", "dreh", "himmel"])
    if kind == "zeit":
        h = R.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
        a = 30 * h if h <= 6 else 30 * (12 - h)
        return mcq("Wie groß ist der kleinere Winkel zwischen den Uhrzeigern um %d:00 Uhr?" % h, "%d°" % a, ["%d°" % x for x in (h * 10 if h * 10 != a else a + 30, 360 - a, a + 30 if a + 30 <= 180 else a - 30)],
                   "Zwischen zwei Zahlen der Uhr liegen 360° : 12 = 30°. %d %s 30° = <b>%d°</b>." % (a // 30, MAL, a))
    if kind == "dreh":
        m = R.choice([5, 10, 15, 20, 25, 30, 40, 45, 50])
        a = 6 * m
        return mcq("Um wie viel Grad dreht sich der Minutenzeiger in %d Minuten?" % m, "%d°" % a, ["%d°" % x for x in (m, 30 * m if 30 * m != a else a + 30, a + 30)], "In 60 min sind es 360°, also 6° pro Minute. %d %s 6° = <b>%d°</b>." % (m, MAL, a))
    t = R.choice([("Viertel", 90), ("halbe", 180), ("Dreiviertel", 270), ("ganze", 360)])
    wort = {"Viertel": "Vierteldrehung", "halbe": "halbe Drehung", "Dreiviertel": "Dreivierteldrehung", "ganze": "ganze Drehung"}[t[0]]
    name, pr = R.choice([("Emma", "sie"), ("Ben", "er"), ("Ein Karussell", "es"), ("Ein Tänzer", "er")])
    return mcq("%s macht eine %s. Um wie viel Grad dreht %s sich?" % (name, wort, pr), "%d°" % t[1],
               ["%d°" % x for x in (90, 180, 270, 360, 45) if x != t[1]], "Eine ganze Drehung sind 360°. %s<b>%d°</b>." % ({"Viertel": "360° : 4 = ", "halbe": "360° : 2 = ", "Dreiviertel": "3 %s 90° = " % MAL, "ganze": ""}[t[0]], t[1]))


def begriffe():
    k = R.choice(range(10))
    D = [
        ("Wie heißt der Punkt, an dem die beiden Schenkel eines Winkels beginnen?", "Scheitelpunkt", ["Schenkelpunkt", "Mittelpunkt", "Endpunkt"], "Die Schenkel beginnen im <b>Scheitelpunkt</b>."),
        ("Was sind die Schenkel eines Winkels?", "zwei Strahlen mit gemeinsamem Anfangspunkt", ["zwei Strecken, die parallel sind", "zwei Geraden ohne Schnittpunkt", "die Zahlen am Geodreieck"], "Ein Winkel besteht aus <b>zwei Strahlen</b> mit gemeinsamem Anfangspunkt."),
        ("Mit welchem Buchstaben bezeichnet man Winkel oft?", "mit griechischen Buchstaben wie α, β, γ", ["mit großen Buchstaben wie A, B, C", "mit Zahlen", "mit kleinen Buchstaben wie g und h"], "Winkel bezeichnet man mit <b>α (alpha), β (beta), γ (gamma)</b>."),
        ("Im Winkel ∠ASB ist welcher Punkt der Scheitelpunkt?", "S", ["A", "B", "keiner"], "Der Scheitel steht in der Mitte: <b>S</b>."),
        ("Wie groß ist ein Vollwinkel?", "360°", ["180°", "90°", "100°"], "Eine ganze Drehung: <b>360°</b>."),
        ("Wie groß ist ein gestreckter Winkel?", "180°", ["90°", "360°", "120°"], "Die Schenkel bilden eine Gerade: <b>180°</b>."),
        ("Zwischen welchen Werten liegt ein stumpfer Winkel?", "zwischen 90° und 180°", ["zwischen 0° und 90°", "zwischen 180° und 360°", "genau bei 90°"], "Stumpf: <b>größer als 90° und kleiner als 180°</b>."),
        ("Zwischen welchen Werten liegt ein überstumpfer Winkel?", "zwischen 180° und 360°", ["zwischen 90° und 180°", "zwischen 0° und 90°", "über 360°"], "Überstumpf: <b>größer als 180° und kleiner als 360°</b>."),
        ("Wie viele rechte Winkel ergeben zusammen einen Vollwinkel?", "4", ["2", "3", "6"], "4 %s 90° = <b>360°</b>." % MAL),
        ("Wie viele rechte Winkel hat ein Rechteck?", "4", ["2", "0", "1"], "Ein Rechteck hat <b>4</b> rechte Winkel."),
    ]
    q, a, w, e = D[k]
    return mcq(q, a, w, e)


def sache():
    k = R.choice(range(10))
    D = [
        ("Ein Riesenrad hat 12 Gondeln in gleichem Abstand. Wie groß ist der Winkel zwischen zwei benachbarten Gondeln (vom Mittelpunkt aus)?", "30°", ["12°", "36°", "60°"], "360° : 12 = <b>30°</b>."),
        ("Eine Pizza wird in 8 gleiche Stücke geschnitten. Wie groß ist der Winkel eines Stücks an der Spitze?", "45°", ["8°", "40°", "90°"], "360° : 8 = <b>45°</b>."),
        ("Eine Torte wird in 6 gleiche Stücke geschnitten. Wie groß ist der Winkel eines Stücks an der Spitze?", "60°", ["6°", "30°", "36°"], "360° : 6 = <b>60°</b>."),
        ("Ein Kreisel dreht sich 3-mal ganz herum. Um wie viel Grad hat er sich gedreht?", "1080°", ["360°", "540°", "300°"], "3 %s 360° = <b>1080°</b>." % MAL),
        ("Eine Tür wird so weit geöffnet, dass sie senkrecht zur Wand steht. Wie groß ist der Öffnungswinkel?", "90°", ["180°", "45°", "360°"], "Senkrecht bedeutet: <b>90°</b>."),
        ("Ein Laptop ist so weit aufgeklappt, dass Bildschirm und Tastatur eine gerade Linie bilden. Wie groß ist der Winkel?", "180°", ["90°", "360°", "120°"], "Eine gerade Linie: gestreckter Winkel, <b>180°</b>."),
        ("Leon steht nach Norden und dreht sich nach rechts, bis er nach Osten schaut. Um wie viel Grad hat er sich gedreht?", "90°", ["180°", "270°", "45°"], "Von Norden nach Osten ist eine Vierteldrehung: <b>90°</b>."),
        ("Mia schaut nach Norden und dreht sich nach rechts, bis sie nach Westen schaut. Um wie viel Grad hat sie sich gedreht?", "270°", ["90°", "180°", "360°"], "Norden → Osten → Süden → Westen: 3 %s 90° = <b>270°</b>." % MAL),
        ("Ein Glücksrad hat 10 gleich große Felder. Wie groß ist der Winkel eines Feldes am Mittelpunkt?", "36°", ["10°", "30°", "45°"], "360° : 10 = <b>36°</b>."),
        ("Eine Rampe ist um 15° geneigt. Eine zweite Rampe ist doppelt so steil geneigt. Welchen Winkel hat sie?", "30°", ["17°", "45°", "60°"], "2 %s 15° = <b>30°</b>." % MAL),
    ]
    q, a, w, e = D[k]
    return mcq(q, a, w, e)


def main():
    seen = set()
    sets = [
        ("Winkelarten erkennen", mix(R, seen, [(arten, 14), (zahl_art, 6)])),
        ("Winkel messen", mix(R, seen, [(messen, 20)])),
        ("Winkel schätzen und Begriffe", mix(R, seen, [(schaetzen, 10), (begriffe, 10)])),
        ("Überstumpfe Winkel, Uhr und Drehungen", mix(R, seen, [(ueber, 8), (uhr, 12)])),
        ("Sachaufgaben mit Winkeln", mix(R, seen, [(sache, 10), (zahl_art, 6), (ueber, 4)])),
    ]
    body = lesson(
        ["Ein <b>Winkel</b> besteht aus zwei <b>Schenkeln</b> (Strahlen), die im <b>Scheitelpunkt</b> beginnen. Man schreibt ∠ASB oder α.",
         "Winkel misst man in Grad (°). Eine ganze Drehung sind 360°.",
         "Winkelarten: spitz (unter 90°), recht (90°), stumpf (90° bis 180°), gestreckt (180°), überstumpf (180° bis 360°), Vollwinkel (360°).",
         "Messen mit dem Geodreieck: Nullpunkt auf den Scheitel, ein Schenkel auf 0°, dann <b>auf derselben Skala</b> ablesen.",
         "Einen überstumpfen Winkel misst man indirekt: kleinen Winkel messen und von 360° abziehen."],
        [example("Ein Winkel ist 130°", ["größer als 90°", "kleiner als 180°"], "stumpfer Winkel"),
         example("Der Innenwinkel ist 70°. Wie groß ist der überstumpfe Winkel?", ["360° − 70°"], "290°")],
        [["50° an der falschen Skala als 130° abgelesen", "Die Skala nehmen, auf der der erste Schenkel bei 0° liegt"],
         ["200° ist stumpf", "200° ist überstumpf (über 180°)"],
         ["Uhr: zwischen 12 und 3 liegen 3°", "Zwischen zwei Zahlen liegen 30°: 3 %s 30° = 90°" % MAL]],
        extra=table(["Winkelart", "Größe"], [["spitz", "unter 90°"], ["recht", "90°"], ["stumpf", "90° bis 180°"], ["gestreckt", "180°"], ["überstumpf", "180° bis 360°"], ["Vollwinkel", "360°"]]))
    faq = [
        {"q": "Wie misst man einen Winkel mit dem Geodreieck?", "a": "Lege den Nullpunkt auf den Scheitel und die Grundlinie auf einen Schenkel. Lies dort ab, wo der andere Schenkel die Skala schneidet – auf der Skala, die beim ersten Schenkel mit 0° beginnt."},
        {"q": "Welche Winkelarten gibt es?", "a": "Spitze, rechte, stumpfe, gestreckte und überstumpfe Winkel sowie den Vollwinkel."},
        {"q": "Wie misst man einen überstumpfen Winkel?", "a": "Man misst den kleinen Winkel daneben und rechnet 360° minus diesen Winkel."},
        {"q": "Was ist ein Scheitelpunkt?", "a": "Der Punkt, an dem die beiden Schenkel eines Winkels beginnen."},
    ]
    make_unit(R, "winkel", "R",
              "Die Schülerinnen und Schüler benennen Winkelarten, messen und schätzen Winkel mit dem Geodreieck, zeichnen Winkel und beschreiben Drehungen mit Winkelgrößen (Zusammenfassung).",
              "Winkel messen und Winkelarten",
              "Winkel Klasse 5 – Winkelarten und Winkel messen, Arbeitsblätter",
              "Winkel",
              "Winkel für Klasse 5: Winkelarten, Winkel mit dem Geodreieck messen, schätzen, überstumpfe Winkel und Drehungen. 100 Aufgaben mit Lösungen, kostenlos.",
              "Nullpunkt auf den Scheitel, auf derselben Skala ablesen.",
              "Spitz unter 90°, stumpf bis 180°, überstumpf bis 360°.",
              body, faq, sets, 14, grade="klasse-5")


if __name__ == "__main__":
    main()
