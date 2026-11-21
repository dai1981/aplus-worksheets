# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 3: Achsensymmetrie（Leitidee Raum und Form）
  python3 tools/gen_de_mathe_k3_achsensymmetrie.py
Symmetrische Figuren erkennen, symmetrische Buchstaben, Spiegelbild ergänzen, Spiegelpunkte, Anzahl der Spiegelachsen.
Fehler: Hälfte verschoben statt gespiegelt, nur „fast“ symmetrisch übersehen, Abstand zur Achse falsch übertragen.
"""
import random
from de_common import mcq, lesson, example, make_unit, mix, wrap
from ws_common import line, text, INK, GREEN, FILL, RED

R = random.Random(49016)
COLS, ROWS = 6, 5
Q = 15


def half():
    cells = set()
    while len(cells) < R.randint(4, 7):
        cells.add((R.randint(0, 2), R.randint(0, ROWS - 1)))
    if not any(c[0] == 2 for c in cells):
        return None
    return cells


def mirror(cells):
    return set(cells) | {(COLS - 1 - x, y) for x, y in cells}


def grid(ox, oy, cells, axis=True, partial=None):
    s = []
    for x in range(COLS + 1):
        s.append(line(ox + x * Q, oy, ox + x * Q, oy + ROWS * Q, "#c9d6df", 0.8))
    for y in range(ROWS + 1):
        s.append(line(ox, oy + y * Q, ox + COLS * Q, oy + y * Q, "#c9d6df", 0.8))
    for x, y in cells:
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='0.8'/>" % (ox + x * Q, oy + y * Q, Q, Q, FILL, GREEN))
    if axis:
        s.append(line(ox + COLS * Q / 2.0, oy - 6, ox + COLS * Q / 2.0, oy + ROWS * Q + 6, RED, 2, " stroke-dasharray='5 3'"))
    return "".join(s)


def four(figs, axis=True):
    s = []
    for i, c in enumerate(figs):
        ox = 10 + i * 112
        s.append(grid(ox, 10, c, axis))
        s.append(text(ox + COLS * Q / 2.0, 10 + ROWS * Q + 24, "ABCD"[i], 16, col=GREEN))
    return wrap(10 + 4 * 112, 10 + ROWS * Q + 32, "".join(s), "vier Figuren A bis D", lg=True)


def broken(sym):
    """fast symmetrisch: ein Kästchen rechts verändert"""
    c = set(sym)
    right = [p for p in c if p[0] >= 3]
    x, y = R.choice(right)
    c.discard((x, y))
    cand = [(xx, yy) for xx in range(3, COLS) for yy in range(ROWS) if (xx, yy) not in c and (COLS - 1 - xx, yy) not in c]
    if not cand:
        return None
    c.add(R.choice(cand))
    return c


def shifted(h):
    """Hälfte verschoben statt gespiegelt"""
    return set(h) | {(x + 3, y) for x, y in h}


def welche():
    hs = [half() for _ in range(4)]
    if not all(hs):
        return None
    good = mirror(hs[0])
    bads = [broken(mirror(hs[1])), shifted(hs[2]), broken(mirror(hs[3]))]
    if not all(bads) or any(b == mirror({(x, y) for x, y in b if x < 3}) for b in bads):
        return None
    figs = bads + [good]
    R.shuffle(figs)
    k = figs.index(good)
    return mcq(four(figs) + "Welche Figur ist achsensymmetrisch zur roten Linie?", "ABCD"[k], ["ABCD"[i] for i in range(4) if i != k],
               "Nur bei Figur %s sind die Kästchen links und rechts genau gleich weit von der Achse entfernt (Spiegelbild)." % "ABCD"[k])


def ergaenzen():
    h = half()
    if not h:
        return None
    good = mirror(h)
    sh = shifted(h)
    near = broken(good)
    flipped = set(h) | {(COLS - 1 - x, ROWS - 1 - y) for x, y in h}
    opts = [good, sh, near, flipped]
    if not near or len({frozenset(o) for o in opts}) < 4:
        return None
    pic_half = wrap(COLS * Q + 20, ROWS * Q + 20, grid(10, 10, h), "halbe Figur mit Spiegelachse")
    R.shuffle(opts)
    k = opts.index(good)
    return mcq(pic_half + "So sieht die linke Hälfte aus. Welches Bild zeigt die richtig ergänzte Figur?" + four(opts), "ABCD"[k],
               ["ABCD"[i] for i in range(4) if i != k],
               "Jedes Kästchen wird an der Achse gespiegelt: gleicher Abstand, andere Seite. Richtig ist <b>%s</b>." % "ABCD"[k])


SENK = list("AHIMOTUVWXY")
WAAG = list("BCDEHIKOX")
NONE = list("FGJLNPQRSZ")


def buchstabe():
    kind = R.choice(["senk", "senk", "waag", "nicht"])
    if kind == "senk":
        a = R.choice(SENK)
        w = R.sample(NONE, 3)
        q = "Welcher Buchstabe hat eine <b>senkrechte</b> Spiegelachse? %s" % ", ".join(sorted([a] + w))
        e = "Faltest du %s entlang einer senkrechten Linie in der Mitte, liegen beide Hälften genau aufeinander. Richtig: <b>%s</b>." % (a, a)
    elif kind == "waag":
        a = R.choice([x for x in WAAG if x not in SENK])
        w = R.sample(NONE, 3)
        q = "Welcher Buchstabe hat eine <b>waagerechte</b> Spiegelachse? %s" % ", ".join(sorted([a] + w))
        e = "Bei %s passen die obere und die untere Hälfte genau aufeinander. Richtig: <b>%s</b>." % (a, a)
    else:
        a = R.choice(NONE)
        w = R.sample(SENK + [x for x in WAAG if x not in SENK], 3)
        q = "Welcher Buchstabe ist <b>nicht</b> achsensymmetrisch? %s" % ", ".join(sorted([a] + w))
        e = "%s hat keine Spiegelachse. Die anderen Buchstaben kann man so falten, dass die Hälften aufeinanderpassen. Richtig: <b>%s</b>." % (a, a)
    return mcq(q, a, w, e)


def spiegelpunkt():
    kind = R.choice(["seite", "abstand", "gitter"])
    if kind == "seite":
        n = R.randint(1, 6)
        side = R.choice(["links", "rechts"])
        other = "rechts" if side == "links" else "links"
        ans = "%d %s %s von der Achse" % (n, "Kästchen", other)
        w = ["%d Kästchen %s von der Achse" % (n, side), "%d Kästchen %s von der Achse" % (n + 1, other), "%d Kästchen %s von der Achse" % (2 * n, other)]
        return mcq("Ein Punkt liegt %d Kästchen %s von einer senkrechten Spiegelachse. Wo liegt sein Spiegelpunkt?" % (n, side), ans, w,
                   "Der Spiegelpunkt hat den gleichen Abstand, aber auf der anderen Seite: <b>%s</b>." % ans)
    if kind == "abstand":
        n = R.randint(1, 7)
        return mcq("Ein Punkt liegt %d Kästchen von der Spiegelachse entfernt. Wie weit ist er von seinem Spiegelpunkt entfernt?" % n,
                   "%d Kästchen" % (2 * n), ["%d Kästchen" % x for x in (n, n + 1, 2 * n + 2)],
                   "Bis zur Achse %d Kästchen, auf der anderen Seite noch einmal %d: zusammen <b>%d Kästchen</b>." % (n, n, 2 * n))
    x = R.randint(0, 2)
    y = R.randint(0, ROWS - 1)
    mx = COLS - 1 - x
    s = grid(10, 10, {(x, y)})
    for i in range(COLS):
        s += text(10 + i * Q + Q / 2.0, 10 + ROWS * Q + 14, str(i + 1), 10, weight=400)
    pic = wrap(COLS * Q + 20, ROWS * Q + 30, s, "Gitter mit einem Kästchen und Spiegelachse")
    return mcq(pic + "In welcher Spalte liegt das gespiegelte Kästchen? (Die Spalten sind unten nummeriert.)", "Spalte %d" % (mx + 1),
               ["Spalte %d" % c for c in (x + 4, mx, mx + 2 if mx + 2 <= COLS else x + 1, x + 1) if c != mx + 1 and 1 <= c <= COLS],
               "Von der Achse aus gezählt ist es das %d. Kästchen links. Das Spiegelbild ist das %d. Kästchen rechts der Achse: <b>Spalte %d</b>." % (3 - x, 3 - x, mx + 1))


ACHSEN = [
    ("ein Quadrat", "4"), ("ein Rechteck, das kein Quadrat ist", "2"), ("ein gleichseitiges Dreieck", "3"),
    ("ein Kreis", "unendlich viele"), ("ein Herz", "1"), ("ein Schmetterling", "1"), ("ein regelmäßiges Sechseck", "6"),
    ("der Buchstabe H", "2"), ("der Buchstabe A", "1"), ("der Buchstabe F", "keine"), ("die Ziffer 8", "2"), ("die Ziffer 3", "1"),
]


def achsen():
    thing, ans = R.choice(ACHSEN)
    w = [x for x in ["keine", "1", "2", "3", "4", "6", "unendlich viele"] if x != ans]
    R.shuffle(w)
    near = {"4": ["2", "8"], "2": ["4", "1"], "3": ["1", "6"], "unendlich viele": ["1", "4"], "1": ["2", "keine"], "6": ["3", "12"], "keine": ["1", "2"]}[ans]
    return mcq("Wie viele Spiegelachsen hat %s?" % thing, ans, near + w, "%s hat <b>%s</b> Spiegelachse%s." % (thing[0].upper() + thing[1:], ans, "" if ans == "1" else "n"))


def main():
    seen = set()
    sets = [
        ("Welche Figur ist symmetrisch?", mix(R, seen, [(welche, 20)])),
        ("Symmetrische Buchstaben", mix(R, seen, [(buchstabe, 20)])),
        ("Das Spiegelbild ergänzen", mix(R, seen, [(ergaenzen, 20)])),
        ("Spiegelpunkte", mix(R, seen, [(spiegelpunkt, 20)])),
        ("Spiegelachsen zählen", mix(R, seen, [(achsen, 10), (buchstabe, 5), (spiegelpunkt, 5)])),
    ]
    body = lesson(
        ["Eine Figur ist <b>achsensymmetrisch</b>, wenn man sie so falten kann, dass beide Hälften genau aufeinanderliegen.",
         "Die Faltlinie heißt <b>Spiegelachse</b> (Symmetrieachse).",
         "Jeder Punkt und sein Spiegelpunkt sind <b>gleich weit</b> von der Achse entfernt, aber auf verschiedenen Seiten.",
         "Manche Figuren haben mehrere Spiegelachsen: Ein Quadrat hat 4, ein Rechteck 2, ein Kreis unendlich viele."],
        [example("Ein Kästchen liegt 2 Kästchen links von der Achse. Wo liegt das Spiegelbild?", ["gleicher Abstand: 2 Kästchen", "andere Seite: rechts"], "2 Kästchen rechts von der Achse")],
        [["Die Hälfte nur verschieben", "Spiegeln: Was links außen ist, kommt rechts nach außen"],
         ["Abstand zur Achse falsch zählen", "Kästchen von der Achse aus zählen, nicht vom Rand"],
         ["Ein Rechteck hat 4 Spiegelachsen", "Nur 2: die Diagonalen sind keine Spiegelachsen"]])
    faq = [
        {"q": "Wie prüft man Symmetrie am einfachsten?", "a": "Mit einem Spiegel auf der Achse oder durch Falten: Passen beide Hälften genau aufeinander, ist die Figur achsensymmetrisch."},
        {"q": "Warum sind die Diagonalen eines Rechtecks keine Spiegelachsen?", "a": "Faltet man ein Rechteck entlang der Diagonale, liegen die Ecken nicht aufeinander. Nur beim Quadrat sind die Diagonalen Spiegelachsen."},
        {"q": "Welche Buchstaben sind symmetrisch?", "a": "Zum Beispiel A, H, M, O, T, U, V, W, X, Y (senkrechte Achse) und B, C, D, E, K (waagerechte Achse, je nach Schrift)."},
        {"q": "Braucht man Karopapier?", "a": "Ja, auf Karopapier lassen sich Abstände zur Achse gut abzählen und Spiegelbilder genau zeichnen."},
    ]
    make_unit(R, "achsensymmetrie", "R",
              "Die Schülerinnen und Schüler erkennen achsensymmetrische Figuren, bestimmen Spiegelachsen und ergänzen bzw. zeichnen Spiegelbilder auf Karopapier (Zusammenfassung).",
              "Achsensymmetrie: Spiegelachse und Spiegelbild",
              "Achsensymmetrie Klasse 3 – Spiegelbilder, Arbeitsblätter mit Lösungen",
              "Achsensymmetrie",
              "Achsensymmetrie für Klasse 3: symmetrische Figuren erkennen, Spiegelbilder ergänzen, Spiegelpunkte, symmetrische Buchstaben und Spiegelachsen zählen. 100 Aufgaben mit Lösungen, kostenlos.",
              "Gleicher Abstand zur Achse, andere Seite.",
              "Achsensymmetrisch heißt: Beim Falten passen beide Hälften genau aufeinander.",
              body, faq, sets, 16)


if __name__ == "__main__":
    main()
