# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 7: Winkel an Geradenkreuzungen（Leitidee Raum und Form, Sek I）
  python3 tools/gen_de_mathe_k7_winkel_an_geradenkreuzungen.py
Nebenwinkel (180°), Scheitelwinkel (gleich groß), Stufenwinkel und Wechselwinkel an parallelen Geraden (gleich groß), Nachbarwinkel (180°), Winkel berechnen und Parallelität begründen.
Fehler: Nebenwinkel und Scheitelwinkel verwechselt, Stufenwinkel auch bei nicht parallelen Geraden gleich gesetzt, 90° statt 180° als Summe.
"""
import math
import random
from de_common import lesson, example, make_unit, mix, Kids, MAL, table, wrap, line, text, INK, RED, BLUE, GREEN
from de_k7 import mcq

R = random.Random(49710)
KIDS = Kids(R)
POS = ["oben rechts", "oben links", "unten links", "unten rechts"]
# Winkel an einem Schnittpunkt: Mitte der Richtung (in Grad, mathematisch) je Position


def wert(t, pos):
    return t if pos in (0, 2) else 180 - t


def svg(t, marks, parallel=True):
    """marks: [(punkt 0/1, pos, label, farbe)]"""
    W, H = 340, 230
    ys = [70, 160]
    xs = [170, 170 - 90 / math.tan(math.radians(t))]
    s = []
    for i, y in enumerate(ys):
        s.append(line(20, y, W - 20, y if parallel or i == 0 else y - 22, INK, 2.2))
    s.append(text(W - 14, ys[0] + 5, "g", 14, italic=True) + text(W - 14, ys[1] + 5 - (0 if parallel else 22), "h", 14, italic=True))
    dx, dy = math.cos(math.radians(t)), -math.sin(math.radians(t))
    cx, cy = (xs[0] + xs[1]) / 2, (ys[0] + ys[1]) / 2
    L = 150
    s.append(line(cx - dx * L, cy - dy * L, cx + dx * L, cy + dy * L, BLUE, 2.2))
    for p, pos, lab, col in marks:
        px, py = xs[p], ys[p]
        a0, a1 = [(0, t), (t, 180), (180, 180 + t), (180 + t, 360)][pos]
        r = 22
        x0, y0 = px + r * math.cos(math.radians(a0)), py - r * math.sin(math.radians(a0))
        x1, y1 = px + r * math.cos(math.radians(a1)), py - r * math.sin(math.radians(a1))
        s.append("<path d='M%.1f %.1f L%.1f %.1f A%d %d 0 0 0 %.1f %.1f Z' fill='%s' fill-opacity='0.25' stroke='%s' stroke-width='1.5'/>" % (px, py, x0, y0, r, r, x1, y1, col, col))
        am = math.radians((a0 + a1) / 2)
        s.append(text(px + 38 * math.cos(am), py - 38 * math.sin(am) + 5, lab, 14, col=col))
    return wrap(W, H, "".join(s), "Zwei Geraden g und h, geschnitten von einer dritten Geraden", lg=True)


def art(p1, q1, p2, q2):
    if p1 == p2:
        return "Scheitelwinkel" if (q1 + 2) % 4 == q2 else "Nebenwinkel"
    if q1 == q2:
        return "Stufenwinkel"
    if (q1 + 2) % 4 == q2:
        return "Wechselwinkel"
    return "Nachbarwinkel" if {q1, q2} in ({0, 3}, {1, 2}) and ((p1 == 0 and q1 in (2, 3)) or (p2 == 0 and q2 in (2, 3))) else None


def berechnen():
    t = R.choice([35, 40, 48, 52, 55, 58, 62, 65, 70, 72, 75, 110, 115, 120, 125, 130])
    while True:
        p1, q1, p2, q2 = R.randint(0, 1), R.randint(0, 3), R.randint(0, 1), R.randint(0, 3)
        if (p1, q1) != (p2, q2) and art(p1, q1, p2, q2):
            break
    a = wert(t, q1)
    b = wert(t, q2)
    k = art(p1, q1, p2, q2)
    pic = svg(t, [(p1, q1, "%d°" % a, RED), (p2, q2, "β", GREEN)])
    regel = {"Scheitelwinkel": "Scheitelwinkel sind gleich groß", "Nebenwinkel": "Nebenwinkel ergeben 180°", "Stufenwinkel": "Stufenwinkel an parallelen Geraden sind gleich groß",
             "Wechselwinkel": "Wechselwinkel an parallelen Geraden sind gleich groß", "Nachbarwinkel": "Nachbarwinkel an parallelen Geraden ergeben 180°"}[k]
    return mcq(pic + "Die Geraden g und h sind parallel. Wie groß ist β?", "%d°" % b, ["%d°" % x for x in (180 - b, 90 - b if b < 90 else b - 90, 360 - b)],
               "%s. <b>β = %d°</b>." % (regel, b))


def benennen():
    t = R.choice([50, 60, 65, 70, 115, 120])
    while True:
        p1, q1, p2, q2 = R.randint(0, 1), R.randint(0, 3), R.randint(0, 1), R.randint(0, 3)
        if (p1, q1) != (p2, q2) and art(p1, q1, p2, q2):
            break
    k = art(p1, q1, p2, q2)
    pic = svg(t, [(p1, q1, "α", RED), (p2, q2, "β", GREEN)])
    return mcq(pic + "Wie nennt man die Winkel α und β?", k, [x for x in ("Scheitelwinkel", "Nebenwinkel", "Stufenwinkel", "Wechselwinkel", "Nachbarwinkel") if x != k],
               {"Scheitelwinkel": "Sie liegen sich am selben Schnittpunkt gegenüber: <b>Scheitelwinkel</b>.", "Nebenwinkel": "Sie liegen am selben Schnittpunkt nebeneinander und bilden zusammen einen gestreckten Winkel: <b>Nebenwinkel</b>.",
                "Stufenwinkel": "Sie liegen an verschiedenen Schnittpunkten an der gleichen Stelle (F-Figur): <b>Stufenwinkel</b>.", "Wechselwinkel": "Sie liegen an verschiedenen Schnittpunkten auf verschiedenen Seiten (Z-Figur): <b>Wechselwinkel</b>.",
                "Nachbarwinkel": "Sie liegen zwischen den Geraden auf derselben Seite der Querlinie (E-Figur): <b>Nachbarwinkel</b>."}[k])


def text_aufgabe():
    a = R.choice([28, 34, 42, 47, 53, 66, 71, 78, 84, 103, 117, 128, 136, 145, 152])
    k = R.choice(["Neben", "Scheitel", "Stufen", "Wechsel", "Nachbar"])
    v = a if k in ("Scheitel", "Stufen", "Wechsel") else 180 - a
    zus = "" if k in ("Neben", "Scheitel") else " (an zwei parallelen Geraden)"
    return mcq("Ein Winkel ist %d° groß. Wie groß ist sein %swinkel%s?" % (a, k, zus), "%d°" % v, ["%d°" % x for x in (180 - v, 90 - a if a < 90 else a - 90, 360 - a)],
               "%swinkel%s %s: <b>%d°</b>." % (k, zus, "sind gleich groß" if v == a else "ergeben zusammen 180°", v))


def parallel():
    t = R.choice([55, 60, 65, 70])
    d = R.choice([-8, -5, 0, 0, 5, 8])
    a, b = t, t + d
    ok = d == 0
    ans = "Ja, denn die Stufenwinkel sind gleich groß." if ok else "Nein, denn die Stufenwinkel sind verschieden groß."
    return mcq("Eine Gerade schneidet zwei andere Geraden g und h. An g ist der Stufenwinkel %d°, an h %d°. Sind g und h parallel?" % (a, b), ans,
               ["Nein, denn die Stufenwinkel sind verschieden groß." if ok else "Ja, denn die Stufenwinkel sind gleich groß.", "Ja, das sind Geraden immer.", "Das kann man nie entscheiden."],
               "Nur wenn Stufenwinkel gleich groß sind, sind die Geraden parallel. <b>%s</b>" % ("Ja" if ok else "Nein"))


def kette():
    t = R.choice([38, 44, 57, 63, 68, 74, 109, 118, 123])
    kind = R.choice(["drei", "summe", "gleichung"])
    if kind == "drei":
        return mcq("An zwei parallelen Geraden ist ein Winkel %d°. Wie groß sind sein Nebenwinkel und dessen Stufenwinkel?" % t, "%d° und %d°" % (180 - t, 180 - t), ["%d° und %d°" % (180 - t, t), "%d° und %d°" % (t, t), "%d° und %d°" % (90 - t if t < 90 else t - 90, t)],
                   "Nebenwinkel: 180° − %d° = %d°. Sein Stufenwinkel ist gleich groß: <b>%d° und %d°</b>." % (t, 180 - t, 180 - t, 180 - t))
    if kind == "summe":
        return mcq("Wie groß ist die Summe aller vier Winkel an einem Schnittpunkt zweier Geraden?", "360°", ["180°", "90°", "270°"] , "Die vier Winkel ergeben einen Vollwinkel: <b>360°</b>.") if t == 38 else None
    x = R.choice([20, 25, 30, 35, 40])
    k = R.choice([2, 3, 4])
    if x + k * x != 180 and (180 - x) % k:
        return None
    if (180 - x) % k == 0 and x + k * x != 180:
        y = (180 - x) // k
        return mcq("Zwei Nebenwinkel sind %d° und %d · x. Wie groß ist x?" % (x, k), "%d°" % y, ["%d°" % v for v in (180 - x, (90 - x) // k if (90 - x) % k == 0 and x < 90 else y + 10, y * k)],
                   "%d° + %dx = 180°. %dx = %d°, <b>x = %d°</b>." % (x, k, k, 180 - x, y))
    return None


def main():
    seen = set()
    sets = [
        ("Winkel benennen", mix(R, seen, [(benennen, 20)])),
        ("Neben- und Scheitelwinkel", mix(R, seen, [(text_aufgabe, 20)])),
        ("Winkel an parallelen Geraden", mix(R, seen, [(berechnen, 20)])),
        ("Gemischte Aufgaben", mix(R, seen, [(berechnen, 12), (kette, 8)])),
        ("Parallel oder nicht?", mix(R, seen, [(parallel, 6), (benennen, 7), (text_aufgabe, 7)])),
    ]
    body = lesson(
        ["Schneiden sich zwei Geraden, entstehen vier Winkel. <b>Nebenwinkel</b> liegen nebeneinander und ergeben 180°. <b>Scheitelwinkel</b> liegen sich gegenüber und sind gleich groß.",
         "Wird ein Paar paralleler Geraden von einer dritten Geraden geschnitten, sind <b>Stufenwinkel</b> (F-Figur) und <b>Wechselwinkel</b> (Z-Figur) gleich groß.",
         "<b>Nachbarwinkel</b> (E-Figur) zwischen den parallelen Geraden ergeben zusammen 180°.",
         "Umgekehrt gilt: Sind Stufenwinkel gleich groß, sind die Geraden parallel."],
        [example("α = 65°: Nebenwinkel?", ["180° − 65°"], "115°"),
         example("α = 65° an g: Wechselwinkel an h (g ∥ h)?", ["Wechselwinkel sind gleich"], "65°")],
        [["Nebenwinkel sind gleich groß", "Nebenwinkel ergeben 180°, Scheitelwinkel sind gleich"],
         ["Stufenwinkel sind immer gleich", "Nur an parallelen Geraden"],
         ["Nebenwinkel ergeben 90°", "Sie bilden eine Gerade: 180°"]])
    faq = [
        {"q": "Was ist der Unterschied zwischen Neben- und Scheitelwinkel?", "a": "Nebenwinkel liegen nebeneinander und ergeben zusammen 180°. Scheitelwinkel liegen sich gegenüber und sind gleich groß."},
        {"q": "Was sind Stufenwinkel?", "a": "Winkel an zwei verschiedenen Schnittpunkten, die an der gleichen Stelle liegen (F-Figur). An parallelen Geraden sind sie gleich groß."},
        {"q": "Was sind Wechselwinkel?", "a": "Winkel an zwei Schnittpunkten auf verschiedenen Seiten der schneidenden Geraden (Z-Figur). An parallelen Geraden sind sie gleich groß."},
        {"q": "Wie kann ich zeigen, dass zwei Geraden parallel sind?", "a": "Man zeigt, dass zwei Stufenwinkel (oder Wechselwinkel) gleich groß sind."},
    ]
    make_unit(R, "winkel-an-geradenkreuzungen", "R",
              "Die Schülerinnen und Schüler nutzen Neben-, Scheitel-, Stufen- und Wechselwinkel an Geradenkreuzungen und parallelen Geraden, um Winkel zu berechnen und Parallelität zu begründen (Zusammenfassung).",
              "Winkel an Geradenkreuzungen",
              "Nebenwinkel, Scheitelwinkel, Stufenwinkel, Wechselwinkel Klasse 7 – Arbeitsblätter",
              "Winkel an Geraden",
              "Winkel an Geradenkreuzungen für Klasse 7: Neben-, Scheitel-, Stufen- und Wechselwinkel an parallelen Geraden. 100 Aufgaben mit Lösungen, kostenlos.",
              "Scheitel-, Stufen- und Wechselwinkel sind gleich groß.",
              "Neben- und Nachbarwinkel ergeben 180°.",
              body, faq, sets, 10, grade="klasse-7")


if __name__ == "__main__":
    main()
