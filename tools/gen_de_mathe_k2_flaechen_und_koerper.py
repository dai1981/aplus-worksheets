# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 2: Flächen und Körper（Leitidee Raum und Form）
  python3 tools/gen_de_mathe_k2_flaechen_und_koerper.py
Ebene Figuren erkennen, Ecken und Seiten, Figuren zählen, Körper erkennen, Körper in der Umwelt, Würfelgebäude.
Die Körper- und Bauplan-Aufgaben kommen aus Klasse 3 (gen_de_mathe_k3_koerper_und_figuren) mit eigenem Zufall.
Fehler: Quadrat und Rechteck verwechselt, Kugel und Kreis verwechselt, verdeckte Würfel nicht mitgezählt.
"""
import random
from de_common import mcq, lesson, example, make_unit, mix, wrap, table
from k_pics import shape, shape_rot, M
from ws_common import svg_wrap, fig, text, GREEN
import gen_de_mathe_k3_koerper_und_figuren as k3

R = random.Random(49215)
k3.R = random.Random(49315)

NAME = {"circle": "Kreis", "square": "Quadrat", "rectangle": "Rechteck", "triangle": "Dreieck", "hexagon": "Sechseck"}
ECKEN = {"circle": 0, "square": 4, "rectangle": 4, "triangle": 3, "hexagon": 6}
COLS = ["red", "blue", "yellow", "green"]


def one(kind, col, r, rot):
    W = int(2 * r * 1.4 + 2 * M)
    return fig(svg_wrap(W, W, shape_rot(kind, W / 2, W / 2, r, col, rot), "eine Figur"))


def figur():
    k = R.choice(list(NAME))
    col = R.choice(COLS)
    r = R.choice([30, 36, 42])
    rot = R.choice([0, 0, 15, 30, 45]) if k in ("square", "rectangle", "triangle") else 0
    ans = NAME[k]
    conf = {"Quadrat": ["Rechteck", "Dreieck"], "Rechteck": ["Quadrat", "Dreieck"], "Kreis": ["Kugel", "Quadrat"],
            "Dreieck": ["Viereck", "Sechseck"], "Sechseck": ["Fünfeck", "Achteck"]}[ans]
    rest = [n for n in NAME.values() if n != ans and n not in conf]
    return mcq(one(k, col, r, rot) + "Wie heißt diese Figur?", ans, conf + rest,
               {"Quadrat": "4 gleich lange Seiten und 4 rechte Ecken: ein <b>Quadrat</b>.",
                "Rechteck": "4 rechte Ecken, zwei lange und zwei kurze Seiten: ein <b>Rechteck</b>.",
                "Kreis": "Rund und ohne Ecken: ein <b>Kreis</b>. (Eine Kugel ist ein Körper.)",
                "Dreieck": "3 Ecken und 3 Seiten: ein <b>Dreieck</b>.",
                "Sechseck": "6 Ecken und 6 Seiten: ein <b>Sechseck</b>."}[ans])


def zaehlen():
    kind = R.choice(["ecken", "ecken", "mix"])
    if kind == "ecken":
        k = R.choice(["square", "rectangle", "triangle", "hexagon"])
        word = R.choice(["Ecken", "Seiten"])
        v = ECKEN[k]
        col = R.choice(COLS)
        return mcq(one(k, col, R.choice([30, 36, 42]), R.choice([0, 20, 40]) if k != "hexagon" else 0) + "Wie viele %s hat diese Figur?" % word, str(v),
                   [str(x) for x in (v + 1, v - 1, v + 2, 2 * v)], "Ein %s hat %d Ecken und %d Seiten: <b>%d</b>." % (NAME[k], v, v, v))
    items = []
    target = R.choice(["triangle", "circle", "square", "rectangle"])
    n = R.randint(2, 6)
    items += [(target, R.choice(COLS)) for _ in range(n)]
    others = [k for k in NAME if k != target and not (target == "square" and k == "rectangle") and not (target == "rectangle" and k == "square")]
    items += [(R.choice(others), R.choice(COLS)) for _ in range(R.randint(4, 15 - n))]
    rnd = random.Random(R.randint(1, 10 ** 6))
    cols, rows = 5, 3
    cells = rnd.sample([(r, c) for r in range(rows) for c in range(cols)], len(items))
    sp = 52
    s = [shape(k, M + sp / 2 + c * sp + rnd.uniform(-4, 4), M + sp / 2 + r * sp + rnd.uniform(-4, 4), 17, col) for (r, c), (k, col) in zip(cells, items)]
    pic = fig(svg_wrap(2 * M + cols * sp, 2 * M + rows * sp, "".join(s), "verschiedene Figuren"))
    pl = {"triangle": "Dreiecke", "circle": "Kreise", "square": "Quadrate", "rectangle": "Rechtecke"}[target]
    return mcq(pic + "Wie viele %s siehst du?" % pl, str(n), [str(n + 1), str(n - 1), str(len(items))],
               "Zähle nur die %s: <b>%d</b>." % (pl, n))


def koerper():
    return k3.erkennen()


def umwelt():
    if R.random() < 0.3:
        it = k3.eigenschaften()
        return it if "Welcher Körper" in it["q"] else None
    return k3.umwelt()


def bau():
    return k3.bauplan() if R.random() < 0.7 else k3.bauplan_hoch()


def main():
    seen = set()
    sets = [
        ("Ebene Figuren erkennen", mix(R, seen, [(figur, 20)])),
        ("Ecken, Seiten und Zählen", mix(R, seen, [(zaehlen, 20)])),
        ("Körper erkennen", mix(R, seen, [(koerper, 20)])),
        ("Körper in der Umwelt", mix(R, seen, [(umwelt, 20)])),
        ("Würfelgebäude", mix(R, seen, [(bau, 20)])),
    ]
    body = lesson(
        ["<b>Flächen</b> (ebene Figuren) sind flach: Dreieck, Viereck, Quadrat, Rechteck und Kreis.",
         "Ein <b>Quadrat</b> hat 4 gleich lange Seiten. Ein <b>Rechteck</b> hat zwei lange und zwei kurze Seiten.",
         "<b>Körper</b> kann man anfassen: Würfel, Quader, Kugel, Zylinder, Kegel und Pyramide.",
         "Ein Kreis ist eine Fläche, eine Kugel ist ein Körper."],
        [example("Eine Figur mit 3 Ecken und 3 Seiten", ["3 Ecken"], "Dreieck"),
         example("Ein Ball", ["überall rund, rollt in jede Richtung"], "Kugel")],
        [["Ein gedrehtes Quadrat ist kein Quadrat mehr", "Es bleibt ein Quadrat"],
         ["Kugel und Kreis verwechseln", "Kreis = flach, Kugel = Körper"],
         ["Nur die sichtbaren Würfel zählen", "Auch verdeckte Würfel mitzählen"]],
        extra=table(["Figur", "Ecken", "Seiten"], [["Dreieck", "3", "3"], ["Quadrat", "4", "4"], ["Rechteck", "4", "4"], ["Kreis", "0", "keine geraden Seiten"]]))
    faq = [
        {"q": "Was ist der Unterschied zwischen Flächen und Körpern?", "a": "Flächen sind flach wie ein Blatt Papier (Dreieck, Kreis). Körper haben eine Höhe und man kann sie anfassen (Würfel, Kugel)."},
        {"q": "Ist ein Quadrat auch ein Rechteck?", "a": "Ja. Ein Quadrat ist ein besonderes Rechteck, bei dem alle vier Seiten gleich lang sind. In Klasse 2 unterscheidet man meist nur die Namen."},
        {"q": "Welche Körper lernen Kinder in Klasse 2?", "a": "Würfel, Quader, Kugel, Zylinder, Kegel und Pyramide. Sie suchen sie auch in der Umwelt, zum Beispiel einen Ball oder eine Dose."},
        {"q": "Was ist ein Bauplan?", "a": "Ein Bauplan zeigt ein Würfelgebäude von oben. Die Zahlen sagen, wie viele Würfel übereinander stehen."},
    ]
    make_unit(R, "flaechen-und-koerper", "R",
              "Die Schülerinnen und Schüler erkennen und benennen ebene Figuren und geometrische Körper, beschreiben Ecken und Seiten, finden Formen in der Umwelt und bauen Würfelgebäude nach Bauplänen (Zusammenfassung).",
              "Flächen und Körper",
              "Flächen und Körper Klasse 2 – Arbeitsblätter mit Lösungen",
              "Flächen und Körper",
              "Flächen und Körper für Klasse 2: Dreieck, Quadrat, Rechteck und Kreis, Ecken und Seiten, Würfel, Kugel, Zylinder, Körper in der Umwelt und Würfelgebäude. 100 Übungsaufgaben mit Lösungen, kostenlos.",
              "Flächen sind flach. Körper kann man anfassen.",
              "Kreis = Fläche, Kugel = Körper",
              body, faq, sets, 15, grade="klasse-2")


if __name__ == "__main__":
    main()
