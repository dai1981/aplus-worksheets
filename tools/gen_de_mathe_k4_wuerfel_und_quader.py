# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 4: Würfel und Quader – Netze, Ansichten, Kanten（Leitidee Raum und Form）
  python3 tools/gen_de_mathe_k4_wuerfel_und_quader.py
Ecken, Kanten, Flächen; gegenüberliegende Flächen im Würfelnetz; Ansichten von Würfelgebäuden; Quader aus Würfeln; Kantenmodelle.
Fehler: Kanten und Ecken verwechselt, im Netz benachbarte statt gegenüberliegende Fläche, Vorder- und Seitenansicht verwechselt, nur die sichtbaren Würfel gezählt.
"""
import random
from de_common import mcq, num, lesson, example, make_unit, mix, Kids, MAL, NB, wrap, table, solid_svg
from ws_common import text, GREEN, FILL, INK
from gen_de_mathe_k3_koerper_und_figuren import roll, is_net

R = random.Random(49117)
KIDS = Kids(R)

KOERPER = {"Würfel": (8, 12, 6), "Quader": (8, 12, 6), "Pyramide mit quadratischer Grundfläche": (5, 8, 5), "dreiseitiges Prisma": (6, 9, 5)}
ART = {"Würfel": "ein", "Quader": "ein", "Pyramide mit quadratischer Grundfläche": "eine", "dreiseitiges Prisma": "ein"}


def zaehlen():
    k = R.choice(list(KOERPER))
    e, ka, f = KOERPER[k]
    what = R.choice(["Ecken", "Kanten", "Flächen"])
    v = {"Ecken": e, "Kanten": ka, "Flächen": f}[what]
    w = [x for x in (e, ka, f, v + 1, v - 1, v * 2) if x != v and x > 0]
    w = list(dict.fromkeys(w))
    pic = solid_svg({"Würfel": "wuerfel", "Quader": "quader", "Pyramide mit quadratischer Grundfläche": "pyramide", "dreiseitiges Prisma": "prisma"}[k]) \
        if k != "dreiseitiges Prisma" else ""
    return mcq(pic + "Wie viele %s hat %s %s?" % (what, ART[k], k), str(v), [str(x) for x in w],
               "%s %s hat %d Ecken, %d Kanten und %d Flächen: <b>%d %s</b>." % (ART[k].capitalize(), k, e, ka, f, v, what))


def kantenmodell():
    kind = R.choice(["wuerfel", "quader", "zurueck"])
    if kind == "wuerfel":
        a = R.randint(3, 25)
        return mcq("Ein Kantenmodell eines Würfels wird aus Draht gebaut. Jede Kante ist %d cm lang. Wie viel Draht braucht man?" % a, "%d%scm" % (12 * a, NB),
                   ["%d%scm" % (x, NB) for x in (6 * a, 8 * a, 4 * a)],
                   "Ein Würfel hat 12 gleich lange Kanten: 12 %s %d cm = <b>%d cm</b>." % (MAL, a, 12 * a))
    if kind == "quader":
        a, b, c = R.sample(range(2, 16), 3)
        L = 4 * (a + b + c)
        return mcq("Ein Quader ist %d cm lang, %d cm breit und %d cm hoch. Wie lang sind alle Kanten zusammen?" % (a, b, c), "%d%scm" % (L, NB),
                   ["%d%scm" % (x, NB) for x in (a + b + c, 2 * (a + b + c), a * b * c, 12 * a) if x != L],
                   "Jede Länge kommt 4-mal vor: 4 %s %d + 4 %s %d + 4 %s %d = <b>%d cm</b>." % (MAL, a, MAL, b, MAL, c, L))
    a = R.randint(2, 15)
    return mcq("Alle Kanten eines Würfels sind zusammen %d cm lang. Wie lang ist eine Kante?" % (12 * a), "%d%scm" % (a, NB),
               ["%d%scm" % (x, NB) for x in (12 * a // 6, 12 * a // 8 if 12 * a % 8 == 0 else a + 1, 12 * a // 4) if x != a],
               "12 Kanten: %d cm : 12 = <b>%d cm</b>." % (12 * a, a))


# ------------------------------------------------------------ Netze: gegenüberliegende Flächen
def all_nets():
    out = set()
    rr = random.Random(7)
    for _ in range(20000):
        cells = {(0, 0)}
        while len(cells) < 6:
            x, y = rr.choice(sorted(cells))
            dx, dy = rr.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
            cells.add((x + dx, y + dy))
        mx, my = min(c[0] for c in cells), min(c[1] for c in cells)
        cells = frozenset((x - mx, y - my) for x, y in cells)
        if is_net(cells):
            out.add(cells)
    return sorted(out, key=lambda c: sorted(c))


NETS = all_nets()


def faces(cells):
    cells = set(cells)
    start = min(cells)
    seen = {start: (0, 1, 2, 3, 4, 5)}
    todo = [start]
    while todo:
        c = todo.pop()
        x, y = c
        for d, (dx, dy) in (("E", (1, 0)), ("W", (-1, 0)), ("N", (0, -1)), ("S", (0, 1))):
            n = (x + dx, y + dy)
            if n in cells and n not in seen:
                seen[n] = roll(seen[c], d)
                todo.append(n)
    return {c: s[0] for c, s in seen.items()}


OPP = {0: 1, 1: 0, 2: 3, 3: 2, 4: 5, 5: 4}


def net_svg(cells, labels):
    q = 34
    W = (max(c[0] for c in cells) + 1) * q + 20
    H = (max(c[1] for c in cells) + 1) * q + 20
    s = []
    for c in sorted(cells):
        x, y = 10 + c[0] * q, 10 + c[1] * q
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='2'/>" % (x, y, q, q, FILL, GREEN))
        s.append(text(x + q / 2, y + q * 0.68, labels[c], 18))
    return wrap(W, H, "".join(s), "Würfelnetz", lg=True)


def gegenueber():
    cells = R.choice(NETS)
    if R.random() < 0.5:
        cells = frozenset((y, x) for x, y in cells)
    fc = faces(cells)
    order = sorted(cells)
    marks = list("123456") if R.random() < 0.5 else list("ABCDEF")
    R.shuffle(marks)
    labels = {c: marks[i] for i, c in enumerate(order)}
    c0 = R.choice(order)
    opp = [c for c in order if fc[c] == OPP[fc[c0]]][0]
    neigh = [c for c in order if c not in (c0, opp)]
    adj = [c for c in neigh if abs(c[0] - c0[0]) + abs(c[1] - c0[1]) == 1]
    wrong = [labels[c] for c in adj] + [labels[c] for c in neigh if c not in adj]
    return mcq(net_svg(cells, labels) + "Das Netz wird zu einem Würfel gefaltet. Welche Fläche liegt <b>gegenüber</b> von %s?" % labels[c0],
               labels[opp], wrong[:3],
               "Gegenüberliegende Flächen berühren sich im Netz nie. Falte in Gedanken: Gegenüber von %s liegt <b>%s</b>." % (labels[c0], labels[opp]))


def spielwuerfel():
    cells = R.choice(NETS)
    fc = faces(cells)
    order = sorted(cells)
    good = R.random() < 0.5
    nums = {}
    pairs = [(1, 6), (2, 5), (3, 4)]
    R.shuffle(pairs)
    for i, (a, b) in enumerate(pairs):
        f1, f2 = [2 * i, 2 * i + 1] if R.random() < 0.5 else [2 * i + 1, 2 * i]
        nums[f1], nums[f2] = a, b
    if not good:
        i, j = R.sample(range(3), 2)
        a = nums[2 * i]
        nums[2 * i] = nums[2 * j]
        nums[2 * j] = a
    labels = {c: str(nums[fc[c]]) for c in order}
    ok = all(nums[k] + nums[OPP[k]] == 7 for k in range(6))
    ans = "Ja, gegenüber ergibt sich immer 7." if ok else "Nein, nicht alle Gegenseiten ergeben 7."
    return mcq(net_svg(cells, labels) + "Bei einem Spielwürfel ergeben die Augenzahlen gegenüberliegender Flächen zusammen immer 7. Passt dieses Netz zu einem Spielwürfel?",
               ans, [v for v in ("Ja, gegenüber ergibt sich immer 7.", "Nein, nicht alle Gegenseiten ergeben 7.") if v != ans] +
               ["Ja, weil alle Zahlen von 1 bis 6 vorkommen.", "Nein, weil die 6 oben stehen muss."],
               "Suche zu jeder Fläche die gegenüberliegende Fläche und addiere. %s" % ("Immer 7: <b>Ja</b>." if ok else "Nicht immer 7: <b>Nein</b>."))


# ------------------------------------------------------------ Ansichten
def views(grid):
    rows, cols = len(grid), len(grid[0])
    front = [max(grid[r][c] for r in range(rows)) for c in range(cols)]
    side = [max(grid[r][c] for c in range(cols)) for r in range(rows)][::-1]
    return front, side


def view_pics(opts):
    q = 16
    s = []
    for i, cols in enumerate(opts):
        ox = 10 + i * 100
        H = 4
        for j, h in enumerate(cols):
            for k in range(h):
                s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.5'/>" % (ox + j * q, 10 + (H - 1 - k) * q, q, q, FILL, GREEN))
        s.append(text(ox + 30, 10 + H * q + 22, "ABCD"[i], 16, col=GREEN))
    return wrap(10 + 4 * 100, 10 + 4 * q + 32, "".join(s), "vier Ansichten A bis D", lg=True)


def bauplan_html(grid):
    return ("<table class='sn-table' style='width:auto;margin:6px 0'><tbody>%s</tbody></table>"
            % "".join("<tr>%s</tr>" % "".join("<td style='text-align:center;min-width:34px;height:30px'>%d</td>" % v for v in r) for r in grid))


def ansicht():
    rows, cols = R.randint(2, 3), R.randint(2, 3)
    grid = [[R.randint(1, 4) for _ in range(cols)] for _ in range(rows)]
    front, side = views(grid)
    which = R.choice(["vorne", "rechts"])
    ans = front if which == "vorne" else side
    other = side if which == "vorne" else front
    w = [other, grid[-1] if which == "vorne" else [r[-1] for r in grid][::-1], grid[0] if which == "vorne" else [r[0] for r in grid][::-1],
         ans[::-1], [min(1 + v, 4) for v in ans]]
    w = [x for x in w if list(x) != list(ans)]
    uniq = []
    for x in w:
        if list(x) not in [list(u) for u in uniq]:
            uniq.append(x)
    if len(uniq) < 3:
        return None
    opts = uniq[:3] + [ans]
    R.shuffle(opts)
    k = opts.index(ans)
    txt = ("Bauplan eines Würfelgebäudes (oben im Plan ist hinten, unten ist vorne). Die Zahlen sagen, wie viele Würfel übereinander stehen. "
           "Welche Ansicht siehst du von <b>%s</b>?" % ("vorne" if which == "vorne" else "rechts"))
    return mcq(txt + bauplan_html(grid) + view_pics(opts), "ABCD"[k], [c for i, c in enumerate("ABCD") if i != k],
               ("Von vorne siehst du in jeder Spalte den höchsten Turm: %s. Das ist <b>%s</b>." % (", ".join(map(str, ans)), "ABCD"[k])) if which == "vorne" else
               ("Von rechts siehst du in jeder Zeile den höchsten Turm (von vorne nach hinten: %s). Das ist <b>%s</b>." % (", ".join(map(str, ans)), "ABCD"[k])))


# ------------------------------------------------------------ Quader aus Würfeln
def quader_wuerfel():
    kind = R.choice(["quader", "wuerfel", "fehlt", "schicht"])
    if kind == "quader":
        a, b, c = R.randint(2, 6), R.randint(2, 5), R.randint(2, 4)
        n = a * b * c
        return mcq("Ein Quader wird aus kleinen Würfeln gebaut. Er ist %d Würfel lang, %d Würfel breit und %d Würfel hoch. Wie viele Würfel braucht man?" % (a, b, c),
                   str(n), [str(x) for x in (a + b + c, a * b, 2 * (a * b + b * c + a * c), n + a) if x != n],
                   "Eine Schicht: %d %s %d = %d Würfel. %d Schichten: %d %s %d = <b>%d</b>." % (a, MAL, b, a * b, c, a * b, MAL, c, n))
    if kind == "wuerfel":
        k = R.randint(2, 5)
        n = k ** 3
        return mcq("Aus kleinen Würfeln wird ein großer Würfel gebaut. Jede Kante ist %d kleine Würfel lang. Wie viele kleine Würfel braucht man?" % k,
                   str(n), [str(x) for x in (k * k, 3 * k, 6 * k * k, 12 * k) if x != n],
                   "%d %s %d %s %d = <b>%d</b>." % (k, MAL, k, MAL, k, n))
    if kind == "fehlt":
        a, b, c = R.randint(2, 5), R.randint(2, 4), R.randint(2, 4)
        n = a * b * c
        have = n - R.randint(2, a * b)
        return mcq("Ein Quader soll %d Würfel lang, %d Würfel breit und %d Würfel hoch werden. Es sind schon %d Würfel da. Wie viele Würfel fehlen noch?" % (a, b, c, have),
                   str(n - have), [str(x) for x in (n, have - (a + b + c) if have > a + b + c else n - have + 1, n - have + a, a * b - (n - have) if a * b > n - have else n - have + 2) if x != n - have],
                   "Man braucht %d %s %d %s %d = %d Würfel. %d − %d = <b>%d</b>." % (a, MAL, b, MAL, c, n, n, have, n - have))
    a, b = R.randint(2, 6), R.randint(2, 5)
    c = R.randint(2, 5)
    n = a * b * c
    return mcq("Ein Quader aus %d Würfeln ist %d Würfel lang und %d Würfel breit. Wie viele Würfel hoch ist er?" % (n, a, b), str(c),
               [str(x) for x in (n // a, n // b, c + 1, n - a * b) if x != c],
               "Eine Schicht hat %d %s %d = %d Würfel. %d : %d = <b>%d</b>." % (a, MAL, b, a * b, n, a * b, c))


def sache():
    kind = R.choice(["strohhalme", "knete", "bekleben", "geschenk", "drahtrest"])
    p = KIDS.next()
    if kind == "strohhalme":
        n = R.randint(2, 6)
        return mcq("%s baut %d Kantenmodelle von Würfeln aus Strohhalmen. Für jede Kante braucht %s einen Strohhalm. Wie viele Strohhalme braucht %s?" % (p[0], n, p[1], p[1]),
                   str(12 * n), [str(x) for x in (8 * n, 6 * n, 12 + n)],
                   "Ein Würfel hat 12 Kanten: %d %s 12 = <b>%d</b>." % (n, MAL, 12 * n))
    if kind == "knete":
        n = R.randint(2, 7)
        return mcq("Für die Ecken eines Würfelmodells nimmt %s Knetkugeln. Wie viele Knetkugeln braucht %s für %d Würfelmodelle?" % (p[0], p[1], n),
                   str(8 * n), [str(x) for x in (12 * n, 6 * n, 8 + n)],
                   "Ein Würfel hat 8 Ecken: %d %s 8 = <b>%d</b>." % (n, MAL, 8 * n))
    if kind == "bekleben":
        a = R.randint(2, 9)
        A = 6 * a * a
        return mcq("%s beklebt alle Flächen eines Würfels mit buntem Papier. Eine Kante ist %d cm lang. Wie viel cm² Papier braucht %s mindestens?" % (p[0], a, p[1]),
                   "%d%scm²" % (A, NB), ["%d%scm²" % (x, NB) for x in (a * a, 4 * a * a, 12 * a) if x != A],
                   "Eine Fläche: %d %s %d = %d cm². 6 Flächen: 6 %s %d = <b>%d cm²</b>." % (a, MAL, a, a * a, MAL, a * a, A))
    if kind == "geschenk":
        n = R.randint(3, 8)
        k = R.randint(2, 4)
        return mcq("Ein Paket ist ein Würfel. %s stellt %d solche Pakete in eine Reihe und %d Reihen hintereinander. Dann stapelt %s noch eine zweite Schicht genauso darauf. Wie viele Pakete sind es?" % (p[0], n, k, p[1]),
                   str(n * k * 2), [str(x) for x in (n * k, n + k + 2, n * 2 + k) if x != n * k * 2],
                   "Eine Schicht: %d %s %d = %d. Zwei Schichten: <b>%d</b>." % (n, MAL, k, n * k, n * k * 2))
    L = R.choice([1, 2, 3])
    a = R.randint(5, 20)
    use = 12 * a
    if use > L * 100:
        return None
    return mcq("%s hat %d m Draht und baut damit das Kantenmodell eines Würfels mit %d cm langen Kanten. Wie viel Draht bleibt übrig?" % (p[0], L, a),
               "%d%scm" % (L * 100 - use, NB), ["%d%scm" % (x, NB) for x in (L * 100 - 8 * a, L * 100 - 6 * a, use) if x != L * 100 - use],
               "Verbraucht: 12 %s %d cm = %d cm. %d m = %d cm. %d − %d = <b>%d cm</b>." % (MAL, a, use, L, L * 100, L * 100, use, L * 100 - use))


def main():
    seen = set()
    sets = [
        ("Ecken, Kanten und Flächen", mix(R, seen, [(zaehlen, 10), (kantenmodell, 10)])),
        ("Würfelnetze", mix(R, seen, [(gegenueber, 14), (spielwuerfel, 6)])),
        ("Ansichten", mix(R, seen, [(ansicht, 20)])),
        ("Quader aus Würfeln", mix(R, seen, [(quader_wuerfel, 20)])),
        ("Sachaufgaben", mix(R, seen, [(sache, 20)])),
    ]
    body = lesson(
        ["Würfel und Quader haben <b>8 Ecken, 12 Kanten und 6 Flächen</b>. Beim Würfel sind alle Flächen gleich große Quadrate.",
         "Ein <b>Netz</b> entsteht, wenn man einen Körper aufschneidet und flach auslegt. Gegenüberliegende Flächen berühren sich im Netz nie.",
         "Bei einem Würfelgebäude siehst du von vorne in jeder Spalte nur den höchsten Turm.",
         "Ein Quader aus Würfeln: Würfel in einer Schicht (Länge %s Breite) mal Anzahl der Schichten." % MAL],
        [example("Würfel mit 5 cm Kanten als Kantenmodell", ["12 Kanten", "12 %s 5 cm = 60 cm" % MAL], "60 cm Draht"),
         example("Quader 4 Würfel lang, 3 breit, 2 hoch", ["eine Schicht: 4 %s 3 = 12" % MAL, "2 Schichten: 12 %s 2 = 24" % MAL], "24 Würfel")],
        [["Kanten und Ecken verwechseln", "Ecken sind Punkte (8), Kanten sind Linien (12)"],
         ["Im Netz die Nachbarfläche als Gegenfläche nehmen", "Gegenüber liegt eine Fläche, die nicht angrenzt"],
         ["Nur die sichtbaren Würfel zählen", "Auch die Würfel innen und hinten mitzählen"]],
        extra=table(["Körper", "Ecken", "Kanten", "Flächen"], [["Würfel", "8", "12", "6"], ["Quader", "8", "12", "6"], ["Pyramide (quadratisch)", "5", "8", "5"], ["dreiseitiges Prisma", "6", "9", "5"]]))
    faq = [
        {"q": "Wie viele Würfelnetze gibt es?", "a": "Es gibt genau 11 verschiedene Würfelnetze. Gedrehte oder gespiegelte Netze zählen dabei nicht extra."},
        {"q": "Wie findet man im Netz die gegenüberliegende Fläche?", "a": "In einer Reihe von drei Quadraten liegen das erste und das dritte gegenüber. Allgemein gilt: Gegenüberliegende Flächen haben im Netz keine gemeinsame Kante."},
        {"q": "Was ist der Unterschied zwischen Würfel und Quader?", "a": "Beide haben 8 Ecken, 12 Kanten und 6 Flächen. Beim Würfel sind alle Kanten gleich lang, beim Quader nicht unbedingt."},
        {"q": "Was ist ein Bauplan?", "a": "Ein Bauplan zeigt ein Würfelgebäude von oben. In jedem Feld steht, wie viele Würfel dort übereinander stehen."},
    ]
    make_unit(R, "wuerfel-und-quader", "R",
              "Die Schülerinnen und Schüler beschreiben Würfel und Quader mit Ecken, Kanten und Flächen, untersuchen Würfelnetze, ordnen Ansichten von Würfelgebäuden zu und bestimmen die Anzahl der Würfel in Quadern (Zusammenfassung).",
              "Würfel und Quader: Netze, Ansichten und Kanten",
              "Würfel und Quader Klasse 4 – Arbeitsblätter mit Lösungen",
              "Würfel und Quader",
              "Würfel und Quader für Klasse 4: Ecken, Kanten und Flächen, Würfelnetze, Ansichten von Würfelgebäuden, Quader aus Würfeln und Kantenmodelle. 100 Übungsaufgaben mit Lösungen, kostenlos.",
              "8 Ecken, 12 Kanten, 6 Flächen.",
              "Gegenüberliegende Flächen berühren sich im Netz nie.",
              body, faq, sets, 17, grade="klasse-4")


if __name__ == "__main__":
    main()
