# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 5: Achsen- und Punktsymmetrie（Leitidee Raum und Form, Sek I）
  python3 tools/gen_de_mathe_k5_achsen_und_punktsymmetrie.py
Achsensymmetrie erkennen und ergänzen, Spiegelachsen zählen, Punktsymmetrie (Drehung um 180°), Achsen- und Punktspiegelung im Koordinatensystem.
Teile der Achsensymmetrie aus gen_de_mathe_k3_achsensymmetrie.py (welche, ergaenzen) mit neuem Zufall.
Fehler: Punkt- und Achsensymmetrie verwechselt, beim Spiegeln nur verschoben, Abstand zum Zentrum nicht verdoppelt.
"""
import random
import gen_de_mathe_k3_achsensymmetrie as k3
from de_common import mcq, lesson, example, make_unit, mix, MAL, table

R = random.Random(49515)
k3.R = random.Random(49565)


def rot(cells):
    return {(k3.COLS - 1 - x, k3.ROWS - 1 - y) for x, y in cells}


def punkt_welche():
    hs = [k3.half() for _ in range(3)]
    if not all(hs):
        return None
    good = set(hs[0]) | rot(hs[0])
    if good == k3.mirror(good):
        return None
    axis = k3.mirror(hs[1])
    if axis == set(axis) | rot(axis):
        return None
    sh = k3.shifted(hs[2])
    br = set(good)
    x, y = R.choice([p for p in br if p[0] >= 3])
    br.discard((x, y))
    if br == br | rot(br):
        return None
    figs = [good, axis, sh, br]
    if len({frozenset(f) for f in figs}) < 4:
        return None
    R.shuffle(figs)
    k = figs.index(good)
    return mcq(k3.four(figs, axis=False) + "Welche Figur ist <b>punktsymmetrisch</b>? (Sie sieht nach einer halben Drehung um die Mitte gleich aus.)", "ABCD"[k],
               ["ABCD"[i] for i in range(4) if i != k], "Dreht man Figur %s um 180° um die Mitte, liegt jedes Kästchen wieder auf einem Kästchen. Richtig ist <b>%s</b>." % ("ABCD"[k], "ABCD"[k]))


PUNKT = list("HINOSXZ")
NICHT = list("ABCDEFGJKLMPRTUVWY")
FIG = [("ein Quadrat", "4", True), ("ein Rechteck, das kein Quadrat ist", "2", True), ("ein Kreis", "unendlich viele", True), ("ein Parallelogramm ohne rechte Winkel (keine Raute)", "keine", True),
       ("eine Raute, die kein Quadrat ist", "2", True), ("ein gleichseitiges Dreieck", "3", False), ("ein Drachenviereck (keine Raute)", "1", False), ("ein gleichschenkliges Trapez", "1", False),
       ("ein regelmäßiges Sechseck", "6", True), ("ein regelmäßiges Fünfeck", "5", False), ("ein gleichschenkliges Dreieck (nicht gleichseitig)", "1", False)]


def buchst():
    kind = R.choice(["ist", "ist", "nicht"])
    if kind == "ist":
        a = R.choice(PUNKT)
        w = R.sample(NICHT, 3)
        q = "Welcher Buchstabe ist punktsymmetrisch? %s" % ", ".join(sorted([a] + w))
        e = "Drehst du %s um 180°, sieht er gleich aus. Richtig: <b>%s</b>." % (a, a)
    else:
        a = R.choice(NICHT)
        w = R.sample(PUNKT, 3)
        q = "Welcher Buchstabe ist <b>nicht</b> punktsymmetrisch? %s" % ", ".join(sorted([a] + w))
        e = "%s sieht nach einer halben Drehung anders aus. Richtig: <b>%s</b>." % (a, a)
    return mcq(q, a, w, e)


def figuren():
    kind = R.choice(["achsen", "achsen", "punkt", "punkt_nicht"])
    if kind == "achsen":
        th, ans, _ = R.choice(FIG)
        near = [x for x in ["keine", "1", "2", "3", "4", "5", "6", "8", "unendlich viele"] if x != ans]
        R.shuffle(near)
        n2 = {"4": ["2", "8"], "2": ["4", "1"], "3": ["1", "6"], "unendlich viele": ["1", "4"], "1": ["2", "keine"], "6": ["3", "12"], "keine": ["2", "1"], "5": ["10", "1"]}[ans]
        return mcq("Wie viele Spiegelachsen hat %s?" % th, ans, n2 + near, "%s hat <b>%s</b> Spiegelachse%s." % (th[0].upper() + th[1:], ans, "" if ans == "1" else "n"))
    yes = [f for f in FIG if f[2]]
    no = [f for f in FIG if not f[2]]
    if kind == "punkt":
        a = R.choice(yes)[0]
        w = [f[0] for f in R.sample(no, 3)]
        return mcq("Welche Figur ist punktsymmetrisch: %s?" % " – ".join(sorted([a] + w)), a, w, "%s sieht nach einer Drehung um 180° um die Mitte gleich aus: <b>%s</b>." % (a[0].upper() + a[1:], a))
    a = R.choice(no)[0]
    w = [f[0] for f in R.sample(yes, 3)]
    return mcq("Welche Figur ist <b>nicht</b> punktsymmetrisch: %s?" % " – ".join(sorted([a] + w)), a, w, "Nach einer Drehung um 180° steht %s auf dem Kopf: <b>%s</b>." % (a, a))


def P(a, b):
    return "(%d|%d)" % (a, b)


def ok(*v):
    return all(0 <= x <= 12 for x in v)


def punktspiegel():
    a, b = R.randint(3, 8), R.randint(3, 8)
    x, y = R.randint(0, 11), R.randint(0, 11)
    xs, ys = 2 * a - x, 2 * b - y
    if not ok(xs, ys) or (x, y) == (a, b) or x == a or y == b:
        return None
    c = ["P'" + P(*t) for t in ((2 * a - x, y), (x, 2 * b - y), (a - x if a > x else x - a, b - y if b > y else y - b), (y, x), (xs + 1, ys)) if ok(*t)]
    return mcq("Der Punkt P%s wird am Punkt Z%s gespiegelt. Welche Koordinaten hat der Bildpunkt P'?" % (P(x, y), P(a, b)), "P'" + P(xs, ys), c,
               "Von P nach Z: x %s %d, y %s %d. Von Z aus noch einmal so weit: x = %d, y = %d. <b>P'%s</b>." % ("+" if a >= x else "−", abs(a - x), "+" if b >= y else "−", abs(b - y), xs, ys, P(xs, ys)))


def achsspiegel():
    kind = R.choice(["x", "y"])
    k = R.randint(3, 8)
    x, y = R.randint(0, 11), R.randint(0, 11)
    if kind == "x":
        xs, ys = 2 * k - x, y
        if not ok(xs) or x == k:
            return None
        ach = "an der Geraden x = %d (parallel zur y-Achse)" % k
        c = [P(xs, 2 * k - y) if ok(2 * k - y) else P(xs + 1, y), P(x, 2 * k - y) if ok(2 * k - y) else P(xs, y + 1), P(abs(k - x), y), P(xs - 1, y)]
        e = "Der Abstand zur Achse x = %d ist %d. Auf der anderen Seite: x = %d, y bleibt %d. <b>P'%s</b>." % (k, abs(x - k), xs, y, P(xs, ys))
    else:
        xs, ys = x, 2 * k - y
        if not ok(ys) or y == k:
            return None
        ach = "an der Geraden y = %d (parallel zur x-Achse)" % k
        c = [P(2 * k - x, ys) if ok(2 * k - x) else P(x + 1, ys), P(2 * k - x, y) if ok(2 * k - x) else P(x, ys + 1), P(x, abs(k - y)), P(x, ys - 1)]
        e = "Der Abstand zur Achse y = %d ist %d. Auf der anderen Seite: y = %d, x bleibt %d. <b>P'%s</b>." % (k, abs(y - k), ys, x, P(xs, ys))
    return mcq("Der Punkt P%s wird %s gespiegelt. Welche Koordinaten hat der Bildpunkt P'?" % (P(x, y), ach), "P'" + P(xs, ys), ["P'" + t for t in c if "-" not in t], e)


def wissen():
    k = R.choice(range(12))
    D = [
        ("Was bedeutet punktsymmetrisch?", "Die Figur sieht nach einer Drehung um 180° um einen Punkt gleich aus.", ["Die Figur hat eine Spiegelachse.", "Die Figur hat nur Punkte als Ecken.", "Die Figur ist rund."], "Punktsymmetrisch heißt: <b>gleich nach einer halben Drehung</b> um das Symmetriezentrum."),
        ("Wie heißt der Punkt, um den eine punktsymmetrische Figur gedreht wird?", "Symmetriezentrum", ["Spiegelachse", "Scheitelpunkt", "Ursprung"], "Der Drehpunkt heißt <b>Symmetriezentrum</b>."),
        ("P und P' liegen punktsymmetrisch zum Zentrum Z. Welche Aussage stimmt?", "Z liegt genau in der Mitte zwischen P und P'.", ["P' liegt immer rechts von P.", "P und P' haben dieselben Koordinaten.", "Z liegt auf einer Spiegelachse."], "Bei der Punktspiegelung ist <b>Z der Mittelpunkt</b> der Strecke PP'."),
        ("Ein Punkt P ist 4 cm vom Zentrum Z entfernt. Wie weit ist er von seinem Bildpunkt P' entfernt?", "8 cm", ["4 cm", "2 cm", "6 cm"], "Bis Z 4 cm, dann noch einmal 4 cm: <b>8 cm</b>."),
        ("Ein Punkt liegt 3 cm von der Spiegelachse entfernt. Wie weit ist er von seinem Spiegelpunkt entfernt?", "6 cm", ["3 cm", "1,5 cm", "9 cm"], "2 %s 3 cm = <b>6 cm</b>." % MAL),
        ("Wie steht die Verbindungsstrecke von P und seinem Spiegelpunkt P' zur Spiegelachse?", "senkrecht", ["parallel", "schräg", "Sie liegt auf der Achse."], "Die Strecke PP' steht <b>senkrecht</b> auf der Spiegelachse."),
        ("Bei einer Achsenspiegelung: Was passiert mit der Größe der Figur?", "Sie bleibt gleich.", ["Sie wird doppelt so groß.", "Sie wird halb so groß.", "Sie wird kleiner."], "Spiegeln ändert die Größe nicht: <b>Sie bleibt gleich</b>."),
        ("Welches Werkzeug hilft am besten beim Spiegeln an einer Achse?", "das Geodreieck", ["der Zirkel allein", "der Taschenrechner", "das Lineal ohne Skala"], "Mit dem <b>Geodreieck</b> zeichnet man die Senkrechte und misst die Abstände."),
        ("Eine Figur ist achsensymmetrisch mit zwei senkrecht aufeinander stehenden Achsen. Ist sie dann auch punktsymmetrisch?", "Ja, immer.", ["Nein, nie.", "Nur wenn sie rund ist.", "Nur wenn sie ein Dreieck ist."], "Zwei Spiegelungen an senkrechten Achsen ergeben eine Drehung um 180°: <b>Ja, immer</b>."),
        ("Welche Ziffer ist punktsymmetrisch?", "8", ["3", "7", "4"], "Die <b>8</b> sieht nach einer halben Drehung gleich aus."),
        ("Welche Spielkarte zeigt oft Punktsymmetrie?", "Bube, Dame und König (zwei Köpfe)", ["keine Karte", "nur das Ass", "nur die Joker"], "Bei <b>Bube, Dame und König</b> ist das Bild oben und unten gedreht gleich."),
        ("Welche Zahl sieht nach einer halben Drehung gleich aus?", "69", ["66", "68", "61"], "Dreht man <b>69</b> um 180°, steht wieder 69 da."),
    ]
    q, a, w, e = D[k]
    return mcq(q, a, w, e)


def main():
    seen = set()
    sets = [
        ("Achsensymmetrie erkennen", mix(R, seen, [(k3.welche, 14), (figuren, 6)])),
        ("Achsensymmetrische Figuren ergänzen", mix(R, seen, [(k3.ergaenzen, 20)])),
        ("Punktsymmetrie erkennen", mix(R, seen, [(punkt_welche, 10), (buchst, 6), (figuren, 4)])),
        ("Spiegeln im Koordinatensystem", mix(R, seen, [(achsspiegel, 10), (punktspiegel, 10)])),
        ("Gemischte Aufgaben", mix(R, seen, [(wissen, 12), (punktspiegel, 4), (figuren, 4)])),
    ]
    body = lesson(
        ["Eine Figur ist <b>achsensymmetrisch</b>, wenn man sie an einer Geraden (Spiegelachse) so falten kann, dass beide Hälften genau aufeinanderliegen.",
         "Beim <b>Spiegeln an einer Achse</b> hat jeder Bildpunkt denselben Abstand zur Achse wie der Punkt. Die Verbindung steht senkrecht auf der Achse.",
         "Eine Figur ist <b>punktsymmetrisch</b>, wenn sie nach einer halben Drehung (180°) um einen Punkt Z gleich aussieht. Z heißt Symmetriezentrum.",
         "Beim <b>Spiegeln an einem Punkt</b> Z liegt Z genau in der Mitte zwischen P und P'."],
        [example("P(2|3) an Z(5|4) spiegeln", ["Von P zu Z: x + 3, y + 1", "Von Z noch einmal: x = 8, y = 5"], "P'(8|5)"),
         example("P(1|6) an x = 4 spiegeln", ["Abstand zur Achse: 3", "Auf der anderen Seite: x = 7"], "P'(7|6)")],
        [["Beim Spiegeln nur verschoben", "Spiegelbild: gleicher Abstand auf der anderen Seite"],
         ["Punktsymmetrie mit Achsensymmetrie verwechselt", "Punktsymmetrie: Drehung um 180°"],
         ["P(2|3) an Z(5|4): P'(5|4)", "Z ist die Mitte, nicht der Bildpunkt: P'(8|5)"]],
        extra=table(["Figur", "Spiegelachsen", "punktsymmetrisch?"], [["Quadrat", "4", "ja"], ["Rechteck", "2", "ja"], ["Raute", "2", "ja"], ["Parallelogramm", "0", "ja"], ["gleichseitiges Dreieck", "3", "nein"], ["Drachenviereck", "1", "nein"]]))
    faq = [
        {"q": "Was ist der Unterschied zwischen Achsen- und Punktsymmetrie?", "a": "Achsensymmetrisch: Man kann die Figur an einer Linie falten. Punktsymmetrisch: Die Figur sieht nach einer Drehung um 180° gleich aus."},
        {"q": "Ist ein Parallelogramm achsensymmetrisch?", "a": "Ein allgemeines Parallelogramm hat keine Spiegelachse, ist aber punktsymmetrisch. Rechteck, Raute und Quadrat haben Spiegelachsen."},
        {"q": "Wie spiegelt man einen Punkt an einem Zentrum Z?", "a": "Man zeichnet die Strecke von P durch Z und verlängert sie über Z hinaus um dieselbe Länge. Der Endpunkt ist P'."},
        {"q": "Welche Buchstaben sind punktsymmetrisch?", "a": "Zum Beispiel H, I, N, O, S, X und Z."},
    ]
    make_unit(R, "achsen-und-punktsymmetrie", "R",
              "Die Schülerinnen und Schüler erkennen achsen- und punktsymmetrische Figuren, bestimmen Spiegelachsen und Symmetriezentren und spiegeln Figuren an Achsen und Punkten (Zusammenfassung).",
              "Achsensymmetrie und Punktsymmetrie",
              "Achsen- und Punktsymmetrie Klasse 5 – Arbeitsblätter mit Lösungen",
              "Achsen- & Punktsymmetrie",
              "Symmetrie für Klasse 5: achsensymmetrische und punktsymmetrische Figuren, Spiegelachsen, Spiegeln im Koordinatensystem. 100 Aufgaben mit Lösungen, kostenlos.",
              "Achse: falten. Punkt: halbe Drehung.",
              "Beim Spiegeln bleibt der Abstand gleich, nur die Seite wechselt.",
              body, faq, sets, 15, grade="klasse-5")


if __name__ == "__main__":
    main()
