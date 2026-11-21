# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 1: Lage und Richtung（Leitidee Raum und Form）
  python3 tools/gen_de_mathe_k1_lage_und_richtung.py
Über, unter, neben; vor, hinter; oben und unten im Regal; links und rechts; Wege auf dem Gitter.
Fehler: links und rechts verwechselt, „über“ und „auf“ verwechselt, beim Weg Schritte falsch gezählt.
"""
import random
from de_common import mcq, lesson, example, make_unit, mix
from de_k2 import de, KINDS, DING
from k_pics import table_scene_svg, box_scene_svg, shelf_svg, kinds_row_svg
from ws_common import svg_wrap, fig, text, line, GREEN, INK, RED

R = random.Random(49415)
ART = {"apple": "der Apfel", "star": "der Stern", "ball": "der Ball", "button": "der Knopf", "fish": "der Fisch", "flower": "die Blume",
       "heart": "das Herz", "duck": "die Ente", "cup": "der Becher", "bug": "der Käfer"}
DAT = {"apple": "dem Apfel", "star": "dem Stern", "ball": "dem Ball", "button": "dem Knopf", "fish": "dem Fisch", "flower": "der Blume",
       "heart": "dem Herz", "duck": "der Ente", "cup": "dem Becher", "bug": "dem Käfer"}


def tisch():
    k = R.choice(KINDS)
    rel = R.choice(["above", "below", "beside", "beside-left"])
    pic = de(table_scene_svg(k, rel), "ein Tisch und %s" % ART[k].split()[1])
    ans = {"above": "über dem Tisch", "below": "unter dem Tisch", "beside": "neben dem Tisch", "beside-left": "neben dem Tisch"}[rel]
    return mcq(pic + "Wo ist %s?" % ART[k], ans, [x for x in ("über dem Tisch", "unter dem Tisch", "neben dem Tisch", "hinter dem Tisch") if x != ans],
               "Schau genau, wo %s im Bild ist: <b>%s</b>." % (ART[k], ans))


def kiste():
    k = R.choice(KINDS)
    rel = R.choice(["front", "behind", "beside", "above"])
    pic = de(box_scene_svg(k, rel), "eine Kiste und %s" % ART[k].split()[1])
    ans = {"front": "vor der Kiste", "behind": "hinter der Kiste", "beside": "neben der Kiste", "above": "über der Kiste"}[rel]
    return mcq(pic + "Wo ist %s?" % ART[k], ans, [x for x in ("vor der Kiste", "hinter der Kiste", "neben der Kiste", "über der Kiste") if x != ans],
               {"front": "Ein Teil der Kiste ist verdeckt: <b>vor der Kiste</b>.", "behind": "Die Kiste verdeckt einen Teil: <b>hinter der Kiste</b>.",
                "beside": "Daneben auf dem Boden: <b>neben der Kiste</b>.", "above": "Oberhalb der Kiste: <b>über der Kiste</b>."}[rel])


def regal():
    ks = R.sample(KINDS, R.choice([3, 4]))
    n = len(ks)
    pic = de(shelf_svg(ks), "ein Regal mit %d Fächern" % n)
    kind = R.choice(["oben", "unten", "ueber", "unter"])
    j = None
    if kind == "oben":
        i = 0
        q = "Was liegt im obersten Fach?"
    elif kind == "unten":
        i = n - 1
        q = "Was liegt im untersten Fach?"
    elif kind == "ueber":
        j = R.randint(1, n - 1)
        i = j - 1
        q = "Was liegt direkt über %s?" % DAT[ks[j]]
    else:
        j = R.randint(0, n - 2)
        i = j + 1
        q = "Was liegt direkt unter %s?" % DAT[ks[j]]
    ans = ART[ks[i]].split()[1]
    others = [ART[x].split()[1] for k2, x in enumerate(ks) if k2 != i and k2 != j]
    rest = [DING[x][0] for x in KINDS if x not in ks]
    return mcq(pic + q, ans, others + R.sample(rest, 2), "<b>%s</b>." % (ART[ks[i]][0].upper() + ART[ks[i]][1:]))


def links_rechts():
    ks = R.sample(KINDS, 5)
    pic = de(kinds_row_svg(ks), "eine Reihe: " + ", ".join(DING[k][0] for k in ks))
    j = R.randint(1, 3)
    side = R.choice(["links", "rechts", "ganz links", "ganz rechts"])
    if side == "links":
        i, q = j - 1, "Was ist direkt links neben %s?" % DAT[ks[j]]
    elif side == "rechts":
        i, q = j + 1, "Was ist direkt rechts neben %s?" % DAT[ks[j]]
    elif side == "ganz links":
        i, q = 0, "Was ist ganz links?"
    else:
        i, q = 4, "Was ist ganz rechts?"
    ans = DING[ks[i]][0]
    mirror = {"links": j + 1, "rechts": j - 1, "ganz links": 4, "ganz rechts": 0}[side]
    others = [DING[ks[mirror]][0]] + [DING[ks[x]][0] for x in range(5) if x not in (i, mirror, j)]
    return mcq(pic + q, ans, others, "Schau %s: <b>%s</b>." % ("nach links" if "links" in side else "nach rechts", ans))


def weg():
    W, H, c = 5, 4, 40
    sx, sy = R.randint(0, W - 1), R.randint(0, H - 1)
    dx, dy = R.randint(-3, 3), R.randint(-2, 2)
    tx, ty = sx + dx, sy + dy
    if not (0 <= tx < W and 0 <= ty < H) or (dx == 0 and dy == 0):
        return None
    letters = {}
    cells = [(x, y) for x in range(W) for y in range(H) if (x, y) not in ((sx, sy),)]
    pick = R.sample([p for p in cells if p != (tx, ty)], 3) + [(tx, ty)]
    R.shuffle(pick)
    for ch, p in zip("ABCD", pick):
        letters[p] = ch
    s = []
    for i in range(W + 1):
        s.append(line(10 + i * c, 10, 10 + i * c, 10 + H * c, "#bcd6e6", 1.5))
    for j in range(H + 1):
        s.append(line(10, 10 + j * c, 10 + W * c, 10 + j * c, "#bcd6e6", 1.5))
    s.append("<circle cx='%d' cy='%d' r='12' fill='%s'/>" % (10 + sx * c + c / 2, 10 + sy * c + c / 2, RED))
    for (x, y), ch in letters.items():
        s.append(text(10 + x * c + c / 2, 10 + y * c + c / 2 + 7, ch, 20, col=GREEN))
    pic = fig(svg_wrap(W * c + 20, H * c + 20, "".join(s), "Gitter mit rotem Punkt und Buchstaben A bis D"))
    parts = []
    if dx:
        parts.append("%d nach %s" % (abs(dx), "rechts" if dx > 0 else "links"))
    if dy:
        parts.append("%d nach %s" % (abs(dy), "unten" if dy > 0 else "oben"))
    ans = letters[(tx, ty)]
    return mcq(pic + "Starte beim roten Punkt. Gehe %s. Wo kommst du an?" % " und dann ".join(parts), ans, [c for c in "ABCD" if c != ans],
               "%s: Du kommst bei <b>%s</b> an." % (", dann ".join(p[0].upper() + p[1:] if k == 0 else p for k, p in enumerate(parts)), ans))


def main():
    seen = set()
    sets = [
        ("Über, unter, neben", mix(R, seen, [(tisch, 20)])),
        ("Vor, hinter, neben", mix(R, seen, [(kiste, 20)])),
        ("Oben und unten im Regal", mix(R, seen, [(regal, 20)])),
        ("Links und rechts", mix(R, seen, [(links_rechts, 20)])),
        ("Wege auf dem Gitter", mix(R, seen, [(weg, 20)])),
    ]
    body = lesson(
        ["Mit Wörtern wie <b>über, unter, neben, vor, hinter</b> sagst du, wo etwas ist.",
         "Was <b>vor</b> etwas steht, verdeckt es ein bisschen. Was <b>hinter</b> etwas steht, wird verdeckt.",
         "Links und rechts: Die meisten Kinder schreiben mit der rechten Hand.",
         "Bei einem Weg zählst du die Schritte genau: 2 nach rechts, 1 nach oben."],
        [example("Der Ball liegt unter dem Tisch", ["Tischplatte ist oben, Ball ist darunter"], "unter dem Tisch"),
         example("Start, dann 2 nach rechts und 1 nach unten", ["2 Felder rechts", "1 Feld runter"], "Ziel gefunden")],
        [["Links und rechts verwechseln", "Hand zum Schreiben zeigt meist nach rechts"],
         ["Vor und hinter verwechseln", "Was verdeckt ist, steht hinten"],
         ["Beim Weg das Startfeld mitzählen", "Erst beim nächsten Feld anfangen zu zählen"]])
    faq = [
        {"q": "Warum lernen Kinder Lagebeziehungen in Mathe?", "a": "Sie sind die Grundlage für Geometrie, für das Lesen von Plänen und für die Sprache im Matheunterricht."},
        {"q": "Wie übt man links und rechts?", "a": "Mit Spielen wie „Hebe die rechte Hand“, mit einem Armband an einem Handgelenk oder beim Abbiegen auf dem Schulweg."},
        {"q": "Was sind Wege auf dem Gitter?", "a": "Man bewegt sich Feld für Feld nach rechts, links, oben oder unten. Das ist eine Vorstufe für Pläne und Koordinaten."},
        {"q": "Wie spielt man das zu Hause?", "a": "Gegenstände verstecken und den Weg beschreiben: „Drei Schritte vor, dann links, unter dem Stuhl.“"},
    ]
    make_unit(R, "lage-und-richtung", "R",
              "Die Schülerinnen und Schüler beschreiben die Lage von Gegenständen mit Begriffen wie über, unter, neben, vor, hinter, links und rechts und verfolgen und beschreiben Wege auf einem Gitter (Zusammenfassung).",
              "Lage und Richtung: oben, unten, links, rechts",
              "Lagebeziehungen Klasse 1 – Arbeitsblätter mit Lösungen",
              "Lage und Richtung",
              "Lage und Richtung für Klasse 1: über, unter, neben, vor, hinter, oben und unten, links und rechts und Wege auf dem Gitter. 100 Übungsaufgaben mit Bildern und Lösungen, kostenlos.",
              "Über, unter, neben, vor, hinter",
              "Schritte genau zählen.",
              body, faq, sets, 15, grade="klasse-1")


if __name__ == "__main__":
    main()
