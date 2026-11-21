# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 3: Körper und Figuren（Leitidee Raum und Form）
  python3 tools/gen_de_mathe_k3_koerper_und_figuren.py
Körper erkennen, Ecken/Kanten/Flächen, Baupläne von Würfelgebäuden, Würfelnetze, Körper und Figuren in der Umwelt.
Fehler: Würfel und Quader verwechselt, Kanten und Ecken verwechselt, Würfel im Bauplan nicht gezählt, Netze mit 2 Flächen übereinander.
"""
import random
from de_common import mcq, lesson, example, make_unit, mix, solid_svg, wrap, table
from ws_common import text, INK, GREEN, FILL

R = random.Random(49015)

NAMES = {"wuerfel": "Würfel", "quader": "Quader", "kugel": "Kugel", "zylinder": "Zylinder", "kegel": "Kegel", "pyramide": "Pyramide"}
EKF = {"Würfel": (8, 12, 6), "Quader": (8, 12, 6), "Pyramide": (5, 8, 5)}
FIG = {"Dreieck": 3, "Viereck": 4, "Fünfeck": 5, "Sechseck": 6, "Achteck": 8}


def erkennen():
    k = R.choice(list(NAMES))
    col = R.choice(["#cfe6d6", "#f6d6a8", "#c9dcf2", "#f2c6d0", "#e8e0a8"])
    r = R.choice([28, 32, 36])
    ans = NAMES[k]
    confuse = {"wuerfel": ["Quader"], "quader": ["Würfel"], "kugel": ["Kreis"], "zylinder": ["Kegel"], "kegel": ["Pyramide"], "pyramide": ["Kegel"]}[k]
    w = confuse + [n for n in NAMES.values() if n != ans and n not in confuse]
    R.shuffle(w)
    w = confuse + w
    pic = solid_svg(k, r, col)
    why = {"Würfel": "Alle 6 Flächen sind gleich große Quadrate.", "Quader": "Er hat 6 rechteckige Flächen; nicht alle sind gleich.",
           "Kugel": "Sie ist überall rund und hat keine Ecken und Kanten.", "Zylinder": "Er hat zwei gleiche Kreise als Grund- und Deckfläche.",
           "Kegel": "Er hat einen Kreis als Grundfläche und eine Spitze.", "Pyramide": "Sie hat eine eckige Grundfläche und Dreiecke, die in einer Spitze zusammenlaufen."}[ans]
    return mcq(pic + "Wie heißt dieser Körper?", ans, w, "%s Es ist %s <b>%s</b>." % (why, "eine" if ans in ("Kugel", "Pyramide") else "ein", ans))


def eigenschaften():
    kind = R.choice(["ekf", "ekf", "ekf", "rund", "fig", "fig", "welcher"])
    if kind == "ekf":
        n = R.choice(list(EKF))
        i = R.randint(0, 2)
        word = ["Ecken", "Kanten", "Flächen"][i]
        v = EKF[n][i]
        others = [x for x in EKF[n] if x != v] + [v + 2, v - 2, 4]
        art = "eine" if n == "Pyramide" else "ein"
        extra = " (mit quadratischer Grundfläche)" if n == "Pyramide" else ""
        return mcq("Wie viele %s hat %s %s%s?" % (word, art, n, extra), str(v), [str(x) for x in others if x != v and x > 0],
                   "%s %s hat %d Ecken, %d Kanten und %d Flächen. Gefragt sind die %s: <b>%d</b>." % (art.capitalize(), n, EKF[n][0], EKF[n][1], EKF[n][2], word, v))
    if kind == "rund":
        q, a, w, e = R.choice([
            ("Welcher Körper hat keine Ecken und keine Kanten?", "Kugel", ["Würfel", "Zylinder", "Kegel"], "Die Kugel ist überall rund."),
            ("Welcher Körper hat zwei Kreise als Flächen?", "Zylinder", ["Kegel", "Kugel", "Quader"], "Der Zylinder hat oben und unten einen Kreis."),
            ("Welcher Körper hat eine Spitze und einen Kreis als Grundfläche?", "Kegel", ["Pyramide", "Zylinder", "Kugel"], "Der Kegel hat eine Spitze und eine Kreisfläche."),
            ("Welcher Körper hat 6 gleich große quadratische Flächen?", "Würfel", ["Quader", "Pyramide", "Zylinder"], "Beim Würfel sind alle Flächen gleich große Quadrate."),
            ("Welcher Körper kann in jede Richtung rollen?", "Kugel", ["Zylinder", "Kegel", "Würfel"], "Die Kugel ist überall rund und rollt in jede Richtung."),
            ("Welcher Körper kann rollen und auch stehen, ohne umzufallen, und hat keine Spitze?", "Zylinder", ["Kugel", "Kegel", "Würfel"], "Der Zylinder rollt auf der gekrümmten Fläche und steht auf einem Kreis."),
        ])
        return mcq(q, a, w, "%s Richtig: <b>%s</b>." % (e, a))
    if kind == "fig":
        n = R.choice(list(FIG))
        v = FIG[n]
        word = R.choice(["Ecken", "Seiten"])
        return mcq("Wie viele %s hat ein %s?" % (word, n), str(v), [str(x) for x in (v + 1, v - 1, v * 2, v + 2) if x != v],
                   "Ein %s hat %d Ecken und %d Seiten: <b>%d</b>." % (n, v, v, v))
    q, a, w = R.choice([
        ("Welche Figur hat 4 gleich lange Seiten und 4 rechte Winkel?", "Quadrat", ["Rechteck", "Dreieck", "Kreis"]),
        ("Welche Figur hat 4 rechte Winkel, aber nicht alle Seiten sind gleich lang?", "Rechteck", ["Quadrat", "Dreieck", "Sechseck"]),
        ("Welche Figur hat keine Ecken?", "Kreis", ["Dreieck", "Quadrat", "Rechteck"]),
        ("Welche Figur hat genau 3 Ecken?", "Dreieck", ["Viereck", "Kreis", "Fünfeck"]),
    ])
    return mcq(q, a, w, "Richtig ist das <b>%s</b>." % a if a != "Kreis" else "Richtig ist der <b>Kreis</b>.")


def bauplan():
    rows, cols = R.randint(2, 3), R.randint(2, 3)
    grid = [[R.randint(0, 3) for _ in range(cols)] for _ in range(rows)]
    if sum(sum(r) for r in grid) < 5 or sum(1 for r in grid for v in r if v == 0) > 2:
        return None
    tot = sum(sum(r) for r in grid)
    cells = sum(1 for r in grid for v in r if v)
    html = ("<table class='sn-table' style='width:auto;margin:6px 0'><tbody>%s</tbody></table>"
            % "".join("<tr>%s</tr>" % "".join("<td style='text-align:center;min-width:34px;height:30px'>%s</td>" % (v if v else "") for v in r) for r in grid))
    w = [cells, tot + 1, tot - 1, tot + 2, max(max(r) for r in grid) * cells]
    return mcq("Ein Bauplan zeigt ein Würfelgebäude von oben. Die Zahl sagt, wie viele Würfel übereinander stehen. Wie viele Würfel sind es?" + html,
               str(tot), [str(x) for x in w if x != tot and x > 0],
               "Addiere alle Zahlen im Bauplan: %s = <b>%d</b>." % (" + ".join(str(v) for r in grid for v in r if v), tot))


def bauplan_hoch():
    rows, cols = R.randint(2, 3), R.randint(2, 3)
    grid = [[R.randint(1, 4) for _ in range(cols)] for _ in range(rows)]
    mx = max(max(r) for r in grid)
    if sum(1 for r in grid for v in r if v == mx) > 1:
        return None
    html = ("<table class='sn-table' style='width:auto;margin:6px 0'><tbody>%s</tbody></table>"
            % "".join("<tr>%s</tr>" % "".join("<td style='text-align:center;min-width:34px;height:30px'>%d</td>" % v for v in r) for r in grid))
    tot = sum(sum(r) for r in grid)
    return mcq("Bauplan eines Würfelgebäudes: Wie hoch ist der höchste Turm?" + html, "%d Würfel" % mx,
               ["%d Würfel" % x for x in (tot, rows * cols, mx + 1, mx - 1) if x != mx and x > 0],
               "Die größte Zahl im Bauplan ist %d. Der höchste Turm ist <b>%d Würfel</b> hoch." % (mx, mx))


# ---------------------------------------------------------------- Würfelnetze
def roll(state, d):
    B, T, N, S, E, W = state
    if d == "E":
        return (E, W, N, S, T, B)
    if d == "W":
        return (W, E, N, S, B, T)
    if d == "N":
        return (N, S, T, B, E, W)
    return (S, N, B, T, E, W)


def is_net(cells):
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
    return len(seen) == 6 and len({s[0] for s in seen.values()}) == 6


def hexomino():
    cells = {(0, 0)}
    while len(cells) < 6:
        x, y = R.choice(sorted(cells))
        dx, dy = R.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
        cells.add((x + dx, y + dy))
    mx, my = min(c[0] for c in cells), min(c[1] for c in cells)
    cells = frozenset((x - mx, y - my) for x, y in cells)
    if max(c[0] for c in cells) > 3 or max(c[1] for c in cells) > 3:
        return None
    return cells


def nets_svg(nets):
    q = 18
    s = []
    for i, cells in enumerate(nets):
        ox = 10 + i * 96
        for x, y in cells:
            s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.5'/>" % (ox + x * q, 8 + y * q, q, q, FILL, GREEN))
        s.append(text(ox + 36, 100, "ABCD"[i], 16, col=GREEN))
    return wrap(10 + 4 * 96, 108, "".join(s), "vier Netze A bis D", lg=True)


def wuerfelnetz():
    want_net = R.random() < 0.75
    pool_good, pool_bad = [], []
    for _ in range(400):
        h = hexomino()
        if not h:
            continue
        (pool_good if is_net(h) else pool_bad).append(h)
    pool_good, pool_bad = list(dict.fromkeys(pool_good)), list(dict.fromkeys(pool_bad))
    if want_net:
        if len(pool_bad) < 3 or not pool_good:
            return None
        ans_net, others = R.choice(pool_good), R.sample(pool_bad, 3)
        q = "Welches Netz kann man zu einem Würfel falten?"
    else:
        if len(pool_good) < 3 or not pool_bad:
            return None
        ans_net, others = R.choice(pool_bad), R.sample(pool_good, 3)
        q = "Drei Netze ergeben einen Würfel. Welches Netz ergibt <b>keinen</b> Würfel?"
    nets = others + [ans_net]
    R.shuffle(nets)
    k = nets.index(ans_net)
    letters = "ABCD"
    return mcq(nets_svg(nets) + q, letters[k], [letters[i] for i in range(4) if i != k],
               ("Netz %s lässt sich zu einem Würfel falten: Beim Falten liegt jede der 6 Flächen an einer anderen Stelle." if want_net else
                "Bei Netz %s würden beim Falten zwei Flächen übereinanderliegen, dafür fehlt eine andere Fläche.") % letters[k])


UMWELT = [
    ("ein Fußball", "Kugel"), ("eine Orange", "Kugel"), ("eine Konservendose", "Zylinder"), ("eine Kerze", "Zylinder"),
    ("ein Schuhkarton", "Quader"), ("ein Ziegelstein", "Quader"), ("ein Spielwürfel", "Würfel"), ("ein Zuckerwürfel", "Würfel"),
    ("eine Eiswaffel", "Kegel"), ("ein Partyhut", "Kegel"), ("ein Verkehrshütchen", "Kegel"), ("eine Milchtüte", "Quader"),
    ("eine Murmel", "Kugel"), ("eine Küchenrolle", "Zylinder"),
]
FLACH = [
    ("ein Vorfahrt-achten-Schild", "Dreieck"), ("eine Tafel im Klassenzimmer", "Rechteck"), ("ein Teller, von oben gesehen", "Kreis"),
    ("ein Schachbrett", "Quadrat"), ("eine Pizza", "Kreis"), ("ein Stoppschild", "Achteck"),
]
ABDRUCK = [("Würfel", "Quadrat"), ("Zylinder", "Kreis"), ("Kegel", "Kreis"), ("Quader", "Rechteck"), ("Pyramide", "Quadrat")]


def umwelt():
    kind = R.choice(["koerper", "koerper", "flach", "abdruck"])
    if kind == "koerper":
        thing, ans = R.choice(UMWELT)
        w = [x for x in ["Kugel", "Zylinder", "Quader", "Würfel", "Kegel", "Pyramide"] if x != ans]
        R.shuffle(w)
        gen = {"Kugel": "einer Kugel", "Zylinder": "eines Zylinders", "Quader": "eines Quaders", "Würfel": "eines Würfels", "Kegel": "eines Kegels", "Pyramide": "einer Pyramide"}[ans]
        return mcq("Welche Körperform hat %s?" % thing, ans, w, "%s hat die Form %s: <b>%s</b>." % (thing[0].upper() + thing[1:], gen, ans))
    if kind == "flach":
        thing, ans = R.choice(FLACH)
        w = [x for x in ["Dreieck", "Rechteck", "Kreis", "Quadrat", "Achteck", "Sechseck"] if x != ans]
        R.shuffle(w)
        return mcq("Welche Form hat %s?" % thing, ans, w, "Die Form ist ein <b>%s</b>." % ans if ans != "Kreis" else "Die Form ist ein <b>Kreis</b>.")
    k, f = R.choice(ABDRUCK)
    art = "eine" if k == "Pyramide" else "einen"
    extra = " mit quadratischer Grundfläche" if k == "Pyramide" else ""
    w = [x for x in ["Quadrat", "Kreis", "Rechteck", "Dreieck"] if x != f]
    return mcq("Du stellst %s %s%s auf ein Blatt und fährst die Grundfläche mit dem Stift nach. Welche Figur entsteht?" % (art, k, extra), f, w,
               "Die Grundfläche ist ein <b>%s</b>." % f)


def main():
    seen = set()
    sets = [
        ("Körper erkennen", mix(R, seen, [(erkennen, 20)])),
        ("Ecken, Kanten und Flächen", mix(R, seen, [(eigenschaften, 20)])),
        ("Baupläne von Würfelgebäuden", mix(R, seen, [(bauplan, 14), (bauplan_hoch, 6)])),
        ("Würfelnetze", mix(R, seen, [(wuerfelnetz, 20)])),
        ("Körper und Figuren in der Umwelt", mix(R, seen, [(umwelt, 20)])),
    ]
    body = lesson(
        ["<b>Körper</b> sind räumlich: Würfel, Quader, Kugel, Zylinder, Kegel und Pyramide. <b>Figuren</b> sind flach: Quadrat, Rechteck, Dreieck, Kreis.",
         "Ein Würfel und ein Quader haben je 8 Ecken, 12 Kanten und 6 Flächen. Beim Würfel sind alle Flächen gleich große Quadrate.",
         "Ein <b>Bauplan</b> zeigt ein Würfelgebäude von oben. Die Zahlen sagen, wie viele Würfel übereinander stehen.",
         "Ein <b>Würfelnetz</b> hat 6 Quadrate. Beim Falten darf keine Fläche doppelt liegen."],
        [example("Wie viele Würfel hat der Bauplan 2 | 1 / 3 | 1?", ["2 + 1 + 3 + 1 = 7"], "7 Würfel")],
        [["Würfel und Quader verwechseln", "Würfel: alle Flächen gleich große Quadrate"],
         ["Ecken und Kanten verwechseln", "Kanten sind die Linien, Ecken die Punkte"],
         ["Beim Bauplan nur die Felder zählen", "Die Zahlen in den Feldern addieren"]],
        extra=table(["Körper", "Ecken", "Kanten", "Flächen"], [["Würfel", "8", "12", "6"], ["Quader", "8", "12", "6"], ["Pyramide (quadratisch)", "5", "8", "5"], ["Kugel", "0", "0", "1"]]))
    faq = [
        {"q": "Was ist der Unterschied zwischen Körper und Figur?", "a": "Körper sind dreidimensional und man kann sie anfassen (Würfel, Kugel). Figuren sind flach und liegen in einer Ebene (Quadrat, Kreis)."},
        {"q": "Wie viele Würfelnetze gibt es?", "a": "Es gibt genau 11 verschiedene Würfelnetze. Kinder können sie durch Ausschneiden und Falten selbst herausfinden."},
        {"q": "Was ist ein Bauplan?", "a": "Die Ansicht eines Würfelgebäudes von oben. In jedem Feld steht, wie viele Würfel übereinander stehen."},
        {"q": "Hat eine Kugel eine Fläche?", "a": "Ja, eine gekrümmte Fläche. Sie hat aber keine Ecken und keine Kanten."},
    ]
    make_unit(R, "koerper-und-figuren", "R",
              "Die Schülerinnen und Schüler erkennen, benennen und beschreiben Körper und ebene Figuren, untersuchen Würfelnetze und stellen Würfelgebäude nach Bauplänen dar (Zusammenfassung).",
              "Körper und Figuren: Würfel, Quader, Kugel und mehr",
              "Geometrische Körper Klasse 3 – Würfelnetze, Baupläne, Arbeitsblätter mit Lösungen",
              "Körper und Figuren",
              "Geometrie Klasse 3: Körper erkennen (Würfel, Quader, Kugel, Zylinder, Kegel, Pyramide), Ecken, Kanten, Flächen, Baupläne und Würfelnetze. 100 Aufgaben mit Lösungen, kostenlos.",
              "Würfel: 8 Ecken, 12 Kanten, 6 Flächen.",
              "Ein Würfelnetz hat 6 Quadrate, und keine Fläche liegt doppelt.",
              body, faq, sets, 15)


if __name__ == "__main__":
    main()
