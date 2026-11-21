# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 5: Koordinatensystem（Leitidee Raum und Form, Sek I）
  python3 tools/gen_de_mathe_k5_koordinatensystem.py
Punkte im ersten Quadranten ablesen und eintragen (P(3|5)), x- und y-Achse, Punkte verschieben, fehlende Eckpunkte von Rechtecken und Quadraten, Abstände auf Gitterlinien.
Fehler: x- und y-Koordinate vertauscht, Kästchen statt Einheiten gezählt, beim Verschieben die Richtung verwechselt.
"""
import random
import re
from de_common import mcq as _mcq, lesson, example, make_unit, mix, MAL, table, wrap, line, text, INK, RED, BLUE, GRAY

R = random.Random(49513)
U = 26
N = 10
LETTERS = "ABCDEFGHKLMNPQRST"


def mcq(q, a, cands, e):
    ok = lambda c: not re.search(r"\((-|\d+\|-)|\b1[1-9]\b|\b[2-9]\d\b", c) if "(" in c else True
    return _mcq(q, a, [c for c in cands if ok(c)], e)


def plane(points=(), polys=(), n=N):
    x0, y0 = 30, 18
    W, H = x0 + n * U + 26, y0 + n * U + 34
    X = lambda v: x0 + v * U
    Y = lambda v: y0 + (n - v) * U
    s = ["<rect width='%d' height='%d' fill='#fff'/>" % (W, H)]
    for i in range(n + 1):
        s.append(line(X(i), Y(0), X(i), Y(n), "#d5dfec", 1))
        s.append(line(X(0), Y(i), X(n), Y(i), "#d5dfec", 1))
    s.append(line(X(0), Y(0), X(n) + 14, Y(0), INK, 2) + "<path d='M%d %d l-9 -5 v10 Z' fill='%s'/>" % (X(n) + 18, Y(0), INK))
    s.append(line(X(0), Y(0), X(0), Y(n) - 10, INK, 2) + "<path d='M%d %d l-5 9 h10 Z' fill='%s'/>" % (X(0), Y(n) - 14, INK))
    s.append(text(X(n) + 14, Y(0) + 20, "x", 14, italic=True) + text(X(0) - 16, Y(n) - 4, "y", 14, italic=True))
    for i in range(1, n + 1):
        s.append(text(X(i), Y(0) + 17, str(i), 12, weight=500) + text(X(0) - 10, Y(i) + 4, str(i), 12, weight=500))
    s.append(text(X(0) - 9, Y(0) + 15, "0", 12, weight=500))
    for poly in polys:
        s.append("<polygon points='%s' fill='#e3eefb' stroke='%s' stroke-width='2'/>" % (" ".join("%d,%d" % (X(a), Y(b)) for a, b in poly), BLUE))
    for (a, b), lab in points:
        s.append("<circle cx='%d' cy='%d' r='4.5' fill='%s'/>" % (X(a), Y(b), RED) + text(X(a) + 9, Y(b) - 7, lab, 14, col=RED))
    return wrap(W, H, "".join(s), "Koordinatensystem", lg=True)


def P(a, b):
    return "(%d|%d)" % (a, b)


def rnd_pt(lo=0, hi=N):
    return (R.randint(lo, hi), R.randint(lo, hi))


def ablesen():
    a, b = rnd_pt(1, 9)
    if a == b:
        return None
    lab = R.choice(LETTERS)
    q = plane([((a, b), lab)]) + "Welche Koordinaten hat der Punkt %s?" % lab
    return mcq(q, lab + P(a, b), [lab + P(b, a), lab + P(a + 1, b), lab + P(a, b - 1)], "Erst nach rechts (x = %d), dann nach oben (y = %d): <b>%s%s</b>." % (a, b, lab, P(a, b)))


def finden():
    pts = []
    while len(pts) < 4:
        p = rnd_pt(1, 9)
        if p not in pts and (p[1], p[0]) not in pts:
            pts.append(p)
    t = pts[0]
    if t[0] == t[1]:
        return None
    labs = R.sample(LETTERS, 4)
    sw = (t[1], t[0])
    pts2 = [t, sw] + pts[2:3]
    q = plane(list(zip(pts2, labs[:3]))) + "Welcher Punkt hat die Koordinaten %s?" % P(*t)
    return mcq(q, labs[0], [labs[1], labs[2], "keiner"], "x = %d nach rechts, y = %d nach oben: Punkt <b>%s</b>. (%s hat x und y vertauscht.)" % (t[0], t[1], labs[0], labs[1]))


def achse():
    kind = R.choice(["auf_x", "auf_y", "ursprung", "welche"])
    if kind == "auf_x":
        a = R.randint(1, 9)
        b = R.randint(1, 9)
        return mcq("Welcher Punkt liegt auf der x-Achse: %s, %s, %s oder %s?" % ("A" + P(a, 0), "B" + P(0, b), "C" + P(a, a), "D" + P(b, 1)), "A" + P(a, 0), ["B" + P(0, b), "C" + P(a, a), "D" + P(b, 1)],
                   "Auf der x-Achse ist die y-Koordinate 0: <b>A%s</b>." % P(a, 0))
    if kind == "auf_y":
        a = R.randint(1, 9)
        b = R.randint(2, 9)
        return mcq("Welcher Punkt liegt auf der y-Achse: %s, %s, %s oder %s?" % ("A" + P(b, 0), "B" + P(0, a), "C" + P(a, b), "D" + P(1, a)), "B" + P(0, a), ["A" + P(b, 0), "C" + P(a, b), "D" + P(1, a)],
                   "Auf der y-Achse ist die x-Koordinate 0: <b>B%s</b>." % P(0, a))
    if kind == "ursprung":
        return mcq("Welche Koordinaten hat der Ursprung des Koordinatensystems?", "(0|0)", ["(1|1)", "(0|1)", "(1|0)"], "Im Ursprung schneiden sich die Achsen: <b>(0|0)</b>.")
    a, b = rnd_pt(1, 9)
    if a == b:
        return None
    return mcq("Der Punkt P%s ist gegeben. Was gibt die erste Zahl an?" % P(a, b), "wie weit man nach rechts geht (x)", ["wie weit man nach oben geht (y)", "die Nummer des Punktes", "den Abstand zum Ursprung"],
               "Die erste Koordinate ist der x-Wert: <b>%d nach rechts</b>, dann %d nach oben." % (a, b))


def verschieben():
    a, b = rnd_pt(1, 7)
    dx, dy = R.choice([1, 2, 3, 4, -1, -2]), R.choice([1, 2, 3, -1, -2])
    if not (0 <= a + dx <= 10 and 0 <= b + dy <= 10):
        return None
    def dirs(dx, dy):
        h = "%d nach %s" % (abs(dx), "rechts" if dx > 0 else "links")
        v = "%d nach %s" % (abs(dy), "oben" if dy > 0 else "unten")
        return h + " und " + v
    ans = P(a + dx, b + dy)
    return mcq("Der Punkt A%s wird %s verschoben. Welche Koordinaten hat der neue Punkt A'?" % (P(a, b), dirs(dx, dy)), "A'" + ans,
               ["A'" + P(a + dy, b + dx), "A'" + P(a - dx, b - dy), "A'" + P(a + dx, b - dy), "A'" + P(a + dx, b), "A'" + P(a, b + dy), "A'" + P(a - dx, b + dy)], "x: %d %s %d = %d, y: %d %s %d = %d. <b>A'%s</b>." % (a, "+" if dx > 0 else "−", abs(dx), a + dx, b, "+" if dy > 0 else "−", abs(dy), b + dy, ans))


def ecke():
    kind = R.choice(["rechteck", "quadrat"])
    x1, y1 = R.randint(1, 5), R.randint(1, 5)
    w = R.randint(2, 5)
    h = w if kind == "quadrat" else R.randint(2, 5)
    if kind == "rechteck" and h == w:
        return None
    A, B, Cc, D = (x1, y1), (x1 + w, y1), (x1 + w, y1 + h), (x1, y1 + h)
    miss = R.choice(["B", "C", "D"])
    pts = {"A": A, "B": B, "C": Cc, "D": D}
    given = [(pts[k], k) for k in "ABCD" if k != miss]
    q = plane(given) + "A, B, C und D sollen ein %s ABCD bilden. Welche Koordinaten hat der Punkt %s?" % ("Rechteck" if kind == "rechteck" else "Quadrat", miss)
    m = pts[miss]
    return mcq(q, miss + P(*m), [miss + P(m[1], m[0]) if m[0] != m[1] else miss + P(m[0] + 1, m[1]), miss + P(m[0] + 1, m[1]), miss + P(m[0], m[1] - 1)],
               "Benachbarte Ecken liegen auf derselben Gitterlinie. %s bekommt x = %d von %s und y = %d von %s: <b>%s%s</b>." % ((miss,) + {"B": (m[0], "C", m[1], "A"), "C": (m[0], "B", m[1], "D"), "D": (m[0], "A", m[1], "C")}[miss] + (miss, P(*m))))


def abst():
    kind = R.choice(["waag", "senk", "umfang", "flaeche"])
    if kind == "waag":
        y = R.randint(0, 9)
        a, b = sorted(R.sample(range(0, 11), 2))
        return mcq("Wie viele Einheiten liegen A%s und B%s auseinander?" % (P(a, y), P(b, y)), str(b - a), [str(a + b), str(b - a + 1), str(y)] if y not in (b - a, a + b, b - a + 1) else [str(a + b), str(b - a + 1), str(b - a - 1)],
                   "Die y-Koordinate ist gleich. %d − %d = <b>%d</b> Einheiten." % (b, a, b - a))
    if kind == "senk":
        x = R.randint(0, 9)
        a, b = sorted(R.sample(range(0, 11), 2))
        return mcq("Wie viele Einheiten liegen C%s und D%s auseinander?" % (P(x, a), P(x, b)), str(b - a), [str(a + b), str(b - a + 1), str(b - a - 1)],
                   "Die x-Koordinate ist gleich. %d − %d = <b>%d</b> Einheiten." % (b, a, b - a))
    x1, y1 = R.randint(0, 4), R.randint(0, 4)
    w, h = R.randint(2, 6), R.randint(2, 6)
    if w == h:
        return None
    pts = [(x1, y1), (x1 + w, y1), (x1 + w, y1 + h), (x1, y1 + h)]
    lst = ", ".join(k + P(*p) for k, p in zip("ABCD", pts))
    if kind == "umfang":
        return mcq("Das Rechteck ABCD hat die Ecken %s. 1 Einheit = 1 cm. Wie groß ist der Umfang?" % lst, "%d cm" % (2 * (w + h)), ["%d cm" % x for x in (w + h, w * h, 2 * (w + h) + 2)],
                   "Seiten %d cm und %d cm. 2 %s %d + 2 %s %d = <b>%d cm</b>." % (w, h, MAL, w, MAL, h, 2 * (w + h)))
    return mcq("Das Rechteck ABCD hat die Ecken %s. 1 Einheit = 1 cm. Wie groß ist der Flächeninhalt?" % lst, "%d cm²" % (w * h), ["%d cm²" % x for x in (2 * (w + h), w + h, (w + 1) * (h + 1))],
               "Seiten %d cm und %d cm. %d %s %d = <b>%d cm²</b>." % (w, h, w, MAL, h, w * h))


def form():
    kind = R.choice(["dreieck", "linie", "muster", "spiegel"])
    if kind == "linie":
        y = R.randint(1, 8)
        xs = R.sample(range(0, 11), 3)
        if R.random() < 0.5:
            return mcq("Die Punkte %s liegen auf einer Linie. Wie liegt diese Linie?" % ", ".join(P(y, x) for x in sorted(xs)), "parallel zur y-Achse", ["parallel zur x-Achse", "schräg", "auf der x-Achse"],
                       "Alle Punkte haben x = %d: Die Linie ist <b>parallel zur y-Achse</b>." % y)
        return mcq("Die Punkte %s liegen auf einer Linie. Wie liegt diese Linie?" % ", ".join(P(x, y) for x in sorted(xs)), "parallel zur x-Achse", ["parallel zur y-Achse", "schräg", "auf der y-Achse"],
                   "Alle Punkte haben y = %d: Die Linie ist <b>parallel zur x-Achse</b>." % y)
    if kind == "muster":
        a, b = R.randint(0, 3), R.randint(0, 3)
        dx, dy = R.randint(1, 2), R.randint(1, 2)
        seq = [(a + i * dx, b + i * dy) for i in range(4)]
        nx = (a + 4 * dx, b + 4 * dy)
        return mcq("Setze fort: %s, …" % ", ".join(P(*p) for p in seq), P(*nx), [P(nx[1], nx[0]) if nx[0] != nx[1] else P(nx[0] + 1, nx[1]), P(nx[0] + dx, nx[1]), P(nx[0], nx[1] + dy)],
                   "x wächst um %d, y wächst um %d: <b>%s</b>." % (dx, dy, P(*nx)))
    if kind == "spiegel":
        a, b = R.randint(1, 4), R.randint(1, 9)
        m = 5
        sp = 2 * m - a
        return mcq("Der Punkt A%s wird an der Geraden x = 5 (parallel zur y-Achse) gespiegelt. Welche Koordinaten hat der Bildpunkt A'?" % P(a, b), "A'" + P(sp, b),
                   ["A'" + P(a, 10 - b) if 10 - b != b else "A'" + P(a, b + 1), "A'" + P(b, a), "A'" + P(sp + 1, b)], "A ist %d Einheiten links von x = 5, A' %d rechts: x = %d. <b>A'%s</b>." % (m - a, m - a, sp, P(sp, b)))
    pts = [rnd_pt(1, 9) for _ in range(3)]
    lab = ["A", "B", "C"]
    q = plane(list(zip(pts, lab)), polys=[pts]) + "Welche Koordinaten haben die Ecken des Dreiecks ABC?"
    if len(set(pts)) < 3:
        return None
    f = lambda L: ", ".join(k + P(*p) for k, p in zip(lab, L))
    return mcq(q, f(pts), [f([(p[1], p[0]) for p in pts]), f([(p[0], p[1] + 1) for p in pts]), f([pts[0], pts[2], pts[1]])], "Bei jedem Punkt erst x, dann y: <b>%s</b>." % f(pts))


def main():
    seen = set()
    sets = [
        ("Punkte ablesen", mix(R, seen, [(ablesen, 14), (achse, 6)])),
        ("Punkte finden", mix(R, seen, [(finden, 12), (form, 8)])),
        ("Punkte verschieben und spiegeln", mix(R, seen, [(verschieben, 20)])),
        ("Rechtecke und Quadrate", mix(R, seen, [(ecke, 20)])),
        ("Abstände, Umfang und Fläche", mix(R, seen, [(abst, 20)])),
    ]
    body = lesson(
        ["Ein <b>Koordinatensystem</b> hat eine waagerechte <b>x-Achse</b> und eine senkrechte <b>y-Achse</b>. Sie schneiden sich im <b>Ursprung</b> (0|0).",
         "Ein Punkt wird mit zwei Zahlen beschrieben: P(3|5). Die erste Zahl ist die <b>x-Koordinate</b> (nach rechts), die zweite die <b>y-Koordinate</b> (nach oben).",
         "Merksatz: <b>Erst gehen, dann steigen.</b>",
         "Beim <b>Verschieben</b> rechnet man: nach rechts +, nach links −, nach oben +, nach unten −."],
        [example("P(4|2) eintragen", ["4 Einheiten nach rechts", "dann 2 Einheiten nach oben"], "P(4|2)"),
         example("A(2|3) um 3 nach rechts und 1 nach unten", ["x: 2 + 3 = 5", "y: 3 − 1 = 2"], "A'(5|2)")],
        [["P(4|2) als 4 nach oben, 2 nach rechts", "Erst x nach rechts, dann y nach oben"],
         ["(3,5) geschrieben", "In Deutschland schreibt man (3|5)"],
         ["Die Achsen ohne 0 gezählt", "Die Zählung beginnt im Ursprung bei 0"]])
    faq = [
        {"q": "Welche Zahl kommt im Koordinatensystem zuerst?", "a": "Zuerst die x-Koordinate (nach rechts), dann die y-Koordinate (nach oben). Merksatz: erst gehen, dann steigen."},
        {"q": "Wie schreibt man Koordinaten in Deutschland?", "a": "Mit einem senkrechten Strich: P(3|5)."},
        {"q": "Was ist der Ursprung?", "a": "Der Punkt, an dem sich x-Achse und y-Achse schneiden. Er hat die Koordinaten (0|0)."},
        {"q": "Kommen in Klasse 5 auch negative Koordinaten vor?", "a": "Meist arbeitet man zuerst im ersten Quadranten mit Zahlen ab 0. Negative Koordinaten folgen oft in Klasse 6."},
    ]
    make_unit(R, "koordinatensystem", "R",
              "Die Schülerinnen und Schüler beschreiben die Lage von Punkten im Koordinatensystem (erster Quadrant), tragen Punkte ein, verschieben sie und bestimmen fehlende Eckpunkte von Figuren (Zusammenfassung).",
              "Das Koordinatensystem",
              "Koordinatensystem Klasse 5 – Arbeitsblätter mit Lösungen",
              "Koordinatensystem",
              "Koordinatensystem für Klasse 5: Punkte ablesen und eintragen, verschieben und spiegeln, Rechtecke im Koordinatensystem. 100 Aufgaben mit Lösungen, kostenlos.",
              "Erst gehen (x), dann steigen (y).",
              "P(3|5): 3 nach rechts, 5 nach oben.",
              body, faq, sets, 13, grade="klasse-5")


if __name__ == "__main__":
    main()
