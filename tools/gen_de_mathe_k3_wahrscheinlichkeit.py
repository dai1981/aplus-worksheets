# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 3: Wahrscheinlichkeit – sicher, möglich, unmöglich（Leitidee Daten und Zufall）
  python3 tools/gen_de_mathe_k3_wahrscheinlichkeit.py
Sicher, möglich oder unmöglich; Würfeln; Kugeln im Beutel; Glücksräder; Zufall im Alltag.
Fehler: „möglich“ und „sicher“ verwechselt, die Farbe mit der größten Kugel statt der größten Anzahl gewählt, Glücksrad nach Anzahl der Felder statt nach Größe beurteilt.
"""
import math
import random
from de_common import mcq, lesson, example, make_unit, mix, wrap
from ws_common import text, INK

R = random.Random(49019)
COL = {"rot": "#e57373", "blau": "#64b5f6", "grün": "#81c784", "gelb": "#ffd54f"}
ADJ = {"rot": "rote", "blau": "blaue", "grün": "grüne", "gelb": "gelbe"}
SMU = ["sicher", "möglich", "unmöglich", "Das kann man nicht sagen."]


def N(c):
    return c.capitalize()


def kug(counts):
    parts = ["%d %s" % (n, ADJ[c]) for c, n in counts.items()]
    return "diese Kugeln: " + (parts[0] if len(parts) == 1 else ", ".join(parts[:-1]) + " und " + parts[-1])


def beutel(counts):
    """Kugeln in einem Beutel: counts = {farbe: anzahl}"""
    balls = [f for f, n in counts.items() for _ in range(n)]
    rnd = random.Random(len(balls) * 31 + sum(ord(c[0]) * n for c, n in counts.items()))
    rnd.shuffle(balls)
    s = ["<path d='M30 40 Q20 150 110 150 Q200 150 190 40 Z' fill='#f3ead9' stroke='%s' stroke-width='2'/>" % INK,
         "<path d='M30 40 Q110 20 190 40' fill='none' stroke='%s' stroke-width='2'/>" % INK]
    for i, f in enumerate(balls):
        r, c = divmod(i, 6)
        s.append("<circle cx='%d' cy='%d' r='10' fill='%s' stroke='%s'/>" % (52 + c * 23 + (r % 2) * 10, 62 + r * 22, COL[f], INK))
    return wrap(220, 160, "".join(s), "Beutel mit Kugeln")


def rad(sectors):
    """Glücksrad: sectors = [(farbe, anteil in Achteln)]"""
    cx = cy = 70
    r = 60
    s, a = [], -90.0
    for f, k in sectors:
        a2 = a + k * 45
        x1, y1 = cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a))
        x2, y2 = cx + r * math.cos(math.radians(a2)), cy + r * math.sin(math.radians(a2))
        if k == 8:
            s.append("<circle cx='%d' cy='%d' r='%d' fill='%s' stroke='%s'/>" % (cx, cy, r, COL[f], INK))
        else:
            s.append("<path d='M%d %d L%.1f %.1f A%d %d 0 %d 1 %.1f %.1f Z' fill='%s' stroke='%s' stroke-width='1.5'/>"
                     % (cx, cy, x1, y1, r, r, 1 if k > 4 else 0, x2, y2, COL[f], INK))
        a = a2
    s.append("<path d='M%d %d l-7 -14 h14 Z' fill='%s'/>" % (cx, cy - r + 10, INK))
    s.append("<circle cx='%d' cy='%d' r='4' fill='%s'/>" % (cx, cy, INK))
    return s


def rad_svg(sectors):
    return wrap(140, 140, "".join(rad(sectors)), "Glücksrad")


def smu():
    kind = R.choice(["wuerfel", "beutel"])
    if kind == "wuerfel":
        q, a = R.choice([
            ("Du würfelst mit einem normalen Spielwürfel. Du würfelst eine 7.", "unmöglich"),
            ("Du würfelst mit einem normalen Spielwürfel. Du würfelst eine 6.", "möglich"),
            ("Du würfelst mit einem normalen Spielwürfel. Die Augenzahl ist kleiner als 7.", "sicher"),
            ("Du würfelst mit einem normalen Spielwürfel. Die Augenzahl ist eine gerade Zahl.", "möglich"),
            ("Du würfelst mit einem normalen Spielwürfel. Du würfelst eine 0.", "unmöglich"),
            ("Du würfelst mit einem normalen Spielwürfel. Die Augenzahl ist größer als 0.", "sicher"),
        ])
        return mcq(q + " Ist das sicher, möglich oder unmöglich?", a, [x for x in SMU if x != a],
                   "Ein Spielwürfel hat die Augenzahlen 1 bis 6. Also ist es <b>%s</b>." % a)
    colors = R.sample(list(COL), R.randint(1, 3))
    counts = {c: R.randint(1, 5) for c in colors}
    pull = R.choice(list(COL))
    if pull in counts and len(counts) == 1:
        a = "sicher"
    elif pull in counts:
        a = "möglich"
    else:
        a = "unmöglich"
    q = beutel(counts) + "Im Beutel sind %s. Du ziehst ohne hinzusehen eine Kugel. Sie ist %s. Ist das sicher, möglich oder unmöglich?" % (
        kug(counts), pull)
    return mcq(q, a, [x for x in SMU if x != a],
               {"sicher": "Im Beutel sind nur %s Kugeln. Es ist <b>sicher</b>." % ADJ[pull],
                "möglich": "Es gibt %s Kugeln, aber auch andere. Es ist <b>möglich</b>." % ADJ[pull],
                "unmöglich": "Im Beutel ist keine %s Kugel. Es ist <b>unmöglich</b>." % ADJ[pull]}[a])


def kugeln():
    colors = R.sample(list(COL), 3)
    ns = R.sample(range(1, 8), 3)
    counts = dict(zip(colors, ns))
    kind = R.choice(["am", "am", "wenig", "keine"])
    if kind == "am":
        a = max(counts, key=counts.get)
        q = "Im Beutel sind %s. Welche Farbe ziehst du am wahrscheinlichsten?" % kug(counts)
        e = "Von den %sn Kugeln gibt es die meisten (%d)." % (ADJ[a], counts[a])
    elif kind == "wenig":
        a = min(counts, key=counts.get)
        q = "Im Beutel sind %s. Welche Farbe ziehst du am unwahrscheinlichsten?" % kug(counts)
        e = "Von den %sn Kugeln gibt es die wenigsten (%d)." % (ADJ[a], counts[a])
    else:
        missing = [c for c in COL if c not in counts][0]
        a = missing
        q = "Im Beutel sind %s. Welche Farbe kannst du <b>nicht</b> ziehen?" % kug(counts)
        e = "Es gibt keine %s Kugel im Beutel." % ADJ[missing]
        return mcq(beutel(counts) + q, N(a), [N(c) for c in counts], e + " Richtig: <b>%s</b>." % N(a))
    return mcq(beutel(counts) + q, N(a), [N(c) for c in COL if c != a], e + " Richtig: <b>%s</b>." % N(a))


def kugeln_dazu():
    colors = R.sample(list(COL), 2)
    a, b = R.randint(2, 6), R.randint(2, 6)
    if a == b:
        return None
    c1, c2 = colors
    need = abs(a - b)
    less = c1 if a < b else c2
    q = "Im Beutel sind %d %s und %d %s Kugeln. Wie viele %s Kugeln musst du dazulegen, damit beide Farben gleich wahrscheinlich sind?" % (
        a, ADJ[c1], b, ADJ[c2], ADJ[less])
    return mcq(q, str(need), [str(x) for x in (need + 1, need - 1 if need > 1 else need + 2, max(a, b), a + b) if x != need],
               "Gleich wahrscheinlich heißt gleich viele: %d − %d = <b>%d</b>." % (max(a, b), min(a, b), need))


RAEDER = [
    [("rot", 4), ("blau", 2), ("grün", 2)], [("rot", 2), ("blau", 6)], [("gelb", 5), ("grün", 3)], [("blau", 3), ("rot", 3), ("gelb", 2)],
    [("grün", 6), ("rot", 1), ("blau", 1)], [("rot", 1), ("gelb", 1), ("blau", 4), ("grün", 2)], [("gelb", 2), ("blau", 2), ("rot", 4)],
    [("grün", 3), ("gelb", 3), ("rot", 2)], [("blau", 5), ("rot", 2), ("gelb", 1)], [("rot", 7), ("grün", 1)],
]


def gluecksrad():
    sec = R.choice(RAEDER)
    sec = sec[:]
    R.shuffle(sec)
    ks = dict((f, k) for f, k in sec)
    kind = R.choice(["am", "wenig", "nie", "gleich"])
    if kind == "am":
        mx = max(ks.values())
        if list(ks.values()).count(mx) > 1:
            return None
        a = max(ks, key=ks.get)
        q = "Auf welcher Farbe bleibt der Zeiger am wahrscheinlichsten stehen?"
        e = "%s hat das größte Feld." % a.capitalize()
    elif kind == "wenig":
        mn = min(ks.values())
        if list(ks.values()).count(mn) > 1:
            return None
        a = min(ks, key=ks.get)
        q = "Auf welcher Farbe bleibt der Zeiger am unwahrscheinlichsten stehen?"
        e = "%s hat das kleinste Feld." % a.capitalize()
    elif kind == "nie":
        miss = [c for c in COL if c not in ks]
        if not miss or len(ks) < 3:
            return None
        a = miss[0]
        q = "Auf welcher Farbe kann der Zeiger <b>nicht</b> stehen bleiben?"
        e = "%s kommt auf dem Glücksrad nicht vor." % a.capitalize()
        return mcq(rad_svg(sec) + q, N(a), [N(c) for c in list(ks)[:3]], e + " Richtig: <b>%s</b>." % N(a))
    else:
        same = [(f, g) for f in ks for g in ks if f < g and ks[f] == ks[g]]
        if not same:
            return None
        f, g = same[0]
        a = "%s und %s" % (N(f), N(g))
        others = [x for x in ks if x not in (f, g)]
        w = ["%s und %s" % tuple(N(x) for x in sorted((f, o))) for o in others] + ["%s und %s" % tuple(N(x) for x in sorted((g, o))) for o in others] + ["Alle Farben gleich"]
        q = "Welche zwei Farben sind gleich wahrscheinlich?"
        e = "%s und %s haben gleich große Felder." % (N(f), N(g))
        return mcq(rad_svg(sec) + q, a, w, e + " Richtig: <b>%s</b>." % a)
    return mcq(rad_svg(sec) + q, N(a), [N(c) for c in COL if c != a], e + " Richtig: <b>%s</b>." % N(a))


ALLTAG = [
    ("Nach Montag kommt Dienstag.", "sicher"), ("Ein Tag hat 25 Stunden.", "unmöglich"), ("Beim Münzwurf fällt Zahl.", "möglich"),
    ("Morgen regnet es.", "möglich"), ("Eine Woche hat 8 Tage.", "unmöglich"),
    ("Nach dem Winter kommt der Frühling.", "sicher"), ("Bei einer Verlosung gewinnst du den Hauptpreis.", "möglich"),
    ("Ein Jahr hat 13 Monate.", "unmöglich"), ("Du ziehst aus einem Beutel mit nur roten Kugeln eine rote Kugel.", "sicher"),
    ("Heute gibt es in der Schule Nudeln zum Mittagessen.", "möglich"), ("Ein Würfel zeigt nach dem Wurf eine 8.", "unmöglich"),
    ("Nach 9 Uhr kommt 10 Uhr.", "sicher"),
]


def alltag():
    kind = R.choice(["satz", "satz", "satz", "gewinn"])
    if kind == "satz":
        st, a = R.choice(ALLTAG)
        return mcq("„%s“ Ist das sicher, möglich oder unmöglich?" % st, a, [x for x in SMU if x != a],
                   "Das ist <b>%s</b>." % a)
    n_win = R.randint(1, 4)
    n_lose = R.randint(n_win + 1, 12)
    q = "In einer Lostrommel sind %d Gewinne und %d Nieten. Was ist wahrscheinlicher?" % (n_win, n_lose)
    return mcq(q, "eine Niete ziehen", ["einen Gewinn ziehen", "beides gleich wahrscheinlich", "Das kann man nicht sagen."],
               "Es gibt mehr Nieten (%d) als Gewinne (%d). Eine <b>Niete</b> ist wahrscheinlicher." % (n_lose, n_win))


def main():
    seen = set()
    sets = [
        ("Sicher, möglich oder unmöglich?", mix(R, seen, [(smu, 20)])),
        ("Kugeln im Beutel", mix(R, seen, [(kugeln, 14), (kugeln_dazu, 6)])),
        ("Glücksräder", mix(R, seen, [(gluecksrad, 20)])),
        ("Gleich wahrscheinlich?", mix(R, seen, [(kugeln_dazu, 10), (kugeln, 10)])),
        ("Zufall im Alltag", mix(R, seen, [(alltag, 14), (smu, 6)])),
    ]
    body = lesson(
        ["<b>Sicher</b>: Es passiert auf jeden Fall. <b>Möglich</b>: Es kann passieren, muss aber nicht. <b>Unmöglich</b>: Es kann nie passieren.",
         "Je mehr Kugeln einer Farbe im Beutel sind, desto <b>wahrscheinlicher</b> ziehst du diese Farbe.",
         "Bei einem Glücksrad kommt es auf die <b>Größe</b> der Felder an, nicht auf ihre Anzahl.",
         "Sind von zwei Farben gleich viele Kugeln da, sind beide <b>gleich wahrscheinlich</b>."],
        [example("Im Beutel: 5 rote, 2 blaue Kugeln. Was ziehst du wahrscheinlicher?", ["5 rote sind mehr als 2 blaue"], "eine rote Kugel"),
         example("Ein Würfel zeigt eine 7.", ["Ein Würfel hat nur 1 bis 6"], "unmöglich")],
        [["Möglich und sicher verwechseln", "Sicher heißt: Es passiert immer. Möglich heißt: Es kann passieren."],
         ["Wahrscheinlich heißt sicher", "Auch das Wahrscheinliche passiert nicht immer"],
         ["Glücksrad: Farbe mit den meisten Feldern", "Die Größe der Felder zählt"]])
    faq = [
        {"q": "Was lernen Kinder in Klasse 3 über Wahrscheinlichkeit?", "a": "Sie beschreiben Ereignisse mit sicher, möglich und unmöglich, vergleichen Chancen (wahrscheinlicher, weniger wahrscheinlich) und begründen mit Anzahlen oder Flächen."},
        {"q": "Muss man schon Brüche für Wahrscheinlichkeiten kennen?", "a": "Nein. In der Grundschule werden Chancen vor allem mit Worten und Vergleichen beschrieben."},
        {"q": "Wie kann man Zufall erleben?", "a": "Mit Würfeln, Münzen, Glücksrädern und Kugeln im Beutel. Viele Würfe zeigen, welche Ergebnisse häufiger vorkommen."},
        {"q": "Welche Leitidee ist das?", "a": "Daten und Zufall, eine der fünf Leitideen der Bildungsstandards Mathematik für die Grundschule."},
    ]
    make_unit(R, "wahrscheinlichkeit", "D",
              "Die Schülerinnen und Schüler beschreiben Zufallsereignisse mit Grundbegriffen (sicher, möglich, unmöglich, wahrscheinlich) und vergleichen Gewinnchancen bei einfachen Zufallsexperimenten (Zusammenfassung).",
              "Wahrscheinlichkeit: sicher, möglich, unmöglich",
              "Wahrscheinlichkeit Klasse 3 – sicher, möglich, unmöglich, Arbeitsblätter mit Lösungen",
              "Wahrscheinlichkeit",
              "Wahrscheinlichkeit für Klasse 3: sicher, möglich oder unmöglich, Würfel, Kugeln im Beutel, Glücksräder und Zufall im Alltag. 100 Übungsaufgaben mit Lösungen, kostenlos.",
              "Sicher, möglich oder unmöglich?",
              "Mehr Kugeln oder ein größeres Feld bedeuten eine größere Chance.",
              body, faq, sets, 19)


if __name__ == "__main__":
    main()
