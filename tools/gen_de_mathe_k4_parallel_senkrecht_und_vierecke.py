# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 4: Parallel, senkrecht und Vierecke（Leitidee Raum und Form）
  python3 tools/gen_de_mathe_k4_parallel_senkrecht_und_vierecke.py
Parallele und senkrechte Geraden erkennen, rechte Winkel, Vierecke benennen (Quadrat, Rechteck, Raute, Parallelogramm, Trapez),
Eigenschaften, Figuren untersuchen.
Fehler: schräg liegendes Quadrat als Raute bezeichnen, „senkrecht" mit „von oben nach unten" verwechseln, jedes Viereck mit parallelen Seiten Rechteck nennen.
"""
import math
import random
from de_common import mcq, lesson, example, make_unit, mix, wrap, table
from ws_common import line, text, INK, GREEN, FILL, BLUE

R = random.Random(49116)


def seg(x, y, ang, L):
    dx, dy = math.cos(math.radians(ang)) * L / 2, -math.sin(math.radians(ang)) * L / 2
    return (x - dx, y - dy, x + dx, y + dy)


def two_lines(kind):
    a = R.choice([0, 15, 30, 45, 60, 75, 90, 105, 120, 135, 150, 165, R.randint(5, 175)])
    L = R.randint(130, 170)
    if kind == "parallel":
        d = R.randint(40, 70)
        nx, ny = math.cos(math.radians(a + 90)) * d, -math.sin(math.radians(a + 90)) * d
        sh = R.randint(-30, 30)
        l1 = seg(140 - nx / 2, 120 - ny / 2, a, L)
        l2 = seg(140 + nx / 2 + math.cos(math.radians(a)) * sh, 120 + ny / 2 - math.sin(math.radians(a)) * sh, a, L - R.randint(0, 40))
    else:
        b = a + 90 if kind == "senkrecht" else a + R.choice([R.randint(30, 65), R.randint(115, 150)])
        l1 = seg(140, 120, a, L)
        t = R.uniform(-0.3, 0.3) * L
        l2 = seg(140 + math.cos(math.radians(a)) * t, 120 - math.sin(math.radians(a)) * t, b, R.randint(110, 150))
    s = [line(*l1, col=GREEN, w=3), line(*l2, col=BLUE, w=3)]
    return wrap(280, 240, "".join(s), "zwei Geraden"), a


def lage():
    kind = R.choice(["parallel", "senkrecht", "weder"])
    pic, a = two_lines(kind)
    ans = {"parallel": "Sie sind parallel.", "senkrecht": "Sie sind senkrecht zueinander.", "weder": "Weder parallel noch senkrecht."}[kind]
    e = {"parallel": "Die Geraden haben überall den gleichen Abstand und schneiden sich nie: <b>parallel</b>.",
         "senkrecht": "Die Geraden schneiden sich in einem rechten Winkel: <b>senkrecht</b>.",
         "weder": "Sie schneiden sich, aber nicht im rechten Winkel: <b>weder parallel noch senkrecht</b>."}[kind]
    return mcq(pic + "Wie liegen die grüne und die blaue Gerade zueinander?",
               ans, [v for v in ("Sie sind parallel.", "Sie sind senkrecht zueinander.", "Weder parallel noch senkrecht.") if v != ans] + ["Sie sind gleich lang."], e)


def quad_pts(kind):
    s = R.randint(70, 110)
    if kind == "Quadrat":
        w, h, sh, top = s, s, 0, s
    elif kind == "Rechteck":
        w = R.randint(110, 170)
        h = R.randint(55, 95)
        sh, top = 0, w
    elif kind == "Parallelogramm":
        w, h = R.randint(100, 150), R.randint(60, 90)
        sh, top = R.choice([-1, 1]) * R.randint(30, 50), w
        if abs(math.hypot(sh, h) - w) < 20:
            return quad_pts(kind)
    elif kind == "Trapez":
        w, h = R.randint(130, 180), R.randint(60, 90)
        top = w - R.randint(40, 80)
        sh = R.randint(0, w - top)
    else:  # Raute
        d1, d2 = R.randint(130, 180), R.randint(70, 110)
        cx, cy = 110, 100
        return [(cx - d1 / 2, cy), (cx, cy - d2 / 2), (cx + d1 / 2, cy), (cx, cy + d2 / 2)]
    x0 = 30 + max(0, -sh)
    y0 = 40 + h
    return [(x0, y0), (x0 + w, y0), (x0 + sh + top, y0 - h), (x0 + sh, y0 - h)] if kind != "Trapez" else \
           [(x0, y0), (x0 + w, y0), (x0 + sh + top, y0 - h), (x0 + sh, y0 - h)]


def quad_svg(pts, label):
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    ox, oy = 20 - min(xs), 20 - min(ys)
    pp = " ".join("%.0f,%.0f" % (x + ox, y + oy) for x, y in pts)
    W, H = max(xs) - min(xs) + 40, max(ys) - min(ys) + 40
    return wrap(W, H, "<polygon points='%s' fill='%s' stroke='%s' stroke-width='2.5'/>" % (pp, FILL, GREEN), label)


NAMES = ["Quadrat", "Rechteck", "Raute", "Parallelogramm", "Trapez"]
WRONG = {"Quadrat": ["Rechteck", "Raute", "Trapez"], "Rechteck": ["Quadrat", "Parallelogramm", "Trapez"],
         "Raute": ["Quadrat", "Parallelogramm", "Trapez"], "Parallelogramm": ["Rechteck", "Raute", "Trapez"],
         "Trapez": ["Parallelogramm", "Rechteck", "Raute"]}
WHY = {"Quadrat": "4 gleich lange Seiten und 4 rechte Winkel",
       "Rechteck": "4 rechte Winkel, gegenüberliegende Seiten sind gleich lang",
       "Raute": "4 gleich lange Seiten, aber keine rechten Winkel",
       "Parallelogramm": "je zwei gegenüberliegende Seiten sind parallel, aber keine rechten Winkel",
       "Trapez": "nur zwei Seiten sind parallel"}
RIGHT = {"Quadrat": 4, "Rechteck": 4, "Raute": 0, "Parallelogramm": 0, "Trapez": 0}
PAR = {"Quadrat": 2, "Rechteck": 2, "Raute": 2, "Parallelogramm": 2, "Trapez": 1}


def benennen():
    k = R.choice(NAMES)
    pts = quad_pts(k)
    return mcq(quad_svg(pts, "Viereck") + "Wie heißt dieses Viereck?", k, WRONG[k], "Es hat %s: %s <b>%s</b>." % (WHY[k], "eine" if k == "Raute" else "ein", k))


def rechte_winkel():
    kind = R.choice(["viereck", "figur", "uhr"])
    if kind == "viereck":
        k = R.choice(NAMES)
        n = RIGHT[k]
        if k == "Trapez" and R.random() < 0.5:
            w, h, top = R.randint(130, 170), R.randint(60, 90), R.randint(60, 100)
            pts = [(30, 40 + h), (30 + w, 40 + h), (30 + top, 40), (30, 40)]
            n = 2
        else:
            pts = quad_pts(k)
        return mcq(quad_svg(pts, "Viereck") + "Wie viele rechte Winkel hat dieses Viereck?", "%d" % n, ["%d" % x for x in (0, 1, 2, 3, 4) if x != n][:3],
                   "Prüfe jede Ecke mit dem Geodreieck: <b>%d</b> rechte Winkel." % n)
    if kind == "figur":
        w, h = R.randint(3, 6), R.randint(3, 5)
        cx, cy = R.randint(1, w - 1), R.randint(1, h - 1)
        k = 26
        pts = [(0, 0), (w - cx, 0), (w - cx, cy), (w, cy), (w, h), (0, h)]
        pp = " ".join("%d,%d" % (20 + x * k, 20 + y * k) for x, y in pts)
        pic = wrap(w * k + 40, h * k + 40, "<polygon points='%s' fill='%s' stroke='%s' stroke-width='2.5'/>" % (pp, FILL, GREEN), "Figur mit 6 Ecken")
        return mcq(pic + "Diese Figur hat 6 Ecken. An wie vielen Ecken ist innen ein rechter Winkel?", "5", ["6", "4", "3"],
                   "An 5 Ecken ist innen ein rechter Winkel. An der eingeknickten Ecke ist der Winkel innen größer als ein rechter Winkel: <b>5</b>.")
    deg = R.choice([R.randint(25, 70), 90, 90, R.randint(110, 160)])
    rot = R.choice([0, 0, R.randint(10, 60)])
    L = 110
    x0, y0 = 70, 150
    x1, y1 = x0 + L * math.cos(math.radians(rot)), y0 - L * math.sin(math.radians(rot))
    x2, y2 = x0 + L * math.cos(math.radians(rot + deg)), y0 - L * math.sin(math.radians(rot + deg))
    s = [line(x0, y0, x1, y1, col=GREEN, w=3), line(x0, y0, x2, y2, col=GREEN, w=3)]
    xs, ys = [x0, x1, x2], [y0, y1, y2]
    body = "<g transform='translate(%.0f,%.0f)'>%s</g>" % (20 - min(xs), 20 - min(ys), "".join(s))
    pic = wrap(max(xs) - min(xs) + 40, max(ys) - min(ys) + 40, body, "Winkel")
    ans = "genau ein rechter Winkel" if deg == 90 else "kleiner als ein rechter Winkel" if deg < 90 else "größer als ein rechter Winkel"
    return mcq(pic + "Vergleiche den Winkel mit einem rechten Winkel.", ans,
               [v for v in ("genau ein rechter Winkel", "kleiner als ein rechter Winkel", "größer als ein rechter Winkel") if v != ans] + ["Das kann man nicht sagen"],
               "Lege die Ecke des Geodreiecks an: Der Winkel ist <b>%s</b>." % ans)


def eigenschaften():
    facts = [
        ("Welche Aussage stimmt?", "Jedes Quadrat ist auch ein Rechteck.", ["Jedes Rechteck ist auch ein Quadrat.", "Ein Quadrat hat keine rechten Winkel.", "Eine Raute hat immer 4 rechte Winkel."],
         "Ein Quadrat hat 4 rechte Winkel wie ein Rechteck, nur sind alle Seiten gleich lang: <b>Jedes Quadrat ist auch ein Rechteck.</b>"),
        ("Welche Aussage stimmt?", "Jedes Quadrat ist auch eine Raute.", ["Jede Raute ist auch ein Quadrat.", "Eine Raute hat nur 2 gleich lange Seiten.", "Ein Quadrat ist ein Trapez ohne parallele Seiten."],
         "Eine Raute hat 4 gleich lange Seiten. Das hat ein Quadrat auch: <b>Jedes Quadrat ist auch eine Raute.</b>"),
        ("Wie viele Paare paralleler Seiten hat ein Rechteck?", "2", ["1", "4", "0"], "Oben und unten, links und rechts: <b>2</b> Paare."),
        ("Wie viele Paare paralleler Seiten hat ein Trapez mindestens?", "1", ["0", "2", "4"], "Ein Trapez hat <b>mindestens ein</b> Paar paralleler Seiten."),
        ("Welches Viereck hat 4 gleich lange Seiten und 4 rechte Winkel?", "Quadrat", ["Raute", "Rechteck", "Trapez"], "Gleich lange Seiten und rechte Winkel: <b>Quadrat</b>."),
        ("Welches Viereck hat 4 gleich lange Seiten, aber keine rechten Winkel?", "Raute", ["Quadrat", "Rechteck", "Trapez"], "Das ist eine <b>Raute</b>."),
        ("Welches Viereck hat 4 rechte Winkel, aber nicht alle Seiten gleich lang?", "Rechteck", ["Quadrat", "Raute", "Parallelogramm"], "Das ist ein <b>Rechteck</b>."),
        ("Welches Viereck hat genau ein Paar paralleler Seiten?", "Trapez", ["Parallelogramm", "Rechteck", "Raute"], "Nur zwei Seiten parallel: <b>Trapez</b>."),
        ("Bei welchem Viereck sind gegenüberliegende Seiten parallel, aber es gibt keine rechten Winkel und nicht alle Seiten sind gleich lang?", "Parallelogramm",
         ["Rechteck", "Raute", "Trapez"], "Das ist ein <b>Parallelogramm</b>."),
        ("Wie nennt man zwei Geraden, die sich nie schneiden und überall den gleichen Abstand haben?", "parallel", ["senkrecht", "schräg", "waagerecht"],
         "Solche Geraden sind <b>parallel</b>."),
        ("Wie nennt man zwei Geraden, die sich in einem rechten Winkel schneiden?", "senkrecht zueinander", ["parallel", "waagerecht", "gleich lang"],
         "Sie stehen <b>senkrecht zueinander</b>."),
        ("Mit welchem Werkzeug prüfst du am besten, ob ein Winkel ein rechter Winkel ist?", "mit dem Geodreieck", ["mit dem Zirkel", "mit dem Radiergummi", "mit dem Bleistift"],
         "Das Geodreieck hat einen rechten Winkel und eine Mittellinie: <b>mit dem Geodreieck</b>."),
        ("Wie viele Ecken hat ein Viereck?", "4", ["3", "5", "8"], "Ein Viereck hat <b>4</b> Ecken und 4 Seiten."),
        ("Wie viele rechte Winkel hat eine Raute, die kein Quadrat ist?", "0", ["2", "4", "1"], "Eine Raute, die kein Quadrat ist, hat <b>keinen</b> rechten Winkel."),
        ("Welche Aussage stimmt?", "Jedes Rechteck ist auch ein Parallelogramm.", ["Jedes Parallelogramm ist auch ein Rechteck.", "Ein Rechteck hat nur 2 rechte Winkel.", "Ein Rechteck hat keine parallelen Seiten."],
         "Im Rechteck sind gegenüberliegende Seiten parallel: <b>Jedes Rechteck ist auch ein Parallelogramm.</b>"),
        ("Ein Viereck hat zwei Paare paralleler Seiten und 4 rechte Winkel. Die Seiten sind 5 cm und 3 cm lang. Was ist es?", "Rechteck",
         ["Quadrat", "Raute", "Trapez"], "4 rechte Winkel, verschiedene Seitenlängen: <b>Rechteck</b>."),
        ("Ein Viereck hat 4 Seiten von je 4 cm und 4 rechte Winkel. Was ist es?", "Quadrat", ["Rechteck", "Raute", "Parallelogramm"],
         "Alle Seiten gleich und rechte Winkel: <b>Quadrat</b>."),
        ("Ein Viereck hat 4 Seiten von je 6 cm, aber keine rechten Winkel. Was ist es?", "Raute", ["Quadrat", "Rechteck", "Trapez"],
         "Alle Seiten gleich, keine rechten Winkel: <b>Raute</b>."),
        ("Wie nennt man eine Linie, die genau von links nach rechts verläuft wie der Horizont?", "waagerecht", ["senkrecht", "schräg", "parallel"],
         "Wie die Wasseroberfläche: <b>waagerecht</b>."),
        ("Wie viele Diagonalen hat ein Viereck?", "2", ["1", "4", "3"], "Von jeder Ecke zur gegenüberliegenden Ecke: <b>2</b> Diagonalen."),
        ("In welchem Viereck stehen die beiden Diagonalen senkrecht zueinander und sind gleich lang?", "Quadrat", ["Rechteck", "Parallelogramm", "Trapez"],
         "Gleich lang und senkrecht zueinander sind die Diagonalen im <b>Quadrat</b>."),
        ("In welchem Viereck stehen die Diagonalen senkrecht zueinander, sind aber verschieden lang?", "Raute", ["Rechteck", "Quadrat", "Trapez"],
         "Das ist bei der <b>Raute</b> so."),
    ]
    st = {"i": 0}
    order = list(range(len(facts)))
    R.shuffle(order)

    def mk():
        if st["i"] >= len(order):
            return None
        f = facts[order[st["i"]]]
        st["i"] += 1
        return mcq(f[0], f[1], f[2], f[3])
    return mk


EIG = eigenschaften()


def alltag():
    items = [("die beiden Schienen eines Gleises", "parallel"), ("die Linien in einem Schulheft", "parallel"), ("die Saiten einer Gitarre", "parallel"),
             ("die Stufen einer Leiter", "parallel"), ("die Sprossen eines Gitters", "parallel"),
             ("ein Tischbein und die Tischplatte", "senkrecht"), ("ein Fahnenmast und der Boden", "senkrecht"), ("die Kanten an der Ecke eines Buches", "senkrecht"),
             ("die Zeiger einer Uhr um 3 Uhr", "senkrecht"), ("die Zeiger einer Uhr um 9 Uhr", "senkrecht"), ("die beiden Striche in einem Pluszeichen +", "senkrecht"),
             ("die Zeiger einer Uhr um 1 Uhr", "weder"), ("die Striche im Buchstaben V", "weder"), ("die Striche im Buchstaben X", "weder"),
             ("die gegenüberliegenden Kanten einer Tafel", "parallel"), ("die Ränder einer Straße auf gerader Strecke", "parallel"),
             ("die Wand und der Fußboden im Zimmer", "senkrecht"), ("die Striche im Buchstaben L", "senkrecht"), ("die beiden schrägen Striche im Buchstaben A", "weder"),
             ("die Streifen auf einem Zebrastreifen", "parallel"), ("die Striche im Buchstaben T", "senkrecht"), ("die Zeiger einer Uhr um 2 Uhr", "weder")]
    st = {"i": 0}
    order = list(range(len(items)))
    R.shuffle(order)
    A = {"parallel": "parallel", "senkrecht": "senkrecht zueinander", "weder": "weder parallel noch senkrecht"}

    def mk():
        if st["i"] >= len(order):
            return None
        t, k = items[order[st["i"]]]
        st["i"] += 1
        return mcq("Wie liegen %s zueinander?" % t, A[k], [v for v in A.values() if v != A[k]] + ["gleich lang"],
                   {"parallel": "Sie schneiden sich nie und haben immer den gleichen Abstand: <b>parallel</b>.",
                    "senkrecht": "Sie bilden einen rechten Winkel: <b>senkrecht zueinander</b>.",
                    "weder": "Sie treffen sich, aber nicht im rechten Winkel: <b>weder parallel noch senkrecht</b>."}[k])
    return mk


ALL = alltag()


def main():
    seen = set()
    sets = [
        ("Parallel oder senkrecht?", mix(R, seen, [(lage, 20)])),
        ("Im Alltag", mix(R, seen, [(ALL, 20)])),
        ("Vierecke benennen", mix(R, seen, [(benennen, 20)])),
        ("Rechte Winkel zählen", mix(R, seen, [(rechte_winkel, 20)])),
        ("Eigenschaften der Vierecke", mix(R, seen, [(EIG, 20)])),
    ]
    body = lesson(
        ["Zwei Geraden sind <b>parallel</b>, wenn sie überall den gleichen Abstand haben und sich nie schneiden.",
         "Zwei Geraden sind <b>senkrecht zueinander</b>, wenn sie sich in einem <b>rechten Winkel</b> schneiden. Du prüfst das mit dem Geodreieck.",
         "Senkrecht heißt nicht nur „von oben nach unten“. Auch schräge Geraden können senkrecht zueinander sein.",
         "Vierecke unterscheidest du an den Seiten und Winkeln: Quadrat, Rechteck, Raute, Parallelogramm und Trapez."],
        [example("Ein Viereck mit 4 gleich langen Seiten und 4 rechten Winkeln", ["Seiten gleich → Quadrat oder Raute", "rechte Winkel → Quadrat"], "Quadrat"),
         example("Ein Viereck mit genau einem Paar paralleler Seiten", ["nicht alle Gegenseiten parallel"], "Trapez")],
        [["Ein schräg gedrehtes Quadrat ist eine Raute", "Es bleibt ein Quadrat (rechte Winkel prüfen)"],
         ["Senkrecht = immer von oben nach unten", "Senkrecht zueinander = rechter Winkel zwischen zwei Geraden"],
         ["Jedes Viereck mit parallelen Seiten ist ein Rechteck", "Ohne rechte Winkel ist es ein Parallelogramm"]],
        extra=table(["Viereck", "Seiten", "rechte Winkel"],
                    [["Quadrat", "4 gleich lang", "4"], ["Rechteck", "Gegenseiten gleich lang", "4"], ["Raute", "4 gleich lang", "keine"],
                     ["Parallelogramm", "Gegenseiten parallel", "keine"], ["Trapez", "2 Seiten parallel", "oft keine"]]))
    faq = [
        {"q": "Was ist der Unterschied zwischen senkrecht und waagerecht?", "a": "Waagerecht verläuft eine Linie wie der Horizont. Senkrecht zueinander sind zwei Linien, die einen rechten Winkel bilden, egal wie sie gedreht sind."},
        {"q": "Wie prüft man mit dem Geodreieck, ob zwei Geraden parallel sind?", "a": "Man legt die Mittellinie des Geodreiecks auf eine Gerade und schaut, ob die andere Gerade auf einer der parallelen Hilfslinien liegt."},
        {"q": "Ist ein Quadrat ein Rechteck?", "a": "Ja. Ein Quadrat hat 4 rechte Winkel wie jedes Rechteck. Es ist ein besonderes Rechteck mit 4 gleich langen Seiten."},
        {"q": "Welche Vierecke lernt man in der Grundschule?", "a": "Meist Quadrat, Rechteck, Raute, Parallelogramm und Trapez. Manche Bundesländer nehmen auch das Drachenviereck dazu."},
    ]
    make_unit(R, "parallel-senkrecht-und-vierecke", "R",
              "Die Schülerinnen und Schüler erkennen parallele und senkrechte Geraden und rechte Winkel, auch in der Umwelt, benennen Vierecke und beschreiben ihre Eigenschaften mit Fachbegriffen (Zusammenfassung).",
              "Parallel, senkrecht und Vierecke",
              "Parallel und senkrecht, Vierecke Klasse 4 – Arbeitsblätter mit Lösungen",
              "Parallel und senkrecht",
              "Parallel und senkrecht für Klasse 4: Geraden untersuchen, rechte Winkel, Quadrat, Rechteck, Raute, Parallelogramm und Trapez. 100 Übungsaufgaben mit Lösungen, kostenlos.",
              "Parallel: nie schneiden. Senkrecht: rechter Winkel.",
              "Vierecke erkennst du an Seiten und Winkeln.",
              body, faq, sets, 16, grade="klasse-4")


if __name__ == "__main__":
    main()
